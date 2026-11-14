# -*- coding: utf-8 -*-
"""
Structural, sourcing, privacy and rounding verification for the cbd/ desk.

Run:   python3 cbd/_src/verify.py      (non-zero exit on any failure)

  V1  every table body row links an official source OR carries an explicit no-source marker
  V2  every external link is https on an official host from sources.OFFICIAL_HOSTS
  V3  every internal link resolves to a file that exists in the repository
  V4  every money figure is a multiple of $10
  V5  no personal or geographic identifier (city, county, ZIP, street, APN-style number)
  V6  no NaN, Infinity, None or undefined leaked into the output
  V7  no script, iframe, form, embedded object, external asset or inline event handler
  V8  the source register is internally consistent (status, host, reused flags)
  V9  every built page exists, nothing extra is published, and the navigation resolves
  V10 the model reproduces the owner-brief desk's own published figures (cbe/options.html)
"""

import html as htmlmod
import os
import re
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)           # cbd/
ROOT = os.path.dirname(OUT)           # repository root
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import desk_sources as S  # noqa: E402

PAGES = ["index.html", "paths.html", "phased.html", "timeline.html", "brief.html",
         "questions.html", "glossary.html", "suggestions.html", "sources.html",
         "flagged.html", "method.html"]

FORBIDDEN = [
    r"cupertino", r"san\s+francisco", r"santa\s+clara", r"sunset", r"\b9501\d\b", r"\b9412\d\b",
    r"\b\d{1,5}\s+[A-Z][a-z]+\s+(street|st|avenue|ave|road|rd|drive|dr|lane|ln|boulevard|blvd|court|ct|way)\b",
    r"\b\d{3}-\d{3}-\d{3}\b", r"@", r"\(\d{3}\)\s*\d{3}-\d{4}", r"\bsan\s+mateo\b", r"\balameda\b",
    r"\bsanta\s+cruz\b", r"\bbay\s+area\b", r"\bcalifornia\s+county\b",
]

errors = []
warnings = []

# Statutory amounts quoted verbatim from the source, as the cbe desk does. The Proposition 19
# allowance of $1,044,586 is BOE LTA 2025/009 (not re-opened here; flag F14).
STATUTORY_LITERALS = {"1,044,586"}


