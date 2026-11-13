#!/usr/bin/env python3
"""Decision model 2026-2076 for Property A (future trust inheritance) and Property B (already owned).

Rules enforced here
-------------------
* Every constant is either VERIFIED (an official source, listed in desk/sources.html)
  or an ASSUMPTION (an explicit, published modelling choice). Nothing is silently invented.
* Every money output is rounded to the nearest $10 (privacy rule).
* No address, name, parcel number or ZIP code appears anywhere.
* The model is deterministic: all inputs are below and every figure is reproducible.

Two accounting decisions that matter, and why
---------------------------------------------
1. Depreciation is computed on the *date-of-death* improvement value and does not grow.
   Depreciation is taken on basis, not on market value.
2. In the sell-and-reinvest path the owner no longer owns Property A at all, so none of
   A's property tax, insurance, utilities or maintenance are charged. The only charge is
   the cost of housing, which is taken from Property B's own ledgers so B nets to zero.
   A comparison that charges property tax in the sell path double-counts.

Run:  python3 scripts/model_v5.py
      python3 scripts/model_v5.py --vanilla    # owner inputs set to civil-service defaults
"""
from __future__ import annotations
import json
from pathlib import Path

OUT = Path("desk/data/model-v5.json")

# ---------------------------------------------------------------------------
# 1. VERIFIED constants (quoted with official links in desk/sources.html)
# ---------------------------------------------------------------------------
V = {
    "estate_exclusion_2026": 15_000_000,      # IRS estate tax page, filing threshold table
    "estate_exclusion_2027": 15_480_000,      # Rev. Proc. 2026-35, s.3.44
    "annual_gift_exclusion_2027": 20_000,     # Rev. Proc. 2026-35, s.3.46
    "estate_top_rate": 0.40,                  # Form 706 Table A, unified rate schedule
    "prop19_cap_addition": 1_044_586,         # BOE LTA 2025/009 (transfers 2/16/25 - 2/15/27)
    "prop19_claim_years": 3,                  # RTC 63.2(f)(1)(A)
    "prop19_homeowner_claim_months": 12,      # RTC 63.2(a)(1)(B)
    "homeowners_exemption": 7_000,            # BOE Homeowners' Exemption
    "prop13_annual_cap": 0.02,                # BOE LTA 2026/002, 2026 factor 1.02
    "sf_secured_rate": 0.0118162182,          # SF Treasurer, FY2026-27
    "sf_transfer_tax_mid": 0.0075,            # SF.gov: $3.75 per $500 on $1M-$5M
    "sc_county_transfer_tax": 0.0011,         # RTC 11911: $0.55 per $500
    "sf_rent_increase_2026": 0.016,           # SF Rent Board, 3/1/26 - 2/28/27
    "ab1482_cap": 0.05,                       # Civil Code 1947.12 (5% + COLA, max 10%)
    "ab1482_sunset": 2030,                    # Civil Code 1947.12(o)
    "cpi_long_run": 0.02,                     # CBO Long-Term Budget Outlook 2025-2055
    "treasury_10y": 0.0510,                   # US Treasury par yields, 12 Nov 2026
    "mortgage_30y": 0.0711,                   # Freddie Mac PMMS, 12 Nov 2026
    "fhfa_us_hpi_aug2026": 444.61,            # FHFA HPI, Jan 1991 = 100
    "fhfa_yoy_aug2026": 0.024,                # FHFA, Aug 2025 - Aug 2026
    "fhfa_peak_2007": 225.0,                  # FHFA HPI, 2007 peak (approx.)
    "fhfa_trough_2011": 178.6,                # FHFA HPI, Feb 2011
    "cdi_homeowners_avg": 2_339.99,           # CDI 2025 data call
    "cdi_dwelling_fire_avg": 1_701.60,        # CDI 2025 data call
    "cdi_cea_avg": 1_440.11,                  # CDI 2025 data call (homeowners EQ)
    "cpi_1998": 163.0,                        # BLS CPI-U annual average
    "cpi_2023": 304.702,                      # BLS CPI-U annual average
    "niit_threshold_single": 200_000,         # IRS Topic 559
    "niit_rate": 0.038,
    "s121_single": 250_000,                   # IRS Topic 701
    "s121_joint": 500_000,
    "sf_small_estate": 208_850,              # Prob. Code 13100 as adjusted under 890 — DE-300, deaths on/after 1 Apr 2025 (base text 166,250)
    "form706_months": 9,                      # Form 706 instructions
    "form706_extension_months": 6,
    "trustee_notice_days": 60,                # Prob. Code 16061.7(f)
    "us_index_growth_1991_2026": None,        # computed below
}
V["us_index_growth_1991_2026"] = round((V["fhfa_us_hpi_aug2026"] / 100.0) ** (1 / 35.6) - 1, 5)

