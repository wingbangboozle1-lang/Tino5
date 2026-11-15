# -*- coding: utf-8 -*-
"""Page set 1: the decision, the two properties, and the comparison table."""
from __future__ import annotations


def build(x):
    write = x.write
    h1, table, stat, risk, note = x.h1, x.table, x.stat, x.risk, x.note
    money10, pct, tag, src = x.money10, x.pct, x.tag, x.src
    res, best, ranked = x.res, x.best, x.ranked
    shell, ALL_PAGES = x.shell, x.ALL_PAGES

    HORIZON = x.HORIZON
    p1_45 = res(2045, "baseline", "P1")
    p3_45 = res(2045, "baseline", "P3")
    p2_45 = res(2045, "baseline", "P2")
    gap = p3_45["net_worth_with_shelter"] - p1_45["net_worth_with_shelter"]
    hi = best(2045, "high_inflation")
    gr = best(2045, "great_recession")
    st = best(2045, "stagnation")

    # ------------------------------------------------------------------ index
    b = [h1("Live in it, rent it out, or sell it?",
            "Two California homes and one future inheritance, compared on the same dates, "
            "the same horizon and the same tax treatment. Property A is a house in Santa "
            "Clara County, expected through a trust between 2040 and 2050. Property B is a "
            "three-unit building in San Francisco County, already owned: two units are let "
            "and the owner may take the third without losing that rent.")]

    b.append(
        '<div class="answer"><div class="k">The answer, on the central assumptions</div>'
        '<div class="v">Selling A at the transfer date ranks first — but the margin over '
        'keeping it is inside the error bars.</div>'
        '<p>Ranked at a 2045 transfer over twenty years: sell at once '
        '<strong>%(p3)s</strong>, live in A <strong>%(p1)s</strong>, let A out '
        '<strong>%(p2)s</strong>. The sell advantage over living in A is %(gap)s over '
        'twenty years, about %(yr)s a year. That is a real difference, but it turns on house '
        'price growth staying below about %(cx)s a year — see '
        '<a href="what-would-change.html">what would change the answer</a>.</p>'
        '<p>The more stable finding: <strong>letting A out is the weakest of the three pure '
        'choices at every transfer date under the baseline</strong>, and it loses to living '
        'in A in every regime tested. At %(aval)s of value against roughly %(arent)s a year '
        'of rent, a house here yields under 3%% gross. The building cannot pay for itself at '
        'these prices, and the tax code rewards owning it as a home, not as a rental.</p>'
        '<p><strong>Property B is not part of that comparison and must not be.</strong> '
        'It is already owned. Moving into B does not produce the same gain as inheriting A, '
        'because a change of residence inside a building the household already owns does not '
        'reset its assessed value. The two are separated on '
        '<a href="own-vs-inherit.html">why they are not comparable</a>.</p></div>'
        % dict(p3=money10(p3_45["net_worth_with_shelter"]),
               p1=money10(p1_45["net_worth_with_shelter"]),
               p2=money10(p2_45["net_worth_with_shelter"]),
               gap=money10(gap), yr=money10(gap / HORIZON),
               cx=pct(x.CROSS["2045|P1_vs_P3_house"], 1),
               aval=money10(x.MI["a_value"]), arent=money10(x.MI["a_rent_mo"] * 12)))

    b.append(risk(
        "Every headline on this desk is a portfolio outcome, and every portfolio outcome "
        "here depends on what happens to the money after the sale. Selling A and buying "
        "equities converts a building the household can touch into a price series it cannot "
        "control. That risk sits beside each headline below, not at the end of the document.",
        "Reinvestment risk, stated before the numbers"))

    b.append('<h2>The three pure choices, at one glance</h2>')
    rows = []
    for pid in ("P1", "P2", "P3"):
        r = res(2045, "baseline", pid)
        rows.append([
            "<strong>%s</strong> %s" % (pid, r["label"]),
            ("num", money10(r["net_worth_with_shelter"])),
            ("num", money10(r["financial"])),
            ("num", money10(r["a_final"] + r["b_final"])),
            ("num", money10(r["shelter"])),
        ])
    b.append(table(
        "One household, one transfer date, twenty years. Net worth includes the shelter the "
        "household consumes, valued at market rent, so no path gets free housing.",
        ["Path", "#Net worth incl. shelter", "#Financial assets", "#Property held",
         "#Shelter consumed"],
        rows,
        note="Transfer at 2045. Central assumptions: house price growth %s a year, equity "
             "return %s, inflation %s. All three are planning assumptions, not forecasts, "
             "and every one of them is a range on "
             "<a href=\"workbook.html\">the workbook</a>."
             % (pct(x.MI["house_growth"], 1), pct(x.MI["equity_return"], 1),
                pct(x.MI["inflation"], 1))))

    b.append('<h2>The recommendation, stated as a sequence</h2>')
    b.append("<ol>"
             "<li><strong>Sell A at the transfer date.</strong> Basis resets to market value "
             "at death, so a sale in the same tax year as the inheritance produces no "
             "meaningful capital gain. Waiting converts a tax-free step-up into a taxable "
             "gain. See <a href=\"income-basis.html\">income tax and basis</a>.</li>"
             "<li><strong>Do not occupy A to capture the Proposition 19 exclusion unless the "
             "household genuinely intends to live there for years.</strong> The exclusion "
             "requires occupancy as a principal residence within one year and an exemption "
             "claim within one year; taking it and then leaving can cost the whole benefit "
             "back. See <a href=\"prop19.html\">Proposition 19</a>.</li>"
             "<li><strong>Write the investment policy before the money arrives.</strong> The "
             "single largest controllable risk is what the household does in the first "
             "eighteen months after a sale it did not plan for. See "
             "<a href=\"investment-policy.html\">policy for the proceeds</a>.</li>"
             "<li><strong>Move into B's third unit, or stay put, before touching A.</strong> "
             "That decision is free, reversible and independent of the inheritance.</li>"
             "<li><strong>Do not sell B.</strong> It carries a pre-1978-style assessed base in "
             "practice and a rent roll that funds the household's own housing. Selling it "
             "would convert sheltered cash flow into a taxable gain.</li></ol>")

    b.append('<h2>Where the answer flips</h2>')
    b.append(table(
        "Each row is a single change from the central case. The model is re-run at the same "
        "transfer date and horizon.",
        ["Change one thing", "New leader", "#Net worth incl. shelter", "Reading"],
        [
            ["House price growth above %s" % pct(x.CROSS["2045|P1_vs_P3_house"], 1),
             "Live in A", ("num", money10(x.best_at(2045, "baseline", "house",
                                                   x.CROSS["2045|P1_vs_P3_house"] + 0.005)[1])),
             "A appreciating faster than the assumed rate beats selling, because the "
             "house is bought with pre-tax dollars and carries an assessed value far below "
             "its market value."],
            ["Equity return below %s" % pct(x.CROSS["2045|P1_vs_P3_equity"], 1),
             "Live in A", ("num", money10(x.best_at(2045, "baseline", "equity",
                                                   x.CROSS["2045|P1_vs_P3_equity"] - 0.005)[1])),
             "If a balanced portfolio cannot clear roughly 4.5% nominal, the house wins on "
             "cash-flow grounds alone."],
            ["The 1972-1982 inflation record repeats", "Live in A",
             ("num", money10(hi["net_worth_with_shelter"])),
             "High inflation with poor real returns on financial assets is the one regime "
             "where the house is decisively the best place for the money."],
            ["A 2007-2009 style credit shock", "Live in A",
             ("num", money10(gr["net_worth_with_shelter"])),
             "A crash early in the holding period destroys the sell-and-invest case."],
            ["No crash and no boom", "Park, then phase in",
             ("num", money10(st["net_worth_with_shelter"])),
             "In a dull market the phased path edges out buying at once."],
        ],
        note="All values are twenty-year outcomes at a 2045 transfer under the stated regime. "
             "The full grid is on <a href=\"charts.html\">projection charts</a>."))

    b.append('<h2>What this desk will not tell you</h2>')
    b.append(note(
        "It will not tell you what A is worth. The household's figure of %s is an anchor "
        "supplied by the owner, not an appraisal, and it is unverified. It will not tell you "
        "what A would rent for: no independent comparables were obtained, so the rent figure "
        "is a labelled assumption and every letting path is a <em>floor</em>, not an "
        "estimate. It will not price the trust, because the trust instrument has not been "
        "read. Those gaps are listed, with the action that closes each one, on "
        "<a href=\"questions.html\">questions and gaps</a>."
        % money10(x.MI["a_value"]), "good"))

    b.append('<h2>Read it in the order you need it</h2>')
    b.append('<div class="cards">'
             '<div class="card"><h3>If you have five minutes</h3>'
             '<p><a href="choices.html">All choices, same dates</a> and '
             '<a href="what-would-change.html">what would change the answer</a>.</p>'
             '<div class="meta">Two pages, both printable.</div></div>'
             '<div class="card"><h3>If you are the attorney</h3>'
             '<p><a href="briefing-attorney.html">One-page briefing sheet</a>: title, '
             'trust mechanics, Proposition 19 occupancy conditions, the dates.</p>'
             '<div class="meta">Fits on one page at A4 or Letter.</div></div>'
             '<div class="card"><h3>If you are the CPA</h3>'
             '<p><a href="briefing-cpa.html">One-page briefing sheet</a>: basis, section 121, '
             'depreciation recapture, state treatment, estimated return dates.</p>'
             '<div class="meta">Fits on one page at A4 or Letter.</div></div>'
             '<div class="card"><h3>If you want the arithmetic</h3>'
             '<p><a href="workbook.html">The workbook</a> lists every input, its status and '
             'its range, and <a href="methodology.html">method and rounding</a> explains how '
             'the numbers were produced.</p>'
             '<div class="meta">No value on this desk is a black box.</div></div>'
             '</div>')

    write("index.html", shell("index.html", "Live in it, rent it out, or sell it?",
                              "\n".join(b)))
