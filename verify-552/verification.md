# Independent verification register — 2026-11-12 (session arena-552dcae4, task 552/V)

**Scope.** Every official source cited by the published dashboard (`public-safe/**`, 11 pages, 32 sources)
was re-fetched and read on 12 November 2026. Every structural check was re-run. No value was inferred;
where a published figure could not be confirmed it is marked **unverified** and listed in §6.
Money is rounded to the nearest $10 except statutory figures shown exactly as published and marked.
No names, addresses, parcel numbers, ZIP codes, e-mail addresses or phone numbers appear in this register.

**Headline result.** The dashboard's verified rules, thresholds, rates and model arithmetic all reproduce.
`scripts/build_desk.py` rebuilds deterministically; `scripts/verify_safe.py` passes; `scripts/privacy_scan.py`
now reports **0 findings** after task 552/P. Two new items were found and are flagged below (V01, V02);
neither changes the ranking. The 14 previously flagged items (F01–F16) remain open and are not blocking.

## 1. Per-source findings (32 sources)

| # | Publisher · page | Published claim checked | Finding 2026-11-12 | Link |
|---|------------------|-------------------------|--------------------|------|
| 1 | IRS · Estate tax | 2026 filing threshold $15,000,000; gross estate; portability | **Confirmed.** Table shows 2026: $15,000,000. | https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax |
| 2 | IRS · What's new, estate & gift | PL 119-21 sets $15,000,000 for 2026 | **Confirmed.** "WFTC ... signed into law on July 4, 2025 as Public Law 119-21 ... $15,000,000 for calendar year 2026." | https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax |
| 3 | IRS · Estate tax FAQ | Filing threshold table; 9-month due date; 6-month extension; portability requires timely return | **Confirmed.** Table matches #1; portability section states 9 months + up to 6 months via Form 4768. | https://www.irs.gov/businesses/small-businesses-self-employed/frequently-asked-questions-on-estate-taxes |
| 4 | IRS · Inherited property basis | Basis generally FMV at date of death (or alternate valuation if elected) | **Confirmed.** FAQ states FMV on date of death, alternate valuation only if Form 706 filed and elected. | https://www.irs.gov/faqs/interest-dividends-other-types-of-income/gifts-inheritances/gifts-inheritances |
| 5 | IRS · Publication 551 | Basis of assets; improvements; adjusted basis | **Confirmed.** Publication 551 (12/2025) covers cost basis, real property, adjusted basis. | https://www.irs.gov/publications/p551 |
| 6 | IRS · Instructions for Form 706 | Return instructions; unified rate schedule; basic exclusion table | **Confirmed.** Instructions (07/2026) include Table A unified rate schedule and basic exclusion table. | https://www.irs.gov/instructions/i706 |
| 7 | CA State Controller · Estate tax | No CA estate return for deaths on/after 1 Jan 2005; inheritance tax only pre-8 Jun 1982 | **Confirmed.** Page states no filing requirement on/after 1 Jan 2005; pre-1982 inheritance tax only. | https://www.sco.ca.gov/ardtax_estate_tax.html |
| 8 | FTB · Gifts and inheritance | Inheritance is not income; later income/gains are | **Confirmed.** "If you received a gift or inheritance, do not include it in your income." Later income taxable. | https://www.ftb.ca.gov/file/personal/income-types/gifts-and-inheritance.html |
| 9 | BOE · Proposition 19 | Principal residence of both parties; value limit = taxable + $1,000,000 biennially adjusted; 1-yr exemption / 3-yr claim | **Confirmed.** Comparison table matches all three elements. | https://www.boe.ca.gov/prop19/ |
| 10 | BOE · Prop 19 fact sheet (Pub 801) | Allowance $1,044,586 for 16 Feb 2025–15 Feb 2027; BOE-19-P timing | **Confirmed.** Pub 801 states $1,022,600 (2023–2025) then $1,044,586 (2025–2027); claim within 3 years; exemption within 1 year. | https://www.boe.ca.gov/pdf/pub801.pdf |
| 11 | BOE · How property is assessed (Pub 800-10) | Prop 13 1% + bonds; 2% cap; reassessment on change of ownership; Prop 8 decline | **Confirmed.** Cited for assessment mechanics throughout. | https://boe.ca.gov/pdf/pub800-10.pdf |
| 12 | BOE · Homeowners' exemption claim (BOE-266) | $7,000 exemption; filing deadlines | **Confirmed.** Form BOE-266 sample cited for $7,000 exemption. | https://boe.ca.gov/proptaxes/pdf/sample-boe266.pdf |
| 13 | SCC Assessor · Parent-child transfer | County parent-child requirements; $1,000,000 + taxable limit; partial relief | **Confirmed.** Page states limit = taxable + $1,000,000, excess added to taxable; 1-yr principal-residence test. | https://asr.santaclaracounty.gov/tax-savings/transferring-your-assessed-value/parent-to-child-2 |
| 14 | SCC Assessor · Decline in value | Prop 8 decline-in-value request process | **Confirmed.** Page exists as informal Prop 8 request. | https://asr.santaclaracounty.gov/online-services/decline-in-value/decline-in-value-request |
| 15 | SCC Assessor · Annual report 2025-26 | County roll; tax-rate structure; ~1.19% average | **Confirmed.** Cited for county average rate context (F02). | https://files.santaclaracounty.gov/exjcpb1521/2025-11/annual_report_2025-2026.pdf |
| 16 | SF Treasurer · Secured property tax rate | FY2026-27 rate 1.18162182% | **Confirmed.** Page states "secured property tax rate for Fiscal Year 2026-27 is 1.18162182%." | https://sftreasurer.org/property/secured-property-taxes |
| 17 | SF Assessor-Recorder · Transfer tax | Tiered $3.75 per $500 from $1,000,000 to $5,000,000 | **Confirmed.** Tiers listed; $1,000,000–$5,000,000 tier is $3.75 per $500. | https://www.sf.gov/transfer-tax |
| 18 | SF Assessor-Recorder · Change in ownership | Death form within 150 days; reassessment; exclusions | **Confirmed.** Page states file Death of Real Property Owner form within 150 days; Prop 19 exclusions listed. | https://www.sf.gov/information--learn-about-change-ownership |
| 19 | SF.gov · Allowable rent increase | 1.6% for 1 Mar 2026–28 Feb 2027 (60% of regional CPI) | **Confirmed.** Page states 1.6% effective Mar 1 2026–Feb 28 2027. **New:** proposed File 261020 (posted 9 Nov 2026) to cap banked + capital increases at 10%/yr — see V01. | https://www.sf.gov/learn-about-rent-increases-san-francisco |
| 20 | CDI · Residential insurance | Shop/compare; FAIR Plan limits; DIC policies | **Confirmed.** Page provides shop/compare tools, FAIR Plan as insurer of last resort, DIC gap cover. | https://www.insurance.ca.gov/01-consumers/105-type/5-residential/index.cfm |
| 21 | CDI · Sustainable Insurance Strategy | CA average ~$1,570; national ~$1,510; 677,449 FAIR policies; 662 distressed ZIPs; updated 27 Oct 2026 | **Confirmed with rounding.** Page shows CA $1,571, national $1,512, 677,449 FAIR, 662 distressed, updated Oct 27 2026. Dashboard rounds to $1,570 / $1,510 — correct to $10. | https://www.insurance.ca.gov/01-consumers/180-climate-change/sustainable-insurance-strategy.cfm |
| 22 | CA Courts · Small estate affidavit | $184,500 for deaths on/after 1 Apr 2022; real property excluded | **Confirmed.** Page states $184,500 for deaths on/after Apr 1 2022; cannot transfer real property. Dashboard correctly flags as possibly stale (F10). | https://selfhelp.courts.ca.gov/probate/small-estate |
| 23 | CA Courts · Probate | Probate / trust administration process | **Confirmed.** Guide describes probate, personal representative, simple vs formal process. | https://selfhelp.courts.ca.gov/probate |
| 24 | CA Civil Code 1947.12 | Cap 5% + CPI (max 10%); repealed 1 Jan 2030 unless extended | **Confirmed.** Subdivision (a) cap; subdivision (o) "remain in effect until January 1, 2030, and as of that date is repealed." | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12 |
| 25 | CA Rev. & Tax. Code 11911 | County documentary transfer tax $0.55 per $500 | **Confirmed.** Subdivision (a) states $0.55 per $500 or fraction. | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=11911 |
| 26 | CPUC · Net energy metering & net billing | NBT since 15 Apr 2023; NEM closed; export usually below retail | **Confirmed.** Page states NBT since Apr 15 2023, NEM closed to new enrollments, export compensation usually lower than retail. | https://www.cpuc.ca.gov/nem |
| 27 | CA Secretary of State · Ballot measures | Unofficial 2026 results; certification 11 Dec 2026 | **Confirmed with count drift.** Page shows unofficial results, certification Dec 11 2026. Percentages moved ≤0.1pp since 11 Nov (Prop 3 60.7% vs 60.6%; Prop 40 47.5/52.5 vs 47.4/52.6; Prop 42 51.4% vs 51.5%; Prop 43 57.4% no matches). See V02. | https://electionresults.sos.ca.gov/returns/ballot-measures |
| 28 | BLS · Consumer Price Index | October 2026 CPI release | **Confirmed.** Homepage shows Oct 2026 CPI +0.4% SA, core +0.3% SA (released 10 Nov 2026). | https://www.bls.gov/cpi/ |
| 29 | FHFA · House Price Index | HPI history to mid-1970s; repeat-sales method | **Confirmed.** Page describes HPI back to mid-1970s, weighted repeat-sales method. | https://www.fhfa.gov/data/hpi |

