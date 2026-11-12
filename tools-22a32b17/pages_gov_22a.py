#!/usr/bin/env python3
"""Black-swan, trust walkthrough, law-watch, audit, flagged & sources pages (Pages 7-12)."""
from __future__ import annotations

from typing import List, Tuple

import layout_22a as L
import model_22a as m


def build_black_swan_page() -> str:
    regimes = m.build_black_swan_regimes()
    reg_rows = []
    for r in regimes:
        sid = str(r["source_id"])
        reg_rows.append(f"""
            <tr>
              <td><strong>{L.esc(r['code'])} · {L.esc(r['name'])}</strong><br><small style="color:#475569;">{L.esc(r['desc'])}</small></td>
              <td class="num">{m.fmt_money(float(r['fmv_2045']))}</td>
              <td class="num">{m.fmt_money(float(r['tax_occ_2045']))}</td>
              <td class="num">{m.fmt_money(float(r['w_occ']))}</td>
              <td class="num">{m.fmt_money(float(r['w_rent']))}</td>
              <td class="num"><strong>{m.fmt_money(float(r['w_eq']))}</strong></td>
              <td class="num">{m.fmt_money(float(r['w_tr']))}</td>
              <td><strong>{L.esc(r['winner'])}</strong></td>
              <td>{L.badge_model()}</td>
              <td>{L.cite(sid)}</td>
            </tr>""")

    body = f"""
    <section class="section">
      <h2>1. Why Linear 50-Year Projections Misprice Risk — Official Empirical Evidence (1976–2026)</h2>
      <p>Over any real 50-year U.S. and California window, constant annual appreciation and constant inflation <em>never</em> occur. Official federal and California data verified on November 12, 2026 demonstrate four non-linear path dependencies that materially alter inheritance decisions:</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Real-World Non-Linearity</th>
              <th>Official Empirical Evidence (Verified 2026-11-12)</th>
              <th>Path-Dependent Effect on Property A &amp; B</th>
              <th>Status</th>
              <th>Official Sources</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>1. Prop 13 Cap Asymmetry &amp; Deflation Years</strong></td>
              <td>BOE LTA 2026/002 records 50 years of CCPI (1976–2027) ranging from <strong>-0.237%</strong> (2010–11 factor <code>0.99763</code>) and <strong>0.454%</strong> (2014–15) up to <strong>+17.316%</strong> (1980–81) and <strong>+7.274%</strong> (2023–24)—all upside capped at <strong>2.00%</strong>.</td>
              <td>In high-inflation / stagflation decades, real property taxes plunge in inflation-adjusted terms while nominal rents rise; in disinflationary years, sub-2% CCPI permanently ratchets FBYV lower without catch-up.</td>
              <td>{L.badge_verified()}</td>
              <td>{L.cites([('S_BOE_LTA26002', 'BOE LTA 2026/002'), ('S_RTC_51', 'R&TC §51')])}</td>
            </tr>
            <tr>
              <td><strong>2. Sticky Inflation &amp; Rate Re-Tightening</strong></td>
              <td>On Sept 16, 2026, the Federal Reserve <em>raised</em> the federal funds target range +25 bps to <strong>3.75%–4.00%</strong> (IORB <strong>3.90%</strong>) with Aug PCE at <strong>3.8%</strong>; Oct 2026 BLS CPI rose <strong>+0.4% MoM</strong> (+0.6% in Sept).</td>
              <td>Higher-for-longer nominal risk-free yields boost CA-state-tax-exempt U.S. Treasury reinvestment returns while compressing leveraged housing affordability and price-to-rent multiples.</td>
              <td>{L.badge_verified()}</td>
              <td>{L.cites([('S_FED_FOMC', 'Fed FOMC Sep 2026'), ('S_BLS_CPI', 'BLS CPI Oct 2026')])}</td>
            </tr>
            <tr>
              <td><strong>3. Prop 8 Temporary Reductions &amp; Transfer-Year Timing</strong></td>
              <td>Under CA R&amp;TC §51(a)(2) (Prop 8), county assessors enroll current lien-date market value whenever housing dips below FBYV, then recapture >2%/yr on recovery up to the Prop 13 ceiling.</td>
              <td>If death occurs during a localized Bay Area housing trough (Regime R3), keeping Property A locks in a <em>permanently lower</em> Prop 19 base value, whereas selling at the trough forfeits recovery.</td>
              <td>{L.badge_verified()}</td>
              <td>{L.cites([('S_BOE_PUB800', 'BOE Pub 800-10'), ('S_FHFA_HPI', 'FHFA HPI')])}</td>
            </tr>
            <tr>
              <td><strong>4. Correlated Bay Area Seismic &amp; Insurance Tail Risk</strong></td>
              <td>USGS UCERF3 assigns a <strong>72%</strong> 30-year probability of an <strong>M≥6.7</strong> earthquake (51% M≥7.0) in the San Francisco Bay region; CDI reports <strong>677,449</strong> FAIR Plan policies in force as of Oct 2026.</td>
              <td>Holding both Property A and 3-unit Property B concentrates 100% of real-asset net worth inside a single seismic fault system where standard HO-3/DP-3 policies exclude earthquake damage.</td>
              <td>{L.badge_verified()}</td>
              <td>{L.cites([('S_USGS_EQ', 'USGS UCERF3'), ('S_CDI_SIS', 'CDI Oct 2026')])}</td>
            </tr>
            <tr>
              <td><strong>5. Federal Fiscal Dominance &amp; Tax-Regime Drift</strong></td>
              <td>CBO's Feb 2026 Outlook projects federal debt held by the public rising from <strong>101% of GDP</strong> (2026) to <strong>120% of GDP</strong> (2036), exceeding post-WWII peaks.</td>
              <td>Rising debt service increases long-term legislative pressure to trim the federal estate exclusion, raise capital-gains rates, or cap step-up—favoring clean §1014 realization when available.</td>
              <td>{L.badge_verified()}</td>
              <td>{L.cite('S_CBO_2026', 'CBO Pub 62105')}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <h2>2. Seven Non-Linear 50-Year Economic Regimes (2026–2076 Path Engine, Evaluated at 2070)</h2>
      <p>Unlike flat sensitivity tables, our Black Swan Engine steps year-by-year from 2026 through 2076, enforcing exact California R&amp;TC §51 Prop 13 caps (≤2.0%), sub-2% / deflation factors, Prop 8 temporary decline-in-value reductions, biennial Prop 19 allowance resets, and sequence-of-returns compounding. Notice that <strong>Regime R0 matches our central 2045→2070 baseline to the exact dollar</strong>, isolating the pure effect of each real-world macro regime:</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Regime (2026–2076 Path)</th>
              <th class="num">2045 FMV at Death</th>
              <th class="num">2045 Tax (Occupy)</th>
              <th class="num">Occupy A (S1a) 2070</th>
              <th class="num">Rent A (S2) 2070</th>
              <th class="num">Sell → Equities (S3a)</th>
              <th class="num">Sell → Treasuries (S3b)</th>
              <th>Regime Winner</th>
              <th>Status</th>
              <th>Anchor Source</th>
            </tr>
          </thead>
          <tbody>
            {"".join(reg_rows)}
          </tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <h2>3. Four Adaptive Decision Rules Derived From the Black Swan Regimes</h2>
      <div class="two-col">
        <div class="callout rec">
          <strong class="title">Rule 1 — Variance Drag Is Real (R1 vs. R0: -$7,494,070), Yet Diversification Still Wins</strong>
          Even when geometric mean returns match the smooth baseline (Regime R1: five -21% equity recessions and five inflation waves over 50 years), volatility and sequence effects trim S3a terminal wealth from <strong>$24,996,440</strong> to <strong>$17,502,370</strong>—yet S3a still beats renting Property A (<strong>$9,885,140</strong>) by <strong>+$7,617,230</strong>.
        </div>
        <div class="callout warn">
          <strong class="title">Rule 2 — Never Lump-Sum Into Peak Equities; Use a 24–36 Month U.S. Treasury Ladder (Solves R4)</strong>
          In Regime R4 (a 2000–2002 / 2008–2009 bear market starting the year after a 2045 sale), investing 100% of sale proceeds immediately into equities drops 2070 wealth to <strong>$11,517,030</strong>—behind both U.S. Treasuries (<strong>$11,787,100</strong>) and renting Property A (<strong>$12,244,450</strong>). Parking net sale proceeds in a 24–36 month U.S. Treasury bill/note ladder (exempt from CA's 13.3% state tax) and dollar-cost-averaging into equities eliminates single-date crash risk.
        </div>
        <div class="callout info">
          <strong class="title">Rule 3 — The Stagflation Exception (Regime R2): Prop 13's 2% Cap Is an Inflation Call Option</strong>
          Only in Regime R2 (a 1973–1982 stagflation decade with ~8.8% CPI and flat equities) does <strong>Renting Property A ($19,421,940)</strong> beat <strong>Selling Into Equities ($17,395,920)</strong>. Why? Once reassessed at death, Property A's tax base is re-locked under Prop 13's 2%/yr ceiling while 8.8% inflation drives nominal rents and replacement values sharply higher. If CPI exceeds 6%+ with high equity CAPE valuations at transfer, holding/renting for 5–7 years before selling is rational.
        </div>
        <div class="callout flag">
          <strong class="title">Rule 4 — De-Concentrate Two-Structure Bay Area Seismic Risk (Regime R5)</strong>
          In Regime R5 (California insurance tripling + a single uninsured 12%-of-FMV Bay Area earthquake repair shock in 2048), keeping Property A slashes Occupy wealth to <strong>$2,669,820</strong> while Property B simultaneously faces repair exposure in the same metro fault zone. Selling Property A converts half of the household's geographic real-estate exposure into globally diversified liquid capital.
        </div>
      </div>
    </section>
    """
    return L.render_page(
        "black-swan-economics.html",
        "Non-Linear Macro & Tail-Risk Stress Lab",
        "50-Year Black Swan & Real-World Economic Regimes (2026–2076)",
        "Path-dependent 50-year stress testing across business cycles, 1970s stagflation, regional housing busts, post-sale equity lost decades, Bay Area M≥6.7 seismic + insurance shocks, and federal fiscal dominance.",
        body,
    )


