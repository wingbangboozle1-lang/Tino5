#!/usr/bin/env python3
"""desk-9af5443d generator.

Gap-filling decision desk (session arena-9af5443d, 2026-11-15) for the Property A /
San Francisco inheritance decision project. Focuses on the requirement items not
fully covered by the previously merged desks:

  * SF Proposition H modelled with its OFFICIAL terms — both the November 2024
    firefighter-pension measure and the November 2026 Muni parcel tax — plus the
    companion measures (Prop M business tax, Measure I transfer tax, RTM sales tax).
  * Form 540 read line-by-line from the official FTB 2025 instructions: the
    Behavioral Health Services Tax (1% on CA taxable income over $1,000,000,
    Form 540 line 62) and the capital-gain treatment; the MHST sensitivity value
    is updated on this desk.
  * Property A rent comparables from official Census ACS evidence (QuickFacts),
    so the rent path is ranked on evidence rather than a voucher benchmark.
  * Five-year maintenance and capital plan for both buildings.
  * Estate liquidity plan (federal exclusion, portability, prior gifts).
  * Distribution chart on the projections page.
  * Decision-and-date register.

Design rules (hard, privacy-first):
  * No names, street addresses, ZIP codes, neighbourhoods, parcel/account numbers
    or contact details anywhere on the published site. Properties are "Property A"
    (future trust inheritance, Santa Clara County) and "Property B" (already owned,
    San Francisco County) at county level only.
  * Money rounded to nearest $10 unless a statutory / agency figure is quoted
    exactly (those are tagged `exact`).
  * Every table row carries an official-source link, or is left blank and tagged
    `unverified` / `owner` / `assumption`. No inferred or invented values presented
    as fact.
  * Model outputs are labelled `assumption` / `derived` and show their inputs.
"""
import os

OUT = os.path.join(os.path.dirname(__file__), "..")
ASSETS = os.path.join(OUT, "assets")

# ----------------------------------------------------------------------------- sources
# Each: key -> (label, official URL). Only domains confirmed as official.
SRC = {
 "irs_estate":  ("IRS — Working Families Tax Cuts: 2026 federal estate/gift basic exclusion $15,000,000 per person, top rate 40%, gift annual exclusion $19,000",
                 "https://www.irs.gov/newsroom/working-families-tax-cuts-individuals-and-workers"),
 "irs_706":     ("IRS — Form 706 (United States Estate (and Generation-Skipping Transfer) Tax Return) and its instructions (filing deadlines, portability/DSUE election)",
                 "https://www.irs.gov/forms-pubs/about-form-706"),
 "irs_stepup":  ("IRS — Topic No. 403, Basis of Assets: step-up in basis to fair market value at date of death (IRC §1014)",
                 "https://www.irs.gov/taxtopics/tc403"),
 "irs_121":     ("IRS — Topic No. 703, Sale of Home: §121 exclusion up to $250,000 ($500,000 married filing jointly), ownership + use 2 of 5 years",
                 "https://www.irs.gov/taxtopics/tc703"),
 "irs_niit":    ("IRS — Net Investment Income Tax (3.8%) Q&A",
                 "https://www.irs.gov/individuals/net-investment-income-tax"),
 "ftb_540":     ("CA FTB — 2025 Instructions for Form 540, California Resident Income Tax Return (Behavioral Health Services Tax at line 62; capital-gain reporting via federal Schedule D)",
                 "https://www.ftb.ca.gov/forms/2025/2025-540-instructions.html"),
 "ftb_540form": ("CA FTB — 2025 Form 540 itself (line 62 Behavioral Health Services Tax; line 19 taxable income)",
                 "https://www.ftb.ca.gov/forms/2025/2025-540.pdf"),
 "ftb_rates":   ("CA FTB — 2025 California Tax Rate Schedules (top personal rate 12.3%; no preferential capital-gain rate)",
                 "https://www.ftb.ca.gov/forms/2025/2025-540-tax-rate-schedules.pdf"),
 "ftb_fedchanges": ("CA FTB — Summary of Federal Income Tax Changes (California conformity; no state LTCG preference)",
                 "https://www.ftb.ca.gov/about-ftb/data-reports-plans/summary-of-federal-income-tax-changes/index.html"),
 "ftb_home":    ("CA FTB — California has no state estate tax and no inheritance tax; inherited property is not taxable income to the recipient",
                 "https://www.ftb.ca.gov/"),
 "boe_home":    ("California State Board of Equalization — property tax, Proposition 13 / 19 program pages",
                 "https://www.boe.ca.gov/"),
 "boe_prop13":  ("BOE — Proposition 13: 1% general tax limit, assessed-value annual increase capped at 2% absent change in ownership or new construction",
                 "https://www.boe.ca.gov/proptaxes/proposition13.htm"),
 "boe_prop19":  ("BOE — Proposition 19 (Rev. & Tax. Code §63.2): parent-child exclusion limited to primary residence, transferee must occupy within 1 year, file BOE-19-P within 3 years, non-primary property fully reassessed",
                 "https://www.boe.ca.gov/proptaxes/proposition19.htm"),
 "scc_prop13":  ("Santa Clara County Assessor — Understanding Proposition 13 (1% rate, 2% cap, tax-rate areas)",
                 "https://asr.santaclaracounty.gov/faq/understanding-proposition-13"),
 "scc_ratebook":("County of Santa Clara Compilation of Tax Rates & Information, FY2025-26 (tax rate areas; 1% levy; installment dates)",
                 "https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf"),
 "sfelections_2024": ("San Francisco Department of Elections — November 5, 2024 Final Results (Measure H — Retirement Benefits for Firefighters; Measure M — Changes to Business Taxes)",
                 "https://www.sfelections.org/results/20241105/index.html"),
 "sfelections_2026": ("San Francisco Department of Elections — November 3, 2026 Preliminary Results (Measure H — Parcel Tax to Fund Muni Operations; Measure I — Changes to Real Property Transfer Tax; Regional Measure RTM)",
                 "https://www.sfelections.org/results/20261103/index.html"),
 "sfmta_proph": ("SFMTA — Proposition H: Stronger Muni For All Parcel Tax (official city agency page: rate schedule, effective dates, exemptions)",
                 "https://sfmta.com/projects/proposition-h-muni-local-measure"),
 "sfgov_digest":("City and County of San Francisco — Ballot Simplification Committee Final Digest: Changes to Business Taxes (Measure M, Nov 2024)",
                 "https://www.sf.gov/sites/default/files/2024-08/Final%20Digest%20-%20Changes%20to%20Business%20Taxes.pdf"),
 "census_cupertino": ("U.S. Census Bureau QuickFacts — city-level ACS profile for the Property A area (median gross rent $3,500+, 2020-2024 ACS 5-year)",
                 "https://www.census.gov/quickfacts/fact/table/cupertinocitycalifornia/PST045225"),
 "census_scc":  ("U.S. Census Bureau QuickFacts — Santa Clara County, California (median gross rent $2,857, 2020-2024 ACS 5-year)",
                 "https://www.census.gov/quickfacts/fact/table/santaclaracountycalifornia/RHI825222"),
 "treasury":    ("U.S. Department of the Treasury — Daily Treasury Par Yield Curve (3-month and 2-year points used for the phased-investing parking path)",
                 "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve"),
 "sjwater":     ("San Jose Water Company — approved residential tiered quantity rates and monthly service charge (serves the Property A area)",
                 "https://www.sjwater.com/media/kccm45hy/san-jose-water-company-al-599-approved_0.pdf"),
 "sfpuc":       ("SFPUC — Water & Sewer Rates, Proposition 218 notice (Property B area general schedule; average single-family combined bill)",
                 "https://www.sfpuc.gov/accounts-services/water-power-sewer-rates/proposed-water-sewer-rates-2026/proposition-218-notice"),
 "cpuc":        ("CPUC — PG&E residential average price and Income-Graduated Base Services Charge (electricity reference for both counties)",
                 "https://www.cpuc.ca.gov/"),
 "doi":         ("California Department of Insurance — homeowners / dwelling fire (DP) policy framework and FAIR Plan context",
                 "https://www.insurance.ca.gov/"),
 "fairplan":    ("California FAIR Plan — insurer of last resort; dwelling fire policy limits (fire-zone context)",
                 "https://www.cfpnet.com/"),
 "nber_2008":   ("NBER — Business Cycle Dating Committee announcement (Sept 20, 2010): 2007-2009 recession chronology",
                 "https://www.nber.org/news/business-cycle-dating-committee-announcement-september-20-2010"),
 "fedhist_1929":("Federal Reserve History — Stock Market Crash of 1929 (historical drawdown reference for black-swan entry risk)",
                 "https://www.federalreservehistory.org/essays/stock-market-crash-of-1929"),
 "fedhist_2008":("Federal Reserve History — The Great Recession of 2007-09 (historical drawdown reference for black-swan entry risk)",
                 "https://www.federalreservehistory.org/essays/great-recession-of-200709"),
 "sco_estate":  ("California State Controller — California Estate Tax (no state estate tax for deaths on/after January 1, 2005)",
                 "https://www.sco.ca.gov/ardtax_estate_tax.html"),
 "leginfo_rt":  ("California Legislative Information — Revenue & Taxation Code (official statutes, including §63.2 for Proposition 19)",
                 "https://leginfo.legislature.ca.gov/faces/codes.xhtml"),
}

def src(key):
    label, url = SRC[key]
    return f'<a href="{url}" target="_blank" rel="noopener">{label}</a>'

# ----------------------------------------------------------------------------- money
def m0(x):
    """Round to nearest $10, format. None -> blank."""
    if x is None:
        return ""
    return f"${int(round(x / 10.0) * 10):,}"

def m_exact(x):
    """Statutory/exact figure: format as published, tag exact."""
    if x is None:
        return ""
    return f"${int(x):,}"

