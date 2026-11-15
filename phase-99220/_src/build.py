# -*- coding: utf-8 -*-
"""
Build the phase-99220 desk: static HTML, written into phase-99220/.

Run from anywhere:  python3 phase-99220/_src/build.py
Then:               python3 phase-99220/_src/verify.py
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import desk_model as X     # noqa: E402
import desk_sources as SRC  # noqa: E402

M = X.M
money = X.money
pct = lambda x, p=2: M.pct(x, p)  # noqa: E731

SRC_BY_ID = {s["id"]: s for s in SRC.SOURCES}


def e(s):
    return html.escape(str(s), quote=True)


def src(*ids_or_links):
    """Render a source cell: links to registered official sources or internal pages."""
    parts = []
    for item in ids_or_links:
        if item in SRC_BY_ID:
            s = SRC_BY_ID[item]
            parts.append('<a href="%s" rel="noopener">%s %s</a>' % (e(s["url"]), e(s["id"]), e(s["publisher"])))
        elif isinstance(item, tuple):
            label, href = item
            parts.append('<a href="%s">%s</a>' % (e(href), e(label)))
        else:
            parts.append(e(item))
    return "<br>".join(parts)


def table(headers, rows, cls="data"):
    h = "".join("<th>%s</th>" % e(x) for x in headers)
    body = []
    for r in rows:
        tds = []
        for i, c in enumerate(r):
            tds.append("<td>%s</td>" % c)
        body.append("<tr>%s</tr>" % "".join(tds))
    return '<div class="scroll"><table class="%s"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (
        cls, h, "".join(body))


# ------------------------------------------------------------------ menu (grouped)
GROUPS = [
    ("Decide", [
        ("index.html", "Start here", "Answer, what would change it, reinvestment risk"),
        ("what-if.html", "What-if controls", "Change the transfer year, return, and price growth"),
        ("mixed-paths.html", "Mixed paths", "Live then sell, rent then sell, park then phase in"),
        ("phased-replay.html", "Crash-entry replay", "Phased entry against the 1929 and 2008 drawdowns"),
    ]),
    ("Law and process", [
        ("timeline.html", "Deadlines timeline", "What is due, and when, after a death"),
        ("brief.html", "Attorney and CPA brief", "One printable page"),
    ]),
    ("Reference", [
        ("glossary.html", "Glossary", "Terms used on this desk"),
        ("sources.html", "Sources", "Every official link, and what it supports"),
        ("methodology.html", "Method and inputs", "Every input, and whether it is verified"),
    ]),
    ("Review", [
        ("questions.html", "Questions and gaps", "What must be known before deciding"),
        ("suggestions.html", "Suggestions", "Proposed changes; none implemented"),
        ("flagged.html", "Flagged for review", "Unverified items and irregularities"),
    ]),
]


def shell(active, title, body, extra_head="", extra_script=""):
    nav = []
    for gname, items in GROUPS:
        lis = []
        for fn, label, sub in items:
            cur = ' aria-current="page"' if fn == active else ""
            lis.append('<li><a href="%s"%s>%s</a><span>%s</span></li>' % (fn, cur, e(label), e(sub)))
        nav.append('<section><h3>%s</h3><ul>%s</ul></section>' % (e(gname), "".join(lis)))
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>%(title)s | Property A decision desk</title>
<link rel="stylesheet" href="assets/style.css">%(extra_head)s
</head><body>
<header class="top"><a class="brand" href="index.html">Property A decision desk</a>
<span class="tag">Rounded to $10 &middot; sourced rows only &middot; not legal or tax advice</span></header>
<div class="layout">
<nav class="menu" aria-label="Pages">%(nav)s</nav>
<main>%(body)s</main>
</div>
<footer class="foot">Built from official sources listed on <a href="sources.html">Sources</a>. Property A and Property B are anonymised; no names, addresses, parcel or account numbers appear on this desk. Values marked <em>owner-supplied</em> are not verified against an official record and are flagged.</footer>
%(extra_script)s
</body></html>
""" % dict(title=e(title), nav="".join(nav), body=body, extra_head=extra_head, extra_script=extra_script)


# ------------------------------------------------------------------ data
SNAP = X.snapshot()
H = SNAP["headline"]
H_ALL = {ty: X.headline(ty) for ty in (2040, 2045, 2050)}
BE = SNAP["breakevens"]
RE = SNAP["reinvest"]
MX = X.mixed_paths()
MX24 = X.mixed_paths(park_months=24)
R29 = X.replay(X.CRASH_1929)
R08 = X.replay(X.CRASH_2008)
GRID = X.what_if_grid()
PG3 = M.compare(price_growth=0.03)
Y2 = X.TREASURY_2026_11_13


def best_label(h):
    opts = dict(live_in=h["occupy_econ"], rent=h["rent_econ"], sell=h["sell_econ"])
    k = max(opts, key=opts.get)
    return {"live_in": "Live in", "rent": "Rent out", "sell": "Sell and invest"}[k]


OPTION_NAMES = {"occupy": "Live in", "rent": "Rent out", "sell": "Sell and invest"}


