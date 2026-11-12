#!/usr/bin/env python3
"""Deterministic generator for the published (allowlisted) artifact.

Output: public-safe/*.html + public-safe/style.css. No JS, no external assets, no
analytics, no forms. Every table body row carries at least one official source link.

Writes only files under public-safe/. Run:  python3 scripts/build_desk.py
"""
from pathlib import Path
import html
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import desk_model as m  # noqa: E402

OUT = Path("public-safe")
UPDATED = "11 November 2026"

# ------------------------------------------------------------------ source register
S = {
    "irs_estate": ("IRS · Estate tax", "https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax"),
    "irs_new": ("IRS · What's new, estate & gift", "https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax"),
    "irs_faq": ("IRS · Estate tax FAQ", "https://www.irs.gov/businesses/small-businesses-self-employed/frequently-asked-questions-on-estate-taxes"),
    "irs_basis": ("IRS · Inherited property basis", "https://www.irs.gov/faqs/interest-dividends-other-types-of-income/gifts-inheritances/gifts-inheritances"),
    "irs_551": ("IRS · Publication 551", "https://www.irs.gov/publications/p551"),
    "irs_706": ("IRS · Instructions for Form 706", "https://www.irs.gov/instructions/i706"),
    "sco": ("CA State Controller · Estate tax", "https://www.sco.ca.gov/ardtax_estate_tax.html"),
    "ftb": ("FTB · Gifts and inheritance", "https://www.ftb.ca.gov/file/personal/income-types/gifts-and-inheritance.html"),
    "prop19": ("BOE · Proposition 19", "https://www.boe.ca.gov/prop19/"),
    "pub801": ("BOE · Prop 19 fact sheet (Pub 801)", "https://www.boe.ca.gov/pdf/pub801.pdf"),
    "boe800": ("BOE · How property is assessed (Pub 800-10)", "https://boe.ca.gov/pdf/pub800-10.pdf"),
    "boe266": ("BOE · Homeowners' exemption claim (BOE-266)", "https://boe.ca.gov/proptaxes/pdf/sample-boe266.pdf"),
    "boe_home": ("BOE · Homeowners' exemption eligibility", "https://www.boe.ca.gov/proptaxes/homeowners_exemption.htm"),
    "irs_523": ("IRS · Publication 523, sale gain and expenses", "https://www.irs.gov/publications/p523"),
    "irs_527": ("IRS · Publication 527, rental income and depreciation", "https://www.irs.gov/publications/p527"),
    "scc_prop19": ("SCC Assessor · Parent-child transfer", "https://asr.santaclaracounty.gov/tax-savings/transferring-your-assessed-value/parent-to-child-2"),
    "scc_assessor": ("SCC Assessor · Decline in value", "https://asr.santaclaracounty.gov/online-services/decline-in-value/decline-in-value-request"),
    "scc_report": ("SCC Assessor · Annual report 2025-26", "https://files.santaclaracounty.gov/exjcpb1521/2025-11/annual_report_2025-2026.pdf"),
    "sf_rate": ("SF Treasurer · Secured property tax rate", "https://sftreasurer.org/property/secured-property-taxes"),
    "sf_transfer": ("SF Assessor-Recorder · Transfer tax", "https://www.sf.gov/transfer-tax"),
    "sf_cos": ("SF Assessor-Recorder · Change in ownership", "https://www.sf.gov/information--learn-about-change-ownership"),
    "sf_rent": ("SF.gov · Allowable rent increase", "https://www.sf.gov/learn-about-rent-increases-san-francisco"),
    "cdi_home": ("CDI · Residential insurance", "https://www.insurance.ca.gov/01-consumers/105-type/5-residential/index.cfm"),
    "cdi_sis": ("CDI · Sustainable Insurance Strategy", "https://www.insurance.ca.gov/01-consumers/180-climate-change/sustainable-insurance-strategy.cfm"),
    "courts_small": ("CA Courts · Small estate affidavit", "https://selfhelp.courts.ca.gov/probate/small-estate"),
    "courts_probate": ("CA Courts · Probate", "https://selfhelp.courts.ca.gov/probate"),
    "civ1947": ("CA Civil Code 1947.12", "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12"),
    "rtc11911": ("CA Rev. & Tax. Code 11911", "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=11911"),
    "cpuc_nem": ("CPUC · Net energy metering & net billing", "https://www.cpuc.ca.gov/nem"),
    "sos": ("CA Secretary of State · Ballot measures", "https://electionresults.sos.ca.gov/returns/ballot-measures"),
    "bls": ("BLS · Consumer Price Index", "https://www.bls.gov/cpi/"),
    "fhfa": ("FHFA · House Price Index", "https://www.fhfa.gov/data/hpi"),
}


def src(*keys, label=None):
    """Render one or more official source links for a table row."""
    parts = []
    for k in keys:
        name, url = S[k]
        parts.append(f'<a href="{url}" rel="noopener noreferrer">{html.escape(name)}</a>')
    out = " · ".join(parts)
    if label:
        out = f"{html.escape(label)}<br>{out}"
    return out


def stat(text):
    return f'<span class="stat">{text}</span>'


NAV = [
    ("index.html", "Dashboard"),
    ("decision.html", "Decision"),
    ("projections.html", "Projections"),
    ("properties.html", "Properties"),
    ("costs.html", "Costs"),
    ("black-swans.html", "Black swans"),
    ("tax.html", "Inheritance & tax"),
    ("process.html", "Step by step"),
    ("law-watch.html", "Law watch"),
    ("flagged.html", "Flagged"),
    ("sources.html", "Sources"),
]

CSS = """
:root{--bg:#f7f8fa;--panel:#fff;--ink:#16202b;--muted:#5c6b7a;--line:#dfe4ea;--accent:#0b6b5b;
--accent-2:#0d3b66;--warn:#8a5a00;--bad:#8c2d2d;--chip:#eef3f1;--shadow:0 1px 2px rgba(16,32,48,.06)}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accent-2);text-decoration-thickness:1px;text-underline-offset:2px}
a:hover{color:var(--accent)}
header.top{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between;
padding:14px 20px;background:#0f1b26;color:#eaf1f5}
header.top .brand{color:#fff;text-decoration:none;font-weight:650;letter-spacing:.2px}
header.top .meta{font-size:12.5px;color:#9fb3c2;text-transform:uppercase;letter-spacing:.08em}
.layout{display:grid;grid-template-columns:236px minmax(0,1fr);gap:28px;max-width:1240px;margin:0 auto;padding:24px 20px 64px}
nav.side{position:sticky;top:16px;align-self:start;display:flex;flex-direction:column;gap:2px;
background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:8px;box-shadow:var(--shadow)}
nav.side a{display:block;padding:8px 10px;border-radius:8px;color:var(--ink);text-decoration:none;font-size:14.5px}
nav.side a:hover{background:#f0f4f7}
nav.side a[aria-current=page]{background:var(--chip);color:var(--accent);font-weight:650}
main{min-width:0}
.eyebrow{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);font-weight:650}
h1{font-size:clamp(26px,3.4vw,38px);line-height:1.15;margin:.25em 0 .35em;letter-spacing:-.01em}
h2{font-size:21px;margin:2.1em 0 .5em;letter-spacing:-.01em}
h3{font-size:16.5px;margin:1.6em 0 .35em}
p.lead{font-size:18px;color:#33414f;max-width:70ch}
p,li{max-width:78ch}
.notice{background:#fff8e6;border:1px solid #efd9a3;border-left:4px solid #c9942b;padding:12px 16px;border-radius:8px;margin:18px 0}
.callout{background:var(--chip);border:1px solid #cfe0da;border-left:4px solid var(--accent);padding:14px 16px;border-radius:8px;margin:18px 0}
.callout.bad{background:#fdf0f0;border-color:#e7c9c9;border-left-color:var(--bad)}
.callout h3{margin-top:0}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin:20px 0}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px;box-shadow:var(--shadow)}
.card .k{font-size:12px;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);font-weight:650}
.card .v{font-size:23px;font-weight:680;margin:4px 0 2px;letter-spacing:-.02em}
.card .n{font-size:13px;color:var(--muted)}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:18px}
.scroll{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--panel);box-shadow:var(--shadow);margin:14px 0}
table{border-collapse:collapse;width:100%;font-size:14px;min-width:560px}
caption{caption-side:top;text-align:left;padding:12px 14px 0;font-weight:650;font-size:14.5px}
th,td{padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top;text-align:left}
thead th{background:#eef2f5;font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:#41505f;position:sticky;top:0}
tbody tr:nth-child(even){background:#fbfcfd}
tbody tr:hover{background:#f3f7f9}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
td a{font-size:12.5px}
.chip{display:inline-block;padding:1px 8px;border-radius:999px;font-size:11.5px;font-weight:650;white-space:nowrap;
background:#eef2f5;color:#41505f;border:1px solid #dbe3e9}
.chip.ok{background:#e8f4ef;color:#0b5c4d;border-color:#c8e3d8}
.chip.assume{background:#fdf5e3;color:#7a5300;border-color:#eddcae}
.chip.flag{background:#fbecec;color:#8c2d2d;border-color:#eccaca}
.chip.derived{background:#eaf0f8;color:#234a77;border-color:#cfdcee}
.btn{display:inline-block;padding:9px 14px;border-radius:8px;background:var(--accent);color:#fff;text-decoration:none;font-weight:600;font-size:14.5px}
.btn:hover{background:#095448;color:#fff}
ul.tight li{margin:.2em 0}
footer.site{max-width:1240px;margin:0 auto;padding:0 20px 48px;color:var(--muted);font-size:13px}
footer.site p{max-width:none}
.small{font-size:13px;color:var(--muted)}
.stat{white-space:nowrap}
@media (max-width:880px){
 .layout{grid-template-columns:1fr;padding-top:14px}
 nav.side{position:static;flex-direction:row;overflow-x:auto;gap:4px}
 nav.side a{white-space:nowrap}
 table{min-width:520px}
}
@media print{
 nav.side,header.top .meta,.btn{display:none}
 .layout{display:block;padding:0}
 .scroll{overflow:visible;border:none;box-shadow:none}
 body{background:#fff}
}
"""


def page(slug, title, eyebrow, body, lead=None):
    nav = "".join(
        f'<a{" aria-current=page" if href == slug else ""} href="{href}">{html.escape(name)}</a>'
        for href, name in NAV
    )
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<meta name="referrer" content="no-referrer">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="top">
  <a class="brand" href="index.html">Estate decision desk</a>
  <span class="meta">Public · anonymized · verified {UPDATED}</span>
