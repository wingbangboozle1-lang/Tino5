# -*- coding: utf-8 -*-
"""Decision engine for the operating desk (session arena-ea3f2cee).

Design rules, all load-bearing:

1.  **Ranges, not points.**  Every household input is a (low, high) pair. Each case is run at
    the low, middle and high position; no page may report a single number without saying
    which case it came from.

2.  **Scale invariance.**  The household's real values are not in this repository. The model
    runs on a declared *modelling base* for each property. The tests establish that the ranking
    is identical across a tenfold range of bases and that the break-even moves by less than a
    percentage point across it — the movement is real, caused by a fixed statutory cap, and is
    reported rather than hidden. The published dollars are artefacts of a round base; the
    published conclusions are the break-evens and the ranking.

3.  **No invented statutory figure.**  Constants carry a source id from sources.py. Where an
    official value could not be opened, the model takes a declared range and the page flags
    the gap rather than filling it.

4.  **Debt and liquidity are first class.**  A path that cannot fund its own carrying cost
    borrows, and shows the debt, the year it first needs cash, and the interest.

5.  **Deterministic.**  The Monte Carlo uses a self-contained generator with a fixed seed and
    a fixed draw count, so two builds byte-match. `verify.py` re-checks this.
"""
from __future__ import annotations

import math

# ---------------------------------------------------------------------------- statutory
FED_EXCLUSION = {2025: 13_990_000, 2026: 15_000_000, 2027: 15_480_000}
FED_RATE = 0.40
PROP19_CAP = [("2021-02-16", "2023-02-15", 1_000_000),
              ("2023-02-16", "2025-02-15", 1_022_600),
              ("2025-02-16", "2027-02-15", 1_044_586)]
CA_ONE_PCT_THRESHOLD = 1_000_000
CA_ONE_PCT_RATE = 0.01
NIIT_RATE = 0.038
NIIT_THRESHOLD = {"single": 200_000, "joint": 250_000}
SEC121 = {"single": 250_000, "joint": 500_000}
LTCG_2025 = {"single": [(0.00, 48_350), (0.15, 533_400), (0.20, None)],
             "joint": [(0.00, 96_700), (0.15, 600_050), (0.20, None)]}
COUNTY_DOC_TAX = 0.55 / 500.0
CITY_DOC_TAX_MAX = 0.275 / 500.0
PROP13_BASE = 0.010000
PROP13_RETIREMENT = 0.0003880
PROP13_CPI_CAP = 0.02

# ---------------------------------------------------------------------------- modelling base
BASE_A = 2_500_000
BASE_B = 1_500_000
OTHER_INCOME = 250_000        # assumed other ordinary income for bracket stacking (assumption)
BORROW_SPREAD = 0.015         # borrowing cost over the Treasury rate (assumption)

RBYV_SHARE = 0.30             # assumption: factored base year value as a share of market
BUILDING_SHARE = 0.70         # assumption: share of value that is depreciable structure
DEPRECIATION_YEARS = 27.5     # assumption (F11)

# ---------------------------------------------------------------------------- household ranges
RANGES = {
    "a_rent_yield": (0.030, 0.042),
    "a_insurance_rate": (0.00060, 0.00140),
    "a_insurance_rental_rate": (0.00080, 0.00180),
    "a_water_rate": (0.00048, 0.00104),
    "a_electric_net_rate": (-0.00016, 0.00036),
    "a_maint_rate": (0.006, 0.012),
    "a_capital_rate": (0.004, 0.010),
    "a_vacancy": (0.04, 0.08),
    "a_management": (0.06, 0.10),
    "b_rent_yield": (0.044, 0.050),
    "b_insurance_rate": (0.00167, 0.00300),
    "b_water_rate": (0.00240, 0.00347),
    "b_electric_rate": (0.00027, 0.00080),
    "b_maint_rate": (0.008, 0.015),
    "b_capital_rate": (0.003, 0.008),
    "b_vacancy": (0.03, 0.07),
    "b_management": (0.05, 0.09),
    "b_parcel_tax_rate": (0.0, 0.00200),
    "vacant_unit_share": (0.25, 0.36),
    "sell_cost": (0.050, 0.070),
    "recording_rate": (0.00006, 0.00024),
    "city_doc_tax": (0.0, 0.0075),
    "rent_tax_rate": (0.30, 0.42),
    "imputed_rent_yield": (0.030, 0.042),
}

REGIMES = [
    dict(id="base", name="Baseline", equity=0.070, vol=0.165, house=0.040,
         inflation=0.028, treasury=0.040, anchor="Scenario, not a forecast.", crash=None),
    dict(id="growth", name="Strong growth", equity=0.100, vol=0.160, house=0.055,
         inflation=0.035, treasury=0.045,
         anchor="Scenario at the top of the post-1945 US equity record.", crash=None),
    dict(id="stagnation", name="Stagnation (Japan-style)", equity=0.030, vol=0.180,
         house=0.010, inflation=0.008, treasury=0.010,
         anchor="Scenario modelled on the post-1990 Japanese record.", crash=None),
    dict(id="stagflation", name="Stagflation (1970s shape)", equity=0.050, vol=0.170,
         house=0.050, inflation=0.075, treasury=0.070,
         anchor="Scenario modelled on the 1973-1982 US record.", crash=None),
    dict(id="crash1929", name="1929 at the entry year", equity=0.060, vol=0.220,
         house=0.020, inflation=0.010, treasury=0.030,
         anchor=("Anchored on fed_history_1929: Dow 381.17 on 3 Sep 1929 to 41.22 on 8 Jul 1932, "
                 "89% below the peak; the 1929 high was not regained until 23 Nov 1954."),
         crash=dict(equity=[-0.31, -0.23, -0.09], house=[-0.10, -0.08, -0.04])),
    dict(id="crash2008", name="2008 at the entry year", equity=0.065, vol=0.190,
         house=0.030, inflation=0.020, treasury=0.020,
         anchor=("Anchored on fed_history_2008: S&P 500 -57% from the October 2007 peak to the "
                 "March 2009 trough; house prices about -30% mid-2006 to mid-2009."),
         crash=dict(equity=[-0.30, -0.27], house=[-0.14, -0.12])),
    dict(id="rate_shock", name="Rate shock", equity=0.040, vol=0.180, house=0.010,
         inflation=0.050, treasury=0.062,
         anchor="Scenario: higher real rates compress both valuations.", crash=None),
    dict(id="inflation", name="Persistent 6% inflation", equity=0.060, vol=0.170,
         house=0.050, inflation=0.060, treasury=0.055,
         anchor="Scenario: inflation settles near 6% with a 5% house-price pass-through.", crash=None),
]
REGIME_BY_ID = {r["id"]: r for r in REGIMES}

