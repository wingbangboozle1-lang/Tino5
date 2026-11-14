# -*- coding: utf-8 -*-
"""Pages 9-17: black swans, the transfer process, questions, suggestions, law watch,
repository review, sources, flagged items and method."""

import cpi as _cpi
import shell as sh
import sources as src
import model as m
from model import money as M, pct as P
from shell import src_cell as _src_cell

pill = sh.pill
esc = sh.esc

# ------------------------------------------------------------------------ shared

_R = m.compare()
_RATE_A = m.effective_rate_a()
_RATE_LO, _RATE_HI, _RATE_HIST = m.effective_rate_a_band()
_B_RESIDUAL, _B_ADVAL = m.b_rate_residual()
_UNIT_B = m.b_unit_rent()

# First-year tax with the exclusion versus a full reassessment, on the baseline case.
_TAX_EXCL = _R["taxable_excluded"] * _RATE_A
_TAX_FULL = _R["taxable_reassessed"] * _RATE_A
_EXCL_SAVING = _TAX_FULL - _TAX_EXCL

_REMOVE_GAP = (m.compare(lead_occupancy_years=3)["assessed_excluded"][-1]
               - m.compare(lead_occupancy_years=3, removal_enrolls_capped_value=True)
               ["assessed_excluded"][-1])

_MC_OCCUPY = None
_MC_RENT = None
_REGIMES = None


def _mc():
    global _MC_OCCUPY, _MC_RENT
    if _MC_OCCUPY is None:
        _MC_OCCUPY = m.monte_carlo_cached(paths=1200, target="occupy")
        _MC_RENT = m.monte_carlo_cached(paths=1200, target="rent")
    return _MC_OCCUPY, _MC_RENT


def _regimes():
    global _REGIMES
    if _REGIMES is None:
        _REGIMES = m.regime_scenarios()
    return _REGIMES


# ------------------------------------------------------------------ 9. black swans

def page_black_swan():
    b = []
    b.append('<p class="lead">Fifty years is long enough that growth and inflation will not be '
             'constant. This page replays the real inflation record instead of assuming a smooth '
             'line, and shows what each historical environment does to the decision.</p>')

    b.append('<div class="banner warn"><b>What is real here and what is not.</b> The inflation '
             'record is the official Consumer Price Index series published by the Bureau of Labor '
             'Statistics, transcribed month by month from the series page and linked on every row. '
             'The <i>real</i> house price growth and <i>real</i> equity return attached to each '
             'historical episode are <b>assumptions</b>: no official long-run series for either was '
             'retrieved into this desk. The sampling therefore gives you a realistic <i>shape</i> '
             'for the inflation path &mdash; persistence, shocks, long stretches of calm &mdash; and '
             'not a forecast.</div>')

    # ---------------------------------------------------------------- where we are
    b.append("<h2>Where inflation is right now</h2>")
    now = [
        (["All items, twelve months to September 2026", ("num", "3.7%"), pill("ver", "verified"),
          _src_cell(["bls_cpi_home"])], "hi"),
        (["All items less food and energy", ("num", "2.6%"), pill("ver", "verified"),
          _src_cell(["bls_cpi_home"])], None),
        (["Energy", ("num", "20.4%"), pill("ver", "verified"), _src_cell(["bls_cpi_home"])], None),
        (["Gasoline, all types", ("num", "34.2%"), pill("ver", "verified"),
          _src_cell(["bls_cpi_home"])], None),
        (["Shelter", ("num", "3.2%"), pill("ver", "verified"), _src_cell(["bls_cpi_home"])], None),
        (["Owners' equivalent rent of residences", ("num", "3.3%"), pill("ver", "verified"),
          _src_cell(["bls_cpi_home"])], None),
        (["Rent of primary residence", ("num", "2.8%"), pill("ver", "verified"),
          _src_cell(["bls_cpi_home"])], None),
        (["Index level, October 2026", ("num", "337.511"), pill("ver", "verified"),
          _src_cell(["bls_cpi_oct2026"])], None),
        (["October 2026, seasonally adjusted, month on month", ("num", "0.4%"),
          pill("ver", "verified"), _src_cell(["bls_cpi_oct2026"])], None),
        (["Why some twelve-month comparisons cannot be published here",
          "The Bureau did not collect survey data for October 2025 because of a lapse in "
          "appropriations. One month of the official record does not exist, so any twelve-month "
          "change that needs it cannot be computed.", pill("ver", "verified"),
          _src_cell(["bls_cpi_oct2026"])], "hi"),
    ]
    b.append(sh.table(["Measure", ("num", "Value"), "Status", "Source"], now,
                      note="Not seasonally adjusted twelve-month changes unless the row says "
                           "otherwise. Every figure is transcribed from the Bureau's own release."))

    # ------------------------------------------------------------- the whole record
    b.append("<h2>The inflation record, 1914 to 2026</h2>")
    b.append('<p class="small">The complete official record of annual inflation, computed as the '
             'change in the annual average of the Consumer Price Index. This is the distribution the '
             'simulation draws from, and it is published in full so that nothing is hidden behind a '
             'summary statistic.</p>')
    rec = []
    for y, avg, yoy, nmonths in _cpi.annual_table():
        if yoy is None:
            continue
        cls = "hi" if y in (1918, 1921, 1932, 1947, 1974, 1980, 2009, 2022) else None
        note = "" if nmonths == 12 else " (%d of 12 months published)" % nmonths
        rec.append(([str(y), ("num", "%.3f" % avg), ("num", P(yoy, 1)),
                     sh.bar(yoy, -0.11, 0.20), pill("ver", "verified"),
                     _src_cell(["bls_cpi_series"]) + note], cls))
    b.append(sh.table(["Year", ("num", "Annual average index"), ("num", "Inflation"),
                       "Shape", "Status", "Source"], rec,
                      note="1982-84 = 100. October 2025 is absent from the official record, so the "
                           "2025 average is taken over the eleven published months and 2026 over "
                           "ten. Highlighted years are the extremes of the record."))

    # ---------------------------------------------------------------- the stretches
    b.append("<h2>Named stretches in that record</h2>")
    win = []
    for label, a, z in m.REGIME_WINDOWS:
        mu = _cpi.mean_over(a, z)
        tot = _cpi.compound_over(a, z)
        if mu is None:
            win.append(([label, "%d to %d" % (a, z), ("num", "n/a"), ("num", "n/a"),
                         pill("ver", "verified"),
                         _src_cell(["bls_cpi_series"], "no published monthly value inside this "
                                   "window, so no inflation rate can be computed for it")], None))
            continue
        win.append(([label, "%d to %d" % (a, z), ("num", P(mu)), ("num", P(tot)),
                     pill("ver", "verified"), _src_cell(["bls_cpi_series"])], None))
    b.append(sh.table(["Stretch", "Years", ("num", "Mean annual inflation"),
                       ("num", "Compound over the stretch"), "Status", "Source"], win,
                      note="Both columns are computed from the official monthly index. Read them "
                           "together: a stretch can have a modest mean and still compound to a very "
                           "large number."))

    # ------------------------------------------------------------- regime scenarios
    b.append("<h2>What each environment does to the decision</h2>")
    b.append('<p class="small">Each row holds one environment constant for the whole %d years after '
             'the transfer. Nothing in the historical record actually behaves like that; the rows '
             'are stress tests, not scenarios with probabilities. The tax columns show the Property A '
             'bill in the first full year after the transfer.</p>' % _R["years_after"])
    rows = []
    for x in _regimes():
        rg = x["regime"]
        anchored = rg["anchor_years"] is not None
        rows.append(([rg["name"],
                      ("num", P(x["inflation"])), ("num", P(x["price_growth"])),
                      ("num", P(x["portfolio"])),
                      ("num", M(x["occ_gap"])), ("num", M(x["rent_gap"])),
                      ("num", M(x["tax_excluded"])), ("num", M(x["tax_full"])),
                      pill("der", "derived"),
                      _src_cell(["bls_cpi_series"] if anchored else None,
                                None if anchored else
                                "both growth inputs for this environment are assumptions; it is a "
                                "thought experiment, not a measured episode")],
                     "hi" if rg["key"] == "great_inflation" else None))
    b.append(sh.table(["Environment", ("num", "Inflation"), ("num", "House price growth"),
                       ("num", "Portfolio return"),
                       ("num", "Occupy less sell"), ("num", "Let less sell"),
                       ("num", "Year&nbsp;1 tax, exclusion"), ("num", "Year&nbsp;1 tax, full"),
                       "Status", "Source"], rows,
                      note="A positive gap means keeping wins. The inflation column is measured from "
                           "the official record; the two growth columns are nominal rates built as "
                           "inflation plus the assumed real rate for that environment."))

    spread = [x["occ_gap"] for x in _regimes() if x["regime"]["anchor_years"]]
    if spread:
        b.append('<div class="banner warn"><b>The spread is the finding.</b> Across measurable '
                 'environments the occupy-versus-sell gap runs from %s to %s &mdash; a range of '
                 '%s. That is far wider than the difference between any two of the three options '
                 'under the baseline. Which decade the transfer happens to fall in matters more '
                 'than which option you pick, and nobody can choose the decade.</div>'
                 % (M(min(spread)), M(max(spread)), M(max(spread) - min(spread))))

    # ---------------------------------------------------------------- mechanisms
    b.append("<h2>Five mechanisms that only show up in an uneven world</h2>")
    mech = [
        (["Proposition 8 cuts the bill when prices fall",
          "If market value drops below the trended base year value the county assessor enrolls the "
          "lower value, so the tax bill falls with the market. It then rises with the market again "
          "until it meets the trend. A house carried through a slump is cheaper to hold than a "
          "smooth-line model suggests, which is exactly the cushion that mattered in the deflation "
          "row above.", pill("ver", "verified"), _src_cell(["boe_pub29"])], "hi"),
        (["The Proposition 19 allowance moves with house prices, not with inflation",
          "The allowance is indexed to a California house price index, which rose 2.15% in 2024. In "
          "a housing boom the allowance grows quickly, so the protected slice grows quickly too. In "
          "a housing slump the allowance can barely move while the rest of the taxable value "
          "keeps climbing.", pill("ver", "verified"),
          _src_cell(["boe_lta2025_009", "fhfa_hpi"])], "hi"),
        (["The statewide rent cap binds only above 5% inflation",
          "The cap is 5% plus the change in the cost of living, or 10%, whichever is lower. Below 5% "
          "inflation it does not bind at all. In a high-inflation stretch it caps rent increases "
          "below inflation while insurance, maintenance and water all rise with inflation, so the "
          "real return on a letting compresses precisely when the overall price level is moving "
          "fastest.", pill("ver", "verified"), _src_cell(["leginfo_civ1947_12"])], None),
        (["A rental stream is nominal, and so is the tax on it",
          "Rent is taxed as it is received. In a high-inflation stretch with flat real rents, the "
          "nominal rent that clears the thresholds grows and the tax on it grows with it, while the "
          "real value of the depreciation shield stays fixed in nominal terms. The shield is worth "
          "less every year and nothing in the tax code restores it.", pill("ver", "verified"),
          _src_cell(["irs_niit", "irs_tc409"])], None),
        (["An asset held to death is never taxed on its gain",
          "All three options here end with an unsold asset, so no option is charged a terminal "
          "capital gains tax that another avoids. If the asset is still held at death its basis is "
          "stepped up again. That is why the sell-and-reinvest comparison uses an <i>after-tax</i> "
          "portfolio return rather than a gross one, and it is why a high-inflation environment "
          "hurts selling twice: it erodes the real return and it leaves a nominal gain that would be "
          "taxed on the way out.", pill("ver", "verified"),
          _src_cell(["irs_tc409", "irs_p551"])], None),
    ]
    b.append(sh.table(["Mechanism", "Why it only matters when the path is uneven", "Status",
                       "Source"], mech))

    # ------------------------------------------------------------ block resampling
    b.append("<h2>Block resampling: assembling the future out of real five-year stretches</h2>")
    b.append('<p class="small">Independent draws from the historical distribution would jump from 14% '
             'to &minus;10% and back with no memory. Inflation does not behave like that: it '
             'persists. The simulation therefore draws contiguous five-year blocks of real history '
             'and chains them, which preserves the way a bad stretch runs for years before it turns. '
             'Each block also carries one growth regime with it, so a high-inflation block is also a '
             'block in which real returns were poor &mdash; the correlation is the point.</p>')
    occ, rnt = _mc()
    dist = []
    for label, d in (("Occupy less sell", occ), ("Let less sell", rnt)):
        dist.append(([label, ("num", M(d["p05"])), ("num", M(d["p25"])), ("num", M(d["p50"])),
                      ("num", M(d["p75"])), ("num", M(d["p95"])), ("num", M(d["mean"])),
                      ("num", P(d["keep_wins"], 0)), pill("der", "derived"),
                      _src_cell(["bls_cpi_series"], "inflation paths resampled from the official "
                                "record; the two growth inputs are assumptions")], None))
    b.append(sh.table(["Comparison", ("num", "5th"), ("num", "25th"), ("num", "Median"),
                       ("num", "75th"), ("num", "95th"), ("num", "Mean"),
                       ("num", "Keeping wins"), "Status", "Source"], dist,
                      note="%s resampled paths per comparison, fixed seed so the numbers reproduce. "
                           "This is a dispersion study, not a probability forecast: the environments "
                           "are drawn with equal weight, which is a choice and not an estimate of how "
                           "likely each one is." % format(occ["paths"], ",")))

    b.append('<div class="banner warn"><b>The honest read.</b> Across resampled histories the median '
             'favours selling by %s, but keeping wins in about %s of paths and the middle half of '
             'outcomes runs from %s to %s. A decision this close to the line should not be made on a '
             'projection at all. It should be made on the break-even rent, which is observable once '
             'you have a letting appraisal, and on whether you actually want to live in the house, '
             'which is not a financial question.</div>'
             % (M(abs(occ["p50"])), P(occ["keep_wins"], 0), M(occ["p25"]), M(occ["p75"])))
    return "Black swans", "".join(b)


