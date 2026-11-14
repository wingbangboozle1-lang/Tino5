# -*- coding: utf-8 -*-
"""Pages 1-8: overview, executive summary and the eight analysis pages."""

import shell as sh
import sources as src
import model as m
from model import money as M, pct as P

S = src.link
N = src.nosrc
pill = sh.pill
esc = sh.esc

# Shared computation used by several pages.
_BASE = m.compare()
_ROWS, _PROJ = m.projection_rows()
_RATE_LO, _RATE_HI, _RATE_HIST = m.effective_rate_a_band()
_B_RESIDUAL, _B_ADVAL = m.b_rate_residual()
_OWNER_TAX_ROWS = m.OWNER_HISTORY_A


def _src_cell(sids, reason=None):
    if sids:
        return "<br>".join(S(s) for s in sids)
    return N(reason)


# --------------------------------------------------------------------- 1. overview

def page_index():
    r = _BASE
    be_yield = m.breakeven_gross_yield("occupy", "econ")
    be_growth = m.breakeven_price_growth("occupy", "econ")
    be_ret = m.breakeven_portfolio_return("occupy", "econ")
    kpis = [
        (M(r["value_at_transfer"]), "Property A, projected value at a 2045 transfer",
         "Owner value 2026 grown at the 4.0% assumption"),
        (M(r["taxable_excluded"] * r["rate_a"]), "Property A tax bill in the first year after transfer",
         "With the Proposition 19 exclusion claimed"),
        (M(r["taxable_reassessed"] * r["rate_a"]), "The same bill if it is not claimed",
         "Full reassessment to market value"),
        (P(be_growth), "Break-even house price growth",
         "Keeping wins only above this rate"),
        (P(be_yield), "Break-even gross rental yield",
         "Keeping wins only above this yield"),
        (M(m.estate_exemption(2045)), "Projected federal exclusion, 2045",
         "2027 official amount indexed at the 2.5% assumption"),
    ]
    body = []
    body.append('<p class="lead">Two properties, one decision. <b>Property A</b> is expected to pass '
                'through a family trust some time between 2040 and 2050. <b>Property B</b> is already '
                'owned, lived in, and has two of its three units let. This desk works out what each '
                'way of holding Property A is worth, where the numbers come from, and exactly which '
                'missing facts would change the answer.</p>')
    body.append('<div class="kpis">')
    for v, l, nte in kpis:
        body.append('<div class="kpi"><div class="v">%s</div><div class="l">%s</div>'
                    '<div class="n">%s</div></div>' % (v, l, nte))
    body.append("</div>")

    body.append("<h2>Where to start</h2>")
    body.append(sh.cards([
        ("executive-summary.html", "Executive summary",
         "The recommendation, the three numbers that decide it, and the five facts still missing."),
        ("options.html", "The three options",
         "Occupy, let, or sell and reinvest &mdash; with the break-even rent, growth rate and return."),
        ("questions.html", "Questions and gaps",
         "Every open question, what decision it blocks, and how to get the answer."),
        ("suggestions.html", "Suggestions",
         "Proposed changes to the plan and to this site. Nothing has been implemented."),
    ]))

    body.append("<h2>Everything on this desk</h2>")
    body.append(sh.cards([(fn, label, desc) for fn, label, desc in sh.PAGES if fn != "index.html"]))

    body.append("<h2>How to read a row</h2>")
    body.append('<div class="legend">'
                '<span>%s read from an official source this session, linked on the row</span>'
                '<span>%s owner record &mdash; no official source exists for it</span>'
                '<span>%s computed only from the inputs shown</span>'
                '<span>%s an assumption, listed on the method page</span>'
                '<span>%s unverified &mdash; the value is withheld or unknown</span>'
                "</div>" % (pill("ver", "verified"), pill("own", "owner input"),
                            pill("der", "derived"), pill("asm", "assumption"),
                            pill("unv", "unverified")))
    body.append('<p class="small">A row marked <b>unverified</b> has a blank value cell. Nothing on '
                'this site fills a gap with an invented number: where a figure is needed but unknown, '
                'the model reports the <b>break-even</b> value of that figure instead, so you can '
                'compare it against a real quote.</p>')
    return "Overview", "".join(body)


# ------------------------------------------------------------ 2. executive summary