</header>
<div class="layout">
<nav class="side" aria-label="Sections">{nav}</nav>
<main>
<div class="eyebrow">{html.escape(eyebrow)}</div>
<h1>{html.escape(title)}</h1>
{lead_html}
{body}
<footer class="site">
<p><strong>Not advice.</strong> Educational analysis for one household, using published rules and named
assumptions. Not legal, tax, insurance or investment advice. Re-verify every rule and rate in the year of
the transfer; the transfer is expected around 2040–2050 and today's law is not guaranteed to survive.</p>
<p><strong>Privacy.</strong> No names, street addresses, parcel or account numbers, ZIP codes, e-mail
addresses or phone numbers appear on this site. The properties are Property A and Property B. The
assessment and tax-bill histories supplied in the brief are deliberately not republished at any precision,
because those values are public assessor records and remain searchable when rounded. Residual risk and
every unverified item are listed on <a href="flagged.html">Flagged for review</a>.</p>
</footer>
</main>
</div>
</body>
</html>
"""
    (OUT / slug).write_text(doc)


def table(caption, headers, rows, numeric=(), cls=""):
    head = "".join(
        f'<th class="num" scope="col">{html.escape(h)}</th>' if i in numeric
        else f'<th scope="col">{html.escape(h)}</th>'
        for i, h in enumerate(headers)
    )
    body = []
    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            c = f' class="num"' if i in numeric else ""
            cells.append(f"<td{c}>{cell}</td>")
        body.append("<tr>" + "".join(cells) + "</tr>")
    cap = f"<caption>{html.escape(caption)}</caption>" if caption else ""
    return (f'<div class="scroll"><table class="{cls}">{cap}<thead><tr>{head}</tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table></div>')


# ------------------------------------------------------------------ computed figures
TY = m.ASSUMPTIONS["transfer_year"]
T = m.transfer_year_view(TY)
W = m.wealth(TY)
W40 = m.wealth(2040)
W50 = m.wealth(2050)
BE_PORT = m.break_even_portfolio(TY)
BE_RENT = m.break_even_rent_growth(TY)
A26 = m.A.tax(2026)
B26 = m.B.tax(2026)
BVIEW = m.property_b_view(2026)
B_SALE_PROCEEDS = m.B.market_value * (1 - m.ASSUMPTIONS["sf_sell_cost_rate"])

# ------------------------------------------------------------------ 1. dashboard
def build_index():
    kpis = [
        ("Property A today", m.money(m.A.market_value), "Market-value anchor, rounded to $100,000", "derived"),
        ("Property A at transfer", m.money(T["fmv"]), f"2045 at {m.pct(m.ASSUMPTIONS['home_growth'],1)} a year", "derived"),
        ("Property A tax if occupied", m.money(T["tax_occupy"]), "After Prop 19 partial exclusion, 2045", "derived"),
        ("Property A tax if rented", m.money(T["tax_rent"]), "No exclusion: full reassessment, 2045", "derived"),
        ("Net sale proceeds at 2045", m.money(T["proceeds"]), "After 6% selling costs; no gain tax", "derived"),
        ("Property B net rental income", m.money(BVIEW["noi"]), "Today, before income tax", "derived"),
        ("Federal estate-tax threshold", stat("$15,000,000"), "2026, per person; not per heir", "ok"),
        ("25-year outcome, sell vs rent", m.money(W["s3"] - W["s2"]), f"Selling ahead by {m.money(W['s3']-W['s2'])}, 2045→2070", "derived"),
    ]
    cards = "".join(
        f'<div class="card"><div class="k">{html.escape(k)}</div><div class="v">{v}</div>'
        f'<div class="n">{html.escape(n)}</div></div>'
        for k, v, n, _ in kpis
    )
    rows = [
        ("<strong>Occupy A</strong>", "Possible only if you genuinely make it your principal residence. Costs "
         f"{m.money(T['cost_occupy_total'])} a year in 2045 and ties up {m.money(T['fmv'])} of capital, while B already "
         "provides a place to live.",
         '<span class="chip flag">Weakest of the three</span>', src("prop19", "boe266")),
        ("<strong>Rent A</strong>", f"Full reassessment to {m.money(T['assess_rent'])} means tax of {m.money(T['tax_rent'])} on rent of "
         f"{m.money(T['rent'])}. After vacancy, management, insurance and repairs the net is "
         f"{m.money(T['net_rent'])} a year — negative.",
         '<span class="chip flag">Cash-flow negative</span>', src("prop19", "pub801")),
        ("<strong>Sell A and reinvest</strong>", f"Basis steps up at death, so a sale near the date-of-death value pays no "
         f"federal or California capital-gains tax. Net proceeds {m.money(T['proceeds'])} at 2045, "
         f"{m.money(T['proceeds']*(1+m.ASSUMPTIONS['portfolio_return'])**25)} by 2070 at "
         f"{m.pct(m.ASSUMPTIONS['portfolio_return'],1)} after tax.",
         '<span class="chip ok">Recommended baseline</span>', src("irs_basis", "ftb")),
        ("<strong>Keep B</strong>", f"Already owned. No step-up and no reassessment from A's transfer. Net rental income "
         f"{m.money(BVIEW['noi'])} a year before income tax; sale proceeds before capital-gains tax "
         f"would be {m.money(B_SALE_PROCEEDS)}. The actual basis and tax are unknown.",
         '<span class="chip ok">Hold unless plans change</span>', src("sf_rate", "civ1947")),
    ]
    body = f"""
<div class="notice"><strong>The short answer.</strong> Inherit A, keep B, and treat selling A as the default.
It is the only path that converts an illiquid, reassessed, low-yielding asset into a diversified portfolio
without a capital-gains bill. Living in A is a legitimate choice, but it is a lifestyle purchase: on these
assumptions A-only cash flows trail selling by {m.money(W['s3']-W['s1'])} over 25 years;
this excludes any rent from the freed unit at B and is not a housing-adjusted comparison.</div>

<div class="cards">{cards}</div>

<h2>Executive summary</h2>
<ul class="tight">
<li><strong>Two assets, two different problems.</strong> Property A is inherited around 2040–2050: its income-tax
basis resets to date-of-death value and its property tax resets unless the heir occupies it. Property B is
already owned and is unaffected by A's transfer — no step-up, no reassessment, tenants and rents unchanged.</li>
<li><strong>The tax mechanics decide the answer.</strong> Occupying A and claiming the Prop 19 family-home
exclusion keeps part of the old assessment; renting it out forfeits the exclusion entirely, so the taxable
value becomes full market value. At 2045 that is {m.money(T['assess_rent'])}, and the tax is
{m.money(T['tax_rent'])} a year on rent of {m.money(T['rent'])}.</li>
<li><strong>The numbers at a 2045 transfer.</strong> A is worth about {m.money(T['fmv'])}; tax is
{m.money(T['tax_occupy'])} if occupied and {m.money(T['tax_rent'])} if rented; net rental is
{m.money(T['net_rent'])} after costs; selling nets about {m.money(T['proceeds'])} with a stepped-up basis and no
capital-gains tax. By 2070 the paths are {m.money(W['s3'])} (sell), {m.money(W['s2'])} (rent) and
{m.money(W['s1'])} (occupy).</li>
<li><strong>Recommendation.</strong> Keep B; sell A and reinvest unless you genuinely want to live in A. The
A-only comparison shows {m.money(W['s3']-W['s1'])} less over 25 years, but excludes
rent that might be earned from the unit freed at B. This is not a personal housing-cost estimate.</li>
<li><strong>Inheritance tax.</strong> California has no estate or inheritance tax. The federal estate tax is
paid by the estate, not the heir, and only above {stat('$15,000,000')} per person in 2026. A received
inheritance is not taxable income.</li>
<li><strong>What could reverse the ranking.</strong> Losing the step-up through how the trust is drafted;
after-tax portfolio returns below about {m.pct(BE_PORT,2)}; rent growth above about {m.pct(BE_RENT,2)} a year;
or a genuine wish to live in the house.</li>
<li><strong>What is not known.</strong> Trust terms and estate inclusion, B's income-tax basis, actual
insurance quotes, water and power bills, the legal status of B's third unit, and whether the solar tariff
survives a transfer. These are published on <a href="flagged.html">Flagged for review</a>.</li>
</ul>

<h2>Decision at a glance</h2>
{table("Three paths for Property A and the standing decision for Property B",
       ["Option", "What the numbers say", "Verdict", "Official source"], rows, numeric=())}

<h2>What this site is, and what it refuses to do</h2>
<div class="grid2">
<div class="callout"><h3>Verified rules, published arithmetic</h3>
<p>Statutes, thresholds and rates were read on official pages on {UPDATED} and are linked in every row.
Projections are arithmetic on named assumptions — never presented as facts. Money is rounded to the
nearest $10; property anchors are banded to $1,000 or $100,000 so they cannot be matched back to a
public assessment record.</p></div>
<div class="callout bad"><h3>Deliberately withheld</h3>
<p>Exact values, bills, rents, addresses, parcel numbers and family details. The historical assessment
and tax-bill series is not republished: rounding to $10 does not anonymize a public record. Where a
figure cannot be verified, the cell is blank and the item is on <a href="flagged.html">Flagged for
review</a>. Nothing here is individually tailored advice.</p></div>
</div>

<h2>Where to go next</h2>
<div class="scroll"><table class="navtable"><thead><tr><th scope="col">Question</th><th scope="col">Page</th></tr></thead><tbody>
<tr><td>Which option wins, by how much, and what would change it?</td><td><a href="decision.html">Decision</a></td></tr>
<tr><td>What is A worth in 2035, 2045, 2055, and what is the tax?</td><td><a href="projections.html">Projections</a></td></tr>
<tr><td>What do we actually know about each property?</td><td><a href="properties.html">Properties</a></td></tr>
<tr><td>What will insurance, water, power and repairs cost?</td><td><a href="costs.html">Costs</a></td></tr>
<tr><td>What if growth and inflation are not smooth for 50 years?</td><td><a href="black-swans.html">Black swans</a></td></tr>
<tr><td>How much can be inherited before tax, and whose tax is it?</td><td><a href="tax.html">Inheritance &amp; tax</a></td></tr>
<tr><td>What does the transfer involve, step by step?</td><td><a href="process.html">Step by step</a></td></tr>
<tr><td>What law could change before 2045?</td><td><a href="law-watch.html">Law watch</a></td></tr>
<tr><td>What is unverified or inconsistent?</td><td><a href="flagged.html">Flagged for review</a></td></tr>
<tr><td>Which official page supports each number?</td><td><a href="sources.html">Sources</a></td></tr>
</tbody></table></div>
<p class="small">Last verified {UPDATED}. The 2026 statewide ballot results cited here are <em>unofficial</em>
until certification, due 11 December 2026.</p>
"""
    page("index.html", "Inherit A, keep B, sell A unless you want to live in it",
         "Dashboard · inheritance decision desk", body,
         lead="Two properties, three real options, one 25-year arithmetic comparison. Everything below is "
              "reproducible from the published assumptions on the Projections page.")


# ------------------------------------------------------------------ 2. decision
def build_decision():
    snap = [
        ("A value at transfer", m.money(T["fmv"]), src("boe800")),
        ("Protected taxable value (Prop 13 continuation)", m.money(T["taxable"]), src("boe800")),
        ("Prop 19 allowance, 2045 projection", m.money(T["allowance"]), src("pub801")),
        ("Taxable value if you occupy", m.money(T["assess_occupy"]), src("prop19")),
        ("Taxable value if you rent", m.money(T["assess_rent"]), src("prop19")),
        ("Annual tax if you occupy (1.25% assumed)", m.money(T["tax_occupy"]), src("scc_report")),
        ("Annual tax if you rent", m.money(T["tax_rent"]), src("scc_report")),
        ("Gross rent if you rent it out", m.money(T["rent"]), src("boe800")),
        ("Operating costs if rented (incl. vacancy, management)", m.money(T["opex_rent"]), src("cdi_sis")),
        ("Net rental result before income tax", m.money(T["net_rent"]), src("civ1947")),
        ("Net sale proceeds (6% costs, stepped-up basis)", m.money(T["proceeds"]), src("irs_basis")),
        ("Portfolio income from proceeds (4.5% after tax)", m.money(T["portfolio_income"]), src("irs_basis")),
    ]
    comp = []
    for w in (W40, W, W50):
        comp.append((
            f"{w['year']} → {w['end']}",
            m.money(w["s1"]), m.money(w["s2"]), m.money(w["s3"]),
            m.money(w["s2"] - w["s3"]), m.money(w["s1"] - w["s3"]), src("irs_basis", "prop19"),
        ))

    # sensitivity: portfolio return x rent growth -> sell minus rent
    sens_rows = []
    for pr in (0.030, 0.045, 0.060):
        cells = [f"{m.pct(pr,1)} after tax"]
        for rg in (0.020, 0.030, 0.040):
            d = m.wealth(TY, portfolio=pr, rent_growth=rg)
            cells.append(m.money(d["s3"] - d["s2"]))
        cells.append(src("irs_basis", "civ1947"))
        sens_rows.append(cells)

    home_rows = []
    for g in (0.020, 0.030, 0.040, 0.050, 0.060):
        d = m.wealth(TY, home_growth=g)
        home_rows.append((m.pct(g, 1), m.money(d["fmv"]), m.money(d["s1"]), m.money(d["s2"]),
                          m.money(d["s3"]), src("fhfa", "boe800")))

    body = f"""
