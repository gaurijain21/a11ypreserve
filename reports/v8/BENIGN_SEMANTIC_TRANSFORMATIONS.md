# Conservative benign transformations

Status: COMPLETED AND VERIFIED for the limited transformations tested.

Twenty-six controls were executed: one metadata-only rewrite and one `pypdf`
serialization round-trip for each of the 13 feature families. All 26 retained
the independent contract projection, all 26 retained the frozen comparator
classification, and there were zero extraction errors or semantic-regression
alerts.

These controls support only the tested equivalence class. They do not prove
that alternate tagging representations, reading-order changes, visual edits,
or producer-specific structures are semantically equivalent. Those candidates
were not promoted without a defensible oracle.

Evidence: `experiments/v8/V8_BENIGN_TRANSFORMATIONS.json` and
`experiments/v8/benign_transformation_cases/`; protocol:
`scripts/v8_benign_transformations.py`.