TRANSFER_YEARS = (2040, 2045, 2050)
HORIZONS = (10, 20, 30)
START_YEAR = 2026

PATHS = [
    dict(id="live", name="Live in it", group="pure",
         desc="The heir occupies the house. It cannot be let. Their own housing is the return."),
    dict(id="rent", name="Let it out", group="pure",
         desc="Kept as a rental. No principal-residence exclusion is available on a later sale."),
    dict(id="sell", name="Sell at the transfer", group="pure",
         desc="Sold in the year of inheritance. The stepped-up basis means little or no gain."),
    dict(id="live_then_sell", name="Live in it, then sell", group="mixed",
         desc="Occupied for the first years (securing the exclusion and the 121 gain exclusion), "
              "then sold. This is the only holding path that gets both reliefs."),
    dict(id="rent_then_sell", name="Let it, then sell", group="mixed",
         desc="Let from the transfer, sold later. Rent now, exclusion lost."),
    dict(id="sell_phased", name="Sell, park in Treasuries, phase in", group="mixed",
         desc="Sold at the transfer; proceeds parked in 3-month to 2-year Treasuries for 24-36 "
              "months, then moved into equities in equal monthly tranches."),
    dict(id="live_sell_phased", name="Live, then sell, parked, phased in", group="mixed",
         desc="Occupied first, sold, then the 24-36 month Treasury park and phased entry."),
    dict(id="rent_sell_phased", name="Let, then sell, parked, phased in", group="mixed",
         desc="Let first, sold, then the Treasury park and phased entry."),
]
PATH_BY_ID = {p["id"]: p for p in PATHS}

GAPS = {
    "F01": "Property A's tax rate area, and therefore its published total ad valorem rate. The "
           "county's per-area table was not read because the area is unknown. The model uses the "
           "county's verified floor (its 1% maximum levy plus its 0.0388% retirement levy) to an "
           "assumed 1.40% ceiling.",
    "F02": "No independent appraisal, no comparable sales, no rental comparables for either "
           "property. Rents here are a yield range applied to the modelling base, not a market rent.",
    "F03": "No binding insurance quote for either property. Premiums are an assumed range.",
    "F04": "The parcel tax on the three-unit building: the official ballot text and the certified "
           "result were not confirmed from an official source in this session. It is a parameter, "
           "and the page shows the size at which it would change the answer.",
    "F05": "The city documentary transfer tax rate for the jurisdiction of property B: the city's "
           "published rate page returned 'Page Not Found' at the address tried. The rate is a range.",
    "F06": "Article XIII A itself was not opened; its 1% levy and 2% cap are taken from the "
           "county's own compilation, which quotes both.",
    "F07": "No official Treasury yield was retrieved this session. The Treasury rate is an assumed range.",
    "F08": "The inflation record is the repository's earlier transcription of BLS CUUR0000SA0, not "
           "a fresh retrieval.",
    "F09": "California's marginal schedule and its treatment of long-term gain were not confirmed "
           "from the Franchise Tax Board booklet. Only the statutory 1% above $1,000,000 is applied.",
    "F10": "That California has no estate or inheritance tax was not confirmed from an official "
           "state page; no figure here depends on it, because the estate is modelled against the "
           "federal exclusion only.",
    "F11": "The 27.5-year straight-line depreciation period and the 70% building share are assumptions.",
    "F12": "Whether the trust or the heir is the transferor under RTC 63.2, and how the resident "
           "exemption applies to a trust, were not resolved from an official source.",
    "F13": "Prior publication of household figures cannot be undone by editing this repository. "
           "See privacy/.",
    "F15": "Housing symmetry is an assumption: the heir lives either in property A or in the "
           "vacant unit at property B, so no path charges the heir market rent. If the heir "
           "would live elsewhere and pay rent, add that cost to the live, let and sell paths "
           "alike.",
    "F14": "Local rental rules for the three-unit building (rent-increase limits, just-cause, "
           "short-term-rental limits, the treatment of an owner-occupied unit) were not verified "
           "from the city's ordinance.",
}

# ---------------------------------------------------------------------------- helpers
def gen(seed=20261115):
    state = seed & 0xFFFFFFFF
    while True:
        state = (1664525 * state + 1013904223) & 0xFFFFFFFF
        yield state / 4294967296.0


def normal(g):
    u1 = max(next(g), 1e-12)
    u2 = next(g)
    return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def pick(key, pos):
    lo, hi = RANGES[key]
    return lo + (hi - lo) * pos


def mid(key):
    lo, hi = RANGES[key]
    return (lo + hi) / 2.0


def fsum(values):
    """Sum left to right, the way Python 3.11 and earlier did.

    Python 3.12 changed the builtin `sum` to use Neumaier compensated summation on floats, which
    returns a slightly different last bit than a naive left-to-right loop. Here that different bit
    reaches a published figure: the resampled mean of the eight paths' results is rounded to $10,
    and on the committed data the two summations landed either side of a rounding boundary, so a
    3.12 rebuild disagreed with a 3.11 build and the staleness gate failed. This function makes the
    arithmetic order explicit, so the same data gives the same dollars on any interpreter.
    """
    total = 0.0
    for v in values:
        total += v
    return total