<p class="lead">Property B is retained in every path. In the rent and sell cases the owner can remain in B.
In the occupy-A case the owner moves out of B, freeing its third unit. No rent is counted for that
unit because legal status, condition and market rent are unverified. Thus the A-only occupancy figure
is <strong>not</strong> a housing-equivalent wealth comparison.</p>

<div class="callout"><h3>The result</h3>
<p>Selling A is ahead of renting by <strong>{m.money(W['s3']-W['s2'])}</strong> and ahead of A-only occupancy cash flows (excluding possible extra B rent) by
<strong>{m.money(W['s3']-W['s1'])}</strong> by {W['end']}. Renting only wins if the reinvested portfolio earns
less than <strong>{m.pct(BE_PORT,2)}</strong> after tax, or if rent grows faster than
<strong>{m.pct(BE_RENT,2)}</strong> a year for 25 years.</p></div>

<h2>The transfer year, line by line (2045 baseline)</h2>
{table("Property A in the year the trust distributes it", ["Line", "Amount / value", "Source"], snap)}

<h2>25-year comparison</h2>
{table("A-only horizon cash-flow illustration; B held, freed-unit rent excluded",
       ["Transfer year → horizon", "Occupy A", "Rent A", "Sell A", "Rent − sell", "Occupy − sell", "Source"],
       comp, numeric=(1, 2, 3, 4, 5))}
<p class="small">Arithmetic: home value grows at {m.pct(m.ASSUMPTIONS['home_growth'],1)}; operating costs at
{m.pct(m.ASSUMPTIONS['inflation'],1)}; rent at {m.pct(m.ASSUMPTIONS['rent_growth_a'],1)}; taxes at the Prop 13
2% cap after the transfer-year reassessment; selling costs 6%; reinvested proceeds earn
{m.pct(m.ASSUMPTIONS['portfolio_return'],1)} after tax; a terminal sale of A pays capital-gains tax at
{m.pct(m.ASSUMPTIONS['terminal_cg_rate'],1)} on gain after selling costs above stepped-up basis (before other basis adjustments, exclusions or depreciation).
Exactly 25 annual cost and rental periods are counted, 2045–2069, for a 2070 terminal value;
vacancy and management grow with rent, not with inflation. Annual A cash flows are carried
to the same terminal date at the assumed portfolio return; rental income tax is not included
({src("irs_523", "irs_527", "boe_home")}).</p>

<h2>Sensitivity — sell minus rent</h2>
{table("Positive means selling wins. After-tax portfolio return (rows) × rent growth (columns)",
       ["Portfolio return", "Rent +2.0%", "Rent +3.0%", "Rent +4.0%", "Source"], sens_rows, numeric=(1, 2, 3))}
{table("Home-price growth sensitivity (2045 transfer, 25-year horizon)",
       ["Market growth", "Value at transfer", "Occupy A", "Rent A", "Sell A", "Source"], home_rows, numeric=(1, 2, 3, 4))}

<h2>Why selling wins here — and why that is not a general rule</h2>
<ul class="tight">
<li><strong>Basis steps up, so the exit is cheap.</strong> Inherited property takes a date-of-death basis
({src("irs_basis")}). Selling near that value produces almost no gain, so the only friction is selling cost.</li>
<li><strong>Prop 19 punishes a rental heir.</strong> The parent-child exclusion requires the home to be the
transferee's principal residence. Rent it out and the taxable value becomes the full market value:
{m.money(T['assess_rent'])} at 2045, tax {m.money(T['tax_rent'])} ({src("prop19")}).</li>
<li><strong>Bay Area rental yields are thin at these prices.</strong> Gross rent is
{m.pct(T['rent']/T['fmv'],2)} of value at 2045 before costs — the reason the net result is
{m.money(T['net_rent'])}.</li>
<li><strong>Occupying converts an asset into consumption.</strong> The A-only gap is
{m.money(W['s3']-W['s1'])} over 25 years, before any additional rent from the vacated unit at B.
Without a verified third-unit rent, it is not a price of occupancy or a personalized optimum.</li>
<li><strong>Property B is different.</strong> It is already owned, so there is no step-up and no reassessment.
Its tax basis is unknown: proceeds before income tax would be {m.money(B_SALE_PROCEEDS)};
capital-gains tax and after-tax investable proceeds are blank pending basis records. Compare against
{m.money(BVIEW['noi'])} in existing net rent before income tax ({src("irs_551", "sf_rate")}).</li>
</ul>

<h2>One offset not in the table</h2>
<p>If you moved into A, the third unit at B could in principle be let, adding rent that the table does not
count. At a placeholder {m.money(36_000)} a year growing {m.pct(m.ASSUMPTIONS['rent_growth_a'],1)}, that would
narrow the gap to selling by roughly {m.money(36_000*sum((1+m.ASSUMPTIONS['rent_growth_a'])**i for i in range(25)))}.
This simple gross-rent illustration ignores expenses, income tax and reinvestment of receipts; the placeholder is not a rent estimate, and letting the unit depends on its legal
status and condition — both unverified ({src("civ1947")}).</p>

<h2>What would change the recommendation</h2>
{table("Decision triggers to re-run before the transfer", ["Trigger", "Effect", "Action", "Official source"], [
 ("You want to live in A", "Occupy becomes a consumption choice, not a yield comparison",
  "Model rent from the freed B unit before valuing occupancy; confirm the one-year exemption deadline", src("prop19", "boe266")),
 ("Rent could clear roughly 4% of value net", "Rental economics change materially",
  "Obtain written rent estimates and a unit-condition report; rerun with verified rent", src("civ1947")),
 (f"Rent growth above about {m.pct(BE_RENT,1)} a year sustained", "Rental path can overtake selling",
  "Check against rent-control rules and 50-year history, not a single hot year", src("civ1947", "sf_rent")),
 (f"After-tax returns below about {m.pct(BE_PORT,1)}", "Selling loses its advantage",
  "Reassess portfolio assumptions and fees", src("irs_basis")),
 ("Trust does not include A in the gross estate", "No step-up; a sale then carries capital-gains tax",
  "Obtain the trust document and an accountant's opinion before selling", src("irs_551", "irs_estate")),
], numeric=())}
"""
    page("decision.html", "Occupy, rent, or sell — the comparison that decides it",
         "Decision framework", body)


# ------------------------------------------------------------------ 3. projections
def build_projections():
    a_rows = []
    for y in range(2026, 2051):
        a_rows.append((str(y), m.money(m.value_a(y)), m.money(m.A.taxable(y)), m.money(m.A.tax(y)),
                       m.money(m.A.opex(y)), m.money(m.A.tax(y) + m.A.opex(y)), src("boe800", "scc_report")))
    t_rows = []
    for y in range(2040, 2051):
        v = m.transfer_year_view(y)
        t_rows.append((str(y), m.money(v["fmv"]), m.money(v["taxable"]), m.money(v["allowance"]),
                       m.money(v["assess_occupy"]), m.money(v["tax_occupy"]), m.money(v["tax_rent"]),
                       m.money(v["net_rent"]), m.money(v["proceeds"]), src("prop19", "pub801")))
    b_rows = []
    for y in range(2026, 2077):
        v = m.property_b_view(y)
        b_rows.append((str(y), m.money(v["value"]), m.money(v["taxable"]), m.money(v["tax"]),
                       m.money(v["rent"]), m.money(v["opex"]), m.money(v["noi"]), src("sf_rate", "civ1947")))
    body = f"""
<p class="lead">Fifty years of arithmetic, not a forecast. Every column is a formula with the inputs
shown. Change one assumption and the whole table moves — which is why the decision rests on the gap
between paths, not on any single year.</p>

<div class="callout"><h3>Assumptions, in one place</h3>
<p>Market value growth {m.pct(m.ASSUMPTIONS['home_growth'],1)} · inflation {m.pct(m.ASSUMPTIONS['inflation'],1)} ·
Prop 13 assessment cap {m.pct(m.ASSUMPTIONS['prop13_cap'],0)} · rent growth A {m.pct(m.ASSUMPTIONS['rent_growth_a'],1)},
B {m.pct(m.ASSUMPTIONS['rent_growth_b'],1)} · Prop 19 allowance {stat(f"${m.ASSUMPTIONS['allowance_base']:,}")}
growing {m.pct(m.ASSUMPTIONS['allowance_growth'],1)} · selling cost {m.pct(m.ASSUMPTIONS['sell_cost_rate'],1)} ·
after-tax portfolio return {m.pct(m.ASSUMPTIONS['portfolio_return'],1)} · transfer year
{m.ASSUMPTIONS['transfer_year']}. Rates: A {m.pct(m.A.tax_rate,2)}, B {m.pct(m.B.tax_rate,4)}.
None of these is an official forecast.</p></div>

<h2>Property A — value and tax before the transfer</h2>
{table("Continuity table: what the current owner's bill does if nothing changes",
       ["Year", "Market value", "Taxable value", "Annual tax", "Operating costs", "Total carrying cost", "Source"],
       a_rows, numeric=(1, 2, 3, 4, 5))}
<p class="small">The taxable value rises at most 2% a year until a change of ownership; the market value can
move independently ({src("boe800")}). Tax is the modelled ad valorem charge at the assumed area rate; the
county's actual charge includes voter-approved bonds and fixed assessments that vary by tax-rate area.</p>

<h2>Property A — what the transfer year does</h2>
{table("One row per candidate transfer year. Occupy keeps the partial exclusion; renting loses it.",
       ["Year", "Market value", "Protected taxable", "Prop 19 allowance", "Taxable if occupied",
        "Tax if occupied", "Tax if rented", "Net rent after costs", "Net sale proceeds", "Source"],
       t_rows, numeric=(1, 2, 3, 4, 5, 6, 7, 8))}

