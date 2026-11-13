"""Builds the static decision site into ../ (tino5-3f269806/). Run: python3 _src/build.py
Every table row must carry at least one source id; build fails otherwise.
"""
import html, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from model import *   # noqa
from sources import SRC, STATUS_LABEL

OUT = os.path.abspath(os.path.join(HERE, ".."))
ASOF = "13 Nov 2026"
BASE_PATH = "."  # relative links so the site works under GitHub Pages sub-path

PAGES = [
    ("index.html", "Home"),
    ("executive-summary.html", "Executive summary"),
    ("property-facts.html", "Property facts"),
    ("tax-thresholds.html", "Tax and inheritance thresholds"),
    ("projections.html", "Projections 2026-2076"),
    ("scenarios.html", "Live, rent or sell"),
    ("black-swans.html", "Black-swan economics"),
    ("trust-process.html", "Trust inheritance steps"),
    ("questions.html", "Questions and gaps"),
    ("suggestions.html", "Suggestions (for your choice)"),
    ("law-watch.html", "Law watch"),
    ("sources.html", "Source register"),
    ("flagged.html", "Flagged for review"),
]

ST = {
    "verified": ("Verified", "b-ok"),
    "statutory": ("Statutory (exact)", "b-ok"),
    "owner": ("Owner input - unverified", "b-warn"),
    "assume": ("Assumption", "b-grey"),
    "derived": ("Derived from inputs", "b-blue"),
    "unverified": ("Unverified - blank", "b-bad"),
    "answered": ("Answered (law)", "b-ok"),
    "partial": ("Partly answered", "b-warn"),
    "missing": ("Missing", "b-bad"),
    "pending": ("Awaiting your choice", "b-warn"),
}


def M(x):
    """Money, rounded to nearest $10."""
    v = r10(x)
    return ("-$" if v < 0 else "$") + f"{abs(v):,}"


def MM(x):
    """Money per month, rounded to nearest $10."""
    return M(x)


def S(x):
    """Statutory / agency amount shown exactly as published (marked)."""
    return f"${x:,}"


def P(x, d=2):
    return f"{x*100:.{d}f}%"


def esc(t):
    return html.escape(str(t), quote=True)


def srclinks(ids):
    out = []
    for i in ids:
        s = SRC[i]
        out.append(f'<a href="{esc(s["url"])}" rel="noopener" title="{esc(s["title"])}">{i}</a>')
    return ", ".join(out)


def badge(st):
    label, cls = ST[st]
    return f'<span class="badge {cls}">{label}</span>'


def table(tid, headers, rows, note=None):
    """rows: list of dict(cells=[str...], st=key, src=[ids])  (cells are pre-formatted HTML)."""
    head = "".join(f"<th>{h}</th>" for h in headers) + "<th>Status</th><th>Source (official link)</th>"
    body = []
    for r in rows:
        if not r.get("src"):
            raise SystemExit(f"Table {tid}: row without source: {r['cells'][0]}")
        for sid in r["src"]:
            if sid not in SRC:
                raise SystemExit(f"Table {tid}: unknown source {sid}")
        cells = "".join(f"<td>{c}</td>" for c in r["cells"])
        body.append(f"<tr>{cells}<td>{badge(r['st'])}</td><td>{srclinks(r['src'])}</td></tr>")
    nt = f'<p class="note">{note}</p>' if note else ""
    return (f'<div class="tablewrap"><input class="filter" data-target="{tid}" placeholder="Filter this table..." type="search">'
            f'<table class="data" id="{tid}"><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>{nt}')


def simple_table(tid, headers, rows):
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return (f'<div class="tablewrap"><input class="filter" data-target="{tid}" placeholder="Filter this table..." type="search">'
            f'<table class="data" id="{tid}"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')


def nav(active):
    items = []
    for f, label in PAGES:
        cls = ' class="on"' if f == active else ""
        items.append(f'<a href="{f}"{cls}>{label}</a>')
    return "<nav>" + "".join(items) + "</nav>"


def page(fname, title, body, lede=""):
    lab = dict(PAGES)[fname]
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{esc(title)} | Inheritance decision desk</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="top">
  <div class="brand"><a href="index.html">Inheritance decision desk</a><span>Property A (trust, 2040-2050) &middot; Property B (owned)</span></div>
  {nav(fname)}
</header>
<main>
<h1>{esc(title)}</h1>
{('<p class="lede">' + lede + '</p>') if lede else ''}
{body}
</main>
<footer>
  <p>Data as of {ASOF}. Owner figures are rounded to the nearest $10 and are not verified against assessor or bill records. Official sources are linked on every table row (see the source register). Educational analysis only: not legal, tax or investment advice. Confirm with a California estate attorney and a CPA before acting.</p>
  <p>Privacy: no names, street addresses, parcel or account numbers, ZIP codes or city names appear on this site. Properties are labelled A and B.</p>
</footer>
<script src="assets/app.js"></script>
</body>
</html>
"""


def kpi(label, value, sub=""):
    return f'<div class="kpi"><div class="kl">{label}</div><div class="kv">{value}</div><div class="ks">{sub}</div></div>'


# ---------------------------------------------------------------- computed numbers
CAP_2026 = A_AV0 + CAP_ADD_2026
TAX_LIVE_2026 = A_RATE * min(A_MV0, CAP_2026)
TAX_RENT_2026 = A_RATE * A_MV0
B_NOI26 = B_noi(BASE, 2026)
DEC = {T: decision(BASE, T) for T in (2040, 2045, 2050)}
KNOWN_EST_2026 = A_MV0 + B_MV0
HEADROOM_2026 = FED_EXEMPT_2026 - KNOWN_EST_2026
# federal exemption projected at CPI assumption (ASSUMPTION; statute indexes from 2027)
def exempt_proj(year):
    return FED_EXEMPT_2026 * (1 + BASE["cpi"]) ** (year - 2026)


# CPI Dec-to-Dec 1972..1982 from BLS S15 (values transcribed from the official table)
CPI_DEC = {1972: 42.5, 1973: 46.2, 1974: 51.9, 1975: 55.5, 1976: 58.2, 1977: 62.1, 1978: 67.7,
           1979: 76.7, 1980: 86.3, 1981: 94.0, 1982: 97.6}
CPI_YOY = {y: CPI_DEC[y] / CPI_DEC[y - 1] - 1 for y in range(1973, 1983)}
CPI_AVG_72_82 = (CPI_DEC[1982] / CPI_DEC[1972]) ** (1 / 10) - 1


def build():
    files = {}

    # ---------------- INDEX
    kp = "".join([
        kpi("Property A value (owner estimate)", M(A_MV0), "Santa Clara County; trust inheritance 2040-2050"),
        kpi("Property A assessed value 2026", M(A_AV0), "Prop 13 base, owner input (unverified)"),
        kpi("Federal exclusion 2026", S(FED_EXEMPT_2026), "Per person; statutory; S01 / S02"),
        kpi("California estate or inheritance tax", "None", "S07"),
        kpi("Renting A forfeits Prop 19 exclusion", "Yes", "Tax on A would rise to market value; S08"),
        kpi("Break-even rent to live in A (2040, base)", MM(DEC[2040]["be_live"] / 12) + " / mo", "Derived; assumption-driven; see scenarios"),
    ])
    cards = "".join(f'<a class="card" href="{f}"><h3>{lab}</h3><p>{desc}</p></a>' for f, lab, desc in [
        ("executive-summary.html", "Executive summary", "The answer first: what is verified, what is not, and the leading path."),
        ("property-facts.html", "Property facts", "Both properties, assessment and tax histories (rounded), rules that apply."),
        ("tax-thresholds.html", "Tax and inheritance thresholds", "Federal, California and local thresholds with headroom."),
        ("projections.html", "Projections 2026-2076", "Year-by-year value, assessed value, tax, insurance, water, rent."),
        ("scenarios.html", "Live, rent or sell", "Three paths compared for transfers in 2040, 2045 and 2050."),
        ("black-swans.html", "Black-swan economics", "Stagflation, slump, deflation and rule-change stress cases over 50 years."),
        ("trust-process.html", "Trust inheritance steps", "Step-by-step process with deadlines and official references."),
        ("questions.html", "Questions and gaps", "What is answered, what is missing, and how to close each gap."),
        ("suggestions.html", "Suggestions (for your choice)", "Options to improve the decision process. Nothing is implemented until you pick."),
        ("law-watch.html", "Law watch", "Enacted changes, dated deadlines and proposals that could change the answer."),
        ("sources.html", "Source register", "Every official link used, with what was read on it."),
        ("flagged.html", "Flagged for review", "Irregularities and unverified items, with links for manual checking."),
    ])
    body = f"""