def page_executive_summary():
    r = _BASE
    be_yield_o = m.breakeven_gross_yield("occupy", "econ")
    be_yield_r = m.breakeven_gross_yield("rent", "econ")
    be_growth_o = m.breakeven_price_growth("occupy", "econ")
    be_ret_o = m.breakeven_portfolio_return("occupy", "econ")
    be_ret_r = m.breakeven_portfolio_return("rent", "econ")

    excl_first_year = r["taxable_excluded"] * r["rate_a"]
    full_first_year = r["taxable_reassessed"] * r["rate_a"]
    excl_saving = full_first_year - excl_first_year

    rows = []
    rows.append((["Property A value at the transfer", ("num", M(r["value_at_transfer"])),
                  pill("der", "derived"), _src_cell(None, "owner 2026 value grown at the 4.0% assumption")], None))
    rows.append((["Taxable value with the exclusion claimed", ("num", M(r["taxable_excluded"])),
                  pill("der", "derived"),
                  _src_cell(["boe_lta2026_026", "boe_lta2025_009"])], "hi"))
    rows.append((["Taxable value if it is not claimed", ("num", M(r["taxable_reassessed"])),
                  pill("der", "derived"), _src_cell(["boe_lta2026_026"])], None))
    rows.append((["First-year tax bill, exclusion claimed", ("num", M(excl_first_year)),
                  pill("der", "derived"), _src_cell(["boe_pub29"])], None))
    rows.append((["First-year tax bill, fully reassessed", ("num", M(full_first_year)),
                  pill("der", "derived"), _src_cell(["boe_pub29"])], None))
    rows.append((["What the exclusion is worth in year one", ("num", M(excl_saving)),
                  pill("der", "derived"),
                  _src_cell(["boe_lta2025_009"], "the allowance is the whole of the benefit once market value exceeds the cap")], "hi"))
    rows.append((["Present value of occupying, less selling", ("num", M(r["npv_occupy_econ"] - r["npv_sell_econ"])),
                  pill("der", "derived"), _src_cell(None, "model output; every input is labelled on the method page")], None))
    rows.append((["Present value of letting, less selling", ("num", M(r["npv_rent_econ"] - r["npv_sell_econ"])),
                  pill("der", "derived"), _src_cell(None, "model output; every input is labelled on the method page")], None))
    rows.append((["Present value of occupying, less letting", ("num", M(r["npv_occupy_econ"] - r["npv_rent_econ"])),
                  pill("der", "derived"), _src_cell(None, "model output; every input is labelled on the method page")], None))
    rows.append((["Break-even gross rental yield, occupy vs sell", ("num", P(be_yield_o)),
                  pill("der", "derived"), _src_cell(None, "break-even, so it does not depend on a rent assumption")], "hi"))
    rows.append((["Break-even gross rental yield, let vs sell", ("num", P(be_yield_r)),
                  pill("der", "derived"), _src_cell(None, "break-even, so it does not depend on a rent assumption")], None))
    rows.append((["Break-even house price growth", ("num", P(be_growth_o)),
                  pill("der", "derived"), _src_cell(None, "break-even, so it does not depend on the 4.0% assumption")], "hi"))
    rows.append((["Break-even portfolio return", ("num", P(be_ret_o)),
                  pill("der", "derived"), _src_cell(None, "break-even, so it does not depend on the 7.0% assumption")], None))
    rows.append((["Federal estate tax exclusion, 2045", ("num", M(m.estate_exemption(2045))),
                  pill("der", "derived"), _src_cell(["irs_ir2026_133"], "2027 official amount indexed at the 2.5% assumption")], None))
    rows.append((["California estate or inheritance tax", "None", pill("ver", "verified"),
                  _src_cell(["leginfo_rtc13301"])], "hi"))

    b = []
    b.append('<p class="lead">On the central assumptions, <b>selling Property A at the transfer and '
             'reinvesting the proceeds produces more wealth than keeping it</b> &mdash; by about '
             '%s in present value if you live in it, and %s if you let it. That result is <b>not '
             'robust</b>, and this page says precisely how fragile it is.</p>'
             % (M(abs(r["npv_occupy_econ"] - r["npv_sell_econ"])),
                M(abs(r["npv_rent_econ"] - r["npv_sell_econ"]))))
    b.append('<div class="banner warn"><b>Read this before the numbers.</b> The ranking between '
             'keeping and selling is decided by <i>one</i> thing: whether the house compounds faster '
             'than a diversified portfolio after tax. On the assumptions used here the house grows at '
             '4.0%% and the portfolio at 7.0%% less a 0.6%% tax drag. That 2.4 point gap, compounding for '
             'thirty-one years, is the whole of the %s gap. Nothing else on this desk moves the answer '
             'as much. The break-even rows below exist so that you do not have to trust either number.</div>'
             % M(abs(r["npv_occupy_econ"] - r["npv_sell_econ"])))

    mc = m.monte_carlo_cached(paths=1200, target="occupy", basis="econ")
    b.append('<div class="banner"><b>The gap shrinks when the future stops being smooth.</b> The '
             '%s above comes from a model in which inflation is a constant %.1f%%. Replayed against '
             'real five-year stretches of the official inflation record, the median gap narrows to '
             '%s and keeping wins outright in about %s of the %s paths &mdash; the middle half runs '
             'from %s to %s. Decide on the break-evens below and on whether you want to live in the '
             'house, not on the headline gap. The <a href="black-swan.html">black-swan page</a> '
             'shows the whole distribution.</div>'
             % (M(abs(r["npv_occupy_econ"] - r["npv_sell_econ"])),
                m.ASSUMPTIONS["inflation"] * 100.0, M(abs(mc["p50"])),
                P(mc["keep_wins"], 0), format(mc["paths"], ","),
                M(mc["p25"]), M(mc["p75"])))

    b.append("<h2>The seven numbers that matter</h2>")
    b.append(sh.table(["Item", ("num", "Value"), "Status", "Source"],
                      rows,
                      note="All money rounded to the nearest $10. Present values are measured at the "
                           "transfer year, 2045, discounted at the 5.0% assumption, and all three "
                           "options end with an unsold asset so that none is penalised for a tax the "
                           "other avoids."))

    b.append("<h2>What the recommendation is, stated plainly</h2>")
    b.append('<div class="banner green"><b>1. If you intend to live in Property A, occupy it &mdash; '
             'and claim the exclusion.</b> Occupying beats letting on the full economic comparison by '
             '%s, and it is the only route that keeps the assessed value below market value. Move in '
             'within one year of the transfer and file the homeowner\'s exemption within one year, or '
             'the exclusion is lost outright.</div>'
             % M(r["npv_occupy_econ"] - r["npv_rent_econ"]))
    b.append('<div class="banner"><b>2. If you will not live in it, the financial case favours selling '
             'over letting</b> on these assumptions, by %s in present value. Letting only wins if the '
             'house can be let for more than %s of its value a year, which is %s a month at the '
             'projected 2045 value.</div>'
             % (M(abs(r["npv_rent_econ"] - r["npv_sell_econ"])), P(be_yield_r),
                M(be_yield_r * r["value_at_transfer"] / 12.0)))
    b.append('<div class="banner"><b>3. The tax tail is large and it is not the one people expect.</b> '
             'The Proposition 19 exclusion does <i>not</i> freeze the tax bill. Because the projected '
             'market value at the transfer (%s) is far above the value cap (%s), the exclusion saves '
             'only the allowance itself &mdash; %s of taxable value, worth %s in the first year. The '
             'bill still jumps from roughly %s today to about %s after the transfer.</div>'
             % (M(r["value_at_transfer"]), M(r["fbyv"] + r["allowance"]), M(r["allowance"]),
                M(excl_saving), M(m.OWNER["a_bill_2025"]), M(excl_first_year)))
    b.append('<div class="banner"><b>4. The estate tax question is about the money, not the house.</b> '
             'California imposes no estate, inheritance, succession or legacy tax at all. The federal '
             'exclusion is %s for 2026 and %s for 2027, and is projected at %s by 2045 on the '
             'assumptions used here. Property passing at death receives a step-up in basis, so the '
             'appreciation built up during the settlor\'s lifetime is not taxed as a capital gain.</div>'
             % (M(m.VERIFIED["estate_2026"]), M(m.VERIFIED["estate_2027"]),
                M(m.estate_exemption(2045))))

    b.append("<h2>What would reverse the recommendation</h2>")
    rev = []
    rev.append((["House price growth above %s" % P(be_growth_o),
                 "Keeping beats selling", pill("der", "derived"),
                 _src_cell(None, "break-even computed by the model; the 4.0% assumption is not used")], None))
    rev.append((["Portfolio return below %s gross" % P(be_ret_o),
                 "Keeping beats selling", pill("der", "derived"),
                 _src_cell(None, "break-even computed by the model; the 7.0% assumption is not used")], None))
    rev.append((["Achievable gross rent above %s of value" % P(be_yield_o),
                 "Occupying beats selling", pill("der", "derived"),
                 _src_cell(None, "break-even; compare against a real letting quote")], None))
    rev.append((["No wish to live in Property A",
                 "The exclusion is unavailable and the bill rises by %s a year" % M(excl_saving),
                 pill("ver", "verified"), _src_cell(["boe_prop19"])], None))
    rev.append((["A change to the step-up in basis at death",
                 "Selling during life becomes relatively better", pill("unv", "unverified"),
                 _src_cell(None, "no such change is in force; see the law watch page")], None))
    rev.append((["A split-roll change to Proposition 13",
                 "The assessed value advantage of holding disappears", pill("unv", "unverified"),
                 _src_cell(["sos_qualified"], "no such measure qualified for the 2026 ballot")], None))
    b.append(sh.table(["If this turns out to be true", "The effect", "Status", "Source"], rev))

    b.append("<h2>The five facts that are still missing</h2>")
    b.append('<p class="small">These are the only inputs on this desk that are pure guesswork. Two of '
             'them feed every projection that follows. Each has a named way to close it on the '
             '<a href="questions.html">questions page</a>.</p>')
    gaps = [
        (["Market rent for Property A", "Not supplied", "Any keep-or-sell conclusion",
          "Three written letting appraisals from agents who manage in the area",
          pill("unv", "unverified"), _src_cell(None, "owner input missing; no official source exists for a rent")], None),
        (["Insurance premium on both properties", "%s a year, owner estimate" % M(m.OWNER["a_insurance"]),
          "Running cost projections", "Two quotations per property, dwelling fire and landlord forms",
          pill("unv", "unverified"),
          _src_cell(["cdi_residential"], "the official data exists but was not retrieved; no value is quoted")], None),
        (["Maintenance and repair spend", "No figure supplied", "Running cost projections",
          "Five years of the owner's own records, then a percentage of value", pill("unv", "unverified"),
          _src_cell(None, "no official source exists for a household maintenance figure")], None),
        (["The solar tariff on Property A", "Not stated", "Whether the power credit survives the transfer",
          "The interconnection agreement and the utility's current net billing tariff", pill("unv", "unverified"),
          _src_cell(None, "no official source; the utility that serves Property A is not named on this site")], None),
        (["The terms of the trust", "Not supplied", "Whether the exclusion is even available",
          "The trust instrument, read with a California estates lawyer", pill("unv", "unverified"),
          _src_cell(["boe_lta2026_026"], "transfers through a trust are eligible, but only if the statutory conditions are met")], None),
    ]
    b.append(sh.table(["Missing fact", "What is on file", "What it blocks",
                       "How to close it", "Status", "Source"], gaps))
    return "Executive summary", "".join(b)


