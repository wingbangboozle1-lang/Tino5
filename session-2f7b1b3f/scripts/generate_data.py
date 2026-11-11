#!/usr/bin/env python3
"""
Cupertino (95014) & San Francisco (94122) Trust Inheritance Financial Model (2026-2060)
Verified Statutory Parameters + $10-increment Decision Output Rounding
All personal identifiers anonymized.
"""

import json
from pathlib import Path


def r10(val: float) -> int:
    """Round any dollar figure to the nearest $10 increment."""
    return int(round(val / 10.0) * 10)


# ==============================================================================
# 1. HISTORICAL PROPERTY TAX & ASSESSMENT AUDIT (USER DATA VS OFFICIAL BOE CCPI)
# ==============================================================================
BOE_CCPI_FACTORS = {
    2014: {"fy": "2014-15", "ccpi_pct": 0.454, "factor": 1.00454},
    2015: {"fy": "2015-16", "ccpi_pct": 1.998, "factor": 1.01998},
    2016: {"fy": "2016-17", "ccpi_pct": 1.525, "factor": 1.01525},
    2017: {"fy": "2017-18", "ccpi_pct": 2.619, "factor": 1.02000},
    2018: {"fy": "2018-19", "ccpi_pct": 2.962, "factor": 1.02000},
    2019: {"fy": "2019-20", "ccpi_pct": 3.847, "factor": 1.02000},
    2020: {"fy": "2020-21", "ccpi_pct": 2.980, "factor": 1.02000},
    2021: {"fy": "2021-22", "ccpi_pct": 1.036, "factor": 1.01036},
    2022: {"fy": "2022-23", "ccpi_pct": 5.561, "factor": 1.02000},
    2023: {"fy": "2023-24", "ccpi_pct": 7.274, "factor": 1.02000},
    2024: {"fy": "2024-25", "ccpi_pct": 3.181, "factor": 1.02000},
    2025: {"fy": "2025-26", "ccpi_pct": 2.514, "factor": 1.02000},
    2026: {"fy": "2026-27", "ccpi_pct": 3.307, "factor": 1.02000},
}

CUPERTINO_HISTORY = [
    {"year": 2014, "tax": 5970, "tax_pct_note": None, "assessed": 440310, "assessed_pct_note": 0.5},
    {"year": 2015, "tax": 6130, "tax_pct_note": 2.8, "assessed": 449100, "assessed_pct_note": 2.0},
    {"year": 2016, "tax": 6410, "tax_pct_note": 4.6, "assessed": 455950, "assessed_pct_note": 1.5},
    {"year": 2017, "tax": 6380, "tax_pct_note": -0.5, "assessed": 465070, "assessed_pct_note": 2.0},
    {"year": 2018, "tax": 6380, "tax_pct_note": 0.0, "assessed": 474370, "assessed_pct_note": 2.0},
    {"year": 2019, "tax": 6570, "tax_pct_note": 2.8, "assessed": 483850, "assessed_pct_note": 2.0},
    {"year": 2020, "tax": 6570, "tax_pct_note": 0.0, "assessed": 493530, "assessed_pct_note": 2.0},
    {"year": 2021, "tax": 6660, "tax_pct_note": 1.5, "assessed": 498640, "assessed_pct_note": 1.0},
    {"year": 2022, "tax": 6760, "tax_pct_note": 1.4, "assessed": 508610, "assessed_pct_note": 2.0},
    {"year": 2023, "tax": 6920, "tax_pct_note": 2.4, "assessed": 518790, "assessed_pct_note": 2.0},
    {"year": 2024, "tax": 7000, "tax_pct_note": 1.2, "assessed": 529160, "assessed_pct_note": 2.0},
    {"year": 2025, "tax": 7210, "tax_pct_note": 2.9, "assessed": 539740, "assessed_pct_note": 2.0},
    {"year": 2026, "tax": None, "tax_pct_note": None, "assessed": 550540, "assessed_pct_note": 2.0},
]

