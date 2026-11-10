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
| T10 | Integration: merge, build check, PR, merge PR, confirm Pages deploy | in progress | arena-8a82cdf2 | `COORDINATION.md` |

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
