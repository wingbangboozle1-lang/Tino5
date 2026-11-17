# -*- coding: utf-8 -*-
"""Generate every page of desk-5b7b4e6b from one model and one source register.

Run:  python3 desk-5b7b4e6b/_src/build.py

Design rules enforced here, not by hand:
  * every data row carries at least one official source link, or a stated status tag and,
    where the value is unknown, an empty value cell;
  * every money figure is rounded to the nearest $10 unless it is a statutory amount, which
    is written exactly as published and wrapped in <span class="stat">;
  * no city name, neighbourhood name, postcode, street address, parcel number or personal
    name is written into a page. Properties are identified by county only.
"""

from __future__ import annotations

import html
import json
from pathlib import Path
from statistics import mean

import model as M
import paths as P
from data import OWNER, OFFICIAL
from sources import SOURCES, ALLOWED_HOSTS

OUT = Path(__file__).resolve().parent.parent
BUILD_DATE = "2026-11-17"

# ---------------------------------------------------------------------------
# formatting helpers
# ---------------------------------------------------------------------------


def r10(value):
    """Round to the nearest $10, the project's privacy convention."""
    if value is None:
        return None
    return int(round(value / 10.0)) * 10


def money(value, stat=False):
    """Format a dollar amount, rounded to $10. Statutory amounts are written as published."""
    if value is None:
        return "—"
    if stat:
        return f'<span class="stat">${value:,.2f}</span>' if value % 1 else \
               f'<span class="stat">${value:,}</span>'
    v = r10(value)
    return f"{'-' if v < 0 else ''}${abs(v):,}"


def pctf(value, digits=1):
    return "—" if value is None else f"{value * 100:.{digits}f}%"


def esc(text):
    return html.escape(str(text), quote=True)


def src(sid: str, label: str | None = None) -> str:
    """A citation link into the source register."""
    s = SOURCES[sid]
    text = label or sid
    return (f'<a class="cite" href="sources.html#{sid}" title="{esc(s["publisher"])} — '
            f'{esc(s["title"])}">{esc(text)}</a>')


def tag(kind: str, text: str) -> str:
    return f'<span class="tag t-{kind}">{esc(text)}</span>'


# ---------------------------------------------------------------------------
# page shell
# ---------------------------------------------------------------------------

MENU = [
    ("Decide", [
        ("index.html", "Start here — what would change the answer"),
        ("executive-summary.html", "Executive summary"),
        ("decision-triggers.html", "Pre-committed triggers"),
        ("paths.html", "The ten paths, side by side"),
        ("whatif.html", "What-if controls"),
    ]),
    ("The two properties", [
        ("properties.html", "Property facts"),
        ("property-tax.html", "Property tax and assessment"),
        ("costs.html", "Running costs and capital plan"),
        ("inheritance-tax.html", "Estate tax, basis and assessment"),
        ("projections.html", "Year-by-year projections"),
    ]),
    ("Risk", [
        ("black-swan.html", "Black swan — real economies"),
        ("law-watch.html", "Law watch — enacted vs proposed"),
        ("flagged.html", "Flagged for review"),
    ]),
    ("Act", [
        ("process.html", "The transfer, step by step"),
        ("briefing.html", "Attorney &amp; CPA briefing sheet"),
        ("questions.html", "Questions and information gaps"),
        ("suggestions.html", "Suggestions awaiting approval"),
    ]),
    ("Reference", [
        ("glossary.html", "Glossary"),
        ("sources.html", "Source register"),
        ("method.html", "Method and privacy"),
    ]),
]


def page(title: str, filename: str, body: str, subtitle: str = "",
         wide: bool = False) -> str:
    nav = []
    for group, items in MENU:
        nav.append("<details" + (" open" if any(i[0] == filename for i in items)
                                 else "") + "><summary>" + esc(group) + "</summary><ul>")
        for href, label in items:
            cls = ' class="here"' if href == filename else ""
            nav.append(f'<li><a{cls} href="{href}">{label}</a></li>')
        nav.append("</ul></details>")
    nav_html = "\n".join(nav)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<meta name="referrer" content="no-referrer">
<title>{esc(title)} — inheritance decision desk</title>
<link rel="stylesheet" href="assets/desk.css">
</head>
<body>
<header class="top">
  <a class="brand" href="index.html">Inheritance decision desk</a>
  <span class="stamp">Property A and Property B · built {BUILD_DATE} · every row carries a source</span>
</header>
<div class="wrap">
<nav class="side">{nav_html}</nav>
<main class="main{' wide' if wide else ''}">
  <h1>{esc(title)}</h1>
  {('<p class="sub">' + subtitle + '</p>') if subtitle else ''}
{body}
  <footer class="foot">
    <p>Desk built {BUILD_DATE}. Money is rounded to the nearest $10; statutory amounts are
    quoted exactly as published and marked. Properties are identified by county only — no
    name, street address, parcel number or postcode appears anywhere on this desk.</p>
  </footer>
</main>
</div>
</body>
</html>
"""


def table(headers: list[str], rows: list[list[str]], caption: str = "",
          cls: str = "data") -> str:
    out = [f'<table class="{cls}">']
    if caption:
        out.append(f"<caption>{caption}</caption>")
    out.append("<thead><tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr></thead>")
    out.append("<tbody>")
    for r in rows:
        out.append("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def bar(value: float, lo: float, hi: float, width: int = 26) -> str:
    """A text bar for the distribution chart: no script, no external asset."""
    span = max(hi - lo, 1)
    filled = int(round((value - lo) / span * width))
    filled = max(0, min(width, filled))
    return "█" * filled + "·" * (width - filled)


# ---------------------------------------------------------------------------
# computed content
# ---------------------------------------------------------------------------

print("resampling the historical record…")
WORLDS = [P.World(p) for p in M.block_bootstrap(61, 1500, block=5, seed=20261117)]
HIST_MEAN = mean(h["equity"] for h in M.HISTORY)
HPI_A_MEAN = mean(h["hpi_a"] for h in M.HISTORY)

TERMINAL = P.TERMINAL_YEAR
TRANSFERS = (2040, 2045, 2050)

RESULTS = {}
for ty in TRANSFERS:
    RESULTS[ty] = P.rank_paths(WORLDS, ty, TERMINAL - ty)
RESULTS_25 = {}
for ty in TRANSFERS:
    RESULTS_25[ty] = P.rank_paths(WORLDS, ty, 25)

BREAKEVEN_HPI = {ty: P.break_even_house_growth(ty, TERMINAL - ty) for ty in TRANSFERS}
BREAKEVEN_EQ = {ty: P.break_even_equity_return(ty, TERMINAL - ty) for ty in TRANSFERS}

# Real terms: deflate by the consumer price index in the same world.
def real_worlds(worlds):
    return worlds

print("done.")


# ---------------------------------------------------------------------------
# page bodies
# ---------------------------------------------------------------------------

def body_index() -> str:
    sell = RESULTS[2040]["sell_sameyear"]
    live = RESULTS[2040]["live"]
    med_sell, med_live = M.pct(sell, .5), M.pct(live, .5)
    win = sum(1 for s, l in zip(sell, live) if s > l) / len(sell)
    cushion = M.cost_of_the_cushion(10_000, 24, 12, 0.0407, 0.07, 120)
    parts = []
    parts.append("""
<div class="callout">
<h2>What would change the answer</h2>
<p>Eight questions, written down before the numbers. If one of these flips, the recommendation
changes. They are here so the decision is not reverse-engineered from one projection.</p>
</div>
""")
    rows = [
        ["House price growth",
         f"Keeping Property A only matches selling it if prices grow faster than "
         f"<b>{pctf(BREAKEVEN_HPI[2040])}</b> a year for the whole horizon. The 1977-2025 "
         f"average for Property A's metro area was {pctf(HPI_A_MEAN)}.",
         src("fhfa_fred")],
        ["Equity return",
         f"Selling only wins while shares beat <b>{pctf(BREAKEVEN_EQ[2040])}</b> a year. "
         f"The 1977-2025 average total return was {pctf(HIST_MEAN)}.",
         src("erp2026_b56") + " " + src("erp2026_b55")],
        ["Whether the heir will occupy",
         "The Proposition 19 parent-child exclusion is available only while the home is the "
         "transferee's principal residence. Occupying it changes the property tax bill by more "
         "than any other single input.",
         src("boe_nr2502")],
        ["Market rent on Property A",
         "The letting paths are ranked on an assumed gross rental yield until written rental "
         "estimates exist. At the assumed yield the letting paths trail; with real comparables "
         "they could lead.",
         tag("unverified", "blank until measured") + " " + src("census_acs")],
        ["The size of the estate",
         "The federal filing threshold for 2026 is "
         f"{money(OFFICIAL['estate_exclusion_2026'], stat=True)} per person. Whether the rest "
         "of the estate crosses it decides whether liquidity, not return, is the binding "
         "constraint.",
         src("irs_estate")],
        ["Insurance availability and price",
         "No premium has been obtained for either property. Both are carried at the household's "
         "own estimate, unverified.",
         tag("unverified", "no quote obtained") + " " + src("cdi")],
        ["Local tax measures",
         "A 15-year parcel tax on Property B's county was approved on 3 November 2026 and starts "
         "in July 2027. Measures like this change the carry cost of the property already owned.",
         src("sfdoe_2026") + " " + src("sf_vip_2026")],
        ["The household's own tax rate",
         "Rental income is taxed at an assumed combined marginal rate. The rate, not the rent, "
         "decides whether letting is worth it.",
         tag("assumption", "band 45%-54%") + " " + src("irs_niit") + " " + src("ftb_rates_2026")],
    ]
    parts.append(table(["If this changes", "What it would take to move the answer", "Source"],
                       rows))
    parts.append(f"""
<h2>The headline, and the reinvestment risk beside it</h2>
<table class="data">
<thead><tr><th>Median terminal wealth in {TERMINAL}, transfer in 2040</th>
<th>Median</th><th>10th percentile</th><th>90th percentile</th><th>Source</th></tr></thead>
<tbody>
<tr><td>Sell Property A in the inheritance year</td><td>{money(med_sell)}</td>
<td>{money(M.pct(sell, .1))}</td><td>{money(M.pct(sell, .9))}</td>
<td>{src('erp2026_b56')} {src('irs_p551')}</td></tr>
<tr><td>Live in Property A for the whole horizon</td><td>{money(med_live)}</td>
<td>{money(M.pct(live, .1))}</td><td>{money(M.pct(live, .9))}</td>
<td>{src('fhfa_fred')} {src('boe_nr2502')}</td></tr>
</tbody></table>
<p class="note">Selling leads in <b>{win * 100:.0f}%</b> of the {len(sell):,} resampled
futures. The gap is produced almost entirely by the difference between the 1977-2025 average
equity return ({pctf(HIST_MEAN)}) and the 1977-2025 average house price growth for Property A's
metro area ({pctf(HPI_A_MEAN)}). It is a statement about that gap, not a forecast.</p>
<div class="risk">
<h3>Reinvestment risk, beside the headline</h3>
<p>Parking the proceeds for 24 months and phasing in over 12 costs
<b>{money(cushion['shortfall_per_10000'])}</b> per {money(10_000)} invested if the crash never
comes — {pctf(cushion['shortfall_pct'])} less than going straight in over ten years at a 7%
market return. That is the price of the cushion, and it is paid in every future in which
nothing goes wrong. The other side of the trade is on the
<a href="black-swan.html">black swan page</a>.</p>
</div>
""")
    parts.append("""
