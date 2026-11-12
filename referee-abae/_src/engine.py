"""Reference engine for the Property A decision (referee-abae).

Purpose: a second implementation of the after-tax comparison, used to cross-check numbers other sessions
publish. HONEST LIMIT: it was written after reading the model of desk-b4f, so agreement with that desk is
*replication* (the same stated mechanics give the same numbers), not independent validation of the mechanics.
Independence in this referee comes from other checks: official-source constants, closed-form identities,
alternative conventions, and historical baselines (see robustness.html and baselines.html).

Three paths for Property A after it is inherited in year T, all valued at the same terminal date T + h:
  S1 occupy  - heir lives in A: Prop 19 value-limit test, homeowners' exemption, section 121 on exit;
  S2 rent    - full reassessment, Schedule E with 27.5-year depreciation, passive-loss carry-forward,
               unrecaptured section 1250 gain on exit;
  S3 sell    - sell at the stepped-up basis and reinvest the net proceeds at an *after-tax* return.
Property B is already owned and identical in every path, so it drops out of the comparison (it appears only
through the optional unit-3 line).

Stdlib only, deterministic. Household-derived inputs have no defaults here (see Params).
"""
from dataclasses import dataclass, replace

BASE = 2026


@dataclass(frozen=True)
class Params:
    """Inputs of the reference model.

    The first block (anchors) has NO defaults on purpose: it is where household-derived inputs go, and this
    repository copy of the engine must not carry any. Tests use synthetic anchors; reproduce.py loads the
    anchors from the desk it is checking, at run time, and never writes them to any page.
    """
    # anchors: required, supplied by the caller
    v0: float                        # market value in 2026
    taxable0: float                  # factored taxable value in 2026
    fixed: float                     # direct (non ad valorem) parcel charges, 2026 dollars
    insurance: float
    water: float
    maint: float
    reserve: float
    elec_pre: float                  # negative = net credit while on the legacy solar tariff
    elec_post: float
    rent0: float                     # gross annual rent, 2026 dollars
    # growth
    g: float = 0.04                  # nominal home-price growth
    infl: float = 0.025              # CPI-type inflation
    cap: float = 0.02                # Prop 13 annual cap on taxable-value growth
    # property tax
    rate: float = 0.0118             # ad valorem rate for A (county-level approximation)
    hox: float = 7_000.0             # homeowners' exemption (occupied only)
    # Prop 19 value-limit allowance
    allowance0: float = 1_044_586.0  # 16 Feb 2025 - 15 Feb 2027 (BOE LTA 2025/009)
    allowance_mode: str = "desk"     # "desk": grows ag per year | "statute": biennial one-year HPI change
    prop19: bool = True              # False = relief not obtained (e.g. homeowners' exemption not filed in time)
    ag: float = 0.02
    nem_sunset: int = 2043
    tenant_pays_utilities: bool = False
    # rent path
    rent_g: float = 0.03
    vac: float = 0.05
    mgmt: float = 0.08
    bldg: float = 0.40               # depreciable share of stepped-up basis
    life: float = 27.5
    # sale and reinvestment
    sell: float = 0.06
    r: float = 0.045                 # after-tax nominal portfolio return
    # combined marginal tax rates (federal + NIIT + California)
    t_ord: float = 0.521
    t_cg: float = 0.371
    t_rec: float = 0.421
    s121: float = 500_000.0          # married filing jointly; 250_000 if single
    h: int = 25                      # holding / investment horizon, years
    unit3_net: float = 0.0           # optional: net annual rent of B's third unit, 2026 $, S1 only
    rent_g_b: float = 0.02
    # terminal-tax convention used to compare the paths at the horizon
    #   "desk"          : A is sold and taxed at the horizon (S1, S2); the reinvested portfolio is not taxed
    #   "liquidate_all" : S3's portfolio is also liquidated at the horizon; all return treated as gain (upper bound)
    #   "hold_all"      : nothing is liquidated; no terminal tax on any path (heir's own heirs get a new basis)
    terminal: str = "desk"
    water_g: float = -1.0            # water-cost growth; negative means "same as infl"


def fmv(p, year):
    return p.v0 * (1 + p.g) ** (year - BASE)


def taxable_before(p, year):
    return p.taxable0 * (1 + p.cap) ** (year - BASE)


def allowance(p, transfer_year):
    """Prop 19 value-limit allowance in force at the transfer.

    desk mode  : allowance0 * (1+ag)^(T-2026)  (what the published desks use)
    statute    : Art. XIII A s.2.1(c)(4): every other 16 Feb from 2027, multiply by (1 + FHFA California HPI change
                 for the *prior calendar year*). Projected here with the home-price growth g.
    """
    if p.allowance_mode == "desk":
        return p.allowance0 * (1 + p.ag) ** (transfer_year - BASE)
    n = 0 if transfer_year < 2027 else (transfer_year - 2027) // 2 + 1
    return p.allowance0 * (1 + p.g) ** n


def prop19_taxable(fmv_t, taxable_t, limit):
    """BOE Pub 801 value-limit test: excluded if fmv <= taxable + limit, else the excess is added."""
    return taxable_t if fmv_t <= taxable_t + limit else fmv_t - limit


