"""After-tax estate & property decision model for the anonymized desk (desk-b4f).

Extends the PR #36 baseline (scripts/desk_model.py) with four official-source
tax and tariff mechanics while maintaining identical privacy guarantees:
  * Only banded property anchors and verified official statutory parameters.
  * Zero personal identifiers, addresses, parcel numbers, ZIPs, or city names.
  * Zero multi-year parcel-traceable assessment/tax bill histories.
  * Money rounded to the nearest $10 only at display time (statutory limits
    are tagged and printed verbatim).

New mechanics verified against IRS / FTB / BOE / CPUC / CDI / SCC / SFPUC sources:
  1. IRC Sec. 121 Principal Residence Exclusion ($250,000 single / $500,000 MFJ;
     CA R&TC Sec. 17152 conformity) applied to terminal sale in S1 (Occupy A).
  2. IRC Sec. 168 / 469 / 1250 Residential Rental Tax Engine for S2 (Rent A):
     - Date-of-death stepped-up basis (IRC Sec. 1014) = FMV_transfer.
     - 27.5-year MACRS GDS straight-line depreciation on building share (40% default,
       tested across 35%-45%; land is non-depreciable per IRS Pub 527).
     - IRC Sec. 469 passive activity loss suspension (when MAGI >= $150,000;
       also models active $25,000 allowance when MAGI <= $100,000) and pure
       property-only disposition release (offsetting Sec. 1250 recapture first,
       then Sec. 1231/capital gain, without assuming outside W-2 arbitrage).
     - IRC Sec. 1250 unrecaptured depreciation taxed at 25% federal max + 3.8% NIIT
       + CA ordinary rate (42.1% combined top bracket; 34.3%-42.1% across brackets).
  3. Ad Valorem vs. Fixed Direct Parcel Charges split (SCC FY 2025-26 Tax Rate
     Book & SF Treasurer): fixed charges inflate at CPI rather than scaling when
     Prop 19 / full reassessment resets ad valorem taxable value.
  4. CPUC 20-Year Solar NEM Legacy Sunset (D.14-03-041 / D.22-12-056 / D.24-05-028):
     pre-April 15, 2023 NEM 1.0/2.0 systems roll onto Solar Billing Plan (NBT)
     plus PG&E $24.15/mo Tier 3 Base Services Charge by 2043.
"""

from dataclasses import dataclass

BASE = 2026

STATUTORY_2026_2027 = {
    "estate_exclusion_2026": 15_000_000,       # P.L. 119-21 (2026)
    "estate_exclusion_2027": 15_480_000,       # IRS Rev. Proc. 2026-35 Sec. 3.44
    "gift_annual_2026": 19_000,
    "gift_annual_2027": 20_000,                # IRS Rev. Proc. 2026-35 Sec. 3.46(1)
    "noncitizen_spouse_gift_2027": 201_000,    # IRS Rev. Proc. 2026-35 Sec. 3.46(2)
    "trust_top_ordinary_threshold_2027": 16_500,  # 37% above $16,500
    "trust_top_ltcg_threshold_2027": 16_750,      # 20% LTCG above $16,750
    "prop19_allowance_2025_2027": 1_044_586,      # BOE LTA 2025/009 (Feb 16 2025 - Feb 15 2027)
    "homeowners_exemption": 7_000,                # BOE Homeowners' Exemption
    "sec121_single": 250_000,                     # IRS Pub 523 / FTB R&TC 17152
    "sec121_mfj": 500_000,
    "pge_base_services_charge_monthly": 24.15,    # CPUC D.24-05-028 / Res. E-5354
    "sf_secured_rate_2026_27": 0.0118162182,      # SF Treasurer FY 2026-27
    "ca_estate_tax": 0,                           # SCO Form ET-1 (post-2004 deaths)
}

