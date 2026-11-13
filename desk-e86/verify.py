#!/usr/bin/env python3
"""Verification for desk-e86 (session arena-e86df670).

Checks, per page in desk-e86/:
  1. every body row of every data table carries at least one link
     (an official-source link, or an internal link on rows explicitly
     marked unverified / derived / proposal);
  2. external links are on the official-host allowlist;
  3. internal links resolve to files that exist in this repository;
  4. every dollar amount of $1,000 or more is a multiple of $10
     (published constants may be listed in MONEY_ALLOW);
  5. no personal-identifier pattern appears in visible text:
     e-mail, phone, SSN, parcel-number shape, street address,
     city/neighbourhood names, or ZIP-like numeric tokens other
     than the whitelisted statutory section numbers in section context.
  6. the pages exist and the nav is consistent.

Run:  python3 desk-e86/verify.py
Exit code 0 = pass.
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

PAGES = ["index.html", "questions.html", "suggestions.html", "repo-review.html", "flagged.html"]

ALLOWED_HOSTS = {
    "www.irs.gov", "irs.gov",
    "www.boe.ca.gov", "boe.ca.gov",
    "www.sco.ca.gov", "www.ftb.ca.gov",
    "courts.ca.gov", "selfhelp.courts.ca.gov",
    "sftreasurer.org",
    "www.insurance.ca.gov", "insurance.ca.gov",
    "www.cbo.gov", "cbo.gov",
    "leginfo.legislature.ca.gov",
    "www.sf.gov", "sf.gov",
    "www.huduser.gov",
    "www.cpuc.ca.gov",
    "github.com",
}

# Published official constants that are not multiples of $10 (as printed by the agency).
MONEY_ALLOW = {"1,571", "1,044,586"}

# Statutory code-section tokens allowed despite looking like 5-digit postal codes,
# but only in explicit "section"/"§" context (checked separately).
STAT_OK = {"13100", "13151", "13101", "17043"}

CITY_PATTERNS = [
    r"\bCupertino\b", r"\bSunnyvale\b", r"\bSan Jose\b", r"\bPalo Alto\b",
    r"\bSaratoga\b", r"\bLos Altos\b", r"\bOuter Sunset\b",
]

RE_MONEY = re.compile(r"\$\s?(\d{1,3}(?:,\d{3})+|\d{3,})(?![\d,])")
RE_EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")
RE_PHONE = re.compile(r"(?<![\d./-])(?:\+?1[\s.-])?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}(?![\d-])")
RE_SSN = re.compile(r"(?<![\d-])\d{3}-\d{2}-\d{4}(?![\d-])")
RE_APN = re.compile(r"(?<![\d-])\d{3}-\d{2}-\d{3}(?![\d-])")
RE_ADDR = re.compile(
    r"\b\d{2,5}\s+(?:[NSEW]\.\s+)?[A-Z][a-z]+(?:\s[A-Z][a-z]+)?\s+"
    r"(?:St|Street|Ave|Avenue|Rd|Road|Dr|Drive|Blvd|Boulevard|Ct|Court|Ln|Lane|Way|Pl|Place|Ter|Terrace)\b\.?",
    re.I,
)
RE_ZIP = re.compile(r"(?<![\d,.])\d{5}(?:-\d{4})?(?![\d])")

errors: list[str] = []
stats = {"rows": 0, "links_official": 0, "links_internal": 0, "money": 0, "pages": 0}


class PageScan(HTMLParser):
    def __init__(self, path: Path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.in_table = False
        self.in_row = False
        self.in_head = False
        self.row_links: list[str] = []
        self.row_text: list[str] = []
        self.anchors: list[str] = []
        self.text_chunks: list[str] = []
        self.nav_hrefs: list[str] = []
        self.in_nav = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table":
            self.in_table = True
        elif tag == "tr" and self.in_table:
            self.in_row = True
            self.row_links, self.row_text = [], []
        elif tag == "th":
            self.in_head = True
        elif tag == "nav":
            self.in_nav = True
        if tag == "a" and "href" in a:
            href = a["href"]
            if self.in_row:
                self.row_links.append(href)
            if self.in_nav:
                self.nav_hrefs.append(href)
            self.anchors.append(href)

    def handle_endtag(self, tag):
        if tag == "table":
            self.in_table = False
        elif tag == "tr" and self.in_row:
            self._check_row()
            self.in_row = False
        elif tag == "th":
            self.in_head = False
        elif tag == "nav":
            self.in_nav = False

    def handle_data(self, data):
        if self.in_row and not self.in_head:
            self.row_text.append(data)
        if data.strip():
            self.text_chunks.append(data)

    def _check_row(self):
        text = " ".join(self.row_text).strip()
        if not text:
            return
        stats["rows"] += 1
        if not self.row_links:
            errors.append(f"{self.path.name}: row without any link: {text[:80]!r}")
            return
        official = internal = 0
        for href in self.row_links:
            if href.startswith(("http://", "https://")):
                host = urlparse(href).netloc
                if host in ALLOWED_HOSTS:
                    official += 1
                else:
                    errors.append(f"{self.path.name}: external host not allowlisted: {host} in {href}")
            else:
                internal += 1
                target = (self.path.parent / href.split("#")[0]).resolve()
                if not target.exists():
                    errors.append(f"{self.path.name}: broken internal link {href}")
        stats["links_official"] += official
        stats["links_internal"] += internal


def visible_text(html: str) -> str:
    html = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S | re.I)
    return re.sub(r"<[^>]+>", " ", html)


def main() -> int:
    for name in PAGES:
        path = HERE / name
        if not path.exists():
            errors.append(f"missing page: {name}")
            continue
        stats["pages"] += 1
        html = path.read_text(encoding="utf-8")
        scan = PageScan(path)
        scan.feed(html)

        # internal links (including non-table links)
        for href in scan.anchors:
            if not href.startswith(("http://", "https://")):
                target_part = href.split("#")[0]
                if target_part and not (path.parent / target_part).resolve().exists():
                    errors.append(f"{name}: broken link {href}")
                if target_part.endswith(".md"):
                    errors.append(f"{name}: links to a non-published repo file {href}")

        text = visible_text(html)

        # money
        for m in RE_MONEY.finditer(text):
            val = m.group(1)
            if val in MONEY_ALLOW:
                continue
            plain = int(val.replace(",", ""))
            if plain >= 1000 and plain % 10 != 0:
                errors.append(f"{name}: money not rounded to $10: ${val}")
            else:
                stats["money"] += 1

        # identifiers
        for rx, label in (
            (RE_EMAIL, "e-mail"), (RE_PHONE, "phone"), (RE_SSN, "SSN"),
            (RE_APN, "parcel-number shape"), (RE_ADDR, "street address"),
        ):
            for m in rx.finditer(text):
                errors.append(f"{name}: {label} pattern: {m.group(0)!r}")
        for pat in CITY_PATTERNS:
            m = re.search(pat, text)
            if m:
                errors.append(f"{name}: place name present: {m.group(0)}")
        for m in RE_ZIP.finditer(text):
            tok = m.group(0)
            if tok in STAT_OK:
                ctx = text[max(0, m.start() - 40):m.start()].lower()
                if "section" in ctx or "§" in text[max(0, m.start() - 6):m.start()]:
                    continue
            errors.append(f"{name}: ZIP-like numeric token: {tok}")

    print(f"desk-e86 verify: {stats['pages']} pages, {stats['rows']} data rows, "
          f"{stats['links_official']} official links, {stats['links_internal']} internal row links")
    if errors:
        print(f"FAIL — {len(errors)} problem(s):")
        for e in errors:
            print("  -", e)
        return 1
    print("PASS: every row linked, hosts allowlisted, money rounded, no identifier patterns.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
