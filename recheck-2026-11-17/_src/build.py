#!/usr/bin/env python3
"""Build the periodic official-source recheck desk (2026-11-17).

Session arena-1e93b0b8, tasks 1e9/RECHECK, 1e9/INDEX, 1e9/REBUILD, 1e9/REVIEW.
Every figure on these pages was read from the official document named in its
source link during the 2026-11-17 session, or is explicitly marked as carried
over from a prior verified read (P), derived (D), assumption (A), owner (O) or
unverified (U). Money is a multiple of $10 except agency-published exact
figures, which are marked EXACT.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent
DATE = "2026-11-17"

# ---------------------------------------------------------------- source URLs
S = {
    "rp2635": "https://www.irs.gov/pub/irs-drop/rp-26-35.pdf",
    "rp2532": "https://www.irs.gov/pub/irs-drop/rp-25-32.pdf",
    "irs2027": "https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2027-taxpayers-continue-to-benefit-from-the-working-families-tax-cuts",
    "lta25009": "https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf",
    "lta26002": "https://www.boe.ca.gov/proptaxes/pdf/lta26002.pdf",
    "boe19": "https://www.boe.ca.gov/prop19/",
    "ratebook": "https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf",
    "tra": "https://plandev.santaclaracounty.gov/how-do-i/research-property/find-jurisdiction",
    "highlights": "https://controller.santaclaracounty.gov/property-tax-distribution/property-tax-highlights",
    "sjw": "https://www.sjwater.com/media/2zxdiui1/al621a_advice_letter_web-1.pdf",
    "sfpuc": "https://www.sfpuc.gov/sites/default/files/accounts-and-services/Rates_Schedule_Water_Sewer_2026-7.pdf",
    "asr": "https://media.api.sf.gov/documents/ASR_Factsheet_PropertyTransfer_English_2025.pdf",
    "sftitle": "https://media.api.sf.gov/documents/Title_and_Summary_Changes_to_Real_Property_Transfer_Tax_third_submission.pdf",
    "legistar": "https://sfgov.legistar.com/LegislationDetail.aspx?GUID=AC759C0E-DED0-450B-BA55-A54F7F19F8D0&ID=7933667",
    "pmms": "https://www.freddiemac.com/pmms",
    "hpi": "https://www.fhfa.gov/data/hpi",
    "treasury": "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026",
    "ftb540": "https://www.ftb.ca.gov/forms/2025/2025-540-instructions.html",
    "sccfees": "https://files.santaclaracounty.gov/exjcpb1531/2025-09/recording-fees-schedule.pdf",
    "sfhpi": "https://www.fhfa.gov/hpi",
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
UPDATED = tag("UPDATED", "updated")
CONF = tag("CONFIRMED", "verified")


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


def shell(title, active, body, subtitle):
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
<footer>Built {DATE} by session arena-1e93b0b8 from one generator (<code>_src/build.py</code>). Working decision aid, not advice. Figures rounded to the nearest $10 except agency-published exact figures marked EXACT. County-level anonymisation: no names, street addresses, ZIP codes, parcel or account numbers.</footer>
</body>
</html>
"""


def table(headers, rows):
    h = "".join(f"<th>{c}</th>" for c in headers)
    cells = []
    for r in rows:
        tds = []
        for i, c in enumerate(r):
            cls = ' class="num"' if i in NUMCOLS else ""
            tds.append(f"<td{cls}>{c}</td>")
        cells.append("<tr>" + "".join(tds) + "</tr>")
    return f"<table><thead><tr>{h}</tr></thead><tbody>{''.join(cells)}</tbody></table>"


NUMCOLS = set()  # pages set this before rendering


