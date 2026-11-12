"""Regression tests for the publicly disclosed A-only model (no private values)."""
import math
import unittest
import desk_model as m


class ModelAccounting(unittest.TestCase):
    def test_homeowner_exemption_only_when_occupied(self):
        t = m.transfer_year_view(2045)
        self.assertAlmostEqual(t['tax_occupy'], (t['assess_occupy'] - 7000) * m.A.tax_rate)
        self.assertAlmostEqual(t['tax_rent'], t['assess_rent'] * m.A.tax_rate)
        self.assertAlmostEqual(t['tax_rent'] - m.A.tax_on(t['assess_rent'], occupied=True), 7000 * m.A.tax_rate)

    def test_one_year_has_one_period_of_cash_flows(self):
        t = m.transfer_year_view(2045)
        w = m.wealth(2045, horizon=1)
        net_terminal = t['fmv'] * 1.04 * .94
        gain_tax = .371 * max(0, net_terminal - t['fmv'])
        self.assertAlmostEqual(w['s1'], net_terminal - gain_tax - (t['tax_occupy'] + t['opex_occupy']) * 1.045)
        self.assertAlmostEqual(w['s2'], net_terminal - gain_tax + t['net_rent'] * 1.045)
        self.assertAlmostEqual(w['s3'], t['proceeds'] * 1.045)

    def test_terminal_sale_expense_reduces_gain(self):
        w = m.wealth(2045)
        self.assertAlmostEqual(w['gain_tax_end'], .371 * max(0, w['value_end'] * .94 - w['fmv']))

    def test_variable_costs_follow_rent_not_inflation(self):
        t = m.transfer_year_view(2045, rent_growth=.10, inflation=.01)
        w = m.wealth(2045, horizon=2, rent_growth=.10, inflation=.01)
        two_rents = t['rent'] * (1.045 ** 2 + 1.10 * 1.045)
        expected = (t['opex_rent'] - t['var']) * (1.045 ** 2 + 1.01 * 1.045) + t['var'] * (1.045 ** 2 + 1.10 * 1.045)
        self.assertAlmostEqual(w['rent_s2'], two_rents)
        self.assertAlmostEqual(w['opex_s2'], expected)

    def test_stress_inflation_changes_transfer_costs(self):
        t = m.transfer_year_view(2045, inflation=.05)
        w = m.wealth(2045, inflation=.05)
        self.assertAlmostEqual(w['opex_s2'],
                               sum((t['opex_rent'] - t['var']) * 1.05 ** i * 1.045 ** (25-i)
                                   for i in range(25)) + t['var'] / t['rent'] * w['rent_s2'])
        self.assertGreater(t['fixed'], m.transfer_year_view(2045)['fixed'])
        self.assertLess(m.wealth(2045, vacancy=.20)['s2'], m.wealth(2045, vacancy=.05)['s2'])

    def test_zero_horizon_rejected(self):
        with self.assertRaises(ValueError):
            m.wealth(horizon=0)


if __name__ == '__main__':
    unittest.main()