# -------------------------------------------------------------------- 10. process

_STEPS = [
    ("Before the transfer", [
        ("Confirm the property is held in the trust, and that the trust is the kind the exclusion "
         "recognises",
         "Transfers through a trust are eligible, because the trust is looked through to the "
         "present beneficial ownership. But an entity is not: property held by a legal person does "
         "not qualify, so the property must not have been moved into a company or a limited "
         "liability company.",
         ["boe_lta2026_026"]),
        ("Keep it as the settlor's principal residence",
         "The exclusion requires the home to be the principal residence of the transferor. A home "
         "that has become a rental does not qualify. Letting it out before the transfer would end "
         "the exclusion permanently, and nothing restores it.",
         ["boe_prop19", "boe_lta2026_026"]),
        ("Do not transfer it into a legal entity",
         "Moving the property into a company, including a single-member company, would make it "
         "ineligible for the exclusion and would also end the homeowner's exemption.",
         ["boe_lta2026_026"]),
        ("Read the trust instrument with a California estates lawyer",
         "Who the trustee is, who the beneficiaries and heirs are, and what the trustee may do "
         "determines everything that follows. This desk has not seen the instrument and cannot tell "
         "you what yours says.",
         None),
    ]),
    ("In the first sixty days", [
        ("The trustee serves the statutory notification",
         "Within 60 days of the death the trustee must serve a notification on every beneficiary of "
         "the trust and every heir of the deceased settlor, in the manner provided by Probate Code "
         "section 1215, to the last known address.",
         ["leginfo_prob16061_7"]),
        ("Obtain a date-of-death valuation",
         "The value at the date of death sets the income tax basis of what is inherited, and it "
         "sets the new assessed value if the exclusion turns out not to apply. A valuation obtained "
         "later is harder to defend than one obtained at the time.",
         ["irs_tc409", "irs_p551"]),
    ]),
    ("Property tax filings", [
        ("Notify the county assessor of the change in ownership",
         "A change in ownership statement is required, and the assessor then decides whether to "
         "reassess and to what value.",
         ["boe_pub29"]),
        ("Move in within one year of the transfer",
         "The law requires the transferee to occupy the family home within one year of the transfer "
         "for the exclusion to apply as of the date of transfer. This is the single most valuable "
         "date on this desk.",
         ["boe_lta2026_026"]),
        ("File the homeowner's or disabled veterans' exemption within one year",
         "Filed on the form the Board prescribes with the county assessor. The exclusion is not "
         "available without it, and if it is filed after the year has passed the exclusion cannot "
         "be applied retrospectively once the property has been sold.",
         ["boe_prop19", "boe_lta2026_026"]),
        ("File the exclusion claim within three years",
         "The statute ends the window at whichever comes first of three years, a transfer to a "
         "third party, and the date an eligible transferee no longer occupies the residence. A "
         "claim is also treated as timely if it is filed within six months of the mailing of a "
         "supplemental or escape assessment notice.",
         ["leginfo_rtc63_2"]),
        ("Answer any notice of potential eligibility within 45 days",
         "If the assessor writes to say you may be eligible, a certified claim is due within 45 "
         "days. The assessor may send a second notice giving 60 days. Miss both and a late claim "
         "can carry a one-time processing fee of the lesser of the assessor's actual cost and "
         "$175.",
         ["leginfo_rtc63_2"]),
        ("Note that the claim itself is confidential",
         "A claim filed under this section is not a public document and is not open to public "
         "inspection. Only the parties, their legal representatives, the trustees and the "
         "executor or administrator may see it.",
         ["leginfo_rtc63_2"]),
        ("Expect a supplemental or escape assessment",
         "After a change in ownership the assessor may issue a supplemental bill for the part of "
         "the year after the transfer, or an escape assessment if the value is determined late. "
         "Budget for a one-off bill in the first year.",
         ["sftreasurer_secured"]),
    ]),
    ("Federal filings", [
        ("Work out whether an estate tax return is required",
         "A return is required if the gross estate, increased by adjusted taxable gifts and with "
         "the specific gifts listed in the statute, exceeds the threshold for the year of death: "
         "$15,000,000 for 2026 and $15,480,000 for 2027. California imposes no estate tax at all, "
         "so this is the only death tax to consider.",
         ["irs_estate_tax", "irs_ir2026_133", "leginfo_rtc13301"]),
        ("File within nine months, or extend",
         "The return is due nine months after the date of death. An automatic six-month extension "
         "of time to file is available on Form 4768 filed by the due date.",
         ["irs_estate_faq"]),
        ("File even if no tax is due, if portability is wanted",
         "A return must be filed to elect portability of a deceased spouse's unused exclusion, "
         "regardless of the size of the estate. Where no filing requirement existed, a simplified "
         "late election is available under the revenue procedure the Service issued for that "
         "purpose.",
         ["irs_estate_faq"]),
    ]),
    ("Afterwards", [
        ("Tell the insurer",
         "A change of ownership is a material change. An owner-occupier policy will not cover a let "
         "property, and a landlord policy will not cover an owner-occupier's contents. Sort this "
         "before the transfer completes, not after a claim.",
         ["cdi_residential"]),
        ("Transfer the utility accounts and check the rooftop solar tariff",
         "The export tariff was enrolled by the previous account holder and may need to be "
         "re-enrolled under yours. This desk does not know which utility serves Property A, or what "
         "tariff the system is on.",
         None),
        ("Diarise the two annual tax dates",
         "Secured property tax installments are delinquent after 10 December and 10 April, and the "
         "penalty is 10% of the installment. Two dates a year, every year.",
         ["sftreasurer_secured"]),
        ("Keep the assessor's notices and the filed claims",
         "If the exclusion is ever challenged, the notices and the filed claims are the evidence. "
         "Keep them with the trust documents.",
         ["boe_lta2026_026"]),
    ]),
]

