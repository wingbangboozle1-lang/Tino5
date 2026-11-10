# Coordination — Tino5 Inheritance Decision Site

Integration history: `arena/d66fc558-tino5` (research/build), `arena/036d45c7-tino5` (original final integration), and current privacy audit `arena/9a1b9ff8-tino5`. Date: 2026-11-10.

## Task board

| ID | Task | Status | Owner session | Files touched |
|---|---|---|---|---|
| T1 | Research official federal, California, county, court, insurance, and utility sources | done | `arena/d66fc558-tino5` | source and tax reference pages (now replaced by privacy-safe reference pages) |
| T2 | Build GitHub Pages site and decision-analysis pages | done | `arena/d66fc558-tino5` | prior public pages (removed in T5 because they included private case data) |
| T3 | Original source/rounding verification | done | `arena/d66fc558-tino5`, `arena/036d45c7-tino5` | original page set |
| T4 | Original final integration and Pages deployment | done | `arena/036d45c7-tino5` | PR #3 and original site |
| T5 | Privacy remediation: remove case-specific details from public site; retain general official-law guidance; validate new deploy | in progress | `arena/9a1b9ff8-tino5` | `index.html`, `pages/`, `styles.css`, `README.md`, `COORDINATION.md`, former case-specific pages/assets |

Status key: `unclaimed` / `in progress` / `done` / `needs review` (published on Flagged for Review; does not block).

## Handoff / coordination log

- 2026-11-10 — Session `arena/d66fc558-tino5` created the initial project pages and opened PR #1 (merged as `01448a3`).
- 2026-11-10 — Session `arena/036d45c7-tino5` completed integration in PR #3, merged as `e3ae978`; GitHub Pages was live from `main`.
- 2026-11-10 — Session `arena/9a1b9ff8-tino5` initially found only the starting commit on its checkout and no coordination file, created a claim, and pushed it on the fixed Arena branch. Main subsequently advanced through PR #3. The duplicate initial PR #4 was closed after discovering the merged integration and public pages.
- 2026-11-10 — Privacy audit found that the already-published prior pages included user-supplied, property-specific financial details and ZIP-level labels. Although some were marked “user-provided/unverified,” publishing them conflicted with the privacy requirement. T5 removes those pages/assets from the GitHub Pages root, replaces the landing site with a general, non-identifying dashboard, and retains only law/source guidance and blank/flagged case-specific unknowns.
- 2026-11-10 — Merging current `origin/main` into the fixed session branch produced conflicts in `COORDINATION.md`, `README.md`, and `index.html`. Resolved by retaining the prior integration/PR history, rebuilding this board without case details, updating the README, and using the privacy-safe index; prior private-data pages were removed from the public site rather than preserved. No other session’s source or legal research was silently represented as verified case information.
- The original GitHub Pages deployment uses the repository’s existing legacy `main` branch/root source. No separate GitHub Actions deploy workflow is retained; the new site will publish through the existing Pages configuration after PR merge.

## Verification / source record

Official current-law references checked for the replacement site:

- Federal estate/gift rules and current 2026 amounts: [IRS estate-tax FAQs](https://www.irs.gov/businesses/small-businesses-self-employed/frequently-asked-questions-on-estate-taxes), [Rev. Proc. 2025-32](https://www.irs.gov/pub/irs-drop/rp-25-32.pdf), [Form 706 instructions](https://www.irs.gov/instructions/i706), [IRS enacted-law update](https://www.irs.gov/newsroom/working-families-tax-cuts-individuals-and-workers).
- Inherited basis, rental income/expenses and sale rules: [IRS Pub. 551](https://www.irs.gov/publications/p551), [Pub. 527](https://www.irs.gov/publications/p527), [Pub. 559](https://www.irs.gov/publications/p559), [Pub. 523](https://www.irs.gov/publications/p523).
- California estate/inheritance and income treatment: [State Controller](https://www.sco.ca.gov/ardtax_estate_tax.html), [FTB](https://www.ftb.ca.gov/file/personal/income-types/gifts-and-inheritance.html).
- Prop 13 / Prop 19 / death-transfer reporting: [BOE Pub. 800-10](https://boe.ca.gov/pdf/pub800-10.pdf), [BOE Prop 19](https://boe.ca.gov/prop19/), [BOE 2025 allowance notice](https://www.boe.ca.gov/news/2025/nr-25-02.htm), [BOE death-transfer guidance](https://www.boe.ca.gov/proptaxes/pdf/lta24052.pdf), [Santa Clara Assessor Prop 19 guidance](https://asr.santaclaracounty.gov/tax-savings/transferring-your-assessed-value/parent-to-child-2), [SF Assessor family-transfer guide](https://www.sfassessor.org/forms-notices/notices/property-tax-savings-transfers-family).
- Trust administration: [Santa Clara Superior Court probate-trust guidance](https://santaclara.courts.ca.gov/divisions/probate-division/probate-trusts), [California county assessor directory](https://www.boe.ca.gov/proptaxes/assessors.htm).
- Insurance, utilities, solar and repairs: [California DOI](https://www.insurance.ca.gov/01-consumers/105-type/5-residential/Top10Tips_FindingResidentialIns.cfm), [Cal Water tariff portal](https://www.calwater.com/rates/rates-and-tariffs/), [Cal Water service area](https://www.calwater.com/district/los-altos-suburban/), [San Jose Water approved tariff](https://www.sjwater.com/media/dm3lribs/san-jose-water-company-al-628-a-approved.pdf), [SFPUC rates](https://www.sfpuc.gov/accounts-services/water-power-sewer-rates), [CPUC solar consumer guide](https://www.cpuc.ca.gov/industries-and-topics/electrical-energy/demand-side-management/customer-generation/california-solar-consumer-protection-guide), [California CSLB](https://www.cslb.ca.gov/Consumers/FindMyLicensedContractor/).
- Legislative status: [Congress.gov H.Res.206](https://www.congress.gov/bill/119th-congress/house-resolution/206/all-info), [H.R.137](https://www.congress.gov/bill/119th-congress/house-bill/137/all-info). These are proposal/status references only, not enacted future law.

## Current verification

- New public site is general and intentionally omits property-specific financial history, estimates, ZIP codes, lease/rent information, utility usage, insurance/maintenance figures, names, addresses, APNs, and inheritance balance.
- New tables retain official HTTPS links for each data row. Locally validated page count, internal page/anchor links, table citations, privacy scan, and `git diff --check` before final publication; repeat after integration.
- No exact household insurance premium, utility bill, assessed/tax value, maintenance reserve, rental net income, 2040–2050 property-value forecast, or future tax threshold is verified; these stay blank on the Flagged for Review page.

## PR / deployment history

- PR #1: https://github.com/wingbangboozle1-lang/Tino5/pull/1 — merged.
- PR #2: https://github.com/wingbangboozle1-lang/Tino5/pull/2 — merged.
- PR #3: https://github.com/wingbangboozle1-lang/Tino5/pull/3 — merged; original Pages deployment confirmed live.
- PR #4: https://github.com/wingbangboozle1-lang/Tino5/pull/4 — closed as duplicate before merge after discovering PR #3 had already integrated the original site.
- Privacy-remediation PR and final Pages deployment status: pending.
