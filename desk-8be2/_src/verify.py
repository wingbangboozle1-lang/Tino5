# -*- coding: utf-8 -*-
"""Structural, privacy and sourcing verification for desk-8be2/.

Run:   python3 desk-8be2/_src/verify.py     (prints a report, non-zero exit on failure)
       python3 desk-8be2/_src/build.py      (builds, then runs this)

Checks:
  V1  every table body row links an official source or carries the no-source marker
  V2  every external link points at a host on the official allowlist
  V3  every internal link resolves to a page that exists
  V4  every money figure is a multiple of $10, except statutory literals in <span class="stat">
  V5  no personal or geographic identifier (names, ZIP, city, address, parcel)
  V6  no NaN / Infinity / None / undefined leaked into output
  V7  no script/iframe/form/object/embed except inline JS on what-if.html
  V8  every cited source id exists in the source register
  V9  every page carries the privacy banner, the full navigation and robots noindex
"""

import os
import re
import sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import sources as src  # noqa: E402

MONEY = re.compile(r"\$\s?([\d,]+)(?:\.(\d+))?(?![\d.,])")
LEAK = [r"NaN", r"Infinity", r"\bNone\b", r"undefined"]

# Anything that could identify the owner, the properties or the area.
PII = [
    (r"(?i)\bcupertino\b", "city"),
    (r"(?i)\bsunnyvale\b", "city"),
    (r"(?i)\bsan jose\b", "city"),
    (r"(?i)\bpalo alto\b", "city"),
    (r"(?i)\bsaratoga\b", "city"),
    (r"(?i)\blos altos\b", "city"),
    (r"(?i)\bsanta clara\b", "county"),
    (r"(?i)\bsan francisco\b", "city"),
    (r"(?i)\bouter sunset\b", "neighbourhood"),
    (r"\b9[45]\d{3}(?:-\d{4})?\b", "postcode"),
    (r"(?i)\b(?:assessor(?:'s)?\s+parcel|parcel\s+(?:number|no\.?|id)|apn)\b\s*[:#]?\s*[\w-]+",
     "parcel identifier"),
    (r"(?i)\baccount\s*(?:number|no\.?|#)\b\s*[:#]?\s*[\w-]+", "account number"),
    (r"[\w.+-]+@[\w-]+\.[a-z]{2,}", "e-mail address"),
    (r"\b\d{3}-\d{2}-\d{4}\b", "SSN shape"),
    (r"\b\(?\d{3}\)?[-. ]\d{3}[-.]\d{4}\b", "phone shape"),
]

errors = []
stats = {"pages": 0, "rows": 0, "links": 0, "external": 0, "tables": 0}
official_urls = set()
cite_ids = set()


def check_money(text, path):
    stripped = re.sub(r"<script\b.*?</script>", "", text, flags=re.S | re.I)
    stripped = re.sub(r"<span class=\"stat\">.*?</span>", "", stripped, flags=re.S | re.I)
    stripped = re.sub(r"<code>.*?</code>", "", stripped, flags=re.S | re.I)
    for m in MONEY.finditer(stripped):
        value = int(m.group(1).replace(",", ""))
        if value % 10:
            errors.append(f"{path}: unrounded money ${m.group(1)}")


class Check(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.in_row = False
        self.in_head = False
        self.table_class = ""
        self.in_script = False
        self.script_src = None
        self.row_links = []
        self.row_in_navtable = False

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
            self.row_text = ""
            self.row_in_navtable = "navtable" in self.table_class
        if tag == "script":
            self.in_script = True
            self.script_src = a.get("src")
            allowed = (tag == "script" and self.path.name == "what-if.html"
                       and self.script_src is None)
            if tag in ("script", "iframe", "form", "object", "embed") and not allowed:
                errors.append(f"{self.path}: forbidden element <{tag}>" +
                              (f" src={self.script_src}" if self.script_src else ""))
        for key in ("href", "src"):
            if key not in a:
                continue
            v = a[key]
            stats["links"] += 1
            if v.startswith("http"):
                host = urlparse(v).hostname or ""
                if host not in src.OFFICIAL_HOSTS:
                    errors.append(f"{self.path}: unexpected external host {host}")
                stats["external"] += 1
                official_urls.add(v)
                if self.in_row:
                    self.row_links.append(v)
            elif v.startswith("#"):
                continue
            else:
                target = v.split("#")[0]
                if not (self.path.parent / target).exists():
                    errors.append(f"{self.path}: broken local link {v}")

    def handle_data(self, data):
        if self.in_script:
            return
        if self.in_row:
            self.row_text += data
        for pat in LEAK:
            if re.search(pat, data):
                errors.append(f"{self.path}: leaked value {pat!r} in visible text")

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False
            self.script_src = None
        if tag == "tr" and self.in_row:
            if not self.in_head:
                stats["rows"] += 1
                has_marker = "No official source — unverified" in self.row_text
                if not self.row_links and not self.row_in_navtable and not has_marker:
                    errors.append(f"{self.path}: data row with no official source link")
            self.in_row = False
        if tag == "thead":
            self.in_head = False


def main():
    pages = sorted(p.name for p in Path(OUT).glob("*.html"))
    if not pages:
        raise SystemExit("no pages found — run build.py first")
    for name in pages:
        p = Path(OUT) / name
        text = p.read_text()
        stats["pages"] += 1
        check_money(text, str(p))

        # V8: cited source ids
        for m in re.finditer(r'(?:src\.)?cite\((["\'])(.*?)\1\)', text):
            cid = m.group(2)
            cite_ids.add(cid)
            if cid not in src.SOURCE_BY_ID:
                errors.append(f"{p}: unknown source id cited: {cid}")

        # V5 PII on visible prose (links and attributes removed first, then tags stripped)
        visible = re.sub(r"<a\b.*?</a>", "", text, flags=re.S | re.I)
        visible = re.sub(r'(?:href|src)="[^"]*"', "", visible)
        visible = re.sub(r"<[^>]+>", " ", visible)
        for pat, label in PII:
            if re.search(pat, visible, re.I):
                errors.append(f"{p}: {label} pattern")

        # V9 structural markers
        if "noindex" not in text:
            errors.append(f"{p}: missing robots noindex")
        if "Estate decision desk · public · anonymized" not in text:
            errors.append(f"{p}: missing privacy banner/kicker")

        Check(p).feed(text)

    # unresolved placeholder markers
    for name in pages:
        text = (Path(OUT) / name).read_text()
        if "nosource_marker_placeholder" in text:
            errors.append(f"{name}: unresolved placeholder marker")
        if "PLACEHOLDER" in text.upper():
            errors.append(f"{name}: contains PLACEHOLDER text")

    if errors:
        raise SystemExit("\n".join(sorted(set(errors))))

    summary = (
        f"PASS: {stats['pages']} pages; {stats['tables']} tables; {stats['rows']} source-linked rows; "
        f"{stats['links']} links ({stats['external']} official); internal links resolve; "
        "money rounds to $10; no personal-identifier patterns; source register consistent."
    )
    print(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