SF_HISTORY = [
    {"year": 2016, "tax": 1680, "tax_pct_note": 1.6, "assessed": 96560, "assessed_pct_note": 1.5},
    {"year": 2017, "tax": 1740, "tax_pct_note": 3.9, "assessed": 98490, "assessed_pct_note": 2.0},
    {"year": 2018, "tax": 2060, "tax_pct_note": 18.4, "assessed": 100460, "assessed_pct_note": 2.0},
    {"year": 2019, "tax": 2130, "tax_pct_note": 3.5, "assessed": 102470, "assessed_pct_note": 2.0},
    {"year": 2020, "tax": 2200, "tax_pct_note": 3.0, "assessed": 104510, "assessed_pct_note": 2.0},
    {"year": 2021, "tax": 2070, "tax_pct_note": -5.9, "assessed": 105600, "assessed_pct_note": 1.0},
    {"year": 2022, "tax": 2110, "tax_pct_note": 2.0, "assessed": 107660, "assessed_pct_note": 2.0},
    {"year": 2023, "tax": 2180, "tax_pct_note": 3.4, "assessed": 109810, "assessed_pct_note": 2.0},
    {"year": 2024, "tax": 2320, "tax_pct_note": 6.2, "assessed": 112010, "assessed_pct_note": 2.0},
    {"year": 2025, "tax": 2440, "tax_pct_note": 5.3, "assessed": 114250, "assessed_pct_note": 2.0},
    {"year": 2026, "tax": None, "tax_pct_note": None, "assessed": None, "assessed_pct_note": None},
]


def audit_history(rows):
    audited = []
    for i, row in enumerate(rows):
        yr = row["year"]
        boe = BOE_CCPI_FACTORS[yr]
        prev = rows[i - 1] if i > 0 else None
        expected_assessed = None
        if prev and prev["assessed"] and row["assessed"]:
            expected_assessed = prev["assessed"] * boe["factor"]
        eff_rate = (row["tax"] / row["assessed"] * 100.0) if (row["tax"] and row["assessed"]) else None
        actual_tax_chg = (
            ((row["tax"] - prev["tax"]) / prev["tax"] * 100.0)
            if (prev and prev["tax"] and row["tax"])
            else None
        )
        actual_av_chg = (
            ((row["assessed"] - prev["assessed"]) / prev["assessed"] * 100.0)
            if (prev and prev["assessed"] and row["assessed"])
            else None
        )
        flags = []
        if row["tax"] is None:
            flags.append("Missing 2026 property tax bill — verify against County Tax Collector FY 2026-27 bill")
        if row["assessed"] is None:
            flags.append("Missing 2026 assessed value — verify against SF Assessor FY 2026-27 roll (BOE 1.02 projection = $116,530)")
        if actual_tax_chg is not None and abs(actual_tax_chg) > 5.0:
            flags.append(
                f"Large single-year tax change ({actual_tax_chg:+.1f}%) while Prop 13 AV rose <=2%; "
                "indicates voter-approved bond rate / parcel tax / direct charge shift — verify actual bill"
            )
        if row["tax"] == (prev["tax"] if prev else None) and row["assessed"] > (prev["assessed"] if prev else 0):
            flags.append("Total tax flat ($0 change) while assessed value increased ~2%; verify bond rate / parcel tax expiration")
        audited.append({
            **row,
            "tax_r10": r10(row["tax"]) if row["tax"] is not None else None,
            "assessed_r10": r10(row["assessed"]) if row["assessed"] is not None else None,
            "boe_fy": boe["fy"],
            "boe_factor": boe["factor"],
            "boe_ccpi_pct": boe["ccpi_pct"],
            "expected_assessed_r10": r10(expected_assessed) if expected_assessed else None,
            "actual_av_chg_pct": round(actual_av_chg, 2) if actual_av_chg is not None else None,
            "actual_tax_chg_pct": round(actual_tax_chg, 2) if actual_tax_chg is not None else None,
            "effective_tax_pct": round(eff_rate, 3) if eff_rate is not None else None,
            "flags": flags,
        })
    return audited


# ==============================================================================
# 2. VERIFIED BASELINE CONSTANTS (2026)
# ==============================================================================
CUP_FMV_2026 = 3_100_000.0
CUP_AV_2026 = 550_537.0
CUP_PARCEL_TAX_2026 = 900.0
CUP_ADVAL_RATE = 0.0118
CUP_WATER_2026 = 1_500.0
CUP_SOLAR_CREDIT_2026 = -180.0
CUP_INS_CA_AVG_2026 = 1_570.0
CUP_INS_REBUILD_SENS_2026 = 2_800.0
CUP_MAINT_2026 = 6_200.0

SF_FMV_2026 = 1_800_000.0
SF_AV_2025 = 114_248.0
SF_AV_2026 = round(SF_AV_2025 * 1.02)
SF_ADVAL_RATE = 0.0118162182
SF_PARCEL_TAX_2026 = 1_100.0
SF_RENT_2UNITS_2026 = 7_150.0 * 12.0
SF_RENT_UNIT3_EST_2026 = 3_580.0 * 12.0
SF_WATER_2026 = 365.0 * 12.0
SF_ELEC_2026 = 50.0 * 12.0
SF_INS_AVG_2026 = 1_570.0
SF_INS_3UNIT_SENS_2026 = 3_500.0
SF_MAINT_2026 = 12_600.0
SF_RENT_BOARD_FEE_UNIT = 59.0

