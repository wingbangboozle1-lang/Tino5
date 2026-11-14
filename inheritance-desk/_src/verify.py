#!/usr/bin/env python3
"""Publish gate for the inheritance decision desk. Exit 0 = PASS, 1 = FAIL.

Checks:
 V1 every table row carries an official-source link, or a blank value with a flag, or an explicit "no external source" marker
 V2 every external link is on an official host allowlist
 V3 every internal link resolves to a page in this folder (or an anchor on a page)
 V4 every visible money figure is a multiple of $10, unless it is wrapped in <span class="stat"> (published statutory amount)
 V5 no personal identifiers: street-address patterns, 5-digit ZIP codes, city names of the owner's properties, APN-style parcel numbers, e-mail, phone
 V6 no owner tax-history series is published (owner single inputs only, in a labelled list)
 V7 every page in the nav exists
"""
import html as H
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

DESK = Path(__file__).resolve().parent.parent
ALLOWED_HOSTS = {
    "www.irs.gov", "leginfo.legislature.ca.gov", "www.boe.ca.gov", "www.sos.ca.gov", "www.ftb.ca.gov",
    "www.federalreservehistory.org", "www.federalreserve.gov", "home.treasury.gov",
    "files.santaclaracounty.gov", "www.insurance.ca.gov",
}
OFFICIAL = ALLOWED_HOSTS
FLAG_RE = re.compile(r"\[F\d\d\]")
PII = [
    (re.compile(r"\b\d{1,5}\s+(West|East|North|South|[A-Z][a-z]+)\s+(Tasman|Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Way|Lane|Ln|Court|Blvd)\b"), "street address"),
    (re.compile(r"\b9[0-9]{4}\b"), "ZIP-like 5-digit number (possible ZIP)"),
    (re.compile(r"\b\d{3}-\d{3}-\d{3}\b"), "parcel-style number"),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "e-mail"),
    (re.compile(r"\(\d{3}\)\s*\d{3}-\d{4}|\b\d{3}-\d{3}-\d{4}\b"), "phone"),
    (re.compile(r"Cupertino|San Francisco|Sunnyvale|Saratoga|Los Altos|Mountain View|Bay Area", re.I), "owner city/neighbourhood name"),
]