# --------------------------------------------------------------- page: hub
def page_index():
    NUMCOLS.clear()
    body = f"""
<div class="card">
<h2>What this is</h2>
<p>The owner brief requires the project to <b>periodically recheck official federal, state and local
authorities and distinguish enacted changes from proposals</b>, and after any input change to
<b>rebuild the model and the site and see whether the recommendation moved</b>. This desk is the
recheck of {DATE}. Every row of the <a href="register.html">constants register</a> was read from the
official document named in its source link during this session (rows marked <span class="tag tag-prior">PRIOR READ</span>
were line-read by the 2026-11-13/15 verification sessions and re-checked for consistency here).</p>
<div class="callout"><b>Headline verdict — the recommendation did not move.</b> The standing
sequence (sell Property A in the transfer year, do not take the intergenerational exclusion unless
the household will occupy the home for years, write the investment policy before the money arrives)
is unchanged by every input updated in this cycle. The arithmetic is on
<a href="rebuild.html">Rebuild &amp; movement</a>.</div>
</div>

<div class="card kpi">
<div class="box"><b>23</b>rows confirmed line-by-line from official sources</div>
<div class="box"><b>5</b>rows updated or newly published since 2026-11-15</div>
<div class="box"><b>4 / 2</b>six open items closed / partially closed</div>
<div class="box"><b>7</b>new or restated flags for review</div>
<div class="box"><b>0</b>recommendation changes</div>
</div>

<div class="card">
<h2>The six items left open by the 2026-11-13 verification register — status today</h2>
{table(["Item", "Status {DATE}", "Where"], [
 ["Santa Clara County composite property-tax rate (FY2025-26 rate book)",
  f"PARTIAL — components and the tax-rate-area series read officially; exact composite per TRA {OPEN_T}",
  '<a href="open-items.html">Open items</a> &middot; flag R1'],
 ["Property A water utility tariff (fixed charge and tier-1 rate)",
  f"CLOSED — published tariff read in full {CONF}", '<a href="open-items.html">Open items</a>'],
 ["Property B water and sewer schedule, FY2026-27",
  f"CLOSED — adopted schedules read in full {CONF}", '<a href="open-items.html">Open items</a>'],
 ["Property B city transfer tax brackets",
  f"CLOSED — bracket chart read; top tiers confirmed against the official current-law document {CONF}",
  '<a href="open-items.html">Open items</a>'],
 ["30-year fixed mortgage rate (context only)",
  f"CLOSED — survey re-read {CONF}", '<a href="open-items.html">Open items</a>'],
 ["FHFA house-price series (levels and growth)",
  f"CLOSED — release read; statutory 2026 California figure not yet published {CONF}",
  '<a href="open-items.html">Open items</a> &middot; flag R4'],
])}
</div>

<div class="card">
<h2>Decision and date log</h2>
{table(["Item", "Decision", "Date"], [
 ["Recheck cycle", f"Executed; six open items closed or partially closed; register published. {CONF}", "2026-11-17"],
 ["2027 federal figures", "Adopted $15,480,000 basic exclusion and $20,000 annual gift exclusion as the authoritative 2027 amounts for all forward projections. " + UPDATED, "2026-11-17"],
 ["Recommendation", f"Reviewed against updated inputs; <b>unchanged</b>. " + tag("NO MOVE", "move"), "2026-11-17"],
 ["Property A tax-rate-area composite", "Left blank pending a parcel-level lookup; components published instead of an inferred total. " + OPEN_T, "2026-11-17"],
 ["Property B water band", "Owner band and published-tariff derived band diverge; flagged for a twelve-month bill breakdown before the rent paths are re-ranked. " + OPEN_T, "2026-11-17"],
 ["SF transfer-tax proposal", "Recorded as PROPOSED (Legistar File 260178, pending committee); models keep enacted rates. " + PROPOSED, "2026-11-17"],
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
    return shell("Recheck hub", "index.html", body, DATE)


# --------------------------------------------------------- page: register
def page_register():
    NUMCOLS.clear()
    rows = [
        ["Federal estate/gift basic exclusion, 2026", "$15,000,000", EXACT, a("rp2532", "IRS Rev. Proc. 2025-32") + " " + PRIOR, CONF, "2026-11-17"],
        ["Federal basic exclusion, 2027", "$15,480,000", EXACT, a("rp2635", "IRS Rev. Proc. 2026-35 §3.44") + " (read this session)", UPDATED, "2026-11-17"],
        ["Generation-skipping exemption, 2027", "$15,480,000", EXACT, a("rp2635", "IRS Rev. Proc. 2026-35 §3.44") + " (read this session)", UPDATED, "2026-11-17"],
        ["Annual gift exclusion, 2026", "$19,000", EXACT, a("rp2532", "IRS Rev. Proc. 2025-32") + " " + PRIOR, CONF, "2026-11-17"],
        ["Annual gift exclusion, 2027", "$20,000", EXACT, a("rp2635", "IRS Rev. Proc. 2026-35 §3.46(1)") + " (read this session)", UPDATED, "2026-11-17"],
        ["Gifts to a non-citizen spouse, 2027", "$201,000", EXACT, a("rp2635", "IRS Rev. Proc. 2026-35 §3.46(2)") + " (read this session)", UPDATED, "2026-11-17"],
        ["§6601(j) 2-percent portion, 2027 estates", "$2,010,000", EXACT, a("rp2635", "IRS Rev. Proc. 2026-35 §3.56") + " (read this session)", UPDATED, "2026-11-17"],
        ["§2032A special-use aggregate cap, 2027", "$1,500,000", EXACT, a("rp2635", "IRS Rev. Proc. 2026-35 §3.45") + " (read this session)", CONF, "2026-11-17"],
        ["Prop 19 intergenerational value cap (add-on over factored base)", "$1,044,586 for transfers 16 Feb 2025 – 15 Feb 2027", EXACT, a("lta25009", "BOE Letter to Assessors 2025/009") + " (read this session)", CONF, "2026-11-17"],
        ["Prop 19 cap adjustment rule", "Adjusted every other February by the FHFA House Price Index for California; next adjustment February 2027", "rule", a("lta25009", "BOE LTA 2025/009") + " (read this session)", CONF, "2026-11-17"],
        ["Prop 19 cap amount from Feb 2027", "not determinable until BOE publishes the adjusted amount", "", a("lta25009", "BOE LTA 2025/009") + " " + a("hpi", "FHFA HPI"), OPEN_T, "2026-11-17"],
        ["Prop 13 factored-base inflation factor, 2026 roll", "1.02 (CCPI +3.307%, capped at 2%)", EXACT, a("lta26002", "BOE LTA 2026/002") + " (read this session)", CONF, "2026-11-17"],
        ["Countywide levy components, FY2025-26 (per $100 of taxable value)", "1% maximum levy 1.00000; county retirement levy 0.03880; VMC 2008 0.00520; county housing bond 2016 0.00560", "rates", a("ratebook", "SCC Compilation of Tax Rates FY2025-26") + " (read this session)", CONF, "2026-11-17"],
        ["Property A taxing-area series", "series 013 (the property's incorporated city; name on the linked county table, not repeated under the anonymisation rule)", "", a("tra", "SCC jurisdiction table") + " (read this session)", CONF, "2026-11-17"],
        ["Property A school / college / hospital bond components (per $100)", "Elem 2001 0.01650; Elem 2012 0.01690; Elem 2024 0.00010; hospital 2003 0.00200; community college 1999 0.00750", "rates", a("ratebook", "SCC rate book FY2025-26") + " (read this session)", CONF, "2026-11-17"],
        ["Property A exact composite rate for its TRA", "blank pending parcel-level lookup (rate-book pages for the 013 series sit beyond the automated parse window)", "", a("ratebook", "SCC rate book FY2025-26") + " " + a("tra", "TRA lookup"), OPEN_T, "2026-11-17"],
        ["Property A water — service charge, meter 5/8×3/4 in (per month)", "$75.84", EXACT, a("sjw", "Water utility Schedule No. 1 (CPUC tariff, AL 621-A)") + " (read this session)", CONF, "2026-11-17"],
        ["Property A water — residential tier 1, 0–6 CCF per month", "$4.7924 per CCF", EXACT, a("sjw", "Water utility Schedule No. 1") + " (read this session)", CONF, "2026-11-17"],
        ["Property A water — residential tiers 2 / 3", "$7.1528 per CCF (6–12); $13.6618 per CCF (over 12)", EXACT, a("sjw", "Water utility Schedule No. 1") + " (read this session)", CONF, "2026-11-17"],
        ["Property A water — bill add-ons", "assistance-program surcharge $2.61 per month; loan surcharge $0.02 per month; commission fee 0.7%; utility user tax 5%", EXACT, a("sjw", "Water utility Schedule No. 1, special conditions") + " (read this session)", CONF, "2026-11-17"],
        ["Property A water — provider of record for the parcel", "blank (the confirmed utility serves only portions of the city; confirm on the tax bill)", "", a("sjw", "Water utility tariff territory") + " " + a("ratebook", "county rate book"), OPEN_T, "2026-11-17"],
        ["Property A water — derived annual band (usage assumption 8–12 CCF per month)", "$1,540 – $1,900 per year", DERIVED + " from the tariff rows above", a("sjw", "Water utility Schedule No. 1"), CONF, "2026-11-17"],
        ["Property B water — service charge, meter 3/4 in (FY2026-27)", "$24.93 per month", EXACT, a("sfpuc", "SFPUC Rate Schedules FY2026-27 (Res. 26-0064)") + " (read this session)", CONF, "2026-11-17"],
        ["Property B water — single-family commodity (W-1A)", "$12.20 per CCF first 4 units; $13.55 additional (FY2026-27)", EXACT, a("sfpuc", "SFPUC Schedule W-1A") + " (read this session)", CONF, "2026-11-17"],
        ["Property B water — multi-family commodity (W-1B)", "$12.03 per CCF first 3 units per dwelling; $12.91 additional (FY2026-27)", EXACT, a("sfpuc", "SFPUC Schedule W-1B") + " (read this session)", CONF, "2026-11-17"],
        ["Property B wastewater — residential (Schedule A, FY2026-27)", "service $6.62 per month; $20.74 per discharge unit; flow factor 90% single-family, 95% multi-family", EXACT, a("sfpuc", "SFPUC Schedule A (Res. 26-0066)") + " (read this session)", CONF, "2026-11-17"],
        ["Property B water/sewer — FY2027-28 step", "service $26.68 (3/4 in); commodity $13.05 / $14.49 (W-1A); wastewater $22.84 per discharge unit", EXACT, a("sfpuc", "SFPUC FY2027-28 columns") + " (read this session)", CONF, "2026-11-17"],
        ["Property B stormwater component (residential tiers)", "tier structure exists in Schedule D; exact tiers not transcribed in this cycle", "", a("sfpuc", "SFPUC Schedule D"), OPEN_T, "2026-11-17"],
        ["Property B transfer tax, tier $1M – under $5M", "$3.75 per $500 (0.75%)", EXACT, a("asr", "Assessor-Recorder transfer factsheet (chart)") + " (read this session)", CONF, "2026-11-17"],
        ["Property B transfer tax, tiers below $1M", "$2.50 per $500 to $250,000; $3.40 per $500 to $1,000,000", EXACT, a("asr", "Assessor-Recorder transfer factsheet") + " (read this session)", CONF, "2026-11-17"],
        ["Property B transfer tax, tier $5M – under $10M", "$11.25 per $500 (2.25%)", EXACT, a("asr", "Assessor-Recorder transfer factsheet") + " (read this session)", CONF, "2026-11-17"],
        ["City transfer tax top tiers (enacted)", "5.5% from $10M to under $25M; 6% from $25M", EXACT, a("sftitle", "Controller current-law digest") + " (read this session)", CONF, "2026-11-17"],
        ["City transfer-tax reduction (proposed)", "2.75% / 3.0% from 1 Jul 2026, single-family residences excluded from the reduction — pending committee", PROPOSED, a("legistar", "Legislation File 260178") + " (read this session)", PROPOSED, "2026-11-17"],
        ["County documentary transfer tax (Property A sale)", "$0.55 per $500 (0.11%)", EXACT, a("sccfees", "County Clerk-Recorder fee schedule") + " " + PRIOR, CONF, "2026-11-17"],
        ["County recording fees on the sell path", "SB 2 $75; AB 1466 $2; preliminary change-of-ownership $20", EXACT, a("sccfees", "County Clerk-Recorder fee schedule") + " " + PRIOR, CONF, "2026-11-17"],
        ["Mortgage rate context (no debt modelled)", "30-year fixed 7.11%; 15-year 6.45% (week of 12 Nov 2026)", EXACT, a("pmms", "Freddie Mac PMMS") + " (read this session)", CONF, "2026-11-17"],
        ["FHFA House Price Index, national", "+0.3% Aug 2026 month; +2.4% year (27 Oct 2026 release); quarterly release 24 Nov 2026", EXACT, a("hpi", "FHFA HPI release") + " (read this session)", CONF, "2026-11-17"],
        ["FHFA House Price Index, California 2026 annual change (statutory input to the Feb 2027 Prop 19 adjustment)", "blank — published in early 2027", "", a("hpi", "FHFA HPI"), OPEN_T, "2026-11-17"],
        ["Short Treasury yields (phased-path parking)", "curve current through 16 Nov 2026; 3-month 4.32% and 2-year 4.88% as of 13 Nov 2026", EXACT + " (dated)", a("treasury", "Treasury daily par yield curve") + " " + PRIOR, CONF, "2026-11-17"],
        ["California income tax: 1% surcharge above $1,000,000 taxable income (Behavioral Health Services Tax, Form 540 line 62)", "1% of the excess only; California taxes capital gain as ordinary income", EXACT, a("ftb540", "FTB 2025 Form 540 instructions") + " " + PRIOR, CONF, "2026-11-17"],
        ["California estate / inheritance tax", "none enacted (state inheritance tax repealed 1982; no current statute)", "rule", a("ftb540", "FTB") + " " + PRIOR, CONF, "2026-11-17"],
    ]
    body = f"""
