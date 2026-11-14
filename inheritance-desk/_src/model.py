"""Decision model for the inherited-property decision (Property A) and the owned property (Property B).

Every constant is tagged with its basis:
  V  = verified against an official source (see sources.json)
  P  = partially verified (official page reached, figure from a secondary report, flagged)
  O  = owner-supplied, not verifiable from a public source (flagged as unverified)
  A  = model assumption (no source; labelled, and varied on the what-if page)

Money is computed at full precision; the site rounds to the nearest $10 (statutory amounts are
printed exactly as published and marked).

Run:  python3 inheritance-desk/_src/model.py   -> writes inheritance-desk/data/model.json
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"

# ------------------------------------------------------------------ V: sourced constants
FED_EXCLUSION_2026 = 15_000_000        # V  IRS Rev. Proc. 2025-32 s.2.14 (basic exclusion, 2026); IRS estate-tax page
GIFT_ANNUAL_EXCL_2026 = 19_000         # V  IRS Rev. Proc. 2025-32 s.4.42(1)
PROP19_CAP_2025_27 = 1_044_586         # V  BOE Letter to Assessors 2025/009 (Feb 16 2025 - Feb 15 2027)
PROP13_MAX_GROWTH = 0.02               # V  Rev. & Tax. Code s.51(a)(1)(D): inflation factor capped at 2%
NIIT_RATE = 0.038                      # V  IRS Topic 559
NIIT_THRESH_SINGLE = 200_000           # V  IRS Topic 559 (not indexed)
SEC121_EXCL_SINGLE = 250_000           # V  IRS Topic 701 (single filer; $500,000 if married filing jointly)
CAP_GAINS_0_SINGLE = 49_450            # V  IRS Rev. Proc. 2025-32 s.4.03 (0% zero-rate amount, all other individuals, 2026)
CAP_GAINS_15_SINGLE = 545_500          # V  IRS Rev. Proc. 2025-32 s.4.03 (15% rate max, all other individuals, 2026)
CA_PROBATE_SMALL_EST = 208_850         # P  Probate Code 13100 / Judicial Council DE-300 (secondary; DE-300 not opened)
TREASURY_3M = 0.0432                   # V  Treasury daily par yield curve, 13 Nov 2026, 3 Mo
TREASURY_2Y = 0.0488                   # V  Treasury daily par yield curve, 13 Nov 2026, 2 Yr
FED_INFLATION_GOAL = 0.02              # V  Federal Reserve Statement on Longer-Run Goals (2025)
DOW_1929_DROP = 0.89                   # V  Federal Reserve History: 381.17 (3 Sep 1929) -> 41.22 (8 Jul 1932)
DOW_1929_MONTHS_TO_TROUGH = 34         # V  derived from the two dates above
DOW_1929_MONTHS_TO_RECOVER = 268       # V  trough (Jul 1932) -> Nov 23 1954 recovery
SP500_2008_DROP = 0.57                 # V  Federal Reserve History (S&P 500 -57%, Oct 2007 peak to Mar 2009 trough)
SP500_2008_MONTHS_TO_TROUGH = 17       # P  Oct 2007 -> Mar 2009 (secondary index table)
SP500_2008_MONTHS_TO_RECOVER = 48      # P  Mar 2009 -> Mar 2013 (secondary)
HOME_2008_DROP = 0.30                  # V  Federal Reserve History (home prices ~-30%, mid-2006 to mid-2009)
HOME_2008_MONTHS = 36                  # V  mid-2006 -> mid-2009

# ------------------------------------------------------------------ O: owner-supplied (rounded to $10)
OWNER = {
    "A_fmv_2026": 3_100_000,           # O  owner estimate, Nov 2026
    "A_fbyv_2026": 550_540,            # O  owner's 2026 assessed-value projection (+2%)
    "A_tax_2025": 7_210,               # O  owner table: 2025 property tax
    "A_av_2025": 539_740,              # O  owner table: 2025 assessed value
    "B_fmv_2026": 1_800_000,           # O  owner estimate, Nov 2026
    "B_tax_2025": 2_440,               # O  owner table: 2025 property tax
    "B_av_2025": 114_250,              # O  owner table: 2025 assessed value
    "B_rent_month": 7_150,             # O  rent from the two rented units
    "B_water_month": 370,              # O  owner range $330-$400, rounded to $10 (midpoint 365)
    "B_elec_month": 50,                # O  midpoint of $30-$70
    "insurance_year": 1_500,           # O  owner estimate (primary-residence policy); unverified
}

# ------------------------------------------------------------------ A: model assumptions
A = {
    "composite_tax_rate": 0.0120,      # A  county composite rate assumed; county text summarised as ~1.12%-1.24%
    "water_month": 130,                # A  owner range $100-$150 (Property A), rounded to $10 (midpoint 125)
    "solar_credit_month": 20,          # A  owner range $10-$20, rounded to $10 (midpoint 15)
    "insurance_extra_growth": 0.01,    # A  insurance grows at CPI + 1 point
    "maintenance_rate": 0.002,         # A  0.2% of value per year (no source)
    "rent_gross_yield": 0.040,         # A  gross rent / value per year (no source; replace with appraisal)
    "rent_vacancy_mgmt": 0.08,         # A  vacancy and management share of gross rent
    "sale_cost": 0.06,                 # A  selling costs share of price (no source)
    "gain_tax_rate": 0.281,            # A  15% federal + 3.8% NIIT + 9.3% CA (CA rate unverified; CPA to confirm)
    "park_rate": TREASURY_3M,          # V  3-month T-bill rate used for cash and parked proceeds
    "park_rate_low": 0.030,            # A  reinvestment-risk case
    "equity_base": 0.06,               # A  nominal equity return (planning assumption, no source)
    "equity_stag": 0.04,               # A
    "equity_low": 0.03,                # A
    "home_base": 0.02,                 # A  nominal home growth = Fed inflation goal (no real growth)
    "home_stag": 0.03,                 # A
    "home_low": 0.00,                  # A
    "infl_base": FED_INFLATION_GOAL,   # V anchor
    "infl_stag": 0.05,                 # A
    "infl_low": 0.01,                  # A
    "cap_growth": 0.02,                # A  $1,044,586 cap indexed at 2%/yr (BOE indexes it every two years)
}

START_YEAR = 2026
END_YEAR = 2076                        # 50-year horizon (owner's brief)
TRANSFER_YEARS = [2040, 2045, 2050]


class Regime:
    def __init__(self, name, label, equity_mu, home_g, inflation, crash=None):
        self.name, self.label = name, label
        self.equity_mu, self.home_g, self.inflation = equity_mu, home_g, inflation
        self.crash = crash

    def equity_index(self, m):
        """Equity index m months after transfer (1.0 at transfer)."""
        c = self.crash
        if c is None:
            return (1 + self.equity_mu) ** (m / 12)
        L, n1, n2 = c["trough"], c["n1"], c["n2"]
        if m <= n1:
            return L ** (m / n1)
        if m <= n2:
            return L * (1 / L) ** ((m - n1) / (n2 - n1))
        return (1 + self.equity_mu) ** ((m - n2) / 12)

    def home_index(self, m):
        c = self.crash
        if c is None:
            return (1 + self.home_g) ** (m / 12)
        Lh, nh = c["home_trough"], c["home_months"]
        if m <= nh:
            return Lh ** (m / nh)
        return Lh * (1 + self.home_g) ** ((m - nh) / 12)

    def cpi(self, months_from_2026):
        return (1 + self.inflation) ** (months_from_2026 / 12)


CRASH_2008 = {"trough": 1 - SP500_2008_DROP, "n1": SP500_2008_MONTHS_TO_TROUGH,
              "n2": SP500_2008_MONTHS_TO_TROUGH + SP500_2008_MONTHS_TO_RECOVER,
              "home_trough": 1 - HOME_2008_DROP, "home_months": HOME_2008_MONTHS}
# housing path for the 1929 analogue is NOT sourced; the 2008 housing path is used as a flagged proxy
CRASH_1929 = {"trough": 1 - DOW_1929_DROP, "n1": DOW_1929_MONTHS_TO_TROUGH,
              "n2": DOW_1929_MONTHS_TO_TROUGH + DOW_1929_MONTHS_TO_RECOVER,
              "home_trough": 1 - HOME_2008_DROP, "home_months": HOME_2008_MONTHS}

REGIMES = [
    Regime("base", "Base: 2% inflation, 6% stocks, homes +2% a year", A["equity_base"], A["home_base"], A["infl_base"]),
    Regime("stagflation", "Stagflation: 5% inflation, 4% stocks, homes +3% a year", A["equity_stag"], A["home_stag"], A["infl_stag"]),
    Regime("low_growth", "Low growth: 1% inflation, 3% stocks, flat homes", A["equity_low"], A["home_low"], A["infl_low"]),
    Regime("crash_2008", "2008-style crash right after transfer (stocks -57%, homes -30%)", A["equity_base"], A["home_base"], A["infl_base"], CRASH_2008),
    Regime("crash_1929", "1929-style crash right after transfer (stocks -89%, about 22 years to recover)", A["equity_base"], A["home_base"], A["infl_base"], CRASH_1929),
]

OPTIONS = [
    # key, kwargs, label, short label
    ("live", {"avoid_rent": True}, "A. Live in it (move in within 1 year; Prop 19 applies; counts the rent you do not pay)", "Live in it"),
    ("live", {"avoid_rent": False}, "A0. Live in it, cash only (no credit for rent avoided)", "Live, cash only"),
    ("rent", {}, "B. Rent it out (no move-in; full reassessment)", "Rent it out"),
    ("sell_lump", {}, "C. Sell at transfer; invest all at once", "Sell, invest at once"),
    ("sell_phased", {"park_months": 24}, "D. Sell; park 24 months in T-bills; then phase into stocks over 12 months", "Sell, park 24m then phase"),
    ("sell_phased", {"park_months": 36}, "E. Sell; park 36 months in T-bills; then phase into stocks over 12 months", "Sell, park 36m then phase"),
    ("mixed_live_rent", {"avoid_rent": True}, "F. Mixed: live 1 year (keeps Prop 19), then rent it out", "Live 1 yr, then rent"),
    ("mixed_live_sell", {"live_years": 10, "avoid_rent": True}, "G. Mixed: live 10 years, then sell and invest at once", "Live 10 yrs, then sell"),
]


def simulate(option, T, regime, *, park_months=24, live_years=10, rent_yield=None, tax_rate=None,
             park_rate=None, fmv=None, fbyv=None, detail=False, avoid_rent=True, credit_yield=None):
    """Monthly simulation from transfer (Jan of year T) to the end of END_YEAR. Returns 2026-dollar wealth."""
    fmv = OWNER["A_fmv_2026"] if fmv is None else fmv
    fbyv = OWNER["A_fbyv_2026"] if fbyv is None else fbyv
    tax_rate = A["composite_tax_rate"] if tax_rate is None else tax_rate
    rent_yield = A["rent_gross_yield"] if rent_yield is None else rent_yield
    park_rate = A["park_rate"] if park_rate is None else park_rate

    m0 = (T - START_YEAR) * 12                       # months from 2026-01 to transfer
    horizon = (END_YEAR - T + 1) * 12
    # value at transfer (pre-crash) and the Prop 13 base at transfer
    H_T = fmv * (1 + regime.home_g) ** (m0 / 12)
    fbyv_T = fbyv * (1 + PROP13_MAX_GROWTH) ** (T - START_YEAR)
    cap_T = PROP19_CAP_2025_27 * (1 + A["cap_growth"]) ** (T - 2025)
    prop19 = option in ("live", "mixed_live_rent", "mixed_live_sell")
    av_base_T = max(fbyv_T, H_T - cap_T) if prop19 else H_T

    hold = int(live_years * 12) if option == "mixed_live_sell" else (12 if option == "mixed_live_rent" else None)
    sells_at_start = option in ("sell_lump", "sell_phased")

    cash = 0.0
    units = 0.0
    park = 0.0
    phase = None
    rows = []
    for m in range(horizon):
        t_abs = m0 + m
        cpi = regime.cpi(t_abs)
        H_t = H_T * regime.home_index(m)
        taxable = min(av_base_T * (1 + PROP13_MAX_GROWTH) ** (m / 12), H_t)

        if option == "live":
            owned = "live"
        elif option == "rent":
            owned = "rent"
        elif option == "mixed_live_rent":
            owned = "live" if m < 12 else "rent"
        elif option == "mixed_live_sell":
            owned = "live" if m < hold else "none"
        else:
            owned = "none" if sells_at_start else "live"

        prop_tax = carry = rent_net = 0.0
        if owned in ("live", "rent"):
            prop_tax = taxable * tax_rate / 12
            water = A["water_month"] * cpi
            ins = OWNER["insurance_year"] / 12 * (1 + regime.inflation + A["insurance_extra_growth"]) ** (t_abs / 12)
            maint = A["maintenance_rate"] * H_t / 12
            solar = A["solar_credit_month"] * cpi
            carry = water + ins + maint - solar
            if owned == "rent":
                rent_net = rent_yield * H_t / 12 * (1 - A["rent_vacancy_mgmt"])
            elif avoid_rent:
                # owner-occupier: the rent the heir would otherwise pay elsewhere is a cash-equivalent benefit
                cy = rent_yield if credit_yield is None else credit_yield
                rent_net = cy * H_t / 12 * (1 - A["rent_vacancy_mgmt"])

        cash = cash * (1 + park_rate) ** (1 / 12) + rent_net - carry - prop_tax

        if park > 0:
            park *= (1 + park_rate) ** (1 / 12)

        sale_now = (m == 0 and sells_at_start) or (option == "mixed_live_sell" and m == hold)
        if sale_now:
            gross = H_t * (1 - A["sale_cost"])
            gain = max(0.0, gross - H_T)                                  # basis = FMV at death (IRS Pub 551)
            excl = SEC121_EXCL_SINGLE if option == "mixed_live_sell" else 0.0
            proceeds = gross - A["gain_tax_rate"] * max(0.0, gain - excl)
            if option == "sell_phased":
                park += proceeds
                phase = {"start": m + park_months, "months": 12, "amount": proceeds / 12}
            else:
                units += proceeds / regime.equity_index(m)

        if phase and phase["start"] <= m < phase["start"] + phase["months"]:
            amt = min(phase["amount"], park)
            park -= amt
            units += amt / regime.equity_index(m)

        if detail:
            rows.append({"m": m, "year": T + m // 12, "home": H_t, "taxable": taxable,
                         "prop_tax": prop_tax, "carry": carry, "rent_net": rent_net, "cpi": cpi})

    end = horizon - 1
    H_end = H_T * regime.home_index(end)
    financial = units * regime.equity_index(end) + park + cash
    if option in ("live", "rent", "mixed_live_rent"):
        gross = H_end * (1 - A["sale_cost"])
        gain = max(0.0, gross - H_T)
        excl = SEC121_EXCL_SINGLE if option == "live" else 0.0
        financial += gross - A["gain_tax_rate"] * max(0.0, gain - excl)
    end_cpi = regime.cpi((END_YEAR - START_YEAR + 1) * 12 - 1)
    out = {"option": option, "T": T, "regime": regime.name, "wealth": financial / end_cpi}
    if detail:
        out["rows"] = rows
        out["H_T"] = H_T
        out["av_base_T"] = av_base_T
    return out


def first_year(option, T, regime=REGIMES[0], **kw):
    """Year-one carrying figures after transfer, in 2026 dollars."""
    r = simulate(option, T, regime, detail=True, **kw)
    first = r["rows"][:12]
    base = regime.cpi((T - START_YEAR) * 12)
    return {
        "prop_tax": sum(x["prop_tax"] for x in first) / base,
        "carry": sum(x["carry"] for x in first) / base,
        "rent_net": sum(x["rent_net"] for x in first) / base,
        "taxable_value": first[0]["taxable"] / base,
        "home_value": r["H_T"] / base,
    }


def quick_annual(p):
    """Annual approximation used by the what-if page (the same formulas, no monthly compounding).

    p keys: fmv, fbyv, rate, water, insurance, maint_rate, solar, rent_yield, vacancy, growth, cap, T, move_in
    """
    dy = p["T"] - START_YEAR
    H_T = p["fmv"] * (1 + p["growth"]) ** dy
    fbyv_T = p["fbyv"] * (1 + PROP13_MAX_GROWTH) ** dy
    cap_T = p["cap"] * (1 + A["cap_growth"]) ** (p["T"] - 2025)
    av_live = max(fbyv_T, H_T - cap_T) if p["move_in"] else H_T
    tax_live = av_live * p["rate"]
    tax_rent = H_T * p["rate"]
    carry = p["water"] + p["insurance"] + p["maint_rate"] * H_T - p["solar"]
    rent_net = p["rent_yield"] * H_T * (1 - p["vacancy"])
    return {
        "home_value_at_transfer": H_T,
        "taxable_live": av_live,
        "taxable_rent": H_T,
        "tax_live": tax_live,
        "tax_rent": tax_rent,
        "carry": carry,
        "rent_net": rent_net,
        "net_live_year1": -(carry + tax_live),
        "net_rent_year1": rent_net - carry - tax_rent,
    }


def build():
    res = {"assumptions": A, "owner": OWNER, "options": [{"key": k, "kw": kw, "label": l, "short": s}
                                                          for k, kw, l, s in OPTIONS],
           "regimes": [{"name": r.name, "label": r.label} for r in REGIMES]}
    res["constants"] = {k: v for k, v in globals().items() if k.isupper() and isinstance(v, (int, float))}

    grid = []
    for T in TRANSFER_YEARS:
        for reg in REGIMES:
            for key, kw, label, short in OPTIONS:
                grid.append({"T": T, "regime": reg.name, "option": key, "kw": kw,
                             "wealth": simulate(key, T, reg, **kw)["wealth"]})
    res["grid"] = grid

    res["first_year"] = {str(T): {"live": first_year("live", T), "rent": first_year("rent", T)}
                         for T in TRANSFER_YEARS}

    # 2026-2050 trajectory, base regime (value, assessed value, property tax before and after transfer)
    traj = []
    for year in range(START_YEAR, 2051):
        H = OWNER["A_fmv_2026"] * (1 + A["home_base"]) ** (year - START_YEAR)
        av_pre = OWNER["A_fbyv_2026"] * (1 + PROP13_MAX_GROWTH) ** (year - START_YEAR)
        row = {"year": year, "home": H, "av_pre": av_pre, "tax_pre": av_pre * A["composite_tax_rate"]}
        for T in TRANSFER_YEARS:
            if year >= T:
                H_T = OWNER["A_fmv_2026"] * (1 + A["home_base"]) ** (T - START_YEAR)
                fbyv_T = OWNER["A_fbyv_2026"] * (1 + PROP13_MAX_GROWTH) ** (T - START_YEAR)
                cap_T = PROP19_CAP_2025_27 * (1 + A["cap_growth"]) ** (T - 2025)
                av_l = min(max(fbyv_T, H_T - cap_T) * (1 + PROP13_MAX_GROWTH) ** (year - T), H)
                av_r = min(H_T * (1 + PROP13_MAX_GROWTH) ** (year - T), H)
                row[f"av_live_{T}"] = av_l
                row[f"av_rent_{T}"] = av_r
                row[f"tax_live_{T}"] = av_l * A["composite_tax_rate"]
                row[f"tax_rent_{T}"] = av_r * A["composite_tax_rate"]
        traj.append(row)
    res["trajectory"] = traj

    # what would change the answer (2040 transfer, base): the avoided-rent yield at which living in the
    # house equals renting it out. Rent-out income and avoided rent use the same yield, so the comparison
    # is run on the avoided-rent credit only (credit_yield), against the rent-out case at the base yield.
    target = simulate("rent", 2040, REGIMES[0])["wealth"]
    lo, hi = 0.0, 0.12
    for _ in range(60):
        mid = (lo + hi) / 2
        if simulate("live", 2040, REGIMES[0], credit_yield=mid)["wealth"] < target:
            lo = mid
        else:
            hi = mid
    res["break_even_rent_yield_2040_base"] = (lo + hi) / 2
    # cash-only living (A0, no credit for avoided rent) against renting out: gross rent yield at which they tie
    lo, hi = 0.0, 0.12
    for _ in range(60):
        mid = (lo + hi) / 2
        if simulate("rent", 2040, REGIMES[0], rent_yield=mid)["wealth"] < simulate("live", 2040, REGIMES[0], avoid_rent=False)["wealth"]:
            lo = mid
        else:
            hi = mid
    res["cash_only_vs_rent_break_even_gross_yield_2040_base"] = (lo + hi) / 2

    # composite tax rate sensitivity
    res["sens_tax_rate"] = {}
    for label, rate in [("1.12", 0.0112), ("1.20", 0.0120), ("1.24", 0.0124),
                        ("owner_implied", OWNER["A_tax_2025"] / OWNER["A_av_2025"])]:
        res["sens_tax_rate"][label] = {"rate": rate,
            "live": simulate("live", 2040, REGIMES[0], tax_rate=rate)["wealth"],
            "rent": simulate("rent", 2040, REGIMES[0], tax_rate=rate)["wealth"]}

    # reinvestment risk: park yield 4.32% vs 3.00%, T=2040, all regimes
    res["reinvestment"] = {}
    for label, pr in [("4.32", TREASURY_3M), ("3.00", A["park_rate_low"])]:
        res["reinvestment"][label] = {}
        for reg in REGIMES:
            res["reinvestment"][label][reg.name] = {
                "sell_lump": simulate("sell_lump", 2040, reg)["wealth"],
                "sell_phased_24": simulate("sell_phased", 2040, reg, park_months=24, park_rate=pr)["wealth"],
                "sell_phased_36": simulate("sell_phased", 2040, reg, park_months=36, park_rate=pr)["wealth"],
            }
    res["_meta"] = {"horizon": f"{START_YEAR}-{END_YEAR}", "unit": "2026 dollars (CPI-deflated)",
                    "model": "monthly simulation; see methodology page"}
    return res


if __name__ == "__main__":
    DATA.mkdir(parents=True, exist_ok=True)
    res = build()
    def _round(x, key=""):
        # money to the nearest $10; rates and yields (|x| < 1) are kept at full precision
        if isinstance(x, bool) or not isinstance(x, float):
            if isinstance(x, dict):
                return {k: _round(v, k) for k, v in x.items()}
            if isinstance(x, list):
                return [_round(v, key) for v in x]
            return x
        if abs(x) < 1:
            return x
        return round(x / 10.0) * 10.0

    res = _round(res)
    (DATA / "model.json").write_text(json.dumps(res, indent=1, sort_keys=True))
    print("wrote", DATA / "model.json", "grid cells:", len(res["grid"]))
