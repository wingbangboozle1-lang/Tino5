# -*- coding: utf-8 -*-
"""
Decision model for the owner-brief desk (session arena-cbe837cb).

Everything here is arithmetic applied to inputs labelled in exactly one of four ways, and
the label is carried into every published cell:

  verified   - read from an official source this session (see sources.py)
  owner      - supplied by the owner; no official source exists for it
  derived    - computed only from verified and owner inputs
  assumption - chosen here, listed on the methodology page, never presented as fact

No value is invented to fill a gap. Where the owner has not supplied a figure the model
needs (market rent for Property A, maintenance, insurance quotations) the model takes it as
a CLOSURE PARAMETER and reports the break-even value of that parameter. That is the point of
the design: "should I keep or sell" is answered as "keep if the rent is above $X", not as a
single dollar figure resting on a made-up rent.

Money is rounded to the nearest $10 by r10()/money() before it reaches a page.
"""

import math
import random

# --------------------------------------------------------------------------- rounding

def r10(x):
    """Round to the nearest $10."""
    if x is None:
        return None
    return int(math.floor(abs(x) / 10.0 + 0.5)) * 10 * (1 if x >= 0 else -1)


def money(x):
    if x is None:
        return "&mdash;"
    v = r10(x)
    if v < 0:
        return "&minus;$%s" % format(-v, ",d")
    return "$%s" % format(v, ",d")


def pct(x, places=2):
    if x is None:
        return "&mdash;"
    return ("%." + str(places) + "f%%") % (x * 100.0)


# --------------------------------------------------------------------- owner inputs
# Owner figures are rounded to the nearest $10 on entry, per the owner's instruction that
# published figures must not be traceable back to a public record.

OWNER = dict(
    # Property A - the home to be inherited through a trust, expected 2040-2050.
    a_value_2026=3_100_000,
    a_assessed_2026=550_540,      # owner record, rounded from the 2026 assessment
    a_bill_2025=7_210,            # owner record, rounded, last full year known
    a_assessed_2025=539_740,      # owner record, rounded, used to derive the effective rate
    a_water_lo=100 * 12,          # $100 a month
    a_water_hi=150 * 12,          # $150 a month
    a_power_lo=-20 * 12,          # a credit of $20 a month in the owner's good months
    a_power_hi=-10 * 12,          # a credit of $10 a month in the owner's typical months
    a_insurance=1_500,            # owner estimate; no quotation obtained
    # Property B - already owned; lived in; two of three units let.
    b_value_2026=1_800_000,
    b_assessed_2025=114_250,      # owner record, rounded
    b_bill_2025=2_440,            # owner record, rounded
    b_rent=7_150 * 12,            # $7,150 a month from two units
    b_water_lo=330 * 12,
    b_water_hi=400 * 12,
    b_power_lo=30 * 12,
    b_power_hi=70 * 12,
    b_insurance=1_500,            # owner estimate; no quotation obtained
)

# Owner property tax history, rounded to $10, used only to derive the effective rate band.
OWNER_HISTORY_A = [
    (2014, 5_970, 440_310), (2015, 6_130, 449_100), (2016, 6_410, 455_950),
    (2017, 6_380, 465_070), (2018, 6_380, 474_370), (2019, 6_570, 483_850),
    (2020, 6_570, 493_530), (2021, 6_660, 498_640), (2022, 6_760, 508_610),
    (2023, 6_920, 518_790), (2024, 7_000, 529_160), (2025, 7_210, 539_740),
]

# ------------------------------------------------------------------ verified constants

VERIFIED = dict(
    sf_secured_rate_2026_27=0.0118162182,   # sftreasurer_secured
    prop19_allowance=1_044_586,             # boe_lta2025_009
    estate_2026=15_000_000,                 # irs_estate_tax
    estate_2027=15_480_000,                 # irs_ir2026_133
    pl119_21=15_000_000,                    # irs_estate_faq (Public Law 119-21, 4 July 2025)
    niit=0.038,                             # irs_niit
    fed_top_2027=0.37,                      # irs_ir2026_133
    ca_top=0.123,                           # ftb_2025_rates
    ca_surcharge=0.01,                      # leginfo_rtc17043
    ltcg_top=0.20,                          # irs_tc409
    unrecaptured_1250=0.25,                 # irs_tc409
    prop13_factor=0.02,                     # boe_pub29
    prop13_ceiling=0.01,                    # boe_pub29
)

# ------------------------------------------------------------------------ assumptions

