# Home & Legacy — California Property Decision Dashboard

A privacy-first, source-linked research site to help compare inheriting, occupying, renting, or selling two anonymized California properties. It focuses on current federal estate-tax rules, California Proposition 19 property-tax reassessment, rental and insurance research, a practical inheritance checklist, cost-model inputs, and items needing verification.

## Run locally

Open `index.html` in a browser, or serve the repository root with any static HTTP server. The site has no runtime dependencies, tracking, forms, user-submitted data, or build step.

## Privacy

The public site intentionally omits names, street addresses, ZIP codes, parcel numbers, exact property values, rents, utility amounts, beneficiary details, trust documents, and household financial records. Use only the `Property A` / `Property B` aliases. Source links support the law and method—not verification of private parcel-specific figures.

## Verification and limitations

Each displayed factual table row links to an official government source. If a property-specific amount could not be verified, it is blank and listed on the **Flagged for review** page. Future market values, carrying costs, tax law, premiums, and investment returns are not presented as forecasts. Dollar values displayed on the site are rounded to the nearest $10. Source review date: November 10, 2026.

## Publish

The repository already has GitHub Pages enabled from the root of its `main` branch (legacy branch publishing). Merging a change to `main` triggers that existing Pages build. `.github/workflows/pages.yml` adds a separate pull-request / main-branch validation check; it does not change the repository’s current Pages deployment source.