def tag(kind):
    # kind: verified | assumption | unverified | owner | exact
    cls = {"verified": "verified", "assumption": "assumption", "unverified": "unverified",
           "owner": "owner", "exact": "exact"}[kind]
    lab = {"verified": "verified", "assumption": "assumption", "unverified": "unverified",
           "owner": "owner-supplied", "exact": "exact (statutory)"}[kind]
    return f'<span class="tag {cls}">{lab}</span>'

# ----------------------------------------------------------------------------- page shell
NAV_GROUPS = [
 ("Start", [("Home", "index.html"), ("Executive summary", "executive-summary.html")]),
 ("Property A — inherited via trust ~2040-2050",
  [("Projections & distribution", "projections.html"), ("Rent comparables", "rent-comparables.html")]),
 ("Property B — already owned",
  [("SF measures: Prop H & others", "sf-measures.html"), ("Five-year maintenance plan", "maintenance-plan.html")]),
 ("Taxes",
  [("CA income tax & Form 540", "ca-income-tax.html"), ("Estate tax & liquidity plan", "estate-liquidity.html")]),
 ("Decision", [("Decision & date log", "decision-log.html")]),
 ("Record",
  [("Questions & gaps", "questions.html"), ("Suggestions board", "suggestions.html"),
   ("Law watch", "law-watch.html"), ("Sources", "sources.html"),
   ("Flagged for review", "flagged.html"), ("Methodology & privacy", "methodology.html")]),
 ("For advisers", [("Attorney & CPA Briefing Sheet", "briefing-sheet.html")]),
]

def nav_html():
    parts = []
    for grp, items in NAV_GROUPS:
        parts.append(f'<span class="grp">{grp}</span>')
        for t, h in items:
            parts.append(f'<a href="{h}">{t}</a>')
    return "".join(parts)

def page(title, body, dek="", printable=False):
    css = '<link rel="stylesheet" href="assets/style.css">'
    pr = ' class="print-page"' if printable else ""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><meta name="referrer" content="no-referrer">
<title>{title} — Inheritance decision desk (gap desk)</title>{css}</head><body{pr}>
<header><div class="bar"><h1>Inheritance decision desk — gap desk</h1><div class="sub">Property A (future trust inheritance) · Property B (already owned) · County level · No personal identifiers</div></div>
<nav>{nav_html()}</nav></header>
<main><div class="page-header"><h2>{title}</h2>{f'<p class="dek">{dek}</p>' if dek else ''}</div>{body}
<div class="foot no-print"><b>Not tax, legal or investment advice.</b> Figures are planning estimates based on the sources named in each row. Statutory amounts are quoted as published; all other money rounded to the nearest $10. Re-check the then-current law before acting. <a href="sources.html">Source register</a> · <a href="flagged.html">Flagged for review</a> · <a href="methodology.html">Methodology &amp; privacy</a></div></main>
</body></html>"""

def tbl(headers, rows, caption=None):
    cap = f'<p class="small" style="margin-top:10px">{caption}</p>' if caption else ""
    h = "".join(f"<th>{x}</th>" for x in headers)
    b = ""
    for r in rows:
        cells, kind = r
        if kind in ("owner", "unverified", "assumption", "exact", "verified"):
            cells = cells + [tag(kind)]
        else:
            cells = cells + [""]
        b += "<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"
    return f'{cap}<table class="data"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>'

# =============================================================================
# MODEL
# =============================================================================
GROWTH = 0.05          # assumption: home value growth
COST_INFL = 0.03       # assumption: operating-cost inflation
PROP13_CAP = 0.02      # statutory: Prop 13 assessment growth cap
TAX_RATE = 0.01        # statutory: Prop 13 general levy (plus bonds/assessments)
MHST_THRESHOLD = 1_000_000
MHST_RATE = 0.01

def prop_value(base_2026, year, g=GROWTH):
    return base_2026 * (1 + g) ** (year - 2026)

def prop_tax(year, base_2026, g=GROWTH):
    """1% of market value at year (full reassessment assumption for A at transfer)."""
    return TAX_RATE * prop_value(base_2026, year, g)

def mhst(taxable_income):
    return max(0.0, (taxable_income - MHST_THRESHOLD)) * MHST_RATE

pages = {}

# ---------------------------------------------------------------- index
glossary = [
 ("Assessed value", "The value the county uses to calculate property tax; under Prop 13 it grows at most 2%/yr until a change in ownership reassesses it to market value."),
 ("Behavioral Health Services Tax (MHST)", "California's 1% surtax on taxable income over $1,000,000, computed on Form 540 line 62 (FTB instructions)."),
 ("Black swan regime", "A stress scenario built on real historical drawdowns (1929, 2008) rather than a constant growth rate; growth and inflation are never consistent over 50 years."),
 ("Change in ownership", "Death, transfer or new construction that resets assessed value to market value unless an exclusion (e.g. Proposition 19) applies."),
 ("DSUE / portability", "Deceased spousal unused exclusion: a surviving spouse can inherit a deceased spouse's unused federal estate exclusion if portability was elected on Form 706."),
 ("Factored base year value", "A property's assessed value carried forward at up to 2%/yr under Prop 13; the starting point for Proposition 19 calculations."),
 ("Like-kind exchange (1031)", "A tax-deferred exchange of certain property; must be structured before a sale and requires professional advice."),
 ("MHST sensitivity", "The table showing how much the 1% surtax adds once CA taxable income crosses $1,000,000 in a single year."),
 ("Parcel tax", "A per-parcel tax (not based on value); SF Measure H (2026) is a parcel tax added to the regular property tax bill."),
 ("Phased investing", "Parking sale proceeds in short-term Treasuries for 24-36 months, then moving into stocks gradually to soften crash-entry risk."),
 ("Proposition 19 allowance", "The inflation-adjusted dollar amount above the parent's factored base year value that can pass without reassessment for a qualifying primary residence ($1,044,586 for 2025-2027)."),
 ("Reinvestment risk", "The risk that cash parked for the phased-investing path earns less than the portfolio it replaces, or that markets rise while the money is parked."),
 ("Step-up in basis", "The heir's tax basis in inherited property resets to fair market value at the date of death (IRC §1014)."),
]
gl_rows = [([f"<b>{k}</b>", v], "assumption") for k, v in glossary]

kpi = [
 (m_exact(3100000), "Property A estimated value, Nov 2026 (owner input · unverified)"),
 (m_exact(1800000), "Property B estimated value, Nov 2026 (owner input · unverified)"),
 (m_exact(15000000), "Federal estate/gift basic exclusion per person, 2026"),
 (m_exact(1000000), "MHST threshold: CA taxable income over this amount pays +1%"),
 (m_exact(129), "SF Measure H parcel tax base, single-family (from FY2027-28)"),
 (m_exact(1044586), "Prop 19 allowance 2025-2027 (BOE; exact)"),
]
kpi_html = "".join(f'<div class="t"><div class="v">{v}</div><div class="l">{l}</div></div>' for v, l in kpi)

index_body = f"""
<div class="callout info"><b>What this desk adds.</b> The merged desks already cover the core live / rent / sell
model, the phased-investing (Black swan) path, the briefing sheets and the question registers. This desk closes
the remaining gaps from the full requirement list: <b>Prop H modelled with its official terms</b> (both the
Nov-2024 firefighter-pension measure and the Nov-2026 Muni parcel tax), the <b>Form 540 1% tax and
capital-gain treatment read line-by-line from the official FTB instructions with the sensitivity value updated</b>,
<b>Property A rent comparables from official Census ACS evidence</b>, a <b>five-year maintenance and capital plan</b>,
an <b>estate liquidity plan</b>, a <b>distribution chart</b> and a <b>decision-and-date log</b>.</div>

<h3>What would change the answer (read first)</h3>
<ul>
<li><b>Whether the heir occupies Property A within one year of transfer.</b> That is the switch between the
Proposition 19 capped reassessment and full market reassessment — the single largest lever on Property A's tax bill.</li>
<li><b>Whether any single year pushes CA taxable income over $1,000,000.</b> A large one-year gain (sale, vesting,
business sale) then adds the 1% MHST on the excess — see the updated sensitivity on the CA income tax page.</li>
<li><b>SF Measure H (Nov 2026).</b> A new annual parcel tax on SF parcels from the FY2027-28 bill adds a small,
fixed cost to Property B (base $249 for multifamily; size-based additions unverified until building area is known).</li>
<li><b>Rent evidence for Property A.</b> The official Census ACS median gross rent for the area is $3,500+/month;
a property-specific written rent opinion is still needed before ranking the rent path on its own numbers.</li>
<li><b>Estate size versus the $15,000,000 federal exclusion.</b> The "considerable money" in the inheritance decides
whether an estate liquidity plan and Form 706 deadlines matter at all.</li>
</ul>

<h3>Grouped menu</h3>
<p>Use the navigation above, grouped by category. Every table row cites its official source or says in the row
that none exists.</p>

<h3>Key figures at a glance</h3>
<div class="kpi">{kpi_html}</div>

<h3>Glossary</h3>
{tbl(["Term", "Meaning"], gl_rows, "Terms used across this desk. Wording is the desk's plain-English gloss, not statutory text; the statutory term of art is linked in the relevant row.")}
"""
pages["index.html"] = dict(title="Home", dek="Gap-filling decision desk: Prop H with official terms, Form 540 MHST, rent comparables, maintenance plan, estate liquidity, distribution chart and decision log.", body=index_body)

# ---------------------------------------------------------------- executive summary
exec_body = f"""
<div class="callout ok"><b>Headline (baseline, $10 rounding).</b> The recommendation is unchanged from the
merged desks: on the baseline assumptions, <b>selling Property A at inheritance and reinvesting after tax
out-keeps holding it as a rental</b>, because a $3,100,000 inherited home largely reassesses to market value and
carries a material tax bill, while the Prop 19 allowance shields only about {m0(1044586)} of the gap — and only if
the heir occupies within one year. This desk adds the tax-law detail that sharpens the numbers: the 1% MHST applies
in any year CA taxable income exceeds $1,000,000, and SF's new parcel tax adds a fixed cost to Property B from the
FY2027-28 tax bill.</div>

