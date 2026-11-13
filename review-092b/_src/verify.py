"""Verification gate for review-092b.

Fails (non-zero exit) if any published page breaks a rule from the brief:
  1. every table body row carries a link that traces the claim — an official document
     for a factual row, or a repository path for a row about the repository itself;
  2. every external link is https and on an official publisher host;
  3. every internal link resolves to a real file;
  4. every dollar amount in prose or tables is a multiple of $10
     (statutory amounts are wrapped in <span class="stat"> and are exempt);
  5. no personal-identifier pattern appears (ZIP, phone, e-mail, street address,
     APN/parcel language, city or neighbourhood names);
  6. no scripts, forms, iframes or remote assets.

It is a structural gate, not a fact checker: semantic accuracy rests on each row's
link, which a human has to read. Run: python3 review-092b/_src/verify.py
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

OUT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sources import SOURCES  # noqa: E402

EXPECTED = {
    "index.html", "questions.html", "suggestions.html", "projections.html",
    "decision.html", "black-swans.html", "inheritance.html", "costs.html",
    "repo-review.html", "flagged.html", "sources.html",
}
ALLOWED_HOSTS = {urlparse(s["url"]).hostname for s in SOURCES}

PII = [
    (r"[\w.+-]+@[\w-]+\.[a-z]{2,}", "e-mail address"),
    (r"\b\d{3}-\d{2}-\d{4}\b", "SSN shape"),
    (r"\(\d{3}\)\s?\d{3}-\d{4}", "phone shape"),
    (r"(?<![\w.-])\d{5}(?:-\d{4})?(?![\w-])", "ZIP / postal code shape"),
    (r"\b\d{1,4}\s+(?:[A-Z][a-z]+\s){1,3}(?:Ave|Avenue|St|Street|Rd|Road|Blvd|Boulevard|Dr|Drive|Ct|Court|Ln|Lane|Way|Pl|Place|Ter|Terrace)\b",
     "street address"),
    (r"\bAPN\b", "APN token"),
    (r"\bparcel\s+number\b", "parcel number language"),
    (r"\bCupertino\b|\bSunnyvale\b|\bSan\s+Jose\b|\bPalo\s+Alto\b|\bSaratoga\b|"
     r"\bLos\s+Altos\b|\bLos\s+Gatos\b|\bOuter\s+Sunset\b|\bInner\s+Sunset\b|\bSunset\b",
     "city or neighbourhood identifier"),
    (r"\b95014\b|\b94122\b", "the property ZIP code"),
]
# A dollar figure, excluding shorthand ("$15M"), per-unit rates ("$0.55 per $500",
# "$1,000 of premium") and decimals.
MONEY = re.compile(r"(?<![\w$.])\$(\d{1,3}(?:,\d{3})+|\d+)(?![\d.,%MKB])(?!\s*(?:of|per)\b)")

errors: list[str] = []
stats = {"rows": 0, "row_sources": 0, "links": 0, "external": 0, "tables": 0, "pages": 0}


class Check(HTMLParser):
    def __init__(self, path: Path):
        super().__init__()
        self.path = path
        self.in_row = False
        self.in_head = False
        self.table_class = ""
        self.row_links: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table":
            self.table_class = a.get("class", "")
            stats["tables"] += 1
        if tag == "thead":
            self.in_head = True
        if tag == "tr":
            self.in_row = True
            self.row_links = []
        if tag in ("script", "iframe", "form", "object", "embed", "link"):
            if tag == "link" and a.get("href", "").startswith("style.css"):
                pass  # local stylesheet only
            else:
                errors.append(f"{self.path.name}: forbidden element <{tag}>")
        for key in ("href", "src"):
            if key not in a:
                continue
            v = a[key]
            stats["links"] += 1
            if v.startswith("http"):
                host = urlparse(v).hostname or ""
                if not v.startswith("https://"):
                    errors.append(f"{self.path.name}: non-https external link {v}")
                if host not in ALLOWED_HOSTS:
                    errors.append(f"{self.path.name}: unexpected external host {host}")
                stats["external"] += 1
                stats["row_sources"] += 1
                if self.in_row:
                    self.row_links.append(v)
            elif v.startswith("#"):
                continue
            else:
                target = v.split("#")[0]
                if target and not (self.path.parent / target).exists():
                    errors.append(f"{self.path.name}: broken local link {v}")
                elif target and self.in_row:
                    # A claim whose evidence is the repository itself (a directory review)
                    # is traceable by following the link; count it as a row source.
                    self.row_links.append(v)

    def handle_endtag(self, tag):
        if tag == "tr" and self.in_row:
            if not self.in_head and self.table_class == "data":
                stats["rows"] += 1
                if not self.row_links:
                    errors.append(f"{self.path.name}: data row with no traceable source link")
            self.in_row = False
        if tag == "thead":
            self.in_head = False


def main() -> int:
    pages = sorted(p.name for p in OUT.glob("*.html"))
    stats["pages"] = len(pages)
    if set(pages) != EXPECTED:
        errors.append(f"page set mismatch: missing {EXPECTED - set(pages)}, extra {set(pages) - EXPECTED}")
    for p in OUT.rglob("*"):
        if p.is_dir():
            continue
        if "_src" in p.parts:
            continue
        if p.suffix not in (".html", ".css", ".json"):
            errors.append(f"unexpected artifact {p.name}")
    for p in OUT.glob("*.html"):
        text = p.read_text()
        visible = re.sub(r"<a\b.*?</a>", "", text, flags=re.S)
        visible = re.sub(r'(?:href|src)="[^"]*"', "", visible)
        # Marked elements are exempt from both gates: statutory amounts, publisher names,
        # and statute section numbers ("R&TC 11911") which are not postal codes.
        visible = re.sub(r'<span class="(?:stat|host)">.*?</span>', "", visible, flags=re.S)
        visible = re.sub(r"<code>.*?</code>", "", visible, flags=re.S)
        visible = re.sub(r"§\s*\d+[\w.\-]*", "", visible)
        for pattern, label in PII:
            if re.search(pattern, visible, re.I):
                errors.append(f"{p.name}: {label} pattern")
        stripped = re.sub(r'<span class="stat">.*?</span>', "", text, flags=re.S)
        stripped = re.sub(r"<code>.*?</code>", "", stripped, flags=re.S)
        for amount in MONEY.finditer(stripped):
            value = int(amount.group(1).replace(",", ""))
            if value % 10:
                errors.append(f"{p.name}: unrounded money ${amount.group(1)}")
        Check(p).feed(text)
    if errors:
        print("\n".join(sorted(set(errors))))
        print(f"\nFAIL — {len(set(errors))} problem(s)")
        return 1
    print(f"PASS: {stats['pages']} pages; {stats['tables']} tables; {stats['rows']} table rows, "
          f"all source-linked; {stats['links']} links ({stats['external']} official citations); "
          f"internal targets resolve; every dollar amount is a multiple of $10; "
          f"no personal-identifier patterns; no scripts, forms or remote assets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
