#!/usr/bin/env python3
"""Build the inheritance decision desk (static HTML) from data/model.json and the sourced rows below.

Run from the repository root:  python3 inheritance-desk/_src/build.py
Writes HTML pages one level above this folder (inheritance-desk/*.html).
Every table row carries an official-source link, or the value is left blank and flagged.
Money is rounded to the nearest $10; statutory amounts are shown as published and marked.
"""
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DESK = HERE.parent
MODEL = json.loads((DESK / "data" / "model.json").read_text())

# ---------- official sources (each URL was opened during research; see flagged.html for pending ones)
S = {
    "irs_estate": "https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax",
    "irs_rp": "https://www.irs.gov/pub/irs-drop/rp-25-32.pdf",
    "irs_whatsnew": "https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax",
    "irs_filing": "https://www.irs.gov/businesses/small-businesses-self-employed/filing-estate-and-gift-tax-returns",
    "irs_p551": "https://www.irs.gov/publications/p551",
    "irs_tc701": "https://www.irs.gov/taxtopics/tc701",
    "irs_tc409": "https://www.irs.gov/taxtopics/tc409",
    "irs_tc559": "https://www.irs.gov/taxtopics/tc559",
    "rtc51": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=51",
    "boe_prop19": "https://www.boe.ca.gov/Prop19/",
    "boe_lta": "https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf",
    "sos_failed": "https://www.sos.ca.gov/elections/ballot-measures/initiative-and-referendum-status/failed-qualify",
    "sos_certified": "https://www.sos.ca.gov/administration/news-releases-and-advisories/2026-news-releases-and-advisories/california-secretary-state-shirley-n-weber-phd-certifies-measures-november-3-2026-general-election-ballot",
    "ftb_news": "https://www.ftb.ca.gov/about-ftb/newsroom/tax-news/index.html",
    "fed_1929": "https://www.federalreservehistory.org/essays/stock-market-crash-of-1929",
    "fed_2007": "https://www.federalreservehistory.org/essays/great-recession-of-200709",
    "fed_goal": "https://www.federalreserve.gov/monetarypolicy/monetary-policy-strategy-tools-and-communications-statement-on-longer-run-goals-monetary-policy-strategy-2025.htm",
    "treasury": "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202611",
    "sc_rate_book": "https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf",
    "sc_annual": "https://files.santaclaracounty.gov/exjcpb1521/2025-11/annual_report_2025-2026.pdf",
    "cdi": "https://www.insurance.ca.gov/",
}

LABEL = {k: k for k in S}


def link(key, text=None):
    text = text or key
    return f'<a href="{html.escape(S[key])}" rel="noopener">{html.escape(text)}</a>'


def money(x):
    """Round to nearest $10 and format."""
    v = int(round(x / 10.0) * 10)
    return ("&minus;$" if v < 0 else "$") + f"{abs(v):,}"


def stat_money(text):
    """Statutory amounts: shown exactly as published."""
    return f'<span class="stat">{html.escape(text)}</span> <span class="muted">(published)</span>'


def badge(code):
    names = {"V": "verified", "P": "published", "O": "owner input", "A": "assumption", "D": "derived", "X": "flagged"}
    return f'<span class="badge b-{code}" title="{names[code]}">{code}</span>'


# ---------- page shell
NAV = [
    ("index.html", "Executive summary"),
    ("what-changes.html", "What would change the answer"),
    ("facts.html", "Federal and CA rules"),
    ("property.html", "Property facts (inputs)"),
    ("scenarios.html", "Scenarios: live / rent / sell"),
    ("black-swans.html", "Black-swan regimes & phased entry"),
    ("projections.html", "Projections 2026–2050"),
    ("costs.html", "Operating costs"),
    ("process.html", "Trust process & deadlines"),
    ("glossary.html", "Glossary"),
    ("questions.html", "Questions & information gaps"),
    ("suggestions.html", "Suggestions (awaiting owner approval)"),
    ("briefing.html", "Attorney & CPA briefing (print)"),
    ("methodology.html", "Methodology & model inputs"),
    ("flagged.html", "Flagged for Review"),
]


def page(name, title, body, lead="", one_page=False):
    nav = "".join(
        f'<a href="{href}" class="{"active" if href == name else ""}">{html.escape(label)}</a>'
        for href, label in NAV
    )
    cls = " one-page" if one_page else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · Inheritance decision desk</title>
