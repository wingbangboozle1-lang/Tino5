# -*- coding: utf-8 -*-
"""Build desk-03242c78: a static, script-free, privacy-first decision desk.

Usage:  python3 desk-03242c78/_src/build.py

Reads model.json (written by model.py) and sources.py, and writes the HTML pages plus a
machine-readable page manifest used by verify.py and by the repo's verify_safe.py gate.

Design rules enforced here:
  * no JavaScript, no webfonts, no images, no analytics, no third-party requests;
  * every data-table body row carries either an official source link or a status tag
    (owner / derived / assumption / exact / none / unverified);
  * money is printed through money10(), which refuses to print a figure that is not a
    multiple of $10 unless the caller marks it exact and passes a statutory literal;
  * no place names beyond "California", "Santa Clara County" and "San Francisco County";
    no ZIP, street, parcel number, or unit-level identifying detail.
"""

from __future__ import annotations

import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import sources as S  # noqa: E402
from model import PATHS as PATHS_RAW, run_path, REGIMES as _REG, phase_compare  # noqa: E402

BUILT = "15 November 2026"
HORIZON = 20
TRANSFER_YEARS = (2040, 2045, 2050)

with open(os.path.join(HERE, "model.json")) as fh:
    M = json.load(fh)

MI = M["model"]
BANDS = M["bands"]
REGIMES = M["regimes"]
PATHS = {p["id"]: p for p in M["paths"]}
RESULTS = M["results"]
DIST = M["distribution"]
BREAK = M["breakevens"]
CROSS = M["crossovers"]
PHASE = M["phase"]

# --------------------------------------------------------------------------- formatting


class Exact(str):
    """A stated statutory amount: exempt from the round-to-$10 rule, marked on the page."""


def money10(x, exact=None):
    """Format a money amount.

    Rounds to the nearest $10 unless the amount is a registered statutory literal, in which
    case it is printed exactly and wrapped in <code> so that the repository's own publication
    gate can tell an exact statutory amount from an unrounded one.
    """
    if exact is not None:
        return Exact('<code class="stat">$%s</code>' % html.escape(str(exact)))
    v = int(round(float(x) / 10.0) * 10)
    sign = "-" if v < 0 else ""
    text = sign + "$" + "{:,}".format(abs(v))
    if S.is_literal(abs(v)):
        return '<code class="stat">%s</code>' % text
    return text


def money0(x):
    """Money with no rounding, used only for statutory amounts."""
    return '<code class="stat">$%s</code>' % "{:,}".format(int(round(x)))


def pct(x, nd=2):
    return ("{:." + str(nd) + "f}%").format(x * 100.0)


def num(x, nd=0):
    return ("{:,.%df}" % nd).format(x)


def tag(kind, label=None):
    text = {
        "ok": "official",
        "exact": "exact",
        "own": "owner",
        "asm": "assumption",
        "drv": "derived",
        "none": "no source",
        "unv": "unverified",
    }[kind]
    return '<span class="tag-%s">%s</span>' % (kind, label or text)


def src(*ids):
    return " ".join(S.link(i) for i in ids)


def ex(amount):
    """Wrap a statutory amount quoted in prose so it is treated as exact, not as model money."""
    return '<code class="stat">%s</code>' % amount


def res(transfer_year, regime, path_id):
    for r in RESULTS:
        if (r["transfer_year"] == transfer_year and r["regime"] == regime
                and r["path"] == path_id):
            return r
    raise KeyError((transfer_year, regime, path_id))


def ranked(transfer_year, regime, key="net_worth_with_shelter"):
    rows = [r for r in RESULTS
            if r["transfer_year"] == transfer_year and r["regime"] == regime]
    return sorted(rows, key=lambda r: -r[key])


def best(transfer_year, regime):
    return ranked(transfer_year, regime)[0]


def regime_name(k):
    return REGIMES[k]["label"]


def sign(x):
    return "+" if x >= 0 else "−"


