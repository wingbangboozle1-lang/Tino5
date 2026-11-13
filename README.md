# Estate decision desk — privacy-first inheritance planning

A source-linked decision framework for a future trust inheritance (Property A) and a separate property already owned by the inheritor (Property B).

**Live site:** https://wingbangboozle1-lang.github.io/Tino5/

**Site map:** the root [`index.html`](index.html) is the hub. The newest desk is the [decision desk](decision-ad038/index.html) (live vs rent vs sell, projections, black-swan paths, law, questions, flagged items, sources). The curated dashboard remains at [`public-safe/index.html`](public-safe/index.html).

The GitHub Pages landing page is a hub that links to each desk.

## Dashboard sections

- [Executive summary](public-safe/index.html)
- [Occupy, rent, or sell](public-safe/decision.html)
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

**Repository caveat:** a repository-wide scan found residual owner-derived amounts in five non-deployed legacy files, and earlier commits/branches may also retain previous figures. Those files are excluded from the deployed artifact; removing content from the site cannot erase public Git history or caches. Repository cleanup, visibility changes, or history rewriting is an owner decision.

## Build and verification

```bash
python3 scripts/build_desk.py
python3 scripts/verify_safe.py
```

The structural verifier checks the 11-page artifact, table-row source links, internal links, allowed external hosts, money rounding, and common personal-identifier patterns. It does not prove a cited source supports a claim; sources are separately reviewed and linked beside each row.
