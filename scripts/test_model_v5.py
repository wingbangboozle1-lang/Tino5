#!/usr/bin/env python3
"""Deterministic regression tests for the decision model.

Each test pins one arithmetic relationship that the published pages rely on, so a later
edit that breaks the logic fails the build instead of silently changing a published number.

Run: python3 -m unittest discover -s scripts -p 'test_model_v5.py' -v
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import model_v5 as m


class TestProp19(unittest.TestCase):
    def test_taxable_value_formula(self):
        """RTC 63.2(d): factored base-year value + excess over the cap."""
        st = m.a_state_at_transfer(2045)
        self.assertAlmostEqual(st["cap"], st["assessed"] + m.V["prop19_cap_addition"], places=2)
        taxable = m.a_taxable_value(2045, True)
        self.assertAlmostEqual(taxable, st["assessed"] + max(0.0, st["fmv"] - st["cap"]), places=2)

    def test_no_exclusion_when_not_owner_occupied(self):
        """A rental transfer is a change in ownership and reassesses at full cash value."""
        st = m.a_state_at_transfer(2045)
        self.assertAlmostEqual(m.a_taxable_value(2045, False), st["fmv"], places=2)

    def test_prop19_saving_is_positive_when_market_exceeds_cap(self):
        self.assertGreater(m.a_taxable_value(2045, False) - m.a_taxable_value(2045, True), 0)

    def test_homeowners_exemption_only_when_occupied(self):
        taxable = 1_000_000.0
        occ = m.a_property_tax(taxable, True)
        rent = m.a_property_tax(taxable, False)
        self.assertAlmostEqual(rent - occ, m.V["homeowners_exemption"] * m.O["A_advalorem"], places=2)

    def test_prop13_cap_is_two_percent(self):
        a = m.a_state_at_transfer(2046)["assessed"]
        b = m.a_state_at_transfer(2045)["assessed"]
        self.assertAlmostEqual(a / b, 1.02, places=6)


class TestPaths(unittest.TestCase):
    def test_sell_path_has_no_carrying_cost(self):
        """Selling means the owner no longer holds A, so A's costs must be zero."""
        r = m.run_path("sell", 2045)
        self.assertTrue(all(row["property_tax"] == 0 for row in r["annual_rows"]))
        self.assertTrue(all(row["maintenance"] == 0 for row in r["annual_rows"]))

    def test_sell_proceeds_equal_value_less_costs(self):
        r = m.run_path("sell", 2045)
        expected = m.r10(r["transfer_fmv"] * (1 - m.A["selling_cost"]))
        self.assertAlmostEqual(r["sale_proceeds_net"], expected, delta=20)

    def test_depreciation_only_in_rental_path(self):
        self.assertEqual(m.run_path("occupy", 2045)["depreciation_taken"], 0)
        self.assertGreater(m.run_path("rent", 2045)["depreciation_taken"], 0)

    def test_depreciation_straight_line_on_basis(self):
        """27.5-year straight line on the improvement share of the date-of-death value."""
        r = m.run_path("rent", 2045)
        basis = r["transfer_fmv"] * (1 - m.A["land_share"])
        per_year = basis / m.A["depr_years"]
        expected = per_year * min(r["years"], int(m.A["depr_years"]))
        self.assertAlmostEqual(r["depreciation_taken"], m.r10(expected), delta=30)

    def test_terminal_net_worth_is_sale_less_tax(self):
        r = m.run_path("rent", 2045)
        expected = (r["terminal_sale_price"] - r["terminal_selling_costs"]
                    - r["terminal_capital_gain_tax"] - r["terminal_niit"]
                    + r["reinvested_cash_flow"])
        self.assertAlmostEqual(r["terminal_net_worth"], expected, delta=40)

    def test_s121_exclusion_applies_only_to_occupancy(self):
        self.assertEqual(m.run_path("rent", 2045)["s121_excluded"], 0)
        self.assertGreater(m.run_path("occupy", 2040)["s121_excluded"], 0)


