# -*- coding: utf-8 -*-
"""Regression tests for the phase-99220 model layer. Run: python3 -m unittest discover -s phase-99220/_src -p "test_*.py" -v"""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import desk_model as X  # noqa: E402

M = X.M


class RoundingTests(unittest.TestCase):
    def test_r10_nearest_ten(self):
        self.assertEqual(M.r10(1234), 1230)
        self.assertEqual(M.r10(1235), 1240)
        self.assertEqual(M.r10(-1235), -1240)

    def test_every_headline_figure_is_multiple_of_ten(self):
        h = X.headline()
        for k, v in h.items():
            if k in ("transfer_year", "years_after"):
                continue
            if isinstance(v, int) and abs(v) >= 1000:
                self.assertEqual(v % 10, 0, k)


class BreakEvenTests(unittest.TestCase):
    def test_portfolio_break_even_equalises_sell_and_live_in(self):
        p = X.breakevens()["portfolio_return"]
        r = M.compare(portfolio_return=p)
        self.assertAlmostEqual(r["npv_sell_econ"], r["npv_occupy_econ"], delta=5000)

    def test_price_growth_break_even_equalises(self):
        g = X.breakevens()["price_growth"]
        r = M.compare(price_growth=g)
        self.assertAlmostEqual(r["npv_sell_econ"], r["npv_occupy_econ"], delta=5000)

    def test_sell_leads_below_price_break_even(self):
        r = M.compare(price_growth=0.03)
        self.assertGreater(r["npv_sell_econ"], r["npv_occupy_econ"])


class ReplayTests(unittest.TestCase):
    def test_index_endpoints(self):
        p = X.index_path(X.CRASH_1929, 400)
        self.assertAlmostEqual(p[0], 1.0)
        self.assertAlmostEqual(p[X.CRASH_1929["months_down"]], 0.11, places=9)
        self.assertAlmostEqual(p[X.CRASH_1929["months_down"] + X.CRASH_1929["months_up"]], 1.0, places=9)

    def test_2008_index_endpoints(self):
        p = X.index_path(X.CRASH_2008, 100)
        self.assertAlmostEqual(p[17], 0.43, places=9)
        self.assertAlmostEqual(p[65], 1.0, places=9)

    def test_lump_no_crash_compounds_at_net_return(self):
        rp = X.replay(X.CRASH_1929)
        inv = rp["invested"]
        expected = inv * (1.0 + X.NET_GROWTH) ** 10
        self.assertAlmostEqual(rp["results"]["lump"]["nocrash_10y"], expected, delta=inv * 0.001)

    def test_lump_crash_low_matches_drop(self):
        rp = X.replay(X.CRASH_1929)
        self.assertAlmostEqual(rp["results"]["lump"]["lowest"], rp["invested"] * 0.11, delta=20)

    def test_park_36_has_no_loss_before_buying(self):
        rp = X.replay(X.CRASH_1929)
        self.assertGreaterEqual(rp["results"]["park_36_phase_12"]["lowest"], rp["invested"] - 10)


class MixedTests(unittest.TestCase):
    def test_sell_now_beats_park_when_no_crash(self):
        mv = X.mixed_paths()["values"]
        self.assertGreater(mv["sell_now"], mv["park_36_phase_12"])

    def test_park_longer_is_worse_without_crash(self):
        a = X.mixed_paths(park_months=24)["values"]["park_24_phase_12"]
        b = X.mixed_paths(park_months=36)["values"]["park_36_phase_12"]
        self.assertGreater(a, b)


if __name__ == "__main__":
    unittest.main()
