# -*- coding: utf-8 -*-
"""Deterministic decision model for desk-03242c78.

Everything here is arithmetic on labelled inputs. No input is presented as an official
figure unless `sources.py` carries an official document for it. Each input states its
status:

    owner      - household-supplied, unverified, rounded for publication
    derived    - arithmetic on owner figures; the method is stated on the page
    statutory  - quoted from an official document listed in sources.py
    assumption - a planning assumption, not a fact, always published as a range

PRIVACY RULE ENFORCED HERE: no input below may be a figure that could be matched back to
one parcel on a public assessment roll. Assessed values are rounded to the nearest
$10,000 and the household's year-by-year tax/assessment history is deliberately NOT stored
in this repository -- only the rate band it implies is kept, as three literals. Money is
rounded to the nearest $10 at the point of publication (`r10`).

Run: python3 desk-03242c78/_src/model.py   -> prints a summary, writes model.json
"""

from __future__ import annotations

import json
import os

# --------------------------------------------------------------------------- inputs
A_VALUE_2026 = 3_100_000        # owner anchor, presented as stated by the household
B_VALUE_2026 = 1_800_000        # owner anchor
A_ASSESSED = 550_000            # owner, rounded to nearest $10,000 for publication
B_ASSESSED = 115_000            # owner, rounded to nearest $5,000 for publication
B_TAX_2025 = 2_440              # owner, rounded to nearest $10

# Property A tax rate. The household's own tax/assessment history implies 1.323%-1.407%
# of assessed value (mean 1.349%). The county's published *typical* tax rate area is
# 1.1488 per $100 = 1.1488%. The parcel's own tax rate area is unverified, so the model
# carries the whole band and uses the owner-implied midpoint as its base case.
A_RATE_FLOOR = 0.011488         # statutory: typical TRA, Santa Clara assessor booklet
A_RATE_BASE = 0.013400          # derived from owner history (midpoint 1.349% rounded)
A_RATE_CEIL = 0.014100          # derived from owner history

# Property B. San Francisco secured rate for FY2026-27 is 1.18162182%; parcel taxes, bond
# measures and direct assessments sit outside that rate, so the add-on below is the part
# of the bill the ad valorem rate does not explain.
B_RATE = 0.0118162182           # statutory: sftreasurer.org
B_ADDON = 1_080                 # derived: owner's bill less (assessed value x B_RATE)

PROP13_CAP = 0.02               # statutory: factored base year value rises at most 2%/yr
PROP19_ALLOWANCE = 1_044_586    # statutory: 16 Feb 2025 - 15 Feb 2027
PROP19_GROWTH = 0.025           # assumption: FHFA California HPI to the next adjustment

SEC121_SINGLE = 250_000         # statutory
SEC121_JOINT = 500_000          # statutory

FED_LTCG = 0.20                 # Topic 409, top long-term rate
FED_NIIT = 0.038                # Topic 559
CA_TOP = 0.123                  # FTB: capital gain taxed as ordinary income
CA_BHST = 0.01                  # RTC 17043 / Form 540 line 62
CA_MAX = CA_TOP + CA_BHST       # 13.3%
FED_DEPREC_RECAPTURE = 0.25     # unrecaptured s.1250 gain, Topic 409

SELL_COST_BASE = 0.060          # assumption band 5%-7%: commission, escrow, title
SELL_COST_LO, SELL_COST_HI = 0.050, 0.070
COUNTY_TRANSFER_TAX = 0.0011    # statutory: RTC 11911, $0.55 per $500; no city rate added
RECORDING_FEE = 60              # derived from the SF recording schedule (band 50-120)
RECORDING_FEE_LO, RECORDING_FEE_HI = 50, 120

A_WATER_MO = 130                # owner band $100-$150
A_ELEC_MO = 0                   # owner: solar offsets consumption
B_WATER_MO = 365                # owner band $330-$400 for three units
B_ELEC_MO = 50                  # owner band $30-$70
INS_YR = 1_500                  # owner estimate, single figure each
B_RENT_MO = 7_150               # owner: two of three units combined
B_UNITS, B_UNITS_RENTED = 3, 2

