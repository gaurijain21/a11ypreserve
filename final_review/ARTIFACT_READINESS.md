# Artifact Readiness

## Classification: MINOR FIXES

## Safe to release after sanitization

- Frozen DOCX fixtures and machine-readable manifests.
- Frozen corpus manifest and hash records.
- Source and destination extraction code.
- `a11ydiff` comparison code and regression tests.
- Conversion scripts that do not embed credentials.
- Sanitized automation logs, validation reports, and evidence records.
- Manuscript source and bibliography.

## Must not be released as-is

- Authenticated Google Docs browser state, cookies, tokens, or account artifacts if present outside the tracked evidence tree.
- Raw logs and JSON containing personal absolute paths such as `C:\Users\iamga`.
- Local MiKTeX build logs and rendered scratch directories unless paths are generalized.
- Any private cloud document identifiers or account-specific metadata.

## Licensing and provenance

The project should document licenses for code and any included images before public release. The frozen fixtures appear project-generated, but each embedded image and dependency should be checked explicitly. External PDFs or web pages should be referenced by URL rather than redistributed without permission.

The artifact is scientifically ready but needs a release-sanitization pass before public upload. No credentials were found by the repository scan, but absence of a match is not a substitute for checking the final release archive.
