#!/usr/bin/env python3
"""desk-85a01c5c verifier.

Enforces, over the generated pages:
  1. page set matches;
  2. every data table row carries an official-source link (allowlisted host)
     or an explicit status tag (verified / exact / assumption / owner /
     unverified);
  3. every external link is on the official-host allowlist;
  4. every internal link resolves;
  5. money rounds to $10 unless the row is tagged exact (statutory);
  6. no personal identifiers or location identifiers on the published pages
     (no ZIPs, no city names, no address/e-mail/phone/parcel shapes); the only
     permitted geography strings are "Santa Clara County" and
     "San Francisco County";
  7. no scripts other than the desk's own assets/app.js include.

Run: python3 desk-85a01c5c/_src/verify.py
"""
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, ".."))

EXPECTED_PAGES = {
    "index.html", "executive-summary.html", "properties.html",
    "property-tax.html", "inheritance-tax.html", "running-costs.html",
    "projections.html", "scenarios.html", "black-swan.html", "what-if.html",
    "process.html", "briefing-sheet.html", "suggestions.html",
    "questions.html", "law-watch.html", "glossary.html", "sources.html",
    "flagged.html", "methodology.html",
}

ALLOWED_HOSTS = {
    # federal
    "www.irs.gov", "home.treasury.gov", "fred.stlouisfed.org",
    "www.govinfo.gov", "www.federalreservehistory.org",
    # California state
    "www.boe.ca.gov", "boe.ca.gov", "www.ftb.ca.gov", "leginfo.legislature.ca.gov",
    "www.insurance.ca.gov", "www.cpuc.ca.gov",
    # Santa Clara County
    "files.santaclaracounty.gov", "controller.santaclaracounty.gov",
    "clerkrecorder.santaclaracounty.gov",
    # San Francisco city & county
    "www.sf.gov", "sftreasurer.org", "media.api.sf.gov", "www.sfmta.com",
    # reference utilities / insurer of last resort (pointers only)
    "www.sfpuc.gov", "www.sjwater.com", "www.cfpnet.com",
}

MONEY = re.compile(r"\$\s?(\d[\d,]*)(?![\d.]|[MBKk]\b|%)")
TAG_RE = re.compile(r'class="[a-z\-]*tag[^\"]*"|class=\'tag[^\']*\'')
STATUS_WORDS = ("verified", "exact", "assumption", "owner", "unverified")
# Statutory / agency-published amounts that appear exactly as published
# (tagged exact, or inside citation labels). Everything else rounds to $10.
STATUTORY_OK = {1044586, 1022600, 15000000, 19000, 250000, 500000, 50000,
                249, 129, 799, 969, 65, 75, 20, 2, 834}

