#!/usr/bin/env python3
"""
Tino5 inheritance decision model  (no third-party dependencies)

Every input is labelled:
  VERIFIED   - traced to an official/primary source (see data/sources.json by id)
  PROVIDED   - supplied by the property owner (unverified, flagged for review)
  ASSUMPTION - a modelling choice, documented with an id (A1..A28), flagged

Output: data/model.json  (all money rounded to nearest $10 by r10()).

Privacy: no names, addresses, APNs or account numbers are used. The subject
properties are referred to only as "Property A" (95014) and "Property B" (94122).
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def r10(x):
    return int(round(x / 10.0)) * 10


def grow(base, rate, years):
    return base * (1 + rate) ** years


# ---------------------------------------------------------------- VERIFIED
V = {
    "prop13_cap": 0.02,                 # CA Const. art. XIII A, s.2(b)
    "prop19_excl_2025_2027": 1044586,   # BOE, transfers 2025-02-16 .. 2027-02-15
    "hox_av": 7000,                     # BOE homeowners' exemption
    "sf_rate": 0.0118162182,            # SF Treasurer & Tax Collector FY2026-27
    "scc_adval": 0.01193,               # SCC Assessor annual report, county average
    "fed_excl_2026": 15000000,          # IRS basic exclusion amount, 2026
    "fed_estate_top": 0.40,             # IRC s.2001(c)
    "transfer_tax": 0.0011,             # RTC s.11911 / s.11931 ($0.55 per $500)
}

# ---------------------------------------------------------------- PROVIDED
P = {
    "A_value_2026": 3100000,
    "A_assessed_2026": 550540,
    "A_tax_2025": 7210,
    "B_value_2026": 1800000,
    "B_tax_2025": 2440,  # FY2025-26 bill; FY2026-27 rate 1.18162182%
    "B_assessed_2025": 114250,
    "B_rent_2units_mo": 7150,
    "A_water_mo": 130,
    "A_elec_mo": -15,
    "B_water_mo": 365,
    "B_elec_mo": 50,
    "A_ins_quote": 1500,
    "B_ins_quote": 1500,
}

# -------------------------------------------------------------- ASSUMPTIONS
AS = {
    "A1_appreciation": 0.040,
    "A2_cpi": 0.023,
    "A3_rent_growth": 0.030,
    "A4_water_growth": 0.045,
    "A5_elec_growth": 0.050,
    "A6_insurance_growth": 0.060,
    "A7_insurance_rate_of_rc": 0.0030,
    "A8_structure_share": 0.55,
    "A9_maint_rate": 0.0100,
    "A10_maint_rate_rental": 0.0125,
    "A11_vacancy": 0.05,
    "A12_management": 0.08,
    "A13_sell_commission": 0.055,
    "A14_sell_other": 0.005,
    "A15_invest_nominal": 0.060,
    "A16_invest_tax_drag": 0.010,
    "A17_discount": 0.050,
    "A18_fed_ord": 0.24,
    "A19_ca_ord": 0.093,
    "A20_fed_cg": 0.20,
    "A21_niit": 0.038,
    "A22_ca_cg": 0.133,
    "A23_depr_life": 27.5,
    "A24_recapture": 0.25,
    "A25_exclusion_growth": 0.030,
    "A26_fixed_direct_assess": 770,
    "A27_land_share": 0.45,
    "A28_gross_yield": 0.038,
    "A29_post_nem_elec_kwh": 900,
}


def param(**over):
    p = dict(AS)
    p.update(over)
    return p


def structure_value(v, p):
    return v * p["A8_structure_share"]


# ------------------------------------------------------------ PROP 19 ENGINE
def exclusion_at(year, p):
    if year <= 2027:
        return V["prop19_excl_2025_2027"]
    return grow(V["prop19_excl_2025_2027"], p["A25_exclusion_growth"], year - 2027)


def prop19_new_base(fmv, fbyv, excl):
    limit = fbyv + excl
    if fmv <= limit:
        return fbyv, 0.0
    return fmv - excl, fmv - limit


def cu_tax(year, inherit_year, scenario, p):
    """(tax, assessed_value, base_year_value, excess_above_prop19_limit)"""
    fbyv = grow(P["A_assessed_2026"], V["prop13_cap"], inherit_year - 2026)
    fixed = p["A26_fixed_direct_assess"]
    if year < inherit_year:
        av = grow(P["A_assessed_2026"], V["prop13_cap"], year - 2026)
        return V["scc_adval"] * av + fixed, av, P["A_assessed_2026"], 0.0
    fmv = grow(P["A_value_2026"], p["A1_appreciation"], inherit_year - 2026)
    if scenario == "live":
        base, excess = prop19_new_base(fmv, fbyv, exclusion_at(inherit_year, p))
        hox = True
    else:
        base, excess = fmv, fmv - (fbyv + exclusion_at(inherit_year, p))
        hox = False
    av = grow(base, V["prop13_cap"], year - inherit_year)
    if hox:
        av = max(0.0, av - V["hox_av"])
    return V["scc_adval"] * av + fixed, av, base, excess


def sf_tax(year, fixed=0.0):
    av0 = P["B_tax_2025"] / V["sf_rate"]          # implied total assessed value
    av = grow(av0, V["prop13_cap"], year - 2026)
    return V["sf_rate"] * av + fixed, av


# ------------------------------------------------------- OPERATING COSTS
def cu_costs(year, inherit_year, scenario, p):
    t = year - 2026
    value = grow(P["A_value_2026"], p["A1_appreciation"], t)
    rc0 = structure_value(P["A_value_2026"], p)
    rental = (year >= inherit_year and scenario == "rent")
    rate = p["A7_insurance_rate_of_rc"] * (1.25 if rental else 1.0)
    rate = min(rate * (1 + p["A6_insurance_growth"]) ** t, 0.008 * (1.25 if rental else 1.0))
    ins = structure_value(value, p) * rate
    water = P["A_water_mo"] * 12 * (1 + p["A4_water_growth"]) ** t
    elec = P["A_elec_mo"] * 12 * (1 + p["A5_elec_growth"]) ** t
    if year >= inherit_year + 16:
        elec = max(elec, p["A29_post_nem_elec_kwh"] * (1 + p["A5_elec_growth"]) ** t)
    if rental:
        elec = 0.0
    maint = structure_value(value, p) * (p["A10_maint_rate_rental"] if rental else p["A9_maint_rate"])
    return dict(value=value, insurance=ins, water=water, electric=elec, maintenance=maint)


def sf_costs(year, p):
    t = year - 2026
    value = grow(P["B_value_2026"], p["A1_appreciation"], t)
    rc0 = structure_value(P["B_value_2026"], p)
    return dict(
        value=value,
        insurance=structure_value(value, p) * min(p["A7_insurance_rate_of_rc"] * 1.4
                                                  * (1 + p["A6_insurance_growth"]) ** t, 0.008 * 1.4),
        water=P["B_water_mo"] * 12 * (1 + p["A4_water_growth"]) ** t,
        electric=P["B_elec_mo"] * 12 * (1 + p["A5_elec_growth"]) ** t,
        maintenance=structure_value(value, p) * p["A10_maint_rate_rental"],
    )


def cu_market_rent(year, p):
    return grow(P["A_value_2026"], p["A1_appreciation"], year - 2026) * p["A28_gross_yield"] / 12


def sf_rent(year, units, p):
    per_unit = (P["B_rent_2units_mo"] / 2) * (1 + p["A3_rent_growth"]) ** (year - 2026)
    return per_unit * units


# ------------------------------------------------------------ SCENARIO RUN
def run(scenario, inherit_year, horizon, p):
    portfolio = 0.0
    rows, cum_cash, depr_total = [], 0.0, 0.0
    net_inv = p["A15_invest_nominal"] - p["A16_invest_tax_drag"]
    sf_units = 3 if scenario == "live" else 2

    for year in range(2026, horizon + 1):
        cu = cu_costs(year, inherit_year, scenario, p)
        sf = sf_costs(year, p)
        ct, cav, cbase, cexcess = cu_tax(year, inherit_year, scenario, p)
        st, sav = sf_tax(year)

        if year < inherit_year:
            gross = sf_rent(year, 2, p) * 12 * (1 - p["A11_vacancy"])
            opex = sf["water"] + sf["electric"] + sf["maintenance"]
            net = gross - opex - st
            tax = max(0.0, gross - sf["maintenance"]) * (p["A18_fed_ord"] + p["A19_ca_ord"])
            net -= tax
            rows.append(dict(year=year, phase="pre-inheritance", cu_value=r10(cu["value"]),
                             cu_property_tax=r10(ct), cu_assessed=r10(cav), sf_value=r10(sf["value"]),
                             sf_property_tax=r10(st), rent=r10(gross), insurance=r10(sf["insurance"]),
                             other_costs=r10(opex + cu["insurance"]), income_tax=r10(tax),
                             net_cash=r10(net), sale_proceeds=0, portfolio=r10(portfolio)))
            portfolio = portfolio * (1 + net_inv) + net
            cum_cash += net
            continue

        sale = 0.0
        if scenario == "sell" and year >= inherit_year:
            if year == inherit_year:
                costs = cu["value"] * (p["A13_sell_commission"] + p["A14_sell_other"] + V["transfer_tax"])
                sale = cu["value"] - costs
                portfolio += sale
            ct = 0.0
            cu = dict(cu, insurance=0.0, water=0.0, electric=0.0, maintenance=0.0)

        gross = sf_rent(year, sf_units, p) * 12 * (1 - p["A11_vacancy"])
        cu_rent = cu_market_rent(year, p) * 12 * (1 - p["A11_vacancy"]) if scenario == "rent" else 0.0
        mgmt = (cu_rent + gross) * p["A12_management"]
        depr = 0.0
        if scenario in ("live", "rent"):
            depr = (cu["value"] * (1 - p["A27_land_share"])) / p["A23_depr_life"]
        depr_total += depr

        opex = (cu["insurance"] + cu["water"] + cu["electric"] + cu["maintenance"]
                + sf["insurance"] + sf["water"] + sf["electric"] + sf["maintenance"] + mgmt)
        deductible = sf["maintenance"] + mgmt + (cu["maintenance"] if scenario == "rent" else 0.0)
        taxable = max(0.0, (gross + cu_rent) - deductible - depr)
        itax = taxable * (p["A18_fed_ord"] + p["A19_ca_ord"])
        net = gross + cu_rent - opex - ct - st - itax

        rows.append(dict(year=year, phase="post-inheritance", cu_value=r10(cu["value"]),
                         cu_property_tax=r10(ct), cu_assessed=r10(cav), cu_base_year_value=r10(cbase),
                         prop19_excess=r10(cexcess), sf_value=r10(sf["value"]),
                         sf_property_tax=r10(st), rent=r10(gross + cu_rent),
                         insurance=r10(cu["insurance"] + sf["insurance"]),
                         other_costs=r10(opex - cu["insurance"] - sf["insurance"]),
                         income_tax=r10(itax), net_cash=r10(net), sale_proceeds=r10(sale),
                         portfolio=r10(portfolio)))
        portfolio = portfolio * (1 + net_inv) + net
        cum_cash += net

    cu_end = grow(P["A_value_2026"], p["A1_appreciation"], horizon - 2026)
    sell_cost = p["A13_sell_commission"] + p["A14_sell_other"] + V["transfer_tax"]
    housing, cgtax, imputed = 0.0, 0.0, 0.0
    if scenario in ("live", "rent"):
        basis = grow(P["A_value_2026"], p["A1_appreciation"], inherit_year - 2026)
        gain = max(0.0, cu_end * (1 - sell_cost) - basis)
        cgtax = gain * (p["A20_fed_cg"] + p["A21_niit"] + p["A22_ca_cg"]) + depr_total * p["A24_recapture"]
        housing = cu_end * (1 - sell_cost)
    if scenario == "live":
        # occupies Property A; Property B third unit is rented out
        imputed = sum(cu_market_rent(y, p) * 12 * (1 - p["A11_vacancy"])
                      for y in range(inherit_year, horizon + 1))
    else:
        # keeps occupying the third unit of Property B (no rent paid, rent forgone)
        imputed = sum(sf_rent(y, 1, p) * 12 * (1 - p["A11_vacancy"])
                      for y in range(inherit_year, horizon + 1))
    terminal = portfolio + housing - cgtax
    return dict(rows=rows, portfolio=r10(portfolio), housing_asset=r10(housing),
                cap_gains_tax=r10(cgtax), terminal=r10(terminal), cum_cash=r10(cum_cash),
                imputed_rent=r10(imputed), economic_value=r10(terminal + imputed))


def npv(rows, discount, base_year=2026):
    return sum(r["net_cash"] / (1 + discount) ** (r["year"] - base_year) for r in rows)


def pv_total(res, discount, horizon, base_year=2026):
    """PV of net cash flow + imputed rent, plus PV of net liquidation value of real assets."""
    pv_cash = 0.0
    for row in res["rows"]:
        pv_cash += (row["net_cash"] + row["sale_proceeds"]) / (1 + discount) ** (row["year"] - base_year)
    liq = res["housing_asset"] - res["cap_gains_tax"]
    return pv_cash + liq / (1 + discount) ** (horizon - base_year)


def prop19_value(p, inherit_year=2045, horizon=2065):
    """PV of the property-tax difference between living in A (exclusion kept) and renting A (full reassessment)."""
    pv = 0.0
    rows = []
    for y in range(inherit_year, horizon + 1):
        live = cu_tax(y, inherit_year, "live", p)[0]
        rent = cu_tax(y, inherit_year, "rent", p)[0]
        rows.append(dict(year=y, tax_live=r10(live), tax_rent=r10(rent), saving=r10(rent - live)))
        pv += (rent - live) / (1 + p["A17_discount"]) ** (y - 2026)
    return r10(pv), rows


def breakeven_appreciation(p, inherit_year=2045, horizon=2065, scen="rent"):
    lo, hi = 0.0, 0.15
    target = run("sell", inherit_year, horizon, p)["terminal"]
    for _ in range(60):
        mid = (lo + hi) / 2
        q = dict(p); q["A1_appreciation"] = mid
        if run(scen, inherit_year, horizon, q)["terminal"] < target:
            lo = mid
        else:
            hi = mid
    return hi


# --------------------------------------------------- INHERITANCE TAX ENGINE
def estate_tax_table():
    """Federal estate tax exposure by year of death. California imposes no estate/inheritance tax."""
    rows = []
    for year in (2026, 2030, 2035, 2040, 2045, 2050):
        idx = grow(V["fed_excl_2026"], AS["A2_cpi"], year - 2026)
        rows.append(dict(year=year, exemption=r10(idx), couple_portability=r10(idx * 2)))
    return rows


def estate_exposure(estate_value, exemption):
    return max(0.0, estate_value - exemption) * V["fed_estate_top"]


def main():
    inherit_year, horizon = 2045, 2065
    base = param()
    scen = {k: run(k, inherit_year, horizon, base) for k in ("live", "rent", "sell")}

    grid = []
    for case, (app, inv) in {"low": (0.030, 0.050), "mid": (0.040, 0.060),
                             "high": (0.050, 0.070)}.items():
        for year in (2040, 2045, 2050):
            p = param(A1_appreciation=app, A15_invest_nominal=inv)
            for k in ("live", "rent", "sell"):
                res = run(k, year, year + 20, p)
                grid.append(dict(case=case, inherit_year=year, horizon=year + 20, scenario=k,
                                 terminal=res["terminal"], cum_cash=res["cum_cash"],
                                 economic_value=res["economic_value"],
                                 imputed_rent=res["imputed_rent"],
                                 npv=r10(pv_total(res, p["A17_discount"], year + 20))))

    # year-by-year projection table (base case, "live" and "rent" tax paths)
    proj = []
    for year in range(2026, 2051):
        t = year - 2026
        ct_live, av_live, base_live, exc = cu_tax(year, inherit_year, "live", base)
        ct_rent, av_rent, _, _ = cu_tax(year, inherit_year, "rent", base)
        st, sav = sf_tax(year)
        proj.append(dict(
            year=year,
            cu_market_value=r10(grow(P["A_value_2026"], base["A1_appreciation"], t)),
            cu_assessed_no_transfer=r10(grow(P["A_assessed_2026"], V["prop13_cap"], t)),
            cu_tax_no_transfer=r10(cu_tax(year, 9999, "live", base)[0]),
            cu_assessed_live=r10(av_live), cu_tax_live=r10(ct_live),
            cu_assessed_rent=r10(av_rent), cu_tax_rent=r10(ct_rent),
            sf_market_value=r10(grow(P["B_value_2026"], base["A1_appreciation"], t)),
            sf_assessed=r10(sav), sf_tax=r10(st),
            prop19_exclusion=r10(exclusion_at(year, base)),
            prop19_limit=r10(grow(P["A_assessed_2026"], V["prop13_cap"], inherit_year - 2026)
                             + exclusion_at(inherit_year, base))))
    pv19, pv19_rows = prop19_value(base)
    snapshot = {}
    for k in ("live", "rent", "sell"):
        r = [x for x in scen[k]["rows"] if x["year"] == inherit_year][0]
        snapshot[k] = r

    out = dict(
        meta=dict(inherit_year=inherit_year, horizon_end=horizon, generated_by="scripts/model.py",
                  money_rounding="nearest $10", base_year=2026),
        verified=V, provided=P, assumptions=AS,
        scenarios={k: {kk: vv for kk, vv in v.items() if kk != "rows"} for k, v in scen.items()},
        timeline={k: v["rows"] for k, v in scen.items()},
        projection=proj,
        sensitivity=grid,
        derived=dict(
            prop19_pv_2045_2065=pv19, prop19_rows=pv19_rows,
            breakeven_appreciation_vs_sell=dict(rent=round(breakeven_appreciation(base, scen="rent"), 4),
                                                live=round(breakeven_appreciation(base, scen="live"), 4)),
            snapshot_at_inheritance=snapshot),
        estate=dict(exemption_path=estate_tax_table(),
                    examples=[dict(estate=e,
                                   tax_2026=r10(estate_exposure(e, V["fed_excl_2026"])),
                                   tax_at_death=r10(estate_exposure(
                                       e, grow(V["fed_excl_2026"], AS["A2_cpi"], 2045 - 2026))))
                              for e in (2000000, 5000000, 10000000, 20000000, 30000000, 50000000)]),
    )
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "model.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("wrote data/model.json")


if __name__ == "__main__":
    main()
