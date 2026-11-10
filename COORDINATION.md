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
     are shown, and the row is labelled `model` not `verified`.
  4. Money rounded to the nearest $10 unless the source value is itself an exact
     statutory/assessed figure (those are shown as published and also rounded in
     projection columns).

## Task board

| ID | Task | Status | Session | File scope |
|----|------|--------|---------|-----------|
| T0 | Coordination board + repo scaffold | done | arena-8a82cdf2 | `COORDINATION.md`, `.nojekyll`, `README.md` |
| T1 | Source registry + verified-data schema | in progress | arena-8a82cdf2 | `data/sources.json`, `data/schema.md` |
| T2 | Property tax: CA Prop 13/19 law, Santa Clara + SF rates, assessment projections | unclaimed | — | `data/property-tax.json`, `pages/property-tax.html` |
| T3 | Inheritance tax: federal estate/gift, step-up basis, CA (no estate tax), trust nuance | unclaimed | — | `data/inheritance-tax.json`, `pages/inheritance-tax.html` |
| T4 | Operating costs: insurance, water, electricity, maintenance | unclaimed | — | `data/operating-costs.json`, `pages/operating-costs.html` |
| T5 | Step-by-step inheritance process | unclaimed | — | `data/process.json`, `pages/inheritance-process.html` |
| T6 | Scenario model: live in / rent / sell-and-reinvest (+ executive summary) | unclaimed | — | `data/scenarios.json`, `pages/scenarios.html`, `pages/executive-summary.html` |
| T7 | Law-change watch (pending legislation, ballot measures, proposals) | unclaimed | — | `data/law-watch.json`, `pages/law-watch.html` |
| T8 | Site shell: layout, nav, CSS, JS table renderer | unclaimed | — | `index.html`, `assets/**` |
| T9 | Verification pass: row-by-row source check, link check | unclaimed | — | `scripts/verify.mjs`, `pages/flagged.html`, `data/flagged.json` |
| T10 | Integration: merge, build check, PR, merge PR, confirm Pages deploy | unclaimed | — | `COORDINATION.md` |

Status values: `unclaimed` · `in progress` · `needs review` · `done`.
`needs review` = published on the Flagged for Review page; does **not** block merge.

## Log

- **2026-11-10 — arena-8a82cdf2** — Read repo: only `README.md` ("# Tino5") plus git
  history (`db3ab93` Initial commit). No prior sessions, no prior claims, no site files.
  Created this board and scaffolded the repo. Claiming T0 and T1 with
  `git` scope `COORDINATION.md`, `.nojekyll`, `README.md`, `data/sources.json`,
  `data/schema.md`.
