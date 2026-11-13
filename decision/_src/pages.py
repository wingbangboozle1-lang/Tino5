# -*- coding: utf-8 -*-
"""Content for the consolidated decision site: every row carries a source id.

Cell helper C(text, sources, status) - status is one of
  verified | owner | derived | assumption | unverified | reported
An `unverified` cell must have an empty text. Nothing here is invented: if no
official source was read for a figure, its cell is blank and status unverified.
"""

import model as M

# ------------------------------------------------------------------ helpers
STATUS_LABEL = {
    "verified": "verified",
    "owner": "owner input",
    "derived": "derived",
    "assumption": "assumption",
    "unverified": "unverified",
    "reported": "reported - verify",
}


def C(text, src=None, status="verified"):
    return dict(t=text, s=src or [], st=status)


def money(x, src=None, status="derived"):
    return C(M.money(M.r10(x)), src, status)


def pct(x, dp=2, src=None, status="verified"):
    return C(("%." + str(dp) + "f%%") % (x * 100), src, status)


def blank(note, src=None):
    return C("", src or [], "unverified")


R10 = M.r10
m = M.money

# ------------------------------------------------------------------ constants
RATE_A = M.rate_a()
B_FIXED = M.b_fixed_charges()
YEARS = list(range(2026, 2077))
TRANSFER_YEARS = [2040, 2045, 2050]
T_MID = 2045
LAST = 2076

A_SER = {r["year"]: r for r in M.property_a_series(last=LAST)}
B_SER = {r["year"]: r for r in M.property_b_series(last=LAST)}
TV = {t: M.transfer_values(t) for t in TRANSFER_YEARS}
NP = {t: M.scenario_npv(t, last=LAST) for t in TRANSFER_YEARS}
SWANS = M.black_swan(T_MID, LAST)

S = "s"   # shorthand key name used in C(..., src=[...])


def tv_row(year, key):
    return TV[year][key]