# ------------------------------------------------------------------ pages
def page_index():
    h = H
    gap = h["sell_econ"] - h["occupy_econ"]
    reinv_rows = []
    for r in RE:
        if abs(r["yield_"] - 0.025) < 1e-9:
            label, srcs = "2.5% (low case, assumption)", [("Flag F11: assumption, no official forecast", "flagged.html"), ("Method and inputs", "methodology.html")]
        elif abs(r["yield_"] - 0.0432) < 1e-9:
            label, srcs = "4.32% (3-month Treasury bill, 13 Nov 2026)", ["S1"]
        else:
            label, srcs = "4.88% (2-year Treasury note, 13 Nov 2026)", ["S1"]
        reinv_rows.append([
            e(label), money(r["sell_econ"]), money(r["vs_occupy"]),
            src(*srcs),
        ])
    be_run = M.compare(transfer_year=None, portfolio_return=BE["portfolio_return"])
    reinv_rows.append([
        "%s (model break-even, before the 0.6%% drag)" % pct(BE["portfolio_return"]),
        money(be_run["npv_sell_econ"]), money(be_run["npv_sell_econ"] - h["occupy_econ"]),
        src("S1", ("Break-even: Method and inputs", "methodology.html")),
    ])

    headline_rows = [
        ["Live in", money(h["occupy_econ"]), money(h["occupy_cash"]),
         src("S7", ("Model (derived): Method and inputs", "methodology.html"))],
        ["Rent out", money(h["rent_econ"]), money(h["rent_cash"]),
         src("S7", ("Model (derived): Method and inputs", "methodology.html"))],
        ["Sell and invest (model return 7.00% gross, 0.6% drag)", money(h["sell_econ"]), money(h["sell_cash"]),
         src("S1", ("Model (derived): Method and inputs", "methodology.html"))],
    ]

    menu_cards = []
    for gname, items in GROUPS:
        lis = "".join('<li><a href="%s">%s</a> <span>%s</span></li>' % (fn, e(label), e(sub)) for fn, label, sub in items)
        menu_cards.append('<div class="card"><h3>%s</h3><ul>%s</ul></div>' % (e(gname), lis))

    body = f"""
<h1>Property A: live in, rent out, or sell after the trust inheritance</h1>
<p class="lede">Property A is the home to be inherited through a trust, expected between 2040 and 2050, in Santa Clara County.
Property B is the home in San Francisco County that the heir already owns; it is not inherited and is kept out of the Property A comparison.
Transfer year 2045 is the midpoint of the 2040 to 2050 window. Present values are in 2045 dollars, economic basis, discounted at 5.00%.</p>

<section class="answer" id="what-would-change">
<h2>What would change the answer</h2>
<p><strong>Today's model answer:</strong> {e(best_label(h))} has the highest present value at the 7.00% portfolio assumption, by {money(gap)} over Live in.
That answer depends on the inputs below. Each is tested on the What-if page.</p>
<ol>
<li><strong>How well the sale proceeds grow.</strong> Selling beats living in only if the proceeds earn about <strong>{pct(BE['portfolio_return'])}</strong> a year before the 0.6% tax drag. The 3-month Treasury bill is 4.32% and the 2-year note 4.88% (13 Nov 2026), both below that line. At the bill rate, selling gives {money(RE[1]['sell_econ'])} against {money(h['occupy_econ'])} for living in. <span class="src">[S1]</span></li>
<li><strong>When the transfer happens.</strong> Each year of delay moves the answer. Compare 2040 and 2050 on the What-if page.</li>
<li><strong>House price growth.</strong> Selling keeps its lead only while house prices grow more slowly than <strong>{pct(BE['price_growth'])}</strong> a year (model break-even). At 3.0% a year, selling leads Live in by {money(PG3['npv_sell_econ'] - PG3['npv_occupy_econ'])}; the lead closes as growth rises toward the break-even.</li>
<li><strong>Whether the Proposition 19 exclusion is claimed.</strong> The exclusion applies only if the heir moves in and makes the home a principal residence within one year of the date of death. Without it, the house is reassessed to market value on transfer. <span class="src">[S7]</span></li>
<li><strong>Rent and running costs for Property A.</strong> No rent quote, insurance quote, or official utility figure for Property A has been verified. Living in is valued at the rent it avoids: at the 2.50% placeholder yield it is worth less than selling. Living in matches selling only if that avoided rent is at least <strong>{pct(BE['gross_yield'])}</strong> of value a year (model break-even). <span class="src">[Flagged F06, F07]</span></li>
<li><strong>Federal estate size.</strong> The 2026 filing threshold is $15,000,000. An estate under it files no Form 706. <span class="src">[S5]</span></li>
</ol>
</section>

<h2>Headline: present value by option, transfer in 2045</h2>
<p>Economic basis counts the rent the household avoids paying (for Live in and the sell path). Cash basis counts money only.</p>
{table(["Option", "Present value, economic basis", "Present value, cash basis", "Source"], headline_rows)}

<h2>Reinvestment risk beside the headline</h2>
<p>The sell option is only as good as the return on the money it releases. These rows re-run the sell option with the proceeds earning a stated yield, against the Live in answer.</p>
{table(["Proceeds earn", "Sell and invest, economic basis", "Sell minus Live in", "Source"], reinv_rows)}

<h2>Menu</h2>
<div class="cards">{''.join(menu_cards)}</div>

<h2>Executive summary</h2>
<ul>
<li>Property A's inheritance is a change in ownership at the date of death, not at distribution, for property held in a trust. <span class="src">[S7]</span></li>
<li>Property B is owned already and is not part of the inheritance; its rent and costs are shown only where they change the Property A comparison. Owner-supplied: two of its three units are let.</li>
<li>Selling is the highest-value option at the model's return, but it is the option most exposed to how the proceeds are invested and to a market crash just after the sale. The crash-entry replay shows the size of that exposure. <a href="phased-replay.html">See the replay</a>.</li>
<li>Every money figure is rounded to the nearest $10. Owner figures are marked owner-supplied and unverified; the verified cells stay blank.</li>
</ul>
"""
    return shell("index.html", "Start here", body)


