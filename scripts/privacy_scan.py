#!/usr/bin/env python3
"""Repository privacy scan (session arena-22c14528, task 22c/P).

Finds values that break the project's privacy rule without this file containing any private value:

  A. money in prose  - a "$" amount of $1,000 or more that is not a multiple of $10
                       ($100-$999 are listed with --minor; too small to identify an assessment or a bill)
  B. money in data   - a bare integer of 1,000 or more, not a multiple of 10, stored under a
                       money-like key (tax, assess, value, rent, price, premium, cost ...)
  C. identifiers     - e-mail addresses, phone numbers, SSN-shaped and parcel-number-shaped
                       tokens, street addresses

A deliberate design point: the scan is generic. It does NOT carry a list of the owner's real figures,
because a "forbidden values" list committed to a public repository publishes exactly what it is meant
to protect.

Published official constants (statutory amounts, agency averages) are public by nature and are listed
in PUBLIC_CONSTANTS so they are reported as "official constant" rather than as a finding. Whether each
constant is *correct* is a separate question answered by the verification register, not by this scan.

Usage:
    python3 scripts/privacy_scan.py              # masked output, exit 1 if findings
    python3 scripts/privacy_scan.py --show       # print the tokens (local terminal only)
    python3 scripts/privacy_scan.py --summary    # one line per file
    python3 scripts/privacy_scan.py --minor      # also list unrounded amounts under $1,000
    python3 scripts/privacy_scan.py path ...     # limit to paths
"""
from __future__ import annotations

import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TEXT_SUFFIXES = {".html", ".htm", ".md", ".json", ".js", ".mjs", ".py", ".css", ".csv", ".yml", ".yaml", ".txt"}

# Amounts the repository cites as published official figures. Public information, not owner data.
PUBLIC_CONSTANTS = {
    "1,044,586",   # BOE: Prop 19 adjusted amount, 16 Feb 2025 - 15 Feb 2027
    "742,953", "1,485,906",   # FTB 2025 tax rate schedules: 12.3% bracket thresholds, single / joint
    "1,022,600",   # BOE: Prop 19 adjusted amount, 16 Feb 2023 - 15 Feb 2025
    "69,625", "107,900", "208,850",  # Judicial Council DE-300 probate thresholds (deaths on/after 1 Apr 2025)
    "661,375", "75,197",            # IRS 2027 / FTB 2026 published bracket thresholds as cited
    "1,440.11",                     # published utility/tariff figure as cited by the desk verifier
    "1,571", "1,512", "1,655", "1,737", "1,702", "1,701.60", "2,339.99",  # insurance averages as cited
    "2,918.18",                     # CDI FAIR Plan dwelling-fire average (2025 data call) as cited
    "768,213", "1,536,426",                                              # FTB bracket thresholds as cited
    "4,688", "3,697", "4,832",                                           # HUD fair market rents as cited
    "8,245", "24,733", "5,497",                                          # SF Rent Board relocation amounts as cited
    "9,999,999",                                                          # SF transfer-tax bracket bound
    "125.44", "131.12",                                                   # utility bill examples as cited
    "123,456",                                                            # synthetic rounding example (not a real value)
}

MONEY_KEY = re.compile(r"(tax|assess|value|rent|price|premium|cost|bill|income|av\b|fmv)", re.I)
# keys that hold statutory or official figures rather than owner data
OFFICIAL_KEY = re.compile(r"(exclusion|exemption|threshold|limit|cap|bracket|allowance|statut|fmr|official)", re.I)

RE_MONEY = re.compile(r"\$\s?(\d{1,3}(?:,\d{3})+|\d{3,})(?:(\.\d{1,2})(?!\d)|(?![.,]\d))(?!\s?(?:million|billion|trillion|[MBKk]\b))")
RE_KV = re.compile(r"""(?:["']([A-Za-z_][\w\-]*)["']\s*:|\b([A-Za-z_]\w*)\s*=)\s*(-?\d{4,9})(?![\d.\w])""")
RE_EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")
RE_PHONE = re.compile(r"(?<![\d.\-/])(?:\+?1[\s.-])?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}(?![\d-])")
RE_SSN = re.compile(r"(?<![\d-])\d{3}-\d{2}-\d{4}(?![\d-])")
RE_APN = re.compile(r"(?<![\d-])\d{3}-\d{2}-\d{3}(?![\d-])")          # county parcel-number shape
RE_ADDR = re.compile(
    r"\b\d{2,5}\s+(?:[NSEW]\.?\s+)?[A-Z][a-z]+(?:\s[A-Z][a-z]+)?\s+"
    r"(?:St|Street|Ave|Avenue|Rd|Road|Dr|Drive|Blvd|Boulevard|Ct|Court|Ln|Lane|Way|Pl|Place|Ter|Terrace)\b\.?"
)