# ---------------------------------------------------------------------------
# 2. OWNER-SUPPLIED inputs. Not independently verifiable; carried as bands, rounded to $10.
# ---------------------------------------------------------------------------
O = {
    "A_value_2026": 3_100_000,        # owner estimate, Nov 2026
    "A_assessed_2026": 550_540,       # owner's 2026 assessed value, nearest $10
    "A_bill_2025": 7_210,             # owner's 2025 bill, nearest $10
    "A_assessed_2025": 539_740,       # owner's 2025 assessed value, nearest $10
    "A_water_month": 130,             # owner: $100-$150
    "A_elec_month": -15,              # owner: solar credit, nets a small profit
    "A_insurance_year": 1_500,        # owner estimate -> below the CDI average, flagged F03
    "B_value_2026": 1_800_000,        # owner estimate, Nov 2026
    "B_assessed_2025": 114_250,       # owner's 2025 assessed value, nearest $10
    "B_bill_2025": 2_440,             # owner's 2025 bill, nearest $10
    "B_rent_two_units_month": 7_150,  # owner-reported combined rent, two units
    "B_water_month": 365,             # owner: $330-$400 for three units
    "B_elec_month": 50,               # owner: $30-$70
    "B_insurance_year": 1_500,        # owner estimate -> flagged F04
}

# A property tax bill has two parts and they behave differently, so they are modelled apart:
#   (a) an ad valorem part, at the county's verified composite secured rate, which tracks the
#       assessed value; and
#   (b) fixed charges (bonds, parcel taxes, direct assessments), which do not track value.
# The ad valorem rate is the verified county rate. The fixed-charge amount is the residual
# between that and the owner's own reported bill, so it is an owner-derived figure.
O["A_advalorem"] = 0.011488          # Santa Clara County FY2025-26 typical composite TRA
O["B_advalorem"] = V["sf_secured_rate"]
O["A_fixed_charges"] = round((O["A_bill_2025"] - O["A_assessed_2025"] * 0.011488) / 10) * 10
O["B_fixed_charges"] = round((O["B_bill_2025"] - O["B_assessed_2025"] * V["sf_secured_rate"]) / 10) * 10
# Reported diagnostics only: the blended charge divided by the assessed value.
O["A_implied_rate"] = round(O["A_bill_2025"] / O["A_assessed_2025"], 6)
O["B_implied_rate"] = round(O["B_bill_2025"] / O["B_assessed_2025"], 6)

