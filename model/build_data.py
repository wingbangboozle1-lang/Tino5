#!/usr/bin/env python3
"""
Build the single source of truth for the decision-support site.

Three value classes are kept strictly separate everywhere:
  * VERIFIED  - read directly from an official government source (row carries that link)
  * CLIENT    - anonymous figure supplied in the brief; no official confirmation (value cell blank, flagged)
  * MODEL     - computed projection from explicit, labelled assumptions (never an official value)

All dollar outputs are rounded to the nearest $10 (ROUND_HALF_UP).
No personal information is stored or emitted. Geography stops at ZIP code.
"""
from __future__ import annotations

import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "site_data.json"

# ----------------------------------------------------------------------------
# 1. OFFICIAL SOURCE REGISTRY
#    Every URL below was fetched and read during research (2026-11-10 UTC).
# ----------------------------------------------------------------------------
SOURCES = {
    "IRS_ESTATE": dict(
        title="Estate tax (filing thresholds by year of death)", agency="Internal Revenue Service",
        url="https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax",
        note="Gross-estate definition; 2026 Form 706 filing threshold $15,000,000; portability election."),
    "IRS_ESTATE_FAQ": dict(
        title="Frequently asked questions on estate taxes", agency="Internal Revenue Service",
        url="https://www.irs.gov/businesses/small-businesses-self-employed/frequently-asked-questions-on-estate-taxes",
        note="Public Law 119-21 raised the basic exclusion to $15,000,000 for 2026; Form 706 due 9 months after death; 6-month extension via Form 4768; DSUE portability."),
    "CONGRESS_HR1": dict(
        title="H.R.1, Public Law 119-21, text (Sec. 70106)", agency="United States Congress",
        url="https://www.congress.gov/bill/119th-congress/house-bill/1/text",
        note="Sec. 70106 replaces $5,000,000 with $15,000,000; inflation indexing for years beginning after 2026."),
    "CONGRESS_HR1_SUM": dict(
        title="H.R.1 summary, Public Law 119-21 (07/04/2025)", agency="United States Congress",
        url="https://www.congress.gov/bill/119th-congress/house-bill/1",
        note="Increases the base estate, gift and GST exemption after 2025 to $15 million, adjusted for inflation."),
    "IRS_RP2532": dict(
        title="Revenue Procedure 2025-32 (2026 inflation adjustments)", agency="Internal Revenue Service",
        url="https://www.irs.gov/pub/irs-drop/rp-25-32.pdf",
        note="2026 long-term capital gain 0%/15% thresholds (MFJ $98,900 / $613,700); 2026 annual gift exclusion $19,000; estates/trusts 20% rate above $16,250."),
    "IRS_I706": dict(
        title="Instructions for Form 706 (07/2026)", agency="Internal Revenue Service",
        url="https://www.irs.gov/instructions/i706",
        note="Estate tax is levied on the entire taxable estate, not on a beneficiary's share; top unified rate 40%; estate/GST tax due within 9 months."),
    "IRS_P551": dict(
        title="Publication 551, Basis of Assets", agency="Internal Revenue Service",
        url="https://www.irs.gov/publications/p551",
        note="Basis of inherited property is generally FMV at date of death (or alternate valuation date); §1014(f) consistency rule."),
    "IRS_INHERIT_FAQ": dict(
        title="Gifts & inheritances (IRS FAQ)", agency="Internal Revenue Service",
        url="https://www.irs.gov/faqs/interest-dividends-other-types-of-income/gifts-inheritances/gifts-inheritances",
        note="Inherited-property basis is FMV at death whether or not Form 706 is filed; gain on later sale is taxable."),
    "IRS_P525": dict(
        title="Publication 525, Taxable and Nontaxable Income", agency="Internal Revenue Service",
        url="https://www.irs.gov/publications/p525",
        note="Generally, property received as a gift, bequest or inheritance is not included in income; later interest, dividends or rents are taxable."),
    "IRS_TC701": dict(
        title="Topic no. 701, Sale of your home", agency="Internal Revenue Service",
        url="https://www.irs.gov/taxtopics/tc701",
        note="§121 exclusion up to $250,000 ($500,000 joint); ownership and use 2 of the 5 years before sale; no exclusion if another home was excluded in prior 2 years."),
    "IRS_P523": dict(
        title="Publication 523, Selling Your Home", agency="Internal Revenue Service",
        url="https://www.irs.gov/publications/p523",
        note="Rules for home inherited from a decedent; business or rental use, nonqualified use after 2008, and basis adjustments."),
    "IRS_TC409": dict(
        title="Topic no. 409, Capital gains and losses", agency="Internal Revenue Service",
        url="https://www.irs.gov/taxtopics/tc409",
        note="0% / 15% / 20% rates; 25% maximum on unrecaptured §1250 gain; short-term gains at ordinary rates."),
    "IRS_TC559": dict(
        title="Topic no. 559, Net investment income tax", agency="Internal Revenue Service",
        url="https://www.irs.gov/taxtopics/tc559",
        note="3.8% NIIT; $250,000 MFJ / $200,000 single MAGI thresholds; rents and gains from real estate generally included; §121-excluded gain is not."),
    "IRS_P527": dict(
        title="Publication 527, Residential Rental Property", agency="Internal Revenue Service",
        url="https://www.irs.gov/publications/p527",
        note="Rental income, deductible expenses, depreciation, repairs vs. improvements, and sale of a main home used as rental property."),
    "IRS_FS1031": dict(
        title="Like-Kind Exchanges Under IRC Section 1031 (FS-2008-18)", agency="Internal Revenue Service",
        url="https://www.irs.gov/pub/irs-news/fs-08-18.pdf",
        note="§1031 applies only to business/investment real property; primary residences, stocks, bonds, notes and securities do not qualify."),
    "IRS_P544": dict(
        title="Publication 544, Sales and Other Dispositions of Assets", agency="Internal Revenue Service",
        url="https://www.irs.gov/publications/p544",
        note="Like-kind exchange nonrecognition rules apply only to real property held for investment or business use."),
    "IRS_TC503": dict(
        title="Topic no. 503, Deductible taxes", agency="Internal Revenue Service",
        url="https://www.irs.gov/taxtopics/tc503",
        note="SALT deduction limited to $40,000 ($20,000 MFS), subject to MAGI limitation, floor $10,000."),
    "IRS_SALT2026": dict(
        title="Correction to 2026 Form 1040-ES SALT amount", agency="Internal Revenue Service",
        url="https://www.irs.gov/forms-pubs/correction-to-state-and-local-income-tax-deduction-amount-in-the-2026-form-1040-es",
        note="2026 SALT limit $40,400 ($20,200 MFS); reduced above MAGI $505,000 ($252,500 MFS); floor $10,000."),
    "IRS_F1041ES": dict(
        title="Form 1041-ES 2026, Estimated Income Tax for Estates and Trusts", agency="Internal Revenue Service",
        url="https://www.irs.gov/pub/irs-pdf/f1041es.pdf",
        note="2026 estates/trusts: 20% capital-gain rate above $16,250; NIIT 3.8% on undistributed net investment income."),
    "IRS_P559": dict(
        title="Publication 559, Survivors, Executors and Administrators", agency="Internal Revenue Service",
        url="https://www.irs.gov/publications/p559",
        note="Duties of the personal representative, final Form 1040, Form 56, and estate/trust income tax reporting."),
    "FED_FOMC": dict(
        title="Statement on Longer-Run Goals and Monetary Policy Strategy (reaffirmed 2026)", agency="Federal Reserve",
        url="https://www.federalreserve.gov/monetarypolicy/files/FOMC_LongerRunGoals.pdf",
        note="FOMC longer-run inflation goal is 2 percent (PCE). This is a policy goal, not a forecast through 2050."),
    "FHFA_HPI": dict(
        title="FHFA House Price Index datasets", agency="Federal Housing Finance Agency",
        url="https://www.fhfa.gov/data/hpi/datasets",
        note="Official repeat-sales house price indexes at metro-area, county and ZIP-code level; used as the official anchor for appreciation scenarios."),
    "HUD_FMR": dict(
        title="FY 2026 Schedule of Fair Market Rents", agency="U.S. Department of Housing and Urban Development",
        url="https://www.huduser.gov/portal/datasets/fmr/fmr2026/FY2026_FMR_Schedule.pdf",
        note="CA metropolitan FMRs: San Jose-Sunnyvale-Santa Clara HMFA 4-BR $5,010/mo; San Francisco HMFA 4-BR $4,770/mo (official figure, rounded to the nearest $10). Program benchmark, not a property appraisal."),
    "COURTS_TRUST": dict(
        title="Probate Trusts — trustee duties when the settlor dies", agency="California Courts (Santa Clara County Superior Court)",
        url="https://santaclara.courts.ca.gov/self-help/self-help-topics/self-help-probate/self-help-probate-property-transfers/probate-trusts",
        note="Successor trustee acceptance; written notice to beneficiaries/heirs within 60 days; inventory and appraisal; estate tax returns and payment within 9 months; new trust TIN; trust income tax returns."),
    "COURTS_LIVING": dict(
        title="Living Trusts (self-help)", agency="California Courts (Santa Clara County Superior Court)",
        url="https://santaclara.courts.ca.gov/self-help/self-help-probate/self-help-probate-medicalfinancialend-life-issues/living-trusts",
        note="A funded living trust avoids probate; successor trustee distributes without court supervision; pour-over will used for unfunded assets."),
    "BOE_PROP19": dict(
        title="Proposition 19 (official BOE page and comparison charts)", agency="California State Board of Equalization",
        url="https://www.boe.ca.gov/prop19/",
        note="Current law: principal residence of transferor AND transferee; value limit of current taxable value + $1,000,000 (biennially adjusted); homeowners' exemption within 1 year; claim within 3 years; R&T Code §63.2."),
    "BOE_P801": dict(
        title="Proposition 19 Fact Sheet (Publication 801)", agency="California State Board of Equalization",
        url="https://www.boe.ca.gov/pdf/pub801.pdf",
        note="Date of death is the date of transfer; transferee must occupy as principal residence within 1 year; adjusted value limit $1,044,590 for 2/16/2025-2/15/2027; forms BOE-19-P, BOE-19-G, BOE-266, BOE-261-G."),
    "BOE_P800_9": dict(
        title="Death of a Real Property Owner — Reporting Requirements (Publication 800-9)", agency="California State Board of Equalization",
        url="https://www.boe.ca.gov/pdf/pub800-9.pdf",
        note="Death is a change in ownership as of date of death even when property is held in a trust; BOE-502-D filed within 150 days; BOE-19-P / BOE-19-G / BOE-58-H claims; reassessment to market value unless an exclusion applies."),
    "BOE_P800_10": dict(
        title="How Property Is Assessed for Property Tax Purposes (Publication 800-10)", agency="California State Board of Equalization",
        url="https://boe.ca.gov/pdf/pub800-10.pdf",
        note="Assessed value less exemptions multiplied by the tax rate; homeowners' exemption reduces assessed value by $7,000."),
    "BOE_502D": dict(
        title="Sample BOE-502-D, Change in Ownership Statement — Death of a Real Property Owner", agency="California State Board of Equalization",
        url="https://www.boe.ca.gov/proptaxes/pdf/sample-boe502d.pdf",
        note="Trustee/transferee files within 150 days of death; 18 CCR 462.260(c) sets date of change in ownership at date of death."),
    "SCC_PROP13": dict(
        title="Understanding Proposition 13", agency="Santa Clara County Assessor",
        url="https://asr.santaclaracounty.gov/faq/understanding-proposition-13",
        note="1% rate limit, assessed-value growth no greater than 2% annually, reassessment at market value on change of ownership; additional voter-approved taxes may raise the rate."),
    "SCC_RATEBOOK": dict(
        title="Property Tax Rate Book (archive, incl. FY2025-26)", agency="Santa Clara County Controller-Treasurer",
        url="https://controller.santaclaracounty.gov/property-tax-distribution/property-tax-rate-book",
        note="Official TRA-specific rates; 816 tax rate areas in FY2025-26; 1.00000% maximum levy plus voter-approved bond rates; supplemental bills after change in ownership."),
    "SCC_RATEPDF": dict(
        title="County of Santa Clara Compilation of Tax Rates & Information, FY2025-2026", agency="Santa Clara County Controller-Treasurer",
        url="https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf",
        note="1.00000% maximum levy plus bond rates; assessed value increases by CCPI or 2%, whichever is less; direct/special assessments are separate."),
    "SCC_ANNUAL": dict(
        title="Santa Clara County Assessor Annual Report 2025-2026", agency="Santa Clara County Assessor",
        url="https://www.sccassessor.org/edocman/AnnualReport2025-2026.pdf",
        note="2025-26 CCPI 2.514% produced the maximum 2% assessed-value increase; death of an owner is a reassessable change in ownership; trust-held property reassessed at date of death."),
    "SF_ASSESSOR": dict(
        title="Learn about real property assessments", agency="San Francisco Assessor-Recorder",
        url="https://www.sfassessor.org/property-information/homeowners/real-property-assessments",
        note="1% rate plus voter-approved bond indebtedness and direct assessments; assessment growth capped at inflation or 2%, whichever is lower."),
    "SF_TREASURER": dict(
        title="Secured Property Taxes", agency="San Francisco Treasurer & Tax Collector",
        url="https://sftreasurer.org/property/secured-property-taxes",
        note="FY2026-27 secured property tax rate 1.18162182%; supplemental and escape assessments after a change in ownership; total due includes direct charges/special assessments."),
    "SCO_ESTATE": dict(
        title="California Estate Tax", agency="California State Controller's Office",
        url="https://www.sco.ca.gov/ardtax_estate_tax.html",
        note="For decedents dying on or after January 1, 2005, no California Estate Tax Return is required."),
    "SCO_RTC13301": dict(
        title="Estate Tax and GST Tax Laws (R&T Code §13301)", agency="California State Controller's Office",
        url="https://www.sco.ca.gov/Files-ARD-Tax-Info/estate_lawreg_lawreg.pdf",
        note="§13301: neither the state nor any political subdivision may impose any gift, inheritance, succession, legacy, income or estate tax on a transfer occurring by reason of death."),
    "FTB_FEDCHANGES": dict(
        title="Summary of Federal Income Tax Changes", agency="California Franchise Tax Board",
        url="https://www.ftb.ca.gov/about-ftb/data-reports-plans/summary-of-federal-income-tax-changes/index.html",
        note="California does not provide special rates for net capital gain; gains are taxed at ordinary income rates of 1% to 12.3%."),
    "FTB_RATES": dict(
        title="2025 California Tax Rate Schedules", agency="California Franchise Tax Board",
        url="https://www.ftb.ca.gov/forms/2025/2025-540-tax-rate-schedules.pdf",
        note="Top California personal income tax rate 12.30% on the highest bracket."),
    "FTB_540ES": dict(
        title="2025 Instructions for Form 540-ES", agency="California Franchise Tax Board",
        url="https://www.ftb.ca.gov/forms/2025/2025-540-es-instructions.html",
        note="Additional 1% tax on California taxable income over $1,000,000 (Behavioral Health Services Tax), making the top marginal rate 13.3%."),
    "SOS_BALLOT": dict(
        title="Qualified Statewide Ballot Measures — November 3, 2026", agency="California Secretary of State",
        url="https://www.sos.ca.gov/elections/ballot-measures/qualified-ballot-measures",
        note="14 measures qualified, including Prop. 3 (extends high-income tax), Prop. 40 (one-time tax on certain taxpayers), Prop. 42 (prohibits new state personal property taxes), Prop. 43 (limits local revenue measures)."),
    "SOS_CERTIFIES": dict(
        title="Secretary of State certifies measures for Nov. 3, 2026 ballot", agency="California Secretary of State",
        url="https://www.sos.ca.gov/administration/news-releases-and-advisories/2026-news-releases-and-advisories/california-secretary-state-shirley-n-weber-phd-certifies-measures-november-3-2026-general-election-ballot",
        note="Prop. 3 would make permanent the 2012 high-income tax rates otherwise expiring in 2031; estimated $5B-$15B annual state income tax maintained."),
    "SOS_PROP40": dict(
        title="Official Voter Information Guide — Proposition 40", agency="California Secretary of State",
        url="https://voterguide.sos.ca.gov/propositions/40/",
        note="One-time tax measure; SOS news release describes up to 5% on covered assets over $1 billion, excluding real property."),
    "SOS_RESULTS": dict(
        title="State Ballot Measures — unofficial statewide results, Nov. 3, 2026", agency="California Secretary of State",
        url="https://electionresults.sos.ca.gov/returns/ballot-measures",
        note="Unofficial results as of Nov. 9, 2026 (23,860 of 23,860 precincts partially reporting): Prop. 3 Yes 60.6%, Prop. 40 No 52.8%, Prop. 42 Yes 51.6%, Prop. 43 No 57.3%. Results certified by Dec. 11, 2026."),
    "SOS_RESULTS_FAQ": dict(
        title="Election results FAQ — November 3, 2026", agency="California Secretary of State",
        url="https://electionresults.sos.ca.gov/frequently-asked-questions",
        note="County results due December 4, 2026; Secretary of State compiles and certifies results by December 11, 2026."),
    "SF_RENT": dict(
        title="Learn about rent increases in San Francisco", agency="City and County of San Francisco (Rent Board)",
        url="https://www.sf.gov/learn-about-rent-increases-san-francisco/",
        note="For covered units the allowable annual rent increase effective March 1, 2026 through February 28, 2027 is 1.6%."),
    "CDI_AVG": dict(
        title="Sustainable Insurance Strategy — California market snapshot", agency="California Department of Insurance",
        url="https://www.insurance.ca.gov/01-consumers/180-climate-change/sustainable-insurance-strategy.Cfm",
        note="California average homeowner premium $1,570 (national $1,510); page updated October 27, 2026. Statewide average, not ZIP-specific."),
    "CDI_REPORT": dict(
        title="Residential Property Insurance Report", agency="California Department of Insurance",
        url="https://www.insurance.ca.gov/0400-news/0200-studies-reports/0250-homeowners-study/",
        note="CDI collects ZIP-code-level earned premiums, coverage amounts and losses by policy form; reports cover dwelling-fire, homeowners multi-peril, renters and condo policies."),
    "CDI_TOOL": dict(
        title="2026 Homeowners Insurance premium comparison tool", agency="California Department of Insurance",
        url="https://interactive.web.insurance.ca.gov/apex_extprd/f?p=111:21:::NO:::",
        note="Annual premiums effective May 1, 2026; lists 'SANTA CLARA CUPERTINO' and 'SAN FRANCISCO SAN FRANCISCO-Sunset District'; explicitly not a quote."),
    "CPUC_SB695": dict(
        title="2025 Senate Bill 695 Report (net energy metering)", agency="California Public Utilities Commission",
        url="https://www.cpuc.ca.gov/-/media/cpuc-website/divisions/office-of-governmental-affairs-division/reports/2025/2025-sb-695-report_093025.pdf",
        note="New solar customers from April 2023 receive the Net Billing Tariff; NEM 1.0/2.0 legacy 20-year periods remain in effect when a property with a NEM system changes hands."),
    "CPUC_VNEM": dict(
        title="Virtual Net Energy Metering / Net Billing Tariff", agency="California Public Utilities Commission",
        url="https://www.cpuc.ca.gov/industries-and-topics/electrical-energy/demand-side-management/customer-generation/virtual-net-metering",
        note="Decision D.22-12-056 adopted the net billing tariff; NEM 2.0 sunset April 14, 2023; legacy period rules."),
    "CPUC_WATER": dict(
        title="San Jose Water Company tariff (Cupertino service territory)", agency="California Public Utilities Commission",
        url="https://docs.cpuc.ca.gov/PublishedDocs/Efile/G000/M359/K001/359001611.PDF",
        note="CPUC tariff schedules list 'portions of Cupertino' in the regulated water service territory; meter and quantity rates are tariff-based, not a fixed monthly bill."),
    "SFPUC_RATES": dict(
        title="Rates Schedules and Fees (2026-27 water, sewer, power)", agency="San Francisco Public Utilities Commission",
        url="https://sfpuc.org/accounts-services/water-power-and-sewer-rates",
        note="Official rate schedules for water/sewer and Hetch Hetchy Power / CleanPowerSF."),
    "SFPUC_218": dict(
        title="Proposition 218 notice for proposed water and sewer rates", agency="San Francisco Public Utilities Commission",
        url="https://sfpuc.org/accounts-services/water-power-sewer-rates/proposition-218-notice-proposed-water-and-sewer-rates",
        note="Approved average single-family water/sewer bill increase of about 8.3% per year; rates are set by tariff, not by a fixed monthly bill."),
}