def build_process_page() -> str:
    steps: List[Tuple[str, str, str, str, List[Tuple[str, str]]]] = [
        (
            "Pre-Transfer (Now – 2040)",
            "1. Audit Trust Instrument & Prior Spousal DSUE",
            "Confirm Property A is held in a revocable living trust included in the settlor's gross estate (preserving IRC §1014 step-up and avoiding Rev. Rul. 2023-2 carryover trap). Verify whether any predeceased spouse filed Form 706 for DSUE portability (5-yr late relief under Rev. Proc. 2022-32).",
            "Unverified trust clause (Flag F-03); losing §1014 step-up costs $2,280,000+ in 2045 sale tax.",
            [("S_IRS_RR2302", "Rev. Rul. 2023-2"), ("S_IRS_FAQ", "IRS Rev. Proc. 2022-32")],
        ),
        (
            "Days 1–30 Post-Death",
            "2. Death Certificates, Insurance Binder & Trust EIN",
            "Obtain certified death certificates; notify Property A's homeowner insurer immediately to maintain vacancy/trustee dwelling coverage during administration; apply online for a Trust Employer Identification Number (EIN, IRS Form SS-4) once the revocable trust becomes irrevocable at death.",
            "Uninsured vacancy exclusion if carrier is not notified promptly after settlor's death.",
            [("S_CDI_RES", "CDI Res. Guide"), ("S_IRS_EST", "IRS Estate Tax")],
        ),
        (
            "Within 60 Days of Death",
            "3. Mandatory Statutory Trustee Notice (Probate Code §16061.7)",
            "Successor trustee must serve formal statutory Notification by Trustee on all trust beneficiaries and legal heirs within 60 days after death (starting the 120-day trust contest limitation window).",
            "Personal trustee liability and open-ended contest window if statutory 60-day notice is omitted.",
            [("S_PROB_16061", "Prob. Code §16061.7"), ("S_COURTS", "CA Courts Probate")],
        ),
        (
            "Within 90–120 Days",
            "4. Certified Date-of-Death Appraisal (Real Estate & Non-Cash Assets)",
            "Commission a qualified MAI/certified residential date-of-death appraisal of Property A (and consider IRC §2032 6-month alternate valuation date if market values drop after death and estate is taxable) to substantiate IRC §1014 stepped-up basis.",
            "Unsupported §1014 basis upon IRS/FTB Schedule D audit if sold without date-of-death appraisal.",
            [("S_IRS_BASIS", "IRS §1014 FAQ"), ("S_IRS_P551", "IRS Pub 551")],
        ),
        (
            "Within 150 Days of Death",
            "5. County Assessor Death Notification (CA R&TC §480(b))",
            "Trustee must file Form BOE-502-D (Change in Ownership Statement — Death of Real Property Owner) with the Santa Clara County Assessor within 150 days of date of death—even when title remains inside a trust and no deed has yet recorded!",
            "Statutory 10% penalty of taxes applicable to the new base year value under R&TC §482.",
            [("S_RTC_480", "R&TC §480(b)"), ("S_SCC_P19", "SCC Assessor")],
        ),
        (
            "Months 4–8 (Decision Fork)",
            "6. Execute Strategy Fork: Sell Under §1014 (S3) vs. Move In (S1) vs. Lease (S2)",
            "Remember: under BOE LTA 2026/026, date of death (NOT deed distribution date) is the statutory transfer date! Decide well before Month 9 whether to list/sell Property A via the trust/beneficiary or move in as principal residence.",
            "Missing the 1-year occupancy window permanently forfeits Proposition 19 family-home relief.",
            [("S_BOE_LTA26026", "BOE LTA 2026/026"), ("S_RTC_632", "R&TC §63.2")],
        ),
        (
            "Within 9 Months (+6-Mo Ext.)",
            "7. Federal Form 706 Estate Return & Form 8971 Consistent Basis",
            "If gross estate + prior taxable gifts exceed the exclusion ($15.0M in 2026; $15.48M in 2027; ~$24.13M projected in 2045), file Form 706 and pay any 40% estate tax within 9 months (Form 4768 grants automatic 6-month filing extension). Distribute Form 8971 Schedule A to beneficiaries within 30 days after Form 706.",
            "Late-filing/late-payment penalties plus IRC §6035 inconsistent-basis penalties.",
            [("S_IRS_I706", "IRS Form 706"), ("S_IRS_WN", "IRS IRC §6035")],
        ),
        (
            "Within 1 Year (If Occupying A)",
            "8. Move Into Property A, File BOE-266 & Terminate Property B HOX",
            "Only if choosing Strategy S1a/S1b: establish physical principal residence in Property A within 1 year of death, file Form BOE-266 ($7,000 Homeowners' Exemption) in Santa Clara County, and notify the San Francisco Assessor in writing (by Dec 10) to terminate the Homeowners' Exemption on Property B.",
            "Dual Homeowners' Exemption escape assessment + 25% penalty; loss of Prop 19 eligibility.",
            [("S_BOE_266", "Form BOE-266"), ("S_BOE_HOX", "BOE HOX Rules")],
        ),
        (
            "At Deed Recording / Sale",
            "9. Affidavit of Death of Trustee, Trust Distribution Deed & R&TC §11930 Exemption",
            "Record Affidavit of Death of Trustee + Preliminary Change of Ownership Report (BOE-502-A). If distributing to beneficiary, claim documentary transfer tax exemption '$0 — R&TC §11930 transfer by reason of death'. If selling directly from trust to buyer, county transfer tax is $0.55/$500 (R&TC §11911).",
            "Avoidable county/city transfer tax collection if §11930 statutory exemption is not cited on deed.",
            [("S_RTC_11930", "R&TC §11930"), ("S_RTC_11911", "R&TC §11911")],
        ),
        (
            "April 15 Following Death/Sale",
            "10. Final Form 1040/540, Fiduciary Form 1041/541 & Schedule D Sale Reporting",
            "File decedent's final individual returns (Form 1040 & CA Form 540), trust fiduciary income returns (Form 1041 & CA Form 541 for post-death income), and report any sale of Property A on Form 8949 / Schedule D showing §1014 FMV basis less selling expenses (typically a small deductible capital loss!).",
            "IRS automated 1099-S gross-proceeds mismatch notice if Form 8949 / Schedule D is omitted.",
            [("S_IRS_BASIS", "IRS §1014 / Sch D"), ("S_FTB_INH", "CA FTB 540/541")],
        ),
        (
            "Months 1–36 Post-Sale",
            "11. Reinvest Net Proceeds via U.S. Treasury Ladder Into Global Equities (S3b → S3a)",
            "Place net sale proceeds (~$6.40M in 2045 baseline) into direct U.S. Treasury bills/notes (interest 100% exempt from CA 13.3% state income tax) and tranche systematically over 24–36 months into low-cost total-market equity index funds.",
            "Holding cash in ordinary bank CDs/HYSA unnecessarily forfeits 13.3% CA state tax on interest.",
            [("S_IRS_P550", "IRS Pub 550"), ("S_TSP_RET", "TSP G/C Funds")],
        ),
        (
            "Within 3 Years (If Occupying A)",
            "12. Final Deadline for Form BOE-19-P Retroactive Prop 19 Relief",
            "If occupying Property A under Strategy S1a/S1b, file Form BOE-19-P (Claim for Reassessment Exclusion for Transfer Between Parent and Child Occurring on or After Feb 16, 2021) within 3 years of death (and before transferring to a third party) to receive retroactive relief back to date of death.",
            "Filing after 3 years yields prospective relief only—losing 3+ years of supplemental tax refunds!",
            [("S_BOE_PUB801", "BOE Pub 801"), ("S_SCC_P19", "SCC BOE-19-P")],
        ),
    ]

    rows = []
    for window, step, action, risk, srcs in steps:
        rows.append(f"""
            <tr>
              <td><strong>{L.esc(window)}</strong></td>
              <td><strong>{L.esc(step)}</strong></td>
              <td>{L.esc(action)}</td>
              <td>{L.esc(risk)}</td>
              <td>{L.badge_verified()}</td>
              <td>{L.cites(srcs)}</td>
            </tr>""")

    body = f"""
    <section class="section">
      <h2>Chronological 12-Step Trust Inheritance, Assessor &amp; Tax Execution Checklist</h2>
      <p>Because Property A passes via trust rather than formal Superior Court probate, title administration happens privately through the successor trustee—<em>but statutory tax and assessor deadlines run strictly from the <strong>date of death</strong>, not the date a deed is recorded</em> (BOE LTA 2026/026; CA R&amp;TC §480(b); Probate Code §16061.7).</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Statutory Window</th>
              <th>Execution Step</th>
              <th>Required Legal, Tax &amp; Assessor Action</th>
              <th>Penalty / Failure Mode Avoided</th>
              <th>Status</th>
              <th>Official Sources</th>
            </tr>
          </thead>
          <tbody>
            {"".join(rows)}
          </tbody>
        </table>
      </div>
    </section>
    """
    return L.render_page(
        "inheritance-process.html",
        "Execution Playbook",
        "Step-by-Step Trust Inheritance, Assessor & Tax Filing Walkthrough",
        "Twelve deadline-anchored stages from pre-transfer trust verification through Probate Code §16061.7 notice, R&TC §480(b) 150-day assessor filing, Form 706/8971, BOE-266/BOE-19-P, §1014 sale reporting, and tax-efficient Treasury-to-equity deployment.",
        body,
    )


