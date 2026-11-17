# -*- coding: utf-8 -*-
"""Model for desk-5b7b4e6b (session arena-5b7b4e6b, 2026-11-17).

Two ideas run through everything here.

1. Ranges, not round numbers. Every uncertain quantity is a low / base / high band. The
   bands are propagated through the arithmetic, so a result is reported as a band too and
   the reader can see which input moves it.

2. Real conditions, not a constant growth rate. The 1976-2025 record of official series
   (BLS price indexes, FHFA house price indexes, the Economic Report of the President's
   stock tables, and the Treasury rate series) is resampled in contiguous five-year blocks.
   A block keeps the joint behaviour of the years inside it, so a decade of high inflation
   arrives with the house-price and equity behaviour of that same decade. Nothing is held
   constant for fifty years.

Every figure the model reports is derived. Nothing in this file is a forecast.
"""

from __future__ import annotations

import math
import random
from statistics import mean, median

from data import (CPI_US, CPI_SF, CPI_SF_RENT, TB3MS, GS10, HPI_SJ, HPI_SF,
                  SP500, SP500_DIV, OFFICIAL, OWNER, REGIMES,
                  HISTORY_START, HISTORY_END)

# ---------------------------------------------------------------------------
# 1. Year-on-year changes from the official levels
# ---------------------------------------------------------------------------


def yoy(series: dict[int, float]) -> dict[int, float]:
    """Year-on-year change, as a fraction. The first year has no prior year and is absent."""
    out = {}
    years = sorted(series)
    for prev, cur in zip(years, years[1:]):
        out[cur] = series[cur] / series[prev] - 1.0
    return out


INFL_US = yoy(CPI_US)
INFL_SF = yoy(CPI_SF)
INFL_SF_RENT = yoy(CPI_SF_RENT)
HPI_SJ_G = yoy(HPI_SJ)
HPI_SF_G = yoy(HPI_SF)


def equity_total_return() -> dict[int, float]:
    """Price change plus the dividend-price ratio published for the same year.

    This is the standard total-return approximation from the Economic Report of the
    President tables: the index is a price index, and the dividend-price ratio is the
    income component. It is an approximation, not a published total-return series, and
    every page that uses it says so.
    """
    out = {}
    for year in sorted(SP500):
        if year - 1 not in SP500:
            continue
        price_change = SP500[year] / SP500[year - 1] - 1.0
        out[year] = price_change + SP500_DIV[year] / 100.0
    return out


EQ = equity_total_return()

# The joint record. One row per historical year; a missing cell means the official
# response does not carry that value for that year.
HISTORY: list[dict] = []
for _y in range(HISTORY_START, HISTORY_END + 1):
    HISTORY.append({
        "year": _y,
        "infl_us": INFL_US.get(_y),
        "infl_sf": INFL_SF.get(_y),
        "rent_sf": INFL_SF_RENT.get(_y),
        "hpi_a": HPI_SJ_G.get(_y),
        "hpi_b": HPI_SF_G.get(_y),
        "equity": EQ.get(_y),
        "tb3": TB3MS.get(_y),
        "gs10": GS10.get(_y),
    })
HISTORY = [h for h in HISTORY
           if None not in (h["infl_sf"], h["rent_sf"], h["hpi_a"], h["hpi_b"],
                           h["equity"], h["tb3"], h["gs10"], h["infl_us"])]


# ---------------------------------------------------------------------------
# 2. What the record actually looked like — regime table
# ---------------------------------------------------------------------------

def regime_table() -> list[dict]:
    rows = []
    for start, end, name in REGIMES:
        years = [h for h in HISTORY if start <= h["year"] <= end]
        if not years:
            continue
        rows.append({
            "name": name,
            "start": start,
            "end": end,
            "years": len(years),
            "infl_us": mean(h["infl_us"] for h in years),
            "infl_sf": mean(h["infl_sf"] for h in years),
            "rent": mean(h["rent_sf"] for h in years),
            "hpi_a": mean(h["hpi_a"] for h in years),
            "hpi_b": mean(h["hpi_b"] for h in years),
            "equity": mean(h["equity"] for h in years),
            "tb3": mean(h["tb3"] for h in years),
            "worst_equity": min(h["equity"] for h in years),
            "worst_hpi_a": min(h["hpi_a"] for h in years),
            "cum_hpi_a": math.prod(1 + h["hpi_a"] for h in years) - 1,
            "cum_equity": math.prod(1 + h["equity"] for h in years) - 1,
        })
    return rows


