# V6 human release audit

Recorded 2026-10-19. This is a release-preparation audit, not a HotCRP submission
and not an author approval.

## Completed release work

- The V6 manuscript was compiled from the current source to the alternate job
  name `v6_rebuild` using MiKTeX pdfTeX 25.12 and BibTeX 0.99e. The final build
  is 9 pages on US letter paper and has no unresolved reference or citation
  diagnostics in the final rebuild log.
- The current source contains 13 cited bibliography entries and no unused
  bibliography entries. Citation keys resolve structurally.
- Every page of the 9-page PDF was rendered to PNG and visually inspected for
  clipping, overlap, unreadable tables, broken references, and anonymity. No
  visual defect was found. IEEE two-column layout and the 10-page limit pass.
- An anonymous upload candidate was built at
  `submission/ICST2027_V6/ICST2027_V6_anonymous_upload.zip`. It contains the
  current canonical paper, the sanitized V5 historical package, V6
  evidence, reports, scripts, and reproduction instructions (1,136 packaged
  files). The independent verifier passes and checks the archive contents and
  hashes rather than trusting its manifest. The paper payload hash is
  `d929515580ca814c9b0d9a4be1906eae58108651a4982be3ce6011c456ef5617`.
- Root `CITATION.cff` and placeholder `LICENSE` are intentionally omitted from
  the anonymous candidate because they contain unresolved human decisions.

## Current release artifact state

The fresh build is now the canonical
`submission/ICST2027_V6/main.pdf` with 9 pages and SHA-256
`d929515580ca814c9b0d9a4be1906eae58108651a4982be3ce6011c456ef5617`.
The previous timestamped PDF was preserved as `main_pre_rebuild.pdf` and is
not included in the anonymous upload bundle. The provenance record now points
to the canonical current PDF and its successful alternate-jobname build log.

## Human decisions still required

1. Verify every reference's metadata and claim support against the cited
   source; structural citation checks are not semantic verification.
2. Inspect the exact final ZIP and HotCRP metadata for author names,
   institutions, repository URLs, private paths, credentials, cookies, and
   account identifiers.
3. Complete authorship, conflicts, originality, simultaneous-submission, and
   artifact-access declarations.
4. Select the public license and resolve `LICENSE`/`CITATION.cff` after the
   anonymous review stage; no legal choice is inferred here.
5. Confirm the AI disclosure and complete human verification of references,
   code, results, and final claims.
6. The historically retained repeatability `NOT_RUN` record is preserved, and
   the separate V6 interpretation is now in `V6_REPEATABILITY_METADATA.md`.
   Historical records must not be rewritten.
7. The additive V6 evidence-drift layer flags 59/59 valid applied mutants while
   retaining the frozen 46/59 coarse detections and ten meaningful survivors.
   The blinded adjudication protocol is prepared but awaits authorized human
   reviewers.

## Not claimed

No submission, upload, author decision, legal decision, external adjudication,
human-usability result, natural-document validation, PDF/UA conformance result,
or authenticated temporal Google Docs repeatability run was performed here.
