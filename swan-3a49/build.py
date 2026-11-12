#!/usr/bin/env python3
"""Uneven-economy replay (task 3a4/S, session arena-3a49d618).

Reads the four official series files in data/, replays the 49 recorded years 1977-2025 over
2027-2075 in every rotation, and writes the HTML pages in this directory.

No household input is used anywhere. Results are scale-free (per $1 or per $1,000,000) or are
shown for round reference home sizes. Money is rounded to $10 at display time; statutory amounts
are shown as published and marked.

Run from the repository root:  python3 swan-3a49/build.py
"""
import csv
import html
import re
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
RETRIEVED = "12 November 2026"

# ----------------------------------------------------------------------------- load
def read(name):
    with open(DATA / name, newline="") as fh:
        return list(csv.DictReader(fh))

hpi = {int(r["observation_date"][:4]): r for r in read("fred_hpi_annual.csv")}
cpi = {int(r["observation_date"][:4]): r for r in read("fred_cpi_rates_annual.csv")}
sp = {int(r["year"]): r for r in read("erp2026_sp500.csv")}
boe = {int(r["roll_year"][:4]): r for r in read("boe_lta2026_002_factors.csv")}

def f(table, year, col):
    v = table[year][col]
    if v == "":
        raise ValueError(f"blank {col} {year}")
    return float(v)

H0, H1 = 1977, 2025                      # first and last replayed historical year
HIST = list(range(H0, H1 + 1))
N = len(HIST)                            # 49
assert N == 49

chg = {}
for h in HIST:
    chg[h] = {
        "home_a": f(hpi, h, "ATNHPIUS41940Q") / f(hpi, h - 1, "ATNHPIUS41940Q") - 1,
        "home_b": f(hpi, h, "ATNHPIUS41884Q") / f(hpi, h - 1, "ATNHPIUS41884Q") - 1,
        "home_ca": f(hpi, h, "CASTHPI") / f(hpi, h - 1, "CASTHPI") - 1,
        "cpi": f(cpi, h, "CPIAUCNS") / f(cpi, h - 1, "CPIAUCNS") - 1,
        "cpi_bay": f(cpi, h, "CUURA422SA0") / f(cpi, h - 1, "CUURA422SA0") - 1,
        "rent_bay": f(cpi, h, "CUURA422SEHA") / f(cpi, h - 1, "CUURA422SEHA") - 1,
        "gs10": f(cpi, h, "GS10") / 100,
        "bill": f(cpi, h, "TB3MS") / 100,
        "stock_price": f(sp, h, "sp500_end_of_year") / f(sp, h - 1, "sp500_end_of_year") - 1,
        "div": f(sp, h, "dividend_price_ratio_pct") / 100,
        "p13": f(boe, h, "factor"),
        "ccpi": f(boe, h, "ccpi_pct_change") / 100,
    }
    chg[h]["stock"] = chg[h]["stock_price"] + chg[h]["div"]

# checks on the transcription (figures quoted in the sources themselves)
assert abs(f(boe, 2010, "factor") - 0.99763) < 1e-9 and abs(f(boe, 1983, "factor") - 1.01) < 1e-9
for y in (2000, 2001, 2002, 2003):       # years printed in both ERP tables
    assert sp[y]["erp2026_table"] == "B-55"
for h in HIST:                           # factor = min(2%, CCPI change) except the 1983-84 row, which BOE lists as 1%
    exp = min(1.02, 1 + chg[h]["ccpi"])
    assert abs(exp - chg[h]["p13"]) < 6e-5 or h == 1983, h

START, END = 2026, 2075
YEARS = list(range(START + 1, END + 1))  # 2027..2075, 49 projected years
assert len(YEARS) == N
TRANSFERS = (2040, 2045, 2050)
HOLD = 25
ALLOW_2026 = 1_044_586                   # BOE LTA 2025/009, transfers 16 Feb 2025 - 15 Feb 2027
EXCL_2026 = 15_000_000                   # IRC 2010(c)(3) as amended by P.L. 119-21 sec. 70106
SIZES = (1_000_000, 2_000_000, 3_000_000, 4_000_000, 5_000_000)

def hist_year(start, t):
    """Historical year replayed in projected year t on the path that begins with `start`."""
    return H0 + ((start - H0) + (t - YEARS[0])) % N

def path(start):
    p = {"start": start, "h": {}, "home_a": {START: 1.0}, "home_b": {START: 1.0}, "cpi": {START: 1.0},
         "bay": {START: 1.0}, "rent": {START: 1.0}, "allowed": {START: 1.0}, "fb": {START: 1.0},
         "stock": {START: 1.0}, "bill": {START: 1.0}, "allow": {START: float(ALLOW_2026)},
         "excl": {START: float(EXCL_2026)}}
    for t in YEARS:
        h = hist_year(start, t)
        c = chg[h]
        p["h"][t] = h
        p["home_a"][t] = p["home_a"][t - 1] * (1 + c["home_a"])
        p["home_b"][t] = p["home_b"][t - 1] * (1 + c["home_b"])
        p["cpi"][t] = p["cpi"][t - 1] * (1 + c["cpi"])
        p["bay"][t] = p["bay"][t - 1] * (1 + c["cpi_bay"])
        p["rent"][t] = p["rent"][t - 1] * (1 + c["rent_bay"])
        # rent-controlled unit: 60% of the area CPI change (sf.gov); no ceiling or floor applied (flag S08)
        p["allowed"][t] = p["allowed"][t - 1] * (1 + 0.6 * c["cpi_bay"])
        p["fb"][t] = p["fb"][t - 1] * c["p13"]
        p["stock"][t] = p["stock"][t - 1] * (1 + c["stock"])
        p["bill"][t] = p["bill"][t - 1] * (1 + c["bill"])
        # Prop 19 amount: adjusted on 16 February of every other year (2027, 2029, ...) by the
        # California HPI change for the prior calendar year. 2026 is not replayed, so no 2027 step.
        a = p["allow"][t - 1]
        if t % 2 == 1 and t - 1 >= YEARS[0]:
            a *= 1 + chg[p["h"][t - 1]]["home_ca"]
        p["allow"][t] = a
        # Estate exclusion: $15,000,000 for 2026; later years indexed with a one-year lag.
        p["excl"][t] = EXCL_2026 * p["cpi"][t - 1]
    return p

PATHS = {s: path(s) for s in HIST}

def wraps(start, t_from, t_to):
    """True when the replayed years t_from+1..t_to cross the artificial 2025 -> 1977 joint."""
    hs = [hist_year(start, t) for t in range(t_from + 1, t_to + 1)]
    return any(b < a for a, b in zip(hs, hs[1:]))

