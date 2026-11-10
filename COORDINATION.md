# Coordination board

Single-session execution on Arena branch `arena/63ef1e05-tino5` (fixed by Arena; no parallel worktrees/branches are permitted in this session).

| Task | Status | Owner session | File scope |
|---|---|---|---|
| Official-source research, privacy-safe decision dashboard, verification and deployment setup | done (branch-only; upstream task already integrated) | `63ef1e05-tino5` | `COORDINATION.md`, `README.md`, `index.html`, `assets/*`, `pages/*`, `scripts/*`, `.github/workflows/*` |

## Verification / handoff log

- Initial board checked before work on the assigned branch: no `COORDINATION.md` existed there; no other claims were visible.
- Claim commit `3044e39` was pushed to `arena/63ef1e05-tino5` after `git pull --rebase origin main`. Arena fixes the branch name; no alternate worktree/branch was created.
- Scope is confined to the paths above; public site uses placeholders and omits user-supplied home valuations, address/ZIP details, rent, utility amounts and insurance estimates. Unverified inputs are marked rather than repeated as facts.
- Official sources checked against primary pages: California BOE Prop 19 Fact Sheet and Property Tax Overview; IRS estate-tax FAQs, 2026 estate/gift-tax updates and Form 706 instructions; IRS Publication 551; California State Controller estate-tax page; California FTB 2026 Form 593 instructions; California Courts self-help trust material; California Department of Insurance 2026 comparison tool; California Public Utilities Commission consumer resources; Santa Clara County Assessor; San Francisco Assessor-Recorder, Rent Board and Department of Elections; SEC Investor.gov.
- Verification performed: `scripts/check_site.py` checks all six HTML pages, resolves local links, and requires an official-government source link in every data table row. `git diff --check` passes. Privacy grep found none of the supplied ZIPs, home values, rent figure or other supplied private numeric details in this branch's public site content.
- Findings/irregularities: supplied property assessment/tax histories were not supported by county statements or parcel-specific notices; one history has a material assessment/bill scope reconciliation question. No user estimate, property-tax projection, home-value forecast, utility cost, insurance price, maintenance cost, rent projection or portfolio return is published in this branch. 2040–2050 legal/economic inputs remain uncertain; categories are on `pages/flagged-review.html`.

## Upstream coordination / conflict resolution

- After this branch was pushed, `origin/main` advanced to `e3ae978` and its `COORDINATION.md` showed T1–T4 already done by other sessions, with PR #3 merged and a successful Pages deployment. The upstream commit added the same `index.html`, `README.md`, `COORDINATION.md`, `assets/*` and site purpose. This was a real overlapping-scope conflict discovered through `git fetch origin main` and a non-mutating `git merge-tree` inspection; no rebase or conflict resolution that overwrote upstream files was attempted.
- Verified upstream PR #3 is merged at `e3ae97875620801e8b8a192d48f98c297ab380de`; GitHub Pages API reports `https://wingbangboozle1-lang.github.io/Tino5/`, public, built, legacy source `main:/`; latest Pages build/deployment run `42797221776` completed successfully.
- This branch's PR #6 (`https://github.com/wingbangboozle1-lang/Tino5/pull/6`) was closed on 2026-11-10 because GitHub reported `CONFLICTING` and merging the duplicate site would overwrite/discard the already-integrated upstream site. It was not merged. No push to `main` or alternate branch was made. The earlier live project is PR #3, not PR #6.
- The branch's privacy-focused version is preserved for reference but is not the live GitHub Pages product. Any changes to the already-integrated `main` files should be requested via the shared coordination board and owned by a follow-up integration task.
