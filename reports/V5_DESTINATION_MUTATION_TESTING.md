# V5 destination-side mutation testing

The V4 `39/39` result tested source-oracle sensitivity only. V5 adds a
destination-side harness at `experiments/v5/destination_mutation_testing.py`
and records every attempted mutant in
`experiments/v5/destination_mutation_manifest.json`.

The harness starts from all 65 tagged LibreOffice atomic PDFs, applies one
family-specific structure/value mutation per variant where possible (heading
role, `/Alt`, list role, TH/TD, `/Lang`, decorative Artifact/Figure state,
URI, title, Note, Formula, or Caption), verifies parseability, runs the
destination extractor/comparator, and records detected, surviving, invalid,
and measurement-error outcomes. A mutation is detected when the mutated
classification differs from the baseline classification. This is a
classification-level fault-sensitivity criterion, not a universal mutation
score.

The expanded run attempted 65 mutants. Fifty-nine were valid, 46 were
detected, 13 survived without a classification change, six were unsupported
(including five decorative-image cases without an Artifact node and one link
case without a URI), and two valid footnote mutants remained measurement
errors. The same run records 65 no-op controls; all retained their baseline
classification and none was a false positive. Surviving mutants are retained
as evidence of comparator blind spots, not relabeled as detections.

Invalid/unsupported operators remain recorded and are excluded from the valid
mutant detection rate. No V4 classification is changed.
