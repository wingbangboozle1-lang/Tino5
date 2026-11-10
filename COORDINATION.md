# Coordination board

Single-session execution on Arena branch `arena/63ef1e05-tino5` (fixed by Arena; no parallel worktrees/branches are permitted in this session).

| Task | Status | Owner session | File scope |
|---|---|---|---|
| Official-source research, privacy-safe decision dashboard, verification and deployment setup | in progress | `63ef1e05-tino5` | `COORDINATION.md`, `README.md`, `index.html`, `assets/*`, `pages/*`, `scripts/*`, `.github/workflows/*` |

## Verification / handoff log

- Initial board checked before work: no existing `COORDINATION.md`; no other claims to avoid.
- Claim commit `3044e39` was pushed to `arena/63ef1e05-tino5` after `git pull --rebase origin main`. Arena fixes the branch name; no alternate worktree/branch is permitted in this session.
- Scope is confined to the paths above; public site uses placeholders and omits user-supplied home valuations, address/ZIP details, rent, utility amounts and insurance estimates. Unverified inputs are marked as such rather than repeated as facts.
- Official sources checked against primary pages: California BOE Prop 19 Fact Sheet and Property Tax Overview; IRS estate-tax FAQs, 2026 estate/gift-tax updates and Form 706 instructions; IRS Publication 551; California State Controller estate-tax page; California FTB 2026 Form 593 instructions; California Courts self-help trust material; California Department of Insurance 2026 comparison tool; California Public Utilities Commission consumer resources; Santa Clara County Assessor; San Francisco Assessor-Recorder, Rent Board, and Department of Elections; SEC Investor.gov.
- Verification performed: `scripts/check_site.py` checks all six HTML pages, resolves local links, and requires an official-government source link in every data table row. Re-run before each push and in the Pages build. Privacy grep found none of the supplied ZIPs, home values, rent figure or other named private numeric details in website/repository text.
- Findings/irregularities: the supplied property assessment/tax histories are not supported by county tax statements or parcel-specific assessor notices; one history has a material assessment/bill scope reconciliation question. No user estimate, property tax projection, home-value forecast, utility cost, insurance price, maintenance cost, rent projection or portfolio return is published. The 2040–2050 legal/economic inputs remain uncertain. These items are published on `pages/flagged-review.html` and do not block the site.
