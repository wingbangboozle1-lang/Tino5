# Executive Summary (anonymized)

No personal information appears on this site. All identities, street addresses, trust names and account numbers are replaced with placeholders; only city and ZIP-code-level geography is used. All dollar amounts are rounded to the nearest $10. Research date 2026-11-10 (UTC).

## The decision

Property A (Cupertino, ZIP 95014) is expected to pass via trust between 2040 and 2050. The
beneficiary has a residence at Property B (San Francisco, ZIP 94122), a three-unit property with
two rented units. Options: live in Property A, rent it, or sell and reinvest after tax.

**Base case (2045 transfer, 4% appreciation, 5% portfolio return):**

| Option | Ten-year wealth | Official rule behind it |
| --- | --- | --- |
| Sell at inheritance and reinvest | $10,000,370 | [IRS_P551](https://www.irs.gov/publications/p551) (stepped-up basis), [IRS_FS1031](https://www.irs.gov/pub/irs-news/fs-08-18.pdf) (no §1031 for stocks) |
| Rent it out | $7,847,410 | [BOE_P800_9](https://www.boe.ca.gov/pdf/pub800-9.pdf) (full reassessment), [IRS_P527](https://www.irs.gov/publications/p527) (rental income) |
| Occupy, Prop 19 approved | $7,208,090 | [BOE_P801](https://www.boe.ca.gov/pdf/pub801.pdf), [IRS_TC701](https://www.irs.gov/taxtopics/tc701) (§121) |

**Recommendation: 3 · Sell & reinvest.** Renting needs about $16,260/month in
2026-equivalent dollars to match selling, against an official HUD 4-BR benchmark of
$5,010/month ([HUD_FMR](https://www.huduser.gov/portal/datasets/fmr/fmr2026/FY2026_FMR_Schedule.pdf)). Occupying needs about
8.49% annual appreciation to match selling, against a 4.00% base
assumption. Even crediting the full HUD benchmark as imputed housing value does not close the gap.

## Important numbers

* Federal estate-tax exemption 2026: **$15,000,000** per person,
  **$30,000,000** for a couple with portability; top rate
  **40%** ([IRS_ESTATE](https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax), [IRS_I706](https://www.irs.gov/instructions/i706)). Projected 2045 single
  exemption: $21,852,170 (model, 2% inflation). California and local
  estate/inheritance tax: **$0** ([SCO_RTC13301](https://www.sco.ca.gov/Files-ARD-Tax-Info/estate_lawreg_lawreg.pdf)). Estate size was not supplied —
  FLAG-013.
* Property tax at 2045: preserved base **$10,710/yr**, full reassessment
  **$87,210/yr**, Prop 19 **$66,480/yr**. The exclusion saves
  only **$20,730/yr** because market value ($6,531,230) far exceeds
  the factored base ($802,030) plus the projected allowance
  ($1,552,200); the only official allowance today is
  $1,044,590 ([BOE_P801](https://www.boe.ca.gov/pdf/pub801.pdf)).
* Insurance baseline: **$1,570/yr**, the official CDI statewide average,
  flagged as not ZIP-specific ([CDI_AVG](https://www.insurance.ca.gov/01-consumers/180-climate-change/sustainable-insurance-strategy.Cfm)).
* Property B modelled 2026 net operating cash flow: **$73,100/yr** before income
  tax — the low-cost residence anchor.

## Highest-urgency actions

1. **Privacy** — no personal information is published; keep it that way.
2. Confirm the decedent's principal residence and decide on beneficiary occupancy within one
   year ([BOE_PROP19](https://www.boe.ca.gov/prop19/)). This is FLAG-010 and the largest open uncertainty.
3. Diarise: 60-day trustee notice ([COURTS_TRUST](https://santaclara.courts.ca.gov/self-help/self-help-topics/self-help-probate/self-help-probate-property-transfers/probate-trusts)); 150-day BOE-502-D
   ([BOE_P800_9](https://www.boe.ca.gov/pdf/pub800-9.pdf)); 1-year occupancy and homeowners' exemption, 3-year BOE-19-P
   ([BOE_P801](https://www.boe.ca.gov/pdf/pub801.pdf)); 9-month Form 706 ([IRS_ESTATE_FAQ](https://www.irs.gov/businesses/small-businesses-self-employed/frequently-asked-questions-on-estate-taxes)).
4. Quantify the gross estate, lifetime taxable gifts and any DSUE portability election.
5. Get ZIP-specific insurance quotes via [CDI_TOOL](https://interactive.web.insurance.ca.gov/apex_extprd/f?p=111:21:::NO:::) and [CDI_REPORT](https://www.insurance.ca.gov/0400-news/0200-studies-reports/0250-homeowners-study/).
6. Reconcile the client tax/assessment figures against actual bills (FLAG-003).
7. Re-check the November 3, 2026 California results after certification on December 11, 2026
   (unofficial returns: [SOS_RESULTS](https://electionresults.sos.ca.gov/returns/ballot-measures); certification: [SOS_RESULTS_FAQ](https://electionresults.sos.ca.gov/frequently-asked-questions)).

## Conditions that would change the recommendation

Repeal of §1014 stepped-up basis; loss of Prop 19 eligibility; appreciation above
8.49%/yr; portfolio returns far below 5%; rent above
$16,260/month; enacted ballot or legislative changes; or non-financial
preferences. See `docs/decision-analysis.html` and `docs/law-changes.html`.

## Verification

Every data-table row carries a link to an official government source. Values that cannot be confirmed are left blank and flagged. Official values, client inputs and model outputs are three separate, labelled categories. Full line-by-line record: `research/verification-log.md`.
All 20 flagged items are published on `docs/flagged.html` and do not block
publication.