_STEP_NOTES = {
    "Read the trust instrument with a California estates lawyer":
        "no official source publishes a step like this; it is legal advice, and this desk has not "
        "seen the instrument",
    "Transfer the utility accounts and check the rooftop solar tariff":
        "the utility that serves Property A is not named on this site and no tariff was retrieved, "
        "so no official document can be linked",
}


def page_process():
    b = []
    b.append('<p class="lead">What actually happens when a property held in a family trust passes, '
             'in the order it happens, with the deadline for each step and the document that '
             'imposes it.</p>')
    b.append('<div class="banner warn"><b>Two dates decide the tax outcome.</b> You must <b>occupy '
             'the home within one year</b> of the transfer and <b>file the homeowner\'s exemption '
             'within one year</b>. Miss either one and the Proposition 19 exclusion is lost, and the '
             'assessed value resets to full market value &mdash; on the projections used here that '
             'is the difference between a %s bill and a %s bill in the first full year, or %s a year, '
             'and it then compounds for as long as you hold the property.</div>'
             % (M(_TAX_EXCL), M(_TAX_FULL), M(_EXCL_SAVING)))
    n = 0
    for group, items in _STEPS:
        b.append("<h2>%s</h2>" % group)
        rows = []
        for what, why, sids in items:
            n += 1
            rows.append(([str(n), what, why,
                          pill("ver", "verified") if sids else pill("asm", "action"),
                          _src_cell(sids, _STEP_NOTES.get(what))],
                         "hi" if n in (5, 6) else None))
        b.append(sh.table(["#", "Step", "Why it matters, and the deadline", "Status", "Source"],
                          rows))
    b.append('<div class="banner">Nothing on this page is legal advice. The trust instrument, the '
             'number of beneficiaries and the exact terms of the transfer can each change which of '
             'these steps applies to you. Take the instrument to a California estates lawyer before '
             'the transfer, not after it.</div>')
    return "The transfer, step by step", "".join(b)


# ----------------------------------------------------------------- 11. questions

def _questions():
    return [
        ("What rent could Property A actually be let for?",
         "The keep-or-sell answer for the letting option, and the size of the housing benefit if you "
         "live in it",
         "Not answered",
         "Three written letting appraisals from agents who manage lettings in the area, refreshed "
         "every two years until the transfer",
         ["boe_prop19"]),
        ("Do you want to live in Property A?",
         "Whether the Proposition 19 exclusion is available at all. On these projections it is worth "
         "about %s in the first full year after the transfer, and the advantage compounds" % M(
             _EXCL_SAVING),
         "Not answered",
         "A decision, not a document. Nothing else on this desk moves as much money as this one.",
         ["boe_prop19", "boe_lta2026_026"]),
        ("What does the trust actually say?",
         "Who the trustee is, who must be notified within 60 days, whether the property can be sold, "
         "and whether you are permitted to occupy it",
         "Not answered",
         "The trust instrument, read with a California estates lawyer",
         ["leginfo_prob16061_7"]),
        ("Will the settlor still be living there at the transfer?",
         "The exclusion requires the home to be the transferor's principal residence. A home that "
         "has become a rental does not qualify",
         "Not answered",
         "Confirm now and keep evidence of residence, so the position can be shown later",
         ["boe_prop19", "boe_lta2026_026"]),
        ("How many beneficiaries and heirs are there?",
         "The trustee must notify every one of them within 60 days, and any eligible transferee can "
         "occupy the home to preserve the exclusion",
         "Not answered",
         "The trust instrument, and the trustee's own list",
         ["leginfo_prob16061_7"]),
        ("What will the insurance actually cost?",
         "Every running cost projection on this desk, for both properties",
         "Owner estimate only, %s a year" % M(m.OWNER["a_insurance"]),
         "Two written quotations per property. For Property B ask for a landlord or dwelling fire "
         "form, not an owner-occupier form",
         ["cdi_residential"]),
        ("What do you actually spend on maintenance?",
         "The second largest running cost after the tax bill, and there is no figure for it at all",
         "No figure supplied",
         "Five years of the owner's own records, reduced to a percentage of value",
         None),
        ("Which utility serves Property A, and on what solar tariff?",
         "Whether the power credit survives the transfer, and whether re-enrolment changes it",
         "Not stated",
         "The interconnection agreement, and the utility's current export tariff",
         None),
        ("Which utility supplies water to Property A?",
         "The water cost projection on the running costs page, and how fast it rises",
         "Not stated",
         "The water bill itself names the utility; then read its published rate schedule",
         None),
        ("What is the exact property tax rate printed on Property A's bill?",
         "Every tax projection on this desk. The rate used here is derived from the owner's own bill "
         "divided by the owner's own assessed value",
         "Derived, %s" % P(_RATE_A),
         "Read the rate area and the itemised charges off the current bill",
         ["boe_pub29"]),
        ("What makes up the unexplained %s on Property B's bill?" % M(_B_RESIDUAL),
         "About %s of that bill is not explained by the official secured rate applied to the "
         "assessed value" % P(_B_RESIDUAL / m.OWNER["b_bill_2025"]),
         "Flagged",
         "Read the itemised charges on the bill; parcel taxes and bond levies are not ad valorem",
         ["sftreasurer_secured"]),
        ("Are the three units at Property B comparable in rent?",
         "How much income you actually free by moving out, which is a real benefit of occupying "
         "Property A. This desk assumes one unit is worth %s a year" % M(_UNIT_B),
         "Assumed comparable",
         "A letting appraisal for the unit that is currently not let",
         None),
        ("What year was Property B built, and was the tenant given written notice?",
         "Whether the statewide rent cap and the just-cause rules apply to it at all. The cap has "
         "exemptions that turn on the year built and on notice given to the tenant",
         "Not supplied",
         "The building record or the assessor's property characteristics, plus the tenancy papers",
         ["leginfo_civ1947_12"]),
        ("What is the gross estate likely to be, including the cash?",
         "Whether a federal estate tax return will be required, and whether portability should be "
         "elected",
         "Not supplied",
         "An estimate kept and refreshed, then professional advice before the transfer",
         ["irs_estate_tax", "irs_ir2026_133"]),
        ("Is portability available, and was it elected on any earlier death?",
         "It can double the exclusion, but only where an estate tax return was filed in time",
         "Not answered",
         "Look for the earlier estate tax return, or establish that none was filed",
         ["irs_estate_faq"]),
        ("Will there be a mortgage on Property A at the transfer?",
         "The carrying cost, and whether the trust and the lender permit the debt to continue",
         "Not answered",
         "The trust instrument and the lender's file",
         None),
        ("What is the land share of Property A's value?",
         "The depreciation shield if you let it. Only the improvement share is depreciable, and "
         "this desk assumes land is 20% of value",
         "Assumed 20%",
         "A county assessor's property characteristic record, or an appraisal",
         None),
        ("How long do you expect to hold after the transfer?",
         "The horizon is the second largest driver after the growth rates. The whole case for "
         "selling rests on compounding, and compounding needs time",
         "Assumed to 2076",
         "A decision, not a document",
         None),
    ]


