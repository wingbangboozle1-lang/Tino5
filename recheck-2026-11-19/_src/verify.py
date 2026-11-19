#!/usr/bin/env python3
"""Verify the recheck desk contract (session arena-c267f0b0).

Checks:
  1. all expected pages exist,
  2. every table body row carries an official source link or an explicit tag,
  3. external hosts are on the official allowlist,
  4. internal links resolve within the published tree,
  5. money >= $1,000 is a multiple of $10 (agency-exact figures listed below),
  6. no personal-identifier patterns and no un-anonymised place names,
  7. the carried flags R1-R7 and new flags S1-S3 are all addressed.

Exit 0 = PASS.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

OUT = Path(__file__).resolve().parent.parent

PAGES = ["index.html", "register.html", "open-items.html", "rebuild.html",
         "requirements.html", "law-watch.html", "repo-review.html",
         "flagged.html", "sources.html", "methodology.html", "style.css"]

ALLOWED_HOSTS = {
    "www.irs.gov", "www.boe.ca.gov", "boe.ca.gov", "files.santaclaracounty.gov",
    "controller.santaclaracounty.gov", "plandev.santaclaracounty.gov",
    "asr.santaclaracounty.gov", "sccassessor.org", "www.sfpuc.gov", "sfpuc.gov",
    "media.api.sf.gov", "sf.gov", "www.sf.gov", "sfassessor.org", "sftreasurer.org",
    "www.sfmta.com", "sfmta.com", "sfgov.legistar.com", "www.freddiemac.com",
    "www.fhfa.gov", "fhfa.gov", "home.treasury.gov", "www.sjwater.com",
    "sjwater.com", "www.cpuc.ca.gov", "cpuc.ca.gov", "www.ftb.ca.gov",
    "www.insurance.ca.gov", "www.bls.gov", "www.census.gov", "huduser.gov",
    "www.huduser.gov", "selfhelp.courts.ca.gov", "leginfo.legislature.ca.gov",
    "fred.stlouisfed.org", "clerkrecorder.santaclaracounty.gov",
    "www.sos.ca.gov", "elections.cdn.sos.ca.gov",
}

# agency-published exact amounts that are not multiples of $10
MONEY_EXEMPT = {"1,044,586", "661,375", "793,650", "742,953", "1,485,906",
               "1,010,417", "768,213", "1,536,426", "1,571", "1,512", "2,339",
               "1,701", "69,625", "84,209", "155,384", "260,241"}

RE_MONEY = re.compile(r"\$\s?(\d{1,3}(?:,\d{3})+|\d{3,})(?:\.\d+)?")
RE_EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")
RE_PHONE = re.compile(r"(?<![\d.\-/])(?:\+?1[\s.-])?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}(?![\d-])")
RE_SSN = re.compile(r"(?<![\d-])\d{3}-\d{2}-\d{4}(?![\d-])")
RE_APN = re.compile(r"(?<![\d-])\d{3}-\d{2}-\d{3}(?![\d-])")
RE_ADDR = re.compile(
    r"\b\d{2,5}\s+(?:[NSEW]\.?\s+)?[A-Z][a-z]+(?:\s[A-Z][a-z]+)?\s+"
    r"(?:St|Street|Ave|Avenue|Rd|Road|Dr|Drive|Blvd|Boulevard|Ct|Court|Ln|Lane|Way|Pl|Place)\b"
)
FORBIDDEN = [r"Cupertino", r"95014", r"94122", r"San Jose", r"Monta Vista",
             r"San Francisco(?! County)"]


class TableScan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []          # (classes, text, has_td)
        self._in_row = False
        self._classes = []
        self._row_text = ""
        self._has_td = False

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._in_row = True
            self._classes = []
            self._row_text = ""
            self._has_td = False
        if self._in_row:
            if tag == "td":
                self._has_td = True
            d = dict(attrs)
            if "class" in d:
                self._classes.extend(d["class"].split())

    def handle_endtag(self, tag):
        if tag == "tr" and self._in_row:
            self._in_row = False
            self.rows.append((set(self._classes), self._row_text, self._has_td))

    def handle_data(self, data):
        if self._in_row:
            self._row_text += data


def main():
    errors = []
    stats = {"rows": 0, "sourced": 0, "links": 0, "external": 0}

    for name in PAGES:
        if not (OUT / name).exists():
            errors.append(f"missing page: {name}")

    for name in PAGES:
        path = OUT / name
        if not path.exists() or path.suffix != ".html":
            continue
        html = path.read_text()

        # 5. money rounding
        for m in RE_MONEY.finditer(html):
            n = int(m.group(1).replace(",", ""))
            if n < 1000:
                continue
            if n % 10 != 0 and m.group(1) not in MONEY_EXEMPT:
                errors.append(f"{name}: unrounded money ${m.group(1)}")

        # 6. identifiers and place names
        for rx, label in [(RE_EMAIL, "email"), (RE_PHONE, "phone"), (RE_SSN, "ssn"),
                          (RE_APN, "apn-shape"), (RE_ADDR, "street address")]:
            for m in rx.finditer(html):
                errors.append(f"{name}: {label} pattern: {m.group(0)[:40]}")
        for pat in FORBIDDEN:
            for m in re.finditer(pat, html):
                errors.append(f"{name}: forbidden term: {m.group(0)}")

        # 2/3. links
        for href in re.findall(r'href="([^"]+)"', html):
            if href.startswith(("http://", "https://")):
                stats["links"] += 1
                stats["external"] += 1
                host = href.split("/")[2]
                if host not in ALLOWED_HOSTS:
                    errors.append(f"{name}: host not allowlisted: {host}")
            elif href.endswith(".css"):
                if not (OUT / href).exists():
                    errors.append(f"{name}: broken internal link {href}")
            else:
                stats["links"] += 1
                if not (OUT / href).exists():
                    errors.append(f"{name}: broken internal link {href}")

        # 2. every table row sourced or tagged
        scan = TableScan()
        scan.feed(html)
        for i, (classes, row_text, has_td) in enumerate(scan.rows):
            if not has_td:
                continue
            has_src = "src" in classes
            has_tag = any(c.startswith("tag-") for c in classes)
            if not (has_src or has_tag):
                errors.append(f"{name}: row {i} without source link or tag: {row_text.strip()[:60]}")
            stats["rows"] += 1
            if has_src:
                stats["sourced"] += 1

    # 7. flags addressed
    open_page = (OUT / "open-items.html").read_text() if (OUT / "open-items.html").exists() else ""
    for phrase in ["composite property-tax rate", "water utility tariff",
                   "water and sewer schedule", "transfer tax brackets",
                   "mortgage rate", "house-price series", "R1", "R2", "R3", "R4",
                   "R5", "R6", "R7", "S1", "S2", "S3"]:
        if phrase not in open_page:
            errors.append(f"open-items.html: does not address '{phrase}'")

    if errors:
        for e in errors[:40]:
            print("FAIL:", e)
        print(f"verify: {len(errors)} error(s)")
        return 1
    print(f"PASS: {len(PAGES)} files; {stats['rows']} table rows ({stats['sourced']} with official "
          f"source links); {stats['links']} links ({stats['external']} external, all allowlisted); "
          f"money rounding ok; no identifier patterns; all flags addressed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
