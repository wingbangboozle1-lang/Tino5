"""Unit tests for desk-b4f after_tax_model.py."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import after_tax_model as m


class AfterTaxModelTests(unittest.TestCase):
    def test_2026_anchors_match_baseline_to_10(self):
        a26 = m.a_continuity_row(2026)
        b26 = m.b_continuity_row(2026)
        self.assertEqual(m.money(a26["tax"]), "$6,880")
        self.assertEqual(m.money(b26["tax"]), "$2,430")
        self.assertEqual(m.money(b26["noi"]), "$53,430")

    def test_prop19_exact_boe_rule(self):
        # Under ceiling: taxable stays old taxable
        self.assertEqual(m.prop19_taxable(1_400_000, 500_000, 1_044_586), 500_000)
        # Over ceiling: old taxable + (fmv - (old taxable + allowance))
        self.assertEqual(m.prop19_taxable(2_000_000, 500_000, 1_044_586), 955_414)

    def test_nem_20yr_sunset_activates_at_2043(self):
        before = m.electric_cost_a(2042, apply_sunset=True)
        at_sunset = m.electric_cost_a(2043, apply_sunset=True)
        self.assertLess(before, 0)
        self.assertGreater(at_sunset, 0)

    def test_sec121_exclusion_reduces_s1_tax(self):
        no_121 = m.simulate_after_tax(2045, sec121_exclusion=0)
        single = m.simulate_after_tax(2045, sec121_exclusion=250_000)
        mfj = m.simulate_after_tax(2045, sec121_exclusion=500_000)
        self.assertAlmostEqual(mfj["sec121_tax_saved"], 500_000 * 0.371, places=2)
        self.assertAlmostEqual(single["sec121_tax_saved"], 250_000 * 0.371, places=2)
        self.assertGreater(mfj["s1_wealth"], single["s1_wealth"])
        self.assertGreater(single["s1_wealth"], no_121["s1_wealth"])

    def test_sec469_active_allowance_helps_low_magi_s2(self):
        hi = m.simulate_after_tax(2045, magi_high=True)
        lo = m.simulate_after_tax(2045, magi_high=False)
        self.assertGreater(lo["s2_wealth"], hi["s2_wealth"])
        self.assertLess(lo["suspended_pal_end"], hi["suspended_pal_end"])

    def test_fixed_parcel_charges_do_not_scale_with_reassessment(self):
        # Fixed charges are identical in S1 and S2 year 1 despite ~3.6x difference in assessed value
        res = m.simulate_after_tax(2045)
        diff_tax = res["tax_s2_yr1"] - res["tax_s1_yr1"]
        expected_adval_diff = (res["assess_s2"] - max(res["assess_s1"] - m.A.homeowners_exemption, 0)) * m.A.ad_valorem_rate
        self.assertAlmostEqual(diff_tax, expected_adval_diff, places=4)

    def test_sfpuc_fy27_fy28_rate_steps(self):
        b26 = m.b_continuity_row(2026)
        b27 = m.b_continuity_row(2027)
        b28 = m.b_continuity_row(2028)
        self.assertAlmostEqual(b27["water"] / b26["water"], 1.125, places=6)
        self.assertAlmostEqual(b28["water"] / b27["water"], 1.123, places=6)

    def test_estate_headroom_dsue_exceeds_single(self):
        rows = m.estate_headroom_matrix()
        for r in rows:
            self.assertGreater(r["headroom_dsue"], r["headroom_single"])
            self.assertGreater(r["headroom_single"], r["headroom_halved"])

    def test_invalid_horizon_rejected(self):
        with self.assertRaises(ValueError):
            m.simulate_after_tax(2045, horizon=0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
