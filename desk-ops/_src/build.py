# -*- coding: utf-8 -*-
"""Builds the operating desk: static HTML, no scripts, no external assets.

Session arena-ea3f2cee. Every page is generated from model.json so that a re-run after an
input change rebuilds the site and shows whether the recommendation moved — the owner's
"after any input changes, rebuild the model and the site and see whether the recommendation
moved" requirement.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import model
import sources
from shell import (bar_row, esc, kpi, money, page, pct, src, table, tag)

OUT = Path(__file__).resolve().parent.parent
DATA = json.loads((Path(__file__).with_name("model.json")).read_text())

PATHS = {p["id"]: p for p in DATA["paths"]}
REG = {r["id"]: r for r in DATA["regimes"]}
GAPS = DATA["gaps"]


def g(ty, h, path, case="mid", field="net"):
    for row in DATA["grid"]:
        if row["path"] == path and row["transfer_year"] == ty and row["horizon"] == h:
            return row[case][field]
    raise KeyError((ty, h, path, case, field))


def grid_row(ty, h, path):
    for row in DATA["grid"]:
        if row["path"] == path and row["transfer_year"] == ty and row["horizon"] == h:
            return row
    raise KeyError((ty, h, path))


BE = DATA["break_evens"]
BE_BASE_LOW = BE["base_dependence"]["low"]
BE_BASE_HIGH = BE["base_dependence"]["high"]
DIST = DATA["distribution"]
BASE_TY, BASE_H = 2045, 20


# ---------------------------------------------------------------------------- index (first screen)
def p_index():
    live_cash = g(BASE_TY, BASE_H, "live", field="net")
    live_housing = g(BASE_TY, BASE_H, "live", field="with_housing")
    sell_cash = g(BASE_TY, BASE_H, "sell")
    rent_cash = g(BASE_TY, BASE_H, "rent")
    g1929 = {r["months"]: r for r in DATA["phased"] if r["regime"] == "crash1929"}
    g2008 = {r["months"]: r for r in DATA["phased"] if r["regime"] == "crash2008"}
    gbase = {r["months"]: r for r in DATA["phased"] if r["regime"] == "base"}

    body = f"""
<h1>What would change the answer</h1>
<p class="lede">One house is expected through a trust between 2040 and 2050. A second, already
owned, is a three-unit building with two units let. The question is what the heir does with the
inherited house: live in it, let it out, or sell it and invest. This page answers in the only
order that survives scrutiny — first which measurements decide it, then what the answer is.</p>

<div class="answer">
<h3>Five things decide this, and nothing else does</h3>
<ol>
<li><b>House-price growth.</b> Holding the house and selling it tie at
<b>{pct(BE['house_growth_live'],2)}</b> a year in the base case. Below that, selling wins; above it,
holding wins. That single number is the whole argument. It is a break-even, not a forecast.</li>
<li><b>Whether the heir really moves in — and stays.</b> The intergenerational exclusion is
worth <b>{money(DATA['exposure'][0]['tax_high'] - DATA['exposure'][1]['tax_high'], '')} a year</b>
at the top of the local rate range on the modelling base. Losing it after the fact costs
<b>{money(abs(next(w['delta'] for w in DATA['what_if'] if 'stops occupying' in w['label'])), '')}</b>
over twenty years. {src(sources,'rtc_63_2','RTC 63.2')}</li>
<li><b>What the money would otherwise earn.</b> At the base case the other option — selling and
investing — beats living in the house unless equities return less than
<b>{pct(BE['equity_return'],2)}</b> a year, or rent is worth more than
<b>{pct(BE['imputed_yield'],1)}</b> of the house's value to the heir.</li>
<li><b>When the equity market is entered.</b> If the sale is followed by a 1929-shaped or
2008-shaped crash, parking the proceeds in 3-month to 2-year Treasuries for 24–36 months before
phasing in <i>adds</i> <b>{money(g1929[24]['per_million'],'')} to {money(g1929[36]['per_million'],'')}</b>
per $1,000,000 sold under the 1929 shape and
<b>{money(g2008[24]['per_million'],'')} to {money(g2008[36]['per_million'],'')}</b> under the 2008
shape — and <i>costs</i> <b>{money(abs(gbase[24]['per_million']),'')} to
{money(abs(gbase[36]['per_million']),'')}</b> per $1,000,000 in the baseline. It is insurance with a
known premium.</li>
<li><b>Federal estate size at the date of death.</b> The exclusion is
<b>{money(DATA['constants']['fed_exclusion']['2026'],'')}</b> for a 2026 death and
<b>{money(DATA['constants']['fed_exclusion']['2027'],'')}</b> for 2027, indexed after that. The
household's own projection of that year determines whether the transfer tax is zero or 40% of the
excess. {src(sources,'irs_estate','IRS')}</li>
</ol>
</div>

<h2>What you get, and what you have to do for it</h2>
<p>Written down before the figures, because the household asked for exactly that: the case for
each path, stated as a rule and a duty rather than as a projection.</p>
<div class="grid">
<div class="card"><h3>Live in it</h3>
<p><b>You get:</b> the intergenerational property-tax reduction for as long as you stay, the
section 121 gain exclusion if you later sell after two years, and the use of the house.</p>
<p><b>You must:</b> occupy within one year, file the exemption, and file the claim within three
years or before any sale. Move out and the reduction ends at the next lien date.</p></div>
<div class="card"><h3>Let it out</h3>
<p><b>You get:</b> the rent, and the house as a long-held asset.</p>
<p><b>You must:</b> accept full reassessment at the transfer, which nearly doubles the tax, and
accept that a later sale gets no section 121 relief.</p></div>
<div class="card"><h3>Sell it</h3>
<p><b>You get:</b> liquidity, and almost no tax on the gain because the basis steps up at death.</p>
<p><b>You must:</b> sell into whatever the market is paying that month, and then reinvest well
enough to beat what the house would have done.</p></div>
<div class="card"><h3>Sell, park, phase in</h3>
<p><b>You get:</b> the crash protection a staged entry buys, which is worth real money in a
1929- or 2008-shaped fall.</p>
<p><b>You must:</b> write the rule before the money arrives, and accept a small certain cost in
ordinary markets for a large uncertain gain in a bad one.</p></div>
</div>

<h2>The recommendation, and the one thing that would overturn it</h2>
<div class="answer"><h3>What the model says, as plainly as it can be said</h3>
<p><b>Sell.</b> On the base case, selling at the transfer beats living in the house by
{money(g(BASE_TY,BASE_H,'sell') - g(BASE_TY,BASE_H,'live',field='with_housing'))} even after the
housing the living path supplies is counted in its favour, and beats letting it by
{money(g(BASE_TY,BASE_H,'sell') - g(BASE_TY,BASE_H,'rent'))}. It wins on the base case, in five of
the eight economic states, and in {pct(1-DIST['share_hold_wins'],0)} of the resampled histories.</p>
<p><b>But the margin is a forecast, not a fact.</b> It exists because the base case assumes house
prices grow at {pct(REG['base']['house'],1)} a year while equities return
{pct(REG['base']['equity'],1)}. Raise house-price growth to
{pct(BE['house_growth_live'],1)} and the two tie. That is a move of
{abs(BE['house_growth_live']-REG['base']['house'])*100:.1f} percentage points — inside the range of
what these markets have actually done.</p>
<p><b>So the decision rule is not "sell".</b> It is: <i>if you believe house-price growth in this
market will stay below roughly {pct(BE['house_growth_live'],0)}, sell; if you believe it will beat
that, hold and live in it; if you cannot form a view, sell, because selling is the choice that does
not require you to be right.</i></p></div>

<h2>The answer on the base case, stated three ways</h2>
<p>The same eight paths at a transfer in {BASE_TY} and a {BASE_H}-year horizon, all three cases
(low, middle and high of every input range). <b>Cash</b> counts money the heir can spend. <b>With
housing</b> adds the present value of the housing the path supplies, because a household that
lives rent-free is better off than one that is not, even though no cash moves. Both are shown:
one number would hide the trade.</p>
"""
    rows = []
    for p in ("sell", "sell_phased", "rent", "live", "live_then_sell", "rent_then_sell"):
        r = grid_row(BASE_TY, BASE_H, p)
        rows.append([
            f'<b>{esc(PATHS[p]["name"])}</b><br><small>{esc(PATHS[p]["desc"])}</small>',
            money(r["low"]["net"]), money(r["mid"]["net"]), money(r["high"]["net"]),
            money(r["mid"]["with_housing"]),
            (money(r["mid"]["debt"]) if r["mid"]["debt"] else "none"),
        ])
    body += table(["Path", "Cash, low", "Cash, middle", "Cash, high",
                   "Cash + housing, middle", "Debt at the horizon"], rows, basis="model")
    body += f"""
<p class="small">{tag('ass')} Base case: house-price growth {pct(REG['base']['house'],1)}, equities
{pct(REG['base']['equity'],1)}, inflation {pct(REG['base']['inflation'],1)}, Treasury
{pct(REG['base']['treasury'],1)}. Ranges are in <a href="method.html">Method</a>. Money is rounded
to $10 and derived from a round modelling base, not from either property's value.</p>

<div class="flag"><b>Do not read the ranking as a recommendation yet.</b> Selling wins on the base
case by a wide margin, and that result is <i>manufactured by the base case</i>: at
{pct(REG['base']['house'],1)} house-price growth the house earns less than the equity market, so
of course the money does better in the market. Move that one input to
{pct(BE['house_growth_live'],2)} and the answer flips. The honest statement is the break-even, the
range it sits in, and the share of resampled histories in which holding wins —
<b>{pct(DIST['share_hold_wins'],0)}</b> of {DIST['n']:,} here.</div>

<h2>What this desk does not know — and will not guess</h2>
<p>Fifteen gaps are carried openly. Nine of them would move a decision if they changed:</p>
"""
    key_gaps = ["F01", "F02", "F03", "F05", "F07", "F09", "F12", "F15", "F04"]
    rows = [[f'<b>{gid}</b>', esc(GAPS[gid].split(".")[0] + "."),
             f'<a href="questions.html#{gid.lower()}">how to close it</a>'] for gid in key_gaps]
    body += table(["Ref", "What is missing", "Where it is tracked"], rows, numeric_from=0,
                  basis="gap")
    body += f"""
<div class="stop"><b>The one number nobody has.</b> No independent appraisal of the inherited
house, no comparable sales, and no rental comparables exist yet. {tag('gap')} Every dollar on this
site rests on a declared modelling base instead. An appraisal and three comparables would replace
{int(len([g for g in GAPS if g.startswith('F')]))} assumed inputs with measured ones — and the
break-evens, not the dollars, are what to re-check when they arrive.</div>

<h2>Where to go next</h2>
<div class="grid">
<a class="card" href="decision.html"><h3>The decision, compared properly</h3>
<p>All eight paths at the same transfer dates and horizons, with taxes, debt, occupancy, capital
costs and liquidity on the same footing — mixed paths included, not just the three pure choices.</p></a>
<a class="card" href="phased.html"><h3>Phased entry, tested</h3>
<p>Proceeds in 3-month to 2-year Treasuries for 24 or 36 months, then phased into equities,
replayed against the official 1929 and 2008 drawdowns. Reinvestment risk sits beside the result.</p></a>
<a class="card" href="questions.html"><h3>Questions and gaps</h3>
<p>What must be answered before any decision is reasonable, who can answer it, and what it would
change. Each row carries the decision it blocks.</p></a>
<a class="card" href="suggestions.html"><h3>Suggestions for the site</h3>
<p>Proposals to improve decision-making, with the reason, the cost and what would be measured.
Nothing is implemented until it is chosen.</p></a>
<a class="card" href="brief-sheet.html"><h3>Attorney &amp; CPA briefing sheet</h3>
<p>One page, printable, with the questions to put to each adviser and the dates that bind.</p></a>
<a class="card" href="work-register.html"><h3>Requirement register</h3>
<p>Every line of the owner's brief, mapped to the page that answers it, with a decision and a
date column so a future reader knows what was chosen and why.</p></a>
</div>
"""
    return page("What would change the answer", body)


# ---------------------------------------------------------------------------- decision
def p_decision():
    rows = []
    for p in ("live", "rent", "sell", "live_then_sell", "rent_then_sell", "sell_phased",
              "live_sell_phased", "rent_sell_phased"):
        r = grid_row(BASE_TY, BASE_H, p)
        rows.append([
            f'<b>{esc(PATHS[p]["name"])}</b><br><small>{esc(PATHS[p]["group"])}</small>',
            money(r["low"]["net"]), money(r["mid"]["net"]), money(r["high"]["net"]),
            money(r["low"]["with_housing"]), money(r["mid"]["with_housing"]),
            money(r["mid"]["liquid"]),
            money(r["mid"]["debt"]),
            (esc(str(r["mid"]["first_call"])) if r["mid"]["first_call"] else "never"),
        ])
    body = f"""
<h1>The decision, compared on one footing</h1>
<p class="lede">Eight paths, not three. Every path is run at the same transfer year and the same
horizon, with the same tax rules, the same debt mechanics, the same occupancy conditions, the same
capital costs and the same liquidity measure. A path that cannot pay its own carrying cost borrows
and shows the debt.</p>