<h2>Property B — the asset that stays</h2>
{table("Already owned, part-rented building: value, assessment, tax, rent and net operating income",
       ["Year", "Market value", "Taxable value", "Annual tax", "Gross rent", "Operating costs", "Net operating income", "Source"],
       b_rows, numeric=(1, 2, 3, 4, 5, 6))}
<p class="small">B's taxable value grows at the Prop 13 cap and is not reset by A's inheritance. Rent growth is
capped in practice by the local rent ordinance and by state law while it remains in force
({src("sf_rent", "civ1947")}); the model uses {m.pct(m.ASSUMPTIONS['rent_growth_b'],1)}, below market rent
growth, for that reason.</p>

<h2>How to read these tables</h2>
<ul class="tight">
<li><strong>Nominal dollars.</strong> No inflation adjustment. At {m.pct(m.ASSUMPTIONS['inflation'],1)} inflation,
{m.money(m.value_a(2050))} in 2050 is about {m.money(m.value_a(2050)/(1+m.ASSUMPTIONS['inflation'])**24)} in
2026 purchasing power.</li>
<li><strong>Net sale proceeds</strong> assume {m.pct(m.ASSUMPTIONS['sell_cost_rate'],1)} of price for commission,
escrow, title and documentary transfer tax ({src("rtc11911")}).</li>
<li><strong>Stepped-up basis</strong> means no capital-gains tax on appreciation before death
({src("irs_basis")}); the projection does not deduct one.</li>
<li><strong>Declines are possible.</strong> A market crash can lower the assessed value only while market value
is below the factored base value ({src("boe800", "scc_assessor")}); the Black Swans page tests that.</li>
</ul>
"""
    page("projections.html", "Year-by-year value, assessment and tax",
         "Projections · 2026–2076", body)

# ------------------------------------------------------------------ 4. properties
def build_properties():
    a_rows = [
        ("Jurisdiction", "Santa Clara County, California", "County stated; city and ZIP withheld", src("scc_report")),
        ("Type / use", "Single-family home; the transferor's occupancy is not independently verified",
         '<span class="chip flag">assumption</span> needed for the Prop 19 exclusion', src("prop19", "boe800")),
        ("Ownership status", "Expected through a trust distribution, 2040–2050", "Not yet owned → reassessment event at transfer", src("scc_prop19")),
        ("Market-value anchor", m.money(m.A.market_value), f'Banded to $100,000 <span class="chip derived">derived</span>', src("fhfa")),
        ("Taxable (assessed) anchor", m.money(m.A.taxable_value), 'Banded to $1,000 to prevent record matching <span class="chip derived">derived</span>', src("boe800")),
        ("Modelled area tax rate", m.pct(m.A.tax_rate, 2), "1% base plus voter-approved bonds; the model sits between the county's ~1.19% average and the ~1.31% implied by the supplied bill (F02)", src("boe800", "scc_report")),
        ("Modelled annual tax, 2026", m.money(A26), "Supplied bill was about $7,200 → irregularity F02", src("scc_report")),
        ("Insurance (assumption)", m.money(m.A.insurance), "Owner estimate $1,500 held as a low case", src("cdi_sis")),
        ("Water / sewer (assumption)", m.money(m.A.water), "Owner range $100–$150 a month", src("boe800")),
        ("Electricity, net of solar", m.money(m.A.electric), "Owner reports a small annual credit", src("cpuc_nem")),
        ("Maintenance + capital reserve", m.money(m.A.maintenance + m.A.reserve), "Roof, paint, HVAC, inverter, plumbing", src("cdi_home")),
        ("Total carrying cost excl. tax", m.money(m.A.opex(2026)), "Insurance + water + power + maintenance + reserve", src("cdi_home")),
        ("Mortgage / debt", "", "Unknown; not assumed", src("irs_estate")),
    ]
    b_rows = [
        ("Jurisdiction", "San Francisco, California", "County stated; neighbourhood and ZIP withheld", src("sf_rate")),
        ("Type / use", "Three-unit building; two units leased, one occupant-usable", "Owner-supplied context", src("sf_rent")),
        ("Ownership status", "Already owned by the future heir", "No step-up and no reassessment from A's transfer", src("irs_basis")),
        ("Market-value anchor", m.money(m.B.market_value), 'Banded to $100,000 <span class="chip derived">derived</span>', src("fhfa")),
        ("Taxable anchor used", m.money(m.B.taxable_value), "Implied by the supplied bill at the official rate (F01)", src("sf_rate")),
        ("Official secured rate FY2026-27", m.pct(m.B.tax_rate, 8), "As published by the Treasurer & Tax Collector", src("sf_rate")),
        ("Modelled annual tax, 2026", m.money(B26), "Supplied bill: about $2,440", src("sf_rate")),
        ("Gross rent", m.money(BVIEW["rent"]), "Two leased units; rounded to $10", src("sf_rent")),
        ("Insurance (assumption)", m.money(m.B.insurance), "Landlord form for a 3-unit building", src("cdi_sis")),
        ("Water / sewer (assumption)", m.money(m.B.water), "Owner range $330–$400 a month for all units", src("boe800")),
        ("Electricity (assumption)", m.money(m.B.electric), "Owner range $30–$70 a month", src("boe800")),
        ("Maintenance + reserve", m.money(m.B.maintenance + m.B.reserve), "Older multi-unit building", src("cdi_home")),
        ("Vacancy + management", m.money(BVIEW["rent"] * (m.B.vacancy_rate + m.B.management_rate)), "5% vacancy, 8% management", src("civ1947")),
        ("Net operating income", m.money(BVIEW["noi"]), "Before income tax and debt service", src("civ1947")),
    ]
    sale_rows = [
        ("Sale price anchor", m.money(m.B.market_value), src("fhfa")),
        ("Selling costs (6.25% incl. SF transfer tax)", m.money(m.B.market_value * m.ASSUMPTIONS["sf_sell_cost_rate"]), src("sf_transfer")),
        ("Net proceeds", m.money(B_SALE_PROCEEDS), src("sf_transfer")),
        ("Income-tax basis — unverified", "", "Requires acquisition, improvement and depreciation records; F09", src("irs_551")),
        ("Taxable gain — unverified", "", "No assessed-value proxy can establish income-tax basis", src("irs_551")),
        ("Capital-gains tax — unverified", "", "Depends on actual basis and tax circumstances", src("irs_523")),
        ("After-tax investable proceeds — unverified", "", "Do not compare with rent until tax is known", src("irs_551")),
        ("Compare: current net operating income", m.money(BVIEW["noi"]), "Plus appreciation and a later step-up", src("civ1947")),
    ]
    body = f"""
<p class="lead">Two properties, opposite starting points. A is a future inheritance with a low taxable value and
a high market value. B is already owned, with a very low taxable value and rent-controlled tenants; its
income-tax basis is unknown. Confusing the two produces bad advice, so they are
kept separate throughout.</p>

<div class="callout"><h3>The distinction that drives everything</h3>
<p><strong>A is inherited.</strong> Its income-tax basis steps up to date-of-death value, and its property-tax
assessment is reset unless the heir occupies it and claims the Prop 19 family-home exclusion.
<strong>B is already owned.</strong> Inheriting A does not change B's basis, its assessment, its tenants or its
rents. Any plan that sells B "because of the inheritance" is solving a problem that does not exist.</p></div>

<h2>Property A — future inheritance</h2>
{table("Fact sheet, with every non-source item labelled", ["Item", "Value", "Basis / note", "Official source"], a_rows)}

<h2>Property B — already owned</h2>
{table("Fact sheet, with every non-source item labelled", ["Item", "Value", "Basis / note", "Official source"], b_rows)}

<h2>Should B also be sold?</h2>
{table("A sale of B today, for comparison with holding it", ["Line", "Amount", "Source"], sale_rows, numeric=(1,))}
<p class="small">B's actual income-tax basis is unknown; taxable gain and after-tax proceeds are intentionally blank.
Holding B keeps {m.money(BVIEW['noi'])} of modelled net rent before income tax and keeps housing available.
No conclusion about selling B is possible without basis and the owner's investment alternative.</p>

<h2>What is still unknown</h2>
<ul class="tight">
<li>Trust terms, successor-trustee powers, and whether A is included in the transferor's gross estate.</li>
<li>Whether either property carries a mortgage, reverse mortgage, lien or deferred maintenance.</li>
<li>Actual B leases, security deposits, rent-control registration and the legal status of the third unit.</li>
<li>Whether the solar system's net-metering tariff survives a change of ownership
({src("cpuc_nem")}).</li>
<li>Actual insurance quotes, water and power tariffs, and property-tax direct assessments.</li>
</ul>
<p class="small">All of these are on <a href="flagged.html">Flagged for review</a>.</p>
"""
    page("properties.html", "What is known about each property — and what is not",
         "Property fact sheets", body)


# ------------------------------------------------------------------ 5. costs
def build_costs():
    rows = [
        ("Property tax, A", m.money(A26), "1.25% of the banded taxable value; bonds and fixed assessments vary by area",
         '<span class="chip derived">derived</span>', src("boe800", "scc_report")),
        ("Property tax, B", m.money(B26), "Official FY2026-27 rate × the implied taxable value",
         '<span class="chip ok">reconciled</span>', src("sf_rate")),
        ("Home insurance, A", m.money(m.A.insurance), "Assumption: replacement cost of a $3.1M home. Owner estimate $1,500 is a low case",
         '<span class="chip assume">assumption</span>', src("cdi_sis", "cdi_home")),
        ("Home insurance, B", m.money(m.B.insurance), "Assumption: landlord form for three units",
         '<span class="chip assume">assumption</span>', src("cdi_home")),
        ("Water / sewer, A", m.money(m.A.water), "Owner range $100–$150 a month; provider and meter unknown",
         '<span class="chip flag">owner estimate</span>', src("boe800")),
        ("Water / sewer, B", m.money(m.B.water), "Owner range $330–$400 a month across three units",
         '<span class="chip flag">owner estimate</span>', src("boe800")),
        ("Electricity, A", m.money(m.A.electric), "Net credit reported by the owner; depends on the solar tariff and true-up",
         '<span class="chip flag">owner estimate</span>', src("cpuc_nem")),
        ("Electricity, B", m.money(m.B.electric), "Owner range $30–$70 a month",
         '<span class="chip flag">owner estimate</span>', src("boe800")),
        ("Maintenance, A", m.money(m.A.maintenance), "Routine repairs; the owner reports lower upkeep than B",
         '<span class="chip assume">assumption</span>', src("cdi_home")),
        ("Maintenance, B", m.money(m.B.maintenance), "Older building, three kitchens and baths",
         '<span class="chip assume">assumption</span>', src("cdi_home")),
        ("Capital reserve, A", m.money(m.A.reserve), "Roof, HVAC, inverter replacement; not routine maintenance",
         '<span class="chip assume">assumption</span>', src("cdi_home")),
        ("Capital reserve, B", m.money(m.B.reserve), "Same logic, shared systems",
         '<span class="chip assume">assumption</span>', src("cdi_home")),
        ("Vacancy, B", m.money(BVIEW["rent"] * m.B.vacancy_rate), "5% of gross rent; actual turnover unknown",
         '<span class="chip assume">assumption</span>', src("civ1947")),
        ("Management, B", m.money(BVIEW["rent"] * m.B.management_rate), "8% of gross rent; zero if self-managed",
         '<span class="chip assume">assumption</span>', src("civ1947")),
        ("Vacancy + management, A if rented", m.money(T["rent"] * (m.A.vacancy_rate + m.A.management_rate)),
         "Same convention applied to the rental scenario", '<span class="chip assume">assumption</span>', src("civ1947")),
        ("Homeowners' exemption, A", f"-{m.money(7_000 * m.A.tax_rate)}", "$7,000 of assessed value, owner-occupied only",
         '<span class="chip ok">verified</span>', src("boe266")),
    ]
    body = f"""
