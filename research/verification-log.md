# Verification Log

Generated: 2026-11-10 (UTC). Automated: `python3 scripts/verify.py`.

## What was verified

- 54 official government sources, each fetched and read during research.
- 21 data tables containing 326 rows in total.
- 44 rows of federal and state/local law read directly from the linked agency pages.
- 13 published HTML pages, all served successfully over HTTP (200).
- 20 items published on the Flagged for Review page.

## Checks performed

| # | Check | Result |
| --- | --- | --- |
| 1 | Every source URL uses HTTPS and an official government host | PASS |
| 2 | Every table row has the correct number of cells, a valid source ID and a status | PASS |
| 3 | Every rendered table row contains an official source link and a status badge | PASS |
| 4 | Every internal link resolves; HTTP smoke test returns 200 | PASS |
| 5 | No personal-information patterns in any published HTML | PASS |
| 6 | All dollar amounts ≥ $100 are rounded to the nearest $10 | PASS |

## Official source register (line by line)

| ID | Agency | Document | URL | What was read |
| --- | --- | --- | --- | --- |
| `IRS_ESTATE` | Internal Revenue Service | Estate tax (filing thresholds by year of death) | https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax | Gross-estate definition; 2026 Form 706 filing threshold $15,000,000; portability election. |
| `IRS_ESTATE_FAQ` | Internal Revenue Service | Frequently asked questions on estate taxes | https://www.irs.gov/businesses/small-businesses-self-employed/frequently-asked-questions-on-estate-taxes | Public Law 119-21 raised the basic exclusion to $15,000,000 for 2026; Form 706 due 9 months after death; 6-month extension via Form 4768; DSUE portability. |
| `CONGRESS_HR1` | United States Congress | H.R.1, Public Law 119-21, text (Sec. 70106) | https://www.congress.gov/bill/119th-congress/house-bill/1/text | Sec. 70106 replaces $5,000,000 with $15,000,000; inflation indexing for years beginning after 2026. |
| `CONGRESS_HR1_SUM` | United States Congress | H.R.1 summary, Public Law 119-21 (07/04/2025) | https://www.congress.gov/bill/119th-congress/house-bill/1 | Increases the base estate, gift and GST exemption after 2025 to $15 million, adjusted for inflation. |
| `IRS_RP2532` | Internal Revenue Service | Revenue Procedure 2025-32 (2026 inflation adjustments) | https://www.irs.gov/pub/irs-drop/rp-25-32.pdf | 2026 long-term capital gain 0%/15% thresholds (MFJ $98,900 / $613,700); 2026 annual gift exclusion $19,000; estates/trusts 20% rate above $16,250. |
| `IRS_I706` | Internal Revenue Service | Instructions for Form 706 (07/2026) | https://www.irs.gov/instructions/i706 | Estate tax is levied on the entire taxable estate, not on a beneficiary's share; top unified rate 40%; estate/GST tax due within 9 months. |
| `IRS_P551` | Internal Revenue Service | Publication 551, Basis of Assets | https://www.irs.gov/publications/p551 | Basis of inherited property is generally FMV at date of death (or alternate valuation date); §1014(f) consistency rule. |
| `IRS_INHERIT_FAQ` | Internal Revenue Service | Gifts & inheritances (IRS FAQ) | https://www.irs.gov/faqs/interest-dividends-other-types-of-income/gifts-inheritances/gifts-inheritances | Inherited-property basis is FMV at death whether or not Form 706 is filed; gain on later sale is taxable. |
| `IRS_P525` | Internal Revenue Service | Publication 525, Taxable and Nontaxable Income | https://www.irs.gov/publications/p525 | Generally, property received as a gift, bequest or inheritance is not included in income; later interest, dividends or rents are taxable. |
| `IRS_TC701` | Internal Revenue Service | Topic no. 701, Sale of your home | https://www.irs.gov/taxtopics/tc701 | §121 exclusion up to $250,000 ($500,000 joint); ownership and use 2 of the 5 years before sale; no exclusion if another home was excluded in prior 2 years. |
| `IRS_P523` | Internal Revenue Service | Publication 523, Selling Your Home | https://www.irs.gov/publications/p523 | Rules for home inherited from a decedent; business or rental use, nonqualified use after 2008, and basis adjustments. |
| `IRS_TC409` | Internal Revenue Service | Topic no. 409, Capital gains and losses | https://www.irs.gov/taxtopics/tc409 | 0% / 15% / 20% rates; 25% maximum on unrecaptured §1250 gain; short-term gains at ordinary rates. |
| `IRS_TC559` | Internal Revenue Service | Topic no. 559, Net investment income tax | https://www.irs.gov/taxtopics/tc559 | 3.8% NIIT; $250,000 MFJ / $200,000 single MAGI thresholds; rents and gains from real estate generally included; §121-excluded gain is not. |
| `IRS_P527` | Internal Revenue Service | Publication 527, Residential Rental Property | https://www.irs.gov/publications/p527 | Rental income, deductible expenses, depreciation, repairs vs. improvements, and sale of a main home used as rental property. |
| `IRS_FS1031` | Internal Revenue Service | Like-Kind Exchanges Under IRC Section 1031 (FS-2008-18) | https://www.irs.gov/pub/irs-news/fs-08-18.pdf | §1031 applies only to business/investment real property; primary residences, stocks, bonds, notes and securities do not qualify. |
| `IRS_P544` | Internal Revenue Service | Publication 544, Sales and Other Dispositions of Assets | https://www.irs.gov/publications/p544 | Like-kind exchange nonrecognition rules apply only to real property held for investment or business use. |
| `IRS_TC503` | Internal Revenue Service | Topic no. 503, Deductible taxes | https://www.irs.gov/taxtopics/tc503 | SALT deduction limited to $40,000 ($20,000 MFS), subject to MAGI limitation, floor $10,000. |
| `IRS_SALT2026` | Internal Revenue Service | Correction to 2026 Form 1040-ES SALT amount | https://www.irs.gov/forms-pubs/correction-to-state-and-local-income-tax-deduction-amount-in-the-2026-form-1040-es | 2026 SALT limit $40,400 ($20,200 MFS); reduced above MAGI $505,000 ($252,500 MFS); floor $10,000. |
| `IRS_F1041ES` | Internal Revenue Service | Form 1041-ES 2026, Estimated Income Tax for Estates and Trusts | https://www.irs.gov/pub/irs-pdf/f1041es.pdf | 2026 estates/trusts: 20% capital-gain rate above $16,250; NIIT 3.8% on undistributed net investment income. |
| `IRS_P559` | Internal Revenue Service | Publication 559, Survivors, Executors and Administrators | https://www.irs.gov/publications/p559 | Duties of the personal representative, final Form 1040, Form 56, and estate/trust income tax reporting. |
| `FED_FOMC` | Federal Reserve | Statement on Longer-Run Goals and Monetary Policy Strategy (reaffirmed 2026) | https://www.federalreserve.gov/monetarypolicy/files/FOMC_LongerRunGoals.pdf | FOMC longer-run inflation goal is 2 percent (PCE). This is a policy goal, not a forecast through 2050. |
| `FHFA_HPI` | Federal Housing Finance Agency | FHFA House Price Index datasets | https://www.fhfa.gov/data/hpi/datasets | Official repeat-sales house price indexes at metro-area, county and ZIP-code level; used as the official anchor for appreciation scenarios. |
| `HUD_FMR` | U.S. Department of Housing and Urban Development | FY 2026 Schedule of Fair Market Rents | https://www.huduser.gov/portal/datasets/fmr/fmr2026/FY2026_FMR_Schedule.pdf | CA metropolitan FMRs: San Jose-Sunnyvale-Santa Clara HMFA 4-BR $5,010/mo; San Francisco HMFA 4-BR $4,770/mo (official figure, rounded to the nearest $10). Program benchmark, not a property appraisal. |
| `COURTS_TRUST` | California Courts (Santa Clara County Superior Court) | Probate Trusts — trustee duties when the settlor dies | https://santaclara.courts.ca.gov/self-help/self-help-topics/self-help-probate/self-help-probate-property-transfers/probate-trusts | Successor trustee acceptance; written notice to beneficiaries/heirs within 60 days; inventory and appraisal; estate tax returns and payment within 9 months; new trust TIN; trust income tax returns. |
| `COURTS_LIVING` | California Courts (Santa Clara County Superior Court) | Living Trusts (self-help) | https://santaclara.courts.ca.gov/self-help/self-help-probate/self-help-probate-medicalfinancialend-life-issues/living-trusts | A funded living trust avoids probate; successor trustee distributes without court supervision; pour-over will used for unfunded assets. |
| `BOE_PROP19` | California State Board of Equalization | Proposition 19 (official BOE page and comparison charts) | https://www.boe.ca.gov/prop19/ | Current law: principal residence of transferor AND transferee; value limit of current taxable value + $1,000,000 (biennially adjusted); homeowners' exemption within 1 year; claim within 3 years; R&T Code §63.2. |
| `BOE_P801` | California State Board of Equalization | Proposition 19 Fact Sheet (Publication 801) | https://www.boe.ca.gov/pdf/pub801.pdf | Date of death is the date of transfer; transferee must occupy as principal residence within 1 year; adjusted value limit $1,044,590 for 2/16/2025-2/15/2027; forms BOE-19-P, BOE-19-G, BOE-266, BOE-261-G. |
| `BOE_P800_9` | California State Board of Equalization | Death of a Real Property Owner — Reporting Requirements (Publication 800-9) | https://www.boe.ca.gov/pdf/pub800-9.pdf | Death is a change in ownership as of date of death even when property is held in a trust; BOE-502-D filed within 150 days; BOE-19-P / BOE-19-G / BOE-58-H claims; reassessment to market value unless an exclusion applies. |
| `BOE_P800_10` | California State Board of Equalization | How Property Is Assessed for Property Tax Purposes (Publication 800-10) | https://boe.ca.gov/pdf/pub800-10.pdf | Assessed value less exemptions multiplied by the tax rate; homeowners' exemption reduces assessed value by $7,000. |
| `BOE_502D` | California State Board of Equalization | Sample BOE-502-D, Change in Ownership Statement — Death of a Real Property Owner | https://www.boe.ca.gov/proptaxes/pdf/sample-boe502d.pdf | Trustee/transferee files within 150 days of death; 18 CCR 462.260(c) sets date of change in ownership at date of death. |
| `SCC_PROP13` | Santa Clara County Assessor | Understanding Proposition 13 | https://asr.santaclaracounty.gov/faq/understanding-proposition-13 | 1% rate limit, assessed-value growth no greater than 2% annually, reassessment at market value on change of ownership; additional voter-approved taxes may raise the rate. |
| `SCC_RATEBOOK` | Santa Clara County Controller-Treasurer | Property Tax Rate Book (archive, incl. FY2025-26) | https://controller.santaclaracounty.gov/property-tax-distribution/property-tax-rate-book | Official TRA-specific rates; 816 tax rate areas in FY2025-26; 1.00000% maximum levy plus voter-approved bond rates; supplemental bills after change in ownership. |
| `SCC_RATEPDF` | Santa Clara County Controller-Treasurer | County of Santa Clara Compilation of Tax Rates & Information, FY2025-2026 | https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf | 1.00000% maximum levy plus bond rates; assessed value increases by CCPI or 2%, whichever is less; direct/special assessments are separate. |
| `SCC_ANNUAL` | Santa Clara County Assessor | Santa Clara County Assessor Annual Report 2025-2026 | https://www.sccassessor.org/edocman/AnnualReport2025-2026.pdf | 2025-26 CCPI 2.514% produced the maximum 2% assessed-value increase; death of an owner is a reassessable change in ownership; trust-held property reassessed at date of death. |
| `SF_ASSESSOR` | San Francisco Assessor-Recorder | Learn about real property assessments | https://www.sfassessor.org/property-information/homeowners/real-property-assessments | 1% rate plus voter-approved bond indebtedness and direct assessments; assessment growth capped at inflation or 2%, whichever is lower. |
| `SF_TREASURER` | San Francisco Treasurer & Tax Collector | Secured Property Taxes | https://sftreasurer.org/property/secured-property-taxes | FY2026-27 secured property tax rate 1.18162182%; supplemental and escape assessments after a change in ownership; total due includes direct charges/special assessments. |
| `SCO_ESTATE` | California State Controller's Office | California Estate Tax | https://www.sco.ca.gov/ardtax_estate_tax.html | For decedents dying on or after January 1, 2005, no California Estate Tax Return is required. |
| `SCO_RTC13301` | California State Controller's Office | Estate Tax and GST Tax Laws (R&T Code §13301) | https://www.sco.ca.gov/Files-ARD-Tax-Info/estate_lawreg_lawreg.pdf | §13301: neither the state nor any political subdivision may impose any gift, inheritance, succession, legacy, income or estate tax on a transfer occurring by reason of death. |
| `FTB_FEDCHANGES` | California Franchise Tax Board | Summary of Federal Income Tax Changes | https://www.ftb.ca.gov/about-ftb/data-reports-plans/summary-of-federal-income-tax-changes/index.html | California does not provide special rates for net capital gain; gains are taxed at ordinary income rates of 1% to 12.3%. |
| `FTB_RATES` | California Franchise Tax Board | 2025 California Tax Rate Schedules | https://www.ftb.ca.gov/forms/2025/2025-540-tax-rate-schedules.pdf | Top California personal income tax rate 12.30% on the highest bracket. |
| `FTB_540ES` | California Franchise Tax Board | 2025 Instructions for Form 540-ES | https://www.ftb.ca.gov/forms/2025/2025-540-es-instructions.html | Additional 1% tax on California taxable income over $1,000,000 (Behavioral Health Services Tax), making the top marginal rate 13.3%. |
| `SOS_BALLOT` | California Secretary of State | Qualified Statewide Ballot Measures — November 3, 2026 | https://www.sos.ca.gov/elections/ballot-measures/qualified-ballot-measures | 14 measures qualified, including Prop. 3 (extends high-income tax), Prop. 40 (one-time tax on certain taxpayers), Prop. 42 (prohibits new state personal property taxes), Prop. 43 (limits local revenue measures). |
| `SOS_CERTIFIES` | California Secretary of State | Secretary of State certifies measures for Nov. 3, 2026 ballot | https://www.sos.ca.gov/administration/news-releases-and-advisories/2026-news-releases-and-advisories/california-secretary-state-shirley-n-weber-phd-certifies-measures-november-3-2026-general-election-ballot | Prop. 3 would make permanent the 2012 high-income tax rates otherwise expiring in 2031; estimated $5B-$15B annual state income tax maintained. |
| `SOS_PROP40` | California Secretary of State | Official Voter Information Guide — Proposition 40 | https://voterguide.sos.ca.gov/propositions/40/ | One-time tax measure; SOS news release describes up to 5% on covered assets over $1 billion, excluding real property. |
| `SOS_RESULTS_FAQ` | California Secretary of State | Election results FAQ — November 3, 2026 | https://electionresults.sos.ca.gov/frequently-asked-questions | County results due December 4, 2026; Secretary of State compiles and certifies results by December 11, 2026. |
| `SF_RENT` | City and County of San Francisco (Rent Board) | Learn about rent increases in San Francisco | https://www.sf.gov/learn-about-rent-increases-san-francisco/ | For covered units the allowable annual rent increase effective March 1, 2026 through February 28, 2027 is 1.6%. |
| `CDI_AVG` | California Department of Insurance | Sustainable Insurance Strategy — California market snapshot | https://www.insurance.ca.gov/01-consumers/180-climate-change/sustainable-insurance-strategy.Cfm | California average homeowner premium $1,570 (national $1,510); page updated October 27, 2026. Statewide average, not ZIP-specific. |
| `CDI_REPORT` | California Department of Insurance | Residential Property Insurance Report | https://www.insurance.ca.gov/0400-news/0200-studies-reports/0250-homeowners-study/ | CDI collects ZIP-code-level earned premiums, coverage amounts and losses by policy form; reports cover dwelling-fire, homeowners multi-peril, renters and condo policies. |
| `CDI_TOOL` | California Department of Insurance | 2026 Homeowners Insurance premium comparison tool | https://interactive.web.insurance.ca.gov/apex_extprd/f?p=111:21:::NO::: | Annual premiums effective May 1, 2026; lists 'SANTA CLARA CUPERTINO' and 'SAN FRANCISCO SAN FRANCISCO-Sunset District'; explicitly not a quote. |
| `CPUC_SB695` | California Public Utilities Commission | 2025 Senate Bill 695 Report (net energy metering) | https://www.cpuc.ca.gov/-/media/cpuc-website/divisions/office-of-governmental-affairs-division/reports/2025/2025-sb-695-report_093025.pdf | New solar customers from April 2023 receive the Net Billing Tariff; NEM 1.0/2.0 legacy 20-year periods remain in effect when a property with a NEM system changes hands. |
| `CPUC_VNEM` | California Public Utilities Commission | Virtual Net Energy Metering / Net Billing Tariff | https://www.cpuc.ca.gov/industries-and-topics/electrical-energy/demand-side-management/customer-generation/virtual-net-metering | Decision D.22-12-056 adopted the net billing tariff; NEM 2.0 sunset April 14, 2023; legacy period rules. |
| `CPUC_WATER` | California Public Utilities Commission | San Jose Water Company tariff (Cupertino service territory) | https://docs.cpuc.ca.gov/PublishedDocs/Efile/G000/M359/K001/359001611.PDF | CPUC tariff schedules list 'portions of Cupertino' in the regulated water service territory; meter and quantity rates are tariff-based, not a fixed monthly bill. |
| `SFPUC_RATES` | San Francisco Public Utilities Commission | Rates Schedules and Fees (2026-27 water, sewer, power) | https://sfpuc.org/accounts-services/water-power-and-sewer-rates | Official rate schedules for water/sewer and Hetch Hetchy Power / CleanPowerSF. |
| `SFPUC_218` | San Francisco Public Utilities Commission | Proposition 218 notice for proposed water and sewer rates | https://sfpuc.org/accounts-services/water-power-sewer-rates/proposition-218-notice-proposed-water-and-sewer-rates | Approved average single-family water/sewer bill increase of about 8.3% per year; rates are set by tariff, not by a fixed monthly bill. |