ASSUMPTIONS = dict(
    base_year=2026,
    transfer_year=2045,          # midpoint of the 2040-2050 window
    transfer_early=2040,
    transfer_late=2050,
    horizon=2076,
    price_growth=0.040,
    inflation=0.030,
    rent_growth=0.030,
    portfolio_return=0.070,
    portfolio_tax_drag=0.006,
    discount_rate=0.050,
    prop19_hpi=0.020,
    estate_index=0.025,
    vacancy=0.050,
    management=0.080,
    land_share=0.200,
    depreciation_years=27.5,
    selling_cost=0.060,
    maint_a=0.008,
    maint_b=0.012,
    rent_tax_rate=0.500,
    gross_yield_a=0.025,         # CLOSURE PARAMETER
)

ASSUMPTION_NOTES = [
    ("transfer_year", "2045",
     "The midpoint of the 2040-2050 window the owner gave. 2040 and 2050 are shown alongside it. "
     "The transfer year is the single biggest driver of the answer and cannot be known in advance."),
    ("horizon", "2076",
     "Fifty years from the base year, covering the owner's planning horizon and the step-up that "
     "would apply if the asset is still held at death."),
    ("price_growth", "4.0%",
     "A long-run nominal rate for California single-family housing, one point above general "
     "inflation. No official forecast exists, so every conclusion is restated as a break-even "
     "growth rate that does not require this number to be trusted."),
    ("inflation", "3.0%",
     "Set against the official record: the Bureau of Labor Statistics shows all items up 3.7% over "
     "the twelve months to September 2026 and the index at 337.511 in October 2026. The black-swan "
     "page replays real BLS inflation paths instead of this constant."),
    ("rent_growth", "3.0%",
     "Market rent assumed to track general inflation. The statewide cap in Civil Code 1947.12 "
     "(5% plus the cost-of-living change, or 10%, whichever is lower) only binds above 5% inflation."),
    ("portfolio_return", "7.0%",
     "A conventional nominal total return for a diversified equity-heavy portfolio. Not an official "
     "figure. Break-even returns are published so it can be tested directly."),
    ("portfolio_tax_drag", "0.6%",
     "Annual drag from dividends and realised gains. A constant annual reduction is a simplification "
     "of a graduated, path-dependent tax."),
    ("discount_rate", "5.0%",
     "The rate used to bring future dollars back to the transfer year. Deliberately below the "
     "portfolio return: the portfolio return is a risky expected return, the discount rate is a "
     "time preference."),
    ("prop19_hpi", "2.0%",
     "Indexation of the Proposition 19 allowance. The Board of Equalization adjusted it for a "
     "California house price index change of 2.15% for 2024. The allowance steps every two years, "
     "as the Constitution requires."),
    ("estate_index", "2.5%",
     "Indexation of the federal basic exclusion amount after 2027. The 2026 and 2027 amounts are "
     "official; the indexation rate is not, so projections beyond 2027 are projections."),
    ("vacancy", "5.0%",
     "Share of gross rent lost to vacancy on a single-family letting. No owner history was supplied."),
    ("management", "8.0%",
     "Share of collected rent paid to a managing agent. Set to zero in the sensitivity, because the "
     "owner already manages Property B."),
    ("land_share", "20.0%",
     "Land as a share of value; only the improvement share is depreciable. Chosen, not appraised."),
    ("depreciation_years", "27.5",
     "The federal straight-line recovery period for residential rental property."),
    ("selling_cost", "6.0%",
     "Commission, escrow, transfer charges and any city and county transfer tax on a sale."),
    ("maint_a / maint_b", "0.8% / 1.2% of value a year",
     "The owner supplied no maintenance figure. These are informed only by the owner's statement "
     "that Property A is lighter than Property B. Both are tested in the sensitivity grid."),
    ("rent_tax_rate", "50.0%",
     "A combined marginal rate on net rental income. The official components are 37% federal "
     "ordinary (IR-2026-133), 12.3% California (FTB 2025 schedule) plus the 1% surcharge over "
     "$1,000,000 (R&TC 17043), and 3.8% net investment income tax. The combined rate after "
     "deductions, the state and local tax cap and offsetting losses is not modelled, so 40% and "
     "60% are shown as well."),
    ("gross_yield_a", "2.5%",
     "CLOSURE PARAMETER, not an estimate. No rent figure for Property A was supplied. The model "
     "reports the break-even yield and a grid from 2.0% to 4.0% to compare against a real quote."),
]

# --------------------------------------------------------------------- derived rates

def effective_rate_a():
    """Property A's all-in property tax rate, derived only from the owner's own records."""
    return OWNER["a_bill_2025"] / OWNER["a_assessed_2025"]


def effective_rate_a_band():
    """(low, high, [(year, rate)]) across the owner's 2014-2025 records."""
    rates = [(y, b / a) for y, b, a in OWNER_HISTORY_A]
    return min(r for _, r in rates), max(r for _, r in rates), rates


