# Cupertino (95014) & San Francisco Outer Sunset (94122) Trust Inheritance Decision Dashboard

A verified, privacy-protected financial and legal decision dashboard analyzing trust inheritance options (2040–2050 horizon) for:
- **[Cupertino Residence — ZIP 95014, Parcel Placeholder]**
- **[San Francisco 3-Unit Property — Outer Sunset ZIP 94122, Parcel Placeholder]**

Live GitHub Pages Dashboard: `https://wingbangboozle1-lang.github.io/Tino5/`

---

## Privacy & Verification Standards

1. **Anonymization First:** All personal names, trust names, street addresses, APNs, and personal accounts are strictly replaced with placeholders. Zero PII is committed to this repository or published to GitHub Pages.
2. **$10 Rounding Standard:** All financial outputs, property values, tax projections, operating expenses, and net worth comparisons are rounded to the nearest **$10** increment (`r10()` in `scripts/generate_data.py` and `assets/app.js`).
3. **Line-by-Line Official Verification:** All tax laws, exemption caps, property tax rates, utility schedules, housing appreciation indexes, and equity/Treasury benchmarks are verified directly from official government and utility websites (`irs.gov`, `boe.ca.gov`, `ftb.ca.gov`, `sco.ca.gov`, `sos.ca.gov`, `electionresults.sos.ca.gov`, `congress.gov`, `leginfo.legislature.ca.gov`, `oag.ca.gov`, `controller.santaclaracounty.gov`, `clerkrecorder.sccgov.org`, `cupertino.gov`, `sjwater.com`, `pge.com`, `cpuc.ca.gov`, `sftreasurer.org`, `sfassessor.org`, `sf.gov`, `sfpuc.gov`, `insurance.ca.gov`, `fhfa.gov`, `tsp.gov`, `bls.gov`, `huduser.gov`, `census.gov`).
4. **Non-Hallucination & Flagged for Review:** Any empirical value that cannot be confirmed from public official sources without private parcel, underwriting, or trust documents is left blank in official columns and itemized on the **Flagged for Review** page (`pages/verification-review.html`).

---

## Dashboard Pages

- `index.html` — **Executive Summary & Decision Overview** (Recommended Strategy A vs. all alternatives, KPI summary, critical traps)
- `pages/decision-analysis.html` — **Live vs. Rent vs. Sell Portfolio Analysis & Interactive Simulator**
- `pages/projections.html` — **2026–2050 Year-by-Year Projections** (Historical Official vs. Conservative regimes)
- `pages/tax-laws.html` — **Federal, California & Local Tax and Property Laws** (including Nov. 3, 2026 California ballot measure outcomes)
- `pages/estate-thresholds.html` — **Federal & State Inheritance Tax Thresholds & Liquid Estate Headroom**
- `pages/inheritance-process.html` — **Step-by-Step California Trust Inheritance Workflow & Filing Checklist**
- `pages/verification-review.html` — **Line-by-Line Historical Audit & Flagged for Review**

---

## Reproducing Model Data

```bash
python3 scripts/generate_data.py
```

This regenerates `data/model_output.json` and `assets/data.js` with all `$10`-rounded projections and historical BOE CCPI audit results.
