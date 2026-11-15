# Estate decision desk

A source-linked decision aid for comparing what to do with **Property A**, a future trust inheritance, while taking account of **Property B**, which is already owned. Property B is not treated as part of the inheritance. No path is a recommendation until the missing values and legal facts are verified.

## Live site

**Start:** [Estate decision desk](https://wingbangboozle1-lang.github.io/Tino5/)

The Pages publication is intentionally small and has one primary decision model:

- [`cbe/`](cbe/index.html) — the main desk: executive summary, property facts, property tax, inheritance and estate tax, carrying costs, year-by-year projections, pure and mixed paths, black-swan regimes, trust process, questions, suggestions, law watch, sources, flags and glossary.
- [`phase-99220/`](phase-99220/index.html) — what-if controls, mixed paths and a separate historical 1929/2008 crash-entry replay for Treasury parking and phased stock investment; includes a deadline timeline and printable attorney/CPA brief.
- [`public-safe/`](public-safe/index.html) — a rules-and-source reference without household figures.

The other decision-desk generations remain in the repository for audit, but are excluded from GitHub Pages so a visitor is not asked to choose between duplicate or inconsistent dashboards. The root page leads with what would change the answer and where the evidence is missing.

## Privacy — an important limitation

The published Pages surface uses generic Property A / Property B labels, has no city or neighbourhood names, street, postal, parcel or account identifiers, and is checked for common name, address and contact patterns. Broad county-level jurisdiction references may remain where needed for legal context. The root and main desk use `noindex`; `robots.txt` asks crawlers not to fetch the site. These are crawler directives, not access controls. The **GitHub repository itself is public**. Earlier commits and excluded working trees still retain previously exposed household/location material. Removing or excluding a directory from Pages does not erase it from GitHub or from repository history. A shared-history rewrite was not performed in this branch; therefore the repository is **not scrubbed** and this must remain a flagged issue until a coordinated repository-wide remediation is completed. Do not treat the website’s privacy scan as proof that the public Git history is private.

## Evidence and limits

Official-source links accompany the decision tables, and each desk distinguishes verified rules from owner-supplied inputs, assumptions, derived values and unknowns. Unknown values are left blank or expressed as a break-even threshold. Dollar model figures are rounded to the nearest $10; statutory amounts are quoted as published where rounding would change a legal threshold. Rounded figures are not a guarantee of anonymity. The model is not tax, legal or investment advice and cannot forecast 2040–2050 law, rent, insurance prices, house prices, inflation or market returns.

## Rebuild and verify

```bash
python3 scripts/verify_safe.py
python3 scripts/check_landing.py
python3 cbe/_src/build.py
python3 cbe/_src/verify.py
python3 -m unittest discover -s cbe/_src -p 'test_*.py' -v
python3 phase-99220/_src/build.py
python3 phase-99220/_src/verify.py
python3 -m unittest discover -s phase-99220/_src -p 'test_*.py' -v
```

GitHub Actions repeats the source, link, privacy, rounding and regression checks for the live desks. A clean structural check does not establish the legal meaning of a fact pattern; confirm the current rules with the relevant professional before acting.