<link rel="stylesheet" href="assets/style.css">
</head><body>
<div class="layout">
<nav class="menu no-print"><div class="brand">Inheritance decision desk</div>
<div class="muted" style="margin-bottom:8px">Privacy-first. Property A / Property B. Not advice.</div>
{nav}
</nav>
<main class="{cls.strip()}">
<h1>{html.escape(title)}</h1>
{f'<p class="lead">{lead}</p>' if lead else ''}
{body}
<div class="disclaimer">Educational analysis, not legal, tax or investment advice. Figures are rounded to the nearest $10
unless a statutory amount is marked "published". Each table row shows its source; blank values are unverified and listed on the
<a href="flagged.html">Flagged for Review</a> page. Owner inputs are labelled and are not independently verified.</div>
</main></div></body></html>
"""


def table(headers, rows, num_cols=()):
    h = "".join(f'<th class="{"num" if i in num_cols else ""}">{html.escape(x)}</th>' for i, x in enumerate(headers))
    body = []
    for r in rows:
        blank = any(c == "" for c in r[1:2])
        cells = []
        for i, c in enumerate(r):
            cls = "num" if i in num_cols else ""
            cells.append(f'<td class="{cls}">{c}</td>')
        body.append(f'<tr class="{"blank" if blank else ""}">' + "".join(cells) + "</tr>")
    return f'<table><thead><tr>{h}</tr></thead><tbody>{"".join(body)}</tbody></table>'


def flag(code):
    return f'<a href="flagged.html#{code}" class="tag-flag">[{code}]</a>'


# ---------- derived model values
def grid_val_kw(T, option, regime, kw):
    for g in MODEL["grid"]:
        if g["T"] == T and g["option"] == option and g["regime"] == regime and g["kw"] == kw:
            return g["wealth"]
    raise KeyError((T, option, regime, kw))


OPT_ROWS = [
    ("live", {"avoid_rent": True}, "A. Live in it (rent avoided counted)"),
    ("live", {"avoid_rent": False}, "A0. Live in it, cash only"),
    ("rent", {}, "B. Rent it out"),
    ("sell_lump", {}, "C. Sell at transfer; invest at once"),
    ("sell_phased", {"park_months": 24}, "D. Sell; park 24 months; phase in over 12"),
    ("sell_phased", {"park_months": 36}, "E. Sell; park 36 months; phase in over 12"),
    ("mixed_live_rent", {"avoid_rent": True}, "F. Live 1 year, then rent"),
    ("mixed_live_sell", {"live_years": 10, "avoid_rent": True}, "G. Live 10 years, then sell at once"),
]
REG_ROWS = [
    ("base", "Base"),
    ("stagflation", "Stagflation"),
    ("low_growth", "Low growth"),
    ("crash_2008", "2008-style crash at transfer (proxy)"),
    ("crash_1929", "1929-style crash at transfer (proxy)"),
]
MODEL_SRC = ' <span class="muted">Model output, assumption-driven; inputs: ' + ", ".join(
    [link("treasury", "Treasury"), link("fed_goal", "Fed 2% goal"), link("irs_p551", "IRS Pub 551"),
     link("irs_tc701", "IRS §121"), link("rtc51", "RTC §51")]) + ". See methodology.</span>"


def headline_row(T=2040, regime="base"):
    rows = []
    for key, kw, label in OPT_ROWS:
        v = grid_val_kw(T, key, regime, kw)
        rows.append([label, money(v), badge("D") + " " + link("irs_p551", "Pub 551 basis")])
    return rows


# ---------- PAGES
def p_index():
    live = grid_val_kw(2040, "live", "base", {"avoid_rent": True})
    rent = grid_val_kw(2040, "rent", "base", {})
    sell = grid_val_kw(2040, "sell_lump", "base", {})
    be = MODEL["break_even_rent_yield_2040_base"] * 100
    cash_be = MODEL["cash_only_vs_rent_break_even_gross_yield_2040_base"] * 100
    body = f"""
<div class="card change">
<h2 style="margin-top:0">What would change the answer (read first)</h2>
<ul>
<li><b>The rent you avoid.</b> If the heir would otherwise pay rent, living in the house beats renting it out only while the avoided rent is worth more than about <b>{be:.2f}%</b> of value a year (base case, 2040 transfer; the model assumes 4.00%). If the heir would not pay rent elsewhere (cash-only, A0), renting it out beats living there once the gross rent yield exceeds about <b>{cash_be:.2f}%</b>.</li>
<li><b>Stock returns.</b> The sell-and-invest result is driven by the assumed stock return (6% base, 3%–4% in weaker regimes). A lower return favours keeping the house.</li>
<li><b>The economic regime.</b> In the stagflation regime (5% inflation, 4% stocks), living in the house ranks first: {money(grid_val_kw(2040,'live','stagflation',{'avoid_rent':True}))} against {money(grid_val_kw(2040,'sell_lump','stagflation',{}))} for selling and investing at once. In the base regime selling ranks first. See <a href="scenarios.html">Scenarios</a>.</li>
<li><b>A crash at transfer.</b> A 1929-style or 2008-style fall right after transfer changes the ranking. Phased entry only helps if it happens to enter after a fall, which nobody can know in advance (see black-swan page).</li>
<li><b>The Prop 19 cap wording.</b> Official pages describe the cap two ways (see <a href="flagged.html#F03">F03</a>). The result changes with the wording used.</li>
<li><b>Property tax rate.</b> Your tax-rate-area composite rate is not yet confirmed (<a href="flagged.html#F01">F01</a>).</li>
</ul></div>

<h2>Executive summary (2040 transfer, base regime, 2026 dollars)</h2>
<p>These are model outputs, not forecasts. They show end-of-model (2076) wealth in 2026 dollars under one set of assumptions.</p>
<div class="grid3">
<div class="card"><div class="kpi-label">A. Live in it (rent avoided counted)</div><div class="kpi stat">{money(live)}</div></div>
<div class="card"><div class="kpi-label">B. Rent it out</div><div class="kpi stat">{money(rent)}</div></div>
<div class="card"><div class="kpi-label">C. Sell at transfer, invest at once</div><div class="kpi stat">{money(sell)}</div></div>
</div>
<p class="muted">Under these assumptions, selling and investing at once ranks first. The gap depends on the assumed stock return and the rent credit. See <a href="scenarios.html">Scenarios</a> and <a href="methodology.html">Methodology</a>. Live-in with no credit for avoided rent (A0) is shown on the Scenarios page.</p>

