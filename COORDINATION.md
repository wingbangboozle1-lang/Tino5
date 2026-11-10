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
| T10 | Integration: PR → merge → GitHub Pages deploy confirmation → log PR link/result | in progress | `arena-91a4a9f9` | `COORDINATION.md`, `.github/workflows/**` (if needed) |

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
| 2026-11-10 | All T1–T9 committed and pushed to `arena/91a4a9f9-tino5`. | pending PR |
