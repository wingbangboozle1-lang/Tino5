# Estate decision desk

A source-linked decision desk for a future trust inheritance (**Property A**) and a separate
property already owned outright (**Property B**). The two are analysed separately, because one is
inherited and the other is not.

**Site map:** the root [`index.html`](index.html) is the hub. It links the published desks:
[`desk/`](desk/index.html) (the numeric decision desk, 2026–2076, $10 rounding),
[`public-safe/`](public-safe/index.html) (the privacy-first curated dashboard, no household
figures), [`desk-e86/`](desk-e86/index.html) (46-question decision-readiness register),
[`review-092b/`](review-092b/index.html) (question/suggestion hub), [`decision-ad038/`](decision-ad038/index.html)
(indexed projections and law), [`swan-3a49/`](swan-3a49/index.html) (uneven-economy replay) and
[`referee-abae/`](referee-abae/index.html) (independent cross-check). The publication set is
recorded in `PUBLISHED_DESKS` in [`scripts/verify_safe.py`](scripts/verify_safe.py); every other
top-level directory is excluded from Pages by the fail-closed gate and by `_config.yml`.
`desk-22a32b17/` stays excluded until its Proposition 19 cap error is corrected and `desk-b4f/`
until referee X04/X05 are corrected.

**Live site:** https://wingbangboozle1-lang.github.io/Tino5/ → root hub → the desks above.

A working decision aid, not advice. It asks one question — when the house passes to the heir
somewhere between 2040 and 2050, should the heir move in, rent it out, or sell it and reinvest? —
and answers it three ways: with arithmetic that can be re-run, with sourced law, and with stress
cases that break the arithmetic.

| Page (lead desk `desk/`) | What it answers |
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

## Privacy

Every dollar amount is rounded to the nearest $10 so that no figure can be traced back to a
specific bill. Statutory amounts, rates, and thresholds are the exception: they are quoted exactly
and marked as exact, because rounding a legal threshold would misstate it. No desk carries names,
addresses, parcel identifiers or ZIP codes; year-by-year assessment or tax-bill histories are not
published at any precision (a rounded series still matches one parcel against open assessor rolls).

`desk-22a32b17/` and the legacy trees still contain owner-derived figures from earlier
generations; they are excluded from Pages and flagged. Excluding a directory from the built site
hides it; it does not remove it from the repository — anything that must not be public has to be
deleted, and repository history is an owner decision.

## Reproducing it

```bash
python3 scripts/model_v5.py                                   # writes desk/data/model-v5.json
python3 -m unittest discover -s scripts -p 'test_model_v5.py'  # 20 regression tests
python3 scripts/build_desk_v5.py                              # writes desk/*.html
python3 scripts/verify_desk_v5.py --json                      # the desk contract
python3 scripts/build_desk.py                                 # writes public-safe/*.html
python3 scripts/verify_safe.py                                # published-surface gate
python3 scripts/check_landing.py                              # hub links resolve
python3 scripts/privacy_scan.py --summary                     # identifier scan
python3 review-092b/_src/verify.py                            # decision hub contract
python3 desk-e86/verify.py                                    # readiness desk contract
python3 decision-ad038/_src/verify_site.py                    # indexed desk contract
python3 referee-abae/_src/crosscheck.py                       # independent cross-check
```