def page_questions():
    b = []
    b.append('<p class="lead">Every question that has to be answered before a decision is '
             'reasonable, what it blocks, and the concrete way to answer it. Sorted by how much '
             'money it moves.</p>')
    rows = []
    for i, (q, blocks, status, how, sids) in enumerate(_questions(), 1):
        if status.startswith("Not") or status == "Flagged":
            sp = pill("unv", status)
        elif status.startswith(("Owner", "Assumed", "Derived")):
            sp = pill("own", status)
        else:
            sp = pill("ver", status)
        rows.append(([str(i), q, blocks, sp, how,
                      _src_cell(sids, None if sids else
                                "no official source exists for this item; the answer has to come "
                                "from the owner's own records or from a professional")],
                     "hi" if i <= 3 else None))
    b.append(sh.table(["#", "Question", "What it blocks", "Status", "How to answer it", "Source"],
                      rows,
                      note="The first three questions move the most money. Everything below them is "
                           "second order by comparison, and two of the three are not questions of "
                           "fact at all."))

    b.append("<h2>Questions this desk cannot answer, and says so</h2>")
    cant = [
        (["When the transfer will happen",
          "It depends on a death. The desk models 2040, 2045 and 2050 and shows all three side by "
          "side, because a single date would be a guess dressed as a fact.",
          pill("unv", "unknown"),
          _src_cell(None, "not knowable; the window is the owner's own estimate")], "hi"),
        (["What house prices will do over the next fifty years",
          "No official forecast exists. The desk publishes the break-even growth rate instead, so "
          "that the answer does not depend on a forecast you cannot verify.",
          pill("unv", "unknown"),
          _src_cell(["fhfa_hpi"], "the official index is linked, but no forecast is quoted from it")],
         "hi"),
        (["What the reinvestment portfolio will return",
          "Same. The desk publishes the break-even return, which is the number you actually need.",
          pill("unv", "unknown"),
          _src_cell(None, "no official source publishes forward returns; the break-even return is "
                    "published so this does not have to be assumed")], None),
        (["Whether Congress will change the step-up in basis at death",
          "Proposals recur in commentary. Nothing is in force. This desk could not find such a "
          "change in the Federal Register, in the Internal Revenue Bulletin or on the Treasury's "
          "site, so no value is asserted for it anywhere.",
          pill("unv", "unverified"),
          _src_cell(["irs_tc409"], "the rule currently in force is linked; no change was found on "
                    "any official source")], None),
        (["Whether a planned short occupancy satisfies the exclusion",
          "The guidance is clear that the exclusion is removed when the home stops being the "
          "transferee's principal residence, and that the new base year value is then enrolled from "
          "the transfer. It does not address a plan to occupy for a limited period. That is a legal "
          "question about facts this desk does not have.",
          pill("unv", "unverified"),
          _src_cell(["boe_lta2026_026"], "the guidance is linked; it does not decide this fact "
                    "pattern")], None),
        (["What a local rent ordinance might require for Property B",
          "A city can be stricter than the statewide cap. This desk names no city, so no local "
          "ordinance was retrieved and none is described.",
          pill("unv", "unverified"),
          _src_cell(["leginfo_civ1947_12"], "the statewide rule is linked; local rules were not "
                    "retrieved")], None),
    ]
    b.append(sh.table(["Question", "Why it is not answered here", "Status", "Source"], cant))
    return "Questions and gaps", "".join(b)


# --------------------------------------------------------------- 12. suggestions

_SUGGESTIONS = [
    ("Get three written letting appraisals for Property A, now and every two years",
     "Decision",
     "Rent is the single largest unknown on this desk and it is the input the break-even is built "
     "to be compared against. Three appraisals also give you a range rather than a point, which is "
     "what you need when the answer is close to the line.",
     "Low: a few hours every two years",
     "None. It only produces information.",
     "Do this first"),
    ("Get two insurance quotations per property, on the correct policy form",
     "Cost",
     "Both insurance figures here are owner estimates. Property B needs a landlord or dwelling fire "
     "form rather than an owner-occupier form, and the two are priced differently.",
     "Low",
     "None",
     "Do this first"),
    ("Pull five years of maintenance and repair records for both properties",
     "Cost",
     "Maintenance is the second largest running cost and there is no figure for it at all. Five "
     "years of what you actually spent beats any percentage rule of thumb, including the one this "
     "desk falls back on.",
     "Medium: a few hours of paperwork",
     "None",
     "Do this first"),
    ("Confirm the trust instrument, and take it to a California estates lawyer",
     "Decision",
     "Whether you may occupy the property, who must be notified within 60 days, and whether the "
     "property can be sold at all each come from the instrument. This desk has never seen it.",
     "Medium: a paid consultation",
     "None, but act before the transfer rather than after it",
     "Do this first"),
    ("Keep Property A as the settlor's principal residence until the transfer",
     "Tax",
     "The exclusion requires the home to be the principal residence of the transferor. Letting it "
     "out before the transfer would end the exclusion permanently, and nothing restores it "
     "afterwards.",
     "None, if you were not planning to let it",
     "The rent you forgo in the meantime",
     "High value"),
    ("Do not move Property A into a company or a limited liability company",
     "Tax",
     "Property held by a legal entity is not eligible for the exclusion, and moving it into an "
     "entity after the transfer removes an exclusion that has already been granted. This is a "
     "warning about a step not to take rather than a change to make.",
     "None",
     "None; it forecloses an option rather than taking one",
     "High value"),
    ("Plan to move in within a year, and file the homeowner's exemption within the year",
     "Tax",
     "Both are statutory conditions. Missing either costs about %s a year on these projections, and "
     "the loss compounds for as long as the property is held." % M(_EXCL_SAVING),
     "High: it changes where you live",
     "You give up the flexibility to let the property instead",
     "High value"),
    ("Let the unit at Property B that is currently not let",
     "Income",
     "It produces income today with no effect on any of the three options, unless the unit is being "
     "kept empty for a reason this desk does not know about.",
     "Low",
     "Loss of the use of the unit; possible local rules on the dwelling",
     "Worth testing"),
    ("Check whether the statewide rent cap, or a local ordinance, applies to Property B",
     "Compliance",
     "The statewide cap is 5% plus the change in the cost of living, or 10%, whichever is lower, "
     "and it has exemptions that turn on the year the building was built and on notice given to "
     "the tenant.",
     "Low",
     "None",
     "Worth testing"),
    ("Confirm the rooftop solar tariff on Property A, and when the enrolment ends",
     "Cost",
     "The power credit is assumed to continue unchanged. If the tariff ends or is replaced, the "
     "running cost rises by the whole of the credit and a little more.",
     "Low",
     "None",
     "Worth testing"),
    ("Ask the county assessor for a written projection of the post-transfer assessed value",
     "Tax",
     "An assessor can tell you what the new taxable value would be. That converts the largest "
     "single projected number on this desk from a projection into a fact, and it costs a phone "
     "call or a letter.",
     "Low",
     "None",
     "Recommended"),
    ("Read the rate area and the itemised charges off Property A's current tax bill",
     "Tax",
     "The rate used here is derived from the owner's own records. The bill itself itemises the rate "
     "area, the voter-approved debt and any parcel charges, which would replace three assumptions "
     "with three facts.",
     "Low",
     "None",
     "Recommended"),
    ("Re-run this model once the five missing facts are known",
     "Process",
     "The break-evens are stable and will not move much. The headline gap will. Re-running with a "
     "real rent, a real insurance quote and a real maintenance figure is the difference between a "
     "projection and a plan.",
     "Low",
     "None",
     "Recommended"),
    ("Replace the assumed per-unit rent at Property B with a real figure",
     "Model",
     "The model assumes the three units are comparable, so the unit you free by moving out is worth "
     "the same as the unit you live in. A letting appraisal for the empty unit would replace that "
     "assumption.",
     "Low",
     "None",
     "Model improvement"),
    ("Decide the holding horizon explicitly rather than accepting 2076",
     "Model",
     "Fifty years is a modelling convenience, not a plan. If you expect to sell or move within "
     "fifteen years of the transfer the answer changes materially, because the compounding gap has "
     "less time to work.",
     "Low",
     "None",
     "Model improvement"),
    ("Record an accept, modify or reject decision against every row on this page",
     "Process",
     "Nothing here has been implemented. The point of the page is that changes are reviewed before "
     "they are made, which only works if each one is actually marked off.",
     "Low",
     "None",
     "Process"),
]

