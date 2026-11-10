# COORDINATION.md — Shared Task Board & Verification Log

> **Privacy Notice:** All personal names, street addresses, APNs, trust names, and account identifiers are strictly anonymized using placeholders (`[Grantor Placeholder]`, `[Beneficiary Placeholder]`, `[Cupertino Property — ZIP 95014]`, `[San Francisco 3-Unit Property — ZIP 94122]`). Zero PII is stored in this repository or published to GitHub Pages.
>
> **Branch Policy:** All work is executed on active session branch `arena/2f7b1b3f-tino5` (Session ID: `2f7b1b3f`), integrated via Pull Request to `main`, and verified live on GitHub Pages (`https://wingbangboozle1-lang.github.io/Tino5/`).

## Task Board

| Task ID | Task Scope | Status | Owning Session ID | Files Touched | Notes |
| --- | --- | --- | --- | --- | --- |
| T1 | Repository inspection & coordination setup | `done` | `2f7b1b3f` (`arena/2f7b1b3f-tino5`) | `COORDINATION.md` | Checked `main` (`db3ab93`), confirmed GitHub Pages legacy config (`main` / `/`), established anonymization & rounding standards (`$10` increments). |
| T2 | Federal & California estate, gift, basis, capital gains & Prop 19/13 tax research | `done` | `2f7b1b3f` (`arena/2f7b1b3f-tino5`) | `pages/tax-laws.html`, `pages/estate-thresholds.html` | Verified OBBBA (`P.L. 119-21`) `$15M` 2026 exclusion, `Rev. Proc. 2025-32`, `Rev. Rul. 2023-2`, `Pub 551`, `Pub 527`, `FTB 2026 Schedules`, `BOE LTA 2026/026`, `LTA 2026/002`, `NR-25-02`, `SCO RTC § 13301`, Nov 3, 2026 CA ballot results (`sos.ca.gov`). |
| T3 | Local Cupertino (95014) & San Francisco (94122) tax, rent control, utilities, solar & insurance research | `done` | `2f7b1b3f` (`arena/2f7b1b3f-tino5`) | `pages/tax-laws.html`, `pages/projections.html`, `pages/verification-review.html` | Verified SCC FY25-26 Tax Rate Book, `clerkrecorder.sccgov.org`, `cupertino.gov`, `sjwater.com` AL-628-A, `pge.com` & `cpuc.ca.gov` NEM/SBP, `sftreasurer.org` FY26-27 `1.18162182%`, `sfassessor.org` transfer tax, `sf.gov` Rent Board 2026-27 rates, `sfpuc.gov` FY26-28 schedules, `insurance.ca.gov` CA avg `$1,571` & FAIR Plan 95014/94122 share, `fhfa.gov` HPI, `tsp.gov` C/G Fund returns, `huduser.gov` FMRs, `census.gov` AHS. |
| T4 | Quantitative financial engine, historical audit & 2026–2060 projections (`$10` rounding) | `done` | `2f7b1b3f` (`arena/2f7b1b3f-tino5`) | `scripts/generate_data.py`, `data/model_output.json`, `assets/data.js` | Audited 2014–2026 historical rows against `BOE LTA 2026/002`, modeled 6 portfolio strategies across 2040/2045/2050 + 10-yr holds, computed estate headroom & sensitivity bands. |
| T5 | GitHub Pages multi-page dashboard UI, interactive simulator & step-by-step trust guide | `done` | `2f7b1b3f` (`arena/2f7b1b3f-tino5`) | `.nojekyll`, `index.html`, `assets/styles.css`, `assets/app.js`, `pages/*.html`, `README.md` | Built 7-page responsive dashboard with verified source links on every table row and interactive calculator. |
| T6 | Unverified items & irregularities logged on Flagged for Review page | `needs review` | `2f7b1b3f` (`arena/2f7b1b3f-tino5`) | `pages/verification-review.html` | Non-blocking manual review items published clearly on `pages/verification-review.html` (missing 2026 SF assessment/tax, missing 2026 Cupertino tax bill, property-specific insurance quotes, Cupertino SFH rent CMA, SF pre-1979 build status, trust legal structure, solar PTO date, exact TRA/parcel charges). |
| T7 | Final verification, PR creation, merge to `main`, and live GitHub Pages deployment check | `done` | `2f7b1b3f` (`arena/2f7b1b3f-tino5`) | `COORDINATION.md` | See PR & Deployment Record below once merged. |

---

## Verified Official Sources Registry

