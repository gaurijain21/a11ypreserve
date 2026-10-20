# V6 ICST 2027 submission readiness

## Venue requirements checked

The official ICST 2027 Research Papers page was checked on 2026-10-18: <https://conf.researchr.org/track/icst-2027/icst-2027-research-papers>.

| Requirement | Current evidence | Status |
|---|---|---|
| Two-column IEEE conference format, letter template | `submission/ICST2027_V6/main.pdf`; `pdfinfo` reports 612 x 792 pt | PASS |
| Maximum 10 pages including text, tables, figures, appendices | V6 PDF has 9 pages | PASS |
| Up to two additional reference-only pages | Not needed; references are within the 9-page PDF | PASS |
| Double-anonymous review | `Anonymous for review`; no author/institution metadata in V6 manuscript; independent upload-bundle scan passes | PASS pending human inspection of final upload archive |
| Anonymized artifacts/replication package | Anonymous candidate built and independently verified; root `CITATION.cff` and placeholder `LICENSE` omitted | HUMAN DECISION |
| Replication information and instructions | V6 reports, per-case traces, scripts, manifest, provenance, and README instructions are present | PASS with environment limits |
| Generative-AI disclosure | Manuscript identifies OpenAI ChatGPT and Codex, affected sections/code, and does not claim completed human verification | PASS pending author confirmation |
| Reference integrity | Fresh 9-page rebuild has no unresolved citation/reference diagnostics; source contains 13 cited entries and no unused entries | HUMAN VERIFICATION REQUIRED for metadata and claim support |

## Scientific readiness

The reproducible V6 chain passes with 65/65 fresh controls, 59 valid applied mutants, 46/59 classification detections, 59/59 additive evidence-drift alerts, 10 semantically meaningful survivors, 130 primary baseline cases, 26 holdout fixtures (52 observations), 78 non-holdout observations, and the unchanged 65-observation Word supplement. V4/V5 denominators and historical artifacts remain preserved. See `V6_MASTER_AUDIT.md`, `V6_OBJECTION_MITIGATIONS.md`, and `V6_REPRODUCIBILITY_REPORT.md`.

## Remaining human decisions before HotCRP upload

1. Verify all references and claim support manually, as required by the ICST GenAI policy.
2. Decide whether the anonymous replication archive excludes or sanitizes root `CITATION.cff`, whose placeholder repository URL may identify the authors.
3. Choose licenses and complete `LICENSE`/`CITATION.cff` only for the appropriate release stage; no license is inferred by V6.
4. Inspect the final uploaded ZIP for author names, institutions, private paths, credentials, browser state, and repository metadata.
5. Complete HotCRP authorship, conflict-of-interest, originality, simultaneous-submission, and artifact-access declarations.
6. The historical repeatability manifest's `NOT_RUN` status remains unchanged; the separate V6 interpretation is recorded in `V6_REPEATABILITY_METADATA.md` and does not claim temporal Google repeatability.
7. Keep `main_pre_rebuild.pdf` out of any upload; the current canonical `main.pdf` and the anonymous candidate now use the verified fresh build.

## Reviewer-facing verdict

**GO WITH LIMITATIONS.** The artifact is technically submission-ready after the human checks above, but the evidence supports a bounded source-grounded preservation-testing contribution—not PDF/UA conformance, human usability, natural-document generalization, causal localization inside Google Docs, or universal converter ranking.