def b_rate_residual():
    """
    Property B: the owner's bill less the official rate applied to the owner's assessed value.
    The residual is carried as a flat charge; parcel taxes, bonds and district levies are not
    ad valorem. Its composition is unknown, so it is flagged on the property tax page.
    """
    rate = VERIFIED["sf_secured_rate_2026_27"]
    adval = OWNER["b_assessed_2025"] * rate
    return OWNER["b_bill_2025"] - adval, adval


def b_unit_rent():
    """
    Rent for one unit of Property B, derived from the owner's $7,150 a month for two units,
    on the assumption the three units are comparable. Used because moving into Property A
    frees the third unit, and living in Property B consumes one. Owner-informed assumption.
    """
    return OWNER["b_rent"] / 2.0


# ------------------------------------------------------------------ statutory engines

def prop19_allowance(year, hpi=None):
    """
    The Proposition 19 intergenerational allowance in force on 1 January of `year`.

    $1,044,586 covers 16 Feb 2025 - 15 Feb 2027 (BOE LTA 2025/009). The next adjustment is
    February 2027 and every second February after that, so the first full year carrying an
    adjustment is 2028 and each adjustment carries two years of house price change.
    """
    hpi = ASSUMPTIONS["prop19_hpi"] if hpi is None else hpi
    base = VERIFIED["prop19_allowance"]
    if year < 2028:
        return base
    steps = (year - 2028) // 2 + 1
    return base * (1.0 + hpi) ** (2 * steps)


def estate_exemption(year, index=None):
    """Federal basic exclusion amount. 2026 and 2027 are official; beyond that it is indexed."""
    index = ASSUMPTIONS["estate_index"] if index is None else index
    if year <= 2026:
        return VERIFIED["estate_2026"]
    return VERIFIED["estate_2027"] * (1.0 + index) ** (year - 2027)


def estate_tax_on(gross, year, rate=0.40):
    """Tax on the amount above the exclusion. The 40% rate is statutory; the exclusion is keyed
    to the year of death, and the tax is charged to the estate, not to the heir."""
    return max(0.0, gross - estate_exemption(year)) * rate


# ---------------------------------------------------------------------- value engines

def value_path(v0, years, growth):
    """Nominal market value path. `growth` may be a number or a list of annual rates."""
    out = [v0]
    for i in range(years):
        g = growth[i] if isinstance(growth, (list, tuple)) else growth
        out.append(out[-1] * (1.0 + g))
    return out


def assessed_path(base_year_value, market_path, start_year, switch_year=None,
                  new_base=None, factor=None):
    """
    Proposition 13 trending with a Proposition 8 floor.

    Assessed value is the base year value trended at no more than 2% a year. If market value
    falls below that trend the assessor enrolls the lower market value (Proposition 8), and when
    the market recovers the assessed value rises with it until it meets the trend again.
    min(trend, market) reproduces both halves of that rule.
    """
    factor = VERIFIED["prop13_factor"] if factor is None else factor
    out = []
    trend = base_year_value
    for i, y in enumerate(range(start_year, start_year + len(market_path))):
        if i > 0:
            trend = trend * (1.0 + factor)
        if switch_year is not None and y == switch_year and new_base is not None:
            trend = new_base
        out.append(min(trend, market_path[i]))
    return out


def transfer_taxable_value(fbyv, market_at_transfer, allowance, claim_exclusion):
    """
    New taxable value on an intergenerational transfer.

    With the exclusion (Revenue and Taxation Code 63.2; BOE LTA 2026/026):
        value cap = factored base year value + allowance
        if market value <= cap, taxable value stays at the factored base year value
        otherwise taxable value = factored base year value + the excess,
        which is the same thing as market value less the allowance
    Without the exclusion the property is reassessed to its market value.
    """
    if claim_exclusion:
        cap = fbyv + allowance
        if market_at_transfer <= cap:
            return fbyv
        return fbyv + (market_at_transfer - cap)
    return market_at_transfer


# ------------------------------------------------------------------- operating costs

def _cpi_factor(years_out, inflation):
    if isinstance(inflation, (list, tuple)):
        return math.prod(1.0 + g for g in inflation[:years_out])
    return (1.0 + inflation) ** years_out