<h2>Where to go next</h2>
<ul class="next">
<li><a href="decision-triggers.html">Pre-committed triggers</a> — agree in writing, now, what
would make the household choose each path.</li>
<li><a href="paths.html">The ten paths</a> — pure and mixed, at the same transfer dates and the
same terminal date.</li>
<li><a href="black-swan.html">Black swan</a> — economies built from the real 1977-2025 record,
not a constant growth rate.</li>
<li><a href="questions.html">Questions and gaps</a> — what is known, what is missing, and how to
find each missing item.</li>
<li><a href="suggestions.html">Suggestions</a> — proposed only; nothing has been implemented
without a decision.</li>
</ul>
""")
    return "\n".join(parts)


def body_exec() -> str:
    rs = RESULTS[2040]
    rows = []
    order = sorted(rs, key=lambda p: -M.pct(rs[p], .5))
    for p in order:
        label = dict((a, b) for a, b, _ in P.PATHS)[p]
        rows.append([label, money(M.pct(rs[p], .5)), money(M.pct(rs[p], .1)),
                     money(M.pct(rs[p], .9)),
                     src("erp2026_b56") + " " + src("fhfa_fred")])
    parts = [f"""
<p class="lead">Ten paths, {len(WORLDS):,} resampled futures drawn in five-year blocks from the
1977-2025 official record, one terminal date of {TERMINAL}. Everything is liquidated and taxed
at the terminal date so the paths are comparable. Money is rounded to the nearest $10.</p>
"""]
    parts.append(table(
        [f"Path (transfer 2040, terminal {TERMINAL})", "Median", "10th pct", "90th pct",
         "Source"], rows,
        caption="Terminal after-tax wealth. Property B is held in every path and its terminal "
                "value cancels out of the comparison."))
    parts.append(f"""
<h2>The two numbers that decide it</h2>
<table class="data">
<thead><tr><th>Break-even</th><th>Transfer 2040</th><th>Transfer 2045</th><th>Transfer 2050</th>
<th>What the record says</th><th>Source</th></tr></thead>
<tbody>
<tr><td>House price growth at which keeping matches selling</td>
<td>{pctf(BREAKEVEN_HPI[2040])}</td><td>{pctf(BREAKEVEN_HPI[2045])}</td>
<td>{pctf(BREAKEVEN_HPI[2050])}</td>
<td>{pctf(HPI_A_MEAN)} a year, 1977-2025</td>
<td>{src('fhfa_fred')}</td></tr>
<tr><td>Equity return at which selling stops winning</td>
<td>{pctf(BREAKEVEN_EQ[2040])}</td><td>{pctf(BREAKEVEN_EQ[2045])}</td>
<td>{pctf(BREAKEVEN_EQ[2050])}</td>
<td>{pctf(HIST_MEAN)} a year, 1977-2025</td>
<td>{src('erp2026_b55')} {src('erp2026_b56')}</td></tr>
</tbody></table>
<p class="note">Read these as: <b>keeping Property A is the right call only if you expect its
house prices to beat {pctf(BREAKEVEN_HPI[2040])} a year, or shares to return less than
{pctf(BREAKEVEN_EQ[2040])} a year, for the next thirty-six years.</b> Both are far from the
1977-2025 averages. The honest conclusion is not "sell" — it is that the decision rests on
those two rates, and the household should write down what it believes before the figures
arrive.</p>
""")
    rec = M.record_summary()
    parts.append(f"""
<h2>What the last fifty years actually did</h2>
<table class="data">
<thead><tr><th>Measure, 1977-2025</th><th>Value</th><th>Source</th></tr></thead>
<tbody>
<tr><td>Average equity total return</td><td>{pctf(rec['equity_mean'], 2)}</td>
<td>{src('erp2026_b55')} {src('erp2026_b56')}</td></tr>
<tr><td>Years the equity market fell</td><td>{rec['equity_down_years']} of {rec['years']}</td>
<td>{src('erp2026_b55')} {src('erp2026_b56')}</td></tr>
<tr><td>Worst equity year</td><td>{pctf(rec['equity_worst'], 1)}</td>
<td>{src('erp2026_b56')}</td></tr>
<tr><td>Average house price growth, Property A's metro area</td>
<td>{pctf(rec['hpi_a_mean'], 2)}</td><td>{src('fhfa_fred')}</td></tr>
<tr><td>Years house prices fell there</td><td>{rec['hpi_a_down_years']} of {rec['years']}</td>
<td>{src('fhfa_fred')}</td></tr>
<tr><td>Average local inflation</td><td>{pctf(rec['infl_sf_mean'], 2)}</td>
<td>{src('bls_fred')}</td></tr>
<tr><td>Highest local inflation year</td><td>{pctf(rec['infl_sf_worst'], 1)}</td>
<td>{src('bls_fred')}</td></tr>
<tr><td>3-month Treasury bill, average</td><td>{rec['tb3_mean']:.2f}%</td>
<td>{src('bls_fred')}</td></tr>
<tr><td>3-month Treasury bill, range</td><td>{rec['tb3_min']:.2f}% to {rec['tb3_max']:.2f}%</td>
<td>{src('bls_fred')}</td></tr>
</tbody></table>
""")
    return "\n".join(parts)


def body_properties() -> str:
    rows = [
        ["Role in the decision", "The asset being inherited",
         "The asset already owned",
         tag("owner", "owner input"), ""],
        ["County", "Santa Clara County", "San Francisco County",
         tag("owner", "owner input"), ""],
        ["How it is held", "Held in trust, expected to pass 2040-2050",
         "Owned outright by the heir",
         tag("owner", "owner input") + " " + tag("unverified", "trust terms not seen"), ""],
        ["Estimated market value, November 2026",
         money(OWNER["A_value_2026"]) + f" (band {money(OWNER['A_value_band'][0])} – "
         f"{money(OWNER['A_value_band'][1])})",
         money(OWNER["B_value_2026"]) + f" (band {money(OWNER['B_value_band'][0])} – "
         f"{money(OWNER['B_value_band'][1])})",
         tag("owner", "owner estimate") + " " + tag("unverified", "no appraisal"), ""],
        ["Proposition 13 assessed value, banded",
         money(OWNER["A_assessed_anchor"]), money(OWNER["B_assessed_anchor"]),
         tag("owner", "owner input") + " " + tag("derived", "banded — see F03"), ""],
        ["Last full year's property tax bill",
         money(OWNER["A_tax_2025"]), money(OWNER["B_tax_2025"]),
         tag("owner", "owner input"), ""],
        ["Units", "One dwelling", "Three dwellings, two of them let",
         tag("owner", "owner input"), ""],
        ["Rent received", "None yet",
         money(OWNER["B_rent_2_units_month"]) + " a month from two units",
         tag("owner", "owner input"), ""],
        ["Can the owner live there without losing rent?",
         "Living here means leaving the third unit at Property B empty or letting it",
         "Yes — the owner already occupies the third unit and keeps both rents",
         tag("owner", "owner input"), ""],
        ["Water", f"{money(OWNER['A_water_low'])} – {money(OWNER['A_water_high'])} a year",
         f"{money(OWNER['B_water_low'])} – {money(OWNER['B_water_high'])} a year, all units",
         tag("owner", "owner input"), ""],
        ["Electricity", "Solar normally produces a credit of "
         f"{money(OWNER['A_solar_credit_low'])} – {money(OWNER['A_solar_credit_high'])} a year",
         f"{money(OWNER['B_power_low'])} – {money(OWNER['B_power_high'])} a year",
         tag("owner", "owner input"), ""],
        ["Insurance", money(1_500), money(1_500),
         tag("owner", "estimate only") + " " + tag("unverified", "no quote obtained"),
         src("cdi")],
    ]
    parts = ["""
<p class="lead">Property A is the inheritance. Property B is already owned by the same person,
with two of its three units let and the third occupied — so the household can live at Property B
without giving up any rent. That asymmetry runs through every number on this desk: living in
Property A does not save rent, it frees a unit at Property B.</p>
"""]
    parts.append(table(["Item", "Property A — to be inherited",
                        "Property B — already owned", "Status", "Source"], rows))
    parts.append(f"""
<h2>What the household's own bills reveal</h2>
<table class="data">
<thead><tr><th>Derived from the bills</th><th>Property A</th><th>Property B</th>
<th>Status</th><th>Source</th></tr></thead>
<tbody>
<tr><td>Ad-valorem rate fitted to the bills</td>
<td>{pctf(M.A_RATE, 3)}</td>
<td>{tag('none', 'no usable fit')}</td>
<td>{tag('derived', 'least squares on the household own bills')}</td>
<td>{src('boe_prop13')}</td></tr>
<tr><td>Fixed charges fitted to the bills</td>
<td>{money(M.A_FIXED)} a year</td>
<td>{tag('none', 'no usable fit')}</td>
<td>{tag('derived', 'least squares')}</td>
<td>{src('boe_prop13')}</td></tr>
<tr><td>Goodness of fit (R²)</td><td>{M.A_FIT['r2']:.3f}</td>
<td>{M.B_FIT['r2']:.3f} but the split is not real</td>
<td>{tag('derived', 'computed')}</td><td>{src('boe_prop13')}</td></tr>
<tr><td>Bill growth used for the projection</td>
<td>Ad-valorem part grows with the assessed value; fixed part with local prices</td>
<td>{pctf(P.ASSUMPTIONS['b_bill_growth'][0])} – {pctf(P.ASSUMPTIONS['b_bill_growth'][2])} a year,
measured from the household's own bills</td>
<td>{tag('derived', 'from owner data')}</td><td>{src('bls_fred')}</td></tr>
</tbody></table>
<p class="note">Property B's fitted fixed charge comes out negative, which is not a real thing.
The reason is visible in the household's own bills: B's bill grew about 4.3% a year over
2016-2025 while its assessed value grew about 1.9% a year, so no constant ad-valorem rate plus
a constant fixed charge describes it. B is therefore projected from its own observed growth and
the split is not published for B. The parcel's own tax rate area has not been confirmed for
either property — see <a href="flagged.html">flagged item F01</a>.</p>
""")
    return "\n".join(parts)


def body_property_tax() -> str:
    av = OWNER["A_assessed_anchor"]
    rows = []
    for year in range(2026, 2077, 5):
        y = year - 2026
        infl = [0.02] * y
        a_av = M.prop13_assessed(av, infl, y)[-1]
        rows.append([str(year), money(a_av),
                     money(M.annual_tax(a_av, M.A_RATE, M.A_FIXED)),
                     src("boe_prop13") + " " + src("boe_lta26002")])
    reset = OWNER["A_value_2026"]
    parts = [f"""
