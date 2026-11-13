"""Transparent decision model for the Property A (future trust inheritance) and
Property B (already owned) comparison.

Standard library only. Deterministic. Every money output is rounded to the
nearest $10 (statutory amounts are passed through unrounded and marked as such).

Inputs are of three kinds, and every input carries a tag:
  VERIFIED  - value read from an official source (see sources.py, ID in brackets)
  OWNER     - supplied by the owner; NOT verified against an official source
  ASSUMED   - modelling assumption; no official source; replace with quotes/appraisals
Nothing here is a forecast. The output is a set of consistent comparisons under
stated assumptions.
"""
from __future__ import annotations

import math

START_YEAR = 2026
END_YEAR = 2060
DECISION_YEARS = (2040, 2045, 2050)
HORIZON_YEARS = 10  # years after transfer over which each option is compared


def r10(x: float) -> int:
    """Round to nearest $10 (half-up for positives, half-away for negatives)."""
    if x >= 0:
        return int(math.floor(x / 10 + 0.5) * 10)
    return -int(math.floor(-x / 10 + 0.5) * 10)


def pct(x: float) -> str:
    return f"{x * 100:.2f}%"


# ---------------------------------------------------------------- constants
# VERIFIED constants
PROP13_FACTOR = 1.02            # [S04] BOE LTA 2026/002, 2026-27 factor (2% cap)
PROP19_ALLOW_2025 = 1_044_586   # [S03] BOE LTA 2025/009, transfers 16 Feb 2025 - 15 Feb 2027
FED_EXCL_2026 = 15_000_000      # [S01] IRS What's new, 2026 basic exclusion amount
FED_EXCL_2027 = 15_480_000      # [S02] IRS IR-2026-133 / Rev. Proc. 2026-35 (as reported; primary page not re-fetched)
SF_SECURED_RATE = 0.0118162182  # [S12] SF Treasurer, FY2026-27 secured rate
CBO_CPI_2026 = 0.028            # [S11] CBO Feb 2026, CPI-U 2.8% in 2026
CBO_CPI_LONG = 0.023            # [S11] CBO: CPI-U back to 2.3% from 2028
CBO_10Y_2026 = 0.041            # [S11] CBO 10-yr Treasury 4.1% (2026)
CBO_10Y_2027 = 0.043            # [S11] CBO 10-yr Treasury 4.3% (2027)
HUD_FMR_3BR_2026 = 3944         # [S16] HUD FY2026 FMR, Santa Clara County metro area, 3-bedroom (secondary transcription)
FED_LTCG_TOP = 0.15             # [S17] IRS Topic 409: 15% most taxpayers; 20% above ceiling (ASSUMED 15% here)
NIIT = 0.038                    # [S17] IRS Topic 559: 3.8% above MAGI threshold (ASSUMED applies)
UNRECAP_1250 = 0.25             # [S17] IRS Topic 409: 25% maximum on unrecaptured section 1250 gain
SECTION121_SINGLE = 250_000     # [S17] IRS Topic 701 (single filer)

# OWNER-supplied (not verified against an official source) - loaded from local file
# Owner-supplied inputs are kept in owner_inputs.local.json (git-ignored, never committed).
import json as _json
import os as _os
_OWN_PATH = _os.path.join(_os.path.dirname(__file__), "owner_inputs.local.json")
with open(_OWN_PATH, encoding="utf-8") as _fh:
    _OWN = _json.load(_fh)
globals().update({k: v for k, v in _OWN.items()})


# ASSUMED (no official source; replace with quotes/appraisal/advice)
A_EFF_TAX_RATE = 0.0134          # owner's 2025 bill / assessed value (1.34%); sensitivity 1.18%-1.30%
A_TAX_RATE_ALT = 0.0118          # secondary composite for the Property A area, unverified
A_INS_GROWTH = 0.04
A_WATER_GROWTH = 0.04
A_MAINT_PCT = 0.005              # maintenance as share of market value per year
A_ELEC_NET = 0                   # owner says usually zero net cost; no credit counted
A_RENT_2026 = 3_940              # HUD FMR 3BR rounded to $10, used as the rent proxy
A_RENT_GROWTH = 0.03
A_VACANCY = 0.05
A_MGMT = 0.08
A_LANDLORD_INS_MULT = 1.25       # landlord policy vs homeowners premium
A_SELL_COST = 0.06
A_ORDINARY_RATE = 0.333          # 24% federal + 9.3% California (ASSUMED marginal)
A_CA_CG_RATE = 0.093             # California taxes gains as ordinary income (ASSUMED marginal)
A_BUILDING_SHARE = 0.75          # building share of value for depreciation (ASSUMED)
A_LIVE_AVOIDED_RENT = True       # True: owner would otherwise pay rent; False: housing already covered
REINVEST = {                     # after-tax annual return on reinvested money (ASSUMED, anchored to CBO rates)
    "Treasuries": 0.032,         # ~4.2% pre-tax x (1 - 24% federal); CA exempts Treasury interest
    "Balanced": 0.040,
    "Equities": 0.050,           # 6.0% pre-tax less ~1% tax drag
}
ALLOW_GROWTH = 0.011             # derived: BOE adjusted $1M twice (+2.26% then +2.15%), about 1.1% a year
MAX_CASE = "base"

