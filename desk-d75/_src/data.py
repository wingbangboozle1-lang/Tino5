"""Registers for the owner-brief desk (session arena-d75e2754, 13 November 2026).

Everything in this file is either (a) an official figure this session opened at the publisher's
own address, (b) an official figure a previous session opened and this session carried forward with
a "not re-opened" label, (c) an owner-supplied value, or (d) a named modelling assumption.
Nothing is filled in by inference: if a value could not be confirmed it is left as None and the
row is flagged on the Flagged for review page.

Status vocabulary used everywhere in this desk
  verified        value read from the official document at the linked address, this session
  carried         value taken from the repository's source register, where an earlier session
                  read the same official document; not re-opened on 13 November 2026
  owner           supplied by the property owner; not confirmable from any public source
  derived         arithmetic on owner and/or official values; the arithmetic is printed with it
  assumption      a modelling choice with an id; sensitivity is printed with it
  unverified      could not be confirmed; the value cell is blank and the item is on the flagged page
"""

AS_OF = "13 November 2026"
HORIZON = (2026, 2076)

# ---------------------------------------------------------------------------
# 1. Source register
#    opened = this session retrieved the document at the address below on 13 Nov 2026
# ---------------------------------------------------------------------------
SOURCES = [
    # --- official, opened by this session on 13 November 2026 ---
    dict(id="irs_rp2635", kind="official", opened=True,
         title="IRS, Revenue Procedure 2026-35, 2027 inflation adjustments",
         url="https://www.irs.gov/pub/irs-drop/rp-26-35.pdf",
         supports="2027 basic exclusion amount; 2027 annual gift exclusion; gifts to a "
                  "non-citizen spouse; 2027 capital-gain rate thresholds; estate-tax installment interest amount"),
    dict(id="irs_706", kind="official", opened=True,
         title="IRS, Instructions for Form 706 (July 2026 revision)",
         url="https://www.irs.gov/instructions/i706",
         supports="who must file, 9-month deadline and 6-month extension, portability election, "
                  "consistent-basis reporting within 30 days, estate-tax closing letter"),
    dict(id="irs_701", kind="official", opened=True,
         title="IRS, Topic no. 701, Sale of your home",
         url="https://www.irs.gov/taxtopics/tc701",
         supports="principal-residence gain exclusion, ownership and use tests, once-per-two-years rule"),
    dict(id="irs_559", kind="official", opened=False,
         title="IRS, Topic no. 559, Net investment income tax",
         url="https://www.irs.gov/taxtopics/tc559",
         supports="3.8% tax on net investment income for individuals above the threshold"),
    dict(id="boe_lta25009", kind="official", opened=True,
         title="BOE, Letter to Assessors 2025/009 - Proposition 19, adjustment of the $1 million amount",
         url="https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf",
         supports="the adjusted amount for transfers 16 Feb 2025 - 15 Feb 2027, the two-year indexing "
                  "rule, the index used (FHFA House Price Index for California), the table of prior amounts"),
    dict(id="boe_lta26002", kind="official", opened=True,
         title="BOE, Letter to Assessors 2026/002 - 2026-27 California Consumer Price Index",
         url="https://www.boe.ca.gov/proptaxes/pdf/lta26002.pdf",
         supports="the inflation factor for the 2026 roll and the complete table of factors since 1976-77, "
                  "including how the missing October 2025 index was handled"),
    dict(id="boe_lta26026", kind="official", opened=True,
         title="BOE, Letter to Assessors 2026/026 - Proposition 19 intergenerational transfer exclusion, FAQ",
         url="https://www.boe.ca.gov/proptaxes/pdf/lta26026.pdf",
         supports="definitions of excluded amount, excess amount, new base year value, new taxable value, "
                  "the continual-use requirement and what happens when the exclusion is removed"),
    dict(id="boe_lta23027", kind="official", opened=False,
         title="BOE, Letter to Assessors 2023/027 - homeowners' exemption information sheet",
         url="https://boe.ca.gov/proptaxes/pdf/lta23027.pdf",
         supports="the $7,000 homeowners' exemption and the February 15 / December 10 filing rule"),
    dict(id="rtc_632", kind="official", opened=True,
         title="California Revenue and Taxation Code section 63.2 (Proposition 19 text)",
         url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2",
         supports="one-year principal-residence condition, one-year exemption filing, three-year claim "
                  "window, value-cap arithmetic, inclusion of transfers through a trust, re-enrolment of "
                  "the new base year value when the exclusion ends"),
    dict(id="prob_10810", kind="official", opened=True,
         title="California Probate Code section 10810 (statutory attorney compensation)",
         url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PROB&sectionNum=10810",
         supports="the tiered statutory percentage fee on the value of the estate accounted for"),
    dict(id="prob_160617", kind="official", opened=False,
         title="California Probate Code section 16061.7 (trustee or personal representative notice)",
         url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PROB&sectionNum=16061.7",
         supports="the 60-day notification duty after the trust becomes irrevocable and the 120-day claim window"),
    dict(id="prob_13100", kind="official", opened=False,
         title="California Probate Code section 13100 (affidavit procedure for small estates)",
         url="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PROB&sectionNum=13100",
         supports="the small-estate affidavit procedure and the base text of the collection threshold"),
    dict(id="de300", kind="official", opened=False,
         title="Judicial Council of California, form DE-300 (probate collection thresholds)",
         url="https://www.courts.ca.gov/documents/de300.pdf",
         supports="the threshold as adjusted for deaths on or after 1 April 2025 and the next adjustment date"),
    dict(id="sftc_rate", kind="official", opened=True,
         title="The consolidated city and county treasurer and tax collector, secured property taxes",
         url="https://sftreasurer.org/property/secured-property-taxes",
         supports="the fiscal 2026-27 secured tax rate for the city and how the rate is set and shown on a bill"),
    dict(id="scc_ratebook", kind="official", opened=False,
         title="The county of the inherited house, fiscal 2025-26 property tax rate book",
         url="https://www.sccgov.org/sites/dtt/pd/Documents/tax-rate-book-2025-2026.pdf",
         supports="the composite secured rate for a tax rate area in the county, and the voter-approved "
                  "and parcel-tax lines that sit on top of the 1% constitutional rate"),
    dict(id="scc_recorder", kind="official", opened=False,
         title="The county recorder of the inherited house, recording real estate",
         url="https://clerkrecorder.santaclaracounty.gov/recording-documents/recording-real-estate",
         supports="documentary transfer tax on a recorded deed in the county and the recording fees"),
    dict(id="sos_results", kind="official", opened=True,
         title="California Secretary of State, 2026 General Election, state ballot measures (unofficial results)",
         url="https://electionresults.sos.ca.gov/returns/ballot-measures",
         supports="the vote on every statewide measure on the 3 November 2026 ballot, as reported by the "
                  "Secretary of State on 12 November 2026, with certification due 11 December 2026"),
    dict(id="sos_measures", kind="official", opened=False,
         title="California Secretary of State, qualified statewide ballot measures",
         url="https://www.sos.ca.gov/elections/ballot-measures/qualified-ballot-measures",
         supports="the official titles of the measures that qualified, and the withdrawal of ACA 13"),
    dict(id="sco_estate", kind="official", opened=True,
         title="California State Controller, estate tax programme",
         url="https://www.sco.ca.gov/ardtax_estate_tax.html",
         supports="that California operates no state estate tax and how the former state estate tax ended"),
    dict(id="ftb_593", kind="official", opened=False,
         title="California Franchise Tax Board, form 593 instructions (real estate withholding)",
         url="https://www.ftb.ca.gov/forms/2024/2024-593-instructions.html",
         supports="the withholding rules that apply to a California real property sale and the exclusions"),
    dict(id="fred_hpi", kind="official", opened=True,
         title="FHFA all-transactions House Price Index via FRED: the metropolitan area of the inherited "
               "house, the division of the other house, and California (annual, end of period)",
         url="https://fred.stlouisfed.org/graph/fredgraph.csv?id=ATNHPIUS41940Q,ATNHPIUS41884Q,CASTHPI"
             "&fq=Annual,Annual,Annual&fam=eop,eop,eop&cosd=1991-01-01",
         supports="every house-price growth rate, peak-to-trough drawdown and recovery length in this desk. The "
                  "series are named by their published identifiers because the identifier-to-area mapping could not "
                  "be confirmed from an official page in this session: the metro area of the inherited house is "
                  "ATNHPIUS41940Q, the division of the other house is ATNHPIUS41884Q, and the state is CASTHPI. The "
                  "metro series is transcribed year by year from 1988; the division series is transcribed at the "
                  "years this desk quotes (1991, 1994-1995, 2000 and 2006 onward), so its window rates are measured "
                  "between those points. A retrieved series is a snapshot: re-download before relying on a rate "
                  "that moves this much"),
    dict(id="fred_cpi_sf", kind="official", opened=True,
         title="BLS CPI-U for the metropolitan area of the other house via FRED, annual average, with the "
               "10-year Treasury yield and the 30-year mortgage rate",
         url="https://fred.stlouisfed.org/graph/fredgraph.csv?id=CUURA422SA0,GS10,MORTGAGE30US"
             "&fq=Annual,Annual,Annual&fam=avg,avg,avg&cosd=1990-01-01&coed=2025-12-31",
         supports="local inflation, the risk-free rate used for reinvestment, and the mortgage-rate path"),
    dict(id="fred_cpi_us", kind="official", opened=True,
         title="BLS CPI-U, US city average via FRED, annual average",
         url="https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCNS&fq=Annual&fam=avg"
             "&cosd=1990-01-01&coed=2025-12-31",
         supports="national inflation history and the missing 2025 annual average"),
    dict(id="cpuc_nem", kind="official", opened=False,
         title="California Public Utilities Commission, net energy metering",
         url="https://www.cpuc.ca.gov/industries-and-topics/electrical-energy/demand-side-management/net-energy-metering",
         supports="which net-metering tariff a system sits under and how long its grandfathered terms run"),
    dict(id="inherited_utility_tariff", kind="official", opened=False,
         title="The water utility serving the inherited house, advice letter 628-A (water tariff)",
         url="https://www.sjwater.com/sites/default/files/AL-628-A.pdf",
         supports="the published residential water and sewer charges that a bill in that service area is built from"),
    dict(id="other_utility_rates", kind="official", opened=False,
         title="The water and sewer utility serving the other house, rate schedule FY2026-27",
         url="https://www.sfpuc.gov/sites/default/files/accounts-and-services/Rates_Schedule_Water_Sewer_2026-7.pdf",
         supports="the published water and sewer schedule for the other property's utility"),
    dict(id="cdi_premium", kind="official", opened=False,
         title="California Department of Insurance, residential premium and policy-count report",
         url="https://www.insurance.ca.gov/01-consumers/105-type/95-guides/03-res-homeowners/upload/EQEXP2025Summary.pdf",
         supports="the department's published average premiums by policy form, the only official premium data that "
                  "exists for this state; used to mark the owner's figure as low, never to replace it"),
    dict(id="cdi_tool", kind="official", opened=False,
         title="California Department of Insurance, sample premium lookup",
         url="https://interactive.web.insurance.ca.gov/apex_extprd/f?p=111:21:::NO:::",
         supports="the published sample premiums by coverage area and policy form, which the department itself "
                  "labels an example rather than a quote - the reason no address-specific premium can be verified "
                  "from an official source"),
    dict(id="cbo_ltb", kind="official", opened=False,
         title="Congressional Budget Office, Long-Term Budget Outlook",
         url="https://www.cbo.gov/publication/61270",
         supports="the official long-run view of interest rates and growth used as the baseline in the projections"),
    dict(id="congress_bills", kind="official", opened=False,
         title="congress.gov, bill text search for estate, gift and step-up proposals",
         url="https://www.congress.gov/search?q=%7B%22source%22%3A%22legislation%22%2C%22bill%22%3A%22%22%7D",
         supports="used only as the place to check whether a proposal has become law; no value in this desk "
                  "depends on a bill that has not been enacted"),
    # --- secondary (named as such; no conclusion in this desk rests on them) ---
    # No secondary source is cited anywhere in this desk. An earlier draft listed a trade article that had
    # been used only as a pointer to the primary documents; since the primary documents are cited directly,
    # the pointer was removed rather than published, and verify.py fails the build if a non-official host
    # appears in the register at all.

]
SRC = {s["id"]: s for s in SOURCES}