<p class="lede">A decision desk for a future trust inheritance of <b>Property A</b> (Santa Clara County, California, expected 2040-2050) and a property already owned, <b>Property B</b> (San Francisco County). Built only from official sources where available; owner figures are rounded to $10 and labelled.</p>
<div class="kpis">{kp}</div>
<h2>Start here</h2>
<div class="cards">{cards}</div>
<h2>How to read this site</h2>
<ul>
<li><span class="badge b-ok">Verified</span> read on an official page and linked.</li>
<li><span class="badge b-warn">Owner input - unverified</span> your figure, rounded to $10; not checked against records.</li>
<li><span class="badge b-grey">Assumption</span> a modelling choice (labelled); change it to test the answer.</li>
<li><span class="badge b-bad">Unverified - blank</span> no value is shown because no official source confirmed it.</li>
</ul>
<p>Last research pass: {ASOF}. Other decision pages in this repository (from earlier sessions) show some figures that differ from official sources. See <a href="flagged.html">Flagged for review</a>.</p>
"""
    files["index.html"] = page("index.html", "Inheritance decision desk", body)

    # ---------------- EXECUTIVE SUMMARY
    d40 = DEC[2040]
    body = f"""
<h2>Bottom line</h2>
<div class="callout">
<p><b>1. Do not rent Property A.</b> Under Proposition 19, the parent-child exclusion applies only if the heir lives in the home as a principal residence. Renting it puts the home back to full market value for tax. On owner estimates, 2026 tax would move from about {M(A_TAX25)} a year to about {M(TAX_RENT_2026)} a year (source: <a href="https://www.boe.ca.gov/prop19/">S08</a>, <a href="https://www.boe.ca.gov/pdf/pub800-9.pdf">S10</a>).</p>
<p><b>2. If the heir moves in, the tax stays far higher than today but well below market.</b> With the $1,044,586 add-on (<a href="https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf">S09</a>), the taxable value would be about {M(CAP_2026)} in 2026 terms, giving about {M(TAX_LIVE_2026)} a year at the owner-implied rate.</p>
<p><b>3. Living versus selling is not settled. It depends on one number you do not have yet:</b> the rent you would otherwise pay (or the rent you would forgo) for comparable housing. In the 2040 base case, living in A only wins if that avoided rent is above about <b>{M(d40["be_live"]/12)} a month</b>. Below that level, the base case favours selling and reinvesting, but only while the after-tax return assumption holds (see <a href="scenarios.html">scenarios</a>).</p>
<p><b>4. Federal estate tax is a decedent-level question.</b> The federal basic exclusion is {S(FED_EXEMPT_2026)} per person for 2026 deaths (<a href="https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax">S01</a>). Heirs do not pay it. California has no estate or inheritance tax (<a href="https://www.sco.ca.gov/ardtax_estate_tax.html">S07</a>).</p>
</div>

<h2>Key figures (rounded to $10)</h2>
{table("es1", ["Item", "Value", "Basis"], [
    dict(cells=["Property A market value (owner estimate, Nov 2026)", M(A_MV0), "Owner input; check the assessor's record and an appraisal"], st="owner", src=["S25", "S27"]),
    dict(cells=["Property A assessed value 2026 (owner input)", M(A_AV0), "Owner input; check the assessor's roll"], st="owner", src=["S25", "S27"]),
    dict(cells=["Property A tax if heir lives there, 2026 terms (derived)", M(TAX_LIVE_2026), "Owner-implied rate x base plus add-on (S09)"], st="derived", src=["S09", "S12"]),
    dict(cells=["Property A tax if rented, 2026 terms (derived)", M(TAX_RENT_2026), "Owner-implied rate x market value (S08)"], st="derived", src=["S08", "S10"]),
    dict(cells=["Property B market value (owner estimate)", M(B_MV0), "Owner input; check the assessor's record and an appraisal"], st="owner", src=["S26"]),
    dict(cells=["Property B net operating income 2026 (derived)", M(B_NOI26["noi"]), "Rent less vacancy, upkeep, tax, water, power and insurance (owner inputs and assumptions)"], st="derived", src=["S13", "S19"]),
    dict(cells=["Known property, both (owner estimates)", M(KNOWN_EST_2026), "Sum of two owner estimates"], st="owner", src=["S25", "S26"]),
    dict(cells=["Federal exclusion 2026 minus known property (derived)", M(HEADROOM_2026), "Only if nothing else is in the estate (S01)"], st="derived", src=["S01", "S02"]),
])}

<h2>What is verified, and what is not</h2>
<ul>
<li><b>Verified:</b> federal exclusion and filing threshold, 2026 (S01, S02); gift exclusion $19,000 (S03); top estate rate 40% (S04); basis at date of death (S05); no CA estate tax (S07); Prop 19 rules (S08); the $1,044,586 add-on (S09); reassessment at date of death and the 150-day filing (S10); Prop 13 base rules and the $7,000 homeowners' exemption (S11); Santa Clara 1% plus bonds (S12); SF FY 2026-27 rate (S13).</li>
<li><b>Not verified:</b> every owner figure (values, assessed values, tax bills, rent, utilities, insurance); the water provider for Property A; the solar credit; Property B's billed tax (it implies a rate about {P(B_RATE_BILLED,2)}, well above the SF rate). These are blank in the verified tables and flagged.</li>
<li><b>Assumptions:</b> inflation 2% (anchored to the Fed goal, S14); property growth 2%; after-tax reinvestment return 4%; selling costs 6%; upkeep; insurance growth. All are labelled and can be changed in the model.</li>
</ul>

