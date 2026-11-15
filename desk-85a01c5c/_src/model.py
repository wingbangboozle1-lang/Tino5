"""desk-85a01c5c decision model.

Conventions (mirroring the repo's hard rules):
  * Money figures are rounded to the nearest $10 by m0() unless they are
    statutory / agency-published amounts, which are kept exact and marked.
  * Owner-supplied figures are anchors labelled unverified; official-verified
    cells stay blank where no official source exists.
  * Privacy: properties are "Property A" (future trust inheritance, Santa Clara
    County) and "Property B" (already owned, San Francisco County). No ZIP,
    city, street, parcel or account identifier enters this module.

Series embedded below are transcriptions of official publications. Their
provenance was established in this repository by session arena-3a49d618
(swan-3a49/data/README.md): the pages were fetched from the official hosts,
transcribed, and later compared value-by-value against fresh official responses
(three discrepancies found and corrected on the record). The official URLs are
in SOURCES in build.py; the model states the values it uses and nothing more.
"""

# ---------------------------------------------------------------------------
# 1. Owner-supplied anchors (round of record: nearest $10)
# ---------------------------------------------------------------------------
OWNER = {
    # Property A (to be inherited through the trust, expected 2040-2050)
    "A_value_2026":        3_100_000,   # owner estimate, Nov 2026
    "A_assessed_2026":     550_000,     # owner-supplied, published as a banded
                                        # anchor (exact figure withheld: public
                                        # record traceable to a parcel)
    "A_water_lo":          100,         # $/month, owner-supplied
    "A_water_hi":          150,
    "A_solar_lo":          10,          # $/month credit, owner-supplied
    "A_solar_hi":          20,
    "A_insurance":         1_500,       # $/year, owner-supplied, unverified
    # Property B (already owned; 3 livable units, 2 rented)
    "B_value_2026":        1_800_000,   # owner estimate, Nov 2026
    "B_assessed_2026":     112_500,     # owner-supplied, banded anchor
    "B_effective_rate":    0.021,       # owner-implied incl. fixed charges,
                                        # banded, unverified
    "B_rent":              7_150,       # $/month, 2 rented units, owner-supplied
    "B_water_lo":          330,         # $/month, 3 units, owner-supplied
    "B_water_hi":          400,
    "B_elec_lo":           30,
    "B_elec_hi":           70,
    "B_insurance":         1_500,       # $/year, owner-supplied, unverified
}

# ---------------------------------------------------------------------------
# 2. Statutory / agency-published exact amounts (never $10-rounded)
# ---------------------------------------------------------------------------
STATUTORY = {
    # Federal estate & gift (Rev. Proc. 2025-32 sec. 2.14; IRS newsroom 2026)
    "estate_exclusion_2026": 15_000_000,
    "estate_top_rate_pct":   40,          # IRC 2001(c)
    "gst_exemption_2026":    15_000_000,
    # California Prop 19 (BOE NR-25-02; transfers 2/16/2025-2/15/2027)
    "prop19_allowance":      1_044_586,
    "prop19_allowance_prior": 1_022_600,
    # Prop 13 (Cal. Const. art. XIII-A): 1% levy; 2% assessed-value cap
    "levy_1pct":             1.00000,
    "cap_2pct_pct":          2,
    # Santa Clara County components (Tax Rate Book FY2025-26, pp. A-4)
    "scc_retirement_levy":   0.03880,
    "scc_library_levy":      0.00240,
    "scc_housing_bond_2016": 0.00560,
    "scc_vmc_2008":          0.00520,
    "scc_scvwd_state_water": 0.00390,     # applied to land & improvements
    # Santa Clara County documentary transfer tax / recording (Clerk-Recorder)
    "scc_transfer_tax_per_500": 0.55,
    "scc_sb2_fee":           75,
    "scc_ab1466_fee":        2,
    "scc_pcor_fee":          20,
    # San Francisco transfer tax, tier $1,000,000-$4,999,999
    # (Assessor-Recorder factsheet 2025: $3.75 per $500 of full value)
    "sf_transfer_per_500_1m_5m": 3.75,
    # San Francisco Prop H parcel tax (SFMTA FAQ, FY2027-28 rates)
    "proph_multifamily_base": 249,
    "proph_multifamily_per_sqft_over_5000": 0.195,
    "proph_sfh_base":        129,
    "proph_nonres_base":     799,
    "proph_passthrough_max": 65,          # per rent-controlled unit, per year
    # IRS Sec. 121 exclusion
    "sec121_single":         250_000,
    "sec121_joint":          500_000,
}

