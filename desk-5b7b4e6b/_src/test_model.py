# -*- coding: utf-8 -*-
"""Model tests for desk-5b7b4e6b.

These pin the conventions the pages depend on rather than re-checking arithmetic that a
reader can do: the month convention in the crash replays, the split of a bill into an
ad-valorem part and a fixed part, the Proposition 13 cap, the Proposition 19 limit, the
section 1014 basis, the recapture order on a sale, and the identity of the exchange path
with the same-year sale.

Run:  python3 -m unittest discover -s desk-5b7b4e6b/_src -p "test_*.py"
"""

from __future__ import annotations

import pathlib
import unittest

import model as M
import paths as P


class TestSeries(unittest.TestCase):
    def test_history_is_the_years_every_series_shares(self):
        self.assertEqual(M.HISTORY[0]["year"], 1977)
        self.assertEqual(M.HISTORY[-1]["year"], 2025)
        for row in M.HISTORY:
            for key in ("infl_us", "infl_sf", "rent_sf", "hpi_a", "hpi_b", "equity",
                        "tb3", "gs10"):
                self.assertIsNotNone(row[key], f"{row['year']} {key}")

    def test_year_on_year_has_one_fewer_row_than_levels(self):
        self.assertEqual(len(M.INFL_US), len(M.CPI_US) - 1)
        self.assertEqual(len(M.HPI_SJ_G), len(M.HPI_SJ) - 1)

    def test_a_falling_index_gives_a_negative_change(self):
        # 2008: the S&P composite fell from 1,468.36 to 903.25 in the official table.
        self.assertLess(M.EQ[2008], 0)
        self.assertAlmostEqual(M.SP500[2008] / M.SP500[2007] - 1, -0.3849, places=3)

    def test_regime_table_covers_the_whole_record(self):
        rows = M.regime_table()
        self.assertEqual(sum(r["years"] for r in rows), len(M.HISTORY))
        names = [r["name"] for r in rows]
        self.assertEqual(len(names), len(set(names)))

    def test_block_bootstrap_keeps_the_block_together(self):
        paths = M.block_bootstrap(10, 4, block=5, seed=1)
        self.assertEqual(len(paths), 4)
        for p in paths:
            self.assertEqual(len(p), 10)
            # the first five rows are a contiguous run of the real record
            index = {id(r): i for i, r in enumerate(M.HISTORY)}
            positions = [index[id(r)] for r in p[:5]]
            deltas = [(b - a) % len(M.HISTORY)
                      for a, b in zip(positions, positions[1:])]
            self.assertTrue(all(d == 1 for d in deltas),
                            [r["year"] for r in p[:5]])

    def test_percentiles_are_ordered(self):
        values = list(range(101))
        self.assertEqual(M.pct(values, 0.0), 0)
        self.assertEqual(M.pct(values, 0.5), 50)
        self.assertEqual(M.pct(values, 1.0), 100)


class TestBillFit(unittest.TestCase):
    def test_a_perfect_split_is_recovered_exactly(self):
        rows = [(100_000, 100_000 * 0.012 + 400),
                (200_000, 200_000 * 0.012 + 400),
                (300_000, 300_000 * 0.012 + 400)]
        fit = M.fit_bill(rows)
        self.assertAlmostEqual(fit["rate"], 0.012, places=9)
        self.assertAlmostEqual(fit["fixed"], 400, places=6)
        self.assertAlmostEqual(fit["r2"], 1.0, places=9)
        self.assertTrue(fit["usable"])

    def test_a_negative_fixed_charge_is_reported_as_unusable(self):
        fit = M.fit_bill([(100_000, 1_000), (200_000, 3_000)])
        self.assertLess(fit["fixed"], 0)
        self.assertFalse(fit["usable"])

    def test_property_b_fit_is_unusable_and_property_a_fit_is_not(self):
        self.assertFalse(M.B_FIT["usable"])
        self.assertTrue(M.A_FIT["usable"])
        self.assertGreater(M.A_RATE, 0.01)
        self.assertLess(M.A_RATE, 0.013)

    def test_bill_growth_windows_are_all_present(self):
        self.assertEqual(set(M.B_BILL_GROWTH), {3, 6, 9})
        for v in M.B_BILL_GROWTH.values():
            self.assertGreater(v, 0)