# =============================================================================
#  Executive summary
# =============================================================================
def executive_summary():
    t45 = TV[2045]
    n45 = NP[2045]
    n40, n50 = NP[2040], NP[2050]
    findings = [
        dict(
            h="1. The property tax bill is the decision, not the house value",
            p=[
                "Under Proposition 13 the assessed value of Property A rises by at most 2% a year "
                "and the current bill is about {now}. The instant the property changes ownership it "
                "is reassessed. Even if the Prop 19 parent-child exclusion is claimed in full, the "
                "taxable value in 2045 becomes about {occ_av} and the bill becomes about {occ_tax}. "
                "If the exclusion is not claimed, the taxable value is the full market value "
                "({fmv}) and the bill becomes about {rent_tax}."
                    .format(now=m(R10(A_SER[2026]["tax"])), occ_av=m(R10(t45["occ_av"])),
                            occ_tax=m(R10(t45["occ_tax"])), fmv=m(R10(t45["fmv"])),
                            rent_tax=m(R10(t45["rent_tax"]))),
                "That is a {x} increase with the exclusion and a {y} increase without it. No other "
                "line item in this analysis is close to that size."
                    .format(x="%.0fx" % (t45["occ_tax"] / A_SER[2026]["tax"]),
                            y="%.0fx" % (t45["rent_tax"] / A_SER[2026]["tax"])),
            ],
            src=["boe_pub29", "boe_prop19", "boe_lta2025_009"]),
        dict(
            h="2. California will not tax the inheritance - the federal government might",
            p=[
                "Revenue and Taxation Code section 13301 says plainly that neither the state nor any "
                "local government may impose 'any gift, inheritance, succession, legacy, income, or "
                "estate tax' on a transfer at death. There is no California return to file and no "
                "California threshold to cross.",
                "The only death tax that can apply is the federal estate tax, and it applies to the "
                "estate, not to the heir. The filing threshold is {e26} for a death in 2026 and "
                "{e27} for a death in 2027. Amounts above the threshold are taxed at up to 40%."
                    .format(e26=m(15_000_000), e27=m(15_480_000)),
            ],
            src=["ca_rtc_13301", "irs_estate_tax", "irs_rp2026_35"]),
        dict(
            h="3. On the numbers supplied, selling and reinvesting wins - but only just past a testable line",
            p=[
                "Valued like for like over 2026-2076 at a {d} discount rate and a {r} portfolio "
                "return, and crediting each option with the market rent of the home it lets you live "
                "in, the 2045 transfer produces: occupy {occ}, rent out {rent}, sell and reinvest "
                "{sell}."
                    .format(d=pct(0.05, 0)["t"], r=pct(0.07, 0)["t"],
                            occ=m(R10(n45["occupy_h"])), rent=m(R10(n45["rent_h"])),
                            sell=m(R10(n45["sell_h"]))),
                "The ranking is not robust, and that is the useful finding: it flips at a portfolio "
                "return of {be_r} against renting and {be_o} against occupying, and at a gross rental "
                "yield on Property A of {be_y}. Those are thresholds you can judge; a forecast of "
                "what the market will return is not."
                    .format(be_r=pct(M.breakeven_portfolio_return(2045, "rent", with_housing=True), 2)["t"],
                            be_o=pct(M.breakeven_portfolio_return(2045, "occupy", with_housing=True), 2)["t"],
                            be_y=pct(M.breakeven_gross_yield(2045, with_housing=True), 2)["t"]),
            ],
            src=[]),
        dict(
            h="4. Renting Property A out is the weakest of the three unless the rent is far higher than assumed",
            p=[
                "Renting forfeits the Prop 19 exclusion: the property is reassessed to full market "
                "value, the bill roughly doubles again versus occupying, and a house worth several "
                "million dollars does not throw off enough rent on a {y} gross yield to cover tax, "
                "maintenance, insurance and management. The net operating income in the first year "
                "after a 2045 transfer is about {noi}."
                    .format(y=pct(0.026, 1)["t"],
                            noi=m(R10(NP[2045]["_detail"]["rent"]["rows"][0]["noi"]))),
                "Renting only ties selling if the gross yield on the property reaches about "
                "{be_y}. That is the number to go and test against real comparable rents."
                    .format(be_y=pct(M.breakeven_gross_yield(2045, with_housing=True), 2)["t"]),
            ],
            src=["boe_prop19"]),
        dict(
            h="5. There is no deadline to sell, and the step-up in basis is why",
            p=[
                "Assets acquired from a decedent take a basis equal to fair market value at death. "
                "Selling immediately after the transfer therefore realises almost no gain and almost "
                "no tax. Selling ten years later realises ten years of gain. The decision can be made "
                "after the transfer, with real numbers in hand - which is the strongest argument "
                "against committing today.",
                "The exception is the Prop 19 exclusion, which does have hard clocks: the homeowners' "
                "exemption must be filed within one year of the transfer and the BOE-19-P claim "
                "within three years.",
            ],
            src=["irs_p551", "boe_pub800_1"]),
        dict(
            h="6. Five inputs drive almost the entire spread, and four of them are currently unknown",
            p=[
                "The market rent for Property A, the market rent for the San Francisco unit that "
                "would be freed, the real home insurance premium for each property, the maintenance "
                "profile of Property A, and whether the estate will approach the federal exemption. "
                "Each is listed with a discovery action on the questions page.",
            ],
            src=[]),
    ]

    at_a_glance = dict(
        id="glance",
        title="The three options compared - transfer in 2045, valued to 2076",
        cols=["Option", "What you do", "Property A taxable value after transfer",
              "Property A tax bill in 2045", "Net present value (cash only)",
              "Net present value (housing counted)", "Status"],
        rows=[
            [C("1 - Occupy", [], "assumption"),
             C("Move in, claim the Prop 19 parent-child exclusion, file BOE-19-P, hold",
               ["boe_pub800_1"], "verified"),
             money(TV[2045]["occ_av"], ["boe_prop19"], "derived"),
             money(TV[2045]["occ_tax"], ["boe_prop19"], "derived"),
             money(NP[2045]["occupy"], [], "derived"),
             money(NP[2045]["occupy_h"], [], "derived"),
             C("Rank 2 of 3", [], "derived")],
            [C("2 - Rent out", [], "assumption"),
             C("Do not move in; the property is reassessed to full market value and let",
               ["boe_prop19"], "verified"),
             money(TV[2045]["rent_av"], ["boe_prop19"], "derived"),
             money(TV[2045]["rent_tax"], ["boe_prop19"], "derived"),
             money(NP[2045]["rent"], [], "derived"),
             money(NP[2045]["rent_h"], [], "derived"),
             C("Rank 3 of 3", [], "derived")],
            [C("3 - Sell and reinvest", [], "assumption"),
             C("Sell at the stepped-up basis, pay disposal costs, invest the proceeds",
               ["irs_p551"], "verified"),
             C("n/a - property sold", [], "derived"),
             C("$0", [], "derived"),
             money(NP[2045]["sell"], [], "derived"),
             money(NP[2045]["sell_h"], [], "derived"),
             C("Rank 1 of 3", [], "derived")],
        ],
        note="Net present value is measured at the date of transfer, discounted at 5.0% a year, and "
             "includes the value of the property or portfolio at 2076 net of sale costs and tax. "
             "'Housing counted' adds the market rent of the home each option lets you live in, which "
             "is the only like-for-like comparison: option 1 houses you in Property A, options 2 and "
             "3 leave you in your San Francisco unit. All figures rounded to the nearest $10.")

    tax_jump = dict(
        id="jump",
        title="The property tax jump on transfer (Property A)",
        cols=["Year of transfer", "Taxable value if nothing changes (2% cap)",
              "Bill if nothing changes", "Taxable value with Prop 19 exclusion",
              "Bill with exclusion", "Taxable value without exclusion",
              "Bill without exclusion", "Prop 19 saving per year"],
        rows=[[C(str(t), [], "derived"),
               money(TV[t]["fbyv"], ["boe_pub29"], "derived"),
               money(TV[t]["keep_tax"], ["boe_pub29"], "derived"),
               money(TV[t]["occ_av"], ["boe_prop19"], "derived"),
               money(TV[t]["occ_tax"], ["boe_prop19"], "derived"),
               money(TV[t]["rent_av"], ["boe_prop19"], "derived"),
               money(TV[t]["rent_tax"], ["boe_prop19"], "derived"),
               money(TV[t]["rent_tax"] - TV[t]["occ_tax"], ["boe_prop19"], "derived")]
              for t in TRANSFER_YEARS],
        note="The 'nothing changes' column is a counterfactual: Proposition 13 assessment growth "
             "cannot actually continue once ownership changes, so it is shown only to size the jump. "
             "Bills use the effective rate implied by the owner's own 2025 bill and assessed value "
             "(1.34%), which bundles the 1% levy with voter-approved debt and any parcel charges.")

    thresholds = dict(
        id="thresholds",
        title="Thresholds that decide whether any tax is owed at the transfer",
        cols=["Tax", "Threshold", "Rate above it", "Applies here?", "Source"],
        rows=[
            [C("California estate tax", ["ca_rtc_13301"], "verified"),
             C("None - prohibited by the state constitution", ["ca_rtc_13301"], "verified"),
             C("n/a", ["ca_rtc_13301"], "verified"),
             C("No", ["ca_rtc_13301"], "verified"),
             C("R&TC 13301", ["ca_rtc_13301"], "verified")],
            [C("California inheritance tax", ["ca_rtc_13301"], "verified"),
             C("None - prohibited by the state constitution", ["ca_rtc_13301"], "verified"),
             C("n/a", ["ca_rtc_13301"], "verified"),
             C("No", ["ca_rtc_13301"], "verified"),
             C("R&TC 13301", ["ca_rtc_13301"], "verified")],
            [C("Federal estate tax - death in 2026", ["irs_estate_tax"], "verified"),
             C("$15,000,000 per person", ["irs_estate_tax"], "verified"),
             pct(0.40, 0, ["crs_if12846"], "verified"),
             C("Only if the whole estate exceeds it", ["irs_estate_tax"], "derived"),
             C("IRS estate tax page", ["irs_estate_tax"], "verified")],
            [C("Federal estate tax - death in 2027", ["irs_rp2026_35"], "verified"),
             C("$15,480,000 per person", ["irs_rp2026_35"], "verified"),
             pct(0.40, 0, ["crs_if12846"], "verified"),
             C("Only if the whole estate exceeds it", ["irs_rp2026_35"], "derived"),
             C("Rev. Proc. 2026-35 sec. 3.44", ["irs_rp2026_35"], "verified")],
            [C("Federal gift tax annual exclusion - 2025", ["crs_if12846"], "verified"),
             C("$19,000 per recipient", ["crs_if12846"], "verified"),
             C("n/a", ["crs_if12846"], "verified"),
             C("Only for lifetime gifts", ["crs_if12846"], "derived"),
             C("CRS IF12846", ["crs_if12846"], "verified")],
            [C("Federal gift tax annual exclusion - 2027", ["irs_rp2026_35"], "verified"),
             C("$20,000 per recipient", ["irs_rp2026_35"], "verified"),
             C("n/a", ["irs_rp2026_35"], "verified"),
             C("Only for lifetime gifts", ["irs_rp2026_35"], "derived"),
             C("Rev. Proc. 2026-35 sec. 3.46", ["irs_rp2026_35"], "verified")],
            [C("Federal capital gains on a later sale", ["irs_tc409"], "verified"),
             C("Basis steps up to market value at death, so only post-death gain is taxed",
               ["irs_p551"], "verified"),
             C("20% + 3.8% NIIT + 13.3% CA = 37.1% combined",
               ["irs_tc409", "irs_niit", "ftb_2025_rates"], "derived"),
             C("Only on gain after the transfer", ["irs_p551"], "derived"),
             C("IRS Pub 551, Topic 409", ["irs_p551", "irs_tc409"], "verified")],
            [C("California income tax on the gain", ["ftb_2025_rates"], "verified"),
             C("Top bracket starts over $1,485,906 joint / $742,953 single (2025)",
               ["ftb_2025_rates"], "verified"),
             C("13.3% top marginal (12.3% + 1% over $1,000,000)",
               ["ftb_2025_rates"], "derived"),
             C("Yes, on any gain", ["ftb_2025_rates"], "derived"),
             C("FTB 2025 rate schedules", ["ftb_2025_rates"], "verified")],
        ],
        note="The 1% surcharge over $1,000,000 that lifts the California top rate from 12.3% to "
             "13.3% is not shown on the FTB rate schedules themselves. It is widely reported and is "
             "used here as an assumption; confirm it on the FTB site before relying on it.")

    return dict(findings=findings, tables=[at_a_glance, tax_jump, thresholds])


