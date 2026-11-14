# -*- coding: utf-8 -*-
"""Shared page shell for the cbd/ desk: grouped navigation, privacy banner, print styles."""

NAV = [
    ("Decide", [
        ("index.html", "Summary", "index"),
        ("paths.html", "Mixed paths", "paths"),
        ("phased.html", "Phased entry test", "phased"),
    ]),
    ("Plan", [
        ("timeline.html", "Deadlines timeline", "timeline"),
        ("questions.html", "Questions and gaps", "questions"),
    ]),
    ("Share", [
        ("brief.html", "Attorney &amp; CPA sheet", "brief"),
    ]),
    ("Reference", [
        ("glossary.html", "Glossary", "glossary"),
        ("sources.html", "Sources", "sources"),
        ("method.html", "Method", "method"),
    ]),
    ("Review", [
        ("suggestions.html", "Suggestions", "suggestions"),
        ("flagged.html", "Flagged for review", "flagged"),
    ]),
]

CSS = """
:root{--ink:#1b2330;--muted:#5b6474;--line:#dfe3ea;--bg:#f6f7f9;--card:#fff;--blue:#1f4e79;
--blue-lt:#eef3f7;--amber:#8a5a00;--amber-lt:#fdf3e0;--red:#9b2226;--red-lt:#fdecec;--green:#1f6b3f}
*{box-sizing:border-box}
body{margin:0;font:15px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg)}
header.top{background:#fff;border-bottom:1px solid var(--line)}
.top-in{max-width:1180px;margin:auto;padding:14px 22px;display:flex;align-items:baseline;gap:16px;flex-wrap:wrap}
.top-in .brand{font-weight:700;color:var(--blue);font-size:18px;text-decoration:none}
.top-in .sub{font-size:13px;color:var(--muted)}
nav.main{background:var(--blue)}
nav.main .in{max-width:1180px;margin:auto;padding:0 22px;display:flex;flex-wrap:wrap;gap:4px 18px}
nav.main .grp{padding:6px 0;}
nav.main .grp b{display:block;font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:#9fc0da;margin-top:4px}
nav.main .grp a{display:inline-block;padding:3px 0;color:#e6eff6;text-decoration:none;font-size:13.5px;margin-right:12px}
nav.main .grp a:hover{color:#fff;text-decoration:underline}
nav.main .grp a.on{color:#fff;font-weight:700;border-bottom:2px solid #fff}
main{max-width:1180px;margin:auto;padding:22px 22px 70px}
h1{font-size:24px;margin:6px 0 6px;color:var(--blue)}
h2{font-size:18px;margin:26px 0 10px;color:var(--blue)}
h3{font-size:15px;margin:18px 0 6px}
p{margin:8px 0}
.sub{color:#2b3444;font-size:15px}
.small{font-size:13px;color:var(--muted)}
.banner{background:var(--blue-lt);border:1px solid #cfe0ec;border-left:4px solid var(--blue);padding:10px 14px;border-radius:6px;font-size:13.5px;margin:14px 0}
.banner.warn{background:var(--amber-lt);border-color:#f0dcb4;border-left-color:var(--amber)}
.banner.red{background:var(--red-lt);border-color:#f3cfcf;border-left-color:var(--red)}
.privacy{background:#eef6ef;border:1px solid #c9e3d2;border-left:4px solid var(--green);padding:8px 12px;border-radius:6px;font-size:12.5px;margin:10px 0 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:16px 18px;margin:12px 0}
.card.hl{border-left:4px solid var(--blue)}
.card.rr{border-left:4px solid var(--amber)}
.card.wc{border-left:4px solid var(--red)}
.split{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media (max-width:820px){.split{grid-template-columns:1fr}}
.grid4{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px;margin:14px 0}
a.card{color:var(--ink);text-decoration:none;display:flex;flex-direction:column;gap:4px}
a.card:hover{border-color:var(--blue)}
a.card b{color:var(--blue)}
a.card span{font-size:13px;color:var(--muted)}
.scroll{overflow-x:auto;margin:10px 0}
table.t{border-collapse:collapse;width:100%;background:#fff;font-size:13.5px}
table.t th,table.t td{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
table.t th{background:#eef2f7;font-weight:600;color:#2a3a52}
td.n{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
td.c{text-align:center}
td.src{font-size:12px;color:#33405a}
a{color:var(--blue)}
.tag{display:inline-block;font-size:10.5px;background:#eef2f7;color:#2a3a52;border-radius:3px;padding:0 4px;margin-left:2px}
.flag{background:var(--red-lt);color:var(--red);padding:0 4px;border-radius:3px;font-size:12px}
.nosrc{color:#7a4b00;font-style:italic;font-size:12.5px}
.timeline{margin:12px 0}
.tick{display:flex;gap:12px;padding:6px 0;border-left:3px solid var(--blue);padding-left:12px;margin-left:6px}
.tick .when{min-width:170px;font-weight:600;color:var(--blue)}
ol.q li{margin:4px 0}
footer{max-width:1180px;margin:auto;padding:0 22px 30px;font-size:12.5px;color:var(--muted)}
/* one-page printable brief */
.sheet{background:#fff;border:1px solid var(--line);padding:18px 22px}
@page{size:letter;margin:0.5in}
@media print{
  header.top,nav.main,footer,.noprint{display:none!important}
  body{background:#fff;font-size:10.5pt;line-height:1.3}
  main{padding:0;max-width:none}
  .sheet{border:none;padding:0}
  h1{font-size:16pt;margin:0 0 4px}
  h2,h3{font-size:11pt;margin:6px 0 3px}
  table.t{font-size:9pt}
  table.t th,table.t td{padding:2px 4px}
  ol.q{margin:2px 0 2px 16px;padding:0}
  ol.q li{margin:1px 0;font-size:9.5pt}
  p,.small{margin:3px 0;font-size:9pt}
  .sheet{page-break-inside:avoid}
  a{color:#000;text-decoration:none}
}
"""


