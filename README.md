# Tino5 — Property Inheritance Decision Support

A source-verified, **anonymized** decision dashboard for a planned 2040–2050 trust inheritance of a
Cupertino property (ZIP 95014), with a San Francisco rental/residence property (ZIP 94122) as the
housing anchor.

**Live site:** published from `docs/` on the `main` branch via GitHub Pages.

## Privacy (highest priority)

No personal information appears in any published site file. Identities, street addresses, trust
names and account identifiers are replaced with placeholders (`Property A`, `Property B`,
`Beneficiary`, `Trust`). Geography stops at city and ZIP-code level. Client-supplied financial
figures are anonymous scenario inputs and are never presented as verified facts.

## Three value classes — never mixed

| Class | Meaning | Rendering |
| --- | --- | --- |
| `VERIFIED` | Read directly from an official government page | Value shown; row links to that page |
| `CLIENT INPUT — UNVERIFIED` | Supplied in the brief | Official-value cell left **blank**; flagged |
| `MODEL OUTPUT — NOT AN OFFICIAL VALUE` | Computed from explicit assumptions | Labelled as model output; flagged |

Every data-table row has a link to an official government source. Values that cannot be confirmed
are left blank and published on the **Flagged for Review** page. No value is inferred or filled in.
All dollar figures are rounded to the nearest $10.

## Site map

| Page | Contents |
| --- | --- |
| `index.html` | Dashboard, KPIs, bottom-line recommendation |
| `executive-summary.html` | Executive summary with clear numbers |
| `properties.html` | Anonymous client inputs and tax/assessment history |
| `tax-law.html` | Verified federal, state and local law/figures |
| `inheritance-process.html` | Step-by-step trust inheritance and statutory clocks |
| `projections.html` | 2026–2050 market value, assessed value, property tax |
| `costs.html` | Carrying costs and every model parameter |
| `decision-analysis.html` | Live / rent / sell comparison, sensitivity, break-even |
| `estate-tax.html` | Exemptions, projected headroom, 40% rate matrix |
| `law-changes.html` | Enacted, pending and proposed law changes |
| `flagged.html` | **Flagged for Review** — unverified values and irregularities |
| `sources.html` | Complete official source registry |
| `methodology.html` | Privacy, verification and limitations |

## Reproduce locally

```bash
python3 model/build_data.py      # -> data/site_data.json (source of truth)
python3 scripts/build_site.py    # -> docs/*.html
python3 scripts/verify.py        # verification + research/verification-log.md
python3 scripts/write_research.py
cd docs && python3 -m http.server 8000
```

No third-party packages are required. The site is plain HTML/CSS/JS with no build tool and no
external CDN dependencies, so it works offline and behind the GitHub Pages proxy.

## Repository layout

```
COORDINATION.md          shared task board / session log
data/site_data.json      single source of truth (sources, tables, flags, summary)
model/build_data.py      official source registry, assumptions, projections, decision model
scripts/build_site.py    static HTML renderer
scripts/verify.py        line-by-line verification + HTTP smoke test
scripts/write_research.py
research/                human-readable notes with official links + verification log
docs/                    published static site (GitHub Pages source)
docs/.nojekyll          disables Jekyll processing
```

## Coordination

Multiple agent sessions may work on this repository. Read `COORDINATION.md` before starting, claim
a task with non-overlapping file scope, commit and push the claim immediately, and record sources,
verification and irregularities there when done. Shared outputs (`data/site_data.json`,
`docs/index.html`, navigation) are integration-owned.

## Disclaimer

Research and modelling only — not legal, tax, appraisal or investment advice. Confirm all figures
with the linked government agencies and a qualified adviser before acting.
