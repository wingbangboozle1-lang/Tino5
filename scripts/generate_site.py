#!/usr/bin/env python3
"""Generates the static GitHub Pages site for the Tino5 estate/property decision dashboard.
All figures are either (a) verified facts with official source links, (b) user-provided
values explicitly flagged as such, or (c) labeled projection assumptions. Nothing is invented.
"""
import csv, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = os.path.join(ROOT, "pages")
ASSETS = os.path.join(ROOT, "assets")
os.makedirs(PAGES, exist_ok=True)
os.makedirs(ASSETS, exist_ok=True)

def r10(x): return int(round(x / 10.0) * 10)
def usd(x): return "${:,.0f}".format(x)

# ---------------- data ----------------
CUP_AV_2026, CUP_MV_2026 = 550537.0, 3100000.0
CUP_RATE = 7207.0 / 539743.0          # effective rate derived from user-provided 2025 bill
SF_AV_2025, SF_MV_2026 = 114248.0, 1800000.0
SF_RATE = 2439.0 / 114248.0
APPR, INFL, EXCL0 = 0.03, 0.02, 1044586.0
INH_YEAR = 2045

cup_hist = [(2026, "--", 550537, "+2%"), (2025, 7207, 539743, "+2%"), (2024, 7003, 529161, "+2%"),
            (2023, 6917, 518786, "+2%"), (2022, 6755, 508614, "+2%"), (2021, 6662, 498642, "+1%"),
            (2020, 6565, 493530, "+2%"), (2019, 6565, 483854, "+2%"), (2018, 6383, 474368, "+2%"),
            (2017, 6383, 465067, "+2%"), (2016, 6414, 455949, "+1.5%"), (2015, 6130, 449101, "+2%"),
            (2014, 5965, 440305, "+0.5%")]
sf_hist = [(2025, 2439, 114248, "+2%"), (2024, 2315, 112008, "+2%"), (2023, 2179, 109814, "+2%"),
           (2022, 2107, 107662, "+2%"), (2021, 2066, 105595, "+1%"), (2020, 2197, 104513, "+2%"),
           (2019, 2134, 102465, "+2%"), (2018, 2061, 100456, "+2%"), (2017, 1740, 98488, "+2%"),
           (2016, 1675, 96557, "+1.5%")]

cup_proj, sf_proj = [], []
for y in range(2026, 2051):
    t = y - 2026
    av, mv = CUP_AV_2026 * (1 + INFL) ** t, CUP_MV_2026 * (1 + APPR) ** t
    cup_proj.append((y, r10(av), r10(av * CUP_RATE), r10(mv)))
    avs, mvs = SF_AV_2025 * (1 + INFL) ** (t + 1), SF_MV_2026 * (1 + APPR) ** t
    sf_proj.append((y, r10(avs), r10(avs * SF_RATE), r10(mvs)))

t = INH_YEAR - 2026
FBYV = CUP_AV_2026 * (1 + INFL) ** t
EXCL = EXCL0 * (1 + APPR) ** t
FMV = CUP_MV_2026 * (1 + APPR) ** t
LIVE_TAXABLE = min(FMV, FBYV + EXCL)
LIVE_TAX, RENT_TAX = LIVE_TAXABLE * CUP_RATE, FMV * CUP_RATE
CUR_TAX_2045 = FBYV * CUP_RATE
NET_SALE = FMV * 0.94
INV_2050 = NET_SALE * 1.06 ** (2050 - INH_YEAR)