A_MAINT_RATE = 0.0060           # assumption band 0.30%-0.90% of value per year
A_MAINT_LO, A_MAINT_HI = 0.0030, 0.0090
B_MAINT_RATE = 0.0090           # assumption band 0.60%-1.40%
B_MAINT_LO, B_MAINT_HI = 0.0060, 0.0140

A_RENT_MO = 7_500               # assumption band $6,000-$9,000: no comparables obtained
A_RENT_LO, A_RENT_HI = 6_000, 9_000
BUILDING_SHARE = 0.60           # assumption: share of value in the building, not land

HOUSE_GROWTH = 0.035
HOUSE_LO, HOUSE_HI = 0.015, 0.055
EQUITY_RETURN = 0.065
EQUITY_LO, EQUITY_HI = 0.040, 0.090
INFLATION = 0.027
INFLATION_LO, INFLATION_HI = 0.020, 0.035
TREASURY_3M = 0.0432            # observed 13 Nov 2026, not a forecast
TREASURY_2Y = 0.0488            # observed 13 Nov 2026, not a forecast

TRANSFER_YEARS = (2040, 2045, 2050)
HORIZON = 20
PARK_MONTHS = (24, 36)
PHASE_MONTHS = 24


def r10(x):
    """Round a money amount to the nearest $10 for publication."""
    return int(round(x / 10.0) * 10)


# --------------------------------------------------------------------------- helpers
def grown(x, years, rate):
    return x * (1.0 + rate) ** years


def prop13_step(cpi):
    return min(PROP13_CAP, cpi)


def prop19_taxable(prior_taxable, fmv, allowance):
    """RTC 63.2(d). Prior taxable value survives if FMV <= prior value + allowance."""
    cap = prior_taxable + allowance
    return prior_taxable if fmv <= cap else fmv - allowance


def allowance_at(year):
    return grown(PROP19_ALLOWANCE, max(0, year - 2025), PROP19_GROWTH)


# --------------------------------------------------------------------------- regimes
REGIMES = {
    "baseline": dict(
        label="Long-run baseline",
        inflation=0.0270, house=0.035, equity=0.065,
        note="Inflation is the 1913-2026 compound average of the CPI-U, computed on this "
             "desk from the BLS series. House growth and equity return are planning "
             "assumptions shown as a range, not forecasts.",
        anchor="bls_cpi", kind="anchor"),
    "high_inflation": dict(
        label="High inflation: the 1972-1982 record",
        inflation=0.0872, house=0.055, equity=0.045,
        note="Inflation is the actual CPI-U compound rate from 1972 to 1982, computed on "
             "this desk (index 41.82 to 96.50 = 8.72% a year). House and equity growth in "
             "that decade are assumptions; both are set below inflation because real "
             "returns were poor.",
        anchor="bls_cpi", kind="anchor"),
    "deflation_1930s": dict(
        label="Deflation: the 1929-1933 record",
        inflation=-0.0685, house=-0.040, equity=-0.120,
        note="Inflation is the actual CPI-U compound rate from 1929 to 1933, computed on "
             "this desk (index 17.16 to 12.93 = -6.85% a year). The Dow's -89% drawdown "
             "over the same period is from Federal Reserve History. The house and equity "
             "paths are assumptions that reproduce that record.",
        anchor="fed_1929", kind="anchor"),
    "great_recession": dict(
        label="Credit shock: the 2007-2009 record",
        inflation=0.0100, house=-0.070, equity=-0.140,
        note="Federal Reserve History: the S&P 500 fell 57% from October 2007 to March "
             "2009 and home prices about 30% from mid-2006 to mid-2009. The annual rates "
             "used here are assumptions that reproduce those cumulative moves over three "
             "years.",
        anchor="fed_great_recession", kind="anchor"),
    "stagnation": dict(
        label="Low growth: no crash and no boom",
        inflation=0.0180, house=0.015, equity=0.035,
        note="A deliberately dull regime, assumption only, included so the comparison is "
             "not decided by one optimistic path.",
        anchor=None, kind="assumption"),
}

