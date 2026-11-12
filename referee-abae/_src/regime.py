"""Historical baselines and rolling 25-year windows from the official series transcribed by session 3a49d618.

Data: swan-3a49/data/*.csv (working tree after PR #44 merges, otherwise read from the session branch with
`git show`). Those CSVs are transcriptions of FHFA / BLS / Federal Reserve series (served by FRED) and of
Economic Report of the President 2026 Tables B-55 and B-56. This module re-derives nothing from memory.

Everything this module returns is a rate or a ratio. No dollar amount appears.
"""
import csv
import io
import statistics as st
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import engine as E  # noqa: E402

BRANCH = "origin/arena/3a49d618-tino5"
FILES = ("fred_hpi_annual.csv", "fred_cpi_rates_annual.csv", "erp2026_sp500.csv", "boe_lta2026_002_factors.csv")


def _read(name):
    local = ROOT / "swan-3a49" / "data" / name
    if local.exists():
        return local.read_text(encoding="utf-8"), "working tree (merged)"
    txt = subprocess.check_output(["git", "show", f"{BRANCH}:swan-3a49/data/{name}"], cwd=ROOT, text=True)
    return txt, f"branch {BRANCH.split('/', 1)[1]} (not yet merged)"


def load():
    raw, where = {}, None
    for f in FILES:
        raw[f], where = _read(f)
    rows = {f: list(csv.DictReader(io.StringIO(t))) for f, t in raw.items()}
    hpi_a = {int(r["observation_date"][:4]): float(r["ATNHPIUS41940Q"]) for r in rows[FILES[0]] if r["ATNHPIUS41940Q"]}
    hpi_b = {int(r["observation_date"][:4]): float(r["ATNHPIUS41884Q"]) for r in rows[FILES[0]] if r["ATNHPIUS41884Q"]}
    hpi_ca = {int(r["observation_date"][:4]): float(r["CASTHPI"]) for r in rows[FILES[0]] if r["CASTHPI"]}
    cpi = {int(r["observation_date"][:4]): float(r["CPIAUCNS"]) for r in rows[FILES[1]] if r["CPIAUCNS"]}
    gs10 = {int(r["observation_date"][:4]): float(r["GS10"]) for r in rows[FILES[1]] if r["GS10"]}
    sp = {int(r["year"]): (float(r["sp500_end_of_year"]), float(r["dividend_price_ratio_pct"])) for r in rows[FILES[2]]}
    factors = [(r["roll_year"], float(r["ccpi_pct_change"]), float(r["factor"])) for r in rows[FILES[3]]]
    return {"where": where, "hpi_a": hpi_a, "hpi_b": hpi_b, "hpi_ca": hpi_ca, "cpi": cpi, "gs10": gs10, "sp": sp,
            "factors": factors}


def cagr(d, a, b):
    return (d[b] / d[a]) ** (1.0 / (b - a)) - 1.0


def equity_total(sp, s, e):
    """Approximate total return: S&P price CAGR plus the mean dividend-price ratio over the window."""
    price = (sp[e][0] / sp[s][0]) ** (1.0 / (e - s)) - 1.0
    div = st.mean(sp[y][1] for y in range(s + 1, e + 1)) / 100.0
    return price, price + div


def windows(data, p, h=25):
    """Rolling windows. For each: home growth, inflation, equity return, break-even portfolio return, tolerable tax drag."""
    out = []
    for s in range(min(data["hpi_a"]), max(data["hpi_a"]) - h + 1):
        e = s + h
        if e not in data["hpi_a"] or s not in data["cpi"] or e not in data["cpi"] or s not in data["sp"] or e not in data["sp"]:
            continue
        g, pi = cagr(data["hpi_a"], s, e), cagr(data["cpi"], s, e)
        price, tot = equity_total(data["sp"], s, e)
        bond = st.mean(data["gs10"][y] for y in range(s + 1, e + 1)) / 100.0
        q = E.with_(p, g=g, infl=pi, cap=min(0.02, pi), rent_g=pi + 0.005, h=h)

        def gap(r):
            x = E.run(E.with_(q, r=r), 2026)
            return x["S3"] - x["S2"]

        r_star = E.bisect(gap, -0.05, 0.25)
        out.append({"start": s, "end": e, "home": g, "cpi": pi, "eq_price": price, "eq_total": tot, "bond_pre": bond,
                    "r_star": r_star, "tax_drag_tolerated": 1.0 - r_star / tot})
    return out


def summarize(ws):
    def stats(k):
        v = [w[k] for w in ws]
        return {"min": min(v), "median": st.median(v), "max": max(v)}
    out = {"n": len(ws)}
    for k in ("home", "cpi", "eq_price", "eq_total", "r_star", "tax_drag_tolerated"):
        out[k] = stats(k)
    return out


def data_commit():
    local = ROOT / "swan-3a49" / "data" / FILES[0]
    if local.exists():
        return subprocess.run(["git", "log", "-1", "--format=%h", "--", "swan-3a49/data"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return subprocess.run(["git", "rev-parse", "--short", BRANCH], cwd=ROOT, capture_output=True, text=True).stdout.strip()


def equity_crosscheck(data):
    """ERP-derived approximate total return, end-1987 to end-2025, to set beside the TSP C Fund figure (since 1988)."""
    s, e = 1987, 2025
    price, tot = equity_total(data["sp"], s, e)
    return {"start": s, "end": e, "price": price, "total": tot}


# Verbatim lines read from the FRED data page for series ATNHPIUS41940Q on 2026-11-12 (index 1995Q1 = 100).
A_LINES = {"1981-10-01": 52.27, "1982-07-01": 46.14, "1989-10-01": 114.25, "1994-07-01": 99.94,
            "2006-07-01": 320.14, "2012-01-01": 234.33, "2022-04-01": 531.62, "2023-01-01": 505.82,
            "2026-01-01": 566.96, "2026-04-01": 558.75}
DRAWDOWNS = [("1981-10-01", "1982-07-01"), ("1989-10-01", "1994-07-01"), ("2006-07-01", "2012-01-01"), ("2022-04-01", "2023-01-01"),
             ("2026-01-01", "2026-04-01")]


def drawdowns():
    return [{"peak": a, "trough": b, "change": A_LINES[b] / A_LINES[a] - 1.0} for a, b in DRAWDOWNS]


if __name__ == "__main__":
    import json
    from reproduce import load_desk_module, params_from_desk
    d = load()
    p = params_from_desk(load_desk_module())
    ws = windows(d, p)
    print(d["where"], len(ws))
    print(json.dumps(summarize(ws), indent=1))
    for w in ws[:3] + ws[-3:]:
        print({k: round(v, 4) if isinstance(v, float) else v for k, v in w.items()})
    print([ (x['peak'], x['trough'], round(x['change'],3)) for x in drawdowns()])
    over = sum(1 for w in ws if w["home"] > 0.0610)
    print("windows with home growth above 6.10%:", over, "of", len(ws))
    print("min factor in BOE table:", min(f for _, _, f in d["factors"]), "max:", max(f for _, _, f in d["factors"]), "rows", len(d["factors"]))
    below = [(y, c, f) for y, c, f in d["factors"] if c < 2.0]
    print("roll years with CCPI below 2%:", below)
