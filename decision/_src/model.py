# -*- coding: utf-8 -*-
"""
Deterministic projection engine for the two-property inheritance decision.

Every published dollar figure is passed through r10() (nearest $10) before it
reaches a page, except statutory amounts that are quoted exactly as published
by the legislature or the IRS - those are stored in STATUTORY and are never
run through a model.

Inputs are split into three tiers so the verifier can tell them apart:
  VERIFIED   - read from an official source (sources.py ids carried through)
  OWNER      - supplied by the owner, no official confirmation exists
  ASSUMPTION - chosen here, no source at all; every one is listed and is a
               sensitivity variable on the scenarios page
"""

import math

# ---------------------------------------------------------------- formatting
def r10(x):
    """Round to the nearest $10, halves away from zero (so -15 becomes -20)."""
    if x is None:
        return None
    return int(math.floor(x / 10.0 + 0.5) if x >= 0 else math.ceil(x / 10.0 - 0.5)) * 10


def money(x):
    if x is None:
        return ""
    neg = x < 0
    s = "${:,}".format(abs(int(x)))
    return "-" + s if neg else s


# ------------------------------------------------------------ statutory quotes
STATUTORY = {
    "estate_2026": 15_000_000,
    "estate_2027": 15_480_000,
    "estate_2025": 13_990_000,
    "estate_2024": 13_610_000,
    "gift_annual_2025": 19_000,
    "gift_annual_2027": 20_000,
    "prop19_allowance": 1_044_586,
    "estate_rate": 0.40,
    "ca_top_rate": 0.133,
    "ca_top_bracket_rate": 0.123,
    "fed_ltcg_top": 0.20,
    "niit": 0.038,
    "sec1250_recapture": 0.25,
    "sec121_single": 250_000,
    "sec121_joint": 500_000,
    "sf_rate_fy2026_27": 0.0118162182,
}

# ------------------------------------------------------------- owner inputs
# All rounded to $10 by the owner's instruction so they cannot be traced back
# to the parcel through a public search.
OWNER = {
    "A_market_value_2026": 3_100_000,
    "A_assessed_2026": 550_540,          # owner 2026 assessed value, rounded
    "A_tax_2025": 7_210,
    "A_assessed_2025": 539_740,
    "A_water_month": 130,                # owner range $100-$150
    "A_electric_month": -10,             # owner: solar usually yields a small credit
    "A_insurance_year": 1_500,           # owner estimate, UNVERIFIED
    "B_market_value_2026": 1_800_000,
    "B_assessed_2025": 114_250,
    "B_tax_2025": 2_440,
    "B_water_month": 370,                # owner range $330-$400 for all three units
    "B_electric_month": 50,              # owner range $30-$70
    "B_insurance_year": 1_500,           # owner estimate, UNVERIFIED
    "B_rent_month": 7_150,               # two of three units
    "B_units": 3,
    "B_units_rented": 2,
}

# ---------------------------------------------------------------- assumptions
# Every one of these is a sensitivity variable shown on the scenarios page.
A_DEFAULT = {
    "g_market": 0.040,          # nominal home price growth, baseline
    "g_assessed": 0.020,        # Prop 13 cap - VERIFIED ceiling, used as the growth rate
    "g_allowance": 0.0215,      # CA HPI 2024 change, published in BOE LTA 2025/009
    "cpi": 0.030,               # cost inflation for water / insurance / maintenance
    "rent_growth": 0.035,       # below the AB 1482 cap of 5% + CPI (max 10%)
    "gross_yield": 0.026,       # Property A rent as a share of market value
    "vacancy": 0.05,
    "management": 0.08,
    "maintenance_pct": 0.010,   # share of market value per year
    "disposition_cost": 0.055,  # commission + escrow + transfer charges
    "building_share": 0.70,     # depreciable share of a stepped-up basis
    "portfolio_return": 0.070,  # nominal total return before tax
    "portfolio_yield": 0.020,   # share of return realised and taxed each year
    "discount": 0.050,          # nominal discount rate for NPV
    "sale_tax_rate": 0.371,     # 20% fed + 3.8% NIIT + 13.3% CA
    "horizon": 2076,
    # Market rent for the San Francisco unit that becomes available if the
    # owner moves into Property A. UNKNOWN - no comps supplied. The financial
    # case for occupying does not rest on this figure: the rent collected is
    # offset by the housing given up at Property B, so it is shown separately
    # and switched off in the headline comparison.
    "sf_unit_rent_month": 2_500,
}