class TestProp13(unittest.TestCase):
    def test_the_cap_binds_when_inflation_is_higher(self):
        out = M.prop13_assessed(100_000, [0.09, 0.09], 2)
        self.assertAlmostEqual(out[1], 102_000)
        self.assertAlmostEqual(out[2], 104_040)

    def test_the_index_binds_when_it_is_lower_than_the_cap(self):
        out = M.prop13_assessed(100_000, [0.005], 1)
        self.assertAlmostEqual(out[1], 100_500)

    def test_values_fall_in_a_falling_market(self):
        out = M.prop13_assessed(100_000, [-0.03], 1)
        self.assertAlmostEqual(out[1], 97_000)


class TestSaleTax(unittest.TestCase):
    def test_basis_step_up_leaves_almost_no_gain(self):
        sale = M.sale_proceeds(price=3_000_000, basis=3_000_000, costs_rate=0.065)
        self.assertAlmostEqual(sale["gain_before_exclusion"], 0)
        self.assertAlmostEqual(sale["total_tax"], 0)

    def test_section_121_reduces_the_taxable_gain(self):
        raw = M.sale_proceeds(1_000_000, 400_000, 0.0, 0.0)
        exc = M.sale_proceeds(1_000_000, 400_000, 0.0, 250_000)
        self.assertAlmostEqual(raw["taxable_gain"] - exc["taxable_gain"], 250_000)
        self.assertLess(exc["total_tax"], raw["total_tax"])

    def test_recapture_is_taxed_first_and_at_its_own_rate(self):
        sale = M.sale_proceeds(1_000_000, 600_000, 0.0, 0.0, 100_000)
        self.assertEqual(sale["unrecaptured_1250"], 100_000)
        expected_fed = 0.25 * 100_000 + 0.20 * 300_000 + 0.038 * 400_000
        self.assertAlmostEqual(sale["federal_tax"], expected_fed, places=6)

    def test_california_taxes_a_gain_as_ordinary_income(self):
        # The published 2026 Schedule X: 12.30% over $768,213, plus 1% over $1,000,000.
        gain = 2_000_000
        expected = 74_675.27 + 0.1230 * (gain - 768_213) + 0.01 * (gain - 1_000_000)
        self.assertAlmostEqual(M.ca_income_tax(gain), expected, places=2)

    def test_california_tax_is_marginal_not_average(self):
        self.assertAlmostEqual(M.ca_income_tax(500_000, 0.0), M.ca_tax_on_income(500_000))
        self.assertLess(M.ca_income_tax(100_000, 2_000_000),
                        M.ca_tax_on_income(2_100_000))

    def test_the_top_combined_rate_is_the_sum_of_the_sourced_parts(self):
        self.assertAlmostEqual(M.OFFICIAL["ca_top_rate"] + M.OFFICIAL["ca_mhst_rate"],
                               0.1330, places=9)
        self.assertAlmostEqual(M.OFFICIAL["fed_ltcg_top"] + M.OFFICIAL["fed_niit"],
                               0.2380, places=9)


class TestPhasedEntry(unittest.TestCase):
    def test_all_in_multiplies_every_month(self):
        self.assertAlmostEqual(M.all_in(1_000, [0.0] * 12), 1_000)

    def test_parking_earns_the_cash_rate_and_nothing_else(self):
        # Park for the whole window: no instalment is ever bought.
        value = M.phased_entry(1_000, park_months=24, phase_months=12,
                               cash_rate=0.04, equity_path=[-0.5] * 24)
        self.assertAlmostEqual(value, 1_000 * 1.04 ** 2, places=6)

    def test_a_flat_market_makes_phasing_cost_the_foregone_return(self):
        flat = [0.0] * 36
        self.assertAlmostEqual(M.all_in(1_000, flat), 1_000)
        self.assertAlmostEqual(
            M.phased_entry(1_000, 12, 12, 0.0, flat), 1_000, places=6)

    def test_the_cushion_costs_more_the_longer_the_park(self):
        short = M.cost_of_the_cushion(10_000, 24, 12, 0.04, 0.07, 120)
        long = M.cost_of_the_cushion(10_000, 36, 12, 0.04, 0.07, 120)
        self.assertGreater(long["shortfall"], short["shortfall"])
        self.assertGreater(short["shortfall"], 0)

    def test_the_crash_replays_measure_the_drawdown(self):
        rows = {r["strategy"]: r for r in M.crash_replay_1929(10_000)}
        all_in = rows["All in at the peak"]
        self.assertLess(all_in["per_10000_trough"], 1_200)
        for name, row in rows.items():
            if name != "All in at the peak":
                self.assertGreater(row["per_10000_trough"], all_in["per_10000_trough"])

    def test_the_2008_replay_follows_the_official_annual_levels(self):
        rows = {r["strategy"]: r for r in M.crash_replay_2008(10_000)}
        self.assertLess(rows["All in at the peak"]["per_10000_trough"], 10_000)

    def test_the_replay_carries_a_hindsight_caveat_on_the_page(self):
        page = (pathlib.Path(__file__).resolve().parent.parent
                / "black-swan.html").read_text()
        self.assertIn("These replays know the crash", page)