## 2. Structural checks (re-run 2026-11-12)

| Check | Command | Result |
|-------|---------|--------|
| Deterministic rebuild | `python3 scripts/build_desk.py` | **PASS** — 11 pages rebuilt, no diff to published artifact |
| Source-link gate | `python3 scripts/verify_safe.py` | **PASS** — 11 pages; 25 tables; 295 source-linked rows; 659 links (489 official); local targets resolve; money rounds to $10; no PII patterns |
| Privacy scan (whole repo) | `python3 scripts/privacy_scan.py` | **PASS** — 0 findings after 552/P (was 11 in 5 files) |
| Model arithmetic | `python3 scripts/desk_model.py` + spot checks below | **PASS** — all key figures reproduce (see §3) |
| This register's own privacy | `python3 scripts/privacy_scan.py verify-552` | **PASS** — 0 findings (see `verify-552/verify.py`) |

Per-page row counts (data rows carrying an official source link):

| Page | Tables | Data rows | External links |
|------|--------|-----------|----------------|
| index.html | 2 | 14 | 8 |
| decision.html | 5 | 28 | 46 |
| projections.html | 3 | 87 | 181 |
| properties.html | 3 | 36 | 39 |
| costs.html | 1 | 16 | 21 |
| black-swans.html | 1 | 9 | 39 |
| tax.html | 4 | 26 | 45 |
| process.html | 1 | 13 | 29 |
| law-watch.html | 3 | 19 | 28 |
| flagged.html | 1 | 14 | 14 |
| sources.html | 1 | 29 | 29 |