# ---------------------------------------------------------------------------
# 3. ASSUMPTIONS (published with ranges and reasoning)
# ---------------------------------------------------------------------------
A = {
    "home_growth": 0.035,       # nominal. Realised CPI was 2.56%/yr 1998-2023; FHFA index
                                # gained 3.52%/yr 1991-2026. 3.5% sits between the two.
    "rent_growth": 0.020,       # constrained by AB 1482 / SF Rent Board; tied to CBO CPI
    "expense_growth": 0.020,    # CBO long-run CPI
    "insurance_growth": 0.040,  # above CPI: California repricing (CDI premium data)
    "fixed_charge_growth": 0.020,  # bonds and parcel taxes roughly track CPI
    "vacancy": 0.04,
    "management": 0.06,
    "maint_pct_A": 0.010,       # of market value per year
    "maint_pct_B": 0.012,
    "land_share": 0.25,         # depreciation only: the land component of basis
    "depr_years": 27.5,
    "selling_cost": 0.06,
    "ordinary_rate": 0.33,      # federal 24% + California 9.3%, combined and rounded up
    "ltcg_rate": 0.243,         # federal 15% + California 9.3%
    "unrecaptured_rate": 0.343, # federal 25% + California 9.3%
    "niit_rate_total": 0.038,
    "s121_exclusion": 250_000,  # single filer
    "invest_pre_tax": 0.051,    # risk-free anchor: 10-year Treasury, 12 Nov 2026
    "invest_tax_drag": 0.33,    # interest taxed at ordinary rates
    "rent_target_month": 5_200, # A rented as one whole-house unit
    "gross_rent_yield_low": 0.018,   # sensitivity band for the rent scenario
    "gross_rent_yield_high": 0.030,
    "transfer_years": [2040, 2045, 2050],
    "end_year": 2076,
}


def r10(x: float) -> int:
    """Round money to the nearest $10 (privacy rule)."""
    return int(round(x / 10.0)) * 10


def growth(base: float, rate: float, years: int) -> float:
    return base * (1.0 + rate) ** years


# ---------------------------------------------------------------------------
# 4. Property A at the transfer year, under Prop 19 as written
# ---------------------------------------------------------------------------
def a_state_at_transfer(year: int, g: float | None = None) -> dict:
    g = A["home_growth"] if g is None else g
    n = year - 2026
    fmv = growth(O["A_value_2026"], g, n)
    assessed = growth(O["A_assessed_2026"], V["prop13_annual_cap"], n)
    cap = assessed + V["prop19_cap_addition"]
    return {"n": n, "fmv": fmv, "assessed": assessed, "cap": cap,
            "excess": max(0.0, fmv - cap)}


def a_taxable_value(year: int, occupy: bool, g: float | None = None) -> float:
    """RTC 63.2(d): factored base-year value plus the excess over the value cap.

    If the home is not the transferee's principal residence the exclusion is unavailable
    (RTC 63.2(a)(1)), the transfer is a change in ownership, and s.110.1 reassesses the
    property at full cash value.
    """
    st = a_state_at_transfer(year, g)
    return st["assessed"] + st["excess"] if occupy else st["fmv"]


def a_property_tax(taxable: float, occupy: bool, year_offset: int = 0) -> float:
    """Ad valorem part on the net taxable value, plus flat fixed charges grown at CPI."""
    exempt = V["homeowners_exemption"] if occupy else 0.0
    flat = O["A_fixed_charges"] * (1 + A["fixed_charge_growth"]) ** year_offset
    return max(0.0, taxable - exempt) * O["A_advalorem"] + flat


# ---------------------------------------------------------------------------
# 5. Property B ledger (already owned; identical across all three paths)
# ---------------------------------------------------------------------------
def b_year(year: int) -> dict:
    n = year - 2026
    per_unit_month = O["B_rent_two_units_month"] / 2
    assessed = growth(O["B_assessed_2025"], V["prop13_annual_cap"], n + 1)
    rent_two = growth(O["B_rent_two_units_month"] * 12, A["rent_growth"], n)
    return {
        "assessed": assessed,
        "property_tax": (assessed * O["B_advalorem"]
                         + O["B_fixed_charges"] * (1 + A["fixed_charge_growth"]) ** (n + 1)),
        "gross_rent_two_units": rent_two,
        # the empty third unit, the owner-occupied house and the A-occupant's housing all
        # carry the same value of shelter in this model
        "shelter_value": growth(per_unit_month * 12, A["rent_growth"], n),
        "water_elec": (growth(O["B_water_month"], A["expense_growth"], n)
                       + growth(O["B_elec_month"], A["expense_growth"], n)) * 12,
        "insurance": growth(O["B_insurance_year"], A["insurance_growth"], n),
        "maintenance": growth(O["B_value_2026"], A["home_growth"], n) * A["maint_pct_B"],
    }