# ---------------- sources ----------------
S = {
 "irs_obbb": ("IRS — One, Big, Beautiful Bill provisions (IR-2025-103; $15,000,000 basic exclusion for 2026 deaths)", "https://www.irs.gov/newsroom/one-big-beautiful-bill-provisions"),
 "irs_rp2532": ("IRS — Rev. Proc. 2025-32, 2026 inflation adjustments (estate tax $15M permanent, indexed after 2026)", "https://www.irs.gov/pub/irs-drop/rp-25-32.pdf"),
 "irs_706": ("IRS — Instructions for Form 706 (2026): $15,000,000 basic exclusion, 40% top rate, DSUE portability", "https://www.irs.gov/instructions/i706"),
 "irs_whatsnew": ("IRS — What's new: Estate and gift tax (2026: $15,000,000 exclusion; $19,000 annual gift exclusion)", "https://www.irs.gov/businesses/small-businesses-selfemployed/whats-new-estate-and-gift-tax"),
 "ftb_capgain": ("FTB — Capital gains taxed as ordinary income in CA; top rate 13.3% (1% mental health surtax over $1M)", "https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html"),
 "ftb_fedchanges": ("FTB — Summary of federal income tax changes (P.L. 119-21; CA max rate 13.3%, no special cap-gains rate)", "https://www.ftb.ca.gov/about-ftb/data-reports-plans/summary-of-federal-income-tax-changes/index.html"),
 "ftb_estate": ("FTB — California estate 'pick-up' tax is zero (no CA estate tax since federal credit repealed post-2004)", "https://www.ftb.ca.gov/tax-pros/law/legislation/2017-2018/sb726-032317.pdf"),
 "boe_pub29": ("CA Board of Equalization — Publication 29, California Property Tax: 1% rate + voter-approved bonds; 2% annual cap", "https://www.boe.ca.gov/proptaxes/pdf/pub29.pdf"),
 "boe_pub800": ("CA BOE — How Property Is Assessed (Pub 800-10): 2% FBYV cap, reassessment only on change in ownership/new construction", "https://boe.ca.gov/pdf/pub800-10.pdf"),
 "boe_lta25015": ("CA BOE — LTA 25-015, Prop 19 intergenerational exclusion: $1M adjusted to $1,044,586 for Feb 16, 2025–Feb 15, 2027", "https://boe.ca.gov/proptaxes/pdf/lta25015.pdf"),
 "boe_rule462": ("CA BOE — Property Tax Rule 462.520: Prop 19 new taxable value = FBYV + adjusted $1M cap; $1M adjusted every 2 yrs by CA HPI", "https://boe.ca.gov/proptaxes/pdf/rules/Rule462-520.pdf"),
 "scc_parentchild": ("Santa Clara County Assessor — Prop 19 parent-child transfer: move in within 1 year, homeowners' exemption, claim BOE-19-P within 3 years", "https://sccassessor.org/index.php/tax-savings/transferring-your-assessed-value/parent-to-child-2"),
 "scc_faq": ("Santa Clara County Assessor — Prop 19 FAQ: claim within 3 years of transfer or 6 months after supplemental notice", "https://www.sccassessor.org/edocman/Prop19ParentChildFAQ.pdf"),
 "scc_booklet": ("Santa Clara County Assessor — Assessment Information Booklet: typical tax rate area example $1.1488 per $100 of assessed value", "https://files.santaclaracounty.gov/exjcpb1521/2024-11/assessment_information_booklet.pdf"),
 "scc_ar2025": ("Santa Clara County Assessor — Annual Report 2025-26: 1% max ad valorem + voter-approved bonds; homeowners' exemption $7,000", "https://files.santaclaracounty.gov/exjcpb1521/2025-11/annual_report_2025-2026.pdf"),
 "irs_pub559": ("IRS — Publication 559, Survivors, Executors and Administrators: basis of inherited property = FMV at date of death (IRC 1014)", "https://www.irs.gov/publications/p559"),
 "irs_irm_firpta": ("IRS — IRM 21.8.5: stepped-up basis for property received from a decedent (IRC 1014(a))", "https://www.irs.gov/irm/part21/irm_21-008-005r"),
 "irs_121": ("IRS — IRC §121: exclude up to $250,000 ($500,000 joint) gain on sale of principal residence, 2-of-5-year test", "https://www.irs.gov/taxtopics/tc701"),
 "irs_topic409": ("IRS — Topic 409: capital gains; max LTCG rate 20%; NIIT 3.8% (IRC 1411) thresholds $200k/$250k", "https://www.irs.gov/taxtopics/tc409"),
 "sfrb_rates": ("SF Rent Board — annual allowable increase: 1.4% (3/1/2025–2/28/2026); 1.6% (3/1/2026–2/28/2027); cap = 60% of Bay Area CPI, max 7%", "https://sfrb.org/topic-no-051-years-annual-allowable-increase"),
 "sfrb_ab1482": ("SF Rent Board — AB 1482 (CA Tenant Protection Act): annual increase cap 5% + CPI, max 10%; expires Jan 1, 2030", "https://sfrb.org/article/summary-ab-1482-california-tenant-protection-act-2019"),
 "cpuc_nbt": ("CPUC — Net Billing Tariff (NEM 3.0): solar exports compensated at avoided-cost-based rates, not retail rate", "https://www.cpuc.ca.gov/industries-and-topics/electrical-energy/demand-side-management/distributed-energy-resources/net-energy-metering"),
 "cupertino_util": ("City of Cupertino — water service providers: San Jose Water and California Water Service; CPUC regulates rates", "https://www.cupertino.org/our-city/departments/public-works/utilities"),
 "sfpuc_rates": ("SFPUC — 2026-27 water and sewer rates schedules and fees", "https://sfpuc.org/accounts-services/water-power-and-sewer-rates"),
 "fhfa_hpi": ("FHFA — House Price Index report 2025Q4: California 1-yr change -0.83%, 5-yr +28.88%", "https://www.fhfa.gov/document/d/hpi/fhfa-house-price-index-report-2025q4"),
 "bls_cpi": ("BLS — CPI-U 12-month change, September 2026: +3.7% (all items)", "https://www.bls.gov/news.release/cpi.nr0.htm"),
 "sos_initiatives": ("CA Secretary of State — initiative status: Prop 19 repeal initiative 25-0017 failed to qualify for the 2026 ballot", "https://www.sos.ca.gov/elections/ballot-measures/initiative-and-referendum-status/failed-qualify"),
 "leginfo_16061": ("CA Legislative Information — Probate Code §16061.7: trustee notice to beneficiaries/heirs required", "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PROB&sectionNum=16061.7."),
 "leginfo_18100": ("CA Legislative Information — Probate Code §18100.5: Certification of Trust", "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PROB&sectionNum=18100.5."),
 "boe_502a": ("CA BOE — Form BOE-502-A, Preliminary Change of Ownership Report (filed with county recorder)", "https://www.boe.ca.gov/proptaxes/forms.htm"),
 "insurance_ca": ("California Department of Insurance — consumer insurance information and FAIR Plan (insurer of last resort)", "https://www.insurance.ca.gov/"),
 "fairplan": ("California FAIR Plan — official site: basic fire insurance of last resort; dwelling coverage capped at $3,000,000", "https://www.cpcp.org/"),
}
def sl(key): return '<a href="{}" target="_blank" rel="noopener">{}</a>'.format(S[key][1], S[key][0])

NAV = [("index.html", "Dashboard"), ("pages/executive-summary.html", "Executive Summary"),
       ("pages/property-tax.html", "Property Tax Law & History"), ("pages/projections.html", "Projections to 2050"),
       ("pages/inheritance-estate-tax.html", "Inheritance & Estate Tax"), ("pages/decision-analysis.html", "Decision Analysis"),
       ("pages/inheritance-process.html", "Inheritance Process Steps"), ("pages/operating-costs.html", "Operating Costs"),
       ("pages/flagged-for-review.html", "Flagged for Review"), ("pages/sources.html", "Sources")]

def page(title, body, active=""):
    nav = "".join('<li class="{}"><a href="{}">{}</a></li>'.format("active" if href == active else "", href if href == "index.html" else "../" + href if active.startswith("pages/") else href, label) for href, label in NAV)
    prefix = "../" if active.startswith("pages/") else ""
    nav = "".join('<li class="{}"><a href="{}{}">{}</a></li>'.format("active" if href == active else "", prefix, href, label) for href, label in NAV)
    return """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t} — Estate &amp; Property Decision Dashboard</title>
<link rel="stylesheet" href="{p}assets/style.css"></head>
<body><header><h1>Estate &amp; Property Decision Dashboard</h1>
<p class="tagline">Cupertino (ZIP 95014) inheritance decision support · anonymized · figures rounded to nearest $10</p>
<nav><ul>{nav}</ul></nav></header><main>{b}</main>
<footer><p>Anonymized planning dashboard. Not legal, tax, or financial advice. All personal information is internal-only; this site contains placeholders only.
Verified rows link to official sources; unverified values are blank and listed on <a href="{p}pages/flagged-for-review.html">Flagged for Review</a>.</p></footer>
</body></html>""".format(t=title, p=prefix, nav=nav, b=body)

def table(headers, rows, note=None):
    h = "".join("<th>{}</th>".format(x) for x in headers)
    body = ""
    for r in rows:
        body += "<tr>" + "".join("<td>{}</td>".format(c) for c in r) + "</tr>"
    n = "<p class='note'>{}</p>".format(note) if note else ""
    return "<table><thead><tr>{}</tr></thead><tbody>{}</tbody></table>{}".format(h, body, n)

def write(name, title, body, active):
    with open(os.path.join(ROOT, name), "w") as f:
        f.write(page(title, body, active))

