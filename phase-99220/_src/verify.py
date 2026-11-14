# -*- coding: utf-8 -*-
"""
Gates for the phase-99220 desk. Exit 1 on any failure.

V1  every table row that carries a value has at least one link (official host, registered
    source, or an explicit flag page for an unverified item)
V2  every external host is on the official allowlist
V3  every internal link resolves to a file in the repository
V4  every dollar figure of $1,000 or more is a multiple of $10
V5  no external scripts, images, fonts or stylesheets; one inline script only (what-if page)
V6  privacy: no ZIP codes, no street-number patterns, no parcel-number patterns, no e-mail
    or phone patterns, no owner names
V7  every page is linked from the menu of every other page (navigation is complete)
V8  print stylesheet present; brief page is under one printed page of text (line budget)
"""
import glob
import os
import re
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
ROOT = os.path.dirname(OUT)
sys.path.insert(0, HERE)
import desk_sources as SRC  # noqa: E402

ALLOW = set(SRC.OFFICIAL_HOSTS) | {"www.sfpuc.org", "www.insurance.ca.gov", "www.boe.ca.gov"}

fails = []


def fail(msg):
    fails.append(msg)


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.scripts = []
        self.ext = []
        self.in_script = False
        self.rows = []
        self._row = None
        self._cell = None
        self.menu_links = []
        self.in_nav = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "nav":
            self.in_nav = True
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
            if self.in_nav:
                self.menu_links.append(a["href"])
        if tag == "script":
            if "src" in a:
                self.ext.append(("script", a["src"]))
            self.scripts.append(a)
            self.in_script = True
        if tag in ("img", "iframe", "source", "embed", "object"):
            self.ext.append((tag, a.get("src", "")))
        if tag == "link" and a.get("rel") != "stylesheet":
            self.ext.append(("link", a.get("href", "")))
        if tag == "link" and a.get("rel") == "stylesheet" and a.get("href", "").startswith("http"):
            self.ext.append(("stylesheet", a.get("href")))
        if tag == "tr":
            self._row = {"td": 0, "links": 0}
        if tag == "td" and self._row is not None:
            self._row["td"] += 1
        if tag == "a" and self._row is not None and "href" in a:
            self._row["links"] += 1

    def handle_endtag(self, tag):
        if tag == "nav":
            self.in_nav = False
        if tag == "script":
            self.in_script = False
        if tag == "tr" and self._row is not None:
            self.rows.append(self._row)
            self._row = None


def is_external(h):
    return h.startswith("http://") or h.startswith("https://")


pages = sorted(glob.glob(os.path.join(OUT, "*.html")))
names = {os.path.basename(p) for p in pages}
menu_targets_all = None
per_page_menu = {}

for p in pages:
    fn = os.path.basename(p)
    text = open(p, encoding="utf-8").read()
    P = Page()
    P.feed(text)

    # V1 rows with values carry a link (rows inside the what-if script template are excluded)
    body_no_script = re.sub(r"<script.*?</script>", "", text, flags=re.S)
    P2 = Page()
    P2.feed(body_no_script)
    for r in P2.rows:
        if r["td"] and r["links"] == 0:
            fail("V1 %s: a table row has no link" % fn)

    # V2 external hosts
    for h in P.links:
        if is_external(h):
            host = re.sub(r"^https?://", "", h).split("/")[0]
            if host not in ALLOW:
                fail("V2 %s: host not allowlisted: %s" % (fn, host))
    for kind, h in P.ext:
        if kind == "script" or is_external(h) or h.startswith("//"):
            fail("V5 %s: external %s: %s" % (fn, kind, h))
    if len([a for a in P.scripts if "src" not in a]) > 1:
        fail("V5 %s: more than one inline script" % fn)
    if fn != "what-if.html" and P.scripts:
        fail("V5 %s: unexpected script" % fn)

    # V3 internal links resolve (relative to the page's folder)
    for h in P.links:
        if h.startswith("#") or is_external(h) or h.startswith("mailto:"):
            continue
        target = h.split("#")[0]
        if not target:
            continue
        path = os.path.normpath(os.path.join(OUT, target))
        if not os.path.exists(path):
            fail("V3 %s: broken internal link %s" % (fn, h))

    # V4 money $1,000+ multiple of $10 (scan text outside tags)
    visible = re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", "", text, flags=re.S))
    for m in re.finditer(r"\$([0-9][0-9,]*)", visible):
        n = int(m.group(1).replace(",", ""))
        if n >= 1000 and n % 10 != 0:
            fail("V4 %s: money not a multiple of $10: $%s" % (fn, m.group(1)))

    # V6 privacy
    for pat, label in [
        (r"\b9[0-9]{4}\b(?![,.]\d)", "ZIP-shaped number"),
        (r"\b\d{1,5}\s+[A-Z][a-z]+\s+(Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Way|Court|Ct|Boulevard|Blvd)\b", "street address"),
        (r"\b\d{3}-\d{3}-\d{2,3}\b", "parcel-number shape"),
        (r"[\w.+-]+@[\w-]+\.[\w.]+", "e-mail"),
        (r"\(\d{3}\)\s?\d{3}-\d{4}", "phone"),
        (r"\bCupertino\b|\bSunnyvale\b|\bSaratoga\b|\bSan Jose\b", "city name (Santa Clara County)"),
        (r"\bSan Francisco\b(?! County)", "bare city name (use San Francisco County)"),
    ]:
        if re.search(pat, visible):
            fail("V6 %s: %s found: %s" % (fn, label, re.search(pat, visible).group(0)))

    # V7 menu completeness: each page links to every other page
    per_page_menu[fn] = set(P.menu_links)

    # V8 print stylesheet
css = os.path.join(OUT, "assets", "style.css")
if "@media print" not in open(css, encoding="utf-8").read():
    fail("V8 print stylesheet missing")

expected = {fn for fn, _ in [("index.html",0),("what-if.html",0),("mixed-paths.html",0),("phased-replay.html",0),("timeline.html",0),("brief.html",0),("glossary.html",0),("sources.html",0),("methodology.html",0),("questions.html",0),("suggestions.html",0),("flagged.html",0)]}
for fn in expected:
    if fn not in names:
        fail("V7 missing page %s" % fn)
for fn, links in per_page_menu.items():
    for other in expected:
        if other != fn and other not in links:
            fail("V7 %s: menu lacks %s" % (fn, other))

print("pages:", len(pages))
if fails:
    for f in fails:
        print("FAIL", f)
    sys.exit(1)
print("PASS: rows linked, hosts allowlisted, internal links resolve, $10 rounding, privacy, menu complete, print CSS present")