# ----------------------------------------------------------------------------- post-transfer windows
def window(start, T):
    """25 years after a transfer at the end of year T, per $1 of home value at the transfer."""
    p = PATHS[start]
    end = T + HOLD
    v = lambda t: p["home_a"][t] / p["home_a"][T]
    out = {"start": start, "first": hist_year(start, T + 1), "last": hist_year(start, end),
           "wrap": wraps(start, T, end), "home": v(end), "cpi": p["cpi"][end] / p["cpi"][T],
           "stock": p["stock"][end] / p["stock"][T], "bill": p["bill"][end] / p["bill"][T]}
    for key in ("stock", "bill"):
        g = lambda a, b: p[key][b] / p[key][a]
        denom = sum(v(t - 1) * g(t, end) for t in range(T + 1, end + 1))
        out["be_" + key] = (g(T, end) - v(end)) / denom
    # property tax if the heir does not occupy: new base year value = market value at transfer
    # the first roll after the transfer carries the new base year value itself; factors apply after that
    fb, total, flat, decline = 1.0, 0.0, 0.0, 0
    for k, t in enumerate(range(T + 1, end + 1)):
        if k:
            fb *= chg[p["h"][t]]["p13"]
        market = v(t - 1)                # lien date 1 January of year t
        enrolled = min(fb, market)
        decline += enrolled < fb - 1e-12
        total += enrolled * 0.01
        flat += 1.02 ** k * 0.01
    out.update(tax25=total, tax25_flat=flat, decline_years=decline)
    low = min(v(t) for t in range(T, end + 1))
    out["trough"] = low
    return out

# the set of 25-year windows is the same for every transfer year (rotations), so compute once
WIN = [window(s, 2050) for s in HIST]
WIN_ACTUAL = [w for w in WIN if not w["wrap"]]

# ----------------------------------------------------------------------------- helpers
def r10(x):
    return int(round(x / 10.0)) * 10

def money(x):
    return ("-" if x < 0 else "") + f"${abs(r10(x)):,}"

def stat(x):
    return f'<span class="stat">${x:,}</span>'

def pct(x, d=1):
    return f"{x * 100:.{d}f}%"

def mult(x):
    return f"{x:.2f}×"

def med(xs):
    return statistics.median(xs)

def spread(xs, fmt):
    return f'{fmt(med(xs))} <span class="rng">({fmt(min(xs))} to {fmt(max(xs))})</span>'

def a(url, label):
    return f'<a href="{html.escape(url, quote=True)}">{html.escape(label)}</a>'

U = {
    "hpi": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=ATNHPIUS41940Q,ATNHPIUS41884Q,CASTHPI&fq=Annual,Annual,Annual&fam=eop,eop,eop",
    "cpi": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCNS,CUURA422SA0,CUURA422SEHA,GS10,TB3MS&fq=Annual,Annual,Annual,Annual,Annual&fam=avg,avg,avg,avg,avg",
    "b55": "https://www.govinfo.gov/content/pkg/ERP-2026/pdf/ERP-2026-table55.pdf",
    "b56": "https://www.govinfo.gov/content/pkg/ERP-2026/pdf/ERP-2026-table56.pdf",
    "lta26": "https://www.boe.ca.gov/proptaxes/pdf/lta26002.pdf",
    "lta25": "https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf",
    "pub801": "https://www.boe.ca.gov/pdf/pub801.pdf",
    "prop8": "https://www.boe.ca.gov/proptaxes/decline-in-value/",
    "hox": "https://www.boe.ca.gov/proptaxes/homeowners_exemption.htm",
    "plaw": "https://www.govinfo.gov/content/pkg/PLAW-119publ21/html/PLAW-119publ21.htm",
    "irs_estate": "https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax",
    "irs_basis": "https://www.irs.gov/faqs/interest-dividends-other-types-of-income/gifts-inheritances/gifts-inheritances",
    "cbo": "https://www.cbo.gov/system/files/2026-02/61882-Executive-Summary.pdf",
    "ssa": "https://www.ssa.gov/oact/tr/2026/II_C_assump.html",
    "sfrent": "https://www.sf.gov/learn-about-rent-increases-san-francisco",
    "sftax": "https://sftreasurer.org/property/secured-property-taxes",
}
S = {
    "hpi": a(U["hpi"], "FHFA house price index (FRED)"),
    "cpi": a(U["cpi"], "BLS CPI and Treasury rates (FRED)"),
    "erp": a(U["b55"], "ERP 2026 B-55") + " · " + a(U["b56"], "B-56"),
    "lta26": a(U["lta26"], "BOE LTA 2026/002"),
    "lta25": a(U["lta25"], "BOE LTA 2025/009"),
    "pub801": a(U["pub801"], "BOE Prop 19 fact sheet"),
    "prop8": a(U["prop8"], "BOE decline in value"),
    "hox": a(U["hox"], "BOE homeowners' exemption"),
    "plaw": a(U["plaw"], "P.L. 119-21 sec. 70106"),
    "irs_estate": a(U["irs_estate"], "IRS estate tax"),
    "irs_basis": a(U["irs_basis"], "IRS inherited property FAQ"),
    "cbo": a(U["cbo"], "CBO outlook 2026-2036"),
    "ssa": a(U["ssa"], "Social Security Trustees 2026"),
    "sfrent": a(U["sfrent"], "SF Rent Board"),
    "sftax": a(U["sftax"], "SF Treasurer"),
}

