# -*- coding: utf-8 -*-
"""Regression tests for the cbd/ desk model. Run: python3 -m unittest discover -s cbd/_src -p "test_*.py" -v"""

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import desk_model as dm  # noqa: E402
import model as cbe  # noqa: E402  (read-only owner-brief model)


class PhasedEngine(unittest.TestCase):
    def test_lump_sum_compounds_at_net_return(self):
        self.assertAlmostEqual(dm.phased_value(1, 31), (1 + dm.EQ_NET) ** 31, places=9)

    def test_no_tranches_is_cash_only(self):
        expected = (1 + dm.CASH_NET) ** 10
        self.assertAlmostEqual(dm.simulate(0, 120)[-1], expected, places=9)

    def test_crash_reaches_trough_level_exactly(self):
        for level in (0.43, 0.11, 0.9):
            self.assertAlmostEqual(dm.equity_index(17, dm.EQ_NET, (level, 17)), level, places=9)

    def test_crash_path_is_continuous_at_no_crash(self):
        growth_level = (1 + dm.EQ_NET) ** (17 / 12.0)
        a = dm.phased_value(24, 10, dm.EQ_NET, (growth_level, 17))
        b = dm.phased_value(24, 10, dm.EQ_NET, None)
        self.assertAlmostEqual(a, b, places=9)

    def test_deeper_crash_lowers_lump_sum(self):
        vals = [dm.phased_value(1, 10, dm.EQ_NET, (lv, 17)) for lv in (0.9, 0.7, 0.43)]
        self.assertTrue(vals[0] > vals[1] > vals[2])

    def test_breakeven_trough_ties_the_two_strategies(self):
        level, fall = dm.breakeven_trough(24)
        diff = (dm.phased_value(24, 10, dm.EQ_NET, (level, 17))
                - dm.phased_value(1, 10, dm.EQ_NET, (level, 17)))
        self.assertLess(abs(diff), 1e-6)
        self.assertAlmostEqual(fall, 1.0 - level, places=12)

    def test_phase_in_wins_below_breakeven_and_loses_above(self):
        level, _ = dm.breakeven_trough(36)
        below = (dm.phased_value(36, 10, dm.EQ_NET, (level - 0.05, 17))
                 > dm.phased_value(1, 10, dm.EQ_NET, (level - 0.05, 17)))
        above = (dm.phased_value(36, 10, dm.EQ_NET, (level + 0.05, 17))
                 < dm.phased_value(1, 10, dm.EQ_NET, (level + 0.05, 17)))
        self.assertTrue(below)
        self.assertTrue(above)

    def test_reinvestment_shock_lowers_phase_in(self):
        base = dm.phased_value(36, 31)
        shocked = dm.phased_value(36, 31, dm.EQ_NET, None, dm.CASH_NET, 0.02)
        self.assertLess(shocked, base)


class Rounding(unittest.TestCase):
    def test_money_rounds_to_ten(self):
        self.assertEqual(dm.money(2834853.4), "$2,834,850")
        self.assertEqual(dm.money(2834855), "$2,834,860")

    def test_difference_of_rounded_figures(self):
        self.assertEqual(dm.r10(9256465.56) - dm.r10(8574343.0), 9256470 - 8574340)


class AgreementWithOwnerBrief(unittest.TestCase):
    def test_paths_a_b_c_equal_cbe(self):
        t = dm.paths_for_transfer(2045)
        r = cbe.compare()
        self.assertLess(abs(t["A"]["pv"] - r["npv_occupy_cash"]), 10)
        self.assertLess(abs(t["B"]["pv"] - r["npv_rent_cash"]), 10)
        self.assertLess(abs(t["C"]["pv"] - r["npv_sell_cash"]), 10)

    def test_equity_free_paths_do_not_move_with_crashes(self):
        base = dm.paths_for_transfer(2045)
        stressed = dm.paths_for_transfer(2045, crash=(0.43, 17))
        self.assertEqual(base["A"]["pv"], stressed["A"]["pv"])
        self.assertEqual(base["B"]["pv"], stressed["B"]["pv"])

    def test_home_sale_exclusion_is_applied_once(self):
        t = dm.paths_for_transfer(2045)
        self.assertGreater(t["F"]["sale_gain"], 0)
        self.assertGreater(t["F"]["sale_tax"], 0)
        joint = dm.paths_for_transfer(2045, joint=True)
        self.assertGreater(joint["F"]["pv"], t["F"]["pv"])

    def test_sale_tax_rates_match_components(self):
        self.assertAlmostEqual(dm.CGT_TOTAL_LTCG, 0.20 + 0.038 + 0.123 + 0.01, places=12)
        self.assertAlmostEqual(dm.CGT_TOTAL_RECAP, 0.25 + 0.038 + 0.123 + 0.01, places=12)


if __name__ == "__main__":
    unittest.main()
