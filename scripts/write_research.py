#!/usr/bin/env python3
"""Write the human-readable research notes (with manual-review links) from site_data.json."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = json.loads((ROOT / "data" / "site_data.json").read_text(encoding="utf-8"))
S, T, SUM = D["sources"], D["tables"], D["summary"]
R = ROOT / "research"
R.mkdir(exist_ok=True)


def link(sid):
    return f"[{sid}]({S[sid]['url']})"


def fact_table(tid):
    t = T[tid]
    out = ["| Item | Official value | Basis | Source |", "| --- | --- | --- | --- |"]
    for r in t["rows"]:
        c = [x.replace("|", "\\|") for x in r["cells"]]
        out.append(f"| {c[0]} | {c[1]} | {c[2]} | {link(r['source'])} |")
    return "\n".join(out)


# ---------------------------------------------------------------- federal
fed = f"""# Federal law research (anonymized)

Research date: {D['meta']['generated']} (UTC). Every row below was read from the linked official
government page. No secondary or commercial source is used anywhere in the published site.

## Verified federal facts

{fact_table('federal_law')}

## Key interactions for a trust inheritance

* A revocable living trust does not remove assets from the gross estate. Form 706 is filed on the
  **estate**, not on the beneficiary's share, and is due nine months after death. See {link('IRS_I706')}
  and {link('IRS_ESTATE_FAQ')}.
* The beneficiary generally has no income on receipt, but the basis of the real property becomes
  its fair market value at death. A sale at that value realises essentially no gain. See
  {link('IRS_P525')} and {link('IRS_P551')}.
* Reinvesting sale proceeds in stocks cannot use §1031: like-kind exchange treatment applies only
  to real property held for investment or business use. See {link('IRS_FS1031')}.
* If the property is held, later gain is taxed at up to 20% federal plus 3.8% NIIT, and up to
  13.3% California (which taxes capital gains as ordinary income). §121 can exclude $250,000
  ($500,000 joint) after two years of ownership and use. See {link('IRS_RP2532')},
  {link('IRS_TC559')}, {link('FTB_FEDCHANGES')} and {link('IRS_TC701')}.
* Public Law 119-21 §70106 made the $15M basic exclusion permanent and inflation-indexed after
  2026. Congress can still amend it. See {link('CONGRESS_HR1')} and {link('CONGRESS_HR1_SUM')}.

## Manual review

Open each link above and compare the 'Official value' column with the page text. The live site
reproduces these rows on the *Tax Law & Official Figures* page.
"""
(R / "federal.md").write_text(fed, encoding="utf-8")

# ---------------------------------------------------------------- california
ca = f"""# California, county and local research (anonymized)

Research date: {D['meta']['generated']} (UTC). Sources: CA Board of Equalization, Franchise Tax
Board, State Controller, Santa Clara County Assessor / Controller-Treasurer, San Francisco
Assessor-Recorder / Treasurer / Rent Board, Secretary of State, CDI, CPUC and California Courts.

## Verified state and local facts

{fact_table('state_law')}

## The single most important rule

A property owner's death is a **change in ownership as of the date of death**, including property
held in a revocable trust, even if the deed to beneficiaries is recorded years later. Reassessment
is to market value unless an exclusion applies. See {link('BOE_P800_9')} and
{link('BOE_502D')}.

The BOE-502-D statement is due within 150 days. Proposition 19 then requires:
the home was the transferor's principal residence; the transferee occupies it as principal
residence within one year; the homeowners' exemption is filed within one year; and BOE-19-P (or
BOE-19-G) is filed within three years. See {link('BOE_PROP19')} and {link('BOE_P801')}.

The value limit is the factored base year value plus an inflation-adjusted allowance. The only
official amount currently published is **$1,044,590** (rounded) for transfers from 2/16/2025
through 2/15/2027. Any market value above the cap is **added** to the new taxable value, so a
high-value home receives only partial relief. See {link('BOE_P801')}.

## No state or local death tax

The State Controller requires no California Estate Tax Return for deaths on or after January 1,
2005, and Revenue & Taxation Code §13301 prohibits the state and **any political subdivision**
from imposing a gift, inheritance, succession, legacy, income or estate tax on a death transfer.
See {link('SCO_ESTATE')} and {link('SCO_RTC13301')}.

## Official tax rates