# ---------------------------------------------------------------------------
# 6. The three paths
# ---------------------------------------------------------------------------
def run_path(path: str, transfer: int, rent_month: float | None = None,
             g: float | None = None) -> dict:
    g = A["home_growth"] if g is None else g
    rent_month = A["rent_target_month"] if rent_month is None else rent_month
    occupy = (path == "occupy")
    st = a_state_at_transfer(transfer, g)
    taxable = a_taxable_value(transfer, occupy, g)
    fmv0, basis = st["fmv"], st["fmv"]
    n_years = A["end_year"] - transfer
    improve_dep = fmv0 * (1 - A["land_share"])     # fixed: depreciation uses basis
    annual_dep = improve_dep / A["depr_years"]
    dep_years = int(A["depr_years"])     # 27 full years at one 27.5-year line, then it stops
    rows = []
    after_tax_invest = A["invest_pre_tax"] * (1 - A["invest_tax_drag"])
    portfolio = fmv0 * (1 - A["selling_cost"]) if path == "sell" else 0.0
    suspended_loss = 0.0

    for i in range(n_years):
        yr = transfer + i
        mv = growth(fmv0, g, i)
        tv = growth(taxable, V["prop13_annual_cap"], i)
        tax = a_property_tax(tv, occupy, i) if path != "sell" else 0.0
        ins = growth(O["A_insurance_year"], A["insurance_growth"], i) if path != "sell" else 0.0
        util = 0.0 if path == "sell" else (growth(O["A_water_month"], A["expense_growth"], i)
                                          + growth(O["A_elec_month"], A["expense_growth"], i)) * 12
        maint = mv * A["maint_pct_A"] if path != "sell" else 0.0
        row = {"year": yr, "market_value": mv, "taxable_value": tv, "property_tax": tax,
               "insurance": ins, "utilities": util, "maintenance": maint}

        if path == "rent":
            # depreciation stops when the recovery period is exhausted
            # whole recovery years only: the 0.5 in 27.5 does not buy an extra full year
            dep_this_year = annual_dep if i < int(dep_years) else 0.0
            gross = growth(rent_month * 12, A["rent_growth"], i)
            vac, mgmt = gross * A["vacancy"], gross * A["management"]
            net_pre = gross - vac - mgmt - tax - ins - util - maint
            row.update({"gross_rent": gross, "vacancy": vac, "management": mgmt,
                        "depreciation": dep_this_year})
            # a rental loss is passive: it is suspended, not deducted against other income
            income_tax = max(0.0, net_pre - dep_this_year) * A["ordinary_rate"]
            added = max(0.0, dep_this_year - max(0.0, net_pre))
            suspended_loss += added
            row.update({"income_tax": income_tax, "suspended_loss_added": added,
                        "net_cash_flow": net_pre - income_tax})
            housing_source = "rents elsewhere or lives in Property B's own unit"
        elif path == "occupy":
            # Moving into A vacates the unit the heir currently occupies at Property B,
            # so that unit becomes rentable. It is carried at B's own reported per-unit rent.
            freed = b_year(yr)["shelter_value"]
            row.update({"gross_rent": freed, "income_tax": 0.0,
                        "vacated_b_unit_rent": freed,
                        "net_cash_flow": -(tax + ins + util + maint) + freed})
            housing_source = ("lives in Property A; the unit vacated at Property B is let at "
                              "Property B's own reported per-unit rent")
        else:
            row.update({"gross_rent": 0.0, "income_tax": 0.0, "net_cash_flow": 0.0})
            portfolio = portfolio * (1 + after_tax_invest)
            row["portfolio_value"] = portfolio
            housing_source = "lives in Property B's own unit"
        rows.append(row)

    fmv_end = growth(fmv0, g, n_years)
    out = {
        "path": path, "transfer_year": transfer, "end_year": A["end_year"],
        "years": n_years,
        "transfer_fmv": r10(fmv0), "transfer_assessed": r10(st["assessed"]),
        "prop19_cap": r10(st["cap"]), "prop19_excess": r10(st["excess"]),
        "taxable_at_transfer": r10(taxable),
        "tax_at_transfer": r10(a_property_tax(taxable, occupy)),
        "tax_if_reassessed": r10(a_property_tax(st["fmv"], False)),
        "prop19_saving_year1": r10(a_property_tax(st["fmv"], False)
                                   - a_property_tax(taxable, occupy)),
        "assessed_gap_vs_market": r10(fmv0 - taxable),
        "terminal_market_value": r10(fmv_end),
        "housing_source": housing_source,
        "cumulative_cash_flow": r10(sum(r["net_cash_flow"] for r in rows)),
    }

    if path == "sell":
        out.update({
            "sale_proceeds_net": r10(fmv0 * (1 - A["selling_cost"])),
            "terminal_net_worth": r10(portfolio),
            "note": "Sold at the stepped-up date-of-death basis: realised gain at transfer is "
                    "zero, so no income tax is due on the sale itself.",
        })
    else:
        sold = fmv_end * (1 - A["selling_cost"])
        claimed = sum(r["depreciation"] for r in rows) if path == "rent" else 0.0
        # IRS Topic 425: on disposition of the entire interest, suspended passive losses
        # are fully deductible, so they reduce the gain before the rate is applied.
        gain = sold - basis - claimed - (suspended_loss if path == "rent" else 0.0)
        recapture = min(max(0.0, gain), claimed) if claimed else 0.0
        remaining = max(0.0, gain - recapture)
        excluded = min(remaining, A["s121_exclusion"]) if occupy else 0.0
        taxable_gain = remaining - excluded
        cap_tax = recapture * A["unrecaptured_rate"] + taxable_gain * A["ltcg_rate"]
        niit = taxable_gain * A["niit_rate_total"] if taxable_gain > 0 else 0.0
        pool = 0.0
        for r in rows:
            pool = pool * (1 + after_tax_invest) + r["net_cash_flow"]
        out.update({
            "terminal_sale_price": r10(fmv_end),
            "terminal_selling_costs": r10(fmv_end * A["selling_cost"]),
            "terminal_gain": r10(gain),
            "depreciation_taken": r10(claimed),
            "suspended_passive_loss": r10(suspended_loss),
            "s121_excluded": r10(excluded),
            "terminal_recapture_tax": r10(recapture * A["unrecaptured_rate"]),
            "terminal_capital_gain_tax": r10(cap_tax),
            "terminal_niit": r10(niit),
            "terminal_net_worth": r10(sold - cap_tax - niit + pool),
            "reinvested_cash_flow": r10(pool),
        })
    out["annual_rows"] = rows
    return out