_PRIORITY_PILL = {
    "Do this first": "unv",
    "High value": "ver",
    "Recommended": "der",
    "Worth testing": "asm",
    "Model improvement": "own",
    "Process": "own",
}


def page_suggestions():
    b = []
    b.append('<p class="lead">Suggestions only. <b>Nothing on this page has been implemented.</b> '
             'Each row is a proposal for you to accept, modify or reject before anything changes. '
             'The status column is empty of any decision because none has been taken.</p>')
    b.append('<div class="banner warn"><b>Review before implementing.</b> These are proposals '
             'produced by the analysis, not instructions. Several of them &mdash; moving in, moving '
             'the property into a company, letting the empty unit &mdash; have consequences that '
             'depend on facts this desk does not have. Read the reason, then decide.</div>')
    rows = []
    for i, (what, kind, why, effort, risk, priority) in enumerate(_SUGGESTIONS, 1):
        rows.append((["S%02d" % i, what, kind, why, effort, risk,
                      pill(_PRIORITY_PILL.get(priority, "own"), priority),
                      pill("new", "PROPOSED"),
                      _src_cell(None, "a proposal; no official source applies to a suggestion, and "
                                "none is claimed")],
                     "hi" if priority in ("Do this first", "High value") else None))
    b.append(sh.table(["ID", "Suggestion", "Type", "Why it is proposed", "Effort", "Risk or cost",
                       "Priority", "Status", "Source"], rows,
                      note="Priority is assigned by how much of the decision it unblocks or how much "
                           "money it moves, not by how easy it is. 'Do this first' means the "
                           "analysis cannot be trusted without it."))

    b.append("<h2>Suggestions about this site itself</h2>")
    site = [
        (["T01", "Publish a county-by-county rate table instead of a derived effective rate",
          "Would replace the weakest input on the desk with a published one. Deliberately not done: "
          "a named county would identify the area.", pill("new", "PROPOSED"),
          _src_cell(["boe_pub29"], "the publication explains the 1% ceiling and the 2% factor, but "
                    "no county rate is quoted here")], None),
        (["T02", "Retrieve the official ZIP-level insurance data and publish a range",
          "Would replace both insurance estimates. The Department publishes the figures only as "
          "spreadsheet files, which this desk did not retrieve; the ZIP-level file would also "
          "identify the area, though a statewide figure would not.",
          pill("new", "PROPOSED"), _src_cell(["cdi_residential"])], None),
        (["T03", "Add the county assessor's own projection once it has been requested",
          "Turns the largest single projected number on the desk into a fact.",
          pill("new", "PROPOSED"), _src_cell(["boe_lta2026_026"])], None),
        (["T04", "Keep every page free of script, external asset, form and tracker",
          "Already the case. A page that cannot run code and cannot call out cannot leak what it "
          "displays, which is a stronger guarantee than any redaction.", pill("new", "PROPOSED"),
          _src_cell(None, "a design rule of this desk, enforced by its verifier rather than sourced "
                    "from a document")], None),
        (["T05", "Re-verify every statutory figure each November",
          "The federal inflation adjustments are published in the autumn and the Proposition 19 "
          "allowance moves every second February. Both change numbers on this desk.",
          pill("new", "PROPOSED"), _src_cell(["irs_ir2026_133", "boe_lta2025_009"])], None),
        (["T06", "Consider whether the rounded tax history should be published at all",
          "Rounding makes a figure hard to match to a record, but a multi-year series of assessed "
          "values is close to a fingerprint when combined with a county. This desk names no county. "
          "The trade-off is the owner's to make.", pill("new", "PROPOSED"),
          _src_cell(None, "a judgement about this site, not a sourced fact")], None),
    ]
    b.append(sh.table(["ID", "Change", "Why", "Status", "Source"], site))
    return "Suggestions", "".join(b)


# ----------------------------------------------------------------- 13. law watch

def page_law_watch():
    b = []
    b.append('<p class="lead">What is in force, what moved at the November 2026 election, and what '
             'is under discussion &mdash; with the distinction drawn sharply, because most commentary '
             'on these subjects does not draw it at all.</p>')

    b.append("<h2>In force now</h2>")
    now = [
        (["Federal estate tax basic exclusion, 2026", ("num", "$15,000,000"),
          "In force. Public Law 119-21, signed 4 July 2025, amended section 2010(c)(3).",
          pill("ver", "verified"), _src_cell(["irs_estate_tax", "irs_estate_faq"])], "hi"),
        (["Federal estate tax basic exclusion, 2027", ("num", "$15,480,000"),
          "Announced on 5 November 2026; applies to the estates of people who die during 2027.",
          pill("ver", "verified"), _src_cell(["irs_ir2026_133"])], "hi"),
        (["Annual gift exclusion, 2026 and 2027", ("num", "$19,000 then $20,000"),
          "In force. The 2027 figure was announced with the 2027 inflation adjustments.",
          pill("ver", "verified"), _src_cell(["irs_ir2026_133"])], None),
        (["Federal estate tax rate above the exclusion", ("num", "40%"),
          "Applied through the rate schedule in section 2001. The exclusion is what matters here; "
          "the rate is the fallback.",
          pill("ver", "verified"), _src_cell(["irs_estate_tax"])], None),
        (["California estate, inheritance and gift tax", "Prohibited",
          "Neither the state nor any of its political subdivisions may impose any gift, "
          "inheritance, succession, legacy, income or estate tax on a transfer by reason of death.",
          pill("ver", "verified"), _src_cell(["leginfo_rtc13301"])], "hi"),
        (["California top marginal income tax rate", ("num", "13.3%"),
          "12.3% on the Franchise Tax Board rate schedules, plus the 1% surcharge imposed by statute "
          "on taxable income over $1,000,000. The surcharge does not appear on the schedules "
          "themselves, which is why it has been flagged elsewhere in this repository.",
          pill("ver", "verified"), _src_cell(["ftb_2025_rates", "leginfo_rtc17043"])], None),
        (["Proposition 13",
          "1% ceiling plus voter-approved debt; base year value capped at 2% a year",
          "In force. The lien date is 1 January and the 1% levy applies to the base year value as "
          "adjusted.", pill("ver", "verified"), _src_cell(["boe_pub29"])], None),
        (["Proposition 19 intergenerational exclusion",
          "Factored base year value plus $1,044,586, in force to 15 February 2027",
          "The next adjustment is February 2027 and every second February after that. The prior "
          "amount was $1,022,600.", pill("ver", "verified"), _src_cell(["boe_lta2025_009"])], None),
        (["Statewide rent cap",
          "5% plus the change in the cost of living, or 10%, whichever is lower",
          "Civil Code section 1947.12, no more than two increases in any twelve months, with the "
          "exemptions listed in subdivision (d).", pill("ver", "verified"),
          _src_cell(["leginfo_civ1947_12"])], None),
        (["Net investment income tax", ("num", "3.8%"),
          "Applies to rents and to gains on investment real estate. The thresholds are set by "
          "statute and are not indexed for inflation, so more taxpayers fall inside them every "
          "year.", pill("ver", "verified"), _src_cell(["irs_niit"])], None),
        (["Trustee notification on irrevocability", "60 days",
          "The trustee must notify each beneficiary and each heir within 60 days of the trust "
          "becoming irrevocable.", pill("ver", "verified"),
          _src_cell(["leginfo_prob16061_7"])], None),
    ]
    b.append(sh.table(["Rule", "Amount or effect", "Detail", "Status", "Source"], now))

    b.append("<h2>The 3 November 2026 California statewide ballot</h2>")
    b.append('<div class="banner warn"><b>These results are unofficial.</b> The Secretary of State '
             'states that county elections officials must report their final official results by '
             '4 December 2026 and that the results will be certified on 11 December 2026. Nothing '
             'below should be acted on as settled until certification.</div>')
    el = [
        (["Proposition 3",
          "Provides Permanent Funding for Schools and Health Care by Extending Existing Tax on High "
          "Incomes",
          ("num", "Yes 60.7% / No 39.3%"),
          "Makes permanent the existing voter-approved rates for individuals earning over $371,000 "
          "instead of letting them expire in 2031. Fiscal impact given by the state's own analyst: "
          "maintains between $5 billion and $15 billion of annual state income tax revenue.",
          pill("ver", "verified"), _src_cell(["sos_prop3", "sos_results_bm"])], "hi"),
        (["Proposition 40", "Imposes One-Time Tax on Certain Taxpayers",
          ("num", "Yes 47.7% / No 52.3%"),
          "A 5% one-time tax on certain taxpayers with assets over $1 billion, with revenue going "
          "primarily to health care. The threshold is far above anything on this desk either way.",
          pill("ver", "verified"), _src_cell(["sos_prop40", "sos_results_bm"])], None),
        (["Proposition 42",
          "Prohibits New State Personal Property Taxes and Certain Retroactive State Taxes",
          ("num", "Yes 51.3% / No 48.7%"),
          "Official title as listed by the Secretary of State.",
          pill("ver", "verified"), _src_cell(["sos_qualified", "sos_results_bm"])], None),
        (["Proposition 43",
          "Limits Voters' Ability to Raise Revenues for Local Government Services",
          ("num", "Yes 42.4% / No 57.6%"),
          "Official title as listed by the Secretary of State.",
          pill("ver", "verified"), _src_cell(["sos_qualified", "sos_results_bm"])], None),
        (["A split roll, or any change to Proposition 13", "No such measure qualified",
          "Checked against the Secretary of State's own list of the measures on the ballot. A "
          "proposed constitutional amendment that would have made it easier to raise local taxes "
          "was removed from the ballot on 25 June 2026.",
          pill("ver", "verified"), _src_cell(["sos_qualified"])], "hi"),
        (["Certification dates",
          "4 December 2026 for county returns, 11 December 2026 for certification", "",
          "Published on the results site itself.", pill("ver", "verified"),
          _src_cell(["sos_results_home"])], None),
    ]
    b.append(sh.table(["Measure", "Official title or subject", ("num", "Unofficial result"),
                       "What it does", "Status", "Source"], el,
                      note="Only measures that bear on property tax, income tax or wealth tax are "
                           "listed. The other measures on the ballot were read and set aside as "
                           "irrelevant to this decision."))

    b.append("<h2>Under discussion, and what could actually be confirmed</h2>")
    disc = [
        (["Taxing unrealised gains at death, or limiting the step-up in basis", "",
          "Discussed in commentary and in successive budget proposals. This desk could not find such "
          "a change in the Federal Register, in the Internal Revenue Bulletin, or on the Treasury's "
          "site. No value is asserted and no probability is implied.",
          pill("unv", "unverified"),
          _src_cell(["irs_tc409"], "the rule currently in force is linked; no change was found on "
                    "any official source")], "hi"),
        (["Indexation of the federal basic exclusion after 2027", "",
          "The 2026 and 2027 amounts are official. The rate of indexation after 2027 is not a "
          "published figure, so this desk indexes at an assumed 2.5% a year and labels every "
          "projection beyond 2027 as a projection.",
          pill("asm", "assumption"), _src_cell(["irs_ir2026_133"])], None),
        (["A further adjustment of the Proposition 19 allowance", "",
          "The next adjustment is February 2027 and every second February afterwards. The amount is "
          "not knowable in advance, because it tracks a house price index that has not yet been "
          "measured for that period.",
          pill("ver", "verified"), _src_cell(["boe_lta2025_009", "fhfa_hpi"])], None),
        (["Changes to the statewide rent cap", "",
          "The Legislative Analyst's Office must report to the Legislature on the effectiveness of "
          "the cap by 1 January 2030. That is a reporting duty, not a change in the law, and the "
          "cap has no sunset provision.",
          pill("ver", "verified"), _src_cell(["leginfo_civ1947_12"])], None),
        (["A state wealth tax", "",
          "Proposition 40 would have imposed a 5% one-time tax on assets over $1 billion. The "
          "unofficial result is that it failed. The threshold is far above anything on this desk "
          "either way.", pill("ver", "verified"),
          _src_cell(["sos_prop40", "sos_results_bm"])], None),
    ]
    b.append(sh.table(["Proposal", ("num", "Amount"), "What could be confirmed from official sources",
                       "Status", "Source"], disc,
                      note="An empty amount cell is deliberate. This desk does not repeat a number "
                           "it could not find on an official source, and it does not dress an "
                           "assumption up as a finding."))
    return "Law watch", "".join(b)


