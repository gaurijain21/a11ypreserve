# Pre-limitation-resolution freeze

This record freezes the audited submission-ready state before any new
limitation-resolution experiment. The commit below is the guaranteed fallback;
all later work must be additive and must not rewrite the frozen primary evidence.

## Baseline commit

- Stage 1 submission-ready commit: `d361f99740a86cad15e4009282f7ee9a086405a3`
- Branch: `master`
- Remote: none configured
- Worktree after the Stage 1 commit: clean

## Canonical submission hashes

- Manuscript: `submission/ICST2027_V3/main.pdf`
  - SHA-256: `4F4CC53B5783ADEECF418B645EDDC16D39A7CD17144B8CD2A76D6A32D8B46285`
  - 9 pages; 146,472 bytes
- Reviewer artifact: `submission/A11yPreserve_artifact_ICST2027_V3.zip`
  - SHA-256: `B315C204C2E112909498B12D17F69B582ACA8813E8A9E42CC1E0E37D1EF08F49`
  - 342 packaged files; 4,632,945 bytes

## Frozen primary counts

- 52 fixture--pipeline rows.
- 18 `VERIFIED_PRESERVED`.
- 4 `OBSERVED_PARTIAL`.
- 7 `ALTERED`.
- 4 `CONFIRMED_LOST`.
- 18 `UNRESOLVED_EQUIVALENCE`.
- 1 `MEASUREMENT_ERROR`.
- 26 rows each for LibreOffice and Google Docs.

## Additive counts already accepted into the baseline record

- Independent hyperlink evidence resolves 4 frozen unresolved rows.
- Derived additive analysis: 14 unresolved rows remain.
- Frozen result JSON, hashes, provenance, classifications, fixtures, and
  converter outputs are unchanged.
- Interaction source corpus: 6 fixtures and 25/25 source-contract checks.
- Microsoft Word feasibility: no-go at COM activation (`0x80070520`), zero
  generated PDFs.
- Presence-only contrast: 16 of 18 frozen unresolved rows have a feature-shaped
  destination structure.

## Limitations at the freeze

1. Only two completed DOCX-to-PDF pipelines support the primary comparison.
2. The corpus is purposive and controlled, not statistically representative.
3. Fourteen rows remain unresolved in the additive analysis.
4. Word produced no outputs, and the six new interaction fixtures have no
   converter outputs.
5. No trustworthy real-world sanity corpus was included.
6. No screen-reader or disabled-user study was performed; structural semantic
   preservation is not equivalent to end-user usability.

Any limitation-resolution result must be recorded separately and compared with
this freeze before it can affect the manuscript or reviewer artifact.