def breakeven(transfer: int) -> dict:
    """The two break-evens that decide the answer.

    rent_growth: the rent at which renting out ties selling and reinvesting.
    home_growth: the appreciation rate at which holding (occupying) ties selling. Both paths are
    re-run at each trial growth rate, because the sell proceeds depend on it too.
    """
    sell = run_path("sell", transfer)["terminal_net_worth"]
    lo, hi = 500.0, 60_000.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if run_path("rent", transfer, rent_month=mid)["terminal_net_worth"] < sell:
            lo = mid
        else:
            hi = mid
    rent_be = (lo + hi) / 2

    lo_g, hi_g = 0.0, 0.15
    for _ in range(60):
        mid = (lo_g + hi_g) / 2
        hold = run_path("occupy", transfer, g=mid)["terminal_net_worth"]
        sell_g = run_path("sell", transfer, g=mid)["terminal_net_worth"]
        if hold < sell_g:
            lo_g = mid
        else:
            hi_g = mid
    return {"transfer_year": transfer,
            "breakeven_monthly_rent": r10(rent_be),
            "breakeven_home_growth": round((lo_g + hi_g) / 2, 5),
            "rent_target": A["rent_target_month"],
            "sell_terminal_net_worth": sell}


# ---------------------------------------------------------------------------
# 7. Black swans. Each anchored to a real, sourced episode.
# ---------------------------------------------------------------------------
SWANS = [
    {"id": "S1", "name": "1970s stagflation replay", "home_growth": 0.045,
     "insurance_growth": 0.090, "rent_growth": 0.060, "occupy_ok": True,
     "anchor": "BLS CPI-U: +13.3% in the 12 months to December 1979, and +13.5% for calendar 1980.",
     "effect": "The 2% assessment cap makes the property tax a shrinking real cost while every "
               "operating line and the discount rate rise. Holding wins on tax and loses on cost."},
    {"id": "S2", "name": "2006-2011 housing bust replay", "home_growth": -0.008,
     "insurance_growth": 0.030, "rent_growth": 0.010, "occupy_ok": True,
     "anchor": "The national purchase-only house price index fell about 21% from its 2007 peak to "
               "February 2011.",
     "effect": "A forced sale at the wrong moment is the largest single risk in the sell path. A "
               "long hold can wait out a trough. A sale cannot."},
    {"id": "S3", "name": "2022-style inflation shock", "home_growth": 0.010,
     "insurance_growth": 0.150, "rent_growth": 0.045, "occupy_ok": True,
     "anchor": "BLS CPI-U: +8.0% for calendar 2022 while the house price index gained only about "
               "2.7%.",
     "effect": "Real house prices fall. Rents rise faster than the statutory cap allows a landlord "
               "to capture, which is the one condition under which renting out is not dominated."},
    {"id": "S4", "name": "High-rate, low-growth decade", "home_growth": 0.015,
     "insurance_growth": 0.040, "rent_growth": 0.015, "occupy_ok": True,
     "anchor": "Ten-year Treasury par yield of 5.10% on 12 November 2026.",
     "effect": "A high risk-free rate raises the bar every illiquid asset must clear, and compresses "
               "house prices through cap-rate repricing."},
    {"id": "S5", "name": "Insurance-market contraction", "home_growth": 0.030,
     "insurance_growth": 0.200, "rent_growth": 0.025, "occupy_ok": True,
     "anchor": "Regulator's 2025 data call: homeowners' premium about $2,340 a policy, plus about "
               "$1,440 of earthquake cover, with dwelling-fire cover at about $1,700.",
     "effect": "Both houses are budgeted at premiums below the statewide average, so a repricing "
               "lands on a line that is already understated."},
    {"id": "S6", "name": "Exclusion claimed, then lost", "home_growth": 0.035,
     "insurance_growth": 0.040, "rent_growth": 0.020, "occupy_ok": True, "lose_exclusion_at": 8,
     "anchor": "RTC s.63.2(a)(1)(B) removes the exclusion on the date the transferee stops being "
               "eligible for the homeowners' exemption, and enrolls a new base-year value from the "
               "following lien date.",
     "effect": "The heir claims the exclusion, then moves out after eight years. The tax reverts "
               "to market value for the remaining term. This is the most expensive mistake that is "
               "entirely within the heir's control."},
    {"id": "S7", "name": "Rented from the outset", "home_growth": 0.035,
     "insurance_growth": 0.040, "rent_growth": 0.020, "occupy_ok": False,
     "anchor": "RTC s.63.2(a)(1): no exclusion is available unless the property becomes the "
               "transferee's principal residence and the claim is filed.",
     "effect": "The house is let instead of occupied, so the exclusion never applies and the "
               "property is reassessed at full cash value from the transfer date."},
]


