#!/usr/bin/env python3
"""Find candidate unrounded monetary amounts in tracked public HTML.

This is a triage check, not a privacy proof. It deliberately prints paths and
counts only. Statutory amounts and prices from government sources are possible
false positives; identifying combinations and non-dollar data are not detected.
"""
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')
pattern = re.compile(r'\$\s*(\d{1,3}(?:,\d{3})+|\d{3,})(?![\d.,])')
findings = []
for name in paths:
    if not name.endswith('.html'):
        continue
    path = root / name
    if not path.is_file():
        continue
    text = path.read_text(encoding='utf-8')
    count = sum(int(m.group(1).replace(',', '')) % 10 != 0 for m in pattern.finditer(text))
    if count:
        findings.append((name, count))
for name, count in findings:
    print(f'{name}: {count} candidate(s)')
print(f'{len(findings)} HTML file(s) need review; matches are not necessarily personal data.')
print('Not scanned: non-HTML assets, history, context, and non-currency identifiers.')
sys.exit(1 if findings else 0)