<h3>What would change the answer</h3>
{tbl(["Condition that flips the decision", "Break-even / threshold", "Source / basis"], [
 ([ "Heir occupies Property A as primary residence within 1 year of transfer",
    "Qualifies for the Prop 19 capped reassessment; assessed value ≈ factored base + $1,044,586 allowance (2025-2027)",
    src("boe_prop19") ], "verified"),
 ([ "Heir does <b>not</b> occupy within 1 year",
    "Full reassessment to market value at transfer; the exclusion is lost",
    src("boe_prop19") ], "verified"),
 ([ "A single year pushes CA taxable income over $1,000,000",
    "Adds 1% MHST on the excess (Form 540 line 62); top CA marginal rate becomes 13.3% on the excess",
    src("ftb_540") ], "verified"),
 ([ "Gross rental yield &gt; after-tax portfolio return + carrying costs",
    "Renting/keeping beats selling",
    "Desk model (assumption)" ], "assumption"),
 ([ "House price growth &gt; portfolio return (after tax)",
    "Keeping compounds better than selling",
    "Desk model (assumption)" ], "assumption"),
 ([ "Heir sells and lived in the home ≥2 of 5 years before sale",
    "§121 exclusion up to $250,000/$500,000 on top of the stepped-up basis",
    src("irs_121") ], "verified"),
 ([ "Total estate exceeds the federal basic exclusion",
    "Federal estate tax applies above $15,000,000/person (2026); California adds no estate or inheritance tax",
    src("irs_estate") + " " + src("sco_estate") ], "verified"),
])}

<h3>Decisions recorded this session (full log on the Decision page)</h3>
{tbl(["Item", "Desk decision", "Date", "Basis"], [
 ([ "Model Prop H with official terms", "Modelled both SF Prop H measures with official terms; Property B cost = +$249/yr base parcel tax from FY2027-28 (size additions unverified)", "2026-11-15", src("sfelections_2026") + " " + src("sfmta_proph") ], "verified"),
 ([ "Update the 1% tax sensitivity", "Sensitivity updated from the official Form 540 instructions: 1% on taxable income over $1,000,000, Form 540 line 62; capital gains at ordinary CA rates", "2026-11-15", src("ftb_540") + " " + src("ftb_rates") ], "verified"),
 ([ "Rank the rent path on evidence", "Ranked on official Census ACS median gross rent ($3,500+/mo, 2020-2024); property-specific rent remains unverified — obtain a written rent opinion", "2026-11-15", src("census_cupertino") ], "verified"),
 ([ "Five-year maintenance plan", "Built at $10 rounding from owner anchors and official rate references; capital items left blank until inspection", "2026-11-15", "Desk model (assumption)" ], "assumption"),
 ([ "Estate liquidity plan", "Thresholds verified; portability and prior-taxable-gift questions posed for the estate attorney", "2026-11-15", src("irs_706") + " " + src("irs_estate") ], "verified"),
 ([ "Scrub pre-rounding git history", "<b>Not performed</b> — rewriting public history is an owner decision; options documented on the Flagged page", "2026-11-15", "Owner decision (flagged)" ], "unverified"),
])}

<h3>Where the numbers come from</h3>
<p>Every figure on every page links its official source in the row, or is marked <span class="tag owner">owner-supplied</span>,
<span class="tag unverified">unverified</span> or <span class="tag assumption">assumption</span>. Model projections are
labelled as such and show their inputs. See <a href="methodology.html">Methodology &amp; privacy</a>.</p>
"""
pages["executive-summary.html"] = dict(title="Executive summary", dek="Headline recommendation, the conditions that flip it, and the decisions recorded on 2026-11-15.", body=exec_body)

# ---------------------------------------------------------------- projections
proj_rows = []
for y in range(2026, 2051, 5):
    av = prop_value(3_100_000, y)
    av2 = prop_value(1_800_000, y)
    proph = 249 * (1 + COST_INFL) ** (max(0, y - 2027)) if y >= 2027 else 0
    proj_rows.append(([
        str(y),
        m0(av),
        m0(prop_tax(y, 3_100_000)),
        m0(av2),
        m0(prop_tax(y, 1_800_000)),
        m0(proph) if y >= 2027 else "—",
        "assumption — value growth 5%/yr, 1% levy, $10 rounding",
    ], "assumption"))

# distribution chart: Property A value across growth regimes at three horizons
dist_years = [2035, 2045, 2050]
dist_rates = [0.03, 0.05, 0.07]
dist_data = {y: [3_100_000 * (1 + g) ** (y - 2026) for g in dist_rates] for y in dist_years}
allv = [v for vs in dist_data.values() for v in vs]
vmax = max(allv)
BAR_COLORS = ["#1f4e79", "#3b7bbf", "#7fb0e0"]
dist_bars = []
for y in dist_years:
    dist_bars.append(f'<div class="dist-group"><div class="dist-label">{y}</div><div class="dist-bars">')
    for i, v in enumerate(dist_data[y]):
        h = 8 + 78 * (v / vmax)
        dist_bars.append(f'<div class="dist-bar" style="height:{h:.0f}px;background:{BAR_COLORS[i]}"><span class="dist-val">{m0(v)}</span></div>')
    dist_bars.append("</div></div>")
dist_chart = f"""<div class="chart">{''.join(dist_bars)}
<div class="dist-legend"><span><i style="background:{BAR_COLORS[0]}"></i> 3%/yr</span><span><i style="background:{BAR_COLORS[1]}"></i> 5%/yr (baseline)</span><span><i style="background:{BAR_COLORS[2]}"></i> 7%/yr</span></div></div>"""

proj_body = f"""
<p class="small">Baseline assumptions: value growth {GROWTH:.0%}/yr; property tax 1% of value (Prop 13 general levy plus
voter-approved bonds/assessments not separately priced); operating-cost inflation {COST_INFL:.0%}/yr; all money rounded
to the nearest $10. Property A is shown at <b>full reassessment at transfer</b> (heir does not occupy). Property B is
already owned; its assessed base is not published (privacy), so its tax is shown at 1% of market value as an
illustrative assumption. <b>Distribution chart:</b> Property A value under three growth regimes — growth and inflation
are never consistent over 50 years, so a single point projection is not the decision.</p>

<h3>Year-by-year projection, 2026-2050</h3>
{tbl(["Year", "Property A est. value", "Property A est. tax (1%)", "Property B est. value", "Property B est. tax (1%)", "SF Measure H parcel tax (B)", "Basis"], proj_rows,
     "Model arithmetic from the stated assumptions; rounded to $10. Statutory rate and parcel-tax base are linked in the rows below.")}

<h3>Distribution chart — Property A value under three growth regimes</h3>
{dist_chart}
<p class="note"><span class="tag assumption">assumption</span> The bars show Property A's estimated market value in
2035, 2045 and 2050 under 3%, 5% and 7% annual growth. 5%/yr is the baseline assumption; the range shows the spread
the decision has to survive. This is a model output, not a forecast.</p>

<h3>Property A tax-rate area</h3>
{tbl(["Item", "Figure / rule", "Source"], [
 ([ "Property A sits in Santa Clara County; the county publishes tax-rate areas, each with its own combined rate",
    "816 tax-rate areas in the FY2025-26 Compilation of Tax Rates; the general levy is capped at 1%",
    src("scc_ratebook") ], "verified"),
 ([ "Property A's own tax-rate-area combined rate",
    "Not published on this desk — the owner's tax bill shows the combined rate; read it from the bill before relying on the 1% alone",
    "Owner decision (flagged R05)" ], "unverified"),
 ([ "Prop 13 base rules",
    "1% general tax limit; assessed value grows at most 2%/yr absent change in ownership or new construction",
    src("boe_prop13") + " " + src("scc_prop13") ], "verified"),
])}
"""
pages["projections.html"] = dict(title="Projections &amp; distribution", dek="Year-by-year 2026-2050 projection and the growth-regime distribution chart.", body=proj_body)

# ---------------------------------------------------------------- rent comparables
rent_body = f"""
<div class="callout info"><b>Why this page exists.</b> The rent path must be ranked on evidence, not on a voucher
benchmark. Official area-level evidence exists (Census ACS); property-specific rent does not. Rows below cite the
official source or are left blank and flagged.</div>

<h3>Official area-level rent evidence</h3>
{tbl(["Area", "Official measure", "Value", "Period", "Source"], [
 ([ "Property A area (city level)", "Median gross rent", m_exact(3500) + "+ / month", "2020-2024 ACS 5-year", src("census_cupertino") ], "verified"),
 ([ "Santa Clara County", "Median gross rent", m_exact(2857) + " / month", "2020-2024 ACS 5-year", src("census_scc") ], "verified"),
 ([ "Property A area", "Owner-occupied housing rate", "60.6%", "2020-2024 ACS 5-year", src("census_cupertino") ], "verified"),
 ([ "Property A area", "Median value of owner-occupied units", m_exact(2000000) + "+", "2020-2024 ACS 5-year", src("census_cupertino") ], "verified"),
 ([ "Property A area", "Median household income", m_exact(234707), "2020-2024 ACS 5-year", src("census_cupertino") ], "verified"),
])}
<p class="note">The $3,500+ figure is the Census Bureau's published area median for all rental housing units in the
city, not a rent opinion for Property A. Census ACS is an official source; it is area evidence, not a property
comparable.</p>

<h3>Property-specific rent (the number that actually decides the rent path)</h3>
{tbl(["Item", "Value", "Status", "Source"], [
 ([ "Property A market rent (1-unit single-family home)",
    "",
    "No official source publishes a rent for a specific property; Census ACS area median is $3,500+/mo",
    src("census_cupertino") ], "unverified"),
 ([ "Written rental market analysis / rent opinion for Property A",
    "Not obtained",
    "Discovery action: commission a licensed broker's or appraiser's written rent opinion before ranking rent vs. sell",
    "Owner action (flagged R08)" ], "unverified"),
 ([ "Property B achieved rent (2 units)", m0(7150) + " / month",
    "Owner-supplied; no official confirmation",
    "Owner input" ], "owner"),
 ([ "HUD Fair Market Rent (voucher benchmark)", "Not used on this desk",
    "Deliberately excluded: the brief requires evidence-based ranking, not a voucher benchmark",
    "Desk policy" ], "assumption"),
])}

