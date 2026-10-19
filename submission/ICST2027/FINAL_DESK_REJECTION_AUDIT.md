# Final desk-rejection audit

Audit date: 2026-09-29

Target: ICST 2027 Research Papers track, frozen V2 candidate.

| Check | Status | Evidence / remaining action |
|---|---|---|
| Correct venue and track | PASS | Current official ICST 2027 Research Papers CFP identifies this as the full research-paper track. |
| IEEE conference format | PASS | PDF is two-column letter format with IEEEtran styling. |
| Page limit | PASS | 9 pages total; current CFP permits up to 10 pages including content, with up to 2 additional reference-only pages. |
| PDF integrity and layout | PASS | PDF parses and renders cleanly; all 9 pages visually inspected. |
| Anonymous author block | PASS | PDF says `Anonymous for review`; no author, affiliation, email, repository, or personal URL markers found. |
| Anonymous artifact | PASS | Frozen ZIP contains no author identity, browser state, credentials, Git metadata, or local-path leak. |
| AI disclosure | PASS | Anonymous acknowledgment names ChatGPT and Codex, describes the assistance, and excludes experimental ground truth, independent human validation, and autonomous adjudication. |
| References and citations | PASS | 13 citation keys match 13 unique bibliography entries; no missing or duplicate keys; no placeholders or undefined-reference markers found. |
| Required V2 numerical results | PASS | 13 fixtures, 26 primary cases, final six-category distribution, and separate 3-document/21-of-21/42 sanity check match the frozen records. |
| V3 exclusion | PASS | No Variant B, 52-case, or Google three-run repeatability material appears in the V2 submission source or artifact ZIP. The only `v3` text in the paper is the cited EN 301 549 version identifier. |
| Exact paper hash | PASS | SHA-256 matches the recorded frozen value. |
| Exact artifact hash | PASS | SHA-256 matches the recorded frozen value. |
| Paper–artifact consistency | PASS | See `FINAL_CLAIM_ARTIFACT_TRACE.md`. |
| Originality and concurrent-submission declarations | HUMAN CHECK | Researcher must complete the portal declarations and confirm no conflicting submission. |
| Portal-rendered PDF and metadata | HUMAN CHECK | Researcher must inspect the PDF generated/served by HotCRP after upload and confirm author metadata is entered only where appropriate. |

## Result

There are zero known technical or formatting desk-rejection issues in the frozen upload pair. The remaining items are ordinary researcher-controlled portal declarations and the final portal-rendered-PDF inspection; they are not changes to the science or upload files.

Official CFP checked: https://conf.researchr.org/track/icst-2027/icst-2027-research-papers