def page_what_if():
    rows = []
    for g in GRID:
        rows.append([
            str(g["ty"]), pct(g["pr"]), pct(g["pg"], 1), money(g["occupy"]), money(g["rent"]),
            money(g["sell"]), OPTION_NAMES[g["best"]], money(g["gap"]),
            src("S1", "S7", ("Model (derived): Method and inputs", "methodology.html")),
        ])
    data = json.dumps([[g["ty"], g["pr"], g["pg"], g["occupy"], g["rent"], g["sell"], g["best"], g["gap"]] for g in GRID])
    body = f"""
<h1>What-if controls</h1>
<p class="lede">Pick a transfer year, a return on the sale proceeds, and a house price growth rate. The page looks up the matching row in the model run; it does not recalculate in the browser.
Return values use the two official Treasury yields, the model's 7.00% base case, and a 6.00% middle case.</p>
<section class="controls" aria-label="What-if controls">
<label>Transfer year
<select id="ty"><option value="2040">2040</option><option value="2045" selected>2045</option><option value="2050">2050</option></select></label>
<label>Return on sale proceeds, gross of the 0.6% drag
<select id="pr">
<option value="0.0432">4.32% (3-month Treasury, S1)</option>
<option value="0.0488">4.88% (2-year Treasury, S1)</option>
<option value="0.06">6.00% (assumption)</option>
<option value="0.07" selected>7.00% (model base case)</option>
</select></label>
<label>House price growth a year
<select id="pg"><option value="0.03">3.0% (assumption)</option><option value="0.04" selected>4.0% (model base case)</option><option value="0.05">5.0% (assumption)</option></select></label>
</section>
<section class="result" id="result" aria-live="polite"></section>
<h2>Every combination in the model run</h2>
<p>Economic basis, nearest $10. A row shows the best option and the gap between selling and living in.</p>
{table(["Transfer year", "Proceeds return", "House growth", "Live in", "Rent out", "Sell and invest", "Best", "Gap, sell vs live in", "Source"], rows)}
"""
    script = f"""<script>
(function(){{
var G={data};
var NAMES={{occupy:"Live in",rent:"Rent out",sell:"Sell and invest"}};
function fmt(n){{return (n<0?"&minus;$":"$")+Math.abs(n).toLocaleString("en-US");}}
function pc(x){{return (x*100).toFixed(2)+"%";}}
function show(){{
 var ty=+document.getElementById("ty").value, pr=+document.getElementById("pr").value, pg=+document.getElementById("pg").value;
 var hit=G.filter(function(g){{return g[0]===ty && Math.abs(g[1]-pr)<1e-9 && Math.abs(g[2]-pg)<1e-9;}})[0];
 var el=document.getElementById("result");
 if(!hit){{el.innerHTML="<p>No model run for this combination.</p>";return;}}
 el.innerHTML="<h2>Result: "+NAMES[hit[6]]+" has the highest present value</h2>"+
 "<table class='data'><thead><tr><th>Option</th><th>Present value, economic basis</th></tr></thead><tbody>"+
 "<tr><td>Live in</td><td>"+fmt(hit[3])+"</td></tr><tr><td>Rent out</td><td>"+fmt(hit[4])+"</td></tr><tr><td>Sell and invest</td><td>"+fmt(hit[5])+"</td></tr></tbody></table>"+
 "<p>Gap, sell minus live in: "+fmt(hit[5]-hit[3])+". Source: model run on this page; inputs on <a href='methodology.html'>Method and inputs</a>.</p>";
}}
["ty","pr","pg"].forEach(function(id){{document.getElementById(id).addEventListener("change",show);}});
show();
}})();
</script>"""
    return shell("what-if.html", "What-if controls", body, extra_script=script)


def page_mixed():
    mv = MX["values"]
    rows = [
        ["Live in (cash basis, no rent counted)", money(mv["keep_occupy"]), src("S7", ("Model", "methodology.html"))],
        ["Rent out (cash basis)", money(mv["keep_rent"]), src("S7", ("Model", "methodology.html"))],
        ["Live 5 years, then sell", money(mv["live_5_sell"]), src("S7", "S1", ("Model", "methodology.html"))],
        ["Live 10 years, then sell", money(mv["live_10_sell"]), src("S7", "S1", ("Model", "methodology.html"))],
        ["Rent 5 years, then sell", money(mv["rent_5_sell"]), src("S7", "S1", ("Model", "methodology.html"))],
        ["Rent 10 years, then sell", money(mv["rent_10_sell"]), src("S7", "S1", ("Model", "methodology.html"))],
        ["Sell at transfer and invest now", money(mv["sell_now"]), src("S1", ("Model", "methodology.html"))],
        ["Sell at transfer, park 24 months in Treasuries, then buy over 12 months (no crash)", money(MX24["values"]["park_24_phase_12"]), src("S1", ("Model", "methodology.html"))],
        ["Sell at transfer, park 36 months in Treasuries, then buy over 12 months (no crash)", money(mv["park_36_phase_12"]), src("S1", ("Model", "methodology.html"))],
    ]
    body = f"""
<h1>Mixed paths</h1>
<p class="lede">The brief asked for paths that combine the three pure choices. Each mixed path below is built from the same model rows as the pure options.
These values are <strong>cash basis</strong>, present value at the 2045 transfer, discounted at 5.00%. Cash basis counts money only, so it is not the same as the headline table, which also counts rent avoided.
Read the rows against each other: the first two rows are the pure living and renting options on the same basis.</p>
{table(["Path", "Present value, cash basis", "Source"], rows)}
<h2>How to read the mixed rows</h2>
<ul>
<li><strong>Live then sell</strong> and <strong>rent then sell</strong> use the model's own year-by-year cash rows for the years before the sale, then sell at that year's modelled value less 6.0% selling costs, and grow the proceeds at the net return.</li>
<li><strong>Park then phase in</strong> is the mechanics the brief asked for: the proceeds sit in 3-month Treasury bills at 4.32% for the parking period, then are bought in equal monthly parts over 12 months (the 12-month buying period is an assumption). It has no market crash. The crash-entry test is on the <a href="phased-replay.html">replay page</a>.</li>
<li>Choosing a mixed path does not change the Proposition 19 rule: moving out and renting makes the house reassessable. Check the timing on the <a href="timeline.html">timeline</a>.</li>
</ul>
"""
    return shell("mixed-paths.html", "Mixed paths", body)


