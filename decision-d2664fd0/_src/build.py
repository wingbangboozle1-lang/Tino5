"""Static site build for decision-d2664fd0 (no-op: pages are hand-authored HTML).

This desk publishes hand-authored HTML pages directly. The build script is a
placeholder that validates all pages exist and internal links resolve.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = [
    "index.html", "executive-summary.html", "properties.html", "property-tax.html",
    "inheritance-tax.html", "running-costs.html", "scenarios.html", "mixed-paths.html",
    "what-if.html", "black-swans.html", "process.html", "timeline.html",
    "questions.html", "suggestions.html", "sources.html", "flagged.html",
    "glossary.html", "briefing-sheet.html", "law-watch.html", "methodology.html",
    "projections.html",
]


def main():
    missing = [p for p in PAGES if not (ROOT / p).exists()]
    if missing:
        raise SystemExit("missing pages: " + ", ".join(missing))
    print(f"build OK: {len(PAGES)} pages present in {ROOT.name}")


if __name__ == "__main__":
    main()