def _swan_costs(swan: dict, transfer: int) -> dict:
    """Holding cost and terminal value for one stress path, with one defensible convention.

    A renter must pay rent, so the sell path's occupant is charged rent equal to the rent the
    house itself could earn. Without that, the comparison credits the seller with both the
    investment return and free housing.
    """
    g = swan["home_growth"]
    st = a_state_at_transfer(transfer, g)
    n = A["end_year"] - transfer
    off = transfer - 2026
    lose_at = swan.get("lose_exclusion_at")
    occupy_ok = swan.get("occupy_ok", True)
    market_base = a_property_tax(st["fmv"], False, off)
    cash = 0.0
    pool = 0.0
    at = A["invest_pre_tax"] * (1 - A["invest_tax_drag"])
    portfolio = st["fmv"] * (1 - A["selling_cost"])
    tax_series = []
    for i in range(n):
        mv = growth(st["fmv"], g, i)
        if occupy_ok and (lose_at is None or i < lose_at):
            tv = growth(a_taxable_value(transfer, True, g), V["prop13_annual_cap"], i)
            tax = a_property_tax(tv, True, off + i)
        else:
            # RTC 63.2(a)(1)(C): on loss of eligibility the assessor enrols the base-year value
            # "established as of the change in ownership date", adjusted annually since then. It
            # is the transfer-date value, not a later re-derivation, so a house that is occupied
            # and then vacated converges with one that was never occupied.
            tv = growth(st["fmv"], V["prop13_annual_cap"], i)
            tax = a_property_tax(tv, False, off + i)
        tax_series.append(tax)
        ins = growth(O["A_insurance_year"], swan["insurance_growth"], i)
        util = (growth(O["A_water_month"], swan["rent_growth"] * 0.5, i)
                - growth(abs(O["A_elec_month"]), swan["rent_growth"] * 0.5, i)) * 12
        maint = mv * A["maint_pct_A"]
        rent = growth(A["rent_target_month"], swan["rent_growth"], i) * 12
        pool = pool * (1 + at) - (tax + ins + util + maint)
        cash += -(tax + ins + util + maint)
        portfolio = portfolio * (1 + at) - rent
    return {"st": st, "n": n, "pool": pool, "cash": cash, "portfolio": portfolio,
            "tax_year1": tax_series[0], "tax_year30": tax_series[min(29, n - 1)],
            "op_year30": (growth(O["A_insurance_year"], swan["insurance_growth"], 30)
                          + (growth(O["A_water_month"], swan["rent_growth"] * 0.5, 30)
                             - growth(abs(O["A_elec_month"]), swan["rent_growth"] * 0.5, 30)) * 12
                          + growth(st["fmv"], g, 30) * A["maint_pct_A"]
                          + tax_series[min(29, n - 1)])}