<h2>Leading path (decision as it stands)</h2>
<ol>
<li>Treat renting Property A as the weakest path on current law unless the rent covers about {M(d40["be_rent"]/12)} a month gross (2040, base).</li>
<li>Collect the three missing inputs before choosing between living and selling: an appraisal for A, a comparable-rent study for A, and the trust's distribution terms. See <a href="questions.html">questions and gaps</a>.</li>
<li>Choose from the <a href="suggestions.html">suggestions</a> page. Nothing on the site changes until you pick an option.</li>
</ol>
<p class="note">This is an analysis of rules and owner inputs, not advice. The threshold figures change with the assumptions; test them on the scenarios page.</p>
"""
    files["executive-summary.html"] = page("executive-summary.html", "Executive summary", body,
                                           lede="The one-page answer, with what is verified and what is still missing.")

    # ---------------- PROPERTY FACTS
    facts = table("facts", ["Item", "Value", "Note"], [
        dict(cells=["Property A: estimated market value, Nov 2026", M(A_MV0), "Owner estimate; needs an appraisal"], st="owner", src=["S08"]),
        dict(cells=["Property A: assessed value, 2026", M(A_AV0), "Owner input; Prop 13 limit is the lesser of CPI or 2% a year"], st="owner", src=["S12"]),
        dict(cells=["Property A: tax rate used (derived from owner's 2025 bill)", P(A_RATE, 3), "Santa Clara rule is 1% plus voter bonds; exact parcel rate not verified (flag F03)"], st="derived", src=["S12"]),
        dict(cells=["Property A: add-on above base year value at transfer", S(CAP_ADD_2026), "Statutory; adjusted every other February by HPI; next Feb 2027"], st="statutory", src=["S09"]),
        dict(cells=["Property A: homeowners' exemption (owner-occupied only)", S(HOMEOWNERS_EXEMPT), "Rentals do not qualify (S11). Not modelled."], st="statutory", src=["S11"]),
        dict(cells=["Property B: estimated market value, Nov 2026", M(B_MV0), "Owner estimate; needs an appraisal"], st="owner", src=["S08"]),
        dict(cells=["Property B: secured tax rate, FY 2026-27", P(SF_RATE_FY2627, 4), "Published SF rate (S13)"], st="verified", src=["S13"]),
        dict(cells=["Property B: rent, two rented units (per month)", M(B_RENT_MO), "Owner input; rent-control and lease terms not checked (flag F12)"], st="owner", src=["S13"]),
        dict(cells=["Property B: water, three units (per month, midpoint)", M(B_WATER_MO), "Owner range $330-$400; SFPUC rate schedule not extracted"], st="owner", src=["S19"]),
        dict(cells=["Property B: electricity (per month, midpoint)", M(B_ELEC_MO), "Owner range $30-$70; provider and tariff not verified"], st="owner", src=["S19"]),
        dict(cells=["Property A: water (per month, midpoint)", M(A_WATER_MO), "Owner range $100-$150; provider not confirmed (F05)"], st="owner", src=["S20"]),
        dict(cells=["Property A: electricity and solar credit", "$0 net (base)", "Owner reports a credit of about $10-$20 a month; not verifiable without 12 months of PG&E statements (F06)"], st="unverified", src=["S16"]),
        dict(cells=["Homeowners insurance, A and B (per year, each)", M(A_INS), "Owner estimate. CDI does not publish a per-property average on the page we read (F04)"], st="unverified", src=["S17", "S18"]),
        dict(cells=["Maintenance, A", "0.5% of value a year", "Assumption; no source. Owner said it is lower than B."], st="assume", src=["S08"]),
    ])
    body = f"""
<h2>Rules that drive the answer</h2>
{table("rules", ["Rule", "What it means for this decision"], [
    dict(cells=["Prop 13 base: assessed value resets to market only on change of ownership or new construction", "Property A has been taxed on a low base; a transfer resets it"], st="verified", src=["S11"]),
    dict(cells=["Prop 13 annual growth: lesser of CPI or 2%", "The base grows at most 2% a year"], st="verified", src=["S12"]),
    dict(cells=["Tax rate: 1% plus voter-approved bonds", "Effective rate differs by location and bonds"], st="verified", src=["S11", "S12"]),
    dict(cells=["Death is a change of ownership on the date of death, even if distribution is delayed", "Reassessment is measured from death, not from distribution"], st="verified", src=["S10"]),
    dict(cells=["Parent-child exclusion: child must make the home a principal residence", "Occupancy within one year of the death; claim within three years or before any sale"], st="verified", src=["S08", "S10"]),
    dict(cells=["Renting out the home loses the parent-child exclusion", "Market value is used for tax on the home"], st="verified", src=["S08"]),
    dict(cells=["Add-on above base value: $1,044,586 (valid to 15 Feb 2027)", "Taxable value on a qualifying transfer = base value plus add-on"], st="statutory", src=["S09"]),
    dict(cells=["Homeowners' exemption: $7,000 for an owner-occupied principal residence", "Applies to Property B only if the owner-occupied unit qualifies (flag F10)"], st="statutory", src=["S11"]),
    dict(cells=["SF secured rate FY 2026-27: 1.18162182%", "Used for comparison; the owner's billed amount does not match it (flag F02)"], st="verified", src=["S13"]),
])}
<h2>Property facts used in the model</h2>
{facts}
"""
    files["property-facts.html"] = page("property-facts.html", "Property facts", body,
                                        lede="Both properties, anonymised as A and B. Owner figures are rounded to $10 and are labelled unverified until checked against official records.")

    # ---------------- TAX & THRESHOLDS
    tax_rows = table("tax", ["Item", "Value", "Notes"], [
        dict(cells=["Federal estate and gift basic exclusion, deaths and gifts in 2026", S(FED_EXEMPT_2026), "Per person. Married couples can combine with portability (S01, S02)."], st="statutory", src=["S01", "S02"]),
        dict(cells=["Federal estate tax filing threshold, 2026 deaths", S(FED_EXEMPT_2026), "Form 706 needed only above this gross estate (S02)."], st="statutory", src=["S02"]),
        dict(cells=["Top federal estate tax rate", "40%", "Applies only above the exclusion (rate table ends at 40% above $1,000,000) (S04)."], st="statutory", src=["S04"]),
        dict(cells=["Federal annual gift exclusion, 2026, per recipient", S(GIFT_EXCL_2026), "Gifts above this use the lifetime exclusion (S03 sec 4.42)."], st="statutory", src=["S03"]),
        dict(cells=["Estates and trusts: top 37% bracket starts above taxable income of", "$16,000", "Trusts reach the top bracket fast (S03, table 5)."], st="statutory", src=["S03"]),
        dict(cells=["Estates and trusts: maximum 0% capital-gains amount", S(3300), "2026 (S03 sec 4.03)."], st="statutory", src=["S03"]),
        dict(cells=["Estates and trusts: maximum 15% capital-gains amount", S(16250), "2026 (S03 sec 4.03). A different figure appears on another page in this repo (F09)."], st="statutory", src=["S03"]),
        dict(cells=["Basis of inherited property", "Fair market value at date of death", "IRC sec 1014 (S05). Step-up applies to both properties."], st="statutory", src=["S05"]),
        dict(cells=["California estate tax", "None (decedents dying on or after 1 Jan 2005)", "Per the State Controller (S07)."], st="verified", src=["S07"]),
        dict(cells=["California inheritance tax", "None", "The SCO page covers estate, inheritance and gift tax; the only remaining inheritance-tax collection is for deaths before 1982 (S07)."], st="verified", src=["S07"]),
        dict(cells=["California gift tax", "None (new gifts)", "The SCO page says it collects gift tax only for gifts before 8 June 1982 (S07)."], st="verified", src=["S07"]),
        dict(cells=["Prop 19 add-on to base value (valid to 15 Feb 2027)", S(CAP_ADD_2026), "Next adjustment Feb 2027 (S09)."], st="statutory", src=["S09"]),
        dict(cells=["Prop 19 claim timing", "Occupancy within 1 year; claim within 3 years or before transfer", "Per BOE (S08, S10). Confirm with the assessor."], st="verified", src=["S08", "S10"]),
        dict(cells=["Filing: BOE-502-D (change in ownership on death)", "Within 150 days", "Trustee or transferee files with the assessor (S10)."], st="verified", src=["S10"]),
        dict(cells=["Property tax installments (Santa Clara)", "Due 1 Nov and 1 Feb; delinquent after 10 Dec and 10 Apr", "Penalties 10% (S12)."], st="verified", src=["S12"]),
        dict(cells=["Property tax installments (San Francisco)", "1st due 10 Dec; 2nd due 10 Apr", "Penalties 10% (S13)."], st="verified", src=["S13"]),
    ])
    body = f"""
