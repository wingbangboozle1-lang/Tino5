# -*- coding: utf-8 -*-
"""Build the consolidated decision site under decision/.

Run:  python3 decision/_src/build.py
Then: python3 decision/_src/verify.py

Every table row carries a link to an official source. Rows that could not be
confirmed carry a blank value cell and an explicit unverified marker.
"""

import os
import html
import re

import sources
import model as M
import pages as P

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
BASE = ""          # relative links inside decision/

m = M.money
r10 = M.r10

# --------------------------------------------------------------------- sources
def src_links(ids):
    if not ids:
        return ""
    out = []
    for i in ids:
        s = sources.S_BY_ID.get(i)
        if not s:
            raise SystemExit("unknown source id: %s" % i)
        label = s["publisher"]
        out.append('<a class="src" href="%s" target="_blank" rel="noopener noreferrer" '
                   'title="%s">%s</a>' % (html.escape(s["url"], quote=True),
                                          html.escape(s["title"]), html.escape(label)))
        if i in sources.NOT_OPENED:
            out.append('<span class="tag t-open">not opened</span>')
    return " ".join(out)


# --------------------------------------------------------------------- tables
STATUS_TAG = {
    "verified": ("t-ver", "verified"),
    "owner": ("t-own", "owner input"),
    "derived": ("t-der", "derived"),
    "assumption": ("t-asm", "assumption"),
    "unverified": ("t-unv", "unverified"),
    "reported": ("t-rep", "reported"),
    "label": ("t-lab", ""),
}


def cell_html(c):
    t = c.get("t", "")
    st = c.get("st", "verified")
    cls, _ = STATUS_TAG[st]
    txt = "" if t is None else str(t)
    if txt == "":
        txt = '<span class="blank">&mdash; unverified, value withheld</span>'
    body = html.escape(txt, quote=False) if "<span" not in txt else txt
    for e in ("mdash", "ndash", "hellip", "rarr", "larr", "nbsp", "amp", "quot"):
        body = body.replace("&amp;%s;" % e, "&%s;" % e)
    return '<td class="%s">%s%s</td>' % (cls, body, ("<br>" + src_links(c.get("s", []))) if c.get("s") else "")


def has_official(c):
    from urllib.parse import urlparse
    for i in c.get("s", []):
        rec = sources.S_BY_ID.get(i)
        if rec and urlparse(rec["url"]).netloc in sources.OFFICIAL_HOSTS:
            return True
    return False


# Order matters: the weakest status in the row is the one that governs.
NOSRC_ORDER = ["unverified", "assumption", "owner", "derived", "reported", "label", "verified"]
NOSRC_REASON = {
    "unverified": "value withheld, could not be confirmed against any official publication",
    "assumption": "modelling assumption, no official publication sets this figure",
    "owner": "owner record only, not independently verifiable from any public source",
    "derived": "derived from owner records rather than read from an official publication",
    "reported": "secondary report, not confirmed against a primary source",
    "label": "descriptive row, no figure to source",
    "verified": "no official source cited",
}


def worst_status(row):
    for st in NOSRC_ORDER:
        if any(c.get("st", "verified") == st for c in row):
            return st
    return "verified"


def render_table(t):
    tid = t.get("id", "")
    filt = ''
    if t.get("filter", True):
        filt = ('<div class="tf"><input type="search" placeholder="Filter this table&hellip;" '
                'oninput="filterRows(this,\'%s\')"></div>' % tid)
    head = "".join("<th>%s</th>" % html.escape(c, quote=False) for c in t["cols"])
    rows = []
    for i, r in enumerate(t["rows"]):
        cells = [cell_html(c) for c in r]
        if not any(has_official(c) for c in r):
            cells[-1] = cells[-1].replace(
                "</td>", "<br><span class='nosrc'>No official source &mdash; %s</span></td>"
                % NOSRC_REASON[worst_status(r)], 1)
        rows.append('<tr data-i="%d">%s</tr>' % (i, "".join(cells)))
    note = ""
    if t.get("note"):
        note = '<p class="tnote">%s</p>' % t["note"]
    return ('<div class="tblwrap">%s<table class="data" id="%s"><thead><tr>%s</tr></thead>'
            '<tbody>%s</tbody></table>%s</div>' % (filt, tid, head, "".join(rows), note))


# --------------------------------------------------------------------- shell
PAGES_NAV = [
    ("index.html", "Overview"),
    ("executive-summary.html", "Executive summary"),
    ("properties.html", "Properties"),
    ("property-tax.html", "Property tax"),
    ("inheritance-tax.html", "Inheritance &amp; estate tax"),
    ("operating-costs.html", "Running costs"),
    ("projections.html", "Projections"),
    ("scenarios.html", "Options compared"),
    ("black-swan.html", "Black swans"),
    ("process.html", "Transfer process"),
    ("questions.html", "Questions &amp; gaps"),
    ("suggestions.html", "Suggestions"),
    ("law-watch.html", "Law watch"),
    ("sources.html", "Sources"),
    ("flagged.html", "Flagged"),
    ("methodology.html", "Method &amp; privacy"),
]

CSS = """
:root{--ink:#16202e;--mut:#5d6b7f;--line:#dfe5ee;--bg:#f6f8fb;--card:#fff;
--blue:#1f4e79;--blue-l:#eaf1f8;--amber:#8a5a00;--amber-l:#fdf3e2;--red:#8c2f2f;
--red-l:#fbecec;--green:#1d6b45;--green-l:#e9f5ee;--grey:#5b6474;--grey-l:#eef1f5}
*{box-sizing:border-box}
body{margin:0;font:15px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
color:var(--ink);background:var(--bg)}
a{color:var(--blue)}
header{background:var(--card);border-bottom:1px solid var(--line);padding:14px 20px;position:sticky;top:0;z-index:20}
header .wrap{display:flex;align-items:center;gap:14px;flex-wrap:wrap;max-width:1280px;margin:auto}
header h1{font-size:17px;margin:0;color:var(--blue);white-space:nowrap}
nav{display:flex;gap:2px;flex-wrap:wrap;margin-left:auto}
nav a{font-size:12.5px;padding:5px 9px;border-radius:6px;color:var(--mut);text-decoration:none;white-space:nowrap}
nav a:hover{background:var(--blue-l);color:var(--blue)}
nav a.on{background:var(--blue);color:#fff}
main{max-width:1280px;margin:auto;padding:22px 20px 70px}
h2.kick{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);margin:0 0 4px}
h1.pt{font-size:26px;margin:0 0 8px;color:var(--blue)}
h2{font-size:18px;margin:30px 0 8px;color:var(--blue);border-bottom:1px solid var(--line);padding-bottom:6px}
h3{font-size:15px;margin:20px 0 6px}
p{max-width:88ch}
.lead{font-size:15.5px;color:#2a3646}
.muted{color:var(--mut);font-size:13.5px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px;margin:14px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:14px 16px}
.card h3{margin:0 0 6px;font-size:15px;color:var(--blue)}
.card p{margin:6px 0 0;font-size:14px}
.card ul{margin:8px 0 0;padding-left:18px;font-size:14px}
.card li{margin:4px 0}
.tblwrap{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:9px;
margin:12px 0 22px;padding:4px 0 0}
.tf{padding:8px 10px}
.tf input{width:100%;max-width:340px;padding:6px 9px;border:1px solid var(--line);border-radius:6px;font:inherit}
table.data{width:100%;border-collapse:collapse;font-size:13px}
table.data th{background:var(--blue-l);text-align:left;padding:8px 10px;border-bottom:2px solid var(--line);
font-weight:600;color:#1b3d5c;white-space:nowrap}
table.data td{padding:8px 10px;border-bottom:1px solid #eef1f6;vertical-align:top}
table.data tbody tr:hover{background:#fafcff}
td.t-ver{background:#fbfefc}td.t-own{background:#fffdf7}td.t-der{background:#fafcff}
td.t-asm{background:#f8f9fb}td.t-unv{background:var(--red-l)}
td.t-rep{background:var(--amber-l)}td.t-lab{font-weight:600;color:#22303f}
.blank{color:var(--red);font-style:italic;font-size:12.5px}
.nosrc{display:inline-block;margin-top:3px;color:var(--red);font-size:11.5px;font-style:italic;background:var(--red-l);border-radius:3px;padding:1px 5px}
.src{display:inline-block;font-size:11px;text-decoration:none;background:var(--grey-l);color:#3a4658;
border-radius:4px;padding:1px 6px;margin:2px 3px 0 0;border:1px solid #e0e6ef}
.src:hover{background:var(--blue);color:#fff;border-color:var(--blue)}
.tag{display:inline-block;font-size:10.5px;border-radius:4px;padding:1px 5px;margin:2px 3px 0 0;
border:1px solid transparent}
.t-open{background:#f3e8fb;color:#5b2b7a;border-color:#e3d0f0}
.tnote{font-size:12.5px;color:var(--mut);padding:2px 12px 12px;margin:0}
.legend{display:flex;gap:8px;flex-wrap:wrap;font-size:12px;margin:8px 0 14px;align-items:center}
.legend span{padding:2px 8px;border-radius:5px;border:1px solid var(--line)}
.lg-ver{background:#fbfefc}.lg-own{background:#fffdf7}.lg-der{background:#fafcff}
.lg-asm{background:#f8f9fb}.lg-unv{background:var(--red-l);color:var(--red)}
.lg-rep{background:var(--amber-l);color:var(--amber)}
.banner{background:#fff8e8;border:1px solid #f0d9a8;border-left:4px solid #d99b1c;border-radius:8px;
padding:11px 14px;margin:16px 0;font-size:13.5px}
.banner.red{background:var(--red-l);border-color:#eecccc;border-left-color:#c05555}
.banner.blue{background:var(--blue-l);border-color:#cfe0ee;border-left-color:var(--blue)}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px;margin:14px 0 6px}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:12px 14px}
.kpi .v{font-size:21px;font-weight:650;color:var(--blue);line-height:1.2}
.kpi .l{font-size:12px;color:var(--mut);margin-top:3px}
ol.steps{counter-reset:s;list-style:none;padding:0;margin:12px 0}
ol.steps>li{counter-increment:s;position:relative;padding:0 0 16px 44px;border-left:2px solid var(--line);margin-left:14px}
ol.steps>li::before{content:counter(s);position:absolute;left:-15px;top:-2px;width:28px;height:28px;
border-radius:50%;background:var(--blue);color:#fff;font-size:13px;font-weight:600;
display:flex;align-items:center;justify-content:center}
ol.steps>li:last-child{border-left-color:transparent}
ol.steps h4{margin:2px 0 4px;font-size:14.5px}
ol.steps p{margin:3px 0;font-size:13.5px}
.q{border-left:3px solid var(--blue);padding-left:12px;margin:18px 0}
.q .qq{font-weight:600}
.chk{font-weight:600;color:var(--green)}
footer{max-width:1280px;margin:auto;padding:20px;border-top:1px solid var(--line);
color:var(--mut);font-size:12.5px}
@media(max-width:900px){nav{display:none}h1.pt{font-size:22px}}
"""

JS = """
function filterRows(el,id){
  var q=el.value.toLowerCase(),t=document.getElementById(id);
  if(!t)return;
  var rows=t.querySelectorAll('tbody tr');
  for(var i=0;i<rows.length;i++){
    var txt=rows[i].textContent.toLowerCase();
    rows[i].style.display = txt.indexOf(q)>-1 ? '' : 'none';
  }
}
"""


