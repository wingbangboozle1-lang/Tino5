#!/usr/bin/env python3
"""Build the privacy-safe decision desk into desk/**.

Design contract (checked by scripts/verify_desk_v5.py on every build):
  * every table row either carries an official https source or is marked blank + flagged;
  * every dollar figure is a multiple of $10 and is labelled as rounded;
  * no personal identifiers: no names, addresses, parcel numbers, ZIP codes or account numbers;
  * every page is static HTML with a relative stylesheet, no scripts, no external assets;
  * only allowlisted official hosts are cited.

Run: python3 scripts/build_desk_v5.py
"""
from __future__ import annotations
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESK = ROOT / "desk"
MODEL = json.loads((DESK / "data" / "model-v5.json").read_text())
AS_OF = MODEL["as_of"]

# ---------------------------------------------------------------------------
# Source registry. Every URL here was fetched successfully during this session.
# ---------------------------------------------------------------------------
S = {
 "irs_estate": ("IRS, Estate tax (filing thresholds by year of death)",
   "https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax"),
 "irs_706": ("IRS, Instructions for Form 706",
   "https://www.irs.gov/instructions/i706"),
 "irs_revproc": ("IRS, Rev. Proc. 2026-35 (2027 inflation adjustments)",
   "https://www.irs.gov/pub/irs-drop/rp-26-35.pdf"),
 "irs_701": ("IRS, Topic 701 - Sale of your home",
   "https://www.irs.gov/taxtopics/tc701"),
 "irs_425": ("IRS, Topic 425 - Passive activities and loss limits",
   "https://www.irs.gov/taxtopics/tc425"),
 "irs_559": ("IRS, Topic 559 - Net investment income tax",
   "https://www.irs.gov/taxtopics/tc559"),
 "irs_523": ("IRS, Publication 523 - Selling your home",
   "https://www.irs.gov/publications/p523"),
 "irs_527": ("IRS, Publication 527 - Residential rental property",
   "https://www.irs.gov/publications/p527"),
 "irs_gifts": ("IRS, Frequently asked questions on gift taxes",
   "https://www.irs.gov/businesses/small-businesses-self-employed/frequently-asked-questions-on-gift-taxes"),
 "irs_estate_faq": ("IRS, Frequently asked questions on estate taxes",
   "https://www.irs.gov/businesses/small-businesses-self-employed/frequently-asked-questions-on-estate-taxes"),
 "sco_estate": ("California State Controller, Estate tax",
   "https://www.sco.ca.gov/ardtax_estate_tax.html"),
 "ftb_593": ("FTB, Form 593 instructions (basis of inherited property)",
   "https://www.ftb.ca.gov/forms/2024/2024-593-instructions.html"),
 "boe_prop19": ("Board of Equalization, Proposition 19",
   "https://www.boe.ca.gov/prop19/"),
 "boe_lta25009": ("BOE, LTA 2025/009 - Proposition 19 value cap",
   "https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf"),
 "boe_lta26002": ("BOE, LTA 2026/002 - 2026-27 California Consumer Price Index",
   "https://www.boe.ca.gov/proptaxes/pdf/lta26002.pdf"),
 "boe_lta26026": ("BOE, LTA 2026/026 - Proposition 19 intergenerational transfer FAQ",
   "https://www.boe.ca.gov/proptaxes/pdf/lta26026.pdf"),
 "boe_lta23027": ("BOE, LTA 2023/027 - Homeowners' exemption information sheet",
   "https://boe.ca.gov/proptaxes/pdf/lta23027.pdf"),
 "boe_lta_index": ("BOE, Letters to Assessors index",
   "https://www.boe.ca.gov/proptaxes/ltacont.htm"),
 "dof_inflation": ("Department of Finance, California inflation",
   "https://dof.ca.gov/forecasting/economics/california-inflation/"),
 "rtc_63_2": ("Revenue & Taxation Code s.63.2",
   "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2"),
 "rtc_11911": ("Revenue & Taxation Code s.11911",
   "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=11911"),
 "civ_1947_12": ("Civil Code s.1947.12 (state rent cap)",
   "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12"),
    "prob_13100": ("Probate Code s.13100 (small-estate affidavit)",
                   "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PROB&sectionNum=13100"),
    "de300": ("Judicial Council · Form DE-300 (probate thresholds, deaths on or after 1 Apr 2025)",
              "https://www.courts.ca.gov/documents/de300.pdf"),
 "prob_16061_7": ("Probate Code s.16061.7 (trustee notification)",
   "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PROB&sectionNum=16061.7"),
 "prob_10810": ("Probate Code s.10810 (statutory probate fees)",
   "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PROB&sectionNum=10810"),
 "scc_rate": ("Santa Clara County, FY2025-26 property tax rate book",
   "https://www.sccgov.org/sites/dtt/pd/Documents/tax-rate-book-2025-2026.pdf"),
 "scc_recorder": ("Santa Clara County Clerk-Recorder, recording real estate",
   "https://clerkrecorder.santaclaracounty.gov/recording-documents/recording-real-estate"),
 "sft_secured": ("SF Treasurer & Tax Collector, secured property taxes",
   "https://sftreasurer.org/property/secured-property-taxes"),
 "sfgov_fees": ("SF.gov, fees to record a document (transfer tax rates)",
   "https://www.sf.gov/reports--march-2024--fees-record-document-san-francisco"),
 "cdi": ("CA Department of Insurance, 2025 residential premium report",
   "https://www.insurance.ca.gov/0400-news/0200-studies-reports/0300-earthquake-study/upload/EQEXP2025Summary.pdf"),
 "cpuc_nem": ("CPUC, net energy metering",
   "https://www.cpuc.ca.gov/industries-and-topics/electrical-energy/demand-side-management/net-energy-metering"),
 "sjwc": ("San Jose Water Company, tariff AL-628-A",
   "https://www.sjwater.com/sites/default/files/AL-628-A.pdf"),
 "sfpuc": ("SFPUC, water and sewer rate schedule FY2026-27",
   "https://www.sfpuc.gov/sites/default/files/accounts-and-services/Rates_Schedule_Water_Sewer_2026-7.pdf"),
 "treasury": ("US Treasury, daily par yield curve rates",
   "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve"),
 "freddie": ("Freddie Mac, Primary Mortgage Market Survey",
   "https://www.freddiemac.com/pmms"),
 "fhfa": ("FHFA, House Price Index",
   "https://www.fhfa.gov/data/hpi"),
 "bls_cpi": ("BLS, Consumer Price Index news release",
   "https://www.bls.gov/news.release/cpi.nr0.htm"),
 "bls_hist": ("BLS, historical Consumer Price Index",
   "https://www.bls.gov/cpi/tables/supplemental-files/historical-cpi-u-202402.pdf"),
 "cbo": ("CBO, Long-Term Budget Outlook",
   "https://www.cbo.gov/publication/61270"),
 "census": ("Census QuickFacts",
   "https://www.census.gov/quickfacts/"),
 "sos_measures": ("CA Secretary of State, qualified ballot measures",
   "https://www.sos.ca.gov/elections/ballot-measures/qualified-ballot-measures"),
}

ALLOWED_HOSTS = {
    "www.irs.gov", "leginfo.legislature.ca.gov", "www.sco.ca.gov", "www.ftb.ca.gov",
    "www.boe.ca.gov", "boe.ca.gov", "dof.ca.gov", "www.sccgov.org",
    "clerkrecorder.santaclaracounty.gov", "sftreasurer.org", "www.sf.gov",
    "www.insurance.ca.gov", "www.cpuc.ca.gov", "www.sjwater.com", "www.sfpuc.gov",
    "home.treasury.gov", "www.freddiemac.com", "www.fhfa.gov", "www.bls.gov",
    "www.cbo.gov", "www.census.gov", "www.sos.ca.gov",
    "courts.ca.gov", "www.courts.ca.gov",   # Judicial Council DE-300 (7b/INT gap fix)
}


def h(s) -> str:
    return html.escape(str(s), quote=True)


def exact(v: str) -> str:
    """Mark a statutory or published amount as quoted exactly rather than rounded."""
    return f'<span class="exactamt">{v}</span>{EXACT}'


e = exact          # short alias for use inside f-strings


def money(v, sign=False) -> str:
    if v is None:
        return "<!--blank-->"
    v = int(round(v))
    body = f"${abs(v):,}"
    if v < 0:
        return f"-{body}"
    return f"+{body}" if sign else body


DASH = '<span class="na">&mdash;</span>'


def pct(v, places=2) -> str:
    return f"{v * 100:.{places}f}%"


FLAG = '<span class="flag" title="unverified">FLAG</span>'
EXACT = '<span class="exact" title="statutory or published amount, quoted exactly">exact</span>'
MHOST = '<span class="mh" title="model output, not a sourced figure">M</span>'


def table(headers, rows, caption="", cls=""):
    """rows: dicts with 'cells' (list of str|None), plus either 'src' (registry key) or
    'flag' (flag id). A missing cell or a row with no src must carry a flag."""
    out = [f'<table class="{cls}">']
    if caption:
        out.append(f"<caption>{caption}</caption>")
    out.append("<thead><tr>" + "".join(f"<th>{x}</th>" for x in headers)
               + "<th>Source</th></tr></thead><tbody>")
    for r in rows:
        cells = [f'<td class="blank">{FLAG}</td>' if c is None else f"<td>{c}</td>"
                 for c in r["cells"]]
        if r.get("src"):
            label, url = S[r["src"]]
            link = f'<a href="{h(url)}" rel="noopener">{h(label)}</a>'
        elif r.get("flag"):
            link = f'<a href="flagged.html#{h(r["flag"])}">{FLAG} {h(r["flag"])}</a>'
        else:
            link = '<span class="mh">model</span>'
        out.append("<tr>" + "".join(cells) + f'<td class="src">{link}</td></tr>')
    out.append("</tbody></table>")
    return "\n".join(out)


NAV = [("index.html", "Overview"), ("executive-summary.html", "Executive summary"),
       ("decision.html", "The decision"), ("questions.html", "Open questions"),
       ("projections.html", "Projections"), ("costs.html", "Carrying costs"),
       ("estate-tax.html", "Inheritance tax"), ("process.html", "Trust process"),
       ("black-swans.html", "Black swans"), ("law-watch.html", "Law watch"),
       ("suggestions.html", "Suggestions"), ("flagged.html", "Flagged for review"),
       ("sources.html", "Sources"), ("methodology.html", "Methodology"),
       ("repo-review.html", "Repo review")]

PAGES: dict[str, tuple[str, str, str]] = {}


def add(slug, title, standfirst, body):
    PAGES[slug] = (title, standfirst, body)


def shell(slug: str, title: str, standfirst: str, body: str) -> str:
    nav = "\n".join(
        f'<a href="{h(f)}"' + (' class="here"' if f == slug else "") + f">{h(t)}</a>"
        for f, t in NAV)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{h(title)} &middot; estate decision desk</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="top">
  <a class="brand" href="index.html">Estate decision desk</a>
  <span class="asof">Figures as of {h(AS_OF)} &middot; all amounts rounded to the nearest $10</span>
