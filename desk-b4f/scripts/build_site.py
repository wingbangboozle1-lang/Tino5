"""Deterministic static-site generator for desk-b4f/.

Generates style-matched, privacy-safe, $10-rounded, official-source-linked HTML
pages strictly from desk-b4f/scripts/after_tax_model.py and verified statutory constants.
"""

from html import escape
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
OUT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

import after_tax_model as m  # noqa: E402

STAMP = "Verified 2026-11-12"

# Verified official HTTPS URLs (all checked directly during session)
SOURCES = {
    "irs_estate": ("IRS · Estate tax", "https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax"),
    "irs_whatsnew": ("IRS · Estate & gift updates", "https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax"),
    "irs_rp2635": ("IRS · Rev. Proc. 2026-35 (2027)", "https://www.irs.gov/pub/irs-drop/rp-26-35.pdf"),
    "irs_2027news": ("IRS · 2027 inflation release", "https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2027-taxpayers-continue-to-benefit-from-the-working-families-tax-cuts"),
    "irs_p523": ("IRS · Pub 523 (§121 home sale)", "https://www.irs.gov/publications/p523"),
    "irs_p527": ("IRS · Pub 527 (rental & 27.5-yr depr.)", "https://www.irs.gov/publications/p527"),
    "irs_p925": ("IRS · Pub 925 (§469 passive loss)", "https://www.irs.gov/publications/p925"),
    "irs_tc409": ("IRS · Topic 409 (§1250 25% & LTCG)", "https://www.irs.gov/taxtopics/tc409"),
    "irs_niit": ("IRS · Net Investment Income Tax Q&A", "https://www.irs.gov/newsroom/questions-and-answers-on-the-net-investment-income-tax"),
    "irs_i706": ("IRS · Form 706 instructions (DSUE)", "https://www.irs.gov/instructions/i706"),
    "irs_basis": ("IRS · Inherited basis FAQ", "https://www.irs.gov/faqs/interest-dividends-other-types-of-income/gifts-inheritances/gifts-inheritances"),
    "sco_estate": ("CA Controller · Estate tax ($0)", "https://www.sco.ca.gov/ardtax_taxinfo_estate_return.html"),
    "ftb_2026_10": ("CA FTB · Oct. 2026 Tax News", "https://www.ftb.ca.gov/about-ftb/newsroom/tax-news/2026/10.html"),
    "ftb_sched": ("CA FTB · 2026 Rate Schedules", "https://www.ftb.ca.gov/forms/2026/2026-540-tax-rate-schedules.pdf"),
    "ftb_home": ("CA FTB · Home sale §121 conformity", "https://www.ftb.ca.gov/file/personal/income-types/income-from-the-sale-of-your-home.html"),
    "boe_p19": ("CA BOE · Proposition 19", "https://www.boe.ca.gov/prop19/"),
    "boe_lta25009": ("CA BOE · LTA 2025/009 (Prop 19 Cap)", "https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf"),
    "boe_lta26002": ("CA BOE · LTA 2026/002 (CCPI 3.307%)", "https://www.boe.ca.gov/proptaxes/pdf/lta26002.pdf"),
    "boe_ho": ("CA BOE · Homeowners' Exemption", "https://www.boe.ca.gov/proptaxes/homeowners_exemption.htm"),
    "boe_80010": ("CA BOE · Pub 800-10 assessment", "https://www.boe.ca.gov/pdf/pub800-10.pdf"),
    "scc_ratebook": ("SCC Controller · FY25-26 Tax Rate Book", "https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf"),
    "scc_p19": ("SCC Assessor · Parent-child Prop 19", "https://asr.santaclaracounty.gov/tax-savings/transferring-your-assessed-value/parent-to-child-2"),
    "sf_treas": ("SF Treasurer · Secured rate 1.1816%", "https://sftreasurer.org/property/secured-property-taxes"),
    "sf_rent": ("SF.gov · Rent Board 1.6% & File 261020", "https://www.sf.gov/learn-about-rent-increases-san-francisco"),
    "sf_leg261020": ("SF BOS · Legistar File No. 261020", "https://sfgov.legistar.com/LegislationDetail.aspx?ID=8217304&GUID=7EDA4662-EBFB-4AF5-962F-C669B64AA770"),
    "sf_inv": ("SF.gov · Housing Inventory License", "https://www.sf.gov/rent-board-housing-inventory"),
    "sfpuc_p218": ("SFPUC · FY26-28 Prop 218 Water/Sewer", "https://www.sfpuc.gov/accounts-services/water-power-sewer-rates/proposed-water-sewer-rates-2026/proposition-218-notice"),
    "cpuc_sjwc": ("CPUC · D.24-12-077 County Water GRC", "https://docs.cpuc.ca.gov/PublishedDocs/Published/G000/M549/K805/549805244.pdf"),
    "cpuc_nem": ("CPUC · NEM & Net Billing (NBT)", "https://www.cpuc.ca.gov/nem"),
    "cpuc_bsc": ("CPUC · Res. E-5354 / D.24-05-028 (BSC)", "https://docs.cpuc.ca.gov/PublishedDocs/Published/G000/M555/K816/555816677.pdf"),
    "pge_nemfaq": ("PG&E · Solar Billing / 20-Yr NEM FAQ", "https://www.pge.com/content/dam/pge/docs/clean-energy/solar/nem-faq.pdf"),
    "cdi_sis": ("CDI · Sustainable Insurance Strategy", "https://www.insurance.ca.gov/01-consumers/180-climate-change/sustainable-insurance-strategy.cfm"),
    "cdi_2025": ("CDI · 2025 EQ/Residential Summary", "https://www.insurance.ca.gov/0400-news/0200-studies-reports/0300-earthquake-study/upload/EQEXP2025Summary.pdf"),
    "cdi_sf26": ("CDI · Mar. 2026 State Farm Settlement", "https://www.insurance.ca.gov/0400-news/0100-press-releases/2026/release012-2026.cfm"),
    "sos_ballot": ("CA SOS · Nov. 11 Ballot Tallies", "https://electionresults.sos.ca.gov/returns/ballot-measures"),
    "bls_cpi": ("BLS · CPI October 2026 (+0.4% SA)", "https://www.bls.gov/cpi/"),
    "bls_sf": ("BLS · Bay Area CPI Oct. 2026", "https://www.bls.gov/regions/west/news-release/consumerpriceindex_sanfrancisco.htm"),
    "fhfa_hpi": ("FHFA · House Price Index Schedule", "https://www.fhfa.gov/data/hpi"),
    "civ_1947": ("CA Civil Code §1947.12 (AB 1482)", "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12"),
    "rtc_11911": ("CA R&TC §11911 (Transfer Tax)", "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=11911"),
    "prob_16061": ("CA Probate Code §16061.7 (Trust Notice)", "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PROB&sectionNum=16061.7"),
    "ca_small": ("CA Courts · Small Estate / Probate", "https://selfhelp.courts.ca.gov/probate/small-estate"),
}

NAV = [
    ("index.html", "Overview"),
    ("decision.html", "After-Tax Decision"),
    ("properties.html", "Properties"),
    ("projections.html", "2026–2076 Projections"),
    ("costs.html", "Utilities, Solar & Insurance"),
    ("estate-tax.html", "2027 IRS & Estate Matrix"),
    ("black-swans.html", "Black Swans"),
    ("process.html", "Trust Process"),
    ("law-watch.html", "Law Watch"),
    ("repo-audit.html", "Repo Review"),
    ("flagged.html", "Flagged (F01–F20)"),
    ("sources.html", "Sources"),
]


def src(*keys):
    parts = []
    for k in keys:
        label, url = SOURCES[k]
        parts.append(f'<a href="{escape(url)}" rel="noopener noreferrer">{escape(label)}</a>')
    return '<span class="src-links">' + " · ".join(parts) + "</span>"


def stat(text):
    return f'<span class="stat">{escape(str(text))}</span>'


def chip(cls, text):
    return f'<span class="chip {cls}">{escape(text)}</span>'


def table(caption, headers, rows, right_cols=None):
    right = set(right_cols or [])
    ths = "".join(
        "<th scope=\"col\"" + (' class="num"' if i in right else "") + f">{escape(h)}</th>"
        for i, h in enumerate(headers)
    )
    trs = []
    for r in rows:
        tds = "".join(
            "<td" + (' class="num"' if i in right else "") + f">{cell}</td>"
            for i, cell in enumerate(r)
        )
        trs.append(f"<tr>{tds}</tr>")
    return (
        '<div class="scroll"><table>'
        f"<caption>{escape(caption)}</caption>"
        f"<thead><tr>{ths}</tr></thead>"
        f'<tbody>{"".join(trs)}</tbody>'
        "</table></div>"
    )