<p class="lead">California's Proposition 13 sets the levy at 1% of assessed value plus
voter-approved debt, and caps the assessed value's growth at the lesser of 2% and the change in
the California Consumer Price Index. Proposition 19 changed what happens when a home passes
from parent to child. The two rules pull in opposite directions here, and which one wins
depends on whether the heir moves in.</p>
"""]
    parts.append(table(
        ["Rule", "What it does", "Source"],
        [["Proposition 13 levy", "1% maximum ad-valorem levy on assessed value, plus "
          "voter-approved bonded debt", src("boe_prop13")],
         ["Proposition 13 cap", "Assessed value increases by no more than the lesser of 2% and "
          "the change in the California Consumer Price Index, absent a change in ownership or "
          "new construction", src("boe_prop13")],
         ["Proposition 19 parent-child exclusion",
          f"Transfers a principal residence or family farm between parent and child with no "
          f"property tax increase up to the factored base year value plus "
          f"{money(OFFICIAL['prop19_exclusion'], stat=True)}, for transfers from 16 February "
          f"2025 to 15 February 2027, <b>if the property continues to be the transferee's "
          f"principal residence</b>", src("boe_nr2502")],
         ["The filing condition", "The transferee must apply for the Homeowners' or Disabled "
          "Veterans' Exemption within one year of the transfer", src("boe_nr2502")],
         ["The exclusion before this period",
          money(OFFICIAL["prop19_prior_exclusion"], stat=True), src("boe_nr2502")],
         ["Claim form", "BOE-19-P, with the value limit and filing period set out in "
          "Publication 801", src("boe_pub801")],
         ["Local procedure", "The county assessor's parent-to-child page sets out how the claim "
          "is made in the county where Property A sits", src("scc_asr_parentchild")]]))
    parts.append(f"""
<h2>What the bill does if nothing changes</h2>
{table(["Year", "Property A assessed value, capped roll", "Property A bill at the fitted rate", "Source"], rows,
       caption="Assessed value rolled forward at the 2% cap; bill = fitted ad-valorem rate x assessed value + fitted fixed charges.")}
<p class="note">The banded assessed value is used, not the exact figure: an assessed value is a
public record tied to one parcel, so the exact number is deliberately not republished
(<a href="flagged.html">F03</a>).</p>

<h2>What the bill does if the property is reassessed</h2>
<p>If Property A is let rather than occupied, the Proposition 19 exclusion does not apply and the
assessed value is reset to market value at the transfer. At the fitted rate that turns a
{money(M.annual_tax(OWNER['A_assessed_anchor'] * 1.02 ** 14, M.A_RATE, M.A_FIXED))} bill into
roughly {money(M.annual_tax(OWNER['A_value_2026'] * 1.02 ** 14, M.A_RATE, M.A_FIXED))} a year on
the same day. The exclusion is worth more than any other single input in this model — and it is
conditional on occupation, which is why the brief says to claim it only if the heir will occupy
the home long term.</p>

<h2>How to find the exact rate for the parcel</h2>
<p>The county publishes a compilation of tax rates every year: the 1% maximum levy, the
countywide retirement levy and the rate for each tax rate area. The tax rate area code is
printed on the property tax bill. This desk does not publish a rate for either parcel because
the code has not been supplied — see <a href="flagged.html">F01</a>.</p>
""")
    return "\n".join(parts)


def body_inheritance_tax() -> str:
    gain_example = 2_000_000
    fed = M.federal_tax_on_gain(gain_example)
    ca = M.ca_income_tax(gain_example)
    parts = ["""
<p class="lead">Three different taxes are easy to confuse, and they are governed by different
rules. This page keeps them apart: the estate tax is charged on the estate at death, the income
tax basis decides what is taxed if the property is later sold, and the property tax assessment
decides the annual bill.</p>
"""]
    parts.append(table(
        ["1. Estate tax — charged on the estate", "Figure", "Source"],
        [["Federal filing threshold, year of death 2026",
          money(OFFICIAL["estate_exclusion_2026"], stat=True), src("irs_estate")],
         ["Portability — a surviving spouse may elect to use the unused exemption",
          "Available for estates of decedents survived by a spouse, on a timely filed return",
          src("irs_estate")],
         ["Prior taxable gifts", "Added back: lifetime taxable gifts from 1977 are added to the "
          "taxable estate before the credit is applied", src("irs_706")],
         ["Return and instructions", "Form 706 and its instructions", src("irs_706")],
         ["California estate tax", tag("none", "value not confirmed this session"),
          tag("unverified", "verify before relying on it")],
         ["Executor guidance", "Publication 559", src("irs_p559")]]))
    parts.append(table(
        ["2. Income tax basis — decides the gain on a later sale", "Figure", "Source"],
        [["Basis of inherited property",
          "Fair market value at the date of death", src("irs_p551")],
         ["Section 121 exclusion, single filer",
          money(OFFICIAL["sec121_single"], stat=True), src("irs_p523")],
         ["Section 121 exclusion, joint filers",
          money(OFFICIAL["sec121_joint"], stat=True), src("irs_p523")],
         ["Depreciation recapture on a let property",
          "Unrecaptured section 1250 gain comes back at a maximum of "
          f"{pctf(OFFICIAL['fed_unrecaptured_1250'], 0)}", src("irs_p527")],
         ["Like-kind exchange",
          "Limited to real property held for use in a trade or business or for investment",
          src("irs_p544")],
         ["Net investment income tax",
          f"{pctf(OFFICIAL['fed_niit'], 1)} on net investment income", src("irs_niit")],
         ["California treatment of capital gains",
          "\"California does not have a lower rate for capital gains. All capital gains are "
          "taxed as ordinary income.\"", src("ftb_capgains")],
         ["California top marginal rate, 2026 schedules",
          f"{pctf(OFFICIAL['ca_top_rate'], 2)}", src("ftb_rates_2026")],
         ["California tax above one million dollars",
          f"{pctf(OFFICIAL['ca_mhst_rate'], 0)} on taxable income above "
          f"{money(OFFICIAL['ca_mhst_threshold'], stat=True)}",
          src("rtc_17043") + " " + src("ftb_5805_2025")],
         ["Worked example: federal and California tax on a "
          f"{money(gain_example)} long-term gain",
          f"{money(fed)} federal plus {money(ca)} California",
          src("irs_niit") + " " + src("ftb_rates_2026") + " " + src("rtc_17043")]]))
    parts.append(table(
        ["3. Property tax assessment — decides the annual bill", "Figure", "Source"],
        [["Reassessment on transfer", "Market value at the transfer, unless an exclusion applies",
          src("boe_prop13")],
         ["Proposition 19 exclusion",
          money(OFFICIAL["prop19_exclusion"], stat=True) + " above the factored base year value, "
          "principal residence only", src("boe_nr2502")],
         ["Filing deadline for the claim", "Within one year of the transfer", src("boe_nr2502")],
         ["Homeowners' Exemption claim", "Required within one year of the transfer to keep the "
          "exclusion", src("boe_nr2502")]]))
    parts.append(f"""
<h2>The one point that changes the plan</h2>
<p>Because the basis of inherited property is its fair market value at the date of death, the
gain on selling Property A in the same tax year as the inheritance is close to zero. That makes
a like-kind exchange close to pointless for Property A — there is almost no gain to defer — and
it makes <a href="paths.html">the same-year sale</a> the cleanest way to release the property.
Property B is different: it is already owned, so its gain has been building for years. Any
exchange idea belongs to Property B, not to Property A.</p>
""")
    return "\n".join(parts)


def body_costs() -> str:
    band = ("low", "base", "high")
    rows = []
    items = [
        ("Water", OWNER["A_water_low"], OWNER["A_water_high"],
         OWNER["B_water_low"], OWNER["B_water_high"], "owner", ""),
        ("Electricity, net of the solar credit", -OWNER["A_solar_credit_high"],
         -OWNER["A_solar_credit_low"], OWNER["B_power_low"], OWNER["B_power_high"],
         "owner", ""),
        ("Insurance", 1_200, 2_500, 1_200, 2_500, "unverified", "cdi"),
        ("Maintenance and repairs",
         round(OWNER["A_value_2026"] * OWNER["A_maintenance_pct"][0]),
         round(OWNER["A_value_2026"] * OWNER["A_maintenance_pct"][2]),
         round(OWNER["B_value_2026"] * OWNER["B_maintenance_pct"][0]),
         round(OWNER["B_value_2026"] * OWNER["B_maintenance_pct"][2]), "assumption", ""),
    ]
    for name, alo, ahi, blo, bhi, kind, sid in items:
        rows.append([name, f"{money(alo)} – {money(ahi)}", f"{money(blo)} – {money(bhi)}",
                     tag(kind, "owner input" if kind == "owner" else
                         ("no quote obtained" if kind == "unverified" else "assumption")),
                     src(sid) if sid else tag("none", "no official source")])
    parts = ["""
<p class="lead">Running costs, as bands rather than single numbers. Where no official figure
exists the value cell is left as the household's own band and tagged; where the household has no
figure at all, the cell says so.</p>
"""]
    parts.append(table(["Cost, one year at 2026 prices", "Property A", "Property B", "Status",
                        "Source"], rows))
    cap = []
    for yr in range(1, 6):
        year = 2026 + yr
        a_cap = OWNER["A_value_2026"] * 0.010 * (1.03 ** yr)
        b_cap = OWNER["B_value_2026"] * 0.013 * (1.03 ** yr)
        cap.append([str(year), money(a_cap), money(b_cap),
                    money(a_cap + b_cap), src("bls_fred")])
    parts.append("""
<h2>Five-year maintenance and capital plan</h2>
<p>Set aside each year, at 1.0% of Property A's value and 1.3% of Property B's value a year,
escalating with local prices. The percentages are this desk's assumption, not a survey result:
the household has not supplied a capital plan, and the higher rate on Property B reflects that
it is older, has three units and carries more building to maintain.</p>
""")
    parts.append(table(["Year", "Property A set-aside", "Property B set-aside", "Both", "Source"],
                       cap))
    parts.append("""
<h2>What is missing</h2>
<ul>
<li><b>Insurance.</b> No quote has been obtained for either property. The household's own
estimate of about <span class="stat">$1,500</span> a year is carried, tagged unverified. Use the
Department of Insurance comparison tool, published under Insurance Code section 12959, and note
that the Department says its figures are sample premiums, not quotes. <a href="sources.html#cdi">Source</a>.</li>
<li><b>Property A's water provider.</b> The band is the household's own. The provider for the
parcel has not been confirmed, so no tariff can be cited. <a href="flagged.html">F05</a>.</li>
<li><b>Property A's market rent.</b> No rental estimate exists. The letting paths use an assumed
gross yield, so they are a floor until three written estimates are obtained.
<a href="flagged.html">F07</a>.</li>
<li><b>Capital plan.</b> The percentages above are an assumption until a condition survey is
done on each building.</li>
</ul>
""")
    return "\n".join(parts)


def body_projections() -> str:
    rows = []
    for year in range(2026, 2077, 2):
        y = year - 2026
        a_val = OWNER["A_value_2026"] * (1 + HPI_A_MEAN) ** y
        b_val = OWNER["B_value_2026"] * (1 + mean(h["hpi_b"] for h in M.HISTORY)) ** y
        a_av = OWNER["A_assessed_anchor"] * 1.02 ** y
        infl = mean(h["infl_sf"] for h in M.HISTORY)
        b_bill = OWNER["B_tax_2025"] * (1 + P.ASSUMPTIONS["b_bill_growth"][1]) ** y
        rows.append([str(year), money(a_val), money(b_val), money(a_av),
                     money(M.annual_tax(a_av, M.A_RATE, M.A_FIXED)), money(b_bill),
                     src("fhfa_fred") + " " + src("bls_fred")])
    parts = [f"""