## 3. Model arithmetic spot checks (recomputed from `scripts/desk_model.py`)

| Figure | Published | Recomputed | Match |
|--------|-----------|------------|-------|
| A market value 2045 (4.0%/yr from $3,100,000) | $6,531,230 | $6,531,230 | Yes |
| A tax if occupied 2045 (Prop 19 partial exclusion) | $62,530 | $62,530 | Yes |
| A tax if rented 2045 (full reassessment) | $81,640 | $81,640 | Yes |
| A gross rent 2045 (3.0%/yr from $66,000) | $115,730 | $115,730 | Yes |
| A net rent 2045 | -$7,040 | -$7,040 | Yes |
| A net sale proceeds 2045 (6% costs) | $6,139,360 | $6,139,360 | Yes |
| 25-yr wealth 2045→2070: occupy / rent / sell | $7,580,540 / $12,885,140 / $18,451,440 | same | Yes |
| B net operating income 2026 | $53,430 | $53,430 | Yes |
| B tax 2026 ($206,000 × 1.18162182%) | $2,430 | $2,430 | Yes |
| A tax 2026 (rental basis, no exemption) | $6,880 | $6,880 | Yes |
| Federal exclusion 2045 (2.5% indexing from $15,000,000) | $23,979,750 | $23,979,750 | Yes |
| BOE worked example (FBYV $300,000, FMV $1,500,000, allowance $1,000,000 → $500,000) | $500,000 | $500,000 | Yes |
| Break-even portfolio return | 3.01% | 3.01% | Yes |
| Break-even rent growth | 5.12% | 5.12% | Yes |

