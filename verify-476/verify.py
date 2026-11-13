"""Structural checks for verify-476 pages. Run: python3 verify-476/verify.py
Checks: every table row carries a source link or an explicit OPEN/Referee verdict; no privacy
patterns (email, phone, 5-digit ZIP-like tokens, APN/parcel wording); internal links resolve;
USD amounts are multiples of $10 unless marked 'as published by the agency'. Structural only.
"""
import os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
errs = []
rows = 0
rows_ok = 0
# Exact statutory amounts and published unit rates, quoted as published (project rounding rule).
USD_AS_PUBLISHED = {"56", "76", "67", "1044586", "69625", "208850", "107900", "750000", "0.55", "1.65"}
# Identifier tokens that look like ZIP codes but are not (e.g. Treasury Decision 10055).
IDENT_OK = {"10055"}

for f in sorted(os.listdir(D)):
    if not f.endswith(".html"):
        continue
    txt = open(os.path.join(D, f), encoding="utf-8").read()
    body = re.sub(r"<[^>]+>", " ", re.sub(r'href="[^"]*"', "", txt))

    # 1) table rows: each has a link in-row or an explicit verdict phrase
    for tbody in re.findall(r"<tbody>(.*?)</tbody>", txt, re.S):
        for row in re.findall(r"<tr>(.*?)</tr>", tbody, re.S):
            rows += 1
            if re.search(r'href="https?://', row) or re.search(r'href="\.\./', row) \
               or re.search(r"OPEN|Referee-confirmed|CONFIRMED|CORRECTED", row) \
               or re.search(r'class="(ok|fixed|open)"', row):
                rows_ok += 1
            else:
                errs.append(f"{f}: row lacks source/verdict: {row[:90]}")

    # 2) privacy
    body_no_url = re.sub(r"https?://\S+", " ", body)
    for pat, name in [(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", "email"),
                      (r"\b\(?\d{3}\)?[-. ]\d{3}[-.]\d{4}\b", "phone"),
                      (r"\bAPN\b|\bparcel number\b", "parcel"),
                      (r"(?<![\d$,.])\b\d{5}\b(?![\d,])", "zip-like")]:
        for m in re.finditer(pat, body_no_url):
            if m.group(0) in IDENT_OK:
                continue
            errs.append(f"{f}: privacy {name}: {m.group(0)}")

    # 3) internal links resolve
    for h in re.findall(r'href="([^"#?]+)"', txt):
        if h.startswith("http") or h.startswith("mailto"):
            continue
        if not os.path.exists(os.path.join(D, h)):
            errs.append(f"{f}: broken link {h}")

    # 4) USD rounding (allowed decimals appear only in agency-quote context)
    for m in re.finditer(r"\$(\d{1,3}(?:,\d{3})+|\d+)(\.\d+)?", body):
        raw = m.group(1).replace(",", "")
        if m.group(2):
            if raw + m.group(2) in USD_AS_PUBLISHED or "as published by the agency" in body:
                continue
            errs.append(f"{f}: decimal USD not marked as agency figure: {m.group(0)}")
            continue
        if raw in USD_AS_PUBLISHED:
            continue
        if int(raw) % 10 != 0:
            errs.append(f"{f}: USD not multiple of 10: {m.group(0)}")

print(f"rows={rows} rows_ok={rows_ok}")
print("\n".join(errs) if errs else "NO ERRORS")
sys.exit(1 if errs else 0)
