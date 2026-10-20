# Association and semantic attack results

## Executed protocol

`python scripts/v7_association_attack_audit.py` independently generated one
valid destination mutation for each of the 13 feature families where the
archived PDF representation permitted the operator. The script then ran the
frozen comparator on the original and mutated PDFs. Outputs and per-case
classifications are under `experiments/v7/association_cases/`.

| Outcome | Count |
|---|---:|
| Attempts | 13 |
| Applied | 12 |
| Valid PDFs | 12 |
| Scorable attacks | 12 |
| Classification detections | 11/12 |
| Unsupported/unscored | 1 |

The unsupported case is decorative images: the selected archived PDF contained
no `/Artifact` representation. The complex-table attack was valid and scorable
but retained the already non-preserved `OBSERVED_PARTIAL` classification. It
therefore did not create a confident false-preservation result, but it did not
change the coarse category either; this is a granularity blind spot that must
remain visible. The other 11 attacks changed a role, URI target, metadata value,
or association-bearing field and changed the frozen classification.

These are controlled fault injections, not independent ground truth. They show
that association-sensitive attacks can be executable and detected in most, but
not all, tested families.

The additive `scripts/v7_complex_table_diagnostic.py` detected the header-role
delta in 5/5 valid complex-table mutants. This diagnostic surfaces the fault
without retroactively changing the frozen six-way classification.