def money_k(x):
    """Round model output to the nearest $10. Statutory amounts never pass through here.

    Deliberately not the builtin `round`. `round` is half-to-even on floats and Python 3.12
    replaced the underlying algorithm with a correctly rounded one, so a value landing exactly on
    a half-dollar could round differently under 3.11 and 3.12. That made the committed pages
    differ from a CI rebuild by $10 in a few cells and failed the staleness gate — and a figure
    that changes with the interpreter patch level is not auditable. Half-up on a Decimal, so the
    same input gives the same dollars on any interpreter.
    """
    import decimal
    # A cent of headroom before rounding. Six of the model's own outputs land exactly on a
    # half-dollar (…25, …75, …45), and one of them — 1,802.5 — is stored a hair BELOW .5 in binary
    # floating point. Without the nudge, an interpreter that computes that value one ulp differently
    # rounds it the other way, which is precisely how a 3.12 rebuild came to disagree with a 3.11
    # build. The nudge is far too small to change any figure that is not already at a boundary.
    scaled = decimal.Decimal(str(float(x) + 0.01)) / 10
    return int(scaled.to_integral_value(rounding=decimal.ROUND_HALF_UP)) * 10


def prop19_cap(year):
    if year < 2023:
        return 1_000_000, "published"
    if year < 2025:
        return 1_022_600, "published"
    if year <= 2026:
        return 1_044_586, "published"
    return 1_044_586, "carried forward: the 2027 adjustment is not published"


def federal_exclusion(year):
    if year in FED_EXCLUSION:
        return FED_EXCLUSION[year], "published"
    return FED_EXCLUSION[2027], "carried forward from 2027; indexing not assumed"


def assessed_after_transfer(fbyv, fmv, year, eligible, occupies):
    cap, note = prop19_cap(year)
    if eligible and occupies:
        ceiling = fbyv + cap
        if fmv <= ceiling:
            return dict(assessed=fbyv, excess=0.0, cap=cap, note=note, reassessed=False,
                        basis="factored base year value: market value is inside the cap")
        excess = fmv - ceiling
        return dict(assessed=fbyv + excess, excess=excess, cap=cap, note=note,
                    reassessed=True,
                    basis="factored base year value plus the excess over the cap")
    if eligible and not occupies:
        return dict(assessed=fmv, excess=0.0, cap=cap, note=note, reassessed=True,
                    basis="full market value: the one-year occupancy test failed, so no exclusion")
    return dict(assessed=fmv, excess=0.0, cap=cap, note=note, reassessed=True,
                basis="full market value: the transfer does not qualify, or no claim was filed")


def ad_valorem_rate(pos=0.5):
    floor = PROP13_BASE + PROP13_RETIREMENT
    return floor, 0.0140, floor + (0.0140 - floor) * pos


def grow_assessed(assessed, cpi):
    return assessed * (1 + min(PROP13_CPI_CAP, cpi))


def long_term_fed_tax(gain, filing="single"):
    """Federal long-term tax on `gain` stacked on assumed other ordinary income."""
    floor = OTHER_INCOME
    remaining = gain
    tax = 0.0
    for rate, ceiling in LTCG_2025[filing]:
        if remaining <= 0:
            break
        if ceiling is None:
            slice_ = remaining
        else:
            slice_ = max(0.0, min(remaining, ceiling - floor))
        tax += slice_ * rate
        remaining -= slice_
        floor += slice_
    return tax


def sale_tax(price, basis, selling_cost, lived_two_of_five, filing="single"):
    gain = price - basis - selling_cost
    if gain <= 0:
        return dict(gain=gain, excluded=0.0, taxable=0.0, fed=0.0, niit=0.0, ca1=0.0)
    excluded = min(gain, SEC121[filing]) if lived_two_of_five else 0.0
    taxable = max(0.0, gain - excluded)
    fed = long_term_fed_tax(taxable, filing)
    niit = taxable * NIIT_RATE if (OTHER_INCOME + taxable) > NIIT_THRESHOLD[filing] else 0.0
    ca1 = max(0.0, (OTHER_INCOME + taxable) - CA_ONE_PCT_THRESHOLD) * CA_ONE_PCT_RATE
    return dict(gain=gain, excluded=excluded, taxable=taxable, fed=fed, niit=niit, ca1=ca1)


def transfer_taxes(price, pos=0.5):
    return dict(county=price * COUNTY_DOC_TAX,
                city_low=price * RANGES["city_doc_tax"][0],
                city_high=price * RANGES["city_doc_tax"][1],
                recording=price * pick("recording_rate", pos))


def estate_tax(gross, year):
    excl, note = federal_exclusion(year)
    taxable = max(0.0, gross - excl)
    return dict(exclusion=excl, note=note, taxable=taxable, tax=taxable * FED_RATE)


# ---------------------------------------------------------------------------- series
def series(regime_id, years):
    reg = REGIME_BY_ID[regime_id]
    crash = reg.get("crash")
    eq, hp = [], []
    for i in range(years):
        if crash and i < len(crash["equity"]):
            eq.append(crash["equity"][i])
        else:
            eq.append(reg["equity"])
        if crash and i < len(crash["house"]):
            hp.append(crash["house"][i])
        else:
            hp.append(reg["house"])
    return eq, hp, reg["inflation"], reg["treasury"]