<h2>Where to start</h2>
<div class="grid2">
<div class="card"><b>Inherit with the trust:</b> <a href="process.html">step-by-step process and deadlines</a>.</div>
<div class="card"><b>Rules and thresholds:</b> <a href="facts.html">federal and California rules</a>, with official links.</div>
<div class="card"><b>Give to your advisers:</b> <a href="briefing.html">one-page briefing (print)</a>.</div>
<div class="card"><b>Open items:</b> <a href="flagged.html">Flagged for Review</a> and <a href="questions.html">information gaps</a>.</div>
</div>
<p class="muted">Owner inputs (values, rent, utilities, insurance) are used in the model but are not yet verified. They are listed on the <a href="property.html">Property facts</a> page.</p>
"""
    return page("index.html", "Executive summary", body,
                lead="Inheritance decision for Property A, with rental and owner-occupancy options for Property B. Source-linked; privacy-first.")


def p_what():
    rows = []
    for T in (2040, 2045, 2050):
        r = [str(T)]
        for key, kw in [("live", {"avoid_rent": True}), ("rent", {}), ("sell_lump", {})]:
            r.append(money(grid_val_kw(T, key, "base", kw)))
        r.append(badge("D") + " " + link("treasury", "Treasury") + ", " + link("rtc51", "RTC §51"))
        rows.append(r)
    t1 = table(["Transfer year", "A. Live", "B. Rent", "C. Sell at once", "Source"], rows, num_cols=(1, 2, 3))
    sens = MODEL["sens_tax_rate"]
    srows = []
    for k in ("1.12", "1.20", "1.24", "owner_implied"):
        s = sens[k]
        srows.append([("Owner-implied rate" if k == "owner_implied" else f"{float(k):.2f}%"),
                      f"{s['rate']*100:.2f}%", money(s["live"]), money(s["rent"]),
                      badge("A") + " " + flag("F01") + " " + link("sc_rate_book", "Tax Rate Book")])
    t2 = table(["Composite tax rate case", "Rate", "A. Live (2040 base)", "B. Rent (2040 base)", "Status and source"], srows, num_cols=(1, 2, 3))
    body = f"""
<div class="card change">
<p><b>Break-even avoided rent:</b> living in the house (counting avoided rent) matches renting it out when the avoided rent is worth about <b>{MODEL['break_even_rent_yield_2040_base']*100:.2f}%</b> of value a year (2040 transfer, base regime). The model assumes 4.00%. <b>Cash-only living</b> (A0) matches renting out at a gross yield of about <b>{MODEL['cash_only_vs_rent_break_even_gross_yield_2040_base']*100:.2f}%</b>.</p>
</div>
<h2>Transfer-year sensitivity (base regime)</h2>
{t1}
<p class="muted">Model output. Source for inputs: {link('treasury','Treasury')}, {link('fed_goal','Fed 2% goal')}, {link('irs_p551','IRS Pub 551')}.</p>
<h2>Property tax rate sensitivity (2040 base)</h2>
{t2}
<p class="muted">The composite rate is not verified. Santa Clara County's {link('sc_rate_book','Tax Rate Book 2025–26')} sets a 1% levy plus voter-approved debt, and rates vary by tax rate area. The rate for the specific area has to be read from the owner's own bill; that step is not done here.</p>
<h2>Questions that change the answer</h2>
<ul>
<li>Would the heir otherwise pay rent of the same value? If not, the avoided-rent credit does not apply and A0 is the right comparison.</li>
<li>Is the heir likely to move in within 1 year of transfer? That is required to keep the Prop 19 parent-child benefit (BOE rules, <a href="facts.html">Federal and CA rules</a>).</li>
<li>Does the trust hold the property, and is it a revocable or irrevocable trust? (Not modelled; see <a href="questions.html">questions</a>.)</li>
</ul>"""
    return page("what-changes.html", "What would change the answer", body,
                lead="The answer depends on a few inputs. The sensitivities below show how much each one moves the result.")


def p_facts():
    fed = [
        ["Federal estate and gift basic exclusion, 2026 (per person)", stat_money("$15,000,000"), link("irs_estate", "IRS estate tax")],
        ["Annual gift exclusion, 2026 (per recipient)", stat_money("$19,000"), link("irs_rp", "Rev. Proc. 2025-32")],
        ["Gift and estate top rate", "40%", link("irs_estate", "IRS estate tax")],
        ["Non-citizen spouse marital deduction limit, 2026", stat_money("$194,000"), link("irs_rp", "Rev. Proc. 2025-32")],
        ["Form 706 (estate return) due", "9 months after death; 6-month extension if requested before the due date and estimated tax paid", link("irs_filing", "IRS filing guide")],
        ["Form 709 (gift return) due", "April 15 of the year after the gift", link("irs_filing", "IRS filing guide")],
        ["Basis of inherited property", "Generally fair market value at date of death (or alternate valuation date if elected)", link("irs_p551", "IRS Pub 551")],
        ["Long-term capital gains 0% rate, single (2026)", stat_money("$49,450"), link("irs_rp", "Rev. Proc. 2025-32 §4.03")],
        ["Long-term capital gains 15% rate, single (2026)", "up to " + stat_money("$545,500"), link("irs_rp", "Rev. Proc. 2025-32 §4.03")],
        ["Estates and trusts: 0% capital gains up to (2026)", stat_money("$3,300"), link("irs_rp", "Rev. Proc. 2025-32 §4.03")],
        ["Estates and trusts: 15% capital gains up to (2026)", stat_money("$16,250"), link("irs_rp", "Rev. Proc. 2025-32 §4.03")],
        ["Net investment income tax (3.8%) threshold, single", stat_money("$200,000 (not indexed)"), link("irs_tc559", "IRS Topic 559")],
        ["Home-sale exclusion, single (2 of 5 years use and ownership)", stat_money("$250,000"), link("irs_tc701", "IRS Topic 701")],
        ["Home-sale exclusion, married filing jointly", stat_money("$500,000"), link("irs_tc701", "IRS Topic 701")],
        ["Capital gains rate structure", "0%, 15%, 20% brackets (see IRS page for thresholds)", link("irs_tc409", "IRS Topic 409")],
        ["Estate-and-trust closing letter fee from Oct 26, 2026", stat_money("$76"), link("irs_whatsnew", "IRS what's new")],
    ]
    ca = [
        ["California estate tax or inheritance tax", flag("F05") + " not confirmed from a primary source here", link("ftb_news", "FTB newsroom (no estate tax item)")],
        ["Prop 19 parent-child: transferred home must become the child's principal residence", "Yes, see BOE", link("boe_prop19", "BOE Prop 19")],
        ["Prop 19 cap, current 2025–2027 figure", stat_money("$1,044,586") + " added to base-year value (LTA 2025/009)", link("boe_lta", "BOE LTA 2025/009")],
        ["Prop 19 cap wording", "Conflict: BOE page says \"current taxable value plus <span class='stat'>$1,000,000</span>\"; BOE LTA says \"factored base year value plus <span class='stat'>$1,044,586</span>\". " + flag("F03"), link("boe_prop19", "BOE Prop 19")],
        ["Property tax base rate (1% levy plus voter-approved debt)", "1% of assessed value plus bond debt", link("rtc51", "RTC §51"), ],
        ["Assessed-value annual growth limit", "Lesser of 2% or California CPI change", link("rtc51", "RTC §51")],
        ["Prop 19 repeal or change on the 2026 ballot", "Not confirmed. " + flag("F04"), link("sos_certified", "SOS certified measures (not opened line by line)")],
    ]
    hist = [
        ["1929 Dow peak to trough (Sept 1929 to July 1932)", "About 89% decline", link("fed_1929", "Fed History: 1929")],
        ["2007–2009 S&P 500 peak to trough", "57% decline (Oct 2007 to Mar 2009)", link("fed_2007", "Fed History: Great Recession")],
        ["2007–2009 home prices, mid-2006 to mid-2009", "About 30% decline", link("fed_2007", "Fed History: Great Recession")],
        ["Fed inflation goal", "2% PCE", link("fed_goal", "Fed statement 2025")],
        ["Treasury 3-month yield, Nov 13, 2026", "4.32%", link("treasury", "Treasury par yields")],
        ["Treasury 2-year yield, Nov 13, 2026", "4.88%", link("treasury", "Treasury par yields")],
    ]
    body = f"""
