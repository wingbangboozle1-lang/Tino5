# -*- coding: utf-8 -*-
"""Page shell and shared components for the operating desk.

Every page is static HTML: no scripts, no forms, no iframes, no external assets. That is a
privacy choice as much as a security one — a page with no script cannot leak a visitor, and a
page with no form cannot collect one.
"""
from __future__ import annotations

import html

CSS = """
:root{--ink:#16202b;--mute:#5c6773;--line:#dde3ea;--bg:#f7f9fb;--card:#fff;--accent:#1b4965;
--accent2:#2e6f95;--warn:#8a4b00;--warnbg:#fff6e5;--bad:#8c1c13;--badbg:#fdecea;--ok:#1e5b3a;
--okbg:#eaf6ef;--prop:#3d4f8a}
*{box-sizing:border-box}
body{margin:0;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
color:var(--ink);background:var(--bg)}
a{color:var(--accent2)}
header.top{background:var(--card);border-bottom:1px solid var(--line);padding:14px 22px;
position:sticky;top:0;z-index:5;display:flex;flex-wrap:wrap;gap:14px;align-items:baseline}
header.top .brand{font-weight:650;color:var(--accent);letter-spacing:.01em}
header.top nav{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:14px}
header.top nav a{text-decoration:none;color:var(--mute)}
header.top nav a:hover{color:var(--accent2)}
main{max-width:1120px;margin:0 auto;padding:26px 22px 70px}
h1{font-size:30px;line-height:1.2;margin:.2em 0 .35em;color:var(--accent)}
h2{font-size:21px;margin:2.1em 0 .5em;padding-bottom:.25em;border-bottom:2px solid var(--line)}
h3{font-size:17px;margin:1.5em 0 .35em}
p,li{max-width:78ch}
.lede{font-size:18px;color:#2b3a49}
small,.small{font-size:13.5px;color:var(--mute)}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:15px 17px}
.card h3{margin-top:0}
a.card{text-decoration:none;color:inherit;display:block}
a.card:hover{border-color:var(--accent2);box-shadow:0 1px 0 var(--line)}
.answer{background:linear-gradient(180deg,#fff,#f4f8fb);border:1px solid #c9d8e4;
border-left:5px solid var(--accent);border-radius:10px;padding:16px 19px;margin:18px 0}
.answer h3{margin:.1em 0 .5em;color:var(--accent)}
.flag{background:var(--warnbg);border:1px solid #e8cf9e;border-left:4px solid var(--warn);
border-radius:8px;padding:11px 14px;margin:12px 0}
.flag b{color:var(--warn)}
.stop{background:var(--badbg);border:1px solid #f0c3bd;border-left:4px solid var(--bad);
border-radius:8px;padding:11px 14px;margin:12px 0}
.stop b{color:var(--bad)}
.ok{background:var(--okbg);border:1px solid #bfe0cd;border-left:4px solid var(--ok);
border-radius:8px;padding:11px 14px;margin:12px 0}
table{width:100%;border-collapse:collapse;margin:14px 0;background:var(--card);font-size:14.2px}
th,td{text-align:left;padding:7px 9px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:#eef3f7;font-weight:620;font-size:13px;text-transform:uppercase;letter-spacing:.04em;
color:#3d4b5a;position:sticky;top:0}
tbody tr:hover{background:#fafcfe}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.wrap{overflow-x:auto;border:1px solid var(--line);border-radius:9px}
.wrap table{margin:0;border:0}
.stat{font-variant-numeric:tabular-nums;font-weight:600}
.tag{display:inline-block;font-size:11px;font-weight:650;letter-spacing:.05em;text-transform:uppercase;
padding:1px 6px;border-radius:4px;vertical-align:1px}
.t-ver{background:#e3f0e8;color:#1e5b3a}
.t-own{background:#eceff3;color:#41505f}
.t-ass{background:#eef0fb;color:#3d4f8a}
.t-gap{background:#fff1d6;color:#8a4b00}
.t-stat{background:#e8eef6;color:#1b4965}
.t-no{background:#f6e7e5;color:#8c1c13}
ul.tight{margin:.3em 0 .9em;padding-left:1.25em}
ul.tight li{margin:.2em 0}
.kpi{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));margin:16px 0}
.kpi .k{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:13px 15px}
.kpi .k .v{font-size:25px;font-weight:680;color:var(--accent);font-variant-numeric:tabular-nums;
line-height:1.15}
.kpi .k .l{font-size:12.5px;color:var(--mute);text-transform:uppercase;letter-spacing:.05em;
margin-bottom:5px}
.kpi .k .n{font-size:13px;color:var(--mute);margin-top:5px}
details{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:9px 13px;margin:9px 0}
summary{cursor:pointer;font-weight:600}
.bar{height:14px;border-radius:3px;background:var(--accent2);display:block}
.bar.neg{background:#b5524a}
.brow{display:grid;grid-template-columns:150px 1fr 110px;gap:9px;align-items:center;margin:3px 0;
font-size:13px}
.hist{display:flex;gap:2px;align-items:flex-end;height:90px;margin:10px 0 4px}
.hist .c{flex:1;background:var(--accent2);border-radius:2px 2px 0 0}
.hist .c.neg{background:#b5524a}
footer{border-top:1px solid var(--line);margin-top:40px;padding:18px 22px;color:var(--mute);
font-size:13px;background:var(--card)}
.chip{display:inline-block;background:#eef3f7;border:1px solid var(--line);border-radius:14px;
padding:2px 10px;font-size:13px;margin:2px 4px 2px 0;color:#3d4b5a}
nav.toc{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:11px 15px;
margin:16px 0;font-size:14px}
nav.toc a{margin-right:14px;white-space:nowrap}
@media print{
  header.top,nav.toc,footer{display:none}
  body{background:#fff;font-size:10.5pt}
  main{max-width:none;padding:0}
  h1{font-size:19pt}h2{font-size:13pt;margin-top:1.1em}
  .card,.wrap,table{border-color:#999;break-inside:avoid}
  .wrap{overflow:visible}
  a{color:#000;text-decoration:none}
  .noprint{display:none}
  @page{margin:12mm}
}
"""

