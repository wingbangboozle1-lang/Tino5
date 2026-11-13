"""Deterministic decision model for review-092b.

Rules
-----
1. Every constant is (a) a figure read in an official document during this session
   (see sources.py), (b) arithmetic on such figures, or (c) a named ASSUMPTION with
   an explicit range. Nothing is recalled from memory.
2. Unknown values are None and render as an em dash. They are never filled in.
3. Displayed money is rounded to the nearest $10 (r10). Amounts quoted verbatim as
   statute/agency figures are marked separately and are not rounded.
4. No personal identifiers: Property A (to be inherited) and Property B (already
   owned), county-level jurisdiction only.

Run:  python3 review-092b/_src/engine.py
"""
from __future__ import annotations

import math

from dataclasses import dataclass

# ---------------------------------------------------------------------------
# 1. OFFICIAL CONSTANTS (each used in a table row that cites its source id)
# ---------------------------------------------------------------------------
OFFICIAL = {
    "fed_exclusion_2026": 15_000_000,          # irs-estate-tax, irs-whats-new
    "fed_exclusion_2027": 15_480_000,          # irs-ir-2026-133
    "gift_annual_2026": 19_000,                # irs-ir-2026-133
    "gift_annual_2027": 20_000,                # irs-ir-2026-133
    "irc121_single": 250_000,                  # irs-topic-701
    "irc121_joint": 500_000,                   # irs-topic-701
    "prop13_cap_pct": 2.0,                     # ca-rtc-51, boe-lta-2026-002
    "cpi_factor_2026": 1.02,                   # boe-lta-2026-002
    "homeowners_exemption_value": 7_000,       # boe-homeowners-exemption
    "prop19_allowance_2025_2027": 1_044_586,   # boe-lta-2025-009
    "prop19_allowance_2023_2025": 1_022_600,   # boe-lta-2025-009
    "prop19_claim_years": 3,                   # boe-prop19
    "prop19_occupy_months": 12,                # ca-rtc-63-2 (within one year)
    "scc_typical_tra_rate_pct": 1.1488,        # scc-assessor-booklet
    "sf_secured_rate_pct": 1.18162182,         # sfttc-secured
    "county_transfer_tax_per_500": 0.55,       # ca-rtc-11911
    "ca_top_marginal_pct": 12.30,              # ftb-2026-rates
    "ca_mhst_pct": 1.0,                        # ca-rtc-17043
    "ca_mhst_threshold": 1_000_000,            # ca-rtc-17043
    "sf_rent_cap_pct": 1.6,                    # sf-rent-board-rates
    "ab1482_base_pct": 5.0,                    # ca-civ-1947-12
    "ab1482_max_pct": 10.0,                    # ca-civ-1947-12
    "cbo_pce_2026_pct": 2.7,                   # cbo-outlook-2026
    "cbo_pce_2030_pct": 2.0,                   # cbo-outlook-2026
    "cpi_yoy_2026_09_pct": 3.7,                # bls-cpi-historical
    "tsp_c_1yr_pct": 12.09,                    # tsp-rates
    "tsp_g_1yr_pct": 4.61,                     # tsp-rates
    "fed_funds_2026_09": "3.75–4.00",          # fed-open-market
    "depreciation_years": 27.5,                # irs-p527
    "fed_dep_recapture_pct": 25.0,             # irs-p527 (unrecaptured §1250)
}

# CPI-U all items (1982-84=100), October of each year, from FRED CPIAUCNS.
# 2025-10 is published as "." (unavailable) and is deliberately absent, not filled.
CPI_OCT = {
    1973: 45.6, 1974: 51.1, 1975: 54.9, 1976: 57.9, 1977: 61.6, 1978: 67.1,
    1979: 75.2, 1980: 84.8, 1981: 93.4, 1982: 98.2,
    2005: 199.2, 2006: 201.8, 2007: 208.936, 2008: 216.573, 2009: 216.177,
    2010: 218.711, 2011: 226.421, 2012: 231.317,
    2021: 276.589, 2022: 298.012, 2023: 307.671, 2024: 315.664, 2026: 337.511,
}
CPI_MONTH = {
    (1973, 10): 45.6, (1980, 3): 80.1, (1980, 10): 84.8,
    (2006, 1): 198.3, (2012, 1): 226.665, (2020, 4): 256.389,
    (2021, 1): 261.582, (2022, 1): 281.148, (2022, 6): 296.311,
    (2023, 1): 299.170,
    (2026, 10): 337.511,
}
# FHFA all-transactions HPI, US, 1980Q1=100, from FRED USSTHPI.
HPI = {
    (1979, 4): 98.26, (1980, 1): 100.00, (1982, 3): 106.85, (1990, 4): 166.14,
    (2006, 1): 368.22, (2007, 1): 380.31, (2009, 4): 329.73, (2012, 1): 309.55,
    (2020, 1): 448.64, (2022, 2): 613.46, (2023, 1): 619.69,
    (2026, 1): 712.20, (2026, 2): 719.87,
}