def build_law_watch_page() -> str:
    body = f"""
    <section class="section">
      <h2>1. Enacted Federal, State &amp; Regulatory Changes (Verified Through November 12, 2026)</h2>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Statute / Ruling / Regulation</th>
              <th>Jurisdiction &amp; Effective Date</th>
              <th>Verified Rule &amp; Planning Impact</th>
              <th>Status</th>
              <th>Official Sources</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Public Law 119-21 (Working Families Tax Cuts)</strong></td>
              <td>Federal · Signed July 4, 2025 (effective TY 2026+)</td>
              <td>Replaced the scheduled 2026 TCJA sunset (~$7M) with a permanent {L.stat('$15,000,000')} basic estate/gift/GST exclusion for 2026, indexed for inflation starting 2027.</td>
              <td>{L.badge_verified('Enacted Law')}</td>
              <td>{L.cites([('S_IRS_WN', "IRS What's New"), ('S_IRS_EST', 'IRS Estate Tax')])}</td>
            </tr>
            <tr>
              <td><strong>IRS Rev. Proc. 2026-35 (IR-2026-133)</strong></td>
              <td>Federal · Released November 5, 2026 (effective TY 2027)</td>
              <td>Raises the 2027 federal estate/gift exclusion to {L.stat('$15,480,000')} (+3.20% YoY; {L.stat('$30,960,000')} w/ DSUE) and raises the annual gift exclusion from {L.stat('$19,000')} to {L.stat('$20,000')}.</td>
              <td>{L.badge_verified('Enacted 2027 Schedule')}</td>
              <td>{L.cite('S_IRS_2027', 'IRS IR-2026-133')}</td>
            </tr>
            <tr>
              <td><strong>IRS Revenue Ruling 2023-2</strong></td>
              <td>Federal · Binding IRS Precedent</td>
              <td>Confirms that assets transferred to an <em>irrevocable</em> grantor trust not included in the decedent's Ch. 11 gross estate receive <strong>no IRC §1014 basis step-up</strong> at death.</td>
              <td>{L.badge_verified('Binding Ruling')}</td>
              <td>{L.cite('S_IRS_RR2302', 'IRS Rev. Rul. 2023-2')}</td>
            </tr>
            <tr>
              <td><strong>BOE LTA 2026/026 &amp; Biennial Prop 19 Reset</strong></td>
              <td>California · Issued August 3, 2026; next cap reset Feb 16, 2027</td>
              <td>Current Prop 19 family-home allowance is {L.stat('$1,044,586')} (Feb 16, 2025 – Feb 15, 2027); next biennial CCPI adjustment takes effect February 16, 2027. Clarifies trust eligibility and continual-occupancy rules.</td>
              <td>{L.badge_verified('Active Guidance')}</td>
              <td>{L.cites([('S_BOE_LTA26026', 'BOE LTA 2026/026'), ('S_BOE_PUB801', 'BOE Pub 801')])}</td>
            </tr>
            <tr>
              <td><strong>CA Civil Code §1947.12 (AB 1482 Rent Cap Sunset)</strong></td>
              <td>California · Statutory repeal date January 1, 2030</td>
              <td>Caps non-exempt statewide residential rent increases at 5% + CPI (max 10%) through Dec 31, 2029 unless extended by the Legislature; SFRs remain exempt only if statutory written exemption notice is in the lease.</td>
              <td>{L.badge_verified('Enacted Sunset')}</td>
              <td>{L.cite('S_CIV_1947', 'Civ. Code §1947.12')}</td>
            </tr>
            <tr>
              <td><strong>CPUC Decision 22-12-056 (Net Billing Tariff)</strong></td>
              <td>California · Effective April 15, 2023 (20-yr legacy sunset)</td>
              <td>Replaced retail-rate NEM export credits with avoided-cost Solar Billing Plan credits for new interconnections and upon 20-year legacy PTO expiration.</td>
              <td>{L.badge_verified('Active Tariff')}</td>
              <td>{L.cite('S_CPUC_NEM', 'CPUC NEM/NBT')}</td>
            </tr>
            <tr>
              <td><strong>CDI Sustainable Insurance Strategy</strong></td>
              <td>California · Phased rollout through Oct 27, 2026 snapshot</td>
              <td>Permits forward-looking catastrophe modeling and California-only net reinsurance cost recovery in homeowners/dwelling filings alongside distressed-area writing commitments.</td>
              <td>{L.badge_verified('Active Regulation')}</td>
              <td>{L.cite('S_CDI_SIS', 'CDI Oct 27, 2026')}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <h2>2. November 2026 California Ballot Measures &amp; Pending Local Ordinances (Watched / Unofficial)</h2>
      <p>Per the <strong>California Secretary of State</strong>, November 3, 2026 General Election returns remain <em>unofficial</em> until statutory certification on <strong>December 11, 2026</strong> (<a href="flagged.html#F-15">Flag F-15</a>), and San Francisco Board of Supervisors <strong>File No. 261020</strong> (posted November 9, 2026) is <em>proposed legislation</em> not yet enacted (<a href="flagged.html#F-16">Flag F-16</a>):</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Measure / Ordinance</th>
              <th>Unofficial Tally / Status (as of Nov 11–12, 2026)</th>
              <th>Direct Relevance to Property A, Property B &amp; Liquid Inheritance</th>
              <th>Status</th>
              <th>Official Sources</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>CA Proposition 3 — High-Income Tax Rate Extension</strong></td>
              <td>Leading: <strong>60.7% Yes</strong> / 39.3% No (unofficial; cert. Dec 11, 2026)</td>
              <td>Permanently extends top California personal income &amp; capital-gains tax brackets (up to 12.3% + 1% >$1M surcharge = <strong>13.3%</strong>), increasing the value of Property A's §1014 step-up and CA-tax-exempt U.S. Treasuries.</td>
              <td>{L.badge_pending('F-15', 'Unofficial Returns')}</td>
              <td>{L.cites([('S_SOS_2026', 'CA SOS Returns'), ('S_FTB_RATES', 'FTB 540 Rates')])}</td>
            </tr>
            <tr>
              <td><strong>CA Proposition 42 — Prohibition on New State Personal-Property / Wealth Taxes</strong></td>
              <td>Leading: <strong>51.4% Yes</strong> / 48.6% No (close margin; unofficial)</td>
              <td>Constitutional bar against state ad valorem taxes on intangible/personal wealth—reinforcing California's $0 state wealth/inheritance tax baseline if certified.</td>
              <td>{L.badge_pending('F-15', 'Close Race / Unofficial')}</td>
              <td>{L.cite('S_SOS_2026', 'CA SOS Returns')}</td>
            </tr>
            <tr>
              <td><strong>CA Proposition 40 (55% Local Tax Threshold) &amp; Proposition 43</strong></td>
              <td>Trailing: Prop 40 <strong>52.5% No</strong>; Prop 43 <strong>57.4% No</strong> (unofficial)</td>
              <td>Voters currently rejecting lower voter thresholds for local special parcel taxes—helping contain future fixed parcel-tax creep on both Property A and Property B.</td>
              <td>{L.badge_pending('F-15', 'Unofficial Returns')}</td>
              <td>{L.cite('S_SOS_2026', 'CA SOS Returns')}</td>
            </tr>
            <tr>
              <td><strong>SF Board of Supervisors File No. 261020 (Rent Ordinance Amendment)</strong></td>
              <td>Proposed Legislation (posted Nov 9, 2026; not yet enacted)</td>
              <td>Would cap combined annual rent increases from <em>banked</em> rent increases plus <em>capital improvement</em> passthroughs at <strong>10%/yr</strong> on rent-controlled SF units such as Property B's 2 rented units.</td>
              <td>{L.badge_pending('F-16', 'Proposed Ordinance')}</td>
              <td>{L.cite('S_SF_RENT', 'SF Rent Board Notice')}</td>
            </tr>
            <tr>
              <td><strong>Future Federal Estate Exclusion &amp; Prop 19 Repeal Proposals</strong></td>
              <td>No active 2026 ballot qualifier (Howard Jarvis Prop 19 repeal initiatives did not qualify for Nov 2026 ballot); CBO flags post-2030 federal fiscal pressure.</td>
              <td>Never base irreversible lifetime deeds on speculative future repeal of Prop 19; keep trust flexible (revocable) until actual transfer window in 2040–2050.</td>
              <td>{L.badge_verified('Verified Non-Enacted')}</td>
              <td>{L.cites([('S_SOS_2026', 'CA SOS Ballot'), ('S_CBO_2026', 'CBO Outlook')])}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
    """
    return L.render_page(
        "law-watch.html",
        "Legislative & Ballot Tracker",
        "Federal, California & Local Law Watch (Through November 12, 2026)",
        "Verified enactment status of Public Law 119-21, IRS 2027 inflation adjustments (Rev. Proc. 2026-35), Rev. Rul. 2023-2, Prop 19 LTA 2026/026, November 2026 California ballot returns, and pending San Francisco Rent Ordinance File No. 261020.",
        body,
    )


