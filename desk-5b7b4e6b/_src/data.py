# -*- coding: utf-8 -*-
"""Official series and owner inputs for desk-5b7b4e6b (session arena-5b7b4e6b, 2026-11-17).

Provenance of every number in this file
---------------------------------------
The four blocks below are transcriptions of official responses. Each block was compared
row by row against the live official response on 17 November 2026 and every value matched:

  * CPI / rates   — FRED CSV (BLS series CPIAUCNS, CUURA422SA0, CUURA422SEHA; Federal
                    Reserve series TB3MS, GS10), annual averages, 1975-2025.
  * House prices  — FRED CSV (FHFA series ATNHPIUS41940Q, ATNHPIUS41884Q, CASTHPI),
                    fourth-quarter value of each year, 1975-2025.
  * Equities      — Economic Report of the President 2026, Tables B-55 (1975-1999) and
                    B-56 (2000-2025): S&P composite index at end of year and the
                    dividend-price ratio. The four years that appear in both tables
                    (2000-2003) agree.
  * Prop 13 factors — California Board of Equalization Letter to Assessors 2026/002.

Nothing here is inferred, interpolated or estimated. A year without a published value is
absent, not zero-filled.

Owner inputs are separated into their own block and are labelled unverified: they are the
household's own figures, they are not corroborated by any official page, and they are used
only because the household supplied them. Values that can be tied to an individual parcel
(assessed values) are deliberately coarsened before publication; see flags F02 and F03.
"""

# ---------------------------------------------------------------------------
# 1. Consumer price index — annual averages (source: bls_fred)
# ---------------------------------------------------------------------------
CPI_US = {
    1975: 53.817, 1976: 56.908, 1977: 60.608, 1978: 65.233, 1979: 72.575,
    1980: 82.408, 1981: 90.925, 1982: 96.500, 1983: 99.600, 1984: 103.883,
    1985: 107.567, 1986: 109.608, 1987: 113.625, 1988: 118.258, 1989: 123.967,
    1990: 130.658, 1991: 136.192, 1992: 140.317, 1993: 144.458, 1994: 148.225,
    1995: 152.383, 1996: 156.850, 1997: 160.517, 1998: 163.008, 1999: 166.575,
    2000: 172.200, 2001: 177.067, 2002: 179.875, 2003: 183.958, 2004: 188.883,
    2005: 195.292, 2006: 201.592, 2007: 207.342, 2008: 215.303, 2009: 214.537,
    2010: 218.056, 2011: 224.939, 2012: 229.594, 2013: 232.957, 2014: 236.736,
    2015: 237.017, 2016: 240.007, 2017: 245.120, 2018: 251.107, 2019: 255.657,
    2020: 258.811, 2021: 270.970, 2022: 292.655, 2023: 304.702, 2024: 313.689,
    2025: 321.943,
}
# San Francisco area, all items — drives local running costs
CPI_SF = {
    1975: 52.050, 1976: 54.850, 1977: 59.200, 1978: 64.500, 1979: 70.200,
    1980: 80.767, 1981: 91.250, 1982: 97.583, 1983: 98.600, 1984: 104.283,
    1985: 108.483, 1986: 111.767, 1987: 115.392, 1988: 120.500, 1989: 126.350,
    1990: 132.050, 1991: 137.908, 1992: 142.500, 1993: 146.342, 1994: 148.650,
    1995: 151.567, 1996: 155.067, 1997: 160.383, 1998: 165.750, 1999: 172.767,
    2000: 180.583, 2001: 190.200, 2002: 193.083, 2003: 196.533, 2004: 198.983,
    2005: 202.867, 2006: 209.533, 2007: 216.388, 2008: 222.772, 2009: 224.634,
    2010: 227.612, 2011: 233.669, 2012: 239.868, 2013: 245.281, 2014: 252.260,
    2015: 258.812, 2016: 266.808, 2017: 275.399, 2018: 286.338, 2019: 295.371,
    2020: 300.444, 2021: 310.590, 2022: 327.961, 2023: 339.492, 2024: 349.021,
    2025: 356.632,
}
# San Francisco area, rent of primary residence — the best official series for how rents
# actually moved in the Bay Area
CPI_SF_RENT = {
    1975: 51.250, 1976: 54.300, 1977: 58.425, 1978: 62.617, 1979: 67.383,
    1980: 75.817, 1981: 83.433, 1982: 91.500, 1983: 100.650, 1984: 108.983,
    1985: 117.850, 1986: 127.500, 1987: 133.067, 1988: 138.783, 1989: 144.225,
    1990: 151.008, 1991: 156.400, 1992: 160.050, 1993: 164.367, 1994: 167.475,
    1995: 169.950, 1996: 174.458, 1997: 185.117, 1998: 199.617, 1999: 213.575,
    2000: 228.583, 2001: 252.875, 2002: 262.542, 2003: 262.842, 2004: 262.167,
    2005: 262.967, 2006: 266.992, 2007: 277.314, 2008: 288.810, 2009: 298.154,
    2010: 297.814, 2011: 304.693, 2012: 317.228, 2013: 331.454, 2014: 349.710,
    2015: 371.075, 2016: 395.720, 2017: 417.509, 2018: 439.733, 2019: 455.169,
    2020: 467.039, 2021: 467.526, 2022: 475.227, 2023: 498.649, 2024: 508.109,
    2025: 519.667,
}

