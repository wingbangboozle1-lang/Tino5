"""Registers used by the referee pages. Plain data, no logic.

status vocabulary (what the referee itself did on 2026-11-12):
  opened      - the referee opened the official page or document and read the value there
  secondary   - only non-official summaries were found; the operative official text was not read
  transcribed - taken from another session's transcription of an official series; spot-checked where stated

Nothing here is household data. Every figure is a published rate, threshold or official statistic. Places are
not named in page text (the published site's boundary: "the locations are intentionally not named"); the
official links themselves identify the series.
"""

RETRIEVED = "2026-11-12"

# link table: key -> (label, url). Labels never name a place.
L = {
    "irs_new": ("IRS - What's new, estate and gift tax", "https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax"),
    "rp2632": ("IRS - Rev. Proc. 2025-32 (2026 amounts)", "https://www.irs.gov/pub/irs-drop/rp-25-32.pdf"),
    "rp2635": ("IRS - Rev. Proc. 2026-35 (2027 amounts)", "https://www.irs.gov/pub/irs-drop/rp-26-35.pdf"),
    "ir2026133": ("IRS - IR-2026-133 (5 Nov 2026)", "https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2027-taxpayers-continue-to-benefit-from-the-working-families-tax-cuts"),
    "tc701": ("IRS - Topic 701, sale of your home", "https://www.irs.gov/taxtopics/tc701"),
    "tc409": ("IRS - Topic 409, capital gains and losses", "https://www.irs.gov/taxtopics/tc409"),
    "tc559": ("IRS - Topic 559, net investment income tax", "https://www.irs.gov/taxtopics/tc559"),
    "tc425": ("IRS - Topic 425, passive activities", "https://www.irs.gov/taxtopics/tc425"),
    "tc704": ("IRS - Topic 704, depreciation", "https://www.irs.gov/taxtopics/tc704"),
    "p527": ("IRS - Publication 527, residential rental property", "https://www.irs.gov/publications/p527"),
    "p551": ("IRS - Publication 551, basis of assets", "https://www.irs.gov/publications/p551"),
    "ftb26": ("FTB - 2026 California tax rate schedules", "https://www.ftb.ca.gov/forms/2026/2026-540-tax-rate-schedules.pdf"),
    "ftbnews": ("FTB - Tax News, October 2026 (2026 indexing)", "https://www.ftb.ca.gov/about-ftb/newsroom/tax-news/2026/10.html"),
    "rtc17043": ("California Legislative Information - R&TC 17043", "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=17043."),
    "lta25009": ("BOE - Letter To Assessors 2025/009", "https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf"),
    "lta26002": ("BOE - Letter To Assessors 2026/002", "https://www.boe.ca.gov/proptaxes/pdf/lta26002.pdf"),
    "prop19": ("BOE - Proposition 19", "https://www.boe.ca.gov/prop19/"),
    "lta26026": ("BOE - Letter To Assessors 2026/026, Prop 19 questions and answers", "https://www.boe.ca.gov/proptaxes/pdf/lta26026.pdf"),
    "hox": ("BOE - Homeowners' exemption", "https://www.boe.ca.gov/proptaxes/homeowners_exemption.htm"),
    "pub8009": ("BOE - Publication 800-9, death of a property owner", "https://www.boe.ca.gov/pdf/pub800-9.pdf"),
    "sco": ("State Controller - California estate tax", "https://www.sco.ca.gov/ardtax_estate_tax.html"),
    "sco_et1": ("State Controller - estate tax return filing requirements", "https://www.sco.ca.gov/ardtax_taxinfo_estate_return.html"),
    "de300": ("Judicial Council - form DE-300", "https://www.courts.ca.gov/documents/de300.pdf"),
    "selfhelp": ("California Courts - Self-Help, small estates", "https://selfhelp.courts.ca.gov/probate/small-estate"),
    "tax_collector": ("Treasurer & Tax Collector - secured property taxes", "https://sftreasurer.org/property/secured-property-taxes"),
    "cdi": ("California Dept. of Insurance - Sustainable Insurance Strategy", "https://www.insurance.ca.gov/01-consumers/180-climate-change/sustainable-insurance-strategy.cfm"),
    "cdi_eq": ("California Dept. of Insurance - 2025 premium data summary", "https://www.insurance.ca.gov/0400-news/0200-studies-reports/0300-earthquake-study/upload/EQEXP2025Summary.pdf"),
    "cbo": ("CBO - Budget and Economic Outlook 2026-2036, executive summary", "https://www.cbo.gov/system/files/2026-02/61882-Executive-Summary.pdf"),
    "ssa": ("SSA - 2026 Trustees Report, economic assumptions (V.B)", "https://www.ssa.gov/oact/tr/2026/V_B_econ.html"),
    "tsp": ("Thrift Savings Plan - C Fund performance", "https://www.tsp.gov/c-fund/"),
    "fred_a": ("FHFA House Price Index, local metro series (via FRED)", "https://fred.stlouisfed.org/data/ATNHPIUS41940Q.txt"),
    "fhfa": ("FHFA - House Price Index", "https://www.fhfa.gov/data/hpi"),
    "leginfo": ("California Legislative Information", "https://leginfo.legislature.ca.gov/"),
    "hud_fmr": ("HUD - Fair Market Rents", "https://www.huduser.gov/portal/datasets/fmr.html"),
    "county_rates": ("County Auditor - 2025-26 tax rate book", "https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf"),
    "bls_cpi": ("BLS - Consumer Price Index", "https://www.bls.gov/cpi/"),
    "erp55": ("Economic Report of the President 2026, Table B-55", "https://www.govinfo.gov/content/pkg/ERP-2026/pdf/ERP-2026-table55.pdf"),
    "erp56": ("Economic Report of the President 2026, Table B-56", "https://www.govinfo.gov/content/pkg/ERP-2026/pdf/ERP-2026-table56.pdf"),
}