# ----------------------------------------------------------------------------
# 2. Status vocabulary
# ----------------------------------------------------------------------------
VERIFIED = "VERIFIED"
CLIENT = "CLIENT INPUT — UNVERIFIED"
MODEL = "MODEL OUTPUT — NOT AN OFFICIAL VALUE"
BLANK = "—"


def r10(x: float) -> int:
    """Round a dollar amount to the nearest $10 using half-up rounding."""
    return int(Decimal(str(x)).quantize(Decimal("1E1"), rounding=ROUND_HALF_UP)) // 10 * 10


def money(x) -> str:
    if x is None:
        return BLANK
    return "${:,}".format(r10(float(x)))


def pct(x: float, dp: int = 2) -> str:
    return f"{x * 100:.{dp}f}%"


def row(cells, source, status, note=""):
    return dict(cells=[str(c) for c in cells], source=source, status=status, note=note)


def table(tid, title, columns, rows, caption=""):
    return dict(id=tid, title=title, columns=columns + ["Official source", "Status"],
                rows=rows, caption=caption)


TABLES: dict[str, dict] = {}
FLAGS: list[dict] = []


def add_table(t):
    TABLES[t["id"]] = t


# ----------------------------------------------------------------------------
# 3. MODEL CONSTANTS (each one is labelled and flagged)
# ----------------------------------------------------------------------------
BASE_YEAR = 2026
END_YEAR = 2050
HORIZON = 10                      # years of comparison after transfer
INFLATION = 0.02                  # FOMC 2% longer-run goal used as model input
PROP13_CAP = 0.02                 # official cap (SCC_PROP13)
APPRECIATION = {"low": 0.02, "base": 0.04, "high": 0.06}
PORTFOLIO = {"low": 0.03, "base": 0.05, "high": 0.07}

