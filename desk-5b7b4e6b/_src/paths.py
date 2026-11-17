# -*- coding: utf-8 -*-
"""The path engine for desk-5b7b4e6b.

Ten ways of dealing with Property A, run over identical years, identical transfer dates and
identical horizons, in identical resampled worlds, then liquidated and taxed at the same
terminal date. Property B is held throughout in every path because the household already
owns it; what changes between paths is who occupies which unit. B's operating cash flow, its
escalating bill and its incremental depreciation recapture are therefore inside every path,
while B's terminal sale value is not: it is the same in every path and would cancel out of
the comparison (flag F09).

Paths
-----
live                Occupy Property A as the principal residence for the whole horizon.
                    This is the path that carries the Proposition 19 parent-child exclusion,
                    because the exclusion requires exactly that occupation.
rent                Let Property A. The exclusion is not available, so the assessed value is
                    reset to market value at the transfer.
sell_sameyear       Sell Property A in the same tax year as the inheritance, before anything
                    else is decided. The basis is fair market value at death, so the gain is
                    close to zero.
live_then_sell      Occupy for ten years, then sell. Section 121 is available because the
                    home was the principal residence for two of the five years before sale.
rent_then_sell      Let for ten years, then sell. No section 121; depreciation claimed comes
                    back as unrecaptured section 1250 gain.
live_10_then_rent   Occupy for ten years to secure the Proposition 19 exclusion, then move
                    out and let the property. The exclusion depends on the home remaining
                    the principal residence, so the assessed value is reset to market value
                    in the year the occupation ends. This path is here to price that risk.
sell_phase24        Sell, park the proceeds in short Treasuries for 24 months, phase in over
                    twelve months.
sell_phase36        Sell, park for 36 months, phase in over twelve months.
hold_treasury       Sell and hold short Treasuries to the terminal date.
exchange_1031       Sell and exchange into other real property under section 1031. Because
                    the inherited basis steps up to fair market value at death, there is
                    almost no gain to defer; the path is carried so that the point is
                    measured rather than asserted.

None of these is a recommendation. They are the arithmetic that the pre-committed triggers
on the decision-triggers page are written to read.
"""

from __future__ import annotations

from model import (OFFICIAL, OWNER, A_RATE, A_FIXED, B_BILL_GROWTH,
                   sale_proceeds, annual_tax)

BASE_YEAR = 2026
TERMINAL_YEAR = 2076
HOLD_YEARS_FOR_MIXED = 10


def _band_value(band: tuple, which: str) -> float:
    """Pick low, base or high out of a three-part assumption band."""
    return {"low": band[0], "base": band[1], "high": band[2]}[which]


PATHS = [
    ("live", "Live in Property A for the whole horizon", "pure"),
    ("rent", "Let Property A for the whole horizon", "pure"),
    ("sell_sameyear", "Sell Property A in the same tax year as the inheritance", "pure"),
    ("live_then_sell", "Live in it for ten years, then sell", "mixed"),
    ("rent_then_sell", "Let it for ten years, then sell", "mixed"),
    ("live_10_then_rent", "Live in it for ten years, then move out and let it", "mixed"),
    ("sell_phase24", "Sell, park 24 months in Treasuries, phase in over 12", "mixed"),
    ("sell_phase36", "Sell, park 36 months in Treasuries, phase in over 12", "mixed"),
    ("hold_treasury", "Sell and hold short Treasuries to the terminal date", "mixed"),
    ("exchange_1031", "Sell and exchange into other real property", "mixed"),
]

ASSUMPTIONS = {
    # Combined marginal rate on ordinary rental income. Components, each sourced: the
    # federal ordinary rate, California at 12.30% (ftb_rates_2026), the 1% over $1,000,000
    # (rtc_17043) and the 3.8% net investment income tax (irs_niit). The federal deduction
    # for state tax is capped, so the California part is not fully deductible federally.
    "ordinary_rate": (0.45, 0.50, 0.54),
    # Selling costs — commission, escrow, transfer taxes and recording fees.
    "selling_cost_rate": (0.050, 0.065, 0.080),
    "vacancy": (0.03, 0.06, 0.10),
    "management": (0.00, 0.06, 0.10),
    "improvement_share": (0.70, 0.80, 0.90),
    # Property A's market rent, as a gross yield on value. Until written rental estimates
    # exist this is an assumption, not a measurement: flag F07.
    "rent_yield_a": (0.020, 0.026, 0.032),
    "insurance_a": (1_200, 1_500, 2_500),
    "insurance_b": (1_200, 1_500, 2_500),
    # Property B's bill has no usable ad-valorem split (see model.B_FIT), so it is projected
    # from its own observed growth. The band is the three-, six- and nine-year compound
    # rates measured from the household's own bills.
    "b_bill_growth": (0.0225, 0.0426, 0.0500),
    "joint": False,
}