# ---------------------------------------------------------------------------------------------------------
# A. Official constants. id, topic, value (as printed by the source), link keys, status, used by, note
# ---------------------------------------------------------------------------------------------------------
CONSTANTS = [
    ("K01", "Federal basic exclusion amount, decedents dying in 2026", "$15,000,000",
     ["irs_new", "rp2632"], "opened", "desk-b4f; public-safe", "Rev. Proc. 2025-32 section 2.14 and the IRS What's new page agree."),
    ("K02", "Federal basic exclusion amount, decedents dying in 2027", "$15,480,000",
     ["rp2635", "ir2026133"], "opened", "desk-b4f", "Rev. Proc. 2026-35 section 3.44. Published 5 November 2026."),
    ("K03", "Annual gift-tax exclusion, 2027 (2026: $19,000)", "$20,000",
     ["rp2635", "ir2026133"], "opened", "desk-b4f", "Rev. Proc. 2026-35 section 3.46(1)."),
    ("K04", "Annual exclusion for gifts to a non-citizen spouse, 2027 (2026: $194,000)", "$201,000",
     ["rp2635", "ir2026133"], "opened", "desk-b4f", "Rev. Proc. 2026-35 section 3.46(2)."),
    ("K05", "Federal ordinary-income brackets, 2027: where 35% and 37% begin",
     "35% from $264,550 (single) and $529,100 (joint); 37% from $793,650 (joint)",
     ["rp2635"], "opened", "desk-b4f (rates assumed)", "Rev. Proc. 2026-35 section 3.01, Tables 1 and 3. The desks apply one top-bracket rate to every dollar; see X03."),
    ("K06", "Home-sale exclusion (IRC section 121)", "$250,000 single; $500,000 joint; owned and used 2 of the last 5 years",
     ["tc701"], "opened", "desk-b4f (occupy path)", ""),
    ("K07", "Maximum federal rate on unrecaptured section 1250 gain", "25%",
     ["tc409"], "opened", "desk-b4f (rent path)", ""),
    ("K08", "Long-term capital-gain 0% and 15% ceilings, 2027 (joint / single)", "$102,100 and $633,600 / $51,050 and $563,200",
     ["rp2635"], "opened", "desk-b4f", "Rev. Proc. 2026-35 section 3.03. The 20% rate applies above the 15% ceiling."),
    ("K09", "Net investment income tax", "3.8% above modified AGI of $250,000 joint / $200,000 single",
     ["tc559"], "opened", "desk-b4f", "Estates and trusts have a separate, much lower threshold."),
    ("K10", "Passive losses", "Disallowed losses carry forward; may be deducted in full when the entire interest is disposed of",
     ["tc425"], "opened", "desk-b4f (rent path)", ""),
    ("K11", "California 12.3% bracket begins, tax year 2026 (single / joint)", "$768,213 / $1,536,426",
     ["ftb26", "ftbnews"], "opened", "desk-b4f", "FTB published the 2026 schedules; Tax News says complete 2026 tables follow in late December."),
    ("K12", "California additional tax on taxable income above $1,000,000", "1%",
     ["rtc17043"], "opened", "desk-b4f (inside its 13.3%)", "Statute text read. Applies only to the portion above $1,000,000."),
    ("K13", "Prop 19 value-limit allowance, transfers 16 Feb 2025 - 15 Feb 2027", "$1,044,586",
     ["lta25009"], "opened", "desk-b4f; public-safe (no number)", "Earlier amounts: $1,000,000 (2021-23) and $1,022,600 (2023-25)."),
    ("K14", "Prop 19 allowance adjustment rule",
     "Every other 16 February from 2023, by the FHFA California house-price change for the prior calendar year (2.15% for 2024); next in February 2027",
     ["lta25009"], "opened", "desk-b4f grows it 2%/yr", "Reconciled in check C3 on the desk-check page."),
    ("K15", "Prop 13 inflation factor, 2026-27", "1.02 (California CPI +3.307%, capped at 2%)",
     ["lta26002"], "opened", "desk-b4f (2% growth)", "The factor was below 1.02 in 11 of the 51 roll years 1976-77 to 2026-27; lowest 0.99763 in 2010-11."),
    ("K16", "Homeowners' exemption", "$7,000 off taxable value; principal residence on 1 January; file by 15 February for the full year",
     ["hox", "prop19"], "opened", "desk-b4f (occupy path)", "Claim form BOE-266. For the family-home exclusion the claim must be filed within one year of the transfer."),
    ("K17", "Prop 19 family-home exclusion: conditions",
     "Principal residence of transferor and transferee; value limit = current taxable value + the adjusted $1,000,000; claim within 3 years or before transfer to a third party",
     ["prop19"], "opened", "desk-b4f; public-safe", "BOE comparison chart; BOE states it is summary information, not legal interpretation."),
    ("K35", "Prop 19 continual-use requirement",
     "The family home must be continually used as the family home by an eligible transferee. If the transferee is no longer eligible for either exemption the exclusion is removed as of that date, and the full cash value established at the change in ownership, factored for inflation, is enrolled on the following lien date",
     ["lta26026"], "opened", "desk-22a32b17", "BOE LTA 2026/026 (3 August 2026): definitions, 'Continual Use Requirement' and 'Filing Requirements' read in full (first 2 of 11 parts); the question-and-answer numbering the desk cites was not checked."),
    ("K18", "Reporting a change in ownership after a death",
     "Within 150 days of death (trustee if held in trust); property is treated as changed ownership on the date of death, not the date of distribution; claim forms BOE-19-P (child) / BOE-19-G (grandchild)",
     ["pub8009"], "opened", "process pages", "BOE-58-H in the same publication is the surviving-cotenant form, not a conflicting form."),
    ("K19", "California estate or inheritance tax", "None for decedents dying on or after 1 January 2005",
     ["sco", "sco_et1"], "opened", "desk-b4f; public-safe", ""),
    ("K20", "Small-estate affidavit limit (Prob. Code 13100), deaths on or after 1 April 2025",
     "$208,850 (deaths 1 Apr 2022 - 31 Mar 2025: $184,500); primary-residence petition (13152): $750,000; next adjustment 1 April 2028",
     ["de300"], "opened", "no published desk", "DE-300 rev. 28 April 2025. The Self-Help page still prints $184,500; see X07."),
    ("K21", "Secured property tax rate, FY2026-27 (county-level, owned multi-unit property)", "1.18162182%",
     ["tax_collector"], "opened", "desk-b4f", ""),
    ("K22", "California average homeowners premium, CDI snapshot of 27 October 2026", "$1,571 (national $1,512)",
     ["cdi"], "opened", "desk-b4f cites CDI", "Page updated 27 October 2026."),
    ("K23", "CDI 2025 statewide average premiums, non-earthquake", "Homeowners $2,339.99; dwelling fire $1,701.60; renters $197.03",
     ["cdi_eq"], "opened", "desk-b4f", "The two CDI averages differ by about 49%; they measure different books of business."),
    ("K24", "CBO baseline, February 2026: consumer price index (Q4 to Q4)", "2.8% (2026), 2.4% (2027), 2.3% (2028 and each year to 2036)",
     ["cbo"], "opened", "desk inflation 2.5%", ""),
    ("K25", "CBO baseline, February 2026: 10-year Treasury notes (annual average)", "4.1% (2026), 4.3% (2027-2030), 4.4% (2031-2036)",
     ["cbo"], "opened", "bond-only stress", ""),
    ("K26", "SSA 2026 Trustees Report: ultimate CPI growth", "2.40% intermediate (3.00% low-cost, 1.80% high-cost), reached in 2028",
     ["ssa"], "opened", "desk inflation 2.5%", ""),
    ("K27", "CPI average annual increase, 1969-2019 (six complete economic cycles)", "3.89% (GDP deflator 3.44%)",
     ["ssa"], "opened", "baselines page", ""),
    ("K28", "TSP C Fund (S&P 500 index) average annual returns, as of October 2026",
     "1 year 12.09%; 5 years 12.03%; 10 years 15.41%; since 29 Jan 1988 inception 11.40%",
     ["tsp"], "opened", "equity cross-check", "Net of a 0.035% expense ratio."),
    ("K29", "Depreciation period for residential rental buildings", "27.5 years, straight line; land is never depreciable",
     ["p527", "tc704"], "secondary", "desk-b4f (rent path)", "Topic 704 confirms land is never depreciable. The 27.5-year figure was not read in operative IRS text; open item F-A1."),
    ("K30", "Income-tax basis of inherited property",
     "Generally fair market value at the date of death (or the alternate valuation date if elected); consistent-basis rule when a Form 706 is filed; exception for appreciated property given to the decedent within one year before death",
     ["p551"], "opened", "desk-b4f; public-safe", "Publication 551 (12/2025), 'Inherited Property'."),
    ("K31", "Estates and trusts: where the top bracket begins (2026 / 2027)", "37% above $16,000 / above $16,500",
     ["rp2632", "rp2635"], "opened", "desk-b4f", "Rev. Proc. 2025-32 Table 5; Rev. Proc. 2026-35 Table 5."),
    ("K32", "Estates and trusts: 15% capital-gain ceiling (2026 / 2027)", "$16,250 / $16,750",
     ["rp2632", "rp2635"], "opened", "desk-b4f", "Rev. Proc. 2025-32 section 4.03; Rev. Proc. 2026-35 section 3.03. See X04."),
    ("K33", "Estate tax closing letter user fee", "$76 from 26 October 2026 (previously $56)",
     ["irs_new"], "opened", "desk-b4f", "See X05."),
    ("K34", "Special-use valuation cap, section 2032A (2027); 2% portion of deferred estate tax, section 6166 (2027)", "$1,500,000; $2,010,000",
     ["rp2635"], "opened", "desk-b4f", "Rev. Proc. 2026-35 sections 3.45 and 3.56."),
]

