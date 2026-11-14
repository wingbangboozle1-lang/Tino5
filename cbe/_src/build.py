# -*- coding: utf-8 -*-
"""Build the owner-brief desk: write every page as static HTML into cbe/.

Run from anywhere:  python3 cbe/_src/build.py

The published artifact is static HTML and CSS only. There is no JavaScript, no external
font, image or style reference, no form and no analytics. verify.py enforces that, and
build.py runs it before reporting success.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import shell as sh              # noqa: E402
import pages_core as pc         # noqa: E402
import pages_extra as pe        # noqa: E402

# (filename, nav label, page function)
BUILD = [
    ("index.html", pc.page_index),
    ("executive-summary.html", pc.page_executive_summary),
    ("properties.html", pc.page_properties),
    ("property-tax.html", pc.page_property_tax),
    ("inheritance-tax.html", pc.page_inheritance_tax),
    ("running-costs.html", pc.page_running_costs),
    ("projections.html", pc.page_projections),
    ("options.html", pc.page_options),
    ("black-swan.html", pe.page_black_swan),
    ("process.html", pe.page_process),
    ("questions.html", pe.page_questions),
    ("suggestions.html", pe.page_suggestions),
    ("law-watch.html", pe.page_law_watch),
    ("repo-review.html", pe.page_repo_review),
    ("sources.html", pe.page_sources),
    ("flagged.html", pe.page_flagged),
    ("methodology.html", pe.page_methodology),
]


def check_names():
    """Every page in shell.PAGES must be built, and nothing else."""
    declared = [fn for fn, _, _ in sh.PAGES]
    built = [fn for fn, _ in BUILD]
    missing = [fn for fn in declared if fn not in built]
    extra = [fn for fn in built if fn not in declared]
    if missing or extra:
        raise SystemExit("navigation mismatch: missing=%s extra=%s" % (missing, extra))
    if len(set(built)) != len(built):
        raise SystemExit("duplicate filenames in BUILD")


def main():
    check_names()
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    written = []
    for fn, fn_page in BUILD:
        title, body = fn_page()
        html = sh.page(title, fn, body)
        path = os.path.join(OUT, fn)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        written.append((fn, len(html)))
    for fn, n in written:
        print("  wrote %-26s %7d bytes" % (fn, n))
    print("%d pages written to %s" % (len(written), OUT))

    import verify
    ok = verify.main(quiet=True)
    if not ok:
        raise SystemExit(1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