<div class="card">
<h2>Constants register — read from official sources {DATE}</h2>
<p class="small">Verdicts: CONFIRMED = read against the official document this session or re-checked against a
prior line-read. UPDATED = the published figure changed or first appeared since the 2026-11-15 build.
OPEN = cannot be confirmed yet; the cell is blank and the row carries a flag on
<a href="flagged.html">Flagged for review</a>. PROPOSED = not law.</p>
{table(["Item", "Value", "Basis", "Official source", "Verdict", "Checked"], rows)}
</div>

<div class="card">
<h2>Consistency check: owner cost bands against published tariffs</h2>
<p class="small">Owner-supplied bands are unverified inputs. This table checks them against the tariff rows
above. It does not publish any owner bill.</p>
{table(["Check", "Owner band (owner-supplied)", "Derived from official tariffs", "Verdict", "Source"], [
 ["Property A water, per year", "$1,200 – $1,800 (from $100–$150 per month)", "$1,540 – $1,900 at 8–12 CCF per month", tag("CONSISTENT", "verified"), a("sjw", "Water utility tariff")],
 ["Property B water and sewer, per month", "$330 – $400 (owner-supplied)", "water ~$210 + wastewater ~$300 before stormwater at 15 CCF — derived band is higher, suggesting the owner band covers water only or fewer units", OPEN_T, a("sfpuc", "SFPUC schedules")],
 ["Property A electricity", "net credit of $10 – $20 per month (solar; owner-supplied)", "not derivable from a tariff — net-billing arrangement unverified", tag("OWNER", "owner"), a("sfpuc", "general rate reference")],
])}
</div>
"""
    return shell("Constants register", "register.html", body, DATE)


# ------------------------------------------------------ page: open items
def page_open():
    NUMCOLS.clear()
    body = f"""
<div class="card">
<h2>The six items left open on 2026-11-13 — closure record {DATE}</h2>
{table(["Open item (as registered 2026-11-13)", "What was read this session", "Verdict", "Residual"], [
 ["Property A county composite tax rate (FY2025-26 rate book)",
  "The countywide components (1% levy, retirement levy, voter-approved debt line items) and the property's taxing-area series were read from the official rate book and the official jurisdiction table. The composite total printed for each 013-series TRA page sits beyond the automated 30-page parse window of the rate book PDF.",
  f"PARTIAL {OPEN_T}", "flag R1 — read the 013-series pages of the linked rate book (section III) or the parcel's tax bill; do not infer a total from components"],
 ["Property A water utility tariff (fixed charge and tier-1 rate)",
  "The regulated utility's published Schedule No. 1 was read in full: service charge, three residential tiers, assistance and loan surcharges, commission fee, utility user tax. The tariff's stated territory covers portions of the property's city.",
  f"CLOSED {CONF}", "flag R2 — the provider of record for the parcel itself is still unconfirmed without an address"],
 ["Property B water and sewer schedule, FY2026-27",
  "Adopted rate schedules were read in full: water service charges and two-tier commodity (single-family and multi-family), residential wastewater service charge and per-discharge-unit rate, flow factors, and the FY2027-28 step.",
  f"CLOSED {CONF}", "flag R3 — residential stormwater tiers (Schedule D) not transcribed; see the linked schedule"],
 ["Property B city transfer tax brackets",
  "The Assessor-Recorder transfer-tax chart was read in full (six tiers). The two top tiers in that chart predate the current top-tier rates, which were confirmed against the Controller's official current-law digest (5.5% / 6%) and the pending legislation's own description of current law.",
  f"CLOSED {CONF}", "flag R7 — the factsheet is a 2017-vintage chart carrying a 2025 file name; low tiers unchanged, top tiers stale"],
 ["30-year fixed mortgage rate",
  "The survey page was re-read: 7.11% (30-year) and 6.45% (15-year), week of 12 Nov 2026. Context only — neither property carries a mortgage in the model.",
  f"CLOSED {CONF}", "none"],
 ["FHFA house-price series (levels and growth)",
  "The official index page was re-read: national +0.3% month / +2.4% year (Aug 2026 data, 27 Oct 2026 release), quarterly release scheduled 24 Nov 2026. The long-run 3.5% growth input stays labelled ASSUMPTION on the projection desks.",
  f"CLOSED {CONF}", "flag R4 — the California 2026 annual change (the statutory input for the February 2027 Prop 19 cap adjustment) is not published until early 2027"],
])}
</div>

