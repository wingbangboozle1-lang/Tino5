#!/usr/bin/env python3
"""Validate internal links and official source links in every public table row."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = [ROOT / "index.html", *sorted((ROOT / "pages").glob("*.html"))]
OFFICIAL_EXACT = {"sfelections.org"}
OFFICIAL_SUFFIXES = ("sfelections.org",)
errors: list[str] = []


def official(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return host.endswith(".gov") or host in OFFICIAL_EXACT or host.endswith(OFFICIAL_SUFFIXES) or host.endswith(".gov.uk")


class PageParser(HTMLParser):
    def __init__(self, path: Path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.row_depth = 0
        self.row_has_td = False
        self.row_has_official_source = False
        self.current_row = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "tr":
            self.row_depth += 1
            self.current_row += 1
            self.row_has_td = False
            self.row_has_official_source = False
        elif tag == "td" and self.row_depth:
            self.row_has_td = True
        elif tag == "a" and attrs.get("href"):
            href = attrs["href"]
            parsed = urlparse(href)
            if parsed.scheme in {"http", "https", "mailto"}:
                if self.row_depth and self.row_has_td and parsed.scheme in {"http", "https"} and official(href):
                    self.row_has_official_source = True
            elif not parsed.scheme and not href.startswith("#"):
                target = unquote(parsed.path)
                if target:
                    target_path = (self.path.parent / target).resolve()
                    if not target_path.exists():
                        errors.append(f"{self.path.relative_to(ROOT)}: broken internal link {href}")

    def handle_endtag(self, tag):
        if tag == "tr" and self.row_depth:
            if self.row_has_td and not self.row_has_official_source:
                errors.append(f"{self.path.relative_to(ROOT)}: table row {self.current_row} has no official source link")
            self.row_depth -= 1


for html in HTML_FILES:
    parser = PageParser(html)
    parser.feed(html.read_text(encoding="utf-8"))

if errors:
    print("Site validation failed:")
    print("\n".join(f"- {e}" for e in errors))
    raise SystemExit(1)
print(f"Validated {len(HTML_FILES)} pages: all local links resolve and every data row has an official source link.")