## Table register (line by line)

| Table | Rows | Every row carries official link | Status classes present |
| --- | --- | --- | --- |
| `inputs` — Anonymous client-supplied inputs (all unverified) | 16 | YES | CLIENT INPUT — UNVERIFIED |
| `history` — Client-supplied tax and assessment history (unverified) | 23 | YES | CLIENT INPUT — UNVERIFIED |
| `federal_law` — Federal law and official figures (verified) | 20 | YES | VERIFIED |
| `state_law` — California, county and city law and official figures (verified) | 24 | YES | VERIFIED |
| `assumption_values` — Model parameter values (labelled model outputs, not official figures) | 21 | YES | MODEL OUTPUT — NOT AN OFFICIAL VALUE |
| `proj_value` — Property A — projected market value and taxable assessed value, 2026-2050 | 25 | YES | MODEL OUTPUT — NOT AN OFFICIAL VALUE |
| `proj_tax` — Property A — projected annual property tax under three assessment outcomes | 25 | YES | MODEL OUTPUT — NOT AN OFFICIAL VALUE |
| `prop19` — Proposition 19 value-limit test at each candidate transfer year | 3 | YES | MODEL OUTPUT — NOT AN OFFICIAL VALUE |
| `cost_a` — Property A — projected annual carrying costs (base preserved) | 6 | YES | MODEL OUTPUT — NOT AN OFFICIAL VALUE |
| `cost_b` — Property B — projected operating costs and rental cash flow | 6 | YES | MODEL OUTPUT — NOT AN OFFICIAL VALUE |
| `process` — Step-by-step inheritance of Property A through a trust | 18 | YES | VERIFIED |
| `estate_threshold` — Inheritance / estate tax thresholds and projected headroom | 5 | YES | MODEL OUTPUT — NOT AN OFFICIAL VALUE, VERIFIED |
| `estate_matrix` — Illustrative federal estate tax by gross estate size (2026 law) | 8 | YES | MODEL OUTPUT — NOT AN OFFICIAL VALUE |
| `law_changes` — Enacted, pending and proposed law changes that could alter the decision | 11 | YES | VERIFIED |
| `decision` — Three options compared at each candidate transfer year (base case) | 9 | YES | MODEL OUTPUT — NOT AN OFFICIAL VALUE |
| `ranking` — 2045 base-case ranking by 10-year wealth | 3 | YES | MODEL OUTPUT — NOT AN OFFICIAL VALUE |
| `sensitivity` — Sensitivity of 10-year wealth to appreciation and portfolio return | 18 | YES | MODEL OUTPUT — NOT AN OFFICIAL VALUE |
| `breakeven` — Break-even and tax-friction numbers behind the recommendation | 7 | YES | MODEL OUTPUT — NOT AN OFFICIAL VALUE, VERIFIED |
| `property_b` — Property B — the low-cost residence anchor | 4 | YES | MODEL OUTPUT — NOT AN OFFICIAL VALUE |
| `flags_table` — Flagged for Review — all unverified values and irregularities | 20 | YES | CLOSED, FLAGGED — UNVERIFIED |
| `sources_table` — Official source registry (all links retrieved and read 2026-11-10 UTC) | 54 | YES | VERIFIED |