def page_replay():
    def rowset(res_key):
        rows = []
        names = {"lump": "Lump sum at the peak", "park_24_phase_12": "Park 24 months, buy over 12",
                 "park_36_phase_12": "Park 36 months, buy over 12"}
        for k in ("lump", "park_24_phase_12", "park_36_phase_12"):
            r = res_key["results"][k]
            rows.append([
                names[k], money(r["crash_10y"]), money(r["crash_h"]), money(r["lowest"]),
                money(r["nocrash_10y"]),
                money(r["crash_10y"] - r["nocrash_10y"]),
            ])
        return rows
    hdr = ["Strategy", "Value after 10 years, crash", "Value after 25 years, crash", "Lowest value on the path", "Value after 10 years, no crash", "Crash minus no crash, at 10 years"]
    srcs1929 = ["S3"]
    srcs2008 = ["S4", ("Recovery 48 months: assumption, not from an official source (flag F02)", "flagged.html")]
    rows29 = [r + [src(*srcs1929)] for r in rowset(R29)]
    rows08 = [r + [src(*srcs2008)] for r in rowset(R08)]
    hdr2 = hdr + ["Source"]
    body = f"""
<h1>Crash-entry replay: phased entry against the 1929 and 2008 drawdowns</h1>
<p class="lede">The question: does parking the sale proceeds for 24 to 36 months, then buying in over a year, soften the damage if the market falls just after the sale?
The replay starts at the market peak, with {money(R29['invested'])} invested (the model's sale proceeds, rounded). It uses the official peak-to-trough figures and tests two cases.</p>

<h2>Official drawdowns used</h2>
{table(["Episode", "Peak to trough", "Months to trough", "Recovery used in the replay", "Source"], [
    ["1929 to 1932 (Dow Jones Industrial Average)", "&minus;89%", "34 (Sep 1929 to Jul 1932)", "268 months (Jul 1932 to Nov 1954, prior high regained)", src("S3")],
    ["2007 to 2009 (S&P 500)", "&minus;57%", "17 (Oct 2007 to Mar 2009)", "48 months: an assumption, not stated in the official essay", src("S4", ("Flag F02", "flagged.html"))],
])}

<h2>1929 crash: results, in nominal dollars</h2>
{table(hdr2, rows29)}

<h2>2008 crash: results, in nominal dollars</h2>
{table(hdr2, rows08)}

<h2>What the replay shows, and what it does not</h2>
<ul>
<li><strong>Lump sum at the peak</strong> carries the whole drop. In 1929 the lowest value is {money(R29['results']['lump']['lowest'])}, against {money(R29['invested'])} invested. The phased strategies never buy at the peak.</li>
<li><strong>Parking for 24 or 36 months</strong> keeps the money in Treasury bills while the fall happens. A 36-month park is still in cash through the 1929 trough, so its lowest value is the amount parked ({money(R29['results']['park_36_phase_12']['lowest'])}). A 24-month park starts buying at month 24, while the 1929 fall is still under way, so its lowest value is {money(R29['results']['park_24_phase_12']['lowest'])}. Its risk is the rate on the parked money and the price paid during the buying period.</li>
<li><strong>A phased entry that buys into a fall can beat no-crash.</strong> This is a result of buying at low prices if the index later recovers. It is not a forecast, and it reverses if prices stay low. The replay assumes a recovery, and the recovery shapes are straight lines, which the real markets did not follow.</li>
<li><strong>Reinvestment risk.</strong> The cash rate used for parking is 4.32%, the 3-month Treasury bill on 13 Nov 2026. If bill rates fall, the parked money earns less.</li>
<li>The replay is not a forecast of 2040 to 2050 markets. It answers one question: how big is entry risk, measured against two historical drawdowns. The hypothetical constant-decline calculator from another desk is on <a href="../cbe/phased-investing.html">cbe / phased investing</a>, and is not a historical replay.</li>
</ul>
"""
    return shell("phased-replay.html", "Crash-entry replay", body)


def page_timeline():
    rows = [
        ["Day 0", "Date of death. For property held in a trust, the date of death is the change in ownership for tax purposes, even if the deed to the heir is recorded later.", src("S7")],
        ["Within 90 days", "If the home is held in an LLC, partnership or corporation, file BOE-100-B with the State Board of Equalization.", src("S7", "S8")],
        ["Within 150 days", "File BOE-502-D (Change in Ownership Statement, Death of a Real Property Owner) with the County Assessor. The trustee files it for trust property. If probate applies, it is due before or at the inventory filing instead.", src("S7")],
        ["Within 9 months (if Form 706 is required)", "Form 706 due date for estates above the filing threshold. The 2026 threshold is $15,000,000. Due-date wording is not yet confirmed from the official instructions.", src("S5", "S6", ("Flag F04: due-date text not yet read", "flagged.html"))],
        ["6 months after the 706 due date", "Automatic extension to file (Form 4768). The extension does not extend time to pay. Not yet confirmed from an official page.", src(("Flag F04", "flagged.html"))],
        ["Within 1 year of the change in ownership", "For the parent-child exclusion (Proposition 19), the home must become the heir's principal residence within one year of the change in ownership. Claim form BOE-19-P goes to the County Assessor.", src("S7")],
        ["Claim filing deadline (BOE-19-P)", "Not confirmed from an official page in this session. Do not rely on any date until verified.", src(("Flag F05", "flagged.html"))],
        ["10 December", "Delinquency date for the first property tax installment. A 10% penalty applies after it.", src("S7")],
        ["10 April", "Delinquency date for the second property tax installment. A 10% penalty applies after it.", src("S7")],
    ]
    body = f"""
<h1>Deadlines as a timeline</h1>
<p class="lede">Dates run from the day of death, not the day of distribution. Dates that the official pages confirm are shown as confirmed; anything not yet read is flagged. This page is not legal advice; check each date with the trust attorney and the CPA.</p>
<ol class="timeline">
{''.join('<li><span class="when">%s</span><span class="what">%s</span><span class="srcs">%s</span></li>' % (e(r[0]), r[1], r[2]) for r in rows)}
</ol>
<h2>As a table</h2>
{table(["When", "What is due", "Source"], rows)}
"""
    return shell("timeline.html", "Deadlines timeline", body)


