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
- **Follow-up Polish PR:** Reconciles `$10` rounding boundary on `prop19_annual_tax_saving` (`$84,560 - $57,380 = $27,180`) and records the PR #14 merge & Pages deploy above.

