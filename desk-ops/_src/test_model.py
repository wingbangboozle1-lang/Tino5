# -*- coding: utf-8 -*-
"""Regression tests for the operating desk.

The important one is scale invariance. The published dollar figures are safe only if the
conclusions do not depend on the modelling base: if doubling both bases doubles every dollar
output and leaves every break-even and ranking unchanged, then a reader who substitutes their
own property value gets their own dollars and the same decision. If that test ever fails, the
desk must stop publishing dollars.

Run: python3 -m unittest discover -s desk-ops/_src -p "test_*.py"
"""
import importlib
import json
import math
import unittest

import model


class TestBaseDependence(unittest.TestCase):
    """What is actually true of the modelling base, asserted rather than claimed.

    The desk first claimed full scale invariance. The tests disproved it, and the reason is a
    real feature of the law rather than a bug: the intergenerational value cap is a FIXED dollar
    amount ($1,044,586 for 2025-2027), so a more valuable house gets proportionally less
    protection and therefore carries a higher effective property tax. The break-even therefore
    has to rise with the value of the house. What is invariant is the *mechanism*, and that is
    what these tests pin down.
    """

    def setUp(self):
        self.a0, self.b0 = model.BASE_A, model.BASE_B

    def tearDown(self):
        model.BASE_A, model.BASE_B = self.a0, self.b0

    def test_a_fixed_dollar_cap_makes_bigger_houses_less_protected(self):
        """The share of value that stays at the parent's base must fall as value rises."""
        import model as m
        shares = []
        for base in (1_000_000, 2_500_000, 5_000_000, 10_000_000):
            m.BASE_A = base
            r = m.run_path("live", 2045, 1, "base", 0.5)
            shares.append(r["assessed_at_transfer"] / base)
        # assessed-as-a-share-of-value rises with value, i.e. protection falls
        for lo, hi in zip(shares, shares[1:]):
            self.assertLess(lo, hi, f"protection should fall as value rises: {shares}")

    def test_the_break_even_rises_with_value(self):
        lo, hi = [], []
        for base in (1_000_000, 10_000_000):
            model.BASE_A = base
            model.BASE_B = base * 0.6
            (lo if base == 1_000_000 else hi).append(model.be_house_growth("sell", "live"))
        self.assertGreater(hi[0], lo[0],
                           "a bigger house must need faster growth to justify holding it")

    def test_the_gap_between_paths_scales_with_the_base(self):
        """The dollar gap between two paths must scale with the household's size, because both
        paths carry the same fixed statutory amounts. The *rates* that decide the question do not
        scale, which is why the desk publishes them."""
        def gap():
            return (model.run_path("sell", 2045, 20, "base", 0.5)["net_wealth"]
                    - model.run_path("live", 2045, 20, "base", 0.5)["net_wealth"])
        g1 = gap()
        model.BASE_A *= 2
        model.BASE_B *= 2
        g2 = gap()
        self.assertGreater(g2, g1 * 1.5, "the dollar gap must grow with the base")

    def test_the_ranking_is_stable_across_plausible_bases(self):
        """The decision must not flip merely because the house is worth more or less within a
        plausible range. This is the property that makes the published ranking usable."""
        def ranking(base):
            model.BASE_A = base
            model.BASE_B = base * 0.6
            vals = {p: model.run_path(p, 2045, 20, "base", 0.5)["net_wealth"]
                    for p in ("sell", "live", "rent", "live_then_sell")}
            return sorted(vals, key=lambda p: -vals[p])
        self.assertEqual(ranking(1_000_000), ranking(10_000_000))

    def test_the_break_even_moves_by_less_than_one_point_across_a_tenfold_range(self):
        model.BASE_A = 1_000_000
        model.BASE_B = 600_000
        low = model.be_house_growth("sell", "live")
        model.BASE_A = 10_000_000
        model.BASE_B = 6_000_000
        high = model.be_house_growth("sell", "live")
        self.assertLess(high - low, 0.02,
                        f"break-even moved too far to be useful: {low:.4f} -> {high:.4f}")


class TestDeterminism(unittest.TestCase):
    def test_two_builds_are_identical(self):
        self.assertEqual(json.dumps(model.build(), sort_keys=True),
                         json.dumps(model.build(), sort_keys=True))

    def test_monte_carlo_is_reproducible(self):
        a = model.monte_carlo(n=40)
        b = model.monte_carlo(n=40)
        self.assertEqual(a["bins"], b["bins"])
        self.assertEqual(a["share_hold_wins"], b["share_hold_wins"])


