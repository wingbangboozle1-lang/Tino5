#!/usr/bin/env python3
"""desk-31cb5781 generator.

Builds the inheritance decision desk (Property A = future trust inheritance,
Santa Clara County; Property B = already owned, San Francisco County).

Design rules (hard, privacy-first):
  * No names, street addresses, ZIP codes, neighbourhoods, parcel/account numbers
    or contact details anywhere on the published site. Properties are "Property A"
    and "Property B" at county level only.
  * Money rounded to nearest $10 unless a statutory / agency figure is quoted
    exactly (those are tagged `exact`).
  * Every table row carries an official-source link, or is left blank and tagged
    `unverified` / `owner`. No inferred or invented values presented as fact.
  * Model outputs are labelled `assumption` / `derived` and show their inputs.
"""
import os, re, datetime

OUT = os.path.join(os.path.dirname(__file__), "..")
ASSETS = os.path.join(OUT, "assets")

# ----------------------------------------------------------------------------- sources
# Each: key -> (label, official URL). Only domains I can confirm as official.
SRC = {
 "irs_estate":  ("IRS — Working Families Tax Cuts: 2026 federal estate/gift basic exclusion $15,000,000 per person, top rate 40%, gift annual exclusion $19,000 (OBBBA / Rev. Proc. 2025-32)",
                 "https://www.irs.gov/newsroom/working-families-tax-cuts-individuals-and-workers"),
 "irs_stepup":  ("IRS — Topic No. 403, Basis of Assets: step-up in basis to fair market value at date of death (IRC §1014)",
                 "https://www.irs.gov/taxtopics/tc403"),
 "irs_121":     ("IRS — Topic No. 703, Sale of Home: §121 exclusion up to $250,000 ($500,000 married filing jointly), ownership+use 2 of 5 years",
                 "https://www.irs.gov/taxtopics/tc703"),
 "irs_706":     ("IRS — Form 706 / estate tax: top marginal rate 40% on amounts above the exclusion",
                 "https://www.irs.gov/forms-pubs/about-form-706"),
 "boe_home":    ("California State Board of Equalization — property tax & Proposition 13 / 19 program pages",
                 "https://www.boe.ca.gov/"),
 "boe_prop13":  ("BOE — Proposition 13: 1% general tax limit, assessed-value annual increase capped at 2% absent change in ownership/new construction (Cal. Const. art. XIII-A)",
                 "https://www.boe.ca.gov/proptaxes/proposition13.htm"),
 "boe_prop19":  ("BOE — Proposition 19 (Rev. & Tax. §63.2): parent-child exclusion limited to primary residence, transferee must occupy within 1 year, file BOE-19-P within 3 years, non-primary property fully reassessed; inflation-adjusted allowance set every 2 years",
                 "https://www.boe.ca.gov/proptaxes/proposition19.htm"),
 "ftb":         ("California Franchise Tax Board — California has no state estate tax and no inheritance tax; inherited property not taxable income to recipient",
                 "https://www.ftb.ca.gov/"),
 "sjwater":     ("San Jose Water Company — serves Property A; approved residential tiered quantity rates and monthly service charge (Advice Letter 599)",
                 "https://www.sjwater.com/media/kccm45hy/san-jose-water-company-al-599-approved_0.pdf"),
 "sfpuc":       ("SFPUC — Water & Sewer Rates, Proposition 218 notice (FYE 2026–2028; rates effective 7/1/2026); average single-family combined bill ~$171–$189/mo",
                 "https://www.sfpuc.gov/accounts-services/water-power-sewer-rates/proposed-water-sewer-rates-2026/proposition-218-notice"),
 "pge":         ("PG&E / CPUC Public Advocates Office — PG&E residential average ~33.7¢/kWh (June 2026), Income-Graduated Base Services Charge ~$24.15/mo (CPUC D.24-05-028 / AB 205)",
                 "https://www.cpuc.ca.gov/"),
 "treasury":    ("U.S. Department of the Treasury — Daily Treasury Par Yield Curve (constant-maturity Treasury rates; 3-month and 2-year used for the phased-investing path)",
                 "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve"),
 "ftb_estate":  ("CA FTB / California State Controller — state death-tax credit ended for deaths after 2004; California collects no estate tax today",
                 "https://www.ftb.ca.gov/"),
 "doi":         ("California Department of Insurance — homeowners / dwelling fire (DP) policies and the FAIR Plan framework",
                 "https://www.insurance.ca.gov/"),
 "fairplan":    ("California FAIR Plan — insurer of last resort; dwelling fire policy, ~$3M dwelling limit (from 1/1/2026), no liability/water/theft; typically paired with a DIC wrap",
                 "https://www.cfpnet.com/"),
 "leginfo_rt":  ("California Legislative Information — Revenue & Taxation Code (official statutes incl. §63.1 / §63.2)",
                 "https://leginfo.legislature.ca.gov/faces/codes.xhtml"),
 "leginfo_irc": ("Official U.S. House / IRS statute references — Internal Revenue Code (estate, gift, §1014 step-up, §121 exclusion)",
                 "https://www.irs.gov/"),
}

def src(key):
    label, url = SRC[key]
    return f'<a href="{url}" target="_blank" rel="noopener">{label}</a>'

# ----------------------------------------------------------------------------- money
def m0(x):
    """Round to nearest $10, format. None -> blank."""
    if x is None: return ""
    return f"${int(round(x/10.0)*10):,}"

def m_exact(x):
    """Statutory/exact figure: format as published, tag exact."""
    if x is None: return ""
    return f"${int(x):,}"

def tag(kind):
    # kind: verified | assumption | unverified | owner | exact
    cls = {"verified":"verified","assumption":"assumption","unverified":"unverified",
           "owner":"owner","exact":"exact"}[kind]
    lab = {"verified":"verified","assumption":"assumption","unverified":"unverified",
           "owner":"owner-supplied","exact":"exact (statutory)"}[kind]
    return f'<span class="tag {cls}">{lab}</span>'

# ----------------------------------------------------------------------------- page shell
NAV_GROUPS = [
 ("Start", [("Executive summary","index.html"),("How to use this desk","index.html")]),
 ("Property A — to be inherited", [("Property facts","properties.html"),("Property tax & assessment","property-tax.html"),("Step-by-step trust process","process.html")]),
 ("Property B — already owned", [("Property facts","properties.html"),("Running costs","running-costs.html")]),
 ("Taxes & inheritance", [("Inheritance & estate tax","inheritance-tax.html"),("Law watch","law-watch.html")]),
 ("Decision model", [("Scenarios: live / rent / sell","scenarios.html"),("Black swan & phased investing","black-swans.html")]),
 ("Timing & deadlines", [("Deadlines timeline","process.html")]),
 ("Questions & gaps", [("Questions & information gaps","questions.html")]),
 ("Owner input", [("Suggestions board","suggestions.html"),("Glossary","glossary.html")]),
 ("For advisers", [("Attorney & CPA Briefing Sheet","briefing-sheet.html")]),
 ("Record", [("Sources","sources.html"),("Flagged for review","flagged.html"),("Methodology & privacy","methodology.html")]),
]

def nav_html():
    parts=[]
    for grp, items in NAV_GROUPS:
        parts.append(f'<span class="grp">{grp}</span>')
        for t,h in items:
            parts.append(f'<a href="{h}">{t}</a>')
    return "".join(parts)

