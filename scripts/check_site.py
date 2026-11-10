#!/usr/bin/env python3
"""Lightweight static-site checks for internal links and source-linked table rows."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted([ROOT / "index.html", *sorted((ROOT / "pages").glob("*.html"))])

class CheckParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.tables = []
        self.row = None
        self.in_tbody = False
        self.in_table = False
        self._stack = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "table":
            self.in_table = True
        elif tag == "tbody":
            self.in_tbody = True
        elif tag == "tr" and self.in_tbody:
            self.row = []
        elif tag == "a" and self.row is not None and attrs.get("href", "").startswith("https://"):
            self.row.append(attrs["href"])
        self._stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "tr" and self.row is not None:
            self.tables.append(self.row)
            self.row = None
        elif tag == "tbody":
            self.in_tbody = False
        elif tag == "table":
            self.in_table = False
        if tag in self._stack:
            i = len(self._stack) - 1 - self._stack[::-1].index(tag)
            self._stack = self._stack[:i]


def main():
    failures = []
    all_source_rows = 0
    for page in PAGES:
        text = page.read_text(encoding="utf-8")
        parser = CheckParser()
        parser.feed(text)
        base = page.parent
        for href in parser.links:
            if href.startswith(("https://", "http://", "mailto:", "tel:", "#")):
                continue
            target = href.split("#", 1)[0]
            if not target:
                continue
            resolved = (base / target).resolve()
            if not resolved.exists():
                failures.append(f"{page.relative_to(ROOT)}: broken local link: {href}")
        for row_num, sources in enumerate(parser.tables, 1):
            all_source_rows += 1
            if not sources:
                failures.append(f"{page.relative_to(ROOT)}: table body row {row_num} has no HTTPS source link")

    for required in [ROOT / "assets/site.css", ROOT / "assets/site.js", ROOT / "pages/decision.html", ROOT / "pages/projections.html", ROOT / "pages/inheritance.html", ROOT / "pages/flagged.html", ROOT / "pages/sources.html"]:
        if not required.exists():
            failures.append(f"missing required file: {required.relative_to(ROOT)}")

    if failures:
        print("SITE CHECK FAILED")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1
    print(f"SITE CHECK PASSED: {len(PAGES)} HTML pages; {all_source_rows} table body rows have official HTTPS source links; internal links resolve; required pages present.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