# Appreciation scenarios for Property A market value (nominal, ASSUMED)
GROWTH = {"low": 0.010, "base": 0.035, "high": 0.050}


def allowance(year: int) -> int:
    """Prop 19 value-limit add-on for a transfer in `year` (approximate after Feb 2027)."""
    if year <= 2027:
        return PROP19_ALLOW_2025
    return r10(PROP19_ALLOW_2025 * (1 + ALLOW_GROWTH) ** (year - 2027))


def growth_path(case: str, years=range(START_YEAR, END_YEAR + 1)):
    g = GROWTH[case]
    return {y: g for y in years}


def fmv_path(case: str, years=range(START_YEAR, END_YEAR + 1), growth=None):
    g = growth if growth is not None else GROWTH[case]
    out = {}
    v = OWN_A_FMV_2026
    for y in years:
        if y == START_YEAR:
            out[y] = v
        else:
            v = v * (1 + g)
            out[y] = v
    return out


def prop13_path(years=range(START_YEAR, END_YEAR + 1)):
    """Parent-held assessed value under Prop 13 with no transfer (2% cap)."""
    out, v = {}, OWN_A_ASSESSED_2026
    for y in years:
        if y == START_YEAR:
            out[y] = v
        else:
            v = v * PROP13_FACTOR
            out[y] = v
    return out


def transfer_taxable(year: int, fmv_at_transfer: float, occupied: bool) -> float:
    """Taxable (assessed) value at transfer, before the post-transfer 2% cap."""
    base = prop13_path()[year]  # factored base year value of the parent's home
    if not occupied:
        return fmv_at_transfer  # no exclusion: full reassessment to market
    allow = allowance(year)
    if fmv_at_transfer <= base + allow:
        return base
    return fmv_at_transfer - allow  # BOE/LA County rule: excess over (base + allow) is added to base


def post_transfer_taxable(t0: float, transfer_year: int, year: int) -> float:
    return t0 * PROP13_FACTOR ** (year - transfer_year)


def property_tax(taxable: float, rate: float = A_EFF_TAX_RATE) -> float:
    return taxable * rate


def costs_year(year: int, transfer_year: int, fmv: float, ins0: float = OWN_A_INS,
               water0: float = (OWN_A_WATER_LOW + OWN_A_WATER_HIGH) / 2 * 12) -> dict:
    n = year - transfer_year
    return {
        "insurance": ins0 * (1 + A_INS_GROWTH) ** n,
        "water": water0 * (1 + A_WATER_GROWTH) ** n,
        "maintenance": fmv * A_MAINT_PCT,
        "electricity": A_ELEC_NET,
    }


def avoided_rent(year: int) -> float:
    return 12 * A_RENT_2026 * (1 + A_RENT_GROWTH) ** (year - START_YEAR)


def gain_tax_on_sale(sale_net: float, basis: float, accum_dep: float, excl: float) -> float:
    """Tax on sale of Property A. Depreciation recapture at 25% federal + CA ordinary.
    Remaining gain at 15% + 3.8% federal + CA ordinary (ASSUMED rates)."""
    gain = max(0.0, sale_net - basis)
    taxable_gain = max(0.0, gain - excl)
    recap = min(accum_dep, taxable_gain)
    other = taxable_gain - recap
    fed_lt = FED_LTCG_TOP + NIIT
    return recap * (UNRECAP_1250 + A_CA_CG_RATE) + other * (fed_lt + A_CA_CG_RATE)


def fv_of_flows(flows: dict, t0: int, t1: int, r: float) -> float:
    """Future value at t1 of cash flows (dict year->amount) reinvested at r."""
    total = 0.0
    for y, cf in flows.items():
        if t0 <= y < t1:
            total += cf * (1 + r) ** (t1 - 1 - y)
    return total