def opex_a(year, market_value, inflation, maint=None):
    """
    Property A running costs. Insurance and maintenance scale with value (rebuilding cost and
    fabric); water and power are metered and scale with general prices. Power is negative: the
    rooftop system normally produces a credit.
    """
    maint = ASSUMPTIONS["maint_a"] if maint is None else maint
    cpi = _cpi_factor(year - ASSUMPTIONS["base_year"], inflation)
    scale = market_value / OWNER["a_value_2026"]
    water = ((OWNER["a_water_lo"] + OWNER["a_water_hi"]) / 2.0) * cpi
    power = ((OWNER["a_power_lo"] + OWNER["a_power_hi"]) / 2.0) * cpi
    insurance = OWNER["a_insurance"] * scale
    maintenance = maint * market_value
    return dict(water=water, power=power, insurance=insurance, maintenance=maintenance,
                total=water + power + insurance + maintenance)


def opex_b(year, market_value, inflation, maint=None):
    maint = ASSUMPTIONS["maint_b"] if maint is None else maint
    cpi = _cpi_factor(year - ASSUMPTIONS["base_year"], inflation)
    scale = market_value / OWNER["b_value_2026"]
    water = ((OWNER["b_water_lo"] + OWNER["b_water_hi"]) / 2.0) * cpi
    power = ((OWNER["b_power_lo"] + OWNER["b_power_hi"]) / 2.0) * cpi
    insurance = OWNER["b_insurance"] * scale
    maintenance = maint * market_value
    return dict(water=water, power=power, insurance=insurance, maintenance=maintenance,
                total=water + power + insurance + maintenance)


# ------------------------------------------------------------------------- the model