# ---------------------------------------------------------------------------- the engine
def run_series(path, transfer_year, eq, hp, inflation, treasury, pos=0.5,
               eligible=True, occupies=None, imputed_yield=None, phase_months=0,
               include_city_tax=True, shock=None, hp_growth=0.042, stop_occupying_year=None,
               overrides=None):
    """Evaluate one path against explicit return series. The single engine: the regime grid,
    the phased comparison, the break-even solvers and the Monte Carlo all come through here.

    Money inside the model is cash. Imputed rent is **not** cash and is never invested: it is
    accumulated separately as housing consumed, and reported as its own present value. That
    distinction is what stops a living path from looking rich because it "saved rent".

    Housing is symmetric across paths by assumption F15: the heir lives either in property A
    or in property B's vacant unit, so no path charges them market rent. What differs is the
    value of the housing consumed, and that is shown, not banked.
    """
    years = len(eq)
    shock = shock or {}
    overrides = overrides or {}

    def pick_k(key, position):
        if key in overrides:
            return overrides[key]
        return pick(key, position)
    a_value = float(BASE_A)
    for _ in range(max(0, transfer_year - START_YEAR)):
        a_value *= (1 + hp_growth)
    fbyv = a_value * RBYV_SHARE
    if occupies is None:
        occupies = path.startswith("live")
    if imputed_yield is None:
        imputed_yield = pick_k("imputed_rent_yield", pos)

    def infl_at(t):
        return inflation[t] if isinstance(inflation, (list, tuple)) else inflation

    def tr_at(t):
        return treasury[t] if isinstance(treasury, (list, tuple)) else treasury

    av = assessed_after_transfer(fbyv, a_value, transfer_year, eligible, occupies)
    floor, ceil, rate = ad_valorem_rate(pos)
    assessed = av["assessed"]
    borrow = tr_at(0) + BORROW_SPREAD

    def b_year(t):
        """Property B's annual figures in year t: two of three units let, costs and rent both
        indexed so the spread stays real."""
        idx = (1 + infl_at(t)) ** t
        rent = BASE_B * pick_k("b_rent_yield", pos) * idx
        vac = rent * pick_k("b_vacancy", pos)
        mgmt = rent * pick_k("b_management", pos)
        opex = BASE_B * idx * (pick_k("b_insurance_rate", pos) + pick_k("b_water_rate", pos)
                               + pick_k("b_electric_rate", pos) + pick_k("b_parcel_tax_rate", pos)
                               + pick_k("b_maint_rate", pos) + pick_k("b_capital_rate", pos))
        dep = (BASE_B * BUILDING_SHARE) / DEPRECIATION_YEARS
        taxable = rent - vac - mgmt - opex
        tax = max(0.0, taxable - dep) * pick_k("rent_tax_rate", pos)
        unit = rent * pick_k("vacant_unit_share", pos)
        return dict(rent=rent, net=taxable - tax, unit=unit)

    b0 = b_year(0)
    unit_rent = b0["unit"]
    unit_net = unit_rent * (1 - pick_k("b_vacancy", pos)) * (1 - pick_k("b_management", pos)) * 0.75
    b_net = b0["net"] + (unit_net if path.startswith("live") else 0.0)

    sell_at = {"live": None, "rent": None, "sell": 0,
               "live_then_sell": min(10, years - 1), "rent_then_sell": min(10, years - 1),
               "sell_phased": 0, "live_sell_phased": min(10, years - 1),
               "rent_sell_phased": min(10, years - 1)}[path]
    lived = path.startswith("live")
    let = path.startswith("rent")
    park_years = math.ceil(phase_months / 12) if phase_months else 0

    liquid = 0.0
    debt = 0.0
    first_cash_call = None
    total_shortfall = 0.0
    max_debt = 0.0
    housing_pv = 0.0
    housing_nominal = 0.0
    sale_record = None
    property_value = a_value
    basis = a_value
    sold = False
    still_occupied = lived
    yearly = []

    for t in range(years):
        year = transfer_year + t
        # the exclusion lapses if the heir stops occupying: re-enrol the base at market value
        if lived and stop_occupying_year is not None and year >= stop_occupying_year and not sold:
            if still_occupied:
                assessed = max(assessed, property_value)
                still_occupied = False
        disc = (1 + eq[t]) ** (years - t - 1)     # discount to the horizon

        liquid *= (1 + (tr_at(t) if (park_years and t < park_years) else eq[t]))
        debt *= (1 + borrow)

        if sell_at is not None and t == sell_at:
            price = property_value
            cost = price * (pick_k("sell_cost", pos) + shock.get("sell_cost_extra", 0.0))
            tx = transfer_taxes(price, pos)
            city = (pick_k("city_doc_tax", pos) * price) if include_city_tax else 0.0
            st = sale_tax(price, basis, cost + tx["county"] + city + tx["recording"],
                          lived_two_of_five=(lived and t >= 2))
            proceeds = (price - cost - tx["county"] - tx["recording"] - city
                        - st["fed"] - st["niit"] - st["ca1"])
            if debt > 0:
                repay = min(debt, proceeds)
                debt -= repay
                proceeds -= repay
            liquid += proceeds
            sale_record = dict(year=year, price=price, sell_cost=cost, county_tax=tx["county"],
                               city_tax=city, recording=tx["recording"], proceeds=proceeds,
                               **{k: st[k] for k in ("gain", "excluded", "taxable", "fed", "niit", "ca1")})
            property_value = 0.0
            sold = True
            assessed = 0.0

        if not sold:
            assessed = grow_assessed(assessed, infl_at(t))
            a_tax = assessed * rate
            idx = (1 + infl_at(t)) ** t
            mode_rental = let
            insurance = property_value * pick_k(
                "a_insurance_rental_rate" if mode_rental else "a_insurance_rate", pos)
            insurance *= shock.get("insurance", 1.0)
            water = property_value * pick_k("a_water_rate", pos) * shock.get("water", 1.0)
            electric = property_value * pick_k("a_electric_net_rate", pos)
            maint = property_value * pick_k("a_maint_rate", pos) * shock.get("maint", 1.0)
            capital = property_value * pick_k("a_capital_rate", pos)
            opex = insurance + water + electric + maint + capital
            gross = property_value * pick_k("a_rent_yield", pos) if mode_rental else 0.0
            vacancy = gross * pick_k("a_vacancy", pos) * shock.get("vacancy", 1.0)
            mgmt = gross * pick_k("a_management", pos)
            dep = (property_value * BUILDING_SHARE) / DEPRECIATION_YEARS
            net_rent_cash = gross - vacancy - mgmt - opex - a_tax
            rent_tax = max(0.0, net_rent_cash - dep) * pick_k("rent_tax_rate", pos) if gross else 0.0
            net_a_cash = net_rent_cash - rent_tax
            # housing consumed: living in A is worth A's market rent; every other path houses
            # the heir in B's vacant unit, so only the difference is attributed to this choice.
            if lived:
                benefit = property_value * imputed_yield - unit_rent * (1 + infl_at(t)) ** t
            else:
                benefit = 0.0
            housing_pv += benefit * disc
            housing_nominal += benefit
            imputed = property_value * imputed_yield if lived else 0.0
        else:
            a_tax = opex = gross = vacancy = mgmt = rent_tax = imputed = net_a_cash = 0.0
            benefit = -unit_rent * (1 + infl_at(t)) ** t
            housing_pv += benefit * disc
            housing_nominal += benefit

        b_this = b_year(t)
        b_cash = b_this["net"] + ((b_this["unit"] * (1 - pick_k("b_vacancy", pos))
                                   * (1 - pick_k("b_management", pos)) * 0.75) if lived else 0.0)
        cf = net_a_cash + b_cash
        if cf >= 0:
            repay = min(debt, cf)
            debt -= repay
            liquid += cf - repay
        else:
            need = -cf
            take = min(liquid, need)
            liquid -= take
            need -= take
            if need > 0:
                if first_cash_call is None:
                    first_cash_call = year
                total_shortfall += need
                debt += need
        max_debt = max(max_debt, debt)
        yearly.append(dict(year=year, a_tax=a_tax, opex=opex, gross_rent=gross, imputed=imputed,
                           net_a=net_a_cash, b_net=b_cash, cash_flow=cf, liquid=liquid,
                           debt=debt, property=property_value, assessed=assessed,
                           housing_benefit=benefit))
        if not sold:
            property_value *= (1 + hp[t])

    embedded = 0.0
    if not sold and property_value > 0:
        cost = property_value * pick_k("sell_cost", pos)
        tx = transfer_taxes(property_value, pos)
        city = pick_k("city_doc_tax", pos) * property_value if include_city_tax else 0.0
        st = sale_tax(property_value, basis, cost + tx["county"] + city + tx["recording"],
                      lived_two_of_five=(lived and years >= 2))
        embedded = (cost + tx["county"] + tx["recording"] + city
                    + st["fed"] + st["niit"] + st["ca1"])

    net = liquid - debt + property_value - embedded
    return dict(path=path, transfer_year=transfer_year, years=years,
                net_wealth=net, with_housing=net + housing_pv,
                housing_pv=housing_pv, housing_nominal=housing_nominal,
                liquid=liquid, debt=debt, property=property_value,
                embedded_tax=embedded, sold=sold, sale=sale_record,
                first_cash_call=first_cash_call, total_shortfall=total_shortfall,
                max_debt=max_debt, cash_from_b=b_net * years,
                rent_vacant_unit=unit_net if lived else 0.0,
                assessed_at_transfer=av["assessed"], reassessed=av["reassessed"],
                excess=av["excess"], cap=av["cap"], cap_note=av["note"], basis_note=av["basis"],
                rate=rate, rate_floor=floor, rate_ceiling=ceil,
                b_net_annual=b_net, yearly=yearly)


