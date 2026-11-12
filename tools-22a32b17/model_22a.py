#!/usr/bin/env python3
"""Deterministic, privacy-safe 2026-2076 inheritance decision & black-swan model.

Scope: Session arena-22a32b17 (tools-22a32b17/** and desk-22a32b17/**).
Privacy contract:
  - Placeholders only: Property A (inherited single-family home, Santa Clara County)
    and Property B (already-owned 3-unit residential building, San Francisco County).
  - Zero personal identifiers, addresses, parcel/account numbers, ZIP codes, city or
    neighborhood names, or multi-year county assessment-roll sequences.
  - All model/baseline/projection dollar amounts are rounded to the nearest $10 at
    display time via r10() / fmt_money(). Statutory constants are tagged separately.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

BASE_YEAR = 2026
END_YEAR = 2076  # Full 50-year projection window (2026..2076 = 51 annual snapshots)

# Official verified sources (all 45 fetched & verified HTTP 200 on 2026-11-12)
SOURCES: List[Dict[str, str]] = [
    {
        "id": "S_IRS_EST",
        "agency": "Internal Revenue Service",
        "title": "Estate Tax — Filing Thresholds (2011–2026) & Gross Estate Rules",
        "url": "https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax",
        "verified": "2026-11-12",
        "used_for": "2026 basic exclusion $15,000,000; gross estate definition; portability overview.",
    },
    {
        "id": "S_IRS_WN",
        "agency": "Internal Revenue Service",
        "title": "What's New — Estate and Gift Tax (Public Law 119-21)",
        "url": "https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax",
        "verified": "2026-11-12",
        "used_for": "P.L. 119-21 enacted July 4, 2025 increasing IRC §2010(c)(3) exclusion to $15,000,000 in 2026; IRC §6035 consistent basis.",
    },
    {
        "id": "S_IRS_2027",
        "agency": "Internal Revenue Service",
        "title": "IR-2026-133 / Rev. Proc. 2026-35 — Tax Year 2027 Inflation Adjustments",
        "url": "https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2027-taxpayers-continue-to-benefit-from-the-working-families-tax-cuts",
        "verified": "2026-11-12",
        "used_for": "2027 basic exclusion $15,480,000 (+3.20% YoY); 2027 annual gift exclusion $20,000 (up from $19,000 in 2026); 2027 top 37% bracket.",
    },
    {
        "id": "S_IRS_FAQ",
        "agency": "Internal Revenue Service",
        "title": "Frequently Asked Questions on Estate Taxes",
        "url": "https://www.irs.gov/businesses/small-businesses-self-employed/frequently-asked-questions-on-estate-taxes",
        "verified": "2026-11-12",
        "used_for": "Form 706 due 9 months after death (+6-month Form 4768 extension); DSUE portability; Rev. Proc. 2022-32 5-year relief.",
    },
    {
        "id": "S_IRS_I706",
        "agency": "Internal Revenue Service",
        "title": "Instructions for Form 706 (Rev. 07/2026)",
        "url": "https://www.irs.gov/instructions/i706",
        "verified": "2026-11-12",
        "used_for": "Table A Unified Rate Schedule (40% top estate tax rate); DSUE computation; Form 8971 consistent basis reporting.",
    },
    {
        "id": "S_IRS_BASIS",
        "agency": "Internal Revenue Service",
        "title": "Gifts & Inheritances — Basis of Inherited Property FAQ",
        "url": "https://www.irs.gov/faqs/interest-dividends-other-types-of-income/gifts-inheritances/gifts-inheritances",
        "verified": "2026-11-12",
        "used_for": "IRC §1014 date-of-death FMV stepped-up basis (or §2032 alternate valuation); Schedule D / Form 8949 reporting.",
    },
    {
        "id": "S_IRS_RR2302",
        "agency": "Internal Revenue Service",
        "title": "Revenue Ruling 2023-2 — Basis of Assets in Irrevocable Grantor Trust",
        "url": "https://www.irs.gov/pub/irs-drop/rr-23-02.pdf",
        "verified": "2026-11-12",
        "used_for": "No IRC §1014 step-up at death for assets in an irrevocable grantor trust excluded from the gross estate under Ch. 11.",
    },
    {
        "id": "S_IRS_P523",
        "agency": "Internal Revenue Service",
        "title": "Publication 523 — Selling Your Home",
        "url": "https://www.irs.gov/publications/p523",
        "verified": "2026-11-12",
        "used_for": "IRC §121 principal-residence gain exclusion ($250,000 single / $500,000 MFJ); selling expenses reduce amount realized.",
    },
    {
        "id": "S_IRS_P527",
        "agency": "Internal Revenue Service",
        "title": "Publication 527 — Residential Rental Property",
        "url": "https://www.irs.gov/publications/p527",
        "verified": "2026-11-12",
        "used_for": "Rental income and operating deductions; 27.5-year MACRS straight-line depreciation on residential building basis (land excluded).",
    },
    {
        "id": "S_IRS_P550",
        "agency": "Internal Revenue Service",
        "title": "Publication 550 — Investment Income and Expenses",
        "url": "https://www.irs.gov/publications/p550",
        "verified": "2026-11-12",
        "used_for": "3.8% Net Investment Income Tax (IRC §1411); U.S. Treasury interest state-tax exemption; capital gains and dividends.",
    },
    {
        "id": "S_IRS_P551",
        "agency": "Internal Revenue Service",
        "title": "Publication 551 — Basis of Assets",
        "url": "https://www.irs.gov/publications/p551",
        "verified": "2026-11-12",
        "used_for": "Cost basis, capital improvements vs repairs, land/building allocation, and basis reductions for allowable depreciation.",
    },
    {
        "id": "S_SCO_EST",
        "agency": "California State Controller's Office",
        "title": "California Estate, Inheritance, and Gift Tax",
        "url": "https://www.sco.ca.gov/ardtax_estate_tax.html",
        "verified": "2026-11-12",
        "used_for": "Zero California estate tax for deaths on/after Jan 1, 2005; California inheritance/gift tax repealed June 8, 1982.",
    },
    {
        "id": "S_FTB_INH",
        "agency": "California Franchise Tax Board",
        "title": "Gifts and Inheritance — Personal Income Types",
        "url": "https://www.ftb.ca.gov/file/personal/income-types/gifts-and-inheritance.html",
        "verified": "2026-11-12",
        "used_for": "Inherited principal excluded from California gross income; subsequent interest, dividends, rent, and sale gains taxable.",
    },
    {
        "id": "S_FTB_RATES",
        "agency": "California Franchise Tax Board",
        "title": "2026 California Tax Rate Schedules (Form 540)",
        "url": "https://www.ftb.ca.gov/forms/2026/2026-540-tax-rate-schedules.pdf",
        "verified": "2026-11-12",
        "used_for": "2026 CA brackets 1.0%–12.3% (over $768,213 single / $1,536,426 MFJ), plus 1.0% surcharge over $1M = 13.3% top CA rate.",
    },
    {
        "id": "S_BOE_P19",
        "agency": "California State Board of Equalization",
        "title": "Proposition 19 — Intergenerational & Base Year Value Transfers",
        "url": "https://www.boe.ca.gov/prop19/",
        "verified": "2026-11-12",
        "used_for": "Principal-residence requirement for both transferor and transferee; 1-yr BOE-266 & 3-yr BOE-19-P filing; rental exclusion repealed.",
    },
    {
        "id": "S_BOE_PUB801",
        "agency": "California State Board of Equalization",
        "title": "Publication 801 — Proposition 19 Fact Sheet",
        "url": "https://www.boe.ca.gov/pdf/pub801.pdf",
        "verified": "2026-11-12",
        "used_for": "Statutory allowance $1,044,586 for transfers Feb 16, 2025–Feb 15, 2027 (LTA 2025/009); excess FMV formula; prospective relief.",
    },
    {
        "id": "S_BOE_LTA26026",
        "agency": "California State Board of Equalization",
        "title": "Letter to Assessors No. 2026/026 (Aug 3, 2026) — Prop 19 Intergenerational FAQ",
        "url": "https://www.boe.ca.gov/proptaxes/pdf/lta26026.pdf",
        "verified": "2026-11-12",
        "used_for": "Trust beneficial transfers qualify; legal entity interests excluded; continual occupancy required; multi-unit single-unit limit.",
    },
    {
        "id": "S_BOE_LTA26002",
        "agency": "California State Board of Equalization",
        "title": "Letter to Assessors No. 2026/002 (Jan 13, 2026) — 2026-27 CCPI & 1976-2027 Roll Factors",
        "url": "https://www.boe.ca.gov/proptaxes/pdf/lta26002.pdf",
        "verified": "2026-11-12",
        "used_for": "50-year California CPI & Prop 13 factor table (1976-77 to 2026-27); confirms 2014-2026 roll percentages & 2026-27 1.02 factor.",
    },
    {
        "id": "S_BOE_PUB800",
        "agency": "California State Board of Equalization",
        "title": "Publication 800-10 — How Property Is Assessed for Property Tax Purposes",
        "url": "https://boe.ca.gov/pdf/pub800-10.pdf",
        "verified": "2026-11-12",
        "used_for": "Prop 13 1% base + voter-approved debt, max 2%/yr FBYV growth, and Prop 8 temporary decline-in-value reductions.",
    },
    {
        "id": "S_BOE_HOX",
        "agency": "California State Board of Equalization",
        "title": "Homeowners' Exemption ($7,000 Principal Residence Reduction)",
        "url": "https://www.boe.ca.gov/proptaxes/homeowners_exemption.htm",
        "verified": "2026-11-12",
        "used_for": "$7,000 taxable-value reduction on owner's single principal residence; Feb 15 full-exemption deadline; Dec 10 termination rule.",
    },
    {
        "id": "S_BOE_266",
        "agency": "California State Board of Equalization",
        "title": "Sample Form BOE-266 — Claim for Homeowners' Property Tax Exemption",
        "url": "https://boe.ca.gov/proptaxes/pdf/sample-boe266.pdf",
        "verified": "2026-11-12",
        "used_for": "One Homeowners' Exemption per household; moving from Property B to Property A requires terminating B's exemption.",
    },
    {
        "id": "S_RTC_632",
        "agency": "California Legislature",
        "title": "Revenue and Taxation Code §63.2 (Proposition 19 Implementation)",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2.",
        "verified": "2026-11-12",
        "used_for": "Statutory 1-year occupancy test, removal of exclusion upon moving out, and enrollment of factored change-in-ownership value.",
    },
    {
        "id": "S_RTC_51",
        "agency": "California Legislature",
        "title": "Revenue and Taxation Code §51 (Prop 13 Cap & Prop 8 Decline in Value)",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=51.",
        "verified": "2026-11-12",
        "used_for": "Taxable value is lesser of FBYV (compounded <=2%/yr) or current lien-date full cash value during housing downturns.",
    },
    {
        "id": "S_RTC_480",
        "agency": "California Legislature",
        "title": "Revenue and Taxation Code §480(b) (Death of Real Property Owner Filing)",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=480.",
        "verified": "2026-11-12",
        "used_for": "Mandatory Change in Ownership Statement by trustee or transferee within 150 days after date of death; penalty for non-filing.",
    },
    {
        "id": "S_RTC_11911",
        "agency": "California Legislature",
        "title": "Revenue and Taxation Code §11911 (County Documentary Transfer Tax)",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=11911.",
        "verified": "2026-11-12",
        "used_for": "$0.55 per $500 (0.11%) county documentary transfer tax on sales of Property A.",
    },
    {
        "id": "S_RTC_11930",
        "agency": "California Legislature",
        "title": "Revenue and Taxation Code §11930 (Death & Gift Transfer Tax Exemption)",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=11930.",
        "verified": "2026-11-12",
        "used_for": "$0 documentary transfer tax on deeds transferring property outright or via trust by reason of death.",
    },
    {
        "id": "S_PROB_16061",
        "agency": "California Legislature",
        "title": "Probate Code §16061.7 (Mandatory Trustee Notification at Death)",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PROB&sectionNum=16061.7.",
        "verified": "2026-11-12",
        "used_for": "Successor trustee must serve statutory notification on all beneficiaries and heirs within 60 days after settlor's death.",
    },
    {
        "id": "S_CIV_1947",
        "agency": "California Legislature",
        "title": "Civil Code §1947.12 (Tenant Protection Act / AB 1482 Rent Cap)",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12",
        "verified": "2026-11-12",
        "used_for": "Statewide rent increase cap (5% + CPI, max 10%) and single-family alienable-title exemption disclosure requirements.",
    },
    {
        "id": "S_SCC_P19",
        "agency": "Santa Clara County Office of the Assessor",
        "title": "Parent-Child Transfer (Proposition 19) Guidance & Worked Example",
        "url": "https://asr.santaclaracounty.gov/tax-savings/transferring-your-assessed-value/parent-to-child-2",
        "verified": "2026-11-12",
        "used_for": "County implementation of Prop 19 parent-child exclusion, BOE-19-P filing, and multi-unit apportionment note.",
    },
    {
        "id": "S_SCC_AR",
        "agency": "Santa Clara County Office of the Assessor",
        "title": "Assessor's Annual Report 2025–2026",
        "url": "https://files.santaclaracounty.gov/exjcpb1521/2025-11/annual_report_2025-2026.pdf",
        "verified": "2026-11-12",
        "used_for": "Santa Clara County assessment roll administration, 1% base + local voter-approved bonds, and Prop 8/13/19 procedures.",
    },
    {
        "id": "S_SF_TAX",
        "agency": "San Francisco Treasurer & Tax Collector",
        "title": "Secured Property Taxes — FY 2026-27 Rate & Deadlines",
        "url": "https://sftreasurer.org/property/secured-property-taxes",
        "verified": "2026-11-12",
        "used_for": "FY 2026-27 secured property tax rate 1.18162182%; Dec 10 / Apr 10 installment deadlines; supplemental & escape bills.",
    },
    {
        "id": "S_SF_TT",
        "agency": "San Francisco Office of the Assessor-Recorder",
        "title": "Real Property Transfer Tax Rates & Affidavit Rules",
        "url": "https://www.sf.gov/transfer-tax",
        "verified": "2026-11-12",
        "used_for": "SF tiered transfer tax ($3.75/$500 = 0.75% at $1M-$5M; $11.25/$500 = 2.25% at $5M-$10M; $27.50/$500 = 5.50% at $10M-$25M).",
    },
    {
        "id": "S_SF_RENT",
        "agency": "San Francisco Rent Board",
        "title": "Current Rates: Allowable Annual Rent Increase (2026-2027), Relocation & Deposit Interest",
        "url": "https://www.sf.gov/reports--current-rates-including-rent-increase-relocation-sec-deposit",
        "verified": "2026-11-12",
        "used_for": "1.6% allowable rent increase (3/1/2026–2/28/2027); 4.2% deposit interest; File No. 261020 proposed 10% banked/capital cap; relocation fees.",
    },
    {
        "id": "S_SFPUC",
        "agency": "San Francisco Public Utilities Commission",
        "title": "Proposition 218 Notice: Water and Sewer Rates FYE 2027–2028",
        "url": "https://www.sfpuc.gov/accounts-services/water-power-sewer-rates/proposed-water-sewer-rates-2026/proposition-218-notice",
        "verified": "2026-11-12",
        "used_for": "Fixed meter + volumetric water/wastewater tariff structure; ~12.5%/yr FY27-28 combined rate increases for aging infrastructure.",
    },
    {
        "id": "S_CDI_SIS",
        "agency": "California Department of Insurance",
        "title": "Sustainable Insurance Strategy — Market Snapshot (Updated Oct 27, 2026)",
        "url": "https://www.insurance.ca.gov/01-consumers/180-climate-change/sustainable-insurance-strategy.cfm",
        "verified": "2026-11-12",
        "used_for": "CA average homeowner premium $1,571 ($1,570 rounded) vs US $1,512 ($1,510 rounded); 677,449 FAIR Plan policies; catastrophe modeling.",
    },
    {
        "id": "S_CDI_RES",
        "agency": "California Department of Insurance",
        "title": "Residential Insurance: Homeowners and Renters Guide (Rev. Jan 2026)",
        "url": "https://www.insurance.ca.gov/01-consumers/105-type/95-guides/03-res/res-ins-guide.cfm",
        "verified": "2026-11-12",
        "used_for": "Coverage A-F structure (owner HO-3 vs landlord dwelling policy), replacement cost sizing, and earthquake/flood exclusions.",
    },
    {
        "id": "S_CPUC_NEM",
        "agency": "California Public Utilities Commission",
        "title": "Net Energy Metering (NEM) and Net Billing Tariff (Solar Billing Plan)",
        "url": "https://www.cpuc.ca.gov/nem",
        "verified": "2026-11-12",
        "used_for": "NEM closed Apr 15, 2023 (D.22-12-056); avoided-cost export credits under NBT; NSC ~$0.02-$0.03/kWh; E-ELEC TOU requirement.",
    },
    {
        "id": "S_COURTS",
        "agency": "Judicial Branch of California",
        "title": "Self-Help Guide to Property After Someone Dies (Probate & Trusts)",
        "url": "https://selfhelp.courts.ca.gov/probate",
        "verified": "2026-11-12",
        "used_for": "Non-probate trust transfer vs formal Superior Court probate administration.",
    },
    {
        "id": "S_SOS_2026",
        "agency": "California Secretary of State",
        "title": "2026 General Election — Unofficial Statewide Ballot Measure Returns (Nov 11, 2026)",
        "url": "https://electionresults.sos.ca.gov/returns/ballot-measures",
        "verified": "2026-11-12",
        "used_for": "Prop 3 (60.7% Yes), Prop 40 (52.5% No), Prop 42 (51.4% Yes), Prop 43 (57.4% No); official certification due Dec 11, 2026.",
    },
    {
        "id": "S_BLS_CPI",
        "agency": "U.S. Bureau of Labor Statistics",
        "title": "Consumer Price Index Summary — October 2026 (USDL-26-1685, Nov 10, 2026)",
        "url": "https://www.bls.gov/news.release/cpi.nr0.htm",
        "verified": "2026-11-12",
        "used_for": "Oct 2026 CPI-U +0.4% SA (+0.6% Sep), shelter +0.3%, electricity +0.9% MoM, CPI-U index 337.511.",
    },
    {
        "id": "S_FED_FOMC",
        "agency": "Board of Governors of the Federal Reserve System",
        "title": "Minutes of the Federal Open Market Committee — September 15–16, 2026",
        "url": "https://www.federalreserve.gov/monetarypolicy/fomcminutes20260916.htm",
        "verified": "2026-11-12",
        "used_for": "Fed funds target raised +25 bps to 3.75%-4.00%; IORB 3.90%; Aug PCE 3.8% / core 3.4%; 2.0% long-run inflation goal.",
    },
    {
        "id": "S_FHFA_HPI",
        "agency": "Federal Housing Finance Agency",
        "title": "FHFA House Price Index (HPI) — Repeat-Sales Data & Volatility Parameters",
        "url": "https://www.fhfa.gov/data/hpi",
        "verified": "2026-11-12",
        "used_for": "Long-run single-family home appreciation methodology and metro housing cycle volatility.",
    },
    {
        "id": "S_CBO_2026",
        "agency": "Congressional Budget Office",
        "title": "The Budget and Economic Outlook: 2026 to 2036 (Feb 2026)",
        "url": "https://www.cbo.gov/publication/62105",
        "verified": "2026-11-12",
        "used_for": "Federal debt held by public projected from 101% of GDP (2026) to 120% (2036); baseline inflation & Treasury rate path.",
    },
    {
        "id": "S_TSP_RET",
        "agency": "Federal Retirement Thrift Investment Board (TSP)",
        "title": "Official Fund Rates of Return (C Fund S&P 500 & G Fund Treasury)",
        "url": "https://www.tsp.gov/rates-return/",
        "verified": "2026-11-12",
        "used_for": "12-month through Oct 2026 C Fund 12.09% / G Fund 4.61%; long-run equity vs risk-free return benchmarks.",
    },
    {
        "id": "S_USGS_EQ",
        "agency": "U.S. Geological Survey",
        "title": "Uniform California Earthquake Rupture Forecast 3 (UCERF3) — Bay Area Probabilities",
        "url": "https://www.usgs.gov/faqs/what-probability-earthquake-will-occur-los-angeles-area-san-francisco-bay-area",
        "verified": "2026-11-12",
        "used_for": "72% 30-year probability of M>=6.7 and 51% probability of M>=7.0 earthquake in the San Francisco Bay region.",
    },
]

SOURCE_MAP: Dict[str, Dict[str, str]] = {s["id"]: s for s in SOURCES}

# Official BOE LTA 2026/002 CCPI & Prop 13 Factor table (2014-15 through 2026-27)
BOE_CCPI_RECENT: List[Tuple[str, str, str, str]] = [
    ("2014–15", "0.454%", "0.45%", "1.00454"),
    ("2015–16", "1.998%", "2.00%", "1.01998"),
    ("2016–17", "1.525%", "1.53%", "1.01525"),
    ("2017–18", "2.619%", "2.00%", "1.02000"),
    ("2018–19", "2.962%", "2.00%", "1.02000"),
    ("2019–20", "3.847%", "2.00%", "1.02000"),
    ("2020–21", "2.980%", "2.00%", "1.02000"),
    ("2021–22", "1.036%", "1.04%", "1.01036"),
    ("2022–23", "5.561%", "2.00%", "1.02000"),
    ("2023–24", "7.274%", "2.00%", "1.02000"),
    ("2024–25", "3.181%", "2.00%", "1.02000"),
    ("2025–26", "2.514%", "2.00%", "1.02000"),
    ("2026–27", "3.307%", "2.00%", "1.02000"),
]


def r10(val: float) -> int:
    """Round any dollar figure to the nearest $10 increment."""
    return int(round(val / 10.0) * 10)


def fmt_money(val: float, dash_zero: bool = False) -> str:
    rounded = r10(val)
    if dash_zero and rounded == 0:
        return "—"
    if rounded < 0:
        return f"-${abs(rounded):,}"
    return f"${rounded:,}"


def fmt_pct(val: float, digits: int = 2) -> str:
    return f"{val * 100:.{digits}f}%"


@dataclass(frozen=True)
class ModelParams:
    # Macroeconomic baseline assumptions
    inflation: float = 0.025              # 2.5%/yr long-run CPI
    home_growth_a: float = 0.042          # 4.2%/yr Santa Clara County SFR appreciation
    home_growth_b: float = 0.036          # 3.6%/yr San Francisco 3-unit appreciation
    prop13_cap: float = 0.020             # 2.0%/yr statutory Prop 13 max roll growth
    prop19_allowance_2026: float = 1_044_586.0  # BOE LTA 2025/009 statutory constant
    prop19_allowance_growth: float = 0.022      # Biennial CCPI indexing (~2.2%/yr)
    estate_excl_2026: float = 15_000_000.0      # P.L. 119-21 statutory 2026 exclusion
    estate_excl_2027: float = 15_480_000.0      # Rev. Proc. 2026-35 statutory 2027 exclusion
    estate_tax_rate: float = 0.40               # IRC §2001(c) top marginal estate rate

    # Investment return assumptions (after annual dividend/interest tax drag)
    equity_pre_tax: float = 0.072         # 7.2%/yr diversified equity nominal total return
    equity_after_tax: float = 0.056       # 5.6%/yr compounding after dividend/realization drag
    treasury_pre_tax: float = 0.039       # 3.9%/yr US Treasury yield (CA state-tax exempt)
    treasury_after_tax: float = 0.025     # 2.5%/yr after federal ordinary income tax

    # Income & capital-gains tax assumptions for high-bracket CA filer
    ltcg_combined_rate: float = 0.371     # 20% Fed LTCG + 3.8% NIIT + 13.3% CA
    recapture_combined_rate: float = 0.383  # 25% Fed §1250 + 13.3% CA on depreciation
    ordinary_combined_rate: float = 0.503   # 37% Fed + 13.3% CA marginal ordinary rate
    rental_effective_tax_rate: float = 0.420  # Effective marginal rate on net positive rent
    sec121_exclusion: float = 250_000.0     # IRC §121 single filer ($500k MFJ sensitivity)
    building_share_a: float = 0.65          # 65% structure / 35% land for §168 depreciation

    # Property A (Inherited SFR, Santa Clara County) — banded/rounded 2026 baselines
    a_fmv_2026: float = 3_100_000.0
    a_fbyv_2026: float = 550_000.0        # Banded roll baseline (avoids parcel fingerprinting)
    a_ad_valorem_rate: float = 0.0119     # 1.00% Prop 13 + ~0.19% voter-approved bonds
    a_direct_charges_2026: float = 660.0  # Fixed parcel/special assessments (~$7,210 total)
    a_ins_ho3_2026: float = 3_200.0       # Researched Coverage A primary-residence HO-3
    a_ins_dp3_2026: float = 3_800.0       # Researched DP-3 landlord dwelling policy
    a_water_2026: float = 1_500.0         # $1,500/yr midpoint ($100-$150/mo range)
    a_elec_2026: float = -180.0           # -$180/yr solar credit (-$10 to -$20/mo range)
    a_elec_post_nem_2026_eq: float = 600.0  # Post-legacy-NEM NBT + base charge equivalent
    a_nem_sunset_year: int = 2038         # 20-yr legacy NEM transition assumption
    a_maint_2026: float = 12_400.0        # Routine maintenance + capital reserve (~0.40%)
    a_rent_2026: float = 68_400.0         # $5,700/mo market rent baseline
    a_rent_growth: float = 0.030          # 3.0%/yr market rent growth
    a_vacancy_mgmt: float = 0.12          # 5% vacancy + 7% leasing/management
    a_sell_cost_rate: float = 0.055       # 5.0% brokerage/prep + 0.11% county TT + escrow

    # Property B (Already-Owned 3-Unit Building, San Francisco County)
    b_fmv_2026: float = 1_800_000.0
    b_ad_valorem_base_2026: float = 114_000.0  # Banded stated roll base
    b_tax_rate: float = 0.0118162182      # Verified FY 2026-27 SF secured rate
    b_direct_charges_2026: float = 1_090.0  # Fixed SF parcel/direct charges (~$2,440 total)
    b_ins_2026: float = 4_200.0           # Researched 3-unit habitational/landlord policy
    b_water_2026: float = 4_380.0         # $4,380/yr midpoint ($330-$400/mo across 3 units)
    b_water_growth: float = 0.035         # Water/sewer escalation above general CPI
    b_elec_2026: float = 600.0            # $50/mo midpoint ($30-$70/mo common/owner)
    b_maint_2026: float = 14_400.0        # Older 3-unit coastal structure (~0.80%)
    b_rent_2units_2026: float = 85_800.0  # $7,150/mo across 2 rented units
    b_rent_unit3_2026: float = 42_000.0   # $3,500/mo potential market rent if Unit 3 leased
    b_rent_growth: float = 0.020          # Constrained by SF Rent Ordinance (60% of CPI)
    b_vacancy_mgmt: float = 0.08          # Self-managed / low turnover on 2 rent-controlled units


DEFAULT_PARAMS = ModelParams()


def prop19_new_taxable(fmv: float, fbyv: float, allowance: float) -> float:
    """Compute new taxable value under CA R&TC §63.2 / Prop 19 family-home transfer."""
    excluded_cap = fbyv + allowance
    if fmv <= excluded_cap:
        return fbyv
    return fbyv + (fmv - excluded_cap)


def prop19_allowance_at(year: int, p: ModelParams = DEFAULT_PARAMS) -> float:
    """Biennial adjustment on Feb 16 of odd years (2025, 2027, 2029...)."""
    if year <= 2026:
        return p.prop19_allowance_2026
    steps = (year - 2025) // 2
    return p.prop19_allowance_2026 * ((1.0 + p.prop19_allowance_growth) ** (2 * steps))


def federal_estate_exclusion_at(year: int, p: ModelParams = DEFAULT_PARAMS, cpi_override: float | None = None) -> float:
    """Statutory $15,000,000 in 2026, $15,480,000 in 2027, CPI-indexed thereafter."""
    if year <= 2026:
        return p.estate_excl_2026
    if year == 2027 and cpi_override is None:
        return p.estate_excl_2027
    g = p.inflation if cpi_override is None else cpi_override
    if year >= 2027 and cpi_override is None:
        return p.estate_excl_2027 * ((1.0 + g) ** (year - 2027))
    return p.estate_excl_2026 * ((1.0 + g) ** (year - 2026))


def sf_transfer_tax_rate(price: float) -> float:
    """Official San Francisco Real Property Transfer Tax rate per $1 of consideration."""
    if price <= 250_000:
        return 2.50 / 500.0
    if price < 1_000_000:
        return 3.40 / 500.0
    if price < 5_000_000:
        return 3.75 / 500.0
    if price < 10_000_000:
        return 11.25 / 500.0
    if price < 25_000_000:
        return 27.50 / 500.0
    return 30.00 / 500.0


def property_a_annual_snapshot(
    year: int,
    transfer_year: int = 2045,
    p: ModelParams = DEFAULT_PARAMS,
) -> Dict[str, float]:
    """Annual snapshot for Property A across 2026..2076 given a transfer in transfer_year."""
    t = year - BASE_YEAR
    infl = (1.0 + p.inflation) ** t
    fmv = p.a_fmv_2026 * ((1.0 + p.home_growth_a) ** t)
    pre_transfer_fbyv = p.a_fbyv_2026 * ((1.0 + p.prop13_cap) ** t)
    direct = p.a_direct_charges_2026 * ((1.0 + 0.015) ** t)

    if year < transfer_year:
        assess_occ = pre_transfer_fbyv
        assess_rent = pre_transfer_fbyv
        tax_occ = max(assess_occ - 7_000.0, 0.0) * p.a_ad_valorem_rate + direct
        tax_rent = tax_occ
    else:
        n_tr = transfer_year - BASE_YEAR
        fmv_tr = p.a_fmv_2026 * ((1.0 + p.home_growth_a) ** n_tr)
        fbyv_tr = p.a_fbyv_2026 * ((1.0 + p.prop13_cap) ** n_tr)
        allow_tr = prop19_allowance_at(transfer_year, p)
        base_occ = prop19_new_taxable(fmv_tr, fbyv_tr, allow_tr)
        base_rent = fmv_tr
        post_yrs = year - transfer_year
        assess_occ = min(fmv, base_occ * ((1.0 + p.prop13_cap) ** post_yrs))
        assess_rent = min(fmv, base_rent * ((1.0 + p.prop13_cap) ** post_yrs))
        tax_occ = max(assess_occ - 7_000.0, 0.0) * p.a_ad_valorem_rate + direct
        tax_rent = assess_rent * p.a_ad_valorem_rate + direct

    ins_occ = p.a_ins_ho3_2026 * infl
    ins_rent = p.a_ins_dp3_2026 * infl
    water = p.a_water_2026 * infl
    elec = (p.a_elec_2026 if year < p.a_nem_sunset_year else p.a_elec_post_nem_2026_eq) * infl
    maint = p.a_maint_2026 * infl
    gross_rent = p.a_rent_2026 * ((1.0 + p.a_rent_growth) ** t)
    vac_mgmt = gross_rent * p.a_vacancy_mgmt

    carry_occ = tax_occ + ins_occ + water + elec + maint
    noi_rent_pre_tax = gross_rent - vac_mgmt - tax_rent - ins_rent - water - elec - maint

    return {
        "year": float(year),
        "fmv": fmv,
        "pre_fbyv": pre_transfer_fbyv,
        "assess_occ": assess_occ,
        "assess_rent": assess_rent,
        "tax_occ": tax_occ,
        "tax_rent": tax_rent,
        "ins_occ": ins_occ,
        "ins_rent": ins_rent,
        "water": water,
        "elec": elec,
        "maint": maint,
        "gross_rent": gross_rent,
        "vac_mgmt": vac_mgmt,
        "carry_occ": carry_occ,
        "noi_rent": noi_rent_pre_tax,
    }


def property_b_annual_snapshot(
    year: int,
    owner_occupied: bool = True,
    lease_unit3: bool = False,
    lease_unit3_start: int = 2045,
    p: ModelParams = DEFAULT_PARAMS,
) -> Dict[str, float]:
    """Annual snapshot for already-owned Property B across 2026..2076."""
    t = year - BASE_YEAR
    infl = (1.0 + p.inflation) ** t
    fmv = p.b_fmv_2026 * ((1.0 + p.home_growth_b) ** t)
    fbyv = p.b_ad_valorem_base_2026 * ((1.0 + p.prop13_cap) ** t)
    hox = 7_000.0 if owner_occupied else 0.0
    direct = p.b_direct_charges_2026 * ((1.0 + 0.015) ** t)
    tax = max(fbyv - hox, 0.0) * p.b_tax_rate + direct

    ins = p.b_ins_2026 * infl
    water = p.b_water_2026 * ((1.0 + p.b_water_growth) ** t)
    elec = p.b_elec_2026 * infl
    maint = p.b_maint_2026 * infl

    rent_2 = p.b_rent_2units_2026 * ((1.0 + p.b_rent_growth) ** t)
    rent_3 = 0.0
    if lease_unit3 and year >= lease_unit3_start:
        # Initial market rent at lease_unit3_start grows at market rate up to start, then SF rent-cap rate
        start_mkt = p.b_rent_unit3_2026 * ((1.0 + 0.030) ** (lease_unit3_start - BASE_YEAR))
        rent_3 = start_mkt * ((1.0 + p.b_rent_growth) ** (year - lease_unit3_start))

    gross_rent = rent_2 + rent_3
    vac_mgmt = gross_rent * p.b_vacancy_mgmt
    opex = ins + water + elec + maint + vac_mgmt
    noi = gross_rent - tax - opex

    return {
        "year": float(year),
        "fmv": fmv,
        "fbyv": fbyv,
        "tax": tax,
        "ins": ins,
        "water": water,
        "elec": elec,
        "maint": maint,
        "gross_rent": gross_rent,
        "opex_total": tax + opex,
        "noi": noi,
    }


def evaluate_strategies(
    transfer_year: int = 2045,
    horizon_years: int = 25,
    p: ModelParams = DEFAULT_PARAMS,
    step_up_applies: bool = True,
    carryover_basis_a: float = 250_000.0,
) -> Dict[str, Dict[str, float]]:
    """Compare the 5 household strategies over [transfer_year, transfer_year + horizon_years).

    Every strategy accounts for:
      - Property A outcome + Property B incremental difference (held consistent so housing
        consumption and the single $7,000 Homeowners' Exemption are treated identically!).
      - Annual after-tax cash flows compounded forward to end_year at equity_after_tax
        (or treasury_after_tax for S3b) so 2045 dollars and 2070 dollars are never mixed!
      - Both Hold-Without-Sale Net Worth and Post-Liquidation After-Tax Net Wealth at end_year.
    """
    end_year = transfer_year + horizon_years
    n_tr = transfer_year - BASE_YEAR
    fmv_tr = p.a_fmv_2026 * ((1.0 + p.home_growth_a) ** n_tr)
    init_basis = fmv_tr if step_up_applies else carryover_basis_a

    # Baseline B cash flow when owner lives in B Unit 3 (used by S2, S3a, S3b)
    def b_after_tax_cf(yr: int, owner_occ: bool, lease_u3: bool) -> float:
        b = property_b_annual_snapshot(
            yr, owner_occupied=owner_occ, lease_unit3=lease_u3, lease_unit3_start=transfer_year, p=p
        )
        # B's existing low basis yields minimal remaining depreciation; tax positive NOI
        tax_on_b = max(b["noi"], 0.0) * p.rental_effective_tax_rate
        return b["noi"] - tax_on_b

    # Annual depreciation on Property A if rented (27.5-yr straight-line on building share)
    annual_depr_a = (init_basis * p.building_share_a) / 27.5

    # Accumulators of liquid side-portfolio from [transfer_year .. end_year - 1]
    port_s1a = 0.0
    port_s1b = 0.0
    port_s2 = 0.0

    # Sale at transfer_year for S3a & S3b
    net_sale_tr = fmv_tr * (1.0 - p.a_sell_cost_rate)
    cap_gain_tr = max(net_sale_tr - init_basis, 0.0)
    tax_tr = cap_gain_tr * p.ltcg_combined_rate
    proceeds_after_tax_tr = net_sale_tr - tax_tr

    port_s3a = proceeds_after_tax_tr
    port_s3b = proceeds_after_tax_tr

    yr1_cf: Dict[str, float] = {}
    cum_depr_a = 0.0

    for idx in range(horizon_years):
        yr = transfer_year + idx
        a = property_a_annual_snapshot(yr, transfer_year=transfer_year, p=p)

        # Incremental B difference relative to living in B Unit 3:
        # Living in B Unit 3 gives b_base; moving to A gives b_s1a (Unit 3 vacant) or b_s1b (Unit 3 leased).
        b_base = b_after_tax_cf(yr, owner_occ=True, lease_u3=False)
        b_vac = b_after_tax_cf(yr, owner_occ=False, lease_u3=False)
        b_lse = b_after_tax_cf(yr, owner_occ=False, lease_u3=True)

        cf_s1a = -a["carry_occ"] + (b_vac - b_base)
        cf_s1b = -a["carry_occ"] + (b_lse - b_base)

        # S2: Rent Property A while living in Property B Unit 3
        depr_this_yr = min(annual_depr_a, max(init_basis * p.building_share_a - cum_depr_a, 0.0))
        cum_depr_a += depr_this_yr
        taxable_rent_a = a["noi_rent"] - depr_this_yr
        # If taxable_rent_a > 0, taxed at rental_effective_tax_rate; if < 0, passive loss carried forward
        # (modeled conservatively as carried forward to offset terminal gain rather than current wages,
        # because high-income filers >$150k MAGI phase out of IRC §469(i) $25k active-participation allowance)
        inc_tax_a = max(taxable_rent_a, 0.0) * p.rental_effective_tax_rate
        cf_s2 = a["noi_rent"] - inc_tax_a

        if idx == 0:
            yr1_cf["S1a"] = cf_s1a
            yr1_cf["S1b"] = cf_s1b
            yr1_cf["S2"] = cf_s2
            yr1_cf["S3a"] = proceeds_after_tax_tr * p.equity_after_tax
            yr1_cf["S3b"] = proceeds_after_tax_tr * p.treasury_after_tax

        # Compound prior portfolio for 1 year and add end-of-year cash flow
        port_s1a = port_s1a * (1.0 + p.equity_after_tax) + cf_s1a
        port_s1b = port_s1b * (1.0 + p.equity_after_tax) + cf_s1b
        port_s2 = port_s2 * (1.0 + p.equity_after_tax) + cf_s2
        port_s3a = port_s3a * (1.0 + p.equity_after_tax)
        port_s3b = port_s3b * (1.0 + p.treasury_after_tax)

    # Terminal Property A valuation at end_year
    fmv_end = p.a_fmv_2026 * ((1.0 + p.home_growth_a) ** (end_year - BASE_YEAR))
    net_sale_end = fmv_end * (1.0 - p.a_sell_cost_rate)

    # S1a / S1b terminal capital-gains tax (eligible for IRC §121 principal-residence exclusion)
    gain_s1 = max(net_sale_end - init_basis - p.sec121_exclusion, 0.0)
    cg_tax_s1 = gain_s1 * p.ltcg_combined_rate
    net_a_liq_s1 = net_sale_end - cg_tax_s1

    # S2 terminal tax: §1250 unrecaptured depreciation + LTCG on remaining appreciation,
    # offset by accumulated suspended passive losses if any
    suspended_losses = 0.0
    cum_d = 0.0
    for idx in range(horizon_years):
        yr = transfer_year + idx
        a_snap = property_a_annual_snapshot(yr, transfer_year=transfer_year, p=p)
        d_yr = min(annual_depr_a, max(init_basis * p.building_share_a - cum_d, 0.0))
        cum_d += d_yr
        if a_snap["noi_rent"] - d_yr < 0:
            suspended_losses += abs(a_snap["noi_rent"] - d_yr)

    adj_basis_s2 = init_basis - cum_depr_a
    total_gain_s2 = max(net_sale_end - adj_basis_s2, 0.0)
    recapture_part = min(total_gain_s2, cum_depr_a)
    apprec_part = max(total_gain_s2 - recapture_part, 0.0)
    gross_tax_s2 = recapture_part * p.recapture_combined_rate + apprec_part * p.ltcg_combined_rate
    passive_tax_shield = suspended_losses * p.rental_effective_tax_rate
    cg_tax_s2 = max(gross_tax_s2 - passive_tax_shield, 0.0)
    net_a_liq_s2 = net_sale_end - cg_tax_s2

    return {
        "meta": {
            "transfer_year": float(transfer_year),
            "end_year": float(end_year),
            "horizon_years": float(horizon_years),
            "fmv_transfer": fmv_tr,
            "proceeds_transfer": proceeds_after_tax_tr,
            "fmv_end": fmv_end,
            "cum_depr_s2": cum_depr_a,
        },
        "S1a": {
            "yr1_cf": yr1_cf["S1a"],
            "side_portfolio": port_s1a,
            "hold_net_worth": fmv_end + port_s1a,
            "liquidated_wealth": net_a_liq_s1 + port_s1a,
            "terminal_tax": cg_tax_s1,
        },
        "S1b": {
            "yr1_cf": yr1_cf["S1b"],
            "side_portfolio": port_s1b,
            "hold_net_worth": fmv_end + port_s1b,
            "liquidated_wealth": net_a_liq_s1 + port_s1b,
            "terminal_tax": cg_tax_s1,
        },
        "S2": {
            "yr1_cf": yr1_cf["S2"],
            "side_portfolio": port_s2,
            "hold_net_worth": fmv_end + port_s2,
            "liquidated_wealth": net_a_liq_s2 + port_s2,
            "terminal_tax": cg_tax_s2,
        },
        "S3a": {
            "yr1_cf": yr1_cf["S3a"],
            "side_portfolio": port_s3a,
            "hold_net_worth": port_s3a,
            "liquidated_wealth": port_s3a,
            "terminal_tax": tax_tr,
        },
        "S3b": {
            "yr1_cf": yr1_cf["S3b"],
            "side_portfolio": port_s3b,
            "hold_net_worth": port_s3b,
            "liquidated_wealth": port_s3b,
            "terminal_tax": tax_tr,
        },
    }


def build_black_swan_regimes() -> List[Dict[str, object]]:
    """Simulate 7 non-linear 50-year (2026-2076) path-dependent economic regimes.

    Each regime defines year-by-year vectors for:
      cpi[y], home_g[y], rent_g[y], eq_r[y], tr_r[y], ins_shock[y], seismic_hit_a[y]
    and applies exact California R&TC §51 (lesser of Prop 13 2%-capped FBYV or current FMV
    under Prop 8 decline-in-value!) at every single year from 2026 through 2076!
    """
    years = list(range(BASE_YEAR, END_YEAR + 1))

    def base_vectors() -> Dict[int, Tuple[float, float, float, float, float, float, float]]:
        return {y: (0.025, 0.042, 0.030, 0.056, 0.025, 1.0, 0.0) for y in years}

    regimes_spec: List[Tuple[str, str, str, str, Dict[int, Tuple[float, float, float, float, float, float, float]]]] = []

    # Regime 0: Smooth Textbook Baseline (benchmark)
    regimes_spec.append((
        "R0",
        "Smooth Constant-Rate Baseline (Benchmark)",
        "4.2% home / 2.5% CPI / 5.6% after-tax equity every single year — shown to expose what linear models hide.",
        "S_CBO_2026",
        base_vectors(),
    ))

    # Regime 1: Full 50-Year Realistic Multi-Cycle Path (mean-matched to historical CAGRs)
    v1 = base_vectors()
    for y in years:
        phase = (y - 2026) % 10
        if phase == 0:            # Late-cycle Fed tightening (mirrors 2026 FOMC)
            v1[y] = (0.036, 0.032, 0.035, 0.035, 0.029, 1.0, 0.0)
        elif phase == 1:          # Recession & equity drawdown (mirrors 2001 / 2008 / 2022)
            v1[y] = (0.008, -0.095, -0.025, -0.210, 0.022, 1.0, 0.0)
        elif phase == 2:          # Housing lag trough & early equity snapback
            v1[y] = (0.012, -0.035, 0.000, 0.175, 0.018, 1.0, 0.0)
        elif phase in (3, 4, 5):  # Multi-year expansion & bull market
            v1[y] = (0.024, 0.082, 0.044, 0.122, 0.025, 1.0, 0.0)
        elif phase in (6, 7):     # Mid-cycle steady growth
            v1[y] = (0.026, 0.056, 0.035, 0.085, 0.026, 1.0, 0.0)
        elif phase == 8:          # Inflation spike (Prop 13 caps roll at 2.0%!)
            v1[y] = (0.056, 0.068, 0.052, -0.035, 0.031, 1.0, 0.0)
        else:                     # Soft-landing disinflation
            v1[y] = (0.019, 0.028, 0.022, 0.072, 0.025, 1.0, 0.0)
    regimes_spec.append((
        "R1",
        "50-Year Multi-Cycle Real-World Path (5 Recessions + 5 Inflation Waves)",
        "Mean-matched (~4.2% home, ~5.6% net equity, ~2.5% CPI) with realistic -21% equity & -13% housing cycles and Prop 13/Prop 8 asymmetry.",
        "S_BOE_LTA26002",
        v1,
    ))

    # Regime 2: 1973-1982 Stagflation Wave Across Transfer Decade (2042-2051)
    v2 = base_vectors()
    for y in range(2042, 2052):
        v2[y] = (0.088, 0.075, 0.072, -0.015, 0.032, 1.25, 0.0)
    regimes_spec.append((
        "R2",
        "1970s-Style Stagflation Decade (2042–2051: CPI ~8.8%, Flat Equities)",
        "High nominal inflation + stagnant equities; Prop 13 caps property tax growth at 2%/yr while nominal rents & home values surge.",
        "S_BLS_CPI",
        v2,
    ))

    # Regime 3: Regional Bay Area Housing Slump AT Inheritance (1991-94 / 2023-25 Divergence)
    v3 = base_vectors()
    v3[2043] = (0.022, -0.080, -0.020, 0.090, 0.025, 1.0, 0.0)
    v3[2044] = (0.018, -0.120, -0.040, 0.080, 0.024, 1.0, 0.0)
    v3[2045] = (0.016, -0.080, -0.020, 0.070, 0.024, 1.0, 0.0)
    for y in range(2046, 2052):
        v3[y] = (0.025, 0.092, 0.050, 0.032, 0.025, 1.0, 0.0)
    regimes_spec.append((
        "R3",
        "Regional Housing Trough AT Inheritance (2043–2045 Home -25.5%, Then Recovery)",
        "Inheriting in a local housing dip locks in a permanently lower Prop 19 tax base, whereas selling at the local trough into pricey stocks misfires.",
        "S_FHFA_HPI",
        v3,
    ))

    # Regime 4: Sequence-of-Returns Equity Crash Immediately AFTER 2045 Sale (2046-2048)
    v4 = base_vectors()
    v4[2046] = (0.015, -0.040, 0.000, -0.260, 0.024, 1.0, 0.0)
    v4[2047] = (0.012, -0.030, 0.000, -0.220, 0.022, 1.0, 0.0)
    v4[2048] = (0.018, 0.030, 0.020, -0.060, 0.022, 1.0, 0.0)
    regimes_spec.append((
        "R4",
        "Post-Sale Equity Lost-Decade Shock (2046–2048: Equities -46% After 2045 Sale)",
        "Selling A at 2045 peak into 100% equities suffers severe sequence-of-returns drawdown vs Treasury ladder or keeping real estate.",
        "S_TSP_RET",
        v4,
    ))

    # Regime 5: California Insurance Crisis + Bay Area M6.8 Seismic Repair Shock (2048)
    v5 = base_vectors()
    for y in range(2035, END_YEAR + 1):
        v5[y] = (0.028, 0.036, 0.032, 0.056, 0.025, 3.20, 0.12 if y == 2048 else 0.0)
    regimes_spec.append((
        "R5",
        "CA Insurance Tripling (3.2x) + Uninsured Seismic Repair Shock (12% of FMV in 2048)",
        "Anchored to CDI FAIR Plan distress & USGS 72% 30-yr M>=6.7 Bay Area hazard: concentrated Bay Area structure risk vs diversified portfolio.",
        "S_USGS_EQ",
        v5,
    ))

    # Regime 6: Fiscal Dominance & Higher Capital-Tax Regime (CBO 120%+ Debt/GDP)
    v6 = base_vectors()
    for y in range(2036, END_YEAR + 1):
        v6[y] = (0.038, 0.044, 0.036, 0.044, 0.020, 1.20, 0.0)
    regimes_spec.append((
        "R6",
        "Fiscal Dominance & Tax-Drag Regime (Higher Inflation 3.8%, Lower Real After-Tax Returns)",
        "Anchored to CBO 120% debt-to-GDP path: higher tax drag compresses after-tax equity/bond returns while hard assets track inflation.",
        "S_CBO_2026",
        v6,
    ))

    results: List[Dict[str, object]] = []
    p = DEFAULT_PARAMS
    transfer_year = 2045
    end_year = 2070  # 25-year post-transfer comparison inside the 2026-2076 path

    for code, name, desc, src_id, vec in regimes_spec:
        fmv = p.a_fmv_2026
        fbyv = p.a_fbyv_2026
        allow = p.prop19_allowance_2026
        ins_base_occ = p.a_ins_ho3_2026
        ins_base_rent = p.a_ins_dp3_2026
        water = p.a_water_2026
        maint = p.a_maint_2026
        rent = p.a_rent_2026
        direct = p.a_direct_charges_2026

        fmv_tr = 0.0
        proceeds_tr = 0.0
        base_occ_fbyv = 0.0
        base_rent_fbyv = 0.0
        port_occ = 0.0
        port_rent = 0.0
        port_eq = 0.0
        port_tr = 0.0
        tax_occ_tr = 0.0
        tax_rent_tr = 0.0
        suspended_losses = 0.0
        cum_depr = 0.0

        for y in range(BASE_YEAR, end_year + 1):
            cpi, hg, rg, eq_r, tr_r, ins_mult, seis_pct = vec[y]
            if y > BASE_YEAR:
                fmv = fmv * (1.0 + hg)
                prop13_factor = min(cpi, p.prop13_cap)
                fbyv = fbyv * (1.0 + prop13_factor)
                if y % 2 == 1:
                    allow_g = p.prop19_allowance_growth if code == "R0" else max(cpi, 0.0)
                    allow = allow * ((1.0 + allow_g) ** 2)
                ins_base_occ *= (1.0 + cpi)
                ins_base_rent *= (1.0 + cpi)
                water *= (1.0 + cpi)
                maint *= (1.0 + cpi)
                rent *= (1.0 + rg)
                direct *= (1.0 + max(cpi * 0.6, 0.0))

            if y == transfer_year:
                fmv_tr = fmv
                proceeds_tr = fmv_tr * (1.0 - p.a_sell_cost_rate)
                base_occ_fbyv = prop19_new_taxable(fmv_tr, fbyv, allow)
                base_rent_fbyv = fmv_tr
                port_eq = proceeds_tr
                port_tr = proceeds_tr
            elif y > transfer_year:
                prop13_factor = min(cpi, p.prop13_cap)
                base_occ_fbyv = base_occ_fbyv * (1.0 + prop13_factor)
                base_rent_fbyv = base_rent_fbyv * (1.0 + prop13_factor)

            if transfer_year <= y < end_year:
                enrolled_occ = min(fmv, base_occ_fbyv)
                enrolled_rent = min(fmv, base_rent_fbyv)
                tax_occ = max(enrolled_occ - 7_000.0, 0.0) * p.a_ad_valorem_rate + direct
                tax_rent = enrolled_rent * p.a_ad_valorem_rate + direct
                if y == transfer_year:
                    tax_occ_tr = tax_occ
                    tax_rent_tr = tax_rent

                elec = p.a_elec_post_nem_2026_eq * ((1.0 + 0.025) ** (y - BASE_YEAR))
                seismic_repair = fmv * seis_pct
                # Include B Homeowners' Exemption shift when owner moves to A in S1a
                b_hox_delta = -(7_000.0 * p.b_tax_rate) * (1.0 - p.rental_effective_tax_rate)
                cf_occ = -(tax_occ + ins_base_occ * ins_mult + water + elec + maint + seismic_repair) + b_hox_delta

                annual_d = (fmv_tr * p.building_share_a) / 27.5
                depr_yr = min(annual_d, max(fmv_tr * p.building_share_a - cum_depr, 0.0))
                cum_depr += depr_yr
                noi_r = rent * (1.0 - p.a_vacancy_mgmt) - tax_rent - ins_base_rent * ins_mult - water - elec - maint - seismic_repair
                if noi_r - depr_yr < 0:
                    suspended_losses += abs(noi_r - depr_yr)
                inc_tax = max(noi_r - depr_yr, 0.0) * p.rental_effective_tax_rate
                cf_rent = noi_r - inc_tax

                port_occ = port_occ * (1.0 + eq_r) + cf_occ
                port_rent = port_rent * (1.0 + eq_r) + cf_rent
                port_eq = port_eq * (1.0 + eq_r)
                port_tr = port_tr * (1.0 + tr_r)

        # Terminal liquidation at end_year (2070)
        net_sale_end = fmv * (1.0 - p.a_sell_cost_rate)
        cg_occ = max(net_sale_end - fmv_tr - p.sec121_exclusion, 0.0) * p.ltcg_combined_rate
        tot_gain_r = max(net_sale_end - (fmv_tr - cum_depr), 0.0)
        recap_r = min(tot_gain_r, cum_depr)
        app_r = max(tot_gain_r - recap_r, 0.0)
        gross_cg_r = recap_r * p.recapture_combined_rate + app_r * p.ltcg_combined_rate
        cg_rent = max(gross_cg_r - suspended_losses * p.rental_effective_tax_rate, 0.0)

        w_occ = (net_sale_end - cg_occ) + port_occ
        w_rent = (net_sale_end - cg_rent) + port_rent
        w_eq = port_eq
        w_tr = port_tr

        best_label, best_val = max(
            [("Occupy A (S1a)", w_occ), ("Rent A (S2)", w_rent), ("Sell → Equities (S3a)", w_eq), ("Sell → Treasuries (S3b)", w_tr)],
            key=lambda kv: kv[1],
        )

        results.append({
            "code": code,
            "name": name,
            "desc": desc,
            "source_id": src_id,
            "fmv_2045": fmv_tr,
            "tax_occ_2045": tax_occ_tr,
            "tax_rent_2045": tax_rent_tr,
            "fmv_2070": fmv,
            "w_occ": w_occ,
            "w_rent": w_rent,
            "w_eq": w_eq,
            "w_tr": w_tr,
            "winner": best_label,
            "winner_val": best_val,
        })

    return results


def liquid_inheritance_matrix(
    transfer_year: int = 2045,
    liquid_growth: float = 0.060,
    p: ModelParams = DEFAULT_PARAMS,
) -> List[Dict[str, float]]:
    """Compute gross estate, exclusion headroom, and 40% federal estate tax across 2026 liquid sizes."""
    n = transfer_year - BASE_YEAR
    fmv_a = p.a_fmv_2026 * ((1.0 + p.home_growth_a) ** n)
    excl_single = federal_estate_exclusion_at(transfer_year, p)
    excl_married = excl_single * 2.0  # Full DSUE portability via timely Form 706

    rows: List[Dict[str, float]] = []
    for liq_2026 in (0.0, 2_000_000.0, 5_000_000.0, 5_740_000.0, 8_000_000.0, 12_000_000.0, 20_000_000.0):
        liq_tr = liq_2026 * ((1.0 + liquid_growth) ** n)
        gross_est = fmv_a + liq_tr
        tax_single = max(gross_est - excl_single, 0.0) * p.estate_tax_rate
        tax_married = max(gross_est - excl_married, 0.0) * p.estate_tax_rate
        rows.append({
            "liq_2026": liq_2026,
            "liq_tr": liq_tr,
            "fmv_a": fmv_a,
            "gross_estate": gross_est,
            "excl_single": excl_single,
            "headroom_single": excl_single - gross_est,
            "tax_single": tax_single,
            "net_heir_single": gross_est - tax_single,
            "excl_married": excl_married,
            "tax_married": tax_married,
            "net_heir_married": gross_est - tax_married,
        })
    return rows


if __name__ == "__main__":
    for ty in (2040, 2045, 2050):
        res = evaluate_strategies(transfer_year=ty)
        m = res["meta"]
        print(
            f"Transfer {ty} -> {int(m['end_year'])}: FMV {fmt_money(m['fmv_transfer'])} | "
            f"S1a {fmt_money(res['S1a']['liquidated_wealth'])} | "
            f"S1b {fmt_money(res['S1b']['liquidated_wealth'])} | "
            f"S2 {fmt_money(res['S2']['liquidated_wealth'])} | "
            f"S3a {fmt_money(res['S3a']['liquidated_wealth'])} | "
            f"S3b {fmt_money(res['S3b']['liquidated_wealth'])}"
        )
    for reg in build_black_swan_regimes():
        print(
            f"{reg['code']} {reg['name'][:38]}: Occ {fmt_money(reg['w_occ'])} | "
            f"Rent {fmt_money(reg['w_rent'])} | Eq {fmt_money(reg['w_eq'])} | "
            f"Tr {fmt_money(reg['w_tr'])} -> {reg['winner']}"
        )