BASE_YEAR = 2026
HORIZONS = (2040, 2045, 2050)
PATH_KEYS = ("P1", "P2", "P3")
PATH_NAMES = {
    "P1": "Occupy A, keep B as it is",
    "P2": "Rent A out, live in B's third unit",
    "P3": "Sell A at the transfer, reinvest, live in B's third unit",
}


def r10(x):
    """Round to the nearest $10, half away from zero (banker's rounding would send $5 to $0)."""
    if x is None:
        return None
    n = int(math.floor(abs(x) / 10.0 + 0.5)) * 10
    return n if x >= 0 else -n


def money(x):
    if x is None:
        return "—"
    v = r10(x)
    return f"−${abs(v):,}" if v < 0 else f"${v:,}"


def pct(x, d=2):
    return "—" if x is None else f"{x:.{d}f}%"


# ---------------------------------------------------------------------------
# 2. ASSUMPTIONS
# ---------------------------------------------------------------------------
@dataclass
class Assumption:
    key: str
    label: str
    value: float | None
    low: float | None
    high: float | None
    basis: str
    group: str


ASSUMPTIONS = [
    # --- market / economic ---
    Assumption("a_growth", "Property A market-value growth, nominal %/yr", 4.0, 2.0, 6.0,
               "Owner's figure is a today's-value estimate, so the forward path is an assumption. "
               "Official history brackets it: FHFA US house-price index rose 4.3%/yr nominal from "
               "1980Q1 to 2026Q1 while CPI-U rose 3.2%/yr, about 1.0%/yr real (computed here from "
               "fred-hpi-us and fred-cpiaucns).", "market"),
    Assumption("b_growth", "Property B market-value growth, nominal %/yr", 4.0, 2.0, 6.0,
               "Same basis as A. B is rent-controlled stock, so no official forward path exists.", "market"),
    Assumption("equity_return", "After-tax reinvestment return, nominal %/yr", 5.0, 3.0, 7.0,
               "Pre-tax market return less tax drag, not a forecast. TSP C Fund earned 12.09% in the "
               "year to 31 Oct 2026 and the G Fund 4.61% (tsp-rates); a constant 50-year rate is an "
               "assumption and is the single most powerful lever in the model.", "market"),
    Assumption("inflation", "CPI inflation used for cost escalation, %/yr", 2.5, 1.5, 4.0,
               "CBO projects PCE inflation of 2.0% from 2030 (cbo-outlook-2026); actual CPI-U was "
               "3.7% y/y in September 2026 (bls-cpi-historical), so the upper half of the range is live.", "market"),
    Assumption("a_gross_yield_pct", "Property A gross rent yield, % of value /yr", 3.2, 2.5, 4.0,
               "Assumption. No official rent for A exists; HUD Fair Market Rents are 40th-percentile "
               "gross rents for voucher purposes (hud-fmr) and are not the rent this house would achieve.", "market"),
    Assumption("vacancy_pct", "Vacancy and credit loss, % of gross rent", 5.0, 0.0, 10.0,
               "Assumption. Rent caps and just-cause rules (ca-civ-1947-12, sf-rent-board-rates) limit "
               "increases, not vacancy.", "market"),
    Assumption("mgmt_pct", "Management fee, % of gross rent", 5.0, 0.0, 10.0,
               "Assumption; self-management would put it at 0%.", "market"),
    Assumption("selling_cost_pct", "Selling cost, % of price", 5.5, 4.5, 7.0,
               "The only official component is the documentary transfer tax, $0.55 per $500 = 0.11% "
               "(ca-rtc-11911). Commission and escrow are negotiated and unpublished: assumption.", "market"),
    Assumption("maintenance_pct", "Maintenance and repair, % of market value /yr", 1.0, 0.5, 2.0,
               "No official schedule exists for one parcel. The owner states A costs less than B; a "
               "single rate is applied to both for that reason, and the whole range is tested.", "market"),
    Assumption("fed_ltcg_pct", "Federal long-term capital-gains rate, %", 20.0, 15.0, 23.8,
               "Statutory top rate is 20% plus the 3.8% net investment income tax; the owner's future "
               "bracket is unknown, so 20% is used and the range spans 15% to 23.8%.", "tax"),
    Assumption("fed_prop19_allowance_growth", "Prop 19 $1,000,000 allowance growth after 2027, %/yr", 3.0, 0.0, 5.0,
               "The allowance is re-indexed every second 16 February to the FHFA California house-price "
               "change (boe-lta-2025-009). The February 2027 figure is not published yet, so later "
               "growth is an assumption.", "tax"),
    Assumption("fed_exclusion_growth", "Federal estate exclusion growth after 2027, %/yr", 2.5, 0.0, 4.0,
               "The exclusion is indexed (irs-estate-tax, irs-ir-2026-133); the indexation rate is an assumption.", "tax"),
    # --- owner-supplied anchors (published only as ranges / rounded) ---
    Assumption("a_fmv_2026", "Property A market value, 2026", 3_100_000, 3_000_000, 3_200_000,
               "Owner-supplied estimate, published rounded to $10,000. No per-parcel official value is used.", "property"),
    Assumption("b_fmv_2026", "Property B market value, 2026", 1_800_000, 1_700_000, 1_900_000,
               "Owner-supplied estimate, published rounded to $10,000.", "property"),
    Assumption("a_taxable_2026", "Property A taxable (factored base year) value, 2026", 550_540, 550_000, 551_000,
               "Owner-supplied 2026 roll figure rounded to the nearest $10. The multi-year history is "
               "NOT published: a rounded series is still a fingerprint on open assessor rolls (Q-01).", "property"),
    Assumption("b_taxable_2026", "Property B taxable value, 2026", 114_250, 113_000, 116_000,
               "Owner-supplied roll figure rounded to the nearest $10; history not published.", "property"),
    Assumption("a_effective_tax_rate", "Property A effective ad valorem rate, %", 1.3353, 1.1488, 1.4000,
               "Derived from the owner's own 2025 bill over the 2025 roll value (7,207 / 539,743). The "
               "county's stated 'typical' tax-rate-area rate is 1.1488% (scc-assessor-booklet); the two "
               "bracket the range.", "property"),
    Assumption("b_rent_mo", "Property B rent from the two leased units, $/month", 7_150, 6_800, 7_500,
               "Owner-supplied, rounded to $10. Not an official figure.", "property"),
    Assumption("b_unit3_rent_mo", "Property B third-unit rent if let instead of occupied, $/month", 3_580, 3_400, 3_750,
               "Assumption: half the two-unit total, i.e. the two leased units' average. No rent for the "
               "third unit was supplied.", "property"),
    Assumption("a_water_mo", "Property A water and sewer, $/month", 130, 100, 150,
               "Owner-supplied range of $100–$150; midpoint used, rounded to $10.", "property"),
    Assumption("a_elec_net_mo", "Property A electricity, net $/month (credit)", -15, -20, -10,
               "Owner states the solar normally yields a credit. CPUC confirms export credits are usually "
               "below the retail rate (cpuc-nem), so a durable credit is not guaranteed; negative = income.", "property"),
    Assumption("b_water_mo", "Property B water and sewer, three units, $/month", 365, 330, 400,
               "Owner-supplied range of $330–$400; midpoint used, rounded to $10.", "property"),
    Assumption("b_elec_mo", "Property B electricity, $/month", 50, 30, 70,
               "Owner-supplied range of $30–$70; midpoint used, rounded to $10.", "property"),
    Assumption("a_insurance_yr", "Property A homeowners insurance, $/yr", None, None, None,
               "BLANK. No official premium table could be read in this session (F-01). The owner's "
               "~$1,500 is a guess and is not published as a fact; the model shows the effect per "
               "$1,000 of premium instead.", "property"),
    Assumption("b_insurance_yr", "Property B landlord insurance, $/yr", None, None, None,
               "BLANK, same reason as A (F-01).", "property"),
]
A = {a.key: a for a in ASSUMPTIONS}


