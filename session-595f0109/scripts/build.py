"""Build the session-595f0109 privacy-safe dashboard.

Generates static HTML from verified official sources retrieved 2026-11-11.
Property-specific values are intentionally withheld (blank cells).
Fictional illustrations use explicit formulas; display rounded to $10.
No personal identifiers, no city names, no ZIP codes, no owner figures.
"""
from pathlib import Path
from html import escape as e

ROOT = Path(__file__).resolve().parents[1]

S = {
    "estate": ("IRS · Estate tax", "https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax"),
    "new": ("IRS · Enacted exclusion (PL 119-21)", "https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax"),
    "faq": ("IRS · Estate tax FAQs", "https://www.irs.gov/businesses/small-businesses-self-employed/frequently-asked-questions-on-estate-taxes"),
    "f706": ("IRS · Form 706 instructions", "https://www.irs.gov/instructions/i706"),
    "basis": ("IRS · Inherited basis", "https://www.irs.gov/faqs/interest-dividends-other-types-of-income/gifts-inheritances/gifts-inheritances"),
    "t703": ("IRS · Topic 703 (basis)", "https://www.irs.gov/taxtopics/tc703"),
    "p551": ("IRS · Publication 551 (basis)", "https://www.irs.gov/publications/p551"),
    "p527": ("IRS · Publication 527 (rental)", "https://www.irs.gov/publications/p527"),
    "p523": ("IRS · Publication 523 (home sale)", "https://www.irs.gov/publications/p523"),
    "boe19": ("BOE · Proposition 19", "https://boe.ca.gov/prop19/"),
    "pub801": ("BOE · Proposition 19 fact sheet (Pub 801)", "https://www.boe.ca.gov/pdf/pub801.pdf"),
    "pub29": ("BOE · Property tax overview (Pub 29)", "https://www.boe.ca.gov/proptaxes/pdf/pub29.pdf"),
    "sco": ("State Controller · Estate tax", "https://www.sco.ca.gov/ardtax_estate_tax.html"),
    "ftb": ("FTB · Gifts and inheritance", "https://www.ftb.ca.gov/file/personal/income-types/gifts-and-inheritance.html"),
    "cdi": ("CDI · Residential insurance", "https://www.insurance.ca.gov/01-consumers/105-type/5-residential/index.cfm"),
    "cdis": ("CDI · Sustainable Insurance Strategy", "https://www.insurance.ca.gov/01-consumers/180-climate-change/sustainable-insurance-strategy.cfm"),
    "cpi": ("BLS · December 2022 CPI", "https://www.bls.gov/news.release/archives/cpi_01122023.htm"),
    "blsdata": ("BLS · CPI databases", "https://www.bls.gov/cpi/data.htm"),
    "court": ("California Courts · Probate guide", "https://selfhelp.courts.ca.gov/probate"),
    "fed": ("Federal Reserve · Open market operations", "https://www.federalreserve.gov/monetarypolicy/openmarket.htm"),
    "sep": ("Federal Reserve · SEP Sep 2025", "https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20250917.htm"),
    "hpi": ("FHFA · House Price Index", "https://www.fhfa.gov/data/hpi"),
    "uad": ("FHFA · Appraisal dataset (UAD PUF)", "https://www.fhfa.gov/data/uad/puf"),
    "cpuc": ("CPUC · Electric rates", "https://www.cpuc.ca.gov/industries-and-topics/electrical-energy/electric-rates"),
    "cityutil": ("City utility · Water/power/sewer", "https://www.sfpuc.gov/"),
    "hr1": ("Congress.gov · H.R.1 (PL 119-21)", "https://www.congress.gov/bill/119th-congress/house-bill/1"),
}

NAV = [
    ("index", "Overview"),
    ("decision", "Decision framework"),
    ("tax", "Tax rules"),
    ("costs", "Operating costs"),
    ("projections", "50-year illustrations"),
    ("stress", "Black swans"),
    ("process", "Inheritance steps"),
    ("law-watch", "Law watch"),
    ("flagged", "Flagged for Review"),
    ("sources", "Sources & method"),
]

def link(k):
    a, b = S[k]
    return f'<a href="{b}">{a}</a>'

def m(x):
    """Round to nearest $10 and format."""
    v = round(float(x) / 10) * 10
    return f"${v:,.0f}"

def table(head, rows_html):
    th = "".join(f'<th scope="col">{e(x)}</th>' for x in head)
    return f'<div class="scroll"><table><thead><tr>{th}</tr></thead><tbody>{rows_html}</tbody></table></div>'

def rows(items):
    """items: (topic, finding, status, source_key)"""
    body = ""
    for a, b, c, d in items:
        body += f"<tr><td>{e(a)}</td><td>{e(b)}</td><td>{e(c)}</td><td>{link(d)}</td></tr>"
    return table(["Topic", "Finding / action", "Status", "Official source"], body)