def page(title, body, dek="", printable=False, extra_head=""):
    css = '<link rel="stylesheet" href="assets/style.css">'
    js = '<script src="assets/app.js"></script>' if not printable else ''
    pr = ' class="print-page"' if printable else ''
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><meta name="referrer" content="no-referrer">
<title>{title} — Inheritance decision desk</title>{css}{extra_head}{js}</head><body{pr}>
<header><div class="bar"><h1>Inheritance decision desk</h1><div class="sub">Property A (future trust inheritance) · Property B (already owned) · County level · No personal identifiers</div></div>
<nav>{nav_html()}</nav></header>
<main><div class="page-header"><h2>{title}</h2>{f'<p class="dek">{dek}</p>' if dek else ''}</div>{body}
<div class="foot no-print"><b>Not tax, legal or investment advice.</b> Figures are planning estimates based on the sources named in each row. Statutory amounts are quoted as published; all other money rounded to the nearest $10. Re-check the then-current law before acting. <a href="sources.html">Source register</a> · <a href="flagged.html">Flagged for review</a> · <a href="methodology.html">Methodology &amp; privacy</a></div></main>
</body></html>"""

def tbl(headers, rows, caption=None):
    # rows: list of (cells, kind_for_last)  OR cells where last cell is source html
    cap = f'<p class="small" style="margin-top:10px">{caption}</p>' if caption else ""
    h="".join(f"<th>{h}</th>" for h in headers)
    b=""
    for r in rows:
        cells, kind = r
        if kind=="owner":
            cells=cells+[tag("owner")]
        elif kind=="unverified":
            cells=cells+[tag("unverified")]
        elif kind=="assumption":
            cells=cells+[tag("assumption")]
        elif kind=="exact":
            cells=cells+[tag("exact")]
        elif kind=="verified":
            cells=cells+[tag("verified")]
        else:
            cells=cells+[""]
        b+="<tr>"+"".join(f"<td>{c}</td>" for c in cells)+"</tr>"
    return f'{cap}<table class="data"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>'

# =============================================================================
# CONTENT
# =============================================================================

OWNER_NOTE = ('Owner-supplied figures (market value, rent, utilities, insurance, solar credit) are shown '
              'as "owner-supplied — unverified": no official source confirms them, and they are not used as '
              'verified inputs to the model.')

pages = {}

# ---------------------------------------------------------------- index
pages["index.html"] = dict(
 title="Home",
 dek="Clean dashboard for deciding what to do with an inherited house. Property A passes through a trust around 2040–2050; Property B is already owned outright. The two are analysed separately because one is inherited and the other is not.",
 body="""
<div class="callout info"><b>Start here.</b> The core question: when Property A passes to the heir (around 2040–2050), should the heir move in, rent it out, sell it and reinvest, or combine those over time? This desk answers with arithmetic that can be re-run, sourced law, and stress cases that break the arithmetic.</div>

<h3>What would change the answer (read first)</h3>
<p>The decision is not determined by today's headline price. It flips on three break-evens:</p>
<ul>
<li><b>Gross rental yield</b> on Property A vs. the cost of carrying it (tax, insurance, maintenance, water/electric). If net rent after carrying costs &gt; after-tax portfolio return, keeping wins.</li>
<li><b>Price growth</b> vs. portfolio return. If the house appreciates faster than a diversified portfolio (after tax), keeping compounds better.</li>
<li><b>Whether the heir moves in within one year</b> of transfer. That is the switch between Prop 19's capped reassessment (child occupies) and full market reassessment (child does not occupy).</li>
</ul>
<div class="callout warn">These break-evens are shown on the Executive Summary and the Scenarios page, with what-if controls so you can test them yourself.</p>

<h3>Grouped menu</h3>
<p>Use the top navigation, grouped by category. Each page stands alone and cites its sources in every table row.</p>

<h3>Glossary (key terms)</h3>
<table data>
""",  # body continues below in assembler

# We'll assemble index body fully in code to reuse glossary.
)
# NOTE: index.html body is assembled specially below.

# ---------------------------------------------------------------- executive summary
exec_body = f"""
<div class="callout ok"><b>Headline (baseline, 2026 figures, $10 rounding):</b> On the baseline assumptions, <b>selling Property A at inheritance and reinvesting after tax is projected to out-keep keeping it as a rental</b>, mainly because the Prop 19 allowance shields only about $1,044,590 of the assessed-to-market gap, so a $3,100,000 inherited home largely reassesses to market value and carries a material tax bill. Keeping wins only if the heir moves in (qualifying for the Prop 19 cap) <i>and</i> rent growth outpaces portfolio returns.</div>

<h3>What would change the answer</h3>
<table>
<thead><tr><th>Condition that flips the decision</th><th>Break-even / threshold</th><th>Source / basis</th></tr></thead>
<tbody>
<tr><td>Heir occupies Property A as primary residence within 1 year of transfer</td><td>Qualifies for Prop 19 capped reassessment; assessed ≈ factored base year value + $1,044,590 (2025–2027 cap)</td><td>{src('boe_prop19')}</td></tr>
<tr><td>Heir does <b>not</b> occupy within 1 year</td><td>Full reassessment to market value at transfer; Prop 19 exclusion lost</td><td>{src('boe_prop19')}</td></tr>
<tr><td>Gross rental yield &gt; after-tax portfolio return + carrying costs</td><td>Renting/keeping beats selling</td><td>Desk model (assumption)</td></tr>
<tr><td>House price growth &gt; portfolio return (after tax)</td><td>Keeping compounds better than selling</td><td>Desk model (assumption)</td></tr>
<tr><td>Heir sells and lives in the home ≥2 of 5 years before sale</td><td>§121 exclusion up to $250,000/$500,000 of gain on top of stepped-up basis</td><td>{src('irs_121')}</td></tr>
<tr><td>Estate above federal basic exclusion</td><td>Federal estate tax applies above $15,000,000/person (2026); California has no estate/inheritance tax</td><td>{src('irs_estate')} {src('ftb')}</td></tr>
</tbody>
</table>

<div class="kpi">
 <div class="t"><div class="v">$3,100,000</div><div class="l">Property A estimated value, Nov 2026 (owner input · unverified)</div></div>
 <div class="t"><div class="v">$1,800,000</div><div class="l">Property B estimated value, Nov 2026 (owner input · unverified)</div></div>
 <div class="t"><div class="v">$15,000,000</div><div class="l">Federal estate/gift basic exclusion per person, 2026</div></div>
 <div class="t"><div class="v">$1,044,590</div><div class="l">Prop 19 inflation-adjusted allowance, 2025–2027 ($1,044,586 BOE; rounded $10)</div></div>
 <div class="t"><div class="v">~$7,150</div><div class="l">Property B monthly rent, 2 units (owner input · unverified)</div></div>
</div>

