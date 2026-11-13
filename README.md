# Estate decision desk — privacy-first inheritance planning

A source-linked decision framework for a future trust inheritance (Property A) and a separate property already owned by the inheritor (Property B).

**Live site:** https://wingbangboozle1-lang.github.io/Tino5/

**Site map:** the root [`index.html`](index.html) is the hub and links to the published curated dashboard at [`public-safe/index.html`](public-safe/index.html). The decision desk in [`decision-ad038/`](decision-ad038/index.html) is kept in the repository and is excluded from Pages until the owner approves publication (the verifier fails closed for every top-level directory except `public-safe/`).

The GitHub Pages landing page is a hub that links to the published curated dashboard.

## Dashboard sections

- [Executive summary](public-safe/index.html)
- [Occupy, rent, or sell](public-safe/decision.html)
- [Suggestions for review](public-safe/suggestions.html)
- [Year-by-year projection worksheet](public-safe/projections.html)
- [Property facts and unknowns](public-safe/properties.html)
- [Insurance, utilities, and repairs](public-safe/costs.html)
- [Black-swan and uneven-economy scenarios](public-safe/black-swans.html)
- [Inheritance, estate, and property tax](public-safe/tax.html)
- [Trust inheritance process](public-safe/process.html)
- [Law and policy watch](public-safe/law-watch.html)
- [Flagged for review](public-safe/flagged.html)
- [Official source register](public-safe/sources.html)

## Privacy and verification

Property-specific values, tax histories, rents, bills, addresses, parcel identifiers, and other household financial details are intentionally omitted from the public dashboard. Unknown or unverified property-specific values remain blank and are listed on the Flagged for review page. Property A is the future trust inheritance; Property B is already owned, and the decision framework treats them separately.

The current release presents official legal rules and economic-history references, not a personalized numeric forecast or investment recommendation. No 2040–2050 law, market return, property value, insurance premium, or rental cash flow is guaranteed. Re-check the law and obtain property-specific professional advice at the time of transfer.

**Repository caveat:** a repository-wide scan found residual owner-derived amounts in non-deployed repository files, and earlier commits/branches may also retain prior figures. The curated Pages configuration excludes these research/legacy trees; excluding content from the current site does not erase public Git history or caches. Repository cleanup, visibility changes, or history rewriting is an owner decision.

## Build and verification

```bash
python3 scripts/build_desk.py
python3 scripts/verify_safe.py
```

The structural verifier checks the 12-page artifact, table-row source links, internal links, allowed external hosts, deployment exclusions, money rounding, and common personal-identifier patterns. It does not prove a cited source supports a claim; sources are separately reviewed and linked beside each row.

The structural verifier checks the 11-page artifact, table-row source links, internal links, allowed external hosts, money rounding, and common personal-identifier patterns. It does not prove a cited source supports a claim; sources are separately reviewed and linked beside each row.

## Decision desk (`review-092b/`)

Eleven pages, generated from a deterministic model, checked by a structural verifier. **Not yet
published:** the fail-closed rule in `scripts/verify_safe.py` permits only `public-safe/` to be a
publishable top-level directory, so `review-092b` is listed in the deployment exclusions and the root
hub does not link into it. Publishing it needs an owner decision to add it as a reviewed publishable
directory (add it to `DEPLOYMENT_EXCLUSIONS`'s exception and remove it from `_config.yml`).

```bash
python3 review-092b/_src/build.py                              # rebuild review-092b/
python3 review-092b/_src/verify.py                             # structural gate
python3 -m unittest discover -s review-092b/_src -p "test_*.py" # regression tests
```

- [Executive summary](review-092b/index.html)
- [Questions that must be answered first](review-092b/questions.html)
- [Suggestions, for review before any change](review-092b/suggestions.html)
- [Projections, cost by cost, year by year](review-092b/projections.html)
- [Occupy, rent, or sell](review-092b/decision.html)
- [Black swans and uneven economies](review-092b/black-swans.html)
- [How inheriting through a trust works](review-092b/inheritance.html)
- [Inheritance tax, property tax and carrying costs](review-092b/costs.html)
- [Repository review and irregularities](review-092b/repo-review.html)
- [Flagged for review](review-092b/flagged.html)
- [Official source register](review-092b/sources.html)

`review-092b/summary.json` holds the model's published outputs. `_src/` is excluded from the
published site by `_config.yml` (matched as `_src`).

### What the verifier enforces

Every table body row must carry a link that traces the claim — an official document for a factual
row, a repository path for a row about the repository. Every external link must be `https` on a
publisher host listed in `_src/sources.py`. Every internal link must resolve. Every dollar amount in
prose must be a multiple of $10, except statutory or agency figures wrapped in
`<span class="stat">`, which are quoted exactly as published. No e-mail, phone, ZIP, street address,
parcel token or city name may appear. No scripts, forms, iframes or remote assets.

### Departure from the owner's literal instruction, flagged for review

The owner asked for all figures rounded to the nearest $10. In this desk that rule is applied in the
protective direction: the two 2026 roll values are published rounded, but the multi-year assessment
and tax histories are **not published at all**, at any rounding. A rounded series is still a unique
fingerprint against the county's open roll data. The departure is recorded on the flagged page for
the owner to accept or reverse.