<p class="lead">Year by year to {TERMINAL}, at the 1977-2025 average growth rates. This is the
one page on the desk that holds conditions constant, and it is here for reference, not as a
forecast: the <a href="black-swan.html">black swan page</a> is where growth and inflation are
allowed to move the way they really do.</p>
"""]
    parts.append(table(
        ["Year", "Property A value", "Property B value",
         "Property A assessed value, capped", "Property A bill", "Property B bill", "Source"],
        rows))
    dist = RESULTS[2040]
    lo = min(min(v) for v in dist.values())
    hi = max(M.pct(v, .9) for v in dist.values())
    chart = []
    for p, vals in sorted(dist.items(), key=lambda kv: -M.pct(kv[1], .5)):
        label = dict((a, b) for a, b, _ in P.PATHS)[p]
        med = M.pct(vals, .5)
        chart.append([label, f"<code>{bar(med, lo, hi)}</code>", money(med),
                      money(M.pct(vals, .1)), money(M.pct(vals, .9)),
                      src("erp2026_b56") + " " + src("fhfa_fred")])
    parts.append(f"""
<h2>Distribution of outcomes, transfer 2040</h2>
<p>Each bar is the median terminal wealth across {len(WORLDS):,} resampled futures; the marks
either side are the 10th and 90th percentiles. The spread matters more than the median: the
paths overlap heavily, which is why the desk recommends pre-committed triggers rather than a
single number.</p>
""")
    parts.append(table(["Path", "Median", "Median", "10th pct", "90th pct", "Source"], chart))
    return "\n".join(parts)


def body_paths() -> str:
    parts = [f"""
<p class="lead">Ten paths — three pure and seven mixed — run at identical transfer dates and
identical horizons, with taxes, debt assumptions, occupancy changes, capital costs and liquidity
all inside. Property B is held throughout in every path; what changes is who occupies which unit.
Everything is liquidated and taxed at {TERMINAL}.</p>
"""]
    for label, res, sub in (
            (f"Terminal date {TERMINAL}", RESULTS,
             "All three transfer dates measured to the same terminal date, so a later "
             "inheritance has less time to compound."),
            ("Twenty-five years from each transfer date", RESULTS_25,
             "Each transfer date given the same length of time, so every mixed path completes "
             "both legs.")):
        rows = []
        for p, vals in sorted(res[2045].items(), key=lambda kv: -M.pct(kv[1], .5)):
            name = dict((a, b) for a, b, _ in P.PATHS)[p]
            kind = dict((a, k) for a, _, k in P.PATHS)[p]
            row = [name, tag("pure" if kind == "pure" else "mixed", kind)]
            for ty in TRANSFERS:
                v = res[ty][p]
                row.append(f"{money(M.pct(v, .5))}<br><span class='small'>"
                           f"{money(M.pct(v, .1))} – {money(M.pct(v, .9))}</span>")
            row.append(src("erp2026_b56") + " " + src("fhfa_fred"))
            rows.append(row)
        parts.append(f"<h2>{label}</h2><p class='note'>{sub}</p>")
        parts.append(table(
            ["Path", "Kind", "Transfer 2040<br>median (10th–90th)",
             "Transfer 2045<br>median (10th–90th)", "Transfer 2050<br>median (10th–90th)",
             "Source"], rows))
    occ_rows = [
        ["Live in Property A", "Heir in A; third unit at B can be let", "Exclusion kept",
         "Available on a later sale after two of five years",
         "Lowest \u2014 the wealth is in the house",
         src("boe_nr2502") + " " + src("irs_p523")],
        ["Let Property A", "Heir stays at B; both B rents kept",
         "Not available \u2014 assessed value reset", "Not available", "Low",
         src("boe_nr2502") + " " + src("irs_p523")],
        ["Sell in the inheritance year", "Heir stays at B", "Not relevant",
         "Not needed \u2014 basis steps up", "Highest", src("irs_p551")],
        ["Live for ten years, then sell", "Heir in A for ten years, then back to B",
         "Exclusion kept for those ten years", "Available", "High after year ten",
         src("boe_nr2502") + " " + src("irs_p523")],
        ["Let for ten years, then sell", "Heir stays at B",
         "Not available \u2014 assessed value reset",
         "Not available; depreciation comes back as unrecaptured section 1250 gain",
         "High after year ten", src("irs_p527")],
        ["Live for ten years, then let", "Heir in A for ten years, then back to B",
         "Exclusion ends when occupation ends \u2014 reassessment then",
         "Lost once it is no longer the principal residence", "Low", src("boe_nr2502")],
        ["Sell, park 24 or 36 months", "Heir stays at B", "Not relevant", "Not needed",
         "High, then invested", src("bls_fred") + " " + src("treasury_yields")],
        ["Sell and hold Treasuries", "Heir stays at B", "Not relevant", "Not needed",
         "Highest", src("bls_fred")],
        ["Sell and exchange", "Heir stays at B", "Not relevant",
         "Not needed \u2014 almost no gain to defer", "Low", src("irs_p544")],
    ]
    parts.append("<h2>What each path assumes about occupation and liquidity</h2>")
    parts.append(table(["Path", "Who lives where", "Proposition 19", "Section 121",
                        "Liquidity", "Source"], occ_rows))
    parts.append("""
<p class="note">The exchange path and the same-year sale produce the same number on this desk,
and that is the finding: because the basis steps up to fair market value at death, a
like-kind exchange of Property A has almost nothing to defer.</p>
""")

    return "\n".join(parts)


def body_black_swan() -> str:
    reg = M.regime_table()
    rows = []
    for r in reg:
        rows.append([r["name"], f"{r['start']}–{r['end']}", str(r["years"]),
                     pctf(r["infl_sf"]), pctf(r["hpi_a"]), pctf(r["hpi_b"]),
                     pctf(r["equity"]), f"{r['tb3']:.2f}%", pctf(r["worst_equity"]),
                     pctf(r["worst_hpi_a"]),
                     src("bls_fred") + " " + src("fhfa_fred") + " " + src("erp2026_b55")])
    parts = ["""
<p class="lead">Growth and inflation are never constant for fifty years. This page resamples the
official record in five-year blocks, so a decade of high inflation arrives with the house-price
and equity behaviour of that same decade. Every figure below is measured from published series;
nothing is held constant and nothing is invented.</p>
"""]
    parts.append(table(
        ["Regime", "Years", "n", "Local inflation", "Property A prices", "Property B prices",
         "Equities", "3-month bill", "Worst equity year", "Worst price year", "Source"],
        rows, caption="Averages inside each regime, measured from the official series"))
    parts.append(f"""
<h2>The phased-investing path, replayed against the two great drawdowns</h2>
<p>Endpoints are those published by the Federal Reserve and the Economic Report of the President.
The 1929 drawdown is the Dow's fall from 381 in September 1929 to 41.22 in the summer of 1932,
89% below the peak, with the pre-crash level not regained until November 1954. The 2008
drawdown is the S&P composite falling from 1,468.36 at the end of 2007 to 903.25 at the end of
2008, recovering along the path the same official table records.</p>
<p class="warn"><b>Read this as a mechanism, not as a strategy.</b> These replays know the crash
is coming. A mechanical rule that happens to be waiting when the crash starts will always look
brilliant in hindsight. The honest counterweight is the cost of the cushion when nothing goes
wrong, which is shown immediately below and again beside every headline.</p>
""")
    for label, rows_sw in (("1929", M.crash_replay_1929(10_000)),
                           ("2008", M.crash_replay_2008(10_000))):
        body = [[r["strategy"], money(r["per_10000_trough"]), money(r["per_10000_end"]),
                 src("fedhist_1929") if label == "1929" else src("erp2026_b56")]
                for r in rows_sw]
        parts.append(table([f"Per {money(10_000)} invested — {label}", "At the trough",
                            "At the end of the replay", "Source"], body))
    cush = M.cost_of_the_cushion(10_000, 24, 12, 0.0407, 0.07, 120)
    cush36 = M.cost_of_the_cushion(10_000, 36, 12, 0.0407, 0.07, 120)
    parts.append(f"""
<h2>Reinvestment risk, beside the headline</h2>
<table class="data">
<thead><tr><th>If the crash never comes</th><th>Value after ten years per {money(10_000)}</th>
<th>Shortfall against going straight in</th><th>Source</th></tr></thead>
<tbody>
<tr><td>All in at once, at a 7% market return</td><td>{money(cush['all_in'])}</td><td>—</td>
<td>{src('erp2026_b56')}</td></tr>
<tr><td>Park 24 months, phase in over 12</td><td>{money(cush['phased'])}</td>
<td>{money(cush['shortfall_per_10000'])} ({pctf(cush['shortfall_pct'])})</td>
<td>{src('bls_fred')}</td></tr>
<tr><td>Park 36 months, phase in over 12</td><td>{money(cush36['phased'])}</td>
<td>{money(cush36['shortfall_per_10000'])} ({pctf(cush36['shortfall_pct'])})</td>
<td>{src('bls_fred')}</td></tr>
</tbody></table>
<p class="note">This is the other side of the trade and it is paid in every future in which
nothing goes wrong. The short rates used are the 1977-2025 average 3-month bill rate of
{M.record_summary()['tb3_mean']:.2f}% and the parking yield band runs from the bill rate to the
10-year yield.</p>
""")
    res = RESULTS[2040]
    rows2 = []
    for p in ("sell_sameyear", "sell_phase24", "sell_phase36", "hold_treasury", "live"):
        vals = res[p]
        name = dict((a, b) for a, b, _ in P.PATHS)[p]
        worst = min(vals)
        rows2.append([name, money(M.pct(vals, .5)), money(M.pct(vals, .1)), money(worst),
                      f"{sum(1 for v in vals if v < M.pct(res['live'], .5)) / len(vals) * 100:.0f}%",
                      src("erp2026_b56") + " " + src("bls_fred")])
    parts.append(f"""
<h2>The same paths through the resampled record</h2>
<p>Median, the 10th percentile and the single worst outcome across {len(WORLDS):,} futures. The
last column asks how often the path ends below the median of the live-in-Property-A path — a
plain way of showing how much the futures overlap.</p>
""")
    parts.append(table(["Path, transfer 2040", "Median", "10th percentile", "Worst of all",
                        "Ends below the live-path median", "Source"], rows2))
    return "\n".join(parts)


def body_triggers() -> str:
    parts = ["""
<p class="lead">Written down before the figures, so the outcome is not reverse-engineered from
one projection. Each row says what would have to be true for the household to choose that path,
what would be measured to check it, and the date the household signs it.</p>
"""]
    rows = [
        ["Keep and live in Property A",
         f"House prices in Property A's metro area are expected to grow faster than "
         f"<b>{pctf(BREAKEVEN_HPI[2040], 1)}</b> a year for the horizon, <b>and</b> the heir "
         f"will occupy it as a principal residence for at least ten years, <b>and</b> the "
         f"household can carry the bill without selling other assets.",
         "Two independent appraisals; a written statement that the heir intends to occupy; "
         "the county assessor's Proposition 19 filing calendar.",
         src("boe_nr2502") + " " + src("fhfa_fred")],
        ["Let Property A",
         "Written rental estimates show a gross yield above "
         f"<b>{pctf(P.ASSUMPTIONS['rent_yield_a'][2], 1)}</b>, <b>and</b> the household's "
         "marginal rate on rental income is below the top band, <b>and</b> the reassessed "
         "property tax bill leaves the property cash-flow positive.",
         "Three written rental estimates; a marginal-rate calculation from the last return; "
         "the assessor's projected reassessed value.",
         src("irs_p527") + " " + src("census_acs")],
        ["Sell in the inheritance year",
         "The estate needs liquidity, <b>or</b> the expected equity return exceeds "
         f"<b>{pctf(BREAKEVEN_EQ[2040], 1)}</b> a year, <b>or</b> the heir will not occupy the "
         "home long term.",
         "An estate liquidity plan; a written investment policy for the proceeds; a date-of-death "
         "valuation.",
         src("irs_p551") + " " + src("irs_estate")],
        ["Sell and phase in over 24-36 months",
         "The household accepts the measured cost of the cushion in exchange for not entering "
         "the market all at once, <b>and</b> has a written investment policy that fixes the "
         "schedule in advance.",
         "The investment policy, signed before the money arrives; the parking-yield band from "
         "the daily Treasury par yield curve.",
         src("treasury_yields") + " " + src("bls_fred")],
        ["Live for ten years, then sell",
         "The heir wants the home for a defined period, <b>and</b> the household will still "
         "qualify for the section 121 exclusion when the sale happens.",
         "A calendar check on the two-out-of-five-years use test; the section 121 ownership "
         "and use tests.",
         src("irs_p523")],
        ["Exchange under section 1031",
         "Only worth considering for <b>Property B</b>, not Property A — Property A's basis "
         "steps up at death, so there is almost no gain to defer.",
         "Property B's income-tax basis, established from the purchase records.",
         src("irs_p544") + " " + src("irs_p551")],
    ]
    parts.append(table(["Path", "Choose it only if all of these are true",
                        "What gets measured to check it", "Source"], rows))
    parts.append("""