# ---------------------------------------------------------------------------
# 2. Interest rates — annual averages, percent (source: bls_fred)
# ---------------------------------------------------------------------------
TB3MS = {
    1975: 5.78, 1976: 4.97, 1977: 5.27, 1978: 7.19, 1979: 10.07,
    1980: 11.43, 1981: 14.03, 1982: 10.61, 1983: 8.61, 1984: 9.52,
    1985: 7.48, 1986: 5.98, 1987: 5.78, 1988: 6.67, 1989: 8.11,
    1990: 7.49, 1991: 5.38, 1992: 3.43, 1993: 3.00, 1994: 4.25,
    1995: 5.49, 1996: 5.01, 1997: 5.06, 1998: 4.78, 1999: 4.64,
    2000: 5.82, 2001: 3.39, 2002: 1.60, 2003: 1.01, 2004: 1.37,
    2005: 3.15, 2006: 4.73, 2007: 4.35, 2008: 1.37, 2009: 0.15,
    2010: 0.14, 2011: 0.05, 2012: 0.09, 2013: 0.06, 2014: 0.03,
    2015: 0.05, 2016: 0.32, 2017: 0.93, 2018: 1.94, 2019: 2.06,
    2020: 0.37, 2021: 0.04, 2022: 2.02, 2023: 5.07, 2024: 4.97,
    2025: 4.07,
}
GS10 = {
    1975: 7.99, 1976: 7.61, 1977: 7.42, 1978: 8.41, 1979: 9.44,
    1980: 11.46, 1981: 13.91, 1982: 13.00, 1983: 11.11, 1984: 12.44,
    1985: 10.62, 1986: 7.68, 1987: 8.38, 1988: 8.85, 1989: 8.50,
    1990: 8.55, 1991: 7.86, 1992: 7.01, 1993: 5.87, 1994: 7.08,
    1995: 6.58, 1996: 6.44, 1997: 6.35, 1998: 5.26, 1999: 5.64,
    2000: 6.03, 2001: 5.02, 2002: 4.61, 2003: 4.02, 2004: 4.27,
    2005: 4.29, 2006: 4.79, 2007: 4.63, 2008: 3.67, 2009: 3.26,
    2010: 3.21, 2011: 2.79, 2012: 1.80, 2013: 2.35, 2014: 2.54,
    2015: 2.14, 2016: 1.84, 2017: 2.33, 2018: 2.91, 2019: 2.14,
    2020: 0.89, 2021: 1.44, 2022: 2.95, 2023: 3.96, 2024: 4.21,
    2025: 4.29,
}

