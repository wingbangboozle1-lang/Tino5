"""Regression tests for review-092b.

Run: python3 -m unittest discover -s review-092b/_src -p "test_*.py"
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC))

import build  # noqa: E402
import engine  # noqa: E402
import verify  # noqa: E402
from engine import (A, BASE_YEAR, CPI_MONTH, HORIZONS, OFFICIAL, build_regimes,
                    break_even_equity, break_even_growth, compound_schedule, fed_exclusion,
                    money, path_wealth, prop13_taxable, prop19_new_taxable, r10, schedule,
                    transfer_table)


class TestFormatting(unittest.TestCase):
    def test_r10_rounds_to_ten(self):
        self.assertEqual(r10(1_234_567), 1_234_570)
        self.assertEqual(r10(1_234_564), 1_234_560)
        self.assertEqual(r10(5), 10)          # half rounds away from zero, not to even
        self.assertEqual(r10(-5), -10)
        self.assertEqual(r10(-1_234_563), -1_234_560)

    def test_money_puts_sign_before_the_dollar(self):
        self.assertEqual(money(1_234_560), "$1,234,560")
        self.assertEqual(money(-59_572_310), "−$59,572,310")
        self.assertNotIn("$-", money(-1_000))
        self.assertEqual(money(None), "—")

    def test_enforce_rounding_spares_statutory_amounts_and_shorthand(self):
        src = ('<p>$1,044,586</p><span class="stat">$1,044,586</span>'
               '<p>$15M and $0.55 per $500 and $1,000 of premium</p>')
        out = build.enforce_rounding(src)
        self.assertIn('<p>$1,044,590</p>', out)
        self.assertIn('<span class="stat">$1,044,586</span>', out)
        self.assertIn("$15M", out)
        self.assertIn("$0.55 per $500", out)
        self.assertIn("$1,000 of premium", out)

    def test_enforce_rounding_marks_publisher_hosts(self):
        out = build.enforce_rounding('<a href="https://www.sf.gov/x">sf.gov</a>')
        self.assertIn('href="https://www.sf.gov/x"', out)   # URL untouched
        self.assertIn('<span class="host">sf.gov</span>', out)


class TestPropertyTax(unittest.TestCase):
    def test_prop13_cap_compounds(self):
        self.assertAlmostEqual(prop13_taxable(100_000, 2026 + 10), 100_000 * 1.02 ** 10)

    def test_prop19_telescopes_to_value_minus_allowance_above_the_cap(self):
        fbyv, fmv, allowance = 500_000.0, 3_000_000.0, 1_000_000.0
        cap = fbyv + allowance
        # above the cap the enrolled value telescopes to fair market value minus the allowance
        self.assertAlmostEqual(prop19_new_taxable(fmv, fbyv, allowance), fmv - allowance)
        # inside the cap the factored base value carries over untouched
        self.assertAlmostEqual(prop19_new_taxable(fbyv + 500_000, fbyv, allowance), fbyv)
        self.assertAlmostEqual(prop19_new_taxable(cap, fbyv, allowance), fbyv)
        # at or below the cap, the factored base value simply carries over
        self.assertAlmostEqual(prop19_new_taxable(fbyv - 1, fbyv, allowance), fbyv)

    def test_occupying_never_costs_more_tax_than_renting(self):
        for y in HORIZONS:
            t = transfer_table(y)
            self.assertLessEqual(t["p1_tax"], t["p2_tax"])
            self.assertGreater(t["tax_gap"], 0)

    def test_sale_at_transfer_is_tax_free(self):
        t = transfer_table(2045)
        self.assertEqual(t["cap_gain_tax_if_sold_at_transfer"], 0)
        self.assertLess(t["net_sale"], t["fmv"])          # costs are deducted
        self.assertGreater(t["net_sale"], t["fmv"] * 0.9)


class TestWealthModel(unittest.TestCase):
    def test_six_percent_house_growth_favours_keeping_the_house(self):
        saved = A["a_growth"].value
        try:
            A["a_growth"].value = 6.0
            w = path_wealth(2045)
        finally:
            A["a_growth"].value = saved
        self.assertGreater(max(w["P1"], w["P2"]), w["P3"])

    def test_central_case_prefers_selling(self):
        w = path_wealth(2045)
        self.assertGreater(w["P3"], w["P2"])
        self.assertGreater(w["P2"], w["P1"])

    def test_break_even_growth_sits_inside_the_tested_range(self):
        for y in HORIZONS:
            be = break_even_growth(y)
            self.assertIsInstance(be, float)
            self.assertGreater(be, 2.0)
            self.assertLess(be, 12.0)

    def test_break_even_equity_is_the_solved_tie(self):
        be = break_even_equity(2045)
        self.assertIsInstance(be, float)
        regime = dict(code="base", hpi_ann=A["a_growth"].value,
                      cpi_ann=A["inflation"].value, episode_years=25)
        # `equity_real` is the real return; the total is the regime CPI plus that spread
        below = engine.regime_outcome(2045, regime=regime,
                                      equity_real=be - 0.75 - regime["cpi_ann"])
        above = engine.regime_outcome(2045, regime=regime,
                                      equity_real=be + 0.75 - regime["cpi_ann"])
        self.assertIn(below["best"], ("P1", "P2"))     # weak reinvestment: keeping A wins
        self.assertEqual(above["best"], "P3")          # strong reinvestment: selling wins

    def test_a_regime_shock_is_not_applied_for_the_whole_horizon(self):
        """The defect this guards: a two-year crash compounded for 25 years."""
        s2 = [r for r in build_regimes() if r["code"] == "S2"][0]
        out = engine.regime_outcome(2045, regime=s2)
        self.assertAlmostEqual(out["growth_path"][0], s2["hpi_ann"], places=9)
        self.assertEqual(out["growth_path"][-1], A["a_growth"].value)
        self.assertEqual(out["growth_path"].count(A["a_growth"].value), 25 - s2["episode_years"])

    def test_schedule_and_compounding(self):
        self.assertEqual(schedule(8.0, 5, 2.5, episode=2), [8.0, 8.0, 2.5, 2.5, 2.5])
        self.assertEqual(schedule(8.0, 3, 2.5, episode=9), [8.0, 8.0, 8.0])
        self.assertAlmostEqual(compound_schedule(100.0, [10.0, -10.0]), 99.0)

    def test_no_negative_prices_in_any_path(self):
        for y in HORIZONS:
            w = path_wealth(y)
            for k in ("P1", "P2", "P3"):
                self.assertGreater(w[k], 0)


class TestRegimes(unittest.TestCase):
    def setUp(self):
        self.regimes = {r["code"]: r for r in build_regimes()}

    def test_five_regimes(self):
        self.assertEqual(sorted(self.regimes), ["S1", "S2", "S3", "S4", "S5"])

    def test_windows_match_the_series_they_claim(self):
        self.assertIn("1973", self.regimes["S1"]["cpi_window"])
        self.assertEqual(self.regimes["S3"]["cpi_window"], "Jan 2022–Jan 2023")
        self.assertEqual(self.regimes["S3"]["hpi_window"], "2022Q2–2023Q1")
        self.assertTrue(self.regimes["S4"]["cpi_window"].startswith("Apr 2020"))

    def test_housing_bust_is_negative_in_real_terms(self):
        self.assertLess(self.regimes["S2"]["hpi"], 0)
        self.assertLess(self.regimes["S2"]["real"], self.regimes["S2"]["hpi"])

    def test_stagflation_loses_half_its_real_value(self):
        self.assertAlmostEqual(self.regimes["S1"]["real"], -49.5, places=1)

    def test_annualised_rates_reconstruct_the_total(self):
        for code, r in self.regimes.items():
            months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                      "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
            m = re.match(r"(\w{3}) (\d{4})–(\w{3}) (\d{4})", r["cpi_window"])
            yrs = max(1, (int(m.group(4)) - int(m.group(2))) * 12
                      + months[m.group(3)] - months[m.group(1)]) / 12
            rebuilt = ((1 + r["cpi_ann"] / 100) ** yrs - 1) * 100
            self.assertAlmostEqual(rebuilt, r["cpi"], places=6)


class TestSiteOutput(unittest.TestCase):
    def test_page_set_is_exactly_expected(self):
        self.assertEqual({p.name for p in verify.OUT.glob("*.html")}, verify.EXPECTED)

    def test_every_row_has_a_traceable_source(self):
        errors = []
        for p in verify.OUT.glob("*.html"):
            verify.Check(p).feed(p.read_text())
        self.assertEqual(verify.errors, [])

    def test_privacy_patterns_absent_from_every_page(self):
        for p in verify.OUT.glob("*.html"):
            text = p.read_text()
            for bad in ("Cupertino", "Outer Sunset", "94122", "95014"):
                self.assertNotIn(bad, text, f"{bad} in {p.name}")

    def test_no_active_content(self):
        for p in verify.OUT.glob("*.html"):
            text = p.read_text()
            for tag in ("<script", "<form", "<iframe", "http://"):
                self.assertNotIn(tag, text, f"{tag} in {p.name}")

    def test_verifier_passes_end_to_end(self):
        self.assertEqual(verify.main(), 0)


if __name__ == "__main__":
    unittest.main()
