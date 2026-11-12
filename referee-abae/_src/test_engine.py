"""Tests for the reference engine. Synthetic anchors only; the desk reproduction test loads the desk's own
anchors at run time and is skipped when the desk module is not present.

Run:  python3 -m unittest discover -s referee-abae/_src -p 'test_*.py' -v
"""
import importlib.util
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import engine as E  # noqa: E402

SYN = dict(v0=1_000_000.0, taxable0=200_000.0, fixed=300.0, insurance=2_000.0, water=1_000.0, maint=5_000.0,
           reserve=2_000.0, elec_pre=0.0, elec_post=300.0, rent0=40_000.0)


def P(**kw):
    d = dict(SYN)
    d.update(kw)
    return E.Params(**d)


class Allowance(unittest.TestCase):
    def test_statute_adjustment_counts(self):
        # adjustments on every other 16 February from 2027: 2027, 2029, ... ; count by transfer year
        for T, n in ((2026, 0), (2027, 1), (2028, 1), (2029, 2), (2040, 7), (2045, 10), (2050, 12)):
            p = P(allowance_mode="statute", g=0.04)
            self.assertAlmostEqual(E.allowance(p, T) / p.allowance0, 1.04 ** n, places=9, msg=str(T))

    def test_desk_mode_close_to_statute_at_matching_growth(self):
        # a 2%/yr allowance is the statutory mechanism (one year of HPI per two years) at 4% HPI growth
        for T in (2040, 2045, 2050):
            a = E.allowance(P(allowance_mode="statute", g=0.04), T)
            b = E.allowance(P(allowance_mode="desk", ag=0.02), T)
            self.assertLess(abs(a / b - 1), 0.02)

    def test_value_limit_test(self):
        self.assertEqual(E.prop19_taxable(900.0, 500.0, 500.0), 500.0)     # within limit: base value kept
        self.assertEqual(E.prop19_taxable(1000.0, 500.0, 500.0), 500.0)    # exactly at the limit
        self.assertEqual(E.prop19_taxable(1300.0, 500.0, 500.0), 800.0)    # excess added
        self.assertEqual(E.prop19_taxable(1300.0, 500.0, 500.0), 1300.0 - 500.0)


class Paths(unittest.TestCase):
    def test_s3_formula(self):
        p = P()
        x = E.run(p, 2045)
        self.assertAlmostEqual(x["S3"], E.fmv(p, 2045) * (1 - p.sell) * (1 + p.r) ** p.h, places=4)

    def test_s3_does_not_depend_on_rent_or_tax_inputs(self):
        a = E.run(P(), 2040)["S3"]
        b = E.run(P(rent0=90_000.0, t_ord=0.2, t_cg=0.1, t_rec=0.1, bldg=0.2, taxable0=1.0), 2040)["S3"]
        self.assertAlmostEqual(a, b, places=4)

    def test_rent_path_uses_full_reassessment(self):
        x = E.run(P(), 2045)
        self.assertAlmostEqual(x["assess_rent"], x["fmv_T"], places=6)
        self.assertLessEqual(x["assess_occ"], x["assess_rent"])

    def test_higher_rent_raises_s2_only(self):
        lo, hi = E.run(P(rent0=40_000.0), 2045), E.run(P(rent0=80_000.0), 2045)
        self.assertGreater(hi["S2"], lo["S2"])
        self.assertAlmostEqual(hi["S1"], lo["S1"], places=4)

    def test_terminal_conventions_order(self):
        d, l, h = (E.run(P(terminal=t), 2045) for t in ("desk", "liquidate_all", "hold_all"))
        self.assertLess(l["S3"], d["S3"])                  # taxing the portfolio lowers S3
        self.assertAlmostEqual(h["S3"], d["S3"], places=4)  # holding changes nothing for S3
        self.assertGreaterEqual(h["S2"], d["S2"])           # no terminal tax raises S2 ...
        self.assertGreaterEqual(h["S1"], d["S1"])           # ... and S1
        self.assertAlmostEqual(l["S2"], d["S2"], places=4)

    def test_breakeven_return_exists_and_is_monotone(self):
        f = lambda r: E.run(E.with_(P(), r=r), 2045)["S3"] - E.run(E.with_(P(), r=r), 2045)["S2"]
        self.assertLess(f(0.0), 0.0)
        self.assertGreater(f(0.15), 0.0)
        r_star = E.bisect(f, 0.0, 0.15)
        self.assertAlmostEqual(f(r_star), 0.0, delta=1.0)

    def test_horizon_is_exactly_h_periods(self):
        x = E.run(P(h=25), 2045)
        self.assertEqual(x["end"], 2070)
        with self.assertRaises(Exception):
            E.run(P(h=0), 2045)["S1"]  # an empty horizon must not silently produce a wealth figure


class Bisect(unittest.TestCase):
    def test_root(self):
        self.assertAlmostEqual(E.bisect(lambda x: x ** 3, -1.0, 2.0, target=0.0), 0.0, places=6)
        self.assertAlmostEqual(E.bisect(lambda x: x * x, 0.0, 3.0, target=2.0), 2 ** 0.5, places=6)


class DeskReproduction(unittest.TestCase):
    """Compare with desk-b4f's own module. Skipped when the desk or its module is absent."""

    def setUp(self):
        path = HERE.parents[1] / "desk-b4f" / "scripts" / "after_tax_model.py"
        if not path.exists():
            self.skipTest("desk-b4f module not present in this checkout")
        spec = importlib.util.spec_from_file_location("desk_after_tax_model", path)
        self.desk = importlib.util.module_from_spec(spec)
        sys.modules["desk_after_tax_model"] = self.desk   # dataclasses need the module registered
        spec.loader.exec_module(self.desk)

    def test_three_paths_match_within_ten_dollars(self):
        from reproduce import params_from_desk
        p = params_from_desk(self.desk)
        for T in (2040, 2045, 2050):
            mine, theirs = E.run(p, T), self.desk.simulate_after_tax(T)
            for a, b in (("S1", "s1_wealth"), ("S2", "s2_wealth"), ("S3", "s3_wealth")):
                self.assertLessEqual(abs(mine[a] - theirs[b]), 10.0, f"{a} {T}")


if __name__ == "__main__":
    unittest.main()