ASSUMPTIONS = {
    "inflation": 0.025,
    "home_growth": 0.040,
    "prop13_cap": 0.020,
    "rent_growth_a": 0.030,
    "rent_growth_b": 0.020,
    "allowance_base": 1_044_586,
    "allowance_growth": 0.020,      # Sensitivity also tests 0.011 (2021-2025 HPI pace) & 0.035
    "sell_cost_rate": 0.060,
    "sf_sell_cost_rate": 0.0625,
    "portfolio_return": 0.045,      # After-tax nominal portfolio return baseline
    "horizon": 25,
    "transfer_year": 2045,
    # Extended after-tax parameters
    "building_share_a": 0.40,       # 40% building / 60% land (tested 35% - 45%)
    "depreciation_life": 27.5,      # MACRS GDS residential rental (IRS Pub 527)
    "fed_ord_rate": 0.35,           # High-earner CA household federal ordinary rate
    "fed_ltcg_rate": 0.20,          # Federal top LTCG (20%; 15% sensitivity tested)
    "niit_rate": 0.038,             # IRC Sec. 1411 NIIT (3.8% above $200k/$250k)
    "ca_rate": 0.133,               # CA top rate 12.3% + 1.0% MHSA (tested 9.3%-13.3%)
    "sec1250_fed_rate": 0.25,       # Unrecaptured Sec. 1250 max federal rate (Topic 409)
    "nem_sunset_year": 2043,        # Latest 20-yr expiration for pre-Apr 15, 2023 NEM 1/2
    "post_nem_electric_2026_real": 480.0,  # $290 Base Services Charge + modest net evening import
}


def r10(x):
    return int(round(x / 10.0) * 10)


def money(x, dash_zero=True):
    if dash_zero and abs(x) < 5:
        return "—"
    sign = "-" if x < 0 else ""
    return f"{sign}${abs(r10(x)):,}"


def pct(x, digits=2):
    return f"{x * 100:.{digits}f}%"


@dataclass(frozen=True)
class BandedProperty:
    code: str
    market_value: float
    taxable_value: float
    ad_valorem_rate: float
    fixed_parcel_charges: float
    insurance: float
    water: float
    electric_pre_nem_sunset: float
    maintenance: float
    reserve: float
    gross_rent: float = 0.0
    vacancy_rate: float = 0.0
    management_rate: float = 0.0
    homeowners_exemption: float = 0.0
    rent_growth: float = 0.0
    water_growth: float = 0.025

    def taxable(self, year):
        return self.taxable_value * (1 + ASSUMPTIONS["prop13_cap"]) ** (year - BASE)

    def tax_on(self, base_value, year, occupied=False):
        ex = self.homeowners_exemption if occupied else 0.0
        ad_val = max(base_value - ex, 0.0) * self.ad_valorem_rate
        fixed = self.fixed_parcel_charges * (1 + ASSUMPTIONS["inflation"]) ** (year - BASE)
        return ad_val + fixed

    def rent(self, year):
        return self.gross_rent * (1 + self.rent_growth) ** (year - BASE)


A = BandedProperty(
    code="A",
    market_value=3_100_000.0,
    taxable_value=550_000.0,
    ad_valorem_rate=0.0118,       # 1.00% + ~0.18% SCC/local GO bonds
    fixed_parcel_charges=390.0,   # Non-ad-valorem direct parcel charges (2026 total = $6,880)
    insurance=3_000.0,
    water=1_500.0,
    electric_pre_nem_sunset=-180.0,
    maintenance=9_000.0,
    reserve=3_000.0,
    gross_rent=66_000.0,
    vacancy_rate=0.05,
    management_rate=0.08,
    homeowners_exemption=7_000.0,
    rent_growth=ASSUMPTIONS["rent_growth_a"],
    water_growth=0.030,           # Aligned with CPUC D.24-12-077 SJWC rate steps
)