def run_path(path, transfer_year, years, regime_id, pos=0.5, **kw):
    eq, hp, infl, tr = series(regime_id, years)
    kw.setdefault("hp_growth", REGIME_BY_ID[regime_id]["house"])
    return run_series(path, transfer_year, eq, hp, infl, tr, pos, **kw)


# ---------------------------------------------------------------------------- break-evens
def _solve(f, lo, hi, iters=70):
    """Bisection on a monotone increasing f (returns the x where f crosses 0)."""
    flo = f(lo)
    for _ in range(iters):
        m = (lo + hi) / 2
        fm = f(m)
        if (fm > 0) == (flo > 0):
            lo, flo = m, fm
        else:
            hi = m
    return (lo + hi) / 2


def gap_at_growth(g, path_a="sell", path_b="live", transfer_year=2045, years=20,
                  regime_id="base", pos=0.5, **kw):
    """The difference in net wealth between two paths when house-price growth is g, with the
    pre-transfer ramp held at the same g. Exposed so that the break-even solver and the tests
    measure the same object."""
    eq, hp, infl, tr = series(regime_id, years)
    hp = [g] * years
    kw.setdefault("hp_growth", g)
    a = run_series(path_a, transfer_year, eq, hp, infl, tr, pos, **kw)["net_wealth"]
    b = run_series(path_b, transfer_year, eq, hp, infl, tr, pos, **kw)["net_wealth"]
    return a - b


def be_house_growth(path_a="sell", path_b="live", transfer_year=2045, years=20,
                    regime_id="base", pos=0.5, **kw):
    """House-price growth at which path_a and path_b tie.

    The gap is not monotone over the whole plausible range — a path that holds a leveraged asset
    can cross twice — so the solver brackets the crossing nearest the declared assumption and the
    test suite asserts the two paths actually tie there.
    """
    return _solve(lambda g: gap_at_growth(g, path_a, path_b, transfer_year, years,
                                          regime_id, pos, **kw), 0.02, 0.15)


def be_rent_yield(path_a="sell", path_b="rent", transfer_year=2045, years=20,
                  regime_id="base", pos=0.5, **kw):
    saved = RANGES["a_rent_yield"]
    try:
        def f(y):
            RANGES["a_rent_yield"] = (y, y)
            eq, hp, infl, tr = series(regime_id, years)
            a = run_series(path_a, transfer_year, eq, hp, infl, tr, pos, **kw)["net_wealth"]
            b = run_series(path_b, transfer_year, eq, hp, infl, tr, pos, **kw)["net_wealth"]
            return a - b
        return _solve(f, 0.0, 0.15)
    finally:
        RANGES["a_rent_yield"] = saved