# ---------------------------------------------------------------------------
# 3. House price indexes — fourth quarter of each year (source: fhfa_fred)
#    The 1975 values for the two metro series are not published in this response.
# ---------------------------------------------------------------------------
HPI_SJ = {          # San Jose metro area — used for Property A
    1976: 23.21, 1977: 30.02, 1978: 32.66, 1979: 40.49, 1980: 47.66,
    1981: 52.27, 1982: 50.50, 1983: 52.72, 1984: 56.65, 1985: 60.95,
    1986: 65.56, 1987: 72.14, 1988: 90.70, 1989: 114.25, 1990: 107.32,
    1991: 106.23, 1992: 104.34, 1993: 101.44, 1994: 99.95, 1995: 102.45,
    1996: 108.06, 1997: 122.46, 1998: 138.45, 1999: 157.67, 2000: 203.54,
    2001: 205.16, 2002: 216.22, 2003: 220.87, 2004: 255.24, 2005: 309.48,
    2006: 318.32, 2007: 302.81, 2008: 258.84, 2009: 237.76, 2010: 240.85,
    2011: 235.66, 2012: 252.50, 2013: 291.32, 2014: 319.27, 2015: 353.92,
    2016: 373.83, 2017: 396.48, 2018: 425.46, 2019: 415.13, 2020: 419.68,
    2021: 463.63, 2022: 510.15, 2023: 546.45, 2024: 558.19, 2025: 560.05,
}
HPI_SF = {          # San Francisco metro division — used for Property B
    1976: 23.70, 1977: 28.62, 1978: 31.52, 1979: 40.23, 1980: 45.17,
    1981: 46.03, 1982: 45.89, 1983: 49.44, 1984: 52.64, 1985: 58.13,
    1986: 65.71, 1987: 78.06, 1988: 98.50, 1989: 113.64, 1990: 109.68,
    1991: 107.13, 1992: 104.16, 1993: 101.60, 1994: 98.88, 1995: 100.94,
    1996: 103.59, 1997: 114.45, 1998: 127.97, 1999: 150.39, 2000: 184.16,
    2001: 192.89, 2002: 206.94, 2003: 219.05, 2004: 256.29, 2005: 301.62,
    2006: 307.14, 2007: 298.91, 2008: 267.06, 2009: 250.31, 2010: 248.26,
    2011: 240.50, 2012: 257.01, 2013: 296.34, 2014: 329.82, 2015: 374.38,
    2016: 396.57, 2017: 416.06, 2018: 445.81, 2019: 442.90, 2020: 425.06,
    2021: 451.73, 2022: 487.95, 2023: 495.49, 2024: 505.79, 2025: 512.99,
}

# ---------------------------------------------------------------------------
# 4. S&P composite index at end of year and dividend-price ratio (source: erp2026)
# ---------------------------------------------------------------------------
SP500 = {
    1975: 90.19, 1976: 107.46, 1977: 95.10, 1978: 96.11, 1979: 107.94,
    1980: 135.76, 1981: 122.55, 1982: 140.64, 1983: 164.93, 1984: 167.24,
    1985: 211.28, 1986: 242.17, 1987: 247.08, 1988: 277.72, 1989: 353.40,
    1990: 330.22, 1991: 417.09, 1992: 435.71, 1993: 466.45, 1994: 459.27,
    1995: 615.93, 1996: 740.74, 1997: 970.43, 1998: 1229.23, 1999: 1469.25,
    2000: 1320.28, 2001: 1148.08, 2002: 879.82, 2003: 1111.92, 2004: 1211.92,
    2005: 1248.29, 2006: 1418.30, 2007: 1468.36, 2008: 903.25, 2009: 1115.10,
    2010: 1257.64, 2011: 1257.60, 2012: 1426.19, 2013: 1848.36, 2014: 2058.90,
    2015: 2043.94, 2016: 2238.83, 2017: 2673.61, 2018: 2506.85, 2019: 3230.78,
    2020: 3756.07, 2021: 4766.18, 2022: 3839.50, 2023: 4769.83, 2024: 5881.63,
    2025: 6845.50,
}
SP500_DIV = {
    1975: 4.31, 1976: 3.77, 1977: 4.62, 1978: 5.28, 1979: 5.47,
    1980: 5.26, 1981: 5.20, 1982: 5.81, 1983: 4.40, 1984: 4.64,
    1985: 4.25, 1986: 3.49, 1987: 3.08, 1988: 3.64, 1989: 3.45,
    1990: 3.61, 1991: 3.24, 1992: 2.99, 1993: 2.78, 1994: 2.82,
    1995: 2.56, 1996: 2.19, 1997: 1.77, 1998: 1.49, 1999: 1.25,
    2000: 1.15, 2001: 1.32, 2002: 1.61, 2003: 1.77, 2004: 1.72,
    2005: 1.83, 2006: 1.87, 2007: 1.86, 2008: 2.37, 2009: 2.40,
    2010: 1.98, 2011: 2.05, 2012: 2.24, 2013: 2.14, 2014: 2.04,
    2015: 2.10, 2016: 2.19, 2017: 1.97, 2018: 1.90, 2019: 1.93,
    2020: 1.89, 2021: 1.38, 2022: 1.57, 2023: 1.62, 2024: 1.34,
    2025: 1.24,
}

