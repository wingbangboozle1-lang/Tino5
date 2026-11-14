# -*- coding: utf-8 -*-
"""
Build the cbd/ desk: mixed paths, phased-entry test, deadlines, Attorney & CPA sheet,
questions, glossary, suggestions, sources and flagged items.

Run:   python3 cbd/_src/build.py        (writes static HTML into cbd/, then runs verify.py)

Every money figure is computed by desk_model.py and rounded to the nearest $10 by money().
The published artifact is static HTML and CSS. No script is published (see verify.py).
"""

import html
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)          # the cbd/ directory
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import desk_model as dm  # noqa: E402
import desk_sources as S  # noqa: E402
import desk_shell as shell  # noqa: E402

money = dm.money
pct = dm.pct
L = S.link

# ----------------------------------------------------------------- computed values

T45 = dm.stressed_table(2045)
T40 = dm.stressed_table(2040)
T50 = dm.stressed_table(2050)
JOINT45 = dm.paths_for_transfer(2045, joint=True)
PROCEEDS = T45["base"]["_meta"]["proceeds"]
SC = ["base", "crash2008", "crash1929"]


def pv(t, path, sc="base"):
    return t[sc][path]["pv"]


BE24 = dm.breakeven_trough(24)
BE36 = dm.breakeven_trough(36)
NO_CRASH_17 = (1.0 + dm.EQ_NET) ** (17.0 / 12.0)

# reinvestment shock on the phase-in paths (31-year horizon, same as the paths table)
YEARS_AFTER = T45["base"]["_meta"]["years_after"]


def shock_pv(n_months, shock):
    return (dm.phased_value(n_months, YEARS_AFTER, dm.EQ_NET, None, dm.CASH_NET, shock)
            * PROCEEDS / (1.0 + dm.DISC) ** YEARS_AFTER)


SHOCKS = [0.0, 0.01, 0.02]

# cbe break-evens (cbe/options.html, econ basis as published there)
import model as cm  # noqa: E402  (cbe model, read-only)
BE_YIELD = cm.breakeven_gross_yield("occupy")
BE_PRICE = cm.breakeven_price_growth("occupy")
BE_PORT = cm.breakeven_portfolio_return("occupy")
BE_YIELD_LET = cm.breakeven_gross_yield("rent")
BE_PRICE_LET = cm.breakeven_price_growth("rent")
BE_PORT_LET = cm.breakeven_portfolio_return("rent")

def dif(a, b):
    """Difference of two figures after each is rounded to $10, so a reader can re-add the page."""
    return dm.r10(a) - dm.r10(b)


E_COST_BASE = dif(pv(T45, "C"), pv(T45, "E"))
E_GAIN_2008 = dif(pv(T45, "E", "crash2008"), pv(T45, "C", "crash2008"))
E_GAIN_1929 = dif(pv(T45, "E", "crash1929"), pv(T45, "C", "crash1929"))


def best(t, sc, paths="ABCDEFG"):
    return max(paths, key=lambda p: t[sc][p]["pv"])


def path_label(pid):
    return dict((p, lbl) for p, lbl, _ in dm.PATHS)[pid]


BEST_BASE = best(T45, "base")
BEST_2008 = best(T45, "crash2008")
BEST_1929 = best(T45, "crash1929")

# ----------------------------------------------------------------- helpers


def td(x, cls=""):
    return '<td class="%s">%s</td>' % (cls, x)


def table(headers, rows, cls="t"):
    h = "".join("<th>%s</th>" % x for x in headers)
    body = "".join("<tr>%s</tr>" % "".join(r) for r in rows)
    return '<div class="scroll"><table class="%s"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (cls, h, body)


def src_cell(sid=None, note="No official source applies"):
    """An official link when the source was opened or reused; otherwise an explicit marker."""
    if sid and S.SOURCES[sid]["status"] in ("opened", "reused"):
        return L(sid, S.SOURCES[sid]["title"][:70])
    return '<span class="nosrc">%s</span>' % html.escape(note, quote=False)


def unverified(text="unverified"):
    return '<span class="flag">%s</span>' % text


def page(name, title, active, body, kind="std"):
    return shell.render(name, title, active, body, kind)


# ----------------------------------------------------------------- pages