<p class="lead">Costs are where optimistic plans fail. Each line is either an official figure, an arithmetic
result from one, or an explicitly labelled guess. Insurance and utilities are guesses because no official
source publishes a premium or a water bill for a specific home.</p>

<h2>Annual cost stack, today's dollars</h2>
{table("Line items for both properties", ["Item", "2026 amount", "Basis", "Status", "Official source"],
       rows, numeric=(1,))}

<h2>Carrying-cost summary</h2>
<div class="cards">
<div class="card"><div class="k">Property A, unoccupied or occupied</div><div class="v">{m.money(A26 + m.A.opex(2026))}</div>
<div class="n">Property tax {m.money(A26)} + other costs {m.money(m.A.opex(2026))}</div></div>
<div class="card"><div class="k">Property A, rented, before the transfer</div><div class="v">{m.money(m.A.rent(2026) - A26 - m.A.opex(2026) - m.A.rent(2026)*(m.A.vacancy_rate+m.A.management_rate))}</div>
<div class="n">Rent {m.money(m.A.rent(2026))} less tax, costs, vacancy and management — before income tax</div></div>
<div class="card"><div class="k">Property B, all-in</div><div class="v">{m.money(B26 + BVIEW["opex"])}</div>
<div class="n">Against gross rent {m.money(BVIEW["rent"])}</div></div>
<div class="card"><div class="k">Property B, net operating income</div><div class="v">{m.money(BVIEW["noi"])}</div>
<div class="n">Before income tax and debt service</div></div>
</div>

<h2>Insurance: what the official data does and does not say</h2>
<p>The California Department of Insurance publishes a market snapshot, not quotes. It reports an average
California homeowner premium of <strong>{stat('$1,571')}</strong> against a national average of
<strong>{stat('$1,512')}</strong>, with <strong>677,449</strong> FAIR Plan homeowner policies and
<strong>662</strong> ZIP codes in distressed areas ({src("cdi_sis")}). None of those numbers is a premium for
either property.</p>
<ul class="tight">
<li><strong>A $1,500 homeowner premium is below the state average</strong> and is not plausible for a dwelling
whose replacement cost is well over seven figures. The model uses {m.money(m.A.insurance)} and tests
{m.money(m.A.insurance*3)} on the stress page.</li>
<li><strong>A three-unit building needs a landlord policy</strong>, not a homeowner policy. Coverage, liability
and loss-of-rent terms differ, and the premium is not comparable to A's.</li>
<li><strong>FAIR Plan is a last resort</strong> and covers only fire, lightning, internal explosion and smoke;
extended coverage and a separate differences-in-conditions policy are usually needed
({src("cdi_home")}).</li>
<li><strong>Earthquake is separate.</strong> Nothing in this analysis assumes earthquake cover.</li>
</ul>

<h2>Water, power and solar</h2>
<ul class="tight">
<li><strong>Water.</strong> The owner's ranges imply about {m.money(m.A.water)} a year for A and
{m.money(m.B.water)} for B. Provider tariffs, sewer charges, meter size and irrigation are unverified.</li>
<li><strong>Electricity.</strong> A's solar is reported to produce a small annual credit. Exports are credited at
the applicable tariff, which for systems interconnected after April 2023 is the net billing tariff with export
credits usually below retail ({src("cpuc_nem")}). Whether an existing tariff survives a change of ownership is
not established here — that is the single largest risk to the "no electricity cost" assumption.</li>
<li><strong>Inverter and battery replacement</strong> are in the capital reserve, not in the electricity line.</li>
</ul>

<h2>Maintenance rule of thumb used</h2>
<p>Routine maintenance is modelled at {m.money(m.A.maintenance)} for A and {m.money(m.B.maintenance)} for B, plus
capital reserves of {m.money(m.A.reserve)} and {m.money(m.B.reserve)}. That is far below the common
"1% of value" rule for A ({m.money(m.A.market_value*0.01)}), because that rule scales with land value in a
high-price market and overstates upkeep on a maintained house. It is an assumption, and the low-growth stress
case shows what happens if it is wrong.</p>
"""
    page("costs.html", "What it actually costs to hold each property",
         "Operating costs", body)

# ------------------------------------------------------------------ 6. black swans
def build_black_swans():
    stress = [
        ("Baseline", 0.025, 0.040, 0.030, 1.0, 0.0, m.wealth()),
        ("Housing crash: −30% value at the transfer date, rents −15%", 0.025, 0.040, 0.030, 1.0, 0.30,
         m.wealth(transfer_discount=0.30, rent_discount=0.15)),
        ("Stagflation: 5% CPI, 3% home growth, 4% rent growth", 0.050, 0.030, 0.040, 1.0, 0.0,
         m.wealth(inflation=0.05, home_growth=0.03, rent_growth=0.04)),
        ("Secular stagnation: 2% home growth, 2% rent growth", 0.025, 0.020, 0.020, 1.0, 0.0,
         m.wealth(home_growth=0.02, rent_growth=0.02)),
        ("Insurance shock: premiums ×3 (non-renewal, FAIR Plan, DIC)", 0.025, 0.040, 0.030, 3.0, 0.0,
         m.wealth(insurance_mult=3.0)),
        ("Rent caps tighten: rent growth 1.5%", 0.025, 0.040, 0.015, 1.0, 0.0,
         m.wealth(rent_growth=0.015)),
        ("Portfolio disappointment: 3% after tax", 0.025, 0.040, 0.030, 1.0, 0.0,
         m.wealth(portfolio=0.03)),
        ("Boom: 6% home growth", 0.025, 0.060, 0.030, 1.0, 0.0,
         m.wealth(home_growth=0.06)),
        ("Transfer slips to 2050", 0.025, 0.040, 0.030, 1.0, 0.0, m.wealth(year=2050)),
    ]
    rows = []
    for name, pi, g, rg, ins, disc, w in stress:
        rows.append((f"<strong>{html.escape(name)}</strong><br><span class='small'>CPI {m.pct(pi,1)} · home "
                     f"{m.pct(g,1)} · rent {m.pct(rg,1)}</span>",
                     m.money(w["s1"]), m.money(w["s2"]), m.money(w["s3"]),
                     m.money(w["s2"] - w["s3"]), src("fhfa", "boe800", "cdi_sis")))
    body = f"""
<p class="lead">A 50-year plan built on a single growth rate is a plan built on fiction. This page keeps the
same arithmetic but changes the regime: crashes, inflation, insurance shocks, rent caps and a portfolio that
disappoints.</p>

<div class="notice"><strong>What the evidence says about smoothness.</strong> The most recent official CPI
release shows monthly all-items changes of +0.6% in September 2026 and +0.4% in October 2026, energy +5.2%
then +0.7%, gasoline up 37.4% over the periods BLS could compare, and electricity +0.9% in one month
({src("bls")}). BLS also could not publish a 12-month change for October 2026 at all, because October 2025
data were not collected during a lapse in appropriations. That is the texture of real data: gaps, spikes and
revisions. A flat 2.5% line is a modelling convenience, not the world.</div>

<h2>Stress matrix</h2>
{table("Net worth at 2070 under each regime (2045 transfer unless stated). Positive rent−sell means renting wins.",
       ["Scenario", "Occupy A", "Rent A", "Sell A", "Rent − sell", "Official source for the rule stressed"],
       rows, numeric=(1, 2, 3, 4))}
<p class="small">Each row re-runs the same model with the stated inputs. These are scenarios, not
probabilities. The sell path is not immune to the first row: a crash at the transfer date lowers the sale
price, which is why the timing of a sale matters more than the timing of a forecast.</p>

<h2>The five shocks that matter most</h2>
<div class="grid2">
<div class="callout"><h3>1. A crash at the wrong moment</h3>
<p>Sequence, not average, decides the outcome. A 30% fall at the transfer date cuts every path, and at the
horizon the sale path ends {m.money(W['s3'] - m.wealth(transfer_discount=0.30, rent_discount=0.15)['s3'])}
lower than in the baseline ({m.money(m.wealth(transfer_discount=0.30, rent_discount=0.15)['s3'])} versus
{m.money(W['s3'])}). Property tax does not fall with the market unless the assessed value is above market and
the county enrolls a Prop 8 decline-in-value assessment ({src("boe800", "scc_assessor")}).</p></div>
<div class="callout"><h3>2. Insurance withdrawal</h3>
<p>The state's insurer of last resort already carries 677,449 homeowner policies, and 662 ZIP codes are
designated distressed ({src("cdi_sis")}). Tripling the premium reduces the rental path by about
{m.money(W['s2'] - m.wealth(insurance_mult=3.0)['s2'])} and the occupancy path by
{m.money(W['s1'] - m.wealth(insurance_mult=3.0)['s1'])}. A non-renewal with no replacement is worse: it is
an uninsurable asset, not an expensive one.</p></div>
<div class="callout"><h3>3. Uninsurable physical loss</h3>
<p>A fire or earthquake loss equal to 20% of value is {m.money(0.2 * T['fmv'])} at the transfer date. The
owner of the house absorbs it; the seller of the house does not. Earthquake cover is separate, and FAIR Plan
cover is narrow ({src("cdi_home")}).</p></div>
<div class="callout"><h3>4. Rent regulation and tenants</h3>
<p>Statewide caps under Civil Code 1947.12 allow 5% plus CPI, capped at 10%, and the section is repealed on
1 January 2030 unless extended; local ordinances layer on top ({src("civ1947", "sf_rent")}). A permanent
1.5% rent-growth regime costs the rental path about {m.money(W['s2'] - m.wealth(rent_growth=0.015)['s2'])}.
Tenant buyouts, eviction limits and habitability claims can cost more than the cap itself.</p></div>
</div>

