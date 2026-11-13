"""Projection model for the inheritance decision desk (arena-3f269806).

Every owner input is ROUNDED to the nearest $10 before it is typed in here.
Every assumption is labelled ASSUMPTION; every official constant carries a source id.
Outputs are derived values; they are never presented as verified facts.
"""

def r10(x):
    """Round to nearest $10 (half up)."""
    if x >= 0:
        return int(((x + 5) // 10) * 10)
    return -int(((-x + 5) // 10) * 10)

# ---------- OFFICIAL CONSTANTS (see sources.html) ----------
CAP_ADD_2026 = 1044586        # BOE LTA 2025/009: Prop 19 $1M amount, valid 2025-02-16 to 2027-02-15 (S09)
FED_EXEMPT_2026 = 15000000    # IRS What's New / Estate tax page (S01, S02)
GIFT_EXCL_2026 = 19000        # Rev. Proc. 2025-32 sec 4.42 (S03)
TOP_ESTATE_RATE = 0.40        # IRC 2001(c) rate table top bracket (S04)
SF_RATE_FY2627 = 0.0118162182 # SF Treasurer FY2026-27 secured property tax rate (S13)
HOMEOWNERS_EXEMPT = 7000      # BOE Pub 29 (S11)
CPI_TARGET = 0.02             # FOMC longer-run goals (S15)

# ---------- OWNER INPUTS (rounded to $10; NOT verified against official records) ----------
A_MV0 = 3100000   # estimated market value, Nov 2026 (owner)
A_AV0 = 550540    # 2026 assessed value (owner)
A_TAX25 = 7210    # 2025 secured tax (owner)
A_AV25 = 539740   # 2025 assessed value (owner)
A_INS = 1500      # homeowners insurance estimate per year (owner; unverified)
A_WATER_MO = 125  # midpoint of owner range $100-$150 per month
B_MV0 = 1800000   # estimated market value, Nov 2026 (owner)
B_AV25 = 114250   # 2025 assessed value (owner)
B_TAX25 = 2440    # 2025 secured tax (owner)
B_RENT_MO = 7150  # rent from two rented units (owner)
B_WATER_MO = 365  # midpoint of owner range $330-$400 for three units
B_ELEC_MO = 50    # midpoint of owner range $30-$70
B_INS = 1500      # estimate per year (owner; unverified)

# effective tax rate implied by the owner's own 2025 bill (derived; not an official rate)
A_RATE = A_TAX25 / A_AV25          # about 1.3357 percent
B_RATE_BILLED = B_TAX25 / B_AV25   # about 2.1355 percent (does NOT match SF rate; flagged F02)

# ---------- ASSUMPTIONS (labelled; not from a source) ----------
BASE = dict(
    name="Base",
    cpi=0.02,        # = FOMC target (S15)
    hpi=0.02,        # value growth, Property A and B (ASSUMPTION)
    rent_g=0.03,     # rent growth, Property B (ASSUMPTION)
    ins_g=0.04,      # insurance growth (ASSUMPTION)
    water_g=0.03,    # water growth (ASSUMPTION)
    maint_A=0.005,   # maintenance on A as share of market value (ASSUMPTION, no source)
    maint_B=0.05,    # maintenance on B as share of gross rent (ASSUMPTION, no source)
    vac_B=0.05,      # vacancy on B (ASSUMPTION)
    sell_cost=0.06,  # selling costs on A (ASSUMPTION, no source)
    r_at=0.04,       # after-tax return on reinvested proceeds (ASSUMPTION, no source)
    slump_years=0,
)

SCENARIOS = [
    BASE,
    dict(BASE, name="1970s-style inflation", cpi=0.07, hpi=0.04, rent_g=0.06, ins_g=0.08, water_g=0.06, r_at=0.03),
    dict(BASE, name="Housing slump, then recovery", cpi=0.01, hpi=-0.02, rent_g=0.01, ins_g=0.05, slump_years=10),
    dict(BASE, name="Deflation", cpi=-0.01, hpi=-0.01, rent_g=-0.01, ins_g=0.02, water_g=0.0, r_at=0.03),
    dict(BASE, name="Insurance shock", ins_g=0.10),
    dict(BASE, name="Strong growth", hpi=0.04, rent_g=0.04, r_at=0.06),
]


def hpi_path(sc, n):
    """Cumulative value growth factor after n years (supports a multi-year slump)."""
    f = 1.0
    for i in range(n):
        g = sc["hpi"]
        if sc.get("slump_years") and i >= sc["slump_years"]:
            g = 0.02
        f *= (1 + g)
    return f


def av_growth(sc):
    # Prop 13: annual increase is the lesser of CPI or 2% (S12, S11).
    # Declines (Prop 8 reviews) are not modelled: growth floored at 0.
    return max(0.0, min(sc["cpi"], 0.02))


def prop_a(sc, year):
    n = year - 2026
    V = A_MV0 * hpi_path(sc, n)
    base = A_AV0 * (1 + av_growth(sc)) ** n
    return V, base


def A_tax_no_transfer(sc, year):
    _, base = prop_a(sc, year)
    return A_RATE * base


def A_av_excl(sc, T, t):
    """Assessed value after a transfer in year T with the parent-child exclusion (child lives there)."""
    VT, baseT = prop_a(sc, T)
    AV_T = min(VT, baseT + CAP_ADD_2026)
    Vt, _ = prop_a(sc, t)
    return min(Vt, AV_T * (1 + av_growth(sc)) ** (t - T))


def A_av_noexcl(sc, T, t):
    """Reassessed to market value at transfer, no exclusion (rented or not occupied by transferee)."""
    VT, _ = prop_a(sc, T)
    return VT * (1 + av_growth(sc)) ** (t - T)


def A_costs(sc, year):
    n = year - 2026
    V, _ = prop_a(sc, year)
    ins = A_INS * (1 + sc["ins_g"]) ** n
    water = A_WATER_MO * 12 * (1 + sc["water_g"]) ** n
    maint = sc["maint_A"] * V
    return ins, water, maint


def B_noi(sc, year):
    n = year - 2026
    rent = B_RENT_MO * 12 * (1 + sc["rent_g"]) ** n
    gross = rent * (1 - sc["vac_B"])
    maint = sc["maint_B"] * rent
    tax = B_TAX25 * (1 + av_growth(sc)) ** (year - 2025)
    water = B_WATER_MO * 12 * (1 + sc["water_g"]) ** n
    elec = B_ELEC_MO * 12 * (1 + sc["water_g"]) ** n
    ins = B_INS * (1 + sc["ins_g"]) ** n
    noi = gross - maint - tax - water - elec - ins
    return dict(rent=rent, gross=gross, maint=maint, tax=tax, water=water, elec=elec, ins=ins, noi=noi)


def decision(sc, T):
    """Annual steady-state economics for a transfer in year T (first year after transfer)."""
    VT, _ = prop_a(sc, T)
    ins, water, maint = A_costs(sc, T)
    tax_ex = A_RATE * A_av_excl(sc, T, T)
    tax_no = A_RATE * A_av_noexcl(sc, T, T)
    P = VT * (1 - sc["sell_cost"])     # net proceeds if sold
    inv = P * sc["r_at"]               # annual return if reinvested (after-tax assumption)
    carry_live = tax_ex + ins + water + maint
    carry_rent = tax_no + ins + water + maint
    be_live = carry_live + inv                       # avoided comparable rent needed to prefer living in A
    be_rent = (carry_rent + inv) / (1 - sc["vac_B"])  # gross rent needed to prefer renting A over selling
    return dict(T=T, V=VT, tax_ex=tax_ex, tax_no=tax_no, ins=ins, water=water, maint=maint,
                P=P, inv=inv, carry_live=carry_live, carry_rent=carry_rent,
                be_live=be_live, be_rent=be_rent)


def cpi_real_factor(sc, year):
    n = year - 2026
    return (1 + sc["cpi"]) ** n


if __name__ == "__main__":
    for y in (2026, 2040, 2045, 2050, 2076):
        V, b = prop_a(BASE, y)
        print(y, r10(V), r10(b), r10(A_RATE * b))
    for T in (2040, 2045, 2050):
        d = decision(BASE, T)
        print({k: (r10(v) if isinstance(v, float) and k not in ("T",) else v) for k, v in d.items()})
    print("A rate", A_RATE, "B billed rate", B_RATE_BILLED)