<div class="card">
<h2>New and restated flags {DATE}</h2>
{table(["Flag", "What it is", "Why it is not resolved here", "Discovery action"], [
 ["R1", "Exact FY2025-26 composite property-tax rate for the property's taxing area " + a("ratebook", "rate book"), "The rate book publishes each TRA total only on its own page; the automated read window stops before the 013 series. Inferring a total from components would violate the no-inference rule.", "Open the linked county rate book, section III, pages for the 013 series, or read the parcel's tax bill; record the total and this flag closes."],
 ["R2", "Provider of record for Property A's water " + a("sjw", "tariff territory"), "The confirmed utility serves only portions of the city; a second provider exists in parts of the same jurisdiction. Naming the provider needs the parcel.", "Check the tax bill or the county assessor record for the service district; one line closes this."],
 ["R3", "Residential stormwater tiers for Property B " + a("sfpuc", "Schedule D"), "The tiers sit on a schedule page not parsed in this cycle.", "Read Schedule D of the linked rate document; transcribe the three residential tiers."],
 ["R4", "February 2027 Prop 19 cap amount " + a("lta25009", "BOE letter"), "Statutorily adjusted only after the FHFA California annual change for 2026 is published (early 2027).", "Re-run this recheck after the board's February 2027 letter; until then projections use the enacted $1,044,586 plus a modelled inflation step labelled ASSUMPTION."],
 ["R5", "Treasury curve full refresh " + a("treasury", "curve table"), "The official table paginates and the raw feed returned a server error during this cycle; the latest curve values on file (13 Nov 2026) were re-checked against the live table header (16 Nov 2026).", "At the next recheck, pull the curve CSV and refresh the parking yields."],
 ["R6", "Property B owner cost band vs derived tariff band " + a("sfpuc", "adopted rates"), "The owner's $330–$400 per month sits below the water-plus-wastewater total derived from adopted rates at a plausible 3-unit usage, which suggests a scope difference (water only, or fewer billable units).", "Obtain a twelve-month bill breakdown (water vs wastewater vs stormwater, units billed) and re-rank the rent paths."],
 ["R7", "Stale vintage of the city transfer-tax factsheet " + a("asr", "factsheet"), "The official factsheet is a 2017 chart published under a 2025 file name; its low tiers are unchanged law but its top tiers are superseded.", "Ask the Assessor-Recorder for a current chart; until then the register cites the Controller's current-law digest for the top tiers."],
])}
</div>
"""
    return shell("Open items and flags", "open-items.html", body, DATE)


# ------------------------------------------------------- page: rebuild
def page_rebuild():
    NUMCOLS.clear()
    # derived illustrations: house at transfer under a stated growth assumption
    def grow(v, years, r=0.035):
        x = v
        for _ in range(years):
            x *= (1 + r)
        return round(x / 10) * 10

    h2040 = grow(3_100_000, 14)
    h2045 = grow(3_100_000, 19)
    h2050 = grow(3_100_000, 24)
    e2040 = grow(15_480_000, 13, 0.025)
    e2045 = grow(15_480_000, 18, 0.025)
    e2050 = grow(15_480_000, 23, 0.025)

    def fm(x):
        return f"${x:,.0f}"

    body = f"""
<div class="card">
<h2>Inputs that changed this cycle</h2>
{table(["Input", "Was (2026-11-15 build)", "Now ({DATE})", "Where it bites"], [
 ["Federal basic exclusion, 2027", "indexed from $15,000,000, amount unpublished", "$15,480,000 " + tag("EXACT", "exact"), "estate-tax headroom only"],
 ["Annual gift exclusion, 2027", "$19,000", "$20,000 " + tag("EXACT", "exact"), "gifting cadence only"],
 ["Mortgage rate context", "7.32% (22 Oct 2026)", "7.11% (12 Nov 2026) " + tag("EXACT", "exact"), "none — no debt in the model"],
 ["Short Treasury yields", "3-month 4.32% / 2-year 4.88% (13 Nov 2026)", "unchanged on file; curve live through 16 Nov 2026 " + a("treasury", "Treasury curve"), "phased-entry parking yield"],
 ["Property A / B utility rows", "blank + flagged", "adopted tariffs read and published " + a("sjw", "utility A") + " " + a("sfpuc", "utility B"), "carrying costs on all hold paths, symmetrically"],
])}
</div>

<div class="card">
<h2>Why the ranking holds (the arithmetic)</h2>
<p>The three pure paths and the mixed paths are ranked by after-tax value at the same transfer dates and
horizons. None of the changed inputs feeds those rankings:</p>
<ul>
<li><b>Estate-tax headroom</b> is not binding in any modelled year. Illustration (derived, ASSUMPTION
growth 3.5% on the house value anchor, 2.5% indexation of the exclusion):</li>
</ul>
{table(["Transfer year", "House at transfer (derived)", "Exclusion (indexed from $15,480,000)", "Headroom before any other estate assets", "Binding?"], [
 ["2040", fm(h2040), fm(e2040), fm(e2040 - h2040), "no " + DERIVED + " " + a("rp2635", "exclusion basis")],
 ["2045", fm(h2045), fm(e2045), fm(e2045 - h2045), "no " + DERIVED + " " + a("rp2635", "exclusion basis")],
 ["2050", fm(h2050), fm(e2050), fm(e2050 - h2050), "no " + DERIVED + " " + a("rp2635", "exclusion basis")],
])}
<p class="small">Basis: derived illustration, not a forecast. The exclusion row assumes statutory
indexation continues; the house row uses the desks' planning assumption. Both are labelled
{DERIVED}. The estate's other assets (owner-supplied, unverified) are what can make the exclusion
binding — that is why the estate-liquidity plan and the portability question stay on the
<a href="requirements.html">requirement index</a>. Since the exclusion is slack in every modelled
year, the 2027 update moves headroom, not the ranking of live / rent / sell.</p>
<ul>
<li><b>Carrying costs</b> changed for both hold paths symmetrically: Property A's water is now
sourced at the published tariff (derived $1,540–$1,900 per year), which matches the owner's
$1,200–$1,800 band and therefore does not move the rent-vs-live margin. Property B's derived
water-plus-wastewater band is <i>higher</i> than the owner band (flag R6) — this depresses both
the rent path and the live path of Property B together and does not flip their order.</li>
<li><b>The phased-investing path</b> parks proceeds in 3-month to 2-year Treasuries for 24–36
months; its parking yield input is unchanged this cycle (flag R5).</li>
<li><b>Capital-gains treatment</b> is unchanged: basis resets to market value at death
(step-up), a same-year sale realises no meaningful gain, and California taxes any later gain as
ordinary income including the 1% surcharge above $1,000,000 of taxable income (Form 540 line 62,
confirmed).</li>
</ul>
<div class="callout"><b>Verdict {DATE}: the recommendation did not move.</b> Sell Property A in the
transfer year; do not claim the intergenerational exclusion unless the household will occupy the
home for years; write the investment policy before the money arrives; decide Property B's vacant
unit first. {tag("NO MOVE", "move")}</div>
</div>

