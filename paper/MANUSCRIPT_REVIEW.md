# Manuscript Review

## Reviewer 1 — Accessibility / ASSETS

### Summary
The manuscript presents a clear source-preservation question and distinguishes it from destination accessibility. The controlled fixtures and confirmed-loss evidence are useful.

### Strengths
The paper avoids user-impact overclaiming, keeps the measurement error visible, and treats altered but usable information separately from loss.

### Major concerns
The corpus is synthetic and there is no disabled-user evaluation. Some partial outcomes depend on representation or parser limits. The paper must not imply that every reported change produces the same assistive-technology consequence.

### Minor concerns
Feature families have unequal complexity and only one primary instance each.

### Recommendation
Weak accept or revise, provided the paper remains a scoped structural-preservation benchmark rather than a comprehensive accessibility or user study.

## Reviewer 2 — Document Engineering / DocEng

### Summary
The method is reproducible locally and documents the two DOCX-to-PDF conditions with hashes and structure evidence.

### Strengths
Frozen OOXML manifests, native converter outputs, destination structure extraction, and independent forensic checks provide a credible chain of evidence.

### Major concerns
Google Docs is cloud-versioned; PDF equivalence is not uniform across features; F11 remains unresolved; and only two pipelines are evaluated.

### Minor concerns
Word is excluded, output text is not always attached to marked-content nodes, and some PDF associations are established by adjacency.

### Recommendation
Accept after revision if the Google condition is described as an end-to-end pipeline and the scope is not broadened beyond DOCX-to-PDF.

## Reviewer 3 — Software Testing / Reliability

### Summary
The experiment is naturally differential and has an explicit oracle, frozen hashes, regression tests, and a hostile audit.

### Strengths
The matrix was independently reconstructed with zero discrepancies; two losses were forensically checked; and the measurement error was not forced into a convenient category.

### Major concerns
The 26 cases are not a statistical sample, feature units are unequal, and PDF parsers can miss structure. A future freeze should include the test-results hash.

### Minor concerns
The benchmark has limited mutation testing and no systematic third-party validator comparison.

### Recommendation
Minor revision. No additional large experiment is required for the scoped claims, but the manuscript should preserve feature-level reporting and evidence links.

## Cross-review action

The manuscript already narrows the claims, reports counts before percentages, uses end-to-end Google pipeline language, and assigns validator comparison to future work. No frozen scientific result was changed in response to these reviews.