<h2>Federal estate, gift and income tax (2026)</h2>
{table(["Item", "Value", "Official source"], fed, num_cols=())}
<h2>California</h2>
{table(["Item", "Value", "Official source"], ca)}
<p class="muted">California estate and inheritance tax: none is charged under current law by the FTB's published information. The primary check is still open ({flag('F05')}).</p>
<h2>Historical and market data</h2>
{table(["Item", "Value", "Official source"], hist)}
<p class="muted">Treasury and Fed figures are as published. The 1929 and 2007–09 declines are from Fed History essays.</p>
"""
    return page("facts.html", "Federal and California rules", body,
                lead="Rules and thresholds as published by the IRS, California Legislature, BOE and Fed. Statutory amounts are shown as published.")


def p_property():
    o = MODEL["owner"]
    owner_list = [
        f"Property A, estimated market value (Nov 2026): {money(o['A_fmv_2026'])}",
        f"Property A, 2026 assessed value (owner figure, rounded): {money(o['A_fbyv_2026'])}",
        "Owner-held historical assessment series: not published on this site (flag F08)",
        f"Property B, estimated market value (Nov 2026): {money(o['B_fmv_2026'])}",
        "Property B, rent from two units: about $7,150 a month (owner figure)",
        "Property B, water: $330–$400 a month; electricity: $30–$70 a month (owner ranges)",
        "Property A, water: $100–$150 a month; solar credit: about $10–$20 a month profit (owner ranges)",
        "Insurance: about $1,500 a year (owner estimate)",
    ]
    rows = [
        ["Property A, 2026 assessed value", "Blank", "County assessor record", flag("F09")],
        ["Property A, 2025 property tax", "Blank", "Tax bill", flag("F02")],
        ["Property B, 2025 assessed value", "Blank", "Assessor record", flag("F02")],
        ["Property B, 2025 property tax", "Blank", "Tax bill", flag("F02")],
        ["Property B, monthly rent (two units)", "Blank", "Lease records", flag("F02")],
        ["Property A and B market values (Nov 2026)", "Blank", "Independent appraisal or county data", flag("F02")],
    ]
    body = f"""
<div class="card"><b>Privacy:</b> the site shows no addresses, names, parcel or account numbers. Property A is the house to be inherited; Property B is the house already owned and rented.</div>
<h2>Owner-supplied figures (not verified)</h2>
<p>The owner's figures are used as model inputs. They have no official confirmation yet and are not shown in the verified tables.</p>
<ul>{''.join(f'<li>{html.escape(x)}</li>' for x in owner_list)}</ul>
<h2>Official records still needed</h2>
{table(["Item", "Value", "Official record", "Status"], rows)}
<h2>Assessment rules that apply</h2>
<ul>
<li>Assessed value resets to market value on a change in ownership, except where Prop 19 applies (see <a href="facts.html">Federal and CA rules</a>).</li>
<li>Annual growth in assessed value is capped at the lesser of 2% or the California CPI change (RTC §51, {link('rtc51','official text')}).</li>
</ul>
"""
    return page("property.html", "Property facts (inputs)", body,
                lead="Owner-supplied inputs and the rules that apply to them. Official records are needed before any value is treated as verified.")


def p_scen():
    t = table(["Option (2040 transfer)"] + [r[1] for r in REG_ROWS] + ["Source"],
              [[label] + [money(grid_val_kw(2040, key, reg, kw)) for reg, _ in REG_ROWS]
               + [badge("D") + " " + link("treasury", "Treasury") + ", " + link("irs_p551", "Pub 551")]
               for key, kw, label in OPT_ROWS],
              num_cols=(1, 2, 3, 4, 5))
    rein = MODEL["reinvestment"]
    rrows = []
    for rate in ("3.00", "4.32"):
        for reg, lab in REG_ROWS:
            r = rein[rate][reg]
            src = link("fed_1929", "Fed: 1929") if reg == "crash_1929" else (link("fed_2007", "Fed: 2007–09") if reg.startswith("crash") else link("treasury", "Treasury"))
            rrows.append([f"{rate}%", lab, money(r["sell_lump"]), money(r["sell_phased_24"]), money(r["sell_phased_36"]),
                          (badge("X") + " " + flag("F07")) if reg.startswith("crash") else badge("D"), src])
    body = f"""
