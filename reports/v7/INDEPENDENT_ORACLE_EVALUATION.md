# Independent oracle evaluation

## Executed protocol

`python scripts/v7_independent_oracle_audit.py` inspected all 130 primary
fixture--pipeline cases and all 65 supplementary Word cases. The implementation
uses standard-library DOCX ZIP/XML inspection, pypdf 6.18.1, and PyMuPDF
1.28.2. It imports neither the frozen destination extractor nor the frozen
comparator. Per-case records are under
`experiments/v7/independent_oracle_cases/`.

## Result

| Unit | Count |
|---|---:|
| Total archived cases | 195 |
| Primary cases | 130 |
| Supplementary Word cases | 65 |
| Extraction errors | 0 |

The implementation produced bounded observations such as structure-role
presence, alternative-text values, language evidence, URI actions, note/formula/
caption roles, and metadata. It did not produce independent adjudicated labels.
That distinction is recorded in `V7_INDEPENDENT_ORACLE.json`.

## Interpretation

This is independent implementation corroboration, not independent expert
validation. Agreement or disagreement with a frozen six-way classification is
diagnostic only. A separate human adjudicator remains required before any claim
of external ground truth can be made.