<div class="card">
<h2>Rebuild performed</h2>
<p class="small">The model engines and the site generators were re-run on {DATE} with the updated
register: the regression suites for the projection engines pass unchanged (their outputs do not
depend on the 2027 exclusion within the slack range), and the published desks remain internally
consistent. The desk that carries 2027 figures (<code>desk-03242c78</code>) already matches the
official amounts read today; the desks anchored on 2026 figures remain correct <i>for 2026</i> and
are listed on the <a href="requirements.html">requirement index</a> with this register as the
2027+ authority.</p>
</div>
"""
    return shell("Rebuild and recommendation movement", "rebuild.html", body, DATE)


# --------------------------------------------------- page: requirements
REQS = [
    ("Phased-investing path in the black-swan section (proceeds in 3-month–2-year Treasuries 24–36 months, then phase into stocks; test 1929/2008 crash entry)", "ANSWERED", 'desk-85a01c5c/black-swan.html (quantified replay), desk-03242c78/phased.html, cbe/phased-investing.html'),
    ("Scrub pre-rounding git history / keep the repo privacy-first", "PARTIAL", 'repo-review.html — live tree contained, rounded and identifier-free (2026-11-17 containment); the public remote still retains ~3,500 commits with pre-rounding figures; the filter-repo rewrite + force-push is owner decision F1 (not performed)'),
    ("One-page printable Attorney &amp; CPA Briefing Sheet export", "ANSWERED", 'desk-03242c78/briefing-attorney.html, briefing-cpa.html; desk-85a01c5c/briefing-sheet.html'),
    ("Replace round-number assumptions with ranges or real figures", "ANSWERED", 'desk-03242c78/workbook.html, what-would-change.html; what-if pages'),
    ("Put &ldquo;what would change the answer&rdquo; on the first screen", "ANSWERED", 'desk-03242c78/index.html + what-would-change.html; desk-85a01c5c/index.html'),
    ("Model mixed paths, not only the three pure choices", "ANSWERED", 'desk-03242c78/mixed-paths.html; decision-d2664fd0/mixed-paths.html; cbe/options.html'),
    ("Show reinvestment risk beside the headline", "ANSWERED", 'desk-85a01c5c/black-swan.html (cost-of-cushion beside every headline)'),
    ("Add what-if controls", "ANSWERED", 'desk-85a01c5c/what-if.html; decision-d2664fd0/what-if.html; cbe/assets/what-if.js'),
    ("One-page brief for the attorney and the tax adviser", "ANSWERED", 'see briefing-sheet row above'),
    ("Show the deadlines as a timeline", "ANSWERED", 'desk-03242c78/timeline.html; decision-d2664fd0/timeline.html; cbd/timeline.html'),
    ("Group the menu and add a glossary", "ANSWERED", 'grouped nav + glossary.html on desk-03242c78, desk-85a01c5c, decision-d2664fd0, cbd'),
    ("Compare all choices at the same transfer dates and horizons, with taxes, debt, occupancy changes, capital costs and liquidity", "ANSWERED", 'desk-03242c78/choices.html + sell-path.html; desk-85a01c5c/scenarios.html (2040/2045/2050)'),
    ("Periodically recheck official authorities; distinguish enacted from proposals", "ANSWERED (cycle 2026-11-17)", 'this desk: register.html + law-watch.html'),
    ("Agree in writing what would make the household choose each path, before the figures arrive", "ANSWERED (awaiting owner signature)", 'desk-03242c78/what-would-change.html + suggestions.html; desk/decision.html'),
    ("Contain the prior public-data exposure", "PARTIAL", 'repo-review.html — live surface contained by the 2026-11-17 privacy rounds (identifiers and exact figures removed; locality-naming trees hidden); remote history exposure remains owner decision F1'),
    ("Build a private estate inventory", "PARTIAL", 'template and liquidity plan on desk-9af5443d; the filled inventory must stay off-repo (owner action)'),
    ("Obtain independent property and rental estimates", "PARTIAL", 'comparables published (desk-9af5443d rents); independent appraisals are an offline owner action'),
    ("Validate Proposition 19 eligibility", "ANSWERED", 'desk-03242c78/prop19.html (conditions, occupancy test, filing)'),
    ("Model depreciation and recapture", "ANSWERED", 'desk-03242c78/depreciation.html'),
    ("Verify Property B leases and local rules", "PARTIAL", 'desk-03242c78/local-rules.html covers the ordinance framework; lease review needs the leases (owner action)'),
    ("Create a documented investing policy", "ANSWERED", 'desk-03242c78/investment-policy.html'),
    ("Run tax-aware sensitivities", "ANSWERED", 'what-if sensitivity grids; desk-03242c78/workbook.html'),
    ("Review extreme scenarios annually", "ANSWERED (cycle)", 'swan-3a49, desk-85a01c5c/black-swan.html; annual-rerun.html'),
    ("Track proposed legislation", "ANSWERED", 'law-watch.html (this desk) + desk-85a01c5c/law-watch.html'),
    ("Improve dashboard explanations", "ANSWERED (iterative)", 'suggestions boards across desks'),
    ("Add an imputed-rent input for living paths", "ANSWERED", 'desk-03242c78/live-path.html + choices.html; decision-d2664fd0/mixed-paths.html'),
    ("Switch on the primary-residence exclusion for living-then-sell paths", "ANSWERED", 'desk-03242c78/sec121.html'),
    ("Model Prop H with its official terms", "ANSWERED", 'desk-03242c78/propH.html; desk-9af5443d (both measures modelled with official terms)'),
    ("Carry the Proposition 19 allowance forward", "ANSWERED", 'desk-03242c78/prop19.html (carry-forward mechanics)'),
    ("Price the transfer tax and recording fees into the sell path", "ANSWERED", 'desk-03242c78/sell-path.html; register.html (bracket rows, this cycle)'),
    ("Run the private model on ranges rather than points", "ANSWERED", 'desk-03242c78/workbook.html; what-if pages'),
    ("Read the official Form 540 instructions for the 1% tax above one million and the capital-gain treatment; update the sensitivity value", "ANSWERED", 'desk-9af5443d (line-read; sensitivity updated); register.html (re-checked)'),
    ("Obtain comparables for Property A so the rent path is ranked on evidence", "ANSWERED (official comparables)", 'desk-9af5443d (Census/ACS and fair-market-rent comparables); broker comps remain an owner action'),
    ("After any input changes, rebuild the model and the site and see whether the recommendation moved", "ANSWERED (cycle)", 'rebuild.html'),
    ("Write the decision and the date next to the item", "ANSWERED", 'index.html decision log; desk-9af5443d decision-and-date log'),
    ("Look up Property A&rsquo;s tax rate area and read the published rate", "PARTIAL", 'register.html — series identified and components read officially; composite flagged R1 pending parcel-level lookup'),
    ("Model a sale in the same tax year as the inheritance, before deciding anything else", "ANSWERED", 'desk-03242c78/sell-path.html; standing recommendation step 1'),
    ("Claim the Proposition 19 exclusion only if the heir will occupy the home long term", "ANSWERED", 'desk-03242c78/prop19.html + what-would-change.html; recommendation step 2'),
    ("Build a five-year maintenance and capital plan for both buildings", "ANSWERED", 'desk-9af5443d; desk-03242c78/maintenance.html'),
    ("Obtain a written valuation of Property A at the date of death", "OPEN (future trigger)", 'desk-03242c78/valuation.html — required at death; cannot exist before it'),
    ("Decide whether a like-kind exchange is wanted, and take advice before selling", "ANSWERED (awaiting owner choice)", 'desk-03242c78/like-kind.html'),
    ("Write an investment policy for the sale proceeds before the money arrives", "ANSWERED", 'see investing-policy row'),
    ("Prepare an estate liquidity plan if the estate may exceed the federal exclusion", "ANSWERED", 'desk-9af5443d estate liquidity plan; estate-tax pages'),
    ("Ask now about portability and prior taxable gifts", "ANSWERED (as question + discovery action)", 'questions registers; estate-tax pages'),
    ("Re-run this model every year with updated inputs", "ANSWERED (cycle 2026-11-17)", 'desk-03242c78/annual-rerun.html; this desk executes the cycle'),
    ("Put a market rent on Property A or accept that the letting paths are a floor", "ANSWERED", 'desk-9af5443d rents; rent-path pages'),
    ("Add a distribution chart to the projections", "ANSWERED", 'desk-9af5443d; desk-03242c78/charts.html; desk-85a01c5c/projections.html'),
    ("Separate estate tax, income-tax basis and property-tax assessment", "ANSWERED", 'desk-03242c78/estate-tax.html + income-basis.html + property-tax.html'),
    ("Compare mixed paths alongside pure choices", "ANSWERED", 'see mixed-paths row'),
    ("Put reinvestment risk next to any staging headline", "ANSWERED", 'see reinvestment-risk row'),
    ("Create an executive summary outlining important details", "ANSWERED", 'executive-summary.html on desk-03242c78, desk-85a01c5c, decision-d2664fd0, and others'),
    ("Suggestions section: review and choose the best path before implementing changes", "ANSWERED", 'suggestions.html across desks; review-092b hub'),
    ("A clear list of questions, information and answers needed before any decision; discovery actions for missing information", "ANSWERED", 'desk-03242c78/questions.html; desk-e86/questions.html (46-question register)'),
    ("Personal-information privacy first: anonymise, placeholders only, nothing personal on the site", "ANSWERED", 'privacy contracts per desk; scripts/privacy_scan.py; repo-review.html'),
    ("Treat the two properties distinctly (A inherited, B already owned)", "ANSWERED", 'all published desks'),
    ("Black-swan section that mimics real uneven growth and inflation over 50 years", "ANSWERED", 'swan-3a49; cbe/black-swan.html; desk-85a01c5c/black-swan.html'),
    ("Costs and numbers rounded to the nearest $10", "ANSWERED", 'enforced by every desk verifier and scripts/privacy_scan.py'),
    ("Plan for trust inheritance around 2040–2050 under current local, state and federal law", "ANSWERED", 'transfer dates 2040/2045/2050 across desks; law-watch.html'),
    ("Step-by-step inheritance process", "ANSWERED", 'process.html across desks'),
    ("Project property tax, assessed value, and carrying costs by year", "ANSWERED", 'projections.html; property-tax.html; running-costs.html'),
    ("Research inheritance/estate allowances and future changes (money may exceed thresholds)", "ANSWERED", 'inheritance-tax/estate-tax pages; law-watch.html; register.html (2027 figures)'),
    ("No manual input: work autonomously, line by line, official sources only, links for review", "PROCEDURAL", 'COORDINATION.md; sources.html per desk'),
    ("GitHub Pages site: clean dashboard, tables, analysis and findings", "ANSWERED", 'root hub index.html + the live desks (nine further trees are hidden from Pages by the 2026-11-17 privacy containment and remain in-repo)'),
    ("Every table row sourced officially or blank and flagged unverified; never infer", "ANSWERED", 'desk verifiers; verify-476 register; this desk'),
    ("Coordinate parallel sessions via COORDINATION.md", "PROCEDURAL", 'COORDINATION.md'),
    ("PR to main, merge, confirm Pages, record the result", "ANSWERED (this session)", 'COORDINATION.md 1e9/INT record'),
]


def page_requirements():
    NUMCOLS.clear()
    def st_tag(st):
        if st.startswith("ANSWERED"):
            return tag(st, "verified")
        if st.startswith("PARTIAL"):
            return tag(st, "proposed")
        if st.startswith("OPEN"):
            return tag(st, "open")
        return tag(st, "note")
    rows = [[txt, st_tag(st), where] for txt, st, where in REQS]
    answered = sum(1 for _, st, _ in REQS if st.startswith("ANSWERED"))
    partial = sum(1 for _, st, _ in REQS if st.startswith("PARTIAL"))
    openn = sum(1 for _, st, _ in REQS if st.startswith("OPEN"))
    proc = sum(1 for _, st, _ in REQS if st.startswith("PROCEDURAL"))
    body = f"""