def compare(transfer_year=None, horizon=None, price_growth=None, inflation=None,
            portfolio_return=None, gross_yield_a=None, rent_tax_rate=None,
            management=None, vacancy=None, maint_a=None, maint_b=None,
            discount_rate=None, selling_cost=None, tax_rate_override=None,
            lead_occupancy_years=0, count_b_unit=True):
    """
    Net present value, measured at the transfer year, of three ways to hold the home.

      occupy  move in within a year, claim the homeowner's exemption and the Proposition 19
              exclusion, live in the house, and let the third unit of Property B that you free
              by moving out
      rent    let the home. No exclusion is available, because the transferee does not occupy
              it, so the property is reassessed to its market value
      sell    sell at the transfer, invest the net proceeds, and hold the portfolio

    All three end with an asset that has NOT been sold at the horizon, so no option is penalised
    for a terminal capital gains tax that another avoids: if an asset is still held at death its
    basis is stepped up again, which is exactly the treatment assumed here.

    Two numbers are produced for each option:

      cash    money only. Imputed rent is excluded, because you cannot bank it.
      econ    money plus the market rent of the dwelling the household actually lives in.
              Living in your own home is untaxed; being paid rent is not. That asymmetry is
              real and it is why the two columns rank the options differently.

    The two units of Property B that are already let are common to all three options and are
    left out of all of them.
    """
    A = ASSUMPTIONS
    transfer_year = A["transfer_year"] if transfer_year is None else transfer_year
    horizon = A["horizon"] if horizon is None else horizon
    price_growth = A["price_growth"] if price_growth is None else price_growth
    inflation = A["inflation"] if inflation is None else inflation
    portfolio_return = A["portfolio_return"] if portfolio_return is None else portfolio_return
    gross_yield_a = A["gross_yield_a"] if gross_yield_a is None else gross_yield_a
    rent_tax_rate = A["rent_tax_rate"] if rent_tax_rate is None else rent_tax_rate
    management = A["management"] if management is None else management
    vacancy = A["vacancy"] if vacancy is None else vacancy
    maint_a = A["maint_a"] if maint_a is None else maint_a
    maint_b = A["maint_b"] if maint_b is None else maint_b
    discount_rate = A["discount_rate"] if discount_rate is None else discount_rate
    selling_cost = A["selling_cost"] if selling_cost is None else selling_cost

    rate_a = tax_rate_override if tax_rate_override is not None else effective_rate_a()
    base = A["base_year"]
    n_total = horizon - base

    market = value_path(OWNER["a_value_2026"], n_total, price_growth)      # 2026..horizon
    pre_market = market[:transfer_year - base + 1]
    pre_assessed = assessed_path(OWNER["a_assessed_2026"], pre_market, base)

    v_at_transfer = market[transfer_year - base]
    fbyv = pre_assessed[-1]
    allowance = prop19_allowance(transfer_year)
    taxable_excl = transfer_taxable_value(fbyv, v_at_transfer, allowance, True)
    taxable_full = transfer_taxable_value(fbyv, v_at_transfer, allowance, False)

    post_market = market[transfer_year - base:]

    if lead_occupancy_years:
        excl_part = assessed_path(taxable_excl, post_market[:lead_occupancy_years + 1],
                                  transfer_year)
        # On removal the new base year value established at the transfer - the market value at
        # that date - is enrolled, trended at 2% a year from the transfer date (LTA 2026/026 Q10).
        trended_new_base = v_at_transfer * (1.0 + VERIFIED["prop13_factor"]) ** lead_occupancy_years
        rest = assessed_path(trended_new_base, post_market[lead_occupancy_years:],
                             transfer_year + lead_occupancy_years)
        assessed_excl = excl_part + rest[1:]
    else:
        assessed_excl = assessed_path(taxable_excl, post_market, transfer_year)
    assessed_full = assessed_path(taxable_full, post_market, transfer_year)

    years_after = horizon - transfer_year
    d = discount_rate
    unit_b = b_unit_rent() if count_b_unit else 0.0
    fs = []

    # ---------------------------------------------------------------- OCCUPY
    basis = v_at_transfer
    npv_occ_cash = 0.0
    npv_occ_imputed = 0.0
    occ_rows = []
    for k in range(1, years_after + 1):
        y = transfer_year + k
        v = market[y - base]
        assessed = assessed_excl[k]
        tax = assessed * rate_a
        cost = opex_a(y, v, inflation, maint_a)["total"]
        rent_a = gross_yield_a * v                                  # housing consumed, untaxed
        extra = unit_b * _cpi_factor(y - base, inflation)           # third unit of B, taxable
        extra_after_tax = extra * (1.0 - rent_tax_rate)
        cash = extra_after_tax - tax - cost
        npv_occ_cash += cash / (1.0 + d) ** k
        npv_occ_imputed += rent_a / (1.0 + d) ** k
        occ_rows.append(dict(year=y, value=v, assessed=assessed, tax=tax, opex=cost,
                             rent=rent_a, extra=extra_after_tax, cash=cash))
    terminal_house = market[-1] / (1.0 + d) ** years_after
    npv_occ_cash += terminal_house

    # ------------------------------------------------------------------ RENT
    depreciable = basis * (1.0 - A["land_share"])
    annual_dep = depreciable / A["depreciation_years"]
    npv_rent_cash = 0.0
    npv_rent_imputed = 0.0
    rent_rows = []
    for k in range(1, years_after + 1):
        y = transfer_year + k
        v = market[y - base]
        assessed = assessed_full[k]
        tax = assessed * rate_a
        cost = opex_a(y, v, inflation, maint_a)["total"]
        gross = gross_yield_a * v
        collected = gross * (1.0 - vacancy)
        mgmt = collected * management
        noi = collected - mgmt - cost - tax
        taxable = noi - annual_dep
        cash_tax = max(0.0, taxable) * rent_tax_rate
        cash = noi - cash_tax
        npv_rent_cash += cash / (1.0 + d) ** k
        npv_rent_imputed += unit_b * _cpi_factor(y - base, inflation) / (1.0 + d) ** k
        rent_rows.append(dict(year=y, value=v, assessed=assessed, tax=tax, opex=cost,
                              gross=gross, noi=noi, dep=annual_dep, cashtax=cash_tax,
                              cash=cash))
    npv_rent_cash += terminal_house

    # ------------------------------------------------------------------ SELL
    # The proceeds are NOT added to the terminal value: the terminal value IS the proceeds
    # grown. Counting both would count the same money twice. What the option is worth is the
    # present value of the portfolio you end with, which is exactly parallel to the present
    # value of the house you end with in the other two options.
    proceeds = v_at_transfer * (1.0 - selling_cost)
    net_return = portfolio_return - A["portfolio_tax_drag"]
    portfolio_terminal = proceeds * (1.0 + net_return) ** years_after
    npv_sell_cash = portfolio_terminal / (1.0 + d) ** years_after
    npv_sell_imputed = npv_rent_imputed        # the household still lives in its own unit

    return dict(
        transfer_year=transfer_year, horizon=horizon, years_after=years_after,
        value_at_transfer=v_at_transfer, fbyv=fbyv, allowance=allowance,
        taxable_excluded=taxable_excl, taxable_reassessed=taxable_full,
        assessed_excluded=assessed_excl, assessed_reassessed=assessed_full,
        market=market, rate_a=rate_a, annual_dep=annual_dep, unit_b=unit_b,
        npv_occupy_cash=npv_occ_cash, npv_occupy_econ=npv_occ_cash + npv_occ_imputed,
        npv_rent_cash=npv_rent_cash, npv_rent_econ=npv_rent_cash + npv_rent_imputed,
        npv_sell_cash=npv_sell_cash, npv_sell_econ=npv_sell_cash + npv_sell_imputed,
        imputed_occupy=npv_occ_imputed, imputed_other=npv_sell_imputed,
        proceeds=proceeds, portfolio_terminal=portfolio_terminal,
        terminal_house_discounted=terminal_house,
        occ_rows=occ_rows, rent_rows=rent_rows,
    )