def page_index():
    headline = (
        "<p class=\"lead\">Under the base assumptions the sale path that scores highest is "
        "<b>%s</b>: <b>%s</b> in present value at the transfer year (2045 midpoint), against "
        "<b>%s</b> for keeping the house and living in it. That ranking is the base case only. "
        "It changes if a deep fall in equities comes soon after the sale, which is the risk the "
        "phase-in is meant to cover.</p>"
    ) % (BEST_BASE, money(pv(T45, BEST_BASE)), money(pv(T45, "A")))

    change = [
        "<b>A market fall in the first 2 to 3 years after the sale.</b> A 2008-style fall at entry makes "
        "the 36-month phase-in (E) the best sale path, by %s over the lump sum. A 1929-style fall "
        "makes letting the house (B) the best of all seven paths, because B has no equity "
        "exposure." % money(E_GAIN_2008),
        "<b>The price of the phase-in in a rising market.</b> In the base case the 36-month phase-in gives up "
        "%s of present value against the lump sum (C). That is the premium paid for protection." % money(E_COST_BASE),
        "<b>Portfolio return.</b> Living in the house beats selling only if the net portfolio return is below "
        "<b>%s</b> a year; letting it beats selling only below <b>%s</b> (cbe break-evens, econ basis)." % (pct(BE_PORT), pct(BE_PORT_LET)),
        "<b>Rent for Property A.</b> Letting beats selling only at a gross yield of at least <b>%s</b> "
        "(cbe, let versus sell; living in it, <b>%s</b>). No rent figure for Property A has been supplied or verified." % (pct(BE_YIELD_LET), pct(BE_YIELD)),
        "<b>Price growth.</b> Living in the house beats selling only if house prices grow at least <b>%s</b> a year; "
        "letting it, at least <b>%s</b> (cbe break-evens)." % (pct(BE_PRICE), pct(BE_PRICE_LET)),
        "<b>Filing status for the home-sale exclusion.</b> A joint return doubles the exclusion from "
        "%s to %s, which changes path F (live 5 years, then sell)." % (money(dm.S121_SINGLE), money(dm.S121_JOINT)),
        "<b>Whether the transfer is into the trust as the statute describes.</b> The exclusion depends on "
        "the trust and the principal-residence tests. This desk has not read the trust instrument.",
    ]

    rate_src = td(L("tsy_curve", "Treasury yields") + '; <span class="nosrc">model arithmetic, 1-point shock is a what-if</span>', "src")
    reinv = table(
        ["Phase-in path (transfer 2045, 31 years, per the paths table)", "No shock", "Cash rate down 1 point after 12 months", "Down 2 points", "Source"],
        [
            [td("D: sell, 24 months"), td(money(shock_pv(24, 0.0)), "n"),
             td(money(shock_pv(24, 0.01)), "n"), td(money(shock_pv(24, 0.02)), "n"), rate_src],
            [td("E: sell, 36 months"), td(money(shock_pv(36, 0.0)), "n"),
             td(money(shock_pv(36, 0.01)), "n"), td(money(shock_pv(36, 0.02)), "n"), rate_src],
        ],
    )

    body = """
<section class="first">
  <h1>Property A: sell, let or live in it, and how to phase in the money</h1>
  <p class="sub">Summary for the owner, the attorney and the tax adviser. Figures in present value at the
  2045 midpoint of the 2040 to 2050 transfer window, rounded to the nearest $10.</p>
  <div class="split">
    <div class="card hl">
      <h2>Headline</h2>
      %(headline)s
      <p class="small">Cash basis, as in the owner-brief options page. Living in the house is shown at its cash value
      only, so it looks worse than it is. The imputed rent is shown on the options page.</p>
    </div>
    <div class="card rr">
      <h2>Reinvestment risk, beside the headline</h2>
      <p>The sale proceeds are assumed to sit in 3-month Treasury bills at <b>4.32%%</b> (Treasury,
      13 November 2026), which is <b>%(cash)s</b> after federal tax at 37%% and the 3.8%% surcharge. Equity is
      assumed at <b>%(eq)s</b> net. The gap between those two rates is the cost of waiting.</p>
      %(reinv)s
      <p class="small">If bill rates fall, the phase-in earns less while it waits. The loss is small, because the
      money is parked for only 24 to 36 months.</p>
    </div>
  </div>

  <div class="card wc">
    <h2>What would change the answer</h2>
    <ol>%(change)s</ol>
  </div>
</section>

<section>
  <h2>Pick a path</h2>
  <p>The table below has the seven paths, with a row-level source on each. The full table with
  the stress columns is on <a href="paths.html">Mixed paths</a>. The phase-in mechanics are tested on
  <a href="phased.html">the phased entry test</a>. The interactive calculator for the same mechanics is
  <a href="../cbe/phased-investing.html">cbe/phased-investing.html</a>, built by another session.</p>
  %(summary)s
</section>

<section class="grid4">
  <a class="card" href="paths.html"><b>Mixed paths</b><span>Seven paths, three crash scenarios, three transfer years.</span></a>
  <a class="card" href="phased.html"><b>Phased entry test</b><span>1929 and 2008 entry crashes, break-even trough levels.</span></a>
  <a class="card" href="timeline.html"><b>Deadlines timeline</b><span>The dated steps, with the statute behind each.</span></a>
  <a class="card" href="brief.html"><b>Attorney &amp; CPA sheet</b><span>One printable page for the two advisers.</span></a>
</section>
""" % dict(
        headline=headline,
        cash=pct(dm.CASH_NET),
        eq=pct(dm.EQ_NET),
        reinv=reinv,
        change="".join("<li>%s</li>" % c for c in change),
        summary=summary_table(),
    )
    return page("index.html", "Summary", "index", body)


def summary_table():
    rows = []
    labels = {"A": "Live in it, hold it", "B": "Let it out, hold it",
              "C": "Sell at transfer, one lump sum", "D": "Sell, phase in over 24 months",
              "E": "Sell, phase in over 36 months",
              "F": "Live 5 years, then sell and phase in over 36 months",
              "G": "Let 5 years, then sell and phase in over 24 months"}
    for pid in "ABCDEFG":
        rows.append([
            td(pid, "c"), td(labels[pid]),
            td(money(pv(T45, pid)), "n"),
            td(money(pv(T45, pid, "crash2008")), "n"),
            td(money(pv(T45, pid, "crash1929")), "n"),
            td(src_for_path(pid), "src"),
        ])
    return table(["Path", "What it means", "Base", "2008-style fall at entry", "1929-style fall at entry", "Sources"],
                 rows)


def page_paths():
    rows = []
    for pid, lbl, _ in dm.PATHS:
        base = pv(T45, pid)
        rows.append([
            td(pid, "c"),
            td(lbl),
            td(money(pv(T40, pid)), "n"),
            td(money(base), "n"),
            td(money(pv(T50, pid)), "n"),
            td(money(pv(T45, pid, "crash2008")), "n"),
            td(money(pv(T45, pid, "crash1929")), "n"),
            td(src_for_path(pid), "src"),
        ])
    main_table = table(
        ["Path", "Description", "Transfer 2040", "Transfer 2045 (base)", "Transfer 2050",
         "2008-style fall at entry", "1929-style fall at entry", "Sources"],
        rows)
    joint = table(["Path", "Single filer (base)", "Joint return", "Source"],
                  [[td("F"), td(money(pv(T45, "F")), "n"), td(money(JOINT45["F"]["pv"]), "n"),
                    td(L("irs_701", "IRS Topic 701 ($250,000 / $500,000)"), "src")]])
    whatif = whatif_table()
    body = """
<h1>Mixed paths</h1>
<p class="sub">Seven ways to hold the house, not three. Every path is a present value in the transfer
year, on the cash basis used by the owner-brief options page, and discounted at the 5.0%% rate used there.</p>
<div class="banner">Reading the table: paths A and B hold the house, so a market fall does not change them.
Paths C to G put money into equities, so the stress columns move them. Path F sells after 5 years of living
in the house. Path G sells after 5 years of letting it out. The 5-year sale date is an assumption.</div>
<h2>Present value by path, transfer year and crash scenario</h2>
%(main)s
<h2>Filing status for path F</h2>
<p>The home-sale exclusion is $250,000 for a single filer and $500,000 on a joint return (IRS). The
filing status of the eventual owner is not known, so the single figure is the base.</p>
%(joint)s
%(whatif)s
<h2>How each row is built</h2>
<ul>
<li><b>A and B</b> are the cbe owner-brief values, unchanged: <a href="../cbe/options.html">cbe/options.html</a>. Their
property inputs are owner records with no official source (flag F01).</li>
<li><b>C, D, E</b> sell at transfer. The proceeds are the cbe figure after the 6.0%% selling cost. D and E
invest them in equal monthly tranches over 24 or 36 months, parked in 3-month bills at the after-tax rate until
bought (Phase-in test on <a href="phased.html">phased.html</a>).</li>
<li><b>F</b> lives in the house for 5 years, collecting the cbe occupancy cash flows. It then sells. The gain
above the $250,000 exclusion is taxed at 37.1%% (20%% federal, 3.8%% net investment income tax, 13.3%% California).
The remaining proceeds are phased in over 36 months.</li>
<li><b>G</b> lets the house for 5 years, collecting the cbe rent cash flows. On sale the depreciation taken is
recaptured at 42.1%% (25%% federal, 3.8%%, 13.3%%). The rest of the gain is taxed at 37.1%%. The remaining proceeds
are phased in over 24 months.</li>
<li>Crash scenarios: a 57%% fall over 17 months from entry (2008) and an 89%% fall over 34 months (1929), then growth
at the net return. Both are stylised paths built from the official peak-to-trough figures; they are not the
actual daily record.</li>
</ul>
<p>Known gaps, all flagged: California tax on Treasury interest is not modelled. California conformity with the
federal home-sale exclusion is not modelled, which is conservative for path F. The depreciation period of
27.5 years is an assumption carried from the cbe desk.</p>
""" % dict(main=main_table, joint=joint, whatif=whatif)
    return page("paths.html", "Mixed paths", "paths", body)


