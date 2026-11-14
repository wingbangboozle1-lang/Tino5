# -*- coding: utf-8 -*-
"""
Source register for the phase-99220 desk (session arena-99220bc7).

Rule: a source is listed here only if this session opened it (or, where marked, read the
excerpt the search tool returned). Anything cited but not opened is listed as NOT OPENED and
the row that depends on it is flagged.
"""

OFFICIAL_HOSTS = {
    "home.treasury.gov", "fred.stlouisfed.org", "www.federalreservehistory.org",
    "www.irs.gov", "www.boe.ca.gov", "boe.ca.gov", "www.bls.gov",
}

SOURCES = [
    dict(id="S1", publisher="U.S. Department of the Treasury",
         title="Daily Treasury Par Yield Curve Rates (13 Nov 2026 row: 3 Mo 4.32, 2 Yr 4.88)",
         url="https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202611",
         status="Opened 2026-11-14.",
         supports="3-month and 2-year Treasury yields on 13 Nov 2026, used as the cash rate for parking proceeds."),
    dict(id="S2", publisher="Board of Governors of the Federal Reserve System, via FRED",
         title="DGS2 - 2-Year Treasury constant maturity (12 Nov 2026: 4.86)",
         url="https://fred.stlouisfed.org/series/DGS2",
         status="Opened 2026-11-14.",
         supports="Cross-check of the 2-year yield (one day earlier than S1, 4.86 against 4.88 on 13 Nov)."),
    dict(id="S3", publisher="Federal Reserve Bank of St. Louis / Federal Reserve History",
         title="The Stock Market Crash of 1929",
         url="https://www.federalreservehistory.org/essays/stock-market-crash-of-1929",
         status="Opened 2026-11-14.",
         supports="Dow Jones Industrial Average peak 381.17 on 3 Sep 1929; closing low 41.22 on 8 Jul 1932, 89% below peak; prior high regained 23 Nov 1954."),
    dict(id="S4", publisher="Federal Reserve History",
         title="The Great Recession (S&P 500 fell 57% from October 2007 peak to March 2009 trough)",
         url="https://www.federalreservehistory.org/essays/great-recession-of-200709",
         status="Opened 2026-11-14.",
         supports="S&P 500 drawdown of 57%, Oct 2007 peak to Mar 2009 trough. The essay does not state a recovery date."),
    dict(id="S5", publisher="Internal Revenue Service",
         title="Estate tax (filing threshold table)",
         url="https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax",
         status="Opened 2026-11-14.",
         supports="Filing threshold for deaths in 2026: $15,000,000."),
    dict(id="S6", publisher="Internal Revenue Service",
         title="About Form 706, United States Estate (and Generation-Skipping Transfer) Tax Return",
         url="https://www.irs.gov/forms-pubs/about-form-706",
         status="Opened 2026-11-14.",
         supports="Form 706 is used by the executor to figure the estate tax. Current instructions dated 07/2026."),
    dict(id="S7", publisher="State Board of Equalization, Taxpayers' Rights Advocate Office",
         title="Information Sheet Pub 800-9: Death of a Real Property Owner (LTA 2024/052)",
         url="https://www.boe.ca.gov/proptaxes/pdf/lta24052.pdf",
         status="Opened 2026-11-14, chunks 0-2 of 4 read.",
         supports="BOE-502-D within 150 days after death (R&TC 480(b)); date of death is the change in ownership for trust-held property; principal residence must be in place within one year; claim form BOE-19-P; BOE-100-B within 90 days; property tax delinquency dates 10 Dec and 10 Apr."),
    dict(id="S8", publisher="State Board of Equalization, Legal Entity Ownership Program",
         title="LEOP Filing Requirements and Penalty Provisions",
         url="https://www.boe.ca.gov/proptaxes/leoppenalty.htm",
         status="Read as the search tool's excerpt on 2026-11-14; page not opened in full.",
         supports="BOE-100-B within 90 days of a change in control or ownership of a legal entity; 10% penalty under R&TC 482(b)."),
    dict(id="S9", publisher="Internal Revenue Service",
         title="Instructions for Form 706 (07/2026)",
         url="https://www.irs.gov/instructions/i706",
         status="NOT OPENED for the due-date passage: the page loaded but the 'When To File' text was not reached in the fetch window.",
         supports="Intended to confirm: Form 706 due 9 months after the date of death; automatic 6-month extension on Form 4768. Flagged F04 until read."),
]

NOT_OPENED = [
    ("IRS Form 706 instructions, due-date passage", "S9"),
    ("IRS Form 4768 (extension)", None),
    ("BOE-19-P claim filing deadline", None),
    ("Santa Clara County water and power rates", None),
    ("Homeowners insurance premium data (CDI)", None),
]