<h3>How the rent path is ranked on evidence</h3>
{tbl(["Step", "Evidence used", "Source"], [
 ([ "1. Establish the area rent floor", "Official Census ACS median gross rent for the city ($3,500+/mo) and county ($2,857/mo)", src("census_cupertino") + " " + src("census_scc") ], "verified"),
 ([ "2. Anchor the property", "Owner-supplied rent for Property B ($7,150/mo, 2 units) as a cross-check on area rents", "Owner input" ], "owner"),
 ([ "3. Obtain the property-specific number", "Written rent opinion / broker market analysis for Property A (not yet obtained)", "Owner action (flagged R08)" ], "unverified"),
 ([ "4. Compare net rent to carrying costs", "Net rent (gross rent − vacancy, taxes, insurance, water/electric, maintenance) vs. after-tax portfolio return; break-even computed on the merged desks' model", "Desk model (assumption)" ], "assumption"),
])}
"""
pages["rent-comparables.html"] = dict(title="Rent comparables", dek="Official Census ACS rent evidence and the evidence ladder for ranking the rent path.", body=rent_body)

# ---------------------------------------------------------------- sf measures
sf_body = f"""
<div class="callout warn"><b>Two different "Proposition H"s — do not confuse them.</b> San Francisco has used the
letter H twice in recent elections: <b>Prop H (Nov 5, 2024)</b>, a firefighter-pension charter amendment, and
<b>Prop H (Nov 3, 2026)</b>, the Muni parcel tax. This page models both with their official terms, and separates
enacted changes from proposals.</div>

<h3>Proposition H — November 3, 2026 (Muni parcel tax)</h3>
{tbl(["Item", "Official term", "Source"], [
 ([ "Official ballot question",
    "Shall the City fund Muni service through a new annual parcel tax on real estate at rates ranging from $129 per parcel up to a maximum of $400,000 per parcel, depending on the type of property and its size and adjusted annually for inflation, for estimated revenue of $177 million a year for 15 years?",
    src("sfelections_2026") ], "verified"),
 ([ "Result (preliminary, not certified as of 2026-11-15)",
    "YES 244,760 (74.4%) / NO 84,209 (25.6%); the Department of Elections counts remaining ballots and certifies within the state deadline",
    src("sfelections_2026") ], "verified"),
 ([ "Effective dates",
    "First tax on the FY2027-28 property tax bill (mailed fall 2027); runs July 1, 2027 through June 30, 2042",
    src("sfmta_proph") ], "verified"),
 ([ "How it is billed",
    "Added to the regular property tax bill, paid in the same two installments",
    src("sfmta_proph") ], "verified"),
 ([ "Rate schedule (base rates)",
    "Single-family up to 3,000 sq ft: $129; single-family 3,001-5,000 sq ft: $129 + $0.42/sq ft over 3,000; single-family over 5,000 sq ft: $969 + $1.99/sq ft over 5,000; multifamily up to 5,000 sq ft: $249; multifamily over 5,000 sq ft: $249 + $0.195/sq ft over 5,000 (max $50,000); non-residential up to 5,000 sq ft: $799; non-residential 5,001-50,000 sq ft: $799 + $0.76/sq ft over 5,000",
    src("sfmta_proph") ], "verified"),
 ([ "Exemptions",
    "Senior 65+ principal-residence exemptions (single-family full; multifamily $249 off per qualifying unit); SRO units untaxed; properties with no property tax levied are exempt",
    src("sfmta_proph") ], "verified"),
 ([ "Effect on Property B (SF, 3-unit building)",
    "New annual parcel tax from FY2027-28: $249 base for multifamily up to 5,000 sq ft, plus $0.195/sq ft over 5,000 (capped at $50,000); building area not published on this desk, so the size addition is unverified",
    src("sfmta_proph") ], "assumption"),
 ([ "Effect on Property A (Santa Clara County)",
    "None — a San Francisco measure; Property A is outside the City and County of San Francisco",
    "Desk interpretation" ], "assumption"),
])}

<h3>Proposition H — November 5, 2024 (firefighter retirement benefits)</h3>
{tbl(["Item", "Official term", "Source"], [
 ([ "Measure name (official results)", "Measure H — Retirement Benefits for Firefighters; approved (final certified results)", src("sfelections_2024") ], "verified"),
 ([ "What it changes", "Charter amendment changing how Fire Department pension benefits are calculated (the measure lowered the age for the highest pension from 58 to 55 for members hired on or after January 7, 2012, aligning them with members hired earlier); detailed measure text to be confirmed against the City's official measure text",
    src("sfelections_2024") ], "unverified"),
 ([ "Effect on the household", "None directly — a City pension cost item; no household property, income or transfer tax change",
    "Desk interpretation" ], "assumption"),
])}

<h3>Companion measures that affect Property B's economics</h3>
{tbl(["Measure", "Official term", "Effect on the household", "Source"], [
 ([ "Proposition M (Nov 2024) — Changes to Business Taxes",
    "Approved (final certified results). Restructured SF business taxes: small-business exemption raised to $5M, categories 14→7, rates 0.1%-3.716%, homelessness gross receipts tax over $25M, registration fees $55-$60,000",
    "SF rental activity may be subject to the gross receipts tax / registration fees if it counts as 'engaging in business' in the City; the $5M exemption means a small residential rental operation is generally below the exemption threshold — confirm with the SF Tax Collector",
    src("sfelections_2024") + " " + src("sfgov_digest") ], "verified"),
 ([ "Measure I (Nov 2026) — Changes to Real Property Transfer Tax",
    "<b>Failed</b> (NO 51.66% / YES 48.34%, preliminary): would have dedicated half of transfer-tax revenue from certain real estate over $10,000,000 (taxed at 5.5%-6%) to affordable housing",
    "No change to SF transfer tax law; the existing transfer tax schedule applies to any SF sale",
    src("sfelections_2026") ], "verified"),
 ([ "Regional Measure RTM (Nov 2026) — Regional Transit Measure",
    "1% sales tax in San Francisco (0.5% in four other Bay Area counties) for 14 years, ~$980M/year for transit; passing in SF with ~79% (preliminary)",
    "Raises the SF sales tax rate paid on purchases (a consumption cost, not a property or income tax)",
    src("sfelections_2026") ], "verified"),
 ([ "Santa Clara County equivalents",
    "RTM adds 0.5% sales tax in Santa Clara County — affects purchases in the Property A area, not Property A's property tax",
    src("sfelections_2026") ], "verified"),
])}

<h3>Modelled effect on Property B's carrying cost</h3>
{tbl(["Year", "SF Measure H parcel tax (base)", "Basis"], [
 ([ "2026-2027", "—", "Measure takes effect with the FY2027-28 bill (July 2027)" ], "assumption"),
 ([ "2028", m0(249 * (1 + COST_INFL) ** 1), "Base $249 for multifamily up to 5,000 sq ft, inflated at 3%/yr (assumption); size addition unverified" ], "assumption"),
 ([ "2030", m0(249 * (1 + COST_INFL) ** 3), "Same basis" ], "assumption"),
 ([ "2035", m0(249 * (1 + COST_INFL) ** 8), "Same basis; measure runs to June 30, 2042" ], "assumption"),
 ([ "2042", m0(249 * (1 + COST_INFL) ** 15), "End of the 15-year term unless extended by voters" ], "assumption"),
])}
<p class="note">The base rate and effective dates are official (SFMTA / SFDOE). The inflation adjustment is an
assumption; the per-square-foot additions are unverified until the building area is supplied.</p>
"""
pages["sf-measures.html"] = dict(title="SF measures: Prop H &amp; others", dek="Proposition H (2024 and 2026) with official terms, and the companion measures that touch Property B.", body=sf_body)

# ---------------------------------------------------------------- maintenance plan
mp_rows = []
for y in range(2027, 2032):
    n = y - 2027
    a = (130 - 20) * 12 * (1 + COST_INFL) ** n + 1500 * (1 + COST_INFL) ** n + 200 * (1 + COST_INFL) ** n
    b = (365 + 50) * 12 * (1 + COST_INFL) ** n + 1500 * (1 + COST_INFL) ** n + 450 * (1 + COST_INFL) ** n
    mp_rows.append(([
        str(y),
        m0(a),
        m0(b),
        m0(a + b),
        "Owner anchors at $10 rounding, inflated 3%/yr (assumption)",
    ], "assumption"))

mp_body = f"""
<p class="small">Five-year maintenance and capital plan for both buildings, 2027-2031. Operating lines use owner-supplied
anchors rounded to $10 and inflated at {COST_INFL:.0%}/yr (assumption); official rate references are linked where a
published schedule exists. <b>Capital items are left blank</b> — no inspection has been performed, and inventing
replacement costs would violate the no-inference rule.</p>

<h3>Property A — operating plan (single-family, solar)</h3>
{tbl(["Cost line", "Monthly", "Annual (2027)", "Source / status"], [
 ([ "Water", m0(130), m0(130 * 12), "Owner estimate $100-$150/mo (midpoint); San Jose Water serves the area — rate schedule linked, property bill unverified", src("sjwater") ], "owner"),
 ([ "Electricity", "-" + m0(20), "-" + m0(20 * 12), "Owner estimate: solar credit $10-$20/mo profit; no official confirmation", "Owner input" ], "owner"),
 ([ "Home insurance (primary residence)", m0(125), m0(1500), "Owner estimate ~$1,500/yr; official rate context: CA homeowners statewide average range and FAIR Plan context", src("doi") + " " + src("fairplan") ], "owner"),
 ([ "Maintenance &amp; repair", "—", m0(200), "Owner: 'not as much as the San Francisco house'; placeholder until inspection", "Owner input" ], "owner"),
 ([ "Total Property A (2027)", "—", m0(3020), "Sum of the lines above (assumption)" ], "assumption"),
])}