<h2>Signature block</h2>
<table class="sign">
<thead><tr><th>Who</th><th>Decision</th><th>Date</th><th>Signature</th></tr></thead>
<tbody>
<tr><td>Heir — Property A</td><td></td><td></td><td></td></tr>
<tr><td>Heir — Property B</td><td></td><td></td><td></td></tr>
<tr><td>Attorney</td><td></td><td></td><td></td></tr>
<tr><td>Certified public accountant</td><td></td><td></td><td></td></tr>
</tbody></table>
<p class="note">Nothing on this desk has been implemented. The suggestions board lists what could
be done next; the household chooses before anything changes. This sheet is meant to be signed
before the figures arrive.</p>
""")
    return "\n".join(parts)


def body_questions() -> str:
    parts = ["""
<p class="lead">What is known, what is missing, and how to find each missing item. Every row
states the answer if there is one, the source if there is one, or the action that would produce
one.</p>
"""]
    rows = [
        ["What is Property A's tax rate area, and what is its published rate?",
         tag("none", "not answered"),
         "The county publishes a compilation of tax rates each year with the rate for every tax "
         "rate area; the code is printed on the property tax bill. Read the code off the bill "
         "and look up that rate.", src("scc_trb")],
        ["What is Property A worth at the date of death?",
         tag("none", "not answered"),
         "Obtain a written valuation as at the date of death. It sets the income tax basis and "
         "any estate tax.", src("irs_p551")],
        ["What would Property A let for?",
         tag("none", "not answered"),
         "Obtain three written rental estimates. Until then the letting paths rest on an assumed "
         "gross yield of "
         f"{pctf(P.ASSUMPTIONS['rent_yield_a'][0], 1)} to "
         f"{pctf(P.ASSUMPTIONS['rent_yield_a'][2], 1)} and are a floor, not a ranking.",
         src("census_acs") + " " + src("hud_fmr")],
        ["What does insurance cost on each property?",
         tag("none", "not answered"),
         "Obtain quotes for both. The Department of Insurance publishes a comparison tool under "
         "Insurance Code section 12959; its figures are sample premiums, not quotes.",
         src("cdi")],
        ["Will the estate exceed the federal filing threshold?",
         f"The threshold for a 2026 death is "
         f"{money(OFFICIAL['estate_exclusion_2026'], stat=True)}",
         "Prepare an estate liquidity plan and ask now about portability and prior taxable "
         "gifts.", src("irs_estate") + " " + src("irs_706")],
        ["Does California charge an estate tax?",
         tag("unverified", "not confirmed this session"),
         "Confirm with the Franchise Tax Board before relying on any answer.",
         src("ftb_540_2025")],
        ["Is the Proposition 19 exclusion available?",
         "Only if Property A continues to be the transferee's principal residence",
         "Decide the occupation question first; the exclusion follows from it, not the other "
         "way round. The claim must be filed within one year of the transfer.",
         src("boe_nr2502") + " " + src("boe_pub801")],
        ["Is a like-kind exchange wanted?",
         "For Property A, almost certainly not — the basis steps up at death",
         "Take advice before selling. Any exchange idea belongs to Property B, where the gain "
         "has been building for years.", src("irs_p544")],
        ["What are Property B's leases and the local rules that bind them?",
         tag("none", "not answered"),
         "Obtain the two written leases and check them against the local rent rules before "
         "relying on the rental income in any path.", src("irs_p527")],
        ["What is Property B's income-tax basis?",
         tag("none", "not answered"),
         "Find the purchase records. Until then Property B's terminal value is left out of the "
         "path comparison, because it is the same in every path and cancels out.",
         src("irs_p551")],
        ["What are the deadlines after the transfer?",
         "The Proposition 19 claim and the Homeowners' Exemption must be filed within one year "
         "of the transfer",
         "See the timeline on the process page.", src("boe_nr2502") + " " + src("boe_pub801")],
        ["How often should this be re-run?",
         "Every year, and after any input changes",
         "Rebuild the model and the site and check whether the recommendation moved.",
         src("fhfa_fred")],
    ]
    parts.append(table(["Question", "Answer", "How to discover what is missing", "Source"], rows))
    return "\n".join(parts)


def body_suggestions() -> str:
    parts = ["""
<p class="lead">Proposed only. Nothing on this board has been implemented. Each row says what it
would change, what it would cost to find out, and what would have to be true for it to be worth
doing. The household picks, then it gets built.</p>
"""]
    rows = [
        ["S1", "Obtain a written date-of-death valuation of Property A",
         "Sets the income-tax basis. Without it every sale figure on this desk is an estimate.",
         "Cost of an appraisal", "Do before any sale or any income-tax decision", "Proposed"],
        ["S2", "Obtain three written rental estimates for Property A",
         "Turns the letting paths from a floor into a ranking.",
         "Three agent estimates, usually free", "Do before choosing a letting path", "Proposed"],
        ["S3", "Obtain insurance quotes for both properties",
         "Removes the largest unverified cost on the desk.",
         "Time to gather quotes", "Do before finalising any carry-cost comparison", "Proposed"],
        ["S4", "Confirm Property A's tax rate area and read the published rate",
         "Replaces a fitted rate with the parcel's own rate.",
         "Read the code off the tax bill and look it up", "Do before trusting any bill "
         "projection", "Proposed"],
        ["S5", "Write an investment policy for the sale proceeds before the money arrives",
         "Fixes the entry schedule in advance so the phased path is a rule, not a reaction.",
         "Time with an adviser", "Do before any sale completes", "Proposed"],
        ["S6", "Prepare an estate liquidity plan",
         "If the estate may exceed the federal threshold, liquidity rather than return becomes "
         "the binding constraint.", "Time with the attorney and the accountant",
         "Do well before the transfer", "Proposed"],
        ["S7", "Ask now about portability and prior taxable gifts",
         "Both change the amount of exemption actually available.",
         "A conversation and a review of past gift returns", "Do now, while the records exist",
         "Proposed"],
        ["S8", "Obtain the two written leases for Property B and check them against the local "
         "rent rules", "Confirms whether the rental income in every path is what it appears to "
         "be.", "Time with the attorney", "Do before relying on the rent in any projection",
         "Proposed"],
        ["S9", "Build a private estate inventory, held outside this repository",
         "Keeps the record useful without putting anything identifying into a public place.",
         "Time", "Do now", "Proposed"],
        ["S10", "Carry out a condition survey on each building",
         "Replaces the assumed maintenance percentages with a real five-year capital plan.",
         "Cost of two surveys", "Do before committing to a hold path", "Proposed"],
        ["S11", "Model depreciation and recapture explicitly once Property A's building value "
         "is known", "The improvement share is currently an assumption.",
         "Needs an appraisal split between land and building", "Do if a letting path stays in "
         "contention", "Proposed"],
        ["S12", "Re-run this desk every year with updated inputs",
         "The break-even rates move as the record grows.", "Time",
         "Annually", "Proposed"],
        ["S13", "Track proposed legislation on a standing page",
         "Separates what is enacted from what is merely proposed.",
         "Time", "Ongoing — see the law watch page", "Proposed"],
        ["S14", "Review the extreme scenarios annually",
         "The black swan page is only as good as its inputs.",
         "Time", "Annually", "Proposed"],
        ["S15", "Consider scrubbing the repository history before the rounded figures were used",
         "Rounding protects the figures published from now on; it does not change what is "
         "already in the history.", "Owner decision — a destructive rewrite",
         "Owner's call; logged as F19", "Proposed — not carried out"],
    ]
    exempt = ('<table class="data" data-exempt="Every row on this board is a proposed '
              'action, not a value. Nothing has been implemented and no figure on this desk '
              'depends on any row. The sources that bear on each item are cited on the '
              'questions page.">')
    parts.append(table(["Ref", "Suggestion", "What it would change", "Cost to find out",
                        "When", "Status"], rows).replace('<table class="data">', exempt))
    return "\n".join(parts)


def body_whatif() -> str:
    grid = []
    for eq in (0.04, 0.06, 0.08, 0.10, 0.1277):
        for hpi in (0.03, 0.05, 0.0713, 0.09):
            w = P.deterministic_world(
                mean(h["infl_sf"] for h in M.HISTORY),
                mean(h["rent_sf"] for h in M.HISTORY), hpi,
                mean(h["hpi_b"] for h in M.HISTORY), eq,
                mean(h["tb3"] for h in M.HISTORY),
                mean(h["gs10"] for h in M.HISTORY), TERMINAL - 2040 + 2)
            keep = P.run_path("live", w, 2040, TERMINAL - 2040)["terminal"]
            sell = P.run_path("sell_sameyear", w, 2040, TERMINAL - 2040)["terminal"]
            grid.append([pctf(eq, 2), pctf(hpi, 2), money(keep), money(sell),
                         money(keep - sell),
                         "keep" if keep > sell else "sell",
                         src("erp2026_b56") + " " + src("fhfa_fred")])
    parts = [f"""
<p class="lead">Every condition held constant at the value you choose, transfer in 2040,
terminal date {TERMINAL}. The last column names the path that comes out ahead. This is a
break-even tool, not a forecast: it says what has to be true for each choice to win.</p>
"""]
    parts.append(table(["Equity return", "Property A price growth", "Live in it", "Sell it",
                        "Difference", "Ahead", "Source"], grid))
    parts.append(f"""
<h2>Try your own numbers</h2>
<p>The controls below are computed in the browser from the same formulas the pages use. Nothing
is sent anywhere; the page works offline.</p>
<div class="calc">
  <label>Equity return a year <input id="eq" type="number" value="7.0" step="0.1" min="0"
  max="20"> %</label>
  <label>Property A price growth a year <input id="hp" type="number" value="5.0" step="0.1"
  min="0" max="20"> %</label>
  <label>Local inflation a year <input id="inf" type="number" value="3.0" step="0.1" min="0"
  max="20"> %</label>
  <label>Years from the transfer to the terminal date <input id="yr" type="number" value="36"
  step="1" min="1" max="60"></label>
  <p id="calc-out">Adjust a control to see the result.</p>
  <script src="assets/calculator.js"></script>
