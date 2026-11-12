"""Regression tests for the generic, household-independent calculation primitives."""
import unittest
import desk_model as model


class GenericModelTests(unittest.TestCase):
    def test_future_value_compounds_scenario_inputs(self):
        self.assertAlmostEqual(model.future_value(100.0, 0.10, 2), 121.0)

    def test_property_tax_arithmetic_is_explicit(self):
        self.assertAlmostEqual(model.annual_property_tax(100_000.0, 0.012), 1_200.0)

    def test_net_rent_subtracts_cost_items(self):
        self.assertAlmostEqual(model.net_rent(12_000.0, 1_000.0, 2_000.0, 1_000.0), 8_000.0)

    def test_invalid_scenario_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            model.future_value(100.0, -1.0, 1)
        with self.assertRaises(ValueError):
            model.annual_property_tax(-1.0, 0.01)
        with self.assertRaises(ValueError):
            model.net_rent(10.0, -1.0, 0.0, 0.0)


if __name__ == "__main__":
    unittest.main()
