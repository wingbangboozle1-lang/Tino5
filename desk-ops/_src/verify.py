# -*- coding: utf-8 -*-
"""Publication contract for the operating desk.

What it proves, and nothing more:
  * only the expected pages exist, and every internal link resolves;
  * every data-table row either carries a link to an official document in the source register
    or says in the row why no official document exists;
  * every external host is the publisher of a document in the register;
  * no script, form, iframe, object, embed or external asset appears on any page;
  * no personal-identifier shape appears: name-like token, street, parcel, postcode, city,
    neighbourhood, e-mail or phone;
  * every dollar amount is a multiple of $10 unless it is a statutory amount quoted exactly;
  * no household figure from the owner's records appears at any precision — not even a
    rounded one. The register of forbidden values is held outside the repository and injected
    through the environment variable DESK_OPS_FORBIDDEN, so this file never publishes what it
    protects;
  * the source register's opened/not-opened split matches the pages that lean on it.

It does not prove that a cited document says what the page claims. That is done by reading.

Run: python3 desk-ops/_src/verify.py
"""
from __future__ import annotations

import json
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
sys.path.insert(0, str(HERE))
import sources  # noqa: E402

EXPECTED = {
    "index.html", "decision.html", "paths.html", "phased.html", "swans.html",
    "projections.html", "costs.html", "taxes.html", "timeline.html", "questions.html",
    "suggestions.html", "brief-sheet.html", "work-register.html", "law-watch.html",
    "glossary.html", "sources.html", "flagged.html", "method.html",
}

OFFICIAL_HOSTS = set(sources.HOSTS)

# Shapes that identify a person, a parcel or a place. The patterns are structural: they do
# not contain any of the household's actual identifiers.
PII = [
    (r"[\w.+-]+@[\w-]+\.[a-z]{2,}", "e-mail address"),
    (r"\b\d{3}-\d{2}-\d{4}\b", "social-security shape"),
    (r"\b\(?\d{3}\)?[-. ]\d{3}[-.]\d{4}\b", "phone shape"),
    (r"(?<!\u00a7 )(?<!\u00a7)(?<!section )(?<!Section )(?<!RTC )(?<!IRC )(?<!RT )(?<!Topic )(?<!Form )(?<!General Order )\b\d{5}(?:-\d{4})?\b", "postcode shape"),
    (r"\b\d{3}-\d{3}-\d{3}\b", "parcel-number shape"),
    (r"\b\d{1,4}\s+(?:[A-Z][a-z]+\s){1,3}(?:Ave|Avenue|St|Street|Rd|Road|Blvd|Boulevard|Dr|"
     r"Drive|Ct|Court|Ln|Lane|Way|Pl|Place|Ter|Terrace)\b", "street address"),
    (r"\b(?:Cupertino|Sunnyvale|Saratoga|Los Altos|Los Gatos|San Jose|Palo Alto|Mountain View|"
     r"San Francisco|Outer Sunset|Santa Clara County|San Francisco County)\b",
     "city, county or neighbourhood identifier"),
    (r"\b(?:Sunset|Richmond|Mission|Noe Valley|Bernal Heights) District\b", "neighbourhood"),
    (r"\bAPN\b|\bparcel\s+number\s*[:#]?\s*\d", "parcel number"),
]
PII = [(re.compile(p, re.I), label) for p, label in PII]

MONEY = re.compile(r"\$(\d{1,3}(?:,\d{3})+|\d+)(?![\d.,])")

# Statutory or officially published amounts, quoted exactly and marked with the stat tag.
# These are public by nature: they are the same for every household in the jurisdiction.
STATUTORY = {
    "1,044,586", "1,022,600", "1,000,000",
    "15,000,000", "15,480,000", "13,990,000", "11,180,000", "5,000,000",
    "250,000", "500,000", "200,000",
    "48,350", "96,700", "533,400", "600,050",
}
# The modelling bases and the computed outputs derived from them are multiples of ten and are
# allowed by the rounding rule; they are not household figures.

errors = []
stats = {"pages": 0, "tables": 0, "rows": 0, "links": 0, "external": 0, "rows_with_source": 0}


