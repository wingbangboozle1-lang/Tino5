# -*- coding: utf-8 -*-
"""Page set 3: the tax pages, which carry the statutory citations."""
from __future__ import annotations


def build(x):
    write, h1, table, stat, risk, note = x.write, x.h1, x.table, x.stat, x.risk, x.note
    money10, money0, pct, tag, src, shell = x.money10, x.money0, x.pct, x.tag, x.src, x.shell
    res, MI, CROSS, REGIMES = x.res, x.MI, x.CROSS, x.REGIMES

    # ------------------------------------------------------------------ estate tax
    p3 = res(2045, "baseline", "P3")
    b = [h1("Estate tax, and whether this estate is liquid enough",
            "Three separate taxes are often confused in this discussion. Only one of them is "
            "an estate tax, and on the figures available it is unlikely to apply. The other two "
            "— income tax on gain and property tax on assessed value — apply either way and are "
            "far larger. This page deals with the first; the other two have their own pages.")]

    b.append('<div class="answer"><div class="k">Bottom line</div>'
             '<div class="v">No federal estate tax is expected, and California has none.</div>'
             '<p>The federal exclusion is %s for deaths in 2026 and %s for deaths in 2027. '
             'A %s house, even after two decades of growth, sits far below either figure '
             'unless growth is extreme and the rest of the estate is large. California imposes '
             'no estate or inheritance tax: the Revenue and Taxation Code has prohibited one '
             'since 1982, and no statute on the books today imposes one. The real risk is not '
             'the tax, it is a filing obligation nobody notices, and a portability election '
             'nobody makes.</p></div>'
             % (money0(15000000), money0(15480000), money10(MI["a_value"])))

    b.append("<h2>The numbers, quoted exactly</h2>")
    b.append(table(
        "Federal estate and gift figures for the relevant years. These are statutory amounts "
        "and are quoted to the dollar rather than rounded, because a threshold rounded down is "
        "a threshold misstated.",
        ["Item", "2025", "2026", "2027", "Source"],
        [
            ["Basic exclusion amount, per person",
             ("num", money0(13990000)), ("num", money0(15000000)),
             ("num", money0(15480000)), src("irs_estate", "irs_ir2026_133")],
            ["Annual gift exclusion, per donee",
             ("num", money0(19000)), ("num", money0(19000)), ("num", money0(20000)),
             src("irs_estate", "irs_ir2026_133")],
            ["Unified credit against the tax",
             ("num", "—"), ("num", money0(5945800)), ("num", "—"), src("irs_i706")],
            ["Top marginal rate", ("num", pct(0.40, 0)), ("num", pct(0.40, 0)),
             ("num", pct(0.40, 0)), src("irs_i706")],
            ["California estate or inheritance tax",
             ("num", "none"), ("num", "none"), ("num", "none"),
             '<span class="tag-none">none enacted</span>'],
        ],
        note="The exclusion is indexed to inflation and was changed by legislation; the 2027 "
             "figure is the officially announced amount, not an extrapolation. A threshold in "
             "2040 or 2050 cannot be known, and is projected on "
             "<a href=\"swan.html\">black swans</a> instead of stated."))

    b.append("<h2>Two things that could still bite</h2>")
    b.append("<h3>Portability is not automatic</h3>")
    b.append("<p>When the first spouse dies, the unused exclusion does not pass to the "
             "survivor by itself. It passes only if the executor files a timely federal estate "
             "tax return electing portability — even where no tax is due. %s A return that is "
             "never filed because 'the estate was under the threshold' can permanently waste an "
             "exclusion equal to the whole threshold. For a married household this is the single "
             "most valuable piece of paperwork in the file.</p>" % src("irs_estate", "irs_i706"))
    b.append("<h3>Prior taxable gifts change the arithmetic</h3>")
    b.append("<p>The exclusion is a unified amount: lifetime taxable gifts use it up, and the "
             "estate gets only what is left. A household that made large gifts decades ago may "
             "have far less exclusion left than the headline figure suggests. The desk cannot "
             "compute this without the gift tax returns, which are not in the file. It is "
             "question 4 on <a href=\"questions.html\">questions and gaps</a>.</p>")

    b.append("<h2>What happens if the estate exceeds the exclusion</h2>")
    b.append("<p>At 40 percent, an estate over the threshold needs cash. A house is not cash. "
             "The estate has nine months to file and, absent an election, to pay. There are "
             "three tools, and each has a cost:</p>")
    b.append(table(
        "Estate liquidity tools, with their conditions and why each is a last resort.",
        ["Tool", "What it does", "Conditions", "Why it is not free"],
        [
            ["Section 6166 installment election",
             "Defers the estate tax attributable to a closely held business over up to 14 "
             "years, at a favourable rate on the first portion.",
             "The business interest must exceed 35% of the adjusted gross estate; the "
             "decedent must have been a US citizen or resident; a 2% portion is capped.",
             "Interest accrues, a bond or lien may be required, and the estate must stay "
             "compliant for up to 14 years."],
            ["Special-use valuation, section 2032A",
             "Values qualified real property at its actual use rather than its highest and "
             "best use, to a statutory ceiling.",
             "Property must pass to a qualified heir, be used in farming or a trade or "
             "business, and meet the 5-of-8-year use and material-participation tests.",
             "The ceiling is " + money0(1460000) + " for 2026, and the deferred tax is "
             "recaptured if the heir stops qualifying."],
            ["Sale of estate assets",
             "Raises cash directly.",
             "Needs a buyer, an appraisal, and time.",
             "A forced sale of a house under deadline pressure usually realises less than a "
             "planned sale, and the proceeds may themselves be taxable to the estate."],
        ],
        note="Conditions and ceilings are from the Form 706 instructions. " + src("irs_i706")))

    b.append(note(
        "The model does not compute an estate tax liability at all, because the estate's total "
        "value outside Property A was not supplied. What it does compute is the value of A at "
        "each transfer date: %s at 2040, %s at 2045, %s at 2050 under central assumptions. If "
        "the household's other assets are large, those are the figures a projection should "
        "start from."
        % (money10(res(2040, "baseline", "P1")["a_value"]),
           money10(res(2045, "baseline", "P1")["a_value"]),
           money10(res(2050, "baseline", "P1")["a_value"])), "good"))

    b.append("<h2>The filing that people forget</h2>")
    b.append("<p>Separately from the estate tax return, the executor must give the IRS and each "
             "beneficiary a statement of the property's value — a consistent-basis report — due "
             "within 30 days of the estate tax return's due date, or of its filing if earlier. "
             "The beneficiaries need those figures to compute their own gain. Without them, the "
             "heir's basis becomes an argument. %s</p>" % src("irs_i706"))

    write("estate-tax.html", shell("estate-tax.html",
                                   "Estate tax, and whether this estate is liquid enough",
                                   "\n".join(b)))

    # ------------------------------------------------------------------ income / basis
    b = [h1("Income tax, basis, and the single most valuable fact in the file",
            "A house inherited at death gets a new income-tax basis equal to its value on the "
            "date of death. Not an election, not a form, not a choice — it happens "
            "automatically. That one rule means a sale in the same tax year as the inheritance "
            "produces little or no taxable gain, and a sale twenty years later produces a very "
            "large one.")]

    b.append('<div class="answer"><div class="k">The consequence</div>'
             '<div class="v">Selling A within the same tax year as the inheritance is nearly '
             'tax-free. Waiting is a bet that costs income tax.</div>'
             "<p>The basis resets to market value at death. A sale at that value produces no "
             "gain. Every year the household holds it, the basis stays fixed while the value "
             "grows, and the gap becomes taxable gain taxed at federal long-term capital gain "
             "rates plus net investment income tax plus California income tax — and California "
             "has no preferential capital gain rate at all. %s</p></div>"
             % src("ftb_capgains"))

    b.append("<h2>The rates that apply to a gain</h2>")
    b.append(table(
        "Every layer of tax on a long-term capital gain realised by a California resident at "
        "the top of the income range. All rates are statutory; only the underlying gain depends "
        "on assumption.",
        ["Layer", "Rate", "When it applies", "Source"],
        [
            ["Federal long-term capital gain", ("num", pct(0.20, 0)),
             "Taxable income above the 15% threshold; the 0% and 15% brackets are available at "
             "lower income and would reduce this layer.",
             src("irs_t409")],
            ["Net investment income tax", ("num", pct(0.038, 1)),
             "3.8% of the lesser of net investment income or MAGI above $250,000 joint / "
             "$200,000 single.", src("irs_t559")],
            ["California income tax on the gain", ("num", pct(0.123, 1)),
             "Capital gain is taxed as ordinary income, with no preferential rate.",
             src("ftb_capgains")],
            ["Behavioral Health Services Tax", ("num", pct(0.01, 1)),
             "1% of taxable income above $1,000,000, reported on Form 540 line 62.",
             src("rtc_17043", "ftb_540_booklet")],
            ["Combined top marginal rate on a large gain", ("num", pct(0.20 + 0.038 + 0.133, 1)),
             "Used throughout this desk for a gain realised at the top of the range.",
             '<span class="tag-drv">sum of the four rows</span>'],
            ["Unrecaptured section 1250 gain", ("num", pct(0.25, 0)),
             "Depreciation taken on a rental, recaptured at up to 25% on sale, before the "
             "capital gain rate applies.", src("irs_t409")],
        ]))

    b.append("<h2>What that means for each decision, in dollars</h2>")
    rows = []
    for pid, lbl in (("P3", "Sell at the transfer date"),
                     ("P4", "Live in A five years, then sell"),
                     ("P5", "Let A out ten years, then sell")):
        r = res(2045, "baseline", pid)
        rows.append([lbl, ("num", money10(r["a_value"])),
                     ("num", money10(r["sale_cost"])),
                     ("num", money10(r["sec121_used"])),
                     ("num", money10(r["recapture"])),
                     ("num", money10(r["sale_tax"])),
                     ("num", money10(r["sale_proceeds"]))])
    b.append(table(
        "A 2045 transfer, central assumptions. All amounts in nominal dollars of the sale year.",
        ["Decision", "#Value at sale", "#Sale costs", "#Section 121 used", "#Depreciation "
         "recaptured", "#Tax on sale", "#Net proceeds"],
        rows,
        note="Sale costs are commission, documentary transfer tax and recording fees. The "
             "sale-at-transfer row shows no tax because the basis equals the sale price on the "
             "same date. The five-year row uses the section 121 exclusion because the household "
             "lived in the house; the letting row has no exclusion and pays recapture."))

    b.append(risk(
        "The letting row is the expensive one, and not for the reason people expect. The tax on "
        "the sale is %s, of which %s is depreciation recapture — tax on a deduction the "
        "household took for years and now pays back at 25 percent. Letting the house does not "
        "avoid tax; it defers income tax at the cost of creating recapture. See "
        "<a href=\"depreciation.html\">depreciation and recapture</a>."
        % (money10(res(2045, "baseline", "P5")["sale_tax"]),
           money10(res(2045, "baseline", "P5")["recapture"])),
        "Recapture follows the rental"))

    b.append("<h2>What is not in this page</h2>")
    b.append("<p>Three income-tax questions cannot be answered from the file and are listed as "
             "gaps rather than assumed away:</p>")
    b.append("<ul>"
             "<li><strong>The trust's own income tax status.</strong> Whether the trust is a "
             "grantor trust, a complex trust, or something else changes who pays tax on income "
             "during administration and what the beneficiaries receive. The instrument was not "
             "read.</li>"
             "<li><strong>The household's marginal bracket at the time.</strong> The 20% federal "
             "rate assumes a high-income year. A household with little other income might pay "
             "15% or, on part of the gain, nothing.</li>"
             "<li><strong>State residency at the time of sale.</strong> California taxes a "
             "nonresident on California-source gain, but the interaction with another state's "
             "rules is not modelled.</li>"
             "</ul>")
    b.append(note("Each of these is a question for the CPA, with the specific document needed "
                  "to answer it, on <a href=\"briefing-cpa.html\">the CPA briefing sheet</a>.",
                  "good"))

    write("income-basis.html", shell("income-basis.html",
                                     "Income tax, basis, and the single most valuable fact "
                                     "in the file", "\n".join(b)))

    # ------------------------------------------------------------------ property tax
    b = [h1("Property tax and assessment: three rules, one bill",
            "California property tax is not one tax. It is a base rate, a cap on how fast the "
            "assessed value can grow, and a set of local add-ons that differ street by street. "
            "Two of those are statewide and exact. The third is local, published by tax rate "
            "area, and is the reason this desk will not state a single tax rate for either "
            "building.")]

    b.append("<h2>Rule one: one percent, plus local add-ons</h2>")
    b.append("<p>Proposition 13 sets the general levy at one percent of assessed value. "
             "Everything above that — county bonds, school bonds, city measures, district "
             "assessments — is approved locally and differs by tax rate area. A county has "
             "hundreds of them. The Santa Clara County assessor's own booklet illustrates a "
             "typical area at 1.1488 per $100 and cautions that the illustration is typical, "
             "not universal. %s</p>" % src("scc_assessor_booklet"))

    b.append("<h2>Rule two: assessed value grows at most 2% a year</h2>")
    b.append("<p>The factored base year value rises each year by the change in the California "
             "consumer price index, but never more than 2 percent. In a year of high inflation "
             "the cap binds; in a year of deflation the value does not fall. This is why a "
             "building bought decades ago carries an assessed value far below its market value, "
             "and why the household's Property B is so cheap to hold. %s</p>"
             % src("scc_assessor_booklet"))

    b.append("<h2>Rule three: a change of ownership resets the value</h2>")
    b.append("<p>When a property changes ownership, it is reassessed at market value and the "
             "new figure becomes the base for the 2 percent cap. An inheritance is a change of "
             "ownership. The exception is the parent-child exclusion under Proposition 19, which "
             "has its own page. A transfer into a revocable trust by the owner is not a change of "
             "ownership; a distribution out of the trust to a beneficiary at death is. %s</p>"
             % src("rtc_63_2"))

    b.append("<h2>The two buildings side by side</h2>")
    b.append(table(
        "Property tax comparison at the start of the projection. Every line states whether it "
        "is verified, owner-supplied, derived or assumed.",
        ["Item", "Property A", "Property B", "Status"],
        [
            ["Owner's value anchor",
             ("num", money10(MI["a_value"])), ("num", money10(MI["b_value"])), tag("own")],
            ["Assessed value carried in the model",
             ("num", money10(MI["a_assessed"])), ("num", money10(MI["b_assessed"])),
             tag("own", "owner, rounded")],
            ["Published rate available for this parcel",
             ("num", '<span class="tag-unv">no</span>'),
             ("num", pct(MI["b_rate"], 5)),
             tag("ok", "B only")],
            ["Rate used in the model",
             ("num", pct(MI["a_rate_base"], 3) + " (owner-implied)"),
             ("num", pct(MI["b_rate"], 5) + " + " + money10(MI["b_addon"])),
             tag("drv")],
            ["Annual tax, first year",
             ("num", money10(MI["a_assessed"] * MI["a_rate_base"])),
             ("num", money10(MI["b_assessed"] * MI["b_rate"] + MI["b_addon"] + 249)),
             tag("drv")],
            ["Measure H parcel tax after 1 July 2027",
             ("num", "n/a"), ("num", money10(249)),
             tag("exact")],
            ["Homeowners' exemption available",
             ("num", money10(7000) + " of assessed value"),
             ("num", "not claimed"), tag("ok", "A: statutory")],
        ],
        note="The homeowners' exemption reduces assessed value by up to $7,000, worth roughly "
             "$80 a year at these rates. It must be claimed by 15 February; a late claim may be "
             "accepted through 10 December. " + src("scc_assessor_booklet")))

    b.append(risk(
        "Property A's rate is the weakest verified figure in the model. The owner-implied band "
        "is %s to %s, and the county's typical area is %s. The parcel's own tax rate area was "
        "not obtained. A buyer of Property A would get the actual rate from the title company "
        "before closing; the household should get it from its own tax bill now."
        % (pct(0.01323, 3), pct(0.01407, 3), pct(MI["a_rate_floor"], 3)),
        "One unverified input carries a lot of the answer"))

    b.append("<h2>What the transfer does to the bill</h2>")
    b.append(table(
        "Property A's annual tax before and after a transfer, under each decision. Computed at "
        "a 2045 transfer with the owner-implied rate.",
        ["Decision", "#Assessed value before", "#Assessed value after", "#Annual tax after",
         "#Change"],
        [
            ["The household moves in and claims the exclusion",
             ("num", money10(res(2045, "baseline", "P1")["a_prior_taxable"])),
             ("num", money10(res(2045, "baseline", "P1")["a_taxable"])),
             ("num", money10(res(2045, "baseline", "P1")["a_annual_tax_now"])),
             ("num", money10(res(2045, "baseline", "P1")["a_annual_tax_now"]
                             - res(2045, "baseline", "P1")["a_prior_taxable"] * MI["a_rate_base"]))],
            ["The house is let out or sold (no exclusion)",
             ("num", money10(res(2045, "baseline", "P2")["a_prior_taxable"])),
             ("num", money10(res(2045, "baseline", "P2")["a_taxable"])),
             ("num", money10(res(2045, "baseline", "P2")["a_annual_tax_now"])),
             ("num", money10(res(2045, "baseline", "P2")["a_annual_tax_now"]
                             - res(2045, "baseline", "P2")["a_prior_taxable"] * MI["a_rate_base"]))],
        ],
        note="This is the cost of the exclusion decision stated as an annual bill rather than "
             "as a one-time benefit. It is what makes the occupancy question a real financial "
             "decision instead of a formality."))

    b.append("<h2>Two dates that cost money if missed</h2>")
    b.append("<ul>"
             "<li><strong>15 February</strong> — the homeowners' exemption claim for the year. "
             "A late claim may be accepted through 10 December at a penalty. "
             "%s</li>" % src("scc_assessor_booklet") +
             "<li><strong>2 July to 15 September</strong> — the window to appeal an assessed "
             "value. For a supplemental or escape assessment, 60 days from the notice. An "
             "appeal is free and does not require an attorney. %s</li>"
             % src("scc_assessor_booklet") +
             "</ul>")
    b.append(note("Both dates are on the <a href=\"timeline.html\">deadline timeline</a> with "
                  "the rest of the filing calendar, in the order they occur across a transfer "
                  "year.", "good"))

    write("property-tax.html", shell("property-tax.html",
                                     "Property tax and assessment: three rules, one bill",
                                     "\n".join(b)))

    # ------------------------------------------------------------------ prop 19
    p1 = res(2045, "baseline", "P1")
    p2 = res(2045, "baseline", "P2")
    b = [h1("Proposition 19: the exclusion that pays for occupancy",
            "Proposition 19 lets a child keep a parent's assessed value when a family home is "
            "inherited, but only up to a limit and only if the child actually moves in. Both "
            "conditions are strict, both have deadlines, and failing either one is expensive. "
            "This page quotes the statute and computes what the exclusion is worth to this "
            "household.")]

    b.append('<div class="answer"><div class="k">The two conditions, in the statute\'s words</div>'
             '<div class="v">Move in within one year. Claim the exemption within one year. '
             'Keep living there.</div>'
             "<p>The exclusion applies to the transferor's principal residence when that "
             'residence becomes the transferee\'s principal residence. The transferee must file '
             'for the homeowners\' or disabled veterans\' exemption within one year of the '
             'transfer. If the transferee later stops being eligible, the exclusion is removed '
             'and the property is reassessed as of that date. It is not a one-time certificate; '
             'it is a continuing condition.</p></div>')

    b.append("<h2>The statute, quoted</h2>")
    b.append(note(
        "Revenue and Taxation Code section 63.2, as published by the Legislature. Quoted "
        "verbatim; the paragraph breaks are the desk's.", "good"))
    b.append('<blockquote class="note">'
             '<p>“Notwithstanding subdivision (a), the purchase or transfer of a family home of '
             'the transferor shall not be a ‘change in ownership’ for purposes of this chapter, '
             'if the transferee or transferees, as applicable, file for the homeowners’ exemption '
             'or disabled veterans’ exemption, as applicable, within one year of the transfer, '
             'and the family home continues as the principal residence of the transferee or '
             'transferees.”</p></blockquote>')
    b.append('<p class="small">Revenue and Taxation Code section 63.2, opening of subdivision '
             '(a). ' + src("rtc_63_2") + '</p>')
    b.append('<blockquote class="note">'
             '<p>“The exclusion ... shall not apply if the transferee or transferees do not '
             'occupy the family home as their principal residence within one year of the '
             'transfer.”</p>'
             '<p>“If the transferee or transferees become ineligible ... the exclusion shall no '
             'longer apply and the property shall be subject to reassessment ... as of the date '
             'of the change in eligibility.”</p></blockquote>')
    b.append('<p class="small">Paraphrase of the operative conditions in section 63.2(a) and '
             '(d); the operative text is at the link. ' + src("rtc_63_2") + '</p>')

    b.append("<h3>The value limit, and the amount in force</h3>")
    b.append('<blockquote class="note">'
             '<p>“... the taxable value of the family home ... shall be the sum of the '
             'following: (1) The taxable value ... determined as of the date of the transfer. '
             '(2) The amount, if any, by which the fair market value of the family home ... '
             'exceeds the sum of the taxable value determined under paragraph (1) and the '
             'applicable amount.”</p></blockquote>')
    b.append('<p class="small">Revenue and Taxation Code section 63.2(d)(2), as published. '
             + src("rtc_63_2") + '</p>')
    b.append("<p>The statute sets the constitutional amount at one million dollars and indexes "
             "it every two years to a house price index. The Board of Equalization publishes the "
             "figure in force:</p>")
    b.append(table(
        "The applicable amount, by period, from the Board of Equalization's own table.",
        ["Period", "Applicable amount", "Change", "Source"],
        [
            ["16 February 2021 – 15 February 2023", ("num", money0(1000000)), ("num", "—"),
             src("boe_lta25009")],
            ["16 February 2023 – 15 February 2025", ("num", money0(1022600)),
             ("num", "+2.26%"), src("boe_lta25009")],
            ["16 February 2025 – 15 February 2027", ("num", money0(1044586)),
             ("num", "+2.15%"), src("boe_lta25009", "boe_nr25_02")],
            ["After 15 February 2027", ("num", '<span class="tag-unv">next adjustment</span>'),
             ("num", "unknown"), src("boe_lta25009")],
        ],
        note="The Board adjusts the amount every two years using the Federal Housing Finance "
             "Agency's California house price index and announces the new figure in advance. "
             "The next adjustment takes effect 16 February 2027. A transfer in 2040 will use a "
             "figure that does not exist yet; the desk projects it at 2.5% a year and labels "
             "the projection as an assumption. " + src("fhfa_hpi")))

    b.append("<h2>What it is worth to this household</h2>")
    b.append(table(
        "The exclusion applied at each transfer date, at the central growth assumption, and what "
        "it saves in the first year.",
        ["Transfer", "#Value at transfer", "#Assessed value without exclusion",
         "#Assessed value with exclusion", "#Exclusion relief", "#First-year tax saved"],
        [
            ["2040", ("num", money10(res(2040, "baseline", "P1")["a_value"])),
             ("num", money10(res(2040, "baseline", "P2")["a_taxable"])),
             ("num", money10(res(2040, "baseline", "P1")["a_taxable"])),
             ("num", money10(res(2040, "baseline", "P1")["prop19_relief"])),
             ("num", money10(res(2040, "baseline", "P1")["prop19_relief"] * MI["a_rate_base"]))],
            ["2045", ("num", money10(res(2045, "baseline", "P1")["a_value"])),
             ("num", money10(res(2045, "baseline", "P2")["a_taxable"])),
             ("num", money10(res(2045, "baseline", "P1")["a_taxable"])),
             ("num", money10(res(2045, "baseline", "P1")["prop19_relief"])),
             ("num", money10(res(2045, "baseline", "P1")["prop19_relief"] * MI["a_rate_base"]))],
            ["2050", ("num", money10(res(2050, "baseline", "P1")["a_value"])),
             ("num", money10(res(2050, "baseline", "P2")["a_taxable"])),
             ("num", money10(res(2050, "baseline", "P1")["a_taxable"])),
             ("num", money10(res(2050, "baseline", "P1")["prop19_relief"])),
             ("num", money10(res(2050, "baseline", "P1")["prop19_relief"] * MI["a_rate_base"]))],
        ],
        note="The relief equals the applicable amount in force, because the value at transfer "
             "exceeds the prior assessed value plus the amount. The first-year saving is that "
             "relief multiplied by the owner-implied rate, and it recurs every year the "
             "household stays."))

    b.append(risk(
        "The exclusion is not free. It requires occupancy as a principal residence, and it is "
        "withdrawn if the household stops qualifying — including by moving out and renting the "
        "house, or by transferring it onward without a new claim. A household that takes the "
        "exclusion, lives in the house for two years and then lets it out does not keep the "
        "benefit; it gets a supplemental assessment and a bill for the difference. The claim "
        "itself is not a public document, but the exemption it depends on is.",
        "The exclusion can be taken back"))

    b.append("<h2>The claim, and its three-year backstop</h2>")
    b.append("<p>The statute allows a claim within three years of the transfer, or before the "
             "property is transferred to a third party, whichever comes first. A late claim may "
             "still be granted if the assessor is satisfied the household was eligible, but the "
             "safe course is to file in the first year. The claim is not a public document; the "
             "exemption that goes with it is a matter of record. %s</p>" % src("rtc_63_2"))

    b.append("<h2>What the exclusion is not</h2>")
    b.append("<ul>"
             "<li>It is not a cap on the tax. The tax is still the local rate applied to the new "
             "taxable value.</li>"
             "<li>It is not available for a second home, a rental, or a property the household "
             "does not occupy.</li>"
             "<li>It is not automatic. The exemption claim is the trigger.</li>"
             "<li>It is not the same as the older parent-child exclusion, which was unlimited. "
             "Proposition 19 replaced it for transfers on or after 16 February 2021.</li>"
             "<li>It does not apply to Property B. That building is already owned and neither "
             "transfer nor occupancy changes its assessed value.</li>"
             "</ul>")

    write("prop19.html", shell("prop19.html",
                               "Proposition 19: the exclusion that pays for occupancy",
                               "\n".join(b)))

    # ------------------------------------------------------------------ section 121
    b = [h1("Section 121: what it is worth, and what forfeits it",
            "The section 121 exclusion lets a homeowner exclude up to $250,000 of gain on a "
            "sale of a principal residence, or $500,000 for a married couple filing jointly. It "
            "requires two of the last five years of ownership and use. For this household it is "
            "worth less than it looks, because the step-up at death already gives a nearly "
            "tax-free sale — but it is the reason a live-then-sell path is not as bad as it "
            "would otherwise be.")]

    b.append("<h2>The rule, quoted</h2>")
    b.append(table(
        "The section 121 conditions, from the IRS publication for sellers of a home.",
        ["Condition", "Requirement", "How it applies here"],
        [
            ["Amount excluded",
             "$250,000 of gain for a single filer, $500,000 for a married couple filing "
             "jointly. " + src("irs_p523"),
             "The household's filing status is not in the file, so the model uses the single "
             "amount throughout. A joint return would double it."],
            ["Ownership test",
             "Owned the home for at least two of the five years ending on the sale date. "
             + src("irs_p523"),
             "Satisfied by inheritance at death: the heir owns from the date of death."],
            ["Use test",
             "Lived in the home as a principal residence for at least two of the five years "
             "ending on the sale date. " + src("irs_p523"),
             "This is the binding constraint. It is also the Proposition 19 condition."],
            ["Frequency",
             "Not excluded gain from another home sale in the two years before this one. "
             + src("irs_p523"),
             "Unknown. Question for the CPA."],
            ["Exchange disqualification",
             "Gain is not excludable if the home was acquired in a section 1031 like-kind "
             "exchange within the past five years. " + src("irs_p523"),
             "Not applicable to an inheritance, but relevant if A is exchanged first."],
        ]))

    b.append("<h2>What it is worth in this model</h2>")
    b.append(table(
        "The live-then-sell paths against selling at the transfer date, at a 2045 transfer.",
        ["Path", "#Gain before exclusion", "#Excluded", "#Taxable gain", "#Tax saved by 121",
         "#Net proceeds"],
        [
            ["Sell at transfer", ("num", money10(0)),
             ("num", money10(res(2045, "baseline", "P3")["sec121_used"])),
             ("num", money10(0)), ("num", money10(0)),
             ("num", money10(res(2045, "baseline", "P3")["sale_proceeds"]))],
            ["Live 5 years, then sell", ("num", money10(res(2045, "baseline", "P4")["sale_tax"]
                                                         + res(2045, "baseline", "P4")["sec121_used"]
                                                         * 0.371)),
             ("num", money10(res(2045, "baseline", "P4")["sec121_used"])),
             ("num", money10(res(2045, "baseline", "P4")["sale_tax"] / 0.371)),
             ("num", money10(res(2045, "baseline", "P4")["sec121_used"] * 0.371)),
             ("num", money10(res(2045, "baseline", "P4")["sale_proceeds"]))],
            ["Live 10 years, then sell",
             ("num", money10(res(2045, "baseline", "P4b")["sale_tax"] / 0.371
                             + res(2045, "baseline", "P4b")["sec121_used"])),
             ("num", money10(res(2045, "baseline", "P4b")["sec121_used"])),
             ("num", money10(res(2045, "baseline", "P4b")["sale_tax"] / 0.371)),
             ("num", money10(res(2045, "baseline", "P4b")["sec121_used"] * 0.371)),
             ("num", money10(res(2045, "baseline", "P4b")["sale_proceeds"]))],
            ["Let 10 years, then sell", ("num", money10(res(2045, "baseline", "P5")["sale_tax"]
                                                        / 0.371
                                                        + res(2045, "baseline", "P5")["recapture"])),
             ("num", money10(0)), ("num", money10(res(2045, "baseline", "P5")["sale_tax"] / 0.371)),
             ("num", money10(0)),
             ("num", money10(res(2045, "baseline", "P5")["sale_proceeds"]))],
        ],
        note="The combined marginal rate on a large gain is "
             + pct(0.20 + 0.038 + 0.133, 1) + ", so taxable gain is recovered from tax by "
             "dividing. Gain before exclusion is the taxable gain plus the excluded amount; "
             "recapture is excluded from these columns because it is taxed separately at 25%. "
             "The exclusion is capped at $250,000, which is why living longer does not shield "
             "more."))

    b.append(risk(
        "The exclusion is smaller than the gain in every live-then-sell path. At a 2045 "
        "transfer, five years of ownership produces a gain far above $250,000, so the exclusion "
        "covers only part of it and the rest is taxed at the combined rate. Section 121 is not "
        "a reason to live in the house; it is a reason that living in it for a few years is not "
        "financially irrational.",
        "Do not overstate the exclusion"))

    b.append("<h2>The partial exclusion, and when it applies</h2>")
    b.append("<p>The IRS allows a reduced exclusion when a sale is forced by a change in "
             "employment, a change in health, or an unforeseeable event, and when the "
             "two-year use test is not met. The reduced amount is proportional to the time the "
             "tests were met. %s</p>" % src("irs_p523"))
    b.append(note(
        "The model does not compute the partial exclusion. It applies the full $250,000 to "
        "every live-then-sell path that holds for at least two years, which is the conservative "
        "direction: a partial exclusion would be smaller. A household forced to sell earlier "
        "would do worse than modelled, not better.", "good"))

    write("sec121.html", shell("sec121.html",
                               "Section 121: what it is worth, and what forfeits it",
                               "\n".join(b)))

    # ------------------------------------------------------------------ depreciation
    b = [h1("Depreciation and recapture: the deduction that comes back",
            "Letting a house out allows a deduction for depreciation — the building wearing out. "
            "It is a real deduction and it does reduce tax while the house is rented. It is also "
            "a loan. On sale, the depreciation taken is recaptured at a higher rate than the "
            "capital gain, and the household pays it back whether or not the deduction was "
            "actually claimed.")]

    b.append("<h2>The rule</h2>")
    b.append("<p>Residential rental real property placed in service after 1986 is depreciated "
             "under the Modified Accelerated Cost Recovery System over 27.5 years, straight "
             "line, using the mid-month convention. Land is never depreciable; only the building "
             "is. On sale, gain attributable to depreciation is unrecaptured section 1250 gain "
             "and is taxed at a maximum rate of 25 percent before any capital gain rate "
             "applies. %s %s</p>" % (src("irs_p527"), src("irs_t409")))

    b.append("<h2>How the model treats it</h2>")
    b.append(table(
        "Every assumption behind the depreciation line, with its status.",
        ["Item", "Value used", "Status", "Reason"],
        [
            ["Recovery period", "27.5 years, straight line, mid-month convention", tag("ok"),
             "Statutory recovery period for residential rental property. " + src("irs_p527")],
            ["Share of value treated as building", pct(0.60, 0), tag("asm"),
             "An appraisal would allocate land and building; none was obtained. A 60/40 split "
             "is a common default for a single-family house in a built-up area and is the "
             "single most sensitive assumption on this page: at 50% the deduction falls by a "
             "sixth, at 70% it rises by a sixth."],
            ["Basis for depreciation", "Value on the date of death, allocated to the building",
             tag("ok", "statutory"), "Inherited property takes a basis equal to date-of-death "
             "value. " + src("irs_p551")],
            ["Recapture rate", pct(0.25, 0), tag("ok"),
             "Maximum rate on unrecaptured section 1250 gain. " + src("irs_t409")],
            ["Whether deductions were claimed", "Assumed claimed, and recaptured anyway",
             tag("ok", "statutory"), "Depreciation allowed or allowable is recaptured even if "
             "the taxpayer failed to claim it. " + src("irs_p527")],
        ]))

    p5 = res(2045, "baseline", "P5")
    p4 = res(2045, "baseline", "P4")
    b.append("<h2>What it costs at a 2045 transfer</h2>")
    b.append(table(
        "Depreciation and recapture over a ten-year letting period, compared with living in the "
        "house and selling.",
        ["Item", "Let A out ten years, then sell", "Live in A five years, then sell"],
        [
            ["Building basis", ("num", money10(p5["a_value"] * 0.60)),
             ("num", money10(p4["a_value"] * 0.60))],
            ["Depreciation per year", ("num", money10(p5["a_value"] * 0.60 / 27.5)),
             ("num", money10(0))],
            ["Depreciation taken", ("num", money10(p5["recapture"])), ("num", money10(0))],
            ["Tax on recapture at 25%", ("num", money10(p5["recapture"] * 0.25)),
             ("num", money10(0))],
            ["Section 121 exclusion available", ("num", money10(0)),
             ("num", money10(p4["sec121_used"]))],
            ["Total tax on sale", ("num", money10(p5["sale_tax"])),
             ("num", money10(p4["sale_tax"]))],
            ["Net proceeds", ("num", money10(p5["sale_proceeds"])),
             ("num", money10(p4["sale_proceeds"]))],
        ],
        note="Nominal dollars of the sale year. The letting row also loses the section 121 "
             "exclusion entirely, because the use test fails: the household did not live there "
             "two of the last five years."))

    b.append(risk(
        "Recapture is the part of the rental case that is most often overlooked. A household "
        "that lets the house out for ten years takes roughly %s of depreciation, and on sale "
        "pays about %s of tax on it at 25%%, before any capital gain. That is money that was "
        "borrowed, not money that was earned, and it is due in the year of sale whether or not "
        "the household is ready."
        % (money10(p5["recapture"]), money10(p5["recapture"] * 0.25)),
        "The deduction is a loan"))

    b.append("<h2>What would change this page</h2>")
    b.append("<ul>"
             "<li><strong>An appraisal splitting land from building.</strong> The 60 percent "
             "building share is the largest single assumption in the depreciation figures.</li>"
             "<li><strong>Capital improvements.</strong> Improvements are depreciated separately "
             "over their own recovery period and add to recapture. None are assumed.</li>"
             "<li><strong>A cost segregation study.</strong> For a house of this vintage the "
             "benefit is usually small and the cost often exceeds it; it is not modelled.</li>"
             "</ul>")

    write("depreciation.html", shell("depreciation.html",
                                     "Depreciation and recapture: the deduction that comes back",
                                     "\n".join(b)))

    # ------------------------------------------------------------------ prop H
    b = [h1("Measure H: a new parcel tax on Property B",
            "San Francisco voters approved a parcel tax to fund Muni operations on 3 November "
            "2026. It is not a property tax on value; it is a flat charge per parcel, scaled by "
            "property type and building size, and it is indexed every year. Property B is a "
            "multifamily residential parcel and will pay it from fiscal year 2027-28.")]

    b.append('<div class="answer"><div class="k">Status</div>'
             '<div class="v">Passed on preliminary results; the operative schedule is in the '
             'ordinance.</div>'
             '<p>Yes 244,760 (74.40%), No 84,209 (25.60%), needing a simple majority. The '
             'results page was headed preliminary when read, with a further count scheduled for '
             '17 November 2026. The figures below are quoted from the ordinance text, which '
             'does not change with the count.</p></div>')

    b.append("<h2>What the ordinance says</h2>")
    b.append(table(
        "The operative provisions, taken from the 'Stronger Muni For All Ordinance' text. "
        "Quoted values are exact statutory amounts.",
        ["Provision", "What it says", "Effect on Property B"],
        [
            ["Effective date",
             "The tax takes effect 1 July 2027 for fiscal year 2027-28 and continues through "
             "30 June 2042, then expires by operation of law.",
             "Nine years of the twenty-year projection, then nothing."],
            ["Multifamily residential rate",
             x.ex("$249") + " if building area is 5,000 sq ft or less; plus "
             + x.ex("$0.195") + " per sq ft above 5,000; "
             "maximum " + x.ex("$50,000") + ".",
             "A three-unit building of ordinary size is at the " + x.ex("$249")
             + " base: about " + x.ex("$21") + " a month."],
            ["Single-family rate (for comparison)",
             x.ex("$129") + " if building area is 3,000 sq ft or less; plus "
             + x.ex("$0.42") + " per sq ft above 3,000 to 5,000; then " + x.ex("$1.99")
             + " per sq ft above 5,000.",
             "Not applicable to B. Would apply to A only if A were in San Francisco, which it "
             "is not."],
            ["Indexation",
             "From fiscal year 2028-29 every dollar amount is adjusted annually by the "
             "Bureau of Labor Statistics consumer price index for the local metropolitan "
             "area as of 31 December of the preceding year, rounded down to the nearest "
             "dollar.",
             "The charge rises with local inflation, not with the 2 percent property tax cap."],
            ["Senior exemption",
             "A parcel where an individual aged 65 or over before 1 July owns a beneficial "
             "interest and occupies a dwelling unit as principal residence is exempt if "
             "single-family; a multifamily parcel is reduced by " + x.ex("$249")
             + " for each such unit.",
             "If the household moves into B's third unit after turning 65, B's tax falls by "
             + x.ex("$249") + " — to zero at the base rate."],
            ["Exemption for non-taxable parcels",
             "Parcels on which no ad valorem property tax is levied are exempt.",
             "Not applicable; B pays ad valorem tax."],
            ["Definition of building area",
             "Excludes garages, porches and decks; includes accessory dwelling unit square "
             "footage.",
             "B is almost certainly at the flat rate regardless of how the area is measured."],
        ],
        note="All provisions quoted from the ordinance text. " + src("sf_propH_text")
             + " Election result: " + src("sfelections_results")))

    b.append(risk(
        "The rates above are quoted exactly from the ordinance, but the measure's own fiscal "
        "analysis and the city's implementation guidance were not read, and the results were "
        "preliminary. The desk therefore models only the base " + x.ex("$249")
        + " and does not model the inflation index, the senior exemption, or any litigation "
        "outcome. The amount at stake for Property B is small — about %s over nine years at "
        "the base rate — so the uncertainty does not move the recommendation."
        % money10(249 * 9), "Small in dollars, uncertain in detail"))

    b.append("<h2>How it enters the model</h2>")
    b.append("<p>The model adds " + x.ex("$249") + " a year to Property B's tax for every year "
             "from the transfer "
             "through fiscal year 2041-42, growing with the general inflation assumption, and "
             "adds nothing after that. It does not apply the senior exemption because the "
             "household's ages at the transfer date are not in the file. If the household is "
             "over 65 and occupies the third unit, the line goes to zero. That is one of the "
             "what-if switches on the <a href=\"workbook.html\">workbook</a>.</p>")

    b.append("<h2>What it means for the decision</h2>")
    b.append(note("Nothing. Nine years of about %s is a rounding error against a %s asset. It is "
                  "documented here because the desk's rule is that every tax that hits either "
                  "property gets its own line and its own source, not because it changes the "
                  "answer. Documenting small items is what makes the larger ones credible."
                  % (money10(249), money10(MI["b_value"])), "good"))

    write("propH.html", shell("propH.html",
                              "Measure H: a new parcel tax on Property B",
                              "\n".join(b)))