def page(name, title, body):
    parts = []
    for n, t in NAV:
        cur = 'aria-current="page" ' if name == n else ""
        parts.append(f'<a {cur}href="{n}.html">{t}</a>')
    nav = "".join(parts)
    html = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="robots" content="noindex,nofollow">'
        '<meta name="referrer" content="no-referrer">'
        f"<title>{e(title)} · Inheritance planning</title>"
        '<link rel="stylesheet" href="assets/style.css"></head><body>'
        '<header class="top"><a class="brand" href="index.html">Estate decision desk</a>'
        '<span class="tag">PUBLIC · ANONYMIZED · PROPERTY A / PROPERTY B</span></header>'
        f'<div class="layout"><nav class="side" aria-label="Main">{nav}</nav><main>'
        '<div class="eyebrow">RESEARCH REVIEW · 11 NOVEMBER 2026 · SESSION 595F0109</div>'
        f"<h1>{e(title)}</h1>{body}"
        "<footer>Educational analysis, not individualized legal, tax, insurance or investment advice. "
        "Recheck rules at transfer. No personal identifiers or owner-supplied financial histories are included in this artifact. "
        "All money rounded to the nearest $10; statutory figures shown rounded per project rule.</footer>"
        "</main></div></body></html>"
    )
    (ROOT / f"{name}.html").write_text(html, encoding="utf-8")

# ---------- fictional illustration math ----------
def proj_rows():
    out = ""
    for yr in range(2026, 2077):
        n = yr - 2026
        v = 1000000 * (1.03 ** n)
        real = v / (1.025 ** n)
        a = 200000 * (1.02 ** n)
        t = a * 0.01
        b = 15000 * (1.025 ** n)
        out += (
            f"<tr><td>{yr}</td><td>{m(v)}</td><td>{m(real)}</td><td>{m(a)}</td>"
            f"<td>{m(t)}</td><td>{m(b)}</td>"
            f'<td>Illustration only · {link("boe19")} / {link("cpi")}</td></tr>'
        )
    return out

# ---------- index ----------
page("index", "A decision plan, not a prediction",
    '<p class="lead">One home is expected through a future trust transfer (Property A). '
    "Another building is already owned (Property B). Keep those decisions separate.</p>"
    '<section class="notice"><strong>Privacy comes first.</strong> Property A and Property B are placeholders. '
    "Actual valuations, rents, bills, dates of family events, locations and assessment histories are intentionally withheld. "
    "Rounding alone cannot prevent identification, so property-specific numbers are left blank and flagged rather than shown rounded.</section>"
    '<div class="kpis">'
    '<article><div class="k">Federal exclusion (2026)</div><div class="v">$15,000,000</div>'
    '<div class="d">Per individual, not per beneficiary. Enacted by PL 119-21.</div>'
    f'<div class="d">{link("new")}</div></article>'
    '<article><div class="k">Family-home allowance</div><div class="v">$1,044,590</div>'
    '<div class="d">Current biennial allowance, rounded to $10 per project rule. Future allowance unknown.</div>'
    f'<div class="d">{link("pub801")}</div></article>'
    '<article><div class="k">Statewide average premium</div><div class="v">$1,570</div>'
    '<div class="d">Average only, rounded to $10 per project rule. Not a quote for either property.</div>'
    f'<div class="d">{link("cdis")}</div></article>'
    '<article><div class="k">Property-tax base</div><div class="v">1% + bonds</div>'
    '<div class="d">Base levy plus voter-approved bonded debt; growth generally capped at 2%.</div>'
    f'<div class="d">{link("pub29")}</div></article>'
    "</div>"
    '<div class="cards">'
    "<article><h2>Property A</h2><p>Future inherited home. Compare occupancy, rental and sale only after checking trust terms and transfer-year law.</p></article>"
    "<article><h2>Property B</h2><p>Already owned, with existing rental activity. No new basis adjustment or reassessment is assumed from inheriting A.</p></article>"
    "<article><h2>Current decision</h2><p>Preserve flexibility. Do not make an irreversible sale or relocation decision based on a smooth long-run forecast.</p></article>"
    "</div>"
    "<h2>Executive summary</h2>"
    + rows([
        ("Working strategy", "Use staying in B and selling A after transfer as the comparison baseline, not an established winner. Confirm net proceeds, tax basis and housing preferences first.", "Conditional analysis", "basis"),
        ("Live in A", "Consider only if genuine principal-residence occupancy is desired and the family-home exclusion qualifies. Savings may be limited by the value cap.", "Conditional analysis", "boe19"),
        ("Rent A", "Require market-supported rent to cover reassessed taxes, vacancy, repairs, insurance, management and tax. No verified rent estimate is available.", "Needs review", "cdi"),
        ("Estate exposure", "Measure the transferor's entire includible estate and lifetime taxable gifts, not just the beneficiary's cash inheritance.", "Verified rule; private amount withheld", "estate"),
        ("Main limitation", "No defensible personalized after-tax ranking exists without verified trust, basis, debt, rental and expense data. This site does not invent them.", "Unresolved", "t703"),
    ])
    + '<p><a class="button" href="decision.html">Explore the decision framework →</a></p>'
    "<h2>How to read this site</h2>"
    + rows([
        ("Verified", "General rule checked in retrieved official text. Does not verify any private property figure.", "Label definition", "estate"),
        ("Illustration only", "Fictional worked example with shown formulas. Links give legal/economic context, not endorsement of the chosen rates.", "Label definition", "cpi"),
        ("Unverified / blank", "Value cannot be confirmed from an official source. Cell stays blank and the item is listed on Flagged for Review.", "Label definition", "boe19"),
    ])
)

