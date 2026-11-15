# -*- coding: utf-8 -*-
"""Page set 4b: the what-if workbook and the projection charts."""
from __future__ import annotations


def build(x):
    write, h1, table, stat, risk, note = x.write, x.h1, x.table, x.stat, x.risk, x.note
    money10, pct, tag, src, shell = x.money10, x.pct, x.tag, x.src, x.shell
    res, MI, BANDS, REGIMES, DIST, CROSS, PHASE = (
        x.res, x.MI, x.BANDS, x.REGIMES, x.DIST, x.CROSS, x.PHASE)

    # ------------------------------------------------------------------ what would change
    b = [h1("What would change the answer",
            "A recommendation that cannot be overturned is not an analysis, it is a slogan. "
            "Each row below is one change to one input, with the model re-run and the ranking "
            "checked. Where the answer does not move, that is worth knowing too.")]

    b.append('<div class="answer"><div class="k">Short version</div>'
             '<div class="v">Two inputs can overturn the recommendation. Nothing else can.</div>'
             "<p>The recommendation is selling A at the transfer date. It survives every "
             'tax change, every cost change, and a wide range of rents. It does not survive '
             'house prices growing faster than about <strong>%s</strong> a year, and it does '
             'not survive a portfolio that cannot earn about <strong>%s</strong> nominal. Both '
             'of those are plausible. Neither is the base case.</p></div>'
             % (pct(CROSS["2045|P1_vs_P3_house"], 1), pct(CROSS["2045|P1_vs_P3_equity"], 1)))

    b.append("<h2>Inputs tested, and what happens to the ranking</h2>")
    rows = [
        ["House price growth",
         pct(BANDS["house"][0], 1) + " to " + pct(BANDS["house"][1], 1) + " (base "
         + pct(MI["house_growth"], 1) + ")",
         "Living in A overtakes selling above " + pct(CROSS["2045|P1_vs_P3_house"], 1),
         "<strong>Overturns the answer</strong>"],
        ["Equity return",
         pct(BANDS["equity"][0], 1) + " to " + pct(BANDS["equity"][1], 1) + " (base "
         + pct(MI["equity_return"], 1) + ")",
         "Living in A overtakes selling below " + pct(CROSS["2045|P1_vs_P3_equity"], 1),
         "<strong>Overturns the answer</strong>"],
        ["Inflation",
         pct(BANDS["inflation"][0], 1) + " to " + pct(BANDS["inflation"][1], 1),
         "Moves every level, changes no rank ordering on its own",
         "Level only"],
        ["Market rent on A",
         money10(BANDS["a_rent"][0]) + " to " + money10(BANDS["a_rent"][1]) + " a month",
         "Letting A out still ranks last of the three pure choices across the whole band",
         "No change"],
        ["Selling costs",
         pct(BANDS["sell_cost"][0], 0) + " to " + pct(BANDS["sell_cost"][1], 0),
         "Two percentage points is " + money10(
             res(2045, "baseline", "P3")["a_value"] * 0.02) + " at a 2045 transfer: material "
         "but not decisive",
         "No change"],
        ["Property A tax rate",
         pct(MI["a_rate_floor"], 3) + " to " + pct(MI["a_rate_ceil"], 2),
         "Every keeping path worsens as the rate rises; the ordering holds",
         "No change"],
        ["Maintenance reserve",
         pct(BANDS["a_maint"][0], 2) + " to " + pct(BANDS["a_maint"][1], 2) + " of value",
         "Hurts keeping paths only, because a sold house needs no reserve",
         "Widens the gap"],
        ["Transfer date",
         "2040, 2045, 2050",
         "Shifts every level; no rank changes",
         "No change"],
        ["Measure H parcel tax",
         money10(249) + " a year for nine years",
         "A rounding error against both buildings",
         "No change"],
        ["Proposition 19 amount",
         "projected at " + pct(MI["prop19_growth"], 1) + " a year after the published figure",
         "Each dollar of allowance is worth about " + money10(MI["a_rate_base"] * 100)
         + " of annual tax in the first year",
         "No change"],
    ]
    b.append(table(
        "Every input, the range tested, the effect on the ranking, and whether it changes the "
        "recommendation.",
        ["Input", "Range tested", "What moves", "Does the answer change?"], rows))

    b.append(risk(
        "The two overturning inputs are not independent. House prices and equity returns tend to "
        "move together in the short run and diverge over decades, and a scenario where "
        "California house prices compound above %s for twenty years while equities return less "
        "than %s is conceivable but is not a central case. If the household believes it, the "
        "recommendation is to keep the house — and the model agrees, on those inputs."
        % (pct(CROSS["2045|P1_vs_P3_house"], 1), pct(CROSS["2045|P1_vs_P3_equity"], 1)),
        "The two that matter are correlated"))

    b.append("<h2>What does not change the answer, and why that is useful</h2>")
    b.append("<p>Almost every tax question on this desk turns out not to decide anything, "
             "because the same rule applies to both sides of the comparison. The step-up in "
             "basis applies to A whether the household keeps it or sells it. Proposition 19 "
             "applies to occupancy, and occupancy is a separate choice. Measure H applies to B "
             "regardless. Recognising which questions are decisive and which are merely "
             "interesting is most of the value of doing this at all.</p>")

    b.append(note(
        "The decisive questions, in order of how much they move the answer: what happens to "
        "house prices, what the portfolio earns, how long the household actually stays, and how "
        "much the household spends. The first two cannot be known. The third and fourth are "
        "choices. That is where attention belongs.", "good"))

    write("what-would-change.html", shell("what-would-change.html",
                                          "What would change the answer",
                                          "\n".join(b)))

    # ------------------------------------------------------------------ charts
    b = [h1("Projection charts",
            "One picture per question. The distribution charts show every outcome across a grid "
            "of assumptions, not one line. Where two paths overlap, the ranking between them is "
            "not a fact about the future, it is a fact about the assumptions.")]

    def bars(title, sub, items, fmt="money"):
        """items: list of (label, lo, med, hi, scale_max)"""
        mx = max(i[4] for i in items)
        out = ['<div class="chart">', '<div class="ttl">%s</div>' % title,
               '<div class="sub">%s</div>' % sub, '<div class="bars">']
        for label, lo, med, hi, _ in items:
            left = max(0.0, lo / mx) * 100.0
            width = max(0.6, (hi - lo) / mx * 100.0)
            out.append(
                '<div class="bar-row"><div class="lb">%s</div>'
                '<div class="tr"><div class="fl" style="left:%.2f%%;width:%.2f%%"></div>'
                '<div class="md" style="left:%.2f%%"></div></div>'
                '<div class="vl">%s</div></div>'
                % (label, left, width, med / mx * 100.0,
                   money10(med) if fmt == "money" else med))
        out.append('</div>')
        out.append('<div class="axis"><span>%s</span><span>%s</span></div>'
                   % (money10(0), money10(mx)))
        out.append('</div>')
        return "\n".join(out)

    items = []
    for pid in ("P1", "P2", "P3", "P4", "P4b", "P5", "P6", "P6b", "P7"):
        v = DIST["2045|%s" % pid]
        items.append((pid, v[2], v[len(v) // 2], v[-3], max(DIST["2045|%s" % q][-3]
                                                           for q in
                                                           ("P1", "P2", "P3", "P4", "P4b",
                                                            "P5", "P6", "P6b", "P7"))))
    b.append(bars(
        "Net worth including shelter, twenty years from a 2045 transfer",
        "Bar spans the 10th to 90th percentile across a five-by-five grid of house growth "
        "(1.5% to 5.5%) and equity return (4.0% to 9.0%). The dark line is the median.",
        items))
    b.append(note(
        "The bars overlap heavily. The distance between the medians of the best and worst pure "
        "choices is smaller than the width of either bar, which is the honest summary of this "
        "whole exercise: the decision matters, but not as much as the market does.", "good"))

    b.append("<h2>Where the ranking flips</h2>")
    rows = []
    for t in x.TRANSFER_YEARS:
        rows.append([
            str(t),
            ("num", pct(CROSS["%d|P1_vs_P3_house" % t], 1)),
            ("num", pct(CROSS["%d|P4_vs_P3_house" % t], 1)),
            ("num", pct(CROSS["%d|P1_vs_P3_equity" % t], 1)),
            ("num", pct(CROSS["%d|P5_vs_P3_house" % t], 1)),
        ])
    b.append(table(
        "The house-price growth rate at which each keeping path overtakes selling at once, and "
        "the equity return below which living in A wins.",
        ["Transfer", "#Living in A beats selling above", "#Live 5 then sell beats selling above",
         "#Living in A beats selling below equity", "#Let 10 then sell beats selling above"],
        rows,
        note="Read across: the thresholds are stable across transfer dates, which is what makes "
             "them usable. Read down the second column: a household that expects 6% house price "
             "growth should keep the house."))

    # distribution across regimes for the three pure choices
    b.append("<h2>The three pure choices under each regime</h2>")
    items = []
    mx = 0
    for rk in ("baseline", "high_inflation", "deflation_1930s", "great_recession",
               "stagnation"):
        for pid in ("P1", "P2", "P3"):
            mx = max(mx, res(2045, rk, pid)["net_worth_with_shelter"])
    for rk in ("baseline", "high_inflation", "deflation_1930s", "great_recession",
               "stagnation"):
        vals = [res(2045, rk, p)["net_worth_with_shelter"] for p in ("P1", "P2", "P3")]
        items.append((REGIMES[rk]["label"][:26], min(vals), sorted(vals)[1], max(vals), mx))
    b.append(bars(
        "Range across the three pure choices, by regime",
        "For each regime: the lowest and highest of living in A, letting A out, and selling at "
        "once, with the middle value marked. Twenty years from a 2045 transfer.",
        items))

    b.append(risk(
        "This chart is the strongest argument for not treating the recommendation as settled. "
        "In three of five regimes the lowest pure choice still leaves more than the highest pure "
        "choice does in another. A household that cannot tolerate the spread should not be "
        "making a twenty-year decision on a point estimate at all.",
        "The spread dominates the ranking"))

    b.append("<h2>Parking and phasing, in one picture</h2>")
    items = []
    mx = 0
    for r in PHASE:
        if r["regime"] != "baseline":
            continue
        mx = max(mx, max(r["buy_once"], r["park24"]))
    for r in PHASE:
        if r["regime"] != "baseline":
            continue
        items.append(("Buy at once, %d" % r["transfer_year"], r["buy_once"],
                      r["buy_once"], r["buy_once"], mx))
        items.append(("Park 24m, %d" % r["transfer_year"], r["park24"], r["park24"],
                      r["park24"], mx))
    b.append(bars(
        "One dollar invested at the transfer date, twenty years later",
        "A 35% equity fall at month 12, comparing buying at once with parking in Treasuries for "
        "24 months and then phasing in over 24 months.",
        items))

    write("charts.html", shell("charts.html", "Projection charts", "\n".join(b)))

    # ------------------------------------------------------------------ workbook
    b = [h1("Workbook: every input, its status, and what happens if it moves",
            "This is the page to argue with. Every number the model uses appears once, with "
            "where it came from, and with a note on what it would take to replace it with "
            "something better. Anything marked assumption is a placeholder for a fact the "
            "household does not yet have.")]

    b.append("<h2>Property inputs</h2>")
    b.append(table(
        "Owner-supplied and property-level inputs. Owner figures are rounded and labelled: they "
        "are the household's own estimates, not appraisals or bills as issued.",
        ["Input", "Value used", "Status", "How to replace it with something verified"],
        [
            ["Property A value, November 2026", ("num", money10(MI["a_value"])), tag("own"),
             "Two independent appraisals, or the county's assessed value plus a market "
             "adjustment. Question 1 on <a href=\"questions.html\">gaps</a>."],
            ["Property A assessed value", ("num", money10(MI["a_assessed"])),
             tag("own", "owner, rounded"), "The tax bill itself. Not obtained."],
            ["Property A tax rate", ("num", pct(MI["a_rate_base"], 3) + " (band "
                                     + pct(MI["a_rate_floor"], 3) + "-"
                                     + pct(MI["a_rate_ceil"], 2) + ")"), tag("drv"),
             "The tax rate area number printed on the bill, looked up in the county's annual "
             "tax rate book."],
            ["Property B value, November 2026", ("num", money10(MI["b_value"])), tag("own"),
             "Independent appraisal; a three-unit building is valued on income as well as "
             "comparables."],
            ["Property B assessed value", ("num", money10(MI["b_assessed"])),
             tag("own", "owner, rounded"), "The tax bill."],
            ["Property B rent, two units", ("num", money10(MI["b_rent_mo"]) + "/mo"), tag("own"),
             "The leases themselves. The desk has not seen them; see "
             "<a href=\"local-rules.html\">local rules</a>."],
            ["Property B non-ad-valorem add-on", ("num", money10(MI["b_addon"])), tag("drv"),
             "The bill broken out by line, which shows the parcel taxes and assessments "
             "individually."],
            ["Insurance, both buildings", ("num", money10(1500) + " each"), tag("own"),
             "Two current declarations pages. An owner-occupied policy and a landlord policy "
             "are not the same product or the same price."],
            ["Water and electricity, both buildings", ("num", "see building pages"), tag("own"),
             "Twelve months of utility bills."],
        ]))

    b.append("<h2>Market assumptions</h2>")
    b.append(table(
        "Assumptions about the future. None of these is knowable, all of them are ranges, and "
        "the model's ranking has been tested across the whole of each range.",
        ["Input", "Base", "Range tested", "Status", "Why this base"],
        [
            ["House price growth, both buildings", ("num", pct(MI["house_growth"], 1)),
             pct(BANDS["house"][0], 1) + " to " + pct(BANDS["house"][1], 1), tag("asm"),
             "Roughly the long-run nominal growth of US house prices. The FHFA publishes the "
             "index that would replace this with a measured figure. " + src("fhfa_hpi")],
            ["Equity return, nominal", ("num", pct(MI["equity_return"], 1)),
             pct(BANDS["equity"][0], 1) + " to " + pct(BANDS["equity"][1], 1), tag("asm"),
             "A diversified portfolio of mostly equities, before tax and before fees. "
             "Deliberately not a forecast of any index."],
            ["Inflation", ("num", pct(MI["inflation"], 1)),
             pct(BANDS["inflation"][0], 1) + " to " + pct(BANDS["inflation"][1], 1), tag("asm"),
             "The 1913-2026 compound average of the CPI-U, computed on this desk from the BLS "
             "series. " + src("bls_cpi")],
            ["Market rent on A", ("num", money10(MI["a_rent_mo"]) + "/mo"),
             money10(BANDS["a_rent"][0]) + " to " + money10(BANDS["a_rent"][1]), tag("asm"),
             "No comparables obtained. This is the weakest number on the desk and every "
             "letting path is a floor because of it."],
            ["Maintenance and capital, A", ("num", pct(MI["a_maint"], 2) + " of value"),
             pct(BANDS["a_maint"][0], 2) + " to " + pct(BANDS["a_maint"][1], 2), tag("asm"),
             "A reserve study or three contractor quotes would replace it."],
            ["Maintenance and capital, B", ("num", pct(MI["b_maint"], 2) + " of value"),
             pct(BANDS["b_maint"][0], 2) + " to " + pct(BANDS["b_maint"][1], 2), tag("asm"),
             "Older three-unit building; more common areas, more systems."],
            ["Selling costs", ("num", pct(MI["sell_cost"], 0) + " of price"),
             pct(BANDS["sell_cost"][0], 0) + " to " + pct(BANDS["sell_cost"][1], 0), tag("asm"),
             "Commission, escrow, title. Two broker quotes would replace it."],
            ["Building share of value for depreciation",
             ("num", pct(0.60, 0)), "50% to 70%", tag("asm"),
             "An appraisal allocating land and improvements."],
            ["Treasury yield for parking", ("num", pct(MI["treasury_2y"], 2) + " for 2 years"),
             "current curve", tag("ok"),
             "Observed 13 November 2026, not a forecast. " + src("treasury_yields")],
            ["Proposition 19 amount after 2027",
             ("num", pct(MI["prop19_growth"], 1) + " a year"), "0% to 4%", tag("asm"),
             "The Board of Equalization announces each figure two years ahead; the 2027 figure "
             "does not exist yet. " + src("boe_lta25009")],
        ]))

    b.append("<h2>Tax parameters</h2>")
    b.append(table(
        "Statutory inputs. These are quoted exactly and marked, because rounding a threshold "
        "misstates it.",
        ["Input", "Value", "Applied to", "Source"],
        [
            ["Federal long-term capital gain, top rate", ("num", pct(0.20, 0)),
             "Gain on a sale not sheltered by the step-up or section 121", src("irs_t409")],
            ["Net investment income tax", ("num", pct(0.038, 1)),
             "Same gain, plus portfolio income (not modelled)", src("irs_t559")],
            ["California top rate", ("num", pct(0.123, 1)), "All gain, no preferential rate",
             src("ftb_capgains")],
            ["California Behavioral Health Services Tax", ("num", pct(0.01, 1)),
             "Taxable income above " + money10(1000000, exact="1,000,000"),
             src("rtc_17043")],
            ["Unrecaptured section 1250 rate", ("num", pct(0.25, 0)),
             "Depreciation taken on a rental", src("irs_t409")],
            ["Section 121 exclusion, single", ("num", money10(250000, exact="250,000")),
             "Live-then-sell paths", src("irs_p523")],
            ["Proposition 13 cap", ("num", pct(0.02, 0) + " a year"), "Both assessed values",
             src("scc_assessor_booklet")],
            ["Documentary transfer tax", ("num", "0.11% (county)"),
             "Sale of A; city rate not added because none is verified", src("rtc_11911")],
            ["Measure H, multifamily base", ("num", money10(249, exact="249")),
             "Property B from fiscal 2027-28", src("sf_propH_text")],
            ["Electricity and gas deduction ceiling", ("num", "not modelled"), "—",
             '<span class="tag-none">out of scope</span>'],
        ]))

    b.append("<h2>What the model does not include</h2>")
    b.append("<ul>"
             "<li><strong>Tax on portfolio income.</strong> Dividends, interest and realised gains "
             "inside the portfolio are taxed annually. The model uses a gross return.</li>"
             "<li><strong>Fees.</strong> An adviser charging 1 percent a year on a portfolio of "
             "this size would consume about a fifth of the assumed real return.</li>"
             "<li><strong>Vacancy longer than the allowance.</strong> A 5 percent vacancy "
             "allowance on A; a longer vacancy in a soft rental market would hurt.</li>"
             "<li><strong>Rent control and eviction costs.</strong> A three-unit building in San "
             "Francisco is subject to the rent ordinance. Not modelled.</li>"
             "<li><strong>Long-term care and health costs.</strong> The largest financial risk in "
             "most households this age, and entirely outside this decision.</li>"
             "<li><strong>The trust.</strong> No term of the trust instrument was read. The desk "
             "assumes A passes outright with basis reset.</li>"
             "</ul>")
    b.append(note(
        "Every omission above pushes in the same direction: they make the sell-and-invest path "
        "look better than it is. Presenting them plainly is the only honest way to publish a "
        "recommendation that favours that path.", "good"))

    write("workbook.html", shell("workbook.html",
                                 "Workbook: every input, its status, and what happens if it moves",
                                 "\n".join(b)))