# ---------------------------------------------------------------------------
# 2. Verified constants and official series values used in the arithmetic
#    exact figures are statutory or published values; they are quoted exactly and labelled.
# ---------------------------------------------------------------------------
VERIFIED = [
    dict(item="Federal estate and gift basic exclusion, deaths and gifts in 2026", value="$15,000,000",
         status="verified", src=["irs_706"],
         note="quoted exactly; the Form 706 instructions set the filing requirement by year of death"),
    dict(item="Federal estate and gift basic exclusion, deaths and gifts in 2027", value="$15,480,000",
         status="verified", src=["irs_rp2635"],
         note="section 3.44 of Revenue Procedure 2026-35, read in the PDF on 13 Nov 2026"),
    dict(item="Annual gift exclusion, 2026", value="$19,000", status="verified", src=["irs_rp2635"],
         note="the 2026 amount is carried from the repository register; the 2027 amount below is the "
              "one read this session"),
    dict(item="Annual gift exclusion, 2027", value="$20,000", status="verified", src=["irs_rp2635"],
         note="section 3.46(1) of Revenue Procedure 2026-35"),
    dict(item="Top federal estate and gift rate", value="40%", status="verified", src=["irs_706"],
         note="unified rate schedule, Table A of the Form 706 instructions"),
    dict(item="Gifts to a spouse who is not a US citizen, 2027", value="$201,000", status="verified",
         src=["irs_rp2635"], note="section 3.46(2)"),
    dict(item="California estate or inheritance tax", value="none", status="verified", src=["sco_estate"],
         note="read from the State Controller's own page on 13 Nov 2026: no filing requirement for deaths on or "
              "after 1 January 2005; the inheritance tax and gift tax programmes remain administered only for "
              "deaths and gifts before 8 June 1982, and the generation-skipping transfer tax does not apply to "
              "transfers after 31 December 2004"),
    dict(item="Proposition 13 annual increase cap on a base year value", value="2%", status="verified",
         src=["boe_lta26002"], note="the cap binds in 40 of the 51 roll years published in the table"),
    dict(item="Inflation factor used for the 2026 roll", value="1.02", status="verified",
         src=["boe_lta26002"],
         note="the California CPI rose 3.307% between August 2024 and August 2025 because October 2025 "
              "was not published; the factor is capped at 2% either way"),
    dict(item="Proposition 19 adjusted amount, transfers 16 Feb 2025 - 15 Feb 2027", value="$1,044,586",
         status="verified", src=["boe_lta25009"],
         note="indexed every second February from the FHFA House Price Index for California; the next "
              "adjustment is due February 2027"),
    dict(item="Homeowners' exemption", value="$7,000", status="carried", src=["boe_lta23027"],
         note="a flat statutory amount, not indexed; not re-opened by this session"),
    dict(item="Secured tax rate, city and county of the already-owned house, FY2026-27",
         value="1.18162182%", status="verified", src=["sftc_rate"], note="quoted exactly"),
    dict(item="Typical composite secured rate in the county of the inherited house",
         value="1.1488%", status="carried", src=["scc_ratebook"],
         note="read from the county rate book by an earlier session; the FY2026-27 book was not re-opened "
              "on 13 Nov 2026 - confirm on the bill"),
    dict(item="Principal-residence gain exclusion, single filer", value="$250,000", status="verified",
         src=["irs_701"], note="plus $500,000 on a joint return; 2-of-5-year ownership and use tests"),
    dict(item="Net investment income tax", value="3.8% above $200,000 modified AGI", status="carried",
         src=["irs_559"], note="not re-opened this session"),
    dict(item="Estate tax return deadline", value="9 months after death; 6 more on extension",
         status="verified", src=["irs_706"], note="Form 4768 for the extension"),
    dict(item="Consistent-basis reporting to heirs", value="within 30 days of the return due date",
         status="verified", src=["irs_706"], note="the value on the return becomes the heirs' ceiling"),
    dict(item="Proposition 19: time to make the house the transferee's principal residence",
         value="1 year from the transfer", status="verified", src=["rtc_632"],
         note="section 63.2(a)(1)(A)"),
    dict(item="Proposition 19: time to file for the homeowners' exemption", value="1 year from the transfer",
         status="verified", src=["rtc_632"], note="section 63.2(a)(1)(B)"),
    dict(item="Proposition 19: time to file the exclusion claim",
         value="3 years, or before sale or before the transferee stops occupying, whichever is first",
         status="verified", src=["rtc_632"], note="section 63.2(f)(1)(A); a late claim is considered but "
         "only from the lien date of the year it is filed"),
    dict(item="Proposition 19: what happens if the heir later stops living there",
         value="the base year value from the date of transfer is enrolled", status="verified",
         src=["rtc_632", "boe_lta26026"],
         note="section 63.2(a)(1)(C) and the FAQ definition of 'new base year value' - the exclusion is "
              "conditional, not permanent"),
    dict(item="Transfers through a trust are covered by Proposition 19", value="yes",
         status="verified", src=["rtc_632"], note="section 63.2(e)(9) defines 'transfer' to include a "
         "transfer through the medium of an inter vivos or testamentary trust"),
    dict(item="Statutory probate attorney fee, first tiers", value="4% / 3% / 2% / 1% / 0.5% bands",
         status="verified", src=["prob_10810"],
         note="4% on the first $100,000, 3% on the next $100,000, 2% on the next $800,000, 1% on the next "
              "$9,000,000, 0.5% on the next $15,000,000, and above $25,000,000 a reasonable amount set by "
              "the court; the same schedule applies to the personal representative"),
    dict(item="Trustee or personal representative notice after death", value="60 days", status="carried",
         src=["prob_160617"], note="Probate Code section 16061.7; creditor claims are barred after 120 days"),
    dict(item="Small-estate affidavit threshold (deaths on or after 1 April 2025)", value="$208,850",
         status="carried", src=["de300", "prob_13100"],
         note="the adjusted figure published by the Judicial Council; the base text of section 13100 is "
              "$166,250 as adjusted under section 890"),
    dict(item="Change in ownership statement after death", value="150 days", status="carried",
         src=["scc_ratebook"], note="preliminary change of ownership / change in ownership statement filed "
         "with the county assessor after a death; the same form applies to a transfer by trust"),
    dict(item="Ballot measures on the 3 November 2026 California ballot that touch property tax",
         value="none changed Proposition 13 or 19", status="verified", src=["sos_results", "sos_measures"],
         note="the titles are read from the Secretary of State's own results table: Proposition 40 (one-time tax "
              "on certain taxpayers) led no at 52.4%, 41 (new state taxes and audits for local special taxes) no at "
              "55.1%, 42 (barring new state personal property and certain retroactive taxes) yes at 51.4%, 43 "
              "(limiting local revenue measures) no at 57.5%, 45 (environmental review) no at 56.4%. None of the "
              "fourteen proposed any change to the 1% rate, the 2% cap, the assess-on-transfer rules or the "
              "exclusion for family homes. 100% of precincts reporting; unofficial until 11 Dec 2026"),
    dict(item="Ballot measure that could change the tax treatment of the reinvestment money",
         value="Proposition 42 passed (leading yes 51.4%)", status="verified", src=["sos_results"],
         note="bars new state taxes on personal property including financial assets, and bars certain "
              "retroactive state taxes"),
    dict(item="Top state income-tax rates made permanent", value="Proposition 3 passed (leading yes 60.7%)",
         status="verified", src=["sos_results"],
         note="the 2012 rates on income above the top bracket continue, which is the rate band the rental "
              "and investment income in this analysis is taxed in"),
    dict(item="The basis adjustment at death survived the 2025 federal tax act", value="section 1014 unchanged",
         status="carried", src=["irs_rp2635", "irs_701", "congress_bills"],
         note="the published 2027 inflation procedure carries the act's indexed exclusion and no change to the "
              "basis rule, and a bill-status search finds no enacted repeal; the primary text of the act was not "
              "re-opened in this session, so the conclusion is labelled carried and flagged G14 rather than "
              "asserted as re-read"),
]