# ---------------------------------------------------------------------------------------------------------
# B. Statutory items the unpublished desk shows, compared with the official source:
#    id, item, desk value, official value, result, link keys
# ---------------------------------------------------------------------------------------------------------
DESK_STATUTORY = [
    ("D01", "Federal basic exclusion 2026 / 2027", "$15,000,000 / $15,480,000", "$15,000,000 / $15,480,000", "match", ["irs_new", "rp2635"]),
    ("D02", "Annual gift exclusion 2027; non-citizen spouse 2027", "$20,000; $201,000", "$20,000; $201,000", "match", ["rp2635"]),
    ("D03", "Estates and trusts: top 37% bracket begins 2026 / 2027", "$16,000 / $16,500", "$16,000 / $16,500", "match", ["rp2632", "rp2635"]),
    ("D04", "Estates and trusts: 15% capital-gain ceiling 2027", "$16,750", "$16,750", "match", ["rp2635"]),
    ("D05", "Estates and trusts: 15% capital-gain ceiling 2026", "$16,200", "$16,250", "MISMATCH ($50)", ["rp2632"]),
    ("D06", "Individual capital-gain ceilings 2027 (joint 0% / 15%; single 0% / 15%)", "$102,100 / $633,600; $51,050 / $563,200", "same", "match", ["rp2635"]),
    ("D07", "Individual top 37% bracket 2027 (joint; the single threshold also matches after the desk's rounding to $10)", "$793,650", "$793,650", "match", ["rp2635"]),
    ("D08", "California 12.3% bracket begins 2026 (single / joint)", "$768,213 / $1,536,426", "$768,213 / $1,536,426", "match", ["ftb26", "ftbnews"]),
    ("D09", "California additional 1% above $1,000,000", "1% (13.3% top rate)", "1% on the portion above $1,000,000", "match", ["rtc17043"]),
    ("D10", "Estate tax closing letter fee: new fee and date", "$76 from 26 Oct 2026", "$76 from 26 Oct 2026", "match", ["irs_new"]),
    ("D11", "Estate tax closing letter fee: previous fee", "$67", "$56", "MISMATCH ($11)", ["irs_new"]),
    ("D12", "Section 6166 2% portion 2027; section 2032A cap 2027", "$2,010,000; $1,500,000", "$2,010,000; $1,500,000", "match", ["rp2635"]),
    ("D13", "California estate tax", "$0", "none after 2004", "match", ["sco"]),
    ("D14", "Prop 19 allowance from 16 Feb 2025", "$1,044,586", "$1,044,586", "match", ["lta25009"]),
    ("D15", "Prop 13 factor 2026-27; California CPI change", "1.02; 3.307%", "1.02; 3.307%", "match", ["lta26002"]),
    ("D16", "Federal estate headroom lines (2040, 2045, 2050): exclusion minus market value of A", "three lines, rounded to $10", "arithmetic reproduced to the dollar", "match (arithmetic)", ["rp2635"]),
]

