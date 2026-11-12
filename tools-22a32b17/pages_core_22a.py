#!/usr/bin/env python3
"""Core decision & projection page builders (Pages 1-6) for desk-22a32b17."""
from __future__ import annotations

from typing import Dict

import layout_22a as L
import model_22a as m


def build_index_page() -> str:
    r40 = m.evaluate_strategies(2040, 25)
    r45 = m.evaluate_strategies(2045, 25)
    r50 = m.evaluate_strategies(2050, 25)
    a26 = m.property_a_annual_snapshot(2026, 2045)
    a45 = m.property_a_annual_snapshot(2045, 2045)
    b26 = m.property_b_annual_snapshot(2026, owner_occupied=True)

    max_w = r45["S3a"]["liquidated_wealth"]

    def bar_pct(val: float) -> int:
        return max(4, min(100, int(round((val / max_w) * 100))))

    body = f"""
    <div class="kpi-grid">
      <div class="kpi-card highlight">
        <div class="kpi-label">Recommended Strategy (2045 → 2070)</div>
        <div class="kpi-value">{m.fmt_money(r45['S3a']['liquidated_wealth'])}</div>
        <div class="kpi-note">Sell Property A at §1014 step-up (<strong>$0</strong> cap-gains tax) → stage into diversified equities while living in Property B Unit 3.</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Property A (Inherited via Trust)</div>
        <div class="kpi-value">{m.fmt_money(a26['fmv'])} <span style="font-size:0.86rem;font-weight:500;color:#475569;">(2026 est.)</span></div>
        <div class="kpi-note">Projected 2045 FMV: <strong>{m.fmt_money(a45['fmv'])}</strong> · Prop 19 occupy tax: <strong>{m.fmt_money(a45['tax_occ'])}/yr</strong> vs rental tax: <strong>{m.fmt_money(a45['tax_rent'])}/yr</strong>.</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Property B (Already Owned — 3 Units)</div>
        <div class="kpi-value">{m.fmt_money(b26['fmv'])} <span style="font-size:0.86rem;font-weight:500;color:#475569;">(2026 est.)</span></div>
        <div class="kpi-note">2 rented units yield <strong>{m.fmt_money(b26['gross_rent'])}/yr</strong> ({m.fmt_money(b26['gross_rent']/12)}/mo); 3rd unit owner-usable without losing rent.</div>
      </div>
      <div class="kpi-card warn">
        <div class="kpi-label">2026–2027 Federal Estate Headroom</div>
        <div class="kpi-value">{L.stat('$15,000,000')} / {L.stat('$15,480,000')}</div>
        <div class="kpi-note">CA &amp; local inheritance tax: <strong>$0</strong>. Liquid headroom above Property A in 2026: <strong>$11,900,000</strong> single (<strong>$26,900,000</strong> w/ DSUE).</div>
      </div>
    </div>

    <section class="section">
      <h2>Executive Verdict &amp; Strategic Reasoning</h2>
      <div class="callout rec">
        <strong class="title">Primary Recommendation — Retain &amp; Occupy Property B Unit 3 + Sell Property A Under IRC §1014 Step-Up + Reinvest via 24–36 Month U.S. Treasury Ladder Into Global Equities (Strategy S3b → S3a)</strong>
        Because <strong>Property B</strong> is <em>already owned</em> by the beneficiary—delivering <strong>{m.fmt_money(b26['gross_rent'])}/yr</strong> across two leased units, an ultra-low Proposition 13 tax bill (<strong>{m.fmt_money(b26['tax'])}/yr</strong> baseline), and a dedicated 3rd unit for owner occupancy—housing is already solved at near-zero marginal cost. Conversely, <strong>Property A</strong> arrives via revocable trust at death with a full <strong>IRC §1014 date-of-death fair-market-value basis step-up</strong> (wiping out decades of embedded appreciation tax-free) while simultaneously losing most of its Proposition 13 shield under <strong>Proposition 19 (CA R&amp;TC §63.2)</strong>. Selling Property A promptly after transfer captures <strong>{m.fmt_money(r45['meta']['proceeds_transfer'])}</strong> net of ~5.5% transaction costs in the 2045 central case with <strong>$0 federal and $0 California capital-gains tax</strong>, outperforming renting Property A by <strong>{m.fmt_money(r45['S3a']['liquidated_wealth'] - r45['S2']['liquidated_wealth'])}</strong> and outperforming moving into Property A (with B Unit 3 unleased) by <strong>{m.fmt_money(r45['S3a']['liquidated_wealth'] - r45['S1a']['liquidated_wealth'])}</strong> over 25 years.
      </div>

      <div class="bar-list" aria-label="25-Year Post-Transfer Net Wealth Comparison (2045 Transfer to 2070)">
        <div class="bar-row">
          <div><strong>S3a · Sell A → Diversified Equities</strong></div>
          <div class="bar-track"><div class="bar-fill" style="width:{bar_pct(r45['S3a']['liquidated_wealth'])}%"></div></div>
          <div style="text-align:right;font-weight:700;">{m.fmt_money(r45['S3a']['liquidated_wealth'])}</div>
        </div>
        <div class="bar-row">
          <div><strong>S2 · Stay in B + Rent Out Property A</strong></div>
          <div class="bar-track"><div class="bar-fill alt" style="width:{bar_pct(r45['S2']['liquidated_wealth'])}%"></div></div>
          <div style="text-align:right;font-weight:700;">{m.fmt_money(r45['S2']['liquidated_wealth'])}</div>
        </div>
        <div class="bar-row">
          <div><strong>S3b · Sell A → U.S. Treasuries Only</strong></div>
          <div class="bar-track"><div class="bar-fill alt" style="width:{bar_pct(r45['S3b']['liquidated_wealth'])}%"></div></div>
          <div style="text-align:right;font-weight:700;">{m.fmt_money(r45['S3b']['liquidated_wealth'])}</div>
        </div>
        <div class="bar-row">
          <div><strong>S1b · Occupy A + Lease B's 3rd Unit</strong></div>
          <div class="bar-track"><div class="bar-fill warn" style="width:{bar_pct(r45['S1b']['liquidated_wealth'])}%"></div></div>
          <div style="text-align:right;font-weight:700;">{m.fmt_money(r45['S1b']['liquidated_wealth'])}</div>
        </div>
        <div class="bar-row">
          <div><strong>S1a · Occupy A + Keep B Unit 3 Vacant</strong></div>
          <div class="bar-track"><div class="bar-fill warn" style="width:{bar_pct(r45['S1a']['liquidated_wealth'])}%"></div></div>
          <div style="text-align:right;font-weight:700;">{m.fmt_money(r45['S1a']['liquidated_wealth'])}</div>
        </div>
      </div>

      <div class="callout warn">
        <strong class="title">Four Critical Guardrails Before Executing Any Option</strong>
        1. <strong>Verify Revocable vs. Irrevocable Trust Status Now (IRS Rev. Rul. 2023-2):</strong> If Property A was placed into an irrevocable grantor trust excluded from the federal gross estate, IRC §1014 step-up is <em>denied</em>—creating a <strong>$2,282,200+</strong> tax trap upon sale (<a href="flagged.html#F-03">Flag F-03</a>).<br>
        2. <strong>Never Sell Property B Instead of Property A:</strong> Property B receives <em>no</em> basis step-up at the settlor's death and faces San Francisco's tiered transfer tax (<strong>0.75%–2.25%</strong>) plus ~37.1% combined capital-gains tax.<br>
        3. <strong>Stage Sale Proceeds via U.S. Treasuries (24–36 Months):</strong> Our <a href="black-swan-economics.html">Black Swan Engine</a> proves that a post-sale 2000/2008 equity bear market (Regime R4) cuts a lump-sum equity investment by ~54%; staging via CA-tax-exempt U.S. Treasuries eliminates sequence-of-returns risk.<br>
        4. <strong>Audit Liquid Estate Headroom &amp; DSUE Portability:</strong> If the settlor's 2026 liquid portfolio exceeds <strong>~$5,740,000</strong> (single, no DSUE portability) at 6%/yr growth, combined house + cash crosses the projected 2045 federal 40% estate-tax threshold (<a href="inheritance-and-estate-tax.html">Estate &amp; Cash Tax</a>).
      </div>
    </section>

    <section class="section">
      <h2>Executive Comparison Across the 2040–2050 Inheritance Window (25-Year Post-Transfer Horizon)</h2>
      <p>Every figure below is rounded to the nearest <strong>$10</strong> and holds household housing consumption consistent (the beneficiary lives either in Property A under S1a/S1b or in Property B's unrented 3rd unit under S2/S3a/S3b, shifting the single {L.stat('$7,000')} California Homeowners' Exemption accordingly).</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Strategy</th>
              <th>Housing &amp; Tax Treatment</th>
              <th class="num">2040 → 2065 Net Wealth</th>
              <th class="num">2045 → 2070 Net Wealth</th>
              <th class="num">2050 → 2075 Net Wealth</th>
              <th class="num">2045 Year-1 Net Cash Flow</th>
              <th>Verification</th>
              <th>Official Sources</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>S3a · Sell A → Diversified Equities</strong></td>
              <td>Live in B Unit 3; sell A at §1014 FMV basis ($0 cap-gains tax); compound net proceeds at 5.6% after-tax drag.</td>
              <td class="num"><strong>{m.fmt_money(r40['S3a']['liquidated_wealth'])}</strong></td>
              <td class="num"><strong>{m.fmt_money(r45['S3a']['liquidated_wealth'])}</strong></td>
              <td class="num"><strong>{m.fmt_money(r50['S3a']['liquidated_wealth'])}</strong></td>
              <td class="num">{m.fmt_money(r45['S3a']['yr1_cf'])}</td>
              <td>{L.badge_model()}</td>
              <td>{L.cites([('S_IRS_BASIS', 'IRS §1014'), ('S_RTC_11911', 'R&TC §11911'), ('S_TSP_RET', 'TSP C Fund')])}</td>
            </tr>
            <tr>
              <td><strong>S2 · Stay in B + Rent Out Property A</strong></td>
              <td>Live in B Unit 3; lease A at market rent; 100% FMV reassessment under Prop 19; 27.5-yr §168 building depreciation + §1250 recapture.</td>
              <td class="num">{m.fmt_money(r40['S2']['liquidated_wealth'])}</td>
              <td class="num">{m.fmt_money(r45['S2']['liquidated_wealth'])}</td>
              <td class="num">{m.fmt_money(r50['S2']['liquidated_wealth'])}</td>
              <td class="num">{m.fmt_money(r45['S2']['yr1_cf'])}</td>
              <td>{L.badge_model()}</td>
              <td>{L.cites([('S_BOE_P19', 'BOE Prop 19'), ('S_IRS_P527', 'IRS Pub 527'), ('S_CIV_1947', 'Civ §1947.12')])}</td>
            </tr>
            <tr>
              <td><strong>S3b · Sell A → U.S. Treasury Savings</strong></td>
              <td>Live in B Unit 3; sell A at §1014 FMV basis; hold conservative U.S. Treasury ladder (CA state income-tax exempt; 2.5% net).</td>
              <td class="num">{m.fmt_money(r40['S3b']['liquidated_wealth'])}</td>
              <td class="num">{m.fmt_money(r45['S3b']['liquidated_wealth'])}</td>
              <td class="num">{m.fmt_money(r50['S3b']['liquidated_wealth'])}</td>
              <td class="num">{m.fmt_money(r45['S3b']['yr1_cf'])}</td>
              <td>{L.badge_model()}</td>
              <td>{L.cites([('S_IRS_P550', 'IRS Pub 550'), ('S_FED_FOMC', 'Fed FOMC'), ('S_TSP_RET', 'TSP G Fund')])}</td>
            </tr>
            <tr>
              <td><strong>S1b · Occupy A + Lease B's 3rd Unit</strong></td>
              <td>Move into A within 1 yr (Prop 19 partial exclusion + §121 at terminal sale); lease B Unit 3 (adds rent but locks in SF Rent Ordinance).</td>
              <td class="num">{m.fmt_money(r40['S1b']['liquidated_wealth'])}</td>
              <td class="num">{m.fmt_money(r45['S1b']['liquidated_wealth'])}</td>
              <td class="num">{m.fmt_money(r50['S1b']['liquidated_wealth'])}</td>
              <td class="num">{m.fmt_money(r45['S1b']['yr1_cf'])}</td>
              <td>{L.badge_model()}</td>
              <td>{L.cites([('S_BOE_PUB801', 'BOE Pub 801'), ('S_SF_RENT', 'SF Rent Board'), ('S_IRS_P523', 'IRS Pub 523')])}</td>
            </tr>
            <tr>
              <td><strong>S1a · Occupy A + Keep B Unit 3 Vacant</strong></td>
              <td>Move into A within 1 yr (Prop 19 partial exclusion); keep B's 2 rented units active and Unit 3 unleased for family/flex use.</td>
              <td class="num">{m.fmt_money(r40['S1a']['liquidated_wealth'])}</td>
              <td class="num">{m.fmt_money(r45['S1a']['liquidated_wealth'])}</td>
              <td class="num">{m.fmt_money(r50['S1a']['liquidated_wealth'])}</td>
              <td class="num">{m.fmt_money(r45['S1a']['yr1_cf'])}</td>
              <td>{L.badge_model()}</td>
              <td>{L.cites([('S_BOE_PUB801', 'BOE Pub 801'), ('S_BOE_266', 'BOE-266'), ('S_IRS_P523', 'IRS Pub 523')])}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <h2>Baseline Asset &amp; Statutory Snapshot (Verified November 12, 2026)</h2>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Parameter</th>
              <th>Property A (Inherited Santa Clara County SFR)</th>
              <th>Property B (Already-Owned San Francisco 3-Unit)</th>
              <th>Official Record Status</th>
              <th>Primary Authority</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Ownership &amp; Transfer Posture</strong></td>
              <td>Held by settlor's trust; transfers to beneficiary at death (~2040–2050).</td>
              <td>Already owned by beneficiary; unaffected by settlor's death.</td>
              <td>{L.badge_unverified('F-03', 'Deed/Trust Blank')}</td>
              <td>{L.cites([('S_PROB_16061', 'Prob. Code §16061.7'), ('S_BOE_LTA26026', 'BOE LTA 2026/026')])}</td>
            </tr>
            <tr>
              <td><strong>Nov 2026 Market Value Baseline</strong></td>
              <td><strong>$3,100,000</strong> (planning baseline; parcel appraisal blank: <code>—</code>)</td>
              <td><strong>$1,800,000</strong> (planning baseline; parcel appraisal blank: <code>—</code>)</td>
              <td>{L.badge_model()} · {L.badge_unverified('F-04', 'Appraisal Blank')}</td>
              <td>{L.cites([('S_FHFA_HPI', 'FHFA HPI'), ('S_SCC_AR', 'SCC Assessor')])}</td>
            </tr>
            <tr>
              <td><strong>Current County Roll Assessed Value</strong></td>
              <td><code>—</code> (blank; modeled on banded <strong>$550,000</strong> FBYV baseline)</td>
              <td><code>—</code> (blank; modeled on banded <strong>$114,000</strong> roll + direct charges)</td>
              <td>{L.badge_unverified('F-01', 'Roll Blank')}</td>
              <td>{L.cites([('S_BOE_PUB800', 'BOE Pub 800-10'), ('S_SF_TAX', 'SF Treasurer')])}</td>
            </tr>
            <tr>
              <td><strong>2026 Annual Property Tax Baseline</strong></td>
              <td><strong>$7,210/yr</strong> (1.19% ad valorem + $660 fixed direct charges)</td>
              <td><strong>$2,440/yr</strong> (1.18162182% SF rate + $1,090 fixed charges; reconciled in F-01)</td>
              <td>{L.badge_model()} · {L.badge_unverified('F-01', 'Bill Blank')}</td>
              <td>{L.cites([('S_SCC_AR', 'SCC Assessor'), ('S_SF_TAX', 'SF Treasurer 1.18162182%')])}</td>
            </tr>
            <tr>
              <td><strong>Income Basis Step-Up at Settlor's Death</strong></td>
              <td><strong>100% Date-of-Death FMV</strong> under IRC §1014 (if revocable trust / estate-included).</td>
              <td><strong>None ($0 step-up)</strong> — already owned by beneficiary.</td>
              <td>{L.badge_verified()}</td>
              <td>{L.cites([('S_IRS_BASIS', 'IRS §1014 FAQ'), ('S_IRS_RR2302', 'Rev. Rul. 2023-2')])}</td>
            </tr>
            <tr>
              <td><strong>Prop 19 Reassessment at Settlor's Death</strong></td>
              <td>Partial exclusion only if both settlor &amp; beneficiary occupy as principal residence (allowance {L.stat('$1,044,586')} through Feb 15, 2027); 100% FMV if rented.</td>
              <td><strong>No reassessment</strong> — no change in ownership occurs on Property B.</td>
              <td>{L.badge_verified()}</td>
              <td>{L.cites([('S_BOE_PUB801', 'BOE Pub 801'), ('S_RTC_632', 'R&TC §63.2')])}</td>
            </tr>
            <tr>
              <td><strong>Rental Income &amp; Occupancy Capacity</strong></td>
              <td>Unrented today; modeled at <strong>$68,400/yr</strong> ($5,700/mo) if leased post-transfer.</td>
              <td><strong>$85,800/yr</strong> ($7,150/mo) from 2 leased units + 3rd unit free for owner occupancy.</td>
              <td>{L.badge_model()} · {L.badge_unverified('F-07', 'Lease Roll Blank')}</td>
              <td>{L.cites([('S_SF_RENT', 'SF Rent Board'), ('S_CIV_1947', 'Civ. Code §1947.12')])}</td>
            </tr>
            <tr>
              <td><strong>Utilities &amp; Solar Baseline (2026)</strong></td>
              <td>Water <strong>$1,500/yr</strong> ($100–$150/mo); Solar electricity <strong>-$180/yr</strong> (-$10 to -$20/mo net credit pre-NEM sunset).</td>
              <td>Water/sewer <strong>$4,380/yr</strong> ($330–$400/mo across 3 units); Common/owner electricity <strong>$600/yr</strong> ($30–$70/mo).</td>
              <td>{L.badge_model()} · {L.badge_unverified('F-09', 'Tariff Blank')}</td>
              <td>{L.cites([('S_CPUC_NEM', 'CPUC NEM/NBT'), ('S_SFPUC', 'SFPUC Prop 218')])}</td>
            </tr>
            <tr>
              <td><strong>Researched Insurance &amp; Maintenance (2026)</strong></td>
              <td>Insurance <strong>$3,200/yr</strong> HO-3 (<strong>$3,800/yr</strong> DP-3 rental); Maintenance <strong>$12,400/yr</strong> (0.40% of FMV).</td>
              <td>3-unit habitational insurance <strong>$4,200/yr</strong>; Maintenance <strong>$14,400/yr</strong> (0.80% of FMV — older multi-unit).</td>
              <td>{L.badge_model()} · {L.badge_unverified('F-08', 'Policy Blank')}</td>
              <td>{L.cites([('S_CDI_SIS', 'CDI Oct 2026'), ('S_CDI_RES', 'CDI Res. Guide')])}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
    """
    return L.render_page(
        "index.html",
        "Executive Decision Summary",
        "Two-Property California Inheritance Strategy (2026–2076)",
        "Line-by-line verified analysis comparing living in, renting out, or selling an inherited Santa Clara County single-family home (Property A) alongside an already-owned San Francisco County 3-unit residential building (Property B), rounded to the nearest $10 and stress-tested across 50 years of real-world economic regimes.",
        body,
    )