B = BandedProperty(
    code="B",
    market_value=1_800_000.0,
    taxable_value=206_000.0,      # Implied anchor at SF secured rate (incl. typical direct charges F01)
    ad_valorem_rate=0.0118162182, # Exact SF FY 2026-27 secured rate
    fixed_parcel_charges=0.0,     # Embedded in $206k implied anchor until exact tax-bill split verified (F01)
    insurance=3_300.0,
    water=4_380.0,
    electric_pre_nem_sunset=600.0,
    maintenance=7_000.0,
    reserve=3_500.0,
    gross_rent=85_800.0,
    vacancy_rate=0.05,
    management_rate=0.08,
    homeowners_exemption=0.0,
    rent_growth=ASSUMPTIONS["rent_growth_b"],
    water_growth=0.035,           # SFPUC FY26-28 +12.5%/+12.3% near-term shock, moderating
)


def prop19_taxable(fmv, taxable, allowance):
    ceiling = taxable + allowance
    if fmv <= ceiling:
        return taxable
    return taxable + (fmv - ceiling)


def electric_cost_a(year, inflation=None, sunset_year=None, post_nem_real=None, apply_sunset=True):
    pi = ASSUMPTIONS["inflation"] if inflation is None else inflation
    sy = ASSUMPTIONS["nem_sunset_year"] if sunset_year is None else sunset_year
    p_real = ASSUMPTIONS["post_nem_electric_2026_real"] if post_nem_real is None else post_nem_real
    f = (1 + pi) ** (year - BASE)
    if apply_sunset and year >= sy:
        return p_real * f
    return A.electric_pre_nem_sunset * f


def a_continuity_row(year, apply_nem_sunset=True):
    fmv = A.market_value * (1 + ASSUMPTIONS["home_growth"]) ** (year - BASE)
    taxable = A.taxable(year)
    ad_val = taxable * A.ad_valorem_rate
    fixed_parcel = A.fixed_parcel_charges * (1 + ASSUMPTIONS["inflation"]) ** (year - BASE)
    tax = ad_val + fixed_parcel
    f = (1 + ASSUMPTIONS["inflation"]) ** (year - BASE)
    ins = A.insurance * f
    wat = A.water * (1 + A.water_growth) ** (year - BASE)
    elec = electric_cost_a(year, apply_sunset=apply_nem_sunset)
    maint_res = (A.maintenance + A.reserve) * f
    opex = ins + wat + elec + maint_res
    return {
        "year": year,
        "fmv": fmv,
        "taxable": taxable,
        "ad_val": ad_val,
        "fixed_parcel": fixed_parcel,
        "tax": tax,
        "insurance": ins,
        "water": wat,
        "electric": elec,
        "maint_reserve": maint_res,
        "opex": opex,
        "total_carry": tax + opex,
    }


def b_continuity_row(year, water_shock=False):
    fmv = B.market_value * (1 + ASSUMPTIONS["home_growth"]) ** (year - BASE)
    taxable = B.taxable(year)
    tax = taxable * B.ad_valorem_rate
    f = (1 + ASSUMPTIONS["inflation"]) ** (year - BASE)
    ins = B.insurance * f
    if year == 2026:
        wat = B.water
    elif year == 2027:
        wat = B.water * 1.125
    elif year == 2028:
        wat = B.water * 1.125 * 1.123
    else:
        wg = 0.055 if water_shock else B.water_growth
        wat = B.water * 1.125 * 1.123 * (1 + wg) ** (year - 2028)
    elec = B.electric_pre_nem_sunset * f
    maint_res = (B.maintenance + B.reserve) * f
    rent = B.rent(year)
    var = rent * (B.vacancy_rate + B.management_rate)
    opex = ins + wat + elec + maint_res + var
    noi = rent - tax - opex
    return {
        "year": year,
        "fmv": fmv,
        "taxable": taxable,
        "tax": tax,
        "rent": rent,
        "water": wat,
        "opex": opex,
        "noi": noi,
    }


