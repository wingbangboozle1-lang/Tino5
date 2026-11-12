"""Decision model for the anonymized estate desk.

Every figure published on the site is produced here from:
  * two published, banded anchors per property (market value; taxable value), and
  * named, published assumptions listed in ASSUMPTIONS.

No supplied assessment/tax history is stored or republished. Money is rounded to $10
only at display time. Rates are shown as percentages.

The arithmetic is deliberately plain so it can be checked by hand:
  taxable value grows at most 2%/yr (Prop 13 cap) until a change of ownership;
  at a Prop 19 family-home transfer the taxable value becomes
      min(taxable, fmv)  when fmv <= taxable + allowance
      taxable + (fmv - (taxable + allowance))  otherwise;
  a non-occupying heir receives no exclusion, so the taxable value becomes full FMV.
"""

from dataclasses import dataclass

# ------------------------------------------------------------------ assumptions
ASSUMPTIONS = {
    "inflation": 0.025,
    "home_growth": 0.040,
    "prop13_cap": 0.020,
    "rent_growth_a": 0.030,
    "rent_growth_b": 0.020,
    "allowance_base": 1_044_586,
    "allowance_growth": 0.020,
    "sell_cost_rate": 0.060,
    "sf_sell_cost_rate": 0.0625,
    "portfolio_return": 0.045,
    "terminal_cg_rate": 0.371,
    "horizon": 25,
    "transfer_year": 2045,
}

BASE = 2026


def r10(x):
    return int(round(x / 10.0) * 10)


def money(x, dash_zero=True):
    if dash_zero and abs(x) < 5:
        return "—"
    sign = "-" if x < 0 else ""
    return f"{sign}${abs(r10(x)):,}"


def pct(x, digits=2):
    return f"{x * 100:.{digits}f}%"


@dataclass(frozen=True)
class Property:
    code: str
    market_value: float
    taxable_value: float
    tax_rate: float
    insurance: float
    water: float
    electric: float
    maintenance: float
    reserve: float
    gross_rent: float = 0.0
    vacancy_rate: float = 0.0
    management_rate: float = 0.0
    homeowners_exemption: float = 0.0
    rent_growth: float = 0.0

    def taxable(self, year):
        return self.taxable_value * (1 + ASSUMPTIONS["prop13_cap"]) ** (year - BASE)

    def tax_on(self, base_value, occupied=False):
        exemption = self.homeowners_exemption if occupied else 0
        return max(base_value - exemption, 0) * self.tax_rate

    def tax(self, year):
        return self.tax_on(self.taxable(year))

    def opex(self, year, rent=None):
        f = (1 + ASSUMPTIONS["inflation"]) ** (year - BASE)
        fixed = (self.insurance + self.water + self.electric + self.maintenance + self.reserve) * f
        if rent is None:
            return fixed
        return fixed + rent * (self.vacancy_rate + self.management_rate)

    def rent(self, year):
        return self.gross_rent * (1 + self.rent_growth) ** (year - BASE)


A = Property(
    code="A",
    market_value=3_100_000,
    taxable_value=550_000,
    tax_rate=0.0125,
    insurance=3_000,
    water=1_500,
    electric=-180,
    maintenance=9_000,
    reserve=3_000,
    gross_rent=66_000,
    vacancy_rate=0.05,
    management_rate=0.08,
    homeowners_exemption=7_000,
    rent_growth=ASSUMPTIONS["rent_growth_a"],
)

B = Property(
    code="B",
    market_value=1_800_000,
    taxable_value=206_000,
    tax_rate=0.0118162182,
    insurance=3_300,
    water=4_380,
    electric=600,
    maintenance=7_000,
    reserve=3_500,
    gross_rent=85_800,
    vacancy_rate=0.05,
    management_rate=0.08,
    homeowners_exemption=0.0,
    rent_growth=ASSUMPTIONS["rent_growth_b"],
)


def prop19_taxable(fmv, taxable, allowance):
    ceiling = taxable + allowance
    if fmv <= ceiling:
        return taxable
    return taxable + (fmv - ceiling)


def value_a(year, growth=None):
    g = ASSUMPTIONS["home_growth"] if growth is None else growth
    return A.market_value * (1 + g) ** (year - BASE)


def value_b(year, growth=None):
    g = ASSUMPTIONS["home_growth"] if growth is None else growth
    return B.market_value * (1 + g) ** (year - BASE)