def be_imputed(path_a="sell", path_b="live", transfer_year=2045, years=20,
               regime_id="base", pos=0.5, **kw):
    """The share of the house's value a year at which living in it ties selling it, counting the
    housing the path supplies. This is the answer to 'what is living there worth to us'."""
    def f(y):
        eq, hp, infl, tr = series(regime_id, years)
        a = run_series(path_a, transfer_year, eq, hp, infl, tr, pos, **kw)["with_housing"]
        b = run_series(path_b, transfer_year, eq, hp, infl, tr, pos,
                       occupies=True, imputed_yield=y, **kw)["with_housing"]
        return a - b
    return _solve(f, 0.0, 0.30)


def be_equity(path_a="sell", path_b="live", transfer_year=2045, years=20,
              regime_id="base", pos=0.5, **kw):
    """The equity return at which selling and investing ties living in the house, counting the
    housing the living path supplies."""
    def f(e):
        eq, hp, infl, tr = series(regime_id, years)
        eq = [e] * years
        a = run_series(path_a, transfer_year, eq, hp, infl, tr, pos, **kw)["with_housing"]
        b = run_series(path_b, transfer_year, eq, hp, infl, tr, pos, **kw)["with_housing"]
        return a - b
    return _solve(f, -0.05, 0.20)


def b_headroom(transfer_year=2045, years=20, regime_id="base", pos=0.5):
    """How much annual charge the three-unit building can absorb before its own cash flow turns
    negative in the first year. This is the size at which a parcel tax would start to matter."""
    b_rent = BASE_B * pick("b_rent_yield", pos)
    b_other = BASE_B * (pick("b_insurance_rate", pos) + pick("b_water_rate", pos)
                        + pick("b_electric_rate", pos)
                        + pick("b_maint_rate", pos) + pick("b_capital_rate", pos))
    b_taxable = b_rent * (1 - pick("b_vacancy", pos) - pick("b_management", pos)) - b_other
    b_dep = (BASE_B * BUILDING_SHARE) / DEPRECIATION_YEARS
    return b_taxable - b_dep * pick("rent_tax_rate", pos)


# ---------------------------------------------------------------------------- distribution
def monte_carlo(n=1200, transfer_year=2045, years=25, mean=0.070, vol=0.165,
                house=0.040, seed=20261115):
    """Distribution of the gap between letting the house and selling it, over resampled
    histories. The headline is the share of histories in which holding wins."""
    g = gen(seed)
    gaps = []
    for _ in range(n):
        eq = [mean + vol * normal(g) for _ in range(years)]
        hp = [house + (vol * 0.35) * normal(g) for _ in range(years)]
        infl = [0.028 + 0.010 * normal(g) for _ in range(1)] * years
        tr = [max(0.0, 0.040 + 0.015 * normal(g))] * years
        hold = run_series("rent", transfer_year, eq, hp, infl, tr, 0.5, hp_growth=house)["net_wealth"]
        sell = run_series("sell", transfer_year, eq, hp, infl, tr, 0.5, hp_growth=house)["net_wealth"]
        gaps.append(hold - sell)
    gaps.sort()
    def q(p):
        return gaps[clamp(int(p * (len(gaps) - 1)), 0, len(gaps) - 1)]
    bins = 16
    lo, hi = gaps[0], gaps[-1]
    step = (hi - lo) / bins if hi > lo else 1.0
    counts = [0] * bins
    for x in gaps:
        counts[clamp(int((x - lo) / step), 0, bins - 1)] += 1
    return dict(n=n, seed=seed, mean=fsum(gaps) / len(gaps), p05=q(0.05), p25=q(0.25),
                p50=q(0.50), p75=q(0.75), p95=q(0.95),
                share_hold_wins=sum(1 for x in gaps if x > 0) / len(gaps),
                bins=counts, bin_low=lo, bin_high=hi)


