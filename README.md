# Inheritance decision dashboard — Cupertino (95014) & San Francisco (94122)

A source-linked decision analysis for a house expected to pass by trust around 2040–2050, alongside an
already-owned, part-rented San Francisco building that stays in place either way.

**Live site:** https://wingbangboozle1-lang.github.io/Tino5/

## What the site answers

| Question | Page |
|---|---|
| What is the best plan, and why? | `pages/executive-summary.html` |
| Should I live in it, rent it, or sell and reinvest? | `pages/scenarios.html` |
| What will it be worth, and what will the tax be, year by year? | `pages/projections.html` |
| How does Proposition 19 change the cost? | `pages/property-tax.html` |
| How much can be inherited before a tax applies? | `pages/inheritance-tax.html` |
| What does the transfer actually involve, step by step? | `pages/inheritance-process.html` |
| What will insurance, water, power and repairs cost? | `pages/operating-costs.html` |
| What is changing in the law? | `pages/law-watch.html` |
| What is unverified or inconsistent? | `pages/flagged.html` |
| How were the numbers produced? | `pages/methodology.html` |
| Audited Interactive Briefing (Charts, 2027 IRS / LTA 26-026, Liquid Estate Matrix) | `audited-v4/index.html` |

## Privacy

No personal data is stored in this repository or served on the site. The properties are referred to only as
**Property A** (95014) and **Property B** (94122). No names, street addresses, parcel numbers, account
numbers, emails or phone numbers appear anywhere — `scripts/verify.mjs` scans for those patterns on every run.
Anything identified during research that could identify a person is kept out of the repository entirely.

## Verification model

Every table row carries one of six statuses:

- **verified** — read from an official source (statute, agency, utility tariff), linked in the row
- **secondary** — credible non-official reporting, or an official value whose page could not be retrieved here
- **owner-provided** — supplied by the owner on 10 Nov 2026, not independently confirmed
- **derived** — arithmetic on the above, with the arithmetic shown in the note
- **assumption** — a named model parameter (A1–A29) with a sensitivity
- **unverified** — not confirmable; the value is left blank and listed on the Flagged for Review page

Nothing is inferred or filled in. Money in the analysis is rounded to the nearest $10; statutory constants are
quoted exactly as published.

## Repository layout

```
index.html                  dashboard
pages/*.html                built pages (generated — do not edit by hand)
src/pages/*.html            page bodies; the build wraps them in the shared shell
assets/style.css, app.js    styling and the data-driven renderer (no dependencies)
data/sources.json           source registry (publisher, document, URL, how verified)
data/*.json                 verified / flagged data tables
data/model.json             model output (generated)
scripts/model.py            the financial model — one named parameter per assumption
scripts/build_site.py       builds pages/*.html from src/pages/*.html
scripts/verify.mjs          verification and link checker
verification-report.json    last verification run
COORDINATION.md             shared task board for parallel agent sessions
session-2f7b1b3f/           standalone 7-page interactive dashboard & simulator (session arena-2f7b1b3f)
```

## Rebuild

```bash
python3 scripts/model.py       # recompute data/model.json
python3 scripts/build_site.py  # rebuild pages/*.html
node scripts/verify.mjs        # verify rows, sources, links, rounding, PII patterns
```

No build tooling, no external CDNs, no npm dependencies. The site is plain HTML, CSS and JavaScript served
directly by GitHub Pages.

## Disclaimer

Decision support only — not legal, tax or investment advice. Trust drafting, titling, insurance and condition
are unknown and each can change the answer; see the flagged list before acting.

## Parallel Session Interactive Simulator (`session-2f7b1b3f/`)

Session `arena-2f7b1b3f` contributed a standalone 7-page interactive simulator and verified regulatory compendium under `session-2f7b1b3f/index.html`, preserved alongside the combined dashboard (`index.html`), `/archive/`, and `/mine/pages/`. Reproduce its dataset with:

```bash
python3 session-2f7b1b3f/scripts/generate_data.py
```
