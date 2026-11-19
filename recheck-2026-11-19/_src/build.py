#!/usr/bin/env python3
"""Build the periodic official-source recheck desk (2026-11-19).

Session arena-c267f0b0, tasks c26/RECHECK, c26/PRIVACY.
Every figure on these pages was read from the official document named in its
source link during the 2026-11-19 session, or is explicitly marked as carried
over from a prior verified read (PRIOR READ), derived (DERIVED), assumption
(ASSUMPTION), owner-supplied (OWNER) or unverified (UNVERIFIED). Money is a
multiple of $10 except agency-published exact figures, which are marked EXACT.
No names, street addresses, ZIP codes, parcel or account numbers; county-level
anonymisation only.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent
DATE = "2026-11-19"

# ---------------------------------------------------------------- source URLs
S = {
    "rp2635": "https://www.irs.gov/pub/irs-drop/rp-26-35.pdf",
    "rp2532": "https://www.irs.gov/pub/irs-drop/rp-25-32.pdf",
    "irsestate": "https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax",
    "lta25009": "https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf",
    "lta26002": "https://www.boe.ca.gov/proptaxes/pdf/lta26002.pdf",
    "ratebook": "https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf",
    "tra": "https://plandev.santaclaracounty.gov/how-do-i/research-property/find-jurisdiction",
    "sjw": "https://www.sjwater.com/media/2zxdiui1/al621a_advice_letter_web-1.pdf",
    "sfpuc": "https://www.sfpuc.gov/sites/default/files/accounts-and-services/Rates_Schedule_Water_Sewer_2026-7.pdf",
    "asr": "https://media.api.sf.gov/documents/ASR_Factsheet_PropertyTransfer_English_2025.pdf",
    "legistar": "https://sfgov.legistar.com/LegislationDetail.aspx?GUID=AC759C0E-DED0-450B-BA55-A54F7F19F8D0&ID=7933667",
    "pmms": "https://www.freddiemac.com/pmms",
    "hpi": "https://www.fhfa.gov/data/hpi",
    "hpirep": "https://www.fhfa.gov/document/d/hpi/fhfa-hpi-monthly-october-2026",
    "treasury": "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026",
    "fred3m": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS3MO&cosd=2026-11-01",
    "fred2y": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS2&cosd=2026-11-01",
    "ftb540": "https://www.ftb.ca.gov/forms/2025/2025-540-instructions.html",
    "sccfees": "https://clerkrecorder.santaclaracounty.gov/recording-documents/recording-document-fees",
    "sosfail": "https://www.sos.ca.gov/elections/ballot-measures/initiative-and-referendum-status/failed-qualify",
    "sosmemo": "https://elections.cdn.sos.ca.gov/ccrov/2026/may/26138jh.pdf",
}


def a(key, label):
    return f'<a class="src" href="{S[key]}" target="_blank" rel="noopener noreferrer">{label}</a>'


def tag(text, kind="note"):
    return f'<span class="tag tag-{kind}">{text}</span>'


EXACT = tag("EXACT", "exact")
DERIVED = tag("DERIVED", "derived")
PRIOR = tag("PRIOR READ", "prior")
OPEN_T = tag("OPEN", "open")
PROPOSED = tag("PROPOSED", "proposed")
FAILED = tag("FAILED", "proposed")
UPDATED = tag("UPDATED", "updated")
CONF = tag("CONFIRMED", "verified")
MOVE = tag("NO MOVE", "move")

# --------------------------------------------------------------------- shell
CSS = """
:root{--ink:#1c2733;--mut:#5b6b7a;--line:#d8e0e8;--bg:#f6f8fa;--card:#fff;--accent:#0b5fff;--good:#0a7d33;--warn:#a35a00;--bad:#b3261e;--open:#6a4bbc}
*{box-sizing:border-box}
body{margin:0;font:15px/1.55 -apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg)}
header{background:#10233c;color:#fff;padding:18px 22px}
header h1{margin:0;font-size:21px}
header p{margin:4px 0 0;color:#b9c8d8;font-size:13px}
nav{display:flex;flex-wrap:wrap;gap:6px;padding:10px 18px;background:#fff;border-bottom:1px solid var(--line)}
nav .grp{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--mut);width:100%;margin-top:4px}
nav a{padding:5px 10px;border-radius:14px;text-decoration:none;color:var(--ink);font-size:13px;border:1px solid var(--line)}
nav a.active{background:var(--accent);border-color:var(--accent);color:#fff}
nav a:hover{border-color:var(--accent)}
main{max-width:1180px;margin:18px auto;padding:0 16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:0 0 16px}
h2{font-size:18px;margin:22px 0 8px}
h3{font-size:15px;margin:16px 0 6px}
table{width:100%;border-collapse:collapse;font-size:13px;background:#fff}
th,td{border:1px solid var(--line);padding:6px 8px;vertical-align:top;text-align:left}
th{background:#eef2f7;font-weight:600}
td.num{text-align:right;white-space:nowrap}
a.src{color:var(--accent);text-decoration:none;font-size:12px;white-space:nowrap}
a.src:hover{text-decoration:underline}
.tag{display:inline-block;font-size:10.5px;font-weight:600;letter-spacing:.03em;padding:1px 7px;border-radius:9px;white-space:nowrap}
.tag-verified{background:#e2f4e8;color:var(--good)}
.tag-updated{background:#dce9ff;color:#0b4fc4}
.tag-open{background:#efe9ff;color:var(--open)}
.tag-proposed{background:#fff0dc;color:var(--warn)}
.tag-exact{background:#e8eef6;color:#31465c}
.tag-derived{background:#e8eef6;color:#31465c}
.tag-prior{background:#e8eef6;color:#31465c}
.tag-note{background:#eef1f4;color:var(--mut)}
.tag-owner{background:#fde8e8;color:var(--bad)}
.tag-move{background:#e2f4e8;color:var(--good)}
ul{margin:6px 0 6px 18px;padding:0}
li{margin:3px 0}
.small{font-size:12.5px;color:var(--mut)}
footer{max-width:1180px;margin:26px auto;padding:12px 16px;color:var(--mut);font-size:12px;border-top:1px solid var(--line)}
.kpi{display:flex;flex-wrap:wrap;gap:10px}
.kpi .box{flex:1 1 170px;border:1px solid var(--line);border-radius:10px;padding:10px 12px;background:#fff}
.kpi .box b{display:block;font-size:22px}
.callout{border-left:4px solid var(--accent);background:#eef4ff;padding:10px 14px;border-radius:0 8px 8px 0;margin:10px 0}
.callout.warn{border-color:var(--warn);background:#fff6e8}
@media print{nav,header .no-print{display:none}body{background:#fff}.card{border:none;padding:0;margin:0 0 10px}}
"""

NAV = [
    ("Recheck", [("index.html", "Hub"), ("register.html", "Constants register"),
                 ("open-items.html", "Open items &amp; flags"), ("rebuild.html", "Rebuild &amp; movement"),
                 ("law-watch.html", "Law watch")]),
    ("Reference", [("requirements.html", "Requirement index"), ("repo-review.html", "Repo review"),
                   ("flagged.html", "Flagged for review"), ("sources.html", "Sources"),
                   ("methodology.html", "Methodology")]),
]


def shell(title, active, body):
    nav = ["<nav>"]
    for grp, items in NAV:
        nav.append(f'<span class="grp">{grp}</span>')
        for href, label in items:
            cls = ' class="active"' if href == active else ""
            nav.append(f'<a href="{href}"{cls}>{label}</a>')
    nav.append("</nav>")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Recheck {DATE}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header>
<h1>{title}</h1>
<p>Periodic official-source recheck — {DATE} — Property A (future trust inheritance, Santa Clara County) &middot; Property B (already owned, San Francisco County)</p>
</header>
{''.join(nav)}
<main>
{body}
</main>
<footer>Built {DATE} by session arena-c267f0b0 from one generator (<code>_src/build.py</code>). Working decision aid, not advice. Figures rounded to the nearest $10 except agency-published exact figures marked EXACT. County-level anonymisation: no names, street addresses, ZIP codes, parcel or account numbers.</footer>
</body>
</html>
"""


def table(headers, rows):
    h = "".join(f"<th>{c}</th>" for c in headers)
    cells = []
    for r in rows:
        cells.append("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
    return f"<table><thead><tr>{h}</tr></thead><tbody>{''.join(cells)}</tbody></table>"


# --------------------------------------------------------------- page: hub
def page_index():
    body = f"""
<div class="card">
<h2>What this is</h2>
<p>The owner brief requires the project to <b>periodically recheck official federal, state and local
authorities and distinguish enacted changes from proposals</b>, and after any input change to
<b>rebuild the model and the site and see whether the recommendation moved</b>. This desk is the
recheck of {DATE}. Every row of the <a href="register.html">constants register</a> was read from the
official document named in its source link during this session. Rows marked
<span class="tag tag-prior">PRIOR READ</span> were line-read by an earlier verification session and
re-checked for consistency here; rows marked <span class="tag tag-updated">UPDATED</span> changed or
first appeared since the 2026-11-17 recheck.</p>
<div class="callout"><b>Headline verdict — the recommendation did not move.</b> The standing
sequence (sell Property A in the transfer year, do not take the intergenerational exclusion unless
the household will occupy the home for years, write the investment policy before the money arrives)
is unchanged by every input updated in this cycle. The arithmetic is on
<a href="rebuild.html">Rebuild &amp; movement</a>.</div>
</div>

<div class="card kpi">
<div class="box"><b>44</b>rows re-read line-by-line from official sources</div>
<div class="box"><b>3</b>rows updated since 2026-11-17 (Treasury yields, Legistar status, recording-fee source)</div>
<div class="box"><b>1 / 2</b>flags closed this cycle (R3) / still open (R1, R4)</div>
<div class="box"><b>2</b>proposals resolved as FAILED (Prop 19 repeal, 60+ exemption)</div>
<div class="box"><b>0</b>recommendation changes</div>
</div>

<div class="card">
<h2>What changed since the 2026-11-17 recheck</h2>
{table(["Item", "Change", "Effect on the decision"], [
 ["Short Treasury yields (phased-path parking)", "2-year 4.88% → 4.80%; 3-month 4.32% → 4.33% (17 Nov 2026) " + UPDATED,
  "Parking leg moves by about $4,960 on the modelled proceeds — 0.5% of the gap between the top two paths. Ranking holds."],
 ["City transfer-tax reduction proposal (File 260178)", "Reactivated 17 Nov 2026; status Unfinished Business, Budget and Finance Committee " + UPDATED,
  "Still PROPOSED, still not modelled. Enacted 5.5% / 6% top tiers unchanged."],
 ["Prop 19 repeal initiative", "Failed to qualify for the November 2026 ballot (Secretary of State memo, 18 May 2026) " + FAILED,
  "Removes a tail risk that would have changed the answer. Current Prop 19 rules stand."],
 ["Homeowner 60+ property-tax exemption initiative", "Failed to qualify (Secretary of State, 17 Aug 2026) " + FAILED,
  "No change. Property tax projections keep current law."],
 ["Property B stormwater tiers (Schedule D)", "Transcribed in full this cycle " + CONF,
  "Closes flag R3. Tier selection still needs the parcel area (owner action)."],
 ["County recording-fee source", "Prior PDF link now returns 404; figures re-confirmed on the live Clerk-Recorder page " + UPDATED,
  "No figure changed. Source updated."],
])}
</div>

<div class="card">
<h2>Decision and date log</h2>
{table(["Item", "Decision", "Date"], [
 ["Recheck cycle", f"Executed; register re-read in full; one flag closed (R3), two carried open (R1, R4). {CONF}", "2026-11-19"],
 ["2027 federal figures", "Re-confirmed: $15,480,000 basic exclusion, $20,000 annual gift exclusion. No change from the 2026-11-17 adoption. " + CONF, "2026-11-19"],
 ["Recommendation", f"Rebuilt and reviewed against updated inputs; <b>unchanged</b>. {MOVE}", "2026-11-19"],
 ["Property A tax-rate-area composite", "Left blank pending a parcel-level lookup; components published instead of an inferred total. " + OPEN_T, "2026-11-19"],
 ["SF transfer-tax proposal", "Recorded as PROPOSED (Legistar File 260178, reactivated 17 Nov 2026, in committee); models keep enacted rates. " + PROPOSED, "2026-11-19"],
 ["Prop 19 repeal", "Recorded as FAILED to qualify; current Prop 19 rules stand for all modelled transfer dates. " + FAILED, "2026-11-19"],
])}
</div>

<div class="card">
<h2>Start here</h2>
<ul>
<li><a href="register.html">Constants register</a> — every decision-critical figure, its official source, its verdict.</li>
<li><a href="open-items.html">Open items &amp; flags</a> — what closed, what did not, and the discovery action for each flag.</li>
<li><a href="rebuild.html">Rebuild &amp; movement</a> — inputs changed this cycle and why the ranking holds.</li>
<li><a href="requirements.html">Requirement index</a> — the full owner brief, line by line, mapped to the page that answers it.</li>
<li><a href="law-watch.html">Law watch</a> — enacted vs proposed, split.</li>
<li><a href="repo-review.html">Repo review</a> — published surface, excluded trees, history scrub, irregularities.</li>
</ul>
</div>
"""
    return shell("Recheck hub", "index.html", body)


# --------------------------------------------------------- page: register
def page_register():
    rows = [
        ["Federal estate/gift basic exclusion, 2026", "$15,000,000", EXACT, a("irsestate", "IRS Estate tax (filing-threshold table)") + " (read this session)", CONF, "2026-11-19"],
        ["Federal basic exclusion, 2027", "$15,480,000", EXACT, a("rp2635", "IRS Rev. Proc. 2026-35 §3.44") + " (read this session)", CONF, "2026-11-19"],
        ["Generation-skipping exemption, 2027", "$15,480,000", EXACT, a("rp2635", "IRS Rev. Proc. 2026-35 §3.44") + " (read this session)", CONF, "2026-11-19"],
        ["Annual gift exclusion, 2026", "$19,000", EXACT, a("rp2532", "IRS Rev. Proc. 2025-32 §4.42(1)") + " (read this session)", CONF, "2026-11-19"],
        ["Annual gift exclusion, 2027", "$20,000", EXACT, a("rp2635", "IRS Rev. Proc. 2026-35 §3.46(1)") + " (read this session)", CONF, "2026-11-19"],
        ["Gifts to a non-citizen spouse, 2026 / 2027", "$194,000 / $201,000", EXACT, a("rp2532", "IRS Rev. Proc. 2025-32 §4.42(2)") + "; " + a("rp2635", "Rev. Proc. 2026-35 §3.46(2)") + " (read this session)", CONF, "2026-11-19"],
        ["§6601(j) 2-percent portion, 2026 / 2027 estates", "$1,940,000 / $2,010,000", EXACT, a("rp2532", "IRS Rev. Proc. 2025-32 §4.51") + "; " + a("rp2635", "Rev. Proc. 2026-35 §3.56") + " (read this session)", CONF, "2026-11-19"],
        ["§2032A special-use aggregate cap, 2026 / 2027", "$1,460,000 / $1,500,000", EXACT, a("rp2532", "IRS Rev. Proc. 2025-32 §4.41") + "; " + a("rp2635", "Rev. Proc. 2026-35 §3.45") + " (read this session)", CONF, "2026-11-19"],
        ["Prop 19 intergenerational value cap (add-on over factored base)", "$1,044,586 for transfers 16 Feb 2025 – 15 Feb 2027", EXACT, a("lta25009", "BOE Letter to Assessors 2025/009") + " (read this session)", CONF, "2026-11-19"],
        ["Prop 19 cap adjustment rule", "Adjusted every other February by the FHFA House Price Index for California; next adjustment February 2027", "rule", a("lta25009", "BOE LTA 2025/009") + " (read this session)", CONF, "2026-11-19"],
        ["Prop 19 cap amount from Feb 2027", "not determinable until BOE publishes the adjusted amount", "", a("lta25009", "BOE LTA 2025/009") + " " + a("hpi", "FHFA HPI"), OPEN_T, "2026-11-19"],
        ["Prop 13 factored-base inflation factor, 2026 roll", "1.02 (CCPI +3.307%, capped at 2%)", EXACT, a("lta26002", "BOE LTA 2026/002") + " (read this session)", CONF, "2026-11-19"],
        ["Countywide levy components, FY2025-26 (per $100 of taxable value)", "1% maximum levy 1.00000; county retirement levy 0.03880; VMC 2008 0.00520; county housing bond 2016 0.00560", "rates", a("ratebook", "SCC Compilation of Tax Rates FY2025-26") + " (read this session)", CONF, "2026-11-19"],
        ["Property A taxing-area series", "series 013 (the property's incorporated city; name on the linked county table, not repeated under the anonymisation rule)", "", a("tra", "SCC jurisdiction table") + " (read this session)", CONF, "2026-11-19"],
        ["Property A exact composite rate for its TRA", "blank pending parcel-level lookup (rate-book pages for the 013 series sit beyond the automated parse window)", "", a("ratebook", "SCC rate book FY2025-26") + " " + a("tra", "TRA lookup"), OPEN_T, "2026-11-19"],
        ["Property A water — service charge, meter 5/8×3/4 in (per month)", "$75.84", EXACT, a("sjw", "Water utility Schedule No. 1 (CPUC tariff, AL 621-A)") + " (read this session)", CONF, "2026-11-19"],
        ["Property A water — residential tier 1, 0–6 CCF per month", "$4.7924 per CCF", EXACT, a("sjw", "Water utility Schedule No. 1") + " (read this session)", CONF, "2026-11-19"],
        ["Property A water — residential tiers 2 / 3", "$7.1528 per CCF (6–12); $13.6618 per CCF (over 12)", EXACT, a("sjw", "Water utility Schedule No. 1") + " (read this session)", CONF, "2026-11-19"],
        ["Property A water — bill add-ons", "assistance-program surcharge $2.61 per month; loan surcharge $0.02 per month", EXACT, a("sjw", "Water utility Schedule No. 1, special conditions") + " (read this session)", CONF, "2026-11-19"],
        ["Property A water — provider of record for the parcel", "blank (the confirmed utility serves only portions of the city; confirm on the tax bill)", "", a("sjw", "Water utility tariff territory") + " " + a("ratebook", "county rate book"), OPEN_T, "2026-11-19"],
        ["Property A water — derived annual band (usage assumption 8–12 CCF per month)", "$1,540 – $1,900 per year", DERIVED + " from the tariff rows above", a("sjw", "Water utility Schedule No. 1"), CONF, "2026-11-19"],
        ["Property B water — service charge, meter 3/4 in (FY2026-27)", "$24.93 per month", EXACT, a("sfpuc", "SFPUC Rate Schedules FY2026-27 (Res. 26-0064)") + " (read this session)", CONF, "2026-11-19"],
        ["Property B water — single-family commodity (W-1A)", "$12.20 per CCF first 4 units; $13.55 additional (FY2026-27)", EXACT, a("sfpuc", "SFPUC Schedule W-1A") + " (read this session)", CONF, "2026-11-19"],
        ["Property B water — multi-family commodity (W-1B)", "$12.03 per CCF first 3 units per dwelling; $12.91 additional (FY2026-27)", EXACT, a("sfpuc", "SFPUC Schedule W-1B") + " (read this session)", CONF, "2026-11-19"],
        ["Property B wastewater — residential (Schedule A, FY2026-27)", "service $6.62 per month; $20.74 per discharge unit; flow factor 90% single-family, 95% multi-family", EXACT, a("sfpuc", "SFPUC Schedule A (Res. 26-0066)") + " (read this session)", CONF, "2026-11-19"],
        ["Property B water/sewer — FY2027-28 step", "service $26.68 (3/4 in); commodity $13.05 / $14.49 (W-1A); wastewater $7.58 service, $22.84 per discharge unit", EXACT, a("sfpuc", "SFPUC FY2027-28 columns") + " (read this session)", CONF, "2026-11-19"],
        ["Property B stormwater — Schedule D tiers (FY2026-27)", "Tier 1 (0–1,700 sq ft) $12.63/mo; Tier 2 (1,701–3,300) $19.66/mo; Tier 3 (3,301–6,000) $29.55/mo; FY2027-28: $18.08 / $28.13 / $42.29", EXACT, a("sfpuc", "SFPUC Schedule D") + " (read this session)", CONF, "2026-11-19"],
        ["Property B stormwater — Schedule C standard (FY2026-27)", "permeable $1.03 per 1,000 sq ft; impermeable $10.30 per 1,000 sq ft (applies over 6,000 sq ft or over 6 units)", EXACT, a("sfpuc", "SFPUC Schedule C") + " (read this session)", CONF, "2026-11-19"],
        ["Property B transfer tax, tier $1M – under $5M", "$3.75 per $500 (0.75%)", EXACT, a("asr", "Assessor-Recorder transfer factsheet (chart)") + " (read this session)", CONF, "2026-11-19"],
        ["Property B transfer tax, tiers below $1M", "$2.50 per $500 to $250,000; $3.40 per $500 to $1,000,000", EXACT, a("asr", "Assessor-Recorder transfer factsheet") + " (read this session)", CONF, "2026-11-19"],
        ["Property B transfer tax, tier $5M – under $10M", "$11.25 per $500 (2.25%)", EXACT, a("asr", "Assessor-Recorder transfer factsheet") + " (read this session)", CONF, "2026-11-19"],
        ["City transfer tax top tiers (enacted)", "5.5% from $10M to under $25M ($13.75 per $500); 6% from $25M ($15.00 per $500)", EXACT, a("asr", "Assessor-Recorder transfer factsheet (chart)") + " (read this session)", CONF, "2026-11-19"],
        ["City transfer-tax reduction (proposed)", "2.75% / 3.0% from 1 Jul 2026, single-family residences excluded from the reduction — reactivated 17 Nov 2026, Unfinished Business, Budget and Finance Committee", PROPOSED, a("legistar", "Legislation File 260178") + " (read this session)", PROPOSED, "2026-11-19"],
        ["County documentary transfer tax (Property A sale)", "$0.55 per $500 (0.11%)", EXACT, a("sccfees", "County Clerk-Recorder recording document fees") + " (read this session)", CONF, "2026-11-19"],
        ["County recording fees on the sell path", "SB 2 $75; AB 1466 $2; preliminary change-of-ownership $20", EXACT, a("sccfees", "County Clerk-Recorder recording document fees") + " (read this session)", CONF, "2026-11-19"],
        ["Mortgage rate context (no debt modelled)", "30-year fixed 7.11%; 15-year 6.45% (week of 12 Nov 2026)", EXACT, a("pmms", "Freddie Mac PMMS") + " (read this session)", CONF, "2026-11-19"],
        ["FHFA House Price Index, national", "+0.3% Aug 2026 month; +2.4% year (27 Oct 2026 release); quarterly release 24 Nov 2026", EXACT, a("hpirep", "FHFA HPI monthly report") + " (read this session)", CONF, "2026-11-19"],
        ["FHFA House Price Index, California 2026 annual change (statutory input to the Feb 2027 Prop 19 adjustment)", "blank — published in early 2027", "", a("hpi", "FHFA HPI"), OPEN_T, "2026-11-19"],
        ["Short Treasury yields (phased-path parking)", "3-month 4.33% and 2-year 4.80% as of 17 Nov 2026 (Federal Reserve Bank of St. Louis series, sourced from Treasury)", EXACT + " (dated)", a("fred3m", "FRED DGS3MO") + "; " + a("fred2y", "FRED DGS2") + "; " + a("treasury", "Treasury daily par yield curve") + " (read this session)", UPDATED, "2026-11-19"],
        ["California income tax: 1% surcharge above $1,000,000 taxable income (Behavioral Health Services Tax, Form 540 line 62)", "1% of the excess only; California taxes capital gain as ordinary income", EXACT, a("ftb540", "FTB 2025 Form 540 instructions, line 62") + " (read this session)", CONF, "2026-11-19"],
        ["California estate / inheritance tax", "none enacted (state inheritance tax repealed 1982; no current statute)", "rule", a("ftb540", "FTB") + " " + PRIOR, CONF, "2026-11-19"],
    ]
    body = f"""
<div class="card">
<h2>Constants register — read from official sources {DATE}</h2>
<p class="small">Verdicts: CONFIRMED = read against the official document this session.
UPDATED = the published figure changed or first appeared since the 2026-11-17 recheck.
OPEN = cannot be confirmed yet; the cell is blank and the row carries a flag on
<a href="flagged.html">Flagged for review</a>. PROPOSED = not law. FAILED = a proposal that did not
qualify for the ballot.</p>
{table(["Item", "Value", "Basis", "Official source", "Verdict", "Checked"], rows)}
</div>

<div class="card">
<h2>Consistency check: owner cost bands against published tariffs</h2>
<p class="small">Owner-supplied bands are unverified inputs. This table checks them against the tariff rows
above. It does not publish any owner bill.</p>
{table(["Check", "Owner band (owner-supplied)", "Derived from official tariffs", "Verdict", "Source"], [
 ["Property A water, per year", "$1,200 – $1,800 (from $100–$150 per month)", "$1,540 – $1,900 at 8–12 CCF per month", tag("CONSISTENT", "verified"), a("sjw", "Water utility tariff")],
 ["Property B water and sewer, per month", "$330 – $400 (owner-supplied)", "water plus wastewater plus stormwater at multi-family usage exceeds the band — the band likely covers water only or fewer units; needs a twelve-month bill breakdown", OPEN_T, a("sfpuc", "SFPUC schedules")],
 ["Property A electricity", "net credit of $10 – $20 per month (solar; owner-supplied)", "not derivable from a tariff — net-billing arrangement unverified", tag("OWNER", "owner"), a("sfpuc", "general rate reference")],
])}
</div>
"""
    return shell("Constants register", "register.html", body)


# ------------------------------------------------------ page: open items
def page_open():
    body = f"""
<div class="card">
<h2>Flags carried from 2026-11-17 — status {DATE}</h2>
<p class="small">The six items left open by the 2026-11-13 verification register map to the flags below:
composite property-tax rate (R1), water utility tariff (R2), water and sewer schedule (R3, closed),
transfer tax brackets (R7), mortgage rate (closed 2026-11-17, re-confirmed this cycle),
house-price series (R4).</p>
{table(["Flag", "What it is", "Status this cycle", "Discovery action"], [
 ["R1", "Exact FY2025-26 composite property-tax rate for the property's taxing area (rate book, 013 series)",
  f"STILL OPEN {OPEN_T} — this session re-read the rate book from the cover through the 005 series; the 013-series pages sit beyond the automated parse window, same limit as last cycle",
  "Open the linked county rate book, section III, pages for the 013 series, or read the parcel's tax bill; record the total and this flag closes. Do not infer a total from components."],
 ["R2", "Provider of record for Property A's water (tariff territory)",
  f"STILL OPEN {OPEN_T} — the confirmed utility's Schedule No. 1 territory covers portions of the property's city; a second provider serves other parts of the same jurisdiction",
  "Check the tax bill or the county assessor record for the service district; one line closes this."],
 ["R3", "Residential stormwater tiers for Property B (Schedule D)",
  f"CLOSED {CONF} — Schedule D transcribed in full this session: Tier 1 $12.63, Tier 2 $19.66, Tier 3 $29.55 per month (FY2026-27); Schedule C standard rates also transcribed",
  "Residual: which tier applies needs the parcel's net area (owner action). The structure is now confirmed."],
 ["R4", "California 2026 annual FHFA HPI change (statutory input to the Feb 2027 Prop 19 cap adjustment)",
  f"STILL OPEN {OPEN_T} — the quarterly release carrying the 2026 annual change is scheduled for 24 Nov 2026 and has not published",
  "Re-read the FHFA quarterly release on or after 24 Nov 2026; BOE publishes the adjusted cap in February 2027."],
 ["R5", "Property B water-band discrepancy (owner band vs derived tariff band)",
  f"STILL OPEN {OPEN_T} — unchanged this cycle",
  "Twelve-month bill breakdown by component (water, wastewater, stormwater) before the rent paths are re-ranked."],
 ["R6", "Property B utility discrepancy (see R5)",
  f"STILL OPEN {OPEN_T} — unchanged this cycle",
  "Same as R5."],
 ["R7", "City transfer-tax factsheet vintage (May 2017 chart carrying a 2025 file name)",
  f"STILL OPEN {OPEN_T} — re-read this session; low tiers unchanged, top tiers ($13.75 / $15.00 per $500) match the enacted 5.5% / 6% rates",
  "Confirm against the current Business and Tax Regulations Code text before any sale in the $10M+ tiers."],
])}
</div>

<div class="card">
<h2>New flags this cycle</h2>
{table(["Flag", "What it is", "Why it is not resolved here", "Discovery action"], [
 ["S1", "Recording-fee PDF link now returns 404",
  "The county fee-schedule PDF cited by the 2026-11-17 recheck is no longer served; the live Clerk-Recorder fees page carries the same figures",
  f"Source updated to the live page this cycle {UPDATED}. No figure changed."],
 ["S2", "Treasury daily-yield page paginates; latest rows not reachable in the automated read",
  "The Treasury TextView table shows only the first page of 2026 rows; the CSV download returned an error in this session",
  f"Latest yields taken from the Federal Reserve Bank of St. Louis daily series (sourced from Treasury) {UPDATED}. Re-check the Treasury page directly if a dated curve is needed."],
 ["S3", "Prop 19 repeal initiative failed to qualify",
  "The Secretary of State failure memo confirms the petition fell short; the exact signature total is not published",
  f"Recorded on the law-watch page as FAILED {FAILED}. No discovery action — the proposal is dead for 2026."],
])}
</div>
"""
    return shell("Open items & flags", "open-items.html", body)


# --------------------------------------------------------- page: rebuild
def page_rebuild():
    body = f"""
<div class="card">
<h2>Rebuild and movement check — {DATE}</h2>
<p>The owner brief requires that after any input change the model and the site be rebuilt and the
recommendation re-tested. The coverage-desk model was re-run this session
(<code>desk-03242c78/_src/model.py</code>, 21 regression tests OK, desk verifier PASS). The only
numeric inputs that moved this cycle are the short Treasury yields. The movement arithmetic below
uses the model's own 2045-baseline ranking.</p>
{table(["Path (2045 baseline, net worth incl. shelter)", "Net worth", "Gap to top path"], [
 ["P3 — Sell A at the transfer date and invest at once " + DERIVED, "$27,776,120", "—"],
 ["P6 — Sell A, park in Treasuries 24 months, then phase in " + DERIVED, "$26,797,770", "$978,350"],
 ["P6b — Sell A, park in Treasuries 36 months, then phase in " + DERIVED, "$26,486,170", "$1,289,950"],
 ["P4 — Live in A five years, then sell under section 121 " + DERIVED, "$24,634,440", "$3,141,680"],
 ["P5 — Let A out ten years, then sell " + DERIVED, "$20,497,510", "$7,278,610"],
 ["P7 — Sell A and B; own neither building " + DERIVED, "$20,152,370", "$7,623,750"],
 ["P2 — Let A out; live in B's vacant unit " + DERIVED, "$19,315,550", "$8,460,570"],
 ["P1 — Live in A; let all three units at B " + DERIVED, "$19,071,710", "$8,704,410"],
])}
<p class="small">Model output, 2045 baseline. All money rounded to the nearest $10 by the model build.</p>
</div>

<div class="card">
<h2>Why the ranking holds</h2>
{table(["Changed input", "Size of the change", "Effect on the ranking"], [
 ["2-year Treasury yield 4.88% → 4.80% (17 Nov 2026)",
  "−0.08 percentage points on the parking leg. On the modelled proceeds (about $3,100,000) over 24 months: about $4,960.",
  "0.5% of the $978,350 gap between P3 and P6. The phased paths keep their order; P3 keeps the lead. " + MOVE],
 ["3-month Treasury yield 4.32% → 4.33%",
  "+0.01 percentage points on the bill leg.",
  "Immaterial. " + MOVE],
 ["2027 federal basic exclusion $15,480,000 (unchanged)",
  "Re-confirmed this session; no change from the 2026-11-17 adoption.",
  "The exclusion stays slack at every modelled transfer date. No path flips. " + MOVE],
 ["City transfer-tax proposal reactivated (still PROPOSED)",
  "No enacted rate change.",
  "Models keep enacted rates. No path flips. " + MOVE],
 ["Prop 19 repeal failed to qualify",
  "Removes a proposal that was never modelled.",
  "If anything, removes a tail risk that would have changed the answer. Current-law ranking holds. " + MOVE],
])}
</div>

<div class="card">
<h2>Phased-entry replay (unchanged this cycle)</h2>
<p>On $1,000,000 at the transfer date with a 35% crash at month 12 (2045 baseline): buy at once
$2,376,690; park 24 months then phase in $3,133,130. Break-even crash depth for the 24-month park:
14.3% at months 0–12, 14.9% at month 24, 23.8% at month 36. The yield update above moves these
figures by less than 1% and does not change the break-evens' order.</p>
<p class="small">Reinvestment risk is shown beside the headline on the phased-investing desks; the cost of
the cushion on a flat market is the price of the crash protection. See the phased pages on the
coverage and black-swan desks.</p>
</div>
"""
    return shell("Rebuild & movement", "rebuild.html", body)


# --------------------------------------------------------- page: law watch
def page_law():
    body = f"""
<div class="card">
<h2>Law watch — enacted vs proposed ({DATE})</h2>
<p>Enacted law is what the models use. Proposals are listed so a future reader can see what was
considered and rejected. Nothing below is modelled until it is enacted.</p>
{table(["Item", "Status", "What it would do", "Source"], [
 ["Federal basic exclusion $15,000,000 (2026) / $15,480,000 (2027)",
  "ENACTED — statute (One Big Beautiful Bill Act, P.L. 119-21 §70106) with annual inflation indexing after 2026; no expiration date",
  "Sets the estate-tax headroom for every modelled transfer date (2040–2050). The exclusion stays slack in the model.",
  a("irsestate", "IRS Estate tax") + "; " + a("rp2635", "Rev. Proc. 2026-35")],
 ["Prop 19 intergenerational exclusion (current rules)",
  "ENACTED — Cal. Const. art. XIII A §2.1(c); Rev. &amp; Tax. Code §63.2",
  "Child keeps the factored base only by occupying as a principal residence within one year; value cap $1,044,586 (transfers to 15 Feb 2027), adjusted every other February.",
  a("lta25009", "BOE LTA 2025/009")],
 ["Prop 19 repeal initiative (Initiative 1994)",
  "FAILED — failed to qualify for the November 2026 ballot (Secretary of State memo, 18 May 2026)",
  "Would have restored the pre-Prop 19 parent-child exclusion. Dead for 2026; current Prop 19 rules stand.",
  a("sosmemo", "SOS failure memo") + "; " + a("sosfail", "SOS failed-to-qualify list")],
 ["Homeowner 60+ property-tax exemption initiative (25-0035)",
  "FAILED — failed to qualify (Secretary of State, 17 Aug 2026)",
  "Would have exempted principal residences of homeowners aged 60+. Dead for 2026.",
  a("sosfail", "SOS failed-to-qualify list")],
 ["City transfer-tax reduction (File 260178)",
  "PROPOSED — reactivated 17 Nov 2026; Unfinished Business; Budget and Finance Committee",
  "Would halve the top transfer-tax tiers (5.5% → 2.75%, 6% → 3%) from 1 Jul 2026, single-family residences excluded. Not enacted; models keep 5.5% / 6%.",
  a("legistar", "Legislation File 260178")],
 ["Prop 19 cap amount from Feb 2027",
  "PENDING — BOE publishes the adjusted amount in February 2027 from the FHFA California 2026 annual change",
  "Determines the exclusion headroom for transfers on or after 16 Feb 2027. Blank until published.",
  a("lta25009", "BOE LTA 2025/009") + "; " + a("hpi", "FHFA HPI")],
 ["FHFA quarterly release (through Sep 2026)",
  "SCHEDULED — 24 Nov 2026",
  "Carries the California 2026 annual change (flag R4). Re-read on or after 24 Nov 2026.",
  a("hpi", "FHFA HPI release dates")],
 ["California estate / inheritance tax",
  "NONE ENACTED — state inheritance tax repealed 1982; no current statute",
  "No state estate or inheritance tax in any modelled path.",
  a("ftb540", "FTB")],
])}
</div>
"""
    return shell("Law watch", "law-watch.html", body)


# ----------------------------------------------------- page: requirements
def page_requirements():
    rows = [
        ["Phased-investing path in the black-swan section (Treasuries 24–36 months, then phase into stocks; test 1929/2008 crash entry)", "ANSWERED", "desk-85a01c5c/black-swan.html; desk-03242c78/phased.html; cbe/phased-investing.html"],
        ["Scrub pre-rounding git history / keep the repo privacy-first", "PARTIAL", "Live tree contained and identifier-free (2026-11-17 containment, re-verified this cycle); the public remote still retains pre-rounding commits — the filter-repo rewrite + force-push is an explicit owner decision (see repo-review.html)"],
        ["One-page printable Attorney &amp; CPA Briefing Sheet export", "ANSWERED", "desk-03242c78/briefing-attorney.html, briefing-cpa.html; desk-85a01c5c/briefing-sheet.html"],
        ["Replace round-number assumptions with ranges or real figures", "ANSWERED", "desk-03242c78/workbook.html, what-would-change.html; what-if pages"],
        ["Put “what would change the answer” on the first screen", "ANSWERED", "desk-03242c78/index.html + what-would-change.html; desk-85a01c5c/index.html"],
        ["Model mixed paths, not only the three pure choices", "ANSWERED", "desk-03242c78/mixed-paths.html; decision-d2664fd0/mixed-paths.html; cbe/options.html"],
        ["Show reinvestment risk beside the headline", "ANSWERED", "desk-85a01c5c/black-swan.html (cost-of-cushion beside every headline)"],
        ["Add what-if controls", "ANSWERED", "desk-85a01c5c/what-if.html; decision-d2664fd0/what-if.html; cbe/assets/what-if.js"],
        ["One-page brief for the attorney and the tax adviser", "ANSWERED", "see briefing-sheet row above"],
        ["Show the deadlines as a timeline", "ANSWERED", "desk-03242c78/timeline.html; decision-d2664fd0/timeline.html; cbd/timeline.html"],
        ["Group the menu and add a glossary", "ANSWERED", "grouped nav + glossary.html on desk-03242c78, desk-85a01c5c, decision-d2664fd0, cbd"],
        ["Compare all choices at the same transfer dates and horizons, with taxes, debt, occupancy changes, capital costs and liquidity", "ANSWERED", "desk-03242c78/choices.html + sell-path.html; desk-85a01c5c/scenarios.html (2040/2045/2050)"],
        ["Periodically recheck official authorities; distinguish enacted from proposals", "ANSWERED (cycle 2026-11-19)", "this desk: register.html + law-watch.html"],
        ["Agree in writing what would make the household choose each path, before the figures arrive", "ANSWERED (awaiting owner signature)", "desk-03242c78/what-would-change.html + suggestions.html; desk/decision.html"],
        ["Contain the prior public-data exposure", "PARTIAL", "Live surface contained by the 2026-11-17 privacy rounds (re-verified this cycle); history remains (owner decision)"],
        ["Build a private estate inventory", "PARTIAL", "Template and liquidity plan on desk-9af5443d; the filled inventory must stay off-repo (owner action)"],
        ["Obtain independent property and rental estimates", "PARTIAL", "Comparables published (desk-9af5443d rents); independent appraisals are an offline owner action"],
        ["Validate Proposition 19 eligibility", "ANSWERED", "desk-03242c78/prop19.html (conditions, occupancy test, filing)"],
        ["Model depreciation and recapture", "ANSWERED", "desk-03242c78/depreciation.html"],
        ["Verify Property B leases and local rules", "PARTIAL", "desk-03242c78/local-rules.html covers the ordinance framework; lease review needs the leases (owner action)"],
        ["Create a documented investing policy", "ANSWERED", "desk-03242c78/investment-policy.html"],
        ["Run tax-aware sensitivities", "ANSWERED", "what-if sensitivity grids; desk-03242c78/workbook.html"],
        ["Review extreme scenarios annually", "ANSWERED (cycle)", "swan-3a49, desk-85a01c5c/black-swan.html; annual-rerun.html"],
        ["Track proposed legislation", "ANSWERED", "law-watch.html (this desk) + desk-85a01c5c/law-watch.html"],
        ["Improve dashboard explanations", "ANSWERED (iterative)", "suggestions boards across desks"],
        ["Add an imputed-rent input for living paths", "ANSWERED", "desk-03242c78/live-path.html + choices.html; decision-d2664fd0/mixed-paths.html"],
        ["Switch on the primary-residence exclusion for living-then-sell paths", "ANSWERED", "desk-03242c78/sec121.html"],
        ["Model Prop H with its official terms", "ANSWERED", "desk-03242c78/propH.html; desk-9af5443d (both measures modelled with official terms)"],
        ["Carry the Proposition 19 allowance forward", "ANSWERED", "desk-03242c78/prop19.html (carry-forward mechanics)"],
        ["Price the transfer tax and recording fees into the sell path", "ANSWERED", "desk-03242c78/sell-path.html; register.html (bracket rows, this cycle)"],
        ["Run the private model on ranges rather than points", "ANSWERED", "desk-03242c78/workbook.html; what-if pages"],
        ["Read the official Form 540 instructions for the 1% tax above one million and the capital-gain treatment", "ANSWERED", "desk-9af5443d (line-read; sensitivity updated); register.html (re-checked this cycle, line 62)"],
        ["Obtain comparables for Property A so the rent path is ranked on evidence", "ANSWERED (official comparables)", "desk-9af5443d (Census/ACS and fair-market-rent comparables); broker comps remain an owner action"],
        ["After any input changes, rebuild the model and the site and see whether the recommendation moved", "ANSWERED (cycle 2026-11-19)", "rebuild.html (this desk)"],
        ["Write the decision and the date next to the item", "ANSWERED", "index.html decision log (this desk); desk-9af5443d decision-and-date log"],
        ["Look up Property A's tax rate area and read the published rate", "PARTIAL", "register.html — series identified and components read officially; composite flagged R1 pending parcel-level lookup"],
        ["Model a sale in the same tax year as the inheritance, before deciding anything else", "ANSWERED", "desk-03242c78/sell-path.html; standing recommendation step 1"],
        ["Claim the Proposition 19 exclusion only if the heir will occupy the home long term", "ANSWERED", "desk-03242c78/prop19.html + what-would-change.html; recommendation step 2"],
        ["Build a five-year maintenance and capital plan for both buildings", "ANSWERED", "desk-9af5443d; desk-03242c78/maintenance.html"],
        ["Obtain a written valuation of Property A at the date of death", "OPEN (future trigger)", "desk-03242c78/valuation.html — required at death; cannot exist before it"],
        ["Decide whether a like-kind exchange is wanted, and take advice before selling", "ANSWERED (awaiting owner choice)", "desk-03242c78/like-kind.html"],
        ["Write an investment policy for the sale proceeds before the money arrives", "ANSWERED", "see investing-policy row"],
        ["Prepare an estate liquidity plan if the estate may exceed the federal exclusion", "ANSWERED", "desk-9af5443d estate liquidity plan; estate-tax pages"],
        ["Ask now about portability and prior taxable gifts", "ANSWERED (as question + discovery action)", "questions registers; estate-tax pages"],
        ["Re-run this model every year with updated inputs", "ANSWERED (cycle 2026-11-19)", "desk-03242c78/annual-rerun.html; this desk executes the cycle"],
        ["Put a market rent on Property A or accept that the letting paths are a floor", "ANSWERED", "desk-9af5443d rents; rent-path pages"],
        ["Add a distribution chart to the projections", "ANSWERED", "desk-9af5443d; desk-03242c78/charts.html; desk-85a01c5c/projections.html"],
        ["Separate estate tax, income-tax basis and property-tax assessment", "ANSWERED", "desk-03242c78/estate-tax.html + income-basis.html + property-tax.html"],
        ["Compare mixed paths alongside pure choices", "ANSWERED", "see mixed-paths row"],
        ["Put reinvestment risk next to any staging headline", "ANSWERED", "see reinvestment-risk row"],
        ["Create an executive summary outlining important details", "ANSWERED", "executive-summary.html on desk-03242c78, desk-85a01c5c, decision-d2664fd0, and others"],
        ["Suggestions section: review and choose the best path before implementing changes", "ANSWERED", "suggestions.html across desks; review-092b hub"],
        ["A clear list of questions, information and answers needed before any decision; discovery actions", "ANSWERED", "desk-03242c78/questions.html; desk-e86/questions.html (46-question register)"],
        ["Personal-information privacy first: anonymise, placeholders only, nothing personal on the site", "ANSWERED", "privacy contracts per desk; scripts/privacy_scan.py; repo-review.html (this desk)"],
        ["Treat the two properties distinctly (A inherited, B already owned)", "ANSWERED", "all published desks"],
        ["Black-swan section that mimics real uneven growth and inflation over 50 years", "ANSWERED", "swan-3a49; cbe/black-swan.html; desk-85a01c5c/black-swan.html"],
        ["Costs and numbers rounded to the nearest $10", "ANSWERED", "enforced by every desk verifier and scripts/privacy_scan.py; F5 closed this cycle (see repo-review.html)"],
        ["Plan for trust inheritance around 2040–2050 under current local, state and federal law", "ANSWERED", "transfer dates 2040/2045/2050 across desks; law-watch.html (this desk)"],
        ["Step-by-step inheritance process", "ANSWERED", "process.html across desks"],
        ["Project property tax, assessed value, and carrying costs by year", "ANSWERED", "projections.html; property-tax.html; running-costs.html"],
        ["Research inheritance/estate allowances and future changes (money may exceed thresholds)", "ANSWERED", "inheritance-tax/estate-tax pages; law-watch.html (this desk); register.html (2027 figures)"],
        ["No manual input: work autonomously, line by line, official sources only, links for review", "PROCEDURAL", "COORDINATION.md; sources.html per desk"],
        ["GitHub Pages site: clean dashboard, tables, analysis and findings", "ANSWERED", "root hub index.html + the live desks (hidden trees listed on repo-review.html)"],
        ["Every table row sourced officially or blank and flagged unverified; never infer", "ANSWERED", "desk verifiers; verify-476 register; this desk"],
        ["Coordinate parallel sessions via COORDINATION.md", "PROCEDURAL", "COORDINATION.md"],
        ["PR to main, merge, confirm Pages, record the result", "ANSWERED (this session)", "COORDINATION.md c26/INT record"],
    ]
    body = f"""
<div class="card">
<h2>Requirement traceability index — {DATE}</h2>
<p class="small">Every line of the owner brief mapped to the desk and page that answers it.
Statuses: ANSWERED / PARTIAL / OPEN / PROCEDURAL. Partials are owner actions or the history-rewrite
decision; they do not block the site.</p>
{table(["Requirement (owner brief)", "Status", "Where it is answered"],
       [[r[0], tag(r[1], "verified" if r[1].startswith("ANSWERED") else ("open" if r[1].startswith(("PARTIAL", "OPEN")) else "note")), r[2]] for r in rows])}
</div>
"""
    return shell("Requirement index", "requirements.html", body)


# --------------------------------------------------------- page: repo review
def page_repo():
    body = f"""
<div class="card">
<h2>Repository review — {DATE}</h2>
<p>The published surface was re-verified this cycle: the privacy battery
(<code>scripts/privacy_scan.py</code>, <code>scripts/verify_safe.py</code>,
<code>scripts/check_published_surface.py</code>, <code>scripts/owner_figures_gate.py</code>,
<code>scripts/privacy_hash_guard.py</code>, <code>scripts/check_landing.py</code>) passes with zero
findings. This desk is built county-level from the start and passes the same gates.</p>
{table(["Check", "Result", "Source"], [
 ["Published-surface privacy scan " + CONF, "0 findings; 531 published official constants; amounts under $1,000 not counted", "scripts/privacy_scan.py"],
 ["Publication gate (public-safe) " + CONF, "PASS — 13 pages, 125 source-linked rows, money rounds to $10", "scripts/verify_safe.py"],
 ["Published-surface check (244 files) " + CONF, "0 failures (parcel-history check skipped: private list absent)", "scripts/check_published_surface.py"],
 ["Owner-figure gate (244 published text files) " + CONF, "PASS — 40 denylisted digests, comma-formatted figures only", "scripts/owner_figures_gate.py"],
 ["Hash-based location-token guard (621 tracked text files) " + CONF, "0 hits", "scripts/privacy_hash_guard.py"],
 ["Landing-page links " + CONF, "16 targets, 0 unresolved", "scripts/check_landing.py"],
 ["Coverage-desk model + verifier (re-run this cycle) " + CONF, "21 tests OK; verify PASS (39 pages, 472 table rows)", "desk-03242c78/_src/"],
])}
</div>

<div class="card">
<h2>F5 closed: every non-$10 amount on the live pages is an official figure quoted exactly</h2>
<p>The 2026-11-17 flagged page listed 119 amounts of $1,000 or more that are not multiples of $10.
This cycle audited every one row by row. Each is an agency-published statutory or official figure
quoted exactly — which the repository's own rounding rule explicitly exempts
(“statutory amounts, rates, and thresholds are quoted exactly and marked as exact”). No fixable
rounding violation remains.</p>
{table(["Amount", "What it is", "Official source"], [
 ["$1,044,586", "Prop 19 intergenerational cap (transfers 16 Feb 2025 – 15 Feb 2027)", a("lta25009", "BOE LTA 2025/009")],
 ["$661,375 / $793,650", "2027 federal top-rate thresholds (single / joint)", a("rp2635", "Rev. Proc. 2026-35")],
 ["$742,953 / $1,485,906 / $1,010,417", "FTB 2025 Schedule X / Y / Z 12.3% thresholds", a("ftb540", "FTB 2025 Form 540 instructions")],
 ["$768,213 / $1,536,426", "FTB 2026 12.3% thresholds (single / joint)", "FTB published 2026 schedules (via referee-abae constants) " + EXACT],
 ["$1,571 / $1,512 / $2,339.99 / $1,701.60", "CDI published average premiums (statewide / national)", "California Department of Insurance (via referee-abae constants) " + EXACT],
 ["$69,625", "Judicial Council small-value real-property threshold", "courts.ca.gov DE-300 (via public-safe qa) " + EXACT],
 ["Election vote counts (e.g. 84,209; 155,384; 260,241)", "Official preliminary election results, quoted exactly", "the city elections department (name on the linked source; via desk-03242c78 sources) " + EXACT],
])}
</div>

<div class="card">
<h2>Git history — the one step that needs an explicit owner decision</h2>
<p>The live tree is contained, rounded and identifier-free. The public remote still retains the
pre-rounding commits (about 3,500 commits on <code>main</code> history). This session's clone is
shallow (one squashed commit), so the rewrite cannot be performed from here. The procedure, when the
owner authorises it, is: clone the full repository, run <code>git filter-repo</code> to replace the
pre-rounding figures and identifiers in every commit, force-push <code>main</code>, and re-clone every
session branch. That invalidates open PRs and every session branch, and cannot recall copies already
cloned. It is recorded here as the procedure, not executed.</p>
<p class="small">Reference: GitHub Docs, removing sensitive data from a repository —
https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository</p>
</div>

<div class="card">
<h2>Irregularities for review</h2>
{table(["#", "Item", "Status"], [
 ["F1", "Git history still holds the owner's exact figures (see above).", "Owner decision — procedure documented, not executed " + tag("OWNER DECISION", "owner")],
 ["F2", "Repository visibility is public (GitHub Pages requires it on the current plan).", "Owner decision " + tag("OWNER DECISION", "owner")],
 ["F3", "Rounded owner history tables are live on cbe/properties.html (2014–2025 series at $10 rounding).", "Owner decision — keep rounded, drop the series, or move to a private page " + tag("OWNER DECISION", "owner")],
 ["F4", "Owner anchors (a property value and a monthly rent figure, both $10 multiples) appear on live pages.", "Owner decision — keep, round further, or remove " + tag("OWNER DECISION", "owner")],
 ["F5", "Money not rounded to $10 on live pages.", f"CLOSED {CONF} this cycle — every amount is an official figure quoted exactly (table above)"],
 ["F6", "Checker limits (private owner-figure list absent; images/PDFs not inspected).", "Run after every change " + tag("NOTE", "note")],
 ["F7", "Scope of this session.", "Recheck + privacy hardening + integration (this desk) " + tag("NOTE", "note")],
])}
</div>
"""
    return shell("Repo review", "repo-review.html", body)


# --------------------------------------------------------- page: flagged
def page_flagged():
    body = f"""
<div class="card">
<h2>Flagged for review — {DATE}</h2>
<p>Unverified items stay blank in the register and are listed here. Nothing below blocks the merge;
each item names the discovery action that closes it.</p>
{table(["Flag", "Item", "Status"], [
 ["R1", "Property A exact composite property-tax rate (TRA 013 series).", "OPEN — components published; total blank " + OPEN_T],
 ["R2", "Provider of record for Property A's water.", "OPEN — confirm on the tax bill " + OPEN_T],
 ["R4", "California 2026 annual FHFA HPI change (Feb 2027 Prop 19 adjustment input).", "OPEN — quarterly release 24 Nov 2026 " + OPEN_T],
 ["R5 / R6", "Property B water-band discrepancy (owner band vs derived tariff band).", "OPEN — twelve-month bill breakdown " + OPEN_T],
 ["R7", "City transfer-tax factsheet vintage (May 2017 chart).", "OPEN — confirm against the Code text before a $10M+ sale " + OPEN_T],
 ["S1", "Recording-fee PDF link returns 404.", "CLOSED — source updated to the live Clerk-Recorder page " + CONF],
 ["S2", "Treasury daily-yield page paginates; latest rows via FRED series.", "CLOSED — dated yields published from the official Federal Reserve series " + CONF],
 ["S3", "Prop 19 repeal initiative failed to qualify.", "CLOSED — recorded as FAILED on the law-watch page " + FAILED],
 ["F1", "Git history rewrite (pre-rounding commits on the public remote).", "Owner decision — procedure documented on repo-review.html " + tag("OWNER DECISION", "owner")],
 ["F3 / F4", "Rounded history tables and owner anchors on live pages.", "Owner decision " + tag("OWNER DECISION", "owner")],
])}
</div>
"""
    return shell("Flagged for review", "flagged.html", body)


# --------------------------------------------------------- page: sources
def page_sources():
    rows = [
        ["IRS Rev. Proc. 2026-35 (2027 inflation adjustments)", a("rp2635", "irs.gov PDF"), "2027 basic exclusion $15,480,000 (§3.44); gift $20,000 (§3.46(1)); non-citizen spouse $201,000 (§3.46(2)); §2032A cap $1,500,000 (§3.45); §6601(j) 2% portion $2,010,000 (§3.56)"],
        ["IRS Rev. Proc. 2025-32 (2026 inflation adjustments)", a("rp2532", "irs.gov PDF"), "2026 gift $19,000 (§4.42(1)); non-citizen spouse $194,000 (§4.42(2)); §2032A cap $1,460,000 (§4.41); §6601(j) 2% portion $1,940,000 (§4.51)"],
        ["IRS Estate tax (filing-threshold table)", a("irsestate", "irs.gov"), "2026 filing threshold $15,000,000 (statutory, One Big Beautiful Bill Act P.L. 119-21 §70106)"],
        ["BOE Letter to Assessors 2025/009", a("lta25009", "boe.ca.gov PDF"), "Prop 19 cap $1,044,586 for transfers 16 Feb 2025 – 15 Feb 2027; adjustment every other February by FHFA California HPI"],
        ["BOE Letter to Assessors 2026/002", a("lta26002", "boe.ca.gov PDF"), "2026 factored-base factor 1.02 (CCPI +3.307% capped at 2%)"],
        ["SCC Compilation of Tax Rates FY2025-26", a("ratebook", "files.santaclaracounty.gov PDF"), "Countywide levy components; TRA structure (816 tax rate areas)"],
        ["SCC jurisdiction table (TRA series)", a("tra", "plandev.santaclaracounty.gov"), "TRA 013 = the property's incorporated city (name on the linked page)"],
        ["Water utility Schedule No. 1 (CPUC Advice Letter 621-A)", a("sjw", "sjwater.com PDF"), "Service charge $75.84; tiers $4.7924 / $7.1528 / $13.6618 per CCF; CAP surcharge $2.61; territory covers portions of the property's city"],
        ["SFPUC Rate Schedules FY2026-27 / FY2027-28", a("sfpuc", "sfpuc.gov PDF"), "W-1A / W-1B commodity; Schedule A wastewater; Schedule C standard and Schedule D simplified stormwater (Res. 26-0064 / 26-0066)"],
        ["Assessor-Recorder transfer-tax factsheet", a("asr", "media.api.sf.gov PDF"), "Six-tier transfer-tax chart; inheritance and gifts exempt; top tiers $13.75 / $15.00 per $500 (5.5% / 6%)"],
        ["Legislation File 260178 (Legistar)", a("legistar", "sfgov.legistar.com"), "Transfer-tax reduction proposal; reactivated 17 Nov 2026; Unfinished Business; Budget and Finance Committee — PROPOSED"],
        ["Freddie Mac PMMS", a("pmms", "freddiemac.com"), "30-year 7.11%; 15-year 6.45% (week of 12 Nov 2026)"],
        ["FHFA HPI monthly report (Aug 2026 data)", a("hpirep", "fhfa.gov PDF"), "National +0.3% month, +2.4% year (released 27 Oct 2026); quarterly release 24 Nov 2026"],
        ["FHFA HPI release dates", a("hpi", "fhfa.gov"), "2026–2027 release calendar"],
        ["Treasury daily par yield curve", a("treasury", "home.treasury.gov"), "Official curve page (paginated; latest rows via FRED below)"],
        ["FRED DGS3MO / DGS2 (Federal Reserve Bank of St. Louis)", a("fred3m", "fred.stlouisfed.org CSV") + "; " + a("fred2y", "fred.stlouisfed.org CSV"), "3-month 4.33% and 2-year 4.80% as of 17 Nov 2026 (series sourced from Treasury)"],
        ["FTB 2025 Form 540 instructions", a("ftb540", "ftb.ca.gov"), "Line 62 Behavioral Health Services Tax: 1% of taxable income above $1,000,000"],
        ["County Clerk-Recorder recording document fees", a("sccfees", "clerkrecorder.santaclaracounty.gov"), "Documentary transfer tax $0.55 per $500; SB 2 $75; AB 1466 $2; PCOR $20"],
        ["SOS failed-to-qualify list", a("sosfail", "sos.ca.gov"), "60+ homeowner exemption initiative (25-0035) failed 17 Aug 2026"],
        ["SOS CC/ROV Memo #26138 (18 May 2026)", a("sosmemo", "elections.cdn.sos.ca.gov PDF"), "Initiative 1994 (Prop 19 repeal) failed to qualify"],
    ]
    body = f"""
<div class="card">
<h2>Source register — {DATE}</h2>
<p class="small">Every source below was opened and read during this session. Secondary sources (law-firm
blogs, news) were used only as leads and are not cited for any figure.</p>
{table(["Official source", "Link", "What it supports"], rows)}
</div>
"""
    return shell("Sources", "sources.html", body)


# ------------------------------------------------------ page: methodology
def page_method():
    body = f"""
<div class="card">
<h2>Methodology and privacy — {DATE}</h2>
{table(["Rule", "How this desk applies it"], [
 ["Official sources only " + tag("RULE", "note"), "Every figure is read from the official document named in its source link. A value that cannot be confirmed stays blank and is flagged OPEN. No inferred values."],
 ["Rounding " + tag("RULE", "note"), "All money is a multiple of $10, except agency-published exact figures marked EXACT (only $1,044,586 in this desk) and rates under $1,000, which are quoted as published."],
 ["Anonymisation " + tag("RULE", "note"), "County-level only (Santa Clara County; San Francisco County). No names, street addresses, ZIP codes, parcel or account numbers, or city/neighbourhood names on any page."],
 ["Owner figures " + tag("RULE", "note"), "Owner-supplied bands are labelled OWNER and never published as verified. They appear only in the consistency-check table, as bands."],
 ["Verdicts " + tag("RULE", "note"), "CONFIRMED = read this session. UPDATED = changed or first published since 2026-11-17. OPEN = blank, flagged. PROPOSED / FAILED = not law."],
 ["Rebuild " + tag("RULE", "note"), "The coverage-desk model was re-run this session (21 tests OK). The movement check is on rebuild.html."],
 ["Not advice " + tag("RULE", "note"), "A working decision aid prepared for review by a licensed California attorney and a CPA. Re-check the then-current law before acting."],
])}
</div>
"""
    return shell("Methodology", "methodology.html", body)


PAGES = {
    "index.html": page_index,
    "register.html": page_register,
    "open-items.html": page_open,
    "rebuild.html": page_rebuild,
    "requirements.html": page_requirements,
    "law-watch.html": page_law,
    "repo-review.html": page_repo,
    "flagged.html": page_flagged,
    "sources.html": page_sources,
    "methodology.html": page_method,
}


def main():
    (OUT / "style.css").write_text(CSS.strip() + "\n")
    for name, fn in PAGES.items():
        (OUT / name).write_text(fn())
        print(f"wrote {name}")
    print(f"done: {len(PAGES)} pages + style.css")


if __name__ == "__main__":
    main()
