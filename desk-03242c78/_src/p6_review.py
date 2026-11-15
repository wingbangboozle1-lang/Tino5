# -*- coding: utf-8 -*-
"""Page set 6: briefing sheets, registers, source list, method, glossary, privacy."""
from __future__ import annotations


def build(x):
    write, h1, table, stat, risk, note = x.write, x.h1, x.table, x.stat, x.risk, x.note
    money10, pct, tag, src, shell = x.money10, x.pct, x.tag, x.src, x.shell
    res, MI, BANDS, REGIMES, CROSS, S = x.res, x.MI, x.BANDS, x.REGIMES, x.CROSS, x.S

    # ------------------------------------------------------------------ CPA brief
    p1 = res(2045, "baseline", "P1")
    p3 = res(2045, "baseline", "P3")
    p5 = res(2045, "baseline", "P5")
    b = [h1("Attorney and CPA briefing sheet: tax and income",
            "One page. Print it, hand it over, and ask for the specific answers at the bottom.")]
    b.append('<p class="small"><strong>Prepared 15 November 2026.</strong> A planning document '
             "prepared for review, not advice. All figures are projections from a stated model; "
             "statutory amounts are quoted exactly and marked. Owner-supplied figures are "
             "approximate and unverified. Nothing here identifies a person or a property.</p>")

    b.append('<div class="stats">')
    b.append(stat("Property A, inherited 2040-2050", money10(MI["a_value"]) + " today",
                  "value at a 2045 transfer: " + money10(p1["a_value"])))
    b.append(stat("Basis at death", "= date-of-death value", "automatic, no election needed"))
    b.append(stat("Section 121 exclusion", money10(250000, exact="250,000") + " single",
                  "$500,000 joint, 2 of last 5 years"))
    b.append(stat("Combined rate on a large gain", pct(0.20 + 0.038 + 0.133, 1),
                  "federal + NIIT + California"))
    b.append('</div>')

    b.append("<h2>Selling Property A in the year of death</h2>")
    b.append(table(
        "The same-year sale, line by line.",
        ["Line", "#Amount", "Basis of the figure"],
        [
            ["Value at date of death (basis)", ("num", money10(p3["a_value"])),
             "Projected at " + pct(MI["house_growth"], 1) + " a year from the owner's anchor"],
            ["Commission, escrow, title", ("num", money10(-p3["a_value"] * 0.06)),
             "Assumption, 5%-7% band"],
            ["Documentary transfer tax", ("num", money10(-p3["a_value"] * 0.0011)),
             x.ex("$0.55") + " per $500, county rate. " + src("rtc_11911")],
            ["Recording", ("num", money10(-60)), "Recording schedule, city of San Francisco"],
            ["Realised gain", ("num", money10(0)), "Basis equals value: no gain"],
            ["Federal capital gain tax", ("num", money10(0)), "No gain"],
            ["California income tax", ("num", money10(0)), "No gain"],
            ["Net to the heir", ("num", money10(p3["sale_proceeds"])), "Value less costs"],
        ]))

    b.append("<h2>If the house is lived in, then sold</h2>")
    b.append(table(
        "Live-then-sell at a 2045 transfer, against letting it out.",
        ["Item", "Live 5 years", "Let 10 years", "Note"],
        [
            ["Section 121 exclusion available",
             ("num", money10(res(2045, "baseline", "P4")["sec121_used"])),
             ("num", money10(0)), "Use test fails for a rental. " + src("irs_p523")],
            ["Depreciation recapture", ("num", money10(0)),
             ("num", money10(p5["recapture"])), "27.5-year straight line; 25% rate. "
             + src("irs_t409")],
            ["Tax on sale", ("num", money10(res(2045, "baseline", "P4")["sale_tax"])),
             ("num", money10(p5["sale_tax"])), "Federal + NIIT + California"],
            ["Net proceeds", ("num", money10(res(2045, "baseline", "P4")["sale_proceeds"])),
             ("num", money10(p5["sale_proceeds"])), ""],
        ]))

    b.append("<h2>Estate figures</h2>")
    b.append(table(
        "Federal estate and gift amounts, quoted exactly.",
        ["Item", "2026", "2027", "Source"],
        [
            ["Basic exclusion", ("num", money10(15000000, exact="15,000,000")),
             ("num", money10(15480000, exact="15,480,000")),
             src("irs_estate", "irs_ir2026_133")],
            ["Annual gift exclusion", ("num", money10(19000, exact="19,000")),
             ("num", money10(20000, exact="20,000")), src("irs_estate", "irs_ir2026_133")],
            ["Unified credit", ("num", money10(5945800, exact="5,945,800")), ("num", "—"),
             src("irs_i706")],
            ["California estate tax", ("num", "none"), ("num", "none"),
             '<span class="tag-none">no statute</span>'],
        ]))

    b.append("<h2>Questions for the CPA</h2>")
    b.append("<ol>"
             "<li>What is the filing status, and does the section 121 exclusion double to "
             + money10(500000, exact="500,000") + "?</li>"
             "<li>Have prior taxable gifts used part of the exclusion? If so, how much remains, "
             "and are the gift tax returns available?</li>"
             "<li>Is a portability election available and was a Form 706 filed at the first "
             "death? If not, can a late election still be made?</li>"
             "<li>What is the trust's income tax status, and who reports income during "
             "administration?</li>"
             "<li>Will the household be a California resident at the time of sale? If not, how is "
             "the California-source gain computed?</li>"
             "<li>What allocation between land and building should be used for depreciation if "
             "the house is let, and is an appraisal needed to support it?</li>"
             "<li>What is the expected state and federal tax on the parking-window interest "
             "while proceeds sit in Treasuries?</li>"
             "</ol>")

    b.append(note("Sources for every statutory figure are on "
                  "<a href=\"sources.html\">the source register</a>. The model itself is in the "
                  "repository and is reproducible from the inputs on "
                  "<a href=\"workbook.html\">the workbook</a>.", "good"))

    write("briefing-cpa.html", shell("briefing-cpa.html",
                                      "Attorney and CPA briefing sheet: tax and income",
                                      "\n".join(b), body_class="brief"))

    # ------------------------------------------------------------------ attorney brief
    b = [h1("Attorney and CPA briefing sheet: title, trust and deadlines",
            "One page: what must be true for the recommended path, and the dates that make it "
            "true or false.")]
    b.append('<p class="small"><strong>Prepared 15 November 2026.</strong> A planning document '
             "prepared for review, not advice. No trust instrument, deed, or title report was "
             "read in preparing it. Owner-supplied values are unverified.</p>")

    b.append("<h2>The facts as the desk understands them</h2>")
    b.append(table(
        "What the desk assumes, with the confidence it has.",
        ["Assumption", "Confidence", "What would confirm it"],
        [
            ["Property A passes outright to the heir at the second death, through a trust",
             tag("unv", "unverified"), "The trust instrument, and the deed into the trust"],
            ["The heir will be an individual child of the transferor",
             "assumed", "The instrument and the family record"],
            ["The heir does not already own a principal residence that would defeat the "
             "occupancy condition", tag("unv", "unverified"), "A conversation, not a document"],
            ["Property A is the transferor's principal residence at death",
             "assumed", "Homestead or exemption records, utility records, voter registration"],
            ["Property B is owned outright or on a known mortgage, with two units let",
             "owner-supplied", "The leases, the deed, and the loan statement"],
        ]))

    b.append("<h2>The three legal conditions that carry money</h2>")
    b.append(table(
        "Each condition, its deadline, and the consequence of failure.",
        ["Condition", "Deadline", "Consequence of failure", "Source"],
        [
            ["Occupy Property A as principal residence",
             "within 1 year of the transfer",
             "The Proposition 19 exclusion is lost; the house is reassessed at market value, "
             "costing about " + money10(p1["a_taxable"] * MI["a_rate_base"]
                                        - p1["a_annual_tax_now"]) + " a year",
             src("rtc_63_2")],
            ["File the homeowners' or disabled veterans' exemption",
             "within 1 year of the transfer",
             "The exclusion is conditioned on the claim; without it the benefit does not exist",
             src("rtc_63_2")],
            ["Continue to occupy; do not let the property out",
             "every year until sale",
             "Reassessment as of the date eligibility ends, with a supplemental bill",
             src("rtc_63_2")],
            ["Claim the exclusion", "within 3 years, or before transfer to a third party",
             "A backstop only; the occupancy facts must exist regardless", src("rtc_63_2")],
            ["File a timely Form 706 if portability is wanted", "within 9 months of death",
             "The deceased spouse's unused exclusion is wasted", src("irs_estate")],
        ]))

    b.append("<h2>Title and transfer questions for counsel</h2>")
    b.append("<ol>"
             "<li>How does the trust hold Property A, and what does the instrument direct on the "
             "second death — outright distribution, continuing trust, or a power of appointment?</li>"
             "<li>If the property continues in trust rather than distributing outright, does the "
             "transferee meet the Proposition 19 definition of an eligible transferee, and who "
             "occupies it?</li>"
             "<li>Is a distribution out of the trust to the beneficiary a transfer for property "
             "tax purposes, and when does it take effect?</li>"
             "<li>Does the trust direct a sale, or does it give the trustee discretion that "
             "conflicts with the heir's plans?</li>"
             "<li>Is there a mortgage, reverse mortgage, or lien that survives the transfer?</li>"
             "<li>Does the deed into the trust describe the property in a way that would affect "
             "the tax rate area or the parcel's assessment?</li>"
             "<li>What probate or administration filing does this estate actually require, given "
             "that Property A alone exceeds the small-estate threshold of "
             + money10(166250, exact="166,250") + "?</li>"
             "<li>Are there any claims, creditor issues, or litigation that would make a sale "
             "necessary regardless of the financial analysis?</li>"
             "</ol>")

    b.append("<h2>What the desk recommends, in one line</h2>")
    b.append(note("<strong>Sell Property A at the transfer date; do not sell Property B; decide "
                  "on occupancy only if the household genuinely intends to live in the house for "
                  "years, because the exclusion is conditional and revocable.</strong> "
                  "The financial margin is small enough that a non-financial reason to keep the "
                  "house is a legitimate basis for deciding differently.", "good"))

    write("briefing-attorney.html", shell("briefing-attorney.html",
                                          "Attorney and CPA briefing sheet: title, trust and "
                                          "deadlines", "\n".join(b), body_class="brief"))

    # ------------------------------------------------------------------ questions / gaps
    b = [h1("Questions and information gaps",
            "Everything the desk does not know, stated as a question, with the action that would "
            "close it and the page it would change. This register is the honest boundary of the "
            "analysis: below it, the numbers are arithmetic on assumptions.")]

    b.append('<div class="stats">')
    b.append(stat("Open questions", "18", "grouped by what they would change"))
    b.append(stat("Inputs marked assumption", "11", "listed on the workbook"))
    b.append(stat("Inputs marked unverified", "6", "owner-supplied or unsourced"))
    b.append(stat("Blocking the recommendation", "2", "questions 1 and 2"))
    b.append('</div>')

    rows = [
        ["1", "What is Property A actually worth, on an appraisal basis?", "A property appraisal",
         "Every dollar figure on the desk", "Blocks the magnitude, not the direction",
         tag("unv")],
        ["2", "What would Property A rent for, from three written comparables?",
         "Three rental comparables from a local manager",
         "Every letting path", "Blocks the rent case entirely", tag("unv")],
        ["3", "What is the tax rate area on Property A's own bill, and what is the rate?",
         "The current tax bill", "All property tax figures for A",
         "Narrows the band from 1.15%-1.41% to one number", tag("unv")],
        ["4", "Have prior taxable gifts used part of the exclusion?",
         "Prior gift tax returns, or the CPA's records", "Estate tax page",
         "Could make portability the most valuable item in the file", tag("unv")],
        ["5", "Was a Form 706 filed at the first death, and was portability elected?",
         "The estate's file for the first death", "Estate tax page, timeline",
         "Could be worth an entire exclusion", tag("unv")],
        ["6", "What does the trust instrument direct on the second death?",
         "The trust instrument and any amendments", "Every path",
         "Could change the answer before any number does", tag("unv")],
        ["7", "Is Property A the transferor's principal residence at death?",
         "Homestead exemption, utility and voter records", "Proposition 19 page",
         "Without it the exclusion is unavailable", tag("unv")],
        ["8", "Are both units at Property B under current written leases, at what rent?",
         "The leases and the rent registration", "Property B cash flow",
         "Could move B's contribution materially", tag("unv")],
        ["9", "What is the allowable annual rent increase under the local ordinance?",
         "The rent ordinance and the annual bulletin", "Property B cash flow",
         "The model assumes rent grows with inflation, which may be optimistic",
         tag("unv")],
        ["10", "Is the third unit at Property B vacant, or would an owner move-in be required?",
         "The leases, and a conversation with the tenants", "Every path that houses the "
         "household in B", "An eviction would be slow, costly and regulated", tag("unv")],
        ["11", "What is the household's actual cost basis in Property B?",
         "Purchase documents, improvement records, depreciation schedules",
         "The sell-B comparison", "Makes the sell-B path look cheaper than it is", tag("unv")],
        ["12", "What is the household's filing status and marginal bracket at the time of sale?",
         "A CPA's projection", "The section 121 amount and the rate on every gain",
         "Could halve or double the exclusion", tag("unv")],
        ["13", "Will the household be a California resident when the sale occurs?",
         "A conversation, planned in advance", "California tax on the gain",
         "Mostly a planning question, not a discovery one", tag("unv")],
        ["14", "What is the condition of both buildings, from an inspection?",
         "Two building inspections", "Maintenance plan, and the reserve assumption",
         "Could move the reserve by a factor of two", tag("unv")],
        ["15", "What are the actual commissions and costs of sale in these two counties?",
         "Two broker quotes each", "Selling costs, and every sell path",
         "A full percentage point is a five-figure sum here", tag("unv")],
        ["16", "Is any earthquake retrofit required or pending on either building?",
         "The local building department's records", "Maintenance plan and insurability",
         "Soft-story work on a three-unit building can be a large one-time cost", tag("unv")],
        ["17", "What is the household's other income, and how much does it spend?",
         "A budget, and the last two tax returns", "The spending rule in the investment policy",
         "Determines the cash reserve, not the ranking", tag("unv")],
        ["18", "What insurance is actually in force, on what terms, at what premium?",
         "Both declarations pages", "Operating costs", "The owner's estimate may be low",
         tag("unv")],
    ]
    b.append(table(
        "The gap register. Question 1 and 2 block the magnitude of the recommendation; the rest "
        "refine or confirm it.",
        ["#", "Question", "Document or action that closes it", "What it would change",
         "How much it matters", "Status"],
        rows))

    b.append("<h2>What the desk did not attempt</h2>")
    b.append("<ul>"
             "<li><strong>Reading the trust.</strong> Not available, and reading it is the "
             "attorney's job, not this desk's.</li>"
             "<li><strong>Appraising either property.</strong> Not a licensed appraiser.</li>"
             "<li><strong>Quoting insurance.</strong> Not an insurer or broker.</li>"
             "<li><strong>Forecasting house prices or equity returns.</strong> No one can, and the "
             "desk presents ranges and regimes rather than a forecast.</li>"
             "<li><strong>Advising on specific securities.</strong> Out of scope; see "
             "<a href=\"investment-policy.html\">the policy page</a>.</li>"
             "<li><strong>Modelling the rental market for Property A.</strong> No comparables were "
             "obtained; the rent is a labelled assumption.</li>"
             "</ul>")
    b.append(note("Each of these is a boundary the desk states rather than crosses. A projection "
                  "that pretends to know any of them would be less useful, not more.", "good"))

    write("questions.html", shell("questions.html", "Questions and information gaps",
                                  "\n".join(b)))

    # ------------------------------------------------------------------ suggestions
    b = [h1("Suggestions for review",
            "Nothing on this desk has been implemented. These are the proposals that follow from "
            "the analysis, in the order they should be considered, each with what it would cost "
            "and what it would change. Any of them can be rejected without affecting the others.")]

    b.append('<div class="answer"><div class="k">How to use this page</div>'
             '<div class="v">Read each proposal, choose a path, and nothing happens until you '
             'say so.</div>'
             '<p>Every suggestion is a decision the household could take. None has been taken. '
             'The desk recommends the first three; the rest are options that follow from the '
             'analysis and are listed so the choice is visible rather than implicit.</p></div>')

    b.append(table(
        "Proposals, with what each costs and what it would change.",
        ["#", "Suggestion", "What it would cost", "What it would change", "Desk's view"],
        [
            ["1", "<strong>Write the investment policy before the transfer.</strong> A short "
                  "document fixing the cash reserve, the phasing schedule, the asset mix, the "
                  "spending rule and who may override it.",
             "A few hours of the household's time, plus a review by the CPA.",
             "The largest controllable risk in the whole decision.",
             "Recommended"],
            ["2", "<strong>Obtain a current tax bill for Property A.</strong> It carries the tax "
                  "rate area and the exact rate, which is the weakest verified figure in the "
                  "model.",
             "Free; it is already in the household's records.",
             "Replaces a 1.15%-1.41% band with one number.",
             "Recommended"],
            ["3", "<strong>Obtain three written rental comparables for Property A.</strong>",
             "Free from most local managers.",
             "Converts the letting paths from a floor to an estimate.",
             "Recommended"],
            ["4", "Commission appraisals of both properties.", "A few hundred dollars each.",
             "Replaces both value anchors with defensible figures.", "Optional"],
            ["5", "Obtain the trust instrument and have counsel summarise its distribution terms.",
             "Counsel's time.", "Could change what is inherited, before any number matters.",
             "Optional, but ahead of the numbers"],
            ["6", "Ask the CPA whether a portability election was made at the first death.",
             "A phone call.", "Potentially the largest single item in the file.",
             "Optional, high value"],
            ["7", "Commission building inspections of both properties.",
             "A few hundred dollars each.", "Replaces the maintenance reserve assumption.",
             "Optional"],
            ["8", "Adopt the phased-entry schedule: 24 months parked, 24 monthly slices.",
             "About " + money10(abs(res(2045, "baseline", "P6")["net_worth_with_shelter"]
                                   - res(2045, "baseline", "P3")["net_worth_with_shelter"]))
             + " of expected return at a 2045 transfer.",
             "A defined answer to a crash in the first two years.", "Optional"],
            ["9", "Re-run the model every year and record each decision with its date.",
             "An hour a year.", "Keeps the recommendation honest as inputs change.",
             "Recommended"],
            ["10", "Do not complete a like-kind exchange on these facts.",
             "Nothing.", "Avoids forfeiting the section 121 exclusion and the state exclusion.",
             "Recommended, as a decision not to act"],
        ]))

    b.append("<h2>What approval looks like</h2>")
    b.append("<p>Approval is a sentence in the decision log on "
             "<a href=\"annual-rerun.html\">the annual re-run page</a>: the item, the date, and "
             "who approved it. Until then the item stays open, and the desk's recommendation "
             "stays a recommendation.</p>")
    b.append(note(
        "Nothing in this repository acts on its own. There is no automation that moves money, "
        "files a form or contacts anyone. The site is static text and the model is arithmetic.",
        "good"))

    write("suggestions.html", shell("suggestions.html", "Suggestions for review",
                                     "\n".join(b)))

    # ------------------------------------------------------------------ flagged
    b = [h1("Flagged for review",
            "Every figure on this desk that could not be traced to an official document, every "
            "internal inconsistency found while building it, and every item that needs a human "
            "decision before it can be used. Published rather than hidden, because a reader who "
            "cannot see the weak points cannot judge the strong ones.")]

    b.append("<h2>Unverified values in the model</h2>")
    b.append(table(
        "Each row is a number the model uses that no official document supports. Each is "
        "labelled on the page where it appears.",
        ["Value", "Where it comes from", "Status", "What would verify it", "Impact if wrong"],
        [
            ["Property A value " + money10(MI["a_value"]),
             "Owner's own estimate, November 2026", tag("unv"),
             "An appraisal", "Scales every figure; does not change the ranking"],
            ["Property B value " + money10(MI["b_value"]), "Owner's own estimate", tag("unv"),
             "An appraisal", "Scales the sell-B comparison"],
            ["Property A assessed value " + money10(MI["a_assessed"]),
             "Owner, rounded to $10,000", tag("unv"), "The tax bill", "Small"],
            ["Property B assessed value " + money10(MI["b_assessed"]),
             "Owner, rounded to $5,000", tag("unv"), "The tax bill", "Small"],
            ["Property A tax rate " + pct(MI["a_rate_base"], 2) + " (midpoint)",
             "Owner-implied band, not a published rate", tag("unv"),
             "The tax rate area on the bill", "Affects every keeping path"],
            ["Property B add-on " + money10(MI["b_addon"]),
             "Owner's bill less the published rate applied to assessed value", tag("unv"),
             "An itemised bill", "Small"],
            ["Rent on A " + money10(MI["a_rent_mo"]) + " a month",
             "Planning assumption; no comparables", tag("unv"),
             "Three written comparables", "Affects every letting path; letting already loses"],
            ["Property B rent " + money10(MI["b_rent_mo"]) + " a month", "Owner-supplied",
             tag("unv"), "The leases", "Affects every path"],
            ["Insurance $1,500 a building", "Owner estimate", tag("unv"),
             "Declarations pages", "Small"],
            ["Utilities", "Owner estimates", tag("unv"), "Twelve months of bills", "Small"],
            ["Cost basis of Property B", "Not supplied; assessed value used as a stand-in",
             tag("unv"), "Purchase and improvement records",
             "Makes the sell-B path under-taxed"],
            ["Filing status and bracket", "Not supplied; single, top bracket assumed", tag("unv"),
             "A CPA's projection", "Affects section 121 and every rate"],
        ]))

    b.append("<h2>Inconsistencies and issues found</h2>")
    b.append(table(
        "Issues found while building or reviewing, including ones that are not this desk's to "
        "fix. Items marked 'other desk' are recorded and left alone.",
        ["ID", "Issue", "Where", "Status", "Action"],
        [
            ["032-01", "Property A's tax rate area is not published anywhere in the model; the "
             "rate is an owner-implied band.", "property-a.html, property-tax.html",
             "Open", "Question 3 on the gap register"],
            ["032-02", "Measure H results were preliminary when read, with a further count "
             "scheduled for 17 November 2026.", "propH.html, property-b.html", "Open",
             "Re-check after certification"],
            ["032-03", "The San Francisco recording-fee schedule is used as a stand-in for "
             "Property A's county, whose schedule was not read.", "sell-path.html", "Open",
             "Read the county's recorder fee schedule"],
            ["032-04", "San Francisco's rent ordinance was not fetched, so rent-control "
             "constraints on Property B are stated but not modelled.", "rents.html, local-rules.html",
             "Open", "Fetch the ordinance and its annual bulletin"],
            ["032-05", "The 6% cost of sale is an assumption, not a published rate.",
             "sell-path.html, workbook.html", "Open", "Two broker quotes per property"],
            ["032-06", "The 60% building share for depreciation is an assumption.",
             "depreciation.html", "Open", "An appraisal allocating land and improvements"],
            ["032-07", "Ten-year and twenty-year projections use a single inflation rate per "
             "regime, not a stochastic path.", "swan.html", "By design",
             "Replace with a resampling model if a distribution rather than a regime is wanted"],
            ["032-08", "Estate tax is not computed; the estate's other assets are unknown.",
             "estate-tax.html", "Open", "Obtain a statement of the household's other assets"],
            ["032-09", "Portfolio return is modelled gross of tax and fees.",
             "workbook.html, investment-policy.html", "By design",
             "Stated as an omission that favours the sell path"],
            ["032-10", "The like-kind exchange option is described but not modelled.",
             "like-kind.html", "By design", "Requires facts that do not exist"],
            ["032-11", "Owner-supplied water, electricity and insurance figures are estimates, "
             "not bills.", "property-a.html, property-b.html", "Open",
             "Twelve months of bills and two declarations pages"],
            ["032-12", "The model compares shelter at market rent rather than applying imputed "
             "rent tax rules.", "own-vs-inherit.html", "By design",
             "Stated: the two treatments cancel for a personal residence"],
        ]))
    b.append(note(
        "Nothing on this page blocks publication. Items 032-01, 032-05 and the rent assumption "
        "are the three that would most improve the analysis, and all three are cheap to close.",
        "good"))

    b.append("<h2>How this page is maintained</h2>")
    b.append("<p>An item is closed by editing the page it appears on and recording the closure "
             "here with the date and the document that closed it. An item is never deleted; it "
             "moves to closed with its resolution, so the history of what was uncertain stays "
             "visible.</p>")

    write("flagged.html", shell("flagged.html", "Flagged for review", "\n".join(b)))

    # ------------------------------------------------------------------ sources
    b = [h1("Source register",
            "Every official document this desk relies on, what it supports, and the date it was "
            "read. Documents marked 'check' are linked so a reader can follow them but were not "
            "used to support a number on their own.")]
    b.append(table(
        "Official sources, grouped by issuing body. Every link opens the publisher's own page.",
        ["Publisher", "Document", "What it supports", "Status", "Link"],
        [
            [s["publisher"], s["title"], s["supports"],
             tag("ok") if s["status"] == "verified" else
             (tag("none", "check") if s["status"] == "check" else tag("unv", "not opened")),
             src(s["id"])]
            for s in S.SOURCES
        ],
        note="All documents were read on 15 November 2026 unless the status says otherwise. "
             "Statutory text is quoted verbatim where the desk quotes it; the rest is "
             "summarised and linked."))
    b.append("<h2>What is deliberately not cited</h2>")
    b.append(note(
        "No secondary commentary, blog, brokerage page or news article is cited as authority for "
        "any figure. Where such a page was consulted to find a primary document, the primary "
        "document is what appears here. Several widely repeated figures — including some parcel "
        "tax estimates for Measure H that do not match the ordinance's own schedule — were "
        "discarded for that reason.", "good"))

    write("sources.html", shell("sources.html", "Source register", "\n".join(b)))

    # ------------------------------------------------------------------ methodology
    b = [h1("Method, rounding and reproducibility",
            "The desk is a deterministic model plus a static site generator. Both are in the "
            "repository. Given the same inputs, it produces the same pages, and anyone can check "
            "the arithmetic rather than take it on trust.")]

    b.append("<h2>How the model works</h2>")
    b.append("<ol>"
             "<li><b>One household, one dwelling.</b> Every path houses the household in exactly "
             "one place. Shelter is valued at market rent and reported separately, so no path "
             "receives free housing.</li>"
             "<li><b>Monthly steps.</b> Cash flow is annual but portfolio growth is monthly, "
             "because the parking paths switch assets mid-year and a monthly step needs no "
             "day-count convention.</li>"
             "<li><b>Same dates, same horizon.</b> Every path is measured from the same transfer "
             "date to the same end date. Nothing is annualised differently between paths.</li>"
             "<li><b>Taxes computed per path.</b> Each path applies the rules that actually apply "
             "to it: step-up in basis, section 121 only where the use test is met, depreciation "
             "and recapture only where the property is let, Proposition 19 only where the "
             "household occupies.</li>"
             "<li><b>Regimes, then a grid.</b> Five named regimes anchored on published records, "
             "plus a five-by-five grid of house growth and equity return for the distribution.</li>"
             "<li><b>Crossovers, not just outcomes.</b> Where the ranking turns on an assumption, "
             "the desk solves for the value at which it turns, and publishes that instead of a "
             "point estimate.</li>"
             "</ol>")

    b.append("<h2>Rounding</h2>")
    b.append(table(
        "The rounding rules, and why they exist.",
        ["Rule", "What it means", "Why"],
        [
            ["Money to the nearest $10", "Every dollar figure on every page, except the "
             "statutory literals listed below.",
             "Privacy. A figure precise to the dollar can be matched to a public record. This "
             "is the household's own instruction and it is applied without exception."],
            ["Statutory amounts quoted exactly", "Thresholds, ceilings, rates and published "
             "tables are printed as published and marked <span class=\"tag-exact\">exact</span>.",
             "Rounding a legal threshold misstates it: "
             + x.ex("$1,044,586") + " rounded to " + money10(1044586)
             + " is a different number."],
            ["Percentages to one or two decimals", "Rates are shown to enough precision to be "
             "checkable, not to imply precision.",
             "A rate of 1.34% is a rate; 1.3400% claims four digits of accuracy that do not "
             "exist."],
            ["Years as whole numbers", "No fractional years anywhere.",
             "The underlying events happen on dates, not on fractions."],
        ]))
    b.append("<p>The statutory literals exempt from rounding are: "
             + ", ".join(sorted(S.STATUTORY_LITERALS)) + ". Each is registered against the "
             "document that states it, and the build fails if one appears without a "
             "registration.</p>")

    b.append("<h2>Privacy rules applied at build time</h2>")
    b.append(table(
        "Every rule the build enforces, and how.",
        ["Rule", "Enforcement"],
        [
            ["No personal names, addresses, parcel numbers or ZIP codes",
             "The build checks the generated HTML against a pattern list before writing it."],
            ["No city or neighbourhood names beyond three county-level identifiers",
             "Only 'California', 'Santa Clara County' and 'San Francisco County' appear; the "
             "build rejects a longer locality list."],
            ["No figures precise enough to match a public record",
             "Assessed values are rounded to $10,000 and $5,000 before they enter the model; "
             "money is formatted through a single rounding function."],
            ["No external requests",
             "No JavaScript, no webfonts, no images, no analytics, no third-party stylesheets. "
             "The pages are static HTML and one local CSS file."],
            ["No owner figures in the repository's history",
             "Owner figures are rounded before they are stored; the household's year-by-year "
             "tax history is deliberately not in the repository at all, only the rate band it "
             "implies."],
        ]))

    b.append("<h2>How to reproduce it</h2>")
    b.append('<p class="small mono">python3 desk-03242c78/_src/model.py<br>'
             'python3 desk-03242c78/_src/build.py<br>'
             'python3 desk-03242c78/_src/verify.py</p>')
    b.append("<p>The first writes the model output, the second writes the pages from it, and "
             "the third checks every table row for a source link or a status tag, every internal "
             "link, and every rounding rule. The build fails rather than publishing a page that "
             "breaks a rule.</p>")

    write("methodology.html", shell("methodology.html",
                                     "Method, rounding and reproducibility", "\n".join(b)))

    # ------------------------------------------------------------------ glossary
    terms = [
        ("Ad valorem tax", "A tax on value, as opposed to a flat charge per parcel. California's "
                           "one percent general levy is ad valorem; Measure H is not."),
        ("Assessed value", "The value the county uses to compute property tax. Not market value, "
                           "and usually far below it for a long-held property."),
        ("Basis", "The amount against which gain is measured. For inherited property it is the "
                  "value on the date of death, automatically."),
        ("Boot", "Cash or other property received in an exchange that is not like-kind. It is "
                 "taxable even where the exchange itself is deferred."),
        ("Consistent-basis report", "The statement an executor must give the IRS and each "
                                    "beneficiary, on Form 8971, stating the value used for basis."),
        ("Crossovers", "The value of one assumption at which the ranking of two paths reverses. "
                       "More useful than a point estimate because it states the condition."),
        ("Documentary transfer tax", "A tax on the recorded transfer of real property, set by "
                                     "statute for counties and often matched by cities."),
        ("Factored base year value", "The assessed value under Proposition 13, adjusted each year "
                                     "by the lesser of the consumer price index and two percent."),
        ("Fair market rent", "A published rent benchmark, the 40th percentile of gross rents for "
                             "standard-quality units, used for federal voucher programs. Not an "
                             "appraisal of a particular dwelling."),
        ("Form 706", "The federal estate tax return. Also the only vehicle for electing "
                     "portability of a deceased spouse's unused exclusion."),
        ("Form 8971", "The form on which consistent-basis reports are made."),
        ("Imputed rent", "The rental value of a home the owner occupies. Not taxed and not "
                         "deductible, which is why comparing it on both sides of a decision "
                         "cancels out."),
        ("Like-kind exchange", "An exchange of business or investment real property for other "
                               "real property, on which gain is deferred rather than eliminated."),
        ("Net investment income tax", "A 3.8 percent federal surtax on investment income above an "
                                      "income threshold."),
        ("Net worth including shelter", "The ranking measure used throughout: financial assets "
                                        "plus property held plus the market rent of housing "
                                        "consumed over the horizon."),
        ("Parcel tax", "A flat charge per parcel rather than a percentage of value. Measure H is "
                       "one."),
        ("Portability", "The ability of a surviving spouse to use a deceased spouse's unused "
                        "estate tax exclusion, available only by a timely election on Form 706."),
        ("Proposition 13", "The 1978 initiative that set the one percent general levy, the two "
                           "percent assessment cap, and the reassessment-on-change-of-ownership "
                           "rule."),
        ("Proposition 19", "The 2020 initiative that replaced the parent-child exclusion with a "
                           "narrower one: for a family home, an exclusion worth the applicable "
                           "amount, conditional on the child occupying it."),
        ("Recapture", "The part of a gain that represents depreciation previously deducted, taxed "
                      "at up to 25 percent rather than the capital gain rate."),
        ("Regime", "A named set of market assumptions anchored on a published record, used to "
                   "test a decision against a plausible past rather than an average."),
        ("Section 121", "The income tax provision excluding up to $250,000 of gain ($500,000 "
                        "joint) on the sale of a principal residence."),
        ("Section 1031", "The like-kind exchange provision."),
        ("Step-up in basis", "The reset of an asset's basis to its value at the owner's death. "
                             "The single most valuable rule in an inheritance."),
        ("Tax rate area", "A geographic unit within a county carrying its own combination of "
                          "local levies. Explains why two properties on the same street can pay "
                          "different rates."),
    ]
    b = [h1("Glossary",
            "Every term used on the desk, in plain language, in alphabetical order.")]
    b.append('<dl>')
    for t, d in sorted(terms):
        b.append('<dt><strong>%s</strong></dt><dd>%s</dd>' % (t, d))
    b.append('</dl>')
    b.append('<style>dt{margin-top:.7rem}dd{margin:.15rem 0 .1rem 0;color:#3d434b;font-size:.93rem}</style>')
    write("glossary.html", shell("glossary.html", "Glossary", "\n".join(b)))

    # ------------------------------------------------------------------ privacy
    b = [h1("Privacy statement",
            "This desk is published so that it can be reviewed. It is built so that it cannot be "
            "used to identify anyone.")]

    b.append("<h2>What is not here</h2>")
    b.append(table(
        "The categories removed, and how.",
        ["Category", "Treatment"],
        [
            ["Names of any person", "None appear. The household is referred to as 'the household' "
                                    "or 'the heir' throughout."],
            ["Street addresses", "None appear. The properties are described by county only."],
            ["Assessor's parcel numbers", "None appear, in any form."],
            ["ZIP codes or postal codes", "None appear."],
            ["City or neighbourhood names", "Do not appear. The desk names only California, Santa "
                                            "Clara County and San Francisco County, because the "
                                            "tax rules differ at county level and the comparison "
                                            "would be misleading without them."],
            ["Account numbers", "None. No financial account, loan, or policy number is referenced."],
            ["Assessed values exact to the dollar",
             "Rounded to $10,000 and $5,000 before entering the model. An exact assessed value "
             "matches one parcel in an open assessment roll."],
            ["The household's year-by-year tax and assessed-value history",
             "Deliberately not stored in this repository. Only the rate band it implies is kept, "
             "as three numbers."],
            ["Photographs", "None. The desk is text and one stylesheet."],
        ]))

    b.append("<h2>Why the county names stay</h2>")
    b.append("<p>Property tax is administered by county and the rules genuinely differ: the "
             "transfer tax, the recording fees, the assessment calendar and the rent ordinance "
             "are all local. Removing the county names would make the desk unusable without "
             "meaningfully protecting anyone, because a county of a million people does not "
             "identify a household. The parcel-level facts — value, address, assessment history — "
             "are what would identify it, and none of them appear.</p>")

    b.append("<h2>What the site does not do</h2>")
    b.append("<ul>"
             "<li>It sets no cookies and stores nothing in the browser.</li>"
             "<li>It loads nothing from any other server: no fonts, no scripts, no images, no "
             "analytics.</li>"
             "<li>It has no forms, no comments, and no way for a reader to submit anything.</li>"
             "<li>It contains no email address or phone number.</li>"
             "<li>It links to official documents only, and none of those links carries a query "
             "parameter that could identify a reader.</li>"
             "</ul>")

    b.append("<h2>If you find something that identifies someone</h2>")
    b.append("<p>That is a defect of the same severity as a wrong figure, and more urgent. The "
             "page it appears on should be removed from publication immediately, before the "
             "figure is corrected. The <a href=\"flagged.html\">flagged for review</a> page is "
             "where such an item would be recorded.</p>")

    write("privacy.html", shell("privacy.html", "Privacy statement", "\n".join(b)))
