# desk-03242c78 — coverage desk

A privacy-first, source-verified decision desk for two California properties: Property A, a
house in Santa Clara County expected through a trust between 2040 and 2050, and Property B, a
three-unit building in San Francisco County that is already owned.

Open `index.html`, or start from the repository hub.

## What this desk adds

This is a coverage and traceability desk, not a clone of the existing desks. Its contribution
is the tax detail worked in dollars from primary documents:

* Revenue and Taxation Code section 63.2 quoted verbatim, with the Proposition 19 applicable
  amount (**$1,044,586** for 16 February 2025 to 15 February 2027) taken from BOE LTA 2025/009.
* Measure H's operative rate schedule quoted from the ordinance text, with the election result.
* The 2026 and 2027 federal estate figures, the unified rate schedule, Form 8971, special-use
  valuation and section 6166 conditions from the Form 706 instructions.
* Section 121, depreciation and recapture, and the California 1% surtax worked through each
  path rather than asserted.
* Crossovers: the house-growth and equity-return values at which the recommendation reverses.
* Nine paths (three pure, four mixed, two phased) compared at identical dates and horizons,
  with shelter valued at market rent on every path so no path receives free housing.

## Rebuild

```sh
python3 desk-03242c78/_src/model.py     # writes _src/model.json
python3 desk-03242c78/_src/build.py     # writes the 39 pages from the model
python3 desk-03242c78/_src/verify.py    # fails on any broken rule
python3 -m unittest discover -s desk-03242c78/_src -p "test_*.py"
```

`_src/` is Jekyll-excluded: the model contains the owner-supplied anchors before rounding.

## Rules the build enforces

* Every table row carries an official source link or an explicit status tag.
* Every money figure is a multiple of $10, except statutory amounts, which are wrapped in
  `class="stat"` and registered against the document that states them.
* No names, addresses, parcel numbers, ZIP codes, or locality names beyond the three
  county-level identifiers; no scripts, images, or external requests.
* The verifier fails rather than warns.

## Not advice

A planning document prepared for review by a licensed California attorney and a CPA. Owner
figures are approximate and unverified; every assumption is labelled as one.