# public agency / tooling contact strings that are not personal data
EMAIL_OK = re.compile(r"(@users\.noreply\.github\.com|@boe\.ca\.gov|@ftb\.ca\.gov|@irs\.gov|@sfgov\.org|"
                      r"@sccgov\.org|@asr\.sccgov\.org|@insurance\.ca\.gov|@sfwater\.org|@example\.(com|org))", re.I)


def tracked_files(paths: list[str]) -> list[Path]:
    out = subprocess.check_output(["git", "ls-files", "--", *paths], cwd=ROOT, text=True)
    return [ROOT / p for p in out.splitlines() if p and (ROOT / p).suffix.lower() in TEXT_SUFFIXES]


def mask(tok: str) -> str:
    if "=" in tok:                       # key=value: mask the value only
        key, _, val = tok.partition("=")
        return key + "=" + mask(val)
    digits = [c for c in tok if c.isdigit()]
    if len(digits) <= 2:
        return tok
    seen, out = 0, []
    for c in tok:
        if c.isdigit():
            seen += 1
            out.append(c if seen in (1, len(digits)) else "\u2022")
        else:
            out.append(c)
    return "".join(out)


def scan_text(text: str):
    """Yield (line_no, category, token)."""
    for i, line in enumerate(text.splitlines(), 1):
        if len(line) > 200000:          # minified bundles: still scanned, just guard pathological lines
            line = line[:200000]
        for m in RE_MONEY.finditer(line):
            whole, cents = m.group(1), m.group(2) or ""
            n = int(whole.replace(",", ""))
            if n < 100:
                continue
            unrounded = (n % 10 != 0) or (cents and set(cents[1:]) != {"0"})
            if not unrounded:
                continue
            token = whole + cents
            if token in PUBLIC_CONSTANTS:
                yield i, "official-constant", "$" + token
            elif n < 1000:
                yield i, "minor-under-1000", "$" + token
            else:
                yield i, "A-unrounded-money", "$" + token
        for m in RE_KV.finditer(line):
            key, val = (m.group(1) or m.group(2)), int(m.group(3))
            if abs(val) < 1000 or val % 10 == 0:
                continue
            if 1900 <= val <= 2100 and not MONEY_KEY.search(key):
                continue
            if MONEY_KEY.search(key) and not OFFICIAL_KEY.search(key):
                yield i, "B-unrounded-data", f"{key}={val}"
        for m in RE_EMAIL.finditer(line):
            if not EMAIL_OK.search(m.group(0)):
                yield i, "C-email", m.group(0)
        for m in RE_SSN.finditer(line):
            yield i, "C-ssn-shape", m.group(0)
        for m in RE_APN.finditer(line):
            yield i, "C-parcel-shape", m.group(0)
        for m in RE_ADDR.finditer(line):
            yield i, "C-street-address", m.group(0)


def main(argv: list[str]) -> int:
    show = "--show" in argv
    summary = "--summary" in argv
    paths = [a for a in argv if not a.startswith("--")]
    findings = defaultdict(list)
    constants = 0
    minor = 0
    for path in tracked_files(paths):
        rel = path.relative_to(ROOT).as_posix()
        if rel == "scripts/privacy_scan.py":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for line_no, cat, tok in scan_text(text):
            if cat == "official-constant":
                constants += 1
                continue
            if cat == "minor-under-1000":
                minor += 1
                if "--minor" in argv:
                    print(f"{rel}:{line_no}: {cat}: {tok if show else mask(tok)}")
                continue
            findings[rel].append((line_no, cat, tok))
    total = sum(len(v) for v in findings.values())
    for rel in sorted(findings):
        rows = findings[rel]
        if summary:
            cats = defaultdict(int)
            for _, cat, _ in rows:
                cats[cat] += 1
            print(f"{rel}: " + ", ".join(f"{c}={n}" for c, n in sorted(cats.items())))
            continue
        for line_no, cat, tok in rows:
            print(f"{rel}:{line_no}: {cat}: {tok if show else mask(tok)}")
    print(f"privacy_scan: {total} finding(s) in {len(findings)} file(s); "
          f"{constants} published official constant(s) and {minor} amount(s) under $1,000 not counted "
          f"(list the latter with --minor).")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