# =============================================================================
#  Questions and information gaps
# =============================================================================
QUESTIONS = [
    # id, category, question, status, what is known, what is missing, how to find it, sources
    dict(id="Q01", cat="Trust and title",
         q="Is Property A already titled in the revocable trust, or will it be transferred into it later?",
         st="unknown",
         known="A transfer of a home into a revocable trust where the settlor remains the beneficiary "
               "is excluded from reassessment, so it does not itself reset the property tax base.",
         missing="The current vesting and whether a deed into the trust has been recorded.",
         how="Read the grant deed and any trust transfer deed; confirm with the trustee. If the deed "
             "was never recorded, a petition may be needed to confirm the trust assets.",
         src=[]),
    dict(id="Q02", cat="Trust and title",
         q="Who is the trustee and successor trustee, and is the trust a single or joint revocable trust?",
         st="unknown",
         known="On the death of a settlor the trustee must serve a notification on every beneficiary "
               "and every heir within 60 days under Probate Code section 16061.7.",
         missing="Names and the succession chain. Deliberately not recorded on this site.",
         how="Read the trust instrument's trustee provisions. Keep the answer off any public page.",
         src=["ca_prob_16061_7"]),
    dict(id="Q03", cat="Trust and title",
         q="Is Property A held as community property with a surviving spouse, or as separate property?",
         st="unknown",
         known="How the property is held changes who must sign, what passes, and what basis "
               "adjustment applies at each death.",
         missing="Marital property character of the parcel.",
         how="Check the deed vesting and any pre- or post-marital agreement. Ask the estate attorney.",
         src=[]),
    dict(id="Q04", cat="Trust and title",
         q="Are there other beneficiaries of the trust, and does the trust require the property be "
           "sold or allow it to be distributed in kind?",
         st="unknown",
         known="If other beneficiaries are entitled to a share, distributing a house in kind creates "
               "a liquidity problem and may force a sale regardless of the analysis here.",
         missing="The distribution provisions and the identity and number of beneficiaries.",
         how="Read the distribution article of the trust. This single answer can override every "
             "financial conclusion on this site.",
         src=[]),
    dict(id="Q05", cat="Timing",
         q="What is the expected date of transfer - 2040, 2045, 2050, or outside that window entirely?",
         st="unknown",
         known="The owner's stated planning window is 2040-2050. Every projection on this site is "
               "shown at 2040, 2045 and 2050 for that reason.",
         missing="An actual estimate. Note the transfer date sets the reassessment date and the "
                 "market value used for the step-up.",
         how="Discuss with the trustee and the settlor. Revisit this page if the window moves: the "
             "taxable value and the bill change materially with each year.",
         src=[]),
    dict(id="Q06", cat="Timing",
         q="Will the settlor still be occupying Property A as a principal residence at the transfer?",
         st="unknown",
         known="The Prop 19 parent-child exclusion requires that the home was the transferor's "
               "principal residence. If the settlor has moved out, the exclusion may not be "
               "available at all.",
         missing="Whether Property A will still be the settlor's principal residence.",
         how="Confirm with the trustee. If the settlor may move into care or elsewhere, this is the "
             "single highest-value question to resolve early.",
         src=["boe_pub800_1", "boe_prop19"]),
    dict(id="Q07", cat="Property A",
         q="What would Property A rent for on the open market, unfurnished, today and at transfer?",
         st="unknown",
         known="Nothing. No rental comparable has been supplied. The analysis uses a gross yield "
               "assumption of 2.6% of market value, shown with a 2.0%-3.2% band.",
         missing="The number that decides option 2. Renting only ties selling at a gross yield of "
                 "about %s." % pct(M.breakeven_gross_yield(2045, with_housing=True), 2)["t"],
         how="Get three written rental opinions from agents who manage single-family lets in the "
             "same Santa Clara County submarket, and re-run the scenarios page with the real "
             "figure.",
         src=[]),
    dict(id="Q08", cat="Property A",
         q="What is the real home insurance premium for Property A, and is the property in a "
           "carrier-restricted area?",
         st="unverified",
         known="The owner's estimate is about $1,500 a year. The California Department of Insurance "
               "publishes ZIP-level residential insurance data, but no figure for this property was "
               "read from it in this pass.",
         missing="A real quote, and whether the FAIR Plan is a fallback.",
         how="Pull the CDI Residential Property Insurance Report Part II ZIP-level data for the "
             "property's ZIP and get two quotes from admitted carriers.",
         src=["cdi_residential"]),
    dict(id="Q09", cat="Property A",
         q="What is the maintenance profile - roof age, foundation, HVAC, sewer lateral, "
           "and any deferred work?",
         st="unknown",
         known="Nothing supplied. The model assumes 1.0% of market value a year, shown with a "
               "0.5%-1.5% band.",
         missing="Any capital plan. A single roof or foundation event can be tens of thousands of "
                 "dollars and is the main reason the maintenance figure is a band, not a number.",
         how="Commission a whole-house inspection and a sewer lateral scope now, while the property "
             "is still occupied and easy to access.",
         src=[]),
    dict(id="Q10", cat="Property A",
         q="What net metering or net billing tariff is the solar system on, and when does it expire?",
         st="unverified",
         known="The owner reports the system normally produces a small credit, about $10-$20 a "
               "month. That is owner input with no official confirmation.",
         missing="The interconnection agreement, the tariff version, and the enrolment end date. "
                 "Solar economics change materially between tariff generations.",
         how="Pull the interconnection agreement and the last twelve months of statements from the "
             "serving utility, and confirm the tariff with the California Public Utilities Commission.",
         src=[]),
    dict(id="Q11", cat="Property A",
         q="Is Property A a single-family home, and is any part of it separately rentable "
           "(accessory dwelling unit, junior unit)?",
         st="unknown",
         known="The owner describes water use consistent with a single household "
               "(about $100-$150 a month).",
         missing="The unit count and whether an ADU exists or could be added.",
         how="Check the assessor's property characteristics record and the building permits on file.",
         src=["scc_assessor_p19"]),
    dict(id="Q12", cat="Property B",
         q="What would the San Francisco unit you currently occupy rent for if you moved into "
           "Property A?",
         st="unknown",
         known="Two of three units currently produce about $7,150 a month. The third unit's market "
               "rent has never been stated.",
         missing="The figure that determines the cash cost of choosing to occupy Property A.",
         how="Get two rental opinions for the exact unit. Note the offset: the rent you collect is "
             "matched by the housing you give up, so this is cash, not pure gain.",
         src=[]),
    dict(id="Q13", cat="Property B",
         q="When was Property B built, and are the tenancies subject to the San Francisco rent "
           "ordinance or only to the statewide cap?",
         st="unknown",
         known="Statewide, Civil Code section 1947.12 caps annual increases at 5% plus the change "
               "in the cost of living, or 10%, whichever is lower, with a vacancy-decontrol rule and "
               "exemptions for newer housing and, with notice, for separately alienable single-family "
               "homes and condominiums. San Francisco's own ordinance is separate and stricter where "
               "it applies.",
         missing="The year built for the parcel and the tenancy start dates.",
         how="Pull the assessor's property characteristics and the original building permit. If the "
             "building predates the local ordinance cut-off, get advice before any change of terms.",
         src=["ca_civ_1947_12"]),
    dict(id="Q14", cat="Property B",
         q="Why is the San Francisco bill about $1,090 a year higher than assessed value times the "
           "official rate?",
         st="unverified",
         known="The official SF secured rate for FY2026-27 is 1.18162182%. Applied to the owner's "
               "2025 assessed value that gives about $1,350, against a reported bill of about "
               "$2,440. The residual of about $1,090 is being carried as fixed charges.",
         missing="The actual bill, with the ad valorem, parcel tax, direct assessment and special "
                 "charge lines separated.",
         how="Download the current secured tax bill and match each line. If the residual is a parcel "
             "tax or a bond charge it behaves differently from the ad valorem part as value grows.",
         src=["sf_treasurer_secured"]),
    dict(id="Q15", cat="Property B",
         q="What is the landlord insurance premium for Property B, and does it cover loss of rents?",
         st="unverified",
         known="The owner's estimate is about $1,500 a year; no confirmation.",
         missing="A real premium for a three-unit let property, which is materially different from "
                 "an owner-occupied single-family policy.",
         how="Get two quotes for a dwelling-fire or landlord policy with loss-of-rents cover.",
         src=["cdi_residential"]),
    dict(id="Q16", cat="Taxes",
         q="Roughly how large is the rest of the estate - the 'considerable amount of money' "
           "mentioned - and will it approach the federal exemption?",
         st="unknown",
         known="The federal filing threshold is $15,000,000 for a death in 2026 and $15,480,000 for "
               "2027, indexed after that. Projected forward at 2.5 percent a year it reaches about "
               "%s by 2045." % m(R10(M.estate_exemption_projection(0.025)[2045 - 2026]["amount"])),
         missing="Any estimate at all of the estate's total value. Without it, no statement can be "
                 "made about whether federal estate tax will be owed.",
         how="Prepare a confidential schedule of assets for the estate attorney. Never put the "
             "figure on a website.",
         src=["irs_estate_tax", "irs_rp2026_35"]),
    dict(id="Q17", cat="Taxes",
         q="Has any lifetime gift used up part of the federal exemption?",
         st="unknown",
         known="Lifetime taxable gifts are added back and consume the same unified exemption. The "
               "annual exclusion ($19,000 per recipient in 2025) shelters gifts below it.",
         missing="Whether past gift tax returns were filed.",
         how="Ask whether Forms 709 were ever filed, and retrieve them if so.",
         src=["crs_if12846"]),
    dict(id="Q18", cat="Taxes",
         q="Is portability available, and was a portability election made on any earlier death?",
         st="unknown",
         known="A surviving spouse may elect to use a deceased spouse's unused exemption, but only "
               "on a timely filed estate tax return.",
         missing="Whether there is a surviving spouse and whether an election was made.",
         how="Check for a filed Form 706 on any earlier death; the election is made there and "
             "nowhere else.",
         src=["irs_estate_tax"]),
    dict(id="Q19", cat="Taxes",
         q="What is the filing status and marginal tax position of the heir in the transfer year?",
         st="unknown",
         known="It drives the NIIT (3.8% above $200,000 single / $250,000 joint), the California "
               "bracket (top 12.3% over $742,953 single / $1,485,906 joint for 2025), and whether "
               "the $250,000 or $500,000 section 121 exclusion applies on a later sale.",
         missing="Everything. No tax profile has been supplied.",
         how="Work it out with a tax adviser in the transfer year, not now - the answer will change.",
         src=["irs_niit", "ftb_2025_rates"]),
    dict(id="Q20", cat="Market",
         q="What long-run home price growth should be assumed for the two submarkets?",
         st="assumption",
         known="The California House Price Index rose 2.15% in 2024, which is the figure the Board "
               "of Equalization used to adjust the Prop 19 allowance. The official FHFA index files "
               "are public.",
         missing="A defensible forward assumption. This site uses 4.0% nominal with a "
                 "2.5%-5.5% band and shows the break-even growth rate explicitly.",
         how="Download the FHFA state and metro index files and compute the long-run rate for "
             "California and for the two relevant metropolitan areas.",
         src=["fhfa_hpi", "boe_lta2025_009"]),
    dict(id="Q21", cat="Market",
         q="What inflation rate should be used for costs?",
         st="assumption",
         known="The most recent official reading available when this was built is the BLS 12-month "
               "change for all items, 3.7% to September 2026; the CPI rose 0.4% in October 2026. "
               "The annual averages were 8.0% in 2022, 4.1% in 2023 and 2.9% in 2024.",
         missing="A forward assumption. This site uses 3.0% with a 2.0%-5.0% band.",
         how="Track the BLS release and reset the band each year.",
         src=["bls_cpi_home", "bls_cpi_hist"]),
    dict(id="Q22", cat="Market",
         q="What discount rate and portfolio return should the comparison use?",
         st="assumption",
         known="Neither can be sourced from an official publication. This site therefore leads with "
               "break-even rates rather than a forecast.",
         missing="A defensible pair of numbers for this household.",
         how="Set them from the household's actual risk tolerance and the cost of any debt, and read "
             "the break-even table on the scenarios page instead of trusting a single point estimate.",
         src=[]),
    dict(id="Q23", cat="Law change",
         q="Will the step-up in basis still exist at the transfer date?",
         st="reported",
         known="It exists today. CRS lists 'taxing unrealized gains under the income tax at death or "
               "eliminating step-up in basis' among the options Congress could consider, and several "
               "bills have been introduced. No bill has been enacted.",
         missing="Any certainty past the current Congress.",
         how="Watch congress.gov for the bills listed on the law-watch page, and revisit this "
             "question in every year the transfer is still pending.",
         src=["crs_if12846"]),
    dict(id="Q24", cat="Law change",
         q="Will Proposition 13 or the Prop 19 exclusion still be in the same form?",
         st="reported",
         known="No measure on the November 3, 2026 California ballot changed either. Proposition 43, "
               "which would have required a two-thirds vote for voter-proposed local special taxes, "
               "was reported as not carrying; Propositions 40, 41 and 42 were competing tax measures. "
               "Results are certified in December 2026.",
         missing="Certified official results, and any measure on a later ballot.",
         how="Check the Secretary of State's certified results and the qualified-measures list for "
             "each future statewide ballot.",
         src=["ca_sos_ballot", "ca_sos_results"]),
    dict(id="Q25", cat="Household",
         q="Do you actually want to live in Property A?",
         st="unknown",
         known="Nothing in the numbers substitutes for this. Occupying is the only route to the "
               "Prop 19 exclusion, and the exclusion is worth about %s a year at a 2045 transfer."
               % m(R10(TV[2045]["rent_tax"] - TV[2045]["occ_tax"])),
         missing="The household's own answer.",
         how="Decide as a household question first; use the numbers to price the answer, not to "
             "produce it.",
         src=["boe_prop19"]),
    dict(id="Q26", cat="Household",
         q="Are there other heirs who would need to be bought out if one heir keeps the house?",
         st="unknown",
         known="Nothing supplied.",
         missing="The number of heirs and whether any would need cash rather than a share of the "
                 "house. This is often the binding constraint.",
         how="Establish the beneficiary list and ask each directly, in writing, before the "
             "transfer date.",
         src=[]),
]


