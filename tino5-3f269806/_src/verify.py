"""Structural verifier for the decision site. Run: python3 _src/verify.py  (exit 0 = pass)."""
import os, re, sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
from build import PAGES  # noqa
from sources import SRC  # noqa

ALLOWED_HOSTS = {
    "www.irs.gov", "www.boe.ca.gov", "boe.ca.gov", "www.sco.ca.gov", "files.santaclaracounty.gov",
    "sftreasurer.org", "www.federalreserve.gov", "www.bls.gov", "www.pge.com", "www.insurance.ca.gov",
    "www.sfpuc.org", "www.sjwater.com", "voterguide.sos.ca.gov", "www.congress.gov",
    "www.law.cornell.edu", "weekslawfirm.com", "www.sccassessor.org", "www.sfassessor.org", "www.scctax.org",  # weekslawfirm = secondary, labelled as such on the page
}
# exact statutory / agency amounts that are permitted not to be multiples of $10 (marked with class-free S() output)
STATUTORY_OK = {1, 56, 67, 76, 1044586, 15000000, 19000, 16250, 3300, 7000}
PII_PATTERNS = [
    (r"\b9[0-9]{4}\b", "ZIP-like 5-digit token starting with 9"),
    (r"\bCupertino\b|\bSunnyvale\b|\bSunset\b|\bOuter\b", "city or neighbourhood name"),
    (r"[\w.]+@[\w.]+\.\w+", "e-mail address"),
    (r"\(\d{3}\)\s?\d{3}-\d{4}|\b\d{3}-\d{3}-\d{4}\b", "phone number"),
    (r"\b\d{1,5}\s+\w+\s+(St|Street|Ave|Avenue|Blvd|Road|Rd|Way|Drive|Dr|Lane|Ln)\b", "street address"),
    (r"\bAPN\b|\bparcel number\b|\baccount number\b", "parcel or account identifier wording"),
]


class Pg(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.rows = []      # (cells_text, has_source_link)
        self._in_tbody = False
        self._row = None
        self._cell = None
        self._cells = []
        self._cell_links = 0
        self.text = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
            if self._cell is not None:
                self._cell_links += 1
        if tag == "tbody":
            self._in_tbody = True
        if tag == "tr" and self._in_tbody:
            self._row = []
            self._cells = []
        if tag == "td" and self._row is not None:
            self._cell = []
            self._cell_links = 0

    def handle_endtag(self, tag):
        if tag == "tbody":
            self._in_tbody = False
        if tag == "td" and self._cell is not None:
            self._cells.append((" ".join(self._cell), self._cell_links))
            self._cell = None
        if tag == "tr" and self._row is not None:
            last_links = self._cells[-1][1] if self._cells else 0
            self.rows.append(([c for c, _ in self._cells], last_links))
            self._row = None

    def handle_data(self, data):
        self.text.append(data)
        if self._cell is not None:
            self._cell.append(data)


def main():
    problems = []
    names = [p for p, _ in PAGES]
    for n in names:
        if not os.path.exists(os.path.join(OUT, n)):
            problems.append(f"missing page {n}")
    if problems:
        print("\n".join(problems)); return 1

    FORBIDDEN = ["529,160", "114,250", "440,310", "96,560", "tax history"]  # owner history: internal only
    for n in names:
        raw_all = open(os.path.join(OUT, n), encoding="utf-8").read()
        for f in FORBIDDEN:
            if f in raw_all:
                problems.append(f"{n}: owner history value published: {f}")
    stats = dict(pages=0, rows=0, links=0, money=0)
    for n in names:
        raw = open(os.path.join(OUT, n), encoding="utf-8").read()
        stats["pages"] += 1
        if "{{" in raw or "{%" in raw:
            problems.append(f"{n}: template token present")
        p = Pg()
        p.feed(raw)
        stats["links"] += len(p.links)
        # row-level source check
        for cells, has_src in p.rows:
            stats["rows"] += 1
            if has_src < 1:
                problems.append(f"{n}: table row without an official source link: {cells[0][:60]}")
        # link checks
        for href in p.links:
            if href.startswith("http"):
                host = re.sub(r"^https?://", "", href).split("/")[0]
                if host not in ALLOWED_HOSTS:
                    problems.append(f"{n}: external host not allowlisted: {host}")
            elif href.startswith("#") or href.startswith("mailto:"):
                pass
            else:
                target = href.split("#")[0]
                if target and not os.path.exists(os.path.join(OUT, target)):
                    problems.append(f"{n}: broken internal link {href}")
        # money rounding
        text = " ".join(p.text)
        for m in re.finditer(r"-?\$([0-9][0-9,]*)", text):
            val = int(m.group(1).replace(",", ""))
            stats["money"] += 1
            if val % 10 != 0 and val not in STATUTORY_OK:
                problems.append(f"{n}: money not rounded to $10: ${m.group(1)}")
        # privacy patterns on visible text and on attribute-free content
        for pat, label in PII_PATTERNS:
            for m in re.finditer(pat, text):
                problems.append(f"{n}: possible {label}: {m.group(0)[:40]!r}")
    print("pages:", stats["pages"], "table rows:", stats["rows"], "links:", stats["links"], "money tokens:", stats["money"])
    if problems:
        print("PROBLEMS:")
        for x in problems[:200]:
            print(" -", x)
        return 1
    print("VERIFY PASS: every table row has an official source link; links allowlisted; money rounded to $10 except statutory amounts; no identifier patterns.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
