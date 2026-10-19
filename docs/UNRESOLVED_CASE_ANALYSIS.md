# Unresolved-case analysis

Recorded: 2026-10-03

This is an additive reanalysis. The frozen 52-row result file, hashes, provenance, and primary classifications were not changed.

## Summary

| Measure | Frozen baseline | Additive reanalysis |
|---|---:|---:|
| Atomic rows | 52 | 52 |
| `UNRESOLVED_EQUIVALENCE` | 18 | 14 remaining |
| Newly resolvable rows | 0 | 4 hyperlink rows |
| Remaining unresolved rate | 34.6% | 26.9% |
| Google Docs unresolved rows | 11 | 9 |
| LibreOffice unresolved rows | 7 | 5 |

The four newly resolvable rows are F08/LibreOffice, F08/Google Docs, B08/LibreOffice, and B08/Google Docs. A separate deterministic PyMuPDF audit matches every contracted URI to exactly one annotation and verifies that the annotation rectangle covers the contracted visible words in reading order. This is stronger evidence than the original annotation-only extraction. The frozen classifications remain unchanged; the additive result is a derived measurement improvement, not a historical rewrite.

## Row-by-row analysis

| Fixture | Feature | Pipeline | Source accessibility contract / expected property | Observable PDF evidence | Frozen comparator output | Why the original decision failed | Taxonomy | Additive outcome |
|---|---|---|---|---|---|---|---|---|
| F03 | Lists | Google Docs | Seven items: unordered Accessibility with two nested items, unordered Usability, and ordered Extract/Convert/Compare; preserve item text, type, depth, and parent relation. | List structure and item counts/nesting are observed; ordered/unordered distinction is not exposed by the saved extraction. | `PARTIALLY_PRESERVED` → `UNRESOLVED_EQUIVALENCE` | Item/type equivalence cannot be established from the available destination encoding. | Target-format representability ambiguity | Remains unresolved. |
| F08 | Hyperlinks | LibreOffice | One link: visible text “Accessibility Guidelines” and the WCAG URI, with visible-name association. | URI annotation, `/Link` structure, and page text are present. | `PARTIALLY_PRESERVED` → `UNRESOLVED_EQUIVALENCE` | Original extractor did not independently map annotation geometry to the visible source name. | Extractor limitation; resolved by secondary evidence | **Additively resolved**: exact URI and visible-span match. |
| F08 | Hyperlinks | Google Docs | Same one-link contract as above. | URI annotation, `/Link` structure, and page text are present. | `PARTIALLY_PRESERVED` → `UNRESOLVED_EQUIVALENCE` | Same association gap in the original extraction path. | Extractor limitation; resolved by secondary evidence | **Additively resolved**: exact URI and visible-span match. |
| F10 | Complex table | Google Docs | 5×3 table; two header rows; Enrollment spans Year/Students; Outcome spans Completion Rate; preserve headers, grouping, and cell structure. | Table, TH, and column-span evidence survive; complete multi-level header association/scope is not established. | `PARTIALLY_PRESERVED` → `UNRESOLVED_EQUIVALENCE` | Structural presence does not prove the full multi-level association contract. | Target-format representability and semantic-equivalence ambiguity | Remains unresolved. |
| F12 | Equation | Google Docs | OMML expression `E = mc^2` with tokens E, =, m, c, 2. | Visible equation text survives, but no machine-readable formula/token representation is established. | `PARTIALLY_PRESERVED` → `UNRESOLVED_EQUIVALENCE` | Visible text is not sufficient evidence for the contracted mathematical structure. | Target-format representability ambiguity | Remains unresolved. |
| F14 | Captions | Google Docs | Figure 1 must be associated with “Figure 1. Benchmark workflow overview.” in order. | Caption text and caption-like/page-text evidence survive; structural figure-caption association is absent from the available evidence. | `PARTIALLY_PRESERVED` → `UNRESOLVED_EQUIVALENCE` | Ordered text adjacency does not establish a semantic figure-caption association. | Target-format representability ambiguity | Remains unresolved. |
| B03 | Lists | LibreOffice | Ordered First/Second items with nested unordered alpha/beta/gamma items; preserve text, type, depth, and parent relation. | List roles/nesting and 19 list nodes are observed, but source item text/type correspondence is not recovered. | `UNRESOLVED_EQUIVALENCE` | Destination list-node multiplicity is not a sufficient source contract match. | Extraction incomplete; target-format representability ambiguity | Remains unresolved. |
| B03 | Lists | Google Docs | Same B03 mixed ordered/nested list contract. | 13 list nodes and one heading are observed; item text/type equivalence is not established. | `UNRESOLVED_EQUIVALENCE` | Same item-level correspondence gap. | Extraction incomplete; target-format representability ambiguity | Remains unresolved. |
| B04 | Table | LibreOffice | 4×4 table with header row Quarter, Region, Cases handled, Completion rate and all cell values. | Table/header structure and 17 table nodes are observed. | `UNRESOLVED_EQUIVALENCE` | Complete source-cell correspondence is not established by the destination extractor. | Extraction incomplete; semantic-equivalence ambiguity | Remains unresolved. |
| B04 | Table | Google Docs | Same 4×4 table/cell contract. | Table/header structure and 17 table nodes are observed. | `UNRESOLVED_EQUIVALENCE` | Same cell-level correspondence gap. | Extraction incomplete; semantic-equivalence ambiguity | Remains unresolved. |
| B08 | Hyperlinks | LibreOffice | Two visible-name links: “the WCAG standard” → WCAG URI and “the PDF reference” → PDF Association URI. | Two annotations, two `/Link` roles, and page text are present. | `UNRESOLVED_EQUIVALENCE` | Original extraction retained targets but did not prove the visible-name association. | Extractor limitation; resolved by secondary evidence | **Additively resolved**: both exact URI/span matches. |
| B08 | Hyperlinks | Google Docs | Same two-link contract. | Two annotations, two `/Link` roles, and page text are present. | `UNRESOLVED_EQUIVALENCE` | Same association gap in the original extraction path. | Extractor limitation; resolved by secondary evidence | **Additively resolved**: both exact URI/span matches. |
| B10 | Complex table | LibreOffice | 5×4 table with two header rows, Population/Outcome groups, and Year/Group/Rate/Count cells. | Complex table/header structure is observed; complete multi-level association equivalence is not established. | `UNRESOLVED_EQUIVALENCE` | Header presence and spans do not establish the full source grouping relation. | Target-format representability and semantic-equivalence ambiguity | Remains unresolved. |
| B10 | Complex table | Google Docs | Same B10 two-level header/grouping contract. | Complex table/header structure is observed; complete multi-level association equivalence is not established. | `UNRESOLVED_EQUIVALENCE` | Same association limitation. | Target-format representability and semantic-equivalence ambiguity | Remains unresolved. |
| B11 | Footnotes | LibreOffice | Two footnotes with exact note texts “First variant note.” and “Second variant note.” plus reference mapping. | Two `/Note` structures, two footnotes, and link/reference nodes are observed; exact note text/reference mapping is not recovered. | `UNRESOLVED_EQUIVALENCE` | Note presence does not establish body-text/reference identity. | Extraction incomplete; intentionally undecidable with current evidence | Remains unresolved. |
| B12 | Equations | LibreOffice | Two machine-readable expressions: `E = mc^2` and `a = b + c`, with exact tokens. | Two `/Formula` nodes are observed, but token/expression equivalence is not established. | `UNRESOLVED_EQUIVALENCE` | Formula-role presence does not prove expression identity. | Target-format representability and semantic-equivalence ambiguity | Remains unresolved. |
| B12 | Equations | Google Docs | Same two-expression/token contract. | Visible equations occur in page text, but no required machine-readable formula representation is established. | `UNRESOLVED_EQUIVALENCE` | Text survival cannot establish the contracted equation structure. | Target-format representability ambiguity | Remains unresolved. |
| B13 | Captions | Google Docs | Figure 1 “Figure 1. Workflow.” and Figure 2 “Figure 2. Results.” with ordered figure-caption pairs. | Two figures and caption text are present through ordered page-text evidence, but no destination Caption association is established. | `UNRESOLVED_EQUIVALENCE` | Text presence/ordering is weaker than the pair association contract. | Target-format representability ambiguity | Remains unresolved. |

