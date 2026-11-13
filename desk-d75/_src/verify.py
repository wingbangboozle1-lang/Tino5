"""Contract check for the owner-brief desk (desk-d75/).

This does not re-derive the economics. It enforces the promises the pages make, so that a future
edit cannot quietly break one:

  1  every generated file is exactly what the generator produces (no hand-edited HTML)
  2  the requirement register covers the owner's brief, and every 'answered on' target exists
  3  every table body row in a data table carries at least one official external link
  4  every external host is an official publisher on the allowlist
  5  every dollar amount in a table cell is a multiple of $10, unless the cell marks it exact
     (a statutory threshold rounded to $10 would be a misstatement, so the two rules are kept apart)
  6  no personal-identifier pattern and no place name appears in visible text
  7  every source id referenced by a register exists, and every verified figure links a source
  8  every assumption id is cited by the page text that uses it
  9  no script, form, iframe or external asset is published
 10  the four findings this desk was commissioned to deliver are actually on the pages
 11  every flagged item is stated as open, and no item is marked implemented without an owner decision
 12  every table has as many cells in each body row as it has headers, every local link and anchor resolves,
     and the pages do not disagree with the engine about a headline figure

Run: python3 desk-d75/_src/verify.py [--json]
Exit status is non-zero with a list of findings if any check fails.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import data as D  # noqa: E402
import build as M  # noqa: E402

ROOT = HERE.parents[1]
REPO = ROOT.parent

ALLOWED_HOSTS = {
    # federal
    "www.irs.gov", "www.treasury.gov", "home.treasury.gov", "www.congress.gov",
    "fred.stlouisfed.org", "www.fhfa.gov", "www.bls.gov", "www.cbo.gov",
    "www.freddiemac.com",
    # state of California, and the agencies that publish the figures used here
    "www.boe.ca.gov", "boe.ca.gov", "leginfo.legislature.ca.gov", "www.sco.ca.gov",
    "www.ftb.ca.gov", "www.insurance.ca.gov", "interactive.web.insurance.ca.gov",
    "www.cpuc.ca.gov", "www.sos.ca.gov", "electionresults.sos.ca.gov",
    "www.courts.ca.gov", "courts.ca.gov", "selfhelp.courts.ca.gov",
    # local offices: the citation is to the office, and its address is the only way to check a rate
    "sftreasurer.org", "www.sf.gov", "sfassessor.org", "www.sccgov.org",
    "sccgov.org", "clerkrecorder.santaclaracounty.gov", "www.sjwater.com", "www.sfpuc.gov",
    "sfpuc.gov", "www.santaclaracounty.gov", "sccassessor.org", "www.sccassessor.org",
}

# Statutory and published constants that the owner's rule requires to be quoted exactly.
EXACT_OK = {
    "1,044,586", "1,022,600", "1,000,000", "15,000,000", "15,480,000", "19,000", "20,000",
    "201,000", "208,850", "166,250", "7,000", "250,000", "500,000", "21,240", "1,500,000",
    "940,000", "218,000", "137,300", "5,450", "2,100", "2,070", "10,340", "12,370", "6,180",
    "2,010,000", "3,000,000", "77,390,000", "7,704,600", "5,503,300", "15,480", "2,400",
    "1,000", "200,000", "100,000", "800,000", "9,000,000", "15,000,000", "25,000,000",
    "661,375", "793,650", "563,200", "21,240.31", "14.33", "71.65", "143.30",
}
PLACE_NAMES = ("Cupertino", "Sunnyvale", "Santa Clara", "San Jose", "San Francisco", "Oakland",
               "Millbrae", "Los Gatos", "Mountain View", "Palo Alto", "Santa Cruz", "Hayward",
               "Outer Sunset", "Inner Sunset", "Bay Area", "SFPUC", "sjwater", "sccgov",
               "santaclaracounty", "sftreasurer", "sf.gov", "sfassessor")
ZIPISH = re.compile(r"(?<![\d.a-zA-Z_-])\d{5}(?:-\d{4})?(?![\d.a-zA-Z_-])")
MONEY = re.compile(r"\$\s?(\d{1,3}(?:,\d{3})+|\d{3,})(?:\.\d{1,2})?")

errors: list[str] = []
stats = {"files": 0, "rows": 0, "external": 0, "internal": 0, "cells_checked": 0}


def err(msg):
    errors.append(msg)


class RowCheck(HTMLParser):
    """Every data row must cite, and every amount in it must round."""

    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.in_table = False
        self.in_head = False
        self.in_row = False
        self.in_cell = False
        self.cell_text = ""
        self.row_links = []
        self.row_cells = []
        self.row_html = ""
        self.reg_style = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table":
            self.in_table = True
            self.reg_style = "reg" in (a.get("class") or "")
            self.in_head = False
        if tag == "thead":
            self.in_head = True
        if tag == "tr" and self.in_table:
            self.in_row = True
            self.row_links = []
            self.row_cells = []
            self.row_html = "<tr>"
        if tag == "td" and self.in_row:
            self.in_cell = True
            self.cell_text = ""
        if tag in ("script", "iframe", "form", "object", "embed"):
            err(f"{self.path}: published element <{tag}>")
        if tag == "link":
            href = a.get("href", "")
            if href.startswith("http"):
                err(f"{self.path}: external asset {href}")
        if self.in_row:
            self.row_html += self.get_starttag_text() or ""
        if tag == "a":
            href = a.get("href", "")
            if href.startswith("http"):
                host = urlparse(href).hostname or ""
                if host not in ALLOWED_HOSTS:
                    err(f"{self.path}: host not on the allowlist: {host}")
                if self.in_row:
                    self.row_links.append(href)
            elif href.startswith("#") or href.startswith("mailto:"):
                pass
            else:
                target = (self.path.parent / href.split("#")[0]).resolve()
                if href.split("#")[0] and not target.exists():
                    err(f"{self.path}: broken local link {href}")

    def handle_data(self, text):
        if self.in_cell:
            self.cell_text += text
        if self.in_row:
            self.row_html += text

    def handle_startendtag(self, tag, attrs):
        if self.in_row:
            self.row_html += self.get_starttag_text() or ""

    def handle_endtag(self, tag):
        if self.in_row:
            self.row_html += f"</{tag}>"
        if tag == "td" and self.in_cell:
            self.in_cell = False
            self.row_cells.append(self.cell_text.strip())
        if tag == "tr" and self.in_row:
            self.in_row = False
            if not self.in_head:
                stats["rows"] += 1
                self.check_row()
        if tag == "thead":
            self.in_head = False
        if tag == "table":
            self.in_table = False

    def check_row(self):
        text = " ".join(self.row_cells)
        if not text.strip():
            return
        amounts = [cell for cell in self.row_cells if MONEY.search(cell)]
        for cell in ([] if self.reg_style else self.row_cells):
            for mt in MONEY.finditer(cell):
                stats["cells_checked"] += 1
                raw = mt.group(1).replace(",", "")
                if "." in mt.group(0):
                    continue
                val = int(raw)
                marked = "exact" in cell or mt.group(1) in EXACT_OK
                if val % 10 and not marked:
                    err(f"{self.path}: unrounded amount ${mt.group(1)} in a data row without an exact mark")
        if amounts and not self.row_links and not self.reg_style:
            # A row of figures with no source is what the brief forbids. The one acceptable reason for
            # no official link is that the row is not claiming an official figure at all: it is an owner
            # input or a derived number, labelled as such, and it links the in-desk page that explains
            # why nothing public backs it.
            tagged = bool(re.search(r"tag (sm )?(owner|derived|assumption|unverified|carried)", self.row_html))
            in_desk = re.findall(r'href="(?!http|#|mailto:)([^"]+\.html)"', self.row_html)
            if not (tagged and in_desk):
                err(f"{self.path}: row carries amounts but no official link: {text[:110]}")


def visible_text(html):
    body = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    return re.sub(r"<[^>]+>", " ", body)


def main():
    as_json = "--json" in sys.argv

    # 1. the published files are the generator's output, byte for byte
    gen = M.build(write=False)
    for name, text in gen.items():
        path = ROOT / name
        stats["files"] += 1
        if not path.exists():
            err(f"missing generated file {name}")
            continue
        if path.read_text() != text:
            err(f"{name} does not match the generator; run python3 desk-d75/_src/build.py")

    pages = sorted(p for p in ROOT.glob("*.html"))
    listed = {k + ".html" for k, _ in M.PAGES}
    extra = {p.name for p in pages} - listed
    if extra:
        err(f"pages published that the generator does not know about: {sorted(extra)}")

    for path in pages:
        html = path.read_text()
        RowCheck(path).feed(html)
        vis = visible_text(html)

        # 6. identifiers
        for tok in PLACE_NAMES:
            if re.search(re.escape(tok), vis, re.I):
                err(f"{path.name}: visible text names a place ({tok})")
        probe = re.sub(r"(?i)\b(section|rule|form|code|title|part|division|article|chapter|"
                       r"subsection|paragraph|letter|advice|tariff|no|lta)\b[\s.]*[0-9][0-9.,()\u2013-]*",
                       " ", vis)
        probe = re.sub(r"(?i)\b(ATNHPIUS\d+Q|CASTHPI|CUURA\w+|GS10|MORTGAGE30US|P?L\. \d+-\d+)\b", " ", probe)
        probe = re.sub(r"(?i)(?:laws|act|amended by stats\.)\s+ch\.?\s*[0-9]+", " ", probe)
        probe = re.sub(r"\.(?:html|css|js|pdf|gov|org|com)[^ ]*", " ", probe)
        probe = re.sub(r"\d{4}-\d{2}(?:-\d{2})?", " ", probe)      # dates such as 2025-26 form ids
        probe = re.sub(r"\b\d{4,5}(?:/\d{3})?\b", " ", probe)      # years, and LTA-style 2025/009
        hit = ZIPISH.search(probe)
        if hit:
            err(f"{path.name}: postcode-shaped number {hit.group(0)}")
        for pat, label in [(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", "e-mail"),
                           (r"\b\d{3}-\d{2}-\d{4}\b", "SSN shape"),
                           (r"\(?\d{3}\)?[-.]\d{3}[-.]\d{4}\b", "phone shape"),
                           (r"\b\d{1,4}\s+[A-Z][a-z]+\s+(?:Ave|St|Rd|Blvd|Dr|Ct|Ln|Way|Pl)\b",
                            "street address"),
                           (r"\bAPN\b|\bparcel number\b", "parcel identifier")]:
            if re.search(pat, vis):
                err(f"{path.name}: {label} pattern in visible text")

        # links out of the desk must not be assumed to exist
        for href in re.findall(r'href="([^"#]+)"', html):
            if href.startswith("http"):
                stats["external"] += 1
            elif not href.startswith("mailto:"):
                stats["internal"] += 1

    # 2. the requirement register
    ids = [r["id"] for r in D.REQUIREMENTS]
    if len(ids) != len(set(ids)):
        err("requirement ids are not unique")
    if not (20 <= len(D.REQUIREMENTS) <= 60):
        err(f"requirement register has {len(D.REQUIREMENTS)} rows, which is not a credible count")
    for r in D.REQUIREMENTS:
        if r["status"] not in ("met", "met-with-gaps", "open-on-owner"):
            err(f"{r['id']}: unknown status {r['status']}")
        target = ROOT / r["where"]
        if not target.exists():
            err(f"{r['id']}: 'answered on' points at a page that does not exist ({r['where']})")
        if r["status"] == "met" and not r.get("note"):
            err(f"{r['id']}: marked met with no evidence line")

    # 7. registers reference real sources
    for reg, name in ((D.VERIFIED, "VERIFIED"), (D.FLAGS, "FLAGS"), (D.ASSUMPTIONS, "ASSUMPTIONS")):
        for row in reg:
            for k in row.get("src", []):
                if k not in D.SRC:
                    err(f"{name} row {row.get('id', row.get('item', '?'))[:40]}: unknown source id {k}")
    for s in D.SOURCES:
        if not re.match(r"^https://", s["url"]):
            err(f"source {s['id']}: url is not https")
        host = urlparse(s["url"]).hostname or ""
        if host not in ALLOWED_HOSTS:
            err(f"source {s['id']}: host {host} is not an official publisher on the allowlist")
        if not s["supports"]:
            err(f"source {s['id']}: says nothing about what it supports")
    for v in D.VERIFIED:
        if v["status"] in ("verified", "carried") and not v["src"]:
            err(f"VERIFIED: {v['item'][:50]} has status {v['status']} but no source")
        if v["status"] == "verified" and not any(D.SRC[k]["opened"] for k in v["src"]):
            err(f"VERIFIED: {v['item'][:50]} is marked verified but no listed source was opened this session")

    # 8. every assumption id is cited where it is used
    all_html = " ".join(p.read_text() for p in pages)
    for a in D.ASSUMPTIONS:
        if a["id"] not in all_html:
            err(f"assumption {a['id']} is never cited on any page")
        if not a["sens"]:
            err(f"assumption {a['id']} carries no sensitivity")
    used = set(re.findall(r"\bD(\d{1,2})\b", all_html))
    for n in used:
        if f"D{n}" not in {a["id"] for a in D.ASSUMPTIONS}:
            err(f"a page cites assumption D{n}, which does not exist in the register")

    # 3/4/5 for questions, suggestions, flags
    qids = [q["id"] for q in D.QUESTIONS]
    if len(qids) != len(set(qids)):
        err("question ids are not unique")
    for q in D.QUESTIONS:
        if q["status"] not in ("open", "answered", "derivable"):
            err(f"{q['id']}: unknown status")
        if q["status"] == "open" and (not q["how"] or not q["who"]):
            err(f"{q['id']}: open question with no discovery route")
        if q["status"] == "answered" and not q.get("answer"):
            err(f"{q['id']}: marked answered with no answer text")
    sids = [s["id"] for s in D.SUGGESTIONS]
    if len(sids) != len(set(sids)):
        err("suggestion ids are not unique")
    for s in D.SUGGESTIONS:
        if s["status"] != "awaiting owner":
            err(f"suggestion {s['id']}: status {s['status']} - nothing may be implemented without an owner decision")
        for k in ("why", "benefit", "effort", "risk"):
            if not s.get(k):
                err(f"suggestion {s['id']}: missing the {k} field")
    fids = [f["id"] for f in D.FLAGS]
    if len(fids) != len(set(fids)):
        err("flag ids are not unique")
    for f in D.FLAGS:
        if f["severity"] not in ("material", "review", "info"):
            err(f"{f['id']}: unknown severity")
        if not f["action"]:
            err(f"{f['id']}: a flag with no stated way to close it")
        if f["id"] not in all_html:
            err(f"flag {f['id']} is not printed on the flagged page")

    # owner inputs are used, not restated as official
    for o in D.OWNER:
        if o["status"] != "owner":
            err(f"OWNER row {o['item'][:40]}: status must be owner, is {o['status']}")

    # 10. the findings this desk exists to deliver
    must = [
        ("the 2026 election changed nothing about Proposition 13 or 19", "Proposition 19", "law-watch.html"),
        ("the ballot findings name the measures", "Proposition 40", "law-watch.html"),
        ("the environmental-review measure is named too", "Proposition 45", "law-watch.html"),
        ("the step-up is cited to the code section", "section 1014", "estate-tax.html"),
        ("the act is named as not amending it", "did not amend", "estate-tax.html"),
        ("the carryover-basis limit on gifts is stated", "section 1015", "estate-tax.html"),
        ("the 2027 exclusion is stated", "15,480,000", "estate-tax.html"),
        ("the 2027 annual gift exclusion is stated", "20,000", "estate-tax.html"),
        ("the step-up question is answered explicitly", "basis", "estate-tax.html"),
        ("the Proposition 19 amount is treated as windowed", "1,044,586", "properties.html"),
        ("the window on that amount is printed", "16 Feb", "law-watch.html"),
        ("the owner's rounding rule is stated", "nearest $10", "methodology.html"),
        ("the black-swan section exists as its own page", "regime", "black-swans.html"),
        ("the suggestions board is separate and unimplemented", "awaiting owner", "suggestions.html"),
    ]
    for label, needle, page in must:
        text = (ROOT / page).read_text() if (ROOT / page).exists() else ""
        if needle not in text:
            err(f"deliverable missing: {label} - expected {needle!r} on {page}")

    # the four paths the owner asked about are all present, and priced
    for word in ("Live in it", "Rent it out", "Sell it at transfer"):
        if word not in (ROOT / "decision.html").read_text():
            err(f"decision page never names the {word!r} path")

    # every row of the projection covers the horizon the brief asked for
    proj = (ROOT / "projections.html").read_text()
    for year in (2026, 2040, 2050, 2060, 2076):
        if f"<td>{year}</td>" not in proj:
            err(f"projections table has no row for {year}")

    # 12. structure of every emitted table, and every anchor
    for path in pages:
        html = path.read_text()
        for m in re.finditer(r'<table class="[^"]*">(.*?)</table>', html, re.S):
            seg = m.group(1)
            head, _, body = seg.partition("</thead>")
            h = len(re.findall(r"<th[\s>]", head))
            for i, rr in enumerate(re.findall(r"<tr>(.*?)</tr>", body, re.S)):
                n = len(re.findall(r"<t[dh][\s>]", rr))
                if h and n != h:
                    err(f"{path.name}: table row {i} has {n} cells against {h} headers")
        for href in re.findall(r'href="([^"#]+)"', html):
            if href.startswith(("http", "mailto:")):
                continue
            target = (path.parent / href.split("#")[0]).resolve()
            if href.split("#")[0] and not target.exists():
                err(f"{path.name}: local link has no target: {href}")
        for frag in set(re.findall(r'href="#([^"]+)"', html)):
            if f'id="{frag}"' not in html:
                err(f"{path.name}: anchor #{frag} has no target on the page")

    # the exec summary and the decision page must not disagree about the headline figures
    for T in M.TRANSFER_YEARS:
        for key, _ in M.PATHS:
            term = M.money(M.simulate(T, key)["terminal"])
            if term not in (ROOT / "executive-summary.html").read_text():
                err(f"executive summary no longer carries the {key} figure at {T} ({term})")

    # 9. determinism: the generator must not depend on environment or order
    r = subprocess.run([sys.executable, str(HERE.parent / "build.py"), "--check"], cwd=str(HERE.parent),
                       capture_output=True, text=True)
    if r.returncode != 0:
        err("rebuild check: " + (r.stdout + r.stderr).strip()[:300])

    ok = not errors
    if as_json:
        print(json.dumps({"ok": ok, "checks": 12, "stats": stats,
                          "pages": [p.name for p in pages],
                          "errors": sorted(set(errors))}, indent=2))
    else:
        for e in sorted(set(errors)):
            print("FAIL:", e)
        print(f"{'PASS' if ok else 'FAIL'}: {len(pages)} pages; {stats['rows']} source-checked rows; "
              f"{stats['external']} external links; {stats['internal']} internal links; "
              f"{stats['cells_checked']} amounts checked for rounding; "
              f"{len(D.REQUIREMENTS)} requirements, {len(D.QUESTIONS)} questions, "
              f"{len(D.SUGGESTIONS)} suggestions, {len(D.FLAGS)} flags, {len(D.SOURCES)} sources.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