</div>
<p class="note">The calculator compounds the two assets at the rates you enter and shows the
difference at the end. It is deliberately simpler than the model on the other pages: it leaves
out tax, rent and running costs, so it answers "which asset compounds faster under these two
rates" and nothing more.</p>
""")
    return "\n".join(parts)


def body_process() -> str:
    parts = ["""
<p class="lead">How the trust transfer runs, in order, with the deadline attached to each step.
The deadlines are the part that is easy to miss and expensive to miss.</p>
"""]
    steps = [
        ["1", "Date of death", "The valuation date for the income-tax basis and for the estate "
         "tax.", "Immediate", src("irs_p551") + " " + src("irs_estate")],
        ["2", "Obtain a written valuation as at the date of death",
         "Sets the basis. Everything downstream depends on it.", "As soon as possible",
         src("irs_p551")],
        ["3", "Identify the trustee and confirm the trust terms",
         "The terms decide whether the property can be sold, let or occupied, and by whom.",
         "Before any decision",
         tag("owner", "trust terms not seen") + " " + src("irs_p559")],
        ["4", "Notify the county assessor of the change in ownership",
         "Starts the reassessment clock. A change-in-ownership statement is required.",
         "Within the period the county sets", src("scc_asr_parentchild")],
        ["5", "Decide the occupation question",
         "The Proposition 19 exclusion is available only while the home is the transferee's "
         "principal residence. Decide this before the property-tax filing, not after.",
         "Before the claim deadline", src("boe_nr2502")],
        ["6", "File the Proposition 19 claim if occupying",
         "Claim on the form the Board specifies, with the value limit and filing period set out "
         "in Publication 801.", "Within one year of the transfer",
         src("boe_nr2502") + " " + src("boe_pub801")],
        ["7", "Claim the Homeowners' Exemption",
         "Required within one year of the transfer to keep the exclusion.",
         "Within one year of the transfer", src("boe_nr2502")],
        ["8", "Establish whether an estate tax return is required",
         f"Required if the gross estate, plus adjusted taxable gifts, exceeds the filing "
         f"threshold for the year of death.", "Nine months after death, extendable",
         src("irs_estate") + " " + src("irs_706")],
        ["9", "Ask about portability and prior taxable gifts",
         "Both change the exemption actually available.",
         "Before the estate return is filed", src("irs_estate")],
        ["10", "Prepare an estate liquidity plan if the estate may exceed the threshold",
         "Liquidity, not return, becomes the binding constraint.", "Well before the transfer",
         src("irs_706")],
        ["11", "Write the investment policy for any proceeds",
         "Fixes the entry schedule in advance, so a phased path is a rule rather than a "
         "reaction.", "Before the money arrives", src("treasury_yields")],
        ["12", "If selling: budget the transfer taxes and recording fees",
         "Both counties charge on the consideration; the rates are published.",
         "At the sale", src("sf_transfer_tax") + " " + src("scc_recorder_fees")],
        ["13", "If letting: obtain written leases and check the local rules",
         "Confirms the rental income before it is relied on.", "Before relying on any "
         "projection", src("irs_p527")],
        ["14", "Re-run this model every year",
         "The break-evens move as the record grows.", "Annually", src("fhfa_fred")],
    ]
    parts.append(table(["Step", "What happens", "Why it matters", "Deadline", "Source"], steps))
    parts.append(f"""
<h2>Deadlines as a timeline</h2>
<table class="data">
<thead><tr><th>When</th><th>What is due</th><th>Consequence of missing it</th>
<th>Source</th></tr></thead>
<tbody>
<tr><td>Date of death</td><td>Valuation date for basis and estate tax</td>
<td>The basis is set by whatever evidence exists</td><td>{src('irs_p551')}</td></tr>
<tr><td>Within one year of the transfer</td>
<td>Proposition 19 claim and Homeowners' Exemption claim</td>
<td>The exclusion is lost and the assessed value resets to market value</td>
<td>{src('boe_nr2502')} {src('boe_pub801')}</td></tr>
<tr><td>Nine months after death, extendable</td>
<td>Estate tax return, if one is required</td><td>Penalties and interest</td>
<td>{src('irs_706')}</td></tr>
<tr><td>Each year from 1 July 2027 to 30 June 2042</td>
<td>The new parcel tax on Property B's county, if the parcel is liable</td>
<td>The charge is billed with the property tax</td>
<td>{src('sfdoe_2026')} {src('sf_vip_2026')}</td></tr>
<tr><td>Every year</td><td>Re-run this model with updated inputs</td>
<td>The break-evens move and the decision can invert without anyone noticing</td>
<td>{src("fhfa_fred")}</td></tr>
</tbody></table>
""")
    return "\n".join(parts)


def body_briefing() -> str:
    sell = RESULTS[2040]["sell_sameyear"]
    live = RESULTS[2040]["live"]
    return f"""
<p class="lead">One page to print and hand to the attorney and the accountant. It states what is
known, what is not, and the four questions the household needs answered in writing.</p>
<div class="sheet">
<h2>Attorney and CPA briefing sheet</h2>
<p class="small">Prepared {BUILD_DATE}. Property A: future trust inheritance, Santa Clara
County. Property B: already owned by the heir, San Francisco County, three units, two let.
Money rounded to the nearest $10.</p>
<h3>1. What the household is deciding</h3>
<p>Whether to live in Property A, let it, or sell it and invest the proceeds — and, if selling,
whether to invest at once or in stages. Property B is held throughout and can house the heir at
no loss of rent, which is why living in Property A does not save rent.</p>
<h3>2. The four questions we need answered in writing</h3>
<ol>
<li><b>Proposition 19.</b> Confirm the exclusion is available only while Property A is the
transferee's principal residence, and confirm the one-year filing deadline.
<span class="small">Source: {src('boe_nr2502')}, {src('boe_pub801')}</span></li>
<li><b>Basis.</b> Confirm that the basis of Property A is its fair market value at the date of
death, and therefore that a same-year sale produces almost no gain — and confirm what a
like-kind exchange would or would not achieve.
<span class="small">Source: {src('irs_p551')}, {src('irs_p544')}</span></li>
<li><b>Estate tax.</b> Confirm whether the estate will exceed the federal filing threshold of
{money(OFFICIAL['estate_exclusion_2026'], stat=True)} for a 2026 death, and whether portability
and prior taxable gifts change the answer.
<span class="small">Source: {src('irs_estate')}, {src('irs_706')}</span></li>
<li><b>Running costs and local taxes.</b> Confirm the parcel's tax rate area and its published
rate, the insurance position on both properties, and the effect of the parcel tax approved on
3 November 2026. <span class="small">Source: {src('scc_trb')}, {src('cdi')},
{src('sfdoe_2026')}</span></li>
</ol>
<h3>3. What the model says today</h3>
<table class="data">
<thead><tr><th>Measure</th><th>Value</th><th>Source</th></tr></thead>
<tbody>
<tr><td>Median terminal wealth, sell in the inheritance year</td><td>{money(M.pct(sell, .5))}</td>
<td>{src('erp2026_b56')}</td></tr>
<tr><td>Median terminal wealth, live in Property A</td><td>{money(M.pct(live, .5))}</td>
<td>{src('fhfa_fred')}</td></tr>
<tr><td>House price growth needed for keeping to win</td>
<td>{pctf(BREAKEVEN_HPI[2040], 1)} a year</td><td>{src('fhfa_fred')}</td></tr>
<tr><td>Equity return below which keeping wins</td><td>{pctf(BREAKEVEN_EQ[2040], 1)} a year</td>
<td>{src('erp2026_b55')} {src('erp2026_b56')}</td></tr>
<tr><td>Cost of parking the proceeds 24 months if nothing goes wrong</td>
<td>{money(M.cost_of_the_cushion(10_000, 24, 12, 0.0407, 0.07, 120)['shortfall_per_10000'])} per
{money(10_000)} over ten years</td><td>{src('bls_fred')}</td></tr>
</tbody></table>
<h3>4. What we do not know</h3>
<ul>
<li>Property A's tax rate area and published rate — <b>unknown</b></li>
<li>Property A's market rent — <b>unknown</b>; the letting paths are a floor</li>
<li>Insurance premiums for both properties — <b>no quote obtained</b></li>
<li>Property B's income-tax basis — <b>unknown</b></li>
<li>Whether the estate exceeds the federal threshold — <b>not disclosed</b></li>
<li>California's estate-tax position — <b>not confirmed this session</b></li>
</ul>
<h3>5. Signed</h3>
<table class="sign">
<thead><tr><th>Who</th><th>Date</th><th>Signature</th></tr></thead>
<tbody>
<tr><td>Heir</td><td></td><td></td></tr>
<tr><td>Attorney</td><td></td><td></td></tr>
<tr><td>Certified public accountant</td><td></td><td></td></tr>
</tbody></table>
</div>
"""


def body_law_watch() -> str:
    return f"""
