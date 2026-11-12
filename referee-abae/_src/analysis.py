"""All numbers the referee pages show, computed in one place. Output is rates, ratios, counts and pass/fail
flags only. No dollar level derived from household inputs is returned (see test_build.py, which enforces it)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import engine as E  # noqa: E402
import reproduce as RP  # noqa: E402
import regime as G  # noqa: E402
import registry as R  # noqa: E402

T_MAIN = 2045
TS = (2040, 2045, 2050)


def ratios(x):
    return {"s3_s2": x["S3"] / x["S2"], "s3_s1": x["S3"] / x["S1"], "s2_s1": x["S2"] / x["S1"]}


def ordering(r):
    pairs = sorted((("S1", 1.0), ("S2", r["s2_s1"]), ("S3", r["s3_s1"])), key=lambda t: -t[1])
    return " > ".join(n for n, _ in pairs)


def compute():
    out = {"desk_present": False}
    desk = RP.load_desk_module()
    if desk is None:
        return out
    out["desk_present"] = True
    p = RP.params_from_desk(desk)
    rep = RP.run_all()
    out["rep"] = rep

    base = {T: ratios(E.run(p, T)) for T in TS}
    out["base"] = base
    out["base_order"] = {T: ordering(base[T]) for T in TS}

    # --- scenarios at the main transfer year; label, source keys, params override, note
    def sc(label, links, note="", **kw):
        q = E.with_(p, **kw)
        r = ratios(E.run(q, T_MAIN))
        return {"label": label, "links": links, "note": note, "r": r, "order": ordering(r),
                "flip_s3_s2": r["s3_s2"] < 0.995, "flip_s2_s1": r["s2_s1"] < 0.995,
                "at_breakeven": abs(r["s3_s2"] - 1.0) <= 0.005}

    r_pre = p.r / (1 - p.t_cg)          # pre-tax return implied by the desk's after-tax return at its own rate
    rows = [
        sc("Desk assumptions, unchanged", ["rp2635", "ir2026133"], "Reference row."),
        sc("Tax on the reinvested portfolio's embedded gains also charged at the horizon (upper-bound stress)", ["tc409", "p551"],
           "Applies if the after-tax return is net of yearly tax only, not of tax due on unrealised gains.", terminal="liquidate_all"),
        sc("Nothing sold at the horizon: no terminal tax on any path", ["p551"],
           "Heir's own heirs would receive a new basis; shows the size of the terminal-tax effect.", terminal="hold_all"),
        sc("Moderate marginal rates (37.1% ordinary, 28.1% capital gain, 38.1% section 1250); return held at the desk's value", ["rp2635", "ftb26"],
           "Rates are assumptions; this row changes taxes on rent and on sale only.", t_ord=0.371, t_cg=0.281, t_rec=0.381),
        sc("Moderate marginal rates, with the after-tax return re-derived from the same pre-tax return", ["rp2635", "ftb26"],
           "Consistent version of the previous row.", t_ord=0.371, t_cg=0.281, t_rec=0.381, r=r_pre * (1 - 0.281)),
        sc("Insurance cost halved", ["cdi", "cdi_eq"], "CDI averages: statewide homeowners $2,339.99; California average $1,571.", insurance=p.insurance * 0.5),
        sc("Insurance at the CDI 2025 statewide homeowners average", ["cdi_eq"], "", insurance=2340.0),
        sc("Rent 20% lower", ["hud_fmr"], "Rent is an unverified assumption (desk flag F05).", rent0=p.rent0 * 0.8),
        sc("Rent 20% higher", ["hud_fmr"], "", rent0=p.rent0 * 1.2),
        sc("Market value 27% below trend at transfer, growth resumes after", ["fred_a", "fhfa"],
           "Local metro index fell 27% from 2006 Q3 to 2012 Q1 (see baselines).", v0=p.v0 * 0.73),
        sc("Reinvestment in Treasuries only: 4.4% before tax at the desk's ordinary rate", ["cbo", "rp2635"],
           "CBO 10-year yield 4.4% for 2031-2036.", r=0.044 * (1 - p.t_ord)),
        sc("Prop 19 relief not obtained (homeowners' exemption not filed within one year)", ["prop19", "hox"],
           "Occupy path is then assessed at full market value.", prop19=False),
        sc("Prop 19 allowance projected by the statute's own rule (one year of price change every other February)", ["lta25009"],
           "", allowance_mode="statute"),
        sc("Home-price growth 2% a year", ["fhfa"], "Below every historical 25-year window in baselines.", g=0.02),
        sc("Home-price growth 6.1% a year", ["fhfa"], "The desk's published break-even growth.", g=0.061),
        sc("Water cost grows 3.0% a year (the desk's projection-table rate) instead of 2.5%", ["cbo", "ssa"],
           "Both rates exceed the CBO and SSA baseline for consumer prices.", water_g=0.03),
        sc("Property-tax rate 0.1 point higher", ["tax_collector"], "Rate for A is not verified (flag F-A2).", rate=p.rate + 0.001),
        sc("Property-tax rate 0.1 point lower", ["tax_collector"], "", rate=p.rate - 0.001),
    ]
    out["scen"] = rows

    # --- ranges over the three windows for the headline conclusion
    out["ranges"] = {k: (min(base[T][k] for T in TS), max(base[T][k] for T in TS)) for k in ("s3_s2", "s3_s1", "s2_s1")}

    # --- indifference value of living in A, as a yield on market value, compared with market rent yield
    x = E.run(p, T_MAIN)
    h = p.h
    ann = sum((1 + p.infl) ** i * (1 + p.r) ** (h - i) for i in range(h))
    c0_vs_sell = (x["S3"] - x["S1"]) / ann
    c0_vs_rent = (x["S2"] - x["S1"]) / ann
    out["indiff"] = {"vs_sell": c0_vs_sell / x["fmv_T"], "vs_rent": c0_vs_rent / x["fmv_T"], "rent_yield": x["rent_y1"] / x["fmv_T"]}

    # --- historical windows
    data = G.load()
    ws = G.windows(data, p)
    out["windows"] = ws
    out["win_summary"] = G.summarize(ws)
    out["win_where"] = data["where"]
    out["win_commit"] = G.data_commit()
    out["win_s3_wins_full_drag"] = sum(1 for w in ws if w["eq_total"] * (1 - p.t_cg) > w["r_star"])
    out["win_home_above_6_1"] = sum(1 for w in ws if w["home"] > 0.061)
    out["win_bond_wins"] = sum(1 for w in ws if w["bond_pre"] * (1 - p.t_ord) > w["r_star"])
    out["win_bond_range"] = (min(w["bond_pre"] for w in ws), max(w["bond_pre"] for w in ws))
    out["desk_g"] = p.g
    out["desk_r"] = p.r
    out["equity_check"] = G.equity_crosscheck(data)
    out["drawdowns"] = G.drawdowns()
    out["factors"] = {"n": len(data["factors"]), "below_1_02": sum(1 for _, _, f in data["factors"] if f < 1.02),
                      "min": min(f for _, _, f in data["factors"])}
    # long-run local index growth, Q4 1976 to Q4 2025 (both read on the official page)
    a = data["hpi_a"]
    out["a_cagr_long"] = (a[2025] / a[1976]) ** (1 / 49) - 1
    out["tax_rates"] = {"ord": p.t_ord, "cg": p.t_cg, "rec": p.t_rec}

    # --- historical after-tax equity return (all return taxed every year at the desk's capital-gain rate)
    at = sorted(w["eq_total"] * (1 - p.t_cg) for w in ws)
    out["eq_after_tax"] = {"min": at[0], "median": at[len(at) // 2], "max": at[-1],
                           "below_desk": sum(1 for v in at if v < p.r), "below_22a": None}

    # --- second desk (22a32b17): reproduce with the same engine; explain the gap to the first desk
    m22 = RP.load_desk22()
    if m22 is not None:
        P22 = m22.DEFAULT_PARAMS
        p22h, p22d = RP.params_from_22a(m22, P22.a_ins_ho3_2026), RP.params_from_22a(m22, P22.a_ins_dp3_2026)
        rep22 = []
        for T in TS:
            theirs = m22.evaluate_strategies(transfer_year=T, horizon_years=25)
            mine_s3 = E.run(p22h, T)["S3"]
            mine_s2 = E.run(p22d, T)["S2"]
            mine_s1 = E.run(p22h, T)["S1"]
            rep22.append({"T": T, "s3": mine_s3 / theirs["S3a"]["liquidated_wealth"] - 1, "s2": mine_s2 / theirs["S2"]["liquidated_wealth"] - 1,
                          "s1": mine_s1 / theirs["S1a"]["liquidated_wealth"] - 1,
                          "their_s3_s2": theirs["S3a"]["liquidated_wealth"] / theirs["S2"]["liquidated_wealth"],
                          "their_s2_s1": theirs["S2"]["liquidated_wealth"] / theirs["S1a"]["liquidated_wealth"]})
        out["rep22"] = rep22
        base2 = ratios(E.run(p, T_MAIN))
        groups = [
            ("Home-price growth", "4.0% -> 4.2% a year", dict(g=P22.home_growth_a)),
            ("After-tax return on reinvested proceeds", "4.5% -> 5.6% a year", dict(r=P22.equity_after_tax)),
            ("Selling cost", "6.0% -> 5.5%", dict(sell=P22.a_sell_cost_rate)),
            ("Tax rates on rent and depreciation recapture", "52.1% / 42.1% -> 42.0% / 38.3%", dict(t_ord=P22.rental_effective_tax_rate, t_rec=P22.recapture_combined_rate)),
            ("Prop 19 allowance growth", "2.0% -> 2.2% a year", dict(ag=P22.prop19_allowance_growth)),
            ("Rent level and vacancy plus management", "rent about 4% higher; 13% -> 12%", dict(rent0=P22.a_rent_2026, vac=0.05, mgmt=0.07)),
            ("Insurance, maintenance, solar-credit end year", "insurance 27% higher on the rental policy; maintenance 3% higher; 2043 -> 2038", dict(insurance=P22.a_ins_dp3_2026, maint=P22.a_maint_2026, reserve=0.0, nem_sunset=P22.a_nem_sunset_year, elec_post=P22.a_elec_post_nem_2026_eq)),
            ("Building share of basis for depreciation", "40% -> 65%", dict(bldg=P22.building_share_a)),
            ("Home-sale exclusion on exit", "married $500,000 -> single $250,000", dict(s121=P22.sec121_exclusion)),
            ("Tax rate and parcel charges", "1.18% -> 1.19%; charges about 70% higher", dict(rate=P22.a_ad_valorem_rate, fixed=P22.a_direct_charges_2026)),
        ]
        grows, allkw = [], {}
        for name, change, kw in groups:
            r = ratios(E.run(E.with_(p, **kw), T_MAIN))
            grows.append({"name": name, "change": change, "s3_s2_pct": r["s3_s2"] / base2["s3_s2"] - 1, "s3_s2": r["s3_s2"]})
            allkw.update(kw)
        rall = ratios(E.run(E.with_(p, **allkw), T_MAIN))
        out["groups22"] = grows
        out["all22"] = rall
        out["their22"] = rep22[1]
        at22 = P22.equity_after_tax
        out["eq_after_tax"]["below_22a"] = sum(1 for v in at if v < at22)
        out["r22"] = at22
    return out


if __name__ == "__main__":
    import json
    r = compute()
    for s in r["scen"]:
        print("%-100s %.3f %.3f %.3f %s %s %s" % (s["label"][:100], s["r"]["s3_s2"], s["r"]["s3_s1"], s["r"]["s2_s1"], s["order"],
                                                 "FLIP32" if s["flip_s3_s2"] else "", "FLIP21" if s["flip_s2_s1"] else ""))
    print(r["ranges"])
    print(r["indiff"])
    print(r["win_summary"]["n"], r["win_s3_wins_full_drag"], r["win_home_above_6_1"], r["a_cagr_long"], r["equity_check"], r["factors"])
