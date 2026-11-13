"""Builds the public decision-ad038 pages (static HTML) from model.py and sources.py.

PRIVACY RULE: owner-supplied dollar figures (property values, assessed values, tax bills, rent,
insurance, water, electricity) are NEVER written to public pages or to committed JSON. Public
pages show official figures, official rules, rankings, and percentages or indices relative to the
starting value (2026 = 100, or live-in option = 100). Absolute owner-derived results are written to
owner_outputs.local.json (git-ignored, internal only).

Run from this folder:  python3 build_site.py
Writes decision-ad038/*.html, style.css, site-data.json (public, indices only) and
owner_outputs.local.json (internal, ignored by git).
"""
import html
import json
import os

import model as m
from sources import SOURCES, link

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, ".."))
ACCESSED = "13 Nov 2026"
CSS = "style.css"

NAV = [
    ("index.html", "Home"),
    ("dashboard.html", "Dashboard"),
    ("projections.html", "Projections 2026-2060"),
    ("decision.html", "Decision: live vs rent vs sell"),
    ("black-swans.html", "Black-swan economics"),
    ("law.html", "Law now and proposed"),
    ("inheritance.html", "Inheritance steps and thresholds"),
    ("assumptions.html", "Assumptions"),
    ("questions.html", "Questions and gaps"),
    ("suggestions.html", "Suggestions for review"),
    ("flagged.html", "Flagged for review"),
    ("sources.html", "Sources"),
]


def esc(x):
    return html.escape(str(x))


def usd(x):
    """Official / published dollar figures only (rounded to $10)."""
    if x is None or x == "":
        return '<span class="flag">blank</span>'
    return f"${m.r10(x):,}"


def idx(x, base):
    if x is None or not base:
        return '<span class="flag">blank</span>'
    return f"{100 * x / base:,.1f}"


def pct(x):
    return f"{x * 100:.2f}%"


def srcs(*ids):
    out = []
    for i in ids:
        out.append(link(i) if i in SOURCES else esc(i))
    return " ".join(out)


def page(name, title, body, lede=""):
    nav = "".join(f'<a href="{h}"{" class=on" if h == name else ""}>{esc(t)}</a>' for h, t in NAV)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} | Estate decision analysis</title>