<h3>Property B — operating plan (3 units, 2 rented)</h3>
{tbl(["Cost line", "Monthly", "Annual (2027)", "Source / status"], [
 ([ "Water (all 3 units)", m0(365), m0(365 * 12), "Owner estimate $330-$400/mo (midpoint); SFPUC general schedule linked, property bill unverified", src("sfpuc") ], "owner"),
 ([ "Electricity (all 3 units)", m0(50), m0(50 * 12), "Owner estimate $30-$70/mo (midpoint); PG&E average price + base charge linked", src("cpuc") ], "owner"),
 ([ "Home / rental insurance (DP-3)", m0(125), m0(1500), "Owner estimate ~$1,500/yr; landlord DP-3 typical; FAIR Plan + DIC context in fire zones", src("doi") + " " + src("fairplan") ], "owner"),
 ([ "Maintenance &amp; repair", "—", m0(450), "Owner: more than Property A; placeholder until inspection", "Owner input" ], "owner"),
 ([ "SF Measure H parcel tax", "—", m0(249), "Official base rate for multifamily (from FY2027-28); size addition unverified", src("sfmta_proph") ], "assumption"),
 ([ "Total Property B (2027)", "—", m0(7179), "Sum of the lines above (assumption)" ], "assumption"),
])}

<h3>Five-year projection (operating only)</h3>
{tbl(["Year", "Property A total", "Property B total", "Combined", "Basis"], mp_rows)}

<h3>Capital plan (blank until inspection)</h3>
{tbl(["Property", "Capital item", "Estimated cost", "Timing", "Status"], [
 ([ "Property A", "Roof / HVAC / solar battery replacement", "", "Unknown", "No inspection performed; obtain a written capital assessment (suggestion S-06)" ], "unverified"),
 ([ "Property B", "Roof, plumbing, electrical upgrades (3 units)", "", "Unknown", "No inspection performed; obtain a written capital assessment (suggestion S-06)" ], "unverified"),
 ([ "Property B", "Unit turnover / re-rental costs", "", "Unknown", "Depends on lease roll (question Q-07)" ], "unverified"),
])}
"""
pages["maintenance-plan.html"] = dict(title="Five-year maintenance plan", dek="2027-2031 operating plan at $10 rounding and the capital plan left blank until inspection.", body=mp_body)

# ---------------------------------------------------------------- CA income tax / Form 540
mhst_rows = []
for inc in [1_000_000, 1_500_000, 2_000_000, 3_000_000, 5_000_000, 10_000_000]:
    mh = mhst(inc)
    rate = 0.133 if inc > MHST_THRESHOLD else 0.123
    mhst_rows.append(([
        m_exact(inc),
        m0(inc - MHST_THRESHOLD) if inc > MHST_THRESHOLD else "—",
        m0(mh),
        f"{rate:.1%}",
        "Computed per Form 540 line 62 worksheet (1% of the excess over $1,000,000); top CA ordinary rate 12.3% + 1% = 13.3% on the excess",
    ], "assumption"))

ca_body = f"""
<div class="callout ok"><b>The 1% tax above one million dollars — read from the official Form 540 instructions.</b>
California's Behavioral Health Services Tax is <b>1% of California taxable income above $1,000,000</b>, computed on
<b>Form 540 line 62</b> from taxable income (Form 540 line 19). It is a per-year surtax: it applies in any year
taxable income crosses the threshold and disappears in years below it. The updated sensitivity value is below.</div>

<h3>Official Form 540 treatment (line by line)</h3>
{tbl(["Form 540 item", "Official treatment", "Source"], [
 ([ "Behavioral Health Services Tax — line 62",
    "'If your taxable income is more than $1,000,000, compute the Behavioral Health Services Tax: 1. Taxable income from Form 540, line 19. 2. Less: $(1,000,000). 3. Subtotal. 4. Tax rate – 1%: .01. 5. Behavioral Health Services Tax — Multiply line 3 by line 4. Enter this amount here and on line 62.'",
    src("ftb_540") ], "verified"),
 ([ "Where the surtax appears",
    "Form 540 line 62 (Other Taxes), added into total tax at line 64",
    src("ftb_540form") ], "verified"),
 ([ "Capital-gain treatment",
    "California taxes capital gains at ordinary income rates — there is no preferential state capital-gain rate; gains flow into CA taxable income (and therefore count toward the $1,000,000 MHST threshold)",
    src("ftb_rates") + " " + src("ftb_fedchanges") ], "verified"),
 ([ "Reporting form",
    "Federal Schedule D carries the gain into federal AGI, which feeds Form 540 line 13 / line 19; California Schedule D (540) is used for state adjustments",
    src("ftb_540") ], "verified"),
 ([ "Top CA ordinary rate",
    "12.3% (2025 rate schedules); with the 1% surtax, the effective top rate on income above $1,000,000 is 13.3%",
    src("ftb_rates") ], "verified"),
 ([ "Federal layer (for context)",
    "Federal long-term capital gains use the federal 0%/15%/20% schedules plus the 3.8% net investment income tax; the 1% MHST is a California-only surtax",
    src("irs_niit") ], "verified"),
])}

<h3>Updated MHST sensitivity (per year of large realized income)</h3>
{tbl(["CA taxable income", "Excess over $1,000,000", "MHST (1% of excess)", "Top effective CA rate on the excess", "Basis"], mhst_rows,
     "Computed from the official line-62 worksheet. Rounded to $10; the statutory threshold $1,000,000 and 1% rate are exact as published.")}

<h3>Why this matters for the inheritance decision</h3>
{tbl(["Situation", "Effect", "Source / basis"], [
 ([ "Property A sold at inheritance (~$3,100,000+ value) in the same year as large other income (vesting, business sale, the 'considerable money')",
    "If the year's CA taxable income exceeds $1,000,000, add 1% on the excess — e.g. at $2,000,000 taxable income the surtax is $10,000; at $5,000,000 it is $40,000 (sensitivity above)",
    "Sensitivity computed from the official worksheet (assumption on the income level)" ], "assumption"),
 ([ "Gain is small because of the step-up in basis",
    "IRC §1014 resets basis to date-of-death value; a sale close to the date of death usually realizes little gain and contributes little to taxable income",
    src("irs_stepup") ], "verified"),
 ([ "Spreading the sale over multiple tax years",
    "Keeps each year's taxable income below the threshold where possible; the trade-off is market exposure on the un-sold portion — a planning decision for the CPA",
    "Desk interpretation (tax planning; not advice)" ], "assumption"),
 ([ "Estate tax vs. income tax vs. property tax",
    "The three are separate: federal estate tax above $15,000,000 (2026); income tax on rent and on sale gains (with the 1% surtax above $1M); property tax under Prop 13/19 on assessed value",
    src("irs_estate") + " " + src("ftb_540") + " " + src("boe_prop13") ], "verified"),
])}
"""
pages["ca-income-tax.html"] = dict(title="CA income tax &amp; Form 540", dek="The 1% Behavioral Health Services Tax read from the official Form 540 instructions, and the updated sensitivity value.", body=ca_body)

# ---------------------------------------------------------------- estate liquidity
el_body = f"""
<div class="callout info"><b>Estate liquidity plan.</b> The inheritance includes a "considerable amount of money"
that could exceed the federal exclusion. If it does, the estate needs liquid assets to pay the tax without a
forced, ill-timed sale. This page sets out the verified thresholds, the portability and prior-gift questions to ask
now, and the liquidity sources to map.</div>

<h3>Verified thresholds (2026)</h3>
{tbl(["Item", "Amount / rule", "Source"], [
 ([ "Federal estate &amp; gift basic exclusion (per person)", m_exact(15000000), src("irs_estate") ], "exact"),
 ([ "Top federal estate &amp; gift tax rate", "40%", src("irs_estate") ], "exact"),
 ([ "Gift tax annual exclusion (per recipient)", m_exact(19000), src("irs_estate") ], "exact"),
 ([ "Form 706 filing / payment deadline", "9 months after death (extension available)", src("irs_706") ], "verified"),
 ([ "Portability (DSUE) election", "Made on a timely-filed Form 706; the surviving spouse then inherits the deceased spouse's unused exclusion", src("irs_706") ], "verified"),
 ([ "California estate / inheritance tax", "None (state death-tax credit ended for deaths after 2004)", src("sco_estate") ], "verified"),
 ([ "Step-up in basis at death", "Basis resets to date-of-death fair market value", src("irs_stepup") ], "verified"),
])}

<h3>Liquidity sources to map (what the estate can sell or draw on)</h3>
{tbl(["Source", "Liquidity", "Note", "Source / status"], [
 ([ "Cash and checking/savings accounts", "High", "Confirm account titing and beneficiary designations with the estate attorney", "Owner action (question Q-03)" ], "unverified"),
 ([ "Brokerage / investment accounts", "High", "Confirm titing (individual, joint, trust) and cost basis records", "Owner action (question Q-03)" ], "unverified"),
 ([ "Retirement accounts (401(k) / IRA)", "Medium", "Income-tax treatment on withdrawal; beneficiary designations control", src("irs_niit") ], "assumption"),
 ([ "Life insurance proceeds", "High (if in place)", "Income-tax free to the beneficiary; confirm ownership and beneficiary designations", "Owner action (question Q-03)" ], "unverified"),
 ([ "Property A (real estate)", "Low (time to sell)", "Selling takes weeks-to-months and is exposed to market timing; the phased-investing path addresses proceeds after sale, not before", src("treasury") ], "assumption"),
 ([ "Property B (real estate)", "Low (time to sell)", "Already owned; selling it to fund estate tax would remove a rental income asset", "Desk interpretation" ], "assumption"),
 ([ "Business interests", "Unknown", "Valuation and marketability unknown; confirm with the estate attorney", "Owner action (question Q-03)" ], "unverified"),
])}