def _nav(active):
    out = ['<nav class="main" aria-label="Main"><div class="in">']
    for group, items in NAV:
        out.append('<div class="grp"><b>%s</b>' % group)
        for href, label, key in items:
            cls = ' class="on"' if key == active else ""
            out.append('<a href="%s"%s>%s</a>' % (href, cls, label))
        out.append("</div>")
    out.append("</div></nav>")
    return "".join(out)


def render(name, title, active, body, kind="std"):
    head = (
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="robots" content="index,follow">'
        "<title>%s &mdash; Property A and B decision desk</title>"
        "<style>%s</style></head><body>" % (title, CSS)
    )
    top = (
        '<header class="top"><div class="top-in">'
        '<a class="brand" href="index.html">Property A and B decision desk</a>'
        '<span class="sub">Sell, let or live in it, and how to phase the money. Source-linked; placeholders only.</span>'
        "</div></header>"
    )
    privacy = (
        '<div class="privacy noprint">Privacy: Property A and Property B are placeholders. No names, addresses, '
        "parcel or account numbers, ZIP codes or city names appear on this desk. Money is rounded to the nearest $10. "
        "This desk is a decision aid, not advice.</div>"
    )
    if kind == "print":
        main_body = body
    else:
        main_body = privacy + body
    foot = (
        "<footer>Generated by cbd/_src/build.py. Every figure is computed by desk_model.py and checked by verify.py. "
        'Sources: <a href="sources.html">sources</a> &middot; <a href="flagged.html">flagged for review</a> '
        '&middot; <a href="method.html">method</a> &middot; <a href="../index.html">hub</a></footer>'
    )
    return head + top + ("" if kind == "print" else _nav(active)) + "<main>" + main_body + "</main>" + (
        "" if kind == "print" else foot) + "</body></html>\n"
