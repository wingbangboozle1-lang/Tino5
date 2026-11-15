# -*- coding: utf-8 -*-
"""Official source register for the operating desk (session arena-ea3f2cee).

Rule: a source is listed here only if the document was retrieved and opened during this
session (2026-11-15) or is recorded as NOT_OPENED and every row that leans on it says so.
No value in this desk is taken from a news site, a law firm, a blog or an aggregator.

Hosts allowed in published output are the hosts of the entries below.
"""

SOURCES = [
    # ------------------------------------------------------------------ federal: estate
    dict(
        id="irs_estate",
        publisher="Internal Revenue Service",
        title="Estate tax — filing threshold for year of death, portability",
        url="https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax",
        supports=(
            "The filing-threshold table by year of death, transcribed row by row, with the 2026 amount "
            "at fifteen million dollars and the 2025 amount at just under fourteen million. Portability exists "
            "for a decedent survived by a spouse and is made on a timely filed return."
        ),
        opened="2026-11-15. Threshold table and portability paragraph read on the page.",
    ),
    dict(
        id="irs_estate_faq",
        publisher="Internal Revenue Service",
        title="Frequently asked questions on estate taxes",
        url="https://www.irs.gov/businesses/small-businesses-self-employed/frequently-asked-questions-on-estate-taxes",
        supports=(
            "Form 706 is due nine months after death; an automatic six-month extension is "
            "available by filing Form 4768 on or before the due date, including for estates "
            "filing solely to elect portability. A return is required to elect portability "
            "regardless of size. Public Law 119-21 amended IRC 2010(c)(3) to set the basic "
            "exclusion at $15,000,000 for calendar year 2026. Rev. Proc. 2022-32 simplified "
            "late portability (fifth annual anniversary of death)."
        ),
        opened="2026-11-15. The filing, portability, extension and Public Law 119-21 passages were read.",
    ),
    dict(
        id="irs_ir2026_133",
        publisher="Internal Revenue Service",
        title="IR-2026-133 (5 November 2026) — tax year 2027 inflation adjustments",
        url=(
            "https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-"
            "2027-taxpayers-continue-to-benefit-from-the-working-families-tax-cuts"
        ),
        supports=(
            "Estates of decedents who die during 2027 have a basic exclusion amount of "
            "$15,480,000, up from $15,000,000 for 2026. Annual gift exclusion $20,000 for 2027, "
            "up from $19,000 for 2026. Top rate 37% over the published 2027 income thresholds."
        ),
        opened="2026-11-15. The estate, gift and rate-schedule passages were read verbatim.",
    ),
    dict(
        id="irs_niit",
        publisher="Internal Revenue Service",
        title="Questions and answers on the Net Investment Income Tax",
        url="https://www.irs.gov/newsroom/questions-and-answers-on-the-net-investment-income-tax",
        supports=(
            "NIIT is 3.8% (IRC 1411) on net investment income above modified AGI thresholds of "
            "the published joint, separate, single and head-of-household thresholds; the "
            "thresholds are not indexed for inflation. Gain on investment real estate is net "
            "investment income; gain excluded under section 121 is not."
        ),
        opened="2026-11-15. Threshold table and the section 121 interaction were read.",
    ),
    dict(
        id="irs_tc701",
        publisher="Internal Revenue Service",
        title="Topic no. 701, Sale of your home — section 121 exclusion",
        url="https://www.irs.gov/taxtopics/tc701",
        supports=(
            "The published single and joint caps on excluded gain for a main home; the ownership test is 24 months out of the last five years and the use "
            "test is 24 months of the previous five."
        ),
        opened="2026-11-15. Both tests and both amounts were read.",
    ),
    dict(
        id="irs_tc409",
        publisher="Internal Revenue Service",
        title="Topic no. 409, Capital gains and losses",
        url="https://www.irs.gov/taxtopics/tc409",
        supports=(
            "For 2025 a 0% long-term rate applies at the published single and joint thresholds, 15% "
            "above that up to the published 15% ceilings, and 20% above; "
            "unrecaptured section 1250 gain is taxed at a maximum 25%; losses on personal-use "
            "property such as a home are not deductible."
        ),
        opened="2026-11-15. All four rate/threshold statements were read.",
    ),
    dict(
        id="irs_p551",
        publisher="Internal Revenue Service",
        title="Publication 551, Basis of Assets",
        url="https://www.irs.gov/publications/p551",
        supports=(
            "Linked from Topic 409 as the authority for the basis of inherited property. "
            "NOT OPENED this session: the inherited-property basis paragraph is not quoted on "
            "this desk. The basis rule used (date-of-death value) is stated as an assumption "
            "and flagged for the CPA to confirm against Publication 551 and Form 706."
        ),
        opened="NOT OPENED — listed as a check-here link only.",
    ),
    # ------------------------------------------------------------------ federal: market data
    dict(
        id="fed_history_1929",
        publisher="Federal Reserve History (Federal Reserve System)",
        title="Stock Market Crash of 1929",
        url="https://www.federalreservehistory.org/essays/stock-market-crash-of-1929",
        supports=(
            "The Dow peaked on 3 September 1929 at 381.17 and closed at 41.22 on 8 July 1932, "
            "89 percent below its peak; the index did not reach the 1929 high again until "
            "23 November 1954. Black Monday (28 October 1929) was a decline of nearly 13 percent."
        ),
        opened="2026-11-15. The peak, trough, percentage and recovery date were read.",
    ),
    dict(
        id="fed_history_2008",
        publisher="Federal Reserve History (Federal Reserve System)",
        title="The Great Recession, December 2007–June 2009",
        url="https://www.federalreservehistory.org/essays/great-recession-of-200709",
        supports=(
            "The S&P 500 fell 57 percent from its October 2007 peak to its trough in March 2009; "
            "home prices fell approximately 30 percent on average from mid-2006 to mid-2009; the "
            "federal funds rate was cut to a 0–0.25 percent range by December 2008."
        ),
        opened="2026-11-15. The 57 percent drawdown and the 30 percent house-price passage were read.",
    ),
    dict(
        id="treasury_curve",
        publisher="U.S. Department of the Treasury",
        title="Daily Treasury Par Yield Curve Rates",
        url="https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026",
        supports=(
            "Official daily par yield curve. NOT OPENED this session: the rendered table did not "
            "return. The Treasury yield range used for the phased path is therefore an assumption "
            "labelled 'T-bill range' and flagged, not a quoted rate. See flagged page F07."
        ),
        opened="NOT OPENED — the page did not render for this session; flagged.",
    ),
    dict(
        id="bls_cpi",
        publisher="U.S. Bureau of Labor Statistics",
        title="CPI-U, U.S. city average, all items (series CUUR0000SA0)",
        url="https://data.bls.gov/timeseries/CUUR0000SA0?years_option=all_years&period=M13&output_view=data",
        supports=(
            "Official CPI-U monthly and annual-average index. NOT RE-OPENED this session: the "
            "inflation distribution used here is drawn from the 1914–2026 record already "
            "transcribed into this repository at cbe/_src/cpi.py (read this session, source "
            "labelled in that file), not from a fresh retrieval. Flagged F08."
        ),
        opened="Read from the repository's earlier transcription (cbe/_src/cpi.py) on 2026-11-15.",
    ),
    # ------------------------------------------------------------------ California: property tax
    dict(
        id="rtc_63_2",
        publisher="California Legislative Information",
        title="Revenue and Taxation Code section 63.2 — intergenerational transfer exclusion",
        url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2",
        supports=(
            "From 16 February 2021 a change in ownership does not include a transfer of the "
            "transferor's principal residence between parent and child if (A) the property "
            "becomes the transferee's principal residence within one year of the transfer and "
            "(B) the transferee files for the homeowners' or disabled veterans' exemption within "
            "a year, and the exclusion 'shall be removed' on the date the transferee is no longer "
            "eligible for either exemption, with the base year value re-enrolled at the lien date "
            "following (C). Subdivision (b): no exclusion unless a claim is filed. Subdivision (c): "
            "the claim is not a public document."
        ),
        opened="2026-11-15. Subdivisions (a)(1)(A)–(C), (b) and (c) were read.",
    ),
    dict(
        id="boe_lta_2025_009",
        publisher="California State Board of Equalization",
        title="LTA 2025/009 — intergenerational transfer exclusion, adjustment of the one-million-dollar amount",
        url="https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf",
        supports=(
            "The value cap is the property's factored base year value plus the one-million-dollar amount, adjusted "
            "every other 16 February from 2023 for the FHFA California House Price Index. For "
            "transfers occurring 16 February 2025 through 15 February 2027 the amount is "
            "$1,044,586; the prior amount was $1,022,600 (16 Feb 2023 – 15 Feb 2025); the next "
            "adjustment is February 2027."
        ),
        opened="2026-11-15. The letter and its adjustment table were read.",
    ),
    dict(
        id="boe_lta_2026_026",
        publisher="California State Board of Equalization",
        title="LTA 2026/026 — Proposition 19 intergenerational transfer exclusion FAQ",
        url="https://www.boe.ca.gov/proptaxes/pdf/lta26026.pdf",
        supports=(
            "Definitions: the excluded amount is the factored base year value immediately before "
            "transfer plus the adjusted one-million-dollar amount; the excess amount is full cash value at "
            "transfer minus the excluded amount; the new taxable value is the factored base year "
            "value plus the excess. 'The family home ... must be continually used ... by an "
            "eligible transferee ... in order to maintain the intergenerational transfer "
            "exclusion', and the exclusion is removed if the property becomes ineligible for the "
            "homeowners' or disabled veterans' exemption. Transfers include those by death, "
            "'whether within or outside a trust'."
        ),
        opened="2026-11-15. The definitions and the continual-use passage were read.",
    ),
    dict(
        id="boe_prop19",
        publisher="California State Board of Equalization",
        title="Proposition 19 — Board of Equalization resource page",
        url="https://www.boe.ca.gov/prop19/",
        supports=(
            "Index of official Proposition 19 guidance and Letters to Assessors; cites "
            "section 2.1 of article XIII A and RTC 63.2; links LTA 2026/026 as the current "
            "intergenerational FAQ."
        ),
        opened="2026-11-15. The index and the footer note that the page lists the LTA series were read.",
    ),
    dict(
        id="scc_tax_rate_book",
        publisher="County of Santa Clara, Controller-Treasurer",
        title="Compilation of Tax Rates and Information, fiscal year 2025-2026",
        url="https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf",
        supports=(
            "The 1% maximum levy is 1% of assessed value; voter-approved debt is "
            "added on top and varies by tax rate area; the county retirement levy is 0.0388%; "
            "there are 816 tax rate areas in fiscal year 2025-26; assessed value rises each year "
            "by the change in the California CPI or 2%, whichever is less; secured taxes are due "
            "1 November (delinquent 10 December) and 1 February (delinquent 10 April); a 10% "
            "penalty applies after the delinquency date and 1.5% per month redemption penalty "
            "from the following 1 July; supplemental bills are issued for a change in ownership."
        ),
        opened=(
            "2026-11-15. The General Information section (A-1 to A-3) was read. The per-tax-rate-"
            "area rate table (B-1 to B-185) was NOT read for the parcel in question: the rate "
            "area is unknown. See open question Q04 and flagged item F01."
        ),
    ),
    # ------------------------------------------------------------------ California: income, transfer, assessment
    dict(
        id="rtc_17043",
        publisher="California Legislative Information",
        title="Revenue and Taxation Code §17043 — 1% additional tax above one million dollars",
        url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=17043",
        supports=(
            "'an additional tax shall be imposed at the rate of 1 percent on that portion of a "
            "taxpayer's taxable income in excess of one million dollars ($1,000,000)', for each "
            "taxable year beginning on or after 1 January 2005 (Proposition 63). Credits under "
            "the credit provisions, the filing-status recomputation provisions and the "
            "joint-return rule "
            "do not apply to it."
        ),
        opened="2026-11-15. The full section text was read.",
    ),
    dict(
        id="rtc_11911",
        publisher="California Legislative Information",
        title="Revenue and Taxation Code section 11911 — documentary transfer tax authority",
        url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=11911",
        supports=(
            "A county board of supervisors may impose 55 cents for each $500 of value "
            "(subdivision (a)); a city within a county that has imposed the tax may impose half "
            "that amount, 27.5 cents per $500, and a credit is allowed against the county tax "
            "(subdivisions (b) and (c))."
        ),
        opened="2026-11-15. Subdivisions (a), (b) and (c) were read.",
    ),
    dict(
        id="sfttc_rates",
        publisher="City Treasurer & Tax Collector (the city's own office)",
        title="Real property transfer tax — published rate schedule (city rate tier)",
        url="https://sftreasurer.org/",
        supports=(
            "Official publisher of city transfer-tax rates. NOT OPENED this session: the rate "
            "schedule page returned 'Page Not Found' at the address tried. The city rate used "
            "for jurisdiction B (0.75% at its price band, i.e. $3.75 per $500) is therefore "
            "taken as an assumption consistent with the statutory half-rate ceiling for a city add-on and flagged "
            "F05, not quoted from the city's schedule."
        ),
        opened="NOT OPENED — address returned 404; flagged.",
    ),
    dict(
        id="ca_const_xiii_a",
        publisher="California Legislative Information",
        title="Article XIII A, section 2 — Proposition 13 assessment limit",
        url="https://leginfo.legislature.ca.gov/faces/codes_displayArticle.xhtml?lawCode=CONS&article=XIII%20A",
        supports=(
            "The maximum ad valorem levy is 1% of full cash value and the assessed value may not "
            "be increased by more than 2% a year except on a change in ownership or new "
            "construction. Cited through the county compilation above, which quotes the same "
            "limit; the article itself was NOT opened this session and is flagged F06."
        ),
        opened="NOT OPENED — cited through the county compilation; flagged F06.",
    ),
    dict(
        id="ftb_540_booklet",
        publisher="California Franchise Tax Board",
        title="Form 540 personal income tax booklet — instructions",
        url="https://www.ftb.ca.gov/forms/2025/2025-540-booklet.html",
        supports=(
            "Instructions for the additional 1% tax above $1,000,000 of taxable income and for "
            "the rate schedules. NOT OPENED this session: the 2025 booklet address was not "
            "retrieved. The 1% tax is therefore computed from the statute (RTC 17043) that was "
            "read, and the capital-gain treatment is described from IRS Topic 409 plus the "
            "statutory 1% (California taxes capital gain as ordinary income under its own "
            "schedule, which is flagged as needing the FTB booklet to confirm the schedule)."
        ),
        opened="NOT OPENED — flagged F09.",
    ),
    dict(
        id="de_300",
        publisher="California Courts (Judicial Council)",
        title="Form DE-300 — small estate affidavit threshold",
        url="https://selfhelp.courts.ca.gov/probate",
        supports="Self-help entry point for probate and small-estate procedure. NOT OPENED this session; no figure on this desk rests on it.",
        opened="NOT OPENED — listed as a check-here link only.",
    ),
]

NOT_OPENED = [
    "irs_p551", "treasury_curve", "sfttc_rates", "ca_const_xiii_a", "ftb_540_booklet", "de_300",
]

HOSTS = sorted({__import__("urllib.parse", fromlist=["urlparse"]).urlparse(s["url"]).hostname for s in SOURCES})

BY_ID = {s["id"]: s for s in SOURCES}