NOSRC_OWNER = "No official source for owner property figures (flag F01); model arithmetic from cbe"


WHATIF_CASES = [
    ("Base: equity 6.40% net, parked cash 2.56% after tax", None, None),
    ("Equity 1 point lower (5.40% net)", dm.EQ_NET - 0.01, None),
    ("Equity 1 point higher (7.40% net)", dm.EQ_NET + 0.01, None),
    ("Parked cash 1 point lower after tax (1.56%)", None, dm.CASH_NET - 0.01),
    ("Parked cash 1 point higher after tax (3.56%)", None, dm.CASH_NET + 0.01),
    ("Weak markets and low bill rates together", dm.EQ_NET - 0.01, dm.CASH_NET - 0.01),
]


def whatif_table():
    rows = []
    for lbl, eq, cash in WHATIF_CASES:
        t = dm.stressed_table(2045, eq=eq, cash=cash)
        rows.append([
            td(lbl),
            td(money(pv(t, "C")), "n"), td(money(pv(t, "E")), "n"),
            td(money(dif(pv(t, "E"), pv(t, "C"))), "n"),
            td(money(pv(t, "C", "crash2008")), "n"), td(money(pv(t, "E", "crash2008")), "n"),
            td(money(dif(pv(t, "E", "crash2008"), pv(t, "C", "crash2008"))), "n"),
            td(L("tsy_curve", "Treasury") + " (cash); " + L("irs_niit", "IRS NIIT") + " (tax)", "src"),
        ])
    return ("<h2>What if: change the return and the cash rate</h2>"
            "<p>Each row changes one or both inputs and reruns the model at the 2045 transfer year. The "
            "values are present values in the transfer year.</p>"
            + table(["Case", "C, sell lump (base)", "E, 36 months (base)", "E less C (base)",
                     "C, 2008-style", "E, 2008-style", "E less C (2008)", "Source"], rows))


def src_for_path(pid):
    return {
        "A": NOSRC_OWNER + "; rate rule: " + L("boe_lta26026", "BOE LTA 2026/026"),
        "B": NOSRC_OWNER,
        "C": L("tsy_curve", "Treasury yields") + ", " + L("fed_2008", "Fed History") ,
        "D": L("tsy_curve", "Treasury yields") + ", " + L("fed_2008", "Fed History"),
        "E": L("tsy_curve", "Treasury yields") + ", " + L("fed_2008", "Fed History"),
        "F": L("irs_701", "IRS Topic 701") + ", " + L("irs_409", "IRS Topic 409") + ", " + L("irs_niit", "IRS NIIT"),
        "G": L("irs_409", "IRS Topic 409") + ", " + L("irs_701", "IRS Topic 701"),
    }[pid]