# Sensitivity grid for the headline comparison.
SENSITIVITY = {
    "g_market": [0.025, 0.040, 0.055],
    "gross_yield": [0.020, 0.026, 0.032],
    "maintenance_pct": [0.005, 0.010, 0.015],
    "portfolio_return": [0.050, 0.070, 0.090],
    "cpi": [0.020, 0.030, 0.050],
    "discount": [0.030, 0.050, 0.070],
}

# ------------------------------------------------------------- derived rates
def rate_a():
    """Property A effective property-tax rate implied by the owner's 2025 bill.

    Owner 2025 bill / owner 2025 assessed value, both rounded to $10. This is a
    DERIVED figure, not an officially published rate - it bundles the 1% Prop 13
    levy, voter-approved debt and any parcel taxes and direct charges on the
    bill. Santa Clara County has over 900 tax rate areas, so no single
    published rate can be quoted for the parcel.
    """
    return OWNER["A_tax_2025"] / float(OWNER["A_assessed_2025"])


def b_fixed_charges():
    """Property B: the part of the bill that is not ad valorem.

    Owner 2025 bill minus assessed value x the official SF secured rate. A
    positive residual means the bill carries parcel taxes, direct assessments or
    special charges on top of the ad valorem levy. DERIVED from owner input and
    the official rate; flagged for reconciliation against the actual bill.
    """
    adval = OWNER["B_assessed_2025"] * STATUTORY["sf_rate_fy2026_27"]
    return r10(OWNER["B_tax_2025"] - adval)


# ------------------------------------------------------------- core projections
def property_a_series(a=None, last=2076):
    """Year-by-year: market value, Prop 13 assessed value and property tax."""
    a = dict(A_DEFAULT, **(a or {}))
    out = []
    av = float(OWNER["A_assessed_2026"])
    for y in range(2026, last + 1):
        k = y - 2026
        mv = OWNER["A_market_value_2026"] * (1 + a["g_market"]) ** k
        if y > 2026:
            av *= (1 + a["g_assessed"])
        tax = av * rate_a()
        out.append(dict(year=y, market=mv, assessed=av, tax=tax))
    return out


def property_b_series(a=None, last=2076):
    """Year-by-year: assessed value, ad valorem tax, total bill, rent, net."""
    a = dict(A_DEFAULT, **(a or {}))
    fixed = b_fixed_charges()
    out = []
    av = float(OWNER["B_assessed_2025"])          # 2025 is the last owner figure
    rent = OWNER["B_rent_month"] * 12             # current annual rent, 2 units
    for y in range(2025, last + 1):
        if y > 2025:
            av *= (1 + a["g_assessed"])
            rent *= (1 + a["rent_growth"])
        adval = av * STATUTORY["sf_rate_fy2026_27"]
        water = OWNER["B_water_month"] * 12 * (1 + a["cpi"]) ** (y - 2025)
        elec = OWNER["B_electric_month"] * 12 * (1 + a["cpi"]) ** (y - 2025)
        ins = OWNER["B_insurance_year"] * (1 + a["cpi"]) ** (y - 2025)
        maint = OWNER["B_market_value_2026"] * (1 + a["g_market"]) ** (y - 2026) \
            * a["maintenance_pct"]
        costs = water + elec + ins + maint
        out.append(dict(year=y, assessed=av, adval=adval, fixed=fixed,
                        total=adval + fixed, rent=rent, costs=costs,
                        net=rent - costs - (adval + fixed)))
    return out


def freed_unit_income(a=None, year=2045):
    """Annual rent from the San Francisco unit freed up by moving to Property A.

    Zero in the headline comparison (see the note on sf_unit_rent_month).
    """
    a = dict(A_DEFAULT, **(a or {}))
    return a["sf_unit_rent_month"] * 12 * (1 + a["rent_growth"]) ** (year - 2025)