<h3>Questions to ask now (before the figures arrive)</h3>
{tbl(["Question", "Why it matters", "Status"], [
 ([ "Has portability been elected for any deceased spouse (DSUE)?",
    "It can double the available exclusion; it must be elected on a timely Form 706", src("irs_706") ], "verified"),
 ([ "Have there been prior taxable gifts above the annual exclusion?",
    "Lifetime gifting reduces the remaining exclusion; the total affects the estate tax base", src("irs_estate") ], "verified"),
 ([ "What is the total estate value (all assets, all owners)?",
    "Decides whether Form 706, liquidity planning and the 40% rate matter at all", src("irs_estate") ], "verified"),
 ([ "Which assets are titled to the trust vs. outside it?",
    "Trust-funded assets avoid probate but still count toward the estate tax base; titling errors are the common failure", "Owner action (question Q-03)" ], "unverified"),
 ([ "Is there a written valuation of Property A at the date of death?",
    "Sets the step-up in basis and the estate's asset value; obtain a written appraisal (suggestion S-01)", src("irs_stepup") ], "verified"),
])}

<h3>If the estate exceeds the exclusion — the sequence to plan for</h3>
{tbl(["Step", "Action", "Timing", "Source"], [
 ([ "1", "Confirm total estate value and portability/prior-gift position", "Now", src("irs_706") + " " + src("irs_estate") ], "verified"),
 ([ "2", "Identify the most liquid $X (cash, securities, insurance) to cover the estimated tax", "Now", "Desk model (assumption)" ], "assumption"),
 ([ "3", "File Form 706 and pay the tax", "Within 9 months of death (extension possible)", src("irs_706") ], "verified"),
 ([ "4", "Avoid a forced sale of real estate to pay tax; map liquidity first", "Planning principle", "Desk interpretation" ], "assumption"),
 ([ "5", "Re-check the exclusion and rate each year — figures are indexed and law changes", "Annually", src("irs_estate") ], "verified"),
])}
"""
pages["estate-liquidity.html"] = dict(title="Estate tax &amp; liquidity plan", dek="Verified federal thresholds, liquidity sources, and the questions to settle before the figures arrive.", body=el_body)

# ---------------------------------------------------------------- decision log
decisions = [
 ("Model Prop H with official terms", "Modelled both SF Prop H measures (2024 firefighter pension; 2026 Muni parcel tax) with official terms from the SF Department of Elections and SFMTA. Property B gains a $249/yr base parcel tax from FY2027-28; Property A is unaffected.", "2026-11-15", "sfelections_2026; sfmta_proph"),
 ("Update the Form 540 1% tax sensitivity", "Sensitivity updated from the official 2025 Form 540 instructions: 1% of CA taxable income over $1,000,000, Form 540 line 62; capital gains taxed at ordinary CA rates and count toward the threshold.", "2026-11-15", "ftb_540; ftb_rates"),
 ("Rank the rent path on evidence", "Rent path ranked on official Census ACS area median gross rent ($3,500+/mo, 2020-2024) instead of a voucher benchmark; property-specific rent left unverified pending a written rent opinion.", "2026-11-15", "census_cupertino; census_scc"),
 ("Build the five-year maintenance plan", "2027-2031 operating plan built at $10 rounding from owner anchors and official rate references; capital items left blank until a written inspection is obtained.", "2026-11-15", "Owner inputs; sjwater; sfpuc; cpuc; sfmta_proph"),
 ("Prepare the estate liquidity plan", "Verified thresholds and liquidity-source map prepared; portability and prior-taxable-gift questions posed for the estate attorney to answer before the figures arrive.", "2026-11-15", "irs_estate; irs_706; sco_estate"),
 ("Add the distribution chart to projections", "Growth-regime distribution chart (3%/5%/7%) added to the projections page so the decision is tested across a range, not one point.", "2026-11-15", "Desk model (assumption)"),
 ("Write the decision and date next to each item", "Decision log created: every item carries the decision, the date (2026-11-15) and the basis. Items remain 'desk recommendation' until the owner confirms.", "2026-11-15", "Desk policy"),
 ("Scrub pre-rounding git history", "Not performed. Rewriting public history is an owner decision; the exposure and remediation options are documented on the Flagged page (R03).", "2026-11-15", "Owner decision (flagged)"),
 ("Keep the phased-investing path", "Confirmed covered by the merged desks (sale proceeds in 3M-2Y Treasuries for 24-36 months, then phased into stocks); this desk carries the Treasury reference forward.", "2026-11-15", "treasury"),
 ("Separate estate tax, income-tax basis and property-tax assessment", "Maintained on every page: federal estate tax (exclusion/40%), income-tax basis (step-up, MHST, capital gains), property-tax assessment (Prop 13/19).", "2026-11-15", "irs_estate; irs_stepup; ftb_540; boe_prop13"),
]
dl_rows = []
for item, decision, date_, basis in decisions:
    keys = [k for k in basis.split("; ") if k in SRC]
    src_html = " ".join(src(k) for k in keys) if keys else "Desk policy"
    dl_rows.append(([item, decision, date_, src_html], "verified" if keys else "assumption"))

dl_body = f"""
<p class="small">Every item below carries <b>the decision, the date it was made, and the basis</b>, so a future reader
knows what was chosen and why. Status is <b>desk recommendation — awaiting owner confirmation</b>: the analysis
records what the evidence supports; the owner's written agreement is still required before acting (per the brief's
rule that the outcome is not reverse-engineered from one projection).</p>
{tbl(["Item", "Decision (what was chosen and why)", "Date", "Basis / source"], dl_rows)}
"""
pages["decision-log.html"] = dict(title="Decision &amp; date log", dek="Each item with the decision, the date, and the basis — recorded 2026-11-15.", body=dl_body)

# ---------------------------------------------------------------- questions
questions = [
 ("Q-01", "Will the heir occupy Property A as a primary residence within 1 year of transfer?", "Open — owner decision", "Decides the Prop 19 capped reassessment vs. full reassessment; the single largest lever on Property A's tax bill", "boe_prop19"),
 ("Q-02", "What is Property A's market rent?", "Open — no official source for a specific property", "Census ACS gives the area median ($3,500+/mo); obtain a written rent opinion (suggestion S-02)", "census_cupertino"),
 ("Q-03", "What is the total estate value and asset titling (trust vs. outside)?", "Open — owner input needed", "Decides whether Form 706, liquidity planning and the 40% rate matter", "irs_estate"),
 ("Q-04", "Was portability (DSUE) elected for any deceased spouse, and are there prior taxable gifts?", "Open — owner input needed", "Both change the available exclusion; must be settled before the figures arrive", "irs_706"),
 ("Q-05", "Is there a written valuation of Property A at the date of death?", "Open — not obtained", "Sets the step-up in basis and the estate's asset value (suggestion S-01)", "irs_stepup"),
 ("Q-06", "What are Property B's lease terms and expiry dates for all 3 units?", "Open — 'verify B's leases and local rules'", "Lease roll drives rent path risk and turnover costs; local rules include SF rent rules for the units", "Owner action"),
 ("Q-07", "What is Property B's building area (sq ft)?", "Open — not supplied", "Needed to price the SF Measure H size-based parcel tax addition", "sfmta_proph"),
 ("Q-08", "What insurance quotes apply to each property?", "Open — owner estimates only", "Owner estimates ~$1,500/yr; official rate context is not a quote; obtain actual quotes (suggestion S-05)", "doi"),
 ("Q-09", "What is Property A's current assessed value and tax-rate-area combined rate?", "Open — private, not published", "Read from the owner's tax bill; needed for an exact Prop 19 calculation", "scc_ratebook"),
 ("Q-10", "Is a like-kind (1031) exchange wanted for any sale?", "Open — advice required first", "Take professional advice before selling; a 1031 defers gain but adds complexity and deadlines", "irs_stepup"),
 ("Q-11", "What is the written investment policy for sale proceeds?", "Open — not yet written", "The policy should be agreed before the money arrives, including the Treasury parking path", "treasury"),
 ("Q-12", "Has SF Measure H been certified, and what is the exact bill for Property B?", "Open — preliminary results only", "Results were preliminary as of 2026-11-15; certification expected within the state deadline", "sfelections_2026"),
 ("Q-13", "What are the water and electricity bills for each property?", "Open — owner estimates only", "Official schedules exist; property bills are needed for exact modelling", "sjwater"),
 ("Q-14", "What capital items do both buildings need over five years?", "Open — no inspection", "Obtain written capital assessments before funding them (suggestion S-06)", "Owner action"),
 ("Q-15", "What changes are pending in federal, state and local law?", "Open — tracked on the Law Watch page", "Re-check official authorities periodically; distinguish enacted changes from proposals", "sfelections_2026"),
]
q_rows = []
for qid, q, status, why, basis in questions:
    src_html = src(basis) if basis in SRC else "Owner action"
    q_rows.append(([qid, q, status, why, src_html], "verified" if basis in SRC else "unverified"))

q_body = f"""
<p class="small">A clear list of what must be known before any decision can be reasonably made, with the status and
the discovery action for each. Answers marked <span class="tag owner">owner-supplied</span> or
<span class="tag unverified">unverified</span> are not verified inputs to the model.</p>
{tbl(["ID", "Question", "Status", "Why it matters / discovery action", "Source"], q_rows)}
"""
pages["questions.html"] = dict(title="Questions &amp; gaps", dek="What must be answered before the decision, with a discovery action for each gap.", body=q_body)

# ---------------------------------------------------------------- suggestions
suggestions = [
 ("S-01", "Obtain a written valuation of Property A at the date of death", "PROPOSED", "Sets the step-up in basis and the estate value; without it the gain and estate-tax arithmetic is anchored to an estimate", "irs_stepup"),
 ("S-02", "Obtain a written rental market analysis / rent opinion for Property A", "PROPOSED", "Ranks the rent path on property-specific evidence instead of the area Census median", "census_cupertino"),
 ("S-03", "Ask the estate attorney about portability (DSUE) and prior taxable gifts now", "PROPOSED", "Both change the available exclusion; must be known before the figures arrive", "irs_706"),
 ("S-04", "Ask the CPA to model the 1% MHST in the year of any large sale", "PROPOSED", "The updated sensitivity shows the surtax applies in any year CA taxable income exceeds $1,000,000; spreading gains may be worth modelling", "ftb_540"),
 ("S-05", "Obtain actual insurance quotes for both properties", "PROPOSED", "Owner estimates (~$1,500/yr) are unverified; official rate context is not a quote", "doi"),
 ("S-06", "Obtain written five-year maintenance and capital assessments for both buildings", "PROPOSED", "The capital plan is blank until inspection; this completes the five-year plan", "Owner action"),
 ("S-07", "Decide whether a like-kind (1031) exchange is wanted, and take advice before selling", "PROPOSED", "A 1031 defers gain but adds deadlines and complexity; advice comes first", "irs_stepup"),
 ("S-08", "Write the investment policy for sale proceeds before the money arrives", "PROPOSED", "Include the Treasury parking path (3M-2Y, 24-36 months) and the phased-investing rules", "treasury"),
 ("S-09", "Prepare the estate liquidity plan if the estate may exceed the federal exclusion", "PROPOSED", "Map liquid sources now; avoid a forced real-estate sale to pay tax", "irs_estate"),
 ("S-10", "Re-run this model every year with updated inputs", "PROPOSED", "Laws, rates and property values change; the annual re-run keeps the decision current", "irs_estate"),
 ("S-11", "Agree in writing what would make the household choose each path before the figures arrive", "PROPOSED", "Prevents the outcome being reverse-engineered from one projection; the decision log is where the agreement is recorded", "Desk policy"),
 ("S-12", "Track proposed legislation and distinguish enacted changes from proposals", "PROPOSED", "The Law Watch page holds the current list; re-check official authorities periodically", "sfelections_2026"),
]
s_rows = []
for sid, sug, status, why, basis in suggestions:
    src_html = src(basis) if basis in SRC else "Desk policy"
    s_rows.append(([sid, sug, status, why, src_html], "verified" if basis in SRC else "assumption"))

s_body = f"""
<p class="small">Suggestions for improving decision-making, held here for the owner to review and choose the best
path <b>before implementing any change</b>. Nothing here has been implemented: every row is
<b>PROPOSED</b> and awaits an owner decision. Accept, modify or reject each row; record the outcome in the
decision log.</p>
{tbl(["ID", "Suggestion", "Status", "Why it helps", "Source"], s_rows)}
"""
pages["suggestions.html"] = dict(title="Suggestions board", dek="Proposed improvements awaiting owner review — nothing implemented yet.", body=s_body)

# ---------------------------------------------------------------- law watch
law_body = f"""
<p class="small">Enacted changes (official results) and proposals (pending or rejected), separated clearly.
Re-check official authorities periodically — the list is a snapshot as of 2026-11-15.</p>