def run_swan(swan: dict, transfer: int) -> dict:
    c = _swan_costs(swan, transfer)
    st, n = c["st"], c["n"]
    fmv_end = growth(st["fmv"], swan["home_growth"], n)
    hold = fmv_end * (1 - A["selling_cost"]) + c["pool"]
    sell = c["portfolio"]
    return {
        "id": swan["id"], "name": swan["name"], "anchor": swan["anchor"],
        "effect": swan["effect"],
        "home_growth": swan["home_growth"],
        "insurance_growth": swan["insurance_growth"],
        "rent_growth": swan["rent_growth"],
        "transfer_fmv": r10(st["fmv"]),
        "tax_year1": r10(c["tax_year1"]),
        "tax_year30": r10(c["tax_year30"]),
        "tax_year1_if_reassessed": r10(a_property_tax(st["fmv"], False, transfer - 2026)),
        "annual_holding_cost_year30": r10(c["op_year30"]),
        "fmv_at_horizon": r10(fmv_end),
        "sell_now_then_invest": r10(sell),
        "hold_then_sell": r10(hold),
        "verdict": "holding wins" if hold > sell else "selling wins",
        "occupies": bool(swan.get("occupy_ok", True)),
    }


# ---------------------------------------------------------------------------
# 8. Inheritance-threshold headroom, 2026-2076
# ---------------------------------------------------------------------------
def estate_headroom() -> list:
    """Estate-tax exclusion projected forward against a growing gross estate.

    The exclusion has been indexed to inflation since 2026 (P.L. 119-21). It is projected
    here at the CBO long-run CPI, which is a modelling choice, not law: the statute indexes
    the amount, and a future Congress can change both the base and the index.
    """
    out = []
    estate_2026 = O["A_value_2026"] + O["B_value_2026"]
    for yr in (2026, 2027, 2030, 2035, 2040, 2045, 2050, 2060, 2076):
        n = yr - 2026
        excl = (V["estate_exclusion_2026"] if yr == 2026 else V["estate_exclusion_2027"]
                if yr == 2027 else growth(V["estate_exclusion_2027"], V["cpi_long_run"], yr - 2027))
        gross = growth(estate_2026, A["home_growth"], n)
        out.append({"year": yr, "exclusion_projected": r10(excl), "gross_estate_projected": r10(gross),
                    "headroom": r10(excl - gross),
                    "status": "under" if gross < excl else "OVER"})
    return out