<div class="card change">
<b>Reinvestment and opportunity risk.</b> Selling and investing at once means you may invest just before a fall. Parking cash and
phasing it in can reduce that, but only if the entry happens to be after the fall. The model's crash results are on one assumed path,
and a phased investor who entered at the bottom would look better only in hindsight. Read the black-swan page before using these numbers.
</div>
<h2>Options by economic regime (2040 transfer, 2026 dollars)</h2>
{t}
<p class="muted">Options D and E are shown under each regime with their stated park period. Live and rent options hold no stocks, so a stock crash does not change them; both crash columns use the 2008 housing proxy, which is why those two columns match for A, A0 and B ({flag('F07')}). {MODEL_SRC}</p>
<h2>Headline comparison (base regime)</h2>
{table(["Option", "2040 base", "Source"], headline_row(2040, "base"), num_cols=(1,))}
<h2>Reinvestment risk: phased entry versus sell-at-once (2040 transfer)</h2>
{table(["T-bill park rate", "Regime", "Sell, invest at once", "Park 24m, then phase", "Park 36m, then phase", "Status", "Source"], rrows, num_cols=(2,3,4))}
<p class="muted">Park rate 4.32% is the 3-month Treasury yield on Nov 13, 2026 ({link('treasury','Treasury')}); 3.00% is a low case. Stock path and crash shape are assumptions.</p>
"""
    return page("scenarios.html", "Scenarios: live, rent, sell", body,
                lead="Eight options under five economic regimes. The 2040 transfer year is the headline; other transfer years are on the What-would-change page.")


def p_black():
    body = f"""
<div class="card change">
<p><b>Why this page matters.</b> A black-swan crash right after transfer changes the ranking. The model tests two historical-style paths:
a 1929-style fall (stocks down 89%, about 34 months to trough, about 22 years to regain the peak) and a 2008-style fall (stocks down 57%, about 17 months to trough).</p>
<p><b>What is not established:</b> the 1929 housing path is a proxy (2008 housing, flagged {flag('F07')}). The phased-entry results depend on the crash timing and cannot be used as a forecast.</p>
</div>
<h2>Source figures</h2>
{table(["Figure", "Value", "Official source"], [
 ["1929 stock decline, peak to trough", "About 89%", link("fed_1929", "Fed History: 1929")],
 ["2007–09 stock decline, peak to trough", "57%", link("fed_2007", "Fed History: Great Recession")],
 ["2007–09 home price decline", "About 30%", link("fed_2007", "Fed History: Great Recession")],
])}
<h2>Phased entry: what the model shows</h2>
<p>In the 1929-style path the phased entry outcome is far above the sell-at-once outcome. This follows from entering near the trough of a path the model already knows. It is shown to illustrate sensitivity, not as a plan. Do not treat it as evidence that waiting pays.</p>
<p>Pending review: the 1929 phased results exceed the base-regime sell-at-once result, and the 2008 phased result is also high. Both are under review ({flag('F07')}).</p>
"""
    return page("black-swans.html", "Black-swan regimes and phased entry", body,
                lead="How the ranking changes under a 1929-style or 2008-style crash at transfer, and why phased entry is path-dependent.")


def p_proj():
    rows = []
    for t in MODEL["trajectory"]:
        rows.append([str(t["year"]), money(t["home"]), money(t.get("av_pre", 0)), money(t.get("tax_pre", 0)),
                     badge("D") + " " + link("rtc51", "RTC §51")])
    t1 = table(["Year", "Property A market value (model, 2%/yr)", "Assessed value, no transfer (Prop 13 path)", "Property tax, no transfer", "Source"], rows, num_cols=(1, 2, 3))
    last = MODEL["trajectory"][-1]
    t2 = table(["Measure (2050, nominal model values)", "Live (Prop 19)", "Rent (full reassessment)", "Source"], [
        ["Assessed value after transfer", money(last["av_live_2050"]), money(last["av_rent_2050"]), link("boe_prop19", "BOE Prop 19")],
        ["Annual property tax after transfer", money(last["tax_live_2050"]), money(last["tax_rent_2050"]), link("sc_rate_book", "Tax Rate Book")],
    ], num_cols=(1, 2))
    body = f"""