def page_phased():
    trough_levels = [
        ("2008-style: fall of 57% by month 17", 1.0 - dm.CRASH_2008, dm.MONTHS_2008),
        ("1929-style: fall of 89% by month 34", 1.0 - dm.CRASH_1929, dm.MONTHS_1929),
        ("Trough 30% below entry, at month 17", 0.70, dm.MONTHS_2008),
        ("Trough 10% below entry, at month 17", 0.90, dm.MONTHS_2008),
        ("Trough at the entry level, at month 17", 1.00, dm.MONTHS_2008),
        ("Trough 5% above entry, at month 17", 1.05, dm.MONTHS_2008),
        ("No crash: growth at the net return", None, None),
    ]
    rows = []
    for lbl, lev, months in trough_levels:
        crash = None if lev is None else (lev, months)
        lump = dm.phased_value(1, 10, dm.EQ_NET, crash)
        p24 = dm.phased_value(24, 10, dm.EQ_NET, crash)
        p36 = dm.phased_value(36, 10, dm.EQ_NET, crash)
        vals = dict(lump=lump, p24=p24, p36=p36)
        top = max(vals, key=vals.get)
        name = {"lump": "Lump sum", "p24": "24-month phase-in", "p36": "36-month phase-in"}[top]
        rows.append([
            td(lbl),
            td(pct(lev if lev is not None else (1.0 + dm.EQ_NET) ** (dm.MONTHS_2008 / 12.0), 1), "n"),
            td(money(lump * PROCEEDS), "n"), td(money(p24 * PROCEEDS), "n"),
            td(money(p36 * PROCEEDS), "n"), td(name, "c"),
            td(L("tsy_curve", "Treasury yields") + "; " + L("fed_2008", "Fed History") if lev is not None
               and months == dm.MONTHS_2008 else
               (L("fed_1929", "Fed History (1929)") + "; " + L("tsy_curve", "Treasury yields")
                if lev is not None else "Model arithmetic only; no crash input. " + L("tsy_curve", "Treasury yields")), "src"),
        ])
    grid = table(["Market path", "Index at trough (entry = 100%)", "Lump sum, 10 years",
                  "24-month phase-in, 10 years", "36-month phase-in, 10 years", "Highest", "Sources"],
                 rows)
    body = """
<h1>Phased entry test: 1929 and 2008 crash risk</h1>
<p class="sub">Whether to invest the proceeds in one go, or to park them in Treasury bills and buy in
equal monthly tranches over 24 or 36 months. This page tests the entry risk. The mechanics are the same
as the calculator on <a href="../cbe/phased-investing.html">cbe/phased-investing.html</a>, built in the
owner-brief desk, which this desk links to rather than duplicates.</p>

<div class="banner">Each 'dollar' below is the proceeds of the sale, using the transfer-year figure of
<b>%(proceeds)s</b>. The test runs over 10 years from entry, not to the 2076 horizon used on the paths page.</div>

<h2>Break-even: how deep must the crash be?</h2>
<div class="card hl">
<p>A 24-month phase-in ends level with the lump sum after 10 years if the market is <b>at or below %(be24)s
of its entry level</b> at the 17-month trough. A 36-month phase-in breaks even at <b>%(be36)s</b>.
Above those levels, the lump sum wins; below them, the phase-in wins.</p>
<p class="small">Break-even levels are computed by bisection on the model, not read from a published table.</p>
</div>

<h2>Trough levels tested</h2>
%(grid)s

<h2>How the model moves the market</h2>
<ul>
<li>Before the trough, the index moves from 100%% to the trough level over 17 months. After the trough it grows at
the net return of <b>%(eq)s</b> a year.</li>
<li>Parked cash earns <b>%(cash)s</b> a year after federal tax and the 3.8%% surcharge, from the Treasury
3-month rate of 4.32%% on 13 November 2026.</li>
<li>The 2008 fall (57%%) and the 1929 fall (89%%) are the official peak-to-trough figures from Federal Reserve
History. The 1929 figure is for the Dow Jones Industrial Average, which has no dividends.</li>
</ul>

<h2>Reinvestment risk</h2>
<p>Parked cash earns less than the market, and less still if bill rates fall. For the 36-month
phase-in, a fall of 2 points in the cash rate after the first 12 months lowers the value at 2076 by
<b>%(drop2)s</b>. It is the price of waiting that matters, more than the risk of the rate itself.</p>

<h2>Why the phase-in is not free</h2>
<p>In the base case with no crash, the 36-month phase-in gives up <b>%(cost)s</b> of present value against the lump
sum. In the 2008-style case it gains <b>%(g08)s</b>. In the 1929-style case it gains <b>%(g29)s</b>. Whether that
trade is worth making depends on the probability of a deep fall in the first few years, which this model does
not estimate.</p>
""" % dict(
        proceeds=money(PROCEEDS), be24=pct(BE24[0], 1), be36=pct(BE36[0], 1),
        grid=grid, eq=pct(dm.EQ_NET), cash=pct(dm.CASH_NET),
        drop2=money(dif(shock_pv(36, 0.0), shock_pv(36, 0.02))),
        cost=money(E_COST_BASE), g08=money(E_GAIN_2008), g29=money(E_GAIN_1929),
    )
    return page("phased.html", "Phased entry test", "phased", body)


def page_timeline():
    steps = [
        ("Day 0", "Death of the owner; the trust holds the home", "Starts every clock below.",
         '<span class="nosrc">No official source: the date of death starts the federal and state clocks</span>',
         "The filing threshold year is the year of death."),
        ("Within 9 months", "Form 706 due, if a return is required",
         "Due nine months after the date of death. An automatic six-month extension is available on Form 4768 filed by the due date.",
         L("irs_faq_estate", "IRS FAQ on estate taxes"), "Required only if the gross estate is above the filing threshold ($15,000,000 for a 2026 death)."),
        ("Within 1 year", "Move in and make it the principal residence",
         "The transferee must make the home a principal residence within one year of the transfer.",
         L("rtc_63_2", "R&amp;TC 63.2(a)(1)(A)"), "Missing this ends the exclusion. Path F assumes it is met."),
        ("Within 1 year", "File for the homeowners' exemption",
         "File within a year of the transfer.",
         L("rtc_63_2", "R&amp;TC 63.2(a)(1)(B)"), "The exclusion is not available without it."),
        ("Within 3 years, or earlier", "File the exclusion claim",
         "Within three years of the transfer, or before a transfer to a third party, or when an eligible transferee stops occupying the home, whichever is earlier.",
         L("rtc_63_2", "R&amp;TC 63.2(f)(1)(A)"), "The claim is not a public document (R&amp;TC 63.2(c))."),
        ("6 months after a notice", "Late claim after a supplemental or escape assessment",
         "A claim is timely if filed within six months after the mailing of a supplemental or escape assessment notice.",
         L("rtc_63_2", "R&amp;TC 63.2(f)(1)(B)"), "Keep the assessor's notices."),
        ("Year 5 (assumption)", "Path F or G: sell the home",
         "The home-sale exclusion needs 24 months of ownership and use in the 5 years before the sale.",
         L("irs_701", "IRS Topic 701"), "Five years is an assumption of this desk, tested on the paths page."),
        ("Year 5 onward", "Phase the proceeds into the market",
         "The phase-in runs 24 or 36 monthly tranches, after the sale.",
         '<span class="nosrc">No official source: the phase-in is a chosen strategy</span>',
         "Tranche length is a choice; see the phased test."),
    ]
    rows = [[td(a), td(b), td(c), td(d, "src"), td(e)] for a, b, c, d, e in steps]
    tl = table(["When", "Step", "What the rule says", "Source", "What it means here"], rows)
    body = """
<h1>Deadlines timeline</h1>
<p class="sub">Only the steps below are on this page, and each is read from the statute or the IRS text named
in its source cell. Steps reported elsewhere but not re-opened here are on <a href="flagged.html">Flagged for review</a>.</p>
<div class="banner warn">This is a timeline of rules, not advice. The attorney confirms the trust
instrument and the dates for the actual transfer.</div>
<div class="timeline">
%(bars)s
</div>
%(tl)s
""" % dict(tl=tl, bars="".join(
        '<div class="tick"><span class="when">%s</span><span class="what">%s</span></div>' % (a, b)
        for a, b, *_ in steps))
    return page("timeline.html", "Deadlines timeline", "timeline", body)