Santa Clara County's 1.00000% maximum levy plus voter-approved bond rates are published per tax
rate area (816 TRAs in FY2025-26). San Francisco's FY2026-27 secured rate is 1.18162182%, and
the bill also carries direct charges and special assessments. See {link('SCC_RATEPDF')},
{link('SCC_RATEBOOK')} and {link('SF_TREASURER')}.

## Pending law changes

{fact_table('law_changes')}

## Irregularities

The client-supplied tax/assessment pairs imply effective rates of about
{SUM['effective_rate_a']} (Cupertino) and {SUM['effective_rate_b']} (San Francisco), above the
official ad-valorem rates. Direct charges / special assessments are a plausible explanation but
are unconfirmed. See FLAG-003 on the site's Flagged for Review page.
"""
(R / "california.md").write_text(ca, encoding="utf-8")

# ---------------------------------------------------------------- costs
costs = f"""# Cost research (anonymized)

Research date: {D['meta']['generated']} (UTC). Client-provided utility, insurance and
maintenance figures are **unverified** and appear with blank official-value cells on the site.

## What an official source does and does not provide

| Cost | Official source | What it confirms | What remains unverified |
| --- | --- | --- | --- |
| Primary-residence insurance, 95014 | {link('CDI_TOOL')} | CDI publishes sample annual premiums effective May 1, 2026 for "SANTA CLARA CUPERTINO"; explicitly not a quote | The property-specific premium |
| Statewide homeowner premium | {link('CDI_AVG')} | California average {SUM['ca_avg_insurance']}/yr (rounded); page updated Oct 27, 2026 | ZIP-specific premium; landlord policy |
| Rental / landlord insurance, 94122 | {link('CDI_REPORT')} | ZIP-level earned premiums by policy form (dwelling-fire, homeowners, renters, condo) | The property-specific premium |
| Water, 95014 | {link('CPUC_WATER')} | CPUC tariff lists "portions of Cupertino" in a regulated water service territory; usage-based rates | A fixed monthly bill |
| Water / power, 94122 | {link('SFPUC_RATES')} | Official 2026-27 water, sewer and power rate schedules | A fixed monthly bill for 3 units |
| Solar export credit | {link('CPUC_SB695')} | NEM 1.0/2.0 20-year legacy periods remain in effect when a solar property changes hands; new systems since April 2023 use the Net Billing Tariff | Interconnection date and monthly credit |
| Rent benchmark, 95014 | {link('HUD_FMR')} | FY2026 4-BR FMR {SUM['hud_fmr']}/mo for the San Jose HMFA (official program benchmark) | Property-specific market rent |
| SF rent increase | {link('SF_RENT')} | 1.6% allowable increase for covered units, 3/1/2026-2/28/2027 | Whether the two let units are covered |
| Repairs and maintenance | {link('IRS_P527')} | Repairs are deductible rental expenses; improvements are capitalised | Any cost benchmark for these properties |

## Client-supplied cost inputs (unverified)

| Item | Client figure | Official value |
| --- | --- | --- |
| Property A water | $100-$150 / month | — |
| Property A electricity / solar | +$10-$20 / month net credit | — |
| Property A home insurance | ~$1,500 / year (client guess) | — |
| Property A maintenance | "less than Property B" (qualitative) | — |
| Property B water (3 units) | $330-$400 / month | — |
| Property B electricity | $30-$70 / month | — |
| Property B rental insurance | ~$1,500 / year (client guess) | — |
| Property B rent (2 of 3 units) | $7,150 / month | — |

## Model treatment

The model uses midpoints of the client ranges, the official CDI statewide average for insurance,
0.20% of market value per year for maintenance, and 2% annual escalation. All of these are
labelled MODEL OUTPUT — NOT AN OFFICIAL VALUE and flagged. See
`docs/costs.html` → *Every model parameter* and `docs/flagged.html`.
"""
(R / "costs.md").write_text(costs, encoding="utf-8")

# ---------------------------------------------------------------- executive summary
ex = f"""# Executive Summary (anonymized)

{D['meta']['privacy']} {D['meta']['rounding']} Research date {D['meta']['generated']} (UTC).

## The decision

Property A (Cupertino, ZIP 95014) is expected to pass via trust between 2040 and 2050. The
beneficiary has a residence at Property B (San Francisco, ZIP 94122), a three-unit property with
two rented units. Options: live in Property A, rent it, or sell and reinvest after tax.