class World:
    """One future: a sequence of annual conditions, one per year from BASE_YEAR."""

    def __init__(self, rows: list[dict], start_year: int = BASE_YEAR):
        self.rows = list(rows)
        self.start = start_year

    def at(self, year: int) -> dict:
        idx = year - self.start
        if idx < 0:
            return self.rows[0]
        if idx < len(self.rows):
            return self.rows[idx]
        return self.rows[-1]


def deterministic_world(infl_sf: float, rent_sf: float, hpi_a: float, hpi_b: float,
                        equity: float, tb3: float, gs10: float,
                        years: int = 60) -> World:
    """A world in which every year repeats the same conditions. Used for break-even tests."""
    return World([{
        "year": BASE_YEAR + i, "infl_us": infl_sf, "infl_sf": infl_sf,
        "rent_sf": rent_sf, "hpi_a": hpi_a, "hpi_b": hpi_b,
        "equity": equity, "tb3": tb3, "gs10": gs10,
    } for i in range(years)])


def run_path(path: str, world: World, transfer_year: int, horizon: int,
             setting: str = "base", **over) -> dict:
    """Run one strategy through one world. Returns terminal after-tax wealth and its parts."""
    a = dict(ASSUMPTIONS)
    a.update(over)
    pick = lambda key: _band_value(a[key], setting)

    ord_rate = pick("ordinary_rate")
    sell_cost = pick("selling_cost_rate")
    vac = pick("vacancy")
    mgmt = pick("management")
    imp_share = pick("improvement_share")
    yield_a = pick("rent_yield_a")
    ins_a = pick("insurance_a")
    ins_b = pick("insurance_b")
    b_growth = pick("b_bill_growth")
    joint = a["joint"]

    end_year = BASE_YEAR + horizon
    a_value = OWNER["A_value_2026"]
    b_value = OWNER["B_value_2026"]
    a_av = OWNER["A_assessed_anchor"]
    b_tax = OWNER["B_tax_2025"]

    rent_per_unit_b = OWNER["B_rent_2_units_month"] / OWNER["B_units_let"] * 12
    water_a = OWNER["A_water_low"]
    solar_a = OWNER["A_solar_credit_low"]
    water_b = OWNER["B_water_low"]
    power_b = OWNER["B_power_low"]

    portfolio = 0.0
    a_accum_dep = 0.0
    b_extra_dep = 0.0
    a_basis = None
    sold_a_in = None
    a_tax_total = 0.0
    rent_tax_total = 0.0
    imputed_total = 0.0
    costs_total = 0.0
    sale_detail = None
    a_tax_first_year_after = None
    reassessed_in = None

    for year in range(BASE_YEAR, end_year + 1):
        w = world.at(year)
        infl, rent_growth, equity = w["infl_sf"], w["rent_sf"], w["equity"]
        tb3, gs10 = w["tb3"] / 100.0, w["gs10"] / 100.0

        a_value *= (1 + w["hpi_a"])
        b_value *= (1 + w["hpi_b"])
        rent_per_unit_b *= (1 + rent_growth)
        b_tax *= (1 + b_growth)

        owns_a = (year >= transfer_year) and (sold_a_in is None)
        holds_a = sold_a_in is None

        # ------------------------------------------------- Property A assessed value
        if year <= transfer_year:
            a_av *= (1 + min(OFFICIAL["prop13_cap"], infl))
        elif year == transfer_year + 1 and holds_a:
            if path in ("live", "live_then_sell", "live_10_then_rent"):
                # Proposition 19 parent-child exclusion: the value limit is the factored
                # base year value carried over, plus the adjusted exclusion amount.
                a_av = min(a_value, a_av + OFFICIAL["prop19_exclusion"])
            else:
                a_av = a_value       # no principal residence, so no exclusion: reassessment
        elif holds_a:
            if path == "live_10_then_rent" and year == transfer_year + 1 + HOLD_YEARS_FOR_MIXED:
                a_av = a_value       # occupation has ended, so the exclusion ends with it
                reassessed_in = year
            else:
                a_av *= (1 + min(OFFICIAL["prop13_cap"], infl))

        a_tax = annual_tax(a_av, A_RATE, A_FIXED) if owns_a else 0.0
        if owns_a and a_tax_first_year_after is None and year > transfer_year:
            a_tax_first_year_after = a_tax
        a_tax_total += a_tax

        # ------------------------------------------------------------- occupation
        living_in_a = owns_a and path in ("live", "live_then_sell", "live_10_then_rent")
        if path == "live_10_then_rent" and owns_a:
            living_in_a = year <= transfer_year + HOLD_YEARS_FOR_MIXED
        units_let_b = OWNER["B_units"] if living_in_a else OWNER["B_units_let"]

        # ------------------------------------------------------------ rental income
        gross_b = rent_per_unit_b * units_let_b
        dep_b = (b_value * imp_share / 27.5) * (units_let_b / OWNER["B_units"])
        if units_let_b > OWNER["B_units_let"]:
            b_extra_dep += dep_b / OWNER["B_units"]
        net_b = gross_b * (1 - vac - mgmt) - dep_b

        gross_a = dep_a = 0.0
        if owns_a and not living_in_a:
            gross_a = a_value * yield_a
            dep_a = a_value * imp_share / 27.5
            a_accum_dep += dep_a
        net_a = gross_a * (1 - vac - mgmt) - dep_a

        net_rent = net_a + net_b
        rent_tax = ord_rate * max(net_rent, 0.0)
        rent_tax_total += rent_tax

        # Housing consumed: Property A when living there, otherwise the third unit at B.
        imputed = rent_per_unit_b
        if living_in_a:
            imputed = a_value * yield_a
        imputed_total += imputed

        # ------------------------------------------------------------ running costs
        costs = b_tax + water_b + power_b + ins_b
        costs += b_value * _band_value(OWNER["B_maintenance_pct"], setting)
        if owns_a:
            costs += a_tax + water_a - solar_a + ins_a
            costs += a_value * _band_value(OWNER["A_maintenance_pct"], setting)
        costs_total += costs

        if year == transfer_year:
            a_basis = a_value       # section 1014: basis is fair market value at death

        # ----------------------------------------------------------------- sale of A
        sells_now = (
            (path == "sell_sameyear" and year == transfer_year)
            or (path in ("live_then_sell", "rent_then_sell")
                and year == transfer_year + HOLD_YEARS_FOR_MIXED)
            or (path in ("sell_phase24", "sell_phase36", "hold_treasury", "exchange_1031")
                and year == transfer_year)
        )
        if sells_now and holds_a and owns_a:
            sold_a_in = year
            sec121 = 0.0
            if path in ("live", "live_then_sell") and (year - transfer_year) >= 2:
                sec121 = OFFICIAL["sec121_joint"] if joint else OFFICIAL["sec121_single"]
            sale_detail = sale_proceeds(a_value, a_basis, sell_cost, sec121, a_accum_dep)
            portfolio += sale_detail["net_proceeds"]
            # Section 1031 defers gain. Because the basis steps up to fair market value at
            # death (section 1014), the deferred gain here is whatever the property earned
            # between the transfer and the exchange, which is measured in the sale detail
            # rather than assumed away.
            a_accum_dep = 0.0

        # -------------------------------------------------------------- investment
        # A negative balance is a borrowing, not an investment: it accrues at a financing
        # rate rather than earning the equity return. Without this rule the worst futures
        # compound an operating deficit at the equity rate and report impossible wealth.
        loan_rate = tb3 + 0.03
        if sold_a_in is not None:
            if path in ("sell_phase24", "sell_phase36"):
                park_years = 2 if path == "sell_phase24" else 3
                since = year - sold_a_in
                cash_r = tb3 + 0.35 * (gs10 - tb3)
                target = cash_r if since < park_years else (
                    0.5 * cash_r + 0.5 * equity if since == park_years else equity)
            elif path == "hold_treasury":
                target = tb3 + 0.35 * (gs10 - tb3)
            else:
                target = equity
            portfolio *= (1 + (target if portfolio >= 0 else loan_rate))
        portfolio += net_rent - rent_tax - costs

    # -------------------------------------------------------------- terminal date
    terminal = portfolio
    if sold_a_in is None:
        sec121 = 0.0
        if path in ("live", "live_then_sell", "live_10_then_rent") \
                and (end_year - transfer_year) >= 2 and path != "live_10_then_rent":
            sec121 = OFFICIAL["sec121_joint"] if joint else OFFICIAL["sec121_single"]
        sale_detail = sale_proceeds(a_value, a_basis, sell_cost, sec121, a_accum_dep)
        terminal += sale_detail["net_proceeds"]

    # The extra depreciation taken on Property B's third unit comes back as unrecaptured
    # section 1250 gain. Every other part of Property B is identical across paths.
    terminal -= OFFICIAL["fed_unrecaptured_1250"] * b_extra_dep

    return {
        "path": path,
        "transfer_year": transfer_year,
        "horizon": horizon,
        "setting": setting,
        "terminal": terminal,
        "portfolio": portfolio,
        "a_value": a_value,
        "b_value": b_value,
        "sold_a_in": sold_a_in,
        "reassessed_in": reassessed_in,
        "a_accum_dep": a_accum_dep,
        "a_tax_total": a_tax_total,
        "a_tax_first_year": a_tax_first_year_after,
        "rent_tax_total": rent_tax_total,
        "costs_total": costs_total,
        "imputed_total": imputed_total,
        "sale_detail": sale_detail,
    }


