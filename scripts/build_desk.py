#!/usr/bin/env python3
"""Build the privacy-safe, source-linked inheritance decision desk.

Only public legal rules and general research belong in the artifact. Property-specific
inputs supplied in conversation are deliberately not copied into pages, code or tables.
Unknown or owner-specific values stay blank and are listed on Flagged for review.
"""
from pathlib import Path
from html import escape

OUT = Path("public-safe")
AS_OF = "12 November 2026"

SOURCES = {
    "irs_estate": ("IRS · Estate tax", "https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax"),
    "irs_new": ("IRS · Estate and gift tax updates", "https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax"),
    "irs_basis": ("IRS · Basis of inherited property", "https://www.irs.gov/faqs/interest-dividends-other-types-of-income/gifts-inheritances/gifts-inheritances"),
    "irs_706": ("IRS · Form 706 instructions", "https://www.irs.gov/instructions/i706"),
    "irs527": ("IRS · Publication 527, rental property", "https://www.irs.gov/publications/p527"),
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
}

NAV = [
    ("index.html", "Dashboard"), ("decision.html", "Decision"),
    ("suggestions.html", "Suggestions"),
    ("questions-answers.html", "Questions & answers"),
    ("projections.html", "Projections"), ("properties.html", "Properties"),
    ("costs.html", "Costs"), ("black-swans.html", "Black swans"),
    ("tax.html", "Inheritance & tax"), ("process.html", "Step by step"),
    ("law-watch.html", "Law watch"), ("flagged.html", "Flagged for review"),
    ("sources.html", "Sources"),
]