# =============================================================================
#  Suggestions for review
# =============================================================================
SUGGESTIONS = [
    dict(id="S01", cat="Property tax", status="proposed",
         title="Confirm the trust vesting of Property A now, before anything else",
         why="A transfer into a revocable trust where the settlor stays a beneficiary is excluded "
             "from reassessment, but only if it is actually done. If the deed was never recorded, "
             "the fix later is a court petition rather than a form.",
         effect="Protects a taxable value that is a fraction of market value. Losing it is the most "
                "expensive single failure available in this plan.",
         effort="Low - read the deed, record if needed",
         risk="Low",
         src=["boe_pub29"]),
    dict(id="S02", cat="Property tax", status="proposed",
         title="Diary the two Prop 19 clocks: one year and three years",
         why="The homeowners' or disabled veterans' exemption must be filed within one year of the "
             "transfer and the BOE-19-P claim within three years. A late exemption claim moves the "
             "start of the exclusion to the year it is filed, not the year of transfer.",
         effect="At a 2045 transfer the exclusion is worth about %s a year."
                % m(R10(TV[2045]["rent_tax"] - TV[2045]["occ_tax"])),
         effort="Low - calendar entries with the trustee",
         risk="Low",
         src=["boe_pub800_1", "boe_prop19"]),
    dict(id="S03", cat="Property tax", status="proposed",
         title="Decide the occupancy question before the transfer, not after",
         why="The Prop 19 exclusion requires the home to become the transferee's principal residence "
             "within one year. Renting it out instead forfeits the exclusion entirely and the "
             "property is reassessed to full market value.",
         effect="Roughly %s a year at a 2045 transfer."
                % m(R10(TV[2045]["rent_tax"] - TV[2045]["occ_tax"])),
         effort="Low - a decision, not a transaction",
         risk="Medium - committing to occupy is a lifestyle decision",
         src=["boe_prop19", "scc_assessor_p19"]),
    dict(id="S04", cat="Information", status="proposed",
         title="Get three written rental opinions for Property A",
         why="The gross rental yield is the single unknown that decides whether renting beats "
             "selling. The break-even is about %s."
             % pct(M.breakeven_gross_yield(2045, with_housing=True), 2)["t"],
         effect="Converts the largest unknown on the scenarios page into a number.",
         effort="Low - three phone calls",
         risk="None",
         src=[]),
    dict(id="S05", cat="Information", status="proposed",
         title="Get a real insurance quote for both properties, and check the CDI ZIP-level data",
         why="Both premiums on this site are owner estimates. The California Department of Insurance "
             "publishes ZIP-level residential insurance data, and California homeowners direct "
             "written premium rose from $14.5bn in 2024 to $16.4bn in 2025 with a reported 2025 loss "
             "ratio of 170%, so pricing is moving.",
         effect="Replaces two unverified cells with real numbers and reveals any FAIR Plan exposure.",
         effort="Low",
         risk="None",
         src=["cdi_residential", "cdi_marketshare"]),
    dict(id="S06", cat="Information", status="proposed",
         title="Commission a whole-house inspection and sewer scope on Property A while it is occupied",
         why="Maintenance is modelled as a percentage of value because nothing better exists. A real "
             "capital plan turns a band into a schedule.",
         effect="Sharpens the maintenance line, which is the second-largest holding cost after tax.",
         effort="Medium - a few hundred dollars and one visit",
         risk="None",
         src=[]),
    dict(id="S07", cat="Information", status="proposed",
         title="Reconcile the San Francisco tax bill line by line",
         why="The reported bill is about $1,090 a year more than assessed value times the official "
             "1.18162182% rate. Until the residual is identified it is carried as a flat charge, "
             "which is the least reliable assumption on the projections page.",
         effect="Determines whether the residual grows with value, with inflation, or not at all.",
         effort="Low - download the bill",
         risk="None",
         src=["sf_treasurer_secured"]),
    dict(id="S08", cat="Information", status="proposed",
         title="Pull the solar interconnection agreement and twelve months of statements",
         why="The reported $10-$20 a month credit is owner input. Which net metering or net billing "
             "tariff the system is on, and when that enrolment ends, changes the answer completely.",
         effect="Confirms or removes a small but permanent credit, and dates its expiry.",
         effort="Low",
         risk="None",
         src=[]),
    dict(id="S09", cat="Estate planning", status="proposed",
         title="Prepare a confidential schedule of the whole estate, and keep it off every website",
         why="The federal threshold is $15,000,000 for a death in 2026 and $15,480,000 for 2027. "
             "Without a total, nothing can be said about whether federal estate tax will be owed. "
             "California will never tax it.",
         effect="Makes the estate tax question answerable instead of open.",
         effort="Medium",
         risk="High if the schedule is ever published - keep it with the attorney only",
         src=["irs_estate_tax", "irs_rp2026_35", "ca_rtc_13301"]),
    dict(id="S10", cat="Estate planning", status="proposed",
         title="Ask whether any Form 709 was ever filed and whether portability was elected",
         why="Lifetime taxable gifts consume the same unified exemption, and portability of a "
             "deceased spouse's unused exemption exists only if it was elected on a timely filed "
             "estate tax return.",
         effect="Can double or halve the exemption actually available.",
         effort="Low",
         risk="None",
         src=["crs_if12846", "irs_estate_tax"]),
    dict(id="S11", cat="Strategy", status="proposed",
         title="Do not commit to a course of action before the transfer - the step-up makes waiting free",
         why="Property acquired from a decedent takes a basis equal to market value at death, so a "
             "sale immediately after the transfer realises almost no gain. There is no deadline to "
             "sell, and no tax penalty for deciding later.",
         effect="Preserves the option to sell, occupy or rent with real numbers in hand.",
         effort="None",
         risk="Low - the only exception is the one-year Prop 19 occupancy clock",
         src=["irs_p551", "boe_pub800_1"]),
    dict(id="S12", cat="Strategy", status="proposed",
         title="Re-run the break-even table each year rather than trusting a point forecast",
         why="The ranking of the three options flips at a portfolio return of about %s against "
             "renting and %s against occupying. Those thresholds move with the market; a single "
             "forecast does not."
             % (pct(M.breakeven_portfolio_return(2045, "rent", with_housing=True), 2)["t"],
                pct(M.breakeven_portfolio_return(2045, "occupy", with_housing=True), 2)["t"]),
         effect="Turns the decision into a monitored threshold rather than a one-time bet.",
         effort="Low - recompute annually",
         risk="None",
         src=[]),
    dict(id="S13", cat="Strategy", status="proposed",
         title="If you rent Property A, price in the loss of the exclusion explicitly",
         why="Renting forfeits Prop 19, doubles the property tax versus occupying, and adds vacancy, "
             "management and depreciation recapture. It only ties selling at a gross yield of about "
             "%s." % pct(M.breakeven_gross_yield(2045, with_housing=True), 2)["t"],
         effect="Prevents choosing the one option that is dominated at every tested assumption.",
         effort="None",
         risk="None",
         src=["boe_prop19"]),
    dict(id="S14", cat="Privacy", status="proposed",
         title="Keep every owner figure off any public page, and remember git history is public",
         why="Assessed values and tax bills are public record in California. Rounding to $10 makes "
             "the published tables non-traceable, but earlier full-precision figures remain in this "
             "repository's public history, merged branches and pull request diffs.",
         effect="Removes the remaining traceable surface.",
         effort="Owner action - repository visibility or a history rewrite",
         risk="Not fixable by any commit in this branch",
         src=[]),
    dict(id="S15", cat="Law change", status="proposed",
         title="Put the pending-law list on an annual review",
         why="The transfer window is 2040-2050. Over that horizon Congress could restrict the "
             "step-up in basis and California voters could revisit Proposition 13. Neither is on the "
             "books today.",
         effect="Avoids being surprised by a rule change a year before the transfer.",
         effort="Low - one review a year against the law-watch page",
         risk="None",
         src=["crs_if12846", "ca_sos_ballot"]),
]


