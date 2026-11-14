# -*- coding: utf-8 -*-
"""
Official source register for the owner-brief decision desk (session arena-cbe837cb).

Rule for this desk: a source is listed here ONLY if the document was retrieved and read
during this session. Anything linked but not opened is listed in NOT_OPENED and every row
that leans on it says so in the cell. No secondary source (news, law firm, blog) is used
for a value; a secondary source may only appear in the law-watch narrative and is labelled
secondary there.

Hosts allowed in published output (external links must be on this list):
"""

OFFICIAL_HOSTS = {
    "www.irs.gov",
    "www.boe.ca.gov",
    "boe.ca.gov",
    "www.ftb.ca.gov",
    "leginfo.legislature.ca.gov",
    "sftreasurer.org",
    "www.sos.ca.gov",
    "voterguide.sos.ca.gov",
    "electionresults.sos.ca.gov",
    "www.bls.gov",
    "data.bls.gov",
    "www.fhfa.gov",
    "www.insurance.ca.gov",
    "www.congress.gov",
    "crsreports.congress.gov",
}

SOURCES = [
    # ------------------------------------------------------------ federal: estate
    dict(
        id="irs_estate_tax",
        publisher="Internal Revenue Service",
        title="Estate tax (filing threshold for year of death)",
        url="https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax",
        evidences=(
            "Filing threshold by year of death, published as a table: 2011 $5,000,000; "
            "2018 $11,180,000; 2024 $13,610,000; 2025 $13,990,000; 2026 $15,000,000. "
            "Portability: from 1 Jan 2011 an estate survived by a spouse may elect to pass "
            "the unused exemption to the surviving spouse on a timely filed return."
        ),
        checked="Retrieved and read 2026-11-14. The threshold table was transcribed row by row.",
    ),
    dict(
        id="irs_ir2026_133",
        publisher="Internal Revenue Service",
        title="News release IR-2026-133, 5 November 2026 — tax year 2027 inflation adjustments",
        url=(
            "https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-"
            "year-2027-taxpayers-continue-to-benefit-from-the-working-families-tax-cuts"
        ),
        evidences=(
            "Estates of decedents who die during 2027 have a basic exclusion amount of "
            "$15,480,000, up from $15,000,000 for 2026. Annual gift exclusion $20,000 for "
            "2027, up from $19,000 for 2026. Top income rate remains 37% over $661,375 "
            "single / $793,650 married filing jointly for 2027."
        ),
        checked="Retrieved and read 2026-11-14. The estate, gift and marginal-rate passages were read verbatim.",
    ),
    dict(
        id="irs_rp2026_35",
        publisher="Internal Revenue Service",
        title="Revenue Procedure 2026-35 (tax year 2027 inflation adjustments)",
        url="https://www.irs.gov/pub/irs-drop/rp-26-35.pdf",
        evidences="The revenue procedure that carries the 2027 statutory amounts announced in IR-2026-133.",
        checked=(
            "NOT OPENED this session: the PDF fetch failed twice (2026-11-14). Listed only as a "
            "'check here' link. Every 2027 figure on this desk is taken from IR-2026-133, which was read."
        ),
    ),
    dict(
        id="irs_estate_faq",
        publisher="Internal Revenue Service",
        title="Frequently asked questions on estate taxes",
        url="https://www.irs.gov/businesses/small-businesses-self-employed/frequently-asked-questions-on-estate-taxes",
        evidences=(
            "The Working Families Tax Cuts Bill was signed into law on 4 July 2025 as Public Law "
            "119-21 and amends section 2010(c)(3) by increasing the basic exclusion amount to "
            "$15,000,000 for gifts for calendar year 2026. Filing threshold table reproduced. "
            "Portability: the estate's representative must file Form 706 within nine months of "
            "death, with an automatic six-month extension on Form 4768; a return must be filed to "
            "elect portability regardless of the size of the estate. Rev. Proc. 2022-32 gives a "
            "simplified method for a late portability election where there is no filing requirement. "
            "The user fee for an estate tax closing letter (Letter 627) is $67, effective 28 October "
            "2021 under TD 9957."
        ),
        checked="Retrieved and read 2026-11-14. The threshold table, the Public Law 119-21 passage, the portability timetable and the $67 fee were read verbatim.",
    ),
    dict(
        id="irs_i706",
        publisher="Internal Revenue Service",
        title="Instructions for Form 706 (07/2026)",
        url="https://www.irs.gov/instructions/i706",
        evidences="Estate tax return filing rules for the year of death.",
        checked="Linked from the IRS estate tax page on 2026-11-14. NOT OPENED; 'check here' only.",
    ),
    # ------------------------------------------------------------ federal: income
    dict(
        id="irs_tc409",
        publisher="Internal Revenue Service",
        title="Topic no. 409, Capital gains and losses",
        url="https://www.irs.gov/taxtopics/tc409",
        evidences=(
            "Long-term net capital gain rates 0% / 15% / 20%; 2025 thresholds ($48,350 single, "
            "$96,700 joint for the 0% rate; 15% ceiling $533,400 single, $600,050 joint); 25% "
            "maximum on unrecaptured section 1250 gain; 28% on collectibles and section 1202 stock; "
            "net short-term gain taxed as ordinary income."
        ),
        checked="Retrieved and read 2026-11-14. All quoted rates and thresholds confirmed in the text.",
    ),
    dict(
        id="irs_niit",
        publisher="Internal Revenue Service",
        title="Questions and Answers on the Net Investment Income Tax",
        url="https://www.irs.gov/newsroom/questions-and-answers-on-the-net-investment-income-tax",
        evidences=(
            "NIIT is 3.8% under section 1411; thresholds $250,000 married filing jointly, "
            "$200,000 single, $125,000 married filing separately; the thresholds are NOT indexed "
            "for inflation. Gain excluded under section 121 is also excluded from the NIIT. "
            "Rental income and gain from the sale of investment real estate are net investment income."
        ),
        checked="Retrieved and read 2026-11-14. Rate, thresholds, non-indexation and the section 121 interaction confirmed.",
    ),
    dict(
        id="irs_p551",
        publisher="Internal Revenue Service",
        title="Publication 551 (12/2025), Basis of Assets",
        url="https://www.irs.gov/publications/p551",
        evidences=(
            "Basis of assets; the 'Basis Other Than Cost' part of the publication covers property "
            "acquired from a decedent and the fair market value definition."
        ),
        checked=(
            "Retrieved 2026-11-14; the table of contents was read and the 'Basis Other Than Cost' "
            "section located. The section text itself was NOT opened, so basis rules are cited here as "
            "'check here' and the desk relies on Topic 409 and the IRS estate tax page for the figures it asserts."
        ),
    ),
    # ---------------------------------------------------- california: property tax
    dict(
        id="boe_pub29",
        publisher="California State Board of Equalization",
        title="Publication 29, California Property Tax: An Overview (March 2025)",
        url="https://www.boe.ca.gov/proptaxes/pdf/pub29.pdf",
        evidences=(
            "Proposition 13 (June 1978): 1% rate ceiling plus the rate needed to fund voter-approved "
            "bonded indebtedness; reassessment to current market value only on a change in ownership "
            "or completion of new construction; annual increase in base year value limited to no more "
            "than 2%; property tax raised more than $89 billion for local government in 2022-23. "
            "Key dates: 1 January lien date, 15 February exemption deadline, 10 December and 10 April "
            "installment deadlines."
        ),
        checked="Retrieved and read 2026-11-14. The Proposition 13 and disparities sections and the dates table were read.",
    ),
    dict(
        id="leginfo_rtc63_2",
        publisher="California Legislative Information",
        title="Revenue and Taxation Code section 63.2 — exclusion of intergenerational transfers of a family home or family farm from change in ownership",
        url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2",
        evidences=(
            "The statute behind the Proposition 19 intergenerational exclusion, amended by Stats. 2025 "
            "Ch. 539 Sec. 2 (SB 293), effective 1 January 2026. (a)(1)(A): the transfer must be of the "
            "transferor's principal residence and become the principal residence of the transferee "
            "within one year of the transfer. (a)(1)(B): the transferee must file for the homeowners' "
            "or disabled veterans' exemption within a year, and the exclusion is removed on the date "
            "an eligible transferee is no longer eligible for either exemption. (a)(1)(C): on removal, "
            "the base year value established as of the change in ownership date, adjusted annually "
            "under Article XIII A Section 51(a)(1), is enrolled. (d): the new taxable value is the "
            "factored base year value plus zero if fair market value is below that value plus "
            "$1,000,000, otherwise fair market value minus the sum of that value and $1,000,000. "
            "(c): a claim filed under this section is not a public document and is not open to public "
            "inspection. (e)(5): family home means a dwelling eligible for the homeowners' exemption "
            "as a result of the transferor's ownership and occupation, and includes only so much of "
            "the land as is a site of reasonable size for the residence. (e)(8): real property does "
            "not include any interest in a legal entity. (e)(9): transfer includes a transfer of "
            "present beneficial ownership through an inter vivos or testamentary trust. (f)(1)(A): "
            "the claim is filed within three years, or before transfer to a third party, or before an "
            "eligible transferee no longer occupies the residence, whichever is earliest. (f)(1)(B): "
            "a claim is timely if filed within six months of the mailing of a supplemental or escape "
            "assessment notice. (g): where the assessor sends a notice of potential eligibility the "
            "certified claim is due in 45 days, extendable by a second notice to 60 days, and a late "
            "claim may carry a one-time processing fee of the lesser of actual cost or $175."
        ),
        checked="Retrieved and read in full 2026-11-14: subdivisions (a) through (h) were read.",
    ),
    dict(
        id="boe_prop19",
        publisher="California State Board of Equalization",
        title="Proposition 19 — Home Protection for Seniors, Severely Disabled, Families, and Victims of Wildfire or Natural Disasters Act",
        url="https://www.boe.ca.gov/prop19/",
        evidences=(
            "Comparison chart (Proposition 58/193 vs Proposition 19): under Proposition 19 the principal "
            "residence must be the principal residence of BOTH the transferor and the transferee; the value "
            "limit is the current taxable value plus $1,000,000 as biennially adjusted; the exclusion for "
            "other real property is eliminated; the homeowner's exemption claim must be filed within 1 year "
            "and the exclusion claim within 3 years; implementing statute is Revenue and Taxation Code "
            "section 63.2, operative 16 February 2021. FAQ: a rental home does not qualify."
        ),
        checked="Retrieved and read 2026-11-14 (comparison charts and the Parent-Child and Grandparent-Grandchild FAQ items 1-6).",
    ),
    dict(
        id="boe_lta2025_009",
        publisher="California State Board of Equalization",
        title="Letter To Assessors No. 2025/009 — Intergenerational Transfer Exclusion, Adjustment of the $1 Million Amount (7 March 2025)",
        url="https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf",
        evidences=(
            "The value cap is the property's factored base year value plus $1,044,586 for transfers "
            "16 February 2025 through 15 February 2027; prior amounts $1,000,000 (2021-2023) and "
            "$1,022,600 (2023-2025); the next adjustment is February 2027; the amount tracks the "
            "percentage change in the Federal Housing Finance Agency House Price Index for California, "
            "which was 2.15% for 2024."
        ),
        checked="Retrieved and read in full 2026-11-14. All three amounts, the dates and the 2.15% figure confirmed verbatim.",
    ),
    dict(
        id="boe_lta2026_026",
        publisher="California State Board of Equalization",
        title="Letter To Assessors No. 2026/026 — Proposition 19 Intergenerational Transfer Exclusion Frequently Asked Questions and Answers (3 August 2026)",
        url="https://www.boe.ca.gov/proptaxes/pdf/lta26026.pdf",
        evidences=(
            "Definitions of excluded amount (factored base year value plus $1 million, adjusted every "
            "other 16 February) and excess amount. Continual use requirement: the family home must be "
            "continually used as the family home by an eligible transferee; if the home becomes ineligible "
            "for the homeowner's or disabled veterans' exemption the exclusion is removed. Q13: the "
            "transferee must occupy within one year of the transfer and the exemption claim must be filed "
            "within one year. Q15: each unit of a multi-unit property is a separate principal residence. "
            "Q32-Q35: property held by a legal entity (including a single-member LLC) is not eligible. "
            "Q39: transfers through a trust are eligible — the trust is looked through to present "
            "beneficial ownership. Filing checklist: BOE-266 or BOE-261-G within 1 year; BOE-19-G within "
            "3 years or before transfer to a third party."
        ),
        checked=(
            "Retrieved and read 2026-11-14: the definitions block, the continual-use section, and "
            "questions 10-15, 31-35 and 36-41 were read."
        ),
    ),
    dict(
        id="boe_lta2021_054",
        publisher="California State Board of Equalization",
        title="Letter To Assessors No. 2021/054 — Property Tax Rule 462.520, Exclusion from Change in Ownership: Intergenerational Transfers",
        url="https://www.boe.ca.gov/proptaxes/pdf/lta21054.pdf",
        evidences="Rule 462.520 was adopted after a public hearing on 27 July 2021 and became effective 1 January 2022.",
        checked="NOT OPENED this session (identified through search results only). 'Check here' only.",
    ),
    # ------------------------------------------------------ california: income tax
    dict(
        id="ftb_2025_rates",
        publisher="California Franchise Tax Board",
        title="2025 California Tax Rate Schedules (Form 540)",
        url="https://www.ftb.ca.gov/forms/2025/2025-540-tax-rate-schedules.pdf",
        evidences=(
            "Nine brackets, 1% to 12.3%. Schedule X (single / married filing separately): 12.3% applies "
            "above $742,953. Schedule Y (married filing jointly / surviving spouse): 12.3% above "
            "$1,485,906. Schedule Z (head of household): 12.3% above $1,010,417."
        ),
        checked="Retrieved and read 2026-11-14. All three schedules were transcribed row by row.",
    ),
    dict(
        id="leginfo_rtc17043",
        publisher="California Legislative Information",
        title="Revenue and Taxation Code section 17043",
        url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=17043",
        evidences=(
            "For each taxable year beginning on or after 1 January 2005 an additional tax of 1 percent is "
            "imposed on that portion of a taxpayer's taxable income in excess of one million dollars. "
            "Added 2 November 2004 by initiative Proposition 63, section 12."
        ),
        checked=(
            "Retrieved and read 2026-11-14. This is the statute that closes flag F12 of the earlier "
            "consolidated desk: the 1% surcharge over $1,000,000 is in the code, so the 13.3% top "
            "California marginal rate (12.3% + 1%) is confirmed from an official source."
        ),
    ),
    dict(
        id="leginfo_rtc13301",
        publisher="California Legislative Information",
        title="Revenue and Taxation Code section 13301",
        url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=13301",
        evidences=(
            "Neither the state nor any political subdivision of the state shall impose any gift, "
            "inheritance, succession, legacy, income, or estate tax, or any other tax, on gifts or on the "
            "estate or inheritance of any person or on or by reason of any transfer occurring by reason "
            "of a death."
        ),
        checked="Retrieved and read 2026-11-14. Quoted verbatim.",
    ),
    # ---------------------------------------------------- california: landlord law
    dict(
        id="leginfo_civ1947_12",
        publisher="California Legislative Information",
        title="Civil Code section 1947.12 (statewide rent increase cap)",
        url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12",
        evidences=(
            "An owner may not increase gross rent over any 12-month period by more than 5 percent plus "
            "the percentage change in the cost of living, or 10 percent, whichever is lower. Exemptions "
            "include: (d)(4) housing with a certificate of occupancy issued within the previous 15 years; "
            "(d)(5) residential real property alienable separate from the title to any other dwelling unit "
            "(a single-family home) where the owner is not a REIT, a corporation, or an LLC with a "
            "corporate member, AND the tenant has been given the statutory written notice; (d)(6) a "
            "property containing two separate dwelling units in one structure where the owner occupied one "
            "unit at the start of the tenancy and continues in occupancy. A new tenancy may be set at "
            "market (subdivision (b))."
        ),
        checked="Retrieved and read 2026-11-14 (subdivisions (a) through (i), including the full exemption list and the notice text).",
    ),
    dict(
        id="leginfo_prob16061_7",
        publisher="California Legislative Information",
        title="Probate Code section 16061.7 (trustee's notification on irrevocability)",
        url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PROB&sectionNum=16061.7",
        evidences=(
            "When a revocable trust becomes irrevocable on the death of a settlor the trustee shall serve "
            "a notification on each beneficiary and each heir of the deceased settlor within 60 days, "
            "served in the manner provided by section 1215 to the last known address."
        ),
        checked="Retrieved and read 2026-11-14 (subdivisions (a) through (g)).",
    ),
    # --------------------------------------------------------------- local: tax
    dict(
        id="sftreasurer_secured",
        publisher="Office of the Treasurer and Tax Collector",
        title="Secured Property Taxes",
        url="https://sftreasurer.org/property/secured-property-taxes",
        evidences=(
            "The secured property tax rate for Fiscal Year 2026-27 is 1.18162182%. Secured bills are "
            "mailed in October. Installments are delinquent after 10 December (10% penalty) and 10 April "
            "(10% plus fees). A supplemental assessment follows a change in ownership or completed new "
            "construction."
        ),
        checked="Retrieved and read 2026-11-14. The rate and the installment dates were read verbatim.",
    ),
    dict(
        id="sftreasurer_heirs",
        publisher="Office of the Treasurer and Tax Collector",
        title="Information for Heirs",
        url="https://sftreasurer.org/property/information-heirs",
        evidences=(
            "Procedure for absent or missing heirs: money deposited with the Treasurer is claimed by "
            "petition under Probate Code section 11854; unclaimed funds move to the State Controller's "
            "Office after one year."
        ),
        checked="Retrieved and read 2026-11-14.",
    ),
    # ------------------------------------------------------------- economy: BLS
    dict(
        id="bls_cpi_series",
        publisher="U.S. Bureau of Labor Statistics",
        title="CPI-U, all items, U.S. city average, not seasonally adjusted (series CUUR0000SA0), all years",
        url="https://data.bls.gov/timeseries/CUUR0000SA0?years_option=all_years&period=M13&output_view=data&include_graphs=false",
        evidences=(
            "Monthly index values, 1982-84 = 100, January 1913 through October 2026. October 2025 is "
            "missing because BLS did not collect survey data during the 2025 lapse in appropriations. "
            "October 2026 index level 337.511."
        ),
        checked=(
            "Retrieved 2026-11-14 (extraction stamp on the page: 13 November 2026). Both chunks of the "
            "table were read and the monthly series is reproduced in this desk's data module."
        ),
    ),
    dict(
        id="bls_cpi_home",
        publisher="U.S. Bureau of Labor Statistics",
        title="Consumer Price Index home page",
        url="https://www.bls.gov/cpi/",
        evidences=(
            "12-month percent changes, September 2026, not seasonally adjusted: all items 3.7%; "
            "all items less food and energy 2.6%; energy 20.4%; gasoline (all types) 34.2%; fuel oil "
            "74.2%; electricity 4.4%; shelter 3.2%; owners' equivalent rent of residences 3.3%; "
            "rent of primary residence 2.8%."
        ),
        checked="Retrieved and read 2026-11-14. The chart's underlying table was read.",
    ),
    dict(
        id="bls_cpi_oct2026",
        publisher="U.S. Bureau of Labor Statistics",
        title="Consumer Price Index Summary, October 2026 (USDL-26-1685, released 10 November 2026)",
        url="https://www.bls.gov/news.release/cpi.nr0.htm",
        evidences=(
            "CPI-U rose 0.4% in October 2026 on a seasonally adjusted basis after rising 0.6% in "
            "September. The index level reached 337.511 (1982-84 = 100). BLS did not collect survey data "
            "for October 2025 because of a lapse in appropriations, so 12-month percent changes cannot be "
            "published for most October 2026 series; gasoline, for which October 2025 data exist, is up "
            "37.4% over 12 months."
        ),
        checked="Retrieved and read 2026-11-14.",
    ),
    # ------------------------------------------------------------ economy: FHFA
    dict(
        id="fhfa_hpi",
        publisher="Federal Housing Finance Agency",
        title="FHFA House Price Index datasets",
        url="https://www.fhfa.gov/data/house-price-index",
        evidences=(
            "The official house price index for single-family homes, back to the mid-1970s, published as "
            "purchase-only (sales price) and all-transactions (sales and appraisal) indexes for the U.S., "
            "census divisions, states and metropolitan areas. The state and metro files are the series "
            "the Board of Equalization uses to adjust the Proposition 19 allowance."
        ),
        checked=(
            "Retrieved and read 2026-11-14. The dataset index page was read and the download links "
            "confirmed; the data files themselves were not downloaded into this desk, so no index "
            "value from this source is quoted."
        ),
    ),
    # --------------------------------------------------------------- insurance
    dict(
        id="cdi_residential",
        publisher="California Department of Insurance",
        title="Residential Property Insurance Report",
        url="https://www.insurance.ca.gov/0400-news/0200-studies-reports/0250-homeowners-study/",
        evidences=(
            "Part I: written premiums, exposures and average written premiums by policy form for "
            "2008-2023. Part II: ZIP-code-level experience (coverage amounts, earned premiums, wildfire "
            "risk, fire and smoke claims) for 2018-2023, produced under Insurance Code section 929. "
            "Structures of 5 or more residential units are excluded because they are written under a "
            "commercial policy."
        ),
        checked=(
            "Retrieved and read 2026-11-14. The report index was read; the data files were not "
            "downloaded, so no ZIP-level average premium is quoted anywhere on this desk."
        ),
    ),
    # --------------------------------------------------------------- elections
    dict(
        id="sos_qualified",
        publisher="California Secretary of State",
        title="Qualified Statewide Ballot Measures",
        url="https://www.sos.ca.gov/elections/ballot-measures/qualified-ballot-measures",
        evidences=(
            "The fourteen measures on the 3 November 2026 statewide general election ballot: "
            "Propositions 1, 2, 3, 4, 5, 37, 38, 39, 40, 41, 42, 43, 44 and 45, with their official "
            "titles. No measure on the list changes Proposition 13 or creates a split roll. "
            "ACA 13 was removed from this ballot on 25 June 2026 by ACA 21 (Res. Ch. 131, 2026)."
        ),
        checked="Retrieved and read 2026-11-14. The full list of fourteen titles was transcribed.",
    ),
    dict(
        id="sos_prop3",
        publisher="California Secretary of State",
        title="Official Voter Information Guide — Proposition 3 (3 November 2026)",
        url="https://voterguide.sos.ca.gov/propositions/3/index.htm",
        evidences=(
            "'Provides Permanent Funding for Schools and Health Care by Extending Existing Tax on High "
            "Incomes. Initiative Constitutional Amendment.' Makes permanent existing voter-approved tax "
            "rates for individuals earning over $371,000 (adjusted annually for inflation); without it "
            "the temporary increase expires in 2031. Fiscal impact: maintains $5 billion to $15 billion "
            "of annual state income tax revenue."
        ),
        checked="Retrieved and read 2026-11-14. Title, summary and fiscal impact read verbatim.",
    ),
    dict(
        id="sos_prop40",
        publisher="California Secretary of State",
        title="Official Voter Information Guide — Proposition 40 (3 November 2026)",
        url="https://voterguide.sos.ca.gov/propositions/40/index.htm",
        evidences=(
            "'Imposes One-Time Tax on Certain Taxpayers. Initiative Constitutional Amendment and "
            "Statute.' Imposes a 5% tax on certain taxpayers with assets over $1 billion, revenue "
            "primarily for health care, and exempts the revenue from the school funding requirement and "
            "the state spending limit. Fiscal impact: a temporary revenue increase of tens of billions "
            "of dollars spread over several years."
        ),
        checked="Retrieved and read 2026-11-14. Title, summary and fiscal impact read verbatim.",
    ),
    dict(
        id="sos_results_bm",
        publisher="California Secretary of State",
        title="State Ballot Measures — statewide results, 3 November 2026 general election",
        url="https://electionresults.sos.ca.gov/returns/ballot-measures",
        evidences=(
            "Unofficial results as of 13 November 2026, 4:21 p.m., 23,860 of 23,860 precincts partially "
            "reporting: Proposition 3 Yes 7,653,400 (60.7%) / No 4,950,766 (39.3%); Proposition 40 Yes "
            "6,058,251 (47.7%) / No 6,640,502 (52.3%); Proposition 42 Yes 6,456,528 (51.3%) / No "
            "6,131,357 (48.7%); Proposition 43 Yes 5,251,471 (42.4%) / No 7,129,221 (57.6%); "
            "Proposition 44 Yes 2,214,283 (17.9%) / No 10,140,521 (82.1%)."
        ),
        checked=(
            "Retrieved and read 2026-11-14. Every figure above is transcribed from the results table. "
            "These are UNOFFICIAL: the page states results will be certified by 11 December 2026."
        ),
    ),
    dict(
        id="sos_results_home",
        publisher="California Secretary of State",
        title="Election Night Results — 2026 General Election (home page)",
        url="https://electionresults.sos.ca.gov/",
        evidences=(
            "County elections officials must report final official results to the Secretary of State by "
            "4 December 2026; the Secretary of State will certify the results on 11 December 2026."
        ),
        checked="Retrieved and read 2026-11-14.",
    ),
]