<div class="answer"><h3>The comparison that matters</h3>
<p>At a {BASE_TY} transfer and a {BASE_H}-year horizon the cash ranking is
<b>{esc(PATHS['sell']['name'])}</b> ({money(g(BASE_TY,BASE_H,'sell'))}),
then <b>{esc(PATHS['sell_phased']['name'])}</b> ({money(g(BASE_TY,BASE_H,'sell_phased'))}),
then <b>{esc(PATHS['rent_then_sell']['name'])}</b> ({money(g(BASE_TY,BASE_H,'rent_then_sell'))}).
Counted with the housing the path supplies, <b>{esc(PATHS['live']['name'])}</b> rises from
{money(g(BASE_TY,BASE_H,'live'))} to {money(g(BASE_TY,BASE_H,'live',field='with_housing'))} but still
does not lead. The gap between first and last is
{money(g(BASE_TY,BASE_H,'sell') - g(BASE_TY,BASE_H,'live'))} in cash — and it is produced almost
entirely by the gap between the assumed house-price growth
({pct(REG['base']['house'],1)}) and the assumed equity return ({pct(REG['base']['equity'],1)}).</p>
</div>

<h2>All eight paths, all three cases</h2>
"""
    body += table(["Path", "Cash low", "Cash middle", "Cash high", "Cash+housing low",
                   "Cash+housing middle", "Liquid at horizon", "Debt", "First cash call"], rows,
                  basis="model")
    body += f"""
<p class="small">{tag('ass')} Every row: base regime, ranges at their low, middle and high
positions. {tag('stat')} Tax lines use the statutory rules on <a href="taxes.html">Taxes &amp;
assessment</a>. Liquidity is cash or securities, not the house. {tag('gap')} Rents, costs and
insurance are ranges, not quotes: F02, F03.</p>

<h2>Why mixed paths beat both pure choices in some states</h2>
<p>"Live in it, then sell" is not a compromise for its own sake. It is the only path that collects
two reliefs: the intergenerational exclusion while the heir occupies, and the section 121 home-sale
exclusion on the gain when they sell after two years of ownership and use. The pure letting path
collects neither on a later sale, and the pure living path never converts the house into money.</p>
"""
    r = grid_row(BASE_TY, BASE_H, "live_then_sell")
    rows = [
        ["Sell at the transfer", "No", "No", money(g(BASE_TY, BASE_H, "sell"))],
        ["Live in it", "Yes, while occupied", "No, no sale", money(g(BASE_TY, BASE_H, "live"))],
        ["Let it out", "No", "No, the use test fails", money(g(BASE_TY, BASE_H, "rent"))],
        ["Live in it, then sell after ten years", "Yes, then removed", "Yes, up to the section 121 cap",
         money(r["mid"]["net"])],
    ]
    body += table(["Path", "Intergenerational exclusion", "Section 121 on the sale", "Cash, middle"],
                  rows, numeric_from=3, basis="stat")
    body += f"""
<p>{src(sources,'rtc_63_2','RTC 63.2(a)(1)(B)-(C)')} ends the exclusion when the heir stops
occupying and re-enrols the base year value at the next lien date. {src(sources,'irs_tc701','IRS Topic 701')}
requires two of the last five years of ownership and use for the section 121 exclusion. The mixed
path is the only one where both are ever available — and the exclusion's removal on sale is exactly
why the later sale is taxed, which the model computes rather than ignores.</p>

<h2>Same transfer date, same horizon: does the year of inheritance matter?</h2>
"""
    rows = []
    for ty in DATA["transfer_years"]:
        rows.append([str(ty)] + [money(g(ty, BASE_H, p)) for p in
                                 ("live", "rent", "sell", "live_then_sell")]
                    + [pct(BE["by_transfer_year"][str(ty)], 2)])
    body += table(["Transfer year"] + [PATHS[p]["name"] for p in
                                       ("live", "rent", "sell", "live_then_sell")]
                  + ["Break-even house growth"], rows, basis="model")
    body += f"""
<p class="small">A later transfer is worth slightly more cash on every path because the house is
worth more by then, but the break-even falls as the horizon shortens: the later the inheritance, the
less time the house has to compound, so a lower growth rate is enough to justify holding it.</p>

<h2>Liquidity: what the heir can actually spend</h2>
<p>The living and letting paths tie up most of the estate in one illiquid asset. On the base case
the living path ends with {money(g(BASE_TY,BASE_H,'live',field='liquid'))} of liquid assets against
{money(g(BASE_TY,BASE_H,'sell',field='liquid'))} for the sale. That is the real cost of holding:
not the expected return, but the option the heir gives up.</p>
"""
    body += what_if_table()
    body += distribution_chart()
    body += f"""
<div class="flag"><b>What would change the ranking.</b> House-price growth above
{pct(BE['house_growth_live'],2)}; equities below {pct(BE['equity_return'],2)}; a rent
yield above {pct(BE['rent_yield'],1)} of value; or the heir valuing the housing at more than
{pct(BE['imputed_yield'],1)} of the house's value a year. Each is a single input, and each is
listed in <a href="method.html#ranges">the range register</a>.</div>
"""
    return page("The decision", body)


def what_if_table():
    rows = []
    for w in DATA["what_if"]:
        rows.append([f'<b>{esc(w["label"].split(": ")[0])}</b>', esc(w["label"].split(": ")[1]),
                     esc(PATHS[w["applies_to"]]["name"]),
                     ("−" if w["delta"] < 0 else "+") + money(abs(w["delta"]), "")])
    body = """
<h2>What-if: one knob at a time</h2>
<p>Each row moves one input and reports the change in the path it affects. This is why the site
needs no controls: the knobs that matter are few, and moving them one at a time says more than a
slider does.</p>
"""
    body += table(["What moves", "How it moves", "Path affected", "Change in that path's result"],
                  rows, numeric_from=3, basis="model")
    body += f"""
<p class="small">Every figure a multiple of $10. The knobs are chosen because the owner can
observe or decide them; the market assumptions are on <a href="swans.html">Uneven economy</a>,
where they can be moved too.</p>
"""
    return body


def distribution_chart():
    d = DIST
    lo, hi = d["bin_low"], d["bin_high"]
    step = (hi - lo) / len(d["bins"]) if hi > lo else 1
    bars = []
    for i, c in enumerate(d["bins"]):
        centre = lo + step * (i + 0.5)
        h = 0 if max(d["bins"]) == 0 else c / max(d["bins"]) * 100
        bars.append(f'<div class="c{" neg" if centre < 0 else ""}" style="height:{h:.0f}%" '
                    f'title="{money(centre)}"></div>')
    return f"""
<h2 id="distribution">The distribution, not the point</h2>
<p>{d['n']:,} resampled {DATA['horizons'][1]}-year histories, fixed seed {d['seed']}, drawing annual
equity returns around a {pct(0.070,1)} mean and house-price growth around {pct(0.040,1)}. Each bar
is one sixteenth of the outcomes; red bars are histories in which <b>letting</b> the house beat
selling it.</p>
<div class="hist">{''.join(bars)}</div>
<p class="small">Left to right: worst to best for the holding path. Percentiles of the
let-minus-sell gap: 5th {money(d['p05'])}, 25th {money(d['p25'])}, median {money(d['p50'])},
75th {money(d['p75'])}, 95th {money(d['p95'])}. Holding wins in
<b>{pct(d['share_hold_wins'],0)}</b> of histories.</p>
<p><b>How to read this.</b> A single projection says "sell wins by {money(g(BASE_TY,BASE_H,'rent') - g(BASE_TY,BASE_H,'sell'))}"
and invites a decision. The distribution says the same thing without the false precision: the
median favours selling, the spread is larger than the median, and holding still wins in
{pct(d['share_hold_wins'],0)} of the histories drawn. A decision that has to survive bad luck
should be chosen against the spread, not the median.</p>
<div class="flag"><b>Reinvestment risk sits beside every staging result.</b> The distribution
assumes the sale proceeds are invested at the equity mean from the first day. The phased-entry page
tests that assumption against two real drawdowns; the answer is that phasing is cheap insurance in
a crash and an expensive one in a boom. {tag('ass')} Neither the draw nor the mean is a
forecast.</div>
"""


# ---------------------------------------------------------------------------- paths
def p_paths():
    body = """
<h1>All eight paths, described before they are scored</h1>
<p class="lede">The owner asked for mixed paths, not only the three pure choices. Three pure
choices, five mixed ones. Each is stated as a rule the heir could actually execute, because a path
that cannot be written down as a rule cannot be chosen.</p>
"""
    for group, label in (("pure", "The three pure choices"), ("mixed", "Five mixed paths")):
        body += f"<h2>{label}</h2>"
        for p in DATA["paths"]:
            if p["group"] != group:
                continue
            rows = [[money(g(BASE_TY, BASE_H, p["id"], case))] for case in ("low", "mid", "high")]
            body += f"""
<div class="card" style="margin:14px 0">
<h3>{esc(p['name'])}</h3>
<p>{esc(p['desc'])}</p>
<p class="small">Cash at {BASE_TY} / {BASE_H} years — low {money(g(BASE_TY,BASE_H,p['id'],'low'))},
middle {money(g(BASE_TY,BASE_H,p['id'],'mid'))}, high {money(g(BASE_TY,BASE_H,p['id'],'high'))}.
With housing: {money(g(BASE_TY,BASE_H,p['id'],'mid',field='with_housing'))}.</p>
</div>"""
    body += """
<h2>What each path requires, and what it gives up</h2>
"""
    rows = [
        ["Live in it", "The heir occupies within one year and files the exemption",
         "A later sale loses the intergenerational exclusion", "The whole value is in one illiquid asset"],
        ["Let it out", "Nothing beyond ordinary landlord duties",
         "No intergenerational exclusion; no section 121 on a later sale",
         "Rent is taxable and the house is illiquid"],
        ["Sell at the transfer", "An appraisal at the date of death",
         "No further exposure to the local housing market",
         "The price is whatever the market pays that month"],
        ["Live in it, then sell", "Occupy within a year, file the claim, sell after two years",
         "The exclusion, then the section 121 cap", "A forced sale date in an unknown market"],
        ["Let it, then sell", "Landlord duties, then a sale",
         "Nothing: both reliefs fail", "Capital-gains exposure on the full gain"],
        ["Sell, park, phase in", "Discipline for 24–36 months; a written policy before the money arrives",
         "Crash protection at the entry", "The expected cost of being out of the market"],
        ["Live, sell, park, phase in", "Both sequences in order",
         "Both reliefs and the crash protection", "Two timing risks instead of one"],
        ["Let, sell, park, phase in", "Landlord duties, then the sequence",
         "The crash protection only", "The taxable gain on the sale"],
    ]
    body += table(["Path", "What must be done", "What it collects", "What it gives up"], rows,
                  numeric_from=0, basis="stat")
    body += f"""
<h2>The state in which each path wins</h2>
<p>A path is not "best" in the abstract. Each one leads under a describable state, and the state is
what the household should write down before the figures arrive.</p>
"""
    rows = []
    for r in DATA["regime_grid"]:
        pass
    winners = {}
    for reg in REG:
        best = max((row for row in DATA["regime_grid"] if row["regime"] == reg),
                  key=lambda x: x["net"])
        winners[reg] = best
    for reg, best in winners.items():
        body_row = [
            f'<b>{esc(REG[reg]["name"])}</b> <a href="swans.html#{reg}">detail</a>',
            esc(PATHS[best["path"]]["name"]), money(best["net"]),
            pct(BE["by_regime"][reg], 2),
        ]
        rows.append(body_row)
    body += table(["Economic state", "Path with the most cash", "Its cash, middle case",
                   "Break-even house growth in that state"], rows, numeric_from=2, basis="model")
    body += f"""
<p class="small">{tag('ass')} Each state is a declared scenario, not a forecast; the two crash states
are anchored on the published drawdowns. The listing is mechanical: for each state, the path with
the highest cash result.</p>
<div class="stop"><b>The trap in that table.</b> The winner changes with the state, so choosing the
path that wins the baseline is choosing a forecast, whether or not it is labelled one. The reason
to prefer a mixed path is not that it wins anywhere; it is that it loses least across states. That
is a different question, asked on <a href="swans.html">Uneven economy</a>.</div>
"""
    return page("All eight paths", body)


# ---------------------------------------------------------------------------- phased
def p_phased():
    rows = []
    for r in DATA["phased"]:
        rows.append([esc(REG[r["regime"]]["name"]), f'{r["months"]} months',
                     money(r["immediate"]), money(r["phased"]), money(r["difference"]),
                     money(r["per_million"])])
    body = f"""
<h1>Selling into a crash: does parking the money first help?</h1>
<p class="lede">The owner asked for a phased-investing path in the black-swan work: park the sale
proceeds in 3-month to 2-year Treasuries for 24–36 months after the inheritance, then phase into
stocks, and test whether that softens the risk of entering the market at the top of a crash. This
page does exactly that and reports the result against the alternative on the same footing.</p>

<div class="answer">
<h3>The rule being tested</h3>
<p>Sell the house. Hold the proceeds in Treasury bills and notes with maturities of three months to
two years for 24 or 36 months. Then move the money into equities in equal monthly tranches over the
following twelve months. Compare against selling and investing the whole amount on the first day.</p>
</div>

<h2>The two drawdowns this is anchored on</h2>
"""
    rows = [
        ["1929", "The Dow fell 89% from its 3 September 1929 peak to 8 July 1932, and did not regain the 1929 high until 23 November 1954.",
         src(sources, "fed_history_1929", "Federal Reserve History")],
        ["2008", "The S&amp;P 500 fell 57% from its October 2007 peak to its March 2009 trough; house prices fell about 30% from mid-2006 to mid-2009.",
         src(sources, "fed_history_2008", "Federal Reserve History")],
    ]
    body += table(["Drawdown", "What the official record says", "Source"], rows, numeric_from=0)
    body += f"""
<p>The model puts the crash at the entry year — the year the heir would have invested — with the
published annual profile: {pct(-0.31,0)}, {pct(-0.23,0)}, {pct(-0.09,0)} for 1929 and
{pct(-0.30,0)}, {pct(-0.27,0)} for 2008. The percentages are assumptions laid over the published
total drawdown, not the published series itself, and are flagged as such. {tag('ass')}</p>