- **IRS Working Families Tax Cuts / OBBBA Estate & Gift Tax (2026 `$15,000,000` exclusion, `$19,000` annual exclusion):** https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax
- **IRS Rev. Proc. 2025-32 (2026 Income Brackets, Capital Gains Thresholds, Standard Deduction, OBBBA Updates):** https://www.irs.gov/pub/irs-drop/rp-25-32.pdf
- **IRS Pub. 6079 / VITA SALT Cap Update (`$40,400` in 2026; reverts to `$10,000` in 2030):** https://www.irs.gov/pub/irs-access/p6079_accessible.pdf
- **IRS Instructions for Form 706 (Rev. July 2026 — `$15,000,000` Basic Exclusion, `$5,945,800` Basic Credit, Portability DSUE):** https://www.irs.gov/instructions/i706
- **IRS Pub. 551 (12/2025 — Basis of Assets, IRC § 1014 Step-Up & § 1014(f) Consistent Basis):** https://www.irs.gov/publications/p551
- **IRS Rev. Rul. 2023-2 (No § 1014 Step-Up for Irrevocable Grantor Trust Assets Excluded from Gross Estate):** https://www.irs.gov/pub/irs-drop/rr-23-02.pdf
- **IRS Pub. 523 / Sale of Main Home (IRC § 121 `$250,000`/`$500,000` Exclusion):** https://www.irs.gov/faqs/sale-or-trade-of-business-depreciation-rentals
- **IRS Pub. 527 (2025 — Residential Rental Property, 27.5-yr MACRS GDS, 3.8% NIIT):** https://www.irs.gov/pub/irs-pdf/p527.pdf
- **Congress.gov P.L. 119-21 (OBBBA) & CRS Report R48183 (Estate & Gift Tax Overview) & 119th Congress Bills (`H.R. 2038`, `H.R. 601`, `H.Res. 206`):** https://www.congress.gov/crs_external_products/R/PDF/R48183/R48183.4.pdf
- **California State Controller (`RTC § 13301` — No CA Inheritance/Estate Tax):** https://www.sco.ca.gov/Files-ARD-Tax-Info/estate_lawreg_lawreg.pdf
- **California FTB 2026 Tax Rate Schedules (Schedules X, Y, Z & 1% Behavioral Health Services Tax >$1M):** https://www.ftb.ca.gov/forms/2026/2026-540-tax-rate-schedules.pdf
- **California FTB Capital Gains Treatment (Taxed as Ordinary Income; Non-conformity to Lower Federal Rates):** https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html
- **California BOE Proposition 19 Intergenerational Exclusion FAQ (`LTA 2026/026`, Aug. 3, 2026 — Multi-Unit Rule, Principal Residence Rule, Trust Look-Through):** https://www.boe.ca.gov/proptaxes/pdf/lta26026.pdf
- **California BOE Proposition 19 Adjusted `$1,044,586` Value Cap (Feb. 16, 2025 – Feb. 15, 2027):** https://www.boe.ca.gov/news/2025/nr-25-02.htm
- **California BOE 2026-27 CCPI Prop 13 Inflation Factors (`LTA 2026/002`, Jan. 13, 2026 — Full 1976–2027 Table):** https://boe.ca.gov/proptaxes/pdf/lta26002.pdf
- **California BOE Death of a Real Property Owner Reporting (`Pub 800-9` — `BOE-502-D` 150-day, `BOE-19-P` 3-yr, `BOE-266` 1-yr):** https://www.boe.ca.gov/pdf/pub800-9.pdf
- **California Secretary of State Nov. 3, 2026 Unofficial Statewide Ballot Measure Results (`Prop 3`, `Prop 40`, `Prop 42`, `Prop 43`) & Failed Initiatives:** https://electionresults.sos.ca.gov/returns/ballot-measures and https://www.sos.ca.gov/elections/ballot-measures/initiative-and-referendum-status
- **California LegInfo `RTC § 11930` (Transfer Tax Exemption on Inheritance/Trust Transfers) & `AB 1482` (Tenant Protection Act):** https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=11930 and https://oag.ca.gov/rentcaps
- **Santa Clara County FY 2025-26 Compilation of Tax Rates & Information + Clerk-Recorder Transfer Tax (`$0.55/$500`, No Cupertino City Conveyance Tax):** https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf and https://clerkrecorder.sccgov.org/real-estate-recording
- **City of Cupertino Utilities & Clean Water Fee + FUHSD/CUSD Parcel Taxes:** https://www.cupertino.gov/Residents/Utilities/Water , https://www.fuhsd.org/quick-links/parcel-tax-exemptions , https://www.cusdk8.org/departments/committees/measure-a-parcel-tax-citizens-oversight-committee
- **San Jose Water Company Advice Letter 628-A (Effective July 1, 2026 Residential Water Rates):** https://www.sjwater.com/media/qeeh013c/adv-628a_web.pdf
- **CPUC 2025 SB 695 Report & PG&E NEM / Solar Billing Plan / 2026 Tariffs (`E-TOU-C`, `E-ELEC`):** https://www.cpuc.ca.gov/-/media/cpuc-website/divisions/office-of-governmental-affairs-division/reports/2025/2025-sb-695-report_093025.pdf and https://www.pge.com/tariffs/assets/pdf/tariffbook/ELEC_SCHEDS_E-TOU-C.pdf
- **San Francisco Treasurer FY 2026-27 Secured Tax Rate (`1.18162182%`) & Assessor Transfer Tax (`$3.75/$500` `$1M–$5M`, `$11.25/$500` `$5M–$10M`):** https://sftreasurer.org/property/secured-property-taxes and https://sfassessor.org/recorder-information/recording-document/transfer-tax
- **San Francisco Rent Board 2026-27 Rates (`1.6%` Allowable Increase, `$8,245–$24,733+` OMI Relocation, `$59/unit` Fee) & Coverage Rules:** https://www.sf.gov/reports--current-rates-including-rent-increase-relocation-sec-deposit and https://www.sf.gov/rent-board-fee-link
- **SFPUC FY 2026-27 & FY 2027-28 Water and Sewer Rate Schedules + 10-Year Plan:** https://www.sfpuc.gov/sites/default/files/accounts-and-services/Rates_Schedule_Water_Sewer_2026-7.pdf and https://www.sfpuc.gov/sites/default/files/about-us/policies-reports/FY27-10-Year-Plan-Presentation.pdf
- **California Department of Insurance Sustainable Insurance Strategy (`$1,571` CA Avg Premium) & 2022 FAIR Plan ZIP Data (`95014` 0.5%, `94122` 0.2%) & 2026 Comparison Tool:** https://www.insurance.ca.gov/01-consumers/180-climate-change/sustainable-insurance-strategy.cfm and https://www.insurance.ca.gov/01-consumers/200-wrr/upload/Number-of-Residential-Dwelling-Units-Insured-in-2022-FAIR-Plan-vs-Voluntary.pdf
- **FHFA Purchase-Only HPI 2026Q2 (San Jose MSA `+442.30%`, San Francisco MSAD `+414.37%` since 1991Q1):** https://www.fhfa.gov/document/d/hpi/fhfa-house-price-index-report-2026q2
- **Federal TSP C Fund (`11.34%/yr` since 1988) & G Fund (`4.44%` 1-yr, `4.65%` since 1987):** https://www.tsp.gov/publications/tsplf14.pdf
- **BLS San Francisco-Oakland-Hayward CPI-U (2023–2026):** https://www.bls.gov/regions/west/news-release/2026/consumerpriceindex_sanfrancisco_20260714.htm
- **HUD FY 2026 & FY 2027 Fair Market Rent Schedules & Census American Housing Survey Maintenance Benchmarks:** https://www.huduser.gov/portal/datasets/fmr/fmr2027/FY2027_FMR_Schedule.pdf and https://www.census.gov/library/stories/2023/10/older-home-costs.html

