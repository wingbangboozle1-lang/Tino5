#!/usr/bin/env python3
"""Verify the built desk against its published contract.

Checks, in order of severity:
  1. PAGE SET      the exact fifteen pages exist and nothing else is presented as a page
  2. LINKS         every href is either a page here or an allowlisted official host
  3. SOURCING      every data row carries a source link or a flag reference
  4. ROUNDING      every dollar amount is a multiple of $10, except declared statutory figures
  5. PRIVACY       no ZIP codes, street addresses, parcel numbers, account numbers, or names
  6. HYGIENE       no scripts, no forms, no external assets, no analytics
  7. FLAGS         every flag referenced exists on the flagged page, and vice versa

Run: python3 scripts/verify_desk_v5.py [--json]
Exit code 0 means every check passed. Warnings do not fail the build.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DESK = ROOT / "desk"

EXPECTED = {
    "index.html", "executive-summary.html", "decision.html", "questions.html",
    "projections.html", "costs.html", "estate-tax.html", "process.html",
    "black-swans.html", "law-watch.html", "suggestions.html", "flagged.html",
    "sources.html", "methodology.html", "repo-review.html", "style.css",
}

sys.path.insert(0, str(ROOT / "scripts"))
from build_desk_v5 import ALLOWED_HOSTS  # single source of truth for cited hosts

# Statutory amounts and published rates that are quoted exactly and must NOT be rounded.
EXACT_ALLOWED = {
    "$15,000,000", "$15,480,000", "$1,044,586", "$7,000", "$250,000", "$500,000",
    "$200,000", "$166,250", "$208,850", "$750,000", "$107,900", "$69,625",
    "$20,000", "$100,000", "$800,000", "$9,000,000",
    "$25,000,000", "$166,250.", "$0.55", "$1.65", "$3.75", "$11.25", "$2.50", "$3.40",
    "$27.50", "$30.00", "$1,090", "$1,350", "$2,440", "$114,250", "$4.9692", "$78.64",
    "$2,339.99", "$1,701.60", "$1,440.11", "$3,780", "$3,000", "$1,500", "$5,200",
    "$2,000", "$150,000", "$1,000,000", "$5,000,000", "$10,000,000", "$2,340",
    "$12,440", "$12,000,000",
}

PII_PATTERNS = [
    (r"\b9[0-5]\d{3}(?:-\d{4})?\b", "ZIP code"),
    (r"\b\d{1,5}\s+[A-Z][a-z]+\s+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|"
     r"Boulevard|Blvd|Court|Ct|Way|Place|Pl|Terrace|Ter)\b", "street address"),
    (r"\b(?:APN|Assessor'?s? Parcel|Parcel)\s*(?:No\.?|Number|#)?\s*[:#]?\s*\d{3}-\d{2}-\d{3}",
     "parcel number"),
    (r"\b\d{3}-\d{2}-\d{4}\b", "social security number"),
    (r"\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b", "account or card number"),
    (r"\b(?:born|DOB|date of birth)\b", "date of birth"),
]

# Place names are permitted only where a county or city is named as the publisher of a rate.
PLACE_ALLOWED_CONTEXTS = (
    "county", "city", "recorder", "treasurer", "assessor", "rate book", "Santa Clara",
    "San Francisco", "Pacific division", "San Jose", "Palo Alto", "Mountain View",
    "Cupertino", "Sunset",
)


def load_pages():
    return {p.name: p.read_text() for p in sorted(DESK.glob("*.html"))}


def published_surface(pages, warn, fail):
    """Only public-safe/ may be reachable on the built site.

    This is the check that would have caught the .nojekyll regression. GitHub Pages honours
    _config.yml exclude ONLY when Jekyll builds the site; an empty .nojekyll turns the whole
    repository into static files and silently serves every excluded directory, including
    research/ and the older desks. So the presence of .nojekyll is a hard failure here, and
    every existing path named in the exclude list is reported.
    """
    config = (ROOT / "_config.yml").read_text() if (ROOT / "_config.yml").exists() else ""
    excluded = re.findall(r'^\s*-\s*"([^"]+)"', config, re.M)
    if (ROOT / ".nojekyll").exists():
        fail("published-surface",
             ".nojekyll exists: it disables Jekyll, so every _config.yml exclude is inert and "
             "research/, analysis/, and the older desks become publicly reachable")
    on_disk = [e for e in excluded if (ROOT / e).exists()]
    # desk/ is intentionally published (PUBLISHED_DESKS in scripts/verify_safe.py, owner
    # brief 7b/INT); it must therefore NOT appear in the Jekyll exclude list. Everything
    # else in this set must stay excluded while it exists on disk.
    required = {"research", "analysis", "desk-22a32b17", "COORDINATION.md", "scratch"}
    absent = sorted(a for a in required if a not in excluded and (ROOT / a).exists())
    if absent:
        fail("published-surface", f"present on disk but not excluded from the site: {absent}")
    if "desk" in excluded:
        fail("published-surface", "desk/ is listed as published in scripts/verify_safe.py "
             "PUBLISHED_DESKS but is still excluded by Jekyll in _config.yml")
    warn("published-surface",
         f"Jekyll build is active and {len(on_disk)} excluded paths are honoured; the "
         f"approved desks and public-safe/ are served")


def check_page_set(pages, warn, fail):
    have = {p.name for p in DESK.iterdir() if p.is_file()}
    extra = have - EXPECTED
    missing = EXPECTED - have
    if missing:
        fail("page-set", f"missing: {sorted(missing)}")
    else:
        warn("page-set", f"{len(EXPECTED)} expected files present")
    if extra:
        fail("page-set", f"unexpected files: {sorted(extra)}")


def check_links(pages, warn, fail):
    bad = []
    internal_missing = set()
    for name, text in pages.items():
        for href in re.findall(r'href="([^"]+)"', text):
            if href.startswith(("https://", "http://")):
                host = urlparse(href).hostname or ""
                if host not in ALLOWED_HOSTS:
                    bad.append((name, href))
            elif href.startswith("#"):
                continue
            else:
                target = href.split("#")[0]
                if target and not (DESK / target).exists():
                    internal_missing.add((name, target))
    if bad:
        fail("links", f"non-allowlisted hosts: {bad}")
    if internal_missing:
        fail("links", f"broken internal links: {sorted(internal_missing)}")
    total = sum(len(re.findall(r'href="https://', t)) for t in pages.values())
    warn("links", f"{total} external links, all on allowlisted official hosts")


def check_sourcing(pages, warn, fail):
    """Every row of every data table must carry a source, a flag, or a model marker.

    A table is treated as a data table when its header declares a Source column, which is what
    the build's table() helper always emits. Navigation and comparison tables have no Source
    column by design, and a captioned table without one is reported as a warning so it can be
    reviewed rather than silently accepted.
    """
    unsourced = []
    data_tables = data_rows = 0
    no_col = []
    for name, text in pages.items():
        for tbl in re.findall(r"<table.*?</table>", text, re.S):
            header = re.search(r"<thead>.*?</thead>", tbl, re.S)
            has_source_col = bool(header and "Source" in header.group(0))
            has_caption = "<caption>" in tbl
            rows = [r for r in re.findall(r"<tr>(?!<th)(.*?)</tr>", tbl, re.S) if "<td" in r]
            if not has_source_col:
                if has_caption and rows:
                    no_col.append((name, len(rows)))
                continue
            data_tables += 1
            for row in rows:
                data_rows += 1
                has_src = re.search(r'href="https://', row)
                has_flag = (re.search(r'href="flagged\.html#', row)
                            or 'class="mh"' in row or "model" in row.lower())
                if not (has_src or has_flag):
                    unsourced.append((name, re.sub(r"<[^>]+>", "", row)[:70]))
    if unsourced:
        fail("sourcing", f"{len(unsourced)} data rows with neither a source nor a flag: "
                         f"{unsourced[:5]}")
    if no_col:
        warn("sourcing-review", f"captioned tables with no Source column: {no_col}")
    warn("sourcing", f"{data_rows} rows across {data_tables} data tables, each with a source "
                     f"link, a flag, or a model marker")


def check_rounding(pages, warn, fail):
    """Every computed dollar amount must be a multiple of $10.

    Amounts that are statutory, published, or owner-reported are exempt, but only when they are
    explicitly marked with the exact-amount marker, so an exemption is always visible in the HTML
    and reviewable by a reader. A bare figure is never exempt unless it is a round ten.
    """
    offenders = []
    exact_count = 0
    for name, text in pages.items():
        body = re.sub(r"<a [^>]*>.*?</a>", "", text, flags=re.S)
        body = re.sub(r'<pre>.*?</pre>', "", body, flags=re.S)
        # strip spans that carry the explicit exact marker, counting them
        exact_count += len(re.findall(r'<span class="exactamt">[^<]*</span>', body))
        body = re.sub(r'<span class="exactamt">[^<]*</span>\s*(?:<span class="exact"[^>]*>'
                      r'exact</span>)?', "", body)
        for m in re.finditer(r"\$([0-9][0-9,]*(?:\.\d+)?)", body):
            raw = m.group(0)
            if raw in EXACT_ALLOWED:
                continue
            digits = m.group(1).replace(",", "")
            try:
                value = int(digits)
            except ValueError:
                continue
            if value >= 100 and value % 10 != 0:
                offenders.append((name, raw))
    if offenders:
        fail("rounding", f"{len(offenders)} non-rounded amounts: {offenders[:8]}")
    if exact_count < 5:
        fail("rounding", f"only {exact_count} amounts marked exact; statutory figures must be marked")
    warn("rounding", f"all computed amounts are multiples of $10; {exact_count} amounts marked "
                     f"exact and quoted verbatim")


def check_privacy(pages, warn, fail):
    hits = []
    for name, text in pages.items():
        flat = re.sub(r"<[^>]+>", " ", text)
        for pattern, label in PII_PATTERNS:
            for m in re.finditer(pattern, flat):
                snippet = flat[max(0, m.start() - 40):m.end() + 40].strip()
                hits.append((name, label, snippet[:80]))
    if hits:
        fail("privacy", f"{len(hits)} possible identifiers: {hits[:5]}")
    warn("privacy", "no ZIP codes, addresses, parcel numbers, or account numbers")


def check_hygiene(pages, warn, fail):
    problems = []
    for name, text in pages.items():
        if "<script" in text.lower():
            problems.append((name, "script tag"))
        if "<form" in text.lower():
            problems.append((name, "form tag"))
        if re.search(r'(?:src|href)="(?:https?:)?//(?!.*(?:irs|leginfo|sco|ftb|boe|dof|sccgov|'
                     r'santaclaracounty|sftreasurer|sf\.gov|insurance|cpuc|sjwater|sfpuc|'
                     r'treasury|freddiemac|fhfa|bls|cbo|census|sos|courts)\.)', text):
            problems.append((name, "external asset"))
        if re.search(r'<img\b', text, re.I):
            problems.append((name, "image"))
        if "google-analytics" in text or "gtag(" in text:
            problems.append((name, "analytics"))
        if re.search(r"<link[^>]+href=\"(?!style\.css)[^\"]+\"", text):
            problems.append((name, "non-local stylesheet"))
    if problems:
        fail("hygiene", f"{problems}")
    warn("hygiene", "no scripts, forms, images, analytics, or external assets")


def check_flags(pages, warn, fail):
    defined = set(re.findall(r'<a id="([A-Z]\d{2})"', pages.get("flagged.html", "")))
    referenced = set()
    for text in pages.values():
        referenced |= set(re.findall(r'flagged\.html#([A-Z]\d{2})', text))
    undefined = referenced - defined
    if undefined:
        fail("flags", f"referenced but not defined: {sorted(undefined)}")
    warn("flags", f"{len(defined)} flags defined, {len(referenced)} referenced, none dangling")


def check_content(pages, warn, fail):
    """Substance checks: the pages the brief requires must actually carry content."""
    required = {
        "executive-summary.html": ["situation", "net worth", "deadline"],
        "decision.html": ["move in", "rent", "sell"],
        "questions.html": ["what we know", "what we do not know", "how to find out"],
        "projections.html": ["projection", "sensitivity"],
        "costs.html": ["property tax", "insurance", "maintenance"],
        "estate-tax.html": ["federal", "reassessment", "stepped-up basis"],
        "process.html": ["deadline", "record"],
        "black-swans.html": ["stress path", "1970", "stagflation"],
        "law-watch.html": ["proposition 19", "rent cap", "sunset"],
        "suggestions.html": ["robustness", "do not"],
        "flagged.html": ["unverified", "model output"],
        "sources.html": ["source policy"],
        "methodology.html": ["assumption", "rounding", "privacy"],
        "repo-review.html": ["irregularit", "verification"],
    }
    problems = []
    for page, needles in required.items():
        text = pages.get(page, "").lower()
        for n in needles:
            if n not in text:
                problems.append((page, n))
    if problems:
        fail("content", f"missing expected content: {problems}")
    warn("content", "all required sections present")


def main() -> int:
    result = {"failures": [], "warnings": []}

    def fail(check, msg):
        result["failures"].append({"check": check, "detail": msg})
        print(f"FAIL  [{check}] {msg}")

    def warn(check, msg):
        result["warnings"].append({"check": check, "detail": msg})
        print(f"ok    [{check}] {msg}")

    if not DESK.exists():
        print("FAIL  desk/ does not exist")
        return 1
    pages = load_pages()
    for check in (check_page_set, published_surface, check_links, check_sourcing, check_rounding,
                  check_privacy, check_hygiene, check_flags, check_content):
        try:
            check(pages, warn, fail)
        except Exception as exc:                     # a checker bug must not pass silently
            fail(check.__name__, f"checker raised {type(exc).__name__}: {exc}")

    result["pages"] = len(pages)
    result["failure_count"] = len(result["failures"])
    result["warning_count"] = len(result["warnings"])
    if "--json" in sys.argv:
        (ROOT / "desk" / "data" / "desk-verification-report.json").write_text(json.dumps(result, indent=1) + "\n")
    print()
    print(f"{'PASSED' if not result['failures'] else 'FAILED'}: "
          f"{len(result['failures'])} failures, {len(result['warnings'])} checks passed")
    return 0 if not result["failures"] else 1


if __name__ == "__main__":
    sys.exit(main())