## Taxonomy and counts after the additive check

| Reason category | Remaining rows | Explanation |
|---|---:|---|
| Target-format representability ambiguity | 11 | Lists, multi-level table relations, equations, and captions lack an accepted observable PDF representation sufficient for the full contract. |
| Semantic-equivalence ambiguity | 2 | B04 cell correspondence requires a relation not exposed by current evidence; this is not automatically a converter failure. |
| Extraction incomplete / measurement limitation | 1 | B11 note-body/reference mapping is not recoverable from current structured evidence. |
| Extractor limitation resolved by independent geometry | 0 remaining (4 resolved) | Link annotation geometry plus independent text extraction established the missing association for F08/B08. |

The categories are evidence-derived. No LLM judgment, visual-only decision, or assumed one-to-one tag mapping was used. “Unresolved” remains the safer result where a richer extraction would still require an unjustified equivalence assumption.

## Exact additive logic change

The frozen `extract_semantics.py`, comparator, and 17 existing comparator tests were not modified. The additive script `scientific_strengthening/unresolved_analysis/link_association_audit.py` adds one independent rule for hyperlink rows:

1. read URI annotations with PyMuPDF;
2. extract page words and retain words substantially covered by each annotation rectangle;
3. compare normalized linked-span words and URI against the source contract; and
4. resolve only when each expected link has exactly one target match and an exact visible-span match.

The script's four-case output is deterministic. Because no frozen comparator was changed, no comparator regression suite was required; the script itself serves as a bounded secondary-evidence audit. A future public artifact can include this audit as a derived analysis without replacing the frozen result file.