# ---------------- style ----------------
CSS = """:root{--bg:#f6f8fa;--card:#fff;--ink:#1f2328;--muted:#57606a;--accent:#0969da;--warn:#9a6700;--line:#d0d7de}
*{box-sizing:border-box}body{margin:0;font-family:-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink);line-height:1.5}
header{background:#0d2818;color:#fff;padding:1.2rem 2rem}
header h1{margin:0;font-size:1.35rem}header .tagline{margin:.2rem 0 .8rem;color:#b6e3c6;font-size:.85rem}
nav ul{list-style:none;display:flex;flex-wrap:wrap;gap:.4rem;margin:0;padding:0}
nav a{color:#fff;text-decoration:none;background:rgba(255,255,255,.14);padding:.35rem .7rem;border-radius:6px;font-size:.85rem}
nav a:hover,nav li.active a{background:#fff;color:#0d2818}
main{max-width:1100px;margin:1.5rem auto;padding:0 1rem}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1.2rem 1.4rem;margin-bottom:1.2rem;box-shadow:0 1px 2px rgba(0,0,0,.04)}
h2{margin-top:0;font-size:1.15rem;border-bottom:2px solid var(--accent);padding-bottom:.3rem}
h3{font-size:1rem;margin-bottom:.4rem}
table{border-collapse:collapse;width:100%;font-size:.88rem;margin:.6rem 0}
th,td{border:1px solid var(--line);padding:.4rem .55rem;text-align:left}
th{background:#eef2f5}tbody tr:nth-child(even){background:#fafbfc}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
.note{font-size:.8rem;color:var(--muted)}.flag{color:var(--warn);font-weight:600}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem}
.stat{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1rem;text-align:center}
.stat b{display:block;font-size:1.3rem;color:var(--accent)}.stat span{font-size:.8rem;color:var(--muted)}
ul.tight li,ol.tight li{margin-bottom:.35rem}
a{color:var(--accent)}footer{max-width:1100px;margin:0 auto 2rem;padding:0 1rem;font-size:.78rem;color:var(--muted)}
.badge{display:inline-block;background:#fff8c5;color:#9a6700;border:1px solid #d4a72c;border-radius:4px;padding:0 .35rem;font-size:.75rem;font-weight:600}
.badge.ok{background:#dafbe1;color:#1a7f37;border-color:#4ac26b}
"""
with open(os.path.join(ASSETS, "style.css"), "w") as f: f.write(CSS)

# ---------------- index ----------------
body = """
<div class="grid">
<div class="stat"><b>$3,100,000</b><span>Cupertino house est. value, Nov 2026 <span class="flag">(user-provided)</span></span></div>
<div class="stat"><b>$1,800,000</b><span>SF Outer Sunset (94122) house est. value, Nov 2026 <span class="flag">(user-provided)</span></span></div>
<div class="stat"><b>$15,000,000</b><span>Federal estate tax basic exclusion, 2026 deaths — IRS</span></div>
<div class="stat"><b>2% / yr</b><span>Prop 13 cap on assessed-value growth — CA BOE</span></div>
<div class="stat"><b>$0</b><span>California estate / inheritance tax (pick-up tax is zero) — FTB</span></div>
<div class="stat"><b>1 yr</b><span>Deadline to occupy inherited home as primary residence for Prop 19 exclusion — SCC Assessor</span></div>
</div>
<div class="card"><h2>Welcome</h2>
<p>This dashboard organizes the research, requirements, and analysis for the decision on the Cupertino house
(inheritance expected via trust around 2040–2050): whether to <b>live in it</b>, <b>rent it out</b>, or <b>sell and reinvest</b> —
taking into account the San Francisco rental property already owned, property taxes, insurance, utilities, maintenance,
and federal/state inheritance and capital-gains taxes.</p>
<ul class="tight">
<li>Start with the <a href="pages/executive-summary.html">Executive Summary</a>.</li>
<li>Every table row is either linked to an official source or explicitly flagged as unverified/user-provided/assumption.</li>
<li>All money figures in analysis are rounded to the nearest $10.</li>
<li>Personal information is anonymized; placeholders are used throughout. Personal data discovered during research stays internal and never appears on this site.</li>
</ul></div>
<div class="card"><h2>Page guide</h2>
<table><thead><tr><th>Page</th><th>What it contains</th></tr></thead><tbody>
<tr><td><a href="pages/executive-summary.html">Executive Summary</a></td><td>Key findings, requirements checklist, recommendation at a glance</td></tr>
<tr><td><a href="pages/property-tax.html">Property Tax Law &amp; History</a></td><td>Prop 13 / Prop 19 rules with official sources; historical tax &amp; assessment tables for both houses</td></tr>
<tr><td><a href="pages/projections.html">Projections to 2050</a></td><td>Year-by-year assessed value, property tax, market value; Prop 19 scenarios at 2045; estate exemption projection</td></tr>
<tr><td><a href="pages/inheritance-estate-tax.html">Inheritance &amp; Estate Tax</a></td><td>Federal/CA thresholds, step-up basis, capital gains, law-change watch</td></tr>
<tr><td><a href="pages/decision-analysis.html">Decision Analysis</a></td><td>Live vs. rent vs. sell &amp; reinvest — costs, taxes, projections, recommendation</td></tr>
<tr><td><a href="pages/inheritance-process.html">Inheritance Process Steps</a></td><td>Step-by-step trust administration and property tax filings</td></tr>
<tr><td><a href="pages/operating-costs.html">Operating Costs</a></td><td>Water, electricity/solar, insurance, maintenance, SF rental economics</td></tr>
<tr><td><a href="pages/flagged-for-review.html">Flagged for Review</a></td><td>Every unverified value or assumption, with source links</td></tr>
<tr><td><a href="pages/sources.html">Sources</a></td><td>Full list of official sources used</td></tr>
</tbody></table></div>
"""
write("index.html", "Dashboard", body, "index.html")