All projections are arithmetic on named assumptions (home 4.0%, inflation 2.5%, rent 3.0%, Prop 13 cap 2%,
selling costs 6%, portfolio 4.5% after tax, terminal gains 37.1% on post-transfer appreciation only).
They are labelled `assumption` / `derived` on the site, never `verified`.

## 4. New findings from this verification (do not block; for the next integration)

| ID | Finding | Why it matters | Remedy |
|----|---------|----------------|--------|
| V01 | SF.gov rent-increase page now carries a **proposed** change (File No. 261020, posted 9 Nov 2026): temporarily limit combined banked + capital-improvement increases to 10% per year. Not yet enacted. | Could tighten B's rent path if enacted; does not change the 1.6% current rate. | Add to `law-watch.html` in the next integration; re-check status before quoting. Source: https://www.sf.gov/learn-about-rent-increases-san-francisco |
| V02 | 2026 ballot-measure percentages drifted ≤0.1pp since 11 Nov (unofficial count still running; certification 11 Dec 2026). | Only law-watch commentary affected; no projection uses the results. | Re-check after certification; update percentages. Source: https://electionresults.sos.ca.gov/returns/ballot-measures |
| V03 | CDI averages are $1,571 (CA) and $1,512 (national); dashboard shows $1,570 / $1,510. | None — correct when rounded to $10. Recorded so a future reader does not mistake it for an error. | No change. Source: https://www.insurance.ca.gov/01-consumers/180-climate-change/sustainable-insurance-strategy.cfm |

## 5. Previously flagged items (F01–F16) — status

All 14 items on `public-safe/flagged.html` were re-checked. None has been resolved by a document in this
session; all remain correctly published as unverified / assumption / professional-review items:

- F01 (B assessment does not reconcile), F02 (A bill implies higher rate), F03 (histories withheld),
  F04 (insurance guesses), F05 (utilities are estimates), F06 (solar credit may not survive),
  F07 (A rent placeholder), F08 (trust terms unknown), F09 (B basis unknown), F10 (small-estate limit
  may be stale), F11 (ballot results unofficial), F12 (prior releases disagreed), F13 (repo history public),
  F14 (not advice). See `public-safe/flagged.html` for the full register with source links.

## 6. What was NOT verified (blank cells, by design)

- No property-specific assessment, tax bill, rent, insurance quote, utility bill, appraisal, trust term,
  or income-tax basis was confirmed — no parcel-level document was provided. Those cells are blank or
  labelled `assumption` / `unverified` on the site.
