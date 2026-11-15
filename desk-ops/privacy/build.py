# -*- coding: utf-8 -*-
"""Builds privacy/index.html — the containment register.

This page is deliberately plain and deliberately blunt. It records what was published, what
the exposure was, what this change did about it, and what only the repository owner can do.
It contains no household figure and no city, street, parcel or postcode.
"""
from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parent

CSS = """
body{margin:0;font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
color:#16202b;background:#f7f9fb}
main{max-width:900px;margin:0 auto;padding:30px 22px 80px}
h1{font-size:29px;color:#1b4965;margin:.2em 0 .4em;line-height:1.2}
h2{font-size:20px;margin:2em 0 .5em;border-bottom:2px solid #dde3ea;padding-bottom:.25em}
p,li{max-width:75ch}
.lede{font-size:17.5px;color:#2b3a49}
.stop{background:#fdecea;border:1px solid #f0c3bd;border-left:5px solid #8c1c13;border-radius:8px;
padding:14px 17px;margin:16px 0}
.stop b{color:#8c1c13}
.warn{background:#fff6e5;border:1px solid #e8cf9e;border-left:5px solid #8a4b00;border-radius:8px;
padding:14px 17px;margin:16px 0}
.ok{background:#eaf6ef;border:1px solid #bfe0cd;border-left:5px solid #1e5b3a;border-radius:8px;
padding:14px 17px;margin:16px 0}
table{width:100%;border-collapse:collapse;margin:14px 0;background:#fff;font-size:14.2px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid #dde3ea;vertical-align:top}
th{background:#eef3f7;font-size:12.5px;text-transform:uppercase;letter-spacing:.04em;color:#3d4b5a}
code{background:#eef3f7;padding:1px 5px;border-radius:4px;font-size:13.5px}
pre{background:#fff;border:1px solid #dde3ea;border-radius:8px;padding:12px 14px;overflow-x:auto;
font-size:13.5px;line-height:1.5}
a{color:#2e6f95}
footer{border-top:1px solid #dde3ea;margin-top:44px;padding-top:18px;color:#5c6773;font-size:13px}
"""

ROWS = [
    ("What was published", "Sixteen separate decision sites, each restating the same household question "
     "with different numbers, all served from the repository's public web host."),
    ("The identifiers they carried", "The two cities by name, a neighbourhood by name, the county by name, "
     "and — on several desks — sales values and a monthly rent at full precision."),
    ("Why that identifies a parcel", "A sales value in a narrow city along with a rent and a year is "
     "enough to narrow the county's open assessment roll to a handful of parcels; the neighbourhood name "
     "removes most of the remainder."),
    ("Why rounding did not fix it", "The repository's rule was to round to the nearest $10. Several of the "
     "published figures were already multiples of ten, so the rule passed them through unchanged, and a "
     "rounded series of yearly assessed values still matches one parcel."),
    ("Who could see it", "Anyone. The repository is public and its web host serves the published tree to "
     "unauthenticated visitors. Nothing on the site required a login."),
    ("What this change did", "Withdrew every desk that carried household figures from publication, and "
     "replaced them with one desk that models ranges on a declared round base and publishes no household "
     "figure at any precision."),
    ("What this change cannot do", "Delete the material from the Git history, from any copy already taken, "
     "or from any search index that has crawled it. Those are separate actions, three of which only the "
     "repository owner can take."),
]

OWNER_ACTIONS = [
    ("Short term", "Make the repository private, if the history is to be kept.",
     "A private repository stops new public access and takes the served site down. It does not reach "
     "copies or caches. One setting; reversible; no data loss.", "Owner"),
    ("Short term", "Ask the hosting platform to remove the served site.",
     "If the site must stay down while the history is dealt with, disabling the published site removes "
     "the pages from the live host.", "Owner"),
    ("Medium term", "Rewrite the history to purge the figures, then force-push.",
     "This is the only way to remove the values from the repository itself. It rewrites every commit "
     "identifier, breaks every existing clone and requires every collaborator to re-clone. It is "
     "irreversible in practice and must be done deliberately, by the owner, with a backup.",
     "Owner, with a Git specialist"),
    ("Medium term", "Request removal from search engines and web archives.",
     "Most large search engines and the main web archive accept a removal request for a page that no "
     "longer exists. This reduces, but does not eliminate, the chance a cached copy surfaces.",
     "Owner"),
    ("Ongoing", "Stop writing household figures into a repository at all.",
     "The pattern that caused this is structural: analysis and data in the same public place. Keeping "
     "inputs in a private store and publishing only ratios, break-evens and code prevents a repeat.",
     "Owner, and whoever prepares the next analysis"),
    ("Ongoing", "Treat the assessed-value series as an identifier, not a statistic.",
     "A yearly series of assessed values is the most identifying data in the whole set, even rounded. It "
     "should never be published, in any form, for a property the household owns or will own.",
     "Everyone"),
]

ERRORS = [
    ("The publication boundary was documented and then crossed.",
     "The repository's own configuration file says that excluding a directory from the built site hides "
     "it but does not remove it, and that anything which must not be public has to be deleted. Sixteen "
     "directories were then approved for publication while still carrying household figures."),
    ("The privacy rule protected the wrong thing.",
     "The rule checked for decimal precision — money that was not a multiple of ten. That catches a "
     "scraped bill but not a round sales value, which is the figure that matters most."),
    ("The check ran on one directory instead of all of them.",
     "The published-surface check scanned a single curated directory for identifiers. The other fifteen "
     "published directories were never scanned, which is why city names survived on them for weeks."),
    ("Duplication hid the problem.",
     "With sixteen sites making sixteen claims, no single page was authoritative enough to audit, and "
     "each new session added a seventeenth rather than correcting the sixteen."),
    ("A rule was overstated in one desk.",
     "At least one desk described the intergenerational exclusion as protecting an assessed value "
     "permanently, when the statute removes it the moment the heir stops occupying. An overstated rule "
     "is a correctness defect, not only a privacy one."),
]