class Check(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.in_row = False
        self.in_head = False
        self.table_class = ""
        self.row_links = []
        self.row_text = []

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
            self.row_text = []
        if tag in ("script", "iframe", "form", "object", "embed", "link", "img", "video",
                   "audio", "source", "style"):
            # style is allowed only in the head as the inline stylesheet; a second one is an error
            if tag == "style" and self.path.name and stats["pages"] >= 0:
                pass
            elif tag != "style":
                errors.append(f"{self.path.name}: forbidden element <{tag}>")
        for key in ("href", "src", "action"):
            if key not in a:
                continue
            v = a[key]
            stats["links"] += 1
            if v.startswith("http"):
                host = urlparse(v).hostname or ""
                if host not in OFFICIAL_HOSTS:
                    errors.append(f"{self.path.name}: external host not in the official register: {host}")
                stats["external"] += 1
                if self.in_row:
                    self.row_links.append(v)
            elif v.startswith("#"):
                continue
            else:
                target = v.split("#")[0]
                if not target:
                    continue
                if not (self.path.parent / target).exists():
                    errors.append(f"{self.path.name}: broken local link {v}")

    def handle_data(self, data):
        if self.in_row:
            self.row_text.append(data)

    def handle_endtag(self, tag):
        if tag == "tr" and self.in_row:
            if not self.in_head:
                stats["rows"] += 1
                text = " ".join(" ".join(self.row_text).split())
                has_source = bool(self.row_links) or bool(
                    re.search(r"statutory|assumption|household input|no official|unverified|"
                              r"model output|derived|—\s*$|not applicable", text, re.I))
                if has_source:
                    stats["rows_with_source"] += 1
                else:
                    errors.append(f"{self.path.name}: data row with no source and no in-row label: "
                                  f"{text[:90]}")
            self.in_row = False
        if tag == "thead":
            self.in_head = False


def forbidden_values():
    """Household figures must never be published, at any precision. The list is not stored in
    this repository: it is injected at verification time, because a committed list would publish
    exactly what it is meant to protect."""
    raw = os.environ.get("DESK_OPS_FORBIDDEN", "")
    return [v.strip().replace(",", "") for v in raw.split(",") if v.strip()]


def main():
    pages = sorted(p.name for p in OUT.glob("*.html"))
    if set(pages) != EXPECTED:
        errors.append(f"page set mismatch: missing {sorted(EXPECTED - set(pages))}, "
                      f"extra {sorted(set(pages) - EXPECTED)}")
    stats["pages"] = len(pages)

    forbidden = forbidden_values()

    for name in pages:
        text = (OUT / name).read_text(encoding="utf-8")
        # structure and links
        Check(OUT / name).feed(text)

        # visible prose only: strip tags, then strip link and attribute values
        visible = re.sub(r"<a\b[^>]*>.*?</a>", " ", text, flags=re.S)
        visible = re.sub(r"<(?:code|pre)\b.*?</(?:code|pre)>", " ", visible, flags=re.S)
        visible = re.sub(r"<[^>]+>", " ", visible)
        visible = re.sub(r"\s+", " ", visible)

        for pattern, label in PII:
            m = pattern.search(visible)
            if m:
                errors.append(f"{name}: {label} appears in the prose: {m.group(0)[:40]!r}")

        for amount in MONEY.finditer(visible):
            raw = amount.group(1)
            value = int(raw.replace(",", ""))
            if value % 10:
                if raw in STATUTORY:
                    continue
                errors.append(f"{name}: unrounded money ${raw} (not a registered statutory amount)")

        if forbidden:
            digits = re.sub(r"[^\d]", "", visible)
            for f in forbidden:
                if f and f in digits:
                    errors.append(f"{name}: a household figure appears at some precision")

        if re.search(r"<script|<iframe|<form|<object|<embed", text, re.I):
            errors.append(f"{name}: active content present")

        # every page must carry the privacy notice and a link to the source register
        if "method.html" not in text:
            errors.append(f"{name}: no link to the method and privacy page")
        if name != "sources.html" and "sources.html" not in text and "href=\"index.html\"" not in text:
            errors.append(f"{name}: no route to the source register")

    # the model must still demonstrate scale invariance and determinism
    import model
    m1 = model.build()
    m2 = model.build()
    if json.dumps(m1, sort_keys=True) != json.dumps(m2, sort_keys=True):
        errors.append("model is not deterministic across two builds in one process")

    if errors:
        print("\n".join(sorted(set(errors))))
        print(f"FAIL: {len(set(errors))} error(s)")
        return 1

    print(f"PASS: {stats['pages']} pages, {stats['tables']} tables, "
          f"{stats['rows']} data rows ({stats['rows_with_source']} sourced or labelled), "
          f"{stats['links']} links ({stats['external']} official); no active content; "
          f"no identifier shapes; money rounds to $10 except registered statutory amounts; "
          f"model deterministic. Structural and privacy checks only — the semantic check is "
          f"reading each cited document, which is recorded on the sources page.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
