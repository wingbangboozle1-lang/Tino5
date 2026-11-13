#!/usr/bin/env python3
"""Build the privacy-safe, source-linked inheritance decision desk.

Published artifact: public-safe/ (the sole GitHub Pages application).
Only public legal rules and general research belong here. Property-specific
inputs supplied by the owner are deliberately not copied into pages, code or
tables. Unknown or owner-specific values stay blank and are listed on
Flagged for review.

Every data-table row carries at least one official source link. Dollar figures
in narrative and tables are rounded to the nearest $10 unless they are
statutory/agency amounts quoted exactly as published (wrapped in
<span class="stat">). Model outputs are labelled assumption/derived and are
never presented as verified facts.

Run: python3 scripts/build_desk.py
       python3 scripts/verify_safe.py
"""
from pathlib import Path
from html import escape

OUT = Path("public-safe")
AS_OF = "13 November 2026"

SOURCES = {
    "irs_estate": ("IRS · Estate tax", "https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax"),
    "irs_new": ("IRS · Estate and gift tax updates", "https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax"),
    "irs_basis": ("IRS · Basis of inherited property", "https://www.irs.gov/faqs/interest-dividends-other-types-of-income/gifts-inheritances/gifts-inheritances"),
    "irs_706": ("IRS · Form 706 instructions", "https://www.irs.gov/instructions/i706"),
    "irs527": ("IRS · Publication 527, rental property", "https://www.irs.gov/publications/p527"),
    "irs_p523": ("IRS · Publication 523, selling your home", "https://www.irs.gov/publications/p523"),
    "irs_p551": ("IRS · Publication 551, basis of assets", "https://www.irs.gov/publications/p551"),
    "sco": ("California State Controller · Estate tax", "https://www.sco.ca.gov/ardtax_estate_tax.html"),
    "ftb": ("California FTB · Gifts and inheritance", "https://www.ftb.ca.gov/file/personal/income-types/gifts-and-inheritance.html"),
    "boe19": ("California BOE · Proposition 19", "https://www.boe.ca.gov/prop19/"),
    "boe801": ("California BOE · Proposition 19 fact sheet", "https://www.boe.ca.gov/pdf/pub801.pdf"),
    "boe800": ("California BOE · How property is assessed", "https://boe.ca.gov/pdf/pub800-10.pdf"),
    "boe29": ("California BOE · Property tax overview", "https://www.boe.ca.gov/proptaxes/pdf/pub29.pdf"),
    "cdi_home": ("California Department of Insurance · Home insurance", "https://www.insurance.ca.gov/01-consumers/105-type/5-residential/index.cfm"),
    "cdi_market": ("California Department of Insurance · Sustainable Insurance Strategy", "https://www.insurance.ca.gov/01-consumers/180-climate-change/sustainable-insurance-strategy.cfm"),
    "cpuc": ("California Public Utilities Commission · Net energy metering", "https://www.cpuc.ca.gov/nem"),
    "water": ("California Public Utilities Commission · Water", "https://www.cpuc.ca.gov/industries-and-topics/water"),
    "bls": ("U.S. Bureau of Labor Statistics · CPI", "https://www.bls.gov/cpi/"),
    "bls2022": ("BLS · December 2022 CPI release", "https://www.bls.gov/news.release/archives/cpi_01122023.htm"),
    "blshist": ("BLS · Historical CPI-U data", "https://www.bls.gov/cpi/tables/supplemental-files/historical-cpi-u-202402.pdf"),
    "fhfa": ("Federal Housing Finance Agency · House Price Index", "https://www.fhfa.gov/data/hpi"),
    "fed": ("Federal Reserve · Monetary policy", "https://www.federalreserve.gov/monetarypolicy.htm"),
    "usgs": ("U.S. Geological Survey · Earthquake hazards", "https://www.usgs.gov/programs/earthquake-hazards"),
    "courts": ("California Courts · Probate", "https://selfhelp.courts.ca.gov/probate"),
    "leginfo": ("California Legislative Information · Codes", "https://leginfo.legislature.ca.gov/faces/codes.xhtml"),
    "sftreasurer": ("San Francisco Treasurer & Tax Collector · Secured property taxes", "https://sftreasurer.org/property/secured-property-taxes"),
}

NAV = [
    ("index.html", "Dashboard"), ("decision.html", "Decision"),
    ("projections.html", "Projections"), ("properties.html", "Properties"),
    ("costs.html", "Costs"), ("black-swans.html", "Black swans"),
    ("tax.html", "Inheritance & tax"), ("process.html", "Step by step"),
    ("law-watch.html", "Law watch"), ("suggestions.html", "Suggestions"),
    ("qa.html", "Questions & answers"), ("flagged.html", "Flagged for review"),
    ("sources.html", "Sources"),
]