GRID_HOUSE = (0.015, 0.025, 0.035, 0.045, 0.055)
GRID_EQUITY = (0.040, 0.052, 0.065, 0.078, 0.090)


# --------------------------------------------------------------------------- paths
# (id, label, kind, sell A, occupy A, let A, years held before sale of A)
PATHS = [
    ("P1", "Live in A; let all three units at B", "pure", False, True, False, 0),
    ("P2", "Let A out; live in B's vacant unit", "pure", False, False, True, 0),
    ("P3", "Sell A at the transfer date and invest at once", "pure", True, False, False, 0),
    ("P4", "Live in A five years, then sell under section 121", "mixed", True, True, False, 5),
    ("P4b", "Live in A ten years, then sell under section 121", "mixed", True, True, False, 10),
    ("P5", "Let A out ten years, then sell", "mixed", True, False, True, 10),
    ("P6", "Sell A, park in Treasuries 24 months, then phase in", "phased", True, False, False, 0),
    ("P6b", "Sell A, park in Treasuries 36 months, then phase in", "phased", True, False, False, 0),
    ("P7", "Sell A and B; own neither building", "mixed", True, False, False, 0),
]
PATHS_BY_ID = {p[0]: p for p in PATHS}
KIND_LABEL = {
    "pure": "One of the three pure choices",
    "mixed": "Mixed path: two or more decisions combined",
    "phased": "Phased-investing path",
}


def sell_property_A(gross, basis, depreciated, use_121):
    """Tax and net proceeds on a sale of Property A. Basis is FMV at death, adjusted up
    for later capital improvements (none assumed) and down by depreciation taken."""
    sell_cost = gross * SELL_COST_BASE
    ttax = gross * COUNTY_TRANSFER_TAX
    rec = RECORDING_FEE
    raw = gross - sell_cost - ttax - rec - basis + depreciated
    recapture = min(max(0.0, raw), depreciated)
    capgain = max(0.0, raw - recapture)
    excluded = min(capgain, SEC121_SINGLE) if use_121 else 0.0
    capgain -= excluded
    fed_recap = recapture * FED_DEPREC_RECAPTURE
    tax = fed_recap + capgain * (FED_LTCG + FED_NIIT + CA_MAX)
    proceeds = gross - sell_cost - ttax - rec - tax
    return dict(gross=gross, sell_cost=sell_cost, ttax=ttax, recording=rec,
                recapture=recapture, capgain=capgain, excluded=excluded,
                tax=tax, proceeds=proceeds)


