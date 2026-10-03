# 1. Verdict

**READY — SUBMIT**

The final manuscript and sanitized artifact are internally consistent, buildable,
anonymous, and independently verified. The remaining scientific risks are real
limitations of scope and construct validity, but none invalidates the bounded
claim that A11yPreserve is a source-grounded testing protocol for selected,
machine-verifiable DOCX-to-tagged-PDF preservation contracts.

# 2. Canonical submission files

| Item | Canonical path | SHA-256 / status |
|---|---|---|
| Manuscript source | `submission/ICST2027_V3/main.tex` | canonical source |
| Manuscript PDF | `submission/ICST2027_V3/main.pdf` | `CAE94FA084B653F7CECA21435D6F39F4D71B1BC0324F4BC2F8B15F4C1CEE084C`; 9 pages; 146,413 bytes |
| Bibliography | `submission/ICST2027_V3/references.bib` | used by the canonical build |
| Primary result dataset | `artifact_v3/results/V3_PRIMARY_RESULTS.json` | 52 records; frozen evidence record |
| Artifact directory | `artifact_v3/` | self-contained reviewer boundary |
| Reviewer artifact ZIP | `submission/A11yPreserve_artifact_ICST2027_V3.zip` | `B315C204C2E112909498B12D17F69B582ACA8813E8A9E42CC1E0E37D1EF08F49`; 342 files; 4,632,945 bytes |

Current Git commit: `7043a2164dce6ef162aeed7655d90c3e92bbbb68` on `master`.
The worktree is dirty because the strengthening analyses, final manuscript,
reviewer-package documentation, and audit records are local changes. No remote
is configured. Older PDF/ZIP files remain explicitly marked historical in
`submission/CANONICAL_SUBMISSION.md` and are not upload alternatives.

# 3. Consistency status

- **Numeric consistency: PASS.** Independent recomputation gives 52 primary rows: 18 `VERIFIED_PRESERVED`, 4 `OBSERVED_PARTIAL`, 7 `ALTERED`, 4 `CONFIRMED_LOST`, 18 `UNRESOLVED_EQUIVALENCE`, and 1 `MEASUREMENT_ERROR`; 26 rows per named pipeline.
- **18 vs 14 consistency: PASS.** The manuscript now states that 18/52 is the frozen primary analysis. It separately states that an additive hyperlink-evidence audit resolves four rows, leaving 14/52 in that derived analysis, without rewriting the frozen result file or denominators.
- **Interaction-fixture wording: PASS.** The six new fixtures pass 25/25 source-contract checks, but produced no new converter outputs. The paper does not present them as additional pipeline evidence; the converted coexistence evidence remains the separate three-document, 42-observation sanity check.
- **Word wording: PASS.** Microsoft Word is described only as a deterministic feasibility attempt blocked by COM error `0x80070520`; zero PDFs were generated and Word is excluded from converter counts.
- **Baseline wording: PASS.** The presence-only contrast is explicitly weaker and reports the exact result: 16 of 18 frozen unresolved rows contain a feature-shaped destination structure. It is used to show why presence is not equivalence, not as a competing validator.
- **Oracle terminology: PASS.** The paper consistently uses source contract, specification-derived oracle, destination evidence, cross-format comparison, outcome, and abstention. Unresolved is not treated as converter failure.
- **Related-work consistency: PASS.** The paper names adjacent office-to-EPUB conversion, generic conversion-loss, PDF accessibility benchmark, destination-evaluation, and testing/oracle work, and avoids a “first accessibility-preservation study” claim.
- **Claim boundaries: PASS.** Claims are limited to selected machine-verifiable semantics, controlled fixtures, and the two completed named pipelines; no user-accessibility, population-rate, universal-converter, or screen-reader claim remains.

# 4. Strongest attempt to kill novelty

**Attack:** A reviewer can argue that A11yPreserve is merely an application of
known test-oracle, transformation-testing, accessibility-validation, and
format-conversion ideas, with office-to-EPUB work and generic conversion-loss
frameworks already establishing the important contribution.