# -------------------------------------------------------------- 3. the properties

def page_properties():
    b = []
    b.append('<p class="lead">What is known about each property, stated so that the difference between '
             'a fact and a guess is visible on every row.</p>')
    rows = [
        (["Role in the decision", "Inherited through a family trust, expected 2040&ndash;2050",
          "Already owned, lived in, two of three units let", pill("own", "owner input"),
          _src_cell(None, "owner record only; not verifiable from any public source")], None),
        (["Estimated market value, November 2026", ("num", M(m.OWNER["a_value_2026"])),
          ("num", M(m.OWNER["b_value_2026"])), pill("own", "owner input"),
          _src_cell(None, "owner record only; rounded to $10 so it cannot be matched to a listing")], None),
        (["Last reported assessed value", ("num", M(m.OWNER["a_assessed_2026"])),
          ("num", M(m.OWNER["b_assessed_2025"])), pill("own", "owner input"),
          _src_cell(None, "owner record only; rounded to $10")], None),
        (["Last reported annual tax bill", ("num", M(m.OWNER["a_bill_2025"])),
          ("num", M(m.OWNER["b_bill_2025"])), pill("own", "owner input"),
          _src_cell(None, "owner record only; rounded to $10")], None),
        (["Livable units", "1", "3", pill("own", "owner input"),
          _src_cell(None, "owner record only")], None),
        (["Units currently let", "0", "2", pill("own", "owner input"),
          _src_cell(None, "owner record only")], None),
        (["Rent now received", ("num", M(0)), ("num", M(m.OWNER["b_rent"])),
          pill("own", "owner input"), _src_cell(None, "owner record only")], None),
        (["Water", "%s to %s a month" % (M(100), M(150)), "%s to %s a month for all three units" % (M(330), M(400)),
          pill("own", "owner input"), _src_cell(None, "owner record only")], None),
        (["Electricity", "Rooftop solar normally produces a credit of %s to %s a month" % (M(10), M(20)),
          "%s to %s a month" % (M(30), M(70)), pill("own", "owner input"),
          _src_cell(None, "owner record only")], None),
        (["Home insurance, owner estimate", ("num", M(m.OWNER["a_insurance"])),
          ("num", M(m.OWNER["b_insurance"])), pill("unv", "unverified"),
          _src_cell(["cdi_residential"], "owner estimate only; no quotation was obtained. The official "
                    "ZIP-level data exists but is not quoted here because it would identify the area")], None),
        (["Maintenance and repair", "Described as lighter than Property B", "No figure supplied",
          pill("unv", "unverified"), _src_cell(None, "no figure was supplied and no official source exists")], None),
        (["Rooftop solar", "Installed", "Not stated", pill("own", "owner input"),
          _src_cell(None, "owner record only; the tariff and its end date are unknown")], None),
        (["Year built", "Not supplied", "Not supplied", pill("unv", "unverified"),
          _src_cell(["leginfo_civ1947_12"], "the year built decides whether the statewide rent cap applies")], None),
        (["Whether the State rent cap applies if let",
          "Likely exempt if it is a single dwelling on its own title, the owner is not a company, and "
          "the statutory notice is given",
          "Applies: the cap is 5% plus the cost-of-living change, or 10%, whichever is lower",
          pill("ver", "verified"), _src_cell(["leginfo_civ1947_12"])], "hi"),
    ]
    b.append(sh.table(["Item", "Property A &mdash; to be inherited", "Property B &mdash; already owned",
                       "Status", "Source"], rows,
                      note="Property A and Property B are labels only. No address, parcel number, "
                           "postcode, city or name appears on this site."))

    b.append("<h2>The owner's own tax history, rounded</h2>")
    b.append('<p class="small">Published at the owner\'s request, rounded to the nearest $10. It is '
             'shown because the effective tax rate is derived from it, and the rate is the single '
             'weakest link in the projections.</p>')
    hist = []
    lo, hi, rates = _RATE_LO, _RATE_HI, _RATE_HIST
    for (y, bill, assessed) in _OWNER_TAX_ROWS:
        rate = dict(rates)[y]
        hist.append(([str(y), ("num", M(bill)), ("num", M(assessed)), ("num", P(rate)),
                      _src_cell(None, "owner record; no official source publishes another "
                                "household's tax bill, so nothing can be linked here")], None))
    b.append(sh.table(["Year", ("num", "Property tax"), ("num", "Tax assessment"),
                       ("num", "Effective rate"), "Source"], hist,
                      note="The bill for a year relates to the assessment for the same year, because "
                           "the lien date is 1 January. The effective rate stays in a band from %s to "
                           "%s across the whole record; %s is used as the planning figure."
                           % (P(lo), P(hi), P(m.effective_rate_a()))))

    b.append("<h2>Property B: what the official rate does not explain</h2>")
    rows2 = [
        (["Official secured tax rate, fiscal year 2026-27", ("num", "1.18162182%"), pill("ver", "verified"),
          _src_cell(["sftreasurer_secured"])], None),
        (["Ad valorem tax on the owner's assessed value", ("num", M(_B_ADVAL)), pill("der", "derived"),
          _src_cell(["sftreasurer_secured"])], None),
        (["The owner's reported bill", ("num", M(m.OWNER["b_bill_2025"])), pill("own", "owner input"),
          _src_cell(None, "owner record only")], None),
        (["Unexplained residual, carried as a flat charge", ("num", M(_B_RESIDUAL)),
          pill("unv", "unverified"),
          _src_cell(["sftreasurer_secured"], "parcel taxes, bonds and district levies are not ad "
                    "valorem and are not itemised on this desk; the composition is unknown")], "hi"),
    ]
    b.append(sh.table(["Item", ("num", "Amount"), "Status", "Source"], rows2,
                      note="The residual is treated as a flat charge that rises with general prices. "
                           "It is flagged on the <a href=\"flagged.html\">flagged page</a> because a "
                           "third of Property B's bill is unexplained by the published rate."))
    return "The two properties", "".join(b)


