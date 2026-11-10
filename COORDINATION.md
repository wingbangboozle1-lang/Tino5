# Coordination Board — Cupertino & San Francisco Inheritance Decision Project

> **Privacy Policy (Highest Priority):** No real names, street addresses, Assessor's Parcel Numbers (APNs), trust names, or personally identifiable information (PII) may ever appear in this repository or on the published website. All property and personal references use anonymized placeholders (`Property A — Cupertino 95014`, `Property B — San Francisco 94122`, `[Grantor]`, `[Beneficiary / Successor Trustee]`, `[Revocable Living Trust]`).

## Active Session & Branch Policy

- **Active Session ID:** `arena/f9da2018-tino5`
- **Working Branch:** `arena/f9da2018-tino5` (session-locked branch per Arena environment policy)
- **Target Integration Branch:** `main` (GitHub Pages source: `main` `/`)
- **Started:** `2026-11-10T10:04:00Z`

---

## Task Board

| Task ID | Description | Status | Owning Session | Files Touched |
| --- | --- | --- | --- | --- |
| T0 | Repo review, privacy framework, `.nojekyll`, and coordination board initialization | `done` | `arena/f9da2018-tino5` | `COORDINATION.md`, `.nojekyll` |
| T1 | Federal & CA estate, trust, capital gains, Prop 13/19 tax law & legislative research | `done` | `arena/f9da2018-tino5` | `data/laws-verified.json` |
| T2 | Cupertino (ZIP 95014) property tax, utility, solar, insurance, and anomaly verification | `done` | `arena/f9da2018-tino5` | `data/cupertino-verified.json` |
| T3 | San Francisco (ZIP 94122) 3-unit property tax, rent law, utility, insurance verification | `done` | `arena/f9da2018-tino5` | `data/san-francisco-verified.json` |
| T4 | 2026–2050 quantitative financial model & nearest-$10 rounded scenario engine | `done` | `arena/f9da2018-tino5` | `scripts/model.py`, `data/projections.json` |
| T5 | GitHub Pages multi-page dashboard UI (`index.html`, subpages, `Flagged for Review`) | `in progress` | `arena/f9da2018-tino5` | `index.html`, `pages/*.html`, `assets/*` |
| T6 | Line-by-line verification, PII audit, link/JS check, PR to `main`, merge & Pages live check | `unclaimed` | — | `COORDINATION.md`, PR & merge record |

---

## Verification & Source Log

- **Federal Estate, Gift & Income Tax:**
  - IRS Rev. Proc. 2025-32 (`https://www.irs.gov/pub/irs-drop/rp-25-32.pdf`) & P.L. 119-21 Sec. 70106 (`https://www.congress.gov/bill/119th-congress/house-bill/1/all-info`): 2026 Estate/Gift/GST exclusion `$15,000,000` (`$30M` married), permanent & indexed; 2026 LTCG 0%/15%/20% thresholds (`$49,450`/`$545,500` single; `$98,900`/`$613,700` MFJ; `$16,250` trusts).
  - IRS Rev. Proc. 2026-35 (`https://www.irs.gov/pub/irs-drop/rp-26-35.pdf`): 2027 Estate/Gift/GST exclusion `$15,480,000` (`$30.96M` married, `+3.20%` YoY), annual gift exclusion `$20,000` (up from `$19,000` in 2026 per Rev. Proc. 2026-25), trust top 37% rate at `$16,500`.
  - IRS Form 706 Instructions (`https://www.irs.gov/pub/irs-pdf/i706.pdf`): 40% top estate tax rate; DSUE portability election rules.
  - IRS Pub. 523 (`https://www.irs.gov/publications/p523`), Topic 701 (`https://www.irs.gov/taxtopics/tc701`), Pub. 505 (`https://www.irs.gov/publications/p505`): IRC § 1014 full basis step-up at death (100% double step-up for CA community property), IRC § 121 `$250k/$500k` exclusion, `3.8%` NIIT (`$200k` single / `$250k` MFJ).
  - Congress.gov H.R. 2038 (`https://www.congress.gov/bill/119th-congress/house-bill/2038/text`) & H.Res. 206 (`https://www.congress.gov/bill/119th-congress/house-resolution/206/text/ih?format=xml&overview=closed`).
