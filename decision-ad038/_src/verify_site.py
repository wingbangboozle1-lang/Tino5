"""Structural checks for decision-ad038 pages: every table row has a source (link, flag, or source ID), money is a multiple of $10 (published unit rates excepted), internal links resolve, and no personal-identifier pattern appears. Run: python3 verify_site.py (from this folder). Structural only; it does not prove that a cited page says what the row claims."""
import re, os, sys
from html.parser import HTMLParser
D = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
pages = [f for f in os.listdir(D) if f.endswith(".html")]
errs = []; stats = dict(rows=0, rows_ok=0, money=0, links=0)
UNIT_OK = {"78.64", "13.13", "2.13"}  # published unit rates (not rounded; labelled in text)

class P(HTMLParser):
    def __init__(s, name):
        super().__init__(); s.name = name; s.in_tbody = False; s.row = None; s.intable = False
        s.hrefs = []
    def handle_starttag(s, tag, a):
        a = dict(a)
        if tag == "table": s.intable = True
        if tag == "tbody": s.in_tbody = True
        if tag == "tr" and s.in_tbody: s.row = {"cells": 0, "src": 0}
        if tag == "td" and s.row is not None: s.row["cells"] += 1
        if tag == "a" and "href" in a:
            s.hrefs.append(a["href"])
            if a["href"].startswith("http"): stats["links"] += 1
        if tag == "span" and "flag" in a.get("class", "") and s.row is not None: s.row["src"] += 0
    def handle_endtag(s, tag):
        if tag == "tbody": s.in_tbody = False
        if tag == "tr" and s.row is not None:
            stats["rows"] += 1
            if s.row["cells"] == 0: errs.append(f"{s.name}: empty row")
            s.row = None
    def handle_data(s, d): pass

for f in pages:
    txt = open(os.path.join(D, f), encoding="utf-8").read()
    # 1) every tbody row has a source link or a flagged source span
    for tr in re.findall(r"<tbody>(.*?)</tbody>", txt, re.S):
        for row in re.findall(r"<tr>(.*?)</tr>", tr, re.S):
            stats["rows"] += 1
            cells = re.findall(r"<td>(.*?)</td>", row, re.S)
            srcc = " ".join(cells[-1:]) if cells else ""
            if re.search(r'href="https?://', row): srcc = row
            if re.search(r"href=\"https?://", srcc) or 'class="flag"' in srcc or re.search(r"\bS\d\d\b|MODEL|OWNER", srcc):
                stats["rows_ok"] += 1
            else:
                errs.append(f"{f}: row lacks source: {cells[-1][:80] if cells else row[:80]}")
    # 2) money multiples of 10
    body = re.sub(r"<[^>]+>", " ", re.sub(r'href="[^"]*"', "", txt))
    for m_ in re.finditer(r"\$(\d{1,3}(?:,\d{3})+|\d+)(\.\d+)?", body):
        stats["money"] += 1
        raw = m_.group(1).replace(",", "")
        if m_.group(2): 
            if raw + m_.group(2) not in UNIT_OK and raw not in UNIT_OK:
                errs.append(f"{f}: decimal money ${raw}{m_.group(2)}")
            continue
        if int(raw) % 10 != 0:
            errs.append(f"{f}: money not multiple of 10: ${raw}")
    # 3) internal links resolve
    for h in re.findall(r'href="([^"#?]+)"', txt):
        if h.startswith("http") or h.startswith("mailto"): continue
        if not os.path.exists(os.path.join(D, h)): errs.append(f"{f}: broken link {h}")
    # 4) privacy patterns
    body = re.sub(r"https?://\S+", " ", body)
    for pat, name in [(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", "email"), (r"\b\(?\d{3}\)?[-. ]\d{3}[-.]\d{4}\b", "phone"),
                      (r"\bAPN\b|\bparcel number\b", "parcel"), (r"(?<![\d$,.])\b\d{5}\b(?![\d,])", "zip-like")]:
        for mm in re.finditer(pat, body):
            errs.append(f"{f}: privacy {name}: {mm.group(0)}")
    if "<script" in txt or "<iframe" in txt: errs.append(f"{f}: forbidden element")
print(stats)
print("\n".join(errs) if errs else "NO ERRORS")