# --------------------------------------------------------------- 14. repo review

def page_repo_review():
    b = []
    b.append('<p class="lead">What is in this repository, what is published, and the irregularities '
             'found while reading it. Written so that you can check any of it yourself.</p>')
    rows = [
        (["Published sites in this repository",
          "Several independent decision desks, each with its own generator and its own verifier, "
          "plus a curated privacy-first dashboard and an independent verification register",
          "Each desk keeps its own source register and its own flagged page. The figures have not "
          "been reconciled between them, so two desks can publish different headline numbers.",
          pill("ver", "verified"),
          _src_cell(None, "observed by reading the repository; not a fact about the law and no "
                    "official source applies")], None),
        (["Coordination board",
          "A shared task board at the repository root records who claimed what, with a session "
          "identifier and a file scope",
          "Claims also carry a lapse rule, so an abandoned claim does not block a directory "
          "forever.", pill("ver", "verified"),
          _src_cell(None, "observed by reading the repository")], None),
        (["Publication boundary",
          "A verifier fails the build if a top-level directory is neither approved for publication "
          "nor explicitly excluded",
          "The rule is fail-closed: a new directory that nobody listed will break the build rather "
          "than quietly publish. This desk is added to the approved list at integration time.",
          pill("ver", "verified"),
          _src_cell(None, "observed by reading the repository's verification script")], None),
        (["Generated pages are committed and re-checked",
          "Each desk's HTML is committed alongside its generator, and the build is re-run and "
          "re-verified in continuous integration, so a stale checked-in page fails the check",
          "This desk follows the same pattern: the pages in this directory are generated, and the "
          "generator lives beside them but is not served.",
          pill("ver", "verified"),
          _src_cell(None, "observed by reading the repository")], None),
    ]
    b.append(sh.table(["Area", "What is there", "Note", "Status", "Source"], rows))

    b.append("<h2>Irregularities found in this repository</h2>")
    b.append('<p class="small">Nothing below was changed by this session: each item belongs to files '
             'this desk does not own. They are logged so that you can decide what to do about '
             'them.</p>')
    irr = [
        (["R01", "Earlier unrounded figures remain in public git history",
          "Several earlier generations of this project published figures that were not rounded to "
          "$10. No later commit can remove them from the history of a public repository, and "
          "rewriting shared history has its own costs.",
          "Read the history and decide whether the repository should be private, or whether the "
          "history should be rewritten and everyone re-cloned.",
          pill("unv", "unverified"),
          _src_cell(None, "observed by reading the repository; no official source applies")], "hi"),
        (["R02", "Published desks disagree with each other",
          "Independent desks in the same repository publish different headline figures, because "
          "they chose different assumptions and none of them reconciled against the others.",
          "Pick one desk as the reference, or add a page that reconciles them and explains why they "
          "differ.", pill("der", "derived"),
          _src_cell(None, "observed by reading the repository")], None),
        (["R03", "An earlier desk overstated the Proposition 19 saving",
          "One earlier desk treated the exclusion as protecting the whole gap between assessed and "
          "market value. It protects only the allowance: once market value exceeds the cap, the new "
          "taxable value is the market value less the allowance, and everything above the cap is "
          "taxed. That desk is excluded from publication.",
          "Confirm the correction against the guidance, then decide whether to reinstate or retire "
          "that desk.", pill("ver", "verified"), _src_cell(["boe_lta2026_026"])], "hi"),
        (["R04", "An estate tax closing letter fee was reported inconsistently",
          "An earlier page showed a fee that did not match the published figure. The official user "
          "fee for the letter is $67, effective 28 October 2021.",
          "Correct the page, or leave it and rely on the flagged entry to warn a reader.",
          pill("ver", "verified"), _src_cell(["irs_estate_faq"])], None),
        (["R05", "A 1% California surcharge was reported as unconfirmed",
          "An earlier desk flagged that the 1% surcharge over $1,000,000 did not appear on the rate "
          "schedules. It does not: it is imposed by statute, not by the schedules, so looking for "
          "it there was always going to fail. The 13.3% top rate is confirmed from two official "
          "sources.",
          "Close that flag. This desk treats the surcharge as resolved and uses 13.3%.",
          pill("ver", "verified"), _src_cell(["leginfo_rtc17043", "ftb_2025_rates"])], "hi"),
        (["R06", "A Proposition 3 income threshold was reported from commentary",
          "An earlier desk recorded the Proposition 3 threshold as $361,000 and labelled the source "
          "secondary. The Secretary of State's own voter guide says over $371,000.",
          "Correct the figure on that desk and relabel the source as official.",
          pill("ver", "verified"), _src_cell(["sos_prop3"])], None),
        (["R07", "Owner tax histories have been published by earlier desks",
          "Rounding to $10 makes a single figure hard to match to a record, but a thirteen-year "
          "series of assessed values is close to a fingerprint when it is combined with a county. "
          "This desk names no county and no city.",
          "Decide whether any tax history should be published at all, on this desk or on the "
          "others.", pill("unv", "unverified"),
          _src_cell(None, "a judgement about the repository, not a sourced fact")], None),
        (["R08", "Two source documents were linked but never opened",
          "A revenue procedure and a Board of Equalization letter to assessors are cited in earlier "
          "registers but were never retrieved, so nothing on those desks rests on them. This desk "
          "records its own unopened links on the sources page rather than implying they were read.",
          "Retrieve them, or drop the citations.", pill("unv", "unverified"),
          _src_cell(["irs_rp2026_35", "boe_lta2021_054"])], None),
    ]
    b.append(sh.table(["ID", "Irregularity", "Detail", "Owner action", "Status", "Source"], irr))
    return "Repository review", "".join(b)