- **California Tax, Probate & Prop 13/19:**
  - CA State Controller's Office (`https://sco.ca.gov/Files-EO/Appendices_cea.pdf`): Zero CA state estate/inheritance tax since 1982 (Prop 5/6) & 2005 pickup repeal.
  - CA FTB 2026 Tax Schedules (`https://www.ftb.ca.gov/forms/2026/2026-540-tax-rate-schedules.pdf`) & Conformity Summary (`https://www.ftb.ca.gov/about-ftb/data-reports-plans/summary-of-federal-income-tax-changes/index.html`) & Schedule D Instructions (`https://www.ftb.ca.gov/forms/2024/2024-540-d-instructions.html`) & R&TC § 18031: CA taxes capital gains as ordinary income up to `13.3%` (`12.3%` + `1%` MHSA `>$1M`) and conforms to IRC § 1014 step-up in basis.
  - CA BOE LTA 2026/002 (`https://boe.ca.gov/proptaxes/pdf/lta26002.pdf`): Full 1976–2027 Prop 13 CCPI table (`2021-22: 1.036%`, `2022-27: 2.00%`, matching user assessment history).
  - CA BOE LTA 2025/009 (`https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf`), Pub. 801 (`https://www.boe.ca.gov/pdf/pub801.pdf`), LTA 2026/026 (`https://www.boe.ca.gov/proptaxes/pdf/lta26026.pdf`), Pub. 800-6 (`https://www.boe.ca.gov/pdf/pub800-6.pdf`): Prop 19 FBYV + `$1,044,586` (2025–2027), 1-yr residency + BOE-266 (`$7,000` Homeowners' Exemption), 3-yr BOE-19-P, Q5 multi-unit single-unit cap, Q32–Q35 LLC ineligibility.
  - CA Probate Code § 16061.7 (`https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PROB&sectionNum=16061.7`): 60-day trustee notice / 120-day contest window.
  - CA Secretary of State Nov 3, 2026 Ballot Results (`https://electionresults.sos.ca.gov/returns/ballot-measures`), Qualified List (`https://www.sos.ca.gov/elections/ballot-measures/qualified-ballot-measures`), Failed/Withdrawn List (`https://www.sos.ca.gov/elections/ballot-measures/initiative-and-referendum-status/failed-qualify`), Prop 19 Repeal Notice (`https://www.sos.ca.gov/administration/news-releases-and-advisories/2025-news-releases-and-advisories/proposed-initiative-enters-circulation-repeals-voter-enacted-changes-property-tax-rules-transfers-between-family-members-initiat`): Prop 3 (`60.6%` Yes), Prop 42 (`51.6%` Yes), Prop 40 (`47.2%` Yes / trailing), Prop 19 repeal (#1994/25-0017) & 60+ exemption (#2012/25-0035) did not qualify.
- **Cupertino (95014) & San Francisco (94122) Local Agencies, Utilities, Insurance & Macro:**
  - Santa Clara County Tax Rate Book FY 2025-26 (`https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf`) & Clerk-Recorder (`https://clerkrecorder.santaclaracounty.gov/recording-documents/recording-real-estate`): Cupertino bond components (`~1.1612%` ad valorem), `$1.10/$1,000` County DTT, `$0` Cupertino city conveyance tax.
  - City of Cupertino Utilities (`https://www.cupertino.gov/Residents/Utilities`), CPUC Cal Water Res./D.26-04-045 (`https://docs.cpuc.ca.gov/PublishedDocs/Published/G000/M610/K156/610156069.pdf`), CPUC SJWC A.24-01-001 (`https://docs.cpuc.ca.gov/PublishedDocs/Efile/G000/M522/K429/522429327.PDF`): Cal Water `$87.53/mo` avg vs SJWC `$125.44/mo` (2026).
  - SVCE Solar Billing Plan & NEM Schedule (`https://www.svcleanenergy.org/solar-billing-plan/`, `https://svcleanenergy.org/wp-content/uploads/2025-1112-Presentations-Combined-3-4-5-6-scrubbed.pdf`) & CPUC SB 695 Report / Webinar (`https://www.cpuc.ca.gov/-/media/cpuc-website/divisions/news-and-outreach/documents/bco/webinars/final-slides_revised_electric-rates-and-you_10282026.pdf`) & CPUC D.24-05-028 Base Services Charge (`https://docs.cpuc.ca.gov/PublishedDocs/Published/G000/M555/K816/555816677.pdf`): SVCE 2x->1x NSC cut in 2026, `$24.15/mo` Base Services Charge, 20-yr NEM sunset to NBT.
  - SF Treasurer Secured Property Taxes (`https://sftreasurer.org/property/secured-property-taxes`) & Assessor Transfer Tax (`https://www.sf.gov/transfer-tax`, `https://www.sf.gov/information--learn-about-transfer-tax`): `1.18162182%` FY 2026-27 (`1.18268325%` FY 2025-26); `$3.75/$500` (`$1M-<$5M`) jumping to `$11.25/$500` (`$5M-<$10M`); inheritance/trust transfers exempt.
  - SF Rent Board (`https://www.sf.gov/reports--current-rates-including-rent-increase-relocation-sec-deposit`, `https://media.api.sf.gov/documents/m021026.pdf`): `1.6%` allowable increase (3/1/26–2/28/27), `$59/unit` annual fee.
  - SFPUC Water & Sewer Rates FY26-28 (`https://www.sfpuc.gov/sites/default/files/accounts-and-services/Rates_Schedule_Water_Sewer_2026-7.pdf`), 10-Yr Plan (`https://www.sfpuc.gov/sites/default/files/about-us/policies-reports/FY27-10-Year-Plan-Report.pdf`), CleanPowerSF (`https://www.sfpuc.gov/accounts-services/water-power-sewer-rates/power-rates`).
  - CA Dept. of Insurance 2025 Residential Summary (`https://www.insurance.ca.gov/0400-news/0200-studies-reports/0300-earthquake-study/upload/EQEXP2025Summary.pdf`), Sustainable Insurance Strategy (`https://www.insurance.ca.gov/01-consumers/180-climate-change/sustainable-insurance-strategy.Cfm`), State Farm Settlement (`https://www.insurance.ca.gov/0400-news/0100-press-releases/2026/release012-2026.cfm`).
  - Macro: FHFA HPI 2026Q2 (`https://www.fhfa.gov/document/d/hpi/fhfa-house-price-index-report-2026q2`), BLS SF CPI-U Aug 2026 (`https://www.bls.gov/regions/west/news-release/consumerpriceindex_sanfrancisco.htm`), CBO Budget & Long-Term Outlook (`https://www.cbo.gov/publication/62105`, `https://www.cbo.gov/publication/61270`), U.S. Treasury Oct 2026 Yield Curve (`https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=202610`), SEC Investing Guide (`https://www.sec.gov/investor/pubs/savings-investing-for-students.pdf`).

---

## Flagged Irregularities & Unverified Items Log

1. **Cupertino 2026 Property Tax Missing (`--`) & 2017–2018 / 2019–2020 Flat Taxes:** 2026 tax bill not provided (`--`); 2017–18 (`$6,383`) and 2019–20 (`$6,565`) show 0% tax change despite verified `+2%` AV growth (possible portal duplication or bond rate drop). Unverified without parcel APN.
2. **San Francisco 2026 Row Missing & 2018 (`+18.4%`) / 2021 (`-5.9%`) Tax Swings:** 2026 SF tax and AV omitted from prompt; 2018 jump (`+$321`) likely reflects voter-approved parcel taxes on a low `$100k` Prop 13 base, while 2021 dip (`-$131`) conflicts with `+1.036%` AV growth. Implied ~2.14% effective rate confirms significant fixed direct charges on top of `1.18%` ad valorem.
3. **Insurance Estimates (`~$1,500/yr` on Both Properties) Unverified & Below CDI Benchmarks:** Exact carrier quotes are unverified without square footage/year built/underwriting. CDI 2025 data averages `$2,340/yr` (`$3.38/$1,000`) statewide for average Homeowners coverage and State Farm's March 2026 settlement raised homeowners `+17%` and rental dwelling `+32.8%`; `$1,500/yr` likely materially understates replacement-cost policies for a `$3.1M` Cupertino home and a `$1.8M` 3-unit SF rental.
4. **Cupertino Solar Credit (`+$10–$20/mo`) Policy Cliff:** SVCE cut Net Surplus Compensation from `2x` to `1x` PG&E NSC in 2026, PG&E added a non-offsettable `$24.15/mo` Base Services Charge, and 20-year NEM 1.0/2.0 grandfathering expires (2037–2043) before/during the 2040–2050 inheritance window, flipping net electricity from a credit to a net expense.
5. **Cupertino Water Utility Split (Cal Water vs SJWC) & Imputed Cupertino Rent:** 95014 is split between Cal Water (`~$87.53/mo` avg) and San Jose Water (`~$125.44/mo` avg); exact provider requires street address. Cupertino market rent (`$7,200/mo` modeled in Strategy B) and exact Unit 3 SF market rent (`$3,575/mo` in Strategy A2) are unverified market assumptions requiring local comps.
6. **Prop 19 Primary Residence Conflict & SF 3-Unit Restriction:** Parents/child can claim Prop 19 on only ONE primary residence. Moving into SF Unit 3 forfeits Cupertino's larger Prop 19 shield; furthermore, per BOE LTA 2026/026 Q5, even on an owner-occupied multi-unit SF building, ONLY the single occupied unit can qualify while the 2 rented units are 100% reassessed. Also unverified whether the SF building was built before June 13, 1979 (SF Rent Ordinance coverage) and whether properties are held in a look-through Revocable Living Trust (not an LLC, which disqualifies Prop 19).
7. **Unverified Maintenance/CapEx, Exact Parent Financial Assets & Inheritance Year:** Maintenance reserves (`$12k/yr` Cupertino, `$16.5k/yr` SF), parents' exact 2026 liquid/retirement assets, and exact date of death within 2040–2050 are modeled via transparent parametric ranges and left unverified as site-specific facts.

---

## Pull Request & Deployment Record

*(Populated upon PR creation, merge to `main`, and live GitHub Pages verification.)*