def table(head, rows, cls=""):
    """Every body row must end with a cell that holds at least one official link."""
    out = [f'<div class="scroll"><table class="{cls}"><thead><tr>']
    out += [f"<th>{h}</th>" for h in head]
    out.append("</tr></thead><tbody>")
    for r in rows:
        assert len(r) == len(head), (head, r)
        assert "href=" in r[-1], f"row without source link: {r}"
        out.append("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)

NAV = [("index.html", "Overview"), ("replay.html", "Replay results"), ("paths.html", "Year by year"),
       ("baseline.html", "Baseline"), ("sources.html", "Sources and method"), ("flagged.html", "Flagged for review")]

CSS = """
:root{--ink:#1c2430;--mute:#5a6675;--line:#d9dee5;--bg:#f6f7f9;--card:#fff;--accent:#1f5f8b;--warn:#8a4b00;--warnbg:#fff6e5}
*{box-sizing:border-box}
body{margin:0;font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--ink);background:var(--bg)}
header,main,footer{max-width:1080px;margin:0 auto;padding:0 20px}
header{padding-top:22px}
.kicker{font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:var(--mute)}
h1{font-size:28px;line-height:1.2;margin:6px 0 10px}
h2{font-size:20px;margin:34px 0 8px}
h3{font-size:16px;margin:22px 0 6px}
p{margin:8px 0}
.lede{font-size:17px;max-width:70ch}
nav{display:flex;flex-wrap:wrap;gap:6px 8px;margin:14px 0 6px;padding:10px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
nav a{padding:5px 10px;border-radius:6px;text-decoration:none;color:var(--accent);font-size:14px}
nav a.on{background:var(--accent);color:#fff}
nav a.back{margin-left:auto;color:var(--mute)}
a{color:var(--accent)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin:14px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.card .big{font-size:26px;font-weight:650;line-height:1.15;margin:2px 0 4px}
.card .lab{font-size:13px;color:var(--mute)}
.card .src{font-size:12px;margin-top:6px}
.note{background:var(--warnbg);border-left:4px solid #d08a1f;padding:10px 14px;border-radius:0 8px 8px 0;margin:14px 0;color:#4a3200}
.plain{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 16px;margin:14px 0}
.scroll{overflow-x:auto;margin:10px 0 6px;border:1px solid var(--line);border-radius:10px;background:var(--card)}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{padding:7px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{background:#eef1f5;font-weight:600;font-size:13px}
tbody tr:last-child td{border-bottom:0}
table.num td:not(:first-child):not(:last-child){text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
table.num th:not(:first-child):not(:last-child){text-align:right}
td:last-child{font-size:12.5px;min-width:150px}
.rng{color:var(--mute);font-size:12.5px;white-space:nowrap}
.neg{color:#a11}
.stat{white-space:nowrap}
.small{font-size:13px;color:var(--mute)}
ul{padding-left:20px;margin:8px 0}
li{margin:4px 0}
footer{margin-top:40px;padding-top:14px;padding-bottom:40px;border-top:1px solid var(--line);font-size:13px;color:var(--mute)}
"""

def page(name, title, body):
    on = ' class="on"'
    nav = "".join(f'<a href="{h}"{on if h == name else ""}>{t}</a>' for h, t in NAV)
    nav += '<a class="back" href="../public-safe/index.html">Main dashboard</a>'
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{title} · Uneven-economy replay</title>
<style>{CSS}</style></head><body>
<header><div class="kicker">Estate decision desk · black-swan section · public · anonymized</div>
<h1>{title}</h1><nav>{nav}</nav></header>
<main>
{body}
</main>
<footer><p><strong>Not advice.</strong> This is arithmetic on published historical series. It is not a forecast and not legal, tax or investment advice.</p>
<p><strong>Privacy.</strong> No household figure is used or shown. Results are per dollar, per $1,000,000, or for round reference home sizes. Property A is the inherited home; Property B is the home already owned.</p>
<p>Sources retrieved {RETRIEVED}. Built by <code>swan-3a49/build.py</code> from the series files listed under <a href="sources.html">Sources and method</a>.</p></footer>
</body></html>
"""
    (HERE / name).write_text(doc)

# ----------------------------------------------------------------------------- derived results
def at(T, key, sub=None):
    return [PATHS[s][key][T] for s in HIST]

def actual_at(T):
    return [s for s in HIST if not wraps(s, START, T)]

def span(w):
    return f"{w['first']} to {H1}, then {H0} to {w['last']}" if w["wrap"] else f"{w['first']} to {w['last']}"

worst = lambda xs, k: min(xs, key=lambda w: w[k])
best = lambda xs, k: max(xs, key=lambda w: w[k])

def episodes(col, table_, label, src):
    """Peak-to-trough declines of at least 10% in year-end levels."""
    ys = sorted(y for y in table_ if 1976 <= y <= 2025 and table_[y][col] != "")
    rows, peak_y = [], ys[0]
    i = 0
    while i < len(ys):
        y = ys[i]
        if float(table_[y][col]) >= float(table_[peak_y][col]):
            peak_y = y
            i += 1
            continue
        # in a decline: find the trough before the peak level is regained
        j, trough_y = i, y
        while j < len(ys) and float(table_[ys[j]][col]) < float(table_[peak_y][col]):
            if float(table_[ys[j]][col]) < float(table_[trough_y][col]):
                trough_y = ys[j]
            j += 1
        drop = float(table_[trough_y][col]) / float(table_[peak_y][col]) - 1
        regained = ys[j] if j < len(ys) else None
        if drop <= -0.10:
            rows.append([label, f"end of {peak_y}", f"end of {trough_y}", f'<span class="neg">{pct(drop)}</span>',
                         f"{trough_y - peak_y}", f"{regained}" if regained else "not by end of 2025",
                         f"{regained - peak_y}" if regained else "", src])
        if regained is None:
            break
        peak_y = regained
        i = j
    return rows

# ----------------------------------------------------------------------------- pages
def build_index():
    n_act = len(WIN_ACTUAL)
    stock_beats = sum(w["stock"] > w["home"] for w in WIN_ACTUAL)
    bill_beats = sum(w["bill"] > w["home"] for w in WIN_ACTUAL)
    be_s = [w["be_stock"] for w in WIN_ACTUAL]
    be_b = [w["be_bill"] for w in WIN_ACTUAL]
    v45 = at(2045, "home_a")
    low45 = min(HIST, key=lambda s: PATHS[s]["home_a"][2045])
    hi45 = max(HIST, key=lambda s: PATHS[s]["home_a"][2045])
    dec = [w["decline_years"] for w in WIN]
    real45 = [PATHS[s]["home_a"][2045] / PATHS[s]["cpi"][2045] for s in HIST]
    stock_all = (PATHS[H0]["stock"][END]) ** (1 / N) - 1
    cards = [
        ("49 paths", "The same 49 recorded years (1977 to 2025), replayed over 2027 to 2075 starting from each year in turn. Only the order changes.", S["hpi"]),
        (f"{mult(min(v45))} to {mult(max(v45))}", f"Range of the home-price multiple for Property A's metro area between 2026 and 2045. Median {mult(med(v45))}. A constant-rate model gives one number.", S["hpi"]),
        (f"{stock_beats} of {n_act}", f"Recorded 25-year periods in which stocks with dividends ended ahead of metro home prices alone (before rent, costs and tax). Treasury bills ended ahead in {bill_beats} of {n_act}.", S["erp"]),
        (f"{pct(med(be_s))} a year", f"Median net cash yield the house would have had to pay, after every cost and tax, to keep up with stocks. Range {pct(min(be_s))} to {pct(max(be_s))}.", S["erp"]),
        (f"{sum(d > 0 for d in dec)} of {N}", "Paths in which a home reassessed at market value on transfer was later worth less than its taxable value on at least one 1 January, so the lower market value should be enrolled.", S["prop8"]),
        (f"{sum(1 for h in HIST if chg[h]['p13'] < 1.02)} of {N} years", "Recorded years in which the Prop 13 factor was below the 2% ceiling. In one year it was negative.", S["lta26"]),
    ]
    body = f"""<p class="lede">The main dashboard tests a few scenarios that each hold one growth rate for decades. Real economies do not do that. This section takes what actually happened to prices, house values, rents, interest rates and stocks in each year from 1977 to 2025 and replays those years, in order, over the next half century.</p>
<div class="note"><strong>What this is not.</strong> It is not a forecast, and it does not say what Property A or Property B is worth. Nothing here uses a household figure. The replay shows how much the answer to "live in, rent, or sell and reinvest" can move when good and bad years arrive in a different order.</div>
<div class="grid">""" + "".join(
        f'<div class="card"><div class="big">{b}</div><div class="lab">{l}</div><div class="src">{s}</div></div>' for b, l, s in cards) + f"""</div>
<h2>What the replay says about the decision</h2>
<ul>
<li><strong>The order of good and bad years moves the result a long way.</strong> Every path has the same average growth. By 2045 the home-price multiple ranges from {mult(min(v45))} (the path that begins with the years from {low45}) to {mult(max(v45))} (the path that begins with {hi45}). After inflation the range is {mult(min(real45))} to {mult(max(real45))}.</li>
<li><strong>Sell and buy stocks: ahead on price in {stock_beats} of {n_act} recorded 25-year periods.</strong> That is before rent, costs and tax. Keeping the house matched stocks only if it paid net cash, after all costs and taxes, of {pct(min(be_s))} to {pct(max(be_s))} of its value each year (middle {pct(med(be_s))}). Living in the house counts as that cash only to the extent it replaces rent the owner would otherwise pay.</li>
<li><strong>Sell and hold savings: behind in {n_act - bill_beats} of {n_act}.</strong> Treasury bills ended ahead of home prices in {bill_beats} of {n_act} periods. The house could have cost its owner {pct(-max(be_b))} to {pct(-min(be_b))} of its value a year and still matched bills.</li>
<li><strong>The replay can only reorder the record.</strong> Over these 49 years stocks with dividends returned about {pct(stock_all)} a year and local home prices rose about {pct(cagr(hpi, "ATNHPIUS41940Q"))} a year. It cannot show an economy worse than the record itself (flags S02, S11).</li>
<li><strong>Renting out the inherited home resets its taxable value to market value.</strong> In {sum(d > 0 for d in dec)} of {N} paths that new value was later above the market on at least one 1 January. A decline-in-value review applies in those years (flag S06).</li>
<li><strong>The Prop 19 amount and the estate exclusion move with different indexes than the house.</strong> See the transfer-year tables for how far each can drift.</li>
</ul>
<h2>Where to look</h2>
""" + table(["Page", "What it holds", "Main official sources"], [
        [a("replay.html", "Replay results"), "Home values, Prop 19 amount, estate exclusion and property tax at transfers in 2040, 2045 and 2050; house against stocks and Treasury bills over the 25 years after; rent control on Property B; the recorded downturns.", S["hpi"] + " · " + S["erp"] + " · " + S["lta26"]],
        [a("paths.html", "Year by year"), "Three complete paths, 2027 to 2075, one row a year: the lowest, middle and highest home value in 2045.", S["hpi"] + " · " + S["cpi"]],
        [a("baseline.html", "Baseline"), "What official forecasters assume for inflation and interest rates, next to the recorded averages.", S["cbo"] + " · " + S["ssa"]],
        [a("sources.html", "Sources and method"), "Every series, where it came from, and each rule used in the arithmetic.", S["lta25"] + " · " + S["plaw"]],
        [a("flagged.html", "Flagged for review"), "Approximations, gaps, and things that do not line up.", S["lta25"] + " · " + S["erp"]],
    ])
    page("index.html", "Uneven-economy replay", body)


def build_replay():
    b = []
    b.append("""<p class="lede">Every figure below is the middle result across the 49 paths, with the lowest and highest in brackets. Figures are per dollar or per $1,000,000, or for round reference home sizes. Pick the size nearest your own and scale.</p>""")

    # 1. home value multiples
    rows = []
    for T in TRANSFERS:
        va = at(T, "home_a"); vb = at(T, "home_b"); c = at(T, "cpi")
        ra = [x / y for x, y in zip(va, c)]
        act = actual_at(T)
        va_act = [PATHS[s]["home_a"][T] for s in act]
        rows.append([str(T), f"{T - START}", spread(va, mult), spread(va_act, mult) + f' <span class="rng">n={len(act)}</span>',
                     spread(ra, mult), spread(vb, mult), spread(c, mult), S["hpi"] + " · " + S["cpi"]])
    b.append("<h2>1. Home prices by the transfer year</h2><p>Multiple of the 2026 level. A multiple of 2.00× means prices doubled. \"Recorded order only\" leaves out paths that jump from 2025 back to 1977 before the transfer year.</p>")
    b.append(table(["Transfer at end of", "Years from 2026", "Property A metro, all 49 paths", "Property A metro, recorded order only",
                    "Property A metro after inflation", "Property B metro", "Consumer prices", "Source"], rows, "num"))

    # 2. Prop 19
    b.append(f"""<h2>2. Prop 19 amount and the taxable value if the heir moves in</h2>
<p>If a child makes the inherited family home a principal residence, the old taxable value carries over unless market value is more than the old taxable value plus an adjustable amount, now {stat(ALLOW_2026)}. Any excess is added. When there is an excess, the new taxable value works out to market value minus the amount, whatever the old taxable value was. If the heir does not move in, the new taxable value is full market value.</p>""")
    rows = []
    for T in TRANSFERS:
        al = at(T, "allow")
        rows.append([str(T), spread(al, money), spread([x / ALLOW_2026 for x in al], mult),
                     spread([PATHS[s]["allow"][T] / ALLOW_2026 / PATHS[s]["home_a"][T] for s in HIST], mult),
                     S["lta25"] + " · " + S["hpi"]])
    b.append(table(["Transfer at end of", "Replayed Prop 19 amount", "Multiple of today's amount", "Amount growth relative to Property A metro prices", "Source"], rows, "num"))
    b.append("<p class=\"small\">A figure below 1.00× in the last column means the amount grew more slowly than local home prices, so it shields a smaller share of the home.</p>")
    rows = []
    for T in TRANSFERS:
        for size in SIZES:
            mv = [size * PATHS[s]["home_a"][T] for s in HIST]
            nt = [max(size * PATHS[s]["home_a"][T] - PATHS[s]["allow"][T], 0) for s in HIST]
            share = [PATHS[s]["allow"][T] / (size * PATHS[s]["home_a"][T]) for s in HIST]
            rows.append([f"{T}", money(size), spread(mv, money), spread(nt, money), spread([x * 0.01 for x in nt], money),
                         spread([x * 0.01 for x in mv], money), spread(share, pct), S["pub801"] + " · " + S["hpi"]])
    b.append("<h3>Reference home sizes</h3><p>Tax is shown at the 1% basic rate only. Voter-approved debt and parcel charges are added on every bill and are not included (flag S05). \"Market value minus amount\" is the new taxable value only when it is higher than the old taxable value; otherwise the old value carries over.</p>")
    b.append(table(["Transfer", "Home value in 2026", "Market value at transfer", "Market value minus Prop 19 amount (heir moves in)",
                    "1% tax on that, first year", "1% tax at full market value (heir does not move in), first year", "Share of value shielded by the amount", "Source"], rows, "num"))

    # 3. estate exclusion
    b.append(f"""<h2>3. Federal estate exclusion against the home's value</h2>
<p>The basic exclusion is {stat(EXCL_2026)} for 2026 and is indexed to consumer prices after that. State-level rules are on the main dashboard's <a href="../public-safe/tax.html">inheritance and tax page</a>. The replay indexes the exclusion with replayed consumer prices, one year behind.</p>""")
    rows = []
    for T in TRANSFERS:
        ex = at(T, "excl")
        rows.append([str(T), spread(ex, money)] +
                    [spread([size * PATHS[s]["home_a"][T] / PATHS[s]["excl"][T] for s in HIST], pct) for size in SIZES] +
                    [S["plaw"] + " · " + S["irs_estate"] + " · " + S["cpi"]])
    b.append(table(["Death in", "Replayed exclusion"] + [f"Home worth {money(s)} in 2026, as share of exclusion" for s in SIZES] + ["Source"], rows, "num"))
    b.append("<p class=\"small\">Whatever share the home uses, the rest is the room left for cash and other assets before any estate tax. Home prices and consumer prices do not move together, so that room can shrink even when the exclusion rises every year.</p>")

    # 4. after the transfer
    n_act = len(WIN_ACTUAL)
    b.append(f"""<h2>4. The 25 years after the transfer: keep the house or sell and reinvest</h2>
<p>Per dollar of home value on the transfer date, before selling costs and before income tax on either side (flags S03, S04). Stocks are the S&amp;P 500 price change plus the year's dividend yield. Savings are 3-month Treasury bills rolled over. The break-even yield is the net cash the house would have to pay each year, as a share of its value, for keeping it to match selling, with that cash reinvested the same way.</p>""")
    def wrow(label, ws):
        return [label, f"{len(ws)}", spread([w["home"] for w in ws], mult), spread([w["stock"] for w in ws], mult),
                spread([w["bill"] for w in ws], mult), spread([w["cpi"] for w in ws], mult),
                f"{sum(w['stock'] > w['home'] for w in ws)} of {len(ws)}", f"{sum(w['bill'] > w['home'] for w in ws)} of {len(ws)}",
                spread([w["be_stock"] for w in ws], pct), spread([w["be_bill"] for w in ws], pct), S["hpi"] + " · " + S["erp"] + " · " + S["cpi"]]
    b.append(table(["25-year periods", "Count", "A dollar of house price becomes", "A dollar in stocks becomes", "A dollar in Treasury bills becomes",
                    "Consumer prices", "Stocks ahead of house price", "Bills ahead of house price",
                    "Break-even net yield against stocks", "Break-even net yield against bills", "Source"],
                   [wrow("Recorded order only", WIN_ACTUAL), wrow("All 49 rotations", WIN)], "num"))
    b.append("<p class=\"small\">The set of 25-year periods is the same whichever year the transfer happens, because every path is a rotation of the same years. What changes with the transfer year is which period you land in.</p>")
    rows = []
    for w in sorted(WIN_ACTUAL, key=lambda w: w["first"]):
        rows.append([f"{w['first']} to {w['last']}", mult(w["home"]), mult(w["stock"]), mult(w["bill"]), mult(w["cpi"]),
                     f'<span class="neg">{pct(w["trough"] - 1)}</span>' if w["trough"] < 1 else "none",
                     pct(w["be_stock"]), pct(w["be_bill"]), S["hpi"] + " · " + S["erp"] + " · " + S["cpi"]])
    b.append("<h3>Each recorded 25-year period</h3>")
    b.append(table(["Years replayed after transfer", "House price", "Stocks", "Treasury bills", "Consumer prices",
                    "Lowest house price against transfer date", "Break-even net yield against stocks", "Break-even net yield against bills", "Source"], rows, "num"))

    # 5. property tax after transfer when not occupied
    b.append("""<h2>5. Property tax after the transfer if the heir does not move in</h2>
<p>The home is reassessed at market value. From then on the taxable value rises by the Board of Equalization factor for each year, never more than 2%, and the assessor must enrol market value instead in any year it is lower. Figures are per $1,000,000 of market value at transfer, at the 1% basic rate, summed over 25 years.</p>""")
    t = [w["tax25"] * 1_000_000 for w in WIN]; flat = WIN[0]["tax25_flat"] * 1_000_000
    dec = [w["decline_years"] for w in WIN]
    wmax = max(WIN, key=lambda w: w["decline_years"])
    b.append(table(["Measure", "Result", "Source"], [
        ["25-year tax if the value rose exactly 2% every year", money(flat), S["lta26"]],
        ["25-year tax on the replayed paths", spread(t, money), S["lta26"] + " · " + S["prop8"] + " · " + S["hpi"]],
        ["Paths with at least one year below the taxable value", f"{sum(d > 0 for d in dec)} of {N}", S["prop8"] + " · " + S["hpi"]],
        ["Most years below the taxable value on any path", f"{max(dec)} of 25 (years replayed {span(wmax)})", S["prop8"] + " · " + S["hpi"]],
        ["Recorded years with a factor below 2%", ", ".join(f"{h} ({(chg[h]['p13'] - 1) * 100:.3f}%)" for h in HIST if chg[h]["p13"] < 1.02), S["lta26"]],
    ]))
    b.append("<p class=\"small\">A decline-in-value reduction is not automatic everywhere. The owner may need to ask for a review (flag S06).</p>")

    # 6. Property B rent control
    b.append("""<h2>6. Property B: rent control when inflation is uneven</h2>
<p>Property B is already owned, so nothing about the inheritance changes its taxable value. Its exposure is different. Whether its units are covered by the rent ordinance is not confirmed here; if they are, for a sitting tenant the yearly increase is 60% of the area's consumer price change. The table compares that with the area's recorded market rent index. A figure below 100% means a long-running tenancy pays less than a new one would.</p>""")
    rows = []
    for T in (2035,) + TRANSFERS:
        gap = [PATHS[s]["allowed"][T] / PATHS[s]["rent"][T] for s in HIST]
        rows.append([str(T), spread(at(T, "rent"), mult), spread(at(T, "allowed"), mult), spread(gap, pct),
                     spread(at(T, "home_b"), mult), S["sfrent"] + " · " + S["cpi"] + " · " + S["hpi"]])
    b.append(table(["By end of", "Area market rent index", "Allowed rent for a tenancy that began in 2026",
                    "Allowed rent as share of market rent", "Property B metro home prices", "Source"], rows, "num"))
    b.append("<p class=\"small\">No ceiling or floor on the yearly increase is applied, because none appears on the page retrieved (flag S08). Vacancies reset rent to market and are not modelled.</p>")

    # 7. the downturns themselves
    b.append("<h2>7. The recorded downturns</h2><p>Falls of 10% or more in year-end levels, 1976 to 2025. These are the events the replay moves around.</p>")
    rows = (episodes("ATNHPIUS41940Q", hpi, "Home prices, Property A metro", S["hpi"]) +
            episodes("ATNHPIUS41884Q", hpi, "Home prices, Property B metro", S["hpi"]) +
            episodes("CASTHPI", hpi, "Home prices, California", S["hpi"]) +
            episodes("sp500_end_of_year", sp, "S&amp;P 500 (price only)", S["erp"]))
    b.append(table(["Series", "Peak", "Low", "Fall", "Years to the low", "Back above the peak by end of", "Years from peak to recovery", "Source"], rows))
    hi_inf = [h for h in HIST if chg[h]["cpi"] >= 0.05]
    neg_inf = [h for h in HIST if chg[h]["cpi"] < 0]
    low_bill = [h for h in HIST if chg[h]["bill"] <= 0.0015]
    flat_rent = [h for h in HIST if chg[h]["rent_bay"] <= 0.002]
    neg_stock = [h for h in HIST if chg[h]["stock"] <= -0.10]
    b.append(table(["Other uneven years", "Years", "Source"], [
        ["Consumer prices up 5% or more", ", ".join(f"{h} ({pct(chg[h]['cpi'])})" for h in hi_inf), S["cpi"]],
        ["Consumer prices down", ", ".join(f"{h} ({pct(chg[h]['cpi'])})" for h in neg_inf), S["cpi"]],
        ["Treasury bill rate 0.15% or lower", ", ".join(f"{h} ({pct(chg[h]['bill'], 2)})" for h in low_bill), S["cpi"]],
        ["Area rent index flat or falling", ", ".join(f"{h} ({pct(chg[h]['rent_bay'])})" for h in flat_rent), S["cpi"]],
        ["Stocks down 10% or more with dividends", ", ".join(f"{h} ({pct(chg[h]['stock'])})" for h in neg_stock), S["erp"]],
    ]))
    page("replay.html", "Replay results", "\n".join(b))


def build_paths():
    order = sorted(HIST, key=lambda s: PATHS[s]["home_a"][2045])
    picks = [("Lowest home value in 2045", order[0]), ("Middle home value in 2045", order[N // 2]), ("Highest home value in 2045", order[-1])]
    b = ["""<p class="lede">Three of the 49 paths in full. Each row replays one recorded year. Home value is per $1,000,000 in 2026. Taxable value is per $1,000,000 of taxable value in 2026 and shows only the yearly factor, with no change of ownership.</p>"""]
    b.append(table(["Path", "Begins with the year", "Home-price multiple by 2045", "Source"],
                   [[lab, str(s), mult(PATHS[s]["home_a"][2045]), S["hpi"]] for lab, s in picks]))
    for lab, s in picks:
        p = PATHS[s]
        rows = []
        for t in YEARS:
            h = p["h"][t]; c = chg[h]
            neg = lambda x, d=1: f'<span class="neg">{pct(x, d)}</span>' if x < 0 else pct(x, d)
            rows.append([str(t), str(h), neg(c["cpi"]), neg(c["home_a"]), money(1_000_000 * p["home_a"][t]),
                         f"{(c['p13'] - 1) * 100:.3f}%", money(1_000_000 * p["fb"][t]), money(p["allow"][t]), money(p["excl"][t]),
                         neg(c["stock"]), pct(c["bill"], 2), neg(c["rent_bay"]),
                         a(U["hpi"], "FHFA") + " · " + a(U["cpi"], "BLS, Treasury") + " · " + a(U["lta26"], "BOE") + " · " + a(U["b55"] if h <= 2003 else U["b56"], "ERP")])
        b.append(f"<h2>{lab}: path beginning with {s}</h2>")
        b.append(table(["Year", "Replays", "Consumer prices", "Home prices, Property A metro", "Home value per $1,000,000",
                        "Prop 13 factor", "Taxable value per $1,000,000", "Prop 19 amount", "Estate exclusion",
                        "Stocks with dividends", "Treasury bill rate", "Area rent index", "Source"], rows, "num"))
    page("paths.html", "Year by year", "\n".join(b))


def cagr(table_, col, y0=1976, y1=2025):
    return (float(table_[y1][col]) / float(table_[y0][col])) ** (1 / (y1 - y0)) - 1

def build_baseline():
    avg = lambda k: statistics.mean(chg[h][k] for h in HIST)
    stock_cagr = 1.0
    bill_cagr = 1.0
    for h in HIST:
        stock_cagr *= 1 + chg[h]["stock"]; bill_cagr *= 1 + chg[h]["bill"]
    stock_cagr = stock_cagr ** (1 / N) - 1; bill_cagr = bill_cagr ** (1 / N) - 1
    b = ["""<p class="lede">A baseline is the calm case: one steady rate a year. Official forecasters publish steady long-run rates for consumer prices and interest rates. None retrieved for this section publishes a long-run rate for local home prices, rents or stock returns, so those cells are blank rather than filled in.</p>"""]
    b.append("<h2>Official long-run assumptions</h2>")
    b.append(table(["Measure", "Official assumption", "Period it covers", "Recorded average 1977 to 2025", "Source"], [
        ["Consumer prices (CPI)", "2.8% in 2026, 2.4% in 2027, then 2.3% a year", "2026 to 2036, fourth quarter to fourth quarter", pct(cagr(cpi, "CPIAUCNS")) + " a year", S["cbo"] + " · " + S["cpi"]],
        ["Consumer prices (CPI-W), long range", "2.4% a year (range 1.8% to 3.0%)", "2036 to 2100", pct(cagr(cpi, "CPIAUCNS")) + " a year (CPI-U)", S["ssa"] + " · " + S["cpi"]],
        ["3-month Treasury bill rate", "3.3% in 2026, 3.2% for 2027 to 2030, 3.1% for 2031 to 2036", "2026 to 2036, annual average", pct(avg("bill")) + " average; " + pct(bill_cagr) + " compounded", S["cbo"] + " · " + S["cpi"]],
        ["10-year Treasury note rate", "4.1% in 2026, 4.3% for 2027 to 2030, 4.4% for 2031 to 2036", "2026 to 2036, annual average", pct(avg("gs10")) + " average", S["cbo"] + " · " + S["cpi"]],
        ["Real interest rate on new Trust Fund issues", "2.3% (range 1.8% to 2.8%)", "2044 and later", "", S["ssa"]],
        ["Average covered wage, nominal", "3.57% a year (range 2.34% to 4.79%)", "2036 to 2100", "", S["ssa"]],
        ["Real GDP", "2.2% in 2026, then 1.8% a year", "2026 to 2036", "", S["cbo"]],
        ["Home prices, Property A metro", "", "No official long-run forecast retrieved (flag S09)", pct(cagr(hpi, "ATNHPIUS41940Q")) + " a year", S["hpi"]],
        ["Home prices, Property B metro", "", "No official long-run forecast retrieved (flag S09)", pct(cagr(hpi, "ATNHPIUS41884Q")) + " a year", S["hpi"]],
        ["Home prices, California", "", "No official long-run forecast retrieved (flag S09)", pct(cagr(hpi, "CASTHPI")) + " a year", S["hpi"]],
        ["Area rent index", "", "No official long-run forecast retrieved (flag S09)", pct(cagr(cpi, "CUURA422SEHA")) + " a year", S["cpi"]],
        ["Stocks with dividends", "", "No official long-run forecast retrieved (flag S09)", pct(stock_cagr) + " a year (approximate, flag S02)", S["erp"]],
        ["Prop 13 yearly factor", "At most 2%, by the state constitution", "Every year", f"{(statistics.mean(chg[h]['p13'] for h in HIST) - 1) * 100:.2f}% average", S["lta26"]],
    ]))
    b.append(f"""<div class="note"><strong>The recorded averages are history, not a forecast.</strong> The record starts with consumer prices rising {pct(chg[1980]["cpi"])} in 1980 and a 10-year Treasury yield of {pct(chg[1981]["gs10"], 2)} in 1981, and ends with both far lower. Nothing says the next 49 years will repeat it.</div>""")
    # steady-rate baseline, using only the official CPI assumption
    b.append("<h2>What a steady rate gives for the indexed amounts</h2><p>Only the estate exclusion can be projected from an official long-run rate, because it is tied to consumer prices. It is shown at the Trustees' intermediate, low and high inflation assumptions, next to the replay.</p>")
    rows = []
    for T in TRANSFERS:
        n = T - 2026
        rows.append([str(T), money(EXCL_2026 * 1.024 ** n), money(EXCL_2026 * 1.018 ** n), money(EXCL_2026 * 1.030 ** n),
                     spread(at(T, "excl"), money), S["ssa"] + " · " + S["plaw"]])
    b.append(table(["Year", "Exclusion at 2.4% a year", "At 1.8%", "At 3.0%", "Replay, all 49 paths", "Source"], rows, "num"))
    b.append(f"<p class=\"small\">The steady-rate columns compound from {stat(EXCL_2026)} in 2026 and ignore the rounding rule in the statute (flag S07). The replay column lags one year.</p>")
    b.append("<h2>Steady rate against uneven path, same average</h2><p>Each of the 49 paths has exactly the same 49 yearly changes, so each ends 2075 at the same level. The table shows how far apart they are on the way, which is when the transfer happens.</p>")
    end_mult = PATHS[H0]["home_a"][END]
    steady = end_mult ** (1 / N)
    rows = []
    for T in TRANSFERS:
        v = at(T, "home_a")
        rows.append([str(T), mult(steady ** (T - 2026)), mult(min(v)), mult(med(v)), mult(max(v)),
                     pct(min(v) / steady ** (T - 2026) - 1), pct(max(v) / steady ** (T - 2026) - 1), S["hpi"]])
    b.append(table(["Transfer at end of", "Steady path at the recorded average", "Lowest replay", "Middle replay", "Highest replay",
                    "Lowest against steady", "Highest against steady", "Source"], rows, "num"))
    page("baseline.html", "Baseline", "\n".join(b))


def build_sources():
    b = ["""<p class="lede">Every number in this section comes from the series and rules below. The series files are in the repository so the arithmetic can be re-run.</p>"""]
    b.append("<h2>Series</h2>")
    b.append(table(["Series", "Publisher", "What is used", "Years", "File", "Source"], [
        ["House price index, all transactions: Property A metro area, Property B metro division, California", "Federal Housing Finance Agency, served by the Federal Reserve Bank of St. Louis", "Fourth-quarter level; change from one year to the next", "1976 to 2025", a("data/fred_hpi_annual.csv", "fred_hpi_annual.csv"), S["hpi"]],
        ["Consumer price index, all urban consumers, U.S. city average", "Bureau of Labor Statistics, served by the Federal Reserve Bank of St. Louis", "Annual average; yearly change", "1976 to 2025", a("data/fred_cpi_rates_annual.csv", "fred_cpi_rates_annual.csv"), S["cpi"]],
        ["Consumer price index for the San Francisco area: all items, and rent of primary residence", "Bureau of Labor Statistics, served by the Federal Reserve Bank of St. Louis", "Annual average; yearly change", "1976 to 2025", a("data/fred_cpi_rates_annual.csv", "fred_cpi_rates_annual.csv"), S["cpi"]],
        ["3-month Treasury bill rate; 10-year Treasury yield", "Federal Reserve Board, served by the Federal Reserve Bank of St. Louis", "Annual average rate", "1977 to 2025", a("data/fred_cpi_rates_annual.csv", "fred_cpi_rates_annual.csv"), S["cpi"]],
        ["S&amp;P composite index, end of year; dividend-price ratio", "Council of Economic Advisers, Economic Report of the President 2026", "Price change plus dividend yield", "1976 to 2025", a("data/erp2026_sp500.csv", "erp2026_sp500.csv"), S["erp"]],
        ["Prop 13 inflation factors", "California State Board of Equalization", "Factor for the roll year that starts in the replayed year", "1977-78 to 2025-26", a("data/boe_lta2026_002_factors.csv", "boe_lta2026_002_factors.csv"), S["lta26"]],
    ]))
    b.append("<h2>Rules</h2>")
    b.append(table(["Rule", "How the replay applies it", "Source"], [
        ["Base year value rises by an inflation factor of at most 2% a year", "The actual factor published for each replayed year", S["lta26"]],
        ["The assessor enrols the lower of factored base year value and market value on 1 January", "Market value on 1 January is taken as the previous year-end index level", S["prop8"]],
        [f"Family-home transfer: value cap is the factored base year value plus {stat(ALLOW_2026)} (16 February 2025 to 15 February 2027); the heir must make it a principal residence within one year", "Excess of market value over the cap is added to taxable value", S["pub801"] + " · " + S["lta25"]],
        ["The amount is adjusted every other 16 February by the California house price index change for the prior calendar year", "Adjusted in 2029, 2031 and so on by the replayed California index change of the year before", S["lta25"]],
        ["The homeowners' exemption takes $7,000 off taxable value for an owner-occupied home", "Not applied; too small to change any figure shown", S["hox"]],
        [f"Federal basic exclusion amount is {stat(EXCL_2026)} for 2026, indexed after 2026 from a 2025 base", "Indexed by replayed consumer prices, one year behind", S["plaw"] + " · " + S["irs_estate"]],
        ["Inherited property generally takes a basis equal to fair market value at the date of death", "Not modelled; the comparison is before income tax", S["irs_basis"]],
        ["Covered rental units: allowed yearly increase is 60% of the area consumer price change (1.6% from 1 March 2026)", "60% of the replayed area price change each year", S["sfrent"]],
        ["Property B's county secured rate for fiscal year 2026-27 is 1.18162182%", "Not used in the replay; tax is shown at the 1% basic rate", S["sftax"]],
    ]))
    b.append(f"""<h2>Method</h2>
<div class="plain"><ul>
<li>There are {N} recorded years with every series available: {H0} to {H1}.</li>
<li>A path is those {N} years laid over {YEARS[0]} to {YEARS[-1]} in their recorded order, starting from one chosen year and continuing from {H1} back to {H0} when the record runs out. There are {N} paths, one for each starting year.</li>
<li>Every path contains the same years, so every path has the same average. Only the order differs. That isolates the effect of timing.</li>
<li>All series for a given year stay together. A year of high inflation keeps its own house prices, interest rates and stock returns.</li>
<li>Transfers are placed at the end of 2040, 2045 or 2050. The comparison period is the 25 years after.</li>
<li>"Recorded order only" results leave out any window that crosses the join from {H1} back to {H0}.</li>
<li>2026 itself is not replayed. Levels start from 2026 and the first replayed year is 2027.</li>
</ul></div>
<h2>Checks run by the build</h2>
<div class="plain"><ul>
<li>Each published factor equals the lower of 2% and the published California price change, except the 1983-84 row, which the Board lists as 1%.</li>
<li>Every table row carries an official source link. Every dollar figure is a multiple of $10 unless it is a statutory amount shown as published.</li>
<li>No page contains a name, address, parcel number, postal code or city name for either property.</li>
</ul></div>
<h2 id="correction">Correction on record</h2>
<p>The data files were typed from the text of the official pages, because the build machine cannot download them directly. They are transcriptions, not downloads.</p>
<p>A first version of the series file was committed with a header saying every value had been copied from the cited pages. That was not true: the pages were not at hand when it was written and most values had been entered from memory. The file was withdrawn before anything was built from it. The pages were then fetched again and the withdrawn values were compared one by one with the official figures. Three differed:</p>""")
    b.append(table(["Series", "Year", "Official response", "Withdrawn file had", "Source"], [
        ["House price index, Property A metro", "1975", "blank", "19.14", S["hpi"]],
        ["House price index, Property B metro", "1975", "blank", "19.28", S["hpi"]],
        ["Consumer price index, U.S. city average", "2025", "321.943", "321.9", S["cpi"]],
    ]))
    b.append("<p class=\"small\">None of the three is used by the replay in its withdrawn form: 1975 is outside the replayed years, and the 2025 figure now comes from the official response.</p>")
    page("sources.html", "Sources and method", "\n".join(b))


def build_flagged():
    ca24 = f(hpi, 2024, "CASTHPI") / f(hpi, 2023, "CASTHPI") - 1
    ca22 = f(hpi, 2022, "CASTHPI") / f(hpi, 2021, "CASTHPI") - 1
    rows = [
        ["S01", "Prop 19 amount: the index used here does not reproduce the Board's figure",
         f"The Board adjusted the amount by 2.15% for 2024, citing the FHFA quarterly report. The all-transactions California index used in this replay rose {pct(ca24, 2)} over the same year (fourth quarter to fourth quarter), and {pct(ca22, 2)} in 2022 against the 2.26% implied by the 2023 adjustment. The Board is using a different FHFA measure, which was not identified.",
         "In both adjustments made so far the Board's figure was lower than this index, so replayed Prop 19 amounts may be too high.", S["lta25"] + " · " + S["hpi"]],
        ["S02", "Stock returns are approximate",
         "No official yearly total-return series was found. Returns are year-end price change plus the dividend-price ratio, which is an average over the year.",
         "Small error in each year; does not change which periods were good or bad.", S["erp"]],
        ["S03", "No income tax on either side of the comparison",
         "Tax on rent, dividends, interest and gains depends on the owner's own return and on the basis of the inherited home.",
         "Break-even yields are before tax. The real hurdle differs for each household.", S["irs_basis"]],
        ["S04", "No selling costs",
         "Commissions and transfer taxes at sale are not included because no official figure for commissions exists.",
         "Selling and reinvesting looks slightly better here than it would be.", S["irs_basis"]],
        ["S05", "Tax shown at the 1% basic rate only",
         "Each bill also carries voter-approved debt rates and fixed charges that differ by tax-rate area. Property A's total rate was not confirmed from an official page and is left out.",
         "Actual bills are higher than the 1% figures.", S["sftax"] + " · " + S["lta26"]],
        ["S06", "Decline-in-value relief may need a request",
         "The replay assumes the lower market value is enrolled in every year it applies.",
         "If a review is not requested or not granted, tax in those years is higher.", S["prop8"]],
        ["S07", "Estate exclusion indexing is approximate",
         "The law points to the cost-of-living adjustment in section 1(f)(3) with a 2025 base. This replay uses the CPI-U annual average, lagged one year, with no rounding. Whether that matches the statutory measure and rounding was not checked. The 2027 amount is held at the 2026 figure because 2026 inflation is not yet known. The replay also lets the amount fall after a year of falling prices, which the law may not allow.",
         "Replayed exclusions can differ from the amounts the IRS will publish.", S["plaw"] + " · " + S["irs_estate"]],
        ["S08", "Rent-control ceiling and floor not applied",
         "The city page states the 60% rule. Any yearly maximum or minimum in the ordinance was not on the page retrieved. In the highest-inflation replayed year, 60% of the area price change is " + pct(0.6 * max(chg[h]["cpi_bay"] for h in HIST)) + ".",
         "Allowed rents may be overstated in high-inflation paths.", S["sfrent"]],
        ["S09", "No official long-run forecast for home prices, rents or stocks",
         "The baseline page leaves those cells blank. Recorded averages are shown as history only.",
         "No steady-rate baseline is offered for those series.", S["cbo"] + " · " + S["ssa"]],
        ["S10", "2025 consumer price averages rest on incomplete months",
         "October 2025 prices were not collected during the federal shutdown, as the Board's letter records. An earlier request for the 2025 annual average returned a blank; the request on " + RETRIEVED + " returned a value.",
         "The 2025 inflation figure may be revised.", S["lta26"] + " · " + S["cpi"]],
        ["S11", "The join from 2025 back to 1977 never happened",
         "Paths that run past 2025 continue with 1977. Results marked recorded order only exclude windows that cross the join.",
         "Use the recorded-order rows when in doubt.", S["hpi"]],
        ["S12", "A metro index is not a house",
         "The index tracks repeat sales and appraisals across a whole metro area. One property can do better or worse.",
         "Ranges for a single home are wider than shown.", S["hpi"]],
        ["S13", "Proposed limit on banked and capital-improvement rent increases",
         "The city page carries a notice, posted 9 November 2026, of proposed legislation (File No. 261020) to cap combined banked and capital-improvement increases at 10% a year. It has not been enacted.",
         "Could limit catch-up increases on Property B after high-inflation years.", S["sfrent"]],
        ["S14", "First data file in this section was withdrawn",
         "An earlier commit on this session's branch held series values entered from memory and described as transcribed. It was removed and replaced with values typed from the official pages. Three values differed.",
         "No published figure was built from the withdrawn file.", a("sources.html#correction", "Correction on record") + " · " + S["hpi"]],
        ["S16", "The replay lets the Prop 19 amount fall",
         "The amount is moved by the replayed California index change, including years when the index fell. Whether the law allows the amount to go down was not checked.",
         "The lowest replayed amounts may be too low.", S["lta25"]],
        ["S15", "Treasury bill rate is not a return",
         "The series is the secondary-market rate on a discount basis, averaged over the year. Rolling bills would earn slightly more.",
         "Savings results are slightly understated.", S["cpi"]],
    ]
    b = ["""<p class="lede">These are the approximations, gaps and mismatches in this section. None blocks the replay; each changes how much weight a figure can bear.</p>""",
         table(["Flag", "Issue", "What was found", "Effect", "Source"], rows)]
    page("flagged.html", "Flagged for review", "\n".join(b))


# ----------------------------------------------------------------------------- self-check
PII = [
    (r"[\w.+-]+@[\w-]+\.[a-z]{2,}", "e-mail"), (r"\b\d{3}-\d{2}-\d{4}\b", "SSN shape"),
    (r"\b\(?\d{3}\)?[-. ]\d{3}[-.]\d{4}\b", "phone shape"), (r"\b\d{5}(?:-\d{4})?\b", "postal code shape"),
    (r"\bAPN\b|\bparcel\s+number\b", "parcel"),
    (r"\bCupertino\b|\bSunnyvale\b|\bSan Jose\b|\bPalo Alto\b|\bSaratoga\b|\bLos Altos\b|\bOuter Sunset\b", "city"),
]
MONEY = re.compile(r"\$(\d{1,3}(?:,\d{3})+|\d+)(?![\d.,])")

def self_check():
    errs, rows, links = [], 0, 0
    for p in sorted(HERE.glob("*.html")):
        text = p.read_text()
        body = re.sub(r"<style>.*?</style>", "", text, flags=re.S)
        visible = re.sub(r"<a\b.*?</a>", "", body, flags=re.S)
        visible = re.sub(r'(?:href|src)="[^"]*"', "", visible)
        for pat, lab in PII:
            if lab == "parcel" and p.name == "sources.html":
                continue                 # the checks list names the pattern it tests for
            m = re.search(pat, visible, re.I)
            if m:
                errs.append(f"{p.name}: {lab}: {m.group(0)}")
        stripped = re.sub(r'<span class="stat">.*?</span>', "", body, flags=re.S)
        for m in MONEY.finditer(stripped):
            if int(m.group(1).replace(",", "")) % 10:
                errs.append(f"{p.name}: unrounded ${m.group(1)}")
        for tr in re.findall(r"<tbody>(.*?)</tbody>", body, flags=re.S):
            for row in re.findall(r"<tr>(.*?)</tr>", tr, flags=re.S):
                rows += 1
                if "https://" not in row:
                    errs.append(f"{p.name}: row without official link: {row[:80]}")
        for href in re.findall(r'href="([^"]+)"', body):
            links += 1
            if not href.startswith("http") and not (HERE / href.split("#")[0]).exists():
                errs.append(f"{p.name}: broken local link {href}")
        if re.search(r"<(script|iframe|form)\b", body):
            errs.append(f"{p.name}: forbidden element")
    if errs:
        raise SystemExit("\n".join(errs))
    print(f"PASS: {len(list(HERE.glob('*.html')))} pages, {rows} table rows each with an official link, {links} links, money rounds to $10, no identifier patterns")


if __name__ == "__main__":
    build_index(); build_replay(); build_paths(); build_baseline(); build_sources(); build_flagged()
    self_check()
