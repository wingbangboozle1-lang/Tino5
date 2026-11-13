"""Source register. Each entry was opened on 2026-11-13 unless noted.

status:
  read       - fetched and the cited figure/rule was read on the page or document
  index      - fetched (page or index), cited for the rule only; figures not extracted
  secondary  - NOT an official source; used only to flag a proposal; must be checked at the official site
  unread     - linked for manual review; not opened in this session
"""

SOURCES = [
    ("S01", "IRS - What's New: Estate and gift tax (2026 exclusion $15,000,000; Working Families Tax Cuts Act, P.L. 119-21; Estate Tax Closing Letter fee $56 to $76 from 26 Oct 2026)",
     "IRS", "https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax", "read"),
    ("S02", "IRS - Estate tax (filing threshold table: 2026 = $15,000,000)",
     "IRS", "https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax", "read"),
    ("S03", "IRS Rev. Proc. 2025-32 (2026 inflation adjustments: estates and trusts brackets sec 4.01; max 15% capital gains amount $16,250 sec 4.03; annual gift exclusion $19,000 sec 4.42)",
     "IRS", "https://www.irs.gov/pub/irs-drop/rp-25-32.pdf", "read"),
    ("S04", "26 U.S.C. sec 2001 - Imposition and rate of tax (rate table top bracket 40% above $1,000,000) - Cornell LII copy of the U.S. Code",
     "Cornell Law School LII (copy of U.S. Code)", "https://www.law.cornell.edu/uscode/text/26/2001", "read"),
    ("S05", "26 U.S.C. sec 1014 - Basis of property acquired from a decedent (basis = fair market value at date of death) - Cornell LII copy",
     "Cornell Law School LII (copy of U.S. Code)", "https://www.law.cornell.edu/uscode/text/26/1014", "read"),
    ("S07", "California State Controller - California Estate Tax (no state estate tax for decedents dying on or after 1 Jan 2005)",
     "California State Controller's Office", "https://www.sco.ca.gov/ardtax_estate_tax.html", "read"),
    ("S08", "BOE - Proposition 19 (principal residence rule; value cap = factored base year value + $1 million; other real property exclusion eliminated; filing deadlines)",
     "California State Board of Equalization", "https://www.boe.ca.gov/prop19/", "read"),
    ("S09", "BOE Letter to Assessors 2025/009 - Intergenerational transfer exclusion: $1 million amount adjusted to $1,044,586 for transfers 16 Feb 2025 to 15 Feb 2027; next adjustment Feb 2027",
     "California State Board of Equalization", "https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf", "read"),
    ("S10", "BOE Information Sheet 'Death of a Real Property Owner - Reporting Requirements' (reassessment at date of death; BOE-502-D within 150 days; BOE-19-P; occupancy within one year)",
     "California State Board of Equalization", "https://www.boe.ca.gov/pdf/pub800-9.pdf", "read"),
    ("S11", "BOE Publication 29 'California Property Tax: An Overview' (Prop 13: 1% plus voter-approved bonds; 2% limit; $7,000 homeowners' exemption, rentals excluded; solar exclusion stated to sunset 1 Jan 2027)",
     "California State Board of Equalization", "https://www.boe.ca.gov/proptaxes/pdf/pub29.pdf", "read"),
    ("S12", "County of Santa Clara - Compilation of Tax Rates and Information FY 2025-26 (1% plus bonds; AV increase lesser of CPI or 2%; installment dates; penalties)",
     "County of Santa Clara", "https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf", "read"),
    ("S13", "City & County of San Francisco Treasurer & Tax Collector - Secured Property Taxes (FY 2026-27 secured rate 1.18162182%; due dates; supplemental bills)",
     "City & County of San Francisco", "https://sftreasurer.org/property/secured-property-taxes", "read"),
    ("S14", "Federal Reserve - Statement on Longer-Run Goals and Monetary Policy Strategy (2% PCE inflation goal; reaffirmed 27 Jan 2026)",
     "Federal Reserve Board", "https://www.federalreserve.gov/monetarypolicy/files/FOMC_LongerRunGoals.pdf", "read"),
    ("S15", "BLS - Historical Consumer Price Index for All Urban Consumers (CPI-U), monthly, 1913 onward (Dec values 1972-1982 used for black-swan history)",
     "U.S. Bureau of Labor Statistics", "https://www.bls.gov/cpi/tables/supplemental-files/historical-cpi-u-202402.pdf", "read"),
    ("S16", "PG&E - Solar Billing Plan (monthly credits and charges depend on generation and usage; true-up; Energy Export Bonus only for customers starting before 2028)",
     "PG&E (utility)", "https://www.pge.com/en/clean-energy/solar/getting-started-with-solar/solar-billing-plan.html", "read"),
    ("S17", "California Department of Insurance - Home/Residential Insurance (shop-around guidance; FAIR Plan as insurer of last resort; no premium averages on this page)",
     "California Department of Insurance", "https://www.insurance.ca.gov/01-consumers/105-type/5-residential/index.cfm", "index"),
    ("S18", "California Department of Insurance - Residential Property Insurance Report (Part I premium data, 2008-2023, downloadable workbook)",
     "California Department of Insurance", "https://www.insurance.ca.gov/0400-news/0200-studies-reports/0250-homeowners-study/", "index"),
    ("S19", "SFPUC - Water and power rate schedules (2026-27 water and sewer schedule PDF linked from this page; figures not extracted in this session)",
     "San Francisco Public Utilities Commission", "https://www.sfpuc.org/accounts-services/water-power-and-sewer-rates", "index"),
    ("S20", "San Jose Water Company - Advice Letter 629 (CPUC filing, June 2026; rate-base context only; water service area for the Santa Clara property NOT confirmed)",
     "San Jose Water Company (filed with CPUC)", "https://www.sjwater.com/media/gyqpekkb/al629-ami-ratebase-2026-web.pdf", "index"),
    ("S21", "California Secretary of State - Proposition 40 official voter guide (one-time 5% tax on assets over $1 billion; Nov 3, 2026 ballot)",
     "California Secretary of State", "https://voterguide.sos.ca.gov/propositions/40/", "read"),
    ("S22", "Congress.gov - H.R. 1, 119th Congress (identifier of P.L. 119-21, cited by IRS S01; full text NOT opened in this session)",
     "U.S. Congress", "https://www.congress.gov/bill/119th-congress/house-bill/1/text", "unread"),
    ("S23", "SECONDARY (not official): summary of 2025 Senate STEP Act proposal to end step-up in basis; bill text and status not verified",
     "Weeks Law Firm (secondary commentary)", "https://weekslawfirm.com/senators-propose-sweeping-changes-to-the-taxation-of-estates-and-inherited-gains/", "secondary"),
    ("S25", "Santa Clara County Assessor - where the assessed value and market value for Property A can be checked (site NOT opened in this session; linked for manual check)",
     "County of Santa Clara Assessor", "https://www.sccassessor.org/", "unread"),
    ("S26", "San Francisco Assessor-Recorder - where the assessed value and market value for Property B can be checked (site NOT opened in this session; linked for manual check)",
     "City & County of San Francisco Assessor-Recorder", "https://www.sfassessor.org/", "unread"),
    ("S27", "Santa Clara County Tax Collector - where the Property A tax bill and rate can be checked (site NOT opened in this session; linked for manual check)",
     "County of Santa Clara Tax Collector", "https://www.scctax.org/", "unread"),
    ("S24", "CDI Residential Property Insurance Report - Part I workbook (average written premium by policy type and year; NOT parsed in this session)",
     "California Department of Insurance", "https://www.insurance.ca.gov/0400-news/0200-studies-reports/0250-homeowners-study/upload/A-Part-I-Data-Summary.xlsx", "unread"),
]

SRC = {s[0]: {"id": s[0], "title": s[1], "publisher": s[2], "url": s[3], "status": s[4]} for s in SOURCES}

STATUS_LABEL = {
    "read": "Read at source",
    "index": "Index only",
    "secondary": "Secondary (not official)",
    "unread": "Not opened",
}
