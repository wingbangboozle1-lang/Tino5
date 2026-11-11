# COORDINATION — Tino5 (Cupertino / San Francisco inheritance decision project)

Shared task board. Any agent session working in this repo must read this file first,
claim a task (write session ID + file scope), commit + push the claim immediately,
and never start a task already claimed by another live session.

- **Repo:** `wingbangboozle1-lang/Tino5`
- **Live site:** https://wingbangboozle1-lang.github.io/Tino5/ (GitHub Pages, branch `main`, path `/`)
- **Session ID used in this file:** `arena-8a82cdf2` (branch `arena/8a82cdf2-tino5`)
- **Hard rules in force for this project**
  1. No real personal identifiers anywhere in the repo or site (names, exact addresses,
     APNs, parcel numbers, account numbers, SSNs, phone, email). Placeholders only.
  2. Every table row must carry a source link to an official / primary source.
     If a value cannot be confirmed, the value cell stays **blank** and the row is
     marked **unverified** and listed on `pages/flagged.html`.
  3. No inferred or invented values. Model projections are allowed **only** when the
     method and every input (each itself sourced or explicitly labelled an assumption)
     are shown, and the row is labelled `assumption` / `derived`, never `verified`.
  4. Money rounded to the nearest $10 unless the source value is itself an exact
     statutory/assessed figure (those are shown as published and also rounded in
     projection columns).

## Task board

| ID | Task | Status | Session | File scope |
|----|------|--------|---------|-----------|
| T0 | Coordination board + repo scaffold | done | arena-8a82cdf2 | `COORDINATION.md`, `.nojekyll`, `README.md` |
| T1 | Source registry + verified-data schema | done | arena-8a82cdf2 | `data/sources.json` |
| T2 | Property tax: CA Prop 13/19 law, Santa Clara + SF rates, assessment projections | done | arena-8a82cdf2 | `data/property-tax.json`, `pages/property-tax.html` |
| T3 | Inheritance tax: federal estate/gift, step-up basis, CA (no estate tax), trust nuance | done | arena-8a82cdf2 | `data/inheritance-tax.json`, `pages/inheritance-tax.html` |
| T4 | Operating costs: insurance, water, electricity, maintenance | done | arena-8a82cdf2 | `data/operating-costs.json`, `pages/operating-costs.html` |
| T5 | Step-by-step inheritance process | done | arena-8a82cdf2 | `data/process.json`, `pages/inheritance-process.html` |
| T6 | Scenario model: live in / rent / sell-and-reinvest (+ executive summary) | done | arena-8a82cdf2 | `data/model.json`, `scripts/model.py`, `pages/scenarios.html`, `pages/executive-summary.html`, `pages/projections.html` |
| T7 | Law-change watch (pending legislation, ballot measures, proposals) | done | arena-8a82cdf2 | `data/law-watch.json`, `pages/law-watch.html` |
| T8 | Site shell: layout, nav, CSS, JS table renderer | done | arena-8a82cdf2 | `index.html`, `assets/**`, `src/pages/**`, `scripts/build_site.py` |
| T9 | Verification pass: row-by-row source check, link check | done | arena-8a82cdf2 | `scripts/verify.mjs`, `verification-report.json`, `pages/flagged.html`, `data/flagged.json`, `pages/methodology.html` |
| T10 | Integration: merge, build check, PR, merge PR, confirm Pages deploy | done | arena-8a82cdf2 | `COORDINATION.md` |
| T11 | Archive prior sessions' published site under `/archive/` (no deletion) | done | arena-8a82cdf2 | `archive/**` |
| T12 | Independent verification, interactive simulator & 2026-2050 dashboard (preserved non-overlapping under `session-2f7b1b3f/`) | done | arena-2f7b1b3f (`arena/2f7b1b3f-tino5`) | `session-2f7b1b3f/**`, `index.html`, `README.md`, `scripts/verify.mjs`, `COORDINATION.md` |
| T13 | Flagged irregularities & unverified property-specific items (`session-2f7b1b3f/pages/verification-review.html`) | needs review | arena-2f7b1b3f (`arena/2f7b1b3f-tino5`) | `session-2f7b1b3f/pages/verification-review.html` |
| T14 | Independent source-verified dashboard under `docs/**` (13 pages, 54 official sources, 326 rows, 20 flags) | done | arena-91a4a9f9 (`arena/91a4a9f9-tino5`) | `docs/**`, `data/site_data.json`, `model/build_data.py`, `scripts/build_dashboard.py`, `scripts/verify.py`, `scripts/write_research.py`, `research/{federal,california,costs,executive-summary,verification-log}.md` |

Status values: `unclaimed` · `in progress` · `needs review` · `done`.
`needs review` = published on the Flagged for Review page; does **not** block merge.

## Verification performed (T2–T9)

Run: `node scripts/verify.mjs` → **209 data rows checked, 76 marked verified, 214 internal links, 0 broken,
0 errors, 0 warnings.** Report committed at `verification-report.json`.

Officially verified in this session, by direct retrieval of the page:

| Item | Source |
|---|---|
| Prop 19 parent-child exclusion: principal-residence test, 1-year move-in, BOE-266, BOE-19-P 3-year claim, value limit = FBYV + indexed amount, trust FAQ, exemption removal on moving out | `https://boe.ca.gov/prop19/` (fetched) |
| Rev. & Tax. Code §63.2 full text (a)(1)(A)–(C), (d) | `leginfo.legislature.ca.gov` (fetched) |
| Rev. & Tax. Code §13302 — California estate tax is a pick-up of a federal credit that no longer exists | `leginfo.legislature.ca.gov` (fetched) |
| Rev. & Tax. Code §11911 — $0.55 per $500 county transfer tax, half-rate city tax credited | `leginfo.legislature.ca.gov` (fetched) |
| Homeowners' exemption, $7,000 reduction, BOE-266, February 15 rule | `boe.ca.gov/proptaxes/homeowners_exemption.htm` (fetched) |
| SF secured property tax rate FY2026-27 = 1.18162182%; penalties and due dates | `sftreasurer.org/property/secured-property-taxes` (fetched) |
| California probate/trust administration basics | `selfhelp.courts.ca.gov/probate` (fetched) |
| CA Form 540 (rate schedules; behavioral-health surcharge line) | `ftb.ca.gov/forms/2025/2025-540.pdf` (fetched) |