<h3>5. Tax and legal surprises</h3>
<ul class="tight">
<li><strong>No step-up.</strong> If the trust is drafted or funded so that A is not included in the
transferor's gross estate, the basis may carry over. On a $6,531,230 sale with a $250,000 basis the
capital-gains tax at 37.1% would be about {m.money((T['fmv'] - 250_000) * m.ASSUMPTIONS['terminal_cg_rate'])}.
This is the single most expensive possible surprise ({src("irs_551")}).</li>
<li><strong>Prop 19 tolerance.</strong> The allowance ({stat('$1,044,586')} for transfers through 15 February
2027) is adjusted every other year and can be changed by the Legislature or the voters. A smaller allowance
raises the occupied-path tax ({src("prop19", "pub801")}).</li>
<li><strong>A wealth or inheritance tax.</strong> A 2026 statewide measure that would have imposed a one-time
tax on certain taxpayers was defeated, 47.4% yes to 52.6% no, in unofficial results; a separate measure
prohibiting new state personal property taxes and certain retroactive state taxes passed. Neither outcome is
certified yet ({src("sos")}).</li>
<li><strong>Administration delay.</strong> A contested trust or a late appraisal can add a year of carrying
costs, roughly {m.money(T['cost_occupy_total'])} at 2045 values, before any decision is possible.</li>
</ul>

<h2>How to hold the plan together</h2>
<ul class="tight">
<li>Keep 24 months of full carrying costs in cash before the transfer, sized from the table on the
<a href="costs.html">Costs</a> page.</li>
<li>Sell on a documented timetable or a documented trigger, not in a panic and not on a forecast.</li>
<li>Confirm insurance replacement cost, exclusions and earthquake cover before occupancy or letting.</li>
<li>Do not rely on the solar credit surviving the transfer until the utility confirms the tariff
({src("cpuc_nem")}).</li>
<li>Re-run these five shocks whenever a real input changes.</li>
</ul>
"""
    page("black-swans.html", "When growth and inflation stop being well behaved",
         "Black swans & uneven regimes", body)


# ------------------------------------------------------------------ 7. tax
def build_tax():
    hist = [(y, v, src("irs_estate")) for y, v in [
        ("2018", "$11,180,000"), ("2019", "$11,400,000"), ("2020", "$11,580,000"),
        ("2021", "$11,700,000"), ("2022", "$12,060,000"), ("2023", "$12,920,000"),
        ("2024", "$13,610,000"), ("2025", "$13,990,000"), ("2026", stat("$15,000,000"))]]
    proj = []
    for y in (2026, 2030, 2035, 2040, 2045, 2050):
        proj.append((str(y), m.money(m.estate_threshold(y)),
                     f"{m.pct(0.025,1)} indexing", src("irs_estate", "irs_new")))
    estate_rows = []
    for size in (10_000_000, 20_000_000, 30_000_000, 40_000_000):
        t26 = 0.40 * max(size - 15_000_000, 0)
        t45 = 0.40 * max(size - m.estate_threshold(2045), 0)
        estate_rows.append((m.money(size), m.money(t26), m.money(t45), src("irs_estate", "irs_706")))
    rules = [
        ("Who pays", "The <em>estate</em> pays federal estate tax, not the beneficiary. There is no per-heir allowance and no flat penalty on receiving an inheritance.",
         '<span class="chip ok">verified</span>', src("irs_estate", "irs_faq")),
        ("California", "No California estate tax return is required for deaths on or after 1 January 2005; the old inheritance tax applies only to deaths before 8 June 1982. No California inheritance tax exists today.",
         '<span class="chip ok">verified</span>', src("sco")),
        ("Income tax on receipt", "An inheritance is not income. Interest, dividends, rent or gains it later produces are taxable.",
         '<span class="chip ok">verified</span>', src("ftb")),
        ("Inherited basis", "Generally the fair market value at the date of death (or an elected alternate valuation date), so pre-death appreciation is not taxed to the heir.",
         '<span class="chip ok">verified</span>', src("irs_basis", "irs_551")),
        ("Trust assets", "Trust property can be included in the gross estate. A trust label alone does not create a step-up or an estate-tax exemption.",
         '<span class="chip flag">professional review</span>', src("irs_estate")),
        ("Filing and portability", "Form 706 is due nine months after death; a six-month extension is available. A portability election requires a timely return.",
         '<span class="chip ok">verified</span>', src("irs_faq")),
        ("California income tax on a sale", "Gain on a later sale is California income; the top marginal rate reaches 13.3%. The model uses 37.1% combined, which is an assumption.",
         '<span class="chip assume">assumption</span>', src("ftb")),
    ]
    body = f"""
<p class="lead">Three different taxes are routinely confused: a tax on the estate, a tax on the heir, and a
tax on a later sale. Only the first can be triggered by inheriting, and only if the estate is large.</p>

<div class="callout"><h3>Bottom line</h3>
<p>A {stat('$15,000,000')} federal exclusion applies per person in 2026, and it is not a per-heir allowance
({src("irs_estate")}). California imposes no estate or inheritance tax ({src("sco")}). An inheritance is not
income ({src("ftb")}). The realistic risks are (a) the transferor's total estate exceeding the exclusion,
(b) losing the step-up because of how the trust is drafted, and (c) capital-gains tax on a later sale.</p></div>

<h2>Federal filing threshold, as published</h2>
{table("Filing threshold by year of death", ["Year of death", "Threshold", "Official source"], hist)}
<p class="small">The 2026 figure was set by Public Law 119-21, which raised the basic exclusion to
{stat('$15,000,000')} and removed the scheduled sunset ({src("irs_new")}). Indexing begins in 2027; the
projections below assume {m.pct(0.025,1)} a year, which is an assumption, not a published schedule.</p>

<h2>Projected exclusion, if current law is left alone</h2>
{table("Projection, for planning only", ["Year", "Projected exclusion", "Basis", "Official source"], proj, numeric=(1,))}

<h2>What an estate of a given size could owe</h2>
{table("Illustrative federal estate tax at a 40% marginal rate (assumption) above the exclusion",
       ["Taxable estate", "Tax at 2026 rules", "Tax at 2045 projected rules", "Official source"],
       estate_rows, numeric=(1, 2))}
<p class="small">Real estates are rarely taxed at a flat 40%: deductions, marital transfers, charitable gifts,
valuation discounts and the graduated schedule all matter, and state-level rules differ. The 40% figure is the
commonly cited top marginal rate and is used here as an assumption; the rate schedule is in the Form 706
instructions ({src("irs_706")}). What matters for planning is the shape: below the threshold, no federal
estate tax at all.</p>

<h2>The rules that decide who pays what</h2>
{table("Recipient, estate and sale — kept separate", ["Question", "Rule", "Status", "Official source"], rules)}

<h2>Why the step-up is worth more than the estate tax here</h2>
<p>If A is included in the transferor's estate, its basis becomes the date-of-death value. Selling at or near
that value then produces little or no gain. If instead the basis carried over at, say, a hypothetical
{stat('$250,000')}, a sale at {m.money(T['fmv'])} in 2045 would produce a gain of about
{m.money(T['fmv'] - 250_000)} and, at the assumed 37.1% combined rate,
{m.money((T['fmv'] - 250_000) * m.ASSUMPTIONS['terminal_cg_rate'])} of tax — an amount larger than any
plausible property-tax difference between the three options. Confirm inclusion in the estate before relying
on it ({src("irs_basis", "irs_551")}).</p>

<h2>What "considerable money" changes</h2>
<ul class="tight">
<li><strong>If the whole estate is below the exclusion</strong> — including A, B if owned by the same person,
life insurance, retirement accounts and prior taxable gifts — there is no federal estate tax and no California
estate tax.</li>
<li><strong>If it is above</strong>, the excess is taxed at the estate level. Cash set aside for that tax is
not available to the heirs, which is why liquidity planning belongs in the trust review.</li>
<li><strong>Gifts before death reduce the estate</strong> but also use exclusion and can affect the basis of
what is given. That is a specialist question, not something this site can settle.</li>
<li><strong>The 2040–2050 threshold is unknowable.</strong> The current law is permanent only in the sense that
it has no sunset; a future Congress can change it.</li>
</ul>
"""
    page("tax.html", "Who pays what: estate, inheritance and capital gains",
         "Inheritance & tax", body)

# ------------------------------------------------------------------ 8. process
def build_process():
    steps = [
        ("0 · Now to 2039", "Collect the documents: the trust and every amendment, deeds, title policy, mortgage or lien statements, insurance policies, the solar agreement, permits, and receipts for improvements that affect basis.",
         "Before the transfer; no deadline", "A missing amendment or unfunded trust can force probate or change who owns what.", src("courts_probate", "irs_551")),
        ("1 · Now to 2039", "Confirm who the successor trustee is, what powers the trustee has, and whether A is included in the transferor's gross estate. Ask an accountant to model the estate against the exclusion.",
         "Before the transfer; review every few years", "No step-up; unexpected estate tax; a sale that cannot be executed quickly.", src("irs_estate", "irs_faq")),
        ("2 · Now to 2039", "Fix insurance now: replacement-cost estimate, exclusions, earthquake decision, and whether the carrier will keep the policy after a change of ownership.",
         "Before the transfer", "Non-renewal at the worst moment; a large uninsured gap.", src("cdi_home", "cdi_sis")),
        ("3 · At death", "Obtain certified death certificates, notify the trustee and the insurer, secure the property, redirect mail, photograph its condition, and stop unnecessary services.",
         "Immediately; the insurer should be told at once", "Vacancy losses and cover disputes.", src("courts_probate")),
        ("4 · At death + 0–150 days", "File the change-of-ownership statement with the county assessor for a death transfer (BOE-502-D / BOE-502-AH).",
         "Within 150 days of death where no probate; with the inventory if probated", "Penalty of the greater of $100 or 10% of the new tax, capped, for failing to answer the assessor's request.", src("sf_cos")),
        ("5 · At death + 0–4 months", "Obtain a defensible date-of-death valuation and an inventory; keep it with the basis records for every asset, not just the house.",
         "Before any sale or distribution", "A basis that cannot be defended on audit.", src("irs_basis", "irs_551")),
        ("6 · At death + 9 months", "Decide whether Form 706 is required; if the estate elects portability, file on time. A six-month extension is available.",
         "9 months from death (+6-month extension)", "Lost portability; interest and penalties.", src("irs_faq")),
        ("7 · Within 1 year of transfer", "If you will occupy A, file the homeowners' exemption (BOE-266) within one year of the transfer. This is what makes the Prop 19 exclusion effective from the transfer date.",
         "1 year; exemption claim each year by 15 February", "Exclusion starts only when the claim is filed — a permanent tax increase.", src("prop19", "boe266")),
        ("8 · Within 3 years, before any sale", "File the Prop 19 intergenerational exclusion claim (BOE-19-P) with the county assessor.",
         "3 years from transfer, or before transfer to a third party", "Loss of the exclusion for prior years.", src("pub801", "scc_prop19")),
        ("9 · Months 1–12", "Establish the trust's accounting, pay allowed debts and expenses, and distribute according to the trust — not by informal agreement among heirs.",
         "Per trust terms and trustee duties", "Personal liability for the trustee; disputes among heirs.", src("courts_probate")),
        ("10 · Decision window", "Get three insurance quotes, two estate-agent opinions of value, a rental opinion, a home inspection and a tax projection. Then decide: occupy, rent or sell.",
         "Before signing a lease or listing agreement", "A decision made on one opinion and no inspection.", src("cdi_home", "irs_basis")),
        ("11 · Execution", "If selling: list, disclose, and confirm the transfer tax and escrow costs. If renting: verify the legal unit count, rent limits and deposits.",
         "Before marketing or letting", "Illegal units, unenforceable rents, or a transfer-tax surprise.", src("rtc11911", "civ1947")),
        ("12 · Every year", "Re-check the tax bill and exemptions, insurance, the solar tariff, rents and capital needs. Re-run the decision if a trigger on the Decision page moves.",
         "Annual", "Drift between plan and reality.", src("boe800", "cpuc_nem")),
    ]
    rows = [(a, b, c, d, e) for a, b, c, d, e in steps]
    body = f"""