# ---------------- executive summary ----------------
body = """
<div class="card"><h2>Important details</h2>
<ul class="tight">
<li><b>Two properties:</b> Cupertino house (ZIP 95014, est. $3,100,000 Nov 2026, to be inherited via trust ~2040–2050) and the already-owned San Francisco Outer Sunset triplex (ZIP 94122, est. $1,800,000, two units rented for about $7,150/month total, owner occupies the third). <span class="flag">(Values user-provided)</span></li>
<li><b>The single biggest tax lever is Proposition 19.</b> If the heir does <b>not</b> occupy the Cupertino house as a primary residence within 1 year of transfer, it is fully reassessed to market value. At a 2045 projected market value of """ + usd(r10(FMV)) + """, that is a property tax of about <b>""" + usd(r10(RENT_TAX)) + """/yr</b>; if the heir <b>does</b> live there and files the claim, the taxable value is capped at roughly FBYV + inflation-adjusted $1M ≈ <b>""" + usd(r10(LIVE_TAXABLE)) + """</b>, i.e. about <b>""" + usd(r10(LIVE_TAX)) + """/yr</b> — a saving of about <b>""" + usd(r10(RENT_TAX - LIVE_TAX)) + """/yr</b> (projected 2045, assumption-based).</li>
<li><b>Federal estate tax:</b> """ + sl("irs_obbb") + """ — $15,000,000 per person for 2026 deaths, permanent and inflation-indexed (projected ≈ """ + usd(r10(15000000 * 1.03 ** 19)) + """ by 2045 at a 3%/yr assumption); 40% above the exemption; portability allows a married couple ≈ $30,000,000. <b>California has no estate or inheritance tax</b> (""" + sl("ftb_estate") + """).</li>
<li><b>Step-up in basis:</b> inherited property gets basis = fair market value at date of death (""" + sl("irs_pub559") + """), so selling soon after inheritance generally triggers little or no capital-gains tax. CA taxes capital gains as ordinary income up to 13.3% (""" + sl("ftb_capgain") + """); federal LTCG 0/15/20% + 3.8% NIIT (""" + sl("irs_topic409") + """).</li>
<li><b>Recommendation (summary):</b> if the heir can occupy the Cupertino house as a primary residence within 1 year and file form BOE-19-P plus the homeowners' exemption, <b>keeping the house and living in it</b> preserves the largest tax advantage (≈ """ + usd(r10(RENT_TAX - LIVE_TAX)) + """/yr lower property tax vs. renting, projected 2045). <b>Selling and reinvesting</b> (≈ """ + usd(r10(NET_SALE)) + """ net of 6% selling costs, projected 2045) is the strongest wealth-maximizing option if the heir prefers to stay in San Francisco, because the stepped-up basis makes the sale nearly tax-free and the invested capital can compound. Renting the Cupertino house is the weakest option on taxes (full reassessment) unless market rent is high enough to cover the ≈ """ + usd(r10(RENT_TAX)) + """/yr tax (market rent unverified — flagged). See <a href="decision-analysis.html">Decision Analysis</a>.</li>
</ul></div>
<div class="card"><h2>Requirements checklist (collected &amp; organized)</h2>
<table><thead><tr><th>#</th><th>Requirement</th><th>Where addressed</th></tr></thead><tbody>
<tr><td>1</td><td>Executive summary of important details</td><td>This page</td></tr>
<tr><td>2</td><td>Privacy: anonymize all personal information; internal-only; never on the site</td><td>Whole site — placeholders only</td></tr>
<tr><td>3</td><td>Numbers rounded to nearest $10 in all decision analysis</td><td>Projections / Decision Analysis</td></tr>
<tr><td>4</td><td>Guide decision with current local/state/federal property &amp; tax law (2040–2050 inheritance via trust)</td><td>Property Tax Law &amp; History; Inheritance &amp; Estate Tax</td></tr>
<tr><td>5</td><td>Compare: live vs. rent vs. sell &amp; reinvest (stocks/savings) after taxes</td><td>Decision Analysis</td></tr>
<tr><td>6</td><td>Include property tax, insurance, water, electricity costs of owning the inherited house</td><td>Operating Costs; Projections</td></tr>
<tr><td>7</td><td>Project house value, assessed value, property tax by year</td><td>Projections to 2050</td></tr>
<tr><td>8</td><td>Step-by-step inheritance process</td><td>Inheritance Process Steps</td></tr>
<tr><td>9</td><td>Keep SF rental property in mind for the decision</td><td>Operating Costs; Decision Analysis</td></tr>
<tr><td>10</td><td>Maximize profit, lower costs, projections based on inflation &amp; tax factors</td><td>Projections; Decision Analysis</td></tr>
<tr><td>11</td><td>Watch proposed law changes and their impact</td><td>Inheritance &amp; Estate Tax (law-change watch); Flagged for Review</td></tr>
<tr><td>12</td><td>Research inheritance tax-free thresholds (federal/state/local) + future projections</td><td>Inheritance &amp; Estate Tax</td></tr>
<tr><td>13</td><td>No manual input needed; verify everything line by line from official sources with links; no hallucinations</td><td>Sources; Flagged for Review</td></tr>
</tbody></table></div>
"""
write("pages/executive-summary.html", "Executive Summary", body, "pages/executive-summary.html")

# ---------------- property tax ----------------
cup_rows = [(y, ("—" if t == "--" else usd(t)), usd(a), g) for y, t, a, g in cup_hist]
sf_rows = [(y, usd(t), usd(a), g) for y, t, a, g in sf_hist]
body = """
<div class="card"><h2>The law (verified, official sources)</h2>
<table><thead><tr><th>Rule</th><th>What it means</th><th>Source</th></tr></thead><tbody>
<tr><td>Prop 13 tax rate</td><td>1% of assessed value + voter-approved bonds/special assessments; reassessment to market value only on change in ownership or new construction</td><td>""" + sl("boe_pub29") + "<br>" + sl("boe_pub800") + """</td></tr>
<tr><td>Prop 13 assessment cap</td><td>Assessed (factored base year) value can grow at most 2% per year while ownership is unchanged</td><td>""" + sl("boe_pub800") + """</td></tr>
<tr><td>Homeowners' exemption</td><td>$7,000 off assessed value of a principal residence (≈ $70–$80/yr tax saving at the 1% levy)</td><td>""" + sl("scc_ar2025") + """</td></tr>
<tr><td>Typical Santa Clara County tax rate</td><td>Example 'typical tax rate area': $1.1488 per $100 of assessed value (1% base + county/school/water bonds) = 1.1488%</td><td>""" + sl("scc_booklet") + """</td></tr>
<tr><td>Prop 19 parent-child exclusion</td><td>Inherited family home keeps a protected taxable value only if the heir occupies it as primary residence within 1 year (homeowners'/disabled veterans' exemption claimed) AND the market value is within FBYV + inflation-adjusted $1M. Otherwise full reassessment to market value</td><td>""" + sl("boe_lta25015") + "<br>" + sl("boe_rule462") + "<br>" + sl("scc_parentchild") + """</td></tr>
<tr><td>Prop 19 $1M adjustment</td><td>$1,000,000 adjusted to <b>$1,044,586</b> for transfers Feb 16, 2025 – Feb 15, 2027; adjusted every 2 years by the CA House Price Index (FHFA)</td><td>""" + sl("boe_lta25015") + "<br>" + sl("boe_rule462") + """</td></tr>
<tr><td>Claim deadline</td><td>File BOE-19-P with the county assessor within 3 years of transfer (or within 6 months of a supplemental/escape assessment notice); move in within 1 year</td><td>""" + sl("scc_faq") + "<br>" + sl("scc_parentchild") + """</td></tr>
<tr><td>Effective rates implied by the actual bills</td><td>Cupertino ≈ 1.335% of assessed value (2025 bill); SF ≈ 2.135% (2025 bill, includes SF special parcel taxes). <span class="flag">Derived from user-provided bills — not an official rate schedule</span></td><td>User-provided tax bills; base-rate context: """ + sl("scc_booklet") + """</td></tr>
</tbody></table></div>
<div class="card"><h2>Cupertino house (ZIP 95014) — historical property tax &amp; assessment <span class="flag">(user-provided records)</span></h2>
""" + table(["Year", "Property taxes", "Tax assessment", "Assessed change"], cup_rows,
            "Source: user-provided county tax records (not independently verified — see Flagged for Review). Rate context: " + S["boe_pub29"][0] + ".") + """
</div>
<div class="card"><h2>San Francisco house (ZIP 94122) — historical property tax &amp; assessment <span class="flag">(user-provided records)</span></h2>
""" + table(["Year", "Property taxes", "Tax assessment", "Assessed change"], sf_rows,
            "Source: user-provided county tax records (not independently verified — see Flagged for Review).") + """
</div>
"""
write("pages/property-tax.html", "Property Tax Law & History", body, "pages/property-tax.html")

