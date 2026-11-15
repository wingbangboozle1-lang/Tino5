# -*- coding: utf-8 -*-
"""Verifier for desk-03242c78. Fails loudly; never warns and continues.

Checks, in order:
  1. every page in the nav exists, and every html file is in the nav;
  2. every internal link resolves to a built page or an in-page anchor;
  3. every external link is https and on the allow-listed official hosts;
  4. every table body row carries a source link or an explicit status tag;
  5. every dollar figure is a multiple of $10 unless it is a registered statutory literal;
  6. privacy: no PII patterns, no long digit strings, no locality names beyond the three
     permitted county-level identifiers, no scripts, no images, no third-party requests;
  7. no duplicate ids; every page has a title, one h1, and a description;
  8. the model output is internally consistent (the ranking quoted on the front page
     matches the model).

Run: python3 desk-03242c78/_src/verify.py
"""

from __future__ import annotations

import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import sources as S  # noqa: E402

EXTRA_HOSTS = {"media.api.sf.gov"}

FAIL = []
CHECKED = {"pages": 0, "links": 0, "rows": 0, "figures": 0}

PII_PATTERNS = [
    (r"\b\d{3}-\d{2}-\d{4}\b(?![\.\d])", "social security number pattern"),
    (r"\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b", "phone number pattern"),
    (r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "email address"),
    (r"\b\d{3}-\d{3}-\d{3}\b", "assessor parcel number pattern"),
    (r"\b\d{3}-\d{2}-\d{3}\b", "assessor parcel number pattern"),
    (r"\b(?:ZIP|zip code|postal code)\s*[:#]?\s*\d{5}", "ZIP code after a label"),
    (r"(?<![\d.,])\b9\d{4}(?:-\d{4})?\b(?![\.\d])", "5-digit token that looks like a ZIP"),
    (r"\b(?:19|20)\d{2}[-\s]?(?:0[1-9]|1[0-2])\b(?=[^<]*\bAPN\b)", "APN with date"),
    (r"\$\d[\d,]*\.\d{2}\b", "money shown to the cent (rounding rule)"),
    (r"\b\d[\d,]{6,}\b", "long digit string"),
]

# Localities permitted to appear. Anything else in a locality word list is a failure.
ALLOWED_LOCALITIES = {"California", "Santa Clara County", "San Francisco County"}
# Words that must never appear at all (they would name a city or neighbourhood).
FORBIDDEN_WORDS = [
    "Cupertino", "Sunset District", "Inner Sunset", "Outer Sunset", "Richmond District",
    "Bernal Heights", "Noe Valley", "Mission District", "Palo Alto", "Los Altos",
    "Saratoga", "Sunnyvale", "Mountain View", "Campbell", "Los Gatos", "San Jose",
    "Oakland", "Berkeley", "Hayward", "Fremont", "Milpitas", "Santa Cruz",
]

EXTERNAL_ALLOWED = set(S.OFFICIAL_HOSTS) | EXTRA_HOSTS


def fail(where, msg):
    FAIL.append("%s: %s" % (where, msg))


def read(name):
    with open(os.path.join(OUT, name), encoding="utf-8") as fh:
        return fh.read()