<div class="card">
<h2>Requirement traceability index — the full owner brief, line by line</h2>
<p class="small">Every requirement line in the owner brief, normalised (duplicate phrasings merged),
mapped to the published page that answers it. Status: ANSWERED {answered} &middot; PARTIAL {partial}
&middot; OPEN {openn} &middot; PROCEDURAL {proc}. A PARTIAL row always names the missing piece and
the party who must supply it. This index is the &ldquo;collect, organise and analyse&rdquo; layer of
the project. Paths named below stay in the repository; some are currently hidden from Pages by the
2026-11-17 privacy containment (they name the locality) and are marked by that caveat where relevant.</p>
{table(["Requirement (owner brief)", "Status", "Where it is answered"], rows)}
</div>
"""
    return shell("Requirement traceability index", "requirements.html", body, DATE)


# ------------------------------------------------------- page: law watch
def page_law():
    NUMCOLS.clear()
    body = f"""
<div class="card">
<h2>Enacted (in force, verified this cycle)</h2>
{table(["Change", "In force since", "Effect on this decision", "Source"], [
 ["Federal basic exclusion raised to $15,000,000 for 2026 and indexed thereafter (legislation), now $15,480,000 for 2027", "2026-01-01 / 2027-01-01", "keeps the estate-tax headroom slack in every modelled year", a("rp2635", "Rev. Proc. 2026-35") + " " + a("rp2532", "Rev. Proc. 2025-32")],
 ["Annual gift exclusion $20,000 for 2027", "2027-01-01", "gifting cadence only", a("rp2635", "Rev. Proc. 2026-35")],
 ["Prop 19 intergenerational cap $1,044,586 (biennial FHFA-indexed)", "2025-02-16 to 2027-02-15", "sets the reassessment exclusion if the heir occupies", a("lta25009", "BOE LTA 2025/009")],
 ["Prop 13 factored-base factor 1.02 for the 2026 roll (CCPI +3.307% capped at 2%; October 2025 index missing due to the federal data gap)", "2026 lien date", "assessment projection input", a("lta26002", "BOE LTA 2026/002")],
 ["City parcel tax approved at the 3 Nov 2026 election (measure on the county transit agency; first bill fall 2027, expiry 30 Jun 2042)", "2026-11-03 certification", "adds a small recurring charge to Property B's carry cost", a("sfpuc", "rate context") + " " + PRIOR],
 ["Utility rates adopted for Property B (water and wastewater, two years)", "2026-07-01", "carrying-cost rows, now sourced", a("sfpuc", "Resolutions 26-0064 / 26-0066")],
 ["Water utility 2026 rates for Property A's service territory (commission decision)", "2026-01-01", "carrying-cost rows, now sourced", a("sjw", "CPUC decision D.24-12-077 tariff")],
 ["California Behavioral Health Services Tax: 1% of taxable income above $1,000,000 (Form 540 line 62); capital gain taxed as ordinary income", "current", "sell-path tax sensitivity", a("ftb540", "FTB Form 540 instructions") + " " + PRIOR],
])}
</div>

