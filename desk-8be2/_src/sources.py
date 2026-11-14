# -*- coding: utf-8 -*-
"""
Official source register for the independent decision desk `desk-8be2/`
(session arena-8be27405).

Rule for this desk: every external link in the published output must point at a host on
OFFICIAL_HOSTS below. Every source id is either (a) an official document that was read
and used for a value, or (b) an official "check here" landing page that this session
could not fetch (network-limited sandbox) and is therefore labelled so; any figure that
leans on such a link is shown blank and marked unverified, or is clearly labelled an
assumption.

Statutory amounts are quoted verbatim and marked; they are exempt from the $10 rounding
rule because rounding a legal threshold would misstate it.
"""

OFFICIAL_HOSTS = {
    "www.irs.gov",
    "irs.gov",
    "www.ftb.ca.gov",
    "ftb.ca.gov",
    "www.boe.ca.gov",
    "boe.ca.gov",
    "leginfo.legislature.ca.gov",
    "www.courts.ca.gov",
    "courts.ca.gov",
    "www.bls.gov",
    "data.bls.gov",
    "www.fhfa.gov",
    "www.treasury.gov",
    "home.treasury.gov",
    "fiscal.treasury.gov",
    "www.federalreserve.gov",
    "www.govinfo.gov",
    "www.ssa.gov",
    "www.cbo.gov",
    "www.insurance.ca.gov",
    "www.congress.gov",
    "crsreports.congress.gov",
    "www.sos.ca.gov",
    "voterguide.sos.ca.gov",
    "electionresults.sos.ca.gov",
}

# Statutory / published official amounts quoted verbatim. Exempt from $10 rounding.
STATUTORY_LITERALS = {
    "15,000,000",   # IRS basic exclusion amount, deaths in 2026 (irs.gov estate tax)
    "15,480,000",   # IRS basic exclusion amount, deaths in 2027 (IRS IR-2026-133)
    "13,990,000",   # IRS basic exclusion amount, deaths in 2025
    "19,000",       # IRS annual gift exclusion, 2026
    "20,000",       # IRS annual gift exclusion, 2027
    "1,044,586",    # BOE Prop 19 inflation-adjusted cap, 16 Feb 2025 - 15 Feb 2027
    "1,022,600",    # BOE Prop 19 cap, 16 Feb 2023 - 15 Feb 2025
    "69,625",       # Judicial Council DE-300 probate threshold reference
    "107,900",
    "208,850",
    "661,375",
    "75,197",
}

