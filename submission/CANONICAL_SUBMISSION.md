# A11yPreserve canonical submission files

This manifest identifies the files intended for submission from the current
working tree. Historical files remain in place for provenance but are not
submission alternatives.

## Upload files

- Manuscript PDF: `submission/ICST2027_V3/main.pdf`
  - SHA-256: `CAE94FA084B653F7CECA21435D6F39F4D71B1BC0324F4BC2F8B15F4C1CEE084C`
  - Pages: 9
- Reviewer artifact ZIP: `submission/A11yPreserve_artifact_ICST2027_V3.zip`
  - SHA-256: `B315C204C2E112909498B12D17F69B582ACA8813E8A9E42CC1E0E37D1EF08F49`
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

- Current commit at audit start: `7043a2164dce6ef162aeed7655d90c3e92bbbb68`
- Branch: `master`
- Remote: none configured
- The worktree is intentionally dirty because the final manuscript wording,
  artifact documentation, strengthening analyses, and audit records are local
  changes. No remote publication is configured or performed.