# Sources referenced by a link but not opened in this session. Every row that leans on one of
# these carries an explicit "not opened — check here" marker in the cell.
NOT_OPENED = ["irs_rp2026_35", "irs_i706", "irs_p551", "boe_lta2021_054", "fhfa_hpi", "cdi_residential"]

# Statutory amounts quoted exactly as published. Statewide constants; they identify nothing,
# so they are deliberately NOT rounded to $10. Everything else on the desk is rounded.
STATUTORY_LITERALS = {
    "1,044,586",   # BOE LTA 2025/009, Prop 19 allowance 16 Feb 2025 - 15 Feb 2027
    "1,022,600",   # BOE LTA 2025/009, Prop 19 allowance 16 Feb 2023 - 15 Feb 2025
    "1,000,000",   # the constitutional base amount (also a threshold, not a household figure)
    "15,000,000",  # IRS, 2026 estate tax basic exclusion
    "15,480,000",  # IRS IR-2026-133, 2027 estate tax basic exclusion
    "13,990,000",  # IRS, 2025 estate tax filing threshold
    "13,610,000",  # IRS, 2024 estate tax filing threshold
    "742,953",     # FTB 2025 Schedule X, 12.3% threshold, single
    "1,485,906",   # FTB 2025 Schedule Y, 12.3% threshold, joint
    "1,010,417",   # FTB 2025 Schedule Z, 12.3% threshold, head of household
    "661,375",     # IRS IR-2026-133, 2027 top bracket, single
    "793,650",     # IRS IR-2026-133, 2027 top bracket, joint
    "371,000",     # SOS voter guide, Proposition 3 income threshold
    "250,000",     # IRS, NIIT threshold, married filing jointly (also the section 121 exclusion)
    "67",           # IRS, estate tax closing letter user fee (TD 9957)
    "175",          # R&TC 63.2(g)(2), maximum assessor processing fee on a late certified claim
    "200,000",     # IRS, NIIT threshold, single
    "19,000",      # IRS IR-2026-133, 2026 annual gift exclusion
    "20,000",      # IRS IR-2026-133, 2027 annual gift exclusion
}


def by_id():
    return {s["id"]: s for s in SOURCES}


def link(sid, label=None):
    """Render an official source link for use inside a table cell."""
    s = by_id()[sid]
    text = label or s["publisher"]
    return (
        '<a class="src" href="%s" target="_blank" rel="noopener noreferrer" '
        'title="%s">%s</a>' % (s["url"], s["title"].replace('"', "&quot;"), text)
    )


def nosrc(reason):
    return '<span class="nosrc">No official source &mdash; %s</span>' % reason