# ---------- decision ----------
page("decision", "Compare the incremental decision",
    '<p class="lead">Hold the already-owned property constant unless a separate, fully costed decision changes it. '
    "Existing rental income must not disappear simply because occupancy moves.</p>"
    + rows([
        ("Occupy A", "Net benefit = housing value enjoyed + eligible tax savings − incremental carrying costs − investment opportunity cost. Do not count market rent as cash income from an occupied house.", "Framework, not forecast", "boe19"),
        ("Rent A", "NOI = collected rent − vacancy − management − taxes − insurance − utilities − maintenance − capital reserve. Then subtract debt service and income tax to get spendable cash.", "Framework; inputs unverified", "p527"),
        ("Sell A", "Investable proceeds = sale price − selling costs − debt payoff − applicable gain tax − estate settlement allocation. Inherited basis is generally date-of-death fair market value, subject to exceptions.", "Conditional framework", "basis"),
        ("B treatment", "Retain existing leases and costs in all three scenarios. Extra rent from a currently occupied space is not automatic; legality, condition and tenancy terms require review.", "User context; not independently verified", "court"),
        ("Comparable endpoints", "Compare total after-tax liquidation wealth at the same date, including home selling costs, portfolio tax, cumulative cash flows and equivalent housing consumption.", "Analytical method", "t703"),
        ("Decision gate", "Prefer a sale only if its after-tax, risk-adjusted outcome exceeds the alternatives and liquidity/diversification goals support it. Prefer rental only with resilient net cash flow.", "Conditional recommendation", "basis"),
    ])
    + "<h2>Illustrative break-even, not a property estimate</h2>"
    + rows([
        ("Fictional capital", "Assume net sale proceeds $1,000,000 and a 4% net annual alternative return: $40,000 annual opportunity cost.", "Assumption / derived; not officially endorsed", "basis"),
        ("Fictional rental hurdle", "With $30,000 annual operating costs, $10,000 capital reserve, 5% vacancy and no debt or income tax: break-even scheduled rent = ($40,000 + $30,000 + $10,000) / 0.95 = $84,210 per year.", "Assumption / derived; pre-income-tax only", "t703"),
        ("Interpretation", "This hurdle excludes appreciation and terminal gain taxes. It is not a sufficient investment ranking and does not establish a rent estimate.", "Limitation", "t703"),
    ])
    + '<div class="calc"><h3>Try the fictional break-even (illustration only)</h3>'
      '<p class="small">Adjust the fictional inputs. Nothing here is a quote or a forecast for either property.</p>'
      '<label for="proceeds">Fictional net sale proceeds ($)</label>'
      '<input id="proceeds" type="number" value="1000000" min="0" step="10000">'
      '<label for="ret">Fictional net annual return (%)</label>'
      '<input id="ret" type="number" value="4" min="0" step="0.5">'
      '<label for="costs">Fictional annual operating costs ($)</label>'
      '<input id="costs" type="number" value="30000" min="0" step="1000">'
      '<label for="reserve">Fictional capital reserve ($)</label>'
      '<input id="reserve" type="number" value="10000" min="0" step="1000">'
      '<label for="vac">Fictional vacancy (%)</label>'
      '<input id="vac" type="number" value="5" min="0" max="50" step="1">'
      '<output id="out">Break-even scheduled rent: $84,210 per year</output>'
      '<p class="small">Formula: (proceeds × return + costs + reserve) / (1 − vacancy). Pre-income-tax; excludes appreciation and terminal taxes.</p></div>'
      '<script>(function(){function f(){var p=parseFloat(document.getElementById("proceeds").value)||0;'
      'var r=(parseFloat(document.getElementById("ret").value)||0)/100;'
      'var c=parseFloat(document.getElementById("costs").value)||0;'
      'var s=parseFloat(document.getElementById("reserve").value)||0;'
      'var v=(parseFloat(document.getElementById("vac").value)||0)/100;'
      'var rent=(p*r+c+s)/(1-v);rent=Math.round(rent/10)*10;'
      'document.getElementById("out").textContent="Break-even scheduled rent: $"+rent.toLocaleString("en-US")+" per year";}'
      '["proceeds","ret","costs","reserve","vac"].forEach(function(id){document.getElementById(id).addEventListener("input",f);});f();})();</script>'
)