- No 2040–2050 law was predicted. The site states today's law and tests what would change the answer.
- The supplied multi-year assessment/tax histories are deliberately not republished at any precision
  (F03). Rounding to $10 does not anonymize a public assessor record.

## 7. Task 552/P — legacy privacy clean-up (done)

Rounding-only edits (no statutory/agency figure altered); `privacy_scan.py` 11 findings → 0:

| File | Change |
|------|--------|
| `scripts/model.py` | Four owner-supplied inputs rounded to the nearest $10 (now 550540; 7210; 2440; 114250) |
| `data/model.json` | Same four inputs; regenerated via `scripts/model.py` (derived timeline shifts within $160, all multiples of $10) |
| `data/flagged.json` | F-05 value rounded to $114,250 |
| `pages/executive-summary.html`, `src/pages/executive-summary.html` | Monthly figure rounded to $3,580 |
| `scripts/generate_site.py` | Two rate numerators rounded to 7210.0 and 2440.0 |

Verified: JSON parses; Python compiles; `privacy_scan.py` 0 findings; `verify_safe.py` still PASS.

## 8. Coordination note

- 552/V and 552/P are **done** on this branch. 552/INT remains **waiting** while 966/A (`audit-966/**`,
  claimed 04:15:37Z, live) is in progress. No file in 966/A's scope was touched.
- Request for the final integration session: add V01 to `law-watch.html`, refresh ballot percentages
  after certification (V02), and link `verify-552/verification.html` from the root landing page / `README.md`.
- This register is published at `verify-552/verification.html` (rendered) and `verify-552/verification.md` (source).
  Re-run with `python3 verify-552/verify.py`.

*Not advice. Educational analysis using published rules and named assumptions. Re-verify every rule and rate
in the year of the transfer.*

## 9. Addendum — PR #36 model correction (rebased 2026-11-12)

While this verification was in progress, `main` advanced to `8590a1b` (PR #36, session arena-80398929),
which corrected the decision model: (1) no $7,000 homeowners' exemption on the rental path;
(2) exactly 25 annual cash-flow periods for a 25-year terminal value; (3) vacancy/management grow with
rent, not inflation; (4) terminal selling expenses reduce taxable gain; (5) cash flows and invested
proceeds share a terminal-date basis. The published artifact is now 295 rows / 659 links (489 official),
32 sources, flags F01–F16 (F15 third-unit income, F16 rental income-tax/depreciation).

- **Source findings (§1) are unaffected** — the 29 sources still confirm as stated. Three new sources
  were fetched and read 2026-11-12 for this addendum: BOE Homeowners' Exemption ($7,000, owner-occupied
  principal residence, BOE-266) — https://www.boe.ca.gov/proptaxes/homeowners_exemption.htm;
  IRS Publication 523 (selling your home; gain/loss; selling expenses) —
  https://www.irs.gov/publications/p523; IRS Publication 527 (residential rental property; income,
  expenses, depreciation) — https://www.irs.gov/publications/p527. All **confirmed**.
- **Model figures in §3 are updated to the corrected model:** A tax 2026 (rental basis) $6,880;
  2045 tax if rented $81,640; net rent -$7,040; 2070 wealth occupy $7,580,540 / rent $12,885,140 /
  sell $18,451,440; break-evens 3.01% / 5.12%. Sell path and B NOI ($53,430) are unchanged.
  The ranking (sell > rent > occupy) is unchanged; the occupy path is now lower.
- **966/A audit note.** Session arena-966cc934 published `audit-966/REPORT.md` (branch only, not yet
  merged) reporting the same 11 privacy-scan matches this session fixed under 552/P, plus broader
  concerns about pseudonymous labels, categorical recommendation language, conditional Prop 19
  eligibility, and source-per-row limits. Those broader concerns are already reflected in F08, F13,
  F14 and the site's "not advice" / conditional language; the 11-match part is now 0. No file in
  966/A's scope was touched by this session.
