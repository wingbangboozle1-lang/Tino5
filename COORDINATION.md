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
| T1 | Coordination, repo scaffolding, privacy/verification policy | in progress | `arena-91a4a9f9` | `COORDINATION.md`, `README.md`, `.gitignore`, `.nojekyll` |
| T2 | Federal law research (estate/gift/GST tax, trust basis, capital gains, NIIT, §121, §1031, depreciation) | in progress | `arena-91a4a9f9` | `research/federal.md`, `data/sources.json` (federal keys only) |
| T3 | California + county research (Prop 13, Prop 19, FTB, assessor rates, transfer taxes, rent rules, pending law changes) | in progress | `arena-91a4a9f9` | `research/california.md`, `data/sources.json` (state/local keys only) |
| T4 | Cost research (insurance, water, electricity/solar, maintenance) + client-supplied input inventory | in progress | `arena-91a4a9f9` | `research/costs.md`, `data/inputs.json` |
| T5 | Financial model, year-by-year projections, decision analysis, step-by-step inheritance process | unclaimed | `arena-91a4a9f9` | `model/model.py`, `data/projections.json` |
| T6 | Executive summary | unclaimed | `arena-91a4a9f9` | `research/executive-summary.md` |
| T7 | Site build: landing + subpages + navigation + tables (all rows carry official source links) | unclaimed | `arena-91a4a9f9` | `scripts/build_site.py`, `docs/**`, `assets/**` |
| T8 | Flagged for Review page (unverified / irregular items) | unclaimed | `arena-91a4a9f9` | `data/flags.json`, `docs/flagged.html` |
| T9 | Line-by-line verification + broken-link / build check | unclaimed | `arena-91a4a9f9` | `scripts/verify.py`, `research/verification-log.md` |
| T10 | Integration: PR → merge → GitHub Pages deploy confirmation → log PR link/result | unclaimed | `arena-91a4a9f9` | `COORDINATION.md`, `.github/workflows/**` (if needed) |

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