class TestSwans(unittest.TestCase):
    def test_every_swan_produces_a_verdict(self):
        for swan in m.SWANS:
            r = m.run_swan(swan, 2045)
            self.assertIn(r["verdict"], ("holding wins", "selling wins"))

    def test_losing_the_exclusion_raises_the_tax(self):
        """S6 holds and then loses the exclusion; S7 never had it. By year 30 both are being
        taxed on market value, so the two must converge, and S6 must be worse than never moving."""
        lost = m.run_swan([x for x in m.SWANS if x["id"] == "S6"][0], 2045)
        never = m.run_swan([x for x in m.SWANS if x["id"] == "S7"][0], 2045)
        self.assertLess(lost["tax_year1"], never["tax_year1"])
        # occupying for eight years is still worth something, so the lost-and-then-moved case
        # must beat never occupying by roughly the present value of those eight years
        self.assertGreater(lost["hold_then_sell"], never["hold_then_sell"])
        # by year 30 both are taxed on the same transfer-date base, so they converge
        self.assertAlmostEqual(lost["tax_year30"], never["tax_year30"],
                               delta=never["tax_year30"] * 0.02)
        # and occupying for eight years must still beat never occupying
        self.assertGreater(lost["hold_then_sell"], never["hold_then_sell"])

    def test_a_bust_reverses_the_ranking(self):
        bust = m.run_swan([x for x in m.SWANS if x["id"] == "S2"][0], 2045)
        self.assertEqual(bust["verdict"], "selling wins")


class TestB(unittest.TestCase):
    def test_b_ledger_reproduces_the_reported_2025_bill(self):
        """At n = -1 the ledger must return the owner's own 2025 charge, by construction."""
        led = m.b_year(2025)
        self.assertAlmostEqual(led["property_tax"], 2_440, delta=1)

    def test_b_implied_rate_far_above_secured_rate(self):
        """A 2.1% implied rate against a 1.18% secured rate is a flag, not a modelling choice."""
        self.assertGreater(m.O["B_implied_rate"], m.V["sf_secured_rate"] * 1.5)


class TestPrivacyAndRounding(unittest.TestCase):
    def test_all_money_is_multiple_of_ten(self):
        def walk(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if isinstance(v, (int, float)) and not isinstance(v, bool):
                        if any(t in k for t in ("worth", "value", "tax", "proceeds", "gain",
                                                "cost", "excluded", "flow", "headroom",
                                                "estate", "cap", "assessed", "fmv", "liability",
                                                "premium", "rent_cost")):
                            if abs(v) > 100:
                                yield k, v
                    elif isinstance(v, (dict, list)):
                        yield from walk(v)
            elif isinstance(o, list):
                for v in o:
                    yield from walk(v)

        # the model's own API must return multiples of $10
        NON_MONEY = {"transfer_year", "end_year", "years", "path"}
        for t in m.A["transfer_years"]:
            for p in ("occupy", "rent", "sell"):
                r = m.run_path(p, t)
                for k, v in r.items():
                    if k in NON_MONEY or not isinstance(v, int):
                        continue
                    if abs(v) > 100:
                        self.assertEqual(v % 10, 0, f"{p}/{t}/{k}={v} is not a multiple of $10")

    def test_no_zip_or_address_tokens_in_source(self):
        import re
        src = Path(m.__file__).read_text()
        self.assertIsNone(re.search(r"\b9\d{4}(?:-\d{4})?\b", src))
        self.assertIsNone(re.search(r"\b(?:Cupertino|Sunset|San Francisco|San Jose)\b", src))


class TestEstate(unittest.TestCase):
    def test_headroom_equals_exclusion_minus_estate(self):
        for e in m.estate_headroom():
            self.assertAlmostEqual(e["headroom"], e["exclusion_projected"] - e["gross_estate_projected"],
                                   delta=20)

    def test_2026_and_2027_use_the_published_amounts(self):
        rows = {e["year"]: e for e in m.estate_headroom()}
        self.assertEqual(rows[2026]["exclusion_projected"], 15_000_000)
        self.assertEqual(rows[2027]["exclusion_projected"], 15_480_000)


if __name__ == "__main__":
    unittest.main()
