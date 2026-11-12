"""Privacy-safe calculation primitives for the public decision desk.

No household inputs or property-specific values belong in this module. Values which
cannot be verified from public official sources remain blank in the published site.
The expressions below are generic model methods, not forecasts or advice.
"""

from __future__ import annotations


def future_value(base: float, annual_rate: float, years: int) -> float:
    """Compound a stated scenario input; callers must label inputs as assumptions."""
    if base < 0 or years < 0 or annual_rate <= -1:
        raise ValueError("base and years must be nonnegative; rate must exceed -100%")
    return base * (1 + annual_rate) ** years


def annual_property_tax(taxable_value: float, effective_rate: float) -> float:
    """Illustrative arithmetic only; use the property's actual tax-rate area bill."""
    if taxable_value < 0 or effective_rate < 0:
        raise ValueError("taxable value and effective rate must be nonnegative")
    return taxable_value * effective_rate


def net_rent(gross_rent: float, vacancy: float, operating_costs: float,
             property_tax: float, management: float = 0.0) -> float:
    """Illustrative annual rental cash flow before income tax and financing."""
    if min(gross_rent, vacancy, operating_costs, property_tax, management) < 0:
        raise ValueError("cash-flow inputs must be nonnegative")
    return gross_rent - vacancy - operating_costs - property_tax - management


if __name__ == "__main__":
    print("Generic formulas only; the public model contains no household-specific inputs.")