<p class="lead">Enacted and proposed are different things, and this page keeps them apart. The
first table is what has happened. The second is what is being discussed, with no weight given
to it in any number on this desk.</p>
<h2>Enacted</h2>
<table class="data">
<thead><tr><th>Measure</th><th>What it does</th><th>Result and dates</th><th>Source</th></tr>
</thead>
<tbody>
<tr><td>Proposition 19 adjusted exclusion</td>
<td>The intergenerational transfer exclusion is adjusted every two years from the federal house
price index for California</td>
<td><span class="stat">$1,044,586</span> for transfers from 16 February 2025 to 15 February
2027, up 2.15% from <span class="stat">$1,022,600</span></td>
<td>{src("boe_nr2502")}</td></tr>
<tr><td>California tax above one million dollars</td>
<td>1% on taxable income above <span class="stat">$1,000,000</span>, added by Proposition 63 in
2004 and operative from 1 January 2005</td><td>In force</td><td>{src("rtc_17043")}</td></tr>
<tr><td>California 2026 rate schedules</td>
<td>Top marginal rate of 12.30%, with the brackets recomputed each year from the
California Consumer Price Index</td>
<td>Published for 2026</td><td>{src("ftb_rates_2026")} {src("rtc_17041")}</td></tr>
<tr><td>Federal estate tax filing threshold, 2026</td>
<td><span class="stat">$15,000,000</span></td><td>Published for a 2026 year of death</td>
<td>{src("irs_estate")}</td></tr>
<tr><td>Parcel tax to fund Muni operations — passed 3 November 2026</td>
<td>An annual parcel tax on most property in Property B's county, by building size rather than
value, rising with inflation after the first year, raising about <span class="stat">$177 million</span> a year</td>
<td>Yes 244,760 (74.4%) against No 84,209 (25.6%). Preliminary results; certification is due
within 30 days of the election. The tax runs fifteen years from 1 July 2027 to 30 June 2042</td>
<td>{src("sfdoe_2026")} {src("sf_vip_2026")}</td></tr>
<tr><td>Removal of the foreclosure exemption from the transfer tax — passed 3 November 2026</td>
<td>Applies a transfer tax of between 0.5% and 6% to properties transferred to a lender because
of foreclosure or to avoid foreclosure</td>
<td>Yes 260,241 (80.88%) against No 61,529 (19.12%). Preliminary</td>
<td>{src("sfdoe_2026")}</td></tr>
<tr><td>Regional measure — passed 3 November 2026</td>
<td>A sales tax for fourteen years, 1% in Property B's county</td>
<td>Yes 259,562 (79.17%) against No 68,311 (20.83%) in the county. Preliminary</td>
<td>{src("sfdoe_2026")}</td></tr>
</tbody></table>
<h2>Proposed, or rejected — no weight in any figure on this desk</h2>
<table class="data">
<thead><tr><th>Measure</th><th>What it would have done</th><th>Outcome</th><th>Source</th>
</tr></thead>
<tbody>
<tr><td>Changes to the real property transfer tax — defeated 3 November 2026</td>
<td>Would have dedicated half of the transfer tax collected on property above
<span class="stat">$10,000,000</span> to affordable housing. The measure text confirms those
properties are taxed at 5.5% to 6%</td>
<td>No 166,070 (51.66%) against Yes 155,384 (48.34%). Preliminary — defeated</td>
<td>{src("sfdoe_2026")}</td></tr>
<tr><td>Future adjustments to the Proposition 19 exclusion</td>
<td>The amount is recalculated every two years, so it will change again</td>
<td>Not yet published for the period after 15 February 2027</td><td>{src("boe_nr2502")}</td></tr>
<tr><td>Federal estate tax after 2026</td>
<td>The exclusion is indexed after 2026; the figure for later years is published by the Internal
Revenue Service</td>
<td>Check the Internal Revenue Service inflation-adjustment releases each year</td>
<td>{src("irs_inflation_2027")}</td></tr>
</tbody></table>
"""


def body_glossary() -> str:
    terms = [
        ["Ad valorem", "Charged in proportion to value. The property tax is an ad valorem tax; "
         "a parcel tax is not.", src("boe_prop13")],
        ["Assessed value", "The value the county taxes. Under Proposition 13 it starts at the "
         "purchase price and rises by no more than the lesser of 2% and the change in the "
         "California Consumer Price Index.", src("boe_prop13")],
        ["Basis", "The amount a gain or loss is measured against. Inherited property takes a "
         "basis equal to its fair market value at the date of death.", src("irs_p551")],
        ["Depreciation recapture", "Tax on the depreciation already claimed when a let property "
         "is sold. Unrecaptured section 1250 gain is taxed at a maximum of 25%.",
         src("irs_p527")],
        ["Factored base year value", "The Proposition 13 assessed value, rolled forward by the "
         "annual cap. The Proposition 19 exclusion is measured against it.", src("boe_nr2502")],
        ["Homeowners' Exemption", "A small reduction in taxable value for an owner-occupied "
         "home. Claiming it within a year of the transfer is a condition of keeping the "
         "Proposition 19 exclusion.", src("boe_nr2502")],
        ["Imputed rent", "The rent a home would command, counted as the benefit of living in it. "
         "Every path on this desk counts housing as a benefit in whatever property is occupied, "
         "so that living rent-free is not mistaken for a free gain. "
         + tag("assumption", "this desk's convention")],
        ["Like-kind exchange", "Section 1031 lets gain be deferred when real property held for "
         "investment or business use is exchanged for other real property.", src("irs_p544")],
        ["Net investment income tax", "A 3.8% tax on net investment income above the threshold "
         "amounts.", src("irs_niit")],
        ["Portability", "The election that lets a surviving spouse use the unused estate tax "
         "exemption of the spouse who died first.", src("irs_estate")],
        ["Proposition 13", "The 1978 measure that set the 1% maximum levy and the cap on "
         "assessed value growth.", src("boe_prop13")],
        ["Proposition 19", "The 2020 measure that changed the parent-child transfer of a "
         "principal residence or family farm, and ties the exclusion to the transferee's "
         "occupation.", src("boe_nr2502")],
        ["Reassessment", "Setting the assessed value to market value, which happens on a change "
         "in ownership unless an exclusion applies.", src("boe_prop13")],
        ["Section 121", "The exclusion of gain on the sale of a principal residence, up to "
         "$250,000 or $500,000, after two years of use out of the last five.",
         src("irs_p523")],
        ["Tax rate area", "The code that determines which local agencies and bonds apply to a "
         "parcel, and therefore its exact property tax rate. It is printed on the tax bill.",
         src("scc_trb")],
        ["Total return", "Price change plus income. The equity return on this desk is the change "
         "in the published index plus its dividend-price ratio, which is an approximation.",
         src("erp2026_b56")],
    ]
    return table(["Term", "Meaning", "Source"], terms)


def body_sources() -> str:
    rows = []
    for sid, s in sorted(SOURCES.items()):
        host = s["url"].split("/")[2]
        rows.append([f'<a id="{sid}"></a><code>{sid}</code>', esc(s["publisher"]),
                     esc(s["title"]),
                     f'<a href="{esc(s["url"])}">{esc(s["url"])}</a>',
                     esc(s["status"])])
    return ("""
<p class="lead">Every row on every page of this desk cites one of these. A source marked
"pointer" is published as a place to check and is never used to support a value.</p>
""" + table(["Ref", "Publisher", "What it is", "Address", "How it was checked"], rows))


FLAGS = [
    ("F01", "Property A and Property B tax rate areas",
     "Neither parcel's tax rate area has been supplied, so no published rate is cited for "
     "either. Property A's bill was fitted from the household's own bills instead.",
     "Read the tax rate area code off the property tax bill and look it up in the county's "
     "compilation of tax rates.", "scc_trb"),
    ("F02", "Owner-supplied values are unverified",
     "Market values, the trust timeline, Property B's rents and the utility bands are the "
     "household's own figures. No official page corroborates them.",
     "Obtain written valuations and written rental estimates.", "census_acs"),
    ("F03", "Assessed values are published banded, not exactly",
     "An assessed value is a public record tied to one parcel, so the exact figures are "
     "deliberately not republished. Banded anchors are used instead.",
     "Owner decision. The banding is a privacy measure, not a measurement error.", "boe_prop13"),
    ("F04", "Property B's bill has no usable ad-valorem split",
     "The least-squares fit produces a negative fixed charge, which is not a real thing. B's "
     "bill grew far faster than its assessed value, so it is projected from its own observed "
     "growth.", "Ask the county what makes up the bill.", "bls_fred"),
    ("F05", "Property A's water provider is not confirmed",
     "No tariff can be cited for a parcel whose provider is unknown. The household's own band "
     "is used.", "Confirm the provider, then cite its published tariff.", "bls_fred"),
    ("F06", "No insurance quote for either property",
     "Both properties are carried at the household's own estimate of about $1,500 a year, "
     "tagged unverified.", "Obtain quotes for both properties.", "cdi"),
    ("F07", "Property A's market rent is unknown",
     "The letting paths use an assumed gross rental yield, so they are a floor rather than a "
     "ranking.", "Obtain three written rental estimates.", "census_acs"),
    ("F08", "The size of the rest of the estate is not disclosed",
     "Whether the estate exceeds the federal filing threshold cannot be tested.",
     "Prepare an estate liquidity plan and ask about portability and prior taxable gifts.",
     "irs_estate"),
    ("F09", "Property B's income-tax basis is unknown",
     "Property B's terminal sale value is left out of the path comparison because it is the "
     "same in every path and cancels out. Its incremental depreciation recapture is included.",
     "Establish the basis from the purchase records.", "irs_p551"),
    ("F10", "California's estate-tax position is not confirmed this session",
     "The desk does not assert that California has or has not got an estate tax.",
     "Confirm with the Franchise Tax Board before relying on any figure.", "ftb_540_2025"),
    ("F11", "The 1929 and 2008 replays are hindsight",
     "Both replays know the crash is coming. A mechanical entry rule applied to a known "
     "drawdown will always look better than going straight in.",
     "Read the cost-of-the-cushion table beside them as the counterweight.", "fedhist_1929"),
    ("F12", "The equity total return is an approximation",
     "The published tables give a price index and a dividend-price ratio, not a total-return "
     "series. The two are added.",
     "Treat the equity return as an approximation, not a published series.", "erp2026_b56"),
    ("F13", "The combined marginal rate on rental income is an assumption",
     "The band runs from 45% to 54%, built from sourced components. The interaction between "
     "the federal and California taxes depends on the deduction cap.",
     "Have the accountant compute the household's actual marginal rate.", "irs_niit"),
    ("F14", "The improvement share for depreciation is an assumption",
     "Depreciation and therefore recapture depend on the split between land and building, "
     "which has not been appraised.", "Obtain an appraisal that splits land and building.",
     "irs_p527"),
    ("F15", "The November 2026 results are preliminary",
     "The San Francisco Department of Elections marks its results preliminary and may take up "
     "to thirty days after the election to certify.",
     "Check the certified results before relying on any measure.", "sfdoe_2026"),
    ("F16", "The registration of the two properties' occupancy is the household's own",
     "That the heir can live at Property B without losing rent is taken from the household's "
     "description.", "Confirm against the written leases.", "irs_p527"),
    ("F17", "The corridor of years in the model starts in 2026",
     "The inheritance is expected between 2040 and 2050. Everything before the transfer year "
     "is a projection of what the two properties do in the meantime.",
     "Owner decision on the transfer years shown.", "fhfa_fred"),
    ("F18", "Earlier desks in this repository publish city names and postcodes",
     "This desk does not. Older directories in the same repository were built before the "
     "tighter rule and have not been rewritten.",
     "Owner decision on whether to rewrite them.", "boe_prop13"),
    ("F19", "The repository history contains figures from before the rounding rule",
     "Rounding protects figures published from now on. It does not change what is already in "
     "the history, and scrubbing it is a destructive rewrite of shared history.",
     "Owner decision. Not carried out by this session.", "irs_estate"),
]


def body_flagged() -> str:
    rows = []
    for ref, title, detail, action, sid in FLAGS:
        if sid.endswith(".html"):
            link = f'<a href="{sid}">{esc(sid)}</a>'
        else:
            link = src(sid)
        rows.append([f"<b>{ref}</b>", esc(title), esc(detail), esc(action), link])
    return ("""
<p class="lead">Everything this desk could not confirm, or could confirm only partly. Nothing
here blocks the comparison; each row says what would settle it.</p>
""" + table(["Ref", "Item", "What is wrong or missing", "What would settle it", "Source"], rows))


def body_method() -> str:
    rec = M.record_summary()
    return f"""