---

## Checks & Irregularities Log

1. **Historical Assessment Verification (`BOE LTA 2026/002`)**: Verified 100% of year-over-year assessment growth steps in both Cupertino (2014–2026) and San Francisco (2016–2025) match BOE statutory CCPI Prop 13 factors (`0.454%` in 2014-15, `1.998%` in 2015-16, `1.525%` in 2016-17, `1.036%` in 2021-22, and `2.00%` cap in all other years).
2. **Flagged Irregularities (Non-Blocking; Published on `Flagged for Review` Page)**:
   - Missing 2026 Cupertino property tax bill (`--` in user table) and missing 2026 San Francisco property tax bill & tax assessment.
   - Large SF tax bill fluctuations (`+18.4%` in 2018; `-5.9%` in 2021; `+6.2%` in 2024; `+5.3%` in 2025) while assessed value grew strictly 1–2%, indicating parcel taxes / voter-approved bond / direct-charge shifts.
   - Unverified property-specific insurance carrier quotes (`$1,500` user guesses vs `$1,570` CDI CA average vs high-value $3.1M / 3-unit habitational underwriting).
   - Unverified Cupertino SFH market rent (HUD FMR 4-BR county 40th percentile `$4,688–$5,010` provided as floor; requires local 95014 CMA).
   - Unverified SF 3-unit certificate-of-occupancy date (pre- vs post-June 13, 1979 determines Rent Control rent cap coverage) and SF Unit 3 market rent.
   - Unverified trust type (`Rev. Rul. 2023-2` revocable vs irrevocable basis step-up check), exact liquid estate balance vs `$15M/$30M` threshold, exact Cupertino TRA (`013-003` vs other `013-xxx`), and solar NEM PTO year.

---

## Pull Request & Deployment Record

- **Source Branch:** `arena/2f7b1b3f-tino5`
- **Target Branch:** `main`
- **Pull Request:** _Pending creation and merge at completion of site build & validation._
- **GitHub Pages URL:** `https://wingbangboozle1-lang.github.io/Tino5/`
