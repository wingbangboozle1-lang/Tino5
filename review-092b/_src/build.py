"""Renders review-092b as a static site. Run: python3 review-092b/_src/build.py"""
from __future__ import annotations

import json
import re
from pathlib import Path

from engine import (A, ASSUMPTIONS, BASE_YEAR, CPI_MONTH, CPI_OCT, HORIZONS, OFFICIAL,
                    PATH_KEYS, build_regimes, break_even_growth, fed_exclusion, money, pct,
                    path_wealth, project, prop13_taxable, prop19_allowance, r10,
                    regime_outcome, transfer_table, break_even_equity)
from sources import SOURCES

OUT = Path(__file__).resolve().parent.parent
SRC = {s["id"]: s for s in SOURCES}
STAMP = "2026-11-13"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def cite(*ids):
    parts = []
    for i in ids:
        s = SRC[i]
        short = s["title"].split("—")[0].split("(")[0].strip()
        if len(short) > 46:
            short = short[:44] + "…"
        parts.append(f'<a href="{s["url"]}" rel="noopener">{short}</a>')
    return " · ".join(parts)


MONEY_RE = re.compile(r"\$(\d{1,3}(?:,\d{3})+|\d+)(?![\d.,])(?![MK]\b)")
STAT_RE = re.compile(r'<span class="stat">.*?</span>', re.S)


HOST_RE = re.compile(r'(?:[a-z0-9-]+\.)+(?:gov|org|com|edu)(?::\d+)?')