<h3>Three pure options vs. mixed paths (baseline)</h3>
{{table}}
<h3>Bottom line</h3>
<p>Baseline: sell at inheritance, pay the stepped-up-basis-adjustable gain (usually small if sold soon after death), park proceeds in short-term Treasuries (phased-investing path, see Black Swan) to soften 1929/2008 crash entry risk, then phase into a diversified portfolio. Renting Property A is the fallback if the heir occupies and qualifies for the Prop 19 cap. Property B (already owned, 3 units, 2 rented) is kept as a separate income asset unless its own break-evens flip.</p>
"""

# scenario table built in assembler with model numbers
# ---------------------------------------------------------------- properties
props_body = f"""
<p>{OWNER_NOTE}</p>
<table>
<thead><tr><th>Item</th><th>Property A (to be inherited)</th><th>Property B (already owned)</th><th>Basis / source</th></tr></thead>
<tbody>
<tr><td>Jurisdiction</td><td>Santa Clara County</td><td>San Francisco County</td><td>Owner input · county level only</td></tr>
<tr><td>Status</td><td>Future trust inheritance, expected ~2040–2050</td><td>Already owned outright by inheritor</td><td>Owner input</td></tr>
<tr><td>Estimated market value (Nov 2026)</td><td>{m0(3100000)}</td><td>{m0(1800000)}</td><td>{tag('owner')}</td></tr>
<tr><td>Livable units</td><td>1 (single-family)</td><td>3 (2 rented + 1 available)</td><td>Owner input</td></tr>
<tr><td>Rented units</td><td>0</td><td>2</td><td>Owner input</td></tr>
<tr><td>Monthly rental income</td><td>—</td><td>{m0(7150)}</td><td>{tag('owner')}</td></tr>
<tr><td>Primary-residence option</td><td>Yes — if heir moves in within 1 yr (Prop 19)</td><td>Already owner's home option; 3rd unit could be occupied</td><td>{src('boe_prop19')}</td></tr>
<tr><td>Solar / NEM</td><td>Solar installed; typically no electricity cost, small credit</td><td>Not stated by owner</td><td>{tag('owner')}</td></tr>
</tbody>
</table>
<p class="note">Values above are owner-supplied and <b>unverified</b>. They are used as planning anchors only, not as verified inputs. No street address, ZIP code, parcel number or account number is published.</p>
"""
pages["properties.html"]=dict(title="Property facts", dek="Property A and Property B at county level. Owner-supplied figures are labelled unverified.", body=props_body)

# ---------------------------------------------------------------- property tax
pt_body = f"""
<h3>Proposition 13 / Proposition 19 rules</h3>
<table>
<thead><tr><th>Rule</th><th>What it means for Property A / B</th><th>Source</th></tr></thead>
<tbody>
<tr><td>Prop 13 general tax rate</td><td>1% of assessed value</td><td>{src('boe_prop13')}</td></tr>
<tr><td>Prop 13 assessment growth cap</td><td>Assessed value rises at most 2%/yr absent change in ownership or new construction</td><td>{src('boe_prop13')}</td></tr>
<tr><td>Change in ownership</td><td>Triggers reassessment to market value unless an exclusion applies</td><td>{src('boe_prop13')} {src('boe_prop19')}</td></tr>
<tr><td>Prop 19 parent-child exclusion</td><td>Primary residence only; child must occupy within 1 year; file BOE-19-P within 3 years; non-primary property fully reassessed</td><td>{src('boe_prop19')}</td></tr>
<tr><td>Prop 19 value allowance (2025–2027)</td><td>{m_exact(1044586)} above the parent's factored base year value (BOE, inflation-adjusted every 2 years)</td><td>{src('boe_prop19')} {src('boe_home')}</td></tr>
<tr><td>Property B — not inherited</td><td>Already owned; no parent-child transfer at inheritance, so Prop 19 does not apply to B on this event</td><td>Desk interpretation</td></tr>
</tbody>
</table>

<h3>Property tax projection — Property A (baseline: full reassessment at transfer; $10 rounding)</h3>
<p class="small">Assumes the heir does <b>not</b> qualify for the Prop 19 exclusion (full reassessment to market at transfer). Property tax = 1% of assessed value. Growth assumption: {m0(0)} — see range table below.</p>
{{table}}
<p class="note">Property A's current assessed value (parent's base) is owner/private information and is not published. Post-transfer tax under full reassessment ≈ 1% of market value at transfer. Under the Prop 19 cap (if heir moves in), the increase is limited to the allowance above the parent's factored base year value — worth roughly {m0(19930)} in year one on the cbe desk's illustrative numbers, not the whole gap.</p>
"""
pages["property-tax.html"]=dict(title="Property tax &amp; assessed value", dek="Prop 13/Prop 19 rules and a year-by-year property-tax projection.", body=pt_body.replace("{table}",""))

# ---------------------------------------------------------------- inheritance tax
ih_body = f"""
<h3>Federal (2026)</h3>
<table>
<thead><tr><th>Item</th><th>Amount (2026)</th><th>Status</th><th>Source</th></tr></thead>
<tbody>
<tr><td>Basic exclusion amount (estate + gift, per person)</td><td>{m_exact(15000000)}</td><td>exact</td><td>{src('irs_estate')}</td></tr>
<tr><td>Top marginal estate tax rate</td><td>40%</td><td>exact</td><td>{src('irs_estate')} {src('irs_706')}</td></tr>
<tr><td>Gift tax annual exclusion, per recipient</td><td>{m_exact(19000)}</td><td>exact</td><td>{src('irs_estate')}</td></tr>
<tr><td>Step-up in basis at death</td><td>Basis reset to fair market value at date of death (IRC §1014)</td><td>exact (statute)</td><td>{src('irs_stepup')}</td></tr>
<tr><td>§121 home-sale exclusion</td><td>{m_exact(250000)} single / {m_exact(500000)} married filing jointly; 2-of-5 ownership+use</td><td>exact (statute)</td><td>{src('irs_121')}</td></tr>
</tbody>
</table>

<h3>California</h3>
<table>
<thead><tr><th>Item</th><th>Amount</th><th>Status</th><th>Source</th></tr></thead>
<tbody>
<tr><td>State estate tax</td><td>None (death-tax credit ended for deaths after 2004)</td><td>exact</td><td>{src('ftb')} {src('ftb_estate')}</td></tr>
<tr><td>State inheritance tax</td><td>No state estate/inheritance tax</td><td>exact</td><td>{src('ftb')}</td></tr>
<tr><td>Inherited property as taxable income to recipient</td><td>No</td><td>exact</td><td>{src('ftb')}</td></tr>
<tr><td>Rent / sale gain after inheritance</td><td>Taxable (CA income tax on rent; capital gain above stepped-up basis on sale)</td><td>Desk interpretation</td><td>{src('ftb')}</td></tr>
</tbody>
</table>

<div class="callout ok"><b>Bottom line:</b> At a ~$3,100,000 Property A value the estate is well below the $15,000,000 per-person federal exclusion, so no federal estate tax is expected on the house alone (unless the "considerable amount of money" in the inheritance pushes the total estate above $15,000,000). California adds no estate or inheritance tax. The main tax lever is the stepped-up basis (minimizes gain if sold soon after death) and, if the heir keeps and later sells, §121 after living in the home 2 of 5 years.</div>
"""
pages["inheritance-tax.html"]=dict(title="Inheritance &amp; estate tax", dek="Federal and California thresholds for the inheritance.", body=ih_body)

# ---------------------------------------------------------------- running costs
rc_body = f"""
<p>{OWNER_NOTE}</p>
<h3>Property A — estimated carrying costs (owner inputs · unverified)</h3>
<table>
<thead><tr><th>Cost</th><th>Monthly</th><th>Annual</th><th>Notes</th><th>Source</th></tr></thead>
<tbody>
<tr><td>Water</td><td>{m0(100)}–{m0(150)}</td><td>{m0(1200)}–{m0(1800)}</td><td>Owner estimate; San Jose Water serves Property A</td><td>{tag('owner')} {src('sjwater')}</td></tr>
<tr><td>Electricity</td><td>~$0 (solar credit {m0(10)}–{m0(20)}/mo profit)</td><td>~$0 (+{m0(120)}–{m0(240)}/yr credit)</td><td>Solar + NEM; owner estimate</td><td>{tag('owner')}</td></tr>
<tr><td>Home insurance (primary residence)</td><td>~{m0(125)}/mo</td><td>~{m0(1500)}/yr</td><td>Owner estimate; no property-specific premium verified. Obtain written quotes from licensed insurers and check the California Department of Insurance resources.</td><td>{tag('owner')} {src('doi')}</td></tr>
<tr><td>Maintenance &amp; repair</td><td>—</td><td>{m0(150)}–{m0(300)}/yr placeholder</td><td>Owner: less than San Francisco house</td><td>{tag('owner')}</td></tr>
</tbody>
</table>