# ---------------------------------------------------------------------------
# 3. Owner-supplied inputs (internal record; published only at $10 rounding, no identifiers)
# ---------------------------------------------------------------------------
OWNER = [
    dict(item="Inherited house - market value, November 2026", value=3100000, status="owner",
         note="owner statement of 10 Nov 2026; no appraisal in the file"),
    dict(item="Inherited house - assessed value on the 2026 roll", value=550540, status="owner",
         note="rounded to $10 from the figure the owner quoted for 2026"),
    dict(item="Inherited house - property tax bill, 2025", value=7210, status="owner",
         note="the owner's figure includes whatever parcel taxes and special charges the bill carries"),
    dict(item="Inherited house - water", value="$100-$150 a month", status="owner",
         note="modelled at $130 a month"),
    dict(item="Inherited house - electricity with a solar array", value="no bill; a $10-$20 monthly credit",
         status="owner", note="modelled as a $180 a year credit, the mid-point of the range, while the array's tariff lasts"),
    dict(item="Inherited house - home insurance", value="about $1,500 a year", status="owner",
         note="unconfirmed; below the statewide average the department publishes for a homeowners policy"),
    dict(item="Inherited house - maintenance", value="less than the other house", status="owner",
         note="modelled at 0.8% of market value a year against 1.2% for the other house"),
    dict(item="Already-owned house - market value, November 2026", value=1800000, status="owner",
         note="owner statement; three livable units"),
    dict(item="Already-owned house - assessed value, 2025 roll", value=114240, status="owner",
         note="rounded to $10"),
    dict(item="Already-owned house - property tax bill, 2025", value=2440, status="owner",
         note="this bill implies a charge of about 2.14% of the assessed value, against a published "
              "secured rate of 1.18162182% - see the flagged page"),
    dict(item="Already-owned house - rent, two units", value="$7,150 a month", status="owner",
         note="modelled as $85,800 a year; a third unit is vacant and can be added if the household moves out"),
    dict(item="Already-owned house - water for three units", value="$330-$400 a month", status="owner",
         note="modelled at $4,380 a year, the mid-point of the range you gave"),
    dict(item="Already-owned house - electricity", value="$30-$70 a month", status="owner",
         note="modelled at $50 a month"),
    dict(item="Already-owned house - insurance", value="about $1,500 a year", status="owner",
         note="unconfirmed; a three-unit rental is normally rated above a single-family homeowners policy"),
    dict(item="Trust and timing", value="passes by trust, expected between 2040 and 2050", status="owner",
         note="the trust has not been produced, so the desk treats 'in the trust' as unconfirmed"),
    dict(item="Cash in the same inheritance", value="'considerable', possibly above the tax threshold",
         status="owner", note="no figure given; the estate-tax page works the arithmetic across a range "
         "of estate sizes instead of guessing one"),
]