<h2>Threshold: how much can pass tax-free</h2>
<p>The federal estate tax falls on the <b>decedent's</b> estate, not on the heir. The threshold is the decedent's total taxable estate plus lifetime taxable gifts, against the exclusion for the year of death. California has no estate or inheritance tax. Heirs owe no federal inheritance tax.</p>
{table("head", ["Measure", "Amount", "Basis"], [
    dict(cells=["Federal exclusion, 2026 deaths", S(FED_EXEMPT_2026), "Statutory (S01, S02)"], st="statutory", src=["S01", "S02"]),
    dict(cells=["Known property, both (owner estimates, rounded)", M(KNOWN_EST_2026), "Owner input (unverified)"], st="owner", src=["S25", "S26"]),
    dict(cells=["Headroom before any federal estate tax, 2026 (derived)", M(HEADROOM_2026), "Only if no other assets, debts or gifts count"], st="derived", src=["S02"]),
    dict(cells=["Exclusion projected to 2040 at 2% CPI (assumption)", M(exempt_proj(2040)), "Statute indexes from 2027; 2027+ figure not yet published (flag F07)"], st="assume", src=["S01", "S14"]),
    dict(cells=["Exclusion projected to 2050 at 2% CPI (assumption)", M(exempt_proj(2050)), "Same assumption"], st="assume", src=["S01", "S14"]),
    dict(cells=["Estate tax on each dollar above the exclusion", "40 cents", "Top rate (S04)"], st="statutory", src=["S04"]),
])}
<p class="note">Illustration only: if the decedent's estate were {M(KNOWN_EST_2026 + 15000000 - 1000000)} with a 2026 exclusion, the excess of $1,000,000 would bear about {M(0.40 * 1000000)} of federal estate tax, before deductions and credits. This uses the statutory rate and is not a calculation for any real estate.</p>
<h2>Tax and inheritance rules (verified)</h2>
{tax_rows}
<h2>Local property tax on inheritance (Santa Clara County and San Francisco)</h2>
<p>The main local cost of inheriting is property tax. Under Prop 13 the base resets on transfer. For a transfer to a child, the parent-child exclusion keeps taxable value to the base plus the add-on, but only if the child occupies the home. Without it, the home is taxed at market value. The projections and scenarios show both cases.</p>
"""
    files["tax-thresholds.html"] = page("tax-thresholds.html", "Tax and inheritance thresholds", body,
                                        lede="Federal, California and local thresholds with the headroom each one leaves.")

    # ---------------- PROJECTIONS
    yrs = list(range(2026, 2051)) + [2060, 2070, 2076]
    rows = []
    for y in yrs:
        V, base = prop_a(BASE, y)
        tax_keep = A_RATE * base
        if y >= 2040:
            tex = A_RATE * A_av_excl(BASE, 2040, y)
            tno = A_RATE * A_av_noexcl(BASE, 2040, y)
            tex_s, tno_s = M(tex), M(tno)
        else:
            tex_s = tno_s = "pre-transfer"
        ins, water, maint = A_costs(BASE, y)
        b = B_noi(BASE, y)
        rows.append(dict(cells=[str(y), M(V), M(base), M(tax_keep), tex_s, tno_s, M(ins), M(water), M(maint), M(b["noi"])],
                         st="derived", src=["S08", "S09", "S12", "S13"]))
    pr = table("proj", ["Year", "Property A market value", "A assessed value (no transfer)", "A tax (no transfer)",
                        "A tax if heir lives there (from 2040)", "A tax if rented (from 2040)", "A insurance", "A water", "A upkeep", "B net operating income"],
               rows, note="Base case only. Transfer assumed in 2040 for the two tax columns. Tax rate " + P(A_RATE, 3) + " (owner-implied). Add-on $1,044,586 held flat (the BOE adjusts it, so this is conservative). Owner inputs are unverified; assumptions are on the Scenarios page. Rows cite the rules and the owner-input status shown.")
    body = f"""
<h2>Year-by-year base case, 2026-2050, with milestones to 2076</h2>
<p>Values are nominal dollars, rounded to $10. Use the 'if rented' column to see what letting the home out would cost in tax.</p>
{pr}
<h2>Reading the table</h2>
<ul>
<li>Property A market value grows at the base assumption (2% a year), so market value roughly doubles about every 35 years.</li>
<li>Without a transfer, A's assessed value grows only at the lesser of CPI or 2%, so its tax grows slowly. A transfer resets it.</li>
<li>If the heir lives in A, the taxable value is the base plus the add-on, which is far below market but well above today's assessed value.</li>
<li>If the heir rents A, the taxable value is the market value, which is several times higher.</li>
<li>Property B's net operating income uses owner inputs for rent, utilities and insurance, and assumptions for vacancy and upkeep. It excludes the owner-occupied unit's imputed rent.</li>
</ul>
"""
    files["projections.html"] = page("projections.html", "Projections 2026-2076", body,
                                     lede="Year-by-year value, assessed value, tax, insurance, water and rent. Base case, with owner inputs labelled.")

    # ---------------- SCENARIOS
    rows = []
    def scen_row(label, key, fmt, src, st="derived"):
        cells = [label] + [fmt(DEC[T][key]) for T in (2040, 2045, 2050)]
        return dict(cells=cells, st=st, src=src)
    rows = [
        scen_row("Market value of A at transfer", "V", M, ["S08"]),
        scen_row("Net proceeds if sold (after 6% selling-cost assumption)", "P", M, ["S08"], "assume"),
        scen_row("Annual return if reinvested (4% assumption, after tax)", "inv", M, ["S11"], "assume"),
        scen_row("Tax on A if heir lives there (exclusion kept)", "tax_ex", M, ["S09", "S08"]),
        scen_row("Tax on A if rented (exclusion lost)", "tax_no", M, ["S08", "S10"]),
        scen_row("Insurance, A (estimate grown 4% a year)", "ins", M, ["S17"], "owner"),
        scen_row("Water, A (midpoint grown 3% a year)", "water", M, ["S19"], "owner"),
        scen_row("Upkeep, A (0.5% of value)", "maint", M, ["S08"], "assume"),
        scen_row("Yearly carry if living in A", "carry_live", M, ["S09"]),
        scen_row("Yearly carry if renting A", "carry_rent", M, ["S08"]),
        scen_row("Avoided comparable rent needed to prefer living in A (a year)", "be_live", M, ["S08"]),
        scen_row("Same, per month", "be_live", lambda x: M(x / 12), ["S08"]),
        scen_row("Gross rent needed to prefer renting A (a month)", "be_rent", lambda x: M(x / 12), ["S08"]),
    ]
    sc_tab = table("scen", ["Measure (base case)", "Transfer 2040", "Transfer 2045", "Transfer 2050"], rows,
                   note="All figures are derived from the owner inputs and the labelled assumptions; none is a forecast. Income tax on rent and investment income is not modelled (F13). Selling costs, upkeep and return are assumptions.")
    # threshold grid: reinvest return at which living beats selling, by avoided monthly rent
    grid_rows = []
    for m in (8000, 12000, 16000, 20000):
        r_star = (12 * m - DEC[2040]["carry_live"]) / DEC[2040]["P"]
        grid_rows.append(dict(cells=[M(m), P(r_star, 2) if r_star > 0 else "n/a (living wins at any return)"],
                              st="derived", src=["S08", "S11"]))
    grid = table("grid", ["Comparable rent you would avoid (per month)", "Reinvestment return below which living in A wins (transfer 2040)"], grid_rows,
                 note="Rent amounts are illustrations, not estimates. Replace them with an appraiser's or a rental study's figure (see Questions).")
    body = f"""