# ---------------------------------------------------------------------------
# 3. Model assumptions (labelled assumption everywhere they are used)
# ---------------------------------------------------------------------------
ASSUMPTIONS = {
    "a_growth": 0.045,     # Property A market-value growth
    "b_growth": 0.045,     # Property B market-value growth
    "cap_2pct": 0.02,      # Prop 13 assessed-value cap assumed to bind
    "rate_lo": 0.0104,     # ad-valorem band, SCC rate book TRA tables reviewed
    "rate_base": 0.0112,   # band midpoint used as the base case
    "rate_hi": 0.0125,
    "rent_growth": 0.03,   # rent growth on Property B income
    "mgmt_pct": 0.08,      # property-management fee if A is let
    "vacancy_pct": 0.05,   # vacancy allowance if A is let
    "brokerage_pct": 0.05, # selling commission (negotiable; no official rate)
    "sale_fees_flat": 100, # recording + misc. per deed (assumption; SB2 $75 +
                           # AB1466 $2 are verified, first-page base fee varies)
    "inflation": 0.025,     # general inflation for cost escalation
    "base_equity_return": 7.0,   # nominal %/yr, assumption, below the ERP record
    "transfer_years": [2040, 2045, 2050],
    "horizon_year": 2076,
    "park_months_options": [24, 36],
    "phase_months_options": [12, 24],
}

# ---------------------------------------------------------------------------
# 4. Official series (transcribed; provenance in the module docstring)
# ---------------------------------------------------------------------------
# S&P composite index, end of year, and dividend-price ratio, per cent.
# Economic Report of the President 2026, Tables B-55 / B-56.
ERP_SP500 = {
    1975: (90.19, 4.31), 1976: (107.46, 3.77), 1977: (95.10, 4.62),
    1978: (96.11, 5.28), 1979: (107.94, 5.47), 1980: (135.76, 5.26),
    1981: (122.55, 5.20), 1982: (102.42, 5.82), 1983: (164.93, 4.20),
    1984: (167.28, 4.49), 1985: (211.28, 4.05), 1986: (242.17, 3.61),
    1987: (247.08, 3.45), 1988: (277.72, 3.70), 1989: (353.40, 3.51),
    1990: (330.22, 3.83), 1991: (417.09, 3.20), 1992: (438.48, 2.94),
    1993: (466.45, 2.83), 1994: (459.27, 2.97), 1995: (615.93, 2.42),
    1996: (740.74, 2.14), 1997: (970.43, 1.75), 1998: (1229.23, 1.33),
    1999: (1469.25, 1.21), 2000: (1320.28, 1.41), 2001: (1148.08, 1.47),
    2002: (879.82, 1.83), 2003: (1109.64, 1.60), 2004: (1211.92, 1.59),
    2005: (1248.29, 1.79), 2006: (1418.30, 1.87), 2007: (1468.36, 1.86),
    2008: (903.25, 2.37), 2009: (1115.10, 2.40), 2010: (1257.64, 1.98),
    2011: (1257.60, 2.05), 2012: (1426.19, 2.24), 2013: (1848.36, 2.14),
    2014: (2058.90, 1.91), 2015: (2043.94, 2.06), 2016: (2238.83, 1.99),
    2017: (2673.61, 1.85), 2018: (2506.85, 2.04), 2019: (3230.78, 1.84),
    2020: (3756.07, 1.57), 2021: (4766.18, 1.29), 2022: (3839.50, 1.57),
    2023: (4769.83, 1.62), 2024: (5881.63, 1.34), 2025: (6845.50, 1.24),
}