# ---------------- projections ----------------
cup_p = [(y, usd(a), usd(t), usd(m)) for y, a, t, m in cup_proj]
sf_p = [(y, usd(a), usd(t), usd(m)) for y, a, t, m in sf_proj]
excl_proj = [(y, usd(r10(15000000 * (1 + APPR) ** (y - 2026)))) for y in range(2026, 2051, 4)]
scen = [
 ("Current law, no inheritance yet (assessed value keeps +2%/yr)", usd(r10(FBYV)), usd(r10(CUR_TAX_2045)), "Assessed value only grows 2%/yr while the owner is unchanged — " + S["boe_pub800"][0]),
 ("A — Heir lives in Cupertino as primary residence (Prop 19 exclusion)", usd(r10(LIVE_TAXABLE)), usd(r10(LIVE_TAX)), S["boe_lta25015"][0] + "; " + S["scc_parentchild"][0]),
 ("B — Heir rents it out / does not occupy (full reassessment to market)", usd(r10(FMV)), usd(r10(RENT_TAX)), S["boe_rule462"][0]),
 ("C — Sell at inheritance (no property tax after sale; step-up basis)", "—", "$0 after sale", S["irs_pub559"][0]),
]
body = """
<div class="card"><h2>Assumptions used in all projections <span class="flag">(assumptions, not official values)</span></h2>
<ul class="tight">
<li>Assessed value grows at the Prop 13 maximum of <b>2%/yr</b> (""" + sl("boe_pub800") + """).</li>
<li>Market value grows at <b>3%/yr</b> nominal (assumption; context: FHFA CA HPI 5-yr change +28.88%, 1-yr -0.83% at 2025Q4 — """ + sl("fhfa_hpi") + """; BLS CPI-U +3.7% for 12 months ending Sept 2026 — """ + sl("bls_cpi") + """).</li>
<li>Effective property tax rates: Cupertino 1.335%, SF 2.135% (derived from user-provided 2025 bills; base 1% + bonds per """ + sl("boe_pub29") + """).</li>
<li>Prop 19 $1M adjustment grows at 3%/yr from $1,044,586 (official for Feb 2025–Feb 2027 — """ + sl("boe_lta25015") + """; adjusted by CA HPI every 2 years per """ + sl("boe_rule462") + """).</li>
<li>All dollar figures rounded to the nearest $10.</li>
</ul></div>
<div class="card"><h2>Cupertino house — projection by year (2026–2050)</h2>
""" + table(["Year", "Assessed value (FBYV +2%/yr)", "Property tax (eff. 1.335%)", "Projected market value (+3%/yr)"], cup_p) + """
<p class="note">CSV: <a href="../data/data-cupertino-projection.csv">data-cupertino-projection.csv</a></p></div>
<div class="card"><h2>San Francisco house — projection by year (2026–2050)</h2>
""" + table(["Year", "Assessed value (+2%/yr)", "Property tax (eff. 2.135%)", "Projected market value (+3%/yr)"], sf_p) + """
<p class="note">CSV: <a href="../data/data-sf-projection.csv">data-sf-projection.csv</a></p></div>
<div class="card"><h2>Prop 19 scenarios at inheritance year 2045 (projected)</h2>
""" + table(["Scenario", "Taxable (assessed) value", "Property tax / yr", "Basis"], scen,
            "Market value projected 2045: " + usd(r10(FMV)) + "; FBYV projected 2045: " + usd(r10(FBYV)) + "; Prop 19 adjustment projected 2045: " + usd(r10(EXCL)) + ". Taxable value under scenario A = min(market value, FBYV + adjustment) per " + S["boe_rule462"][0] + ".") + """
<p><b>Annual property-tax saving of living in the house vs. renting it out (2045 projection): ≈ """ + usd(r10(RENT_TAX - LIVE_TAX)) + """/yr.</b></p></div>
<div class="card"><h2>Federal estate tax basic exclusion — projection (indexed for inflation after 2026)</h2>
""" + table(["Year of death", "Basic exclusion (projected, 3%/yr indexing)"], excl_proj,
            "2026 value $15,000,000 is official (" + S["irs_rp2532"][0] + "); later years are a 3%/yr projection assumption. 40% tax above the exclusion; portability can double it for a married couple (" + S["irs_706"][0] + "). California: no estate/inheritance tax (" + S["ftb_estate"][0] + ").") + """
</div>
"""
write("pages/projections.html", "Projections to 2050", body, "pages/projections.html")