# ---------- tax ----------
page("tax", "Separate three different tax systems",
    rows([
        ("Federal estate exclusion", "2026 basic exclusion: $15,000,000 per individual. This is not a per-beneficiary allowance. Filing tests include adjusted taxable gifts; deductions affect tax due.", "Verified from IRS, retrieved 2026-11-11", "new"),
        ("Filing threshold", "Form 706 is required when the gross estate plus adjusted taxable gifts exceeds the filing threshold for the year of death ($15,000,000 for 2026). Portability election also requires a timely return.", "Verified general rule", "faq"),
        ("Headroom", "Simplified headroom = applicable exclusion + valid portable exclusion − taxable estate − adjusted taxable gifts. Actual amount: withheld / unverified. No flat penalty is assumed on an inheritance.", "Framework only", "estate"),
        ("Trust assets", "Trust assets may be included in the gross estate. A trust label alone does not establish estate-tax exemption or inherited basis.", "Verified general rule; trust-specific result unknown", "estate"),
        ("Inherited income-tax basis", "Generally date-of-death fair market value, or elected alternate valuation when applicable. A later sale above adjusted basis may create taxable gain.", "Verified general rule, exceptions apply", "basis"),
        ("Already-owned B", "Do not reset its income-tax basis merely because A is inherited. Track improvements and allowed/allowable depreciation separately.", "Application of basis principles", "t703"),
        ("California income tax", "FTB says not to include the received gift or inheritance in income; subsequent interest, dividends, rental income or sale gains can be taxable. This does not certify a separate estate-tax rule.", "Verified general rule", "ftb"),
        ("Prop 13", "Base tax is 1% plus voter-approved bonded debt; assessed-value growth is generally limited to no more than 2% except ownership change or new construction. 2% is not a guaranteed annual bill increase.", "Verified general rule", "pub29"),
        ("Prop 19 eligibility", "Family-home exclusion requires qualifying relationship and principal residence of transferor and transferee. Other investment real estate does not receive this exclusion.", "Verified general rule", "boe19"),
        ("Prop 19 timing", "File homeowners exemption within one year of transfer; exclusion claim within three years or before third-party transfer. Check detailed assessor instructions.", "Verified summary", "pub801"),
        ("Prop 19 value limit", "Current taxable value plus a biennially adjusted statutory allowance limits exclusion. Trust transfer does not automatically preserve the old assessment.", "Verified general rule; future allowance unknown", "boe19"),
        ("California estate / inheritance tax", "Controller states no California estate return for deaths on or after January 1, 2005; inheritance tax collection applies to deaths before June 8, 1982. Do not confuse later income tax with tax on receipt.", "Verified current state guidance", "sco"),
        ("Local transfer costs", "Local sale/recording/transfer-tax treatment is not certified in this release; no unverified local threshold or sale tax is filled in.", "Needs review", "pub29"),
        ("Future laws", "The 2040–2050 exclusion, tax brackets and Prop 19 allowance are unknown. Recheck enactments at transfer, not just today's rules.", "Unknown future law", "new"),
    ])
)

