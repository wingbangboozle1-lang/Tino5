# -*- coding: utf-8 -*-
"""Page set 2: the two properties and the side-by-side comparison."""
from __future__ import annotations


def build(x):
    write, h1, table, stat, risk, note = x.write, x.h1, x.table, x.stat, x.risk, x.note
    money10, pct, tag, src, shell = x.money10, x.pct, x.tag, x.src, x.shell
    res, best, ranked, MI, BANDS = x.res, x.best, x.ranked, x.MI, x.BANDS
    CROSS, REGIMES = x.CROSS, x.REGIMES

    # ------------------------------------------------------------------ property A
    p1 = res(2045, "baseline", "P1")
    b = [h1("Property A: the house that arrives later",
            "A single-family house in Santa Clara County, expected through a trust between "
            "2040 and 2050. Nothing on this page identifies it: no street, no parcel number, "
            "no ZIP code, and assessed values are rounded so the page cannot be matched to a "
            "public assessment roll.")]

    b.append('<div class="stats">')
    b.append(stat("Owner's value anchor", money10(MI["a_value"]),
                  "unverified, owner-supplied, Nov 2026"))
    b.append(stat("Assessed value used", money10(MI["a_assessed"]), "rounded to $10,000"))
    b.append(stat("Effective tax rate", pct(MI["a_rate_base"], 2) + " of assessed",
                  "owner-implied midpoint; band below"))
    b.append(stat("Annual property tax now", money10(p1["a_annual_tax_now"]), "2026 dollars"))
    b.append('</div>')

    b.append("<h2>The rate that actually applies is not published anywhere</h2>")
    b.append("<p>California property tax is one percent of assessed value plus whatever the "
             "voters in that tax rate area have approved. The base one percent never changes. "
             "Everything else — county bonds, school bonds, city and district measures — "
             "varies by tax rate area, and a county has hundreds of them. The county's own "
             "booklet states the composition of a typical area and warns that it is typical, "
             "not universal. %s</p>" % src("scc_assessor_booklet"))
    b.append(table(
        "The three rates the model carries for Property A, and where each comes from.",
        ["Rate on assessed value", "Value", "Where it comes from", "Status"],
        [
            ["Typical tax rate area, county booklet",
             ("num", pct(MI["a_rate_floor"], 3)),
             "1.0000 base + 0.0388 county bonds + 0.100 school bonds + 0.010 water bonds "
             "= 1.1488 per $100, from the assessor's 2026 owner booklet. " + src("scc_assessor_booklet"),
             tag("ok")],
            ["Owner-implied midpoint", ("num", pct(MI["a_rate_base"], 2)),
             "The midpoint of the band the household's own tax and assessed-value history "
             "produces, rounded to 1.340%. The history itself is deliberately not stored in "
             "this repository.", tag("drv")],
            ["Owner-implied ceiling", ("num", pct(MI["a_rate_ceil"], 2)),
             "The top of that band.", tag("drv")],
            ["This parcel's actual tax rate area", ("num", '<span class="tag-unv">blank</span>'),
             "Not verified. The county publishes a tax rate book and the parcel's own bill "
             "carries the rate; neither was obtained. " + src("scc_assessor"), tag("unv")],
        ],
        note="The model runs the whole band. At the low end the annual tax is "
             "lower and every keeping path improves; at the high end it worsens. The ranking "
             "of the three pure choices does not change anywhere in the band."))

    b.append("<h2>What a year of owning it costs and produces</h2>")
    b.append(table(
        "Operating budget for Property A in today's dollars. Each line states its status, "
        "because most of them are the household's own estimates rather than measured costs.",
        ["Line", "#Annual", "Status", "Note"],
        [
            ["Property tax at the owner-implied rate", ("num", money10(p1["a_annual_tax_now"])),
             tag("drv"), "Rises by the lesser of 2% and inflation each year under "
             "Proposition 13. " + src("scc_assessor_booklet")],
            ["Homeowners' exemption effect",
             ("num", money10(-MI["a_assessed"] * 0.0001)),
             tag("ok"), "Up to $7,000 of assessed value is exempt, worth about $80 a year. "
             "The claim is due by 15 February. " + src("scc_assessor_booklet")],
            ["Insurance", ("num", money10(1500)), tag("own"),
             "Owner estimate, not a quote. A replaced-cost policy on an older single-family "
             "house in this county is commonly more than this figure."],
            ["Water", ("num", money10(130 * 12)), tag("own"), "Owner band of $100-$150 a month."],
            ["Electricity", ("num", money10(0)), tag("own"),
             "Owner reports solar offsets consumption to roughly zero, sometimes a small credit."],
            ["Maintenance and capital reserve", ("num", money10(MI["a_value"] * MI["a_maint"])),
             tag("asm"), "0.60% of value a year, inside a 0.30%-0.90% band. A house of this "
             "age needs a roof, a sewer lateral and a heating system within twenty years; "
             "see the <a href=\"maintenance.html\">five-year plan</a>."],
            ["Market rent, if let", ("num", money10(MI["a_rent_mo"] * 12)), tag("asm"),
             "A labelled assumption of $6,000-$9,000 a month. No independent comparables "
             "were obtained, so every letting path is a floor."],
            ["Gross yield on the owner's value anchor",
             ("num", pct(MI["a_rent_mo"] * 12 / MI["a_value"], 2)), tag("drv"),
             "Rent divided by value. Below the yield on a two-year Treasury, before a single "
             "expense. " + src("treasury_yields")],
        ]))

    b.append(risk(
        "The rent figure is the weakest number on this page. At the low end of the band the "
        "house yields %s gross; at the high end, %s. Both are below the two-year Treasury "
        "yield of %s observed on 13 November 2026, before taxes, insurance, water and "
        "maintenance. A rental that yields less than a government bond, before expenses, is a "
        "bet on price growth, not an income asset. That is the whole case against letting it out."
        % (pct(6000 * 12 / MI["a_value"], 2), pct(9000 * 12 / MI["a_value"], 2),
           pct(MI["treasury_2y"], 2)),
        "The rent assumption carries the letting case"))

    b.append("<h2>The valuation that will actually matter</h2>")
    b.append("<p>The number this desk uses, %s, is the household's rough anchor for November "
             "2026. The number that will govern the tax outcome is different: the fair market "
             "value on the date of death, which becomes the income-tax basis automatically and "
             "the estate-tax value for the federal return. If the transfer happens in 2045 at "
             "the assumed growth rate, that figure is %s. See "
             "<a href=\"valuation.html\">date-of-death valuation</a> for how to establish it "
             "defensibly.</p>" % (money10(MI["a_value"]),
                                  money10(p1["a_value"])))

    write("property-a.html", shell("property-a.html",
                                   "Property A: the house that arrives later",
                                   "\n".join(b)))

    # ------------------------------------------------------------------ property B
    b2 = res(2045, "baseline", "P1")
    b = [h1("Property B: the building already owned",
            "A three-unit building in San Francisco County. It is not inherited and it is not "
            "part of the decision about A. It is included because it changes the household's "
            "cash flow, its housing and its tax position, and because any plan that ignores it "
            "would be wrong.")]

    b.append('<div class="stats">')
    b.append(stat("Owner's value anchor", money10(MI["b_value"]), "unverified, owner-supplied"))
    b.append(stat("Assessed value used", money10(MI["b_assessed"]), "rounded to $5,000"))
    b.append(stat("Rent from two units", money10(MI["b_rent_mo"]) + "/mo",
                  "owner-supplied, combined"))
    b.append(stat("Rent per let unit", money10(MI["b_rent_mo"] / 2) + "/mo",
                  "derived from the combined figure"))
    b.append('</div>')

    b.append("<h2>Its tax bill is not the published rate applied to its value</h2>")
    b.append("<p>The city publishes a secured property tax rate of %s for fiscal year "
             "2026-27. %s Applying that rate to the assessed value gives %s. The household's "
             "2025 bill was about %s. The difference, roughly %s a year, is parcel taxes, bond "
             "measures and direct assessments that sit outside the ad valorem rate. The model "
             "carries that difference as a separate line so the bill is reproduced, and labels "
             "it for what it is: arithmetic on two owner figures, not a verified breakdown.</p>"
             % (pct(MI["b_rate"], 5), src("sftreasurer_secured"),
                money10(MI["b_assessed"] * MI["b_rate"]), money10(MI["b_tax_reported"]),
                money10(MI["b_addon"])))

    b.append(table(
        "Property B's annual tax, built from the published rate plus the owner-implied add-on.",
        ["Line", "#Annual", "Status", "Source or note"],
        [
            ["Assessed value × published secured rate",
             ("num", money10(MI["b_assessed"] * MI["b_rate"])), tag("ok"),
             "Rate of " + pct(MI["b_rate"], 5) + " for FY2026-27. " + src("sftreasurer_secured")],
            ["Owner-implied add-on", ("num", money10(MI["b_addon"])), tag("drv"),
             "The reported bill less the line above. Reason unverified."],
            ["Measure H parcel tax, multifamily",
             ("num", money10(249)), tag("exact"),
             "First levied fiscal year 2027-28: " + x.ex("$249") + " for a multifamily parcel "
             "with building area of 5,000 square feet or less, plus " + x.ex("$0.195")
             + " a square foot above that, capped at " + x.ex("$50,000")
             + ". Expires 30 June 2042. " + src("sf_propH_text")],
            ["Both above, total", ("num", money10(MI["b_assessed"] * MI["b_rate"]
                                                  + MI["b_addon"] + 249)), tag("drv"),
             "What the model charges in the first year of the projection."],
        ]))

    b.append(risk(
        "Measure H passed on 3 November 2026 with %.2f%% of the vote on preliminary results. "
        "The results page was headed 'preliminary' when read, with a further count scheduled "
        "for 17 November 2026. Until the count is certified, treat the parcel-tax figures as "
        "provisional. The operative rate schedule is quoted from the ordinance text on "
        "<a href=\"propH.html\">the Measure H page</a>."
        % 74.40, "Provisional election result"))

    b.append("<h2>Why the rent matters more than the value</h2>")
    b.append("<p>Two units at about %s a month pay the building's own costs and then some. "
             "The third unit is the household's housing, or its rent-free option. That is an "
             "unusual position: the household can house itself and still collect rent from the "
             "same building. Any plan that sells B trades that for cash, and the cash is then "
             "taxed, invested and spent.</p>" % money10(MI["b_rent_mo"]))
    b.append(table(
        "What B contributes in the first year of the projection, before any decision about A.",
        ["Item", "#Annual", "Status"],
        [
            ["Gross rent, two units", ("num", money10(MI["b_rent_mo"] * 12)), tag("own")],
            ["Gross rent, three units if the household lives in A",
             ("num", money10(MI["b_rent_mo"] / 2 * 3 * 12)), tag("drv")],
            ["Property tax, including Measure H", ("num", money10(
                MI["b_assessed"] * MI["b_rate"] + MI["b_addon"] + 249)), tag("drv")],
            ["Insurance", ("num", money10(1500)), tag("own")],
            ["Water for three units", ("num", money10(365 * 12)), tag("own")],
            ["Electricity, common areas", ("num", money10(50 * 12)), tag("own")],
            ["Maintenance and capital reserve", ("num", money10(MI["b_value"] * MI["b_maint"])),
             tag("asm")],
            ["Net operating income, two units let", ("num", money10(
                MI["b_rent_mo"] * 12 - MI["b_assessed"] * MI["b_rate"] - MI["b_addon"] - 249
                - 1500 - 365 * 12 - 50 * 12 - MI["b_value"] * MI["b_maint"])), tag("drv")],
        ],
        note="Maintenance at 0.90%% of value is the middle of a 0.60%%-1.40%% band for a "
             "three-unit building of this age. At the top of the band, net operating income "
             "falls by about %s. The five-year capital plan is on "
             "<a href=\"maintenance.html\">building plan</a>."
             % money10(MI["b_value"] * (1.4 - 0.9) / 100)))

    write("property-b.html", shell("property-b.html",
                                   "Property B: the building already owned",
                                   "\n".join(b)))

    # ------------------------------------------------------------------ own vs inherit
    b = [h1("Why the two properties are not comparable",
            "The most common mistake in a case like this is to compare the two buildings as if "
            "they were the same kind of asset. They are not. One is a purchase the household "
            "already made and already pays tax on. The other is a transfer at death, which "
            "resets both the income-tax basis and, if nobody lives in it, the assessed value.")]

    b.append("<h2>Four differences that change the arithmetic</h2>")
    b.append(table(
        "The same two buildings, treated differently by four separate rules.",
        ["Question", "Property A (inherited)", "Property B (already owned)", "Consequence"],
        [
            ["What is the income-tax basis?",
             "Fair market value on the date of death, automatically, with no election. "
             + src("irs_p551"),
             "Historic cost plus improvements less depreciation already taken. Not verified "
             "for this building.",
             "A can be sold soon after death with little or no gain. B cannot."],
            ["What is the assessed value?",
             "Reset to market on transfer unless the transferee moves in and claims the "
             "parent-child exclusion. " + src("rtc_63_2"),
             "Carries its existing factored base year value; a change of residence inside "
             "the building is not a change of ownership.",
             "A costs far more to hold as a rental than B does, in tax terms, relative to its value."],
            ["Does living in it change the tax?",
             "Yes, decisively: occupancy is a condition of the Proposition 19 exclusion, "
             "worth up to about " + x.ex("$1,044,586") + " of assessed value. "
             + src("boe_lta25009"),
             "No. The household already owns it; occupancy changes no assessed value.",
             "Occupancy has a price on A and almost none on B."],
            ["What does selling it cost?",
             "Transfer tax at the county rate, recording fees, commission, and any capital "
             "gain not sheltered by the step-up.",
             "Transfer tax at the city rate too, plus a much larger taxable gain because the "
             "historic basis is low.",
             "Selling A is cheap in tax terms. Selling B is expensive."],
        ]))

    b.append(risk(
        "Selling B is modelled on this desk only as a comparison path, and it ranks last or "
        "next to last in every regime. The basis used for B's sale is its assessed value "
        "because the household's actual cost basis was not supplied. That makes B's sale look "
        "cheaper than it is: a building held for decades has a basis far below its assessed "
        "value, so the real taxable gain — and the real tax — are larger than modelled here.",
        "The B sale path is under-taxed in this model"))

    b.append("<h2>Why the household's own housing must be counted</h2>")
    b.append("<p>If living in A were scored as free housing and renting were scored as paying "
             "rent elsewhere, living would win by construction. The model avoids that. Every "
             "path carries the same housing consumption, valued at market rent: a household "
             "living in A is charged the rent it does not receive, and a household that sells "
             "everything is charged the rent it must pay. Shelter is reported as its own column "
             "so the reader can see how much of each outcome is housing rather than money.</p>")
    b.append(note(
        "Shelter is counted at market rent, not at imputed-rent tax rules. That is a "
        "deliberate simplification: the internal revenue code does not tax the rental value of "
        "a home the owner occupies, and it does not allow a deduction for rent paid on a "
        "personal residence. Counting both sides at market rent therefore cancels out and "
        "leaves a clean comparison. The tax consequences of each are modelled separately.",
        "good"))

    write("own-vs-inherit.html", shell("own-vs-inherit.html",
                                       "Why the two properties are not comparable",
                                       "\n".join(b)))

    # ------------------------------------------------------------------ choices
    b = [h1("All choices, compared at the same dates and horizons",
            "Nine paths, three transfer dates, twenty years, identical tax treatment for "
            "identical facts. Only the decisions differ. Every figure below is the same model "
            "with one or more switches changed, so a difference between two rows is a "
            "difference between two decisions and nothing else.")]

    b.append(risk(
        "These are twenty-year projections. A ranking produced by a twenty-year projection is "
        "not a prediction of the future; it is a statement that, if these particular "
        "assumptions held, this path would leave more. The distribution of outcomes under each "
        "path is on <a href=\"charts.html\">projection charts</a>, and it overlaps heavily.",
        "How to read a twenty-year rank"))

    b.append("<h2>At a 2045 transfer</h2>")
    order = ranked(2045, "baseline")
    rows = []
    for i, r in enumerate(order, 1):
        cls = "best" if i == 1 else ("worst" if i == len(order) else "")
        rows.append((cls, [
            "<strong>%d</strong>" % i,
            "<strong>%s</strong> %s<br><span class=\"small\">%s</span>"
            % (r["path"], r["label"], r["kind_label"]),
            ("num", money10(r["net_worth_with_shelter"])),
            ("num", money10(r["financial"])),
            ("num", money10(r["a_final"] + r["b_final"])),
            ("num", money10(r["shelter"])),
        ]))
    b.append(table(
        "Twenty years from a 2045 transfer, central assumptions. Net worth including shelter "
        "is the ranking column: property held plus financial assets plus the market rent of "
        "the housing the household occupied.",
        ["", "Path", "#Net worth incl. shelter", "#Financial assets", "#Property held",
         "#Shelter consumed"],
        rows))

    b.append("<h2>Does the date of the transfer change the ranking?</h2>")
    rows = []
    for pid in [r["path"] for r in order]:
        cells = ["<strong>%s</strong> %s" % (pid, x.PATHS[pid]["label"])]
        for t in x.TRANSFER_YEARS:
            r = res(t, "baseline", pid)
            cells.append(("num", money10(r["net_worth_with_shelter"])))
        rk = [x.rank_of(t, "baseline", pid) for t in x.TRANSFER_YEARS]
        cells.append(" / ".join(str(k) for k in rk))
        rows.append(cells)
    b.append(table(
        "Net worth including shelter at each of the three transfer dates, with the rank at "
        "each date after the last column.",
        ["Path", "#2040", "#2045", "#2050", "Rank at each date"],
        rows,
        note="The date shifts every level but does not reorder the paths. Twenty years of "
             "growth moves all nine outcomes by the same order of magnitude."))

    b.append("<h2>The same nine paths under five market regimes</h2>")
    head = ["Path"] + ["#" + REGIMES[k]["label"] for k in
                       ("baseline", "high_inflation", "deflation_1930s",
                        "great_recession", "stagnation")]
    rows = []
    for pid in [p for p in x.PATHS]:
        cells = ["<strong>%s</strong> %s" % (pid, x.PATHS[pid]["label"])]
        for rk in ("baseline", "high_inflation", "deflation_1930s", "great_recession",
                   "stagnation"):
            cells.append(("num", money10(res(2045, rk, pid)["net_worth_with_shelter"])))
        rows.append(cells)
    b.append(table(
        "Twenty years from a 2045 transfer, each path under each regime. The regimes are "
        "described, with their official anchors, on <a href=\"swan.html\">black swans</a>.",
        head, rows,
        note="Read the rows, not the levels. Living in A wins in three of five regimes; "
             "selling at once wins only in the baseline; the phased paths win in the dull "
             "market. No single path is robust."))

    b.append("<h2>What every path pays along the way</h2>")
    rows = []
    for pid in [p for p in x.PATHS]:
        r = res(2045, "baseline", pid)
        rows.append([
            "<strong>%s</strong> %s" % (pid, r["label"]),
            ("num", money10(r["taxes_paid"])),
            ("num", money10(r["operating_costs"])),
            ("num", money10(r["rental_income"])),
            ("num", money10(r["sale_cost"])),
            ("num", money10(r["sale_tax"])),
        ])
    b.append(table(
        "Cumulative over twenty years from a 2045 transfer, undiscounted, in nominal dollars.",
        ["Path", "#Property tax paid", "#All operating costs", "#Rental income received",
         "#Sale costs", "#Tax on sale"],
        rows,
        note="Sale costs are commission, transfer tax and recording fees. Tax on sale is "
             "federal capital gain and net investment income tax plus California income tax, "
             "including depreciation recapture where the house was let."))

    b.append(note(
        "Two paths are missing from this table on purpose. A like-kind exchange of A for other "
        "rental property is not modelled as a path because it is a decision that needs counsel "
        "on facts not in the file; the considerations are set out on "
        "<a href=\"like-kind.html\">like-kind exchange decision</a>. A partial sale or a "
        "fractional-interest gift is likewise not modelled. Nothing is implemented without "
        "approval; see <a href=\"suggestions.html\">suggestions for review</a>.", "good"))

    write("choices.html", shell("choices.html",
                                "All choices, compared at the same dates and horizons",
                                "\n".join(b)))