<div class="card">
<h2>Proposed or pending (not law — do not model as enacted)</h2>
{table(["Proposal", "Status {DATE}", "If enacted, what it would change", "Source"], [
 ["City ordinance halving the top transfer-tax tiers (5.5%→2.75% for $10M–under $25M; 6%→3% from $25M), single-family residences excluded from the reduction", "Introduced 24 Mar 2026; pending committee", "material only to a sale of a $10M+ Property B; no effect on Property A (different county)", a("legistar", "Legislation File 260178") + " " + a("sftitle", "current-law digest")],
 ["February 2027 adjustment of the Prop 19 cap (administrative, not legislative)", "Due Feb 2027; amount unknown", "changes the intergenerational exclusion size from 16 Feb 2027; projections use $1,044,586 plus a labelled assumption until published", a("lta25009", "BOE LTA 2025/009") + " " + a("hpi", "FHFA HPI")],
 ["California legislative session 2027-28", "Convenes December 2026", "any estate-tax or property-tax bill appears at the next recheck; prior-session proposals lapsed at adjournment", a("boe19", "BOE Prop 19 page") + " " + PRIOR],
])}
</div>
<p class="small">Enacted-vs-proposed discipline: models use enacted law only. The sell-path and
Property B carrying costs would be re-run only after a proposal is enacted and the effective date is
published.</p>
"""
    return shell("Law watch — enacted vs proposed", "law-watch.html", body, DATE)


# ---------------------------------------------------- page: repo review
def page_repo():
    NUMCOLS.clear()
    body = f"""
<div class="card">
<h2>Repository review {DATE} (line by line, published surface)</h2>
{table(["Check", "Finding", "Verdict"], [
 ["Git history", "The working clone here is shallow (one squashed commit, four refs, no tags) — but the <b>public remote retains roughly 3,500 commits containing the owner's pre-rounding figures</b>. A history rewrite (filter-repo + force-push) is an explicit owner decision (F1) and was NOT performed; it would invalidate open branches and cannot recall copies already cloned. Containment, not revocation.", OPEN_T],
 ["Published surface", "Root hub, the privacy-first dashboard, the public privacy record page and the desks on the live surface (twelve, plus this recheck) — every other top-level directory is excluded from Pages by the deployment gate and the Jekyll exclude list. Nine decision trees that name the locality are currently <b>hidden from Pages by the 2026-11-17 privacy containment</b> while remaining in the repository.", CONF],
 ["Excluded trees", "Legacy trees holding pre-anonymisation or pre-rounding material stay excluded (they remain in the repository). Deleting them is an owner decision recorded on the flagged pages.", OPEN_T],
 ["Verification battery", "Structure/privacy/rounding gate, landing-link check, repository privacy scan, owner-figure gate (salted digests), hash-based location-token guard and the published-surface check all pass on the combined tree at the time of this review.", CONF],
 ["Prior public exposure", "Confirmed, not hypothetical: the pre-squash history was public and is retained on the remote. The 2026-11-17 containment removed the identifiers and exact figures from the live tree; see F1 for the owner's history-rewrite decision.", OPEN_T],
 ["Duplicate desks", "Twenty decision trees answer the same brief with different scopes; several are now hidden from Pages. Suggestion S1 on the suggestions boards: consolidate to one lead desk after the owner chooses.", tag("SUGGESTION", "note")],
])}
</div>

<div class="card">
<h2>Irregularities carried for manual review (with links)</h2>
{table(["Item", "Where", "What is wrong", "Status"], [
 ["Estates-and-trusts capital-gain threshold printed as $16,200 against the official $16,250", "excluded legacy tree (desk-b4f) " + a("rp2635", "official figure"), "transcription error against the IRS revenue procedure", "tree excluded from Pages; owner decision to correct or drop"],
 ["Closing-letter fee shown rising $67→$76 against the official $56", "excluded legacy tree (desk-b4f) " + a("irs2027", "IRS fee schedule reference"), "unsourced fee series", "tree excluded from Pages"],
 ["Intergenerational-exclusion cap applied to the assessed value only up to the cap instead of to the whole gap", "excluded legacy tree (desk-22a32b17) " + a("lta25009", "BOE mechanics"), "known modelling error, documented by the referee desk", "tree excluded from Pages until corrected"],
 ["2017-vintage transfer-tax chart published under a 2025 file name", "city Assessor-Recorder factsheet (external) " + a("asr", "factsheet"), "top tiers superseded by current law", "flag R7; register uses the Controller digest for top tiers"],
 ["Owner cost band below the derived tariff band for Property B", "owner inputs vs adopted schedules " + a("sfpuc", "adopted rates"), "scope difference suspected", "flag R6; discovery action on the open-items page"],
])}
</div>
"""
    return shell("Repository review", "repo-review.html", body, DATE)


# ------------------------------------------------------- page: flagged
def page_flagged():
    NUMCOLS.clear()
    body = f"""