PROP19_EXCLUSION_2026 = 1_044_586.0
FED_ESTATE_EXEMPT_2026 = 15_000_000.0


def run_yearly_projection(
    cup_apprec=0.0491,
    sf_apprec=0.0476,
    cpi=0.028,
    prop19_cap_growth=0.042,
    sf_water_near_growth=0.085,
    nem_sunset_year=2042,
):
    rows = []
    cup_fmv = CUP_FMV_2026
    cup_av = CUP_AV_2026
    sf_fmv = SF_FMV_2026
    sf_av = SF_AV_2026
    prop19_cap = PROP19_EXCLUSION_2026
    fed_exempt = FED_ESTATE_EXEMPT_2026

    for yr in range(2026, 2051):
        t = yr - 2026
        if t > 0:
            cup_fmv *= (1.0 + cup_apprec)
            cup_av *= 1.02
            sf_fmv *= (1.0 + sf_apprec)
            sf_av *= 1.02
            if yr % 2 == 1:
                prop19_cap *= (1.0 + prop19_cap_growth) ** 2
            fed_exempt *= (1.0 + cpi)

        cup_parcel = CUP_PARCEL_TAX_2026 * ((1.0 + cpi) ** t)
        cup_tax_pre = cup_av * CUP_ADVAL_RATE + cup_parcel

        sf_parcel = SF_PARCEL_TAX_2026 * ((1.0 + cpi) ** t)
        sf_tax_pre = sf_av * SF_ADVAL_RATE + sf_parcel

        cup_excluded_limit = cup_av + prop19_cap
        cup_excess = max(0.0, cup_fmv - cup_excluded_limit)
        cup_taxable_prop19 = cup_av + cup_excess
        cup_tax_prop19 = cup_taxable_prop19 * CUP_ADVAL_RATE + cup_parcel
        cup_tax_no_prop19 = cup_fmv * CUP_ADVAL_RATE + cup_parcel
        cup_prop19_savings = cup_tax_no_prop19 - cup_tax_prop19

        sf_tax_full_reassess = sf_fmv * SF_ADVAL_RATE + sf_parcel
        sf_unit_av = sf_av / 3.0
        sf_unit_fmv = sf_fmv / 3.0
        sf_unit_excess = max(0.0, sf_unit_fmv - (sf_unit_av + prop19_cap))
        sf_taxable_1unit_prop19 = (sf_unit_av + sf_unit_excess) + 2.0 * sf_unit_fmv
        sf_tax_1unit_prop19 = sf_taxable_1unit_prop19 * SF_ADVAL_RATE + sf_parcel
        sf_prop19_1unit_savings = sf_tax_full_reassess - sf_tax_1unit_prop19

        cup_water = CUP_WATER_2026 * ((1.0 + 0.04) ** t)
        if yr < nem_sunset_year:
            cup_elec = CUP_SOLAR_CREDIT_2026 * ((1.0 + 0.025) ** t)
        else:
            cup_elec = 420.0 * ((1.0 + 0.03) ** t)
        cup_ins = CUP_INS_CA_AVG_2026 * ((1.0 + 0.045) ** t)
        cup_ins_sens = CUP_INS_REBUILD_SENS_2026 * ((1.0 + 0.045) ** t)
        cup_maint = CUP_MAINT_2026 * ((1.0 + cpi) ** t)

        sf_water_factor = 1.0
        for k in range(1, t + 1):
            sf_water_factor *= (1.0 + (sf_water_near_growth if k <= 10 else 0.045))
        sf_water = SF_WATER_2026 * sf_water_factor
        sf_elec = SF_ELEC_2026 * ((1.0 + 0.035) ** t)
        sf_ins = SF_INS_AVG_2026 * ((1.0 + 0.045) ** t)
        sf_ins_sens = SF_INS_3UNIT_SENS_2026 * ((1.0 + 0.045) ** t)
        sf_maint = SF_MAINT_2026 * ((1.0 + cpi) ** t)
        sf_rent_2u_rc = SF_RENT_2UNITS_2026 * ((1.0 + 0.018) ** t)
        sf_rent_2u_blend = SF_RENT_2UNITS_2026 * ((1.0 + 0.030) ** t)

        combined_re = cup_fmv + sf_fmv
        headroom_single = fed_exempt - combined_re
        headroom_married = (2.0 * fed_exempt) - combined_re
        headroom_7_5m_risk = (7_500_000.0 * ((1.0 + cpi) ** t)) - combined_re

        rows.append({
            "year": yr,
            "cup_fmv": r10(cup_fmv),
            "cup_av_prop13": r10(cup_av),
            "cup_tax_pre": r10(cup_tax_pre),
            "prop19_cap": r10(prop19_cap),
            "cup_taxable_prop19": r10(cup_taxable_prop19),
            "cup_tax_prop19": r10(cup_tax_prop19),
            "cup_tax_no_prop19": r10(cup_tax_no_prop19),
            "cup_prop19_savings": r10(cup_prop19_savings),
            "cup_water": r10(cup_water),
            "cup_elec": r10(cup_elec),
            "cup_ins_base": r10(cup_ins),
            "cup_ins_sens": r10(cup_ins_sens),
            "cup_maint": r10(cup_maint),
            "sf_fmv": r10(sf_fmv),
            "sf_av_prop13": r10(sf_av),
            "sf_tax_pre": r10(sf_tax_pre),
            "sf_tax_full_reassess": r10(sf_tax_full_reassess),
            "sf_tax_1unit_prop19": r10(sf_tax_1unit_prop19),
            "sf_prop19_1unit_savings": r10(sf_prop19_1unit_savings),
            "sf_water": r10(sf_water),
            "sf_elec": r10(sf_elec),
            "sf_ins_base": r10(sf_ins),
            "sf_ins_sens": r10(sf_ins_sens),
            "sf_maint": r10(sf_maint),
            "sf_rent_2u_rc": r10(sf_rent_2u_rc),
            "sf_rent_2u_blend": r10(sf_rent_2u_blend),
            "combined_re": r10(combined_re),
            "fed_exempt_single": r10(fed_exempt),
            "fed_exempt_married": r10(2.0 * fed_exempt),
            "headroom_single": r10(headroom_single),
            "headroom_married": r10(headroom_married),
            "headroom_7_5m_risk": r10(headroom_7_5m_risk),
            "_exact": {
                "cup_fmv": cup_fmv, "cup_av": cup_av, "cup_tax_prop19": cup_tax_prop19,
                "cup_tax_no_prop19": cup_tax_no_prop19, "cup_water": cup_water, "cup_elec": cup_elec,
                "cup_ins": cup_ins, "cup_ins_sens": cup_ins_sens, "cup_maint": cup_maint,
                "sf_fmv": sf_fmv, "sf_av": sf_av, "sf_tax_full_reassess": sf_tax_full_reassess,
                "sf_tax_1unit_prop19": sf_tax_1unit_prop19,
                "sf_water": sf_water, "sf_elec": sf_elec, "sf_ins": sf_ins, "sf_ins_sens": sf_ins_sens,
                "sf_maint": sf_maint, "sf_rent_2u_rc": sf_rent_2u_rc, "sf_rent_2u_blend": sf_rent_2u_blend,
                "prop19_cap": prop19_cap,
            },
        })
    return rows


