# Baseline and ablation evaluation

Status: COMPLETED WITH LIMITATIONS.

The executable baseline evidence currently available is a bounded source-aware
structural baseline on 59 known valid V6 mutants: it detected 25/59, compared
with 46/59 coarse-classification detections by the full historical method. The
family-level baseline detections are recorded in
`experiments/v7/V7_COMPETITIVE_BASELINE.json`.

The evidence supports the narrow claim that source-aware pairing plus the
full evidence-aware procedure detects more of these known injected faults than
the deliberately simpler structural baseline. It is not an independent truth
set and not a claim about population accuracy. The evidence does not support
inventing binary labels for unresolved or unsupported cases. A complete
six-baseline table involving tag presence, text equality, destination-only
checks, secondary-evidence ablation, and forced binary abstention policy is
not fully executable from the frozen release without choosing new adjudication
rules; that gap remains explicit rather than being filled with synthetic labels.

Evidence: `experiments/v7/V7_COMPETITIVE_BASELINE.json`,
`experiments/v7/V7_SEMANTIC_EQUIVALENCE.json`, and the frozen V6 mutation rows.