CSS = """
:root{--bg:#f5f7f8;--panel:#fff;--ink:#17242e;--muted:#526371;--line:#dce3e8;--green:#116b5a;--blue:#174b70;--warn:#7a5100;--red:#842b2b}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.58 system-ui,-apple-system,"Segoe UI",sans-serif}
a{color:var(--blue);text-underline-offset:2px}a:hover{color:var(--green)}header{background:#122331;color:#fff;padding:14px max(20px,calc((100% - 1200px)/2));display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}header a{color:#fff;text-decoration:none;font-weight:700}header span{font-size:12px;color:#c5d3dc;letter-spacing:.07em;text-transform:uppercase}.layout{max-width:1240px;margin:auto;padding:22px 20px 50px;display:grid;grid-template-columns:220px minmax(0,1fr);gap:24px}nav{align-self:start;position:sticky;top:12px;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:8px;display:flex;flex-direction:column}nav a{padding:8px 10px;border-radius:7px;text-decoration:none;color:var(--ink);font-size:14px}nav a[aria-current=page]{background:#e7f2ef;color:var(--green);font-weight:700}main{min-width:0}.eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:.12em;color:var(--muted);font-weight:700}h1{font-size:clamp(27px,4vw,40px);line-height:1.15;margin:.25em 0 .45em}h2{font-size:22px;margin:2em 0 .5em}h3{font-size:17px}.lead{font-size:19px;max-width:72ch;color:#344754}.callout,.notice{padding:15px 18px;border-radius:9px;margin:18px 0;background:#eaf3f0;border:1px solid #c9dfd8;border-left:5px solid var(--green)}.notice{background:#fff6e2;border-color:#edd8a2;border-left-color:#ba861d}.bad{background:#fff0f0;border-color:#edcaca;border-left-color:var(--red)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(225px,1fr));gap:12px;margin:18px 0}.card{background:#fff;border:1px solid var(--line);border-radius:9px;padding:14px}.card b{display:block;color:var(--green);font-size:18px}.small{font-size:13px;color:var(--muted)}.scroll{overflow:auto;background:#fff;border:1px solid var(--line);border-radius:9px;margin:14px 0}table{border-collapse:collapse;width:100%;min-width:620px;font-size:14px}caption{text-align:left;padding:12px 13px 3px;font-weight:700}th,td{text-align:left;vertical-align:top;padding:9px 12px;border-bottom:1px solid var(--line)}thead th{background:#edf2f5;color:#334653;font-size:12px;text-transform:uppercase;letter-spacing:.04em}tbody tr:nth-child(even){background:#fafcfd}td a{font-size:12.5px}.blank{color:#657583;font-style:italic}ul li{margin:.35em 0}footer{border-top:1px solid var(--line);margin-top:35px;padding-top:12px;color:var(--muted);font-size:13px}code{background:#edf1f3;padding:1px 4px;border-radius:4px}@media(max-width:850px){.layout{grid-template-columns:1fr;padding-top:12px}nav{position:static;flex-direction:row;overflow:auto;gap:3px}nav a{white-space:nowrap}table{min-width:580px}}
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


def build():
    OUT.mkdir(exist_ok=True)
    (OUT / "style.css").write_text(CSS, encoding="utf-8")

    body = '''<div class="notice"><strong>Executive summary:</strong> No defensible financial winner can be named today from official public sources alone. Property A is expected to arrive through a trust; Property B is already owned and is not part of that inheritance. Treat them as separate tax, operating-cost, and housing decisions.</div>
<div class="grid"><div class="card"><b>Property A</b>Future inheritance through a trust. Actual transfer date, trust terms, tax basis, current insurance quote, utilities, and rent are not publicly verified here.</div><div class="card"><b>Property B</b>Already owned. Its basis, multi-unit legal status, operating costs, and rental economics require separate review and are not altered by assuming A is inherited.</div><div class="card"><b>Known current federal rule</b>For 2026 the federal basic estate-tax exclusion is <strong>$15,000,000</strong> per decedent. It applies to the estate calculation, not as a per-heir income-tax-free cash allowance.</div></div>
<h2>Recommended decision sequence</h2><ol><li>Before transfer: establish trust authority, title, estate inclusion, basis records, family eligibility, and current law.</li><li>At transfer: obtain date-of-death valuation and determine Prop 19 eligibility, deadlines, and property tax outcome.</li><li>Compare occupying, renting, and selling A using actual quotes, actual local tax bill, defensible rent, reserves, and after-tax investment alternatives.</li><li>Keep B's ownership, existing tenants, housing use, tax basis, and repair obligations in a separate ledger.</li></ol>
<p>As a provisional strategy—not a numeric recommendation—avoid committing to A before verifying the trust and tax treatment. Compare holding A as a home, as a rental, and as a sale only after the transfer facts are known. The verified rules below describe current law, not 2040–2050 law.</p>'''
    page("index.html", "A disciplined inheritance decision", "Executive summary", body,
         "Separate the future inherited home from the already-owned rental property; use official rules, protect private figures, and delay irreversible choices until verified transfer facts exist.")

    body = table("Decision matrix — household-specific numeric cells intentionally withheld", ["Path for A", "What decides it", "Current conclusion", "Official source"], [
        ("Occupy A", "Personal preference; principal-residence and family-transfer eligibility; post-transfer costs; value of housing already supplied by B.", "Possible; evaluate only after eligibility, title and actual carrying costs are confirmed.", link("boe19")),
        ("Rent A", "Lawful rentable configuration; market rent; vacancy; management; insurance; maintenance; property tax after transfer; income-tax treatment.", "Cannot rank without verified rent, legal status, insurance, tax bill and repair budget.", link("boe19") + " · " + link("leginfo")),
        ("Sell A", "Trust authority; basis; date-of-death value; selling costs; tax on post-transfer gain; reinvestment risk and tax.", "Compare net proceeds with actual holding alternatives; inherited basis is generally date-of-death FMV, subject to exceptions.", link("irs_basis")),
        ("Continue holding B", "Existing ownership and basis; actual rental records; legal unit status; current debt, tax, insurance and maintenance.", "Analyze separately. A's inheritance is not treated as B being inherited.", link("irs_basis") + " · " + link("boe800")),
    ]) + '''<div class="callout"><strong>Decision rule:</strong> estimate annual after-tax net cash flow for rent, total cost of ownership for occupancy, and after-tax investable proceeds for sale. Then stress each option under inflation, insurance shocks, interest-rate changes, and home-price declines. Do not compare gross rent with sale proceeds.</div>'''
    page("decision.html", "Occupy, rent, or sell", "Decision framework", body,
         "No option is declared the winner without verifiable property-specific inputs. Use the same time horizon, housing assumptions, tax treatment and risk measure for every alternative.")

    body = '''<div class="notice"><strong>Purpose and guardrail:</strong> These are proposed improvements for a reviewer to accept, revise, or defer before implementation. Nothing on this page changes the decision model or asserts a financial winner. Keep property-specific documents and figures in a private, access-controlled working file; publish only anonymized, independently supported conclusions.</div>
<h2>Suggestions for review</h2>''' + table("Proposed actions — reviewer choice is required before implementation", ["Priority", "Suggestion", "Why it improves the decision", "Reviewer choice", "Official reference"], [
        ("1 · Required", "Confirm the trust instrument, trustee authority, title, transfer timing, and whether the assets are included in the taxable estate.", "Determines who can decide, what actually transfers, the applicable filing obligations, and which rules apply. Keep the already-owned Property B in a separate ledger.", "Accept · Revise · Defer", link("irs_estate") + " · " + link("courts")),
        ("2 · Required", "At transfer, obtain a qualified date-of-transfer valuation and preserve the estate / basis records; have a tax professional confirm inherited-basis treatment and any exceptions.", "A sale-versus-hold comparison depends materially on basis and date-specific value; do not assume a private estimate is the tax basis.", "Accept · Revise · Defer", link("irs_basis") + " · " + link("irs_706")),
        ("3 · Required", "Before choosing to occupy or rent the inherited home, check current family-transfer eligibility, principal-residence requirements, claim deadlines, title, and reassessment treatment with the county assessor.", "Property-tax treatment can change the annual holding cost; eligibility is fact-specific and future law may differ.", "Accept · Revise · Defer", link("boe19") + " · " + link("boe801")),
        ("4 · Required", "Compare occupy, rent, and sell using a single after-tax worksheet, and show the already-owned Property B's housing and rental role separately rather than treating it as inherited.", "Prevents comparing gross rent with net sale proceeds and prevents double-counting housing benefits, income, taxes, or costs.", "Accept · Revise · Defer", link("irs527") + " · " + link("irs_basis")),
        ("5 · Before estimating", "Obtain current written insurance quotes for each relevant occupancy and rental configuration; separately verify coverage availability, exclusions, deductible, replacement-cost basis, and renewal terms.", "Statewide averages cannot establish insurability or price for a specific home; insurance shocks can change the hold-versus-sell result.", "Accept · Revise · Defer", link("cdi_home") + " · " + link("cdi_market")),
        ("6 · Before estimating", "Collect bills, solar/interconnection terms, leases, permits, inspection findings, and repair bids in a private evidence file; keep verified figures separate from estimates and leave unknown cells blank.", "Makes recurring costs, legal use, solar credits, and near-term capital needs measurable without presenting owner-supplied claims as official facts.", "Accept · Revise · Defer", link("cpuc") + " · " + link("water") + " · " + link("leginfo")),
        ("7 · Model improvement", "Retain a steady baseline, but also replay year-by-year historical inflation and housing paths and add clearly labeled severe-but-plausible shocks; avoid treating any 50-year path as a forecast or assigning unsupported probabilities.", "Long horizons can include recessions, inflation surges, insurance-market stress, and asset-price drawdowns; timing and sequence matter, not only average growth.", "Accept · Revise · Defer", link("blshist") + " · " + link("fhfa") + " · " + link("fed")),
        ("8 · Annual review", "Refresh federal and California law, estate thresholds, property-tax rules, insurance availability, and the source register annually and again near the actual transfer.", "The planned transfer is decades away, and current thresholds or rules should not be extrapolated as guaranteed future law.", "Accept · Revise · Defer", link("irs_new") + " · " + link("boe19") + " · " + link("leginfo")),
    ]) + '''<h2>Reviewer decision record</h2><p>For each item, choose <strong>Accept</strong>, <strong>Revise</strong>, or <strong>Defer</strong> in a private review record. Record the responsible professional, evidence needed, decision date, and next review date. This static public page does not collect submissions and contains no personal or property-specific information.</p><h2>Suggested order of work</h2><ol><li>Resolve the trust, authority, title, basis, and legal status questions listed on <a href="flagged.html">Flagged for review</a>.</li><li>Build a private, evidence-linked operating-cost file and obtain current independent quotes.</li><li>Only then populate an after-tax decision model with traceable inputs and an explicit baseline plus stress cases.</li><li>Compare alternatives; document the chosen path, rejected alternatives, sensitivity, and conditions that would trigger reconsideration.</li></ol>'''
    page("suggestions.html", "Suggestions for review", "Proposed improvements", body,
         "A prioritized, non-binding action list to improve decision quality. Review and choose a path before implementing changes.")

    years = ["2026", "2040", "2045", "2050", "2060", "2070"]
    rows = []
    for year in years:
        rows.append((year, '<span class="blank"></span>', '<span class="blank"></span>', '<span class="blank"></span>', link("fhfa") + " · " + link("boe800")))
    body = '''<div class="notice">Property-specific value and tax projection cells are intentionally blank. Future home prices, tax-rate-area charges, trust terms, transfer timing, and future law cannot be verified from today's official sources. This avoids presenting a made-up forecast as a fact.</div>''' + table("Property-specific projections: unverified cells remain blank", ["Year", "Market value", "Taxable / assessed value", "Property tax", "Official references"], rows) + '''<h2>Reproducible method for future use</h2><ul><li>Market-value scenario: verified transfer-year baseline × (1 + named annual growth assumption)<sup>years</sup>. Show several growth paths; do not call one a forecast.</li><li>California taxable value: start from the assessor's factored base-year value; Proposition 13 generally limits annual assessed-value inflation adjustments to 2%, but ownership change and exclusions can alter the result.</li><li>Transfer: apply the Prop 19 family-home rules only if transferor/transferee, principal-residence, filing and timing requirements are met.</li><li>Annual tax: actual taxable value × the actual tax-rate-area levy, plus applicable direct assessments. Use the secured bill, not a countywide proxy.</li></ul><p class="small">Generic calculation helpers in the repository contain no household values. They do not output a property forecast without verified inputs.</p>''' + table("Projection inputs to verify at the time of transfer", ["Input", "Required evidence", "Value in public report", "Reference"], [
        ("Transfer date and trust distribution authority", "Trust instrument and trustee determination", '<span class="blank"></span>', link("courts")),
        ("Date-of-death fair market value and income-tax basis", "Qualified valuation and estate basis documents", '<span class="blank"></span>', link("irs_basis")),
        ("Factored base-year value, tax rate area, direct assessments", "Current assessor record and secured tax bill", '<span class="blank"></span>', link("boe800") + " · " + link("boe29")),
        ("Prop 19 eligibility and exclusion allowance", "Transferor/transferee eligibility, residence and timely claims", '<span class="blank"></span>', link("boe19")),
    ])
    page("projections.html", "Year-by-year projections", "Projection worksheet", body)

    body = table("What is known without publishing personal financial information", ["Asset", "Status", "Property-specific value / tax", "Verification"], [
        ("Property A", "Expected trust inheritance around the stated future planning window; trust terms and transfer date are unknown.", '<span class="blank"></span>', link("irs_estate") + " · " + link("boe19")),
        ("Property B", "Already owned by the future inheritor; multi-unit use and rental arrangements require current documentation.",  '<span class="blank"></span>', link("boe800") + " · " + link("leginfo")),
    ]) + '''<h2>Privacy and verification boundary</h2><p>Owner-provided estimates, assessment histories, rent receipts, utility costs, and insurance estimates are not reproduced here. They cannot be independently confirmed through a public official source in a way that establishes the facts for these specific properties. The locations are intentionally not named. See <a href="flagged.html">Flagged for review</a> for the evidence categories that remain open.</p>'''
    page("properties.html", "Property facts and unknowns", "Properties", body)

    body = table("Operating-cost items — property-specific amounts are not verified", ["Cost", "Published value", "Why blank", "Official reference"], [
        ("Statewide homeowners-premium benchmark (not a local quote)", "$1,570 per year (CDI statewide average, rounded from the agency's published figure)", "A statewide average is not a quote, does not establish replacement cost, and may not represent this home's primary-residence or landlord coverage.", link("cdi_market")),
        ("Home insurance for A (future primary residence or rental)", '<span class="blank"></span>', "Premium depends on occupancy, replacement cost, coverage, claims, wildfire exposure and underwriting; obtain current written quotes.", link("cdi_home") + " · " + link("cdi_market")),
        ("Rental-property insurance for B", '<span class="blank"></span>', "Owner estimate is not a quote; coverage for multiple units and owner occupancy must be confirmed with insurers.", link("cdi_home")),
        ("Water and sewer", '<span class="blank"></span>', "Use actual account bills and current provider tariff; meter count, occupancy and conservation charges matter. CPUC regulation applies only to regulated providers; municipal utilities publish their own tariffs.", link("water")),
        ("Electricity and solar export credit", '<span class="blank"></span>', "Need meter records, tariff, system ownership and confirmation whether existing interconnection terms transfer.", link("cpuc")),
        ("Repairs, maintenance and capital reserve", '<span class="blank"></span>', "No inspection, age/condition report, contractor bids or unit-level history was reviewed.", link("boe800")),
        ("Rental operating costs", '<span class="blank"></span>', "Requires lawful unit count, actual leases, vacancy, management, taxes, insurance, utilities and repairs.", link("leginfo") + " · " + link("ftb")),
    ]) + '''<div class="notice"><strong>Insurance planning:</strong> do not substitute a statewide average for a property quote. Confirm replacement cost and policy form, and separately test nonrenewal, deductible increases, FAIR Plan availability, and required wrap-around coverage.</div>'''
    page("costs.html", "Insurance, utilities and repairs", "Operating costs", body)

    body = table("Stress regimes to model; no probabilities or household-specific forecasts asserted", ["Regime", "What to shock", "Why it matters", "Official historical / monitoring source"], [
        ("Historic inflation flare-up / stagflation", "BLS annual-average CPI inflation was 13.5% in 1980. Stress several years of high inflation with weak real growth; raise insurance, water, repairs and other costs separately.", "A high-inflation episode is documented; do not assume all household costs or home values rise at the same rate.", link("blshist") + " · " + link("fed")),
        ("Recent inflation and utility-cost shock", "BLS reported 12-month CPI inflation of 6.5% and electricity inflation of 14.3% through December 2022. Stress headline inflation and electricity separately.", "The episode shows why one smooth inflation rate can understate uneven costs; solar credits and tariffs are property-specific.", link("bls2022") + " · " + link("cpuc")),
        ("Interest-rate and liquidity shock", "Test higher borrowing costs, lower bond/stock values and delayed sale timing.", "A sale-and-reinvest plan can suffer sequence risk; borrowing and buyer demand also change.", link("fed")),
        ("Housing drawdown and slow recovery", "Apply a sharp nominal home-price fall, a multi-year flat period, then recovery; test transaction costs.", "Averages conceal long drawdowns and local housing outcomes differ from national indexes.", link("fhfa")),
        ("Insurance availability / premium shock", "Test higher premiums, larger deductibles, reduced coverage or inability to obtain standard coverage.", "Insurance cost and availability can dominate carrying costs and affect saleability.", link("cdi_market")),
        ("Seismic / disaster event", "Model repair, temporary housing, insurance limits, special assessments and delayed rebuilding.", "Physical loss can interact with insurance markets, rents, utilities and sale timing.", link("usgs") + " · " + link("cdi_home")),
        ("Long low-return period", "Use a prolonged low real return and poor early sequence for a diversified portfolio.", "A fixed average return is not a safe proxy for the order of returns.", link("fed") + " · " + link("bls")),
    ]) + '''<h2>How to use the scenarios</h2><p>For each regime, vary one factor and then combine correlated shocks. Keep nominal and inflation-adjusted results separate. Compare the same horizon and include taxes, transaction costs, vacancy, capital spending and the value of housing. No single black-swan scenario is assigned a probability or presented as a prediction.</p>'''
    page("black-swans.html", "Black-swan and uneven-economy scenarios", "Stress testing", body)

    body = table("Current inheritance and property-tax rules checked against official sources", ["Rule", "Current statement", "Scope / caveat", "Official source"], [
        ("Federal estate-tax exclusion", 'For 2026, the federal basic exclusion amount is <span class="stat">$15,000,000</span> per decedent.', "Estate-level calculation; not a separate per-heir inheritance allowance. Estate composition, deductions, prior taxable gifts and elections matter. Future amounts must be rechecked.", link("irs_estate") + " · " + link("irs_new")),
        ("California estate tax", "California says no estate-tax return is required for decedents dying on or after 1 January 2005.", "This does not eliminate federal estate tax or income tax on later income/gain.", link("sco")),
        ("California inheritance receipt", "California FTB says a gift or inheritance is not included in the recipient's income; income it later produces is taxable.", "Rental income, interest, dividends and taxable gain are distinct from receipt of the inheritance.", link("ftb")),
        ("Inherited income-tax basis", "Generally, basis is fair market value on date of death; alternate valuation and consistent-basis rules can apply.", "A sale near basis is not automatically tax-free: valuation, trust/estate inclusion, later appreciation and expenses matter.", link("irs_basis") + " · " + link("irs_706")),
        ("California parent-child property-tax exclusion", "Current Prop 19 rules require eligible family transfer and principal-residence requirements; value above the adjusted limit can increase taxable value.", "Claim timing and eligibility are critical; no exclusion for other real property under the current rule. Verify the applicable-year adjusted limit.", link("boe19") + " · " + link("boe801")),
        ("Property-tax assessment", "California assessed value is generally subject to a 2% annual inflation cap; the base property-tax rate is generally 1% plus voter-approved bonded debt, with reassessment and exceptions governed by law.", "The actual bill also depends on local tax-rate area and direct assessments; no property-specific amount is published here.", link("boe800") + " · " + link("boe29")),
    ]) + '''<p class="small">As of this review, the IRS lists the 2026 threshold. A 2040–2050 threshold is not stated as a forecast: inflation indexing and future legislation make a long-range dollar value uncertain.</p>'''
    page("tax.html", "Inheritance, estate and property tax", "Tax rules", body)

    body = table("Practical sequence for a trust-held inherited home", ["Step", "Action / evidence", "Why it matters", "Official source"], [
        ("1 · Identify authority", "Confirm trust instrument, successor trustee, distribution powers, debts, title and beneficiaries.", "A beneficiary may not be able to sell, occupy or lease before distribution or trustee approval.", link("courts")),
        ("2 · Inventory estate", "Document assets, liabilities, ownership, trust status, lifetime gifts, marital status and possible filing obligations.", "Federal estate tax uses the gross estate, deductions, adjusted taxable gifts and elections—not the value of one home alone.", link("irs_estate") + " · " + link("irs_706")),
        ("3 · Establish basis and value", "Obtain date-of-death valuation and retain basis, appraisal, improvement, expense and any estate-return documentation.", "Basis affects tax on later sale and must be supported by records.", link("irs_basis")),
        ("4 · Protect Prop 19 deadlines", "Check family eligibility, principal-residence occupancy and submit required homeowner/exclusion claims within current deadlines.", "Current BOE guidance describes a one-year homeowner-exemption filing period and a three-year exclusion claim period, subject to details and exceptions.", link("boe19") + " · " + link("boe801")),
        ("5 · Secure property and operations", "Bind appropriate insurance, confirm utilities, inspect condition, preserve leases and comply with local rental/habitability rules.", "Coverage and legal status cannot be assumed to continue unchanged through transfer.", link("cdi_home") + " · " + link("leginfo")),
        ("6 · Compare options after verification", "Build occupy / rent / sell cases from actual taxes, quotes, rental evidence, sale costs, income-tax basis and portfolio risks.", "Avoid using gross rent, unsupported insurance or a countywide proxy as net economic value.", link("ftb") + " · " + link("irs_basis")),
        ("7 · Recheck law and file", "Confirm federal and state law, forms, transfer recording, tax bills and insurance requirements for the actual transfer year.", "A transfer expected decades out cannot be safely administered from current rules alone.", link("irs_new") + " · " + link("boe19")),
    ])
    page("process.html", "Trust inheritance: step by step", "Transfer process", body)

    body = table("No future legal change is assumed in the model", ["Topic to monitor", "Current position", "Recheck trigger", "Official source"], [
        ("Federal estate and gift tax", "2026 federal estate-tax exclusion is $15,000,000; the law in the future transfer year controls.", "Each annual IRS update and any enacted federal tax legislation.", link("irs_new") + " · " + link("irs_estate")),
        ("California Prop 19", "Current exclusions, adjusted value limit, eligibility and claim deadlines are described by BOE.", "Before transfer, claim, move-in, sale or third-party transfer; check statutory and BOE updates.", link("boe19") + " · " + link("leginfo")),
        ("Property-tax rate and assessment", "Tax-rate-area levies, assessments, direct charges and reassessment rules vary by parcel and year.", "Annual secured tax bill and assessor notice; not replaced by a general projection.", link("boe29") + " · " + link("boe800")),
        ("Insurance market", "Availability, underwriting and premium conditions change; state market conditions are not a property quote.", "Annual renewal, nonrenewal notice, ownership/occupancy change or insurer-market disruption.", link("cdi_market") + " · " + link("cdi_home")),
        ("Rent, utilities and solar", "Applicable rent rules, utility tariffs and solar compensation depend on law, provider, equipment and contract.", "At transfer and whenever a lease, tariff or ownership changes.", link("leginfo") + " · " + link("cpuc") + " · " + link("water")),
    ]) + '''<p>Proposed bills are not treated as law. This page does not make claims about pending proposals unless a primary source confirms their status. Re-run the decision model using enacted law at the time of transfer.</p>'''
    page("law-watch.html", "Law and policy watch", "Monitoring", body)

    body = table("Items that cannot be independently verified and are intentionally not published", ["Open item", "Public value", "Why unresolved", "Official reference"], [
        ("Property-specific market value, tax assessments and tax bills", '<span class="blank"></span>', "These are private/identifying household facts; public records do not establish which records belong to the described household.", link("boe800")),
        ("Local tax-rate area and municipal rules", '<span class="blank"></span>', "The public report does not name a municipality or parcel, so a specific tax-rate area, rental ordinance, utility provider tariff or permitted unit configuration cannot be matched.", link("boe29") + " · " + link("leginfo")),
        ("Trust text, transfer date, estate inclusion and authority", '<span class="blank"></span>', "Private documents were not reviewed; no assumption is made about ownership or trustee power.", link("irs_estate") + " · " + link("courts")),
        ("Property A or B rent and lawful unit status", '<span class="blank"></span>', "Lease records and permits are not independently available in this review; no rental projection is presented as verified.", link("leginfo")),
        ("Rental-income tax, depreciation and tax on a later sale", '<span class="blank"></span>', "Rental income, deductible costs, depreciation, passive-loss rules and recapture depend on basis and taxpayer facts; no after-tax rental comparison is presented.", link("irs527") + " · " + link("irs_basis")),
        ("Housing-use tradeoff between A and B", '<span class="blank"></span>', "The household-specific use, legal occupancy and rent alternative for the already-owned property has not been valued; options are not represented as housing-equivalent.", link("irs527")),
        ("Insurance premiums and insurability", '<span class="blank"></span>', "Only an insurer can quote specific coverage after underwriting; statewide references cannot validate a home premium.", link("cdi_home") + " · " + link("cdi_market")),
        ("Water, electricity, solar credits and repairs", '<span class="blank"></span>', "No utility account history, tariff contract, inspection or contractor quote was reviewed.", link("water") + " · " + link("cpuc")),
        ("Future tax threshold, rates and rules", '<span class="blank"></span>', "A transfer decades away depends on future legislation, inflation indexing and jurisdictional rates.", link("irs_new") + " · " + link("boe19")),
    ]) + '''<div class="callout bad"><strong>Privacy notice:</strong> exact and rounded owner-supplied financial details are omitted from the deployed site. A repository-wide scan also found residual owner-derived amounts in non-deployed repository files; the values are not reproduced here. Older public Git history and caches may retain prior figures. Excluding legacy files from this release does not erase them. Repository cleanup, visibility changes, or history rewriting require the repository owner's decision.</div>'''
    page("flagged.html", "Flagged for review", "Open evidence gaps", body)

    rows = []
    descriptions = {
        "irs_estate": "Federal estate tax framework and year-of-death filing threshold.",
        "irs_new": "Enacted federal tax updates; current and future law monitoring.",
        "irs_basis": "General basis rules for inherited property and later sale.",
        "irs_706": "Estate return instructions, elections and reporting.", "irs527": "Rental income, expenses, repairs and depreciation rules.",
        "sco": "California estate-tax status.", "ftb": "California income treatment of gifts and inheritances.",
        "boe19": "California Proposition 19 rules and filing requirements.", "boe801": "BOE's Prop 19 fact sheet and eligibility details.",
        "boe800": "Assessment and change-in-ownership background.", "boe29": "Property tax overview and local bill components.",
        "cdi_home": "Residential insurance shopping and consumer guidance.", "cdi_market": "California insurance-market conditions and reforms.",
        "cpuc": "California net energy metering and billing context.", "water": "Water-rate information and conservation portal.",
        "bls": "Consumer Price Index program and inflation context.", "bls2022": "BLS December 2022 release: 12-month CPI and electricity changes.",
        "blshist": "Historical CPI-U series for earlier inflation episodes.", "fhfa": "House price index data and methodology.",
        "fed": "Federal Reserve policy context and releases.", "usgs": "Earthquake hazard information.", "courts": "California probate process overview.",
        "leginfo": "California statutes and legislative code database.",
    }
    for key, description in descriptions.items():
        rows.append((link(key), escape(description), "Official primary source"))
    body = table("Official references used in this release", ["Source", "Use in this site", "Status"], rows) + '''<p class="small">The linked official primary sources were retrieved and reviewed for this release. Each source supports only the rule or historical fact described; it does not certify any private property fact. Every data row on this site has at least one official source link.</p>'''
    page("sources.html", "Official sources", "Source register", body)

    # HTML files are composed above once each. Ensure all expected routes exist.
    for slug, _ in NAV:
        if not (OUT / slug).exists():
            raise RuntimeError(f"missing page: {slug}")
    print(f"built {len(NAV)} privacy-safe pages in {OUT}/")


if __name__ == "__main__":
    build()