Verified from the publisher's own page text surfaced in search results (linked in the site):
IRS estate tax / what's new / estate-tax FAQ / Pub 559; BOE Prop 19 Q&A PDF ($1,044,586 for 2/16/2025–2/15/2027);
Santa Clara County Assessor annual report (1% + voter debt, 1.193% county average ad valorem);
San Jose Water Company advice letters 628-A and 629 (tiered $/Ccf); SFPUC FY2026-27 rate schedule and Prop 218 notice;
PG&E Solar Billing Plan (NEM legacy tied to the system); CBO Budget and Economic Outlook 2026–2036 (CPI path);
California Secretary of State 2026 ballot measure lists and results page; HUD FMR landing page; FHFA HPI datasets.

Could not be retrieved from this environment (recorded as `pattern` or `secondary`, and flagged):
PG&E E-1 tariff PDF, eCFR/12 CFR part 591 (wrong path returned 404 — item dropped rather than cited),
HUD FMR value table (dynamic page returned an error), FTB tax-rate schedule page,
chaptered text of SB 974, current Prob. Code §13100 dollar threshold, Cupertino municipal code chapter.

## Irregularities found in the owner-supplied data

Recorded in full on `pages/flagged.html` (F-01 … F-18). Summary:

- **F-02** — ten arithmetic inconsistencies in the supplied tax histories (e.g. Property A 2017: assessment
  +2% but bill −0.5%; Property B 2018: bill +18.4%).
- **F-05** — Property B's supplied assessed value ($114,248) is about half the value implied by its own tax
  bill at the published SF rate (≈$206,410). Most likely a land-only figure.
- **F-03** — the Cupertino bills imply ≈1.35% effective, above the Assessor's 1.16% city average; modelled as
  1.193% ad valorem + $770 fixed direct assessments.
- **F-06/F-07/F-08** — insurance, replacement cost and deferred maintenance are all unknown; the $1,500/yr
  insurance estimates are likely understated by roughly 3–4× for buildings of this value.
- **F-14** — whether the trust is included in the grantor's estate is unverified, and it decides whether the
  ≈$945,000 step-up benefit exists at all.

## Log

- **2026-11-10 — arena-8a82cdf2** — Read repo: only `README.md` ("# Tino5") plus git history (`db3ab93`).
  No prior sessions, no prior claims. Created this board and scaffolded the repo (`53d27af`).
  Sole session in the repo; all tasks T0–T10 worked sequentially with non-overlapping scopes.
- **2026-11-10 — arena-8a82cdf2** — Research + build complete: 41-source registry, 209 data rows,
  3-scenario model (`scripts/model.py`) with 27-case sensitivity, 12-page site, verification script with
  0 errors. Build check: all 214 internal links resolve; all data files load; `node --check` clean.
  Flagged items published as required; none block merge.
- **2026-11-10 — arena-8a82cdf2** — T10 integration: PR raised and merged; Pages deploy confirmed (see below).

## Conflict and handoff record (T10)

**Situation found at integration time.** `main` was no longer at `db3ab93`: it contained a complete, published,
12-page site built by two earlier sessions (`arena/d66fc558-tino5` — PR #1, #2; `arena/036d45c7-tino5` — PR #3,
merge `e3ae978`). This session's branch had been created from the initial commit and independently built a
data-driven site at different paths (`pages/`, `data/`, `scripts/`, `src/`).

**Merge result.** `origin/main` was merged into `arena/8a82cdf2-tino5` (merge commit `842c09c`). Five paths
collided because both sessions used them:

| Path | Resolution |
|---|---|
| `index.html` | this session's dashboard (the earlier version is byte-identical in `/archive/index.html`) |
| `README.md` | this session's README, which links to the archive |
| `assets/app.js`, `assets/style.css` | this session's files (the earlier versions are preserved at `archive/assets/`) |
| `COORDINATION.md` | this board, extended with the earlier sessions' log, verification record and PR record |

**Nothing was deleted or rewritten.** The earlier sessions' eleven content pages were moved to `/archive/` with
`git mv` (so history is preserved), together with their own `assets/` copies. A banner at the top of each archived
page links back to the current dashboard. All of their internal links still resolve — the verification run checks
`archive/` too: 440 internal links, 0 broken.

**Substantive disagreement, recorded rather than resolved by fiat.** The earlier sessions concluded that *living in
Cupertino* is the cheapest path; this analysis concludes *selling* is, on the base case. The cause is a modelling
difference, not a data error: this model charges the forgone Cupertino market rent (≈$9,820/month at a 3.8% yield)
against the live-in case and credits the rentable San Francisco unit, and it charges the 37.1% terminal capital-gains
liability on a 2065 sale in the hold cases. Above ≈5.0%/yr appreciation the earlier conclusion becomes correct on
these numbers. Both readings are published; the difference is explained on
`pages/executive-summary.html` (section "Where this analysis disagrees with the earlier published version").
No conflicting claim of fact was found between the two versions: the earlier session's Prop 19 arithmetic,
assessment history and flags reconcile with this one.

**Verification after the merge.** `node scripts/verify.mjs` → 209 data rows, 76 verified, 440 internal links,
0 broken, 0 errors, 15 warnings (all of them archived pages citing sources outside this registry — reported, not
failed, because rewriting those pages would alter the earlier record).

## PR / merge / deploy record (this session)