def option_wealth(transfer_year: int, growth_case: str = "base", reinvest: str = "Equities",
                  live_avoided: bool | None = None, growth_override: float | None = None,
                  tax_rate: float | None = None, prop19_repealed: bool = False,
                  fmv_override: dict | None = None, ins_growth: float | None = None,
                  rent_mult: float = 1.0, reinvest_rate: float | None = None) -> dict:
    """Compare three options for one transfer year at horizon transfer_year + HORIZON_YEARS.
    Returns the value of each option in nominal dollars at the horizon (rounded to $10)."""
    if live_avoided is None:
        live_avoided = A_LIVE_AVOIDED_RENT
    rate = tax_rate if tax_rate is not None else A_EFF_TAX_RATE
    g = growth_override if growth_override is not None else GROWTH[growth_case]
    r = reinvest_rate if reinvest_rate is not None else REINVEST[reinvest]
    ins_g = ins_growth if ins_growth is not None else A_INS_GROWTH
    T = transfer_year
    H = T + HORIZON_YEARS
    fmv = fmv_override if fmv_override is not None else fmv_path(growth_case, growth=g)
    fmv_T = fmv[T]
    fmv_H = fmv[H]
    base_T = prop13_path()[T]
    dep_per_year = A_BUILDING_SHARE * fmv_T / 27.5
    basis_T = fmv_T
    def ins_at(y):
        return OWN_A_INS * (1 + ins_g) ** (y - T)
    def water_at(y):
        return (OWN_A_WATER_LOW + OWN_A_WATER_HIGH) / 2 * 12 * (1 + A_WATER_GROWTH) ** (y - T)
    def rent_at(y):
        return 12 * A_RENT_2026 * rent_mult * (1 + A_RENT_GROWTH) ** (y - START_YEAR)
    # ---- Option 1: occupy with Prop 19 claim -------------------------------
    if prop19_repealed:
        taxable_live = fmv_T  # exclusion removed: full reassessment to market at transfer
    else:
        taxable_live = transfer_taxable(T, fmv_T, occupied=True)
    flows_live = {}
    for y in range(T, H):
        taxable_y = post_transfer_taxable(taxable_live, T, y)
        pt = property_tax(taxable_y, rate)
        cost = pt + ins_at(y) + water_at(y) + fmv[y] * A_MAINT_PCT
        flows_live[y] = (rent_at(y) if live_avoided else 0) - cost
    sale_live = fmv_H * (1 - A_SELL_COST)
    tax_live = gain_tax_on_sale(sale_live, basis_T, 0.0, SECTION121_SINGLE)
    wealth_live = fv_of_flows(flows_live, T, H, r) + sale_live - tax_live
    # ---- Option 2: rent out (no exclusion: full reassessment) --------------
    taxable_rent = fmv_T
    flows_rent, accum = {}, 0.0
    for y in range(T, H):
        gross = rent_at(y) * (1 - A_VACANCY)
        mgmt = gross * A_MGMT
        pt = property_tax(post_transfer_taxable(taxable_rent, T, y), rate)
        ins_l = ins_at(y) * A_LANDLORD_INS_MULT
        net_before_tax = gross - mgmt - ins_l - pt - water_at(y) - fmv[y] * A_MAINT_PCT
        dep = dep_per_year
        income_tax = max(0.0, net_before_tax - dep) * A_ORDINARY_RATE  # losses suspended (conservative)
        accum += dep
        flows_rent[y] = net_before_tax - income_tax
    sale_rent = fmv_H * (1 - A_SELL_COST)
    tax_rent = gain_tax_on_sale(sale_rent, basis_T, accum, 0.0)
    wealth_rent = fv_of_flows(flows_rent, T, H, r) + sale_rent - tax_rent
    # ---- Option 3: sell at transfer and reinvest ---------------------------
    proceeds = fmv_T * (1 - A_SELL_COST)
    tax_sell = gain_tax_on_sale(proceeds, basis_T, 0.0, 0.0)  # step-up: basis = date-of-death value
    net_invest = proceeds - tax_sell
    wealth_sell = net_invest * (1 + r) ** HORIZON_YEARS
    return {
        "transfer_year": T, "horizon_year": H, "growth": g, "reinvest": reinvest,
        "reinvest_rate": r, "live_avoided_rent": live_avoided, "tax_rate": rate,
        "rent_mult": rent_mult, "prop19_repealed": prop19_repealed,
        "fmv_transfer": r10(fmv_T), "fmv_horizon": r10(fmv_H),
        "taxable_transfer_live": r10(taxable_live), "taxable_transfer_rent": r10(taxable_rent),
        "tax_year1_live": r10(property_tax(taxable_live, rate)),
        "tax_year1_rent": r10(property_tax(taxable_rent, rate)),
        "live": r10(wealth_live), "rent": r10(wealth_rent), "sell": r10(wealth_sell),
        "sale_tax_live": r10(tax_live), "sale_tax_rent": r10(tax_rent),
        "sell_net_invested": r10(net_invest),
    }