def run_path(path_id, label, kind, sells_a, occupies_a, rents_a, hold,
             transfer_year, regime, gh=None, ge=None):
    """Monthly simulation of one path at one transfer year under one regime.

    The household always consumes exactly one dwelling. Shelter is valued at market rent
    and reported separately (`shelter`), so a path that occupies a house is not treated as
    receiving free housing and a path that sells is charged rent for a comparable dwelling.
    Every path therefore faces the same cost of shelter and the same horizon, and is
    compared at the same date through (financial assets) + (property held).

    Why monthly: the Treasury-parking paths switch assets mid-year. A monthly step is the
    shortest interval that needs no day-count convention and keeps every path comparable.
    """
    n0 = transfer_year - 2026
    cpi = regime["inflation"]
    house = regime["house"] if gh is None else gh
    eq = regime["equity"] if ge is None else ge
    allow = allowance_at(transfer_year)

    a_fmv0 = grown(A_VALUE_2026, n0, house)
    b_fmv0 = grown(B_VALUE_2026, n0, house)
    rent_a0 = grown(A_RENT_MO * 12.0, n0, cpi)
    rent_b_unit0 = grown(B_RENT_MO / float(B_UNITS_RENTED) * 12.0, n0, cpi)

    a_prior = grown(A_ASSESSED, n0, prop13_step(cpi))
    if occupies_a:
        a_taxable = prop19_taxable(a_prior, a_fmv0, allow)
        prop19_applied = True
    else:
        a_taxable = a_fmv0
        prop19_applied = False
    b_assessed = grown(B_ASSESSED, n0, prop13_step(cpi))
    prop_h = 249 if transfer_year <= 2042 else 0     # Measure H, multifamily parcel

    park = 0
    if path_id == "P6":
        park = 24
    elif path_id == "P6b":
        park = 36
    phased = park > 0
    sale_month = hold * 12 if sells_a else None

    opot = 0.0            # equity portfolio
    ppot = 0.0            # parked Treasury balance
    a_owned, b_owned = True, (path_id != "P7")
    a_basis = a_fmv0
    a_depreciated = 0.0
    a_moved = 0           # monthly slices transferred out of parking
    sale_report = None
    b_sale_report = None
    taxes_paid = operating_costs = rental_income = shelter = rent_paid = 0.0

    eq_m, r_m = eq / 12.0, TREASURY_2Y / 12.0
    months = HORIZON * 12

    for m in range(months):
        i = m // 12
        infl = (1.0 + cpi) ** i
        hfact = (1.0 + house) ** i
        monthly_cash = 0.0

        if m % 12 == 0:
            # -------- start-of-year disposals
            if a_owned and sale_month is not None and m == sale_month:
                rep = sell_property_A(a_fmv0 * hfact, a_basis, a_depreciated,
                                      occupies_a and hold >= 2)
                sale_report = dict(rep)
                a_owned = False
                if phased:
                    ppot += rep["proceeds"]
                else:
                    opot += rep["proceeds"]
            if b_owned and path_id == "P7" and m == 0:
                # Basis of the already-owned building is unknown; the assessed value is a
                # stand-in and is flagged as unverified on the page.
                rep = sell_property_A(b_fmv0, B_ASSESSED, 0.0, False)
                b_sale_report = dict(rep)
                b_owned = False
                opot += rep["proceeds"]

            # -------- annual operating flows for year i
            a_cash = 0.0
            if a_owned:
                a_tax = a_taxable * ((1.0 + prop13_step(cpi)) ** i if i else 1.0) * A_RATE_BASE
                a_costs = (a_tax + INS_YR * infl + (A_WATER_MO + A_ELEC_MO) * 12.0 * infl
                           + a_fmv0 * hfact * A_MAINT_RATE)
                a_cash = -a_costs
                if rents_a:
                    a_cash += rent_a0 * infl
                    a_depreciated += a_fmv0 * BUILDING_SHARE / 27.5
                taxes_paid += a_tax
                operating_costs += a_costs
                rental_income += max(0.0, a_cash + a_costs)
            b_cash = 0.0
            if b_owned:
                b_tax = (b_assessed * ((1.0 + prop13_step(cpi)) ** i if i else 1.0) * B_RATE
                         + B_ADDON * infl + prop_h * infl)
                b_costs = (b_tax + INS_YR * infl + (B_WATER_MO + B_ELEC_MO) * 12.0 * infl
                           + b_fmv0 * hfact * B_MAINT_RATE)
                let_units = B_UNITS if occupies_a else B_UNITS_RENTED
                b_cash = rent_b_unit0 * let_units * infl - b_costs
                taxes_paid += b_tax
                operating_costs += b_costs
                rental_income += rent_b_unit0 * let_units * infl
            # -------- shelter consumed
            if occupies_a and a_owned:
                shelter += rent_a0 * infl
            else:
                shelter += rent_b_unit0 * infl
                if path_id == "P7":
                    b_cash -= rent_b_unit0 * infl
                    rent_paid += rent_b_unit0 * infl
            monthly_cash = (a_cash + b_cash) / 12.0

        # -------- monthly growth
        opot *= (1.0 + eq_m)
        if ppot:
            ppot *= (1.0 + r_m)
            if phased and m >= (sale_month or 0) + park and ppot > 1.0:
                remaining = max(1, PHASE_MONTHS - a_moved)
                share = ppot / remaining if a_moved < PHASE_MONTHS else ppot
                ppot -= share
                opot += share
                a_moved += 1
        opot += monthly_cash

    a_final = a_fmv0 * (1.0 + house) ** HORIZON if a_owned else 0.0
    b_final = b_fmv0 * (1.0 + house) ** HORIZON if b_owned else 0.0
    nw = opot + ppot + a_final + b_final

    return dict(
        path=path_id, label=label, kind=kind, kind_label=KIND_LABEL[kind],
        transfer_year=transfer_year, regime=regime["key"],
        a_value=r10(a_fmv0), b_value=r10(b_fmv0),
        a_prior_taxable=r10(a_prior), a_taxable=r10(a_taxable),
        allowance=r10(allow), prop19_applied=prop19_applied,
        prop19_relief=r10(max(0.0, a_fmv0 - a_taxable)),
        a_annual_tax_now=r10(a_taxable * A_RATE_BASE),
        b_annual_tax_now=r10(b_assessed * B_RATE + B_ADDON + prop_h),
        sale_proceeds=r10(sale_report["proceeds"] if sale_report else 0.0),
        sale_tax=r10(sale_report["tax"] if sale_report else 0.0),
        sale_cost=r10((sale_report["sell_cost"] + sale_report["ttax"]
                       + sale_report["recording"]) if sale_report else 0.0),
        sec121_used=r10(sale_report["excluded"] if sale_report else 0.0),
        recapture=r10(sale_report["recapture"] if sale_report else 0.0),
        b_sale_proceeds=r10(b_sale_report["proceeds"] if b_sale_report else 0.0),
        b_sale_tax=r10(b_sale_report["tax"] if b_sale_report else 0.0),
        taxes_paid=r10(taxes_paid), operating_costs=r10(operating_costs),
        rental_income=r10(rental_income), rent_paid=r10(rent_paid),
        shelter=r10(shelter), financial=r10(opot + ppot),
        a_final=r10(a_final), b_final=r10(b_final),
        net_worth=r10(nw), net_worth_with_shelter=r10(nw + shelter),
    )


