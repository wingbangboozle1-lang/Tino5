# -*- coding: utf-8 -*-
"""Regression tests for the desk-03242c78 model.

These are guard rails, not assertions that the recommendation is correct. They pin the
behaviour that the published pages depend on, so that a later edit cannot silently change a
number the site quotes.

Run: python3 -m unittest discover -s desk-03242c78/_src -p "test_*.py" -v
"""

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import model as M  # noqa: E402


def base(regime="baseline"):
    return dict(M.REGIMES[regime], key=regime)


def run(pid, t=2045, regime="baseline", **kw):
    return M.run_path(*M.PATHS_BY_ID[pid], transfer_year=t, regime=base(regime), **kw)


class TestRounding(unittest.TestCase):
    def test_every_published_amount_is_ten(self):
        for p in M.PATHS:
            for t in M.TRANSFER_YEARS:
                r = run(p[0], t=t)
                for k, v in r.items():
                    if (isinstance(v, int) and k not in ("transfer_year",)
                            and not isinstance(v, bool)):
                        self.assertEqual(v % 10, 0, "%s %s not rounded" % (p[0], k))


class TestProps(unittest.TestCase):
    def test_prop13_cap_binds(self):
        self.assertAlmostEqual(M.prop13_step(0.05), 0.02)
        self.assertAlmostEqual(M.prop13_step(0.01), 0.01)

    def test_prop19_keeps_prior_value_below_the_cap(self):
        self.assertEqual(M.prop19_taxable(500_000, 1_400_000, 1_000_000), 500_000)

    def test_prop19_subtracts_the_allowance_above_the_cap(self):
        self.assertEqual(M.prop19_taxable(500_000, 3_000_000, 1_000_000), 2_000_000)

    def test_allowance_rolls_forward(self):
        self.assertEqual(M.allowance_at(2025), M.PROP19_ALLOWANCE)
        self.assertGreater(M.allowance_at(2045), M.PROP19_ALLOWANCE)


class TestSelling(unittest.TestCase):
    def test_sale_at_the_transfer_date_realises_no_gain(self):
        r = run("P3")
        self.assertEqual(r["sale_tax"], 0)
        self.assertGreater(r["sale_proceeds"], 0)

    def test_sale_costs_are_deducted(self):
        r = run("P3")
        self.assertLess(r["sale_proceeds"], r["a_value"])
        self.assertGreater(r["sale_cost"], 0)

    def test_living_then_selling_uses_the_exclusion(self):
        r = run("P4")
        self.assertEqual(r["sec121_used"], M.SEC121_SINGLE)

    def test_letting_pays_recapture(self):
        r = run("P5")
        self.assertGreater(r["recapture"], 0)
        self.assertEqual(r["sec121_used"], 0)


class TestPaths(unittest.TestCase):
    def test_selling_leads_the_baseline(self):
        rows = sorted([run(p[0]) for p in M.PATHS],
                      key=lambda r: -r["net_worth_with_shelter"])
        self.assertEqual(rows[0]["path"], "P3")

    def test_letting_A_never_beats_living_in_A(self):
        for regime in M.REGIMES:
            for t in M.TRANSFER_YEARS:
                self.assertLess(run("P2", t=t, regime=regime)["net_worth_with_shelter"],
                                run("P1", t=t, regime=regime)["net_worth_with_shelter"],
                                "P2 beat P1 in %s at %d" % (regime, t))

    def test_selling_B_is_never_the_best_choice(self):
        for regime in M.REGIMES:
            for t in M.TRANSFER_YEARS:
                rows = sorted([run(p[0], t=t, regime=regime) for p in M.PATHS],
                              key=lambda r: -r["net_worth_with_shelter"])
                self.assertNotEqual(rows[0]["path"], "P7")

    def test_every_path_houses_the_household(self):
        for p in M.PATHS:
            self.assertGreater(run(p[0])["shelter"], 0, p[0])

    def test_phased_paths_lose_a_little_in_the_baseline(self):
        p6 = run("P6")["net_worth_with_shelter"]
        p3 = run("P3")["net_worth_with_shelter"]
        self.assertLess(p6, p3)
        self.assertGreater(p6, p3 * 0.90)      # a cost, not a catastrophe


class TestPhasing(unittest.TestCase):
    def test_parking_loses_without_a_crash(self):
        a, b = M.phase_compare(2045, base(), 24, 24, 12, 0.0)
        self.assertLess(b, a)

    def test_parking_wins_through_a_deep_early_crash(self):
        a, b = M.phase_compare(2045, base(), 24, 24, 12, 0.60)
        self.assertGreater(b, a)

    def test_break_even_is_a_depth_between_zero_and_one(self):
        be = M.phase_break_even(2045, base(), 24, 24, 12)
        self.assertIsNotNone(be)
        self.assertGreater(be, 0.0)
        self.assertLess(be, 1.0)


class TestCrossover(unittest.TestCase):
    def test_house_growth_crossover_is_stable_and_plausible(self):
        for t in M.TRANSFER_YEARS:
            c = M.crossover("P1", "P3", t, axis="house")
            self.assertIsNotNone(c)
            self.assertGreater(c, 0.04)
            self.assertLess(c, 0.08)

    def test_equity_crossover_is_below_the_base_case(self):
        c = M.crossover("P1", "P3", 2045, axis="equity")
        self.assertLess(c, M.EQUITY_RETURN)


class TestPrivacyInputs(unittest.TestCase):
    def test_assessed_values_are_rounded_before_use(self):
        self.assertEqual(M.A_ASSESSED % 10_000, 0)
        self.assertEqual(M.B_ASSESSED % 5_000, 0)

    def test_no_year_by_year_history_in_the_module(self):
        with open(os.path.join(HERE, "model.py")) as fh:
            src = fh.read()
        # The owner's tax history must never be stored: only the implied rate band.
        self.assertNotIn("539_743", src)
        self.assertNotIn("529_161", src)


if __name__ == "__main__":
    unittest.main()