**Does it succeed?** No, but it remains the main novelty risk. The related work
does subsume the general ideas of semantic preservation, conversion comparison,
and test oracles. It does not, on the evidence reviewed, provide the same
controlled DOCX-to-tagged-PDF fixture protocol with explicit source contracts,
accepted cross-format representations, provenance-linked case outcomes, and
conservative unresolved results. The defensible novelty is therefore the narrow
combination and empirical application, not invention of any individual testing
concept.

# 5. Strongest attempt to kill methodology

**Attack:** The source contracts are hand-authored by the same team that wrote
the comparator, so they may encode assumptions rather than ground truth. The
target PDF representation can be structurally similar but semantically
different, or equivalent but not observable through the extractors. This could
make the oracle circular.

**Does it succeed?** No, as a rejection argument, because the paper explicitly
limits the construct to machine-verifiable contract properties, validates Core
and Variant B source contracts independently through raw-OOXML checks, records
parser/calibration weaknesses, and abstains when equivalence is not established.
It does establish a meaningful construct-validity limitation: the oracle is not
external human ground truth and is not a complete accessibility semantics model.

# 6. Strongest attempt to kill the evaluation

**Attack:** Thirteen selected feature families, two controlled instances per
family, two completed pipelines, no Word outputs, no converted new interaction
fixtures, and no real-world corpus may be too little evidence for an ICST paper.

**Does it succeed?** No. It would succeed against prevalence, ecosystem-wide,
or product-ranking claims, but those claims are not made. The evaluation is
adequate for the narrower protocol question: can a fixture--pipeline case be
specified, executed, measured, and conservatively classified? The limitation is
high-value and should remain visible: the empirical result is controlled and
condition-specific rather than broad converter coverage.

# 7. Strongest attack on ICST fit

**Attack:** The work may fit ASSETS or DocEng better because the domain is PDF
accessibility, while the testing contribution is only terminology.

**Defense:** The primary unit is a fixture--pipeline test case. DOCX fixtures
are test inputs; named conversion pipelines are systems under test; source
contracts are specification-derived cross-format oracles; PDF extraction is
the observation mechanism; comparator rules produce evidence-aware outcomes;
and abstention is an explicit response to oracle uncertainty. The paper also
positions the method against oracle, metamorphic/differential, and format-
transformation testing literature, reports comparator calibration, a weak
presence baseline, repeatability, provenance, and a test-adequacy boundary.
This is software-testing research with an accessibility-document domain, not a
destination-only accessibility checker.

# 8. Strongest attack on abstention

**Attack:** Eighteen frozen unresolved cases, or 14 after the additive audit,
could be read as a weak measurement method or as selective avoidance of hard
failures. The four newly resolved hyperlink rows may appear insufficient, and
the unresolved cases could bias preservation conclusions.

The attack does not invalidate the conclusion. The frozen and additive counts
are now explicit; the 14 remaining additive abstentions are concentrated in
list-item correspondence, table associations, equations, captions, and note
mapping where the target representation is incomplete or ambiguous. The
presence-only baseline finds destination structures in 16 of the 18 frozen
unresolved rows, demonstrating why a weaker method would over-interpret
presence. The correct interpretation is reduced measurement coverage and a
bounded conclusion, not a hidden failure rate. Abstention is safer than
calling feature-shaped output equivalent without evidence.

# 9. Remaining Reviewer-2 criticisms

1. **HIGH — Pipeline breadth.** Only LibreOffice and the recorded Google Docs route completed the primary experiment; Word was blocked before conversion.
2. **HIGH — Oracle independence.** Source contracts and comparison rules are not externally adjudicated ground truth, and cross-format equivalence remains partial.
3. **MEDIUM — Measurement coverage.** Fourteen of 52 rows remain unresolved in the additive analysis, so aggregate preservation summaries must not be over-read.
4. **MEDIUM — Corpus external validity.** Fixtures are purposive and controlled; the six new interaction fixtures strengthen source-contract extensibility but add no converter observations.
5. **MEDIUM — User impact.** No screen-reader, disabled-user, or task-completion evaluation establishes end-user accessibility or harm.