CSS = """
:root{--bg:#f5f7f8;--panel:#fff;--ink:#17242e;--muted:#526371;--line:#dce3e8;--green:#116b5a;--blue:#174b70;--warn:#7a5100;--red:#842b2b;--amber:#b45309}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.58 system-ui,-apple-system,"Segoe UI",sans-serif}
a{color:var(--blue);text-underline-offset:2px}a:hover{color:var(--green)}
header{background:#122331;color:#fff;padding:14px max(20px,calc((100% - 1200px)/2));display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
header a{color:#fff;text-decoration:none;font-weight:700}header span{font-size:12px;color:#c5d3dc;letter-spacing:.07em;text-transform:uppercase}
.layout{max-width:1240px;margin:auto;padding:22px 20px 60px;display:grid;grid-template-columns:220px minmax(0,1fr);gap:24px}
nav{align-self:start;position:sticky;top:12px;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:8px;display:flex;flex-direction:column}
nav a{padding:8px 10px;border-radius:7px;text-decoration:none;color:var(--ink);font-size:14px}
nav a[aria-current=page]{background:#e7f2ef;color:var(--green);font-weight:700}
main{min-width:0}.eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:.12em;color:var(--muted);font-weight:700}
h1{font-size:clamp(27px,4vw,40px);line-height:1.15;margin:.25em 0 .45em}
h2{font-size:22px;margin:2em 0 .5em}
h3{font-size:17px;margin:1.5em 0 .5em}
.lead{font-size:19px;max-width:72ch;color:#344754}
.callout,.notice{padding:15px 18px;border-radius:9px;margin:18px 0;background:#eaf3f0;border:1px solid #c9dfd8;border-left:5px solid var(--green)}
.notice{background:#fff6e2;border-color:#edd8a2;border-left-color:#ba861d}
.bad{background:#fff0f0;border-color:#edcaca;border-left-color:var(--red)}
.sugg{background:#eef6ff;border-color:#c9daef;border-left-color:var(--blue)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(225px,1fr));gap:12px;margin:18px 0}
.card{background:#fff;border:1px solid var(--line);border-radius:9px;padding:14px}
.card b{display:block;color:var(--green);font-size:18px}
.small{font-size:13px;color:var(--muted)}
.scroll{overflow:auto;background:#fff;border:1px solid var(--line);border-radius:9px;margin:14px 0}
table{border-collapse:collapse;width:100%;min-width:620px;font-size:14px}
caption{text-align:left;padding:12px 13px 3px;font-weight:700}
th,td{text-align:left;vertical-align:top;padding:9px 12px;border-bottom:1px solid var(--line)}
thead th{background:#edf2f5;color:#334653;font-size:12px;text-transform:uppercase;letter-spacing:.04em}
tbody tr:nth-child(even){background:#fafcfd}
td a{font-size:12.5px}
.blank{color:#657583;font-style:italic}
.stat{color:var(--green);font-weight:700}
ul li{margin:.35em 0}
.status{font-size:12px;font-weight:700;padding:2px 7px;border-radius:10px;display:inline-block}
.st-proposed{background:#fff3e2;color:#8a5a00}
.st-review{background:#e7f2ef;color:#116b5a}
.st-approved{background:#e7f7ee;color:#1b7a44}
.st-declined{background:#f7e7e7;color:#842b2b}
footer{border-top:1px solid var(--line);margin-top:40px;padding-top:14px;color:var(--muted);font-size:13px}
code{background:#edf1f3;padding:1px 4px;border-radius:4px}
@media(max-width:850px){.layout{grid-template-columns:1fr;padding-top:12px}nav{position:static;flex-direction:row;overflow:auto;gap:3px}nav a{white-space:nowrap}table{min-width:580px}}
"""

def link(key):
    title, url = SOURCES[key]
    return f'<a href="{url}" rel="noopener noreferrer">{escape(title)}</a>'

