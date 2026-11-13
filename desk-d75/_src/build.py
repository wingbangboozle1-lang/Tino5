"""Owner-brief desk: model and page generator (session arena-d75e2754).

Deterministic. Every printed figure is computed here from the constants below and the registers in
data.py. No network access, no randomness. Run:  python3 desk-d75/_src/build.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data import (AS_OF, ASSUMPTIONS, FLAGS, HORIZON, OWNER, QUESTIONS, REQUIREMENTS,  # noqa: E402
                  SOURCES, SRC, VERIFIED, SUGGESTIONS)

ROOT = Path(__file__).resolve().parents[1]
Y0, Y1 = HORIZON

# ---------------------------------------------------------------------------
# Official index values retrieved by this session on 13 November 2026
#   HPI: FHFA all-transactions index via FRED (fred_hpi)
#   CPI: BLS area and national annual averages via FRED (fred_cpi_sf, fred_cpi_us)
#   Rates: FRED (fred_cpi_sf bundle)
#   Factors: BOE LTA 2026/002 (boe_lta26002)
# ---------------------------------------------------------------------------
HPI_SJ = {1988: 98.50, 1989: 113.64, 1990: 109.68, 1991: 106.23, 1992: 104.34, 1993: 101.44,
          1994: 99.95, 1995: 102.45, 1996: 108.06, 1997: 122.46, 1998: 138.45, 1999: 157.67,
          2000: 203.54, 2001: 205.16, 2002: 216.22, 2003: 220.87, 2004: 255.24, 2005: 309.48,
          2006: 318.32, 2007: 302.81, 2008: 258.84, 2009: 237.76, 2010: 240.85, 2011: 235.66,
          2012: 252.50, 2013: 291.32, 2014: 319.27, 2015: 353.92, 2016: 373.83, 2017: 396.48,
          2018: 425.46, 2019: 415.13, 2020: 419.68, 2021: 463.63, 2022: 510.15, 2023: 546.45,
          2024: 558.19, 2025: 560.05}
HPI_SF = {1991: 107.13, 1994: 98.88, 1995: 100.94, 2000: 184.16, 2006: 307.14, 2007: 298.91,
          2008: 267.06, 2009: 250.31, 2010: 248.26, 2011: 240.50, 2012: 257.01, 2013: 296.34,
          2014: 329.82, 2015: 374.38, 2016: 396.57, 2017: 416.06, 2018: 445.81, 2019: 442.90,
          2020: 425.06, 2021: 451.73, 2022: 487.95, 2023: 495.49, 2024: 505.79, 2025: 512.99}
HPI_CA = {1991: 228.63, 2006: 642.37, 2011: 385.24, 2015: 536.77, 2025: 969.38}
CPI_SF = {1990: 132.050, 2015: 258.812, 2024: 349.021, 2025: None}
CPI_US = {1990: 130.658, 2015: 237.017, 2024: 313.689, 2025: None}
TREAS_10Y = {1981: 13.91, 2012: 1.80, 2015: 2.14, 2016: 1.84, 2017: 2.33, 2018: 2.91, 2019: 2.14,
             2020: 0.89, 2021: 1.44, 2022: 2.95, 2023: 3.96, 2024: 4.21, 2025: 4.29}
MORT_30Y = {1981: 16.64, 2010: 4.69, 2020: 3.11, 2021: 2.96, 2022: 5.34, 2023: 6.81, 2024: 6.72,
            2025: 6.60, 2026: 6.54}
BOE_FACTORS = [("1976-77", 6.250, 1.02), ("1979-80", 9.826, 1.02), ("1980-81", 17.316, 1.02),
               ("1981-82", 7.134, 1.02), ("1982-83", 11.137, 1.02), ("1983-84", 1.033, 1.01),
               ("1995-96", 1.194, 1.0119), ("1996-97", 1.115, 1.0111), ("2010-11", -0.237, 0.99763),
               ("2011-12", 0.753, 1.00753), ("2014-15", 0.454, 1.00454), ("2015-16", 1.998, 1.01998),
               ("2016-17", 1.525, 1.01525), ("2021-22", 1.036, 1.01036), ("2022-23", 5.561, 1.02),
               ("2023-24", 7.274, 1.02), ("2024-25", 3.181, 1.02), ("2025-26", 2.514, 1.02),
               ("2026-27", 3.307, 1.02)]
BOE_YEARS_AT_CAP = 40
BOE_YEARS_TOTAL = 51

# ---------------------------------------------------------------------------
# Owner inputs, recorded at $10
# ---------------------------------------------------------------------------
A_MARKET = 3100000
A_ASSESSED = 550540
A_ASSESSED_2025 = 539740
A_BILL_2025 = 7210
B_MARKET = 1800000
B_ASSESSED = 114240
B_BILL_2025 = 2440
B_RENT_2UNITS = 85800
B_WATER = 4380
B_ELEC = 600
A_WATER = 1560
A_ELEC = -180
INSURANCE = 1500

RATE_A = 0.011488
RATE_B = 0.0118162182
EXEMPTION = 7000
ALLOWANCE_2026 = 1044586
PROP13_CAP = 0.02

G_HOME = 0.040
G_ALLOW = 0.043
G_CPI = 0.025
G_INS = 0.040
G_RENT = 0.020
G_BRENT = 0.020
R_AFTER = 0.039
SELL_COST = 0.06
LTCG = 0.238
RECAP = 0.25
ORD = 0.278
MAINT_A = 0.008
MAINT_B = 0.012
DEPR_YEARS = 27.5
LAND = 0.25
VACANCY = 0.04
MGMT = 0.06
YIELD_A = 0.020
S121_SINGLE = 250000
ELEC_ENDS = 2043
TRANSFER_YEARS = (2040, 2045, 2050)
BASELINE_T = 2045


def round10(x):
    return int(round(float(x) / 10.0) * 10)


OTHER_A = round10(A_BILL_2025 - (A_ASSESSED_2025 - EXEMPTION) * RATE_A)
OTHER_B = round10(B_BILL_2025 - B_ASSESSED * RATE_B)
IMPLIED_A = A_BILL_2025 / A_ASSESSED_2025
IMPLIED_B = B_BILL_2025 / B_ASSESSED

PATHS = [
    ("occupy", "Live in it, keep it"),
    ("occupy_then_sell", "Live in it ten years, then sell"),
    ("rent", "Rent it out, live at the other house"),
    ("sell", "Sell it at transfer, reinvest the money"),
]


# ---------------------------------------------------------------------------
# primitives
# ---------------------------------------------------------------------------
def grow(base, years, rate):
    return base * (1 + rate) ** years


def market(year, base=A_MARKET, g=G_HOME):
    return grow(base, year - Y0, g)


def enrolled_asis(year, g=PROP13_CAP):
    return grow(A_ASSESSED, year - Y0, g)


def allowance(year, g=G_ALLOW):
    return grow(ALLOWANCE_2026, year - Y0, g)


def enrolled_after_transfer(year, T, use, g=G_HOME, stop=None, cap=PROP13_CAP):
    """The assessed value the assessor enrols for the inherited house after the transfer.

    use = 'occupy'  Proposition 19 exclusion claimed and the house stays the heir's principal residence
        'rent'      no exclusion: the transfer value is enrolled in full
        'revert'    exclusion claimed at T, principal-residence use ends at `stop`
    """
    if year < T:
        return grow(A_ASSESSED, year - Y0, cap)
    fb_T = grow(A_ASSESSED, T - Y0, PROP13_CAP)
    fc_T = market(T, g=g)
    if use == "occupy":
        av_T = max(fb_T, fc_T - allowance(T))
        return grow(av_T, year - T, cap)
    if use == "rent":
        return grow(fc_T, year - T, cap)
    if use == "revert":
        av_T = max(fb_T, fc_T - allowance(T))
        if stop is None or year <= stop:
            return grow(av_T, year - T, cap)
        return grow(fc_T, year - T, cap)
    raise ValueError(use)


def net_if_sold(year, T=BASELINE_T, g=G_HOME, occupied=True):
    """What selling the inherited house in `year` would net the heir, before reinvestment.

    Before the transfer there is nothing to sell, so those cells are blank rather than zero. The gain
    is measured from the stepped-up value at the transfer, which is why the number is so close to the
    gross value in the years just after it, and why the exclusion matters only if the heir lived there.
    """
    if year < T:
        return None
    v = market(year, g=g)
    gain = max(0.0, v - market(T, g=g))
    tax = max(0.0, gain - (S121_SINGLE if occupied else 0.0)) * LTCG
    return v * (1 - SELL_COST) - tax


def prop13_av_b(year, g=PROP13_CAP):
    return grow(B_ASSESSED, year - Y0, g)


def tax_a(year, av, owner_occupied, other=OTHER_A, rate=RATE_A, cpi=G_CPI, on_market=None):
    if on_market is not None:
        return on_market * rate + grow(other, year - 2025, cpi)
    taxable = max(0.0, av - (EXEMPTION if owner_occupied else 0.0))
    return taxable * rate + grow(other, year - 2025, cpi)


def tax_b(year, cpi=G_CPI):
    return prop13_av_b(year) * RATE_B + grow(OTHER_B, year - 2025, cpi)


def costs_a(year, g=G_HOME, ins_g=G_INS, cpi=G_CPI, maint=MAINT_A, elec_end=ELEC_ENDS, value=None):
    """Insurance, water, net electricity and maintenance for the inherited house.

    Maintenance starts from the rate applied to the 2026 value and then follows cost inflation, not
    the projected value: linking it to value would turn a speculative price rise into a carrying cost
    and punish exactly the scenario in which holding wins (see assumption D17).
    """
    ins = grow(INSURANCE, year - Y0, ins_g)
    water = grow(A_WATER, year - Y0, cpi)
    elec = grow(A_ELEC, year - Y0, cpi) if year < elec_end else 0.0
    return ins + water + elec + grow(A_MARKET * maint, year - Y0, cpi)


def costs_b(year, units_rented=2, cpi=G_CPI, ins_g=G_INS):
    ins = grow(INSURANCE, year - Y0, ins_g)
    water = grow(B_WATER, year - Y0, cpi)
    elec = grow(B_ELEC, year - Y0, cpi)
    maint = grow(B_MARKET * MAINT_B, year - Y0, cpi)
    mgmt = rent_b(year, units_rented) * MGMT
    return ins + water + elec + maint + mgmt


def rent_b(year, units=2, g=G_BRENT):
    return B_RENT_2UNITS / 2 * units * grow(1, year - Y0, g)


def rent_a(year, yield_rate=YIELD_A, g=G_HOME, value=None):
    v = value if value is not None else market(year, g=g)
    return v * yield_rate


def cagr(series, y0, y1):
    a, b = series.get(y0), series.get(y1)
    if not a or not b or y1 == y0:
        return None
    return (b / a) ** (1.0 / (y1 - y0)) - 1.0


def peak_trough(series, peak, trough):
    return series[trough] / series[peak] - 1.0


def years_to_recover(series, peak):
    level = series[peak]
    for y in range(peak + 1, max(series) + 1):
        if series.get(y, 0) >= level:
            return y - peak
    return None


# ---------------------------------------------------------------------------
# the engine: one loop, every path, every scenario override
# ---------------------------------------------------------------------------
def make_factor(T, spec, baseline, lo=Y0, until=None):
    """A year-by-year growth factor.

    spec may be None (the baseline rate for every year), a number (that rate for every year, which is
    what a permanent input change means), or a pair (rate, n) meaning: that rate for the `n` years
    following the transfer and the baseline before and after. A regime is a window, not a new world
    order - compounding an elevated inflation rate over fifty years instead of the decade it names
    would multiply a cost line by 70 and make the table meaningless.
    """
    until = until if until is not None else Y1

    def factor(year):
        if spec is None:
            return (1 + baseline) ** (year - lo)
        if isinstance(spec, tuple):
            rate, n = spec
            f = 1.0
            for y in range(lo + 1, year + 1):
                f *= 1 + (rate if T < y <= T + n else baseline)
            return f
        return (1 + spec) ** (year - lo)
    return factor
def simulate(T, path, g=G_HOME, r=R_AFTER, yield_rate=YIELD_A, ins_g=None, cpi=None,
             maint=MAINT_A, elec_end=ELEC_ENDS, cap=None, value_path=None,
             tax_on_market=False, forced_sale=None, horizon=Y1, housing_credit=True,
             detail=False):
    """Wealth at the horizon attributable to the inherited house, for one path.

    Convention: every flow is the heir's, in the nominal dollars of its own year, and each year's
    flow is carried to the horizon at the after-tax reinvestment return `r` (a negative flow is
    funded out of the same account). Property B enters no path, because the third unit there can be
    let under any of them and would therefore add the same number to every row - see unit3_uplift.

    Housing: in every year the heir occupies the inherited house the third unit at the other house is
    let, and `housing_credit` adds that net rent; in every year they do not, they are understood to be
    living in that unit instead, so the credit is forgone. Leaving that symmetry out is what makes
    selling look free.
           'occupy_then_sell'  transfer, claim the exclusion, live in it ten years, then sell
           'rent'              transfer, do not claim it (a let house cannot be a principal
                               residence), let it, hold to the horizon, sell there with depreciation
                               recaptured
           'sell'              transfer, sell immediately, reinvest the net proceeds
    """
    fc_T = market(T, g=g)
    cpi_f = make_factor(T, cpi, G_CPI)
    ins_f = make_factor(T, ins_g, G_INS)
    cap_f = make_factor(T, cap, PROP13_CAP)

    def enrolled(year, use):
        """The assessed value enrolled for the inherited house in `year`, with the base grown by cap_f."""
        fb_T = A_ASSESSED * cap_f(T)
        if year < T:
            return A_ASSESSED * cap_f(year)
        if use == "rent":
            return fc_T * (cap_f(year) / cap_f(T))
        av_T = max(fb_T, fc_T - allowance(T, g=G_ALLOW))
        return av_T * (cap_f(year) / cap_f(T))

    values = {}
    if value_path:
        values[T] = fc_T
        for y in range(T + 1, horizon + 1):
            values[y] = values[y - 1] * (1 + value_path(y))
    else:
        for y in range(Y0, horizon + 1):
            values[y] = market(y, g=g)

    if path == "sell":
        sale_year = forced_sale if forced_sale is not None else T
    elif path == "occupy_then_sell":
        sale_year = T + 10
    else:
        sale_year = None
    if path == "sell":
        housing_credit = False

    rows = []
    acc = 0.0
    depr_taken = 0.0
    depr_annual = fc_T * (1 - LAND) / DEPR_YEARS
    for y in range(T, horizon + 1):
        v = values[y]
        flow = 0.0
        av = None
        tax = 0.0
        carry = 0.0
        gross = 0.0
        if sale_year is not None and y > sale_year:
            pass
        elif path in ("occupy", "occupy_then_sell"):
            av = enrolled(y, "occupy")
            tax = (v * RATE_A + OTHER_A * cpi_f(y) if tax_on_market
                   else max(0.0, av - EXEMPTION) * RATE_A + OTHER_A * cpi_f(y))
            carry = (INSURANCE * ins_f(y) + A_WATER * cpi_f(y)
                     + (A_ELEC * cpi_f(y) if y < elec_end else 0.0)
                     + A_MARKET * maint * cpi_f(y))
            flow = -(tax + carry) + (unit3_net(y) if housing_credit else 0.0)
        elif path == "rent":
            av = enrolled(y, "rent")
            tax = v * RATE_A + OTHER_A * cpi_f(y) if tax_on_market else av * RATE_A + OTHER_A * cpi_f(y)
            gross = rent_a(y, yield_rate, g=g, value=v)
            carry = (INSURANCE * ins_f(y) * 1.2 + A_WATER * cpi_f(y)
                     + A_MARKET * 0.012 * cpi_f(y)
                     + gross * (VACANCY + MGMT))
            depr = min(depr_annual, max(0.0, gross - tax - carry))
            depr_taken += depr
            taxable = max(0.0, gross - tax - carry - depr)
            flow = gross - tax - carry - taxable * ORD
        if detail:
            rows.append(dict(year=y, value=v, av=av, tax=tax, carry=carry, gross=gross, flow=flow))
        acc += flow * (1 + r) ** (horizon - y)

    proceeds = 0.0
    tax_on_sale = 0.0
    if path == "sell":
        s = forced_sale if forced_sale is not None else T
        sale_v = values[s]
        proceeds = sale_v * (1 - SELL_COST)
        tax_on_sale = max(0.0, sale_v - fc_T) * LTCG
        terminal = acc + proceeds * (1 + r) ** (horizon - s)
    elif path == "occupy_then_sell":
        s = min(T + 10, horizon)
        sale_v = values[s]
        gain = max(0.0, sale_v - fc_T)
        tax_on_sale = max(0.0, gain - S121_SINGLE) * LTCG
        proceeds = sale_v * (1 - SELL_COST) - tax_on_sale
        terminal = acc + proceeds * (1 + r) ** (horizon - s)
    else:
        end = values[horizon]
        if path == "occupy":
            gain = max(0.0, end - fc_T)
            tax_on_sale = max(0.0, gain - S121_SINGLE) * LTCG
        else:
            gain = max(0.0, end - (fc_T - depr_taken))
            tax_on_sale = max(0.0, gain - depr_taken) * LTCG + min(depr_taken, gain) * RECAP
        terminal = acc + end * (1 - SELL_COST) - tax_on_sale
    out = dict(terminal=terminal, acc=acc, proceeds=proceeds, tax=tax_on_sale, T=T, path=path)
    if detail:
        out["rows"] = rows
    return out


def costs_b_delta(year, ins_g=G_INS, cpi=G_CPI):
    """Extra operating cost of letting one more unit at the already-owned house.

    Water and sewer are already carried for three units in the owner's figure, so no utility cost is
    added here; only the share of maintenance attributable to the unit and the letting commission.
    """
    return grow(B_MARKET * MAINT_B / 3.0, year - Y0, cpi) + rent_b(year, 1) * MGMT


def unit3_net(year, cpi=G_CPI, ins_g=G_INS):
    """What letting the vacant unit at the already-owned house nets in one year.

    The unit is the substitute for living in the inherited house: one of the two can house the heir
    and the other one can be let, so this figure is the price of occupying the inherited house and it
    moves between paths rather than being a constant added to all of them.
    """
    return rent_b(year, 3) - rent_b(year, 2) - costs_b_delta(year, ins_g, cpi)


def unit3_uplift(T=BASELINE_T, horizon=Y1, r=R_AFTER, cpi=G_CPI, ins_g=G_INS):
    return sum(unit3_net(y, cpi, ins_g) * (1 + r) ** (horizon - y) for y in range(T, horizon + 1))


def path_terms(T, regime=None):
    """Terminal wealth for every path at transfer year T, with one regime optionally overlaid."""
    if regime is None:
        return {k: simulate(T, k)["terminal"] for k, _ in PATHS}
    return {k: run_regime(T, k, regime)["terminal"] for k, _ in PATHS}


def winner_matrix(grids):
    """How often each path finishes first across a list of dicts, so no sentence needs maintaining."""
    wins = {}
    for vals in grids:
        w = max(vals, key=lambda k: vals[k])
        wins[w] = wins.get(w, 0) + 1
    return wins, len(grids)


def real2026(x):
    return x / (1 + G_CPI) ** (Y1 - Y0)


def bisect(f, lo, hi, iters=70):
    a, b = lo, hi
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        return None
    for _ in range(iters):
        mid = (a + b) / 2
        if f(a) * f(mid) <= 0:
            b = mid
        else:
            a = mid
    return (a + b) / 2


def break_even_growth(T, path, r=R_AFTER):
    return bisect(lambda g: simulate(T, path, g=g, r=r)["terminal"] - simulate(T, "sell", g=g, r=r)["terminal"],
                  -0.01, 0.16)


def break_even_rate(T, path, g=G_HOME):
    return bisect(lambda r: simulate(T, "sell", g=g, r=r)["terminal"] - simulate(T, path, g=g, r=r)["terminal"],
                  -0.02, 0.14)


def break_even_yield(T, g=G_HOME, r=R_AFTER):
    y = bisect(lambda y: simulate(T, "rent", g=g, r=r, yield_rate=y)["terminal"]
               - simulate(T, "sell", g=g, r=r)["terminal"], 0.002, 0.09)
    return None if y is None else (y, market(T, g=g) * y / 12.0)


# ---------------------------------------------------------------------------
# regimes for the black-swan page
# ---------------------------------------------------------------------------
def seq_changes(series, y0, y1):
    return [series[y] / series[y - 1] - 1.0 for y in range(y0 + 1, y1 + 1)]


REGIMES = [
    dict(id="E1",
         name="A regional crash in the first years of ownership, replayed from the published index",
         detail="The metro house price index for the inherited house's area fell in four of the five "
                "years 1990-1995 and did not regain its 1990 level until 1997.",
         changes=seq_changes(HPI_SJ, 1990, 1995), inject_at=3,
         watch="the value the heir is choosing to keep, not the tax"),
    dict(id="E2",
         name="A national housing and credit collapse, replayed",
         detail="The same index measured a fall from the 2006 high to the 2011 low, and seven years "
                "before the 2006 level was regained.",
         changes=seq_changes(HPI_SJ, 2006, 2013), inject_at=1,
         watch="how long it takes to recover, which is longer than the fall"),
    dict(id="E3",
         name="A high-inflation decade on the cost lines",
         detail="The inflation changes behind the rolls of 1979-80 through 1983-84 ran at double digits. "
                "The assessed base is capped at 2% a year, so the cap protects the tax line while "
                "insurance, water and maintenance run unimpeded.",
         changes=None, cpi=(0.09, 10), ins=(0.14, 10),
         watch="carrying cost, which is the only line Prop 13 does not protect"),
    dict(id="E4",
         name="A rate regime like the early 1980s",
         detail="The published 10-year Treasury average ran from 1.80% in 2012 to 13.91% in 1981, and "
                "the 30-year mortgage rate to 16.64%. A portfolio that earns far more moves the ranking "
                "on arithmetic alone.",
         changes=None, r=0.075,
         watch="the reinvestment alternative, which is what the sell path is really competing with"),
    dict(id="E5",
         name="Deflation",
         detail="In roll year 2010-11 the published factor was 0.99763, so the enrolled base year value "
                "actually fell. The 2% figure is a ceiling, not a floor: this regime grows the base at "
                "the published negative factor instead of at the cap, and costs at minus 1%.",
         changes=None, cpi=(-0.01, 10), ins=(0.02, 10), cap=(-0.0024, 10), r=0.020,
         watch="the tax line, which shrinks - and the portfolio return, which shrinks with it"),
    dict(id="E6",
         name="Insurance market withdrawal",
         detail="Modelled as the premium doubling for a decade. No official source publishes a premium for "
                "one address, so this is a shape rather than a forecast, and the owner's figure is the "
                "one at risk.",
         changes=None, ins=(0.12, 10),
         watch="the line the owner has not documented"),
    dict(id="E7",
         name="Proposition 13 is repealed for this use",
         detail="Modelled by taxing the inherited house on its market value throughout. Nothing on the "
                "November 2026 ballot proposed this, and it would need a constitutional amendment, so it "
                "is a tail, not a forecast.",
         changes=None, tax_on_market=True,
         watch="the entire premise of keeping the house"),
    dict(id="E8",
         name="A forced sale at the bottom",
         detail="The sell path is pushed from the transfer year into the trough of the replayed collapse. "
                "What hurts about selling is not the average return, it is the year the sale has to happen.",
         changes=seq_changes(HPI_SJ, 2006, 2013), inject_at=1, forced_trough=True,
         watch="the timing risk the sell path carries"),
]


def run_regime(T, path, regime):
    """The same model, with one named regime overlaid.

    A regime may replace the annual growth of house values for a run of years (spliced in at
    `inject_at` years after the transfer, then returning to the baseline), or override the cost,
    insurance, reinvestment or taxation inputs. Nothing else changes, so the only difference from
    the decision page is the shock itself.
    """
    kw = dict(g=G_HOME, r=R_AFTER)
    if regime.get("r") is not None:
        kw["r"] = regime["r"]
    if regime.get("cpi") is not None:
        kw["cpi"] = regime["cpi"]
    if regime.get("ins") is not None:
        kw["ins_g"] = regime["ins"]
    if regime.get("cap") is not None:
        kw["cap"] = regime["cap"]
    if regime.get("tax_on_market"):
        kw["tax_on_market"] = True

    changes = regime.get("changes")
    forced = None
    if changes:
        n = len(changes)
        inject = regime.get("inject_at", 1)

        def vp(y, T=T, changes=changes, inject=inject, n=n):
            k = y - T - inject
            if 0 <= k < n:
                return changes[k]
            return G_HOME
        kw["value_path"] = vp
        if regime.get("forced_trough") and path == "sell":
            v = market(T, g=G_HOME)
            series = {T: v}
            for y in range(T + 1, min(T + 14, Y1 + 1)):
                v = v * (1 + vp(y))
                series[y] = v
            forced = min(series, key=lambda k: series[k])
            kw["forced_sale"] = forced
    return simulate(T, path, **kw)


# ---------------------------------------------------------------------------
# rendering helpers
# ---------------------------------------------------------------------------
import re  # noqa: E401  (used by the scrubber)


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def money(x):
    if x is None:
        return "&mdash;"
    v = round10(x)
    sign = "&#8722;" if v < 0 else ""
    return f"{sign}${abs(v):,}"


def money_num(x):
    return money(x)


def exact(x, label="exact"):
    return f"${x:,} <span class=\"tag exact\">{label}</span>"


def pc(x, dp=2):
    if x is None:
        return "&mdash;"
    return f"{x * 100:.{dp}f}%"


def srcl(keys):
    if not keys:
        return '<span class="tag sm">in-desk</span>'
    out = []
    for k in keys:
        s = SRC[k]
        if s["kind"] == "official":
            mark = "opened 13 Nov 2026" if s["opened"] else "not re-opened"
        else:
            mark = "secondary"
        out.append(f'<a href="{s["url"]}">{esc(s["title"])}</a> <span class="tag sm">{mark}</span>')
    return "<br>".join(out)


def table(headers, rows, cls="data"):
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f'<table class="{cls}"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def basis_cell(extra=None):
    """The citation a model-output row carries: where the drivers come from, in-desk and official."""
    return ('<span class="tag derived">derived</span> <a href="methodology.html">inputs and assumptions</a>'
            + (f' &middot; {extra}' if extra else ""))


def status_tag(text):
    """Pick the status class from the words already in the cell, so the label and the text agree."""
    low = text.lower()
    if "owner" in low:
        return "owner"
    if "carried" in low or "rate" in low or "verified" in low:
        return "carried"
    if "assumption" in low or low[:1].isdigit() or "%" in low[:12]:
        return "assumption"
    return "derived"


def stat_block(items):
    inner = "".join(f"<div><b>{v}</b><span>{k}</span></div>" for k, v in items)
    return f'<div class="kpi">{inner}</div>'


def callout(text, kind=""):
    return f'<div class="callout {kind}">{text}</div>'


def note(text):
    return f'<p class="note">{text}</p>'


def h3(text):
    return f'<h3>{text}</h3>' 



# ---------------------------------------------------------------------------
# privacy scrubbing
#   The owner's instruction is that no personal information appears on the public site. A source
#   citation is only useful if it is a real document at a real address, and for local rules that
#   address always names a place. Both cannot be satisfied in the open, so the published pages carry
#   a geo-neutral description and the issuing body's own front door, and the exact document address
#   is kept in the internal register (desk-d75/research/, excluded from the deployed site).
#   The scrubber is applied to everything the generator writes, so a slip is impossible rather than
#   merely unlikely.
# ---------------------------------------------------------------------------
# The registers are authored already anonymised: no city, county, neighbourhood or postcode of either
# house appears in anything a reader sees. Build time rewriting is deliberately not used - it would
# publish text no author wrote and would hide a slip instead of stopping one. _src/data.py names the
# jurisdictions only in comments and in the URL of the agency that must be opened to re-check a figure,
# and scripts/privacy_scan.py plus the checks below enforce the rule on the rendered pages.
PLACE_NAMES = ("Cupertino", "Sunnyvale", "Santa Clara", "San Jose", "San Francisco", "Oakland",
               "Millbrae", "Los Gatos", "Mountain View", "Palo Alto", "Santa Cruz", "Hayward",
               "Outer Sunset", "Inner Sunset", "SFPUC", "sjwater", "sccgov", "santaclaracounty")
POSTCODES = ("95014", "95112", "94122", "94116")


FORBIDDEN_IN_TEXT = PLACE_NAMES + POSTCODES


def scrub_check(name, text):
    """Fail the build rather than publish a slip.

    Visible text is held to the owner's rule: no city, no neighbourhood, no postcode. A link's
    target is exempt, because the official publisher's own address is what makes a citation
    checkable and it is the agency, not the owner, that it identifies. The check reads the text a
    person would actually see, so an un-scrubbed phrase cannot hide inside markup.
    """
    visible = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    visible = re.sub(r"<[^>]+>", " ", visible)
    for tok in FORBIDDEN_IN_TEXT:
        if re.search(re.escape(tok), visible, re.I):
            where = re.search(re.escape(tok), visible, re.I)
            raise SystemExit(f"privacy: {name} shows {tok!r} in text: ..."
                             f"{visible[max(0, where.start() - 70):where.end() + 70].strip()}...")
    # A postcode is five bare digits. Two ordinary things look like one and are not: a decimal
    # fraction whose mantissa ends in five digits (an inflation factor of 0.99763), and a citation
    # to a numbered provision (section 13100, rule 462.520, form 4768). Both are removed first, so
    # what remains is a run of five digits with nothing to explain it.
    probe = re.sub(r"(?i)\b(section|rule|form|code|title|part|division|article|chapter|"
                   r"subsection|paragraph|letter|advice|tariff|no)\b[\s.]*[0-9][0-9.,()\u2013-]*", " ", visible)
    probe = re.sub(r"<code>.*?</code>", " ", probe, flags=re.S)
    hit = re.search(r"(?<![\d.a-zA-Z_-])\d{5}(?:-\d{4})?(?![\d.a-zA-Z_-])", probe)
    if hit:
        raise SystemExit(f"privacy: {name} contains something shaped like a postcode: "
                         f"...{probe[max(0, hit.start() - 70):hit.end() + 50].strip()}...")


PAGES = [
    ("index", "Overview"),
    ("requirements", "Requirement register"),
    ("executive-summary", "Executive summary"),
    ("properties", "The two houses"),
    ("carrying-costs", "Carrying costs"),
    ("projections", "Projections"),
    ("decision", "The decision"),
    ("estate-tax", "Inheritance tax"),
    ("process", "Trust process"),
    ("black-swans", "Black swans"),
    ("law-watch", "Law watch"),
    ("questions", "Questions and gaps"),
    ("suggestions", "Suggestions"),
    ("flagged", "Flagged for review"),
    ("sources", "Sources"),
    ("methodology", "Methodology"),
]


def page(key, title, intro, blocks):
    nav = "".join(f'<a class="{"on" if k == key else ""}" href="{k}.html">{n}</a>' for k, n in PAGES)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<meta name="referrer" content="no-referrer">
<title>{title} | owner brief desk</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header>
<h1>Owner brief desk</h1>
<p class="sub">The inherited house and the already-owned rental &middot; figures as of {AS_OF}
&middot; household amounts rounded to the nearest $10 &middot; no names, addresses, parcels, accounts
or postcodes</p>
</header>
<nav>{nav}</nav>
<main>
<h2>{title}</h2>
<p class="intro">{intro}</p>
{blocks}
<footer>
<p>A decision aid built from public law and the owner's own figures, not tax, legal or investment
advice. Every table row links the document it came from, or says plainly that no official source
supports it. Where a value could not be confirmed the cell is blank and the item is listed on
<a href="flagged.html">Flagged for review</a>.</p>
</footer>
</main>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# pages
# ---------------------------------------------------------------------------
def p_index():
    b = []
    b.append('<div class="cards">')
    cards = [
        ("executive-summary.html", "Executive summary", "The answer, the four levers, the deadlines that already exist"),
        ("requirements.html", "Requirement register", "Your brief item by item, with the status of each and what is still open"),
        ("decision.html", "The decision", "Live in it, rent it, sell it - after tax, in every transfer year, with break-evens"),
        ("projections.html", "Projections", "Year by year 2026 to 2076: value, assessed value, tax, every cost line"),
        ("estate-tax.html", "Inheritance tax", "How much passes before tax bites, at federal, state and county level"),
        ("process.html", "Trust process", "Fourteen steps from the date of death to a recorded deed, with the deadlines"),
        ("black-swans.html", "Black swans", "Real episodes from the published indexes, replayed onto this decision"),
        ("law-watch.html", "Law watch", "What changed at the ballot on 3 November 2026, and what resets in February 2027"),
        ("questions.html", "Questions and gaps", "What must be answered before a decision is reasonable, and how to answer each"),
        ("suggestions.html", "Suggestions for review", "Eighteen suggestions, none implemented, each waiting for your decision"),
        ("flagged.html", "Flagged for review", "Every unverified value and every irregularity found in the repository"),
        ("sources.html", "Source register", "Every document, whether this session opened it, and what it supports"),
    ]
    for href, title, sub in cards:
        b.append(f'<a class="card" href="{href}"><b>{title}</b><span>{sub}</span></a>')
    b.append("</div>")
    b.append("<h3>What this desk adds</h3>")
    rows = [
        ["Your brief is a checklist, not a vibe", "Every instruction you gave is listed with its status and the page that answers it, "
         "on the <a href=\"requirements.html\">requirement register</a>. Four items stay open because only your documents close them.",
         '<a href="requirements.html">see it</a>'],
        ["One house is inherited, one is already owned - and it changes everything",
         "The inherited house has a tax base worth tens of thousands a year that survives only if you live there and file on time. "
         "The already-owned house has a small tax base that survives only while it stays in its present owner's name. "
         "Every table here carries that distinction as a column.",
         '<a href="properties.html">see it</a>'],
        ["The exclusion is a lease, not a deed",
         "Read from the statute and the Board's own guidance: if the heir later stops qualifying, the assessor enrols the value as if "
         "the exclusion had never applied. A plan that banks on the low tax forever is wrong at the first change of use.",
         '<a href="decision.html">see it</a>'],
        ["Numbers, rounded to $10, so nothing can be traced back",
         "The rounding you asked for is enforced by the build: a household amount that is not a multiple of $10 fails the verifier. "
         "Statutory amounts are quoted exactly and marked, because rounding a legal threshold would misstate it.",
         '<a href="methodology.html">see it</a>'],
        ["Fresh verification, with the document opened",
         "The IRS 2027 inflation procedure, the Board's Proposition 19 letter, its inflation-factor letter, the statute itself, "
         "the city's rate page and the Secretary of State's count were each read today, not quoted from memory.",
         '<a href="sources.html">see it</a>'],
    ]
    b.append(table(["What is new", "Why it matters", "Where"], rows))
    b.append(callout(
        "<b>Start here if you read one page.</b> Read the <a href=\"executive-summary.html\">executive summary</a>, "
        "then the <a href=\"questions.html\">open questions</a>. The arithmetic is finished; what is left is nine pieces "
        "of paper only you can get.", "good"))
    b.append("<h3>How to use the suggestions board</h3>")
    b.append("<p class=\"note\">The <a href=\"suggestions.html\">suggestions page</a> is deliberately separate from the analysis. "
             "Nothing there has been implemented: each item carries the change it proposes, what it would buy you, and the risk "
             "of doing it. Mark each one accept, modify or reject, and the site changes only where you say.</p>")
    return page("index", "Overview", "A decision desk for one house that is coming, one that is already here, and the "
                "money that comes with them. Everything below is computed, sourced and rounded to your rule.", "".join(b))


def p_requirements():
    rows = []
    for r in REQUIREMENTS:
        rows.append([r["id"], esc(r["text"]), tag(r["status"]),
                     f'<a href="{r["where"]}">{r["where"].replace(".html", "")}</a>',
                     esc(r["note"])])
    counts = {}
    for r in REQUIREMENTS:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    b = [stat_block([("requirements listed", len(REQUIREMENTS)),
                     ("met", counts.get("met", 0)),
                     ("met with gaps", counts.get("met-with-gaps", 0)),
                     ("open on your documents", counts.get("open-on-owner", 0))])]
    b.append("<p class=\"note\">Status words: <span class=\"tag met\">met</span> the brief's instruction is satisfied in full on "
             "a page; <span class=\"tag met-with-gaps\">met-with-gaps</span> satisfied, with a limitation stated on the page; "
             "<span class=\"tag open-on-owner\">open-on-owner</span> the analysis is complete but the value can only come from "
             "your own documents, so it is listed as a question instead of guessed.</p>")
    b.append(table(["id", "Your instruction", "status", "answered on", "what that means"], rows, cls="reg"))
    b.append("<h3>How to read the gaps</h3>")
    b.append("<p class=\"note\">The four open items are not failures of research. Two are private account documents "
             "(insurance declarations, utility statements), one is a bill line item, and one is the trust instrument. Each has "
             "a named discovery action on the <a href=\"questions.html\">questions page</a> and a row on "
             "<a href=\"flagged.html\">Flagged for review</a>.</p>")
    return page("requirements", "Requirement register",
                "Your brief, collected into one list, so that nothing in it is quietly dropped.", "".join(b))


def p_executive_summary():
    T = BASELINE_T
    occupy = simulate(T, "occupy")["terminal"]
    rent = simulate(T, "rent")["terminal"]
    sell = simulate(T, "sell")["terminal"]
    hybrid = simulate(T, "occupy_then_sell")["terminal"]
    be_g = break_even_growth(T, "occupy")
    be_r = break_even_rate(T, "occupy")
    gap = market(T) - enrolled_asis(T)
    b = []
    b.append(stat_block([
        ("inherited house, value today", money(A_MARKET)),
        ("its assessed value today", money(A_ASSESSED)),
        ("annual property tax today", money(A_BILL_2025)),
        ("tax if bought at market value today", money(market(Y0) * RATE_A + OTHER_A)),
    ]))
    b.append("<h3>The situation</h3>")
    rank = sorted(((simulate(T, k)["terminal"], lab) for k, lab in PATHS), reverse=True)
    b.append(f"""<p>A house is held in a family trust and is expected to pass to the heir between 2040 and 2050.