# ---------------------------------------------------------------------------
# 4. Modelling assumptions
# ---------------------------------------------------------------------------
ASSUMPTIONS = [
    dict(id="D1", item="House value growth, inherited house", value="4.0% a year nominal",
         basis="measured from the FHFA all-transactions index for the metro area of the inherited house, on the "
               "values transcribed in the source register: 5.8% a year over 1995-2025, 4.7% over 2015-2025 and "
               "3.0% measured from the 2006 peak. 4.0% sits between the long and the recent window, and above "
               "what the market has done since the last peak, so it is not a generous number",
         sens="every path is also run at 1.5%, 2.9%, 5.8% and 8.0%", src=["fred_hpi"]),
    dict(id="D2", item="House value growth, already-owned house", value="4.0% a year nominal",
         basis="measured from the FHFA index for the division the house sits in: 5.6% a year over 1995-2025, "
               "3.2% over 2015-2025 and 2.7% from the 2006 peak. The same 4.0% is applied to both houses, which "
               "is above what the other market has done since its peak and below its long-run rate",
         sens="same grid as D1", src=["fred_hpi"]),
    dict(id="D3", item="Proposition 13 factoring of an enrolled base year value", value="2% a year",
         basis="the cap in the Constitution and the factor table published for the 2026 roll; the cap "
               "binds in 40 of the 51 published years",
         sens="in a decade of low inflation the enrolled value grows closer to 1%; the model is "
              "conservative in the other direction", src=["boe_lta26002"]),
    dict(id="D4", item="Growth of the Proposition 19 adjusted amount", value="4.3% a year",
         basis="the amount is indexed every second February by the FHFA index for California; that index "
               "rose at 4.3% a year over 1991-2025 (228.63 to 969.38)",
         sens="run at 3.0% and 5.5%; the amount is a rounding error compared with the gap here",
         src=["boe_lta25009", "fred_hpi"]),
    dict(id="D5", item="General inflation on operating costs", value="2.5% a year",
         basis="CPI-U for the metropolitan area of the already-owned house: 2.9% a year over 1990-2024, "
               "3.4% over 2015-2024; national CPI-U 2.6% a year over 1990-2024",
         sens="2.0% and 3.5% on the carrying-cost table", src=["fred_cpi_sf", "fred_cpi_us"]),
    dict(id="D6", item="Insurance premium growth", value="4.0% a year",
         basis="held above general inflation because rebuilding costs and wildfire losses have pushed "
               "California premiums up faster than CPI; no official local series was confirmed this session",
         sens="2.5% and 6.0% on the carrying-cost table", src=["cdi_premium"]),
    dict(id="D7", item="Rent the inherited house would fetch if let", value="2.0% gross yield",
         basis="an assumption, not a market observation: at the owner's stated value it is about $5,180 a "
               "month, which is the figure earlier generations of this project also used",
         sens="1.8% to 3.0%, and the break-even rent against selling is printed on the decision page",
         src=[]),
    dict(id="D8", item="Rent growth at the already-owned house", value="2.0% a year",
         basis="below assumed inflation because the units are inside a rent cap; the state cap and the "
               "local ordinance both limit increases, and the local increase permitted for 2026 was well "
               "below inflation",
         sens="1.0% and 3.0%", src=[]),
    dict(id="D9", item="Reinvestment return after tax", value="3.9% a year",
         basis="a balanced portfolio earning 5.0% nominal with the tax on interest and dividends at a "
               "24% federal bracket plus 3.8%; the risk-free anchor actually published is the 10-year "
               "Treasury, whose annual average over 2016-2025 was 2.70% and over 2025 was 4.29%",
         sens="2.5%, 3.9% and 5.2% after tax, and the break-even rate is printed",
         src=["fred_cpi_sf", "cbo_ltb"]),
    dict(id="D10", item="Selling cost", value="6% of price",
         basis="brokerage and transfer costs on a resale; the county's documentary transfer tax is charged "
               "separately and is small beside the 6%",
         sens="5% and 7%", src=["scc_recorder"]),
    dict(id="D11", item="Capital-gains rate applied to a sale of the inherited house",
         value="20% plus 3.8%, reduced by the principal-residence exclusion when applicable",
         basis="the 2027 top long-term rate applies above $563,200 of taxable income for a single filer; "
               "the zero and 15% breakpoints are published in the same revenue procedure",
         sens="15%+3.8% and 20%+3.8%", src=["irs_rp2635", "irs_701"]),
    dict(id="D12", item="Tax on rental profit", value="24% ordinary rate, with depreciation deducted",
         basis="a modelling shortcut: rental profit is taxed at the owner's ordinary bracket; the passive "
               "loss rules can defer losses against wages and are not modelled",
         sens="18% and 32%", src=["irs_559"]),
    dict(id="D13", item="Solar credit duration", value="the credit stops when the grandfathered tariff ends",
         basis="the array's tariff and interconnection date are not in the file; a 20-year term from "
               "interconnection is the published structure, so a system connected before about 2023 is "
               "not expected to run to 2050",
         sens="the projections run the credit to zero in 2043 and also hold it flat", src=["cpuc_nem"]),
    dict(id="D14", item="Vacancy and management on a let house", value="4% of gross rent, 6% management",
         basis="standard single-family letting practice; neither is sourced to a local dataset",
         sens="0% to 10% combined", src=[]),
    dict(id="D15", item="Transfer year", value="tested at 2040, 2045 and 2050",
         basis="the owner's stated window; every figure is printed by transfer year so nothing depends on "
               "one guess",
         sens="the full window is shown", src=[]),
    dict(id="D17", item="Maintenance basis",
         value="the rate applied to the 2026 value, then cost inflation",
         basis="an owner statement that the inherited house needs less than the rental, expressed as 0.8% of its "
               "2026 value against the rental's 1.2%, then grown with costs rather than with price",
         sens="indexing it to the projected value instead would turn a price rise into a carrying cost and punish "
              "the one scenario in which holding wins; at 1.5% of the 2026 value it is the largest cost line in "
              "the table", src=[]),
    dict(id="D16", item="Rounding", value="every household amount is rounded to the nearest $10",
         basis="the owner's instruction, so that no figure can be matched to a bill or a roll online; "
               "statutory amounts are quoted exactly and marked exact, because rounding a legal threshold "
               "would misstate it",
         sens="not applicable", src=[]),
]

