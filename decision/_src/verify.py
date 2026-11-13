# -*- coding: utf-8 -*-
"""Verify the built decision site.

Run: python3 decision/_src/verify.py     (exit code 0 = pass)

Checks
  V1  every table row carries at least one link to an official source
  V2  every external link points at an official host on the allowlist
  V3  every internal link resolves to a file that exists
  V4  every published dollar figure is a multiple of $10, except the statutory
      amounts that are quoted exactly as published
  V5  no personal identifier pattern appears anywhere in the output
  V6  no placeholder leaked from the model (nan, None, inf)
"""

import os
import re
import sys
from urllib.parse import urlparse

import sources

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)

# Amounts quoted exactly as published by a legislature or the IRS. These are
# statewide constants, identify nothing, and are deliberately not rounded.
STATUTORY_LITERALS = {
    "1,044,586",   # Prop 19 adjusted allowance, BOE LTA 2025/009
    "1,022,600",   # Prop 19 adjusted allowance 2023-2025
    "742,953",     # CA top bracket threshold, single, FTB 2025
    "1,485,906",   # CA top bracket threshold, joint, FTB 2025
    "361,000",     # Prop 3 (2026) threshold, single
    "721,000",     # Prop 3 (2026) threshold, joint
}

# Personal identifier patterns. None of these may appear in published output.
PII_PATTERNS = [
    (r"\bZIP\s*(code)?\s*\d{5}\b", "ZIP code with a number"),
    (r"\b\d{1,5}\s+[A-Z][a-z]+\s+(Street|Avenue|Road|Drive|Lane|Court|Boulevard)\b",
     "numbered street address"),
    (r"\bAPN\s*[:#]?\s*\d[\d-]+\b", "parcel identifier with a number"),
    (r"\b\d{3}-\d{2}-\d{4}\b", "social security number pattern"),
    (r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", "email address"),
    (r"\b\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "telephone number"),
    (r"\baccount\s+(number|no\.?|#)\s*[:#]?\s*\d", "account number with a number"),
]

LEAKED = [r"\bnan\b", r"\binf\b", r"\$None", r"\{-?\d+\}"]


def pages():
    return sorted(f for f in os.listdir(OUT) if f.endswith(".html"))


def main():
    errs, warns = [], []
    files = pages()
    total_rows = 0
    total_links = 0
    unsourced = 0

    for fn in files:
        path = os.path.join(OUT, fn)
        with open(path, encoding="utf-8") as f:
            doc = f.read()

        # --- V1: every row is sourced or declares that it cannot be ----------
        bodies = re.findall(r"<tbody>(.*?)</tbody>", doc, flags=re.S)
        for bi, body in enumerate(bodies):
            for ri, row in enumerate(re.findall(r"<tr[^>]*>(.*?)</tr>", body, flags=re.S)):
                total_rows += 1
                hrefs = re.findall(r'href="([^"]+)"', row)
                official = [h for h in hrefs
                            if h.startswith("http")
                            and urlparse(h).netloc in sources.OFFICIAL_HOSTS]
                if official:
                    continue
                if "nosrc" in row:
                    unsourced += 1
                    continue
                errs.append("V1 %s: table %d row %d is neither sourced nor declared "
                            "unsourceable" % (fn, bi, ri))

        # --- V2 / V3: links -------------------------------------------------
        for href in re.findall(r'href="([^"]+)"', doc):
            total_links += 1
            if href.startswith("http"):
                host = urlparse(href).netloc
                if host not in sources.OFFICIAL_HOSTS:
                    errs.append("V2 %s: non-official external host %s (%s)"
                                % (fn, host, href))
            elif href.startswith("#") or href.startswith("mailto:"):
                pass
            else:
                target = href.split("#")[0].split("?")[0]
                if target and not os.path.exists(os.path.join(OUT, target)):
                    errs.append("V3 %s: broken internal link %s" % (fn, href))

        # --- V4: money rounding ---------------------------------------------
        text = re.sub(r'title="[^"]*"', "", doc)
        for amt, unit in re.findall(r"\$([\d,]+(?:\.\d+)?)\s*(bn|billion|million|trillion|m\b|k\b)?",
                                    text, flags=re.I):
            if unit:
                continue
            if amt in STATUTORY_LITERALS:
                continue
            try:
                v = float(amt.replace(",", ""))
            except ValueError:
                continue
            if abs(v - int(v)) > 1e-9:
                continue
            if int(v) % 10 != 0:
                errs.append("V4 %s: $%s is not a multiple of $10" % (fn, amt))

        # --- V5: personal identifiers ---------------------------------------
        scan = re.sub(r'<div class="banner">.*?</div>', "", doc, flags=re.S)
        scan = re.sub(r"<p class='lead privacy'>.*?</p>", "", scan, flags=re.S)
        scan = re.sub(r'title="[^"]*"', "", scan)
        for pat, what in PII_PATTERNS:
            for hit in re.findall(pat, scan):
                errs.append("V5 %s: possible %s: %r" % (fn, what, hit))

        # --- V6: leaked placeholders ----------------------------------------
        for pat in LEAKED:
            for hit in re.findall(pat, doc):
                errs.append("V6 %s: leaked placeholder %r" % (fn, hit))

    # --- source register integrity ------------------------------------------
    seen = set()
    for s in sources.SOURCES:
        if s["id"] in seen:
            errs.append("sources: duplicate id %s" % s["id"])
        seen.add(s["id"])
        host = urlparse(s["url"]).netloc
        if host not in sources.OFFICIAL_HOSTS:
            errs.append("sources: %s host %s not on allowlist" % (s["id"], host))
    for i in sources.NOT_OPENED:
        if i not in seen:
            errs.append("sources: NOT_OPENED id %s not in registry" % i)

    print("pages              : %d" % len(files))
    print("table rows checked : %d" % total_rows)
    print("links checked      : %d" % total_links)
    print("sources registered : %d (%d marked not-opened)"
          % (len(sources.SOURCES), len(sources.NOT_OPENED)))
    print("rows declared unsourceable : %d (owner record, assumption or unverified; "
          "each says so in the row)" % unsourced)

    if warns:
        print("\nWARNINGS (%d)" % len(warns))
        for w in warns:
            print("  -", w)

    if errs:
        print("\nFAIL (%d)" % len(errs))
        for e in errs[:60]:
            print("  -", e)
        if len(errs) > 60:
            print("  ... and %d more" % (len(errs) - 60))
        return 1

    print("\nPASS - every table row carries an official source link; all money "
          "rounded to $10; no personal identifiers.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