def build_properties_page() -> str:
    # Worked Prop 19 projections for 2026, 2040, 2045, 2050
    p = m.DEFAULT_PARAMS
    p19_rows = []
    for yr in (2026, 2040, 2045, 2050):
        t = yr - m.BASE_YEAR
        fmv = p.a_fmv_2026 * ((1.0 + p.home_growth_a) ** t)
        fbyv = p.a_fbyv_2026 * ((1.0 + p.prop13_cap) ** t)
        allow = m.prop19_allowance_at(yr, p)
        cap = fbyv + allow
        new_occ = m.prop19_new_taxable(fmv, fbyv, allow)
        direct = p.a_direct_charges_2026 * ((1.0 + 0.015) ** t)
        tax_occ = max(new_occ - 7_000.0, 0.0) * p.a_ad_valorem_rate + direct
        tax_rent = fmv * p.a_ad_valorem_rate + direct
        savings = tax_rent - tax_occ
        allow_str = L.stat("$1,044,586") if yr == 2026 else m.fmt_money(allow)
        badge = L.badge_verified("Statutory 2026 Allowance") if yr == 2026 else L.badge_model()
        p19_rows.append(f"""
            <tr>
              <td><strong>{yr}</strong></td>
              <td class="num">{m.fmt_money(fmv)}</td>
              <td class="num">{m.fmt_money(fbyv)}</td>
              <td class="num">{allow_str}</td>
              <td class="num">{m.fmt_money(cap)}</td>
              <td class="num"><strong>{m.fmt_money(new_occ)}</strong></td>
              <td class="num">{m.fmt_money(tax_occ)}</td>
              <td class="num">{m.fmt_money(tax_rent)}</td>
              <td class="num">{m.fmt_money(savings)}/yr</td>
              <td>{badge}</td>
              <td>{L.cites([('S_BOE_PUB801', 'BOE Pub 801'), ('S_SCC_P19', 'SCC Prop 19')])}</td>
            </tr>""")

    ccpi_rows = []
    for fy, ccpi_raw, shown, factor in m.BOE_CCPI_RECENT:
        sub2 = "Sub-2% CCPI Year" if factor != "1.02000" else "Capped at 2.00%"
        ccpi_rows.append(f"""
            <tr>
              <td><strong>{L.esc(fy)}</strong></td>
              <td class="num">{L.stat(ccpi_raw)}</td>
              <td class="num">{L.stat(shown)}</td>
              <td class="num">{L.stat(factor)}</td>
              <td>{L.esc(sub2)}</td>
              <td>{L.badge_verified()}</td>
              <td>{L.cite('S_BOE_LTA26002', 'BOE LTA 2026/002')}</td>
            </tr>""")

    body = f"""
    <section class="section">
      <h2>1. Core Legal &amp; Tax Asymmetry: Inherited Property A vs. Already-Owned Property B</h2>
      <p>The single most important structural fact in this decision is that <strong>Property A</strong> (single-family home in Santa Clara County) is being <em>inherited at death via trust</em>, whereas <strong>Property B</strong> (3-unit building in San Francisco County) is <em>already owned by the beneficiary today</em>. Under federal and California tax law, those two postures produce completely opposite tax incentives:</p>
      <div class="two-col">
        <div class="callout rec">
          <strong class="title">Property A — High Reassessment Risk, Zero Sale Tax at Death</strong>
          At the settlor's death, Property A undergoes a <strong>change in ownership</strong> under CA R&amp;TC §60/§63.2 (triggering massive property-tax reassessment even WITH Proposition 19's partial allowance because its multi-million-dollar value far exceeds FBYV + {L.stat('$1,044,586')}). Simultaneously, under <strong>IRC §1014(a)</strong>, Property A's income-tax basis resets to <strong>100% of date-of-death FMV</strong>—meaning an immediate sale pays <strong>$0 federal and $0 California capital-gains tax</strong> and only {L.stat('$0.55')} per {L.stat('$500')} (0.11%) county transfer tax.
        </div>
        <div class="callout info">
          <strong class="title">Property B — Protected Prop 13 Tax Base, Heavy Tax Penalty if Sold</strong>
          Because the beneficiary already owns Property B, the settlor's death triggers <strong>zero reassessment</strong> (keeping its ~<strong>$2,440/yr</strong> property tax bill intact) and <strong>zero IRC §1014 basis step-up</strong>. Selling Property B would trigger ~37.1% combined federal + California capital-gains/recapture taxes on embedded gain PLUS San Francisco's steep tiered transfer tax (<strong>0.75%</strong> at $1M–$5M; <strong>2.25%</strong> at $5M–$10M), while forfeiting <strong>$85,800/yr</strong> in 2-unit rent and a free owner-occupiable 3rd unit.
        </div>
      </div>
    </section>

    <section class="section">
      <h2>2. Proposition 19 Formula &amp; Property A Reassessment Schedule (2026, 2040, 2045, 2050)</h2>
      <p>Under <strong>California Constitution Article XIII A, §2.1</strong> and <strong>R&amp;TC §63.2</strong> (effective February 16, 2021), an inherited property avoids full reassessment <em>only</em> if: (1) it was the transferor's principal residence, (2) the child moves in as their principal residence within <strong>1 year</strong> of death and files Form <strong>BOE-266</strong> ({L.stat('$7,000')} Homeowners' Exemption), and (3) Form <strong>BOE-19-P</strong> is filed within <strong>3 years</strong>. Even when all three tests are met, the excluded value is capped at <code>Factored Base Year Value + Adjusted Allowance</code> ({L.stat('$1,044,586')} for transfers Feb 16, 2025 – Feb 15, 2027 per BOE LTA 2025/009; next biennial adjustment Feb 16, 2027). Any FMV above that cap is added dollar-for-dollar to the old FBYV.</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Transfer Year</th>
              <th class="num">Projected FMV</th>
              <th class="num">Pre-Death FBYV</th>
              <th class="num">Prop 19 Allowance</th>
              <th class="num">Excluded Cap</th>
              <th class="num">New Taxable (Occupy)</th>
              <th class="num">Year-1 Tax (Occupy)</th>
              <th class="num">Year-1 Tax (Rent / Non-Occ.)</th>
              <th class="num">Prop 19 Annual Tax Savings</th>
              <th>Status</th>
              <th>Official Sources</th>
            </tr>
          </thead>
          <tbody>
            {"".join(p19_rows)}
          </tbody>
        </table>
      </div>
      <div class="callout warn">
        <strong class="title">Crucial Takeaway on Proposition 19's Shrinking Relative Shield</strong>
        Even if the beneficiary moves into Property A in 2045 and qualifies for Proposition 19, Property A's annual property tax still jumps more than <strong>6x</strong>—from <strong>$10,130/yr</strong> pre-death to <strong>$62,190/yr</strong>—because home appreciation at 4.2%/yr outpaces the 2.0%/yr FBYV cap and ~2.2%/yr allowance indexing. Prop 19 saves <strong>$19,290/yr</strong> relative to renting Property A (<strong>$81,490/yr</strong>), but it does <em>not</em> preserve the settlor's low property-tax bill, and per <strong>BOE LTA 2026/026 (Q&amp;A 29)</strong> moving out in any later year immediately terminates the exclusion as of the next January 1 lien date!
      </div>
    </section>

    <section class="section">
      <h2>3. Official County Roll Audit, Tax-Rate Reconciliation &amp; Transfer-Tax Comparison</h2>
      <p>To strictly prevent parcel-level identification via public county tax lookup tools, exact parcel assessment histories are omitted (left blank <code>—</code> where unverified from official deeds/bills) and reconciled below against official county rates.</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Audit Item</th>
              <th>Official Verified Rule / Rate</th>
              <th>Confirmed Parcel Record</th>
              <th>Planning Model Treatment ($10-Rounded)</th>
              <th>Status</th>
              <th>Official Sources</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Property A Tax Rate &amp; Direct Charges</strong></td>
              <td>Prop 13 1.00% base + Santa Clara County voter-approved local debt (~0.19%) + fixed parcel/special assessments.</td>
              <td class="blank">—</td>
              <td>Modeled as <strong>1.19%</strong> ad valorem on taxable value + <strong>$660/yr</strong> fixed direct assessments (<strong>$7,210/yr</strong> 2026 baseline) so fixed parcel charges are not falsely multiplied 12x upon reassessment.</td>
              <td>{L.badge_unverified('F-02', 'TRA Bill Blank')}</td>
              <td>{L.cites([('S_SCC_AR', 'SCC Annual Report'), ('S_BOE_PUB800', 'BOE Pub 800-10')])}</td>
            </tr>
            <tr>
              <td><strong>Property B Secured Rate Reconciliation</strong></td>
              <td>San Francisco FY 2026–2027 secured property tax rate is exactly {L.stat('1.18162182%')}.</td>
              <td class="blank">—</td>
              <td>Banded <strong>$114,000</strong> roll × 1.18162182% = <strong>$1,350/yr</strong> ad valorem (less {L.stat('$7,000')} HOX = <strong>$1,260/yr</strong>) + <strong>$1,180/yr</strong> fixed parcel/Rent Board/special charges = <strong>$2,440/yr</strong> rounded total.</td>
              <td>{L.badge_unverified('F-01', 'SF Bill Blank')}</td>
              <td>{L.cites([('S_SF_TAX', 'SF Treasurer'), ('S_BOE_HOX', 'BOE HOX')])}</td>
            </tr>
            <tr>
              <td><strong>Single Homeowners' Exemption Rule</strong></td>
              <td>CA Const. Art. XIII §3(k) grants {L.stat('$7,000')} taxable-value reduction on <em>one</em> principal residence per household (Form BOE-266).</td>
              <td class="blank">—</td>
              <td>Claimed on Property B Unit 3 in S2/S3a/S3b; terminated on Property B (by Dec 10) and filed on Property A in S1a/S1b.</td>
              <td>{L.badge_verified()}</td>
              <td>{L.cites([('S_BOE_HOX', 'BOE HOX'), ('S_BOE_266', 'Form BOE-266')])}</td>
            </tr>
            <tr>
              <td><strong>Transfer Tax at Trust Distribution (Death)</strong></td>
              <td>CA R&amp;TC §11930 exempts transfers by gift or by reason of death (outright or via trust) from documentary transfer tax.</td>
              <td><strong>$0</strong> (Statutory)</td>
              <td><strong>$0</strong> transfer tax at inheritance deed recording.</td>
              <td>{L.badge_verified()}</td>
              <td>{L.cites([('S_RTC_11930', 'R&TC §11930'), ('S_SF_TT', 'SF Transfer Tax')])}</td>
            </tr>
            <tr>
              <td><strong>Transfer Tax on Market Sale — Property A vs. B</strong></td>
              <td>Santa Clara County general law county rate: {L.stat('$0.55')} per {L.stat('$500')} (<strong>0.11%</strong>); charter-city surtaxes apply only inside charter cities. San Francisco tiered rate: <strong>0.75%</strong> ($1M–$5M), <strong>2.25%</strong> ($5M–$10M), <strong>5.50%</strong> ($10M–$25M).</td>
              <td class="blank">—</td>
              <td>Property A 2045 sale ({m.fmt_money(6_774_050)}): <strong>$7,450</strong> county transfer tax (charter-city applicability flagged in F-05). Selling Property B at $5M+ would cost <strong>$112,500+</strong> in SF transfer tax alone.</td>
              <td>{L.badge_verified()} · {L.badge_unverified('F-05', 'City Tier Blank')}</td>
              <td>{L.cites([('S_RTC_11911', 'R&TC §11911'), ('S_SF_TT', 'SF Transfer Tax')])}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <h2>4. Official BOE 2014–2027 California CPI &amp; Proposition 13 Inflation Factors (LTA 2026/002)</h2>
      <p>Verified directly from <strong>BOE Letter to Assessors No. 2026/002 (January 13, 2026)</strong>, California's assessment roll did <em>not</em> compound at a flat 2.00% every year: three fiscal years between 2014–15 and 2026–27 fell below 2% (compounding to 23.51% over 12 years vs. 26.82% at a constant 2%/yr), while high-inflation years such as 2023–24 ({L.stat('7.274%')} CCPI) were capped at {L.stat('1.02000')}.</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Assessment Roll Year</th>
              <th class="num">Oct–Oct California CPI Change</th>
              <th class="num">Rounded % Change</th>
              <th class="num">Enacted Prop 13 Factor</th>
              <th>Regime Classification</th>
              <th>Status</th>
              <th>Official Source</th>
            </tr>
          </thead>
          <tbody>
            {"".join(ccpi_rows)}
          </tbody>
        </table>
      </div>
    </section>
    """
    return L.render_page(
        "properties-and-tax.html",
        "Asset & Property-Tax Mechanics",
        "Property A vs. Property B: Proposition 13, Proposition 19 & Basis Rules",
        "Detailed legal reconciliation of Santa Clara County single-family Property A (inherited via trust) and San Francisco County 3-unit Property B (already owned), verified against BOE Publication 801, LTA 2026/002, LTA 2026/026, R&TC §63.2, and IRC §1014.",
        body,
    )