# ---------------------------------------------------------------------------
# 3. PROPERTY TAX MACHINERY
# ---------------------------------------------------------------------------
def grow(base, rate_pct, years):
    return base * (1.0 + rate_pct / 100.0) ** years


def compound_schedule(base, rates):
    """Compound `base` through a year-by-year list of annual percentage rates."""
    v = base
    for r in rates:
        v *= 1.0 + r / 100.0
    return v


def schedule(rate, years, central, episode=None):
    """`rate` for `episode` years (default: the observed episode's length), then `central`."""
    n = years if episode is None else max(1, min(int(episode), years))
    return [float(rate)] * n + [float(central)] * (years - n)


def prop13_taxable(base_2026, year, cap_pct=None):
    """R&TC §51: base year value compounded by the CCPI factor, never above 2% a year."""
    cap_pct = OFFICIAL["prop13_cap_pct"] if cap_pct is None else cap_pct
    return grow(base_2026, cap_pct, year - BASE_YEAR)


def prop19_allowance(year):
    """The adjusted $1,000,000 amount (boe-lta-2025-009); later years are assumption-driven."""
    if year <= 2027:
        return OFFICIAL["prop19_allowance_2025_2027"]
    return grow(OFFICIAL["prop19_allowance_2025_2027"],
                A["fed_prop19_allowance_growth"].value, year - 2027)


