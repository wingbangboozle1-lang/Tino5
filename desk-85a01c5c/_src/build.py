#!/usr/bin/env python3
"""desk-85a01c5c generator: inheritance decision desk.

Builds the pages under desk-85a01c5c/. Rules enforced here and by verify.py:
  * every table body row carries an official source link, an explicit
    unverified/owner/assumption marker, or an exact (statutory) tag;
  * money rounded to the nearest $10 (m0) unless statutory, tagged exact;
  * privacy: Property A / Property B at county level only; no names, street
    addresses, ZIP codes, city names, parcel or account numbers.
Run: python3 desk-85a01c5c/_src/build.py
"""
import os

import model as M

OUT = os.path.join(os.path.dirname(__file__), "..")

# ----------------------------------------------------------------- sources
SRC = {
    "irs_wftc": ("IRS - Working Families Tax Cuts (2026: basic exclusion amount $15,000,000, up from $13,990,000 for 2025 decedents; standard deductions)",
                 "https://www.irs.gov/newsroom/working-families-tax-cuts-individuals-and-workers"),
    "irs_rp2532": ("IRS - Rev. Proc. 2025-32 (sec. 2.14: OBBBA sec. 70106 raises the basic exclusion amount to $15,000,000 for 2026 and indexes it after 2026; GST exemption $15,000,000; annual gift exclusion adjusted under sec. 2503(b))",
                   "https://www.irs.gov/pub/irs-drop/rp-25-32.pdf"),
    "irs_706": ("IRS - About Form 706, United States Estate Tax Return (filing requirements and deadlines)",
                "https://www.irs.gov/forms-pubs/about-form-706"),
    "irs_403": ("IRS - Topic No. 403, Basis of Assets (inherited property: fair market value at date of death, IRC sec. 1014)",
                "https://www.irs.gov/taxtopics/tc403"),
    "irs_703": ("IRS - Topic No. 703, Sale of Home (sec. 121 exclusion $250,000 / $500,000 married filing jointly; ownership and use 2 of the last 5 years)",
                "https://www.irs.gov/taxtopics/tc703"),
    "boe_nr": ("CA Board of Equalization - News Release NR-25-02 (7 Mar 2025): Prop 19 intergenerational exclusion adjusted to $1,044,586 for transfers 2/16/2025-2/15/2027; transferee must file for the homeowners' or disabled veterans' exemption within one year",
               "https://www.boe.ca.gov/news/2025/nr-25-02.htm"),
    "boe_prop19": ("CA Board of Equalization - Proposition 19 page (filing requirements checklist: $1,044,586 for transfers 2/16/2025-2/15/2027; principal-residence requirement)",
                   "https://www.boe.ca.gov/prop19/"),
    "boe_pub801": ("CA Board of Equalization - Publication 801, Proposition 19 fact sheet (form BOE-19-P; value limit = factored base year value + $1,044,586; excess added to taxable value; filing period)",
                   "https://www.boe.ca.gov/pdf/pub801.pdf"),
    "boe_prop13": ("CA Board of Equalization - Proposition 13 (1% maximum levy; assessed value increase capped at 2%/yr absent change in ownership or new construction; Cal. Const. art. XIII-A)",
                   "https://www.boe.ca.gov/proptaxes/proposition13.htm"),
    "scc_trb": ("County of Santa Clara - Compilation of Tax Rates & Information, FY2025-2026 (1% maximum levy 1.00000; county retirement levy 0.03880; county library 0.00240; County Housing Bond 2016 0.00560; VMC 2008 0.00520; SCVWD State Water Project 0.00390 L&I; 816 tax rate areas; rate area code printed on the property tax bill)",
                "https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf"),
    "scc_trb_page": ("County of Santa Clara Controller - Property Tax Rate Book page",
                     "https://controller.santaclaracounty.gov/property-tax-distribution/property-tax-rate-book"),
    "scc_rec": ("County of Santa Clara Clerk-Recorder - Recording document fees (documentary transfer tax $0.55 per $500; city conveyance tax $1.65 per $500 applies only in three named cities; SB 2 fee $75/title; AB 1466 fee $2/title; PCOR fee $20 when missing)",
                "https://clerkrecorder.santaclaracounty.gov/recording-documents/recording-document-fees"),
    "sf_asr": ("SF Assessor-Recorder - Things to Know During Property Transfer factsheet (transfer tax tiers; tier $1,000,000 to under $5,000,000 = $3.75 per $500 of full value, worked example)",
               "https://media.api.sf.gov/documents/ASR_Factsheet_PropertyTransfer_English_2025.pdf"),
    "sf_digest": ("SF - November 2026 ballot digest, Changes to Real Property Transfer Tax (states the current two highest rates: 5.5% for $10M-under $25M and 6% at $25M or more; a 2026 measure dedicates half of the revenue from $10M+ transactions)",
                  "https://media.api.sf.gov/documents/Approved_Digest_-_Changes_to_Real_Property_Transfer_Tax.pdf"),
    "sf_heirs": ("SF Treasurer & Tax Collector - Information for heirs",
                 "https://sftreasurer.org/property/information-heirs"),
    "sfmta_parcel": ("SFMTA - Proposition H: Stronger Muni For All Parcel Tax (approved 3 Nov 2026; first tax on the FY2027-28 property tax bill mailed fall 2027; exemption/adjustment portals open 1 Dec 2026; applications due 1 Jun 2027)",
                     "https://www.sfmta.com/getting-around/muni/parcel"),
    "sfmta_faq": ("SFMTA - Proposition H FAQ (official rate table: multifamily residential up to 5,000 sq ft $249, +$0.195 per sq ft over 5,000, max $50,000; single-family $129/$0.42/$1.99; non-residential $799+; amounts rise with inflation from FY2028-29; tax expires 30 Jun 2042; rent-controlled pass-through up to 50% of the tax, max $65/yr; senior principal-residence exemptions)",
                  "https://www.sfmta.com/getting-around/muni/parcel/frequently-asked-questions"),
    "fedhist_1929": ("Federal Reserve History - Stock Market Crash of 1929 (DJIA peak 381.17 on 3 Sep 1929; close 41.22 on 8 Jul 1932, 89% below the peak; Black Monday -13%, Black Tuesday -12%; pre-crash level regained 23 Nov 1954)",
                     "https://www.federalreservehistory.org/essays/stock-market-crash-of-1929"),
    "fedhist_gr": ("Federal Reserve History - The Great Recession (S&P 500 fell 57% from its October 2007 peak to its trough in March 2009; home prices fell about 30% from mid-2006 to mid-2009; real GDP -4.3%; unemployment 5% to 10%)",
                   "https://www.federalreservehistory.org/essays/great-recession-of-200709"),
    "treasury": ("U.S. Department of the Treasury - Daily Treasury Par Yield Curve Rates (13 Nov 2026: 3-month 4.32%, 2-year 4.88%)",
                 "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve"),
    "fred_tb3ms": ("FRED (Federal Reserve Bank of St. Louis) - TB3MS, 3-month Treasury bill secondary-market discount rate, monthly/annual (series used here via annual averages; values transcribed in this repository with documented provenance)",
                   "https://fred.stlouisfed.org/series/TB3MS"),
    "erp_b55": ("Economic Report of the President 2026 - Table B-55 (S&P composite common stock price index, end of year) and Table B-56 (dividend-price ratio)",
                "https://www.govinfo.gov/content/pkg/ERP-2026/pdf/ERP-2026-table55.pdf"),
    "erp_b56": ("Economic Report of the President 2026 - Table B-56 (S&P composite dividend-price ratio)",
                "https://www.govinfo.gov/content/pkg/ERP-2026/pdf/ERP-2026-table56.pdf"),
    "ftb": ("California Franchise Tax Board (California has no state estate tax and no inheritance tax)",
            "https://www.ftb.ca.gov/"),
    "ftb_540": ("California FTB - 2026 Form 540 tax rate schedules (individual brackets; 1% tax on income over $1,000,000)",
                "https://www.ftb.ca.gov/forms/2026/2026-540-tax-rate-schedules.pdf"),
    "cdi": ("California Department of Insurance - homeowners and dwelling-fire insurance information (rate research pointer; no premium figure is asserted from it on this desk)",
            "https://www.insurance.ca.gov/"),
    "cfpnet": ("California FAIR Plan Association - insurer of last resort (dwelling fire policy; check current dwelling limits and required DIC wrap)",
               "https://www.cfpnet.com/"),
    "sfpuc": ("SFPUC - water and sewer rate schedules (reference schedule; the parcel's retail water provider is not confirmed on this desk)",
              "https://www.sfpuc.gov/accounts-services/water-power-sewer-rates"),
    "sjwc": ("SJWC tariff PDF - approved schedule on file in the repository's source registers (reference only; the parcel's provider is unconfirmed)",
             "https://www.sjwater.com/media/kccm45hy/san-jose-water-company-al-599-approved_0.pdf"),
    "cpuc": ("CPUC - utility rate information (electricity research pointer; no parcel-specific figure asserted)",
             "https://www.cpuc.ca.gov/"),
    "sf_assessor19": ("SF Assessor-Recorder - Proposition 19 information (parent-child exclusions in SF County)",
                      "https://www.sf.gov/proposition-19"),
    "leginfo": ("California Legislative Information (official statutes, incl. Revenue & Taxation Code)",
                "https://leginfo.legislature.ca.gov/faces/codes.xhtml"),
}


def src(*keys):
    return " ".join(
        f'<a href="{SRC[k][1]}" target="_blank" rel="noopener">{SRC[k][0]}</a>'
        for k in keys)


def tag(kind):
    cls = {"verified": "verified", "exact": "exact", "assumption": "assumption",
           "owner": "owner", "unverified": "unverified"}[kind]
    lab = {"verified": "verified", "exact": "exact (statutory)",
           "assumption": "assumption", "owner": "owner-supplied - unverified",
           "unverified": "unverified - blank"}[kind]
    return f'<span class="tag {cls}">{lab}</span>'


def m0(x):
    return M.m0(x)


def ex(x):
    """Exact statutory/agency figure as published (decimals preserved)."""
    if isinstance(x, float) and not x.is_integer():
        s = f"{x:.3f}".rstrip("0").rstrip(".")
        return f"${s}"
    return f"${int(x):,}"


def pc(x, nd=2):
    return f"{x:.{nd}f}%"