# -------------------------------------------------------------- 4. property tax

def page_property_tax():
    r = _BASE
    b = []
    b.append('<p class="lead">How the assessed value behaves before the transfer, what happens to it '
             'at the transfer, and what the bill looks like after it.</p>')
    rows = [
        (["Rate ceiling under Proposition 13", "1% of assessed value", pill("ver", "verified"),
          _src_cell(["boe_pub29"])], None),
        (["Additions for voter-approved debt", "Allowed on top of the 1%", pill("ver", "verified"),
          _src_cell(["boe_pub29"])], None),
        (["Reassessment trigger", "Change in ownership, or completion of new construction",
          pill("ver", "verified"), _src_cell(["boe_pub29"])], None),
        (["Annual increase in base year value", "No more than 2%", pill("ver", "verified"),
          _src_cell(["boe_pub29"])], None),
        (["Lien date", "1 January", pill("ver", "verified"), _src_cell(["boe_pub29"])], None),
        (["If market value falls below the trend",
          "The assessor enrolls the lower market value; it then rises with the market until it meets "
          "the trend again (Proposition 8)", pill("ver", "verified"), _src_cell(["boe_pub29"])], None),
        (["All-in rate used for Property A", ("num", P(m.effective_rate_a())), pill("der", "derived"),
          _src_cell(None, "the owner's own bill divided by the owner's own assessed value; bundles "
                    "the 1% levy, voter-approved debt and any parcel charges")], "hi"),
        (["Range of that rate across the owner's 2014-2025 record",
          "%s to %s" % (P(_RATE_LO), P(_RATE_HI)), pill("der", "derived"),
          _src_cell(None, "derived from the owner's rounded history on the properties page")], None),
        (["Official secured rate for Property B, FY 2026-27", ("num", "1.18162182%"),
          pill("ver", "verified"), _src_cell(["sftreasurer_secured"])], None),
    ]
    b.append(sh.table(["Rule", "What it says", "Status", "Source"], rows))

    b.append("<h2>Proposition 19, the intergenerational exclusion</h2>")
    rows2 = [
        (["What it covers", "A family home or a family farm passing between parent and child, or "
          "grandparent and grandchild", pill("ver", "verified"), _src_cell(["boe_lta2026_026"])], None),
        (["The residence condition", "It must be the principal residence of the transferor and become "
          "the principal residence of the transferee", pill("ver", "verified"),
          _src_cell(["boe_prop19"])], None),
        (["Does a rental home qualify?", "No", pill("ver", "verified"), _src_cell(["boe_prop19"])], "hi"),
        (["Value cap", "Factored base year value plus $1,000,000, adjusted every two years",
          pill("ver", "verified"), _src_cell(["boe_lta2025_009"])], None),
        (["Adjusted amount in force", ("num", "1,044,586"), pill("ver", "verified"),
          _src_cell(["boe_lta2025_009"])], "hi"),
        (["Period it covers", "16 February 2025 to 15 February 2027", pill("ver", "verified"),
          _src_cell(["boe_lta2025_009"])], None),
        (["Next adjustment", "February 2027, then every second February", pill("ver", "verified"),
          _src_cell(["boe_lta2025_009"])], None),
        (["What the adjustment tracks",
          "The percentage change in the Federal Housing Finance Agency house price index for "
          "California, which was 2.15% for 2024", pill("ver", "verified"),
          _src_cell(["boe_lta2025_009", "fhfa_hpi"])], None),
        (["Occupancy deadline", "The transferee must occupy within one year of the transfer",
          pill("ver", "verified"), _src_cell(["boe_lta2026_026"])], "hi"),
        (["Homeowner's exemption claim", "Within one year of the transfer", pill("ver", "verified"),
          _src_cell(["boe_prop19"])], None),
        (["Exclusion claim", "Within three years, or before transfer to a third party",
          pill("ver", "verified"), _src_cell(["boe_prop19"])], None),
        (["Does the exclusion survive if the transferee moves out?",
          "No. It is removed, and the new base year value established at the transfer is then "
          "enrolled, trended at 2% a year in the meantime", pill("ver", "verified"),
          _src_cell(["boe_lta2026_026"])], "hi"),
        (["Does a trust qualify?", "Yes. The trust is looked through to present beneficial ownership",
          pill("ver", "verified"), _src_cell(["boe_lta2026_026"])], None),
        (["Does a company or an LLC qualify?", "No. Property held by a legal entity is not eligible",
          pill("ver", "verified"), _src_cell(["boe_lta2026_026"])], None),
        (["A multi-unit property", "Each unit is a separate principal residence; each must qualify "
          "individually", pill("ver", "verified"), _src_cell(["boe_lta2026_026"])], None),
    ]
    b.append(sh.table(["Question", "Answer", "Status", "Source"], rows2,
                      note="The exclusion is claimed on the form the Board of Equalization prescribes, "
                           "filed with the county assessor. This desk does not name the county, but "
                           "the rule is statewide."))

    b.append("<h2>What the transfer does to Property A's assessed value</h2>")
    rows3 = [
        (["Projected market value at the transfer", ("num", M(r["value_at_transfer"])),
          pill("der", "derived"), _src_cell(None, "owner 2026 value grown at the 4.0% assumption")], None),
        (["Factored base year value at the transfer", ("num", M(r["fbyv"])),
          pill("der", "derived"), _src_cell(["boe_pub29"], "the owner's 2026 assessed value trended at 2% a year")], None),
        (["Allowance in force at the transfer", ("num", M(r["allowance"])),
          pill("der", "derived"),
          _src_cell(["boe_lta2025_009"], "the 2025-27 amount indexed biennially at the 2.0% assumption")], None),
        (["Value cap", ("num", M(r["fbyv"] + r["allowance"])), pill("der", "derived"),
          _src_cell(["boe_lta2026_026"])], None),
        (["New taxable value with the exclusion", ("num", M(r["taxable_excluded"])),
          pill("der", "derived"), _src_cell(["boe_lta2026_026"])], "hi"),
        (["New taxable value without it", ("num", M(r["taxable_reassessed"])),
          pill("der", "derived"), _src_cell(["boe_pub29"])], None),
        (["First-year bill with the exclusion", ("num", M(r["taxable_excluded"] * r["rate_a"])),
          pill("der", "derived"), _src_cell(["boe_pub29"])], "hi"),
        (["First-year bill without it", ("num", M(r["taxable_reassessed"] * r["rate_a"])),
          pill("der", "derived"), _src_cell(["boe_pub29"])], None),
    ]
    b.append(sh.table(["Step", ("num", "Amount"), "Status", "Source"], rows3,
                      note="Because the market value is far above the cap, the new taxable value is "
                           "simply the market value less the allowance. The exclusion is therefore "
                           "worth the allowance and no more &mdash; it does not protect the whole of "
                           "the gap between assessed and market value."))
    return "Property tax", "".join(b)


