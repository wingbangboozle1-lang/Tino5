#!/usr/bin/env python3
"""
Audited 2026-2050 Inheritance & Carrying-Cost Financial Model
Cupertino (ZIP 95014) & San Francisco Outer Sunset 3-Unit (ZIP 94122)

Rules:
- All decision analysis and projection dollar metrics are rounded to the nearest $10.
- Verified statutory constants are separated clearly from flagged model assumptions.
- Zero PII anywhere.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any, List


def r10(val: float) -> int:
    """Round any dollar value to the nearest $10 increment."""
    return int(round(val / 10.0) * 10)


def load_verified() -> Dict[str, Any]:
    root = Path(__file__).resolve().parent.parent
    with open(root / "data" / "laws-verified.json") as f:
        laws = json.load(f)
    with open(root / "data" / "cupertino-verified.json") as f:
        cu = json.load(f)
    with open(root / "data" / "san-francisco-verified.json") as f:
        sf = json.load(f)
    return {"laws": laws, "cu": cu, "sf": sf}


PARAMS = {
    "start_year": 2026,
    "end_year": 2050,
    "inheritance_years_examined": [2040, 2045, 2050],
    "primary_inheritance_year": 2045,
    # Property A: Cupertino (95014)
    "cu_value_2026": 3100000,
    "cu_av_2026": 550540,
    "cu_ad_valorem_rate": 0.011612,        # Verified FY25-26 Santa Clara Tax Rate Book bond components
    "cu_fixed_charges_2026": 960,          # Implied direct charges (2025 tax $7,210 - 539,740*1.1612% = $940 * 1.02)
    "cu_water_2026": 1500,                 # $125/mo midpoint of user $100-$150/mo
    "cu_water_growth": 0.042,              # CPUC SJWC/CalWater multi-year GRC escalation
    "cu_solar_credit_2026_user": -180,     # -$15/mo user baseline (pre-2026 SVCE 2x NSC)
    "cu_electric_2026_audited": 200,       # Net after SVCE cut 2x->1x NSC + PG&E $24.15/mo Base Services Charge ($290/yr - ~$90 export)
    "cu_nem_sunset_year": 2040,            # 20-year NEM 1.0/2.0 legacy expiration window (2037-2043)
    "cu_electric_post_nem_base_2026": 1320,# Equivalent 2026$ annual net bill once transitioned to NBT w/o battery
    "cu_electric_growth": 0.035,           # CPUC SB 695 electric cost growth
    "cu_ins_user_2026": 1500,              # User baseline (Flagged)
    "cu_ins_audited_2026": 4230,           # Model assumption: $1.25M exposure * CDI $3.38/$1k homeowner avg
    "cu_ins_growth": 0.035,
    "cu_maint_2026": 12000,                # Model assumption: ~0.39% of $3.1M (~1.0% of structure)
    "cu_maint_growth": 0.023,              # CBO CPI-U
    "cu_imputed_rent_2026": 86400,         # Model assumption (Flagged): $7,200/mo (~2.79% gross yield on $3.1M)
    "cu_selling_cost_rate": 0.0511,        # ~5.0% brokerage/closing + 0.11% Santa Clara DTT (no city tax)

    # Property B: San Francisco (94122) 3-Unit
    "sf_value_2026": 1800000,
    "sf_av_2025": 114250,                  # 2026 missing in user input; 2026 = 114250 * 1.02 = 116530
    "sf_ad_valorem_rate": 0.0118162182,    # Verified FY 2026-27 SF Secured Rate (sftreasurer.org)
    "sf_fixed_charges_2026": 1110,         # Implied direct parcel taxes (2025 $2,440 - 114,250*1.18268% = $1,090 * 1.023)
    "sf_rent_2units_2026": 85800,          # $7,150/mo * 12 (user input)
    "sf_rent_unit3_2026": 42900,           # Assumed equal market rent ($3,575/mo) if 3rd unit rented (Flagged)
    "sf_vacancy_rate": 0.04,               # 4% turnover/vacancy reserve
    "sf_rent_board_fee_2026": 180,         # $59/unit * 3 = $177 rounded
    "sf_water_2026": 4380,                 # $365/mo midpoint of user $330-$400/mo
    "sf_water_growth_pre2036": 0.075,      # SFPUC FY27-36 10-Yr Plan (+6.4% water, +10.1% wastewater)
    "sf_water_growth_post2036": 0.035,
    "sf_electric_2026": 600,               # $50/mo midpoint of user $30-$70/mo
    "sf_electric_growth": 0.035,
    "sf_ins_user_2026": 1500,              # User baseline (Flagged)
    "sf_ins_audited_2026": 4800,           # Model assumption: $1.3M structure * CDI dwelling rate + 32.8% rental surge + liability
    "sf_ins_growth": 0.038,
    "sf_maint_2026": 16500,                # Model assumption: $5,500/unit/yr for older coastal 3-unit (~0.92% of value)
    "sf_maint_growth": 0.023,

    # Macro & Statutory
    "prop13_cap": 0.02,                    # Verified Cal. Const. Art XIII A Sec. 2(b)
    "prop19_addon_2026": 1044586,          # Verified BOE LTA 2025/009 (Feb 16, 2025 - Feb 15, 2027)
    "prop19_addon_growth": 0.041,          # Long-run FHFA CA HPI (~4.13%/yr since 1991Q1)
    "homeowners_exemption_av": 7000,       # Verified R&TC Sec. 218
    "fed_estate_excl_2026": 15000000,      # Verified IRS Rev. Proc. 2025-32
    "fed_estate_excl_2027": 15480000,      # Verified IRS Rev. Proc. 2026-35
    "fed_estate_rate": 0.40,               # Verified Form 706 Table A
    "cpi_long_term": 0.023,                # Verified CBO 2025-2055 CPI-U

    "scenarios": {
        "base": {
            "label": "Base Case (FHFA/CBO Historical Blend — 7.0% Balanced Reinvestment)",
            "cu_appreciation": 0.045,
            "sf_appreciation": 0.040,
            "reinvest_return": 0.070,
            "reinvest_yield_tax_drag": 0.0085,
            "sf_rent_growth": 0.020,
            "use_audited_costs": True
        },
        "conservative": {
            "label": "Conservative Case (3.0%/2.5% RE Growth, 4.5% Treasury-Weighted Reinvestment)",
            "cu_appreciation": 0.030,
            "sf_appreciation": 0.025,
            "reinvest_return": 0.045,
            "reinvest_yield_tax_drag": 0.0090,
            "sf_rent_growth": 0.016,
            "use_audited_costs": True
        },
        "growth": {
            "label": "High Growth Case (5.2%/4.7% RE Growth, 9.0% Equity-Tilted Reinvestment)",
            "cu_appreciation": 0.052,
            "sf_appreciation": 0.047,
            "reinvest_return": 0.090,
            "reinvest_yield_tax_drag": 0.0105,
            "sf_rent_growth": 0.024,
            "use_audited_costs": True
        },
        "user_naive": {
            "label": "Unadjusted User Baseline ($1,500 Ins. & Pre-2026 Solar Credit)",
            "cu_appreciation": 0.045,
            "sf_appreciation": 0.040,
            "reinvest_return": 0.070,
            "reinvest_yield_tax_drag": 0.0085,
            "sf_rent_growth": 0.020,
            "use_audited_costs": False
        }
    }
}


def sf_transfer_tax(sale_price: float) -> float:
    """Verified SF Article 12-C tiered transfer tax (applies to ENTIRE price)."""
    units_500 = sale_price / 500.0
    if sale_price <= 250000:
        rate = 2.50
    elif sale_price < 1000000:
        rate = 3.40
    elif sale_price < 5000000:
        rate = 3.75      # 0.75%
    elif sale_price < 10000000:
        rate = 11.25     # 2.25%
    elif sale_price < 25000000:
        rate = 27.50     # 5.50%
    else:
        rate = 30.00     # 6.00%
    return units_500 * rate


def prop19_new_av(fbyv: float, fmv: float, addon_cap: float) -> float:
    excluded = fbyv + addon_cap
    excess = max(0.0, fmv - excluded)
    return fbyv + excess


def project_yearly(scenario_key: str) -> List[Dict[str, Any]]:
    sc = PARAMS["scenarios"][scenario_key]
    rows: List[Dict[str, Any]] = []
    use_aud = sc["use_audited_costs"]

    cu_val = float(PARAMS["cu_value_2026"])
    sf_val = float(PARAMS["sf_value_2026"])
    cu_av = float(PARAMS["cu_av_2026"])
    sf_av = PARAMS["sf_av_2025"] * (1.0 + PARAMS["prop13_cap"])

    prop19_addon = float(PARAMS["prop19_addon_2026"])
    fed_excl = float(PARAMS["fed_estate_excl_2026"])

    cu_water = float(PARAMS["cu_water_2026"])
    cu_fixed_tax = float(PARAMS["cu_fixed_charges_2026"])
    cu_ins = float(PARAMS["cu_ins_audited_2026"] if use_aud else PARAMS["cu_ins_user_2026"])
    cu_maint = float(PARAMS["cu_maint_2026"])
    cu_imputed_rent = float(PARAMS["cu_imputed_rent_2026"])

    sf_water = float(PARAMS["sf_water_2026"])
    sf_elec = float(PARAMS["sf_electric_2026"])
    sf_fixed_tax = float(PARAMS["sf_fixed_charges_2026"])
    sf_ins = float(PARAMS["sf_ins_audited_2026"] if use_aud else PARAMS["sf_ins_user_2026"])
    sf_maint = float(PARAMS["sf_maint_2026"])
    sf_rent_2u = float(PARAMS["sf_rent_2units_2026"])
    sf_rent_u3 = float(PARAMS["sf_rent_unit3_2026"])
    sf_rb_fee = float(PARAMS["sf_rent_board_fee_2026"])

    for yr in range(PARAMS["start_year"], PARAMS["end_year"] + 1):
        t = yr - 2026
        if yr == 2027:
            fed_excl = float(PARAMS["fed_estate_excl_2027"])
        elif yr > 2027:
            fed_excl *= (1.0 + PARAMS["cpi_long_term"])

        if yr > 2026:
            cu_val *= (1.0 + sc["cu_appreciation"])
            sf_val *= (1.0 + sc["sf_appreciation"])
            cu_av *= (1.0 + PARAMS["prop13_cap"])
            sf_av *= (1.0 + PARAMS["prop13_cap"])
            if (yr - 2025) % 2 == 0:
                prop19_addon *= (1.0 + PARAMS["prop19_addon_growth"]) ** 2

            cu_water *= (1.0 + PARAMS["cu_water_growth"])
            cu_fixed_tax *= (1.0 + PARAMS["cpi_long_term"])
            cu_ins *= (1.0 + PARAMS["cu_ins_growth"])
            cu_maint *= (1.0 + PARAMS["cu_maint_growth"])
            cu_imputed_rent *= (1.0 + PARAMS["cpi_long_term"])

            sf_w_g = PARAMS["sf_water_growth_pre2036"] if yr <= 2036 else PARAMS["sf_water_growth_post2036"]
            sf_water *= (1.0 + sf_w_g)
            sf_elec *= (1.0 + PARAMS["sf_electric_growth"])
            sf_fixed_tax *= (1.0 + PARAMS["cpi_long_term"])
            sf_ins *= (1.0 + PARAMS["sf_ins_growth"])
            sf_maint *= (1.0 + PARAMS["sf_maint_growth"])
            sf_rent_2u *= (1.0 + sc["sf_rent_growth"])
            sf_rent_u3 *= (1.0 + sc["sf_rent_growth"])
            sf_rb_fee *= (1.0 + PARAMS["cpi_long_term"])

        if not use_aud:
            cu_elec = PARAMS["cu_solar_credit_2026_user"] * ((1.0 + PARAMS["cpi_long_term"]) ** t)
        else:
            if yr < PARAMS["cu_nem_sunset_year"]:
                cu_elec = PARAMS["cu_electric_2026_audited"] * ((1.0 + PARAMS["cu_electric_growth"]) ** t)
            else:
                cu_elec = PARAMS["cu_electric_post_nem_base_2026"] * ((1.0 + PARAMS["cu_electric_growth"]) ** t)

        cu_tax_parent = max(0.0, cu_av - PARAMS["homeowners_exemption_av"]) * PARAMS["cu_ad_valorem_rate"] + cu_fixed_tax
        sf_tax_parent = sf_av * PARAMS["sf_ad_valorem_rate"] + sf_fixed_tax

        cu_av_p19 = prop19_new_av(cu_av, cu_val, prop19_addon)
        cu_tax_p19 = max(0.0, cu_av_p19 - PARAMS["homeowners_exemption_av"]) * PARAMS["cu_ad_valorem_rate"] + cu_fixed_tax
        cu_tax_full = cu_val * PARAMS["cu_ad_valorem_rate"] + cu_fixed_tax
        cu_p19_annual_saving = cu_tax_full - cu_tax_p19

        sf_tax_full = sf_val * PARAMS["sf_ad_valorem_rate"] + sf_fixed_tax
        sf_1unit_av_p19 = prop19_new_av(sf_av / 3.0, sf_val / 3.0, prop19_addon)
        sf_av_if_u3_p19 = sf_1unit_av_p19 + (2.0 / 3.0) * sf_val
        sf_tax_if_u3_p19 = max(0.0, sf_av_if_u3_p19 - PARAMS["homeowners_exemption_av"]) * PARAMS["sf_ad_valorem_rate"] + sf_fixed_tax

        cu_non_tax_cost = cu_water + cu_elec + cu_ins + cu_maint
        sf_non_tax_cost = sf_water + sf_elec + sf_ins + sf_maint + sf_rb_fee

        sf_gross_2u_eff = sf_rent_2u * (1.0 - PARAMS["sf_vacancy_rate"])
        sf_gross_3u_eff = (sf_rent_2u + sf_rent_u3) * (1.0 - PARAMS["sf_vacancy_rate"])

        sf_noi_parent_2u = sf_gross_2u_eff - (sf_non_tax_cost + sf_tax_parent)
        sf_noi_reassessed_2u = sf_gross_2u_eff - (sf_non_tax_cost + sf_tax_full)
        sf_noi_reassessed_3u = sf_gross_3u_eff - (sf_non_tax_cost + sf_tax_full)

        cu_sell_cost = cu_val * PARAMS["cu_selling_cost_rate"]
        sf_broker_cost = sf_val * 0.05
        sf_tt = sf_transfer_tax(sf_val)
        sf_sell_cost = sf_broker_cost + sf_tt

        rows.append({
            "year": yr,
            "fed_estate_excl_single": r10(fed_excl),
            "fed_estate_excl_married": r10(fed_excl * 2.0),
            "prop19_cap_addon": r10(prop19_addon),
            "cu": {
                "market_value": r10(cu_val),
                "parent_av": r10(cu_av),
                "parent_prop_tax": r10(cu_tax_parent),
                "water": r10(cu_water),
                "electric_solar": r10(cu_elec),
                "insurance": r10(cu_ins),
                "maintenance": r10(cu_maint),
                "non_tax_operating": r10(cu_non_tax_cost),
                "total_cost_parent": r10(cu_non_tax_cost + cu_tax_parent),
                "inherit_av_prop19": r10(cu_av_p19),
                "inherit_tax_prop19": r10(cu_tax_p19),
                "inherit_tax_full_reassess": r10(cu_tax_full),
                "prop19_annual_tax_saving": r10(cu_tax_full) - r10(cu_tax_p19),
                "imputed_gross_rent": r10(cu_imputed_rent),
                "est_selling_costs": r10(cu_sell_cost),
                "net_sale_proceeds_at_death": r10(cu_val - cu_sell_cost)
            },
            "sf": {
                "market_value": r10(sf_val),
                "parent_av": r10(sf_av),
                "parent_prop_tax": r10(sf_tax_parent),
                "water_sewer": r10(sf_water),
                "electric": r10(sf_elec),
                "insurance": r10(sf_ins),
                "maintenance": r10(sf_maint),
                "rent_board_fee": r10(sf_rb_fee),
                "non_tax_operating": r10(sf_non_tax_cost),
                "total_cost_parent": r10(sf_non_tax_cost + sf_tax_parent),
                "gross_rent_2u_eff": r10(sf_gross_2u_eff),
                "gross_rent_3u_eff": r10(sf_gross_3u_eff),
                "net_cashflow_parent_2u": r10(sf_noi_parent_2u),
                "inherit_tax_full_reassess": r10(sf_tax_full),
                "inherit_tax_if_1unit_prop19": r10(sf_tax_if_u3_p19),
                "net_cashflow_reassessed_2u": r10(sf_noi_reassessed_2u),
                "net_cashflow_reassessed_3u": r10(sf_noi_reassessed_3u),
                "sf_transfer_tax": r10(sf_tt),
                "sf_transfer_tax_rate_pct": round((sf_tt / sf_val) * 100.0, 2),
                "est_selling_costs": r10(sf_sell_cost),
                "net_sale_proceeds_at_death": r10(sf_val - sf_sell_cost)
            },
            "combined_real_estate_value": r10(cu_val + sf_val)
        })
    return rows


def evaluate_strategies(scenario_key: str, inherit_year: int = 2045, horizon_years: int = 10) -> Dict[str, Any]:
    sc = PARAMS["scenarios"][scenario_key]
    rows = project_yearly(scenario_key)
    base_row = next(r for r in rows if r["year"] == inherit_year)

    cu_v0 = float(base_row["cu"]["market_value"])
    sf_v0 = float(base_row["sf"]["market_value"])
    cu_av0 = float(base_row["cu"]["parent_av"])
    sf_av0 = float(base_row["sf"]["parent_av"])
    p19_cap0 = float(base_row["prop19_cap_addon"])

    r_cu = sc["cu_appreciation"]
    r_sf = sc["sf_appreciation"]
    r_inv_net = sc["reinvest_return"] - sc["reinvest_yield_tax_drag"]
    r_cpi = PARAMS["cpi_long_term"]
    r_rent_sf = sc["sf_rent_growth"]

    cu_net_sale0 = float(base_row["cu"]["net_sale_proceeds_at_death"])
    sf_net_sale0 = float(base_row["sf"]["net_sale_proceeds_at_death"])

    eff_ordinary_tax = 0.32

    def sim_cu_hold(owner_occupied: bool, prop19_qualified: bool) -> Dict[str, Any]:
        val = cu_v0
        av = prop19_new_av(cu_av0, cu_v0, p19_cap0) if prop19_qualified else cu_v0
        fixed = base_row["cu"]["parent_prop_tax"] - max(0.0, cu_av0 - 7000) * PARAMS["cu_ad_valorem_rate"]
        water = float(base_row["cu"]["water"])
        elec = float(base_row["cu"]["electric_solar"])
        ins = float(base_row["cu"]["insurance"])
        maint = float(base_row["cu"]["maintenance"])
        rent_gross = float(base_row["cu"]["imputed_gross_rent"]) * (1.0 - 0.04)
        dep_annual = (0.45 * cu_v0) / 27.5 if not owner_occupied else 0.0

        cashflows = []
        imputed_consumption = []
        for k in range(horizon_years):
            ptax = max(0.0, av - (7000.0 if owner_occupied else 0.0)) * PARAMS["cu_ad_valorem_rate"] + fixed
            opex = water + elec + ins + maint + ptax
            if owner_occupied:
                cf = -opex
                imputed_consumption.append(rent_gross)
            else:
                landlord_opex = ins + maint + ptax + 0.05 * rent_gross
                taxable = max(0.0, rent_gross - landlord_opex - dep_annual)
                cf = rent_gross - landlord_opex - taxable * eff_ordinary_tax
                imputed_consumption.append(0.0)
            cashflows.append(cf)

            val *= (1.0 + r_cu)
            av *= (1.0 + PARAMS["prop13_cap"])
            fixed *= (1.0 + r_cpi)
            water *= (1.0 + PARAMS["cu_water_growth"])
            elec *= (1.0 + PARAMS["cu_electric_growth"])
            ins *= (1.0 + PARAMS["cu_ins_growth"])
            maint *= (1.0 + PARAMS["cu_maint_growth"])
            rent_gross *= (1.0 + r_cpi)

        end_sell_cost = val * PARAMS["cu_selling_cost_rate"]
        cap_gain = max(0.0, (val - end_sell_cost) - cu_v0)
        cap_gain_excludable = max(0.0, cap_gain - 250000.0) if owner_occupied else cap_gain
        dep_recap_tax = (dep_annual * horizon_years) * 0.25 if not owner_occupied else 0.0
        end_tax = cap_gain_excludable * 0.28 + dep_recap_tax
        return {
            "yr1_cf": cashflows[0],
            "cum_cf": sum(cashflows),
            "cum_imputed_housing": sum(imputed_consumption),
            "end_gross_value": val,
            "end_net_liquidation_value": val - end_sell_cost - end_tax,
            "cashflows": cashflows
        }

    def sim_sf_hold(units_rented: int, owner_in_unit3: bool, unit3_prop19: bool) -> Dict[str, Any]:
        val = sf_v0
        if owner_in_unit3 and unit3_prop19:
            av = prop19_new_av(sf_av0 / 3.0, sf_v0 / 3.0, p19_cap0) + (2.0 / 3.0) * sf_v0
        else:
            av = sf_v0
        fixed = base_row["sf"]["parent_prop_tax"] - sf_av0 * PARAMS["sf_ad_valorem_rate"]
        water = float(base_row["sf"]["water_sewer"])
        elec = float(base_row["sf"]["electric"])
        ins = float(base_row["sf"]["insurance"])
        maint = float(base_row["sf"]["maintenance"])
        rb = float(base_row["sf"]["rent_board_fee"])
        rent_eff = float(base_row["sf"]["gross_rent_2u_eff"] if units_rented == 2 else base_row["sf"]["gross_rent_3u_eff"])
        u3_val = float(base_row["sf"]["gross_rent_3u_eff"] - base_row["sf"]["gross_rent_2u_eff"])
        rental_share = 2.0 / 3.0 if owner_in_unit3 else 1.0
        dep_annual = ((0.60 * sf_v0) * rental_share) / 27.5

        cashflows = []
        imputed_consumption = []
        for k in range(horizon_years):
            yr_k = inherit_year + k
            ptax = max(0.0, av - (7000.0 if owner_in_unit3 else 0.0)) * PARAMS["sf_ad_valorem_rate"] + fixed
            opex = water + elec + ins + maint + rb + ptax
            deductible_opex = opex * rental_share
            taxable = max(0.0, rent_eff - deductible_opex - dep_annual)
            cf = rent_eff - opex - taxable * eff_ordinary_tax
            cashflows.append(cf)
            imputed_consumption.append(u3_val if owner_in_unit3 else 0.0)

            val *= (1.0 + r_sf)
            av *= (1.0 + PARAMS["prop13_cap"])
            fixed *= (1.0 + r_cpi)
            water *= (1.0 + (PARAMS["sf_water_growth_pre2036"] if yr_k < 2036 else PARAMS["sf_water_growth_post2036"]))
            elec *= (1.0 + PARAMS["sf_electric_growth"])
            ins *= (1.0 + PARAMS["sf_ins_growth"])
            maint *= (1.0 + PARAMS["sf_maint_growth"])
            rb *= (1.0 + r_cpi)
            rent_eff *= (1.0 + r_rent_sf)
            u3_val *= (1.0 + r_rent_sf)

        end_sell_cost = val * 0.05 + sf_transfer_tax(val)
        cap_gain = max(0.0, (val - end_sell_cost) - sf_v0)
        if owner_in_unit3:
            taxable_gain = max(0.0, (cap_gain / 3.0) - 250000.0) + cap_gain * (2.0 / 3.0)
        else:
            taxable_gain = cap_gain
        dep_recap_tax = (dep_annual * horizon_years) * 0.25
        end_tax = taxable_gain * 0.28 + dep_recap_tax
        return {
            "yr1_cf": cashflows[0],
            "cum_cf": sum(cashflows),
            "cum_imputed_housing": sum(imputed_consumption),
            "end_gross_value": val,
            "end_net_liquidation_value": val - end_sell_cost - end_tax,
            "cashflows": cashflows
        }

    def sim_portfolio(initial_cash: float, annual_external_cfs: List[float], housing_cost_yr1: float = 0.0) -> Dict[str, Any]:
        bal = initial_cash
        basis = initial_cash
        for k in range(horizon_years):
            h_cost = housing_cost_yr1 * ((1.0 + r_cpi) ** k)
            net_add = annual_external_cfs[k] - h_cost
            bal = bal * (1.0 + r_inv_net) + net_add
            basis += (bal * 0.015) + net_add
        unrealized = max(0.0, bal - basis)
        net_liq = bal - unrealized * 0.26
        return {
            "end_gross_portfolio": bal,
            "end_net_liquidation_value": net_liq,
            "yr1_portfolio_income_net": initial_cash * r_inv_net
        }

    equiv_sf_housing_yr1 = float(base_row["sf"]["gross_rent_3u_eff"] - base_row["sf"]["gross_rent_2u_eff"]) / (1.0 - PARAMS["sf_vacancy_rate"])
    cum_sf_housing_10yr = sum(equiv_sf_housing_yr1 * ((1.0 + r_cpi) ** k) for k in range(horizon_years))

    a_cu = sim_cu_hold(owner_occupied=True, prop19_qualified=True)
    a_sf = sim_sf_hold(units_rented=2, owner_in_unit3=False, unit3_prop19=False)
    a_cfs = [a_cu["cashflows"][k] + a_sf["cashflows"][k] for k in range(horizon_years)]
    a_port = sim_portfolio(0.0, a_cfs, 0.0)

    a3_sf = sim_sf_hold(units_rented=3, owner_in_unit3=False, unit3_prop19=False)
    a3_cfs = [a_cu["cashflows"][k] + a3_sf["cashflows"][k] for k in range(horizon_years)]
    a3_port = sim_portfolio(0.0, a3_cfs, 0.0)

    b_cu = sim_cu_hold(owner_occupied=False, prop19_qualified=False)
    b_sf = sim_sf_hold(units_rented=2, owner_in_unit3=True, unit3_prop19=False)
    b_cfs = [b_cu["cashflows"][k] + b_sf["cashflows"][k] for k in range(horizon_years)]
    b_port = sim_portfolio(0.0, b_cfs, 0.0)

    c_sf = sim_sf_hold(units_rented=2, owner_in_unit3=True, unit3_prop19=False)
    c_port = sim_portfolio(cu_net_sale0, c_sf["cashflows"], 0.0)

    d_cu = sim_cu_hold(owner_occupied=True, prop19_qualified=True)
    d_port = sim_portfolio(sf_net_sale0, d_cu["cashflows"], 0.0)

    e_port = sim_portfolio(cu_net_sale0 + sf_net_sale0, [0.0] * horizon_years, equiv_sf_housing_yr1)

    strategies = [
        {
            "id": "strategy_c",
            "name": "C. Live in SF Unit 3 + Sell Cupertino & Reinvest",
            "housing": "SF Unit 3 (2 units rented)",
            "prop19_shield_captured": False,
            "yr1_net_cash_flow": r10(c_sf["yr1_cf"] + c_port["yr1_portfolio_income_net"]),
            "yr1_property_cash_flow_only": r10(c_sf["yr1_cf"]),
            "yr1_portfolio_return_after_tax": r10(c_port["yr1_portfolio_income_net"]),
            "horizon_end_gross_wealth": r10(c_sf["end_gross_value"] + c_port["end_gross_portfolio"]),
            "horizon_end_after_tax_wealth": r10(c_sf["end_net_liquidation_value"] + c_port["end_net_liquidation_value"]),
            "cum_10yr_housing_value_enjoyed": r10(c_sf["cum_imputed_housing"]),
            "housing_adjusted_10yr_wealth": r10(c_sf["end_net_liquidation_value"] + c_port["end_net_liquidation_value"] + c_sf["cum_imputed_housing"]),
            "notes": "Unlocks ~95% of Cupertino equity tax-free via Sec. 1014, lives in SF Unit 3 while keeping 2-unit rent, diversifies single-city concentration."
        },
        {
            "id": "strategy_d",
            "name": "D. Live in Cupertino (Prop 19) + Sell SF & Reinvest",
            "housing": "Cupertino Single-Family Home",
            "prop19_shield_captured": True,
            "yr1_net_cash_flow": r10(d_cu["yr1_cf"] + d_port["yr1_portfolio_income_net"]),
            "yr1_property_cash_flow_only": r10(d_cu["yr1_cf"]),
            "yr1_portfolio_return_after_tax": r10(d_port["yr1_portfolio_income_net"]),
            "horizon_end_gross_wealth": r10(d_cu["end_gross_value"] + d_port["end_gross_portfolio"]),
            "horizon_end_after_tax_wealth": r10(d_cu["end_net_liquidation_value"] + d_port["end_net_liquidation_value"]),
            "cum_10yr_housing_value_enjoyed": r10(d_cu["cum_imputed_housing"]),
            "housing_adjusted_10yr_wealth": r10(d_cu["end_net_liquidation_value"] + d_port["end_net_liquidation_value"] + d_cu["cum_imputed_housing"]),
            "notes": "Captures Cupertino Prop 19 cap, avoids SF 2.25% transfer-tax cliff & full SF reassessment, turns SF equity into liquid compounding assets."
        },
        {
            "id": "strategy_e",
            "name": "E. Sell Both Tax-Free (Sec. 1014) & Reinvest 100%",
            "housing": "Rent Comparable SF Residence (Cost Deducted)",
            "prop19_shield_captured": False,
            "yr1_net_cash_flow": r10(e_port["yr1_portfolio_income_net"] - equiv_sf_housing_yr1),
            "yr1_property_cash_flow_only": r10(-equiv_sf_housing_yr1),
            "yr1_portfolio_return_after_tax": r10(e_port["yr1_portfolio_income_net"]),
            "horizon_end_gross_wealth": r10(e_port["end_gross_portfolio"]),
            "horizon_end_after_tax_wealth": r10(e_port["end_net_liquidation_value"]),
            "cum_10yr_housing_value_enjoyed": r10(cum_sf_housing_10yr),
            "housing_adjusted_10yr_wealth": r10(e_port["end_net_liquidation_value"] + cum_sf_housing_10yr),
            "notes": "Zero landlord operations, maximum liquidity and diversification, pays market rent out of portfolio yield."
        },
        {
            "id": "strategy_a2",
            "name": "A2. Live in Cupertino (Prop 19) + Keep & Rent All 3 SF Units",
            "housing": "Cupertino Single-Family Home",
            "prop19_shield_captured": True,
            "yr1_net_cash_flow": r10(a3_cfs[0]),
            "yr1_property_cash_flow_only": r10(a3_cfs[0]),
            "yr1_portfolio_return_after_tax": 0,
            "horizon_end_gross_wealth": r10(a_cu["end_gross_value"] + a3_sf["end_gross_value"] + a3_port["end_gross_portfolio"]),
            "horizon_end_after_tax_wealth": r10(a_cu["end_net_liquidation_value"] + a3_sf["end_net_liquidation_value"] + a3_port["end_net_liquidation_value"]),
            "cum_10yr_housing_value_enjoyed": r10(a_cu["cum_imputed_housing"]),
            "housing_adjusted_10yr_wealth": r10(a_cu["end_net_liquidation_value"] + a3_sf["end_net_liquidation_value"] + a3_port["end_net_liquidation_value"] + a_cu["cum_imputed_housing"]),
            "notes": "Keeps both homes in family, preserves Cupertino Prop 19, rents Unit 3 to absorb SF reassessment + SFPUC hikes."
        },
        {
            "id": "strategy_b",
            "name": "B. Live in SF Unit 3 + Rent Out Cupertino (Forfeits Prop 19)",
            "housing": "SF Unit 3 (2 units rented)",
            "prop19_shield_captured": False,
            "yr1_net_cash_flow": r10(b_cfs[0]),
            "yr1_property_cash_flow_only": r10(b_cfs[0]),
            "yr1_portfolio_return_after_tax": 0,
            "horizon_end_gross_wealth": r10(b_cu["end_gross_value"] + b_sf["end_gross_value"] + b_port["end_gross_portfolio"]),
            "horizon_end_after_tax_wealth": r10(b_cu["end_net_liquidation_value"] + b_sf["end_net_liquidation_value"] + b_port["end_net_liquidation_value"]),
            "cum_10yr_housing_value_enjoyed": r10(b_sf["cum_imputed_housing"]),
            "housing_adjusted_10yr_wealth": r10(b_cu["end_net_liquidation_value"] + b_sf["end_net_liquidation_value"] + b_port["end_net_liquidation_value"] + b_sf["cum_imputed_housing"]),
            "notes": "Forfeits Cupertino Prop 19 exclusion, causing full ~$85k/yr Cupertino property tax + ordinary tax on high rent."
        },
        {
            "id": "strategy_a1",
            "name": "A1. Live in Cupertino (Prop 19) + Keep SF (2 Rented, 1 Vacant)",
            "housing": "Cupertino Single-Family Home",
            "prop19_shield_captured": True,
            "yr1_net_cash_flow": r10(a_cfs[0]),
            "yr1_property_cash_flow_only": r10(a_cfs[0]),
            "yr1_portfolio_return_after_tax": 0,
            "horizon_end_gross_wealth": r10(a_cu["end_gross_value"] + a_sf["end_gross_value"] + a_port["end_gross_portfolio"]),
            "horizon_end_after_tax_wealth": r10(a_cu["end_net_liquidation_value"] + a_sf["end_net_liquidation_value"] + a_port["end_net_liquidation_value"]),
            "cum_10yr_housing_value_enjoyed": r10(a_cu["cum_imputed_housing"]),
            "housing_adjusted_10yr_wealth": r10(a_cu["end_net_liquidation_value"] + a_sf["end_net_liquidation_value"] + a_port["end_net_liquidation_value"] + a_cu["cum_imputed_housing"]),
            "notes": "Keeping SF Unit 3 empty while paying Cupertino taxes + reassessed SF taxes creates severe annual cash-flow drag."
        }
    ]

    strategies.sort(key=lambda x: x["horizon_end_after_tax_wealth"], reverse=True)
    return {
        "scenario": scenario_key,
        "inherit_year": inherit_year,
        "horizon_end_year": inherit_year + horizon_years,
        "at_inheritance_snapshot": base_row,
        "strategies": strategies
    }


def estate_threshold_matrix(inherit_year: int = 2045) -> List[Dict[str, Any]]:
    base_rows = project_yearly("base")
    row_y = next(r for r in base_rows if r["year"] == inherit_year)
    re_val_y = row_y["combined_real_estate_value"]
    excl_single_cur = row_y["fed_estate_excl_single"]
    excl_married_cur = row_y["fed_estate_excl_married"]

    t = inherit_year - 2026
    excl_single_rollback = 7500000.0 * ((1.0 + PARAMS["cpi_long_term"]) ** t)
    excl_married_rollback = excl_single_rollback * 2.0

    liquid_2026_buckets = [0, 3000000, 6000000, 10000000, 15000000, 20000000, 30000000]
    matrix = []
    for liq_26 in liquid_2026_buckets:
        liq_y = liq_26 * ((1.06) ** t)
        gross_estate = re_val_y + liq_y
        tax_single_cur = max(0.0, gross_estate - excl_single_cur) * PARAMS["fed_estate_rate"]
        tax_married_cur = max(0.0, gross_estate - excl_married_cur) * PARAMS["fed_estate_rate"]
        tax_single_stress = max(0.0, gross_estate - excl_single_rollback) * PARAMS["fed_estate_rate"]
        tax_married_stress = max(0.0, gross_estate - excl_married_rollback) * PARAMS["fed_estate_rate"]

        matrix.append({
            "liquid_assets_2026": r10(liq_26),
            "liquid_assets_projected": r10(liq_y),
            "real_estate_projected": r10(re_val_y),
            "total_gross_estate": r10(gross_estate),
            "current_law_single_excl": r10(excl_single_cur),
            "current_law_single_tax": r10(tax_single_cur),
            "current_law_married_excl": r10(excl_married_cur),
            "current_law_married_tax": r10(tax_married_cur),
            "rollback_stress_single_excl": r10(excl_single_rollback),
            "rollback_stress_single_tax": r10(tax_single_stress),
            "rollback_stress_married_tax": r10(tax_married_stress)
        })
    return matrix


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    verified = load_verified()

    projections = {
        "metadata": {
            "generated_date": "2026-11-10",
            "rounding_rule": "All projected & decision-analysis dollar amounts rounded to nearest $10",
            "primary_inheritance_year": 2045,
            "horizon_years": 10
        },
        "yearly_by_scenario": {
            k: project_yearly(k) for k in PARAMS["scenarios"].keys()
        },
        "strategy_comparisons": {
            f"{sc}_{yr}": evaluate_strategies(sc, yr, 10)
            for sc in ["base", "conservative", "growth", "user_naive"]
            for yr in [2040, 2045, 2050]
        },
        "estate_tax_matrix": {
            str(yr): estate_threshold_matrix(yr) for yr in [2040, 2045, 2050]
        },
        "verified_anchors": verified
    }

    out_path = root / "data" / "projections.json"
    with open(out_path, "w") as f:
        json.dump(projections, f, indent=2)

    print("=== STRATEGY RANKING (BASE CASE, INHERIT 2045 -> 2055) ===")
    for s in projections["strategy_comparisons"]["base_2045"]["strategies"]:
        print(f"  {s['name']}: Yr1 CF=${s['yr1_net_cash_flow']:,} | 2055 Liq Wealth=${s['horizon_end_after_tax_wealth']:,} | Housing-Adj Wealth=${s['housing_adjusted_10yr_wealth']:,}")

    print("\n=== ESTATE TAX MATRIX (2045) ===")
    for m in projections["estate_tax_matrix"]["2045"]:
        print(f"  2026 Liq ${m['liquid_assets_2026']:,} -> 2045 Estate ${m['total_gross_estate']:,} | Single Cur Tax ${m['current_law_single_tax']:,} | Married Cur Tax ${m['current_law_married_tax']:,} | Rollback Single Tax ${m['rollback_stress_single_tax']:,}")


if __name__ == "__main__":
    main()