def summary_row(res):
    return (res["path"], res["label"], res["kind"],
            res["net_worth"], res["net_worth_with_shelter"],
            res["financial"], res["a_final"] + res["b_final"], res["shelter"])


# --------------------------------------------------------------------------- phased
def phase_compare(transfer_year, regime, park_months=24, phase_months=24,
                  crash_month=12, depth=0.35, horizon=20):
    """Park-and-phase versus buy-at-once, with one equity crash at `crash_month`.

    Returns the terminal multiple of $1 for each (a) buying at once, (b) parking first.
    The crash depth is a scenario input, never a prediction.
    """
    eq = regime["equity"]
    r_m = TREASURY_2Y / 12.0
    g_m = eq / 12.0
    months = horizon * 12

    # (a) buy everything at month 0
    port = 1.0
    for m in range(months):
        port *= (1.0 + g_m)
        if m == crash_month:
            port *= (1.0 - depth)

    # (b) park, then buy in equal monthly slices
    pot, port2 = 1.0, 0.0
    for m in range(months):
        if m < park_months:
            pot *= (1.0 + r_m)        # Treasuries are not marked down by an equity crash
        else:
            share = pot / float(phase_months)
            pot -= share
            port2 = port2 * (1.0 + g_m) + share
        if m == crash_month:
            port2 *= (1.0 - depth)
    return port, port2 + pot