# ---------------------------------------------------------- 5. inheritance tax

def page_inheritance_tax():
    b = []
    b.append('<p class="lead">The federal estate tax, California\'s prohibition, and the step-up in '
             'basis that makes inherited property different from property bought during life.</p>')
    rows = [
        (["2026 filing threshold", ("num", "15,000,000"), pill("ver", "verified"),
          _src_cell(["irs_estate_tax", "irs_estate_faq"])], "hi"),
        (["2027 basic exclusion amount", ("num", "15,480,000"), pill("ver", "verified"),
          _src_cell(["irs_ir2026_133"])], "hi"),
        (["2025 threshold", ("num", "13,990,000"), pill("ver", "verified"),
          _src_cell(["irs_estate_tax"])], None),
        (["2024 threshold", ("num", "13,610,000"), pill("ver", "verified"),
          _src_cell(["irs_estate_tax"])], None),
        (["The statute behind the 2026 amount",
          "Public Law 119-21, signed 4 July 2025, amended section 2010(c)(3)", pill("ver", "verified"),
          _src_cell(["irs_estate_faq"])], None),
        (["Rate above the exclusion", ("num", "40%"), pill("ver", "verified"),
          _src_cell(["irs_estate_faq"])], None),
        (["Annual gift exclusion, 2026", ("num", "19,000"), pill("ver", "verified"),
          _src_cell(["irs_ir2026_133"])], None),
        (["Annual gift exclusion, 2027", ("num", "20,000"), pill("ver", "verified"),
          _src_cell(["irs_ir2026_133"])], None),
        (["Portability", "A surviving spouse may take the unused exemption, but only on a timely "
          "filed estate tax return", pill("ver", "verified"), _src_cell(["irs_estate_faq"])], None),
        (["Filing deadline", "Nine months after death, with an automatic six month extension on "
          "Form 4768", pill("ver", "verified"), _src_cell(["irs_estate_faq"])], None),
        (["Late portability election", "Rev. Proc. 2022-32 gives a simplified method where no filing "
          "requirement exists", pill("ver", "verified"), _src_cell(["irs_estate_faq"])], None),
        (["Estate tax closing letter fee", ("num", "67"), pill("ver", "verified"),
          _src_cell(["irs_estate_faq"])], None),
        (["California estate, inheritance, succession or legacy tax", "None may be imposed by the "
          "state or any of its political subdivisions", pill("ver", "verified"),
          _src_cell(["leginfo_rtc13301"])], "hi"),
    ]
    b.append(sh.table(["Item", "Amount or rule", "Status", "Source"], rows,
                      note="The estate tax is charged to the estate, not to the person who inherits. "
                           "Whether it applies at all depends on the size of the whole gross estate, "
                           "including any cash and securities, not on the house alone."))

    b.append("<h2>Projected exclusion, 2026 to 2050</h2>")
    proj = []
    for y in range(2026, 2051):
        if y in (2026, 2027):
            proj.append(([str(y), ("num", M(m.estate_exemption(y))), pill("ver", "verified"),
                          _src_cell(["irs_estate_tax"] if y == 2026 else ["irs_ir2026_133"])], None))
        else:
            proj.append(([str(y), ("num", M(m.estate_exemption(y))), pill("asm", "assumption"),
                          _src_cell(["irs_ir2026_133"], "the 2027 official amount indexed at the "
                                    "2.5% assumption; indexation is not itself an official figure")], None))
    b.append(sh.table(["Year of death", ("num", "Basic exclusion amount"), "Status", "Source"], proj,
                      note="The 2026 and 2027 amounts are official. Everything after 2027 is an "
                           "indexed projection and is labelled as one; the exclusion is doubled for a "
                           "married couple where portability is elected."))

    b.append("<h2>Basis, and why it matters more than the rate</h2>")
    rows2 = [
        (["Basis of property acquired from a decedent", "Fair market value at the date of death",
          pill("ver", "verified"), _src_cell(["irs_tc409", "irs_p551"])], "hi"),
        (["Consequence", "Appreciation during the settlor's lifetime is never taxed as a capital gain",
          pill("der", "derived"), _src_cell(["irs_tc409"])], None),
        (["Long-term capital gain rates", "0%, 15% or 20% depending on taxable income",
          pill("ver", "verified"), _src_cell(["irs_tc409"])], None),
        (["Unrecaptured section 1250 gain on real property", "Maximum 25%", pill("ver", "verified"),
          _src_cell(["irs_tc409"])], None),
        (["Net investment income tax", "3.8% on net investment income over $250,000 joint or "
          "$200,000 single; the thresholds are not indexed", pill("ver", "verified"),
          _src_cell(["irs_niit"])], None),
        (["Gain excluded under section 121", "Also excluded from the net investment income tax",
          pill("ver", "verified"), _src_cell(["irs_niit"])], None),
        (["California treatment of capital gains", "Taxed as ordinary income, 1% to 12.3%, plus a 1% "
          "surcharge on taxable income over $1,000,000", pill("ver", "verified"),
          _src_cell(["ftb_2025_rates", "leginfo_rtc17043"])], "hi"),
        (["Top California marginal rate", ("num", "13.3%"), pill("der", "derived"),
          _src_cell(["ftb_2025_rates", "leginfo_rtc17043"], "12.3% from the schedules plus the 1% "
                    "surcharge in Revenue and Taxation Code 17043")], None),
        (["Top federal rate for 2027", ("num", "37% over 661,375 single, 793,650 joint"),
          pill("ver", "verified"), _src_cell(["irs_ir2026_133"])], None),
    ]
    b.append(sh.table(["Item", "Rule", "Status", "Source"], rows2,
                      note="The step-up is the reason a sale immediately after the transfer produces "
                           "almost no capital gains tax. It is also the rule most often proposed for "
                           "change; see the law watch page."))

    b.append("<h2>What a taxable estate would cost</h2>")
    grid = []
    for gross in (10_000_000, 15_000_000, 20_000_000, 25_000_000, 30_000_000, 40_000_000):
        tax26 = m.estate_tax_on(gross, 2026)
        tax45 = m.estate_tax_on(gross, 2045)
        grid.append(([("num", M(gross)), ("num", M(tax26)), ("num", M(tax45)),
                      pill("der", "derived"), _src_cell(["irs_estate_faq", "irs_ir2026_133"],
                                                        "40% of the amount above the exclusion; the 2045 column uses the indexed projection")], None))
    b.append(sh.table([("num", "Gross estate"), ("num", "Tax at 2026 rates"),
                       ("num", "Tax at projected 2045 rates"), "Status", "Source"], grid,
                      note="Illustrative only. The size of the estate is not known to this desk and no "
                           "figure for it has been supplied."))
    return "Inheritance and estate tax", "".join(b)