class Collect(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.in_tbody = False
        self.rows = []
        self.cur = None
        self.text = []
        self.tags = []
        self.attrs_all = []
        self.in_style = False

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        self.tags.append(tag)
        self.attrs_all.append((tag, d))
        if tag == "a" and "href" in d:
            self.links.append((d["href"], d.get("rel", "")))
        if tag == "tbody":
            self.in_tbody = True
        if tag == "tr" and self.in_tbody:
            self.cur = {"html": []}
        if tag == "style":
            self.in_style = True

    def handle_endtag(self, tag):
        if tag == "tbody":
            self.in_tbody = False
        if tag == "tr" and self.cur is not None:
            self.rows.append(self.cur)
            self.cur = None
        if tag == "style":
            self.in_style = False

    def handle_data(self, data):
        if not self.in_style:
            self.text.append(data)
        if self.cur is not None:
            self.cur["html"].append(data)


def load(name):
    with open(os.path.join(OUT, name), encoding="utf-8") as f:
        raw = f.read()
    c = Collect()
    c.feed(raw)
    return raw, c


def check_rows(name, raw, c):
    """V1: every tbody row has an official link or an explicit no-source marker."""
    # re-scan raw HTML rows, which keeps the marker class
    for m in re.finditer(r"<tbody>(.*?)</tbody>", raw, re.S):
        for r in re.finditer(r"<tr>(.*?)</tr>", m.group(1), re.S):
            body = r.group(1)
            has_official = any(_official(h) for h, _ in re.findall(r'href="([^"]+)"([^>]*)', body))
            has_marker = ('class="nosrc"' in body) or ("No official source" in body)
            if not (has_official or has_marker):
                errors.append("V1 %s: table row has no official link and no no-source marker: %s"
                              % (name, htmlmod.unescape(re.sub(r"<[^>]+>", " ", body))[:120]))


def _official(href):
    m = re.match(r"https://([^/]+)/", href)
    return bool(m) and m.group(1) in S.OFFICIAL_HOSTS


def check_links(name, c):
    """V2 external hosts; V3 internal targets exist."""
    for href, _ in c.links:
        if href.startswith("http://"):
            errors.append("V2 %s: non-https link %s" % (name, href))
        elif href.startswith("https://"):
            if not _official(href):
                errors.append("V2 %s: link host not on the official allowlist: %s" % (name, href))
        elif href.startswith("mailto:") or href.startswith("#"):
            continue
        else:
            target = href.split("#")[0]
            if not target:
                continue
            path = os.path.normpath(os.path.join(OUT, target))
            if not os.path.exists(path):
                errors.append("V3 %s: broken internal link %s" % (name, href))


def check_money(name, text):
    """V4: every $ figure is a whole multiple of $10 (no cents, no odd tens)."""
    for m in re.finditer(r"\$\s?([0-9][0-9,]*)(\.\d+)?", text):
        if m.group(2):
            errors.append("V4 %s: money has cents: %s" % (name, m.group(0)))
            continue
        val = int(m.group(1).replace(",", ""))
        if val % 10 and m.group(1) not in STATUTORY_LITERALS:
            errors.append("V4 %s: money not a multiple of $10: %s" % (name, m.group(0)))


def check_pii(name, text):
    """V5: no city, county, ZIP, street, phone, e-mail or parcel-style identifier."""
    for pat in FORBIDDEN:
        for m in re.finditer(pat, text, re.I):
            errors.append("V5 %s: possible identifier '%s' near: ...%s..."
                          % (name, m.group(0), text[max(0, m.start() - 40):m.end() + 40].replace("\n", " ")))


def check_values(name, text):
    """V6: no NaN, Infinity, None or undefined in the output."""
    for pat in [r"\bNaN\b", r"\bInfinity\b", r"\bNone\b", r"\bundefined\b", r"\bnull\b"]:
        for m in re.finditer(pat, text):
            errors.append("V6 %s: %s leaked: ...%s..." % (name, m.group(0), text[max(0, m.start() - 40):m.end() + 40]))


def check_markup(name, raw, c):
    """V7: no script, iframe, form, embed, external asset or inline handler."""
    for bad in ["<script", "<iframe", "<form", "<embed", "<object", "<link ", "<img "]:
        if bad in raw.lower():
            errors.append("V7 %s: forbidden markup %s" % (name, bad.strip()))
    for m in re.finditer(r"\son[a-z]+\s*=", raw, re.I):
        errors.append("V7 %s: inline event handler %s" % (name, m.group(0).strip()))
    for m in re.finditer(r'<a [^>]*href="https?://[^"]*"([^>]*)>', raw):
        if "noopener" not in m.group(1):
            errors.append("V7 %s: external link without rel=noopener: %s" % (name, m.group(0)[:80]))


def check_register():
    """V8: each source has a known status; opened/reused links use an official https host."""
    for sid, s in S.SOURCES.items():
        if s["status"] not in ("opened", "reused", "internal"):
            errors.append("V8 register: %s has unknown status %s" % (sid, s["status"]))
        if s["status"] in ("opened", "reused") and not _official(s["url"]):
            errors.append("V8 register: %s is not on an official host: %s" % (sid, s["url"]))
        if s["status"] == "opened" and "Retrieved 2026-11-14" not in s["read"]:
            errors.append("V8 register: %s is marked opened without a retrieval statement" % sid)
        if s["status"] == "reused" and "not re-opened" not in s["read"].lower():
            errors.append("V8 register: %s is reused but does not say so" % sid)


def check_pages_and_nav():
    """V9: every page exists, no extra HTML, navigation resolves."""
    present = sorted(f for f in os.listdir(OUT) if f.endswith(".html"))
    if sorted(PAGES) != present:
        errors.append("V9 page set mismatch: expected %s, found %s" % (sorted(PAGES), present))
    for name in PAGES:
        if not os.path.exists(os.path.join(OUT, name)):
            errors.append("V9 missing page %s" % name)


def check_against_cbe():
    """V10: the cbd model reproduces the owner-brief desk's published figures for paths A, B, C."""
    import desk_model as dm
    import model as cm  # the read-only cbe model
    r = cm.compare()
    t = dm.paths_for_transfer(2045)
    pairs = [("A", t["A"]["pv"], r["npv_occupy_cash"]),
             ("B", t["B"]["pv"], r["npv_rent_cash"]),
             ("C", t["C"]["pv"], r["npv_sell_cash"])]
    for pid, mine, theirs in pairs:
        if abs(mine - theirs) > 10:      # rounding to the nearest $10 allowed
            errors.append("V10 path %s differs from cbe: %.2f vs %.2f" % (pid, mine, theirs))
    # the phased engine with no crash and no tranches must equal plain compounding
    years = 31
    if abs(dm.phased_value(1, years) - (1 + dm.EQ_NET) ** years) > 1e-9:
        errors.append("V10 lump sum does not compound at the net return")


def main():
    for name in PAGES:
        raw, c = load(name)
        text = htmlmod.unescape(re.sub(r"<style.*?</style>", " ", raw, flags=re.S))
        text = re.sub(r"<[^>]+>", " ", text)
        check_rows(name, raw, c)
        check_links(name, c)
        check_money(name, text)
        check_pii(name, text)
        check_values(name, text)
        check_markup(name, raw, c)
    check_register()
    check_pages_and_nav()
    check_against_cbe()

    if errors:
        for e in errors:
            print("FAIL", e)
        print("cbd verify: %d failure(s)" % len(errors))
        return 1
    print("cbd verify PASS: %d pages; every table row sourced or marked; $10 rounding; no identifiers; "
          "no script; %d registered sources; model reproduces cbe figures." % (len(PAGES), len(S.SOURCES)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