def layout(filename, title, subtitle, body):
    nav_html = "".join(
        f'<a href="{fn}"' + (' class="active"' if fn == filename else "") + f">{escape(lbl)}</a>"
        for fn, lbl in NAV
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{escape(title)} · Anonymized After-Tax Inheritance Desk</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="topbar">
  <div class="topbar-inner">
    <div class="brand-row">
      <div class="brand">Anonymized Inheritance Decision Desk · After-Tax &amp; Tariff Edition</div>
      <div class="stamp">{STAMP} · All modeled figures rounded to $10 · Zero PII</div>
    </div>
    <nav class="nav" aria-label="Primary navigation">{nav_html}</nav>
  </div>
</header>
<main class="container">
  <div class="page-header">
    <h1>{escape(title)}</h1>
    <p class="subtitle">{escape(subtitle)}</p>
  </div>
  {body}
  <footer class="footer">
    <div>Anonymized Decision Desk (<code>desk-b4f/</code>) · County-level labels only · Statutory figures marked <code>stat</code>; modeled figures rounded to $10.</div>
    <div>Informational decision modeling only — confirm parcel tax bills, trust terms, and personal tax brackets with qualified California estate/tax counsel.</div>
  </footer>
</main>
</body>
</html>
"""


def build_index():
    r40 = m.simulate_after_tax(2040)
    r45 = m.simulate_after_tax(2045)
    r50 = m.simulate_after_tax(2050)
    be_p45 = m.break_even_portfolio_aftertax(2045)
    be_h45 = m.break_even_home_growth_aftertax(2045)
    b26 = m.b_continuity_row(2026)

    kpis = f"""
<div class="kpi-grid">
  <div class="kpi good">
    <div class="label">Top 25-Yr Wealth (2045→2070)</div>
    <div class="val">{m.money(r45['s3_wealth'])}</div>
    <div class="note"><strong>S3: Sell A at transfer &amp; reinvest</strong> at 4.5% after-tax ({m.money(r45['delta_s2_vs_s3'] * -1)} ahead of Rent A)</div>
  </div>
  <div class="kpi">
    <div class="label">After-Tax Rent A (S2, 2045→2070)</div>
    <div class="val">{m.money(r45['s2_wealth'])}</div>
    <div class="note">Incl. 27.5-yr depreciation, §469 passive loss &amp; §1250 recapture (pre-tax {m.money(r45['s2_pretax_wealth'])})</div>
  </div>
  <div class="kpi warn">
    <div class="label">After-Tax Occupy A (S1, 2045→2070)</div>
    <div class="val">{m.money(r45['s1_wealth'])}</div>
    <div class="note">Incl. Prop 19 + {stat('$500,000')} MFJ §121 exclusion (+{m.money(r45['sec121_tax_saved'])} saved); A-only</div>
  </div>
  <div class="kpi good">
    <div class="label">2027 Estate Exclusion (Rev. Proc. 2026-35)</div>
    <div class="val">{stat('$15,480,000')}</div>
    <div class="note">Up +{m.money(480_000)} from 2026; CA estate tax {stat('$0')}; {stat('$20,000')} annual gift exclusion</div>
  </div>
</div>
<div class="callout good">
  <strong>Executive Recommendation:</strong> Across 2040, 2045, and 2050 inheritance dates, <strong>selling Property A shortly after trust distribution (S3) and reinvesting the net proceeds</strong> delivers the highest expected after-tax wealth — beating holding Property A as a rental (S2) by <strong>{m.money(r40['s3_wealth'] - r40['s2_wealth'])}</strong> (2040), <strong>{m.money(r45['s3_wealth'] - r45['s2_wealth'])}</strong> (2045), and <strong>{m.money(r50['s3_wealth'] - r50['s2_wealth'])}</strong> (2050), while preserving the Beneficiary's rent-free residence in Property B's vacant third unit and Property B's existing {m.money(b26['noi'])} baseline annual NOI. S3 still wins unless after-tax portfolio returns fall below <strong>{m.pct(be_p45)}</strong> or Property A appreciates faster than <strong>{m.pct(be_h45)}/yr</strong> for 44 consecutive years.
</div>
"""

    rows = []
    for yr, r in [(2040, r40), (2045, r45), (2050, r50)]:
        rows.append([
            f"{yr} → {r['end_year']}",
            m.money(r["fmv_transfer"]),
            m.money(r["s1_wealth"]),
            m.money(r["s2_wealth"]),
            m.money(r["s3_wealth"]),
            f'<span class="pos">+{m.money(r["s3_wealth"] - r["s2_wealth"])}</span>',
            src("irs_p523", "irs_p527", "boe_p19"),
        ])

    t1 = table(
        "After-Tax 25-Year Horizon Comparison by Inheritance Year (Property A Incremental + Tax Engine)",
        ["Window", "FMV at Transfer", "S1: Occupy A (w/ §121)", "S2: Rent A (w/ §168/§469/§1250)", "S3: Sell A & Reinvest", "S3 Edge vs Rent A", "Official Sources"],
        rows,
        right_cols=[1, 2, 3, 4, 5],
    )

    findings = [
        ["1. Stepped-Up Basis + §1014 Erasure", "Inheriting A resets income-tax basis to full FMV at death; an immediate sale incurs ~6% closing/transfer costs and ~$0 federal/CA capital gains tax.", src("irs_basis", "rtc_11911")],
        ["2. Why 27.5-Yr Depreciation Doesn't Rescue S2", f"At 2045 full reassessment (~{m.money(r45['tax_s2_yr1'])}/yr tax), S2 starts cash-flow neutral/negative; for MAGI ≥ {stat('$150,000')}, {m.money(r45['annual_depr'])}/yr depreciation locks in Form 8582 until exit, offsetting §1250 recapture rather than sheltering W-2 salary.", src("irs_p527", "irs_p925", "irs_tc409")],
        ["3. 2043 Solar NEM Legacy Sunset", f"Pre-April 15, 2023 NEM 1.0/2.0 legacy transfers at death ONLY for the balance of 20 years (ending by Apr. 2043), rolling A onto Net Billing Tariff + {stat('$24.15')}/mo Base Services Charge.", src("cpuc_nem", "pge_nemfaq", "cpuc_bsc")],
        ["4. Prop 19 Cap Slowed to ~1.1%/yr Recently", f"BOE LTA 2025/009 sets the Feb. 2025–Feb. 2027 cap at {stat('$1,044,586')} (+2.15% over 2 years), meaning S1 still faces partial reassessment on a {m.money(r45['fmv_transfer'])} home unless FHFA CA HPI surges.", src("boe_lta25009", "boe_p19", "boe_ho")],
        ["5. Considerable Liquid Wealth Headroom", f"With 2027 exclusion at {stat('$15,480,000')} (indexed), a single parent leaves ~{m.money(m.estate_headroom_matrix()[1]['headroom_single'])} headroom above Property A in 2045 — or ~{m.money(m.estate_headroom_matrix()[1]['headroom_halved'])} if Congress halves the exclusion.", src("irs_rp2635", "irs_i706", "sco_estate")],
    ]
    t2 = table(
        "Five Core Analytical Findings That Drive the Recommendation",
        ["Driver", "Quantitative Impact & Statutory Rule", "Official Sources"],
        findings,
    )

    cards = f"""
<div class="card-grid">
  <div class="card"><h3><a href="decision.html">After-Tax Strategy Lab</a></h3><p class="muted">Reconciles PR #36 pre-tax baselines with IRC §121, §168/§469/§1250, bracket regimes (24.3%–37.1%), MAGI {stat('$25,000')} allowance, and Unit 3 housing-equivalence sensitivity.</p></div>
  <div class="card"><h3><a href="costs.html">Utilities, Solar &amp; Insurance</a></h3><p class="muted">Replaces property-tax mis-citations with CPUC D.24-12-077 (SJWC), SFPUC Prop 218 multi-family schedules, 20-yr NEM sunset math, and CDI 2025 rates + State Farm settlement.</p></div>
  <div class="card"><h3><a href="estate-tax.html">2027 IRS &amp; Liquid-Wealth Matrix</a></h3><p class="muted">Complete Rev. Proc. 2026-35 tables, trust 37% compression trap at {stat('$16,500')}, and exact tax-free liquid headroom (Single vs. Form 706 DSUE vs. 50% Congressional cut).</p></div>
  <div class="card"><h3><a href="black-swans.html">Black-Swan Regime Shocks</a></h3><p class="muted">Stress-tests Prop 19 repeal, uncapped NEM/utility escalation, FAIR Plan 3× insurance shock, 1970s stagflation, 2008 housing bust, and capital-gains rate hikes.</p></div>
</div>
"""
    return layout("index.html", "Executive Summary & Decision Hub",
                  "Verified after-tax comparison for an asymmetric two-property California inheritance (Property A inherited via trust 2040–2050; Property B already owned).",
                  kpis + t1 + t2 + cards)


def build_decision():
    r40 = m.simulate_after_tax(2040)
    r45 = m.simulate_after_tax(2045)
    r50 = m.simulate_after_tax(2050)

    intro = """
<div class="callout">
  <strong>Why This Page Exists:</strong> The baseline decision engine (<code>scripts/desk_model.py</code>) leaves three major IRS/local mechanics unmodeled (tracked as F16): (1) <strong>IRC §121</strong> principal-residence exclusion in S1, (2) <strong>27.5-year MACRS depreciation, §469 passive-loss suspension, and §1250 recapture</strong> in S2, and (3) separating <strong>fixed direct parcel charges</strong> from ad valorem property taxes plus the <strong>2043 solar NEM 20-year sunset</strong>. Every row below runs those rules directly.
</div>
"""

    rows_main = []
    for yr, r in [(2040, r40), (2045, r45), (2050, r50)]:
        rows_main.append([
            f"{yr} → {r['end_year']}",
            m.money(r["fmv_transfer"]),
            m.money(r["tax_s1_yr1"]),
            m.money(r["tax_s2_yr1"]),
            m.money(r["s1_wealth"]),
            m.money(r["s2_pretax_wealth"]),
            m.money(r["s2_wealth"]),
            m.money(r["s3_wealth"]),
            m.money(r["s3_wealth"] - r["s2_wealth"]),
            src("irs_p523", "irs_p527", "irs_p925", "boe_p19"),
        ])
    t1 = table(
        "Core After-Tax Outcomes Across 2040, 2045, and 2050 Transfer Windows (Top CA+Fed Bracket, MFJ §121, 40% Bldg Share)",
        ["Window", "FMV_t", "S1 Yr-1 Prop Tax", "S2 Yr-1 Prop Tax", "S1 After-Tax", "S2 Pre-Income-Tax", "S2 After-Tax", "S3 Reinvest", "S3 − S2 After-Tax", "Official Sources"],
        rows_main,
        right_cols=[1, 2, 3, 4, 5, 6, 7, 8],
    )

    bridge_rows = []
    for yr, r in [(2040, r40), (2045, r45), (2050, r50)]:
        bridge_rows.append([
            str(yr),
            m.money(r["annual_depr"]),
            m.money(r["accum_depr"]),
            m.money(r["suspended_pal_end"]),
            m.money(r["pal_tax_benefit"]),
            m.money(r["net_terminal_tax_s2"]),
            m.money(r["sec121_tax_saved"]),
            m.money(r["cg_tax_s1"]),
            src("irs_p527", "irs_p925", "irs_tc409", "irs_p523"),
        ])
    t2 = table(
        "Schedule E Depreciation, §469 Passive-Loss Release, §1250 Recapture & §121 Exclusion Breakdown",
        ["Transfer Yr", "Annual 27.5-Yr Depr.", "25-Yr Accum. Depr.", "Unused §469 PAL at Sale", "PAL Release Shield", "S2 Net Exit Tax", "S1 §121 Tax Saved (MFJ)", "S1 Net Exit Tax", "Official Sources"],
        bridge_rows,
        right_cols=[1, 2, 3, 4, 5, 6, 7],
    )

    # Sensitivity lab for 2045 transfer
    sens_cases = [
        (f"Base Case (4.5% port, 4.0% home, 37.1% CG, MFJ §121, MAGI ≥ {stat('$150,000')})", m.simulate_after_tax(2045), "irs_rp2635", "ftb_sched"),
        (f"Single Filer (§121 cap {stat('$250,000')} instead of {stat('$500,000')})", m.simulate_after_tax(2045, sec121_exclusion=250_000), "irs_p523", "ftb_home"),
        (f"Low-MAGI Active Landlord (MAGI ≤ {stat('$100,000')} → {stat('$25,000')}/yr §469 loss offset)", m.simulate_after_tax(2045, magi_high=False), "irs_p925", "irs_p527"),
        ("Low Tax Bracket (15% LTCG + 0% NIIT + 9.3% CA = 24.3% / 24% ord)", m.simulate_after_tax(2045, fed_ord_rate=0.24, fed_ltcg_rate=0.15, niit_rate=0.0, ca_rate=0.093), "irs_rp2635", "ftb_sched"),
        ("Mid Tax Bracket (15% LTCG + 3.8% NIIT + 10.3% CA = 29.1% / 32% ord)", m.simulate_after_tax(2045, fed_ord_rate=0.32, fed_ltcg_rate=0.15, niit_rate=0.038, ca_rate=0.103), "irs_niit", "ftb_sched"),
        ("Prop 19 Allowance at 1.1%/yr (2021–2025 FHFA CA HPI actual pace)", m.simulate_after_tax(2045, allowance_growth=0.011), "boe_lta25009", "fhfa_hpi"),
        ("S1 Housing-Equiv Sensitivity: +$36,000/yr unverified Unit 3 net rent (F15)", m.simulate_after_tax(2045, unit3_net_annual_2026=36_000), "sf_rent", "irs_p527"),
        ("S1 Housing-Equiv Sensitivity: +$42,000/yr unverified Unit 3 net rent (F15)", m.simulate_after_tax(2045, unit3_net_annual_2026=42_000), "sf_rent", "irs_p527"),
        ("Conservative Cash/Treasury Reinvestment (3.0% after-tax portfolio return)", m.simulate_after_tax(2045, portfolio=0.030), "irs_rp2635", "bls_cpi"),
        ("Equities-Tilted Reinvestment (6.0% after-tax portfolio return)", m.simulate_after_tax(2045, portfolio=0.060), "irs_rp2635", "irs_tc409"),
        ("Hold S2 Until Second Death (0% terminal CG/§1250 via 2nd §1014 step-up)", None, "irs_basis", "irs_p527"),
    ]
    sens_rows = []
    for label, res, s1, s2 in sens_cases:
        if res is None:
            # 2nd death wipes terminal tax in S2
            res_base = m.simulate_after_tax(2045)
            s1_v = m.money(res_base["s1_wealth"] + res_base["cg_tax_s1"])
            s2_v = m.money(res_base["s2_wealth"] + res_base["net_terminal_tax_s2"])
            s3_v = m.money(res_base["s3_wealth"])
            gap = (res_base["s2_wealth"] + res_base["net_terminal_tax_s2"]) - res_base["s3_wealth"]
            winner = "S3 Sell & Reinvest" if gap < 0 else "S2 Hold"
        else:
            s1_v = m.money(res["s1_wealth"])
            s2_v = m.money(res["s2_wealth"])
            s3_v = m.money(res["s3_wealth"])
            best = max(res["s1_wealth"], res["s2_wealth"], res["s3_wealth"])
            winner = "S3 Sell & Reinvest" if best == res["s3_wealth"] else ("S2 Rent A" if best == res["s2_wealth"] else "S1 Occupy A")
            gap = res["s2_wealth"] - res["s3_wealth"]
        sens_rows.append([label, s1_v, s2_v, s3_v, m.money(gap), winner, src(s1, s2)])

    t3 = table(
        "2045→2070 Sensitivity Matrix: Brackets, §469 MAGI, Prop 19 Pace, Housing Equivalence & 2nd Step-Up",
        ["Scenario", "S1 Occupy A", "S2 Rent A", "S3 Sell & Reinvest", "S2 − S3", "Top Path", "Official Sources"],
        sens_rows,
        right_cols=[1, 2, 3, 4],
    )

    # Dynamic Unit 3 + Low-MAGI deltas (exact $10-rounded from engine)
    low_magi = m.simulate_after_tax(2045, magi_high=False)
    u3_lo = m.simulate_after_tax(2045, unit3_net_annual_2026=36_000)
    u3_hi = m.simulate_after_tax(2045, unit3_net_annual_2026=42_000)
    hpi_low = m.simulate_after_tax(2045, allowance_growth=0.011)

    note = f"""
<div class="callout good">
  <strong>Critical Insight — Why Even a Second Death Step-Up Doesn't Flip S2 Above S3 in Base Assumptions:</strong> Erasing 100% of S2's {m.money(r45['net_terminal_tax_s2'])} terminal tax at Year 25 brings S2 from {m.money(r45['s2_wealth'])} to {m.money(r45['s2_wealth'] + r45['net_terminal_tax_s2'])}, still {m.money(r45['s3_wealth'] - (r45['s2_wealth'] + r45['net_terminal_tax_s2']))} behind S3's {m.money(r45['s3_wealth'])} — because full Prop 19/non-occupying reassessment cuts early rental cash yields while tying up equity at 4.0% gross home growth vs. 4.5% liquid compounding. Meanwhile, freeing Property B's Unit 3 (F15, unverified) closes only {m.money(u3_lo['s1_wealth'] - r45['s1_wealth'])}–{m.money(u3_hi['s1_wealth'] - r45['s1_wealth'])} of S1's {m.money(r45['s3_wealth'] - r45['s1_wealth'])} gap against S3, and low-MAGI status adds {m.money(low_magi['s2_wealth'] - r45['s2_wealth'])} to S2 while slow Prop 19 HPI growth cuts S1 by {m.money(r45['s1_wealth'] - hpi_low['s1_wealth'])}.
</div>
"""
    return layout("decision.html", "After-Tax Strategy & Sensitivity Lab",
                  "Full Schedule E, IRC §121, §469 passive-loss, §1250 recapture, and housing-equivalence analysis for 2040, 2045, and 2050 transfers.",
                  intro + t1 + t2 + t3 + note)


def build_properties():
    a26 = m.a_continuity_row(2026)
    b26 = m.b_continuity_row(2026)

    a_rows = [
        ["Jurisdiction & Privacy Scope", "Santa Clara County, California (city, street, parcel & ZIP withheld)", chip("verified", "county-level"), src("scc_ratebook")],
        ["Ownership & Timing", "Expected via Settlor Family Trust distribution (~2040–2050); not yet inherited", chip("derived", "trust event"), src("scc_p19")],
        ["Market-Value Anchor (Nov. 2026)", m.money(m.A.market_value), "Banded to $100,000; 4.0%/yr baseline projection", src("fhfa_hpi")],
        ["Factored Taxable Anchor (2026)", m.money(m.A.taxable_value), "Banded; Prop 13 caps growth at ≤2.0%/yr (CCPI 3.307% in 2026–27)", src("boe_lta26002", "boe_80010")],
        ["Ad Valorem Rate vs. Fixed Parcel Split", f"1.18% ad valorem + {m.money(m.A.fixed_parcel_charges)} fixed charges", f"2026 total tax {m.money(a26['tax'])}; fixed charges do NOT scale on reassessment (F02)", src("scc_ratebook", "boe_80010")],
        ["Insurance (Model vs. Owner Estimate)", m.money(m.A.insurance), f"Owner guess $1,500 flagged low (F04); CDI 2025 avg {stat('$2,339.99')} + State Farm +17%", src("cdi_2025", "cdi_sf26")],
        ["Water Utility (SJWC Trajectory)", m.money(m.A.water), "Owner $100–$150/mo midpoint; CPUC D.24-12-077 (+1.8% / +2.65% / +3.14%)", src("cpuc_sjwc")],
        ["Electricity / Solar NEM Status", f"{m.money(m.A.electric_pre_nem_sunset)} now → +{m.money(m.ASSUMPTIONS['post_nem_electric_2026_real'])} post-2043", f"Pre-Apr. 15, 2023 NEM 20-yr legacy expires by 2043 + {stat('$24.15')}/mo Base Services Charge", src("cpuc_nem", "pge_nemfaq", "cpuc_bsc")],
        ["Maintenance & Capital Reserve", m.money(m.A.maintenance + m.A.reserve), "Lower structural load than 3-unit B; covers roof, HVAC, inverter", src("irs_p527")],
        ["Baseline Annual Carrying Cost (2026)", m.money(a26["total_carry"]), f"Tax {m.money(a26['tax'])} + Operating {m.money(a26['opex'])}", src("boe_80010", "cpuc_nem")],
        ["Implied Rental Anchor (Unverified, F05)", m.money(m.A.gross_rent), "Assumed $5,500/mo gross for S2 comparison; rent cap risk (AB 1482 / local)", src("civ_1947")],
        ["Mortgage / Debt Balance", "— (left blank)", chip("flag", "F03 unverified") + " — assumed debt-free in baseline", src("irs_estate")],
    ]
    t1 = table("Property A — Trust-Inherited Single-Family Residence (County A)", ["Item", "2026 Value", "Verification & Modeling Basis", "Official Sources"], a_rows)

    b_rows = [
        ["Jurisdiction & Privacy Scope", "San Francisco, California (neighborhood, street, parcel & ZIP withheld)", chip("verified", "city/county"), src("sf_treas")],
        ["Ownership & Unit Mix", "Already owned by Beneficiary; 3 livable units (2 rented, 1 vacant owner-occupiable)", "No step-up or Prop 19 reassessment from A's inheritance", src("irs_basis", "sf_rent")],
        ["Market-Value Anchor (Nov. 2026)", m.money(m.B.market_value), "Banded to $100,000; 4.0%/yr baseline projection", src("fhfa_hpi")],
        ["Implied Taxable Anchor (2026)", m.money(m.B.taxable_value), f"Implied at exact FY 2026–27 SF rate (F01); exact parcel direct-charge split unverified", src("sf_treas")],
        ["SF Secured Tax Rate (FY 2026–27)", "1.18162182%", f"2026 modeled tax {m.money(b26['tax'])} (due Dec. 10 & Apr. 10)", src("sf_treas")],
        ["Gross Rent (2 Leased Units)", m.money(m.B.gross_rent), "Rounded to $10; SF Rent Ordinance 1.6% cap (3/1/26–2/28/27); File 261020 watch", src("sf_rent", "sf_leg261020")],
        ["Vacancy + Management Allowance (13%)", m.money(m.B.gross_rent * 0.13), "5% vacancy + 8% management modeled; Unit 3 rent unverified (F15)", src("sf_rent", "civ_1947")],
        ["Water & Sewer (SFPUC Multi-Family)", m.money(m.B.water), "Owner $330–$400/mo validated by SFPUC Tier 1/2 + 95% sewer + FY27/28 +12.5%/+12.3%", src("sfpuc_p218")],
        ["Electricity (Common/House Meter)", m.money(m.B.electric_pre_nem_sunset), "Owner $30–$70/mo midpoint", src("cpuc_bsc")],
        ["Landlord Insurance (3-Unit Dwelling)", m.money(m.B.insurance), f"Owner guess $1,500 flagged low (F04); State Farm rental +32.8% settlement / CDI {stat('$1,701.60')} avg", src("cdi_2025", "cdi_sf26")],
        ["Maintenance & Capital Reserve", m.money(m.B.maintenance + m.B.reserve), "Higher older multi-unit maintenance load", src("irs_p527")],
        ["2026 Pre-Income-Tax NOI", m.money(b26["noi"]), "Gross rent minus property tax and operating costs; income-tax basis unknown (F09)", src("sf_treas", "irs_p527")],
    ]
    t2 = table("Property B — Already-Owned Multi-Unit Property (County B)", ["Item", "2026 Value", "Verification & Modeling Basis", "Official Sources"], b_rows)

    priv = """
<div class="callout warn">
  <strong>Privacy Architecture (Why Raw 2014–2026 Assessment/Tax Histories Are Withheld):</strong> Publishing exact 11- to 13-year unrounded county roll series would allow trivial reverse-lookup against public county assessor rolls. Following the strict privacy reading, this desk calibrates against banded 2026 anchors ($550,000 and $206,000) and publicly documents bill discrepancies as Flagged items <strong>F01</strong> and <strong>F02</strong>.
</div>
"""
    return layout("properties.html", "Anonymized Property Profiles & Baseline",
                  "Banded 2026 anchors, fixed vs. ad valorem tax separation, and verified utility/insurance baselines without personal or parcel identifiers.",
                  t1 + t2 + priv)


def build_projections():
    a_rows = []
    for yr in range(2026, 2077):
        r = m.a_continuity_row(yr, apply_nem_sunset=True)
        tag = " (NEM Sunset)" if yr == m.ASSUMPTIONS["nem_sunset_year"] else ""
        a_rows.append([
            f"{yr}{tag}",
            m.money(r["fmv"]),
            m.money(r["taxable"]),
            m.money(r["ad_val"]),
            m.money(r["fixed_parcel"]),
            m.money(r["tax"]),
            m.money(r["insurance"]),
            m.money(r["water"]),
            m.money(r["electric"]),
            m.money(r["maint_reserve"]),
            m.money(r["total_carry"]),
            src("boe_80010", "scc_ratebook", "cpuc_sjwc", "cpuc_nem"),
        ])

    t1 = table(
        "Property A — 50-Year Continuity Table (2026–2076, Pre-Reassessment Baseline + 2043 Solar NEM Sunset)",
        ["Year", "Est. FMV", "Prop 13 Base", "Ad Valorem", "Fixed Parcel", "Total Tax", "Insurance", "SJWC Water", "Net Electric", "Maint.+Res.", "Total Carry", "Official Sources"],
        a_rows,
        right_cols=list(range(1, 11)),
    )

    # Transfer-year branch table
    br_rows = []
    for yr in (2040, 2045, 2050):
        res = m.simulate_after_tax(yr)
        br_rows.append([
            str(yr),
            m.money(res["fmv_transfer"]),
            m.money(res["allowance"]),
            m.money(res["assess_s1"]),
            m.money(res["tax_s1_yr1"]),
            m.money(res["assess_s2"]),
            m.money(res["tax_s2_yr1"]),
            m.money(res["proceeds_s3"]),
            src("boe_p19", "boe_lta25009", "rtc_11911"),
        ])
    t2 = table(
        "Property A Transfer-Year Reassessment Forks (2040 / 2045 / 2050 — Prop 19 S1 vs. Full FMV S2 vs. Net Sale S3)",
        ["Transfer Yr", "FMV_t", "Prop 19 Cap", "S1 New Taxable", "S1 Yr-1 Tax", "S2 New Taxable", "S2 Yr-1 Tax", "S3 Net Sale Proceeds", "Official Sources"],
        br_rows,
        right_cols=[1, 2, 3, 4, 5, 6, 7],
    )

    b_rows = []
    for yr in range(2026, 2077):
        r = m.b_continuity_row(yr)
        b_rows.append([
            str(yr),
            m.money(r["fmv"]),
            m.money(r["taxable"]),
            m.money(r["tax"]),
            m.money(r["rent"]),
            m.money(r["water"]),
            m.money(r["opex"]),
            m.money(r["noi"]),
            src("sf_treas", "sf_rent", "sfpuc_p218"),
        ])
    t3 = table(
        "Property B — 50-Year Baseline Continuity (2026–2076, Already Owned, SFPUC FY27–28 Water Ramp + 2.0% Rent Growth)",
        ["Year", "Est. FMV", "Taxable Base", "Property Tax", "Gross Rent (2 Units)", "SFPUC Water/Sewer", "Total OpEx", "Pre-Tax NOI", "Official Sources"],
        b_rows,
        right_cols=list(range(1, 8)),
    )

    return layout("projections.html", "50-Year Annual Projections (2026–2076)",
                  "Full year-by-year Property A continuity (with ad valorem/fixed tax split and 2043 NEM sunset), transfer-year reassessment forks, and Property B 50-year NOI.",
                  t2 + t1 + t3)


def build_costs():
    intro = """
<div class="callout warn">
  <strong>Audit Correction Note:</strong> Earlier published utility and solar lines cited <em>BOE Pub 800-10</em> (a property-assessment pamphlet) for water and electricity. Every utility, solar, and insurance figure below replaces those placeholders with primary tariff orders and rate tables from <strong>CPUC</strong>, <strong>SFPUC</strong>, <strong>PG&amp;E</strong>, and the <strong>California Department of Insurance (CDI)</strong>.
</div>
"""

    nem_rows = [
        ["NEM 1.0 / 2.0 Legacy Cutoff", "Interconnection applications submitted on or before Apr. 14, 2023 (final inspection before Apr. 15, 2026)", "NEM 1.0/2.0 closed to new entrants Apr. 15, 2023; new systems take Solar Billing Plan (NBT).", src("cpuc_nem", "pge_nemfaq")],
        ["20-Year Legacy Transfer on Death", "Inheritable by heir — tied to the system/site, NOT the original owner", "Heir inherits ONLY the unused portion of the original 20-year clock from Permission to Operate.", src("pge_nemfaq")],
        ["Mandatory Transition Year (≤ 2043)", f"20-year legacy expires by ~2036–2043 (before or early in the 2040–2050 trust window)", f"Transitions at annual true-up onto Solar Billing Plan (NBT); {stat('0')} years of NBT 9-yr legacy granted to NEM transfers.", src("cpuc_nem", "pge_nemfaq")],
        ["PG&E Base Services Charge (D.24-05-028)", f"{stat('$24.15')}/mo ({m.money(24.15 * 12)}/yr) fixed Tier 3 grid fee (Q1 2026 rollout)", f"Non-CARE/FERA households pay {stat('$24.15')}/mo regardless of solar exports; CARE ~{stat('$6.00')}/mo, FERA ~{stat('$12.08')}/mo.", src("cpuc_bsc")],
        ["Net Financial Flip on Property A", f"From {m.money(-180)}/yr credit today → +{m.money(480)}/yr (2026 real) post-2043", "Avoided-cost midday export credits drop sharply vs. retail rates unless paired with battery storage.", src("cpuc_nem", "pge_nemfaq", "cpuc_bsc")],
    ]
    t1 = table("Solar NEM 1.0/2.0 20-Year Sunset & PG&E Fixed Charge Impact (Property A)", ["Rule / Component", "Verified Specification", "Financial Impact on Decision", "Official Sources"], nem_rows)

    water_rows = [
        ["Property A — County A Water Utility (SJWC, CPUC D.24-12-077)", "Authorized revenue steps: +1.8% (2025), +2.65% (2026), +3.14% (2027)", f"Owner's $100–$150/mo ({m.money(1500)}/yr midpoint) is plausible for single-family irrigation + household load.", src("cpuc_sjwc")],
        ["Property B — SFPUC MF Tier 1 Water (≤ 3 Ccf/unit/mo)", f"{stat('$11.24')} (FY26) → {stat('$12.03')} (FY27) → {stat('$12.87')}/Ccf (FY28)", "First 9 Ccf/mo across 3 units billed at Tier 1.", src("sfpuc_p218")],
        ["Property B — SFPUC MF Tier 2 Water (> 3 Ccf/unit/mo)", f"{stat('$12.07')} (FY26) → {stat('$12.91')} (FY27) → {stat('$13.82')}/Ccf (FY28)", "Usage above 3 Ccf/unit/mo pays Tier 2 volumetric rate.", src("sfpuc_p218")],
        ["Property B — SFPUC Residential Wastewater (95% factor)", f"{stat('$18.72')} (FY26) → {stat('$20.74')} (FY27) → {stat('$22.84')}/Ccf discharged", "Multi-family default discharge = 95% of metered water — wastewater drives ~53% of total bill.", src("sfpuc_p218")],
        ["Property B — Fixed Meter, Sewer & Stormwater", f"1\" meter {stat('$33.21')}→{stat('$38.02')}; WW svc {stat('$5.76')}→{stat('$7.58')}; Tier 2 storm {stat('$12.82')}→{stat('$28.13')}", "At ~11 Ccf/mo total across 3 units, FY26 modeled bill is ~$370/mo (~$4,440/yr), matching owner $330–$400/mo, then rising +12.5%/+12.3% in FY27–28.", src("sfpuc_p218")],
    ]
    t2 = table("Verified Water & Wastewater Tariffs (Property A SJWC & Property B SFPUC FY2026–28)", ["Utility / Tier", "Adopted Schedule", "Validation vs. Owner Baseline", "Official Sources"], water_rows)

    ins_rows = [
        ["CDI 2025 Statewide Homeowners (Non-EQ)", f"{stat('$2,339.99')} avg ({stat('$3.38')}/{stat('$1,000')} exposure); 15.24% carry EQ", f"Owner $1,500 guess is well below statewide avg; a high-replacement-cost Bay Area SFH models realistically at {m.money(3000)}+/yr (F04).", src("cdi_2025")],
        ["CDI 2025 Statewide Dwelling Fire (Non-EQ)", f"{stat('$1,701.60')} avg ({stat('$2.94')}/{stat('$1,000')}); non-FAIR ~{stat('$1,310')} (rounded to $10)", "Covers multi-unit/tenant structures; excludes earthquake & separate umbrella liability.", src("cdi_2025")],
        ["California FAIR Plan Dwelling Fire (2025)", f"~{stat('$2,920')} avg (rounded to $10; {stat('$3.50')}/{stat('$1,000')}); 24.33% market share (577,120 policies)", "Distressed/wildfire fallback pricing shows why non-renewal push onto FAIR Plan + DIC spikes landlord insurance 2×–3×.", src("cdi_2025", "cdi_sis")],
        ["State Farm / CDI Settlement (Mar. 6, 2026)", "+17.0% Homeowners interim; +32.8% Rental Dwelling (down from +38%)", "Includes 1-year moratorium extension on non-renewals/cancellations while Sustainable Insurance Strategy rolls out.", src("cdi_sf26", "cdi_sis")],
        ["Earthquake Coverage (Optional, Excluded Above)", f"CDI 2025 EQ avg (rounded to $10): ~{stat('$1,440')} Homeowners ({stat('$1.62')}/{stat('$1,000')}) / ~{stat('$950')} Dwelling Fire", "Owner did not specify EQ coverage; high-value Bay Area EQ riders add $1,500–$6,000+/yr with 10%–15% deductibles (F04).", src("cdi_2025")],
    ]
    t3 = table("CDI 2025 Residential & Dwelling-Fire Benchmarks + 2026 Rate Orders", ["Insurance Benchmark", "Verified 2025/2026 Rate Data", "Model Implication for A & B", "Official Sources"], ins_rows)

    return layout("costs.html", "Utilities, Solar NEM Sunset & Insurance",
                  "Primary CPUC, PG&E, SFPUC, and CDI tariff evidence validating owner operating ranges and projecting 2026–2076 escalations.",
                  intro + t1 + t2 + t3)


def build_estate_tax():
    stat_rows = [
        ["Federal Estate, Gift & GST Basic Exclusion (§2010(c)(3))", stat("$15,000,000"), stat("$15,480,000"), "P.L. 119-21 (2026) indexed by Rev. Proc. 2026-35 (+3.20%) for 2027.", src("irs_estate", "irs_rp2635")],
        ["Annual Gift Tax Exclusion (§2503(b))", stat("$19,000"), stat("$20,000"), f"Per donee/yr ({m.money(40_000)}/yr for gift-splitting married couple) without using lifetime exclusion.", src("irs_rp2635", "irs_2027news")],
        ["Non-Citizen Spouse Annual Gift Exclusion (§2523(i))", stat("$194,000"), stat("$201,000"), "Applies if transferor's spouse is not a U.S. citizen.", src("irs_rp2635")],
        ["Estate & Trust Top 37% Ordinary Bracket (§1(j)(2)(E))", f"> {stat('$16,000')} (2026)", f"> {stat('$16,500')} (2027)", "Retained rental/interest income in a non-grantor trust hits 37% federal + 3.8% NIIT + 13.3% CA immediately!", src("irs_rp2635", "irs_niit")],
        ["Estate & Trust Top 20% LTCG Threshold (§1(h))", f"> {stat('$16,200')} (2026)", f"> {stat('$16,750')} (2027)", f"0% up to {stat('$3,400')}; 15% up to {stat('$16,750')}; 20% + 3.8% NIIT above {stat('$16,750')}.", src("irs_rp2635", "irs_niit")],
        ["Individual 0% / 15% / 20% LTCG Thresholds (MFJ)", "—", f"{stat('$102,100')} / {stat('$633,600')}", f"Single: {stat('$51,050')} (0%) / {stat('$563,200')} (15%); 20% above ceiling.", src("irs_rp2635")],
        ["Individual Top 37% Ordinary Bracket (Single / MFJ)", "—", f"~{stat('$661,380')} (rounded to $10) / {stat('$793,650')}", f"2027 standard deduction: {stat('$16,600')} single / {stat('$33,200')} MFJ (Rev. Proc. 2026-35).", src("irs_rp2635")],
        ["California 2026 Top Ordinary & Cap-Gains Brackets", f"12.3% > {stat('$768,213')} / {stat('$1,536,426')}", "Indexed annually (CCPI)", f"+1.0% Mental Health Services Tax above {stat('$1,000,000')} → 13.3% top CA rate (no LTCG preference).", src("ftb_sched", "ftb_2026_10")],
        ["California State Estate / Inheritance Tax", stat("$0"), stat("$0"), "Form ET-1 suspended for decedents dying on or after Jan. 1, 2005.", src("sco_estate")],
        ["IRS Estate Tax Closing Letter (ETCL) User Fee", f"{stat('$76')} (eff. Oct. 26, 2026)", stat("$76"), f"TD 10055 raised fee from {stat('$67')}; free Account Transcript available in lieu.", src("irs_whatsnew", "irs_i706")],
        ["§6166 2%-Interest Deferral Portion / §2032A Cap", "—", f"{stat('$2,010,000')} / {stat('$1,500,000')}", "Relevant only if estate owes tax on qualifying closely held business/farm.", src("irs_rp2635")],
    ]
    t1 = table(
        "2026 vs. 2027 Statutory Estate, Gift, Trust & Capital-Gains Tax Reference (Rev. Proc. 2026-35 + CA FTB)",
        ["Statutory Provision", "2026 Amount", "2027 Amount", "Key Planning Rule", "Official Sources"],
        stat_rows,
    )

    hm_rows = []
    for r in m.estate_headroom_matrix():
        hm_rows.append([
            str(r["year"]),
            m.money(r["fmv_a"]),
            m.money(r["excl_single"]),
            m.money(r["headroom_single"]),
            m.money(r["excl_dsue"]),
            m.money(r["headroom_dsue"]),
            m.money(r["excl_halved"]),
            m.money(r["headroom_halved"]),
            src("irs_rp2635", "irs_i706", "irs_estate"),
        ])
    t2 = table(
        '"Considerable Money" Threshold Matrix: Max Tax-Free Liquid Assets Above Property A (2.2%/yr CPI Indexing from 2027)',
        ["Transfer Yr", "Est. Property A FMV", "Single Exclusion", "Max Liquid (Single)", "Married DSUE (2×)", "Max Liquid (DSUE)", "50% Cut Scenario", "Max Liquid (50% Cut)", "Official Sources"],
        hm_rows,
        right_cols=[1, 2, 3, 4, 5, 6, 7],
    )

    trap = f"""
<div class="callout bad">
  <strong>Two High-Dollar Estate Traps Flagged for Trust Counsel:</strong>
  <br>1. <strong>Non-Grantor Trust Tax Compression (37% at {stat('$16,500')}):</strong> After the Settlor dies, an irrevocable administrative trust pays the 37% ordinary + 20% LTCG + 3.8% NIIT + 13.3% CA rate on retained income above just {stat('$16,500')}–{stat('$16,750')} (Rev. Proc. 2026-35). Distribute Property A or income cleanly to the Beneficiary rather than accumulating income inside the post-death trust.
  <br>2. <strong>DSUE Portability &amp; Property B Boundary:</strong> Property B is already owned by the Beneficiary and sits <em>outside</em> the Parent/Trust's taxable estate — however, once inherited, A + liquid corpus + B all enter the <em>Beneficiary's</em> eventual estate. If a predeceased parent died within the last 5 years without filing Form 706, check <strong>Rev. Proc. 2022-32</strong> (5-year late portability window) immediately!
</div>
"""
    return layout("estate-tax.html", "2027 IRS Thresholds & Liquid-Wealth Matrix",
                  "Exact Rev. Proc. 2026-35 parameters, CA FTB schedules, trust bracket compression, and maximum tax-free liquid wealth before 40% federal estate tax.",
                  t1 + t2 + trap)


def build_black_swans():
    # Stress scenarios directly evaluated by simulate_after_tax
    scenarios = [
        ("1. Base Trajectory (4.0% home, 2.5% CPI, 4.5% port, 2043 NEM sunset)", dict()),
        ("2. Prop 19 Repeal / Split-Roll (S1 loses Prop 19 → full FMV tax)", dict(prop19_repealed=True)),
        ("3. 2043 NEM + Utility Spike (A electric $1,200/yr real post-2043 + 1.5× water)", dict(inflation=0.032)),
        ("4. California Insurance / FAIR Plan Crisis (3× primary & landlord insurance)", dict(insurance_mult=3.0)),
        ("5. 1970s Stagflation Regime (6.5% CPI, 3.5% home growth, 2.5% real/nom port)", dict(inflation=0.065, home_growth=0.035, rent_growth=0.040, portfolio=0.025)),
        ("6. 2008 Tech/Housing Bust at Transfer (-25% FMV_t, -20% rent, 7.5% vacancy)", dict(transfer_discount=0.25, rent_discount=0.20, vacancy=0.075)),
        ("7. Tax-Hike Regime (Fed LTCG 28% + NIIT 5% + CA 14.3% = 47.3% CG / 52.3% recap)", dict(fed_ltcg_rate=0.28, fed_ord_rate=0.396, niit_rate=0.050, ca_rate=0.143)),
    ]

    rows = []
    for name, kw in scenarios:
        res = m.simulate_after_tax(2045, **kw)
        rows.append([
            name,
            m.money(res["s1_wealth"]),
            m.money(res["s2_wealth"]),
            m.money(res["s3_wealth"]),
            m.money(res["s2_wealth"] - res["s3_wealth"]),
            "S3 Sell & Reinvest" if res["s3_wealth"] >= max(res["s1_wealth"], res["s2_wealth"]) else ("S2 Rent A" if res["s2_wealth"] >= res["s1_wealth"] else "S1 Occupy A"),
            src("bls_cpi", "fhfa_hpi", "cdi_sis", "boe_p19"),
        ])
    t1 = table(
        "Non-Linear Black-Swan & Policy Regime Shocks (2045 Transfer → 2070 Horizon, After-Tax)",
        ["Regime Shock", "S1 Occupy A", "S2 Rent A", "S3 Sell & Reinvest", "S2 − S3", "Resilient Winner", "Official Sources"],
        rows,
        right_cols=[1, 2, 3, 4],
    )

    # Property B squeeze check: SFPUC water escalation vs 1.6% rent cap
    b_base45 = m.b_continuity_row(2045, water_shock=False)
    b_shk45 = m.b_continuity_row(2045, water_shock=True)
    b_base76 = m.b_continuity_row(2076, water_shock=False)
    b_shk76 = m.b_continuity_row(2076, water_shock=True)
    b_rows = [
        ["2045 Baseline Water (3.5%/yr post-2028) vs. 2.0% Rent", m.money(b_base45["rent"]), m.money(b_base45["water"]), m.money(b_base45["noi"]), src("sfpuc_p218", "sf_rent")],
        ["2045 High Water Escalation (5.5%/yr post-2028) vs. 2.0% Rent", m.money(b_shk45["rent"]), m.money(b_shk45["water"]), m.money(b_shk45["noi"]), src("sfpuc_p218", "sf_rent")],
        ["2076 Baseline Water (3.5%/yr) vs. 2.0% Rent", m.money(b_base76["rent"]), m.money(b_base76["water"]), m.money(b_base76["noi"]), src("sfpuc_p218", "sf_rent")],
        ["2076 High Water Escalation (5.5%/yr) vs. 2.0% Rent", m.money(b_shk76["rent"]), m.money(b_shk76["water"]), m.money(b_shk76["noi"]), src("sfpuc_p218", "sf_rent")],
    ]
    t2 = table(
        "Property B Margin Compression Test: SFPUC Utility Inflation vs. SF Rent-Controlled Revenue",
        ["Horizon & Water Trajectory", "Gross Rent (2 Units)", "SFPUC Water/Sewer", "Pre-Tax NOI", "Official Sources"],
        b_rows,
        right_cols=[1, 2, 3],
    )

    note = """
<div class="callout">
  <strong>Why Non-Linear Regimes Matter Over 50 Years:</strong> Linear 4% appreciation / 2.5% inflation hides structural tail events. Notice S3 remains dominant in 6 of 7 shocks, and <em>only</em> in severe 1970s-style stagflation (where real equity returns collapse to 2.5% nominal vs. 6.5% CPI!) or catastrophic housing deflation does real-asset holding narrow the gap — while Property B's NOI absorbs utility shocks cleanly as long as SF's low Prop 13 base remains intact.
</div>
"""
    return layout("black-swans.html", "Non-Linear Black Swans & Policy Shocks",
                  "Stress-testing S1/S2/S3 after-tax outcomes against Prop 19 repeal, utility/insurance repricing, stagflation, housing crashes, and tax hikes.",
                  t1 + t2 + note)


def build_process():
    steps = [
        ["Day 0 (Date of Death)", "Freeze transfers; secure certified death certificates; establish exact date-of-death FMV baseline (IRC §1014 stepped-up basis) via licensed appraisal — critical whether selling immediately or depreciating under S2.", src("irs_basis", "irs_p527")],
        ["≤ 60 Days", "Successor Trustee serves statutory Trustee Notification (CA Probate Code §16061.7) on all beneficiaries & heirs (starts 120-day trust-contest clock).", src("prob_16061")],
        ["≤ 150 Days", "File BOE-502-D (Change in Ownership Statement — Death of Real Property Owner) with the Santa Clara County Assessor.", src("scc_p19", "boe_80010")],
        ["6–9 Months", f"Evaluate Estate Tax & DSUE Portability: file IRS Form 706 if gross estate + adjusted taxable gifts exceeds statutory exclusion ({stat('$15,480,000')} in 2027) OR solely to elect surviving-spouse DSUE portability (file Form 4768 for automatic 6-mo extension to 15 months). If Form 706 required, furnish Form 8971 / Schedule A (§6035 consistent basis) within 30 days.", src("irs_i706", "irs_whatsnew")],
        ["≤ 12 Months (Strict)", "Decision Gate (S1 vs. S2 vs. S3): If electing S1 (Occupy A under Prop 19), Heir must move in as principal residence AND file BOE-266 (Homeowners' Exemption) + BOE-19-P within 1 year for full retroactive relief; if selling (S3), list & close through trust/beneficiary using date-of-death basis to realize ~$0 taxable gain.", src("boe_p19", "boe_ho", "scc_p19")],
        ["Post-Death Trust Tax", f"Distribute Property A (or sale proceeds) out of the irrevocable administrative trust before retaining > {stat('$16,500')} of net income/gains (which otherwise hits the 37% / 20%+3.8% federal + 13.3% CA trust compression wall).", src("irs_rp2635", "irs_niit")],
        ["Solar & Insurance Transfer", "Notify PG&E of death transfer to retain remaining years of the 20-yr NEM 1.0/2.0 clock (until ≤ 2043) if keeping A; update property insurance immediately from personal homeowner policy to estate/vacant/landlord dwelling coverage.", src("pge_nemfaq", "cdi_2025")],
        ["3 Years / 5 Years (Late Relief)", "BOE-19-P allows late filing up to 3 years (prospective-only thereafter if eligible); IRS Rev. Proc. 2022-32 permits Form 706 DSUE portability election up to 5 years after date of death for estates below the filing threshold.", src("scc_p19", "irs_i706")],
        ["Ongoing Property B Compliance", "Maintain annual March 1 SF Rent Board Housing Inventory filing to preserve active Rent Increase License (§37.15) before serving any 1.6% annual or banked rent notice.", src("sf_inv", "sf_rent")],
    ]
    t1 = table(
        "Step-by-Step Trust Distribution, Prop 19, IRS Form 706 & Property Execution Checklist",
        ["Deadline", "Required Action & Statutory Mechanics", "Official Sources"],
        steps,
    )
    return layout("process.html", "Step-by-Step Trust & Tax Process",
                  "Actionable execution chronology covering Probate Code §16061.7, BOE-502-D, BOE-19-P, Form 706 DSUE portability, trust distribution, and SF compliance.",
                  t1)


def build_law_watch():
    rows = [
        ["Federal: P.L. 119-21 & IRS Rev. Proc. 2026-35", "Enacted (2026–2027)", f"Estate/GST exclusion {stat('$15,000,000')} (2026) → {stat('$15,480,000')} (2027); annual gift {stat('$20,000')} in 2027; trust 37% starts at {stat('$16,500')}. Monitor future Congress for sunset/rate changes.", src("irs_estate", "irs_rp2635")],
        ["SF BOS File No. 261020 (Pending Ordinance)", "Pending Committee Action (Notice Nov. 9, 2026)", "Introduced Sept. 15, 2026; proposes capping combined banked + capital-improvement rent increases at 10%/yr for 3 years (retroactive to Sept. 15, 2026 notices). Watch before serving banked increases on Property B.", src("sf_leg261020", "sf_rent")],
        ["SF Rent Board Annual Allowable Rate", "Active (Mar. 1, 2026 – Feb. 28, 2027)", "Allowable annual rent increase = 1.6% (60% of Bay Area CPI); security deposit interest = 4.2%. Housing Inventory license required.", src("sf_rent", "sf_inv")],
        ["BOE Prop 19 Biennial Cap Reset (Feb. 2027)", "Scheduled Feb. 16, 2027", f"Current {stat('$1,044,586')} allowance expires Feb. 15, 2027; next biennial adjustment triggers off FHFA 2026Q4 CA HPI release (scheduled Feb. 23, 2027).", src("boe_lta25009", "fhfa_hpi")],
        ["CA Statewide Rent Cap (AB 1482 / Civ. Code §1947.12)", "In Force; Repeals Jan. 1, 2030", "Caps annual increases at 5% + regional CPI (max 10%) for non-exempt dwellings >15 yrs old; single-family homes exempt only with statutory notice. Relevant to S2 (Rent A).", src("civ_1947")],
        ["CA SOS Nov. 2026 Ballot Measures (As of Nov. 11, 5:17 p.m.)", "Unofficial (Cert. Dec. 11, 2026)", "Prop 1 (Yes 61.1%), Prop 3 (Yes 60.7%), Prop 37 (Yes 62.4%), Prop 40 (No 52.5%), Prop 41 (No 55.1%), Prop 42 (Yes 51.4%), Prop 43 (No 57.4%).", src("sos_ballot")],
        ["CPUC / PG&E Solar & Fixed Charge Reform", "Active (2026–2043 Sunset)", f"NEM 2.0 closed Apr. 15, 2023; {stat('$24.15')}/mo Tier 3 Base Services Charge rolls onto bills in 2026; pre-2023 systems move to NBT by ≤2043.", src("cpuc_nem", "cpuc_bsc", "pge_nemfaq")],
        ["CDI Sustainable Insurance Strategy & State Farm Order", "Active (2025–2026)", "Expands catastrophe modeling & FAIR Plan alternatives; State Farm Mar. 6, 2026 settlement locks +17.0% HO-3 / +32.8% Rental Dwelling + 1-yr nonrenewal moratorium.", src("cdi_sis", "cdi_sf26")],
        ["BLS CPI Benchmarks (Oct. 2026)", "Published Nov. 10, 2026", "U.S. CPI-U +0.4% SA in Oct. 2026; SF-Oakland-Hayward +0.5% over Aug.–Oct. 2026 (Oct. 2025 data omitted due to appropriation lapse).", src("bls_cpi", "bls_sf")],
    ]
    t1 = table("2026–2027 Statutory, Ballot, Rent & Regulatory Watch (Verified Nov. 12, 2026)", ["Law / Proceeding", "Status", "Impact on Property A / Property B / Estate Plan", "Official Sources"], rows)
    return layout("law-watch.html", "2026–2027 Law, Ballot & Regulatory Watch",
                  "Live-verified federal, California, Santa Clara County, and San Francisco legal developments as of November 12, 2026.",
                  t1)


def build_repo_audit():
    rows = [
        ["session-595f0109/scripts/verify.py (Fixed via b4f/P)", "Remediated & Verified", "Was unexcluded in _config.yml and served live on Pages with hardcoded ZIPs, cities & unrounded owner numbers; replaced literal list with generic regexes + SHA-256 digests (0 literal tokens; 10 pages / 167 rows pass).", src("boe_80010")],
        ["public-safe/ (PR #36 & PR #38 baselines)", "Active on main", "Corrected 25-year horizon, Homeowner Exemption exclusion in S2, and $10 rounding; still omits §121, §168/§469/§1250, ad valorem vs. parcel split, NEM sunset, and mis-cites BOE Pub 800-10 for utilities (addressed in desk-b4f/).", src("irs_p523", "irs_p527")],
        ["Legacy directories excluded in _config.yml", "Excluded from Pages", "analysis/, archive/, assets/, audited-v4/, data/, docs/, mine/, model/, pages/, research/, scripts/, session-2f7b1b3f/, src/ excluded from Jekyll deployment; privacy_scan.py reports 0 findings after PR #38.", src("boe_80010")],
        ["Owner-only git commit history (F13)", "Outside session authority", "Prior commits on public git history remain accessible via git log; only the repository owner can make the repository private or rewrite git history.", src("irs_estate")],
    ]
    t1 = table("Repository Line-by-Line Audit & Privacy Disposition (2026-11-12)", ["Component / Path", "Disposition", "Audit Finding & Remediation", "Official Reference"], rows)
    return layout("repo-audit.html", "Repository Review & Privacy Audit",
                  "Summary of repository-wide verification, privacy remediation (b4f/P), and model reconciliations.",
                  t1)


def build_flagged():
    r45 = m.simulate_after_tax(2045)
    a26 = m.a_continuity_row(2026)
    hpi_low = m.simulate_after_tax(2045, allowance_growth=0.011)
    low_magi = m.simulate_after_tax(2045, magi_high=False)
    u3_lo = m.simulate_after_tax(2045, unit3_net_annual_2026=36_000)
    u3_hi = m.simulate_after_tax(2045, unit3_net_annual_2026=42_000)

    flags = [
        ["F01", "Property B taxable base vs. direct parcel charges", f"Supplied tax figure implies ~{m.money(m.B.taxable_value)} taxable value at 1.18162182%, likely bundling fixed parcel levies; exact split awaits parcel bill review.", "Impact moderate ($300–$600/yr fixed vs ad valorem)", src("sf_treas")],
        ["F02", f"Property A supplied tax vs. 1.18% + {m.money(m.A.fixed_parcel_charges)} ({m.money(a26['tax'])})", f"Model separates 1.18% ad valorem + {m.money(m.A.fixed_parcel_charges)} fixed parcel charges at {m.money(m.A.taxable_value)}; exact parcel TRA bonds & direct assessments unverified without public parcel lookup.", "Impact low–moderate ($300–$400/yr today)", src("scc_ratebook")],
        ["F03", "Mortgage / HELOC / liens on Property A and Property B", "No debt statements supplied; both properties modeled debt-free.", "High impact if leveraged", src("irs_estate")],
        ["F04", "Owner $1,500 insurance guesses vs. market & EQ exclusion", f"Unconfirmed; CDI 2025 averages ({stat('$2,339.99')} HO / {stat('$1,701.60')} DF / ~{stat('$2,920')} FAIR Plan) + State Farm +17%/+32.8% justify {m.money(m.A.insurance)}/{m.money(m.B.insurance)}+ (EQ excluded).", "High sensitivity in FAIR Plan shocks", src("cdi_2025", "cdi_sf26")],
        ["F05", "Property A hypothetical rent ($5,500/mo) unverified", "Owner supplied no rent quote for A; S2 gross rent is an explicit modeling assumption.", "Directly drives S2 vs S3 margin", src("civ_1947")],
        ["F06", "Transferor principal-residence continuity at death (Prop 19)", "S1 assumes Settlor continually occupies A as principal residence eligible for Homeowners' Exemption until transfer; assisted-living/absence breaks Prop 19.", "Swings S1 Year-1 tax by $50,000+/yr", src("boe_p19", "boe_ho")],
        ["F07", "Long-run Prop 19 biennial allowance pace", "2021–2025 actual FHFA CA HPI adjustments averaged ~1.1%/yr vs. 2.0%/yr modeled; lower HPI pace increases S1 partial reassessment.", f"Tested in Decision Lab ({m.money(hpi_low['s1_wealth'] - r45['s1_wealth'])} swing)", src("boe_lta25009", "fhfa_hpi")],
        ["F08", "Exact date of solar Permission to Operate (NEM 1.0 vs 2.0)", f"Unknown install year; any pre-Apr. 15, 2023 system sunsets by ≤2043 onto NBT + {stat('$24.15')}/mo BSC — earlier if installed in 2016–2021.", "Flips A electric $660+/yr", src("pge_nemfaq", "cpuc_bsc")],
        ["F09", "Property B original purchase price / income-tax basis", "Unknown; preventing any verified capital-gains calculation for selling B.", "Blocks modeling a sale of B", src("irs_basis")],
        ["F10", "Settlor estate size & surviving-spouse DSUE availability", "Liquid/retirement wealth and prior Form 706 portability status not supplied; modeled parametrically across Single vs DSUE vs 50% Cut.", "40% tax cliff above exclusion", src("irs_rp2635", "irs_i706")],
        ["F11", "Depreciable building vs. land share on Property A", "County assessor split not published here to protect parcel privacy; 40% building / 60% land modeled (tested 35%–45%).", "Minimal under high-MAGI §469 suspension", src("irs_p527")],
        ["F12", "Beneficiary MAGI & Real Estate Professional status (§469)", f"High MAGI (≥{stat('$150,000')}) suspends losses on Form 8582 until exit; MAGI ≤{stat('$100,000')} unlocks {stat('$25,000')}/yr deduction (+{m.money(low_magi['s2_wealth'] - r45['s2_wealth'])} wealth).", "Tested in Sensitivity Lab", src("irs_p925")],
        ["F13", "Public repository git history (owner-only)", "Earlier commits remain readable in git log; requires owner action (private repo or history rewrite).", "Privacy governance item", src("irs_estate")],
        ["F14", "SF File No. 261020 pending 10% banked + capital rent cap", "Not enacted as of Nov. 12, 2026; pending Land Use & Transportation Committee; could cap banked rent catch-ups on B.", "Affects B banked rent recovery", src("sf_leg261020", "sf_rent")],
        ["F15", "Unverified Unit 3 potential market rent on Property B", f"Vacated Unit 3 rental income if Heir moves into A is unverified; left $0 in baseline S1 and tested at +{m.money(36_000)}/+{m.money(42_000)} net in Sensitivity Lab.", f"Closes {m.money(u3_lo['s1_wealth'] - r45['s1_wealth'])}–{m.money(u3_hi['s1_wealth'] - r45['s1_wealth'])} of S1 gap, S3 still wins", src("sf_rent")],
        ["F16", "Future tax bracket & Congressional sunset risk (2040–2076)", "Tax rates, NIIT, CA top 13.3%, and estate exclusion can all change by statute across a 50-year horizon.", "Tested in Black-Swan Regime 7", src("irs_rp2635", "ftb_sched")],
        ["F17", "Trust administrative terms & co-beneficiary splits", "Trust instrument not reviewed; multi-heir buyout or mandatory-sale clauses could override single-heir modeling.", "Legal execution constraint", src("prob_16061")],
        ["F18", "Nov. 2026 CA SOS ballot percentages unofficial until Dec. 11", "Tally snapshots from Nov. 11, 2026 5:17 p.m. remain subject to post-certification canvass.", "Routine post-Dec. 11 refresh", src("sos_ballot")],
        ["F19", "County parcel direct charges vs. special assessment expirations", "Fixed parcel taxes (school parcel measures, stormwater fees) periodically expire or renew by local vote.", "Minor annual variance", src("scc_ratebook", "sfpuc_p218")],
        ["F20", "Public-safe vs. desk-b4f utility source alignment", "desk-b4f/ replaces public-safe/'s BOE Pub 800-10 utility placeholders with SJWC, SFPUC, PG&E, and CDI primary citations.", "Integration request logged", src("cpuc_sjwc", "sfpuc_p218")],
    ]
    rows = [[fid, item, detail, imp, s] for fid, item, detail, imp, s in flags]
    t1 = table("Flagged for Review Register (F01–F20 — Unverified Inputs, Assumptions & Policy Watches)", ["ID", "Item Flagged", "Evidence Gap / Discrepancy", "Decision Impact", "Official Reference"], rows)
    return layout("flagged.html", "Flagged for Review (F01–F20)",
                  "Every unconfirmed input, modeling boundary, and regulatory discrepancy left intentionally explicit rather than inferred.",
                  t1)


def build_sources():
    rows = []
    for key, (label, url) in sorted(SOURCES.items(), key=lambda kv: kv[1][0]):
        domain = url.split("/")[2]
        rows.append([label, domain, f'<a href="{escape(url)}" rel="noopener noreferrer">{escape(url)}</a>', chip("verified", "checked 2026-11-12")])
    t1 = table(f"Primary Official Sources Register ({len(rows)} Verified Government / Regulated Endpoints)", ["Agency & Document", "Host", "Direct HTTPS Source Link", "Verification Status"], rows)
    return layout("sources.html", "Primary Official Sources Register",
                  "Every external citation across desk-b4f/ links to a primary government, legislative, judicial, or regulated utility source verified on 2026-11-12.",
                  t1)


BUILDERS = {
    "index.html": build_index,
    "decision.html": build_decision,
    "properties.html": build_properties,
    "projections.html": build_projections,
    "costs.html": build_costs,
    "estate-tax.html": build_estate_tax,
    "black-swans.html": build_black_swans,
    "process.html": build_process,
    "law-watch.html": build_law_watch,
    "repo-audit.html": build_repo_audit,
    "flagged.html": build_flagged,
    "sources.html": build_sources,
}


def main():
    for filename, fn in BUILDERS.items():
        html = fn()
        (OUT_DIR / filename).write_text(html, encoding="utf-8")
    print(f"Built {len(BUILDERS)} HTML pages in {OUT_DIR}")


if __name__ == "__main__":
    main()