<div class="callout">
<p><b>Best path on current evidence:</b> renting Property A is clearly the weakest path, because it forfeits the parent-child exclusion. Between living and selling, the answer turns on comparable rent and the return you can earn on the proceeds. Both are unknown today.</p>
</div>
<h2>Three paths compared, transfers in 2040, 2045 and 2050</h2>
{sc_tab}
<h2>Decision threshold</h2>
<p>If the heir would otherwise pay (or forgo) rent of a given amount for comparable housing, the table shows the reinvestment return below which living in A is the better choice for a 2040 transfer. Above that return, selling and reinvesting wins.</p>
{grid}
<h2>How the three paths compare</h2>
{table("paths", ["Path", "Cash effect each year (transfer 2040, base)", "Tax treatment", "Main risk"], [
    dict(cells=["A. Heir lives in A", "Pays about " + M(DEC[2040]["carry_live"]) + " a year; avoids rent for comparable housing", "Exclusion kept, if conditions met", "Occupancy within one year; comparable rent must be realistic"], st="derived", src=["S08", "S10"]),
    dict(cells=["B. Sell A, reinvest proceeds", "Earns about " + M(DEC[2040]["inv"]) + " a year (assumption); no carry on A", "Basis at date of death, so little or no capital gain if sold soon", "Return and selling-cost assumptions; market timing"], st="assume", src=["S05", "S11"]),
    dict(cells=["C. Rent A out", "Must cover about " + M(DEC[2040]["carry_rent"]) + " a year in carry plus the reinvestment return it displaces", "Exclusion lost; market-value tax", "Rent must reach about " + M(DEC[2040]["be_rent"] / 12) + " a month gross; landlord insurance not priced"], st="derived", src=["S08"]),
])}
<h2>What to do with the answer</h2>
<ul>
<li>Without a comparable-rent figure, the base case (4% after-tax return) favours selling over living in A, because the carry is larger than the return on the proceeds.</li>
<li>If comparable housing rents for more than the 2040 threshold, living in A is better. Test with the grid above.</li>
<li>Do not rent Property A out without the numbers in path C.</li>
</ul>
"""
    files["scenarios.html"] = page("scenarios.html", "Live, rent or sell", body,
                                   lede="The three paths for Property A, compared at transfers in 2040, 2045 and 2050. Every figure is derived from labelled inputs.")

    # ---------------- BLACK SWANS
    sc_rows = []
    for sc in SCENARIOS:
        d = decision(sc, 2050)
        V, _ = prop_a(sc, 2050)
        real = V / cpi_real_factor(sc, 2050)
        bnoi = B_noi(sc, 2050)["noi"]
        sc_rows.append(dict(cells=[sc["name"], P(sc["cpi"], 1), P(sc["hpi"], 1), P(sc["rent_g"], 1), P(sc["r_at"], 1),
                                   M(V), M(real), M(d["be_live"] / 12), M(d["be_rent"] / 12), M(bnoi)],
                            st="assume", src=["S14", "S15"]))
    stab = table("bs", ["Scenario (2050 transfer)", "CPI", "Property value growth", "Rent growth", "Reinvest return",
                        "A market value 2050 (nominal)", "A value in 2026 dollars", "Avoided rent to live in A (a month)",
                        "Rent to rent out A (a month)", "B NOI 2050"],
                 sc_rows, note="These are stress cases, not forecasts. Each row changes only the assumptions listed; all other inputs are base. Property value growth in the slump case is -2% a year for 10 years, then 2%.")
    hist = table("hist", ["Year", "CPI-U Dec-to-Dec change", "Source"],
                 [dict(cells=[str(y), P(CPI_YOY[y], 1), "BLS Dec values " + f"{CPI_DEC[y-1]} to {CPI_DEC[y]}"], st="derived", src=["S15"]) for y in range(1973, 1983)],
                 note="Derived from the official BLS monthly CPI-U table (1982-84 = 100). Average 1972-1982 Dec-to-Dec: " + P(CPI_AVG_72_82, 1) + " a year.")
    body = f"""
