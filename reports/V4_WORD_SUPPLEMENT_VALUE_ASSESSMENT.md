# V4 Microsoft Word supplementary-arm value assessment

Date: 2026-10-05

## Scope

Microsoft Word desktop was recovered after the prospectively frozen LibreOffice
+ Google Docs V4 primary experiment. It is therefore evaluated as a supplementary
third pipeline and does not change the frozen 130-case primary denominator.

## Evidence completed

- 65/65 atomic Word GUI PDFs were valid, parseable, nonzero, and structurally
  tagged.
- 10/10 project-created realistic-document Word PDFs were valid and tagged.
- The frozen source extractor/comparator boundary was applied without changing
  the comparator, taxonomy, contracts, fixtures, or holdout membership.
- Six pre-specified difficult variants were each exported three times.

## Word atomic supplementary results

| Classification | Count |
|---|---:|
| VERIFIED_PRESERVED | 16 |
| OBSERVED_PARTIAL | 26 |
| ALTERED | 16 |
| CONFIRMED_LOST | 2 |
| UNRESOLVED_EQUIVALENCE | 0 |
| MEASUREMENT_ERROR | 5 |
| Total | 65 |

Holdout subset: 6 VERIFIED_PRESERVED, 11 OBSERVED_PARTIAL, 6 ALTERED,
1 CONFIRMED_LOST, 0 unresolved, and 2 measurement errors (26 cases).

The realistic arm contains 78 property-contract observations: 23 VERIFIED_PRESERVED,
25 OBSERVED_PARTIAL, 25 ALTERED, 0 CONFIRMED_LOST, 0 unresolved, and 5
measurement errors. These are separate from the 65-case atomic denominator.

## Repeatability

The six pre-specified variants were exported three times each (18 outputs).
All six had stable normalized destination extraction, stable normalized secondary
evidence, and stable frozen classifications (6/6). The PDFs were not byte
identical (0/6 byte-identical fixtures); Word output metadata/object serialization
varied while the normalized semantic evidence and classifications remained stable.

## Scientific recommendation

Word materially strengthens converter coverage and is suitable for a separate
supplementary-results paragraph or artifact report. It should not replace or
retroactively expand the prospectively frozen primary benchmark from 130 cases to
195 cases. The manuscript should only be edited to mention the arm if page space
and the submission protocol permit a transparent post-freeze supplementary result;
the primary claims and denominators must remain unchanged.

## Artifacts

- `experiments/v4/word_supplement/WORD_SUPPLEMENT_PROTOCOL.md`
- `experiments/v4/conversions/word/manifest.json`
- `experiments/v4/conversions/word/repeatability_manifest.json`
- `experiments/v4/conversions/word/analysis/V4_WORD_ANALYSIS.json`
- `experiments/v4/conversions/word/analysis/V4_WORD_REPEATABILITY_ANALYSIS.json`
- `reports/V4_WORD_GUI_RECOVERY_RESULT.md`