def page_brief():
    body = """
<div class="sheet">
<h1>Attorney &amp; CPA briefing sheet</h1>
<p class="small">Property A (trust inheritance, expected 2040 to 2050) and Property B (owned now, two of three units
let). Figures are present values at the 2045 midpoint, rounded to the nearest $10. Cash basis. Placeholders only.</p>

<table class="t brief">
<thead><tr><th>Figure</th><th>Value</th><th>Source</th></tr></thead>
<tbody>
<tr><td>Sell at transfer, one lump sum (C), base</td><td class="n">%(C)s</td><td>%(src_c)s</td></tr>
<tr><td>Sell, phased over 36 months (E), base</td><td class="n">%(E)s</td><td>%(src_e)s</td></tr>
<tr><td>Live in it, hold it (A), base</td><td class="n">%(A)s</td><td>%(src_a)s</td></tr>
<tr><td>Let it out, hold it (B), base</td><td class="n">%(B)s</td><td>%(src_b)s</td></tr>
<tr><td>Phase-in premium over the lump sum, base (C less E)</td><td class="n">%(prem)s</td><td><span class="nosrc">model difference; inputs as C and E (F01, F13)</span></td></tr>
<tr><td>Value of the 36-month phase-in in a 2008-style fall</td><td class="n">%(g08)s</td><td>%(src_2008)s; <span class="nosrc">model result</span></td></tr>
<tr><td>Home-sale exclusion, single filer / joint return</td><td class="n">%(s1)s / %(s2)s</td><td>%(src_701)s</td></tr>
<tr><td>Net portfolio return used (base)</td><td class="n">%(eq)s</td><td>%(src_tsy)s (cash side); <span class="nosrc">equity return assumed (F13)</span></td></tr>
<tr><td>Parked cash, after tax (3-month bill 4.32%%)</td><td class="n">%(cash)s</td><td>%(src_tsy)s; %(src_niit)s</td></tr>
</tbody>
</table>

<h3>For the attorney</h3>
<ol class="q">
<li>Confirm the trust is an inter vivos or testamentary trust that passes present beneficial ownership (R&amp;TC 63.2(e)(9)). Source: %(src_rtc)s.</li>
<li>Confirm no interest in a legal entity holds the home (R&amp;TC 63.2(e)(8)). Source: %(src_rtc)s.</li>
<li>Confirm the home is the transferor's principal residence and that it stays one for the transferee within one year (R&amp;TC 63.2(a)(1)(A)).</li>
<li>Confirm the claim deadline in R&amp;TC 63.2(f)(1)(A) and who will file it.</li>
<li>Confirm the notice duties for the trustee and any notice of supplemental or escape assessment.</li>
</ol>

<h3>For the tax adviser</h3>
<ol class="q">
<li>Confirm the federal filing threshold for the year of death and whether Form 706 is needed (%(src_faq)s).</li>
<li>Confirm California treatment of Treasury interest on the parked proceeds. Not modelled here; flagged F04.</li>
<li>Confirm California conformity with the federal home-sale exclusion. Not modelled; conservative for path F; flagged F05.</li>
<li>Confirm the filing status, which changes the home-sale exclusion from %(s1)s to %(s2)s (%(src_701)s).</li>
<li>Confirm the basis of inherited property and the depreciation method for any letting period (%(src_409)s).</li>
</ol>

<p class="small">Not advice. Sources and every open item: <a href="sources.html">sources</a>,
<a href="flagged.html">flagged for review</a>. The attorney and CPA verify every figure against the actual documents.</p>
</div>
""" % dict(
        C=money(pv(T45, "C")), E=money(pv(T45, "E")), A=money(pv(T45, "A")), B=money(pv(T45, "B")),
        prem=money(E_COST_BASE), g08=money(E_GAIN_2008),
        s1=money(dm.S121_SINGLE), s2=money(dm.S121_JOINT),
        eq=pct(dm.EQ_NET), cash=pct(dm.CASH_NET),
        src_c='<span class="nosrc">No official source for owner figures (F01); equity return assumed (F13)</span>',
        src_e=L("tsy_curve", "Treasury") + " (cash side); " + '<span class="nosrc">equity return assumed (F13)</span>',
        src_a=L("boe_lta26026", "BOE LTA 2026/026") + ' (rate rule); <span class="nosrc">owner figures have no official source (F01)</span>',
        src_b='<span class="nosrc">No official source for owner figures (F01)</span>',
        src_2008=L("fed_2008", "Fed History"), src_701=L("irs_701", "IRS Topic 701"),
        src_tsy=L("tsy_curve", "Treasury"), src_niit=L("irs_niit", "IRS NIIT"),
        src_rtc=L("rtc_63_2", "R&amp;TC 63.2"), src_faq=L("irs_faq_estate", "IRS FAQ"),
        src_409=L("irs_409", "IRS Topic 409"),
    )
    return page("brief.html", "Attorney & CPA sheet", "brief", body, kind="print")


QUESTIONS = [
    ("Q01", "Which path scores highest in the base case?", "Known", "Path C (sell, lump sum). Model result, not advice.", "Mixed paths", "cbe_model"),
    ("Q02", "Which path wins if a deep fall comes in the first 2 to 3 years?", "Known (model)", "Path E (36-month phase-in) after a 2008-style fall; path B after a 1929-style fall.", "Mixed paths", "fed_2008"),
    ("Q03", "How deep a fall makes the 24-month phase-in better over 10 years?", "Known (model)", "A trough at or below 102.2% of the entry level.", "Phased test", "tsy_curve"),
    ("Q04", "What is the transfer date?", "Missing", "Not known; 2040 to 2050 window. Midpoint 2045 is used.", "Ask the owner and the attorney", "boe_lta26026"),
    ("Q05", "Will the home be the owner's principal residence on transfer, and for how long will the heir live there?", "Missing", "Unknown. Decides whether the Prop 19 exclusion and the home-sale exclusion apply.", "Attorney; owner's plan", "rtc_63_2"),
    ("Q06", "Is the trust an eligible trust and is the property held in it directly, not in an entity?", "Missing", "Not known. The trust instrument has not been read by this desk.", "Attorney", "rtc_63_2"),
    ("Q07", "What is the market rent for Property A?", "Missing", "Not known. Letting beats selling only at a gross yield of at least %s." % pct(BE_YIELD), "Obtain two written rent estimates", "cbe_model"),
    ("Q08", "What are the insurance premiums for Property A and Property B?", "Missing", "The owner's estimate is $1,500 a year for each. Not verified; no quote obtained.", "Obtain quotes", "boe_lta26026"),
    ("Q09", "What is the 2025 secured tax bill and assessed value for each property?", "Owner record", "Owner records only (cbe). Not checked against the county roll.", "County assessor or tax bill", "boe_lta26026"),
    ("Q10", "Is the home-sale exclusion single or joint?", "Missing", "Not known. Single $250,000; joint $500,000.", "Owner's filing status", "irs_701"),
    ("Q11", "Will the total estate exceed the federal filing threshold?", "Known (rule)", "Threshold is $15,000,000 for a 2026 death. Whether the estate exceeds it is not known.", "Attorney and CPA, from a full asset list", "irs_faq_estate"),
    ("Q12", "What is the California tax on Treasury interest for the owner?", "Missing", "Not modelled. Flagged.", "CPA", "tsy_curve"),
    ("Q13", "What is the 3-month and 2-year Treasury yield on the transfer date?", "Unknown (future)", "Known only for 13 November 2026 (4.32% and 4.88%). Future yields are a what-if.", "Check the Treasury curve at the time", "tsy_curve"),
    ("Q14", "What does the sale of Property A cost, after commission, transfer tax and escrow?", "Assumption", "6.0%% of value, an assumption (cbe).", "Obtain a sale estimate", "cbe_model"),
    ("Q15", "Does the homeowners' exemption and the claim fall within the one-year window?", "Known (rule)", "The rule is one year; the actual dates depend on the transfer.", "Attorney", "rtc_63_2"),
    ("Q16", "How much is in Property B's own costs, and does Property B have a tax residue?", "Owner record", "The cbe desk carries a residual charge on the Property B bill; its composition is unknown (flag F01).", "Tax bill line items", "boe_lta26026"),
    ("Q17", "What is the owner's own cash position, and what is the rest of the estate?", "Missing", "Not supplied. Needed to decide the scale of any phase-in.", "Owner", "irs_faq_estate"),
    ("Q18", "What is the tax on a sale if the home has been let for part of the period?", "Known (rule)", "Recapture at up to 25% for depreciation taken (path G).", "CPA", "irs_409"),
]