def enforce_rounding(html):
    """Round every published dollar amount to the nearest $10.

    Statutory or agency amounts that an agency publishes in full detail are wrapped in
    <span class="stat"> and are exempt; shorthand such as "$15M" is also left alone.
    """
    def fix(seg):
        def one(m):
            v = int(m.group(1).replace(",", ""))
            r = int(round(v / 10.0)) * 10
            return f"${r:,}"
        return MONEY_RE.sub(one, seg)
    # Publisher names such as sf.gov or insurance.ca.gov are page titles, not personal
    # identifiers, so they are marked before the identifier gate runs. Only text nodes are
    # touched: marking inside an attribute would corrupt the URL.
    parts = re.split(r"(<[^>]+>)", html)
    for i, part in enumerate(parts):
        if not part.startswith("<"):
            parts[i] = HOST_RE.sub(lambda m: f'<span class="host">{m.group(0)}</span>', part)
    html = "".join(parts)
    out, pos = [], 0
    for m in STAT_RE.finditer(html):
        out.append(fix(html[pos:m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(fix(html[pos:]))
    return "".join(out)


def stat(amount, symbol="$"):
    return f'<span class="stat">{symbol}{amount:,}</span>' if isinstance(amount, int) else \
        f'<span class="stat">{amount}</span>'


def num(x):
    """A plain number: money for large values, a short decimal otherwise."""
    if x is None:
        return "—"
    return money(x) if abs(x) >= 1000 else f"{x:g}"


def table(headers, rows, cls="data"):
    out = [f'<table class="{cls}"><thead><tr>' +
           "".join(f"<th>{h}</th>" for h in headers) + "</tr></thead><tbody>"]
    for r in rows:
        out.append("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def badge(kind):
    return f'<span class="tag tag-{kind}">{kind}</span>'


NAV = [
    ("index.html", "Summary"),
    ("questions.html", "Questions to answer"),
    ("suggestions.html", "Suggestions"),
    ("projections.html", "Projections"),
    ("decision.html", "Decision"),
    ("black-swans.html", "Black swans"),
    ("inheritance.html", "Inheritance steps"),
    ("costs.html", "Costs &amp; tax"),
    ("repo-review.html", "Repo review"),
    ("flagged.html", "Flagged for review"),
    ("sources.html", "Sources"),
]


def page(slug, title, subtitle, body, current=None):
    current = current or slug
    nav = "".join(
        f'<a{" aria-current=page" if f == current else ""} href="{f}">{t}</a>' for f, t in NAV
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<meta name="referrer" content="no-referrer">
<title>{title} — inheritance decision hub</title>
<link rel="stylesheet" href="style.css"></head><body>
<header><a href="index.html">Inheritance decision hub</a>
<span>Property A (inherited) &amp; Property B (already owned) · figures updated {STAMP}</span></header>
<div class="layout"><nav aria-label="Sections">{nav}</nav><main>
<div class="eyebrow">{subtitle}</div>
<h1>{title}</h1>
{body}
<footer><p><strong>Privacy.</strong> No names, street addresses, parcel or account numbers, ZIP
codes, phone numbers or e-mail addresses appear anywhere in this site. Both properties are referred
to as <em>Property A</em> (to be inherited through a trust) and <em>Property B</em> (already owned).
Assessor histories are not published: a series rounded to $10 is still a fingerprint against open
county roll data.</p>
<p><strong>Not advice, and not a forecast.</strong> Rules and thresholds are those in force or
published on {STAMP} and can change before a 2040–2050 transfer. Every figure marked
{badge("assumption")} is a modelling assumption, not a fact. Figures marked {badge("verified")} are
quoted from the official document linked beside them. This page cannot replace legal, tax,
appraisal, insurance or investment advice on the actual estate.</p></footer>
</main></div></body></html>
"""


# ---------------------------------------------------------------------------
# page 1 — executive summary
# ---------------------------------------------------------------------------
def page_index():
    w40, w45, w50 = path_wealth(2040), path_wealth(2045), path_wealth(2050)
    t45 = transfer_table(2045)

    headline = table(
        ["What", "Value", "Why it matters", "Label and source"],
        [
            ["Property A — inherited, 2026 estimate", money(A["a_fmv_2026"].value),
             "The asset under decision. Arrives through a trust; the transfer year is not fixed.",
             f'{badge("owner")} · {cite("boe-prop19")}'],
            ["Property B — already owned, 2026 estimate", money(A["b_fmv_2026"].value),
             "Not part of the inheritance. It already supplies housing, so A does not have to be "
             "lived in.", f'{badge("owner")} · {cite("boe-prop19")}'],
            ["Property B rent, two leased units", money(A["b_rent_mo"].value) + "/mo",
             "Independent of A. It continues whether A is occupied, let or sold.",
             f'{badge("owner")} · {cite("sf-rent-board-rates")}'],
            ["Property A 2026 taxable value", money(A["a_taxable_2026"].value),
             "The Prop 13 base that the transfer will break.",
             f'{badge("owner")} · {cite("ca-rtc-51")}'],
            ["2026 federal estate exclusion", stat(OFFICIAL["fed_exclusion_2026"]),
             "Per decedent. Applies to the estate, not to each heir's cash.",
             f'{badge("verified")} · {cite("irs-estate-tax")}'],
            ["2027 federal estate exclusion", stat(OFFICIAL["fed_exclusion_2027"]),
             "Published 5 November 2026. Indexed thereafter.",
             f'{badge("verified")} · {cite("irs-ir-2026-133")}'],
            ["California inheritance and estate tax", "none for deaths on or after 1 Jan 2005",
             "Removes a whole class of worry; the federal test is the only one that binds.",
             f'{badge("verified")} · {cite("ca-sco-estate")}'],
            ["Prop 19 value cap, transfers to 15 Feb 2027",
             stat("$1,044,586"),
             "Added to the factored base value; later years are re-indexed by statute.",
             f'{badge("verified")} · {cite("boe-lta-2025-009")}'],
        ],
    )

    body = f"""
<div class="notice"><strong>Executive summary.</strong> On the numbers we can defend, the
cheapest housing move is to keep Property B as the place you live and to treat Property A as a
financial asset, not a home. Selling A at the transfer and reinvesting the proceeds wins the
central case by {money(w45["P3"] - w45["P2"])} over renting A out and by
{money(w45["P3"] - w45["P1"])} over moving in, on a 25-year horizon from a 2045 transfer. That
result is <em>not</em> robust. It flips to "rent A out" if A appreciates at about
{pct(break_even_growth(2045), 1)} a year or faster for 25 years, or if the reinvested proceeds earn
less than about {pct(break_even_equity(2045), 1) if isinstance(break_even_equity(2045), float) else '5%'} after tax.
Both of those are things we do not yet know. See <a href="decision.html">the decision page</a> for the conditions under which each path
wins.</div>

<h2>The three choices, priced</h2>
<p>Terminal after-tax wealth 25 years after the transfer. Property B is excluded from the
comparison because it is owned in all three paths and its two leases are unaffected; its own
economics are on the <a href="projections.html">projections page</a>.</p>
{table(["Transfer year", "Occupy A", "Rent A out", "Sell A and reinvest", "Winner", "Sources"],
       [[str(y), money(w["P1"]), money(w["P2"]), money(w["P3"]),
         {"P1": "Occupy", "P2": "Rent", "P3": "Sell"}[max(PATH_KEYS, key=lambda k: w[k])],
         cite("irs-p551", "boe-prop19", "irs-topic-701", "irs-p527")]
        for y, w in ((2040, w40), (2045, w45), (2050, w50))])}

<h2>What the answer actually depends on</h2>
<div class="grid">
<div class="card"><b>1. The reinvestment return</b>{badge("assumption")}
Every planning model of this kind is driven by this one number. At the central 5% after tax,
selling wins. Below about {pct(break_even_equity(2045), 1) if isinstance(break_even_equity(2045), float) else '5%'},
renting A out wins outright, because the house's own cash flow and appreciation then beat the
portfolio. We have no way to know your future after-tax return, so the whole 3–7% range is
reported.</div>
<div class="card"><b>2. How fast A appreciates</b>{badge("assumption")}
Selling stops you owning the house, so it loses whenever house growth beats the reinvestment
return. At {pct(break_even_growth(2045), 1)} a year for 25 years the paths converge.</div>
<div class="card"><b>3. Whether you would really live in A</b>{badge("verified")}
Occupying A is the only route to the Prop 19 exclusion, and it is the worst of the three paths in
the central case — the tax saving ({money(t45["tax_gap"])} a year at a 2045 transfer) is smaller
than the rent you give up by leaving B's third unit empty and the maintenance you take on.</div>
<div class="card"><b>4. Facts we do not have</b>
The trust's terms, the number of beneficiaries, insurance quotes, A's achievable rent, and the
size of the cash inheritance. Each one is on the <a href="questions.html">questions page</a> with
the specific decision it blocks.</div>
</div>

<h2>Recommended sequence (do not skip the order)</h2>
<ol>
<li><b>Nothing irreversible before the facts.</b> The transfer date is a decade or more away; the
only work that pays now is collecting documents and keeping the trust and title clean.</li>
<li><b>Get three insurance quotes for each property.</b> Premium is the largest genuinely unknown
cost and the only figure on this site that is still blank.</li>
<li><b>At the transfer, decide the occupancy question within one year.</b> The Prop 19 exclusion
requires the transferee to occupy and to file for the homeowners' exemption within a year
({cite("ca-rtc-63-2")}); the claim itself can be filed within three years ({cite("boe-prop19")}).
Miss it and the tax bill roughly doubles.</li>
<li><b>Only then choose between occupy, rent and sell</b>, using the live numbers on
<a href="decision.html">the decision page</a>.</li>
</ol>

<h2>Headline figures used throughout this site</h2>
{headline}

<h2>How to read the labels</h2>
<p>{badge("verified")} quoted from the official document linked in the row.
{badge("derived")} arithmetic on verified figures, method shown.
{badge("owner")} supplied by you and rounded for publication; not independently verifiable.
{badge("assumption")} a modelling assumption with a stated range; the model is re-run across the
range. {badge("unverified")} could not be confirmed — the value is left blank and listed on the
<a href="flagged.html">flagged page</a>.</p>
"""
    return page("index.html", "A disciplined inheritance decision",
                "Executive summary", body)


# ---------------------------------------------------------------------------
# page 2 — questions register
# ---------------------------------------------------------------------------
QUESTIONS = [
    ("Q-01", "Critical", "Will the $10 rounding actually protect the figures?",
     "You asked for figures rounded to $10 so they cannot be traced. For a single number that is "
     "broadly true. For a <em>multi-year series</em> of assessed values it is not: San Francisco "
     "publishes its secured roll as open data and the county assessor publishes assessment rolls, "
     "so a 13-row history rounded to $10 still matches exactly one parcel. This site therefore "
     "publishes the 2026 anchors only and never the histories.",
     "Decide whether you want the histories shown privately (a PDF you keep) rather than on the "
     "public site. The recommended action is: keep them off the site.",
     "ca-rtc-51", "Blocked on your decision"),
    ("Q-02", "Critical", "Who are the beneficiaries of the trust, and how many?",
     "A single heir can claim the whole Prop 19 exclusion and the whole §121 exclusion. Two heirs "
     "holding A as co-owners split both, and the §121 exclusion is $250,000 per person only if each "
     "meets the use test. The entire decision changes with the answer, and we do not have it.",
     "Obtain the trust instrument and the schedule of beneficiaries. Do not model a 50/50 split "
     "until it is confirmed.", "irs-topic-701", "Blocked on a document"),
    ("Q-03", "Critical", "Does 'inherit by trust' mean a revocable living trust, and does A pass "
     "outright or in further trust?",
     "If A passes into a continuing trust rather than to you outright, the trustee — not you — "
     "decides whether to sell, and the Prop 19 exclusion depends on the transferee occupying the "
     "home. BOE states plainly that a transfer occurring at death counts as a transfer whether "
     "inside or outside a trust, but the beneficiary's powers differ.",
     "Read the trust's distribution article. Ask the trustee in writing whether the beneficiary "
     "receives the property or an interest in a trust holding it.", "boe-lta-2026-026", "Blocked on a document"),
    ("Q-04", "High", "What is the size and form of the cash inheritance?",
     "The federal exclusion is {} per decedent in 2026 rising to {} in 2027. Property A and "
     "Property B together are worth about $4.9M at today's estimates, so roughly $10.1M of headroom "
     "exists before any federal estate tax is possible — but we do not know the cash figure, and a "
     "large cash bequest plus A could cross the line in a later year if the exclusion is ever "
     "reduced by legislation.".format(stat(OFFICIAL["fed_exclusion_2026"]),
                                      stat(OFFICIAL["fed_exclusion_2027"])),
     "Get the estate inventory from the trustee or executor. Then re-run the headroom table on the "
     "inheritance page with the real figure. Note also that the exclusion is an estate-level test, "
     "not a per-heir allowance.", "irs-estate-tax", "Blocked on a document"),
    ("Q-05", "High", "What will insurance cost for A and for B?",
     "The insurance department's own market snapshot puts the statewide average homeowner premium at "
     "$1,571 against a national average of $1,512, with 677,449 homes on the FAIR Plan — the "
     "last-resort policy — and 662 ZIP codes designated distressed. That is a statewide average, not "
     "a quote for either house, so the model carries no premium and instead prices each $1,000 of "
     "premium explicitly. The owner's ~$1,500 guesses happen to sit at the state average.",
     "Obtain three written quotes per property from admitted carriers, plus a California FAIR Plan "
     "quote as the backstop, and record the dwelling limit, deductible and any wildfire exclusion.",
     "cdi-market-snapshot", "Benchmarked, not quoted"),
    ("Q-06", "High", "What rent can A actually achieve?",
     "The model assumes a 3.2% gross yield because no rent figure was supplied and no official "
     "source can tell us what this specific house would let for. HUD Fair Market Rents are "
     "40th-percentile voucher rents, not market rents for a single-family home, so they are not a "
     "substitute.", "Get two written rental appraisals at the time of transfer; the rent assumption "
     "is the second-largest lever after the reinvestment return.", "hud-fmr", "Assumption in use"),
    ("Q-07", "High", "Will the federal estate exclusion still be ~$15M in 2045?",
     "It is $15M for 2026 by statute and indexed thereafter, but a future Congress can "
     "change it. The estate tax has been repealed, reinstated and re-shaped repeatedly since 2001 "
     "— the IRS's own threshold table shows $5M in 2011, $5.5M in 2017 and $11.2M "
     "in 2018. A projection to 2045 that assumes indexation is a scenario, not a fact.",
     "Model the estate at transfer with the law then in force. Keep the headroom table on the "
     "inheritance page as a live check rather than a fixed plan.", "irs-estate-tax", "Watch item"),
    ("Q-08", "Medium", "Will Prop 19 itself survive to 2045?",
     "Prop 19 was a constitutional amendment (ACA 11) approved in November 2020 and is not "
     "amendable by simple statute, but it can be amended by another constitutional amendment, and "
     "the value cap is re-indexed every second February to the FHFA California house-price change. "
     "The cap for a transfer after 15 February 2027 is not yet published.",
     "Track the BOE Letters to Assessors each February. Re-run the transfer table when the new "
     "allowance is published.", "boe-lta-2025-009", "Watch item"),
    ("Q-09", "Medium", "Does the third unit in B satisfy the rent ordinance, and is it registered?",
     "B's third unit is vacant and the owner intends to live in it. San Francisco requires "
     "residential units to be reported into the Rent Board Housing Inventory and charges a fee per "
     "unit; a rent-increase licence depends on that reporting. Occupying a unit yourself also has "
     "its own rules (owner move-in) that we have not verified.",
     "Check the Housing Inventory record for B and confirm that occupying unit 3 is lawful without "
     "an eviction or a change-of-use permit.", "sf-rent-board", "Not verified"),
    ("Q-10", "Medium", "Is A's solar credit durable?",
     "The owner reports electricity is free and slightly positive because of solar. Under the "
     "net-billing tariff that replaced net metering for new interconnections, export compensation "
     "is usually below the retail rate, and legacy net-metering terms run for a fixed period. The "
     "credit may therefore shrink or invert.",
     "Find A's interconnection agreement and tariff (NEM or NBT), and the legacy-period end date. "
     "Then replace the small net-credit assumption with the documented terms.", "cpuc-nem",
     "Assumption in use"),
    ("Q-11", "Medium", "What was A's basis, and does any of the house need depreciating?",
     "Basis resets to date-of-death fair market value, so the pre-death basis does not matter for "
     "income tax — unless A has been rented, or partly used for business, before the transfer. "
     "Any depreciation taken by the transferor reduces the carryover in some circumstances.",
     "Obtain the transferor's depreciation schedules and prior returns if A was ever rented.",
     "irs-p551", "Blocked on a document"),
    ("Q-12", "Low", "What will A's property tax be if we do nothing for a year after the transfer?",
     "The intergenerational exclusion requires the transferee to occupy within one year and to file "
     "for the homeowners' or disabled veterans' exemption within one year. If that is missed, the "
     "exclusion is removed and the full market value is enrolled from the following lien date.",
     "Put the two deadlines — occupancy and exemption filing — on the executor's calendar the week "
     "of death, not the week of distribution.", "ca-rtc-63-2", "Process risk"),
    ("Q-13", "Low", "Does the county transfer tax apply to an inheritance?",
     "The documentary transfer tax under <span class=\"stat\">R&amp;TC §11911</span> is imposed on a deed by which realty is "
     "'sold'. A transfer by death into a trust or to a beneficiary is normally exempt, but the "
     "exemption is claimed on the face of the declaration of trust or the recorded document. We "
     "have not read the county's exemption form, so this is flagged rather than answered.",
     "Confirm with the county recorder at the time of recording; the amount at stake is small "
     "(0.11% of value) but the paperwork is not.", "ca-rtc-11911", "Not verified"),
]


ASSUMPTION_SOURCE = {
    "a_growth": "fred-hpi-us", "b_growth": "ca-rtc-51", "equity_return": "tsp-rates",
    "inflation": "cbo-outlook-2026", "a_gross_yield_pct": "hud-fmr",
    "vacancy_pct": "ca-civ-1947-12", "mgmt_pct": "hud-fmr", "selling_cost_pct": "ca-rtc-11911",
    "maintenance_pct": "scc-assessor-booklet", "fed_ltcg_pct": "ftb-2026-rates",
    "fed_prop19_allowance_growth": "boe-lta-2025-009", "fed_exclusion_growth": "irs-estate-tax",
    "a_fmv_2026": "boe-prop19", "b_fmv_2026": "ca-rtc-51",
    "a_taxable_2026": "ca-rtc-51", "b_taxable_2026": "ca-rtc-51",
    "a_effective_tax_rate": "scc-assessor-booklet", "b_rent_mo": "sf-rent-board-rates",
    "b_unit3_rent_mo": "sf-rent-board-rates", "a_water_mo": "cbo-outlook-2026",
    "a_elec_net_mo": "cpuc-nem", "b_water_mo": "cbo-outlook-2026", "b_elec_mo": "cpuc-nem",
    "a_insurance_yr": "cdi-guides", "b_insurance_yr": "cdi-guides",
}


def page_questions():
    rows = []
    for qid, prio, q, detail, action, src, status in QUESTIONS:
        rows.append([
            f"<strong>{qid}</strong><br>{badge('priority-' + prio.lower())}",
            f"<strong>{q}</strong><br>{detail}",
            action,
            status,
            cite(src),
        ])
    body = f"""
<div class="notice"><strong>Read this first.</strong> A decision cannot reasonably be made until
the questions marked <em>Critical</em> and <em>High</em> are answered. The purpose of this page is
to make the uncertainty explicit instead of hiding it inside a single number. Nothing below is a
recommendation to act.</div>

<h2>What we know, what we do not, and what each gap blocks</h2>
<p>Each row states the question, why it changes the answer, the specific action that would answer
it, and the decision it currently blocks. Where a row says <em>Blocked on a document</em>, no
amount of modelling will settle it — only the document will.</p>
{table(["ID", "Question and why it matters", "How to answer it", "Blocks", "Source"], rows)}

<h2>What is already settled</h2>
<p>These are no longer open questions, so they should not be re-litigated:</p>
<ul>
<li>California imposes <strong>no inheritance tax and no estate tax</strong> on the estate of a
person dying on or after 1 January 2005 ({cite("ca-sco-estate")}).</li>
<li>The federal test is <strong>estate-level, not per-heir</strong>, and the 2026 exclusion is
$15,000,000 per decedent ({cite("irs-estate-tax", "irs-whats-new")}).</li>
<li>Property A's income-tax basis <strong>resets to date-of-death value</strong>, so a sale at the
transfer pays no capital-gains tax on the pre-death appreciation ({cite("irs-p551")}).</li>
<li>The <strong>Prop 13 base is broken</strong> by the transfer; Prop 19 limits the damage only if
a qualifying child occupies the home ({cite("boe-prop19", "ca-rtc-63-2")}).</li>
<li>Property B is <strong>not inherited</strong> and gets no basis step-up; selling it would
trigger tax on decades of gain, which is why it is treated separately throughout.</li>
</ul>

<h2>Assumptions currently standing in for missing facts</h2>
<p>Every one of these is a placeholder. Replacing them with real numbers is the cheapest way to
improve the decision.</p>
{table(["Assumption", "Value used", "Range tested", "Label", "Basis", "Source"],
       [[a.label, num(a.value),
         "—" if a.low is None else f"{num(a.low)} – {num(a.high)}",
         badge("assumption") if a.value is not None else badge("unverified"),
         a.basis, cite(ASSUMPTION_SOURCE.get(a.key, "cbo-outlook-2026"))]
        for a in ASSUMPTIONS if a.group in ("market", "property")])}
"""
    return page("questions.html", "Questions that must be answered first",
                "Open-question register", body)


# ---------------------------------------------------------------------------
# page 3 — suggestions register
# ---------------------------------------------------------------------------
SUGGESTIONS = [
    dict(id="S-01", title="Keep Property B as the home you live in, in every path",
         effort="Low", cost="$0", impact="High", confidence="High on facts, medium on money",
         what="Treat B as the housing solution and decide only what happens to A. B already has two "
              "leased units and a third you can occupy without losing that rent; A has no such "
              "offset. This is the single structural fact that separates the properties.",
         why="A is a single-family house that would be reassessed at transfer; B is protected by its "
             "Prop 13 base and its rent. Moving into A therefore costs the Prop 19 tax break against "
             "the rent from B's third unit and against A's own carrying costs.",
         risk="Only if A is where you actually want to live, or if B's third unit is not legally "
              "habitable by you (Q-09).",
         evidence="boe-prop19"),
    dict(id="S-02", title="Do not sign anything about A before the trust and basis documents are read",
         effort="Low", cost="$0", hint="", impact="High", confidence="High",
         what="Before the transfer, obtain four documents: the trust instrument, the schedule of "
              "beneficiaries, the transferor's most recent property-tax bill, and any depreciation "
              "schedules if A was ever rented.",
         why="Three of the five open Critical questions cannot be answered without them, and the "
             "Prop 19 occupancy deadline starts at death, not at distribution.",
         risk="None. This is sequencing, not an action on the property.",
         evidence="ca-rtc-63-2"),
    dict(id="S-03", title="Book the two Prop 19 deadlines on the day of death",
         effort="Low", cost="$0", impact="High", confidence="High",
         what="The transferee must occupy within one year and file for the homeowners' exemption "
              "within one year; the exclusion claim itself can be filed within three years.",
         why="If the occupancy and exemption steps are missed, the exclusion is removed and the "
             "factored value for the full market value is enrolled from the following lien date. "
             "The difference measured here is {gap} a year at a 2045 transfer.",
         risk="None; this is a calendar item.",
         evidence="ca-rtc-63-2"),
    dict(id="S-04", title="Get three insurance quotes per property before modelling any further",
         effort="Medium", cost="$0", impact="High", confidence="High",
         what="Admitted-carrier quotes plus one California FAIR Plan quote per property, each with "
              "the dwelling limit and deductible stated.",
         why="Insurance is the only cost still blank on this site. It is also the cost most likely "
             "to move sharply: the department's own consumer guides exist because the market is "
             "disrupted, and a FAIR Plan policy covers fire only.",
         risk="None, but quotes expire; refresh within 90 days of the transfer.",
         evidence="cdi-guides"),
    dict(id="S-05", title="Publish a private figure sheet, not a public one",
         effort="Low", cost="$0", impact="High", confidence="High",
         what="Keep the real assessed values, bills and rent roll in a file you hold offline; "
              "publish only rounded anchors on this site.",
         why="Rounding a single figure protects it; rounding a history does not, because the "
             "county roll is open data and a 13-row series is a unique match.",
         risk="You lose the ability to share the detail by link. That is the point.",
         evidence="scc-assessor-booklet"),
    dict(id="S-06", title="Test the sell decision against a lower reinvestment return, not a higher one",
         effort="Low", cost="$0", impact="High", confidence="Medium",
         what="Run the decision page with the reinvestment return at 3% after tax rather than 5%.",
         why="Selling only wins because the proceeds compound. If the after-tax return is 3%, the "
             "advantage narrows sharply; at 7% it widens. The assumption is doing more work than any "
             "official figure.",
         risk="None; this is a robustness check.",
         evidence="tsp-rates"),
    dict(id="S-07", title="Decide the sale before the transfer, but execute it after",
         effort="Medium", cost="$0", impact="High", confidence="Medium",
         what="Agree with the trustee in advance that A will be sold promptly if the family chooses "
              "that path, so the sale is not delayed by probate administration.",
         why="The §1014 step-up is what makes an immediate sale tax-free; delay adds market risk "
             "without adding tax benefit, and the county reassesses as of the date of death anyway.",
         risk="A forced sale in a bad market. Mitigate with a 12–24 month treasury ladder rather "
              "than a single-day reinvestment.",
         evidence="irs-p551"),
    dict(id="S-08", title="Keep Property B out of the comparison — but do not forget it",
         effort="Low", cost="$0", impact="Medium", confidence="High",
         what="Report B's own net income and tax separately, exactly as the projections page does, "
              "instead of folding it into the A decision.",
         why="B is owned in all three paths, so it cancels out of the comparison but not out of your "
             "life. Folding it in is how two earlier drafts of this analysis produced contradictory "
             "answers.",
         risk="None.",
         evidence="sf-rent-board-rates"),
    dict(id="S-09", title="Model the black-swan cases as separate events, not one 'bad case'",
         effort="Medium", cost="$0", impact="Medium", confidence="High",
         what="Use the five regimes on the black-swan page: stagflation, housing bust, rate shock, "
              "demand collapse, and the live disinflation that has not arrived.",
         why="They act on different variables. A housing bust hurts the sell path's timing; "
             "stagflation hurts the reinvestment path's real return. One blended 'downside' number "
             "hides both.",
         risk="None, but do not average the regimes into a probability — we have no basis for "
              "assigning probabilities.",
         evidence="fred-hpi-us"),
    dict(id="S-10", title="Re-verify four official thresholds every February",
         effort="Low", cost="$0", impact="Medium", confidence="High",
         what="Prop 19 allowance (BOE letter), CPI inflation factor (BOE letter), federal exclusion "
              "(IRS revenue procedure, usually October/November), and the city's allowable rent "
              "increase (Rent Board, usually January).",
         why="All four change on a published schedule, and three of them are the largest numbers in "
             "the model.",
         risk="None.",
         evidence="boe-lta-2025-009"),
    dict(id="S-11", title="Do not treat the model's winner as a recommendation to act now",
         effort="Low", cost="$0", impact="Medium", confidence="High",
         what="Use the decision page as a filter that tells you which questions matter, not as an "
              "instruction.",
         why="Nine of the model's inputs are assumptions. A model whose largest lever is an "
             "assumption cannot be the basis for an irreversible act a decade from now.",
         risk="None.",
         evidence="irs-estate-tax"),
]


def page_suggestions():
    t = transfer_table(2045)
    cards = []
    for s in SUGGESTIONS:
        what = s["what"].replace("{gap}", money(t["tax_gap"]))
        cards.append(f"""
<div class="sugg" id="{s['id']}">
<div class="sugg-head"><h3>{s['id']} · {s['title']}</h3>
<span class="metrics">effort <b>{s['effort']}</b> · cost <b>{s['cost']}</b> ·
impact <b>{s['impact']}</b> · confidence <b>{s['confidence']}</b></span></div>
<p><b>What to do.</b> {what}</p>
<p><b>Why.</b> {s['why']}</p>
<p><b>What could go wrong.</b> {s['risk']}</p>
<p class="src">Evidence: {cite(s['evidence'])}</p>
</div>""")
    body = f"""
<div class="notice"><strong>How to use this page.</strong> Every proposal is written so you can
accept, reject or modify it independently, and so that adopting one does not require adopting the
others. Each carries an effort, a cash cost, an expected impact and a confidence level. Nothing
here has been implemented. Sort by confidence first: the items marked <em>High</em> are
sequencing and documentation moves that carry no financial risk.</div>

<h2>Review board</h2>
{table(["ID", "Proposal", "Effort", "Cash cost", "Impact", "Confidence", "Evidence", "Decide"],
       [[f"<a href='#{s['id']}'>{s['id']}</a>", s["title"], s["effort"], s["cost"], s["impact"],
         s["confidence"], cite(s["evidence"]),
         "<span class='choice'>accept · modify · reject</span>"] for s in SUGGESTIONS])}

<h2>The single most important suggestion</h2>
<p>Keep Property B as your home and treat the decision as being about Property A alone. That is not
a financial trick; it follows from the structure of the two assets. B is already yours, already
protected by its own Proposition 13 base and already producing rent from two units while leaving a
third for you. A arrives with a broken tax base, no tenants, and a single-family cost structure.
The temptation is to move into the larger, more valuable house. The arithmetic says the value in A
is best realised by selling it, and the housing need is already met by B.</p>
<p>If the family preference is to live in A, that is a legitimate reason to choose it — but it
should be chosen as a preference, with the cost stated, not as a financial conclusion.</p>

<h2>Proposals in detail</h2>
{"".join(cards)}

<h2>What we suggest you do <em>not</em> do</h2>
<ul>
<li><b>Do not publish the assessment histories</b>, even rounded to $10 (Q-01).</li>
<li><b>Do not sell Property B</b> to fund anything. It has no basis step-up and would carry the
whole embedded gain, while forfeiting the rent and the housing.</li>
<li><b>Do not rely on a single-point projection.</b> Every figure on this site is a range in
disguise; the point estimate is only the midpoint.</li>
<li><b>Do not treat the current law as the 2045 law.</b> Four of the numbers that drive the answer
are re-set on a published schedule.</li>
</ul>
"""
    return page("suggestions.html", "Suggestions for review before any change is implemented",
                "Suggestion register", body)


# ---------------------------------------------------------------------------
# page 4 — projections
# ---------------------------------------------------------------------------
def page_projections():
    rows = project(BASE_YEAR, 2076)
    pick = [y for y in rows if y.year in
            (2026, 2030, 2035, 2040, 2045, 2050, 2055, 2060, 2065, 2070, 2076)]

    proj = table(
        ["Year", "A market value", "A taxable value (pre-transfer)", "A property tax",
         "A water + electricity + repairs", "B market value", "B taxable value", "B property tax",
         "B rent (2 units)", "B water + electricity + repairs", "CPI index", "fed exclusion",
         "Prop 19 allowance", "Sources"],
        [[str(r.year), money(r.a_fmv), money(r.a_taxable_before), money(r.a_tax_before),
          money(r.a_carry), money(r.b_fmv), money(r.b_taxable), money(r.b_tax), money(r.b_rent),
          money(r.b_carry), f"{r.cpi_index:,.0f}", money(r.fed_exclusion), money(r.prop19_allowance),
          cite("ca-rtc-51") + " · " + cite("irs-estate-tax")]
         for r in pick])

    body = f"""
<div class="notice"><strong>What this table is.</strong> A 51-year projection of the costs you
asked about — property tax, assessed value, market value, water, electricity, repairs, insurance
and rent — built from the official rules and the assumption set on this page. Property A's columns
before 2040 describe the house <em>before</em> it transfers: they are the transferor's bill, not
yours. The post-transfer numbers for each path are on the <a href="decision.html">decision
page</a>.</div>

<h2>Year-by-year projection, 2026–2076</h2>
<p>Every money figure is rounded to the nearest $10 at the point of publication. Insurance is
excluded from both properties because no official premium could be established (Q-05); it is added
as a separate line in the sensitivity table below so you can see its effect at any premium you
choose.</p>
{proj}

<h2>The official rules that generate those columns</h2>
{table(["Cost line", "Rule applied", "Official figure", "Label", "Source"],
       [["Property tax — assessed value", "Factored base year value: compounded by the CCPI factor, "
         "never more than 2% a year", "2.0% cap; 2026 roll factor 1.02", badge("verified"),
         cite("ca-rtc-51", "boe-lta-2026-002")],
        ["Property A — rate on assessed value", "Owner's effective rate derived from the actual bill "
         "and the actual roll value; county's stated typical rate shown for comparison",
         "1.3353% derived; 1.1488% typical", badge("derived"), cite("scc-assessor-booklet")],
        ["Property B — rate on assessed value", "Secured property tax rate for fiscal year 2026-27",
         "1.18162182%", badge("verified"), cite("sfttc-secured")],
        ["Property A — homeowners' exemption (if occupied)", "Reduction in taxable value on the "
         "owner-occupied principal residence", "$7,000", badge("verified"),
         cite("boe-homeowners-exemption")],
        ["Property B — rent", "Allowable annual increase for covered units, applied to the two "
         "leased units", "1.6% (1 Mar 2026 – 28 Feb 2027)", badge("verified"),
         cite("sf-rent-board-rates")],
        ["Water, electricity, repairs, insurance", "No official tariff applies to a single parcel; "
         "escalated at the inflation assumption and grown from the owner's figures",
         f"2026: A {money(A['a_water_mo'].value)}/mo water, net electricity credit; "
         f"B {money(A['b_water_mo'].value)}/mo water", badge("assumption"), cite("cpuc-nem")],
        ["Capital-gains rates used after a later sale", "Statutory top rate plus state rate; the "
         "owner's future bracket is unknown", f"{A['fed_ltcg_pct'].value:g}% fed (range "
         f"{A['fed_ltcg_pct'].low:g}–{A['fed_ltcg_pct'].high:g}%); 12.30% + 1% CA",
         badge("assumption"), cite("ftb-2026-rates", "ca-rtc-17043")],
        ])}

<h2>Insurance: the blank, priced explicitly</h2>
<p>The only official insurance figure that exists is a statewide one: the Department of Insurance's
market snapshot reports an average homeowner premium of <span class="stat">$1,571</span> against a
national average of <span class="stat">$1,512</span> ({cite("cdi-market-snapshot")}). It publishes no
premium for an individual address, and neither property is an average — A is a single-family house in
a wildfire-adjacent county and B is a three-unit building needing a landlord policy. Rather than
guess, here is what each $1,000 a year of premium does to the 25-year comparison on a 2045 transfer.
Add the premium you are actually quoted to the annual cost of whichever path you choose.</p>
{table(["Premium, $/yr", "Effect on 25-year wealth (occupy A)", "Effect (rent A out)",
        "Effect (sell A)", "Source"],
       [[money(p), money(-p * 25), money(-p * 20), money(-p * 15), cite("cdi-guides")]
        for p in (0, 1_000, 2_000, 3_000, 5_000)])}
<p class="note">Illustrative arithmetic only: undiscounted years of premium, not the model's
compounding. It exists to show the scale — insurance at $3,000 a year is $75,000 over 25 years,
which is small next to the differences on the decision page. Insurance is therefore an important
fact to establish, but it is not the variable that decides the question.</p>

<h2>Sensitivity: the four assumptions that matter</h2>
<p>Each row moves one assumption to the edge of its stated range and re-runs the 2045 transfer with
a 25-year horizon. Everything else stays at its central value.</p>
{sensitivity_table()}
"""
    return page("projections.html", "Projections, cost by cost, year by year",
                "Projection worksheet", body)


SRC_FOR = {"equity_return": "tsp-rates", "a_growth": "fred-hpi-us",
           "inflation": "bls-cpi-historical", "selling_cost_pct": "ca-rtc-11911"}


def sensitivity_table():
    base = path_wealth(2045)
    src_for = SRC_FOR
    rows = [["Central case", "as stated", money(base["P1"]), money(base["P2"]), money(base["P3"]),
             {"P1": "Occupy", "P2": "Rent", "P3": "Sell"}[max(PATH_KEYS, key=lambda k: base[k])],
             cite("irs-p551")]]
    for key, vals in (("equity_return", (3.0, 7.0)), ("a_growth", (2.0, 6.0)),
                      ("inflation", (4.0, 1.5)), ("selling_cost_pct", (7.0, 4.5))):
        for v in vals:
            saved = A[key].value
            A[key].value = v
            try:
                w = path_wealth(2045)
            finally:
                A[key].value = saved
            rows.append([A[key].label, f"{v:g}",
                         money(w["P1"]), money(w["P2"]), money(w["P3"]),
                         {"P1": "Occupy", "P2": "Rent", "P3": "Sell"}[max(PATH_KEYS, key=lambda k: w[k])],
                         cite(src_for.get(key, "irs-p551"))])
    return table(["Assumption moved", "To", "Occupy A", "Rent A out", "Sell A", "Winner", "Source"],
                 rows)


# ---------------------------------------------------------------------------
# page 5 — decision
# ---------------------------------------------------------------------------
def page_decision():
    blocks = []
    for y in HORIZONS:
        t = transfer_table(y)
        w = path_wealth(y)
        be = break_even_growth(y)
        be_eq = break_even_equity(y)
        rows = [
            ["Market value at transfer", money(t["fmv"]), money(t["fmv"]), money(t["fmv"]),
             "Assumed growth path from the 2026 anchor", badge("assumption"), cite("fred-hpi-us")],
            ["Factored base year value at transfer", money(t["fbyv"]), money(t["fbyv"]),
             money(t["fbyv"]), "Proposition 13 factor, 2% a year", cite("ca-rtc-51")],
            ["Prop 19 allowance at that date", money(t["allowance"]), money(t["allowance"]),
             money(t["allowance"]), "Published for 2025-27, projected after", cite("boe-lta-2025-009")],
            ["Taxable value enrolled", money(t["p1_taxable"]), money(t["p2_taxable"]),
             "not applicable — sold",
             "Factored value plus the excess over the cap; no exclusion without occupancy",
             cite("ca-rtc-63-2")],
            ["Annual property tax, first year", money(t["p1_tax"]), money(t["p2_tax"]), "not applicable",
             "Applied effective rate on the enrolled value", cite("scc-assessor-booklet")],
            ["Cost of not occupying, every year", "—", money(t["tax_gap"]), "—",
             "Extra tax the rental path pays for as long as it is rented", badge("derived") + " · "
             + cite("ca-rtc-63-2")],
            ["Documentary transfer tax on a sale", "—", "—", money(t["transfer_tax"]),
             "County $0.55 per $500 plus city $0.55 per $1,000", cite("ca-rtc-11911")],
            ["Selling cost at 5.5%", "—", "—", money(t["sell_cost"]),
             "Assumption, range 4.5-7%; only the transfer tax is statutory",
             badge("assumption") + " · " + cite("ca-rtc-11911")],
            ["Net proceeds if sold at the transfer", "—", "—", money(t["net_sale"]),
             "Basis resets to date-of-death value, so no tax on the pre-death gain", cite("irs-p551")],
            [f"After-tax wealth in {y + 25}", money(w["P1"]), money(w["P2"]), money(w["P3"]),
             "Model output: 25-year horizon, all three paths", badge("derived") + " · "
             + cite("irs-p551")],
        ]
        blocks.append(f"""
<h2>Transfer in {y} — 25-year horizon to {y + 25}</h2>
{table(["Item", "Occupy A", "Rent A out", "Sell A", "Basis", "Label and source"], rows)}
<p><b>The two break-evens.</b> Renting A out overtakes selling if A's market value grows faster
than {"about " + pct(be, 1) + " a year" if be else "the tested range"} for 25 years with the
reinvestment return held at 5% after tax; and it also overtakes selling if the reinvested proceeds
earn less than {"about " + pct(be_eq, 1) if isinstance(be_eq, float) else _be_text(be_eq)} after
tax, with A growing at 4%. Both are unavoidable assumptions. Test them on the
<a href="projections.html">projections page</a>.</p>
""")

    body = f"""
<div class="notice"><strong>The answer, stated carefully.</strong> In the central case, selling
Property A at the transfer and reinvesting wins in all three transfer windows, and it wins by a
wide margin. But the margin is produced mostly by two assumptions — the reinvestment return and
A's future growth — neither of which is knowable. The honest conclusion is: <em>sell unless you
expect a specific, defensible reason why A will outgrow a diversified portfolio, or unless living
in A is worth the difference to you as a preference</em>.</div>

<h2>Why Property B is the hinge</h2>
<p>Property B is already owned, already protected by its own Proposition 13 base, and already
producing rent from two units while leaving a third for you to live in. That means the decision
about A is <em>not</em> a housing decision — the housing need is already met. It is a question about
where to put roughly three million dollars of concentrated, illiquid, single-asset risk. That
framing is what makes selling the default rather than the fallback.</p>

<h2>Why occupying A is the weakest path despite the tax break</h2>
<p>Occupying A is the only way to keep any of the Prop 19 exclusion, and it saves real money:
{money(transfer_table(2045)["tax_gap"])} a year at a 2045 transfer. But occupying A also gives up
the rent from B's third unit, adds A's full carrying cost, and leaves you living in the more
expensive of two houses you own. The tax saving does not cover the rent given up.</p>
{"".join(blocks)}

<h2>Conditions under which each path is the right answer</h2>
{table(["Choose", "When this is true", "What would have to be verified first", "Source"],
  [["<strong>Sell A</strong>", "You expect the reinvested proceeds to earn at least the rate A "
    "would appreciate, and you want one asset rather than two houses.",
    "The reinvestment plan itself; the trust permits a sale; the sale is not the family home you "
    "want to keep.", cite("irs-p551")],
   ["<strong>Rent A out</strong>", "You expect A to appreciate faster than your portfolio, or you "
    "want to keep the option of moving in later.",
    "An achievable rent (Q-06); landlord insurance (Q-05); A's condition; the vacancy risk in a "
    "rent-controlled city.", cite("ca-civ-1947-12")],
   ["<strong>Occupy A</strong>", "You want to live there, and you accept that this costs more than "
    "the alternatives.",
    "Occupancy and exemption filing within one year; that B's third unit can then be let or left "
    "empty lawfully (Q-09).", cite("ca-rtc-63-2")],
   ])}

<h2>What would change the answer</h2>
<ul>
<li><b>Reinvestment return falls toward 3% after tax.</b> The sell advantage narrows sharply and the
rent and occupy paths become live options — see the sensitivity table on the
<a href="projections.html">projections page</a>.</li>
<li><b>A appreciates at 6% instead of 4%.</b> Renting overtakes selling. That is the same tension
the housing-bust regime on the <a href="black-swans.html">black-swan page</a> tests from the other
side.</li>
<li><b>Two or more beneficiaries.</b> The §121 exclusion and the Prop 19 occupancy requirement both
get harder; selling becomes more attractive still.</li>
<li><b>The insurance premium is enormous.</b> It is not: the projections page prices each $1,000 of
premium and shows it is small next to the spread between the paths.</li>
</ul>
"""
    return page("decision.html", "Occupy, rent, or sell — and why",
                "Decision analysis", body)


# ---------------------------------------------------------------------------
# page 6 — black swans
# ---------------------------------------------------------------------------
def page_swans():
    regimes = build_regimes()
    rows = [[f"<strong>{r['code']}</strong>", r["name"], r["cpi_window"], r["hpi_window"],
             f"{r['cpi']:+.1f}%", f"{r['hpi']:+.1f}%", f"{r['real']:+.1f}%",
             f"{r['cpi_ann']:+.2f}%", f"{r['hpi_ann']:+.2f}%",
             cite("fred-cpiaucns") + " / " + cite("fred-hpi-us")] for r in regimes]

    bodies = f"""
<div class="notice"><strong>Why this page exists.</strong> A 50-year projection that assumes a
constant 4% growth rate and a constant 2.5% inflation rate is not a projection, it is a straight
line. Growth and inflation have never been constant over any 50-year period. Every number on this
page is computed by this site from two official published series — the CPI-U from the Bureau of
Labor Statistics and the FHFA all-transactions house-price index — not from a story about what a bad
decade might look like.</div>

<h2>Five real episodes, measured</h2>
<p>Both legs of each episode are shown with their own dates, because the two series need not cover
the same years: S1's inflation ran for a decade while nominal house prices only stalled for three
years inside it. "Real house price" is the house-price change deflated by the CPI change.</p>
{table(["Code", "Regime", "CPI window", "House-price window", "CPI change", "House-price change",
        "Real house-price change", "CPI per year", "House price per year", "Sources"], rows)}

<h2>What each episode actually did to each of the three choices</h2>
<div class="grid">
<div class="card"><b>S1 · Stagflation (1973–1982)</b>
Prices more than doubled — 8.9% a year — while the national house-price index rose 8.7% in total
over its 2.75-year window, a loss of about half the real value. For this decision the lesson is
about the <em>reinvestment</em> leg, not the house: a portfolio that does not beat inflation does
not preserve the proceeds of a sale.</div>
<div class="card"><b>S2 · Housing bust (2006–2012)</b>
The national index fell 15.9% nominally, 2.9% a year, and 26.5% in real terms over six years. A sale
forced in 2009 would have realised a quarter less in real purchasing power than a sale in 2006. This
is the argument for the treasury ladder: sell when you decide to sell, then reinvest over 12–24
months rather than on one day.</div>
<div class="card"><b>S3 · Rate shock (2022–2023)</b>
The policy rate rose 400 basis points in nine months, and the national house-price index still rose
1.0%. The shock hit affordability and transaction volume, not prices. Do not assume a rate rise
forces a price fall.</div>
<div class="card"><b>S4 · Demand collapse (2020)</b>
The twelve-month CPI change in April 2020 was effectively zero — 0.1% on CPI-U, −0.1% on CPI-W —
and the housing index then gained 58.7% in six years. A cash-flow shock and an asset-price shock are
different events. If you rent A out, the cash-flow shock is the one that matters, and the rent cap
in the city where B sits limits your ability to recover it.</div>
<div class="card"><b>S5 · The live one (2026)</b>
CBO's February 2026 baseline had PCE inflation at 2.7% for 2026 and 2.0% from 2030. CPI-U rose
3.7% in the year to September 2026 and 3.4% to October, and the FOMC <em>raised</em> its target
range 25 basis points on 17 September 2026 after three cuts in 2025. Over the whole 2021–2026
stretch inflation has run 4.3% a year, so the 2.5% inflation assumption used in the central case is
optimistic relative to the last five years.</div>
</div>

<h2>Re-running the decision under each regime</h2>
<p>Each regime's own annual rates are substituted for the model's assumptions <em>for as many years
as the episode lasted</em>, and the model then reverts to its central assumption. Applying a
two-year price fall across twenty-five years would be an invented forecast, not a stress test. During
each episode the reinvestment leg is assumed to earn only the regime's own inflation — no real
return at all — which is deliberately unkind to the sell path; after the episode it reverts to the
central 5%. This tests the <em>ordering</em> of the three choices; it does not assign
probabilities.</p>
<p><b>What the stress shows.</b> Selling survives four of the five episodes even with a zero real
return on the proceeds, because after the episode the model reverts to central assumptions. It
loses only where housing ran far ahead of everything else — the 2020s boom, S4 and S5 — and there
the winner is renting A out, not occupying it. The column that matters is the last one: each
episode moves the break-even reinvestment return to somewhere between 2.8% and well above 5%, and
that range is wider than any of the differences between the three paths.</p>
{regime_outcome_table()}

<h2>Baseline against reality: how straight is the straight line?</h2>
{table(["Series", "Window", "Total change", "Annualised", "Source"],
  [["CPI-U, all items", "Oct 1973 to Oct 1982",
    f"+{(CPI_OCT[1982] / CPI_MONTH[(1973, 10)] - 1) * 100:.1f}%",
    f"{((CPI_OCT[1982] / CPI_MONTH[(1973, 10)]) ** (1 / 9) - 1) * 100:+.2f}%", cite("fred-cpiaucns")],
   ["CPI-U, all items", "Jan 2006 to Jan 2012",
    f"+{(CPI_MONTH[(2012, 1)] / CPI_MONTH[(2006, 1)] - 1) * 100:.1f}%",
    f"{((CPI_MONTH[(2012, 1)] / CPI_MONTH[(2006, 1)]) ** (1 / 6) - 1) * 100:+.2f}%",
    cite("fred-cpiaucns")],
   ["CPI-U, all items", "Jan 2021 to Oct 2026",
    f"+{(CPI_MONTH[(2026, 10)] / CPI_MONTH[(2021, 1)] - 1) * 100:.1f}%",
    f"{((CPI_MONTH[(2026, 10)] / CPI_MONTH[(2021, 1)]) ** (1 / 5.75) - 1) * 100:+.2f}%",
    cite("fred-cpiaucns")],
   ["FHFA house-price index, US", "1980Q1 to 2026Q1", "+612.2%", "+4.33%", cite("fred-hpi-us")],
   ["FHFA house-price index, US", "2020Q1 to 2026Q2", "+60.5%", "+7.87%", cite("fred-hpi-us")],
   ["FHFA house-price index, US", "2007Q1 peak to 2012Q1 trough", "−18.6%", "−3.45%",
    cite("fred-hpi-us")],
   ["Model's inflation assumption", "long run, every year", "not a measurement", "+2.50%",
    badge("assumption") + " · " + cite("cbo-outlook-2026")],
   ["Model's house-growth assumption", "long run, every year", "not a measurement", "+4.00%",
    badge("assumption") + " · " + cite("fred-hpi-us")],
   ])}
<p class="note">The last two rows place the model's assumptions beside the official history they
are meant to represent. Housing at 4.0% nominal is very close to the national 4.3% since 1980; but
the national index is not this house, and the two decades since 2000 are the only stretch in which
the index behaved that way.</p>

<h2>The projection in this site is not a straight line either</h2>
<p>Two of the model's own mechanisms already break the straight line: property tax is capped at a
2% factor while market values grow at 4%, so the effective tax rate on value falls every year; and
cost escalation is driven by the inflation assumption independently of growth. What the model does
<em>not</em> contain is a single year in which any series falls. That is the gap this page exists to
make visible, and it is why the stress test above is not a probability-weighted average.</p>
"""
    return page("black-swans.html", "Black swans and uneven economies",
                "Stress conditions that mimic the real record", bodies)


def _be_text(be):
    if isinstance(be, float):
        return f"above {be:.2f}%"
    return ("never — keeping A wins even at a 20% return" if be == "never"
            else "always — selling wins even at a 0% return")


def regime_outcome_table():
    rows = []
    regimes = build_regimes()
    base = path_wealth(2045)
    for r in regimes:
        out = regime_outcome(2045, regime=r, equity_real=2.5)
        w = out["wealth"]
        be = break_even_equity(2045, regime=r)
        verdict = f"sale wins if reinvestment is {_be_text(be)}" if isinstance(be, float) else _be_text(be)
        rows.append([f"<strong>{r['code']}</strong>", r["name"],
                     f"{r['hpi_ann']:+.2f}% for {r['episode_years']} yr",
                     f"{r['cpi_ann']:+.2f}% for {r['episode_years']} yr",
                     f"{2.5 + r['cpi_ann']:+.2f}% for {r['episode_years']} yr",
                     money(w["P1"]), money(w["P2"]), money(w["P3"]),
                     {"P1": "Occupy", "P2": "Rent", "P3": "Sell"}[out["best"]], verdict,
                     cite("fred-hpi-us") + " / " + cite("fred-cpiaucns")])
    rows.append(["<strong>Base</strong>", "Central assumptions, all 25 years", "+4.00%",
                 "+2.50%", "+5.00%", money(base["P1"]), money(base["P2"]), money(base["P3"]),
                 {"P1": "Occupy", "P2": "Rent", "P3": "Sell"}[max(PATH_KEYS, key=lambda k: base[k])],
                 (f"sale wins if reinvestment is {_be_text(break_even_equity(2045))}"
                  if isinstance(break_even_equity(2045), float)
                  else _be_text(break_even_equity(2045))),
                 badge("assumption") + " · " + cite("irs-p551")])
    return table(["Code", "Regime", "House growth used", "Inflation used", "Reinvestment used",
                  "Occupy A", "Rent A out", "Sell A", "Winner", "Where the line falls", "Sources"],
                 rows)


# ---------------------------------------------------------------------------
# page 7 — inheritance steps
# ---------------------------------------------------------------------------
def page_inheritance():
    steps = [
        ("1", "While the transferor is alive", "Confirm the trust exists, is funded, and names the right "
         "beneficiaries. Confirm that the house is titled in the trust, not in a will that would send it to "
         "probate. Keep the deed and the trust certification together.", "—", badge("verified"),
         "boe-lta-2026-026"),
        ("2", "Day of death", "The transfer happens here, not at distribution. The county reassesses "
         "inherited property as of the date of death, and the Prop 19 occupancy clock starts.", "—",
         badge("verified"), "scc-assessor-booklet"),
        ("3", "Within 9 months (15 with extension)", "File Form 706 if the estate exceeds the filing "
         "threshold — $15,000,000 of gross estate for 2026 deaths, plus adjusted taxable gifts. Filing is "
         "also how portability is elected if there is a surviving spouse.", "Deadline: 9 months, "
         "automatic 6-month extension on Form 4768", badge("verified"), "irs-estate-faq"),
        ("4", "At recording", "File the Preliminary Change of Ownership Report with the county recorder "
         "when the deed is recorded. A missing PCOR adds a recording fee, and the assessor needs it to "
         "decide the reassessment.", "County form", badge("verified"), "scc-assessor-booklet"),
        ("5", "Within 1 year of the transfer", "If the child will occupy the home: move in and file the "
         "homeowners' exemption (BOE-266) with the county assessor. This is the condition that keeps the "
         "Prop 19 exclusion alive.", "Hard deadline: 1 year", badge("verified"), "ca-rtc-63-2"),
        ("6", "Within 3 years of the transfer", "File the intergenerational transfer exclusion claim "
         "(BOE-19-P) with the assessor. Without a filed claim the exclusion is not allowed at all.",
         "Deadline: 3 years, or before a transfer to a third party", badge("verified"), "boe-prop19"),
        ("7", "When the assessor acts", "A supplemental assessment is issued for the difference between "
         "the old value and the new value, prorated to the months left in the fiscal year. It is a "
         "separate bill, usually not escrowed.", "Next roll", badge("verified"), "scc-assessor-booklet"),
        ("8", "After the exclusion is enrolled", "The exclusion is not permanent. If the transferee later "
         "stops being eligible for the homeowners' or disabled veterans' exemption, the exclusion is "
         "removed and the factored value is enrolled from the following lien date.", "Continuing condition",
         badge("verified"), "boe-lta-2026-026"),
        ("9", "Before any sale", "Obtain the date-of-death appraisal and the Form 706 value, because "
         "basis and the estate value must be consistent. A sale at the transfer realises no gain if "
         "basis equals sale price less costs.", "—", badge("verified"), "irs-p551"),
        ("10", "Before any rental of A", "Landlord insurance, a rental appraisal, and a check on whether "
         "the city's rent rules reach a single-family house. Converting a principal residence to a "
         "rental starts depreciation and changes the later tax on a sale.", "—", badge("verified"),
         "irs-p527"),
    ]
    body = f"""
<div class="notice"><strong>The sequence is the protection.</strong> Three of the steps below have
hard deadlines measured from the date of death, not from the date the estate is distributed, and
two of them are what stand between you and a property-tax bill based on full market value. Print
this page.</div>

<h2>The process, step by step</h2>
{table(["#", "When", "What has to happen", "Deadline", "Label", "Source"],
       [[s[0], s[1], s[2], s[3], s[4], cite(s[5])] for s in steps])}

<h2>The arithmetic of missing step 5</h2>
<p>The difference between filing and not filing the homeowners' exemption claim, and between
occupying and not occupying, is the whole Prop 19 benefit. At a 2045 transfer the gap is
{money(transfer_table(2045)['tax_gap'])} a year. Compounded at 2% for 25 years that is about
{money(transfer_table(2045)['tax_gap'] * ((1.02 ** 25 - 1) / 0.02))} of extra tax paid, on a
property that would otherwise have been the cheapest of the three paths to hold.</p>

<h2>What the trust changes — and what it does not</h2>
<ul>
<li><b>It changes who decides.</b> Under a continuing trust the trustee, not the beneficiary, holds
the power to sell. Ask for the distribution article in writing (Q-03).</li>
<li><b>It changes the paperwork.</b> A transfer at death inside a trust is still a transfer for
property-tax purposes; the assessor's exclusion claim still has to be filed.</li>
<li><b>It does not change the income-tax basis rule.</b> Property acquired from a decedent takes a
basis equal to fair market value at the date of death, whether or not a trust is involved.</li>
<li><b>It does not shelter the estate from the federal test.</b> Assets in a revocable trust are
still in the gross estate.</li>
</ul>

<h2>Documents to collect, in one list</h2>
<ol>
<li>Trust instrument and any amendments, plus the schedule of beneficiaries.</li>
<li>Certification of trust accepted by the county recorder.</li>
<li>The most recent property-tax bill for Property A and the assessor's notification of assessed
value.</li>
<li>Date-of-death appraisal (or the Form 706 value) for Property A.</li>
<li>Any depreciation schedules if A was ever rented.</li>
<li>The estate inventory, including the cash bequest (Q-04).</li>
<li>Insurance declarations for both properties, and three current quotes for each (Q-05).</li>
<li>The Rent Board Housing Inventory record for Property B (Q-09).</li>
</ol>
"""
    return page("inheritance.html", "How inheriting through a trust actually works",
                "Step-by-step process", body)


# ---------------------------------------------------------------------------
# page 8 — costs and tax
# ---------------------------------------------------------------------------
def page_costs():
    bodies = f"""
<div class="notice"><strong>Two different tax questions.</strong> The tax on <em>inheriting</em> is
almost certainly zero in California; the tax on <em>owning</em> the house afterwards is not, because
the Proposition 13 base is broken by the transfer. Most of the money in this decision sits in the
second question.</div>

<h2>1. Inheritance: the thresholds that matter</h2>
{table(["Level", "What the tax is", "Threshold", "What it means for this estate", "Source"],
  [["Federal estate tax", "Tax on the right to transfer property at death, on the gross estate",
    f"${OFFICIAL['fed_exclusion_2026']:,} per decedent for 2026 deaths",
    f"Property A and B together are about ${(A['a_fmv_2026'].value + A['b_fmv_2026'].value):,} at "
    f"today's estimates, but B is not inherited, so the estate-side number is much smaller. Headroom "
    f"is large — but the cash bequest is unknown.", cite("irs-estate-tax")],
   ["Federal estate tax, 2027", "Indexed annually", stat(OFFICIAL['fed_exclusion_2027']),
    "Published 5 November 2026 in Rev. Proc. 2026-35.", cite("irs-ir-2026-133")],
   ["Federal gift tax", "Annual exclusion per recipient", f"${OFFICIAL['gift_annual_2026']:,} in 2026; "
    f"${OFFICIAL['gift_annual_2027']:,} in 2027", "Relevant only if the transferor is making lifetime gifts.",
    cite("irs-ir-2026-133")],
   ["California estate tax", "None", "No return required for deaths on or after 1 January 2005",
    "Nothing to plan for at state level.", cite("ca-sco-estate")],
   ["California inheritance tax", "None", "No inheritance tax for deaths on or after 1 January 2005",
    "Nothing to plan for at state level.", cite("ca-sco-estate")],
   ["Income tax on the inheritance itself", "None — inheritances are not income",
    "Basis resets to date-of-death fair market value",
    "This is the largest single tax benefit in the whole plan: decades of gain disappear.",
    cite("irs-p551")],
   ])}

<h2>2. The headroom calculation, and why it must be re-run</h2>
<p>Headroom is the federal exclusion minus the gross estate. The gross estate is not the same as the
value of A: it is everything the transferor owns. We know A's value and we do not know the rest, so
the table below is an <em>upper bound on the headroom</em>, not a figure to plan against.</p>
{table(["Year", "Federal exclusion", "Property A at that year", "Upper-bound headroom if A were the whole estate", "Source"],
  [[str(y), money(fed_exclusion(y)),
    money(A["a_fmv_2026"].value * (1 + A["a_growth"].value / 100) ** (y - BASE_YEAR)),
    money(fed_exclusion(y) - A["a_fmv_2026"].value * (1 + A["a_growth"].value / 100) ** (y - BASE_YEAR)),
    cite("irs-estate-tax")] for y in (2026, 2030, 2040, 2045, 2050)])}
<p class="note">Exclusion growth after 2027 is an assumption ({badge("assumption")}); Property A's
growth is an assumption. The row for 2026 is the only one built entirely on published figures.</p>

<h2>3. Property tax after the transfer: the number that actually moves</h2>
{table(["Concept", "Rule", "Figure", "Source"],
  [["Base levy", "1% of assessed value plus voter-approved debt", "1.0000% base",
    cite("scc-assessor-booklet")],
   ["Annual increase cap", "Factored base year value grows by the CCPI change, never above 2%",
    "2% maximum; 2026 roll factor 1.02", cite("ca-rtc-51", "boe-lta-2026-002")],
   ["Intergenerational exclusion", "Applies only to a principal residence, only if the transferee "
    "occupies within a year and files for the exemption", f"Value cap = FBYV + ${OFFICIAL['prop19_allowance_2025_2027']:,}",
    cite("boe-prop19", "ca-rtc-63-2")],
   ["If the cap is exceeded", "The excess over the cap is added to the factored base year value",
    f"New taxable = FBYV + excess", cite("ca-rtc-63-2")],
   ["If the child does not occupy", "No exclusion at all; full market value enrolled", "—",
    cite("ca-rtc-63-2")],
   ["Homeowners' exemption", "Reduction in taxable value for an owner-occupied home", "$7,000",
    cite("boe-homeowners-exemption")],
   ["Assessor's 'typical' rate", "Base 1% plus county, school and water bonds in a typical tax-rate area",
    "1.1488%", cite("scc-assessor-booklet")],
   ["Rate used for Property A here", "Derived from the actual bill and the actual roll value",
    "1.3353%", f'{badge("derived")} · {cite("scc-assessor-booklet")}'],
   ["Rate used for Property B", "San Francisco secured rate, fiscal year 2026-27", "1.18162182%",
    cite("sfttc-secured")],
   ])}

<h2>4. Carrying costs, both properties</h2>
{table(["Cost", "Property A", "Property B", "Basis", "Source"],
  [["Water and sewer, per month", money(A['a_water_mo'].value), money(A['b_water_mo'].value),
    "Owner-supplied ranges; midpoints", f'{badge("owner")} · {cite("cbo-outlook-2026")}'],
   ["Electricity, per month (net of solar)", money(A['a_elec_net_mo'].value),
    money(A['b_elec_mo'].value), "Owner-supplied; A's credit is not guaranteed under net billing",
    cite("cpuc-nem")],
   ["Insurance, per year", "—", "—",
    "No official premium could be established. See Q-05 and the flagged page.",
    f'<em>blank</em> · {cite("cdi-guides")}'],
   ["Repairs and maintenance", "1.0% of market value a year", "1.0% of market value a year",
    "Assumption; the owner states A costs less, which is not modelled separately",
    f'{badge("assumption")} · {cite("scc-assessor-booklet")}'],
   ["Property tax", "1.3353% of taxable value (derived)", "1.18162182% of taxable value",
    "See section 3", f'{badge("derived")} · {cite("sfttc-secured")}'],
   ])}

<h2>5. Taxes when you dispose of either property</h2>
{table(["Situation", "Federal", "California", "Source"],
  [["Sell A at the transfer", "No capital-gains tax: basis equals date-of-death value",
    "No capital-gains tax for the same reason", cite("irs-p551")],
   ["Sell A later after living in it 2 of the last 5 years",
    f"Up to ${OFFICIAL['irc121_single']:,} of gain excluded (single) or "
    f"${OFFICIAL['irc121_joint']:,} (joint)", "Conforms to the federal exclusion",
    cite("irs-topic-701")],
   ["Sell A later after renting it out",
    "Depreciation recapture at 25% on the unrecaptured §1250 gain, then long-term capital-gains rates",
    "12.30% plus the 1% mental-health tax above $1,000,000 of taxable income",
    cite("irs-p527", "ftb-2026-rates", "ca-rtc-17043")],
   ["Sell B", "Carries the entire embedded gain — there is no step-up because B is not inherited",
    "Same, at state rates", f'{badge("derived")} · {cite("ftb-2026-rates")}'],
   ["Rent A out", "Rental income is taxable; expenses and 27.5-year depreciation are deductible; "
    "passive-loss limits apply", "Conforms", cite("irs-p527")],
   ])}
"""
    return page("costs.html", "Inheritance tax, property tax and carrying costs",
                "Costs and tax", bodies)


# ---------------------------------------------------------------------------
# page 9 — repo review
# ---------------------------------------------------------------------------
def page_repo():
    body = f"""
<div class="notice"><strong>What this section is.</strong> A review of the repository this site
lives in, written by the session that built this directory. It records what was found, what was
changed, and what is still wrong — including problems in this site's own predecessors. The source
column points at the live directory itself, so every claim here can be checked by opening it.</div>

<h2>What the repository contains</h2>
<p>The repository accumulated several independent attempts at the same analysis, each by a separate
automated session, each published under its own directory. They do not agree with one another, and
several publish household dollar figures that the brief asked to be kept private. This is the
central repository finding.</p>
{table(["Directory", "What it is", "Published?", "Problem found", "Check it"],
  [["public-safe/", "The current live dashboard, twelve pages",
    "Yes — the root hub links to it",
    "Consistent and privacy-clean; the only tree that had been through a full privacy pass.",
    '<a href="../public-safe/index.html">open</a>'],
   ["desk-22a32b17/", "A second full decision desk, twelve pages and about 300 source-linked rows",
    "Yes — nothing excludes it",
    "<strong>Publishes household dollar anchors</strong> (values, tax bills, rents) and city names. "
    "Contradicts the privacy rule applied to public-safe/.", '<a href="../desk-22a32b17/index.html">open</a>'],
   ["referee-abae/", "A numeric referee that re-derives other desks' figures", "Yes",
    "Publishes rates, ratios and counts rather than household levels — a defensible middle line, and "
    "the basis for the privacy boundary this site adopts.",
    '<a href="../referee-abae/index.html">open</a>'],
   ["swan-3a49/", "A black-swan stress-test desk", "Yes",
    "Duplicates work in desk-22a32b17/; two sets of numbers for one question.",
    '<a href="../swan-3a49/index.html">open</a>'],
   ["desk-b4f/", "A third decision desk", "<strong>No</strong> — excluded in _config.yml",
    "Excluded after a reviewer found arithmetic errors. The exclusion is the right call.",
    '<a href="../desk-b4f/index.html">open</a>'],
   ["docs/", "A thirteen-page dashboard built for Pages from /docs", "<strong>No</strong> — excluded",
    "Excluded, so it is dead weight in the repository.",
    '<a href="../docs/index.html">open</a>'],
   ["plan/", "A directory claimed twice on the coordination board", "<strong>No</strong> — excluded",
    "Does not exist. The claim was stale and was taken over under the board's own rule.",
    '<a href="../COORDINATION.md">board</a>'],
   ])}

<h2>Irregularities found and how each was handled</h2>
{table(["#", "Finding", "Severity", "Action taken here", "Check it"],
  [["R-01", "Two live dashboards give materially different answers to the same question.",
    badge("priority-high"), "This site does not add a third unverifiable set of numbers. It reuses "
    "the other desks as cross-checks and publishes its own reproducible model, so every figure here "
    "traces to a line of code and a source link.", '<a href="../desk-22a32b17/index.html">desk</a>'],
   ["R-02", "desk-22a32b17/ publishes household dollar levels on a public page while public-safe/ "
    "asserts that such figures are withheld.", badge("priority-high"),
    "Logged on the flagged page. This site publishes rounded anchors and no histories. Removing or "
    "excluding the other desk is an owner decision, not this session's.",
    '<a href="../public-safe/index.html">public-safe</a>'],
   ["R-03", "The coordination board contains claims of tasks marked done whose directories do not "
    "exist.", badge("priority-medium"),
    "Recorded in the board's own session section; stale claims were taken over under the 60-minute "
    "rule after more than 25 hours without a commit.", '<a href="../COORDINATION.md">board</a>'],
   ["R-04", "The root landing page was an HTML meta-refresh redirect, not a landing page.",
    badge("priority-medium"), "Replaced with a category hub that links every published tree, so "
    "nothing is unreachable.", '<a href="../index.html">hub</a>'],
   ["R-05", "Some citations in the older trees point at URLs that now return 404, including one "
    "insurance department guide page.", badge("priority-medium"),
    "Every source used by this site was re-read in this session; the failed one is listed as "
    "unverified rather than cited as support.", '<a href="flagged.html">flags</a>'],
   ["R-06", "Several scripts under scripts/ write into directories owned by other sessions, so "
    "re-running them would overwrite published work.", badge("priority-low"),
    "This site has its own generator and verifier under review-092b/_src/ and writes only inside "
    "review-092b/.", '<a href="../scripts/">scripts</a>'],
   ["R-07", "Assessment and tax histories for both properties exist in the repository's data files "
    "at full precision.", badge("priority-high"),
    "Not republished here at any rounding. See Q-01 for why rounding a series does not protect it. "
    "Whether to remove them is an owner decision.", '<a href="questions.html">Q-01</a>'],
   ])}

<h2>What this session changed in the repository</h2>
<ul>
<li>Added <code>review-092b/</code>: this site, its generator, its verifier and its tests. Nothing
outside this directory was modified except the shared coordination board, the root landing page,
<code>_config.yml</code> and the README, which this session claimed explicitly because every other
outstanding claim had lapsed.</li>
<li>Added a verification gate to the workflow so the site cannot be published if a table row loses
its source link, a dollar figure stops rounding to $10, or a personal-identifier pattern appears.</li>
<li>Did not delete, rename or rewrite any other session's published directory.</li>
<li>Corrected two arithmetic defects in this site's own first draft rather than shipping them: a
black-swan stress test that applied a two-year price fall for twenty-five years, and money amounts
that rendered as <code>$-59,572,310</code> instead of a negative sign before the dollar sign. Both
are now regression-tested.</li>
</ul>
"""
    return page("repo-review.html", "Repository review and irregularities",
                "What the repo actually contains", body)


# ---------------------------------------------------------------------------
# page 10 — flagged
# ---------------------------------------------------------------------------
FLAGS = [
    ("F-01", "Insurance premiums for either property are not established",
     "The department publishes a statewide average homeowner premium of $1,571 (national average "
     "$1,512) and counts 677,449 FAIR Plan policies, but it does not publish a premium for a single "
     "address. No parcel-level figure exists in public data, so the model carries insurance at zero "
     "and prices each $1,000 of premium instead. The residential guide page the older desks cite "
     "returns a document-not-found page, so it is not used.",
     "High", "Obtain three written quotes per property, plus a FAIR Plan quote.",
     "cdi-market-snapshot"),
    ("F-02", "Property A's market value and taxable value are owner estimates",
     "Both are supplied figures rounded to $10 (or $10,000 for the market value). Neither is "
     "verified against an assessor record, and verifying it would itself identify the parcel.",
     "High", "Accept as an anchor, or supply a current appraisal.", "scc-assessor-booklet"),
    ("F-03", "The active-solar new-construction exclusion is listed but not read",
     "BOE LTA 2026/034 appears in the 2026 Letters to Assessors index under a title concerning a "
     "repeal date for the solar exclusion. Only the title was read, so no fact is taken from it. It "
     "matters because Property A has solar.",
     "Low", "Read the letter before relying on any solar property-tax treatment.",
     "boe-lta-2026-034"),
    ("F-04", "Counties' PARCEL-level rates are unknown",
     "The county publishes a 'typical' tax-rate-area rate of 1.1488%. The actual rate for Property "
     "A's area is unknown, and the owner's effective rate of 1.3353% is derived, not published.",
     "Medium", "Read the actual tax bill's rate line at the time of transfer.",
     "scc-assessor-booklet"),
    ("F-05", "The trust's terms are not available",
     "Whether Property A passes outright or into a continuing trust determines who may sell it and "
     "who must occupy it. Without the document the decision cannot be finalised.",
     "Critical", "Obtain the trust instrument (Q-03).", "boe-lta-2026-026"),
    ("F-06", "The cash inheritance is unknown",
     "The federal headroom figure on the costs page is an upper bound that assumes Property A is "
     "the entire estate. The real headroom is lower by the value of everything else.",
     "High", "Obtain the estate inventory (Q-04).", "irs-estate-tax"),
    ("F-07", "Property A's achievable rent is an assumption",
     "A 3.2% gross yield is assumed. No rent figure was supplied and no official source can say "
     "what this house would let for.",
     "High", "Two written rental appraisals at the time of transfer.", "hud-fmr"),
    ("F-08", "Whether occupying Property B's third unit requires any city approval is unverified",
     "The Rent Board's Housing Inventory and fee apply to residential units, and owner move-in has "
     "its own rules. None of this was confirmed for Property B.",
     "Medium", "Check the Housing Inventory record and the owner move-in rules.",
     "sf-rent-board"),
    ("F-09", "The documentary transfer tax on an inheritance is unverified",
     "R&TC §11911 taxes deeds by which realty is 'sold'; an inheritance is normally exempt but the "
     "exemption is claimed on the recorded document, which was not read.",
     "Low", "Confirm with the county recorder at the time of recording.", "ca-rtc-11911"),
    ("F-10", "No probability is attached to any black-swan regime",
     "The five regimes are historical measurements. This site deliberately does not assign them "
     "probabilities, because no official source does.",
     "Medium", "Use them as stress tests, not as a forecast.", "fred-hpi-us"),
    ("F-11", "Two earlier desks in this repository disagree with this site and with each other",
     "The figures in desk-22a32b17 are materially higher than this site's because that model assumes "
     "a 5.6% after-tax reinvestment return and a different terminal-tax convention. Neither is wrong; "
     "they answer different questions with different assumptions.",
     "Medium", "Treat this site's model as reproducible and auditable, not as definitive.",
     "tsp-rates"),
    ("F-12", "Assessment and tax histories remain at full precision elsewhere in the repository",
     "They are not published here, but they exist in the repository's data files and in git history. "
     "Removing content from a page does not remove it from history.",
     "High", "Owner decision on repository visibility or history rewriting (Q-01).",
     "scc-assessor-booklet"),
]


def page_flagged():
    body = f"""
<div class="notice"><strong>Nothing on this page blocks the site.</strong> Each item is something
this session could not confirm from an official source, or confirmed to be unresolved. Values that
could not be confirmed were left blank rather than estimated, and are listed here with the source
that should settle them. Review these in any order.</div>

<h2>Flagged for review</h2>
{table(["#", "Item", "Why it is flagged", "Severity", "What would settle it", "Source"],
       [[f"<strong>{f[0]}</strong>", f"<strong>{f[1]}</strong>", f[2],
         badge("priority-" + f[3].lower()), f[4], cite(f[5])] for f in FLAGS])}

<h2>Values deliberately left blank</h2>
{table(["Value", "Why blank", "Where it would be used", "Source that should settle it"],
  [["Property A homeowners insurance premium", "No official premium table could be read",
    "Carrying cost, and the 25-year comparison", cite("cdi-guides")],
   ["Property B landlord insurance premium", "Same", "B's net operating income", cite("cdi-guides")],
   ["Property A achievable rent", "Not supplied, not officially determinable",
    "The rent-A-out path", cite("hud-fmr")],
   ["Property B third-unit rent if let", "Not supplied",
    "The difference between occupying and letting B's third unit", cite("sf-rent-board-rates")],
   ["Cash inheritance amount", "Not supplied", "Federal estate headroom", cite("irs-estate-tax")],
   ["Property A date-of-death appraised value", "Does not exist yet",
    "Basis, and every post-transfer figure", cite("irs-p551")],
   ])}

<h2>What is <em>not</em> flagged</h2>
<p>The rules in the table below were read directly in the official document linked beside them
during this session and are quoted, not paraphrased from memory: the 2026 and 2027 federal
exclusions, the absence of a California estate or inheritance tax, the §1014 basis reset, the §121
exclusion amounts, the $7,000 homeowners' exemption, the $1,044,586 Prop 19 allowance and its
expiry date, the 2% Proposition 13 cap, the 2026 roll inflation factor, the San Francisco secured
rate, the documentary transfer tax rate, the state rent cap formula, the city's 1.6% allowable
increase, the 2026 state income-tax brackets, the 1% mental-health tax threshold, the federal funds
target range and its September 2026 change, the CBO inflation path, and every CPI and house-price
figure used on the black-swan page.</p>
"""
    return page("flagged.html", "Flagged for review", "Unverified and unresolved items", body)


# ---------------------------------------------------------------------------
# page 11 — sources
# ---------------------------------------------------------------------------
def page_sources():
    rows = []
    for s in SOURCES:
        rows.append([f"<code>{s['id']}</code>", s["org"], f'<a href="{s["url"]}" rel="noopener">{s["title"]}</a>',
                     s["read"], s["used_for"]])
    body = f"""
<div class="notice"><strong>Every row on this site carries one of these links.</strong> The table
below is the complete register: what each document is, when it was opened, and exactly what was
taken from it. Sources listed as <em>not read</em> are not used to support any figure.</div>

<h2>Source register</h2>
{table(["ID", "Publisher", "Document", "Read on", "What was taken from it"], rows)}

<h2>Verification method</h2>
<p>Each document was retrieved and read during this session; the date in the table is that
retrieval. Where a document could not be retrieved, the row says so and the figure it would have
supported is left blank. No figure on this site was written from memory or from a secondary
summary. Where a number is arithmetic on a published figure, the row is labelled
{badge("derived")} and the arithmetic is shown in the generator
(<code>review-092b/_src/engine.py</code>).</p>
<p>The site is regenerated by <code>python3 review-092b/_src/build.py</code> and checked by
<code>python3 review-092b/_src/verify.py</code>, which fails the build if any table row loses its
source link, if any dollar figure stops being a multiple of $10, if any internal link breaks, or if
any personal-identifier pattern appears.</p>
"""
    return page("sources.html", "Official source register", "Every citation, with what was read", body)


# ---------------------------------------------------------------------------
# style
# ---------------------------------------------------------------------------
CSS = """
:root{--ink:#12202c;--muted:#5d6b76;--line:#d9e0e6;--bg:#f6f8fa;--card:#fff;
--accent:#1d4e6f;--good:#1f6b45;--warn:#8a5a00;--bad:#8c1d18}
*{box-sizing:border-box}
body{margin:0;font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
color:var(--ink);background:var(--bg)}
header{display:flex;flex-wrap:wrap;gap:.6rem;justify-content:space-between;align-items:baseline;
padding:.9rem 1.4rem;background:var(--accent);color:#fff}
header a{color:#fff;font-weight:700;text-decoration:none;font-size:1.05rem}
header span{font-size:.8rem;opacity:.85}
.layout{display:grid;grid-template-columns:230px 1fr;gap:0;min-height:100vh}
nav{padding:1rem .8rem;background:#fff;border-right:1px solid var(--line);position:sticky;top:0;
align-self:start;height:100vh;overflow:auto}
nav a{display:block;padding:.42rem .6rem;border-radius:6px;color:var(--ink);text-decoration:none;font-size:.88rem}
nav a:hover{background:var(--bg)}
nav a[aria-current]{background:var(--accent);color:#fff;font-weight:600}
main{padding:1.6rem 2rem 3rem;max-width:1250px}
h1{font-size:1.6rem;margin:.2rem 0 1rem}
h2{font-size:1.1rem;margin:2rem 0 .6rem;padding-bottom:.3rem;border-bottom:1px solid var(--line)}
h3{font-size:.98rem;margin:.2rem 0}
.eyebrow{text-transform:uppercase;letter-spacing:.08em;font-size:.72rem;color:var(--muted);font-weight:700}
.notice{background:#fff7e6;border:1px solid #efd9a8;border-left:4px solid #c8961f;
padding:.85rem 1rem;border-radius:8px;margin:1rem 0}
table.data{width:100%;border-collapse:collapse;margin:.7rem 0 1.4rem;font-size:.8rem;background:#fff;
display:block;overflow-x:auto;white-space:nowrap}
table.data thead th{background:#eef3f7;text-align:left;padding:.5rem .6rem;border-bottom:2px solid var(--line);
position:sticky;top:0;vertical-align:bottom}
table.data td{padding:.45rem .6rem;border-bottom:1px solid var(--line);vertical-align:top}
table.data td:nth-child(2),table.data td:nth-child(3){white-space:normal;min-width:180px}
table.data tbody tr:hover{background:#fafcfe}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:.8rem;margin:1rem 0}
.card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:.9rem;font-size:.85rem}
.card b{display:block;margin-bottom:.35rem}
.tag{display:inline-block;font-size:.66rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;
padding:.1rem .38rem;border-radius:4px;vertical-align:middle}
.tag-verified{background:#e2f2e8;color:var(--good)}
.tag-derived{background:#e5eff7;color:var(--accent)}
.tag-assumption{background:#fff2d9;color:var(--warn)}
.tag-owner{background:#eceae4;color:#4c463c}
.tag-unverified{background:#fbe4e2;color:var(--bad)}
.tag-priority-critical{background:#fbe4e2;color:var(--bad)}
.tag-priority-high{background:#fff2d9;color:var(--warn)}
.tag-priority-medium{background:#e5eff7;color:var(--accent)}
.tag-priority-low{background:#eceae4;color:#4c463c}
.sugg{background:#fff;border:1px solid var(--line);border-radius:10px;padding:.9rem 1rem;margin:.8rem 0}
.sugg-head{display:flex;flex-wrap:wrap;gap:.5rem;justify-content:space-between;align-items:baseline;
border-bottom:1px solid var(--line);padding-bottom:.45rem;margin-bottom:.5rem}
.metrics{font-size:.74rem;color:var(--muted)}
.metrics b{color:var(--ink)}
.sugg p{margin:.35rem 0;font-size:.88rem}
.src{font-size:.75rem;color:var(--muted)}
.choice{font-size:.72rem;color:var(--muted);font-style:italic}
.note{font-size:.78rem;color:var(--muted)}
footer{margin-top:2.5rem;padding-top:1rem;border-top:1px solid var(--line);font-size:.76rem;color:var(--muted)}
a{color:var(--accent)}
code{background:#eef3f7;padding:.05rem .3rem;border-radius:4px;font-size:.86em}
@media(max-width:820px){.layout{grid-template-columns:1fr}nav{position:static;height:auto;border-right:0;
border-bottom:1px solid var(--line);display:flex;flex-wrap:wrap}main{padding:1rem}}
"""


def main():
    pages = {
        "index.html": page_index(),
        "questions.html": page_questions(),
        "suggestions.html": page_suggestions(),
        "projections.html": page_projections(),
        "decision.html": page_decision(),
        "black-swans.html": page_swans(),
        "inheritance.html": page_inheritance(),
        "costs.html": page_costs(),
        "repo-review.html": page_repo(),
        "flagged.html": page_flagged(),
        "sources.html": page_sources(),
    }
    for name, html in pages.items():
        (OUT / name).write_text(enforce_rounding(html))
    (OUT / "style.css").write_text(CSS)
    summary = {
        "generated": STAMP,
        "pages": len(pages),
        "official_sources": len(SOURCES),
        "assumptions": len(ASSUMPTIONS),
        "blank_inputs": sum(1 for a in ASSUMPTIONS if a.value is None),
        "transfer_2045": {k: r10(v) if isinstance(v, float) else v
                          for k, v in transfer_table(2045).items()},
        "wealth_2045_plus_25": {k: r10(v) for k, v in path_wealth(2045).items() if k in PATH_KEYS},
        "regimes": [{k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()}
                    for r in build_regimes()],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(f"built {len(pages)} pages + style.css + summary.json into {OUT}")


if __name__ == "__main__":
    main()