def build_operating_costs_page() -> str:
    a26 = m.property_a_annual_snapshot(2026, 2045)
    a45 = m.property_a_annual_snapshot(2045, 2045)
    b26 = m.property_b_annual_snapshot(2026, True)
    b45 = m.property_b_annual_snapshot(2045, True)

    body = f"""
    <section class="section">
      <h2>1. 2026 &amp; 2045 Annual Operating Cost Comparison ($10-Rounded)</h2>
      <p>Every operating cost category supplied by the owner has been cross-checked against official California utility tariffs (<strong>CPUC Net Billing Tariff / NEM</strong> and <strong>SFPUC Proposition 218 FY 2026–2028 Water &amp; Sewer Schedule</strong>) and residential insurance market data (<strong>California Department of Insurance Sustainable Insurance Strategy, updated October 27, 2026</strong>). Unverified private bills and policy declarations remain blank (<code>—</code>) in the confirmed-record column and are flagged on <a href="flagged.html">Flagged for Review</a>.</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Expense / Revenue Line</th>
              <th>Confirmed Bill / Policy</th>
              <th class="num">Property A (2026)</th>
              <th class="num">Property A (2045 Occupy)</th>
              <th class="num">Property A (2045 Rental)</th>
              <th class="num">Property B 3-Unit (2026)</th>
              <th class="num">Property B 3-Unit (2045)</th>
              <th>Status</th>
              <th>Official Sources</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Secured Property Tax + Direct Charges</strong></td>
              <td class="blank">—</td>
              <td class="num">{m.fmt_money(a26['tax_occ'])}</td>
              <td class="num">{m.fmt_money(a45['tax_occ'])}</td>
              <td class="num">{m.fmt_money(a45['tax_rent'])}</td>
              <td class="num">{m.fmt_money(b26['tax'])}</td>
              <td class="num">{m.fmt_money(b45['tax'])}</td>
              <td>{L.badge_model()} · {L.badge_unverified('F-01', 'Tax Bill')}</td>
              <td>{L.cites([('S_BOE_PUB801', 'BOE Pub 801'), ('S_SF_TAX', 'SF Treasurer')])}</td>
            </tr>
            <tr>
              <td><strong>Property Insurance (HO-3 Primary vs. DP-3 / 3-Unit Rental)</strong></td>
              <td class="blank">—</td>
              <td class="num">{m.fmt_money(a26['ins_occ'])}</td>
              <td class="num">{m.fmt_money(a45['ins_occ'])}</td>
              <td class="num">{m.fmt_money(a45['ins_rent'])}</td>
              <td class="num">{m.fmt_money(b26['ins'])}</td>
              <td class="num">{m.fmt_money(b45['ins'])}</td>
              <td>{L.badge_model()} · {L.badge_unverified('F-08', 'Policy Dec')}</td>
              <td>{L.cites([('S_CDI_SIS', 'CDI Oct 2026'), ('S_CDI_RES', 'CDI Res. Guide')])}</td>
            </tr>
            <tr>
              <td><strong>Water &amp; Wastewater Tariff</strong></td>
              <td class="blank">—</td>
              <td class="num">{m.fmt_money(a26['water'])}<br><small>($100–$150/mo)</small></td>
              <td class="num">{m.fmt_money(a45['water'])}</td>
              <td class="num">{m.fmt_money(a45['water'])}</td>
              <td class="num">{m.fmt_money(b26['water'])}<br><small>($330–$400/mo)</small></td>
              <td class="num">{m.fmt_money(b45['water'])}</td>
              <td>{L.badge_model()} · {L.badge_unverified('F-09', 'Water Bill')}</td>
              <td>{L.cites([('S_SFPUC', 'SFPUC Prop 218'), ('S_BLS_CPI', 'BLS CPI')])}</td>
            </tr>
            <tr>
              <td><strong>Electricity &amp; Rooftop Solar (NEM → NBT Transition)</strong></td>
              <td class="blank">—</td>
              <td class="num">{m.fmt_money(a26['elec'])}<br><small>(-$10 to -$20/mo)</small></td>
              <td class="num">{m.fmt_money(a45['elec'])}<br><small>(post-NEM sunset)</small></td>
              <td class="num">{m.fmt_money(a45['elec'])}</td>
              <td class="num">{m.fmt_money(b26['elec'])}<br><small>($30–$70/mo)</small></td>
              <td class="num">{m.fmt_money(b45['elec'])}</td>
              <td>{L.badge_model()} · {L.badge_unverified('F-10', 'NEM PTO Date')}</td>
              <td>{L.cites([('S_CPUC_NEM', 'CPUC D.22-12-056'), ('S_BLS_CPI', 'BLS CPI')])}</td>
            </tr>
            <tr>
              <td><strong>Repairs, Maintenance &amp; Capital Reserve</strong></td>
              <td class="blank">—</td>
              <td class="num">{m.fmt_money(a26['maint'])}<br><small>(0.40% FMV)</small></td>
              <td class="num">{m.fmt_money(a45['maint'])}</td>
              <td class="num">{m.fmt_money(a45['maint'])}</td>
              <td class="num">{m.fmt_money(b26['maint'])}<br><small>(0.80% FMV)</small></td>
              <td class="num">{m.fmt_money(b45['maint'])}</td>
              <td>{L.badge_model()} · {L.badge_unverified('F-11', 'CapEx Log')}</td>
              <td>{L.cites([('S_IRS_P527', 'IRS Pub 527'), ('S_FHFA_HPI', 'FHFA HPI')])}</td>
            </tr>
            <tr>
              <td><strong>Total Annual Carrying Cost (Before Rent)</strong></td>
              <td class="blank">—</td>
              <td class="num"><strong>{m.fmt_money(a26['carry_occ'])}</strong></td>
              <td class="num"><strong>{m.fmt_money(a45['carry_occ'])}</strong></td>
              <td class="num"><strong>{m.fmt_money(a45['tax_rent'] + a45['ins_rent'] + a45['water'] + a45['elec'] + a45['maint'] + a45['vac_mgmt'])}</strong></td>
              <td class="num"><strong>{m.fmt_money(b26['opex_total'])}</strong></td>
              <td class="num"><strong>{m.fmt_money(b45['opex_total'])}</strong></td>
              <td>{L.badge_model()}</td>
              <td>{L.cites([('S_IRS_P527', 'IRS Pub 527'), ('S_BOE_PUB801', 'BOE Pub 801')])}</td>
            </tr>
            <tr>
              <td><strong>Gross Annual Rental Income</strong></td>
              <td class="blank">—</td>
              <td class="num">—</td>
              <td class="num">—</td>
              <td class="num">{m.fmt_money(a45['gross_rent'])}</td>
              <td class="num">{m.fmt_money(b26['gross_rent'])}</td>
              <td class="num">{m.fmt_money(b45['gross_rent'])}</td>
              <td>{L.badge_model()} · {L.badge_unverified('F-07', 'Rent Roll')}</td>
              <td>{L.cites([('S_SF_RENT', 'SF Rent Board'), ('S_IRS_P527', 'IRS Pub 527')])}</td>
            </tr>
            <tr>
              <td><strong>Pre-Income-Tax Net Operating Cash Flow</strong></td>
              <td class="blank">—</td>
              <td class="num">-{m.fmt_money(a26['carry_occ'])}</td>
              <td class="num">-{m.fmt_money(a45['carry_occ'])}</td>
              <td class="num"><strong>{m.fmt_money(a45['noi_rent'])}</strong></td>
              <td class="num"><strong>{m.fmt_money(b26['noi'])}</strong></td>
              <td class="num"><strong>{m.fmt_money(b45['noi'])}</strong></td>
              <td>{L.badge_model()}</td>
              <td>{L.cites([('S_IRS_P527', 'IRS Pub 527'), ('S_SF_RENT', 'SF Rent Board')])}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <h2>2. Researched Insurance Analysis: Primary Residence (HO-3) vs. Multi-Unit Rental Dwelling</h2>
      <p>The owner's preliminary placeholder (~$1,500/yr) closely mirrors the <strong>California Department of Insurance (CDI) October 27, 2026</strong> statewide homeowner average of {L.stat('$1,571')} (<strong>$1,570</strong> rounded to $10; national average {L.stat('$1,512')} / <strong>$1,510</strong> rounded). However, statewide averages include small inland homes and condominium policies. Under CDI's <em>Residential Insurance Guide (Rev. Jan 2026)</em>, dwelling Coverage A must cover <strong>full structure replacement cost</strong> (not land value, which is uninsured, but Bay Area high-skill construction rebuild cost):</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Coverage Type</th>
              <th>Published Agency Benchmark</th>
              <th class="num">Researched 2026 Baseline ($10-Rounded)</th>
              <th>Key Underwriting &amp; Coverage Drivers</th>
              <th>Status</th>
              <th>Official Sources</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Statewide Homeowner Benchmark</strong></td>
              <td>CA avg {L.stat('$1,571')}/yr; US avg {L.stat('$1,512')}/yr; <strong>677,449</strong> FAIR Plan policies in force.</td>
              <td class="num">$1,570/yr</td>
              <td>CDI Sustainable Insurance Strategy enables forward catastrophe modeling + reinsurance cost pass-through in return for distressed-area writing commitments.</td>
              <td>{L.badge_verified()}</td>
              <td>{L.cite('S_CDI_SIS', 'CDI Oct 27, 2026')}</td>
            </tr>
            <tr>
              <td><strong>Property A — Primary Residence (HO-3)</strong></td>
              <td>Coverage A–F owner-occupied replacement cost policy.</td>
              <td class="num"><strong>$3,200/yr</strong></td>
              <td>Sized for ~2,200–2,500 sq ft Santa Clara County single-family rebuild (~$1.15M–$1.35M Coverage A); excludes earthquake &amp; flood unless endorsed.</td>
              <td>{L.badge_model()} · {L.badge_unverified('F-08', 'Sq Ft / Quote')}</td>
              <td>{L.cites([('S_CDI_RES', 'CDI Res. Guide'), ('S_CDI_SIS', 'CDI SIS')])}</td>
            </tr>
            <tr>
              <td><strong>Property A — Non-Owner Landlord Dwelling (DP-3)</strong></td>
              <td>Landlord fire/dwelling + loss-of-rents + premises liability.</td>
              <td class="num"><strong>$3,800/yr</strong></td>
              <td>Tenant-occupied DP-3 carries ~15%–25% higher liability/dwelling loading than owner-occupied HO-3 plus recommended umbrella coverage.</td>
              <td>{L.badge_model()}</td>
              <td>{L.cites([('S_CDI_RES', 'CDI Res. Guide'), ('S_IRS_P527', 'IRS Pub 527')])}</td>
            </tr>
            <tr>
              <td><strong>Property B — 3-Unit Habitational / Landlord Policy</strong></td>
              <td>Multi-family wood-frame structure + 2–3 unit landlord liability + loss of rents.</td>
              <td class="num"><strong>$4,200/yr</strong></td>
              <td>Older 3-unit San Francisco wood-frame construction requires commercial/habitational multi-family underwriting well above single-family averages.</td>
              <td>{L.badge_model()} · {L.badge_unverified('F-08', 'Policy Dec')}</td>
              <td>{L.cites([('S_CDI_RES', 'CDI Res. Guide'), ('S_CDI_SIS', 'CDI SIS')])}</td>
            </tr>
            <tr>
              <td><strong>Optional Earthquake Endorsement / CEA Sensitivity</strong></td>
              <td>Excluded from standard HO-3/DP-3 per CDI; USGS 30-yr Bay Area M≥6.7 probability = <strong>72%</strong>.</td>
              <td class="num">$3,500–$7,500/yr<br><small>(10%–15% deductible)</small></td>
              <td>High deductibles (~$120,000–$200,000 out-of-pocket before payout) mean self-insuring via liquid reserves or diversifying out of Property A is critical; modeled explicitly in <a href="black-swan-economics.html">Regime R5</a>.</td>
              <td>{L.badge_verified('Hazard Verified')}</td>
              <td>{L.cites([('S_USGS_EQ', 'USGS UCERF3'), ('S_CDI_RES', 'CDI Res. Guide')])}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <h2>3. Utility &amp; Solar Tariff Mechanics: Why 2045 Looks Different From 2026</h2>
      <div class="two-col">
        <div class="callout info">
          <strong class="title">Property A Solar: Legacy NEM Credit Today → CPUC Net Billing Tariff Tomorrow</strong>
          Today Property A enjoys a <strong>$0 to -$20/mo</strong> net electricity credit (modeled at <strong>-$180/yr</strong>), characteristic of legacy Net Energy Metering (NEM 1.0/2.0) retail export credits and annual Net Surplus Compensation (~$0.02–$0.03/kWh). Under <strong>CPUC Decision 22-12-056</strong> (effective April 15, 2023), legacy NEM grandfathering lasts <strong>20 years from original interconnection PTO</strong> (<a href="flagged.html#F-10">Flag F-10</a>). Before or during the 2040–2050 inheritance window, the system transitions to the <strong>Solar Billing Plan (Net Billing Tariff)</strong> with avoided-cost export rates, mandatory TOU rates, fixed monthly base charges, and inverter/battery replacement (~15–25 yr life), shifting net electricity from <strong>-$180/yr</strong> to <strong>+$600/yr</strong> (2026 dollars).
        </div>
        <div class="callout warn">
          <strong class="title">Property B Water &amp; Rent Squeeze: SFPUC +12.5%/yr vs. SF Rent Board 1.6%</strong>
          Owner-paid water &amp; sewer across Property B's 3 units (<strong>$330–$400/mo</strong> = <strong>$4,380/yr</strong> midpoint) is governed by <strong>SFPUC's Proposition 218 tariff</strong>, which enacted ~7% water and ~15% wastewater hikes for FY 2026–27 (~12.5% combined residential bill increase) and another ~12.5% for FY 2027–28 to fund capital infrastructure. Meanwhile, Property B's 2 rented units are capped by the <strong>SF Rent Board</strong> at <strong>1.6%</strong> (Mar 1, 2026 – Feb 28, 2027; 60% of Bay Area CPI). Our model escalates Property B water at 3.5%/yr vs. 2.0%/yr rent growth to capture this structural operating margin compression.
        </div>
      </div>
    </section>
    """
    return L.render_page(
        "operating-costs.html",
        "Utilities, Insurance & Upkeep",
        "Operating Cost Verification: Solar NEM/NBT, Multi-Unit Water & Insurance",
        "Verification and long-horizon projection of water, electricity/solar, repairs, and primary homeowner vs. multi-unit rental dwelling insurance for Property A and Property B.",
        body,
    )