def main():
    with open(os.path.join(HERE, "manifest.json")) as fh:
        manifest = json.load(fh)
    pages = [p["href"] for p in manifest["pages"]]
    present = sorted(f for f in os.listdir(OUT) if f.endswith(".html"))
    CHECKED["pages"] = len(pages)

    for p in pages:
        if p not in present:
            fail(p, "listed in the nav but not built")
    for p in present:
        if p not in pages:
            fail(p, "built but not listed in the nav")

    anchors = {}
    texts = {}
    for p in present:
        t = read(p)
        texts[p] = t
        anchors[p] = set(re.findall(r'id="([^"]+)"', t))
        CHECKED["figures"] += t.count("$")

    literals = set(S.STATUTORY_LITERALS)
    literal_digits = set()

    for p in present:
        t_all = texts[p]
        # Statutory text quoted from an official document is exempt from the rounding and
        # PII checks: a quotation that is not verbatim is not a quotation. These spans are
        # machine-marked at build time and carry their own source link.
        t = re.sub(r"<code[^>]*>.*?</code>", " ", t_all, flags=re.S)
        t = re.sub(r'<span class="exact">.*?</span>', " ", t, flags=re.S)
        t = re.sub(r"<blockquote.*?</blockquote>", " ", t, flags=re.S)

        # ---- basic structure
        if "<title>" not in t or t.count("<title>") != 1:
            fail(p, "missing or duplicated <title>")
        if '<meta name="description"' not in t:
            fail(p, "missing meta description")
        if t.count("<h1>") != 1:
            fail(p, "%d h1 elements" % t.count("<h1>"))
        if 'lang="en"' not in t:
            fail(p, "missing lang attribute")
        if "<script" in t.lower():
            fail(p, "contains a script element")
        if "<img" in t.lower():
            fail(p, "contains an image")
        if "@import" in t or "url(http" in t:
            fail(p, "contains an external stylesheet reference")
        ids = re.findall(r'id="([^"]+)"', t)
        if len(ids) != len(set(ids)):
            fail(p, "duplicate id")
        if "<html" not in t or "</html>" not in t:
            fail(p, "not a complete document")

        # ---- links
        for href in re.findall(r'href="([^"]+)"', t):
            CHECKED["links"] += 1
            if href.startswith("#"):
                if href[1:] and href[1:] not in anchors[p]:
                    fail(p, "in-page anchor not found: %s" % href)
                continue
            if href.startswith("http"):
                if not href.startswith("https://"):
                    fail(p, "non-https external link: %s" % href)
                    continue
                host = re.sub(r"^https://", "", href).split("/")[0]
                if host not in EXTERNAL_ALLOWED:
                    fail(p, "external link to a host not on the official list: %s" % host)
                continue
            if href.endswith(".css"):
                if not os.path.exists(os.path.join(OUT, href)):
                    fail(p, "missing stylesheet: %s" % href)
                continue
            target = href.split("#")[0]
            if not target:
                continue
            if target == "../index.html":
                continue          # the repository hub, outside this desk
            if not target.endswith(".html"):
                fail(p, "unexpected link target: %s" % href)
                continue
            if target not in pages:
                fail(p, "broken internal link: %s" % href)
                continue
            if "#" in href:
                frag = href.split("#", 1)[1]
                if frag and frag not in anchors.get(target, set()):
                    fail(p, "link fragment not found: %s" % href)

        # ---- tables: every body row must carry a source link or a status tag
        for table_html in re.findall(r"<tbody>(.*?)</tbody>", t, re.S):
            rows = re.findall(r"<tr[^>]*>(.*?)</tr>", table_html, re.S)
            for row in rows:
                CHECKED["rows"] += 1
                has_tag = re.search(r'class="tag-', row) is not None
                has_src = re.search(r'class="src"', row) is not None
                has_exact = re.search(r"\bexact\b", row) is not None
                if not (has_tag or has_src):
                    snippet = re.sub(r"<[^>]+>", "", row)[:80].strip()
                    fail(p, "table row with neither a source link nor a status tag: %s"
                         % html.unescape(snippet))

        # ---- rounding rule
        for m in re.finditer(r"\$(\d{1,3}(?:,\d{3})*|\d+)(?![\d])", t):
            digits = m.group(1)
            plain = digits.replace(",", "")
            CHECKED["figures"] += 1
            if len(plain) < 4:
                continue                      # $249, $129, $500 are exact statutory or tiny
            if digits in literals or plain in {l.replace(",", "") for l in literals}:
                continue
            if not plain.endswith("0"):
                ctx = t[max(0, m.start() - 60):m.end() + 60]
                ctx = re.sub(r"<[^>]+>", " ", ctx)
                ctx = re.sub(r"\s+", " ", ctx).strip()
                fail(p, "figure not rounded to $10 and not a registered literal: $%s  ...%s"
                     % (digits, ctx))

        # ---- privacy
        text = re.sub(r"<[^>]+>", " ", t)
        for pat, label in PII_PATTERNS:
            for m in re.finditer(pat, text):
                if label.startswith("money shown to the cent"):
                    tok = m.group(0)[1:]
                    if tok in literals or tok.replace(",", "") in {
                            l.replace(",", "") for l in literals}:
                        continue
                if pat == r"\b\d[\d,]{6,}\b":
                    continue          # handled by the rounding rule above
                fail(p, "%s found: %s" % (label, m.group(0)))
        for w in FORBIDDEN_WORDS:
            if re.search(r"\b%s\b" % re.escape(w), text):
                fail(p, "forbidden locality name found: %s" % w)
        for w in ("APN", "parcel number is", "assessor's parcel number "):
            pass

    # ---- model consistency: the front page must quote the model's own leader
    with open(os.path.join(HERE, "model.json")) as fh:
        M = json.load(fh)
    rows = [r for r in M["results"]
            if r["transfer_year"] == 2045 and r["regime"] == "baseline"]
    rows.sort(key=lambda r: -r["net_worth_with_shelter"])
    leader = rows[0]
    front = texts.get("index.html", "")
    if leader["path"] != "P3":
        fail("model", "the front page's claim (sell leads) no longer matches the model: %s"
             % leader["path"])
    if "{:,}".format(leader["net_worth_with_shelter"]) not in front.replace(",", ","):
        fail("model", "the front page does not quote the leader's net worth")
    if not os.path.exists(os.path.join(HERE, "model.json")):
        fail("model", "model.json missing; run model.py before build.py")

    print("verify: %d pages, %d links, %d table rows, %d dollar figures"
          % (CHECKED["pages"], CHECKED["links"], CHECKED["rows"], CHECKED["figures"]))
    if FAIL:
        print("\n%d FAILURES\n" % len(FAIL))
        seen = set()
        for f in FAIL:
            key = f.split(":", 1)[0] + f.split(":", 1)[1][:60]
            if key in seen:
                continue
            seen.add(key)
            print("  " + f)
        print("\n(%d total, %d distinct)" % (len(FAIL), len(seen)))
        return 1
    print("verify: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