def ranking(row: dict) -> list:
    items = [("Live in Property A", row["live"]), ("Rent out Property A", row["rent"]),
             ("Sell and reinvest", row["sell"])]
    return sorted(items, key=lambda kv: -kv[1])


def projection_table() -> list:
    fb = prop13_path()
    fm = fmv_path("base")
    fmv_low = fmv_path("low")
    fmv_high = fmv_path("high")
    rows = []
    for y in range(START_YEAR, END_YEAR + 1):
        allow = allowance(y)
        taxable_no_transfer = fb[y]
        tx_2045 = transfer_taxable(2045, fmv_path("base")[2045], True)
        tax_no_transfer = property_tax(fb[y])
        base_post_2045 = post_transfer_taxable(tx_2045, 2045, y) if y >= 2045 else None
        rows.append({
            "year": y,
            "fmv_low": r10(fmv_low[y]),
            "fmv_base": r10(fm[y]),
            "fmv_high": r10(fmv_high[y]),
            "prop13_no_transfer": r10(taxable_no_transfer),
            "tax_no_transfer": r10(tax_no_transfer),
            "allowance": allow,
            "taxable_2045_occupy": r10(base_post_2045) if base_post_2045 is not None else None,
            "tax_2045_occupy": r10(property_tax(base_post_2045)) if base_post_2045 is not None else None,
            "reassess_2045_rent": r10(post_transfer_taxable(fm[2045], 2045, y)) if y >= 2045 else None,
            "tax_2045_rent": r10(property_tax(post_transfer_taxable(fm[2045], 2045, y))) if y >= 2045 else None,
        })
    return rows


def b_context() -> dict:
    rent = 12 * OWN_B_RENT_MONTHLY
    water = 12 * (OWN_B_WATER_LOW + OWN_B_WATER_HIGH) / 2
    elec = 12 * (OWN_B_ELEC_LOW + OWN_B_ELEC_HIGH) / 2
    tax_official = OWN_B_ASSESSED_2025 * SF_SECURED_RATE
    noi_before_maint = rent - water - elec - OWN_B_INS - OWN_B_TAX_2025
    return {
        "rent_annual": r10(rent), "water_annual_mid": r10(water), "elec_annual_mid": r10(elec),
        "tax_owner_bill": r10(OWN_B_TAX_2025), "tax_at_official_rate": r10(tax_official),
        "tax_unexplained": r10(OWN_B_TAX_2025 - tax_official),
        "noi_before_maint_and_tax_on_income": r10(noi_before_maint),
    }


def inheritance_thresholds() -> dict:
    out = {"fed_2026": FED_EXCL_2026, "fed_2027": FED_EXCL_2027, "fed_index_rate": CBO_CPI_LONG}
    proj = {}
    for y in (2040, 2045, 2050):
        proj[y] = r10(FED_EXCL_2027 * (1 + CBO_CPI_LONG) ** (y - 2027))
    out["fed_projection_index_2_3"] = proj
    # Japan inheritance tax is out of scope for this analysis (no verified primary read).
    return out


def piecewise_fmv(segments: list) -> dict:
    """segments: list of (start_year, end_year_inclusive, annual_growth). Returns FMV by year."""
    out, v = {START_YEAR: OWN_A_FMV_2026}, OWN_A_FMV_2026
    for y in range(START_YEAR + 1, END_YEAR + 1):
        g = 0.0
        for a, b, gg in segments:
            if a <= y <= b:
                g = gg
        v = v * (1 + g)
        out[y] = v
    return out


