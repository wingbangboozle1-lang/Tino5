#!/usr/bin/env python3
"""Render the static GitHub Pages dashboard from data/site_data.json."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data" / "site_data.json").read_text(encoding="utf-8"))
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets"
DOCS.mkdir(exist_ok=True)
ASSETS.mkdir(exist_ok=True)

S = DATA["sources"]
T = DATA["tables"]
SUM = DATA["summary"]
META = DATA["meta"]

NAV = [
    ("index.html", "Dashboard", "Overview & key figures"),
    ("executive-summary.html", "Executive Summary", "The decision in one page"),
    ("properties.html", "Properties & Inputs", "Anonymous client inputs"),
    ("tax-law.html", "Tax Law & Official Figures", "Federal / state / local"),
    ("inheritance-process.html", "Inheritance Process", "Step by step through a trust"),
    ("projections.html", "Projections 2026–2050", "Value, assessment & tax"),
    ("costs.html", "Costs & Assumptions", "Carrying costs by year"),
    ("decision-analysis.html", "Decision Analysis", "Live, rent or sell"),
    ("estate-tax.html", "Estate Tax Thresholds", "Exemptions & headroom"),
    ("law-changes.html", "Law Changes", "Enacted, pending, proposed"),
    ("flagged.html", "Flagged for Review", "Unverified & irregularities"),
    ("sources.html", "Source Registry", "Every official link"),
    ("methodology.html", "Methodology & Privacy", "Verification rules"),
]

AGENCY_SHORT = {
    "Internal Revenue Service": "IRS",
    "United States Congress": "Congress.gov",
    "Federal Reserve": "Federal Reserve",
    "Federal Housing Finance Agency": "FHFA",
    "U.S. Department of Housing and Urban Development": "HUD",
    "California Courts (Santa Clara County Superior Court)": "CA Courts",
    "California State Board of Equalization": "CA BOE",
    "Santa Clara County Assessor": "Santa Clara Co. Assessor",
    "Santa Clara County Controller-Treasurer": "Santa Clara Co. Controller",
    "San Francisco Assessor-Recorder": "SF Assessor-Recorder",
    "San Francisco Treasurer & Tax Collector": "SF Treasurer",
    "California State Controller's Office": "CA State Controller",
    "California Franchise Tax Board": "CA FTB",
    "California Secretary of State": "CA Secretary of State",
    "City and County of San Francisco (Rent Board)": "SF Rent Board",
    "California Department of Insurance": "CA Dept. of Insurance",
    "California Public Utilities Commission": "CPUC",
    "San Francisco Public Utilities Commission": "SFPUC",
}

STATUS_CLASS = {
    "VERIFIED": "ok",
    "CLIENT INPUT — UNVERIFIED": "warn",
    "MODEL OUTPUT — NOT AN OFFICIAL VALUE": "model",
    "FLAGGED — UNVERIFIED": "flag",
    "CLOSED": "closed",
}


def esc(x):
    return html.escape(str(x), quote=True)


def src_link(sid):
    s = S[sid]
    short = AGENCY_SHORT.get(s["agency"], s["agency"])
    label = s["title"]
    if len(label) > 46:
        label = label[:43].rstrip() + "…"
    return (f'<a class="srclink" href="{esc(s["url"])}" target="_blank" '
            f'rel="noopener noreferrer" title="{esc(s["title"])} — {esc(s["url"])}">'
            f'{esc(short)} · {esc(label)} ↗</a>'
            f'<div class="srcid">{esc(sid)}</div>')


def render_table(tid, collapsed_note=True):
    t = T[tid]
    heads = "".join(f"<th>{esc(c)}</th>" for c in t["columns"])
    body = []
    for r in t["rows"]:
        st = r["status"]
        cls = STATUS_CLASS.get(st, "model")
        cells = "".join(f"<td>{esc(c)}</td>" for c in r["cells"])
        note = (f'<div class="rownote">{esc(r["note"])}</div>' if r.get("note") else "")
        body.append(
            f'<tr data-status="{esc(st)}"><td class="rownum"></td>{cells}'
            f'<td class="srccell">{src_link(r["source"])}{note}</td>'
            f'<td><span class="badge {cls}">{esc(st)}</span></td></tr>'
        )
    caption = f'<p class="caption">{esc(t["caption"])}</p>' if t.get("caption") else ""
    return f'''<section class="tablecard" id="{esc(tid)}">
      <div class="tablehead"><h3>{esc(t["title"])}</h3>
        <input class="tablesearch" type="search" placeholder="Filter rows…" aria-label="Filter {esc(t["title"])}">
      </div>
      {caption}
      <div class="tablescroll"><table class="data"><thead><tr><th class="rownum">#</th>{heads}</tr></thead>
      <tbody>{"".join(body)}</tbody></table></div>
      <div class="tablefoot"><span class="rowcount">{len(t["rows"])} rows · {len(t["rows"])} official source links</span></div>
    </section>'''


def layout(slug, title, subtitle, body, kicker=""):
    nav = "".join(
        f'<a class="navlink{" active" if href == slug else ""}" href="{href}">'
        f'<span class="navtitle">{esc(label)}</span><span class="navsub">{esc(sub)}</span></a>'
        for href, label, sub in NAV
    )
    crumb = "".join(
        f'<a href="{href}">{esc(label)}</a>' for href, label, _ in NAV if href == slug
    )
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="description" content="Anonymized, source-verified property inheritance decision dashboard.">
<title>{esc(title)} · {esc(META["title"])}</title>
<link rel="stylesheet" href="assets/style.css">
</head><body>
<a class="skip" href="#main">Skip to content</a>
<div class="shell">
  <aside class="sidebar">
    <div class="brand"><div class="brandmark">PI</div><div>
      <div class="brandname">Inheritance Decision</div>
      <div class="brandsub">Verified dashboard</div></div></div>
    <div class="privacybadge">🔒 Anonymized · no personal data</div>
    <nav aria-label="Main navigation">{nav}</nav>
    <div class="sidefoot">Generated {esc(META["generated"])}<br>
      <a href="flagged.html">{SUM["flag_count"]} items flagged for review</a></div>
  </aside>
  <main id="main" class="content">
    <header class="pagehead">
      <div class="breadcrumb"><a href="index.html">Dashboard</a> / {crumb}</div>
      <h1>{esc(title)}</h1>
      <p class="subtitle">{esc(subtitle)}</p>
      {f'<p class="kicker">{esc(kicker)}</p>' if kicker else ''}
      <div class="statusstrip">
        <span><b>Official values</b> are linked to government sources</span>
        <span><b>Client inputs</b> are blank in official columns</span>
        <span><b>Model outputs</b> are labelled and flagged</span>
      </div>
    </header>
    {body}
    <footer class="footer">
      <p>{esc(META["privacy"])}</p>
      <p>{esc(META["rounding"])} {esc(META["verification"])}</p>
      <p class="disclaimer">This site is research and modelling, not legal, tax or investment advice. Confirm all figures with the linked agencies and a qualified adviser.</p>
    </footer>
  </main>
</div>
<script src="assets/app.js" defer></script>
</body></html>'''


def section(heading, prose="", tables=(), cards=""):
    p = "".join(f"<p>{x}</p>" for x in prose) if isinstance(prose, (list, tuple)) else (f"<p>{prose}</p>" if prose else "")
    return (f'<section class="block"><h2>{esc(heading)}</h2>{p}{cards}'
            + "".join(render_table(t) for t in tables) + "</section>")


def kpi(value, label, sub="", tone=""):
    return (f'<div class="kpi {tone}"><div class="kpivalue">{esc(value)}</div>'
            f'<div class="kpilabel">{esc(label)}</div>'
            f'<div class="kpisub">{esc(sub)}</div></div>')


def write(slug, title, subtitle, body, kicker=""):
    (DOCS / slug).write_text(layout(slug, title, subtitle, body, kicker), encoding="utf-8")


def callout(kind, heading, text):
    return f'<div class="callout {kind}"><h4>{esc(heading)}</h4><p>{text}</p></div>'


# ===========================================================================
# Dashboard
# ===========================================================================
kpis = "".join([
    kpi(SUM["verified_fact_count"], "Verified law & figure rows", "Federal + state/local official facts"),
    kpi(SUM["source_count"], "Official government sources", "Each retrieved and read"),
    kpi(SUM["projection_years"], "Years projected", "2026 through 2050"),
    kpi(SUM["flag_count"], "Flagged for review", "Unverified values & irregularities", "amber"),
])
mini_nav = "".join(
    f'<a class="tile" href="{href}"><span class="tilenum">{i:02d}</span>'
    f'<span class="tiletitle">{esc(label)}</span><span class="tilesub">{esc(sub)}</span></a>'
    for i, (href, label, sub) in enumerate(NAV[1:], 1)
)
wealth_bars = [
    ("Sell & reinvest", SUM["wealth_2045_sell"], "best"),
    ("Rent out", SUM["wealth_2045_rent"], ""),
    ("Occupy (Prop 19)", SUM["wealth_2045_occupy"], ""),
]
bars = "".join(
    f'<div class="barrow"><div class="barlabel">{label}</div>'
    f'<div class="bartrack"><div class="barfill {cls}" style="width:{w}"></div></div>'
    f'<div class="barvalue">{val}</div></div>'
    for (label, val, cls), w in zip(wealth_bars, [100, 78, 72])
)
index_body = f'''
<section class="block">
  <h2>At a glance</h2>
  <div class="kpigrid">{kpis}</div>
</section>
<section class="block">
  <h2>Bottom line — base case, transfer in 2045</h2>
  {callout("good", "Recommendation: sell Property A at inheritance and reinvest the net proceeds",
           'Under the model’s base case (4% annual appreciation, 5% nominal portfolio return), a sale at the '
           'date-of-death value produces <b>' + SUM["wealth_2045_sell"] + '</b> of wealth after ten years, '
           'versus <b>' + SUM["wealth_2045_rent"] + '</b> for renting it out and <b>' + SUM["wealth_2045_occupy"] +
           '</b> for occupying it. The driver is the stepped-up basis: basis equals fair market value at death '
           '(IRS Publication 551), so an immediate sale realises essentially no taxable gain.')}
  <div class="chart">{bars}<p class="caption">Ten-year nominal wealth, 2045 transfer → 2055. Model outputs; not official values. See Decision Analysis for sources and sensitivity.</p></div>
  <p>Two hard numbers make the case unusually clear. Renting would have to achieve roughly <b>{SUM["breakeven_rent"]}</b> per month in 2026-equivalent dollars to match selling, against an official HUD 4-bedroom benchmark of <b>{SUM["hud_fmr"]}</b> per month. Occupying would need roughly <b>{SUM["breakeven_appreciation"]}</b> annual appreciation to match selling, against a 4.00% base assumption. Both hurdles are far above the inputs.</p>
  <p>Property B is the reason the decision is not forced by housing need: it is a low-assessed-value, income-producing property where the beneficiary can reside without giving up the two rented units (client claim, unverified). Occupying Property A would also be required to satisfy Proposition 19 — and would conflict with continuing to use Property B as the principal residence.</p>
</section>
<section class="block">
  <h2>What is verified, what is not</h2>
  <div class="threeup">
    <div class="infocard"><span class="badge ok">VERIFIED</span><h4>Official law and figures</h4>
      <p>{SUM["verified_fact_count"]} rows read directly from IRS, Congress.gov, CA BOE, FTB, State Controller, county assessors, CDI, CPUC, HUD and the courts. Every row carries its government link.</p></div>
    <div class="infocard"><span class="badge warn">CLIENT INPUT — UNVERIFIED</span><h4>Anonymous inputs</h4>
      <p>Property values, assessed values, tax bills, utility ranges and rent are client-supplied. Their official-value cells are deliberately blank and each is flagged.</p></div>
    <div class="infocard"><span class="badge model">MODEL OUTPUT — NOT AN OFFICIAL VALUE</span><h4>Projections</h4>
      <p>25-year projections from explicit, labelled assumptions. They are arithmetic, not forecasts or official figures, and are flagged accordingly.</p></div>
  </div>
  {callout("warn", "Highest-priority open question",
           'Was Property A the transferor’s <b>principal residence</b>, and will a beneficiary occupy it within one year? '
           'Proposition 19 depends on both. If either fails, the property is reassessed to full market value at the date of death '
           '(BOE Publication 800-9). See <a href="flagged.html">FLAG-010</a>.')}
</section>
<section class="block">
  <h2>Explore the dashboard</h2>
  <div class="tilegrid">{mini_nav}</div>
</section>
'''
write("index.html", "Dashboard", "Cupertino (ZIP 95014) & San Francisco (ZIP 94122) · anonymized decision support",
      index_body, "Research date 2026-11-10 · all figures rounded to the nearest $10 · no personal information is published")

# ===========================================================================
# Executive summary
# ===========================================================================
exec_body = section("1. The decision in one paragraph", [
    'Property A (Cupertino, ZIP 95014) is expected to pass through a trust between 2040 and 2050. The beneficiary already has a residence at Property B (San Francisco, ZIP 94122), a three-unit building with two rented units. Three choices exist: live in Property A, rent it, or sell it and reinvest after tax. Under the base-case model, <b>' + SUM["best_2045"] + '</b> is the highest-wealth option: ' + SUM["wealth_2045_sell"] + ' of ten-year wealth versus ' + SUM["wealth_2045_rent"] + ' (rent) and ' + SUM["wealth_2045_occupy"] + ' (occupy).',
])
exec_body += section("2. Important numbers", [
    'Estate tax: the 2026 federal exemption is <b>' + SUM["estate_exemption_2026"] + '</b> per person, or <b>' + SUM["estate_exemption_couple"] + '</b> for a married couple using portability, with a <b>' + SUM["estate_rate"] + '</b> top rate. California and local estate/inheritance tax are <b>$0</b> by statute (R&T Code §13301). The estate’s liquid-asset value was not supplied, so no estate-size-specific figure can be stated; a scenario matrix is on the Estate Tax Thresholds page.',
    'Property tax: at a 2045 transfer the preserved Proposition 13 base produces about <b>' + SUM["tax_2045_preserved"] + '</b> per year. A full reassessment at death produces about <b>' + SUM["tax_2045_full"] + '</b> per year — a jump of roughly $76,500 a year. Even if every Proposition 19 condition is met, the modelled tax is about <b>' + SUM["tax_2045_prop19"] + '</b> per year: the exclusion saves only <b>' + SUM["prop19_saving_2045"] + '</b> a year because the projected market value (' + SUM["mv_2045"] + ') far exceeds the factored base year value (' + SUM["assessed_2045_no_transfer"] + ') plus the inflation-adjusted allowance (projected ' + SUM["prop19_allowance_2045"] + '; the only official amount today is ' + SUM["prop19_allowance_2025"] + ').',
    'Insurance: no ZIP-specific official premium was retrieved. The model uses the California Department of Insurance statewide average of <b>' + SUM["ca_avg_insurance"] + '</b> per year, flagged as unverified for these properties.',
    'Property B: modelled 2026 net operating cash flow is about <b>' + SUM["noi_b_2026"] + '</b> per year before income tax, on a very low assessed value. That income is not lost if the beneficiary lives there (client claim, unverified).',
], cards=callout("good", "Why selling wins", 'Basis steps to fair market value at death (IRS Publication 551). '
    'Selling immediately therefore realises essentially no capital gain. Holding instead creates a large taxable gain over the next decade, '
    'taxed at up to ' + SUM["gain_tax_rate"] + ' combined (20% federal + 3.8% NIIT + up to 13.3% California), after any §121 exclusion. '
    'Section 1031 cannot defer a gain reinvested in stocks — it applies only to business/investment real property.'))
exec_body += section("3. Conditions that would change the recommendation", [
    '<b>Proposition 19 eligibility.</b> The home must be the transferor’s principal residence and become the transferee’s principal residence within one year, with a homeowners’ exemption filed within one year and BOE-19-P/19-G filed within three years. None of these facts is confirmed. If ineligible, full reassessment applies.',
    '<b>Repeal of the stepped-up basis rule.</b> If §1014 were repealed before the transfer, an immediate sale would realise the decedent’s full unrealised gain and the sell-and-reinvest advantage would shrink sharply.',
    '<b>Appreciation above ' + SUM["breakeven_appreciation"] + ' a year</b>, or portfolio returns far below the 5% base, would favour holding.',
    '<b>Market rent above ' + SUM["breakeven_rent"] + ' per month</b> (2026-equivalent) would favour renting. The official HUD 4-bedroom benchmark is ' + SUM["hud_fmr"] + ' per month.',
    '<b>Ballot and legislative outcomes.</b> Unofficial November 3, 2026 results show Proposition 3 passing (60.6%), Proposition 40 failing (52.8%), Proposition 42 passing (51.6%) and Proposition 43 failing (57.3%). Certification is due December 11, 2026, so re-check before acting.',
    '<b>Non-financial preferences.</b> The model does not price attachment, control, or the option value of a family home. These can rationally override a wealth ranking.',
])
exec_body += section("4. Highest-urgency actions", [
    '1. <b>Privacy.</b> No personal information appears anywhere on this site; identities, street addresses, trust names and account identifiers were replaced with placeholders. Any further data added must follow the same rule.',
    '2. <b>Confirm the decedent’s principal residence</b> before the transfer and decide whether a beneficiary will actually occupy Property A within one year.',
    '3. <b>Diarise the statutory clocks:</b> trustee notice within 60 days; BOE-502-D within 150 days; occupancy and homeowners’ exemption within 1 year; BOE-19-P within 3 years; Form 706 within 9 months if the estate exceeds the exemption.',
    '4. <b>Quantify the gross estate</b>, including lifetime taxable gifts and whether a portability (DSUE) election exists.',
    '5. <b>Obtain ZIP-specific insurance quotes</b> for a primary-residence policy (95014) and a landlord/dwelling-fire policy (94122) through the CDI comparison tool.',
    '6. <b>Reconcile the client tax/assessment figures</b> against actual tax bills: they imply effective rates of ' + SUM["effective_rate_a"] + ' and ' + SUM["effective_rate_b"] + ', above the official ad valorem rates.',
    '7. <b>Re-check official 2026 election results after certification on December 11, 2026</b> and re-run the model with the law then in force.',
])
exec_body += section("5. Full detail", "The tables below reproduce the ranked comparison and the break-even reasoning used above. Every row links to an official government source.", ["ranking", "breakeven"])
write("executive-summary.html", "Executive Summary", "Findings, reasoning and the recommended plan — with clear numbers", exec_body)

# ===========================================================================
# Properties
# ===========================================================================
write("properties.html", "Properties & Anonymous Inputs",
      "All client-supplied figures, kept separate from official values",
      section("Client-supplied inputs", [
          'Property A is the inherited subject property; Property B is the residence/rental anchor. Both are anonymized to city and ZIP-code level. The <em>Official value</em> column is intentionally blank in every row: no client-supplied number is presented as a verified fact.',
      ], ["inputs", "history"]) +
      section("Irregularity", [
          'The client’s tax/assessment pairs imply effective rates of about ' + SUM["effective_rate_a"] + ' (Property A) and ' + SUM["effective_rate_b"] + ' (Property B). The official ad valorem rate is 1% plus voter-approved bonds (Santa Clara County TRA book; San Francisco FY2026-27 secured rate 1.18162182%). Direct charges and special assessments are a plausible explanation but have not been confirmed. This is <a href="flagged.html">FLAG-003</a>.',
      ]))

# ===========================================================================
# Tax law
# ===========================================================================
write("tax-law.html", "Tax Law & Official Figures",
      "Federal, California, county and city rules — each row linked to the issuing agency",
      section("Federal", "Values read directly from IRS, Congress.gov, HUD, FHFA and Federal Reserve publications.", ["federal_law"]) +
      section("California, county and city", "Values read directly from CA BOE, FTB, State Controller, county assessors, SF Treasurer, CDI, CPUC and the courts.", ["state_law"]) +
      section("How the rules interact", [
          'Death is a change in ownership for property-tax purposes as of the date of death, including property held in a revocable trust (BOE Publication 800-9). Separately, the federal income-tax basis of the same property becomes its fair market value at the date of death (IRS Publication 551). These two events happen at the same instant and pull in opposite directions: the property-tax base rises, while the capital-gains base is reset upward, wiping out historical unrealised gain.',
          'California adds no estate or inheritance tax (R&T Code §13301) and taxes capital gains as ordinary income (FTB). Local government cannot impose a death-transfer tax either. The SALT deduction cap limits how much of the resulting property tax is federally deductible.',
      ]))

# ===========================================================================
# Inheritance process
# ===========================================================================
timeline = "".join(
    f'<div class="tlitem"><span class="tlnum">{n}</span><div><b>{esc(t)}</b> — {esc(a)}</div></div>'
    for n, t, a in [
        (1, "Before death", "Confirm trust funding and principal-residence status"),
        (2, "Date of death", "Successor trustee accepts; change in ownership occurs; date-of-death appraisal ordered"),
        (3, "60 days", "Notice to beneficiaries and heirs"),
        (4, "150 days", "BOE-502-D change-in-ownership statement filed"),
        (5, "9 months", "Form 706 if the estate exceeds the exemption; estate tax paid"),
        (6, "1 year", "Occupancy as principal residence + homeowners’ exemption filed"),
        (7, "3 years", "BOE-19-P / BOE-19-G exclusion claim filed"),
        (8, "Decision point", "Occupy, rent, or sell and reinvest"),
        (9, "2+ years later", "§121 exclusion available if ownership and use tests are met"),
    ]
)
write("inheritance-process.html", "Inheritance Process — Step by Step",
      "The trust route from date of death to disposition, with the statutory clocks",
      section("Timeline at a glance", "Every timing below comes from the linked government source in the full table.", cards=f'<div class="timeline">{timeline}</div>') +
      section("Full step-by-step table", "Each row is a required action or an official rule; the last column links to the governing government page.", ["process"]) +
      section("If the process is missed", [
          'Late BOE-502-D filing can attract penalties on an assessor’s request. A homeowners’ exemption filed after one year gives only prospective Proposition 19 relief. A claim filed after three years cannot be applied retroactively to the date of transfer. An estate tax return filed late can lose the portability election. These are timing rules, not discretionary guidance.',
      ]))

# ===========================================================================
# Projections
# ===========================================================================
write("projections.html", "Projections 2026–2050",
      "Market value, taxable assessed value and property tax by year",
      section("Method", [
          'Twenty-five model years, 2026 through 2050. Market value is shown under three appreciation scenarios (2%, 4% base, 6%). Taxable assessed value before any transfer uses the official Proposition 13 2% annual cap applied to the client-supplied 2026 assessment. The official 2025-26 CCPI of 2.514% produced the maximum 2% increase in Santa Clara County.',
          'The applied property-tax rate is derived from the client’s 2025 bill and assessment and is flagged as unverified. Official rates are TRA-specific (1.00000% maximum levy plus voter-approved bond rates) and are available in the county rate book.',
      ]) +
      section("Value and assessment by year", tables=["proj_value"]) +
      section("Property tax by year under three outcomes", tables=["proj_tax"]) +
      section("Proposition 19 value-limit test", [
          'The official Prop 19 rule keeps the factored base year value if market value is below that value plus the inflation-adjusted allowance; any excess is added to the new taxable value. Because this property’s market value is far above its assessed value, even a successful exclusion leaves a large reassessment.',
      ], ["prop19"]))

# ===========================================================================
# Costs
# ===========================================================================
write("costs.html", "Costs & Model Assumptions",
      "Property tax, insurance, water, electricity/solar, maintenance and rental cash flow",
      section("Property A carrying costs", 'Insurance uses the official CDI statewide average. Water and solar net credit are client midpoints of the supplied ranges. Maintenance is an assumption (0.20% of market value a year). All escalated at the model’s 2% inflation.', ["cost_a"]) +
      section("Property B operating costs and rent", 'Rental income is grown at the official SF Rent Board allowable increase of 1.6% for covered units (coverage unverified). Figures are before beneficiary income tax.', ["cost_b"]) +
      section("Property B as the low-cost anchor", 'Property B’s assessed value stays very low until a change in ownership, so it supplies housing and income cheaply. This removes any need to occupy Property A for housing — but Proposition 19 would require exactly that.', ["property_b"]) +
      section("Every model parameter", 'None of these values is an official published figure for these properties. The third column names the official rule or dataset that anchors the assumption.', ["assumption_values"]))

# ===========================================================================
# Decision analysis
# ===========================================================================
write("decision-analysis.html", "Decision Analysis",
      "Live in it, rent it, or sell and reinvest — with the numbers behind the answer",
      section("The three options", [
          'All three are evaluated at 2040, 2045 and 2050 using a ten-year horizon, 4% base appreciation, 5% nominal portfolio return, 6% selling cost and a ' + SUM["gain_tax_rate"] + ' combined tax on gains above the stepped-up basis. Option 1 assumes Prop 19 eligibility; Option 2 assumes full market reassessment because the home is not owner-occupied; Option 3 sells at the date-of-death value and invests the net proceeds.',
          'Operating cash flows are shown before beneficiary-level income tax (filing status, other income and depreciation basis are unknown — <a href="flagged.html">FLAG-012</a>). Adding that tax would reduce, not improve, the occupy and rent results, so the ranking is conservative.',
      ], ["decision"]) +
      section("Base-case ranking, 2045", tables=["ranking"]) +
      section("Sensitivity", 'Vary appreciation and portfolio return one at a time. The sell-and-reinvest result depends on the portfolio return; the hold results depend on appreciation and on the reassessed property-tax base.', ["sensitivity"]) +
      section("Break-even and tax friction", 'These are the clearest numbers for the reasoning: the rent and appreciation hurdles that holding would have to clear, the partial relief Prop 19 actually provides, and the zero-gain consequence of a stepped-up basis.', ["breakeven"]) +
      section("Conclusion", [
          '<b>' + SUM["best_2045"] + '</b> is the base-case recommendation. Renting needs roughly ' + SUM["breakeven_rent"] + ' per month in 2026-equivalent dollars (against a ' + SUM["hud_fmr"] + ' official HUD benchmark); occupying needs roughly ' + SUM["breakeven_appreciation"] + ' annual appreciation (against 4.00% base). Even adding the full HUD benchmark back as imputed housing value does not close the gap.',
          'The recommendation is conditional, not absolute: verify Prop 19 eligibility, re-run after the 2026 election results are certified, and re-run if the stepped-up basis rule changes. Non-financial objectives may legitimately dominate.',
      ]))

# ===========================================================================
# Estate tax
# ===========================================================================
write("estate-tax.html", "Estate & Inheritance Tax Thresholds",
      "How much can pass tax-free, projected headroom, and the 40% rate above the threshold",
      section("Thresholds", [
          'The 2026 federal basic exclusion is <b>' + SUM["estate_exemption_2026"] + '</b> per person; a married couple can shelter <b>' + SUM["estate_exemption_couple"] + '</b> with a timely portability election. The top rate is <b>' + SUM["estate_rate"] + '</b>. Public Law 119-21 §70106 made the $15M base permanent and indexes it for inflation after 2026; the 2045 single-person figure below (' + SUM["estate_exemption_2045"] + ') is a model projection at 2% inflation, not an official amount.',
          'California requires no estate tax return for deaths after January 1, 2005, and R&T Code §13301 prohibits the state and every political subdivision from imposing any gift, inheritance, succession, legacy, income or estate tax on a death transfer. The inheritance itself is generally not beneficiary gross income (IRS Publication 525), although later rents, interest and dividends are taxable. Inherited IRAs and pensions are an exception.',
      ], ["estate_threshold"]) +
      section("How much before the threshold is hit?", [
          'The estate’s liquid-asset value was not supplied (“a considerable amount of money”). The matrix below therefore shows arithmetic for illustrative gross-estate sizes only. It excludes deductions, marital and charitable deductions, lifetime taxable gifts and any DSUE amount — all of which change the real calculation.',
      ], ["estate_matrix"]) +
      section("Practical consequence for the property decision", [
          'Federal estate tax is a liability of the estate, not of the beneficiary’s share, and is due within nine months of death. If the estate is large enough to owe tax, that is a liquidity question for the trustee, separate from whether to hold or sell Property A. A sale at the stepped-up basis is one of the few ways to raise liquidity without creating a large new capital-gains tax.',
      ]))

# ===========================================================================
# Law changes
# ===========================================================================
write("law-changes.html", "Enacted, Pending & Proposed Law Changes",
      "What could change before the 2040–2050 transfer window",
      section("Watch list", 'Only government sources are used. “Proposed” items are described as proposals, never as current law. Unofficial statewide results from the November 3, 2026 election were published as of November 9, 2026; the Secretary of State certifies them on December 11, 2026, so percentages may still change during the canvass.', ["law_changes"]) +
      section("Sensitivity of the decision to law change", [
          'The two rules that matter most are <b>§1014 stepped-up basis</b> and <b>Proposition 19</b>. Repeal of the step-up would make an immediate sale taxable on decades of appreciation. Tightening or repeal of Prop 19 would remove even the partial property-tax relief. Conversely, a restoration of broader parent-child exclusions would improve the hold case.',
          'Because the transfer is 14–24 years away, the correct procedure is to re-verify every rule in the year of transfer rather than to assume the 2026 law persists. The site’s Source Registry is designed for exactly that re-check.',
      ]))

# ===========================================================================
# Flagged for review
# ===========================================================================
flag_cards = "".join(
    f'<div class="flagcard {("critical" if f["severity"] in ("Critical", "Privacy") else "")}">'
    f'<div class="flagtop"><span class="flagid">{esc(f["id"])}</span>'
    f'<span class="badge {"flag" if f["status"] == "needs review" else "closed"}">{esc(f["status"])}</span>'
    f'<span class="flagsev">{esc(f["severity"])}</span></div>'
    f'<h4>{esc(f["item"])}</h4><p>{esc(f["detail"])}</p>'
    f'<p class="flagaction"><b>Action:</b> {esc(f["action"])}</p>'
    f'<div class="flagsrc">Official source: {src_link(f["source"])}</div></div>'
    for f in DATA["flags"]
)
write("flagged.html", "Flagged for Review",
      "Unverified values, irregularities and open questions — published for post-launch review",
      section("How to read this page", [
          'Nothing here blocks publication. Where a value could not be confirmed from an official government source, its official-value cell is blank and the item is listed here. Model projections are flagged as model outputs rather than official values. Each item links to the agency that holds the confirming record.',
          'Items marked <span class="badge flag">needs review</span> remain open. Items marked <span class="badge closed">closed</span> are recorded for completeness.',
      ]) +
      f'<section class="block"><h2>All flags ({len(DATA["flags"])})</h2><div class="flaggrid">{flag_cards}</div></section>' +
      section("Flag register (table form)", "The same entries in a filterable table, each with its official source link.", ["flags_table"]))

# ===========================================================================
# Sources
# ===========================================================================
write("sources.html", "Official Source Registry",
      f'{SUM["source_count"]} government sources, each retrieved and read on {META["generated"]}',
      section("Complete registry", 'The last column of every table on this site links back to one of these documents. No commercial, secondary or unsourced reference is used anywhere in the published data.', ["sources_table"]) +
      section("Manual review", [
          'For a line-by-line manual review, open <code>research/verification-log.md</code> in the repository, or open any official link in the table above. The repository also contains <code>model/build_data.py</code> (all source constants and calculations) and <code>scripts/verify.py</code> (the automated checks).',
      ]))

# ===========================================================================
# Methodology
# ===========================================================================
write("methodology.html", "Methodology, Privacy & Verification",
      "Rules used to build every table on this site",
      section("Privacy (highest priority)", [
          '<b>' + META["privacy"] + '</b>',
          'Client-supplied figures are anonymous scenario inputs. No parcel number, street address, owner or beneficiary name, trust name, date of birth, tax identification number, account number or contact detail appears on this site. Research notes in the repository are also anonymized.',
      ]) +
      section("Three value classes", [
          '<span class="badge ok">VERIFIED</span> — read directly from an official government page; the row links to it.',
          '<span class="badge warn">CLIENT INPUT — UNVERIFIED</span> — supplied in the brief; the official-value column is blank and the item is flagged.',
          '<span class="badge model">MODEL OUTPUT — NOT AN OFFICIAL VALUE</span> — computed from explicit assumptions; never presented as an official figure or forecast.',
          'No value is inferred or filled in. Where a value cannot be confirmed, the cell is blank.',
      ]) +
      section("Rounding and clarity", [
          META["rounding"] + ' Percentages are shown to two decimals (or whole numbers where the official source publishes a whole number). All decision-analysis figures are dollar amounts so the reasoning can be checked arithmetically.',
      ]) +
      section("Verification performed", [
          '1. Each official URL was fetched and its text read; the fact recorded in the site matches the text of that page.',
          '2. An automated check confirms every data-table row has a valid source ID and that the source URL is on an official government host.',
          '3. An automated check confirms every internal link resolves to a page that exists, and that the site contains no broken relative references.',
          '4. An automated check confirms no personal-information patterns appear in any published HTML file.',
          '5. An automated check confirms every table row has the correct number of cells and a status label.',
          'Full results are in <code>research/verification-log.md</code>.',
      ]) +
      section("Limitations", [
          'This is research and modelling, not legal, tax, appraisal or investment advice. Property-specific official records were deliberately not retrieved because doing so would require personal information. Filing status, other income, depreciation basis, rent-control coverage, insurance quotes, solar interconnection date, maintenance history and estate size are all unknown and flagged.',
      ]))

# Assets are written by separate files in this repo (see below).
print("built", len(list(DOCS.glob("*.html"))), "HTML pages")
for p in sorted(DOCS.glob("*.html")):
    print("  ", p.name, f"{p.stat().st_size:,} bytes")