def transfer_year_view(year=None, home_growth=None, rent_growth=None,
                       allowance_growth=None, transfer_discount=0.0,
                       rent_discount=0.0, insurance_mult=1.0, inflation=None, vacancy=None):
    """Everything that happens in the year the trust distributes Property A."""
    y = ASSUMPTIONS["transfer_year"] if year is None else year
    g = ASSUMPTIONS["home_growth"] if home_growth is None else home_growth
    rg = ASSUMPTIONS["rent_growth_a"] if rent_growth is None else rent_growth
    ag = ASSUMPTIONS["allowance_growth"] if allowance_growth is None else allowance_growth
    n = y - BASE

    fmv = A.market_value * (1 + g) ** n * (1 - transfer_discount)
    taxable = A.taxable_value * (1 + ASSUMPTIONS["prop13_cap"]) ** n
    allowance = ASSUMPTIONS["allowance_base"] * (1 + ag) ** n
    assess_occupy = prop19_taxable(fmv, taxable, allowance)
    assess_rent = fmv                       # no principal-residence use, no exclusion
    tax_occupy = A.tax_on(assess_occupy, occupied=True)
    tax_rent = A.tax_on(assess_rent)

    pi = ASSUMPTIONS["inflation"] if inflation is None else inflation
    inflated = (1 + pi) ** n
    rent = A.gross_rent * (1 + rg) ** n * (1 - rent_discount)
    fixed = (A.insurance * insurance_mult + A.water + A.electric
             + A.maintenance + A.reserve) * inflated
    v = A.vacancy_rate if vacancy is None else vacancy
    var = rent * (v + A.management_rate)
    opex_rent = fixed + var
    opex_occupy = fixed
    net_rent = rent - tax_rent - opex_rent

    proceeds = fmv * (1 - ASSUMPTIONS["sell_cost_rate"])
    return {
        "year": y, "fmv": fmv, "taxable": taxable, "allowance": allowance,
        "assess_occupy": assess_occupy, "assess_rent": assess_rent,
        "tax_occupy": tax_occupy, "tax_rent": tax_rent,
        "rent": rent, "fixed": fixed, "var": var,
        "opex_rent": opex_rent, "opex_occupy": opex_occupy,
        "net_rent": net_rent, "proceeds": proceeds,
        "portfolio_income": proceeds * ASSUMPTIONS["portfolio_return"],
        "cost_occupy_total": tax_occupy + opex_occupy,
    }


def accumulate(first, growth, years):
    return sum(first * (1 + growth) ** i for i in range(years + 1))


