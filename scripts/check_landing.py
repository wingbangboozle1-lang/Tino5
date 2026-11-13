"""Fail if a link on the root landing page does not resolve.

The fail-closed rule keeps unpublished desks out of the published site, so the landing
page must only point at paths that exist. Run: python3 scripts/check_landing.py
"""
import re
import sys
from pathlib import Path

HTML = Path("index.html").read_text()
targets = re.findall(r'(?:href|src)="([^"#]+)"', HTML)
bad = [t for t in targets if not t.startswith("http") and not Path(t).exists()]
print(f"landing page: {len(targets)} targets, {len(bad)} unresolved")
for t in bad:
    print("  unresolved:", t)
sys.exit(1 if bad else 0)