# ---------- costs ----------
page("costs", "Budget costs without inventing quotes",
    '<p class="lead">A statewide average is not an insurance quote. Actual values remain blank until supported; '
    "source links explain the relevant rule or verification route, not proof of a private bill.</p>"
    + table(["Cost", "A verified annual amount", "B verified annual amount", "Finding / verification route", "Official source"],
        "<tr><td>Insurance</td><td></td><td></td>"
        "<td>Unverified. Obtain occupancy-correct homeowner vs landlord/multiunit terms, replacement-cost valuation, deductibles, liability and loss-of-rent coverage. Do not assume equal premiums.</td>"
        f"<td>{link('cdi')}</td></tr>"
        "<tr><td>Water / sewer</td><td></td><td></td>"
        "<td>Unverified. Provider, meter, consumption, sewer charges and fixed charges must be established; owner estimates are not public evidence.</td>"
        f"<td>{link('cityutil')}</td></tr>"
        "<tr><td>Electricity / solar</td><td></td><td></td>"
        "<td>Unverified. Annual true-up, tariff, export compensation, equipment age and transfer terms are unknown. Do not capitalize a perpetual solar credit.</td>"
        f"<td>{link('cpuc')}</td></tr>"
        "<tr><td>Repairs / capital expenditure</td><td></td><td></td>"
        "<td>Unverified. Inspect roof, solar inverter, plumbing, foundation and deferred work; replacement reserves are separate from routine maintenance.</td>"
        f"<td>{link('cdi')}</td></tr>"
        "<tr><td>Property tax / direct levies</td><td></td><td></td>"
        "<td>Unverified property-specific assessment and tax-rate area. Do not multiply an assumed all-in rate by a possibly partial assessment.</td>"
        f"<td>{link('boe19')}</td></tr>"
        "<tr><td>Rental cash flow</td><td></td><td></td>"
        "<td>Unverified. Gross rent is not profit. Verify leases, legal unit count, vacancy, rent regulation and expense allocation privately.</td>"
        f"<td>{link('p527')}</td></tr>"
    )
    + "<h2>Insurance research result</h2>"
    + rows([
        ("Statewide average", "CDI reports a California average homeowner premium of $1,570 and a national average of $1,510 (both rounded to $10 per project rule). Averages describe the market, not either property.", "Verified average; not a property quote", "cdis"),
        ("Market stress", "CDI reports 677,449 FAIR Plan homeowner policies and 662 ZIP codes in distressed areas, alongside 8,300,730 total homeowner policies. Availability, not just price, is a risk.", "Verified market context", "cdis"),
        ("FAIR Plan limits", "FAIR Plan covers fire/lightning, internal explosion and smoke; theft and liability are not covered. Supplemental DIC coverage may be needed. Generic fire coverage must not be treated as comprehensive catastrophe protection.", "Verified general rule", "cdi"),
        ("Shopping route", "CDI provides comparison tools and carrier lists. Obtain occupancy-correct quotes privately; do not adopt a generic annual estimate.", "Verification route", "cdi"),
        ("Earthquake", "Standard homeowner terms do not by themselves establish earthquake protection. Test uninsured earthquake loss separately; no loss amount is verified here.", "Scenario; losses not quantified", "cdi"),
    ])
)

# ---------- projections ----------
page("projections", "50 years: transparent, fictional arithmetic",
    '<section class="notice"><strong>Not the owner\'s forecast.</strong> To avoid exposing private financial fingerprints, '
    "this example starts with a fictional $1,000,000 home, $200,000 assessment and $15,000 operating budget. None describes either property. "
    "Actual annual valuation, assessment and bills remain unverified and are not filled in.</section>"
    "<h2>Assumptions and limitations</h2>"
    "<p>Assume nominal appreciation 3%, general costs/CPI 2.5%, assessment growth 2%, and illustrative base tax 1%. "
    "These are analyst-selected sensitivity inputs, not official forecasts or a certified tax bill. Source links provide legal/economic context only. "
    "No inheritance reassessment event is applied in this pre-transfer continuity illustration; it must not be used as a post-transfer bill.</p>"
    "<p>For n = year − 2026: value = $1,000,000 × 1.03ⁿ; real value = value ÷ 1.025ⁿ; assessment = $200,000 × 1.02ⁿ; "
    "illustrative base tax = assessment × 1%; operating budget = $15,000 × 1.025ⁿ. Real dollars use 2026 purchasing power. "
    "Only display values are rounded to $10; intermediate calculations are not rounded. Tax excludes bonds, direct assessments, exemptions and supplemental bills.</p>"
    + table(["Year", "Fictional market value", "Real value", "Continuity assessment", "Illustrative base tax", "Operating budget", "Status / context sources"], proj_rows())
    + "<h2>Transfer-year branches</h2>"
    + rows([
        ("Rent / no exclusion", "Use transfer-date market value as the reassessment planning branch, subject to assessor review. Future private value and bills remain blank.", "Framework only", "boe19"),
        ("Eligible family home", "With old taxable value B, transfer value V and transfer-year allowance L: new taxable value = B + max(0, V − B − L). Confirm assessor treatment and continued eligibility.", "Derived from exclusion framework; future inputs unknown", "boe19"),
        ("Fictional 2040 branch", "Fictional V $1,512,590, B $263,900, L $1,044,590: new taxable = $468,000. Rent branch = $1,512,590. Illustrates the gap; not a bill.", "Assumption / derived", "boe19"),
        ("Fictional 2050 branch", "Fictional V $2,032,790, B $321,690, L $1,044,590: new taxable = $988,200. Rent branch = $2,032,790. Illustrates the gap; not a bill.", "Assumption / derived", "boe19"),
        ("Estate threshold illustration", "Assuming, not predicting, 2% annual indexing from the 2026 $15,000,000 exclusion gives $19,792,180 in 2040 and $24,126,560 in 2050. Actual legal indexing and law changes differ.", "Hypothetical sensitivity, not future legal allowance", "new"),
    ])
)

