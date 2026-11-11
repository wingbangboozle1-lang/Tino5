# Privacy and reliability review — 11 November 2026

## Urgent: existing public disclosure

The repository is public, and GitHub Pages serves `main` from the repository root. Existing pages and tracked files disclose a distinctive combination of owner-supplied property, financial and household facts; some archived pages also repeat unrounded inputs. Labels such as “Property A” and rounding to $10 do not make this combination anonymous. Examples occur in the landing page, archived pages, data files and the coordination history. The issue extends beyond the landing page. This review intentionally does not reproduce those details.

Do not interpret a successful build, a search for names or a lack of addresses as a privacy verification. Data may remain in prior commits, branches, caches, forks and search indexes even after current files are edited. A safe public launch requires a repository-wide privacy inventory, removal or replacement of identifying facts and case-specific derivatives with genuinely synthetic examples, and review of Git history and other copies. Consider restricting access and consulting GitHub's [sensitive-data removal guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository). A private analysis requires storage and access controls outside a public static site. No change in this review removes the existing disclosure.

## Material reliability issues

- `pages/executive-summary.html` says estate tax almost certainly will not apply even though the total estate and lifetime gifts are unknown. The [IRS estate tax page](https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax) explains the filing threshold, includible estate, deductions and adjusted taxable gifts. A threshold is not the same as a known remaining allowance; portability is not automatic.
- The same page instructs readers to file a homeowners' exemption and parent-child exclusion even if selling. The [California BOE](https://www.boe.ca.gov/prop19/) describes the principal-residence and timing requirements. Eligibility depends on facts and timing; a blanket instruction is inappropriate.
- The executive-summary findings table contains rows without individual official source links. Existing automated link verification does not establish that every claim is accurate or that a source supports each value.
- Projected market, rent, insurance, investment and tax outcomes are assumptions, not independently verified facts. A recommendation depends on uncertain estate inclusion, basis, occupancy, local rental rules and future law. Do not treat a model winner as a guaranteed optimal decision.

## Scope and checks

Reviewed the landing page, excerpts of the executive summary and archived pages, the coordination board, GitHub repository visibility and Pages configuration. Retrieved and read the IRS and BOE pages linked above. A text search found matching case-specific financial figures in multiple HTML files. Ran `node scripts/verify.mjs`; it completed successfully but reported warnings. This was a targeted review, not a line-by-line verification of the entire repository, a live-site content audit, or a comprehensive privacy remediation. No assertion is made that other pages are safe or accurate.
