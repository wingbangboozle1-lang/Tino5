"""Render the referee pages (referee-abae/*.html) from analysis.compute() and registry.

Run from the repository root:   python3 referee-abae/_src/build.py
Output is deterministic. Nothing household-derived in dollars is written (test_build.py enforces it).
"""
import html
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
sys.path.insert(0, str(HERE))
import analysis as AN  # noqa: E402
import registry as R  # noqa: E402

NAV = [("index", "Overview"), ("constants", "Official constants"), ("traceability", "Desk check"),
       ("robustness", "Robustness"), ("baselines", "Baselines"), ("discrepancies", "Discrepancies"), ("flagged", "Flagged")]
RETRIEVED_LONG = "12 November 2026"
NAMES = {"S1": "Occupy", "S2": "Rent", "S3": "Sell and reinvest"}

CSS = """:root{--ink:#1d2733;--mute:#566474;--line:#d6dde6;--bg:#f6f8fb;--card:#fff;--accent:#14507a;--ok:#1b7a43;--warn:#9a6700;--bad:#b3261e}
*{box-sizing:border-box}body{margin:0;font:16px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);background:var(--bg)}
header{background:var(--accent);color:#fff;padding:18px 24px}header h1{margin:0 0 4px;font-size:1.5rem}header p{margin:0;opacity:.9;font-size:.95rem}
nav{background:#0f3c5c;padding:0 16px;display:flex;flex-wrap:wrap}nav a{color:#dbe9f4;text-decoration:none;padding:10px 12px;font-size:.95rem}nav a.on,nav a:hover{background:#0b2f48;color:#fff}
main{max-width:1180px;margin:0 auto;padding:22px 24px 48px}h2{margin:30px 0 8px;font-size:1.25rem}h3{margin:20px 0 6px;font-size:1.05rem}
p.lead{font-size:1.05rem;color:#2c3a4a}.note{background:#fff8e1;border:1px solid #f0d98a;border-radius:6px;padding:10px 14px;margin:14px 0}
.box{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:6px 14px 14px;margin:12px 0}
table{border-collapse:collapse;width:100%;background:var(--card);margin:10px 0 18px;font-size:.93rem}th,td{border:1px solid var(--line);padding:7px 9px;text-align:left;vertical-align:top}
th{background:#e9eff6;font-weight:600}tr:nth-child(even) td{background:#fafcfe}td.num{text-align:right;white-space:nowrap}
.badge{display:inline-block;border-radius:10px;padding:1px 9px;font-size:.8rem;font-weight:600;white-space:nowrap}
.ok{background:#e1f4e8;color:var(--ok)}.warn{background:#fff1cc;color:var(--warn)}.bad{background:#fde3e1;color:var(--bad)}.info{background:#e3eefb;color:var(--accent)}
code,pre{font:13px/1.45 ui-monospace,Menlo,Consolas,monospace;background:#eef2f7;border-radius:4px}code{padding:1px 4px}pre{padding:10px 12px;overflow:auto}
footer{max-width:1180px;margin:0 auto;padding:0 24px 40px;color:var(--mute);font-size:.88rem}a{color:var(--accent)}
"""


def esc(s):
    return html.escape(str(s), quote=True)


def A(key):
    label, url = R.L[key]
    return f'<a href="{esc(url)}" rel="noopener">{esc(label)}</a>'


def links(keys):
    return "<br>".join(A(k) for k in keys)


def badge(kind, text):
    return f'<span class="badge {kind}">{esc(text)}</span>'


def pc(x, d=1):
    return f"{x * 100:.{d}f}%"


def rx(x):
    return f"{x:.2f}\u00d7"