<div class="card change"><b>Model, not a forecast.</b> Market value grows at 2% a year in the base case. Assessed value follows the 2% cap. Figures are nominal and rounded to the nearest $10.</div>
<h2>Trajectory 2026–2050 (no transfer)</h2>
{t1}
<p class="muted">Growth rates are assumptions ({link('fed_goal','Fed 2% goal')} is used for inflation in the base case; {link('rtc51','RTC §51')} sets the 2% assessment cap).</p>
<h2>After transfer, 2050</h2>
{t2}
"""
    return page("projections.html", "Projections 2026–2050", body,
                lead="Market value, assessed value and property tax projected to 2050 under the base case.")


def p_costs():
    rows = [
        ["Homeowners insurance (Property A, annual, owner estimate)", "Blank", "Not confirmed", flag("F06")],
        ["Water (Property A, monthly, owner range $100–$150)", "Blank", "Provider rate not confirmed", flag("F06")],
        ["Water (Property B, monthly, owner range $330–$400)", "Blank", "Provider rate not confirmed", flag("F06")],
        ["Electricity (Property B, monthly, owner range $30–$70)", "Blank", "Provider rate not confirmed", flag("F06")],
        ["Solar credit (Property A, monthly, owner range $10–$20)", "Blank", "Bill needed", flag("F06")],
        ["Maintenance", "0.2% of value a year (model assumption; no external source)", "Assumption, no official source", flag("F12")],
    ]
    body = f"""
<div class="card change"><b>Insurance estimate not verified.</b> The state insurance regulator's average homeowners premium figures were not confirmed from a primary source. Secondary sites disagree widely, so no average is published here.</div>
<h2>Operating costs</h2>
{table(["Cost", "Value", "Status", "Flag", "Source to check"], [r + [link("cdi", "CDI")] if "Maintenance" not in r[0] else r + ["No external source (assumption)"] for r in rows])}
<p class="muted">Primary source to check: {link('cdi','California Department of Insurance')}. Owner ranges are used in the model after rounding to the nearest $10 (water $130 a month; solar credit $20 a month; insurance $1,500 a year). The model's insurance figure is owner-supplied and unverified.</p>
"""
    return page("costs.html", "Operating costs", body, lead="Insurance, water, electricity and maintenance. Only confirmed rates would be shown as verified.")


def p_process():
    steps = [
        ("Now", "Gather the trust document, the deed, and the last three assessment notices. Ask the attorney which trust type holds Property A."),
        ("At death", "Get death certificates. Notify the trustee. The trust (not the estate) usually holds the house. Do not change the title yet."),
        ("Within 9 months", "If an estate tax return is needed, file Form 706 with the IRS. Request a 6-month extension before the due date if the estimated tax is not paid in full (see the IRS filing guide)."),
        ("Within 1 year", "If the heir will live in the house, move in and claim the homeowners' exemption. Prop 19 requires the house to become the child's principal residence within 1 year (BOE)."),
        ("Within 3 years", "File BOE-19-P to claim the Prop 19 parent-child exclusion, or before any third-party transfer (BOE Prop 19 page)."),
        ("Each year", "Property tax bills: secured tax installments are due Nov 1 and Feb 1; delinquent after Dec 10 and Apr 10 (Santa Clara County Tax Rate Book)."),
        ("At sale", "Basis is generally the value at death, which limits capital gains tax. Check the Form 8971 value from the executor."),
    ]
    tl = "".join(f'<div class="step"><div class="when">{html.escape(w)}</div><div>{html.escape(t)}</div></div>' for w, t in steps)
    body = f"""
<div class="card change"><b>This is a planning checklist, not legal advice.</b> Trust and estate steps depend on the document and the state. Confirm with an estate attorney.</div>
<h2>Timeline</h2>
<div class="timeline">{tl}</div>
<h2>Deadlines with sources</h2>
{table(["Deadline", "Rule", "Official source"], [
 ["Form 706 (estate return)", "9 months after death; extension of 6 months if requested before due date", link("irs_filing", "IRS filing guide")],
 ["Form 709 (gift return)", "April 15 of the year after the gift", link("irs_filing", "IRS filing guide")],
 ["Prop 19 claim BOE-19-P", "Within 3 years of transfer, or before a third-party transfer", link("boe_prop19", "BOE Prop 19")],
 ["Homeowners' exemption after Prop 19 transfer", "Within 1 year", link("boe_prop19", "BOE Prop 19")],
 ["Secured property tax, first installment", "Due Nov 1; delinquent after Dec 10", link("sc_rate_book", "Santa Clara Tax Rate Book")],
 ["Secured property tax, second installment", "Due Feb 1; delinquent after Apr 10", link("sc_rate_book", "Santa Clara Tax Rate Book")],
])}
"""
    return page("process.html", "Trust process and deadlines", body,
                lead="Step-by-step, from now to sale, with the dates that matter.")


def p_gloss():
    items = [
        ("Basis", "The tax value used to measure gain when property is sold. For inherited property it is generally the value at death.", "irs_p551"),
        ("Prop 19", "California rule letting a parent-child transfer keep a lower assessed value if the child moves in and makes it their main home.", "boe_prop19"),
        ("Assessed value", "The value on which property tax is charged. In California it resets on a change in ownership unless an exclusion applies.", "rtc51"),
        ("Basic exclusion amount", "The amount a person can pass free of federal estate or gift tax (2026: <span class='stat'>$15,000,000</span>).", "irs_estate"),
        ("Form 706", "Federal estate tax return.", "irs_filing"),
        ("Form 709", "Federal gift tax return.", "irs_filing"),
        ("Net investment income tax", "A 3.8% tax on some investment income above a threshold.", "irs_tc559"),
        ("T-bill", "A short-term US Treasury bill. The model uses a 3-month T-bill for parked cash.", "treasury"),
        ("Phased entry", "Moving cash into stocks in equal instalments over time, instead of all at once.", None),
        ("Break-even rent yield", "The gross rent (as a share of value) at which living in the house and renting it out give the same result.", None),
        ("Regime", "A set of economic assumptions (inflation, stock return, housing growth) applied to the model.", None),
    ]
    rows = [[t, d, link(k) if k else "Model definition (no external source)"] for t, d, k in items]
    body = table(["Term", "Meaning", "Source"], rows)
    return page("glossary.html", "Glossary", body, lead="Plain-language meanings for the terms used in this desk.")


def p_questions():
    qs = [
        ["Trust type and terms (revocable or irrevocable; who the trustee is).", "Changes which rules and timelines apply."],
        ["Whether the heir would otherwise pay rent of the same value.", "Decides whether the avoided-rent credit applies (A vs A0)."],
        ["Whether the heir will live in the house within 1 year of transfer.", "Needed for the Prop 19 benefit."],
        ["Confirmed assessed value and tax bill for both properties.", "Replaces owner-supplied inputs."],
        ["Property A's tax-rate-area composite rate (from the bill).", "Changes property tax (F01)."],
        ["Insurance quote for both houses.", "Replaces the $1,500 a year estimate (F06)."],
        ["Current leases and rent for Property B.", "Replaces the owner's estimate (F02)."],
        ["Whether the heir's state of residence has any estate tax.", "Only California is covered here; the heir's state is not known."],
    ]
    body = table(["Question or information gap", "Why it matters", "Source"], [q + ["No external source (owner question)"] for q in qs])
    return page("questions.html", "Questions and information gaps", body,
                lead="These answers would change the model or the rules. None is required to read this desk.")


def p_suggest():
    items = [
        ["S1", "Obtain assessor records for both properties and replace the owner inputs.", "Proposed; awaiting owner approval"],
        ["S2", "Confirm the Prop 19 cap wording with BOE before relying on it (F03).", "Proposed; awaiting owner approval"],
        ["S3", "Replace the 1929 housing proxy with a sourced housing path (F07).", "Proposed; awaiting owner approval"],
        ["S4", "Get a CDI-based insurance quote for each property (F06).", "Proposed; awaiting owner approval"],
    ]
    srcs = {"S1": link("sc_annual", "County assessor report"), "S2": link("boe_prop19", "BOE Prop 19"),
            "S3": link("fed_2007", "Fed History"), "S4": link("cdi", "CDI")}
    items = [i + [srcs[i[0]]] for i in items]
    body = table(["No.", "Suggestion", "Status", "Source to check"], items) + """
