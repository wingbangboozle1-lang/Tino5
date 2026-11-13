"""Source register for decision-ad038. Every table row cites one or more IDs here.

status:
  FETCHED   - page opened and read in this session (13 Nov 2026)
  SEARCHED  - official page text seen in a search result; full page not opened (manual check suggested)
  SECONDARY - claim comes from a secondary report only; no verified official text. Flagged.
  NONE      - no official source obtained. Value is left blank and flagged.
"""

SOURCES = {
    "S01": dict(title="IRS - What's new: Estate and gift tax (2026 basic exclusion)", publisher="Internal Revenue Service",
                url="https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax", status="FETCHED"),
    "S02": dict(title="IRS - Rev. Proc. 2026-35, section 3.44: 2027 estate tax basic exclusion $15,480,000 (section 3.46: annual gift exclusion $20,000)", publisher="Internal Revenue Service",
                url="https://www.irs.gov/pub/irs-drop/rp-26-35.pdf", status="FETCHED"),
    "S03": dict(title="BOE LTA 2025/009 - Prop 19 transfer amount for 16 Feb 2025 to 15 Feb 2027 (published to the dollar; shown rounded to $10)", publisher="California State Board of Equalization",
                url="https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf", status="FETCHED"),
    "S04": dict(title="BOE LTA 2026/002 - 2026-27 CCPI inflation factor 1.02", publisher="California State Board of Equalization",
                url="https://www.boe.ca.gov/proptaxes/pdf/lta26002.pdf", status="FETCHED"),
    "S05": dict(title="BOE news release 2025 (Prop 19 adjustment)", publisher="California State Board of Equalization",
                url="https://www.boe.ca.gov/news/2025/nr-25-02.htm", status="SEARCHED"),
    "S06": dict(title="Rev. & Tax. Code 63.2 - Prop 19 parent-child exclusion conditions", publisher="California Legislative Information",
                url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2", status="FETCHED"),
    "S07": dict(title="Civil Code 1947.12 - statewide residential rent cap", publisher="California Legislative Information",
                url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12", status="FETCHED"),
    "S08": dict(title="FRED - California house price index (CASTHPI)", publisher="FHFA via Federal Reserve Bank of St. Louis",
                url="https://fred.stlouisfed.org/series/CASTHPI", status="FETCHED"),
    "S09": dict(title="FRED - All-Transactions HPI, Santa Clara County metro area (ATNHPIUS41940Q); metro mapping not confirmed",
                publisher="FHFA via Federal Reserve Bank of St. Louis", url="https://fred.stlouisfed.org/series/ATNHPIUS41940Q", status="FETCHED"),
    "S10": dict(title="FRED - All-Transactions HPI, metro series ATNHPIUS41884Q (metro mapping not confirmed)",
                publisher="FHFA via Federal Reserve Bank of St. Louis", url="https://fred.stlouisfed.org/series/ATNHPIUS41884Q", status="FETCHED"),
    "S11": dict(title="CBO - The Budget and Economic Outlook: 2026 to 2036", publisher="Congressional Budget Office",
                url="https://www.cbo.gov/publication/62105", status="SEARCHED"),
    "S12": dict(title="SF Treasurer & Tax Collector - secured property tax rate FY 2026-27", publisher="City and County of San Francisco",
                url="https://sftreasurer.org/property/secured-property-taxes", status="FETCHED"),
    "S13": dict(title="Regional water utility advice letter 628-A (June 2026) - proposed rate change; base charge $78.64/month", publisher="Regional water utility (CPUC advice filing)",
                url="https://www.sjwater.com/media/qeeh013c/adv-628a_web.pdf", status="SEARCHED"),
    "S14": dict(title="SFPUC - Water and sewer rate schedule FY 2026-27 (W-1B)", publisher="San Francisco Public Utilities Commission",
                url="https://www.sfpuc.gov/sites/default/files/accounts-and-services/Rates_Schedule_Water_Sewer_2026-7.pdf", status="SEARCHED"),
    "S15": dict(title="CPUC - net billing tariff for interconnection applications from 15 April 2023 (D.22-12-056)", publisher="California Public Utilities Commission",
                url="https://www.cpuc.ca.gov/industries-and-topics/electrical-energy/demand-side-management/net-energy-metering", status="FETCHED"),
    "S16": dict(title="HUD Fair Market Rents - dataset page (values not extracted)", publisher="HUD User",
                url="https://www.huduser.gov/portal/datasets/fmr.html", status="SECONDARY"),
    "S17": dict(title="IRS Topic 409 - Capital gains and losses (2025 tax-year rates)", publisher="Internal Revenue Service",
                url="https://www.irs.gov/taxtopics/tc409", status="FETCHED"),
    "S18": dict(title="IRS Topic 701 - Sale of your home ($250,000 / $500,000 exclusion)", publisher="Internal Revenue Service",
                url="https://www.irs.gov/taxtopics/tc701", status="FETCHED"),
    "S19": dict(title="IRC 26 U.S.C. 1014 - basis of property acquired from a decedent (step-up)", publisher="U.S. Code via Cornell LII",
                url="https://www.law.cornell.edu/uscode/text/26/1014", status="FETCHED"),
    "S20": dict(title="IRS Publication 551 - Basis of Assets (inherited property)", publisher="Internal Revenue Service",
                url="https://www.irs.gov/publications/p551", status="SEARCHED"),
    "S21": dict(title="Ballotpedia - Initiative 25-0017 (Prop 19 repeal): not on the ballot; failed to qualify", publisher="Ballotpedia",
                url="https://ballotpedia.org/California_Changes_to_Tax_Assessment_on_Inherited_Homes_Initiative_(2026)", status="FETCHED"),
    "S22": dict(title="California State Controller - California Estate Tax (no return for deaths on/after 1 Jan 2005)", publisher="California State Controller's Office",
                url="https://www.sco.ca.gov/ardtax_estate_tax.html", status="SEARCHED"),
    "S23": dict(title="CA Department of Insurance - 2025 residential premium data call summary (homeowners avg $2,340; dwelling fire $1,700; homeowners earthquake $1,440 per policy, rounded to $10)", publisher="California Department of Insurance",
                url="https://www.insurance.ca.gov/0400-news/0200-studies-reports/0300-earthquake-study/upload/EQEXP2025Summary.pdf", status="FETCHED"),
    "S24": dict(title="Santa Clara County Assessor / Tax Collector - tax rate tables (not reached)", publisher="County of Santa Clara",
                url="https://www.sccgov.org/", status="NONE"),
    "S25": dict(title="San Francisco Rent Board - rent ordinance coverage (text not reached)", publisher="City and County of San Francisco",
                url="https://www.sf.gov/", status="NONE"),
    "S26": dict(title="CA BOE - change in ownership FAQ (death with no probate: report within 150 days of death; with probate: with the inventory and appraisal) and Proposition 19 page", publisher="California State Board of Equalization",
                url="https://www.boe.ca.gov/proptaxes/faqs/changeinownership.htm", status="FETCHED"),
    "S27": dict(title="Japan NTA - Tax Answer No.4102, inheritance tax: basic deduction JPY 30,000,000 + JPY 6,000,000 per statutory heir; taxed 10%-55%; return and payment within 10 months; scope rules for residents and non-residents", publisher="National Tax Agency, Japan",
                url="https://www.nta.go.jp/taxes/shiraberu/taxanswer/sozoku/4102.htm", status="FETCHED"),
    "S28": dict(title="IRS - estate and gift tax treaties: United States-Japan estate and gift tax treaty in force", publisher="Internal Revenue Service",
                url="https://www.irs.gov/businesses/small-businesses-self-employed/estate-gift-tax-treaties-international", status="FETCHED"),
}


SOURCES["MODEL"] = dict(title="Model code in this repository (assumptions are set in model.py)", publisher="This project (not an official source)",
    url="https://github.com/wingbangboozle1-lang/Tino5/blob/main/decision-ad038/_src/model.py", status="MODEL")
SOURCES["OWNER"] = dict(title="Owner-supplied figure (not verified against an official source)", publisher="Owner",
    url=None, status="OWNER")


def link(sid: str) -> str:
    s = SOURCES[sid]
    if not s["url"]:
        return f'<span class="flag">{sid} (unverified)</span>'
    return f'<a href="{s["url"]}" target="_blank" rel="noopener">{sid}</a>'