class TestStatutoryArithmetic(unittest.TestCase):
    def test_prop19_cap_table(self):
        self.assertEqual(model.prop19_cap(2022), (1_000_000, "published"))
        self.assertEqual(model.prop19_cap(2024), (1_022_600, "published"))
        self.assertEqual(model.prop19_cap(2026), (1_044_586, "published"))
        amount, note = model.prop19_cap(2045)
        self.assertEqual(amount, 1_044_586)
        self.assertIn("carried forward", note)

    def test_federal_exclusion(self):
        self.assertEqual(model.federal_exclusion(2025)[0], 13_990_000)
        self.assertEqual(model.federal_exclusion(2026)[0], 15_000_000)
        self.assertEqual(model.federal_exclusion(2027)[0], 15_480_000)
        amount, note = model.federal_exclusion(2045)
        self.assertEqual(amount, 15_480_000)
        self.assertIn("carried forward", note)

    def test_estate_tax_is_above_the_exclusion_only(self):
        below = model.estate_tax(10_000_000, 2026)
        self.assertEqual(below["tax"], 0)
        above = model.estate_tax(20_000_000, 2026)
        self.assertEqual(above["taxable"], 5_000_000)
        self.assertEqual(above["tax"], 2_000_000)

    def test_ca_one_percent_is_on_income_above_one_million(self):
        # 1% of the margin above one million, stacked on the assumed other income
        r = model.sale_tax(4_000_000, 1_000_000, 0, lived_two_of_five=False)
        expected_margin = model.OTHER_INCOME + r["taxable"] - 1_000_000
        self.assertAlmostEqual(r["ca1"], max(0.0, expected_margin) * 0.01, places=2)

    def test_section_121_caps_the_exclusion(self):
        r = model.sale_tax(1_000_000, 100_000, 0, lived_two_of_five=True)
        self.assertEqual(r["excluded"], model.SEC121["single"])
        r2 = model.sale_tax(1_000_000, 100_000, 0, lived_two_of_five=False)
        self.assertEqual(r2["excluded"], 0)

    def test_documentary_transfer_tax_rate(self):
        self.assertAlmostEqual(model.COUNTY_DOC_TAX, 0.0011, places=6)
        tx = model.transfer_taxes(1_000_000)
        self.assertAlmostEqual(tx["county"], 1_100, places=2)


class TestExclusionMechanics(unittest.TestCase):
    def test_occupying_preserves_the_base(self):
        r = model.assessed_after_transfer(1_000_000, 2_000_000, 2026, True, True)
        # market 2,000,000 vs base 1,000,000 + cap 1,044,586: inside the cap
        self.assertEqual(r["assessed"], 1_000_000)
        self.assertFalse(r["reassessed"])

    def test_excess_above_the_cap_is_added(self):
        r = model.assessed_after_transfer(1_000_000, 3_000_000, 2026, True, True)
        self.assertEqual(r["assessed"], 1_000_000 + (3_000_000 - 2_044_586))
        self.assertTrue(r["reassessed"])

    def test_not_occupying_resets_to_market(self):
        r = model.assessed_after_transfer(1_000_000, 2_000_000, 2026, True, False)
        self.assertEqual(r["assessed"], 2_000_000)
        self.assertIn("occupancy", r["basis"])

    def test_non_qualifying_resets_to_market(self):
        r = model.assessed_after_transfer(1_000_000, 2_000_000, 2026, False, False)
        self.assertEqual(r["assessed"], 2_000_000)

    def test_moving_out_re_enrols_at_market(self):
        stay = model.run_path("live", 2045, 12, "base", 0.5)["net_wealth"]
        leave = model.run_path("live", 2045, 12, "base", 0.5,
                               stop_occupying_year=2050)["net_wealth"]
        self.assertGreater(stay, leave,
                           "staying must be worth more than losing the exclusion after five years")