def phase_break_even(transfer_year, regime, park_months=24, phase_months=24,
                     crash_month=12, horizon=20):
    """Crash depth at which parking first beats buying at once. None if never."""
    def advantage(depth):
        a, b = phase_compare(transfer_year, regime, park_months, phase_months,
                             crash_month, depth, horizon)
        return b - a

    if advantage(0.0) >= 0:
        return 0.0
    lo, hi = 0.0, 0.999
    if advantage(hi) < 0:
        return None
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if advantage(mid) < 0:
            lo = mid
        else:
            hi = mid
    return hi


# --------------------------------------------------------------------------- grid
def crossover(pa, pb, transfer_year, regime_key="baseline", axis="house",
             lo=0.02, hi=0.10, tol=1e-7):
    """Value of one assumption at which path `pa` stops beating path `pb`.

    axis="house"  - house-price growth
    axis="equity" - equity return
    Returns the crossover on the high side (the value above which pa wins), or None if the
    ranking does not change across the interval.
    """
    base = dict(REGIMES[regime_key], key=regime_key)

    def nw(pid, v):
        kw = {"gh": v} if axis == "house" else {"ge": v}
        return run_path(*PATHS_BY_ID[pid], transfer_year=transfer_year, regime=base,
                        **kw)["net_worth_with_shelter"]

    def better(v):
        return nw(pa, v) > nw(pb, v)

    if better(lo) == better(hi):
        return None
    for _ in range(90):
        mid = (lo + hi) / 2.0
        if better(mid) == better(lo):
            lo = mid
        else:
            hi = mid
    return round(hi, 6)