def gap(target, basis="econ", **kw):
    """Keeping minus selling, on the chosen basis."""
    r = compare(**kw)
    keep = r["npv_occupy_" + basis] if target == "occupy" else r["npv_rent_" + basis]
    return keep - r["npv_sell_" + basis]


def _bisect(fn, lo, hi, tol=1e-9, iters=200):
    flo, fhi = fn(lo), fn(hi)
    if flo is None or fhi is None or flo * fhi > 0:
        return None
    for _ in range(iters):
        mid = (lo + hi) / 2.0
        fmid = fn(mid)
        if fmid is None:
            return None
        if flo * fmid <= 0:
            hi, fhi = mid, fmid
        else:
            lo, flo = mid, fmid
        if hi - lo < tol:
            break
    return (lo + hi) / 2.0


def breakeven_gross_yield(target="occupy", basis="econ", **kw):
    """Gross rental yield on Property A at which keeping it equals selling it."""
    return _bisect(lambda y: gap(target, basis, gross_yield_a=y, **kw), 0.0001, 0.40)


def breakeven_portfolio_return(target="occupy", basis="econ", **kw):
    """Portfolio return at which selling equals keeping."""
    return _bisect(lambda r: gap(target, basis, portfolio_return=r, **kw), 0.0, 0.40)


def breakeven_price_growth(target="occupy", basis="econ", **kw):
    """House price growth at which keeping equals selling."""
    return _bisect(lambda g: gap(target, basis, price_growth=g, **kw), -0.08, 0.40)


def breakeven_tax_rate(target="occupy", basis="econ", **kw):
    """All-in property tax rate on Property A at which keeping equals selling."""
    return _bisect(lambda t: gap(target, basis, tax_rate_override=t, **kw), 0.0001, 0.25)


def breakeven_maint(target="occupy", basis="econ", **kw):
    """Maintenance rate (share of value a year) at which keeping equals selling."""
    return _bisect(lambda m: gap(target, basis, maint_a=m, **kw), 0.0, 0.20)


# ------------------------------------------------------------- black-swan machinery

REGIME_WINDOWS = [
    ("First World War inflation", 1916, 1920),
    ("Post-war deflation", 1920, 1922),
    ("Roaring Twenties stability", 1923, 1929),
    ("Great Depression deflation", 1929, 1933),
    ("Second World War inflation", 1941, 1946),
    ("Post-war inflation spike", 1946, 1948),
    ("Post-war normalisation", 1949, 1965),
    ("Vietnam-era build-up", 1966, 1972),
    ("The Great Inflation", 1973, 1982),
    ("Volcker disinflation", 1980, 1986),
    ("The Great Moderation", 1991, 2007),
    ("Global financial crisis", 2007, 2011),
    ("Post-crisis normalisation", 2012, 2020),
    ("Pandemic and energy shock", 2021, 2023),
    ("The current stretch", 2024, 2026),
]

# `inflation` is the measured BLS record over `anchor_years`. `real_house` and `real_equity`
# are ASSUMPTIONS about the other two series over the same window; no official long-run series
# for California house prices or equity returns was retrieved into this desk.
REGIMES = [
    dict(key="great_inflation", name="The Great Inflation", weight=1,
         anchor_years=(1973, 1982), inflation=None, real_house=-0.010, real_equity=-0.020,
         text=("Ten years of high, uneven inflation. Nominal house prices rise with the price "
               "level, so the Proposition 13 assessed value falls ever further behind market "
               "value, but every running cost rises too and the real value of the portfolio is "
               "cut. The regime that most rewards owning a real asset you can live in.")),
    dict(key="volcker", weight=1, name="Volcker disinflation",
         anchor_years=(1980, 1986), inflation=None, real_house=0.010, real_equity=0.045,
         text=("Inflation brought down fast while real returns on financial assets recover. "
               "Housing delivers little in real terms as the portfolio compounds.")),
    dict(key="great_moderation", weight=1, name="The Great Moderation",
         anchor_years=(1991, 2007), inflation=None, real_house=0.035, real_equity=0.070,
         text=("Steady inflation, strong real house price growth and strong equities. The regime "
               "the baseline case resembles most, and the one that flatters keeping the house.")),
    dict(key="gfc", weight=1, name="Global financial crisis",
         anchor_years=(2007, 2011), inflation=None, real_house=-0.060, real_equity=-0.030,
         text=("Nominal house prices fall. Proposition 8 cuts the assessed value to market value "
               "and the tax bill falls with it, cushioning the carry cost while the asset value "
               "drops at the same time.")),
    dict(key="pandemic", weight=1, name="Pandemic and energy shock",
         anchor_years=(2021, 2023), inflation=None, real_house=0.030, real_equity=0.010,
         text=("A sharp burst of inflation with house prices outrunning it. The Proposition 19 "
               "allowance is indexed to a house price index, so it rises quickly as well.")),
    dict(key="current", weight=1, name="The current stretch",
         anchor_years=(2024, 2026), inflation=None, real_house=0.005, real_equity=0.040,
         text=("All items up 3.7% over the twelve months to September 2026 on the official BLS "
               "measure, with energy up 20.4% and gasoline up 34.2%. Headline inflation near 3% "
               "and house prices roughly flat in real terms.")),
    dict(key="depression", weight=1, name="Deflation",
         anchor_years=(1929, 1933), inflation=None, real_house=-0.040, real_equity=-0.060,
         text=("Falling prices. Proposition 8 would cut the assessed value and the nominal rental "
               "stream shrinks every year, so the carry cost falls more slowly than income does.")),
    dict(key="stagflation_light", weight=1, name="Stagflation, mild and long",
         anchor_years=(1966, 1972), inflation=None, real_house=-0.005, real_equity=-0.010,
         text=("Inflation high enough to erode the portfolio with house prices flat in real terms. "
               "The worst combination for sell-and-reinvest and the least bad for holding a real "
               "asset you can live in.")),
    dict(key="japan", weight=0, name="Long stagnation",
         anchor_years=None, inflation=0.005, real_house=-0.015, real_equity=0.010,
         text=("A quarter century of near-zero inflation and gently falling real house prices. "
               "Not an American episode; included because it is the canonical case of a housing "
               "market that simply stops compounding. Both of its inputs are assumptions.")),
]