def transfer_values(T, a=None):
    """Values that matter at the moment of transfer in year T."""
    a = dict(A_DEFAULT, **(a or {}))
    ser = {r["year"]: r for r in property_a_series(a, last=max(T, 2076))}
    row = ser[T]
    fbyv = row["assessed"]                    # factored base year value at transfer
    fmv = row["market"]                       # fair market value at date of death
    # The Board of Equalization adjusts the exclusion amount every two years.
    # LTA 2025/009 sets $1,044,586 for transfers from 16 Feb 2025 to 15 Feb 2027,
    # so that exact figure applies to 2025 and 2026 and only then steps up one
    # two-year adjustment at a time.
    adj = 2 * max(0, (T - 2025) // 2)
    allowance = STATUTORY["prop19_allowance"] * (1 + a["g_allowance"]) ** adj
    cap = fbyv + allowance
    excess = max(0.0, fmv - cap)
    occ_av = fbyv + excess                    # Prop 19 adjusted base year value
    rent_av = fmv                             # no exclusion: full reassessment
    return dict(year=T, fbyv=fbyv, fmv=fmv, allowance=allowance, cap=cap,
                excess=excess, occ_av=occ_av, rent_av=rent_av,
                occ_tax=occ_av * rate_a(), rent_tax=rent_av * rate_a(),
                keep_tax=row["tax"])


# ------------------------------------------------------------------- scenarios
def _depreciation(basis, years):
    return basis * A_DEFAULT["building_share"] / 27.5 * years


def scenario_occupy(T, a=None, last=2076):
    """Move in, claim the Prop 19 parent-child exclusion, hold to `last`."""
    a = dict(A_DEFAULT, **(a or {}))
    tv = transfer_values(T, a)
    rows = []
    av = tv["occ_av"]
    basis_no_improvements = tv["fmv"]          # step-up in basis under IRC 1014
    for y in range(T, last + 1):
        k = y - T
        if k:
            av *= (1 + a["g_assessed"])
        mv = tv["fmv"] * (1 + a["g_market"]) ** k
        infl = (1 + a["cpi"]) ** (y - 2026)
        tax = av * rate_a()
        water = OWNER["A_water_month"] * 12 * infl
        elec = OWNER["A_electric_month"] * 12 * infl     # negative = credit
        ins = OWNER["A_insurance_year"] * infl
        maint = mv * a["maintenance_pct"]
        freed = a["sf_unit_rent_month"] * 12 * (1 + a["rent_growth"]) ** (y - 2025)
        cost = tax + water + elec + ins + maint
        # Housing services consumed by living in Property A, valued at the
        # market rent the same house would fetch. Not cash - reported apart.
        imputed = mv * a["gross_yield"]
        rows.append(dict(year=y, market=mv, assessed=av, tax=tax, water=water,
                         electric=elec, insurance=ins, maintenance=maint,
                         freed=freed, imputed=imputed, net=freed - cost,
                         basis=basis_no_improvements))
    # Terminal: sell with the section 121 exclusion for an owner-occupier.
    mv_end = rows[-1]["market"]
    proceeds = mv_end * (1 - a["disposition_cost"])
    gain = max(0.0, mv_end - basis_no_improvements - STATUTORY["sec121_single"])
    tax_end = gain * a["sale_tax_rate"]
    terminal = proceeds - tax_end
    return dict(rows=rows, terminal=terminal, proceeds=proceeds,
                end_tax=tax_end, sale_price=mv_end, gain=gain)


def scenario_rent(T, a=None, last=2076):
    """Do not move in: property is fully reassessed and let to tenants."""
    a = dict(A_DEFAULT, **(a or {}))
    tv = transfer_values(T, a)
    rows = []
    av = tv["rent_av"]
    basis = tv["fmv"]
    dep_basis = basis * a["building_share"]
    for y in range(T, last + 1):
        k = y - T
        if k:
            av *= (1 + a["g_assessed"])
        mv = tv["fmv"] * (1 + a["g_market"]) ** k
        infl = (1 + a["cpi"]) ** (y - 2026)
        gross = mv * a["gross_yield"]
        collected = gross * (1 - a["vacancy"])
        mgmt = collected * a["management"]
        tax = av * rate_a()
        water = OWNER["A_water_month"] * 12 * infl
        elec = OWNER["A_electric_month"] * 12 * infl
        ins = OWNER["A_insurance_year"] * infl
        maint = mv * a["maintenance_pct"]
        noi = collected - mgmt - tax - water - elec - ins - maint
        dep = dep_basis / 27.5
        imputed = a["sf_unit_rent_month"] * 12 * (1 + a["rent_growth"]) ** (y - 2025)
        rows.append(dict(year=y, market=mv, assessed=av, gross=gross,
                         collected=collected, mgmt=mgmt, tax=tax, water=water,
                         electric=elec, insurance=ins, maintenance=maint,
                         noi=noi, depreciation=dep, taxable=noi - dep,
                         imputed=imputed))
    mv_end = rows[-1]["market"]
    proceeds = mv_end * (1 - a["disposition_cost"])
    gain = max(0.0, mv_end - basis)
    recapture = min(dep_basis, _depreciation(basis, last - T + 1))
    recapture_tax = recapture * (STATUTORY["sec1250_recapture"] + STATUTORY["ca_top_rate"])
    tax_end = gain * a["sale_tax_rate"] + recapture_tax
    terminal = proceeds - tax_end
    return dict(rows=rows, terminal=terminal, proceeds=proceeds,
                end_tax=tax_end, recapture_tax=recapture_tax,
                sale_price=mv_end, gain=gain)


def scenario_sell(T, a=None, last=2076):
    """Sell immediately after the step-up in basis and reinvest the proceeds."""
    a = dict(A_DEFAULT, **(a or {}))
    tv = transfer_values(T, a)
    proceeds = tv["fmv"] * (1 - a["disposition_cost"])
    # Sale at the date-of-death value: the step-up means there is essentially no
    # gain, so no capital gains tax arises on the sale itself.
    V = proceeds
    B = proceeds
    rows = []
    for y in range(T, last + 1):
        if y > T:
            income = V * a["portfolio_yield"]
            tax_now = income * a["sale_tax_rate"]
            growth = V * (a["portfolio_return"] - a["portfolio_yield"])
            V = V + growth + income - tax_now
            B = B + income - tax_now          # reinvested after-tax income adds basis
        imputed = a["sf_unit_rent_month"] * 12 * (1 + a["rent_growth"]) ** (y - 2025)
        rows.append(dict(year=y, value=V, basis=B, unrealised=V - B,
                         imputed=imputed))
    gain = max(0.0, V - B)
    tax_end = gain * a["sale_tax_rate"]
    terminal = V - tax_end
    return dict(rows=rows, terminal=terminal, proceeds=proceeds,
                end_tax=tax_end, sale_price=tv["fmv"], gain=gain)


def npv(flows, rate):
    return sum(f / (1 + rate) ** i for i, f in enumerate(flows))


def scenario_npv(T, a=None, last=2076, discount=None):
    """NPV at the transfer date of each scenario, including terminal value."""
    a = dict(A_DEFAULT, **(a or {}))
    d = a["discount"] if discount is None else discount
    out = {}
    occ = scenario_occupy(T, a, last)
    out["occupy"] = npv([r["net"] for r in occ["rows"][:-1]]
                        + [occ["rows"][-1]["net"] + occ["terminal"]], d)
    ren = scenario_rent(T, a, last)
    out["rent"] = npv([r["noi"] for r in ren["rows"][:-1]]
                      + [ren["rows"][-1]["noi"] + ren["terminal"]], d)
    sel = scenario_sell(T, a, last)
    out["sell"] = sel["terminal"] / (1 + d) ** (last - T)

    # Same three numbers with the housing each option lets you live in valued
    # at market rent. This is the like-for-like comparison: option 1 lets you
    # live in Property A, options 2 and 3 leave you in your San Francisco unit.
    out["occupy_h"] = out["occupy"] + npv([r["imputed"] for r in occ["rows"]], d)
    out["rent_h"] = out["rent"] + npv([r["imputed"] for r in ren["rows"]], d)
    out["sell_h"] = out["sell"] + npv([r["imputed"] for r in sel["rows"]], d)
    out["_detail"] = dict(occupy=occ, rent=ren, sell=sel)
    return out


# ------------------------------------------------------------- estate tax model
def estate_exemption_projection(g=0.025, first=2026, last=2076):
    """Project the federal basic exclusion amount.

    The 2027 figure ($15,480,000) is statutory (Rev. Proc. 2026-35). Beyond that
    the amount is indexed, so every later year is an ASSUMPTION at the chosen
    indexation rate. Congress can change the exemption at any time - see the
    law-watch page.
    """
    if not 0.0 <= g <= 0.25:
        raise ValueError("indexation rate %r is not a rate" % g)
    out = []
    for y in range(first, last + 1):
        if y == 2026:
            v = STATUTORY["estate_2026"]
        elif y == 2027:
            v = STATUTORY["estate_2027"]
        else:
            v = STATUTORY["estate_2027"] * (1 + g) ** (y - 2027)
        out.append(dict(year=y, amount=v))
    return out


def estate_tax(gross, year, exemption_g=0.025):
    """Rough federal estate tax on a gross estate in a given year.

    California imposes no estate or inheritance tax (R&TC 13301), so the only
    death tax is federal. This ignores the marital deduction, portability,
    charitable deductions, credits for state death taxes and special-use
    valuation - it is a ceiling illustration, not a computation of liability.
    """
    tbl = {r["year"]: r["amount"] for r in estate_exemption_projection(exemption_g)}
    ex = tbl.get(year, tbl[2076])
    taxable = max(0.0, gross - ex)
    return dict(exemption=ex, taxable=taxable, tax=taxable * STATUTORY["estate_rate"])


# ----------------------------------------------------------------- black swans
# Each regime: (key, name, g_market, cpi, description, official anchor source id)
BLACK_SWAN = [
    dict(key="stagflation", name="1970s stagflation replay",
         g_market=0.090, cpi=0.088,
         desc="High nominal home price growth driven entirely by inflation; "
              "real returns near zero; cash flows and insurance costs inflate "
              "faster than the discount rate.",
         anchor="bls_cpi_hist",
         anchor_text="CPI-U annual average change reached 11.0% (1974), 11.3% "
                     "(1979) and 13.5% (1980)."),
    dict(key="gfc", name="Housing bust and long flat recovery",
         g_market=0.000, cpi=0.020,
         desc="Nominal prices go nowhere for a decade. A fully reassessed "
              "rental locks in a high taxable value while the market value "
              "stagnates; Prop 8 would let the owner petition for a temporary "
              "reduction, but the assessed value snaps back as prices recover.",
         anchor="bls_cpi_hist",
         anchor_text="CPI-U fell 0.4% in 2009, the only negative annual average "
                     "in the post-war series."),
    dict(key="inflation_spike", name="2021-2023 style inflation spike",
         g_market=0.060, cpi=0.058,
         desc="A sharp three-to-five-year burst of inflation followed by "
              "normalisation. Costs jump immediately, rents follow with a lag "
              "under the statewide rent cap.",
         anchor="bls_cpi_hist",
         anchor_text="CPI-U annual average change: 4.7% (2021), 8.0% (2022), "
                     "4.1% (2023)."),
    dict(key="disinflation", name="1990s-style disinflation",
         g_market=0.030, cpi=0.025,
         desc="The benign case. Low and stable inflation, moderate nominal "
              "appreciation; financial assets do the heavy lifting.",
         anchor="bls_cpi_hist",
         anchor_text="CPI-U annual average change fell from 5.4% (1990) to "
                     "2.6% (1994) and stayed near 2-3% through 2000."),
    dict(key="japan", name="Long stagnation",
         g_market=0.005, cpi=0.005,
         desc="Three decades of near-zero nominal growth and near-zero "
              "inflation. The property tax bill becomes the dominant variable "
              "because it is the one thing that still rises every year.",
         anchor="bls_cpi_hist",
         anchor_text="Context only: the BLS series shows the deflation boundary "
                     "at -0.4% (2009)."),
    dict(key="prop13_split", name="Proposition 13 change or split roll",
         g_market=0.040, cpi=0.030,
         desc="A constitutional change that ends acquisition-value assessment "
              "for residential property, or removes the 2% cap. Assessed value "
              "converges on market value and the tax bill rises by an order of "
              "magnitude. No measure on a current California ballot does this "
              "to residential property, but the idea recurs each cycle.",
         anchor="ca_sos_ballot",
         anchor_text="The November 3, 2026 California ballot contained no "
                     "split-roll measure; Proposition 43 (which did not carry) "
                     "dealt only with the vote needed for local special taxes."),
    dict(key="stepup_repeal", name="Step-up in basis restricted",
         g_market=0.040, cpi=0.030,
         desc="Congress taxes unrealised appreciation at death, or caps the "
              "step-up. The sell-and-reinvest route is the one that changes "
              "most: the proceeds shrink by the tax on the gain that accrued "
              "before death.",
         anchor="crs_if12846",
         anchor_text="CRS: options include 'taxing unrealized gains under the "
                     "income tax at death or eliminating step-up in basis'."),
    dict(key="insurance_shock", name="Insurance and hazard cost shock",
         g_market=0.020, cpi=0.030,
         desc="Carrier withdrawals or a catastrophe cycle push premiums up "
              "sharply and force some owners onto the FAIR Plan. Hits the "
              "hold-and-rent case hardest because the premium rises while the "
              "rent is capped.",
         anchor="cdi_marketshare",
         anchor_text="California homeowners direct written premium rose from "
                     "$14.5bn (2024) to $16.4bn (2025) with a reported 2025 "
                     "loss ratio of 170.23%."),
]


def black_swan(T, last=2076):
    """Re-run the three scenarios under each regime."""
    out = []
    for r in BLACK_SWAN:
        a = dict(A_DEFAULT, g_market=r["g_market"], cpi=r["cpi"])
        np = scenario_npv(T, a, last)
        tv = transfer_values(T, a)
        out.append(dict(regime=r, npv=np, tv=tv))
    return out


# --------------------------------------------------------------- break-evens
def _npv_gap(T, a, last, other, with_housing=False):
    """Sell NPV minus the other scenario's NPV, in dollars at the transfer date.

    with_housing=True uses the like-for-like view in which every option is
    credited with the market rent of the home it lets you live in.
    """
    n = scenario_npv(T, a, last)
    if with_housing:
        return n["sell_h"] - n[other + "_h"]
    return n["sell"] - n[other]


def breakeven_portfolio_return(T, other="rent", a=None, last=2076,
                               lo=-0.10, hi=0.40, with_housing=False):
    """Nominal portfolio return at which selling ties the other option.

    Below this return, holding the house wins; above it, selling wins. This is
    the single most decision-useful number on the site because it replaces an
    unverifiable forecast (what will the market return?) with a threshold the
    owner can judge.
    """
    a = dict(A_DEFAULT, **(a or {}))
    for _ in range(200):
        mid = (lo + hi) / 2.0
        aa = dict(a, portfolio_return=mid)
        if _npv_gap(T, aa, last, other, with_housing) > 0:
            hi = mid
        else:
            lo = mid
        if hi - lo < 1e-6:
            break
    return (lo + hi) / 2.0


def breakeven_gross_yield(T, a=None, last=2076, lo=0.0, hi=0.20,
                          with_housing=False):
    """Gross rental yield on Property A at which renting ties selling."""
    a = dict(A_DEFAULT, **(a or {}))
    for _ in range(200):
        mid = (lo + hi) / 2.0
        aa = dict(a, gross_yield=mid)
        if _npv_gap(T, aa, last, "rent", with_housing) > 0:
            lo = mid          # selling still wins -> need a higher yield
        else:
            hi = mid
        if hi - lo < 1e-6:
            break
    return (lo + hi) / 2.0


def breakeven_market_growth(T, other="rent", a=None, last=2076,
                            lo=-0.02, hi=0.20, with_housing=False):
    """Nominal home price growth at which holding ties selling."""
    a = dict(A_DEFAULT, **(a or {}))
    for _ in range(200):
        mid = (lo + hi) / 2.0
        aa = dict(a, g_market=mid)
        # The gap (sell minus hold) FALLS as home price growth rises: faster
        # appreciation helps whoever keeps the house.
        if _npv_gap(T, aa, last, other, with_housing) > 0:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-6:
            break
    return (lo + hi) / 2.0