def compare_strategies(
    inherit_year=2045,
    hold_years=10,
    cup_apprec=0.0491,
    sf_apprec=0.0476,
    cpi=0.028,
    equity_return=0.095,
    treasury_return=0.045,
    cup_rent_yield=0.028,
    marginal_ord_tax=0.35,
    div_yield=0.015,
    div_tax_rate=0.30,
    sell_cost_cup=0.0511,
    use_sens_insurance=False,
    parent_primary_is_cup=True,
):
    proj = run_yearly_projection(cup_apprec=cup_apprec, sf_apprec=sf_apprec, cpi=cpi)
    base = next(r for r in proj if r["year"] == inherit_year)["_exact"]

    def sf_trans_rate(val):
        return 0.0225 if val >= 5_000_000 else 0.0075

    ins_cup0 = base["cup_ins_sens"] if use_sens_insurance else base["cup_ins"]
    ins_sf0 = base["sf_ins_sens"] if use_sens_insurance else base["sf_ins"]
    eq_after_div_tax = equity_return - div_yield * div_tax_rate
    treas_after_tax = treasury_return * (1.0 - 0.24)
    cap_gain_tax_rate = 0.30

    def sim_live_sf_sell_cup(reinvest_rate):
        cup_proceeds = base["cup_fmv"] * (1.0 - sell_cost_cup)
        port = cup_proceeds
        sf_val = base["sf_fmv"]
        sf_taxable = base["sf_fmv"] if parent_primary_is_cup else (
            (base["sf_av"] / 3.0 + max(0.0, base["sf_fmv"] / 3.0 - (base["sf_av"] / 3.0 + base["prop19_cap"])))
            + 2.0 * (base["sf_fmv"] / 3.0)
        )
        sf_rent = base["sf_rent_2u_blend"]
        sf_water = base["sf_water"]
        sf_elec = base["sf_elec"]
        sf_ins = ins_sf0
        sf_maint = base["sf_maint"]
        sf_depr_rental = (base["sf_fmv"] * 0.60 * (2.0 / 3.0)) / 27.5

        yr1_cf = None
        init_sf_tax = None
        for y in range(hold_years):
            t_tot = inherit_year - 2026 + y
            if y > 0:
                sf_val *= (1.0 + sf_apprec)
                sf_taxable *= 1.02
                sf_rent *= (1.0 + 0.028)
                sf_water *= (1.0 + 0.045)
                sf_elec *= (1.0 + 0.035)
                sf_ins *= (1.0 + 0.045)
                sf_maint *= (1.0 + cpi)
            sf_prop_tax = sf_taxable * SF_ADVAL_RATE + SF_PARCEL_TAX_2026 * ((1.0 + cpi) ** t_tot)
            if y == 0:
                init_sf_tax = sf_prop_tax

            rental_exp_ded = (2.0 / 3.0) * (sf_prop_tax + sf_water + sf_ins + sf_maint) + 2.0 * SF_RENT_BOARD_FEE_UNIT
            taxable_rental = sf_rent - rental_exp_ded - sf_depr_rental
            income_tax_sf = max(0.0, taxable_rental) * marginal_ord_tax
            net_sf_cf = sf_rent - (sf_prop_tax + sf_water + sf_elec + sf_ins + sf_maint + 2.0 * SF_RENT_BOARD_FEE_UNIT) - income_tax_sf
            if y == 0:
                yr1_cf = net_sf_cf
            port = port * (1.0 + reinvest_rate) + net_sf_cf

        sf_gain_post = max(0.0, sf_val - base["sf_fmv"])
        cum_depr = sf_depr_rental * hold_years
        sf_after_tax = sf_val * (1.0 - (0.05 + sf_trans_rate(sf_val))) - (sf_gain_post * cap_gain_tax_rate + cum_depr * 0.25)
        stock_gain = max(0.0, port - cup_proceeds)
        port_after_tax = port - stock_gain * cap_gain_tax_rate
        return {
            "yr1_net_cf": r10(yr1_cf),
            "end_re_gross": r10(sf_val),
            "end_liq_portfolio": r10(port),
            "end_total_gross": r10(sf_val + port),
            "end_total_after_tax_liq": r10(sf_after_tax + port_after_tax),
            "initial_cup_tax": 0,
            "initial_sf_tax": r10(init_sf_tax),
            "initial_proceeds": r10(cup_proceeds),
        }

    def sim_live_sf_rent_cup():
        cup_val = base["cup_fmv"]
        cup_taxable = base["cup_fmv"]
        cup_rent = base["cup_fmv"] * cup_rent_yield
        cup_depr = (base["cup_fmv"] * 0.45) / 27.5
        cup_ins = ins_cup0 * 1.15
        cup_maint = base["cup_maint"]

        sf_val = base["sf_fmv"]
        sf_taxable = base["sf_fmv"] if parent_primary_is_cup else (
            (base["sf_av"] / 3.0 + max(0.0, base["sf_fmv"] / 3.0 - (base["sf_av"] / 3.0 + base["prop19_cap"])))
            + 2.0 * (base["sf_fmv"] / 3.0)
        )
        sf_rent = base["sf_rent_2u_blend"]
        sf_depr_rental = (base["sf_fmv"] * 0.60 * (2.0 / 3.0)) / 27.5
        sf_water = base["sf_water"]
        sf_elec = base["sf_elec"]
        sf_ins = ins_sf0
        sf_maint = base["sf_maint"]

        side_cash = 0.0
        yr1_cf = None
        init_cup_tax = None
        init_sf_tax = None
        for y in range(hold_years):
            t_tot = inherit_year - 2026 + y
            if y > 0:
                cup_val *= (1.0 + cup_apprec)
                cup_taxable *= 1.02
                cup_rent *= (1.0 + cpi)
                cup_ins *= (1.0 + 0.045)
                cup_maint *= (1.0 + cpi)

                sf_val *= (1.0 + sf_apprec)
                sf_taxable *= 1.02
                sf_rent *= (1.0 + 0.028)
                sf_water *= (1.0 + 0.045)
                sf_elec *= (1.0 + 0.035)
                sf_ins *= (1.0 + 0.045)
                sf_maint *= (1.0 + cpi)

            cup_prop_tax = cup_taxable * CUP_ADVAL_RATE + CUP_PARCEL_TAX_2026 * ((1.0 + cpi) ** t_tot)
            sf_prop_tax = sf_taxable * SF_ADVAL_RATE + SF_PARCEL_TAX_2026 * ((1.0 + cpi) ** t_tot)
            if y == 0:
                init_cup_tax = cup_prop_tax
                init_sf_tax = sf_prop_tax

            cup_vacancy = cup_rent * 0.04
            cup_taxable_inc = (cup_rent - cup_vacancy) - (cup_prop_tax + cup_ins + cup_maint) - cup_depr
            cup_inc_tax = max(0.0, cup_taxable_inc) * marginal_ord_tax
            cup_cf = (cup_rent - cup_vacancy) - (cup_prop_tax + cup_ins + cup_maint) - cup_inc_tax

            sf_exp_ded = (2.0 / 3.0) * (sf_prop_tax + sf_water + sf_ins + sf_maint) + 2.0 * SF_RENT_BOARD_FEE_UNIT
            sf_taxable_inc = sf_rent - sf_exp_ded - sf_depr_rental
            sf_inc_tax = max(0.0, sf_taxable_inc) * marginal_ord_tax
            sf_cf = sf_rent - (sf_prop_tax + sf_water + sf_elec + sf_ins + sf_maint + 2.0 * SF_RENT_BOARD_FEE_UNIT) - sf_inc_tax

            tot_cf = cup_cf + sf_cf
            if y == 0:
                yr1_cf = tot_cf
            side_cash = side_cash * (1.0 + eq_after_div_tax) + tot_cf

        cup_after_tax = cup_val * (1.0 - sell_cost_cup) - max(0.0, cup_val - base["cup_fmv"]) * cap_gain_tax_rate - (cup_depr * hold_years) * 0.25
        sf_after_tax = sf_val * (1.0 - (0.05 + sf_trans_rate(sf_val))) - max(0.0, sf_val - base["sf_fmv"]) * cap_gain_tax_rate - (sf_depr_rental * hold_years) * 0.25
        return {
            "yr1_net_cf": r10(yr1_cf),
            "end_re_gross": r10(cup_val + sf_val),
            "end_liq_portfolio": r10(side_cash),
            "end_total_gross": r10(cup_val + sf_val + side_cash),
            "end_total_after_tax_liq": r10(cup_after_tax + sf_after_tax + side_cash * 0.85),
            "initial_cup_tax": r10(init_cup_tax),
            "initial_sf_tax": r10(init_sf_tax),
            "initial_proceeds": 0,
        }

    def sim_live_cup_rent_sf(rent_unit3=True):
        cup_val = base["cup_fmv"]
        prop19_cap = base["prop19_cap"]
        cup_taxable = (base["cup_av"] + max(0.0, base["cup_fmv"] - (base["cup_av"] + prop19_cap))) if parent_primary_is_cup else base["cup_fmv"]
        cup_water = base["cup_water"]
        cup_elec = base["cup_elec"]
        cup_ins = ins_cup0
        cup_maint = base["cup_maint"]

        sf_val = base["sf_fmv"]
        sf_taxable = base["sf_fmv"]
        unit3_rent = (SF_RENT_UNIT3_EST_2026 * ((1.0 + cpi) ** (inherit_year - 2026))) if rent_unit3 else 0.0
        sf_rent = base["sf_rent_2u_blend"] + unit3_rent
        sf_depr = (base["sf_fmv"] * 0.60) / 27.5
        sf_water = base["sf_water"]
        sf_elec = base["sf_elec"]
        sf_ins = ins_sf0
        sf_maint = base["sf_maint"]

        side_cash = 0.0
        yr1_cf = None
        init_cup_tax = None
        init_sf_tax = None
        for y in range(hold_years):
            t_tot = inherit_year - 2026 + y
            if y > 0:
                cup_val *= (1.0 + cup_apprec)
                cup_taxable *= 1.02
                cup_water *= (1.0 + 0.04)
                cup_elec *= (1.0 + 0.03)
                cup_ins *= (1.0 + 0.045)
                cup_maint *= (1.0 + cpi)

                sf_val *= (1.0 + sf_apprec)
                sf_taxable *= 1.02
                sf_rent *= (1.0 + 0.028)
                sf_water *= (1.0 + 0.045)
                sf_elec *= (1.0 + 0.035)
                sf_ins *= (1.0 + 0.045)
                sf_maint *= (1.0 + cpi)

            cup_prop_tax = cup_taxable * CUP_ADVAL_RATE + CUP_PARCEL_TAX_2026 * ((1.0 + cpi) ** t_tot)
            sf_prop_tax = sf_taxable * SF_ADVAL_RATE + SF_PARCEL_TAX_2026 * ((1.0 + cpi) ** t_tot)
            if y == 0:
                init_cup_tax = cup_prop_tax
                init_sf_tax = sf_prop_tax

            cup_cf = -(cup_prop_tax + cup_water + cup_elec + cup_ins + cup_maint)
            units_rented = 3 if rent_unit3 else 2
            sf_exp_ded = sf_prop_tax + sf_water + sf_elec + sf_ins + sf_maint + units_rented * SF_RENT_BOARD_FEE_UNIT
            sf_taxable_inc = sf_rent - sf_exp_ded - sf_depr
            sf_inc_tax = max(0.0, sf_taxable_inc) * marginal_ord_tax
            sf_cf = sf_rent - sf_exp_ded - sf_inc_tax

            tot_cf = cup_cf + sf_cf
            if y == 0:
                yr1_cf = tot_cf
            side_cash = side_cash * (1.0 + eq_after_div_tax) + tot_cf

        cup_gain_post = max(0.0, cup_val - base["cup_fmv"] - 500_000.0)
        cup_after_tax = cup_val * (1.0 - sell_cost_cup) - cup_gain_post * cap_gain_tax_rate
        sf_after_tax = sf_val * (1.0 - (0.05 + sf_trans_rate(sf_val))) - max(0.0, sf_val - base["sf_fmv"]) * cap_gain_tax_rate - (sf_depr * hold_years) * 0.25
        return {
            "yr1_net_cf": r10(yr1_cf),
            "end_re_gross": r10(cup_val + sf_val),
            "end_liq_portfolio": r10(side_cash),
            "end_total_gross": r10(cup_val + sf_val + side_cash),
            "end_total_after_tax_liq": r10(cup_after_tax + sf_after_tax + side_cash * 0.85),
            "initial_cup_tax": r10(init_cup_tax),
            "initial_sf_tax": r10(init_sf_tax),
            "initial_proceeds": 0,
        }

    def sim_live_cup_sell_sf(reinvest_rate):
        sf_proceeds = base["sf_fmv"] * (1.0 - (0.05 + sf_trans_rate(base["sf_fmv"])))
        port = sf_proceeds
        cup_val = base["cup_fmv"]
        prop19_cap = base["prop19_cap"]
        cup_taxable = (base["cup_av"] + max(0.0, base["cup_fmv"] - (base["cup_av"] + prop19_cap))) if parent_primary_is_cup else base["cup_fmv"]
        cup_water = base["cup_water"]
        cup_elec = base["cup_elec"]
        cup_ins = ins_cup0
        cup_maint = base["cup_maint"]
        yr1_cf = None
        init_cup_tax = None
        for y in range(hold_years):
            t_tot = inherit_year - 2026 + y
            if y > 0:
                cup_val *= (1.0 + cup_apprec)
                cup_taxable *= 1.02
                cup_water *= (1.0 + 0.04)
                cup_elec *= (1.0 + 0.03)
                cup_ins *= (1.0 + 0.045)
                cup_maint *= (1.0 + cpi)
            cup_prop_tax = cup_taxable * CUP_ADVAL_RATE + CUP_PARCEL_TAX_2026 * ((1.0 + cpi) ** t_tot)
            if y == 0:
                init_cup_tax = cup_prop_tax
            cup_cf = -(cup_prop_tax + cup_water + cup_elec + cup_ins + cup_maint)
            if y == 0:
                yr1_cf = cup_cf
            port = port * (1.0 + reinvest_rate) + cup_cf
        cup_gain_post = max(0.0, cup_val - base["cup_fmv"] - 500_000.0)
        cup_after_tax = cup_val * (1.0 - sell_cost_cup) - cup_gain_post * cap_gain_tax_rate
        port_after_tax = port - max(0.0, port - sf_proceeds) * cap_gain_tax_rate
        return {
            "yr1_net_cf": r10(yr1_cf),
            "end_re_gross": r10(cup_val),
            "end_liq_portfolio": r10(port),
            "end_total_gross": r10(cup_val + port),
            "end_total_after_tax_liq": r10(cup_after_tax + port_after_tax),
            "initial_cup_tax": r10(init_cup_tax),
            "initial_sf_tax": 0,
            "initial_proceeds": r10(sf_proceeds),
        }

    def sim_sell_both(reinvest_rate):
        cup_proc = base["cup_fmv"] * (1.0 - sell_cost_cup)
        sf_proc = base["sf_fmv"] * (1.0 - (0.05 + sf_trans_rate(base["sf_fmv"])))
        port = cup_proc + sf_proc
        rent_cost = 4500.0 * 12.0 * ((1.0 + cpi) ** (inherit_year - 2026))
        yr1_cf = None
        for y in range(hold_years):
            if y > 0:
                rent_cost *= (1.0 + cpi)
            if y == 0:
                yr1_cf = -rent_cost
            port = port * (1.0 + reinvest_rate) - rent_cost
        port_after_tax = port - max(0.0, port - (cup_proc + sf_proc)) * cap_gain_tax_rate
        return {
            "yr1_net_cf": r10(yr1_cf),
            "end_re_gross": 0,
            "end_liq_portfolio": r10(port),
            "end_total_gross": r10(port),
            "end_total_after_tax_liq": r10(port_after_tax),
            "initial_cup_tax": 0,
            "initial_sf_tax": 0,
            "initial_proceeds": r10(cup_proc + sf_proc),
        }

    return {
        "inherit_year": inherit_year,
        "hold_years": hold_years,
        "cup_fmv_at_inherit": r10(base["cup_fmv"]),
        "sf_fmv_at_inherit": r10(base["sf_fmv"]),
        "strategies": {
            "A_live_sf_sell_cup_equity": sim_live_sf_sell_cup(eq_after_div_tax),
            "A2_live_sf_sell_cup_treasury": sim_live_sf_sell_cup(treas_after_tax),
            "B_live_sf_rent_cup": sim_live_sf_rent_cup(),
            "C_live_cup_rent_sf3": sim_live_cup_rent_sf(True),
            "D_live_cup_sell_sf_equity": sim_live_cup_sell_sf(eq_after_div_tax),
            "E_sell_both_equity": sim_sell_both(eq_after_div_tax),
        },
    }


