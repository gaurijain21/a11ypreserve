# DO NOT SUBMIT CURRENT CLAIMS

## V2 integrity

The frozen V2 integrity record remains matched for the corpus manifest, primary result freeze, evidence-aware result freeze, ICST PDF, and ICST bibliography. No V2 fixture, PDF, manifest, or result file was modified.

## Google Variant completion

13/13 Variant B Google PDFs exist, are non-empty, parseable, tagged, hashed, and recorded. The visible Google Docs download action did not register after retries; the authenticated in-session Google export backend was used and disclosed in the conversion report. This is a workflow-provenance caveat, not fabricated evidence.

## V3 atomic benchmark

26 fixtures / 52 cases are frozen in `results/V3_PRIMARY_RESULTS.json` and `.md`. Counts are 18 verified preserved, 4 observed partial, 7 altered, 4 confirmed lost, 18 unresolved equivalence, and 1 measurement error.

## Within-feature consistency

The feature matrix is complete. It reports exact consistency for several feature/pipeline pairs and fixture sensitivity or unresolved equivalence where the evidence does not support stronger claims.

## F06 status

Core and Variant B Google inline-language rows are confirmed lost at the machine-verifiable structure-contract level. The dedicated two-path audit found no required inline language representation or serialized language marker; visible text remains.

## F11 status

Core and Variant B Google footnote rows are confirmed lost at the machine-verifiable association-contract level. Core LibreOffice remains the frozen measurement error; Variant B LibreOffice remains unresolved because the available evidence does not establish complete reference/body mapping.

## Google repeatability

Classification stable 13/13. Run 1, Run 2, and Run 3 PDFs were byte-identical for all 13 Core fixtures under the recorded workflow. This does not pin future cloud behavior.

## Calibration

The final calibration record is 12 correct determinate, 6 safe abstentions, 0 false positives, 2 false negatives, and 7 unresolved/indeterminate controls. False-negative impact was checked; it affects link and complex-table rows that remain unresolved and does not invalidate F06/F11.

## False-negative impact

No false negative targets either confirmed-loss family. The impact report is `final_methodology/CALIBRATION_FALSE_NEGATIVE_IMPACT_FINAL.md`.

## Classification reproducibility

The stored Core evidence reclassification reproduced 26/26 labels with the classification field hidden. This is decision-procedure reproducibility, not independent external adjudication.

## Oracle validity

The separately implemented raw-OOXML oracle passed 13/13 Core and 13/13 Variant B source contracts. It is same-team code, not external expert validation. Source ground truth remains manifest + raw OOXML + source-extractor agreement.

## Adequacy boundary

The suite has two controlled instances per 13 selected families, not comprehensive standards coverage. Selection is purposive and measurability-biased; F13 reading order was deferred because reliable automated equivalence could not be established.

## Measurability bias

The benchmark selects properties with inspectable source/destination representations. Unresolved equivalence is retained when the representation cannot be safely mapped.

## Fresh-environment reproduction

The prior fresh-environment dependency install remains constrained by the environment. Existing-evidence verification and local LibreOffice reproduction are documented; Google reproduction is workflow-repeatable but backend-version dependent.

## Prior-art overlap

The manuscript now positions DocAccessible, DAISY, Roig/Ribera, Kumar et al., iTagPDF, and SciA11y as adjacent prior work. The surviving claim is a controlled, source-grounded, contract-based, uncertainty-aware preservation conformance protocol—not a first or unique system.

## ICST testing relevance

The V3 copy explicitly maps contracts to test oracles, fixtures to test inputs, pipelines to systems under test, destination extraction to observations, and unresolved equivalence to conservative oracle abstention. A reviewer may still judge the contribution too domain-specific, but the software-testing framing is now explicit.

## Top remaining weaknesses

1. Novelty and significance may still be judged incremental for ICST.
2. Cross-format oracle coverage is incomplete, reflected by 18 unresolved atomic rows.
3. The corpus is controlled and purposive, not representative.
4. Variant B Google provenance includes the documented export-backend recovery route.
5. The separate V3 manuscript copy has not produced a verified final PDF in this environment: MiKTeX cannot initialize writable configuration, and the built-in compiler reports missing standard directories.

## Any fatal issue?

No fatal scientific issue was found. The current blocker is package verification: the V3 ICST PDF cannot be compiled and visually inspected in this environment. This prevents a clean submission recommendation for the V3 claims, but does not require a new experiment.

## Any new experiment required?

No. The V3 evidence is complete for the requested scope. A working IEEE/LaTeX compilation environment and final visual/anonymity check are required before submission.

## Which manuscript version should be submitted?

Do not submit the uncompiled V3 copy. The already compiled V2 ICST package remains the safer submission candidate until the V3 copy is compiled and visually verified. If a working TeX environment becomes available, use `submission/ICST2027_V3/main.tex` and its separate V3 reports, subject to the final PDF and anonymity checks.

## Exact final human actions

1. Compile `submission/ICST2027_V3/main.tex` in a working IEEEtran environment.
2. Inspect every rendered V3 page, table, bibliography, and PDF metadata.
3. Re-run the final anonymity scan on the V3 submission copy and artifact.
4. Decide whether to retain the already compiled V2 candidate or replace it with the verified V3 copy.
5. Do not submit until that choice is made manually.

## Final recommendation

The V3 science survives hostile review with bounded claims, but the V3 package is not yet submission-ready because its final PDF is unverified. Retain V2 as the currently submit-able artifact and treat V3 as ready for targeting after compilation and visual QA.