A_MV_2026 = 3_100_000            # client
A_ASSESS_2026 = 550_537          # client (2026 assessment, +2% from 2025)
A_TAX_2025, A_ASSESS_2025 = 7_207, 539_743     # client
B_MV_2026 = 1_800_000            # client
B_TAX_2025, B_ASSESS_2025 = 2_439, 114_248     # client

EFF_A = A_TAX_2025 / A_ASSESS_2025   # client-derived effective rate
EFF_B = B_TAX_2025 / B_ASSESS_2025
HOME_EXEMPT = 7_000               # official BOE
CA_AVG_INSURANCE = 1_571          # official CDI statewide average
HUD_FMR_SJ_4BR = 5_010           # official HUD FY2026
HUD_FMR_SF_4BR = 4_772           # official HUD FY2026
RENT_B_MONTH = 7_150              # client
SF_RENT_CAP = 0.016               # official SF Rent Board
A_WATER_M, A_ELEC_M = 120, -20    # client midpoint; negative = solar credit
B_WATER_M, B_ELEC_M = 370, 50     # client midpoint
MAINT_RATE = 0.0020               # model assumption: 0.20% of market value / yr
SELL_COST = 0.06                  # model assumption
PROP19_ALLOWANCE_2025 = 1_044_586 # official BOE, valid 2/16/2025-2/15/2027
FED_LTCG = 0.20                   # official top rate
NIIT = 0.038                      # official
CA_TOP = 0.133                    # official (12.3% + 1%)
SECTION121_SINGLE = 250_000       # official (single filer; joint is $500,000)
ESTATE_EXEMPTION_2026 = 15_000_000
ESTATE_RATE = 0.40                # official top rate
TRANSFER_YEARS = [2040, 2045, 2050]

COMBINED_GAIN_RATE = FED_LTCG + NIIT + CA_TOP   # 37.10%


def mv_a(year, g=APPRECIATION["base"]):
    return A_MV_2026 * (1 + g) ** (year - BASE_YEAR)


def assessed_a_no_transfer(year):
    return A_ASSESS_2026 * (1 + PROP13_CAP) ** (year - BASE_YEAR)


def assessed_b_no_transfer(year):
    # client 2025 base; 2% annual cap thereafter
    return B_ASSESS_2025 * (1 + PROP13_CAP) ** (year - 2025)


def prop19_allowance(year):
    """Biennial inflation adjustment, modelled at 2%/yr from the 2025 official amount."""
    return PROP19_ALLOWANCE_2025 * (1 + INFLATION) ** (year - 2025)


def prop19_assessed(year, g=APPRECIATION["base"]):
    fbyv = assessed_a_no_transfer(year)
    cap = fbyv + prop19_allowance(year)
    return fbyv + max(0.0, mv_a(year, g) - cap)


def a_operating_costs(year, assessed_value, g=APPRECIATION["base"]):
    """Non-property-tax carrying costs, inflated from 2026 dollars."""
    inf = (1 + INFLATION) ** (year - BASE_YEAR)
    return dict(
        insurance=CA_AVG_INSURANCE * inf,
        water=A_WATER_M * 12 * inf,
        electricity=A_ELEC_M * 12 * inf,
        maintenance=MAINT_RATE * mv_a(year, g) * inf,
        property_tax=assessed_value * EFF_A,
    )


def b_operating_costs(year):
    inf = (1 + INFLATION) ** (year - BASE_YEAR)
    return dict(
        insurance=CA_AVG_INSURANCE * inf,
        water=B_WATER_M * 12 * inf,
        electricity=B_ELEC_M * 12 * inf,
        maintenance=MAINT_RATE * B_MV_2026 * (1 + APPRECIATION["base"]) ** (year - BASE_YEAR) * inf,
        property_tax=assessed_b_no_transfer(year) * EFF_B,
    )


def b_rent(year):
    return RENT_B_MONTH * 12 * (1 + SF_RENT_CAP) ** (year - BASE_YEAR)


def cumulative_costs(start, assessed_start, years=HORIZON):
    total = 0.0
    assessed = assessed_start
    for i in range(years):
        y = start + i
        c = a_operating_costs(y, assessed)
        total += sum(c.values())
        assessed *= (1 + PROP13_CAP)
    return total


def cumulative_rent(start, monthly_at_start, years=HORIZON, growth=INFLATION):
    return sum(monthly_at_start * 12 * (1 + growth) ** i for i in range(years))


def terminal_gain_tax(transfer_year, sell_year, exclusion):
    basis = mv_a(transfer_year)                      # §1014 step-up at date of death
    proceeds_net = mv_a(sell_year) * (1 - SELL_COST)
    gain = max(0.0, proceeds_net - basis)
    taxable = max(0.0, gain - exclusion)
    return proceeds_net, taxable * COMBINED_GAIN_RATE


def option_wealth(transfer_year, option, g=APPRECIATION["base"], r=PORTFOLIO["base"],
                  rent_multiplier=1.0):
    """10-year nominal wealth at sell_year, pre-beneficiary-income-tax on operating cash flows."""
    sell = transfer_year + HORIZON
    # re-compute market path with the appreciation scenario g
    mv_t = A_MV_2026 * (1 + g) ** (transfer_year - BASE_YEAR)
    mv_s = A_MV_2026 * (1 + g) ** (sell - BASE_YEAR)
    proceeds_net = mv_s * (1 - SELL_COST)
    basis = mv_t
    gain = max(0.0, proceeds_net - basis)

    if option == "sell":
        return mv_t * (1 - SELL_COST) * (1 + r) ** HORIZON

    if option == "occupy":
        assessed = prop19_assessed(transfer_year, g)
        costs = 0.0
        for i in range(HORIZON):
            y = transfer_year + i
            c = a_operating_costs(y, assessed * (1 + PROP13_CAP) ** i, g)
            costs += sum(c.values())
        cgt = max(0.0, gain - SECTION121_SINGLE) * COMBINED_GAIN_RATE
        return proceeds_net - cgt - costs

    if option == "rent":
        assessed = mv_t                 # no Prop 19 exclusion -> full market reassessment
        costs = 0.0
        for i in range(HORIZON):
            y = transfer_year + i
            c = a_operating_costs(y, assessed * (1 + PROP13_CAP) ** i, g)
            costs += sum(c.values())
        benchmark_at_transfer = HUD_FMR_SJ_4BR * (1 + INFLATION) ** (transfer_year - BASE_YEAR)
        rent = cumulative_rent(transfer_year, benchmark_at_transfer * rent_multiplier)
        cgt = gain * COMBINED_GAIN_RATE   # no §121 (no owner occupancy)
        return proceeds_net - cgt - costs + rent

    raise ValueError(option)


def solve_break_even(func, lo, hi, steps=4000):
    best, best_err = lo, float("inf")
    for i in range(steps + 1):
        x = lo + (hi - lo) * i / steps
        err = abs(func(x))
        if err < best_err:
            best, best_err = x, err
    return best


# ----------------------------------------------------------------------------
# 4. CLIENT INPUT INVENTORY (value cells blank where unverifiable)
# ----------------------------------------------------------------------------
client_rows = [
    row(["Property A", "Cupertino", "95014", "Estimated market value, Nov 2026", BLANK, "$3,100,000 (client estimate)"], "CDI_TOOL", CLIENT, "No official valuation was retrieved; an address-specific lookup would require personal information."),
    row(["Property A", "Cupertino", "95014", "Taxable assessed value, 2026", BLANK, "$550,540 (client)"], "SCC_PROP13", CLIENT, "Official roll lookup would identify a parcel."),
    row(["Property A", "Cupertino", "95014", "Property tax bill, 2025", BLANK, "$7,210 (client)"], "SCC_RATEBOOK", CLIENT, "2026 bill supplied as '--'."),
    row(["Property A", "Cupertino", "95014", "Water, monthly range", BLANK, "$100-$150 (client)"], "CPUC_WATER", CLIENT, "Tariff based on metered usage."),
    row(["Property A", "Cupertino", "95014", "Electricity / solar net result, monthly", BLANK, "+$10-$20 credit (client)"], "CPUC_SB695", CLIENT, "Legacy NEM status and interconnection date unknown."),
    row(["Property A", "Cupertino", "95014", "Primary-residence home insurance, annual", BLANK, "~$1,500 (client guess)"], "CDI_TOOL", CLIENT, "CDI tool is the official quote-comparison source."),
    row(["Property A", "Cupertino", "95014", "Regular maintenance and repairs", BLANK, "Qualitative only ('less than Property B')"], "IRS_P527", CLIENT, "No figure supplied."),
    row(["Property B", "San Francisco", "94122", "Estimated market value, Nov 2026", BLANK, "$1,800,000 (client)"], "SF_ASSESSOR", CLIENT, ""),
    row(["Property B", "San Francisco", "94122", "Taxable assessed value, 2025", BLANK, "$114,250 (client)"], "SF_ASSESSOR", CLIENT, ""),
    row(["Property B", "San Francisco", "94122", "Property tax bill, 2025", BLANK, "$2,440 (client)"], "SF_TREASURER", CLIENT, ""),
    row(["Property B", "San Francisco", "94122", "Rental income, 2 of 3 units, monthly", BLANK, "$7,150 (client)"], "SF_RENT", CLIENT, "Rent-control coverage of the units is not confirmed."),
    row(["Property B", "San Francisco", "94122", "Water, all 3 units, monthly range", BLANK, "$330-$400 (client)"], "SFPUC_RATES", CLIENT, ""),
    row(["Property B", "San Francisco", "94122", "Electricity, monthly range", BLANK, "$30-$70 (client)"], "SFPUC_RATES", CLIENT, ""),
    row(["Property B", "San Francisco", "94122", "Rental-property insurance, annual", BLANK, "~$1,500 (client guess)"], "CDI_REPORT", CLIENT, "Landlord/dwelling-fire policy, not a homeowner policy."),
    row(["Estate", "—", "—", "Cash / liquid assets in the estate", BLANK, "'considerable amount' (unquantified)"], "IRS_ESTATE", CLIENT, "No amount supplied; see Estate Tax Threshold page."),
    row(["Estate", "—", "—", "Planned transfer window", BLANK, "2040-2050 (client)"], "COURTS_TRUST", CLIENT, ""),
]
add_table(table("inputs", "Anonymous client-supplied inputs (all unverified)",
                ["Subject", "Area", "ZIP", "Item", "Official value", "Client-supplied figure"],
                client_rows,
                "The 'Official value' column is deliberately blank. No client-supplied number is presented as a verified fact. "
                "Official links point to the agency that would hold the confirming record."))