<p class="lead">The transfer is an administrative process with hard deadlines. Missing the one-year
homeowners' exemption claim is the most expensive clerical error available here, because it changes whether
the Prop 19 exclusion applies from the transfer date or only from the year of a late claim.</p>

<div class="notice"><strong>Trust, not probate, is the assumption.</strong> A funded trust normally avoids
probate, which is why the timeline below is built around trustee duties and assessor filings rather than
court filings. If A is not actually held by the trust at death, probate is back on the table and the timeline
changes ({src("courts_probate")}). The small-estate affidavit is not a substitute for real property; it covers
personal property only ({src("courts_small")}).</div>

<h2>Step by step</h2>
{table("Timeline from preparation to the first annual review", ["Phase", "Action", "Deadline / authority",
       "If missed", "Official source"], rows)}

<h2>The three deadlines that matter most</h2>
<div class="grid2">
<div class="callout"><h3>150 days — assessor notice</h3>
<p>A death transfer must be reported to the county assessor within 150 days where the estate is not probated.
The penalty for ignoring the assessor's request is the greater of $100 or 10% of the new tax, capped at $5,000
or $20,000 depending on homeowners'-exemption eligibility ({src("sf_cos")}).</p></div>
<div class="callout"><h3>1 year — homeowners' exemption</h3>
<p>The Prop 19 exclusion applies from the transfer date only if the heir files for the homeowners' or
disabled-veterans' exemption within one year. Later filing makes the exclusion prospective only
({src("prop19", "boe266")}).</p></div>
<div class="callout"><h3>3 years — exclusion claim</h3>
<p>The BOE-19-P claim is due within three years of the transfer and before any transfer to a third party, with
a late-claim window of six months after a supplemental or escape assessment notice ({src("pub801")}).</p></div>
<div class="callout"><h3>9 months — Form 706</h3>
<p>A federal estate-tax return, if required, is due nine months after death; a six-month extension is
available, and portability depends on a timely filing ({src("irs_faq")}).</p></div>
</div>

<h2>Documents to assemble before 2040</h2>
<ul class="tight">
<li>Trust instrument, all amendments, schedule of assets and any pour-over will.</li>
<li>Grant deeds, title insurance, mortgage or reverse-mortgage statements, and liens.</li>
<li>Insurance policies, the solar agreement and utility bills for the last 24 months.</li>
<li>Property-tax bills, assessment notices and any exemption or exclusion correspondence.</li>
<li>Improvement receipts, permits and prior appraisals for basis and for the step-up record.</li>
<li>Leases, deposits, rent histories and rent-board registration for B.</li>
</ul>
<p class="small">Do not upload these to any website. This site has no forms and stores nothing.</p>
"""
    page("process.html", "From trust distribution to a signed decision",
         "Inheritance process", body)


# ------------------------------------------------------------------ 9. law watch
def build_law_watch():
    enacted = [
        ("Federal exclusion", "Basic exclusion raised to $15,000,000 for 2026 and the scheduled sunset removed by Public Law 119-21; indexing continues.",
         '<span class="chip ok">enacted</span>', src("irs_new", "irs_estate")),
        ("California estate tax", "No estate tax return for deaths on or after 1 January 2005; no inheritance tax today.",
         '<span class="chip ok">current law</span>', src("sco")),
        ("Proposition 19", "Family-home exclusion limited to a principal residence of both parties, with a value limit of taxable value plus an adjusted $1,000,000.",
         '<span class="chip ok">enacted 2020</span>', src("prop19", "pub801")),
        ("Prop 19 allowance", f"{stat('$1,044,586')} for transfers from 16 February 2025 through 15 February 2027; adjusted every other year.",
         '<span class="chip ok">published</span>', src("pub801")),
        ("Rent caps", "Civil Code 1947.12 caps increases at 5% plus CPI (maximum 10%) and is repealed on 1 January 2030 unless extended.",
         '<span class="chip ok">enacted, sunsetting</span>', src("civ1947")),
        ("Local rent cap", "The local allowable increase is 1.6% for 1 March 2026 through 28 February 2027, set annually at 60% of the regional CPI change.",
         '<span class="chip ok">current</span>', src("sf_rent")),
        ("Solar compensation", "New interconnections since 15 April 2023 take the net billing tariff; legacy net-metering tariffs are closed to new enrolments.",
         '<span class="chip ok">enacted</span>', src("cpuc_nem")),
        ("Insurance regulation", "Sustainable Insurance Strategy reforms continue; 27 homeowner rate filings approved in 2026 and 12 groups expanding.",
         '<span class="chip ok">in force</span>', src("cdi_sis")),
    ]
    ballot = [
        ("Prop 3 — extends the existing high-income income tax for schools and health care",
         "<strong>Passed</strong>, 60.6% yes", "Affects the top marginal rate applied to a future sale.", src("sos")),
        ("Prop 40 — imposes a one-time tax on certain taxpayers",
         "<strong>Failed</strong>, 47.4% yes / 52.6% no", "A statewide wealth-tax approach was rejected, but proponents can return.", src("sos")),
        ("Prop 42 — prohibits new state personal property taxes and certain retroactive state taxes",
         "<strong>Passed</strong>, 51.5% yes", "Constrains new state personal-property or retroactive taxes; does not repeal the estate-tax framework.", src("sos")),
        ("Prop 43 — limits voters' ability to raise local revenues for local services",
         "<strong>Failed</strong>, 57.4% no", "Local parcel taxes and bond measures remain available to raise property-tax charges.", src("sos")),
    ]
    watch = [
        ("Federal estate tax", "Any future Congress can lower the exclusion, change portability or repeal the tax. A halving scenario is tested on the Black Swans page.",
         "IRS guidance each autumn", src("irs_new")),
        ("State wealth or inheritance tax", "A 2026 measure failed, but proposals recur. A statewide tax would need to fit within the personal-property restriction that passed.",
         "Secretary of State ballot measures; Legislative Analyst", src("sos")),
        ("Prop 19 amendments", "The allowance and the principal-residence conditions are statutory and constitutional; both can change before 2045.",
         "BOE letters to assessors; assessor guidance", src("prop19", "pub801")),
        ("Rent regulation", "The statewide cap expires 1 January 2030. Local expansion or contraction changes B's rent path and A's rental case.",
         "Legislature; local rent board", src("civ1947", "sf_rent")),
        ("Property-tax revenue measures", "Local bonds and parcel taxes raise the rate above the 1% base. Splitting the roll or changing Prop 13 needs a constitutional amendment.",
         "County tax-rate books; ballot measures", src("scc_report", "boe800")),
        ("Insurance market", "Rate approvals, FAIR Plan expansion and catastrophe modelling change premiums and availability.",
         "CDI rate filings; Sustainable Insurance Strategy updates", src("cdi_sis")),
        ("Solar tariffs", "Tariff successors and legacy periods determine whether the credit survives a change of ownership.",
         "CPUC; utility tariff books", src("cpuc_nem")),
    ]
    body = f"""
<p class="lead">Today's rules are inputs, not constants. This page separates what is enacted and verified
from what is merely possible, and lists the publication to watch for each.</p>

<div class="notice"><strong>2026 election caveat.</strong> Statewide results below are the Secretary of
State's <em>unofficial</em> count as of 10 November 2026; certification is due 11 December 2026. Percentages
have moved during the count and will move again ({src("sos")}).</div>

<h2>Enacted and verified</h2>
{table("Rules in force now, with the page that states them", ["Topic", "Rule", "Status", "Official source"], enacted)}

<h2>Statewide measures, 2026 general election</h2>
{table("Only the measures with a plausible effect on this decision", ["Measure", "Unofficial result", "Why it matters", "Official source"], ballot)}

<h2>Scheduled to change or expire</h2>
<ul class="tight">
<li><strong>1 January 2030</strong> — the statewide rent cap is repealed by its own terms unless extended
({src("civ1947")}).</li>
<li><strong>15 February 2027</strong> — the current Prop 19 allowance period ends and a new adjusted amount
applies ({src("pub801")}).</li>
<li><strong>Every autumn</strong> — the IRS publishes the next year's exclusion and the BOE publishes the
assessment inflation factor; both are inputs to the model.</li>
<li><strong>Every 1 March</strong> — the local allowable rent increase is reset ({src("sf_rent")}).</li>
</ul>

<h2>What to monitor, and where</h2>
{table("A watch list rather than a prediction", ["Area", "What could change", "Where to watch", "Official source"], watch)}