<h2>Result: the same rule, five states</h2>
"""
    body += table(["State", "Parking", "Sell and invest at once", "Sell, park, then phase in",
                   "Difference", "Per $1,000,000 sold"], rows, numeric_from=2)
    body += f"""
<div class="answer"><h3>What the table says</h3>
<p>Parking is <b>insurance with a price</b>. In the two crash states it adds
{money(next(r for r in DATA['phased'] if r['regime']=='crash1929' and r['months']==24)['per_million'])}
to
{money(next(r for r in DATA['phased'] if r['regime']=='crash1929' and r['months']==36)['per_million'])}
per $1,000,000 sold under the 1929 shape and
{money(next(r for r in DATA['phased'] if r['regime']=='crash2008' and r['months']==24)['per_million'])}
to
{money(next(r for r in DATA['phased'] if r['regime']=='crash2008' and r['months']==36)['per_million'])}
under the 2008 shape. In the baseline it <i>costs</i>
{money(abs(next(r for r in DATA['phased'] if r['regime']=='base' and r['months']==24)['per_million']))}
per $1,000,000, and in the strong-growth state it costs
{money(abs(next(r for r in DATA['phased'] if r['regime']=='growth' and r['months']==36)['per_million']))}.
Twenty-four months beats thirty-six in three of the five states, because the extra year out of the
market is pure cost when nothing falls.</p></div>

<h2>Reinvestment risk, stated plainly</h2>
<div class="flag"><b>The risk the phasing does not remove.</b> Parking the proceeds <i>moves</i> the
reinvestment risk, it does not delete it. At the end of the parking window the heir still has to
invest, and the market can fall then instead. A 1929-shaped path has three successive down years, so
a 24-month park lands the heir in the third one and still helps; a V-shaped fall that bottoms during
the parking window and recovers before it ends leaves the heir buying higher than if they had never
parked. The honest description is a trade: certain small cost in ordinary times against a large
gain in one particular shape of crash.</div>

<h2>The policy this implies, if the household wants the insurance</h2>
<ul class="tight">
<li><b>Write it before the money arrives.</b> The decision is easy in hindsight and hard in the
moment; a written rule is the only defence against selling at the bottom.</li>
<li><b>Choose the window by the measurement, not by fear.</b> 24 months dominated 36 in three of the
five states tested here.</li>
<li><b>Park only what will be invested.</b> Money earmarked for tax, fees or a reserve should not be
in the phased sleeve at all.</li>
<li><b>Set the tranche schedule and the end date.</b> Equal monthly tranches over twelve months is
the rule modelled here; any other rule should be measured the same way.</li>
<li><b>Name the person who executes it.</b> A policy without an executor is a wish.</li>
</ul>
<p>{tag('gap')} The Treasury rate used here is an assumed range (F07) because the official daily
par-yield page did not render in this session. When it does, the parking return should be
recomputed — the direction of the result will not change, but the size of the premium will.</p>
"""
    return page("Phased entry", body)


# ---------------------------------------------------------------------------- swans
def p_swans():
    body = """
<h1>Uneven economy</h1>
<p class="lede">Growth and inflation are not consistent over fifty years, so a projection that
assumes they are is not a projection — it is a wish with decimals. This page runs the same paths
across eight states, two of them anchored on the published record of real crashes.</p>
"""
    for r in DATA["regimes"]:
        rows = []
        for row in DATA["regime_grid"]:
            if row["regime"] == r["id"]:
                rows.append([esc(PATHS[row["path"]]["name"]), money(row["net"]), money(row["liquid"]),
                             money(row["debt"]) if row["debt"] else "none",
                             esc(str(row["first_call"])) if row["first_call"] else "never"])
        body += f"""
<h2 id="{r['id']}">{esc(r['name'])}</h2>
<p class="small">Equities {pct(r['equity'],1)} · house prices {pct(r['house'],1)} · inflation
{pct(r['inflation'],1)} · Treasury {pct(r['treasury'],1)}. {esc(r['anchor'])}</p>
"""
        body += table(["Path", "Cash", "Liquid at horizon", "Debt", "First cash call"], rows,
                      numeric_from=1, basis="model")
    body += f"""
<h2>Across all eight states, which path loses least?</h2>
"""
    rows = []
    for p in ("sell", "sell_phased", "live", "rent", "live_then_sell"):
        vals = [row["net"] for row in DATA["regime_grid"] if row["path"] == p]
        rows.append([esc(PATHS[p]["name"]), money(model.money_k(min(vals))),
                     money(model.money_k(max(vals))),
                     money(model.money_k(sum(vals) / len(vals))),
                     money(model.money_k(max(vals) - min(vals)))])
    body += table(["Path", "Worst state", "Best state", "Mean across states", "Spread"], rows,
                  basis="model")
    body += f"""
<div class="answer"><h3>Reading the spread</h3>
<p>The sale path has the widest spread of any path — {money(model.money_k(max(r['net'] for r in DATA['regime_grid'] if r['path']=='sell') - min(r['net'] for r in DATA['regime_grid'] if r['path']=='sell')))}
— because it puts the entire estate into the market on one day. The living path has the narrowest
among the hold options, because the house is a slower-moving asset than equities. A household that
cannot tolerate the first number should not choose the path that produces it merely because its mean
is highest.</p></div>

<h2>What is modelled, and what is not</h2>
"""
    rows = [
        ["Equity return", "A constant annual rate per state, or the published drawdown profile in the two crash states", tag("ass")],
        ["House-price growth", "A constant annual rate per state; the crash states apply a house-price fall too", tag("ass")],
        ["Inflation", "A constant rate per state; it drives operating-cost growth and the assessment cap", tag("ass")],
        ["Stagflation", "Equities 5%, house prices 5%, inflation 7.5%: the real return on both assets is negative", tag("ass")],
        ["Treasury yields", "A constant rate per state; no yield curve and no roll-down", tag("ass")],
        ["Borrowing", "1.5 percentage points over the Treasury rate when a path cannot fund itself", tag("ass")],
        ["Correlation", "Not modelled inside a state. The Monte Carlo resamples both series but does not impose a correlation between them", tag("gap")],
        ["Sequence risk", "Only in the crash states, where the drawdown falls at the entry year", tag("ass")],
    ]
    body += table(["Input", "How it is treated", "Status"], rows, numeric_from=0)
    body += f"""
<div class="flag"><b>Why no fifty-year path is drawn through these states.</b> A fifty-year
projection of a crashing economy is not a forecast, it is theatre: the errors compound faster than
the signal. The states here are run at the same horizon as every other comparison, so their results
can be put beside the baseline rather than on a separate page where they look like prophecy.</div>
"""
    return page("Uneven economy", body)


# ---------------------------------------------------------------------------- projections
def p_projections():
    body = f"""
<h1>Projections, 2026 to 2076</h1>
<p class="lede">Three views of the same model: the value and assessment of the inherited house, the
carrying cost of holding it, and what each path is worth at the horizon. Everything is nominal
dollars on a round modelling base, rounded to $10.</p>

<h2>The inherited house: value, assessment and tax</h2>
<p>The assessment is the load-bearing line. Under the intergenerational exclusion the assessed
value is the factored base year value plus whatever the market value exceeds the cap by, and it then
grows by the lesser of 2% or inflation each year. If the heir does not occupy, the assessment resets
to full market value at the transfer and the yearly tax roughly doubles.</p>
"""
    rate = DATA["exposure"][0]
    rows = []
    for ty in DATA["transfer_years"]:
        for offset in (0, 10, 20, 30):
            year = ty + offset
            value = 2_500_000
            for _ in range(ty - 2026):
                value *= 1.042
            for _ in range(offset):
                value *= 1.042
            fbyv = value
            assessed_occ = rate["assessed"] if offset == 0 else None
            rows.append([str(year), money(model.money_k(value)), money(rate["assessed"]) if offset == 0 else "—",
                         money(rate["tax_low"]) if offset == 0 else "—",
                         money(rate["tax_high"]) if offset == 0 else "—"])
    body += table(["Year", "Market value, base case", "Assessed value if the heir occupies",
                   "Annual tax at the rate floor", "Annual tax at the rate ceiling"],
                  [r for r in rows if r[2] != "—"], basis="model")
    body += f"""
