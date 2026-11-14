# -*- coding: utf-8 -*-
"""
Mixed-path and phased-entry model for the cbd/ desk (session arena-cbd1473c).

Reuses, read-only, the owner-brief model in cbe/_src/model.py (session arena-cbe837cb) for
every property number: value path, assessed-value path, Proposition 19 allowance, running
costs, rents and the effective tax rate. Nothing under cbe/ is edited.

Every input is labelled in exactly one of these ways, and the label is shown on the
methodology page:

  verified   read from an official page this session (see sources.py)
  owner      supplied by the owner, or taken from the cbe owner record (rounded to $10)
  derived    arithmetic on verified and owner inputs
  assumption chosen here; tested in the sensitivity tables, never presented as fact

Money is rounded to the nearest $10 before it reaches a page (r10 / money).
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CBE_SRC = os.path.join(ROOT, "cbe", "_src")
if CBE_SRC not in sys.path:
    sys.path.insert(0, CBE_SRC)

import model as cm  # noqa: E402  (read-only import of the cbe owner-brief model)

r10 = cm.r10
money = cm.money
pct = cm.pct

# ------------------------------------------------------------------ verified rates

TREASURY_3M = 0.0432      # verified: Treasury par yield curve, 3 Mo, 13 Nov 2026
TREASURY_2Y = 0.0488      # verified: Treasury par yield curve, 2 Yr, 13 Nov 2026
FED_TOP_RATE = 0.37       # verified: IRS IR-2026-133, top income rate 37 percent
NIIT = 0.038              # verified: IRS, net investment income tax 3.8 percent (cbe source)
LTCG_TOP = 0.20           # verified: IRS Topic 409, top long-term capital gain rate
RECAPTURE = 0.25          # verified: IRS Topic 409, unrecaptured section 1250 gain
CA_TOP = 0.123            # verified: FTB 2025 rate schedule, top rate 12.3 percent (cbe source)
CA_MHS = 0.01             # verified: R&TC 17043, 1 percent over $1,000,000 (cbe source)
S121_SINGLE = 250_000     # verified: IRS Topic 701, home-sale exclusion, single filer
S121_JOINT = 500_000      # verified: IRS Topic 701, home-sale exclusion, joint return
CRASH_2008 = 0.57         # verified: Federal Reserve History, S&P 500 down 57 percent
CRASH_1929 = 0.89         # verified: Federal Reserve History, Dow down 89 percent

# Months between the official peak and trough dates (derived from the verified dates)
MONTHS_2008 = 17          # Oct 2007 peak to Mar 2009 trough
MONTHS_1929 = 34          # 3 Sep 1929 peak to 8 Jul 1932 trough

# ------------------------------------------------------------------ assumptions

A = cm.ASSUMPTIONS
EQ_NET = A["portfolio_return"] - A["portfolio_tax_drag"]     # 7.0% less 0.6% drag (cbe)
DISC = A["discount_rate"]                                    # 5.0% (cbe)
CGT_TOTAL_LTCG = LTCG_TOP + NIIT + CA_TOP + CA_MHS           # derived, 37.1%
CGT_TOTAL_RECAP = RECAPTURE + NIIT + CA_TOP + CA_MHS         # derived, 42.1%
# Interest on Treasuries is taxed federally at the top rate plus the 3.8% surcharge.
# State tax on Treasury interest is NOT modelled and is flagged for the CPA.
CASH_NET = TREASURY_3M * (1.0 - FED_TOP_RATE - NIIT)         # derived, after-tax parking yield
SALE_YEAR_OFFSET = 5      # assumption: mixed paths live or let for five years, then sell
HORIZON = A["horizon"]    # 2076 (cbe)
BASE_YEAR = A["base_year"]


# ------------------------------------------------------------------ equity and cash paths

def _g_month(annual):
    return (1.0 + annual) ** (1.0 / 12.0) - 1.0


def equity_index(t, equity_net=EQ_NET, crash=None):
    """
    Index level after t months, starting at 1.0 on the entry date.

    crash = (level, months): the index reaches `level` (1.0 = the entry level) at `months`.
    Growth at equity_net runs throughout; the crash is layered on top of it, so the path is
    continuous in `level` and equals the pure growth path when level = (1+g)^months.
    After the trough the index grows at equity_net from `level`. The decline is stylised,
    not a daily price path. A fall of D from the entry level is level = 1 - D.
    """
    gm = _g_month(equity_net)
    if crash is None:
        return (1.0 + gm) ** t
    level, c = crash
    if t <= c:
        return (1.0 + gm) ** t * (level / (1.0 + gm) ** c) ** (t / float(c))
    return level * (1.0 + gm) ** (t - c)


def simulate(deploy_months, months, equity_net=EQ_NET, crash=None, cash_net=CASH_NET,
             cash_shock=0.0, shock_month=12):
    """
    Monthly simulation of one dollar of proceeds.

    deploy_months = N : equal tranches of 1/N bought at months 0..N-1 (N = 1 is a lump sum)
    deploy_months = 0 : nothing is bought; the whole amount sits in cash (reference only)

    Cash earns cash_net a year after tax. From shock_month the cash rate is lower by
    cash_shock (reinvestment risk: the 3-month bill is rolled at a lower rate).
    Returns W[0..months], total value in dollars per dollar of proceeds.
    """
    cash = 1.0
    shares = 0.0
    out = [1.0]
    for t in range(months):
        if deploy_months and t < deploy_months:
            amt = 1.0 / deploy_months
            buy = min(amt, cash)
            cash -= buy
            shares += buy / equity_index(t, equity_net, crash)
        annual = cash_net - (cash_shock if t >= shock_month else 0.0)
        cash *= (1.0 + _g_month(annual))
        out.append(cash + shares * equity_index(t + 1, equity_net, crash))
    return out


def phased_value(n_months, years, equity_net=EQ_NET, crash=None, cash_net=CASH_NET,
                 cash_shock=0.0):
    """Terminal value per dollar after `years` for a phase-in of n_months."""
    return simulate(n_months, int(round(years * 12)), equity_net, crash, cash_net,
                    cash_shock)[-1]


# ------------------------------------------------------------------ crash scenarios

SCENARIOS = [
    ("base", "No crash: the portfolio compounds at the net return", None),
    ("crash2008", "2008-style: S&P 500 falls 57% over 17 months from entry",
     (1.0 - CRASH_2008, MONTHS_2008)),
    ("crash1929", "1929-style: Dow falls 89% over 34 months from entry",
     (1.0 - CRASH_1929, MONTHS_1929)),
]


def breakeven_trough(n_months, years=10.0, cash_net=CASH_NET, months=MONTHS_2008,
                     cash_shock=0.0):
    """
    Trough level (1.0 = entry level, reached at `months`) at which a phase-in of n_months
    ends level with a lump sum after `years`. Returns (level, fall_from_entry) or None.
    A lower level means a deeper crash; levels above the level reached without a crash
    favour the lump sum.
    """
    def diff(level):
        crash = (level, months)
        return (phased_value(n_months, years, EQ_NET, crash, cash_net, cash_shock)
                - phased_value(1, years, EQ_NET, crash, cash_net, cash_shock))
    lo, hi = 0.05, 1.5
    flo, fhi = diff(lo), diff(hi)
    if flo * fhi > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2.0
        fm = diff(mid)
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    level = (lo + hi) / 2.0
    return level, 1.0 - level


# ------------------------------------------------------------------ mixed paths

def _pv(x, years):
    return x / (1.0 + DISC) ** years


def _sale_tax(gain, recapture_part=0.0, exclusion=0.0):
    """Tax on a realised gain. recapture_part is the unrecaptured section 1250 gain."""
    taxable = max(0.0, gain - exclusion)
    rec = min(max(0.0, recapture_part), taxable)
    return rec * CGT_TOTAL_RECAP + (taxable - rec) * CGT_TOTAL_LTCG


PATHS = [
    ("A", "Live in it, hold it", False),
    ("B", "Let it out, hold it", False),
    ("C", "Sell at transfer, invest as one lump sum", True),
    ("D", "Sell at transfer, phase in over 24 months", True),
    ("E", "Sell at transfer, phase in over 36 months", True),
    ("F", "Live in it 5 years, then sell and phase in over 36 months", True),
    ("G", "Let it out 5 years, then sell and phase in over 24 months", True),
]


def paths_for_transfer(transfer_year, crash=None, joint=False, eq=None, cash=None):
    """
    The seven paths for one transfer year, each a present value in the transfer year
    (cash basis, the same basis as cbe/options.html). Returns dict path_id -> dict.

    A  occupy, held                  cbe value; not an equity exposure
    B  let, held                     cbe value; not an equity exposure
    C  sell at transfer, lump sum    cbe proceeds invested at the net portfolio return
    D  sell at transfer, 24 months   cbe proceeds phased in over 24 monthly tranches
    E  sell at transfer, 36 months   cbe proceeds phased in over 36 monthly tranches
    F  live k years, then sell       occupy cash flows, home-sale exclusion, 36-month phase-in
    G  let k years, then sell        rent cash flows, recapture, 24-month phase-in
    k = SALE_YEAR_OFFSET (assumption, 5 years).
    """
    r = cm.compare(transfer_year=transfer_year)
    market = r["market"]
    ty = transfer_year
    years_after = HORIZON - ty
    proceeds = r["proceeds"]
    excl = S121_JOINT if joint else S121_SINGLE
    k = SALE_YEAR_OFFSET
    sale_year = ty + k
    v_sale = market[sale_year - BASE_YEAR]
    v_transfer = market[ty - BASE_YEAR]

    eq_r = EQ_NET if eq is None else eq
    cash_r = CASH_NET if cash is None else cash

    def tail(p0, n_months, from_years):
        """Value at HORIZON of p0 invested at `from_years` after transfer, in phases."""
        yrs_left = HORIZON - (ty + from_years)
        return p0 * phased_value(n_months, yrs_left, eq_r, crash, cash_r)

    out = {}
    out["A"] = dict(pv=r["npv_occupy_cash"], equity=False)
    out["B"] = dict(pv=r["npv_rent_cash"], equity=False)
    out["C"] = dict(pv=_pv(tail(proceeds, 1, 0), years_after), equity=True)
    out["D"] = dict(pv=_pv(tail(proceeds, 24, 0), years_after), equity=True)
    out["E"] = dict(pv=_pv(tail(proceeds, 36, 0), years_after), equity=True)

    occ = r["occ_rows"][:k]
    flows_f = sum(row["cash"] / (1.0 + DISC) ** (j + 1) for j, row in enumerate(occ))
    net_sale = v_sale * (1.0 - A["selling_cost"])
    gain_f = net_sale - v_transfer
    tax_f = _sale_tax(gain_f, 0.0, excl)
    out["F"] = dict(pv=flows_f + _pv(tail(net_sale - tax_f, 36, k), years_after),
                    equity=True, sale_tax=tax_f, sale_gain=gain_f, sale_year=sale_year)

    rent = r["rent_rows"][:k]
    flows_g = sum(row["cash"] / (1.0 + DISC) ** (j + 1) for j, row in enumerate(rent))
    accum_dep = r["annual_dep"] * k
    gain_g = net_sale - (v_transfer - accum_dep)
    recap = min(accum_dep, max(0.0, gain_g))
    tax_g = _sale_tax(gain_g, recap, 0.0)
    out["G"] = dict(pv=flows_g + _pv(tail(net_sale - tax_g, 24, k), years_after),
                    equity=True, sale_tax=tax_g, sale_gain=gain_g, sale_year=sale_year,
                    accum_dep=accum_dep)
    out["_meta"] = dict(transfer_year=ty, proceeds=proceeds, value_transfer=v_transfer,
                        value_sale=v_sale, sale_year=sale_year, years_after=years_after,
                        allowance=r["allowance"], rate_a=r["rate_a"], joint=joint)
    return out


def stressed_table(transfer_year, joint=False, eq=None, cash=None):
    """Every path under the three scenarios. Paths A and B are identical across them."""
    return {sid: paths_for_transfer(transfer_year, crash=crash, joint=joint, eq=eq, cash=cash)
            for sid, _, crash in SCENARIOS}


if __name__ == "__main__":
    t = paths_for_transfer(2045)
    for p, _, _ in PATHS:
        print(p, money(t[p]["pv"]))
    print(t["_meta"])
    print("CASH_NET", CASH_NET, "EQ_NET", EQ_NET)
    print("breakeven 24m:", breakeven_trough(24), " 36m:", breakeven_trough(36))
