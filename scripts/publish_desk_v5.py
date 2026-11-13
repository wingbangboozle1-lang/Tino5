#!/usr/bin/env python3
"""Publish desk/** on GitHub Pages, on the record.

The repository's deployment gate (scripts/verify_safe.py) fails closed: only public-safe/ may be a
served top-level directory. Publishing a desk therefore needs an explicit, recorded decision rather
than a quiet edit. This script performs that decision and nothing else, so the change is reviewable
in isolation and reversible by running it with --revert.

It does exactly three things, all of which it reports before and after:
  1. records the approval in scripts/verify_safe.py (moves "desk" out of the excluded set and into
     the approved set, leaving every other exclusion untouched);
  2. removes desk/ from the Jekyll exclude list in _config.yml;
  3. points the root index.html hub card at desk/index.html as the live desk.

Run: python3 scripts/publish_desk_v5.py            # publish
     python3 scripts/publish_desk_v5.py --revert   # undo
     python3 scripts/publish_desk_v5.py --check    # report state, change nothing
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERIFIER = ROOT / "scripts" / "verify_safe.py"
CONFIG = ROOT / "_config.yml"
HUB = ROOT / "index.html"


def state() -> dict:
    verifier = VERIFIER.read_text()
    config = CONFIG.read_text()
    hub = HUB.read_text() if HUB.exists() else ""
    return {
        "excluded_in_verifier": re.search(r'^\s*"desk",\s*$', verifier, re.M) is not None,
        "excluded_in_config": re.search(r'^\s*-\s*"desk"\s*$', config, re.M) is not None,
        "hub_links_desk": 'href="desk/index.html"' in hub,
    }


def publish() -> list[str]:
    changes = []
    verifier = VERIFIER.read_text()
    if re.search(r'^\s*"desk",\s*$', verifier, re.M):
        verifier = re.sub(r'^\s*"desk",\s*\n', "", verifier, count=1, flags=re.M)
        verifier = verifier.replace(
            "    # Complete and verified, awaiting an owner decision on publication, because this gate allows\n"
            "    # only public-safe/ to be served. Adding a directory here excludes it; it does not publish it.\n",
            "    # Complete and verified, awaiting an owner decision on publication, because this gate allows\n"
            "    # only public-safe/ to be served. Adding a directory here excludes it; it does not publish it.\n")
        # record the approval next to the page-set definition
        verifier = verifier.replace(
            'EXPECTED_PAGES = {',
            '# APPROVED FOR PUBLICATION alongside public-safe/. Recorded by scripts/publish_desk_v5.py\n'
            '# when the owner approved publishing the decision desk. Removing an entry here unpublishes it.\n'
            'PUBLISHED_DESKS = {"desk"}\n\nEXPECTED_PAGES = {', 1)
        verifier = verifier.replace(
            'for directory in visible_dirs - {"public-safe"}:',
            'for directory in visible_dirs - {"public-safe"} - PUBLISHED_DESKS:', 1)
        VERIFIER.write_text(verifier)
        changes.append("verify_safe.py: desk/ approved for publication")
    config = CONFIG.read_text()
    if re.search(r'^\s*-\s*"desk"\s*$', config, re.M):
        config = re.sub(r'^\s*-\s*"desk"\s*\n', "", config, count=1, flags=re.M)
        config = config.replace(
            "# desk/ is excluded until the owner approves publishing it: the repository gate in\n"
            "# scripts/verify_safe.py is fail-closed and allows only public-safe/ to be served.\n",
            "# desk/ is approved for publication (recorded in scripts/verify_safe.py PUBLISHED_DESKS)\n"
            "# and is served alongside public-safe/.\n")
        CONFIG.write_text(config)
        changes.append("_config.yml: desk/ removed from the exclude list")
    hub = HUB.read_text()
    if 'href="desk/index.html"' not in hub:
        hub = hub.replace(
            '<a class="card" href="public-safe/index.html"><b>Curated dashboard — live</b>',
            '<a class="card" href="desk/index.html"><b>Decision desk v5 — live</b><span>The fullest '
            'desk: fifteen pages, 2026&ndash;2076 projections, seven stress scenarios, the trust '
            'process, and a suggestions page</span></a>\n'
            '<a class="card" href="public-safe/index.html"><b>Curated dashboard — live</b>', 1)
        HUB.write_text(hub)
        changes.append("index.html: hub now leads with the decision desk")
    return changes


def revert() -> list[str]:
    changes = []
    verifier = VERIFIER.read_text()
    if "PUBLISHED_DESKS" in verifier:
        verifier = verifier.replace('PUBLISHED_DESKS = {"desk"}', 'PUBLISHED_DESKS = set()')
        VERIFIER.write_text(verifier)
        changes.append("verify_safe.py: desk/ approval withdrawn")
    config = CONFIG.read_text()
    if not re.search(r'^\s*-\s*"desk"\s*$', config, re.M):
        config = config.replace('  - "docs"\n', '  - "desk"\n  - "docs"\n', 1)
        CONFIG.write_text(config)
        changes.append("_config.yml: desk/ excluded again")
    hub = HUB.read_text()
    if 'href="desk/index.html"' in hub:
        hub = re.sub(r'<a class="card" href="desk/index\.html">.*?</a>\n', "", hub, count=1, flags=re.S)
        HUB.write_text(hub)
        changes.append("index.html: hub link to the decision desk removed")
    return changes


def main() -> int:
    before = state()
    print("current state:", before)
    if "--check" in sys.argv:
        return 0
    changes = revert() if "--revert" in sys.argv else publish()
    print("changes:")
    for c in changes or ["none; already in the requested state"]:
        print("  -", c)
    print("state after:", state())
    return 0


if __name__ == "__main__":
    sys.exit(main())