def page_brief():
    body = f"""
<div class="brief">
<h1>Attorney and CPA briefing sheet: Property A</h1>
<p class="small">Anonymised. Placeholders: [Decedent], [Trustee], [Heir], [Property A] (inherited through trust, Santa Clara County), [Property B] (already owned, San Francisco County). Figures rounded to $10. Owner figures are unverified. Not legal or tax advice. Prepared from this desk; see the links below.</p>

<h2>The question</h2>
<p>When [Property A] passes to [Heir] through [Trustee], expected 2040 to 2050, should [Heir] live in it, rent it, or sell it and invest the proceeds? The model's transfer year is 2045.</p>

<h2>Headline numbers (transfer 2045, economic basis)</h2>
<table class="data small">
<tr><th>Option</th><th>Present value</th><th>Source</th></tr>
<tr><td>Live in</td><td>{money(H['occupy_econ'])}</td><td>{src('S7', ('Model', 'methodology.html'))}</td></tr>
<tr><td>Rent out</td><td>{money(H['rent_econ'])}</td><td>{src('S7', ('Model', 'methodology.html'))}</td></tr>
<tr><td>Sell and invest</td><td>{money(H['sell_econ'])}</td><td>{src('S1', ('Model', 'methodology.html'))}</td></tr>
<tr><td>Break-even return on proceeds, before 0.6% drag</td><td>{pct(BE['portfolio_return'])}</td><td>{src(('Model', 'methodology.html'))}</td></tr>
<tr><td>Treasury yields, 13 Nov 2026: 3-month / 2-year</td><td>4.32% / 4.88%</td><td>{src('S1')}</td></tr>
</table>

<h2>Reinvestment and crash-entry risk</h2>
<p>If the proceeds earn the 3-month bill rate, selling is worth {money(abs(RE[1]['vs_occupy']))} less than living in. A 1929-size fall with a lump-sum purchase at the peak leaves a low of {money(R29['results']['lump']['lowest'])} on {money(R29['invested'])}. Parking 24 to 36 months and buying in over 12 months avoids buying at the peak.</p>

<h2>Law points to confirm</h2>
<ol>
<li>Date of death is the change in ownership for trust property; the reassessment and exclusion clocks start then. <span class="src">[S7]</span></li>
<li>Parent-child exclusion: heir must make the home the principal residence within one year of the change in ownership; claim on BOE-19-P. <span class="src">[S7]</span></li>
<li>BOE-502-D within 150 days after death, trustee filing for trust property. <span class="src">[S7]</span></li>
<li>BOE-100-B within 90 days if an entity holds any interest. <span class="src">[S7, S8]</span></li>
<li>Federal filing threshold for a 2026 death: $15,000,000; Form 706 due date to confirm. <span class="src">[S5, Flag F04]</span></li>
</ol>

<h2>Questions for the attorney</h2>
<ol>
<li>Is the house held in the trust directly, or through an entity? (Changes BOE-100-B.)</li>
<li>Does the trust give the heir a right to live in the house, and on what date?</li>
<li>Who is the trustee for BOE-502-D and for the 150-day clock?</li>
<li>What is the probate position if the trust does not cover the house?</li>
</ol>

<h2>Questions for the CPA</h2>
<ol>
<li>Basis: what is the house's basis on the date of death, and how is it documented?</li>
<li>Is Form 706 needed? If the estate is near $15,000,000 in 2026, what counts toward it?</li>
<li>Income tax on the sale, including the rate that applies to the heir's gain above the basis.</li>
<li>Whether a rental year changes the answer through depreciation or the loss of the exclusion.</li>
</ol>

<h2>What is still missing</h2>
<ul>
<li>No verified rent quote for Property A; no verified insurance quote; no verified water or power bill for Property A. <span class="src">[F06, F07]</span></li>
<li>Owner property tax and assessed value figures are owner-supplied and unverified. <span class="src">[F01]</span></li>
</ul>
<p class="small">Sources: <a href="sources.html">Sources</a>. Flags: <a href="flagged.html">Flagged for review</a>.</p>
</div>
"""
    return shell("brief.html", "Attorney and CPA brief", body)