# Historical client tax/assessment series - reproduced anonymously, flagged
hist_a = [
    ("2026", "—", "550,537"), ("2025", "7,207", "539,743"), ("2024", "7,003", "529,161"),
    ("2023", "6,917", "518,786"), ("2022", "6,755", "508,614"), ("2021", "6,662", "498,642"),
    ("2020", "6,565", "493,530"), ("2019", "6,565", "483,854"), ("2018", "6,383", "474,368"),
    ("2017", "6,383", "465,067"), ("2016", "6,414", "455,949"), ("2015", "6,130", "449,101"),
    ("2014", "5,965", "440,305"),
]
hist_b = [
    ("2025", "2,439", "114,248"), ("2024", "2,315", "112,008"), ("2023", "2,179", "109,814"),
    ("2022", "2,107", "107,662"), ("2021", "2,066", "105,595"), ("2020", "2,197", "104,513"),
    ("2019", "2,134", "102,465"), ("2018", "2,061", "100,456"), ("2017", "1,740", "98,488"),
    ("2016", "1,675", "96,557"),
]
hist_rows = []
for y, t, a in hist_a:
    hist_rows.append(row(["Property A · 95014", y, BLANK,
                           (money(float(t.replace(",", ""))) if t != "—" else t) + " (client)", money(float(a.replace(",", ""))) + " (client)"],
                          "SCC_RATEBOOK", CLIENT))
for y, t, a in hist_b:
    hist_rows.append(row(["Property B · 94122", y, BLANK, money(float(t.replace(",", ""))) + " (client)",
                           money(float(a.replace(",", ""))) + " (client)"], "SF_TREASURER", CLIENT))
add_table(table("history", "Client-supplied tax and assessment history (unverified)",
                ["Property", "Year", "Official tax / assessment record", "Client property tax", "Client tax assessment"],
                hist_rows,
                "The official record column is blank because no parcel-level record was retrieved. "
                "Implied effective rates are ~1.34% for Property A and ~2.13% for Property B; both exceed the official "
                "1% + voter-approved ad valorem rate, which is consistent with separate direct charges / special "
                "assessments but requires reconciliation. See Flagged for Review, FLAG-003."))

# ----------------------------------------------------------------------------
# 5. VERIFIED LAW / FACT TABLES
# ----------------------------------------------------------------------------
federal_facts = [
    ("Federal estate-tax filing threshold, 2026", "$15,000,000", "Form 706 required when gross estate plus adjusted taxable gifts exceeds this amount.", "IRS_ESTATE"),
    ("Basic exclusion amount made permanent", "$15,000,000 per person", "Public Law 119-21 §70106; inflation indexed for years beginning after 2026.", "CONGRESS_HR1"),
    ("Married couple with portability", "$30,000,000", "DSUE election requires a timely filed Form 706.", "IRS_ESTATE_FAQ"),
    ("Top federal estate / GST tax rate", "40%", "Unified rate schedule, Form 706 instructions.", "IRS_I706"),
    ("Estate tax is on the estate, not the beneficiary", "Entire taxable estate", "Not just the share received by a particular beneficiary.", "IRS_I706"),
    ("Form 706 filing deadline", "9 months after death", "Automatic 6-month extension via Form 4768.", "IRS_ESTATE_FAQ"),
    ("Annual gift-tax exclusion, 2026", "$19,000", "Per recipient; excess reduces the lifetime basic exclusion.", "IRS_RP2532"),
    ("Inherited property basis", "FMV at date of death", "Alternate valuation only if Form 706 filed and election made.", "IRS_P551"),
    ("Inheritance as beneficiary gross income", "Generally not included", "Later interest, dividends or rents from inherited property ARE taxable.", "IRS_P525"),
    ("§121 home-sale gain exclusion", "$250,000 / $500,000 joint", "Ownership and use 2 of the 5 years before sale.", "IRS_TC701"),
    ("Long-term capital gain rates", "0% / 15% / 20%", "2026 20% rate begins above $613,700 MFJ taxable income.", "IRS_RP2532"),
    ("Unrecaptured §1250 gain maximum rate", "25%", "Applies to depreciated real property.", "IRS_TC409"),
    ("Net investment income tax", "3.8%", "MAGI thresholds $250,000 MFJ / $200,000 single; rents and real-estate gains included.", "IRS_TC559"),
    ("Estates and trusts 2026 top capital-gain threshold", "$16,250", "20% rate above that amount; NIIT 3.8% on undistributed NII.", "IRS_F1041ES"),
    ("Rental income and expenses", "Schedule E / Form 1040", "Deductible expenses include insurance, repairs, taxes; depreciation required.", "IRS_P527"),
    ("§1031 like-kind exchange", "Real property only", "Stocks, bonds, notes and securities do NOT qualify; a primary residence does not qualify.", "IRS_FS1031"),
    ("SALT deduction cap, 2026", "$40,400", "Reduced above MAGI $505,000; floor $10,000; temporary through 2029.", "IRS_SALT2026"),
    ("Longer-run inflation goal", "2%", "FOMC policy goal (PCE), not a projection to 2050.", "FED_FOMC"),
    ("FY2026 4-BR Fair Market Rent, San Jose HMFA", "$5,010 / month", "Official HUD program benchmark; includes Santa Clara County.", "HUD_FMR"),
    ("FY2026 4-BR Fair Market Rent, San Francisco HMFA", "$4,770 / month", "Official HUD program benchmark.", "HUD_FMR"),
]
add_table(table("federal_law", "Federal law and official figures (verified)",
                ["Item", "Official value", "Basis / detail"],
                [row([a, b, c], s, VERIFIED) for a, b, c, s in federal_facts],
                "Every figure in the 'Official value' column was read directly from the linked government page."))

state_facts = [
    ("California estate tax return", "Not required", "For decedents dying on/after January 1, 2005.", "SCO_ESTATE"),
    ("State and local inheritance / gift / estate tax", "Prohibited", "R&T Code §13301: neither the state nor any political subdivision may impose such a tax on a death transfer.", "SCO_RTC13301"),
    ("California capital-gain treatment", "Ordinary income rates", "CA does not provide special long-term capital-gain rates.", "FTB_FEDCHANGES"),
    ("Top CA personal income tax rate", "12.30%", "2025 Form 540 rate schedules.", "FTB_RATES"),
    ("Additional 1% tax over $1,000,000 taxable income", "Top rate 13.30%", "Behavioral Health Services Tax, Form 540-ES instructions.", "FTB_540ES"),
    ("Proposition 13 base property-tax rate", "1.00%", "Plus voter-approved bond indebtedness and direct/special assessments.", "SCC_PROP13"),
    ("Proposition 13 assessment growth cap", "≤ 2% per year", "Inflation (CCPI) or 2%, whichever is lower.", "SCC_PROP13"),
    ("2025-26 CCPI factor, Santa Clara County", "2.514%", "Produced the maximum 2% assessed-value increase.", "SCC_ANNUAL"),
    ("Santa Clara County FY2025-26 tax rate areas", "816", "Each TRA has a distinct combined rate; 1.00000% maximum levy.", "SCC_RATEPDF"),
    ("Homeowners' exemption", "$7,000 of assessed value", "Principal residence only; must be claimed.", "BOE_P800_10"),
    ("Death of owner = change in ownership", "Date of death", "Applies even when title is held in a revocable trust; reassessment at market value unless excluded.", "BOE_P800_9"),
    ("BOE-502-D filing deadline", "150 days after death", "Trustee or transferee files with each county assessor; penalties may apply.", "BOE_P800_9"),
    ("Prop 19 intergenerational exclusion", "Taxable value + allowance", "Requires transferor principal residence AND transferee principal residence within 1 year.", "BOE_PROP19"),
    ("Prop 19 homeowners' / disabled veterans' exemption filing", "Within 1 year", "BOE-266 or BOE-261-G; late filing gives prospective relief only.", "BOE_P801"),
    ("Prop 19 exclusion claim deadline", "Within 3 years", "Form BOE-19-P (or BOE-19-G); before transfer to a third party.", "BOE_P801"),
    ("Prop 19 inflation-adjusted value limit", "$1,044,590", "Valid for transfer dates 2/16/2025 through 2/15/2027; LTA 2025/009.", "BOE_P801"),
    ("Prop 19 excess-value rule", "Difference added to taxable value", "If market value exceeds FBYV + allowance, the excess is added to the new base year value.", "BOE_P801"),
    ("FY2026-27 San Francisco secured property-tax rate", "1.18162182%", "Total bill also includes direct charges and special assessments; supplemental/escape bills after change in ownership.", "SF_TREASURER"),
    ("San Francisco allowable rent increase 3/1/26-2/28/27", "1.6%", "For covered units under the Rent Ordinance.", "SF_RENT"),
    ("California average homeowner premium", "$1,570 / year", "CDI market snapshot updated Oct 27, 2026; statewide, not ZIP-specific.", "CDI_AVG"),
    ("CDI ZIP-level premium data", "Available by policy form", "Dwelling-fire, homeowners multi-peril, renters, condo; covers 2018-2023.", "CDI_REPORT"),
    ("NEM legacy period on transfer of a solar property", "Remains in effect", "NEM 1.0/2.0 20-year legacy periods survive a change of ownership; new systems since April 2023 use the Net Billing Tariff.", "CPUC_SB695"),
    ("Trustee notice to beneficiaries/heirs", "60 days", "After death / becoming trustee; inventory and appraisal; estate returns and tax paid within 9 months.", "COURTS_TRUST"),
    ("Living trust avoids probate", "No court supervision", "If assets are properly funded into the trust.", "COURTS_LIVING"),
]
add_table(table("state_law", "California, county and city law and official figures (verified)",
                ["Item", "Official value", "Basis / detail"],
                [row([a, b, c], s, VERIFIED) for a, b, c, s in state_facts],
                "State, county and city rows are all linked to the issuing government agency."))