def prop19_new_taxable(fmv, fbyv, allowance):
    """R&TC §63.2(d) / art. XIII A §2.1(c).

    At or below (FBYV + allowance) nothing is reassessed and the FBYV carries over.
    Above it, the new taxable value is FBYV + excess, which telescopes to FMV − allowance.
    """
    cap = fbyv + allowance
    if fmv <= cap:
        return fbyv
    return fbyv + (fmv - cap)


def fed_exclusion(year):
    if year <= 2026:
        return OFFICIAL["fed_exclusion_2026"]
    if year == 2027:
        return OFFICIAL["fed_exclusion_2027"]
    return grow(OFFICIAL["fed_exclusion_2027"], A["fed_exclusion_growth"].value, year - 2027)


# ---------------------------------------------------------------------------
# 4. YEAR-BY-YEAR PROJECTION
# ---------------------------------------------------------------------------
@dataclass
class YearRow:
    year: int
    a_fmv: float
    a_taxable_before: float
    a_tax_before: float
    a_maint: float
    a_water: float
    a_elec: float
    a_carry: float           # water + electricity + maintenance, insurance blank
    b_fmv: float
    b_taxable: float
    b_tax: float
    b_rent: float
    b_water: float
    b_elec: float
    b_maint: float
    b_carry: float
    cpi_index: float
    fed_exclusion: float
    prop19_allowance: float


def project(start=BASE_YEAR, end=2076, **over):
    g = dict(
        a_growth=A["a_growth"].value, b_growth=A["b_growth"].value,
        infl=A["inflation"].value, maint=A["maintenance_pct"].value,
    )
    g.update(over)
    rows = []
    for y in range(start, end + 1):
        n = y - BASE_YEAR
        a_fmv = grow(A["a_fmv_2026"].value, g["a_growth"], n)
        b_fmv = grow(A["b_fmv_2026"].value, g["b_growth"], n)
        a_taxable = prop13_taxable(A["a_taxable_2026"].value, y)
        b_taxable = prop13_taxable(A["b_taxable_2026"].value, y)
        infl = grow(1.0, g["infl"], n)
        a_carry = (A["a_water_mo"].value * 12 * infl
                   + A["a_elec_net_mo"].value * 12 * infl
                   + a_fmv * g["maint"] / 100.0)
        b_carry = (A["b_water_mo"].value * 12 * infl
                   + A["b_elec_mo"].value * 12 * infl
                   + b_fmv * g["maint"] / 100.0)
        rows.append(YearRow(
            year=y, a_fmv=a_fmv,
            a_taxable_before=a_taxable,
            a_tax_before=a_taxable * A["a_effective_tax_rate"].value / 100.0,
            a_maint=a_fmv * g["maint"] / 100.0,
            a_water=A["a_water_mo"].value * 12 * infl,
            a_elec=A["a_elec_net_mo"].value * 12 * infl,
            a_carry=a_carry,
            b_fmv=b_fmv, b_taxable=b_taxable,
            b_tax=b_taxable * OFFICIAL["sf_secured_rate_pct"] / 100.0,
            b_rent=A["b_rent_mo"].value * 12 * grow(1.0, OFFICIAL["sf_rent_cap_pct"], n),
            b_water=A["b_water_mo"].value * 12 * infl,
            b_elec=A["b_elec_mo"].value * 12 * infl,
            b_maint=b_fmv * g["maint"] / 100.0,
            b_carry=b_carry,
            cpi_index=grow(CPI_MONTH[(2026, 10)], g["infl"], n),
            fed_exclusion=fed_exclusion(y),
            prop19_allowance=prop19_allowance(y),
        ))
    return rows