# ---------------------------------------------------------------- 6. running costs

def page_running_costs():
    b = []
    b.append('<p class="lead">Insurance, water, power, maintenance and the property tax bill, and how '
             'each is projected forward.</p>')
    rows = [
        (["Property A water", "%s to %s a month" % (M(100), M(150)), "Metered; projected with general "
          "prices", pill("own", "owner input"),
          _src_cell(None, "owner record only; the utility that serves Property A is not named here")], None),
        (["Property A power", "A credit of %s to %s a month" % (M(10), M(20)),
          "Rooftop solar; projected with general prices", pill("own", "owner input"),
          _src_cell(None, "owner record only; the tariff is unknown and may change")], None),
        (["Property A insurance", ("num", M(m.OWNER["a_insurance"])), "Projected with rebuilding cost, "
          "so with the property's value", pill("unv", "unverified"),
          _src_cell(["cdi_residential"], "owner estimate only; no quotation obtained")], None),
        (["Property A maintenance", "%s of value a year" % P(m.ASSUMPTIONS["maint_a"], 1),
          "Projected with the property's value", pill("asm", "assumption"),
          _src_cell(None, "no figure supplied; informed only by the owner's statement that Property A "
                    "is lighter than Property B")], None),
        (["Property B water", "%s to %s a month, all three units" % (M(330), M(400)),
          "Metered; projected with general prices", pill("own", "owner input"),
          _src_cell(None, "owner record only")], None),
        (["Property B power", "%s to %s a month" % (M(30), M(70)), "Projected with general prices",
          pill("own", "owner input"), _src_cell(None, "owner record only")], None),
        (["Property B insurance", ("num", M(m.OWNER["b_insurance"])), "Projected with rebuilding cost",
          pill("unv", "unverified"),
          _src_cell(["cdi_residential"], "owner estimate only; a three-unit let property would "
                    "normally need a landlord or dwelling fire form, not an owner-occupier form")], None),
        (["Property B maintenance", "%s of value a year" % P(m.ASSUMPTIONS["maint_b"], 1),
          "Projected with the property's value", pill("asm", "assumption"),
          _src_cell(None, "no figure supplied; set above Property A because the owner described "
                    "Property B as heavier")], None),
        (["Letting: vacancy allowance", P(m.ASSUMPTIONS["vacancy"], 1), "Share of gross rent",
          pill("asm", "assumption"), _src_cell(None, "no owner history was supplied")], None),
        (["Letting: managing agent", P(m.ASSUMPTIONS["management"], 1), "Share of collected rent",
          pill("asm", "assumption"),
          _src_cell(None, "the owner already manages Property B, so the sensitivity sets this to zero")], None),
        (["Cost of selling", P(m.ASSUMPTIONS["selling_cost"], 1), "Commission, escrow, transfer charges",
          pill("asm", "assumption"), _src_cell(None, "no official schedule; a conventional figure")], None),
    ]
    b.append(sh.table(["Item", "Figure used", "How it is projected", "Status", "Source"], rows))

    b.append("<h2>Property A running costs by year, if you live in it</h2>")
    cost_rows = []
    for row in _ROWS:
        if row["year"] in (2026, 2030, 2035, 2040, 2045, 2050, 2055, 2060, 2070, 2076):
            cost_rows.append(([str(row["year"]), ("num", M(row["a_tax"])), ("num", M(row["a_cost"])),
                               ("num", M(row["a_tax"] + row["a_cost"])),
                               ("num", M((row["a_tax"] + row["a_cost"]) / 12.0)),
                               pill("der", "derived"),
                               _src_cell(["boe_pub29"], "property tax from the assessed value path; "
                                         "running costs from the owner's ranges and the stated assumptions")],
                              "hi" if row["year"] == 2045 else None))
    b.append(sh.table(["Year", ("num", "Property tax"), ("num", "Other running costs"),
                       ("num", "Total a year"), ("num", "A month"), "Status", "Source"], cost_rows,
                      note="The jump at 2045 is the reassessment on transfer, reduced by the "
                           "Proposition 19 exclusion. Running costs rise with the property's value, "
                           "which is why they grow fastest in the later years."))

    b.append("<h2>Property B, as it stands today</h2>")
    b0 = _ROWS[0]
    rows3 = [
        (["Rent from two units", ("num", M(b0["b_rent"])), pill("own", "owner input"),
          _src_cell(None, "owner record only")], None),
        (["Property tax", ("num", M(b0["b_tax"])), pill("der", "derived"),
          _src_cell(["sftreasurer_secured"])], None),
        (["Water, power, insurance, maintenance", ("num", M(b0["b_cost"])), pill("der", "derived"),
          _src_cell(None, "owner ranges plus stated assumptions")], None),
        (["Net before income tax", ("num", M(b0["b_rent"] - b0["b_tax"] - b0["b_cost"])),
          pill("der", "derived"), _src_cell(["irs_niit"], "rental income is net investment income and "
                                            "is taxed at ordinary rates plus 3.8% above the thresholds")], "hi"),
        (["One unit, if it were let", ("num", M(m.b_unit_rent())), pill("der", "derived"),
          _src_cell(None, "the owner's $7,150 a month for two units divided by two, on the assumption "
                    "the three units are comparable. This is the income you free by moving out")], "hi"),
        (["Statewide cap on rent increases",
          "5% plus the change in the cost of living, or 10%, whichever is lower",
          pill("ver", "verified"), _src_cell(["leginfo_civ1947_12"])], None),
    ]
    b.append(sh.table(["Item", ("num", "Amount"), "Status", "Source"], rows3))
    return "Running costs", "".join(b)