# 3-month Treasury bill secondary-market discount rate, annual average, per
# cent. Federal Reserve H.15 via FRED series TB3MS.
TB3MS = {
    1975: 5.78, 1976: 4.97, 1977: 5.27, 1978: 7.19, 1979: 10.07,
    1980: 11.43, 1981: 14.03, 1982: 10.69, 1983: 8.63, 1984: 9.52,
    1985: 7.48, 1986: 5.98, 1987: 5.78, 1988: 7.57, 1989: 8.11,
    1990: 7.51, 1991: 5.42, 1992: 3.43, 1993: 3.02, 1994: 4.21,
    1995: 5.51, 1996: 5.02, 1997: 5.07, 1998: 4.81, 1999: 4.65,
    2000: 5.82, 2001: 3.40, 2002: 1.62, 2003: 1.01, 2004: 1.37,
    2005: 3.16, 2006: 4.73, 2007: 4.35, 2008: 1.37, 2009: 0.15,
    2010: 0.14, 2011: 0.05, 2012: 0.09, 2013: 0.06, 2014: 0.03,
    2015: 0.05, 2016: 0.32, 2017: 0.95, 2018: 1.97, 2019: 2.11,
    2020: 0.37, 2021: 0.04, 2022: 2.02, 2023: 5.07, 2024: 4.97,
    2025: 4.07,
}

# Current parking-leg yields (U.S. Treasury daily par yield curve, latest
# published business day at build time, 13 Nov 2026): 3 Mo 4.32%, 2 Yr 4.88%.
CURRENT_3M = 4.32
CURRENT_2Y = 4.88

# Crash-replay anchors (Federal Reserve History essays, read in this session).
CRASH_1929 = {
    "peak_label": "Sep 3, 1929 (DJIA 381.17)",
    "trough_label": "Jul 8, 1932 (DJIA 41.22)",
    "drop": 0.89,            # per cent below the peak, official
    "months_down": 34,       # Sep 1929 -> Jul 1932
    "recovery_label": "Nov 23, 1954 (pre-crash level regained)",
    "recovery_month": 303,   # Sep 1929 -> Nov 1954
    "park_yield_note": "assumption",
    # No FRED TB3MS before 1934; the 1929-34 parking yield is an assumption.
    "park_yield_pct": 2.0,
    # The drawdown path is geometric interpolation between the official
    # endpoints (plus the official mid-November 1929 "lost almost half" point,
    # modelled as 52% of the peak ~2.5 months after the peak).
    "anchors": [(0.0, 1.0), (2.5, 0.52), (34.0, 0.11)],
}
CRASH_2008 = {
    "peak_label": "Oct 2007 (S&P 500 peak)",
    "trough_label": "Mar 2009 (S&P 500 trough)",
    "drop": 0.57,            # per cent below the peak, official
    "months_down": 17,       # Oct 2007 -> Mar 2009
    "recovery_label": "S&P end-of-year 2013 (ERP B-55) above the Oct 2007 peak",
    "recovery_month": 77,    # Oct 2007 -> Mar 2014 (ERP 2013 level held flat)
    "park_yield_note": "official (FRED TB3MS annual averages, 2007-2014)",
    # Official annual averages are used month-by-month during the park.
    # Drawdown path: geometric interpolation between the official endpoints.
    "anchors": [(0.0, 1.0), (17.0, 0.43)],
}

# ---------------------------------------------------------------------------
# 5. Helpers
# ---------------------------------------------------------------------------
def m0(x):
    """Round to the nearest $10 and format."""
    if x is None:
        return ""
    return f"${int(round(x / 10.0) * 10):,}"


def m10(x):
    """Nearest-$10 rounding without formatting (for internal consistency)."""
    return int(round(x / 10.0) * 10)