def transfer_table(year):
    """The Prop 19 arithmetic at the moment A transfers, for each path."""
    n = year - BASE_YEAR
    fmv = grow(A["a_fmv_2026"].value, A["a_growth"].value, n)
    fbyv = prop13_taxable(A["a_taxable_2026"].value, year)
    allow = prop19_allowance(year)
    cap = fbyv + allow
    rate = A["a_effective_tax_rate"].value / 100.0
    p1_taxable = prop19_new_taxable(fmv, fbyv, allow)
    p2_taxable = fmv
    p1_tax = max(0.0, (p1_taxable - OFFICIAL["homeowners_exemption_value"]) * rate)
    p2_tax = p2_taxable * rate
    xfer = 2 * (fmv / 500.0 * OFFICIAL["county_transfer_tax_per_500"])
    sell_cost = fmv * A["selling_cost_pct"].value / 100.0
    return dict(
        year=year, fmv=fmv, fbyv=fbyv, allowance=allow, cap=cap,
        excess=max(0.0, fmv - cap),
        p1_taxable=p1_taxable, p1_tax=p1_tax,
        p2_taxable=p2_taxable, p2_tax=p2_tax,
        tax_gap=p2_tax - p1_tax,
        transfer_tax=xfer,
        sell_cost=sell_cost,
        net_sale=fmv - sell_cost,
        gain_over_basis=0.0,
        cap_gain_tax_if_sold_at_transfer=0.0,   # §1014 resets basis to FMV (irs-p551)
    )


# ---------------------------------------------------------------------------
# 5. PATH COMPARISON
# ---------------------------------------------------------------------------
def _a_carry(year, infl_factor=None):
    """A's annual non-tax carrying cost at `year` (water, net electricity, maintenance)."""
    n = year - BASE_YEAR
    infl = infl_factor if infl_factor is not None else grow(1.0, A["inflation"].value, n)
    val = grow(A["a_fmv_2026"].value, A["a_growth"].value, n)
    ins = A["a_insurance_yr"].value or 0.0
    return (A["a_water_mo"].value * 12 * infl
            + A["a_elec_net_mo"].value * 12 * infl
            + val * A["maintenance_pct"].value / 100.0
            + ins)


def _b_net(year, own_unit3, infl_factor=None):
    """B's annual net operating income. Identical in every path except the third unit's rent."""
    n = year - BASE_YEAR
    infl = infl_factor if infl_factor is not None else grow(1.0, A["inflation"].value, n)
    loss = (A["vacancy_pct"].value + A["mgmt_pct"].value) / 100.0
    cap = OFFICIAL["sf_rent_cap_pct"]
    gross = A["b_rent_mo"].value * 12 * grow(1.0, cap, n)
    if not own_unit3:
        gross += A["b_unit3_rent_mo"].value * 12 * grow(1.0, cap, n)
    val = grow(A["b_fmv_2026"].value, A["b_growth"].value, n)
    cost = (A["b_water_mo"].value * 12 * infl
            + A["b_elec_mo"].value * 12 * infl
            + val * A["maintenance_pct"].value / 100.0
            + (A["b_insurance_yr"].value or 0.0)
            + prop13_taxable(A["b_taxable_2026"].value, year) * OFFICIAL["sf_secured_rate_pct"] / 100.0)
    return gross * (1 - loss) - cost


def sale_tax(price, basis, lived_in, depreciable_basis=0.0, years_rented=0.0):
    """Income tax on a later sale of A.

    Official rules: basis is the date-of-death FMV (irs-p551); §121 gives $250,000 single /
    $500,000 joint if the home was the main home 2 of the last 5 years (irs-topic-701);
    residential rental is depreciated over 27.5 years (irs-p527) and the unrecaptured
    §1250 gain is taxed at 25%. Rates beyond those are labelled assumptions.
    """
    net = price * (1 - A["selling_cost_pct"].value / 100.0)
    gain = max(0.0, net - basis)
    dep = 0.0
    if years_rented and depreciable_basis:
        dep = min(depreciable_basis / OFFICIAL["depreciation_years"] * years_rented,
                  depreciable_basis * 0.9, gain)
    recapture = dep * OFFICIAL["fed_dep_recapture_pct"] / 100.0
    cap_gain = max(0.0, gain - dep)
    if lived_in:
        cap_gain = max(0.0, cap_gain - OFFICIAL["irc121_single"])
    ca = OFFICIAL["ca_top_marginal_pct"] + (OFFICIAL["ca_mhst_pct"] if cap_gain > OFFICIAL["ca_mhst_threshold"] else 0.0)
    return recapture + cap_gain * A["fed_ltcg_pct"].value / 100.0 + cap_gain * ca / 100.0