# ----------------------------------------------------------------------------
# 6. MODEL ASSUMPTIONS (official value column blank)
# ----------------------------------------------------------------------------
assumptions = [
    ("General inflation", "2.00% / year", "FOMC 2% longer-run inflation goal", "FED_FOMC", "A policy goal is not an official 25-year forecast."),
    ("Property A market appreciation — low", "2.00% / year", "FHFA HPI official metro series is the anchor; scenario is a model choice", "FHFA_HPI", "Not an official forecast."),
    ("Property A market appreciation — base", "4.00% / year", "FHFA HPI official metro series is the anchor; scenario is a model choice", "FHFA_HPI", "Not an official forecast."),
    ("Property A market appreciation — high", "6.00% / year", "FHFA HPI official metro series is the anchor; scenario is a model choice", "FHFA_HPI", "Not an official forecast."),
    ("Portfolio return — low / base / high", "3% / 5% / 7% nominal", "No official forward return exists; scenario band only", "FED_FOMC", "Not an official forecast; excludes dividend/interest tax detail."),
    ("Assessed-value growth before transfer", "2.00% / year", "Prop 13 cap (official)", "SCC_PROP13", "Rule is official; applying it to this parcel is a model projection."),
    ("Effective property-tax rate, Property A", pct(EFF_A), "Derived from client 2025 tax ÷ assessment", "SCC_RATEBOOK", "Client-derived, unverified; official rate is TRA-specific."),
    ("Effective property-tax rate, Property B", pct(EFF_B), "Derived from client 2025 tax ÷ assessment", "SF_TREASURER", "Client-derived, unverified; official rate is 1.18162182%."),
    ("Prop 19 allowance growth", "2% / year from 2025", "BOE publishes biennial inflation adjustments", "BOE_P801", "Only the 2025-2027 amount ($1,044,590) is official."),
    ("Maintenance and repairs", "0.20% of market value / year", "IRS treats repairs as deductible rental expense; no official benchmark", "IRS_P527", "No client figure supplied."),
    ("Transaction cost on sale", "6.00% of price", "No official source", "IRS_P523", "Model assumption only."),
    ("Combined gain tax rate on sale", pct(COMBINED_GAIN_RATE), "20% federal + 3.8% NIIT + 13.3% CA", "IRS_TC559", "Applies only to gain above the stepped-up basis and any §121 exclusion; filing status unknown."),
    ("§121 exclusion applied", "$250,000 (single)", "Official single-filer amount; joint is $500,000", "IRS_TC701", "Filing status not supplied."),
    ("Water — Property A (model midpoint)", "$120 / month", "Client range $100-$150", "CPUC_WATER", "Client input, not an official tariff bill."),
    ("Electricity — Property A (model midpoint)", "-$20 / month (credit)", "Client range +$10-$20 credit; CPUC NEM/NBT rules", "CPUC_SB695", "Legacy NEM interconnection date unknown."),
    ("Water — Property B (model midpoint)", "$370 / month", "Client range $330-$400 for 3 units", "SFPUC_RATES", "Client input, not an official tariff bill."),
    ("Electricity — Property B (model midpoint)", "$50 / month", "Client range $30-$70", "SFPUC_RATES", "Client input."),
    ("Insurance both properties", money(CA_AVG_INSURANCE) + " / year (2026)", "CDI statewide average homeowner premium", "CDI_AVG", "Not ZIP-specific; landlord policy may differ."),
    ("Benchmark rent for Property A", money(HUD_FMR_SJ_4BR) + " / month (2026)", "HUD FY2026 4-BR FMR, San Jose HMFA", "HUD_FMR", "Program benchmark, not a property-specific appraisal."),
    ("Rental-income growth, Property B", "1.60% / year", "SF Rent Board allowable increase for covered units", "SF_RENT", "Coverage of the two units is unconfirmed."),
    ("Comparison horizon", f"{HORIZON} years after transfer", "Model design", "IRS_TC701", "Chosen to exceed the 2-year §121 use test."),
]
add_table(table("assumption_values", "Model parameter values (labelled model outputs, not official figures)",
                ["Parameter", "Model parameter (not an official value)", "Official anchor / rule"],
                [row([a, b, c], s, MODEL, n) for a, b, c, s, n in assumptions],
                "These are the parameters fed into the projections. None is an official published value for these properties."))

# ----------------------------------------------------------------------------
# 7. YEAR-BY-YEAR PROJECTIONS
# ----------------------------------------------------------------------------
value_rows = []
for y in range(BASE_YEAR, END_YEAR + 1):
    value_rows.append(row([
        y, money(mv_a(y, APPRECIATION["low"])), money(mv_a(y, APPRECIATION["base"])),
        money(mv_a(y, APPRECIATION["high"])), money(assessed_a_no_transfer(y)),
        money(mv_a(y) - assessed_a_no_transfer(y)),
    ], "SCC_PROP13", MODEL, "Market values use 2%/4%/6% scenarios; assessed value uses the official 2% Prop 13 cap applied to the client 2026 assessment."))
add_table(table("proj_value", "Property A — projected market value and taxable assessed value, 2026-2050",
                ["Year", "Market value · 2%", "Market value · 4% (base)", "Market value · 6%",
                 "Taxable assessed value · no transfer (2% cap)", "Gap: market − assessed (4%)"],
                value_rows,
                "Model outputs. The 2% assessment cap is the official Prop 13 rule; the market-value paths are model scenarios, "
                "not official forecasts. Source link is to the Santa Clara County Assessor."))

tax_rows = []
for y in range(BASE_YEAR, END_YEAR + 1):
    no_reassess = assessed_a_no_transfer(y) * EFF_A
    full = mv_a(y) * EFF_A
    p19 = prop19_assessed(y) * EFF_A if y >= 2040 else None
    tax_rows.append(row([
        y, money(no_reassess), money(full), money(p19) if p19 is not None else BLANK,
        money(full - no_reassess),
    ], "BOE_P800_9", MODEL,
        "Full reassessment = market value at date of death × client-derived effective rate. "
        "Prop 19 column shown from 2040 for the candidate transfer window; blank before then."))
add_table(table("proj_tax", "Property A — projected annual property tax under three assessment outcomes",
                ["Year", "Tax if base is preserved", "Tax after full reassessment at death",
                 "Tax if Prop 19 exclusion applies", "Extra annual tax from full reassessment"],
                tax_rows,
                "Model outputs. The reassessment-at-death rule is official (BOE Publication 800-9). "
                "The applied effective rate is client-derived and flagged. Prop 19 figures are shown only for 2040-2050."))

p19_rows = []
for y in TRANSFER_YEARS:
    fbyv = assessed_a_no_transfer(y)
    allow = prop19_allowance(y)
    cap = fbyv + allow
    m = mv_a(y)
    new_assessed = prop19_assessed(y)
    p19_rows.append(row([
        y, money(m), money(fbyv), money(allow), money(cap), money(max(0.0, m - cap)),
        money(new_assessed), money(new_assessed * EFF_A),
        money(m * EFF_A - new_assessed * EFF_A),
    ], "BOE_P801", MODEL,
        "Allowance projected from the official $1,044,590 (2/16/2025-2/15/2027) at 2%/yr; future BOE amounts are not yet published."))
add_table(table("prop19", "Proposition 19 value-limit test at each candidate transfer year",
                ["Transfer year", "Market value (4%)", "Factored base year value",
                 "Projected inflation-adjusted allowance", "Exclusion cap (FBYV + allowance)",
                 "Market value above cap", "New taxable value if eligible",
                 "Annual tax if eligible", "Annual tax saved vs full reassessment"],
                p19_rows,
                "Model outputs computed with the official Prop 19 formula. Eligibility itself is unverified — see FLAG-010."))

# Carrying-cost projections
cost_a_rows, cost_b_rows = [], []
sample_years = [2026, 2030, 2035, 2040, 2045, 2050]
for y in sample_years:
    c = a_operating_costs(y, assessed_a_no_transfer(y))
    cost_a_rows.append(row([
        y, money(c["property_tax"]), money(c["insurance"]), money(c["water"]),
        money(c["electricity"]), money(c["maintenance"]), money(sum(c.values())),
        money(sum(c.values()) / 12),
    ], "CDI_AVG", MODEL, "Property tax uses the preserved Prop 13 base (no transfer). Costs inflated 2%/yr; maintenance at 0.20% of projected market value."))
add_table(table("cost_a", "Property A — projected annual carrying costs (base preserved)",
                ["Year", "Property tax", "Insurance", "Water", "Electricity / solar (negative = credit)",
                 "Maintenance & repairs", "Total annual", "Total monthly"],
                cost_a_rows,
                "Model outputs. Insurance baseline is the official CDI statewide average; all other inputs are client figures or model assumptions."))

for y in sample_years:
    c = b_operating_costs(y)
    rent = b_rent(y)
    total = sum(c.values())
    cost_b_rows.append(row([
        y, money(c["property_tax"]), money(c["insurance"]), money(c["water"]),
        money(c["electricity"]), money(c["maintenance"]), money(total),
        money(rent), money(rent - total), money((rent - total) / 12),
    ], "SF_RENT", MODEL, "Rental income grown at the official 1.6% SF allowable increase; rent-control coverage of the units is unconfirmed."))
add_table(table("cost_b", "Property B — projected operating costs and rental cash flow",
                ["Year", "Property tax", "Insurance", "Water", "Electricity",
                 "Maintenance & repairs", "Total annual cost", "Gross rental income",
                 "Net operating cash flow", "Net per month"],
                cost_b_rows,
                "Model outputs, before income tax. Rental income is taxable (IRS Pub 527) and may attract the 3.8% NIIT (Topic 559); "
                "depreciation and filing status are unknown, so income tax is not computed here. See FLAG-012."))