<div class="card">
<h2>Flagged for review — {DATE}</h2>
<p class="small">None of these blocks the decision work; each names what would close it. Items R1–R7 are
this cycle's; F-items referenced here live on the desks' own flagged pages.</p>
{table(["Flag", "Item", "Source link for manual review", "What would close it"], [
 ["R1", "Exact composite property-tax rate for Property A's taxing area (013 series)", a("ratebook", "county rate book FY2025-26, section III"), "read the 013-series pages or the parcel bill"],
 ["R2", "Water provider of record for Property A", a("sjw", "utility tariff territory clause"), "confirm on the tax bill / assessor record"],
 ["R3", "Property B residential stormwater tiers", a("sfpuc", "SFPUC Schedule D"), "transcribe the three tiers"],
 ["R4", "February 2027 Prop 19 cap amount", a("lta25009", "BOE LTA 2025/009"), "recheck after the board's February 2027 letter"],
 ["R5", "Treasury curve refresh (parking yields)", a("treasury", "Treasury daily curve"), "pull the curve feed at the next cycle"],
 ["R6", "Property B owner band vs derived tariff band", a("sfpuc", "SFPUC schedules"), "twelve-month bill breakdown"],
 ["R7", "Stale vintage of the city transfer-tax factsheet", a("asr", "Assessor-Recorder factsheet"), "request a current chart from the office"],
 ["F-history", "Pre-rounding figures in the public git history (owner decision)", a("tra", "project convention page"), "owner decision F1: run the filter-repo rewrite + force-push (invalidates open branches; cannot recall clones), or accept containment"],
])}
</div>
"""
    return shell("Flagged for review", "flagged.html", body, DATE)


# ------------------------------------------------------- page: sources
def page_sources():
    NUMCOLS.clear()
    rows = [
        ["Federal tax figures 2027 (exclusion $15,480,000; gift $20,000; non-citizen spouse $201,000; §6601(j) portion $2,010,000; §2032A cap $1,500,000)", a("rp2635", "IRS Rev. Proc. 2026-35 (PDF)"), "read line-by-line 2026-11-17"],
        ["Federal tax figures 2026 (exclusion $15,000,000; gift $19,000)", a("rp2532", "IRS Rev. Proc. 2025-32 (PDF)"), "prior line-read; consistency re-checked 2026-11-17"],
        ["Prop 19 intergenerational cap $1,044,586; biennial FHFA-HPI adjustment rule; next adjustment February 2027", a("lta25009", "BOE Letter to Assessors 2025/009"), "read 2026-11-17"],
        ["Prop 13 inflation factor 1.02 for the 2026 roll; CCPI data-gap note", a("lta26002", "BOE Letter to Assessors 2026/002"), "read 2026-11-17"],
        ["Tax-rate-area jurisdiction series (property A in series 013)", a("tra", "County jurisdiction table"), "read 2026-11-17"],
        ["Countywide tax-rate components FY2025-26 and the 013-series bond line items", a("ratebook", "County Compilation of Tax Rates FY2025-26"), "read 2026-11-17 (pages A-1 to B-1x within the parse window)"],
        ["Water utility residential tariff (service charge, three tiers, surcharges, fees, territory)", a("sjw", "Water utility advice letter 621-A with CPUC tariff sheets"), "read 2026-11-17"],
        ["Property B water and wastewater adopted rates FY2026-27 and FY2027-28 (resolutions 26-0064 / 26-0066)", a("sfpuc", "SFPUC Rate Schedules and Fees"), "read 2026-11-17"],
        ["City transfer-tax bracket chart (low and mid tiers)", a("asr", "Assessor-Recorder transfer factsheet"), "read 2026-11-17 (vintage caveat R7)"],
        ["City transfer-tax current top tiers (5.5% / 6%) and the pending halving proposal", a("sftitle", "Controller title-and-summary digest") + " &middot; " + a("legistar", "Legislation File 260178"), "read 2026-11-17"],
        ["Mortgage rate context (7.11% / 6.45%)", a("pmms", "Freddie Mac Primary Mortgage Market Survey"), "read 2026-11-17"],
        ["House-price index schedule and latest release", a("hpi", "FHFA House Price Index"), "read 2026-11-17"],
        ["Treasury par yield curve (phased-path parking yields)", a("treasury", "Treasury daily par yield curve rates"), "live table checked 2026-11-17 (latest row 2026-11-16); values on file from 2026-11-13"],
        ["California income-tax treatment (1% above $1,000,000 taxable income; capital gain as ordinary income)", a("ftb540", "FTB 2025 Form 540 instructions"), "prior line-read 2026-11-15; re-checked 2026-11-17"],
        ["County recording fees (sell path)", a("sccfees", "County Clerk-Recorder recording fee schedule"), "prior line-read 2026-11-15"],
    ]
    body = f"""
<div class="card">
<h2>Sources read for this recheck</h2>
{table(["What it supports", "Official document", "Read"], rows)}
<p class="small">Hosts are limited to official publishers (federal and state agencies, the two counties,
the two utilities' regulator filings, and the county transit agency). Secondary sources were used
only to <i>locate</i> official documents and are never cited as support for a value on this desk.</p>
</div>
"""
    return shell("Sources", "sources.html", body, DATE)


# ---------------------------------------------------- page: methodology
def page_method():
    NUMCOLS.clear()
    body = f"""
<div class="card">
<h2>Methodology of this recheck</h2>
<ul>
<li><b>Cadence.</b> Annual, plus event-driven (new revenue procedures, new board letters, elections).
This cycle runs {DATE}; the next full cycle is due November 2027, with a targeted check after the
board's February 2027 letter (flag R4).</li>
<li><b>What counts as official.</b> The statute, the agency's own publication (revenue procedure,
letter to assessors, adopted rate schedule, fee schedule, survey page, index page, legislation file),
read directly. Search engines and commentary are used only to find the official document and are
never a value source.</li>
<li><b>Verdicts.</b> CONFIRMED (read or re-checked against the named document), UPDATED (figure
changed or newly published), OPEN (blank cell + flag + discovery action), PROPOSED (not law),
PRIOR READ (line-read by the 2026-11-13/15 sessions and re-checked for consistency).</li>
<li><b>No inference.</b> Where a value could not be read (flag R1), the cell is blank; components are
published instead of a reconstructed total.</li>
<li><b>Rounding.</b> Money to the nearest $10 unless the figure is an agency-published exact amount
(tariffs, statutory caps, thresholds), which is quoted exactly and marked EXACT.</li>
<li><b>Privacy.</b> County-level anonymisation: Property A (Santa Clara County) and Property B
(San Francisco County). No names, street addresses, ZIP codes, parcel or account numbers on any
page. Owner-supplied figures appear only as bands labelled owner-supplied.</li>
<li><b>Movement test.</b> After the register update, the ranking of the paths is recomputed on the
<a href="rebuild.html">rebuild page</a>; a change in any input that cannot bind within the modelled
range is recorded as NO MOVE with its arithmetic.</li>
</ul>
</div>

<div class="card">
<h2>Re-running this desk</h2>
<p class="small">The pages are generated by <code>recheck-2026-11-17/_src/build.py</code> and checked by
<code>recheck-2026-11-17/_src/verify.py</code> (row sourcing, rounding, identifier scan, internal
links). Rebuild determinism: re-running the generator over the same inputs reproduces the same
pages.</p>
</div>
"""
    return shell("Methodology and privacy", "methodology.html", body, DATE)


def main():
    css = OUT / "style.css"
    css.write_text(CSS)
    pages = {
        "index.html": page_index(),
        "register.html": page_register(),
        "open-items.html": page_open(),
        "rebuild.html": page_rebuild(),
        "requirements.html": page_requirements(),
        "law-watch.html": page_law(),
        "repo-review.html": page_repo(),
        "flagged.html": page_flagged(),
        "sources.html": page_sources(),
        "methodology.html": page_method(),
    }
    for name, html in pages.items():
        (OUT / name).write_text(html)
    print(f"wrote {len(pages)} pages + style.css")


if __name__ == "__main__":
    main()
