# NO-GO

## Primary V4 experiment
- feature families: 13
- variants: 5 per feature
- fixtures: 65
- converters: 0 successfully established
- primary cases: 0

## Calibration
- controls: 78
- correct determinate: 60
- false positives: 0
- false negatives: 5
- correct unresolved: 13
- other unresolved: 0 unsupported confident classifications

## Holdout
- size: 26
- results: not run; outputs were not available
- unexpected failures: not applicable

## Realistic corpus
- documents: 10
- external: 0
- project-created: 10
- property observations: 78

## Repeatability
- runs: 0
- classification consistency: not run
- byte identity where relevant: not run

## Reading order
- excluded
- justification: a defensible bounded oracle did not pass calibration before conversion.

## Word
- unavailable for V4
- evidence: Word COM `DispatchEx` failed before conversion with `0x80070520`; no output was fabricated.

## Unresolved cases
- total: not applicable because primary conversion cases are zero
- reason categories: not applicable; no conversion evidence exists to classify.

## Novelty

A11yPreserve’s strongest defensible contribution is a prospective source-grounded preservation-testing protocol that combines known DOCX semantics, contract-level source truth, raw-OOXML checking, identical inputs across converter conditions, destination structure evidence, calibrated equivalence mapping, conservative abstention, and provenance certificates. It asks whether a particular author-supplied semantic known to exist before transformation survived the transformation, which is a different question from destination-only accessibility checking.

## Remaining reviewer attacks

The central blocker is the absence of V4 converter outputs. Additional limitations are the project-created realistic corpus, no reading-order extension, five comparator false negatives in calibration, no Word/Google V4 arm, no validator comparison, and no user study. These are disclosed rather than converted into claims.

## Submission blockers

- Establish at least one legitimate V4 converter pipeline and run all 65 fixtures under the frozen protocol.
- Preserve output hashes, extraction evidence, classifications, unresolved causes, and repeatability records.
- Only then create a V4 manuscript; V3 remains the only manuscript with conversion results.

Source validation status: PASS (65/65 raw-oracle and 65/65 primary-extractor supported).
Mutation status: PASS (39/39).
Converter inventory: 0 established.