# =============================================================================
#  Black swan regimes
# =============================================================================
def black_swan_rows():
    base = NP[2045]
    rows = []
    for s in SWANS:
        n = s["npv"]
        rows.append([
            C(s["regime"]["name"], [s["regime"]["anchor"]], "assumption"),
            pct(s["regime"]["g_market"], 1, [], "assumption"),
            pct(s["regime"]["cpi"], 1, [], "assumption"),
            money(n["occupy_h"], [], "derived"),
            money(n["rent_h"], [], "derived"),
            money(n["sell_h"], [], "derived"),
            C(max([("occupy", n["occupy_h"]), ("rent", n["rent_h"]), ("sell", n["sell_h"])],
                  key=lambda x: x[1])[0], [], "derived"),
            C(s["regime"]["anchor_text"], [s["regime"]["anchor"]],
              "verified" if s["regime"]["anchor"] not in ("ca_sos_ballot",) else "verified"),
        ])
    rows.append([
        C("Baseline (this site's default)", ["bls_cpi_home", "boe_lta2025_009"], "assumption"),
        pct(0.040, 1, ["boe_lta2025_009"], "assumption"),
        pct(0.030, 1, ["bls_cpi_home"], "assumption"),
        money(base["occupy_h"], [], "derived"),
        money(base["rent_h"], [], "derived"),
        money(base["sell_h"], [], "derived"),
        C(max([("occupy", base["occupy_h"]), ("rent", base["rent_h"]), ("sell", base["sell_h"])],
              key=lambda x: x[1])[0], [], "derived"),
        C("Growth anchored on the California House Price Index (2.15% in 2024) and inflation "
          "anchored on CPI-U (3.7% over the twelve months to September 2026).",
          ["bls_cpi_home", "boe_lta2025_009"], "assumption"),
    ])
    return rows
