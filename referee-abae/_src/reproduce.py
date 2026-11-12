"""Re-derive the numbers a desk publishes, with the reference engine, and report pass/fail.

Inputs that are household-derived ("anchors") are read from the desk's own module at run time. They are used
in memory only. Nothing written to a published page contains a dollar level; pages receive pass/fail flags,
ratios, percentages and differences.
"""
import importlib.util
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import engine as E  # noqa: E402

DESK = ROOT / "desk-b4f"


def load_desk_module():
    path = DESK / "scripts" / "after_tax_model.py"
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location("desk_after_tax_model", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["desk_after_tax_model"] = mod
    spec.loader.exec_module(mod)
    return mod


def load_desk22():
    """Model module of the second published desk (22a32b17), if present in the working tree."""
    path = ROOT / "tools-22a32b17" / "model_22a.py"
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location("desk22_model", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["desk22_model"] = mod
    spec.loader.exec_module(mod)
    return mod


def params_from_22a(m, insurance):
    """Map the second desk's parameters onto the reference engine. Anchors are used in memory only."""
    P = m.DEFAULT_PARAMS
    return E.Params(
        v0=P.a_fmv_2026, taxable0=P.a_fbyv_2026, fixed=P.a_direct_charges_2026, insurance=insurance, water=P.a_water_2026,
        maint=P.a_maint_2026, reserve=0.0, elec_pre=P.a_elec_2026, elec_post=P.a_elec_post_nem_2026_eq, rent0=P.a_rent_2026,
        g=P.home_growth_a, infl=P.inflation, cap=P.prop13_cap, rate=P.a_ad_valorem_rate, allowance0=P.prop19_allowance_2026,
        ag=P.prop19_allowance_growth, nem_sunset=P.a_nem_sunset_year, rent_g=P.a_rent_growth, vac=0.05, mgmt=0.07,
        bldg=P.building_share_a, life=27.5, sell=P.a_sell_cost_rate, r=P.equity_after_tax, t_ord=P.rental_effective_tax_rate,
        t_cg=P.ltcg_combined_rate, t_rec=P.recapture_combined_rate, s121=P.sec121_exclusion, h=25)


def params_from_desk(d):
    a, s, w = d.A, d.STATUTORY_2026_2027, d.ASSUMPTIONS
    return E.Params(
        v0=a.market_value, taxable0=a.taxable_value, fixed=a.fixed_parcel_charges, insurance=a.insurance,
        water=a.water, maint=a.maintenance, reserve=a.reserve, elec_pre=a.electric_pre_nem_sunset,
        elec_post=w["post_nem_electric_2026_real"], rent0=a.gross_rent,
        g=w["home_growth"], infl=w["inflation"], cap=w["prop13_cap"], rate=a.ad_valorem_rate,
        hox=a.homeowners_exemption, allowance0=w["allowance_base"], ag=w["allowance_growth"],
        nem_sunset=w["nem_sunset_year"], rent_g=w["rent_growth_a"], vac=a.vacancy_rate, mgmt=a.management_rate,
        bldg=w["building_share_a"], life=w["depreciation_life"], sell=w["sell_cost_rate"],
        r=w["portfolio_return"], t_ord=w["fed_ord_rate"] + w["niit_rate"] + w["ca_rate"],
        t_cg=w["fed_ltcg_rate"] + w["niit_rate"] + w["ca_rate"],
        t_rec=w["sec1250_fed_rate"] + w["niit_rate"] + w["ca_rate"], s121=s["sec121_mfj"], h=int(w["horizon"]))


class Rows(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows, self._row, self._cell, self._in = [], None, None, False

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._row = []
        elif tag in ("td", "th") and self._row is not None:
            self._cell, self._in = [], True

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._in:
            self._row.append(re.sub(r"\s+", " ", "".join(self._cell)).strip())
            self._in = False
        elif tag == "tr" and self._row is not None:
            self.rows.append(self._row)
            self._row = None

    def handle_data(self, data):
        if self._in:
            self._cell.append(data)


def table_rows(path):
    p = Rows()
    p.feed(Path(path).read_text(encoding="utf-8"))
    return p.rows


def money(s):
    m = re.search(r"([+-]?)\$?(-?\d[\d,]*)", s.replace("−", "-"))
    return None if not m else int(m.group(2).replace(",", "")) * (-1 if m.group(1) == "-" else 1)


def page_text(path):
    s = Path(path).read_text(encoding="utf-8")
    s = re.sub(r"<style.*?</style>", "", s, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s))


def run_all():
    d = load_desk_module()
    out = {"desk_present": d is not None}
    if d is None:
        return out
    p = params_from_desk(d)

    # 1. published 25-year comparison rows vs reference engine
    rows = [r for r in table_rows(DESK / "index.html") if r and re.match(r"^\d{4} → \d{4}$", r[0])]
    chk = []
    for r in rows:
        T = int(r[0][:4])
        x = E.run(p, T)
        pub = {"FMV at transfer": money(r[1]), "S1": money(r[2]), "S2": money(r[3]), "S3": money(r[4]), "S3 - S2": money(r[5])}
        mine = {"FMV at transfer": x["fmv_T"], "S1": x["S1"], "S2": x["S2"], "S3": x["S3"], "S3 - S2": x["S3"] - x["S2"]}
        for k in pub:
            diff = abs(round(mine[k] / 10.0) * 10 - pub[k])
            chk.append({"T": T, "item": k, "diff": diff, "ok": diff <= 10})
    out["rows_found"] = len(rows)
    out["row_checks"] = chk
    out["row_ok"] = sum(c["ok"] for c in chk)
    out["row_max_diff"] = max([c["diff"] for c in chk] or [0])

    # 2. the engine against the desk's own module, unrounded
    desk_vs = []
    for T in (2040, 2045, 2050):
        x, y = E.run(p, T), d.simulate_after_tax(T)
        desk_vs.append(max(abs(x["S1"] - y["s1_wealth"]), abs(x["S2"] - y["s2_wealth"]), abs(x["S3"] - y["s3_wealth"])))
    out["module_max_abs_diff"] = max(desk_vs)

    # 3. break-evens: published statement vs reference engine (both definitions)
    txt = page_text(DESK / "index.html")
    m = re.search(r"below ([\d.]+)% or Property A appreciates faster than ([\d.]+)%/yr for (\d+) consecutive years", txt)
    pub_r, pub_g, pub_n = (float(m.group(1)), float(m.group(2)), int(m.group(3))) if m else (None, None, None)

    def gap_r(r):
        q = E.run(E.with_(p, r=r), 2045)
        return q["S3"] - q["S2"]

    def gap_g(g):
        q = E.run(E.with_(p, g=g), 2045)
        return q["S3"] - q["S2"]

    r_star = E.bisect(gap_r, 0.0, 0.2)
    g_star = E.bisect(gap_g, 0.0, 0.12)
    base = E.run(p, 2045)

    def gap_r_fixed_s2(r):          # the desk's definition: S2 stays priced at the base portfolio return
        return E.run(E.with_(p, r=r), 2045)["S3"] - base["S2"]

    r_star_desk = E.bisect(gap_r_fixed_s2, 0.0, 0.2)
    out["breakeven"] = {"published_r": pub_r, "published_g": pub_g, "published_years": pub_n,
                        "r_star": r_star, "r_star_desk_definition": r_star_desk, "g_star": g_star,
                        "years_2026_to_end_2045": 2045 + p.h - 2026}

    # 4. estate headroom lines (arithmetic only; the 2.2%/yr indexing is the desk's assumption)
    hd = {}
    for T in (2045,):
        fm = E.fmv(p, T)
        excl = 15_480_000 * 1.022 ** (T - 2027)
        hd = {"published_single": money(re.search(r"leaves ~\$([\d,]+) headroom", txt).group(1)) if re.search(r"leaves ~\$([\d,]+) headroom", txt) else None,
              "recomputed_single": excl - fm, "recomputed_halved": excl / 2 - fm}
    out["headroom"] = hd

    # 5. water growth: projection table vs decision model (ratio only)
    a = d.A
    ratio = {n: ((1 + a.water_growth) / (1 + p.infl)) ** n - 1 for n in (19, 44)}
    out["water_gap"] = {"growth_projection": a.water_growth, "growth_decision": p.infl, "ratio_by_2045": ratio[19], "ratio_by_2070": ratio[44]}

    # 6. allowance, statute vs desk
    out["allowance"] = {T: E.allowance(E.with_(p, allowance_mode="statute", g=p.g), T) / E.allowance(p, T) - 1 for T in (2040, 2045, 2050)}

    # 7. terminal-tax conventions, ratios only
    conv = {}
    for t in ("desk", "liquidate_all", "hold_all"):
        q = E.run(E.with_(p, terminal=t), 2045)
        conv[t] = {"S3_over_S2": q["S3"] / q["S2"], "S3_over_S1": q["S3"] / q["S1"], "S2_over_S1": q["S2"] / q["S1"]}
    out["conventions"] = conv

    # 8. marginal-rate sensitivity, ratios only (moderate bracket case; rates are assumptions, see constants page)
    mod = E.run(E.with_(p, t_ord=0.371, t_cg=0.281, t_rec=0.381), 2045)
    out["moderate_rates"] = {"S3_over_S2": mod["S3"] / mod["S2"], "base_S3_over_S2": base["S3"] / base["S2"]}

    # 9. ordering for all three transfer years under the desk's own assumptions
    out["ordering"] = {T: ("S3>S2>S1" if (lambda q: q["S3"] > q["S2"] > q["S1"])(E.run(p, T)) else "other") for T in (2040, 2045, 2050)}
    out["base_S3_over_S2"] = {T: E.run(p, T)["S3"] / E.run(p, T)["S2"] for T in (2040, 2045, 2050)}
    return out


if __name__ == "__main__":
    import json
    res = run_all()
    print(json.dumps(res, indent=1, default=str)[:6000])
