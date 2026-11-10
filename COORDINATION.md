# COORDINATION.md — Shared Task Board

Session ID for this working branch: `arena-80c92539` (branch `arena/80c92539-tino5`).

> **Governance note (read first):** The system constraint for this engagement is that all work happens on `arena/80c92539-tino5` and only that branch is pushed; the final PR goes from this branch into `main`. This single-branch rule overrides the `session-<id>/<task>` branch convention written below for multi-session operation. Other sessions: if you are reading this, treat the tasks below owned by `arena-80c92539` as claimed. Do not start them. If you find this stale (>60 min since last commit), follow the takeover rule.

## How to use
- Claim a task by writing your session ID and file scope in the table, then commit + push **immediately**.
- A task with status `needs review` is published on the site's Flagged for Review page and does not block anything.
- Never mark anything `done` / verified without an official source link recorded in the Sources column.
- Log handoffs and merge conflicts in the Log section.

## Task board

| # | Task | Status | Owner | File scope | Sources |
|---|------|--------|-------|------------|---------|
| 1 | Repo review (line-by-line) of Tino5 | in progress | arena-80c92539 | `docs/repo-review.html` (report), no repo source changes | see report |
| 2 | Federal estate/gift/GST law research (2026 rules, OBBBA, projections) | in progress | arena-80c92539 | `docs/federal-estate-tax.html`, `docs/data/` | IRS, Congress.gov |
| 3 | CA property tax law research (Prop 13, Prop 19, supplemental bills) | in progress | arena-80c92539 | `docs/california-property-tax.html` | BOE |
| 4 | CA/local income & inheritance tax research (no inheritance tax; capital gains; SALT cap; NIIT) | in progress | arena-80c92539 | `docs/california-taxes.html` | FTB, IRS |
| 5 | Insurance cost research (Cupertino primary residence; SF Outer Sunset landlord/rental) | in progress | arena-80c92539 | `docs/insurance.html` | CA DOI, FAIR Plan |
| 6 | Property A (Cupertino, Santa Clara County) projections 2026–2060 | in progress | arena-80c92539 | `docs/property-a.html` | user-provided rounded data + FHFA |
| 7 | Property B (San Francisco, San Francisco County) projections 2026–2060 | in progress | arena-80c92539 | `docs/property-b.html` | user-provided rounded data + FHFA |
| 8 | Decision analysis: live in vs rent vs sell+reinvest (both properties), NPV-style comparison | in progress | arena-80c92539 | `docs/decision-analysis.html` | derived from 2–7 |
| 9 | Step-by-step inheritance/trust settlement process (2040–2050 horizon) | in progress | arena-80c92539 | `docs/inheritance-process.html` | IRS, CA Probate Code, BOE, county clerk |
| 10 | Site scaffold: landing page + navigation + shared CSS, GitHub Pages config | in progress | arena-80c92539 | `docs/index.html`, `docs/assets/`, `docs/.nojekyll` | — |
| 11 | Flagged-for-review page (unverifiable / conflicting items) | in progress | arena-80c92539 | `docs/flagged-for-review.html` | — |
| 12 | Privacy anonymization pass (no names/addresses/zips/APNs; $ rounded to $10) | in progress | arena-80c92539 | all `docs/**` | privacy protocol |
| 13 | Final integration: re-verify data, build/link check, PR to main, merge, GitHub Pages deploy | in progress | arena-80c92539 | branch `arena/80c92539-tino5` → `main`, Pages settings | — |
| 14 | Executive summary page (landing) with recommendation | in progress | arena-80c92539 | `docs/index.html` | derived |

## Verification log
| Date (UTC) | Task | Verification performed | Source links | Irregularities |
|---|---|---|---|---|
| 2026-11-10 | Repo | Initial clone reviewed: single commit `db3ab93`, only `README.md` (`# Tino5`), no data files, Pages already enabled (legacy build, `main` `/`, https enforced) | n/a (local clone) | Repo contained no inheritance data; all figures below come from user brief + public official sources |

## Log
- 2026-11-10 — `arena-80c92539` created this board; all tasks claimed by the single active session on `arena/80c92539-tino5` per system branch constraint. No other session had claimed any task (file did not exist).
- Handoff rule: takeover allowed if claim >60 min old with no commits; note the handoff here.
- 2026-11-10 — Tasks 1-12 completed and committed (`df01b02`). Site built under `/docs` (landing + 10 pages), all internal links machine-verified, privacy sweep clean (no ZIP/names/addresses/full-precision user figures), rounding sweep clean. External BOE/CDI/CAL-FIRE 404 links found by verification and fixed (re-pointed to verified pages). Public site deliberately excludes raw year-by-year brief tables (Flag F-13).
- 2026-11-10 — PR opened: https://github.com/wingbangboozle1-lang/Tino5/pull/19 (integration: `arena/80c92539-tino5` -> `main`). Merge to follow immediately after this entry; GitHub Pages source to be switched from `main:/` to `main:/docs` post-merge. Deploy result recorded as PR comment and here (branch copy).
- Sources: see docs/methodology.html section M.4 (S1-S28). Verification: internal link checker OK (11 files), HTML parser OK, external spot checks recorded in M.6, calculations re-derived twice programmatically.


## Status summary (2026-11-10)
Tasks 1-12: done (this branch). Task 13: in progress — PR #19 opened; merge + Pages switch + deploy verification pending. Task 14: done (index.html is the executive summary).