# ---------------------------------------------------------------------------------------------------------
# C. Spot checks of series transcribed by session 3a49d618 against pages the referee opened itself.
#    (series, date, transcription value, value on the official page)
# ---------------------------------------------------------------------------------------------------------
SPOT = [
    ("FHFA local metro index, Q4 1976", 23.21, 23.21, "fred_a"), ("FHFA local metro index, Q4 1977", 30.02, 30.02, "fred_a"),
    ("FHFA local metro index, Q4 2021", 463.63, 463.63, "fred_a"), ("FHFA local metro index, Q4 2022", 510.15, 510.15, "fred_a"),
    ("FHFA local metro index, Q4 2023", 546.45, 546.45, "fred_a"), ("FHFA local metro index, Q4 2024", 558.19, 558.19, "fred_a"),
    ("FHFA local metro index, Q4 2025", 560.05, 560.05, "fred_a"),
    ("S&P composite, end of 1975", 90.19, 90.19, "erp55"), ("S&P composite, end of 1976", 107.46, 107.46, "erp55"),
    ("S&P composite, end of 1977", 95.10, 95.10, "erp55"), ("S&P composite, end of 2021", 4766.18, 4766.18, "erp56"),
    ("S&P composite, end of 2025", 6845.50, 6845.50, "erp56"),
    ("S&P dividend-price ratio, 1975 (percent)", 4.31, 4.31, "erp55"), ("S&P dividend-price ratio, 2025 (percent)", 1.24, 1.24, "erp56"),
    ("BOE California CPI change, 2010-11 (percent)", -0.237, -0.237, "lta26002"), ("BOE California CPI change, 2026-27 (percent)", 3.307, 3.307, "lta26002"),
]

# Values that are known to be superseded; a page that shows one as current is flagged for review.
SUPERSEDED = {
    "184,500": "Small-estate limit for deaths before 1 April 2025; DE-300 (rev. April 2025) gives $208,850 for later deaths.",
    "1,022,600": "Prop 19 allowance for transfers 16 Feb 2023 - 15 Feb 2025; the figure is $1,044,586 until 15 Feb 2027.",
}

# Hosts treated as official: government domains plus the named public bodies below.
OFFICIAL_SUFFIXES = (".gov",)
OFFICIAL_HOSTS = {"sfgov.legistar.com", "sfpuc.org", "www.sfpuc.org", "sftreasurer.org", "www.sftreasurer.org",
                  "sfassessor.org", "www.sfassessor.org", "sccassessor.org", "www.sccassessor.org",
                  "fred.stlouisfed.org", "www.stlouisfed.org", "sfwater.org", "www.sfwater.org",
                  "www.courts.ca.gov", "courts.ca.gov", "selfhelp.courts.ca.gov", "www.tsp.gov", "tsp.gov"}


def is_official(host):
    host = (host or "").lower()
    return host.endswith(OFFICIAL_SUFFIXES) or host in OFFICIAL_HOSTS