def black_swan_scenarios() -> dict:
    """Uneven, path-dependent regimes. Each returns a dict of named inputs for option_wealth."""
    # Illustrative only (no drawdown size verified here): model a
    # ASSUMED path: -5.8% a year 2027-2031 (implied cumulative fall about 26%), then 4.5% a year to 2040.
    bust = piecewise_fmv([(2027, 2031, -0.058), (2032, 2040, 0.045), (2041, 2060, 0.025)])
    # 1970s-type stagflation stress: nominal price growth set at an ASSUMED 3.9% a year (illustrative, not a forecast)
    stag = piecewise_fmv([(2027, 2034, 0.0389), (2035, 2060, 0.02)])
    # Long flat decade then catch-up (Japan-style stagnation shape, no Japanese data used)
    flat = piecewise_fmv([(2027, 2036, 0.0), (2037, 2060, 0.035)])
    # Boom then fall: fast growth 2027-2035, then a drop of -20% in 2036-2038
    boom = piecewise_fmv([(2027, 2035, 0.06), (2036, 2038, -0.077), (2039, 2060, 0.03)])
    return {
        "bust_recovery": {"label": "Bust and recovery (ASSUMED -5.8% a year 2027-2031, then 4.5% a year to 2040)", "fmv": bust, "ins_growth": 0.04, "rent_mult": 1.0, "reinvest_rate": None},
        "stagflation": {"label": "1970s-type stagflation (prices +3.9% a year to 2034, insurance +8%)", "fmv": stag, "ins_growth": 0.08, "rent_mult": 1.0, "reinvest_rate": None},
        "flat_decade": {"label": "Flat decade (no price growth to 2036, then 3.5%)", "fmv": flat, "ins_growth": 0.04, "rent_mult": 1.0, "reinvest_rate": None},
        "boom_bust": {"label": "Boom then bust (ASSUMED +6% a year to 2035, about -21% in 2036-2038)", "fmv": boom, "ins_growth": 0.04, "rent_mult": 1.0, "reinvest_rate": None},
        "rate_shock": {"label": "Rate shock: reinvestment after tax falls to 2.8% (ASSUMED)", "fmv": None, "ins_growth": 0.04, "rent_mult": 1.0, "reinvest_rate": 0.028},
        "prop19_repeal": {"label": "Hypothetical: Prop 19 parent-child exclusion removed (heir reassessed to market at transfer)", "fmv": None, "ins_growth": 0.04, "rent_mult": 1.0, "reinvest_rate": None, "prop19_repealed": True},
    }


def build_all() -> dict:
    results = {}
    for T in DECISION_YEARS:
        results[str(T)] = {}
        for case in ("low", "base", "high"):
            for rk in REINVEST:
                results[str(T)][f"{case}|{rk}"] = option_wealth(T, case, rk)
    sens = {}
    for T in DECISION_YEARS:
        sens[str(T)] = {
            "no_avoided_rent": option_wealth(T, "base", "Equities", live_avoided=False),
            "rent_x1_5": option_wealth(T, "base", "Equities", rent_mult=1.5),
            "tax_1_18": option_wealth(T, "base", "Equities", tax_rate=A_TAX_RATE_ALT),
            "tax_1_30": option_wealth(T, "base", "Equities", tax_rate=0.0130),
            "treasuries_only": option_wealth(T, "base", "Treasuries"),
        }
    swans = {}
    for name, sc in black_swan_scenarios().items():
        swans[name] = {"label": sc["label"]}
        for T in DECISION_YEARS:
            swans[name][str(T)] = option_wealth(
                T, "base", "Equities", fmv_override=(sc["fmv"] or fmv_path("base")),
                ins_growth=sc["ins_growth"], rent_mult=sc["rent_mult"],
                reinvest_rate=sc["reinvest_rate"], prop19_repealed=sc.get("prop19_repealed", False))
    return {
        "projection": projection_table(),
        "decision": results,
        "sensitivity": sens,
        "black_swans": swans,
        "b_context": b_context(),
        "thresholds": inheritance_thresholds(),
        "assumptions": {
            "A_EFF_TAX_RATE": A_EFF_TAX_RATE, "A_TAX_RATE_ALT": A_TAX_RATE_ALT,
            "A_MAINT_PCT": A_MAINT_PCT, "A_RENT_2026": A_RENT_2026, "A_RENT_GROWTH": A_RENT_GROWTH,
            "A_VACANCY": A_VACANCY, "A_MGMT": A_MGMT, "A_LANDLORD_INS_MULT": A_LANDLORD_INS_MULT,
            "A_SELL_COST": A_SELL_COST, "A_ORDINARY_RATE": A_ORDINARY_RATE, "A_CA_CG_RATE": A_CA_CG_RATE,
            "A_BUILDING_SHARE": A_BUILDING_SHARE, "ALLOW_GROWTH": ALLOW_GROWTH,
            "GROWTH": GROWTH, "REINVEST": REINVEST, "A_INS_GROWTH": A_INS_GROWTH,
            "A_WATER_GROWTH": A_WATER_GROWTH,
        },
    }


if __name__ == "__main__":
    import json
    res = build_all()
    for T in DECISION_YEARS:
        for k, v in res["decision"][str(T)].items():
            print(T, k, v["live"], v["rent"], v["sell"], ranking(v)[0][0])
    for name, d in res["black_swans"].items():
        print(name, [(T, d[str(T)]["live"], d[str(T)]["rent"], d[str(T)]["sell"]) for T in DECISION_YEARS])
