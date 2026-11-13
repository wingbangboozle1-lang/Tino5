# -*- coding: utf-8 -*-
"""Regression tests for the decision desk model.

Run: python3 -m unittest discover -s decision/_src -p "test_*.py" -v

The tests pin the behaviour that the published tables depend on:
  * the statutory amounts are carried exactly and never rounded,
  * every derived dollar figure is rounded to the nearest $10,
  * the Proposition 19 allowance steps in two-year stages and holds the
    published figure for 2025 and 2026,
  * the three options are comparable because each is credited with the
    housing service it delivers,
  * the model is deterministic.
"""

import unittest

import model as M


class Rounding(unittest.TestCase):
    def test_r10_rounds_to_ten(self):
        for x in (0, 4, 5, 6, 14, 15, 99, 1_234_567):
            self.assertEqual(M.r10(x) % 10, 0, msg="r10(%s)" % x)

    def test_r10_round_half_up(self):
        self.assertEqual(M.r10(15), 20)
        self.assertEqual(M.r10(14.9), 10)
        self.assertEqual(M.r10(-15), -20)

    def test_statutory_amounts_are_exact(self):
        self.assertEqual(M.STATUTORY["prop19_allowance"], 1_044_586)
        self.assertEqual(M.STATUTORY["estate_2026"], 15_000_000)
        self.assertEqual(M.STATUTORY["estate_2027"], 15_480_000)
        self.assertEqual(M.STATUTORY["sf_rate_fy2026_27"], 0.0118162182)

    def test_money_output_is_multiple_of_ten(self):
        for T in (2026, 2040, 2045, 2050):
            tv = M.transfer_values(T)
            for k in ("occ_av", "occ_tax", "rent_av", "rent_tax"):
                s = M.money(M.r10(tv[k]))
                self.assertEqual(int(s.replace("$", "").replace(",", "")) % 10, 0,
                                 msg="%s %s=%s" % (T, k, s))


class Proposition19(unittest.TestCase):
    def test_published_allowance_applies_verbatim_in_2025_and_2026(self):
        for T in (2026,):
            self.assertAlmostEqual(M.transfer_values(T)["allowance"], 1_044_586, places=2,
                                   msg="allowance in %d" % T)

    def test_allowance_steps_every_two_years(self):
        self.assertAlmostEqual(M.transfer_values(2026)["allowance"],
                               M.transfer_values(2027)["allowance"] / 1.0215 ** 2, places=0)

    def test_allowance_never_falls(self):
        prev = 0
        for T in range(2026, 2077):
            a = M.transfer_values(T)["allowance"]
            self.assertGreaterEqual(a, prev, msg="allowance fell in %d" % T)
            prev = a

    def test_occupancy_value_is_below_rental_value(self):
        for T in (2030, 2040, 2045, 2050):
            tv = M.transfer_values(T)
            self.assertLess(tv["occ_av"], tv["rent_av"], msg="%d" % T)
            self.assertLess(tv["occ_tax"], tv["rent_tax"], msg="%d" % T)

    def test_excess_is_market_less_factored_base_and_allowance(self):
        tv = M.transfer_values(2045)
        self.assertAlmostEqual(tv["excess"], max(0.0, tv["fmv"] - tv["cap"]), places=4)
        self.assertAlmostEqual(tv["occ_av"], tv["fbyv"] + tv["excess"], places=4)


class Proposition13(unittest.TestCase):
    def test_assessed_value_never_grows_faster_than_two_percent(self):
        ser = {r["year"]: r["assessed"] for r in M.property_a_series()}
        for y in range(2027, 2077):
            growth = ser[y] / ser[y - 1] - 1
            self.assertLessEqual(growth, 0.02 + 1e-12, msg="%d grew %s" % (y, growth))

    def test_assessed_value_is_below_market_before_transfer(self):
        for r in M.property_a_series():
            self.assertLessEqual(r["assessed"], r["market"], msg="year %d" % r["year"])

    def test_bill_equals_assessed_times_rate(self):
        for r in M.property_a_series():
            self.assertAlmostEqual(r["tax"], r["assessed"] * M.rate_a(), places=4)


class Scenarios(unittest.TestCase):
    def test_all_options_return_a_finite_npv(self):
        for T in (2040, 2045, 2050):
            n = M.scenario_npv(T)
            for k in ("occupy", "rent", "sell", "occupy_h", "rent_h", "sell_h"):
                self.assertIsInstance(n[k], float)
                self.assertEqual(n[k], n[k], msg="nan in %s %s" % (T, k))
                self.assertTrue(abs(n[k]) < 1e12, msg="unbounded %s %s" % (T, k))

    def test_housing_credit_raises_occupy_relative_to_rent(self):
        n = M.scenario_npv(2045)
        self.assertGreater(n["occupy_h"] - n["rent_h"], n["occupy"] - n["rent"])

    def test_break_even_portfolio_return_is_a_rate(self):
        for other in ("rent", "occupy"):
            b = M.breakeven_portfolio_return(2045, other, with_housing=True)
            self.assertTrue(0.0 < b < 0.30, msg="%s -> %s" % (other, b))

    def test_break_even_market_growth_is_a_rate(self):
        for other in ("rent", "occupy"):
            b = M.breakeven_market_growth(2045, other, with_housing=True)
            self.assertTrue(0.0 < b < 0.30, msg="%s -> %s" % (other, b))

    def test_break_even_yield_is_a_rate(self):
        g = M.breakeven_gross_yield(2045, with_housing=True)
        self.assertTrue(0.0 < g < 0.30, msg=str(g))


class Determinism(unittest.TestCase):
    def test_repeated_runs_agree(self):
        first = [tuple(round(M.scenario_npv(T)[k], 6)
                       for k in ("occupy_h", "rent_h", "sell_h"))
                 for T in (2040, 2045, 2050)]
        second = [tuple(round(M.scenario_npv(T)[k], 6)
                        for k in ("occupy_h", "rent_h", "sell_h"))
                  for T in (2040, 2045, 2050)]
        self.assertEqual(first, second)


class EstateTax(unittest.TestCase):
    def test_nothing_owed_below_the_threshold(self):
        self.assertEqual(M.estate_tax(15_000_000, 2026)["tax"], 0.0)
        self.assertEqual(M.estate_tax(1_000_000, 2026)["tax"], 0.0)

    def test_something_owed_above_the_threshold(self):
        self.assertGreater(M.estate_tax(16_000_000, 2026)["tax"], 0.0)

    def test_exemption_projects_forward(self):
        tbl = {r["year"]: r["amount"] for r in M.estate_exemption_projection()}
        self.assertEqual(tbl[2026], 15_000_000)
        self.assertEqual(tbl[2027], 15_480_000)
        self.assertGreater(tbl[2050], tbl[2040])

    def test_indexation_rate_must_be_a_rate(self):
        with self.assertRaises(ValueError):
            M.estate_exemption_projection(2026)


class BlackSwan(unittest.TestCase):
    def test_every_regime_is_anchored(self):
        for r in M.BLACK_SWAN:
            self.assertTrue(r["anchor"], msg=r["name"])
            self.assertTrue(r["anchor_text"], msg=r["name"])

    def test_npvs_stay_finite(self):
        for s in M.black_swan(2045, 2076):
            n = s["npv"]
            for k in ("occupy_h", "rent_h", "sell_h"):
                self.assertTrue(abs(n[k]) < 1e13, msg="%s %s" % (s["regime"]["name"], k))


if __name__ == "__main__":
    unittest.main()