# 10. Submission blockers

None.

# 11. Repairs actually made

- Added `submission/CANONICAL_SUBMISSION.md` to identify the exact upload files and mark older PDF/ZIP files historical.
- Repaired reviewer-facing artifact README terminology and clarified frozen 18 versus additive 14 without changing evidence.
- Added the exact additive-count distinction and the 16-row presence-only baseline interpretation to the manuscript.
- Updated current build/package records and stale current audit records with the rebuilt PDF and repackaged ZIP hashes.
- Rebuilt the manuscript from a clean directory and repackaged the artifact after documentation-only changes.
- Re-ran the public verifier in place and from a clean extracted ZIP; both passed. Re-ran the 17-case comparator regression, which passed 17/17.
- Re-ran the 6-document/25-contract interaction source validation, 52-row presence baseline, and four-case hyperlink geometry audit.
- Re-ran PDF compilation, log scans, metadata, font embedding, anonymity, text, and 9-page render checks.

# 12. Final paper claims

- **Research question:** To what extent do selected, machine-verifiable accessibility semantics survive, change, or become unresolvable when accessible DOCX documents pass through the tested tagged-PDF conversion pipelines?
- **Contribution:** A11yPreserve combines explicit source accessibility contracts, controlled feature-oriented DOCX inputs, specification-derived cross-format oracles, evidence-aware PDF comparison, provenance, and conservative abstention for fixture--pipeline testing.
- **Empirical conclusion:** The 52 frozen cases show mixed, feature- and pipeline-specific outcomes: 18 verified preserved, 4 partial, 7 altered, 4 confirmed lost, 18 unresolved, and 1 measurement error. The additive hyperlink audit improves measurement coverage by four rows but does not replace the frozen primary result.
- **Narrow novelty statement:** A11yPreserve provides a bounded contract-based testing protocol for measuring selected accessibility-semantic preservation from DOCX to tagged PDF across named real conversion pipelines. Its distinctive contribution is the operational combination of source-grounded cross-format equivalence, evidence paths, and explicit abstention, not a new general theory of testing or a complete accessibility validator.

# 13. Final limitations

1. The corpus is purposive and controlled, not statistically representative.
2. Only two completed conversion pipelines support the primary empirical comparison; Google is cloud-versioned and Word produced no outputs.
3. Source contracts are implementation-grounded rather than independently adjudicated human ground truth.
4. Fourteen rows remain unresolved under the additive analysis because target representations or associations are not sufficiently observable.
5. The interaction source corpus was not converted through new pipelines in this environment.
6. Structural semantic preservation is not equivalent to screen-reader usability or end-user accessibility.

# 14. Artifact reproducibility verdict

**PASS.** The canonical ZIP contains 342 files under the sanitized `artifact_v3/`
boundary and no Git metadata, cache directories, credentials, or personal path
leaks. The public verifier passes in place and from a clean extraction with 52
records, hashes, provenance links, 39 repeatability outputs, and sanitization.
The included rerun levels correctly distinguish local evidence verification,
LibreOffice reproduction, and cloud-service repetition.

# 15. Anonymity verdict

**PASS for the canonical upload boundary.** The rebuilt PDF has anonymous
author metadata, no email/username/local-path/GitHub identity text, no
attachments/forms/JavaScript, and all seven reported fonts are embedded. The
artifact ZIP and extracted copy pass identity/path scans. Internal workspace
records retain some development paths and historical filenames for provenance;
they are not part of the canonical upload ZIP, and the manifest identifies the
only intended upload files. No identity-bearing remote is configured.

# 16. Final recommendation

**SUBMIT**

Upload only the canonical manuscript PDF and reviewer artifact ZIP named in
`submission/CANONICAL_SUBMISSION.md`. The remaining attacks should be stated as
limitations, not treated as reasons for another broad research cycle.