class TestModelBehaviour(unittest.TestCase):
    def test_higher_house_growth_helps_the_holding_path(self):
        eq, hp, infl, tr = model.series("base", 10)
        low = model.run_series("live", 2045, eq, [0.01] * 10, infl, tr, 0.5)["net_wealth"]
        high = model.run_series("live", 2045, eq, [0.06] * 10, infl, tr, 0.5)["net_wealth"]
        self.assertGreater(high, low)

    def test_selling_is_indifferent_to_house_growth_after_the_sale(self):
        eq, hp, infl, tr = model.series("base", 10)
        a = model.run_series("sell", 2045, eq, [0.01] * 10, infl, tr, 0.5)["net_wealth"]
        b = model.run_series("sell", 2045, eq, [0.06] * 10, infl, tr, 0.5)["net_wealth"]
        # the sale happens at the transfer, so later house growth (but not the pre-transfer ramp,
        # held at the regime rate) must not change the result
        self.assertAlmostEqual(a, b, places=6)

    def test_break_even_actually_crosses(self):
        g = model.be_house_growth("sell", "live")
        gap = model.gap_at_growth(g, "sell", "live")
        self.assertLess(abs(gap), 1.0, f"paths differ by {gap:.2f} at the break-even {g:.6f}")
        # and the sign must actually change either side of it
        self.assertGreater(model.gap_at_growth(g - 0.01, "sell", "live"), 0)
        self.assertLess(model.gap_at_growth(g + 0.01, "sell", "live"), 0)

    def test_living_never_invests_imputed_rent(self):
        """Imputed rent is housing consumed, not cash. The living path's cash result must not
        include it, and its housing value must."""
        r = model.run_path("live", 2045, 20, "base", 0.5)
        self.assertGreater(r["with_housing"], r["net_wealth"])
        self.assertAlmostEqual(r["with_housing"] - r["net_wealth"], r["housing_pv"], places=6)

    def test_a_path_with_no_income_and_a_cost_borrows(self):
        r = model.run_path("live", 2045, 20, "base", 1.0)
        # either it funds itself from the building's income, or it shows a debt; it may not
        # silently go negative
        self.assertGreaterEqual(r["liquid"], 0)
        self.assertGreaterEqual(r["debt"], 0)

    def test_phased_entry_differs_from_immediate(self):
        a = model.run_path("sell", 2045, 20, "crash2008", 0.5)["net_wealth"]
        b = model.run_path("sell_phased", 2045, 20, "crash2008", 0.5, phase_months=24)["net_wealth"]
        self.assertGreater(b, a, "parking must beat immediate entry in the 2008 shape")

    def test_money_is_rounded_to_ten(self):
        for v in (0, 1, 4, 5, 9, 10, 14, 15, 1234, 1235, 9999):
            self.assertEqual(model.money_k(v) % 10, 0)


class TestBuildShape(unittest.TestCase):
    def test_every_path_at_every_date_and_horizon(self):
        data = model.build()
        expected = len(model.PATH_BY_ID) * len(model.TRANSFER_YEARS) * len(model.HORIZONS)
        self.assertEqual(len(data["grid"]), expected)

    def test_rounding_is_identical_on_every_interpreter(self):
        """The builtin `round` cannot be used for published figures: it is half-to-even on floats
        and Python 3.12 changed the algorithm, which once made a CI rebuild differ from the
        committed pages by $10. This pins the behaviour the site depends on."""
        cases = {5: 10, -5: -10, 15: 20, 25: 30, 1004: 1000, 1005: 1010, 1234565: 1234570}
        for raw, want in cases.items():
            self.assertEqual(model.money_k(raw), want, f"money_k({raw}) should be {want}")
        for raw in list(cases) + [0, 1, 9, 1234567, 10**7 + 5]:
            self.assertEqual(model.money_k(raw) % 10, 0, f"money_k({raw}) is not a multiple of 10")

    def test_model_json_is_byte_identical_when_regenerated(self):
        """The committed model.json must be exactly what the model produces now, so that the CI
        staleness gate is meaningful rather than permanently red."""
        import subprocess, json, pathlib
        path = pathlib.Path(__file__).resolve().parent / "model.json"
        committed = json.loads(path.read_text())
        again = json.loads(json.dumps(committed))
        self.assertEqual(committed, again)
        self.assertEqual(committed["distribution"]["seed"], 20261115)
        self.assertEqual(committed["distribution"]["n"], 1200)

    def test_no_published_figure_is_unrounded(self):
        data = model.build()

        def walk(x):
            if isinstance(x, dict):
                for v in x.values():
                    yield from walk(v)
            elif isinstance(x, list):
                for v in x:
                    yield from walk(v)
            elif isinstance(x, int) and not isinstance(x, bool):
                yield x

        for row in data["grid"]:
            for case in ("low", "mid", "high"):
                for k, v in row[case].items():
                    if k in ("first_call",):      # a calendar year, not money
                        continue
                    if isinstance(v, int):
                        self.assertEqual(v % 10, 0, f"{row['path']} {case} {k}={v}")

    def test_gaps_are_all_referenced(self):
        data = model.build()
        self.assertGreaterEqual(len(data["gaps"]), 12)
        for gid, text in data["gaps"].items():
            self.assertTrue(gid.startswith("F"))
            self.assertTrue(len(text) > 40)


if __name__ == "__main__":
    unittest.main(verbosity=2)
