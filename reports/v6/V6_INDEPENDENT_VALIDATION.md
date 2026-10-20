# V6 independent validation audit

The V5 diagnostic cross-check examined 26 cases and reported 8 agreements and 18 disagreements. V6 preserves the frozen comparator and does not relabel these disagreements as external correctness evidence.

## Disagreement investigation

The 18 disagreements fall into the following evidence-based classes:

| Class | Cases | Stored disagreement rows |
|---|---:|---|
| Missing feature-specific value/association logic | 10 | LibreOffice:F02_A, LibreOffice:F07_A, LibreOffice:F08_A, Google Docs:F01_A, Google Docs:F03_A, Google Docs:F05_A, Google Docs:F06_A, Google Docs:F07_A, Google Docs:F08_A, Google Docs:F09_A |
| Alternate representation not supported | 5 | LibreOffice:F10_A, LibreOffice:F12_A, LibreOffice:F13_A, Google Docs:F10_A, Google Docs:F13_A |
| Extraction limitation or conservative abstention | 3 | LibreOffice:F11_A, Google Docs:F11_A, Google Docs:F12_A |
| Genuine implementation defect | 0 established | No defect was established from the stored cross-check alone; no relabeling was performed. |

The first category covers exact-value or relation logic absent from the lightweight implementation; the second covers alternate structural representations; the third covers cases where marker/text extraction cannot establish the required association or expression. These are audit categories, not new ground-truth labels.

The exact row-level evidence remains in `experiments/v5/independent_oracle_validation.json`. The second implementation is an independent diagnostic implementation, not an external expert panel and not a human usability study.

## Corrective decision

No corrected comparator is claimed in V6 because the disagreement audit did not establish a specific frozen-comparator defect. If a future expert adjudication identifies one, it must receive a new comparator version and a complete affected-row rerun; the frozen V4 comparator remains preserved.
