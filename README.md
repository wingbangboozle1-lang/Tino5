# Estate decision desk

A source-linked decision desk for a future trust inheritance (**Property A**) and a separate
property already owned outright (**Property B**). The two are analysed separately, because one is
inherited and the other is not.

**Site map:** the root [`index.html`](index.html) is the hub and links to the published curated dashboard at [`public-safe/index.html`](public-safe/index.html). Three further desks are kept in the repository and excluded from Pages until the owner approves publication, because the verifier fails closed for every top-level directory except `public-safe/`: [`decision-ad038/`](decision-ad038/index.html), [`review-092b/`](review-092b/index.html), and [`desk/`](desk/index.html).

**Live site:** https://wingbangboozle1-lang.github.io/Tino5/ → `public-safe/index.html`

A working decision aid, not advice. It asks one question — when the house passes to the heir
somewhere between 2040 and 2050, should the heir move in, rent it out, or sell it and reinvest? —
and answers it three ways: with arithmetic that can be re-run, with sourced law, and with stress
cases that break the arithmetic.

| Page | What it answers |
| --- | --- |
| [Overview](desk/index.html) | The question, the headline figures, and where to start |
| [Executive summary](desk/executive-summary.html) | The whole picture on one page |
| [The decision](desk/decision.html) | Move in, rent out, or sell, compared after tax |
| [Open questions](desk/questions.html) | Known, unknown, and how to find out |
| [Projections 2026–2076](desk/projections.html) | Value, tax, and every carrying cost by year |
| [Carrying costs](desk/costs.html) | What each house costs to hold, line by line |
| [Inheritance tax](desk/estate-tax.html) | Federal estate tax, reassessment, income tax |
| [Trust process](desk/process.html) | Death to recorded title, with the deadlines |
| [Black swans](desk/black-swans.html) | Six sourced stress paths |
| [Law watch](desk/law-watch.html) | The rules the plan depends on |
| [Suggestions](desk/suggestions.html) | Options ranked by robustness |
| [Flagged for review](desk/flagged.html) | Every unverified claim, with what would close it |
| [Sources](desk/sources.html) | Every citation, and what it supports |
| [Methodology](desk/methodology.html) | Every input and assumption |
| [Repo review](desk/repo-review.html) | Legacy material and privacy risks |

An earlier, deliberately number-free version remains at `public-safe/`.

## Privacy

Every dollar amount is rounded to the nearest $10 so that no figure can be traced back to a
specific bill. Statutory amounts, rates, and thresholds are the exception: they are quoted exactly
and marked as exact, because rounding a legal threshold would misstate it.

Two earlier desks in this repository publish unrounded property-specific figures. They are a
privacy risk and are flagged on the repo review page. Excluding a directory from the built site
hides it; it does not remove it from the repository.

## Reproducing it

```bash
python3 scripts/model_v5.py                                  # writes desk/data/model-v5.json
python3 -m unittest discover -s scripts -p 'test_model_v5.py' # 17 regression tests
python3 scripts/build_desk_v5.py                             # writes desk/*.html
python3 scripts/verify_desk_v5.py --json                     # the published contract
```