def compare(world: World, transfer_year: int, horizon: int,
            setting: str = "base") -> dict[str, dict]:
    return {p: run_path(p, world, transfer_year, horizon, setting) for p, _, _ in PATHS}


def rank_paths(worlds: list[World], transfer_year: int, horizon: int,
               setting: str = "base") -> dict[str, list[float]]:
    results: dict[str, list[float]] = {p: [] for p, _, _ in PATHS}
    for w in worlds:
        for p, r in compare(w, transfer_year, horizon, setting).items():
            results[p].append(r["terminal"])
    return results


def difference_vs(results: dict[str, list[float]], reference: str
                  ) -> dict[str, list[float]]:
    """Terminal wealth of each path minus the reference path, world by world."""
    base = results[reference]
    return {p: [v - b for v, b in zip(vals, base)]
            for p, vals in results.items() if p != reference}


def break_even_house_growth(transfer_year: int, horizon: int, setting: str = "base",
                            other_path: str = "sell_sameyear",
                            keep_path: str = "live",
                            lo: float = 0.0, hi: float = 0.20) -> float:
    """The constant house-price growth rate at which keeping Property A matches selling it.

    Every other condition is held at its 1977-2025 average. The answer is a break-even, not
    a forecast: it says what has to be true for the two paths to come out level.
    """
    from model import HISTORY
    from statistics import mean
    infl = mean(h["infl_sf"] for h in HISTORY)
    rent = mean(h["rent_sf"] for h in HISTORY)
    hpi_b = mean(h["hpi_b"] for h in HISTORY)
    eq = mean(h["equity"] for h in HISTORY)
    tb3 = mean(h["tb3"] for h in HISTORY)
    gs10 = mean(h["gs10"] for h in HISTORY)

    def gap(g: float) -> float:
        w = deterministic_world(infl, rent, g, hpi_b, eq, tb3, gs10, horizon + 2)
        return (run_path(keep_path, w, transfer_year, horizon, setting)["terminal"]
                - run_path(other_path, w, transfer_year, horizon, setting)["terminal"])

    for _ in range(60):
        mid = (lo + hi) / 2
        if gap(mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def break_even_equity_return(transfer_year: int, horizon: int, setting: str = "base",
                             lo: float = 0.0, hi: float = 0.25) -> float:
    """The constant equity return at which selling matches keeping, other things equal."""
    from model import HISTORY
    from statistics import mean
    infl = mean(h["infl_sf"] for h in HISTORY)
    rent = mean(h["rent_sf"] for h in HISTORY)
    hpi_a = mean(h["hpi_a"] for h in HISTORY)
    hpi_b = mean(h["hpi_b"] for h in HISTORY)
    tb3 = mean(h["tb3"] for h in HISTORY)
    gs10 = mean(h["gs10"] for h in HISTORY)

    def gap(e: float) -> float:
        w = deterministic_world(infl, rent, hpi_a, hpi_b, e, tb3, gs10, horizon + 2)
        return (run_path("live", w, transfer_year, horizon, setting)["terminal"]
                - run_path("sell_sameyear", w, transfer_year, horizon, setting)["terminal"])

    for _ in range(60):
        mid = (lo + hi) / 2
        if gap(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2