def build_estate_tax_page() -> str:
    p = m.DEFAULT_PARAMS
    thresh_rows = []
    for yr in (2026, 2027, 2030, 2035, 2040, 2045, 2050, 2076):
        t = yr - m.BASE_YEAR
        fmv_a = p.a_fmv_2026 * ((1.0 + p.home_growth_a) ** t)
        ex_s = m.federal_estate_exclusion_at(yr, p)
        ex_m = ex_s * 2.0
        head_s = ex_s - fmv_a
        head_m = ex_m - fmv_a
        if yr in (2026, 2027):
            ex_s_str = L.stat(f"${int(ex_s):,}")
            ex_m_str = L.stat(f"${int(ex_m):,}")
            st_badge = L.badge_verified(f"Statutory {yr}")
            srcs = [('S_IRS_WN', 'IRS P.L. 119-21'), ('S_IRS_2027', 'Rev. Proc. 2026-35')]
        else:
            ex_s_str = m.fmt_money(ex_s)
            ex_m_str = m.fmt_money(ex_m)
            st_badge = L.badge_model("Projected 2.5% CPI")
            srcs = [('S_IRS_2027', 'Rev. Proc. 2026-35'), ('S_CBO_2026', 'CBO Outlook')]
        thresh_rows.append(f"""
            <tr>
              <td><strong>{yr}</strong></td>
              <td class="num"><strong>$0</strong></td>
              <td class="num"><strong>$0</strong></td>
              <td class="num">{ex_s_str}</td>
              <td class="num">{ex_m_str}</td>
              <td class="num">{m.fmt_money(fmv_a)}</td>
              <td class="num"><strong>{m.fmt_money(head_s)}</strong></td>
              <td class="num">{m.fmt_money(head_m)}</td>
              <td>{st_badge}</td>
              <td>{L.cites(srcs + [('S_SCO_EST', 'CA SCO')])}</td>
            </tr>""")

    liq_rows_html = []
    for row in m.liquid_inheritance_matrix(2045, 0.060, p):
        head_str = (
            f"{m.fmt_money(row['headroom_single'])} remaining"
            if row["headroom_single"] >= 0
            else f"<strong style='color:#991b1b;'>Exceeds by {m.fmt_money(abs(row['headroom_single']))}</strong>"
        )
        liq_rows_html.append(f"""
            <tr>
              <td class="num"><strong>{m.fmt_money(row['liq_2026'])}</strong></td>
              <td class="num">{m.fmt_money(row['liq_tr'])}</td>
              <td class="num">{m.fmt_money(row['fmv_a'])}</td>
              <td class="num"><strong>{m.fmt_money(row['gross_estate'])}</strong></td>
              <td class="num">{head_str}</td>
              <td class="num"><strong>{m.fmt_money(row['tax_single'])}</strong></td>
              <td class="num">{m.fmt_money(row['net_heir_single'])}</td>
              <td class="num">{m.fmt_money(row['tax_married'])}</td>
              <td>{L.badge_model()} · {L.badge_unverified('F-12', 'Estate Size Blank')}</td>
              <td>{L.cites([('S_IRS_I706', 'Form 706 (40%)'), ('S_IRS_FAQ', 'IRS DSUE FAQ')])}</td>
            </tr>""")

    body = f"""
    <div class="kpi-grid">
      <div class="kpi-card highlight">
        <div class="kpi-label">Local &amp; California Inheritance / Estate Tax</div>
        <div class="kpi-value">$0 / $0</div>
        <div class="kpi-note">CA repealed its inheritance tax in 1982 and eliminated its estate pick-up tax on Jan 1, 2005 (CA SCO &amp; FTB).</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">2026 &amp; 2027 Federal Estate Exclusions</div>
        <div class="kpi-value">{L.stat('$15,000,000')} → {L.stat('$15,480,000')}</div>
        <div class="kpi-note">P.L. 119-21 set $15M for 2026; IRS Rev. Proc. 2026-35 (Nov 5, 2026) indexed 2027 to $15.48M ($30.96M married w/ DSUE).</div>
      </div>
      <div class="kpi-card warn">
        <div class="kpi-label">2026 Liquid Headroom Above Property A</div>
        <div class="kpi-value">$11,900,000</div>
        <div class="kpi-note">$15,000,000 exclusion minus $3,100,000 Property A = $11.90M tax-free liquid cash today ($26.90M w/ spouse DSUE).</div>
      </div>
      <div class="kpi-card warn">
        <div class="kpi-label">2026 Liquid Portfolio That Hits 2045 Cap</div>
        <div class="kpi-value">~$5,740,000</div>
        <div class="kpi-note">Growing at 6.0%/yr, $5.74M in 2026 reaches $17.37M by 2045—exhausting a single settlor's projected $24.14M exclusion once Property A ($6.77M) is added!</div>
      </div>
    </div>

    <section class="section">
      <h2>1. Three-Tier Tax Rules on Inherited Cash, Securities &amp; Real Estate</h2>
      <p>The inheritance includes both <strong>Property A</strong> and a <strong>substantial liquid portfolio</strong>. Below are the exact verified rules at the local, California state, and federal levels as of November 12, 2026:</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Jurisdiction &amp; Tax Type</th>
              <th>Statutory Threshold (2026 / 2027)</th>
              <th>Tax Rate Above Threshold</th>
              <th>Key Legal &amp; Filing Mechanics</th>
              <th>Status</th>
              <th>Official Sources</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Local (County / Municipal) Inheritance or Estate Tax</strong></td>
              <td><strong>None ($0 tax)</strong></td>
              <td><strong>0%</strong></td>
              <td>No California county or municipality levies an estate or inheritance tax; death transfers via trust or probate are exempt from documentary transfer tax under CA R&amp;TC §11930.</td>
              <td>{L.badge_verified()}</td>
              <td>{L.cites([('S_RTC_11930', 'R&TC §11930'), ('S_SF_TT', 'SF Recorder')])}</td>
            </tr>
            <tr>
              <td><strong>California State Estate &amp; Inheritance Tax</strong></td>
              <td><strong>None ($0 tax)</strong></td>
              <td><strong>0%</strong></td>
              <td>CA inheritance tax repealed June 8, 1982; CA estate pick-up tax phased out Jan 1, 2005. Nov 2026 Prop 42 (leading 51.4% Yes, unofficial) further bars new state personal-property/wealth taxes.</td>
              <td>{L.badge_verified()}</td>
              <td>{L.cites([('S_SCO_EST', 'CA Controller'), ('S_SOS_2026', 'CA SOS Prop 42')])}</td>
            </tr>
            <tr>
              <td><strong>Federal Estate &amp; Lifetime Gift Tax (IRC §2001 / §2010)</strong></td>
              <td>2026: {L.stat('$15,000,000')} single ({L.stat('$30,000,000')} w/ DSUE)<br>2027: {L.stat('$15,480,000')} single ({L.stat('$30,960,000')} w/ DSUE)</td>
              <td><strong>40%</strong> marginal rate (Table A, Form 706)</td>
              <td>Public Law 119-21 permanently raised the base exclusion and indexed it for inflation starting 2027. Prior lifetime taxable gifts above the annual exclusion ({L.stat('$19,000')} in 2026; {L.stat('$20,000')} in 2027) reduce remaining estate headroom dollar-for-dollar.</td>
              <td>{L.badge_verified()}</td>
              <td>{L.cites([('S_IRS_WN', 'IRS P.L. 119-21'), ('S_IRS_2027', 'Rev. Proc. 2026-35'), ('S_IRS_I706', 'Form 706')])}</td>
            </tr>
            <tr>
              <td><strong>Federal &amp; CA Income Tax on Inherited Cash / Brokerage</strong></td>
              <td><strong>100% Excluded from Income</strong> (IRC §102)</td>
              <td><strong>0%</strong> on principal; post-death yield taxed normally</td>
              <td>Receiving cash or stepped-up taxable brokerage shares triggers <strong>$0 income tax</strong>; only interest, dividends, and post-death gains earned <em>after</em> death are taxable.</td>
              <td>{L.badge_verified()}</td>
              <td>{L.cites([('S_FTB_INH', 'FTB Inheritance'), ('S_IRS_BASIS', 'IRS §1014 FAQ')])}</td>
            </tr>
            <tr>
              <td><strong>Pre-Tax Retirement Accounts (Traditional IRA / 401(k)) — Critical Exception!</strong></td>
              <td><strong>$0 Income-Tax Exclusion</strong> (IRC §691 IRD)</td>
              <td>Up to <strong>50.3%</strong> combined (37% Fed + 13.3% CA)</td>
              <td>Unlike cash or brokerage stock, inherited Traditional IRAs/401(k)s receive <strong>NO §1014 basis step-up</strong> and generally must be distributed within 10 years as ordinary taxable income (<a href="flagged.html#F-13">Flag F-13</a>).</td>
              <td>{L.badge_verified()} · {L.badge_unverified('F-13', 'IRA Mix Blank')}</td>
              <td>{L.cites([('S_IRS_P550', 'IRS Pub 550'), ('S_FTB_RATES', 'FTB 2026 Schedules')])}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <h2>2. Projected Federal Estate-Tax Threshold &amp; Remaining Liquid Headroom (2026–2076)</h2>
      <p>Anchored to the enacted 2026 ({L.stat('$15,000,000')}) and 2027 ({L.stat('$15,480,000')}) statutory exclusions and indexed at 2.5%/yr baseline CPI thereafter, this table shows exactly how much <strong>liquid cash and securities</strong> can pass alongside Property A before a single dollar of 40% federal estate tax is owed:</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Year</th>
              <th class="num">Local Tax</th>
              <th class="num">CA Estate Tax</th>
              <th class="num">Federal Exclusion (Single)</th>
              <th class="num">Federal Exclusion (Married DSUE)</th>
              <th class="num">Projected Property A FMV</th>
              <th class="num">Liquid Headroom (Single)</th>
              <th class="num">Liquid Headroom (Married DSUE)</th>
              <th>Status</th>
              <th>Official Sources</th>
            </tr>
          </thead>
          <tbody>
            {"".join(thresh_rows)}
          </tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <h2>3. 2045 Liquid Inheritance Sensitivity Matrix: When Does the 40% Federal Penalty Hit?</h2>
      <p>Because the actual size of the settlor's liquid portfolio is private and unverified (left blank <code>—</code> in confirmed records, <a href="flagged.html#F-12">Flag F-12</a>), the matrix below models seven 2026 liquid portfolio sizes compounding at <strong>6.0%/yr</strong> alongside Property A to 2045. Notice the exact inflection point at <strong>$5,740,000</strong> in 2026 liquid assets:</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th class="num">2026 Liquid Portfolio</th>
              <th class="num">2045 Projected Liquid Value (6%/yr)</th>
              <th class="num">2045 Property A FMV</th>
              <th class="num">2045 Combined Gross Estate</th>
              <th class="num">Headroom vs. $24,143,520 Single Cap</th>
              <th class="num">40% Estate Tax (Single / No DSUE)</th>
              <th class="num">Net to Beneficiary (Single)</th>
              <th class="num">40% Estate Tax (Married w/ DSUE)</th>
              <th>Status</th>
              <th>Official Sources</th>
            </tr>
          </thead>
          <tbody>
            {"".join(liq_rows_html)}
          </tbody>
        </table>
      </div>
      <div class="callout rec">
        <strong class="title">Actionable Estate-Tax Shield Checklist</strong>
        1. <strong>Preserve Spousal DSUE Portability (Form 706):</strong> If the settlor had or has a spouse, filing Form 706 upon the first spouse's death (within 9 months + 6-month Form 4768 extension, or within <strong>5 years</strong> under <strong>IRS Rev. Proc. 2022-32</strong> if below the filing threshold) doubles the 2045 tax-free threshold from <strong>$24,143,520</strong> to <strong>$48,287,030</strong>—saving up to <strong>$9,657,410</strong> in federal estate tax!<br>
        2. <strong>Use Annual Tax-Free Gifts ({L.stat('$19,000')} in 2026; {L.stat('$20,000')} in 2027) Only From Cash, Never Low-Basis Real Estate:</strong> Annual exclusion gifts of cash reduce a taxable estate without touching the lifetime exemption, whereas gifting Property A during life forfeits the IRC §1014 basis step-up.
      </div>
    </section>
    """
    return L.render_page(
        "inheritance-and-estate-tax.html",
        "Estate, Gift & Cash Inheritance Tax",
        "Local, State & Federal Inheritance Thresholds, Headroom & 2026–2076 Projections",
        "Exact statutory tax thresholds, remaining liquid inheritance headroom above Property A, 2027 IRS inflation adjustments (Rev. Proc. 2026-35), spousal DSUE portability impact, and Traditional IRA income-in-respect-of-decedent traps.",
        body,
    )


