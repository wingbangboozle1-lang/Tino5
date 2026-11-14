# -*- coding: utf-8 -*-
"""Shared HTML shell, styles and table helpers for the owner-brief desk.

The published artifact is static HTML and CSS only. There is no JavaScript, no external
font, image or style reference, no form and no analytics: a page that cannot run code and
cannot call out cannot leak what it is displaying. The verifier enforces that.
"""

from html import escape

PAGES = [
    ("index.html", "Overview", "Where each question is answered"),
    ("executive-summary.html", "Executive summary", "The decision, the numbers behind it, and what is still unknown"),
    ("properties.html", "The two properties", "What is known, what is owner input, and what is missing"),
    ("property-tax.html", "Property tax", "Proposition 13, Proposition 19 and the assessed value after transfer"),
    ("inheritance-tax.html", "Inheritance and estate tax", "Federal thresholds, California's prohibition, and basis"),
    ("running-costs.html", "Running costs", "Insurance, water, power, maintenance, and what they cost over time"),
    ("projections.html", "Projections 2026-2076", "Value, assessed value, tax and costs, year by year"),
    ("options.html", "The three options", "Occupy, let, or sell and reinvest, with break-evens"),
    ("black-swan.html", "Black swans", "Real inflation history replayed across fifty uneven years"),
    ("process.html", "The transfer, step by step", "What actually happens when the trust property passes"),
    ("questions.html", "Questions and gaps", "What must be answered before a decision is reasonable"),
    ("suggestions.html", "Suggestions", "Proposed only. Nothing here has been implemented"),
    ("law-watch.html", "Law watch", "Rules in force, rules that moved, and rules under discussion"),
    ("repo-review.html", "Repository review", "What is in the repository and what was found in it"),
    ("sources.html", "Sources", "Every official document this desk read"),
    ("flagged.html", "Flagged for review", "Irregularities and unverified items, with the source links"),
    ("methodology.html", "Method and privacy", "How every number was produced and what is kept off this site"),
]

PRIVACY = (
    "<b>Privacy.</b> No name, street address, parcel identifier, account number, postcode or "
    "city appears anywhere on this site. The two properties are called Property A and Property B. "
    "Every dollar figure is rounded to the nearest $10 so that a published number cannot be "
    "matched back to a public record. Statutory amounts are quoted exactly as published because "
    "they are statewide constants and identify nobody."
)