QNOTE = {
    "Q01": "Model result from owner records; no official source for the owner's figures (flag F01)",
    "Q02": "Scenario from official peak-to-trough figures; path choice is model output",
    "Q03": "Model result; inputs are the official yields and crash figures",
    "Q04": "No official source: the transfer date is an owner-plan fact",
    "Q05": "Statutory test, read below; the owner's facts are not official",
    "Q06": "Statutory test, read below; the trust instrument has not been read",
    "Q07": "No official source: no rent figure exists for Property A",
    "Q08": "No official source: owner estimate, no quote obtained (flag F03)",
    "Q09": "No official source: owner record, rounded (flag F01)",
    "Q10": "Statutory amounts, read below",
    "Q11": "Statutory threshold read below; the estate's value is not official",
    "Q12": "No official source: not modelled (flag F04)",
    "Q13": "Official curve for 13 Nov 2026; future yields have no source",
    "Q14": "No official source: model assumption (cbe, 6.0% of value)",
    "Q15": "Statutory deadline read below",
    "Q16": "No official source: owner tax-bill residue, composition unknown (flag F01)",
    "Q17": "No official source: owner fact not supplied",
    "Q18": "Statutory rate read below",
}


def page_questions():
    rows = []
    for qid, q, status, answer, where, sid in QUESTIONS:
        rows.append([td(qid, "c"), td(q), td(status), td(answer), td(where), td(src_cell(sid, QNOTE.get(qid, "No official source applies")), "src")])
    body = """
<h1>Questions, answers and information still needed</h1>
<p class="sub">Each question is answered from a verified source, from the model, or marked as missing with the way to close it.</p>
%s
""" % table(["ID", "Question", "Status", "Answer or gap", "How to close it", "Source"], rows)
    return page("questions.html", "Questions and gaps", "questions", body)


GLOSSARY = [
    ("Proposition 19 intergenerational exclusion", "A California rule that can exclude a transfer of a family home from reassessment when it passes between parent and child, if the statutory conditions are met.", "boe_lta26026"),
    ("Family home / principal residence", "A dwelling eligible for the homeowners' exemption because of the transferor's ownership and occupation.", "rtc_63_2"),
    ("Homeowners' exemption", "The California exemption filed by an owner-occupier. The transferee must file for it within a year.", "rtc_63_2"),
    ("Value cap (excluded amount)", "The factored base year value plus $1,000,000, adjusted as stated in the Board's FAQ.", "boe_lta26026"),
    ("Full cash value", "The value used for reassessment, as defined in the statute at the date of transfer.", "rtc_63_2"),
    ("Base year value / new base year value", "The assessed value the county carries; the new base year value is enrolled if the exclusion is removed.", "boe_lta26026"),
    ("Home-sale exclusion", "The federal exclusion of up to $250,000 of gain ($500,000 joint), if the ownership and use tests are met.", "irs_701"),
    ("Ownership and use tests", "Each needs 24 months in the 5 years before the sale.", "irs_701"),
    ("Net investment income tax", "A 3.8% tax on investment income above the statutory threshold. Gain excluded from income under the home-sale rules is outside it.", "irs_niit"),
    ("Unrecaptured section 1250 gain", "The part of a gain on real property equal to depreciation taken, taxed at a maximum 25% federal rate.", "irs_409"),
    ("Form 706", "The federal estate tax return, due nine months after the date of death, extendable by six months on Form 4768.", "irs_faq_estate"),
    ("Filing threshold", "The gross estate value above which a federal estate tax return is required, for the year of death.", "irs_faq_estate"),
    ("Portability", "An election to pass a deceased spouse's unused exclusion to the survivor. It requires a timely filed return.", "irs_faq_estate"),
    ("Constant maturity Treasury yield", "The Treasury's daily yield for a given maturity, from the par yield curve. The 3-month and 2-year rates are used here.", "tsy_curve"),
    ("Treasury bill", "A short-term U.S. government security. Parking proceeds in bills is the cash side of the phase-in.", "tsy_curve"),
    ("Phase-in (dollar-cost averaging)", "Buying an asset in equal instalments over time instead of all at once. Explanatory; no figure is taken from a source.", None),
    ("Peak-to-trough decline", "The fall from a market's highest close to its lowest close that follows. Used for the 1929 and 2008 paths.", "fed_2008"),
    ("Reinvestment risk", "The risk that cash is rolled into a lower rate than expected. Explanatory; no figure is taken from a source.", None),
    ("Present value", "Future money discounted back to the transfer year at the 5.0% rate used on the owner-brief desk. Explanatory.", None),
    ("Cash basis / econ basis", "Cash basis counts only money. Econ basis adds the market rent of the home the household lives in. Both are on the owner-brief options page.", None),
    ("Basis (of inherited property)", "The starting value for measuring gain. The model assumes the basis is the value at transfer. See IRS Publication 551 for the rule.", "irs_409"),
]