def path_wealth(year, years_after=25, growth=None, equity=None, inflation=None):
    """After-tax wealth `years_after` years after the transfer, by path.

    Anything identical across all three paths (B's property tax, insurance, utilities,
    two leased units' rent) cancels out of the comparison and is reported once on the
    projection page. Only the differences are priced here.

    `growth`, `equity` and `inflation` accept either a number (applied every year) or a
    list of annual percentages (a year-by-year path, used by the black-swan stress tests).
    """
    t = transfer_table(year)
    n = years_after

    def as_path(v, default):
        if v is None:
            return [default] * n
        if isinstance(v, (list, tuple)):
            assert len(v) == n, f"path length {len(v)} != {n}"
            return list(v)
        return [float(v)] * n

    eq_path = as_path(equity, A["equity_return"].value)
    gr_path = as_path(growth, A["a_growth"].value)
    infl_path = as_path(inflation, A["inflation"].value)

    # Discount factors to the horizon: factor[k] accumulates a flow received in
    # year (k+1) to the horizon.
    factor = [1.0] * (n + 1)
    for k in range(n - 1, -1, -1):
        factor[k] = factor[k + 1] * (1 + eq_path[k] / 100.0)
    infl_factor = [1.0] * (n + 1)
    for k in range(n - 1, -1, -1):
        infl_factor[k] = infl_factor[k + 1] * (1 + infl_path[k] / 100.0)

    rate = A["a_effective_tax_rate"].value / 100.0
    cap13 = OFFICIAL["prop13_cap_pct"]

    def a_cost(y, k):
        return _a_carry(y, infl_factor=infl_factor[k])

    def b_net(y, k, own_unit3):
        return _b_net(y, own_unit3=own_unit3, infl_factor=infl_factor[k])

    def a_tax_after(start_taxable, y):
        return start_taxable * grow(1.0, cap13, y - year) * rate

    home_at_horizon = compound_schedule(t["fmv"], gr_path)

    # P1 — occupy A; all three B units stay leased
    p1_cash = 0.0
    for k in range(1, n + 1):
        y = year + k
        tax = max(0.0, a_tax_after(t["p1_taxable"], y)
                  - OFFICIAL["homeowners_exemption_value"] * rate)
        p1_cash += (b_net(y, k, False) - tax - a_cost(y, k)) * factor[k]
    p1_home = home_at_horizon
    p1_tax_due = sale_tax(p1_home, t["fmv"], lived_in=True)

    # P2 — rent A out; live in B's third unit
    p2_cash = 0.0
    for k in range(1, n + 1):
        y = year + k
        gross = (grow(A["a_fmv_2026"].value, A["a_growth"].value, y - BASE_YEAR)
                 * A["a_gross_yield_pct"].value / 100.0)
        rent_net = gross * (1 - (A["vacancy_pct"].value + A["mgmt_pct"].value) / 100.0)
        tax = a_tax_after(t["p2_taxable"], y)
        p2_cash += (b_net(y, k, True) + rent_net - tax - a_cost(y, k)) * factor[k]
    p2_home = home_at_horizon
    p2_tax_due = sale_tax(p2_home, t["fmv"], lived_in=False,
                          depreciable_basis=t["fmv"] * 0.6, years_rented=n)

    # P3 — sell at the transfer; reinvest the net proceeds; live in B's third unit
    p3_cash = 0.0
    for k in range(1, n + 1):
        y = year + k
        p3_cash += b_net(y, k, True) * factor[k]
    p3_invest = t["net_sale"] * factor[0]

    return dict(
        transfer=t,
        P1=p1_home - p1_tax_due + p1_cash,
        P2=p2_home - p2_tax_due + p2_cash,
        P3=p3_invest + p3_cash,
        detail={
            "P1": dict(home=p1_home, sale_tax=p1_tax_due, cash=p1_cash, invest=0.0),
            "P2": dict(home=p2_home, sale_tax=p2_tax_due, cash=p2_cash, invest=0.0),
            "P3": dict(home=0.0, sale_tax=0.0, cash=p3_cash, invest=p3_invest),
        },
    )


def break_even_growth(year, years_after=25, lo=0.0, hi=15.0):
    """Annual nominal growth of A at which P1 or P2 overtakes P3 (bisection on the model)."""
    saved = A["a_growth"].value
    try:
        def f(g):
            A["a_growth"].value = g
            w = path_wealth(year, years_after)
            return max(w["P1"], w["P2"]) - w["P3"]
        if f(lo) < 0 and f(hi) < 0:
            return None
        for _ in range(60):
            mid = (lo + hi) / 2
            if f(mid) < 0:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    finally:
        A["a_growth"].value = saved


