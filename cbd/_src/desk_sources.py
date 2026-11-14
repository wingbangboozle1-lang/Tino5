# -*- coding: utf-8 -*-
"""
Source register for the cbd/ desk (session arena-cbd1473c).

Rule: a source is listed here only if its text was read during this session, or it is
explicitly marked REUSED (taken from the cbe/ register, opened by that session, and NOT
re-opened here). A REUSED source is flagged on flagged.html until it is re-opened.
Every table row on every page cites at least one id from this register or states
explicitly that no official source applies.
"""

OFFICIAL_HOSTS = {
    "home.treasury.gov",
    "www.federalreservehistory.org",
    "www.irs.gov",
    "www.boe.ca.gov",
    "leginfo.legislature.ca.gov",
    "www.ftb.ca.gov",
}

SOURCES = {
    "tsy_curve": dict(
        publisher="U.S. Department of the Treasury",
        title="Daily Treasury Par Yield Curve Rates, November 2026",
        url=("https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
             "TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202611"),
        status="opened",
        read="Retrieved 2026-11-14. Row for 11/13/2026: 3 Mo 4.32 percent; 2 Yr 4.88 percent.",
    ),
    "fed_1929": dict(
        publisher="Federal Reserve History (Federal Reserve System)",
        title="Stock Market Crash of 1929",
        url="https://www.federalreservehistory.org/essays/stock-market-crash-of-1929",
        status="opened",
        read=("Retrieved 2026-11-14. Index peaked 3 Sep 1929 at 381.17; closed 8 Jul 1932 at 41.22, "
              "89 percent below its peak. Did not regain the 1929 high until 23 Nov 1954. "
              "This is the Dow Jones Industrial Average, a price index without dividends."),
    ),
    "fed_2008": dict(
        publisher="Federal Reserve History (Federal Reserve System)",
        title="The Great Recession (December 2007 to June 2009)",
        url="https://www.federalreservehistory.org/essays/great-recession-of-200709",
        status="opened",
        read=("Retrieved 2026-11-14. The S&P 500 index fell 57 percent from its October 2007 peak "
              "to its trough in March 2009. A price index, not total return."),
    ),
    "irs_701": dict(
        publisher="Internal Revenue Service",
        title="Topic no. 701, Sale of your home",
        url="https://www.irs.gov/taxtopics/tc701",
        status="opened",
        read=("Retrieved 2026-11-14. Exclusion of up to $250,000 of gain, or $500,000 on a joint "
              "return. Ownership and use tests: 24 months of the last 5 years each."),
    ),
    "irs_409": dict(
        publisher="Internal Revenue Service",
        title="Topic no. 409, Capital gains and losses",
        url="https://www.irs.gov/taxtopics/tc409",
        status="opened",
        read=("Retrieved 2026-11-14. Net capital gains: 20 percent top rate for taxable income above "
              "the 15 percent thresholds. Unrecaptured section 1250 gain: maximum 25 percent. "
              "Thresholds quoted are for 2025."),
    ),
    "irs_niit": dict(
        publisher="Internal Revenue Service",
        title="Net Investment Income Tax",
        url="https://www.irs.gov/individuals/net-investment-income-tax",
        status="opened",
        read=("Retrieved 2026-11-14. 3.8 percent tax on net investment income above $200,000 "
              "single. Includes interest, dividends and capital gains. Gain excluded under the "
              "home-sale rules is not net investment income."),
    ),
    "irs_faq_estate": dict(
        publisher="Internal Revenue Service",
        title="Frequently asked questions on estate taxes",
        url=("https://www.irs.gov/businesses/small-businesses-self-employed/"
             "frequently-asked-questions-on-estate-taxes"),
        status="opened",
        read=("Retrieved 2026-11-14. Form 706 due nine months after the date of death; automatic "
              "six-month extension on Form 4768 filed by the due date. Filing threshold for a 2026 "
              "death: $15,000,000. Portability election requires a timely return."),
    ),
    "boe_lta26026": dict(
        publisher="California State Board of Equalization",
        title="Letter to Assessors 2026/026: Proposition 19 Intergenerational Transfer Exclusion, FAQ",
        url="https://www.boe.ca.gov/proptaxes/pdf/lta26026.pdf",
        status="opened",
        read=("Retrieved 2026-11-14, dated 3 August 2026. Family home and principal residence "
              "definitions; excluded amount is the factored base year value plus $1,000,000 "
              "(the value cap), adjusted every second February 16 from 2023; new base year value "
              "is enrolled if the exclusion is removed."),
    ),
    "rtc_63_2": dict(
        publisher="California Legislative Information",
        title="Revenue and Taxation Code section 63.2",
        url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2",
        status="opened",
        read=("Retrieved 2026-11-14. (a)(1)(A): transferee must make the home a principal residence "
              "within one year. (a)(1)(B): file for the homeowners' or disabled veterans' exemption "
              "within a year. (f)(1)(A): claim within three years, or before a transfer to a third "
              "party, or when an eligible transferee stops occupying, whichever is earlier. "
              "(f)(1)(B): claim timely if filed within six months after a supplemental or escape "
              "assessment notice. (c): claim is not a public document. (e)(9): transfer through an "
              "inter vivos or testamentary trust counts as a transfer."),
    ),
    "rtc_17043": dict(
        publisher="California Legislative Information",
        title="Revenue and Taxation Code section 17043",
        url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=17043",
        status="opened",
        read="Retrieved 2026-11-14. Additional 1 percent tax on taxable income above $1,000,000.",
    ),
    # ----- reused from the cbe/ register: opened by that session, NOT re-opened here
    "irs_ir2026_133": dict(
        publisher="Internal Revenue Service",
        title="News release IR-2026-133, tax year 2027 inflation adjustments",
        url=("https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2027-"
             "taxpayers-continue-to-benefit-from-the-working-families-tax-cuts"),
        status="reused",
        read=("REUSED from cbe/_src/sources.py (opened by session arena-cbe837cb). Top income rate 37 "
              "percent. Not re-opened in this session; listed on flagged.html."),
    ),
    "ftb_rates": dict(
        publisher="Franchise Tax Board (California)",
        title="2025 California tax rate schedules",
        url="https://www.ftb.ca.gov/forms/2025/2025-540-tax-rate-schedules.pdf",
        status="reused",
        read=("REUSED from cbe/_src/sources.py (opened by session arena-cbe837cb). Top rate 12.3 "
              "percent. Not re-opened in this session; listed on flagged.html."),
    ),
    "cbe_model": dict(
        publisher="Owner-brief desk (this repository)",
        title="cbe/ owner-brief model and options page (read-only import)",
        url="../cbe/options.html",
        status="internal",
        read=("Internal. Property values, rents, running costs and break-evens come from "
              "cbe/_src/model.py, which lists its own sources on cbe/sources.html."),
    ),
    "cbe_phased": dict(
        publisher="Owner-brief desk (this repository)",
        title="Phased investing stress test (cbe/phased-investing.html)",
        url="../cbe/phased-investing.html",
        status="internal",
        read=("Internal. Built by session arena-ad490053 and merged on main. This desk links to it "
              "and does not rebuild it."),
    ),
}


def link(sid, label=None):
    s = SOURCES[sid]
    text = label or s["title"]
    return '<a href="%s" rel="noopener noreferrer">%s</a>' % (s["url"], text)


def tag(sid):
    s = SOURCES[sid]
    flag = {"opened": "opened", "reused": "reused, not re-opened", "internal": "internal"}[s["status"]]
    return '%s <span class="tag">%s</span>' % (link(sid, s["publisher"]), flag)
