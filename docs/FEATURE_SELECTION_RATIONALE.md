# Feature-selection rationale

The 13 families are a purposeful, bounded scope: each is accessibility-relevant, has an inspectable DOCX representation, has at least one plausible PDF representation, and can be tested without asserting that the resulting PDF is fully accessible. The suite is not a standards-completeness claim.

| Family | Source representation | Destination observation | Why included / ambiguity |
|---|---|---|---|
| Headings | Word heading styles and hierarchy | PDF heading roles/levels | Structural navigation; generated or shifted levels create mapping ambiguity. |
| Alternative text | Drawing description (`docPr/@descr`) | Figure `/Alt` or equivalent | Non-text alternative; empty/relocated alternatives may be valid only under a narrower contract. |
| Lists | Numbering definitions and paragraph numbering | List containers, numbering, item structure | Navigation and grouping; extraction may not recover item correspondence. |
| Basic tables | Rows, cells, header row | Table/TR/TH/TD structure | Tabular navigation; cell association can be under-observed. |
| Document language | Default language in styles/settings | PDF `/Lang` | Speech/language semantics; locale normalization can be an alteration or acceptable mapping depending on contract. |
| Inline language | Run-level `w:lang` | Span-level language marker | Speech switching; absence of a serialized span is stronger evidence than visible text alone. |
| Decorative images | Empty alternative/decorative intent | Artifact or empty-alt figure representation | Avoiding redundant announcements; PDF has multiple possible encodings. |
| Hyperlinks | Relationship target, visible link text, order | Link annotation plus structure association | Navigation and link-name semantics; annotations alone do not prove association. |
| Document title/metadata | Core properties | PDF metadata/title | Identification and navigation; producers normalize metadata. |
| Complex tables | Spans and multi-level headers | Table roles and header associations | Higher-order table navigation; complete correspondence is difficult to observe. |
| Footnotes | Footnote part, reference, body association | Note/reference structure | References and notes are semantically related; visible note text is not enough. |
| Equations | OMML | Formula/math structure or equivalent | Mathematical meaning; visual glyphs do not establish semantic math equivalence. |
| Captions | Caption paragraph and figure relation | Caption structure/association | Figure identification; visible caption proximity does not prove semantic association. |

The dimensions covered are structural semantics, image semantics, linguistic semantics, metadata, navigation, tables, mathematics, notes, and figure association. A second controlled instance was added in Variant B for every family. F13 reading order is excluded because a reliable automated cross-format oracle was not established. Selection therefore reflects measurability and conversion relevance, not a claim that these families are the most important or exhaustive.