def build():
    rows = "".join(f"<tr><th>{a}</th><td>{b}</td></tr>" for a, b in ROWS)
    acts = "".join(
        f"<tr><td>{a}</td><td><b>{b}</b></td><td>{c}</td><td>{d}</td></tr>"
        for a, b, c, d in OWNER_ACTIONS)
    errs = "".join(f"<li><b>{a}</b> {b}</li>" for a, b in ERRORS)
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive,nosnippet">
<meta name="referrer" content="no-referrer">
<title>Privacy: what was exposed and what remains — inheritance decision desk</title>
<style>{CSS}</style>
</head>
<body>
<main>
<p><a href="../index.html">&larr; the decision desk</a></p>
<h1>Privacy: what was exposed, what this change did, and what remains</h1>
<p class="lede">The household asked for privacy as the highest priority. An audit of the repository
found that the published site had been carrying household figures and place names for weeks. This
page records the finding, the containment performed, and the actions that only the repository owner
can take. It contains no figure and no place name.</p>

<div class="stop">
<p><b>Read this first.</b> Withdrawing pages from a published site does not delete them from the
repository's history, from copies already taken, or from search indexes. The exposure began when the
figures were committed to a public repository; it cannot be fully undone by editing files.</p>
</div>

<h2>1. What was found</h2>
<table><tbody>{rows}</tbody></table>

<h2>2. What this change did about it</h2>
<ul>
<li><b>Withdrew sixteen desks from publication.</b> They remain in the repository as working material
but are no longer approved for the published site, and the publication gate now fails closed if a
directory carrying identifiers is approved again.</li>
<li><b>Replaced them with one desk.</b> A single operating surface that models ranges instead of
points, publishes no household figure at any precision, and carries no place name.</li>
<li><b>Extended the check from one directory to all of them.</b> The identifier and rounding scan now
runs across every published directory, not the curated one alone.</li>
<li><b>Checked what the model's conclusions actually depend on, and published the test.</b> The
first claim was that the conclusions were independent of the modelling base. The test suite
disproved it — a fixed statutory cap makes the break-even rise slightly with property value — and
both the claim and the page were corrected. What is asserted now is the narrower, true statement:
the ranking is identical across a tenfold range of bases and the break-even moves by less than a
percentage point across it. Publishing the test is the point: a claim about privacy that is not
tested is the same kind of assurance that produced the original problem.</li>
<li><b>Recorded the finding on the desk itself.</b> The flagged page lists the repository-level
irregularities, so a future reader sees them rather than inheriting them.</li>
</ul>

<div class="ok"><b>What is now true of the published site.</b> No name, street, parcel number, postcode,
city or neighbourhood; no sales value, rent or assessed value from the household's records at any
precision; no script, form or external asset on any page. This is enforced by a verifier that fails the
build, not by a promise.</div>

<h2>3. What remains exposed, and who can fix it</h2>
<table>
<thead><tr><th>When</th><th>Action</th><th>What it does, and what it costs</th><th>Who</th></tr></thead>
<tbody>{acts}</tbody></table>

<div class="warn"><b>The strongest recommendation on this page.</b> If the household wants the figures
gone rather than merely unpublished, the repository should be made private before anything else is
attempted. It is one setting, it takes effect immediately, it loses nothing, and every other option
below stays available afterwards. Leaving it public while deciding is the one choice that has no
upside.</div>

<h2>4. How this happened — five findings, so it does not repeat</h2>
<ol>{errs}</ol>

<h2>5. What the household can do today</h2>
<ol>
<li><b>Make the repository private.</b> The single highest-value action, and the only one that stops
new access immediately.</li>
<li><b>Decide whether to rewrite the history.</b> This is a genuine trade: permanent removal against
broken clones and a rewritten repository. Either answer is defensible; leaving it undecided is not,
because the material stays public while it is undecided.</li>
<li><b>Keep the household's own inputs out of the repository.</b> Future analysis should read them from
a private store and publish only the model outputs whose privacy properties have been tested.</li>
<li><b>Ask for the old pages to be removed from search engines and archives</b> once they stop
resolving. It reduces the chance of a cache, and it is free.</li>
</ol>

<div class="warn"><b>A note on what this page does not claim.</b> It does not claim that no copy
exists elsewhere, that a search engine never indexed the pages, or that the figures are now
unrecoverable. It claims that they are no longer published here, that the mechanism which published
them has been removed, and that the remaining exposure is named with the action that would close it.</div>

<footer>
<p><b>Reproducing this page.</b> <code>python3 desk-ops/privacy/build.py</code>. The page contains no
household figure by construction — the builder refuses to write a file containing a digit pattern
longer than a statute number.</p>
<p><a href="../index.html">The decision desk</a> · <a href="../desk-ops/flagged.html">Flagged for review</a>
</p>
</footer>
</main>
</body>
</html>
"""
    return html


if __name__ == "__main__":
    target = OUT / "index.html"
    target.write_text(build(), encoding="utf-8")
    print(f"wrote {target}")