def by_key(key):
    """Look a named environment up in the regime table."""
    for r in REGIMES:
        if r["key"] == key:
            return r
    raise KeyError(key)


import cpi as _cpi  # noqa: E402  (module-local import keeps cpi.py optional elsewhere)


def _regime_inflation(regime):
    """Mean annual CPI-U inflation over the regime's window, inclusive of both end years."""
    if regime["anchor_years"] is None:
        return regime["inflation"]
    a, b = regime["anchor_years"]
    return _cpi.mean_over(a, b)


def block_bootstrap_inflation(block=5, length=50, seed=20261114, first=1914, last=2025):
    """
    Draw a realistic 50-year inflation path from the official BLS record.

    Independent draws from the historical distribution would jump from 14% to -10% and back
    with no memory, which is not how inflation behaves: it persists. Drawing contiguous
    five-year BLOCKS preserves that persistence, including the way a bad stretch runs for
    years before it turns. Only series CUUR0000SA0 (BLS) is used here.
    """
    history = [r for _, r in _cpi.series(first, last)]
    rng = random.Random(seed)
    starts = list(range(0, len(history) - block + 1))
    path = []
    while len(path) < length:
        s = rng.choice(starts)
        path.extend(history[s:s + block])
    return path[:length]


def monte_carlo(paths=1500, seed=20261114, block=5, target="occupy", basis="econ", **kw):
    """
    Replay the decision against block-bootstrapped real inflation combined with the regime
    assumptions, and report the distribution of (keeping - selling).

    The inflation path is sampled from the official record. Real house growth and real equity
    return are drawn from the regime table. Both are assumptions and the page says so: what
    the sampling buys is a realistic SHAPE for the inflation path, not a forecast.
    """
    rng = random.Random(seed + 7)
    real_house = [r["real_house"] for r in REGIMES]
    real_equity = [r["real_equity"] for r in REGIMES]
    A = ASSUMPTIONS
    transfer_year = kw.get("transfer_year", A["transfer_year"])
    length = kw.get("horizon", A["horizon"]) - transfer_year
    out = []
    for _ in range(paths):
        # A block carries one inflation stretch AND one growth regime together, so the
        # correlation between them survives: a high-inflation block is also a block in which
        # real equity and real house growth were poor. Sampling them independently would
        # destroy exactly the relationship the black-swan page exists to capture.
        pool = [r for r in REGIMES for _ in range(r.get("weight", 1))]
        house_nom, eq_nom, infl = [], [], []
        while len(infl) < length:
            pick_regime = pool[rng.randrange(len(pool))]
            stretch = block_bootstrap_inflation(block=block, length=block,
                                                seed=rng.randrange(10 ** 9))
            for g in stretch:
                house_nom.append((1 + g) * (1 + pick_regime["real_house"]) - 1)
                eq_nom.append((1 + g) * (1 + pick_regime["real_equity"]) - 1)
            infl.extend(stretch)
        house_nom, eq_nom, infl = house_nom[:length], eq_nom[:length], infl[:length]
        # The sampled path covers the years after the transfer; the years before it are
        # already history for the projection, so they keep the baseline growth rate.
        pre = transfer_year - A["base_year"]
        price_full = [A["price_growth"]] * pre + house_nom
        infl_full = [A["inflation"]] * pre + infl
        avg_eq = sum(eq_nom) / len(eq_nom)
        out.append(gap(target, basis, inflation=infl_full, price_growth=price_full,
                       portfolio_return=avg_eq, **kw))
    xs = sorted(out)

    def q(p):
        return xs[min(len(xs) - 1, max(0, int(round(p * (len(xs) - 1)))))]
    return dict(p05=q(0.05), p25=q(0.25), p50=q(0.50), p75=q(0.75), p95=q(0.95),
                mean=sum(xs) / len(xs),
                keep_wins=sum(1 for x in xs if x > 0) / len(xs), paths=paths)


