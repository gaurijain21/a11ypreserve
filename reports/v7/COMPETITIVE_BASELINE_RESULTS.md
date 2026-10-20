# Competitive source-aware baseline

## Method

The executable baseline in `scripts/v7_competitive_baseline.py` independently
extracts source contract facts and checks direct destination evidence: role
presence, exact alternative-text values, link targets, document title, language,
note, formula, caption, list, and table evidence. It does not import the frozen
comparator.

## Known-fault result

| Method | Valid known destination faults | Detected |
|---|---:|---:|
| Independent source-aware baseline | 59 | 25 |
| Full A11yPreserve | 59 | 46 |

The baseline detected 25/59 faults, with family-level results in
`experiments/v7/V7_COMPETITIVE_BASELINE.json`. This is not an accuracy result:
the denominator is a controlled fault-injection set, and no independent
adjudicated primary labels are available. The comparison does provide a fairer
competitor than tag presence or visible-text equality and supports a narrower
claim that the full procedure detects additional faults in this operator set.