# ---------- stress ----------
page("stress", "Black swans & uneven economic paths",
    '<p class="lead">Stress tests are scenarios, not probabilities or historical replays. A smooth baseline hides sequence risk and cash shortages.</p>'
    + rows([
        ("Observed inflation", "BLS reported CPI-U up 6.5% over the 12 months ending December 2022, with electricity up 14.3%. Broad CPI and utility costs did not move together.", "Verified historical context", "cpi"),
        ("Rate regime", "Federal Reserve target rose from 0.25–0.50% in March 2022 to 5.25–5.50% in July 2023, eased to 3.50–3.75% by December 2025, then rose to 3.75–4.00% in September 2026. Rates are a regime, not a constant.", "Verified historical context", "fed"),
        ("Official longer-run anchors", "FOMC September 2025 median longer-run projections: PCE inflation 2.0%, real GDP growth 1.8%, unemployment 4.2%, federal funds rate 3.0%. These are participant medians under appropriate policy, not 50-year forecasts.", "Verified official projections (2025–2028 + longer run)", "sep"),
        ("Housing history", "FHFA House Price Index extends to the mid-1970s and uses repeat-sales methodology across states and metros. Long histories contain booms and busts that a single growth rate cannot represent.", "Verified methodology", "hpi"),
        ("Stagflation assumption", "Test home growth 0% for five years; costs +7% annually for five years. Fictional $15,000 budget becomes $21,040. No probability assigned.", "Hypothetical stress; not a BLS forecast", "cpi"),
        ("Housing crash assumption", "Apply −30% in year one, then +3% for nine years. Fictional $1,000,000 home ends year ten at $913,340, not $1,343,920 under smooth 3% growth.", "Hypothetical stress", "hpi"),
        ("Portfolio sequence assumption", "A fictional $1,000,000 portfolio loses 40%, then earns 6% for nine years: $1,013,690. No tax, fees or withdrawals; not a return forecast.", "Hypothetical stress", "t703"),
        ("Cash-flow sequence assumption", "With $40,000 year-end withdrawals, +20% then −20% leaves $888,000 from $1,000,000; −20% then +20% leaves $872,000. Same two returns, different withdrawal outcome.", "Hypothetical arithmetic", "t703"),
        ("Uninsurable loss / nonrenewal", "Test loss of coverage, higher deductibles and uninsured earthquake loss. Generic fire coverage must not be treated as comprehensive catastrophe protection.", "Scenario; losses not quantified", "cdi"),
        ("Vacancy / repair / law shock", "Test one year without rent, a major repair and reduced tax exclusions together. Keep a liquid reserve; its actual size cannot be verified without expenses.", "Scenario; private dollar impacts unknown", "boe19"),
    ])
    + "<h2>Decision consequence</h2>"
    + rows([
        ("Renting", "Concentrates local housing and tenant risk; requires resilient net cash flow under vacancy and repair shocks.", "Risk framing", "p527"),
        ("Selling", "Concentrates timing risk unless proceeds are diversified and liquidity is preserved. Re-run on the same shock path and liquidation date.", "Risk framing", "basis"),
        ("Occupying", "Creates a housing benefit, not spendable yield. Value it explicitly; do not count it as cash income.", "Risk framing", "boe19"),
    ])
)

# ---------- process ----------
page("process", "From trust transfer to a decision",
    rows([
        ("1 · Before transfer", "Privately review deed, trust amendments, successor trustee powers, beneficiaries, debt, ownership shares and inclusion in the transferor's estate. No document uploads to this site.", "Planning checklist, not legal instruction", "estate"),
        ("2 · At death", "Identify authorized trustee/executor, obtain records securely, secure property and notify insurer. Determine whether assets pass through trust or require probate.", "General checklist", "court"),
        ("3 · Inventory and value", "Inventory assets and liabilities; obtain defensible date-of-death valuation and preserve basis documentation.", "General checklist", "basis"),
        ("4 · Determine estate filings", "Evaluate gross estate, lifetime taxable gifts, deductions, marital provisions and any portability election; tax liability is not just inheritance × a penalty rate.", "General checklist", "estate"),
        ("5 · Review property-tax deadlines", "Contact assessor promptly about change-in-ownership reporting and supplemental assessment. If genuinely occupying and eligible, meet the one-year homeowners-exemption deadline.", "Verified timing; parcel process needs review", "boe19"),
        ("6 · Complete exclusion claim", "File applicable family-home exclusion within three years or before third-party transfer; confirm residence, relationship and value-limit evidence.", "Verified summary; case-specific review needed", "pub801"),
        ("7 · Settle and reserve", "Authorized fiduciary addresses debts, expenses, taxes and distributions according to governing documents and applicable process. Keep funds for unsettled liabilities.", "General checklist", "court"),
        ("8 · Choose and document", "Compare verified net sale proceeds to rental NOI and occupancy benefit; confirm policy changes and basis before executing leases, distribution or sale.", "Conditional decision gate", "t703"),
        ("9 · Review annually", "Refresh insurance, leases, capital needs, tax bills and continued eligibility; re-evaluate law before the actual future transfer.", "Planning recommendation", "boe19"),
    ])
)