def build() -> None:
    out = {
        "as_of": "13 November 2026",
        "verified": V, "owner_inputs": O, "assumptions": A,
        "implied_rates": {"A": O["A_implied_rate"], "B": O["B_implied_rate"]},
        "realised": {
            "cpi_annual_1998_2023": round((V["cpi_2023"] / V["cpi_1998"]) ** (1 / 25) - 1, 5),
            "fhfa_annual_1991_2026": V["us_index_growth_1991_2026"],
        },
        "paths": {}, "breakevens": {}, "swans": [run_swan(s, 2045) for s in SWANS],
        "b_ledger": {str(y): b_year(y) for y in A["transfer_years"]},
        "estate": estate_headroom(),
        "sensitivity": [],
    }
    for t in A["transfer_years"]:
        out["paths"][str(t)] = {}
        for p in ("occupy", "rent", "sell"):
            r = run_path(p, t)
            rows = r.pop("annual_rows")
            out["paths"][str(t)][p] = r
            out.setdefault("annual", {}).setdefault(str(t), {})[p] = [
                {k: (r10(v) if isinstance(v, float) else v) for k, v in row.items() if v is not None}
                for row in rows]
        out["breakevens"][str(t)] = breakeven(t)
    # sensitivity grid on the two assumptions the answer is most sensitive to
    for t in A["transfer_years"]:
        for gg in (0.020, 0.035, 0.050):
            for ii in (0.035, 0.051, 0.065):
                A["home_growth"], A["invest_pre_tax"] = gg, ii
                out["sensitivity"].append({
                    "transfer_year": t, "home_growth": gg, "invest_pre_tax": ii,
                    "occupy": run_path("occupy", t)["terminal_net_worth"],
                    "rent": run_path("rent", t)["terminal_net_worth"],
                    "sell": run_path("sell", t)["terminal_net_worth"],
                })
    A["home_growth"], A["invest_pre_tax"] = 0.035, 0.051
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1) + "\n")
    print(f"wrote {OUT}")
    for t in A["transfer_years"]:
        p = out["paths"][str(t)]
        print(f"  {t}: occupy={p['occupy']['terminal_net_worth']:>12,} "
              f"rent={p['rent']['terminal_net_worth']:>12,} "
              f"sell={p['sell']['terminal_net_worth']:>12,} "
              f"| breakeven rent/mo={out['breakevens'][str(t)]['breakeven_monthly_rent']:,}")
    print("  estate headroom:", [(e["year"], e["status"]) for e in out["estate"]])


if __name__ == "__main__":
    build()