def main():
    cup_aud = audit_history(CUPERTINO_HISTORY)
    sf_aud = audit_history(SF_HISTORY)

    proj_hist = run_yearly_projection()
    proj_cons = run_yearly_projection(cup_apprec=0.0375, sf_apprec=0.0350, cpi=0.028, prop19_cap_growth=0.035)

    # Strip _exact before JSON export
    clean_hist = [{k: v for k, v in r.items() if k != "_exact"} for r in proj_hist]
    clean_cons = [{k: v for k, v in r.items() if k != "_exact"} for r in proj_cons]

    scenarios = {
        "hist_2040": compare_strategies(inherit_year=2040),
        "hist_2045": compare_strategies(inherit_year=2045),
        "hist_2050": compare_strategies(inherit_year=2050),
        "cons_2040": compare_strategies(inherit_year=2040, cup_apprec=0.0375, sf_apprec=0.0350, equity_return=0.080),
        "cons_2045": compare_strategies(inherit_year=2045, cup_apprec=0.0375, sf_apprec=0.0350, equity_return=0.080),
        "cons_2050": compare_strategies(inherit_year=2050, cup_apprec=0.0375, sf_apprec=0.0350, equity_return=0.080),
        "hist_2045_sens_ins": compare_strategies(inherit_year=2045, use_sens_insurance=True),
        "hist_2045_sf_parent_primary": compare_strategies(inherit_year=2045, parent_primary_is_cup=False),
    }

    payload = {
        "metadata": {
            "as_of_date": "2026-11-10",
            "rounding_rule": "Nearest $10 increments on all decision & projection dollar amounts",
            "anonymization": "All personal, trust, street address, and APN identifiers replaced with placeholders",
        },
        "history_audit": {
            "cupertino": cup_aud,
            "san_francisco": sf_aud,
        },
        "projections": {
            "historical_baseline": clean_hist,
            "conservative": clean_cons,
        },
        "strategy_comparisons": scenarios,
    }

    root_dir = Path(__file__).resolve().parent.parent
    (root_dir / "data" / "model_output.json").write_text(json.dumps(payload, indent=2))
    (root_dir / "assets" / "data.js").write_text(
        "// Auto-generated by scripts/generate_data.py — all dollar values rounded to nearest $10\n"
        f"window.INHERITANCE_MODEL_DATA = {json.dumps(payload, indent=2)};\n"
    )
    print("Wrote data/model_output.json and assets/data.js successfully.")
    for sname in ["hist_2040", "hist_2045", "hist_2050", "cons_2045", "hist_2045_sf_parent_primary"]:
        sc = scenarios[sname]
        print(f"\n--- {sname} (Cup=${sc['cup_fmv_at_inherit']:,}, SF=${sc['sf_fmv_at_inherit']:,}) ---")
        for k, v in sc["strategies"].items():
            print(
                f"  {k:30s}: Yr1CF=${v['yr1_net_cf']:>8,} | EndGross=${v['end_total_gross']:>11,} | "
                f"EndAfterTax=${v['end_total_after_tax_liq']:>11,} | Tax(Cup/SF)=${v['initial_cup_tax']:,}/${v['initial_sf_tax']:,}"
            )


if __name__ == "__main__":
    main()
