# V5 cross-format equivalence specification

The machine-readable contract is [`contracts/v5/cross_format_equivalence.json`](../contracts/v5/cross_format_equivalence.json). It freezes the distinction between:

- **source-value fidelity**: the author-relevant value survives exactly or under a documented normalization; and
- **machine-observable semantic preservation**: a destination relation required by the source contract is recoverable in an accepted PDF representation.

Tag presence, visible text, or a feature-shaped node is never sufficient by itself. An accepted equivalent must satisfy the family-specific evidence requirements. Exact changed alt text, language tags, metadata, or link targets are reported as `ALTERED` under a fidelity contract; they are not automatically described as human-inaccessible or harmful. Unresolved equivalence and measurement error are explicit abstentions.

The V5 rules make the difficult boundaries explicit:

| Family | Accepted evidence boundary |
|---|---|
| Alternative text | Figure identity plus `/Alt`; changed author wording is altered fidelity, not automatic usability loss. |
| Document language | Document `/Lang`; normalized language tags may be equivalent only when normalization is specified. |
| Tables | Table/cell/header graph and required associations; TH presence alone is insufficient. |
| Lists | L/LI/LBody hierarchy, type, text/order/depth where contracted; list containers alone are insufficient. |
| Equations | Formula structure and expression/token evidence; visible glyphs alone are not mathematical preservation. |
| Captions | Caption text plus recoverable association to the intended figure; page adjacency alone is partial/abstention. |
| Footnotes | Reference, Note, body, and identity relation; a `/Note` node alone is not a preserved footnote. |

The comparator must prefer abstention to an unsupported confident result. A future rule change creates a new V5 comparator version and reruns affected rows; it does not rewrite V4 labels.
