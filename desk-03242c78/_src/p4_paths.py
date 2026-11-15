# -*- coding: utf-8 -*-
"""Page set 4: the path pages, the what-if workbook, and the charts."""
from __future__ import annotations


def build(x):
    write, h1, table, stat, risk, note = x.write, x.h1, x.table, x.stat, x.risk, x.note
    money10, pct, tag, src, shell = x.money10, x.pct, x.tag, x.src, x.shell
    res, MI, BANDS, REGIMES, DIST, CROSS, PHASE = (
        x.res, x.MI, x.BANDS, x.REGIMES, x.DIST, x.CROSS, x.PHASE)

    # ------------------------------------------------------------------ live path
    p1 = res(2045, "baseline", "P1")
    p3 = res(2045, "baseline", "P3")
    b = [h1("Live in Property A",
            "Move in, keep the assessed value, and let all three units at B. This is the only "
            "path that captures the Proposition 19 exclusion, and it is also the only path where "
            "the household's own housing is the asset under discussion.")]

    b.append('<div class="stats">')
    b.append(stat("Net worth incl. shelter, 2045", money10(p1["net_worth_with_shelter"]),
                  "20 years from transfer"))
    b.append(stat("Annual property tax after moving in", money10(p1["a_annual_tax_now"]),
                  "owner-implied rate"))
    b.append(stat("Proposition 19 relief", money10(p1["prop19_relief"]),
                  "assessed value kept off the roll"))
    b.append(stat("Rent collected at B", money10(MI["b_rent_mo"] / 2 * 3 * 12),
                  "all three units let"))
    b.append('</div>')

    b.append(risk(
        "This path puts most of the household's net worth into one building in one county, at "
        "an assessed value that only stays low while the house stays occupied. It is "
        "concentrated, illiquid, and conditional. The financial case for it is a bet on "
        "California house prices growing faster than %s a year. If they do not, selling wins."
        % pct(CROSS["2045|P1_vs_P3_house"], 1),
        "The risk in this path"))

    b.append("<h2>Why it wins in bad markets and loses in good ones</h2>")
    b.append("<p>Living in A converts the household's largest future expense — housing — into "
             "something it already owns. When financial assets do badly, that is worth more than "
             "any portfolio. When they do well, the house cannot keep up: it is one asset, "
             "undiversified, with carrying costs and a cap on how fast its tax basis can rise. "
             "The model reflects exactly that.</p>")
    b.append(table(
        "Living in A, ranked against all nine paths under each regime at a 2045 transfer.",
        ["Regime", "Rank of living in A", "#Net worth incl. shelter", "#Leader",
         "#Leader's net worth"],
        [
            [REGIMES[rk]["label"], ("num", "%d of 9" % x.rank_of(2045, rk, "P1")),
             ("num", money10(res(2045, rk, "P1")["net_worth_with_shelter"])),
             x.best(2045, rk)["label"],
             ("num", money10(x.best(2045, rk)["net_worth_with_shelter"]))]
            for rk in ("baseline", "high_inflation", "deflation_1930s",
                       "great_recession", "stagnation")
        ]))

    b.append("<h2>The conditions attached</h2>")
    b.append(table(
        "Everything that must be true, and stay true, for this path to work as modelled.",
        ["Condition", "Deadline or duration", "Consequence of failure", "Source"],
        [
            ["Occupy as principal residence", "within one year of the transfer",
             "The exclusion is lost and the house is reassessed at market value, raising the "
             "annual tax from about %s to about %s."
             % (money10(p1["a_annual_tax_now"]),
                money10(p1["a_taxable"] * MI["a_rate_base"])),
             src("rtc_63_2")],
            ["File the homeowners' or disabled veterans' exemption",
             "within one year; the exemption itself is claimed by 15 February",
             "The exclusion is conditioned on the claim. A missing claim is the most common way "
             "to lose it.", src("rtc_63_2", "scc_assessor_booklet")],
            ["Continue to occupy", "every year until the house is sold",
             "Reassessment as of the date eligibility ends, with a supplemental bill.",
             src("rtc_63_2")],
            ["Maintain the building", "continuously",
             "A deferred roof or sewer becomes a discount at sale. The five-year plan budgets "
             "about %s a year." % money10(MI["a_value"] * MI["a_maint"]),
             '<span class="tag-asm">assumption</span>'],
            ["Insure it as an owner-occupied home", "from the transfer date",
             "Landlord policies cost more and cover different things; a gap in coverage is "
             "uninsured loss.", tag("none", "no source needed")],
        ]))

    b.append("<h2>What living there actually costs</h2>")
    b.append(table(
        "The household's own housing, valued at what it would pay to rent the same house.",
        ["Year", "#Property tax", "#Insurance", "#Water and power", "#Maintenance",
         "#Total outlay", "#Rent forgone"],
        [
            ["Year 1", ("num", money10(p1["a_annual_tax_now"])), ("num", money10(1500)),
             ("num", money10((130 + 0) * 12)), ("num", money10(MI["a_value"] * MI["a_maint"])),
             ("num", money10(p1["a_annual_tax_now"] + 1500 + 130 * 12
                             + MI["a_value"] * MI["a_maint"])),
             ("num", money10(MI["a_rent_mo"] * 12))],
            ["Year 20", ("num", money10(p1["a_annual_tax_now"] * 1.02 ** 19)),
             ("num", money10(1500 * 1.027 ** 19)),
             ("num", money10(130 * 12 * 1.027 ** 19)),
             ("num", money10(MI["a_value"] * 1.035 ** 19 * MI["a_maint"])),
             ("num", money10(p1["a_annual_tax_now"] * 1.02 ** 19 + 1500 * 1.027 ** 19
                             + 130 * 12 * 1.027 ** 19
                             + MI["a_value"] * 1.035 ** 19 * MI["a_maint"])),
             ("num", money10(MI["a_rent_mo"] * 12 * 1.027 ** 19))],
        ],
        note="The rent-forgone column is what the household would pay to rent an equivalent "
             "house, which is what it saves by owning. It is the economic benefit of this path "
             "and it is counted in the net worth figure above. It is not cash."))

    b.append("<h2>Mixed versions of living there</h2>")
    b.append('<p>Living in A does not have to be permanent. The model also runs two variants:</p>')
    b.append(table(
        "Living in A and then selling, against living in A for the whole horizon.",
        ["Path", "#Years lived in", "#Section 121 used", "#Net worth incl. shelter",
         "#Difference from living throughout"],
        [
            ["Live in A throughout", ("num", "20"), ("num", money10(0)),
             ("num", money10(res(2045, "baseline", "P1")["net_worth_with_shelter"])),
             ("num", money10(0))],
            ["Live 5 years, then sell", ("num", "5"),
             ("num", money10(res(2045, "baseline", "P4")["sec121_used"])),
             ("num", money10(res(2045, "baseline", "P4")["net_worth_with_shelter"])),
             ("num", money10(res(2045, "baseline", "P4")["net_worth_with_shelter"]
                             - res(2045, "baseline", "P1")["net_worth_with_shelter"]))],
            ["Live 10 years, then sell", ("num", "10"),
             ("num", money10(res(2045, "baseline", "P4b")["sec121_used"])),
             ("num", money10(res(2045, "baseline", "P4b")["net_worth_with_shelter"])),
             ("num", money10(res(2045, "baseline", "P4b")["net_worth_with_shelter"]
                             - res(2045, "baseline", "P1")["net_worth_with_shelter"]))],
        ],
        note="All three satisfy the Proposition 19 occupancy condition, and the two that sell "
             "also satisfy the section 121 use test. A household that intends to stay five to "
             "ten years gets both benefits, which is why the mixed paths score above either "
             "extreme."))

    write("live-path.html", shell("live-path.html", "Live in Property A", "\n".join(b)))

    # ------------------------------------------------------------------ rent path
    p2 = res(2045, "baseline", "P2")
    b = [h1("Rent Property A out",
            "Let the house and move into B's third unit. This is the only path that collects "
            "rent from both properties while housing the household for free — and it is the "
            "worst of the three pure choices in every regime tested.")]

    b.append('<div class="stats">')
    b.append(stat("Net worth incl. shelter, 2045", money10(p2["net_worth_with_shelter"]), ""))
    b.append(stat("Gross rent from A", money10(MI["a_rent_mo"] * 12) + "/yr",
                  "labelled assumption"))
    b.append(stat("Gross yield on A", pct(MI["a_rent_mo"] * 12 / MI["a_value"], 2),
                  "before a single expense"))
    b.append(stat("Rank among nine paths", "%d of 9" % x.rank_of(2045, "baseline", "P2"),
                  "baseline, 2045"))
    b.append('</div>')

    b.append(risk(
        "The rent figure is a floor, not an estimate. No independent comparables were obtained "
        "for Property A, so the model uses %s a month, inside a %s to %s band. If actual rent is "
        "at the top of the band the path improves by about %s over twenty years — still not "
        "enough to pass selling. If it is at the bottom, the path is worse than shown."
        % (money10(MI["a_rent_mo"]), money10(6000), money10(9000), "a modest amount"),
        "The central number here is unverified"))

    b.append("<h2>The arithmetic that decides it</h2>")
    b.append(table(
        "What the house produces against what it costs, in the first year, in today's dollars.",
        ["Line", "#Annual", "Status", "Note"],
        [
            ["Gross rent", ("num", money10(MI["a_rent_mo"] * 12)), tag("asm"),
             "A labelled assumption, $6,000-$9,000 a month. No comparables obtained."],
            ["Vacancy allowance", ("num", money10(-MI["a_rent_mo"] * 12 * 0.05)), tag("asm"),
             "5% of gross rent. A single-family rental turns over roughly every two to three "
             "years and can sit empty for a month or more."],
            ["Property tax", ("num", money10(p2["a_annual_tax_now"])), tag("drv"),
             "At market value, because no exclusion applies."],
            ["Insurance, landlord policy", ("num", money10(-2400)), tag("asm"),
             "A landlord policy costs more than an owner policy. The owner's $1,500 estimate is "
             "for an owner-occupied policy."],
            ["Water and power", ("num", money10(-(130) * 12)), tag("own"),
             "If the owner pays. Many single-family rentals pass utilities to the tenant."],
            ["Maintenance and capital", ("num", money10(-MI["a_value"] * MI["a_maint"])),
             tag("asm"), "0.60% of value a year; a rental is maintained to a lower standard "
             "than an owner-occupied home but wears faster."],
            ["Net operating income", ("num", money10(
                MI["a_rent_mo"] * 12 * 0.95 - p2["a_annual_tax_now"] - 2400 - 130 * 12
                - MI["a_value"] * MI["a_maint"])), tag("drv"),
             "Before income tax on the rent, and before depreciation."],
            ["Same figure as a yield on value",
             ("num", pct((MI["a_rent_mo"] * 12 * 0.95 - p2["a_annual_tax_now"] - 2400
                          - 130 * 12 - MI["a_value"] * MI["a_maint"]) / MI["a_value"], 2)),
             tag("drv"), "Compare with the two-year Treasury at " + pct(MI["treasury_2y"], 2)
             + ", which requires no tenant, no roof and no eviction. " + src("treasury_yields")],
        ]))

    b.append("<h2>The three reasons this path loses</h2>")
    b.append("<ol>"
             "<li><strong>The yield is below the risk-free rate.</strong> A house worth %s that "
             "rents for %s a year yields %s gross. After tax, insurance, water and maintenance it "
             "yields roughly %s. A two-year Treasury yielded %s on 13 November 2026. The "
             "house is not an income asset at this price; it is a price-growth bet with a "
             "carrying cost.</li>"
             "<li><strong>No exclusion, no step-up.</strong> The rental produces no Proposition "
             "19 relief and forfeits section 121, and the depreciation it does take is "
             "recaptured at 25 percent on sale.</li>"
             "<li><strong>It ties up the household's housing decision.</strong> The household "
             "lives in B's third unit, which is fine, but the arrangement couples two buildings "
             "that were meant to be separate decisions.</li>"
             "</ol>"
             % (money10(MI["a_value"]), money10(MI["a_rent_mo"] * 12),
                pct(MI["a_rent_mo"] * 12 / MI["a_value"], 2),
                pct((MI["a_rent_mo"] * 12 * 0.95 - p2["a_annual_tax_now"] - 2400 - 130 * 12
                     - MI["a_value"] * MI["a_maint"]) / MI["a_value"], 2),
                pct(MI["treasury_2y"], 2)))

    b.append("<h2>When it would win</h2>")
    b.append(table(
        "Conditions that would reverse the conclusion on letting A out.",
        ["Condition", "Threshold in the model", "Why it helps"],
        [
            ["Rent much higher than assumed",
             "Roughly " + money10(MI["a_value"] * 0.045 / 12) + " a month, about "
             + pct(0.045 / (MI["a_rent_mo"] * 12 / MI["a_value"]) - 1, 0) + " above the "
             "assumption, to reach a 4.5% net yield",
             "At that rent the house pays for itself and the price-growth bet becomes optional "
             "rather than necessary."],
            ["House prices grow faster than " + pct(CROSS["2045|P2_vs_P3_house"], 1) + " a year",
             pct(CROSS["2045|P2_vs_P3_house"], 1),
             "Capital appreciation, not rent, becomes the return."],
            ["The household needs the house kept in the family",
             "not a financial threshold",
             "The model can price a decision but it cannot price a reason."],
        ],
        note="The rent threshold is computed from the net-yield target, not from the model's "
             "ranking, and is shown as an arithmetic consequence of the assumption."))

    write("rent-path.html", shell("rent-path.html", "Rent Property A out", "\n".join(b)))

    # ------------------------------------------------------------------ sell path
    p3 = res(2045, "baseline", "P3")
    b = [h1("Sell Property A and reinvest",
            "Sell at the transfer date, pay the costs, and put the proceeds to work. This is the "
            "path that ranks first on the central assumptions and the one that carries the most "
            "reinvestment risk, because it exchanges a building for a price series.")]

    b.append('<div class="stats">')
    b.append(stat("Value at a 2045 transfer", money10(p3["a_value"]), "central assumptions"))
    b.append(stat("Costs of sale", money10(p3["sale_cost"]), "6% + transfer tax + recording"))
    b.append(stat("Tax on sale", money10(p3["sale_tax"]), "basis equals value: none"))
    b.append(stat("Net proceeds invested", money10(p3["sale_proceeds"]), "at the transfer date"))
    b.append('</div>')

    b.append("<h2>What the sale costs, line by line</h2>")
    b.append(table(
        "Every cost between the sale price and the money in the account. Each line is either "
        "statutory, derived from a published rate, or a labelled assumption.",
        ["Cost", "#Amount", "How it is computed", "Status"],
        [
            ["Commission, escrow and title", ("num", money10(p3["a_value"] * 0.06)),
             "6% of price, inside a 5%-7% band. This is the largest single cost and the least "
             "verified: it is a market rate, not a published one.", tag("asm")],
            ["Documentary transfer tax (county)", ("num", money10(p3["a_value"] * 0.0011)),
             x.ex("$0.55") + " per $500 of value, which is 0.11%. A city may add up to half "
             "that again; "
             "none is verified for this parcel, so none is added. " + src("rtc_11911"),
             tag("ok")],
            ["Recording fees", ("num", money10(60)),
             "The San Francisco schedule is " + x.ex("$14") + " for the first page and "
             + x.ex("$3") + " for each additional page, plus a " + x.ex("$10")
             + " survey monument fee on a deed subject to transfer tax. The "
             "county schedule for Property A was not read, so the city schedule is used as a "
             "stand-in inside a $50-$120 band. " + src("sf_recording_fees"), tag("drv")],
            ["Total costs", ("num", money10(p3["sale_cost"])), "Sum of the three lines above.",
             tag("drv")],
            ["Income tax on the gain", ("num", money10(p3["sale_tax"])),
             "Basis equals value on the date of death, so a same-year sale realises no gain. "
             "This is the step-up, and it is the reason timing matters. " + src("irs_p551"),
             tag("ok")],
            ["Net proceeds", ("num", money10(p3["sale_proceeds"])), "Price less costs less tax.",
             tag("drv")],
        ]))

    b.append(risk(
        "The 6 percent selling cost is an assumption, and it is large: %s on this value. If "
        "commission falls to 5 percent the path gains about %s; at 7 percent it loses about the "
        "same. This is one of the few inputs the household can actually negotiate, and it is "
        "worth more attention than most of the tax questions on this desk."
        % (money10(p3["a_value"] * 0.06), money10(p3["a_value"] * 0.01)),
        "The negotiable number"))

    b.append("<h2>What happens to the money afterwards</h2>")
    b.append("<p>Selling is not a decision about a house; it is a decision to hold a portfolio "
             "instead. The model invests the net proceeds at the assumed equity return and adds "
             "the rental income from B. That is a simplification: a real portfolio would be "
             "diversified, would hold bonds, and would be drawn on for living expenses.</p>")
    b.append(table(
        "The portfolio this path implies, and what it earns under each regime.",
        ["Regime", "#Equity return assumed", "#Net worth incl. shelter, 2045",
         "#Rank of this path"],
        [
            [REGIMES[rk]["label"], ("num", pct(REGIMES[rk]["equity"], 1)),
             ("num", money10(res(2045, rk, "P3")["net_worth_with_shelter"])),
             ("num", "%d of 9" % x.rank_of(2045, rk, "P3"))]
            for rk in ("baseline", "high_inflation", "deflation_1930s",
                       "great_recession", "stagnation")
        ]))

    b.append("<h2>The four ways this path fails</h2>")
    b.append("<ul>"
             "<li><strong>Bad timing at entry.</strong> Selling A puts a large lump sum into the "
             "market on a single date. The 1929 and 2007 records both show what that can mean. "
             "See <a href=\"phased.html\">phased investing</a> for the mitigation and its cost.</li>"
             "<li><strong>Poor real returns.</strong> Below about %s nominal the house wins "
             "outright, and there is no way to know in advance which regime is coming.</li>"
             "<li><strong>Spending the proceeds.</strong> A liquid portfolio is spendable; a "
             "house is not. This path requires a written policy, which is "
             "<a href=\"investment-policy.html\">here</a>.</li>"
             "<li><strong>Tax drag on the portfolio.</strong> The model applies a gross return. "
             "A taxable portfolio of this size loses part of its return to federal and state tax "
             "on dividends and realised gains every year, which the model does not deduct.</li>"
             "</ul>" % pct(CROSS["2045|P1_vs_P3_equity"], 1))

    b.append(note(
        "The fourth point matters. A taxable account returning 6.5 percent gross might return "
        "5.7 percent after tax in a high bracket. Over twenty years that difference is larger "
        "than the gap between the best and second-best paths. It is listed as a gap on "
        "<a href=\"questions.html\">questions and gaps</a> rather than modelled, because the "
        "household's bracket and location at the time are unknown.", "good"))

    write("sell-path.html", shell("sell-path.html", "Sell Property A and reinvest",
                                  "\n".join(b)))

    # ------------------------------------------------------------------ mixed
    b = [h1("Mixed paths: the three pure choices are not the only ones",
            "A household rarely chooses to live in a house forever or sell it on day one. The "
            "realistic options combine decisions and sequence them. Six mixed paths were modelled "
            "against the three pure choices, all at the same dates and the same horizon.")]

    b.append("<h2>All nine paths, ranked</h2>")
    order = x.ranked(2045, "baseline")
    rows = []
    for i, r in enumerate(order, 1):
        rows.append([
            ("num", str(i)),
            "<strong>%s</strong> %s" % (r["path"], r["label"]),
            r["kind_label"],
            ("num", money10(r["net_worth_with_shelter"])),
        ])
    b.append(table(
        "Twenty years from a 2045 transfer, central assumptions.",
        ["", "Path", "Type", "#Net worth incl. shelter"], rows))

    b.append("<h2>What each mixed path adds</h2>")
    b.append(table(
        "The six mixed paths, the decision each one adds, and what the model says it is worth "
        "against the closest pure choice.",
        ["Path", "What it adds", "Against", "#Difference", "Verdict"],
        [
            ["<strong>P4</strong> Live 5 years, then sell",
             "Occupancy to earn both the Proposition 19 exclusion and the section 121 exclusion, "
             "then liquidity.",
             "Selling at once",
             ("num", money10(res(2045, "baseline", "P4")["net_worth_with_shelter"]
                             - res(2045, "baseline", "P3")["net_worth_with_shelter"])),
             "Worse on the central case, better if growth is weak."],
            ["<strong>P4b</strong> Live 10 years, then sell",
             "The same, held longer. The section 121 cap binds, so the extra years add gain "
             "without adding exclusion.",
             "Selling at once",
             ("num", money10(res(2045, "baseline", "P4b")["net_worth_with_shelter"]
                             - res(2045, "baseline", "P3")["net_worth_with_shelter"])),
             "Worse still on the central case; it is a long bet on the house."],
            ["<strong>P5</strong> Let 10 years, then sell",
             "Rental income plus price growth, accepting recapture and no exclusion.",
             "Living 10 years, then selling",
             ("num", money10(res(2045, "baseline", "P5")["net_worth_with_shelter"]
                             - res(2045, "baseline", "P4b")["net_worth_with_shelter"])),
             "Worse than living in it. The rent does not pay for the lost exclusions."],
            ["<strong>P6</strong> Sell, park 24 months, then phase in",
             "Selling at once, with an explicit delay before market entry.",
             "Selling at once",
             ("num", money10(res(2045, "baseline", "P6")["net_worth_with_shelter"]
                             - res(2045, "baseline", "P3")["net_worth_with_shelter"])),
             "Costs a little in the central case; buys protection against a crash."],
            ["<strong>P6b</strong> Sell, park 36 months, then phase in",
             "The same with a longer parking period.",
             "Selling at once",
             ("num", money10(res(2045, "baseline", "P6b")["net_worth_with_shelter"]
                             - res(2045, "baseline", "P3")["net_worth_with_shelter"])),
             "Costs a little more; the protection is longer."],
            ["<strong>P7</strong> Sell both A and B",
             "Liquidity everywhere. The household rents.",
             "Selling A only",
             ("num", money10(res(2045, "baseline", "P7")["net_worth_with_shelter"]
                             - res(2045, "baseline", "P3")["net_worth_with_shelter"])),
             "Clearly worse. Selling B destroys sheltered cash flow and creates a taxable gain."],
        ]))

    b.append(risk(
        "The mixed paths are where the tax detail matters most, and where this desk is least "
        "certain. P4 and P4b depend on the household actually living in the house for the period "
        "the path assumes; the statute does not care about the plan, only the occupancy. P5 "
        "depends on a rent figure that is an unverified assumption. P6 and P6b depend on a "
        "Treasury yield that will not be the one observed on 13 November 2026 when the money "
        "actually arrives.",
        "The paths with the most assumptions"))

    b.append("<h2>The sequencing question</h2>")
    b.append("<p>Order matters independently of which paths are chosen. The model assumes a "
             "rational sequence; a real household faces a deadline. The order that minimises "
             "expensive mistakes:</p>")
    b.append("<ol>"
             "<li><strong>At the death:</strong> obtain the date-of-death appraisal, file the "
             "estate return if required, and do not let the house sit uninsured or unmaintained.</li>"
             "<li><strong>Within one year:</strong> decide occupancy. This is the only decision "
             "with a hard statutory deadline and a large, irreversible tax consequence. "
             "%s</li>" % src("rtc_63_2") +
             "<li><strong>Before the money moves:</strong> write the investment policy. See "
             "<a href=\"investment-policy.html\">policy for the proceeds</a>.</li>"
             "<li><strong>At the sale:</strong> sell, and do not park the proceeds in cash "
             "indefinitely while deciding. That is a decision too, and usually a bad one.</li>"
             "<li><strong>After the sale:</strong> execute the policy, and re-run the model every "
             "year. See <a href=\"annual-rerun.html\">annual re-run</a>.</li>"
             "</ol>")

    write("mixed-paths.html", shell("mixed-paths.html",
                                     "Mixed paths: the three pure choices are not the only ones",
                                     "\n".join(b)))

    # ------------------------------------------------------------------ phased
    b = [h1("Phased investing: parking the proceeds before they reach the market",
            "Selling A puts a large sum into the market on one date. The phased path parks the "
            "proceeds in short Treasuries for 24 or 36 months and then buys equities in 24 equal "
            "monthly slices. It costs something in an ordinary market. The question is whether "
            "it buys enough protection in an extraordinary one.")]

    b.append('<div class="answer"><div class="k">The answer</div>'
             '<div class="v">Parking costs a little and protects against a narrow range of '
             'outcomes. It is not free insurance.</div>'
             '<p>On the central assumptions, parking for 24 months then phasing in ends about '
             '%s behind buying at once, on a %s pot. That is the price. It pays off only if the '
             'market falls more than about %s in the first two years. A fall that deep has '
             'happened — twice in the last century — but it is not the base case.</p></div>'
             % (money10(abs(res(2045, "baseline", "P6")["net_worth_with_shelter"]
                             - res(2045, "baseline", "P3")["net_worth_with_shelter"])),
                money10(res(2045, "baseline", "P3")["sale_proceeds"]),
                pct(x.BREAK["2045|baseline|24|12"] or 0, 1)))

    b.append("<h2>What the parking earns</h2>")
    b.append(table(
        "Treasury par yields observed on 13 November 2026, and what they imply for a parked "
        "balance. These are current observations, not forecasts.",
        ["Maturity", "Par yield", "On a parked balance, first year", "Source"],
        [
            ["3 months", ("num", pct(MI["treasury_3m"], 2)),
             ("num", money10(res(2045, "baseline", "P3")["sale_proceeds"] * MI["treasury_3m"])),
             src("treasury_yields")],
            ["1 year", ("num", pct(0.0465, 2)),
             ("num", money10(res(2045, "baseline", "P3")["sale_proceeds"] * 0.0465)),
             src("treasury_yields")],
            ["2 years", ("num", pct(MI["treasury_2y"], 2)),
             ("num", money10(res(2045, "baseline", "P3")["sale_proceeds"] * MI["treasury_2y"])),
             src("treasury_yields")],
            ["5 years", ("num", pct(0.0498, 2)),
             ("num", money10(res(2045, "baseline", "P3")["sale_proceeds"] * 0.0498)),
             src("treasury_yields")],
        ],
        note="Par yields, not coupons, and no reinvestment assumption. The model uses the "
             "two-year yield with monthly compounding throughout the parking window, because "
             "the shortest ladder that spans a 24-36 month wait is a rolling two-year bill. "
             "Interest is taxable at ordinary rates, which the model does not deduct."))

    b.append("<h2>The break-even crash depth</h2>")
    b.append("<p>The model finds the size of an equity fall at a given month at which parking "
             "starts to beat buying at once, holding both to the same twenty-year horizon. Below "
             "that depth, parking loses. Above it, parking wins.</p>")
    head = ["Parking period", "#Crash at month 0", "#Month 6", "#Month 12", "#Month 24",
            "#Month 36"]
    rows = []
    for pm in (24, 36):
        cells = ["%d months" % pm]
        for cm in (0, 6, 12, 24, 36):
            v = x.BREAK["2045|baseline|%d|%d" % (pm, cm)]
            cells.append(("num", "never" if v is None else pct(v, 1)))
        rows.append(cells)
    b.append(table(
        "Depth of a one-off equity fall at which parking first beats buying at once. 2045 "
        "transfer, central assumptions, twenty-year horizon.",
        head, rows,
        note="'Never' means no fall short of total loss makes parking win — the drag from the "
             "lower expected return is larger than the crash can impose. The depths are "
             "arithmetic break-evens, not predictions. For scale: the Dow fell 89% from 1929 to "
             "1932 and the S&P 500 fell 57% from 2007 to 2009. " + src("fed_1929", "fed_great_recession")))

    b.append(risk(
        "Parking is a bet that the crash comes early in the window. A crash at month 36 or "
        "later costs the parking strategy as much as it costs the buy-at-once strategy, because "
        "by then the parked money is mostly invested anyway. The protection is real but it is "
        "concentrated in the first two years, which is exactly when the household has the least "
        "information and the most anxiety.",
        "The protection has a short window"))

    b.append("<h2>The same analysis in the bad regimes</h2>")
    b.append(table(
        "Whether parking wins, by regime, with a 35% fall at month 12 and a 24-month park.",
        ["Regime", "#Buy at once, from one dollar", "#Park then phase, from one dollar",
         "Parking wins?",
         "Break-even depth"],
        [
            [REGIMES[rk]["label"],
             ("num", "%.3f" % (x.phase_compare(2045, dict(REGIMES[rk], key=rk), 24, 24, 12,
                                               0.35)[0])),
             ("num", "%.3f" % (x.phase_compare(2045, dict(REGIMES[rk], key=rk), 24, 24, 12,
                                               0.35)[1])),
             "yes" if x.BREAK["2045|%s|24|12" % rk] is not None
             and x.BREAK["2045|%s|24|12" % rk] <= 0.35 else "no",
             ("num", "never" if x.BREAK["2045|%s|24|12" % rk] is None
              else pct(x.BREAK["2045|%s|24|12" % rk], 1))]
            for rk in ("baseline", "high_inflation", "deflation_1930s", "great_recession",
                       "stagnation")
        ],
        note="A 35% fall at month 12 is a severe but historically ordinary bear market. In the "
             "two crash regimes parking wins with no crash needed at all, because the expected "
             "equity return is below the Treasury yield."))

    b.append("<h2>What the model does not do</h2>")
    b.append("<ul>"
             "<li>It does not model taxes on the parking interest, which are at ordinary "
             "rates.</li>"
             "<li>It does not model a Treasury ladder in detail, only a rolling two-year "
             "instrument.</li>"
             "<li>It does not model inflation risk in the parked window. A 24-month park in a "
             "high-inflation regime loses real value; that is shown by the high-inflation row "
             "above, where buying at once beats parking even through a crash.</li>"
             "<li>It does not model the behavioural cost, which is usually the largest: a "
             "household that parks for two years and then cannot bring itself to buy is worse "
             "off than one that never parked.</li>"
             "</ul>")

    write("phased.html", shell("phased.html",
                               "Phased investing: parking the proceeds before they reach the market",
                               "\n".join(b)))