# ----------------------------------------------------------------- shell
NAV_GROUPS = [
    ("Start", [("Landing: what would change the answer", "index.html"),
               ("Executive summary", "executive-summary.html")]),
    ("Properties", [("Property facts", "properties.html"),
                    ("Property tax & assessment", "property-tax.html"),
                    ("Running costs", "running-costs.html")]),
    ("Taxes", [("Inheritance & estate tax", "inheritance-tax.html"),
               ("Law watch: enacted vs proposed", "law-watch.html")]),
    ("Decision", [("Scenarios (live / rent / sell / mixed)", "scenarios.html"),
                  ("Black swan & phased investing", "black-swan.html"),
                  ("What-if controls", "what-if.html"),
                  ("Projections 2026-2050", "projections.html")]),
    ("Timing", [("Trust process & deadlines timeline", "process.html")]),
    ("For advisers", [("Attorney & CPA briefing sheet", "briefing-sheet.html")]),
    ("Owner input", [("Suggestions board (proposed)", "suggestions.html"),
                     ("Questions & information gaps", "questions.html"),
                     ("Glossary", "glossary.html")]),
    ("Record", [("Sources", "sources.html"),
                ("Flagged for review", "flagged.html"),
                ("Methodology & privacy", "methodology.html")]),
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
    js = '<script src="assets/app.js"></script>' if not printable else ""
    pr = ' class="print-page"' if printable else ""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><meta name="referrer" content="no-referrer">
<title>{title} - Inheritance decision desk</title>{css}{js}</head><body{pr}>
<header class="site"><h1>Inheritance decision desk (desk-85a01c5c)</h1>
<div class="sub">Property A (future trust inheritance, Santa Clara County) &middot; Property B (already owned, San Francisco County) &middot; county level only &middot; money rounded to $10 unless marked exact &middot; no personal identifiers</div></header>
<nav>{nav_html()}</nav>
<main><h2>{title}</h2>{f'<p class="dek">{dek}</p>' if dek else ''}{body}
<div class="foot no-print"><b>Not tax, legal or investment advice.</b> Planning figures only; statutory amounts are quoted exactly as published and all other money is rounded to the nearest $10. Every table row links its official source, states an assumption, or is blank and marked unverified. Re-check the then-current law before acting.
<a href="sources.html">Sources</a> &middot; <a href="flagged.html">Flagged for review</a> &middot; <a href="methodology.html">Methodology &amp; privacy</a></div></main></body></html>"""


def tbl(headers, rows, caption=None):
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join(f"<tr>{''.join(r)}</tr>" for r in rows)
    cap = f"<caption>{caption}</caption>" if caption else ""
    return (f'<div class="scroll"><table class="data">{cap}<thead><tr>{head}'
            f'</tr></thead><tbody>{body}</tbody></table></div>')


def num(x):
    return f'<td class="num">{x}</td>'


# ==================================================================== pages
def p_index():
    yr = 2040
    s = M.scenario_paths(yr)
    rbe, det = M.required_rent_break_even(yr)
    yield_pct, _ = M.live_vs_rent_break_even_yield(yr)
    lump_v, ph_v, cost, _ = M.reinvestment_cost_no_crash(park_months=36,
                                                         phase_months=24)
    what_changes = [
        (f"The gross rent Property A can command. The model does not assert one: it solves the break-even. For a {M.m0(det['mv_t'])} house at the 2040 transfer, renting beats selling only above about <b>{m0(rbe)}/month</b> gross (about {pc(det['mv_t'] and rbe*12/det['mv_t']*100, 1)} gross yield). A written comparable-rent estimate would replace this with evidence.",
         tag("assumption"), src("fedhist_gr") if False else '<a href="questions.html">discovery action Q2</a>'),
        (f"How long the heir will occupy Property A as a principal residence. The Prop 19 exclusion is conditional: occupancy within one year and the homeowners' exemption filing within one year. If the house is let instead, it is fully reassessed to market value.",
         tag("exact"), src("boe_nr", "boe_pub801")),
        (f"Property growth minus equity return. Base case: property 4.5%/yr, equities 7.0%/yr (assumption, below the official ERP record). If the gap widens toward the official record's {pc(M.erp_long_run_stats()['mean_total_return_pct'],1)} mean total return, selling strengthens; if house growth runs hot, keeping strengthens.",
         tag("assumption"), src("erp_b55", "erp_b56")),
        (f"The size of the whole estate. The federal basic exclusion is {ex(M.STATUTORY['estate_exclusion_2026'])} per person for 2026 (indexed after 2026, per OBBBA). Amounts above it face the 40% estate tax unless sheltered (marital deduction, portability, charitable). This is an information gap: the estate's composition is not on this desk.",
         tag("exact"), src("irs_wftc", "irs_rp2532")),
        (f"Crash timing on any sale-and-reinvest. A lump sum at a 1929-style peak needs the official 25 years to regain the pre-crash price level; the phased path quantified on the black-swan page materially changes that outcome. This risk is the reason the phased path is a separate decision item.",
         tag("verified"), src("fedhist_1929")),
        (f"Operating costs that are still owner-supplied only: water ({m0(100)}-{m0(150)}/mo), solar credit, insurance (~{m0(M.OWNER['A_insurance'])}/yr), maintenance. Each carries a discovery action; none is verified.",
         tag("owner"), src("cdi", "cfpnet")),
        (f"Property B's carrying costs from FY2027-28 include the Prop H parcel tax ({ex(M.STATUTORY['proph_multifamily_base'])}/yr base, indexed from FY2028-29) - a new enacted cost. Whether the parcel exceeds 5,000 sq ft changes it materially ({m0(M.proph_year(2028, sqft=8000))}/yr at 8,000 sq ft).",
         tag("exact"), src("sfmta_faq")),
        (f"Law changes before the 2040-2050 transfer: enacted and proposed items are separated on the law-watch page. The Prop 19 allowance itself resets every two years (next window starts 16 Feb 2027).",
         tag("verified"), src("boe_nr", "sf_digest")),
    ]
    rows = [f"<td>{i+1}</td><td>{txt}</td><td>{t}</td><td>{s_}</td>"
            for i, (txt, t, s_) in enumerate(what_changes)]
    body = f"""
<div class="callout info"><b>Read this first - what would change the answer.</b> The recommendation on this desk is not a single projection; it rests on the eight items below. Each is labelled verified, exact (statutory), assumption, or owner-supplied - unverified, and each carries its official source or a discovery action. Change any of them and the ranking of live / rent / sell can move; the break-evens on <a href="scenarios.html">Scenarios</a> show by how much.</div>
{tbl(["#", "Swing factor", "Status", "Source / action"], rows, "What would change the answer (decision-reversal items)")}

<h3>The headline, with reinvestment risk beside it</h3>
<div class="callout warn"><b>Headline (base case, model output):</b> at the 2040 transfer the choice between keeping and selling Property A rests on the rent it can earn versus the {pc(M.ASSUMPTIONS['base_equity_return'],1)} reinvestment return (assumption) - the model's break-even gross rent is about {m0(rbe)}/month. <b>Reinvestment risk beside the headline:</b> if the heir sells and phases in over 36 months on a flat market, the cushion costs about {m0(cost)} per {m0(10000)} over ten years versus investing at once (at the {pc(M.ASSUMPTIONS['base_equity_return'],1)} assumption); if a 2008-style crash arrives instead, the same phasing leaves about {m0(M.replay_strategy(M.CRASH_2008, 36, 24, 10000, 77))} per {m0(10000)} versus {m0(M.lump_sum_at_peak(M.CRASH_2008, 10000, 77))} invested at the peak (price basis, official drawdown). Details: <a href="black-swan.html">Black swan &amp; phased investing</a>.</div>
<p class="small">No single number decides this. The desk separates what is verified from what is assumed, prices the transfer taxes and the new parcel tax into the sell path, and shows every break-even. See <a href="methodology.html">Methodology</a> for the rules, <a href="flagged.html">Flagged for review</a> for open items.</p>

<h3>Verified anchors (official sources)</h3>
{tbl(["Item", "Figure", "Status", "Source"], [
    num("Federal estate &amp; gift basic exclusion, 2026") + num(ex(M.STATUTORY["estate_exclusion_2026"]) + " per person") + f"<td>{tag('exact')}</td>" + f"<td>{src('irs_wftc','irs_rp2532')}</td>",
    num("Estate/gift tax rate above the exclusion") + num(pc(M.STATUTORY["estate_top_rate_pct"], 0)) + f"<td>{tag('exact')}</td>" + f"<td>{src('irs_rp2532')}</td>",
    num("California estate or inheritance tax") + num("$0") + f"<td>{tag('verified')}</td>" + f"<td>{src('ftb')}</td>",
    num("Prop 19 intergenerational allowance (transfers 2/16/2025-2/15/2027)") + num(ex(M.STATUTORY["prop19_allowance"])) + f"<td>{tag('exact')}</td>" + f"<td>{src('boe_nr','boe_prop19')}</td>",
    num("SCC ad-valorem components (1% levy + county items)") + num(pc(M.STATUTORY["levy_1pct"] + M.STATUTORY["scc_retirement_levy"] + M.STATUTORY["scc_library_levy"] + M.STATUTORY["scc_housing_bond_2016"] + M.STATUTORY["scc_vmc_2008"], 5)) + f"<td>{tag('exact')}</td>" + f"<td>{src('scc_trb')}</td>",
    num("Treasury par yields, 13 Nov 2026 (parking leg)") + num("3-month " + pc(M.CURRENT_3M, 2) + "; 2-year " + pc(M.CURRENT_2Y, 2)) + f"<td>{tag('verified')}</td>" + f"<td>{src('treasury')}</td>",
    num("Prop H parcel tax, Property B, FY2027-28 (multifamily, up to 5,000 sq ft)") + num(ex(M.STATUTORY["proph_multifamily_base"]) + "/yr") + f"<td>{tag('exact')}</td>" + f"<td>{src('sfmta_faq')}</td>",
], "Verified anchors")}

<h3>Desk map (grouped menu)</h3>
<div class="grid">
<a class="card" href="executive-summary.html"><b>Executive summary</b><span>The decision framework, break-evens, estate headroom and the decision log to fill in.</span></a>
<a class="card" href="properties.html"><b>Property facts</b><span>Property A (to be inherited) and Property B (already owned, 2 of 3 units let), county level only.</span></a>
<a class="card" href="property-tax.html"><b>Property tax &amp; assessment</b><span>Prop 13/19 mechanics, the published rate components, tax-rate-area lookup, projections to 2050.</span></a>
<a class="card" href="running-costs.html"><b>Running costs</b><span>Water, solar credit, insurance, maintenance; Property B income and the Prop H parcel tax.</span></a>
<a class="card" href="inheritance-tax.html"><b>Inheritance &amp; estate tax</b><span>Federal exclusion and 40% rate, step-up in basis, sec. 121, sell-path transfer taxes and fees.</span></a>
<a class="card" href="scenarios.html"><b>Scenarios</b><span>Live / rent / sell and mixed paths at identical transfer dates and horizons, with break-evens.</span></a>
<a class="card" href="black-swan.html"><b>Black swan &amp; phased investing</b><span>Uneven regimes; the phased path (3M-2Y Treasuries 24-36 months) replayed against the official 1929 and 2008 drawdowns.</span></a>
<a class="card" href="what-if.html"><b>What-if controls</b><span>Sensitivity grid and a small calculator; change transfer year, growth and return.</span></a>
<a class="card" href="projections.html"><b>Projections 2026-2050</b><span>Year-by-year assessed values, taxes, market values, income and the parcel-tax line.</span></a>
<a class="card" href="process.html"><b>Trust process &amp; deadlines</b><span>Step-by-step inheritance with a deadline timeline (Form 706, BOE-19-P, occupancy, Prop H applications).</span></a>
<a class="card" href="briefing-sheet.html"><b>Attorney &amp; CPA briefing sheet</b><span>One printable page for the first adviser meeting.</span></a>
<a class="card" href="suggestions.html"><b>Suggestions board</b><span>Proposed actions awaiting an owner accept / modify / reject decision; nothing is implemented.</span></a>
<a class="card" href="questions.html"><b>Questions &amp; information gaps</b><span>What is known, what is missing, and the discovery action for each gap.</span></a>
<a class="card" href="law-watch.html"><b>Law watch</b><span>Enacted changes separated from proposals, with official links.</span></a>
<a class="card" href="glossary.html"><b>Glossary</b><span>Plain-language definitions used across the desk.</span></a>
<a class="card" href="sources.html"><b>Sources</b><span>The register: every official document used, with its URL and status.</span></a>
</div>

<div class="callout"><b>Privacy:</b> no names, street addresses, ZIP codes, city names, parcel or account numbers appear on this desk. The two properties are described at county level only, owner figures are labelled as such, and the exact per-year assessment and tax history is withheld because assessed values are public records that can be matched to a parcel. The model works from banded anchors.</div>
"""
    return page("Landing: what would change the answer", body,
                "Start here. The eight items that would flip the recommendation, the headline with reinvestment risk beside it, and the verified anchors.")


def p_executive_summary():
    rows = []
    for ty in M.ASSUMPTIONS["transfer_years"]:
        s = M.scenario_paths(ty)
        rbe, det = M.required_rent_break_even(ty)
        y, _ = M.live_vs_rent_break_even_yield(ty)
        rows.append(
            num(str(ty))
            + num(m0(s["mv_at_transfer"]))
            + num(m0(s["fbv_at_transfer"]))
            + num(m0(s["assessed_after_prop19"]))
            + num(m0(s["live_tax"]) + "/yr")
            + num(m0(s["proceeds"]))
            + num(m0(s["transfer_tax"]))
            + num(m0(rbe) + "/mo")
            + num(pc(y * 100, 2))
            + f"<td>{tag('assumption')} {src('erp_b55','boe_nr')}</td>")
    headroom_rows = []
    for estate in (12_000_000, 15_000_000, 20_000_000, 30_000_000):
        head, taxable, tax = M.estate_headroom(estate)
        headroom_rows.append(
            num(ex(estate) + " (illustrative)")
            + num(m0(head) if head >= 0 else "-" + m0(-head).replace("$", "$"))
            + num(m0(taxable))
            + num(m0(tax))
            + f"<td>{tag('exact')} - rate &amp; exclusion; estate sizes are illustrative {src('irs_rp2532','irs_706')}</td>")
    body = f"""
<h3>The decision, stated as break-evens</h3>
<p>The desk compares <b>live in Property A</b>, <b>rent it</b>, and <b>sell and reinvest</b> - plus mixed paths (live-then-sell, rent-then-sell, sell-then-phase) - at the <b>same transfer dates</b> (2040, 2045, 2050) and the <b>same horizon end (2076)</b>, with the transfer taxes, recording fees, occupancy effects and liquidity differences priced in. Because the market rent of Property A is unknown (flagged), the rent path is expressed as the <b>break-even rent</b> at which renting matches selling, rather than as a forecast.</p>
{tbl(["Transfer year", "Market value at transfer", "Factored base year value", "Assessed after Prop 19 (heir occupies)", "Property tax, year 1 (1.12% band midpoint)", "Sell proceeds after costs", "of which transfer tax", "Break-even gross rent (rent beats sell above this)", "Avoided-rent yield (live beats rent above this)", "Status / sources"], rows, "Decision table, base case (model outputs from banded owner anchors; property growth 4.5%/yr, equities 7.0%/yr, both assumptions)")}
<p class="small">Avoided-rent yield = the value of occupying (the rent the owner does not have to pay) as a share of the house value. Live beats rent when the owner values occupancy above that yield; rent beats sell when achievable gross rent exceeds the break-even column.</p>

<h3>Estate-tax headroom (federal)</h3>
{tbl(["Illustrative gross estate", "Headroom against the 2026 exclusion", "Taxable excess", "Tax at 40%", "Status / sources"], headroom_rows, "Federal estate-tax headroom; the estate's actual composition is an information gap (see Questions)")}
<p class="small">The 2026 basic exclusion amount is {ex(M.STATUTORY['estate_exclusion_2026'])} per person and is indexed after 2026 (OBBBA sec. 70106). A surviving spouse may inherit unused exclusion through a timely estate-tax return (portability). California imposes no estate or inheritance tax. The cash portion of this estate is the deciding unknown: it is not on this desk and is requested on <a href="questions.html">Questions</a>.</p>

<h3>What this summary does not do</h3>
<ul>
<li>It does not assert a market rent, a confirmed insurance premium, a confirmed water provider, or a square footage for Property B - each is a blank row or an owner-supplied band on the relevant page.</li>
<li>It does not model the income-tax return of the whole estate; the 1% California tax above {ex(1_000_000)} of income is noted on <a href="inheritance-tax.html">Inheritance &amp; estate tax</a> and is a CPA question.</li>
<li>It does not claim the phased-investing path is superior: the black-swan page shows it winning in both official crash replays and losing about {m0(M.reinvestment_cost_no_crash(park_months=36, phase_months=24)[2])} per {m0(10000)} over ten years on a flat market at the base-case return. That trade-off is the owner's call.</li>
</ul>

<h3>Decision log (fill in at review)</h3>
{tbl(["Item", "Decision", "Date", "Reason", "Status"], [
    num("Path for Property A (live / rent / sell / mixed)") + "<td></td><td></td><td></td>" + f"<td>{tag('owner')}</td>",
    num("Phased-investing policy if sold (park months, phase months)") + "<td></td><td></td><td></td>" + f"<td>{tag('owner')}</td>",
    num("Prop 19 exclusion claim (only if long-term occupancy)") + "<td></td><td></td><td></td>" + f"<td>{tag('owner')}</td>",
    num("Investment policy statement for sale proceeds") + "<td></td><td></td><td></td>" + f"<td>{tag('owner')}</td>",
    num("Portability / prior-gift review with CPA") + "<td></td><td></td><td></td>" + f"<td>{tag('owner')}</td>",
], "Decision log - write the decision and the date next to the item so a future reader knows what was chosen and why")}
"""
    return page("Executive summary", body,
                "Break-evens instead of a single forecast; estate headroom; the decision log.")


def p_properties():
    A = M.OWNER
    rows_a = [
        num("Status") + f"<td>To be inherited through the family trust, expected 2040-2050; owner-supplied</td><td>{tag('owner')} {src('sf_heirs')}</td>",
        num("County") + "<td>Santa Clara County (California)</td>" + f"<td>{tag('verified')} {src('boe_prop13')}</td>",
        num("Market value, Nov 2026") + num(m0(A["A_value_2026"])) + f"<td>{tag('owner')}</td><td></td>",
        num("Assessed value, 2026 (banded anchor)") + num("about " + m0(A["A_assessed_2026"])) + f"<td>{tag('owner')} - exact figure withheld (public record)</td><td>{src('boe_prop13')}</td>",
        num("Property tax, 2026 (banded, owner-implied)") + num("about " + m0(7100) + "/yr") + f"<td>{tag('owner')}</td><td></td>",
        num("Water") + num(m0(A["A_water_lo"]) + "-" + m0(A["A_water_hi"]) + "/mo") + f"<td>{tag('owner')} - provider unconfirmed for the parcel</td><td>{src('sjwc','sfpuc')}</td>",
        num("Electricity / solar") + num("net credit " + m0(A["A_solar_lo"]) + "-" + m0(A["A_solar_hi"]) + "/mo") + f"<td>{tag('owner')}</td><td>{src('cpuc')}</td>",
        num("Insurance") + num("about " + m0(A["A_insurance"]) + "/yr") + f"<td>{tag('owner')} - no verified market figure</td><td>{src('cdi','cfpnet')}</td>",
        num("Maintenance") + num("model stand-in " + m0(2000) + "/yr") + f"<td>{tag('assumption')} - disclosed input, not a verified cost</td><td></td>",
        num("Occupancy note") + "<td>Prop 19 parent-child exclusion requires the heir to occupy as principal residence and file the homeowners' exemption within one year</td>" + f"<td>{tag('exact')} {src('boe_nr','boe_pub801')}</td>",
    ]
    rows_b = [
        num("Status") + "<td>Already owned; 3 livable units, 2 rented; owner may occupy without losing the rental income</td>" + f"<td>{tag('owner')} {src('sf_heirs')}</td>",
        num("County") + "<td>San Francisco County (California)</td>" + f"<td>{tag('verified')} {src('sf_assessor19')}</td>",
        num("Market value, Nov 2026") + num(m0(A["B_value_2026"])) + f"<td>{tag('owner')}</td><td></td>",
        num("Assessed value, 2026 (banded anchor)") + num("about " + m0(A["B_assessed_2026"])) + f"<td>{tag('owner')} - exact figure withheld (public record)</td><td>{src('boe_prop13')}</td>",
        num("Gross rent, 2 rented units") + num(m0(A["B_rent"]) + "/mo") + f"<td>{tag('owner')}</td><td></td>",
        num("Water (3 units)") + num(m0(A["B_water_lo"]) + "-" + m0(A["B_water_hi"]) + "/mo") + f"<td>{tag('owner')}</td><td>{src('sfpuc')}</td>",
        num("Electricity") + num(m0(A["B_elec_lo"]) + "-" + m0(A["B_elec_hi"]) + "/mo") + f"<td>{tag('owner')}</td><td>{src('cpuc')}</td>",
        num("Insurance") + num("about " + m0(A["B_insurance"]) + "/yr") + f"<td>{tag('owner')} - rental dwelling-fire policy unverified</td><td>{src('cdi')}</td>",
        num("Prop H parcel tax, FY2027-28") + num(ex(M.STATUTORY["proph_multifamily_base"]) + "/yr base") + f"<td>{tag('exact')} - multifamily, up to 5,000 sq ft; square footage unknown</td><td>{src('sfmta_faq')}</td>",
    ]
    body = f"""
<p>Two properties, two different tax positions. Property A is inherited (step-up in basis; Prop 19 exclusion available only if occupied). Property B is already owned with long-held Prop 13 protection (very low assessed value) and rental income; it is <b>not</b> inherited, so nothing about its ownership changes at the transfer. The desks in this repository that treat both as one portfolio are flagged; here they are analysed separately and only combined for estate-size questions.</p>
<h3>Property A - the future inheritance (Santa Clara County)</h3>
{tbl(["Item", "Value", "Status", "Source"], rows_a, "Property A facts (owner-supplied values are anchors, not verified figures)")}
<h3>Property B - already owned (San Francisco County)</h3>
{tbl(["Item", "Value", "Status", "Source"], rows_b, "Property B facts")}
<div class="callout warn"><b>Privacy note:</b> the exact per-year assessed values and tax bills are withheld even though they were supplied, because assessed values are public records that can be matched to a parcel through county open-data roll files. They are used here as banded anchors. The exact figures live in the owner's private records, not on this site.</div>
"""
    return page("Property facts", body)


def p_property_tax():
    comp = M.STATUTORY
    comp_sum = (comp["levy_1pct"] + comp["scc_retirement_levy"] + comp["scc_library_levy"]
                + comp["scc_housing_bond_2016"] + comp["scc_vmc_2008"])
    rate_rows = [
        num("1% maximum levy (constitutional)") + num(pc(comp["levy_1pct"], 5)) + f"<td>{tag('exact')} {src('boe_prop13','scc_trb')}</td>",
        num("County retirement levy") + num(pc(comp["scc_retirement_levy"], 5)) + f"<td>{tag('exact')} {src('scc_trb')}</td>",
        num("County library retirement levy") + num(pc(comp["scc_library_levy"], 5)) + f"<td>{tag('exact')} {src('scc_trb')}</td>",
        num("County Housing Bond 2016") + num(pc(comp["scc_housing_bond_2016"], 5)) + f"<td>{tag('exact')} {src('scc_trb')}</td>",
        num("VMC 2008") + num(pc(comp["scc_vmc_2008"], 5)) + f"<td>{tag('exact')} {src('scc_trb')}</td>",
        num("SCVWD State Water Project (land &amp; improvements)") + num(pc(comp["scc_scvwd_state_water"], 5)) + f"<td>{tag('exact')} {src('scc_trb')}</td>",
        num("Countywide subtotal used as the band floor") + num(pc(comp_sum, 5)) + f"<td>{tag('exact')} {src('scc_trb')}</td>",
        num("School-district and community-college bonds (the parcel's elementary and high-school districts, Foothill-De Anza CCD)") + "<td>present in the tax-rate-area tables; exact TRA total depends on the parcel's rate area</td>" + f"<td>{tag('unverified')} {src('scc_trb_page')}</td>",
        num("Parcel's total ad-valorem rate") + "<td>blank - read the tax rate area code and the itemised rate off the property tax bill; the county publishes 816 tax rate areas</td>" + f"<td>{tag('unverified')} {src('scc_trb','scc_trb_page')}</td>",
    ]
    proj_rows = []
    for y in range(2026, 2051, 3):
        ass = M.property_a_assessed(y)
        mv = M.property_a_at(y)
        proj_rows.append(
            num(str(y))
            + num(m0(ass))
            + num(m0(ass * M.ASSUMPTIONS["rate_lo"]) + " - " + m0(ass * M.ASSUMPTIONS["rate_hi"]))
            + num(m0(mv))
            + num(m0(M.property_a_assessed(y) and mv * 0.0 + ass and ass))  # placeholder replaced below
            + f"<td>{tag('assumption')} {src('boe_prop13')}</td>")
    # rebuild projection rows properly (tax at band midpoint)
    proj_rows = []
    for y in range(2026, 2051, 3):
        ass = M.property_a_assessed(y)
        mv = M.property_a_at(y)
        proj_rows.append(
            num(str(y))
            + num(m0(ass))
            + num(m0(ass * M.ASSUMPTIONS["rate_base"]))
            + num(m0(mv))
            + num(m0(ass) and "")
            + f"<td>{tag('assumption')} {src('boe_prop13')}</td>")
    proj_rows = []
    for y in range(2026, 2051, 3):
        ass = M.property_a_assessed(y)
        mv = M.property_a_at(y)
        proj_rows.append(
            num(str(y))
            + num(m0(ass))
            + num(m0(ass * M.ASSUMPTIONS["rate_base"]))
            + num(m0(mv))
            + f"<td>{tag('assumption')} {src('boe_prop13')}</td>")
    body = f"""
<h3>Rules that set the property tax</h3>
{tbl(["Rule", "Terms", "Status", "Source"], [
    num("Prop 13 base") + "<td>1% maximum levy on assessed value; assessed value rises at most 2%/yr absent change in ownership or new construction</td>" + f"<td>{tag('exact')} {src('boe_prop13','scc_trb')}</td>",
    num("Prop 19, family home") + f"<td>parent-child transfer: assessed value protected up to factored base year value + {ex(comp['prop19_allowance'])} (2/16/2025-2/15/2027 window); the excess is added to the taxable value; only for the heir's principal residence, occupancy within one year, homeowners' exemption filed within one year; form BOE-19-P within three years</td>" + f"<td>{tag('exact')} {src('boe_nr','boe_pub801','boe_prop19')}</td>",
    num("Prop 19, other real estate") + "<td>fully reassessed at market value at the change in ownership (no parent-child protection for non-primary residences)</td>" + f"<td>{tag('verified')} {src('boe_prop19')}</td>",
    num("Change to the allowance") + "<td>recalculated every two years from the FHFA California house-price index; the next adjusted amount applies from 16 Feb 2027</td>" + f"<td>{tag('verified')} {src('boe_nr')}</td>",
    num("Supplemental bills") + "<td>a change of ownership triggers reassessment and supplemental billing from the county</td>" + f"<td>{tag('verified')} {src('scc_trb')}</td>",
], "Statutory mechanics")}

<h3>Property A's tax rate area - what is published and what is not</h3>
{tbl(["Component (FY2025-26)", "Rate", "Status", "Source"], rate_rows, "Ad-valorem components read from the county tax rate book (rates per $100 of assessed value)")}
<div class="callout warn"><b>The exact rate-area total is deliberately blank.</b> The parcel's tax rate area code is printed on its property tax bill; publishing the exact total rate with the banded assessed value would narrow a public-record search. What is published: the countywide components above (verified from the book) and the model band 1.04% - 1.25% (assumption, covering the reviewed neighbouring tax-rate-area totals). The discovery action is on <a href="questions.html">Questions</a>: read the rate area and the itemised rate off the owner's own bill - no parcel identity is needed on the site.</div>
<p class="small">Owner-implied reconciliation: the owner's 2026 bill implies roughly 1.3% including flat parcel charges and possible supplemental amounts; the ad-valorem band above is lower, and the difference is the fixed charges. This reconciliation is owner-supplied and unverified.</p>

<h3>Projections, Property A (model outputs, assumptions shown)</h3>
{tbl(["Year", "Assessed value (2% cap from the banded anchor)", "Tax at 1.12% band midpoint", "Market value at 4.5%/yr (assumption)", "Status / sources"], proj_rows, "Property A projections (the exclusion, if claimed at transfer, resets the assessed value to FBV + excess over FBV + the then-current allowance)")}
<p class="small">At a 2040 transfer the model's Prop 19 assessment is {m0(M.scenario_paths(2040)['assessed_after_prop19'])} (current allowance held constant - conservative; the allowance will be higher by then, an assumption sensitivity shown on <a href="scenarios.html">Scenarios</a>).</p>
"""
    return page("Property tax & assessment", body)


def p_inheritance_tax():
    t40 = M.scenario_paths(2040)
    sale_rows = [
        num("SCC documentary transfer tax, Property A") + num(ex(M.STATUTORY["scc_transfer_tax_per_500"]) + " per $500") + f"<td>{tag('exact')} {src('scc_rec')}</td>",
        num("...priced into a 2040 sale") + num(m0(t40["transfer_tax"])) + f"<td>{tag('assumption')} {src('scc_rec')}</td>",
        num("Recording fees per deed") + num("SB 2 fee " + ex(M.STATUTORY["scc_sb2_fee"]) + " + AB 1466 fee " + ex(M.STATUTORY["scc_ab1466_fee"]) + " + base first-page fee (see fee schedule)") + f"<td>{tag('exact')} {src('scc_rec')}</td>",
        num("SF transfer tax, tier $1M-under $5M (applies to a Property B sale)") + num(ex(M.STATUTORY["sf_transfer_per_500_1m_5m"]) + " per $500") + f"<td>{tag('exact')} {src('sf_asr')}</td>",
        num("...priced into a $1.8M Property B sale") + num(m0(M.transfer_tax_b(1_800_000))) + f"<td>{tag('assumption')} {src('sf_asr')}</td>",
        num("SF top tiers (not triggered below $10M)") + num("5.5% ($10M-under $25M); 6% ($25M+)") + f"<td>{tag('verified')} {src('sf_digest')}</td>",
        num("Brokerage / selling commission") + num(pc(M.ASSUMPTIONS["brokerage_pct"], 1) + " of price (assumption)") + f"<td>{tag('assumption')} - commissions are negotiable; no official rate exists</td><td></td>",
        num("Flat sale fees") + num(m0(M.ASSUMPTIONS["sale_fees_flat"])) + f"<td>{tag('assumption')}</td><td></td>",
    ]
    fed_rows = [
        num("Basic exclusion amount, 2026") + num(ex(M.STATUTORY["estate_exclusion_2026"]) + " per person") + f"<td>{tag('exact')} {src('irs_wftc','irs_rp2532')}</td>",
        num("Indexation after 2026") + "<td>adjusted for inflation for years after 31 Dec 2026 (OBBBA sec. 70106) - enacted, not a sunset</td>" + f"<td>{tag('exact')} {src('irs_rp2532')}</td>",
        num("GST exemption, 2026") + num(ex(M.STATUTORY["gst_exemption_2026"])) + f"<td>{tag('exact')} {src('irs_rp2532')}</td>",
        num("Rate above the exclusion") + num(pc(M.STATUTORY["estate_top_rate_pct"], 0)) + f"<td>{tag('exact')} {src('irs_706')}</td>",
        num("Form 706") + "<td>required when the gross estate plus prior taxable gifts exceeds the exclusion; portability of a deceased spouse's unused exclusion is elected on a timely Form 706 - an adviser question, listed on Questions</td>" + f"<td>{tag('verified')} {src('irs_706')}</td>",
        num("Annual gift exclusion, 2026") + num(ex(19_000) + " per donee") + f"<td>{tag('exact')} {src('irs_rp2532')}</td>",
    ]
    ca_rows = [
        num("California estate tax") + num("$0") + f"<td>{tag('verified')} {src('ftb')}</td>",
        num("California inheritance tax") + num("$0") + f"<td>{tag('verified')} {src('ftb')}</td>",
        num("Step-up in basis") + "<td>inherited property's basis is its fair market value at the date of death (IRC sec. 1014) - a sale soon after death usually realises little taxable gain</td>" + f"<td>{tag('verified')} {src('irs_403')}</td>",
        num("Sec. 121 exclusion (living-then-sell paths)") + f"<td>up to {ex(M.STATUTORY['sec121_single'])} single / {ex(M.STATUTORY['sec121_joint'])} joint of gain on a principal residence with 2 of the last 5 years of ownership and use; switched ON for the live and live-then-sell paths on this desk</td>" + f"<td>{tag('exact')} {src('irs_703')}</td>",
        num("California income tax on gains") + "<td>capital gains taxed as ordinary income; a 1% tax applies to income over $1,000,000 (see the FTB rate schedules) - CPA question for a large single-year realisation</td>" + f"<td>{tag('verified')} {src('ftb_540')}</td>",
    ]
    proph_rows = [
        num("First bill") + "<td>FY2027-28 property tax bill (mailed fall 2027)</td>" + f"<td>{tag('verified')} {src('sfmta_parcel')}</td>",
        num("Multifamily base (up to 5,000 sq ft)") + num(ex(M.STATUTORY["proph_multifamily_base"]) + "/yr") + f"<td>{tag('exact')} {src('sfmta_faq')}</td>",
        num("Multifamily over 5,000 sq ft") + num("+" + str(M.STATUTORY["proph_multifamily_per_sqft_over_5000"]) + " per sq ft over 5,000 (max " + ex(50_000) + ")") + f"<td>{tag('exact')} {src('sfmta_faq')}</td>",
        num("Escalation") + "<td>amounts rise each year with inflation starting FY2028-29</td>" + f"<td>{tag('verified')} {src('sfmta_faq')}</td>",
        num("Sunset") + "<td>expires 30 Jun 2042 (15 years)</td>" + f"<td>{tag('verified')} {src('sfmta_faq')}</td>",
        num("Modelled 15-year total, base (<=5,000 sq ft, 2.5%/yr inflation assumption)") + num(m0(M.proph_total_15yr())) + f"<td>{tag('assumption')} {src('sfmta_faq')}</td>",
        num("Modelled 15-year total at 8,000 sq ft (sensitivity)") + num(m0(M.proph_total_15yr(sqft=8000))) + f"<td>{tag('assumption')} {src('sfmta_faq')}</td>",
        num("Senior exemption") + "<td>$249 off per unit occupied by a 65+ owner as principal residence, by application</td>" + f"<td>{tag('exact')} {src('sfmta_faq')}</td>",
        num("Rent pass-through") + "<td>rent-controlled units: up to 50% of the tax, max $65/unit/yr</td>" + f"<td>{tag('exact')} {src('sfmta_faq')}</td>",
    ]
    body = f"""
<h3>Federal estate and gift tax (enacted law)</h3>
{tbl(["Item", "Terms", "Status", "Source"], fed_rows, "Federal estate and gift tax, 2026")}
<div class="callout info"><b>Portability and prior gifts - ask now.</b> Whether the estate can add a deceased spouse's unused exclusion depends on a timely estate-tax election, and the lifetime use of the exclusion depends on prior taxable gifts. Both are adviser questions before the transfer window (see <a href="questions.html">Questions</a>).</div>

<h3>California and income-tax treatment</h3>
{tbl(["Item", "Terms", "Status", "Source"], ca_rows, "California tax position and income-tax basis")}

<h3>Sell-path costs, priced in (transfer tax and recording fees)</h3>
{tbl(["Cost item", "Amount", "Status", "Source"], sale_rows, "Costs priced into the sell paths on this desk")}

<h3>Prop H parcel tax on Property B (enacted November 2026)</h3>
{tbl(["Term", "Detail", "Status", "Source"], proph_rows, "SF Proposition H - Stronger Muni For All parcel tax, modelled with its official terms")}
<p class="small">Property B's square footage is unknown, so the model carries the base rate and an 8,000 sq ft sensitivity. The parcel-tax lookup tool opens 1 Dec 2026 and exemption/adjustment applications are due 1 Jun 2027 - both are on the <a href="process.html">deadlines timeline</a>.</p>
"""
    return page("Inheritance & estate tax", body)


def p_running_costs():
    A, B = M.OWNER, M.OWNER
    a_rows = [
        num("Water") + num(m0(A["A_water_lo"]) + "-" + m0(A["A_water_hi"]) + "/mo") + f"<td>{tag('owner')} - banded; provider unconfirmed for the parcel (reference tariff linked)</td>" + f"<td>{src('sjwc','sfpuc')}</td>",
        num("Solar credit") + num("net " + m0(A["A_solar_lo"]) + "-" + m0(A["A_solar_hi"]) + "/mo") + f"<td>{tag('owner')} - production varies; no official figure</td>" + f"<td>{src('cpuc')}</td>",
        num("Electricity") + num("about $0/mo net (credit covers usage, owner-supplied)") + f"<td>{tag('owner')}</td>" + f"<td>{src('cpuc')}</td>",
        num("Insurance") + num("about " + m0(A["A_insurance"]) + "/yr") + f"<td>{tag('owner')} - unverified; CDI is the rate-regulator reference; FAIR Plan is the insurer of last resort</td>" + f"<td>{src('cdi','cfpnet')}</td>",
        num("Maintenance &amp; repairs") + num("model stand-in " + m0(2000) + "/yr") + f"<td>{tag('assumption')} - disclosed input for the model only; obtain a real maintenance plan (discovery action)</td>" + f"<td>{src('cdi')}</td>",
        num("Property tax (occupied, Prop 19 claimed)") + num(m0(M.scenario_paths(2040)["live_tax"]) + "/yr at the 2040 transfer (1.12% midpoint)") + f"<td>{tag('assumption')} {src('boe_nr','boe_prop13')}</td>",
    ]
    b_rows = [
        num("Gross rent (2 rented units)") + num(m0(B["B_rent"]) + "/mo") + f"<td>{tag('owner')}</td>" + f"<td>{src('sf_heirs')}</td>",
        num("Water (3 units)") + num(m0(B["B_water_lo"]) + "-" + m0(B["B_water_hi"]) + "/mo") + f"<td>{tag('owner')}</td>" + f"<td>{src('sfpuc')}</td>",
        num("Electricity") + num(m0(B["B_elec_lo"]) + "-" + m0(B["B_elec_hi"]) + "/mo") + f"<td>{tag('owner')}</td>" + f"<td>{src('cpuc')}</td>",
        num("Insurance") + num("about " + m0(B["B_insurance"]) + "/yr") + f"<td>{tag('owner')} - rental dwelling-fire policy unverified</td>" + f"<td>{src('cdi')}</td>",
        num("Property tax") + num("about " + m0(M.property_b_assessed(2026) * M.OWNER["B_effective_rate"]) + "/yr (2.1% owner-implied rate, banded)") + f"<td>{tag('owner')} - includes flat charges; unverified</td>" + f"<td>{src('boe_prop13','sf_assessor19')}</td>",
        num("Prop H parcel tax, FY2027-28") + num(ex(M.STATUTORY["proph_multifamily_base"]) + "/yr base") + f"<td>{tag('exact')} {src('sfmta_faq')}</td>",
        num("Prop H, modelled FY2041-42 (2.5%/yr inflation assumption)") + num(m0(M.proph_year(2042))) + f"<td>{tag('assumption')} {src('sfmta_faq')}</td>",
        num("Prop H, modelled 15-year total") + num(m0(M.proph_total_15yr())) + f"<td>{tag('assumption')} {src('sfmta_faq')}</td>",
        num("Possible rent pass-through offset") + num("up to 2 x " + ex(M.STATUTORY["proph_passthrough_max"]) + "/yr, if both units are rent-controlled") + f"<td>{tag('exact')} - tenancy status unknown</td>" + f"<td>{src('sfmta_faq')}</td>",
    ]
    body = f"""
<p>Running costs are the reason the letting paths are a floor rather than a forecast: every cost row below is either owner-supplied (unverified), an assumption, or exact. None is presented as a verified market figure. Research pointers replace invented averages, following the repository rule that a value with no official source stays blank.</p>
<h3>Property A (the house to be inherited)</h3>
{tbl(["Cost", "Model figure", "Status", "Source / pointer"], a_rows, "Property A annual running costs")}
<div class="callout warn"><b>Insurance research status:</b> the owner figure (~{m0(M.OWNER['A_insurance'])}/yr) is unverified. The Department of Insurance regulates and publishes market data; the FAIR Plan publishes its own dwelling-fire programme. No statewide average is asserted here because a matching official average for this county and coverage was not confirmed - the row stays blank in the official-verified cell. Discovery actions: get two written quotes and check the FAIR Plan limits on <a href="questions.html">Questions</a>.</div>
<h3>Property B (already owned, 3 units, 2 rented)</h3>
{tbl(["Item", "Model figure", "Status", "Source / pointer"], b_rows, "Property B income and running costs, including the new parcel tax")}
<p class="small">The owner notes the heir can also live in Property B without losing the rental income - that option interacts with the Prop 19 senior exemption ({ex(M.STATUTORY['proph_multifamily_base'])} off per senior-occupied unit, by application) and is modelled as a running-cost reduction possibility, not a verified saving.</p>
"""
    return page("Running costs", body)


def p_projections():
    rows = []
    for y in range(2026, 2051, 2):
        assA = M.property_a_assessed(y)
        mvA = M.property_a_at(y)
        assB = M.property_b_assessed(y)
        taxB = assB * M.OWNER["B_effective_rate"]
        proph = M.proph_year(y)
        proph_disp = "-" if proph == 0 else m0(proph)
        rows.append(
            num(str(y))
            + num(m0(assA))
            + num(m0(assA * M.ASSUMPTIONS["rate_base"]))
            + num(m0(mvA))
            + num(m0(assB))
            + num(m0(taxB))
            + num(proph_disp)
            + f"<td>{tag('assumption')} {src('boe_prop13','sfmta_faq')}</td>")
    stats = M.erp_long_run_stats()
    body = f"""
<p>Year-by-year model outputs, 2026-2050, all rounded to $10. Assessed values grow at the Prop 13 cap (2%/yr) from banded owner anchors; market values at the 4.5%/yr assumption; Property A's tax at the 1.12% band midpoint; Property B's tax at the 2.1% owner-implied rate (banded). The parcel-tax line is the official Prop H schedule escalated at the 2.5%/yr assumption.</p>
{tbl(["Year", "A assessed", "A tax/yr", "A market value", "B assessed", "B tax/yr", "Prop H (B)", "Status / sources"], rows, "Projections (model outputs; every input labelled on the pages that introduce it)")}
<h3>How uneven the real record is (why a single smooth projection is not enough)</h3>
{tbl(["Measure (official record)", "Value", "Source"], [
    num("S&amp;P composite annual price change range, 1976-2025") + num("about -38% to +31%") + f"<td>{tag('verified')} {src('erp_b55')}</td>",
    num("3-month bill rate range, 1975-2025 annual averages") + num(pc(min(M.TB3MS.values()), 2) + " to " + pc(max(M.TB3MS.values()), 2)) + f"<td>{tag('verified')} {src('fred_tb3ms')}</td>",
    num("S&amp;P price CAGR, 1975-2025") + num(pc(stats["price_cagr_pct"], 2)) + f"<td>{tag('verified')} {src('erp_b55')}</td>",
    num("Mean annual total return (price + dividend), 1976-2025") + num(pc(stats["mean_total_return_pct"], 2)) + f"<td>{tag('verified')} {src('erp_b55','erp_b56')}</td>",
    num("Mean dividend-price ratio, 1975-2025") + num(pc(stats["mean_dividend_yield_pct"], 2)) + f"<td>{tag('verified')} {src('erp_b56')}</td>",
], "The official record varies enormously - the black-swan page replays it")}
<p class="small">These year-by-year figures are planning aids. The recommendation logic lives in the <a href="scenarios.html">break-evens</a> and the <a href="black-swan.html">regime replays</a>, not in any single line of this table.</p>
"""
    return page("Projections 2026-2050", body)


def p_scenarios():
    t40 = M.scenario_paths(2040)
    rbe, det = M.required_rent_break_even(2040)
    y, det2 = M.live_vs_rent_break_even_yield(2040)
    stat = f"{tag('assumption')} {src('erp_b55','boe_nr','scc_rec')}"
    rows_main = [
        num("Live in A (Prop 19 claimed)") + "<td>occupy as principal residence within 1 year; homeowners' exemption filed within 1 year</td>" + num(m0(t40["assessed_after_prop19"])) + num(m0(t40["live_tax"])) + "<td>no rent income; value of occupancy = avoided rent</td>" + "<td>house is illiquid; costs continue</td>" + f"<td>{stat}</td>",
        num("Rent A (whole house)") + "<td>letting disqualifies the Prop 19 exclusion: full reassessment to market value</td>" + num(m0(t40["mv_at_transfer"])) + num(m0(t40["mv_at_transfer"] * M.ASSUMPTIONS["rate_base"])) + "<td>needs break-even rent " + m0(rbe) + "/mo gross to match selling</td>" + "<td>management + vacancy assumed 8% + 5% (assumptions)</td>" + f"<td>{stat}</td>",
        num("Sell A, reinvest") + "<td>step-up basis: little gain if sold near the transfer; transfer tax and fees priced in</td>" + num(m0(t40["mv_at_transfer"])) + "<td>none after sale</td>" + "<td>proceeds " + m0(t40["proceeds"]) + " after " + m0(t40["brokerage"]) + " brokerage (assumption) + " + m0(t40["transfer_tax"]) + " transfer tax + " + m0(t40["sale_fees_flat"]) + " fees</td>" + "<td>fully liquid</td>" + f"<td>{stat}</td>",
        num("Mixed: live, then sell") + "<td>occupy first; sec. 121 exclusion available (2 of last 5 years)</td>" + num(m0(t40["assessed_after_prop19"])) + num(m0(t40["live_tax"])) + "<td>occupancy years reduce the taxable gain on a later sale</td>" + "<td>liquid only at the later sale</td>" + f"{stat.replace(tag('assumption'), tag('assumption') + ' ' + src('irs_703'))}" if False else f"<td>{stat} {src('irs_703')}</td>",
        num("Mixed: rent, then sell") + "<td>rented years reassess the property; a later move-in can restart sec. 121 use</td>" + num(m0(t40["mv_at_transfer"])) + num(m0(t40["mv_at_transfer"] * M.ASSUMPTIONS["rate_base"])) + "<td>rent income while waiting for a sale window</td>" + "<td>liquid only at the later sale</td>" + f"<td>{stat} {src('irs_703','boe_prop19')}</td>",
        num("Mixed: sell, then phase (park 24-36 months)") + "<td>proceeds parked in 3M-2Y Treasuries, then phased into equities</td>" + num(m0(t40["mv_at_transfer"])) + "<td>none after sale</td>" + "<td>reduces crash-entry risk; costs about " + m0(M.reinvestment_cost_no_crash(park_months=36, phase_months=24)[2]) + " per " + m0(10000) + " over 10 years on a flat market</td>" + "<td>liquid during the park</td>" + f"<td>{stat} {src('treasury','fedhist_gr')}</td>",
    ]
    sens_rows = []
    for r in (0.05, 0.07, 0.09, 0.11):
        rb, _ = M.required_rent_break_even(2040, alt_return=r)
        sens_rows.append(num(pc(r * 100, 1)) + num(m0(rb) + "/mo") + f"<td>{tag('assumption')} {src('erp_b55')}</td>")
    body = f"""
<p>Every path below is computed at the <b>same transfer date (2040 shown; 2045 and 2050 in the executive summary)</b> and the <b>same horizon end (2076)</b>, with taxes, occupancy changes, capital costs and liquidity treated per path. Figures are model outputs from banded owner anchors; assumptions are listed and sourced.</p>
{tbl(["Path", "Occupancy / tax treatment", "Assessed after transfer", "Property tax, year 1", "Income effect", "Liquidity", "Key figures", "Status / sources"], rows_main, "Paths compared on identical dates and horizons (transfer year 2040)")}
<h3>Sensitivity: the break-even rent moves with the reinvestment return</h3>
{tbl(["Reinvestment return (assumption)", "Break-even gross rent, 2040 transfer", "Status / source"], sens_rows, "If the sale proceeds can earn more, the rent needed to justify keeping rises")}
<div class="callout info"><b>How to read this:</b> the model does not know the market rent of Property A - it computes what that rent would have to be. If a written comparable-rent estimate comes in above {m0(rbe)}/month (2040, base case), renting beats selling on these assumptions; below it, selling wins; occupying wins over renting when the owner values living there above {pc(y * 100, 2)} of house value per year. The 2045 and 2050 columns and the full input list are on <a href="executive-summary.html">Executive summary</a>; change the assumptions on <a href="what-if.html">What-if</a>.</div>
"""
    return page("Scenarios: live / rent / sell / mixed", body)


def p_black_swan():
    r29 = M.phasing_replay_table(10_000)
    md29, md08 = M.CRASH_1929["months_down"], M.CRASH_2008["months_down"]
    h29, h08 = md29 + 60, md08 + 60
    lump29_t = M.lump_sum_at_peak(M.CRASH_1929, 10_000, md29)
    lump29_h = M.lump_sum_at_peak(M.CRASH_1929, 10_000, h29)
    lump08_t = M.lump_sum_at_peak(M.CRASH_2008, 10_000, md08)
    lump08_h = M.lump_sum_at_peak(M.CRASH_2008, 10_000, h08)
    rows = []
    for crash, park, phase, lt, vt, dt, lh, vh, dh in r29:
        rows.append(
            num(crash["peak_label"].split(" (")[0])
            + num(str(park))
            + num(str(phase))
            + num(m0(vt))
            + num(m0(vt - lt))
            + num(m0(vh))
            + num(m0(vh - lh))
            + f"<td>{tag('assumption')} {src('fedhist_1929') if crash is M.CRASH_1929 else src('fedhist_gr','fred_tb3ms','erp_b55')}</td>")
    rows.insert(0, num("1929: all-in at the peak") + num("-") + num("-") + num(m0(lump29_t)) + num("-") + num(m0(lump29_h)) + num("-") + f"<td>{tag('verified')} {src('fedhist_1929')}</td>")
    rows.insert(5, num("2008: all-in at the peak") + num("-") + num("-") + num(m0(lump08_t)) + num("-") + num(m0(lump08_h)) + num("-") + f"<td>{tag('verified')} {src('fedhist_gr')}</td>")
    cost36 = M.reinvestment_cost_no_crash(park_months=36, phase_months=24)
    cost24 = M.reinvestment_cost_no_crash(park_months=24, phase_months=12)
    stats = M.erp_long_run_stats()
    body = f"""
<div class="callout warn"><b>Reinvestment risk, stated beside the headline.</b> The phased-investing path - park the after-tax sale proceeds in 3-month to 2-year Treasuries for 24-36 months, then phase into equities - <b>adds</b> about {m0(cost24[2])}-{m0(cost36[2])} per {m0(10000)} over ten years on a flat market (at the {pc(M.ASSUMPTIONS['base_equity_return'],1)} base-case return assumption; the official ERP record's mean total return is {pc(stats['mean_total_return_pct'],1)}). <b>Subtracts</b> nothing in the official 2008 replay at trough+60 (phased ends {m0(M.replay_strategy(M.CRASH_2008, 24, 12, 10000, h08))} vs {m0(lump08_h)} all-in at the peak) and roughly halves the 1929-style drawdown damage. It is insurance whose premium is measurable, not a free lunch.</div>

<h3>Why a flat projection is not enough</h3>
<p>Growth and inflation are never consistent over 50 years. The official record shows annual equity price changes from about -38% to +31% and bill rates from {pc(min(M.TB3MS.values()),2)} to {pc(max(M.TB3MS.values()),2)} between 1975 and 2025. Two official episodes anchor the stress replays:</p>
{tbl(["Episode (official)", "Drawdown", "Duration", "Recovery", "Source"], [
    num("1929 crash") + num("-89% (DJIA 381.17 on 3 Sep 1929 to 41.22 on 8 Jul 1932)") + num("34 months peak-to-trough") + num("pre-crash level regained 23 Nov 1954 (25 years)") + f"<td>{tag('verified')} {src('fedhist_1929')}</td>",
    num("2007-09 crisis") + num("-57% (S&amp;P 500, Oct 2007 peak to Mar 2009 trough)") + num("17 months peak-to-trough") + num("end-of-year 2013 index above the 2007 peak (official ERP table)") + f"<td>{tag('verified')} {src('fedhist_gr','erp_b55')}</td>",
    num("Housing in the same episode") + num("home prices about -30% (mid-2006 to mid-2009)") + num("about 3 years") + num("national average, official essay") + f"<td>{tag('verified')} {src('fedhist_gr')}</td>",
    num("Macro in the same episode") + num("real GDP -4.3%; unemployment 5% to 10%") + num("Dec 2007-Jun 2009") + num("official essay") + f"<td>{tag('verified')} {src('fedhist_gr')}</td>",
], "Official crash anchors")}

<h3>The phased-investing path, specified</h3>
{tbl(["Stage", "Where the money is", "Duration", "Why"], [
    num("1. Inheritance and sale") + "<td>after-tax proceeds (step-up basis: little gain if sold near the transfer)</td>" + num("month 0") + "<td>liquidity for estate costs and taxes</td>" + f"<td>{tag('owner')} {src('irs_403')}</td>",
    num("2. Park") + "<td>3-month to 2-year Treasuries (current curve: 3M " + pc(M.CURRENT_3M, 2) + ", 2Y " + pc(M.CURRENT_2Y, 2) + ", 13 Nov 2026)</td>" + num("24 or 36 months") + "<td>preserve capital; avoid committing the whole sum at one price</td>" + f"<td>{tag('verified')} {src('treasury')}</td>",
    num("3. Phase in") + "<td>equal monthly tranches into a diversified equity portfolio</td>" + num("12 or 24 months") + "<td>average entry price across conditions</td>" + f"<td>{tag('assumption')} {src('erp_b55')}</td>",
    num("4. Hold") + "<td>per the written investment policy</td>" + num("ongoing") + "<td>the long-run return the plan assumes</td>" + f"<td>{tag('owner')}</td>",
], "Phased path (a proposal awaiting owner decision on the suggestions board)")}
<p class="small">The parking leg today would earn the published Treasury curve rates above; what it earned historically is taken from the official record where one exists (2008 replay: annual average bill rates {pc(M.TB3MS[2007],2)} (2007), {pc(M.TB3MS[2008],2)} (2008), {pc(M.TB3MS[2009],2)} (2009), then near zero) and is an assumption where none does (1929 replay: 2.0%/yr, no official FRED bill series before 1934).</p>

<h3>Quantified replay: $10,000 of sale proceeds</h3>
{tbl(["Replay (price index, no dividends)", "Park (months)", "Phase (months)", "Value at the trough", "vs all-in at the peak at the trough", "Value at trough + 60 months", "vs all-in at the peak at trough + 60", "Status / sources"], rows, "Phased-entry replay against the official 1929 and 2008 drawdowns (model outputs; paths are interpolations between official endpoints - see Methodology)")}
<p class="small">Reading: all-in at the 1929 peak leaves {m0(lump29_t)} at the trough and needs the official 25 years to regain the pre-crash price level; parking 36 months preserves the full principal to {m0(M.replay_strategy(M.CRASH_1929, 36, 12, 10000, md29))} through the trough and phases in at prices far below the peak. In the 2008 replay every phased variant ends ahead of all-in-at-the-peak at trough+60, on the official ERP recovery path. <b>Both replays use price indexes only (no dividends), interpolated between official endpoints; the 1929 recovery and parking yield are labelled assumptions.</b> If no crash arrives, the cushion costs {m0(cost24[2])}-{m0(cost36[2])} per {m0(10000)} over ten years (base-case return). That pair of numbers - not either alone - is the decision.</p>

<h3>What the replay does not cover</h3>
<ul>
<li>Dividends are excluded from both replays (price index), which understates the all-in strategy's recovery; the pages say so wherever the numbers appear.</li>
<li>The 1929 monthly path is an interpolation between official endpoints (plus the official mid-November 1929 "lost almost half" point); the real path was jagged.</li>
<li>Taxes on the parking leg (interest is ordinary income) are noted, not modelled - a CPA question for the year of the sale.</li>
<li>A crash during the park that coincides with a housing drawdown (about -30% mid-2006 to mid-2009) hits the keep paths too; the decision is between two risk exposures, not risk versus safety.</li>
</ul>
"""
    return page("Black swan & phased investing", body)


def p_what_if():
    rows = []
    for g in (0.025, 0.035, 0.045, 0.055):
        rb, _ = M.required_rent_break_even(2040)
        # recompute with the custom growth via a direct call
        import math
        mv = M.property_a_at(2040, g)
        proceeds = mv - mv * M.ASSUMPTIONS["brokerage_pct"] - M.transfer_tax_a(mv) - M.ASSUMPTIONS["sale_fees_flat"]
        sell = proceeds * (1.07) ** 36
        keep = M.property_a_at(2076, g)
        rent, _ = M.required_rent_break_even(2040)
        rows.append(num(pc(g * 100, 1)) + num(m0(mv)) + num(m0(sell)) + num(m0(keep)) + f"<td>{tag('assumption')}</td>")
    body = f"""
<p>Two controls: a static sensitivity grid (this page) and a small calculator (below). The grid varies one input at a time around the base case (property growth 4.5%/yr, equities 7.0%/yr, 2040 transfer, horizon 2076).</p>
<h3>Property growth sensitivity (2040 transfer)</h3>
{tbl(["Market growth assumption", "A value at 2040", "Sell-then-reinvest at 2076 (7%/yr)", "Keep value at 2076", "Status"], rows, "One-at-a-time sensitivity (model outputs)")}
<h3>Calculator</h3>
<div class="callout">
<p><label>Transfer year: <select id="wf-year"><option>2040</option><option>2045</option><option>2050</option></select></label>
&nbsp; <label>Market growth %/yr: <input id="wf-growth" type="number" value="4.5" step="0.5" min="0" max="10" style="width:5em"></label>
&nbsp; <label>Equity return %/yr: <input id="wf-return" type="number" value="7.0" step="0.5" min="0" max="15" style="width:5em"></label>
&nbsp; <button id="wf-go" type="button">Compute</button></p>
<table class="data" id="wf-table"><tbody id="wf-out"></tbody></table>
<p class="small">The calculator mirrors the model formulas (Prop 19 assessed = market value minus the current allowance when the heir occupies; transfer tax $0.55 per $500; 5% brokerage assumption; $100 flat fees; phased variant parks 36 months at the 13 Nov 2026 3-month yield and phases in over 24 months on a flat market). It is a planning aid, not advice.</p>
</div>
"""
    return page("What-if controls", body)


def p_process():
    steps = [
        (num("1") + "<td>Trustee triggers: obtain certified copies of the trust, death certificate, and the trustee's deed authority</td>" + f"<td>{tag('verified')} {src('sf_heirs')}</td>"),
        (num("2") + "<td>Date-of-death appraisal of Property A: fixes the stepped-up basis and any estate-tax valuation</td>" + f"<td>{tag('verified')} {src('irs_403','irs_706')}</td>"),
        (num("3") + "<td>Estate inventory incl. the cash portion; test against the federal exclusion; CPA review of portability and prior taxable gifts</td>" + f"<td>{tag('verified')} {src('irs_706','irs_rp2532')}</td>"),
        (num("4") + "<td>File Form 706 if required (due on the IRS schedule stated on the form page); elect portability if applicable</td>" + f"<td>{tag('verified')} {src('irs_706')}</td>"),
        (num("5") + "<td>Change-in-ownership filing with the county assessor; claim the Prop 19 exclusion on form BOE-19-P only if the heir will occupy (within three years), and file the homeowners' exemption within one year</td>" + f"<td>{tag('exact')} {src('boe_pub801','boe_nr')}</td>"),
        (num("6") + "<td>Insurance: renew or rewrite the policy for the new ownership/occupancy; get written quotes (state-regulated market; FAIR Plan as last resort)</td>" + f"<td>{tag('verified')} {src('cdi','cfpnet')}</td>"),
        (num("7") + "<td>Utilities: confirm the parcel's water provider and meter set-up; keep the solar credit arrangement in the new ownership</td>" + f"<td>{tag('owner')} {src('sjwc','sfpuc','cpuc')}</td>"),
        (num("8") + "<td>Decide the path (live / rent / sell / mixed) against the break-evens on Scenarios; record the decision and date in the decision log</td>" + "<td>" + tag('owner') + ' <a href="scenarios.html">Scenarios</a></td>'),
        (num("9") + "<td>If selling: price the transfer tax, recording fees and brokerage; record the deed; PCOR required</td>" + f"<td>{tag('exact')} {src('scc_rec')}</td>"),
        (num("10") + "<td>If selling: put the written investment policy in place BEFORE proceeds arrive; adopt or reject the phased path</td>" + f"<td>{tag('owner')} {src('treasury')}</td>"),
        (num("11") + "<td>Property B only: Prop H parcel-tax lookup from 1 Dec 2026; exemption or adjustment applications due 1 Jun 2027</td>" + f"<td>{tag('verified')} {src('sfmta_parcel','sfmta_faq')}</td>"),
        (num("12") + "<td>Annual re-run: update inputs, re-check the law watch, re-verify the figures; note what changed and why</td>" + f"<td>{tag('owner')} {src('boe_nr')}</td>"),
    ]
    timeline = [
        (num("At death") + "<td>date-of-death value set; step-up in basis; change-in-ownership clock starts</td>" + f"<td>{tag('verified')} {src('irs_403','boe_nr')}</td>"),
        (num("Within 1 year") + "<td>occupancy + homeowners' exemption filing to keep the Prop 19 exclusion</td>" + f"<td>{tag('exact')} {src('boe_nr','boe_pub801')}</td>"),
        (num("9 months") + "<td>federal estate-tax return due (with the extension the form provides) where required; portability election is timely-filed on it</td>" + f"<td>{tag('verified')} {src('irs_706')}</td>"),
        (num("1 Dec 2026") + "<td>Prop H exemption portal and parcel-tax lookup open (Property B)</td>" + f"<td>{tag('verified')} {src('sfmta_parcel')}</td>"),
        (num("1 Jun 2027") + "<td>Prop H exemption/adjustment applications due for FY2027-28 (Property B)</td>" + f"<td>{tag('verified')} {src('sfmta_parcel','sfmta_faq')}</td>"),
        (num("Fall 2027") + "<td>first Prop H charge appears on the FY2027-28 bill (Property B)</td>" + f"<td>{tag('verified')} {src('sfmta_parcel')}</td>"),
        (num("Within 3 years") + "<td>BOE-19-P claim period for the Prop 19 exclusion after a transfer that qualifies</td>" + f"<td>{tag('exact')} {src('boe_pub801')}</td>"),
        (num("16 Feb 2027") + "<td>next Prop 19 allowance window opens (BOE recalculates every two years)</td>" + f"<td>{tag('verified')} {src('boe_nr')}</td>"),
    ]
    body = f"""
<h3>Step-by-step: inheriting Property A through the trust</h3>
{tbl(["Step", "What happens", "Status / sources"], steps, "Inheritance process (the order the paperwork actually follows)")}
<h3>Deadlines timeline</h3>
{tbl(["When", "What", "Status / sources"], timeline, "Deadline timeline (offsets from death unless a date is given)")}
"""
    return page("Trust process & deadlines timeline", body)


def p_briefing_sheet():
    t40 = M.scenario_paths(2040)
    rbe, det = M.required_rent_break_even(2040)
    body = f"""
<div class="callout info no-print"><b>One-page briefing sheet.</b> Print this page for the first attorney and CPA meeting. It carries only verified or explicitly labelled figures and the open questions to bring back.</div>
<h3>Attorney &amp; CPA Briefing Sheet (printable)</h3>
{tbl(["Item", "Brief", "Status / source"], [
    num("Client situation") + "<td>Heir-designate under a family trust for Property A (Santa Clara County, expected transfer 2040-2050). Also owns Property B (San Francisco County; 3 units, 2 rented; may occupy without losing rental income). No other assets modelled here.</td>" + "<td>" + tag("owner") + "</td>",
    num("Federal estate position") + f"<td>2026 basic exclusion {ex(M.STATUTORY['estate_exclusion_2026'])} per person, indexed after 2026; 40% above it; GST exemption {ex(M.STATUTORY['gst_exemption_2026'])}. ASK: estate composition, prior taxable gifts, portability election status.</td><td><span class='tag exact'>exact</span></td>",
    num("California") + "<td>No state estate or inheritance tax. Property tax governed by Prop 13/19. Gains taxed as ordinary income; 1% tax over $1,000,000 of income.</td>" + "<td>" + tag("verified") + " " + src("ftb", "ftb_540") + "</td>",
    num("Basis") + "<td>Property A: stepped-up to date-of-death value (IRC sec. 1014). A sale near the transfer realises little gain.</td>" + "<td>" + tag("verified") + " " + src("irs_403") + "</td>",
    num("Property tax") + f"<td>Prop 19 exclusion (allowance {ex(M.STATUTORY['prop19_allowance'])} in the current window) applies ONLY if the heir occupies and files within the deadlines (occupancy + exemption within 1 year; BOE-19-P within 3 years). Otherwise full reassessment. </td><td><span class='tag exact'>exact</span></td>",
    num("Sell-path costs") + f"<td>SCC transfer tax {ex(M.STATUTORY['scc_transfer_tax_per_500'])}/$500 (2040 model: {m0(t40['transfer_tax'])}); recording fees (SB 2 {ex(M.STATUTORY['scc_sb2_fee'])} + AB 1466 {ex(M.STATUTORY['scc_ab1466_fee'])} + base fee); brokerage 5% assumption. Property B tier: {ex(M.STATUTORY['sf_transfer_per_500_1m_5m'])}/$500 ($1M-under $5M). </td><td><span class='tag exact'>exact</span></td>",
    num("New cost on Property B") + f"<td>Prop H parcel tax {ex(M.STATUTORY['proph_multifamily_base'])}/yr FY2027-28 (multifamily base), indexed from FY2028-29, expires 30 Jun 2042; sq ft over 5,000 adds {M.STATUTORY['proph_multifamily_per_sqft_over_5000']}/sq ft. Lookup 1 Dec 2026; applications due 1 Jun 2027. </td><td><span class='tag exact'>exact</span></td>",
    num("Decision framework") + f"<td>Live beats rent when occupancy value exceeds {pc(M.live_vs_rent_break_even_yield(2040)[0] * 100, 2)}/yr of value; rent beats sell when gross rent exceeds {m0(rbe)}/mo (2040, base case). Sell-and-phase: park 24-36 months in 3M-2Y Treasuries, then phase in - quantified against the official 1929/2008 drawdowns on the desk.</td>" + "<td>" + tag("assumption") + " " + src("erp_b55") + "</td>",
    num("Questions to bring back") + "<td>(1) written date-of-death valuation; (2) written market-rent estimate with comparables; (3) two insurance quotes; (4) water provider confirmation; (5) estate composition + portability + prior gifts; (6) Property B square footage; (7) preferred park/phase months if the sell path is chosen.</td>" + "<td>" + tag("owner") + "</td>",
    num("Decision &amp; date") + "<td>_________________________ (path) &nbsp;&nbsp; ____________ (date) &nbsp;&nbsp; ____________ (signed)</td>" + "<td>" + tag("owner") + "</td>",
], "Briefing sheet (print this page)")}
"""
    return page("Attorney & CPA Briefing Sheet", body, printable=True)


def p_suggestions():
    sug = [
        ("Adopt the phased-investing policy IF the sell path is chosen: park in 3M-2Y Treasuries for 24-36 months, phase into equities over 12-24 months; write it down before proceeds arrive.", "Directly addresses 1929/2008 entry risk quantified on the desk."),
        ("Claim the Prop 19 exclusion only if the heir will occupy long term; otherwise the property is reassessed either way and the letting math applies.", "Avoids claiming and then losing the exclusion."),
        ("Obtain a written date-of-death valuation of Property A (fixes the stepped-up basis).", "Needed for the gain computation on any later sale."),
        ("Obtain a written market-rent estimate with comparables for Property A (replaces the break-even floor with evidence).", "The biggest information gap on the decision."),
        ("Get two written homeowner/landlord insurance quotes; check the FAIR Plan programme limits.", "The insurance rows are owner-supplied and unverified."),
        ("Confirm the parcel's water provider from the bill; replace the banded water row.", "Provider assumption is flagged, not verified."),
        ("Ask the CPA now: portability election status, prior taxable gifts, expected Form 706 need, and the 1% California tax on a large single-year realisation.", "These flip the estate-tax headroom."),
        ("Ask the CPA whether a like-kind exchange is wanted before any sale of either property.", "A sale decision taken before this question can be irreversible."),
        ("Confirm Property B's building area via the Prop H lookup (1 Dec 2026) and file any senior exemption or adjustment by 1 Jun 2027.", "Moves the parcel tax between $249/yr and higher tiers."),
        ("Prepare an estate liquidity plan (cash portion vs the exclusion) before the transfer window.", "The cash portion is the estate's main unknown."),
        ("Write the investment policy statement for sale proceeds, including the park/phase parameters and the target allocation.", "The policy should exist before the money does."),
        ("Re-run this desk annually with updated inputs and re-check the law watch; log the decision and date each year.", "Keeps the outcome from being reverse-engineered from one projection."),
        ("Keep the repository privacy-first: no personal identifiers on the site; exact assessed values stay withheld as banded anchors.", "Follows the standing privacy rule; history rewrite remains an owner decision (see Flagged)."),
        ("Do NOT implement any suggestion until it is marked accept / modify / reject in the decision log.", "The board is advisory by design."),
    ]
    rows = [f"<td>{i+1}</td><td>{t}</td><td>{why}</td><td>{tag('owner')}</td><td>&#9744; accept &nbsp; &#9744; modify &nbsp; &#9744; reject</td>"
            for i, (t, why) in enumerate(sug)]
    body = f"""
<div class="callout warn"><b>Nothing on this board is implemented.</b> Each item is PROPOSED. The owner marks accept / modify / reject and the decision and its date go into the decision log on <a href="executive-summary.html">Executive summary</a>. Only accepted items belong in a future revision.</div>
{tbl(["#", "Suggestion (proposed)", "Why it matters", "Status", "Owner decision"], rows, "Suggestions board - awaiting review")}
"""
    return page("Suggestions board (proposed only)", body)


def p_questions():
    q = [
        ("What is Property A's achievable market rent (with comparables)?", "Owner + market data", "Blocks the rent-vs-sell ranking", "Order a written rental appraisal; the desk's break-even " + m0(M.required_rent_break_even(2040)[0]) + "/mo is the bar to beat"),
        ("What is the estate's composition (cash vs real estate) and its size against the exclusion?", "Owner + CPA", "Blocks estate-tax planning", "Prepare an estate inventory; test against " + ex(M.STATUTORY["estate_exclusion_2026"])),
        ("Is there a deceased spouse's unused exclusion to port, and were there prior taxable gifts?", "CPA", "Blocks the headroom table", "Ask at the first CPA meeting; election is on a timely Form 706"),
        ("Will the heir occupy Property A as a principal residence (within 1 year) and for how long?", "Owner", "Blocks the Prop 19 claim and the live path", "Decide before the transfer; record in the decision log"),
        ("What does Property A's insurance actually cost for the intended occupancy?", "Owner + insurers", "Blocks the carrying-cost total", "Two written quotes; check CDI market data and FAIR Plan terms"),
        ("Which utility serves Property A's parcel for water, and on what schedule?", "Owner + utility", "Blocks the water cost row", "Read it off the current bill (no parcel identity is published)"),
        ("What is Property A's tax rate area and itemised total rate?", "Owner (bill) + county", "Blocks the exact tax projection", "Read the rate area code and rates off the bill; the county book is linked"),
        ("What is Property B's building area (sq ft)?", "Owner", "Blocks the Prop H tier ($249 base vs +$0.195/sq ft)", "Use the official parcel-tax lookup from 1 Dec 2026"),
        ("Are Property B's rented units rent-controlled (pass-through eligibility)?", "Owner + Rent Board", "Blocks the $65/unit offset", "Ask the Rent Board; the cap is official"),
        ("What maintenance/capital plan does each building need over five years?", "Owner + inspector", "Blocks the true net cash flow", "Order a five-year maintenance and capital plan for both buildings"),
        ("Is a like-kind exchange wanted before any sale?", "CPA", "Blocks the sell path mechanics", "Decide BEFORE listing; take advice"),
        ("Should the phased-investing path be adopted, and with what park/phase parameters?", "Owner", "Blocks the sell-and-phase policy", "Choose on the black-swan page's quantified trade-off; write the IPS"),
        ("Which real-estate comparables establish Property A's date-of-death value?", "Appraiser", "Blocks the gain computation", "Commission the appraisal close to the transfer"),
        ("Has any law changed that moves the break-evens?", "Desk + counsel", "Blocks the annual re-run", "Re-check the law-watch page each year; enacted vs proposed is separated"),
        ("Does the trust instrument impose any sale, occupancy or distribution constraint?", "Attorney", "Blocks everything", "Read the trust instrument with counsel first"),
        ("Who is the trustee and what are the fiduciary duties here?", "Attorney", "Blocks the process steps", "Confirm authority and duties in the first attorney meeting"),
    ]
    rows = [f"<td>{i+1}</td><td>{qq}</td><td>{who}</td><td>{blocks}</td><td>{act}</td><td>{tag('owner')}</td>"
            for i, (qq, who, blocks, act) in enumerate(q)]
    body = f"""
<p>The desk already has: the statutory framework (federal exclusion, Prop 13/19, transfer taxes, the new parcel tax, the official crash record). It does not have: the estate's cash composition, Property A's market rent, verified insurance/water/maintenance figures, the parcel's tax rate area, or Property B's square footage. Each gap below has a named owner of the answer and a discovery action; none is filled by inference.</p>
{tbl(["#", "Question / information needed", "Who holds it", "What it blocks", "Discovery action", "Status"], rows, "Questions & information gaps (with discovery actions)")}
"""
    return page("Questions & information gaps", body)


def p_law_watch():
    rows = [
        ("Enacted (federal)", "OBBBA: basic exclusion amount " + ex(M.STATUTORY["estate_exclusion_2026"]) + " for 2026, indexed after 2026; GST exemption " + ex(M.STATUTORY["gst_exemption_2026"]), "Raises and makes permanent the headroom that was due to halve", src("irs_wftc", "irs_rp2532"), tag("exact")),
        ("Enacted (federal)", "Standard deduction and bracket changes for 2026 (OBBBA)", "Context for the income side of a large sale year", src("irs_wftc"), tag("verified")),
        ("Enacted (California)", "Prop 19 in force: family-home exclusion capped at factored base year value + " + ex(M.STATUTORY["prop19_allowance"]) + " for the current window; allowance recalculated every two years", "The heir-occupancy condition decides the assessment", src("boe_nr", "boe_prop19"), tag("exact")),
        ("Enacted (SF, 3 Nov 2026)", "Proposition H parcel tax: multifamily base " + ex(M.STATUTORY["proph_multifamily_base"]) + "/yr (FY2027-28), inflation-indexed from FY2028-29, expires 30 Jun 2042; passed with about 72% of the vote", "New recurring cost on Property B from fall 2027", src("sfmta_faq", "sfmta_parcel"), tag("exact")),
        ("Enacted (California, 1978)", "Prop 13: 1% levy; 2% assessed-value cap", "The reason Property B's tax is low relative to its value", src("boe_prop13"), tag("exact")),
        ("Proposal (SF, Feb 2026)", "BUILD Act plan: return transfer-tax rates for $10M+ non-single-residence transfers to 2.75%/3%", "Not triggered below $10M; watch if either property's value tier changes", src("sf_digest"), tag("verified")),
        ("Measure (SF, Nov 2026)", "Ballot measure dedicating half of the transfer-tax revenue from $10M+ transactions to housing programmes", "Rate-neutral by its digest; outcome to be confirmed - flagged", src("sf_digest"), tag("verified")),
        ("Watch (California)", "Next Prop 19 allowance window from 16 Feb 2027 (BOE recalculates from the FHFA index)", "The allowance the desk holds constant will rise", src("boe_nr"), tag("verified")),
        ("Watch (federal)", "Periodic proposals to cap or eliminate the step-up in basis", "Would change the gain on any sale after the transfer", src("irs_403"), tag("verified")),
        ("Watch (California)", "Home-insurance market and FAIR Plan programme changes", "Affects the unverified insurance rows", src("cdi", "cfpnet"), tag("verified")),
    ]
    rows_html = [f"<td>{k}</td><td>{v}</td><td>{why}</td><td>{s}</td><td>{t}</td>"
                 for k, v, why, s, t in rows]
    body = f"""
<p>Enacted changes are separated from proposals. Enacted items are in force law or approved measures; proposals are plans or pending measures and carry no weight in the model until enacted. The recheck is repeated each re-run (annual, per the process page).</p>
{tbl(["Category", "Item", "Why it matters here", "Source", "Status"], rows_html, "Law watch (enacted vs proposed)")}
"""
    return page("Law watch: enacted vs proposed", body)


def p_glossary():
    terms = [
        ("Step-up in basis (IRC sec. 1014)", "An inherited asset's tax basis resets to its fair market value at the date of death; selling soon after usually realises little taxable gain.", "verified", ("irs_403",)),
        ("Sec. 121 exclusion", "Up to $250,000 ($500,000 joint) of gain excluded when selling a principal residence owned and used 2 of the last 5 years.", "exact", ("irs_703",)),
        ("Basic exclusion amount", "The estate/gift exemption: $15,000,000 per person for 2026, indexed after 2026; 40% applies above it.", "exact", ("irs_wftc", "irs_rp2532")),
        ("Portability", "A surviving spouse may inherit the deceased spouse's unused exclusion by a timely estate-tax election.", "verified", ("irs_706",)),
        ("GST exemption", "Generation-skipping transfer exemption; $15,000,000 for 2026.", "exact", ("irs_rp2532",)),
        ("Prop 13", "California rule: 1% maximum property-tax levy; assessed value rises at most 2%/yr absent ownership change or new construction.", "exact", ("boe_prop13",)),
        ("Prop 19 (intergenerational)", "Parent-child transfer of a family home: assessed value protected up to factored base year value + the adjusted allowance (currently $1,044,586) ONLY for the heir's principal residence, with occupancy and exemption filings within a year; form BOE-19-P within 3 years.", "exact", ("boe_nr", "boe_pub801")),
        ("Factored base year value (FBV)", "The property's current Prop 13 assessed value carried forward at the 2% cap.", "verified", ("boe_prop13",)),
        ("Change in ownership", "The trigger for reassessment; date-of-death is the change date for an inherited property.", "verified", ("boe_prop19",)),
        ("Supplemental bill", "A county bill covering the assessment difference for part of a year after reassessment.", "verified", ("scc_trb",)),
        ("Documentary transfer tax", "County/city tax on recorded property transfers: Santa Clara County $0.55 per $500; SF tiered, $3.75 per $500 for the $1M-under $5M tier.", "exact", ("scc_rec", "sf_asr")),
        ("Recording fees", "Per-deed county fees (SB 2 $75, AB 1466 $2, plus the base first-page fee on the fee schedule).", "exact", ("scc_rec",)),
        ("PCOR", "Preliminary Change of Ownership Report filed with a deed; $20 fee when missing.", "exact", ("scc_rec",)),
        ("Prop H (Stronger Muni For All)", "SF parcel tax approved 3 Nov 2026: multifamily base $249/yr (up to 5,000 sq ft) + $0.195/sq ft over 5,000; indexed from FY2028-29; expires 30 Jun 2042; rent-controlled pass-through capped at 50%, max $65/unit/yr.", "exact", ("sfmta_faq",)),
        ("Phased-investing path", "Park sale proceeds in 3M-2Y Treasuries for 24-36 months, then buy equities in equal monthly tranches over 12-24 months.", "verified", ("treasury", "fedhist_gr")),
        ("Reinvestment risk", "The cost of waiting: what the parked money misses if markets rise, shown beside every phased-path headline here.", "assumption", ("erp_b55",)),
        ("Break-even rent", "The gross monthly rent at which renting the house matches selling and reinvesting, on the stated assumptions.", "assumption", ()),
        ("Avoided-rent yield", "The value of living in the house, expressed as a percentage of its value per year.", "assumption", ()),
        ("Black swan", "A severe, irregular regime (1929-style -89% over 34 months; 2008-style -57% over 17 months), used here to stress-test entry timing.", "verified", ("fedhist_1929", "fedhist_gr")),
        ("Drawdown", "Peak-to-trough decline; the replays use price indexes (no dividends), stated wherever the numbers appear.", "verified", ("fedhist_1929",)),
        ("Owner-supplied (unverified)", "A figure the owner provided that no official source confirms; the official-verified cell stays blank.", "owner", ()),
        ("Assumption", "A disclosed model input that is not asserted as fact; every assumption is listed with the model.", "assumption", ()),
        ("Tax rate area (TRA)", "The county's code for the set of taxing agencies overlapping a parcel; printed on the tax bill; 816 areas in this county.", "verified", ("scc_trb",)),
        ("FAIR Plan", "California's insurer of last resort for properties that cannot obtain standard coverage.", "verified", ("cfpnet",)),
    ]
    rows = []
    for t, d, kind, keys in terms:
        link = src(*keys) if keys else tag(kind)
        rows.append(f"<td><b>{t}</b></td><td>{d}</td><td>{tag(kind)} {link}</td>")
    body = f"<p>Plain-language definitions for every term used on this desk. Statutory figures inside definitions are exact as published.</p>{tbl(['Term', 'Definition', 'Status / source'], rows, 'Glossary')}"
    return page("Glossary", body)


def p_sources():
    rows = []
    statuses = {
        "irs_wftc": "opened and read this session", "irs_rp2532": "opened and read this session",
        "irs_706": "register entry (referenced for filing rules)", "irs_403": "register entry (recorded-verified in this repository)",
        "irs_703": "register entry (recorded-verified in this repository)",
        "boe_nr": "opened and read this session", "boe_prop19": "opened this session (search result extract)",
        "boe_pub801": "opened this session (search result extract)", "boe_prop13": "register entry (recorded-verified)",
        "scc_trb": "opened and read this session (summary pages; TRA tables beyond the parser window)",
        "scc_trb_page": "linked, not opened this session", "scc_rec": "opened and read this session",
        "sf_asr": "opened this session (search result extract of the official factsheet)",
        "sf_digest": "opened this session (search result extract of the official digest)",
        "sf_heirs": "linked, not opened this session", "sfmta_parcel": "opened this session (search result extract)",
        "sfmta_faq": "opened and read this session", "fedhist_1929": "opened and read this session",
        "fedhist_gr": "opened and read this session", "treasury": "opened and read this session",
        "fred_tb3ms": "values transcribed in this repository with documented provenance (see Methodology)",
        "erp_b55": "values transcribed in this repository with documented provenance", "erp_b56": "values transcribed in this repository with documented provenance",
        "ftb": "register entry (recorded-verified)", "ftb_540": "register entry (recorded-verified)",
        "cdi": "pointer - not opened this session", "cfpnet": "pointer - not opened this session",
        "sfpuc": "pointer - not opened this session", "sjwc": "pointer - provider unconfirmed for the parcel",
        "cpuc": "pointer - not opened this session", "sf_assessor19": "pointer - not opened this session",
        "leginfo": "pointer - statutes portal",
    }
    for k, (label, url) in SRC.items():
        rows.append(f"<td><b>{k}</b></td><td>{label}</td><td>{statuses.get(k, '')}</td>"
                    f"<td><a href=\"{url}\" target=\"_blank\" rel=\"noopener\">{url}</a></td>")
    body = f"""
<p>Every official document this desk relies on. "Opened and read this session" means the page or document was fetched and read during the 2026-11-15 build; "recorded-verified" means earlier sessions of this repository checked it and recorded the check (their records are in COORDINATION.md); "pointer" means the link is provided for the owner's own check and no value is asserted from it.</p>
{tbl(["Key", "Document", "Verification status", "URL"], rows, "Source register")}
"""
    return page("Sources", body)


def p_flagged():
    flags = [
        ("F01", "Owner-supplied figures are unverified", "Property A value, Property B value and rent, water, electricity, solar credit and insurance figures are owner inputs. They are labelled owner-supplied and the official-verified cells are blank.", "Owner to supply documents or the rows stay unverified."),
        ("F02", "Insurance: no verified market figure", "The ~$1,500/yr figure is the owner's estimate. No county-and-coverage-matched official average was confirmed, so none is asserted (this corrects the irregularity another session logged against an earlier desk's untraceable range).", "Two written quotes; CDI market data."),
        ("F03", "Water provider for Property A unconfirmed", "The provider depends on the parcel; the reference tariff is linked but the row stays banded and unverified.", "Read the provider off the bill."),
        ("F04", "Exact assessed values and tax history withheld", "Assessed values are public records matchable to a parcel; the desk publishes banded anchors instead of the owner's exact history. This departs from a literal reading of the $10-rounding instruction in the protective direction, as earlier desks did.", "Owner can request exact-value publication; the risk note stays either way."),
        ("F05", "Property A's tax rate area total is blank", "The county book's rate-area tables for the parcel's area were beyond the parseable window of the official PDF in this session; the countywide components are published instead.", "Read the rate area off the owner's bill; no parcel identity is needed on the site."),
        ("F06", "1929 replay parking yield is an assumption", "No official FRED bill series exists before 1934; the replay assumes 2.0%/yr for 1929-34 and says so everywhere the number appears.", "Historical statistics volumes could replace it; not material to the sign of the result."),
        ("F07", "Replays are price-index only", "No dividends in either crash replay; the all-in strategy's recovery is understated and the pages say so.", "A dividend-inclusive replay could be added if requested."),
        ("F08", "Paths between official endpoints are interpolations", "The 1929 drawdown/recovery and the 2008 drawdown are monthly interpolations between official endpoints; the 2008 recovery uses the official ERP annual path.", "Real monthly index histories could be transcribed from official archives if requested."),
        ("F09", "Brokerage 5% and flat fees $100 are assumptions", "Commissions are negotiable and no official rate exists; the amount is a disclosed model input, not a verified cost.", "Replace with a real listing-agent estimate."),
        ("F10", "Maintenance is a model stand-in ($2,000/yr)", "Disclosed assumption, not a verified cost; the owner reported only that Property A needs less than Property B.", "Five-year maintenance and capital plan (suggestion 10)."),
        ("F11", "Property B's tax rate is owner-implied", "2.1% banded, includes flat charges; not an official ad-valorem rate.", "Read the bill's rate components."),
        ("F12", "Property B's building area unknown", "Prop H is modelled at the base rate and an 8,000 sq ft sensitivity; the real bill depends on the lookup.", "Official parcel-tax lookup from 1 Dec 2026."),
        ("F13", "Form 706 instructions not read line-by-line this session", "The filing/deadline rows cite the IRS Form 706 page rather than the full instruction booklet; recorded-verified in earlier sessions' records.", "Read the booklet before filing; not a published figure on this desk."),
        ("F14", "Nov 2026 SF transfer-tax measure outcome unconfirmed", "The digest was read; the result of that measure is not stated on this desk.", "Confirm with the Department of Elections; the $10M+ tiers do not affect either property below $10M."),
        ("F15", "Prior desks' flag lineage", "This desk inherits the open items recorded by earlier sessions (e.g., unverified insurance ranges, provider assumptions, the git-history privacy question). Nothing here repeats their figures.", "See the repository's COORDINATION.md and each desk's flagged page."),
    ]
    rows = [f"<td><b>{k}</b></td><td>{t}</td><td>{d}</td><td>{a}</td><td>{tag('unverified')}</td>" for k, t, d, a in flags]
    body = f"""
<p>Items below are <b>not blocking</b>; they are published here so the owner can review them after the site is live and request changes. Unverified values stay blank on the pages rather than being filled in.</p>
{tbl(["#", "Flag", "Detail", "What would clear it", "Status"], rows, "Flagged for review")}
"""
    return page("Flagged for review", body)


def p_methodology():
    stats = M.erp_long_run_stats()
    body = f"""
<h3>Rounding and figure rules</h3>
<ul>
<li>Money is rounded to the <b>nearest $10</b> unless it is a statutory or agency-published amount, which is quoted exactly as published and tagged <span class="tag exact">exact (statutory)</span>.</li>
<li>Every table row carries an official source link, or is blank and tagged <span class="tag unverified">unverified</span>, or is a disclosed <span class="tag assumption">assumption</span> / <span class="tag owner">owner-supplied</span> input. No value is inferred into a blank.</li>
<li>Model outputs are derived values: their method and every input are shown on the pages that use them.</li>
</ul>
<h3>Model inputs (all disclosed)</h3>
{tbl(["Input", "Value", "Kind"], [
    num("Property A market value, Nov 2026") + num(m0(M.OWNER["A_value_2026"])) + f"<td>{tag('owner')}</td>",
    num("Property A assessed anchor (banded)") + num("about " + m0(M.OWNER["A_assessed_2026"])) + f"<td>{tag('owner')}</td>",
    num("Property A market growth") + num(pc(M.ASSUMPTIONS["a_growth"] * 100, 1) + "/yr") + f"<td>{tag('assumption')}</td>",
    num("Ad-valorem tax band (A)") + num(pc(M.ASSUMPTIONS["rate_lo"] * 100, 2) + " - " + pc(M.ASSUMPTIONS["rate_hi"] * 100, 2)) + f"<td>{tag('assumption')} - band around the verified countywide components {src('scc_trb')}</td>",
    num("Reinvestment return (base case)") + num(pc(M.ASSUMPTIONS["base_equity_return"], 1) + "/yr") + f"<td>{tag('assumption')} - below the official ERP record mean {pc(stats['mean_total_return_pct'],1)} {src('erp_b55','erp_b56')}</td>",
    num("Rent growth / management / vacancy") + num(pc(M.ASSUMPTIONS["rent_growth"] * 100, 0) + " / " + pc(M.ASSUMPTIONS["mgmt_pct"] * 100, 0) + " / " + pc(M.ASSUMPTIONS["vacancy_pct"] * 100, 0)) + f"<td>{tag('assumption')}</td>",
    num("Brokerage / flat fees / maintenance stand-in") + num(pc(M.ASSUMPTIONS["brokerage_pct"] * 100, 0) + " / " + m0(M.ASSUMPTIONS["sale_fees_flat"]) + " / " + m0(2000)) + f"<td>{tag('assumption')}</td>",
    num("Inflation for cost escalation") + num(pc(M.ASSUMPTIONS["inflation"] * 100, 1) + "/yr") + f"<td>{tag('assumption')}</td>",
    num("Prop H inflation path") + num("2.5%/yr from FY2028-29 (official schedule escalates with inflation)") + f"<td>{tag('assumption')} {src('sfmta_faq')}</td>",
    num("1929 parking yield") + num(pc(M.CRASH_1929["park_yield_pct"], 1) + "/yr") + f"<td>{tag('assumption')} - no official series before 1934</td>",
], "Model inputs and their status")}
<h3>Crash-replay method</h3>
<ul>
<li>Drawdown paths are monthly interpolations between official anchors (Federal Reserve History endpoints; the 1929 path also uses the official mid-November 1929 point). The 2008 recovery follows the official ERP end-of-year index levels for 2009-2013, then holds flat.</li>
<li>Price indexes only: dividends are excluded (understating the all-in strategy's recovery), and every table that shows replay numbers says so.</li>
<li>Parking yields: official FRED annual average bill rates for the 2008 replay; a labelled 2.0%/yr assumption for the 1929 replay; today's published Treasury curve for the "what the park earns now" line.</li>
<li>Series values (S&amp;P annual levels and dividend ratios; bill rates) are transcriptions of official publications whose provenance was established and audited in this repository (see the swan data README on main); the official URLs are on <a href="sources.html">Sources</a>.</li>
</ul>
<h3>Verification performed this session</h3>
<ul>
<li>Row-by-row build check (verify.py): every data row sourced or explicitly marked; official-host allowlist; internal links resolve; $10 rounding; statutory figures exact; PII/identifier scan; internal-link and cross-reference checks. 16 unit tests on the model (rounding, path anchors, replay mechanics, tax math).</li>
<li>Repository checks: verify_safe.py, privacy_scan.py, check_landing.py.</li>
<li>Sources opened and read this session: IRS Working Families page and Rev. Proc. 2025-32; BOE NR-25-02, Prop 19 page and Pub 801; SCC Tax Rate Book FY2025-26 (summary pages) and Clerk-Recorder fee pages; SF Assessor-Recorder transfer-tax factsheet and Nov 2026 ballot digest; SFMTA Prop H page and FAQ; Federal Reserve History 1929 and Great Recession essays; Treasury daily par yield curve (13 Nov 2026).</li>
</ul>
<h3>Privacy</h3>
<ul>
<li>No names, street addresses, ZIP codes, city names, parcel or account numbers appear anywhere on this desk. The two properties are described at county level only.</li>
<li>Exact per-year assessed values and tax bills are withheld (banded anchors used instead) because assessed values are public records that can be matched to a parcel.</li>
<li>No personal information appears in the final published product; the owner's exact figures remain in the owner's private records.</li>
</ul>
"""
    return page("Methodology & privacy", body)


PAGES = [
    ("index.html", p_index),
    ("executive-summary.html", p_executive_summary),
    ("properties.html", p_properties),
    ("property-tax.html", p_property_tax),
    ("inheritance-tax.html", p_inheritance_tax),
    ("running-costs.html", p_running_costs),
    ("projections.html", p_projections),
    ("scenarios.html", p_scenarios),
    ("black-swan.html", p_black_swan),
    ("what-if.html", p_what_if),
    ("process.html", p_process),
    ("briefing-sheet.html", p_briefing_sheet),
    ("suggestions.html", p_suggestions),
    ("questions.html", p_questions),
    ("law-watch.html", p_law_watch),
    ("glossary.html", p_glossary),
    ("sources.html", p_sources),
    ("flagged.html", p_flagged),
    ("methodology.html", p_methodology),
]


def main():
    for name, fn in PAGES:
        html = fn()
        path = os.path.join(OUT, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"wrote {name} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
