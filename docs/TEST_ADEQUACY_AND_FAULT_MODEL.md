# Test adequacy and fault model

This suite uses a bounded fault model, not a completeness claim.

| Fault class | Exercised by |
|---|---|
| Semantic deletion | Inline language, footnote association, alternatives |
| Author-value mutation | Alt text, language, title/metadata |
| Structure flattening | Headings, lists, tables, captions |
| Hierarchy mutation | Headings and complex tables |
| Association loss | Links, captions, footnotes, table headers |
| Destination substitution/normalization | Metadata and locale values |
| Representational relocation | Alternatives, notes, equations |
| Alternate valid encoding | Calibration controls and unresolved destination rows |
| Extractor blind spot | Calibration false negatives and parser triangulation |
| Ambiguous equivalence | Lists, links, complex tables, equations, captions, footnotes |

The adequacy argument is that each fixture isolates one meaningful source contract and each Variant B case perturbs the instance without changing the target family. The suite covers multiple semantic classes and includes explicit abstention paths. It does not cover all DOCX features, all PDF encodings, layout stress, large documents, forms, multimedia, or all converter failure modes. The appropriate claim is fault-model coverage of selected machine-verifiable preservation risks, not exhaustive testing adequacy.