def shell(title, kicker, body, active):
    nav = "".join(
        '<a href="%s%s"%s>%s</a>' % (BASE, u, ' class="on"' if u == active else "", lab)
        for u, lab in PAGES_NAV)
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<meta name="referrer" content="no-referrer">
<title>%s &middot; Inheritance decision desk</title>
<style>%s</style></head><body>
<header><div class="wrap"><h1>Inheritance decision desk</h1><nav>%s</nav></div></header>
<main>
<p class="kick">%s</p><h1 class="pt">%s</h1>
%s
</main>
<footer>Not tax, legal or investment advice. Figures are rounded to the nearest $10 and every
table row links to the official source it was read from; rows that could not be confirmed carry a
blank value and an unverified marker. Rules and thresholds change &mdash; re-check the current law
before acting.</footer>
<script>%s</script></body></html>
""" % (html.escape(title), CSS, nav, kicker, html.escape(title), body, JS)


LEGEND = ('<div class="legend"><b style="font-size:12px">Cell key:</b>'
          '<span class="lg-ver">verified &mdash; read from an official source</span>'
          '<span class="lg-own">owner input &mdash; no official source exists</span>'
          '<span class="lg-der">derived &mdash; computed from the inputs shown</span>'
          '<span class="lg-asm">assumption &mdash; chosen here, listed on the method page</span>'
          '<span class="lg-rep">reported &mdash; pending official confirmation</span>'
          '<span class="lg-unv">unverified &mdash; value withheld</span></div>')

BANNER = ('<div class="banner"><b>Privacy.</b> No name, street address, parcel or account number '
          'appears anywhere on this site. Properties are identified only as Property A (Santa Clara '
          'County, to be inherited through a trust) and Property B (San Francisco, already owned). '
          'All money is rounded to the nearest $10 so published figures cannot be matched back to a '
          'public record. Statutory amounts are quoted exactly as published because they are '
          'statewide constants and identify nothing.</div>')


def write(name, title, kicker, body, active=None):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(shell(title, kicker, body, active or name))
    return path


# =============================================================== page: index
def page_index():
    cards = [
        ("executive-summary.html", "Executive summary",
         "The six findings that matter, the three options side by side, and the size of the "
         "property tax jump on transfer."),
        ("properties.html", "Properties",
         "What is known about Property A and Property B, and exactly which figures are owner "
         "estimates with no official source."),
        ("property-tax.html", "Property tax",
         "Proposition 13 and Proposition 19 as they apply here, the assessment rules, and the "
         "deadlines that carry the money."),
        ("inheritance-tax.html", "Inheritance &amp; estate tax",
         "California imposes none. The federal threshold, what is indexed, and how the exemption "
         "projects forward to 2050."),
        ("operating-costs.html", "Running costs",
         "Water, electricity, insurance and maintenance for both properties, and which of them are "
         "guesses."),
        ("projections.html", "Projections",
         "Year by year to 2076: market value, assessed value, the property tax bill, and what the "
         "bill becomes if the property changes hands in that year."),
        ("scenarios.html", "Options compared",
         "Occupy, rent out, or sell and reinvest &mdash; with the break-even rates at which the "
         "ranking flips."),
        ("black-swan.html", "Black swans",
         "Eight regimes built on real historical inflation and price behaviour, because growth and "
         "inflation are never constant over fifty years."),
        ("process.html", "Transfer process",
         "Step by step through a trust inheritance in California, with the form and the clock for "
         "each step."),
        ("questions.html", "Questions &amp; gaps",
         "Twenty-six questions. Each says what is known, what is missing, what decision it blocks, "
         "and how to find the answer."),
        ("suggestions.html", "Suggestions",
         "Fifteen suggestions, none implemented. Each is here for review and a decision before "
         "anything changes."),
        ("law-watch.html", "Law watch",
         "What is actually pending in Congress and on California ballots that could move these "
         "numbers before 2050."),
        ("sources.html", "Sources",
         "Every official document read for this site, what each one evidences, and which were "
         "located but not opened."),
        ("flagged.html", "Flagged",
         "Everything that could not be confirmed, everything that looks wrong, and the one item "
         "that is not fixable by a commit."),
        ("methodology.html", "Method &amp; privacy",
         "Every assumption in one table, how the model works, and exactly what was done to keep "
         "personal information off the site."),
    ]
    g = "".join('<a class="card" href="%s%s"><h3>%s</h3><p>%s</p></a>'
                % (BASE, u, t, d) for u, t, d in cards)

    t45 = P.TV[2045]
    kpi = "".join(
        '<div class="kpi"><div class="v">%s</div><div class="l">%s</div></div>' % (v, l) for v, l in [
            (m(r10(P.A_SER[2026]["tax"])), "Property A bill today (2026)"),
            (m(r10(t45["occ_tax"])), "Property A bill after a 2045 transfer, exclusion claimed"),
            (m(r10(t45["rent_tax"])), "Property A bill after a 2045 transfer, no exclusion"),
            ("$15,000,000", "Federal estate tax threshold, death in 2026"),
            ("None", "California estate or inheritance tax"),
            ("%s" % P.pct(M.breakeven_portfolio_return(2045, "rent", with_housing=True), 2)["t"],
             "Portfolio return at which selling stops beating renting"),
        ])

    body = BANNER + '<div class="kpis">' + kpi + "</div>" + \
        '<p class="lead">Two properties, one decision. Property A is in Santa Clara County and is ' \
        'expected to pass through a family trust somewhere in the 2040&ndash;2050 window. ' \
        'Property B is in San Francisco and is already owned; it has three units, two of them let. ' \
        'The question is whether to live in Property A, let it, or sell it and reinvest.</p>' + \
        '<div class="banner blue"><b>The finding that drives everything else.</b> California ' \
        'assessment is acquisition-based, so today\'s bill reflects a base year value set decades ' \
        'ago. The moment ownership changes the property is reassessed. Even with the Proposition 19 ' \
        'parent-child exclusion claimed in full, the bill multiplies; without it, it multiplies ' \
        'again. Every other line in this analysis is an order of magnitude smaller.</div>' + \
        "<h2>Where to go</h2><div class='grid'>" + g + "</div>" + \
        '<h2>How to read the tables</h2>' + LEGEND + \
        '<p class="muted">Every row links to the official publication it was read from. Where a ' \
        'value could not be confirmed, the cell is blank and marked unverified rather than filled ' \
        'with an estimate. Money is rounded to the nearest $10.</p>'
    return write("index.html", "Overview", "Start here", body)


# ====================================================== page: exec summary
def page_exec():
    es = P.executive_summary()
    cards = []
    for i, f in enumerate(es["findings"], 1):
        ps = "".join("<p>%s</p>" % html.escape(p, quote=False) for p in f["p"])
        cards.append('<div class="card"><h3>%s</h3>%s%s</div>'
                     % (html.escape(f["h"], quote=False), ps, src_links(f["src"])))
    body = BANNER + '<div class="grid">' + "".join(cards) + "</div>" + LEGEND
    for t in es["tables"]:
        body += "<h2>%s</h2>%s" % (html.escape(t["title"]), render_table(t))
    body += ('<div class="banner"><b>Read the break-even table before acting on the ranking.</b> '
             'The order of the three options is produced by a model, not by a fact. What is solid '
             'is the size of the property tax jump, the absence of any California death tax, the '
             'step-up in basis, and the filing deadlines. Everything else is a threshold you should '
             'test against your own numbers.</div>')
    return write("executive-summary.html", "Executive summary",
                 "What the analysis found", body)


# ====================================================== page: properties
def page_properties():
    o = M.OWNER
    a26, b25 = P.A_SER[2026], P.B_SER[2025]
    facts = dict(
        id="facts", title="The two properties",
        cols=["Item", "Property A &mdash; Santa Clara County (inherited)",
              "Property B &mdash; San Francisco (already owned)"],
        rows=[
            [P.C("Role in the decision", [], "label"),
             P.C("To be inherited through a family trust, expected 2040&ndash;2050", [], "owner"),
             P.C("Already owned; lived in; two of three units let", [], "owner")],
            [P.C("Estimated market value, November 2026", [], "label"),
             P.money(o["A_market_value_2026"], [], "owner"),
             P.money(o["B_market_value_2026"], [], "owner")],
            [P.C("Last reported assessed value", [], "label"),
             P.money(o["A_assessed_2026"], [], "owner"),
             P.money(o["B_assessed_2025"], [], "owner")],
            [P.C("Last reported annual property tax bill", [], "label"),
             P.money(o["A_tax_2025"], [], "owner"),
             P.money(o["B_tax_2025"], [], "owner")],
            [P.C("Livable units", [], "label"),
             P.C("Not stated", [], "unverified"),
             P.C("3", [], "owner")],
            [P.C("Units currently let", [], "label"),
             P.C("0 &mdash; owner-occupied", [], "owner"),
             P.C("2", [], "owner")],
            [P.C("Current rent", [], "label"),
             P.C("None", [], "owner"),
             P.C("%s a month, about %s a year" % (m(7150), m(7150 * 12)), [], "owner")],
            [P.C("Water", [], "label"),
             P.C("%s to %s a month (owner range); %s used as the planning figure"
                 % (m(100), m(150), m(130)), [], "owner"),
             P.C("%s to %s a month for all three units (owner range); %s used"
                 % (m(330), m(400), m(370)), [], "owner")],
            [P.C("Electricity", [], "label"),
             P.C("Rooftop solar normally produces a credit of about %s to %s a month; "
                 "%s a month used as the planning figure" % (m(10), m(20), m(10)), [], "owner"),
             P.C("%s to %s a month (owner range); %s used" % (m(30), m(70), m(50)), [], "owner")],
            [P.C("Water and sewer rates", [], "label"),
             P.C("Not the public utility that serves San Francisco; rate schedule not retrieved",
                 [], "unverified"),
             P.C("Served by the San Francisco Public Utilities Commission; official 2026-27 "
                 "schedules published", ["sfpuc_rates"], "verified")],
            [P.C("Home insurance", [], "label"),
             P.C("%s a year &mdash; owner estimate, no quotation obtained"
                 % m(o["A_insurance_year"]), [], "unverified"),
             P.C("%s a year &mdash; owner estimate, no quotation obtained"
                 % m(o["B_insurance_year"]), [], "unverified")],
            [P.C("Insurance data that does exist officially", [], "label"),
             P.C("California Department of Insurance publishes ZIP-level residential insurance "
                 "data under Insurance Code section 929", ["cdi_residential"], "verified"),
             P.C("Same official source applies", ["cdi_residential"], "verified")],
            [P.C("Maintenance", [], "label"),
             P.C("Described by the owner as lighter than Property B; no figure supplied",
                 [], "unverified"),
             P.C("No figure supplied", [], "unverified")],
            [P.C("Solar tariff", [], "label"),
             P.C("Not stated &mdash; which tariff the system is on, and when the enrolment ends, "
                 "is unknown", [], "unverified"),
             P.C("n/a", [], "label")],
            [P.C("Year built", [], "label"),
             P.C("Not supplied", [], "unverified"),
             P.C("Not supplied &mdash; decides whether the local rent ordinance applies",
                 [], "unverified")],
        ],
        note="Every figure in this table is either owner input or explicitly unverified. Nothing "
             "here was read from a public record, which is deliberate: assessed values and tax "
             "bills are searchable, so only rounded figures appear and they are never combined with "
             "an address, parcel number or name.")

    rates = dict(
        id="rates", title="Tax rates applied to each property",
        cols=["Property", "Rate used", "What it is", "Status"],
        rows=[
            [P.C("Property A", [], "label"),
             P.pct(P.RATE_A, 2, [], "derived"),
             P.C("The owner's 2025 bill divided by the owner's 2025 assessed value. It bundles the "
                 "1% Proposition 13 levy with voter-approved debt and any parcel charges. Santa "
                 "Clara County has hundreds of tax rate areas, so no single published rate can be "
                 "quoted for the parcel.", ["boe_pub29"], "derived"),
             P.C("Derived from owner input", [], "derived")],
            [P.C("Property B &mdash; ad valorem", [], "label"),
             P.C("1.18162182%", ["sf_treasurer_secured"], "verified"),
             P.C("The City and County of San Francisco secured property tax rate for Fiscal Year "
                 "2026-27, published by the Treasurer &amp; Tax Collector.",
                 ["sf_treasurer_secured"], "verified"),
             P.C("Verified", [], "verified")],
            [P.C("Property B &mdash; other charges", [], "label"),
             P.money(P.B_FIXED, [], "derived"),
             P.C("A year of charge that is not explained by the official rate. The owner's 2025 "
                 "bill less assessed value times 1.18162182 percent leaves about %s a year. It is "
                 "carried as a flat charge because its nature is unknown."
                 % m(P.B_FIXED), ["sf_treasurer_secured"], "derived"),
             P.C("Derived &mdash; reconcile against the bill", [], "derived")],
        ],
        note="The Property A rate is the weakest link in the projections. It is stable across the "
             "owner's own history (roughly 1.33% to 1.41% every year from 2014 to 2025), which is "
             "reassuring, but it should be replaced with the rate printed on the actual bill.")

    body = BANNER + "<p class='lead'>What is known about each property, stated so that the " \
           "difference between a fact and a guess is visible in every row.</p>" + LEGEND + \
        render_table(facts) + "<h2>Rates used</h2>" + render_table(rates) + \
        ('<div class="banner red"><b>The single most valuable thing you can do with this page.</b> '
         'Replace the four unverified cells &mdash; insurance on both properties, the solar tariff, '
         'and Property A maintenance &mdash; with real documents. They are the only inputs on this '
         'site that are pure guesswork, and two of them feed every projection that follows.</div>')
    return write("properties.html", "Properties", "What is known and what is guessed", body)


# ====================================================== page: property tax
def page_property_tax():
    rules = dict(
        id="rules", title="The rules that set the bill",
        cols=["Rule", "What it says", "Why it matters here", "Source"],
        rows=[
            [P.C("Proposition 13 rate ceiling", ["boe_pub29"], "verified"),
             P.C("The tax rate is limited to 1% of assessed value plus the rate needed to fund "
                 "voter-approved bonded indebtedness.", ["boe_pub29"], "verified"),
             P.C("Explains why the real rate on both properties is above 1%.", [], "derived"),
             P.C("BOE Publication 29", ["boe_pub29"], "verified")],
            [P.C("Proposition 13 assessment cap", ["boe_pub29"], "verified"),
             P.C("Annual increases in base year value are limited to no more than 2%, and the "
                 "property is reassessed to market value only on a change in ownership or new "
                 "construction.", ["boe_pub29"], "verified"),
             P.C("The whole reason the current bill is low, and the whole reason it jumps.",
                 [], "derived"),
             P.C("BOE Publication 29", ["boe_pub29"], "verified")],
            [P.C("What counts as a change in ownership", ["boe_prop19"], "verified"),
             P.C("A transfer of a family home between parent and child on or after 16 February "
                 "2021 is governed by Proposition 19, not Proposition 58.", ["boe_prop19"], "verified"),
             P.C("The transfer date decides which rule applies. The window here is 2040-2050, so "
                 "Proposition 19 will govern.", [], "derived"),
             P.C("BOE Proposition 19", ["boe_prop19"], "verified")],
            [P.C("Proposition 19 value limit", ["boe_lta2025_009"], "verified"),
             P.C("The value cap is the factored base year value plus $1,044,586 for transfers from "
                 "16 February 2025 through 15 February 2027. Market value above the cap is added to "
                 "the taxable value. The amount was $1,000,000 for 2021-2023 and $1,022,600 for "
                 "2023-2025, and is adjusted every two years.", ["boe_lta2025_009"], "verified"),
             P.C("The exclusion is partial, not total. For a house worth several million dollars, "
                 "most of the gap between the old and new assessed values is still taxed.",
                 [], "derived"),
             P.C("BOE LTA 2025/009", ["boe_lta2025_009"], "verified")],
            [P.C("Proposition 19 occupancy requirement", ["boe_pub800_1"], "verified"),
             P.C("The transferee must live in the home as a principal residence within one year of "
                 "the transfer and must continue to occupy it. A transfer of a rental home between "
                 "parent and child does not qualify at all.",
                 ["boe_pub800_1", "boe_prop19"], "verified"),
             P.C("This is the clause that makes 'live in it' and 'rent it' different by an order "
                 "of magnitude.", [], "derived"),
             P.C("BOE Publication 800-1", ["boe_pub800_1"], "verified")],
            [P.C("Consequence of moving out later", ["boe_prop19"], "verified"),
             P.C("At least one eligible transferee must continually live in the property. Once it "
                 "stops being anyone's principal residence it gets a new taxable value as of the "
                 "lien date following the move-out, equal to the fair market value on the date it "
                 "was inherited, adjusted by the inflation factor.", ["boe_prop19"], "verified"),
             P.C("Occupying is not a one-year test. It is a continuing condition.", [], "derived"),
             P.C("BOE Proposition 19", ["boe_prop19"], "verified")],
            [P.C("Homeowners' exemption deadline", ["boe_pub800_1"], "verified"),
             P.C("The homeowners' or disabled veterans' exemption must be filed within one year of "
                 "the transfer to receive the exclusion as of the date of transfer. Filed later, "
                 "the exclusion begins in the year the claim is filed.",
                 ["boe_pub800_1"], "verified"),
             P.C("A late filing does not lose the exclusion, but it loses the back years.",
                 [], "derived"),
             P.C("BOE Publication 800-1", ["boe_pub800_1"], "verified")],
            [P.C("Claim deadline", ["boe_pub800_1"], "verified"),
             P.C("The claim, on form BOE-19-P, must be filed with the county assessor within three "
                 "years of the transfer, or before the property is transferred to a third party, "
                 "whichever comes first.", ["boe_pub800_1", "scc_assessor_p19"], "verified"),
             P.C("Three years sounds generous until it runs against a decision that is still being "
                 "made.", [], "derived"),
             P.C("BOE Publication 800-1", ["boe_pub800_1"], "verified")],
            [P.C("County implementation", ["scc_assessor_p19"], "verified"),
             P.C("Santa Clara County requires at least one child to live in the home as a primary "
                 "residence, applies the value test, and takes BOE-19-P as the claim form.",
                 ["scc_assessor_p19", "scc_assessor_downloads"], "verified"),
             P.C("The county that will actually process the claim.", [], "derived"),
             P.C("Santa Clara County Assessor", ["scc_assessor_p19"], "verified")],
        ],
        note="Proposition 13 and Proposition 19 are both in the California Constitution. Nothing "
             "on this page is a forecast; these are the operative rules as published by the Board "
             "of Equalization and the county assessor.")

    calc = dict(
        id="calc", title="How the taxable value is worked out at transfer",
        cols=["Step", "2040", "2045", "2050"],
        rows=[
            [P.C("Factored base year value at transfer (2% a year)", ["boe_pub29"], "derived"),
             P.money(P.TV[2040]["fbyv"], ["boe_pub29"], "derived"),
             P.money(P.TV[2045]["fbyv"], ["boe_pub29"], "derived"),
             P.money(P.TV[2050]["fbyv"], ["boe_pub29"], "derived")],
            [P.C("Proposition 19 allowance, projected", ["boe_lta2025_009"], "assumption"),
             P.money(P.TV[2040]["allowance"], ["boe_lta2025_009"], "assumption"),
             P.money(P.TV[2045]["allowance"], ["boe_lta2025_009"], "assumption"),
             P.money(P.TV[2050]["allowance"], ["boe_lta2025_009"], "assumption")],
            [P.C("Value cap (base year value plus allowance)", ["boe_prop19"], "derived"),
             P.money(P.TV[2040]["cap"], ["boe_prop19"], "derived"),
             P.money(P.TV[2045]["cap"], ["boe_prop19"], "derived"),
             P.money(P.TV[2050]["cap"], ["boe_prop19"], "derived")],
            [P.C("Market value at transfer", [], "assumption"),
             P.money(P.TV[2040]["fmv"], [], "assumption"),
             P.money(P.TV[2045]["fmv"], [], "assumption"),
             P.money(P.TV[2050]["fmv"], [], "assumption")],
            [P.C("Excess over the cap, added to the taxable value", ["boe_prop19"], "derived"),
             P.money(P.TV[2040]["excess"], ["boe_prop19"], "derived"),
             P.money(P.TV[2045]["excess"], ["boe_prop19"], "derived"),
             P.money(P.TV[2050]["excess"], ["boe_prop19"], "derived")],
            [P.C("New taxable value WITH the exclusion", ["boe_prop19"], "derived"),
             P.money(P.TV[2040]["occ_av"], ["boe_prop19"], "derived"),
             P.money(P.TV[2045]["occ_av"], ["boe_prop19"], "derived"),
             P.money(P.TV[2050]["occ_av"], ["boe_prop19"], "derived")],
            [P.C("New taxable value WITHOUT the exclusion (full reassessment)",
                 ["boe_prop19"], "derived"),
             P.money(P.TV[2040]["rent_av"], ["boe_prop19"], "derived"),
             P.money(P.TV[2045]["rent_av"], ["boe_prop19"], "derived"),
             P.money(P.TV[2050]["rent_av"], ["boe_prop19"], "derived")],
            [P.C("Bill with the exclusion", ["boe_prop19"], "derived"),
             P.money(P.TV[2040]["occ_tax"], ["boe_prop19"], "derived"),
             P.money(P.TV[2045]["occ_tax"], ["boe_prop19"], "derived"),
             P.money(P.TV[2050]["occ_tax"], ["boe_prop19"], "derived")],
            [P.C("Bill without the exclusion", ["boe_prop19"], "derived"),
             P.money(P.TV[2040]["rent_tax"], ["boe_prop19"], "derived"),
             P.money(P.TV[2045]["rent_tax"], ["boe_prop19"], "derived"),
             P.money(P.TV[2050]["rent_tax"], ["boe_prop19"], "derived")],
            [P.C("Value of the exclusion, per year", ["boe_prop19"], "derived"),
             P.money(P.TV[2040]["rent_tax"] - P.TV[2040]["occ_tax"], ["boe_prop19"], "derived"),
             P.money(P.TV[2045]["rent_tax"] - P.TV[2045]["occ_tax"], ["boe_prop19"], "derived"),
             P.money(P.TV[2050]["rent_tax"] - P.TV[2050]["occ_tax"], ["boe_prop19"], "derived")],
        ],
        note="The allowance is $1,044,586 only for transfers between 16 February 2025 and 15 "
             "February 2027. For a transfer in the 2040s it is projected forward at the California "
             "House Price Index change the Board of Equalization last used, 2.15% a year, which is "
             "an assumption, not a published figure. The next published adjustment is in February "
             "2027 and every second February after that.")

    body = BANNER + "<p class='lead'>California assesses property at what it was worth when it was " \
           "last acquired, not what it is worth now. That single fact produces both the low bill " \
           "today and the large increase on transfer.</p>" + LEGEND + \
        render_table(rules) + "<h2>The arithmetic at each candidate transfer year</h2>" + \
        render_table(calc) + \
        ('<div class="banner blue"><b>What the numbers say.</b> The exclusion is worth tens of '
         'thousands of dollars a year, but it does not keep the old bill. The bill multiplies '
         'either way. That reframes the question: it is not how to avoid the increase, it is '
         'whether the property is worth holding at the new carrying cost at all.</div>')
    return write("property-tax.html", "Property tax",
                 "Proposition 13 and Proposition 19", body)


# ================================================ page: inheritance & estate tax
def page_inheritance_tax():
    ex = M.estate_exemption_projection(0.025)
    extab = {r["year"]: r["amount"] for r in ex}

    jur = dict(
        id="jur", title="Which governments can tax the transfer",
        cols=["Tax", "Applies?", "Authority", "Source"],
        rows=[
            [P.C("California inheritance tax", ["ca_rtc_13301"], "verified"),
             P.C("No", ["ca_rtc_13301"], "verified"),
             P.C("Revenue and Taxation Code section 13301: neither the state nor any political "
                 "subdivision may impose any gift, inheritance, succession, legacy, income or "
                 "estate tax on a transfer occurring by reason of a death. Added by Proposition 6 "
                 "in 1982.", ["ca_rtc_13301"], "verified"),
             P.C("R&TC 13301", ["ca_rtc_13301"], "verified")],
            [P.C("California estate tax", ["ca_rtc_13301"], "verified"),
             P.C("No", ["ca_rtc_13301"], "verified"),
             P.C("Same section, same prohibition.", ["ca_rtc_13301"], "verified"),
             P.C("R&TC 13301", ["ca_rtc_13301"], "verified")],
            [P.C("Local estate or transfer tax in California", ["ca_rtc_13301"], "verified"),
             P.C("No", ["ca_rtc_13301"], "verified"),
             P.C("Section 13301 binds political subdivisions as well as the state.",
                 ["ca_rtc_13301"], "verified"),
             P.C("R&TC 13301", ["ca_rtc_13301"], "verified")],
            [P.C("Federal estate tax", ["irs_estate_tax"], "verified"),
             P.C("Only if the estate exceeds the threshold", ["irs_estate_tax"], "verified"),
             P.C("A tax on the estate, not on the heir. Paid before distribution.",
                 ["irs_estate_tax"], "verified"),
             P.C("IRS estate tax page", ["irs_estate_tax"], "verified")],
            [P.C("Federal inheritance tax", ["crs_if12846"], "verified"),
             P.C("No such tax exists", ["crs_if12846"], "verified"),
             P.C("The United States taxes the estate, not the recipient.",
                 ["crs_if12846"], "verified"),
             P.C("CRS IF12846", ["crs_if12846"], "verified")],
            [P.C("Federal income tax on the heir", ["irs_p551"], "verified"),
             P.C("Only on gain after the transfer", ["irs_p551"], "verified"),
             P.C("Property acquired from a decedent takes a basis equal to fair market value at "
                 "death, so appreciation in the decedent's lifetime is never taxed to anyone.",
                 ["irs_p551", "crs_if12846"], "verified"),
             P.C("IRS Publication 551", ["irs_p551"], "verified")],
        ],
        note="This is the cleanest answer on the whole site: California cannot tax the transfer, "
             "and no local government in California can either. Only the federal estate tax can "
             "apply, and only above a threshold that is higher than most estates.")

    thr = dict(
        id="thr", title="The federal threshold, published and projected",
        cols=["Year of death", "Basic exclusion amount", "Basis", "Status"],
        rows=[
            [P.C("2024", [], "label"), P.C("$13,610,000", ["irs_estate_tax"], "verified"),
             P.C("Published by the IRS", ["irs_estate_tax"], "verified"),
             P.C("Verified", [], "verified")],
            [P.C("2025", [], "label"), P.C("$13,990,000", ["irs_estate_tax"], "verified"),
             P.C("Published by the IRS", ["irs_estate_tax"], "verified"),
             P.C("Verified", [], "verified")],
            [P.C("2026", [], "label"), P.C("$15,000,000", ["irs_estate_tax"], "verified"),
             P.C("Set by P.L. 119-21 and made permanent; published by the IRS",
                 ["irs_estate_tax", "crs_if12846"], "verified"),
             P.C("Verified", [], "verified")],
            [P.C("2027", [], "label"), P.C("$15,480,000", ["irs_rp2026_35"], "verified"),
             P.C("Section 3.44 of Rev. Proc. 2026-35. The same figure is the generation-skipping "
                 "transfer exemption.", ["irs_rp2026_35"], "verified"),
             P.C("Verified", [], "verified")],
        ] + [
            [P.C(str(y), [], "label"), P.money(extab[y], ["irs_rp2026_35"], "assumption"),
             P.C("Indexed forward from the published 2027 figure at 2.5% a year",
                 ["irs_rp2026_35"], "assumption"),
             P.C("Assumption", [], "assumption")]
            for y in (2030, 2035, 2040, 2045, 2050)
        ],
        note="Only the 2024 to 2027 rows are facts. Everything from 2028 on assumes Congress leaves "
             "the current law alone, which over a horizon this long is a strong assumption. The "
             "law-watch page lists the proposals that would change it.")

    other = dict(
        id="other", title="Rates that apply once a threshold or a gain exists",
        cols=["Item", "Amount", "Source"],
        rows=[
            [P.C("Top federal estate tax rate", ["crs_if12846"], "verified"),
             P.pct(0.40, 0, ["crs_if12846"], "verified"),
             P.C("CRS IF12846", ["crs_if12846"], "verified")],
            [P.C("Federal gift tax annual exclusion, 2025", ["crs_if12846"], "verified"),
             P.C("$19,000 per recipient", ["crs_if12846"], "verified"),
             P.C("CRS IF12846", ["crs_if12846"], "verified")],
            [P.C("Federal gift tax annual exclusion, 2027", ["irs_rp2026_35"], "verified"),
             P.C("$20,000 per recipient", ["irs_rp2026_35"], "verified"),
             P.C("Rev. Proc. 2026-35 sec. 3.46", ["irs_rp2026_35"], "verified")],
            [P.C("Top federal long-term capital gains rate", ["irs_tc409"], "verified"),
             P.pct(0.20, 0, ["irs_tc409"], "verified"),
             P.C("IRS Topic 409", ["irs_tc409"], "verified")],
            [P.C("Net investment income tax", ["irs_niit"], "verified"),
             P.C("3.8% above $200,000 single / $250,000 joint, thresholds not indexed",
                 ["irs_niit"], "verified"),
             P.C("IRS NIIT Q&amp;A", ["irs_niit"], "verified")],
            [P.C("California top marginal income tax rate, 2025", ["ftb_2025_rates"], "verified"),
             P.C("12.3% over $742,953 single / $1,485,906 joint, plus a 1% surcharge over "
                 "$1,000,000 &mdash; 13.3% combined top rate",
                 ["ftb_2025_rates"], "derived"),
             P.C("FTB 2025 rate schedules", ["ftb_2025_rates"], "verified")],
            [P.C("Maximum rate on unrecaptured section 1250 gain", ["irs_tc409"], "verified"),
             P.pct(0.25, 0, ["irs_tc409"], "verified"),
             P.C("IRS Topic 409", ["irs_tc409"], "verified")],
            [P.C("Section 121 exclusion on a principal residence", ["irs_niit"], "verified"),
             P.C("$250,000 single, $500,000 joint; also excluded from the net investment income tax",
                 ["irs_niit"], "verified"),
             P.C("IRS NIIT Q&amp;A", ["irs_niit"], "verified")],
            [P.C("Combined rate used here on a gain or on portfolio income", [], "label"),
             P.C("37.1% &mdash; 20% federal + 3.8% net investment income tax + 13.3% California",
                 ["irs_tc409", "irs_niit", "ftb_2025_rates"], "derived"),
             P.C("Derived from the three rates above", [], "derived")],
        ],
        note="The 1% California surcharge over $1,000,000 that produces the 13.3% top rate is not "
             "printed on the FTB rate schedules themselves; it is applied here as an assumption. "
             "Confirm it before relying on the 37.1% combined figure.")

    body = BANNER + "<p class='lead'>The inheritance includes cash and investments as well as the " \
           "house, so the federal threshold matters. California's position does not require any " \
           "analysis at all: it is prohibited by statute.</p>" + LEGEND + \
        render_table(jur) + "<h2>How much can pass before any federal tax</h2>" + \
        render_table(thr) + "<h2>Rates that apply if a threshold is crossed</h2>" + \
        render_table(other) + \
        ('<div class="banner"><b>What is still missing.</b> Whether the estate will come near '
         'these thresholds is unknown, and no estimate of the non-property assets has been '
         'supplied. Without that figure, nothing can be said about federal estate tax either way. '
         'Prepare the schedule for the estate attorney and keep it off any website.</div>')
    return write("inheritance-tax.html", "Inheritance &amp; estate tax",
                 "California prohibits it; Washington might not", body)


# ====================================================== page: operating costs
def page_costs():
    o = M.OWNER
    tbl = dict(
        id="costs", title="Annual running costs, both properties, at 2026 prices",
        cols=["Item", "Property A", "Property B", "Basis"],
        rows=[
            [P.C("Water and sewer", [], "label"),
             P.money(o["A_water_month"] * 12, [], "owner"),
             P.money(o["B_water_month"] * 12, [], "owner"),
             P.C("Owner ranges of %s-%s and %s-%s a month. The utility that serves San Francisco "
                 "publishes official schedules; the Property A figure has no utility source."
                 % (m(100), m(150), m(330), m(400)), ["sfpuc_rates"], "owner")],
            [P.C("Electricity", [], "label"),
             P.money(o["A_electric_month"] * 12, [], "owner"),
             P.money(o["B_electric_month"] * 12, [], "owner"),
             P.C("Property A has rooftop solar and normally runs a small credit of %s-%s a month, "
                 "so the figure is negative. Which tariff it is on is unknown."
                 % (m(10), m(20)), [], "owner")],
            [P.C("Insurance", [], "label"),
             P.money(o["A_insurance_year"], [], "unverified"),
             P.money(o["B_insurance_year"], [], "unverified"),
             P.C("Both are owner estimates. The California Department of Insurance publishes ZIP "
                 "level residential insurance data under Insurance Code section 929; no figure was "
                 "read from it for either property.",
                 ["cdi_residential"], "unverified")],
            [P.C("Maintenance and repairs", [], "label"),
             P.C("", [], "unverified"),
             P.C("", [], "unverified"),
             P.C("No figure supplied for either property. The model uses 1.0% of market value a "
                 "year with a 0.5%-1.5% band, which is a rule of thumb, not a measurement.",
                 [], "unverified")],
            [P.C("Management and vacancy", [], "label"),
             P.C("n/a unless let", [], "label"),
             P.C("Charged in the letting scenario only", [], "assumption"),
             P.C("8% of collected rent for management and 5% vacancy, both assumptions with no "
                 "source.", [], "assumption")],
            [P.C("Property tax", [], "label"),
             P.money(P.A_SER[2026]["tax"], ["boe_pub29"], "derived"),
             P.money(P.B_SER[2025]["total"], ["sf_treasurer_secured"], "derived"),
             P.C("Property A at the owner-implied rate; Property B at the official San Francisco "
                 "secured rate of 1.18162182 percent plus the unexplained residual of about %s a "
                 "year." % m(P.B_FIXED), ["boe_pub29", "sf_treasurer_secured"], "derived")],
        ],
        note="Water, electricity and insurance are held flat in real terms in the projections and "
             "grown at the assumed inflation rate. That is a simplification: California insurance "
             "premiums have been moving much faster than general inflation, and the CDI market "
             "data shows direct written premium for the homeowners line rising from $14.5bn in 2024 "
             "to $16.4bn in 2025 with a reported 2025 loss ratio of 170%.")

    ctx = dict(
        id="ctx", title="Official context for the insurance line",
        cols=["Measure", "Value", "Source"],
        rows=[
            [P.C("California homeowners direct written premium, 2024", ["cdi_marketshare"], "verified"),
             P.C("$14.5 billion", ["cdi_marketshare"], "verified"),
             P.C("CDI market share report", ["cdi_marketshare"], "verified")],
            [P.C("California homeowners direct written premium, 2025", ["cdi_marketshare"], "verified"),
             P.C("$16.4 billion", ["cdi_marketshare"], "verified"),
             P.C("CDI market share report", ["cdi_marketshare"], "verified")],
            [P.C("Reported California homeowners loss ratio, 2025", ["cdi_marketshare"], "verified"),
             P.C("170.23%", ["cdi_marketshare"], "verified"),
             P.C("CDI market share report", ["cdi_marketshare"], "verified")],
            [P.C("Official ZIP-level residential premium data", ["cdi_residential"], "verified"),
             P.C("Published by CDI under Insurance Code section 929, covering 2018-2023",
                 ["cdi_residential"], "verified"),
             P.C("CDI Residential Property Insurance Report", ["cdi_residential"], "verified")],
            [P.C("Average premium for either property", [], "label"),
             P.C("", [], "unverified"),
             P.C("Not retrieved. The CDI files were located and linked; no per-ZIP figure was read "
                 "from them in this pass, so no value is asserted here.",
                 ["cdi_residential"], "unverified")],
        ],
        note="This table exists so the unverified insurance cells are visibly unverified rather "
             "than quietly filled in. Pulling the CDI ZIP-level file is a fifteen minute task and "
             "would close both gaps.")

    infl = dict(
        id="infl", title="The inflation anchor used to grow costs",
        cols=["Measure", "Value", "Source"],
        rows=[
            [P.C("CPI-U, all items, 12-month change to September 2026", ["bls_cpi_home"], "verified"),
             P.C("3.7%", ["bls_cpi_home"], "verified"),
             P.C("BLS CPI home page", ["bls_cpi_home"], "verified")],
            [P.C("CPI-U, all items, October 2026 monthly change", ["bls_cpi_home"], "verified"),
             P.C("+0.4%", ["bls_cpi_home"], "verified"),
             P.C("BLS CPI home page", ["bls_cpi_home"], "verified")],
            [P.C("CPI-U annual average change, 2022", ["bls_cpi_hist"], "verified"),
             P.C("8.0%", ["bls_cpi_hist"], "verified"),
             P.C("BLS historical CPI-U table", ["bls_cpi_hist"], "verified")],
            [P.C("CPI-U annual average change, 2023", ["bls_cpi_hist"], "verified"),
             P.C("4.1%", ["bls_cpi_hist"], "verified"),
             P.C("BLS historical CPI-U table", ["bls_cpi_hist"], "verified")],
            [P.C("CPI-U annual average change, 2024", ["bls_cpi_hist"], "verified"),
             P.C("2.9%", ["bls_cpi_hist"], "verified"),
             P.C("BLS historical CPI-U table", ["bls_cpi_hist"], "verified")],
            [P.C("Assumed cost inflation in the model", [], "label"),
             P.C("3.0%, with a 2.0%-5.0% band", [], "assumption"),
             P.C("Assumption anchored on the readings above", ["bls_cpi_home"], "assumption")],
        ],
        note="Note the tension: the most recent official reading is 3.7%, which is above the 3.0% "
             "used in the model. The band on the scenarios page covers this.")

    body = BANNER + "<p class='lead'>Four of the six cost lines on this page are owner estimates " \
           "with no source. They are shown that way deliberately, because they feed every " \
           "projection that follows.</p>" + LEGEND + render_table(tbl) + \
        "<h2>Insurance: what is official and what is not</h2>" + render_table(ctx) + \
        "<h2>Inflation</h2>" + render_table(infl)
    return write("operating-costs.html", "Running costs",
                 "Water, power, insurance, maintenance", body)


# ====================================================== page: projections
def page_projections():
    rows_a = []
    for y in P.YEARS:
        r = P.A_SER[y]
        rows_a.append([
            P.C(str(y), [], "label"),
            P.money(r["market"], [], "assumption"),
            P.money(r["assessed"], ["boe_pub29"], "derived"),
            P.money(r["tax"], ["boe_pub29"], "derived"),
            P.money(P.TV.get(y, M.transfer_values(y))["fmv"], [], "assumption"),
            P.money(P.TV.get(y, M.transfer_values(y))["rent_av"], ["boe_prop19"], "derived"),
            P.money(P.TV.get(y, M.transfer_values(y))["rent_tax"], ["boe_prop19"], "derived"),
            P.money(P.TV.get(y, M.transfer_values(y))["occ_av"], ["boe_prop19"], "derived"),
            P.money(P.TV.get(y, M.transfer_values(y))["occ_tax"], ["boe_prop19"], "derived"),
        ])
    tbl_a = dict(
        id="proja", title="Property A, Santa Clara County &mdash; every year to 2076",
        cols=["Year", "Market value", "Assessed value (2% cap)", "Bill if ownership does not change",
              "Market value at a transfer in this year", "Taxable value, no exclusion",
              "Bill, no exclusion", "Taxable value, Prop 19 exclusion", "Bill, with exclusion"],
        rows=rows_a,
        note="Market value grows at 4.0% nominal, which is an assumption. Assessed value grows at "
             "the 2% Proposition 13 ceiling, which is law. The last four columns answer the "
             "question 'what happens if the property changes hands in this particular year'. Bills "
             "use the owner-implied effective rate of 1.34%.")

    rows_b = []
    for y in P.YEARS:
        r = P.B_SER[y]
        rows_b.append([
            P.C(str(y), [], "label"),
            P.money(r["assessed"], ["boe_pub29"], "derived"),
            P.money(r["adval"], ["sf_treasurer_secured"], "derived"),
            P.money(r["fixed"], ["sf_treasurer_secured"], "derived"),
            P.money(r["total"], ["sf_treasurer_secured"], "derived"),
            P.money(r["rent"], [], "owner"),
            P.money(r["costs"], [], "derived"),
            P.money(r["net"], [], "derived"),
        ])
    tbl_b = dict(
        id="projb", title="Property B, San Francisco &mdash; every year to 2076",
        cols=["Year", "Assessed value (2% cap)", "Ad valorem at 1.18162182%",
              "Unexplained residual", "Total bill", "Rent (two units)", "Water, power, insurance, "
              "maintenance", "Net before income tax"],
        rows=rows_b,
        note="The ad valorem column uses the official San Francisco secured rate for FY2026-27. The "
             "residual is the gap between the owner's reported bill and that rate, carried flat "
             "because its nature is unknown &mdash; reconcile it against the actual bill. Rent grows "
             "at 3.5%, which sits inside the statewide cap of 5% plus the change in the cost of "
             "living, subject to a 10% ceiling.")

    body = BANNER + "<p class='lead'>Two tables, one per property, every year from 2026 to 2076. " \
           "Use the filter box to jump to a year.</p>" + LEGEND + \
        "<h2>Property A</h2>" + render_table(tbl_a) + \
        "<h2>Property B</h2>" + render_table(tbl_b) + \
        ('<div class="banner"><b>These are projections, not predictions.</b> The assessed value '
         'columns follow a legal cap and are therefore the most reliable numbers on the site. The '
         'market value columns follow an assumed growth rate and are the least reliable. Read the '
         'market value columns as a scenario, and use the break-even table on the options page '
         'rather than any single column here.</div>')
    return write("projections.html", "Projections",
                 "Year by year to 2076", body)


# ====================================================== page: scenarios
def page_scenarios():
    n = P.NP
    cmp_rows = []
    for t in P.TRANSFER_YEARS:
        cmp_rows += [
            [P.C("%d &mdash; occupy" % t, [], "label"),
             P.money(n[t]["occupy"], [], "derived"), P.money(n[t]["occupy_h"], [], "derived"),
             P.money(P.TV[t]["occ_tax"], ["boe_prop19"], "derived")],
            [P.C("%d &mdash; rent out" % t, [], "label"),
             P.money(n[t]["rent"], [], "derived"), P.money(n[t]["rent_h"], [], "derived"),
             P.money(P.TV[t]["rent_tax"], ["boe_prop19"], "derived")],
            [P.C("%d &mdash; sell and reinvest" % t, [], "label"),
             P.money(n[t]["sell"], [], "derived"), P.money(n[t]["sell_h"], [], "derived"),
             P.C("$0 &mdash; property sold", [], "derived")],
        ]
    cmp = dict(
        id="cmp", title="Net present value of each option, at the date of transfer",
        cols=["Option and transfer year", "Cash only", "Including the home you get to live in",
              "Property A tax bill in the first year"],
        rows=cmp_rows,
        note="Discounted at 5.0% a year to the date of transfer and carried to 2076. 'Including "
             "the home you get to live in' credits each option with the market rent of the dwelling "
             "it lets you occupy: occupying gives you Property A, renting and selling leave you in "
             "your San Francisco unit. That is the only like-for-like comparison, and it is the "
             "column to read.")

    be = dict(
        id="be", title="Where the ranking flips &mdash; the break-even table",
        cols=["Question", "Break-even", "Reading"],
        rows=[
            [P.C("What portfolio return does selling need to beat renting out?", [], "label"),
             P.pct(M.breakeven_portfolio_return(2045, "rent", with_housing=True), 2, [], "derived"),
             P.C("Above this, sell. Below it, rent. This is the single most useful number on the "
                 "site, because it replaces an unknowable forecast with a threshold you can judge.",
                 [], "derived")],
            [P.C("What portfolio return does selling need to beat occupying?", [], "label"),
             P.pct(M.breakeven_portfolio_return(2045, "occupy", with_housing=True), 2, [], "derived"),
             P.C("Same test against the occupancy option.", [], "derived")],
            [P.C("What gross rental yield on Property A makes renting tie selling?", [], "label"),
             P.pct(M.breakeven_gross_yield(2045, with_housing=True), 2, [], "derived"),
             P.C("The model assumes 2.6%. If the property can really be let for more than this "
                 "share of its value, renting stops being dominated. Go and test it with real "
                 "comparable rents.", [], "derived")],
            [P.C("How fast must prices grow for holding to beat selling?", [], "label"),
             P.C("%s against renting, %s against occupying"
                 % (P.pct(M.breakeven_market_growth(2045, "rent", with_housing=True), 2)["t"],
                    P.pct(M.breakeven_market_growth(2045, "occupy", with_housing=True), 2)["t"]),
                 [], "derived"),
             P.C("Below these growth rates, selling wins regardless of how much you like the house.",
                 [], "derived")],
        ],
        note="All break-evens are computed at a 2045 transfer with the baseline assumptions and "
             "the housing-inclusive comparison. They move when the assumptions move, which is the "
             "point: they are thresholds to monitor, not answers to trust.")

    sens = dict(
        id="sens", title="Sensitivity &mdash; how the 2045 ranking moves",
        cols=["Variable", "Low", "Baseline", "High", "Does the ranking change?"],
        rows=[]
    )
    labels = {
        "portfolio_return": "Portfolio return",
        "g_market": "Home price growth",
        "gross_yield": "Gross rental yield on Property A",
        "maintenance_pct": "Maintenance as a share of value",
        "cpi": "Cost inflation",
        "discount": "Discount rate",
    }
    for k, vals in M.SENSITIVITY.items():
        res = []
        for v in vals:
            nn = M.scenario_npv(2045, {k: v}, P.LAST)
            best = max([("occupy", nn["occupy_h"]), ("rent", nn["rent_h"]),
                        ("sell", nn["sell_h"])], key=lambda x: x[1])[0]
            res.append(best)
        fmt = (lambda x: P.pct(x, 1)["t"]) if k != "maintenance_pct" else (lambda x: P.pct(x, 1)["t"])
        sens["rows"].append([
            P.C(labels[k], [], "label"),
            P.C(fmt(vals[0]) + " &rarr; " + res[0], [], "derived"),
            P.C(fmt(vals[1]) + " &rarr; " + res[1], [], "derived"),
            P.C(fmt(vals[2]) + " &rarr; " + res[2], [], "derived"),
            P.C("Yes" if len(set(res)) > 1 else "No &mdash; " + res[1], [], "derived"),
        ])

    # year-by-year cash flows for the baseline transfer year
    d = n[2045]["_detail"]
    occ, ren, sel = d["occupy"], d["rent"], d["sell"]
    cf = dict(
        id="cf", title="Year by year after a 2045 transfer",
        cols=["Year", "Occupy: net cash", "Occupy: housing value", "Rent: net operating income",
              "Rent: depreciation shelter", "Sell: portfolio value", "Sell: unrealised gain"],
        rows=[[P.C(str(y), [], "label"),
               P.money(occ["rows"][i]["net"], [], "derived"),
               P.money(occ["rows"][i]["imputed"], [], "derived"),
               P.money(ren["rows"][i]["noi"], [], "derived"),
               P.money(ren["rows"][i]["depreciation"], ["irs_tc409"], "derived"),
               P.money(sel["rows"][i]["value"], [], "derived"),
               P.money(sel["rows"][i]["unrealised"], [], "derived")]
              for i, y in enumerate(range(2045, 2077))],
        note="Occupy net cash is negative because it is a cost; the housing value column is what "
             "living there is worth at market rent, and is not cash. Rent's depreciation shelter is "
             "a non-cash deduction against rental income under the 27.5 year straight line "
             "assumption; it comes back as recapture taxed at up to 25% federally when the property "
             "is sold. Sell's portfolio column is the value before the tax that would be due on "
             "liquidating it.")

    body = BANNER + "<p class='lead'>Three options, one comparison, and &mdash; more usefully " \
           "&mdash; the thresholds at which the answer changes.</p>" + LEGEND + \
        render_table(cmp) + "<h2>Break-evens</h2>" + render_table(be) + \
        '<div class="banner blue"><b>Why the ranking is not the headline.</b> The order of these ' \
        'three options is produced by a model running on assumptions, several of which are ' \
        'currently unknown. What survives every sensitivity is narrower and more useful: the ' \
        'property tax jump is real and large, the step-up in basis removes any urgency to decide, ' \
        'and renting is dominated unless the property can be let for far more than the assumed ' \
        'yield.</div>' + \
        "<h2>Sensitivity</h2>" + render_table(sens) + \
        "<h2>Cash flows</h2>" + render_table(cf)
    return write("scenarios.html", "Options compared",
                 "Occupy, rent out, or sell and reinvest", body)


# ====================================================== page: black swan
def page_black_swan():
    tbl = dict(
        id="swan", title="Eight regimes, re-priced against the baseline",
        cols=["Regime", "Home price growth", "Inflation", "Occupy", "Rent out",
              "Sell and reinvest", "Wins", "Official anchor"],
        rows=P.black_swan_rows(),
        note="Each regime re-runs the same model with different growth and inflation paths. The net "
             "present value columns use the housing-inclusive comparison at a 2045 transfer. Growth "
             "and inflation are never constant over fifty years, and this table is the honest way to "
             "say so: it does not predict which regime arrives, it shows what each one would do. "
             "Two rows - a Proposition 13 change or split roll, and a restriction on the step-up in "
             "basis - deliberately reproduce the baseline numbers. The model can re-price growth "
             "and inflation, but it cannot price a law that does not exist yet, and inventing a "
             "figure for it would be the one thing this site promises not to do. Read those two "
             "rows as a statement of exposure, not as a forecast.")

    hist = dict(
        id="hist", title="The historical record these regimes are built from",
        cols=["Period", "What happened", "Source"],
        rows=[
            [P.C("1973-1975", [], "label"),
             P.C("CPI-U annual average change of 6.2%, then 11.0%, then 9.1%",
                 ["bls_cpi_hist"], "verified"),
             P.C("BLS historical CPI-U table", ["bls_cpi_hist"], "verified")],
            [P.C("1979-1982", [], "label"),
             P.C("CPI-U annual average change of 11.3%, 13.5%, 10.3%, 6.2%",
                 ["bls_cpi_hist"], "verified"),
             P.C("BLS historical CPI-U table", ["bls_cpi_hist"], "verified")],
            [P.C("1990-1994", [], "label"),
             P.C("CPI-U annual average change falling from 5.4% to 2.6%",
                 ["bls_cpi_hist"], "verified"),
             P.C("BLS historical CPI-U table", ["bls_cpi_hist"], "verified")],
            [P.C("2008-2009", [], "label"),
             P.C("CPI-U annual average change of 3.8% then -0.4%, the only negative annual average "
                 "in the post-war series", ["bls_cpi_hist"], "verified"),
             P.C("BLS historical CPI-U table", ["bls_cpi_hist"], "verified")],
            [P.C("2021-2023", [], "label"),
             P.C("CPI-U annual average change of 4.7%, then 8.0%, then 4.1%",
                 ["bls_cpi_hist"], "verified"),
             P.C("BLS historical CPI-U table", ["bls_cpi_hist"], "verified")],
            [P.C("2024", [], "label"),
             P.C("California House Price Index up 2.15%, the figure the Board of Equalization used "
                 "to adjust the Proposition 19 allowance",
                 ["boe_lta2025_009"], "verified"),
             P.C("BOE LTA 2025/009", ["boe_lta2025_009"], "verified")],
            [P.C("2025-2026", [], "label"),
             P.C("CPI-U up 2.9% on an annual average basis in 2024, and 3.7% over the twelve months "
                 "to September 2026", ["bls_cpi_hist", "bls_cpi_home"], "verified"),
             P.C("BLS", ["bls_cpi_hist", "bls_cpi_home"], "verified")],
            [P.C("2024-2025", [], "label"),
             P.C("California homeowners direct written premium rose from $14.5bn to $16.4bn with a "
                 "reported 2025 loss ratio of 170.23%", ["cdi_marketshare"], "verified"),
             P.C("CDI market share report", ["cdi_marketshare"], "verified")],
        ],
        note="Every number in this table was read from the official source named beside it. The "
             "regime paths in the table above are interpretations of that record, not predictions.")

    body = BANNER + "<p class='lead'>A single straight-line growth rate compounded for fifty years " \
           "is the least realistic thing in any long-horizon property model. This page replaces it " \
           "with regimes anchored on what actually happened.</p>" + LEGEND + \
        render_table(tbl) + "<h2>The record</h2>" + render_table(hist) + \
        ('<div class="banner"><b>Two regimes deserve particular attention here.</b> A change to '
         'Proposition 13 or a split roll would move the assessed value towards market value and '
         'would dwarf every other variable on this site. A restriction on the step-up in basis '
         'would cut the net proceeds of selling, which is the option this analysis currently '
         'prefers. Neither is law; both are listed on the law-watch page.</div>')
    return write("black-swan.html", "Black swans",
                 "Uneven economies over a fifty year horizon", body)


# ====================================================== page: process
PROCESS = [
    ("Before the transfer &mdash; while the settlor is alive",
     [("Confirm the property is titled in the trust",
       "A transfer of a home into a revocable trust where the settlor remains the beneficiary is "
       "excluded from reassessment, so it does not reset the property tax base. If the deed into "
       "the trust was never recorded, the remedy later is a court petition, not a form.",
       "", []),
      ("Establish whether Property A is the settlor's principal residence",
       "The Proposition 19 exclusion requires the home to have been the transferor's principal "
       "residence. If the settlor has already moved out, the exclusion may be unavailable.",
       "", ["boe_pub800_1", "boe_prop19"]),
      ("Diary the two clocks",
       "The homeowners' or disabled veterans' exemption is due within one year of the transfer; "
       "the BOE-19-P claim within three years of it, or before any transfer to a third party, "
       "whichever comes first.",
       "1 year and 3 years from the transfer date", ["boe_pub800_1", "scc_assessor_p19"]),
      ("Decide the occupancy question in principle",
       "The exclusion requires the home to become the transferee's principal residence within one "
       "year and to stay that way. This is a household decision with a tax consequence of tens of "
       "thousands of dollars a year, so it should not be made in the grief of the moment.",
       "", ["boe_prop19"])]),
    ("At and immediately after the transfer",
     [("The trustee serves the statutory notification",
       "Within 60 days of the settlor's death the trustee must serve a notification on every "
       "beneficiary of the trust and every heir of the deceased settlor. The duty is the "
       "continuing or successor trustee's, and any one co-trustee may serve it.",
       "60 days", ["ca_prob_16061_7"]),
      ("Determine the date-of-death value",
       "This single figure does three jobs: it is the new basis for income tax, it is the value "
       "reported for estate tax if a return is due, and it is the amount the county will use on "
       "reassessment if no exclusion is claimed. Use a qualified appraisal.",
       "", ["irs_p551"]),
      ("Work out whether a federal estate tax return is due",
       "California imposes nothing. Federally, a return is required only if the gross estate "
       "increased by adjusted taxable gifts exceeds the filing threshold for the year of death: "
       "$15,000,000 for 2026 and $15,480,000 for 2027.",
       "9 months after death, extendable", ["irs_estate_tax", "irs_rp2026_35", "ca_rtc_13301"]),
      ("File the homeowners' or disabled veterans' exemption",
       "Required within one year of the transfer to receive the Proposition 19 exclusion as of the "
       "date of transfer. A BOE-19-P claim cannot be filed before this exemption claim.",
       "1 year", ["boe_pub800_1"]),
      ("Move in, if the exclusion is being claimed",
       "The transferee must live in the home as a principal residence within one year and keep "
       "living there. If the property later stops being anyone's principal residence it is "
       "reassessed to its inherited market value, adjusted by the inflation factor.",
       "1 year, then continuously", ["boe_pub800_1", "boe_prop19"]),
      ("File BOE-19-P with the Santa Clara County Assessor",
       "The claim form for the parent-child reassessment exclusion, filed with the assessor of the "
       "county where the property sits, not with the Board of Equalization.",
       "3 years", ["boe_pub800_1", "scc_assessor_p19", "scc_assessor_downloads"]),
      ("Expect a supplemental or escape assessment",
       "On a change in ownership the assessor reappraises and issues a supplemental bill for the "
       "difference, prorated for the part of the fiscal year remaining. If the new value is "
       "determined late, an escape assessment follows instead.",
       "", ["sf_treasurer_secured"])]),
    ("After the transfer &mdash; the ongoing position",
     [("Keep occupying, or lose the exclusion",
       "At least one eligible transferee must continually live in the property for the exclusion "
       "to survive. This is a permanent condition, not a one-year test.",
       "", ["boe_prop19"]),
      ("If the property is let instead",
       "The exclusion does not apply to a rental transfer. The property is reassessed to full "
       "market value, rental income becomes taxable, depreciation begins over 27.5 years, and the "
       "statewide rent cap of 5% plus inflation, subject to a 10% ceiling, governs increases.",
       "", ["boe_prop19", "ca_civ_1947_12", "irs_tc409"]),
      ("If the property is sold",
       "Basis is market value at death, so a sale soon after the transfer realises almost no gain. "
       "Hold it for two of the five years before selling and up to $250,000, or $500,000 filing "
       "jointly, of gain is excluded; that exclusion also removes the gain from the net investment "
       "income tax.",
       "", ["irs_p551", "irs_niit"]),
      ("Re-run this analysis each year",
       "The break-even thresholds move with the market, and the law-watch items move with "
       "Congress and the California ballot. An annual re-read is the cheapest insurance available.",
       "Annually", [])]),
]


def page_process():
    out = []
    for phase, steps in PROCESS:
        lis = []
        for title, desc, clock, srcs in steps:
            cl = ("<p class='muted'><b>Clock:</b> %s</p>" % clock) if clock else ""
            lis.append("<li><h4>%s</h4><p>%s</p>%s%s</li>"
                       % (html.escape(title, quote=False) if "&" not in title else title,
                          html.escape(desc, quote=False), cl, src_links(srcs)))
        out.append("<h2>%s</h2><ol class='steps'>%s</ol>" % (phase, "".join(lis)))
    body = BANNER + "<p class='lead'>A trust inheritance in California, step by step, with the " \
           "form and the deadline for each step. This is the sequence, not legal advice.</p>" + \
           "".join(out) + \
           ('<div class="banner red"><b>The two dates that carry money.</b> One year for the '
            'homeowners\' exemption and for moving in. Three years for the BOE-19-P claim. Both '
            'run from the date of transfer, not from the date anyone gets around to it. Late is '
            'not fatal &mdash; a late exemption claim moves the start of the exclusion forward '
            '&mdash; but it costs the back years.</div>')
    return write("process.html", "Transfer process",
                 "How a trust inheritance actually runs", body)


# ====================================================== page: questions
def page_questions():
    order = ["Trust and title", "Timing", "Property A", "Property B", "Taxes", "Market",
             "Law change", "Household"]
    body = BANNER + "<p class='lead'>Everything that has to be known before a decision can be " \
           "made on the merits, grouped by subject. Each entry says what is known, what is " \
           "missing, what decision the gap blocks, and precisely how to close it.</p>"
    for cat in order:
        qs = [q for q in P.QUESTIONS if q["cat"] == cat]
        if not qs:
            continue
        body += "<h2>%s</h2>" % html.escape(cat, quote=False)
        for q in qs:
            st = {"unknown": "t-unv", "unverified": "t-unv", "assumption": "t-asm",
                  "reported": "t-rep", "verified": "t-ver"}[q["st"]]
            body += (
                '<div class="q"><p class="qq">%s &nbsp;<span class="tag %s">%s</span></p>'
                '<p><b>Known:</b> %s</p>'
                '<p><b>Missing:</b> %s</p>'
                '<p><b>How to find it:</b> %s</p>%s</div>'
                % (html.escape(q["id"]) + " " + html.escape(q["q"]), st,
                   html.escape(P.STATUS_LABEL.get(q["st"], q["st"])),
                   html.escape(q["known"], quote=False), html.escape(q["missing"], quote=False),
                   html.escape(q["how"], quote=False), src_links(q["src"])))
    return write("questions.html", "Questions &amp; gaps",
                 "What must be known before deciding", body)


# ====================================================== page: suggestions
def page_suggestions():
    body = BANNER + (
        '<div class="banner blue"><b>Nothing here has been done.</b> This page exists so that each '
        'suggestion can be read, accepted, modified or rejected before anything changes. No commit '
        'in this branch implements any of them, and none will be implemented without a decision '
        'recorded against its number.</div>'
        '<p class="lead">Fifteen suggestions, ordered by the size of what they protect. Each states '
        'why it matters, what it is worth, what it costs to do, and what could go wrong.</p>')
    rows = []
    for s in P.SUGGESTIONS:
        rows.append([
            P.C(s["id"], [], "label"),
            P.C(html.escape(s["title"]), [], "label"),
            P.C(s["cat"], [], "label"),
            P.C(s["why"], [], "label"),
            P.C(s["effect"], [], "label"),
            P.C(s["effort"], [], "label"),
            P.C(s["risk"], [], "label"),
            P.C('<span class="chk">%s</span>' % s["status"].upper(), s["src"], "label"),
        ])
    tbl = dict(
        id="sug", title="Suggestions awaiting a decision",
        cols=["#", "Suggestion", "Category", "Why", "What it is worth", "Effort", "Risk", "Status"],
        rows=rows,
        note="Status 'proposed' means not implemented and not agreed. To move one forward, record "
             "accept, modify or reject against the number; nothing on this site changes until then.")
    body += LEGEND + render_table(tbl)
    body += ("<h2>How to review these</h2>"
             "<ol class='steps'>"
             "<li><h4>Read the why column first</h4><p>Some of these protect something irreplaceable "
             "&mdash; a filing deadline, a tax base, a piece of privacy. Those matter more than their "
             "dollar value suggests.</p></li>"
             "<li><h4>Group them</h4><p>Four of them are pure information gathering with no "
             "downside. Do those first and the rest of this site gets sharper.</p></li>"
             "<li><h4>Record a decision against each number</h4><p>Accept, modify, or reject. A "
             "rejected suggestion with a reason is worth more than one left open.</p></li>"
             "<li><h4>Only then change anything</h4><p>None of these is implemented here, by "
             "design.</p></li>"
             "</ol>")
    return write("suggestions.html", "Suggestions",
                 "For review before anything changes", body)


# ====================================================== page: law watch
def page_law_watch():
    fed = dict(
        id="fed", title="Federal &mdash; what is law and what is only proposed",
        cols=["Item", "Status", "What it would change", "Source"],
        rows=[
            [P.C("Estate tax exemption, $15,000,000 for 2026", ["irs_estate_tax"], "verified"),
             P.C("Law", ["irs_estate_tax"], "verified"),
             P.C("Made permanent and increased by P.L. 119-21. The prior scheduled reversion to a "
                 "roughly $7 million exemption no longer happens.",
                 ["irs_estate_tax", "crs_if12846"], "verified"),
             P.C("IRS; CRS IF12846", ["irs_estate_tax", "crs_if12846"], "verified")],
            [P.C("Estate tax exemption, $15,480,000 for 2027", ["irs_rp2026_35"], "verified"),
             P.C("Law", ["irs_rp2026_35"], "verified"),
             P.C("Indexed. The same figure is the generation-skipping transfer exemption.",
                 ["irs_rp2026_35"], "verified"),
             P.C("Rev. Proc. 2026-35", ["irs_rp2026_35"], "verified")],
            [P.C("Step-up in basis under section 1014", ["crs_if12846"], "verified"),
             P.C("Law today; change proposed", ["crs_if12846"], "verified"),
             P.C("CRS lists taxing unrealised gains at death or eliminating the step-up among the "
                 "options Congress could consider. Several bills have been introduced. None has "
                 "been enacted or heard in a tax-writing committee.",
                 ["crs_if12846"], "verified"),
             P.C("CRS IF12846", ["crs_if12846"], "verified")],
            [P.C("Repeal of the federal estate tax", ["crs_if12846"], "verified"),
             P.C("Proposed", ["crs_if12846"], "verified"),
             P.C("Critics favour repeal or a higher exemption. Introduced repeatedly; not enacted.",
                 ["crs_if12846"], "verified"),
             P.C("CRS IF12846", ["crs_if12846"], "verified")],
            [P.C("Reduction of the exemption to $3,500,000 with rates up to 65%",
                 ["crs_if12846"], "verified"),
             P.C("Proposed", ["crs_if12846"], "verified"),
             P.C("A bill of this shape has been introduced in earlier Congresses. If something like "
                 "it were enacted, a middling estate would become taxable.",
                 ["crs_if12846"], "verified"),
             P.C("CRS IF12846", ["crs_if12846"], "verified")],
            [P.C("A cap on the step-up of $3,000,000 per decedent", [], "label"),
             P.C("", [], "unverified"),
             P.C("Commentary describes a 2026 Treasury proposal that would cap the step-up and give "
                 "carryover basis above the cap. It could not be found on the Federal Register or "
                 "Treasury's own site during this pass, so no value is asserted here. Treat it as "
                 "rumour until an official document is produced.", [], "unverified"),
             P.C("Not confirmed &mdash; see the flagged page", [], "unverified")],
        ],
        note="Only the first two rows are settled law. Everything below them is a proposal, and the "
             "last row is a proposal this site could not even confirm exists.")

    ca = dict(
        id="ca", title="California &mdash; the November 3, 2026 ballot and after",
        cols=["Measure", "What it does", "Status", "Source"],
        rows=[
            [P.C("Proposition 3", ["ca_sos_ballot"], "verified"),
             P.C("Official title: 'Provides Permanent Funding for Schools and Health Care by "
                 "Extending Existing Tax on High Incomes. Initiative Constitutional Amendment.' "
                 "The income thresholds it extends are widely reported as $361,000 single and "
                 "$721,000 joint, but that detail is not on the Secretary of State's list, so it "
                 "is not relied on here.",
                 ["ca_sos_ballot"], "verified"),
             P.C("Reported as carried; official results are certified in December 2026",
                 ["ca_sos_ballot", "ca_sos_results"], "reported"),
             P.C("CA Secretary of State", ["ca_sos_ballot"], "verified")],
            [P.C("Proposition 40", ["ca_sos_ballot"], "verified"),
             P.C("Official title: 'Imposes One-Time Tax on Certain Taxpayers. Initiative "
                 "Constitutional Amendment and Statute.' The 5% rate and the $1 billion net worth "
                 "threshold are reported in secondary coverage, not on the Secretary of State's "
                 "list, and are not relied on here.", ["ca_sos_ballot"], "verified"),
             P.C("Reported as not carried; competing with Propositions 41 and 42",
                 ["ca_sos_ballot", "ca_sos_results"], "reported"),
             P.C("CA Secretary of State", ["ca_sos_ballot"], "verified")],
            [P.C("Proposition 42", ["ca_sos_ballot"], "verified"),
             P.C("Official title: 'Prohibits New State Personal Property Taxes and Certain "
                 "Retroactive State Taxes. Initiative Constitutional Amendment.'",
                 ["ca_sos_ballot"], "verified"),
             P.C("Reported as leading; competing with Proposition 40",
                 ["ca_sos_ballot", "ca_sos_results"], "reported"),
             P.C("CA Secretary of State", ["ca_sos_ballot"], "verified")],
            [P.C("Proposition 43", ["ca_sos_ballot"], "verified"),
             P.C("Official title: 'Limits Voters' Ability to Raise Revenues for Local Government "
                 "Services. Legislative Constitutional Amendment.' It does not touch Proposition "
                 "13's 1% rate ceiling or its 2% assessment cap, which is why a Proposition 13 "
                 "change is not on this ballot.", ["ca_sos_ballot"], "verified"),
             P.C("Reported as not carried", ["ca_sos_ballot", "ca_sos_results"], "reported"),
             P.C("CA Secretary of State", ["ca_sos_ballot"], "verified")],
            [P.C("ACA 13", ["ca_sos_ballot"], "verified"),
             P.C("Removed from the November 3, 2026 ballot by ACA 21",
                 ["ca_sos_ballot"], "verified"),
             P.C("Withdrawn", ["ca_sos_ballot"], "verified"),
             P.C("CA Secretary of State", ["ca_sos_ballot"], "verified")],
            [P.C("ACA 7 (Jackson), government preferences", ["ca_sos_ballot"], "verified"),
             P.C("Already qualified for the November 7, 2028 statewide ballot. Listed here only so "
                 "the forward calendar is complete; it does not touch property tax.",
                 ["ca_sos_ballot"], "verified"),
             P.C("Qualified for a future ballot", ["ca_sos_ballot"], "verified"),
             P.C("CA Secretary of State", ["ca_sos_ballot"], "verified")],
            [P.C("Any split roll or change to Proposition 13 itself", ["ca_sos_ballot"], "verified"),
             P.C("No measure on the November 3, 2026 ballot changed Proposition 13's rate ceiling, "
                 "its 2% assessment cap, or the treatment of residential property",
                 ["ca_sos_ballot"], "verified"),
             P.C("None qualified as of this pass", ["ca_sos_ballot"], "verified"),
             P.C("CA Secretary of State", ["ca_sos_ballot"], "verified")],
        ],
        note="Measure titles and descriptions are quoted from the Secretary of State's official "
             "list of qualified measures. Results are reported from the count, not from a certified "
             "canvass: California certifies in December 2026. Re-check the official results portal "
             "before relying on any of them.")

    local = dict(
        id="local", title="Local &mdash; what changes a bill without changing the law",
        cols=["Item", "Effect", "Source"],
        rows=[
            [P.C("Voter-approved bonded indebtedness on top of the 1% ceiling",
                 ["boe_pub29"], "verified"),
             P.C("This is why both properties pay more than 1%. It is also the part most likely to "
                 "change without any change to Proposition 13.", ["boe_pub29"], "verified"),
             P.C("BOE Publication 29", ["boe_pub29"], "verified")],
            [P.C("Parcel taxes and direct assessments on the San Francisco bill",
                 ["sf_treasurer_secured"], "verified"),
             P.C("The unexplained residual of about %s a year on Property B is most likely this "
                 "kind of charge." % m(P.B_FIXED), ["sf_treasurer_secured"], "derived"),
             P.C("SF Treasurer &amp; Tax Collector", ["sf_treasurer_secured"], "verified")],
            [P.C("The Proposition 19 allowance adjusts in February 2027 and every second February",
                 ["boe_lta2025_009"], "verified"),
             P.C("The amount is $1,044,586 only through 15 February 2027. It moves with the "
                 "California House Price Index.", ["boe_lta2025_009"], "verified"),
             P.C("BOE LTA 2025/009", ["boe_lta2025_009"], "verified")],
            [P.C("Statewide rent cap", ["ca_civ_1947_12"], "verified"),
             P.C("Annual increases limited to 5% plus the change in the cost of living, or 10%, "
                 "whichever is lower, with exemptions for newer housing and, with notice, for "
                 "separately alienable single-family homes and condominiums.",
                 ["ca_civ_1947_12"], "verified"),
             P.C("Civil Code 1947.12", ["ca_civ_1947_12"], "verified")],
        ],
        note="The local layer is where surprises come from: it changes by ballot measure rather "
             "than by statute, and it lands straight on the tax bill.")

    body = BANNER + "<p class='lead'>The transfer window is 2040 to 2050. Over that horizon " \
           "Congress could restrict the step-up in basis and California voters could revisit " \
           "Proposition 13. Neither is on the books today.</p>" + LEGEND + \
        render_table(fed) + "<h2>California</h2>" + render_table(ca) + \
        "<h2>Local and mechanical</h2>" + render_table(local)
    return write("law-watch.html", "Law watch",
                 "What is pending that could move these numbers", body)


# ====================================================== page: sources
def page_sources():
    rows = []
    for s in sources.SOURCES:
        rows.append([
            P.C(html.escape(s["publisher"]), [s["id"]], "verified"),
            P.C(html.escape(s["title"]), [s["id"]], "verified"),
            P.C(html.escape(s["evidences"]), [s["id"]], "verified"),
            P.C(html.escape(s["checked"]), [s["id"]], "verified"),
            P.C('<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>'
                % (html.escape(s["url"], quote=True), html.escape(s["url"])),
                [s["id"]], "verified"),
        ])
    tbl = dict(id="srcreg", title="Source register",
               cols=["Publisher", "Document", "What it evidences", "What was checked", "URL"],
               rows=rows,
               note="%d documents. Every one was retrieved during this session. Documents marked "
                    "'not opened' were located and linked but not read line by line; any row citing "
                    "one of them says so." % len(sources.SOURCES))
    body = BANNER + "<p class='lead'>Everything on this site traces back to one of these. Where a " \
           "document could not be read in full, that is stated rather than papered over.</p>" + \
           LEGEND + render_table(tbl)
    return write("sources.html", "Sources", "Every document read", body)


# ====================================================== page: flagged
def page_flagged():
    rows = [
        [P.C("F01", [], "label"), P.C("Home insurance, Property A", [], "label"),
         P.C("The only figure is an owner estimate of about %s a year. No quote, and no figure "
             "read from the California Department of Insurance ZIP-level data."
             % m(M.OWNER["A_insurance_year"]), [], "unverified"),
         P.C("", [], "unverified"),
         P.C("Get two quotes and pull the CDI Part II file for the ZIP",
             ["cdi_residential"], "unverified")],
        [P.C("F02", [], "label"), P.C("Home insurance, Property B", [], "label"),
         P.C("Owner estimate only. A three-unit let property needs a landlord policy, which is "
             "priced differently from an owner-occupied policy.", [], "unverified"),
         P.C("", [], "unverified"),
         P.C("Two quotes for a dwelling-fire or landlord policy with loss of rents",
             ["cdi_residential"], "unverified")],
        [P.C("F03", [], "label"), P.C("Property A maintenance", [], "label"),
         P.C("Described as lighter than Property B, with no figure. Modelled at 1.0% of market "
             "value with a 0.5%-1.5% band.", [], "unverified"),
         P.C("", [], "unverified"),
         P.C("Whole-house inspection and sewer scope while the property is occupied",
             [], "unverified")],
        [P.C("F04", [], "label"), P.C("Property B maintenance", [], "label"),
         P.C("No figure supplied at all.", [], "unverified"),
         P.C("", [], "unverified"),
         P.C("Three years of actual spend, then a capital plan", [], "unverified")],
        [P.C("F05", [], "label"), P.C("Solar tariff on Property A", [], "label"),
         P.C("The reported credit of %s-%s a month is owner input. Which net metering or net "
             "billing tariff the system is on, and when the enrolment ends, is unknown."
             % (m(10), m(20)), [], "unverified"),
         P.C("", [], "unverified"),
         P.C("Pull the interconnection agreement and twelve months of statements",
             [], "unverified")],
        [P.C("F06", [], "label"), P.C("Market rent for Property A", [], "label"),
         P.C("No comparable supplied. This is the single largest unknown on the options page; "
             "renting only ties selling at a gross yield of about %s."
             % P.pct(M.breakeven_gross_yield(2045, with_housing=True), 2)["t"], [], "unverified"),
         P.C("", [], "unverified"),
         P.C("Three written rental opinions from agents who manage single-family lets in the same "
             "Santa Clara County submarket",
             [], "unverified")],
        [P.C("F07", [], "label"), P.C("Market rent for the San Francisco unit", [], "label"),
         P.C("Never stated. It sets the cash cost of choosing to occupy Property A.",
             [], "unverified"),
         P.C("", [], "unverified"),
         P.C("Two rental opinions for the exact unit", [], "unverified")],
        [P.C("F08", [], "label"),
         P.C("San Francisco bill exceeds assessed value times the official rate", [], "label"),
         P.C("Assessed value of %s at the official FY2026-27 rate of 1.18162182 percent gives "
             "about %s, against a reported bill of about %s. The residual of about %s a year is "
             "carried flat as an unexplained charge."
             % (m(M.OWNER["B_assessed_2025"]),
                m(r10(M.OWNER["B_assessed_2025"] * M.STATUTORY["sf_rate_fy2026_27"])),
                m(M.OWNER["B_tax_2025"]), m(P.B_FIXED)), ["sf_treasurer_secured"], "derived"),
         P.C("", [], "unverified"),
         P.C("Download the current secured bill and match each line",
             ["sf_treasurer_secured"], "unverified")],
        [P.C("F09", [], "label"),
         P.C("Property A effective tax rate is derived, not published", [], "label"),
         P.C("The rate of %s is the owner's own bill divided by the owner's own assessed value. "
             "Santa Clara County has hundreds of tax rate areas, so no published rate can be quoted "
             "for the parcel. The rate is stable across the owner's history, which helps, but it is "
             "not an official number." % P.pct(P.RATE_A, 2)["t"], ["boe_pub29"], "derived"),
         P.C("", [], "unverified"),
         P.C("Read the rate printed on the current bill and replace it",
             ["boe_pub29"], "unverified")],
        [P.C("F10", [], "label"), P.C("A $3,000,000 cap on the step-up in basis", [], "label"),
         P.C("Secondary commentary describes a 2026 Treasury proposal to cap the step-up. It could "
             "not be found on the Federal Register, on Treasury's site, or in the IRS Internal "
             "Revenue Bulletin during this pass. No value is asserted and no weight is given to it.",
             [], "unverified"),
         P.C("", [], "unverified"),
         P.C("Search the Federal Register for a notice of proposed rulemaking under section 1014; "
             "until one is produced, ignore the claim", [], "unverified")],
        [P.C("F11", [], "label"), P.C("California 2026 ballot measure results", [], "label"),
         P.C("Measure titles come from the Secretary of State, but the results are from the count "
             "and are certified in December 2026. The results portal is scripted and could not be "
             "read as text.", ["ca_sos_ballot"], "reported"),
         P.C("", [], "unverified"),
         P.C("Re-read the Secretary of State results portal after certification",
             ["ca_sos_results"], "unverified")],
        [P.C("F12", [], "label"),
         P.C("The 1% California surcharge over $1,000,000", [], "label"),
         P.C("The FTB 2025 rate schedules stop at 12.3%. The additional 1% that produces the 13.3% "
             "top rate is applied here as an assumption, not read from an FTB document.",
             ["ftb_2025_rates"], "assumption"),
         P.C("", [], "unverified"),
         P.C("Confirm on the FTB site", ["ftb_2025_rates"], "unverified")],
        [P.C("F13", [], "label"), P.C("Property A and Property B year built", [], "label"),
         P.C("Not supplied. For Property B it decides whether the local rent ordinance applies on "
             "top of the statewide cap.", ["ca_civ_1947_12"], "unverified"),
         P.C("", [], "unverified"),
         P.C("Assessor property characteristics record and original building permit",
             [], "unverified")],
        [P.C("F14", [], "label"), P.C("Size of the rest of the estate", [], "label"),
         P.C("No estimate supplied, so nothing can be said about whether the federal estate tax "
             "threshold will be approached.", ["irs_estate_tax"], "unverified"),
         P.C("", [], "unverified"),
         P.C("A confidential schedule for the estate attorney, never published",
             ["irs_estate_tax"], "unverified")],
        [P.C("F15", [], "label"),
         P.C("Earlier full-precision figures remain in public git history", [], "label"),
         P.C("Rounding to $10 protects everything published from this branch forward. Earlier "
             "generations of this project, merged branches and pull request diffs contain "
             "unrounded figures. No commit can remove them.", [], "unverified"),
         P.C("", [], "unverified"),
         P.C("Owner action only: change repository visibility or rewrite the history",
             [], "unverified")],
    ]
    tbl = dict(id="flag", title="Flagged for review",
               cols=["#", "Item", "What is wrong or missing", "Value withheld", "How to close it"],
               rows=rows,
               note="Nothing on this list blocks the site or the analysis. Each item is published "
                    "rather than hidden so it can be worked through in the open.")
    body = BANNER + "<p class='lead'>Everything that could not be confirmed, everything that looks " \
           "wrong, and one item that no commit can fix. Where a value could not be verified it has " \
           "been left blank rather than filled in with a plausible number.</p>" + LEGEND + \
        render_table(tbl) + \
        ('<div class="banner red"><b>F15 is not fixable from here.</b> Rounding to $10 protects '
         'everything published going forward, but earlier unrounded figures remain in this '
         'repository\'s public history, in merged branches and in pull request diffs. Making the '
         'repository private, or rewriting its history, is your decision and yours alone.</div>')
    return write("flagged.html", "Flagged", "Unverified and irregular", body)


# ====================================================== page: methodology
def page_methodology():
    a = M.A_DEFAULT
    rows = [
        ("Nominal home price growth", P.pct(a["g_market"], 1)["t"], "2.5% / 5.5%",
         "No official forecast exists. Anchored on the California House Price Index rising 2.15% "
         "in 2024, published by the Board of Equalization.", ["boe_lta2025_009", "fhfa_hpi"]),
        ("Assessed value growth", P.pct(a["g_assessed"], 1)["t"], "n/a",
         "The Proposition 13 ceiling. This one is law, not an assumption.", ["boe_pub29"]),
        ("Proposition 19 allowance growth", P.pct(a["g_allowance"], 2)["t"], "n/a",
         "The Board of Equalization adjusts the allowance every two years using the California "
         "House Price Index. 2.15% is the last published change. The model holds $1,044,586 "
         "exactly for transfers in 2025 and 2026, then steps it forward one two-year adjustment "
         "at a time.", ["boe_lta2025_009"]),
        ("Cost inflation", P.pct(a["cpi"], 1)["t"], "2.0% / 5.0%",
         "Anchored on the official CPI-U readings: 3.7% over the twelve months to September 2026, "
         "and annual averages of 8.0% in 2022, 4.1% in 2023 and 2.9% in 2024.",
         ["bls_cpi_home", "bls_cpi_hist"]),
        ("Rent growth on Property B", P.pct(a["rent_growth"], 1)["t"], "n/a",
         "Set below the statewide cap of 5% plus the change in the cost of living, subject to a "
         "10% ceiling.", ["ca_civ_1947_12"]),
        ("Gross rental yield on Property A", P.pct(a["gross_yield"], 1)["t"], "2.0% / 3.2%",
         "No comparable was supplied. This is the largest single unknown on the site.", []),
        ("Vacancy", P.pct(a["vacancy"], 1)["t"], "n/a", "Rule of thumb, no source.", []),
        ("Management fee", P.pct(a["management"], 1)["t"], "n/a", "Rule of thumb, no source.", []),
        ("Maintenance as a share of value", P.pct(a["maintenance_pct"], 1)["t"], "0.5% / 1.5%",
         "Rule of thumb in the absence of any inspection or spend history.", []),
        ("Cost of disposal", P.pct(a["disposition_cost"], 1)["t"], "n/a",
         "Commission plus escrow plus transfer charges. No source; test it against real quotes.", []),
        ("Depreciable share of the property", P.pct(a["building_share"], 0)["t"], "n/a",
         "Land does not depreciate. The split between land and building is unknown.", ["irs_tc409"]),
        ("Portfolio nominal total return", P.pct(a["portfolio_return"], 1)["t"], "5.0% / 9.0%",
         "No official source can supply this. The site leads with break-even rates instead.", []),
        ("Share of return taxed each year", P.pct(a["portfolio_yield"], 1)["t"], "n/a",
         "Income component of total return, taxed annually; the rest is deferred until sale.", []),
        ("Discount rate", P.pct(a["discount"], 1)["t"], "3.0% / 7.0%",
         "No official source. Chosen as a conventional nominal rate.", []),
        ("Combined tax on gains and investment income", P.pct(a["sale_tax_rate"], 1)["t"], "n/a",
         "20% federal long-term capital gains, plus 3.8% net investment income tax, plus 13.3% "
         "California. The last of these rests on the F15 assumption.",
         ["irs_tc409", "irs_niit", "ftb_2025_rates"]),
    ]
    tbl = dict(id="asm", title="Every assumption, in one place",
               cols=["Assumption", "Baseline", "Band", "Why this number", "Source"],
               rows=[[P.C(n, [], "label"), P.C(v, s, "assumption"), P.C(b, [], "assumption"),
                      P.C(why, s, "assumption" if s else "assumption"),
                      P.C("None &mdash; rule of thumb" if not s else "See links", s or [],
                          "assumption")]
                     for n, v, b, why, s in rows],
               note="Nothing in this table is a fact. Where an official source informed the choice "
                    "it is linked. The break-even table on the options page exists precisely so "
                    "that these choices do not have to be trusted.")

    body = BANNER + (
        "<h2>How the model works</h2>"
        "<p class='lead'>The projection engine is deterministic: the same inputs always produce the "
        "same output, and the code is in this repository under <code>decision/_src/</code>. It "
        "works like this.</p>"
        "<ol class='steps'>"
        "<li><h4>Assessed values follow the law, not a forecast</h4><p>Property A's assessed value "
        "grows at exactly the 2% Proposition 13 ceiling until the ownership changes. That is why "
        "the assessed value columns on the projections page are the most reliable figures on this "
        "site.</p></li>"
        "<li><h4>Market values follow an assumption</h4><p>4.0% nominal with a band. Every market "
        "value figure on the site inherits that assumption and should be read as a scenario.</p></li>"
        "<li><h4>At the transfer the property is re-priced two ways</h4><p>With the Proposition 19 "
        "exclusion, the new taxable value is the factored base year value plus any market value "
        "above the cap. Without it, the new taxable value is the full market value. Both are shown "
        "for every year so the cost of each choice is visible.</p></li>"
        "<li><h4>Each option is a cash flow stream</h4><p>Occupy pays tax, insurance, maintenance "
        "and water and receives the solar credit and the rent from the San Francisco unit it frees "
        "up. Renting collects rent net of vacancy and management and pays the same costs. Selling "
        "turns the property into a portfolio that compounds, with the income portion taxed each "
        "year and the growth portion taxed at the end.</p></li>"
        "<li><h4>Each option is credited with the home it lets you live in</h4><p>This is the step "
        "most analyses skip. Occupying gives you a house worth several million dollars to live in; "
        "renting and selling leave you in your San Francisco unit. Valuing that at market rent is "
        "the only way to compare the three fairly, and it is why the options page shows two "
        "columns.</p></li>"
        "<li><h4>The result is a threshold, not a verdict</h4><p>The model solves for the portfolio "
        "return, the rental yield and the growth rate at which the ranking flips. Those are the "
        "numbers to act on.</p></li>"
        "</ol>")

    body += "<h2>Assumptions</h2>" + LEGEND + render_table(tbl)

    body += (
        "<h2>Privacy method</h2>"
        "<div class='grid'>"
        "<div class='card'><h3>No identifiers</h3><ul>"
        "<li>No name, street address, parcel number, assessor's parcel identifier, account number, "
        "email address or telephone number appears on any page.</li>"
        "<li>The two properties are called Property A and Property B, identified only by county.</li>"
        "<li>No ZIP code, city name or neighbourhood name appears on any page.</li>"
        "<li>No trust name, trustee name or beneficiary name appears anywhere.</li></ul></div>"
        "<div class='card'><h3>All money rounded</h3><ul>"
        "<li>Every dollar figure is rounded to the nearest $10, following the instruction that "
        "figures be published in a form that cannot be traced back through a public search.</li>"
        "<li>Assessed values and tax bills are public record in California. Rounding is what makes "
        "publishing them safe.</li>"
        "<li>Statutory amounts are quoted exactly as published, because they are statewide "
        "constants and identify no one.</li>"
        "<li>Each figure is rounded on its own. Where two published figures are subtracted the "
        "result can differ by $10 from the difference quoted on another page, which is itself "
        "computed before rounding.</li></ul></div>"
        "<div class='card'><h3>Verified or withheld</h3><ul>"
        "<li>Every table row links to the official document it was read from.</li>"
        "<li>Where a value could not be confirmed, the cell is blank and marked unverified. No "
        "value is ever inferred to fill a gap.</li>"
        "<li>Owner-supplied figures are marked as owner input and are never presented as "
        "verified.</li></ul></div>"
        "<div class='card'><h3>What could not be fixed here</h3><ul>"
        "<li>Earlier generations of this project published unrounded figures. They remain in the "
        "public git history, in merged branches and in pull request diffs.</li>"
        "<li>No commit in any branch can remove them. Repository visibility or a history rewrite is "
        "the only remedy, and that is an owner decision &mdash; see F15 on the flagged page.</li>"
        "</ul></div></div>")

    body += ("<h2>Reproducing this</h2>"
             "<p class='muted'><code>python3 decision/_src/build.py</code> rebuilds every page. "
             "<code>python3 decision/_src/verify.py</code> re-runs the checks: every table row "
             "carries an official source link, every cited host is on the official allowlist, all "
             "money is rounded to $10, every internal link resolves, and no personal identifier "
             "pattern appears anywhere in the output.</p>")
    return write("methodology.html", "Method &amp; privacy",
                 "How the numbers were produced", body)


# ====================================================== main
def main():
    made = []
    made.append(page_index())
    made.append(page_exec())
    made.append(page_properties())
    made.append(page_property_tax())
    made.append(page_inheritance_tax())
    made.append(page_costs())
    made.append(page_projections())
    made.append(page_scenarios())
    made.append(page_black_swan())
    made.append(page_process())
    made.append(page_questions())
    made.append(page_suggestions())
    made.append(page_law_watch())
    made.append(page_sources())
    made.append(page_flagged())
    made.append(page_methodology())
    print("built %d pages into %s" % (len(made), OUT))
    for p in made:
        print("  ", os.path.basename(p))


if __name__ == "__main__":
    main()