def page_glossary():
    rows = []
    for term, defi, sid in GLOSSARY:
        src = L(sid, S.SOURCES[sid]["title"]) if sid else "No official source: explanatory definition, no figure"
        rows.append([td(term), td(defi), td(src, "src")])
    body = """
<h1>Glossary</h1>
<p class="sub">Each term is linked to the official page that defines it. Terms marked as explanatory carry no
figure, and say so.</p>
%s
""" % table(["Term", "Meaning in this desk", "Official source"], rows)
    return page("glossary.html", "Glossary", "glossary", body)


SUGGESTIONS = [
    ("S01", "Add crash-timing grid: move the fall to month 12, 24 and 36 after the sale", "Shows whether the phase-in helps when a fall comes later in the window, not only at entry.", "PROPOSED"),
    ("S02", "Add interactive what-if controls to this desk", "This desk publishes no script (publish-boundary rule). Options: keep static grids, or allow one same-origin script, as cbe/phased-investing.html already does.", "PROPOSED: owner decides"),
    ("S03", "Obtain two written rent estimates for Property A", "Sets the gross yield, which decides whether letting beats selling (break-even %s)." % pct(BE_YIELD), "PROPOSED"),
    ("S04", "Obtain homeowners' insurance quotes for both properties", "The $1,500 owner estimate is unverified; no quote has been obtained.", "PROPOSED"),
    ("S05", "Confirm filing status for the home-sale exclusion", "Changes path F from $250,000 to $500,000 of excluded gain.", "PROPOSED"),
    ("S06", "Have the CPA confirm California tax on Treasury interest", "Not modelled. Changes the parked cash yield and so the phase-in.", "PROPOSED"),
    ("S07", "Have the CPA confirm California conformity with the federal home-sale exclusion", "Not modelled; path F is conservative until confirmed.", "PROPOSED"),
    ("S08", "Test the sale year (2 years, 5 years, 10 years) instead of a single 5-year assumption", "Shows how sensitive the mixed paths are to the sale date.", "PROPOSED"),
    ("S09", "Re-open the three reused sources (IR-2026-133, FTB 2025 rate schedule, and the cbe trustee-notice rule)", "Each is marked reused on the sources page; they should be re-read before publication.", "PROPOSED"),
    ("S10", "Decide the repository privacy question: history rewrite, repository visibility, or leave as is", "Earlier commits contain unrounded figures (cbe flag F19). A history rewrite on main changes shared history and must be the owner's decision. Nothing has been rewritten.", "OWNER DECISION: not executed"),
]


def page_suggestions():
    rows = [[td(a, "c"), td(b), td(c), td(d), td('<span class="nosrc">No official source: a proposal, not a fact</span>', "src")]
            for a, b, c, d in SUGGESTIONS]
    body = """
<h1>Suggestions for review</h1>
<div class="banner red"><b>Nothing on this list has been implemented.</b> Each suggestion needs an
accept, modify or reject decision before any change is made. Record the decision against the
suggestion ID in COORDINATION.md.</div>
%s
""" % table(["ID", "Suggestion", "Why", "Status", "Source"], rows)
    return page("suggestions.html", "Suggestions", "suggestions", body)


SOURCE_NOTES = {
    "tsy_curve": "Treasury 3-month and 2-year yields, 13 Nov 2026",
    "fed_1929": "1929 peak and trough, 89 percent decline",
    "fed_2008": "2008 decline of 57 percent",
    "irs_701": "Home-sale exclusion, ownership and use tests",
    "irs_409": "Capital gains rates, unrecaptured section 1250 gain",
    "irs_niit": "3.8 percent net investment income tax",
    "irs_faq_estate": "Form 706 due date, extension, threshold for 2026",
    "boe_lta26026": "Proposition 19 definitions and value cap",
    "rtc_63_2": "Move-in, exemption and claim deadlines",
    "rtc_17043": "1 percent additional tax above $1,000,000",
    "irs_ir2026_133": "37 percent top rate (reused, not re-opened)",
    "ftb_rates": "12.3 percent top rate (reused, not re-opened)",
    "cbe_model": "Property values, rents, costs, break-evens (cbe desk)",
    "cbe_phased": "Phased-investing calculator (cbe desk)",
}


def page_sources():
    rows = []
    for sid, s in S.SOURCES.items():
        note = SOURCE_NOTES.get(sid, "")
        if s["status"] == "internal":
            note = '<span class="nosrc">No official source: internal page</span> ' + note
        rows.append([td(S.tag(sid)), td(s["title"]), td(s["read"]), td(note, "src")])
    body = """
<h1>Sources</h1>
<p class="sub">Every source used on this desk. "Opened" means the text was read in this session. "Reused" means
it was taken from the cbe/ register and has not been re-opened here; each reused source is flagged.</p>
%s
""" % table(["Publisher", "Title", "What was read or how it is used", "Supports"], rows)
    return page("sources.html", "Sources", "sources", body)


FLAG_SRC = {
    "F01": "No official source: owner record (flag F01)",
    "F02": "No official source: no rent figure exists",
    "F03": "No official source: owner estimate",
    "F04": "No official source read; open question for the CPA",
    "F05": "No official source read; open question for the CPA",
    "F06": "__ftb_rates__",
    "F07": "__irs_ir2026_133__",
    "F08": "No official source read here; statute not re-opened",
    "F09": "No official source read here; county page not re-opened",
    "F10": "__fed__",
    "F11": "No official source: assumption",
    "F12": "No official source: assumption",
    "F13": "No official source: assumption",
    "F14": "BOE LTA 2025/009 not re-opened here; No official source read here",
    "F15": "No official source read here; IRS Publication 527 not re-opened",
    "F16": "No official source: a repository matter; see cbe/repo-review.html",
}