CSS = """
:root{
  --ink:#1b2330; --muted:#5b6474; --line:#dfe3ea; --bg:#f6f7f9; --card:#ffffff;
  --blue:#1f4e79; --blue-lt:#eef3f7; --green:#1f6b3f; --green-lt:#e8f3ec;
  --amber:#8a5a00; --amber-lt:#fdf3e0; --red:#9b2226; --red-lt:#fdecec;
  --grey-lt:#eef0f3;
}
*{box-sizing:border-box}
body{margin:0;font:15px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  color:var(--ink);background:var(--bg)}
header.top{background:#fff;border-bottom:1px solid var(--line);padding:0}
.top-in{max-width:1180px;margin:auto;padding:16px 22px;display:flex;align-items:baseline;gap:16px;flex-wrap:wrap}
header.top h1{margin:0;font-size:19px;color:var(--blue);letter-spacing:.01em}
header.top .sub{font-size:13px;color:var(--muted)}
nav.main{background:var(--blue)}
nav.main ul{max-width:1180px;margin:auto;padding:0 22px;list-style:none;display:flex;flex-wrap:wrap;gap:2px}
nav.main a{display:block;padding:9px 11px;color:#dce8f1;text-decoration:none;font-size:13px;border-bottom:3px solid transparent}
nav.main a:hover{background:#2a5f8f;color:#fff}
nav.main a.on{background:#2a5f8f;border-bottom-color:#fff;color:#fff}
main{max-width:1180px;margin:auto;padding:22px 22px 70px}
h2{font-size:19px;margin:30px 0 10px;color:var(--blue)}
h3{font-size:15px;margin:22px 0 8px;color:var(--ink)}
p{margin:10px 0}
.lead{font-size:15.5px;color:#2b3444}
.banner{background:var(--blue-lt);border:1px solid #cfe0ec;border-left:4px solid var(--blue);
  padding:11px 14px;border-radius:6px;font-size:13.5px;margin:14px 0}
.banner.warn{background:var(--amber-lt);border-color:#f0dcb4;border-left-color:var(--amber)}
.banner.red{background:var(--red-lt);border-color:#f3cfcf;border-left-color:var(--red)}
.banner.green{background:var(--green-lt);border-color:#c9e3d2;border-left-color:var(--green)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(268px,1fr));gap:12px;margin:14px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:14px;
  color:var(--ink);text-decoration:none;display:flex;flex-direction:column;gap:5px}
.card:hover{border-color:var(--blue);background:#fbfdff}
.card b{color:var(--blue);font-size:14.5px}
.card span{font-size:12.8px;color:var(--muted);line-height:1.45}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px;margin:16px 0}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 14px}
.kpi .v{font-size:22px;font-weight:600;color:var(--blue);letter-spacing:-.01em}
.kpi .l{font-size:12.5px;color:var(--muted);margin-top:3px}
.kpi .n{font-size:11.5px;color:var(--muted);margin-top:5px;border-top:1px dotted var(--line);padding-top:5px}
.tblwrap{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:4px 0 0;margin:14px 0;overflow-x:auto}
table.data{width:100%;border-collapse:collapse;font-size:13.2px}
table.data th{background:var(--blue-lt);text-align:left;padding:8px 10px;border-bottom:2px solid var(--line);
  position:sticky;top:0;font-size:12.4px;color:#324a63;vertical-align:bottom}
table.data td{padding:8px 10px;border-bottom:1px solid #edf0f4;vertical-align:top}
table.data tr:last-child td{border-bottom:none}
table.data tbody tr:hover{background:#fafcfe}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
tr.mark td{background:#fffdf5}
tr.hi td{background:var(--blue-lt)}
td.t-lab{font-weight:600;color:#2b3444}
.tn{font-size:12.4px;color:var(--muted);padding:8px 12px 12px}
.legend{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 2px;font-size:12px;color:var(--muted)}
.legend span{padding:2px 8px;border-radius:10px;border:1px solid var(--line);background:#fff}
.pill{display:inline-block;padding:1px 7px;border-radius:9px;font-size:11.5px;font-weight:600;white-space:nowrap}
.p-ver{background:var(--green-lt);color:var(--green);border:1px solid #c9e3d2}
.p-own{background:var(--grey-lt);color:#41505f;border:1px solid #dde1e7}
.p-der{background:var(--blue-lt);color:var(--blue);border:1px solid #cfe0ec}
.p-asm{background:var(--amber-lt);color:var(--amber);border:1px solid #f0dcb4}
.p-unv{background:var(--red-lt);color:var(--red);border:1px solid #f3cfcf}
.p-new{background:#eef0f3;color:#41505f;border:1px solid #dde1e7}
.t-ver{background:#fafdfb}.t-own{}.t-der{}.t-asm{}.t-unv{background:#fffaf9}
a.src{color:var(--blue);text-decoration:none;border-bottom:1px dotted #9db6cc;font-size:12.4px;white-space:nowrap}
a.src:hover{background:var(--blue-lt)}
a.src:visited{color:#3b5f85}
a{color:var(--blue)}
.nosrc{display:block;font-size:11.5px;color:var(--amber);margin-top:3px}
.small{font-size:12.6px;color:var(--muted)}
ul.tight{margin:8px 0;padding-left:20px}
ul.tight li{margin:5px 0}
code{background:var(--blue-lt);padding:1px 5px;border-radius:4px;font-size:12.6px}
footer{max-width:1180px;margin:auto;padding:0 22px 40px;color:var(--muted);font-size:12.4px}
.bar{height:9px;border-radius:5px;background:#e7ebf0;overflow:hidden;min-width:80px}
.bar i{display:block;height:100%;background:var(--blue)}
.bar i.neg{background:var(--red)}
@media (max-width:640px){
  main{padding:16px 14px 50px}
  .kpi .v{font-size:19px}
  table.data{font-size:12.4px}
}
"""


