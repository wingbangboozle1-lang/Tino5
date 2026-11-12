"""Structural, source-link, rounding, and privacy verifier for desk-b4f/.

Run: python3 desk-b4f/scripts/verify.py
"""
import hashlib
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_PAGES = {
    "index.html",
    "decision.html",
    "properties.html",
    "projections.html",
    "costs.html",
    "estate-tax.html",
    "black-swans.html",
    "process.html",
    "law-watch.html",
    "repo-audit.html",
    "flagged.html",
    "sources.html",
}

OFFICIAL_HOSTS = (
    "irs.gov",
    "ftb.ca.gov",
    "sco.ca.gov",
    "boe.ca.gov",
    "leginfo.legislature.ca.gov",
    "selfhelp.courts.ca.gov",
    "electionresults.sos.ca.gov",
    "insurance.ca.gov",
    "cpuc.ca.gov",
    "pge.com",
    "sfpuc.gov",
    "sftreasurer.org",
    "sf.gov",
    "sfgov.legistar.com",
    "santaclaracounty.gov",
    "bls.gov",
    "fhfa.gov",
)

FORBIDDEN_PATTERNS = [
    r"[\w.+-]+@[\w.-]+\.[a-z]{2,}",
    r"\b\d{3}-\d{2}-\d{4}\b",
    r"\b(?!20\d{2}-\d{2}-\d{2}\b)\d{3,4}-\d{2,3}-\d{3}\b",
    r"\b\d{2,5}\s+[A-Z][a-z]+\s+(?:St|Ave|Rd|Dr|Blvd|Ln|Ct|Way|Pl)\b",
]

# SHA-256 16-hex prefixes of normalized private ZIPs, city/neighborhoods, and raw unrounded inputs
# (zero literal PII in source; county names and $100k-banded model baselines remain allowed).
FORBIDDEN_DIGESTS = frozenset({
    "2478d903d7c875f0",
    "43086d953bcc428c",
    "39842cd9da3b334e",
    "099edec0edb103d8",
    "492053065ed017f4",
    "85df60af2698a93c",
    "02cf62656564decc",
    "f6f9c5f004b4e5b5",
    "13ec7cc438685651",
})


def has_forbidden_digest(text):
    words = re.findall(r"[a-z]+|\d[\d,]*\d|\d+", text.lower())
    norm = [w.replace(",", "") for w in words]
    for i, tok in enumerate(norm):
        if hashlib.sha256(tok.encode()).hexdigest()[:16] in FORBIDDEN_DIGESTS:
            return True
        if i + 1 < len(norm):
            pair = f"{tok} {norm[i + 1]}"
            if hashlib.sha256(pair.encode()).hexdigest()[:16] in FORBIDDEN_DIGESTS:
                return True
    return False


class PageCheck(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.has_noindex = False
        self.in_tbody = False
        self.in_row = False
        self.row_links = 0
        self.row_count = 0
        self.ext_links = 0
        self.local_refs = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "meta" and d.get("name") == "robots":
            content = d.get("content", "")
            if "noindex" in content and "nofollow" in content:
                self.has_noindex = True
        elif tag == "link" and "href" in d:
            self.local_refs.append(d["href"])
        elif tag == "tbody":
            self.in_tbody = True
        elif tag == "tr" and self.in_tbody:
            self.in_row = True
            self.row_links = 0
            self.row_count += 1
        elif tag == "a" and "href" in d:
            href = d["href"]
            if href.startswith("https://"):
                host = urlparse(href).netloc.lower()
                if not any(host == h or host.endswith("." + h) for h in OFFICIAL_HOSTS):
                    self.errors.append(f"{self.path.name}: unapproved external host {href}")
                self.ext_links += 1
                if self.in_row:
                    self.row_links += 1
            elif href.startswith("http://"):
                self.errors.append(f"{self.path.name}: insecure http:// link {href}")
            elif not href.startswith("#"):
                self.local_refs.append(href)

    def handle_endtag(self, tag):
        if tag == "tr" and self.in_row:
            if self.row_links == 0:
                self.errors.append(f"{self.path.name}: tbody row #{self.row_count} lacks an official source link")
            self.in_row = False
        elif tag == "tbody":
            self.in_tbody = False


def check_rounding(path, html):
    # Strip <span class="stat">...</span> so exact statutory constants can appear verbatim,
    # and strip HTML tags/attributes before scanning prose & tables.
    no_stat = re.sub(r'<span class="stat">.*?</span>', " ", html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", no_stat)
    errs = []
    # Reject shorthand $k / $M outside statutory spans
    for m in re.finditer(r"\$[\d,.]+[kKmMbB]\b", text):
        errs.append(f"{path.name}: unexpanded shorthand amount {m.group(0)!r}")
    # Check every dollar amount matches integer multiple of $10
    for m in re.finditer(r"\$(\d[\d,]*(?:\.\d+)?)", text):
        raw = m.group(1).replace(",", "")
        if "." in raw:
            errs.append(f"{path.name}: non-integer dollar amount ${m.group(1)} outside <span class='stat'>")
        elif int(raw) % 10 != 0:
            errs.append(f"{path.name}: non-$10-rounded amount ${m.group(1)} outside <span class='stat'>")
    return errs


def main():
    actual = {p.name for p in ROOT.glob("*.html")}
    errors = []
    if actual != EXPECTED_PAGES:
        missing = sorted(EXPECTED_PAGES - actual)
        extra = sorted(actual - EXPECTED_PAGES)
        errors.append(f"page set mismatch: missing={missing}, extra={extra}")

    total_rows = 0
    total_links = 0
    for page in sorted(ROOT.glob("*.html")):
        html = page.read_text(encoding="utf-8")
        parser = PageCheck(page)
        parser.feed(html)
        parser.close()

        if not parser.has_noindex:
            errors.append(f"{page.name}: missing <meta name='robots' content='noindex, nofollow'>")
        for ref in parser.local_refs:
            target = (ROOT / ref.split("#")[0]).resolve()
            if not target.exists():
                errors.append(f"{page.name}: broken local reference {ref}")

        errors.extend(parser.errors)
        errors.extend(check_rounding(page, html))

        # Privacy check across stripped text + raw HTML
        plain = re.sub(r"<[^>]+>", " ", html)
        for pat in FORBIDDEN_PATTERNS:
            if re.search(pat, plain):
                errors.append(f"{page.name}: matched forbidden pattern {pat}")
        if has_forbidden_digest(plain):
            errors.append(f"{page.name}: matched forbidden SHA-256 privacy digest")

        total_rows += parser.row_count
        total_links += parser.ext_links

    if errors:
        print("FAIL:")
        for e in errors[:40]:
            print("  -", e)
        if len(errors) > 40:
            print(f"  ... and {len(errors) - 40} more")
        sys.exit(1)

    print(f"PASS: {len(actual)} pages; {total_rows} source-linked rows; {total_links} official HTTPS links; $10 rounding & privacy verified.")


if __name__ == "__main__":
    main()