# ------------------------------------------------------------------- 15. sources

def page_sources():
    b = []
    b.append('<p class="lead">Every official document read while building this desk, with what it '
             'evidences and what was checked on it. A source that is linked but was not opened is '
             'marked as such, and it carries no value anywhere on this desk.</p>')
    rows = []
    for s in src.SOURCES:
        unopened = s["id"] in src.NOT_OPENED
        rows.append(([s["id"], s["publisher"],
                      '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>'
                      % (s["url"], esc(s["title"])),
                      s["evidences"], s["checked"],
                      pill("unv" if unopened else "ver", "not opened" if unopened else "read"),
                      _src_cell([s["id"]])],
                     "hi" if unopened else None))
    b.append(sh.table(["ID", "Publisher", "Document", "What it evidences", "What was checked",
                       "Status", "Source"], rows,
                      note="%d sources, of which %d are linked but were not opened. No secondary "
                           "source &mdash; news reporting, commentary, or a law firm note &mdash; is "
                           "used for any value anywhere on this desk."
                           % (len(src.SOURCES), len(src.NOT_OPENED))))
    return "Sources", "".join(b)


# ------------------------------------------------------------------- 16. flagged

def _flags():
    return [
        ("F01", "Market rent for Property A", "",
         "No rent figure was supplied and no official source exists for one. The model reports the "
         "break-even yield instead of inventing a number, and a grid from 2.0% to 4.0% to compare "
         "a real quote against.",
         "Three written letting appraisals", ["boe_prop19"]),
        ("F02", "Insurance premium, Property A", "",
         "The %s figure on the properties page is the owner's estimate. No quotation was obtained, "
         "and no carrier rate was retrieved for the area." % M(m.OWNER["a_insurance"]),
         "Two written quotations", ["cdi_residential"]),
        ("F03", "Insurance premium, Property B", "",
         "The same, and a three-unit let property needs a different policy form from an "
         "owner-occupier home, so the estimate is doubly uncertain.",
         "Two quotations on a landlord or dwelling fire form", ["cdi_residential"]),
        ("F04", "Maintenance and repair, both properties", "",
         "No figure was supplied. The model uses 0.8% of value a year for Property A and 1.2% for "
         "Property B, informed only by the owner's statement that Property A is lighter. Both are "
         "tested in the sensitivity grid.",
         "Five years of the owner's own records", None),
        ("F05", "Rooftop solar tariff on Property A", "",
         "The utility is not named on this site and no tariff was retrieved, so whether the credit "
         "survives the transfer, and at what rate, is unknown.",
         "The interconnection agreement, and the utility's current export tariff", None),
        ("F06", "Water utility for Property A", "",
         "Not stated. The rate schedule that actually applies was therefore never retrieved.",
         "The water bill, which names the utility, then its published schedule", None),
        ("F07", "Property A effective tax rate", P(_RATE_A),
         "Derived from the owner's own bill divided by the owner's own assessed value. It bundles "
         "the 1%% levy, voter-approved debt and any parcel charges into one number. It is stable "
         "across the owner's own record, from %s to %s, but it is not a published rate."
         % (P(_RATE_LO), P(_RATE_HI)),
         "Read the rate area and the itemised charges off the current bill", ["boe_pub29"]),
        ("F08", "Unexplained residual on Property B's bill", M(_B_RESIDUAL),
         "The owner's reported bill, less the official secured rate applied to the owner's assessed "
         "value, leaves %s a year unaccounted for. It is carried as a flat charge. Parcel taxes and "
         "bond levies are not ad valorem and would explain it, but the composition is unknown."
         % M(_B_RESIDUAL),
         "Read the itemised charges on the bill", ["sftreasurer_secured"]),
        ("F09", "Comparability of the three units at Property B", M(_UNIT_B),
         "The model assumes all three units let alike, so the unit you free by moving out is worth "
         "the same as the unit you live in. If they differ, adjust the occupy option by the "
         "difference.",
         "A letting appraisal for the unit that is currently not let", None),
        ("F10", "Land share of Property A's value", "20%",
         "Only the improvement share is depreciable, and that drives the depreciation shield if you "
         "let the property. The share is chosen, not appraised.",
         "A county assessor's property characteristic record, or an appraisal", None),
        ("F11", "Transfer year", "2045",
         "The midpoint of the 2040 to 2050 window. It is not knowable, and after the growth rates "
         "it is the largest single driver of the answer. 2040 and 2050 are shown alongside it.",
         "Not knowable; the range is published instead", None),
        ("F12", "November 2026 election results", "Unofficial",
         "County returns are due 4 December 2026 and certification is 11 December 2026. Proposition "
         "3, which makes the high-income rates permanent, is reported as passing on the unofficial "
         "count only.",
         "Wait for certification, then re-read", ["sos_results_home", "sos_results_bm"]),
        ("F13", "Indexation of the federal exclusion after 2027", "2.5% assumed",
         "The 2026 and 2027 amounts are official. No official indexation rate is published, so "
         "every year after 2027 on the projections page is a projection and not a finding.",
         "Re-read the inflation adjustments each autumn", ["irs_ir2026_133"]),
        ("F14", "Any proposal to change the step-up in basis at death", "",
         "Proposals recur in commentary. This desk could not find one in the Federal Register, the "
         "Internal Revenue Bulletin, or on the Treasury's site, so no figure is asserted for it "
         "anywhere on this desk.",
         "Check those three sources directly", ["irs_tc409"]),
        ("F15", "Whether a planned short occupancy satisfies the exclusion", "",
         "The guidance says the exclusion is removed when the home stops being the transferee's "
         "principal residence, and that the new base year value is then enrolled from the transfer. "
         "It does not address a plan to occupy for a limited period.",
         "A California estates lawyer, on the facts", ["boe_lta2026_026"]),
        ("F16", "Which figure is enrolled if the transferee moves out", "Two readings",
         "The statute says the base year value established at the change in ownership is enrolled, "
         "adjusted annually, when the exclusion is removed. The Board's guidance reads that as the "
         "market value at the transfer; subdivision (d) speaks instead of the new taxable value, "
         "which is the capped figure. On these projections the two differ by %s of assessed value "
         "by 2076, and by the whole of the benefit in between. Both are shown on the property tax "
         "page. This desk does not choose between them." % M(_REMOVE_GAP),
         "A California lawyer, or a written projection from the county assessor",
         ["leginfo_rtc63_2", "boe_lta2026_026"]),
        ("F17", "Whether the statewide rent cap applies to Property B", "Not determined",
         "The cap is 5% plus the change in the regional cost of living, or 10%, whichever is "
         "lower. The owner-occupied exemption is drafted for a property containing two separate "
         "dwelling units; Property B has three. The single-family exemption needs a written "
         "notice in the prescribed wording and an owner that is not a company. Which applies, if "
         "any, depends on the building's configuration and on the tenancy dates, neither of which "
         "was supplied.",
         "The building record, the tenancy papers, and a local ordinance check",
         ["leginfo_civ1947_12"]),
        ("F18", "The rent index in the model is national, the statute uses a regional one",
         "Simplification",
         "The statute measures the cost-of-living change with the Consumer Price Index for All "
         "Urban Consumers for the metropolitan area in which the property sits. This desk models "
         "rent as tracking national inflation, which is simpler and can differ from the regional "
         "index in either direction.",
         "Retrieve the regional index and re-run; the desk does not name the area, so it is not "
         "retrieved here", ["leginfo_civ1947_12", "bls_cpi_series"]),
        ("F19", "Earlier unrounded figures in public git history", "Not fixable by a commit",
         "Earlier generations of this repository published figures that were not rounded to $10. No "
         "later commit can remove them from the history of a public repository.",
         "Decide whether the repository should be private, or whether to rewrite its history", None),
    ]


def page_flagged():
    b = []
    b.append('<p class="lead">Everything on this desk that is unverified, assumed or irregular. '
             'Where a value could not be confirmed from an official source the cell is <b>blank</b>, '
             'or it carries the owner\'s own estimate clearly marked as one. Nothing here blocks '
             'anything: it is the list to work through.</p>')
    rows = []
    for fid, item, value, detail, action, sids in _flags():
        rows.append(([fid, item, ("num", value if value else "blank"), detail, action,
                      pill("unv", "flagged"),
                      _src_cell(sids, "no official source exists for this item, so no value is "
                                "asserted for it")], None))
    b.append(sh.table(["ID", "Item", ("num", "Value on this desk"), "What is wrong or missing",
                       "What would close it", "Status", "Source"], rows,
                      note="A blank value is deliberate. A gap on this desk is never filled with an "
                           "invented number; where the model needs the figure, it publishes a "
                           "break-even instead so that nothing has to be trusted."))
    return "Flagged for review", "".join(b)