_MC_CACHE = {}


def monte_carlo_cached(paths=1200, target="occupy", basis="econ", **kw):
    """monte_carlo() with a process-level memo, so several pages can share one run."""
    key = (paths, target, basis, tuple(sorted(kw.items())))
    if key not in _MC_CACHE:
        _MC_CACHE[key] = monte_carlo(paths=paths, target=target, basis=basis, **kw)
    return _MC_CACHE[key]


def regime_scenarios(basis="econ", **kw):
    """Deterministic run of each named regime, held constant across the whole horizon."""
    rows = []
    for r in REGIMES:
        infl = _regime_inflation(r)
        price = (1.0 + infl) * (1.0 + r["real_house"]) - 1.0
        eq = (1.0 + infl) * (1.0 + r["real_equity"]) - 1.0
        res = compare(price_growth=price, inflation=infl, portfolio_return=eq, **kw)
        rows.append(dict(
            regime=r, inflation=infl, price_growth=price, portfolio=eq,
            occupy=res["npv_occupy_" + basis], rent=res["npv_rent_" + basis],
            sell=res["npv_sell_" + basis],
            occ_gap=res["npv_occupy_" + basis] - res["npv_sell_" + basis],
            rent_gap=res["npv_rent_" + basis] - res["npv_sell_" + basis],
            tax_excluded=res["assessed_excluded"][1] * res["rate_a"],
            tax_full=res["assessed_reassessed"][1] * res["rate_a"],
        ))
    return rows


# ------------------------------------------------------------------ year-by-year grid

def projection_rows(**kw):
    """
    The main projection table: market value, assessed value and tax bill for both properties,
    with the reassessment at the transfer year, plus running costs and Property B rent.
    """
    A = ASSUMPTIONS
    transfer_year = kw.get("transfer_year", A["transfer_year"])
    horizon = kw.get("horizon", A["horizon"])
    price_growth = kw.get("price_growth", A["price_growth"])
    inflation = kw.get("inflation", A["inflation"])
    base = A["base_year"]
    n = horizon - base

    res = compare(transfer_year=transfer_year, horizon=horizon,
                  price_growth=price_growth, inflation=inflation)
    market_a = res["market"]
    pre_assessed = assessed_path(OWNER["a_assessed_2026"], market_a[:transfer_year - base + 1],
                                 base)

    market_b = value_path(OWNER["b_value_2026"], n, price_growth)
    b_start = OWNER["b_assessed_2025"] * (1.0 + VERIFIED["prop13_factor"])
    assessed_b = [OWNER["b_assessed_2025"]] + assessed_path(b_start, market_b[1:], base + 1)

    rate_a = res["rate_a"]
    residual, _ = b_rate_residual()
    rows = []
    for i, y in enumerate(range(base, horizon + 1)):
        cpi = _cpi_factor(y - base, inflation)
        if y < transfer_year:
            a_assessed = pre_assessed[i]
        elif y == transfer_year:
            a_assessed = res["taxable_excluded"]
        else:
            a_assessed = res["assessed_excluded"][y - transfer_year]
        a_tax = a_assessed * rate_a
        b_tax = assessed_b[i] * VERIFIED["sf_secured_rate_2026_27"] + residual * cpi
        rows.append(dict(
            year=y,
            a_value=market_a[i], a_assessed=a_assessed, a_tax=a_tax,
            a_cost=opex_a(y, market_a[i], inflation)["total"],
            b_value=market_b[i], b_assessed=assessed_b[i], b_tax=b_tax,
            b_cost=opex_b(y, market_b[i], inflation)["total"],
            b_rent=OWNER["b_rent"] * (1.0 + A["rent_growth"]) ** (y - base),
            transferred=(y >= transfer_year),
        ))
    return rows, res