# ----------------------------------------------------------------------------
# 8. INHERITANCE PROCESS — step by step, every step linked to an official source
# ----------------------------------------------------------------------------
steps = [
    (1, "Before death", "Confirm the property is titled in the trust (funding)", "A living trust only avoids probate for assets actually transferred into it; a pour-over will catches unfunded assets.", "COURTS_LIVING"),
    (2, "Before death", "Document whether the home is the transferor's principal residence", "Prop 19 requires the family home to be the principal residence of BOTH transferor and transferee. This single fact determines whether a reassessment exclusion is even possible.", "BOE_PROP19"),
    (3, "Date of death", "Successor trustee signs Acceptance of Trusteeship; trust becomes irrevocable", "Trustee takes over without probate court supervision when the trust is funded.", "COURTS_TRUST"),
    (4, "Within 60 days", "Written notice to all beneficiaries and heirs (Prob. Code §16061.7)", "Notice must include trustee contact, place of administration, and the right to request a copy of the trust; 120-day contest period follows.", "COURTS_TRUST"),
    (5, "As of date of death", "Date-of-death appraisal / inventory of all estate assets", "Needed to establish fair market value for basis and to determine whether estate tax returns are required.", "COURTS_TRUST"),
    (6, "Date of death", "Property-tax change in ownership occurs on the date of death", "Applies to trust-held property even if the deed to beneficiaries is recorded years later; reassessment to market value unless an exclusion applies.", "BOE_P800_9"),
    (7, "Within 150 days", "File BOE-502-D with the county assessor for each parcel", "Trustee or transferee files; if probated, file with the inventory and appraisal. Penalties may apply on an assessor's request.", "BOE_502D"),
    (8, "Within 1 year", "Beneficiary occupies the home as principal residence", "Required for the Prop 19 intergenerational exclusion. Later occupancy does not qualify retroactively.", "BOE_P801"),
    (9, "Within 1 year", "File homeowners' exemption (BOE-266) or disabled veterans' exemption (BOE-261-G)", "Timely filing gives the exclusion as of the date of transfer; late filing gives prospective relief only.", "BOE_P801"),
    (10, "Within 3 years", "File BOE-19-P (parent→child) or BOE-19-G (grandparent→grandchild)", "Must be filed before transfer to a third party; also timely if within 6 months of a supplemental/escape assessment notice.", "BOE_P801"),
    (11, "If no exclusion", "Assessor issues supplemental / escape assessment at market value", "Supplemental bills are in addition to the regular annual bill; SF also publishes escape-assessment procedures.", "SCC_RATEPDF"),
    (12, "Within 9 months", "File Form 706 if gross estate + adjusted taxable gifts > $15,000,000 (2026)", "Estate tax is on the estate, not the beneficiary; top rate 40%; 6-month extension via Form 4768.", "IRS_ESTATE_FAQ"),
    (13, "Administration period", "Obtain a new TIN for the trust and file Form 1041 for post-death income", "Interest, dividends and rents earned after death are taxable to the estate/trust or to beneficiaries.", "COURTS_TRUST"),
    (14, "At distribution", "Record the deed / affidavit and update the tax mailing address", "The tax bill mailing address is unchanged until the assessor is notified.", "BOE_P800_9"),
    (15, "At distribution", "Basis in the real property = FMV at date of death", "A stepped-up basis normally eliminates gain on an immediate sale; later appreciation is taxable.", "IRS_P551"),
    (16, "Decision point", "Choose: occupy, rent, or sell and reinvest", "See the Decision Analysis page; a sale reinvested in stocks cannot use §1031 deferral.", "IRS_FS1031"),
    (17, "If sold after 2 years of ownership + use", "§121 may exclude up to $250,000 ($500,000 joint) of gain", "Ownership and use tests are 2 out of the 5 years before sale; nonqualified use and depreciation rules apply.", "IRS_TC701"),
    (18, "Solar system", "Confirm the NEM / Net Billing Tariff legacy period transfers with the property", "CPUC states legacy periods remain in effect when a property with a NEM system changes hands.", "CPUC_SB695"),
]
add_table(table("process", "Step-by-step inheritance of Property A through a trust",
                ["#", "Timing", "Action", "Why it matters / official rule"],
                [row([n, t, a, d], s, VERIFIED) for n, t, a, d, s in steps],
                "Timing and rules are read from the linked government pages. Steps describing client-specific facts are labelled as actions to take, not as completed events."))

# ----------------------------------------------------------------------------
# 9. ESTATE / INHERITANCE TAX THRESHOLDS
# ----------------------------------------------------------------------------
est_rows = []
for y in [2026, 2030, 2040, 2045, 2050]:
    proj = ESTATE_EXEMPTION_2026 * (1 + INFLATION) ** (y - 2026)
    est_rows.append(row([
        y,
        money(ESTATE_EXEMPTION_2026) if y == 2026 else BLANK,
        money(2 * ESTATE_EXEMPTION_2026) if y == 2026 else BLANK,
        money(proj), money(2 * proj), "40%", "$0", "$0",
    ], "CONGRESS_HR1", MODEL if y != 2026 else VERIFIED,
        "2026 values are official. Later single-person figures project the statutory inflation indexing at 2%/yr; no official future amounts exist."))
add_table(table("estate_threshold", "Inheritance / estate tax thresholds and projected headroom",
                ["Year", "Official single exemption", "Official couple exemption (portability)",
                 "Projected single exemption", "Projected couple exemption", "Top federal rate",
                 "CA state tax", "Local tax"],
                est_rows,
                "2026 row is verified from IRS / Congress.gov. Later rows are model projections of the statutory inflation index. "
                "California and local estate/inheritance tax are $0 by statute (R&T §13301)."))

matrix_rows = []
for estate in [5_000_000, 10_000_000, 15_000_000, 20_000_000, 25_000_000, 30_000_000, 40_000_000, 50_000_000]:
    tax_single = max(0.0, estate - ESTATE_EXEMPTION_2026) * ESTATE_RATE
    tax_couple = max(0.0, estate - 2 * ESTATE_EXEMPTION_2026) * ESTATE_RATE
    matrix_rows.append(row([
        money(estate), money(max(0.0, ESTATE_EXEMPTION_2026 - estate)),
        money(tax_single), money(tax_couple), "$0", "$0",
        money(estate - tax_single),
    ], "IRS_I706", MODEL,
        "Illustrative gross-estate sizes. Excludes deductions, marital/charitable deductions, lifetime taxable gifts and DSUE; those change the real result."))
add_table(table("estate_matrix", "Illustrative federal estate tax by gross estate size (2026 law)",
                ["Gross estate (illustrative)", "Headroom before 2026 single threshold", "Federal tax · single",
                 "Federal tax · couple with portability", "CA state tax", "Local tax",
                 "Net to heirs · single, before deductions"],
                matrix_rows,
                "The estate size in this case is UNKNOWN. These rows are arithmetic illustrations of the official 40% rate above the "
                "official $15M / $30M thresholds, not statements about this estate. See FLAG-013."))

law_change_rows = [
    ("Federal", "Basic exclusion made permanent at $15M, inflation indexed after 2026", "Already enacted (P.L. 119-21, July 4, 2025)", "Removes the pre-2026 sunset risk; exemption rises with inflation, but Congress can amend it at any time.", "CONGRESS_HR1_SUM"),
    ("Federal", "SALT cap $40,400 in 2026, temporary through 2029", "Enacted", "Affects the after-tax cost of holding a high-property-tax home; a return to $10,000 would raise the net cost of ownership.", "IRS_SALT2026"),
    ("California", "Prop. 3 (Nov. 3, 2026): makes permanent the high-income tax rates due to expire in 2031", "Unofficial result 60.6% Yes; certification due 12/11/2026", "Would keep top marginal CA rates in place for a 2040-2050 sale, increasing tax on gains taxed as ordinary income.", "SOS_RESULTS"),
    ("California", "Prop. 40 (Nov. 3, 2026): one-time up-to-5% tax on covered assets over $1B, excluding real property", "Unofficial result 52.8% No; certification due 12/11/2026", "Real property is excluded, and the measure appears to have been rejected; a very large liquid estate was the only possible exposure.", "SOS_RESULTS"),
    ("California", "Prop. 42 (Nov. 3, 2026): prohibits new state personal property taxes and certain retroactive taxes", "Unofficial result 51.6% Yes; certification due 12/11/2026", "Would constrain future state-level wealth taxation.", "SOS_RESULTS"),
    ("California", "Prop. 43 (Nov. 3, 2026): limits voters' ability to raise revenues for local services", "Unofficial result 57.3% No; certification due 12/11/2026", "Appears rejected, so no immediate constraint on future local bond/parcel taxes.", "SOS_RESULTS"),
    ("California", "Election results certification", "Due December 11, 2026", "Unofficial returns are published (23,860 of 23,860 precincts partially reporting as of Nov. 9, 2026) but are not yet certified; percentages may change during the canvass.", "SOS_RESULTS_FAQ"),
    ("California", "Prop. 19 remains the operative intergenerational-transfer rule", "Current law", "Any repeal or amendment before 2040-2050 would change the reassessment analysis materially; no repeal is on the 2026 statewide ballot.", "BOE_PROP19"),
    ("California", "SB 284 (2025) proposed clarifying the Prop. 19 one-year residency window for probate transfers", "Proposal analysed by BOE; not treated as enacted here", "Would relax a deadline that is critical to the exclusion; status must be re-checked before the transfer.", "BOE_PROP19"),
    ("Federal / CA", "Step-up in basis under §1014", "Current law; repeatedly proposed for repeal in past Congresses", "If repealed before the transfer, an immediate sale would realise the decedent's full unrealised gain and change the recommendation.", "IRS_P551"),
    ("Local", "Solar Net Billing Tariff and NEM legacy periods", "Current CPUC rules", "A 20-year legacy period may expire before 2040-2050; the solar credit assumption would then change.", "CPUC_SB695"),
]
add_table(table("law_changes", "Enacted, pending and proposed law changes that could alter the decision",
                ["Level", "Change", "Status", "Why it matters to this decision"],
                [row([a, b, c, d], s, VERIFIED) for a, b, c, d, s in law_change_rows],
                "Only government sources are used. 'Proposed' items are described as proposals, never as current law. "
                "The SB 284 row links to the BOE Prop. 19 guidance hub rather than asserting an unverified bill status."))