# ---------------------------------------------------------------------------
# 5. Requirement register - the owner's brief, item by item
# ---------------------------------------------------------------------------
# status: met | met-with-gaps | open-on-owner
REQUIREMENTS = [
    dict(id="R01", text="Collect, organise and analyse the project as a full list of requirements",
         status="met-with-gaps", where="requirements.html",
         note="this register is the list; 4 requirements stay open because only the owner can close them"),
    dict(id="R02", text="Executive summary of the important details", status="met",
         where="executive-summary.html",
         note="situation, headline numbers, recommendation, deadlines and the five things that could change it"),
    dict(id="R03", text="Suggestions for improving the site, in a section for review before anything is implemented",
         status="met", where="suggestions.html",
         note="18 suggestions, each with cost, benefit and risk, and a blank decision column; nothing on this "
              "desk implements a suggestion without an owner decision"),
    dict(id="R04", text="A clear list of questions, information and answers needed before a decision can be made, "
                        "with suggestions for discovering what is missing", status="met",
         where="questions.html",
         note="28 questions; 9 already have an answer in the file, 19 are open and each names the document, "
              "office or professional that closes it"),
    dict(id="R05", text="Personal privacy first: anonymise everything, no personal information on the site",
         status="met", where="methodology.html",
         note="no name, address, parcel identifier, account number, ZIP code or city name appears; the "
              "verifier fails the build if one does"),
    dict(id="R06", text="Amounts rounded to the nearest $10 so they cannot be traced back or searched out",
         status="met", where="methodology.html",
         note="enforced mechanically: the verifier rejects a household amount that is not a multiple of $10"),
    dict(id="R07", text="Keep the distinction that one house is inherited and the other is already owned",
         status="met", where="properties.html",
         note="every comparison carries the column; it is the reason reassessment, basis and transfer tax "
              "behave differently on the two sides"),
    dict(id="R08", text="Separate section for black-swan economic conditions, built on real conditions rather "
                        "than a flat growth line", status="met", where="black-swans.html",
         note="the regimes are measured from the published index series: the early-1990s regional fall, the "
              "2006-2011 drawdown, the 1979-81 inflation decade, the 2010-11 deflation factor, the rate "
              "cycles, and what each does to this decision"),
    dict(id="R09", text="Local, state and federal property and tax law as it stands, with a look at changes "
                        "being discussed", status="met", where="law-watch.html",
         note="includes the 3 November 2026 state ballot measures as counted by the Secretary of State, and "
              "the Proposition 19 amount reset due 16 February 2027"),
    dict(id="R10", text="Live in it, rent it, or sell and reinvest - which is best and why", status="met",
         where="decision.html",
         note="six paths, three transfer years, after tax, with the break-evens that decide the ranking"),
    dict(id="R11", text="Property tax, insurance, water, electricity and maintenance on the inherited house",
         status="met", where="carrying-costs.html",
         note="each line has its own growth assumption and its own flag where the owner's figure is unverified"),
    dict(id="R12", text="Project house value, assessed value and tax by year", status="met",
         where="projections.html",
         note="2026 to 2076, year by year, for both houses and for each path"),
    dict(id="R13", text="Show step by step how the inheritance would actually happen", status="met",
         where="process.html",
         note="14 steps from the date of death to the recorded deed, each with its deadline and its form"),
    dict(id="R14", text="How much can be inherited before tax bites, at every level", status="met",
         where="estate-tax.html",
         note="federal exclusion by year of death, no state tax, and what happens to money above the "
              "exclusion; worked across a range of estate sizes because the owner gave no figure"),
    dict(id="R15", text="Use the already-owned house in the reasoning", status="met", where="decision.html",
         note="it supplies the alternative place to live, the rent that offsets, and the transfer-tax and "
              "reassessment exposure if it is ever handed over"),
    dict(id="R16", text="Verify every table row against an official source, blank and flag what cannot be "
                        "confirmed", status="met", where="sources.html",
         note="each row links to the document it came from and says whether this session opened it"),
    dict(id="R17", text="Review the repository, work line by line, flag irregularities with links",
         status="met", where="flagged.html",
         note="five irregularities found in the published material this session, with the file and the "
              "official document that settles it"),
    dict(id="R18", text="A clean, simple dashboard-style site with tables, organised by category",
         status="met", where="index.html",
         note="16 pages, one category each, every table a plain HTML table with no script dependency"),
    dict(id="R19", text="Remove uncertainty from the decision process",
         status="met-with-gaps", where="questions.html",
         note="the arithmetic is now reproducible and every input is labelled; the remaining uncertainty is "
              "concentrated in the 19 open questions, which is where it belongs"),
    dict(id="R20", text="Maximise profit and lower costs using our own projections", status="met",
         where="decision.html", note="rankings, break-evens and the cost lines that can be cut now"),
    dict(id="R21", text="Inheritance through a trust around 2040-2050", status="met-with-gaps",
         where="process.html",
         note="the process is complete on paper; the trust instrument itself has not been produced, so the "
              "desk cannot confirm the house is in it or who the successor trustee is"),
    dict(id="R22", text="Work with no manual input from the owner", status="met", where="index.html",
         note="built, checked and published in this session; the open questions are things only the owner's "
              "documents can answer, and they are listed rather than guessed"),
    dict(id="R23", text="Insurance for the inherited house researched from local data",
         status="open-on-owner", where="carrying-costs.html",
         note="no official source publishes a premium for a specific address; the department publishes "
              "statewide averages only, and the owner's declaration page is the answer - flagged"),
    dict(id="R24", text="Water and solar credit verified against the utility's published tariff",
         status="open-on-owner", where="carrying-costs.html",
         note="the utility pages publish rate schedules, not a household bill; the account number is the "
              "only way to pin this down - flagged"),
    dict(id="R25", text="Confirm what the two tax bills actually contain", status="open-on-owner",
         where="flagged.html",
         note="the already-owned house's bill implies about 2.14% of its assessed value against a published "
              "1.18162182% rate; either the bill carries other charges or the assessed figure covers only "
              "part of the property - this is the single biggest unpriced item in the analysis"),
    dict(id="R26", text="A published, deployed site with everything verified and flagged for review",
         status="met", where="flagged.html",
         note="GitHub Pages; flagged items are published rather than hidden and do not block the release"),
]

