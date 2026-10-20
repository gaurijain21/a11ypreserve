# A11yPreserve V6 final anonymity audit

Recorded 2026-10-19. The audit covers the current canonical PDF, the complete
anonymous ZIP, its nested replication-package ZIP, and generated release
manifests. It is an automated technical audit plus a human-inspection request;
it is not an author attestation.

## Results

| Check | Result | Evidence |
|---|---|---|
| Visible author identity in manuscript | PASS | `main.tex` uses `Anonymous for review`; no author block or acknowledgments |
| PDF metadata identity | PASS | Current PDF metadata was checked by the V6 anonymity audit; no author/institution/private path is used as a release identifier |
| PDF page/layout scan | PASS | All ten pages rendered under `submission/ICST2027_V6/.pdf-qa/v7-adversarial/` and inspected |
| Outer ZIP integrity | PASS | `scripts/verify_v6_upload_bundle.py`; current bundle SHA is recorded in the release manifest |
| Nested replication ZIP integrity | PASS | Bundle verifier checks nested package and hashes |
| Package identity scan | PASS with narrow detector exception | No identity-bearing root metadata is included; detector source contains literal patterns used to test for leaks |
| Absolute paths, synchronized-storage names, account IDs | PASS for packaged evidence | Sanitizer rewrites local paths and known account strings; archive verifier found no live private path |
| Credentials, tokens, cookies, browser profiles, private account data | PASS | Archive contents and filenames contain no credential/browser-state artifacts |
| Git metadata and remotes | PASS for package | `.git` and repository metadata are not packaged |
| Temporary/cache/OS files | PASS | Builder excludes cache, profiles, `__pycache__`, lock/binary/compiler intermediates, logs, and PDF-QA output |
| Historical evidence | PASS as intentional evidence | Historical V4/V5 records are retained under sanitized evidence paths; backup PDFs and build caches are excluded from the upload candidate |
| Hidden author identifiers in filenames | PASS | Package filenames are fixture/report/source names only |

## Scope and exception

The repository-level anonymity scanner intentionally contains strings such as
the local user name, a repository-owner pattern, and an author-only marker so that
it can detect those strings. That scanner source is not evidence of a leak;
the independent archive verifier scans the actual ZIP payload and passed. The
root `CITATION.cff` and placeholder `LICENSE` are omitted from the anonymous
candidate because their current contents require author-controlled decisions.

## Human final check

Before HotCRP upload, an author must open the exact ZIP and inspect HotCRP's
paper metadata, author fields, conflict fields, supplementary links, and any
automatically generated filename or account identifier. This is required even
though the automated archive checks pass.
