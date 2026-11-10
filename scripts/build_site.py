#!/usr/bin/env python3
"""Wrap src/pages/*.html partials in the shared shell -> pages/*.html.

Partial format (first lines are front matter comments):
  <!--title: Property tax-->
  <!--json: data/property-tax.json-->
  <!--blurb: one line shown under the H1-->
  ...body html...
Run: python3 scripts/build_site.py
"""
import os
import re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HERE, "src", "pages")
OUT = os.path.join(HERE, "pages")

NAV = [
    ("index.html", "Overview", "index"),
    ("pages/executive-summary.html", "Executive summary", "executive-summary"),
    ("pages/scenarios.html", "Options", "scenarios"),
    ("pages/projections.html", "Projections", "projections"),
    ("pages/property-tax.html", "Property tax", "property-tax"),
    ("pages/inheritance-tax.html", "Inheritance tax", "inheritance-tax"),
    ("pages/inheritance-process.html", "Process", "inheritance-process"),
    ("pages/operating-costs.html", "Costs", "operating-costs"),
    ("pages/law-watch.html", "Law watch", "law-watch"),
    ("pages/sources.html", "Sources", "sources"),
    ("pages/flagged.html", "Flagged", "flagged"),
    ("pages/methodology.html", "Method", "methodology"),
]

SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Inheritance decision dashboard</title>
<meta name="description" content="{blurb}">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body data-page="{page}" data-root="../"{json_attr}>
<header class="top">
  <div class="top-in">
    <div class="brand"><span class="dot"></span> Inheritance decision dashboard</div>
    <nav class="main">
{nav}
    </nav>
  </div>
</header>
<div class="wrap">
{body}
  <footer>
    Reviewed 10 November 2026. Statutory figures are quoted as published; anything computed or projected is rounded to
    the nearest $10. Not legal, tax or investment advice. <a href="../pages/methodology.html">Methodology</a> ·
    <a href="../pages/sources.html">Sources</a> · <a href="../pages/flagged.html">Flagged for review</a>
  </footer>
</div>
<script src="../assets/app.js"></script>
</body>
</html>
"""


def build():
    os.makedirs(OUT, exist_ok=True)
    for name in sorted(os.listdir(SRC)):
        if not name.endswith(".html"):
            continue
        slug = name[:-5]
        raw = open(os.path.join(SRC, name), encoding="utf-8").read()
        meta = {}
        for key in ("title", "json", "blurb", "page"):
            m = re.search(r"<!--%s:\s*(.*?)-->" % key, raw, re.S)
            if m:
                meta[key] = m.group(1).strip()
        body = re.sub(r"<!--(title|json|blurb|page):.*?-->", "", raw, flags=re.S).strip()
        nav = []
        for href, label, key in NAV:
            cur = ' aria-current="page"' if key == meta.get("page", slug) else ""
            nav.append('      <a href="../%s"%s>%s</a>' % (href, cur, label))
        html = SHELL.format(
            title=meta.get("title", slug),
            blurb=meta.get("blurb", ""),
            page=meta.get("page", slug),
            json_attr=(' data-json="%s"' % meta["json"]) if meta.get("json") else "",
            nav="\n".join(nav),
            body=body,
        )
        with open(os.path.join(OUT, slug + ".html"), "w", encoding="utf-8") as f:
            f.write(html)
        print("built pages/%s.html" % slug)


if __name__ == "__main__":
    build()