# --------------------------------------------------------------- 17. methodology

def page_methodology():
    b = []
    b.append('<p class="lead">How every number on this desk was produced, what is deliberately not '
             'modelled, and what is kept off the site.</p>')

    b.append("<h2>Assumptions, and why each one was chosen</h2>")
    arows = []
    for name, value, why in m.ASSUMPTION_NOTES:
        arows.append(([name, value, why, pill("asm", "assumption"),
                       _src_cell(None, "an input chosen for this model; no official source "
                                 "publishes it, and it is labelled as an assumption everywhere it "
                                 "appears")], None))
    b.append(sh.table(["Input", "Value used", "Why", "Status", "Source"], arows))

    b.append("<h2>How the model works</h2>")
    steps = [
        (["Market value",
          "The owner's 2026 figure grown at the assumed rate, year by year, to the horizon.",
          pill("der", "derived"),
          _src_cell(None, "the starting figure is the owner's own, so every value downstream is a "
                    "projection and none is sourced")], None),
        (["Assessed value before the transfer",
          "The owner's assessed value trended at no more than 2% a year, which is the Proposition "
          "13 factor.", pill("ver", "verified"), _src_cell(["boe_pub29"])], None),
        (["Assessed value if the market falls",
          "The lower of the trend and the market value, which reproduces the Proposition 8 "
          "decline-in-value rule. The bill then falls with the market.",
          pill("ver", "verified"), _src_cell(["boe_pub29"])], None),
        (["Assessed value at the transfer",
          "With the exclusion: the factored base year value, plus any amount by which market value "
          "exceeds the cap, which is the market value less the allowance. Without it: the full "
          "market value. The exclusion protects the allowance and nothing more.",
          pill("ver", "verified"), _src_cell(["boe_lta2026_026"])], "hi"),
        (["Property tax",
          "The assessed value times the all-in rate derived from the owner's own records, held "
          "constant in real terms across the projection.",
          pill("der", "derived"), _src_cell(["boe_pub29"])], None),
        (["Running costs",
          "Insurance and maintenance scale with the property's own value; water and power scale "
          "with the general price level. Solar is modelled as a credit that shrinks in real terms.",
          pill("asm", "assumption"),
          _src_cell(None, "a convention chosen here; the owner's own ranges are the starting point, "
                    "not a published series")], None),
        (["Rental income if let",
          "Gross rent, less vacancy and a managing agent, less running costs and property tax, less "
          "tax on the net figure, with a straight-line depreciation shield on the improvement share "
          "over 27.5 years.", pill("asm", "assumption"),
          _src_cell(["irs_tc409", "irs_niit"], "the rates and the recovery period are official; the "
                    "land share, vacancy rate and management fee are assumptions")], None),
        (["Sale proceeds",
          "Market value at the transfer, less the assumed cost of selling.",
          pill("asm", "assumption"),
          _src_cell(None, "a conventional figure, not a published one, so the break-even is the "
                    "honest way to present it")], None),
        (["Portfolio",
          "Net proceeds grown at the assumed return, less an annual tax drag for dividends and "
          "realised gains.", pill("asm", "assumption"),
          _src_cell(None, "no official source publishes forward returns; the break-even return is "
                    "published so this assumption can be tested directly")], None),
        (["Present value",
          "Every option discounted at the same rate back to the transfer year, and every option "
          "ends with an asset that has not been sold, so no option is charged a terminal capital "
          "gains tax that another avoids.",
          pill("asm", "assumption"),
          _src_cell(None, "a modelling convention, stated here so that it can be challenged")],
         "hi"),
        (["Imputed housing",
          "The market rent of the dwelling the household actually lives in, added in the economic "
          "column only. Living in your own home is not taxed; being paid rent is. That asymmetry is "
          "real and it is why the two columns rank the options differently.",
          pill("ver", "verified"), _src_cell(["irs_niit"])], None),
        (["Property B's two let units",
          "Left out of all three options, because they are produced whatever you choose. Only the "
          "third unit enters, and only under the occupy option, because that is the one that frees "
          "it.", pill("asm", "assumption"),
          _src_cell(None, "a scoping decision, not a sourced claim")], None),
    ]
    b.append(sh.table(["Step", "How it is computed", "Status", "Source"], steps))

    b.append("<h2>What is deliberately not modelled</h2>")
    notmod = [
        (["The state and local tax cap, and the interaction between federal and state deductions",
          "It changes the combined marginal rate on rental income, but the amount depends on the "
          "whole return and cannot be computed without it. A 40% and a 60% rate are shown instead "
          "of a single figure.", pill("asm", "assumption"), _src_cell(["irs_niit"])], None),
        (["Alternative minimum tax, passive activity loss limits and their carry-forwards",
          "Each can change the tax on rent in a particular year, and each depends on facts that "
          "were not supplied.", pill("asm", "assumption"), _src_cell(["irs_tc409"])], None),
        (["Mortgage interest, if any debt is carried on either property",
          "None was reported, so none is modelled. If there is debt, the carry cost rises and the "
          "comparison between the options shifts.",
          pill("unv", "unverified"), _src_cell(None, "no debt figure was supplied")], None),
        (["Local rent ordinances and just-cause rules for Property B",
          "A city can be stricter than the statewide cap, and just-cause rules can restrict what "
          "you may do with a tenancy. This desk names no city, so no local rule was retrieved.",
          pill("unv", "unverified"),
          _src_cell(["leginfo_civ1947_12"], "the statewide rule is linked; local rules were not")],
         None),
        (["Transfer taxes on a sale, beyond the assumed cost of selling",
          "A city or county transfer tax may apply on top of the assumed selling cost, and it is "
          "not modelled separately.",
          pill("unv", "unverified"), _src_cell(None, "no local rate was retrieved")], None),
        (["Capital gains tax on a later sale of a kept property",
          "All three options end with an unsold asset, so no terminal gain is realised in any of "
          "them and none is charged to any of them.",
          pill("asm", "assumption"), _src_cell(["irs_tc409"])], None),
        (["Estate administration costs, trustee fees and professional fees",
          "Real, and not modelled, because no figures were supplied and no official schedule "
          "applies.", pill("unv", "unverified"),
          _src_cell(None, "no figures were supplied and no official schedule applies")], None),
        (["Homeowner association dues, if any",
          "None was reported for either property.", pill("unv", "unverified"),
          _src_cell(None, "no figure was supplied")], None),
    ]
    b.append(sh.table(["Not modelled", "Why", "Status", "Source"], notmod))

    b.append("<h2>Privacy and the publication boundary</h2>")
    priv = [
        (["No name, street address, parcel identifier, account number, postcode or city",
          "The two properties are called Property A and Property B. Where a rule is county or city "
          "specific, the link points to the official page but the text on this site does not name "
          "the place.", pill("ver", "verified"),
          _src_cell(None, "a design rule of this desk, enforced by its verifier")], None),
        (["Money rounded to the nearest $10",
          "Every dollar figure on this site, including the owner's own tax history, so that a "
          "published number cannot be matched back to a public record. Statutory amounts are quoted "
          "exactly as published, because they are statewide constants that identify nobody.",
          pill("ver", "verified"),
          _src_cell(["boe_lta2025_009", "irs_estate_tax"])], None),
        (["No scripts, no external assets, no forms, no analytics",
          "The published pages are static HTML and CSS. A page that cannot run code and cannot call "
          "out cannot leak what it displays, which is a stronger guarantee than redaction.",
          pill("ver", "verified"),
          _src_cell(None, "enforced by this desk's verifier, which fails the build on a script tag, "
                    "an external reference, a form or an iframe")], None),
        (["Source links open in a new tab and carry no referrer",
          "The pages carry a no-referrer policy and the robots directives ask search engines not to "
          "index them or follow their links.",
          pill("ver", "verified"), _src_cell(None, "a design rule of this desk")], None),
        (["The generator is not published",
          "The model, the source register and the verifier live in a directory the site does not "
          "serve. They remain in the repository so that the work can be reviewed line by line.",
          pill("ver", "verified"),
          _src_cell(None, "excluded from the published site and confirmed by the build")], None),
        (["Rounding is a defence, not a guarantee",
          "A multi-year series of assessed values is close to a fingerprint even when rounded. This "
          "desk names no county, but it does publish a rounded history, because the derived tax "
          "rate rests on it. That trade-off is yours to make, and it is logged as a suggestion.",
          pill("unv", "unverified"),
          _src_cell(None, "a judgement about this site, not a sourced fact")], None),
    ]
    b.append(sh.table(["Measure", "What it means", "Status", "Source"], priv))
    return "Method and privacy", "".join(b)