def page_glossary():
    rows = [
        ["Change in ownership", "A transfer that can trigger reassessment of a California property to market value. For trust property, the date of death is the change in ownership.", src("S7")],
        ["Intergenerational exclusion (Proposition 19)", "Lets a parent's principal residence pass to a child without reassessment to market value, if the child makes it their principal residence within one year of the change in ownership.", src("S7")],
        ["Claim form BOE-19-P", "The claim form filed with the County Assessor to apply for the parent-child exclusion.", src("S7")],
        ["BOE-502-D", "The change in ownership statement for a death, filed with the County Assessor within 150 days after death for trust property.", src("S7")],
        ["BOE-100-B", "Statement of change in control or ownership of a legal entity, filed with the State Board of Equalization within 90 days.", src("S7", "S8")],
        ["Form 706", "The federal estate tax return the executor files to figure estate tax.", src("S6")],
        ["Federal filing threshold", "The amount above which an estate must file Form 706. It is $15,000,000 for a 2026 death.", src("S5")],
        ["Treasury bill", "A short-term U.S. government debt security. The 3-month rate is the yield on a 3-month Treasury bill, from the daily par yield curve.", src("S1")],
        ["Constant-maturity yield", "A yield read off the Treasury's daily par yield curve at a fixed maturity, such as 3 months or 2 years.", src("S1")],
        ["Reinvestment risk", "The risk that money from a sale or a maturity can only be re-invested at a lower return.", src(("Definition used on this desk; no official text opened. Flag F09", "flagged.html"))],
        ["Phased entry", "Buying an asset in equal parts over time, instead of all at once. Also called dollar-cost averaging.", src(("Definition used on this desk; no official text opened. Flag F09", "flagged.html"))],
        ["Drawdown", "The fall from a peak to the lowest later point, as a percentage of the peak.", src("S3", "S4")],
        ["Break-even", "The value of one input at which two options are equal, all other inputs held as shown.", src(("Model method; see Method and inputs", "methodology.html"))],
        ["Present value", "Future money restated in today's terms (here, 2045 dollars) at the discount rate.", src(("Model method; see Method and inputs", "methodology.html"))],
        ["Economic basis", "Money plus the rent the household avoids by living in its own home. Cash basis counts money only.", src(("Model method; see Method and inputs", "methodology.html"))],
        ["Parking period", "The time the sale proceeds sit in Treasuries before any stock purchase starts.", src(("Desk term; see Mixed paths", "mixed-paths.html"))],
        ["Net return", "Return after the 0.6% annual tax drag the model applies to a portfolio.", src(("Model assumption; see Method and inputs", "methodology.html"))],
    ]
    body = f"""
<h1>Glossary</h1>
<p class="lede">Each term is linked to the source that defines it on this desk. Where no official text was opened, the row says so and is flagged.</p>
{table(["Term", "Meaning on this desk", "Source"], rows)}
"""
    return shell("glossary.html", "Glossary", body)


def page_questions():
    rows = [
        ["Will the house be held directly in the trust, or through an entity?", "Decides whether BOE-100-B applies (90 days).", src("S7", "S8")],
        ["Will the heir live in the house within one year of the change in ownership?", "Decides whether Prop 19 applies. Without it, the house is reassessed to market value.", src("S7")],
        ["What is the house's market value on the date of death?", "Sets the reassessed value and the sale proceeds. The 2045 value in the model is an assumption.", src(("Flag F01", "flagged.html"))],
        ["What is the current assessed value and property tax bill, verified from the County Assessor?", "The model uses owner records, which are not verified.", src(("Flag F01", "flagged.html"))],
        ["What rent would Property A earn?", "Needed to test the rent option. No quote exists.", src(("Flag F06", "flagged.html"))],
        ["What do insurance, water and power cost for Property A?", "Needed for running costs. Owner estimates only.", src(("Flag F07", "flagged.html"))],
        ["What is the estate's total value on the date of death?", "Decides whether Form 706 is needed, against $15,000,000 for 2026.", src("S5")],
        ["When is the Form 706 due, and does the extension apply?", "Sets the first federal deadline.", src("S9", ("Flag F04", "flagged.html"))],
        ["What is the BOE-19-P claim deadline?", "Sets when the exclusion must be claimed.", src(("Flag F05", "flagged.html"))],
        ["What rate will the proceeds earn after the sale?", "Reinvestment risk: each 1 point of return changes the sell answer.", src("S1")],
    ]
    body = f"""
<h1>Questions and information gaps</h1>
<p class="lede">These questions have to be answered before a decision can reasonably be made. Each row says what it decides and where the answer is found. None of these items has been filled in with an estimate.</p>
{table(["Question", "Why it matters", "Source or flag"], rows)}
"""
    return shell("questions.html", "Questions and gaps", body)


def page_suggestions():
    items = [
        ("S-01", "Add a verified Santa Clara County assessed-value and tax-bill page for Property A, from the County Assessor and Tax Collector.", src("S7")),
        ("S-02", "Obtain three written insurance quotes for a primary-residence policy on Property A, and log the quote dates.", src(("Flag F06", "flagged.html"))),
        ("S-03", "Obtain one written rent opinion for Property A, to test the rent path.", src(("Flag F06", "flagged.html"))),
        ("S-04", "Read the Form 706 instructions 'When To File' section and confirm the due date and extension before anyone plans around it.", src("S9")),
        ("S-05", "Read the BOE-19-P form and its instructions for the claim deadline.", src("S7")),
        ("S-06", "Replace the 48-month 2008 recovery assumption with an official recovery date, or show it as a range.", src("S4", ("Flag F02", "flagged.html"))),
        ("S-07", "Keep the cash rate tied to the Treasury yield on the day the plan is reviewed, not a fixed number.", src("S1")),
        ("S-08", "Show the sell answer at each year of the 2040-2050 window in one table, not only at the 2045 midpoint.", src(("What-if page", "what-if.html"))),
        ("S-09", "Decide, with counsel, whether the git history of this repository should be rewritten to remove earlier unrounded figures. This is a repository-wide decision and is not done by this desk.", src(("Flag F08", "flagged.html"))),
        ("S-10", "Add the Property B rent and running costs as a separate table, so the heir can see the cash flow it covers.", src(("Methodology", "methodology.html"))),
    ]
    rows = [[sid, text, link, "PROPOSED. Not implemented. Decision: [ ] accept  [ ] modify  [ ] reject"] for sid, text, link in items]
    body = f"""
<h1>Suggestions for review</h1>
<p class="lede">Proposed changes to this desk and to the decision process. Nothing on this list has been implemented. Choose accept, modify, or reject for each one before any change is made.</p>
{table(["No.", "Proposal", "Source or flag", "Status and decision"], rows)}
"""
    return shell("suggestions.html", "Suggestions", body)


