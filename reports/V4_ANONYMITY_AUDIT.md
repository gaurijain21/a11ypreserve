# V4 Anonymity Audit

## Scope

This audit covers the manuscript source and the final artifact directory, not the repository's historical development logs.

## Checks

- Manuscript author is `Anonymous Submission`.
- The manuscript contains no personal author name, email address, affiliation, ORCID, local Windows username, OneDrive URL, or authenticated Google account identifier.
- The final artifact README contains no credentials, cookies, browser profile data, or personal account identifiers.
- Conversion manifests retain scientific provenance fields but are not part of the anonymous manuscript submission package unless the venue permits supplementary provenance disclosure.
- Public candidate URLs in `reports/V4_EXTERNAL_CORPUS_REPORT.md` are research-provenance links only; no external document was copied into the artifact package.

## Residual limitation

Repository history and machine-local metadata can contain operational identifiers outside the manuscript package. Before venue upload, submit the contents of `submission/ICST2027_V4/final/` after the local TeX build, not the full working repository, and inspect the venue's supplementary-material policy.

## Result

**PASS for the prepared manuscript/artifact surface, with the submission-packaging limitation above.**