def record_summary() -> dict:
    eqs = [h["equity"] for h in HISTORY]
    hpi = [h["hpi_a"] for h in HISTORY]
    return {
        "years": len(HISTORY),
        "start": HISTORY[0]["year"],
        "end": HISTORY[-1]["year"],
        "equity_mean": mean(eqs),
        "equity_median": median(eqs),
        "equity_worst": min(eqs),
        "equity_best": max(eqs),
        "equity_down_years": sum(1 for e in eqs if e < 0),
        "hpi_a_mean": mean(hpi),
        "hpi_a_worst": min(hpi),
        "hpi_a_best": max(hpi),
        "hpi_a_down_years": sum(1 for h in hpi if h < 0),
        "infl_sf_mean": mean(h["infl_sf"] for h in HISTORY),
        "infl_sf_worst": max(h["infl_sf"] for h in HISTORY),
        "infl_sf_best": min(h["infl_sf"] for h in HISTORY),
        "tb3_mean": mean(h["tb3"] for h in HISTORY),
        "tb3_min": min(h["tb3"] for h in HISTORY),
        "tb3_max": max(h["tb3"] for h in HISTORY),
    }


# ---------------------------------------------------------------------------
# 3. Block resampling of the real record
# ---------------------------------------------------------------------------

def block_bootstrap(n_years: int, n_paths: int = 2000, block: int = 5,
                    seed: int = 20261117) -> list[list[dict]]:
    """Draw contiguous multi-year blocks of the real record, with wraparound.

    A block is drawn as a unit so that the inflation, house-price, equity and rate
    behaviour of those years arrives together, exactly as it happened. Sampling with
    replacement across the whole 1976-2025 record means any regime can follow any other,
    which is deliberately harder on the model than one straight-line assumption.
    """
    rng = random.Random(seed)
    n = len(HISTORY)
    paths = []
    for _ in range(n_paths):
        drawn = []
        while len(drawn) < n_years:
            start = rng.randrange(n)
            for k in range(block):
                drawn.append(HISTORY[(start + k) % n])
                if len(drawn) == n_years:
                    break
        paths.append(drawn)
    return paths