def _electric(p, year):
    return (p.elec_post if year >= p.nem_sunset else p.elec_pre) * (1 + p.infl) ** (year - BASE)


def _carry(p, year, occupied_costs=True):
    """Owner-paid non-tax carrying cost of A in `year` (insurance, maintenance, reserve, water, electricity)."""
    f = (1 + p.infl) ** (year - BASE)
    base = (p.insurance + p.maint + p.reserve) * f
    if not p.tenant_pays_utilities or occupied_costs:
        wg = p.infl if p.water_g < 0 else p.water_g
        base += p.water * (1 + wg) ** (year - BASE) + _electric(p, year)
    return base


def run(p, T=2045):
    """Wealth of the three paths at T + h, plus the intermediate quantities a reader may want to check."""
    if p.h < 1 or int(p.h) != p.h:
        raise ValueError("horizon must be a positive whole number of years")
    if T < BASE:
        raise ValueError("transfer year cannot precede the base year")
    n = T - BASE
    f_val = fmv(p, T)
    tx_pre = taxable_before(p, T)
    lim = allowance(p, T)
    assess_occ = prop19_taxable(f_val, tx_pre, lim) if p.prop19 else f_val
    assess_rent = f_val
    fixed_T = p.fixed * (1 + p.infl) ** n
    out = {"T": T, "end": T + p.h, "fmv_T": f_val, "taxable_pre": tx_pre, "allowance": lim,
           "assess_occ": assess_occ, "assess_rent": assess_rent}

    # ---- S1 occupy
    adv0 = max(assess_occ - p.hox, 0.0) * p.rate
    s1_flows = 0.0
    for i in range(p.h):
        yr = T + i
        tax = adv0 * (1 + p.cap) ** i + fixed_T * (1 + p.infl) ** i
        u3 = 0.0
        if p.unit3_net > 0:
            u3 = p.unit3_net * (1 + p.rent_g_b) ** (yr - BASE) * (1 - p.t_ord)
        s1_flows += (tax + _carry(p, yr) - u3) * (1 + p.r) ** (p.h - i)
    end_val = f_val * (1 + p.g) ** p.h
    net_sale = end_val * (1 - p.sell)
    raw_gain = max(net_sale - f_val, 0.0)
    cg1 = 0.0 if p.terminal == "hold_all" else max(raw_gain - p.s121, 0.0) * p.t_cg
    out["tax_occ_y1"] = adv0 + fixed_T
    out["S1"] = net_sale - cg1 - s1_flows

    # ---- S2 rent
    dep = f_val * p.bldg / p.life
    adv0r = assess_rent * p.rate
    accum = 0.0
    susp = 0.0
    s2_flows = 0.0
    s2_pre = 0.0
    for i in range(p.h):
        yr = T + i
        rent = p.rent0 * (1 + p.rent_g) ** (yr - BASE)
        tax = adv0r * (1 + p.cap) ** i + fixed_T * (1 + p.infl) ** i
        opex = _carry(p, yr, occupied_costs=False) + rent * (p.vac + p.mgmt)
        pre = rent - tax - opex
        d = dep if i < int(p.life) else 0.0
        accum += d
        net = pre - d
        if net < 0:
            susp += -net
            inc_tax = 0.0
        else:
            used = min(net, susp)
            susp -= used
            inc_tax = (net - used) * p.t_ord
        s2_flows += (pre - inc_tax) * (1 + p.r) ** (p.h - i)
        s2_pre += pre * (1 + p.r) ** (p.h - i)
    adj_basis = f_val - accum
    gain = max(net_sale - adj_basis, 0.0)
    recap = min(accum, gain)
    capg = max(gain - recap, 0.0)
    s_on_rec = min(susp, recap)
    s_on_cg = min(susp - s_on_rec, capg)
    tax_end = (recap - s_on_rec) * p.t_rec + (capg - s_on_cg) * p.t_cg
    if p.terminal == "hold_all":
        tax_end = 0.0
    out["tax_rent_y1"] = adv0r + fixed_T
    out["rent_y1"] = p.rent0 * (1 + p.rent_g) ** n
    out["S2"] = net_sale - tax_end + s2_flows
    out["S2_pretax"] = (net_sale - max(net_sale - f_val, 0.0) * p.t_cg) + s2_pre
    out["accum_dep"] = accum
    out["suspended_loss_end"] = susp

    # ---- S3 sell
    out["proceeds"] = f_val * (1 - p.sell)
    out["S3"] = out["proceeds"] * (1 + p.r) ** p.h
    if p.terminal == "liquidate_all":
        out["S3"] -= (out["S3"] - out["proceeds"]) * p.t_cg
    out["housing_premium_per_year"] = (out["S3"] - out["S1"]) / p.h
    return out


def bisect(fn, lo, hi, target=0.0, it=80):
    """Root of fn(x) - target on [lo, hi]; fn must be monotone."""
    flo = fn(lo) - target
    for _ in range(it):
        mid = (lo + hi) / 2
        fm = fn(mid) - target
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def with_(p, **kw):
    return replace(p, **kw)