## Flagged irregularities

See `docs/flagged.html` (published) and `data/site_data.json` → `flags`.

| Flag | Severity | Status | Official source |
| --- | --- | --- | --- |
| FLAG-001 — Single fixed working branch | Process | needs review | https://www.sos.ca.gov/elections/ballot-measures/qualified-ballot-measures |
| FLAG-002 — No personal information published | Privacy | closed | https://asr.santaclaracounty.gov/faq/understanding-proposition-13 |
| FLAG-003 — Client tax/assessment pairs do not reconcile to an official rate | Data quality | needs review | https://sftreasurer.org/property/secured-property-taxes |
| FLAG-004 — Property A primary-residence insurance premium unverified | Insurance | needs review | https://interactive.web.insurance.ca.gov/apex_extprd/f?p=111:21:::NO::: |
| FLAG-005 — Property B landlord / rental dwelling insurance unverified | Insurance | needs review | https://www.insurance.ca.gov/0400-news/0200-studies-reports/0250-homeowners-study/ |
| FLAG-006 — Water, electricity and solar credit figures are client estimates | Utilities | needs review | https://www.cpuc.ca.gov/-/media/cpuc-website/divisions/office-of-governmental-affairs-division/reports/2025/2025-sb-695-report_093025.pdf |
| FLAG-007 — Maintenance and repair cost assumption unverified | Costs | needs review | https://www.irs.gov/publications/p527 |
| FLAG-008 — Appreciation and portfolio-return scenarios are not official forecasts | Model | needs review | https://www.fhfa.gov/data/hpi/datasets |
| FLAG-009 — 2% inflation is a policy goal, not a 25-year forecast | Model | needs review | https://www.federalreserve.gov/monetarypolicy/files/FOMC_LongerRunGoals.pdf |
| FLAG-010 — Prop 19 eligibility is unconfirmed | Critical | needs review | https://www.boe.ca.gov/pdf/pub800-9.pdf |
| FLAG-011 — Future Prop 19 allowance amounts are projected | Model | needs review | https://www.boe.ca.gov/pdf/pub801.pdf |
| FLAG-012 — Beneficiary-level income tax not fully computed in cash-flow comparisons | Tax | needs review | https://www.irs.gov/taxtopics/tc559 |
| FLAG-013 — Estate size is unquantified | Critical | needs review | https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax |
| FLAG-014 — November 3, 2026 California ballot results not certified | Law change | needs review | https://electionresults.sos.ca.gov/frequently-asked-questions |
| FLAG-015 — All projections are model outputs, not official values | Verification | closed | https://asr.santaclaracounty.gov/faq/understanding-proposition-13 |
| FLAG-016 — SF rent-control coverage of the two let units is unconfirmed | Rent | needs review | https://www.sf.gov/learn-about-rent-increases-san-francisco/ |
| FLAG-017 — Property A 2026 tax bill supplied as '--' | Data quality | needs review | https://controller.santaclaracounty.gov/property-tax-distribution/property-tax-rate-book |
| FLAG-018 — HUD Fair Market Rent is a program benchmark, not a market appraisal | Rent | needs review | https://www.huduser.gov/portal/datasets/fmr/fmr2026/FY2026_FMR_Schedule.pdf |
| FLAG-019 — 6% selling-cost assumption unverified | Model | needs review | https://www.irs.gov/publications/p523 |
| FLAG-020 — SB 284 (2025) status not verified against an official bill-status page | Law change | needs review | https://www.boe.ca.gov/prop19/ |

## Manual review instructions

1. Open any page of the live site and click the source link in the last column of any row.
2. Compare the recorded value with the official page text.
3. For client inputs, the official-value cell is intentionally blank; obtain the record from the linked agency.
4. For model outputs, see `model/build_data.py` — every parameter and formula is in that file.
5. Discrepancies or newly verified values should be added to `COORDINATION.md` and the Flagged for Review page.