def table(headers, rows, cls=""):
    h = "".join(f"<th>{esc(c)}</th>" for c in headers)
    body = "".join("<tr>" + "".join(c if c.startswith("<td") else f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table>'


def td_num(s):
    return f'<td class="num">{s}</td>'


def page(slug, title, lead, body):
    nav = "".join(f'<a href="{s}.html"{" class=on" if s == slug else ""}>{esc(t)}</a>' for s, t in NAV)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>{esc(title)} - Independent referee</title>
<link rel="stylesheet" href="style.css"></head><body>
<header><h1>{esc(title)}</h1><p>Independent numeric referee &middot; sources read {RETRIEVED_LONG} &middot; no household dollar amounts &middot; places not named</p></header>
<nav>{nav}<a href="../">Site landing</a></nav>
<main><p class="lead">{lead}</p>{body}</main>
<footer><p>Scope. This page contains no names, addresses, ZIP codes, parcel numbers, household bills, rents, values or account details. It shows official figures, rates, ratios, counts and pass/fail results. Property A is the future trust inheritance; Property B is already owned. Not advice: rules and thresholds may change before a transfer, and every figure here is only as good as the source linked in its row.</p></footer>
</body></html>
"""


def status_badge(s):
    return {"opened": badge("ok", "read in official source"), "secondary": badge("warn", "secondary only - unverified"),
            "transcribed": badge("info", "transcribed, spot-checked")}[s]


# ----------------------------------------------------------------------------------------------------------
def page_constants():
    rows = [[esc(i), esc(t), esc(v), links(ks), status_badge(st), esc(u), esc(n)] for i, t, v, ks, st, u, n in R.CONSTANTS]
    n_open = sum(1 for c in R.CONSTANTS if c[4] == "opened")
    n_sec = sum(1 for c in R.CONSTANTS if c[4] == "secondary")
    body = f"""<p>{len(R.CONSTANTS)} official figures this referee checked, each against the page or document linked in its row.
{n_open} were read in the official source; {n_sec} remain secondary-only and are repeated on the Flagged page. A figure is never
filled in from memory: where the official text was not read, the row says so.</p>
{table(["ID", "Item", "Value as printed by the source", "Official source (opened)", "Status", "Used by", "Note"], rows)}
<h2>Values superseded by a newer official figure</h2>
{table(["Figure", "Superseded because", "Official source"],
       [[esc("$" + k), esc(v), links(["de300"] if k == "184,500" else ["lta25009"])] for k, v in R.SUPERSEDED.items()])}"""
    return page("constants", "Official constants", "Every statutory amount and agency statistic the decision model leans on, with its source.", body)


def page_traceability(a):
    rep = a.get("rep", {})
    rows_ok, rows_n = rep.get("row_ok", 0), len(rep.get("row_checks", []))
    be = rep.get("breakeven", {})
    allow = rep.get("allowance", {})
    wg = rep.get("water_gap", {})
    checks = [
        ["C1", "Published 25-year comparison rows (market value at transfer, occupy, rent, sell, sell minus rent; three transfer years)",
         f"{rows_ok} of {rows_n} figures reproduced within $10 by the reference engine", badge("ok", "pass") if rows_ok == rows_n and rows_n else badge("bad", "check"),
         links(["lta25009", "rp2635"])],
        ["C2", "Reference engine against the desk's own module, unrounded",
         "largest difference over the three transfer years is below one cent", badge("ok", "pass") if rep.get("module_max_abs_diff", 1) < 0.01 else badge("bad", "check"),
         links(["lta25009", "rp2635"])],
        ["C3", "Prop 19 allowance: desk grows it 2% a year; statute adjusts it every other 16 February by one year of California price change",
         "statute rule, projected with 4% price growth, differs from the desk's path by "
         + ", ".join(f"{abs(allow[T]) * 100:.1f}% ({T})" for T in sorted(allow)), badge("ok", "consistent"), links(["lta25009"])],
        ["C4", "Published break-even after-tax return (3.03%) and break-even price growth (6.10% a year for 44 years)",
         f"reproduced: return {pc(be.get('r_star_desk_definition', 0), 2)} on the desk's definition, {pc(be.get('r_star', 0), 2)} with rent income re-priced consistently; growth {pc(be.get('g_star', 0), 2)}",
         badge("ok", "pass"), links(["fhfa", "cbo"])],
        ["C5", "Estate headroom lines for 2040, 2045 and 2050 (exclusion indexed at 2.2% a year from 2027, minus market value of A)",
         "arithmetic reproduced to the dollar for 2045; the 2.2% indexing and the 'estate = A plus cash' premise are the desk's assumptions", badge("warn", "arithmetic only"),
         links(["rp2635", "ir2026133"])],
        ["C6", "Water cost growth: projection table uses 3.0% a year, decision model 2.5%",
         f"the two paths differ by {pc(wg.get('ratio_by_2045', 0))} by 2045 and {pc(wg.get('ratio_by_2070', 0))} by 2070 on the water line; effect on the ordering: none (see X08)",
         badge("warn", "internal gap"), links(["cbo", "ssa"])],
        ["C7", "Closed-form identities (independent of the desk's code): sell-path value equals net proceeds times (1+return)^25; a full-reassessment rent path pays tax on market value; value limit test at, below and above the limit",
         "all hold in the reference engine's unit tests", badge("ok", "pass"), links(["prop19", "lta25009"])],
    ]
    t1 = table(["ID", "Check", "Result", "Verdict", "Official source"], checks)
    drows = []
    for i, item, desk, off, res, ks in R.DESK_STATUTORY:
        kind = "ok" if res.startswith("match") else "bad"
        drows.append([esc(i), esc(item), esc(desk), esc(off), badge(kind, res), links(ks)])
    t2 = table(["ID", "Item shown by the unpublished desk", "Desk value", "Official value", "Result", "Official source"], drows)
    srows = []
    for name, mine, off, key in R.SPOT:
        srows.append([esc(name), td_num(f"{mine:g}"), td_num(f"{off:g}"), badge("ok", "equal") if mine == off else badge("bad", "differs"), A(key)])
    t3 = table(["Series value", "In the 3a49d618 transcription", "On the official page", "Result", "Official source"], srows)
    sec22 = ""
    if a.get("rep22"):
        r22 = a["rep22"]
        t4 = table(["Transfer year", "Sell path: reference engine vs desk", "Rent path: reference engine vs desk", "Occupy path: reference engine vs desk", "Official source"],
                   [[f"{x['T']}", td_num(f"{x['s3'] * 100:+.1f}%"), td_num(f"{x['s2'] * 100:+.1f}%"), td_num(f"{x['s1'] * 100:+.1f}%"), links(["lta25009", "rp2635"])] for x in r22])
        g = a["groups22"]
        t5 = table(["Assumption that differs", "From the first desk to the second", "Effect on Sell \u00f7 Rent when changed alone", "Official source"],
                   [[esc(x["name"]), esc(x["change"]), td_num(f"{x['s3_s2_pct'] * 100:+.1f}%"),
                     links(["rp2635", "ftb26"] if "Tax" in x["name"] or "exclusion" in x["name"] else (["fred_a", "fhfa"] if "growth" in x["name"] else (["tsp", "erp56"] if "return" in x["name"] else ["lta25009"])))] for x in g]
                  + [[esc("All differences together"), esc("first desk's parameters replaced by the second's"), td_num(f"{rx(a['all22']['s3_s2'])} against {rx(a['their22']['their_s3_s2'])} published by the second desk"), links(["tsp", "erp56"])]])
        sec22 = f"""<h2>A second decision desk (22a32b17), run through the same engine</h2>
<p>A second session published its own desk with its own model. The reference engine was fed that desk's parameters (read in memory from its model file) and its three paths compared with the desk's published ones.
The sell path matches to rounding. The rent path is about 1% lower and the occupy path about 4% lower in the engine, because the second desk also includes effects on Property B (owner-occupancy changes there) that the reference engine omits.</p>
{t4}
<p>The two desks reach different headline levels for the same decision. Replacing the first desk's parameters with the second's, one group at a time, shows why:</p>
{t5}
<p>One assumption, the after-tax return on the reinvested proceeds, explains almost all of the gap. Everything else together moves the ratio by a few percent.</p>"""
    body = f"""<div class="note"><strong>What agreement means.</strong> The reference engine was written after the desk's model had been read, so
C1 and C2 show that the stated mechanics give the stated numbers (replication). They do not validate the mechanics. Independence comes from
C3&ndash;C7, from the constants register, and from the stress tests and historical windows on the next pages.</div>
<h2>Model and arithmetic checks</h2>{t1}
<h2>Statutory figures shown by the unpublished desk, against the official source</h2>
<p>{sum(1 for d in R.DESK_STATUTORY if d[4].startswith('match'))} of {len(R.DESK_STATUTORY)} match. Mismatches are logged as X04 and X05 and passed to the desk's owner; the desk is excluded from the site build.</p>{t2}
{sec22}
<h2>Spot checks of series transcribed by another session</h2>
<p>Session 3a49d618 transcribed official time series into <code>swan-3a49/data/</code>. The referee compared {len(R.SPOT)} values with official pages it opened itself; all {len(R.SPOT)} are equal. Other values in those files were not checked (see F-A7).</p>{t3}"""
    return page("traceability", "Desk check", "Do the published numbers follow from the stated rules, and do the statutory figures match the official sources?", body)


def page_robustness(a):
    if not a.get("desk_present"):
        return page("robustness", "Robustness", "Not computed in this build: the desk module was not found.", "<p>No data.</p>")
    base, rng = a["base"], a["ranges"]
    ind = a["indiff"]

    def order_words(o):
        return o.replace("S3", "Sell").replace("S2", "Rent").replace("S1", "Occupy")

    hrows = []
    for T in sorted(base):
        b = base[T]
        hrows.append([f"{T} (valued {T + 25})", td_num(rx(b["s3_s2"])), td_num(rx(b["s3_s1"])), td_num(rx(b["s2_s1"])),
                      esc(order_words(a["base_order"][T])), links(["lta25009", "rp2635"])])
    t_head = table(["Transfer year", "Sell \u00f7 Rent", "Sell \u00f7 Occupy", "Rent \u00f7 Occupy", "Ordering", "Official parameters"], hrows)

    srows = [[esc(a["scen"][0]["label"]), td_num(rx(a["scen"][0]["r"]["s3_s2"])), td_num(rx(a["scen"][0]["r"]["s3_s1"])), td_num(rx(a["scen"][0]["r"]["s2_s1"])),
              badge("info", "reference"), esc(a["scen"][0]["note"]), links(a["scen"][0]["links"])]]
    n_keep = 0
    flips = []
    for s in a["scen"][1:]:
        r = s["r"]
        if s["flip_s3_s2"]:
            verdict = badge("bad", "Sell no longer beats Rent")
            flips.append(s["label"])
        elif s["at_breakeven"]:
            verdict = badge("warn", "at break-even")
            flips.append(s["label"])
        elif s["flip_s2_s1"]:
            verdict = badge("bad", "Rent no longer beats Occupy")
            flips.append(s["label"])
        else:
            verdict = badge("ok", "ordering kept")
            n_keep += 1
        srows.append([esc(s["label"]), td_num(rx(r["s3_s2"])), td_num(rx(r["s3_s1"])), td_num(rx(r["s2_s1"])), verdict,
                      esc(s["note"]), links(s["links"])])
    t_scen = table(["Stress applied (transfer in 2045, valued 25 years later)", "Sell \u00f7 Rent", "Sell \u00f7 Occupy", "Rent \u00f7 Occupy", "Result", "Note", "Official source"], srows)
    body = f"""<p>Ratios of after-tax wealth at the end of the holding period, from the reference engine run on the desk's own assumptions. A ratio above
1.00 means the first path ends ahead. Dollar levels are deliberately not shown.</p>
<div class="note"><strong>Conditional, not a recommendation.</strong> The ordering is a property of the model and of inputs that are not yet verified from official
sources (gross rent, tax-rate area, insurance, transfer date). Treat it as a hypothesis the stress tests below try to break.</div>
<h2>Headline ordering under the desk's assumptions</h2>{t_head}
<p>Across the three windows: Sell &divide; Rent {rx(rng['s3_s2'][0])}&ndash;{rx(rng['s3_s2'][1])}; Sell &divide; Occupy {rx(rng['s3_s1'][0])}&ndash;{rx(rng['s3_s1'][1])};
Rent &divide; Occupy {rx(rng['s2_s1'][0])}&ndash;{rx(rng['s2_s1'][1])}.</p>
<h2>Stress tests</h2>
<p>{n_keep} of {len(a['scen']) - 1} stresses keep the ordering Sell &gt; Rent &gt; Occupy. The ordering fails or sits at break-even in {len(flips)}:</p>
<ul>{''.join(f'<li>{esc(f)}</li>' for f in flips)}</ul>
{t_scen}
<h2>What living in A must be worth</h2>
<p>If the heir lives in A, the model charges all holding costs and gives no credit for housing. The table converts the wealth gap into the yearly value of
living there, as a share of A's market value in the first year (growing with inflation afterwards), and sets it beside the model's own gross rent yield.</p>
{table(["Comparison", "First-year value of living in A needed, as share of market value", "Model's gross rent yield, same year", "Official source"],
       [["Occupy instead of selling and reinvesting", td_num(pc(ind['vs_sell'], 2)), td_num(pc(ind['rent_yield'], 2)), links(["cbo", "fhfa"])],
        ["Occupy instead of renting out", td_num(pc(ind['vs_rent'], 2)), td_num(pc(ind['rent_yield'], 2)), links(["cbo", "fhfa"])]])}
<p>Reading: living in A beats selling only if it is worth about {pc(ind['vs_sell'], 1)} of the home's value each year, roughly {ind['vs_sell'] / ind['rent_yield']:.1f} times the model's gross rent yield. It beats
renting only if worth about {pc(ind['vs_rent'], 1)} a year. Both depend on the unverified rent input.</p>"""
    return page("robustness", "Robustness of the ordering", "Which assumptions can overturn the model's ranking of occupy, rent and sell?", body)


def page_baselines(a):
    if not a.get("desk_present"):
        return page("baselines", "Baselines", "Not computed in this build.", "<p>No data.</p>")
    ws, sm = a["windows"], a["win_summary"]

    def rng(k, d=1):
        return f"{pc(sm[k]['min'], d)} to {pc(sm[k]['max'], d)} (median {pc(sm[k]['median'], d)})"

    ddrows = [[f"{d['peak'][:7]} to {d['trough'][:7]}", td_num(f"{d['change'] * 100:+.1f}%"), links(["fred_a", "fhfa"])] for d in a["drawdowns"]]
    t_dd = table(["Peak to trough (local metro index, quarterly)", "Change", "Official source"], ddrows)
    wrows = []
    for w in ws:
        s3 = w["eq_total"] * (1 - a["tax_rates"]["cg"]) > w["r_star"]
        bd = w["bond_pre"] * (1 - a["tax_rates"]["ord"]) > w["r_star"]
        wrows.append([f"{w['start']} to {w['end']}", td_num(pc(w["home"])), td_num(pc(w["cpi"])), td_num(pc(w["eq_total"])), td_num(pc(w["bond_pre"])),
                      td_num(pc(w["r_star"])), badge("ok", "yes") if s3 else badge("bad", "no"), badge("ok", "yes") if bd else badge("bad", "no"),
                      links(["fred_a", "bls_cpi", "erp55", "erp56"])])
    t_w = table(["25-year window", "Home-price growth a year", "Consumer-price growth a year", "S&P price plus dividends a year (approx.)", "10-year Treasury yield, mean (approx.)",
                 "After-tax return needed for Sell to tie Rent", "Sell beats Rent with equities, all return taxed at the desk's capital-gain rate", "Sell beats Rent with Treasuries, taxed at the desk's ordinary rate", "Official sources"], wrows)
    eq = a["equity_check"]
    f = a["factors"]
    body = f"""<p>What the official series say about the three inputs that drive the decision: local home prices, inflation, and the return on reinvested proceeds.
Series: FHFA house price index for A's metro, BLS consumer prices, the Economic Report of the President's S&amp;P tables, and the 10-year Treasury yield,
as transcribed by session 3a49d618 ({esc(a['win_where'])}, commit {esc(a['win_commit'])}) and spot-checked on the Desk check page.</p>
<h2>Drawdowns in the local price index</h2>{t_dd}
<p>The index has fallen for years at a time (1989&ndash;1994 and 2006&ndash;2012). Over the whole record, from the fourth quarter of 1976 to that of 2025, it grew {pc(a['a_cagr_long'])} a year.</p>
<h2>Rolling 25-year windows</h2>
<p>{sm['n']} windows start between 1976 and 2000. Home-price growth ranged {rng('home')}; consumer prices {rng('cpi')}; the S&amp;P approximation {rng('eq_total')}.
The desk assumes {pc(a['desk_g'])} home growth, below every historical window, and a {pc(a['desk_r'])} after-tax return, inside the {pc(sm['r_star']['min'])} to {pc(sm['r_star']['max'])} range of returns that would make Sell tie Rent across the windows.
Windows overlap heavily, so they are not 25 independent trials: fifty years of data hold about two separate 25-year periods. Each window is run as a transfer in 2026 followed by 25 years at that window's growth, inflation and returns; the desk's own comparison uses 2045, and the break-even return differs by about 0.15 points between the two.</p>
{t_w}
<h2>Summary of the windows</h2>
{table(["Measure", "Result", "Official source"], [
    ["Windows in which Sell beats Rent when the portfolio is equities and all of its return is taxed each year at the desk's rate", td_num(f"{a['win_s3_wins_full_drag']} of {sm['n']}"), links(["erp55", "erp56"])],
    ["Windows in which Sell beats Rent when the portfolio is Treasuries only, taxed at the desk's ordinary rate", td_num(f"{a['win_bond_wins']} of {sm['n']}"), links(["cbo", "fred_a"])],
    ["Windows in which home-price growth exceeded the desk's 6.1% break-even", td_num(f"{a['win_home_above_6_1']} of {sm['n']}"), links(["fred_a", "fhfa"])],
    ["After-tax return needed for Sell to tie Rent: lowest to highest window", td_num(f"{pc(sm['r_star']['min'])} to {pc(sm['r_star']['max'])}"), links(["fred_a", "erp56"])],
    ["After-tax equity return actually earned in the windows (all return taxed every year at the desk's capital-gain rate, approximation): lowest / median / highest", td_num(f"{pc(a['eq_after_tax']['min'])} / {pc(a['eq_after_tax']['median'])} / {pc(a['eq_after_tax']['max'])}"), links(["erp55", "erp56"])],
    ["Windows in which that return fell below the first desk's 4.5% / the second desk's 5.6% assumption", td_num(f"{a['eq_after_tax']['below_desk']} / {a['eq_after_tax']['below_22a']} of {sm['n']}") if a['eq_after_tax']['below_22a'] is not None else td_num(f"{a['eq_after_tax']['below_desk']} of {sm['n']} (first desk only)"), links(["erp56", "tsp"])],
    ["Share of the equity return that could be lost to tax before Sell stops beating Rent", td_num(f"{pc(sm['tax_drag_tolerated']['min'], 0)} to {pc(sm['tax_drag_tolerated']['max'], 0)}"), links(["tc409", "tc559"])],
]) }
<h2>Cross-checks on the equity series</h2>
{table(["Check", "Result", "Official source"], [
    ["S&P price plus dividends, end of 1987 to end of 2025, from the Economic Report tables (approximation: price growth plus mean dividend-price ratio)", td_num(pc(eq['total'], 2) + " a year"), links(["erp55", "erp56"])],
    ["TSP C Fund (tracks the S&P 500), since 29 January 1988 inception, as of October 2026", td_num("11.40% a year"), links(["tsp"])],
    ["Prop 13 inflation factor below 1.02 (inflation under 2%) in", td_num(f"{f['below_1_02']} of {f['n']} roll years"), links(["lta26002"])],
    ["Lowest Prop 13 factor on record (a fall in assessed-value growth, not a cut)", td_num(f"{f['min']:.5f}"), links(["lta26002"])],
    ["CPI average annual increase 1969-2019 / ultimate CPI assumption of the SSA Trustees / CBO 2028-2036", td_num("3.89% / 2.40% / 2.3%"), links(["ssa", "cbo"])],
]) }
<p>The approximation lands within 0.2 percentage points of the TSP figure, over nearly the same period, which supports using it for the windows.</p>"""
    return page("baselines", "Baselines and history", "What local prices, inflation and stock and bond returns actually did over 25-year windows.", body)


def page_discrepancies(a):
    sc = {s["label"]: s["r"] for s in a.get("scen", [])}

    def find(prefix):
        for k, v in sc.items():
            if k.startswith(prefix):
                return v
        return {"s3_s2": float("nan"), "s2_s1": float("nan")}
    base = find("Desk assumptions")
    liq = find("Tax on the reinvested")
    mod_fixed = find("Moderate marginal rates (")
    mod_cons = find("Moderate marginal rates, with")
    ins = find("Insurance cost halved")
    wat = find("Water cost grows")
    rows = [
        ["X02", badge("warn", "medium"), "Terminal-tax convention",
         f"The comparison charges the tax on selling A at the horizon on the occupy and rent paths but charges no tax on embedded gains of the sell-and-reinvest portfolio. That is right only if the {pc(a.get('desk_r', 0.045))} after-tax return already nets out every tax on the portfolio, including gains not yet realised. If it does not, the sell path's lead over renting falls from {rx(base['s3_s2'])} to {rx(liq['s3_s2'])} (an upper bound); the ordering survives. State the convention on the desk's pages.",
         links(["tc409", "p551"])],
        ["X03", badge("info", "low"), "Flat top-bracket tax rates",
         f"The desk charges one combined top rate on every dollar of rent and gain. California's 12.3% bracket begins near $768,000 (single) and $1.54 million (joint) and the extra 1% only above $1,000,000 of taxable income; the federal 35% bracket begins at $264,550 / $529,100. With moderate rates and the return unchanged the sell lead is {rx(mod_fixed['s3_s2'])}; with the return re-derived consistently it is {rx(mod_cons['s3_s2'])}. Ordering unchanged.",
         links(["rp2635", "ftb26", "rtc17043"])],
        ["X04", badge("info", "low"), "Estates-and-trusts capital-gain ceiling for 2026",
         "The unpublished desk shows $16,200; Rev. Proc. 2025-32 section 4.03 gives $16,250. The 2027 figure ($16,750) matches. Owner of desk-b4f to correct.",
         links(["rp2632", "rp2635"])],
        ["X05", badge("info", "low"), "Estate tax closing letter: previous fee",
         "The unpublished desk says the fee was raised from $67; the IRS says from $56 to $76 effective 26 October 2026 (T.D. 10055). The new fee matches. Owner of desk-b4f to correct.",
         links(["irs_new"])],
        ["X06", badge("info", "low"), "Published site lists 2026 federal figures only",
         "The live landing and tax pages say the IRS lists the 2026 estate threshold ($15,000,000). On 5 November 2026 the IRS published 2027 figures (basic exclusion $15,480,000; annual gift exclusion $20,000). They are official, not forecasts. Integration session to add them to the law-watch page.",
         links(["ir2026133", "rp2635"])],
        ["X07", badge("info", "low"), "Small-estate limit printed as current is stale",
         "The Self-Help page and the 552/V register row print $184,500. Judicial Council form DE-300 (rev. 28 April 2025) gives $208,850 for deaths on or after 1 April 2025 and $184,500 only for 1 April 2022 to 31 March 2025; next adjustment 1 April 2028. Legacy data files recorded the figure as unobtainable and quoted a competing $239,700, which appears nowhere on DE-300. Not used in any published decision; a home held in trust does not use this procedure.",
         links(["de300", "selfhelp"])],
        ["X08", badge("info", "low"), "Water growth differs between two parts of one desk",
         f"The projection table grows water costs 3.0% a year; the decision model grows them with inflation at 2.5%. Aligning them moves the sell-over-rent ratio from {rx(base['s3_s2'])} to {rx(wat['s3_s2'])} and changes no ordering. Both rates are above the CBO and SSA baselines.",
         links(["cbo", "ssa"])],
        ["X12", badge("warn", "medium"), "Two published desks, two headline levels",
         f"For the same decision the first desk shows Sell \u00f7 Rent of {rx(base['s3_s2'])} and the second {rx(a['their22']['their_s3_s2']) if a.get('their22') else 'n/a'}. Both rank Sell > Rent > Occupy and both show Treasuries-only losing to renting. The levels differ because of one assumption (after-tax return 4.5% against 5.6%, worth about {pc(a['groups22'][1]['s3_s2_pct'], 0) if a.get('groups22') else 'n/a'} on the ratio). The historical record does not choose between them (see Baselines). The integration session should show one set of assumptions or both as a range, not two unexplained levels.",
         links(["tsp", "erp56", "cbo"])],
        ["X13", badge("info", "low"), "One quantity, two figures inside the second desk",
         "The second desk shows Property B's yearly property tax as one figure on its summary and inheritance pages and a different one (about 4% higher) on its properties, costs and projections pages. Owner of desk-22a32b17 to align them.",
         links(["tax_collector"])],
        ["X10", badge("info", "low"), "Insurance assumption above published averages",
         f"The desk models A's insurance above both CDI averages ($2,339.99 statewide homeowners 2025; $1,571 California average, 27 October 2026); no county figure was found. Halving the cost moves the sell lead from {rx(base['s3_s2'])} to {rx(ins['s3_s2'])}; the ordering is unchanged. The desk flags this itself (F04).",
         links(["cdi", "cdi_eq"])],
    ]
    t = table(["ID", "Severity", "Topic", "Finding and effect", "Official source"], rows)
    body = f"""{t}
<h2>Process notes (no official source applies)</h2>
<ul>
<li><strong>X01 - where the decision numbers live (medium).</strong> The brief asks for decision numbers rounded to $10 in the decision analysis. They exist only in an unpublished desk (excluded from the site build). The published pages show no decision numbers and name no winner. The two readings conflict. The choice is reversible and belongs to the owner or the integration session. This referee's pages show ratios, rates and counts only.</li>
<li><strong>X09 - one guard for the exclusions (low).</strong> <code>scripts/verify_safe.py</code> requires only two exclusions in <code>_config.yml</code>. The exclusion of the unpublished desk and of the older trees rests on that file alone; removing one line would publish them with no check failing. <code>referee-abae/_src/crosscheck.py</code> reports which trees are published and scans them.</li>
<li><strong>X14 - the published trees draw the privacy line in different places (medium).</strong> The landing pages (<code>public-safe/</code>) name no places and show no owner-derived figures. <code>desk-22a32b17/</code>, which is also published, names two counties and shows the model's household anchors rounded to $10, in line with the brief's rounding rule; <code>desk-b4f/</code> does the same but is excluded from the site build. Under the brief's literal rule (round to $10, report in the decision analysis) the second desk complies; under the stricter reading adopted for the landing pages it does not. Neither reading publishes ZIP codes, addresses, parcel numbers or multi-year assessment histories (checked: none found in any published tree). The decision is the owner's or the integration session's; excluding a tree is one line in <code>_config.yml</code>.</li>
<li><strong>X11 - exclusion is not removal (medium, already known).</strong> Folders excluded from the site build remain readable in the public repository and its history (audit finding 1 in <code>audit-966/REPORT.md</code>). Fixing that needs the owner.</li>
<li><strong>Not a discrepancy, checked and cleared:</strong> an early reading suggested BOE publications name conflicting claim forms (BOE-58-H and BOE-19-P). Publication 800-9 uses BOE-19-P and BOE-19-G for children and grandchildren and BOE-58-H for a surviving cotenant, so there is no conflict.</li>
</ul>"""
    return page("discrepancies", "Discrepancies found", "Each item compares a published or desk figure with an official source, or tests a modelling choice. Effects are ratios.", body)


def page_flagged():
    rows = [
        ["F-A1", "Depreciation period of 27.5 years for residential rental buildings", "Topic 704 was read (land never depreciable) but the operative 27.5-year text in Publication 527 was not.", "Read the recovery-period table in Publication 527 or 946.", links(["p527", "tc704"])],
        ["F-A2", "Property A's actual tax rate", "The model uses a county-level approximation. The county tax rate book lists hundreds of tax-rate areas and A's was not identified (and is not published here). A 0.1-point change in rate moves the sell lead by about 2%.", "Read the rate for A's tax-rate area from the secured tax bill.", links(["county_rates"])],
        ["F-A3", "Gross rent for A", "Unverified assumption in the desk (its own flag F05). A 20% change moves the sell lead from about 1.43 to between 1.33 and 1.55.", "Obtain a market-rent appraisal; HUD Fair Market Rents are a floor, not a market rent.", links(["hud_fmr"])],
        ["F-A4", "Index used for future estate exclusions", "The Code adjusts the exclusion for inflation; the desk assumes 2.2% a year. The statutory index was not read.", "Read the inflation-adjustment sections cited in the revenue procedure.", links(["rp2635"])],
        ["F-A5", "Time between death and sale", "Not modelled: costs while the trust holds A, any gain or loss between the date-of-death value and the sale price, supplemental assessment. The BOE treats the death date, not the distribution date, as the change in ownership.", "Model a 6-18 month administration period once the trust terms are known.", links(["pub8009"])],
        ["F-A6", "Size of the decedent's estate and prior taxable gifts", "Headroom lines assume the estate is A plus cash. Gifts, portability and other assets change the answer.", "Needs the actual estate inventory; leave blank until then.", links(["irs_new", "rp2635"])],
        ["F-A7", "Consumer-price annual averages in the transcribed series", "Only home-price, S&P and BOE rows were spot-checked. BLS annual averages were not re-read.", "Re-read the annual averages from BLS or the FRED series.", links(["bls_cpi"])],
        ["F-A8", "Equity return approximation", "S&P price growth plus the mean dividend-price ratio. It is within 0.2 points of the TSP C Fund figure but is not a total-return index.", "Use an official total-return series if one is published.", links(["erp56", "tsp"])],
        ["F-A9", "Pending law, ballot measures and bills", "Not checked by this referee; covered by other sessions.", "See the law-watch pages and the official bill pages.", links(["leginfo"])],
    ]
    t = table(["ID", "Item", "Why it is unverified or open", "What would close it", "Where to check"], rows)
    body = f"""{t}
<h2>Process items</h2>
<ul>
<li><strong>Link liveness.</strong> The referee opened every URL on the Official constants page. The sandbox could not test the other links on the published pages from code, so their liveness is not confirmed here. <code>verify-552/</code> holds that register.</li>
<li><strong>Replication, not validation.</strong> The reference engine was written after reading the desk's model (see the Desk check page).</li>
<li><strong>Re-run.</strong> <code>python3 referee-abae/_src/build.py</code> rebuilds these pages from the repository state; <code>python3 -m unittest discover -s referee-abae/_src</code> runs the checks.</li>
</ul>"""
    return page("flagged", "Flagged for review", "What this referee could not confirm from an official source, and what would close each item.", body)


def page_index(a):
    rep = a.get("rep", {})
    n_const = len(R.CONSTANTS)
    n_open = sum(1 for c in R.CONSTANTS if c[4] == "opened")
    n_sec = n_const - n_open
    n_d = len(R.DESK_STATUTORY)
    n_match = sum(1 for d in R.DESK_STATUTORY if d[4].startswith("match"))
    scen = a.get("scen", [])
    n_keep = sum(1 for s in scen[1:] if not (s["flip_s3_s2"] or s["at_breakeven"] or s["flip_s2_s1"]))
    flips = [s["label"] for s in scen[1:] if s["flip_s3_s2"] or s["at_breakeven"] or s["flip_s2_s1"]]
    rng = a.get("ranges", {})
    sm = a.get("win_summary", {"n": 0})
    rows = [
        ["Published desk figures re-derived", f"{rep.get('row_ok', 0)} of {len(rep.get('row_checks', []))} reproduced within $10 (replication, not independent validation)", '<a href="traceability.html">Desk check</a>', links(["lta25009", "rp2635"])],
        ["Official constants register", f"{n_const} figures: {n_open} read in the official source, {n_sec} secondary-only", '<a href="constants.html">Official constants</a>', links(["ir2026133", "lta25009"])],
        ["Second desk (22a32b17) reproduced with the same engine", (f"sell path matches to rounding, rent path within {abs(a['rep22'][1]['s2']) * 100:.0f}%, occupy path within {abs(a['rep22'][1]['s1']) * 100:.0f}% (it also models Property B effects); the gap between the two desks' headline ratios ({rx(a['base'][2045]['s3_s2'])} against {rx(a['their22']['their_s3_s2'])}) is almost entirely the after-tax return assumption (4.5% against 5.6%)") if a.get("rep22") else "second desk not present in this checkout", '<a href="traceability.html">Desk check</a>', links(["tsp", "erp56"])],
        ["Statutory figures shown by the unpublished desk", f"{n_d} compared: {n_match} match, {n_d - n_match} mismatch (X04, X05)", '<a href="traceability.html">Desk check</a>', links(["rp2632", "irs_new"])],
        ["Ordering under the desk's own assumptions", ("Sell &gt; Rent &gt; Occupy in all three transfer windows; Sell &divide; Rent " + rx(rng['s3_s2'][0]) + "&ndash;" + rx(rng['s3_s2'][1])) if rng else "not computed", '<a href="robustness.html">Robustness</a>', links(["lta25009", "cbo"])],
        ["Stress tests", f"{n_keep} of {max(len(scen) - 1, 0)} stresses keep the ordering; it fails or sits at break-even under {len(flips)} (Treasuries only; growth at the 6.1% break-even)", '<a href="robustness.html">Robustness</a>', links(["cbo", "fhfa"])],
        ["History: 25 rolling windows", f"Sell beats Rent in {a.get('win_s3_wins_full_drag', 0)} of {sm['n']} windows with equities, {a.get('win_bond_wins', 0)} of {sm['n']} with Treasuries only; the desk's 4% home growth is below every window", '<a href="baselines.html">Baselines</a>', links(["fred_a", "erp56"])],
        ["Discrepancies logged", "10 against official sources or modelling choices, plus 4 process notes; none reverses the model's ordering", '<a href="discrepancies.html">Discrepancies</a>', links(["de300", "irs_new"])],
        ["Flagged for review", "9 open items the referee could not confirm", '<a href="flagged.html">Flagged</a>', links(["p527", "pub8009"])],
    ]
    t = table(["Check", "Result", "Page", "Official source"], rows)
    ind = a.get("indiff")
    body = f"""<p>Other sessions built decision desks. This referee does not add another; it checks them. It re-derives their numbers, tests their statutory
figures against official sources, and tries to break their conclusion with the stress tests and the historical record.</p>
<h2>Verdict at a glance</h2>{t}
<div class="note"><strong>Bottom line.</strong> The desk's arithmetic follows from its own rules, and nearly all its statutory figures match official sources (two small errors, X04 and X05).
Its ranking Sell &gt; Rent &gt; Occupy is robust to tax-rate choices, insurance, rent &plusmn;20%, a 27% price fall at transfer, and the terminal-tax convention. It is <em>not</em> robust to the
return on the proceeds: reinvested in Treasuries only, selling loses to renting in every historical window, and if home prices grow about 6.1% a year renting ties selling.
The ranking is therefore a bet on owning equities for 25 years, with inputs (rent, tax-rate area, transfer date) still unverified. The two published desks differ in level mostly because they assume different after-tax returns; the historical record places 4.5% below every 25-year window and 5.6% near the lower middle. Nothing here is a recommendation.</div>
<h2>The three paths, in plain words</h2>
{table(["Path", "What it means", "Official source"], [
    ["Occupy (S1)", "The heir moves into Property A. Property tax follows the Prop 19 family-home rules if the heir files for the homeowners' exemption within one year; the home-sale exclusion applies on a later sale.", links(["prop19", "hox", "tc701"])],
    ["Rent (S2)", "The heir keeps A and rents it. A is reassessed to market value; rental income is taxed with depreciation; the later sale triggers depreciation recapture and capital-gain tax.", links(["lta25009", "tc425", "tc409"])],
    ["Sell and reinvest (S3)", "A is sold at the stepped-up basis, so little or no gain tax, and the proceeds are reinvested at an after-tax return. Property B is already owned and is the same in all three paths.", links(["p551", "tc409"])],
])}
<h2>Not done by this referee</h2>
<ul><li>No property-specific input is verified here: rent, tax-rate area, insurance, repair costs and values are the desks' or the owner's.</li>
<li>No legal, tax or investment advice, and no forecast. Ratios describe a model.</li>
<li>No check of other sessions' pages beyond those listed; the cross-check script is ready to scan them once merged.</li></ul>
<h2>Re-run</h2><pre>python3 referee-abae/_src/build.py
python3 -m unittest discover -s referee-abae/_src
python3 referee-abae/_src/crosscheck.py</pre>"""
    return page("index", "Overview", "Re-deriving the desks' numbers, checking their statutory figures against official sources, and stress-testing their conclusion.", body)


def main():
    a = AN.compute()
    (OUT / "style.css").write_text(CSS, encoding="utf-8")
    pages = {"index": page_index(a), "constants": page_constants(), "traceability": page_traceability(a), "robustness": page_robustness(a),
             "baselines": page_baselines(a), "discrepancies": page_discrepancies(a), "flagged": page_flagged()}
    for slug, txt in pages.items():
        (OUT / f"{slug}.html").write_text(txt, encoding="utf-8")
    print("wrote", len(pages), "pages to", OUT)
    return a


if __name__ == "__main__":
    main()