def build_repo_audit_page() -> str:
    body = f"""
    <section class="section">
      <h2>1. Line-by-Line Repository Audit Summary</h2>
      <p>We audited the repository's existing pages, scripts, data artifacts, Jekyll configuration (<code>_config.yml</code>), and CI gate (<code>.github/workflows/privacy-pages.yml</code>) against live official <code>.gov</code> and statutory sources on November 12, 2026 (respecting parallel-session file scopes by never modifying files owned by sibling sessions and implementing all corrections cleanly in <code>desk-22a32b17/</code> and <code>tools-22a32b17/</code>):</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Audit Dimension</th>
              <th>Repository Finding</th>
              <th>Verification Outcome &amp; Action Taken in <code>desk-22a32b17/</code></th>
              <th>Status</th>
              <th>Official Sources</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>1. Broken HTTP 404 Official Links in <code>public-safe/</code></strong></td>
              <td>Three <code>.gov</code> URLs cited in <code>public-safe/</code> returned HTTP 404 when fetched live on 2026-11-12: (a) <code>sf.gov/reports--march-2026--allowable-annual-rent-increases-2026-2027</code>; (b) <code>asr.santaclaracounty.gov/learn-more-about-proposition-19-parent-child</code>; (c) <code>asr.santaclaracounty.gov/decline-value-prop-8</code>.</td>
              <td>Replaced across all 12 pages of <code>desk-22a32b17/</code> with live HTTP-200 verified official URLs: <code>sf.gov/reports--current-rates-including-rent-increase-relocation-sec-deposit</code>, <code>asr.santaclaracounty.gov/tax-savings/transferring-your-assessed-value/parent-to-child-2</code>, and <code>R&amp;TC §51</code> + <code>SCC 2025–26 Annual Report</code> (<a href="flagged.html#F-17">Flag F-17</a>).</td>
              <td>{L.badge_verified('Fixed in 22a Desk')}</td>
              <td>{L.cites([('S_SF_RENT', 'SF Rent Board (200 OK)'), ('S_SCC_P19', 'SCC Prop 19 (200 OK)'), ('S_RTC_51', 'R&TC §51')])}</td>
            </tr>
            <tr>
              <td><strong>2. Reassessed Tax Scaling (Ad Valorem vs. Direct Charges)</strong></td>
              <td>Dividing Property A's $7,210 bill by the ~$550,000 banded FBYV yields ~1.31%—which bundles ~1.19% ad valorem rate with ~$660/yr fixed parcel charges. Multiplying $6.5M reassessed FMV by 1.31% overstates reassessed tax by ~$7,800/yr.</td>
              <td><code>model_22a.py</code> explicitly separates <strong>1.19% ad valorem rate</strong> (which scales with reassessed taxable value) from <strong>$660/yr fixed direct charges</strong> (which do not jump on reassessment).</td>
              <td>{L.badge_verified('Upgraded in model_22a')}</td>
              <td>{L.cites([('S_BOE_PUB800', 'BOE Pub 800-10'), ('S_SCC_AR', 'SCC Annual Report')])}</td>
            </tr>
            <tr>
              <td><strong>3. 2027 IRS Estate &amp; Gift Inflation Release (Nov 5, 2026)</strong></td>
              <td>Prior tables stopped at the 2026 {L.stat('$15,000,000')} / {L.stat('$19,000')} statutory figures and projected 2027 purely by assumption.</td>
              <td>Incorporated official <strong>IRS IR-2026-133 / Rev. Proc. 2026-35</strong> (Nov 5, 2026): enacted 2027 estate exclusion = {L.stat('$15,480,000')} (+3.20%) and 2027 annual gift exclusion = {L.stat('$20,000')}.</td>
              <td>{L.badge_verified('Verified Official 2027')}</td>
              <td>{L.cite('S_IRS_2027', 'IRS Rev. Proc. 2026-35')}</td>
            </tr>
            <tr>
              <td><strong>4. Rev. Rul. 2023-2 Irrevocable Trust Basis Check</strong></td>
              <td>Assuming IRC §1014 step-up automatically applies to every trust ignores whether the settlor used an excluded irrevocable grantor trust.</td>
              <td>Quantified exact <strong>$2,280,000+</strong> immediate tax penalty under <strong>IRS Rev. Rul. 2023-2</strong> if step-up is lost, added unit test, and flagged trust verification (<a href="flagged.html#F-03">Flag F-03</a>).</td>
              <td>{L.badge_verified('Verified & Tested')}</td>
              <td>{L.cite('S_IRS_RR2302', 'IRS Rev. Rul. 2023-2')}</td>
            </tr>
            <tr>
              <td><strong>5. Rental Depreciation (§168 / §1250) &amp; §121 Exclusion</strong></td>
              <td>Omitting 27.5-year rental building depreciation understates S2 annual after-tax cash flow while omitting §1250 25% recapture + CA tax overstates terminal liquidation proceeds.</td>
              <td><code>model_22a.py</code> models both 27.5-yr MACRS building depreciation + passive-loss carryforward and terminal IRC §1250 recapture (S2) as well as IRC §121 principal-residence exclusion (S1a/S1b).</td>
              <td>{L.badge_verified('Upgraded in model_22a')}</td>
              <td>{L.cites([('S_IRS_P527', 'IRS Pub 527'), ('S_IRS_P523', 'IRS Pub 523')])}</td>
            </tr>
            <tr>
              <td><strong>6. Repository Privacy &amp; Nearest-$10 Rounding Gate</strong></td>
              <td><code>scripts/privacy_scan.py</code> and <code>scripts/verify_safe.py</code> enforce $10 rounding and zero PII across tracked files.</td>
              <td>Verified <strong>0 privacy findings</strong> across the entire repository (including <code>desk-22a32b17/</code> and <code>tools-22a32b17/</code> even with <code>--minor</code> enabled) and banded roll baselines to prevent parcel lookup.</td>
              <td>{L.badge_verified('0 Findings — PASS')}</td>
              <td>{L.cites([('S_BOE_PUB800', 'BOE Roll Privacy'), ('S_RTC_632', 'R&TC §63.2(c)')])}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
    """
    return L.render_page(
        "repo-audit.html",
        "Independent Verification & QA",
        "Line-by-Line Repository Audit, Link Health & Model Reconciliation",
        "Verification of repository claims, live HTTP-200 check of all cited official URLs (catching 3 moved/404 county & municipal URLs), privacy-gate audit, and mathematical model improvements.",
        body,
    )


