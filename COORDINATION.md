# Coordination board

Single-session execution on Arena branch `arena/63ef1e05-tino5` (fixed by Arena; no parallel worktrees/branches are permitted in this session).

| Task | Status | Owner session | File scope |
|---|---|---|---|
| Official-source research, privacy-safe decision dashboard, verification and deployment setup | done (branch-only; upstream task already integrated) | `63ef1e05-tino5` | `COORDINATION.md`, `README.md`, `index.html`, `assets/*`, `pages/*`, `scripts/*`, `.github/workflows/*` |

## Verification / handoff log

- Initial board checked before work on the assigned branch: no `COORDINATION.md` existed there; no other claims were visible.
- Claim commit `3044e39` was pushed to `arena/63ef1e05-tino5` after `git pull --rebase origin main`. Arena fixes the branch name; no alternate worktree/branch was created.
- Official sources checked against primary pages: California BOE Prop 19 Fact Sheet and Property Tax Overview; IRS estate-tax FAQs, 2026 estate/gift-tax updates and Form 706 instructions; IRS Publication 551; California State Controller estate-tax page; California FTB 2026 Form 593 instructions; California Courts self-help trust material; California Department of Insurance 2026 comparison tool; California Public Utilities Commission consumer resources; Santa Clara County Assessor; San Francisco Assessor-Recorder, Rent Board and Department of Elections; SEC Investor.gov.
- Verification performed on this branch: `scripts/check_site.py` checks six HTML pages, resolves local links, and requires an official-government source link in every data table row; `git diff --check` passes. No supplied ZIPs, property valuation, rent figure or household utility/insurance amounts appear in this branch's public site content.
- Irregularities from user-provided records: assessment/tax histories lack supporting county statements or parcel-specific notices; one history has a material assessment/bill scope reconciliation question. Future 2040–2050 values, taxes, operating costs and returns are left blank on this branch.

## Upstream coordination / conflict resolution

- After this branch was pushed, `origin/main` advanced to `e3ae978` and its coordination board showed T1–T4 already done by other sessions, PR #3 merged and Pages deployed. A `git fetch origin main` and non-mutating `git merge-tree` inspection found overlapping changes in `README.md`, `COORDINATION.md`, `index.html` and `assets/*`. No rebase or resolution that overwrote upstream files was attempted.
- Upstream PR #3 is merged at `e3ae97875620801e8b8a192d48f98c297ab380de`; GitHub Pages API reports `https://wingbangboozle1-lang.github.io/Tino5/`, public and built from `main:/`. Latest Pages deployment run `42797221776` completed successfully.
- This branch's PR #6 (`https://github.com/wingbangboozle1-lang/Tino5/pull/6`) was closed on 2026-11-10 because GitHub reported `CONFLICTING` and merging the duplicate site would overwrite/discard the already-integrated upstream site. It was not merged. The earlier live project is PR #3, not PR #6.
- **URGENT PRIVACY REQUEST TO UPSTREAM INTEGRATION OWNER (`arena/036d45c7-tino5`):** review the already-live pages for household-specific details from the user request. The live `main` site currently includes property city/ZIP labels and user-provided values/costs in public pages. Replace those with generic placeholders or remove them before considering that public site privacy-compliant; preserve only verified, non-identifying legal/source facts. This session did not edit those upstream-owned files, in accordance with the coordination rule. The request is also being sent as a comment on merged PR #3 without repeating any private numbers.
- The privacy-focused alternative in this branch uses Property A/Property B placeholders, omits the household financial inputs, leaves future projections blank, and has a separate Flagged for Review page. It is not the live GitHub Pages product. Any changes to the already-integrated `main` files must be made by the owning integration task or a follow-up task entered on its shared board.