def wealth(year=None, horizon=None, home_growth=None, rent_growth=None,
           inflation=None, portfolio=None, insurance_mult=1.0,
           transfer_discount=0.0, rent_discount=0.0, vacancy=None,
           terminal_cg=None, allowance_growth=None):
    """Incremental A-only horizon comparison; B is not sold in any path.
    If occupying A, the owner cannot also live in B. Extra rent from B's
    freed unit is unknown and excluded, so occupancy is NOT housing-adjusted.

    S1 occupy A: own it, pay all costs, no rent, no portfolio.
    S2 rent A:   own it, receive rent, pay landlord costs and the reassessed tax.
    S3 sell A:   pay selling costs, reinvest proceeds at an after-tax return.
    A terminal sale in S1/S2 pays capital-gains tax on net sale proceeds
    exceeding stepped-up basis (before further adjustments),
    because the inherited basis is date-of-death FMV.
    """
    y = ASSUMPTIONS["transfer_year"] if year is None else year
    h = ASSUMPTIONS["horizon"] if horizon is None else horizon
    if h < 1 or int(h) != h:
        raise ValueError("horizon must be a positive integer number of years")
    g = ASSUMPTIONS["home_growth"] if home_growth is None else home_growth
    rg = ASSUMPTIONS["rent_growth_a"] if rent_growth is None else rent_growth
    pi = ASSUMPTIONS["inflation"] if inflation is None else inflation
    pr = ASSUMPTIONS["portfolio_return"] if portfolio is None else portfolio
    cg = ASSUMPTIONS["terminal_cg_rate"] if terminal_cg is None else terminal_cg

    t = transfer_year_view(y, home_growth=g, rent_growth=rg, allowance_growth=allowance_growth,
                           transfer_discount=transfer_discount, rent_discount=rent_discount,
                           insurance_mult=insurance_mult, inflation=pi, vacancy=vacancy)
    fmv = t["fmv"]
    value_end = fmv * (1 + g) ** h
    sale_cost_end = value_end * (1 - ASSUMPTIONS["sell_cost_rate"])
    gain_tax_end = cg * max(sale_cost_end - fmv, 0)
    net_asset_end = sale_cost_end - gain_tax_end

    # Put ALL annual A cash flows on the same terminal-date basis as the
    # invested sale proceeds. An annual cash flow at the start of period i
    # earns the assumed after-tax portfolio return for h-i years. Rental
    # income tax remains unknown, so the rent path is before income tax.
    def future_cashflows(first, growth):
        return sum(first * (1 + growth) ** i * (1 + pr) ** (h - i)
                   for i in range(h))

    cost_s1 = future_cashflows(t["opex_occupy"], pi)
    tax_s1 = future_cashflows(t["tax_occupy"], ASSUMPTIONS["prop13_cap"])
    s1 = net_asset_end - cost_s1 - tax_s1

    rent_s2 = future_cashflows(t["rent"], rg)
    variable_s2 = t["var"] / t["rent"] * rent_s2 if t["rent"] else 0
    opex_s2 = future_cashflows(t["opex_rent"] - t["var"], pi) + variable_s2
    tax_s2 = future_cashflows(t["tax_rent"], ASSUMPTIONS["prop13_cap"])
    s2 = net_asset_end + rent_s2 - opex_s2 - tax_s2

    s3 = t["proceeds"] * (1 + pr) ** h

    return {
        "year": y, "end": y + h, "horizon": h, "fmv": fmv, "value_end": value_end,
        "net_asset_end": net_asset_end, "gain_tax_end": gain_tax_end,
        "s1": s1, "s2": s2, "s3": s3,
        "cost_s1": cost_s1, "tax_s1": tax_s1,
        "rent_s2": rent_s2, "opex_s2": opex_s2, "tax_s2": tax_s2,
        "proceeds": t["proceeds"], "portfolio": s3,
        "delta_rent_vs_sell": s2 - s3, "delta_occupy_vs_sell": s1 - s3,
    }


def break_even_portfolio(year=None, horizon=None):
    """Portfolio return at which selling equals renting (holding both to the horizon)."""
    lo, hi = 0.0, 0.20
    base = wealth(year=year, horizon=horizon)
    target = base["s2"]
    for _ in range(80):
        mid = (lo + hi) / 2
        v = wealth(year=year, horizon=horizon, portfolio=mid)["s3"]
        if v < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def break_even_rent_growth(year=None, horizon=None):
    """Rent growth at which renting equals selling."""
    lo, hi = 0.0, 0.12
    target = wealth(year=year, horizon=horizon)["s3"]
    for _ in range(80):
        mid = (lo + hi) / 2
        v = wealth(year=year, horizon=horizon, rent_growth=mid)["s2"]
        if v < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def estate_threshold(year, growth=0.025):
    return 15_000_000 * (1 + growth) ** (year - 2026)


def property_b_view(year):
    rent = B.rent(year)
    opex = B.opex(year, rent=rent)
    tax = B.tax(year)
    return {"year": year, "value": value_b(year), "taxable": B.taxable(year),
            "tax": tax, "rent": rent, "opex": opex, "noi": rent - tax - opex}


if __name__ == "__main__":
    print("A tax 2026", money(A.tax(2026)), "| B tax 2026", money(B.tax(2026)), "(supplied 2,440)")
    print("B NOI 2026", money(property_b_view(2026)["noi"]))
    for y in (2040, 2045, 2050):
        t = transfer_year_view(y)
        print(y, "fmv", money(t["fmv"]), "taxable", money(t["taxable"]),
              "allow", money(t["allowance"]), "occ", money(t["tax_occupy"]),
              "rent-tax", money(t["tax_rent"]), "rent", money(t["rent"]),
              "net", money(t["net_rent"]), "proceeds", money(t["proceeds"]))
    for y in (2040, 2045, 2050):
        w = wealth(y)
        print(f"{y}->{w['end']}: occupy {money(w['s1'])} | rent {money(w['s2'])} | sell {money(w['s3'])}")
    print("break-even portfolio", pct(break_even_portfolio()))
    print("break-even rent growth", pct(break_even_rent_growth()))
    print("B 2076", property_b_view(2076))