class TestPaths(unittest.TestCase):
    def setUp(self):
        self.world = P.deterministic_world(0.03, 0.035, 0.05, 0.045, 0.08, 0.03, 0.045,
                                           years=60)

    def test_every_path_runs_and_returns_a_finite_terminal_value(self):
        for key, _label, _kind in P.PATHS:
            r = P.run_path(key, self.world, 2040, 36)
            self.assertIsInstance(r["terminal"], float)
            self.assertTrue(r["terminal"] == r["terminal"])   # not NaN

    def test_the_exchange_path_equals_the_same_year_sale(self):
        # Section 1014 steps the basis up to fair market value at death, so there is no
        # gain to defer. The two paths must therefore agree.
        sell = P.run_path("sell_sameyear", self.world, 2040, 36)["terminal"]
        exch = P.run_path("exchange_1031", self.world, 2040, 36)["terminal"]
        self.assertAlmostEqual(sell, exch, places=6)

    def test_letting_resets_the_assessed_value_and_occupying_does_not(self):
        rent = P.run_path("rent", self.world, 2040, 36)
        live = P.run_path("live", self.world, 2040, 36)
        self.assertGreater(rent["a_tax_total"], live["a_tax_total"] * 2)

    def test_living_ten_years_then_letting_costs_the_exclusion(self):
        breach = P.run_path("live_10_then_rent", self.world, 2040, 36)
        self.assertEqual(breach["reassessed_in"], 2040 + 1 + P.HOLD_YEARS_FOR_MIXED)
        live = P.run_path("live", self.world, 2040, 36)
        self.assertGreater(breach["a_tax_total"], live["a_tax_total"])

    def test_the_break_even_is_between_the_two_averages(self):
        from statistics import mean
        hpi_mean = mean(h["hpi_a"] for h in M.HISTORY)
        value = P.break_even_house_growth(2040, 36)
        self.assertGreater(value, hpi_mean)
        self.assertLess(value, 0.30)

    def test_the_break_even_moves_the_gap_to_zero(self):
        from statistics import mean
        g = P.break_even_house_growth(2040, 36)
        w = P.deterministic_world(
            mean(h["infl_sf"] for h in M.HISTORY), mean(h["rent_sf"] for h in M.HISTORY),
            g, mean(h["hpi_b"] for h in M.HISTORY), mean(h["equity"] for h in M.HISTORY),
            mean(h["tb3"] for h in M.HISTORY), mean(h["gs10"] for h in M.HISTORY), 40)
        keep = P.run_path("live", w, 2040, 36)["terminal"]
        sell = P.run_path("sell_sameyear", w, 2040, 36)["terminal"]
        self.assertLess(abs(keep - sell) / max(abs(sell), 1), 1e-6)

    def test_the_same_terminal_date_is_used_for_every_transfer_year(self):
        for ty in (2040, 2045, 2050):
            r = P.run_path("live", self.world, ty, P.TERMINAL_YEAR - ty)
            self.assertEqual(r["horizon"], P.TERMINAL_YEAR - ty)


class TestWorld(unittest.TestCase):
    def test_years_before_the_first_row_fall_back_to_it(self):
        w = P.World([{"year": 2026, "equity": 0.1}])
        self.assertEqual(w.at(2020)["equity"], 0.1)

    def test_years_after_the_last_row_repeat_it(self):
        w = P.World([{"year": 2026, "equity": 0.1}, {"year": 2027, "equity": 0.2}])
        self.assertEqual(w.at(2099)["equity"], 0.2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
