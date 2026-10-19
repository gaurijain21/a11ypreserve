# Real-world sanity corpus decision

## Decision

**Rejected for inclusion.** No document was added to the empirical corpus or
artifact. The controlled fixtures remain preferable because their source
semantics are explicitly inspectable and their provenance is local and stable.

## Candidates investigated

| Candidate | Public provenance | Why it was not included |
|---|---|---|
| [Section508.gov accessible-document resources](https://www.section508.gov/create/documents/) | U.S. government accessibility guidance and downloadable Word guides/checklists | These are authoring guides and checklists, not independently documented real-world source documents with feature-level semantic contracts. The page does not provide machine-readable ground truth for the properties needed here. |
| [Illinois Word Accessibility Exercise](https://doit.illinois.gov/initiatives/accessibility/guides/word/word-accessibility-exercise.html) and its labeled Example 1/Example 2 DOCX files | State of Illinois DoIT training material; the page labels one example “Accessible!” and another “Inaccessible” | The labels are useful provenance but not a complete, independently inspectable contract. The files are training examples intentionally prepared to demonstrate accessibility practice, so they do not provide stronger ecological validity than the controlled corpus for this study. |
| [University of Oregon accessible Word template](https://teaching.uoregon.edu/accessible-ms-word-template) | University teaching-support resource with a public DOCX template | A template is an authoring aid rather than an authored document with stable intended content and feature associations. Its public page does not establish a sufficiently specific source contract. |

## Acquisition and reproducibility check

The public pages were reachable through the literature/web search layer, but the
binary DOCX downloads were not retrievable from this execution environment via
the local HTTP client. The Google/Chrome route was not used to acquire these
files. More importantly, successful download would not solve the oracle problem:
the candidates do not expose enough verified feature-level source semantics to
replace the controlled contracts.

## Scientific conclusion

Adding these files would create an appearance of external validity without
known ground truth. They are retained as rejected candidates and references,
not as empirical observations. The real-world-corpus limitation is therefore
**UNCHANGED**, with a documented rationale rather than an arbitrary omission.