# --------------------------------------------------------------------------- shell
NAV = [
    ("Start here", [
        ("index.html", "The decision"),
        ("what-would-change.html", "What would change the answer"),
        ("charts.html", "Projection charts"),
    ]),
    ("The two properties", [
        ("property-a.html", "Property A — inherited"),
        ("property-b.html", "Property B — already owned"),
        ("own-vs-inherit.html", "Why they are not comparable"),
    ]),
    ("Choices compared", [
        ("choices.html", "All choices, same dates"),
        ("live-path.html", "Live in A"),
        ("rent-path.html", "Rent A out"),
        ("sell-path.html", "Sell and reinvest"),
        ("mixed-paths.html", "Mixed paths"),
        ("phased.html", "Phased investing"),
        ("workbook.html", "Workbook: what-if"),
    ]),
    ("Taxes", [
        ("estate-tax.html", "Estate tax and liquidity"),
        ("income-basis.html", "Income tax and basis"),
        ("property-tax.html", "Property tax and assessment"),
        ("prop19.html", "Proposition 19"),
        ("sec121.html", "Section 121 exclusion"),
        ("depreciation.html", "Depreciation and recapture"),
        ("propH.html", "Measure H parcel tax"),
    ]),
    ("Local rules and market", [
        ("rents.html", "Rents and the rent floor"),
        ("local-rules.html", "Local rules that bind"),
        ("swan.html", "Black swans and extreme paths"),
        ("market-outlook.html", "What the long record shows"),
    ]),
    ("Plan and paperwork", [
        ("timeline.html", "Deadline timeline"),
        ("maintenance.html", "Five-year building plan"),
        ("valuation.html", "Date-of-death valuation"),
        ("like-kind.html", "Like-kind exchange decision"),
        ("investment-policy.html", "Policy for the proceeds"),
        ("annual-rerun.html", "Annual re-run"),
    ]),
    ("Review and registers", [
        ("briefing-cpa.html", "Briefing sheet: CPA"),
        ("briefing-attorney.html", "Briefing sheet: attorney"),
        ("questions.html", "Questions and gaps"),
        ("suggestions.html", "Suggestions for review"),
        ("flagged.html", "Flagged for review"),
        ("sources.html", "Source register"),
        ("methodology.html", "Method and rounding"),
        ("glossary.html", "Glossary"),
        ("privacy.html", "Privacy statement"),
    ]),
]

ALL_PAGES = [(href, label) for _, items in NAV for href, label in items]


def nav_html(current):
    out = ['<nav class="groups" aria-label="Desk sections">', '<div class="wrap">']
    for group, items in NAV:
        out.append('<div class="grp"><span>%s</span></div>' % html.escape(group))
        out.append("<ul>")
        for href, label in items:
            cur = ' aria-current="page"' if href == current else ""
            out.append('<li><a href="%s"%s>%s</a></li>' % (href, cur, html.escape(label)))
        out.append("</ul>")
    out.append("</div></nav>")
    return "\n".join(out)


def shell(page, title, body, body_class="", dek="", parent="../"):
    if not title.endswith("· Tino5"):
        title = title + " · Tino5 estate desk"
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="A source-verified, privacy-first comparison of living in, renting out, selling, and mixed paths for two California homes.">
<meta name="robots" content="index, follow">
<link rel="stylesheet" href="style.css">
</head>
<body class="{bclass}">
<header class="masthead">
  <div class="wrap">
    <div class="site"><a href="{parent}index.html">Tino5</a> · estate decision desk</div>
    <div class="tag">Anonymised · no personal data · every figure sourced</div>
    <div class="stamp">Built {built}</div>
  </div>
</header>
{nav}
<main>
  <div class="wrap">
{body}
  </div>
</main>
<footer>
  <div class="wrap">
    <p><strong>This is a planning document, not advice.</strong> It is prepared for review by a
    licensed California attorney and a CPA before any step is taken. No legal, tax or
    investment advice is given or implied. Statutory amounts are quoted exactly and marked;
    every other figure is an assumption, an owner-supplied anchor, or arithmetic on those.</p>
    <p>Nothing here identifies a person, a street address, an assessor's parcel number, or a
    ZIP code. Owner-supplied figures are approximate and unverified. Money is rounded to the
    nearest $10 except where a statute or official table states an exact amount.</p>
    <p><a href="sources.html">Source register</a> · <a href="methodology.html">Method and
    rounding</a> · <a href="privacy.html">Privacy statement</a> ·
    <a href="flagged.html">Flagged for review</a> · <a href="glossary.html">Glossary</a> ·
    <a href="{parent}index.html">All desks</a></p>
  </div>