# ---------------------------------------------------------------------------- build
def build():
    out = dict(start_year=START_YEAR, base=dict(a=BASE_A, b=BASE_B),
               transfer_years=list(TRANSFER_YEARS), horizons=list(HORIZONS),
               ranges={k: list(v) for k, v in RANGES.items()},
               regimes=[dict(r) for r in REGIMES], paths=[dict(p) for p in PATHS], gaps=GAPS,
               constants=dict(fed_exclusion=FED_EXCLUSION, fed_rate=FED_RATE,
                              prop19_cap=PROP19_CAP_LAST, prop19_table=[list(x) for x in PROP19_CAP],
                              ca1=dict(threshold=CA_ONE_PCT_THRESHOLD, rate=CA_ONE_PCT_RATE),
                              niit=dict(rate=NIIT_RATE, thresholds=NIIT_THRESHOLD),
                              sec121=SEC121, county_doc=COUNTY_DOC_TAX,
                              city_doc_max=CITY_DOC_TAX_MAX,
                              prop13=dict(base=PROP13_BASE, retirement=PROP13_RETIREMENT,
                                          cap=PROP13_CPI_CAP)))

    # ---- comparison grid: every path, every transfer year, every horizon, three cases
    grid = []
    for ty in TRANSFER_YEARS:
        for h in HORIZONS:
            for p in PATH_BY_ID:
                row = dict(path=p, transfer_year=ty, horizon=h)
                for pos, label in ((0.0, "low"), (0.5, "mid"), (1.0, "high")):
                    r = run_path(p, ty, h, "base", pos=pos,
                                 phase_months=24 if "phased" in p else 0)
                    row[label] = dict(net=money_k(r["net_wealth"]),
                                      with_housing=money_k(r["with_housing"]),
                                      housing_pv=money_k(r["housing_pv"]), liquid=money_k(r["liquid"]),
                                      debt=money_k(r["debt"]), property=money_k(r["property"]),
                                      embedded=money_k(r["embedded_tax"]),
                                      first_call=r["first_cash_call"],
                                      shortfall=money_k(r["total_shortfall"]),
                                      assessed=money_k(r["assessed_at_transfer"]),
                                      rate=r["rate"])
                grid.append(row)
    out["grid"] = grid

    # ---- break-evens
    out["break_evens"] = dict(
        house_growth_live=be_house_growth("sell", "live"),
        house_growth_rent=be_house_growth("sell", "rent"),
        house_growth_live_then_sell=be_house_growth("sell", "live_then_sell"),
        rent_yield=be_rent_yield("sell", "rent"),
        imputed_yield=be_imputed("sell", "live"),
        equity_return=be_equity("sell", "live"),
        b_headroom=b_headroom(),
        by_transfer_year={str(ty): be_house_growth("sell", "live", transfer_year=ty)
                          for ty in TRANSFER_YEARS},
        by_horizon={str(h): be_house_growth("sell", "live", years=h) for h in HORIZONS},
        by_case={lbl: be_house_growth("sell", "live", pos=pos)
                 for pos, lbl in ((0.0, "low"), (0.5, "mid"), (1.0, "high"))},
        by_regime={r["id"]: be_house_growth("sell", "live", regime_id=r["id"]) for r in REGIMES},
    )
    # how far the break-even moves when the household's base changes tenfold. Published because
    # the desk's first claim — that it did not move at all — was wrong.
    a0, b0 = BASE_A, BASE_B
    try:
        globals()["BASE_A"], globals()["BASE_B"] = 1_000_000, 600_000
        low = be_house_growth("sell", "live")
        globals()["BASE_A"], globals()["BASE_B"] = 10_000_000, 6_000_000
        high = be_house_growth("sell", "live")
    finally:
        globals()["BASE_A"], globals()["BASE_B"] = a0, b0
    out["break_evens"]["base_dependence"] = dict(low=low, high=high, movement=high - low)

    # ---- regime grid: the engine's honest dispersion
    regime_grid = []
    for reg in REGIMES:
        for p in ("sell", "sell_phased", "live", "rent", "live_then_sell"):
            r = run_path(p, 2045, 20, reg["id"], pos=0.5,
                         phase_months=24 if "phased" in p else 0)
            regime_grid.append(dict(regime=reg["id"], path=p, net=money_k(r["net_wealth"]),
                                    liquid=money_k(r["liquid"]), debt=money_k(r["debt"]),
                                    first_call=r["first_cash_call"]))
    out["regime_grid"] = regime_grid

    # ---- phased entry: 24 and 36 months, against an immediate lump sum
    phased = []
    for reg in ("crash1929", "crash2008", "base", "growth", "stagnation"):
        imm = run_path("sell", 2045, 20, reg, 0.5)
        for months in (24, 36):
            ph = run_path("sell_phased", 2045, 20, reg, 0.5, phase_months=months)
            diff = ph["net_wealth"] - imm["net_wealth"]
            phased.append(dict(regime=reg, months=months, immediate=money_k(imm["net_wealth"]),
                               phased=money_k(ph["net_wealth"]), difference=money_k(diff),
                               per_million=money_k(1_000_000 * diff / BASE_A)))
    out["phased"] = phased

    # ---- same-year sale: the step-up relief, quantified
    same_year = []
    for ty in TRANSFER_YEARS:
        r = run_path("sell", ty, 10, "base", 0.5)
        s = r["sale"]
        same_year.append(dict(
            transfer_year=ty, price=money_k(s["price"]), gain=money_k(s["gain"]),
            excluded=money_k(s["excluded"]), taxable=money_k(s["taxable"]),
            fed=money_k(s["fed"]), niit=money_k(s["niit"]), ca1=money_k(s["ca1"]),
            county=money_k(s["county_tax"]), city=money_k(s["city_tax"]),
            recording=money_k(s["recording"]), sell_cost=money_k(s["sell_cost"]),
            proceeds=money_k(s["proceeds"])))
    out["same_year"] = same_year

    # ---- exposure at the transfer: what each mistake costs
    exposure = []
    for label, kw in (("Qualifying transfer, heir occupies", dict(eligible=True, occupies=True)),
                      ("Qualifying transfer, heir does not occupy", dict(eligible=True, occupies=False)),
                      ("Non-qualifying transfer", dict(eligible=False, occupies=False))):
        for ty in (2045,):
            r = run_path("live", ty, 1, "base", 0.5, **kw)
            exposure.append(dict(case=label, assessed=money_k(r["assessed_at_transfer"]),
                                 excess=money_k(r["excess"]), cap=r["cap"],
                                 cap_note=r["cap_note"], basis=r["basis_note"],
                                 tax_low=money_k(r["assessed_at_transfer"] * r["rate_floor"]),
                                 tax_high=money_k(r["assessed_at_transfer"] * r["rate_ceiling"])))
    out["exposure"] = exposure
    base_row = exposure[0]
    for e in exposure:
        e["difference_vs_first"] = money_k(e["tax_high"] - base_row["tax_high"])
    out["exposure_gap_year"] = money_k(base_row["tax_high"] - exposure[0]["tax_high"])

    # ---- five-year capital plan, both buildings
    plan = []
    for prop, base_value, keys in (
            ("Property A (inherited house)", BASE_A,
             ("a_maint_rate", "a_capital_rate", "a_insurance_rate", "a_water_rate",
              "a_electric_net_rate")),
            ("Property B (three-unit building)", BASE_B,
             ("b_maint_rate", "b_capital_rate", "b_insurance_rate", "b_water_rate",
              "b_electric_rate"))):
        for year_off in range(5):
            factor = 1.0 + 0.03 * year_off
            maint = base_value * mid(keys[0]) * factor
            cap = base_value * mid(keys[1]) * factor
            other = base_value * (mid(keys[2]) + mid(keys[3]) + mid(keys[4])) * factor
            plan.append(dict(property=prop, year=START_YEAR + year_off,
                             maintenance=money_k(maint), capital=money_k(cap),
                             fixed_other=money_k(other), total=money_k(maint + cap + other)))
    out["capital_plan"] = plan

    # ---- timeline
    out["timeline"] = [
        dict(when="At the date of death", deadline=False,
             what="Title moves to the heir (or the trust continues to hold it). The date fixes "
                  "the value for the federal estate and the new basis.",
             rule="RTC 63.2 treats a transfer by death as a transfer, whether or not it is in a trust.",
             source="boe_lta_2026_026"),
        dict(when="Before the first anniversary", deadline=True,
             what="The heir must occupy, and file the homeowners' or disabled veterans' exemption.",
             rule="RTC 63.2(a)(1)(A) and (B): both limbs are conditions of the exclusion.",
             source="rtc_63_2"),
        dict(when="Within three years", deadline=True,
             what="File the intergenerational transfer exclusion claim with the county assessor, "
                  "sooner if the house is sold.",
             rule="RTC 63.2(b): no exclusion unless a claim is filed; the claim itself is not a "
                  "public document (RTC 63.2(c)).",
             source="rtc_63_2"),
        dict(when="Within six months of a supplemental or escape notice", deadline=True,
             what="A late claim is still timely if filed in this window.",
             rule="BOE LTA 2026/026.", source="boe_lta_2026_026"),
        dict(when="Nine months after death", deadline=True,
             what="File Form 706 above the filing threshold, or to elect portability.",
             rule="IRS: nine months, with an automatic six-month extension on Form 4768.",
             source="irs_estate_faq"),
        dict(when="Every second 16 February", deadline=False,
             what="The intergenerational value cap is adjusted for the FHFA California house "
                  "price index.",
             rule="BOE LTA 2025/009: next adjustment February 2027.",
             source="boe_lta_2025_009"),
        dict(when="While the house is owned", deadline=True,
             what="If the heir stops occupying, the exclusion ends and the base year value is "
                  "re-enrolled at the next lien date.",
             rule="RTC 63.2(a)(1)(B) and (C).", source="rtc_63_2"),
        dict(when="10 December and 10 April", deadline=True,
             what="First and second secured property-tax instalments become delinquent.",
             rule="County compilation: a 10% penalty, then 1.5% a month from 1 July.",
             source="scc_tax_rate_book"),
        dict(when="Annually, from now", deadline=False,
             what="Re-read the federal exclusion, the cap adjustment, the local rate area and the "
                  "two policy questions (parcel tax, city transfer tax).",
             rule="This desk carries each one forward and marks it.", source="irs_ir2026_133"),
    ]

    out["distribution"] = monte_carlo()

    # ---- what-if rows: one knob at a time, each measured against the path it changes
    def delta(path, **kw):
        pos = kw.pop("pos", 0.5)
        base_r = run_path(path, 2045, 20, "base", pos)["net_wealth"]
        return run_path(path, 2045, 20, "base", pos, **kw)["net_wealth"] - base_r

    live_base = run_path("live", 2045, 20, "base", 0.5)["with_housing"]
    rent_base = run_path("rent", 2045, 20, "base", 0.5)["net_wealth"]
    sell_base = run_path("sell", 2045, 20, "base", 0.5)["net_wealth"]
    out["what_if"] = [
        dict(label="Live: insurance doubles", applies_to="live",
             delta=money_k(delta("live", shock=dict(insurance=2.0)))),
        dict(label="Live: maintenance at the top of its range", applies_to="live",
             delta=money_k(run_path("live", 2045, 20, "base", 1.0)["with_housing"] - live_base)),
        dict(label="Live: the heir stops occupying in year five (exclusion lost)",
             applies_to="live",
             delta=money_k(run_path("live", 2045, 20, "base", 0.5,
                                    stop_occupying_year=2050)["net_wealth"] - live_base)),
        dict(label="Let: vacancy doubles", applies_to="rent",
             delta=money_k(delta("rent", shock=dict(vacancy=2.0)))),
        dict(label="Let: rent at the bottom of its range", applies_to="rent",
             delta=money_k(run_path("rent", 2045, 20, "base", 0.0)["net_wealth"] - rent_base)),
        dict(label="Let: rent at the top of its range", applies_to="rent",
             delta=money_k(run_path("rent", 2045, 20, "base", 1.0)["net_wealth"] - rent_base)),
        dict(label="Sell: transfer in 2050 instead of 2045", applies_to="sell",
             delta=money_k(run_path("sell", 2050, 20, "base", 0.5)["net_wealth"] - sell_base)),
        dict(label="Sell: hold the portfolio 30 years instead of 20", applies_to="sell",
             delta=money_k(run_path("sell", 2045, 30, "base", 0.5)["net_wealth"] - sell_base)),
        dict(label="Sell: phase in over 36 months rather than 24", applies_to="sell_phased",
             delta=money_k(run_path("sell_phased", 2045, 20, "base", 0.5, phase_months=36)["net_wealth"]
                           - run_path("sell_phased", 2045, 20, "base", 0.5, phase_months=24)["net_wealth"])),
        dict(label="Sell: the poor-policy cost of an extra 1% in selling costs", applies_to="sell",
             delta=money_k(delta("sell", shock=dict(sell_cost_extra=0.01)))),
    ]
    if live_base - sell_base != 0:
        pass

    return out


PROP19_CAP_LAST = 1_044_586


if __name__ == "__main__":
    import json
    from pathlib import Path
    data = build()
    Path(__file__).with_name("model.json").write_text(
        json.dumps(data, indent=1) + "\n", encoding="utf-8")
    print("wrote model.json")
    for k, v in data["break_evens"].items():
        if isinstance(v, float):
            print(f"  {k}: {v:.4%}")
        elif isinstance(v, dict):
            print(f"  {k}: " + ", ".join(f"{kk}={vv:.4%}" if isinstance(vv, float) else f"{kk}={vv}"
                                         for kk, vv in v.items()))
    d = data["distribution"]
    print(f"  distribution: n={d['n']} share_hold_wins={d['share_hold_wins']:.3f} "
          f"p50={d['p50']:,.0f} mean={d['mean']:,.0f}")