def equity_index_path(crash, months_total=None):
    """Monthly index path as a fraction of the pre-crash peak (1.0).

    Drawdown: piecewise-geometric interpolation through the official anchors
    (peak, and for 1929 the official mid-November 1929 point, then the official
    trough). Recovery:
      * 2008 replay: official ERP annual end-of-year index levels 2009-2013
        (B-55), interpolated geometrically month to month, then held flat
        (the 2013 level is above the 2007 peak, so the index stays there).
      * 1929 replay: geometric interpolation back to the pre-crash level at
        the official recovery month (parametric, labelled assumption).
    Index levels only: no dividends. This is stated on the pages.
    """
    months_total = months_total or crash["recovery_month"] + 1
    md = crash["months_down"]
    trough = 1.0 - crash["drop"]
    path = [1.0]
    for k in range(1, md + 1):
        # piecewise-geometric interpolation through the official anchors;
        # the last month of the segment lands exactly on the trough anchor
        for (o0, v0), (o1, v1) in zip(crash["anchors"], crash["anchors"][1:]):
            if o0 <= k <= o1:
                path.append(v0 * (v1 / v0) ** ((k - o0) / (o1 - o0)))
                break
    # the trough month is pinned to the official value
    path[md] = trough
    rec_start_idx = len(path) - 1  # index of the trough entry
    if crash is CRASH_2008:
        # official annual levels relative to the Oct 2007 peak
        pts = [(2009, ERP_SP500[2009][0] / ERP_SP500[2007][0]),
               (2010, ERP_SP500[2010][0] / ERP_SP500[2007][0]),
               (2011, ERP_SP500[2011][0] / ERP_SP500[2007][0]),
               (2012, ERP_SP500[2012][0] / ERP_SP500[2007][0]),
               (2013, ERP_SP500[2013][0] / ERP_SP500[2007][0])]
        # month offsets from the trough (Mar 2009)
        offsets = [(6, pts[0][1]), (18, pts[1][1]), (30, pts[2][1]),
                   (42, pts[3][1]), (54, pts[4][1])]
        prev_off, prev_val = 0, trough
        for off, val in offsets:
            for k in range(1, off - prev_off + 1):
                frac = k / (off - prev_off)
                path.append(prev_val * (val / prev_val) ** frac)
            prev_off, prev_val = off, val
    else:
        rec_len = crash["recovery_month"] - md
        for k in range(1, rec_len + 1):
            path.append(trough * ((1.0 / trough) ** (k / rec_len)))
    while len(path) < months_total:
        path.append(path[-1])
    return path[:months_total]


def park_yield_series(crash, months):
    """Monthly park yield (annual %, bank-disc. annual average basis).

    1929 replay: a constant assumption (no official FRED bill series before
    1934). 2008 replay: the official FRED TB3MS annual averages for 2007-2014,
    applied month by month.
    """
    out = []
    if crash is CRASH_2008:
        base_year = 2007  # Oct 2007 start
        for k in range(months):
            yr = base_year + (9 + k) // 12  # month 0 = Oct 2007
            yr = min(yr, max(TB3MS))
            out.append(TB3MS.get(yr, 0.05))
    else:
        out = [crash["park_yield_pct"]] * months
    return out


def replay_strategy(crash, park_months, phase_months, principal=10_000.0,
                    horizon=None, detail=False):
    """Value at the horizon of: park in 3M-2Y Treasuries for park_months, then
    phase into equities in equal monthly tranches over phase_months.

    The equity path is the crash replay above (fraction of the pre-crash peak,
    price index only, no dividends). Month 0 is the sale month: cash parked at
    month 0 earns its first month's yield by month 1. A tranche is bought at
    the START of month k once the park is over; leftover cash keeps earning the
    park yield. Returns the terminal value in dollars, or (value, cash, units)
    when detail=True.
    """
    path = equity_index_path(crash)
    horizon = horizon or len(path) - 1
    yields = park_yield_series(crash, len(path))
    cash = principal
    units = 0.0
    tranche = principal / phase_months
    for k in range(horizon):
        # phase-in buys at the start of month k once the park is over
        if k >= park_months and cash > 0:
            buy = min(tranche, cash)
            units += buy / path[k]
            cash -= buy
        # cash earns the park yield during month k
        if cash > 0:
            cash *= (1.0 + yields[k] / 100.0 / 12.0)
    value = cash + units * path[horizon]
    if detail:
        return value, cash, units
    return value