# ---------- law-watch ----------
page("law-watch", "What is enacted, what is not",
    '<p class="lead">Only enacted law is stated as law. Pending proposals are not represented as enacted, and no bill is invented.</p>'
    + rows([
        ("Enacted: federal exclusion", "Working Families Tax Cuts signed July 4, 2025 as Public Law 119-21; basic exclusion $15,000,000 for 2026. Congress.gov lists H.R.1 as Became Law (Public Law 119-21).", "Verified enacted law", "hr1"),
        ("Enacted: Prop 19", "Voter-approved November 3, 2020; effective February 16, 2021 for intergenerational exclusion. Current BOE guidance controls; future allowance unknown.", "Verified enacted law", "boe19"),
        ("Enacted: Prop 13", "Voter-approved June 6, 1978; 1% base levy plus bonded debt; acquisition-value system with 2% growth limit. BOE Pub 29 (March 2025) summarizes current law.", "Verified enacted law", "pub29"),
        ("Enacted: state death tax", "No California estate return for deaths on or after January 1, 2005 (Controller guidance). Do not assume a future state estate tax without enactment.", "Verified current guidance", "sco"),
        ("Regulatory: insurance strategy", "CDI Sustainable Insurance Strategy modernizes regulation and requires expanded writing in distressed areas. Regulatory action, not a premium guarantee.", "Verified regulatory context", "cdis"),
        ("Pending legislation", "No pending bill is represented here as enacted. An exhaustive current federal/state/local bill search was not completed; historical repo claims are not carried forward as verified.", "Needs review", "new"),
        ("Future 2040–2050 law", "Exclusion, brackets, Prop 19 allowance and local rules in 2040–2050 are unknown. Recheck enactments at transfer; do not project today's law as certain.", "Unknown future law", "new"),
        ("Ballot / local measures", "No ballot-measure outcome is stated as certified in this release. Local transfer taxes and rental regulation were not comprehensively reverified.", "Needs review", "pub29"),
    ])
)

# ---------- flagged ----------
page("flagged", "Flagged for Review",
    '<p class="lead">Unverified, inconsistent or unresolved items. Blank means not verified — not zero. '
    "These do not block publication, but they block any personalized recommendation until resolved privately.</p>"
    + rows([
        ("F01 · Property values", "No property-specific market value, assessment or tax bill is officially confirmed. Actual numeric cells remain blank.", "Unverified", "boe19"),
        ("F02 · Rental income", "No verified rent, lease, unit count or vacancy rate. Gross rent is not profit.", "Unverified", "p527"),
        ("F03 · Ownership distinction", "Prior summaries suggest disposing of B as if inherited. B is already owned; A's transfer does not by itself create a B step-up or reassessment.", "Corrected in new analysis", "t703"),
        ("F04 · Actual financial values", "No property-specific assessment, tax, rent, utility, premium or repair amount is officially confirmed. Actual numeric cells remain blank.", "Unverified", "boe19"),
        ("F05 · Insurance guess", "No official property-specific premium supports a generic annual estimate. No premium multiplier is adopted from prior reports.", "Unverified", "cdi"),
        ("F06 · Trust and basis", "Estate inclusion, ownership share, relationship, citizenship/domicile and trust terms are unknown. The ordinary exclusion may not fit nonresident estates.", "Unverified", "estate"),
        ("F07 · Assessment discrepancy", "A low reported assessment relative to a bill can have multiple explanations. Partial assessment is a hypothesis, not a verified finding.", "Unverified", "boe19"),
        ("F08 · State/local and law watch", "Local transfer taxes, rental regulation and pending legislation were not comprehensively reverified. No unsupported amounts are shown.", "Needs further official review", "new"),
        ("F09 · No proven optimum", "Without official private inputs, an after-tax personalized ranking cannot honestly be certified. The baseline is a decision comparator, not an investment promise.", "Unresolved", "basis"),
        ("F10 · Forecasts", "The annual table and shock tests are explicitly fictional examples; links do not endorse their chosen growth rates. Actual post-transfer annual forecasts remain unavailable.", "Illustration only", "cpi"),
        ("F11 · Income-tax detail", "Brackets, home-sale exclusion, depreciation and net-investment-tax details were not computed in this release. Do not assume them.", "Unresolved", "p523"),
        ("F12 · HUD rent context", "Attempted HUD rent-data page returned 403 in this session. No rent benchmark is shown.", "Unverified", "uad"),
    ])
)