class Doc(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.text_parts = [], set(), []
        self.tables = []   # list of (headers, rows) where row = list of cell html strings
        self._in_table = 0
        self._cur_row = None
        self._cur_cell = None
        self._hdr = []
        self._in_thead = False
        self._skip = 0
        self._stat = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag in ("script", "style"):
            self._skip += 1
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
        if tag == "table":
            self._in_table += 1
            self.tables.append(([], []))
        if tag == "thead":
            self._in_thead = True
        if tag == "tr" and self._in_table:
            self._cur_row = []
        if tag in ("td", "th") and self._in_table:
            self._cur_cell = []
            if tag == "th":
                self._in_thead = True
        if tag == "span" and a.get("class") == "stat":
            self._stat += 1
            self._stat_depth = getattr(self, "_stat_depth", [])
        if self._cur_cell is not None:
            self._cur_cell.append(self.get_starttag_text() or "")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip -= 1
        if self._cur_cell is not None and tag not in ("td", "th"):
            self._cur_cell.append(f"</{tag}>")
        if tag in ("td", "th") and self._cur_cell is not None:
            cell = "".join(self._cur_cell)
            if self._cur_row is not None:
                self._cur_row.append(cell)
            self._cur_cell = None
        if tag == "tr" and self._cur_row is not None and self._in_table:
            t_headers, t_rows = self.tables[-1]
            if self._in_thead or not t_headers:
                if not t_rows and not t_headers:
                    t_headers.extend(self._cur_row)
                elif not t_headers:
                    t_headers.extend(self._cur_row)
                else:
                    t_rows.append(self._cur_row)
            else:
                t_rows.append(self._cur_row)
            self._cur_row = None
        if tag == "thead":
            self._in_thead = False
        if tag == "table":
            self._in_table -= 1
        if tag == "span" and self._stat:
            self._stat -= 1

    def handle_data(self, data):
        if self._skip:
            return
        if self._cur_cell is not None:
            self._cur_cell.append(H.escape(data, quote=False))
        self.text_parts.append((data, self._stat > 0))


def strip_tags(s):
    return H.unescape(re.sub(r"<[^>]+>", " ", s))


def check_page(path, names):
    fails = []
    src = path.read_text()
    d = Doc()
    d.feed(src)
    name = path.name
    # V1 table rows
    for headers, rows in d.tables:
        for r in rows:
            joined = " ".join(r)
            hrefs = re.findall(r'href="([^"]+)"', joined)
            ext = [h for h in hrefs if h.startswith("http")]
            official = [h for h in ext if re.match(r"https://([^/]+)/", h) and re.match(r"https://([^/]+)/", h).group(1) in OFFICIAL]
            blank_flagged = (strip_tags(r[1]).strip().startswith("Blank") and FLAG_RE.search(strip_tags(joined)) is not None) or \
                            (FLAG_RE.search(strip_tags(joined)) is not None and "Blank" in strip_tags(r[1]))
            no_ext = "no external source" in strip_tags(joined).lower()
            if not (official or blank_flagged or no_ext):
                fails.append(f"V1 {name}: row lacks official source/blank+flag: {strip_tags(joined)[:90]}")
    # V2 external hosts
    for h in d.links:
        if h.startswith("http"):
            host = re.match(r"https://([^/]+)/", h)
            if not host or host.group(1) not in ALLOWED_HOSTS:
                fails.append(f"V2 {name}: non-allowlisted host {h[:80]}")
        elif h.endswith(".html") or ".html#" in h:
            target, _, anchor = h.partition("#")
            if target and target not in names:
                fails.append(f"V3 {name}: unresolved internal link {h}")
            if anchor and target == "" and anchor not in d.ids:
                fails.append(f"V3 {name}: missing anchor {h}")
    # V4 money on visible text outside stat spans
    text = " ".join(t for t, stat in d.text_parts if not stat)
    for m in re.finditer(r"\$\s?([\d,]+(?:\.\d+)?)", text):
        val = float(m.group(1).replace(",", ""))
        if val % 10 != 0 and not re.search(r"\.\d", m.group(1)):
            fails.append(f"V4 {name}: money not multiple of $10: ${m.group(1)}")
    # V5 PII
    vis = " ".join(t for t, _ in d.text_parts)
    for rx, label in PII:
        for m in rx.finditer(vis):
            fails.append(f"V5 {name}: {label}: '{m.group(0)}'")
    # V6: owner tax-history series are never published; only single owner-supplied inputs appear, in the labelled list
    if "tax history" in vis.lower() or "2014" in vis:
        fails.append(f"V6 {name}: owner tax-history series wording or years present")
    for bad in ("7,210", "539,740", "2,440", "114,250"):
        if bad in vis:
            fails.append(f"V6 {name}: owner prior-year assessment or tax figure published: {bad}")
    return fails


def main():
    names = {p.name for p in DESK.glob("*.html")}
    fails = []
    pages = sorted(DESK.glob("*.html"))
    for p in pages:
        fails += check_page(p, names)
    for needed in ["index.html", "what-changes.html", "facts.html", "property.html", "scenarios.html",
                   "black-swans.html", "projections.html", "costs.html", "process.html", "glossary.html",
                   "questions.html", "suggestions.html", "briefing.html", "methodology.html", "flagged.html"]:
        if needed not in names:
            fails.append(f"V7 missing page {needed}")
    print(f"pages checked: {len(pages)}")
    for f in fails:
        print(f)
    print("PASS" if not fails else f"FAIL: {len(fails)} findings")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