<h2>Why a 50-year plan needs black-swan cases</h2>
<p>Inflation, home prices, rents, insurance and interest rates do not move in a straight line. The Fed targets 2% inflation (S14), but actual inflation has run far above target for stretches. The BLS table shows that the December-to-December change in consumer prices was above 8% in five of the nine years from 1973 to 1981 (S15).</p>
<h2>What past inflation looked like</h2>
{hist}
<h2>Stress scenarios, 2050 transfer</h2>
{stab}
<h2>Shocks that are not in the numbers above</h2>
{table("shocks", ["Shock", "What it would change"], [
    dict(cells=["Step-up in basis repealed for inherited property", "Heir would owe tax on gains since the original purchase, not since death. Original cost of both properties is unknown, so the effect cannot be sized.", "Proposed only (secondary source). Verify on congress.gov"], st="unverified", src=["S23", "S22"]),
    dict(cells=["Federal exclusion cut back (for example, to about half, as the 2017 law had scheduled)", "Estates above the exclusion could owe 40% tax on the excess. Not applicable to the known estate at owner values.", "Replaced for 2026 by a $15,000,000 exclusion. Permanence per secondary sources; verify the statute"], st="verified", src=["S01", "S22"]),
    dict(cells=["Prop 19 parent-child exclusion narrowed or removed", "Heir would face market-value tax even if living in A.", "No pending bill verified in this review. Check leginfo and the BOE before any decision"], st="unverified", src=["S08"]),
    dict(cells=["Insurance cost or availability shock", "Premiums or availability could change; FAIR Plan is the insurer of last resort", "Modelled as 10% growth in one case. Not verified"], st="unverified", src=["S17"]),
    dict(cells=["Solar credit disappears", "Owner reports a credit of about $10-$20 a month; base case already assumes $0 net", "Credits depend on PG&E terms. Not verified"], st="unverified", src=["S16"]),
    dict(cells=["Major wildfire or earthquake loss", "Uninsured loss or non-renewal; property value effect", "Not modelled; no verified loss estimate in this review"], st="unverified", src=["S17"]),
    dict(cells=["Slump in Bay Area values or rents", "Lower value and rent; higher vacancy", "Modelled as the slump case (value -2% a year for 10 years)"], st="assume", src=["S14"]),
])}
<p class="note">The 1970s case is an illustration of a high-inflation decade, not a forecast. The historical figures are from the BLS table; the scenario assumptions are not sourced.</p>
"""
    files["black-swans.html"] = page("black-swans.html", "Black-swan economics", body,
                                     lede="Stress cases for 50 years: stagflation, slump, deflation, insurance shock and rule change. Use them to test the decision, not to predict it.")

    # ---------------- TRUST PROCESS
    steps = [
        ("1", "Date of death", "Change in ownership occurs on the date of death, even if distribution to the heir is later. Reassessment is measured from that date.", "S10", "verified"),
        ("2", "Within 150 days", "The trustee (or transferee) files BOE-502-D with the county assessor for each parcel.", "S10", "verified"),
        ("3", "Claim the parent-child exclusion", "File BOE-19-P if the heir qualifies. Occupancy must start within one year of the death. Claim within three years or before any transfer to a third party.", "S08, S10", "verified"),
        ("4", "Homeowners' exemption", "If the heir occupies the home as a principal residence, file for the $7,000 homeowners' exemption within one year of transfer.", "S08, S11", "verified"),
        ("5", "Federal estate tax check", "Form 706 is needed only if the gross estate exceeds $15,000,000 in 2026 (S02). Estimate the total estate before the filing deadline.", "S02", "verified"),
        ("6", "Mailing address and bills", "Ask the assessor to update the tax-bill address. Santa Clara: first installment due 1 Nov, delinquent after 10 Dec; second due 1 Feb, delinquent after 10 Apr (S12).", "S10, S12", "verified"),
        ("7", "Supplemental bill", "A reassessment after transfer can produce a supplemental bill. Budget for it (S12, S13).", "S12, S13", "verified"),
        ("8", "Decide live, rent or sell", "Living keeps the exclusion; renting loses it; selling triggers the sale analysis (basis is value at death, S05).", "S08, S05", "verified"),
        ("9", "Trust income tax", "The trust may owe income tax on income it keeps. Brackets are compressed: 37% above $16,000 of taxable income in 2026 (S03).", "S03", "verified"),
        ("10", "Insurance and utilities", "Move insurance and utilities into the heir's name. Insurance premium, water provider and solar terms are not verified; get quotes (S17, S16).", "S17, S16", "unverified"),
    ]
    rows = [dict(cells=[n, f"<b>{t}</b>", d], st=st, src=s.split(", ")) for n, t, d, s, st in steps]
    tp = table("proc", ["Step", "Action", "What to do"], rows,
               note="Deadlines are as stated by the BOE and IRS. The 'unverified' step covers items not checked against an official source. This is a checklist, not legal advice.")
    body = f"""
<h2>How the trust inheritance of Property A would run</h2>
<p>Steps are in the order they usually occur. Each row shows the official source and whether it was verified.</p>
{tp}
<h2>Key dates</h2>
{table("dates", ["Date", "Event"], [
    dict(cells=["Any time", "Trust distributes Property A to the heir (date not yet known)"], st="missing", src=["S10"]),
    dict(cells=["Within 150 days of death", "File BOE-502-D"], st="verified", src=["S10"]),
    dict(cells=["Within 1 year of death", "Heir occupies the home; file homeowners' exemption within 1 year of transfer"], st="verified", src=["S08", "S10"]),
    dict(cells=["Within 3 years, or before sale", "File the exclusion claim"], st="verified", src=["S08"]),
    dict(cells=["1 Nov (year of tax bill)", "First installment due, Santa Clara"], st="verified", src=["S12"]),
    dict(cells=["10 Dec", "First installment delinquent after this date (Santa Clara); SF first installment has the same date"], st="verified", src=["S12", "S13"]),
    dict(cells=["Feb 2027", "Next Prop 19 add-on adjustment"], st="verified", src=["S09"]),
])}
"""
    files["trust-process.html"] = page("trust-process.html", "Trust inheritance steps", body,
                                       lede="The inheritance of Property A, step by step, with the official rule behind each step.")

    # ---------------- QUESTIONS
    qs = [
        ("Q01", "Does the parent-child exclusion keep the tax low if the heir moves in?", "answered", "Yes, if the home becomes a principal residence within one year and the claim is filed (S08, S10).", "Confirm the heir's plan and dates with an attorney.", ["S08", "S10"]),
        ("Q02", "Does renting Property A keep the exclusion?", "answered", "No. The exclusion covers principal residences only (S08).", "None needed unless the plan changes.", ["S08"]),
        ("Q03", "Does the heir pay federal estate tax?", "answered", "No. The estate tax is on the decedent's estate (S04). The heir pays income tax on income and any gain after death.", "None.", ["S04", "S05"]),
        ("Q04", "What is the federal exclusion?", "answered", "$15,000,000 per person for 2026 deaths (S01, S02). Indexed for inflation from 2027 (secondary: verify S22).", "Watch for the IRS 2027 figure.", ["S01", "S02"]),
        ("Q05", "Does California impose an estate or inheritance tax?", "answered", "No (S07).", "None.", ["S07"]),
        ("Q06", "What is the decedent's total estate?", "missing", "Unknown. Only the two properties are listed, at owner estimates.", "Full asset and debt inventory (suggestion G04).", ["S02"]),
        ("Q07", "What are the current market values of A and B?", "missing", "Owner estimates only: " + M(A_MV0) + " and " + M(B_MV0) + ".", "Licensed appraisals (G02).", ["S08"]),
        ("Q08", "What exact tax rate does the Santa Clara bill use for the parcel?", "partial", "Rule: 1% plus voter bonds (S12). Owner-implied rate " + P(A_RATE, 3) + ". Exact rate not verified.", "Pull the bill (G01).", ["S12"]),
        ("Q09", "Why does Property B's billed tax exceed the SF rate?", "missing", "Billed tax is about " + P(B_RATE_BILLED, 2) + " of assessed value; the published FY 2026-27 rate is " + P(SF_RATE_FY2627, 2) + " (S13).", "Ask for the itemised bill and assessor record (G01).", ["S13"]),
        ("Q10", "Does the homeowners' exemption apply to Property B's owner-occupied unit?", "partial", "The exemption is for owner-occupied principal residences; rentals do not qualify (S11). Multi-unit treatment not verified.", "Ask the assessor (G01).", ["S11"]),
        ("Q11", "What will homeowners insurance cost for A and B?", "missing", "Owner estimate " + M(A_INS) + " a year each. CDI publishes data, not a per-property average on the page read (S17, S18).", "Quotes (G03).", ["S17", "S18"]),
        ("Q12", "Who supplies water for Property A, and at what rate?", "missing", "Not confirmed. Owner range $100-$150 a month (unverified).", "Water bills (G04).", ["S20"]),
        ("Q13", "Is there really a solar credit of $10-$20 a month?", "missing", "PG&E credits depend on generation and use (S16). Owner's figure not verified.", "12 months of PG&E statements (G04).", ["S16"]),
        ("Q14", "What is the comparable rent for Property A?", "missing", "Unknown. This single number decides the living-versus-selling question.", "Rental study or appraiser (G06).", ["S08"]),
        ("Q15", "What does upkeep cost on each property?", "missing", "No source. Model assumes 0.5% of value for A and 5% of gross rent for B.", "Twelve months of invoices (G04).", ["S08"]),
        ("Q16", "What return can the proceeds earn after tax?", "partial", "Assumption only (4%). Three cases tested.", "Adviser's after-tax return range (G08).", ["S11"]),
        ("Q17", "When does the trust distribute the property?", "missing", "Unknown. Reassessment is from death regardless (S10).", "Trust document review (G05).", ["S10"]),
        ("Q18", "What is the heir's income tax position?", "missing", "Unknown. Needed for income tax on rent and investment income.", "CPA input (G08).", ["S03"]),
        ("Q19", "What is the original cost of each property?", "missing", "Unknown. Needed only if step-up were repealed (S23, secondary).", "Purchase records (G04).", ["S05"]),
        ("Q20", "Is there any debt on either property?", "missing", "No debt supplied. None modelled.", "Confirm (G04).", ["S02"]),
        ("Q21", "Is the third unit of Property B legally rentable, and what are the rent limits?", "missing", "Rent-increase rules were not verified in this review.", "City rent-rules check (G01).", ["S13"]),
        ("Q22", "Will any pending law change the answer?", "partial", "Verified: no pending change to Prop 19 found. Proposals to end step-up exist (secondary). Prop 40 does not reach these asset levels (S21).", "Law watch review each quarter.", ["S21", "S23"]),
        ("Q23", "What is the 2027 federal exclusion?", "missing", "Not yet published by the IRS in the sources reviewed (F07).", "Check the IRS in late 2026 or early 2027.", ["S01"]),
    ]
    qrows = [dict(cells=[qid, f"<b>{q}</b>", a, nx], st=st, src=src) for qid, q, st, a, nx, src in qs]
    qt = table("qa", ["ID", "Question", "What we know", "What would close it"], qrows)
    body = f"""