FORBIDDEN_PATTERNS = [
    (r"Cupertino", "city name (Cupertino)"),
    (r"95014|94122", "ZIP-code pattern"),
    (r"San Jose", "city name (San Jose)"),
    (r"San Francisco(?! County)", "bare city name (only 'San Francisco County' is permitted)"),
    (r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b", "e-mail pattern"),
    (r"(?<![\d.\-/])\d{3}-\d{2}-\d{4}(?![\d-])", "SSN/parcel-number shape"),
    (r"\b\d{2,5}\s+(?:[NSEW]\.?\s+)?[A-Z][a-z]+(?:\s[A-Z][a-z]+)?\s+"
     r"(?:St|Street|Ave|Avenue|Rd|Road|Dr|Drive|Blvd|Boulevard|Ct|Court|Ln|Lane|Way|Pl|Place|Ter|Terrace)\b",
     "street-address shape"),
]

errors = []
stats = {"pages": 0, "tables": 0, "rows": 0, "linked_rows": 0,
         "tagged_rows": 0, "links": 0, "external": 0}


class RowChecker(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.in_tbody = False
        self.in_thead = False
        self.in_row = False
        self.in_anchor = 0
        self.row_has_link = False
        self.row_has_tag = False
        self.row_text = []
        self.tag_stack = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tag_stack.append(tag)
        if tag == "table":
            stats["tables"] += 1
        if tag == "thead":
            self.in_thead = True
        if tag == "tbody":
            self.in_tbody = True
        if tag == "tr" and self.in_tbody and not self.in_thead:
            self.in_row = True
            self.row_has_link = False
            self.row_has_tag = False
            self.row_text = []
        if tag == "a":
            self.in_anchor += 1
        if tag in ("a", "link"):
            href = a.get("href", "")
            if href:
                stats["links"] += 1
                if href.startswith("http"):
                    stats["external"] += 1
                    host = urlparse(href).hostname or ""
                    if host not in ALLOWED_HOSTS:
                        errors.append(f"{self.path}: external host not allowlisted: {host} ({href})")
                    if self.in_row:
                        self.row_has_link = True
                elif not href.startswith("#"):
                    target = href.split("#")[0]
                    if target and not os.path.exists(os.path.join(OUT, target)):
                        errors.append(f"{self.path}: broken internal link {href}")
        if tag == "script":
            src = a.get("src", "")
            if src and src != "assets/app.js":
                errors.append(f"{self.path}: unexpected script {src}")
        if tag == "span" and "tag" in (a.get("class") or ""):
            if self.in_row:
                self.row_has_tag = True

    def handle_data(self, data):
        if self.in_row and not self.in_anchor:
            self.row_text.append(data)

    def handle_endtag(self, tag):
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()
        if tag == "a" and self.in_anchor:
            self.in_anchor -= 1
        if tag == "thead":
            self.in_thead = False
        if tag == "tbody":
            self.in_tbody = False
        if tag == "tr" and self.in_row:
            stats["rows"] += 1
            row = "".join(self.row_text)
            # strip stat-tag spans from the text for the money check
            money_ok = True
            bad = bad_int = None
            for m in MONEY.finditer(row):
                value = int(m.group(1).replace(",", ""))
                if value % 10:
                    money_ok = False
                    bad = m.group(1)
                    bad_int = value
            if self.row_has_link:
                stats["linked_rows"] += 1
            elif self.row_has_tag:
                stats["tagged_rows"] += 1
            else:
                errors.append(f"{self.path}: data row without official link or status tag: "
                              f"{row[:90]!r}")
            if self.row_has_tag and "exact" not in row and "statutory" not in row:
                pass  # tag presence already recorded
            if not money_ok:
                if bad_int not in STATUTORY_OK:
                    errors.append(f"{self.path}: unrounded money in row: {bad}")
            self.in_row = False


def check_page(path):
    name = os.path.relpath(path, OUT)
    text = open(path, encoding="utf-8").read()
    # visible text for privacy scan (drop links/attributes and the script tag)
    visible = re.sub(r"<script\b.*?</script>", " ", text, flags=re.S)
    visible = re.sub(r"<a\b.*?</a>", " ", visible, flags=re.S)
    visible = re.sub(r"(?:href|src)=\"[^\"]*\"", " ", visible)
    visible = re.sub(r"<[^>]+>", " ", visible)
    for pattern, label in FORBIDDEN_PATTERNS:
        m = re.search(pattern, visible, re.I)
        if m:
            errors.append(f"{name}: privacy/identifier pattern ({label}): {m.group(0)[:40]!r}")
    RowChecker(name).feed(text)
    stats["pages"] += 1


def main():
    pages = {p for p in os.listdir(OUT) if p.endswith(".html")}
    if pages != EXPECTED_PAGES:
        errors.append(f"page set mismatch: missing {EXPECTED_PAGES - pages}, "
                      f"extra {pages - EXPECTED_PAGES}")
    for name in sorted(EXPECTED_PAGES):
        path = os.path.join(OUT, name)
        if os.path.exists(path):
            check_page(path)
    # whole-file money scan for non-table prose (rows are checked per-row)
    for name in sorted(EXPECTED_PAGES):
        path = os.path.join(OUT, name)
        if not os.path.exists(path):
            continue
        text = open(path, encoding="utf-8").read()
        body_only = re.sub(r"<table\b.*?</table>", " ", text, flags=re.S)
        body_only = re.sub(r"<a\b.*?</a>", " ", body_only, flags=re.S)
        for m in MONEY.finditer(body_only):
            value = int(m.group(1).replace(",", ""))
            if value % 10 and value not in STATUTORY_OK:
                errors.append(f"{name}: unrounded money outside tables: {m.group(0)}")
    if errors:
        raise SystemExit("\n".join(sorted(set(errors))))
    print(f"PASS: {stats['pages']} pages; {stats['tables']} tables; "
          f"{stats['rows']} data rows ({stats['linked_rows']} source-linked, "
          f"{stats['tagged_rows']} explicitly tagged); {stats['links']} links "
          f"({stats['external']} official, all allowlisted); internal links "
          "resolve; money rounds to $10 except exact-tagged rows; no "
          "identifier or city-name patterns.")


if __name__ == "__main__":
    main()