# ---------------------------------------------------------------------------
# 6. BLACK-SWAN REGIMES — every number computed from an official published series
# ---------------------------------------------------------------------------
def build_regimes():
    out = []

    def add(code, name, cpi_win, cpi_from, cpi_to, hpi_win, hpi_from, hpi_to,
            cpi_label, hpi_label, note, cpi_years=None, hpi_years=None):
        """Each regime carries two windows, because the two legs need not cover the same years.

        `cpi_years`/`hpi_years` are the leg lengths used to annualise; `episode_years` is the
        longer of the two and is what the stress test in regime_outcome() applies.
        """
        cpi_chg = (cpi_to / cpi_from - 1) * 100
        hpi_chg = (hpi_to / hpi_from - 1) * 100
        cpi_yrs = cpi_years if cpi_years else max(cpi_win[1] - cpi_win[0], 1)
        hpi_yrs = hpi_years if hpi_years else max(hpi_win[1] - hpi_win[0], 1)
        real = ((1 + hpi_chg / 100) / (1 + cpi_chg / 100) - 1) * 100
        out.append(dict(
            code=code, name=name,
            window=f"{cpi_label} / {hpi_label}",
            cpi_window=cpi_label,
            hpi_window=hpi_label,
            cpi=cpi_chg, hpi=hpi_chg, real=real,
            cpi_ann=((1 + cpi_chg / 100) ** (1 / cpi_yrs) - 1) * 100,
            hpi_ann=((1 + hpi_chg / 100) ** (1 / hpi_yrs) - 1) * 100,
            episode_years=max(1, int(round(max(cpi_yrs, hpi_yrs)))),
            note=note))

    add("S1", "Stagflation: prices double while the house crawls",
        (1973, 1982), CPI_MONTH[(1973, 10)], CPI_OCT[1982],
        (1979, 1982), HPI[(1979, 4)], HPI[(1982, 3)],
        "Oct 1973–Oct 1982", "1979Q4–1982Q3",
        "CPI spans the whole 1973–1982 decade; the housing leg is 1979Q4–1982Q3 because that is when "
        "nominal house prices stalled, and it is the only housing number in the series with a real fall "
        "while inflation ran double digits.", cpi_years=9.0, hpi_years=2.75)
    add("S2", "Housing bust: six years of falling nominal values",
        (2006, 2012), CPI_MONTH[(2006, 1)], CPI_MONTH[(2012, 1)],
        (2006, 2012), HPI[(2006, 1)], HPI[(2012, 1)],
        "Jan 2006–Jan 2012", "2006Q1–2012Q1",
        "The national index falls 15.9% while the CPI rises 14.3%: about a quarter of the real value is gone "
        "in six years, and it took until 2016 to regain the nominal peak.", cpi_years=6.0, hpi_years=6.0)
    add("S3", "Rate shock: +400 basis points in nine months",
        (2022, 2023), CPI_MONTH[(2022, 1)], CPI_MONTH[(2023, 1)],
        (2022, 2023), HPI[(2022, 2)], HPI[(2023, 1)],
        "Jan 2022–Jan 2023", "2022Q2–2023Q1",
        "The federal funds target went from 0.25–0.50% on 17 March 2022 to 4.25–4.50% on 15 December 2022 "
        "(fed-open-market). Nationally, house prices did not fall — the shock hit affordability, not prices.", cpi_years=1.0, hpi_years=0.75)
    add("S4", "Demand collapse and deflation month",
        (2019, 2020), CPI_MONTH[(2020, 4)], CPI_MONTH[(2021, 1)],
        (2020, 2026), HPI[(2020, 1)], HPI[(2026, 1)],
        "Apr 2020–Jan 2021", "2020Q1–2026Q1",
        "April 2020 CPI was 0.1% below a year earlier (bls-cpi-historical) while the housing index went on "
        "to gain 58.7% in six years. A cash-flow shock and an asset-price shock are different events and "
        "must be modelled separately.", cpi_years=0.75, hpi_years=6.0)
    add("S5", "The live one: a disinflation that has not arrived",
        (2021, 2027), CPI_MONTH[(2021, 1)], CPI_MONTH[(2026, 10)],
        (2020, 2026), HPI[(2020, 1)], HPI[(2026, 2)],
        "Jan 2021–Oct 2026", "2020Q1–2026Q2",
        "CBO's February 2026 baseline had PCE inflation at 2.7% for 2026 and 2.0% from 2030 "
        "(cbo-outlook-2026). CPI-U was 3.7% higher y/y in September 2026 and 3.4% higher in October, and on "
        "17 September 2026 the FOMC raised the target range 25 bp — the first increase after three 2025 "
        "cuts (fed-open-market, bls-cpi-historical).", cpi_years=5.75, hpi_years=6.25)
    return out