**Base case (2045 transfer, 4% appreciation, 5% portfolio return):**

| Option | Ten-year wealth | Official rule behind it |
| --- | --- | --- |
| Sell at inheritance and reinvest | {SUM['wealth_2045_sell']} | {link('IRS_P551')} (stepped-up basis), {link('IRS_FS1031')} (no §1031 for stocks) |
| Rent it out | {SUM['wealth_2045_rent']} | {link('BOE_P800_9')} (full reassessment), {link('IRS_P527')} (rental income) |
| Occupy, Prop 19 approved | {SUM['wealth_2045_occupy']} | {link('BOE_P801')}, {link('IRS_TC701')} (§121) |

**Recommendation: {SUM['best_2045']}.** Renting needs about {SUM['breakeven_rent']}/month in
2026-equivalent dollars to match selling, against an official HUD 4-BR benchmark of
{SUM['hud_fmr']}/month ({link('HUD_FMR')}). Occupying needs about
{SUM['breakeven_appreciation']} annual appreciation to match selling, against a 4.00% base
assumption. Even crediting the full HUD benchmark as imputed housing value does not close the gap.

## Important numbers

* Federal estate-tax exemption 2026: **{SUM['estate_exemption_2026']}** per person,
  **{SUM['estate_exemption_couple']}** for a couple with portability; top rate
  **{SUM['estate_rate']}** ({link('IRS_ESTATE')}, {link('IRS_I706')}). Projected 2045 single
  exemption: {SUM['estate_exemption_2045']} (model, 2% inflation). California and local
  estate/inheritance tax: **$0** ({link('SCO_RTC13301')}). Estate size was not supplied —
  FLAG-013.
* Property tax at 2045: preserved base **{SUM['tax_2045_preserved']}/yr**, full reassessment
  **{SUM['tax_2045_full']}/yr**, Prop 19 **{SUM['tax_2045_prop19']}/yr**. The exclusion saves
  only **{SUM['prop19_saving_2045']}/yr** because market value ({SUM['mv_2045']}) far exceeds
  the factored base ({SUM['assessed_2045_no_transfer']}) plus the projected allowance
  ({SUM['prop19_allowance_2045']}); the only official allowance today is
  {SUM['prop19_allowance_2025']} ({link('BOE_P801')}).
* Insurance baseline: **{SUM['ca_avg_insurance']}/yr**, the official CDI statewide average,
  flagged as not ZIP-specific ({link('CDI_AVG')}).
* Property B modelled 2026 net operating cash flow: **{SUM['noi_b_2026']}/yr** before income
  tax — the low-cost residence anchor.

## Highest-urgency actions

1. **Privacy** — no personal information is published; keep it that way.
2. Confirm the decedent's principal residence and decide on beneficiary occupancy within one
   year ({link('BOE_PROP19')}). This is FLAG-010 and the largest open uncertainty.
3. Diarise: 60-day trustee notice ({link('COURTS_TRUST')}); 150-day BOE-502-D
   ({link('BOE_P800_9')}); 1-year occupancy and homeowners' exemption, 3-year BOE-19-P
   ({link('BOE_P801')}); 9-month Form 706 ({link('IRS_ESTATE_FAQ')}).
4. Quantify the gross estate, lifetime taxable gifts and any DSUE portability election.
5. Get ZIP-specific insurance quotes via {link('CDI_TOOL')} and {link('CDI_REPORT')}.
6. Reconcile the client tax/assessment figures against actual bills (FLAG-003).
7. Re-check the November 3, 2026 California results after certification on December 11, 2026
   (unofficial returns: {link('SOS_RESULTS')}; certification: {link('SOS_RESULTS_FAQ')}).

## Conditions that would change the recommendation

Repeal of §1014 stepped-up basis; loss of Prop 19 eligibility; appreciation above
{SUM['breakeven_appreciation']}/yr; portfolio returns far below 5%; rent above
{SUM['breakeven_rent']}/month; enacted ballot or legislative changes; or non-financial
preferences. See `docs/decision-analysis.html` and `docs/law-changes.html`.

## Verification

{D['meta']['verification']} Full line-by-line record: `research/verification-log.md`.
All {SUM['flag_count']} flagged items are published on `docs/flagged.html` and do not block
publication.
"""
(R / "executive-summary.md").write_text(ex, encoding="utf-8")
print("wrote research/federal.md, california.md, costs.md, executive-summary.md")