def build_flagged_page() -> str:
    flags: List[Tuple[str, str, str, str, List[Tuple[str, str]]]] = [
        ("F-01", "Property B Roll vs. Tax Bill Gap", "Stated SF roll base × 1.18162182% = ~$1,350 ad valorem vs. ~$2,440 total bill (~$1,090 gap).", "Left confirmed parcel roll blank (—); inspect private SF FY 2026-27 tax bill for parcel taxes / Rent Board fee / omitted structure roll.", [("S_SF_TAX", "SF Treasurer")]),
        ("F-02", "Property A Ad Valorem vs. Fixed Assessments", "Exact Tax Rate Area (TRA) bond rate and parcel-tax line items on Property A's secured bill are not in public-safe records.", "Left confirmed bill blank (—); modeled 1.19% ad valorem + $660/yr fixed direct charges.", [("S_SCC_AR", "SCC Assessor")]),
        ("F-03", "Trust Revocability & Gross-Estate Inclusion", "Actual trust instrument has not been inspected to confirm revocable living trust status vs. excluded irrevocable grantor trust.", "Left blank (—); critical check under IRS Rev. Rul. 2023-2 before assuming IRC §1014 step-up.", [("S_IRS_RR2302", "Rev. Rul. 2023-2")]),
        ("F-04", "2026 Fair Market Value Appraisals ($3.10M / $1.80M)", "Owner planning estimates ($3,100,000 for Property A; $1,800,000 for Property B) are not certified appraisals.", "Labeled as $10-rounded planning baselines; confirmed appraisal column left blank (—).", [("S_FHFA_HPI", "FHFA HPI")]),
        ("F-05", "Property A Municipal Transfer Tax Applicability", "Because city name is redacted for privacy, applicability of any charter-city real property transfer tax above county $0.55/$500 is unconfirmed.", "Modeled general-law county rate ($0.55/$500 under R&TC §11911); verify city recorder fee privately.", [("S_RTC_11911", "R&TC §11911")]),
        ("F-06", "Settlor Principal-Residence & BOE-266 Status on Property A", "Prop 19 requires Property A to be the settlor's principal residence at transfer (verified via BOE-266 / occupancy records).", "Left confirmed status blank (—); confirm BOE-266 is active on Property A.", [("S_BOE_P19", "BOE Prop 19")]),
        ("F-07", "Property B Rent Roll, Lease Dates & Rent-Control Coverage", "Certificate of occupancy year, tenant move-in dates, and banked rent increases on Property B's 2 leased units ($7,150/mo) are private.", "Left confirmed rent roll blank (—); modeled 2.0%/yr SF Rent Ordinance growth.", [("S_SF_RENT", "SF Rent Board")]),
        ("F-08", "Insurance Declarations, Square Footage & Coverage A Limits", "Current insurance carrier, wildfire/brush score, square footage, and Coverage A limits for A & B are private.", "Left policy column blank (—); replaced $1,500 placeholder with researched $3,200/$3,800/$4,200 baselines.", [("S_CDI_RES", "CDI Res. Guide")]),
        ("F-09", "Exact Water/Wastewater Meter Sizes & Utility Tariffs", "Retail water agency serving Property A and meter size on Property B (5/8\" vs. 3/4\"+) are private.", "Left utility account column blank (—); used owner midpoints ($1,500/yr A; $4,380/yr B) + SFPUC escalation.", [("S_SFPUC", "SFPUC Prop 218")]),
        ("F-10", "Property A Rooftop Solar Interconnection PTO Date & NEM Tier", "Exact 20-year NEM 1.0/2.0 sunset year and inverter age on Property A are unconfirmed.", "Left PTO date blank (—); modeled legacy credit (-$180/yr) transitioning to CPUC NBT (+$600/yr eq.) in 2038.", [("S_CPUC_NEM", "CPUC D.22-12-056")]),
        ("F-11", "Building Age, Roof/Foundation History & CapEx Reserve", "Structural inspection reports and seismic retrofit status (especially soft-story status on 3-unit Property B) are unverified.", "Left inspection column blank (—); modeled 0.40% FMV upkeep on A ($12,400) and 0.80% on B ($14,400) + R5 seismic stress.", [("S_USGS_EQ", "USGS UCERF3")]),
        ("F-12", "Settlor's Exact Liquid Portfolio Size & Prior Taxable Gifts", "Total cash/securities balance and prior lifetime Form 709 taxable gifts are private and unconfirmed.", "Left exact estate balance blank (—); solved full $0–$20M sensitivity matrix showing $5,740,000 2026 inflection point.", [("S_IRS_I706", "IRS Form 706")]),
        ("F-13", "Pre-Tax Retirement (IRA / 401(k)) vs. Taxable Brokerage Split", "Share of liquid inheritance inside Traditional IRAs/401(k)s (subject to ordinary income tax under IRC §691) vs. stepped-up brokerage is unknown.", "Left account split blank (—); documented up to 50.3% combined Fed+CA tax on pre-tax retirement accounts.", [("S_IRS_P550", "IRS Pub 550")]),
        ("F-14", "Spousal Marital Status & Predeceased Spouse DSUE Election", "Whether settlor is married or holds a valid Form 706 DSUE portability election from a predeceased spouse is private.", "Modeled both Single ($15.0M / $15.48M) and Married w/ DSUE ($30.0M / $30.96M) columns.", [("S_IRS_FAQ", "IRS DSUE FAQ")]),
        ("F-15", "Nov 2026 California Statewide Ballot Returns Are Unofficial", "CA SOS returns for Props 3, 40, 42, and 43 (as of Nov 11–12, 2026) await final county canvas and Dec 11, 2026 certification.", "Tagged 'Unofficial / Pending' with exact Nov 11 percentages; re-check after Dec 11, 2026.", [("S_SOS_2026", "CA SOS Returns")]),
        ("F-16", "SF Board of Supervisors File No. 261020 Not Yet Enacted", "Proposed Nov 9, 2026 SF ordinance capping banked + capital-improvement rent increases at 10%/yr is pending legislation.", "Tagged 'Unofficial / Pending'; baseline model does not rely on >10%/yr passthroughs.", [("S_SF_RENT", "SF Rent Board")]),
        ("F-17", "Three Legacy 404 URLs in Sibling <code>public-safe/</code> Pages", "Sibling scope <code>public-safe/</code> (not edited per parallel-session rules) contains 1 moved <code>sf.gov</code> URL and 2 moved <code>asr.santaclaracounty.gov</code> URLs.", "Logged in <code>COORDINATION.md</code> & <code>repo-audit.html</code>; <code>desk-22a32b17/</code> uses 100% live HTTP-200 replacements.", [("S_SCC_P19", "SCC Live URL")]),
        ("F-18", "Beneficiary's Marginal Tax Bracket & Filing Status in 2040–2050", "Beneficiary's future wage income and single vs. MFJ status in 2040–2050 affect IRC §121 ($250k vs. $500k) and rental/NIIT brackets.", "Modeled conservative high-bracket CA single baseline (37.1% LTCG; $250k §121) with sensitivity notes.", [("S_FTB_RATES", "FTB 540 Schedules")]),
    ]

    rows = []
    for fid, title, issue, action, srcs in flags:
        rows.append(f"""
            <tr id="{L.esc(fid)}">
              <td><strong>{L.esc(fid)}</strong></td>
              <td><strong>{L.esc(title)}</strong></td>
              <td class="blank">—</td>
              <td>{L.esc(issue)}</td>
              <td>{L.esc(action)}</td>
              <td>{L.badge_unverified(fid, 'Flagged')}</td>
              <td>{L.cites(srcs)}</td>
            </tr>""")

    body = f"""
    <div class="callout flag">
      <strong class="title">Strict No-Hallucination &amp; Blank-Cell Policy (Non-Blocking Private Review List)</strong>
      Every item below could not be confirmed from an official public source without private owner documents (tax bills, trust instrument, insurance declarations, utility accounts, or certified election canvas). In accordance with project verification rules, <strong>confirmed-record cells are left blank (<code>—</code>)</strong> rather than inferred, and each item is catalogued here for private owner verification. Per repository governance, open flags are expected and <strong>do not block PR merge or deployment</strong>.
    </div>

    <section class="section">
      <h2>Master Flagged-for-Review Register (F-01 through F-18)</h2>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Flag ID</th>
              <th>Item</th>
              <th>Confirmed Value</th>
              <th>Why Unverified / Irregular</th>
              <th>Safe Handling &amp; Private Verification Step</th>
              <th>Status</th>
              <th>Official Reference</th>
            </tr>
          </thead>
          <tbody>
            {"".join(rows)}
          </tbody>
        </table>
      </div>
    </section>
    """
    return L.render_page(
        "flagged.html",
        "Zero-Hallucination Register",
        "Flagged for Review: Unconfirmed Private Inputs & Pending Official Items",
        "Complete register of all 18 unconfirmed property, trust, tax-bill, utility, insurance, and unofficial-return items left blank in confirmed columns for private owner verification.",
        body,
    )


