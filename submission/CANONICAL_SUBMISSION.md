# A11yPreserve canonical submission files

This manifest identifies the files intended for submission from the current
working tree. Historical files remain in place for provenance but are not
submission alternatives.

## Upload files

- Manuscript PDF: `submission/ICST2027_V3/main.pdf`
  - SHA-256: `4F4CC53B5783ADEECF418B645EDDC16D39A7CD17144B8CD2A76D6A32D8B46285`
  - Pages: 9
- Reviewer artifact ZIP: `submission/A11yPreserve_artifact_ICST2027_V3.zip`
  - SHA-256: `C0F0326DBF40E169BD6A0E101B27F486EB001F5A04518E2AF68B5890528D4908`
  - Contents: 342 files under the sanitized `artifact_v3/` boundary

## Canonical source and evidence

- Manuscript source: `submission/ICST2027_V3/main.tex`
- Bibliography: `submission/ICST2027_V3/references.bib`
- Artifact directory: `artifact_v3/`
- Primary result dataset: `artifact_v3/results/V3_PRIMARY_RESULTS.json`

The result-dataset filename and some internal artifact paths retain historical
development labels for provenance. They do not identify separate reviewer-
facing research versions. The frozen primary result record remains the source
of the 52-case baseline; additive analyses are documented separately.

## Historical files — do not upload

- `submission/ICST2027/main.pdf` is an older manuscript build.
- `submission/A11yPreserve_artifact_ICST2027.zip` is an older, smaller artifact
  package.

## Repository state

- Branch: `master`
- Remote: none configured
- The final semantic-measurement audit and its aligned manuscript/artifact
  records are committed locally. No remote publication is configured or
  performed.