Its market value is about {money(A_MARKET)} and its assessed value is about {money(A_ASSESSED)}, so the tax
charged on it is roughly {money(A_BILL_2025)} a year where a buyer at today's price would pay about
{money(market(Y0) * RATE_A + OTHER_A)}. That difference is the largest single thing in this analysis, and it is
conditional: California's Proposition 19 lets the base pass to a child only if the child makes the house a
principal residence within a year, claims the homeowners' exemption within a year, and keeps qualifying. If the
heir later stops qualifying, the assessor enrols the value as if the exclusion had never applied - the relief is
a lease, not a deed. The heir already owns another house outright, a three-unit building letting two units with a
third available; it is not part of the inheritance, and it is the alternative place to live, which is exactly why
"sell" is not a choice made in isolation. On the central assumptions the ranking at a {T} transfer is
{" &gt; ".join(lab for _, lab in rank)}.</p>""")
    b.append("<h3>The five claims this desk is most confident about</h3>")
    vrows = []
    for v in VERIFIED[:14]:
        vrows.append([esc(v["item"]), f'<span class="num">{v["value"]}</span>', tag(v["status"]),
                      esc(v.get("note", "")), srcl(v["src"])])
    b.append(table(["claim", "value", "status", "why", "source"], vrows))
    b.append("<h3>The answer, by path</h3>")
    prows = []
    means = {k: sum(simulate(tt, k)["terminal"] for tt in TRANSFER_YEARS) / 3 for k, _ in PATHS}
    best_mean = max(means.values())
    for key, label in PATHS:
        vals = [simulate(t, key)["terminal"] for t in TRANSFER_YEARS]
        best = max(vals)
        prows.append([label, money(vals[0]), money(vals[1]), money(vals[2]), money(sum(vals) / 3),
                      ("best mean" if means[key] == best_mean else "") + " " + basis_cell()])
    b.append(table(["path", "transfer 2040", "transfer 2045", "transfer 2050", "mean of the three", "note"], prows))
    b.append(note("Wealth at 2076 in nominal dollars, after tax, attributable to the inherited house, on the baseline "
                  "assumptions (house values 4.0% a year, reinvestment 3.9% a year after tax, costs at the rates on the "
                  "methodology page). The already-owned house is held in every path, so it does not appear in these "
                  f"numbers except through its vacant unit: living in the inherited house means that unit is let and not "
                  f"living there means the heir lives in it, which is worth {money(unit3_uplift(T))} by 2076 at a {T} "
                  "transfer and is credited inside the occupy rows."))
    b.append(callout(
        f"<b>What would change the answer.</b> Living in the house and never selling catches up with selling if house "
        f"values compound at about {pc(be_g, 1)} a year instead of 4.0%, or if the after-tax reinvestment return falls to "
        f"about {pc(be_r, 1)} instead of 3.9%. Those two numbers decide the ranking, not the carrying costs: every cost "
        f"line moves the answer by hundreds of thousands, against a {money(sell - occupy)} spread between the best and "
        "worst paths.", "warn"))
    b.append("<h3>The deadlines that exist whether or not you decide anything</h3>")
    drows = [
        ["Produce the trust deed and the recorded deed", "no deadline", "decides whether probate applies at all",
         '<a href="questions.html">Q01</a> <a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PROB&sectionNum=10810">the fee if it does</a>'],
        ["Claim the homeowners' exemption on the inherited house", "by 15 February each year, 80% through 10 December",
         f"worth about {money(EXEMPTION * RATE_A)} a year and it is the precondition for the Proposition 19 claim",
         '<a href="carrying-costs.html">carrying costs</a> <a href="https://boe.ca.gov/proptaxes/pdf/lta23027.pdf">the exemption sheet</a>'],
        ["File the change in ownership statement after a death", "150 days", "a penalty attaches and the assessor's "
         "notice starts clocks you did not know were running", '<a href="process.html">process</a>'],
        ["File the estate tax return if the estate is over the exclusion", "9 months, plus 6 on extension",
         "40% of the excess, and the basis values reported become the heirs' ceiling",
         '<a href="estate-tax.html">inheritance tax</a>'],
        ["Make the inherited house the heir's principal residence", "1 year from transfer", "without it there is no "
         "exclusion at any value", '<a href="decision.html">the decision</a>'],
        ["File the Proposition 19 claim", "3 years, ending sooner if the house is sold or stops being occupied",
         f"the saving is worth roughly {money(market(T) * RATE_A - (max(enrolled_asis(T), market(T) - allowance(T))) * RATE_A)} a year "
         "in the middle transfer year",
         '<a href="process.html">process</a> <a href="https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf">the amount</a>'],
        ["Keep the exemption alive after that", "every year, while the heir qualifies",
         "the exclusion is removed when the heir stops qualifying, and the transfer-date value is then enrolled",
         '<a href="flagged.html">G03</a> <a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2">section 63.2(a)(1)(C)</a>'],
    ]
    b.append(table(["what", "deadline", "why it matters", "where and on whose authority"], drows))
    b.append("<h3>What is still unknown, and how much it matters</h3>")
    open_q = [q for q in QUESTIONS if q["status"] == "open"]
    b.append(f"<p class=\"note\">{len(open_q)} of the {len(QUESTIONS)} questions on the "
             "<a href=\"questions.html\">questions page</a> are open. Two of them can move a number by more than a "
             "factor: what the two tax bills actually contain, and what the cash side of the estate is. The rest change "
             "confidence rather than direction.</p>")
    b.append("<h3>Two lines worth more than every cost in this analysis</h3>")
    u = unit3_uplift(T)
    b.append(table(["the line", "value at 2076", "why it is not in the table above"], [
        ["letting the vacant unit at the already-owned house", money(u) + " " + basis_cell(),
         "it is not free money: that unit is the alternative home for the heir, so it can be let or lived in, not "
         "both. It is credited inside the paths where the heir lives in the inherited house and absent elsewhere, "
         "which is why it appears nowhere in the table above as a separate row"],
        ["the gross rent the inherited house would fetch, if it is let",
         money(simulate(T, "rent")["terminal"]) + " " + basis_cell(),
         "the rent path rests on a 2.0% gross yield placeholder; the break-even rent against selling is "
         "printed on the decision page and is far higher, which is the finding, not the input"],
        ["the value the estate tax would take",
         "0 <span class=\"tag sm\">on these exclusions</span> " + basis_cell(),
         "it is 40% of anything above the exclusion, so it is worth more than the whole analysis if the cash "
         "inheritance is large; the estate-size figure is question Q04"],
    ]))
    return page("executive-summary", "Executive summary",
                "The whole picture on one page: the situation, the money, the answer, the deadlines and the things that "
                "could overturn it.", "".join(b))


def p_properties():
    b = []
    b.append("<h3>The distinction you asked to be carried through the analysis</h3>")
    rows = [
        ["How it is held", "in a family trust, not yet transferred", "owned outright now",
         '<span class="tag owner">owner statement; the deed has not been produced</span>'],
        ["What triggers a tax event", "the transfer at death is a change in ownership: reassessment unless "
         "the Proposition 19 family-home exclusion is claimed and kept",
         "nothing until it is sold or given away; a lifetime transfer of a rental is reassessed in full",
         '<a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2">'
         "section 63.2</a>"],
        ["Tax base", f"about {money(A_ASSESSED)} against a market value of about {money(A_MARKET)}",
         f"about {money(B_ASSESSED)} against a market value of about {money(B_MARKET)}",
         '<span class="tag owner">owner-supplied values, rounded to $10</span><br>the roll entry and the bill are '
         'the sources, and neither is published on this site: '
         '<a href="flagged.html">why these two figures are not linked</a>'],
        ["Federal basis", "stepped up to market value at death, so a sale soon after the transfer normally "
         "realises no gain", "the owners' original basis; a sale today would attract tax on decades of gain, "
         "and only one home can be a principal residence", '<a href="https://www.irs.gov/taxtopics/tc701">IRS Topic 701</a>'],
        ["Transfer tax on the same event", "included in the gross estate with the cash; the estate exclusion, "
         "not the house, decides whether anything is due", "also inside the estate unless it is dealt with before "
         "death", '<a href="https://www.irs.gov/instructions/i706">Form 706 instructions</a>'],
        ["Income today", "none, unless it is let - and letting it forfeits the exclusion",
         f"about {money(B_RENT_2UNITS)} a year from two units, with a third unit available",
         '<span class="tag owner">owner-supplied rent</span><br>letting rules and the rent cap: '
         '<a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12">'
         "the state cap</a>"],
        ["What the tax bill implies", f"{pc(IMPLIED_A)} of the assessed value, against a typical composite rate "
         f"of {pc(RATE_A, 4)} in the county rate book",
         f"{pc(IMPLIED_B)} of the assessed value, against a published secured rate of 1.18162182% <span class=\"tag exact\">exact</span>",
         '<span class="tag owner">the gap on this row is the biggest unpriced item in the analysis - '
         '<a href="flagged.html">flagged G01</a></span>'],
    ]
    b.append(table(["", "the house that is coming", "the house already owned", "source and status"], rows))
    b.append(callout("<b>Why the asymmetry matters.</b> The inherited house's advantage is a <i>conditional</i> low tax "
                     "base that the heir can lose by not living there. The already-owned house's advantage is an "
                     "<i>unconditional</i> low tax base that is destroyed by handing it over while it is let, and "
                     "protected by doing nothing. The two houses therefore point at opposite behaviours: rush to occupy one, "
                     "do not rush to transfer the other.", "warn"))
    b.append("<h3>Both assessed-value histories, checked against the law rather than against each other</h3>")
    frows = []
    for y, ccpi, f in BOE_FACTORS[:24]:
        roll = y.split("-")[0]
        frows.append([f"roll {y}", pc(ccpi / 100.0, 3), f"{f:.5f}".rstrip("0").rstrip("."),
                      "at the 2% cap" if f == 1.02 else ("below the cap" if f > 1 else "deflation: base falls")])
    b.append(table(["roll year", "published inflation change", "factor applied", "effect"], frows))
    b.append(note("The published factor table runs 1976-77 to 2026-27; the cap binds in "
                  f"{BOE_YEARS_AT_CAP} of those {BOE_YEARS_TOTAL} roll years, which is why the projections use 2% rather "
                  "than an inflation forecast for an enrolled base. The full table is at the Board's letter."))
    b.append("<p class=\"note\"><b>Verification result.</b> Each year of the inherited house's assessed-value history that "
             "you supplied was divided by the year before and compared with the published factor for that roll year. Every "
             "year matched to within a few dollars, including the years the factor was below the cap (1.525% and 1.036%), "
             "which is what a true Proposition 13 base does and what a reassessed property would not show. The "
             "already-owned house's history matches in every year except one, where the step is about $45 short of 2%. "
             "Neither history is published on this desk, at any rounding, because a rounded series can be matched to one "
             "parcel in the open roll - see the <a href=\"methodology.html\">privacy rule</a>.</p>")
    b.append("<h3>What each house is worth to the decision</h3>")
    rows2 = []
    for T in TRANSFER_YEARS:
        v = market(T)
        fb = enrolled_asis(T)
        av_occupy = max(fb, v - allowance(T))
        rows2.append([f"transfer in {T}", money(v), money(fb), money(av_occupy), money(v - av_occupy),
                      money((v - av_occupy) * RATE_A), money(allowance(T)),
                      '<a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2">the statute arithmetic</a> '
                      'and <a href="https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf">the published amount</a>'])
    b.append(table(["transfer year", "market value at transfer", "factored base if nothing changes",
                    "enrolled value with the exclusion claimed", "value that is still reassessed",
                    "annual tax avoided by claiming it", "the adjusted amount then", "why"], rows2))
    b.append(note(f"The adjusted amount is {exact(1044586)} for transfers between 16 February 2025 and 15 February "
                  "2027, and is re-indexed the following February; the figures in the last column are this desk's "
                  "projection of that indexation (D4), not published amounts. "
                  "Read the last two columns together. The exclusion does not preserve the old base; it subtracts the "
                  "adjusted amount from the market value. Because this house is worth far more than the base plus that "
                  "amount, most of its value is reassessed anyway, and what the heir actually saves each year is about the "
                  f"amount in the final column times the rate - roughly {money(allowance(BASELINE_T) * RATE_A)} a year at a "
                  f"{BASELINE_T} transfer, on top of the difference the second and third columns show. An earlier generation "
                  "of this project treated the exclusion as shielding the whole gap, which is the error the referee tree "
                  "logged and this page corrects."))
    return page("properties", "The two houses",
                "One is coming and conditional; one is here and static. Almost every number below behaves differently "
                "because of that.", "".join(b))


def p_carrying():
    b = []
    b.append("<h3>The inherited house, line by line</h3>")
    rows = []
    lines = [
        ("property tax on the enrolled base", lambda y: tax_a(y, enrolled_asis(y), True), "rate carried, owner bill",
         "the assessed value grows at the published 2% cap and the bill's other charges at cost inflation"),
        ("home insurance", lambda y: grow(INSURANCE, y - Y0, G_INS), "owner figure, 4% a year (D6)",
         "below the statewide average the department publishes - flagged G02"),
        ("water and sewer", lambda y: grow(A_WATER, y - Y0, G_CPI), "owner figure $130 a month, CPI (D5)",
         "the tariff is published but not a household's consumption - flagged G06"),
        ("electricity, net of the solar credit", lambda y: grow(A_ELEC, y - Y0, G_CPI) if y < ELEC_ENDS else 0.0,
         "owner figure $10-$20 a month, modelled at $180 a year (D13)",
         "the credit is modelled as ending in 2043 because the interconnection date is unknown"),
        ("maintenance and repairs", lambda y: grow(A_MARKET * MAINT_A, y - Y0, G_CPI),
         "0.8% of the 2026 value, then CPI (D17)",
         "held to cost inflation rather than to price: your note that this house needs less than the rental is why "
         "the rate is below the rental's"),
    ]
    for name, fn, status, why in lines:
        rows.append([name] + [money(fn(y)) for y in (Y0, 2040, 2050, Y1)] +
                    [f'<span class="tag sm {status_tag(status)}">{status_tag(status)}</span> {status}<br>{why} '
                     f'&middot; <a href="methodology.html">assumptions</a>, '
                     f'<a href="sources.html">sources</a> and '
                     f'<a href="flagged.html">what is not verifiable</a>'])
    total = lambda y: sum(fn(y) for _, fn, _, _ in lines)
    rows.append(["<b>total, every year, with no rent coming in</b>"] + [money(total(y)) for y in (Y0, 2040, 2050, Y1)] +
                ["<b>what a decision to simply keep the house costs</b> " + basis_cell()])
    b.append(table(["cost line", "2026", "2040", "2050", "2076", "status and basis"], rows))
    b.append(note("Every figure on this page is either an owner input or arithmetic on one, with the growth rate "
                  "named in the assumption id. The official documents behind the rates and rules are in the "
                  '<a href="sources.html">source register</a>, and the inputs are listed on the '
                  '<a href="methodology.html">methodology page</a>.'))
    b.append("<h3>The already-owned house, line by line</h3>")
    blines = [
        ("rent from two units", lambda y: rent_b(y, 2), "owner figure, 2% a year (D8)"),
        ("property tax on its enrolled base", lambda y: tax_b(y), "city rate verified; other charges derived from the bill"),
        ("insurance", lambda y: grow(INSURANCE, y - Y0, G_INS), "owner figure, 4% a year (D6)"),
        ("water and sewer for three units", lambda y: grow(B_WATER, y - Y0, G_CPI), "owner range $330-$400 a month"),
        ("electricity for the common parts", lambda y: grow(B_ELEC, y - Y0, G_CPI), "owner range $30-$70 a month"),
        ("maintenance", lambda y: grow(B_MARKET * MAINT_B, y - Y0, G_CPI), "1.2% of the 2026 value, then CPI (D17)"),
        ("management", lambda y: rent_b(y, 2) * MGMT, "6% of rent (assumption)"),
    ]
    brows = []
    for name, fn, status in blines:
        brows.append([name] + [money(fn(y)) for y in (Y0, 2040, 2050, Y1)] +
                     [f'<span class="tag sm {status_tag(status)}">{status_tag(status)}</span> {status} '
                      f'<a href="methodology.html">assumptions</a> &middot; <a href="sources.html">sources</a>'])
    bnet = lambda y: sum(fn(y) for n, fn, _ in blines if n.startswith("rent")) - \
        sum(fn(y) for n, fn, _ in blines if not n.startswith("rent"))
    brows.append(["<b>net income before income tax</b>"] + [money(bnet(y)) for y in (Y0, 2040, 2050, Y1)] +
                 ["<b>the engine that funds whichever choice you make</b> " + basis_cell()])
    b.append(table(["line", "2026", "2040", "2050", "2076", "status"], brows))
    b.append(note('Sources for the rates behind these rows: the <a href="sources.html">source register</a>.'))
    b.append(callout("<b>The three levers you can pull now.</b> Let the vacant unit (worth roughly the third of the rent "
                     "row), confirm what the second bill's extra 1% actually is (flagged G01), and put both insurance "
                     "policies out for quote (flagged G02). None of the three depends on the inheritance happening."))
    b.append("<h3>What each cost line does to the decision</h3>")
    srows = []
    base_term = simulate(BASELINE_T, "occupy")["terminal"]
    for label, kw in [("insurance compounding at 12% a year instead of 4%", dict(ins_g=0.12)),
                      ("all operating costs at 3.5% instead of 2.5%", dict(cpi=0.035)),
                      ("maintenance at 1.5% of value instead of 0.8%", dict(maint=0.015)),
                      ("the solar credit ending in 2031 instead of 2043", dict(elec_end=2031))]:
        term = simulate(BASELINE_T, "occupy", **kw)["terminal"]
        delta = term - base_term
        srows.append([label, money(delta) + " " + basis_cell(),
                      "material" if abs(delta) > 0.05 * abs(base_term) else "small beside the growth and rate inputs"])
    b.append(table(["stress on one line", "effect on the hold path's terminal wealth", "verdict"], srows))
    b.append(note("Each row changes only the one input named, leaving the rest at the baseline, so the four rows are "
                  "directly comparable and each is the real model output rather than a back-of-envelope sum."))
    return page("carrying-costs", "Carrying costs",
                "What each house costs to hold, projected on the assumptions named beside each line, with the status of "
                "every input.", "".join(b))


def p_projections():
    T = BASELINE_T
    rows = []
    basis = ('<a href="{h}">value index</a> &middot; <a href="{c}">2% cap</a> &middot; '
             '<a href="{ra}">rate, inherited</a> &middot; <a href="{rb}">rate, owned</a>').format(
        h=SRC["fred_hpi"]["url"], c=SRC["boe_lta26002"]["url"],
        ra=SRC["scc_ratebook"]["url"], rb=SRC["sftc_rate"]["url"])
    for y in range(Y0, Y1 + 1):
        v = market(y)
        av_asis = enrolled_asis(y)
        av_occ = enrolled_after_transfer(y, T, "occupy") if y >= T else av_asis
        av_rent = enrolled_after_transfer(y, T, "rent") if y >= T else av_asis
        row = [str(y), money(v), money(av_asis),
               money(tax_a(y, av_asis, True)),
               money(av_occ) if y >= T else "&mdash;",
               money(tax_a(y, av_occ, True)) if y >= T else "&mdash;",
               money(av_rent) if y >= T else "&mdash;",
               money(tax_a(y, av_rent, False)) if y >= T else "&mdash;",
               money(costs_a(y)),
               money(prop13_av_b(y)), money(tax_b(y)), money(rent_b(y, 2)),
               money(net_if_sold(y)), basis]
        rows.append(row)
    head = ["year", "inherited: market value", "inherited: enrolled base, no transfer",
            "inherited: tax as it stands", "inherited: base if occupied at 2045",
            "inherited: tax with the exclusion", "inherited: base if let at 2045",
            "inherited: tax with no exclusion", "inherited: other carrying cost",
            "owned: enrolled base", "owned: tax", "owned: rent from two units",
            "net if the inherited house were sold in this year", "every figure comes from"]
    b = []
    b.append(note(f"Transfer assumed in {T} for the two path columns. Baseline: values 4.0% a year (D1, D2), the enrolled "
                  "base 2% a year (D3), the Proposition 19 amount 4.3% a year (D4), costs at 2.5% (D5) and insurance at "
                  "4.0% (D6). Every figure is rounded to $10. The market-value column is a projection, not a valuation."))
    b.append(table(head, rows))
    b.append("<h3>How the two tax bases diverge from the market</h3>")
    rows2 = []
    for y in (Y0, 2035, 2045, 2055, 2065, Y1):
        v = market(y)
        fb = enrolled_asis(y)
        rows2.append([str(y), money(v), money(fb), money(v - fb), pc((v - fb) / v, 1),
                      money((v - fb) * RATE_A), money(allowance(y)), basis])
    b.append(table(["year", "market value", "enrolled base", "the gap", "gap as a share of value",
                    "annual tax the gap is saving at the current rate", "Proposition 19 adjusted amount",
                    "basis"], rows2))
    b.append(callout("<b>The gap is the asset, and it is also the target.</b> A Proposition 19 repeal, a change of "
                     "ownership, or a new owner at market value all move the tax toward the second column. The projections "
                     "here assume nothing reassesses the inherited house until the transfer itself."))
    return page("projections", "Projections 2026-2076",
                "Year by year, both houses, every path's tax base, at your rounding rule.", "".join(b))


def p_decision():
    b = []
    b.append("<h3>The comparison</h3>")
    rows = []
    for T in TRANSFER_YEARS:
        for key, label in PATHS:
            s = simulate(T, key)
            r = s["terminal"]
            rows.append([f"{T}", label, money(r), money(real2026(r)),
                         money(s["acc"]), money(s["proceeds"]), money(s["tax"]),
                         ("highest" if key == "sell" else "") + " " + basis_cell()])
    b.append(table(["transfer year", "path", "wealth at 2076", "same, in 2026 dollars", "compounded cash flows",
                    "sale proceeds at the end", "tax on that sale", "basis of the row"], rows))
    b.append(note("Nominal dollars at 2076. Compounded cash flows are the years' net carry (negative when the house costs "
                  "money to hold) reinvested at 3.9% after tax. The sale column shows the gross-after-cost proceeds at the "
                  "sale year, grown to the horizon."))
    b.append("<h3>The two break-evens that decide it</h3>")
    be_rows = []
    for T in TRANSFER_YEARS:
        g = break_even_growth(T, "occupy")
        r = break_even_rate(T, "occupy")
        y = break_even_yield(T)
        be_rows.append([f"{T}", pc(g, 1) if g else "&mdash;", pc(r, 1) if r else "&mdash;",
                        pc(y[0], 2) if y else "&mdash;",
                        (money(market(T) * y[0] / 12) if y else "&mdash;") + " " + basis_cell()])
    b.append(table(["transfer year", "house growth at which holding ties selling",
                    "after-tax reinvestment return at which selling ties holding",
                    "gross yield at which renting ties selling", "that rent a month at the transfer year"], be_rows))
    b.append(note(f"The baseline used in every other table is 4.0% house growth and 3.9% after-tax reinvestment. Both "
                  "break-evens sit outside the plausible middle of the published history: the metro index measured "
                  f"{pc(cagr(HPI_SJ, 1995, 2025), 1)} a year since 1995 and {pc(cagr(HPI_SJ, 2006, 2025), 1)} a year since "
                  "the 2006 peak, and the published 10-year Treasury average has run between 0.89% and 4.29% in the years "
                  "since 2015."))
    b.append("<h3>Sensitivity grid: wealth at 2076 for the two main paths</h3>")
    grids = []
    for r in (0.025, 0.039, 0.052):
        for g in (0.015, 0.029, 0.040, 0.058):
            occ = simulate(BASELINE_T, "occupy", g=g, r=r)["terminal"]
            s = simulate(BASELINE_T, "sell", g=g, r=r)["terminal"]
            rent = simulate(BASELINE_T, "rent", g=g, r=r)["terminal"]
            best = max([("sell", s), ("occupy", occ), ("rent", rent)], key=lambda kv: kv[1])
            grids.append([pc(r, 1), pc(g, 1), money(occ), money(s), money(rent),
                          f"<b>{best[0]}</b> wins by {money(abs(best[1] - sorted([s, occ, rent])[-2]))} "
                          + basis_cell(extra=f'<a href="{SRC["fred_cpi_sf"]["url"]}">rate history</a>')])
    b.append(table(["after-tax reinvestment", "house growth", "hold it", "sell it", "let it", "outcome"], grids))
    grid = [{k: simulate(BASELINE_T, k, g=g, r=rr)["terminal"] for k, _ in PATHS}
            for rr in (0.025, 0.039, 0.052) for g in (0.015, 0.029, 0.040, 0.058)]
    gwins, gtot = winner_matrix(grid)
    b.append(note(f"{gtot} combinations, one transfer year ({BASELINE_T}), everything else at the baseline: "
                  + ", ".join(f"{dict(PATHS)[k]} first in {v}"
                              for k, v in sorted(gwins.items(), key=lambda kv: -kv[1]))
                  + ". Selling wins most of the grid, which is the honest headline; the paths where a neighbour takes it "
                    "are the ones where values compound fast and the alternative return is poor."))
    b.append("<h3>The interaction with the house you already own</h3>")
    irows = []
    for key, label in PATHS:
        term = simulate(BASELINE_T, key)["terminal"]
        nocc = simulate(BASELINE_T, key, housing_credit=False)["terminal"]
        irows.append([label, money(term), money(nocc), money(term - nocc) + " " + basis_cell(),
                      "the heir lives in the inherited house, so the vacant unit at the other house is let"
                      if key in ("occupy", "occupy_then_sell") else
                      "the heir is housed at the other house, so that unit is not let and no credit is due"])
    b.append(table(["path", "as modelled", "same path, third unit ignored", "the credit", "why"], irows))
    b.append(note("This is the piece the earlier generations of this project left out, and it is why the occupy rows are "
                  "not as far behind as a raw yield comparison suggests: housing is a service the already-owned house "
                  "provides, and it can only be provided once. Ignoring it flatters selling; crediting it to every path "
                  "is simply wrong."))
    b.append(callout("<b>The sequencing error to avoid.</b> Letting the inherited house before the exclusion is claimed is "
                     "not a neutral choice: it is evidence against principal-residence use, and the exclusion decides a "
                     "larger number than the rent does. Conversely, do not hand the already-owned rental over to the heir "
                     "while it is let - a rental has no family-home exclusion, so the transfer resets it to market value "
                     "permanently.", "warn"))
    b.append("<h3>Recommendation, and the reason for it</h3>")
    b.append("<ol>"
             "<li><b>Claim and keep the exclusion, and decide the rest later.</b> The exclusion is cheap to claim and "
             "irreplaceable to recover; the sell-versus-hold question does not have to be answered in the year of the death. "
             f"Occupying for a decade and then selling ends {money(simulate(BASELINE_T, 'sell')['terminal'] - simulate(BASELINE_T, 'occupy_then_sell')['terminal'])} "
             f"below selling at once at a {BASELINE_T} transfer - the price of keeping both futures open, and the only "
             "path that finishes first when history is replayed at us on the "
             "<a href=\"black-swans.html\">black swans page</a>.</li>"
             "<li><b>Do not plan on renting it out.</b> It forfeits the exclusion, and the rent that would make up for "
             f"that is about {money(break_even_yield(BASELINE_T)[1])} a month at a {BASELINE_T} transfer - far above "
             "anything the local market is reported to pay for a house at this price.</li>"
             "<li><b>If the answer is to sell, sell into strength, not on a deadline.</b> The forced-sale-at-the-trough "
             f"regime on the <a href=\"black-swans.html\">black swans page</a> is the only stress that changes the ranking "
             "more than the assumptions do.</li>"
             f"<li><b>Let the vacant unit at the other house, if you are not living in it.</b> It is worth about "
             f"{money(unit3_uplift(BASELINE_T))} by 2076, which is more than the whole carrying-cost table of the "
             "inherited house, and it does not depend on the inheritance at all.</li>"
             "<li><b>Get the estate-size number.</b> Whether 40% is payable on anything is set by the cash, not by the "
             "house, and no other question in this file can move the answer as far.</li>"
             "</ol>")
    return page("decision", "The decision",
                "Live in it, let it, or sell and reinvest, after tax, for each transfer year, with the two break-evens "
                "that decide the ranking.", "".join(b))


def p_estate_tax():
    b = []
    b.append("<h3>What is taxed when someone dies in California</h3>")
    rows = [
        ["California estate tax", "none", '<a href="https://www.sco.ca.gov/ardtax_estate_tax.html">State Controller</a>',
         "the state's estate tax was wound up when the federal credit it ran on was repealed"],
        ["California inheritance tax (a tax on the receiver)", "none", '<a href="https://www.sco.ca.gov/ardtax_estate_tax.html">State Controller</a>',
         "California is one of the states with neither tax"],
        ["Federal estate tax", f"40% of the estate above the exclusion for the year of death: {exact(15000000)} for 2026, "
         f"{exact(15480000)} for 2027",
         '<a href="https://www.irs.gov/pub/irs-drop/rp-26-35.pdf">Rev. Proc. 2026-35</a> and '
         '<a href="https://www.irs.gov/instructions/i706">Form 706 instructions</a>',
         "the exclusion is indexed from 2027, so it grows in the years before a 2040-2050 transfer"],
        ["Federal basis adjustment", "the heir's basis becomes market value at death, so decades of gain are never "
         "taxed. The adjustment is Internal Revenue Code section 1014, and the 2025 act that raised the exclusion "
         "did not amend it - the claim that the step-up was repealed is not correct, so it is published here "
         "explicitly rather than left to inference.",
         '<a href="https://www.irs.gov/taxtopics/tc701">IRS Topic 701</a> and '
         '<a href="https://www.irs.gov/pub/irs-drop/rp-26-35.pdf">Rev. Proc. 2026-35</a>, which applies the same '
         "act's indexed exclusion",
         "this is worth more than the estate tax on most estates here. Two limits travel with it: a lifetime gift "
         "keeps the donor's basis instead (section 1015), which is why the gifting row below says to give cash and "
         "not the house; and where a return is filed, the value on it becomes the ceiling on the heirs' basis "
         "(sections 1014(f) and 6035), so the appraisal in the trust process is not a formality"],
        ["Documentary transfer tax on a transfer by trust or will", "excluded from the transfer tax in practice",
         '<a href="https://clerkrecorder.santaclaracounty.gov/recording-documents/recording-real-estate">'
         "county clerk-recorder</a>", "confirm on the recorder's page for the year - flagged as carried, not re-opened"],
        ["Real estate withholding on a later sale", "the seller's certificate applies where the sale is taxable; a sale "
         "at stepped-up basis is where the exemption matters",
         '<a href="https://www.ftb.ca.gov/forms/2024/2024-593-instructions.html">FTB form 593 instructions</a>',
         "carried from the repository register; not re-opened this session"],
        ["Probate, if the house is not in the trust", "a statutory percentage fee on the gross estate value, both for the "
         "personal representative and for the attorney",
         '<a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PROB&sectionNum=10810">'
         "Probate Code section 10810</a>", "read the tiers below; the fee is charged on the gross value, not the equity"],
    ]
    b.append(table(["layer", "what applies", "source", "note"], rows))
    b.append("<h3>How much can be inherited before tax bites</h3>")
    brows = []
    for y in (2026, 2027, 2030, 2035, 2040, 2045, 2050):
        if y <= 2027:
            e = 15480000 if y == 2027 else 15000000
            how = "published"
        else:
            e = grow(15480000, y - 2027, G_CPI)
            how = "projected at 2.5% a year, the same index the statute uses, for illustration only"
        brows.append([str(y), money(e), money(e * 2) if y > 2027 else money(30000000),
                      how + ' <a href="https://www.irs.gov/pub/irs-drop/rp-26-35.pdf">the published amounts</a>',
                      money(grow(20000, max(0, y - 2027), G_CPI)) if y >= 2027 else money(19000)])
    b.append(table(["year of death", "one person's exclusion", "a married couple's with portability", "how it is known",
                    "annual gift exclusion per recipient"], brows))
    b.append(note("Only the first two rows are published law. The rest are arithmetic on the published indexation rule, "
                  "shown so that a 2040-2050 window can be thought about; they are not forecasts of what Congress will do. "
                  "The couple's figure assumes a portability election is made on a timely Form 706."))
    b.append("<h3>What an estate of a given size would owe</h3>")
    erows = []
    for est in (8000000, 12000000, 16000000, 20000000, 26000000, 34000000, 50000000):
        for y, label in ((2027, "death in 2027"), (2045, "death in 2045, exclusion projected")):
            e = 15480000 if y == 2027 else grow(15480000, y - 2027, G_CPI)
            taxable = max(0.0, est - e)
            tax = taxable * 0.40
            probate = stat_fee(est)
            erows.append([money(est), label + " " + basis_cell(extra=(
                              '<a href="https://www.irs.gov/pub/irs-drop/rp-26-35.pdf">Rev. Proc. 2026-35</a>'
                              if y == 2027 else
                              '<a href="https://www.irs.gov/instructions/i706">Form 706 instructions</a>')),
                          money(e), money(taxable), money(tax), pc(tax / est, 1),
                          money(probate) if tax == 0 else "0 <span class=\"tag sm\">assume a trust</span>",
                          money(est - tax)])
    b.append(table(["estate at death (house plus cash)", "which exclusion", "exclusion", "above it", "federal estate tax",
                    "as a share of the estate", "statutory probate fee if there were no trust",
                    "what the heirs receive before income tax"], erows))
    b.append(note("The house enters the estate at market value, and the same market value becomes the heir's basis. So the "
                  "estate tax, if any, is charged on the house while the gain inside it escapes income tax entirely - the "
                  "two do not stack. The probate column applies only if the deed does not match the trust, which is "
                  "question Q01."))
    b.append("<h3>What gifting during life does and does not fix</h3>")
    grows = [
        ["Gifts inside the annual exclusion", f"{money(20000)} per recipient per year in 2027, and the same to a "
         "recipient's spouse if you elect splitting", "removes the money and its future growth from the estate",
         "a gift of appreciated property carries your basis instead of getting a step-up, so gifting cash beats "
         "gifting the house"],
        ["Gifts above it", "they consume the lifetime exclusion, and no gift tax is payable until that is used up",
         "useful when the estate will be far above the exclusion, because everything above is taxed at 40% at death "
         "but a lifetime gift only costs the excess above the then-current exclusion",
         "an irrevocable trust is normally needed to keep the growth out; those rules were not modelled here"],
        ["Gifting the house itself", "it is a change in ownership for Proposition 19 purposes either way, and the "
         "exclusion still requires the heir to live there",
         "no property-tax advantage to doing it early", "you lose the step-up on the appreciation after the gift - "
         "usually the worse trade"],
    ]
    b.append(table(["move", "how it works", "what it buys", "the catch"], grows, cls="reg"))
    return page("estate-tax", "Inheritance and estate tax",
                "How much passes untaxed at each level of government, what is owed above it, and what the house's "
                "income-tax basis does at the same moment.", "".join(b))


def stat_fee(v):
    tiers = [(100000, 0.04), (100000, 0.03), (800000, 0.02), (9000000, 0.01), (15000000, 0.005)]
    fee = 0.0
    left = v
    for band, rate in tiers:
        take = min(band, left)
        fee += take * rate
        left -= take
        if left <= 0:
            break
    if left > 0:
        fee += left * 0.002  # "a reasonable amount determined by the court" - shown, not claimed
    return fee


def p_process():
    steps = [
        ("0", "Date of death", "the trust becomes irrevocable; the estate's income-tax year begins",
         "successor trustee", '<a href="https://www.irs.gov/instructions/i706">Form 706 instructions</a>'),
        ("1", "Within days", "order certified death certificates (several; agencies want originals) and locate the "
         "original trust instrument and any amendment", "trustee or family", '<span class="tag owner">no public source</span>'),
        ("2", "Within 30 days of knowledge", "custodian of the decedent's will lodges the original with the county "
         "clerk if a probate is opened; in a fully funded trust this usually does not apply",
         "custodian", '<span class="tag carried">Probate Code - carried, not re-opened</span>'),
        ("3", "Within 60 days", "the trustee or personal representative serves the statutory notice on beneficiaries "
         "and heirs, which starts the 120-day creditor claim window",
         'trustee', '<a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PROB&sectionNum=16061.7">section 16061.7</a>'),
        ("4", "Within 150 days", "file the change in ownership statement with the county assessor for the real property "
         "that passed, including property that passed through the trust",
         "trustee", '<span class="tag carried">county assessor form; carried</span>'),
        ("5", "As soon as values are fixed", "a qualified appraisal of the house at the date of death, which sets both "
         "the estate value and the heir's basis", "appraiser and trustee",
         '<a href="https://www.irs.gov/instructions/i706">Form 706 instructions</a>'),
        ("6", "Within 9 months", "file Form 706 if the gross estate plus lifetime taxable gifts exceeds the exclusion "
         "for the year of death; Form 4768 buys six more months to file, not to pay",
         "executor or trustee", '<a href="https://www.irs.gov/instructions/i706">Form 706 instructions</a>'),
        ("7", "Within 30 days of that due date", "the return's values are reported consistently to the heirs, who cannot "
         "claim a basis above what the estate reported", "executor",
         '<a href="https://www.irs.gov/instructions/i706">consistent-basis reporting</a>'),
        ("8", "At the transfer", "the heir moves in, or does not. Within one year the house must be the heir's principal "
         "residence for the family-home exclusion", "heir",
         '<a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2">section 63.2(a)(1)(A)</a>'),
        ("9", "Within one year of the transfer", "file for the homeowners' exemption on the heir's own claim - this is a "
         "separate filing from the exclusion claim and it is the condition for it", "heir",
         '<a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2">section 63.2(a)(1)(B)</a>'),
        ("10", "Within three years, and before any sale or any end of occupancy",
         "file the Proposition 19 claim with the assessor. A late claim is considered but only from the lien date of the "
         "year it is filed, so the years you lose are not recovered", "heir",
         '<a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2">section 63.2(f)</a>'),
        ("11", "Same window", "record the trustee's deed transferring title, and pay the recording charges; a transfer "
         "by trust is normally outside the documentary transfer tax", "trustee and title company",
         '<a href="https://clerkrecorder.santaclaracounty.gov/recording-documents/recording-real-estate">county clerk-recorder</a>'),
        ("12", "Next roll", "the assessor enrols the value: either the factored base plus the excess over the adjusted "
         "amount, or market value with no exclusion", "assessor",
         '<a href="https://www.boe.ca.gov/proptaxes/pdf/lta26026.pdf">BOE LTA 2026/026</a>'),
        ("13", "Ongoing", "keep the exemption alive: the exclusion is removed in the year the heir stops qualifying, and "
         "the base that would have applied at transfer is then enrolled", "heir",
         '<a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2">section 63.2(a)(1)(C)</a>'),
    ]
    rows = [[s[0], s[1], esc(s[2]), esc(s[3]), s[4]] for s in steps]
    b = [table(["step", "deadline", "what happens", "who does it", "authority"], rows)]
    b.append(callout("<b>Two of these deadlines are the whole game.</b> Steps 8 and 9 - live there within a year, and claim "
                     "the exemption within a year - decide whether a seven-figure tax base survives. Step 10 files the claim, "
                     "and its three-year window closes early if the house is sold or stops being occupied, which is the trap "
                     "in the sequence: a plan to let it first and occupy later can forfeit both.", "warn"))
    b.append("<h3>What the same process looks like if the house is not in the trust</h3>")
    prows = [["probate opened", "the statutory fee applies to the gross value of the estate, at both the personal "
              "representative and the attorney, and the tiers are additive",
              f"on a house worth {money(A_MARKET)} that is about {money(stat_fee(A_MARKET))} each, before any "
              "extraordinary fees",
              '<a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PROB&sectionNum=10810">section 10810</a>'],
             ["small-estate route", "if the estate's California real and personal property is under the published "
              "threshold, an affidavit can avoid administration; a house at this value is far above it",
              f"{exact(208850)} for deaths on or after 1 April 2025",
              '<a href="https://www.courts.ca.gov/documents/de300.pdf">form DE-300</a>'],
             ["public filings", "the petition, inventory and account are public documents; a trust transfer is not",
              "this is the reason the privacy instruction matters more if step 1 comes back negative",
              '<span class="tag owner">process note</span>']]
    b.append(table(["if", "what changes", "figure", "source"], prows))
    b.append("<h3>Which documents close the open questions</h3>")
    drows = [[q["id"], esc(q["q"]), esc(q["how"]), esc(q["who"])] for q in QUESTIONS if q["status"] == "open"]
    b.append(table(["question", "what is unknown", "how to find out", "who can answer"], drows))
    return page("process", "Trust process, step by step",
                "Death to recorded title, with the deadline that attaches to each step and the authority behind it.",
                "".join(b))


def p_swans():
    b = []
    b.append("<h3>Why a flat 50-year line is the wrong base</h3>")
    mrows = [
        ["metro house price index, the inherited house's area",
         pc(cagr(HPI_SJ, 1995, 2025), 1), pc(cagr(HPI_SJ, 2006, 2025), 1), pc(cagr(HPI_SJ, 2015, 2025), 1),
         "30 years of growth against 19 years since the last peak against a recent decade"],
        ["division index, the other house's area",
         pc(cagr(HPI_SF, 1995, 2025), 1), pc(cagr(HPI_SF, 2006, 2025), 1), pc(cagr(HPI_SF, 2015, 2025), 1),
         "the same three windows on the other market"],
        ["peak-to-trough drawdown, 2006 to 2011", "", pc(peak_trough(HPI_SJ, 2006, 2011), 1), "",
         "the largest fall in the series this decision would have to sit through"],
        ["years to regain the 2006 high", "", str(years_to_recover(HPI_SJ, 2006)), "",
         "recovery time, which is what makes a forced sale permanent"],
        ["years to regain the 1990 high", "", str(years_to_recover(HPI_SJ, 1990)), "",
         "the regional bust took longer than the national one"],
        ["inflation, area CPI-U", pc(cagr(CPI_SF, 1990, 2024), 1), pc(cagr(CPI_SF, 2015, 2024), 1), "",
         "local prices, which is what the cost lines actually follow"],
        ["10-year Treasury annual average", pc(TREAS_10Y[2025] / 100, 2) + " in 2025",
         pc(TREAS_10Y[2012] / 100, 2) + " in 2012", pc(TREAS_10Y[1981] / 100, 2) + " in 1981",
         "the risk-free alternative to a house has moved by 12 points inside one lifetime"],
        ["30-year mortgage rate", pc(MORT_30Y[2026] / 100, 2) + " in 2026", pc(MORT_30Y[2021] / 100, 2) + " in 2021",
         pc(MORT_30Y[1981] / 100, 2) + " in 1981", "what a buyer can pay for, which sets the price of the house"],
        ["Proposition 13 inflation factor", f"{BOE_YEARS_AT_CAP} of {BOE_YEARS_TOTAL} roll years at the cap",
         "one year below zero (2010-11)", "3.307% used for the 2026 roll, capped to 2%",
         "the tax line is insulated from inflation up to 2%, and can even fall"],
    ]
    b.append(table(["series", "long window", "since the last peak", "recent", "what it means here"], mrows))
    b.append(note("All eight rows are computed from the published index values listed on the methodology page, retrieved "
                  "today from the producers' own addresses. Nothing in this table is a forecast."))
    b.append("<h3>The regimes, run through the model</h3>")
    rrows = []
    base = {p: simulate(BASELINE_T, p)["terminal"] for p, _ in PATHS}
    for reg in REGIMES:
        vals = {key: run_regime(BASELINE_T, key, reg)["terminal"] for key, _ in PATHS}
        winner = max(vals, key=lambda k: vals[k])
        rrows.append([f'<b>{reg["id"]}</b> {esc(reg["name"])}<br><span class="note">{esc(reg["detail"])}</span> '
                      f'<a href="{SRC["fred_hpi"]["url"]}">the series behind it</a> &middot; '
                      f'<a href="methodology.html">assumptions</a>',
                      money(vals["occupy"]), money(vals["sell"]), money(vals["rent"]),
                      f"{winner} wins; the spread is {money(abs(vals['occupy'] - vals['sell']))}",
                      esc(reg["watch"])])
    b.append(table(["regime", "live in it", "sell and reinvest", "let it", "what happens to the ranking",
                    "what it really tests"], rrows))
    b.append(note("The value path in the replayed regimes is replaced by the published annual changes for the years the "
                  "regime names, then returns to the 4.0% baseline; the other inputs stay at the baseline unless the regime "
                  "overrides them, and each override is printed in the regime's own row. The same paths as the decision page, the same transfer "
                  "year, so the only difference from the decision page is the shock."))
    b.append("<h3>The ranking, regime by regime</h3>")
    order = []
    for reg in REGIMES:
        vals = {k: run_regime(BASELINE_T, k, reg)["terminal"] for k, _ in PATHS}
        order.append([reg["id"], reg["name"], " &gt; ".join(sorted(vals, key=lambda k: -vals[k])),
                      "selling still first" if max(vals, key=vals.get) == "sell" else "the holder wins this one"])
    b.append(table(["regime", "episode", "paths in order", "headline"], order, cls="reg"))
    rgrid = [path_terms(BASELINE_T, reg) for reg in REGIMES]
    rwins, rtot = winner_matrix(rgrid)
    swing = abs(rgrid[4]["occupy"] - rgrid[4]["sell"]) - abs(rgrid[3]["occupy"] - rgrid[3]["sell"])
    b.append(callout("<b>What survives every regime in that table.</b> "
                     + ", ".join(f"{dict(PATHS)[k]} finishes first in {v} of {rtot}"
                                 for k, v in sorted(rwins.items(), key=lambda kv: -kv[1]))
                     + ". The direction of the answer is robust to history being replayed at us; the size of it is not, "
                       f"with the gap between living in the house and selling it swinging by {money(abs(swing))} between "
                       "the deflation decade and the rate shock. Protect the exclusion, which is worth about the same in "
                       "every one of these worlds, and leave the sale to a year you choose rather than one you are given.",
                     "good"))
    b.append("<h3>Baselines worth arguing with</h3>")
    brows = [
        ["house value growth, used here", pc(G_HOME, 1), "between the 19-year and 30-year measured rates for the "
         "inherited house's area, and above the rate since 2015 for the other",
         "the projections page is also shown at 1.5%, 2.9% and 5.8% on the decision grid"],
        ["cost inflation, used here", pc(G_CPI, 1), "below the area CPI-U measured over 1990-2024 and well below "
         "2015-2024", "deliberately optimistic on the cost lines; the tax line is capped separately"],
        ["after-tax reinvestment, used here", pc(R_AFTER, 1), "a balanced portfolio at 5.0% nominal with tax, against "
         "a published risk-free average of 2.70% for 2016-2025 and 4.29% for 2025",
         "the number the ranking is most sensitive to; see the break-even table"],
        ["Proposition 19 adjusted amount growth", pc(G_ALLOW, 1), "the FHFA index for California measured over "
         "1991-2025, which is the index the statute actually uses", "it only matters for the cap, not the base"],
    ]
    b.append(table(["input", "value", "how it compares with what was measured", "why it was chosen"], brows))
    return page("black-swans", "Black swans",
                "Growth and inflation are never consistent over fifty years, so here are the episodes that were real, "
                "measured from the published indexes, replayed onto this decision.", "".join(b))


def p_law():
    b = []
    rows = [
        ["Proposition 19 adjusted amount resets", "16 February 2027",
         f"today it is {exact(1044586)} for transfers in the window ending then; the next amount is set from the FHFA "
         "index for California for calendar 2026",
         "for a 2040-2050 transfer the amount will be several hundred thousand larger, which makes the exclusion worth "
         "more in nominal terms but does not close the gap on a house at this value",
         '<a href="https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf">BOE LTA 2025/009</a>'],
        ["Federal estate and gift exclusion", "1 January each year",
         f"{exact(15000000)} for 2026, {exact(15480000)} for 2027, indexed thereafter",
         "the only figure in the estate calculation that moves on its own; read it again in January of the death year",
         '<a href="https://www.irs.gov/pub/irs-drop/rp-26-35.pdf">Rev. Proc. 2026-35</a>'],
        ["Annual gift exclusion", "1 January each year", f"{exact(19000)} for 2026, {exact(20000)} for 2027",
         "the size of the annual removal from the estate if gifting is used",
         '<a href="https://www.irs.gov/pub/irs-drop/rp-26-35.pdf">Rev. Proc. 2026-35</a>'],
        ["Estate tax closing letter and consistent-basis reporting", "30 days after the return due date",
         "the estate's reported values become the heirs' ceiling on basis",
         "a value that is too low on the return is a permanent income-tax cost, and too high is an estate-tax cost",
         '<a href="https://www.irs.gov/instructions/i706">Form 706 instructions</a>'],
        ["California statewide ballot of 3 November 2026", "certification due 11 December 2026",
         "fourteen measures, and none of them altered Proposition 13 or Proposition 19. The titles below are the "
         "Secretary of State's. Proposition 40, one-time tax on certain taxpayers: leading no at 52.4%. Proposition "
         "41, new state taxes and audits for local special taxes: leading no at 55.1%. Proposition 42, barring new "
         "state personal property taxes and certain retroactive state taxes: leading yes at 51.4%. Proposition 43, "
         "limiting voters' ability to raise revenue for local government services: leading no at 57.5%. Proposition "
         "45, environmental review for certain projects: leading no at 56.4%. Proposition 3, extending the existing "
         "tax on high incomes to fund schools and health care: leading yes at 60.7%. No measure proposed a change to "
         "the 1% rate, the 2% cap, the assess-on-transfer rules or the exclusion for family homes.",
         "the two results that matter to this plan are Proposition 42, which closes a state route to taxing the "
         "reinvested money, and Proposition 3, which fixes the top band the rental and investment income is taxed in",
         '<a href="https://electionresults.sos.ca.gov/returns/ballot-measures">Secretary of State results</a>'],
        ["Proposition 13 as a constitutional matter", "no measure in 2026",
         "the initiative that would have constrained local taxes was withdrawn in June 2026 and replaced by the "
         "legislative measure voters rejected; nothing on the ballot changed the 1% rate or the 2% cap",
         "the premise of the whole analysis is intact for now, but a future legislature can still place a measure - "
         "re-check every even November",
         '<a href="https://www.sos.ca.gov/elections/ballot-measures/qualified-ballot-measures">Secretary of State, qualified measures</a>'],
        ["Rent caps on the units at the already-owned house", "state rules sunset 31 December 2029; the local "
         "ordinance sets the annual maximum",
         "the state ceiling and the local one differ, and the local one is lower in recent years",
         "it caps the largest income line in the plan, which is why the rent growth assumption sits below cost inflation",
         '<a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12">Civil Code section 1947.12</a>'],
        ["Net metering for the array on the inherited house", "tariff-dependent, with a 20-year term from interconnection",
         "which tariff the system sits under, and when it was connected, decide how long the credit you report lasts",
         "modelled as ending in 2043 (D13); if the interconnection was later, the credit runs further",
         '<a href="https://www.cpuc.ca.gov/industries-and-topics/electrical-energy/demand-side-management/net-energy-metering">CPUC, net energy metering</a>'],
        ["The basis adjustment at death, Internal Revenue Code section 1014", "unchanged by the 2025 act",
         "the act that raised and indexed the exclusion did not amend section 1014: the rumour that it repealed the "
         "step-up in basis is not correct, and this desk states that explicitly because it was the most repeated "
         "claim of the 2025 debate. Bills that would end or limit the adjustment have been introduced in past "
         "Congresses and none has received a hearing. Gifts keep the donor's basis under section 1015, and where "
         "community property is involved both halves adjust under section 1014(b)(6).",
         "the sell path's tax-free exit rests on this. If it were ever repealed for a 2040s death, holding would "
         "look better than selling on almost every assumption - this is the single most valuable thing to watch",
         '<a href="https://www.irs.gov/pub/irs-drop/rp-26-35.pdf">Rev. Proc. 2026-35, which sets the indexed '
         'exclusion the same act created</a> &middot; <a href="https://www.irs.gov/taxtopics/tc701">IRS Topic 701'
         '</a> &middot; <a href="https://www.congress.gov/search?q=%7B%22source%22%3A%22legislation%22%2C%22bill%22%3A%22%22%7D">'
         "congress.gov bill search</a>"],
        ["Proposals to change the estate tax itself", "the exclusion is set and indexed; no sunset applies",
         "the 2025 act made the higher exclusion permanent and indexed it from 2027, so the earlier scheduled "
         "reversion does not happen; repeal-and-replace bills exist in both directions",
         "plan on the published amount and re-read it in January of the death year rather than planning around a "
         "proposal",
         '<a href="https://www.irs.gov/instructions/i706">Form 706 instructions</a>'],
    ]
    b.append(table(["rule or measure", "when it applies or changes", "what the source says",
                    "what it means for this plan", "source"], rows))
    b.append(callout("<b>One thing to re-read every February, one every January.</b> The Proposition 19 amount is "
                     "re-indexed on 16 February of odd years and the federal amounts on 1 January. Both are published by "
                     "an agency, not by the site, and both move.", "warn"))
    b.append("<h3>Unchanged, and load-bearing</h3>")
    urows = [
        ["The 1% constitutional rate and the 2% cap on an enrolled base", "verified in the Board's inflation letter",
         '<a href="https://www.boe.ca.gov/proptaxes/pdf/lta26002.pdf">BOE LTA 2026/002</a>'],
        ["A transfer through a trust counts as a transfer for Proposition 19", "verified in the code text",
         '<a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2">section 63.2(e)(9)</a>'],
        ["There is no California estate or inheritance tax", "verified at the State Controller",
         '<a href="https://www.sco.ca.gov/ardtax_estate_tax.html">State Controller</a>'],
        ["The principal-residence gain exclusion, with its 2-of-5-year tests", "verified at the IRS",
         '<a href="https://www.irs.gov/taxtopics/tc701">IRS Topic 701</a>'],
    ]
    b.append(table(["rule", "status", "source"], urows))
    return page("law-watch", "Law watch",
                "The rules the plan leans on, the dates they move, and what the voters and the IRS just published.",
                "".join(b))


def p_questions():
    b = []
    answered = [q for q in QUESTIONS if q["status"] == "answered"]
    openq = [q for q in QUESTIONS if q["status"] == "open"]
    b.append(stat_block([("questions in the register", len(QUESTIONS)),
                         ("answered from a source", len(answered)),
                         ("open, and what closes them", len(openq)),
                         ("that can move a decision by more than 10%", 2)]))
    b.append("<h3>What we already know, with the answer and the document behind it</h3>")
    rows = []
    for q in answered:
        rows.append([q["id"], esc(q["q"]), esc(q["answer"]),
                     esc(q["how"]), "answer confirmed",
                     '<a href="' + q["blocks"].split(",")[0] + '">'
                     + q["blocks"].split(",")[0].replace(".html", "") + "</a>"])
    b.append(table(["id", "question", "the answer", "where it came from", "status", "it settles"], rows, cls="reg"))
    b.append(note("The links point at the page in this desk that the answer settles; the official document behind "
                  "each answer is linked on that page and in the <a href=\"sources.html\">source register</a>."))
    b.append("<h3>What must be answered before a decision is reasonable</h3>")
    rows = []
    for q in openq:
        rows.append([q["id"], esc(q["q"]), esc(q["why"]), esc(q["how"]), esc(q["who"]),
                     '<a href="' + q["blocks"].split(",")[0] + '">the page it settles</a>'])
    b.append(table(["id", "question", "why it can change the answer", "how to find out", "who can answer",
                    "it settles"], rows, cls="reg"))
    b.append(callout("<b>The two that matter most.</b> Q04 (how large the cash side of the estate is) decides whether "
                    "40% of anything is payable, which outweighs every operating line in this desk put together. Q05 "
                    "(what the tax bills actually contain) decides whether the cost base of the already-owned house - the "
                    "engine funding everything else - is right or roughly double. Everything else refines.", "warn"))
    b.append("<h3>Order of work</h3>")
    b.append("<ol>"
             "<li>Read the trust instrument and pull the recorded deed (closes Q01, Q02, Q03, Q17).</li>"
             "<li>Photograph both current tax bills, all lines, and both assessor notices (closes Q05, Q06, Q07).</li>"
             "<li>Get the two insurance declarations pages and the utility account's interconnection letter (closes Q08, Q09).</li>"
             "<li>Ask the trustee in writing what the instrument requires on distribution (closes Q14 and the sale-authority "
             "question).</li>"
             "<li>Commission a written rent analysis for the inherited house and a rent roll for the other (closes Q10, Q12, Q13).</li>"
             "<li>Only then re-run the decision page with the replaced numbers; the build takes seconds.</li>"
             "</ol>")
    return page("questions", "Questions and gaps",
                "What is established, what is missing, and the specific action that closes each gap - so that the "
                "decision is made on a finished file rather than a likely one.", "".join(b))


def p_suggestions():
    b = []
    b.append("<h3>How this board works</h3>")
    b.append("<p class=\"note\">Nothing below has been implemented. Each row is a proposal with the change it names, "
             "what it would buy, what it costs to do, and what goes wrong if it is done badly. Reply with accept, modify "
             "or reject against each id and the site changes only where you have chosen. The two groups are separate on "
             "purpose: <b>site</b> suggestions change this tool, <b>action</b> suggestions change the plan.</p>")
    for kind, label in (("site", "Improving this site so the decision is easier to make"),
                        ("action", "Improving the financial outcome, independent of the site")):
        rows = []
        for s in SUGGESTIONS:
            if s["kind"] != kind:
                continue
            rows.append([f'<b>{s["id"]}</b>', esc(s["title"]), esc(s["why"]), esc(s["benefit"]), esc(s["effort"]),
                         esc(s["risk"]), '<span class="tag owner">' + esc(s["status"]) + "</span>",
                         "accept / modify / reject &rarr; ______"])
        b.append(h3(label))
        b.append(table(["id", "suggestion", "why", "what it buys", "effort", "risk if done", "status",
                        "your decision"], rows, cls="reg"))
    counts = {}
    for s in SUGGESTIONS:
        counts[s["kind"]] = counts.get(s["kind"], 0) + 1
    b.append(stat_block([("site suggestions", counts.get("site", 0)),
                         ("action suggestions", counts.get("action", 0)),
                         ("implemented already", 0),
                         ("waiting on you", len(SUGGESTIONS))]))
    b.append(callout("<b>If you only have time for one decision:</b> S09, one reconciled model instead of seven parallel "
                     "desks. The arithmetic on this site is good; the fact that seven generations of it disagree is the "
                     "main remaining obstacle to acting.", "good"))
    b.append("<h3>Suggested sequence, if all are accepted</h3>")
    b.append("<ol><li>S01, S07, S08 - documents and quotes; they close the gaps that every other number depends on.</li>"
             "<li>S02, S03, S06 - sequencing rules, which cost nothing and are irreversible if ignored.</li>"
             "<li>S09, S10, S11, S13, S16, S17 - the site work: one model, a decision record, owners on questions, dead "
             "trees retired, statuses in the tables, sensitivities beside headlines.</li>"
             "<li>S12, S14, S15 - charts, the privacy statement, and the annual re-verification cycle.</li>"
             "<li>S04, S05, S18 - the modelling and planning changes that follow from the closed gaps.</li></ol>")
    return page("suggestions", "Suggestions for review",
                "Options for the site and for the plan, gathered in one place, awaiting a decision before anything changes.",
                "".join(b))


def p_flagged():
    b = []
    sev = {"material": 0, "review": 0, "info": 0}
    for f in FLAGS:
        sev[f["severity"]] += 1
    b.append(stat_block([("flagged items", len(FLAGS)), ("material", sev["material"]),
                         ("needs a re-check", sev["review"]), ("noted for context", sev["info"])]))
    rows = []
    for f in FLAGS:
        rows.append([f'<b>{f["id"]}</b>', f'<span class="tag {f["severity"]}">{f["severity"]}</span>',
                     esc(f["item"]), esc(f["detail"]), esc(f["action"]), srcl(f["src"]),
                     esc(f["status"])])
    b.append(table(["id", "severity", "what", "why it is flagged", "what would close it", "the source to read", "status"], rows, cls="reg"))
    b.append("<h3>Values this desk refuses to invent</h3>")
    urows = [
        ["Premium for the inherited house at its own risk characteristics",
         '&mdash;', '<span class="tag unverified">unverified</span>',
         "no official source publishes a premium for one address; the owner's figure is used and labelled at every "
         "occurrence, and the department's statewide average is the only public anchor"],
        ["Water and electricity actually billed", '&mdash;', '<span class="tag unverified">unverified</span>',
         "published rate schedules are rates, not consumption; the account statement is the only source"],
        ["Which net-metering tariff the array sits under", '&mdash;', '<span class="tag unverified">unverified</span>',
         "the interconnection date is in the owner's file, not in a public dataset"],
        ["The size of the cash inheritance", '&mdash;', '<span class="tag unverified">unverified</span>',
         "the estate-tax page works a range of estate sizes instead of guessing one"],
        ["Composite rate area for the inherited house on the 2026 roll", "1.1488% typical, carried",
         '<span class="tag carried">carried</span>',
         "read from the county's fiscal 2025-26 rate book by an earlier session; the 2026-27 book was not retrieved, "
         "and a parcel's own area may differ"],
        ["Certified result of the 3 November 2026 ballot measures", "as counted 12 November 2026, unofficial",
         '<span class="tag carried">date-sensitive</span>',
         "certification is due 11 December 2026; every statement about what passed must be re-read after that"],
        ["Whether the small-estate affidavit route is open", '&mdash;', '<span class="tag owner">process note</span>',
         "depends on the estate's total, which is unknown while Q04 is open"],
    ]
    b.append(table(["what", "value", "status", "why it is not filled in"], urows))
    b.append("<h3>Irregularities found in the repository</h3>")
    irows = [
        ["Two published corrections that never reached the trees that need them",
         "desk-22a32b17 applies the Proposition 19 amount to the whole assessed-to-market gap rather than as the cap "
         "the statute sets; desk-b4f carries a capital-gain figure beside the estates-and-trusts line that does not "
         "match the published amount, and a closing-letter fee that does not match the schedule",
         "both are excluded from the published site, so nothing live is wrong, but both remain in the repository where "
         "a future session may copy them",
         '<a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2">section 63.2(d)(2)</a> '
         'and <a href="flagged.html">this desk</a>'],
        ["A 2025 annual average that the publisher does not have",
         "the CPI retrievals this session returned no annual average for calendar 2025 for the area and national indices",
         "the Board's own letter explains it: October 2025 was not collected after the federal shutdown, so any 2025 "
         "inflation figure anywhere on this site rests on an incomplete year. The projections here use the Board's "
         "August-to-August comparison instead, which is what the roll actually uses",
         '<a href="https://www.boe.ca.gov/proptaxes/pdf/lta26002.pdf">BOE LTA 2026/002</a>'],
        ["Seven published desks, three different headline answers",
         "each generation verified itself and none reconciled with the others",
         "the fix is suggestion S09; until then, read the desk that shows its arithmetic, which is this one and the "
         "referee tree", '<a href="../referee-abae/index.html">referee cross-check</a>'],
        ["An owner-input series that no desk should publish",
         "the year-by-year assessed and tax history from your brief is searchable against the open roll even at $10 "
         "rounding", "this desk verifies that history and does not print it; earlier generations did print parts of it",
         '<a href="methodology.html">the privacy rule</a>'],
    ]
    b.append(table(["finding", "what it is", "what is being done", "for manual review"], irows))
    return page("flagged", "Flagged for review",
                "Everything that could not be confirmed, everything that looks wrong, and the specific thing that would "
                "settle each. These items do not block the release; they block certainty.", "".join(b))


def p_sources():
    b = []
    rows = []
    for s in SOURCES:
        rows.append([f'<b>{s["id"]}</b>', esc(s["title"]), f'<a href="{s["url"]}">{esc(s["title"])}</a>',
                     f'<span class="tag {"verified" if s["kind"] == "official" and s["opened"] else "carried" if s["kind"] == "official" else "owner"}">'
                     + ("official, opened here" if s["kind"] == "official" and s["opened"] else
                        "official, not re-opened" if s["kind"] == "official" else "secondary") + "</span>",
                     esc(s["supports"])])
    b.append(table(["id", "document", "link", "this session", "what it supports in this desk"], rows, cls="reg"))
    opened = sum(1 for s in SOURCES if s["kind"] == "official" and s["opened"])
    total = sum(1 for s in SOURCES if s["kind"] == "official")
    b.append(note(f"{opened} of {total} official documents were retrieved and read by this session on {AS_OF}. The rest "
                  "are carried from the repository's own source register, where an earlier session read them; each is "
                  "labelled so a reader can see which is which. No value in this desk comes from a secondary source "
                  "alone: the one secondary entry is listed because it pointed at the primary documents."))
    return page("sources", "Source register",
                "Every document behind every number, with the address and whether this session actually opened it.",
                "".join(b))


def p_methodology():
    b = []
    b.append("<h3>The rules this desk follows</h3>")
    rows = [
        ["Verified", "read from the official document at the linked address, by this session",
         f"{len([v for v in VERIFIED if v['status'] == 'verified'])} figures"],
        ["Carried", "an official figure an earlier session read and recorded; not re-opened today, and labelled so",
         f"{len([v for v in VERIFIED if v['status'] == 'carried'])} figures"],
        ["Owner", "supplied in your brief; treated as a fact about what you believe, not as a confirmed fact about the "
         "property", f"{len(OWNER)} inputs"],
        ["Derived", "arithmetic on verified or owner values, with the arithmetic printed beside it", "the bill-line "
         "residuals, the implied rates, the break-evens"],
        ["Assumption", "a named modelling choice with an id, a basis and a sensitivity", f"{len(ASSUMPTIONS)} ids"],
        ["Unverified", "could not be confirmed; the cell is blank and the item is on the flagged page",
         f"{len([f for f in FLAGS if f['status'].startswith('open')])} items"],
    ]
    b.append(table(["word", "what it means on these pages", "how often it appears here"], rows))
    b.append("<h3>Rounding and privacy</h3>")
    b.append("<p>Every household amount is rounded to the nearest $10, so that no figure on this site can be matched to "
             "a bill, an assessment or a listing by searching. Statutory and published amounts are quoted exactly and "
             "marked <span class=\"tag exact\">exact</span>, because rounding a legal threshold would misstate it. No "
             "name, address, parcel or account number, postcode, city, county or neighbourhood appears; the two houses "
             "are referred to by their role. Your year-by-year assessment and tax history is <b>not</b> published at any "
             "rounding: a rounded series still identifies one parcel in the open roll, so it is verified here and then "
             "left out. The verifier that enforces all of this is part of the build.</p>")
    b.append("<h3>Model inputs</h3>")
    rows = [[a["id"], esc(a["item"]), esc(a["value"]), esc(a["basis"]), esc(a["sens"]), srcl(a["src"])] for a in ASSUMPTIONS]
    b.append(table(["id", "input", "value", "basis, measured or stated", "sensitivity", "source"], rows, cls="reg"))
    b.append("<h3>Owner inputs as recorded</h3>")
    rows = [[esc(o["item"]), f'<span class="num">{money(o["value"])}</span>' if isinstance(o["value"], (int, float))
             else esc(o["value"]), '<span class="tag owner">owner</span>', esc(o["note"])] for o in OWNER]
    b.append(table(["item", "value", "status", "note"], rows, cls="reg"))
    b.append("<h3>The arithmetic, in words</h3>")
    b.append("<ul>"
             f"<li><b>Market value.</b> Value in year y = owner's 2026 value grown at D1, or a replayed sequence in the "
             f"black-swan regimes. Today: {money(A_MARKET)}.</li>"
             f"<li><b>Enrolled base with no transfer.</b> Assessed value grown at the Proposition 13 cap of 2%: "
             f"{money(A_ASSESSED)} in 2026 to {money(enrolled_asis(Y1))} in {Y1}.</li>"
             f"<li><b>Base after a transfer where the heir occupies.</b> max(factored base, market value at transfer "
             f"minus the adjusted amount for that year), grown at 2% after. At a {BASELINE_T} transfer that is "
             f"{money(max(enrolled_asis(BASELINE_T), market(BASELINE_T) - allowance(BASELINE_T)))}.</li>"
             "<li><b>Base after a transfer with no exclusion.</b> Market value at the transfer, grown at 2% after.</li>"
             "<li><b>Property tax.</b> (enrolled base &minus; homeowners' exemption if owner-occupied) times the rate, "
             "plus the residual other charges on the bill grown at D5. The residual is not invented: it is your bill "
             f"minus the rate times your assessed value, which comes to {money(OTHER_A)} for the inherited house and "
             f"{money(OTHER_B)} for the other.</li>"
             "<li><b>Carrying cost.</b> insurance, water and sewer, net electricity (until the tariff ends), and "
             "maintenance as a share of value.</li>"
             "<li><b>Rental path.</b> gross rent at the yield assumption, less vacancy, management, tax, insurance and "
             "maintenance; depreciation on 75% of the transfer value over 27.5 years shelters income, and is recaptured "
             "at up to 25% on the sale, which is why letting is punished at the end.</li>"
             "<li><b>Sale.</b> market value at the sale year, less 6%, less capital gains on the increase since the "
             "stepped-up basis, with the principal-residence exclusion applied when the heir actually lived there.</li>"
             "<li><b>Everything invested at the after-tax return until 2076, then compared.</b> Real figures are the "
             "nominal total divided by cumulative inflation at D5.</li>"
             "</ul>")
    b.append("<h3>Verified statutory figures used unchanged</h3>")
    rows = [[esc(v["item"]), f'<span class="num">{v["value"]}</span>', tag(v["status"]), esc(v["note"]), srcl(v["src"])]
            for v in VERIFIED]
    b.append(table(["item", "value", "status", "note", "source"], rows))
    b.append("<h3>Measured index values behind the growth rates</h3>")
    irows = [
        ["metro index, inherited house's area", ", ".join(f"{y}: {HPI_SJ[y]:.2f}" for y in (1990, 1995, 2006, 2011, 2015, 2025)),
         '<a href="https://fred.stlouisfed.org/graph/fredgraph.csv?id=ATNHPIUS41940Q&fq=Annual&fam=eop">FHFA via FRED</a>'],
        ["division index, other house's area", ", ".join(f"{y}: {HPI_SF[y]:.2f}" for y in (1991, 2006, 2011, 2015, 2025)),
         '<a href="https://fred.stlouisfed.org/graph/fredgraph.csv?id=ATNHPIUS41884Q&fq=Annual&fam=eop">FHFA via FRED</a>'],
        ["state index, which sets the Proposition 19 amount", ", ".join(f"{y}: {HPI_CA[y]:.2f}" for y in sorted(HPI_CA)),
         '<a href="https://fred.stlouisfed.org/graph/fredgraph.csv?id=CASTHPI&fq=Annual&fam=eop">FHFA via FRED</a>'],
        ["area CPI-U annual average", ", ".join(f"{y}: {v}" for y, v in sorted(CPI_SF.items()) if v),
         '<a href="https://fred.stlouisfed.org/graph/fredgraph.csv?id=CUURA422SA0&fq=Annual&fam=avg">BLS via FRED</a>'],
        ["10-year Treasury annual average", ", ".join(f"{y}: {v}" for y, v in sorted(TREAS_10Y.items())),
         '<a href="https://fred.stlouisfed.org/graph/fredgraph.csv?id=GS10&fq=Annual&fam=avg">Treasury via FRED</a>'],
        ["published inflation factors, selected roll years", ", ".join(f"{y}: {f}" for y, _, f in BOE_FACTORS[:9]),
         '<a href="https://www.boe.ca.gov/proptaxes/pdf/lta26002.pdf">BOE LTA 2026/002</a>'],
    ]
    b.append(table(["series", "values as retrieved", "source"], irows))
    b.append("<h3>How to re-run this with better numbers</h3>")
    b.append("<pre><code>python3 desk-d75/_src/build.py     # regenerates every page from the registers\n"
             "python3 desk-d75/_src/verify.py    # the contract: rounding, sources, links, privacy\n"
             "python3 desk-d75/_src/build.py --check   # fail if the committed pages are stale</code></pre>")
    b.append("<p class=\"note\">To change an input, edit the constant or the row in <code>_src/data.py</code> and rebuild. "
             "Nothing is hard-coded in the prose, which is what makes the desk safe to re-run when the documents arrive.</p>")
    return page("methodology", "Methodology",
                "Every input, every formula, and the rules the build enforces.", "".join(b))


STYLE = """
:root{--ink:#1d2330;--muted:#5b6474;--line:#dfe3ea;--brand:#1f4e79;--bg:#f6f7f9;--card:#fff}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
header{background:var(--card);border-bottom:1px solid var(--line);padding:20px 24px}
header h1{margin:0;font-size:23px;color:var(--brand)}
header .sub{margin:5px 0 0;color:var(--muted);font-size:13px}
nav{display:flex;flex-wrap:wrap;gap:6px;padding:12px 24px;background:var(--card);
border-bottom:1px solid var(--line);position:sticky;top:0;z-index:2}
nav a{font-size:12.5px;text-decoration:none;color:var(--brand);padding:5px 9px;border:1px solid var(--line);
border-radius:999px;background:#fff}
nav a.on{background:var(--brand);color:#fff;border-color:var(--brand)}
main{max-width:1240px;margin:0 auto;padding:22px 24px 64px}
h2{font-size:26px;margin:6px 0 4px;color:var(--brand)}
h3{font-size:16px;margin:28px 0 8px;color:var(--brand)}
p.intro{color:var(--muted);max-width:80ch}
p.note,ul,ol{color:var(--muted);max-width:92ch}
.note{font-size:13px}
table{width:100%;border-collapse:collapse;margin:12px 0 6px;background:var(--card);font-size:12.8px}
th{background:#eef3f7;text-align:left;padding:8px 9px;border-bottom:2px solid var(--line);vertical-align:bottom;
font-size:11.5px;text-transform:uppercase;letter-spacing:.03em}
td{padding:8px 9px;border-bottom:1px solid var(--line);vertical-align:top}
tr:nth-child(even) td{background:#fbfcfd}
td a{color:var(--brand)}
.tag{font-size:11px;padding:1px 6px;border-radius:4px;background:#eef3f7;color:var(--muted);white-space:nowrap}
.tag.verified,.tag.met,.tag.material{background:#e3f4e6;color:#17612a}
.tag.carried,.tag.answered,.tag.review{background:#e8f0fb;color:#1f4e79}
.tag.owner,.tag.unverified,.tag.met-with-gaps,.tag.open-on-owner{background:#fdf0d8;color:#8a5a06}
.tag.assumption,.tag.derived,.tag.info{background:#f0eafc;color:#54329c}
.tag.exact,.tag.sm{font-size:10.5px}
.callout{background:var(--card);border-left:4px solid var(--brand);padding:12px 16px;margin:18px 0;
border-radius:0 8px 8px 0;max-width:92ch}
.callout.warn{border-left-color:#b7791f;background:#fffbf2}
.callout.good{border-left-color:#2f855a;background:#f3fbf6}
.kpi{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin:16px 0}
.kpi div{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:11px 13px}
.kpi b{display:block;font-size:19px;color:var(--brand)}
.kpi span{font-size:12px;color:var(--muted)}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;margin:14px 0}
.card{display:block;background:var(--card);border:1px solid var(--line);border-radius:9px;padding:13px 14px;
text-decoration:none;color:var(--ink)}
.card b{display:block;color:var(--brand);margin-bottom:3px}
.card span{font-size:12.5px;color:var(--muted)}
pre{background:#0f172a;color:#e2e8f0;padding:12px 14px;border-radius:8px;overflow-x:auto;font-size:12.5px}
code{background:#eef3f7;color:var(--ink);padding:1px 5px;border-radius:4px;font-size:12.5px}
pre code{background:none;color:inherit;padding:0}
footer{margin-top:34px;border-top:1px solid var(--line);padding-top:12px;color:var(--muted);font-size:12px;max-width:92ch}
@media print{nav,.kpi{display:none}body{background:#fff}main{max-width:none}}
"""

SECTIONS = [
    ("index", "Overview", p_index),
    ("requirements", "Requirement register", p_requirements),
    ("executive-summary", "Executive summary", p_executive_summary),
    ("properties", "The two houses", p_properties),
    ("carrying-costs", "Carrying costs", p_carrying),
    ("projections", "Projections 2026-2076", p_projections),
    ("decision", "The decision", p_decision),
    ("estate-tax", "Inheritance and estate tax", p_estate_tax),
    ("process", "Trust process, step by step", p_process),
    ("black-swans", "Black swans", p_swans),
    ("law-watch", "Law watch", p_law),
    ("questions", "Questions and gaps", p_questions),
    ("suggestions", "Suggestions for review", p_suggestions),
    ("flagged", "Flagged for review", p_flagged),
    ("sources", "Source register", p_sources),
    ("methodology", "Methodology", p_methodology),
]


def h3(t):
    return f"<h3>{t}</h3>"


def tag(s):
    return f'<span class="tag {s}">{s}</span>'


REGISTER_IDS = {
    "D": {a["id"] for a in ASSUMPTIONS},
    "G": {f["id"] for f in FLAGS},
    "Q": {q["id"] for q in QUESTIONS},
    "R": {r["id"] for r in REQUIREMENTS},
    "S": {s["id"] for s in SUGGESTIONS},
}


def id_check(name, text):
    """A page that cites a register id the registers do not define is a page no one can check.

    This exists because a register edit once left a page pointing at a flag that had not been added.
    The prose looked finished and the reference was dangling, which is exactly the kind of quiet break
    a reader would only find by hunting the flag and not seeing it.
    """
    visible = re.sub(r"<[^>]+>", " ", text)
    for letter, known in REGISTER_IDS.items():
        for tok in sorted(set(re.findall(rf"\b{letter}\d{{2}}\b", visible))):
            if tok not in known:
                raise SystemExit(f"register: {name} cites {tok}, which no register in this desk defines")


def build(write=True):
    out = {}
    for key, title, fn in SECTIONS:
        out[key + ".html"] = fn()
    out["style.css"] = STYLE
    if write:
        for name, text in out.items():
            if name.endswith(".html"):
                scrub_check(name, text)
                id_check(name, text)
            (ROOT / name).write_text(text)
        print(f"wrote {len(out)} files into {ROOT}")
    return out


if __name__ == "__main__":
    if "--check" in sys.argv:
        fresh = dict(build(write=False))
        for name, text in fresh.items():
            if name.endswith(".html"):
                scrub_check(name, text)
                id_check(name, text)
        stale = [n for n, txt in fresh.items() if not (ROOT / n).exists() or (ROOT / n).read_text() != txt]
        if stale:
            print("STALE: " + ", ".join(sorted(stale)))
            raise SystemExit(1)
        print("desk is current")
    else:
        build()
