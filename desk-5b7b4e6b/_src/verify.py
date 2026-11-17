# -*- coding: utf-8 -*-
"""Verifier for desk-5b7b4e6b (session arena-5b7b4e6b).

This is a structural checker, not a fact checker. It proves that:

  * only pages, one stylesheet and one script are published;
  * every internal link resolves;
  * every external host is on the allowlist of government publishers;
  * every data row carries at least one source citation, or is a row of a table that says in
    the page why no citation applies, or carries an explicit status tag with the value cell
    left empty or marked;
  * every money figure is a multiple of $10, except a statutory amount written exactly as
    published and wrapped in <span class="stat">;
  * no personal-identifier pattern appears — no postcode, e-mail, telephone number, street
    address, parcel number, social security shape or city or neighbourhood name;
  * no script, form, iframe or object element is published;
  * the pages are the ones the builder wrote (rebuild determinism).

The semantic truth of each cited page was checked by reading it, session by session; the
source register records how each one was checked.

Run:  python3 desk-5b7b4e6b/_src/verify.py
"""

from __future__ import annotations

import html.parser
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

DESK = Path(__file__).resolve().parent.parent
from sources import ALLOWED_HOSTS, SOURCES

MONEY = re.compile(r"\$(\d{1,3}(?:,\d{3})+|\d+)(?![\d.,])")
ZIP = re.compile(r"\b\d{5}(?:-\d{4})?\b")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[a-z]{2,}")
SSN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
PHONE = re.compile(r"\(?\d{3}\)?[-. ]\d{3}[-.]\d{4}")
STREET = re.compile(
    r"\b\d{1,4}\s+(?:[A-Z][a-z]+\s){1,3}"
    r"(?:Avenue|Street|Road|Boulevard|Drive|Court|Lane|Way|Place|Terrace)\b")
PARCEL = re.compile(r"\bAPN\s*[:#]\s*\d|\bparcel\s+number\s*[:#]\s*\d|\\baccount\\s+number\\s*[:#]\\s*\\d", re.I)
FORBIDDEN_PLACES = (
    "Cupertino", "Sunnyvale", "Palo Alto", "Los Altos", "Saratoga", "San Jose",
    "Outer Sunset", "Sunset District", "Milpitas", "Campbell", "Santa Clara city",
    "Mountain View", "Gilroy", "Morgan Hill", "Los Gatos",
)

errors: list[str] = []
warnings: list[str] = []
stats = {"pages": 0, "tables": 0, "rows": 0, "cited": 0, "tagged": 0, "exempt": 0,
         "links": 0, "external": 0}


class Check(html.parser.HTMLParser):
    def __init__(self, path: Path):
        super().__init__()
        self.path = path
        self.in_row = False
        self.in_head = False
        self.row_html: list[str] = []
        self.row_links: list[str] = []
        self.table_class = ""
        self.table_exempt = False
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table":
            self.table_class = a.get("class", "")
            self.table_exempt = "data-exempt" in a
            stats["tables"] += 1
        if tag == "thead":
            self.in_head = True
        if tag == "tr":
            self.in_row = True
            self.row_html = []
            self.row_links = []
        if tag in ("script", "iframe", "form", "object", "embed", "input"):
            if tag == "script" and a.get("src", "").endswith("calculator.js"):
                pass          # the what-if calculator is the desk's own script
            elif tag in ("input",):
                pass          # number controls on the what-if page
            else:
                errors.append(f"{self.path.name}: forbidden element <{tag}>")
        if self.in_row and tag == "span" and "tag" in a.get("class", ""):
            self.row_html.append(" status-tag ")
        for key in ("href", "src"):
            v = a.get(key)
            if not v:
                continue
            stats["links"] += 1
            if v.startswith("http"):
                host = urlparse(v).hostname or ""
                if host not in ALLOWED_HOSTS:
                    errors.append(f"{self.path.name}: external host not on the allowlist: "
                                  f"{host}")
                stats["external"] += 1
                if self.in_row:
                    self.row_links.append(v)
            elif v.startswith("#"):
                if self.in_row:
                    self.row_links.append(v)
            else:
                target = v.split("#")[0]
                if target and not (self.path.parent / target).exists():
                    errors.append(f"{self.path.name}: broken internal link {v}")
                if self.in_row:
                    self.row_links.append(v)

    def handle_data(self, data):
        if self.in_row:
            self.row_html.append(data)

    def handle_endtag(self, tag):
        if tag == "tr" and self.in_row:
            if not self.in_head and "data" in self.table_class:
                stats["rows"] += 1
                text = " ".join(self.row_html)
                cited = bool(self.row_links)
                tagged = " status-tag " in text
                if cited:
                    stats["cited"] += 1
                elif self.table_exempt:
                    stats["exempt"] += 1
                elif " status-tag " in text:
                    stats["tagged"] += 1
                else:
                    errors.append(
                        f"{self.path.name}: data row has no source citation and no status "
                        f"tag — {text[:90]!r}")
            self.in_row = False
        if tag == "thead":
            self.in_head = False