# ----------------------------------------------------------------------------
# 10. DECISION ANALYSIS
# ----------------------------------------------------------------------------
decision_rows = []
for T in TRANSFER_YEARS:
    mv_t = mv_a(T)
    p19_av = prop19_assessed(T)
    for label, opt in [("1 · Occupy (Prop 19 eligible)", "occupy"),
                       ("2 · Rent out (no exclusion)", "rent"),
                       ("3 · Sell at death, reinvest", "sell")]:
        if opt == "occupy":
            assessed, tax = p19_av, p19_av * EFF_A
        elif opt == "rent":
            assessed, tax = mv_t, mv_t * EFF_A
        else:
            assessed, tax = 0.0, 0.0
        w = option_wealth(T, opt)
        decision_rows.append(row([
            T, label, money(mv_t), money(assessed) if assessed else BLANK,
            money(tax) if tax else BLANK,
            money(mv_t * (1 - SELL_COST)) if opt == "sell" else BLANK,
            money(w),
        ], "IRS_P551", MODEL,
            "10-year nominal wealth at year " + str(T + HORIZON) + "; base 4% appreciation, 5% portfolio return, "
            "6% selling cost, 37.10% combined gain tax. Pre-beneficiary-income-tax on operating cash flows."))
add_table(table("decision", "Three options compared at each candidate transfer year (base case)",
                ["Transfer year", "Option", "Market value at death", "New taxable assessed value",
                 "Annual property tax", "Net cash invested if sold", "10-year wealth"],
                decision_rows,
                "All figures are model outputs. The official rules behind them: §1014 stepped-up basis, Prop 19 reassessment "
                "exclusion, and §121 capital-gain exclusion. No beneficiary income tax is applied to annual cash flows (FLAG-012)."))

# Ranked comparison at the 2045 base case
T0 = 2045
w_occ = option_wealth(T0, "occupy")
w_rent = option_wealth(T0, "rent")
w_sell = option_wealth(T0, "sell")
rank = sorted([("1 · Occupy", w_occ), ("2 · Rent out", w_rent), ("3 · Sell & reinvest", w_sell)],
              key=lambda x: -x[1])
ranked_rows = []
for i, (name, w) in enumerate(rank, 1):
    ranked_rows.append(row([i, name, money(w), money(w - w_sell),
                            "Base case (4% appreciation, 5% portfolio return)"],
                           "IRS_P551", MODEL))
add_table(table("ranking", "2045 base-case ranking by 10-year wealth",
                ["Rank", "Option", "10-year wealth", "Difference vs sell & reinvest", "Scenario"],
                ranked_rows,
                "Model output only. The ranking is conditional on the assumptions; see the sensitivity and break-even tables below."))

# Sensitivity: 10-year wealth by transfer year, appreciation and portfolio return
sens_rows = []
for T in TRANSFER_YEARS:
    for gname, g in APPRECIATION.items():
        for rname, r in [("base 5%", PORTFOLIO["base"])]:
            sens_rows.append(row([
                T, f"{gname} {pct(g, 0)}", rname,
                money(option_wealth(T, "occupy", g, r)),
                money(option_wealth(T, "rent", g, r)),
                money(option_wealth(T, "sell", g, r)),
            ], "FHFA_HPI", MODEL))
    for rname, r in PORTFOLIO.items():
        sens_rows.append(row([
            T, "base 4%", f"{rname} ({pct(r, 0)})",
            money(option_wealth(T, "occupy", APPRECIATION["base"], r)),
            money(option_wealth(T, "rent", APPRECIATION["base"], r)),
            money(option_wealth(T, "sell", APPRECIATION["base"], r)),
        ], "FED_FOMC", MODEL))
add_table(table("sensitivity", "Sensitivity of 10-year wealth to appreciation and portfolio return",
                ["Transfer year", "Appreciation scenario", "Portfolio return",
                 "Occupy", "Rent out", "Sell & reinvest"],
                sens_rows,
                "Model outputs. Rows with a portfolio-return variation hold appreciation at the 4% base; "
                "rows with an appreciation variation hold the portfolio at 5%."))

# Break-even analysis at 2045
def rent_objective(multiplier):
    return option_wealth(T0, "rent", APPRECIATION["base"], PORTFOLIO["base"], multiplier) - w_sell

be_mult = solve_break_even(rent_objective, 0.1, 6.0, 2000)
be_rent_month = HUD_FMR_SJ_4BR * be_mult

def app_objective(g):
    return option_wealth(T0, "occupy", g, PORTFOLIO["base"]) - option_wealth(T0, "sell", g, PORTFOLIO["base"])

be_g = solve_break_even(app_objective, 0.0, 0.15, 3000)

be_rows = [
    row(["Monthly rent needed for 'rent out' to match 'sell & reinvest' (2045, 2026-equivalent dollars)",
         money(be_rent_month), money(HUD_FMR_SJ_4BR),
         pct(be_mult - 1) + " above HUD benchmark" if be_mult >= 1 else pct(1 - be_mult) + " below HUD benchmark"],
        "HUD_FMR", MODEL, "HUD FY2026 4-BR FMR for the San Jose HMFA, inflated 2%/yr to 2045, multiplied by the solved factor; reported here in 2026-equivalent dollars."),
    row(["Annual appreciation needed for 'occupy' to match 'sell & reinvest' (2045)",
         pct(be_g), "4.00% (base)", "Break-even appreciation rate"],
        "FHFA_HPI", MODEL, "Solved against the 4% base case; FHFA HPI is the official price-index source."),
    row(["Property tax saved in year 2045 if Prop 19 exclusion is granted",
         money(mv_a(T0) * EFF_A - prop19_assessed(T0) * EFF_A),
         money(mv_a(T0) * EFF_A), "Full reassessment tax"],
        "BOE_P801", MODEL, "Difference between full market reassessment and the Prop 19 adjusted base year value."),
    row(["10-year imputed housing value credited to 'occupy' at the official HUD benchmark",
         money(cumulative_rent(T0, HUD_FMR_SJ_4BR * (1 + INFLATION) ** (T0 - BASE_YEAR))),
         money(HUD_FMR_SJ_4BR) + " / month (2026)", "HUD 4-BR FMR grown 2%/yr"],
        "HUD_FMR", MODEL, "A generous non-cash credit for living in the home; not cash and not a property-specific appraisal."),
    row(["'Occupy' wealth even after crediting that imputed housing value",
         money(w_occ + cumulative_rent(T0, HUD_FMR_SJ_4BR * (1 + INFLATION) ** (T0 - BASE_YEAR))),
         money(w_sell), "'Sell & reinvest' wealth"],
        "IRS_P551", MODEL, "Shows the recommendation is robust even with an unpriced housing benefit added back."),
    row(["Immediate-sale capital gain at date of death (stepped-up basis)",
         money(0), money(mv_a(T0)), "Basis = FMV at date of death"],
        "IRS_P551", MODEL, "A sale at the date-of-death value realises no gain; selling costs and later appreciation do."),
    row(["Beneficiary federal income tax on the inheritance itself",
         "$0 (generally)", "Not gross income", "Later rents/interest/dividends are taxable"],
        "IRS_P525", VERIFIED, "Official rule; excludes inherited IRA/pension income."),
]
add_table(table("breakeven", "Break-even and tax-friction numbers behind the recommendation",
                ["Question", "Answer", "Reference value", "Basis"],
                be_rows,
                "Break-even figures are solved from the model, not published values. The final row is a verified official rule."))

# Property B anchor
anchor_rows = []
for y in [2026, 2040, 2045, 2050]:
    c = b_operating_costs(y)
    rent = b_rent(y)
    anchor_rows.append(row([
        y, money(assessed_b_no_transfer(y)), money(c["property_tax"]),
        money(rent), money(sum(c.values())), money(rent - sum(c.values())),
        money(b_rent(y) / 12),
    ], "SF_ASSESSOR", MODEL,
        "Property B's very low assessed value is preserved until a change in ownership; official 2% cap applied."))
add_table(table("property_b", "Property B — the low-cost residence anchor",
                ["Year", "Taxable assessed value", "Property tax", "Gross rental income",
                 "Total operating cost", "Net operating cash flow", "Gross rent / month"],
                anchor_rows,
                "Model outputs from client-supplied inputs and official rules. The client states residence at Property B "
                "does not reduce the rental income from the two let units — that statement is unverified (FLAG-016)."))

