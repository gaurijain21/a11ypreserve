# V5 independent oracle validation

V5 adds an independently implemented second technical path at
`experiments/v5/independent_oracle_validation.py`. It does not import the
destination extractor, comparator, or classification implementation. It uses
PyMuPDF page text/links and direct serialized-PDF marker counts to inspect one
case per feature family for each primary pipeline, with the V4 classification
retained as the comparison target.

This is technical independent reimplementation, not external expert review or
disabled-user validation. The machine-readable agreement/disagreement table
is `experiments/v5/independent_oracle_validation.json`. Disagreements are
expected where the lightweight independent path cannot establish exact value
or cross-format association; they are evidence about oracle boundaries, not
silent corrections to V4. Any future rule modification requires a new
comparator version and affected-row rerun.