def simulate_after_tax(
    transfer_year=None,
    horizon=None,
    home_growth=None,
    rent_growth=None,
    inflation=None,
    portfolio=None,
    allowance_growth=None,
    building_share=None,
    sec121_exclusion=None,
    fed_ord_rate=None,
    fed_ltcg_rate=None,
    niit_rate=None,
    ca_rate=None,
    magi_high=True,
    apply_nem_sunset=True,
    prop19_repealed=False,
    insurance_mult=1.0,
    transfer_discount=0.0,
    rent_discount=0.0,
    vacancy=None,
    unit3_net_annual_2026=0.0,
):
    """Full after-tax wealth engine for S1 (Occupy A), S2 (Rent A), S3 (Sell A).

    All cash flows compound to `transfer_year + horizon` at the after-tax
    portfolio return `portfolio` so every path uses the exact same terminal date.
    """
    y = ASSUMPTIONS["transfer_year"] if transfer_year is None else transfer_year
    h = ASSUMPTIONS["horizon"] if horizon is None else horizon
    if h < 1 or int(h) != h:
        raise ValueError("horizon must be a positive integer")
    g = ASSUMPTIONS["home_growth"] if home_growth is None else home_growth
    rg = ASSUMPTIONS["rent_growth_a"] if rent_growth is None else rent_growth
    pi = ASSUMPTIONS["inflation"] if inflation is None else inflation
    pr = ASSUMPTIONS["portfolio_return"] if portfolio is None else portfolio
    ag = ASSUMPTIONS["allowance_growth"] if allowance_growth is None else allowance_growth
    bldg = ASSUMPTIONS["building_share_a"] if building_share is None else building_share
    s121 = STATUTORY_2026_2027["sec121_mfj"] if sec121_exclusion is None else sec121_exclusion

    f_ord = ASSUMPTIONS["fed_ord_rate"] if fed_ord_rate is None else fed_ord_rate
    f_cg = ASSUMPTIONS["fed_ltcg_rate"] if fed_ltcg_rate is None else fed_ltcg_rate
    niit = ASSUMPTIONS["niit_rate"] if niit_rate is None else niit_rate
    ca = ASSUMPTIONS["ca_rate"] if ca_rate is None else ca_rate
    vac = A.vacancy_rate if vacancy is None else vacancy

    ord_comb = f_ord + niit + ca
    cg_comb = f_cg + niit + ca
    recap_comb = ASSUMPTIONS["sec1250_fed_rate"] + niit + ca

    n = y - BASE
    fmv0 = A.market_value * (1 + g) ** n * (1 - transfer_discount)
    taxable_pre = A.taxable_value * (1 + ASSUMPTIONS["prop13_cap"]) ** n
    allowance = ASSUMPTIONS["allowance_base"] * (1 + ag) ** n

    assess_s1 = fmv0 if prop19_repealed else prop19_taxable(fmv0, taxable_pre, allowance)
    assess_s2 = fmv0

    # S1: Occupy A
    s1_cf_fv = 0.0
    adval_s1_0 = max(assess_s1 - A.homeowners_exemption, 0.0) * A.ad_valorem_rate
    fixed_parcel_0 = A.fixed_parcel_charges * (1 + pi) ** n
    for i in range(h):
        yr = y + i
        inf_i = (1 + pi) ** (yr - BASE)
        ad_val = adval_s1_0 * (1 + ASSUMPTIONS["prop13_cap"]) ** i
        fixed_parcel = fixed_parcel_0 * (1 + pi) ** i
        tax_i = ad_val + fixed_parcel
        elec_i = electric_cost_a(yr, inflation=pi, apply_sunset=apply_nem_sunset)
        opex_i = (
            (A.insurance * insurance_mult + A.water + A.maintenance + A.reserve) * inf_i
            + elec_i
        )
        u3_after_tax = 0.0
        if unit3_net_annual_2026 > 0:
            u3_after_tax = (
                unit3_net_annual_2026
                * (1 + ASSUMPTIONS["rent_growth_b"]) ** (yr - BASE)
                * (1 - ord_comb)
            )
        net_out = tax_i + opex_i - u3_after_tax
        s1_cf_fv += net_out * (1 + pr) ** (h - i)

    value_end = fmv0 * (1 + g) ** h
    net_sale_gross = value_end * (1 - ASSUMPTIONS["sell_cost_rate"])
    raw_gain_s1 = max(net_sale_gross - fmv0, 0.0)
    taxable_gain_s1 = max(raw_gain_s1 - s121, 0.0)
    cg_tax_s1 = taxable_gain_s1 * cg_comb
    sec121_tax_saved = (raw_gain_s1 - taxable_gain_s1) * cg_comb
    net_asset_s1 = net_sale_gross - cg_tax_s1
    s1_wealth = net_asset_s1 - s1_cf_fv

    # S2: Rent A (Schedule E + 27.5-yr depreciation + Sec. 469 PAL + Sec. 1250 recapture)
    annual_depr = (fmv0 * bldg) / ASSUMPTIONS["depreciation_life"]
    adval_s2_0 = assess_s2 * A.ad_valorem_rate
    suspended_pal = 0.0
    accum_depr = 0.0
    s2_cf_fv = 0.0
    s2_pretax_cf_fv = 0.0

    for i in range(h):
        yr = y + i
        inf_i = (1 + pi) ** (yr - BASE)
        rent_i = A.gross_rent * (1 + rg) ** (yr - BASE) * (1 - rent_discount)
        ad_val = adval_s2_0 * (1 + ASSUMPTIONS["prop13_cap"]) ** i
        fixed_parcel = fixed_parcel_0 * (1 + pi) ** i
        tax_i = ad_val + fixed_parcel
        elec_i = electric_cost_a(yr, inflation=pi, apply_sunset=apply_nem_sunset)
        fixed_opex = (
            (A.insurance * insurance_mult + A.water + A.maintenance + A.reserve) * inf_i
            + elec_i
        )
        var_opex = rent_i * (vac + A.management_rate)
        opex_i = fixed_opex + var_opex
        pretax_cf = rent_i - tax_i - opex_i

        depr_i = annual_depr if i < int(ASSUMPTIONS["depreciation_life"]) else 0.0
        accum_depr += depr_i
        sched_e_net = pretax_cf - depr_i

        income_tax_i = 0.0
        if sched_e_net < 0:
            loss = -sched_e_net
            if magi_high:
                suspended_pal += loss
            else:
                allow = min(loss, 25_000.0)
                income_tax_i = -allow * ord_comb
                suspended_pal += loss - allow
        else:
            absorbed = min(sched_e_net, suspended_pal)
            suspended_pal -= absorbed
            taxable_rent = sched_e_net - absorbed
            income_tax_i = taxable_rent * ord_comb

        aftertax_cf = pretax_cf - income_tax_i
        s2_pretax_cf_fv += pretax_cf * (1 + pr) ** (h - i)
        s2_cf_fv += aftertax_cf * (1 + pr) ** (h - i)

    adj_basis_s2 = fmv0 - accum_depr
    total_gain_s2 = max(net_sale_gross - adj_basis_s2, 0.0)
    recapture_gain = min(accum_depr, total_gain_s2)
    cap_gain_s2 = max(total_gain_s2 - recapture_gain, 0.0)

    # Pure property-only Sec. 469(g) release: unused suspended PAL offsets Sec. 1250
    # recapture first, then long-term capital gain on the sale (no invented outside W-2 arbitrage).
    pal_on_recap = min(suspended_pal, recapture_gain)
    pal_on_cg = min(suspended_pal - pal_on_recap, cap_gain_s2)
    taxable_recap = recapture_gain - pal_on_recap
    taxable_cg_s2 = cap_gain_s2 - pal_on_cg

    net_terminal_tax_s2 = taxable_recap * recap_comb + taxable_cg_s2 * cg_comb
    pal_tax_benefit = pal_on_recap * recap_comb + pal_on_cg * cg_comb
    net_asset_s2 = net_sale_gross - net_terminal_tax_s2

    s2_pretax_wealth = (net_sale_gross - max(net_sale_gross - fmv0, 0.0) * cg_comb) + s2_pretax_cf_fv
    s2_aftertax_wealth = net_asset_s2 + s2_cf_fv

    # S3: Sell A at transfer & reinvest proceeds
    proceeds_s3 = fmv0 * (1 - ASSUMPTIONS["sell_cost_rate"])
    s3_wealth = proceeds_s3 * (1 + pr) ** h

    return {
        "transfer_year": y,
        "end_year": y + h,
        "fmv_transfer": fmv0,
        "value_end": value_end,
        "taxable_pre": taxable_pre,
        "allowance": allowance,
        "assess_s1": assess_s1,
        "assess_s2": assess_s2,
        "tax_s1_yr1": adval_s1_0 + fixed_parcel_0,
        "tax_s2_yr1": adval_s2_0 + fixed_parcel_0,
        "annual_depr": annual_depr,
        "accum_depr": accum_depr,
        "suspended_pal_end": suspended_pal,
        "pal_tax_benefit": pal_tax_benefit,
        "recapture_gain": recapture_gain,
        "sec121_tax_saved": sec121_tax_saved,
        "cg_tax_s1": cg_tax_s1,
        "net_terminal_tax_s2": net_terminal_tax_s2,
        "s1_cf_fv": s1_cf_fv,
        "s2_pretax_cf_fv": s2_pretax_cf_fv,
        "s2_aftertax_cf_fv": s2_cf_fv,
        "s2_tax_drag_fv": s2_pretax_wealth - s2_aftertax_wealth,
        "s1_wealth": s1_wealth,
        "s2_pretax_wealth": s2_pretax_wealth,
        "s2_wealth": s2_aftertax_wealth,
        "s3_wealth": s3_wealth,
        "proceeds_s3": proceeds_s3,
        "delta_s2_vs_s3": s2_aftertax_wealth - s3_wealth,
        "delta_s1_vs_s3": s1_wealth - s3_wealth,
    }


