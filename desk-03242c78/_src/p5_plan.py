# -*- coding: utf-8 -*-
"""Page set 5: local rules, market record, black swans, timeline, plans, valuation."""
from __future__ import annotations


def build(x):
    write, h1, table, stat, risk, note = x.write, x.h1, x.table, x.stat, x.risk, x.note
    money10, pct, tag, src, shell = x.money10, x.pct, x.tag, x.src, x.shell
    res, MI, BANDS, REGIMES, CROSS = x.res, x.MI, x.BANDS, x.REGIMES, x.CROSS

    def timeline(items):
        out = ['<ul class="tl">']
        for when, what, who in items:
            out.append('<li><span class="when">%s</span><div class="what">%s</div>'
                       '<div class="who">%s</div></li>' % (when, what, who))
        out.append("</ul>")
        return "\n".join(out)

    # ------------------------------------------------------------------ rents
    b = [h1("Rents, and why every letting figure here is a floor",
            "The desk has no independent rent estimate for Property A. Not a comparable "
            "listing, not an appraiser's opinion, not the federal government's fair market rent "
            "for the area — nothing that would meet the standard the rest of this desk is held "
            "to. So the rent figure is labelled an assumption, and every letting path is "
            "described as a floor rather than an estimate.")]

    b.append('<div class="answer"><div class="k">What is used, and what it is not</div>'
             '<div class="v">A labelled assumption of %s a month, inside a %s to %s band.</div>'
             '<p>It is not a market rent. It has not been checked against a single comparable. '
             'It is a planning figure chosen so that the letting case is tested fairly: at the '
             'top of the band, letting A out still does not beat selling at the central house '
             'growth assumption. If the true rent is at the bottom of the band, the case against '
             'letting is stronger than shown.</p></div>'
             % (money10(MI["a_rent_mo"]), money10(BANDS["a_rent"][0]),
                money10(BANDS["a_rent"][1])))

    b.append("<h2>The rent floor, and what a real one would take</h2>")
    b.append(table(
        "Three ways to establish a defensible rent for Property A, in order of how much they "
        "would be worth. None has been done.",
        ["Method", "What it produces", "What it costs", "Status"],
        [
            ["Three written rental comparables",
             "A defensible market rent for a house of this size and condition in this "
             "submarket, from recently let units.",
             "A local property manager will usually provide them free in exchange for a "
             "management conversation.", tag("unv", "not obtained")],
            ["HUD Fair Market Rent for the area",
             "The 40th-percentile gross rent for standard-quality units in the metropolitan "
             "area, published annually. A published government figure, but for the whole area "
             "and not for this house. " + src("hud_fmr"),
             "Free.", tag("ok", "available, not used")],
            ["Professional rental appraisal",
             "An opinion of rent from a licensed appraiser, usable in a dispute.",
             "A few hundred dollars.", tag("unv", "not obtained")],
        ],
        note="The HUD figure is published and free and would at least bound the assumption. It "
             "is deliberately not used as the rent here, because an area-wide 40th-percentile "
             "rent for standard-quality units is not a market rent for a specific house, and "
             "using it would give the letting case a false authority."))

    b.append("<h2>Property B's rent is a different matter</h2>")
    b.append("<p>Property B has tenants and leases. Its rent is not an assumption; it is a "
             "contract. The desk uses the owner's figure of %s a month for two units, which is "
             "roughly %s per unit. That figure should be checked against the leases themselves, "
             "together with the tenancy start dates, the deposit amounts and any rent-control "
             "registration. It has not been.</p>"
             % (money10(MI["b_rent_mo"]), money10(MI["b_rent_mo"] / 2)))

    b.append(table(
        "What the model assumes about Property B's rent, and what would verify or change it.",
        ["Assumption", "Why it matters", "How to verify"],
        [
            ["Both let units stay let for twenty years",
             "A vacancy of even six months on one unit is a five-figure loss at this rent.",
             "Tenancy history, plus the local rental market's vacancy rate."],
            ["Rent can be raised with inflation",
             "Under the local rent ordinance, annual increases are capped and require notice. "
             "The model grows rent at the general inflation rate, which may exceed the cap.",
             "The rent ordinance's current allowable increase, and each unit's registration "
             "and lawful rent."],
            ["The third unit can be occupied without losing the other two rents",
             "This is the household's stated position and it is the basis of every path that "
             "houses the household in B.",
             "The leases and the rent ordinance's owner-occupancy provisions."],
            ["No owner move-in eviction is needed",
             "If the third unit is currently let, moving in may require an eviction, which is "
             "expensive, slow and regulated.",
             "Whether the third unit is vacant. The owner's description implies it is."],
        ]))

    b.append(risk(
        "Rent control is the largest unmodelled risk in Property B. A three-unit building in "
        "San Francisco falls under the rent ordinance; annual increases are limited, and "
        "eviction for owner move-in is regulated and can require relocation payments. The model "
        "grows B's rent with general inflation, which is optimistic if the cap binds. On B, "
        "this makes the household's cash flow look better than it may be — the opposite "
        "direction from the omissions listed in the workbook.",
        "The cap that is not modelled"))

    b.append(note(
        "Both directions of bias are now stated: the omissions listed on the workbook make "
        "sell-and-invest look better, and this one makes keeping B look better. They are not "
        "equal in size, and the desk does not claim they cancel. What it claims is that both "
        "are disclosed, which is what a reader needs in order to decide how much to trust the "
        "ranking.", "good"))

    write("rents.html", shell("rents.html",
                              "Rents, and why every letting figure here is a floor",
                              "\n".join(b)))

    # ------------------------------------------------------------------ local rules
    b = [h1("Local rules that bind",
            "Four sets of local rules apply to these two buildings, and three of them are "
            "capable of changing an outcome by more than the difference between two paths. Each "
            "is stated with what is known, what is not, and the document that would settle it.")]

    b.append("<h2>1. San Francisco rent ordinance (Property B)</h2>")
    b.append(table(
        "What the rent ordinance does to this building, and what is unverified.",
        ["Question", "What is known", "What is not"],
        [
            ["Is the building covered?",
             "A three-unit building is within the ordinance's coverage threshold in general "
             "terms.", "Whether any unit is exempt, for example a substantially rehabilitated "
             "building or a unit with a recent certificate of occupancy."],
            ["How much can rent rise each year?",
             "Annual increases are capped by a formula based on a local price index, and notice "
             "must be given in writing.", "The current allowable percentage, and whether any "
             "banked increases exist for either unit."],
            ["Can the owner move into a let unit?",
             "Owner move-in eviction is permitted under defined conditions, with notice and "
             "possible relocation payments.", "Whether the third unit is vacant, which would "
             "make the question moot."],
            ["Does moving in change the assessed value?",
             "No. Occupancy by the owner is not a change of ownership.", "Nothing."],
        ],
        note="No value on this desk depends on a rent-control figure, because the model grows "
             "rent at general inflation. That is a simplification and it is optimistic: if the "
             "cap binds, B's cash flow is lower than modelled. "
             "The ordinance text was not fetched for this session; it is the first item on the "
             "<a href=\"questions.html\">gap register</a> for local rules."))

    b.append("<h2>2. Santa Clara County assessment calendar (Property A)</h2>")
    b.append(table(
        "The assessment dates that apply to Property A, from the assessor's own booklet.",
        ["Date", "What happens", "Consequence if missed", "Source"],
        [
            ["1 January", "Lien date. Ownership and value are determined as of this moment.",
             "A transfer on 31 December and a transfer on 2 January fall in different "
             "assessment years.", src("scc_assessor_booklet")],
            ["15 February", "Last day to file the homeowners' exemption claim for the year.",
             "The exemption is lost for that year; a late claim may be accepted to 10 December "
             "with a penalty.", src("scc_assessor_booklet")],
            ["2 July", "Assessment roll is published; the appeal window opens.",
             "—", src("scc_assessor_booklet")],
            ["15 September", "The appeal window closes.",
             "The year's assessed value becomes final and cannot be challenged.",
             src("scc_assessor_booklet")],
            ["60 days from notice", "Deadline to appeal a supplemental or escape assessment.",
             "A supplemental bill from the transfer becomes final.", src("scc_assessor_booklet")],
        ]))

    b.append("<h2>3. Documentary transfer tax and recording (both buildings)</h2>")
    b.append(table(
        "The costs of recording a sale, and where the two counties differ.",
        ["Item", "Santa Clara County (Property A)", "San Francisco (Property B)", "Source"],
        [
            ["County documentary transfer tax",
             x.ex("$0.55") + " per $500 of value, which is 0.11%",
             "The city imposes its own tiered rate, and the county rate is separate",
             src("rtc_11911")],
            ["City transfer tax, tiered",
             "None verified for Property A's city", "0.75% of the full price between $1,000,000 "
             "and $5,000,000; 2.25% from $5,000,000; higher above that", src("sf_transfer_tax")],
            ["Recording, first page", "County schedule not read", x.ex("$14"),
             src("sf_recording_fees")],
            ["Recording, each extra page", "County schedule not read", x.ex("$3"),
             src("sf_recording_fees")],
            ["Survey monument fee", "County schedule not read",
             "$10 on a deed subject to transfer tax", src("sf_recording_fees")],
            ["Preliminary change of ownership report", "Required in both counties",
             "$20 fee in San Francisco if not presented", src("sf_recording_fees")],
        ],
        note="The San Francisco schedule is used as the recording-fee stand-in for Property A "
             "because the county's own schedule was not read. The difference at these values is "
             "tens of dollars, not thousands."))

    b.append("<h2>4. Ballot measures that touch either building</h2>")
    b.append(table(
        "The November 2026 measures that bear on this decision, with their outcome.",
        ["Measure", "What it would do", "Outcome", "Effect here"],
        [
            ["H — Parcel Tax to Fund Muni Operations",
             "A per-parcel tax on property in San Francisco, scaled by type and size, from "
             "fiscal 2027-28 to 2041-42, indexed annually. " + src("sf_propH_text"),
             "Passed, 74.40% on preliminary results. " + src("sfelections_results"),
             "About " + money10(249) + " a year on Property B. Immaterial, but modelled."],
            ["I — Changes to the Real Property Transfer Tax",
             "Would have changed the transfer tax structure.", "Failed, 51.66% against. "
             + src("sfelections_results"),
             "Nothing. The existing tiered rates stay in force."],
            ["J — Removal of the foreclosure exemption",
             "Would have removed an exemption from the transfer tax for foreclosures.",
             "Passed, 80.88%. " + src("sfelections_results"),
             "Nothing on a voluntary sale."],
        ]))

    b.append(risk(
        "San Francisco's transfer tax is charged on the full price at a single tier, not "
        "progressively. A sale of Property B at more than $5,000,000 would pay 2.25% on the "
        "entire price, not 0.75% on the first $5,000,000. That threshold effect makes selling B "
        "far more expensive than a marginal-rate reading would suggest, and it is one more "
        "reason the sell-B path ranks last.",
        "A cliff, not a slope"))

    write("local-rules.html", shell("local-rules.html", "Local rules that bind", "\n".join(b)))

    # ------------------------------------------------------------------ market outlook
    b = [h1("What the long record shows",
            "Rather than assume a growth rate and defend it, the desk measures the record. "
            "Everything on this page is computed from published series: the BLS consumer price "
            "index from 1913, and the Federal Reserve's own histories of the two worst market "
            "episodes of the last century.")]

    b.append("<h2>Inflation, measured rather than assumed</h2>")
    b.append(table(
        "Compound annual inflation over the periods that matter, computed on this desk from the "
        "BLS consumer price index for all urban consumers.",
        ["Period", "#Compound annual rate", "What it was", "Source"],
        [
            ["1913 to 2026, full series", ("num", pct(0.0270, 2)),
             "Index 9.8 to 337.511", src("bls_cpi")],
            ["1972 to 1982", ("num", pct(0.0872, 2)), "Index 41.8 to 96.5; the high-inflation "
             "decade used as a regime", src("bls_cpi")],
            ["1929 to 1933", ("num", pct(-0.0685, 2)), "Index 17.16 to 12.93; deflation through "
             "the Depression", src("bls_cpi")],
            ["2007 to 2009", ("num", "low"), "Subdued inflation through the credit crisis",
             src("bls_cpi")],
            ["2021 to 2023", ("num", "high"), "The recent inflation episode, visible in the "
             "monthly series", src("bls_cpi")],
        ],
        note="The full monthly series is in the repo's existing CPI module and is not reproduced "
             "here. October 2025 is marked X in the BLS series because of the lapse in "
             "appropriations; the desk uses the annual averages and the latest complete months."))

    b.append("<h2>Two drawdowns, measured</h2>")
    b.append(table(
        "The two episodes used as stress regimes, with the official figures.",
        ["Episode", "Peak to trough", "Recovery", "Source"],
        [
            ["1929 to 1932, equities",
             "The Dow fell from 381.17 on 3 September 1929 to 41.22 on 8 July 1932, "
             "<strong>-89%</strong>.",
             "The index did not regain its 1929 high until 23 November 1954 — twenty-five "
             "years.", src("fed_1929")],
            ["2007 to 2009, equities",
             "The S&amp;P 500 fell <strong>-57%</strong> from its October 2007 peak to its March "
             "2009 trough.",
             "Recovered within the following decade.", src("fed_great_recession")],
            ["2006 to 2009, house prices",
             "Home prices fell about <strong>-30%</strong> from mid-2006 to mid-2009.",
             "Varies by market; California recovered strongly and then some.",
             src("fed_great_recession")],
            ["2007 to 2009, the economy",
             "Real GDP fell 4.3% peak to trough; unemployment peaked at 10% in October 2009.",
             "The recession ended in June 2009.", src("fed_great_recession")],
        ]))

    b.append(risk(
        "The 1929 record is the reason a twenty-year horizon is not a guarantee. An investor who "
        "put money in at the 1929 peak and held did not break even in nominal terms until 1954. "
        "The household's twenty-year window from 2045 is the same length. Anyone who says "
        "'twenty years is long enough' has not read this table.",
        "Twenty years was not long enough once"))

    b.append("<h2>What the regimes do to the comparison</h2>")
    b.append(table(
        "The five regimes, their anchors, and the leading path in each at a 2045 transfer.",
        ["Regime", "Inflation anchor", "Leading path", "#Net worth incl. shelter"],
        [
            [REGIMES[rk]["label"],
             REGIMES[rk]["anchor"] and "computed from published series" or "assumption only",
             x.best(2045, rk)["label"],
             ("num", money10(x.best(2045, rk)["net_worth_with_shelter"]))]
            for rk in ("baseline", "high_inflation", "deflation_1930s", "great_recession",
                       "stagnation")
        ],
        note="The anchors are what gives the regimes their authority: the inflation rates are "
             "measured, the drawdowns are measured, and only the annual house and equity rates "
             "within each regime are assumptions."))

    b.append(note(
        "The honest conclusion from this record is that the future will not look like the "
        "average. It will look like one of the episodes, and which one cannot be known. That is "
        "why the desk publishes a distribution and not a point estimate, and why the "
        "recommendation is stated as a starting point rather than an answer.", "good"))

    write("market-outlook.html", shell("market-outlook.html", "What the long record shows",
                                       "\n".join(b)))

    # ------------------------------------------------------------------ swan
    b = [h1("Black swans and extreme paths",
            "A twenty-year projection built on average growth is a comfortable lie. The record "
            "is not a smooth trend; it is long stretches of ordinary returns punctuated by "
            "crashes, inflation spikes and decades of nothing. This page runs the comparison "
            "through five such paths and reports what survives.")]

    b.append('<div class="answer"><div class="k">What survives every regime</div>'
             '<div class="v">Two findings hold in all five regimes tested.</div>'
             '<p>First, <strong>letting Property A out never beats living in it</strong>, at any '
             'transfer date, in any regime. Second, <strong>selling Property B is always among '
             'the worst two choices</strong>. Everything else — whether to keep A, whether to '
             'park the proceeds — depends on which world arrives.</p></div>')

    b.append("<h2>The five regimes</h2>")
    b.append(table(
        "Each regime, what anchors it, and the assumptions it uses. Every regime is chosen to be "
        "defensible from a published record, not to prove a point.",
        ["Regime", "Inflation", "House growth", "Equity return", "What anchors it"],
        [
            [REGIMES[rk]["label"], ("num", pct(REGIMES[rk]["inflation"], 2)),
             ("num", pct(REGIMES[rk]["house"], 1)), ("num", pct(REGIMES[rk]["equity"], 1)),
             REGIMES[rk]["note"]]
            for rk in ("baseline", "high_inflation", "deflation_1930s", "great_recession",
                       "stagnation")
        ]))

    b.append("<h2>Every path in every regime</h2>")
    rows = []
    for pid in x.PATHS:
        cells = ["<strong>%s</strong> %s" % (pid, x.PATHS[pid]["label"])]
        for rk in ("baseline", "high_inflation", "deflation_1930s", "great_recession",
                   "stagnation"):
            cells.append(("num", money10(res(2045, rk, pid)["net_worth_with_shelter"])))
        rows.append(cells)
    b.append(table(
        "Net worth including shelter, twenty years from a 2045 transfer, central assumptions "
        "within each regime.",
        ["Path", "#Baseline", "#High inflation", "#Deflation", "#Credit shock", "#Low growth"],
        rows))

    b.append("<h2>How bad can it get</h2>")
    b.append(table(
        "The worst outcome for each regime, and which path produces it.",
        ["Regime", "#Worst outcome", "Which path", "#Best outcome", "Which path",
         "#Spread"],
        [
            [REGIMES[rk]["label"],
             ("num", money10(x.ranked(2045, rk)[-1]["net_worth_with_shelter"])),
             x.ranked(2045, rk)[-1]["label"],
             ("num", money10(x.ranked(2045, rk)[0]["net_worth_with_shelter"])),
             x.ranked(2045, rk)[0]["label"],
             ("num", money10(x.ranked(2045, rk)[0]["net_worth_with_shelter"]
                             - x.ranked(2045, rk)[-1]["net_worth_with_shelter"]))]
            for rk in ("baseline", "high_inflation", "deflation_1930s", "great_recession",
                       "stagnation")
        ],
        note="The deflation regime produces outcomes an order of magnitude smaller than the "
             "baseline. That is what a repeat of 1929 to 1933 does to every asset at once, and "
             "it is a reminder that the choice between paths is a small question next to the "
             "choice of how much to hold in any asset at all."))

    b.append("<h2>What is extreme but not modelled</h2>")
    b.append("<ul>"
             "<li><strong>A California earthquake that damages one or both buildings.</strong> "
             "Insurance covers some of it; the deductible, the loss of rent and the rebuilding "
             "period do not appear in any projection here.</li>"
             "<li><strong>A change to Proposition 13 or Proposition 19.</strong> Both are "
             "constitutional and both have been amended before. A repeal of the parent-child "
             "exclusion would remove the entire occupancy benefit and make selling more "
             "attractive still.</li>"
             "<li><strong>A federal wealth tax or a change to the step-up in basis.</strong> The "
             "step-up is statutory, not constitutional, and has been proposed for repeal "
             "repeatedly. Its removal would change the arithmetic of every path on this desk.</li>"
             "<li><strong>A long period of rent control tightening.</strong> Would hurt the "
             "letting paths, which already lose.</li>"
             "<li><strong>Extended long-term care for either spouse.</strong> The largest "
             "unmodelled risk in most households of this age, and the one most likely to force "
             "a sale at the worst time.</li>"
             "</ul>")
    b.append(note("Every one of these is reviewed annually as part of the "
                  "<a href=\"annual-rerun.html\">annual re-run</a>. None of them is priced, "
                  "because pricing a scenario that has no probability is worse than naming it.",
                  "good"))

    write("swan.html", shell("swan.html", "Black swans and extreme paths", "\n".join(b)))

    # ------------------------------------------------------------------ timeline
    p1 = res(2045, "baseline", "P1")
    b = [h1("Deadline timeline",
            "The dates below are the ones that carry a penalty, a lost benefit or an "
            "irreversible consequence. They are in the order they occur, counted from the date "
            "of death, because that is the event the household will actually be reacting to.")]

    b.append(timeline([
        ("Day 0", "Date of death. <b>Basis of every asset is fixed at this moment.</b> Order the "
                  "appraisal of Property A immediately; a value established months later is a "
                  "reconstruction, not a valuation. <span class=\"tag-ok\">official</span> "
                  + src("irs_p551"), "Executor or trustee"),
        ("Within 40 days", "The small-estate affidavit becomes available, but only if the entire "
                           "California estate is worth " + money10(166250, exact="166,250")
         + " or less. Property A alone exceeds that, so formal administration will be needed. "
         + "<span class=\"tag-ok\">official</span> " + src("prob_13100"), "Executor"),
        ("Months 1-3", "Obtain an employer identification number for the estate; marshal the "
                       "assets; notify insurers; secure both buildings; change the locks if the "
                       "house is vacant. " + src("irs_p559"), "Executor"),
        ("Within 9 months", "Federal estate tax return due, if one is required — <b>and the "
                            "portability election can only be made on that return</b>. Filing "
                            "late can forfeit an exclusion worth more than either building. "
                            "<span class=\"tag-ok\">official</span> " + src("irs_estate", "irs_i706"),
         "Executor and CPA"),
        ("Within 1 year of transfer", "<b>The Proposition 19 clock.</b> The heir must occupy "
                                      "Property A as a principal residence and file for the "
                                      "homeowners' or disabled veterans' exemption within one "
                                      "year. Miss it and the house is reassessed at market "
                                      "value, costing about "
         + money10(p1["a_taxable"] * MI["a_rate_base"] - p1["a_annual_tax_now"])
         + " a year. <span class=\"tag-ok\">official</span> " + src("rtc_63_2"), "Heir and attorney"),
        ("By 15 February, each year", "Homeowners' exemption claim for that assessment year. "
                                      "Late claims may be accepted to 10 December with a "
                                      "penalty. <span class=\"tag-ok\">official</span> "
         + src("scc_assessor_booklet"), "Heir"),
        ("Within 30 days of the estate return", "Consistent-basis reports to the IRS and to each "
                                                "beneficiary, on Form 8971. The heir needs these "
                                                "figures to compute gain later. "
         + "<span class=\"tag-ok\">official</span> " + src("irs_i706"), "Executor"),
        ("By 15 April, year after death", "The estate's and the heir's income tax returns. A "
                                          "sale of Property A in the year of death is reported "
                                          "here. " + src("irs_p559"), "CPA"),
        ("2 July to 15 September, each year", "The window to appeal an assessed value in Santa "
                                              "Clara County. Free, no attorney needed, and "
                                              "worth doing if the value looks high. "
         + "<span class=\"tag-ok\">official</span> " + src("scc_assessor_booklet"), "Heir"),
        ("Within 3 years of transfer", "The outer limit for a Proposition 19 claim, or before "
                                       "the property is transferred to a third party, whichever "
                                       "is earlier. This is a backstop, not a plan. "
         + "<span class=\"tag-ok\">official</span> " + src("rtc_63_2"), "Heir and attorney"),
        ("Any time after the transfer", "If the decision is to sell: sell. Section 121 requires "
                                        "two of the last five years of ownership and use, and "
                                        "the exclusion is capped at "
         + money10(250000, exact="250,000") + " for a single filer. "
         + "<span class=\"tag-ok\">official</span> " + src("irs_p523"), "Heir"),
        ("Annually, from then on", "Re-run the model, check the recommendation against the "
                                   "inputs, and record the date of the decision. "
                                   "<a href=\"annual-rerun.html\">Annual re-run</a>.",
         "Household"),
    ]))

    b.append("<h2>The three dates that actually cost money</h2>")
    b.append(table(
        "Of the twelve dates above, three carry a consequence large enough to change the "
        "recommendation if missed.",
        ["Date", "Cost of missing it", "#Amount", "Reversible?"],
        [
            ["Within 1 year: exemption claim", "Property A reassessed at market value; the "
             "Proposition 19 exclusion is lost, and with it the annual saving.",
             ("num", money10((p1["a_taxable"] * MI["a_rate_base"]
                              - p1["a_annual_tax_now"]) * 20)),
             "No. The claim window can be extended, but the exclusion depends on facts, not on "
             "a filing."],
            ["Within 9 months: estate return", "Portability lost. The surviving spouse's "
             "exclusion is not increased by the deceased spouse's unused amount.",
             ("num", money10(15000000, exact="15,000,000") + " of exclusion at stake"),
             "Only with a late election, which the IRS may or may not grant."],
            ["Within 30 days: basis reports", "The heir cannot substantiate basis; the gain on a "
             "later sale becomes an argument with the IRS.",
             ("num", "unquantified"), "Partially, with appraisals and records."],
        ]))

    b.append(note("Print this page. The <a href=\"briefing-attorney.html\">attorney briefing "
                  "sheet</a> repeats the three critical dates on one page, next to the legal "
                  "conditions they depend on.", "good"))

    write("timeline.html", shell("timeline.html", "Deadline timeline", "\n".join(b)))

    # ------------------------------------------------------------------ maintenance
    b = [h1("Five-year building plan for both properties",
            "A house and a three-unit building both need money spent on them, and the money "
            "arrives in lumps. The projection uses a smooth reserve — a percentage of value "
            "every year — because a smooth line is easier to compare. The real spending is not "
            "smooth, and this page says what it probably looks like.")]

    b.append(risk(
        "Every figure on this page is an assumption. No contractor has been asked, no "
        "inspection has been done, and no records of past work were supplied. The percentages "
        "are the reserve convention, not a condition assessment. A building inspection and three "
        "quotes for the largest items would replace this page entirely.",
        "This page is entirely assumption"))

    b.append("<h2>What the reserve assumption implies</h2>")
    b.append(table(
        "The annual reserve the model charges, and what it accumulates over five and twenty "
        "years if nothing is spent.",
        ["Building", "#Annual reserve", "#Accumulated in 5 years", "#Accumulated in 20 years",
         "Status"],
        [
            ["Property A", ("num", money10(MI["a_value"] * MI["a_maint"])),
             ("num", money10(MI["a_value"] * MI["a_maint"] * 5)),
             ("num", money10(MI["a_value"] * MI["a_maint"] * 20)), tag("asm")],
            ["Property B", ("num", money10(MI["b_value"] * MI["b_maint"])),
             ("num", money10(MI["b_value"] * MI["b_maint"] * 5)),
             ("num", money10(MI["b_value"] * MI["b_maint"] * 20)), tag("asm")],
        ],
        note="Accumulation is undiscounted and ignores inflation in construction costs, which "
             "have historically risen faster than the general price level."))

    b.append("<h2>A plausible five-year sequence</h2>")
    b.append(table(
        "A typical sequence for buildings of this age, with the reserve line it would come out "
        "of. Each item is a placeholder until an inspection replaces it.",
        ["Year", "Property A", "#Cost", "Property B", "#Cost"],
        [
            ["1", "Inspection and deferred items found at transfer", ("num", money10(15000)),
             "Inspection, and any deferred items", ("num", money10(20000))],
            ["2", "Roof: inspection, repair or replacement", ("num", money10(45000)),
             "Exterior paint and common-area repairs", ("num", money10(35000))],
            ["3", "Sewer lateral and water heater", ("num", money10(25000)),
             "Sewer lateral, and one unit's kitchen or bath", ("num", money10(40000))],
            ["4", "Heating system and windows", ("num", money10(35000)),
             "Roof repair or replacement share", ("num", money10(45000))],
            ["5", "Interior refresh; seismic evaluation", ("num", money10(30000)),
             "Seismic retrofit evaluation and soft-story work if required",
             ("num", money10(60000))],
            ["Total, five years", "", ("num", money10(150000)), "",
             ("num", money10(200000))],
        ],
        note="These are planning placeholders, not quotes. The five-year total for Property A is "
             "about " + pct(150000 / MI["a_value"], 1) + " of its value and for Property B about "
             + pct(200000 / MI["b_value"], 1) + "; both are inside the 20-year reserve "
             "accumulations above, which is the point of holding a reserve."))

    b.append("<h2>Why this matters to the decision</h2>")
    b.append("<p>Maintenance is one of the few costs that differs sharply between paths. A "
             "house sold at the transfer date needs no reserve for the following twenty years. "
             "A house kept for twenty years needs a new roof, a sewer lateral and a heating "
             "system, and the buyer will discount the price for any of them left undone. The "
             "model captures the average of that with the reserve line; the lumpiness is what "
             "actually breaks a household's cash flow.</p>")
    b.append(note(
        "The practical rule: fund the reserve whether or not the house is kept. A house being "
        "sold still needs to be in saleable condition, and the cost of preparing it for sale is "
        "the first thing buyers negotiate. The reserve is not a cost of keeping; it is a cost of "
        "owning anything.", "good"))

    write("maintenance.html", shell("maintenance.html",
                                    "Five-year building plan for both properties",
                                    "\n".join(b)))

    # ------------------------------------------------------------------ valuation
    b = [h1("Date-of-death valuation",
            "One number governs three separate taxes and one non-tax question, and it has to be "
            "established in the worst possible circumstances: the fair market value of Property "
            "A on the date the owner dies. It becomes the income-tax basis automatically, it is "
            "reported on the estate tax return, and it is the starting point for the property "
            "tax reassessment.")]

    b.append('<div class="answer"><div class="k">Why this one number matters so much</div>'
             '<div class="v">It sets the basis, the estate value, and the fairness of both.</div>'
             '<p>A valuation set too low understates basis, so the heir pays more income tax on a '
             'later sale. Set too high, it overstates the estate and could produce an estate tax '
             'liability that is not owed. There is no single number that is optimal for both; '
             'there is only a number that is defensible.</p></div>')

    b.append("<h2>What the number is used for</h2>")
    b.append(table(
        "Four uses of one date-of-death value, and what happens if it is wrong.",
        ["Use", "What it does", "If it is too low", "If it is too high"],
        [
            ["Income-tax basis", "Sets the gain on any later sale; the step-up is automatic and "
             "requires no election. " + src("irs_p551"),
             "The heir pays capital gain tax on value that existed at death.", "Nothing; the "
             "heir benefits, but the number will not survive an audit."],
            ["Estate tax value", "Included in the gross estate and compared with the exclusion. "
             + src("irs_i706"), "Understates the estate. Low risk if the estate is far below "
             "the threshold.", "Overstates the estate and may create tax that is not owed."],
            ["Consistent-basis report", "Reported to the IRS and to the heir on Form 8971, and "
             "must match what the heir uses. " + src("irs_i706"),
             "A mismatch between the estate return and the heir's return invites inquiry.",
             "Same mismatch, in the other direction."],
            ["Property tax reassessment", "The assessor's own value, which is separately "
             "determined and may differ. " + src("scc_assessor_booklet"),
             "—", "—"],
        ]))

    b.append("<h2>How to establish it after the fact</h2>")
    b.append(table(
        "Three ways to value a house as of a past date, in order of how well they hold up.",
        ["Method", "What it produces", "When to use it", "Cost and timing"],
        [
            ["Retrospective appraisal by a licensed appraiser",
             "An opinion of value as of the date of death, using comparable sales from that "
             "period and the property's condition then.",
             "Always, and commissioned as soon as possible after death.",
             "Weeks to months. The longer the delay, the weaker the opinion."],
            ["Estate's own appraisal at the time",
             "A contemporaneous valuation, prepared for the estate return.",
             "When an appraisal is required for the return, which is usual for a property of "
             "this value.", "Commissioned within the first months."],
            ["Assessor's transfer value",
             "The county's assessed value after the change of ownership.",
             "As a cross-check, never as the basis figure.",
             "Arrives on the supplemental bill. Often differs from market value materially."],
        ]))

    b.append(risk(
        "A valuation obtained years after the death is a reconstruction. It relies on comparable "
        "sales from a past market and on somebody's memory of the property's condition. If the "
        "heir intends to sell within the same tax year, the sale price itself is the best "
        "evidence of value — which is one more argument for deciding quickly, and one reason the "
        "desk models the sale in the year of death first.",
        "Delay destroys evidence"))

    b.append("<h2>What the model does with it</h2>")
    b.append("<p>The model assumes the date-of-death value equals the market value for that "
             "year, so the basis equals the sale price only if the sale happens immediately. Any "
             "gap between the appraised value and the actual sale price creates gain or loss, "
             "and the model does not attempt to predict that gap. At a 2045 transfer under "
             "central assumptions the value is %s.</p>"
             % money10(res(2045, "baseline", "P1")["a_value"]))
    b.append(note(
        "The household's current anchor of %s is used only to establish the starting point for "
        "growth. It is not a date-of-death value and must never be reported as one on any return "
        "or in any filing." % money10(MI["a_value"]), "good"))

    write("valuation.html", shell("valuation.html", "Date-of-death valuation", "\n".join(b)))

    # ------------------------------------------------------------------ like-kind
    b = [h1("Like-kind exchange: the option that needs a decision, not a calculation",
            "A section 1031 exchange would let the household sell Property A and roll the "
            "proceeds into other rental property without paying tax on the gain. For an "
            "inherited house sold soon after death, the gain is close to zero, which means an "
            "exchange would defer almost nothing while imposing real constraints. For a house "
            "held and rented for years, the analysis is different.")]

    b.append('<div class="answer"><div class="k">The desk\'s position</div>'
             '<div class="v">Do not exchange a freshly inherited house. The step-up has already '
             'done the work.</div>'
             '<p>An exchange defers gain that does not exist yet. The cost is that the replacement '
             'property must be identified within 45 days, acquired within 180 days, and the '
             'taxpayer must hold it for investment or business use — which forecloses living in '
             'it. Applying that machinery to a house sold at a near-zero gain buys nothing.</p>'
             '</div>')

    b.append("<h2>The rules, and their cost</h2>")
    b.append(table(
        "What a section 1031 exchange requires, and why each requirement matters here.",
        ["Requirement", "What it means", "Why it is a cost in this case"],
        [
            ["Qualified property", "Real property held for productive use in a trade or "
             "business, or for investment. A personal residence does not qualify.",
             "A house the household lives in cannot be exchanged. The household would have to "
             "hold it as a rental, which forfeits the Proposition 19 exclusion."],
            ["Identification period", "45 days after the sale to identify replacement property "
             "in writing.",
             "A household grieving and administrating an estate has 45 days to commit to a "
             "replacement property. That is a deadline, not a plan."],
            ["Exchange period", "180 days after the sale to close.",
             "Both periods run from the sale date, not from when the household feels ready."],
            ["Basis carryover", "The replacement property takes the old basis, reduced by any "
             "boot received. " + src("irs_p551"),
             "The deferral is permanent only if the property is held until death, when a step-up "
             "wipes it out. That is a bet on holding for decades."],
            ["No personal use", "The replacement property must be held for investment or "
             "business use.",
             "The household cannot live in it, cannot easily use it as a second home, and must "
             "have a genuine rental or business purpose."],
            ["Section 121 interaction", "Gain is not excludable under section 121 if the home "
             "was acquired in a like-kind exchange within the past five years. " + src("irs_p523"),
             "An exchange forecloses the live-then-sell option, and with it the exclusion."],
        ]))

    b.append(risk(
        "An exchange is not a tax-free sale; it is a postponement with conditions. The "
        "conditions are strict, the deadlines are short, and the replacement property carries "
        "the old basis forward. A household that exchanges into a building it does not want, to "
        "meet a 45-day deadline, has solved a tax problem by creating a worse investment "
        "problem.",
        "Deferral is not saving"))

    b.append("<h2>When it would be worth considering</h2>")
    b.append("<p>Only in one configuration: the household has decided to rent Property A out for "
             "a substantial period, has accumulated real gain beyond the section 121 exclusion, "
             "and wants to move the equity into other rental property rather than into "
             "securities. That is a coherent strategy. It is not the strategy this desk "
             "recommends, and it starts from a path that already ranks last among the three pure "
             "choices.</p>")
    b.append(note(
        "This is a decision for the attorney and the CPA together, on the specific facts. The "
        "desk does not model an exchange, because modelling it would require assuming the terms "
        "of a replacement property that does not exist. It is listed on "
        "<a href=\"suggestions.html\">suggestions for review</a> as an open question, not as a "
        "recommendation.", "good"))

    write("like-kind.html", shell("like-kind.html",
                                  "Like-kind exchange: the option that needs a decision, not a "
                                  "calculation", "\n".join(b)))

    # ------------------------------------------------------------------ investment policy
    b = [h1("A policy for the proceeds, written before the money arrives",
            "The single largest controllable risk in this decision is not the tax, the "
            "commission or the rent. It is what the household does with a large, sudden sum of "
            "money while grieving and under deadline pressure. A written policy, adopted in "
            "advance, is the only reliable defence.")]

    b.append('<div class="answer"><div class="k">The point of writing it down first</div>'
             '<div class="v">A policy written after the money arrives is a rationalisation.</div>'
             '<p>A document adopted before the sale, while the household is calm and the amount '
             'is hypothetical, is the only version that will bind when the money is real. It '
             'should state the asset mix, the phasing schedule, the spending rule and the '
             'triggers for changing course — and it should say who is allowed to override it, '
             'and how.</p></div>')

    b.append("<h2>Terms the policy should fix in advance</h2>")
    b.append(table(
        "Each term below is a decision that is much cheaper to make now than after a sale.",
        ["Term", "Why it must be decided in advance", "A defensible starting point"],
        [
            ["How much stays in cash",
             "The household will want more cash than it needs. Deciding the amount first "
             "prevents the whole sum becoming cash by default.",
             "One to two years of household spending, plus the reserve for both buildings."],
            ["Whether to phase in, and over how long",
             "The phased path costs a little in an ordinary market and protects against an early "
             "crash. See <a href=\"phased.html\">phased investing</a>.",
             "Park 24 months in Treasuries, then buy in 24 equal monthly slices. The model "
             "quantifies the cost: about "
             + money10(abs(res(2045, "baseline", "P6")["net_worth_with_shelter"]
                            - res(2045, "baseline", "P3")["net_worth_with_shelter"]))
             + " at a 2045 transfer."],
            ["The asset mix",
             "A single large sum invites a single large position. The mix should be set by "
             "target percentages, not by conviction.",
             "A diversified mix appropriate to the household's age and other income. This desk "
             "does not recommend specific allocations."],
            ["The spending rule",
             "Liquidity changes behaviour. A rule such as a fixed percentage of the portfolio "
             "each year prevents the portfolio being consumed by its own accessibility.",
             "A percentage of the trailing average balance, set low enough that a bad decade "
             "does not force a sale."],
            ["Review triggers",
             "Annual review is too slow for a crash and too fast for nothing.",
             "Annual review, plus a scheduled review after any fall greater than 20 percent, "
             "with the standing instruction to do nothing on the day of the fall."],
            ["Who may override the policy",
             "Someone will want to. Name them, and require a written reason.",
             "No unilateral override. A change requires both spouses and a written note."],
            ["The adviser question",
             "Whether to use an adviser, and on what fee basis, is easier to decide before the "
             "money exists.",
             "If an adviser is used, a fee-only arrangement, and a fee low enough that it does "
             "not consume the assumed real return. One percent a year on this sum is a five- "
             "or six-figure deduction over twenty years."],
        ]))

    b.append(risk(
        "The model's equity return is gross of tax and fees. A taxable portfolio of this size in "
        "a high bracket, with an adviser charging one percent, might keep a little over four "
        "percent of a six and a half percent gross return. At that net return, living in "
        "Property A wins. The policy's costs are not a detail; they can reverse the "
        "recommendation.",
        "Costs and taxes can reverse the answer"))

    b.append("<h2>What to do in the first thirty days after the sale</h2>")
    b.append("<ol>"
             "<li><b>Put the proceeds in a Treasury money market or short Treasury ladder the "
             "same week.</b> Not a bank deposit above insured limits, and not an investment "
             "account with a pending allocation.</li>"
             "<li><b>Do not make any other financial decision for thirty days.</b> No new "
             "property, no gifts, no adviser contract.</li>"
             "<li><b>Confirm the tax set-aside.</b> Even a near-zero-gain sale has costs and "
             "state consequences; the CPA should confirm the amount before any of it is "
             "committed.</li>"
             "<li><b>Execute the policy's first tranche.</b> The point of writing the policy in "
             "advance is that this step requires no further judgement.</li>"
             "</ol>")

    b.append(note(
        "This page deliberately recommends no specific security, allocation or adviser. It sets "
        "out the decisions a policy must contain and the arithmetic that makes each one "
        "consequential. Any actual allocation is a matter for a licensed adviser acting on the "
        "household's full circumstances.", "good"))

    write("investment-policy.html", shell("investment-policy.html",
                                          "A policy for the proceeds, written before the money "
                                          "arrives", "\n".join(b)))

    # ------------------------------------------------------------------ annual rerun
    b = [h1("Annual re-run, and the decision log",
            "A twenty-year projection is not a decision made once. It is a set of inputs that "
            "will be wrong within a year. The discipline that makes this desk useful is re-running "
            "it every year and recording, next to each input, whether the recommendation moved.")]

    b.append("<h2>The procedure</h2>")
    b.append("<ol>"
             "<li><b>Update every input marked owner or assumption.</b> The workbook lists them "
             "all in one place. If a value has not changed, say so explicitly rather than "
             "silently reusing it.</li>"
             "<li><b>Re-run the model and rebuild the site.</b> Both steps are one command each; "
             "the site is generated from the model, so a stale site is impossible if both are "
             "run.</li>"
             "<li><b>Compare the ranking to last year's.</b> If the recommendation moved, record "
             "why, in one sentence, next to the input that moved.</li>"
             "<li><b>Check the watch list.</b> Rates, the Proposition 19 amount, the ballot, the "
             "rent ordinance, and any federal proposal touching the step-up in basis.</li>"
             "<li><b>Record the decision and its date.</b> Including a decision to do nothing. "
             "The log below is the record.</li>"
             "</ol>")

    b.append("<h2>Decision log</h2>")
    b.append(table(
        "Every decision taken, the date, and what the model said at the time. The first row is "
        "the model's own recommendation, which is not a decision by the household.",
        ["Date", "Item", "Decision", "Model's advice at the time", "Status"],
        [
            ["15 Nov 2026", "Whether to live in A, rent it out, or sell it",
             "Recommendation published, not adopted",
             "Sell A at the transfer date; move into B's third unit", tag("drv", "model output")],
            ["15 Nov 2026", "Whether to sell Property B",
             "Recommendation: do not sell B, in any scenario",
             "Selling B is among the worst two choices in every regime", tag("drv", "model output")],
            ["15 Nov 2026", "Whether to complete a like-kind exchange",
             "Deferred to attorney and CPA; not recommended on these facts",
             "An exchange defers almost nothing on a freshly inherited house",
             tag("none", "awaiting review")],
            ["15 Nov 2026", "Whether to take the Proposition 19 exclusion",
             "Conditional on occupancy; no decision until the household decides where to live",
             "Worth about " + money10(res(2045, "baseline", "P1")["prop19_relief"]
                                      * MI["a_rate_base"]) + " a year if occupied, nothing if not",
             tag("none", "awaiting decision")],
            ["15 Nov 2026", "Investment policy for the proceeds",
             "Draft terms published; nothing adopted",
             "Must be written before the money arrives", tag("none", "awaiting review")],
        ],
        note="No item in this log has been implemented. The household has not adopted any path. "
             "Nothing is implemented without approval; see "
             "<a href=\"suggestions.html\">suggestions for review</a>."))

    b.append("<h2>Watch list</h2>")
    b.append(table(
        "What to check each year, and where to check it.",
        ["Item", "Why it matters", "Where to check"],
        [
            ["The Proposition 19 applicable amount",
             "Adjusts every two years and changes the value of occupancy.",
             src("boe_lta25009")],
            ["Treasury yields",
             "Set the return on parked proceeds and the alternative to a rental.",
             src("treasury_yields")],
            ["Consumer price index",
             "Drives the 2 percent property tax cap, rent growth and the inflation assumption.",
             src("bls_cpi")],
            ["Santa Clara County tax rate book",
             "The actual rate for Property A's tax rate area, which is still unverified.",
             src("scc_assessor")],
            ["Measure H indexation",
             "Adjusts the parcel tax annually from fiscal 2028-29.",
             src("sf_propH_text")],
            ["Federal proposals on the step-up in basis",
             "Removal would change the arithmetic of every path on this desk.",
             src("sos_ca")],
            ["The rent ordinance",
             "Annual allowable increase and any change to owner move-in.",
             '<span class="tag-none">not yet sourced</span>'],
        ]))

    b.append(note(
        "The re-run is cheap: two commands and about a minute. The reason it does not happen in "
        "most households is not cost, it is that no one owns it. Someone should.", "good"))

    write("annual-rerun.html", shell("annual-rerun.html",
                                      "Annual re-run, and the decision log", "\n".join(b)))
