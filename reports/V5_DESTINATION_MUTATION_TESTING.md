# V5 destination-side mutation testing

The V4 `39/39` result tested source-oracle sensitivity only. V5 adds a
destination-side harness at `experiments/v5/destination_mutation_testing.py`
and records every attempted mutant in
`experiments/v5/destination_mutation_manifest.json`.

The harness starts from known tagged LibreOffice PDFs, applies one targeted
structure mutation where possible (heading role, `/Alt`, list role, TH/TD,
`/Lang`, decorative Artifact/Figure state, URI, title, Note, Formula, or
Caption), verifies parseability, runs the destination extractor/comparator,
and records detected, surviving, invalid, and measurement-error outcomes. A
mutation is detected only when the resulting classification is no longer
`VERIFIED_PRESERVED`; this is a conservative end-to-end fault-sensitivity
criterion, not a universal mutation score.

Invalid/unsupported operators remain recorded and are excluded from the valid
mutant detection rate. No V4 classification is changed.