def estate_headroom_matrix():
    """Combined Property A + liquid estate headroom across 2040/2045/2050 and statutory regimes."""
    rows = []
    base_2027 = STATUTORY_2026_2027["estate_exclusion_2027"]
    for yr in (2040, 2045, 2050):
        fmv_a = A.market_value * (1 + ASSUMPTIONS["home_growth"]) ** (yr - BASE)
        excl_single = base_2027 * (1.022 ** (yr - 2027))
        excl_dsue = excl_single * 2.0
        excl_halved = excl_single * 0.50
        rows.append({
            "year": yr,
            "fmv_a": fmv_a,
            "excl_single": excl_single,
            "headroom_single": excl_single - fmv_a,
            "excl_dsue": excl_dsue,
            "headroom_dsue": excl_dsue - fmv_a,
            "excl_halved": excl_halved,
            "headroom_halved": excl_halved - fmv_a,
        })
    return rows


def break_even_portfolio_aftertax(year=2045):
    lo, hi = 0.0, 0.20
    target = simulate_after_tax(transfer_year=year)["s2_wealth"]
    for _ in range(80):
        mid = (lo + hi) / 2.0
        v = simulate_after_tax(transfer_year=year, portfolio=mid)["s3_wealth"]
        if v < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def break_even_home_growth_aftertax(year=2045):
    lo, hi = 0.0, 0.12
    for _ in range(80):
        mid = (lo + hi) / 2.0
        res = simulate_after_tax(transfer_year=year, home_growth=mid)
        if res["s2_wealth"] < res["s3_wealth"]:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


if __name__ == "__main__":
    for yr in (2040, 2045, 2050):
        r = simulate_after_tax(yr)
        print(
            f"{yr}->{r['end_year']}: S1={money(r['s1_wealth'])} | "
            f"S2_pre={money(r['s2_pretax_wealth'])} | S2_after={money(r['s2_wealth'])} | "
            f"S3={money(r['s3_wealth'])} | S2-S3={money(r['delta_s2_vs_s3'])}"
        )
    print("Break-even after-tax portfolio 2045:", pct(break_even_portfolio_aftertax(2045)))
    print("Break-even home growth 2045:", pct(break_even_home_growth_aftertax(2045)))