<p class="muted">Nothing on this page is implemented. Each suggestion needs an owner decision (accept, change or reject) before it is acted on.</p>"""
    return page("suggestions.html", "Suggestions (awaiting owner approval)", body,
                lead="Changes proposed for the desk. Not yet approved by the owner.")


def p_brief():
    live = grid_val_kw(2040, "live", "base", {"avoid_rent": True})
    rent = grid_val_kw(2040, "rent", "base", {})
    sell = grid_val_kw(2040, "sell_lump", "base", {})
    body = f"""
<div class="one-page">
<p class="muted">Briefing for attorney and CPA. Not advice. Property A and Property B. Full detail on the desk pages.</p>
<h2>Question</h2>
<p>Property A is expected to pass by trust around 2040–2050. Choose: live in it, rent it out, or sell and invest. Mixed paths also modelled.</p>
<h2>Headline (2040 transfer, base, 2026 dollars)</h2>
<div class="card">Live (rent avoided counted) {money(live)} · Rent {money(rent)} · Sell and invest at once {money(sell)}.
Break-even avoided rent about {MODEL['break_even_rent_yield_2040_base']*100:.2f}% of value a year.</div>
<h2>Rules to confirm</h2>
<ul>
<li>Federal basic exclusion 2026 <span class="stat">$15,000,000</span> (published); gift exclusion <span class="stat">$19,000</span> (published). Form 706 due 9 months after death ({link('irs_filing','IRS')}).</li>
<li>Inherited basis generally the value at death ({link('irs_p551','Pub 551')}).</li>
<li>Prop 19 parent-child: move in within 1 year; claim within 3 years (BOE). Cap wording conflicts (F03).</li>
<li>California estate or inheritance tax: none confirmed from primary source yet (F05).</li>
<li>Capital gains: 0% bracket to <span class="stat">$49,450</span> single; NIIT 3.8% above <span class="stat">$200,000</span> single (IRS).</li>
</ul>
<h2>Open items</h2>
<ul><li>Composite tax rate (F01); insurance (F06); owner inputs unverified (F02); crash-regime proxy (F07).</li></ul>
<h2>Questions for counsel</h2>
<ul><li>Trust type and the trustee's powers over sale or occupancy.</li><li>Whether the heir may occupy the house under the trust terms.</li></ul>
</div>"""
    return page("briefing.html", "Attorney and CPA briefing", body,
                lead="One-page print sheet. Use the browser's print function.", one_page=True)


def p_method():
    a = MODEL["assumptions"]
    rows = [
        ["Composite property tax rate", f"{a['composite_tax_rate']*100:.2f}%", "Assumption (F01); no external source"],
        ["Gross rent yield", f"{a['rent_gross_yield']*100:.2f}%", "Assumption; no external source"],
        ["Vacancy and management", f"{a['rent_vacancy_mgmt']*100:.0f}%", "Assumption; no external source"],
        ["Maintenance", f"{a['maintenance_rate']*100:.1f}% of value a year", "Assumption (F12); no external source"],
        ["Sale cost", f"{a['sale_cost']*100:.0f}%", "Assumption; no external source"],
        ["Capital gains tax rate used on sale", f"{a['gain_tax_rate']*100:.1f}% (15% federal + 3.8% NIIT + 9.3% CA)", "Federal parts verified (IRS links); CA 9.3% not confirmed (F10); no external source for CA rate"],
        ["Base inflation", f"{a['infl_base']*100:.0f}%", "Fed 2% goal (base; see Fed link on Facts page); other regimes assumed; no external source for the other regimes"],
        ["Base stock return", f"{a['equity_base']*100:.0f}%", "Assumption; no external source"],
        ["T-bill park rate", f"{a['park_rate']*100:.2f}% (3-month Treasury, Nov 13, 2026)", link("treasury", "Treasury")],
        ["Water (per month, base)", money(a["water_month"]), "Owner range, rounded (F06); no external source"],
        ["Solar credit (per month, base)", money(a["solar_credit_month"]), "Owner range $10–$20, rounded; assumption (F06); no external source"],
    ]
    body = f"""