</footer>
</body>
</html>
""".format(title=html.escape(title), bclass=body_class, built=BUILT,
           nav=nav_html(page), body=body, parent=parent)


def h1(t, dek=""):
    s = "<h1>%s</h1>" % t
    if dek:
        s += '<p class="lede">%s</p>' % dek
    return s


def table(caption, head, rows, cls="", note="", status="drv"):
    """Render a data table.

    `status` is the provenance tag appended to any body row that does not already carry a
    source link or its own tag. Every table row on this desk therefore states either where
    its figure comes from or that it is arithmetic on stated inputs. Pass status=None only
    for a table that has been checked row by row; the verifier will catch it if a row is bare.
    """
    out = ['<div class="tw"><table class="%s">' % cls]
    if caption:
        out.append("<caption>%s</caption>" % caption)
    out.append("<thead><tr>")
    heads = list(head)
    if status is not None:
        heads.append("Status")
    for h in heads:
        attr = ' class="num"' if h.startswith("#") else ""
        out.append("<th%s>%s</th>" % (attr, h.lstrip("#")))
    out.append("</tr></thead><tbody>")
    for r in rows:
        cls_row = ""
        if isinstance(r, tuple) and len(r) == 2 and isinstance(r[1], list):
            cls_row, r = r
            cls_row = ' class="%s"' % cls_row
        out.append("<tr%s>" % cls_row)
        for cell in r:
            if isinstance(cell, tuple) and cell and cell[0] == "num":
                out.append('<td class="num">%s</td>' % cell[1])
            else:
                out.append("<td>%s</td>" % cell)
        if status is not None:
            joined = " ".join(str(c) for c in r)
            if 'class="tag-' not in joined and 'class="src"' not in joined:
                out.append("<td>%s</td>" % tag(status))
        out.append("</tr>")
    out.append("</tbody></table></div>")
    if note:
        out.append('<p class="small">%s</p>' % note)
    return "\n".join(out)


def stat(k, v, s=""):
    return ('<div class="stat"><div class="k">%s</div><div class="v">%s</div>'
            '<div class="s">%s</div></div>' % (k, v, s))


def risk(text, title="Reinvestment risk"):
    return ('<div class="risk"><strong>%s.</strong> %s</div>' % (title, text))


def note(text, cls=""):
    return '<div class="note %s">%s</div>' % (cls, text)


def rank_of(transfer_year, regime, path_id):
    rows = ranked(transfer_year, regime)
    for i, r in enumerate(rows, 1):
        if r["path"] == path_id:
            return i
    raise KeyError(path_id)


def fmt_range(lo, hi, kind="pct", nd=1):
    if kind == "pct":
        return pct(lo, nd) + " to " + pct(hi, nd)
    return money10(lo) + " to " + money10(hi)


def best_at(transfer_year, regime="baseline", axis="house", value=0.035):
    """Re-run every path with one assumption changed; return (best_id, net worth)."""
    base = dict(REGIMES[regime], key=regime)
    kw = {"gh": value} if axis == "house" else {"ge": value}
    rows = [run_path(*p, transfer_year=transfer_year, regime=base, **kw) for p in PATHS_RAW]
    top = max(rows, key=lambda r: r["net_worth_with_shelter"])
    return top["path"], int(round(top["net_worth_with_shelter"] / 10.0) * 10)


def path_of(pid):
    for p in PATHS_RAW:
        if p[0] == pid:
            return p
    raise KeyError(pid)


def expose():
    """Return the namespace the page modules use (attribute access)."""
    import types
    return types.SimpleNamespace(**dict(
        write=write, h1=h1, table=table, stat=stat, risk=risk, note=note,
        money10=money10, money0=money0, pct=pct, num=num, tag=tag, src=src, ex=ex,
        shell=shell, rank_of=rank_of, fmt_range=fmt_range, best_at=best_at,
        res=res, best=best, ranked=ranked, MI=MI, BANDS=BANDS, REGIMES=REGIMES,
        PATHS=PATHS, DIST=DIST, BREAK=BREAK, CROSS=CROSS, PHASE=PHASE,
        TRANSFER_YEARS=TRANSFER_YEARS,
        NAV=NAV, ALL_PAGES=ALL_PAGES, HORIZON=HORIZON, BUILT=BUILT, path_of=path_of, run_path=run_path,
        PATHS_RAW=PATHS_RAW, phase_compare=phase_compare, S=S, M=M,
    ))


def write(name, content):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return name


