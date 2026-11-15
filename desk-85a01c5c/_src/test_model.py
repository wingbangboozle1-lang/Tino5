"""Unit tests for the desk-85a01c5c model. Run:
    python3 -m unittest discover -s desk-85a01c5c/_src -p "test_*.py" -v
"""
import unittest

import model as M


class TestRounding(unittest.TestCase):
    def test_m0_nearest_ten(self):
        self.assertEqual(M.m0(1234), "$1,230")
        self.assertEqual(M.m0(1235.01), "$1,240")
        self.assertEqual(M.m0(-56.7), "$-60")
        self.assertEqual(M.m0(None), "")

    def test_m10(self):
        self.assertEqual(M.m10(1234), 1230)
        self.assertEqual(M.m10(55), 60)


class TestPaths(unittest.TestCase):
    def test_2008_official_anchors(self):
        p = M.equity_index_path(M.CRASH_2008)
        self.assertEqual(p[0], 1.0)
        self.assertAlmostEqual(p[17], 0.43, places=3)  # official -57%
        # ERP B-55 2013 level above the 2007 peak, held flat afterwards
        expected_2013 = M.ERP_SP500[2013][0] / M.ERP_SP500[2007][0]
        self.assertAlmostEqual(p[74], expected_2013, places=3)
        self.assertEqual(p[77], expected_2013)
        self.assertEqual(p[-1], expected_2013)
        # drawdown is monotonically non-increasing to the trough
        self.assertTrue(all(p[i] >= p[17] for i in range(17)))

    def test_1929_official_anchors(self):
        p = M.equity_index_path(M.CRASH_1929)
        self.assertAlmostEqual(p[34], 0.11, places=3)   # official -89%
        self.assertAlmostEqual(p[303], 1.0, places=4)   # official Nov 1954
        self.assertTrue(all(p[i] >= p[34] for i in range(34)))
        # mid-Nov 1929 official anchor: about half the peak
        self.assertLess(p[2], 0.70)
        self.assertGreater(p[2], 0.35)

    def test_lump_sum_2008_trough(self):
        # $10,000 invested at the peak is worth $4,300 at the trough
        self.assertAlmostEqual(M.lump_sum_at_peak(M.CRASH_2008, 10_000, 17),
                               4_300, delta=5)

    def test_replay_preserves_cash(self):
        # parking 36 months at the 1929 assumption: nothing invested before
        # the trough (month 34), so value = principal compounded at 2%/yr
        expected = 10_000 * (1 + 0.02 / 12) ** 34
        v = M.replay_strategy(M.CRASH_1929, 36, 12, 10_000, 34)
        self.assertAlmostEqual(v, expected, delta=10)

    def test_replay_beats_lump_in_both_replays(self):
        for crash in (M.CRASH_1929, M.CRASH_2008):
            md = crash["months_down"]
            h = md + 60
            lump = M.lump_sum_at_peak(crash, 10_000, h)
            for park in (24, 36):
                for phase in (12, 24):
                    self.assertGreater(
                        M.replay_strategy(crash, park, phase, 10_000, h),
                        lump,
                        msg=f"{crash['peak_label']} park{park} phase{phase}")

    def test_phase_uses_all_cash(self):
        # after park+phase no cash is left; value = units x level at horizon
        v, cash_left, units = M.replay_strategy(M.CRASH_2008, 24, 24, 10_000,
                                                74, detail=True)
        self.assertAlmostEqual(cash_left, 0.0, delta=1e-6)
        path = M.equity_index_path(M.CRASH_2008)
        tranche = 10_000 / 24
        # units bought at start of months 24..47; interim bill growth only
        # adds value, never units, so units >= naive sum and cash is zero
        naive_units = sum(tranche / path[24 + i] for i in range(24))
        self.assertGreaterEqual(units, naive_units)
        self.assertAlmostEqual(v, units * path[74], delta=1)


class TestStats(unittest.TestCase):
    def test_erp_stats(self):
        s = M.erp_long_run_stats()
        self.assertEqual(s["first_year"], 1975)
        self.assertEqual(s["last_year"], 2025)
        self.assertGreater(s["price_cagr_pct"], 7.0)
        self.assertGreater(s["mean_total_return_pct"], s["price_cagr_pct"])

    def test_no_crash_cost_positive(self):
        lump, v, cost, r = M.reinvestment_cost_no_crash()
        self.assertGreater(lump, v)
        self.assertEqual(r, 7.0)


class TestTaxMath(unittest.TestCase):
    def test_prop19(self):
        # MV 3.1M, FBV 550k: assessed = FBV + (MV - FBV - allowance)
        a = M.prop19_assessed_after_transfer(550_000, 3_100_000)
        self.assertEqual(a, 3_100_000 - M.STATUTORY["prop19_allowance"])
        # MV below FBV + allowance: FBV stands
        self.assertEqual(M.prop19_assessed_after_transfer(550_000, 1_500_000),
                         550_000)

    def test_transfer_taxes(self):
        self.assertEqual(M.transfer_tax_a(3_100_000), 3_410)
        self.assertEqual(M.transfer_tax_b(1_800_000), 13_500)

    def test_proph(self):
        self.assertEqual(M.proph_year(2026), 0)
        self.assertEqual(M.proph_year(2027), 249)
        self.assertEqual(M.proph_year(2028), 249)
        self.assertAlmostEqual(M.proph_year(2029), 249 * 1.025, places=2)
        self.assertEqual(M.proph_year(2028, sqft=8000), 834.0)
        self.assertGreater(M.proph_total_15yr(), 4000)
        self.assertLess(M.proph_total_15yr(), 5000)

    def test_estate_headroom(self):
        head, taxable, tax = M.estate_headroom(20_000_000)
        self.assertEqual(head, -5_000_000)
        self.assertEqual(taxable, 5_000_000)
        self.assertEqual(tax, 2_000_000)

    def test_break_evens_sane(self):
        for ty in (2040, 2045, 2050):
            rent, det = M.required_rent_break_even(ty)
            self.assertGreater(rent, 0)
            y, _ = M.live_vs_rent_break_even_yield(ty)
            self.assertGreater(y, 0.01)
            self.assertLess(y, 0.15)

    def test_scenarios_multiples_of_ten(self):
        for ty in (2040, 2045, 2050):
            s = M.scenario_paths(ty)
            for key in ("mv_at_transfer", "assessed_after_prop19",
                        "proceeds", "transfer_tax", "brokerage"):
                self.assertEqual(M.m10(s[key]) % 10, 0)


if __name__ == "__main__":
    unittest.main()