def lump_sum_at_peak(crash, principal=10_000.0, horizon=None):
    """Value at the horizon of investing everything at the crash peak."""
    path = equity_index_path(crash)
    horizon = horizon or len(path) - 1
    return principal * path[horizon]


def phasing_replay_table(principal=10_000.0):
    """Rows: crash x strategy, values at the trough and at trough+60 months.

    The trough-month and trough+60 readings are the honest comparison points:
    at the trough the crash has fully arrived; at trough+60 the recovery is
    far along (for 2008, at the official ERP 2013 level, held flat).
    """
    rows = []
    for crash in (CRASH_1929, CRASH_2008):
        md = crash["months_down"]
        h60 = md + 60
        lump_t = lump_sum_at_peak(crash, principal, md)
        lump_60 = lump_sum_at_peak(crash, principal, h60)
        for park in ASSUMPTIONS["park_months_options"]:
            for phase in ASSUMPTIONS["phase_months_options"]:
                vt = replay_strategy(crash, park, phase, principal, md)
                v60 = replay_strategy(crash, park, phase, principal, h60)
                rows.append((crash, park, phase, lump_t, vt, vt - lump_t,
                             lump_60, v60, v60 - lump_60))
    return rows


def erp_long_run_stats():
    """Long-run anchors from the official ERP record (price + dividends)."""
    yrs = sorted(ERP_SP500)
    trs, prev = [], None
    for y in yrs:
        if prev is not None:
            p_prev, p = ERP_SP500[prev][0], ERP_SP500[y][0]
            d = ERP_SP500[y][1]
            trs.append((p / p_prev - 1.0) * 100.0 + d)
        prev = y
    price_cagr = ((ERP_SP500[yrs[-1]][0] / ERP_SP500[yrs[0]][0])
                  ** (1.0 / (yrs[-1] - yrs[0])) - 1.0) * 100.0
    mean_tr = sum(trs) / len(trs)
    mean_div = sum(v[1] for v in ERP_SP500.values()) / len(ERP_SP500)
    return {"first_year": yrs[0], "last_year": yrs[-1],
            "price_cagr_pct": price_cagr, "mean_total_return_pct": mean_tr,
            "mean_dividend_yield_pct": mean_div}


def reinvestment_cost_no_crash(principal=10_000.0, park_months=36,
                               phase_months=24, years=10, equity_return=None):
    """Cost of the cushion if no crash arrives: park then phase vs lump sum
    when equities earn a steady return. Default return: 7.0%/yr assumption,
    below the official ERP record (shown as the upper anchor on the pages)."""
    if equity_return is None:
        equity_return = ASSUMPTIONS["base_equity_return"]
    mr = equity_return / 100.0 / 12.0
    months = years * 12
    lump = principal * (1.0 + mr) ** months
    cash = principal
    units = 0.0
    tranche = principal / phase_months
    park_rate = CURRENT_3M / 100.0 / 12.0
    for k in range(months):
        if k >= park_months and cash > 0:
            buy = min(tranche, cash)
            units += buy * (1.0 + mr) ** (months - k)
            cash -= buy
        if cash > 0:
            cash *= (1.0 + park_rate)
    value = cash + units
    return lump, value, lump - value, equity_return


# ---------------------------------------------------------------------------
# 6. Scenario engine (live / rent / sell, transfer years, identical horizons)
# ---------------------------------------------------------------------------
def prop19_assessed_after_transfer(assessed_at_transfer, market_at_transfer):
    """New assessed value if the Prop 19 parent-child exclusion is claimed:
    factored base year value + (market value - FBV - allowance), i.e. the
    excess over FBV + $1,044,586 is added to the FBV."""
    allowance = STATUTORY["prop19_allowance"]
    excess = market_at_transfer - (assessed_at_transfer + allowance)
    return assessed_at_transfer + max(0.0, excess)


def property_a_at(year, growth=None):
    g = growth if growth is not None else ASSUMPTIONS["a_growth"]
    return OWNER["A_value_2026"] * (1.0 + g) ** (year - 2026)


def property_a_assessed(year):
    return OWNER["A_assessed_2026"] * (1.0 + ASSUMPTIONS["cap_2pct"]) ** (year - 2026)


