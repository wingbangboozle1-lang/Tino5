# -*- coding: utf-8 -*-
"""
Model layer for the phase-99220 desk (session arena-99220bc7).

This module does NOT re-implement the inheritance model. It imports the owner-brief model
published in cbe/_src (session arena-cbe837cb) read-only and adds four things the brief asks
for that the cbe desk does not compute:

  1. what-if grid      - the three pure options across transfer year, reinvestment return and
                         price growth, so the page can switch between them without a server;
  2. reinvestment test - the sell option re-run with the proceeds earning a stated rate;
  3. mixed paths       - live k years then sell; rent k years then sell; sell then park in
                         Treasuries 24-36 months then phase into equities (cash basis);
  4. historical replay - the phased-entry path replayed against the official 1929 and 2008
                         equity drawdowns (monthly, endpoints from Federal Reserve History).

Every money figure leaves this module through r10() (nearest $10).
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CBE = os.path.join(ROOT, "cbe", "_src")
if CBE not in sys.path:
    sys.path.insert(0, CBE)

import model as M  # noqa: E402  (cbe owner-brief model, read-only)

r10 = M.r10
A = M.ASSUMPTIONS
DRAG = A["portfolio_tax_drag"]
SELL = A["selling_cost"]

# ---- official inputs for this desk (each one also in sources.py of this desk) ----------------
# U.S. Treasury daily par yield curve, 13 Nov 2026 (home.treasury.gov). Percent.
TREASURY_2026_11_13 = dict(date="2026-11-13", m3=4.32, y2=4.88)
# Federal Reserve History: Dow 381.17 on 3 Sep 1929; 41.22 on 8 Jul 1932 (-89%); prior high
# regained 23 Nov 1954. Months from peak to trough: Sep 1929 -> Jul 1932 = 34; trough -> prior
# high Jul 1932 -> Nov 1954 = 268 (both counted in whole months from the dates printed there).
CRASH_1929 = dict(name="1929 crash (Dow Jones Industrial Average)", drop=0.89,
                  months_down=34, months_up=268)
# Federal Reserve History: S&P 500 fell 57% from Oct 2007 peak to Mar 2009 trough (17 months).
# Recovery period is NOT stated in the official essay; 48 months is a flagged assumption.
CRASH_2008 = dict(name="2008 crash (S&P 500)", drop=0.57, months_down=17, months_up=48,
                  recovery_is_assumption=True)

NET_GROWTH = A["portfolio_return"] - DRAG   # 6.4% a year, the cbe model's own net return


def money(x):
    return M.money(x)


# --------------------------------------------------------------------------- headline
def headline(transfer_year=None):
    """Pure options at the transfer year, both bases, from the cbe model."""
    res = M.compare(transfer_year=transfer_year)
    return dict(
        transfer_year=res["transfer_year"],
        value_at_transfer=r10(res["value_at_transfer"]),
        proceeds=r10(res["proceeds"]),
        years_after=res["years_after"],
        allowance=r10(res["allowance"]),
        fbyv=r10(res["fbyv"]),
        occupy_econ=r10(res["npv_occupy_econ"]), rent_econ=r10(res["npv_rent_econ"]),
        sell_econ=r10(res["npv_sell_econ"]),
        occupy_cash=r10(res["npv_occupy_cash"]), rent_cash=r10(res["npv_rent_cash"]),
        sell_cash=r10(res["npv_sell_cash"]),
    )


def breakevens():
    """Each break-even is the value of one input at which keep and sell are equal."""
    return dict(
        gross_yield=M.breakeven_gross_yield(),
        portfolio_return=M.breakeven_portfolio_return(),   # input before the 0.6% drag
        price_growth=M.breakeven_price_growth(),
    )


def reinvestment(transfer_year=None, yields=None):
    """Sell option re-run with the proceeds earning each stated yield (gross, cbe drag applied)."""
    yields = yields or [0.025, TREASURY_2026_11_13["m3"] / 100, TREASURY_2026_11_13["y2"] / 100]
    base = M.compare(transfer_year=transfer_year)
    out = []
    for y in yields:
        s = M.compare(transfer_year=transfer_year, portfolio_return=y)
        out.append(dict(yield_=y, sell_econ=r10(s["npv_sell_econ"]),
                        vs_occupy=r10(s["npv_sell_econ"] - base["npv_occupy_econ"]),
                        vs_rent=r10(s["npv_sell_econ"] - base["npv_rent_econ"])))
    return out


def what_if_grid():
    """All combinations used by the what-if page. Economic basis; $10 rounded."""
    rows = []
    for ty in (2040, 2045, 2050):
        for pr in (0.0432, 0.0488, 0.06, 0.07):
            for pg in (0.03, 0.04, 0.05):
                r = M.compare(transfer_year=ty, portfolio_return=pr, price_growth=pg)
                opts = dict(occupy=r["npv_occupy_econ"], rent=r["npv_rent_econ"],
                            sell=r["npv_sell_econ"])
                best = max(opts, key=opts.get)
                rows.append(dict(ty=ty, pr=pr, pg=pg, occupy=r10(opts["occupy"]),
                                 rent=r10(opts["rent"]), sell=r10(opts["sell"]), best=best,
                                 gap=r10(opts["sell"] - opts["occupy"])))
    return rows


# --------------------------------------------------------------------------- mixed paths
def _pv(x, k, d):
    return x / (1.0 + d) ** k


def mixed_paths(transfer_year=None, park_months=36, phase_months=12, cash_yield=None):
    """
    Cash-basis present values at the transfer year. Same inputs as cbe compare().

      live_k_sell   live in the house k years (cbe occupy rows), then sell at the year-k value
      rent_k_sell   let the house k years (cbe rent rows), then sell at the year-k value
      park_phase    sell at transfer, park the proceeds in Treasuries for park_months, then buy
                    equal monthly tranches over phase_months. No market crash is applied here;
                    the historical replay is on its own page.
    """
    d = A["discount_rate"]
    cash_yield = (TREASURY_2026_11_13["m3"] / 100) if cash_yield is None else cash_yield
    base = M.compare(transfer_year=transfer_year)
    ty = base["transfer_year"]
    Y = base["years_after"]
    market = base["market"]
    b0 = A["base_year"]
    out = {}

    out["keep_occupy"] = base["npv_occupy_cash"]
    out["keep_rent"] = base["npv_rent_cash"]
    out["sell_now"] = base["npv_sell_cash"]

    def live_then_sell(k):
        pv = 0.0
        for row in base["occ_rows"][:k]:
            pv += row["cash"] / (1.0 + d) ** (row["year"] - ty)
        v = market[ty + k - b0]
        proceeds = v * (1.0 - SELL)
        pv += proceeds * (1.0 + NET_GROWTH) ** (Y - k) / (1.0 + d) ** Y
        return pv

    def rent_then_sell(k):
        pv = 0.0
        for row in base["rent_rows"][:k]:
            pv += row["cash"] / (1.0 + d) ** (row["year"] - ty)
        v = market[ty + k - b0]
        proceeds = v * (1.0 - SELL)
        pv += proceeds * (1.0 + NET_GROWTH) ** (Y - k) / (1.0 + d) ** Y
        return pv

    for k in (5, 10):
        out["live_%d_sell" % k] = live_then_sell(k)
        out["rent_%d_sell" % k] = rent_then_sell(k)

    # park then phase: monthly, cash yield on the parked money, net growth once invested
    proceeds = base["proceeds"]
    g_m = (1.0 + NET_GROWTH) ** (1 / 12.0) - 1.0
    c_m = (1.0 + cash_yield) ** (1 / 12.0) - 1.0
    cash = proceeds
    shares_val = 0.0          # value of the invested part, at the growth path
    n_total = Y * 12
    invested_tranche = cash / phase_months
    for m in range(1, n_total + 1):
        if m <= park_months:
            cash *= (1.0 + c_m)
        else:
            cash *= (1.0 + c_m) if cash > 0 else 1.0
            if m <= park_months + phase_months:
                shares_val += invested_tranche
                cash -= invested_tranche
        shares_val *= (1.0 + g_m)
    terminal = shares_val + cash
    out["park_%d_phase_%d" % (park_months, phase_months)] = terminal / (1.0 + d) ** Y
    return dict(values=out, transfer_year=ty, years_after=Y, proceeds=proceeds,
                cash_yield=cash_yield, park_months=park_months, phase_months=phase_months)


# --------------------------------------------------------------------- historical replay
def index_path(crash, months, growth_after=NET_GROWTH):
    """Index value by month from the peak (1.0 at month 0). Linear down, linear back, then growth."""
    down, up, trough = crash["months_down"], crash["months_up"], 1.0 - crash["drop"]
    out = []
    for t in range(months + 1):
        if t <= down:
            v = 1.0 - crash["drop"] * (t / down)
        elif t <= down + up:
            v = trough + (1.0 - trough) * ((t - down) / up)
        else:
            v = 1.0 * (1.0 + growth_after) ** ((t - down - up) / 12.0)
        out.append(v)
    return out


def replay(crash=None, cash_yield=None, park_months=24, phase_months=12, horizon_years=25,
           invested=None):
    """
    Monthly replay. Lump sum buys at the peak (month 0). Phased strategies park the proceeds in
    Treasuries for park_months, then buy in equal monthly tranches over phase_months.
    Returns the value at 10 years and at horizon_years, the lowest value reached, and the
    no-crash equivalent for the same strategy.
    """
    crash = crash or CRASH_1929
    cash_yield = (TREASURY_2026_11_13["m3"] / 100) if cash_yield is None else cash_yield
    invested = invested or M.compare()["proceeds"]
    H = horizon_years * 12
    c_m = (1.0 + cash_yield) ** (1 / 12.0) - 1.0

    def run(path, park, phase):
        cash = invested
        shares = 0.0          # number of index units held
        tranche = invested / phase if phase else 0.0
        worst = None
        vals = {}
        for m in range(0, H + 1):
            p = path[m]
            if m > 0:
                cash *= (1.0 + c_m)
            if m >= park and m < park + phase and phase:
                buy = min(tranche, cash)
                shares += buy / p
                cash -= buy
            value = shares * p + cash
            if m == 0 or m > 0:
                worst = value if worst is None else min(worst, value)
            if m in (120, H):
                vals[m] = value
        return vals[120], vals[H], worst

    out = {}
    path_crash = index_path(crash, H)
    path_flat = [(1.0 + NET_GROWTH) ** (m / 12.0) for m in range(H + 1)]
    strategies = [("lump", 0, 1), ("park_24_phase_12", 24, 12), ("park_36_phase_12", 36, 12)]
    for name, park, phase in strategies:
        if park == 0:
            # lump sum: the whole amount is invested at the peak, no cash leg
            c10, cH, worst = _lump(path_crash, H, invested)
            n10, nH, _ = _lump(path_flat, H, invested)
        else:
            c10, cH, worst = run(path_crash, park, phase)
            n10, nH, _ = run(path_flat, park, phase)
        out[name] = dict(crash_10y=r10(c10), crash_h=r10(cH), lowest=r10(worst),
                         nocrash_10y=r10(n10), nocrash_h=r10(nH))
    return dict(crash=crash, cash_yield=cash_yield, horizon_years=horizon_years,
                invested=r10(invested), results=out)


def _lump(path, H, invested):
    shares = invested / path[0]
    vals = [shares * p for p in path]
    return vals[120], vals[H], min(vals)


# -------------------------------------------------------------------------------- export
def snapshot():
    h = headline()
    h45 = headline(2045)
    return dict(headline=h, breakevens=breakevens(),
                reinvest=reinvestment(), mixed=mixed_paths(),
                replay_1929=replay(CRASH_1929), replay_2008=replay(CRASH_2008),
                replay_2008_no_recovery_assumption=None)


if __name__ == "__main__":
    import pprint
    pprint.pprint(snapshot(), width=110)