# ---------------------------------------------------------------------------
# 5. Official constants read from statute or from an agency publication
# ---------------------------------------------------------------------------
OFFICIAL = {
    "estate_exclusion_2026": 15_000_000,     # irs_estate, filing threshold year of death 2026
    "prop19_exclusion": 1_044_586,           # boe_nr2502, 16 Feb 2025 - 15 Feb 2027
    "prop19_prior_exclusion": 1_022_600,     # boe_nr2502, prior period
    "ca_top_rate": 0.1230,                   # ftb_rates_2026, Schedule X/Y/Z top bracket
    "ca_mhst_rate": 0.0100,                  # rtc_17043
    "ca_mhst_threshold": 1_000_000,          # rtc_17043
    "fed_ltcg_top": 0.2000,                  # irs_p551 / Topic 409, top long-term rate
    "fed_niit": 0.0380,                      # irs_niit
    "fed_unrecaptured_1250": 0.2500,         # irs_p527, maximum rate on unrecaptured 1250 gain
    "prop13_cap": 0.0200,                    # boe_prop13, Cal. Const. art XIII A
    "prop13_base_levy": 0.0100,              # boe_prop13
    "scc_retirement_levy": 0.0003880,        # scc_trb, countywide retirement levy
    "sec121_single": 250_000,                # irs_p523
    "sec121_joint": 500_000,                 # irs_p523
    "sf_mh_base": 249,                       # sf_vip_2026, multifamily parcel, FY2027-28
    "sf_mh_adder": 0.195,                    # sf_vip_2026, per sq ft over 5,000
    "sf_mh_sqft_threshold": 5_000,           # sf_vip_2026
    "sf_mh_cap": 50_000,                     # sf_vip_2026, multifamily cap
    "sf_mh_term_start": 2027,                # sf_vip_2026, 1 Jul 2027
    "sf_mh_term_end": 2042,                  # sf_vip_2026, 30 Jun 2042
}

# ---------------------------------------------------------------------------
# 6. Owner inputs — unverified. Supplied by the household, confirmed by no official page.
#    Where a value can be tied to one specific parcel through a public record (an assessed
#    value), it is coarsened before it reaches a published page; the working figure used by
#    the model is the banded anchor and the reason is recorded as flag F03.
# ---------------------------------------------------------------------------
OWNER = {
    # --- Property A: the future trust inheritance, Santa Clara County -------------------
    "A_value_2026": 3_100_000,           # owner estimate, Nov 2026
    "A_value_band": (2_790_000, 3_410_000),   # +/- 10%, this desk's range convention
    "A_assessed_anchor": 550_000,        # banded; exact figure withheld as a public record
    "A_assessed_note": "banded to the nearest $50,000",
    "A_tax_2025": 7_210,                 # owner's 2025 bill, rounded to $10
    "A_water_low": 1_200,                # $100/mo x 12
    "A_water_high": 1_800,               # $150/mo x 12
    "A_solar_credit_low": 120,           # $10/mo x 12, a credit against electricity
    "A_solar_credit_high": 240,          # $20/mo x 12
    "A_insurance": None,                 # not obtained: see flag F06
    "A_maintenance_pct": (0.005, 0.010, 0.015),  # low / base / high of value per year
    # --- Property B: already owned, San Francisco County ---------------------------------
    "B_value_2026": 1_800_000,           # owner estimate, Nov 2026
    "B_value_band": (1_620_000, 1_980_000),
    "B_assessed_anchor": 125_000,        # banded
    "B_assessed_note": "banded to the nearest $25,000",
    "B_tax_2025": 2_440,                 # owner's 2025 bill, rounded to $10
    "B_rent_2_units_month": 7_150,       # owner: two of three units let
    "B_units": 3,
    "B_units_let": 2,
    "B_water_low": 3_960,                # $330/mo x 12
    "B_water_high": 4_800,               # $400/mo x 12
    "B_power_low": 360,                  # $30/mo x 12
    "B_power_high": 840,                 # $70/mo x 12
    "B_insurance": None,                 # not obtained: see flag F06
    "B_maintenance_pct": (0.008, 0.013, 0.020),
    # --- the estate ---------------------------------------------------------------------
    "estate_other_assets": None,         # not disclosed: see flag F08
    "transfer_years": (2040, 2045, 2050),
}

# ---------------------------------------------------------------------------
# 7. Regimes: how the 1976-2025 record is grouped for the narrative tables.
#    The grouping is this desk's own reading of the official series; the measured
#    averages inside each regime are computed from the transcriptions above, not assumed.
# ---------------------------------------------------------------------------
REGIMES = [
    (1976, 1981, "Great Inflation"),
    (1982, 1999, "Disinflation and the long expansion"),
    (2000, 2012, "Two crashes and a housing bust"),
    (2013, 2019, "Low-inflation expansion"),
    (2020, 2025, "Pandemic shock and the inflation rebound"),
]

HISTORY_START = 1976      # first year with a value in every series
HISTORY_END = 2025