<h2>Questions, answers and gaps</h2>
<p>Each question shows its status. 'Answered' means the rule is settled by a source on this site; the facts still need to be supplied. 'Missing' means no source or owner input settles it yet.</p>
{qt}
"""
    files["questions.html"] = page("questions.html", "Questions and gaps", body,
                                   lede="What must be answered before a decision can reasonably be made, what we already know, and how to close each gap.")

    # ---------------- SUGGESTIONS
    sg = [
        ("G01", "Pull official records for both parcels", "Request the Santa Clara and San Francisco assessor and tax-collector records: assessed values, exemptions, itemised bills, rate areas, unit count.", "Closes Q08, Q09, Q10, Q21. Confirms the owner figures.", "Option A: self-request (free, slower). Option B: a title or tax service (fee, faster)."),
        ("G02", "Commission appraisals for A and B", "A licensed appraisal gives a market value to replace owner estimates; it also sets the base for any sale analysis.", "Closes Q07. Required for the sell path.", "Option A: one appraisal for A (larger cost, most decision value). Option B: both (more cost)."),
        ("G03", "Get insurance quotes for both properties", "Three quotes each (owner-occupied for A; landlord policy for B). Use CDI's shopping tools.", "Closes Q11; tests the $1,500 estimate.", "Option A: quotes now. Option B: wait until transfer."),
        ("G04", "Keep a 12-month utility and cost ledger", "Water, power and upkeep for both properties, plus solar statements and debt and purchase records.", "Closes Q12, Q13, Q15, Q19, Q20.", "Option A: a spreadsheet kept by the owner. Option B: a bookkeeper's monthly review."),
        ("G05", "Review the trust document with an estate attorney", "Confirm distribution timing, occupancy requirement, and whether the trust can hold the home until the heir moves in.", "Closes Q17, Q01 in practice.", "Option A: one-off review. Option B: ongoing trust administration."),
        ("G06", "Get a comparable-rent study for A", "A rental study or broker opinion gives the number that decides living versus selling.", "Closes Q14. Moves the answer from a threshold to a decision.", "Option A: broker opinion (low cost). Option B: appraiser's rent analysis (more defensible)."),
        ("G07", "Choose a privacy boundary for this site", "Option A (current): owner figures rounded to $10 and labelled, no identifiers. Option B (stricter): remove all owner figures and keep only rules and formulas. Option A keeps the decision usable; Option B removes numbers that might be sensitive.", "Changes what appears on every page.", "Choose A or B."),
        ("G08", "Add income tax and an investment plan", "Add the heir's tax brackets (federal and California), tax on rent and on investment income, and an after-tax return range from a CPA or adviser.", "Closes Q16, Q18. Makes the reinvestment comparison realistic.", "Option A: adviser input now. Option B: keep the simple after-tax assumption and show a range."),
        ("G09", "Review the three assumptions that drive the answer", "Reinvestment return, property growth, and upkeep. Test each at a pessimistic and an optimistic value before deciding.", "No new data needed.", "Option A: accept the base case. Option B: adopt the scenario bands on the black-swan page."),
        ("G10", "Reconcile the other decision pages in this repository", "Other published pages in this repository show different figures for the same items (flag F09). Pick one source of truth.", "Removes conflicting numbers.", "Option A: point all pages to this desk. Option B: keep them as archive and label them."),
        ("G11", "Set a review calendar", "Recheck the Prop 19 add-on (Feb 2027), the IRS 2027 exclusion, and the law watch each quarter.", "Keeps the answer current.", "Option A: quarterly. Option B: annual, before any transfer."),
    ]
    srows = [dict(cells=[gid, f"<b>{t}</b>", d, u, opt], st="pending", src=["S08"]) for gid, t, d, u, opt in sg]
    sgt = table("sug", ["ID", "Suggestion", "What it involves", "What it unlocks", "Options for you to choose"], srows,
                note="Nothing on this list has been implemented. Reply with the IDs and option letters you want, and the site will be changed to match.")
    body = f"""
