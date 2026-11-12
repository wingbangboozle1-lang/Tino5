#!/usr/bin/env python3
"""Re-run the 552/V checks: structural gate, privacy, model arithmetic.

Usage: python3 verify-552/verify.py
Exit 0 = PASS, exit 1 = FAIL (prints reasons).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import desk_model as m  # noqa: E402

errors = []

def run(cmd):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()

# 1. verify_safe
rc, out = run(["python3", "scripts/verify_safe.py"])
print(out)
if rc != 0:
    errors.append("verify_safe failed")

# 2. privacy_scan whole repo + verify-552
rc, out = run(["python3", "scripts/privacy_scan.py"])
print(out)
if rc != 0:
    errors.append("privacy_scan failed")

# 3. model arithmetic spot checks
def expect(label, got, want):
    g, w = m.money(got), m.money(want)
    ok = (g == w)
    print(f"{'OK ' if ok else 'FAIL'} {label}: published {w} recomputed {g}")
    if not ok:
        errors.append(label)

t = m.transfer_year_view(2045)
expect("2045 FMV", t["fmv"], 6531230)
expect("2045 tax occupy", t["tax_occupy"], 62530)
expect("2045 tax rent", t["tax_rent"], 81640)
expect("2045 rent", t["rent"], 115730)
expect("2045 net rent", t["net_rent"], -7040)
expect("2045 proceeds", t["proceeds"], 6139360)
w = m.wealth(2045)
expect("2070 occupy", w["s1"], 7580540)
expect("2070 rent", w["s2"], 12885140)
expect("2070 sell", w["s3"], 18451440)
expect("B NOI 2026", m.property_b_view(2026)["noi"], 53430)
expect("estate 2045", m.estate_threshold(2045), 23979750)
# BOE worked example
assert m.prop19_taxable(1500000, 300000, 1000000) == 500000, "Prop19 example"
print("OK  Prop19 BOE example: 500000")
# B tax raw -> rounded
assert m.money(206000 * 0.0118162182) == "$2,430", "B tax"
print("OK  B tax 2026: $2,430")
assert m.money(550000 * 0.0125) == "$6,880", "A tax"
print("OK  A tax 2026: $6,880")

# 4. verify-552 files: no PII patterns, money rounds to $10 (statutory exempt)
PII = [
    (r"[\w.+-]+@[\w-]+\.[a-z]{2,}", "e-mail"),
    (r"\b\d{3}-\d{2}-\d{4}\b", "SSN shape"),
    (r"\b\d{5}(?:-\d{4})?\b", "ZIP shape"),
    (r"\bCupertino\b|\bSan Jose\b|\bPalo Alto\b|\bOuter Sunset\b", "city identifier"),
]
MONEY = re.compile(r"\$(\d{1,3}(?:,\d{3})+|\d+)(?![\d.,])")
for p in sorted((ROOT / "verify-552").glob("*")):
    if p.is_dir() or p.suffix not in (".md", ".html") or p.name == "verify.py":
        continue
    text = p.read_text()
    visible = re.sub(r"https?://\S+", "", text)
    visible = re.sub(r"arena-[0-9a-f]+", "", visible)
    visible = visible.replace("11911", "").replace("1947.12", "")  # statute numbers, not ZIPs
    for pat, label in PII:
        if re.search(pat, visible, re.I):
            errors.append(f"{p.name}: {label} pattern")
    stripped = re.sub(r"\$1,044,586|\$1,022,600|\$15,000,000|\$1,571|\$1,512|\$184,500", "", text)
    for amt in MONEY.finditer(stripped):
        if int(amt.group(1).replace(",", "")) % 10:
            errors.append(f"{p.name}: unrounded money ${amt.group(1)}")

if errors:
    print("\nFAIL:")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)
print("\nPASS: 552/V checks (verify_safe, privacy_scan, model arithmetic, register privacy).")
