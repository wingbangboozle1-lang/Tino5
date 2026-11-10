# Cost research (anonymized)

Research date: 2026-11-10 (UTC). Client-provided utility, insurance and
maintenance figures are **unverified** and appear with blank official-value cells on the site.

## What an official source does and does not provide

| Cost | Official source | What it confirms | What remains unverified |
| --- | --- | --- | --- |
| Primary-residence insurance, 95014 | [CDI_TOOL](https://interactive.web.insurance.ca.gov/apex_extprd/f?p=111:21:::NO:::) | CDI publishes sample annual premiums effective May 1, 2026 for "SANTA CLARA CUPERTINO"; explicitly not a quote | The property-specific premium |
| Statewide homeowner premium | [CDI_AVG](https://www.insurance.ca.gov/01-consumers/180-climate-change/sustainable-insurance-strategy.Cfm) | California average $1,570/yr (rounded); page updated Oct 27, 2026 | ZIP-specific premium; landlord policy |
| Rental / landlord insurance, 94122 | [CDI_REPORT](https://www.insurance.ca.gov/0400-news/0200-studies-reports/0250-homeowners-study/) | ZIP-level earned premiums by policy form (dwelling-fire, homeowners, renters, condo) | The property-specific premium |
| Water, 95014 | [CPUC_WATER](https://docs.cpuc.ca.gov/PublishedDocs/Efile/G000/M359/K001/359001611.PDF) | CPUC tariff lists "portions of Cupertino" in a regulated water service territory; usage-based rates | A fixed monthly bill |
| Water / power, 94122 | [SFPUC_RATES](https://sfpuc.org/accounts-services/water-power-and-sewer-rates) | Official 2026-27 water, sewer and power rate schedules | A fixed monthly bill for 3 units |
| Solar export credit | [CPUC_SB695](https://www.cpuc.ca.gov/-/media/cpuc-website/divisions/office-of-governmental-affairs-division/reports/2025/2025-sb-695-report_093025.pdf) | NEM 1.0/2.0 20-year legacy periods remain in effect when a solar property changes hands; new systems since April 2023 use the Net Billing Tariff | Interconnection date and monthly credit |
| Rent benchmark, 95014 | [HUD_FMR](https://www.huduser.gov/portal/datasets/fmr/fmr2026/FY2026_FMR_Schedule.pdf) | FY2026 4-BR FMR $5,010/mo for the San Jose HMFA (official program benchmark) | Property-specific market rent |
| SF rent increase | [SF_RENT](https://www.sf.gov/learn-about-rent-increases-san-francisco/) | 1.6% allowable increase for covered units, 3/1/2026-2/28/2027 | Whether the two let units are covered |
| Repairs and maintenance | [IRS_P527](https://www.irs.gov/publications/p527) | Repairs are deductible rental expenses; improvements are capitalised | Any cost benchmark for these properties |

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