<div class="callout">
<p><b>For your review.</b> These suggestions improve the decision process. None changes the site until you choose. Pick any combination; the default is to do nothing.</p>
</div>
{sgt}
<h2>Site improvements (also for review)</h2>
<ul>
<li><b>W01</b> Export each table to a spreadsheet (small build change).</li>
<li><b>W02</b> Add an input panel so you can change the assumptions on the Scenarios page (medium build change).</li>
<li><b>W03</b> Add a change log showing each figure's date and source (small).</li>
<li><b>W04</b> Merge the duplicate desks in this repository into one site (medium; touches other sessions' files).</li>
</ul>
"""
    files["suggestions.html"] = page("suggestions.html", "Suggestions (for your choice)", body,
                                     lede="Options to improve the decision process. Review them and choose before anything is implemented.")

    # ---------------- LAW WATCH
    law = [
        ("L01", "Proposition 19 (2020): parent-child exclusion limited to principal residences; reassessment on transfer", "In effect", "S08", "verified"),
        ("L02", "Prop 19 add-on adjusted to $1,044,586 for transfers 16 Feb 2025 to 15 Feb 2027", "In effect; next adjustment Feb 2027", "S09", "verified"),
        ("L03", "Solar new-construction exclusion, scheduled to sunset 1 Jan 2027 (as stated in BOE Pub 29, 2025 edition)", "Status not verified; check before relying on it", "S11", "unverified"),
        ("L04", "Federal basic exclusion $15,000,000 for 2026 (Working Families Tax Cuts Act, P.L. 119-21)", "Enacted; statute indexes it from 2027", "S01, S22", "verified"),
        ("L05", "Estate Tax Closing Letter fee rises from $56 to $76 for requests on or after 26 Oct 2026", "Enacted by Treasury Decision 10055", "S01", "verified"),
        ("L06", "Proposition 40 (Nov 3, 2026): one-time 5% tax on assets over $1 billion", "On ballot; does not reach these asset levels", "S21", "verified"),
        ("L07", "STEP Act (2025 proposal): would end step-up in basis and raise estate tax", "Proposal only; not law. Secondary source, bill status not verified", "S23", "unverified"),
        ("L08", "Step-up in basis (IRC 1014): unchanged by current law", "In effect", "S05", "verified"),
        ("L09", "Federal top estate rate 40%", "In effect", "S04", "verified"),
    ]
    lrows = [dict(cells=[i, t, s], st=st, src=src.split(", ")) for i, t, s, src, st in law]
    lt = table("law", ["ID", "Change or proposal", "Status"], lrows,
               note="Status as of 13 Nov 2026 based on the sources read. Check congress.gov and leginfo.legislature.ca.gov before acting. No pending change to Prop 19 was verified in this review.")
    body = f"""
<h2>Laws and proposals that could change the decision</h2>
{lt}
<h2>What would change the answer</h2>
<ul>
<li><b>Repeal of step-up in basis:</b> would add capital-gains tax to sales of inherited property. Basis of both properties is unknown, so it cannot be sized (Q19).</li>
<li><b>Narrowing of Prop 19:</b> would remove the reason to live in A for tax reasons. Verified no bill found.</li>
<li><b>Lower federal exclusion:</b> does not reach a known estate at owner values; matters only if the decedent holds more assets.</li>
</ul>
"""
    files["law-watch.html"] = page("law-watch.html", "Law watch", body,
                                   lede="Enacted changes, dated deadlines and proposals that could change the answer.")

    # ---------------- SOURCES
    srows = []
    for sid, s in SRC.items():
        srows.append(dict(cells=[sid, s["title"], s["publisher"], STATUS_LABEL.get(s["status"], s["status"])],
                          st="verified" if s["status"] == "read" else "unverified",
                          src=[sid]))
    st_ = table("src", ["ID", "Source (what it supports)", "Publisher", "What was done with it"], srows,
                note="Every link was opened or identified on 13 Nov 2026. 'Index only' means the page was read for the rule it states but the figures were not extracted; those figures are not used. 'Secondary' links are not official and appear only to flag proposals.")
    body = f"""
<h2>Official source register</h2>
<p>Each source has an ID used in the tables. Check the links yourself: the verification of a figure is only as good as the page it is read from.</p>
{st_}
"""
    files["sources.html"] = page("sources.html", "Source register", body,
                                 lede="Every official source used, with what was read on each. Use the links to check any figure yourself.")

    # ---------------- FLAGGED
    flags = [
        ("F01", "Owner figures (values, assessed values, tax bills, rent, utilities, insurance) are unverified", "Rounded to $10 and shown with owner-input status. Blank in the verified rules tables. Verify through G01 and G02.", "S12, S13", "owner"),
        ("F02", "Property B's billed tax is about " + P(B_RATE_BILLED, 2) + " of assessed value; the published FY 2026-27 SF rate is " + P(SF_RATE_FY2627, 4) + " (S13)", "Likely includes charges beyond the basic rate, but this is not confirmed. The model uses the billed amount, grown at the assessed-value rate. Review the itemised bill.", "S13, S11", "unverified"),
        ("F03", "Santa Clara parcel rate not verified; owner-implied rate " + P(A_RATE, 3) + " used", "Rule (1% plus bonds) verified; the parcel's bonds and charges were not. Check the bill.", "S12", "unverified"),
        ("F04", "Insurance estimate ($1,500 per property per year) not verified", "CDI's data workbook (S24) was not extracted; no per-property average was found on the pages read.", "S17, S18, S24", "unverified"),
        ("F05", "Water provider for Property A not confirmed", "San Jose Water's CPUC filing (S20) is context only. SFPUC covers Property B's water schedule (S19), not extracted.", "S19, S20", "unverified"),
        ("F06", "Solar credit for A ($10-$20 a month) not verifiable", "PG&E describes how credits work but gives no amount (S16). Base case uses $0. Solar exclusion sunset (1 Jan 2027, S11) status not verified.", "S16, S11", "unverified"),
        ("F07", "Federal exclusion for 2027 and later not yet published", "Statute indexes it from 2027; the IRS figure was not found in the sources read. Projections use a 2% assumption and are labelled.", "S01", "unverified"),
        ("F08", "Prop 19 add-on held flat in projections", "BOE adjusts it every other February (S09). Holding it flat understates later taxable value on a qualifying transfer, so this is conservative for the living case.", "S09", "assume"),
        ("F09", "Other pages in this repository disagree with official figures", "Checked against IRS sources: a page shows the 2026 estates-and-trusts capital-gains figure as $16,200; IRS Rev. Proc. 2025-32 gives $16,250 (S03). Another page shows the estate closing-letter fee as rising from $67; IRS says from $56 to $76 (S01). These are noted for those pages' owners.", "S03, S01", "unverified"),
        ("F10", "Homeowners' exemption on a multi-unit building not verified", "Rule: owner-occupied principal residence; rentals excluded (S11). How it applies to one owner-occupied unit in a three-unit building needs the assessor's answer.", "S11", "unverified"),
        ("F11", "Upkeep and selling costs are assumptions with no source", "0.5% of value for A, 5% of gross rent for B, 6% selling costs. They are labelled and can be changed.", "S08", "assume"),
        ("F12", "Property B rent and rent rules not verified", "Owner rent $7,150 a month for two units. Rent-increase rules for San Francisco were not checked in this session.", "S13", "unverified"),
        ("F13", "Income tax on rent and investment income not modelled", "Would reduce every path. Needs the heir's tax position (Q18).", "S03", "unverified"),
        ("F14", "Date of trust distribution unknown", "Reassessment uses the date of death regardless (S10); the distribution date affects the claim timing and the cash flow.", "S10", "unverified"),
        ("F15", "Step-up repeal and STEP Act are proposals from a secondary source", "Not verified against the bill text on congress.gov (S22). Not in the base case.", "S23, S22", "unverified"),
        ("F16", "Earlier privacy exposure in this repository", "Other sessions' published or committed files contain owner-derived amounts (see their records). This session did not delete or rewrite them; removal is a repository decision (G07).", "", "unverified"),
    ]
    frows = [dict(cells=[i, t, d], st=st, src=(src.split(", ") if src else ["S01"])) for i, t, d, src, st in flags]
    ft = table("flag", ["ID", "Irregularity or unverified item", "Detail and what to check"], frows,
               note="Flagged items do not block use of the verified rules. Each row links to the official source to check manually.")
    body = f"""
<div class="callout"><p><b>Flagged for review.</b> These items are unverified, irregular, or assumed. They are listed so you can review them and request changes. None blocks the site.</p></div>
{ft}
"""
    files["flagged.html"] = page("flagged.html", "Flagged for review", body,
                                 lede="Irregularities, unverified owner figures and assumptions, with links for manual review.")
    return files


def write(files):
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    for name, content in files.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(content)
    print("wrote", len(files), "pages to", OUT)


if __name__ == "__main__":
    write(build())
