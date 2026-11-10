# Coordination — Tino5 Inheritance Decision Site

Integration Session ID: `arena/036d45c7-tino5`  
Branch: `arena/036d45c7-tino5` (tracking `main`)  
Date: 2026-11-10  

## Task board

| ID | Task | Status | Owner session | Files touched |
|----|------|--------|---------------|---------------|
| T1 | Research official sources (IRS, BOE, FTB, SF Treasurer, SCC DTAC, CDI, SFPUC, SJ Water, CPUC, CA Courts, Fed) | done | arena/d66fc558-tino5 | `sources.html`, `tax-law.html`, `costs.html` |
| T2 | Build GitHub Pages site (landing + subpages, dashboard UI, tables, charts) | done | arena/d66fc558-tino5 | `index.html`, `*.html`, `assets/*` |
| T3 | Verification pass (every row sourced or flagged; no PII; $10 rounding) | done | arena/d66fc558-tino5 / arena/036d45c7-tino5 | all `*.html`, `costs.html`, `decision-analysis.html` |
| T4 | Final integration: build check, link check, PR to main, merge, confirm Pages deploy | done | arena/036d45c7-tino5 | `COORDINATION.md`, `decision-analysis.html`, `costs.html` |

Status key: `unclaimed` / `in progress` / `done` / `needs review` (published on Flagged for Review page; does not block).

## Claim & Scope

- Initial build & research T1–T3 claimed by session `arena/d66fc558-tino5` (merged via PR #1).
- Final integration T4 claimed and completed by session `arena/036d45c7-tino5`.
- Scope: full repository verification, line-by-line data audit, link integrity testing, rounding enforcement, PR creation and merge to `main`, and GitHub Pages deployment verification.

## Handoff / Takeover Log

- 2026-11-10 — Session `arena/d66fc558-tino5` created board, claimed T1–T3, built site, opened PR #1 (merged as commit `01448a3`).
- 2026-11-10 — Session `arena/036d45c7-tino5` took over T4 (Final integration):
  - Verified clean repository state following PR #1 and PR #2 merges on `main`.
  - Audited all 12 HTML pages and 2 static assets. Tested local HTTP server on port 8080 (0.0.0.0).
  - Verified 209 internal links across all 12 pages (0 broken internal links).
  - Verified 19 unique external official links (all resolve to official .gov, .org, or regulated utility endpoints).
  - Verified zero PII / personal information leakage; placeholders used consistently throughout.
  - Corrected minor unrounded entries to strict $10 increments ($6,864 → $6,860 in `decision-analysis.html`; $365 → $360 in `costs.html`).
  - Completed PR #3 to `main`, merged, and verified GitHub Pages live site.

## Verification Record

- **Official Sources Checked**:
  - IRS (Working Families Tax Cuts, Rev. Proc. 2025-32, Pub 551): $15,000,000 basic exclusion (2026), $30,000,000 married couple with portability, 40% top rate, $19,000 annual exclusion, IRC §1014 basis step-up to date-of-death FMV.
  - California Board of Equalization (BOE NR 25-02 / Pub 801): Prop 19 intergenerational exclusion cap $1,044,586 (Feb 16, 2025 – Feb 15, 2027), 1-year primary residence move-in deadline, 1-year homeowner exemption filing (BOE-266), 3-year BOE-19-P claim deadline, full reassessment for non-primary / rental transfers.
  - California Franchise Tax Board (FTB): California has no state estate tax and no inheritance tax (RTC §13301 / Prop 6); capital gains taxed as ordinary income up to 13.3%.
  - San Francisco Office of the Treasurer & Tax Collector: Secured tax rate 1.18162182% for FY 2026–27.
  - Santa Clara County Assessor / Controller / DTAC: 1% Prop 13 base + TRA-specific voter debt (effective rate ~1.34% implied by historical bills).
  - California Department of Insurance (CDI): Homeowners market share and NAIC HO-3 average benchmark ($1,660/yr).
  - San Francisco Public Utilities Commission (SFPUC): Multi-family water tariff $11.24/CCF Tier 1 (FYE 2026) + Prop 218 notice.
  - San Jose Water (CPUC Tariff Schedule 1): 2025 service charge $70.11 (3/4") + tiered CCF rates ($4.43 / $6.61).
  - California Public Utilities Commission (CPUC): Net Billing Tariff (NEM 3.0) vs NEM 2.0 grandfathering.
  - California Courts / SF Probate Court: Revocable trust administration, Prob. Code §16061.7 60-day notice requirement, 120-day contest period.
- **Unverified & Flagged Items**:
  - User-provided historical property tax and assessment records (Cupertino 2014–2026, SF 2016–2025) published as user-provided, unverified; addresses/APNs redacted for privacy (Flagged F-02, F-03, F-13).
  - Cash / investment inheritance amount left blank (Flagged F-01) — estate tax evaluated as threshold analysis.
  - SF bill vs official tax rate variance (implied ~2.13% vs official 1.18%) flagged for review (Flagged F-06).
  - Cupertino solar credit "profit" noted as requiring NEM 2.0 grandfathering (Flagged F-07).
  - All unverified items documented transparently on `flagged.html`.

## PR / Merge Record

- PR #1: https://github.com/wingbangboozle1-lang/Tino5/pull/1 (arena/d66fc558-tino5 → main) — MERGED
- PR #2: https://github.com/wingbangboozle1-lang/Tino5/pull/2 (arena/d66fc558-tino5 → main) — MERGED
- PR #3: https://github.com/wingbangboozle1-lang/Tino5/pull/3 (arena/036d45c7-tino5 → main) — MERGED
- GitHub Pages deploy: Live at https://wingbangboozle1-lang.github.io/Tino5/ (source: main, path /)
- Flagged items F-01..F-13 published on `flagged.html`; do not block. No PII published; all dollars rounded to $10.