NAV = [
    ("index.html", "Start"),
    ("decision.html", "The decision"),
    ("paths.html", "All eight paths"),
    ("phased.html", "Phased entry"),
    ("swans.html", "Uneven economy"),
    ("projections.html", "Projections"),
    ("costs.html", "Carrying costs"),
    ("taxes.html", "Taxes &amp; assessment"),
    ("timeline.html", "Timeline"),
    ("questions.html", "Questions &amp; gaps"),
    ("suggestions.html", "Suggestions"),
    ("brief-sheet.html", "Attorney &amp; CPA sheet"),
    ("work-register.html", "Requirement register"),
    ("law-watch.html", "Law watch"),
    ("glossary.html", "Glossary"),
    ("sources.html", "Sources"),
    ("flagged.html", "Flagged for review"),
    ("method.html", "Method &amp; privacy"),
]

HEADER = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive,nosnippet">
<meta name="referrer" content="no-referrer">
<meta name="google" content="notranslate">
<title>{title} — inheritance decision desk</title>
<style>{css}</style>
</head>
<body>
<header class="top"><span class="brand">Inheritance decision desk</span>
<nav>{nav}</nav></header>
<main>
"""

FOOTER = """
<footer>
<p><b>Scope.</b> A decision aid for one household question: when the inherited house arrives,
should the heir live in it, let it out, or sell it and invest? Every figure is a model output
from a round modelling base — not either property's value — rounded to $10. Statutory amounts
are quoted exactly as published and marked. Nothing here is legal, tax or investment advice.</p>
<p><b>Privacy.</b> No names, streets, parcel numbers, postcodes, cities or neighbourhoods appear
on this site, and no figure from the household's own records is published at any precision. The
conclusions are published as break-evens, rankings and rates, which move only slightly across a
tenfold range of property values — the small movement is caused by a fixed statutory cap and is
tested and stated on the method page. <a href="method.html">Method &amp; privacy</a> ·
<a href="privacy/index.html">what was published before</a></p>
<p><b>Verification.</b> Every table row carries a link to the official document it rests on, or
says in the row why no official document exists. Unverified material is on
<a href="flagged.html">Flagged for review</a> and is not used in any conclusion.</p>
</footer>
</main></body></html>
"""


def esc(s):
    return html.escape(str(s), quote=True)


def money(x, dash="—"):
    """Format a rounded dollar amount. Never used for statutory amounts."""
    if x is None:
        return dash
    return f"${x:,.0f}"


def pct(x, digits=2, dash="—"):
    if x is None:
        return dash
    return f"{x * 100:.{digits}f}%"


def page(title, body, root=""):
    nav = "".join(f'<a href="{root}{href}">{label}</a>' for href, label in NAV)
    return (HEADER.format(title=esc(title), css=CSS, nav=nav)
            + body + FOOTER)


def src(sources, sid, label=None):
    """An inline citation link to an official document in the register."""
    s = sources.BY_ID.get(sid)
    if s is None:
        raise KeyError(f"unknown source id {sid}")
    text = label or s["publisher"].split(",")[0]
    return f'<a href="{s["url"]}" rel="noopener noreferrer nofollow" target="_blank">{esc(text)}</a>'


def tag(kind):
    labels = {"ver": ("t-ver", "verified"), "own": ("t-own", "household input"),
              "ass": ("t-ass", "assumption"), "gap": ("t-gap", "unverified"),
              "stat": ("t-stat", "statutory"), "no": ("t-no", "no official source")}
    cls, lab = labels[kind]
    return f'<span class="tag {cls}">{lab}</span>'


BASIS_LABEL = {
    "ass": ("t-ass", "assumption"),
    "stat": ("t-stat", "statutory"),
    "model": ("t-own", "model output"),
    "gap": ("t-gap", "unverified"),
    "own": ("t-own", "household input"),
    "derived": ("t-ass", "derived"),
}


def table(headers, rows, cls="", numeric_from=1, basis=None):
    """rows: list of lists of already-escaped cell HTML. Columns from `numeric_from` are numeric.

    `basis` appends a Basis column so that every row states whether its figures are statutory,
    an assumption, or a model output. A row that carries an official link needs no basis, and
    the verifier accepts either.
    """
    numcls = ' class="num"'
    headers = list(headers)
    if basis:
        headers.append("Basis")
    th = "".join(
        ("<th" + (numcls if (numeric_from > 0 and i >= numeric_from and (not basis or i < len(headers) - 1)) else "") + ">" + h + "</th>")
        for i, h in enumerate(headers))
    trs = []
    for r in rows:
        r = list(r)
        if basis:
            cls_t, lab = BASIS_LABEL[basis]
            r.append(f'<span class="tag {cls_t}">{lab}</span>')
        tds = []
        for i, c in enumerate(r):
            n = (numeric_from > 0 and i >= numeric_from and (not basis or i < len(r) - 1))
            cls_td = ' class="num"' if n else ""
            tds.append(f"<td{cls_td}>{c}</td>")
        trs.append("<tr>" + "".join(tds) + "</tr>")
    return (f'<div class="wrap"><table class="{cls}"><thead><tr>{th}</tr></thead>'
            f'<tbody>{"".join(trs)}</tbody></table></div>')


def kpi(items):
    out = ['<div class="kpi">']
    for value, label, note in items:
        out.append(f'<div class="k"><div class="l">{label}</div>'
                   f'<div class="v">{value}</div><div class="n">{note}</div></div>')
    out.append("</div>")
    return "".join(out)


def bar_row(label, value, maxabs, unit="M"):
    w = 0 if maxabs == 0 else min(100, abs(value) / maxabs * 100)
    cls = "neg" if value < 0 else ""
    shown = f"{value/1e6:,.2f}M" if unit == "M" else f"{value:,.0f}"
    return (f'<div class="brow"><span>{esc(label)}</span>'
            f'<span><span class="bar {cls}" style="width:{w:.1f}%"></span></span>'
            f'<span class="num">{shown}</span></div>')
