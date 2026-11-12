# referee-abae: independent numeric referee (session arena-abae1b53, task abae/R)

Published pages: `referee-abae/*.html` (Jekyll skips this `_src` folder). Rebuild and check:

    python3 referee-abae/_src/build.py                          # regenerate the 7 pages + style.css
    python3 -m unittest discover -s referee-abae/_src -v       # 22 checks: engine, rows, privacy, links
    python3 referee-abae/_src/crosscheck.py                    # which trees are published; row/link/privacy counts

| File | Role |
| --- | --- |
| `engine.py` | Reference model of the occupy / rent / sell comparison. Household inputs have **no defaults**. |
| `reproduce.py` | Loads the anchors from `desk-b4f/scripts/after_tax_model.py` **at run time, in memory** and re-derives the desk's published figures. |
| `regime.py` | Historical windows from the official series transcribed in `swan-3a49/data/` (reads the working tree, or `origin/arena/3a49d618-tino5` if not merged). |
| `registry.py` | Official constants, links, spot checks. Every figure carries a source URL and a status (read in the official source / secondary only). |
| `analysis.py` | Computes every number a page shows: rates, ratios, counts, pass/fail. No dollar level derived from household inputs. |
| `build.py` | Renders the pages. |
| `crosscheck.py` | Scans every HTML tree in the repository: published or excluded, rows with an official link, privacy-scan categories, superseded figures. Prints counts and paths only. |
| `test_*.py` | Unit tests; `test_build.py` fails if a household-derived dollar level, a place name or an identifier shape reaches a page. |

## Honest limits
* `engine.py` was written after reading desk-b4f's model. Agreement with that desk is replication, not independent validation.
* Window analysis approximates total return as S&P price growth plus the mean dividend-price ratio (checked against the TSP C Fund, within 0.2 points).
* Nothing in this folder verifies property-specific inputs (rent, tax-rate area, insurance, transfer date).

## Withdrawing the pages
The pages carry ratios, rates and counts only. If the owner or the integration session prefers not to publish an ordering at all, add one line,
`- referee-abae`, to the `exclude:` list in `_config.yml`. Nothing else depends on this folder.