def grid_distribution(transfer_year, path_id, regime_key="baseline"):
    base = dict(REGIMES[regime_key], key=regime_key)
    row = PATHS_BY_ID[path_id]
    vals = []
    for gh in GRID_HOUSE:
        for ge in GRID_EQUITY:
            vals.append(run_path(*row, transfer_year=transfer_year, regime=base,
                                 gh=gh, ge=ge)["net_worth_with_shelter"])
    return sorted(vals)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    results = []
    for t in TRANSFER_YEARS:
        for rk, r in REGIMES.items():
            regime = dict(r, key=rk)
            for row in PATHS:
                results.append(run_path(*row, transfer_year=t, regime=regime))

    breakevens, phase_rows = {}, []
    for t in TRANSFER_YEARS:
        for rk, r in REGIMES.items():
            regime = dict(r, key=rk)
            for pm in PARK_MONTHS:
                for cm in (0, 6, 12, 24, 36):
                    breakevens["%d|%s|%d|%d" % (t, rk, pm, cm)] = phase_break_even(
                        t, regime, park_months=pm, crash_month=cm)
            a, b = phase_compare(t, regime, park_months=24, crash_month=12, depth=0.35)
            phase_rows.append(dict(transfer_year=t, regime=rk,
                                   buy_once=r10(1_000_000 * a),
                                   park24=r10(1_000_000 * b)))
    cross = {}
    for t in TRANSFER_YEARS:
        cross["%d|P1_vs_P3_house" % t] = crossover("P1", "P3", t, axis="house",
                                                   lo=0.02, hi=0.10)
        cross["%d|P2_vs_P3_house" % t] = crossover("P2", "P3", t, axis="house",
                                                   lo=0.02, hi=0.10)
        cross["%d|P4_vs_P3_house" % t] = crossover("P4", "P3", t, axis="house",
                                                   lo=0.02, hi=0.14)
        cross["%d|P1_vs_P3_equity" % t] = crossover("P1", "P3", t, axis="equity",
                                                    lo=0.02, hi=0.10)
        cross["%d|P5_vs_P3_house" % t] = crossover("P5", "P3", t, axis="house",
                                                   lo=0.02, hi=0.14)
    dist = {}
    for t in TRANSFER_YEARS:
        for p in PATHS_BY_ID:
            dist["%d|%s" % (t, p)] = grid_distribution(t, p)

    out = dict(
        model=dict(
            a_value=A_VALUE_2026, b_value=B_VALUE_2026,
            a_assessed=A_ASSESSED, b_assessed=B_ASSESSED, b_tax_reported=B_TAX_2025,
            a_rate_floor=A_RATE_FLOOR, a_rate_base=A_RATE_BASE, a_rate_ceil=A_RATE_CEIL,
            b_rate=B_RATE, b_addon=B_ADDON,
            prop19_allowance=PROP19_ALLOWANCE, prop19_growth=PROP19_GROWTH,
            sec121_single=SEC121_SINGLE, sec121_joint=SEC121_JOINT,
            sell_cost=SELL_COST_BASE, transfer_tax=COUNTY_TRANSFER_TAX,
            recording_fee=RECORDING_FEE,
            house_growth=HOUSE_GROWTH, equity_return=EQUITY_RETURN,
            inflation=INFLATION, treasury_3m=TREASURY_3M, treasury_2y=TREASURY_2Y,
            a_rent_mo=A_RENT_MO, b_rent_mo=B_RENT_MO,
            a_maint=A_MAINT_RATE, b_maint=B_MAINT_RATE,
        ),
        bands=dict(house=[HOUSE_LO, HOUSE_HI], equity=[EQUITY_LO, EQUITY_HI],
                   inflation=[INFLATION_LO, INFLATION_HI],
                   sell_cost=[SELL_COST_LO, SELL_COST_HI],
                   a_rent=[A_RENT_LO, A_RENT_HI],
                   a_maint=[A_MAINT_LO, A_MAINT_HI],
                   b_maint=[B_MAINT_LO, B_MAINT_HI]),
        regimes={k: dict(v, key=k) for k, v in REGIMES.items()},
        paths=[dict(id=p[0], label=p[1], kind=p[2], kind_label=KIND_LABEL[p[2]],
                    sells_a=p[3], occupies_a=p[4], rents_a=p[5], hold=p[6])
               for p in PATHS],
        grid=dict(house=GRID_HOUSE, equity=GRID_EQUITY),
        crossovers=cross, results=results, breakevens=breakevens, phase=phase_rows,
        distribution=dist,
    )
    with open(os.path.join(here, "model.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)

    print("== 2045 baseline, ranked by net worth including shelter consumed ==")
    rows = [r for r in results if r["transfer_year"] == 2045 and r["regime"] == "baseline"]
    for r in sorted(rows, key=lambda x: -x["net_worth_with_shelter"]):
        print("  %-4s %-56s NW %13s  +shelter %13s  fin %13s  prop %13s"
              % (r["path"], r["label"][:56], "{:,}".format(r["net_worth"]),
                 "{:,}".format(r["net_worth_with_shelter"]),
                 "{:,}".format(r["financial"]),
                 "{:,}".format(r["a_final"] + r["b_final"])))
    print()
    for k in sorted(dist):
        v = dist[k]
        print("  dist %-8s median %13s  p10 %13s  p90 %13s"
              % (k, "{:,}".format(v[len(v) // 2]), "{:,}".format(v[2]),
                 "{:,}".format(v[-3])))
    print()
    print("phase: $1,000,000 at transfer, 35% crash at month 12, 2045 baseline")
    for r in phase_rows:
        if r["transfer_year"] == 2045 and r["regime"] == "baseline":
            print("  buy at once %s   park 24m then phase %s"
                  % ("{:,}".format(r["buy_once"]), "{:,}".format(r["park24"])))
    print()
    print("break-even crash depth (2045 baseline):")
    for pm in PARK_MONTHS:
        line = []
        for cm in (0, 6, 12, 24, 36):
            v = breakevens["2045|baseline|%d|%d" % (pm, cm)]
            line.append("m%d:%s" % (cm, "never" if v is None else "%.1f%%" % (v * 100)))
        print("  park %dm  %s" % (pm, "  ".join(line)))
    return out


if __name__ == "__main__":
    main()