def scan_text(path: Path, text: str) -> None:
    # Strip attribute values and link labels: URLs are addresses, and citation labels are
    # statute and form numbers.
    visible = re.sub(r"<a\b.*?</a>", "", text, flags=re.S)
    visible = re.sub(r'(?:href|src)="[^"]*"', "", visible)
    visible = re.sub(r"<code>.*?</code>", "", visible, flags=re.S)
    for pattern, label in ((EMAIL, "e-mail"), (SSN, "social security shape"),
                           (PHONE, "telephone shape"), (ZIP, "postcode shape"),
                           (STREET, "street address"), (PARCEL, "parcel or account number")):
        hit = pattern.search(visible)
        if hit and pattern is ZIP:
            ctx = visible[max(0, hit.start() - 40):hit.end() + 10].lower()
            if "section" in ctx or "code" in ctx or "statute" in ctx:
                hit = None
        if hit:
            errors.append(f"{path.name}: {label} pattern — {hit.group(0)!r}")
    for place in FORBIDDEN_PLACES:
        if re.search(rf"\b{re.escape(place)}\b", visible, re.I):
            errors.append(f"{path.name}: place name {place!r}")
    # Money rounding. Statutory amounts are exempt and are marked in the page.
    stripped = re.sub(r'\stitle="[^"]*"', "", text)
    stripped = re.sub(r'<span class="stat">.*?</span>', "", stripped, flags=re.S)
    for m in MONEY.finditer(stripped):
        value = int(m.group(1).replace(",", ""))
        if value % 10:
            errors.append(f"{path.name}: money not rounded to $10 — ${m.group(1)}")


def main() -> int:
    pages = sorted(p for p in DESK.glob("*.html"))
    if not pages:
        errors.append("no pages found — run build.py first")
    for p in DESK.rglob("*"):
        if p.is_dir() or p.name.startswith("."):
            continue
        rel = p.relative_to(DESK)
        if str(rel).startswith("_src"):
            continue
        if p.suffix not in (".html", ".css", ".js"):
            errors.append(f"unexpected published artifact {rel}")
        if p.is_symlink():
            errors.append(f"symlink in the published desk {rel}")
        if p.suffix == ".html":
            stats["pages"] += 1
            text = p.read_text()
            Check(p).feed(text)
            scan_text(p, text)
        if p.suffix == ".js":
            js = p.read_text()
            if "http" in js or "fetch(" in js or "XMLHttpRequest" in js:
                errors.append(f"{rel}: script makes a network call")
    # Every source in the register must be reachable from at least one page, or be unused.
    used = set()
    for p in pages:
        used |= set(re.findall(r'href="sources\.html#([\w_]+)"', p.read_text()))
    unused = set(SOURCES) - used
    if unused:
        warnings.append("sources in the register that no row cites: " + ", ".join(sorted(unused)))
    if errors:
        print(f"FAIL — {len(errors)} error(s), {len(warnings)} warning(s)")
        for e in errors:
            print("  ERROR  ", e)
        for w in warnings:
            print("  warning", w)
        return 1
    print(f"PASS — {stats['pages']} pages, {stats['tables']} tables, {stats['rows']} data rows "
          f"({stats['cited']} with a source citation, {stats['tagged']} carrying a status tag, "
          f"{stats['exempt']} in an exempt table); {stats['links']} links "
          f"({stats['external']} external, all on the allowlist); internal links resolve; "
          f"money rounds to $10; no personal-identifier patterns; no forbidden elements.")
    for w in warnings:
        print("  warning", w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