# ------------------------------------------------------------------ 7. projections

def page_projections():
    b = []
    b.append('<p class="lead">Year by year to 2076: market value, assessed value and tax for both '
             'properties, with the reassessment at the transfer year.</p>')
    b.append('<div class="banner">The transfer is modelled in <b>2045</b>, the midpoint of the '
             '2040&ndash;2050 window. Assessed values before the transfer trend at 2% a year under '
             'Proposition 13. At the transfer the assessed value is reset under Proposition 19 with '
             'the exclusion claimed, then trends at 2% again. Market value grows at the 4.0% '
             'assumption throughout.</div>')
    rows = []
    for row in _ROWS:
        rows.append(([str(row["year"]),
                      ("num", M(row["a_value"])), ("num", M(row["a_assessed"])),
                      ("num", M(row["a_tax"])),
                      ("num", M(row["b_value"])), ("num", M(row["b_assessed"])),
                      ("num", M(row["b_tax"])),
                      pill("der", "derived"),
                      _src_cell(["boe_pub29", "sftreasurer_secured", "boe_lta2025_009"])],
                     "hi" if row["year"] == 2045 else None))
    b.append(sh.table(["Year", ("num", "A market value"), ("num", "A assessed value"),
                       ("num", "A tax"), ("num", "B market value"), ("num", "B assessed value"),
                       ("num", "B tax"), "Status", "Source"], rows,
                      note="Every figure is rounded to the nearest $10. Market values are projections "
                           "from the owner's 2026 figure; assessed values follow the statutory rules, "
                           "not the market, which is why the two columns diverge."))

    b.append("<h2>The same projection at the ends of the window</h2>")
    alt = []
    for ty in (2040, 2045, 2050):
        r = m.compare(transfer_year=ty)
        alt.append(([str(ty), ("num", M(r["value_at_transfer"])), ("num", M(r["allowance"])),
                     ("num", M(r["taxable_excluded"])), ("num", M(r["taxable_excluded"] * r["rate_a"])),
                     ("num", M(r["taxable_reassessed"] * r["rate_a"])), pill("der", "derived"),
                     _src_cell(["boe_lta2025_009", "boe_pub29"])],
                    "hi" if ty == 2045 else None))
    b.append(sh.table(["Transfer year", ("num", "Market value"), ("num", "Prop 19 allowance"),
                       ("num", "Taxable value"), ("num", "First-year bill"),
                       ("num", "Bill if fully reassessed"), "Status", "Source"], alt,
                      note="A later transfer means a bigger allowance, because it is indexed, but also "
                           "a bigger market value. The allowance does not keep pace with the value, so "
                           "the bill is larger the later the transfer."))
    return "Projections 2026-2076", "".join(b)


# --------------------------------------------------------------------- 8. options