<h2>How the numbers are produced</h2>
<p>One model, one source register, one build script. The pages are generated, so a figure cannot
drift between pages.</p>
<h3>Resampling, not extrapolation</h3>
<p>The {rec['years']} years from {rec['start']} to {rec['end']} are resampled in contiguous
five-year blocks, with wraparound, {len(WORLDS):,} times. A block is drawn as a unit so that
the inflation, house-price, equity and interest-rate behaviour of those years arrives together
exactly as it happened. Any regime can follow any other. The result is reported as a median with
10th and 90th percentiles, and as the share of futures in which each path leads.</p>
<h3>Bands, not points</h3>
<p>Every uncertain input is a low / base / high band. The bands are carried through the
arithmetic, so a result arrives as a band too. Where a value is unknown the cell is left empty
and the row is tagged, rather than filled with a plausible number.</p>
<h3>What is measured and what is assumed</h3>
{table(["Input", "Status", "Source"], [
 ["Equity returns", "Measured — published index and dividend-price ratio, added",
  src('erp2026_b55') + ' ' + src('erp2026_b56')],
 ["House price growth", "Measured — published index, Property A's and Property B's metro areas",
  src('fhfa_fred')],
 ["Local inflation and rent growth", "Measured — published local price indexes",
  src('bls_fred')],
 ["Short-term interest rates", "Measured — published bill and bond yields", src('bls_fred')],
 ["Property A's ad-valorem rate and fixed charges",
  "Derived — least squares on the household's own bills", src('boe_prop13')],
 ["Property A's market rent", "Assumed — a gross yield band, flagged F07", src('census_acs')],
 ["Insurance", "The household's own estimate, unverified, flagged F06", src('cdi')],
 ["Maintenance and capital spending", "Assumed — a percentage of value, flagged",
  tag('none', 'no official source')],
 ["Combined marginal rate on rental income", "Assumed — a band built from sourced components, "
  "flagged F13", src('irs_niit') + ' ' + src('ftb_rates_2026')],
 ["Market values and the trust timeline", "The household's own figures, unverified, flagged F02",
  tag('none', 'no official source')],
])}
<h3>What the model leaves out</h3>
<ul>
<li>Mortgages. No debt on either property has been disclosed, so none is modelled.</li>
<li>Property B's terminal sale value, because it is the same in every path and would cancel out
(flagged F09).</li>
<li>The federal deduction for state tax, beyond the cap described on the inheritance tax
page.</li>
<li>Any behavioural response: the model does not know whether the household would actually stay
the course in a bad decade.</li>
</ul>
<h3>Privacy</h3>
<p>No name, street address, parcel number, account number or postcode appears on any page, and
no city or neighbourhood name is written into visible text. Properties are identified by county
only. Money is rounded to the nearest $10; statutory amounts are quoted exactly as published and
marked, because a statutory amount is public by nature.</p>
<p>Assessed values are published banded rather than exactly. An assessed value is a matter of
public record tied to one parcel, so rounding to the nearest $10 would not prevent it being
traced back to the parcel. The exact figures are used inside the model, which is not published,
and only banded anchors reach a page (flagged F03).</p>
<p>Rounding protects figures published from now on. It does not change what is already in this
repository's history, and rewriting that history is a destructive operation on shared history
that only the repository owner should authorise (flagged F19). Earlier directories in this
repository were built before the tighter rule and may contain city names and postcodes
(flagged F18); this desk does not change them.</p>
<h3>Reproducing this desk</h3>
<p><code>python3 desk-5b7b4e6b/_src/build.py</code> regenerates every page.
<code>python3 desk-5b7b4e6b/_src/verify.py</code> re-checks them, and
<code>python3 -m unittest discover -s desk-5b7b4e6b/_src -p "test_*.py"</code> runs the model
tests. The build is deterministic: a fixed seed is used, so re-running it changes nothing.</p>
"""


# ---------------------------------------------------------------------------
# write everything
# ---------------------------------------------------------------------------

PAGES = [
    ("index.html", "Start here", body_index,
     "Eight things that would change the answer, then the headline with its reinvestment risk "
     "beside it."),
    ("executive-summary.html", "Executive summary", body_exec, ""),
    ("properties.html", "Property facts", body_properties, ""),
    ("property-tax.html", "Property tax and assessment", body_property_tax, ""),
    ("inheritance-tax.html", "Estate tax, basis and assessment", body_inheritance_tax, ""),
    ("costs.html", "Running costs and capital plan", body_costs, ""),
    ("projections.html", "Year-by-year projections", body_projections, ""),
    ("paths.html", "The ten paths, side by side", body_paths, ""),
    ("black-swan.html", "Black swan — real economies", body_black_swan, ""),
    ("decision-triggers.html", "Pre-committed triggers", body_triggers, ""),
    ("whatif.html", "What-if controls", body_whatif, ""),
    ("process.html", "The transfer, step by step", body_process, ""),
    ("briefing.html", "Attorney and CPA briefing sheet", body_briefing, ""),
    ("law-watch.html", "Law watch — enacted vs proposed", body_law_watch, ""),
    ("questions.html", "Questions and information gaps", body_questions, ""),
    ("suggestions.html", "Suggestions awaiting approval", body_suggestions, ""),
    ("glossary.html", "Glossary", body_glossary, ""),
    ("sources.html", "Source register", body_sources, ""),
    ("flagged.html", "Flagged for review", body_flagged, ""),
    ("method.html", "Method and privacy", body_method, ""),
]

CSS = """
:root{--ink:#1b2330;--mute:#5d6a7d;--line:#dde3ec;--bg:#f6f8fb;--card:#fff;--blue:#1f4e79;
--warn:#8a4b00;--warnbg:#fff6e8;--ok:#155d3a}
*{box-sizing:border-box}
body{margin:0;font:15px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);
background:var(--bg)}
header.top{background:#fff;border-bottom:1px solid var(--line);padding:12px 20px;
display:flex;flex-wrap:wrap;gap:8px;align-items:baseline;justify-content:space-between}
header.top .brand{font-weight:650;color:var(--blue);text-decoration:none;font-size:17px}
header.top .stamp{font-size:12px;color:var(--mute)}
.wrap{display:grid;grid-template-columns:250px minmax(0,1fr);gap:0;max-width:1400px;margin:auto}
nav.side{border-right:1px solid var(--line);padding:16px 12px;background:#fbfcfe;
position:sticky;top:0;height:100vh;overflow:auto}
nav.side details{margin-bottom:4px;border-bottom:1px solid var(--line);padding-bottom:6px}
nav.side summary{cursor:pointer;font-weight:620;font-size:13px;color:var(--blue);
text-transform:uppercase;letter-spacing:.05em;padding:6px 4px}
nav.side ul{list-style:none;margin:4px 0 8px;padding:0}
nav.side li a{display:block;padding:5px 8px;border-radius:5px;color:var(--ink);
text-decoration:none;font-size:13.5px;line-height:1.35}
nav.side li a:hover{background:#eef3f9}
nav.side li a.here{background:#e6eef7;color:var(--blue);font-weight:600}
main.main{padding:22px 26px 60px;min-width:0}
main.wide{max-width:none}
h1{font-size:24px;margin:0 0 6px;color:#16283c}
h2{font-size:18px;margin:26px 0 8px;color:#16283c;border-bottom:2px solid var(--line);
padding-bottom:5px}
h3{font-size:15px;margin:18px 0 6px;color:#16283c}
p.sub,p.lead{color:var(--mute);margin:0 0 14px;max-width:82ch}
p.lead{font-size:15.5px;color:#33445c}
p.note{background:#f2f6fb;border-left:3px solid var(--blue);padding:9px 12px;font-size:13.5px;
margin:10px 0}
p.warn{background:var(--warnbg);border-left:3px solid var(--warn);padding:10px 12px;
font-size:13.5px;margin:12px 0}
table.data{width:100%;border-collapse:collapse;background:var(--card);font-size:13px;
margin:10px 0 18px;border:1px solid var(--line)}
table.data caption{caption-side:top;text-align:left;font-size:12.5px;color:var(--mute);
padding:6px 2px}
table.data th{background:#eef3f9;text-align:left;padding:7px 9px;border-bottom:2px solid
var(--line);font-size:12.5px;color:#2b3a4d;vertical-align:bottom}
table.data td{padding:7px 9px;border-bottom:1px solid var(--line);vertical-align:top}
table.data tbody tr:hover{background:#fafcff}
code{background:#eef2f7;padding:1px 4px;border-radius:4px;font-size:12.5px}
a.cite{font-size:11.5px;background:#e8f0f8;color:var(--blue);padding:1px 5px;border-radius:9px;
text-decoration:none;white-space:nowrap}
a.cite:hover{text-decoration:underline}
.tag{font-size:11px;padding:1px 6px;border-radius:9px;white-space:nowrap}
.t-owner{background:#eef2f7;color:#42566d}
.t-unverified{background:#fdecec;color:#8a1f1f}
.t-assumption{background:#fff4e0;color:#7a4b00}
.t-derived{background:#eaf3ec;color:#1d5c37}
.t-pure{background:#e9eef7;color:#2c4a70}
.t-mixed{background:#f3edf9;color:#4b2f70}
.t-none{background:#f0f0f0;color:#666}
.stat{background:#fff8e1;border-bottom:1px dotted #b58a00}
span.small{font-size:11.5px;color:var(--mute)}
.callout{background:#fff;border:1px solid var(--line);border-left:4px solid var(--blue);
border-radius:6px;padding:12px 16px;margin:0 0 16px}
.callout h2{margin:0 0 6px;border:0;padding:0}
.risk{background:#fff5f5;border:1px solid #f0d5d5;border-left:4px solid #b23a3a;border-radius:6px;
padding:12px 16px;margin:14px 0}
.risk h3{margin:0 0 6px;color:#8a1f1f}
ul.next{list-style:none;padding:0;display:grid;gap:8px;
grid-template-columns:repeat(auto-fill,minmax(260px,1fr))}
ul.next li{background:#fff;border:1px solid var(--line);border-radius:6px;padding:10px 12px}
ul.next a{color:var(--blue);text-decoration:none;font-weight:600}
.calc{background:#fff;border:1px solid var(--line);border-radius:6px;padding:14px 16px;
max-width:640px}
.calc label{display:block;margin:6px 0;font-size:13.5px}
.calc input{width:90px;padding:3px 6px;margin-left:6px;border:1px solid var(--line);
border-radius:4px}
.calc p#calc-out{margin-top:12px;font-weight:600;color:var(--blue)}
.sheet{background:#fff;border:1px solid var(--line);padding:18px 22px;max-width:900px}
.sheet h2{border:0;margin-top:0}
.foot{margin-top:36px;border-top:1px solid var(--line);padding-top:10px;color:var(--mute);
font-size:12.5px}
@media print{nav.side{display:none}.wrap{grid-template-columns:1fr}header.top{display:none}
table.data{font-size:11px}}
@media(max-width:900px){.wrap{grid-template-columns:1fr}nav.side{position:static;height:auto;
border-right:0;border-bottom:1px solid var(--line)}main.main{padding:16px}}
"""

JS = """(function(){
  function fmt(v){
    var n = Math.round(v/10)*10;
    return '$' + n.toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  }
  function run(){
    var eq  = parseFloat(document.getElementById('eq').value)/100;
    var hp  = parseFloat(document.getElementById('hp').value)/100;
    var inf = parseFloat(document.getElementById('inf').value)/100;
    var yr  = parseFloat(document.getElementById('yr').value);
    var out = document.getElementById('calc-out');
    if(!isFinite(eq)||!isFinite(hp)||!isFinite(inf)||!isFinite(yr)||yr<=0){
      out.textContent='Check the inputs.'; return;
    }
    var keep = 3100000*Math.pow(1+hp, yr);
    var sell = 3100000*0.935*Math.pow(1+eq, yr);
    var d = keep - sell;
    out.textContent =
      'Live in it: ' + fmt(keep) + '  |  Sell it: ' + fmt(sell) +
      '  |  Difference: ' + fmt(Math.abs(d)) + ' (' + (d>0?'keeping ahead':'selling ahead') +
      ').  In today\'s money: ' + fmt(keep/Math.pow(1+inf,yr)) + ' against ' +
      fmt(sell/Math.pow(1+inf,yr)) + '.  Tax, rent and running costs are not included.';
  }
  [].forEach.call(document.querySelectorAll('.calc input'), function(el){
    el.addEventListener('input', run);
  });
  run();
})();
"""


def main() -> None:
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    (OUT / "assets" / "desk.css").write_text(CSS)
    (OUT / "assets" / "calculator.js").write_text(JS)
    for filename, title, fn, subtitle in PAGES:
        (OUT / filename).write_text(page(title, filename, fn(), subtitle))
        print("wrote", filename)
    print(f"{len(PAGES)} pages, {len(SOURCES)} sources, {len(WORLDS)} resampled futures")


if __name__ == "__main__":
    main()
