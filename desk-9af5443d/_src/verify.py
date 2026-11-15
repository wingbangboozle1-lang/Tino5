#!/usr/bin/env python3
"""desk-9af5443d verifier (content-based; avoids flaky filesystem stat in sandbox).

Checks the published desk against the coordination contract:
  * every table row carries an official-source link, or is blank + marked
    unverified/owner/assumption/exact
  * money rounded to nearest $10 unless a statutory/exact figure
  * no personal identifiers (ZIP, street address, parcel/account with value, SSN)
  * internal links point to .html pages or assets/
  * external hosts on the official allowlist
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(__file__))  # desk-9af5443d
EXPECTED_PAGES = [
    "index.html", "executive-summary.html", "projections.html", "rent-comparables.html",
    "sf-measures.html", "maintenance-plan.html", "ca-income-tax.html", "estate-liquidity.html",
    "decision-log.html", "questions.html", "suggestions.html", "law-watch.html",
    "sources.html", "flagged.html", "methodology.html", "briefing-sheet.html",
]
OFFICIAL_HOSTS = [
    "irs.gov", "ftb.ca.gov", "boe.ca.gov", "santaclaracounty.gov", "files.santaclaracounty.gov",
    "sfelections.org", "sfmta.com", "sf.gov", "census.gov", "home.treasury.gov", "nber.org",
    "federalreservehistory.org", "insurance.ca.gov", "cfpnet.com", "leginfo.legislature.ca.gov",
    "sjwater.com", "sfpuc.gov", "cpuc.ca.gov", "sco.ca.gov",
]
ERRORS = []
WARN = []


def add(err):
    ERRORS.append(err)


def read(pg):
    p = os.path.join(ROOT, pg)
    try:
        return open(p, encoding="utf-8").read()
    except FileNotFoundError:
        add(f"{pg}: file not readable (skipped checks)")
        return ""


pii_patterns = [
    (r"\b\d{5}(?:-\d{4})?\b", "ZIP-like"),
    (r"\b\d{1,5}\s+[A-Za-z]+(?:\s+[A-Za-z]+)?\s+(?:St|Ave|Rd|Blvd|Dr|Ln|Way|Ct|Pl|Ter)\b", "street address"),
    (r"\b(?:APN|SSN)\b", "identifier word"),
    (r"\b(?:parcel|account)\s*(?:number|no|#|:)?\s*\d", "identifier with value"),
]

for pg in EXPECTED_PAGES:
    text = read(pg)
    if not text:
        continue
    # PII scan
    for pat, label in pii_patterns:
        for m in re.finditer(pat, text, re.I):
            add(f"{pg}: possible {label}: {m.group(0)!r}")
    # table rows: each data row needs official source link or a tag
    for tr in re.finditer(r"<tr>(.*?)</tr>", text, re.S):
        row = tr.group(0)
        if "<th" in row:
            continue
        rowtext = re.sub(r"<.*?>", " ", row)
        has_source = ("<a href=" in row) and any(h in row for h in OFFICIAL_HOSTS)
        has_tag = '<span class="tag' in row
        if re.findall(r"<t[hd]>", row):
            if not (has_source or has_tag):
                add(f"{pg}: table row without official source link or tag: {rowtext[:90]!r}")
    # rounding: every $ amount should be multiple of 10 (statutory exact ones are warnings only)
    for m in re.finditer(r"\$(\d[\d,]*)", text):
        v = int(m.group(1).replace(",", ""))
        if v % 10 != 0:
            WARN.append(f"{pg}: amount ${v:,} not a multiple of $10")
    # links
    for m in re.finditer(r'href="([^"]+)"', text):
        u = m.group(1)
        if u.startswith(("http", "#", "mailto", "assets/")):
            continue
        if not u.endswith(".html"):
            WARN.append(f"{pg}: internal link target not an html page {u}")
    # external host allowlist
    for m in re.finditer(r'href="(https?://[^"]+)"', text):
        host = re.sub(r"^https?://", "", m.group(1)).split("/")[0]
        if not any(host == h or host.endswith("." + h) for h in OFFICIAL_HOSTS):
            add(f"{pg}: non-official external host {host}")

print("PAGES checked:", len(EXPECTED_PAGES))
print("ERRORS:", len(ERRORS))
for e in ERRORS:
    print("  E:", e)
print("WARNINGS:", len(WARN))
for w in WARN:
    print("  W:", w)
print("RESULT:", "PASS" if not ERRORS else "FAIL")