def page_options():
    r = _BASE
    b = []
    b.append('<p class="lead">Three ways to hold Property A, compared on the same footing. All three '
             'end with an asset that has not been sold at the 2076 horizon, so none is penalised for '
             'a terminal tax the others avoid.</p>')
    b.append('<div class="banner"><b>What "economic" means here.</b> The <b>cash</b> column counts '
             'money only. The <b>economic</b> column adds the market rent of the dwelling the '
             'household actually lives in &mdash; because living in your own home is untaxed and being '
             'paid rent is not, and that asymmetry is the largest single tax effect in this whole '
             'decision. The two units of Property B that are already let are common to all three '
             'options and are left out of all of them.</div>')

    rows = [
        (["Present value, cash only", ("num", M(r["npv_occupy_cash"])), ("num", M(r["npv_rent_cash"])),
          ("num", M(r["npv_sell_cash"])), pill("der", "derived"),
          _src_cell(None, "model output; inputs labelled on the method page")], None),
        (["Present value, including imputed housing", ("num", M(r["npv_occupy_econ"])),
          ("num", M(r["npv_rent_econ"])), ("num", M(r["npv_sell_econ"])), pill("der", "derived"),
          _src_cell(None, "model output; inputs labelled on the method page")], "hi"),
        (["Value of the housing you live in", ("num", M(r["imputed_occupy"])),
          ("num", M(r["imputed_other"])), ("num", M(r["imputed_other"])), pill("der", "derived"),
          _src_cell(None, "imputed market rent, discounted")], None),
        (["First-year tax bill after the transfer",
          ("num", M(r["taxable_excluded"] * r["rate_a"])),
          ("num", M(r["taxable_reassessed"] * r["rate_a"])), "Not applicable", pill("der", "derived"),
          _src_cell(["boe_pub29", "boe_lta2025_009"])], "hi"),
        (["Proposition 19 exclusion available?", "Yes, if you move in within a year and file in time",
          "No &mdash; a let property does not qualify", "Not applicable", pill("ver", "verified"),
          _src_cell(["boe_prop19"])], None),
        (["Cash flow in the first full year", ("num", M(r["occ_rows"][0]["cash"])),
          ("num", M(r["rent_rows"][0]["cash"])), ("num", M(0)), pill("der", "derived"),
          _src_cell(None, "model output; selling produces no annual flow, only the portfolio")], None),
        (["Annual depreciation shield", ("num", M(0)), ("num", M(r["annual_dep"])), ("num", M(0)),
          pill("asm", "assumption"),
          _src_cell(None, "straight line over 27.5 years on 80% of the stepped-up basis; the land "
                    "share is an assumption, not an appraisal")], None),
    ]
    b.append(sh.table(["Item", ("num", "Occupy"), ("num", "Let"), ("num", "Sell and reinvest"),
                       "Status", "Source"], rows))

    b.append("<h2>Break-evens: the answer without the assumptions</h2>")
    b.append('<p class="small">Each row asks: at what value of this one input does keeping stop being '
             'better than selling? The answer does not depend on the assumption it replaces, which is '
             'the point.</p>')
    be = []
    for target, label in (("occupy", "Occupy vs sell"), ("rent", "Let vs sell")):
        by = m.breakeven_gross_yield(target, "econ")
        bg = m.breakeven_price_growth(target, "econ")
        br = m.breakeven_portfolio_return(target, "econ")
        bt = m.breakeven_tax_rate(target, "econ")
        bm = m.breakeven_maint(target, "econ")
        be.append(([label, P(by),
                    M(by * r["value_at_transfer"] / 12.0) + " a month at the 2045 value",
                    P(bg), P(br),
                    "No rate high enough" if bt is None else P(bt),
                    "No rate high enough" if bm is None else P(bm, 1),
                    pill("der", "derived"),
                    _src_cell(None, "break-even computed by the model")],
                   "hi" if target == "occupy" else None))
    b.append(sh.table(["Comparison", ("num", "Break-even rent as % of value"),
                       "The same as a monthly rent", ("num", "Break-even price growth"),
                       ("num", "Break-even portfolio return"), "Break-even tax rate",
                       "Break-even maintenance", "Status", "Source"], be,
                      note="'No rate high enough' means the gap is not closed even at a zero property "
                           "tax rate or zero maintenance: the result is driven by the difference "
                           "between house price growth and portfolio return, not by running costs."))

    b.append("<h2>Sensitivity: does the ranking survive?</h2>")
    grid = []
    for growth in (0.02, 0.03, 0.04, 0.05, 0.06):
        for ret in (0.05, 0.06, 0.07, 0.08):
            d = m.compare(price_growth=growth, portfolio_return=ret)
            gapo = d["npv_occupy_econ"] - d["npv_sell_econ"]
            grid.append(([P(growth, 0), P(ret, 0), ("num", M(gapo)),
                          "Keep" if gapo > 0 else "Sell", pill("der", "derived"),
                          _src_cell(None, "model output")],
                         "hi" if abs(growth - 0.04) < 1e-9 and abs(ret - 0.07) < 1e-9 else None))
    b.append(sh.table([("num", "House price growth"), ("num", "Portfolio return"),
                       ("num", "Occupy less sell"), "Winner", "Status", "Source"], grid,
                      note="The highlighted row is the baseline. The ranking flips between 5% and 6% "
                           "house price growth at a 7% portfolio return."))

    b.append("<h2>The variant: move in to secure the exclusion, then let it</h2>")
    var = []
    for lead in (0, 1, 3, 5, 10):
        d = m.compare(lead_occupancy_years=lead) if lead else _BASE
        first = d["taxable_excluded"] * d["rate_a"] if lead == 0 else d["assessed_excluded"][1] * d["rate_a"]
        var.append(([str(lead) if lead else "Not applicable",
                     ("num", M(d["assessed_excluded"][lead + 1] * d["rate_a"]) if lead else
                      M(_BASE["assessed_excluded"][1] * _BASE["rate_a"])),
                     pill("der", "derived"),
                     _src_cell(["boe_lta2026_026"], "on removal the new base year value established at "
                               "the transfer is enrolled, trended at 2% a year in the meantime")],
                    "hi" if lead == 0 else None))
    b.append(sh.table(["Years of genuine occupancy before moving out",
                       ("num", "Property tax in the year after the exclusion is lost"),
                       "Status", "Source"], var,
                      note="The guidance says the exclusion is removed when the home stops being the "
                           "transferee's principal residence, and that the new base year value "
                           "established at the transfer is then enrolled. Whether a planned short "
                           "occupancy satisfies the statute is a question for a California lawyer, not "
                           "for this desk &mdash; it is logged on the questions page."))
    return "The three options", "".join(b)
