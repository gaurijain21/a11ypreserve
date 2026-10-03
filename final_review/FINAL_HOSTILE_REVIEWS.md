# Final Hostile Reviews

## Reviewer A — Accessibility researcher

### Summary
The paper asks a meaningful preservation question and reports two carefully audited losses, but its evidence is structural rather than user-centered.

### Strengths
Clear distinction between preservation and destination accessibility; explicit measurement error; feature-level reporting; bounded claims.

### Major concerns
The fixtures are synthetic; user impact is not measured; some partial outcomes depend on representational assumptions; two pipelines do not establish prevalence.

### Minor concerns
Feature families have unequal complexity and one primary fixture each. The paper could explain practical importance more clearly without inferring harm.

### Questions for authors
Which changes are likely to matter most in assistive-technology workflows? How will integrated documents be handled later?

### Most likely rejection reason
Reviewers may judge the study as document-structure testing rather than accessibility research if the practical motivation is not kept visible.

### Can it be fixed without new experiments?
Yes, by preserving the scope statement, emphasizing encoded-information preservation, and avoiding user-impact claims. A user study is future work, not a prerequisite for this structural question.

### Recommendation
Major revision or weak accept, depending on venue scope.

## Reviewer B — Document-engineering researcher

### Summary
The frozen corpus, conversion provenance, PDF extraction, and cross-pipeline matrix are credible, but cross-format equivalence remains the central technical risk.

### Strengths
Native DOCX inputs, real conversion outputs, explicit contracts, hashes, independent checks, and a retained measurement-error category.

### Major concerns
Only two pipelines are tested; Google Docs is cloud-versioned; PDF encodings differ; F11 remains unresolved; some associations rely on parser evidence or adjacency.

### Minor concerns
The table is dense, and the source/destination mappings could be expanded in supplementary material.

### Questions for authors
How were contracts frozen before classification? Which observed partials are parser limits versus converter behavior?

### Most likely rejection reason
The benchmark may be viewed as too small or too format-specific for a general document-engineering claim.

### Can it be fixed without new experiments?
Yes for the current paper: narrow the title and claims, retain evidence limitations, and position broader formats/converters as future work.

### Recommendation
Weak accept after revision for a scoped document-engineering venue.

## Reviewer C — Software-testing researcher

### Summary
The work resembles differential testing with a constructed oracle, but the oracle is hand-designed and the test corpus is intentionally small.

### Strengths
Frozen inputs, reproducible output hashes, explicit contracts, hostile comparator tests, independent reconstruction, and no denominator manipulation.

### Major concerns
No randomized generation, mutation study, or third converter; PDF parser limitations may confound failures; one measurement error is unresolved.

### Minor concerns
`a11ydiff` is operational but modest; the paper should not present it as a general PDF checker.

### Questions for authors
What is the general testing abstraction beyond this corpus? How would oracle coverage scale?

### Most likely rejection reason
Insufficient testing novelty or inadequate evidence for a software-testing venue.

### Can it be fixed without new experiments?
Partly. The manuscript can state the testing contribution precisely; stronger testing-venue claims would require future experiments.

### Recommendation
Borderline for ICST/SANER/ISSRE; stronger fit if framed as a source-grounded oracle design with explicit scope.

## Reviewer D — Skeptical general systems reviewer

### Summary
The paper is careful but may be too narrow for a general systems venue.

### Strengths
End-to-end real workflows, reproducibility controls, empirical variation, and transparent limitations.

### Major concerns
Two converters, one source format, no user study, no broad scalability evidence, and cloud-version dependence limit general systems conclusions.

### Minor concerns
The paper could be shortened for venues requiring a tighter empirical narrative.

### Questions for authors
What system-level decision does the benchmark enable? What would a release include?

### Most likely rejection reason
Insufficient breadth relative to general systems scope.

### Can it be fixed without new experiments?
Only partly; venue choice is the main remedy.

### Recommendation
Reject for a broad systems venue; consider accessibility or document-engineering venues.
