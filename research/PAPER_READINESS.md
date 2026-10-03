# READY TO WRITE PAPER

## Frozen corpus

13 controlled DOCX fixtures are frozen, hash-verified, and independently checked through manifest, raw OOXML, and source-extractor agreement.

## Frozen experiment

26 genuine DOCX-to-PDF outputs are frozen: 13 LibreOffice and 13 Google Docs. All are parseable, non-empty, tagged, and validated. Microsoft Word is explicitly excluded from the denominator.

## Final outcome counts

11 PRESERVED, 9 PARTIALLY_PRESERVED, 3 ALTERED, 2 LOST, and 1 MEASUREMENT_ERROR. There are 25 classifiable/determined outcomes after excluding the measurement error.

## Confirmed LOST cases

F06 / Google Docs / inline language and F11 / Google Docs / footnote association are independently confirmed lost under their frozen contracts.

## Measurement error

F11 / LibreOffice remains a measurement error because `/Note` structure is present but the current extraction evidence cannot resolve note-body association.

## Final RQs

RQ1: extent of preservation; RQ2: property-level preserved/partial/altered/lost outcomes; RQ3: differences between the tested LibreOffice and Google Docs pipelines. Validator comparison is future work.

## Final contribution statements

The paper can claim a source-grounded preservation method, a verified 13-fixture DOCX benchmark, a11ydiff with provenance-traceable comparison, and a scoped 26-output empirical study.

## Novelty statement

The defensible gap is narrow: measuring whether known source accessibility information survives specific DOCX-to-PDF pipelines. The project does not claim to be the first accessibility-conversion benchmark, tagging system, or validator.

## Main limitations

Single instances per feature family, synthetic atomic fixtures, two pipelines, cloud-version dependence, PDF representation/parser ambiguity, unequal feature complexity, and no disabled-user study.

## Validator role

FUTURE WORK. Validator evidence is incomplete and is not part of the core RQs.

## Claims supported

The tested pipelines did not uniformly preserve source accessibility information; outcomes varied by feature and pipeline; tagged destination output did not fully characterize source-information fidelity; and source-grounded comparison was technically feasible.

## Claims prohibited

No general converter ranking, population-wide generalization, universal claim about Google Docs or LibreOffice, universal user-impact claim, complete accessibility-checker claim, or attribution of every Google result to PDF export alone.

## Remaining documentation issues

No blocking issues remain for paper writing. Future experiment freezes should record a test-results hash in addition to source/output/classification hashes. The manuscript should preserve feature-level reporting and the end-to-end Google pipeline wording.

## Final recommendation

The project is ready to write the paper. Do not modify frozen experiment evidence or launch additional experiments as a prerequisite for manuscript drafting.