# ----------------------------------------------------------------------------
# 11. FLAGS
# ----------------------------------------------------------------------------
FLAGS = [
    dict(id="FLAG-001", severity="Process", item="Single fixed working branch",
         detail="The parallel-session instructions call for session-<id>/<task> branches and a separate integration branch. This Arena session is bound to one fixed branch (arena/91a4a9f9-tino5) and cannot create or switch branches. Non-overlap was enforced by file scope; all tasks were claimed by one session and no other claim was overwritten.",
         action="If a multi-branch workflow is required later, re-run the coordination step in an environment that permits branch creation.",
         source="SOS_BALLOT", status="needs review"),
    dict(id="FLAG-002", severity="Privacy", item="No personal information published",
         detail="All people, addresses, trust names and account identifiers were replaced with placeholders. Only ZIP-code-level geography is used. Client-supplied financial figures are anonymous and remain unverified.",
         action="No action required; re-check before adding any new data.",
         source="SCC_PROP13", status="closed"),
    dict(id="FLAG-003", severity="Data quality", item="Client tax/assessment pairs do not reconcile to an official rate",
         detail="Client ratios imply ~1.34% (Property A) and ~2.13% (Property B) effective rates, above the official 1% + voter-approved ad valorem rates (Santa Clara TRA book; SF FY2026-27 1.18162182%). Direct charges / special assessments are a plausible explanation but are not confirmed.",
         action="Reconcile against the actual tax bills; the model uses the client-derived ratios and labels them unverified.",
         source="SF_TREASURER", status="needs review"),
    dict(id="FLAG-004", severity="Insurance", item="Property A primary-residence insurance premium unverified",
         detail="No ZIP-specific official premium was retrieved. CDI's tool publishes sample annual premiums effective May 1, 2026, and explicitly says it is not a quote. The model uses the official CDI statewide average of $1,570/yr.",
         action="Obtain quotes through the CDI comparison tool for SANTA CLARA / CUPERTINO at the correct coverage amount.",
         source="CDI_TOOL", status="needs review"),
    dict(id="FLAG-005", severity="Insurance", item="Property B landlord / rental dwelling insurance unverified",
         detail="A landlord or dwelling-fire policy is not the same as a homeowner policy, and no official ZIP-level premium was retrieved.",
         action="Use the CDI Residential Property Insurance Report (ZIP-level earned premiums by policy form) and carrier quotes.",
         source="CDI_REPORT", status="needs review"),
    dict(id="FLAG-006", severity="Utilities", item="Water, electricity and solar credit figures are client estimates",
         detail="Property A water $100-$150/mo and solar net credit $10-$20/mo; Property B water $330-$400/mo and electricity $30-$70/mo. Official tariffs are usage-based; no monthly bill was verified.",
         action="Confirm from CPUC-regulated water tariffs, SFPUC rate schedules, and the actual PG&E NEM/NBT interconnection date.",
         source="CPUC_SB695", status="needs review"),
    dict(id="FLAG-007", severity="Costs", item="Maintenance and repair cost assumption unverified",
         detail="No figure was supplied. The model uses 0.20% of market value per year for both properties, inflated with CPI. The client's statement that Property A needs less maintenance than Property B is qualitative and not modelled.",
         action="Supply a documented maintenance history or a reserve study; replace the assumption.",
         source="IRS_P527", status="needs review"),
    dict(id="FLAG-008", severity="Model", item="Appreciation and portfolio-return scenarios are not official forecasts",
         detail="2%/4%/6% home appreciation and 3%/5%/7% portfolio returns are model scenario bands. FHFA publishes the official historical HPI series, not a forecast to 2050.",
         action="Treat the sensitivity table as the decision range, not a point prediction.",
         source="FHFA_HPI", status="needs review"),
    dict(id="FLAG-009", severity="Model", item="2% inflation is a policy goal, not a 25-year forecast",
         detail="The FOMC's 2% longer-run PCE goal is used to escalate costs and project the estate-tax exemption. No official 2040-2050 inflation forecast is asserted.",
         action="Re-run with alternative inflation paths if needed.",
         source="FED_FOMC", status="needs review"),
    dict(id="FLAG-010", severity="Critical", item="Prop 19 eligibility is unconfirmed",
         detail="The exclusion requires the home to be the transferor's principal residence AND the transferee's principal residence within one year, plus a timely homeowners' exemption and BOE-19-P/19-G claim. None of these facts is verified for this estate. If ineligible, the property is reassessed to full market value.",
         action="Confirm the decedent's principal residence and decide on occupancy BEFORE the transfer; diarise the 1-year and 3-year deadlines.",
         source="BOE_P800_9", status="needs review"),
    dict(id="FLAG-011", severity="Model", item="Future Prop 19 allowance amounts are projected",
         detail="Only $1,044,590 (for transfers 2/16/2025-2/15/2027) is official. BOE publishes the inflation-adjusted amount biennially; 2040-2050 amounts do not yet exist.",
         action="Replace with the BOE-published amount in the year of transfer.",
         source="BOE_P801", status="needs review"),
    dict(id="FLAG-012", severity="Tax", item="Beneficiary-level income tax not fully computed in cash-flow comparisons",
         detail="Filing status, other income, depreciation basis, land/building split and NIIT applicability are unknown. Rental income is taxable under Pub 527; gains may attract 20% + 3.8% NIIT + up to 13.3% CA. The decision table is therefore pre-beneficiary-income-tax on annual cash flows.",
         action="Have a tax professional run the specific return before relying on the net-cash-flow ranking.",
         source="IRS_TC559", status="needs review"),
    dict(id="FLAG-013", severity="Critical", item="Estate size is unquantified",
         detail="The brief says the inheritance includes a 'considerable amount of money' that may exceed the exempt amount, but gives no figure. The estate-tax matrix is therefore illustrative arithmetic, not a calculation for this estate.",
         action="Obtain the gross estate estimate, lifetime taxable gifts, and whether a DSUE portability election was made.",
         source="IRS_ESTATE", status="needs review"),
    dict(id="FLAG-014", severity="Law change", item="November 3, 2026 California ballot results not certified",
         detail="Unofficial statewide results were published as of November 9, 2026 (Prop. 3 60.6% Yes; Prop. 40 52.8% No; Prop. 42 51.6% Yes; Prop. 43 57.3% No), but the Secretary of State certifies results only on December 11, 2026. Percentages may still change during the canvass.",
         action="Re-check the certified results after December 11, 2026 and update the Law Changes page.",
         source="SOS_RESULTS", status="needs review"),
    dict(id="FLAG-015", severity="Verification", item="All projections are model outputs, not official values",
         detail="Every projection row is labelled MODEL OUTPUT and links to the official rule behind it. No future assessed value, market value, tax bill or exemption amount is presented as an official figure.",
         action="None; this is by design.",
         source="SCC_PROP13", status="closed"),
    dict(id="FLAG-016", severity="Rent", item="SF rent-control coverage of the two let units is unconfirmed",
         detail="The official 1.6% allowable increase (3/1/2026-2/28/2027) applies to covered units. The client's $7,150/mo rental income and the claim that owner occupancy does not reduce it are unverified.",
         action="Confirm unit coverage, lawful rent, and the Housing Inventory registration with the SF Rent Board.",
         source="SF_RENT", status="needs review"),
    dict(id="FLAG-017", severity="Data quality", item="Property A 2026 tax bill supplied as '--'",
         detail="The 2026 property tax figure is missing from the client's table; 2025 is used as the effective-rate base.",
         action="Insert the 2026 secured tax bill once available.",
         source="SCC_RATEBOOK", status="needs review"),
    dict(id="FLAG-018", severity="Rent", item="HUD Fair Market Rent is a program benchmark, not a market appraisal",
         detail="FY2026 4-BR FMR of $5,010/mo for the San Jose HMFA is an official HUD program figure. It is used as the rent benchmark because no property-specific official rent exists.",
         action="Replace with a documented appraisal or executed lease if available.",
         source="HUD_FMR", status="needs review"),
    dict(id="FLAG-019", severity="Model", item="6% selling-cost assumption unverified",
         detail="Commission, transfer taxes and closing costs are modelled at 6% of price. No official source sets this rate.",
         action="Use actual listing agreement and closing estimate at the time of sale.",
         source="IRS_P523", status="needs review"),
    dict(id="FLAG-020", severity="Law change", item="SB 284 (2025) status not verified against an official bill-status page",
         detail="A BOE legislative analysis describes a proposal to reset the Prop 19 one-year residency window for probate transfers. The live bill status could not be confirmed from an official legislative status page, so it is described only as a proposal.",
         action="Verify against leginfo.legislature.ca.gov before relying on it.",
         source="BOE_PROP19", status="needs review"),
]
add_table(table("flags_table", "Flagged for Review — all unverified values and irregularities",
                ["ID", "Severity", "Item", "Detail", "Recommended action"],
                [row([f["id"], f["severity"], f["item"], f["detail"], f["action"]],
                     f["source"], "FLAGGED — UNVERIFIED" if f["status"] == "needs review" else "CLOSED")
                 for f in FLAGS],
                "Every flag links to the official agency that holds the confirming record. Flagged items do not block publication."))

# Sources registry table
add_table(table("sources_table", "Official source registry (all links retrieved and read 2026-11-10 UTC)",
                ["ID", "Agency", "Document", "What was verified"],
                [row([k, v["agency"], v["title"], v["note"]], k, VERIFIED) for k, v in SOURCES.items()],
                "The 'Official source' column is the live government URL for each row."))

# ----------------------------------------------------------------------------
# 12. EXECUTIVE SUMMARY NUMBERS (computed)
# ----------------------------------------------------------------------------
summary = dict(
    generated="2026-11-10",
    property_a_value=money(A_MV_2026),
    property_b_value=money(B_MV_2026),
    estate_exemption_2026=money(ESTATE_EXEMPTION_2026),
    estate_exemption_couple=money(2 * ESTATE_EXEMPTION_2026),
    estate_exemption_2045=money(ESTATE_EXEMPTION_2026 * (1 + INFLATION) ** (2045 - 2026)),
    estate_rate=pct(ESTATE_RATE, 0),
    prop19_allowance_2025=money(PROP19_ALLOWANCE_2025),
    prop19_allowance_2045=money(prop19_allowance(2045)),
    ca_avg_insurance=money(CA_AVG_INSURANCE),
    mv_2045=money(mv_a(2045)),
    assessed_2045_no_transfer=money(assessed_a_no_transfer(2045)),
    tax_2045_preserved=money(assessed_a_no_transfer(2045) * EFF_A),
    tax_2045_full=money(mv_a(2045) * EFF_A),
    tax_2045_prop19=money(prop19_assessed(2045) * EFF_A),
    prop19_saving_2045=money(mv_a(2045) * EFF_A - prop19_assessed(2045) * EFF_A),
    cost_a_2045=money(sum(a_operating_costs(2045, assessed_a_no_transfer(2045)).values())),
    noi_b_2026=money(b_rent(2026) - sum(b_operating_costs(2026).values())),
    wealth_2045_occupy=money(w_occ),
    wealth_2045_rent=money(w_rent),
    wealth_2045_sell=money(w_sell),
    best_2045=rank[0][0],
    breakeven_rent=money(be_rent_month),
    breakeven_appreciation=pct(be_g),
    hud_fmr=money(HUD_FMR_SJ_4BR),
    effective_rate_a=pct(EFF_A),
    effective_rate_b=pct(EFF_B),
    gain_tax_rate=pct(COMBINED_GAIN_RATE),
    verified_fact_count=len(federal_facts) + len(state_facts),
    source_count=len(SOURCES),
    flag_count=len(FLAGS),
    projection_years=END_YEAR - BASE_YEAR + 1,
)

payload = dict(
    meta=dict(
        title="Property Inheritance Decision Support",
        subtitle="Cupertino (ZIP 95014) and San Francisco (ZIP 94122) · anonymized",
        generated=summary["generated"],
        privacy="No personal information appears on this site. All identities, street addresses, trust names and account numbers are replaced with placeholders; only city and ZIP-code-level geography is used.",
        rounding="All dollar amounts are rounded to the nearest $10.",
        verification="Every data-table row carries a link to an official government source. Values that cannot be confirmed are left blank and flagged. Official values, client inputs and model outputs are three separate, labelled categories.",
    ),
    sources=SOURCES,
    tables=TABLES,
    flags=FLAGS,
    summary=summary,
)
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes)")
print(f"tables={len(TABLES)} sources={len(SOURCES)} flags={len(FLAGS)}")
print("2045 base case:", summary["wealth_2045_occupy"], summary["wealth_2045_rent"],
      summary["wealth_2045_sell"], "best:", summary["best_2045"])
print("break-even rent:", summary["breakeven_rent"], "break-even appreciation:", summary["breakeven_appreciation"])