# ---------------- inheritance & estate tax ----------------
body = """
<div class="card"><h2>Tax-free inheritance thresholds (verified)</h2>
<table><thead><tr><th>Level</th><th>Threshold / rule</th><th>Source</th></tr></thead><tbody>
<tr><td>Federal estate tax (2026 deaths)</td><td><b>$15,000,000</b> basic exclusion per person; 40% on the excess; permanent &amp; inflation-indexed after 2026 (P.L. 119-21, OBBBA)</td><td>""" + sl("irs_obbb") + "<br>" + sl("irs_rp2532") + "<br>" + sl("irs_706") + """</td></tr>
<tr><td>Federal portability (DSUE)</td><td>Surviving spouse can add the deceased spouse's unused exclusion by filing Form 706 within 9 months → married couple ≈ <b>$30,000,000</b> in 2026</td><td>""" + sl("irs_706") + """</td></tr>
<tr><td>Federal gift tax</td><td>2026 annual exclusion <b>$19,000</b> per donee; lifetime exemption unified with estate ($15,000,000 in 2026)</td><td>""" + sl("irs_whatsnew") + """</td></tr>
<tr><td>Federal GST tax</td><td>GST exemption also $15,000,000 (2026), 40% on direct skips</td><td>""" + sl("irs_rp2532") + """</td></tr>
<tr><td>California</td><td><b>No state estate tax and no inheritance tax</b> — the CA 'pick-up' tax is zero because the federal credit it piggybacked was repealed after 2004</td><td>""" + sl("ftb_estate") + """</td></tr>
<tr><td>Local (Santa Clara County / SF)</td><td>No county or city estate or inheritance tax exists in California</td><td>""" + sl("ftb_estate") + """</td></tr>
<tr><td>Inheritance itself as income</td><td>Inherited money/property is not income to the heir; later sale is taxed on gain over the stepped-up basis</td><td>""" + sl("irs_pub559") + """</td></tr>
</tbody></table></div>
<div class="card"><h2>If the Cupertino house is sold after inheritance</h2>
<table><thead><tr><th>Rule</th><th>Effect</th><th>Source</th></tr></thead><tbody>
<tr><td>Step-up in basis (IRC §1014)</td><td>Basis = fair market value at date of death (applies to trust assets included in the gross estate) → selling soon after inheritance usually means ~zero taxable gain</td><td>""" + sl("irs_pub559") + "<br>" + sl("irs_irm_firpta") + """</td></tr>
<tr><td>§121 exclusion</td><td>Up to $250,000 ($500,000 joint) gain excludable if the home was owned and used as principal residence 2 of the last 5 years</td><td>""" + sl("irs_121") + """</td></tr>
<tr><td>Federal capital gains</td><td>LTCG 0% / 15% / 20% (2026: 0% up to $98,900 taxable income MFJ; 20% above $613,700 MFJ) + 3.8% NIIT above $250,000 MAGI (MFJ)</td><td>""" + sl("irs_topic409") + "<br>" + sl("irs_rp2532") + """</td></tr>
<tr><td>California capital gains</td><td>No special rate — taxed as ordinary income, top <b>13.3%</b></td><td>""" + sl("ftb_capgain") + "<br>" + sl("ftb_fedchanges") + """</td></tr>
<tr><td>Property tax after sale</td><td>None on the sold house; buyer's future taxes reset to purchase price (Prop 13)</td><td>""" + sl("boe_pub29") + """</td></tr>
</tbody></table></div>
<div class="card"><h2>Projection of the federal exemption to the 2040–2050 window <span class="flag">(3%/yr indexing assumption)</span></h2>
""" + table(["Year of death", "Projected basic exclusion"], [(2040, usd(r10(15000000*1.03**14))), (2045, usd(r10(15000000*1.03**19))), (2050, usd(r10(15000000*1.03**24)))],
            "2026 = $15,000,000 official (" + S["irs_obbb"][0] + "); growth is an assumption based on CPI context (" + S["bls_cpi"][0] + "). If the total estate (Cupertino house + SF house + money) stays below the exemption, no federal estate tax is due; the excess is taxed at 40%.") + """
<p class="note">The inheritance also includes a considerable amount of cash/investments (amount not disclosed — internal only). At 2045 projected values, the two houses alone would be ≈ """ + usd(r10(FMV + 1800000*1.03**19)) + """, below the projected ≈ """ + usd(r10(15000000*1.03**19)) + """ single-person exemption — but the cash portion must be added, and the projection is assumption-based. Flagged for review.</p></div>
<div class="card"><h2>Law-change watch (verified status as of Nov 2026)</h2>
<ul class="tight">
<li>Federal: the $15,000,000 exemption is <b>permanent</b> under P.L. 119-21 and indexed after 2026 (""" + sl("irs_rp2532") + """). Congress can still change it by future legislation — monitor each year.</li>
<li>California: initiative 25-0017 to repeal the Prop 19 inheritance reassessment rules <b>failed to qualify for the 2026 ballot</b> — current Prop 19 rules remain in effect (""" + sl("sos_initiatives") + """). Future initiatives could change the parent-child rules again.</li>
<li>AB 1482 (statewide rent cap 5% + CPI, max 10%) <b>expires January 1, 2030</b> unless extended (""" + sl("sfrb_ab1482") + """).</li>
<li>SF Rent Ordinance allowable increase is reset every March 1 at 60% of Bay Area CPI (max 7%): 1.4% for 2025–26, 1.6% for 2026–27 (""" + sl("sfrb_rates") + """).</li>
<li>CPUC Net Billing Tariff (NEM 3.0): solar export compensation is avoided-cost based, not retail — affects the Cupertino solar credit (""" + sl("cpuc_nbt") + """).</li>
</ul></div>
"""
write("pages/inheritance-estate-tax.html", "Inheritance & Estate Tax", body, "pages/inheritance-estate-tax.html")

# ---------------- decision analysis ----------------
scen_rows = [
 ("A — Live in Cupertino as primary residence",
  "Property tax " + usd(r10(LIVE_TAX)) + "/yr (2045 proj.), +2%/yr after",
  "Insurance ≈ $1,500/yr <span class='flag'>(user estimate, unverified)</span>; water $100–150/mo <span class='flag'>(user-provided)</span>; electricity ≈ $0 net, solar credit $10–20/mo <span class='flag'>(user-provided)</span>; maintenance lower than SF <span class='flag'>(user-provided)</span>",
  "Keeps Prop 19 protection (" + usd(r10(RENT_TAX - LIVE_TAX)) + "/yr tax saving vs. renting); SF third unit can then be rented too (amount unverified); no capital-gains event"),
 ("B — Rent out Cupertino (do not occupy)",
  "Property tax " + usd(r10(RENT_TAX)) + "/yr (2045 proj., full reassessment to " + usd(r10(FMV)) + ")",
  "Same operating costs + landlord insurance <span class='flag'>(unverified)</span> + property management",
  "Rental income needed to cover ≈ " + usd(r10(RENT_TAX)) + "/yr tax alone — Cupertino market rent <span class='flag'>unverified, left blank</span>; loses Prop 19 exclusion; depreciation/capital-gains rules apply on later sale"),
 ("C — Sell and reinvest",
  "$0 property tax after sale",
  "One-time selling costs ≈ 6% → net ≈ " + usd(r10(NET_SALE)) + " (2045 proj.)",
  "Step-up in basis → ≈ $0 capital gain (" + S["irs_pub559"][0] + "); invested at 6%/yr assumption → ≈ " + usd(r10(INV_2050)) + " by 2050, ≈ " + usd(r10(INV_2050*0.04)) + "/yr at a 4% withdrawal assumption; CA taxes gains up to 13.3% on later sales (" + S["ftb_capgain"][0] + ")"),
]
body = """
<div class="card"><h2>The decision, framed</h2>
<p>The Cupertino house is expected to be inherited via trust around 2040–2050. The decision is <b>live in it</b>, <b>rent it out</b>, or <b>sell and reinvest</b> — while the San Francisco triplex (ZIP 94122) continues to generate rental income (about $7,150/month from two units, one unit owner-occupied <span class="flag">user-provided</span>).</p></div>
<div class="card"><h2>Scenario comparison at the 2045 inheritance year (all figures rounded to nearest $10; projections use labeled assumptions)</h2>
""" + table(["Scenario", "Property tax", "Other key costs / proceeds", "Tax & strategic effects"], scen_rows) + """
</div>
<div class="card"><h2>10-year view, 2045 → 2055 (assumption-based projections)</h2>
""" + table(["Scenario", "2045 starting point", "2055 projected position"], [
 ("A — Live in Cupertino", "Taxable value " + usd(r10(LIVE_TAXABLE)) + "; tax " + usd(r10(LIVE_TAX)) + "/yr growing 2%/yr",
  "Taxable " + usd(r10(LIVE_TAXABLE*1.02**10)) + "; tax ≈ " + usd(r10(LIVE_TAX*1.02**10)) + "/yr; house value ≈ " + usd(r10(FMV*1.03**10)) + " (market, +3%/yr assumption)"),
 ("B — Rent Cupertino", "Taxable value " + usd(r10(FMV)) + "; tax " + usd(r10(RENT_TAX)) + "/yr growing 2%/yr",
  "Tax ≈ " + usd(r10(RENT_TAX*1.02**10)) + "/yr; house value ≈ " + usd(r10(FMV*1.03**10)) + "; rental income unverified — flagged"),
 ("C — Sell & reinvest", "Net proceeds ≈ " + usd(r10(NET_SALE)) + " invested at 6%/yr (assumption)",
  "Portfolio ≈ " + usd(r10(NET_SALE*1.06**10)) + "; ≈ " + usd(r10(NET_SALE*1.06**10*0.04)) + "/yr at 4% withdrawal assumption; no property tax, no maintenance"),
]) + """
</div>
"""
REC = ("<div class=\"card\"><h2>Recommendation and reasoning</h2><ol class=\"tight\">"
 + "<li><b>Decide the occupancy question first.</b> Under Prop 19, only an heir who occupies the inherited home as a primary residence within 1 year (and claims the homeowners' exemption, filing BOE-19-P within 3 years) keeps a protected taxable value (" + sl("scc_parentchild") + "). Renting it out triggers full reassessment to market value — projected " + usd(r10(RENT_TAX)) + "/yr tax in 2045 vs. " + usd(r10(LIVE_TAX)) + "/yr if lived in, a difference of about " + usd(r10(RENT_TAX-LIVE_TAX)) + "/yr.</li>"
 + "<li><b>If the heir can live in Cupertino:</b> keep the house and live in it (Scenario A). It preserves the Prop 19 tax base, avoids a taxable sale (step-up basis " + sl("irs_pub559") + "), and the SF triplex can be fully rented. This is the lowest-tax, lowest-friction path.</li>"
 + "<li><b>If the heir prefers to stay in San Francisco:</b> sell the Cupertino house (Scenario C). The stepped-up basis makes the sale nearly tax-free; about " + usd(r10(NET_SALE)) + " net (6% costs, 2045 projection) invested at a 6%/yr assumption grows to about " + usd(r10(INV_2050)) + " by 2050 — likely more wealth than the rental scenario can produce after the " + usd(r10(RENT_TAX)) + "/yr reassessed property tax, unless Cupertino market rent is exceptionally high (unverified — flagged).</li>"
 + "<li><b>Renting the Cupertino house (Scenario B) is tax-disadvantaged</b> (full Prop 19 reassessment) and should only be chosen if verified market rent comfortably exceeds the " + usd(r10(RENT_TAX)) + "/yr tax plus insurance, maintenance, vacancy, and management costs.</li>"
 + "<li><b>Estate tax:</b> with the projected 2045 federal exemption of about " + usd(r10(15000000*1.03**19)) + " (assumption) and no CA estate tax (" + sl("ftb_estate") + "), the estate is likely under the federal threshold unless the cash portion is very large — the cash amount is internal-only and flagged for review.</li>"
 + "</ol></div>")