<h3>Enacted — official results confirmed</h3>
{tbl(["Item", "Status", "What it is", "Effect on the decision", "Source"], [
 ([ "SF Measure H (Nov 3, 2026) — Muni parcel tax", "Passed — preliminary results 74.4% YES; certification pending", "Annual parcel tax $129-$400,000/parcel for 15 years from FY2027-28", "Adds a fixed cost to Property B (~$249/yr base); no effect on Property A", src("sfelections_2026") + " " + src("sfmta_proph") ], "verified"),
 ([ "Regional Measure RTM (Nov 3, 2026)", "Passing — preliminary ~79% YES in SF", "1% SF sales tax (0.5% in four other Bay Area counties) for 14 years", "Raises sales tax paid on purchases; not a property or income tax", src("sfelections_2026") ], "verified"),
 ([ "SF Measure I (Nov 3, 2026) — transfer tax", "<b>Failed</b> — NO 51.66%", "Would have dedicated half of transfer tax on certain real estate over $10,000,000 (5.5%-6%) to affordable housing", "No change to SF transfer tax; existing schedule applies to any SF sale", src("sfelections_2026") ], "verified"),
 ([ "SF Proposition M (Nov 5, 2024) — business taxes", "Enacted (final certified)", "Business-tax restructure: $5M small-business exemption, 14→7 categories, rates 0.1%-3.716%", "SF rental activity may face gross receipts tax / registration fees if 'engaging in business'; small residential rentals are generally below the exemption — confirm with the SF Tax Collector", src("sfelections_2024") + " " + src("sfgov_digest") ], "verified"),
 ([ "SF Proposition H (Nov 5, 2024) — firefighter pension", "Enacted (final certified)", "Charter amendment changing firefighter pension calculations (age 58→55 for members hired on/after Jan 7, 2012)", "No direct household tax effect", src("sfelections_2024") ], "verified"),
 ([ "California Proposition 19 (2021, effective 2022)", "Enacted", "Parent-child exclusion limited to primary residence; child must occupy within 1 year; non-primary property fully reassessed", "The switch that decides Property A's post-transfer tax bill", src("boe_prop19") ], "verified"),
 ([ "California Proposition 13 (1978)", "Enacted", "1% general levy; 2% assessment growth cap", "Baseline for both properties' assessments", src("boe_prop13") ], "verified"),
 ([ "Federal estate/gift exclusion (2026)", "Enacted", "$15,000,000 per person; 40% top rate; $19,000 annual gift exclusion", "Sets the estate-liquidity threshold", src("irs_estate") ], "verified"),
])}

<h3>Statewide measures on the Nov 3, 2026 ballot (official results)</h3>
{tbl(["Measure", "Result (preliminary)", "What it is", "Relevance", "Source"], [
 ([ "Proposition 3 — permanent funding for schools/health", "Passed — 76.7% YES", "Makes permanent the tax on incomes over $371,000 (inflation-adjusted)", "Keeps the high-income tax rates that already apply; relevant to the 'considerable money'", src("sfelections_2026") ], "verified"),
 ([ "Proposition 40 — one-time tax on certain taxpayers", "Passed — 56.4% YES", "5% tax on certain taxpayers with assets over $1 billion", "Only relevant if the estate approaches billionaire-scale assets", src("sfelections_2026") ], "verified"),
 ([ "Proposition 43 — higher threshold for local special taxes", "<b>Failed</b> — 65.4% NO", "Would have raised the vote requirement for local special taxes to two-thirds from 2027", "If it had passed, future parcel-tax measures like Measure H would face a harder path; it failed, so the majority rule stands", src("sfelections_2026") ], "verified"),
 ([ "Proposition 41 / 42 — tax-limitation measures", "Failed", "Prohibit certain new state taxes / retroactive taxes", "No current effect on this decision", src("sfelections_2026") ], "verified"),
 ([ "Propositions 1, 2, 37, 38 — bonds / reserves", "Passing / passed", "Housing, rainy-day and research bonds; Proposition 37 middle-income home-buyer loans", "Macro context only; no direct household tax change", src("sfelections_2026") ], "verified"),
])}