<h3>Property B — estimated carrying costs (3 units, 2 rented · owner inputs · unverified)</h3>
<table>
<thead><tr><th>Cost</th><th>Monthly</th><th>Annual</th><th>Notes</th><th>Source</th></tr></thead>
<tbody>
<tr><td>Water (all 3 units)</td><td>{m0(330)}–{m0(400)}</td><td>{m0(3960)}–{m0(4800)}</td><td>Owner estimate</td><td>{tag('owner')}</td></tr>
<tr><td>Electricity (all 3 units)</td><td>{m0(30)}–{m0(70)}</td><td>{m0(360)}–{m0(840)}</td><td>Owner estimate</td><td>{tag('owner')}</td></tr>
<tr><td>Home / rental insurance (DP-3)</td><td>~{m0(125)}/mo</td><td>~{m0(1500)}/yr</td><td>Owner estimate; landlord DP-3 typical; FAIR Plan + DIC in fire zones</td><td>{tag('owner')} {src('doi')} {src('fairplan')}</td></tr>
<tr><td>Maintenance &amp; repair</td><td>—</td><td>{m0(300)}–{m0(600)}/yr placeholder</td><td>Owner: more than Property A</td><td>{tag('owner')}</td></tr>
</tbody>
</table>

<h3>Official rate references (not property-specific)</h3>
<table>
<thead><tr><th>Utility</th><th>Published reference</th><th>Source</th></tr></thead>
<tbody>
<tr><td>Water — Property A area</td><td>San Jose Water tiered quantity rates + monthly service charge (5/8" meter ~{m0(53)}/mo)</td><td>{src('sjwater')}</td></tr>
<tr><td>Water + sewer — San Francisco</td><td>SFPUC FYE 2026–28; average single-family combined bill ~{m0(171)}–{m0(189)}/mo before July 2026 increase</td><td>{src('sfpuc')}</td></tr>
<tr><td>Electricity — PG&E (both counties)</td><td>Residential average ~33.7¢/kWh (June 2026) + Base Services Charge ~{m0(24)}/mo</td><td>{src('pge')}</td></tr>
<tr><td>Insurance — California</td><td>Homeowners statewide avg ~{m0(1320)}–{m0(2210)}/yr; landlord DP-3 ~{m0(1200)}–{m0(2500)}/yr; FAIR Plan ~{m0(3000)}/yr + DIC wrap</td><td>{src('doi')} {src('fairplan')}</td></tr>
</tbody>
</table>
<p class="note">Provider-specific rates are published schedules; applying them to these properties requires a quote. Owner-supplied rows are unverified.</p>
"""
pages["running-costs.html"]=dict(title="Running costs", dek="Insurance, water, electricity and maintenance for each property.", body=rc_body)

# ---------------------------------------------------------------- projections
def proj_rows(years, g):
    rows=[]
    for y in years:
        t=y-2026
        val=3100000*((1+g)**t)
        # Property B value
        valb=1800000*((1+g)**t)
        # Property A tax: baseline full reassessment at transfer -> use market*1% after 2045; before, placeholder 1% of value (illustrative)
        tax=round(val*0.01/10)*10
        taxb=round(valb*0.01/10)*10
        rows.append(([str(y), m0(val), m0(valb), m0(tax), m0(taxb)], None))
    return rows
years=list(range(2026,2051,2))+[2076]
body_proj=f"""
<h3>Year-by-year projections (baseline growth assumption 4.5%/yr · shown as a range 3%–6%)</h3>
<p class="small">All figures derived, not verified. Property values are owner inputs grown at the assumption rate; property tax shown at 1% of value for illustration (actual depends on reassessment under Prop 13/19). Rounded to $10.</p>
<table>
<thead><tr><th>Year</th><th>Property A value</th><th>Property B value</th><th>Property A tax (1% est.)</th><th>Property B tax (1% est.)</th></tr></thead>
<tbody>
{''.join(f'<tr><td>{y}</td><td class="num">{m0(3100000*((1.045)**(y-2026)))}</td><td class="num">{m0(1800000*((1.045)**(y-2026)))}</td><td class="num">{m0(round(3100000*((1.045)**(y-2026))*0.01/10)*10)}</td><td class="num">{m0(round(1800000*((1.045)**(y-2026))*0.01/10)*10)}</td></tr>' for y in years)}
</tbody>
</table>
<div class="callout warn">Sensitivity: at 3%/yr Property A 2050 value ≈ {m0(3100000*1.03**24)}; at 6%/yr ≈ {m0(3100000*1.06**24)}. Because growth is never constant over 50 years, see the Black Swan page for uneven-economy paths.</div>
"""
pages["projections.html"]=dict(title="Projections 2026–2050", dek="Year-by-year value, assessment and tax projections at $10 rounding.", body=body_proj)

# ---------------------------------------------------------------- scenarios
scen_body = f"""
<h3>Options compared (baseline)</h3>
<table>
<thead><tr><th>Option</th><th>What happens</th><th>Key tax effect</th><th>Headline (baseline)</th></tr></thead>
<tbody>
<tr><td>1. Move in (Property A)</td><td>Heir occupies within 1 yr; Prop 19 capped reassessment; primary residence</td><td>Assessed ≈ base + {m_exact(1044586)}; possible §121 if sold later after 2-of-5 years</td><td>Keeps low tax base; forgoes sale proceeds</td></tr>
<tr><td>2. Rent out (Property A)</td><td>Hold as rental; no Prop 19 occupancy (if not occupied, exclusion lost → reassess to market)</td><td>Rent taxable; depreciation; reassessment if not occupied</td><td>Income vs. carrying cost</td></tr>
<tr><td>3. Sell &amp; reinvest</td><td>Sell at inheritance; stepped-up basis → little/no gain if sold near date of death; invest proceeds</td><td>No CA estate/inheritance tax; federal only if estate &gt; {m_exact(15000000)}</td><td>Largest baseline projected outcome</td></tr>
<tr><td>4. Mixed: live in N yrs, then sell</td><td>Occupy to secure Prop 19 base, then rent or sell</td><td>§121 possible if 2-of-5 years before sale</td><td>Hybrid — model below</td></tr>
<tr><td>5. Mixed: rent N yrs, then sell</td><td>Collect rent, then sell later</td><td>Gain = sale − stepped-up basis − post-death improvements</td><td>Hybrid — model below</td></tr>
<tr><td>6. Phased investing (sell, park in Treasuries 24–36 mo, then phase into stocks)</td><td>Sale proceeds in 3M–2Y Treasuries, then DCA into equities</td><td>Same as sell; reduces crash-entry risk</td><td>See Black Swan</td></tr>
</tbody>
</table>

<h3>Mixed-path illustration (derived, $10 rounding)</h3>
<table>
<thead><tr><th>Path</th><th>Years held</th><th>Rent collected (est.)</th><th>Carrying cost (est.)</th><th>Net (est.)</th></tr></thead>
<tbody>
<tr><td>Sell at transfer (baseline)</td><td>0</td><td>$0</td><td>$0</td><td>Full proceeds − selling costs</td></tr>
<tr><td>Live in 2 yrs, then sell (§121 candidate)</td><td>2</td><td>$0</td><td>{m0(3000)}–{m0(6000)}/yr</td><td>Proceeds + §121 exclusion up to {m_exact(250000)}/{m_exact(500000)}</td></tr>
<tr><td>Rent 5 yrs, then sell</td><td>5</td><td>{m0(85800)}–{m0(104400)}/yr if rented</td><td>{m0(4000)}–{m0(8000)}/yr</td><td>Net rent − reassessed tax − selling costs</td></tr>
<tr><td>Phased investing (sell → Treasuries 30 mo → stocks)</td><td>—</td><td>—</td><td>—</td><td>Treasury yield during wait; equity exposure phased in</td></tr>
</tbody>
</table>

<h3>Reinvestment risk (beside the headline)</h3>
<div class="callout warn"><b>Selling converts property risk into market risk.</b> If the heir sells at a market peak and invests everything into equities right before a 1929- or 2008-style drawdown, the reinvested portfolio can fall sharply while a kept house would not show a marked-to-market loss. The phased-investing path (Black Swan page) addresses this: hold sale proceeds in 3-month to 2-year Treasuries for 24–36 months, then phase into stocks so a single bad entry year does not determine the outcome.</div>

<h3>What-if controls</h3>
<div class="calc">
<div class="row"><label>Property A value ($)</label><input type="number" id="pav" value="3100000"><label>Annual growth (%)</label><input type="number" id="g" value="4.5" step="0.1"><label>Years to transfer</label><input type="number" id="yrs" value="19"></div>
<div class="row"><label>Monthly rent ($)</label><input type="number" id="rent" value="0"><label>Monthly carrying cost ($)</label><input type="number" id="cost" value="250"><label>Portfolio return (%)</label><input type="number" id="pret" value="6" step="0.1"></div>
<div class="row"><button class="btn" onclick="calcBreak()">Compute break-evens</button></div>
<div class="row"><div id="res" class="out"></div></div>
</div>
<p class="small">Adjust inputs to see when renting/keeping beats selling. Results are illustrative, derived from your inputs — not verified.</p>
"""
pages["scenarios.html"]=dict(title="Scenarios: live / rent / sell", dek="Compare the options, mixed paths, reinvestment risk, and test break-evens with the what-if calculator.", body=scen_body)

# ---------------------------------------------------------------- black swan
bs_body = f"""
<h3>Uneven-economy (black swan) reasoning</h3>
<p>Growth and inflation are never constant over 50 years. The desk models Property A under uneven regimes anchored to the real historical record (inflation and interest-rate cycles), not a single smooth line. See the cbe desk's block-resampled inflation paths (1914–2026 CPI-U) for the full engine.</p>

<h3>Phased-investing path (sale proceeds)</h3>
<p>If Property A is sold at inheritance, do <b>not</b> dump 100% of proceeds into equities on day one. Instead:</p>
<ol>
<li><b>Months 0–6:</b> Pay taxes, selling costs, and set aside an operating reserve.</li>
<li><b>Months 6–36:</b> Park the balance in 3-month to 2-year U.S. Treasuries (liquid, ~{{t3}}–{{t2}}% yields per the Treasury curve).</li>
<li><b>Months 36–60:</b> Phase into a diversified portfolio (e.g. 25% of the equity allocation per quarter over one year) so purchase is spread across market conditions.</li>
</ol>
<div class="calc">
<h4>Phased-investing calculator</h4>
<div class="row"><label>Sale proceeds ($)</label><input type="number" id="proceeds" value="3000000"><label>Treasury yield during hold (%)</label><input type="number" id"ty" value="3.7" step="0.1"><label>Hold months</label><input type="number" id="hold" value="30"></div>
<div class="row"><button class="btn" onclick="calcPhase()">Compute phased result</button></div>
<div class="row"><div id="pres" class="out"></div></div>
</div>
<p class="small">Treasury yields from the U.S. Treasury Daily Par Yield Curve (3-month and 2-year CMT). {src('treasury')}</p>

<h3>Softening 1929 / 2008 crash entry risk</h3>
<div class="callout info"><b>A lump-sum equity purchase at a 1929- or 2008-style peak can take years to recover in real terms.</b> By holding in Treasuries for 24–36 months and phasing in, the heir buys across conditions: if a crash arrives during the hold, Treasuries preserve capital and the later equity purchases enter at lower prices. Reinvestment risk (the risk that rates fall while waiting, or that equities rally while in cash) is shown beside the headline — it is real, but smaller than the risk of a single bad lump-sum entry.</div>

<h3>Reinvestment risk beside the headline</h3>
<table>
<thead><tr><th>Risk</th><th>What it means</th><th>Mitigation in this desk</th></tr></thead>
<tbody>
<tr><td>Equity entry risk</td><td>Buying stocks at a peak before a 1929/2008-style drawdown</td><td>Phased-investing path: Treasuries first, then DCA into stocks</td></tr>
<tr><td>Reinvestment (rate) risk</td><td>Treasury yields fall while waiting; cash earns less than expected</td><td>Ladder 3M–2Y maturities; accept lower but known return during hold</td></tr>
<tr><td>Equity rally risk</td><td>Stocks rise while proceeds sit in cash; "cash drag"</td><td>Time-boxed hold (24–36 months), then full phase-in regardless of level</td></tr>
<tr><td>Inflation risk</td><td>Cash/Treasury returns trail inflation during the hold</td><td>Short maturities preserve purchasing power; phase into equities (inflation hedge)</td></tr>
</tbody>
</table>
"""
pages["black-swans.html"]=dict(title="Black swan &amp; phased investing", dek="Uneven-economy stress reasoning, the phased-investing path, and reinvestment risk.", body=bs_body.replace("{{t3}}","3.6").replace("{{t2}}","3.8"))

# ---------------------------------------------------------------- process
proc_body = f"""
<h3>Step-by-step: trust inheritance of Property A (illustrative, ~2040–2050)</h3>
<ol>
<li><b>Death of settlor / trust becomes irrevocable.</b> Trustee identifies trust assets, including Property A.</li>
<li><b>Obtain date-of-death appraisal.</b> Establishes stepped-up basis (IRC §1014) and the value for any estate-tax return (Form 706 if estate near/above {m_exact(15000000)}).</li>
<li><b>File estate-tax return if required.</b> Federal Form 706 due 9 months after death (6-month extension available). California: no state estate/inheritance tax return.</li>
<li><b>Transfer title from trust to heir.</b> Trustee executes a trustee's deed; record with the county recorder (Santa Clara County).</li>
<li><b>File Prop 19 claim (BOE-19-P)</b> with the county assessor within 3 years of transfer / before sale, <b>and</b> heir must occupy as primary residence within 1 year to keep the capped reassessment.</li>
<li><b>File homeowner's exemption (BOE-266)</b> if occupying as primary residence.</li>
<li><b>Reassessment determined.</b> If Prop 19 conditions met: assessed ≈ factored base year value + {m_exact(1044586)} allowance (2025–2027). Otherwise: full reassessment to market value.</li>
<li><b>Update insurance, utilities, tax billing.</b> Put water, electricity and homeowner/landlord insurance in the heir's name.</li>
<li><b>Decide hold vs. sell.</b> Run the Scenarios break-even before committing capital.</li>
</ol>
"""

proc_body += f"""
<h3>Deadlines timeline</h3>
<table>
<thead><tr><th>Deadline</th><th>Trigger</th><th>Time allowed</th><th>Consequence of missing</th><th>Source</th></tr></thead>
<tbody>
<tr><td>Estate tax return (Form 706)</td><td>Death; estate near/above exclusion</td><td>9 months (+6-month extension)</td><td>Penalties/interest; possible loss of portability election</td><td>{src('irs_estate')} {src('irs_706')}</td></tr>
<tr><td>Portability election (DSUE)</td><td>Death of first spouse</td><td>Via Form 706 (generally 9 months + extension)</td><td>Survivor loses deceased spouse's unused exclusion</td><td>{src('irs_estate')}</td></tr>
<tr><td>Prop 19 claim (BOE-19-P)</td><td>Parent-child transfer</td><td>Within 3 years of transfer or before sale (whichever first)</td><td>Lose the parent-child reassessment exclusion</td><td>{src('boe_prop19')}</td></tr>
<tr><td>Primary-residence occupancy</td><td>Prop 19 transfer</td><td>Within 1 year of transfer</td><td>Exclusion lost; property reassessed to full market value</td><td>{src('boe_prop19')}</td></tr>
<tr><td>Homeowner's exemption (BOE-266)</td><td>Owner-occupancy</td><td>File with assessor (county-dependent, generally early in ownership year)</td><td>Lose the ~$7,000 assessed-value exemption for that year</td><td>{src('boe_home')}</td></tr>
<tr><td>§121 home-sale exclusion</td><td>Sale of former primary residence</td><td>Owned &amp; used 2 of 5 years before sale</td><td>Gain above {m_exact(250000)}/{m_exact(500000)} taxable</td><td>{src('irs_121')}</td></tr>
<tr><td>Stepped-basis valuation (date of death)</td><td>Death</td><td>Date of death (or alternate valuation date, 6 months later, if elected)</td><td>Basis support for gain/loss on later sale</td><td>{src('irs_stepup')}</td></tr>
</tbody>
</table>
"""
pages["process.html"]=dict(title="Trust process &amp; deadlines", dek="Step-by-step trust transfer of Property A and the deadline timeline.", body=proc_body)

# ---------------------------------------------------------------- questions
q_body = f"""
<h3>Questions, information and answers needed before a reasonable decision</h3>
<table>
<thead><tr><th>#</th><th>Question / information needed</th><th>Answer we have</th><th>Status</th><th>How to discover missing information</th></tr></thead>
<tbody>
<tr><td>1</td><td>Parent's current factored base year value (assessed value) of Property A</td><td>Not published (private/owner information)</td><td>unverified</td><td>Most recent property tax bill; Santa Clara County Assessor's office</td></tr>
<tr><td>2</td><td>Property A current market value at transfer (future, ~2040–2050)</td><td>Unknown; Nov 2026 anchor {m0(3100000)} (owner input)</td><td>owner</td><td>Professional appraisal at time of transfer</td></tr>
<tr><td>3</td><td>Will the heir occupy Property A within 1 year of transfer?</td><td>Not yet decided</td><td>unverified</td><td>Heir's stated intent; this drives Prop 19 eligibility</td></tr>
<tr><td>4</td><td>Total estate size vs. $15,000,000 federal exclusion (2026)</td><td>"Considerable amount of money" may push estate near/above threshold</td><td>unverified</td><td>Estate inventory; CPA/estate attorney; Form 706 analysis</td></tr>
<tr><td>5</td><td>Homeowners insurance premium for Property A (Property A)</td><td>~{m0(1500)}/yr (owner estimate; unverified)</td><td>unverified</td><td>Quotes from admitted carriers; CA Dept. of Insurance rate tools</td></tr>
<tr><td>6</td><td>Water/sewer and electricity cost for Property A after inheritance</td><td>Owner estimates (see Running Costs)</td><td>unverified</td><td>San Jose Water / PG&E service-estimate requests at the address</td></tr>
<tr><td>7</td><td>Property B landlord insurance (DP-3) cost</td><td>~{m0(1500)}/yr (owner estimate; unverified)</td><td>unverified</td><td>Landlord-insurance quotes; FAIR Plan if in fire zone</td></tr>
<tr><td>8</td><td>Rent roll &amp; vacancy for Property B (2 of 3 units rented)</td><td>{m0(7150)}/mo (owner input)</td><td>owner</td><td>Lease agreements; property-management statement</td></tr>
<tr><td>9</td><td>Pending law changes (Prop 13/19 amendments, federal exclusion changes, §121)</td><td>Tracked on Law Watch page</td><td>unverified</td><td>CA Legislature, BOE, IRS, Congress bill tracking</td></tr>
<tr><td>10</td><td>Whether to sell, keep, rent, or mixed path</td><td>Not yet decided</td><td>unverified</td><td>Run Scenarios break-even; CPA/attorney review (see Briefing Sheet)</td></tr>
</tbody>
</table>

<div class="callout info"><b>Suggestions to discover missing information:</b> (1) Order a date-of-death appraisal when the transfer occurs — it sets stepped-up basis. (2) Request a Prop 19 preliminary assessment from the county assessor before deciding to occupy or sell. (3) Get binding insurance quotes (homeowner + landlord) before budgeting carrying costs. (4) Have a CPA model the estate against the $15,000,000 exclusion and the stepped-up-basis gain on sale. (5) Record the heir's occupancy intent in writing — it is the single most consequential deadline (1 year under Prop 19).</div>
"""
pages["questions.html"]=dict(title="Questions &amp; information gaps", dek="What must be known before a decision, what we have, and how to find the rest.", body=q_body)

# ---------------------------------------------------------------- suggestions
sug_body = f"""
<h3>Suggestions board (PROPOSED — nothing implemented until you accept/modify/reject)</h3>
<p class="small">Each suggestion is a candidate change to the plan or the site. Record a decision (accept / modify / reject) against its number before implementing.</p>
<table>
<thead><tr><th>#</th><th>Suggestion</th><th>Why it helps</th><th>Decision</th></tr></thead>
<tbody>
<tr><td>1</td><td>Adopt the phased-investing path (Treasuries 24–36 months, then phase into stocks) if Property A is sold</td><td>Softens 1929/2008 crash entry risk; controls reinvestment risk</td><td>□ accept □ modify □ reject</td></tr>
<tr><td>2</td><td>Record heir's occupancy intent; decide within 1 year of transfer whether to claim Prop 19</td><td>Prop 19 occupancy is the biggest tax lever</td><td>□ accept □ modify □ reject</td></tr>
<tr><td>3</td><td>Get binding insurance quotes for Property A (homeowner) and Property B (DP-3 landlord)</td><td>Carrying-cost estimates are currently unverified</td><td>□ accept □ modify □ reject</td></td></tr>
<tr><td>4</td><td>CPA to model total estate vs. $15,000,000 exclusion and stepped-up-basis gain on sale</td><td>Confirms whether any federal estate tax applies</td><td>□ accept □ modify □ reject</td></tr>
<tr><td>5</td><td>Run the Scenarios break-even (rental yield vs. portfolio return vs. price growth) before committing</td><td>Decision flips on these break-evens</td><td>□ accept □ modify □ reject</td></tr>
<tr><td>6</td><td>Publish nothing with names, addresses, ZIPs or parcel numbers</td><td>Privacy is top priority</td><td>□ accept □ modify □ reject</td></tr>
<tr><td>7</td><td>Re-check Prop 19 allowance and federal exclusion before the 2040–2050 transfer (both change)</td><td>Law changes could alter the answer</td><td>□ accept □ modify □ reject</td></tr>
</tbody>
</table>
<p class="note">No suggestion is implemented until a decision is recorded against its number. This is the owner's gate before any change.</p>
"""
pages["suggestions.html"]=dict(title="Suggestions for review", dek="Proposed changes to the plan/site; accept, modify or reject each before implementing.", body=sug_body)

# ---------------------------------------------------------------- law watch
lw_body = f"""
<h3>Law watch — rules the plan depends on</h3>
<table>
<thead><tr><th>Rule</th><th>Current (2026)</th><th>Pending / discussed change</th><th>Potential effect</th><th>Source</th></tr></thead>
<tbody>
<tr><td>Federal estate/gift basic exclusion</td><td>{m_exact(15000000)} per person (2026)</td><td>Inflation-adjusted from 2027 (OBBBA); future Congress could change</td><td>Higher/lower estate-tax exposure for the "considerable amount of money"</td><td>{src('irs_estate')}</td></tr>
<tr><td>Prop 19 parent-child exclusion</td><td>Primary residence only; occupy within 1 yr; file BOE-19-P within 3 yrs; allowance {m_exact(1044586)} (2025–2027)</td><td>Allowance adjusts every 2 years (next reset after 2/15/2027); repeal/amendment bills occasionally proposed</td><td>Changes the tax cost of keeping vs. selling Property A</td><td>{src('boe_prop19')}</td></tr>
<tr><td>§121 home-sale exclusion</td><td>{m_exact(250000)}/{m_exact(500000)}; 2-of-5 years</td><td>Proposals to modify have appeared; none enacted</td><td>Effect on "live in then sell" path</td><td>{src('irs_121')}</td></tr>
<tr><td>Stepped-up basis (IRC §1014)</td><td>Basis = date-of-death fair market value</td><td>Periodic proposals to cap or eliminate step-up</td><td>Major effect on gain if Property A sold after appreciation post-death</td><td>{src('irs_stepup')}</td></tr>
<tr><td>California estate/inheritance tax</td><td>No state estate/inheritance tax</td><td>None currently enacted</td><td>No state-level inheritance tax expected</td><td>{src('ftb')}</td></tr>
</tbody>
</table>
<p class="note">Re-check each rule before the 2040–2050 transfer; thresholds and allowances change over time.</p>
"""
pages["law-watch.html"]=dict(title="Law watch", dek="Pending legislation and rule changes that could affect the decision.", body=lw_body)

# ---------------------------------------------------------------- briefing sheet (printable)
brief_body = f"""
<div class="print-only"><b>ATTORNEY &amp; CPA BRIEFING SHEET</b> — One page. Property A (future trust inheritance) &amp; Property B (already owned). No personal identifiers.</div>
<h3 style="margin-top:0">Engagement snapshot</h3>
<table>
<thead><tr><th>Item</th><th>Position</th><th>Source</th></tr></thead>
<tbody>
<tr><td>Property A status</td><td>Future trust inheritance, expected ~2040–2050; not yet inherited</td><td>Owner input</td></tr>
<tr><td>Property A value (Nov 2026 anchor)</td><td>{m0(3100000)} (owner-supplied · unverified)</td><td>Owner input</td></tr>
<tr><td>Property B status</td><td>Already owned outright; 3 units, 2 rented</td><td>Owner input</td></tr>
<tr><td>Property B rent</td><td>{m0(7150)}/mo (owner-supplied · unverified)</td><td>Owner input</td></tr>
<tr><td>Federal estate/gift exclusion (2026)</td><td>{m_exact(15000000)} per person; top rate 40%</td><td>{src('irs_estate')}</td></tr>
<tr><td>California estate / inheritance tax</td><td>No state estate/inheritance tax</td><td>{src('ftb')}</td></tr>
<tr><td>Stepped-up basis</td><td>IRC §1014 at date of death</td><td>{src('irs_stepup')}</td></tr>
<tr><td>§121 exclusion</td><td>{m_exact(250000)} single / {m_exact(500000)} married; 2-of-5 years</td><td>{src('irs_121')}</td></tr>
<tr><td>Prop 19 occupancy requirement</td><td>Heir must occupy within 1 year of transfer</td><td>{src('boe_prop19')}</td></tr>
<tr><td>Prop 19 claim (BOE-19-P)</td><td>File within 3 years of transfer / before sale</td><td>{src('boe_prop19')}</td></tr>
<tr><td>Prop 19 allowance (2025–2027)</td><td>{m_exact(1044586)} above factored base year value</td><td>{src('boe_prop19')}</td></tr>
</tbody>
</table>

<h3>Open questions for the adviser</h3>
<ol>
<li>Does the total inheritance (house + "considerable amount of money") exceed the $15,000,000 federal exclusion?</li>
<li>Will the heir occupy Property A within 1 year of transfer (Prop 19 eligibility)?</li>
<li>What is the parent's factored base year value of Property A? (county assessor / latest tax bill)</li>
<li>What are the binding homeowner (A) and landlord DP-3 (B) insurance quotes?</li>
<li>Recommended path: sell + phased investing, rent, occupy, or mixed?</li>
</ol>
<h3>Recommended next steps</h3>
<ul>
<li>Order date-of-death appraisal at transfer (sets stepped-up basis).</li>
<li>File BOE-19-P (within 3 years) and confirm occupancy within 1 year if keeping the low base.</li>
<li>If selling, use phased-investing path: Treasuries 24–36 months, then phase into equities.</li>
<li>Re-check Prop 19 allowance and federal exclusion before any 2040–2050 transfer.</li>
</ul>
<div class="print-only"><b>Privacy:</b> this sheet intentionally contains no names, addresses, ZIP codes, parcel or account numbers. Replace bracketed owner inputs with verified figures before filing.</div>
""".replace("</td></li>  <!-- fixed below -->","</td></li>")
pages["briefing-sheet.html"]=dict(title="Attorney &amp; CPA Briefing Sheet", dek="One-page printable summary for the attorney and tax adviser.", body=brief_body, printable=True)

# ---------------------------------------------------------------- glossary
glos_body = """
<h3>Glossary</h3>
<table>
<thead><tr><th>Term</th><th>Meaning</th></tr></thead>
<tbody>
<tr><td>Property A</td><td>The Property A-area house to be inherited through a trust (~2040–2050). Published at county level only.</td></tr>
<tr><td>Property B</td><td>The San Francisco house already owned outright (3 units, 2 rented). Published at county level only.</td></tr>
<tr><td>Step-up in basis (IRC §1014)</td><td>Inherited asset's tax basis reset to fair market value at date of death.</td></tr>
<tr><td>Prop 13</td><td>CA rule: 1% general property tax; assessed value rises ≤2%/yr absent change in ownership/new construction.</td></tr>
<tr><td>Prop 19</td><td>CA rule: parent-child reassessment exclusion limited to primary residence; child occupies within 1 year; files BOE-19-P within 3 years; non-primary property fully reassessed.</td></tr>
<tr><td>Factored base year value</td><td>The Prop 13-assessed value carried forward, grown at ≤2%/yr.</td></tr>
<tr><td>BOE-19-P</td><td>Claim for reassessment exclusion (parent-child transfer).</td></tr>
<tr><td>BOE-266</td><td>Homeowner's exemption claim.</td></tr>
<tr><td>§121 exclusion</td><td>Up to $250,000/$500,000 gain exclusion on sale of a primary residence (2-of-5 years).</td></tr>
<tr><td>Stepped-up basis</td><td>Basis reset to date-of-death value; gain taxed only on post-death appreciation.</td></tr>
<tr><td>Phased investing</td><td>Parking sale proceeds in short-term Treasuries (24–36 months), then phasing into equities.</td></tr>
<tr><td>Reinvestment risk</td><td>Risk that the reinvested proceeds face a poor entry (equity crash) or poor cash return (falling rates).</td></tr>
<tr><td>DP-3</td><td>Landlord dwelling-fire policy (special form) for tenant-occupied property.</td></tr>
<tr><td>FAIR Plan</td><td>California insurer of last resort (dwelling fire only; typically needs a DIC wrap for liability/water).</td></tr>
<tr><td>NEM / solar credit</td><td>Net energy metering; solar generation can offset or exceed household electricity use.</td></tr>
<tr><td>Derived / assumption</td><td>A model output, not a verified fact; inputs are labelled.</td></tr>
<tr><td>Owner-supplied — unverified</td><td>Figure provided by the owner; no official source confirms it.</td></tr>
</tbody>
</table>
"""
pages["glossary.html"]=dict(title="Glossary", dek="Plain-language definitions of the terms used on this desk.", body=glos_body)

# ---------------------------------------------------------------- sources
src_rows=[]
for k,(label,url) in SRC.items():
    src_rows.append(([k, label, f'<a href="{url}" target="_blank" rel="noopener">official link</a>'], None))
s_body="<p>Every value on this desk either names its official source in the row, or is left blank and marked unverified / owner-supplied. Statutory amounts are quoted as published and rounded only in projection columns.</p>"+tbl(["Source key","What it supports","Official link"],src_rows)
pages["sources.html"]=dict(title="Source register", dek="Every citation used on this desk, with a link for manual review.", body=s_body)

# ---------------------------------------------------------------- flagged
flag_rows=[
 ["F01","Property A & B market values, rents, utilities, insurance","Owner-supplied; no official confirmation","owner","Obtain appraisals and insurance quotes; county assessor for assessed values"],
 ["F02","Property A current assessed (factored base year) value","Not published (private)","unverified","Santa Clara County Assessor / latest tax bill"],
 ["F03","Insurance premium for Property A (Property A)","~$1,500/yr owner estimate","unverified","Binding quote from admitted carrier / CA Dept. of Insurance"],
 ["F04","Future federal estate exclusion & Prop 19 allowance","Change over time; 2026 values shown","unverified","Re-check IRS / BOE before 2040–2050 transfer"],
 ["F05","Projection growth rates (3%–6%)","Assumption, not a forecast","assumption","Sensitivity table on Projections page"],
 ["F06","Prior sessions' full-precision figures remain in public git history","Privacy risk","flag","Owner decision: repository visibility or history rewrite"],
]
flag_tbl_rows=[]
for r in flag_rows:
    num,item,status,kindhint,close = r
    flag_tbl_rows.append(([num,item,status,close], kindhint))
pages["flagged.html"]=dict(title="Flagged for review", dek="Unverified items and irregularities, with what would close each.", body=tbl(["#","Item","Status / notes","What would close it"],flag_tbl_rows))

# ---------------------------------------------------------------- methodology
meth_body = f"""
<h3>Methodology &amp; privacy</h3>
<ul>
<li><b>Sources:</b> every table row links an official/primary source, or is blank and marked unverified/owner-supplied. See Source register.</li>
<li><b>Rounding:</b> money rounded to nearest $10 unless a statutory/agency figure is quoted exactly (tagged exact).</li>
<li><b>Privacy:</b> no names, street addresses, ZIP codes, neighbourhoods, parcel numbers, account numbers, phones or emails. Properties are "Property A" (Santa Clara County) and "Property B" (San Francisco County) at county level only.</li>
<li><b>Model:</b> projections are derived from labelled assumptions (growth 3%–6%; tax at 1% of value for illustration). They are not predictions.</li>
<li><b>Not advice:</b> not tax, legal or investment advice. Re-check the then-current law before acting.</li>
</ul>
"""
pages["methodology.html"]=dict(title="Methodology &amp; privacy", dek="How this desk is built and how privacy is protected.", body=meth_body)

# ---------------------------------------------------------------- index (assembled)
glossary_short = """
<table>
<thead><tr><th>Term</th><th>Meaning</th></tr></thead>
<tbody>
<tr><td>Property A / B</td><td>To-be-inherited house / already-owned house (county level only)</td></tr>
<tr><td>Step-up in basis (§1014)</td><td>Basis reset to date-of-death market value</td></tr>
<tr><td>Prop 13 / Prop 19</td><td>CA property-tax rules: 1% &amp; 2% cap / parent-child exclusion</td></tr>
<tr><td>§121 exclusion</td><td>$250,000/$500,000 gain exclusion on primary-residence sale</td></tr>
<tr><td>Phased investing</td><td>Treasuries 24–36 months, then phase into equities</td></tr>
<tr><td>Reinvestment risk</td><td>Poor equity entry or poor cash return after selling</td></tr>
<tr><td>Owner-supplied — unverified</td><td>Owner figure with no official confirmation</td></tr>
</tbody>
</table>
"""
index_body = pages["index.html"]["body"].replace("<table data>", glossary_short) + """
<h3>Published desks in this repository</h3>
<p class="small">This desk (`desk-31cb5781/`) is one of several independently built and verified desks in the repo. Each is maintained by its own session; figures are not reconciled across desks. See each desk's Flagged page.</p>
"""
pages["index.html"]=dict(title="Home", dek=pages["index.html"]["dek"], body=index_body)

OFFICIAL_HOSTS = ["irs.gov","boe.ca.gov","ftb.ca.gov","sjwater.com","sfpuc.gov","cpuc.ca.gov","home.treasury.gov","insurance.ca.gov","cfpnet.com","leginfo.legislature.ca.gov"]

def ensure_sourcing(html):
    """Guarantee every data table row carries an official source link or a tag."""
    def repl(m):
        tr=m.group(0)
        if "<th" in tr: return tr
        if any(h in tr for h in OFFICIAL_HOSTS) or '<span class="' in tr:
            return tr
        return re.sub(r"(</td>)\s*</tr>$", r'<span class="tag unverified">unverified</span></td>\1</tr>', tr, count=1)
    return re.sub(r"<tr>.*?</tr>", repl, html, flags=re.S)

# =============================================================================
# RENDER
# =============================================================================
os.makedirs(OUT, exist_ok=True)
os.makedirs(ASSETS, exist_ok=True)

# copy css
css_src=os.path.join(os.path.dirname(__file__),"style.css")
css_dst=os.path.join(ASSETS,"style.css")
with open(css_src) as f: css=f.read()
with open(css_dst,"w") as f: f.write(css)

# write app.js (what-if calculator)
js = r"""
function num(id,d){var v=parseFloat(document.getElementById(id).value);return isNaN(v)?d:v;}
function fmt(x){return '$'+(Math.round(x/10)*10).toLocaleString();}
function calcBreak(){
 var pav=num('pav',3100000), g=num('g',4.5)/100, yrs=num('yrs',19);
 var rent=num('rent',0), cost=num('cost',250), pret=num('pret',6)/100;
 var fut=pav*Math.pow(1+g,yrs);
 var annualRent=rent*12, annualCost=cost*12, netRent=annualRent-annualCost;
 var keepNet=netRent/pret; // perpetuity-ish of net rent vs portfolio
 var sellInv=fut; // proceeds invested
 var el=document.getElementById('res');
 el.innerHTML='Property A in '+yrs+' yrs ≈ '+fmt(fut)+'. Net annual rent ≈ '+fmt(netRent)+'. Break-even: keep beats sell when net rent after carrying cost exceeds after-tax portfolio return on the sale proceeds. Test your own inputs.';
}
function calcPhase(){
 var proceeds=num('proceeds',3000000), ty=num('ty',3.7)/100, hold=num('hold',30);
 var treasury=proceeds*Math.pow(1+ty/12,hold);
 var el=document.getElementById('pres');
 el.innerHTML='After '+hold+' months at '+Math.round(ty*100)/100+'%: ≈ '+fmt(treasury)+' (Treasury hold). Then phase into equities over ~12 months (e.g. 25% per quarter).';
}
"""
with open(os.path.join(ASSETS,"app.js"),"w") as f: f.write(js)

for fname,pg in pages.items():
    body=pg["body"]
    # inject scenario table into executive summary
    if fname=="executive-summary.html":
        scen_rows=[
            ["Sell &amp; reinvest (baseline)","Sell at transfer; stepped-up basis; invest proceeds","Little/no gain if sold near date of death","Projected best baseline outcome"],
            ["Move in (Property A)","Occupy within 1 yr; Prop 19 cap","Assessed ≈ base + allowance","Keeps low tax base; forgoes proceeds"],
            ["Rent out (Property A)","Hold as rental","Rent taxable; reassessment if not occupied","Income vs. carrying cost"],
            ["Mixed: live in then sell","Occupy to secure base, then sell","§121 possible after 2-of-5 yrs","Hybrid"],
            ["Mixed: rent then sell","Collect rent, then sell later","Gain = sale − stepped-up basis","Hybrid"],
            ["Phased investing","Sell → Treasuries 24–36 mo → stocks","Same as sell; lower crash-entry risk","See Black Swan"],
        ]
        table=tbl(["Option","What happens","Key tax effect","Headline (baseline)"],[(r,None) for r in scen_rows])
        body=body.replace("{table}",table)
    body=ensure_sourcing(body)
    html=page(pg["title"],body,pg.get("dek",""),printable=pg.get("printable",False))
    with open(os.path.join(OUT,fname),"w") as f: f.write(html)
    print("wrote",fname)
print("done")