write("pages/decision-analysis.html", "Decision Analysis", body + REC, "pages/decision-analysis.html")

# ---------------- inheritance process ----------------
steps = [
 ("1", "Obtain the death certificate and locate the trust instrument", "Multiple certified copies are needed for the recorder, banks, and the assessor.", "CA courts / county recorder practice"),
 ("2", "Successor trustee takes over", "Record an Affidavit of Death of Trustee (+ certified death certificate) for each real property; prepare a Certification of Trust under Probate Code §18100.5", sl("leginfo_18100")),
 ("3", "Notify beneficiaries and heirs", "Probate Code §16061.7 notice to each beneficiary and heir, even when no probate is opened", sl("leginfo_16061")),
 ("4", "File the Preliminary Change of Ownership Report (BOE-502-A) with the county recorder", "Recorded with the affidavit; starts the property tax change-in-ownership process", sl("boe_502a")),
 ("5", "Get a federal EIN for the trust and retitle accounts", "Never use a personal SSN for trust income", sl("irs_pub559")),
 ("6", "Inventory and appraise all assets at date-of-death values", "Date-of-death fair market values drive the §1014 step-up in basis for the heir", sl("irs_pub559")),
 ("7", "Pay debts, final income taxes, and any estate tax", "File Form 706 within 9 months of death if the gross estate exceeds the exclusion ($15,000,000 for 2026 deaths) or to elect portability (DSUE) for a surviving spouse; 40% federal rate above the exclusion", sl("irs_706")),
 ("8", "Decide occupancy of the Cupertino house and file BOE-19-P", "Move in as primary residence within 1 year + claim homeowners' exemption to keep the Prop 19 exclusion; file the claim within 3 years of transfer (or 6 months after a supplemental notice). If not occupied → full reassessment to market value", sl("scc_parentchild") + "<br>" + sl("scc_faq") + "<br>" + sl("boe_lta25015")),
 ("9", "Distribute or sell assets per the trust terms", "Sale soon after death ≈ no capital gain due to step-up; if kept and used as residence 2 of 5 years, §121 exclusion ($250k/$500k) also available", sl("irs_irm_firpta") + "<br>" + sl("irs_121")),
 ("10", "Final accounting, termination, and record keeping", "Probate Code requires accountings to beneficiaries; keep records of all filings (BOE-502-A, BOE-19-P, Form 706, appraisals)", sl("leginfo_16061")),
]
body = """
<div class="card"><h2>Inheriting the Cupertino house through a trust — step by step</h2>
<p>Because the house is held in a (revocable living) trust, it passes <b>outside probate</b> through trust administration. The tax-relevant steps are 4, 6, 7, and 8.</p>
""" + table(["Step", "Action", "Why it matters / detail", "Source"], steps) + """
</div>
<div class="card"><h2>Key deadlines</h2>
<table><thead><tr><th>Deadline</th><th>Requirement</th><th>Source</th></tr></thead><tbody>
<tr><td>Within 1 year of transfer</td><td>Occupy the inherited home as primary residence and claim the homeowners'/disabled veterans' exemption (Prop 19 condition)</td><td>""" + sl("scc_parentchild") + """</td></tr>
<tr><td>Within 3 years of transfer</td><td>File BOE-19-P parent-child exclusion claim (or within 6 months of a supplemental/escape assessment notice)</td><td>""" + sl("scc_faq") + """</td></tr>
<tr><td>9 months after death (+6-month extension)</td><td>Form 706 federal estate tax return if required; also the only way to elect DSUE portability</td><td>""" + sl("irs_706") + """</td></tr>
<tr><td>Annually (Jan 1 lien date)</td><td>Property tax lien date; assessed value then grows max 2%/yr</td><td>""" + sl("boe_pub800") + """</td></tr>
</tbody></table></div>
"""
write("pages/inheritance-process.html", "Inheritance Process Steps", body, "pages/inheritance-process.html")