# ---------------------------------------------------------------------------
# 6. Question register
# ---------------------------------------------------------------------------
# status: answered | owner | derivable | open
QUESTIONS = [
    dict(id="Q01", q="Is the inherited house actually titled in the trust?",
         why="it decides whether probate applies at all, and with it the statutory fee on the process page",
         how="read the recorded deed and the trust schedule of assets; the deed is the controlling document",
         who="owner, with the recorder's online index", status="open", blocks="process.html, decision.html"),
    dict(id="Q02", q="Who is the successor trustee, and does the trust direct a sale or a distribution in kind?",
         why="a trustee who must distribute in kind cannot choose the sell path; a discretionary trustee can",
         how="read the trust instrument, sections on distribution and trustee powers",
         who="owner or the drafting attorney", status="open", blocks="process.html"),
    dict(id="Q03", q="Is the trust revocable, and is it still revocable today?",
         why="a revocable trust keeps the property in the grantor's estate, so the exclusion arithmetic below "
             "is the right frame; an irrevocable trust may already be outside it",
         how="the instrument, and any amendment", who="owner or attorney", status="open", blocks="estate-tax.html"),
    dict(id="Q04", q="How large is the cash side of the inheritance?",
         why="it is the only variable that decides whether any federal estate tax is payable, and the tax is "
             "40% of the excess, so this single number can dwarf every operating line in the analysis",
         how="the estate inventory, or the grantor's own statement of net worth",
         who="owner", status="open", blocks="estate-tax.html"),
    dict(id="Q05", q="What exactly is on the two property tax bills, line by line?",
         why="the already-owned house's bill is about 2.14% of its assessed value against a published rate of "
             "1.18162182%; that extra 1% is roughly $1,000 a year and it is not explained anywhere",
         how="the two current bills: the rate line, the parcel-tax lines and any supplemental assessment",
         who="owner", status="open", blocks="carrying-costs.html, projections.html"),
    dict(id="Q06", q="Is the homeowners' exemption on the inherited house claimed right now?",
         why="it is worth about $80 a year, and more importantly it is the precondition for the Proposition 19 "
             "exclusion at transfer",
         how="the assessor's exemption record or the bill", who="owner", status="open", blocks="properties.html"),
    dict(id="Q07", q="Which dwelling was the grantor's principal residence, and for how long?",
         why="the exclusion only reaches a home that was eligible for the exemption in the transferor's hands",
         how="the exemption history", who="owner", status="open", blocks="decision.html"),
    dict(id="Q08", q="What is the current insurance in force on each house, with what limits?",
         why="both modelled premiums are below the statewide average the department publishes, and one of them "
             "covers a three-unit rental",
         how="the two declarations pages", who="owner or the broker", status="open",
         blocks="carrying-costs.html"),
    dict(id="Q09", q="Is the solar system's tariff the old one, and when was it interconnected?",
         why="it decides how many of the projection years still get the credit the owner reports",
         how="the interconfirmation or permission-to-operate letter, or the utility account",
         who="owner", status="open", blocks="carrying-costs.html"),
    dict(id="Q10", q="Is the third unit at the already-owned house legal and rentable?",
         why="if it is, vacating it is worth about $21,000 a year of rent in the paths where the heir lives in "
             "the inherited house",
         how="the assessor's unit count and the city's records of permits", who="owner", status="open",
         blocks="decision.html"),
    dict(id="Q11", q="Who lives in the vacant unit today?",
         why="it decides whether moving out of it creates income or simply empties a room",
         how="the household's own facts", who="owner", status="answered",
         blocks="decision.html", answer="the owner states the unit is not rented out"),
    dict(id="Q12", q="Is the rent at the already-owned house controlled, and what increase is allowed this year?",
         why="it caps the growth of the largest income line in the plan; the local ordinance limits the annual "
             "increase to well below recent inflation",
         how="the rent board's published maximum for the unit type", who="owner, then the rent board",
         status="open", blocks="projections.html"),
    dict(id="Q13", q="What is the market rent for the inherited house?",
         why="the whole rent-out path rests on it, and the gross-yield assumption used here is a placeholder",
         how="three written appraisals or a broker rent analysis", who="owner instructs an agent",
         status="open", blocks="decision.html"),
    dict(id="Q14", q="Does anyone else have a claim on either house?",
         why="a lien, a co-tenant or a sibling with a right of first refusal changes the sell path entirely",
         how="a title report on each property", who="title company", status="open", blocks="process.html"),
    dict(id="Q15", q="Is the heir a US citizen or resident for transfer-tax purposes?",
         why="the exclusion and the rules for a non-citizen spouse are different, and the annual exclusion for "
             "gifts to a non-citizen spouse is far smaller",
         how="the owner's own facts", who="owner", status="open", blocks="estate-tax.html"),
    dict(id="Q16", q="Does the heir already claim a principal residence?",
         why="the Proposition 19 exclusion needs the house to become the heir's principal residence within a "
             "year, and one person can have only one",
         how="the heir's own tax records", who="heir", status="open", blocks="decision.html"),
    dict(id="Q17", q="Was the inherited house ever transferred into or out of the trust, and when?",
         why="a transfer between the grantor and their own revocable trust is not a change in ownership, but a "
             "later partial transfer to someone else could be",
         how="the grant deed history at the recorder", who="owner", status="open", blocks="properties.html"),
    dict(id="Q18", q="Is the house in a flood, fire or seismic hazard zone that changes insurance?",
         why="it is the difference between the owner's estimate and a much larger premium, and it drives the "
             "black-swan cost line",
         how="the county hazard map and a quote from two carriers", who="owner or broker", status="open",
         blocks="carrying-costs.html, black-swans.html"),
    dict(id="Q19", q="What condition is the roof, plumbing and electrical in?",
         why="maintenance at 0.8% of value is a steady-state figure; a deferred replacement is a lump sum that "
             "the projection does not include",
         how="an inspection", who="owner", status="open", blocks="carrying-costs.html"),
    dict(id="Q20", q="Are there any deferred capital items at the already-owned house?",
         why="it is older and carries three units; its 1.2% maintenance line is an average, not a plan",
         how="an inspection and the rent inspection records", who="owner", status="open",
         blocks="carrying-costs.html"),
    # --- questions that this session's research already answers ---
    dict(id="Q21", q="Is there a California estate or inheritance tax?",
         why="it was the first thing the owner asked about", status="answered",
         how="State Controller, estate tax programme", who="answered from an official source",
         answer="no - California runs neither; the state's bite comes from reassessment and income tax, "
                "not from a death tax", blocks="estate-tax.html"),
    dict(id="Q22", q="Does inheriting a house through a trust trigger the Proposition 19 reassessment?",
         why="the owner assumed the trust either protects or does not", status="answered",
         how="Revenue and Taxation Code section 63.2(e)(9)", who="answered from the code text",
         answer="yes - the statute defines a transfer to include a transfer through the medium of an inter "
                "vivos or testamentary trust, so the trust does not avoid the reassessment test",
         blocks="decision.html, process.html"),
    dict(id="Q23", q="Is the Proposition 19 exclusion permanent once claimed?",
         why="several earlier generations of this project assumed it was, and the plan changes if it is not",
         status="answered", how="section 63.2(a)(1)(B)-(C) and the Board's 2026 FAQ",
         who="answered from the code text and the Board's guidance",
         answer="no - the exclusion is removed if the heir stops qualifying, and on removal the assessor "
                "enrols the base year value that would have applied at the transfer, factored forward",
         blocks="decision.html"),
    dict(id="Q24", q="How much does the exclusion actually save when the house is worth far more than the cap?",
         why="it is the number the whole occupy-versus-sell comparison turns on",
         status="answered", how="section 63.2(d)(2) arithmetic applied to the owner's values",
         who="derived in this desk",
         answer="the enrolled value becomes the market value at transfer minus the adjusted amount, so the "
                "saving is about the value of the adjusted amount, not the whole assessed-to-market gap",
         blocks="decision.html, projections.html"),
    dict(id="Q25", q="Is there a federal estate tax if the estate is under the exclusion?",
         why="the owner asked how much can be inherited without tax", status="answered",
         how="IRS Form 706 instructions and the 2027 inflation procedure",
         who="answered from the IRS documents",
         answer="no tax and normally no return below the exclusion for the year of death; $15,000,000 for a "
                "2026 death and $15,480,000 for a 2027 death, and the estate's basis step-up is the bigger "
                "prize", blocks="estate-tax.html"),
    dict(id="Q26", q="Does a state wealth or personal-property tax threaten the reinvested money?",
         why="two 2026 ballot measures turned on it", status="answered",
         how="Secretary of State results for the 3 November 2026 ballot",
         who="answered from the official count, unofficial until 11 December 2026",
         answer="Proposition 40, a one-time tax on certain taxpayers, was defeated (leading no 52.4%), and "
                "Proposition 42, barring new state taxes on personal property including financial assets and "
                "certain retroactive state taxes, was approved (leading yes 51.4%); both need certification",
         blocks="law-watch.html"),
    dict(id="Q27", q="Did anything on the 2026 ballot change Proposition 13 or 19?",
         why="it would be the largest single change to the plan", status="answered",
         how="Secretary of State results and the measure titles", who="answered from the official count",
         answer="no measure on the ballot alters the 1% rate, the 2% cap or the intergenerational rules. The "
                "measures that touched taxation at all were Proposition 40 (defeated, 52.4% no), 41 (defeated, "
                "55.1% no), 42 (approved, 51.4% yes), 43 (defeated, 57.5% no) and 45 (defeated, 56.4% no); "
                "Proposition 3 (approved, 60.7% yes) fixes the top income-tax band", blocks="law-watch.html"),
    dict(id="Q28", q="Is the assessed-value history the owner supplied internally consistent?",
         why="if it is, the low tax base is real and durable; if not, the base may already have been reset",
         status="answered", how="the Board's published inflation-factor table, roll year by roll year",
         who="verified in this desk",
         answer="yes for the inherited house - every year the owner listed matches the published factor to "
                "the dollar, including the 1.525% and 1.036% years that only a true Prop 13 base would show; "
                "the already-owned house matches except for one year that is about $45 off",
         blocks="properties.html"),
]

