# READY TO TARGET ICST 2027

Verified against official venue pages on 2026-09-29.

## 1. Recommended primary venue

IEEE International Conference on Software Testing, Verification and Validation (ICST 2027), Research Papers track.

## 2. Official venue scope evidence

The official ICST 2027 research-track page lists empirical studies, replication/case studies, testing tools, and testing of non-functional properties including accessibility among its topics. A11yPreserve's contribution is a source-grounded, contract-based preservation test protocol with evidence provenance and an empirical application to DOCX-to-PDF conversion. See the [official ICST research-track page](https://conf.researchr.org/track/icst-2027/icst-2027-research-papers).

## 3. Current deadline/status

The official page lists Nov 2, 2026 for the research paper, with deadlines in AoE (UTC-12). The track is currently actionable as of 2026-09-29. The listed notification dates are Dec 22, 2026, Jan 31, 2027 for major revision, Feb 20, 2027 for final notification, and Mar 18, 2027 for camera ready.

## 4. Paper type / track

Research Papers track. The paper is an empirical testing-methodology study, not an artifact-only submission or an agentic-AI paper.

## 5. Page limit

The official track page states 10 pages including text, figures, tables, and appendices, plus up to 2 additional pages for references. The current ICST-formatted copy is 9 pages total, including references.

## 6. Anonymity policy

The track uses double-blind review. The paper copy has an anonymous author block, a neutral IEEE AI disclosure with no identity-linked acknowledgment, no identifying URLs, and no local paths. The artifact candidate is also sanitized and anonymous. See `submission/ICST2027/ANONYMIZATION_REPORT.md` and the ICST AI disclosure checks.

## 7. Artifact policy

The official track instructions expect an anonymized replication package when applicable, or an explanation when material cannot be provided. The candidate artifact supplies contracts, frozen fixtures and outputs, evidence, analysis code, tests, result files, README instructions, and reproducibility levels. It contains no authentication state. The final public license and author metadata remain human decisions.

## 8. Why A11yPreserve fits

The method is directly expressible as software testing: source contracts are test oracles, destination extraction is an observation layer, differential comparison is the test relation, and uncertainty statuses prevent unsupported failure claims. The paper distinguishes preservation from destination-only accessibility evaluation, remediation, PDF-to-HTML conversion, and user studies. Its controlled corpus and secondary integrated sanity check are reported as bounded evidence rather than prevalence.

## 9. Main reviewer risk at this venue

The likely rejection argument is limited breadth: 13 atomic fixtures, two real pipelines, one cloud backend that cannot be fully pinned, no mutation corpus, and no disabled-user study. This is not fatal for the stated protocol contribution, but reviewers may require stronger justification. The manuscript now makes the limitation explicit, keeps counts descriptive, preserves unresolved equivalence, and avoids product or ecosystem claims.

## 10. Changes made for venue

The canonical manuscript received only the two final wording repairs and was frozen. The separate ICST copy changes document class, layout, anonymous author block, and taxonomy formatting for readability. The artifact copy sanitizes publication paths and adds README, requirements, citation metadata, and a license-status report. No frozen research evidence or scientific count changed.

## 11. Current manuscript page count

The historical canonical build record reports 10 pages, but `paper/main.pdf` is not present in the current checkout. The verified ICST submission copy is 9 pages; its current hash is recorded in `submission/ICST2027/BUILD_RECORD.md` and `SUBMISSION_FREEZE.md`.

## 12. Artifact readiness

The candidate artifact is structurally ready for anonymous review and has passed fresh source-oracle, OOXML, calibration, comparator, JSON, path, and binary scans. The packaged archive is `submission/A11yPreserve_artifact_ICST2027.zip` with SHA-256 `EE343279DC86F9991D3C378D0676D17B2B8DF05545C40561B92FC81E0400E39D`. It is not yet ready for public release because the final license and author metadata are not selected.

## 13. Backup venue

ACM DocEng, next cycle. Its [2026 call](https://doceng.org/doceng2026/cfp) is the strongest topical match for document transformation and accessibility preservation, but its current cycle is closed and the next CFP is not yet published. ACM ASSETS is a later-cycle alternative with excellent accessibility fit but greater likely pressure for representative-user validation; see `submission/VENUE_COMPARISON.md`.

## 14. Remaining human actions

Recheck the official ICST page, insert author metadata only in the submission copy, choose the artifact license, inspect the final anonymized PDF and package, and complete the HotCRP upload/review steps. The canonical `paper/main.pdf` is not present in the current checkout; the verified venue-formatted PDF is `submission/ICST2027/main.pdf` and is the package candidate. Do not submit from this workspace automatically.

## 15. Recommendation

Target ICST 2027 if the researcher accepts the bounded-methodology positioning and the small controlled evaluation. Keep DocEng as the next-cycle venue if the priority is maximal document-engineering topical fit. The project is ready for the human-controlled submission step, not for automatic submission or public release.