def property_b_at(year, growth=None):
    g = growth if growth is not None else ASSUMPTIONS["b_growth"]
    return OWNER["B_value_2026"] * (1.0 + g) ** (year - 2026)


def property_b_assessed(year):
    return OWNER["B_assessed_2026"] * (1.0 + ASSUMPTIONS["cap_2pct"]) ** (year - 2026)


def transfer_tax_a(market_at_transfer):
    n = int(round(market_at_transfer / 500.0))
    return round(STATUTORY["scc_transfer_tax_per_500"] * n, 2)


def transfer_tax_b(market_at_transfer):
    n = int(round(market_at_transfer / 500.0))
    return round(STATUTORY["sf_transfer_per_500_1m_5m"] * n, 2)


def proph_year(base_year_fy, cpi=ASSUMPTIONS["inflation"], sqft=None):
    """Prop H parcel tax for fiscal year base_year_fy. Default: multifamily
    parcel of 5,000 sq ft or less (base rate). sqft > 5000 adds the official
    per-sq-ft rate over 5,000 (capped by the official $50,000 maximum)."""
    if base_year_fy < 2027:
        return 0.0
    fy = base_year_fy
    base = float(STATUTORY["proph_multifamily_base"])
    if sqft is not None and sqft > 5000:
        base = min(base + (sqft - 5000)
                   * STATUTORY["proph_multifamily_per_sqft_over_5000"],
                   50_000.0)
    if fy <= 2028:
        return base
    # rises with inflation from FY2028-29 onward (official FAQ)
    return base * (1.0 + cpi) ** (fy - 2028)


def proph_total_15yr(cpi=ASSUMPTIONS["inflation"], sqft=None):
    return sum(proph_year(fy, cpi, sqft) for fy in range(2027, 2042))


def scenario_paths(transfer_year):
    """Compare, at the SAME transfer date and the SAME horizon end (2076):
      keep-live, keep-rent, sell-and-reinvest — plus the phased-investing
      variant of the sell path. Returns a dict of horizon wealth values.

    Wealth basis: Property A equity value at the horizon plus accumulated net
    operating cash flows, all in nominal dollars. Everything is a model output
    (labelled assumption/derived on the pages), driven by the owner anchors.
    """
    g = ASSUMPTIONS["a_growth"]
    rate = ASSUMPTIONS["rate_base"]
    infl = ASSUMPTIONS["inflation"]
    yrs_hold = ASSUMPTIONS["horizon_year"] - transfer_year
    mv_t = property_a_at(transfer_year, g)
    assessed_t = property_a_assessed(transfer_year)
    new_assessed = prop19_assessed_after_transfer(assessed_t, mv_t)

    # --- keep-live: occupy. Assessed under Prop 19 exclusion (if claimed).
    live_tax = new_assessed * rate
    live_costs = (live_tax
                  + (OWNER["A_water_lo"] + OWNER["A_water_hi"]) / 2.0 * 12
                  + OWNER["A_insurance"]
                  + 2_000)  # maintenance placeholder: blank on pages; $2,000
                            # stand-in here is NOT published; pages leave the
                            # maintenance row blank + flagged.
    live_costs -= (OWNER["A_solar_lo"] + OWNER["A_solar_hi"]) / 2.0 * 12
    # value kept growing
    keep_value = property_a_at(ASSUMPTIONS["horizon_year"], g)
    # --- keep-rent: same carrying costs + management/vacancy on gross rent.
    # Gross rent is unknown (flagged); the model solves the break-even below.
    # --- sell: net proceeds after costs, reinvested at the equity rate.
    brokerage = mv_t * ASSUMPTIONS["brokerage_pct"]
    ttax = transfer_tax_a(mv_t)
    fees = ASSUMPTIONS["sale_fees_flat"]
    proceeds = mv_t - brokerage - ttax - fees
    return {
        "transfer_year": transfer_year,
        "mv_at_transfer": mv_t,
        "fbv_at_transfer": assessed_t,
        "assessed_after_prop19": new_assessed,
        "live_tax": live_tax,
        "live_costs_year1": live_costs,
        "brokerage": brokerage,
        "transfer_tax": ttax,
        "fees": fees,
        "sale_fees_flat": fees,
        "proceeds": proceeds,
        "keep_value_at_horizon": keep_value,
        "years_hold": yrs_hold,
    }