FLAGS = [
    ("F01", "Owner property tax and assessed-value history for Property A and B", "Owner records, rounded to $10. Not checked against county rolls.", "Owner / county assessor", "unverified"),
    ("F02", "Market rent for Property A", "No figure supplied. Only the break-even yield is published.", "Written rent estimates", "unverified"),
    ("F03", "Insurance premiums for both properties", "$1,500 a year each is the owner's estimate.", "Quotes", "unverified"),
    ("F04", "California tax on Treasury interest", "Not modelled. Parked cash may be taxed more or less than modelled.", "CPA", "open"),
    ("F05", "California conformity with the federal home-sale exclusion", "Not modelled. Path F is conservative until confirmed.", "CPA", "open"),
    ("F06", "CA 12.3% top rate (ftb_rates)", "Reused from the cbe register; not re-opened in this session.", "Re-open the FTB 2025 schedule", "reused"),
    ("F07", "37% federal top rate and the 2027 thresholds (irs_ir2026_133)", "Reused from the cbe register; not re-opened in this session.", "Re-open IR-2026-133", "reused"),
    ("F08", "Trustee's 60-day notice to beneficiaries (Probate Code 16061.7)", "Reported by the cbe desk; not on this desk's timeline, and not re-opened here.", "Re-open the statute", "reused"),
    ("F09", "Property tax installment dates of 10 December and 10 April", "Reported by the cbe desk from a county page; not re-opened here, and county-specific for Property A.", "Re-open the county page", "reused"),
    ("F10", "Crash paths are stylised", "They use the official peak-to-trough figures, not the daily record. The 1929 figure is a price index.", "Accepted as a limitation", "limitation"),
    ("F11", "Post-trough growth equals the net portfolio return", "Assumption. A faster or slower recovery changes the answer.", "Test in what-if", "assumption"),
    ("F12", "Sale year five years after transfer (paths F and G)", "Assumption, tested on the paths page only at one sale year.", "Suggestion S08", "assumption"),
    ("F13", "Equity net return of 6.4% (7.0% less a 0.6% tax drag)", "Taken from the cbe model. No official forecast exists.", "Accepted as an assumption", "assumption"),
    ("F14", "Prop 19 allowance indexation at 2% a year", "Assumption from the cbe model. Official allowance is $1,044,586 for 2025-2027 (cbe source, not re-opened).", "Re-open BOE LTA 2025/009", "reused"),
    ("F15", "Depreciation over 27.5 years", "Assumption carried from cbe; no official source was re-read here.", "Re-open IRS Publication 527", "assumption"),
    ("F16", "Earlier commits contain unrounded figures", "Repository privacy issue on shared history, recorded as cbe flag F19. No history rewrite has been made.", "OWNER DECISION (suggestion S10)", "owner decision"),
]


def page_flagged():
    def fsrc(fid):
        v = FLAG_SRC[fid]
        if v == "__ftb_rates__":
            return src_cell("ftb_rates", "FTB 2025 rate schedules (reused)")
        if v == "__irs_ir2026_133__":
            return src_cell("irs_ir2026_133", "IRS IR-2026-133 (reused)")
        if v == "__fed__":
            return L("fed_1929", "Fed History 1929") + "; " + L("fed_2008", "Fed History 2008")
        return '<span class="nosrc">%s</span>' % v
    rows = [[td(a, "c"), td(b), td(c), td(d), td(e, "flag"), td(fsrc(a), "src")] for a, b, c, d, e in FLAGS]
    body = """
<h1>Flagged for review</h1>
<p class="sub">Every unverified item, every reused source, and every open issue on this desk. The flags are
published so the owner can review them after the site is live and ask for changes.</p>
%s
""" % table(["ID", "Item", "What is wrong or missing", "How to close it", "Status", "Source"], rows)
    return page("flagged.html", "Flagged for review", "flagged", body)


def page_method():
    rows = [
        [td("Base year"), td("2026, from the cbe model"), td(src_cell(None, "No official source: internal owner-brief model (cbe/_src/model.py)"), "src")],
        [td("Transfer year"), td("2045 (midpoint of 2040 to 2050); 2040 and 2050 shown"), td(src_cell(None, "No official source: assumption, tested on this desk"), "src")],
        [td("Horizon"), td("2076, the owner's planning horizon (cbe)"), td(src_cell(None, "No official source: internal owner-brief model (cbe/_src/model.py)"), "src")],
        [td("Discount rate"), td("5.0%, as cbe"), td(src_cell(None, "No official source: internal owner-brief model (cbe/_src/model.py)"), "src")],
        [td("Equity net return"), td(pct(dm.EQ_NET) + " = 7.0% gross less 0.6% tax drag"), td(src_cell(None, "No official source: internal owner-brief model (cbe/_src/model.py)"), "src")],
        [td("Parked cash, pre-tax"), td(pct(dm.TREASURY_3M) + " (3-month bill, 13 Nov 2026)"), td(src_cell("tsy_curve"), "src")],
        [td("Parked cash, after tax"), td(pct(dm.CASH_NET) + " = 4.32% x (1 - 37% - 3.8%)"), td(src_cell("irs_701") + "; " + src_cell("irs_niit") + "; " + src_cell("irs_ir2026_133"), "src")],
        [td("Capital gains rate on a sale"), td("37.1% = 20% + 3.8% + 12.3% + 1%"), td(src_cell("irs_409") + "; " + src_cell("irs_niit") + "; " + src_cell("rtc_17043"), "src")],
        [td("Recapture rate"), td("42.1% = 25% + 3.8% + 12.3% + 1%"), td(src_cell("irs_409"), "src")],
        [td("Home-sale exclusion"), td("$250,000 single; $500,000 joint"), td(src_cell("irs_701"), "src")],
        [td("2008 crash"), td("57%% fall over 17 months, from entry"), td(src_cell("fed_2008"), "src")],
        [td("1929 crash"), td("89%% fall over 34 months, from entry"), td(src_cell("fed_1929"), "src")],
        [td("Rounding"), td("Every money figure to the nearest $10, from the model's own results"), td(src_cell(None, "No official source: a presentation rule of this desk"), "src")],
    ]
    body = """
<h1>Method and assumptions</h1>
<p class="sub">Every input, its label, and where it comes from. An input that is not verified is labelled as an
assumption and tested on this desk. Nothing is filled in from memory.</p>
%s
<h2>What the model does not do</h2>
<ul>
<li>It does not estimate the probability of a crash, a recovery, or any future rate.</li>
<li>It does not model state tax on Treasury interest, or California conformity with the home-sale exclusion.</li>
<li>It does not model the trust's own income tax, or the estate's tax position beyond the filing threshold.</li>
<li>It uses the cbe model's property numbers unchanged. Those are owner records, rounded, and unverified (flag F01).</li>
</ul>
""" % table(["Input", "Value used", "Source"], rows)
    return page("method.html", "Method", "method", body)


PAGES = [
    ("index.html", page_index),
    ("paths.html", page_paths),
    ("phased.html", page_phased),
    ("timeline.html", page_timeline),
    ("brief.html", page_brief),
    ("questions.html", page_questions),
    ("glossary.html", page_glossary),
    ("suggestions.html", page_suggestions),
    ("sources.html", page_sources),
    ("flagged.html", page_flagged),
    ("method.html", page_method),
]


def main():
    for name, fn in PAGES:
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(fn())
    print("wrote %d pages to cbd/" % len(PAGES))
    rc = subprocess.call([sys.executable, os.path.join(HERE, "verify.py")])
    if rc:
        raise SystemExit(rc)


if __name__ == "__main__":
    main()