def regime_outcome(year, years_after=25, regime=None, equity_real=0.0):
    """Re-run the three-path comparison with one regime's realised rates substituted.

    The episode's own annual rates are applied for as many years as the episode lasted;
    after that the model reverts to its central assumption. Applying a two-year price
    fall across twenty-five years would be an invented forecast, not a stress test.
    """
    if regime is None:
        raise ValueError("regime required")
    growth_path = schedule(regime["hpi_ann"], years_after, A["a_growth"].value,
                           episode=regime["episode_years"])
    inflation_path = schedule(regime["cpi_ann"], years_after, A["inflation"].value,
                              episode=regime["episode_years"])
    # During the episode the portfolio is assumed to earn only the regime's inflation plus
    # `equity_real` (zero by default) — i.e. no real return at all, which is the unkind case
    # for the sell-and-reinvest path. After the episode it reverts to the central assumption.
    equity_path = schedule(equity_real + regime["cpi_ann"], years_after,
                           A["equity_return"].value, episode=regime["episode_years"])
    w = path_wealth(year, years_after, growth=growth_path, equity=equity_path,
                    inflation=inflation_path)
    best = max(PATH_KEYS, key=lambda k: w[k])
    return dict(wealth=w, best=best, growth_path=growth_path, equity_path=equity_path,
                inflation_path=inflation_path)


def break_even_equity(year, years_after=25, regime=None, lo=0.0, hi=20.0):
    """The reinvestment return at which the best non-sale path ties the sale path.

    Above it, selling and reinvesting wins; below it, keeping A wins. The break-even sits
    just above the house's own growth rate, because both paths reinvest their cash flows at
    the same return. Solved by bisection on the scalar reinvestment return.
    """
    if regime is None:
        regime = dict(code="base", hpi_ann=A["a_growth"].value,
                      cpi_ann=A["inflation"].value, episode_years=years_after)

    def gap(eq):
        out = regime_outcome(year, years_after, regime=regime, equity_real=eq - regime["cpi_ann"])
        w = out["wealth"]
        return max(w["P1"], w["P2"]) - w["P3"]

    if gap(lo) < 0:
        return "always"         # selling wins even with a 0% reinvestment return
    if gap(hi) > 0:
        return "never"          # keeping A wins even with a 20% reinvestment return
    for _ in range(60):
        mid = (lo + hi) / 2
        if gap(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


if __name__ == "__main__":
    print(f"{len(ASSUMPTIONS)} assumptions ({sum(1 for a in ASSUMPTIONS if a.value is None)} blank), "
          f"{len(OFFICIAL)} official constants")
    for y in HORIZONS:
        t = transfer_table(y)
        print(f"\n== transfer {y} ==  FMV {money(t['fmv'])}  FBYV {money(t['fbyv'])}  cap {money(t['cap'])}")
        print(f"   occupy taxable {money(t['p1_taxable'])} tax {money(t['p1_tax'])}")
        print(f"   rent   taxable {money(t['p2_taxable'])} tax {money(t['p2_tax'])}")
        print(f"   net sale {money(t['net_sale'])}")
        w = path_wealth(y)
        print(f"   wealth+25: P1 {money(w['P1'])}  P2 {money(w['P2'])}  P3 {money(w['P3'])}")
        print(f"   break-even growth: {break_even_growth(y)}")
    print()
    for r in build_regimes():
        print(f"{r['code']} {r['window']:>22} CPI {r['cpi']:+7.1f}%  HPI {r['hpi']:+7.1f}%  "
              f"real {r['real']:+7.1f}%  episode {r['episode_years']} yr")
    print("\nregime stress at a 2045 transfer (equity = 2.5% real + regime CPI):")
    for r in build_regimes():
        out = regime_outcome(2045, regime=r)
        w = out["wealth"]
        be = break_even_equity(2045, regime=r)
        print(f"  {r['code']}  P1 {money(w['P1']):>14}  P2 {money(w['P2']):>14}  "
              f"P3 {money(w['P3']):>14}  best {out['best']}  "
              f"sale wins below {pct(be, 2) if isinstance(be, float) else be}")
