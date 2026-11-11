"""Verify session-595f0109 artifact: privacy, rounding, links, rows.

Structural checks only, not semantic certification.
Run: python3 session-595f0109/scripts/verify.py
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []
links = 0
rows = 0

OFFICIAL = (
    "irs.gov", "boe.ca.gov", "sco.ca.gov", "ftb.ca.gov",
    "insurance.ca.gov", "bls.gov", "courts.ca.gov",
    "federalreserve.gov", "fhfa.gov", "cpuc.ca.gov",
    "sfpuc.gov", "congress.gov",
)

FORBIDDEN = [
    r"\b(?:95014|94122|550537|539743|114248|112008)\b",
    r"550,537|539,743|114,248|112,008",
    r"3,100,000|1,800,000|7,150",
    r"Cupertino|Outer Sunset|Santa Clara",
    r"San Francisco",
    r"[\w.+-]+@[\w.-]+\.[a-z]{2,}",
    r"\b\d{3}-\d{2}-\d{4}\b",
]

class Check(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.head = False
        self.inrow = False
        self.rowlinks = 0

    def handle_starttag(self, t, attrs):
        global links
        d = dict(attrs)
        if t == "thead":
            self.head = True
        if t == "tr" and not self.head:
            self.inrow = True
            self.rowlinks = 0
        if t == "a":
            href = d.get("href", "")
            if href.startswith("https://"):
                links += 1
                if not any(h in href for h in OFFICIAL):
                    errors.append(f"{self.path}: non-official external link {href}")
            elif href.startswith("http://"):
                errors.append(f"{self.path}: non-HTTPS link {href}")
            elif href and not href.startswith("#") and not href.startswith("mailto:"):
                target = href.split("#")[0]
                if target and not (self.path.parent / target).exists():
                    errors.append(f"{self.path}: broken local link {href}")
            if self.inrow:
                self.rowlinks += 1
        if t in ("script", "iframe", "form"):
            # inline <script> for the fictional calculator is allowed; flag others
            if t in ("iframe", "form"):
                errors.append(f"{self.path}: forbidden {t}")

    def handle_endtag(self, t):
        global rows
        if t == "tr" and not self.head and self.inrow:
            rows += 1
            if not self.rowlinks:
                errors.append(f"{self.path}: row without official source")
            self.inrow = False
        if t == "thead":
            self.head = False

def main():
    pages = sorted(ROOT.glob("*.html"))
    if len(pages) != 10:
        errors.append(f"Expected 10 pages, found {len(pages)}")
    for p in pages:
        text = p.read_text(encoding="utf-8")
        for pat in FORBIDDEN:
            if re.search(pat, text, re.I):
                errors.append(f"{p.name}: private fingerprint pattern {pat}")
        for m in re.finditer(r"\$([\d,]+)(?![\d,])", text):
            try:
                val = int(m.group(1).replace(",", ""))
            except ValueError:
                continue
            if val % 10 != 0:
                errors.append(f"{p.name}: unrounded money {m.group(0)}")
        if "noindex" not in text:
            errors.append(f"{p.name}: missing noindex")
        Check(p).feed(text)
    # projections row count: 51 years + header
    proj = (ROOT / "projections.html").read_text(encoding="utf-8")
    n_tr = len(re.findall(r"<tr>", proj))
    if n_tr != 58:
        errors.append(f"projections.html: expected 58 <tr> (2 headers + 51 years + 5 branches), found {n_tr}")
    # costs blank cells present
    costs = (ROOT / "costs.html").read_text(encoding="utf-8")
    if costs.count("<td></td>") < 10:
        errors.append("costs.html: expected blank verified-amount cells")
    if errors:
        print("\n".join(errors))
        print(f"FAIL: {len(errors)} errors; {rows} rows; {links} links")
        sys.exit(1)
    print(f"PASS: {len(pages)} pages; {rows} source-linked rows; {links} links; "
          "local targets resolve; privacy patterns clean; money rounded. "
          "Structural checks only, not semantic certification.")

if __name__ == "__main__":
    main()