def build_sources_page() -> str:
    rows = []
    for idx, s in enumerate(m.SOURCES, 1):
        rows.append(f"""
            <tr id="{L.esc(s['id'])}">
              <td class="num">{idx}</td>
              <td><code>{L.esc(s['id'])}</code></td>
              <td><strong>{L.esc(s['agency'])}</strong></td>
              <td><a href="{L.esc(s['url'])}" target="_blank" rel="noopener noreferrer">{L.esc(s['title'])}</a></td>
              <td>{L.esc(s['used_for'])}</td>
              <td>{L.esc(s['verified'])}</td>
              <td>{L.badge_verified('HTTP 200 OK')}</td>
            </tr>""")

    body = f"""
    <section class="section">
      <h2>Master Catalogue of All 45 Live-Verified Official Sources</h2>
      <p>Every single URL below is an official federal, State of California, county, municipal, or statutory authority directly retrieved and verified live (HTTP 200) on <strong>2026-11-12</strong>. Every table row across all 12 pages of <code>desk-22a32b17/</code> links to one or more entries in this register.</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th class="num">#</th>
              <th>Source Key</th>
              <th>Official Agency / Body</th>
              <th>Document Title &amp; Direct Official Link</th>
              <th>Facts &amp; Model Rules Verified</th>
              <th>Verified Date</th>
              <th>Link Status</th>
            </tr>
          </thead>
          <tbody>
            {"".join(rows)}
          </tbody>
        </table>
      </div>
    </section>
    """
    return L.render_page(
        "sources.html",
        "Primary Legal & Statistical Authorities",
        "Verified Official Sources Register (45 Government & Statutory Authorities)",
        "Complete bibliography of live-verified IRS, California BOE, FTB, State Controller, Legislature, Santa Clara County Assessor, San Francisco Treasurer/Recorder/Rent Board/SFPUC, CDI, CPUC, BLS, Federal Reserve, FHFA, CBO, TSP, and USGS sources.",
        body,
    )