def table(caption, headers, rows):
    head = "".join(f"<th scope=\"col\">{escape(h)}</th>" for h in headers)
    body = []
    for row in rows:
        cells = list(row)
        if not any("<a " in str(c) for c in cells):
            raise ValueError(f"table row has no official source: {row!r}")
        body.append("<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
    return (f'<div class="scroll"><table><caption>{escape(caption)}</caption><thead><tr>{head}</tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table></div>')

def page(slug, title, eyebrow, body, lead=""):
    nav = "".join(f'<a{" aria-current=page" if target == slug else ""} href="{target}">{escape(label)}</a>' for target, label in NAV)
    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="referrer" content="no-referrer"><title>{escape(title)}</title><link rel="stylesheet" href="style.css"></head><body>
<header><a href="index.html">Estate decision desk</a><span>Public · privacy-first · source checked {AS_OF}</span></header><div class="layout"><nav aria-label="Sections">{nav}</nav><main><div class="eyebrow">{escape(eyebrow)}</div><h1>{escape(title)}</h1>{f'<p class="lead">{lead}</p>' if lead else ''}{body}
<footer><p><strong>Scope.</strong> This public site contains no household names, addresses, ZIP codes, parcel identifiers, household bills, rents, property values, or account details. Property A is the future trust inheritance; Property B is already owned. Those roles are stated without publishing identifying financial inputs.</p><p><strong>Not advice.</strong> Rules and thresholds may change before a future transfer. Confirm the then-current law and obtain legal, tax, insurance, appraisal, and investment advice for the actual estate.</p></footer></main></div></body></html>'''
    (OUT / slug).write_text(doc, encoding="utf-8")

def stat(n):
    """Render a statutory / agency-published exact figure."""
    return f'<span class="stat">${n:,}</span>'

def money(n):
    """Round to nearest $10 for non-statutory display."""
    return f"${int(round(n / 10) * 10):,}"

BLANK = '<span class="blank"></span>'

def build():
    OUT.mkdir(exist_ok=True)
    (OUT / "style.css").write_text(CSS, encoding="utf-8")

    # ---------------------------------------------------------------- index
    body = '''<div class="notice bad"><strong>Executive summary:</strong> No defensible financial winner can be named today from official public sources alone. Property A is expected to arrive through a trust around the 2040&ndash;2050 planning window; Property B is already owned and is <strong>not</strong> part of that inheritance. Treat them as separate tax, operating-cost, and housing decisions.</div>
<div class="grid"><div class="card"><b>Property A &mdash; future inheritance</b>Expected to arrive through a trust around 2040&ndash;2050. Transfer date, trust terms, income-tax basis, current insurance quote, utilities, and rent are not publicly verified here.</div><div class="card"><b>Property B &mdash; already owned</b>Already owned by the future inheritor; it is a separate asset and is not inherited through the trust. Its basis, multi-unit legal status, operating costs, and rental economics require separate review.</div><div class="card"><b>Key distinction</b>Inherited property (A) generally receives a date-of-death stepped-up basis and may qualify for the Prop 19 family transfer; already-owned property (B) keeps its existing basis and receives no step-up from this inheritance.</div><div class="card"><b>Known current federal rule</b>For 2026 the federal basic estate-tax exclusion is <span class="stat">$15,000,000</span> per decedent. It is an estate-level calculation, not a per-heir income-tax-free cash allowance.</div></div>
<h2>Recommended decision sequence</h2><ol>
<li><strong>Before transfer</strong> &mdash; establish trust authority, title, estate inclusion, basis records, family eligibility, and current law.</li>
<li><strong>At transfer</strong> &mdash; obtain a date-of-death valuation and determine Prop 19 eligibility, deadlines, and the property-tax outcome for A.</li>
<li><strong>Compare options for A</strong> &mdash; occupying, renting, and selling, using actual quotes, the actual local tax bill, defensible rent, reserves, and after-tax investment alternatives.</li>
<li><strong>Hold B separately</strong> &mdash; keep B's ownership, existing tenants, housing use, tax basis, and repair obligations in a separate ledger; do not treat A's inheritance as B being inherited.</li>
<li><strong>Review suggestions first</strong> &mdash; use the Suggestions page to compare candidate actions and choose a path before implementing any change.</li>
</ol>
<p>As a provisional strategy&mdash;not a numeric recommendation&mdash;avoid committing to A before verifying the trust and tax treatment. The verified rules below describe current law, not 2040&ndash;2050 law.</p>'''
    page("index.html", "A disciplined inheritance decision", "Executive summary", body,
         "Separate the future inherited home from the already-owned rental property; use official rules, protect private figures, and delay irreversible choices until verified transfer facts exist.")

    # ---------------------------------------------------------------- decision
    body = table("Decision framework &mdash; numeric cells are illustrative assumptions, not verified facts",
        ["Path for A", "What decides it", "Illustrative outcome lens", "Official source"],
        [
            ("Occupy A", "Personal preference; principal-residence and family-transfer eligibility; post-transfer carrying costs; value of housing already supplied by B.",
             "Total cost of ownership (tax + insurance + utilities + maintenance) vs. the market rent you would otherwise pay. Qualifies only if Prop 19 eligibility and occupancy rules are met.", link("boe19")),
            ("Rent A", "Lawful rentable configuration; market rent; vacancy; management; insurance; maintenance; property tax after transfer; income-tax treatment.",
             "Annual after-tax net cash flow = gross rent &minus; vacancy &minus; operating costs &minus; property tax &minus; management. Cannot be ranked without verified rent, legal status, insurance, tax bill, and repair budget.", link("boe19") + " &middot; " + link("leginfo")),
            ("Sell A", "Trust authority; basis; date-of-death value; selling costs; tax on post-transfer gain; reinvestment risk and tax.",
             "After-tax investable proceeds = sale price &minus; selling costs &minus; tax on gain above stepped-up basis. Compare against holding alternatives.", link("irs_basis")),
            ("Continue holding B", "Existing ownership and basis; actual rental records; legal unit status; current debt, tax, insurance and maintenance.",
             "Analyse separately. A's inheritance is not treated as B being inherited; B's two rented units and one vacant unit are valued on their own records.", link("irs_basis") + " &middot; " + link("boe800")),
        ])
    body += '''<div class="callout"><strong>Decision rule:</strong> estimate annual after-tax net cash flow for rent, total cost of ownership for occupancy, and after-tax investable proceeds for sale. Then stress each option under inflation, insurance shocks, interest-rate changes, and home-price declines. Do not compare gross rent with sale proceeds.</div>
<h3>Break-even principle (illustrative)</h3>
<p>For a reference property, holding as a rental beats selling when the net rental yield (after tax, insurance, maintenance, management and vacancy) exceeds the after-tax reinvestment yield from the sale proceeds. Because every input is property-specific, no break-even figure is published here; compute it from verified quotes and the actual secured tax bill at transfer time. See the generic formulas in <code>scripts/desk_model.py</code>.</p>'''
    page("decision.html", "Occupy, rent, or sell", "Decision framework", body,
         "No option is declared the winner without verifiable property-specific inputs. Use the same time horizon, housing assumptions, tax treatment and risk measure for every alternative.")

    # ---------------------------------------------------------------- projections
    years = ["2026", "2040", "2045", "2050", "2060", "2070"]
    rows = [(y, BLANK, BLANK, BLANK, link("fhfa") + " &middot; " + link("boe800")) for y in years]
    body = ('<div class="notice">Property-specific value and tax projection cells are intentionally blank. Future home prices, tax-rate-area charges, trust terms, transfer timing, and future law cannot be verified from today\'s official sources. This avoids presenting a made-up forecast as a fact.</div>')
    body += table("Property-specific projections: unverified cells remain blank",
        ["Year", "Market value", "Taxable / assessed value", "Property tax", "Official references"], rows)
    body += '''<h2>Reproducible method for future use (assumptions, not forecasts)</h2><ul>
<li>Market-value scenario: verified transfer-year baseline &times; (1 + named annual growth assumption)<sup>years</sup>. Show several growth paths; do not call one a forecast.</li>
<li>California taxable value: start from the assessor's factored base-year value; Proposition 13 generally limits annual assessed-value inflation adjustments to 2%, but ownership change and exclusions can alter the result.</li>
<li>Transfer: apply the Prop 19 family-home rules only if transferor/transferee, principal-residence, filing and timing requirements are met.</li>
<li>Annual tax: actual taxable value &times; the actual tax-rate-area levy, plus applicable direct assessments. Use the secured bill, not a countywide proxy.</li>
</ul>
<h3>Illustrative calculation skeleton (rounded to the nearest $10; enter your own verified inputs)</h3>
<p>All cells below are generic illustrations, not Property A or Property B figures.</p>'''
    body += table("Illustrative arithmetic only &mdash; replace with verified inputs at transfer",
        ["Item", "Formula (illustrative)", "Status", "Reference"],
        [
            ("Future market value", "transfer-year value &times; (1 + growth assumption)<sup>years since transfer</sup>", "assumption", link("fhfa")),
            ("Taxable value under Prop 13 (no reassessment)", "prior taxable value &times; 1.02, capped; enroll lower of factored base-year value or market value", "assumption / rule", link("boe800")),
            ("Taxable value if reassessed at transfer", "market value at change of ownership", "assumption / rule", link("boe800")),
            ("Annual property tax", "taxable value &times; actual tax-rate-area levy + direct assessments", "assumption", link("boe29") + " &middot; " + link("sftreasurer")),
            ("Prop 19 value limit (family transfer)", "current taxable value + inflation-adjusted $1,000,000 allowance", "rule", link("boe19") + " &middot; " + link("boe801")),
        ])
    body += '''<h3>Illustrative reference projection (assumption only &mdash; not Property A or B)</h3>
<p>Compounds a <span class="stat">$1,000,000</span> transfer-year reference value at three named annual growth assumptions. All figures rounded to the nearest $10; not a forecast and not the owner's property.</p>'''
    _fhfa = link("fhfa")
    body += table("Market value of a $1,000,000 reference home under three growth assumptions (rounded to nearest $10)",
        ["Years after transfer", "3% per year", "4% per year", "5% per year", "Source"],
        [
            ("0", "$1,000,000", "$1,000,000", "$1,000,000", _fhfa),
            ("5", "$1,159,270", "$1,216,650", "$1,276,280", _fhfa),
            ("10", "$1,343,920", "$1,480,240", "$1,628,900", _fhfa),
            ("15", "$1,557,970", "$1,800,940", "$2,078,930", _fhfa),
            ("20", "$1,806,110", "$2,191,120", "$2,653,300", _fhfa),
            ("25", "$2,093,780", "$2,665,840", "$3,386,360", _fhfa),
        ])
    body += '''<p class="small">Generic calculation helpers in the repository contain no household values. They do not output a property forecast without verified inputs.</p>'''
    body += table("Projection inputs to verify at the time of transfer",
        ["Input", "Required evidence", "Value in public report", "Reference"],
        [
            ("Transfer date and trust distribution authority", "Trust instrument and trustee determination", BLANK, link("courts")),
            ("Date-of-death fair market value and income-tax basis", "Qualified valuation and estate basis documents", BLANK, link("irs_basis")),
            ("Factored base-year value, tax rate area, direct assessments", "Current assessor record and secured tax bill", BLANK, link("boe800") + " &middot; " + link("boe29")),
            ("Prop 19 eligibility and exclusion allowance", "Transferor/transferee eligibility, residence and timely claims", BLANK, link("boe19")),
        ])
    page("projections.html", "Year-by-year projections", "Projection worksheet", body)

    # ---------------------------------------------------------------- properties
    body = table("What is known without publishing personal financial information",
        ["Asset", "Status", "Property-specific value / tax", "Verification"],
        [
            ("Property A", "Expected trust inheritance around the stated future planning window; trust terms and transfer date are unknown.", BLANK, link("irs_estate") + " &middot; " + link("boe19")),
            ("Property B", "Already owned by the future inheritor; multi-unit use and rental arrangements require current documentation.", BLANK, link("boe800") + " &middot; " + link("leginfo")),
        ])
    body += '''<h2>Privacy and verification boundary</h2><p>Owner-provided estimates, assessment histories, rent receipts, utility costs, and insurance estimates are not reproduced here. They cannot be independently confirmed through a public official source in a way that establishes the facts for these specific properties. The locations are intentionally not named. See <a href="flagged.html">Flagged for review</a> for the evidence categories that remain open.</p>'''
    page("properties.html", "Property facts and unknowns", "Properties", body)

    # ---------------------------------------------------------------- costs
    body = table("Operating-cost items &mdash; property-specific amounts are not verified",
        ["Cost", "Published benchmark", "Why not a property quote", "Official reference"],
        [
            ("Statewide homeowners-premium benchmark (not a local quote)", stat(1571) + " per year average (CDI, rounded to " + money(1571) + " for display)", "A statewide average is not a quote, does not establish replacement cost, and may not represent this home's primary-residence or landlord coverage.", link("cdi_market")),
            ("Home insurance for A (future primary residence or rental)", BLANK, "Premium depends on occupancy, replacement cost, coverage, claims, wildfire exposure and underwriting; obtain current written quotes.", link("cdi_home") + " &middot; " + link("cdi_market")),
            ("Rental-property insurance for B", BLANK, "Coverage for multiple units and owner occupancy must be confirmed with insurers.", link("cdi_home")),
            ("Water and sewer", BLANK, "Use actual account bills and current provider tariff; meter count, occupancy and conservation charges matter.", link("water")),
            ("Electricity and solar export credit", BLANK, "Need meter records, tariff, system ownership and confirmation whether existing interconnection terms transfer.", link("cpuc")),
            ("Repairs, maintenance and capital reserve", BLANK, "No inspection, age/condition report, contractor bids or unit-level history was reviewed.", link("boe800")),
            ("Rental operating costs", BLANK, "Requires lawful unit count, actual leases, vacancy, management, taxes, insurance, utilities and repairs.", link("leginfo") + " &middot; " + link("ftb")),
        ])
    body += '''<div class="notice"><strong>Insurance planning:</strong> do not substitute a statewide average for a property quote. Confirm replacement cost and policy form, and separately test nonrenewal, deductible increases, FAIR Plan availability, and required wrap-around coverage.</div>'''
    page("costs.html", "Insurance, utilities and repairs", "Operating costs", body)

    # ---------------------------------------------------------------- black swans
    body = table("Stress regimes &mdash; uneven economy over a 50-year horizon",
        ["Regime", "What to shock", "Why it matters", "Official historical / monitoring source"],
        [
            ("Historic inflation flare-up / stagflation", "BLS annual-average CPI inflation was 13.5% in 1980. Stress several years of high inflation with weak real growth; raise insurance, water, repairs and other costs separately.",
             "A high-inflation episode is documented; do not assume all household costs or home values rise at the same rate.", link("blshist") + " &middot; " + link("fed")),
            ("Recent inflation and utility-cost shock", "BLS reported 12-month CPI inflation of 6.5% and electricity inflation of 14.3% through December 2022. Stress headline inflation and electricity separately.",
             "One smooth inflation rate can understate uneven costs; solar credits and tariffs are property-specific.", link("bls2022") + " &middot; " + link("cpuc")),
            ("Interest-rate and liquidity shock", "Test higher borrowing costs, lower bond/stock values and delayed sale timing.",
             "A sale-and-reinvest plan can suffer sequence risk; borrowing and buyer demand also change.", link("fed")),
            ("Housing drawdown and slow recovery", "Apply a sharp nominal home-price fall, a multi-year flat period, then recovery; test transaction costs.",
             "Averages conceal long drawdowns and local outcomes differ from national indexes.", link("fhfa")),
            ("Insurance availability / premium shock", "Test higher premiums, larger deductibles, reduced coverage or inability to obtain standard coverage.",
             "Insurance cost and availability can dominate carrying costs and affect saleability.", link("cdi_market")),
            ("Seismic / disaster event", "Model repair, temporary housing, insurance limits, special assessments and delayed rebuilding.",
             "Physical loss can interact with insurance markets, rents, utilities and sale timing.", link("usgs") + " &middot; " + link("cdi_home")),
            ("Long low-return period", "Use a prolonged low real return and poor early sequence for a diversified portfolio.",
             "A fixed average return is not a safe proxy for the order of returns.", link("fed") + " &middot; " + link("bls")),
        ])
    body += '''<h2>How to use the scenarios</h2>
<p>Growth and inflation are never constant over 50 years. For each regime, vary one factor and then combine correlated shocks (for example, high inflation together with an insurance premium shock and a flat housing market). Keep nominal and inflation-adjusted results separate. Compare the same horizon and include taxes, transaction costs, vacancy, capital spending and the value of housing. No single black-swan scenario is assigned a probability or presented as a prediction.</p>
<h3>Baseline projection convention (assumption &mdash; not a forecast)</h3>
<p>Project market value forward from a verified transfer-year baseline using a named annual growth rate, and project taxable value under Proposition 13's 2% annual cap unless a change of ownership triggers reassessment. Run the same calculation under several growth paths (for example, lower-than-average, typical, higher-than-average) so the decision does not rest on one number. Property-specific cells are blank and must be filled from verified inputs at transfer time.</p>'''
    page("black-swans.html", "Black-swan and uneven-economy scenarios", "Stress testing", body)

    # ---------------------------------------------------------------- tax
    body = table("Current inheritance and property-tax rules checked against official sources",
        ["Rule", "Current statement", "Scope / caveat", "Official source"],
        [
            ("Federal estate-tax exclusion", 'For 2026, the federal basic exclusion amount is ' + stat(15000000) + ' per decedent.', "Estate-level calculation; not a separate per-heir inheritance allowance. Estate composition, deductions, prior taxable gifts and elections matter. Future amounts must be rechecked.", link("irs_estate") + " &middot; " + link("irs_new")),
            ("Federal estate tax rate", "The top federal estate-tax rate is 40% on the taxable estate above the exclusion.", "Applies only if the taxable estate exceeds the exclusion; most simple estates do not require a Form 706 filing.", link("irs_estate") + " &middot; " + link("irs_706")),
            ("No federal inheritance tax", "There is no federal tax on the person who receives an inheritance.", "The estate tax (if any) is paid by the estate before distribution; the heir's receipt is not income.", link("irs_estate")),
            ("California estate tax", "California requires no estate-tax return for decedents dying on or after 1 January 2005.", "This does not eliminate federal estate tax or income tax on later income/gain.", link("sco")),
            ("California inheritance receipt", "California FTB: a gift or inheritance is not included in the recipient's income; income it later produces is taxable.", "Rental income, interest, dividends and taxable gain are distinct from receipt of the inheritance.", link("ftb")),
            ("Inherited income-tax basis", "Generally, basis is fair market value on the date of death; alternate valuation and consistent-basis rules can apply.", "A sale near basis is not automatically tax-free: valuation, trust/estate inclusion, later appreciation and expenses matter.", link("irs_basis") + " &middot; " + link("irs_706")),
            ("California parent-child property-tax exclusion", "Current Prop 19 rules require an eligible family transfer and principal-residence requirements; value above the adjusted limit can increase taxable value.", "Claim timing and eligibility are critical; no exclusion for other real property under the current rule. Verify the applicable-year adjusted allowance.", link("boe19") + " &middot; " + link("boe801")),
            ("Prop 19 value allowance", 'The family-transfer value limit is current taxable value plus the inflation-adjusted ' + stat(1000000) + ' allowance.', "Applies to the family home/farm when transferor and transferee each use it as their principal residence and claims are timely.", link("boe19") + " &middot; " + link("boe801")),
            ("Home-sale exclusion (&sect;121)", "Up to $250,000 ($500,000 married filing jointly) of gain on the sale of a principal residence may be excluded, subject to ownership and use tests.", "Exclusion can generally be used once every two years; does not apply to rental or second-home portions.", link("irs_p523")),
            ("Capital gains on inherited property", "Gain is measured against the stepped-up (date-of-death) basis; only post-transfer appreciation is taxable.", "Later depreciation and selling expenses affect the calculation; keep records.", link("irs_basis") + " &middot; " + link("irs_p551")),
            ("Property-tax assessment", "California assessed value is generally subject to a 2% annual inflation cap; the base rate is generally 1% plus voter-approved bonded debt, with reassessment on change of ownership.", "The actual bill also depends on local tax-rate area and direct assessments; no property-specific amount is published here.", link("boe800") + " &middot; " + link("boe29")),
        ])
    body += '''<p class="small">As of this review, the IRS lists the 2026 threshold. A 2040&ndash;2050 threshold is not stated as a forecast: inflation indexing and future legislation make a long-range dollar value uncertain.</p>'''
    page("tax.html", "Inheritance, estate and property tax", "Tax rules", body)

    # ---------------------------------------------------------------- process
    body = table("Practical sequence for a trust-held inherited home",
        ["Step", "Action / evidence", "Why it matters", "Official source"],
        [
            ("1 &middot; Identify authority", "Confirm trust instrument, successor trustee, distribution powers, debts, title and beneficiaries.", "A beneficiary may not be able to sell, occupy or lease before distribution or trustee approval.", link("courts")),
            ("2 &middot; Inventory estate", "Document assets, liabilities, ownership, trust status, lifetime gifts, marital status and possible filing obligations.", "Federal estate tax uses the gross estate, deductions, adjusted taxable gifts and elections&mdash;not the value of one home alone.", link("irs_estate") + " &middot; " + link("irs_706")),
            ("3 &middot; Establish basis and value", "Obtain date-of-death valuation and retain basis, appraisal, improvement, expense and any estate-return documentation.", "Basis affects tax on later sale and must be supported by records.", link("irs_basis")),
            ("4 &middot; Protect Prop 19 deadlines", "Check family eligibility, principal-residence occupancy and submit required homeowner/exclusion claims within current deadlines.", "Current BOE guidance describes a one-year homeowner-exemption filing period and a three-year exclusion claim period, subject to details and exceptions.", link("boe19") + " &middot; " + link("boe801")),
            ("5 &middot; Secure property and operations", "Bind appropriate insurance, confirm utilities, inspect condition, preserve leases and comply with local rental/habitability rules.", "Coverage and legal status cannot be assumed to continue unchanged through transfer.", link("cdi_home") + " &middot; " + link("leginfo")),
            ("6 &middot; Compare options after verification", "Build occupy / rent / sell cases from actual taxes, quotes, rental evidence, sale costs, income-tax basis and portfolio risks.", "Avoid using gross rent, unsupported insurance or a countywide proxy as net economic value.", link("ftb") + " &middot; " + link("irs_basis")),
            ("7 &middot; Recheck law and file", "Confirm federal and state law, forms, transfer recording, tax bills and insurance requirements for the actual transfer year.", "A transfer expected decades out cannot be safely administered from current rules alone.", link("irs_new") + " &middot; " + link("boe19")),
        ])
    page("process.html", "Trust inheritance: step by step", "Transfer process", body)

    # ---------------------------------------------------------------- law watch
    body = table("Monitoring &mdash; no future legal change is assumed in the model",
        ["Topic to monitor", "Current position", "Recheck trigger", "Official source"],
        [
            ("Federal estate and gift tax", "2026 federal estate-tax exclusion is $15,000,000; the law in the future transfer year controls.", "Each annual IRS update and any enacted federal tax legislation.", link("irs_new") + " &middot; " + link("irs_estate")),
            ("California Prop 19", "Current exclusions, adjusted value limit, eligibility and claim deadlines are described by BOE.", "Before transfer, claim, move-in, sale or third-party transfer; check statutory and BOE updates.", link("boe19") + " &middot; " + link("leginfo")),
            ("Property-tax rate and assessment", "Tax-rate-area levies, assessments, direct charges and reassessment rules vary by parcel and year.", "Annual secured tax bill and assessor notice; not replaced by a general projection.", link("boe29") + " &middot; " + link("boe800")),
            ("Insurance market", "Availability, underwriting and premium conditions change; state market conditions are not a property quote.", "Annual renewal, nonrenewal notice, ownership/occupancy change or insurer-market disruption.", link("cdi_market") + " &middot; " + link("cdi_home")),
            ("Rent, utilities and solar", "Applicable rent rules, utility tariffs and solar compensation depend on law, provider, equipment and contract.", "At transfer and whenever a lease, tariff or ownership changes.", link("leginfo") + " &middot; " + link("cpuc") + " &middot; " + link("water")),
        ])
    body += '''<p>Proposed bills are not treated as law. This page does not make claims about pending proposals unless a primary source confirms their status. Re-run the decision model using enacted law at the time of transfer.</p>'''
    page("law-watch.html", "Law and policy watch", "Monitoring", body)

    # ---------------------------------------------------------------- suggestions (NEW)
    body = table("Suggestions &mdash; review and choose a path before implementing any change",
        ["#", "Suggestion", "Why it matters", "Owner decision needed", "Official reference", "Status"],
        [
            ("S-1", "Obtain current written insurance quotes for Property A (primary-residence and landlord forms) before deciding to occupy or rent.", "Premium can dominate carrying costs and may differ sharply from any estimate; insurability affects both options and the sale price.", "Choose insurer, coverage amount and deductible; budget the quoted premium.", link("cdi_home"), '<span class="status st-proposed">Proposed</span>'),
            ("S-2", "Verify Prop 19 eligibility for Property A (both parties principal residence, one-year move-in, timely claims) before the transfer.", "Determines whether A keeps a low taxable value or is reassessed to full market value at transfer&mdash;the single largest tax lever.", "Confirm eligibility with the assessor and file required claims on time.", link("boe19"), '<span class="status st-proposed">Proposed</span>'),
            ("S-3", "Obtain a date-of-death appraisal and document the stepped-up income-tax basis for Property A.", "Basis sets the tax on any later sale and must be supported by records.", "Engage a qualified appraiser at transfer; retain all basis documentation.", link("irs_basis"), '<span class="status st-proposed">Proposed</span>'),
            ("S-4", "Confirm the lawful unit status and rental compliance of Property B (3 units; 2 rented, 1 vacant).", "Renting a non-conforming unit creates legal and financial risk; the vacant unit is a separate decision from the rented units.", "Review permits, local rental ordinance and lease records before acting on B's vacant unit.", link("leginfo"), '<span class="status st-proposed">Proposed</span>'),
            ("S-5", "Compare net, not gross, outcomes: after-tax cash flow for rent, total cost of ownership for occupancy, after-tax proceeds for sale.", "Gross rent ignores vacancy, tax, insurance, management and repairs; comparing it to sale proceeds is misleading.", "Adopt a common horizon, tax treatment and risk measure for all three options.", link("irs_basis"), '<span class="status st-review">Under review</span>'),
            ("S-6", "Stress-test each option under black-swan regimes (inflation, insurance shock, housing drawdown, interest rates) over the holding horizon.", "Growth and inflation are never constant over 50 years; a single average can hide ruinous sequences.", "Decide how much downside risk each option can tolerate before choosing.", link("fhfa"), '<span class="status st-proposed">Proposed</span>'),
            ("S-7", "Do not implement any change to A or B until transfer facts (title, basis, tax bill, insurance, legal unit status) are verified.", "Irreversible choices made on unverified inputs can create large, avoidable tax and cost consequences.", "Owner sign-off on the verified fact base before acting on any suggestion.", link("irs_basis"), '<span class="status st-review">Under review</span>'),
            ("S-8", "Set aside a capital reserve for repairs and maintenance (a percentage of value per year) for whichever property is held.", "Regular maintenance and capital items are unavoidable and grow with the property.", "Choose reserve percentage and funding source.", link("boe800"), '<span class="status st-proposed">Proposed</span>'),
            ("S-9", "Re-check the federal estate-tax exclusion and California rules at the transfer year, not today.", "The 2026 exclusion is indexed and legislation can change; a 2040&ndash;2050 transfer uses then-current law.", "Calendar a review well before the expected transfer.", link("irs_new"), '<span class="status st-proposed">Proposed</span>'),
            ("S-10", "If Prop 19 is unavailable for A, seriously compare selling at transfer and reinvesting the after-tax proceeds.", "Reassessment to full market value can make holding expensive relative to reinvestment.", "Compare after-tax sale proceeds against projected holding costs and appreciation.", link("boe19"), '<span class="status st-proposed">Proposed</span>'),
        ])
    body += '''<div class="callout sugg"><strong>How to use this page:</strong> each suggestion is a candidate action with its rationale, the owner decision it requires, and a status. Review the list, move items between Proposed &rarr; Under review &rarr; Approved / Declined, and implement only Approved items&mdash;and only after the transfer facts in the Process page are verified. No suggestion is a recommendation to act; each requires property-specific verification first.</div>'''
    page("suggestions.html", "Suggestions", "Review suggestions before implementing", body,
         "A dedicated place to list, review, and choose among suggested actions before any change is made to either property.")

    # ---------------------------------------------------------------- Q&A (NEW)
    body = table("Questions, information needed, and answers &mdash; what must be settled before a decision",
        ["#", "Question", "Information needed", "Answer (current, where known)", "Status", "Official source"],
        [
            ("Q-1", "What is the federal estate-tax threshold before tax is due?", "Gross estate plus adjusted taxable gifts for the year of death.", "For 2026 the federal basic exclusion is " + stat(15000000) + " per decedent; the top estate-tax rate above it is 40%. A 2040&ndash;2050 figure is not a forecast.", '<span class="status st-review">Verified for 2026</span>', link("irs_estate")),
            ("Q-2", "Is there a California estate or inheritance tax?", "Date of death and California law.", "No California estate-tax return for deaths on or after 1 January 2005; California has no inheritance tax; an inheritance is not income to the recipient.", '<span class="status st-review">Verified</span>', link("sco") + " &middot; " + link("ftb")),
            ("Q-3", "Does the heir pay income tax on receiving the inheritance?", "Nature of the bequest and later income it produces.", "No. The inheritance itself is not income; later income it produces (rent, interest, gain on sale) is taxable.", '<span class="status st-review">Verified</span>', link("ftb")),
            ("Q-4", "What is the income-tax basis of an inherited home?", "Date-of-death fair market value and estate documentation.", "Generally the date-of-death fair market value (stepped-up basis); alternate valuation and consistent-basis rules can apply.", '<span class="status st-review">Verified</span>', link("irs_basis")),
            ("Q-5", "Does Prop 19 let the family home keep a low taxable value after transfer?", "Transferor/transferee eligibility, principal-residence use, filing deadlines, value limit.", "Yes, only if both parties use it as their principal residence and claims are timely; value above current taxable value plus the adjusted $1,000,000 allowance increases taxable value.", '<span class="status st-review">Verified; eligibility unconfirmed for A</span>', link("boe19")),
            ("Q-6", "What happens to property tax if Prop 19 does not apply?", "Assessed value at change of ownership.", "The property is generally reassessed to market value on change of ownership, raising the taxable value and tax bill.", '<span class="status st-review">Verified</span>', link("boe800")),
            ("Q-7", "Can we live in A and keep B rented at the same time?", "Ownership, legal unit status, and occupancy of each property.", "Yes&mdash;they are separate decisions. A's inheritance is not treated as B being inherited; B's rented and vacant units are evaluated on their own records.", '<span class="status st-review">Verified framework</span>', link("irs_basis") + " &middot; " + link("boe800")),
            ("Q-8", "What are the inheritance thresholds and how much headroom before tax?", "Estate size (all assets), lifetime taxable gifts, exclusions and elections.", "Federal: exclusion plus deductions determine taxable estate. California: none (post-2005 deaths). Headroom must be computed from the full estate, not one home.", '<span class="status st-unverified">Estate size unknown</span>', link("irs_estate") + " &middot; " + link("irs_706")),
            ("Q-9", "What will A be worth and what will its tax be at transfer?", "Transfer date, market value, assessed value, tax-rate area, Prop 19 outcome.", "Cannot be known now. Project from a verified transfer-year baseline using named growth assumptions; tax from the actual secured bill.", '<span class="status st-unverified">Future values unknown</span>', link("fhfa") + " &middot; " + link("boe800")),
            ("Q-10", "What does it cost to hold A (insurance, water, electricity, repairs)?", "Current quotes, utility tariffs, inspection, contractor bids.", "Owner-supplied estimates are not verified; obtain current written quotes before relying on any figure.", '<span class="status st-unverified">Quotes needed</span>', link("cdi_home") + " &middot; " + link("water") + " &middot; " + link("cpuc")),
            ("Q-11", "Which path&mdash;occupy, rent, or sell A&mdash;is best?", "Verified tax, insurance, rent, maintenance, sale costs, portfolio alternatives, and risk tolerance.", "No defensible winner from public sources alone; compute net after-tax outcomes under the same horizon and stress each option.", '<span class="status st-unverified">Cannot rank yet</span>', link("irs_basis") + " &middot; " + link("boe19")),
        ])
    body += '''<div class="callout"><strong>How to use this page:</strong> the right-hand column shows whether each item is verified from an official source, under review, or unverified. Items marked unverified are exactly the information that must be discovered before a decision can reasonably be made. Treat every answer as current law only; re-check at the time of transfer.</div>'''
    page("qa.html", "Questions & answers", "Questions, information and answers", body)

    # ---------------------------------------------------------------- flagged
    body = table("Items that cannot be independently verified and are intentionally not published",
        ["Open item", "Public value", "Why unresolved", "Official reference"],
        [
            ("Property-specific market value, tax assessments and tax bills", BLANK, "Private/identifying household facts; public records do not establish which records belong to the described household.", link("boe800")),
            ("Local tax-rate area and municipal rules", BLANK, "A specific tax-rate area, rental ordinance, utility tariff or permitted unit configuration cannot be matched without naming the parcel.", link("boe29") + " &middot; " + link("leginfo")),
            ("Trust text, transfer date, estate inclusion and authority", BLANK, "Private documents were not reviewed; no assumption is made about ownership or trustee power.", link("irs_estate") + " &middot; " + link("courts")),
            ("Property A or B rent and lawful unit status", BLANK, "Lease records and permits are not independently available; no rental projection is presented as verified.", link("leginfo")),
            ("Rental-income tax, depreciation and tax on a later sale", BLANK, "Rental income, deductible costs, depreciation, passive-loss rules and recapture depend on basis and taxpayer facts.", link("irs527") + " &middot; " + link("irs_basis")),
            ("Housing-use tradeoff between A and B", BLANK, "The household-specific use and rent alternative for the already-owned property has not been valued; options are not represented as housing-equivalent.", link("irs527")),
            ("Insurance premiums and insurability", BLANK, "Only an insurer can quote specific coverage after underwriting.", link("cdi_home") + " &middot; " + link("cdi_market")),
            ("Water, electricity, solar credits and repairs", BLANK, "No utility account history, tariff contract, inspection or contractor quote was reviewed.", link("water") + " &middot; " + link("cpuc")),
            ("Future tax threshold, rates and rules", BLANK, "A transfer decades away depends on future legislation, inflation indexing and jurisdictional rates.", link("irs_new") + " &middot; " + link("boe19")),
        ])
    body += '''<div class="callout bad"><strong>Privacy notice:</strong> exact and rounded owner-supplied financial details are omitted from the deployed site. Owner-supplied figures are for internal use only and must not appear on the website. Older public Git history and caches may retain prior figures; excluding legacy files from this release does not erase them. Repository cleanup, visibility changes, or history rewriting require the repository owner's decision.</div>'''
    page("flagged.html", "Flagged for review", "Open evidence gaps", body)

    # ---------------------------------------------------------------- sources
    rows = []
    descriptions = {
        "irs_estate": "Federal estate tax framework and year-of-death filing threshold.",
        "irs_new": "Enacted federal tax updates; current and future law monitoring.",
        "irs_basis": "General basis rules for inherited property and later sale.",
        "irs_706": "Estate return instructions, elections and reporting.",
        "irs_p523": "Home-sale exclusion rules (section 121).",
        "irs_p551": "Basis of assets, including inherited property.",
        "irs527": "Rental income, expenses, repairs and depreciation rules.",
        "sco": "California estate-tax status.",
        "ftb": "California income treatment of gifts and inheritances.",
        "boe19": "California Proposition 19 rules and filing requirements.",
        "boe801": "BOE's Prop 19 fact sheet and eligibility details.",
        "boe800": "Assessment and change-in-ownership background.",
        "boe29": "Property tax overview and local bill components.",
        "cdi_home": "Residential insurance shopping and consumer guidance.",
        "cdi_market": "California insurance-market conditions and reforms.",
        "cpuc": "California net energy metering and billing context.",
        "water": "Water-rate information and conservation portal.",
        "bls": "Consumer Price Index program and inflation context.",
        "bls2022": "BLS December 2022 release: 12-month CPI and electricity changes.",
        "blshist": "Historical CPI-U series for earlier inflation episodes.",
        "fhfa": "House price index data and methodology.",
        "fed": "Federal Reserve policy context and releases.",
        "usgs": "Earthquake hazard information.",
        "courts": "California probate process overview.",
        "leginfo": "California statutes and legislative code database.",
        "sftreasurer": "San Francisco secured property-tax rate and reassessment practice.",
    }
    for key, description in descriptions.items():
        rows.append((link(key), escape(description), "Official primary source"))
    body = table("Official references used in this release", ["Source", "Use in this site", "Status"], rows)
    body += '''<p class="small">The linked official primary sources were retrieved and reviewed for this release. Each source supports only the rule or historical fact described; it does not certify any private property fact. Every data row on this site has at least one official source link.</p>'''
    page("sources.html", "Official sources", "Source register", body)

    # HTML files are composed above once each. Ensure all expected routes exist.
    expected = {slug for slug, _ in NAV}
    for slug in expected:
        if not (OUT / slug).exists():
            raise RuntimeError(f"missing page: {slug}")
    print(f"built {len(expected)} privacy-safe pages in {OUT}/")


if __name__ == "__main__":
    build()