def pct(values: list[float], q: float) -> float:
    """Linear-interpolated percentile."""
    if not values:
        return 0.0
    s = sorted(values)
    if len(s) == 1:
        return s[0]
    pos = (len(s) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return s[int(pos)]
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


def band(values: list[float]) -> dict[str, float]:
    return {
        "p10": pct(values, 0.10),
        "p25": pct(values, 0.25),
        "median": pct(values, 0.50),
        "p75": pct(values, 0.75),
        "p90": pct(values, 0.90),
        "mean": mean(values),
    }


# ---------------------------------------------------------------------------
# 4. Property tax: fitted to the household's own bills, not to a round rate
# ---------------------------------------------------------------------------

def fit_bill(rows: list[tuple[float, float]]) -> dict:
    """Least-squares fit of  tax = rate * assessed + fixed, with a goodness-of-fit measure.

    `rows` is a list of (assessed value, tax bill) pairs. The split matters because the two
    halves behave differently under Proposition 13: the ad-valorem part grows with the
    assessed value, the fixed part (direct assessments and parcel charges) does not.

    A negative `fixed` means the split does not describe that bill — a household is not
    charged a negative fixed amount. Where that happens the fit is reported as unusable and
    the desk falls back to escalating the observed bill (see `bill_growth`).
    """
    n = len(rows)
    sx = sum(a for a, _ in rows)
    sy = sum(t for _, t in rows)
    sxx = sum(a * a for a, _ in rows)
    sxy = sum(a * t for a, t in rows)
    denom = n * sxx - sx * sx
    if denom == 0:
        return {"rate": 0.0, "fixed": sy / n, "r2": 0.0, "residuals": [], "usable": False}
    rate = (n * sxy - sx * sy) / denom
    fixed = (sy - rate * sx) / n
    ybar = sy / n
    sstot = sum((t - ybar) ** 2 for _, t in rows)
    residuals = [t - (rate * a + fixed) for a, t in rows]
    sse = sum(r * r for r in residuals)
    r2 = 1 - sse / sstot if sstot else 0.0
    return {
        "rate": rate,
        "fixed": fixed,
        "r2": r2,
        "residuals": residuals,
        "usable": fixed >= 0 and rate >= 0,
    }


def bill_growth(rows: list[tuple[float, float]], spans: list[int]) -> dict:
    """Observed compound annual growth of a bill over several look-back windows.

    Used where the ad-valorem split does not describe the bill. Returns one entry per
    window in `spans`, as a compound annual rate over the last `span` observations.
    """
    out = {}
    for span in spans:
        if len(rows) < span + 1:
            continue
        first = rows[-span - 1][1]
        last = rows[-1][1]
        years = span
        out[span] = (last / first) ** (1 / years) - 1 if first > 0 else 0.0
    return out


# The household's own history. These values are a public record tied to the two parcels, so
# they are used here to fit the rate and are never republished row by row.
_A_HISTORY = [
    (440_305, 5_965), (449_101, 6_130), (455_949, 6_414), (465_067, 6_383),
    (474_368, 6_383), (483_854, 6_565), (493_530, 6_565), (498_642, 6_662),
    (508_614, 6_755), (518_786, 6_917), (529_161, 7_003), (539_743, 7_207),
]
_B_HISTORY = [
    (96_557, 1_675), (98_488, 1_740), (100_456, 2_061), (102_465, 2_134),
    (104_513, 2_197), (105_595, 2_066), (107_662, 2_107), (109_814, 2_179),
    (112_008, 2_315), (114_248, 2_439),
]

A_FIT = fit_bill(_A_HISTORY)
B_FIT = fit_bill(_B_HISTORY)
A_RATE, A_FIXED = A_FIT["rate"], A_FIT["fixed"]

# B's fit is not usable: the fixed term comes out negative, which is not a real thing. The
# reason is visible in the household's own bills — B's bill grew 4.3% a year over 2016-2025
# while the assessed value grew 1.9% a year, so no constant ad-valorem rate plus a constant
# fixed charge describes it. B's bill is dominated by charges that escalate on their own
# schedule. B is therefore projected from its own observed growth, as a band.
B_BILL_GROWTH = bill_growth(_B_HISTORY, [3, 6, 9])
B_RATE, B_FIXED = 0.0, 0.0


def prop13_assessed(start_value: float, infl_path: list[float], years: int,
                    cap: float = OFFICIAL["prop13_cap"]) -> list[float]:
    """Prop 13 factored base year value: growth capped, and reduced in a falling market.

    The cap is the lesser of 2% and the change in the California Consumer Price Index.
    Where the index falls, the value falls with it (Proposition 8), floored at zero.
    """
    out = [start_value]
    v = start_value
    for i in range(years):
        change = infl_path[i] if i < len(infl_path) else cap
        applied = min(cap, change) if change > 0 else max(change, -0.10)
        v = max(v * (1 + applied), 0.0)
        out.append(v)
    return out


def annual_tax(assessed: float, rate: float, fixed: float) -> float:
    return assessed * rate + fixed


# ---------------------------------------------------------------------------
# 5. Sale taxes
# ---------------------------------------------------------------------------

CA_BRACKETS_2026_SINGLE = [
    (0, 11_456, 0.00, 0.0100),
    (11_456, 27_157, 114.56, 0.0200),
    (27_157, 42_861, 428.58, 0.0400),
    (42_861, 59_498, 1_056.74, 0.0600),
    (59_498, 75_197, 2_054.96, 0.0800),
    (75_197, 384_109, 3_310.88, 0.0930),
    (384_109, 460_927, 32_039.70, 0.1030),
    (460_927, 768_213, 39_951.95, 0.1130),
    (768_213, float("inf"), 74_675.27, 0.1230),
]
CA_BRACKETS_2026_JOINT = [
    (0, 22_912, 0.00, 0.0100),
    (22_912, 54_314, 229.12, 0.0200),
    (54_314, 85_722, 857.16, 0.0400),
    (85_722, 118_996, 2_113.48, 0.0600),
    (118_996, 150_394, 4_109.92, 0.0800),
    (150_394, 768_218, 6_621.76, 0.0930),
    (768_218, 921_854, 64_079.39, 0.1030),
    (921_854, 1_536_426, 79_903.90, 0.1130),
    (1_536_426, float("inf"), 149_350.54, 0.1230),
]


def ca_tax_on_income(income: float, joint: bool = False) -> float:
    """California income tax from the published 2026 rate schedules, plus the 1% over $1M."""
    brackets = CA_BRACKETS_2026_JOINT if joint else CA_BRACKETS_2026_SINGLE
    income = max(income, 0.0)
    tax = 0.0
    for lo, hi, base, rate in brackets:
        if income > lo:
            tax = base + rate * (min(income, hi) - lo)
    if income > OFFICIAL["ca_mhst_threshold"]:
        tax += OFFICIAL["ca_mhst_rate"] * (income - OFFICIAL["ca_mhst_threshold"])
    return tax


def ca_income_tax(gain: float, other_income: float = 0.0, joint: bool = False) -> float:
    """The California tax attributable to a gain, holding other income constant.

    California taxes capital gains as ordinary income (ftb_capgains); there is no separate
    capital-gain rate.
    """
    return max(ca_tax_on_income(gain + other_income, joint)
               - ca_tax_on_income(other_income, joint), 0.0)


def federal_tax_on_gain(gain: float, unrecaptured_1250: float = 0.0) -> float:
    """Federal tax on a long-term capital gain: 20%, plus 3.8% net investment income tax.

    Depreciation previously claimed comes back first as unrecaptured section 1250 gain at
    a maximum of 25%, then the remainder is taxed at the long-term rate.
    """
    recapture = min(unrecaptured_1250, max(gain, 0.0))
    rest = max(gain - recapture, 0.0)
    return (OFFICIAL["fed_unrecaptured_1250"] * recapture
            + OFFICIAL["fed_ltcg_top"] * rest
            + OFFICIAL["fed_niit"] * max(gain, 0.0))


def sale_proceeds(price: float, basis: float, costs_rate: float,
                  sec121_exclusion: float = 0.0,
                  unrecaptured_1250: float = 0.0,
                  other_income: float = 0.0) -> dict:
    """Net cash from a sale, after selling costs and both layers of tax on the gain."""
    costs = price * costs_rate
    net_price = price - costs
    gain_before = max(net_price - basis, 0.0)
    excluded = min(gain_before, sec121_exclusion)
    taxable_gain = gain_before - excluded
    recapture = min(unrecaptured_1250, taxable_gain)
    fed = federal_tax_on_gain(taxable_gain, recapture)
    state = ca_income_tax(taxable_gain - 0.0, other_income)
    net = net_price - fed - state
    return {
        "price": price,
        "costs": costs,
        "net_price": net_price,
        "basis": basis,
        "gain_before_exclusion": gain_before,
        "sec121_excluded": excluded,
        "taxable_gain": taxable_gain,
        "unrecaptured_1250": recapture,
        "federal_tax": fed,
        "california_tax": state,
        "total_tax": fed + state,
        "net_proceeds": net,
        "effective_rate_on_gain": (fed + state) / gain_before if gain_before else 0.0,
    }


# ---------------------------------------------------------------------------
# 6. The phased-investing path and the crash replays
# ---------------------------------------------------------------------------

def phased_entry(cash: float, park_months: int, phase_months: int,
                 cash_rate: float, equity_path: list[float]) -> float:
    """Park the proceeds in short Treasuries, then phase into equities.

    Convention, pinned by the unit tests: the money earns the cash rate during every month
    it is not invested; each monthly equity instalment is bought at the start of the month
    and earns that month's equity return. `equity_path` holds monthly returns.
    """
    monthly_cash = (1 + cash_rate) ** (1 / 12) - 1
    balance_cash = cash
    units = 0.0
    total = len(equity_path)
    for m in range(total):
        if m < park_months:
            balance_cash *= (1 + monthly_cash)
        elif m < park_months + phase_months:
            instalment = cash / max(phase_months, 1)
            units += instalment
            balance_cash -= instalment
            balance_cash *= (1 + monthly_cash)
        else:
            pass
        if m >= park_months:
            units *= (1 + equity_path[m])
    return units + balance_cash


def all_in(cash: float, equity_path: list[float]) -> float:
    """Buy at the start of month 0 and hold."""
    units = cash
    for r in equity_path:
        units *= (1 + r)
    return units


def monthly_from_annual(annual: list[float]) -> list[float]:
    """Turn a sequence of annual returns into a flat monthly sequence for a replay."""
    out = []
    for a in annual:
        m = (1 + a) ** (1 / 12) - 1
        for _ in range(12):
            out.append(m)
    return out


def crash_replay_1929(cash: float) -> list[dict]:
    """Replay the official 1929 drawdown against three ways of entering the market.

    Endpoints are those published by Federal Reserve History: the Dow stood at 381 in
    September 1929, closed at 41.22 in the summer of 1932, 89% below the peak, and did not
    regain the pre-crash level until November 1954. The drawdown is modelled as a steady
    monthly decline over 34 months from peak to trough, then a steady monthly recovery to
    the pre-crash level 298 months after the peak.
    """
    peak_to_trough_months = 34
    drawdown = -0.89
    trough_to_recovery_months = 298 - peak_to_trough_months
    down_m = (1 + drawdown) ** (1 / peak_to_trough_months) - 1
    up_m = (1 / (1 + drawdown)) ** (1 / trough_to_recovery_months) - 1
    path = [down_m] * peak_to_trough_months + [up_m] * trough_to_recovery_months
    return _replay_rows(cash, path, peak_to_trough_months, 0.05, "1929")


def crash_replay_2008(cash: float) -> list[dict]:
    """Replay the 2008 drawdown using the official annual S&P levels.

    The Economic Report of the President tables give 1,468.36 at the end of 2007, 903.25 at
    the end of 2008 and 1,115.10 at the end of 2009. The recovery to the 2007 level is
    carried on the annual path that follows in the same official table.
    """
    years = [2008, 2009, 2010, 2011, 2012]
    annual = [SP500[y] / SP500[y - 1] - 1 for y in years]
    path = monthly_from_annual(annual)
    trough_month = 16  # March 2009, sixteen months after the October 2007 peak
    return _replay_rows(cash, path, trough_month, 0.05, "2008")


def _replay_rows(cash: float, path: list[float], trough_month: int,
                 cash_rate: float, label: str) -> list[dict]:
    rows = []
    strategies = [
        ("All in at the peak", lambda c: all_in(c, path)),
        ("Park 24 months, then phase in over 12",
         lambda c: phased_entry(c, 24, 12, cash_rate, path)),
        ("Park 36 months, then phase in over 12",
         lambda c: phased_entry(c, 36, 12, cash_rate, path)),
        ("Park 36 months, then phase in over 24",
         lambda c: phased_entry(c, 36, 24, cash_rate, path)),
    ]
    for name, fn in strategies:
        end_value = fn(cash)
        trough_path = path[:trough_month]
        row = {
            "scenario": label,
            "strategy": name,
            "at_trough": None,
            "at_end": end_value,
            "per_10000_trough": None,
            "per_10000_end": end_value / cash * 10_000 if cash else 0.0,
        }
        if "All in" in name:
            trough_value = all_in(cash, trough_path)
        else:
            park, phase = _park_phase(name)
            trough_value = phased_entry(cash, park, min(phase, len(trough_path)),
                                        cash_rate, trough_path)
        row["at_trough"] = trough_value
        row["per_10000_trough"] = trough_value / cash * 10_000 if cash else 0.0
        rows.append(row)
    return rows


def _park_phase(strategy_name: str) -> tuple[int, int]:
    """Recover (park months, phase months) from a strategy label. Pinned by the tests."""
    digits = [int(d) for d in "".join(ch if ch.isdigit() else " "
                                      for ch in strategy_name).split()]
    return digits[0], digits[1]


def cost_of_the_cushion(cash: float, park_months: int, phase_months: int,
                        cash_rate: float, equity_rate: float, horizon_months: int) -> dict:
    """What the delay costs if the crash never comes.

    Reported beside every phased-entry headline. This is the reinvestment risk: the cushion
    is bought with return that is given up in the worlds where nothing goes wrong.
    """
    monthly_equity = (1 + equity_rate) ** (1 / 12) - 1
    flat = [monthly_equity] * horizon_months
    allin = all_in(cash, flat)
    phased = phased_entry(cash, park_months, phase_months, cash_rate, flat)
    return {
        "all_in": allin,
        "phased": phased,
        "shortfall": allin - phased,
        "shortfall_per_10000": (allin - phased) / cash * 10_000,
        "shortfall_pct": (allin - phased) / allin if allin else 0.0,
    }


# ---------------------------------------------------------------------------


def _band_value(band: tuple, which: str) -> float:
    """Pick low, base or high out of a three-part assumption band."""
    return {"low": band[0], "base": band[1], "high": band[2]}[which]