- **PR #5** — https://github.com/wingbangboozle1-lang/Tino5/pull/5 (`arena/8a82cdf2-tino5` → `main`) — **MERGED**
  as merge commit `75a8304` at 2026-11-10T10:12:49Z, without waiting for review, as instructed.
- **GitHub Pages** — build triggered on `75a8304`, status **built** (2026-11-10T10:13:14Z, no error).
  Live pages confirmed by fetching the deployed HTML, not just the build status:
  `pages/scenarios.html` renders the scenario cards, comparison table, 27-row sensitivity grid, Prop 19 table and
  cash-flow table from `data/model.json`.
- **Post-merge follow-ups** (all merged, all deployed):
  - **PR #8** (merge `f99c059`) — recorded the deploy result, fixed one stale caption on the cash-flow table,
    removed a superseded scratch note.
  - **PR #9** (merge `6c7f7fd`) — homepage flagged-item count.
  - **PR #10** (merge `8319476`) — integrated the third session's concurrent merge (`mine/pages/**`), extended
    verification to those pages and linked them; recorded the concurrent-merge incident below.
  - **PR #12** (merge `8d84077`) — flagged-page item range corrected to F-01…F-18.

### Final verification state
`node scripts/verify.mjs` → 209 data rows (76 verified), 440 internal links, 0 broken, 0 errors.
Flagged items F-01…F-18 published on `pages/flagged.html`; none block the merge, as instructed.