<link rel="stylesheet" href="{CSS}">
</head><body>
<header><div class="brand">Estate decision analysis</div>
<nav>{nav}</nav></header>
<main>
<h1>{esc(title)}</h1>
{('<p class="lede">' + lede + '</p>') if lede else ''}
{body}
<p class="note">Privacy: this site uses placeholders only. No names, addresses, parcel numbers, account numbers, contact details, or owner-supplied dollar figures are published. Official figures are rounded to the nearest $10 unless marked as published unit rates. Accessed {ACCESSED}.</p>
</main>
<footer>Estimates under stated assumptions, not tax, legal or investment advice. Items marked <span class="flag">blank</span> or <span class="flag">unverified</span> are listed on the <a href="flagged.html">Flagged for Review</a> page.</footer>
</body></html>
"""


def table(headers, rows, cls="data"):
    th = "".join(f"<th>{esc(h)}</th>" for h in headers)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="scroll"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


# ------------------------------------------------------------------ model runs
res = m.build_all()
proj = res["projection"]
dec = res["decision"]
sens = res["sensitivity"]
swans = res["black_swans"]
thr = res["thresholds"]
A = res["assumptions"]
DY = [str(t) for t in m.DECISION_YEARS]


def best(row):
    return m.ranking(row)[0][0]


base_row = {T: dec[T]["base|Equities"] for T in DY}
cases = [(T, k, r) for T in DY for k, r in dec[T].items()]
ncases = len(cases)
sell_wins = sum(1 for _, _, r in cases if best(r) == "Sell and reinvest")
live_wins = sum(1 for _, _, r in cases if best(r) == "Live in Property A")
rent_wins = sum(1 for _, _, r in cases if best(r) == "Rent out Property A")
gap_2045 = base_row["2045"]["sell"] / base_row["2045"]["live"] - 1
gap_2045_rent = base_row["2045"]["rent"] / base_row["2045"]["live"] - 1

# ------------------------------------------------------------------ internal (never published)
OWN_INTERNAL = {
    "note": "INTERNAL ONLY. Git-ignored. Contains owner-supplied figures and absolute results. Do not publish.",
    "decision": dec, "sensitivity": sens, "black_swans": {k: {kk: vv for kk, vv in v.items() if kk != 'label'} for k, v in swans.items()},
    "projection": proj,
    "b_context": res["b_context"],
}
with open(os.path.join(HERE, "owner_outputs.local.json"), "w", encoding="utf-8") as fh:
    json.dump(OWN_INTERNAL, fh, indent=1, default=str)

# ================================================================= index
index_body = f"""
<section class="cards">
<a class="card" href="dashboard.html"><b>Dashboard</b><span>Official figures, each with a source</span></a>
<a class="card" href="projections.html"><b>Projections</b><span>Year-by-year indices for value, tax, insurance, water, maintenance</span></a>
<a class="card" href="decision.html"><b>Decision</b><span>Live in the home, rent it out, or sell and reinvest</span></a>
<a class="card" href="black-swans.html"><b>Black-swan economics</b><span>Uneven growth and inflation stress paths</span></a>
<a class="card" href="law.html"><b>Law now and proposed</b><span>Federal, California and local rules</span></a>
<a class="card" href="inheritance.html"><b>Inheritance steps and thresholds</b><span>Process and exclusion projections</span></a>
<a class="card" href="questions.html"><b>Questions and gaps</b><span>What is unknown and how to find it</span></a>
<a class="card" href="suggestions.html"><b>Suggestions</b><span>For owner review before any change</span></a>
<a class="card" href="flagged.html"><b>Flagged for review</b><span>Unverified and blank items</span></a>
<a class="card" href="assumptions.html"><b>Assumptions</b><span>Every input, its tag and its source</span></a>
<a class="card" href="sources.html"><b>Sources</b><span>Every source ID, status and link</span></a>
</section>
<h2>Executive summary</h2>
<ul class="bullets">
<li><b>Scope.</b> Property A is a Santa Clara County home expected to pass to a trust between 2040 and 2050. Property B is a San Francisco County three-unit building already owned. This public site analyses Property A in detail. Property B's figures and tenancy details are held internally and not published (privacy); its open questions are listed on the Questions page.</li>
<li><b>Options.</b> For each possible transfer year (2040, 2045, 2050), the model values three options 10 years later: live in the home, rent it out, or sell at transfer and reinvest the after-tax proceeds. Values are shown relative to the live option (= 100). All values are nominal.</li>
<li><b>Result.</b> In {sell_wins} of {ncases} modelled cases, selling and reinvesting gives the highest value. Living in the home is highest in {live_wins} cases (high growth with the lowest reinvestment return). Renting is highest in {rent_wins} cases.</li>
<li><b>Size of the gap.</b> In the base case for a 2045 transfer with equity-like reinvestment, selling gives about {gap_2045*100:.0f}% more value than living in the home. Renting gives about {gap_2045_rent*100:.0f}% relative to living in the home. These are estimates and depend on the rent and tax-rate assumptions (see Sensitivity).</li>
<li><b>Prop 19.</b> If an heir occupies the home, the taxable value resets to the factored base value, or to market value less the transfer allowance if that is higher. If the home is rented, it is reassessed to market value at transfer. This rule is the key legal input.</li>
<li><b>Federal estate tax.</b> The 2026 basic exclusion is {usd(m.FED_EXCL_2026)} and the 2027 amount is {usd(m.FED_EXCL_2027)} (both read in IRS sources: the estate-tax page and Rev. Proc. 2026-35 section 3.44). California has no estate tax for deaths on or after 1 January 2005 (State Controller). Japan: if any heir is a Japanese tax resident, Japanese inheritance tax can apply to worldwide assets at 10%-55% above a basic deduction of JPY 30,000,000 plus JPY 6,000,000 per statutory heir (NTA No.4102, verified); a US-Japan estate and gift tax treaty is in force. See the Inheritance page.</li>
<li><b>Limits.</b> The rent proxy is a secondary HUD figure and is probably low for this property. The property-tax rate is an assumption. Every such input is tagged ASSUMED or OWNER on the Assumptions page.</li>
</ul>
<h2>Privacy and scope</h2>
<p>Names, addresses, parcel numbers, account numbers, contact details and owner-supplied dollar figures are not published. The public pages show official rules and figures, rankings and percentages. This analysis is not tax, legal or investment advice.</p>
"""
site = {}
site["index.html"] = page("index.html", "Estate decision analysis: Property A and Property B", index_body,
                          lede="A transparent comparison of inheriting a Santa Clara County home through a trust, against a San Francisco County three-unit building already owned. Official figures are rounded to $10 and sourced. Owner figures are not published.")

# ================================================================= dashboard
rows = [
    ["Federal estate tax basic exclusion, 2026", usd(m.FED_EXCL_2026), "Published (IRS)", srcs("S01")],
    ["Federal estate tax basic exclusion, 2027", usd(m.FED_EXCL_2027), "Published (IRS Rev. Proc. 2026-35)", srcs("S02")],
    ["California estate tax (deaths on/after 1 Jan 2005)", "No state estate or inheritance tax", "Published (State Controller)", srcs("S22")],
    ["Prop 19 parent-child transfer amount (16 Feb 2025 to 15 Feb 2027)", usd(m.PROP19_ALLOW_2025), "Published (BOE, shown rounded)", srcs("S03")],
    ["2026-27 Prop 13 inflation factor", "1.02", "Published (BOE)", srcs("S04")],
    ["SF secured property tax rate, FY 2026-27", "1.18162182%", "Searched (SF Treasurer)", srcs("S12")],
    ["Initiative 25-0017 (Prop 19 repeal)", "Failed to qualify", "Ballotpedia (SOS page not reached)", srcs("S21")],
    ["Statewide rent increase cap (Civ. Code 1947.12)", "Lesser of 5% + CPI or 10% per 12 months", "Published (leginfo)", srcs("S07")],
    ["Regional water utility base charge (advice letter)", "$78.64 per month (proposed; approval unconfirmed)", '<span class="flag">unverified approval</span>', srcs("S13")],
    ["SF water schedule W-1B, FY 2026-27 (service charge)", "$13.13 per month + $2.13 per hundred cubic feet (published unit rates)", "Searched (SFPUC)", srcs("S14")],
    ["Sell-and-reinvest vs live in A, 2045 transfer, base case", f"Sell {100 * base_row['2045']['sell'] / base_row['2045']['live']:.1f} vs live 100", "Model output", srcs("MODEL", "S04", "S06")],
    ["Cases where selling and reinvesting ranks highest", f"{sell_wins} of {ncases}", "Model output", srcs("MODEL")],
    ["Property A owner-supplied figures (value, assessment, bills, costs)", "Held internally; not published", '<span class="flag">owner, unverified</span>', srcs("OWNER")],
    ["Property B owner-supplied figures (value, rent, bills, costs)", "Held internally; not published", '<span class="flag">owner, unverified</span>', srcs("OWNER")],
]
dash_body = table(["Item", "Value", "Status", "Source"], rows) + """
<p>Each row cites a source ID; the Sources page gives the link and status. Owner figures are not published and are shown as held internally. Model outputs are rankings or indices, not forecasts.</p>
"""
site["dashboard.html"] = page("dashboard.html", "Dashboard", dash_body, lede="Official figures and status at a glance.")

# ================================================================= projections (indices, 2026 = 100)
prow = []
for r in proj:
    y = r["year"]
    v0 = proj[0]["fmv_base"]
    p0 = proj[0]["tax_no_transfer"]
    prow.append([
        str(y),
        idx(r["fmv_base"], v0), idx(r["fmv_low"], proj[0]["fmv_low"]), idx(r["fmv_high"], proj[0]["fmv_high"]),
        idx(r["prop13_no_transfer"], proj[0]["prop13_no_transfer"]),
        idx(r["tax_no_transfer"], p0),
        usd(r["allowance"]),
        idx(m.OWN_A_INS * (1 + m.A_INS_GROWTH) ** (y - 2026), m.OWN_A_INS),
        idx((1 + m.A_WATER_GROWTH) ** (y - 2026), 1),
        '<span class="flag">blank</span>',
        idx(r["fmv_base"] * m.A_MAINT_PCT, proj[0]["fmv_base"] * m.A_MAINT_PCT),
        srcs("MODEL", "S08", "S04", "S03", "OWNER"),
    ])
projections_body = """
<p>Property A before any transfer, 2026 to 2060. Every money column is an <b>index (2026 = 100)</b> so that owner-supplied absolute values are not published. The allowance column is the official Prop 19 amount (rounded to $10); after February 2027 it is an ASSUMED growth path.</p>
<p><b>Basis:</b> market value follows the model's low, base and high growth paths (ASSUMED). The Prop 13 base value uses the 2026-27 factor of 1.02 (BOE, verified) and an ASSUMED 2% cap after that. Tax, insurance, water and maintenance indices follow the stated assumptions. Electricity is blank because no verified figure exists. The index for insurance and tax reflects growth only, not the owner's starting costs.</p>
""" + table(["Year", "Value index (base)", "Value index (low)", "Value index (high)", "Prop 13 base index (no transfer)", "Property tax index (no transfer)", "Prop 19 allowance (official to Feb 2027; then ASSUMED)", "Insurance index", "Water index", "Electricity", "Maintenance index (0.5% of value)", "Source"], prow)
projections_body += "<h2>After transfer: taxable value at key years</h2>"
trows = []
for T in m.DECISION_YEARS:
    b = dec[str(T)]["base|Equities"]
    trows.append([
        str(T),
        f"{100 * b['taxable_transfer_live'] / b['fmv_transfer']:.1f}%",
        "100.0% (no exclusion)",
        f"{100 * b['tax_year1_live'] / b['tax_year1_rent']:.1f}%",
        usd(m.allowance(int(T))),
        srcs("MODEL", "S03", "S06", "S04"),
    ])
projections_body += table(["Transfer year", "Occupied: taxable value as % of market value", "Rented: taxable value as % of market value", "Year-1 tax if occupied as % of year-1 tax if rented", "Transfer allowance (official to Feb 2027; then ASSUMED)", "Source"], trows)
projections_body += """
<p>Under Prop 19 for an occupied home, the taxable value at transfer is the factored base value if the market value is at or below base plus the transfer allowance. Above that limit, it is the market value minus the allowance. The allowance is $1,044,590 until February 2027 (BOE; published to the dollar, rounded here). After February 2027 the model holds it at an ASSUMED 1.1% a year, derived from the last two BOE adjustments (flagged). If the home is rented, no exclusion applies and the taxable value is the market value at transfer. The claim and occupancy rules are in RTC 63.2 (<a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&amp;sectionNum=63.2" target="_blank" rel="noopener">S06</a>). This is a simplified approximation; confirm with the assessor or a CPA.</p>
"""
site["projections.html"] = page("projections.html", "Projections 2026 to 2060 (indices)", projections_body,
                               lede="Year-by-year indices for value, property tax, insurance, water, electricity and maintenance for Property A, with post-transfer taxable value at key years.")

# ================================================================= decision (live = 100)
SCEN = ["low|Treasuries", "low|Balanced", "low|Equities", "base|Treasuries", "base|Balanced", "base|Equities", "high|Treasuries", "high|Balanced", "high|Equities"]


def trio(r):
    return r["live"], r["rent"], r["sell"]


drows = []
for T in DY:
    for k in SCEN:
        r = dec[T][k]
        L, R, S = trio(r)
        drows.append([T, k.replace("|", ", "), "100.0", idx(R, L), idx(S, L), best(r), srcs("MODEL", "S04", "S06", "S11")])
decision_body = """
<p>Each row values three options 10 years after transfer, with the live option set to 100. <b>Live</b>: the heir occupies the home (Prop 19 applies). <b>Rent</b>: the home is let out and reassessed. <b>Sell</b>: the home is sold at transfer; net proceeds are reinvested at the after-tax return. Growth cases are 1%, 3.5% and 5% a year. Reinvestment after tax is 3.2% (Treasuries), 4.0% (balanced) or 5.0% (equities). All are ASSUMED and anchored to the CBO 10-year Treasury forecast of 4.1% for 2026 (<a href="https://www.cbo.gov/publication/62105" target="_blank" rel="noopener">S11</a>).</p>
""" + table(["Transfer year", "Scenario", "Live in A (= 100)", "Rent out A (index)", "Sell and reinvest (index)", "Highest value", "Source"], drows) + """
<h2>Sensitivity (base case, equities reinvestment; live option = 100)</h2>
"""
srows = []
for T in DY:
    s = sens[T]
    L = s["no_avoided_rent"]["live"]  # placeholder base for live = 100 below
    Lb = dec[T]["base|Equities"]["live"]
    srows.append([T,
                  idx(s["no_avoided_rent"]["live"], Lb),
                  idx(s["rent_x1_5"]["rent"], Lb),
                  idx(s["rent_x1_5"]["live"], Lb),
                  idx(s["tax_1_18"]["live"], Lb),
                  idx(s["tax_1_30"]["live"], Lb),
                  idx(s["treasuries_only"]["live"], Lb),
                  idx(s["treasuries_only"]["sell"], Lb),
                  srcs("MODEL", "S04", "S06")])
decision_body += table(["Transfer year", "Live: no avoided rent (index)", "Rent: rent x1.5 (index)", "Live: rent x1.5 (index)", "Live: tax rate 1.18% (index)", "Live: tax rate 1.30% (index)", "Live: Treasuries (index)", "Sell: Treasuries (index)", "Source"], srows)
decision_body += """
<p>The rent proxy is a 3-bedroom HUD fair-market-rent figure for the Santa Clara County metro area (FY 2026, secondary transcription, unverified). It is not a rent for this house, and it is probably low. The rent x1.5 scenario is shown for that reason. An actual rent opinion is needed before relying on these results.</p>
<h2>Prop 19 exclusion removed (hypothetical)</h2>
""" + f"""<p>If the parent-child exclusion were removed at transfer, an occupied heir would be reassessed to market value. In the base case for 2045, the live option falls to {idx(swans['prop19_repeal']['2045']['live'], base_row['2045']['live'])} (live today = 100), against 100 under current law. The exact text of initiative 25-0017 was not reviewed here, and the initiative did not qualify (<a href="https://ballotpedia.org/California_Changes_to_Tax_Assessment_on_Inherited_Homes_Initiative_(2026)" target="_blank" rel="noopener">S21</a>).</p>
"""
site["decision.html"] = page("decision.html", "Decision: live in A vs rent A vs sell and reinvest", decision_body,
                            lede=f"Selling and reinvesting ranks highest in {sell_wins} of {ncases} cases. Living in the home ranks highest in {live_wins}; renting in {rent_wins}.")

# ================================================================= black swans (live = 100)
bsrows = []
for name, d in swans.items():
    cells = [d["label"]]
    for T in DY:
        r = d[T]
        L, R, S = trio(r)
        cells.append(f"{idx(R, L)} / {idx(S, L)}")
    cells.append(", ".join(sorted({best(d[T]) for T in DY})))
    cells.append(srcs("MODEL", "S08", "S11"))
    bsrows.append(cells)
bs_body = """
<p>This section is separate from the base analysis. It tests regimes that are not forecasts: uneven growth, price shocks, long flat periods and inflation spikes over the 50-year horizon. Each path is an <b>ASSUMED</b> input. The FRED house-price series (<a href="https://fred.stlouisfed.org/series/CASTHPI" target="_blank" rel="noopener">S08</a>, <a href="https://fred.stlouisfed.org/series/ATNHPIUS41940Q" target="_blank" rel="noopener">S09</a>) and the CBO baseline (<a href="https://www.cbo.gov/publication/62105" target="_blank" rel="noopener">S11</a>) are the reference points for judging whether a path is plausible.</p>
<p>Cell format: rent out (index) / sell and reinvest (index), with the live option = 100 at each transfer year, base-case equities reinvestment.</p>
""" + table(["Scenario", "2040 transfer", "2045 transfer", "2050 transfer", "Highest value", "Source"], bsrows) + """
<h2>Narrative (economic history)</h2>
<ul class="bullets">
<li><b>Uneven growth.</b> Prices can fall for several years and then recover. The bust-and-recovery path tests a sharp fall in 2027-2031 followed by a rebound. Check any drawdown against the FRED metro series before relying on it.</li>
<li><b>Inflation shocks.</b> A period of high inflation raises insurance, water and maintenance costs, and can lift nominal sale prices. The stagflation path raises insurance growth to 8% a year to test fixed-cost pressure.</li>
<li><b>Flat decades.</b> A long period with no price growth weakens the sell-and-reinvest case, because reinvestment becomes the only source of return. The flat-decade path tests this.</li>
<li><b>Rates.</b> The rate-shock path lowers after-tax reinvestment returns and favours keeping the home if it is kept.</li>
<li><b>Policy.</b> Prop 19 could change through legislation or a ballot measure. The current repeal initiative did not qualify (S21). No future change is modelled as enacted.</li>
</ul>
"""
site["black-swans.html"] = page("black-swans.html", "Black-swan economic conditions (separate section)", bs_body,
                                lede="Stress paths for uneven growth and inflation over 2026 to 2060. Scenario inputs are assumptions, not forecasts.")

# ================================================================= law
lawrows = [
    ["Federal estate tax basic exclusion", "2026: " + usd(m.FED_EXCL_2026) + " (published)", "In effect", srcs("S01")],
    ["Federal estate tax basic exclusion", "2027: " + usd(m.FED_EXCL_2027) + " (published)", "In effect for deaths in 2027 (Rev. Proc. 2026-35)", srcs("S02")],
    ["Basis of inherited property (step-up)", "Basis = fair market value at date of death", "In effect (IRC 1014(a)(1))", srcs("S19", "S20")],
    ["Long-term capital gain rates", "0%, 15%, 20%; 25% maximum on unrecaptured section 1250 gain", "In effect (2025 tax-year figures)", srcs("S17")],
    ["Home sale exclusion", "$250,000 single; $500,000 joint (2 of last 5 years)", "In effect", srcs("S18")],
    ["California estate tax", "No return for deaths on or after 1 Jan 2005", "In effect", srcs("S22")],
    ["Prop 13 base year and inflation factor", "Factor 1.02 for 2026-27 (2% cap)", "In effect", srcs("S04")],
    ["Prop 19 parent-child exclusion (value cap)", usd(m.PROP19_ALLOW_2025) + " for 16 Feb 2025 to 15 Feb 2027", "In effect; next adjustment Feb 2027", srcs("S03", "S06")],
    ["Prop 19 claim and occupancy rules", "Claim within one year; transferee makes the home a principal residence within one year", "In effect", srcs("S06")],
    ["Initiative 25-0017 (Prop 19 repeal)", "Failed to qualify", "Not on the ballot", srcs("S21")],
    ["Statewide rent cap (Civ. Code 1947.12)", "Lesser of 5% + CPI or 10%; two increases per tenancy", "In effect; exemptions apply", srcs("S07")],
    ["SF secured property tax rate", "1.18162182% (FY 2026-27)", "In effect", srcs("S12")],
    ["Net billing for rooftop solar (NEM 3.0)", "Applies to applications from 15 Apr 2023", "In effect (secondary)", srcs("S15")],
    ["Regional water utility base charge", "$78.64 per month (proposed)", '<span class="flag">pending CPUC approval (unconfirmed)</span>', srcs("S13")],
    ["Japan inheritance tax (if any heir is a Japanese tax resident)", "Basic deduction JPY 30,000,000 + JPY 6,000,000 per statutory heir; excess taxed 10%-55%; return and payment within 10 months. Worldwide scope for resident heirs; US-Japan estate and gift tax treaty in force.", "Verified (NTA No.4102; IRS treaty table)", srcs("S27", "S28")],
]
law_body = table(["Topic", "Current rule or value", "Status", "Source"], lawrows) + """
<h2>Proposed or pending changes</h2>
<p>No enacted change is modelled. The 2027 federal amounts are published (Rev. Proc. 2026-35). Pending items are the next Prop 19 amount adjustment in February 2027 (BOE adjusts every other February 16 by the FHFA California house-price change), the regional water utility rate proposal (CPUC approval unconfirmed), and the scheduled repeal of the statewide rent cap on 1 January 2030 (Civ. Code 1947.12(o)). The Prop 19 repeal initiative did not qualify.</p>
"""
site["law.html"] = page("law.html", "Law now and proposed changes", law_body, lede="Federal, California and local rules that affect the decision, with status.")

# ================================================================= inheritance
steps = [
    ["1", "Confirm the death; gather the death certificate, trust documents and asset list.", "Practical step; no figure.", srcs("S06")],
    ["2", "The successor trustee takes control of the trust assets. Confirm the trust terms with an attorney.", "Legal step; no figure.", srcs("MODEL")],
    ["3", "Obtain a date-of-death appraisal. The date-of-death value sets the federal basis (step-up).", "Basis rule verified.", srcs("S19")],
    ["4", "Check whether the Prop 19 exclusion applies. The heir must claim the homeowners' exemption and make the home a principal residence within one year.", "Verified rule; claim within one year.", srcs("S06", "S03")],
    ["5", "Report the change in ownership to the county assessor: within 150 days of the date of death if there is no probate; at the same time the inventory and appraisal is filed if the estate is probated.", "Verified (BOE change-in-ownership FAQ; R&T 480)", srcs("S26")],
    ["6", "If the estate exceeds the federal basic exclusion, file a federal estate tax return. The 2026 exclusion is $15,000,000.", "Verified (2026).", srcs("S01")],
    ["7", "No California estate or inheritance tax return is required for deaths on or after 1 Jan 2005.", "Searched.", srcs("S22")],
    ["8", "Decide whether to keep, rent or sell. Sales carry costs and possible capital gain; the step-up limits the gain.", "Model step.", srcs("MODEL", "S17")],
]
inh_body = table(["Step", "What to do", "Status", "Source"], steps) + f"""
<h2>Inheritance tax thresholds and projections</h2>
<p>The federal estate tax applies only to estates above the basic exclusion. The projection indexes the published 2027 amount ({usd(m.FED_EXCL_2027)}, Rev. Proc. 2026-35) at the CBO long-run inflation rate of 2.3% a year (<a href="https://www.cbo.gov/publication/62105" target="_blank" rel="noopener">S11</a>). It is illustrative only.</p>
""" + table(["Year", "Federal exclusion (projected, indexed 2.3%)", "Status", "Source"], [
    [y, usd(thr["fed_projection_index_2_3"][int(y)]), "projection on published 2027 amount", srcs("S02", "S11", "MODEL")] for y in DY
]) + """
<h2>Japan inheritance tax thresholds (verified)</h2>
<p>Whether Japan taxes this inheritance depends on the tax residence of each heir at the date of death, not on where the house sits. The figures below were read in the National Tax Agency's own page (Tax Answer No.4102) on 13 November 2026. Amounts in JPY are exact statutory figures.</p>
<table><thead><tr><th>Item</th><th>Rule</th><th>Status</th><th>Source</th></tr></thead><tbody>
<tr><td>Basic deduction</td><td>JPY 30,000,000 + JPY 6,000,000 x number of statutory heirs (adopted children counted with limits)</td><td>Verified (NTA No.4102)</td><td>S27</td></tr>
<tr><td>Rate on the excess (taxable estate)</td><td>10% to 55% progressive (8 brackets)</td><td>Verified (NTA)</td><td>S27</td></tr>
<tr><td>Return and payment deadline</td><td>Within 10 months of the day the heir learns of the death</td><td>Verified (NTA No.4102)</td><td>S27</td></tr>
<tr><td>Scope for an heir resident in Japan</td><td>All property acquired, wherever situated (US real property included)</td><td>Verified (NTA No.4102 scope table)</td><td>S27</td></tr>
<tr><td>Scope for an heir neither resident in Japan nor a Japanese national</td><td>Property situated in Japan only</td><td>Verified (NTA No.4102 scope table)</td><td>S27</td></tr>
<tr><td>Double taxation relief</td><td>A US-Japan estate and gift tax treaty is in force; the United States may tax US real property; credits relieve double taxation</td><td>Verified that the treaty is listed (IRS treaty table); treaty text not read</td><td>S28</td></tr>
</tbody></table>
<p>Example (statutory arithmetic, not a forecast): a single heir with no other statutory heirs gets a JPY 36,000,000 basic deduction. If any heir is a Japanese tax resident, get cross-border advice before choosing between occupying, renting and selling; the Japanese tax can exceed the US estate tax because the US exemption is high and Japan's basic deduction is comparatively low.</p>
"""
site["inheritance.html"] = page("inheritance.html", "Inheritance steps and tax thresholds", inh_body, lede="Step-by-step process after a death, and the thresholds that matter for this estate.")

# ================================================================= assumptions
arows = [
    ["Property A market value and assessed value (2026)", "Held internally; not published", "OWNER (consistent with BOE factor chain)", srcs("OWNER", "S04")],
    ["Property A tax rate (effective)", f"{pct(A['A_EFF_TAX_RATE'])} (sensitivity {pct(A['A_TAX_RATE_ALT'])} to 1.30%)", "ASSUMED (derived from owner data; secondary range)", srcs("MODEL", "S24")],
    ["Property A insurance, water, electricity", "Held internally; electricity blank", "OWNER; electricity unverified", srcs("OWNER")],
    ["Insurance growth", pct(A["A_INS_GROWTH"]), "ASSUMED", srcs("MODEL")],
    ["Water growth", pct(A["A_WATER_GROWTH"]), "ASSUMED", srcs("MODEL")],
    ["Maintenance (share of value per year)", pct(A["A_MAINT_PCT"]), "ASSUMED", srcs("MODEL")],
    ["Rent proxy for Property A (per month, 2026)", usd(A["A_RENT_2026"]), '<span class="flag">ASSUMED from HUD FMR (secondary); probably low</span>', srcs("S16", "MODEL")],
    ["Rent growth", pct(A["A_RENT_GROWTH"]), "ASSUMED", srcs("MODEL")],
    ["Vacancy allowance", pct(A["A_VACANCY"]), "ASSUMED", srcs("MODEL")],
    ["Management fee", pct(A["A_MGMT"]), "ASSUMED", srcs("MODEL")],
    ["Selling costs", pct(A["A_SELL_COST"]), "ASSUMED", srcs("MODEL")],
    ["Ordinary income rate (federal + California marginal)", pct(A["A_ORDINARY_RATE"]), "ASSUMED", srcs("MODEL")],
    ["Growth cases (low / base / high, per year)", "1.0% / 3.5% / 5.0%", "ASSUMED", srcs("MODEL", "S11")],
    ["Reinvestment after tax (Treasuries / balanced / equities)", "3.2% / 4.0% / 5.0%", "ASSUMED, anchored to CBO 10-year yield 4.1% (2026)", srcs("MODEL", "S11")],
    ["Prop 13 cap after 2026-27", "2% a year", "Statutory cap (BOE)", srcs("S04")],
    ["Prop 19 allowance growth after Feb 2027", "1.1% a year", "ASSUMED (from BOE adjustments)", srcs("S03", "MODEL")],
    ["Property B values, rent, water, electricity, insurance, tax", "Held internally; not published", "OWNER", srcs("OWNER")],
]
assump_body = table(["Input", "Value", "Tag", "Source"], arows) + """
<p>Tags: <b>OWNER</b> = supplied by the owner and not checked against an official source; owner figures are held internally and not published. <b>ASSUMED</b> = modelling choice with no official source. Official figures are linked in the Source column. The model code is <a href="https://github.com/wingbangboozle1-lang/Tino5/blob/main/decision-ad038/_src/model.py" target="_blank" rel="noopener">linked here</a> so the assumptions can be changed.</p>
"""
site["assumptions.html"] = page("assumptions.html", "Assumptions and inputs", assump_body, lede="Every input, its value and how it is tagged.")

# ================================================================= questions
qrows = [
    ["Is Japanese inheritance tax relevant (any owner or heir a Japanese tax resident)?", "Thresholds are now verified (JPY 30,000,000 + JPY 6,000,000 per statutory heir; 10%-55%); what remains unknown is each heir's tax residence at the date of death", "Confirm tax residence of each heir; cross-border tax adviser; NTA No.4102 and the US-Japan estate and gift tax treaty (both linked)", srcs("S27", "S28")],
    ["Confirmed market value of Property A and Property B", "Appraisals (current and at date of death)", "Licensed appraiser; county assessor records", srcs("OWNER")],
    ["Current assessed value and tax bill for each property", "Tax bills, assessor record", "County assessor and tax collector", srcs("S12", "S04")],
    ["Exact Property A tax rate (tax rate area)", "Tax bill line items", "Santa Clara County tax rate book", srcs("S24")],
    ["Whether the Prop 19 repeal initiative is officially closed", "Secretary of State certified list", "California Secretary of State status pages", srcs("S21")],
    ["2027 federal exclusion amount (primary)", "IRS news release and Rev. Proc.", "irs.gov newsroom; Rev. Proc. 2026-35", srcs("S02")],
    ["Which water utility serves Property A, and its approved rate", "Water bill; utility tariff", "Utility website; CPUC advice-letter docket", srcs("S13")],
    ["Actual rent for Property A (market)", "Rent comparables", "Local property manager; listings (non-official); HUD FMR as a check", srcs("S16")],
    ["Rent-control status for Property B units (built before 13 June 1979?)", "Certificate of occupancy date", "Building permit records; SF Rent Board", srcs("S25")],
    ["Actual electricity cost for each property", "Bills (12 months)", "Utility bills", srcs("MODEL")],
    ["Whether a trust is in place and its terms", "Trust document", "Estate attorney (California)", srcs("MODEL")],
    ["Capital gains and income position of heirs", "Tax returns", "CPA", srcs("S17")],
    ["Property B analysis (live / rent / sell for the building)", "Owner figures and tenancy records (held internally)", "Owner decision whether to publish a private version", srcs("OWNER")],
]
q_body = table(["Question or gap", "Information needed", "How to find it", "Source"], qrows) + """
<p>Each item is open. Nothing is inferred to fill a gap. Values stay blank until confirmed.</p>
"""
site["questions.html"] = page("questions.html", "Questions and information gaps", q_body, lede="What is unknown, what is needed, and where to get it.")

# ================================================================= suggestions
sug = [
    ["Get two independent appraisals (current value; value at a future transfer date) and a rent opinion for Property A.", "Replaces OWNER and ASSUMED inputs with market evidence.", srcs("MODEL")],
    ["Confirm the Prop 19 position on the Secretary of State status page before any decision that depends on it.", "Removes the largest legal uncertainty.", srcs("S21")],
    ["Ask a California estate attorney to review the trust and the Prop 19 claim timeline.", "The one-year claim and occupancy rules are strict.", srcs("S06")],
    ["Ask a CPA to model the step-up and sale tax for each option, including the 3.8% net investment income tax.", "The model uses simplified tax treatment.", srcs("S17", "S19")],
    ["If any heir has Japanese tax residence, get Japanese tax advice before deciding; the verified Japan rows on the Inheritance page show why it can dominate the US tax.", "Thresholds verified; heir residence unknown.", srcs("S27", "S28")],
    ["Decide with the owner whether a private, non-public version of the Property B analysis is wanted.", "Keeps owner figures off the public site.", srcs("OWNER")],
    ["Review the sensitivity table, especially rent x1.5, before deciding.", "Rent is the largest uncertainty in the live-vs-sell comparison.", srcs("S16")],
]
sug_body = table(["Suggestion (for owner review; no change is made automatically)", "Why", "Source"], sug) + """
<p>These suggestions are for review only. They are not decisions.</p>
"""
site["suggestions.html"] = page("suggestions.html", "Suggestions for review", sug_body, lede="Actions the owner may consider before any change is made.")

# ================================================================= flagged
flag_rows = [
    ["2027 federal estate tax exclusion", "Resolved 13 Nov 2026: read in Rev. Proc. 2026-35 section 3.44 ($15,480,000) and section 3.46 (annual gift exclusion $20,000).", srcs("S02")],
    ["Prop 19 repeal initiative 25-0017 status", "Ballotpedia reports failure (May 2026); Secretary of State page not reached; a secondary source gives a different date", srcs("S21")],
    ["Santa Clara County composite tax rate", "Official tax rate book not reached; the effective rate is an assumption; a secondary composite is unverified", srcs("S24")],
    ["Property A electricity cost", "No verified figure; blank", srcs("MODEL")],
    ["Rent proxy for Property A", "HUD FMR (secondary); probably low for this property; rent x1.5 sensitivity shown", srcs("S16")],
    ["Regional water utility base charge ($78.64 per month)", "Advice letter (proposed); approved rate unconfirmed", srcs("S13")],
    ["SF Rent Ordinance coverage for Property B units", "Text not reached; depends on the certificate of occupancy date", srcs("S25")],
    ["Prop 19 transfer amount after February 2027", "Next adjustment not yet published; growth after 2027 is ASSUMED", srcs("S03")],
    ["Japan inheritance tax thresholds", "Resolved 13 Nov 2026: verified against NTA No.4102 (basic deduction, rates, deadline, scope). Heir tax residence remains an owner question.", srcs("S27", "S28")],
    ["Change-in-ownership reporting deadline", "Not confirmed", srcs("S26")],
    ["Owner-supplied figures (Property A and B)", "Not verified against official sources and not published. Consistency with the BOE factor chain was checked internally", srcs("OWNER", "S04")],
    ["Property B analysis", "Held internally; not published on this site", srcs("OWNER")],
    ["CA homeowners insurance benchmark", "Sources conflict by method; not used", srcs("S23")],
    ["Prop 19 model simplification", "The value-cap rule is simplified. An assessor or CPA should confirm", srcs("S06", "S03")],
    ["Public-site privacy boundary", "Owner figures are kept off the public site as a privacy decision. Other published desks in this repository may show owner-derived amounts (see their own pages). Owner decision needed", srcs("OWNER")],
]
flag_body = table(["Item", "Why it is flagged", "Source"], flag_rows) + """
<p>Flagged items do not block publication. They appear here so the owner can check them.</p>
"""
site["flagged.html"] = page("flagged.html", "Flagged for review", flag_body, lede="Unverified, blank or contested items.")

# ================================================================= sources
src_rows = []
for sid, s in SOURCES.items():
    if sid == "OWNER":
        continue
    url = s["url"] or ""
    link_html = f'<a href="{url}" target="_blank" rel="noopener">{esc(url)}</a>' if url else "none"
    src_rows.append([sid, esc(s["title"]), esc(s["publisher"]), link_html, s["status"]])
sources_body = table(["ID", "Title", "Publisher", "Link", "Status"], src_rows) + """
<p><b>Status key.</b> FETCHED = opened and read on 13 Nov 2026. SEARCHED = official text seen in a search result; full page not opened. SECONDARY = secondary report only. NONE = no official source reached; the value is blank. MODEL = this project's own model code, not an official source. OWNER = owner-supplied figure, not verified, not published.</p>
"""
site["sources.html"] = page("sources.html", "Sources", sources_body, lede="Every source used, its status and its link.")

# ================================================================= write
for name, text in site.items():
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(text)

css = """
:root{--ink:#1d2330;--mut:#5b6474;--line:#dfe3ea;--bg:#f7f8fa;--acc:#1f4e79;--flag:#8a4b00;--flagbg:#fff4e0}
*{box-sizing:border-box}
body{margin:0;font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);background:var(--bg)}
header{background:#fff;border-bottom:1px solid var(--line);padding:12px 20px;position:sticky;top:0;z-index:1}
.brand{font-weight:700;color:var(--acc);margin-bottom:6px}
nav a{display:inline-block;margin:2px 8px 2px 0;padding:3px 8px;border-radius:4px;color:var(--acc);text-decoration:none;font-size:13px}
nav a.on,nav a:hover{background:var(--acc);color:#fff}
main{max-width:1100px;margin:0 auto;padding:20px}
h1{font-size:24px;margin:8px 0}
h2{font-size:18px;margin-top:28px;color:var(--acc)}
.lede{color:var(--mut);font-size:16px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px;margin:16px 0}
.card{background:#fff;border:1px solid var(--line);border-radius:8px;padding:14px;color:var(--ink);text-decoration:none;display:flex;flex-direction:column;gap:4px}
.card:hover{border-color:var(--acc)}
.card b{color:var(--acc)}
.card span{color:var(--mut);font-size:13px}
.scroll{overflow-x:auto;background:#fff;border:1px solid var(--line);border-radius:8px;margin:10px 0}
table.data{border-collapse:collapse;width:100%;font-size:13px}
table.data th,table.data td{padding:7px 9px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
table.data th{background:#eef2f7;font-weight:600}
table.data tbody tr:nth-child(even){background:#fafbfd}
.flag{color:var(--flag);background:var(--flagbg);padding:0 4px;border-radius:3px;font-size:12px}
.note,footer{color:var(--mut);font-size:12px;margin-top:24px}
.bullets li{margin:6px 0}
a{color:var(--acc)}
"""
with open(os.path.join(OUT, CSS), "w", encoding="utf-8") as fh:
    fh.write(css)

# public JSON: indices and official values only (no owner-derived absolutes)
pub = {
    "generated": ACCESSED,
    "note": "Public data: indices relative to the live option (=100) or to 2026 (=100); no owner-supplied dollar figures.",
    "decision_index": {T: {k: {"live": 100.0, "rent": round(100 * dec[T][k]["rent"] / dec[T][k]["live"], 1),
                               "sell": round(100 * dec[T][k]["sell"] / dec[T][k]["live"], 1),
                               "highest": best(dec[T][k])} for k in dec[T]} for T in DY},
    "federal_exclusion": {"2026": m.FED_EXCL_2026, "2027": m.FED_EXCL_2027},
    "prop19_allowance_to_2027_02_15": m.PROP19_ALLOW_2025,
}
with open(os.path.join(OUT, "site-data.json"), "w", encoding="utf-8") as fh:
    json.dump(pub, fh, indent=1)
print("pages:", len(site), "dashboard rows:", len(rows), "sell wins:", sell_wins, "of", ncases)