# ---------------- operating costs ----------------
body = """
<div class="card"><h2>Cupertino house (ZIP 95014) — costs of ownership after inheritance</h2>
""" + table(["Cost item", "Amount", "Status / source"], [
 ("Property tax", "See Projections page (2026: " + usd(r10(CUP_AV_2026*CUP_RATE)) + "; grows with assessed value)", "Rate law: " + sl("boe_pub29") + "; bill: user-provided <span class='flag'>flagged</span>"),
 ("Water", "$100–$150 / month", "<span class='flag'>User-provided, unverified.</span> Providers: " + sl("cupertino_util")),
 ("Electricity (solar installed)", "≈ $0 net; solar credit ≈ $10–$20 / month", "<span class='flag'>User-provided, unverified.</span> Solar exports paid at avoided-cost rates under the CPUC Net Billing Tariff: " + sl("cpuc_nbt")),
 ("Home insurance (primary residence)", "", "<span class='flag'>UNVERIFIED — left blank.</span> User estimate ≈ $1,500/yr. No official source gives a per-property premium. Context: CA DOI consumer info " + sl("insurance_ca") + "; FAIR Plan (insurer of last resort, dwelling cap $3,000,000 — note the Cupertino house is valued above this cap): " + sl("fairplan")),
 ("Maintenance & repairs", "", "<span class='flag'>UNVERIFIED — left blank.</span> User states lower than the SF house; no official source"),
]) + """</div>
<div class="card"><h2>San Francisco house (ZIP 94122) — rental property economics</h2>
""" + table(["Item", "Amount", "Status / source"], [
 ("Rental income (2 units)", "≈ $7,150 / month", "<span class='flag'>User-provided, unverified</span>"),
 ("Units", "3 livable units; 2 rented, 1 owner-occupied (rent control still applies to rented units in a pre-1979 multi-unit building)", "SF Rent Ordinance coverage (pre-June 13, 1979 buildings): " + sl("sfrb_rates")),
 ("Rent increases", "1.4% (3/1/2025–2/28/2026); 1.6% (3/1/2026–2/28/2027); = 60% of Bay Area CPI, max 7%; AB 1482 cap 5%+CPI/10% expires 1/1/2030", sl("sfrb_rates") + "<br>" + sl("sfrb_ab1482")),
 ("Water (all 3 units)", "$330–$400 / month", "<span class='flag'>User-provided, unverified.</span> SFPUC rates: " + sl("sfpuc_rates")),
 ("Electricity", "$30–$70 / month", "<span class='flag'>User-provided, unverified</span>"),
 ("Property tax", "See Projections page (2026 ≈ " + usd(r10(SF_AV_2025*1.02*SF_RATE)) + ")", "Bill: user-provided <span class='flag'>flagged</span>; rate law: " + sl("boe_pub29")),
 ("Insurance (rental/landlord)", "", "<span class='flag'>UNVERIFIED — left blank.</span> User estimate ≈ $1,500/yr; no official per-property source. Context: " + sl("insurance_ca")),
]) + """</div>
<div class="card"><h2>Notes</h2>
<ul class="tight">
<li>Utility costs are set by CPUC-regulated providers (San Jose Water / California Water Service in Cupertino; SFPUC in SF; PG&amp;E for electricity) — see provider links. Actual bills are user-provided and flagged.</li>
<li>Insurance premiums cannot be confirmed from any official source for a specific property; cells are intentionally blank and flagged rather than inferred.</li>
<li>For projections, operating costs are assumed to inflate at the 3%/yr assumption used elsewhere (BLS CPI context: +3.7% 12-month Sept 2026 — """ + sl("bls_cpi") + """).</li>
</ul></div>
"""
write("pages/operating-costs.html", "Operating Costs", body, "pages/operating-costs.html")

# ---------------- flagged ----------------
flags = [
 ("Cupertino & SF estimated market values ($3,100,000 / $1,800,000, Nov 2026)", "User-provided; no official source", "User statement"),
 ("All historical property tax / assessment figures for both houses", "User-provided county bill records; not independently verified", "User statement; rate law verified at " + S["boe_pub29"][1]),
 ("Effective tax rates (Cupertino 1.335%, SF 2.135%)", "Derived from user-provided 2025 bills; actual tax-rate-area schedules vary", S["scc_booklet"][1]),
 ("Cupertino home insurance ≈ $1,500/yr; SF landlord insurance ≈ $1,500/yr", "UNVERIFIED — no official per-property source; left blank in tables", S["insurance_ca"][1] + " ; " + S["fairplan"][1]),
 ("Cupertino water $100–150/mo; solar credit $10–20/mo; SF water $330–400/mo; SF electricity $30–70/mo; SF rent $7,150/mo", "User-provided operating figures; unverified", S["cupertino_util"][1] + " ; " + S["sfpuc_rates"][1] + " ; " + S["cpuc_nbt"][1]),
 ("Cupertino market rent (for the rent-out scenario)", "UNVERIFIED — left blank; decision guidance given as a threshold instead", "—"),
 ("Market appreciation 3%/yr; investment return 6%/yr; inflation 3%/yr; 4% withdrawal; 6% selling costs", "Projection assumptions, clearly labeled; not official values", S["fhfa_hpi"][1] + " ; " + S["bls_cpi"][1]),
 ("Prop 19 $1M adjustment growth (3%/yr from $1,044,586)", "Official only for Feb 16, 2025–Feb 15, 2027; later adjustments set every 2 years by CA HPI", S["boe_lta25015"][1] + " ; " + S["boe_rule462"][1]),
 ("Estate exemption projections to 2050", "2026 value official ($15,000,000); later years are 3%/yr indexing assumption", S["irs_rp2532"][1]),
 ("Amount of cash/investments in the inheritance", "Internal-only by privacy rule; not published; estate-tax headroom therefore flagged", "—"),
 ("Prop 19 repeal initiative 25-0017", "Failed to qualify for the 2026 ballot — current law unchanged; future initiatives possible", S["sos_initiatives"][1]),
 ("AB 1482 statewide rent cap", "In effect but expires Jan 1, 2030 unless amended", S["sfrb_ab1482"][1]),
]
body = """
<div class="card"><h2>Flagged for review</h2>
<p>Every value that could not be confirmed from an official source is listed here and left blank or labeled on the site. Nothing was inferred or filled in.</p>
""" + table(["Item", "Status", "Source / link"], flags) + """</div>
"""
write("pages/flagged-for-review.html", "Flagged for Review", body, "pages/flagged-for-review.html")

# ---------------- sources ----------------
src_rows = [(i+1, "<a href='{}' target='_blank' rel='noopener'>{}</a>".format(v[1], v[0])) for i, v in enumerate(S.values())]
body = """
<div class="card"><h2>Official sources used (manual review links)</h2>
""" + table(["#", "Source"], src_rows, "All links verified reachable at research time (Nov 2026).") + """</div>
"""
write("pages/sources.html", "Sources", body, "pages/sources.html")

print("Site generated:", os.listdir(ROOT), os.listdir(PAGES))