def page_flagged():
    rows = [
        ["F01", "Owner-supplied figures: Property A value (2026), assessed value and tax bills, Property B bill and assessed value. Not verified against an official record. Verified cells are blank.", src(("County Assessor and Tax Collector (not opened)", "https://www.boe.ca.gov/proptaxes/countycontacts.htm"))],
        ["F02", "2008 recovery period (48 months) is an assumption. The official essay gives the drawdown only, not a recovery date.", src("S4")],
        ["F03", "The 1929 and 2008 recoveries are drawn as straight lines between official endpoints. Real paths were not straight. The replay shows the shape, not the timing.", src("S3", "S4")],
        ["F04", "Form 706 due date (9 months) and extension (6 months) not confirmed from the official instructions in this session.", src("S9")],
        ["F05", "BOE-19-P claim deadline not confirmed from an official page.", src("S7")],
        ["F06", "No verified insurance premium, and no rent quote, for Property A. Owner estimate of insurance is not used as a verified value.", src(("California Department of Insurance (not opened)", "https://www.insurance.ca.gov/"))],
        ["F07", "Water and power for Property A are owner-supplied. No official utility rate for the property's provider was verified.", src(("Utility rate sources (not opened)", "https://www.sfpuc.org/"))],
        ["F08", "Earlier desks in this repository include unrounded figures in git history. Rewriting shared history is an owner decision; this desk does not rewrite history.", src(("Repository review (earlier desks)", "../cbe/repo-review.html"))],
        ["F09", "Definitions in the glossary marked 'definition used on this desk' have no official text opened.", src("S1")],
        ["F10", "The 2-year yield was 4.86% on 12 Nov 2026 (FRED) and 4.88% on 13 Nov 2026 (Treasury). Both are shown; the 13 Nov row is used for the desk's cash rate.", src("S1", "S2")],
        ["F11", "Price growth (4%), portfolio return (7%), discount rate (5%) and rent growth (3%) are assumptions, not official forecasts. Break-evens are shown so they can be tested.", src(("Method and inputs", "methodology.html"))],
    ]
    body = f"""
<h1>Flagged for review</h1>
<p class="lede">Items that could not be confirmed from an official source, irregularities found in the repository, and assumptions that carry weight. Flagged items do not block the desk. Each one names what would close it.</p>
{table(["Flag", "What is flagged", "Source or where it would be closed"], rows)}
"""
    return shell("flagged.html", "Flagged for review", body)


def page_sources():
    rows = []
    for s in SRC.SOURCES:
        rows.append([e(s["id"]), '<a href="%s">%s</a>' % (e(s["url"]), e(s["title"])), e(s["publisher"]), e(s["status"]), e(s["supports"])])
    body = f"""
<h1>Sources</h1>
<p class="lede">Each source is one this session opened, unless the status column says otherwise. Links go to official sites.</p>
{table(["ID", "Title and link", "Publisher", "What was checked", "What it supports"], rows)}
<h2>Not opened</h2>
<ul>{''.join('<li>%s</li>' % e(t) for t, _ in SRC.NOT_OPENED)}</ul>
"""
    return shell("sources.html", "Sources", body)


def page_methodology():
    F11 = ("Flag F11: assumption", "flagged.html")
    SRCS = [[F11], [F11], [F11], ["S1"], ["S1"], [F11], [F11], ["S5"], [("Flag F01: owner-supplied", "flagged.html")],
            [("Flag F06: no verified figure", "flagged.html")], ["S3"], ["S4"], [("Flag F02: assumption", "flagged.html")]]
    rows = [
        ["Transfer year", "2045 (midpoint of 2040 to 2050)", "Assumption (owner window)"],
        ["House price growth", "4.0% a year", "Assumption; break-even 5.58%"],
        ["Portfolio return", "7.0% a year, less 0.6% drag", "Assumption; break-even 5.20%"],
        ["Cash rate for parking", "4.32% (3-month Treasury, 13 Nov 2026)", "S1"],
        ["Two-year cash rate", "4.88% (2-year Treasury, 13 Nov 2026)", "S1"],
        ["Discount rate", "5.0%", "Assumption"],
        ["Selling cost", "6.0% of value", "Assumption"],
        ["Federal filing threshold, 2026 death", "$15,000,000", "S5"],
        ["Property A value (2026)", "$3,100,000 (owner estimate)", "Owner-supplied, unverified (F01)"],
        ["Property A running costs", "Owner estimates; not verified", "F06, F07"],
        ["1929 drawdown and recovery", "89%; 34 months down; 268 months to regain", "S3"],
        ["2008 drawdown", "57%; 17 months down", "S4"],
        ["2008 recovery", "48 months", "Assumption (F02)"],
    ]
    body = f"""
<h1>Method and inputs</h1>
<p class="lede">The model is the owner-brief model published in the cbe desk, used read-only. This desk adds the what-if grid, the reinvestment test, the mixed paths, and the crash-entry replay. Every input is listed.</p>
{table(["Input", "Value used", "Status", "Source"], [r + [src(*SRCS[i])] for i, r in enumerate(rows)])}
<h2>Method notes</h2>
<ul>
<li>Break-evens are the input values at which keep and sell are equal. They are computed by bisection in the cbe model.</li>
<li>The economic basis adds the rent avoided by living in the home. The cash basis does not.</li>
<li>The replay is monthly. Phased strategies hold the parked money at the cash rate and buy equal parts; the lump sum buys all at the peak.</li>
<li>All money is rounded to the nearest $10. Percentages are shown to two decimal places.</li>
</ul>
"""
    return shell("methodology.html", "Method and inputs", body)