def build_decision_page() -> str:
    r40 = m.evaluate_strategies(2040, 25)
    r45 = m.evaluate_strategies(2045, 25)
    r50 = m.evaluate_strategies(2050, 25)
    no_step = m.evaluate_strategies(2045, 25, step_up_applies=False, carryover_basis_a=250_000.0)

    # Sensitivity grid across equity after-tax return vs home appreciation (2045 -> 2070)
    sens_rows = []
    for eq_net in (0.030, 0.040, 0.056, 0.070):
        for hg in (0.028, 0.042, 0.055):
            custom_p = m.ModelParams(equity_after_tax=eq_net, home_growth_a=hg)
            res = m.evaluate_strategies(2045, 25, p=custom_p)
            w_s1a = res["S1a"]["liquidated_wealth"]
            w_s2 = res["S2"]["liquidated_wealth"]
            w_s3a = res["S3a"]["liquidated_wealth"]
            winner = max(
                [("S1a Occupy A", w_s1a), ("S2 Rent A", w_s2), ("S3a Sell → Equities", w_s3a)],
                key=lambda x: x[1],
            )[0]
            is_base = (abs(eq_net - 0.056) < 1e-6 and abs(hg - 0.042) < 1e-6)
            tag = " <strong>(Central Baseline)</strong>" if is_base else ""
            sens_rows.append(f"""
            <tr>
              <td>{m.fmt_pct(eq_net, 1)} after-tax{tag}</td>
              <td>{m.fmt_pct(hg, 1)}/yr</td>
              <td class="num">{m.fmt_money(w_s1a)}</td>
              <td class="num">{m.fmt_money(w_s2)}</td>
              <td class="num"><strong>{m.fmt_money(w_s3a)}</strong></td>
              <td><strong>{L.esc(winner)}</strong></td>
              <td>{L.badge_model()}</td>
              <td>{L.cites([('S_FHFA_HPI', 'FHFA HPI'), ('S_TSP_RET', 'TSP Returns')])}</td>
            </tr>""")

    def detail_rows(res: Dict[str, Dict[str, float]], label: str) -> str:
        out = []
        names = [
            ("S3a", "Sell A → Diversified Equities", [('S_IRS_BASIS', 'IRS §1014'), ('S_TSP_RET', 'TSP C Fund')]),
            ("S2", "Stay in B + Rent Out A", [('S_BOE_P19', 'BOE Prop 19'), ('S_IRS_P527', 'IRS Pub 527')]),
            ("S3b", "Sell A → U.S. Treasuries", [('S_IRS_P550', 'IRS Pub 550'), ('S_FED_FOMC', 'Fed FOMC')]),
            ("S1b", "Occupy A + Lease B Unit 3", [('S_BOE_PUB801', 'BOE Pub 801'), ('S_SF_RENT', 'SF Rent Board')]),
            ("S1a", "Occupy A + B Unit 3 Vacant", [('S_BOE_PUB801', 'BOE Pub 801'), ('S_IRS_P523', 'IRS Pub 523')]),
        ]
        for code, nm, srcs in names:
            d = res[code]
            out.append(f"""
            <tr>
              <td><strong>{L.esc(label)}</strong></td>
              <td><strong>{code} · {L.esc(nm)}</strong></td>
              <td class="num">{m.fmt_money(d['yr1_cf'])}</td>
              <td class="num">{m.fmt_money(d['side_portfolio'])}</td>
              <td class="num">{m.fmt_money(d['hold_net_worth'])}</td>
              <td class="num">{m.fmt_money(d['terminal_tax'])}</td>
              <td class="num"><strong>{m.fmt_money(d['liquidated_wealth'])}</strong></td>
              <td>{L.badge_model()}</td>
              <td>{L.cites(srcs)}</td>
            </tr>""")
        return "".join(out)

    body = f"""
    <section class="section">
      <h2>1. Full 25-Year Post-Transfer Comparison Across 2040, 2045 &amp; 2050 Inheritance Years</h2>
      <p>Both <strong>Hold-Without-Sale Net Worth</strong> (if Property A is kept for the next generation without paying selling costs or capital-gains tax) and <strong>Post-Liquidation After-Tax Wealth</strong> (net of selling costs, IRC §121 exclusion on S1a/S1b, and IRC §1250 25% federal + 13.3% CA depreciation recapture on S2) are reported side by side:</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Window</th>
              <th>Strategy</th>
              <th class="num">Year-1 Net Cash Flow</th>
              <th class="num">25-Yr Liquid Portfolio</th>
              <th class="num">Hold-Without-Sale Net Worth</th>
              <th class="num">Terminal Sale Cap-Gains Tax</th>
              <th class="num">Post-Liquidation Net Wealth</th>
              <th>Status</th>
              <th>Official Sources</th>
            </tr>
          </thead>
          <tbody>
            {detail_rows(r40, "2040 → 2065")}
            {detail_rows(r45, "2045 → 2070")}
            {detail_rows(r50, "2050 → 2075")}
          </tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <h2>2. Why Renting Property A (S2) Trails Selling (S3a) — And What Changes Under Rev. Rul. 2023-2</h2>
      <div class="two-col">
        <div class="callout info">
          <strong class="title">The Silicon Valley Price-to-Rent + Prop 19 Compression</strong>
          In 2045, Property A's projected value is <strong>{m.fmt_money(r45['meta']['fmv_transfer'])}</strong> while gross market rent is <strong>$119,940/yr</strong> (1.77% gross yield). Because non-occupancy forfeits Proposition 19, secured property tax jumps to <strong>$81,490/yr</strong>—consuming <strong>68% of gross rent</strong> before insurance, maintenance, or vacancy! Even with <strong>{m.fmt_money(r45['meta']['cum_depr_s2'])}</strong> of 27.5-year building depreciation shielding annual rent from income tax, net pre-tax cash yield is ~0.16%/yr on equity.
        </div>
        <div class="callout flag">
          <strong class="title">The Rev. Rul. 2023-2 Irrevocable Trust Exception (Critical Check!)</strong>
          If Property A was placed in an <em>irrevocable grantor trust</em> excluded from the settlor's federal gross estate, <strong>IRS Revenue Ruling 2023-2</strong> denies the IRC §1014 basis step-up. Selling in 2045 with a $250,000 carryover basis triggers <strong>{m.fmt_money(no_step['S3a']['terminal_tax'])}</strong> in immediate 37.1% capital-gains tax—slashing S3a's 2070 terminal wealth from <strong>{m.fmt_money(r45['S3a']['liquidated_wealth'])}</strong> down to <strong>{m.fmt_money(no_step['S3a']['liquidated_wealth'])}</strong> (a <strong>{m.fmt_money(r45['S3a']['liquidated_wealth'] - no_step['S3a']['liquidated_wealth'])}</strong> wealth loss!). Always verify revocable trust inclusion before listing Property A (<a href="flagged.html#F-03">Flag F-03</a>).
        </div>
      </div>
    </section>

    <section class="section">
      <h2>3. Crossover Sensitivity Grid: Equity Return vs. Home Appreciation (2045 → 2070)</h2>
      <p>At what return threshold does keeping and renting Property A beat selling and investing in equities? Only when 25-year after-tax equity compounding falls to ~<strong>3.0%–3.5%/yr</strong> simultaneously with sustained <strong>5.5%+/yr</strong> single-family appreciation:</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>After-Tax Equity Return</th>
              <th>Property A Annual Appreciation</th>
              <th class="num">S1a Occupy A (2070)</th>
              <th class="num">S2 Rent A (2070)</th>
              <th class="num">S3a Sell → Equities (2070)</th>
              <th>Winning Strategy</th>
              <th>Status</th>
              <th>Official Sources</th>
            </tr>
          </thead>
          <tbody>
            {"".join(sens_rows)}
          </tbody>
        </table>
      </div>
    </section>
    """
    return L.render_page(
        "decision-scenarios.html",
        "Scenario & Sensitivity Modeling",
        "Decision Matrix Across 2040, 2045 & 2050 Inheritance Windows",
        "Complete household net-wealth comparison across all five strategies, showing hold-vs-liquidate wealth, IRC §121 and §1250 tax effects, Rev. Rul. 2023-2 carryover-basis risk, and equity-vs-housing return crossovers.",
        body,
    )