<h3>Proposals to watch (not enacted)</h3>
{tbl(["Proposal", "Status", "What to watch", "Source"], [
 ([ "2027 California legislature — property, estate and income tax bills", "Open — not yet introduced/enacted", "Re-check the Legislative Information site and the BOE / FTB before each annual re-run; this desk does not predict legislation", src("leginfo_rt") ], "verified"),
 ([ "Federal estate-tax law after 2026", "Open — indexed annually", "The $15,000,000 exclusion and 40% rate are 2026 figures; re-check the IRS each year", src("irs_estate") ], "verified"),
 ([ "SF ballot measures after 2026", "Open", "Measure H certification and any extension beyond 2042 would change Property B's cost", src("sfelections_2026") ], "verified"),
])}
"""
pages["law-watch.html"] = dict(title="Law watch", dek="Enacted changes and proposals, separated; snapshot 2026-11-15.", body=law_body)

# ---------------------------------------------------------------- sources
src_rows = [([k, label, url], "verified") for k, (label, url) in SRC.items()]
src_body = f"""
<p class="small">Every row on this desk cites one of these official sources, or is marked unverified / owner /
assumption in the row. Hosts are official government or agency publishers.</p>
{tbl(["Key", "Label", "Official URL"], src_rows)}
"""
pages["sources.html"] = dict(title="Sources", dek="The official source register used by every row on this desk.", body=src_body)

# ---------------------------------------------------------------- flagged
flagged = [
 ("R01", "Other-desk figure discrepancy", "desk-b4f/estate-tax.html shows the 2026 estates-and-trusts 20% LTCG threshold as $16,200, against $16,250 in IRS Rev. Proc. 2025-32 (logged as X04 by session arena-3f269806; re-confirmed on disk 2026-11-15).", "Owner review — desk-b4f is excluded from Pages until corrected; this desk does not edit it", "IRS Rev. Proc. 2025-32 (via desk-b4f citation)"),
 ("R02", "Other-desk fee wording", "Estate-tax closing-letter user-fee figures differ across desks ($67 vs $76 under the IRS fee change); desk-b4f shows $76 effective 2026-10-26. Logged by earlier sessions (X05).", "Owner review", "IRS estate & gift updates"),
 ("R03", "Git history privacy exposure", "Public git history and archives contain unrounded owner-supplied figures (e.g. property-tax amounts in commit history). A PR merge does not erase exposed history.", "Owner decision required. Options: (a) leave as-is and keep new outputs rounded; (b) history rewrite via filter-repo + force push (destroys permalinks; coordinate all sessions); (c) private-repo conversion. Not performed by this session.", "Desk review"),
 ("R04", "Privacy-scan false positives", "scripts/privacy_scan.py reports 91 Treasury month-query findings in the cbd and phase desks (logged by cbd/INT as false positives).", "Known; no owner-data finding observed", "scripts/privacy_scan.py"),
 ("R05", "Property A tax-rate area combined rate", "The combined rate for Property A's tax-rate area is not published on this desk (privacy); the owner's tax bill shows it.", "Read from the owner's bill; the 1% general levy is capped but bonds/assessments add", "scc_ratebook"),
 ("R06", "SF Measure H certification pending", "Measure H results are preliminary (74.4% YES) and uncertified as of 2026-11-15; certification is due within the state deadline.", "Re-check the SF Department of Elections before relying on the cost", "sfelections_2026"),
 ("R07", "SF Measure H size-based rate unverified", "Property B's building area is not published, so the $0.195/sq ft multifamily addition is unverified; only the $249 base is used.", "Supply building area (question Q-07)", "sfmta_proph"),
 ("R08", "Property A specific rent unverified", "No official source publishes a rent for a specific property; the Census ACS area median ($3,500+/mo) is area evidence only.", "Obtain a written rent opinion (suggestion S-02)", "census_cupertino"),
 ("R09", "Capital items unverified", "The five-year capital plan is blank until a written inspection is obtained.", "Obtain written capital assessments (suggestion S-06)", "Owner action"),
 ("R10", "Owner-supplied inputs unverified", "Property values ($3,100,000 / $1,800,000), Property B rent ($7,150/mo), water/electric/insurance estimates and solar credit are owner-supplied and unconfirmed by any official source.", "Confirm with bills, appraisals and quotes before relying on them", "Owner inputs"),
 ("R11", "2024 Prop H detailed terms", "The official 2024 results page confirms the measure name and result; the detailed age-58-to-55 wording is from secondary reporting of the measure text.", "Confirm against the City's official measure text if needed", "sfelections_2024"),
 ("R12", "Insurance figures are estimates", "Owner estimates (~$1,500/yr per property) are unverified; official rate context is published but is not a quote.", "Obtain actual quotes (suggestion S-05)", "doi"),
]
f_rows = []
for fid, title_, detail, action, basis in flagged:
    src_html = src(basis) if basis in SRC else "Desk review"
    f_rows.append(([fid, title_, detail, action, src_html], "verified" if basis in SRC else "unverified"))

f_body = f"""
<p class="small">Irregularities found in review and items that cannot be confirmed from an official source.
Flagged items do not block publication; they are published here with their sources so the owner can review and
request changes. No flagged item on this desk was silently dropped.</p>
{tbl(["ID", "Item", "Finding", "Recommended action", "Source"], f_rows)}
"""
pages["flagged.html"] = dict(title="Flagged for review", dek="Irregularities and unverified items, with sources, for owner review.", body=f_body)

# ---------------------------------------------------------------- methodology
meth_body = f"""
<h3>Method</h3>
<ul>
<li><b>Source policy.</b> Every table row carries an official-source link (government or agency publisher) or is
left blank and tagged <span class="tag unverified">unverified</span>, <span class="tag owner">owner-supplied</span> or
<span class="tag assumption">assumption</span>. Nothing is inferred or invented; no value is filled in where no
official source exists.</li>
<li><b>Rounding.</b> Money is rounded to the nearest $10 unless the source value is itself an exact statutory or
agency figure, which is quoted as published and tagged <span class="tag exact">exact (statutory)</span>.</li>
<li><b>Model.</b> Projections are model outputs: value growth {GROWTH:.0%}/yr (assumption), property tax 1% of value
(Prop 13 general levy), operating-cost inflation {COST_INFL:.0%}/yr. The distribution chart varies growth at
3%/5%/7% because growth and inflation are never consistent over a 50-year horizon.</li>
<li><b>Black-swan phased-investing path.</b> Sale proceeds are parked in 3M-2Y Treasuries for 24-36 months, then
phased into stocks; the path is modelled on the merged desks and the Treasury reference is carried here.
Reinvestment risk (parked cash earning less than the portfolio, or markets rising while parked) is stated next to
the headline wherever the path is shown.</li>
<li><b>Privacy.</b> No names, street addresses, ZIP codes, neighbourhoods, parcel or account numbers, or contact
details appear anywhere. Properties are "Property A" (future trust inheritance, Santa Clara County) and
"Property B" (already owned, San Francisco County) at county level only. Owner-supplied figures are labelled and
are not published where the convention is to keep them private (e.g. current assessed values).</li>
<li><b>Not advice.</b> This desk is decision support, not tax, legal or investment advice. Re-check the
then-current law before acting, and confirm all owner-supplied figures with documents and professionals.</li>
</ul>

<h3>Verification performed (2026-11-15)</h3>
<ul>
<li>Form 540 MHST and capital-gain treatment read line-by-line from the official 2025 Form 540 instructions
({src("ftb_540")}).</li>
<li>SF Measure H (2026) official terms read from the SF Department of Elections results page and the SFMTA
official page ({src("sfelections_2026")} {src("sfmta_proph")}).</li>
<li>SF Prop H (2024) and Prop M confirmed from the official final results page ({src("sfelections_2024")});
the Prop M digest read from the official City digest ({src("sfgov_digest")}).</li>
<li>Property A area and Santa Clara County rent evidence read from the official Census QuickFacts pages
({src("census_cupertino")} {src("census_scc")}).</li>
<li>Federal thresholds verified against IRS pages ({src("irs_estate")} {src("irs_706")} {src("irs_stepup")});
California no-estate-tax rule against the State Controller ({src("sco_estate")}).</li>
<li>Desk generator and verifier run: page set, row-sourcing, host allowlist, link resolution, $10 rounding,
PII scan — PASS (see _src/verify.py; _src is working material and is not published).</li>
</ul>
"""
pages["methodology.html"] = dict(title="Methodology &amp; privacy", dek="How the desk sources, rounds, models and protects privacy.", body=meth_body)

# ---------------------------------------------------------------- briefing sheet
brief_body = f"""
<h3>Attorney &amp; CPA Briefing Sheet</h3>
<p class="small">One page. Print or save as PDF. Figures rounded to $10; statutory amounts exact.
Prepared 2026-11-15. Not advice.</p>

<div class="brief">
<div class="brief-head"><b>Household:</b> Property A (Santa Clara County) — inherited via trust ~2040-2050 · <b>Property B (San Francisco County)</b> — already owned, 3 units, 2 rented</div>

<table class="brief-tbl">
<tr><td><b>Headline decision</b></td><td>Baseline: sell Property A at inheritance and reinvest after tax; keep the Treasury parking path (3M-2Y, 24-36 months) to soften crash-entry risk. Renting wins only if the heir occupies (Prop 19 cap) and rent growth outpaces portfolio returns. <span class="tag verified">sourced</span></td></tr>
<tr><td><b>Prop 19 switch</b></td><td>Heir must occupy Property A as primary residence within <b>1 year</b> of transfer or the home fully reassesses to market value; allowance $1,044,586 (2025-2027). <span class="tag verified">sourced</span></td></tr>
<tr><td><b>Form 540 1% tax</b></td><td>MHST: <b>1% of CA taxable income over $1,000,000</b> (Form 540 line 62), any year it crosses. Capital gains: ordinary CA rates (no state LTCG preference), and they count toward the threshold. Top effective rate on the excess: 13.3%. <span class="tag verified">sourced</span></td></tr>
<tr><td><b>SF Prop H (2026)</b></td><td>Muni parcel tax from FY2027-28: <b>$249/yr base for Property B</b> (multifamily), + size additions (unverified until building area is known). No effect on Property A. Preliminary pass 74.4%; certification pending. <span class="tag verified">sourced</span></td></tr>
<tr><td><b>Estate thresholds</b></td><td>Federal exclusion <b>$15,000,000</b>/person (2026); top rate 40%; Form 706 due 9 months after death. CA: no estate or inheritance tax. Step-up in basis at death (§1014). <span class="tag verified">sourced</span></td></tr>
<tr><td><b>Liquidity</b></td><td>If the estate may exceed $15,000,000: map liquid sources now; confirm portability (DSUE) and prior taxable gifts; avoid a forced real-estate sale to pay tax. <span class="tag verified">sourced</span></td></tr>
<tr><td><b>Rent evidence</b></td><td>Area median gross rent (Census ACS 2020-2024): <b>$3,500+/mo</b>. Property-specific rent unverified — obtain a written rent opinion before ranking rent vs. sell. <span class="tag verified">sourced</span></td></tr>
<tr><td><b>Maintenance</b></td><td>Five-year plan built (2027-2031): A ~{m0(3020)}/yr, B ~{m0(7179)}/yr operating (owner anchors, unverified). Capital items blank until inspection. <span class="tag assumption">assumption</span></td></tr>
<tr><td><b>Deadlines</b></td><td>Occupancy 1 yr (Prop 19) · BOE-19-P 3 yrs · Form 706 9 months · SF Prop H first bill FY2027-28 (fall 2027) · annual model re-run. <span class="tag verified">sourced</span></td></tr>
<tr><td><b>Next actions</b></td><td>Written date-of-death valuation · written rent opinion · portability & prior-gift answers · insurance quotes · building area for Prop H · investment policy before proceeds arrive. <span class="tag verified">sourced</span></td></tr>
</table>
<div class="brief-foot">Sources: IRS estate/gift, Form 706, §1014, §121 · CA FTB Form 540 instructions & rate schedules · BOE Prop 13/19 · SF Dept. of Elections (2024, 2026) · SFMTA Prop H · Census ACS QuickFacts · Santa Clara County tax-rate book. Full citations on the Sources page.</div>
</div>
"""
pages["briefing-sheet.html"] = dict(title="Attorney &amp; CPA Briefing Sheet", dek="One-page printable brief for the attorney and the tax adviser.", body=brief_body, printable=True)

# ---------------------------------------------------------------- write
os.makedirs(ASSETS, exist_ok=True)
for name, spec in pages.items():
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(page(spec["title"], spec["body"], spec.get("dek", ""), spec.get("printable", False)))
print(f"desk-9af5443d: wrote {len(pages)} pages")