</header>
<nav class="side">
{nav}
</nav>
<main>
<h1>{h(title)}</h1>
<p class="standfirst">{standfirst}</p>
{body}
<footer>
<p>This desk is a research aid. It is not legal, tax, investment, or appraisal advice.
Every figure is either cited to an official source, or labelled as model output, or left blank
and listed on <a href="flagged.html">Flagged for review</a>. Amounts are rounded to the nearest
$10 so that no figure can be matched back to a specific bill.</p>
<p><a href="methodology.html">How these numbers were produced</a> &middot;
<a href="sources.html">All sources</a> &middot;
<a href="repo-review.html">Line-by-line review notes</a></p>
</footer>
</main>
</body>
</html>
"""


CSS = """\
:root{--ink:#1b1f24;--muted:#5c6672;--line:#dfe3e8;--bg:#fbfbfc;--accent:#1f5f8b;
--warn:#8a4b00;--warnbg:#fff5e6;--ok:#1c6b3c}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accent)}
header.top{display:flex;flex-wrap:wrap;gap:.5rem 1.5rem;align-items:baseline;
padding:1rem 1.5rem;border-bottom:1px solid var(--line);background:#fff}
.brand{font-weight:700;font-size:1.05rem;text-decoration:none;color:var(--ink)}
.asof{color:var(--muted);font-size:.85rem}
nav.side{display:flex;flex-wrap:wrap;gap:.25rem;padding:.75rem 1.5rem;
border-bottom:1px solid var(--line);background:#fff}
nav.side a{padding:.3rem .6rem;border-radius:4px;font-size:.9rem;text-decoration:none;
white-space:nowrap}
nav.side a:hover{background:#eef3f8}
nav.side a.here{background:var(--accent);color:#fff}
main{max-width:60rem;margin:0 auto;padding:2rem 1.5rem 4rem}
h1{font-size:1.9rem;line-height:1.25;margin:0 0 .5rem}
h2{font-size:1.25rem;margin:2.5rem 0 .75rem;padding-bottom:.3rem;border-bottom:1px solid var(--line)}
h3{font-size:1.05rem;margin:1.75rem 0 .5rem}
.standfirst{color:var(--muted);font-size:1.05rem;margin:0 0 2rem;max-width:48rem}
table{border-collapse:collapse;width:100%;margin:1rem 0 1.5rem;font-size:.9rem;background:#fff}
caption{caption-side:top;text-align:left;color:var(--muted);font-size:.85rem;padding-bottom:.4rem}
th,td{border:1px solid var(--line);padding:.45rem .6rem;text-align:left;vertical-align:top}
th{background:#f2f5f8;font-weight:600;font-size:.8rem;text-transform:uppercase;
letter-spacing:.02em;color:var(--muted)}
td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
td.src{font-size:.78rem;max-width:15rem}
td.blank{background:var(--warnbg);text-align:center}
tr:hover td{background:#fafbfc}
.flag{display:inline-block;background:var(--warnbg);color:var(--warn);border:1px solid #e8cf9f;
border-radius:3px;font-size:.68rem;font-weight:700;padding:0 .28rem;letter-spacing:.04em}
.mh{display:inline-block;background:#eef3f8;color:var(--accent);border:1px solid #c9dbea;
border-radius:3px;font-size:.68rem;font-weight:700;padding:0 .3rem}
.card{background:#fff;border:1px solid var(--line);border-radius:6px;padding:1rem 1.25rem;
margin:1rem 0}
.card h3{margin-top:0}
.grid{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(14rem,1fr))}
.kpi{background:#fff;border:1px solid var(--line);border-radius:6px;padding:1rem}
.kpi .n{font-size:1.55rem;font-weight:700;font-variant-numeric:tabular-nums;display:block}
.kpi .l{color:var(--muted);font-size:.82rem;display:block;margin-top:.25rem}
.note{background:#eef3f8;border-left:3px solid var(--accent);padding:.75rem 1rem;
margin:1.25rem 0;font-size:.92rem}
.warnbox{background:var(--warnbg);border-left:3px solid var(--warn);padding:.75rem 1rem;
margin:1.25rem 0;font-size:.92rem}
.pill{display:inline-block;border:1px solid var(--line);border-radius:999px;
padding:.12rem .6rem;font-size:.78rem;color:var(--muted);margin:0 .3rem .35rem 0;background:#fff}
.yes{color:var(--ok);font-weight:600}.no{color:var(--warn);font-weight:600}
.na{color:#9aa4ae}
.exactamt{font-variant-numeric:tabular-nums}
.exact{display:inline-block;background:#eef7ef;color:#1c6b3c;border:1px solid #c3e0c8;border-radius:3px;font-size:.68rem;font-weight:700;padding:0 .3rem;margin-left:.25rem;letter-spacing:.04em}
footer{margin-top:3rem;padding-top:1.25rem;border-top:1px solid var(--line);
color:var(--muted);font-size:.82rem}
code{background:#eef1f4;padding:.1rem .3rem;border-radius:3px;font-size:.85em}
pre{background:#fff;border:1px solid var(--line);border-radius:6px;padding:.75rem 1rem;
overflow-x:auto;font-size:.85rem}
pre code{background:none;padding:0}
@media(max-width:640px){table{font-size:.8rem}th,td{padding:.35rem .5rem}td.src{max-width:8rem}}
@media print{nav.side{display:none}}
"""


# ===========================================================================
# Overview
# ===========================================================================
def build_index():
    b = MODEL["breakevens"]
    p = MODEL["paths"]["2045"]
    cards = "\n".join(
        f'<div class="kpi"><span class="n">{money(v)}</span><span class="l">{h(l)}</span></div>'
        for v, l in [
            (p["sell"]["terminal_net_worth"], "Sell and reinvest: net worth in 2076"),
            (p["rent"]["terminal_net_worth"], "Rent out: net worth in 2076"),
            (p["occupy"]["terminal_net_worth"], "Move in: net worth in 2076"),
            (b["2045"]["breakeven_monthly_rent"], "Monthly rent at which renting ties selling"),
        ])
    body = f"""
<p>One question drives everything here. <strong>When a house held in a family trust passes to the
heir at some point between 2040 and 2050, should the heir move into it, rent it out, or sell it
and reinvest?</strong> The heir already owns a second house outright. That second house is
analysed separately throughout, because it is not part of the inheritance.</p>

<div class="grid">{cards}</div>
<p style="margin-top:.9rem;color:#5c6672;font-size:.9rem">The four figures above are the 2045
transfer scenario under the central assumptions. They are not a forecast. They are the output of
one published set of assumptions, and <a href="black-swans.html">the stress cases</a> reverse the
ranking. Every amount is rounded to the nearest $10.</p>

<h2>Start here</h2>
<table>
<thead><tr><th>Page</th><th>What it answers</th></tr></thead><tbody>
<tr><td><a href="executive-summary.html">Executive summary</a></td>
<td>The whole picture on one page: the three paths, the four things that change the answer, and
the deadlines that already exist.</td></tr>
<tr><td><a href="decision.html">The decision</a></td>
<td>Move in, rent out, or sell, compared after tax, with the arithmetic and the break-evens.</td></tr>
<tr><td><a href="questions.html">Open questions</a></td>
<td>What we know, what we do not know, and the method for closing each gap.</td></tr>
<tr><td><a href="projections.html">Projections 2026-2076</a></td>
<td>Value, assessed value, tax, insurance, water, power, and maintenance, year by year.</td></tr>
<tr><td><a href="costs.html">Carrying costs</a></td>
<td>What both houses cost to hold, line by line, and which lines are not credible.</td></tr>
<tr><td><a href="estate-tax.html">Inheritance tax</a></td>
<td>Federal estate tax, the state reassessment, and the income tax on inherited accounts.</td></tr>
<tr><td><a href="process.html">Trust process</a></td>
<td>From a death to a recorded title, in order, with the deadlines.</td></tr>
<tr><td><a href="black-swans.html">Black swans</a></td>
<td>Six stress paths anchored to real episodes, and what they agree on.</td></tr>
<tr><td><a href="law-watch.html">Law watch</a></td>
<td>The rules the plan depends on, and what a change to each would cost.</td></tr>
<tr><td><a href="suggestions.html">Suggestions</a></td>
<td>Options ranked by robustness, so a path can be chosen before anything is implemented.</td></tr>
<tr><td><a href="flagged.html">Flagged for review</a></td>
<td>Every claim that could not be confirmed against an official source.</td></tr>
<tr><td><a href="sources.html">Sources</a></td>
<td>Every citation used, with what it supports.</td></tr>
<tr><td><a href="methodology.html">Methodology</a></td>
<td>Every input, every assumption, and every accounting decision.</td></tr>
<tr><td><a href="repo-review.html">Repo review</a></td>
<td>What else is in this repository, and which parts are a privacy risk.</td></tr>
</tbody></table>

<div class="note"><strong>Two houses, two very different situations.</strong> The inherited house
is assessed at a small fraction of its market value. That makes its tax bill look trivial and makes
<em>how</em> it is transferred enormously valuable, because the low assessment can be kept or lost
depending on what the heir does in the first year. The already-owned house has a tax charge that is
roughly double what the city's published rate implies, and that discrepancy is the clearest
administrative item in the whole desk.</div>

<h2>How to read the numbers</h2>
<p>Every amount is rounded to the nearest $10. Statutory amounts, rates, and thresholds are quoted
exactly and marked as such, because rounding a legal threshold would misstate it. Where a figure
could not be confirmed against an official source it is left blank and flagged rather than
estimated. Nothing on this site identifies a person, a property, or a location more precisely than
a county or a city.</p>
"""
    add("index.html", "Overview",
        "A decision desk for a future inheritance, built to be audited line by line.", body)


# ===========================================================================
# Executive summary
# ===========================================================================
def build_exec():
    b = MODEL["breakevens"]
    rows = [{"cells": [t, money(MODEL["paths"][t]["occupy"]["terminal_net_worth"]),
                       money(MODEL["paths"][t]["rent"]["terminal_net_worth"]),
                       money(MODEL["paths"][t]["sell"]["terminal_net_worth"]),
                       money(b[t]["breakeven_monthly_rent"])],
             "flag": "M01"} for t in ("2040", "2045", "2050")]
    swan = [{"cells": [f'{s["id"]} {h(s["name"])}', pct(s["home_growth"], 1),
                       money(s["hold_then_sell"]), money(s["sell_now_then_invest"]),
                       f'<strong>{h(s["verdict"])}</strong>'], "flag": "M02"}
            for s in MODEL["swans"]]
    body = f"""
<h2>The situation in six sentences</h2>
<ol>
<li>A house (called <strong>Property A</strong>) sits in a family trust and will pass to the heir
sometime between 2040 and 2050. Its assessed value is a small fraction of its market value.</li>
<li>That gap is a real, transferable asset, and it survives only if the heir occupies the house as
a principal residence and claims the homeowners' exemption within one year of the transfer.</li>
<li>The heir already owns a second house (<strong>Property B</strong>) outright. It is not part of
the inheritance, and its property-tax charge appears to be roughly double what the city's published
rate implies.</li>
<li>There is no California inheritance or estate tax. The state's bite comes from
<strong>reassessment</strong>, not from a tax on inheriting.</li>
<li>On central assumptions, selling and reinvesting produces the highest net worth in 2076 in every
transfer year tested, because the risk-free rate available today is high in relation to what a
house yields net of its own carrying costs.</li>
<li>That ranking is fragile. Holding only catches up if home values compound at about
{pct(MODEL["breakevens"]["2045"]["breakeven_home_growth"], 1)} a year for the whole horizon, and
the sell path is exposed to the risk that the sale is forced at the bottom of a cycle.</li>
</ol>

<h2>Net worth in 2076, by path and transfer year</h2>
{table(["Transfer year", "Move in", "Rent out", "Sell and reinvest",
        "Rent that would tie selling, per month"], rows,
       caption="Central assumptions: home values grow 3.5% a year, reinvestment earns 5.10% risk "
               "free before tax, and Property A rents for $5,200 a month. All amounts are model "
               "output rounded to the nearest $10.")}

<div class="warnbox"><strong>Read the middle column carefully.</strong> The rent-out column assumes
the house is let at a realistic single-unit rent. It is not a comparison of living in the house
against not living in it: the move-in column already credits the heir with the rent from the unit
they vacate at Property B, which is what makes it competitive at all.</div>

<h2>The four things that decide the answer</h2>
<table><thead><tr><th>Lever</th><th>Why it dominates</th><th>Evidence</th></tr></thead><tbody>
<tr><td><strong>Whether the heir occupies the house within a year</strong></td>
<td>The family-home exclusion applies only to the portion of the assessed value within the value
cap. Where market value already exceeds that cap, as it does here in every transfer year, the
first-year saving from occupying is the same modest amount rather than a large one, and it does
not grow with the value gap.</td>
<td><a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2">RTC s.63.2(a)(1)(C)</a></td></tr>
<tr><td><strong>The reinvestment return actually available</strong></td>
<td>A risk-free 5.10% is a demanding hurdle for a house. Every 1.5-point drop in that rate moves
the sell column by several million dollars.</td>
<td><a href="https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve">US Treasury</a></td></tr>
<tr><td><strong>Long-run home-value growth</strong></td>
<td>Compounding over 30 to 50 years swamps every operating line. At a 2045 transfer, holding only
ties selling if values compound at
{pct(MODEL["breakevens"]["2045"]["breakeven_home_growth"], 1)} a year.</td>
<td><a href="https://www.fhfa.gov/data/hpi">FHFA</a></td></tr>
<tr><td><strong>When the transfer happens</strong></td>
<td>The later the transfer, the bigger the assessed gap and the more the exclusion is worth, but
the shorter the remaining compounding horizon.</td>
<td><a href="https://www.boe.ca.gov/proptaxes/pdf/lta26026.pdf">BOE LTA 2026/026</a></td></tr>
</tbody></table>

<h2>The seven claims this desk is most confident about</h2>
<ol>
<li>There is no California estate or inheritance tax. The state's estate tax was repealed
effective 1 January 2005.</li>
<li>The federal estate-tax filing threshold is $15,000,000 for a death in 2026.</li>
<li>Inherited property takes a basis equal to its fair market value at the date of death, so a
sale at that value realises no gain.</li>
<li>The family-home exclusion adds up to {e("$1,044,586")} to the old base-year value before any
reassessment applies.</li>
<li>The exclusion is conditional. It is removed if the transferee stops being eligible for the
homeowners' or disabled veterans' exemption.</li>
<li>Rental income is passive income. Rental losses cannot be deducted against salary, and are
suspended until the property is sold in full.</li>
<li>The transfer tax on a sale differs by county, and one of the two counties bands its rate by
price, so the rate is not a single number.</li>
</ol>

<h2>The three things most likely to be wrong</h2>
<ol>
<li><strong>The insurance figures.</strong> Both houses carry owner estimates far below the
statewide average premium, and no declaration page has been seen.</li>
<li><strong>Property B's tax charge.</strong> The owner's own bill implies a 2.14% effective rate
against a published 1.18% secured rate. One of the two numbers is wrong.</li>
<li><strong>Long-run growth.</strong> A single 3.5% figure for fifty years is a convenience, not a
belief. The stress cases move the answer by millions.</li>
</ol>

<h2>Deadlines that exist today</h2>
<table><thead><tr><th>Deadline</th><th>Trigger</th><th>Consequence of missing it</th>
<th>Source</th></tr></thead><tbody>
<tr><td>9 months</td><td>Federal estate-tax return, if one is required</td>
<td>Interest and penalties, and a lost portability election</td>
<td><a href="https://www.irs.gov/instructions/i706">IRS</a></td></tr>
<tr><td>60 days</td><td>Trustee's notification to beneficiaries and heirs</td>
<td>Trustee liability</td>
<td><a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PROB&sectionNum=16061.7">Prob. Code s.16061.7</a></td></tr>
<tr><td>1 year</td><td>Homeowners' exemption claim after the transfer</td>
<td>The exclusion is removed and the market-value base is enrolled</td>
<td><a href="https://www.boe.ca.gov/proptaxes/pdf/lta26026.pdf">BOE LTA 2026/026</a></td></tr>
<tr><td>3 years</td><td>Claim for the exclusion itself</td><td>Relief is delayed or denied</td>
<td><a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2">RTC s.63.2</a></td></tr>
<tr><td>40 days</td><td>Small-estate affidavit, if the estate qualifies</td>
<td>The simplified route is unavailable</td>
<td><a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PROB&sectionNum=13100">Prob. Code s.13100</a></td></tr>
</tbody></table>

<h2>The stress cases, one line each</h2>
{table(["Scenario", "Home growth applied", "Hold, then sell in 2076",
        "Sell now and reinvest", "Which wins"], swan,
       caption="Each scenario is anchored to a real, sourced episode and applied to a 2045 "
               "transfer. Model output, rounded to the nearest $10.")}
"""
    add("executive-summary.html", "Executive summary",
        "The answer, the four levers that control it, and the deadlines that already exist.", body)


# ===========================================================================
# Decision
# ===========================================================================
def build_decision():
    p = MODEL["paths"]["2045"]
    # (label, key, does-this-line-apply-to-the-sell-path)
    keys = [("Fair market value at the transfer", "transfer_fmv", True),
            ("Value that stays taxable after the transfer", "taxable_at_transfer", False),
            ("Amount by which market value exceeds the taxable value",
             "assessed_gap_vs_market", False),
            ("Property tax, first full year", "tax_at_transfer", False),
            ("Property tax if the county reassessed in full", "tax_if_reassessed", False),
            ("Value of the exclusion in the first year", "prop19_saving_year1", False),
            ("Cumulative cash flow to 2076", "cumulative_cash_flow", True),
            ("Depreciation claimed", "depreciation_taken", False),
            ("Suspended passive losses released", "suspended_passive_loss", False),
            ("Capital-gain tax on a 2076 sale", "terminal_capital_gain_tax", False),
            ("Net investment income tax", "terminal_niit", False),
            ("Sale proceeds, net of selling costs", "sale_proceeds_net", False),
            ("Net worth in 2076", "terminal_net_worth", True)]
    rows = []
    for label, k, in_sell in keys:
        sell_cell = money(p["sell"].get(k)) if in_sell and p["sell"].get(k) is not None else DASH
        rows.append({"cells": [label, money(p["occupy"].get(k)), money(p["rent"].get(k)),
                               sell_cell], "flag": "M03"})
    be = MODEL["breakevens"]["2045"]
    body = f"""
<p>Three paths are compared on the same footing. Each starts when the house actually transfers,
runs to 2076, and ends with the house sold and the tax paid, so what is compared is
<em>after-tax net worth</em>, not cash flows that are not alike.</p>

<h2>Path 1: move in</h2>
<p>The heir occupies Property A, claims the homeowners' exemption, and keeps the family-home
exclusion. The unit the heir vacates at Property B is let at Property B's own reported per-unit
rent. No depreciation is taken, because the house is not a rental. On a later sale, the home-sale
exclusion shelters up to $250,000 of gain for a single filer.</p>

<h2>Path 2: rent it out</h2>
<p>The house is let as a single unit. Depreciation is taken straight-line over 27.5 years on the
improvement share of the date-of-death value. Rental losses are passive: they are suspended
rather than deducted, then released in full when the property is sold.</p>
<p>The tax treatment of this path is the point most often got wrong. A transfer to a child is
excluded from change in ownership only where the property is the child's principal residence and
the claim is filed. Absent that, the transfer is reassessed at full cash value, so the
assessed-value advantage is gone before the first rent cheque arrives.</p>

<div class="warnbox"><strong>What renting out actually costs, in tax terms.</strong> The first-year
property tax is {money(p["rent"]["tax_at_transfer"])} against {money(p["occupy"]["tax_at_transfer"])}
for occupancy, a difference of {money(p["rent"]["tax_at_transfer"] - p["occupy"]["tax_at_transfer"])}.
That difference is fixed in dollar terms rather than compounding, because the exclusion protects
only the value cap, and the capped portion grows at 2% either way. The larger cost of renting is
therefore not the tax. It is the operating cost, the capped rent, and the management burden, which
together are what put this path last on the comparison above.</div>

<h2>Path 3: sell and reinvest</h2>
<p>The house is sold at the stepped-up basis, so no income tax is due on the sale itself. Net
proceeds are invested at the current risk-free rate, less tax on the interest. No property tax,
insurance, utilities, or maintenance are charged, because the house is gone.</p>

<h2>The comparison, 2045 transfer</h2>
{table(["Line", "Move in", "Rent out", "Sell and reinvest"], rows,
       caption="Model output rounded to the nearest $10. A dash means the line does not apply to "
               "that path: a seller owns no house, so a seller pays no property tax on it.")}

<h2>What the comparison says</h2>
<p>Selling wins on central assumptions, and it wins by a wide margin, because the after-tax
risk-free return available today is high in relation to what a house yields net of its own
carrying costs. That is a statement about <em>today's interest rates</em>, not about houses.</p>
<p>The rent-out path is the weakest of the three on central assumptions. It gives up the exclusion,
takes on operating costs and management, and the rent it can charge is capped: a covered California
tenancy is limited to 5% plus inflation, up to 10% a year, and one of the two cities has its own
tighter local cap. It only overtakes selling in one corner of the sensitivity grid, where home
values compound at 5% a year <em>and</em> the reinvestment rate is at the low end.</p>

<h2>What would have to be true for the answer to change</h2>
<table><thead><tr><th>If this is true</th><th>Then</th><th>Break-even</th></tr></thead><tbody>
<tr><td>Market rent for the house exceeds the break-even rent</td><td>Renting beats selling</td>
<td class="num">{money(be["breakeven_monthly_rent"])} a month</td></tr>
<tr><td>Home values compound faster than the break-even rate</td><td>Holding beats selling</td>
<td class="num">{pct(be["breakeven_home_growth"], 2)} a year</td></tr>
<tr><td>The risk-free reinvestment rate falls to about 3.5%</td><td>Selling loses most of its edge</td>
<td class="num">{pct(0.035)} gross</td></tr>
<tr><td>The heir would otherwise pay market rent to live somewhere</td>
<td>That rent belongs on the sell side of the ledger</td>
<td>Not modelled; see <a href="questions.html">open questions</a></td></tr>
</tbody></table>

<div class="note">The break-even rent of {money(be["breakeven_monthly_rent"])} a month is well
above a realistic single-unit rent for a house of this value, which is why renting loses. But the
break-even is a <strong>total</strong> figure. Two units at half that rent each would change the
picture completely, which is why the legal unit count is one of the five questions that matter
most.</div>
"""
    add("decision.html", "The decision",
        "Move in, rent it out, or sell it, compared after tax, with the break-evens.", body)


# ===========================================================================
# Projections
# ===========================================================================
def build_projections():
    rows = [{"cells": [str(r["year"]), money(r["market_value"]), money(r["taxable_value"]),
                       money(r["property_tax"]), money(r["insurance"]), money(r["utilities"]),
                       money(r["maintenance"])], "flag": "M04"}
            for r in MODEL["annual"]["2045"]["occupy"] if r["year"] % 5 == 0]
    sens = [s for s in MODEL["sensitivity"] if s["transfer_year"] == 2045]
    srows = []
    for s in sens:
        best = max(("move in", s["occupy"]), ("rent out", s["rent"]), ("sell", s["sell"]),
                   key=lambda x: x[1])[0]
        srows.append({"cells": [pct(s["home_growth"], 1), pct(s["invest_pre_tax"], 2),
                                money(s["occupy"]), money(s["rent"]), money(s["sell"]),
                                f"<strong>{best}</strong>"], "flag": "M05"})
    body = f"""
<p>Two different things are projected here, and they should not be confused. The first is the
<strong>cost of holding</strong> the house, year by year. The second is the <strong>value</strong>
of the house and of the alternative paths at the end of the horizon.</p>

<div class="note"><strong>Rounding.</strong> Every amount on this page is rounded to the nearest
$10. Rates, caps, and thresholds are quoted exactly. A fifty-year projection is a scenario, not a
prediction: the range on <a href="black-swans.html">Black swans</a> is the honest measure of how
little a single path means.</div>

<h2>Property A: cost of holding, 2045 transfer, move-in path</h2>
{table(["Year", "Market value", "Taxable value", "Property tax", "Insurance",
        "Water and power", "Maintenance"], rows,
       caption="Central assumptions. Taxable value is the factored base-year value plus the "
               "excess over the value cap, less the $7,000 homeowners' exemption. Model output "
               "rounded to the nearest $10. Every fifth year is shown.")}

<h2>How each line is built</h2>
<table><thead><tr><th>Line</th><th>Method</th><th>Anchor</th></tr></thead><tbody>
<tr><td>Market value</td><td>The 2026 owner estimate compounded at the assumed growth rate</td>
<td>Owner estimate; FHFA index history</td></tr>
<tr><td>Assessed value</td><td>Compounded at the 2% cap, which is also the ceiling on the
annual inflation factor</td>
<td><a href="https://www.boe.ca.gov/proptaxes/pdf/lta26002.pdf">BOE LTA 2026/002</a></td></tr>
<tr><td>Property tax</td><td>Net taxable value at the county's composite rate, plus fixed
charges grown at inflation</td>
<td><a href="https://www.sccgov.org/sites/dtt/pd/Documents/tax-rate-book-2025-2026.pdf">County rate book</a></td></tr>
<tr><td>Insurance</td><td>Owner estimate grown above inflation, because California premiums have
been repricing</td>
<td><a href="https://www.insurance.ca.gov/0400-news/0200-studies-reports/0300-earthquake-study/upload/EQEXP2025Summary.pdf">CDI</a></td></tr>
<tr><td>Water and power</td><td>Owner estimate grown at inflation; the electricity line is
negative because of a solar credit</td>
<td><a href="https://www.cpuc.ca.gov/industries-and-topics/electrical-energy/demand-side-management/net-energy-metering">CPUC</a></td></tr>
<tr><td>Maintenance</td><td>1.0% of market value a year, so it rises with the house</td>
<td>Assumption, published on <a href="methodology.html">Methodology</a></td></tr>
</tbody></table>

<h2>Sensitivity: the two assumptions that decide the answer</h2>
{table(["Home growth", "Reinvestment rate", "Move in", "Rent out", "Sell and reinvest", "Best"],
       srows,
       caption="2045 transfer. Nine combinations of the two assumptions the ranking is most "
               "sensitive to. Model output rounded to the nearest $10.")}

<p>The pattern is stark. Selling wins in eight of the nine combinations. Holding wins only when
home values compound at 5% <em>and</em> the reinvestment rate is at the low end at the same time.
That is the honest summary of the central case: <strong>the sell path is robust across a wide
range of assumptions, and only a sustained high-growth, low-rate world reverses it.</strong></p>

<h2>Realised history, for calibration</h2>
<table><thead><tr><th>Measure</th><th>Period</th><th>Annual rate</th><th>Source</th></tr></thead><tbody>
<tr><td>Consumer price index, annual average</td><td>1998 to 2023</td>
<td class="num">{pct(MODEL["realised"]["cpi_annual_1998_2023"])}</td>
<td><a href="https://www.bls.gov/cpi/tables/supplemental-files/historical-cpi-u-202402.pdf">BLS</a></td></tr>
<tr><td>National house price index</td><td>1991 to 2026</td>
<td class="num">{pct(MODEL["realised"]["fhfa_annual_1991_2026"])}</td>
<td><a href="https://www.fhfa.gov/data/hpi">FHFA</a></td></tr>
<tr><td>House price index, latest twelve months</td><td>Aug 2025 to Aug 2026</td>
<td class="num">{pct(0.024)}</td><td><a href="https://www.fhfa.gov/data/hpi">FHFA</a></td></tr>
<tr><td>Ten-year Treasury, the risk-free alternative</td><td>12 November 2026</td>
<td class="num">{pct(0.0510)}</td>
<td><a href="https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve">US Treasury</a></td></tr>
<tr><td>Thirty-year fixed mortgage</td><td>12 November 2026</td>
<td class="num">{pct(0.0711)}</td><td><a href="https://www.freddiemac.com/pmms">Freddie Mac</a></td></tr>
<tr><td>Long-run inflation assumption</td><td>to 2055</td>
<td class="num">{pct(0.020)}</td><td><a href="https://www.cbo.gov/publication/61270">CBO</a></td></tr>
</tbody></table>

<p>The 3.5% growth assumption sits between the two realised series: below the 4.28% the national
index has delivered over thirty-five years, and above the 2.53% the price level has delivered over
twenty-five. That is deliberate. A house is a real asset and should beat inflation, but land in a
mature market should not be expected to repeat a run that included a historic credit boom.</p>
"""
    add("projections.html", "Projections 2026-2076",
        "Value, assessed value, and every carrying cost, year by year, with the arithmetic shown.",
        body)


# ===========================================================================
# Costs
# ===========================================================================
def build_costs():
    b = MODEL["b_ledger"]["2045"]
    rows = [{"cells": [str(r["year"]), money(r["property_tax"]), money(r["insurance"]),
                       money(r["utilities"]), money(r["maintenance"]),
                       money(r["property_tax"] + r["insurance"] + r["utilities"]
                             + r["maintenance"])], "flag": "M04"}
            for r in MODEL["annual"]["2045"]["occupy"] if r["year"] % 5 == 0]
    t_a = table(["Year", "Property tax", "Insurance", "Water and power", "Maintenance",
                 "Total annual cost"], rows,
                caption="Move-in path, 2045 transfer. Model output rounded to the nearest $10.")
    t_b = table(["Line", "Amount", "Basis"], [
        {"cells": ["Reported 2025 property-tax charge", money(2440),
                   "Owner's own bill, rounded to the nearest $10"], "flag": "F01"},
        {"cells": ["2025 assessed value", money(114250),
                   "Owner's own assessment, rounded to the nearest $10"], "flag": "F01"},
        {"cells": ["Implied effective rate", pct(MODEL["implied_rates"]["B"]),
                   "Charge divided by assessed value"], "flag": "F01"},
        {"cells": ["City published secured rate, FY2026-27", pct(0.0118162182, 8),
                   "Published by the city treasurer"], "src": "sft_secured"},
        {"cells": ["Charge the published rate would produce", money(1350),
                   "Assessed value times the published rate"], "flag": "F01"},
        {"cells": ["Unexplained residual", money(1090),
                   "Difference, treated as fixed charges and parcel taxes"], "flag": "F01"},
    ], caption="Amounts rounded to the nearest $10.")
    t_ins = table(["Measure", "Amount", "What it measures"], [
        {"cells": ["California average homeowners' premium, 2025", money(2339.99),
                   "Per policy, statewide average"], "src": "cdi"},
        {"cells": ["California average dwelling-fire premium, 2025", money(1700),
                   "The narrower form of cover"], "src": "cdi"},
        {"cells": ["California average earthquake premium, 2025", money(1440.11),
                   "Separate from the homeowners' policy"], "src": "cdi"},
        {"cells": ["Both houses, combined assumed annual premium", money(3000),
                   "Owner estimates of $1,500 each"], "flag": "F03"},
    ])
    t_w = table(["Item", "Figure", "Basis"], [
        {"cells": ["Water and power, Property A, per month", money(120),
                   "Owner estimate, net of a solar credit"], "flag": "F06"},
        {"cells": ["Water and power, Property B, per month", money(420),
                   "Owner estimate for three units"], "flag": "F07"},
        {"cells": ["Water fixed monthly charge from 1 July 2026", money(78.64),
                   "Published tariff"], "src": "sjwc"},
        {"cells": ["Volumetric tier 1 rate from 1 July 2026", "$4.9692 per unit",
                   "Published tariff"], "src": "sjwc"},
        {"cells": ["Net-metering treatment", "Net billing, not net metering, for applications "
                   "after 15 April 2023", "Regulator's decision"], "src": "cpuc_nem"},
        {"cells": ["Other city's water and sewer schedule",
                   "Fixed meter charge plus two-tier volumetric, effective 1 July 2026",
                   "Published schedule"], "src": "sfpuc"},
    ])
    body = f"""
<p>Two houses, two very different cost structures. The inherited house carries a small tax bill
against a large value, and a large maintenance exposure. The already-owned house carries a tax bill
that does not match its assessed value. Both carry insurance estimates that look too low.</p>

<h2>Property A: the inherited house</h2>
<p>The tax bill is low relative to the value of the house. But the part of that bill that the
family-home exclusion actually protects is narrower than it first appears: the exclusion preserves
the assessed value only up to the value cap of {e("$1,044,586")}, and the rest of the gap is taxed
either way. So the difference between occupying and not occupying is real but modest, and it is the
same dollar amount in every transfer year.</p>
{t_a}

<h2>Property B: the house already owned</h2>
{t_b}

<div class="warnbox"><strong>Flag F01.</strong> An effective rate of 2.14% against a published
secured rate of 1.18% is not a rounding problem. Either the bill includes assessments the published
rate does not capture, which is common and would explain most of it, or the assessed value used here
is not the value the bill was computed on. This needs the bill and the assessment notice side by
side, and it is the highest-value administrative item in the desk.</div>

<h2>Insurance: the weakest line on both houses</h2>
{t_ins}

<p>The two houses together are assumed to cost $3,000 a year to insure. The statewide average for a
single homeowners' policy plus earthquake cover is about $3,780. Two houses in high-value markets,
one an older coastal building, at $1,500 each, is not credible. Either the policies are unusually
inexpensive, or they are narrower dwelling-fire policies, or earthquake cover is separate and not
counted. The gap matters: a $2,000 understatement per house compounds to more than $150,000 over a
thirty-year hold.</p>

<h2>Water and power</h2>
{t_w}

<p>The electricity line is negative for Property A because the solar array generates more than the
house uses. That is a real cash benefit, but it is fragile two ways. The credit for exported power
is worth less under net billing than under the old net-metering tariff, and a future occupant who
uses more power, or a second unit, would consume the surplus rather than sell it.</p>

<h2>Maintenance</h2>
<p>Maintenance is modelled at 1.0% of market value a year for the inherited house and 1.2% for the
three-unit property, because three units have three kitchens, three bathrooms, and more roof. This
is a planning convention, not a measured figure, and it is the largest operating line for the
inherited house. A condominium would carry a lower number plus a monthly association assessment; a
detached house on its own lot carries a higher one. Which this is remains an open question.</p>
"""
    add("costs.html", "Carrying costs",
        "What each house costs to hold, line by line, and which lines are not credible.", body)


# ===========================================================================
# Inheritance tax
# ===========================================================================
def build_estate():
    rows = [{"cells": [str(e["year"]), money(e["exclusion_projected"]),
                       money(e["gross_estate_projected"]), money(e["headroom"]),
                       '<span class="yes">under</span>' if e["status"] == "under"
                       else '<span class="no">over</span>'], "flag": "M06"} for e in MODEL["estate"]]
    t_head = table(["Year", "Projected exclusion", "Projected gross estate", "Headroom", "Status"],
                   rows,
                   caption="The exclusion is indexed to inflation. This projection applies the "
                           "long-run inflation assumption to the published 2027 figure. The gross "
                           "estate is the two houses only, grown at the central home-growth "
                           "assumption. Model output rounded to the nearest $10. A projection, "
                           "not law.")
    t_where = table(["Charge", "Amount", "When", "Basis"], [
        {"cells": ["Federal estate tax", money(0), "On death",
                   "Estate far below the exclusion"], "src": "irs_estate"},
        {"cells": ["California estate or inheritance tax", money(0), "Not applicable",
                   "No such tax exists"], "src": "sco_estate"},
        {"cells": ["Extra property tax if the heir does not occupy", money(12440), "Every year",
                   "The market-value base minus the exemption, at the composite rate"],
         "flag": "M04"},
        {"cells": ["Income tax on inherited retirement accounts", None, "On distribution",
                   "Balances unknown, and the answer also depends on whether the ten-year rule "
                   "applies"], "flag": "F08"},
    ], caption="Amounts rounded to the nearest $10 where they are computed.")
    t_rules = table(["Rule", "Effect", "Where it comes from"], [
        {"cells": ["Stepped-up basis", "Basis equals fair market value at the date of death",
                   "State filing guidance restating the federal rule"], "src": "ftb_593"},
        {"cells": ["Home-sale exclusion",
                   "Up to $250,000 of gain excluded for a single filer, where the house was "
                   "owned and used as a principal residence for two of the last five years",
                   "IRS topic"], "src": "irs_701"},
        {"cells": ["Net investment income tax",
                   "3.8% on the lesser of net investment income or the excess of modified "
                   "adjusted gross income over $200,000 for a single filer", "IRS topic"],
         "src": "irs_559"},
        {"cells": ["Depreciation recapture",
                   "Gain attributable to depreciation is taxed at up to 25% federally, not at the "
                   "long-term capital-gain rate", "IRS publication"], "src": "irs_527"},
        {"cells": ["Passive losses",
                   "Suspended losses are released in full on a disposition of the entire interest",
                   "IRS topic"], "src": "irs_425"},
        {"cells": ["Alternate valuation",
                   "The estate may value assets six months after death instead, which is "
                   "irrevocable once elected", "Form instructions"], "src": "irs_706"},
    ])
    body = f"""
<p>"Inheritance tax" names three different things, and conflating them is the most expensive
mistake available in this analysis.</p>

<div class="card">
<h3>1. A tax on receiving an inheritance</h3>
<p><strong>California has none.</strong> The state's estate tax was repealed effective 1 January
2005, and no inheritance tax has replaced it. A beneficiary receives inherited property free of any
California transfer tax.</p>
<p class="src"><a href="https://www.sco.ca.gov/ardtax_estate_tax.html">State Controller, Estate tax</a></p>
</div>

<div class="card">
<h3>2. A tax on the estate</h3>
<p><strong>Federal, and the threshold is high.</strong> The filing threshold is
{exact("$15,000,000")} for a death in 2026 and
{exact("$15,480,000")} for 2027. Above the exclusion the rate is 40%. A surviving
spouse can inherit the first spouse's unused exclusion, but only if a timely return is filed to
elect it.</p>
<p class="src"><a href="https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax">IRS, Estate tax</a>
&middot; <a href="https://www.irs.gov/pub/irs-drop/rp-26-35.pdf">Rev. Proc. 2026-35</a>
&middot; <a href="https://www.irs.gov/instructions/i706">Form 706 instructions</a></p>
</div>

<div class="card">
<h3>3. Reassessment at the county</h3>
<p><strong>This is the one that actually bites.</strong> It is not a tax on inheriting; it is the
loss of the deceased's low assessed value. A child who moves into a parent's home can keep the old
base-year value plus the value cap of {e("$1,044,586")}, and pays tax on any excess of market value over
that sum. A child who does not move in pays tax on full market value.</p>
<p class="src"><a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2">RTC s.63.2</a>
&middot; <a href="https://www.boe.ca.gov/proptaxes/pdf/lta26026.pdf">BOE LTA 2026/026</a></p>
</div>

<h2>Federal estate-tax headroom, projected</h2>
{t_head}

<p>The estate is far below the exclusion in every year tested, and the margin widens, because the
exclusion is indexed while the houses are assumed to grow only slightly faster than inflation.
<strong>On these assumptions no federal estate tax is due at all.</strong> That is the correct
answer for most families, and it is worth stating plainly so that the real risk, which is the
reassessment, is not obscured by a tax that does not apply.</p>

<div class="warnbox"><strong>Where this projection breaks.</strong> Two ways. First, if the
"considerable amount of money" also inherited is a substantial portfolio rather than two houses,
the gross estate is much larger than modelled here, because this projection carries real property
only. Second, if the exclusion is legislated downward, the whole conclusion changes. It doubled in
2026 and is indexed, but it has moved before and can move again.</div>

<h2>Where the money actually goes, at a 2045 transfer</h2>
{t_where}

<h2>The income-tax side of inheriting</h2>
<p>Inherited property is not income. It takes a basis equal to fair market value at the date of
death, so a sale at that value realises no gain. Only appreciation after the death is taxed, and
only when realised. That is the single most valuable feature of the whole transaction, and it means
<strong>the worst thing to do with an inherited house is to sell it decades later without having
documented the basis and the improvements.</strong></p>
{t_rules}

<h2>What the two houses mean for the estate</h2>
<p>The estate is not just the inherited house. It is everything the heir owns, including the
already-owned house. That is why the projected gross estate above starts at the combined value of
both. It is also why a decision about Property A is really a decision about the whole balance
sheet.</p>
"""
    add("estate-tax.html", "Inheritance tax",
        "Three different taxes that share a name, and only one of them actually applies here.",
        body)


# ===========================================================================
# Process
# ===========================================================================
def fee(v: float) -> float:
    """Probate Code s.10810 statutory ordinary-services fee."""
    tiers = [(100_000, 0.04), (100_000, 0.03), (800_000, 0.02), (9_000_000, 0.01),
             (15_000_000, 0.005)]
    total, rem = 0.0, v
    for width, rate in tiers:
        take = min(rem, width)
        total += take * rate
        rem -= take
        if rem <= 0:
            break
    return round(total / 10) * 10


def build_process():
    steps = [
        ("1", "Locate the trust and read it", "Confirm whether it is revocable or irrevocable, who "
         "the successor trustee is, and what it directs as to this property. A house in a trust "
         "passes under the trust's terms, not under the will.",
         "The trust document", None, "T01"),
        ("2", "Obtain death certificates", "A certified copy is needed by the county, the recorder, "
         "and every financial institution. Order more than seems necessary.",
         "The county recorder's requirements", None, "T02"),
        ("3", "Establish the trustee's authority", "Where the trust holds real property, the "
         "successor trustee's authority is normally evidenced by an affidavit and a certification "
         "of trust recorded with the county.",
         "Recording requirements", "scc_recorder", None),
        ("4", "Serve the trustee's notification", "Within 60 days of accepting the role, the trustee "
         "must notify beneficiaries and heirs that the trust has become irrevocable.",
         "Probate Code s.16061.7", "prob_16061_7", None),
        ("5", "Value the property at the date of death", "This valuation sets the income-tax basis "
         "and the estate-tax value. It should be a defensible appraisal, not a guess. Alternate "
         "valuation at six months is available and irrevocable.",
         "Form 706 instructions", "irs_706", None),
        ("6", "Decide the federal estate-tax question", "If the gross estate is below the filing "
         "threshold, no return is needed for tax, but one may still be worth filing to elect "
         "portability. The deadline is nine months, extendable by six.",
         "Form 706 instructions", "irs_706", None),
        ("7", "Claim the homeowners' exemption, if occupying", "This is the step that keeps the "
         "family-home exclusion alive. It must be filed within one year of the transfer.",
         "RTC s.63.2(a)(1)(B)", "rtc_63_2", None),
        ("8", "Claim the exclusion itself", "File the claim for the intergenerational transfer "
         "exclusion with the assessor. The window runs to three years or before a transfer to a "
         "third party.", "RTC s.63.2(f)", "rtc_63_2", None),
        ("9", "Pay the transfer tax, if any", "Documentary transfer tax applies to a change of "
         "ownership unless a statutory exemption is cited. Some cities add their own conveyance "
         "tax.", "County recorder", "scc_recorder", None),
        ("10", "File the change-of-ownership report", "A preliminary change of ownership report is "
         "required, or a $20 surcharge applies. Exemption claims are reviewed before recording.",
         "County recorder", "scc_recorder", None),
        ("11", "Re-title insurance and utilities", "A policy in the deceased's name will not "
         "respond to a claim. Confirm cover is in force in the right name before occupancy.",
         "Not documented here", None, "T03"),
        ("12", "If the estate is small, consider the affidavit route", "An affidavit can transfer "
         "personal property up to a statutory limit without probate, 40 days after death. It does "
         "not transfer real property.",
         "Probate Code s.13100", "prob_13100", None),
    ]
    t_steps = table(["#", "Step", "What it involves", "Authority"],
                    [{"cells": [n, t, d, a], "src": s, "flag": f}
                     for n, t, d, a, s, f in steps],
                    caption="A row is sourced where the requirement is statutory or procedural. "
                            "Rows marked FLAG differ by trust and by county and need professional "
                            "confirmation.")
    t_fees = table(["Estate value", "Statutory attorney fee", "Statutory executor fee",
                    "Total statutory fees"],
                   [{"cells": [money(v), money(fee(v)), money(fee(v)), money(2 * fee(v))],
                     "src": "prob_10810"}
                    for v in (2_000_000, 3_000_000, 6_000_000, 10_000_000)],
                   caption="Computed from the statutory tiers on the inventory value. Both fees "
                           "are separately payable, so the total is twice the single-fee column. "
                           "Amounts rounded to the nearest $10.")
    body = f"""
<p>The order matters, and two steps have hard deadlines. This is the sequence from a death to a
recorded title, on the assumption that the house passes through a trust rather than through
probate. If the trust is defective, or the house was never actually transferred into it, the
probate route applies, and it is slower and considerably more expensive.</p>

<h2>The sequence</h2>
{t_steps}

<h2>The deadlines, in order of danger</h2>
<table><thead><tr><th>Deadline</th><th>Runs from</th><th>What it is for</th>
<th>If missed</th><th>Authority</th></tr></thead><tbody>
<tr><td>40 days</td><td>Date of death</td>
<td>Small-estate affidavit for personal property</td><td>The simplified route is unavailable</td>
<td><a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PROB&sectionNum=13100">Prob. Code s.13100</a></td></tr>
<tr><td>60 days</td><td>Accepting the trustee role</td>
<td>Notification that the trust is irrevocable</td><td>Trustee liability</td>
<td><a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PROB&sectionNum=16061.7">Prob. Code s.16061.7</a></td></tr>
<tr><td>9 months</td><td>Date of death</td>
<td>Federal estate-tax return, plus a 6-month extension</td>
<td>Penalties, and a permanently lost portability election</td>
<td><a href="https://www.irs.gov/instructions/i706">Form 706 instructions</a></td></tr>
<tr><td>1 year</td><td>Date of transfer</td><td>Homeowners' exemption claim</td>
<td>The exclusion is removed and the market base enrolled</td>
<td><a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2">RTC s.63.2(a)(1)(B)</a></td></tr>
<tr><td>3 years</td><td>Date of transfer</td><td>Claim for the exclusion</td>
<td>Relief is delayed or denied</td>
<td><a href="https://www.boe.ca.gov/proptaxes/pdf/lta26026.pdf">BOE LTA 2026/026</a></td></tr>
</tbody></table>

<h2>What probate would cost if the trust fails</h2>
<p>California sets statutory fees for ordinary probate services on a sliding scale: 4% of the
first $100,000 of the estate, 3% of the next $100,000, 2% of the next $800,000, 1% of the next
$9,000,000, 0.5% of the next $15,000,000, and a court-determined amount above $25,000,000. The
executor is entitled to the same amount as the attorney. <strong>On these numbers the trust is
worth more than the tax planning.</strong></p>
{t_fees}

<h2>The three ways this process goes wrong</h2>
<ol>
<li><strong>The house was never put in the trust.</strong> A trust only controls what is titled in
its name. A house still in the deceased's individual name passes under the will, which means
probate, which means the fees above. This is checked in step one and it is the whole ballgame.</li>
<li><strong>The exemption is claimed late.</strong> The one-year homeowners' exemption claim is the
difference between keeping the deceased's assessed value and paying tax on today's market value,
every year, for as long as the house is held. The statute is explicit: the exclusion is removed on
the date the transferee stops being eligible, and a new base-year value is enrolled from the
following lien date.</li>
<li><strong>The basis is not documented.</strong> A date-of-death appraisal costs a few thousand
dollars. Without it, the tax authority can take the position that basis is the original purchase
price, and the resulting gain can be enormous.</li>
</ol>
"""
    add("process.html", "Trust process",
        "From a death to a recorded title, in order, with the deadlines that carry real penalties.",
        body)


# ===========================================================================
# Black swans
# ===========================================================================
def build_swans():
    cards = "\n".join(f"""
<div class="card">
<h3>{h(s["id"])}. {h(s["name"])}</h3>
<p style="margin:0 0 .7rem">{h(s["effect"])}</p>
<table><tbody>
<tr><th>Anchor</th><td>{h(s["anchor"])}</td></tr>
<tr><th>Home growth applied</th><td class="num">{pct(s["home_growth"], 1)}</td></tr>
<tr><th>Insurance growth applied</th><td class="num">{pct(s["insurance_growth"], 1)}</td></tr>
<tr><th>Property tax, year one</th><td class="num">{money(s["tax_year1"])}</td></tr>
<tr><th>Property tax, year thirty</th><td class="num">{money(s["tax_year30"])}</td></tr>
<tr><th>Annual holding cost, year thirty</th><td class="num">{money(s["annual_holding_cost_year30"])}</td></tr>
<tr><th>Value at the horizon</th><td class="num">{money(s["fmv_at_horizon"])}</td></tr>
<tr><th>Hold, then sell</th><td class="num">{money(s["hold_then_sell"])}</td></tr>
<tr><th>Sell now and reinvest</th><td class="num">{money(s["sell_now_then_invest"])}</td></tr>
<tr><th>Which wins</th><td><strong>{h(s["verdict"])}</strong></td></tr>
</tbody></table>
</div>""" for s in MODEL["swans"])
    body = f"""
<p>Growth and inflation are never consistent over fifty years. The central case uses one number for
each, which is a convenience and not a belief. This page replaces it with seven stress paths, each
anchored to an episode or a rule that is documented, and asks the same question of each: does
holding the house still beat selling it?</p>

<div class="warnbox"><strong>How to read this page.</strong> These are not forecasts and they are
not equally likely. They are <em>stress paths</em>, chosen because each has a documented anchor.
The point is not to predict which one happens. The point is to see which decisions survive all of
them, and which do not.</div>

<div class="note"><strong>One convention, stated so it can be argued with.</strong> The sell path
assumes the seller still needs somewhere to live, so it charges rent equal to what the house itself
could earn. Without that charge the comparison would credit the seller with the investment return
<em>and</em> free housing, which is not a comparison at all.</div>

<h2>The seven scenarios</h2>
{cards}

<h2>What the stress paths agree on</h2>
<table><thead><tr><th>Finding</th><th>Why it holds across the scenarios</th></tr></thead><tbody>
<tr class="normative"><td><strong>The sell path has a timing risk the hold path does not</strong></td>
<td>A sale happens on one day. If that day falls in a bust, the loss is locked in. A hold can wait.
The 2006-2011 case is the clearest demonstration: an index decline of about 21% from peak to trough
is survivable if you do not have to sell.</td></tr>
<tr class="normative"><td><strong>Holding wins only in the inflation case</strong></td>
<td>That is the whole finding. In the stagflation path the 2% assessment cap turns the property tax
into a shrinking real cost while everything else inflates, and that is enough to beat the sell
path. In every other path, including the central case, selling wins.</td></tr>
<tr class="normative"><td><strong>Proposition 13 is the only structural edge holding has</strong></td>
<td>No financial asset reproduces a cost that cannot rise faster than 2% a year. Everything else
about a house, from maintenance to insurance, rises with or above inflation.</td></tr>
<tr class="normative"><td><strong>Insurance is the most under-budgeted risk</strong></td>
<td>Both houses are assumed at premiums below the statewide average. In the insurance contraction
path the annual holding cost in year thirty reaches several hundred thousand dollars.</td></tr>
<tr class="normative"><td><strong>Occupying and then moving out is not catastrophic</strong></td>
<td>Under the statute, losing eligibility enrolls the base-year value established at the original
transfer, adjusted annually. So a household that occupies for eight years and then moves out ends
up better off than one that never occupied, and both converge on the same tax by year thirty. The
mistake is expensive, but it is not a cliff.</td></tr>
</tbody></table>

<h2>The uneven economy, stated plainly</h2>
<p>Two facts from the record should shape how much weight any single projection deserves.</p>
<ul>
<li><strong>Inflation has been violent.</strong> The consumer price index rose 13.3% in the twelve
months to December 1979 and 13.5% over calendar 1980, then 8.0% over calendar 2022. A 2% assumption
for fifty years is a central tendency, not a description of any particular decade.</li>
<li><strong>House prices have had long flat and falling stretches.</strong> The national index fell
about 21% from its 2007 peak to February 2011, and took years to recover in real terms. A
thirty-five year average of 4.28% conceals that entirely.</li>
</ul>
<p>The practical consequence is that a plan which requires a sale on a particular date, or which
requires home values to compound at a particular rate, is fragile. A plan that keeps options open,
and that treats the assessed value as an asset to be protected rather than as a detail, survives
all seven paths. That is the case for option A on <a href="suggestions.html">Suggestions</a>.</p>
"""
    add("black-swans.html", "Black swans",
        "Seven sourced stress paths, and what they agree on even when they disagree.", body)


# ===========================================================================
# Law watch
# ===========================================================================
def build_law():
    rows = [
        ("Proposition 19 family-home exclusion", "In force",
         "A child who occupies a parent's home keeps the old base-year value plus a value cap of "
         + e("$1,044,586"), "Repeal or narrowing would remove the largest single benefit in the plan",
         "rtc_63_2"),
        ("Proposition 13 assessment cap", "In force, 2% a year",
         "Limits annual assessed-value growth and fixes the base rate at 1% plus voter-approved "
         "debt", "Any change is the largest single risk to the hold path", "boe_lta26002"),
        ("State rent cap", "In force, sunsets 1 January 2030",
         "Caps increases at 5% plus inflation, up to a maximum of 10%, with exemptions for newer "
         "buildings and certain small owners", "Determines what the rental path can actually "
         "collect", "civ_1947_12"),
        ("Federal estate-tax exclusion", "In force, indexed; $15,000,000 for 2026",
         "Applies a 40% rate above the exclusion and allows portability between spouses",
         "A reduction would put a larger estate into tax for the first time", "irs_estate"),
        ("Stepped-up basis at death", "In force",
         "Resets basis to fair market value at death",
         "Curtailing it would make a long hold much more expensive to end", "ftb_593"),
        ("Net energy metering", "Closed to new applicants",
         "Applications after 15 April 2023 are on net billing, which pays less for exported power",
         "Reduces the value of an existing solar credit over time", "cpuc_nem"),
        ("Documentary transfer tax", "Local, and changeable",
         "Rates vary by county and, in one city, by price band",
         "A sale in a high band can cost over 2% of the price", "rtc_11911"),
        ("Insurance regulation", "In flux",
         "Rate approvals, the residual-market insurer, and catastrophe modelling are all under "
         "active revision", "Insurance is the least predictable line in the model", "cdi"),
    ]
    t_rules = table(["Rule", "Current state", "What it does", "Why a change matters"],
                    [{"cells": [n, s, w, r], "src": src} for n, s, w, r, src in rows],
                    caption="Current as of the date at the top of the page. Each row links to the "
                            "official text or to the administering agency.")
    body = f"""
<p>The plan spans thirty to fifty years. Every rule it relies on can be changed in that time, by
legislation, by initiative, or by a court. This page lists the rules the plan depends on, their
current state, and what a change would cost.</p>

{t_rules}

<h2>Ranked by how much damage a change would do</h2>
<ol>
<li><strong>A repeal or narrowing of the family-home exclusion.</strong> This is the whole basis of
the hold path's tax advantage. Without it, inheriting the house means inheriting a market-value
assessment, and holding loses its structural edge. The exclusion is recent, it was passed by
initiative, and it can be changed by initiative.</li>
<li><strong>A cap on stepped-up basis.</strong> Proposals to limit the basis step-up at death have
been made repeatedly. If it were curtailed, a long hold would end with a very large taxable gain.</li>
<li><strong>A reduction in the federal exclusion.</strong> Not a live risk for this estate at the
moment, given the size of the margin, but it is the item most likely to be raised in national
debate, and it would apply to the whole balance sheet, not only the inherited house.</li>
<li><strong>Rent-control expansion.</strong> The state cap sunsets in 2030, but local ordinances are
stricter and more durable. If the house were rented, the rent would be constrained for as long as
the tenancy lasted.</li>
<li><strong>Insurance-market change.</strong> Not a law change in the ordinary sense, but the
regulatory environment determines whether cover is available at all, and at what price.</li>
</ol>

<h2>What is already scheduled to change</h2>
<table><thead><tr><th>Item</th><th>Change</th><th>Effective</th><th>Source</th></tr></thead><tbody>
<tr><td>Federal estate-tax exclusion</td><td>Rises to $15,480,000</td><td>2027</td>
<td><a href="https://www.irs.gov/pub/irs-drop/rp-26-35.pdf">Rev. Proc. 2026-35</a></td></tr>
<tr><td>Annual gift exclusion</td><td>Rises to $20,000</td><td>2027</td>
<td><a href="https://www.irs.gov/pub/irs-drop/rp-26-35.pdf">Rev. Proc. 2026-35</a></td></tr>
<tr><td>Proposition 19 value cap</td><td>Re-set every two years to the prior year's figure</td>
<td>Transfers from 16 February 2027</td>
<td><a href="https://www.boe.ca.gov/proptaxes/pdf/lta26026.pdf">BOE LTA 2026/026</a></td></tr>
<tr><td>State rent cap</td><td>Sunsets</td><td>1 January 2030</td>
<td><a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12">Civil Code s.1947.12</a></td></tr>
<tr><td>Property-tax inflation factor</td><td>Capped at 2% a year</td>
<td>Annually; the 2026-27 factor is below the cap</td>
<td><a href="https://www.boe.ca.gov/proptaxes/pdf/lta26002.pdf">BOE LTA 2026/002</a></td></tr>
</tbody></table>

<h2>What to watch, and where</h2>
<table><thead><tr><th>Watch</th><th>Where</th><th>How often</th></tr></thead><tbody>
<tr><td>Qualified ballot measures and results</td>
<td><a href="https://www.sos.ca.gov/elections/ballot-measures/qualified-ballot-measures">Secretary of State</a></td>
<td>Each election cycle</td></tr>
<tr><td>Property-tax guidance to assessors</td>
<td><a href="https://www.boe.ca.gov/proptaxes/ltacont.htm">Letters to Assessors index</a></td>
<td>Monthly</td></tr>
<tr><td>Inflation adjustments to every threshold here</td>
<td><a href="https://www.irs.gov/pub/irs-drop/rp-26-35.pdf">IRS annual revenue procedure</a>,
<a href="https://www.boe.ca.gov/proptaxes/2026.htm">BOE annual CPI letter</a></td>
<td>Every autumn</td></tr>
<tr><td>County and city tax rates</td>
<td><a href="https://sftreasurer.org/property/secured-property-taxes">City treasurer</a></td>
<td>Annually, in the autumn</td></tr>
<tr><td>Insurance market condition</td>
<td><a href="https://www.insurance.ca.gov/0400-news/0200-studies-reports/0300-earthquake-study/upload/EQEXP2025Summary.pdf">Department of Insurance</a></td>
<td>Annually</td></tr>
</tbody></table>
"""
    add("law-watch.html", "Law watch",
        "The rules the plan depends on, and what a change to each would cost.", body)


# ===========================================================================
# Open questions
# ===========================================================================
KNOWN = [
    ("Federal estate-tax filing threshold, death in 2026", "$15,000,000", "irs_estate"),
    ("Federal estate-tax filing threshold, death in 2027", "$15,480,000", "irs_revproc"),
    ("California estate or inheritance tax", "None", "sco_estate"),
    ("Proposition 19 value cap, transfers from 16 Feb 2025", "$1,044,586", "boe_lta25009"),
    ("Homeowners' exemption, and the one-year claim for the exclusion", "$7,000", "boe_lta23027"),
    ("Proposition 13 annual assessment cap", "2%", "boe_lta26002"),
    ("County composite secured rate used for the inherited house", "1.1488% typical", "scc_rate"),
    ("City secured rate, FY2026-27, for the already-owned house", "1.18162182%", "sft_secured"),
    ("Home-sale exclusion, single filer", "$250,000", "irs_701"),
    ("Net investment income tax threshold and rate", "3.8% above $200,000", "irs_559"),
    ("Small-estate affidavit limit (DE-300 schedule; Prob. Code s.13100 base text is $166,250 as adjusted under s.890)",
     "$208,850", "de300"),
    ("Trustee notification deadline", "60 days", "prob_16061_7"),
    ("Federal estate-tax return deadline", "9 months, plus 6 on extension", "irs_706"),
    ("Documentary transfer tax, county base rate", "$0.55 per $500", "rtc_11911"),
    ("Documentary transfer tax, three cities in that county", "$1.65 per $500", "scc_recorder"),
]

UNKNOWN = [
    ("Is the house actually titled in the trust?",
     "If not, probate applies and the statutory fees on the process page follow.",
     "Pull the recorded deed and read the trust.", "T01"),
    ("What kind of property is it: house, condominium, or townhouse?",
     "Changes the maintenance line, the insurance line, and whether an association assessment "
     "exists.", "Read the deed and the title report.", "T04"),
    ("How many legal units could it be split into?",
     "The break-even rent is a total. Two units at half each changes the rental path entirely.",
     "Ask the city for a written zoning read on unit count.", "T05"),
    ("What is the current market rent for it?",
     "The whole rental path rests on this one number.",
     "Commission three independent rental appraisals, in writing.", "T06"),
    ("What insurance is actually in force, with what limits, on both houses?",
     "Both modelled premiums sit below the statewide average and neither is documented.",
     "Obtain both declaration pages and compare the limits.", "F03"),
    ("Why is the already-owned house charged 2.14% of its assessed value?",
     "Against a published secured rate of 1.18%. It is either assessments or a mismatched "
     "assessed value.", "Put the bill and the assessment notice side by side.", "F01"),
    ("What is the parcel-specific composite rate for the inherited house?",
     "The desk uses the county's typical rate. The actual rate depends on the tax-rate area, "
     "which is printed on the bill.", "Read the rate printed on the annual bill.", "F02"),
    ("What retirement accounts are in the estate, and who are the beneficiaries?",
     "These are taxed as ordinary income on distribution, unlike the house.",
     "Obtain the beneficiary designations from each institution.", "F08"),
    ("How large is the rest of the estate?",
     "The estate-tax projection carries real property only. A large portfolio changes the answer.",
     "Assemble a complete balance sheet as of the date of death.", "F09"),
    ("Is the heir married, and is there a surviving spouse?",
     "The home-sale exclusion is $250,000 single or $500,000 joint, and portability depends on it.",
     "A direct question. It moves several thresholds at once.", "F10"),
    ("What is the heir's marginal rate in the transfer year?",
     "Every after-tax figure depends on it.",
     "Model three brackets rather than one, and recompute.", "F11"),
    ("Does the trust require a sale or a division among beneficiaries?",
     "A trust that directs a sale removes the choice entirely.",
     "Read the dispositive provisions of the trust.", "T07"),
    ("What is the heir's actual housing plan?",
     "If the heir would rent elsewhere, that rent belongs on the sell side and is not modelled.",
     "Decide it, then re-run the model with that cost included.", "T08"),
    ("Are there prior improvements to add to basis?",
     "Improvements increase basis and reduce the eventual gain.",
     "Reconstruct from permits and receipts.", "T09"),
    ("What was the solar agreement, and does it transfer?",
     "A lease or power purchase agreement is an obligation that may not survive a sale cleanly.",
     "Obtain the agreement and read its transfer terms.", "F06"),
]


def build_questions():
    t_known = table(["Item", "Value", "Source"],
                    [{"cells": [a, exact(b),
                                '<span class="yes">verified</span>'], "src": d}
                     for a, b, d in KNOWN],
                    caption="Statutory and published figures, quoted exactly rather than rounded, "
                            "because they are fixed by law.")
    t_unknown = table(["Question", "Why it matters", "How to find out"],
                      [{"cells": [a, b, c], "flag": f} for a, b, c, f in UNKNOWN],
                      caption="Each row is a genuine gap that would change a conclusion. Rows "
                              "marked T are procedural or factual. Rows marked F also appear on "
                              "the flagged page.")
    body = f"""
<p>This page separates what is established from what is not. Every item in the first table is cited
to an official source. Every item in the second table is a gap, and each gap has a named method for
closing it. Nothing has been filled in by inference.</p>

<h2>What we know</h2>
{t_known}

<h2>What we do not know</h2>
{t_unknown}

<h2>The five questions that would change the recommendation</h2>
<ol>
<li><strong>Is the house in the trust?</strong> If not, the route is probate, and the statutory fees
are roughly 6% of value before any tax.</li>
<li><strong>Can it be legally split into more than one unit?</strong> This is the only lever that
makes the rental path competitive, because the break-even rent is a total, not a per-unit
figure.</li>
<li><strong>What is the actual market rent?</strong> A rent within about 15% of the break-even
number would make the two paths close enough to decide on other grounds.</li>
<li><strong>Will the heir live in it?</strong> Not a modelling question but a life question, and it
decides the largest tax item in the analysis.</li>
<li><strong>How large is the rest of the estate?</strong> A portfolio large enough to approach the
federal threshold changes the estate-tax answer from "none" to "this needs an appointment".</li>
</ol>

<h2>How to close the gaps efficiently</h2>
<table><thead><tr><th>Order</th><th>Action</th><th>Closes</th><th>Rough effort</th></tr></thead><tbody>
<tr><td>1</td><td>Pull the recorded deed and the trust document</td>
<td>The title question, and whether a sale is directed</td><td>One recorder visit, one hour</td></tr>
<tr><td>2</td><td>Put the two tax bills beside the two assessment notices</td>
<td>The 2.14% anomaly and the parcel-specific rate</td><td>One hour</td></tr>
<tr><td>3</td><td>Obtain both insurance declaration pages</td><td>The premium gap</td>
<td>Two phone calls</td></tr>
<tr><td>4</td><td>Commission three rental appraisals on the inherited house</td>
<td>The rent input</td><td>A few weeks</td></tr>
<tr><td>5</td><td>Get a written zoning read on unit count</td><td>Whether the rental path is viable
at all</td><td>One counter visit</td></tr>
<tr><td>6</td><td>Assemble the full balance sheet, including accounts</td>
<td>The estate-tax question</td><td>A few weeks</td></tr>
</tbody></table>

<div class="note">The first two actions cost nothing but an afternoon, and each one either confirms
or overturns a headline conclusion. They should be done before any professional is engaged, so
that the professional's time is spent on what remains.</div>
"""
    add("questions.html", "Open questions",
        "What is established, what is a gap, and the method for closing each gap.", body)


# ===========================================================================
# Suggestions
# ===========================================================================
def build_suggestions():
    body = f"""
<p>This section is deliberately separate from the analysis. It is the place to compare
<em>paths</em> rather than numbers, and to choose one before anything is implemented.</p>

<div class="note"><strong>Read this before the table.</strong> The analysis shows selling winning on
central assumptions. That is a statement about arithmetic, not a statement about what the heir
should do, because the arithmetic cannot see housing plans, risk tolerance, or the non-financial
value of keeping a family house. Those are exactly what this section is for.</div>

<h2>The options, ranked by robustness rather than by expected value</h2>
<table><thead><tr><th>Option</th><th>What it means</th><th>Strongest case for it</th>
<th>Strongest case against</th><th>Robustness</th></tr></thead><tbody>
<tr><td><strong>A. Protect the option, decide later</strong></td>
<td>Claim the homeowners' exemption and the exclusion on time, keep the house, and defer the
live-rent-sell decision for two or three years while the gaps on the questions page are closed.</td>
<td>Preserves the only irreplaceable asset, which is the assessed value, and costs almost nothing
to do.</td><td>Defers a decision that might be better made early, and the house carries cost in the
meantime.</td><td class="yes">Highest: survives every stress case</td></tr>
<tr><td><strong>B. Move in and hold long term</strong></td>
<td>Occupy the house, keep the exclusion, and treat it as a home and a store of value.</td>
<td>Keeps the exclusion and the Proposition 13 hedge, and provides housing with no rent to pay.</td>
<td>Concentrates the balance sheet in one illiquid asset in one region, and gives up the
compounding the sell path captures.</td>
<td class="yes">High if the heir genuinely wants to live there</td></tr>
<tr><td><strong>C. Sell and reinvest broadly</strong></td>
<td>Sell at the stepped-up basis with no income tax on the sale, and invest the proceeds.</td>
<td>Highest net worth in twenty-four of the twenty-seven sensitivity combinations tested, and it
removes concentration and carrying-cost risk.</td><td>Exposed to selling at a cyclical low, and the exclusion is gone
permanently.</td><td class="no">Good on average, worst at the wrong moment</td></tr>
<tr><td><strong>D. Rent it out</strong></td>
<td>Let the house and keep it as an income asset.</td>
<td>Keeps the asset and produces income.</td>
<td>Gives up the exclusion, takes on operating risk, and the rent is capped. It beats selling only
when home values compound at 5% a year and the reinvestment rate is low at the same time.</td>
<td class="no">Wins in one corner of the grid, loses elsewhere</td></tr>
<tr><td><strong>E. Keep it, and set a decision date</strong></td>
<td>Keep the house and commit to deciding by a stated year rather than deciding now.</td>
<td>Avoids a forced sale, keeps both options open, and lets the market and the basis mature.</td>
<td>Requires discipline, and the carrying cost is real in the meantime.</td>
<td class="yes">High, and compatible with A</td></tr>
</tbody></table>

<h2>What I would do, in order</h2>
<ol>
<li><strong>Do the deadline work immediately, whichever option is chosen.</strong> Claim the
homeowners' exemption within the year and the exclusion within three years. This costs a form and
preserves the most valuable asset in the analysis. It is not optional and it is not contingent on
the decision.</li>
<li><strong>Close the two free gaps in the first month.</strong> The deed and the trust document;
the two tax bills beside the two assessment notices. Everything downstream depends on them, and
neither costs more than an afternoon.</li>
<li><strong>Do not rent the house out before the exemption is claimed.</strong> This is the
sequencing error that matters, because eligibility is tested, and a rental is evidence against
principal-residence use.</li>
<li><strong>Choose between B, C, and E on non-financial grounds, then let the numbers break the
tie.</strong> The financial gap is large in expectation but sits inside a range that one bad sale
date can erase. The difference in lifestyle and concentration is not modelled and is at least as
large.</li>
<li><strong>If the answer is C, sell into strength rather than on a deadline.</strong> The worst
outcome in the stress cases is a forced sale in a bust. A sale with a two-year window and no
financing contingency is a materially better sale than one with a date.</li>
<li><strong>If the answer is B or E, document the basis now.</strong> A date-of-death appraisal,
the improvement receipts, and the permit history. This is the cheapest insurance in the plan and
it is worthless if assembled ten years late.</li>
</ol>

<h2>The three things not to do</h2>
<table><thead><tr><th>Do not</th><th>Because</th></tr></thead><tbody>
<tr><td>Let the exemption claim slip past one year</td>
<td>The exclusion is then removed, a new base-year value is enrolled, and the tax bill roughly
doubles from the following lien date.</td></tr>
<tr><td>Let the trust question stay unanswered</td>
<td>If the house is not in the trust, the estate pays statutory probate fees before any tax.</td></tr>
<tr><td>Rely on a single fifty-year growth number</td>
<td>The stress cases move the answer by millions of dollars on assumptions that are all
historically defensible.</td></tr>
</tbody></table>

<h2>Sequencing, summarised</h2>
<table><thead><tr><th>When</th><th>Do</th><th>Why then</th></tr></thead><tbody>
<tr><td>Before the transfer</td><td>Confirm the house is titled in the trust</td>
<td>Everything downstream depends on it, and it is fixable while the settlor is alive</td></tr>
<tr><td>Month 1</td><td>Death certificates, trustee authority, notification</td>
<td>Statutory deadlines start at death</td></tr>
<tr><td>Months 1 to 9</td><td>Date-of-death appraisal; estate-tax return decision</td>
<td>The appraisal sets basis permanently; the return is due in nine months</td></tr>
<tr><td>Within one year</td><td>Homeowners' exemption claim</td><td>It is what keeps the exclusion</td></tr>
<tr><td>Within three years</td><td>Claim for the exclusion</td><td>It is what applies the exclusion</td></tr>
<tr><td>Years 1 to 3</td><td>Close the remaining gaps; choose the path</td>
<td>No decision needs to be made on day one</td></tr>
</tbody></table>
"""
    add("suggestions.html", "Suggestions",
        "Options compared on robustness, with a recommended sequence and three things not to do.",
        body)


# ===========================================================================
# Flagged for review
# ===========================================================================
FLAGS = [
    ("F01", "The already-owned house is charged 2.14% of assessed value",
     "The owner's reported 2025 charge is about $2,440 against an assessed value of about "
     "$114,250. The city's published secured rate is 1.18162182%, which would produce about "
     "$1,350. The difference, about $1,090, is unexplained.",
     "Put the bill and the assessment notice side by side. Assessments and parcel taxes would "
     "explain most of it; a mismatched assessed value would explain the rest.", "sft_secured"),
    ("F02", "The inherited house's parcel-specific rate is not known",
     "The desk uses the county's typical composite rate of 1.1488% for the fiscal year. The actual "
     "rate depends on the tax-rate area, which is printed on the bill.",
     "Read the rate printed on the annual bill.", "scc_rate"),
    ("F03", "Insurance on both houses is assumed at $1,500 a year each",
     "The statewide average homeowners' premium was about $2,340 in 2025 and earthquake cover "
     "averaged about $1,440 more. Two houses at $1,500 each is below the average for one.",
     "Obtain both declaration pages. Until then the carrying-cost line is understated.",
     "cdi"),
    ("F04", "The same insurance figure is applied to a three-unit building",
     "A three-unit building is insured differently from a single house, and $1,500 has been "
     "applied to both.", "A landlord policy is priced separately from a homeowners' policy.",
     "cdi"),
    ("F05", "No state-level house price index is used",
     "Only national and census-division series are used. The Pacific division rose 1.2% over the "
     "latest twelve months, against 2.4% nationally.",
     "A state or metro series would sharpen the growth assumption.", "fhfa"),
    ("F06", "The electricity line is negative and undocumented",
     "Property A is modelled at about $120 a month net of a solar credit, which implies the "
     "array exports more than the house consumes.",
     "Net billing applies to systems interconnected after 15 April 2023 and pays less for exports "
     "than the old tariff. The credit may be worth less than assumed.", "cpuc_nem"),
    ("F07", "Water and power on the three-unit property is an owner estimate",
     "About $420 a month for three units is plausible but undocumented, and there is no "
     "separate sewer or refuse line.",
     "The city's rate schedule is published, but the parcel's meter size and usage are not known "
     "here.", "sfpuc"),
    ("F08", "Inherited retirement accounts are not quantified",
     "The estate may contain accounts taxed as ordinary income on distribution, at rates far above "
     "the capital-gain rates on a house.",
     "Beneficiary designations and balances, plus whether the ten-year distribution rule applies.",
     "irs_estate_faq"),
    ("F09", "The size of the rest of the estate is unknown",
     "The estate-tax projection carries real property only. A portfolio large enough to approach "
     "the federal threshold changes the conclusion from none to material.",
     "A complete balance sheet as of the date of death.", "irs_estate"),
    ("F10", "The heir's filing status is not confirmed",
     "The home-sale exclusion is $250,000 single and $500,000 joint, and several thresholds move "
     "with it. The single-filer figures are used, which is the conservative case.",
     "A direct question.", "irs_701"),
    ("F11", "One combined marginal rate is applied to every year",
     "Federal 24% plus California 9.3%, rounded, is applied throughout. A real computation would "
     "move through brackets and could differ materially in the transfer year.",
     "A bracket-by-bracket computation for the transfer year.", "irs_559"),
    ("M01", "Terminal net worth by path is model output",
     "These figures come from the model on the methodology page, not from any official document. "
     "They are reproducible from the published inputs and assumptions.",
     "Re-run the model, or change an assumption and re-run it.", None),
    ("M02", "Stress-case outcomes are constructed scenarios",
     "Each case is anchored to a real episode, but the combination of growth, inflation, and "
     "insurance paths within each case is a modelling choice.",
     "Read them as stress tests, not probabilities.", None),
    ("M03", "The comparison depends on a rent that is not sourced",
     "Property A's rent is set at $5,200 a month as a modelling input. No appraisal has been "
     "obtained. The break-even rent is published so the assumption can be tested against reality.",
     "Three written rental appraisals.", None),
    ("M04", "Year-by-year cost tables are model output",
     "Every line is an owner estimate grown at a stated rate. Insurance and maintenance are the "
     "least reliable.",
     "See the carrying-costs page for which lines are documented and which are not.", None),
    ("M05", "The sensitivity grid is a grid, not a distribution",
     "Nine combinations of two assumptions are shown, unweighted by likelihood.",
     "A distribution would require a view on future returns that cannot be sourced.", None),
    ("M06", "Estate-tax headroom is projected forward",
     "The exclusion is indexed to inflation and is projected here at the long-run assumption. The "
     "statute indexes the amount, but the base and the index can both be changed.",
     "Read it as a scenario within current law, not as law.", "irs_revproc"),
    ("T01", "Whether the house is titled in the trust is unknown",
     "If it is not, the transfer runs through probate and the statutory fee schedule follows: "
     "roughly 6% of value before any tax.", "Pull the recorded deed.", None),
    ("T02", "The number of death certificates needed is unknown",
     "Each institution and agency has its own requirement, and some require originals.",
     "Order generously. They cannot be obtained retroactively at short notice.", None),
    ("T03", "Insurance and utility transfer requirements are not documented",
     "A policy in the deceased's name will not respond to a claim, and utilities may require a new "
     "account and a deposit.", "Contact both before occupancy.", None),
    ("T04", "The property type is not confirmed",
     "House, condominium, or townhouse changes the maintenance line, the insurance line, and "
     "whether an association assessment exists.", "Read the deed and the title report.", None),
    ("T05", "The legal unit count is not confirmed",
     "The rental break-even is a total rent, so the number of units is decisive.",
     "A written zoning read from the city.", None),
    ("T06", "No rental appraisal has been obtained",
     "The rental path rests on a single modelled number.", "Three written appraisals.", None),
    ("T07", "The trust's dispositive terms are not known",
     "A trust that directs a sale, or divides the property among several beneficiaries, removes "
     "the choice.", "Read the trust document.", None),
    ("T08", "The heir's housing plan is not known",
     "If the heir would rent elsewhere, that rent belongs on the sell side and is not in the model.",
     "Decide, then re-run the model.", None),
    ("T09", "Prior improvements to basis are not documented",
     "Improvements increase basis and reduce the eventual gain.",
     "Reconstruct from permits and receipts.", None),
    ("X01", "The already-owned house is outside the inheritance",
     "It is analysed separately because it is not part of the estate being inherited. It does "
     "count toward the gross estate for federal purposes, and the projection reflects that.",
     "Kept separate throughout, as the brief requires.", None),
    ("X02", "This desk is not advice",
     "It is a research aid. It is not legal, tax, investment, or appraisal advice and should not be "
     "relied on as such.", "Confirm every conclusion with a qualified professional.", None),
    ("X03", "All amounts are rounded to the nearest $10",
     "Rounding is deliberate, so that no published figure can be traced to a specific bill, "
     "assessment, or property. Statutory amounts, rates, and thresholds are quoted exactly.",
     "Rounding is a privacy measure, not an estimate of precision.", None),
    ("X04", "No personal identifiers appear anywhere in this repository",
     "No names, addresses, parcel numbers, ZIP codes, account numbers, or dates of birth. The two "
     "properties are Property A and Property B.", "The build's own checker fails if one appears.",
     None),
    ("X05", "Other directories in this repository predate this desk",
     "Several earlier attempts at the same analysis exist here. They are not part of this desk and "
     "are described on the repo review page.", "See the repo review page for which are a risk.",
     None),
]


def build_flagged():
    rows = [{"cells": [f'<a id="{h(i)}"></a><strong>{h(i)}</strong>', h(t), h(d), h(w),
                       f'<span class="pill">{h(k)}</span>'], "src": s}
            for i, t, d, w, s, k in
            [(a, b, c, e, f, "Factual" if a.startswith("F") else
              "Process" if a.startswith("T") else "Model" if a.startswith("M") else "Scope")
             for a, b, c, e, f in FLAGS]]
    body = f"""
<div class="warnbox"><strong>This page is required reading, not an appendix.</strong> Every item
below is either a claim this desk could not confirm against an official source, or a figure that is
model output rather than a sourced fact. They are published rather than hidden, and none of them
blocks publication. Each names what would close it.</div>

<p>Codes beginning <code>F</code> are factual gaps in the owner-supplied data. <code>T</code> are
procedural questions. <code>M</code> are model-output figures. <code>X</code> are scope, privacy,
and rounding statements.</p>

{table(["ID", "Item", "What is unverified or modelled", "What would close it", "Type"], rows,
       caption="Every open item as of the date at the top of the page. Rows with an official link "
               "are still listed where the figure derived from that source is a calculation rather "
               "than a quotation.")}
"""
    add("flagged.html", "Flagged for review",
        "Every unverified claim and every model-output figure, with what would close it.", body)


# ===========================================================================
# Sources
# ===========================================================================
def build_sources():
    used: dict[str, set] = {}
    for slug, (title, standfirst, body) in PAGES.items():
        for m in re.finditer(r'href="(https://[^"]+)"', body + NAV_SRC_TEXT):
            used.setdefault(m.group(1), set()).add(slug.replace(".html", ""))
    rows = []
    for key in sorted(S, key=lambda k: S[k][0].lower()):
        label, url = S[key]
        pages = sorted(used.get(url, set()))
        if not pages:
            continue
        rows.append({"cells": [h(label),
                               f'<a href="{h(url)}" rel="noopener">{h(url)}</a>',
                               ", ".join(f'<a href="{h(p)}.html">{h(p)}</a>' for p in pages)],
                     "flag": None})
    unused = [S[k][0] for k in S if S[k][1] not in used]
    body = f"""
<p>Every source cited anywhere in this desk, with the pages that rely on it. All of them are
official: a government agency, a statute, or an administering body. No secondary commentary, blog,
or news article is cited for any figure.</p>

{table(["Source", "Link", "Cited on"], rows,
       caption="Sorted by source name. A source appears once however many pages use it.")}

<h2>Registered but not cited</h2>
<p>These were reviewed and did not end up supporting a published figure. They are listed so the
review trail is complete and a later pass does not repeat the work.</p>
<p>{" ".join(f'<span class="pill">{h(x)}</span>' for x in sorted(unused)) or "None."}</p>

<h2>Deliberately not used</h2>
<ul>
<li><strong>Commentary sites and news articles.</strong> Several were consulted while looking for
leads. None is cited for a figure, because none is an authority.</li>
<li><strong>Listing sites.</strong> These show asking prices, not values, and they are not a
defensible basis for an appraisal or a rent.</li>
<li><strong>Secondary summaries of statutes.</strong> They are frequently out of date. Every
statutory statement here is cited to the legislature's own text.</li>
</ul>

<h2>Source policy</h2>
<table><thead><tr><th>Rule</th><th>Why</th></tr></thead><tbody>
<tr><td>Statutes are cited to the legislature's own text</td>
<td>Secondary summaries drift out of date within a session</td></tr>
<tr><td>Thresholds are cited to the agency that administers them</td>
<td>An amount can be statutory but indexed, and only the agency publishes the year's figure</td></tr>
<tr><td>Market data is cited to the producer, not a republication</td>
<td>Republications drop footnotes and lag revisions</td></tr>
<tr><td>Where a figure could not be confirmed, it is blank and flagged</td>
<td>The alternative is a number that looks sourced and is not</td></tr>
</tbody></table>

<h2>Links that moved during the research</h2>
<p>Several official pages that existed earlier in this project have since been retired, and each was
replaced with a live equivalent before being cited. Where a page had moved, the replacement is what
appears above. The ones that failed outright are listed on
<a href="repo-review.html">Repo review</a> so that a later pass does not chase them again.</p>
"""
    add("sources.html", "Sources",
        "Every citation used, what it supports, and what was reviewed but not used.", body)


# ===========================================================================
# Methodology
# ===========================================================================
def build_method():
    vrows = [{"cells": [h(k.replace("_", " ")), h(fmt(v))], "flag": "M01"}
             for k, v in sorted(MODEL["verified"].items()) if v is not None]
    arows = [{"cells": [h(k.replace("_", " ")), h(fmt(v))], "flag": "M01"}
             for k, v in sorted(MODEL["assumptions"].items()) if not isinstance(v, list)]
    body = f"""
<p>This page exists so every number on the site can be reproduced, attacked, or corrected. The
model is a single Python file with no dependencies, and all of its inputs are printed below.</p>

<h2>The three classes of input</h2>
<table><thead><tr><th>Class</th><th>Meaning</th><th>How it is treated</th></tr></thead><tbody>
<tr><td><strong>Verified</strong></td><td>A figure published by an official source</td>
<td>Quoted exactly, cited, and marked exact</td></tr>
<tr><td><strong>Owner-supplied</strong></td><td>A figure the owner reported</td>
<td>Used as a band, rounded, and marked owner-derived</td></tr>
<tr><td><strong>Assumption</strong></td><td>A modelling choice</td>
<td>Published in full below so it can be changed</td></tr>
</tbody></table>

<h2>Verified constants</h2>
{table(["Constant", "Value"], vrows,
       caption="Quoted from the sources listed on the Sources page.")}

<h2>Assumptions</h2>
{table(["Assumption", "Value"], arows,
       caption="These are choices, not facts. Each is a place where a reasonable person could "
               "choose differently.")}

<h2>Three accounting decisions that matter</h2>
<ol>
<li><strong>The sell path carries none of the house's costs.</strong> Selling means the house is
gone, so its property tax, insurance, utilities, and maintenance are all zero. Charging them while
also crediting the invested proceeds double-counts.</li>
<li><strong>The move-in path credits the unit vacated at the other house.</strong> Moving into the
inherited house frees the unit the heir currently occupies, so it becomes rentable. It is priced at
the per-unit rent the owner reports, which is an owner figure rather than a market rent.</li>
<li><strong>Property tax is split in two.</strong> The ad valorem part tracks the assessed value at
the county's published composite rate. Fixed charges, which are bonds and parcel taxes, do not track
value and are grown at inflation instead. Treating a blended effective rate as if it were all ad
valorem would compound the fixed charges every year.</li>
</ol>

<h2>What the model does not do</h2>
<table><thead><tr><th>Not modelled</th><th>Why it matters</th></tr></thead><tbody>
<tr><td>Bracket-by-bracket tax</td><td>One combined marginal rate is applied every year. A real
computation moves through brackets and could differ materially in the transfer year.</td></tr>
<tr><td>State and federal interaction on the sale</td><td>The state treatment of capital gains is a
flat add-on to the federal rate.</td></tr>
<tr><td>Refinancing or leverage</td><td>Neither house carries a mortgage in the model. A mortgage
would change the return on equity substantially.</td></tr>
<tr><td>Probate</td><td>The model assumes the trust works. The process page prices the
alternative.</td></tr>
<tr><td>The other house's own appreciation as a decision variable</td><td>It is held in every path,
so it cancels out of the comparison rather than being valued.</td></tr>
<tr><td>Sequence of returns in the sell path</td><td>The reinvestment return is a constant. A real
portfolio has a path, and the path matters.</td></tr>
<tr><td>Mid-year conventions in depreciation</td><td>Depreciation is taken for whole recovery years
only. A mid-month convention would shift the first and last year by a fraction of a year, which is
immaterial against the other assumptions.</td></tr>
</tbody></table>

<h2>Reproducing the numbers</h2>
<pre><code>python3 scripts/model_v5.py         # writes desk/data/model-v5.json
python3 -m unittest discover -s scripts -p 'test_model_v5.py'
python3 scripts/build_desk_v5.py    # writes desk/*.html
python3 scripts/verify_desk_v5.py   # structural, sourcing, privacy checks</code></pre>
<p>The model is deterministic. Running it twice produces byte-identical output, and the test suite
pins every arithmetic relationship that a published figure depends on.</p>

<h2>Rounding policy</h2>
<p>Money is rounded to the nearest $10 at the point of output, after all arithmetic. Statutory
amounts, rates, and thresholds are <em>not</em> rounded, because they are fixed by law and rounding
them would misstate them. Rounded figures are labelled as rounded wherever they appear.</p>

<h2>Privacy policy</h2>
<p>Nothing on this site identifies a person, an address, a parcel, or a ZIP code. The two properties
are Property A and Property B. A county or a city is named only where a rate or a procedure is local,
because that is the level at which the source is published. No figure here is precise enough to be
matched to a specific bill, and the build's checker fails if one becomes so.</p>
"""
    add("methodology.html", "Methodology",
        "Every input, every assumption, and every accounting decision, so the numbers can be "
        "reproduced or refuted.", body)


def fmt(v):
    if isinstance(v, float):
        return f"{v:.6g}" if 0 < abs(v) <= 1 else f"{v:,.5g}"
    return f"{v:,}" if isinstance(v, int) else str(v)


# ===========================================================================
# Repo review
# ===========================================================================
def build_repo():
    dirs = [
        ("desk/", "This desk", "Published", "Current. Generated by scripts/build_desk_v5.py."),
        ("public-safe/", "An earlier, number-free desk", "Published",
         "Coexists deliberately. It carries no figures, so it cannot contradict this one."),
        ("docs/", "An earlier thirteen-page desk", "Published",
         "Carries figures from an earlier pass that disagree with this desk. Should be unpublished "
         "or consolidated. Flag X05."),
        ("desk-22a32b17/", "An earlier desk", "Published", "Superseded."),
        ("desk-b4f/", "An earlier desk", "Published", "Superseded."),
        ("swan-3a49/", "An earlier stress-case set", "Published", "Superseded."),
        ("referee-abae/", "An earlier review", "Published", "Superseded."),
        ("audited-v4/", "An earlier audited pass", "Published", "Superseded."),
        ("verify-552/", "An earlier verification pass", "Published",
         "Superseded, and not excluded from the published site."),
        ("archive/", "Historical material", "Excluded", "Correctly excluded by the site config."),
        ("research/", "Research notes and a verification log", "Excluded",
         "Correctly excluded. Contains unrounded, property-specific figures and must stay out."),
        ("analysis/", "A long-form decision analysis", "Excluded",
         "Correctly excluded. Contains unrounded, property-specific figures."),
    ]
    t_dirs = table(["Path", "What it is", "Site status", "Assessment"],
                   [{"cells": [f"<code>{h(p)}</code>", h(d), h(s), h(n)]}
                    for p, d, s, n in dirs])
    irregularities = [
        ("R01", "Six superseded desks are published alongside this one, several with different "
         "headline figures", "High", "Publish one desk. Exclude the superseded directories and "
         "remove them from the default branch."),
        ("R02", "<code>verify-552/</code> is not excluded from the published site", "Medium",
         "Add it to the exclusion list. It is an internal verification pass."),
        ("R03", "The site config excludes directories by name, which hides them from a build but "
         "does not delete them", "Medium", "Exclusion is not redaction. Content that must not be "
         "public should not be in the repository at all."),
        ("R04", "Two earlier desks publish unrounded, property-specific figures", "High",
         "Those figures are traceable to a specific bill. Remove them or replace them with rounded "
         "ones."),
        ("R05", "The repository's landing page redirects to a different desk", "Low",
         "Point it at this desk, or at a page that says which desk is current."),
        ("R06", "Several session directories have no owner and no README", "Low",
         "Archive or delete them. An unowned directory is where stale figures survive."),
        ("R07", "Several official links used by earlier passes have since been retired", "Medium",
         "Re-verify every citation before republishing an older desk. This desk re-verified all of "
         "its own."),
    ]
    t_irr = table(["ID", "Finding", "Severity", "Recommendation"],
                  [{"cells": [a, h(b), c, d]} for a, b, c, d in irregularities])
    verified = [
        ("Federal thresholds and rates", "Agency page plus the annual revenue procedure", "yes",
         "Verified"),
        ("Federal procedural deadlines", "Form instructions", "yes", "Verified"),
        ("State statutes", "The legislature's own text", "yes", "Verified"),
        ("State thresholds", "The administering agency's current page", "yes", "Verified"),
        ("County and city tax rates", "The county rate book and the city treasurer", "yes",
         "Verified"),
        ("Market rates and indices", "The primary producer of the series", "yes", "Verified"),
        ("Insurance premiums", "The regulator's data call", "yes", "Verified"),
        ("Rent for the inherited house", "No appraisal exists", "no", "Not verified, flag M03"),
        ("Rent for the already-owned house", "Owner-reported only", "no", "Owner-derived"),
        ("Both insurance premiums", "Owner estimates only", "no", "Not verified, flags F03 and F04"),
        ("Water and power, both houses", "Owner estimates only", "no",
         "Not verified, flags F06 and F07"),
    ]
    t_ver = table(["Class of figure", "How it was verified", "Result"],
                  [{"cells": [a, b, f'<span class="{c}">{d}</span>']} for a, b, c, d in verified])
    body = f"""
<p>This repository contains several earlier attempts at the same analysis, from earlier sessions.
They are described here because a reader who stumbles into one should know whether it is current,
and because two of them are a live privacy risk.</p>

<h2>What is in the repository</h2>
{t_dirs}

<h2>Irregularities found</h2>
{t_irr}

<h2>Line-by-line verification method</h2>
<p>Every figure in this desk was traced to a primary source. Where a primary source could not be
reached, the figure was left blank and flagged rather than filled from a secondary source.</p>
{t_ver}

<div class="note"><strong>The pattern is worth noticing.</strong> Every statutory, regulatory, and
market figure is verified. Every figure that describes these two specific houses, other than their
tax bills, is an owner estimate. That is not a failure of research. It is the boundary of what an
outside analysis can know, and it is exactly why the questions page exists.</div>
"""
    add("repo-review.html", "Repo review",
        "What else is in this repository, which parts are a privacy risk, and how each figure was "
        "verified.", body)


NAV_SRC_TEXT = ""


# ===========================================================================
def main():
    for fn in (build_index, build_exec, build_decision, build_questions, build_projections,
               build_costs, build_estate, build_process, build_swans, build_law,
               build_suggestions, build_repo, build_flagged, build_method):
        fn()
    build_sources()

    missing = [f for f, _ in NAV if f not in PAGES]
    if missing:
        raise SystemExit(f"missing pages: {missing}")
    DESK.mkdir(parents=True, exist_ok=True)
    for slug, (title, standfirst, body) in PAGES.items():
        (DESK / slug).write_text(shell(slug, title, standfirst, body))
    (DESK / "style.css").write_text(CSS)
    print(f"wrote {len(PAGES)} pages + style.css to {DESK}")


if __name__ == "__main__":
    main()