def build_projections_page() -> str:
    rows_a = []
    rows_b = []
    for yr in range(m.BASE_YEAR, m.END_YEAR + 1):
        a = m.property_a_annual_snapshot(yr, transfer_year=2045)
        b = m.property_b_annual_snapshot(yr, owner_occupied=True)
        phase_note = (
            "Pre-transfer (settlor roll)"
            if yr < 2045
            else ("Inheritance year (Prop 19 / FMV reset)" if yr == 2045 else "Post-transfer (+2% cap)")
        )
        rows_a.append(f"""
            <tr>
              <td><strong>{yr}</strong></td>
              <td>{phase_note}</td>
              <td class="num">{m.fmt_money(a['fmv'])}</td>
              <td class="num">{m.fmt_money(a['assess_occ'])}</td>
              <td class="num">{m.fmt_money(a['tax_occ'])}</td>
              <td class="num">{m.fmt_money(a['assess_rent'])}</td>
              <td class="num">{m.fmt_money(a['tax_rent'])}</td>
              <td class="num">{m.fmt_money(a['ins_occ'])}</td>
              <td class="num">{m.fmt_money(a['water'] + a['elec'])}</td>
              <td class="num">{m.fmt_money(a['maint'])}</td>
              <td class="num">{m.fmt_money(a['carry_occ'])}</td>
              <td class="num">{m.fmt_money(a['noi_rent'])}</td>
              <td>{L.badge_model()}</td>
              <td>{L.cites([('S_BOE_PUB801', 'BOE Pub 801'), ('S_CPUC_NEM', 'CPUC'), ('S_CDI_SIS', 'CDI')])}</td>
            </tr>""")
        rows_b.append(f"""
            <tr>
              <td><strong>{yr}</strong></td>
              <td class="num">{m.fmt_money(b['fmv'])}</td>
              <td class="num">{m.fmt_money(b['fbyv'])}</td>
              <td class="num">{m.fmt_money(b['tax'])}</td>
              <td class="num">{m.fmt_money(b['ins'])}</td>
              <td class="num">{m.fmt_money(b['water'])}</td>
              <td class="num">{m.fmt_money(b['elec'])}</td>
              <td class="num">{m.fmt_money(b['maint'])}</td>
              <td class="num">{m.fmt_money(b['gross_rent'])}</td>
              <td class="num">{m.fmt_money(b['opex_total'])}</td>
              <td class="num"><strong>{m.fmt_money(b['noi'])}</strong></td>
              <td>{L.badge_model()}</td>
              <td>{L.cites([('S_SF_TAX', 'SF Tax'), ('S_SF_RENT', 'SF Rent'), ('S_SFPUC', 'SFPUC')])}</td>
            </tr>""")

    body = f"""
    <section class="section">
      <h2>1. Property A — Year-by-Year 50-Year Projection Table (2026–2076, Central 2045 Inheritance)</h2>
      <p>Every single annual figure from 2026 through 2076 (51 annual snapshots) is rounded to the nearest <strong>$10</strong>. Notice two structural inflection points: (1) in <strong>2038</strong>, legacy 20-year NEM solar grandfathering transitions to the CPUC Solar Billing Plan (+base services charge), turning net electricity from a small credit into a positive utility cost; and (2) in <strong>2045</strong>, death triggers either the Proposition 19 partial reassessment (if occupied within 1 year) or 100% FMV reassessment (if rented out).</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Year</th>
              <th>Roll Phase</th>
              <th class="num">Projected FMV</th>
              <th class="num">Taxable (Occupy)</th>
              <th class="num">Tax (Occupy)</th>
              <th class="num">Taxable (Rental)</th>
              <th class="num">Tax (Rental)</th>
              <th class="num">HO-3 Ins.</th>
              <th class="num">Water + Solar/Elec</th>
              <th class="num">Maint.</th>
              <th class="num">Occupy Total Carry</th>
              <th class="num">Rental Pre-Tax NOI</th>
              <th>Status</th>
              <th>Official Sources</th>
            </tr>
          </thead>
          <tbody>
            {"".join(rows_a)}
          </tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <h2>2. Property B (Already-Owned 3-Unit Building) — Year-by-Year 50-Year Projection Table (2026–2076)</h2>
      <p>Because Property B is already owned by the beneficiary (2 units rented at <strong>$85,800/yr</strong> in 2026, 3rd unit occupied by owner with {L.stat('$7,000')} Homeowners' Exemption), no reassessment occurs at the settlor's death. Observe how Proposition 13 caps ad valorem tax growth at ≤2.0%/yr while SFPUC water/sewer (3.5%/yr) and older-building maintenance (2.5%/yr) gradually rise relative to rent-controlled 2-unit revenue (2.0%/yr).</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Year</th>
              <th class="num">Projected FMV</th>
              <th class="num">Prop 13 Roll Base</th>
              <th class="num">Property Tax</th>
              <th class="num">3-Unit Ins.</th>
              <th class="num">3-Unit Water/Sewer</th>
              <th class="num">Common Elec.</th>
              <th class="num">Maint. (0.8%)</th>
              <th class="num">2-Unit Gross Rent</th>
              <th class="num">Total OpEx + Tax</th>
              <th class="num">Pre-Tax NOI</th>
              <th>Status</th>
              <th>Official Sources</th>
            </tr>
          </thead>
          <tbody>
            {"".join(rows_b)}
          </tbody>
        </table>
      </div>
    </section>
    """
    return L.render_page(
        "projections-50yr.html",
        "Annual Cash-Flow & Assessment Ledger",
        "Year-by-Year 50-Year Projections (2026–2076): Property A & Property B",
        "Complete annual schedules of market value, assessed taxable value, property taxes, insurance, water/sewer, solar/electricity (including legacy NEM sunset), maintenance, rents, and net operating cash flows, rounded to the nearest $10.",
        body,
    )
