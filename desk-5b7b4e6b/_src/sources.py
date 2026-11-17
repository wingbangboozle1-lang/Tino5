# -*- coding: utf-8 -*-
"""Source register for desk-5b7b4e6b (session arena-5b7b4e6b, 2026-11-17).

Every row published on this desk cites one of these sources. A source is used for a value
only when its `status` says the page was opened and read in this session, or when the status
says exactly what was checked in an earlier session. A source marked "pointer" is published
as a "check here" link and is never used to support a value.

No secondary or commercial source appears in this register. A value that cannot be traced to
one of these official pages is left blank on the site and listed on flagged.html.
"""

SOURCES = {
    # ---------------------------------------------------------------- federal
    "irs_estate": {
        "publisher": "Internal Revenue Service",
        "title": "Estate tax — filing threshold by year of death (2026: $15,000,000); "
                 "portability of the unused exemption to a surviving spouse, 2011 onward",
        "url": "https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax",
        "status": "opened and read this session",
    },
    "irs_706": {
        "publisher": "Internal Revenue Service",
        "title": "Instructions for Form 706, United States Estate (and Generation-Skipping "
                 "Transfer) Tax Return",
        "url": "https://www.irs.gov/pub/irs-pdf/i706.pdf",
        "status": "recorded verified (prior session); not re-opened this session",
    },
    "irs_niit": {
        "publisher": "Internal Revenue Service",
        "title": "Net Investment Income Tax — 3.8% on net investment income above the "
                 "statutory threshold amounts",
        "url": "https://www.irs.gov/individuals/net-investment-income-tax",
        "status": "recorded verified (prior session); not re-opened this session",
    },
    "irs_p551": {
        "publisher": "Internal Revenue Service",
        "title": "Publication 551, Basis of Assets — fair market value at the date of death "
                 "as the basis of inherited property",
        "url": "https://www.irs.gov/publications/p551",
        "status": "recorded verified (prior session); not re-opened this session",
    },
    "irs_p523": {
        "publisher": "Internal Revenue Service",
        "title": "Publication 523, Selling Your Home — section 121 exclusion, ownership and "
                 "use tests, $250,000 / $500,000 limits",
        "url": "https://www.irs.gov/publications/p523",
        "status": "recorded verified (prior session); not re-opened this session",
    },
    "irs_p527": {
        "publisher": "Internal Revenue Service",
        "title": "Publication 527, Residential Rental Property — depreciation of rental "
                 "property and recapture on sale",
        "url": "https://www.irs.gov/publications/p527",
        "status": "recorded verified (prior session); not re-opened this session",
    },
    "irs_p544": {
        "publisher": "Internal Revenue Service",
        "title": "Topic 544 / Publication 544, Sales and Other Dispositions of Assets — "
                 "like-kind exchanges limited to real property held for use in a trade or "
                 "business or for investment",
        "url": "https://www.irs.gov/taxtopics/tc409",
        "status": "recorded verified (prior session); not re-opened this session",
    },
    "irs_p559": {
        "publisher": "Internal Revenue Service",
        "title": "Publication 559, Survivors, Executors, and Administrators",
        "url": "https://www.irs.gov/publications/p559",
        "status": "recorded verified (prior session); not re-opened this session",
    },
    "irs_inflation_2027": {
        "publisher": "Internal Revenue Service",
        "title": "Newsroom: tax inflation adjustments for tax year 2027",
        "url": "https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-"
               "year-2027-taxpayers-continue-to-benefit-from-the-working-families-tax-cuts",
        "status": "recorded verified (prior session); not re-opened this session",
    },
    # -------------------------------------------------------------- california
    "rtc_17043": {
        "publisher": "California Legislative Information",
        "title": "Revenue and Taxation Code section 17043 — additional 1% tax on taxable "
                 "income in excess of $1,000,000 (added by Proposition 63, 2004)",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?"
               "lawCode=RTC&sectionNum=17043",
        "status": "opened and read this session",
    },
    "rtc_17041": {
        "publisher": "California Legislative Information",
        "title": "Revenue and Taxation Code section 17041 — personal income tax rates and "
                 "the annual recomputation of the brackets",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?"
               "lawCode=RTC&sectionNum=17041",
        "status": "opened and read this session",
    },
    "ftb_rates_2026": {
        "publisher": "California Franchise Tax Board",
        "title": "2026 California Tax Rate Schedules (Form 540) — Schedules X, Y and Z; "
                 "top marginal rate 12.30%",
        "url": "https://www.ftb.ca.gov/forms/2026/2026-540-tax-rate-schedules.pdf",
        "status": "opened and read this session",
    },
    "ftb_capgains": {
        "publisher": "California Franchise Tax Board",
        "title": "Capital gains and losses — \"California does not have a lower rate for "
                 "capital gains. All capital gains are taxed as ordinary income.\"",
        "url": "https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html",
        "status": "opened and read this session (page last updated 28 Jan 2026)",
    },
    "ftb_540_2025": {
        "publisher": "California Franchise Tax Board",
        "title": "2025 Instructions for Form 540, California Resident Income Tax Return",
        "url": "https://www.ftb.ca.gov/forms/2025/2025-540-instructions.html",
        "status": "opened and read this session",
    },
    "ftb_5805_2025": {
        "publisher": "California Franchise Tax Board",
        "title": "2025 Instructions for Form FTB 5805 — \"the California Behavioral Health "
                 "Services Act imposes an additional 1% tax on taxable income over "
                 "$1,000,000\"",
        "url": "https://www.ftb.ca.gov/forms/2025/2025-5805-instructions.html",
        "status": "search-result extract from the official page; page not opened in full",
    },
    "boe_nr2502": {
        "publisher": "California State Board of Equalization",
        "title": "News Release NR 25-02 (7 March 2025) — Proposition 19 intergenerational "
                 "transfer exclusion amount, adjusted for transfers from 16 February 2025 "
                 "through 15 February 2027 (the figure itself is cited in the tables)",
        "url": "https://www.boe.ca.gov/news/2025/nr-25-02.htm",
        "status": "opened and read this session",
    },
    "boe_pub801": {
        "publisher": "California State Board of Equalization",
        "title": "Publication 801, Proposition 19 — form BOE-19-P, value limit and filing "
                 "period, Homeowners' Exemption within one year of transfer",
        "url": "https://www.boe.ca.gov/pdf/pub801.pdf",
        "status": "recorded verified (prior session); not re-opened this session",
    },
    "boe_prop13": {
        "publisher": "California State Board of Equalization",
        "title": "Proposition 13 — 1% maximum levy; assessed value increase capped at 2% a "
                 "year absent a change in ownership or new construction",
        "url": "https://www.boe.ca.gov/proptaxes/proposition13.htm",
        "status": "recorded verified (prior session); not re-opened this session",
    },
    "boe_lta26002": {
        "publisher": "California State Board of Equalization",
        "title": "Letter to Assessors 2026/002 — table of final Prop 13 inflation factors",
        "url": "https://www.boe.ca.gov/proptaxes/pdf/lta26002.pdf",
        "status": "data file transcribed in this repository with documented provenance; "
                  "not re-opened this session",
    },
    "cdi": {
        "publisher": "California Department of Insurance",
        "title": "Homeowners insurance consumer information (published under Insurance Code "
                 "section 12959); the Department states its figures are sample premiums, "
                 "not quotes",
        "url": "https://www.insurance.ca.gov/",
        "status": "pointer — not opened this session; no premium figure is asserted from it",
    },
    # ---------------------------------------------------- Santa Clara County (A)
    "scc_trb": {
        "publisher": "County of Santa Clara Controller-Treasurer",
        "title": "Property tax rate book (Compilation of Tax Rates) — the 1% maximum levy, "
                 "the countywide retirement levy, and the rate for each tax rate area",
        "url": "https://controller.santaclaracounty.gov/property-tax-distribution/"
               "property-tax-rate-book",
        "status": "pointer — the countywide figures are recorded verified by a prior "
                  "session; the parcel-specific rate is not published (see flag F01)",
    },
    "scc_asr_parentchild": {
        "publisher": "County of Santa Clara Assessor",
        "title": "Transferring your assessed value — parent to child (Proposition 19 claim)",
        "url": "https://asr.santaclaracounty.gov/tax-savings/transferring-your-assessed-"
               "value/parent-to-child-2",
        "status": "recorded verified (prior session); not re-opened this session",
    },
    "scc_recorder_fees": {
        "publisher": "County of Santa Clara Clerk-Recorder",
        "title": "Recording document fees",
        "url": "https://clerkrecorder.santaclaracounty.gov/recording-documents/"
               "recording-document-fees",
        "status": "recorded verified (prior session); not re-opened this session",
    },
    # ------------------------------------------------- San Francisco County (B)
    "sfdoe_2026": {
        "publisher": "San Francisco Department of Elections",
        "title": "November 3, 2026 Consolidated General Election results (preliminary) — "
                 "Measure H parcel tax to fund Muni operations, Measure I transfer tax, "
                 "Measure J foreclosure transfer tax, Measure RTM",
        "url": "https://www.sfelections.org/results/20261103/index.html",
        "status": "opened and read this session (results marked preliminary, last updated "
                  "10 Nov 2026; certification due within 30 days of the election)",
    },
    "sf_vip_2026": {
        "publisher": "City and County of San Francisco",
        "title": "November 3, 2026 Voter Information Pamphlet — official terms of Measure H "
                 "(parcel tax rates, 15-year term 1 Jul 2027 to 30 Jun 2042)",
        "url": "https://media.api.sf.gov/documents/N26_EN_VIP.pdf",
        "status": "opened and read this session",
    },
    "sf_transfer_tax": {
        "publisher": "City and County of San Francisco",
        "title": "Real property transfer tax rates",
        "url": "https://www.sf.gov/transfer-tax",
        "status": "recorded verified (prior session); not re-opened this session",
    },
    # ------------------------------------------------------------ economy data
    "bls_fred": {
        "publisher": "U.S. Bureau of Labor Statistics (series served by the Federal Reserve "
                     "Bank of St. Louis, FRED)",
        "title": "CPIAUCNS (U.S. city average, all items), CUURA422SA0 (San Francisco area, "
                 "all items), CUURA422SEHA (San Francisco area, rent of primary residence), "
                 "TB3MS (3-month Treasury bill), GS10 (10-year Treasury) — annual averages",
        "url": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCNS,CUURA422SA0,"
               "CUURA422SEHA,GS10,TB3MS&fq=Annual,Annual,Annual,Annual,Annual&fam=avg,avg,"
               "avg,avg,avg",
        "status": "opened and read this session; every 1975-2025 row compared with the "
                  "transcription stored in this repository — all match",
    },
    "fhfa_fred": {
        "publisher": "Federal Housing Finance Agency (series served by FRED)",
        "title": "All-transactions House Price Index — ATNHPIUS41940Q (Property A's "
                 "metropolitan area), ATNHPIUS41884Q (Property B's metropolitan division), "
                 "CASTHPI (California), fourth-quarter value of each year",
        "url": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=ATNHPIUS41940Q,"
               "ATNHPIUS41884Q,CASTHPI&fq=Annual,Annual,Annual&fam=eop,eop,eop",
        "status": "opened and read this session; every row compared with the transcription "
                  "stored in this repository — all match",
    },
    "erp2026_b55": {
        "publisher": "Economic Report of the President 2026 (U.S. Government Publishing "
                     "Office)",
        "title": "Table B-55, Common stock prices and yields, 1975-1999 — Standard & Poor's "
                 "composite index at end of year and dividend-price ratio",
        "url": "https://www.govinfo.gov/content/pkg/ERP-2026/pdf/ERP-2026-table55.pdf",
        "status": "recorded verified (prior session); the 2000-2025 half of the same "
                  "transcription was re-verified this session against Table B-56",
    },
    "erp2026_b56": {
        "publisher": "Economic Report of the President 2026 (U.S. Government Publishing "
                     "Office)",
        "title": "Table B-56, Common stock prices and yields, 2000-2025 — Standard & Poor's "
                 "composite index at end of year and dividend-price ratio",
        "url": "https://www.govinfo.gov/content/pkg/ERP-2026/pdf/ERP-2026-table56.pdf",
        "status": "opened and read this session; every 2000-2025 S&P value and "
                  "dividend-price ratio compared with the transcription stored in this "
                  "repository — all match",
    },
    "fedhist_1929": {
        "publisher": "Federal Reserve History",
        "title": "Stock Market Crash of 1929 — Dow Jones Industrial Average 381 in September "
                 "1929, closing low of 41.22 in the summer of 1932 (89% below the peak), "
                 "pre-crash level not regained until November 1954",
        "url": "https://www.federalreservehistory.org/essays/stock-market-crash-of-1929",
        "status": "official page text confirmed this session through the site's own search "
                  "result; the essay page itself was not opened",
    },
    "treasury_yields": {
        "publisher": "U.S. Department of the Treasury",
        "title": "Daily Treasury par yield curve rates",
        "url": "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
               "TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026",
        "status": "recorded verified (prior session); not re-opened this session",
    },
    "census_acs": {
        "publisher": "U.S. Census Bureau",
        "title": "QuickFacts — median gross rent and owner-occupied housing value "
                 "(county level)",
        "url": "https://www.census.gov/quickfacts/fact/table/santaclaracountycalifornia/"
               "RHI825222",
        "status": "recorded verified (prior session); not re-opened this session",
    },
    "hud_fmr": {
        "publisher": "U.S. Department of Housing and Urban Development",
        "title": "Fair Market Rents (used only as a floor check; never as the market rent)",
        "url": "https://www.huduser.gov/portal/datasets/fmr.html",
        "status": "recorded verified (prior session); not re-opened this session",
    },
}

# Hosts this desk is allowed to link to. Every one of them is a government or
# government-established publisher.
ALLOWED_HOSTS = {
    "www.irs.gov", "www.ftb.ca.gov", "www.boe.ca.gov",
    "leginfo.legislature.ca.gov", "www.courts.ca.gov", "courts.ca.gov",
    "www.insurance.ca.gov", "www.census.gov", "census.gov",
    "www.huduser.gov", "www.bls.gov", "data.bls.gov",
    "fred.stlouisfed.org", "www.govinfo.gov", "govinfo.gov",
    "www.federalreservehistory.org", "home.treasury.gov",
    "www.fhfa.gov", "www.federalreserve.gov",
    "www.sfelections.org", "sfelections.org", "www.sf.gov", "sf.gov",
    "media.api.sf.gov", "sfassessor.org", "sftreasurer.org", "sfmta.com",
    "asr.santaclaracounty.gov", "controller.santaclaracounty.gov",
    "clerkrecorder.santaclaracounty.gov", "files.santaclaracounty.gov",
    "www.sccgov.org", "www.sco.ca.gov", "selfhelp.courts.ca.gov",
    "www.nber.org", "nber.org", "www.sfpuc.org", "sfpuc.gov",
}
