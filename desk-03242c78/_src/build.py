# -*- coding: utf-8 -*-
"""Entry point. Builds every page of desk-03242c78 and a manifest for verification."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import common  # noqa: E402
import p1_start, p2_props, p3_tax, p4_paths, p4b_whatif, p5_plan, p6_review  # noqa: E402

X = common.expose()

for mod in (p1_start, p2_props, p3_tax, p4_paths, p4b_whatif, p5_plan, p6_review):
    mod.build(X)

have = sorted(f for f in os.listdir(os.path.dirname(HERE)) if f.endswith(".html"))
want = [h for h, _ in common.ALL_PAGES]
missing = [w for w in want if w not in have]
extra = [h for h in have if h not in want]
print("pages built: %d" % len(want))
if missing:
    print("MISSING: %s" % ", ".join(missing))
if extra:
    print("NOT IN NAV: %s" % ", ".join(extra))

manifest = dict(
    desk="desk-03242c78",
    built=common.BUILT,
    pages=[dict(href=h, title=t) for h, t in common.ALL_PAGES],
    sources=[s["id"] for s in common.S.SOURCES],
    statutory_literals=sorted(common.S.STATUTORY_LITERALS),
)
with open(os.path.join(HERE, "manifest.json"), "w") as fh:
    json.dump(manifest, fh, indent=1)
if missing:
    raise SystemExit(1)