def esc(x):
    return escape(str(x))


def pill(kind, text):
    return '<span class="pill p-%s">%s</span>' % (kind, esc(text))


def table(headers, rows, note=None, cls="data"):
    """rows: list of (cells, row_class_or_None). Cells are raw HTML."""
    out = ['<div class="tblwrap"><table class="%s"><thead><tr>' % cls]
    for h in headers:
        num = ' class="num"' if isinstance(h, tuple) else ''
        txt = h[1] if isinstance(h, tuple) else h
        out.append("<th%s>%s</th>" % (num, txt))
    out.append("</tr></thead><tbody>")
    for cells, rcls in rows:
        out.append('<tr class="%s">' % rcls if rcls else "<tr>")
        for c in cells:
            if isinstance(c, tuple) and len(c) == 2 and c[0] == "num":
                out.append('<td class="num">%s</td>' % c[1])
            else:
                out.append("<td>%s</td>" % c)
        out.append("</tr>")
    out.append("</tbody></table>")
    if note:
        out.append('<p class="tn">%s</p>' % note)
    out.append("</div>")
    return "".join(out)


def page(title, nav_key, body, subtitle=None, extra_head=""):
    nav = []
    for fn, label, _ in PAGES:
        cls = ' class="on"' if fn == nav_key else ""
        nav.append('<li><a%s href="%s">%s</a></li>' % (cls, fn, esc(label)))
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<meta name="referrer" content="no-referrer">
<title>%s &mdash; Property decision desk</title>
<style>%s</style>
%s
</head>
<body>
<header class="top"><div class="top-in">
<h1>Property decision desk</h1>
<div class="sub">%s</div>
</div></header>
<nav class="main"><ul>%s</ul></nav>
<main>
<div class="banner">%s</div>
%s
</main>
<footer>
Not tax, legal or investment advice. Rules and thresholds change; re-check the law in force at
the time of any transfer. Every figure on this site is either quoted from an official source
linked on its row, or labelled as owner input, derived, or an assumption.
</footer>
</body>
</html>
""" % (esc(title), CSS, extra_head, esc(subtitle or title), "".join(nav), PRIVACY, body)


def cards(pairs):
    out = ['<div class="grid">']
    for href, title, desc in pairs:
        out.append('<a class="card" href="%s"><b>%s</b><span>%s</span></a>' % (href, title, desc))
    out.append("</div>")
    return "".join(out)


def bar(value, lo, hi):
    """A tiny inline bar for a signed range. Pure CSS, no images."""
    span = (hi - lo) or 1.0
    frac = max(0.0, min(1.0, (value - lo) / span))
    zero = max(0.0, min(1.0, (0.0 - lo) / span))
    a, b = min(frac, zero), max(frac, zero)
    neg = value < 0
    return ('<span class="bar"><i class="%s" style="margin-left:%.1f%%;width:%.1f%%"></i></span>'
            % ("neg" if neg else "", a * 100.0, (b - a) * 100.0))


def src_cell(links, reason=None):
    """A source cell: one official link per source id, or a blank/flagged marker.

    Every table row must either link an official source or carry a `nosrc` marker that
    explains why no official source exists. The verifier enforces it.
    """
    import sources as src
    if links:
        return "<br>".join(src.link(s) for s in links)
    return src.nosrc(reason or "no official source exists for this row; the value is not asserted")