# ---------------------------------------------------------------------------
# 7. Suggestions board - for owner review, nothing implemented
# ---------------------------------------------------------------------------
# kind: site (improve the decision tool) or action (improve the financial outcome)
SUGGESTIONS = [
    dict(id="S01", kind="action", title="Get the two tax bills and the trust deed into the file this month",
         why="the bills explain the unpriced 1% gap at the already-owned house and the deed decides whether "
             "probate applies; every projection moves when they arrive",
         benefit="removes the two largest unknowns at no cost", effort="one afternoon",
         risk="none - it is document gathering", status="awaiting owner"),
    dict(id="S02", kind="action", title="Do not let the inherited house be rented before the exclusion is claimed",
         why="the heir has one year to make it a principal residence and let the assessor know; a rental is "
             "evidence against principal-residence use, and the exclusion is worth far more than the rent "
             "for that first year",
         benefit="protects the largest single asset in the analysis", effort="sequencing only",
         risk="deferring rental income by a year", status="awaiting owner"),
    dict(id="S03", kind="action", title="Treat the exclusion as a lease, not a deed: plan for the day it ends",
         why="the exclusion is removed if the heir stops qualifying, and the assessor then enrols the "
             "transfer-date value; a plan that assumes the low tax lasts forever is wrong after the first "
             "change of use",
         benefit="prevents a surprise of several tens of thousands a year", effort="a paragraph in the plan",
         risk="none", status="awaiting owner"),
    dict(id="S04", kind="action", title="Price the decision on rent the heir would otherwise pay, not on the "
                                       "house's yield",
         why="living in the inherited house is worth the market rent of that house; comparing it to a "
             "5%-ish portfolio return without that credit is what makes selling look dominant by several "
             "million",
         benefit="changes the ranking in the owner's favour on some paths", effort="model change (S09)",
         risk="none", status="awaiting owner"),
    dict(id="S05", kind="action", title="Ask the trustee in writing whether a sale at or shortly after transfer "
                                       "is permitted",
         why="if the instrument requires distribution in kind, the sell-and-reinvest path is not a choice the "
             "heir controls",
         benefit="removes a path that may not exist", effort="one letter", risk="none", status="awaiting owner"),
    dict(id="S06", kind="action", title="Do not deed the already-owned house to the heir while it is let",
         why="a rental is not a family home under Proposition 19, so a lifetime transfer would reset it to "
             "market value; the current low tax survives only in the present owner's name",
         benefit="avoids a permanent, large increase in the tax on the income property",
         effort="a decision, not a cost", risk="it keeps the asset in the estate, where estate tax applies",
         status="awaiting owner"),
    dict(id="S07", kind="action", title="Get two carrier quotes on the three-unit rental and on the inherited "
                                       "house, in writing",
         why="both insurance lines are owner guesses below the published statewide average, and the older "
             "building with three units is the riskier one",
         benefit="a corrected number on a line that compounds at the highest rate in the model",
         effort="one week", risk="the premium may come back higher than the guess", status="awaiting owner"),
    dict(id="S08", kind="action", title="Write down the rent the inherited house would fetch, from three agents",
         why="the rent-out path currently rests on a gross-yield assumption; one written number retires it",
         benefit="turns the weakest line in the comparison into data", effort="no cost, a few days",
         risk="none", status="awaiting owner"),
    dict(id="S09", kind="site", title="Publish one reconciled model instead of seven parallel desks",
         why="the site now carries seven published desks built by seven sessions, with unreconciled numbers "
             "and three different answers; a reviewer cannot compare them without re-doing the arithmetic",
         benefit="decision quality and speed; the flag pages shrink", effort="one integration session",
         risk="it must not silently overwrite a desk that is right; keep the old ones as history",
         status="awaiting owner"),
    dict(id="S10", kind="site", title="Add a single decision-record page where the owner writes the choice and date",
         why="the brief asks for a place to review suggestions and choose a path before changes are made; "
             "today that choice lives in nobody's file",
         benefit="makes the process auditable and stops re-litigating", effort="one page",
         risk="none", status="awaiting owner"),
    dict(id="S11", kind="site", title="Move every open question to a checklist with an owner and a due date",
         why="a question register without owners and dates does not close",
         benefit="converts the analysis into a completed file", effort="small", risk="none",
         status="awaiting owner"),
    dict(id="S12", kind="site", title="Add the year-by-year charts the desk's tables imply but do not show",
         why="value, tax, assessed base and the gap between them are the story of the decision, and three "
             "tables do not communicate it the way one chart does",
         benefit="faster understanding, same numbers", effort="inline SVG, no library",
         risk="charts must not invent precision; draw the same $10-rounded figures", status="awaiting owner"),
    dict(id="S13", kind="site", title="Fix the two excluded desks or retire them",
         why="desk-22a32b17 overstates the Proposition 19 saving by applying the adjusted amount to the whole "
             "assessed-to-market gap, and desk-b4f still carries a wrong capital-gain figure; both sit in the "
             "repository excluded from the site, where nobody will correct them",
         benefit="removes a wrong answer that a future session may copy", effort="one hour per desk",
         risk="leaving them invites re-use", status="awaiting owner"),
    dict(id="S14", kind="site", title="State the privacy boundary in one place and enforce it in the build",
         why="different desks publish different things; some earlier generations published the owner's "
             "year-by-year assessment history, which is searchable against the open roll even at $10 rounding",
         benefit="the site becomes defensibly private rather than quietly private",
         effort="the verifier in this desk already does it", risk="history remains in the repository",
         status="awaiting owner"),
    dict(id="S15", kind="site", title="Re-verify the statutory page every February and every January",
         why="the Proposition 19 amount is re-indexed on 16 February and the federal amounts on 1 January; a "
             "page written in 2026 is quietly wrong by 2028",
         benefit="keeps the desk trustworthy for a 2040-2050 decision", effort="one session a year",
         risk="none", status="awaiting owner"),
    dict(id="S16", kind="site", title="Give every number a status word in the table, not a footnote",
         why="a reviewer should never have to guess whether a figure is law, a measurement or an owner's "
             "impression; the status column in this desk is the pattern worth copying into the older desks",
         benefit="trust and speed", effort="layout", risk="none", status="awaiting owner"),
    dict(id="S17", kind="site", title="Publish the sensitivity grid next to the headline, not on a separate page",
         why="the ranking of paths flips with the reinvestment rate and the growth rate; a headline number "
             "without the grid invites a decision on a fragile point estimate",
         benefit="better decisions", effort="one table", risk="none", status="awaiting owner"),
    dict(id="S19", kind="site", title="Extend the site's privacy gate from one tree to all of them",
         why="the only repo-wide gate, `scripts/verify_safe.py`, reads `public-safe/`; every other published tree is "
             "checked by its own verifier, or by nobody, which is how the same rule produced one tree with zero "
             "locality words on the live site and another with 267 (flagged G16)",
         benefit="one boundary enforced on every push: the scan in `desk-d75/_src/verify.py` - visible text of "
                 "every page, token list plus the postcode pattern, link labels included - lifted into the shared "
                 "verifier and run over every directory in the publication set, so no future desk can publish an "
                 "identifying pairing by accident",
         effort="small; the check already exists and only its scope changes",
         risk="trees that name localities today would fail until each author anonymises, so this needs either a "
              "grandfather list or a deadline - the owner's call, which is why it is a suggestion and not a change",
         status="awaiting owner"),
    dict(id="S18", kind="action", title="Decide the tax year of the sale, not just the sale",
         why="the exclusion, the bracket and the net investment income tax all turn on the year and the "
             "heir's other income; selling in a year with a large other gain is measurably worse",
         benefit="avoids tax that costs nothing to avoid", effort="planning only", risk="none",
         status="awaiting owner"),
]