PAGES = [
    ("index.html", page_index),
    ("what-if.html", page_what_if),
    ("mixed-paths.html", page_mixed),
    ("phased-replay.html", page_replay),
    ("timeline.html", page_timeline),
    ("brief.html", page_brief),
    ("glossary.html", page_glossary),
    ("sources.html", page_sources),
    ("methodology.html", page_methodology),
    ("questions.html", page_questions),
    ("suggestions.html", page_suggestions),
    ("flagged.html", page_flagged),
]


def main():
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    for fn, fnc in PAGES:
        with open(os.path.join(OUT, fn), "w", encoding="utf-8") as f:
            f.write(fnc())
    with open(os.path.join(OUT, "assets", "style.css"), "w", encoding="utf-8") as f:
        f.write(STYLE)
    print("built %d pages into %s" % (len(PAGES), OUT))


STYLE = """
:root{--ink:#1d2330;--mute:#5b6475;--line:#d9dee7;--bg:#f6f8fb;--acc:#1f5fa8;--warn:#8a5a00;--ok:#1d6b3a}
*{box-sizing:border-box}
body{margin:0;font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);background:var(--bg)}
a{color:var(--acc)}
header.top{background:#fff;border-bottom:1px solid var(--line);padding:12px 20px;display:flex;gap:16px;align-items:baseline;flex-wrap:wrap}
.brand{font-weight:700;color:var(--ink);text-decoration:none;font-size:17px}
.tag{color:var(--mute);font-size:13px}
.layout{display:grid;grid-template-columns:260px 1fr;gap:0;min-height:80vh}
nav.menu{background:#fff;border-right:1px solid var(--line);padding:14px 12px}
nav.menu section{margin-bottom:14px}
nav.menu h3{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--mute);margin:8px 6px 4px}
nav.menu ul{list-style:none;margin:0;padding:0}
nav.menu li{padding:4px 6px;border-radius:6px}
nav.menu li a{font-weight:600;text-decoration:none;color:var(--ink);display:block}
nav.menu li span{display:block;font-size:12px;color:var(--mute)}
nav.menu li:has(a[aria-current]){background:#e8f0fa}
main{padding:22px 28px;max-width:1100px}
h1{font-size:24px;margin:0 0 8px}
h2{font-size:18px;margin:26px 0 8px;border-bottom:1px solid var(--line);padding-bottom:4px}
.lede{color:var(--mute);max-width:820px}
.answer{background:#fff;border:1px solid var(--line);border-left:5px solid var(--acc);border-radius:8px;padding:12px 18px;margin:12px 0}
.answer h2{border:0;margin-top:4px}
.src{font-size:12px;color:var(--mute)}
.scroll{overflow-x:auto}
table.data{border-collapse:collapse;width:100%;background:#fff;font-size:14px;margin:8px 0}
table.data th,table.data td{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
table.data th{background:#eef2f8;font-weight:600}
table.data td a{word-break:break-word}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}
.card{background:#fff;border:1px solid var(--line);border-radius:8px;padding:10px 14px}
.card h3{margin:2px 0 6px;font-size:15px}
.card ul{margin:0;padding-left:16px}
.controls{display:flex;gap:14px;flex-wrap:wrap;background:#fff;border:1px solid var(--line);border-radius:8px;padding:12px}
.controls label{display:flex;flex-direction:column;font-weight:600;font-size:13px;min-width:200px}
.controls select{margin-top:4px;padding:6px;font-size:14px}
.result{margin:12px 0}
ol.timeline{list-style:none;padding:0;margin:8px 0}
ol.timeline li{display:grid;grid-template-columns:200px 1fr 260px;gap:12px;background:#fff;border:1px solid var(--line);border-radius:6px;padding:8px 12px;margin-bottom:8px}
ol.timeline .when{font-weight:700}
ol.timeline .srcs{font-size:12px;color:var(--mute)}
.foot{padding:12px 28px;color:var(--mute);font-size:12px;border-top:1px solid var(--line);background:#fff}
.small{font-size:12.5px}
.brief{background:#fff;padding:18px;border:1px solid var(--line)}
.brief h1{font-size:20px}
.brief h2{font-size:14px;margin:12px 0 4px}
.brief p,.brief li{font-size:12.5px;margin:3px 0}
.brief ol,.brief ul{margin:2px 0;padding-left:18px}
@media (max-width:800px){.layout{grid-template-columns:1fr}nav.menu{border-right:0}ol.timeline li{grid-template-columns:1fr}}
@media print{
 @page{size:Letter;margin:10mm}
 header.top,nav.menu,footer.foot,.controls,.tag{display:none!important}
 .layout{display:block}main{padding:0;max-width:none}
 body{background:#fff;font-size:10pt}
 .brief{border:0;padding:0}
 .brief h1{font-size:14pt}.brief h2{font-size:10.5pt;margin:6px 0 2px}.brief p,.brief li,.brief td,.brief th{font-size:8.5pt;line-height:1.25}
 table.data th,table.data td{padding:2px 4px}
 a{color:#000;text-decoration:none}
}
"""

if __name__ == "__main__":
    main()