# ---------- sources ----------
page("sources", "Sources, evidence & privacy boundaries",
    "<p>Official pages below were retrieved and read during this session on 11 November 2026. "
    "This is a targeted verification of this artifact, not certification of every line in the preserved legacy repository. "
    "Links in hypothetical rows support context, not their fictional inputs.</p>"
    + table(["Publisher / topic", "Evidence checked", "Status"],
        f"<tr><td>{link('sco')}</td><td>California estate-return and historical inheritance-tax dates</td><td>Retrieved and read</td></tr>"
        f"<tr><td>{link('pub29')}</td><td>1% base levy, bonded debt, assessment growth cap and reassessment</td><td>Retrieved and read</td></tr>"
        f"<tr><td>{link('ftb')}</td><td>Inheritance receipt vs subsequent taxable income</td><td>Retrieved and read</td></tr>"
        f"<tr><td>{link('boe19')}</td><td>Principal residence, claims timing, value-limit framework</td><td>Retrieved and read</td></tr>"
        f"<tr><td>{link('pub801')}</td><td>Allowance $1,044,590 (rounded), 1-year / 3-year deadlines, worked example</td><td>Retrieved and read</td></tr>"
        f"<tr><td>{link('estate')}</td><td>2026 exclusion, gross estate, lifetime gifts, portability</td><td>Retrieved and read</td></tr>"
        f"<tr><td>{link('new')}</td><td>Public Law 119-21 and 2026 exclusion</td><td>Retrieved and read</td></tr>"
        f"<tr><td>{link('faq')}</td><td>Filing threshold table and portability election</td><td>Retrieved and read</td></tr>"
        f"<tr><td>{link('basis')}</td><td>Inherited basis and later sale gains</td><td>Retrieved and read</td></tr>"
        f"<tr><td>{link('cdi')}</td><td>Comparison tools; FAIR Plan limitations</td><td>Retrieved and read</td></tr>"
        f"<tr><td>{link('cdis')}</td><td>Average premium $1,570 (rounded), FAIR Plan counts, distressed ZIPs</td><td>Retrieved and read</td></tr>"
        f"<tr><td>{link('cpi')}</td><td>December 2022 annual CPI 6.5% and electricity 14.3%</td><td>Retrieved and read</td></tr>"
        f"<tr><td>{link('court')}</td><td>Estate inventory, authority and transfer process</td><td>Retrieved and read</td></tr>"
        f"<tr><td>{link('t703')}</td><td>Cost basis, improvements and depreciation</td><td>Retrieved and read</td></tr>"
        f"<tr><td>{link('p527')}</td><td>Rental income, expenses, depreciation</td><td>Retrieved and read</td></tr>"
        f"<tr><td>{link('p523')}</td><td>Home-sale exclusion structure and basis adjustments</td><td>Retrieved and read</td></tr>"
        f"<tr><td>{link('fed')}</td><td>Federal funds target path 2022–2026</td><td>Retrieved and read</td></tr>"
        f"<tr><td>{link('sep')}</td><td>FOMC longer-run medians (PCE 2.0%, GDP 1.8%, funds 3.0%)</td><td>Retrieved and read</td></tr>"
        f"<tr><td>{link('hpi')}</td><td>House Price Index history to mid-1970s, repeat-sales method</td><td>Retrieved and read</td></tr>"
        f"<tr><td>{link('cpuc')}</td><td>Electric rate-setting proceedings and tariff structure</td><td>Retrieved and read</td></tr>"
        f"<tr><td>{link('cityutil')}</td><td>City water/power/sewer services and rate pages exist; no fixed bill verified</td><td>Retrieved and read</td></tr>"
        f"<tr><td>{link('hr1')}</td><td>H.R.1 Became Law as Public Law 119-21 on July 4, 2025</td><td>Retrieved and read</td></tr>"
        f"<tr><td>HUD rent data (attempted)</td><td>Attempted rent-data page returned 403; no benchmark shown</td><td>Not retrieved — flagged F12 · {link('uad')}</td></tr>"
        f"<tr><td>BOE homeowners-exemption page (attempted)</td><td>Attempted page returned 404; timing verified via Prop 19 fact sheet instead</td><td>Not retrieved — timing via Pub 801 · {link('pub801')}</td></tr>"
    )
    + "<h2>Verification contract</h2>"
    + rows([
        ("Verified means", "The stated general rule was checked in retrieved official text, not that a private property figure was verified. Unverified values are blank, not zero.", "Contract", "estate"),
        ("Illustrations", "Analysis, assumptions, formulas and stress tests have separate labels. Monetary illustrations are rounded to $10; no external analytics, forms, trackers, libraries or personal-data requests are used.", "Contract", "cpi"),
        ("Deployment boundary", "This directory is additive and standalone. Legacy research trees, data and coordination logs are excluded from the curated Pages artifact. A noindex request is not access control. The public repository and previous commits remain a privacy risk; a private planning tool would be safer for actual financial inputs.", "Boundary", "sco"),
    ])
)

print(f"Built {len(NAV)} pages in {ROOT}")