def required_rent_break_even(transfer_year, alt_return=None):
    """Gross monthly rent on Property A at which keeping-and-renting matches
    selling-and-reinvesting over the identical horizon (nominal, pre-tax on
    the rental side except the transfer taxes priced into the sell path)."""
    g = ASSUMPTIONS["a_growth"]
    rate = ASSUMPTIONS["rate_base"]
    r = alt_return if alt_return is not None else reinvestment_return()
    yrs = ASSUMPTIONS["horizon_year"] - transfer_year
    mv_t = property_a_at(transfer_year, g)
    brokerage = mv_t * ASSUMPTIONS["brokerage_pct"]
    proceeds = mv_t - brokerage - transfer_tax_a(mv_t) - ASSUMPTIONS["sale_fees_flat"]
    sell_wealth = proceeds * (1.0 + r) ** yrs
    # keep+rent wealth: house value grows; annual net operating income accrues
    # and compounds at r as it is collected.
    # Solve: NOI_gross*(1-mgmt)*(1-vac) - tax(new assessed path? rented = reassessed)
    # NOTE: if let, the Prop 19 exclusion cannot be claimed (not the heir's
    # principal residence), so the property is fully reassessed to market value.
    rented_assessed = mv_t
    tax = rented_assessed * rate
    opex = tax + (OWNER["A_water_lo"] + OWNER["A_water_hi"]) / 2.0 * 12 \
        + OWNER["A_insurance"] + 2_000 \
        - (OWNER["A_solar_lo"] + OWNER["A_solar_hi"]) / 2.0 * 12
    factor = ((1.0 + ASSUMPTIONS["rent_growth"]) ** yrs - 1.0) \
        / ASSUMPTIONS["rent_growth"]  # annuity-due approx, year-1 rents
    keep_value = property_a_at(ASSUMPTIONS["horizon_year"], g)
    # keep_wealth = keep_value + NOI_1 * factor * (1+r)^? -> grow NOI at rent
    # growth and accumulate at r; approximate: NOI_1 * ((1+r)^yrs - (1+rg)^yrs)
    # / (r - rg) (growing annuity accumulated at r).
    rg = ASSUMPTIONS["rent_growth"]
    if abs(r - rg) < 1e-9:
        accum = yrs * (1.0 + r) ** (yrs - 1)
    else:
        accum = ((1.0 + r) ** yrs - (1.0 + rg) ** yrs) / (r - rg)
    noi_needed = (sell_wealth - keep_value) / accum
    gross_annual_needed = (noi_needed + opex) \
        / ((1.0 - ASSUMPTIONS["mgmt_pct"]) * (1.0 - ASSUMPTIONS["vacancy_pct"]))
    return gross_annual_needed / 12.0, {
        "sell_wealth": sell_wealth, "keep_value": keep_value,
        "rented_assessed": rented_assessed, "opex": opex, "accum": accum,
        "yrs": yrs, "return": r, "mv_t": mv_t,
    }


def reinvestment_return():
    """Base-case reinvestment return: 7.0%/yr nominal (assumption), below the
    official ERP record anchors (price CAGR 9.2%, mean total return 13.2%)."""
    return ASSUMPTIONS["base_equity_return"] / 100.0


def live_vs_rent_break_even_yield(transfer_year):
    """Avoided-rent yield: the value of occupying Property A as a fraction of
    its value at which living equals renting (nominal)."""
    rent_be, det = required_rent_break_even(transfer_year)
    value_of_occupying = rent_be * 12  # occupying saves paying that rent
    return value_of_occupying / det["mv_t"], det


def estate_headroom(gross_estate):
    excl = STATUTORY["estate_exclusion_2026"]
    taxable = max(0.0, gross_estate - excl)
    return excl - gross_estate, taxable, taxable * STATUTORY["estate_top_rate_pct"] / 100.0