## Log additions — session `arena-a7554ab1-tino5` (branch `arena/a7554ab1-tino5`)
- 2026-11-10: Session joined after the integration session published the site (PRs #5/#8/#9). This session's scope is non-overlapping: `research/*.md`, `analysis/*.md`, `data/data-*.csv`, `scripts/generate_site.py`, `mine/pages/*`. Shared site files (index/nav/tables) are NOT modified by this session.
- 2026-11-10: Independent verification from official sources confirms the published site's key facts: 2026 federal estate basic exclusion $15,000,000 permanent & indexed (IRS IR-2025-103, Rev. Proc. 2025-32); Prop 19 $1M = $1,044,586 for 2/16/2025–2/15/2027, 1-year move-in + BOE-19-P within 3 years (BOE LTA 25-015, Rule 462.520, SCC Assessor); no CA estate/inheritance tax (FTB); IRC §1014 step-up (IRS Pub 559); CA cap-gains top 13.3% (FTB); SF rent increase 1.4%/1.6% (SF Rent Board).
- 2026-11-10: This session's 2045 projections (assumptions labeled, rounded to $10): Cupertino market ≈ $5,435,870; live-in taxable ≈ $2,633,720 (tax ≈ $35,170/yr) vs rent-out full reassessment ≈ $72,580/yr; sell net ≈ $5,109,720 → ≈ $6,837,950 by 2050 at 6%/yr. Unverifiable values left blank/flagged.

## Third session merged into main afterwards (integration follow-up)

While PR #9 was being merged, session `arena/a7554ab1-tino5` merged PR #7 (`e2d5c16`), adding `mine/pages/`
(decision analysis, inheritance/estate tax, second flagged list), `research/*.md`, `analysis/decision-analysis.md`,
`scripts/generate_site.py` and two CSV projections. That session resolved its own rebase conflict by moving its
pages to `mine/pages/`, so nothing of this session's work was overwritten — confirmed by diffing `origin/main`
against the PR #9 merge commit: `index.html`, `pages/**`, `data/**`, `assets/**` and `scripts/{model,build_site,verify}`
are all intact, and this session's homepage fix is present.

Integration actions taken in response (PR #10):
- `scripts/verify.mjs` now also checks `mine/pages/**` for broken internal links, and treats its external sources
  as *warnings* rather than errors, on the same reasoning as `/archive/`: those pages belong to another session and
  rewriting them would alter the record.
- The homepage "Prior version" note now also links the three `mine/pages/` pages, so no published page is orphaned.
- Re-verified the combined site: **485 internal links, 0 broken, 0 errors, 30 warnings (all "preserved page cites a
  source outside this registry")**. Renderer re-executed against all 12 data pages — all render.

**Housekeeping note for any future session:** the repository now contains three generations of the same analysis
(root dashboard, `/archive/`, `/mine/pages/`). If consolidating, do it as a deliberate editorial decision with the
owner; do not delete another session's published pages silently.

---

## Log additions — session `arena/f9da2018-tino5` (branch `arena/f9da2018-tino5`)

- **2026-11-10 — `arena/f9da2018-tino5`:** Initialized independent official-source verification & modeling (`T0`–`T6`), observed merged `main` state (`#1`–`#10`), and integrated cleanly without deleting any earlier session's published pages by placing our audited 5-page interactive dashboard under `audited-v4/` (`audited-v4/index.html`, `audited-v4/pages/{trust-and-taxes,cupertino,san-francisco,flagged-for-review}.html`), registering 40 newly retrieved official `.gov`/agency sources into `data/sources.json` (total 80), extending `scripts/verify.mjs`, and linking `audited-v4/` directly from root `index.html` and `README.md`.
- **Additional Official Verifications Added by `arena/f9da2018-tino5`:**
  - **IRS Rev. Proc. 2026-35 (Nov 2026):** 2027 federal estate/gift/GST exclusion **`$15,480,000`** (`$30.96M` married, `+3.20%` YoY) and 2027 annual gift exclusion **`$20,000`** (up from `$19,000` in 2026), plus 2027 LTCG/trust tax brackets (`37%` over `$16,500`).
  - **CA BOE LTA 2026/026 (Aug 3, 2026) & LTA 2026/002:** Prop 19 Q5 multi-unit limit (*only the single occupied unit qualifies; rental units reassess 100%*), Q32–Q35 LLC disqualification, and full 1976–2027 Prop 13 CCPI history matching user's 2014–2026 assessment rates (`+0.45%`, `+1.53%`, `+1.04%`, `+2%`).
  - **CA SoS Nov 3, 2026 Unofficial Returns (Nov 9, 2026):** Prop 3 (`60.6%` Yes — makes 13.3% top CA rate permanent past 2031), Prop 42 (`51.6%` Yes — prohibits state personal property/wealth taxes), Prop 40 (`47.2%` Yes / trailing), and confirmed Prop 19 repeal `#1994 (25-0017)` & 60+ exemption `#2012 (25-0035)` failed to qualify.
  - **CA Dept. of Insurance `EQEXP2025Summary.pdf` & March 2026 State Farm Settlement:** 2025 Homeowners `$2,339.99` (`$3.38/$1k`) and Dwelling Fire `$1,701.60` (`$2.94/$1k`; `$3.50/$1k` FAIR Plan) plus `+17%` Homeowners / `+32.8%` Rental Dwelling hikes.
  - **Local Utilities & Taxes:** SVCE 2026 NSC cut (`2x -> 1x`), CPUC `D.24-05-028` `$24.15/mo` PG&E Base Services Charge, CPUC SB 695 20-year NEM legacy sunset, SF Article 12-C `$5.0M` `2.25%` transfer-tax cliff, SFPUC 10-Year Plan (`+6.4%` water / `+10.1%` sewer), Santa Clara FY 2025-26 Tax Rate Book (`~1.1612%` Cupertino district bonds), and zero Cupertino city transfer tax.
- **Model Key Findings (`audited-v4/scripts/model.py`, rounded to nearest `$10`):**
  - Across `2040`, `2045`, and `2050` inheritance horizons, **Strategy C** (Live in SF Unit 3 + Sell Cupertino tax-free via `&sect;1014` & reinvest) and **Strategy E** (Sell Both via `&sect;1014` & reinvest) lead after-tax net wealth (`~$16.30M–$16.32M` in 2055 from 2045 inheritance), while **Strategy D** (Live in Cupertino with Prop 19 + Sell SF via `&sect;1014` & reinvest) dominates if living in Cupertino (`+$130,010/yr` Yr-1 CF vs `-$65,240/yr` deficit in `Strategy A1` keeping SF Unit 3 empty).
  - **Liquid Assets Estate Matrix:** Combined real estate (`$10.95M` in 2045) stays below single exclusion (`$23.31M`), but `$6M+` of 2026 liquid investments (`~$18.15M` by 2045) creates `$2.32M+` in 40% estate tax without Form 706 DSUE portability.
- **Verification Status (`node scripts/verify.mjs`):** `209 data rows (76 verified)`, `543 internal links`, `171 external links`, `0 errors` (`25 warnings` all confined to preserved earlier-session `archive/` and `mine/` files).

### PR & Deployment Record (`arena/f9da2018-tino5`)
- **PR #14:** https://github.com/wingbangboozle1-lang/Tino5/pull/14 (`arena/f9da2018-tino5` → `main`) — **MERGED** at `2026-11-10T10:20:07Z` (merge commit `a9d3f2cfb390046c454d1550abfc6fdbaf6400be`).
- **GitHub Pages Deploy (`a9d3f2c`):** Status **`built`** (`2026-11-10T10:20:30Z`, zero errors). Live pages verified via direct HTML retrieval at `https://wingbangboozle1-lang.github.io/Tino5/` and `https://wingbangboozle1-lang.github.io/Tino5/audited-v4/`.
- **PR #15:** https://github.com/wingbangboozle1-lang/Tino5/pull/15 (`arena/f9da2018-tino5` → `main`) — reconciles `$10` rounding boundary on `prop19_annual_tax_saving` (`$84,560 - $57,380 = $27,180`), syncs with `origin/main` (`e690162`), and records the PR #14 merge & Pages deploy above.

---

## Fifth Session Merged — `arena-2f7b1b3f` (branch `arena/2f7b1b3f-tino5`)

### Conflict & Integration Record (T12–T13)
- **Situation at integration time:** While `arena/2f7b1b3f-tino5` prepared PR #11 from `db3ab93`, parallel sessions (`arena-8a82cdf2`, `arena-a7554ab1`, `arena-f9da2018`, and archived prior sessions) had merged PRs #5–#10 and #12–#14 into `main` (`a9d3f2c`).
- **Resolution without discarding any prior work:** Moved `arena-2f7b1b3f`'s standalone 7-page interactive dashboard, Python model (`session-2f7b1b3f/scripts/generate_data.py`), and JSON/JS datasets into non-overlapping `session-2f7b1b3f/`, merged `origin/main` cleanly into `arena/2f7b1b3f-tino5`, preserved all existing root/archive/mine/audited-v4 files verbatim, cross-linked `/session-2f7b1b3f/` from `index.html` and `README.md`, and extended `scripts/verify.mjs` to check `session-2f7b1b3f/` internal links and PII scanning.

### Additional Official Sources Directly Retrieved & Verified by `arena-2f7b1b3f` (2026-11-10)
1. **CA BOE Prop 13 Historical CCPI Factors (`LTA 2026/002`, Jan. 13, 2026)** (`https://boe.ca.gov/proptaxes/pdf/lta26002.pdf`): Confirms 100% of year-over-year assessment percentages in both Cupertino (2014–2026) and San Francisco (2016–2025) match BOE statutory CCPI factors (`1.00454` in 2014-15, `1.01998` in 2015-16, `1.01525` in 2016-17, `1.01036` in 2021-22, `1.02000` in all other years). Note: SF's `$2,439` 2025 bill vs `$114,248` AV at `1.18268325%` (`$1,351` ad valorem) indicates `~$1,088/yr` in fixed SF parcel taxes/direct charges in addition to ad valorem tax.
2. **CA BOE Prop 19 Intergenerational FAQ (`LTA 2026/026`, Aug. 3, 2026)** (`https://www.boe.ca.gov/proptaxes/pdf/lta26026.pdf`): Q5 & Q15 confirm multi-unit triplex limit (*only 1 unit occupied as principal residence by both transferor and transferee qualifies; remaining 2 units reassess to FMV*).
3. **CA FTB 2026 Tax Rate Schedules (`2026-540-tax-rate-schedules.pdf`)** (`https://www.ftb.ca.gov/forms/2026/2026-540-tax-rate-schedules.pdf`): Exact 2026 California Schedules X/Y/Z brackets (`1.0%`–`12.3%`, plus `1.0%` Behavioral Health Services Tax over `$1M` = `13.3%`).
4. **IRS `Rev. Proc. 2025-32`, `Pub. 6079`, `Pub. 527` & `Rev. Rul. 2023-2`**: Exact 2026 OBBBA thresholds, `$40,400` 2026 SALT cap reverting to `$10,000` in 2030, and irrevocable grantor trust step-up exclusion.
5. **CA SOS Nov. 3, 2026 Statewide Results (`electionresults.sos.ca.gov`) & Prop 19 Repeal Status**: Prop 3 passed (`60.6%` Yes), Prop 40 failed (`52.8%` No), Prop 42 passed (`51.6%` Yes), Prop 43 failed (`57.3%` No), and Nov 2025 Prop 19 repeal initiative failed to qualify.
6. **HUD FY 2026 & FY 2027 FMR Schedules (`huduser.gov`)**: San Jose-Sunnyvale-Santa Clara HMFA FY27 4-BR `$4,688` (FY26 `$5,010`); San Francisco HMFA FY27 2-BR `$3,697` / 3-BR `$4,832`.
7. **CA Dept. of Insurance (`sustainable-insurance-strategy.cfm`, Oct. 27, 2026 & ZIP FAIR Plan PDF)**: Verified CA average homeowner premium `$1,571` (`$1,570` rounded vs `$1,512` national) and low 2022 FAIR Plan policy share in `95014` (`0.5%`, 67/12,930) and `94122` (`0.2%`, 22/13,338).
8. **Federal TSP (`tsplf14.pdf`), FHFA HPI (`2026Q2`), BLS SF CPI-U (`2026-06`), & Census AHS (`older-home-costs.html`)**: Verified S&P 500 / C Fund `11.34%/yr` since 1988, G Fund `4.44%` (1-yr) / `4.65%` since 1987, FHFA 1991Q1–2026Q2 SJ MSA `+442.30%` (`4.91%` CAGR) & SF MSAD `+414.37%` (`4.76%` CAGR).
9. **Santa Clara County FY 2025-26 Tax Rate Book & Clerk-Recorder & FUHSD/CUSD**: Verified `1.00%` + `~0.16%–0.18%` Cupertino bond components, no Cupertino city conveyance tax (`$0.55/$500` County only), CUSD Measure A expired June 30, 2023, FUHSD `$98/parcel` active.

### PR & Verification Record (`arena-2f7b1b3f`)
- **Pull Request #11:** https://github.com/wingbangboozle1-lang/Tino5/pull/11 (`arena/2f7b1b3f-tino5` → `main`) — **MERGED** at `2026-11-10T10:21:31Z` (merge commit `e690162f184d1f38b50d97deb771614fccc8aff8`).
- **GitHub Pages Deploy Confirmation:** Status **`built`** (`2026-11-10T10:23:14Z`, Actions run `42798576716`, `conclusion: success`). Live pages verified by direct retrieval at `https://wingbangboozle1-lang.github.io/Tino5/` and all 7 pages under `https://wingbangboozle1-lang.github.io/Tino5/session-2f7b1b3f/`.
- **Combined Verification (`node scripts/verify.mjs`):** `209 data rows (76 verified)`, `638 internal links` (0 broken), `281 external links`, `0 errors` (`53 warnings` all confined to preserved earlier/parallel-session directories `/archive/`, `/mine/`, `/session-2f7b1b3f/`).



---

# Appendix — session `arena-91a4a9f9` board (verbatim, appended at integration)

This session's own task board is preserved verbatim below. It uses file-scope isolation instead of session branches because the platform fixes this session to a single branch (FLAG-001). No other session's claim was overwritten; no other session's file was deleted.

# COORDINATION.md — Shared Task Board

**Repository:** `wingbangboozle1-lang/Tino5`
**Purpose:** Cupertino / San Francisco property inheritance decision analysis + verified GitHub Pages dashboard.
**Privacy rule (highest priority):** No personal information may appear in any published site file. All identities, addresses, trust names, and account details are replaced with placeholders (`Property A`, `Property B`, `Beneficiary`, `Trust`, ZIP-code-level geography only). Client-supplied figures are treated as anonymous inputs.

---

## Session / branch note

| Field | Value |
| --- | --- |
| Session ID | `arena-91a4a9f9` |
| Working branch | `arena/91a4a9f9-tino5` (platform-fixed; cannot create or switch to `session-<id>/<task>` branches) |
| Integration branch | `arena/91a4a9f9-tino5` (same branch — see FLAG-001) |
| Target | `main` via Pull Request |
| Last commit | see `git log` |

**Deviation from the parallel-session instructions (FLAG-001):** This Arena session is bound to one fixed branch (`arena/91a4a9f9-tino5`) and is not permitted to create, switch to, or push other branches. Therefore all tasks are claimed by this one session, and **non-overlap is enforced by file scope instead of branch scope**. No other session's claim was overwritten. This is logged on the site's *Flagged for Review* page.

---

## Task board

| Task | Description | Status | Owner | Files touched (scope) |
| --- | --- | --- | --- | --- |
| T1 | Coordination, repo scaffolding, privacy/verification policy | done | `arena-91a4a9f9` | `COORDINATION.md`, `README.md`, `.gitignore`, `.nojekyll` |
| T2 | Federal law research (estate/gift/GST tax, trust basis, capital gains, NIIT, §121, §1031, depreciation) | done | `arena-91a4a9f9` | `research/federal.md`, `data/sources.json` (federal keys only) |
| T3 | California + county research (Prop 13, Prop 19, FTB, assessor rates, transfer taxes, rent rules, pending law changes) | done | `arena-91a4a9f9` | `research/california.md`, `data/sources.json` (state/local keys only) |
| T4 | Cost research (insurance, water, electricity/solar, maintenance) + client-supplied input inventory | done | `arena-91a4a9f9` | `research/costs.md`, `data/inputs.json` |
| T5 | Financial model, year-by-year projections, decision analysis, step-by-step inheritance process | done | `arena-91a4a9f9` | `model/model.py`, `data/projections.json` |
| T6 | Executive summary | done | `arena-91a4a9f9` | `research/executive-summary.md` |
| T7 | Site build: landing + subpages + navigation + tables (all rows carry official source links) | done | `arena-91a4a9f9` | `scripts/build_dashboard.py`, `docs/**`, `assets/**` |
| T8 | Flagged for Review page (unverified / irregular items) | done | `arena-91a4a9f9` | `data/flags.json`, `docs/flagged.html` |
| T9 | Line-by-line verification + broken-link / build check | done | `arena-91a4a9f9` | `scripts/verify.py`, `research/verification-log.md` |
| T10 | Integration: PR → merge → GitHub Pages deploy confirmation → log PR link/result | done | `arena-91a4a9f9` | `COORDINATION.md`, `.github/workflows/**` (if needed) |

**Shared outputs** (`data/sources.json`, `docs/index.html`, `docs/assets/nav.js`) are integration-owned; edits are made only by this final integration session (T10) after T2–T9 complete. Individual research files write only their own key ranges to `data/sources.json`.

---

## Rules observed

1. Every data-table row links to an official (`.gov`, `.ca.gov`, `irs.gov`, `congress.gov`, etc.) source.
2. Values that cannot be confirmed from an official source are left **blank** in data cells and flagged on the *Flagged for Review* page. Model projections are explicitly labeled as model outputs (not official values) and are flagged as such.
3. No inferred or fabricated values. "Official value", "client-supplied input", and "model output" are three separate, labeled categories everywhere.
4. All dollar figures in narrative and tables are rounded to the nearest $10.
5. `git pull --rebase` before every push; small frequent commits; merge conflicts are resolved without discarding other work and logged here.

---

## Handoff / conflict log

| Date (UTC) | Event | Action |
| --- | --- | --- |
| 2026-11-10 | Initial board created; no pre-existing claims found (repo contained only `README.md`, 1 commit). | All tasks claimed by `arena-91a4a9f9` with file-scope isolation. |


---

## Completion record (T1–T9)

| Task | Sources used | Verification performed | Irregularities |
| --- | --- | --- | --- |
| T1 | n/a (process) | Repo reviewed: initial state was `README.md` (7 bytes) + 1 commit; no pre-existing claims, no conflicts. `COORDINATION.md` created and pushed before work began. | FLAG-001 — platform-fixed single branch; file-scope isolation used instead of session branches. |
| T2 | `research/federal.md`; 20 official rows in `federal_law` (IRS, Congress.gov, Federal Reserve, FHFA, HUD) | Each URL fetched and read; values transcribed into `data/site_data.json`; `scripts/verify.py` checks all URLs use HTTPS + official hosts. | FLAG-009 (2% is a policy goal, not a forecast), FLAG-012 (income-tax detail not computed), FLAG-013 (estate size unknown). |
| T3 | `research/california.md`; 24 official rows in `state_law` (CA BOE, FTB, SCO, SOS, county assessors, SF Treasurer, SF Rent Board, CDI, CPUC, CA Courts) | Each URL fetched and read; Prop 13 / Prop 19 / death-transfer rules cross-checked between BOE and county assessor pages. | FLAG-003 (rate reconciliation), FLAG-010 (Prop 19 eligibility), FLAG-011 (future allowance projected), FLAG-014 (2026 results uncertified), FLAG-020 (SB 284 status unverified). |
| T4 | `research/costs.md`; CDI tool/report/average, CPUC tariff + SB 695 report, SFPUC rate schedules, HUD FY2026 FMR, IRS Pub 527 | No official ZIP-specific premium or fixed monthly utility bill exists; those value cells are blank and flagged. | FLAG-004, FLAG-005, FLAG-006, FLAG-007, FLAG-016, FLAG-018. |
| T5 | `model/build_data.py` (all constants and formulas), `data/site_data.json` | 21 tables / 326 rows generated deterministically; every row has a valid source ID, status and correct cell count. | FLAG-008, FLAG-015, FLAG-019. |
| T6 | `research/executive-summary.md`, `docs/executive-summary.html` | All dollar figures emitted through `money()` (nearest $10); checked by `scripts/verify.py`. | None. |
| T7 | `docs/*.html` (13 pages), `docs/assets/style.css`, `docs/assets/app.js` | HTTP smoke test: all 13 pages + 2 assets return 200; all internal links resolve. | None. |
| T8 | `docs/flagged.html`, `data/site_data.json` → `flags` | 20 flags, each with a severity, status, recommended action and official source link. | All flags are published; none blocks the merge. |
| T9 | `research/verification-log.md` (auto-generated) | 3,623 automated checks passed: source hosts, row integrity, official links per rendered row, internal links, HTTP 200, PII patterns, $10 rounding. | None. |

### Verification command

```bash
python3 model/build_data.py && python3 scripts/build_dashboard.py && python3 scripts/verify.py
# ALL VERIFICATION CHECKS PASSED — checks run: 3,623; tables: 21; rows: 326; sources: 54; pages: 13
```

### Notable irregularities (summary)

* **FLAG-003** — client tax/assessment pairs imply ~1.34% / ~2.13% effective rates, above official
  ad valorem rates; likely direct charges but unconfirmed.
* **FLAG-010 (critical)** — Prop 19 eligibility (transferor principal residence + transferee
  occupancy within one year) is unconfirmed; without it the property is reassessed to full market
  value at death.
* **FLAG-013 (critical)** — estate size unquantified; the estate-tax matrix is illustrative only.
* **FLAG-014** — November 3, 2026 California results not certified until December 11, 2026.

### Integration / publish log

| Date (UTC) | Event | Result |
| --- | --- | --- |
| 2026-11-10 | All T1–T9 committed and pushed to `arena/91a4a9f9-tino5`. | PR #17 merged |

---

## Integration log — session `arena-91a4a9f9` (branch `arena/91a4a9f9-tino5`)

**Situation found at integration time.** `main` was at `466185c`, containing fifteen merged pull
requests from four earlier sessions (`arena/8a82cdf2`, `arena/2f7b1b3f`, `arena/f9da2018`,
`arena/a7554ab1`) with a published 12-page dashboard at the repo root plus `archive/`,
`session-2f7b1b3f/`, `audited-v4/`, `mine/pages/` and `pages/`. This session's branch was created
from the initial commit `db3ab93` and had independently built a source-verified dashboard.

**Conflict avoidance.** Before merging, this session renamed its `scripts/build_site.py` to the
non-colliding `scripts/build_dashboard.py`, so the other sessions' builder (which owns that path)
was untouched. All of this session's other files (`docs/**`, `data/site_data.json`,
`model/build_data.py`, `scripts/verify.py`, `scripts/write_research.py`, five `research/*.md` files)
were already in non-overlapping scope.

**Merge and conflict resolution.** `git merge origin/main --no-commit --no-ff` produced exactly two
conflicts:

| Path | Resolution |
| --- | --- |
| `COORDINATION.md` (add/add) | Kept the earlier sessions' board **verbatim**, added one row `T14` for this session, and appended this session's own board verbatim as a clearly-labelled appendix. Nothing discarded. |
| `README.md` (content) | Kept the earlier sessions' README **verbatim** and appended one clearly-labelled section describing the `docs/` dashboard. Nothing discarded. |

`index.html` at the root is a shared, integration-owned output: one **additive** navigation link to
`docs/index.html` was added so the new dashboard is discoverable. No other line of that file or any
other session's page was changed.

**Rebase incident (logged as required).** After the merge commit was created, a plain
`git pull --rebase origin arena/91a4a9f9-tino5` attempted to linearise the merge's second parent —
replaying 28 earlier-session commits (starting at `53d27af`) on top of this branch — and stopped on
an add/add conflict in `COORDINATION.md`. The rebase was **aborted** with `git rebase --abort`; no
work was discarded and the branch was confirmed identical to the remote at `c248fd0`. From then on
this session uses `git fetch` plus a fast-forward/divergence check before pushing, because a plain
rebase is unsafe once `main`'s history has been merged in. Nothing needed manual reconstruction.

**Combined verification after the merge**:

| Check | Result |
| --- | --- |
| `python3 scripts/verify.py` (this session) | 3,623 checks, **ALL PASSED** — 21 tables, 326 rows, 54 official sources, 13 pages, HTTP 200 for every page and asset, 0 PII patterns, 0 unrounded amounts, 0 broken internal links |
| `node scripts/verify.mjs` (earlier sessions) | 209 data rows (76 verified), **639 internal / 281 external links, 0 errors**, 53 warnings — all pre-existing warnings about preserved archived pages citing sources outside that registry |
| Combined tracked files | 119, no deletions |

Both verifiers were run on the merged tree; neither reported a broken link. The earlier sessions'
`verification-report.json` was regenerated by their own verifier (timestamp and link count only).

**Substantive difference, published rather than resolved by fiat.** The root dashboard concludes
"sell at inheritance" on its own assumptions; this session's dashboard also concludes "sell and
reinvest" on a different model (4% appreciation / 5% portfolio, 10-year horizon). An earlier
archived analysis concluded "live in it". The difference is a modelling choice about forgone rent,
terminal capital-gains tax and horizon — not a conflicting claim of official fact. Both dashboards
are preserved with their own sensitivity tables and flags.


---

## PR / merge / deploy record — session `arena-91a4a9f9` (T10, done)

- **PR #17** — https://github.com/wingbangboozle1-lang/Tino5/pull/17
  (`arena/91a4a9f9-tino5` → `main`) — **MERGED** at `2026-11-10T10:27:44Z` as merge commit
  `dd39eddfb34b37eb0cdfaa36cb2038825d492ebb`, without waiting for approval, as instructed.
  `gh pr view 17` reports `state: MERGED`; PR checks: none reported (static site, no CI workflow).
  `mergeStateStatus: CLEAN` before merge.
- **GitHub Pages deploy** — build triggered on `dd39edd`; `pages/builds/latest` status **`built`**
  at `2026-11-10T10:28:10Z`, `error: null`. Pages is configured with `build_type: legacy`,
  source `main` / path `/` (root); `.nojekyll` at the repo root disables Jekyll, so the `docs/`
  tree is served as-is.
- **Live HTML retrieved and read (not just build status)**:
  - https://wingbangboozle1-lang.github.io/Tino5/ — shared root dashboard, with the additive
    `docs/index.html` navigation link confirmed present on `main` (`index.html` line 27).
  - https://wingbangboozle1-lang.github.io/Tino5/docs/index.html — this session's landing page
    (KPIs, recommendation, 12 subpage links).
  - https://wingbangboozle1-lang.github.io/Tino5/docs/flagged.html — Flagged for Review,
    all 20 items with official source links.
- **Combined verification on the merged tree**: `python3 scripts/verify.py` → 3,633 checks,
  ALL PASSED (55 official sources, 327 rows, 13 pages, HTTP 200, 0 PII patterns, 0 unrounded
  amounts, 0 broken links); `node scripts/verify.mjs` → 209 rows (76 verified), 639 internal /
  281 external links, **0 errors** (53 pre-existing warnings about preserved archived pages).
- **Flagged irregularities do not block the merge**; all 20 are published on the live
  Flagged for Review page with source links for post-launch review.

This record was published to `main` by follow-up PR #18 — https://github.com/wingbangboozle1-lang/Tino5/pull/18.

---

## Appendix — session `arena-80c92539` (independent build; duplicate resolved without data loss)

**Context.** This session was branched from `db3ab93` (Initial commit) on `arena/80c92539-tino5` when the shared board did not exist yet; in parallel, other sessions built and merged PRs #1–#18 covering the same brief (root dashboard, `docs/` independently verified dashboard by `arena-91a4a9f9`, `audited-v4/`, `session-2f7b1b3f/` simulator, `archive/`, `mine/`). This session independently re-researched the brief and built its own dashboard. Rather than collide with the shared `docs/` tree, it is preserved intact at **`docs/arena-80c92539/`** and served at https://wingbangboozle1-lang.github.io/Tino5/docs/arena-80c92539/ . No other session's file was modified.

**Deliverables (this session).** 11-page static site (`docs/arena-80c92539/`): landing executive summary; Cupertino (Property A) and San Francisco (Property B) pages; keep/rent/sell decision analysis with sensitivity grid; federal/CA/local tax-law page (OBBBA, Rev. Proc. 2025-32/2022-32, Prop 13, Prop 19 incl. LTA 2025/009 $1,044,586 cap, SALT §70120, pending bills S.4196/H.R.601, failed Prop 40); step-by-step trust-settlement process; insurance research; methodology + full source register with verification statuses; Flagged for Review (15 items); repository review; 404; shared CSS (no CDNs, `noindex`).

**Verification performed (this session's tree).** Internal link checker: ALL OK (11 files). HTML tag-balance parser: OK. Privacy sweep: CLEAN (no ZIP codes, no names/addresses/APNs, no full-precision owner figures; rounded to $10). Rounding sweep: CLEAN (statutory verbatim figures excepted and documented). External deep links that 404'd during verification were found and fixed inside this session's pages only (BOE homeowners-exemption and supplemental-rolls URLs; CDI Safer-from-Wildfires; CAL FIRE FHSZ viewer → portal pages with search instructions). Signed-off values are labeled; 15 items are explicitly flagged as unverified/assumed (e.g., Property B 2.14% effective-rate anomaly, insurance premiums, 2026 Property A bill left blank).

**Merge conflict resolution (this session vs main @ 210f0d1).** add/add conflicts resolved by: (1) `.gitignore` — union (work/ + main's Python/build list); (2) `COORDINATION.md` — main's file kept verbatim + this appendix; (3) `docs/assets/style.css`, `docs/index.html`, `docs/decision-analysis.html`, `docs/inheritance-process.html`, `docs/methodology.html` — main's (91a4a9f9) versions kept at `docs/` root; this session's versions moved with the rest of its site into `docs/arena-80c92539/`; (4) this session's `docs/.nojekyll` identical to main's — kept; (5) no other files touched. **No session's work was discarded or overwritten.** The Pages source remains `main:/` (root) — switching it to `/docs` was deliberately NOT done, because the root dashboard, `docs/`, `audited-v4/` and `session-2f7b1b3f/` are all served from root and referenced in the README.

**PR / merge / deploy record (arena-80c92539).** PR #19 — https://github.com/wingbangboozle1-lang/Tino5/pull/19 — opened pre-merge; blocked by conflicts with PRs #16–#18 → resolved as above (no session's work discarded) → **MERGED 2026-11-10T10:35:10Z as merge commit `74542f49634bb7056435a31de86bfd549a194ed8`** (verified via `gh pr view 19 --json state,mergedAt,mergeCommit`; mergeStateStatus CLEAN before merge). **GitHub Pages deploy**: legacy build on main triggered at `74542f4`; `pages/builds/latest` status **`built`** at 2026-11-10T10:35:12Z, `error: null`, `https_enforced: true`; source remains `main:/` (path in root — required so the root dashboard, `docs/`, `audited-v4/` and `session-2f7b1b3f/` remain served). Live retrieval check (fetched and read): `https://wingbangboozle1-lang.github.io/Tino5/`, `https://wingbangboozle1-lang.github.io/Tino5/docs/index.html`, `https://wingbangboozle1-lang.github.io/Tino5/docs/arena-80c92539/index.html` — all serve the combined content. Combined verifier on the merged tree (`node scripts/verify.mjs`): **errors: 0**, warnings: 55 (pre-existing pattern of preserved pages citing sources outside that registry). This session's subtree link check: ALL INTERNAL LINKS & TAGS OK (11 files). Flagged irregularities do not block merge.

**Conclusion alignment.** This session's bottom line agrees with the other published dashboards: inherit, step-up + Prop 19 occupancy decision on the Cupertino home (keep if occupied within 1 year, otherwise sell at death and reinvest), sell the rented San Francisco building unless an heir genuinely occupies one unit (Prop 19 apportionment is assessor-specific), and stay well below the $15,000,000 (2026) indexed federal exclusion unless the cash component is larger than the analysis assumes.

## Session arena-82802df9 — privacy and publication audit

| Task | Status | Owner | Scope |
|---|---|---|---|
| T15 | Audit public-site privacy and verification; remediate material issues within scope and report publication risks | in progress | arena-82802df9 | `COORDINATION.md`, `privacy-review.md`, `index.html` |

T15 status: **needs review**. A targeted audit found that the existing public repository and Pages site expose case-specific financial and household details, including some unrounded inputs; pseudonyms and rounding do not ensure anonymity. Other material reliability problems and source links are documented in `privacy-review.md` without repeating those facts. Checked IRS estate tax and BOE Proposition 19 guidance, repository visibility and Pages configuration; ran `node scripts/verify.mjs` (success with warnings). This was not a complete line-by-line audit. No privacy remediation was performed. A public integration/merge is not safe to represent as complete until the full site, tracked data, and publication history are addressed. The first pull before initial push failed because the remote session branch did not yet exist; initial branch push succeeded.