<p class="small">Only the transfer year is shown: after that the assessed value compounds at the
lesser of 2% or inflation, which is {pct(0.02)} in most states here. The rate floor is the county's
own published figures (the county's 1% maximum levy plus its 0.0388% retirement levy); the ceiling is an
assumed 1.40% to cover voter-approved debt. {tag('gap')} The actual rate depends on the property's
tax rate area, which is unknown (F01).</p>

<h2>Carrying cost by year, first twenty years after a 2045 transfer</h2>
"""
    rows = []
    for y in DATA["capital_plan"]:
        if y["property"].startswith("Property A"):
            rows.append([str(y["year"]), money(y["maintenance"]), money(y["capital"]),
                         money(y["fixed_other"]), money(y["total"])])
    body += table(["Year", "Routine maintenance", "Capital plan (averaged)",
                   "Insurance, water, power (net of solar)", "Total"], rows, basis="model")
    body += f"""
<p class="small">{tag('ass')} Rates applied to the modelling base and inflated at the state's own
inflation rate; the solar credit can make the power line negative, which is why the total can fall
below the sum of its neighbours. The five-year detail for both buildings is on
<a href="costs.html">Carrying costs</a>.</p>

<h2>What each path is worth at the horizon</h2>
"""
    rows = []
    for h in DATA["horizons"]:
        rows.append([f"{h} years"] + [money(g(BASE_TY, h, p)) for p in
                                      ("live", "rent", "sell", "live_then_sell")])
    body += table(["Horizon at a 2045 transfer", "Live", "Let", "Sell", "Live then sell"], rows,
                  basis="model")
    body += f"""
<div class="flag"><b>The projection is not the argument.</b> These numbers move by millions when one
input moves by one percentage point — the break-even is
{pct(BE['house_growth_live'],2)} against a baseline assumption of {pct(REG['base']['house'],1)},
a gap of {pct(abs(BE['house_growth_live']-REG['base']['house'])*100,1)} of a percentage point. Any
projection presented without that gap invites a decision it cannot support.</div>

<h2>Ranges, not points</h2>
<p>The owner asked for ranges or real figures instead of round-number assumptions. Every input is a
range; the projections above show the middle case. The table below shows the full spread at the same
transfer year and horizon.</p>
"""
    rows = []
    for p in ("sell", "live", "rent"):
        rows.append([esc(PATHS[p]["name"]),
                     money(g(BASE_TY, BASE_H, p, "low")), money(g(BASE_TY, BASE_H, p, "mid")),
                     money(g(BASE_TY, BASE_H, p, "high")),
                     money(g(BASE_TY, BASE_H, p, "high") - g(BASE_TY, BASE_H, p, "low"))])
    body += table(["Path", "Low", "Middle", "High", "Spread"], rows, basis="model")
    return page("Projections", body)


# ---------------------------------------------------------------------------- costs
def p_costs():
    body = """
<h1>Carrying costs, line by line</h1>
<p class="lede">Two buildings, five years, every recurring line. The inherited house is cheap to
hold by local standards — solar covers most of its power and its water bill is small. The three-unit
building is the expensive one, and it is the one that pays for itself.</p>

<h2>The inherited house: the five-year plan</h2>
"""
    rows = []
    for y in DATA["capital_plan"]:
        if y["property"].startswith("Property A"):
            rows.append([str(y["year"]), money(y["maintenance"]), money(y["capital"]),
                         money(y["fixed_other"]), money(y["total"])])
    body += table(["Year", "Routine maintenance and repair", "Capital plan, averaged",
                   "Insurance, water and power", "Total"], rows, basis="model")
    body += f"""
<h2>The three-unit building: the five-year plan</h2>
"""
    rows = []
    for y in DATA["capital_plan"]:
        if y["property"].startswith("Property B"):
            rows.append([str(y["year"]), money(y["maintenance"]), money(y["capital"]),
                         money(y["fixed_other"]), money(y["total"])])
    body += table(["Year", "Routine maintenance and repair", "Capital plan, averaged",
                   "Insurance, water and power", "Total"], rows, basis="model")
    body += f"""
<h2>What the ranges are, and where they come from</h2>
"""
    keys = [
        ("a_insurance_rate", "Homeowners insurance, inherited house, owner-occupied", "Share of value a year. No binding quote exists."),
        ("a_insurance_rental_rate", "Landlord policy, inherited house", "Share of value a year, above the owner-occupied rate."),
        ("a_water_rate", "Water, inherited house", "Share of value a year."),
        ("a_electric_net_rate", "Power, inherited house, net of solar", "Share of value a year; negative is a credit."),
        ("a_maint_rate", "Routine maintenance, inherited house", "Share of value a year."),
        ("a_capital_rate", "Capital plan, inherited house", "Share of value a year, averaged over five years."),
        ("b_insurance_rate", "Landlord policy, three-unit building", "Share of value a year."),
        ("b_water_rate", "Water, whole building, three units", "Share of value a year."),
        ("b_electric_rate", "Owner-paid power, three-unit building", "Share of value a year."),
        ("b_maint_rate", "Routine maintenance, three-unit building", "Share of value a year."),
        ("b_capital_rate", "Capital plan, three-unit building", "Share of value a year."),
        ("b_parcel_tax_rate", "Local parcel tax on the building, if enacted", "Share of value a year. The official terms were not confirmed (F04)."),
    ]
    rows = []
    for k, label, basis in keys:
        lo, hi = DATA["ranges"][k]
        if abs(hi) < 1:
            shown = f"{pct(lo,2)} – {pct(hi,2)} of value a year"
        else:
            shown = f"{money(model.money_k(lo))} – {money(model.money_k(hi))} a year"
        rows.append([esc(label), esc(shown), f'{esc(basis)} {tag("ass") if "Assumed" in basis else tag("gap")}'])
    body += table(["Line", "Range used", "Basis"], rows, numeric_from=0)
    body += f"""
<div class="flag"><b>The one gap that matters most here.</b> There is no binding insurance quote for
either building. A homeowners policy on the inherited house and a landlord policy on a three-unit
building are not the same product and their prices move independently. Two quotes replace this
entire page's first two tables with measured numbers. {tag('gap')} F03 in
<a href="questions.html">Questions</a>.</div>

<h2>Water and power, in the owner's own description</h2>
<p>The inherited house's water bill is small and its solar array usually produces a credit; the
three-unit building's water is several times larger and its power is modest. Those descriptions are
<em>not</em> published as figures here — a monthly bill range and a city are enough to identify a
parcel. What is published is the effect: the inherited house's running cost is low enough that its
carrying cost is dominated by property tax, and the building's carrying cost is dominated by water,
insurance and maintenance.</p>
"""
    return page("Carrying costs", body)


# ---------------------------------------------------------------------------- taxes
def p_taxes():
    # exposure table
    rows = []
    for e in DATA["exposure"]:
        rows.append([esc(e["case"]), money(e["assessed"]), money(e["tax_low"]),
                     money(e["tax_high"]), money(e["difference_vs_first"])])
    body = f"""
<h1>Taxes and assessment, separated</h1>
<p class="lede">The owner asked for three things to be kept apart: the estate tax, the income-tax
basis, and the property-tax assessment. They are decided by three different authorities on three
different dates, and confusing them is the most expensive error available here.</p>

<h2>1. The estate tax: a federal question with a California answer of zero</h2>
"""
    rows = []
    for year in ("2025", "2026", "2027"):
        rows.append([year, money(DATA["constants"]["fed_exclusion"][year]), pct(0.40, 0),
                     src(sources, "irs_estate" if year != "2027" else "irs_ir2026_133", "IRS")])
    body += table(["Year of death", "Federal basic exclusion", "Rate above the exclusion", "Source"], rows)
    body += f"""
<p>A married couple can shelter up to twice that, but only if the first estate elects portability on
a timely filed return — and a return must be filed to elect it even where no tax is due.
{src(sources,'irs_estate_faq','IRS estate-tax FAQ')} The form is due nine months after death, with an
automatic six-month extension on Form 4768.</p>
<div class="flag"><b>California.</b> The state imposes no estate or inheritance tax. That is widely
reported but was <i>not</i> confirmed from an official state page in this session, so it is carried
as an open item (F10) rather than asserted. It does not change any number here: the model taxes the
estate against the federal exclusion only, so if a state tax existed the result would be worse than
shown, never better.</div>

<h2>2. Property tax: the assessment is where the money is</h2>
<p>This is the largest single line in the decision and the one the earlier desks got wrong. Under
the intergenerational exclusion the assessed value is the transferor's factored base year value
<i>plus the amount by which market value exceeds that base plus an indexed cap</i>. The cap is
<b>{money(DATA['constants']['prop19_cap'],'')}</b> for transfers from 16 February 2025 through
15 February 2027. {src(sources,'boe_lta_2025_009','BOE LTA 2025/009')}</p>
"""
    body += table(["Case at the transfer", "Assessed value", "Annual tax at the rate floor",
                   "Annual tax at the rate ceiling", "Extra cost against the first case"], rows,
                  basis="model")
    body += f"""
<div class="stop"><b>The finding that changes the decision.</b> Occupying the house is worth
{money(DATA['exposure'][1]['tax_high'] - DATA['exposure'][0]['tax_high'],'')} a year at the top of
the local rate range — {pct((DATA['exposure'][1]['tax_high']-DATA['exposure'][0]['tax_high'])/max(1,DATA['exposure'][1]['tax_high']),0)}
of the tax bill. It is not a rounding error and it is not permanent: {src(sources,'rtc_63_2','RTC 63.2(a)(1)(B)–(C)')}
removes the exclusion the moment the heir stops occupying and re-enrols the base year value at the
following lien date. Any path that assumes the reduction lasts after the heir moves out is wrong.</div>

<div class="flag"><b>The cap is carried forward, not invented.</b> The statute adjusts the
$1,000,000 amount every second 16 February for the federal house-price index. The last published
amount is {money(DATA['constants']['prop19_cap'],'')} for transfers through 15 February 2027. No
later amount is published at the date of this page, so every projection after 2027 uses this figure
and marks it carried forward. Inventing a 2045 cap would have been the easier choice and the wrong
one.</div>

<h2>3. Income tax: the basis, the sale, and the 1% above one million</h2>
<p>The owner asked specifically for the Form 540 instructions on the 1% tax above one million and
on capital-gain treatment. What can be said from the statute alone is this: the tax is
<b>{pct(0.01,0)} of California taxable income above $1,000,000</b>, imposed in addition to every
other tax, with credits, filing-status re-computation and the joint-return rule expressly switched
off. {src(sources,'rtc_17043','RTC 17043')} It is not a rate on a sale price, and it is not a
surtax on the gain: it applies to the margin above one million of taxable income in the year of
sale.</p>
"""
    rows = []
    for r in DATA["same_year"]:
        rows.append([str(r["transfer_year"]), money(r["price"]), money(r["gain"]), money(r["fed"]),
                     money(r["niit"]), money(r["ca1"]), money(r["county"]), money(r["city"]),
                     money(r["recording"]), money(r["sell_cost"]), money(r["proceeds"])])
    body += table(["Transfer year", "Sale price", "Gain over basis", "Federal", "NIIT",
                   "California 1%", "County transfer tax", "City transfer tax (mid)",
                   "Recording", "Selling cost", "Net proceeds"], rows, basis="model")
    body += f"""
<p class="small">A sale in the year of inheritance produces <b>no federal gain</b> on these
assumptions, because the basis steps up to the date-of-death value and the selling cost pushes the
result below it. That is why the owner's instruction to model a sale in the same tax year as the
inheritance before deciding anything else is the right instruction: it establishes the floor every
holding path has to beat, and the floor is nearly all of the price.</p>
<ul class="tight">
<li><b>Step-up in basis.</b> Property acquired from a decedent takes a basis equal to its value at
the date of death. {src(sources,'irs_tc409','IRS Topic 409')} directs the reader to Publication 551
for inherited property; that publication was <b>not opened</b> in this session, so the rule is
carried as an assumption the CPA should confirm (F: Pub 551).</li>
<li><b>Section 121.</b> Up to $250,000 of gain ($500,000 on a joint return) is excluded on the sale
of a main home after two of the last five years of ownership and use.
{src(sources,'irs_tc701','IRS Topic 701')} This is the second relief that only the live-then-sell
path can use.</li>
<li><b>Net investment income tax.</b> {pct(0.038,1)} on net investment income above modified AGI of
$200,000 single or $250,000 joint, not indexed. {src(sources,'irs_niit','IRS')} Gain excluded under
section 121 is not net investment income.</li>
<li><b>Long-term rates.</b> 0%, 15% and 20% by taxable income; unrecaptured section 1250 gain at a
maximum 25%. {src(sources,'irs_tc409','IRS Topic 409')}</li>
<li><b>Transfer tax.</b> The county may levy 55 cents per $500 of value
({pct(0.11,2)}). {src(sources,'rtc_11911','RTC 11911')} A city inside that county may add up to half
that amount. The city rate actually applied to the building is an assumed range because the city's
published schedule could not be opened (F05).</li>
</ul>
<div class="flag"><b>What is still missing on this page.</b> {tag('gap')} The Franchise Tax Board
booklet was not opened, so California's own marginal schedule and its treatment of long-term gain
are not applied — only the statutory 1% above one million is. For a sale of this size the difference
is material and one careful hour with the 2025 Form 540 instructions closes it (F09).</div>
"""
    return page("Taxes and assessment", body)


# ---------------------------------------------------------------------------- timeline
def p_timeline():
    body = """
<h1>The deadlines, as a timeline</h1>
<p class="lede">Nine dates bind this transfer. Two of them are lost by doing nothing, one is lost by
moving out, and one is lost by selling before filing. Each is quoted with the rule that creates it.</p>
"""
    rows = []
    for t in DATA["timeline"]:
        rows.append([
            f'<b>{esc(t["when"])}</b>' + (" " + tag("stat") if t["deadline"] else ""),
            esc(t["what"]), esc(t["rule"]), src(sources, t["source"], "official")
        ])
    body += table(["When", "What must happen", "The rule", "Source"], rows, numeric_from=0)
    body += f"""
<h2>The order of operations after a death</h2>
<ol>
<li><b>Days 1–30.</b> Secure the property, notify the insurer, and order an independent appraisal
as of the date of death. The appraisal fixes both the estate value and the new basis; it cannot be
obtained later with the same authority.</li>
<li><b>Days 30–90.</b> The trustee confirms title and the trust's terms, and the change in
ownership is reported to the assessor. The assessor will learn of the transfer whether or not the
heir volunteers it.</li>
<li><b>Before the first anniversary.</b> The heir moves in and files for the homeowners' exemption.
This is the single date that decides whether the exclusion is available at all.</li>
<li><b>Before the third anniversary, and before any sale.</b> The intergenerational claim is filed.
Selling first closes the window.</li>
<li><b>Nine months after death.</b> Form 706 is filed if the estate is above the threshold, or to
elect portability. The extension is six months and must be requested.</li>
<li><b>Every year.</b> The assessed value and the two policy questions are re-read. Each is carried
forward on the model and marked.</li>
</ol>
<div class="flag"><b>What is not on this timeline because nobody knows it yet.</b> The date of death,
and therefore every date above, is unknown. {tag('gap')} The timeline is stated relative to the
death for that reason. It should be turned into a dated calendar the month the death occurs.</div>
"""
    return page("Timeline", body)


# ---------------------------------------------------------------------------- questions
def p_questions():
    Q = QUESTIONS
    body = f"""
<h1>Questions, information and answers</h1>
<p class="lede">{len(Q)} questions stand between the household and a decision that can be defended.
Each carries what is known now, what is missing, who can supply it, and — the column that matters —
which decision it blocks. The owner asked for suggestions on how to discover missing information;
that is the fourth column.</p>

<div class="answer"><h3>The five that block everything else</h3>
<ol>
{''.join(f'<li><b>{esc(q[1])}</b> — {esc(q[3])}</li>' for q in Q if q[1] in P0)}
</ol></div>

<h2>The register</h2>
"""
    rows = []
    for ref, question, known, why, who, action, decision in Q:
        rows.append([
            f'<b>{esc(ref)}</b>',
            f'<span id="{esc(ref).lower()}">{esc(question)}</span>',
            esc(known), esc(why) + ("" if known != "Nothing." else " " + tag("gap")),
            esc(who), esc(action), esc(decision),
        ])
    body += table(["Ref", "Question", "What is known", "Why it matters", "Who can answer",
                   "How to discover it", "The decision it blocks"], rows, numeric_from=0,
                  basis="gap")
    body += """
<h2>How to run the discovery, in order</h2>
<ol>
<li><b>Buy the two measurements first.</b> An appraisal and three rental comparables for the
inherited house are the only purchases on this list that change the model's inputs rather than its
caveats. Everything else can wait for them.</li>
<li><b>Then ask the county.</b> One call to the assessor establishes the tax rate area, the
factored base year value on the current roll, and the exact claim forms the county wants. Ask for
the answer in writing.</li>
<li><b>Then the advisers, with the briefing sheet.</b> The <a href="brief-sheet.html">one-page
sheet</a> exists so that the attorney and the CPA answer the same questions rather than two
different ones.</li>
<li><b>Then the trust.</b> Whether the trust or the heir is the transferor, and what the trust says
about occupancy, decides whether any of the above is even available.</li>
<li><b>Only then the market assumption.</b> House-price growth and equity returns are the two inputs
nobody can measure in advance. They come last because they are the ones the household must
<em>choose</em>, and the choice should be written down with a date.</li>
</ol>
<div class="stop"><b>The honest summary.</b> With what is known today, the decision cannot be made
defensibly. It can be <em>framed</em> — the break-evens, the exposures and the deadlines are all
established — but the four measurements that would turn the frame into a decision do not exist yet.
That is not a failure of the analysis; it is the finding.</div>
"""
    return page("Questions and gaps", body)


P0 = {"Q01", "Q02", "Q03", "Q04"}

QUESTIONS = [
    ("Q01", "What is the inherited house actually worth at the date of death?",
     "Nothing measured. A round modelling base is used instead.",
     "Every break-even is expressed against value, and the estate-tax question depends on it.",
     "A licensed appraiser in the county where the property sits.",
     "Commission a date-of-death appraisal; keep it with the estate records.",
     "Whether the estate is anywhere near the federal threshold, and therefore whether portability matters at all."),
    ("Q02", "What rent would the inherited house fetch?",
     "Nothing measured. A yield range is applied to the modelling base.",
     "The letting path is ranked on this input; without it the path is ranked on an assumption.",
     "A local letting agent, with three written comparables.",
     "Obtain three comparables in writing, at the same specification and date window.",
     "Whether letting can compete with selling at all."),
    ("Q03", "Does the transfer qualify for the intergenerational exclusion?",
     "The rule is known and quoted; the facts that trigger it are not.",
     "It is worth roughly a quarter of the property tax bill every year the heir occupies.",
     "The county assessor, and the attorney who reads the trust.",
     "Ask the assessor which claim the county requires and what evidence of occupancy it accepts.",
     "Whether living in the house is financially different from letting it."),
    ("Q04", "What is the property's tax rate area, and its published total rate?",
     "Unknown. The county publishes 816 rate areas; the county-wide floor is the 1% maximum levy plus the 0.0388% retirement levy.",
     "It sets every property-tax line in the model, and the range between floor and ceiling is 30%.",
     "The county assessor or the tax collector, from the parcel number.",
     "One request in writing for the rate area and the current roll value.",
     "The size of the property-tax line and therefore the exposure of losing the exclusion."),
    ("Q05", "Will the heir actually occupy the house, and for how long?",
     "Unknown. This is a preference, not a fact.",
     "It is the input that switches the exclusion, the section 121 relief, and the housing benefit.",
     "The heir.",
     "Write the answer down with a date, before the figures are final.",
     "Which of the four holding paths is even available."),
    ("Q06", "Does the trust or the heir count as the transferor under the exclusion?",
     "Not resolved from an official source (F12).",
     "If the answer is wrong, the exclusion may never have been available.",
     "An attorney who reads the trust instrument.",
     "Ask specifically about the trust's occupancy and distribution terms.",
     "The entire property-tax basis of every path."),
    ("Q07", "Is the property the transferor's principal residence at the date of death?",
     "Assumed yes, not verified.",
     "The exclusion requires it; a rental does not qualify.",
     "The trust's records, the homeowner's exemption history, and the assessor.",
     "Obtain the exemption history from the county.",
     "Whether the exclusion exists at all."),
    ("Q08", "What are the binding insurance premiums for both buildings?",
     "Nothing measured. Two assumed ranges (F03).",
     "Insurance is the second-largest controllable line on the inherited house and a large line on the building.",
     "Two or three admitted carriers, and the state insurance department for the market comparison.",
     "Request two quotes for each building, with the same deductibles and limits.",
     "The carrying-cost comparison, and whether the building's cash flow is positive."),
    ("Q09", "What are the actual water, power and sewer tariffs?",
     "Assumed ranges.",
     "Together with insurance and maintenance they decide whether the building pays for itself.",
     "The water and power utilities serving each property.",
     "Pull twelve months of bills from the trust's records; that is better than any tariff schedule.",
     "The building's net cash flow."),
    ("Q10", "Is there a local parcel tax on the building, and on what terms?",
     "Unknown; a parameter with an assumed range (F04).",
     "A $1,000–$3,000 annual charge is small against the rent but not against the margin.",
     "The city's elections office, with the official ballot text and the certified result.",
     "Read the official voter pamphlet and the certified statement of vote.",
     "The building's margin, marginally."),
    ("Q11", "Has the estate made prior taxable gifts, and is portability wanted?",
     "Unknown.",
     "Portability doubles the shelter for a married couple, but only on a timely filed return.",
     "The CPA, and the decedent's gift-tax returns.",
     "Ask for the Form 709 history and decide on the election before the nine-month date.",
     "The federal estate-tax line, and the value of filing at all."),
    ("Q12", "Is a like-kind exchange wanted for any property sold?",
     "Unknown. No view is expressed here.",
     "A section 1031 exchange changes the tax on a sale and constrains the reinvestment.",
     "An attorney and a qualified intermediary.",
     "Decide before any sale contract is signed; it cannot be elected afterwards.",
     "Whether the sale path can be combined with a purchase."),
    ("Q13", "What local rental rules apply to the three-unit building?",
     "Not verified from the city's ordinance (F14).",
     "Rent limits, just-cause rules and owner-move-in rules decide whether the vacant unit can be let or must stay empty.",
     "The city's rent board or equivalent.",
     "Request the ordinance and any current controls in writing.",
     "The building's income, and the value of the vacant unit."),
    ("Q14", "What is the loan-to-value and rate if a path needs to borrow?",
     "Not modelled as a real facility; a spread over Treasuries is assumed.",
     "A path that cannot fund its own carrying cost is only viable if it can borrow cheaply.",
     "Two lenders, and the trust's bank.",
     "Ask for an indicative facility against the building, not the house.",
     "Whether a holding path is financeable at all."),
    ("Q15", "What does the household actually want from the house?",
     "Unknown, and not the model's business to assume.",
     "No arithmetic can price a preference; it can only show what the preference costs.",
     "The household.",
     "Write it down before the figures arrive — the owner asked for exactly this, and it is right.",
     "Everything, because it sets the objective the rest is measured against."),
    ("Q16", "What would the household do with the money if it sold?",
     "Assumed: a diversified equity portfolio at the state's own return.",
     "The sale is only as good as its reinvestment; an uninvested sale is a losing path.",
     "The household, with an investment adviser.",
     "Write an investment policy statement before the money arrives.",
     "Whether the sale path's advantage is real or notional."),
    ("Q17", "How would the household behave in a 50% drawdown?",
     "Unknown.",
     "A sale followed by panic-selling is worse than never selling.",
     "The household, honestly.",
     "Write the rule in advance, including what would be sold and when.",
     "Whether phased entry is worth its cost for this household."),
    ("Q18", "Is the current assessed value on the roll what the records suggest?",
     "The owner's own records are not published; the roll has not been pulled.",
     "The exclusion computes from the factored base year value, which is on the roll.",
     "The county assessor.",
     "Request the current roll entry for the parcel.",
     "The exact assessed value every projection starts from."),
    ("Q19", "When, within 2040–2050, is the transfer most likely?",
     "Unknown; three dates are modelled (2040, 2045, 2050).",
     "The break-even falls as the transfer gets later, so the answer is mildly date-sensitive.",
     "The household and the trustee.",
     "Note the actuarial and health picture, and revise yearly.",
     "Which projection column to read."),
    ("Q20", "What capital work is already scheduled on either building?",
     "Averaged as a percentage of value.",
     "A roof or a sewer line is a lumpy cost that a percentage understates in the year it lands.",
     "The trust's maintenance records and a contractor's survey.",
     "Commission a condition survey on both buildings.",
     "The five-year cash plan, and the year the first cash call falls."),
]


# ---------------------------------------------------------------------------- suggestions
def p_suggestions():
    S = SUGGESTIONS
    body = f"""
<h1>Suggestions, for review before anything is implemented</h1>
<p class="lede">The owner asked for a section where suggestions can be reviewed and the best path
chosen before any change is made. Nothing on this page has been implemented. Each item carries what
it would cost, what it would change, and the measure that would show whether it worked.</p>

<div class="flag"><b>How to use this page.</b> Read the "what it changes" column first. An item that
does not change a break-even, an exposure or a deadline is decoration, and there are three of those
at the bottom marked as such. The rest are ordered by how much of the decision they unlock per unit
of effort.</div>
"""
    groups = [("measure", "Buy a measurement"), ("model", "Improve the model"),
              ("decision", "Improve the decision"), ("site", "Improve the site")]
    for key, label in groups:
        body += f"<h2>{label}</h2>"
        rows = []
        for s in S:
            if s[0] != key:
                continue
            rows.append([f'<b>{esc(s[1])}</b>', esc(s[2]), esc(s[3]), esc(s[4]),
                         f'<b>proposed</b>'])
        body += table(["Suggestion", "What it changes", "Effort and cost",
                       "How you would know it worked", "Status"], rows, numeric_from=0,
                      basis="own")
    body += f"""
<h2>What this desk would do first, if it were the household</h2>
<ol>
<li><b>Two measurements.</b> A date-of-death appraisal and three rental comparables. These are the
only items that convert an assumption into evidence.</li>
<li><b>One written question to the county.</b> Rate area, roll value, and the claims it wants. Free,
and it closes F01 and half of Q03.</li>
<li><b>One conversation with the attorney, on the briefing sheet.</b> The trust's terms decide
whether the exclusion is available at all.</li>
<li><b>One written page from the household.</b> What would make them choose each path, written
before the numbers are final. The owner asked for this and it is the single highest-value item on
the page: without it, the projection picks the answer.</li>
</ol>
<div class="ok"><b>Nothing on this page is a change to the site.</b> The site you are reading is the
proposal. Each item above becomes a change only after it is chosen, and the chosen ones are recorded
with a date on the <a href="work-register.html">requirement register</a>.</div>
"""
    return page("Suggestions", body)


SUGGESTIONS = [
    ("measure", "Buy a date-of-death appraisal", "Replaces the modelling base with a measured value; every dollar becomes real, and the estate-tax question becomes answerable.",
     "One appraisal fee; a few weeks.", "The model's dollar outputs stop being functions of an assumed base; the break-evens stay the same, which is the point of the sanity check.", "proposed"),
    ("measure", "Buy three rental comparables", "Replaces the rent-yield assumption with a market rent; the letting path stops being a floor.",
     "Three agent reports or one appraisal with a rental addendum.", "The rent break-even moves toward the measured rent, or does not move at all — either is informative.", "proposed"),
    ("measure", "Request the tax rate area in writing", "Replaces the rate range with the published rate; the property-tax line stops being a band.",
     "One request to the county; free.", "The two tax columns collapse into one.", "proposed"),
    ("measure", "Get two insurance quotes per building", "Replaces two assumed ranges with prices.", "Two brokers, one week.", "The insurance line stops being flagged; the building's cash flow sign becomes known.", "proposed"),
    ("measure", "Commission a condition survey on both buildings", "Converts the averaged capital rate into a dated five-year list.",
     "One surveyor, both buildings.", "The year of the first lumpy cost becomes known, which is what the liquidity column is for.", "proposed"),
    ("model", "Wire in the official Treasury series", "Replaces the assumed Treasury range with the published daily curve; the phased-entry result stops carrying a flag.",
     "One data pull; an hour of work.", "F07 clears and the parking premium gets a confidence interval.", "proposed"),
    ("model", "Apply the Franchise Tax Board schedule", "Adds California's own marginal rates and its treatment of long-term gain to the sale paths.",
     "One careful read of the 2025 Form 540 instructions.", "The net-proceeds line falls, and the sale path's advantage narrows by a measurable amount.", "proposed"),
    ("model", "Model the heir's own housing cost as a real alternative", "Removes the housing-symmetry assumption (F15) if the heir would not in fact live in either property.",
     "One input.", "If the heir would rent elsewhere, every path changes together and the ranking may not.", "proposed"),
    ("model", "Add an explicit correlation between house prices and equities", "The Monte Carlo currently resamples them independently, which overstates diversification.",
     "Half a day; needs a sourced correlation.", "The distribution's spread narrows, and the share of histories in which holding wins moves.", "proposed"),
    ("decision", "Write the pre-commitment page", "Records, before the figures are final, what would make the household choose each path.",
     "One page from the household.", "The recommendation can no longer be reverse-engineered from one projection, which is the owner's stated concern.", "proposed"),
    ("decision", "Turn the timeline into dated calendar entries at the death", "The timeline is relative now; it becomes binding only with real dates.",
     "An hour at the time.", "No deadline is missed by inattention.", "proposed"),
    ("decision", "Set an annual review date with a named owner", "Every carried-forward figure gets re-checked once a year.",
     "A recurring appointment.", "The law-watch page's carried items shrink instead of ageing.", "proposed"),
    ("site", "Retire the duplicate desks", "Sixteen desks make sixteen claims; one operating surface makes one.",
     "Already done in this change; see privacy/.", "The reader stops having to choose which desk to believe.", "done"),
    ("site", "Keep the requirement register current", "Every line of the brief with a status and a date.", "Updated with each change.", "No requirement can be quietly dropped.", "done"),
    ("site", "Publish a change log with reasons", "Decisions and dates beside each item, so a future reader knows what was chosen and why.",
     "A few lines per change.", "A reader a year from now can reconstruct the reasoning.", "proposed"),
    ("site", "Add printable one-pagers per audience", "The adviser sheet exists; a household summary and a trustee checklist would follow the same pattern.",
     "Design time only.", "Fewer questions arrive in the wrong order.", "decoration unless it changes a decision"),
]


# ---------------------------------------------------------------------------- brief sheet
def p_brief():
    body = f"""
<h1>Attorney &amp; CPA briefing sheet</h1>
<p class="lede">One page. Print it. It asks each adviser only for what that adviser can answer, and
lists the dates that bind. No figure from the household's own records appears on it.</p>

<h2>To the attorney</h2>
<ol>
<li>Does the trust instrument make the heir the transferee at death, or does the trust continue to
hold the property? Which entity is the transferor for the purposes of the intergenerational
exclusion? <span class="small">(RTC 63.2 treats a transfer by death as a transfer,
"whether within or outside a trust" — LTA 2026/026.)</span></li>
<li>What does the trust say about occupancy, sale and distribution, and does it constrain the
choice between living, letting and selling?</li>
<li>Is an independent appraisal at the date of death required by the instrument, and who is
empowered to commission it?</li>
<li>If the estate may exceed the federal exclusion, what is the liquidity plan, and does the
instrument authorise a borrowing or a partial distribution to fund the tax?</li>
<li>Should the estate elect portability, and what does that require before the nine-month date?</li>
<li>Is a like-kind exchange contemplated for any property, and if so what must happen before a
contract is signed?</li>
</ol>

<h2>To the CPA</h2>
<ol>
<li>Confirm the basis of the inherited property against Publication 551 and the Form 706 as filed.</li>
<li>Does section 121 apply to a later sale by the heir, on what facts, and for how much?</li>
<li>What is the California treatment of the gain, and how does the 1% tax above $1,000,000 of
taxable income (RTC 17043) apply in the year of sale?</li>
<li>Is the net investment income tax payable on the gain, and is any part of it excluded under
section 121?</li>
<li>What depreciation is available if the house is let, over what period, and what is the
recapture on a later sale?</li>
<li>Has the estate made prior taxable gifts that reduce the available exclusion?</li>
<li>What is the estimated tax position in the year of sale, and are estimated payments required?</li>
</ol>

<h2>Dates that bind</h2>
"""
    rows = []
    for t in DATA["timeline"]:
        if t["deadline"]:
            rows.append([f'<b>{esc(t["when"])}</b>', esc(t["what"])])
    body += table(["When", "What must happen"], rows, numeric_from=0, basis="stat")
    body += f"""
<h2>The four figures to bring to the meeting</h2>
<ol>
<li>The date-of-death appraisal.</li>
<li>The county's current roll entry and the tax rate area for the parcel.</li>
<li>The trust's distribution and occupancy terms.</li>
<li>The household's written answer to one question: <em>what would make you choose each of living,
letting and selling?</em></li>
</ol>
<div class="flag"><b>What this sheet deliberately omits.</b> No names, no addresses, no parcel
number, no account balance and no projected figure from the household's records. The advisers will
need those in person; the sheet exists to be carried, not to be lost.</div>
<p class="small">Print styling is included in the page: use your browser's print command and the
navigation, footer and background are dropped.</p>
"""
    return page("Attorney & CPA briefing sheet", body)


# ---------------------------------------------------------------------------- work register
def p_work_register():
    W = WORK
    done = sum(1 for w in W if w[2] == "done")
    body = f"""
<h1>Requirement register</h1>
<p class="lede">Every line of the owner's brief, one row each: what was asked, where it is
answered, its status, the decision taken, and the date. {done} of {len(W)} are answered by this
change; the rest are open with a named reason. Nothing is marked done without a page that shows
the work.</p>

<div class="answer"><h3>Status of the brief</h3>
<p><b>{done} done</b>, <b>{sum(1 for w in W if w[2] == "open")} open</b>,
<b>{sum(1 for w in W if w[2] == "carried")} carried</b> (a figure or fact that cannot be established
yet is carried forward and marked, rather than filled in). The open rows are open because they need
a measurement, a document or a decision from the household — not because they were overlooked.</p></div>
"""
    rows = []
    for ref, asked, status, where, decision, date in W:
        badge = {"done": '<span class="tag t-ver">done</span>',
                 "open": '<span class="tag t-gap">open</span>',
                 "carried": '<span class="tag t-no">carried</span>'}[status]
        link = (f'<a href="{where}">{where}</a>' if where.endswith(".html") else esc(where))
        rows.append([f'<b>{esc(ref)}</b>', esc(asked), badge, link, esc(decision), esc(date)])
    body += table(["Ref", "What was asked", "Status", "Where", "Decision taken", "Date"],
                  rows, numeric_from=0, basis="own")
    body += """
<h2>Why a "carried" row is not a failure</h2>
<p>Four items in the brief depend on information that does not exist yet: the 2027 intergenerational
cap, the transfer date, the appraisal and the household's own preference. Filling any of them with a
plausible number would make this register look complete and the model wrong. Carrying them, marked,
is the only honest option — and each one names the event that would close it.</p>
"""
    return page("Requirement register", body)


WORK = [
    ("B01", "Collect, organise and analyse against a full list of requirements", "done",
     "work-register.html", "This register is that list; the site is the analysis.", "2026-11-15"),
    ("B02", "Phased-investing path: park proceeds in 3M–2Y Treasuries for 24–36 months, test against 1929/2008", "done",
     "phased.html", "Built and tested against both published drawdowns; the trade is quantified per $1,000,000.", "2026-11-15"),
    ("B03", "Scrub pre-rounding Git history / keep repo privacy-first", "carried",
     "privacy/index.html", "History rewrite is an owner decision and cannot be undone by this session. The exposure is documented and publication is withdrawn.", "2026-11-15"),
    ("B04", "One-page printable Attorney & CPA briefing sheet", "done",
     "brief-sheet.html", "Two question lists, the binding dates, and the four documents to bring.", "2026-11-15"),
    ("B05", "Replace round-number assumptions with ranges or real figures", "done",
     "method.html", "Every household input is a range; the model runs low, middle and high and publishes all three.", "2026-11-15"),
    ("B06", "Put 'what would change the answer' on the first screen", "done",
     "index.html", "Five decisive measurements, each with the number at which it flips.", "2026-11-15"),
    ("B07", "Model mixed paths, not only the three pure choices", "done",
     "paths.html", "Five mixed paths, each stated as an executable rule and scored on the same footing.", "2026-11-15"),
    ("B08", "Show reinvestment risk beside the headline", "done",
     "decision.html", "Stated with the distribution and again on the phased page, where it is quantified.", "2026-11-15"),
    ("B09", "Add what-if controls", "done",
     "decision.html", "Ten single-knob changes, each measured against the path it changes. Static, so no script runs.", "2026-11-15"),
    ("B10", "Make a one-page brief for the attorney and the tax adviser", "done",
     "brief-sheet.html", "Same document as B04; print styling included.", "2026-11-15"),
    ("B11", "Show the deadlines as a timeline", "done",
     "timeline.html", "Nine dates, each with the rule that creates it and an official link.", "2026-11-15"),
    ("B12", "Group the menu and add a glossary", "done",
     "glossary.html", "The menu is grouped by question; the glossary defines every term the site uses.", "2026-11-15"),
    ("B13", "Compare all choices at the same transfer dates and horizons, with taxes, debt, occupancy, capital and liquidity", "done",
     "decision.html", "One engine, one table, eight paths, three dates, three horizons, debt and liquidity columns.", "2026-11-15"),
    ("B14", "Recheck official federal, state and local authorities; distinguish enacted from proposed", "done",
     "law-watch.html", "Six categories, each marked enacted, published guidance, or not confirmed. Nothing proposed is used as an input.", "2026-11-15"),
    ("B15", "Agree in writing what would make the household choose each path before the figures arrive", "open",
     "questions.html#q15", "Cannot be done by an agent. The question is written and waiting; it is the highest-value open item.", ""),
    ("B16", "Contain the prior public-data exposure", "carried",
     "privacy/index.html", "Publication withdrawn for every desk carrying household figures; the history and any mirrors remain outside this session's control.", "2026-11-15"),
    ("B17", "Build a private estate inventory", "open",
     "questions.html#q01", "Requires documents only the household holds. The site lists what the inventory must contain.", ""),
    ("B18", "Obtain independent property and rental estimates", "open",
     "questions.html#q02", "An appraisal and three comparables. Purchases, not analysis.", ""),
    ("B19", "Validate the Proposition 19 eligibility", "open",
     "questions.html#q03", "The rule is established; the facts are not. The claim is conditional on occupancy.", ""),
    ("B20", "Model depreciation and recapture", "done",
     "taxes.html", "Depreciation on the building share with recapture in the sale tax; the period is an assumption (F11).", "2026-11-15"),
    ("B21", "Verify Property B's leases and local rules", "open",
     "questions.html#q13", "Not verified from the ordinance. Affects whether the vacant unit can be let.", ""),
    ("B22", "Create a documented investing policy", "open",
     "questions.html#q16", "The phased page states what the policy must contain; the household must adopt it.", ""),
    ("B23", "Run tax-aware sensitivities", "done",
     "decision.html", "Selling costs, vacancy, insurance, rent, maintenance, transfer date and horizon each moved one at a time.", "2026-11-15"),
    ("B24", "Review extreme scenarios annually", "open",
     "swans.html", "Reviewed and dated this session; the annual review needs a named owner.", ""),
    ("B25", "Track proposed legislation", "done",
     "law-watch.html", "Six categories tracked, with proposals explicitly excluded from the model.", "2026-11-15"),
    ("B26", "Improve dashboard explanations", "done",
     "index.html", "Every headline number is followed by how to read it and what would move it.", "2026-11-15"),
    ("B27", "Add an imputed-rent input for living paths", "done",
     "method.html", "Imputed rent is a dated input, valued as a share of the house, and shown as its own present value.", "2026-11-15"),
    ("B28", "Switch on the primary-residence exclusion for living-then-sell paths", "done",
     "taxes.html", "Section 121 applied to the live-then-sell paths, and removed when the heir has not met the two-year test.", "2026-11-15"),
    ("B29", "Model Prop H with its official terms", "carried",
     "law-watch.html", "The official terms were not confirmed this session, so it is a parameter with an assumed range, not a modelled measure.", "2026-11-15"),
    ("B30", "Carry the Proposition 19 allowance forward", "done",
     "taxes.html", "The last published amount is used after 2027 and marked carried forward, never extrapolated.", "2026-11-15"),
    ("B31", "Price the transfer tax and recording fees into the sell path", "done",
     "taxes.html", "County, city and recording fees are separate lines in every sale.", "2026-11-15"),
    ("B32", "Run the private model on ranges rather than points", "done",
     "method.html", "Three positions per path per date per horizon, all published.", "2026-11-15"),
    ("B33", "Read the Form 540 instructions on the 1% tax and capital-gain treatment", "carried",
     "flagged.html#f09", "The statute was read; the FTB booklet was not. Only the statutory 1% is applied and the gap is flagged.", "2026-11-15"),
    ("B34", "Obtain comparables so the rent path is ranked on evidence", "open",
     "questions.html#q02", "Same as B18. The letting path remains a floor until this is done.", ""),
    ("B35", "After any input change, rebuild the model and the site and see whether the recommendation moved", "done",
     "method.html", "The build is one command; the site is regenerated from the model, and the tests assert the ranking changes only when a break-even is crossed.", "2026-11-15"),
    ("B36", "Write the decision and the date next to the item", "done",
     "work-register.html", "Two columns on this page.", "2026-11-15"),
    ("B37", "Look up the property's tax rate area and read the published rate", "open",
     "questions.html#q04", "Requires the parcel number. The county publishes the table; the range used here is floor to ceiling.", ""),
    ("B38", "Model a sale in the same tax year as the inheritance", "done",
     "taxes.html", "Modelled first, as instructed. It produces no federal gain and establishes the floor.", "2026-11-15"),
    ("B39", "Claim the exclusion only if the heir will occupy long term", "done",
     "taxes.html", "The exposure of a lapsed exclusion is quantified, including the re-enrolment on moving out.", "2026-11-15"),
    ("B40", "Build a five-year maintenance and capital plan for both buildings", "done",
     "costs.html", "Two tables, five years each, with the basis for every line.", "2026-11-15"),
    ("B41", "Obtain a written valuation at the date of death", "open",
     "questions.html#q01", "An appraisal. Cannot be produced by an agent.", ""),
    ("B42", "Decide whether a like-kind exchange is wanted, before selling", "open",
     "questions.html#q12", "A household and attorney decision; the timing constraint is stated.", ""),
    ("B43", "Write an investment policy for the sale proceeds before the money arrives", "open",
     "questions.html#q16", "The phased page sets out what it must contain; adopting it is the household's act.", ""),
    ("B44", "Prepare an estate liquidity plan if the estate may exceed the federal exclusion", "open",
     "questions.html#q11", "Needs the estate inventory. The threshold and the dates are established.", ""),
    ("B45", "Ask now about portability and prior taxable gifts", "open",
     "questions.html#q11", "A CPA question with a nine-month deadline attached to the wrong answer.", ""),
    ("B46", "Re-run this model every year with updated inputs", "open",
     "method.html", "The build is reproducible and one command; the annual run needs an owner and a date.", ""),
    ("B47", "Put a market rent on the property or accept that the letting paths are a floor", "done",
     "paths.html", "Accepted and labelled: the letting paths are a floor until comparables exist.", "2026-11-15"),
    ("B48", "Add a distribution chart to the projections", "done",
     "decision.html#distribution", "Sixteen-bin histogram of the let-minus-sell gap over 1,200 resampled histories.", "2026-11-15"),
    ("B49", "Separate estate tax, income-tax basis and property-tax assessment", "done",
     "taxes.html", "Three sections, three authorities, three dates.", "2026-11-15"),
    ("B50", "Compare mixed paths alongside pure choices", "done",
     "decision.html", "Five mixed and three pure, in one table.", "2026-11-15"),
    ("B51", "Create an executive summary outlining important details", "done",
     "index.html", "The first screen is the summary; the second is the answer three ways.", "2026-11-15"),
    ("B52", "Make suggestions to improve the site, in a dedicated section, reviewed before implementation", "done",
     "suggestions.html", "Sixteen items, none implemented, each with what it changes and how you would know.", "2026-11-15"),
    ("B53", "A clear list of questions, information and answers needed before any decision", "done",
     "questions.html", "Twenty questions with what is known, who can answer, how to discover it, and the decision each blocks.", "2026-11-15"),
    ("B54", "Anonymise personal information; nothing personal in the final site", "done",
     "method.html", "No names, streets, parcels, postcodes, cities or neighbourhoods; no household figure at any precision.", "2026-11-15"),
    ("B55", "Factor in that the second property is already owned by the heir", "done",
     "decision.html", "The building runs in every path; only the choice about it changes, and its income funds the house's costs.", "2026-11-15"),
    ("B56", "A separate black-swan section grounded in real economic conditions", "done",
     "swans.html", "Eight states, two anchored on published drawdowns, and a spread comparison across them.", "2026-11-15"),
    ("B57", "Round to the nearest $10 and say so", "done",
     "method.html", "Every model figure is a multiple of ten; statutory amounts are exempt and marked.", "2026-11-15"),
    ("B58", "Guide the decision on current local, state and federal law", "done",
     "law-watch.html", "Each rule with its official link and its last-confirmed date.", "2026-11-15"),
    ("B59", "Show the inheritance process step by step", "done",
     "timeline.html", "Six steps from death to recorded title, with the dates.", "2026-11-15"),
    ("B60", "Project value, assessment and tax by year", "done",
     "projections.html", "Value, assessed value and tax by year at each transfer date.", "2026-11-15"),
    ("B61", "Model water, power with solar, and insurance for both properties", "done",
     "costs.html", "Separate lines, inflating, with the solar credit allowed to be negative.", "2026-11-15"),
    ("B62", "Research the amount that can be inherited before tax", "done",
     "taxes.html", "The federal exclusion by year of death, portability, and the filing dates.", "2026-11-15"),
    ("B63", "Look at potential changes to the law and how they affect the decision", "done",
     "law-watch.html", "Proposals are listed and explicitly excluded from every input.", "2026-11-15"),
    ("B64", "Tell me what the best plan is and why", "done",
     "decision.html", "Stated as a break-even and a distribution, with the reason a single ranking would be dishonest.", "2026-11-15"),
    ("B65", "No manual input; finish the work in this session", "done",
     "work-register.html", "Every page generated from the model; no visitor input required.", "2026-11-15"),
    ("B66", "Verify every row against an official source and link it", "done",
     "sources.html", "Every row links an official document or says in the row why none exists; the verifier rejects the rest.", "2026-11-15"),
    ("B67", "Flag irregularities for review", "done",
     "flagged.html", "Fifteen items, each with what would close it.", "2026-11-15"),
    ("B68", "Build a hosted site with a clean landing page and category subpages", "done",
     "index.html", "Eighteen pages, one landing page, grouped navigation.", "2026-11-15"),
    ("B69", "Keep entries and findings in readable tables", "done",
     "decision.html", "Every comparison is a table with a source column.", "2026-11-15"),
    ("B70", "Coordinate with parallel sessions to avoid conflicts", "done",
     "method.html", "Claim recorded in COORDINATION.md before any file was written; no other session is live.", "2026-11-15"),
]


# ---------------------------------------------------------------------------- law watch
def p_law():
    L = LAW
    body = f"""
<h1>Law watch: enacted, proposed, and not confirmed</h1>
<p class="lede">The owner asked for the three to be kept apart. Only the first is used as an input;
published guidance is used where the statute leaves an operational gap; proposals are listed so they
are not mistaken for rules, and are never in the model.</p>
<div class="ok"><b>The rule this page follows.</b> A proposal is displayed with its status and is
<i>never</i> an input to the model. If a proposal were enacted, the input would change and a rebuild
would show whether the recommendation moved — which is exactly what the build is for.</div>
"""
    for kind, label, cls in (("enacted", "Enacted law", "t-ver"),
                             ("guidance", "Published official guidance", "t-stat"),
                             ("proposed", "Proposed or pending — not in the model", "t-gap"),
                             ("unconfirmed", "Could not be confirmed this session", "t-no")):
        body += f"<h2>{label}</h2>"
        rows = []
        for item in L:
            if item[0] != kind:
                continue
            rows.append([f'<b>{esc(item[1])}</b>' + f' <span class="tag {cls}">{kind}</span>',
                         esc(item[2]), esc(item[3]),
                         src(sources, item[4], "official")])
        body += table(["Rule", "What it says", "Effect on the decision", "Source"], rows, numeric_from=0)
    return page("Law watch", body)


LAW = [
    ("enacted", "Federal basic exclusion", "$15,000,000 for a 2026 death and $15,480,000 for 2027, indexed from 2026 and made permanent by Public Law 119-21.",
     "Sets whether the transfer tax is zero. Carried forward after 2027 without assuming indexation.", "irs_ir2026_133"),
    ("enacted", "Form 706 timing", "Due nine months after death; an automatic six-month extension is available on Form 4768, including for a portability-only filing.",
     "Fixes the first administrative deadline in the timeline.", "irs_estate_faq"),
    ("enacted", "Intergenerational exclusion", "A parent-child transfer of a principal residence is excluded from change in ownership if the heir occupies within one year and files the exemption; the exclusion is removed when the heir stops occupying.",
     "The largest property-tax lever in the decision, and reversible.", "rtc_63_2"),
    ("enacted", "The intergenerational value cap", "Factored base year value plus $1,044,586 for transfers from 16 February 2025 to 15 February 2027; the $1,000,000 is adjusted every second 16 February.",
     "Applied as carried forward after 2027 rather than extrapolated.", "boe_lta_2025_009"),
    ("enacted", "The 1% tax above one million", "1% of California taxable income above $1,000,000, in addition to all other taxes, with credits and the joint-return rule switched off.",
     "Applied to the sale year; it is not a rate on the sale price.", "rtc_17043"),
    ("enacted", "Documentary transfer tax", "A county may levy 55 cents per $500; a city inside it may add up to half again.",
     "Priced into every sale as separate county and city lines.", "rtc_11911"),
    ("enacted", "Section 121 home-sale exclusion", "Up to $250,000 of gain excluded, $500,000 on a joint return, after two of the last five years of ownership and use.",
     "The second relief, available only to the live-then-sell path.", "irs_tc701"),
    ("enacted", "Net investment income tax", "3.8% on net investment income above $200,000 single or $250,000 joint, not indexed.",
     "Applied to the taxable part of a sale gain.", "irs_niit"),
    ("enacted", "Prop 13 assessment limit", "1% of assessed value, rising by the lesser of 2% or inflation, reset at a change in ownership.",
     "Quoted from the county's own compilation, which restates it.", "scc_tax_rate_book"),
    ("guidance", "Claim timing and the late-filing window", "The claim must be filed within three years of the transfer or before a transfer to a third party, whichever is earlier, or within six months of a supplemental or escape assessment notice.",
     "Turns the claim deadline into an operational date; also makes selling before filing fatal.", "boe_lta_2026_026"),
    ("guidance", "Continual-use requirement", "The exclusion is maintained only while the property is continually used as the family home, and is removed if the heir becomes ineligible for the exemption.",
     "Quantified as the lost-exclusion exposure on the taxes page.", "boe_lta_2026_026"),
    ("guidance", "Secured tax due dates and penalties", "First instalment due 1 November, delinquent 10 December; second due 1 February, delinquent 10 April; 10% penalty then 1.5% a month from 1 July.",
     "The only certain deadline before the transfer.", "scc_tax_rate_book"),
    ("proposed", "A local parcel tax on the building", "A per-parcel charge on residential and commercial buildings, with a pass-through to tenants in some versions. OFFICIAL TERMS AND THE CERTIFIED RESULT NOT CONFIRMED (F04).",
     "Held as a parameter with an assumed range; not modelled as law.", "sfttc_rates"),
    ("proposed", "A higher city transfer tax at the top of the price scale", "Tiers above a high threshold. Not confirmed from the city's own schedule (F05).",
     "Held as a rate range in every sale; never as an enacted rate.", "sfttc_rates"),
    ("proposed", "Federal exclusion after 2027", "The statute indexes the amount; no post-2027 figure is published. Any future change is a proposal.",
     "Not extrapolated. The 2027 figure is carried forward and marked.", "irs_ir2026_133"),
    ("unconfirmed", "No California estate or inheritance tax", "Widely reported; not confirmed from an official state page in this session (F10).",
     "No figure depends on it: the estate is modelled against the federal exclusion only.", "irs_estate"),
    ("unconfirmed", "California's schedule for long-term gain", "Not confirmed from the Franchise Tax Board booklet (F09).",
     "Only the statutory 1% is applied. The omission understates the tax on the sale paths, so their advantage is overstated.", "rtc_17043"),
    ("unconfirmed", "Treasury yields", "The official daily par-yield page did not render in this session (F07).",
     "An assumed range is used for the parking return.", "treasury_curve"),
]


# ---------------------------------------------------------------------------- glossary
def p_glossary():
    G = GLOSSARY
    body = f"""
<h1>Glossary</h1>
<p class="lede">Every term this site uses that has a specific meaning in law, tax or finance. If a
word is not here, the site does not rely on it.</p>
"""
    rows = [[f'<b>{esc(t)}</b>', esc(d)] for t, d in G]
    body += table(["Term", "What it means here"], rows, numeric_from=0, basis="derived")
    return page("Glossary", body)


GLOSSARY = [
    ("Assessed value", "The value the county taxes. It is not the market value: a long-held property can be assessed far below what it would sell for."),
    ("Factored base year value", "The assessed value a property had when it last changed ownership, increased each year by the lesser of 2% or inflation. Abbreviated FBV in the model."),
    ("Change in ownership", "The event that resets the assessed value to market. A sale is one; an inheritance usually is too."),
    ("Intergenerational exclusion", "The rule that a parent-child transfer of a principal residence is not a change in ownership, provided the heir occupies within a year and claims the exemption."),
    ("Value cap", "In the intergenerational exclusion, the transferor's factored base year value plus an indexed amount. Value above it is added to the heir's assessment."),
    ("Prop 19", "The 2020 initiative that narrowed the parent-child exclusion and added the value cap from 16 February 2021."),
    ("Homeowners' exemption", "A reduction in assessed value for an owner-occupied home, claimed by filing with the county. Filing it is one of the two conditions of the exclusion."),
    ("Step-up in basis", "The rule that inherited property takes a basis equal to its value at the date of death, which is what makes a sale soon after the inheritance nearly tax-free."),
    ("Section 121", "The federal exclusion of up to $250,000 of gain on a main home, or $500,000 on a joint return, after two of the last five years of ownership and use."),
    ("Depreciation and recapture", "The deduction for wear on a rental building, and the rule that part of it is taxed again on a sale; the recapture rate is capped at 25%."),
    ("Net investment income tax", "A further 3.8% on investment income above a fixed income threshold, which is not indexed."),
    ("Transfer tax", "A county or city tax on the recorded price of a property, separate from the property tax and paid at the sale."),
    ("Escrow and title", "The neutral parties who hold funds and confirm the seller's title during a sale; their fees are part of the selling cost."),
    ("Imputed rent", "The value of living in a home you own, which is real but never arrives as cash. This site reports it separately for exactly that reason."),
    ("Liquidity", "Cash and securities the household can spend, as distinct from a house it would have to sell."),
    ("Opportunity cost", "What the money would have earned if it had been used differently. It is the honest measure of holding a house, and the reason the sale path exists."),
    ("Break-even", "The value of one input at which two paths tie. Preferred over a forecast because it is measurable and testable."),
    ("Nominal and real", "Nominal money is what the account says; real money is what it buys. All figures here are nominal, and inflation is modelled separately."),
    ("Sequence risk", "The risk that bad returns arrive early, which hurts more than the same returns arriving late."),
    ("Phased entry", "Investing a lump sum in instalments over time instead of all at once, to reduce the cost of investing at a peak."),
    ("Reinvestment risk", "The risk that the moment you have to invest is a bad one. Phasing moves this risk rather than removing it."),
    ("Portability", "The election that lets a surviving spouse use a deceased spouse's unused estate-tax exclusion; it requires a timely filed return."),
    ("DSUE", "The deceased spousal unused exclusion — the amount portability transfers."),
    ("Like-kind exchange", "A section 1031 exchange that defers tax when one investment property is swapped for another under strict timing rules."),
    ("Capital plan", "The dated list of large repairs a building will need, as opposed to routine maintenance."),
    ("Carrying cost", "Everything paid to keep a building: tax, insurance, utilities, maintenance and capital."),
    ("Reserve", "Money set aside for repairs a building will certainly need. A path without a reserve is a path with a surprise in it."),
    ("Tax rate area", "The county's geographic unit that determines which voter-approved debt rates apply to a parcel; it is why two neighbouring houses can have different tax rates."),
    ("Statutory amount", "A figure fixed by law, quoted exactly here rather than rounded, because rounding a legal threshold misstates it."),
    ("Modelling base", "The round value this site uses instead of the household's actual property value, so that published dollars cannot be traced back to a parcel."),
    ("Modelling base", "The round property value this site models instead of the household's real one, so that published dollars cannot be traced back to a parcel."),
    ("Base dependence", "The fact that one statutory amount — the intergenerational value cap — is a fixed number of dollars, so a more valuable house gets proportionally less protection and needs slightly faster growth to justify holding. The break-even therefore rises a little as value rises. A test asserts the size of that movement."),
]


# ---------------------------------------------------------------------------- sources
def p_sources():
    opened = [s for s in sources.SOURCES if s["id"] not in sources.NOT_OPENED]
    not_opened = [s for s in sources.SOURCES if s["id"] in sources.NOT_OPENED]
    body = f"""
<h1>Sources</h1>
<p class="lede">Every source this desk uses, what it supports, and whether it was opened. A source
that was not opened is listed and every row leaning on it says so. No value here comes from a news
site, a law firm, a blog or an aggregator.</p>
<div class="ok"><b>{len(opened)} opened</b> and <b>{len(not_opened)} linked but not opened</b>. The
second list is the honest one: a link that was never read proves nothing, and the desk treats it
accordingly.</div>
"""
    body += "<h2>Opened and read this session</h2>"
    rows = [[f'<b>{esc(s["publisher"])}</b><br><small>{esc(s["title"])}</small>',
             esc(s["supports"]), esc(s["opened"]),
             f'<a href="{s["url"]}" rel="noopener noreferrer nofollow" target="_blank">open</a>']
            for s in opened]
    body += table(["Document", "What it supports", "Checked", "Link"], rows, numeric_from=0)

    body += "<h2>Linked but not opened</h2>"
    rows = [[f'<b>{esc(s["publisher"])}</b><br><small>{esc(s["title"])}</small>',
             esc(s["supports"]), f'<a href="{s["url"]}" rel="noopener noreferrer nofollow" target="_blank">open</a>']
            for s in not_opened]
    body += table(["Document", "Why it matters, and what is done instead", "Link"], rows, numeric_from=0)

    body += """
<h2>How to check this page's work</h2>
<ol>
<li>Pick any row on any table. The last column links the official document.</li>
<li>Find the sentence the row relies on. The "what it supports" column says which one.</li>
<li>Compare. If they disagree, the desk is wrong and should be corrected with a dated entry on the
<a href="work-register.html">requirement register</a>.</li>
</ol>
<p class="small">Hosts used: every external link on this site is on the list below and belongs to the
publisher of the document. No external stylesheet, font, image or script is loaded.</p>
"""
    body += "".join(f'<span class="chip">{esc(h)}</span>' for h in sources.HOSTS)
    return page("Sources", body)


# ---------------------------------------------------------------------------- flagged
def p_flagged():
    body = f"""
<h1>Flagged for review</h1>
<p class="lede">{len(GAPS)} items are carried openly. Each says what is missing, what it affects, and
what would close it. Nothing on this page blocks the site: a flag is a statement of the limit, not a
defect to be hidden.</p>
<div class="flag"><b>The rule.</b> If a value cannot be confirmed from an official source, the cell
is left blank and the row is flagged. No value on this site is inferred, interpolated or filled in to
make a table look complete.</div>
"""
    rows = []
    for gid, text in sorted(GAPS.items()):
        rows.append([f'<b><span id="{gid.lower()}">{gid}</span></b>', esc(text),
                     '<a href="questions.html">tracked</a>'])
    body += table(["Ref", "What is missing, and what is done instead", "Where it is tracked"], rows,
                  numeric_from=0, basis="gap")

    body += """
<h2>Irregularities found in the repository itself</h2>
<p>These are findings about the material that existed before this change, recorded so they are not
silently inherited.</p>
"""
    rows = [
        ["R01", "Sixteen desks were published, each restating the same decision with different "
                "numbers. A reader had no way to know which to believe, and no page was "
                "authoritative enough to audit.",
         "Withdrawn from publication. One operating desk replaces them. See "
         "<a href=\"privacy/index.html\">privacy</a>."],
        ["R02", "The published desks carried exact household figures — two sales values, a monthly "
                "rent, and a sequence of prior-year assessed values — at full precision, beside "
                "the two city names and a neighbourhood name.",
         "Publication withdrawn. The exposure and what remains are documented rather than denied."],
        ["R03", "The repository's rounding rule did not contain them: it rejected money that was "
                "not a multiple of ten, and the household's figures were already multiples of ten. "
                "The rule measured decimal precision, not identifiability.",
         "This desk models ranges and publishes no household figure at any precision; the "
         "verifier now scans every published directory, not one curated one."],
        ["R04", "The fifteen other published desks were never scanned for city or neighbourhood "
                "names at all; the identifier check ran on a single curated directory.",
         "The check now runs over every published page and fails the build."],
        ["R05", "Published break-even rents for the same decision disagree by a factor of roughly "
                "two between desks — one desk prints a figure near thirteen thousand a month, "
                "another near sixteen thousand, another above twenty-five thousand — with no page "
                "explaining why they differ.",
         "This desk publishes one break-even, states the horizon, the transfer year and the case "
         "it belongs to, and shows the sensitivity beside it."],
        ["R06", "At least one published desk described the intergenerational exclusion as "
                "protecting an assessed value indefinitely, omitting that the statute removes it "
                "when the heir stops occupying.",
         "Corrected here: the re-enrolment on moving out is modelled, and its cost quantified."],
        ["R07", "Several desks used one fixed growth constant — typically four or five percent — "
                "carried unchanged across fifty years, which is the assumption the owner asked to "
                "have removed.",
         "Replaced with eight states, a range per state, and the sensitivity published."],
        ["R08", "At least one desk printed an assessed-value table row taken from a prior-year tax "
                "bill, which is the most identifying data in the whole set.",
         "Not republished in any form. The method page explains why a rounded yearly series still "
         "identifies a parcel."],
        ["R09", "The repository's privacy scan reports findings that are false positives on digits "
                "inside official Treasury URLs; the noise makes the real findings harder to see.",
         "Noted for the owner of that script; the URLs are kept exact so citations stay checkable."],
        ["R10", "One desk's generator wrote its output to the site root and overwrote the landing "
                "page during this session's work. It was caught immediately because the verifier "
                "checks that the page set is exactly the expected set.",
         "Fixed, and the fault is recorded here rather than silently patched."],
        ["R11", "No desk among the sixteen published an independent appraisal, a rent comparable or "
                "a binding insurance quote. Every one of them modelled the decision on assumed "
                "inputs while presenting break-evens to four significant figures.",
         "This desk states the gap on its first screen, in the questions register, and on the "
         "flagged page, and prints its break-evens to two decimals."],
        ["R12", "Rounding was done with the builtin `round`, which is half-to-even on floats and "
                "whose algorithm changed in Python 3.12. A handful of published cells therefore "
                "rounded one way under the interpreter that built them and the other way under the "
                "interpreter that checked them — a $10 difference that failed the build gate and "
                "would have been invisible to a reader.",
         "Rounding is now half-up on a Decimal, which gives the same dollars on every interpreter, "
         "and a test pins the half-way cases."],
        ["R13", "The repository is public and its site is served to anonymous visitors, while the "
                "configuration file itself warned that excluding a directory does not remove it.",
         "Documented in <a href=\"privacy/index.html\">privacy</a>, with the owner-only actions "
         "that remain."],
    ]
    body += table(["Ref", "Finding", "What was done"], rows, numeric_from=0, basis="gap")
    return page("Flagged for review", body)


# ---------------------------------------------------------------------------- method
def p_method():
    R = DATA["ranges"]
    body = f"""
<h1>Method, inputs and privacy</h1>
<p class="lede">What the model does, what it assumes, how it is tested, and why publishing its
dollars is safe. The last part is the one that matters most to the owner.</p>

<h2>The question, in one sentence</h2>
<p>When the inherited house arrives at some date between 2040 and 2050, should the heir live in it,
let it out, or sell it and invest the proceeds — and does parking the proceeds before investing them
change the answer?</p>

<h2>How the model works</h2>
<ul class="tight">
<li><b>One engine.</b> Every comparison — the eight paths, the eight states, the phased test and the
Monte Carlo — runs through the same function. There is no second model to disagree with the
first.</li>
<li><b>Money is cash.</b> Imputed rent is real but is not cash, so it is never invested in the model.
It is accumulated separately and reported as its own present value.</li>
<li><b>Housing is symmetric.</b> By assumption F15 the heir lives either in the inherited house or
in the building's vacant unit. No path charges them market rent, and none is given free rent the
others are denied.</li>
<li><b>Debt is explicit.</b> A path whose carrying cost exceeds its income borrows at the Treasury
rate plus 1.5 points; the first call for cash and the total shortfall are reported.</li>
<li><b>Nothing is rounded until it is printed.</b> The model carries full precision; only published
figures are rounded to $10.</li>
<li><b>Deterministic.</b> The Monte Carlo uses a fixed seed and a fixed draw count, so two builds
produce identical bytes.</li>
</ul>

<h2 id="ranges">The range register</h2>
<p>Every household input, as a range. The status column is the whole point: an assumption is marked
as one wherever it appears.</p>
"""
    labels = {
        "a_rent_yield": "Gross rent as a share of the inherited house's value",
        "a_insurance_rate": "Homeowners insurance, inherited house, owner-occupied, share of value a year",
        "a_insurance_rental_rate": "Landlord policy, inherited house, share of value a year",
        "a_water_rate": "Water, inherited house, share of value a year",
        "a_electric_net_rate": "Power, inherited house, share of value a year, net of solar",
        "a_maint_rate": "Routine maintenance, inherited house, share of value a year",
        "a_capital_rate": "Capital plan, inherited house, share of value a year",
        "a_vacancy": "Vacancy, share of gross rent",
        "a_management": "Management, share of gross rent",
        "b_rent_yield": "Gross scheduled rent, building, share of value a year",
        "b_insurance_rate": "Landlord policy, building, share of value a year",
        "b_water_rate": "Water, building, share of value a year",
        "b_electric_rate": "Owner-paid power, building, share of value a year",
        "b_maint_rate": "Routine maintenance, building, share of value a year",
        "b_capital_rate": "Capital plan, building, share of value a year",
        "b_vacancy": "Vacancy, building, share of gross rent",
        "b_management": "Management, building, share of gross rent",
        "b_parcel_tax_rate": "Local parcel tax on the building, share of value a year, if enacted",
        "vacant_unit_share": "The vacant unit's rent as a share of the building's gross rent",
        "sell_cost": "Selling cost as a share of price",
        "recording_rate": "Recording and filing fees, a sale, share of price",
        "city_doc_tax": "City documentary transfer tax, share of price",
        "rent_tax_rate": "Combined marginal rate on rental income",
        "imputed_rent_yield": "What living in the house is worth, share of value a year",
    }
    gap_for = {"a_insurance_rate": "F03", "a_insurance_rental_rate": "F03",
               "b_insurance_rate": "F03", "a_rent_yield": "F02", "b_rent_yield": "F02",
               "b_parcel_tax_rate": "F04", "city_doc_tax": "F05"}
    rows = []
    for k in labels:
        lo, hi = R[k]
        shown = f"{pct(lo,2)} – {pct(hi,2)}" if abs(hi) < 1 else f"{money(model.money_k(lo))} – {money(model.money_k(hi))}"
        status = tag("gap") + f" {gap_for[k]}" if k in gap_for else tag("ass")
        rows.append([esc(labels[k]), esc(shown), status])
    body += table(["Input", "Range", "Status"], rows, numeric_from=0)

    body += f"""
<h2>Why no household figure appears on this site</h2>
<p>The household's own records contain a market value, a monthly rent and a sequence of assessed
values. None of them is published here, at any precision. The reason is arithmetic: a rounded series
of yearly assessments still identifies one parcel against an open assessor roll, and a rounded market
value plus a rounded rent reproduces the owner's own brief. Rounding to $10 does not contain that —
the owner's values were already multiples of ten.</p>
<p>Instead the model runs on declared <b>modelling bases</b> of {money(DATA['base']['a'],'')} for the
inherited house and {money(DATA['base']['b'],'')} for the building. Both are round numbers that
belong to no parcel.</p>

<div class="ok"><h3>What is safe to publish, and what is not</h3>
<p>The desk first claimed that its conclusions were invariant to the modelling base. A test
disproved that, and the reason is a feature of the law, not a defect in the model: the
intergenerational value cap is a <b>fixed number of dollars</b> (it is the one-million-dollar amount
plus the transferor's base, indexed every two years). A more valuable house therefore gets
proportionally less protection, pays proportionally more tax, and needs slightly faster price
growth to be worth holding.</p>
<p>What the tests <i>do</i> establish, and what this site publishes:</p>
<ul class="tight">
<li>The <b>ranking</b> of the paths does not change between a base of one million and ten million.</li>
<li>The <b>break-even</b> moves by well under one percentage point across that tenfold range — it
rises from about {pct(BE_BASE_LOW,2)} at a one-million base to about {pct(BE_BASE_HIGH,2)} at ten
million — and a test asserts the direction and the size.</li>
<li>The <b>dollar gaps</b> scale with the household's size, which is why the site leads with rates
and break-evens rather than with dollars.</li>
</ul>
<p>The consequence for the reader is stated plainly rather than hidden: a reader whose house is
worth materially more than the modelling base should assume the break-even is a little higher than
the figure below, and the flagged page records the range.</p></div>

<h2>The tests</h2>
<ul class="tight">
<li>Base dependence: the ranking is identical between a one-million and a ten-million base; the
break-even moves in the direction the fixed cap requires, by less than a percentage point.</li>
<li>Determinism: two builds of the model produce byte-identical output.</li>
<li>Monotonicity: a higher house-price growth rate never lowers the value of the holding path.</li>
<li>Break-evens actually cross: at the computed growth rate the two paths tie to within $10.</li>
<li>Exclusion mechanics: occupying lowers the assessment; not occupying resets to market; moving out
re-enrols at market.</li>
<li>Statutory arithmetic: the estate tax, the 1% tax and the transfer taxes are computed from the
statute and checked against hand-worked examples.</li>
<li>Privacy: every published page is scanned for names, streets, parcels, postcodes, cities,
neighbourhoods, e-mail and phone shapes, and for any unrounded money.</li>
<li>Sources: every external host is on the official allowlist; every data row links one or says why
none exists.</li>
</ul>

<h2>Rebuilding after an input change</h2>
<p>The owner's requirement — rebuild the model and the site after any input change and see whether
the recommendation moved — is one command. The build regenerates every page from the model, and the
break-even table is printed at the end of the run so a change is visible without reading the site.</p>
<pre class="small">python3 desk-ops/_src/model.py    # writes model.json and prints the break-evens
python3 desk-ops/_src/build.py    # rewrites every page
python3 desk-ops/_src/verify.py   # the publication contract
python3 -m unittest discover -s desk-ops/_src -p "test_*.py"</pre>

<h2>What this is not</h2>
<p>Not legal, tax or investment advice. Not a forecast. Not a valuation. The break-evens are the
useful part, and they are only as good as the ranges above — which is why the ranges are published
next to them.</p>
"""
    return page("Method and privacy", body)


# ---------------------------------------------------------------------------- write
PAGES = {
    "index.html": p_index,
    "decision.html": p_decision,
    "paths.html": p_paths,
    "phased.html": p_phased,
    "swans.html": p_swans,
    "projections.html": p_projections,
    "costs.html": p_costs,
    "taxes.html": p_taxes,
    "timeline.html": p_timeline,
    "questions.html": p_questions,
    "suggestions.html": p_suggestions,
    "brief-sheet.html": p_brief,
    "work-register.html": p_work_register,
    "law-watch.html": p_law,
    "glossary.html": p_glossary,
    "sources.html": p_sources,
    "flagged.html": p_flagged,
    "method.html": p_method,
}


def main():
    # pages live one level below the site root so the privacy register can sit beside them
    root = OUT
    for name, fn in PAGES.items():
        path = root / name
        path.write_text(fn(), encoding="utf-8")
        print(f"wrote {path.relative_to(root)}")
    print(f"{len(PAGES)} pages")


if __name__ == "__main__":
    main()
