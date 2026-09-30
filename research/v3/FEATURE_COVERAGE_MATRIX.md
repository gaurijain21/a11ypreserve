# V3 feature coverage and adequacy boundary

The 13 Core fixtures were selected purposively, not sampled as a representative corpus. Selection required: (1) a machine-verifiable DOCX source assertion, (2) accessibility relevance or conversion sensitivity, (3) a plausible inspectable PDF representation, and (4) a feature-specific comparison rule. The documented basis is `research/FEATURE_SELECTION_MATRIX.md`, supplemented by W3C accessibility concepts, PDF/UA structure guidance, and exporter mappings.

| Family | Core instance | Contract observable? | Destination mapping | Variant B stress | Coverage limitation |
|---|---|---:|---|---|---|
| headings | F01 | yes | H roles/order | deeper nesting/title boundary | one hierarchy pattern |
| alt text | F02 | yes | Figure/Alt | multiple images and punctuation | one source string pattern |
| lists | F03 | yes | L/LI/LBody/numbering | nested mixed list | one list layout |
| table headers | F04 | yes | Table/TR/TH/TD | repeated header and width changes | small regular table |
| document language | F05 | yes | document/structure Lang | language-specific text | one default language |
| inline language | F06 | yes | span/structure Lang | two language runs | one override boundary |
| decorative image | F07 | yes | Artifact or empty Figure | decorative + informative pair | producer-specific encoding |
| hyperlinks | F08 | yes | Link/annotation/URI | two link names/targets | one association pattern |
| title/metadata | F09 | yes | title/metadata | visible and metadata disagreement | one title shape |
| complex table | F10 | scoped | table/header spans | three-level header | no exhaustive table model |
| footnote | F11 | scoped | Note/Reference | two notes and cross-page body | one note type in Core |
| equation | F12 | scoped | Formula/MathML/equivalent | multiple expressions | renderer-specific math |
| captions | F14 | scoped | Caption/figure association | two figures/captions | adjacency ambiguity |

## Adequacy statement

This matrix demonstrates a principled selection basis, not standards completeness or test-suite adequacy in the formal software-testing sense. One atomic instance per family cannot estimate within-family variance or exhaust an accessibility fault model. Variant Set B and the integrated sanity check improve methodological stress coverage but do not convert the corpus into a representative sample.

F13 remains reserved for reading order and deferred because reliable automated source-to-PDF equivalence could not be established.