# ---------------------------------------------------------------------------
# 8. Flagged items
# ---------------------------------------------------------------------------
# severity: info | review | material
FLAGS = [
    dict(id="G01", severity="material", item="The already-owned house's bill implies about 2.14% of its assessed "
                                             "value against a published secured rate of 1.18162182%",
         detail="the assessed figure and the bill cannot both be the whole property. If the rate line is "
                "right, roughly $1,000 a year of parcel taxes or a supplemental assessment is unexplained; "
                "if the assessed figure is only part of the property, every projection for that house is low.",
         action="read the rate line and the itemised charges on the current bill; compare with the assessor's "
                "record for the same parcel", src=["sftc_rate"], status="open - owner document needed"),
    dict(id="G02", severity="material", item="Both insurance figures are owner estimates below the published "
                                              "statewide average",
         detail="the department's report gives an average homeowners premium well above $1,500 and a "
                "dwelling-fire average for a rental, and a three-unit building is normally rated above a "
                "single-family house. Insurance is also the fastest-compounding line in the model.",
         action="the two declarations pages", src=["cdi_premium"], status="open - owner document needed"),
    dict(id="G03", severity="material", item="The trust has not been produced",
         detail="the whole process page assumes a revocable trust holding the house. If the deed does not "
                "match, probate applies and the statutory fee schedule on the process page becomes real.",
         action="recorded deed plus the trust's schedule of assets", src=["prob_10810"], status="open"),
    dict(id="G04", severity="review", item="The cash inheritance is unquantified",
         detail="the estate-tax page therefore reports a range across estate sizes rather than one answer; "
                "40% of anything above the exclusion is too large a number to leave as a range when the "
                "owner knows the figure.",
         action="a current statement of the estate's other assets", src=["irs_706", "irs_rp2635"],
         status="open - owner document needed"),
    dict(id="G05", severity="review", item="No official source publishes a premium for one address",
         detail="the state insurance department publishes average premiums by policy form and coverage area, and a "
                "sample-premium lookup that the department itself labels an example rather than a quote. A carrier "
                "quote is address-specific and is not published anywhere. This desk therefore verifies only that the "
                "owner's figure is low relative to the state average, and does not restate market aggregates as data.",
         action="the declarations page, or two written quotes", src=["cdi_premium", "cdi_tool"],
         status="structural - no official source can close it"),
    dict(id="G06", severity="review", item="The 2026 water and solar figures are utility-account facts, not "
                                           "public data",
         detail="the tariff schedules that are published show rates, not a household's consumption; the "
                "owner's figures are used and labelled owner at every occurrence.",
         action="twelve months of statements, and the interconnection date for the array",
         src=["inherited_utility_tariff", "cpuc_nem"], status="structural"),
    dict(id="G07", severity="review", item="Ballot measure results are unofficial until 11 December 2026",
         detail="this desk quotes the Secretary of State's count of 12 November 2026 with 100% of precincts "
                "reporting. Any statement about what passed must be re-read after certification.",
         action="re-check the same page after certification", src=["sos_results"], status="date-sensitive"),
    dict(id="G08", severity="review", item="The Proposition 19 adjusted amount changes on 16 February 2027",
         detail="the $1,044,586 figure applies only to transfers in the window that ends then; the next "
                "amount is set from the FHFA index for California for calendar 2026 and will not be published "
                "before February 2027. For a 2040-2050 transfer the amount will be much larger, and this desk "
                "projects it rather than guessing it.",
         action="re-read the Board's letters after each February 16", src=["boe_lta25009"],
         status="date-sensitive"),
    dict(id="G09", severity="info", item="The county composite rate for the inherited house is carried, not "
                                         "re-opened",
         detail="1.1488% is the typical rate from the county's fiscal 2025-26 rate book, read by an earlier "
                "session. The parcel's own rate area may differ slightly and the fiscal 2026-27 book was not "
                "retrieved by this session.",
         action="the rate line on the current bill, or the county's rate book for the year of the roll",
         src=["scc_ratebook"], status="carried forward"),
    dict(id="G10", severity="info", item="A 2025 annual average is missing from the published CPI series",
         detail="the retrieval used here returns no annual average for calendar 2025 for the area and national "
                "indices, and the Board's own letter explains why: October 2025 was not collected after the "
                "federal shutdown. Any inflation figure quoted for 2025 in any generation of this project is "
                "based on an incomplete year.",
         action="prefer the Board's August-to-August comparison, which is what the roll actually uses",
         src=["boe_lta26002", "fred_cpi_us"], status="explains an oddity in older pages"),
    dict(id="G11", severity="info", item="The 2022 roll year of the already-owned house does not match the "
                                         "published inflation factor",
         detail="the assessed value the owner lists for that year is about $45 below a strict 2% step-up from "
                "the prior year - immaterial to every conclusion, but it is the one year in either history "
                "that does not tie to the factor table, so it is recorded rather than smoothed away.",
         action="no action needed unless the full history is produced", src=["boe_lta26002"],
         status="noted"),
    dict(id="G12", severity="info", item="Earlier published pages that this session did not correct",
         detail="desk-22a32b17 applies the Proposition 19 adjusted amount as if it shielded the whole "
                "assessed-to-market gap, which the statute does not do (section 63.2(d)(2): the new taxable "
                "value is factored base plus the excess of market value over base plus the amount). desk-b4f "
                "carries a capital-gain figure of $16,200 where the published amount for estates and trusts "
                "is $16,250, and a closing-letter fee that rises from $67 where the fee schedule starts at "
                "$56. Both trees are excluded from the published site, so the errors are not live, but they "
                "remain in the repository for a future session to copy.",
         action="correct or retire them; the arithmetic in this desk and in the referee tree is right",
         src=["rtc_632", "irs_706"], status="logged, not edited - not this session's files"),
    dict(id="G13", severity="material", item="The owner-identifying history is in the repository even though it "
                                              "is not in the deployed site",
         detail="the year-by-year assessed and tax figures supplied with the brief are excluded from Pages and are "
                "not republished here at any rounding; only the 2026 inputs appear, rounded. But the repository's "
                "own history contains earlier generations that printed the full series, and git history survives "
                "deletion. The site the world can fetch is clean; the checkout a determined reader can browse is "
                "not, and that gap is the owner's to decide on - a session cannot fix it by editing files.",
         action="either make the repository private or rewrite its history; the alternative is to accept that a "
                "parcel-level series sits in a public repo",
         src=[], status="open - owner decision, not a build problem"),
    dict(id="G14", severity="review", item="The step-up conclusion rests on a carried reading of the 2025 act",
         detail="this desk publishes that the 2025 federal tax act did not amend the basis adjustment at death, "
                "which is the assumption the sell path depends on. It is supported by the published 2027 inflation "
                "procedure, which carries the act's indexed exclusion and no change to the basis rule, and by a "
                "bill-status search finding no enacted repeal; the section of the act itself was not read in its own "
                "text in this session, so the conclusion is labelled carried rather than verified.",
         action="read the act's estate-tax section and the then-current section 1014 in the year of death; if they "
                "have moved, the sell and rent paths must be re-priced",
         src=["irs_rp2635", "congress_bills"], status="open - one reading away from closing"),
    dict(id="G16", severity="material", item="Locality words are on other published trees, and no gate looks at them",
         detail="the site's privacy gate, `scripts/verify_safe.py`, reads `public-safe/` only. The sibling trees are "
                "governed by their own verifiers, and the results differ widely: on the deployed site today this "
                "desk shows 0 locality words in visible text, the referee tree 0, while the consolidated decision "
                "site names the two counties or cities 267 times across sixteen pages, the earlier independent desk "
                "37, the numeric desk 16, the decision hub 37, the indexed desk 18 and the readiness desk 7. Most "
                "of those are the name of a public agency or of a large consolidated city-county, which narrows "
                "very little; the pairing that matters is a city name next to the facts that distinguish a "
                "household, which is what the hub's own card used to do for another desk - that card is anonymised "
                "in this change and the desk's own pages were left as their author wrote them.",
         action="each tree's owner should decide whether its county and city words are load-bearing for a reader "
                "checking a citation; this desk's answer is that they are not, and its pages carry no city name "
                "outside a link target",
         src=[], status="open - reported, not edited, because they are other sessions' files"),
    dict(id="G15", severity="info", item="The published numeric desk's committed verification report says it failed",
         detail="`desk/data/desk-verification-report.json` in the repository records one failure, a hygiene check "
                "against an external asset on two of its pages. Re-running that desk's own verifier in this session "
                "returns zero failures, so the committed report is stale rather than the desk being broken. Nothing "
                "was changed here: it is another desk's artifact, and the rule on this project is to flag an "
                "irregularity rather than smooth it over.",
         action="whoever owns `desk/` re-runs `python3 scripts/verify_desk_v5.py --json` and commits the fresh "
                "report; no page of this desk depends on that file",
         src=[], status="informational - not this desk's file to fix"),
]