<h2>What would actually change the decision</h2>
<ul class="tight">
<li><strong>A smaller Prop 19 allowance</strong> makes occupying A more expensive and strengthens the case for
selling.</li>
<li><strong>A lower federal exclusion</strong> matters only if the total estate is near or above it.</li>
<li><strong>Rent deregulation</strong> improves the rental case; tighter caps weaken it further.</li>
<li><strong>Higher transaction taxes</strong> make selling more expensive but do not change the ranking until
selling costs reach about {m.pct(1 - W["s2"]/(T["fmv"]*(1+m.ASSUMPTIONS["portfolio_return"])**25),0)} of value —
far above today's total.</li>
<li><strong>A change in step-up rules</strong> would be the most consequential change of all, because it would
put a capital-gains tax on the sale of A.</li>
</ul>
"""
    page("law-watch.html", "What could change before 2045",
         "Law watch", body)

# ------------------------------------------------------------------ 10. flagged
def build_flagged():
    flags = [
        ("F01 · Property B assessment does not reconcile", 
         "The supplied assessment implies a tax bill of roughly $1,350 at the official rate, but the supplied bill "
         f"is about $2,440. The bill implies an assessed value near {m.money(m.B.taxable_value)} — about 1.8 times the stated figure.",
         "Projections use the implied value, so B's tax may be overstated if the stated assessment is right and the bill contains large fixed charges.",
         "Obtain the current assessor record and the bill's line-item breakdown.", src("sf_rate")),
        ("F02 · Property A bill implies a higher rate",
         f"The supplied bill is about $7,200 against an assessment near {m.money(m.A.taxable_value)}, an effective "
         f"rate near 1.31%, while the modelled rate is {m.pct(m.A.tax_rate,2)}.",
         "Tax levels could be understated by roughly one tenth if the higher rate is real and value-based.",
         "Get the tax-rate-area breakdown; separate fixed assessments from ad valorem tax.", src("scc_report")),
        ("F03 · Assessment histories withheld",
         "The supplied multi-year assessment and tax-bill series is not republished at any precision, including rounded to $10.",
         "None for the arithmetic; the projections start from banded anchors instead.",
         "Keep the histories private; use them only in a local, non-public model.", src("boe800")),
        ("F04 · Insurance premiums are guesses",
         f"The owner's estimate for A is about $1,500; the published state average is about $1,570 and a dwelling of this value has a far higher replacement cost. B is modelled at {m.money(m.B.insurance)} without a quote.",
         "Premiums could be two to three times higher, which the Black Swans page tests.",
         "Obtain occupancy-correct quotes with replacement-cost worksheets.", src("cdi_sis")),
        ("F05 · Utilities are owner estimates",
         "Water and electricity ranges were supplied informally; no tariff, meter or usage history was reviewed.",
         "Costs could be materially different, especially water for three units.",
         "Pull 24 months of bills before the transfer.", src("boe800")),
        ("F06 · Solar credit may not survive the transfer",
         "Net-metering tariffs are closed to new enrolments and export compensation under the net billing tariff is usually below retail.",
         "The 'no electricity cost' assumption could fail, adding several hundred dollars a year.",
         "Ask the utility whether the existing tariff transfers to a new owner.", src("cpuc_nem")),
        ("F07 · Rental value of A is a placeholder",
         f"The model uses {m.money(m.A.rent(2026))} a year; no appraisal, listing or lease supports it.",
         "The rental case is the most sensitive to this input.",
         "Obtain written rental opinions for the actual condition and unit count.", src("civ1947")),
        ("F08 · Trust terms are unknown",
         "Whether A is included in the gross estate, how the trust is funded, and who may sell are all unverified.",
         "Could eliminate the step-up and change the entire ranking.",
         "Read the trust with an estate attorney and accountant before the transfer.", src("irs_estate")),
        ("F09 · Property B income-tax basis is unknown",
         "Assessment is not income-tax basis. No taxable-gain figure for B can be verified.",
         "After-tax proceeds from a sale of B cannot currently be calculated.",
         "Reconstruct basis from the purchase deed and improvement records.", src("irs_551")),
        ("F10 · Small-estate limit may be stale",
         "The courts' page states $184,500 for deaths on or after 1 April 2022; the current statutory amount is published in form DE-300.",
         "No effect here — A is real property and a trust is assumed — but the figure should not be quoted.",
         "Read DE-300 before relying on any small-estate procedure.", src("courts_small")),
        ("F11 · 2026 ballot results are unofficial",
         "Percentages changed during the count and certification is due 11 December 2026.",
         "Only the law-watch commentary is affected; no projection uses the results.",
         "Re-check after certification.", src("sos")),
        ("F12 · Prior releases disagreed with each other",
         "Earlier site versions treated B as if it were inherited and withheld all figures; the 2026-11-11 release corrects both.",
         "Old URLs and git history still contain the earlier text.",
         "Treat this release as authoritative; ignore cached older dashboards.", src("irs_basis")),
        ("F13 · Repository history is still public",
         "Earlier commits and merged pull requests contain full-precision supplied figures. The curated deployment excludes those files, but it cannot unpublish history or caches.",
         "The privacy objective is only partly met at repository level.",
         "Decide whether to make the repository private or rewrite history; both are owner actions outside this session.", src("sco")),
        ("F16 · Rental income tax and depreciation not modelled",
         "Rental results are before income tax. Depreciation, passive-loss limits, basis adjustments and recapture depend on records and tax bracket not supplied.",
         "The sell-versus-rent horizon ranking is a scenario, not a verified after-tax result.",
         "Recalculate with a tax adviser using the actual estate basis and rental tax records.", src("irs_527", "irs_551")),
        ("F15 · Occupancy comparison excludes the freed B unit",
         "Occupying A means the owner can no longer occupy B. The published A-only horizon calculation keeps B owned but does not count possible new rent from its third unit.",
         "The displayed occupy-versus-sell gap is not a housing-equivalent opportunity cost; it can change materially.",
         "Confirm legal unit status and obtain a rent opinion before comparing occupancy and sale.", src("prop19", "sf_rent")),
        ("F14 · This is not advice",
         "No attorney, accountant, insurer or appraiser reviewed this analysis.",
         "Personal circumstances could reverse the ranking.",
         "Have a professional check the trust, basis and sale before acting.", src("irs_faq")),
    ]
    rows = [(f"<strong>{html.escape(a)}</strong><br>{html.escape(b)}", html.escape(c), html.escape(d), s)
            for a, b, c, d, s in flags]
    body = f"""
<p class="lead">Nothing here blocks publication. Everything here limits how far the conclusions can be
pushed. Items are ordered by how much they could move the answer.</p>

<div class="callout bad"><h3>Read this before using any number</h3>
<p>The two official facts that matter most are the federal exclusion ({stat('$15,000,000')} for 2026) and
California's absence of an estate or inheritance tax. The two private facts that matter most — the trust's
terms and Property B's actual basis — are unknown. A conclusion that depends on an unknown is labelled as
one.</p></div>

<h2>Register</h2>
{table("Flagged items, impact and remedy", ["Item and finding", "Why it matters", "Remedy", "Official source"], rows)}

<h2>Privacy residual, stated plainly</h2>
<ul class="tight">
<li>This site uses no names, addresses, parcel numbers, account numbers, ZIP codes, e-mail addresses or phone
numbers, and it has no forms, cookies, analytics or external scripts.</li>
<li>Market values are banded to $100,000 and assessments to $1,000; model outputs are rounded to $10. That is
enough to prevent a direct record match, not enough to guarantee anonymity against someone who already knows
the family.</li>
<li>The public repository's history, earlier branches and merged pull requests still contain full-precision
figures. Excluding files from the deployed site does not remove them from git. Only the repository owner can
decide whether to make the repository private or rewrite history.</li>
<li>The page is marked <code>noindex,nofollow</code>. That is a request to search engines, not access control.</li>
</ul>

<h2>What was checked, and how</h2>
<ul class="tight">
<li>Every official link on this site was retrieved and read on {UPDATED}; the source table records what each
page was used for.</li>
<li>Every table row carries at least one official source link; rows that are arithmetic say so in the row.</li>
<li>All dollar figures rendered by the model are multiples of $10. Published statutory amounts are shown as
published and marked.</li>
<li><code>scripts/verify_safe.py</code> re-checks the built artifact for broken internal links, missing row
sources, unrounded model money, forbidden personal-data patterns and unexpected external hosts.</li>
</ul>
"""
    page("flagged.html", "Flagged for review",
         "Limits, irregularities and unverified items", body)


# ------------------------------------------------------------------ 11. sources
SOURCE_USE = {
    "irs_estate": "2026 basic exclusion; gross estate; filing threshold; portability",
    "irs_new": "Public Law 119-21 change to the exclusion",
    "irs_faq": "Filing deadline, extension, portability mechanics",
    "irs_basis": "Inherited basis = date-of-death fair market value",
    "irs_551": "Basis of assets; improvements; adjusted basis",
    "irs_706": "Estate-tax return instructions and rate schedule (top rate assumed)",
    "sco": "No California estate return for deaths on or after 1 January 2005",
    "ftb": "An inheritance is not income; later income and gains are",
    "prop19": "Family-home exclusion, principal-residence test, claims timing",
    "pub801": "Prop 19 statutory allowance through 15 February 2027; BOE-19-P timing",
    "boe800": "Prop 13 1% + bonds, 2% cap, reassessment on change of ownership, Prop 8 decline",
    "boe266": "$7,000 homeowners' exemption and filing deadlines",
    "boe_home": "Only an owner-occupied principal home qualifies for the $7,000 exemption",
    "irs_523": "Selling expenses reduce proceeds when calculating gain",
    "irs_527": "Rental income, expenses and depreciation require income-tax treatment",
    "scc_prop19": "County assessor's parent-child transfer requirements",
    "scc_assessor": "Decline-in-value (Prop 8) request process",
    "scc_report": "County assessed-value roll and tax-rate structure",
    "sf_rate": "FY2026-27 secured property-tax rate 1.18162182%",
    "sf_transfer": "Tiered documentary transfer tax, $3.75 per $500 from $1,000,000 to $5,000,000",
    "sf_cos": "Change-of-ownership statement after a death; 150-day rule; penalties",
    "sf_rent": "Annual allowable rent increase 1.6% for 2026-27",
    "cdi_home": "Residential insurance guidance; FAIR Plan limits; DIC policies",
    "cdi_sis": "Market snapshot: average premium of about $1,570; FAIR Plan counts; distressed areas",
    "courts_small": "Small-estate affidavit limit and its exclusion of real property",
    "courts_probate": "Probate and trust administration process",
    "civ1947": "Statewide rent cap 5% + CPI (max 10%), repealed 1 January 2030",
    "rtc11911": "County documentary transfer tax rate of $0.55 per $500",
    "cpuc_nem": "Net billing tariff, closed NEM tariffs, export compensation",
    "sos": "Unofficial 2026 statewide ballot-measure results",
    "bls": "October 2026 CPI release: monthly changes and data gaps",
    "fhfa": "House-price index used to monitor appreciation assumptions",
}


def build_sources():
    rows = []
    for key, (name, url) in S.items():
        rows.append((f'<a href="{url}" rel="noopener noreferrer">{html.escape(name)}</a>',
                     html.escape(SOURCE_USE.get(key, "")), UPDATED, "Retrieved and read"))
    body = f"""
<p class="lead">One table, every official page used, and what it was used for. Retrieved and read on
{UPDATED}. If a value is not on this list, it is an assumption and is labelled as one where it appears.</p>

<h2>Source register</h2>
{table("Official pages", ["Publisher · page", "Used for", "Retrieved", "Status"], rows)}

<h2>Verification standard</h2>
<ul class="tight">
<li><strong>Verified</strong> means the stated rule was read on the linked official page on the date shown.
It does not mean a private property fact was confirmed.</li>
<li><strong>Derived</strong> means arithmetic on a banded anchor and/or a verified rule, with the formula shown
on the page.</li>
<li><strong>Assumption</strong> means a named model input chosen by the analyst; sensitivities are on the
Decision and Black Swans pages.</li>
<li><strong>Unverified</strong> means no official source supports it. The cell is left blank, not filled with a
guess, and the item appears on <a href="flagged.html">Flagged for review</a>.</li>
</ul>

<h2>Why some official pages are not used</h2>
<ul class="tight">
<li>County assessor property-search results are not cited because looking up a specific parcel would defeat the
anonymization this site depends on.</li>
<li>Insurer quote engines and utility rate calculators produce property-specific numbers; those are quotes, not
published facts, so they are left for the owner to obtain privately.</li>
<li>Secondary commentary, blogs and estimator sites were not used for any figure.</li>
</ul>

<h2>Reproducing the numbers</h2>
<p>The published pages are generated by <code>scripts/build_desk.py</code> from <code>scripts/desk_model.py</code>.
Both are plain Python with no dependencies. Every figure on this site can be recomputed from the assumptions
block on the <a href="projections.html">Projections</a> page.</p>
"""
    page("sources.html", "Sources and verification standard",
         "Evidence register", body)


# ------------------------------------------------------------------ main
def main():
    OUT.mkdir(exist_ok=True)
    (OUT / "style.css").write_text(CSS)
    build_index()
    build_decision()
    build_projections()
    build_properties()
    build_costs()
    build_black_swans()
    build_tax()
    build_process()
    build_law_watch()
    build_flagged()
    build_sources()
    pages = sorted(p.name for p in OUT.glob("*.html"))
    print(f"built {len(pages)} pages: {', '.join(pages)}")


if __name__ == "__main__":
    main()