SOURCES = [
    # ------------------------------------------------------------------ federal: estate
    dict(
        id="irs_estate_tax",
        publisher="Internal Revenue Service",
        title="Estate Tax (filing threshold for year of death)",
        url="https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax",
        evidences=(
            "Filing threshold / basic exclusion amount by year of death: 2025 $13,990,000; "
            "2026 $15,000,000. Portability: a surviving spouse may elect to pass the unused "
            "exclusion to the surviving spouse on a timely filed Form 706."
        ),
        checked="Verified and read in session arena-cbe837cb (2026-11-14); re-cited here.",
    ),
    dict(
        id="irs_ir2026_133",
        publisher="Internal Revenue Service",
        title="IR-2026-133, 5 November 2026 — tax year 2027 inflation adjustments",
        url=(
            "https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-"
            "year-2027-taxpayers-continue-to-benefit-from-the-working-families-tax-cuts"
        ),
        evidences=(
            "Estates of decedents who die during 2027: basic exclusion $15,480,000 (up from "
            "$15,000,000 for 2026). Annual gift exclusion $20,000 for 2027 (up from $19,000 "
            "for 2026)."
        ),
        checked="Verified and read in session arena-cbe837cb (2026-11-14); re-cited here.",
    ),
    dict(
        id="irs_stepup_basis",
        publisher="Internal Revenue Service",
        title="Publication 559, Survivors, Executors, and Administrators — basis of inherited property",
        url="https://www.irs.gov/publications/p559",
        evidences=(
            "The basis of inherited property is generally its fair market value at the date of "
            "death (step-up in basis), or the alternate valuation date if elected."
        ),
        checked="Official link; text not re-fetched in this session (sandbox network limit). "
                "Treat the rule citation as verified in session arena-cbe837cb; re-read before relying.",
    ),
    dict(
        id="irs_form706",
        publisher="Internal Revenue Service",
        title="Form 706, United States Estate (and Generation-Skipping Transfer) Tax Return",
        url="https://www.irs.gov/forms-pubs/about-form-706",
        evidences=(
            "Generally due nine months after the date of death; a six-month extension is "
            "available. Portability election (DSUE) is made on a timely filed return."
        ),
        checked="Official link; not re-fetched in this session. Citation only.",
    ),
    # ------------------------------------------------------- california: estate / inheritance
    dict(
        id="ftb_inheritance",
        publisher="California Franchise Tax Board",
        title="Inheritance and estate tax — California does not impose a state estate or inheritance tax",
        url="https://www.ftb.ca.gov/",
        evidences=(
            "California has no state estate tax and no inheritance tax. Inherited assets are not "
            "taxable income to the recipient at the state level; later rent or sale gains are "
            "taxed."
        ),
        checked="Official home page cited; exact landing path not re-fetched in this session. "
                "Rule confirmed via FTB-cited material in session arena-cbe837cb.",
    ),
    # ------------------------------------------------------- california: property tax / Prop 19
    dict(
        id="boe_prop19",
        publisher="California State Board of Equalization",
        title="Proposition 19 — parent-child and grandparent-grandchild reassessment exclusions",
        url="https://www.boe.ca.gov/proptaxes/prop19/",
        evidences=(
            "Under Revenue and Taxation Code section 63.2, the parent-child exclusion applies only "
            "to a primary residence, the child must occupy it as their primary residence within one "
            "year of transfer, and the market-value-over-assessment spread is protected up to an "
            "inflation-adjusted cap ($1,044,586 for 16 Feb 2025 - 15 Feb 2027)."
        ),
        checked="Verified and read in session arena-cbe837cb (2026-11-14); re-cited here.",
    ),
    dict(
        id="boe_rtc632",
        publisher="California Legislature",
        title="Revenue and Taxation Code section 63.2 (Proposition 19)",
        url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2.",
        evidences=(
            "Statutory text: transfers via inter vivos or testamentary trust qualify; an interest "
            "in a legal entity does not; a claim under the section is not a public document."
        ),
        checked="Verified and read in session arena-cbe837cb (2026-11-14); re-cited here.",
    ),
    dict(
        id="boe_prop13",
        publisher="California State Board of Equalization",
        title="Proposition 13 — base year value and 2% annual assessment cap",
        url="https://www.boe.ca.gov/proptaxes/proposition13.htm",
        evidences=(
            "Base year value set at purchase or new construction; annual assessment increase "
            "capped at 2% absent a change in ownership or new construction."
        ),
        checked="Official link; not re-fetched in this session. Rule citation only.",
    ),
    # ------------------------------------------------------- california: probate / trust
    dict(
        id="courts_de300",
        publisher="Judicial Council of California",
        title="DE-300 probate thresholds and estate administration",
        url="https://www.courts.ca.gov/selfhelp-probate.htm",
        evidences=(
            "Probate thresholds and small-estate procedures; trust administration generally avoids "
            "probate when title is held in trust."
        ),
        checked="Official link; not re-fetched in this session. Citation only.",
    ),
    # ------------------------------------------------------- federal: markets / treasury / data
    dict(
        id="treasury_rates",
        publisher="U.S. Department of the Treasury",
        title="Daily Treasury Par Yield Curve Rates (3-month, 2-year, etc.)",
        url="https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date=2026",
        evidences=(
            "Official Treasury yield curve. Current 3-month and 2-year yields used as the "
            "parking-rate reference for the phased-investing path (see what-if page)."
        ),
        checked="Official link; current rates not re-fetched this session. Figure shown only as "
                "an illustrative reference marked unverified.",
    ),
    dict(
        id="bls_cpi",
        publisher="U.S. Bureau of Labor Statistics",
        title="Consumer Price Index (CPI-U)",
        url="https://www.bls.gov/cpi/",
        evidences=("Official CPI-U series used for inflation indexing in projections."),
        checked="Official link; series not re-fetched this session. Citation only.",
    ),
    dict(
        id="fhfa_hpi",
        publisher="Federal Housing Finance Agency",
        title="House Price Index (HPI)",
        url="https://www.fhfa.gov/DataTools/Downloads/Pages/House-Price-Index-Datasets.aspx",
        evidences=("Official house-price index used for home-value projection ranges."),
        checked="Official link; not re-fetched this session. Citation only.",
    ),
    dict(
        id="federal_reserve_erp",
        publisher="Board of Governors of the Federal Reserve System",
        title="Economic Report of the President — long-run stock, bond and bill returns (tables B-55/B-56)",
        url="https://www.govinfo.gov/content/pkg/ERP-2026/pdf/ERP-2026.pdf",
        evidences=(
            "Historical long-run annual returns for stocks (with dividends), bonds and Treasury "
            "bills used as the reference record for crash-entry stress tests."
        ),
        checked="Official link; not re-fetched this session. Citation only.",
    ),
    dict(
        id="ssa_trustees",
        publisher="Social Security Administration",
        title="OASDI Trustees Report — long-run economic assumptions",
        url="https://www.ssa.gov/oact/tr/2026/",
        evidences=("Long-run inflation and interest-rate assumptions used as the baseline projection."),
        checked="Official link; not re-fetched this session. Citation only.",
    ),
    dict(
        id="cbo_outlook",
        publisher="Congressional Budget Office",
        title="CBO Budget and Economic Outlook",
        url="https://www.cbo.gov/",
        evidences=("Official macroeconomic assumptions used as a cross-check on baseline projections."),
        checked="Official link; not re-fetched this session. Citation only.",
    ),
    # ------------------------------------------------------- california: insurance
    dict(
        id="cdi_insurance",
        publisher="California Department of Insurance",
        title="Homeowners insurance and rate information",
        url="https://www.insurance.ca.gov/",
        evidences=(
            "California Department of Insurance is the official source for homeowners insurance "
            "market and rate information; specific premiums vary by property and are not published "
            "per parcel, so quotes are shown as ranges marked as assumptions."
        ),
        checked="Official home page cited; specific premium not re-fetched this session.",
    ),
    # ------------------------------------------------------- california: legislature / ballot
    dict(
        id="leginfo",
        publisher="California Legislature",
        title="California Legislative Information — bills and codes",
        url="https://leginfo.legislature.ca.gov/",
        evidences=("Official bill text for pending property-tax and inheritance legislation."),
        checked="Official link; not re-fetched this session. Citation only.",
    ),
]

SOURCE_BY_ID = {s["id"]: s for s in SOURCES}

def cite(id):
    """Return an HTML anchor for a source id."""
    s = SOURCE_BY_ID[id]
    return f'<a href="{s["url"]}">{s["publisher"]} — {s["title"]}</a>'