<h2>Method</h2>
<p>Monthly simulation from transfer to 2076, all results converted to 2026 dollars. Live-in and rent options count the property's value, rent and costs. Phased options park cash in T-bills, then buy stocks over 12 months. Mixed options switch at a set date. A Prop 19 cap is applied to live-in only (and to the mixed live option).</p>
<h2>Inputs</h2>
{table(["Input", "Value", "Status"], rows)}
<h2>Grid</h2>
<p>The full 120-cell grid (3 transfer years × 5 regimes × 8 option variants) is in <code>data/model.json</code>. The model script is <code>_src/model.py</code>.</p>
<h2>Limits</h2>
<ul>
<li>Not a forecast. Single deterministic path per regime.</li>
<li>Avoided-rent credit assumes the heir would otherwise pay rent of the same value.</li>
<li>No state income tax, no heir's own tax, no trust-level tax, no gift strategy.</li>
</ul>
"""
    return page("methodology.html", "Methodology and model inputs", body,
                lead="How the scenario results are built, and every input's status.")


def p_flagged():
    flags = [
        ("F01", "Composite property tax rate for Property A is not confirmed. The county Tax Rate Book sets the 1% levy plus bond debt; the rate for the specific tax-rate area has to come from the owner's bill. Model uses 1.20% as an assumption.", ["sc_rate_book"]),
        ("F02", "Owner-supplied values (market value, assessed value, property tax, rent, utilities) have no official confirmation yet. They are model inputs only.", []),
        ("F03", "Prop 19 cap wording conflict. BOE Prop 19 page: \"current taxable value plus <span class=\"stat\">$1,000,000</span>\". BOE LTA 2025/009: \"factored base year value plus <span class=\"stat\">$1,044,586</span>\". Both are computed; the model uses the LTA form.", ["boe_prop19", "boe_lta"]),
        ("F04", "Prop 19 repeal status for the 2026 ballot is not confirmed. The failed-to-qualify list read so far has no Prop 19 entry; the certified list has not been read line by line.", ["sos_failed", "sos_certified"]),
        ("F05", "California estate or inheritance tax: the FTB newsroom contains no estate-tax item; a primary statute check is still open.", ["ftb_news"]),
        ("F06", "Insurance, water and electricity: no CDI or provider primary source confirmed. Secondary average premiums conflict and are not published.", ["cdi"]),
        ("F07", "Black-swan model: the 1929 housing path is a 2008 proxy; phased-entry results in crash regimes depend on crash timing and exceed the base sell-at-once result; under review. Not for use as a forecast.", ["fed_1929", "fed_2007"]),
        ("F08", "Repository history: earlier commits and archived desks contain unrounded figures and identifiers (ZIP codes, city and neighbourhood names, owner property text). Flagged, not rewritten. The model data file (data/model.json) holds owner input values and is excluded from the published site.", []),
        ("F09", "Property A 2026 assessed value owner-supplied; must be confirmed with the assessor record. Not published as verified.", ["sc_annual"]),
        ("F10", "The CA capital gains rate (9.3%) used in the model is not confirmed from a primary source.", []),
        ("F11", "CA small-estate probate threshold (<span class='stat'>$208,850</span>) is in the model's constants from a secondary source; the Judicial Council form was not opened. Not used on any page.", []),
        ("F13", "Privacy-scan false positive: scripts/privacy_scan.py reads the integer 202611 in the official Treasury daily par-yield URL (its month parameter) as unrounded data. The exact URL is kept so the citation can be checked. Same pattern and handling as the cbd/ desk. For the scanner owner to review.", ["treasury"]),
        ("F12", "Model assumptions (equity return, rent yield, maintenance, housing growth by regime) are not sourced. Labelled assumptions.", []),
    ]
    rows = []
    for code, text, keys in flags:
        src = " ".join(link(k) for k in keys) if keys else '<span class="muted">No external source (see note)</span>'
        rows.append([f'<a id="{code}"></a><b>{code}</b>', text, src])
    body = table(["Flag", "Issue", "Source for review"], rows) + """
<p class="muted">Flagged items do not block publication. They are listed so the owner, attorney or CPA can check them.</p>"""
    return page("flagged.html", "Flagged for Review", body,
                lead="Open items, irregularities and unverified values. Each row links to the source to check.")


PAGES = {
    "index.html": p_index, "what-changes.html": p_what, "facts.html": p_facts,
    "property.html": p_property, "scenarios.html": p_scen, "black-swans.html": p_black,
    "projections.html": p_proj, "costs.html": p_costs, "process.html": p_process,
    "glossary.html": p_gloss, "questions.html": p_questions, "suggestions.html": p_suggest,
    "briefing.html": p_brief, "methodology.html": p_method, "flagged.html": p_flagged,
}


def main():
    for name, fn in PAGES.items():
        (DESK / name).write_text(fn())
    print(f"wrote {len(PAGES)} pages to {DESK}")


if __name__ == "__main__":
    main()
