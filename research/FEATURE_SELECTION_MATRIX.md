# Feature Selection Matrix

This matrix ranks candidate accessibility-semantic feature families for the expanded A11yPreserve benchmark. Scores are qualitative design judgments made before fixture generation. “Include” means the feature has a sufficiently clear DOCX source contract and a plausible, inspectable PDF representation for the first full benchmark. “Defer” means the feature remains valuable but should not enter the frozen corpus until its equivalence rule is less subjective.

| Feature | Accessibility importance | DOCX ground truth | PDF equivalent | Automation feasibility | Ambiguity | Expected preservation risk | Include? |
|---|---|---|---|---|---|---|---|
| F01 Heading hierarchy | High | High | High: H1–H6 structure elements | High | Low | Medium | Existing |
| F02 Image alternative text | High | High | High: Figure /Alt | High | Low | Medium | Existing |
| F03 List semantics | High | High | High: L/LI/LBody plus list numbering where emitted | High | Medium | High | Existing |
| F04 Table/header structure | High | High | High: Table/TR/TH/TD | High | Medium | High | Existing |
| F05 Document language | High | High: w:lang/default document setting | High: catalog or structure /Lang | High | Low–Medium | Medium | Include |
| F06 Inline language changes | High | High: run-level w:lang | Medium–High: structure language or span-level evidence where emitted | Medium | Medium–High | High | Include |
| F07 Decorative image state | High | High: explicit decorative/non-decorative intent plus image properties | Medium–High: artifact/decorative representation or absence of /Alt with supporting structure | Medium | Medium | High | Include |
| F08 Hyperlink semantics | High | High: relationship target, visible text, hyperlink run | High: Link structure/annotation and URI | High | Medium | High | Include |
| F09 Document title and metadata | Medium–High | High: core properties and title text | Medium–High: PDF /Title, document title structure, metadata | High | Medium | Medium–High | Include |
| F10 Complex/multi-level table headers | High | High: header rows/cells and explicit span/group intent | Medium–High: TH/TR plus scope/headers/span attributes where emitted | Medium | High | High | Include, scoped |
| F11 Footnote/endnote association | Medium–High | Medium–High: note IDs, references, note body relationships | Medium: Note structure, reference, link/backlink patterns | Medium–Low | High | High | Include, scoped |
| F12 Equation/math semantics | High | Medium–High: OMML tree and visible fallback | Medium–Low: MathML/Formula structure or equivalent; often renderer-specific | Medium–Low | High | High | Include, scoped |
| F13 Reading order | High | Medium: source order is clear but intended reading order can be layout-dependent | Medium: structure order and page content order | Low–Medium | High | High | Defer |
| F14 Figure/caption association | Medium–High | High: caption paragraph and figure relationship/ordering | Medium–High: Caption/associated structure or stable adjacency | Medium | Medium–High | Medium–High | Include, scoped |
| Decorative image semantics as a second image variant | High | High | Medium–High | High after F07 contract | Medium | High | Variant of F07 |
| Merged table cells | Medium–High | High: grid spans and cell geometry | Medium: row/cell spans may be emitted inconsistently | Medium | High | High | Defer; stress F10 later |
| Multiple images with distinct alt text | High | High | High: multiple Figure /Alt values | High | Low–Medium | Medium | Variant of F02/F07 |
| Nested headings | High | High | High | High | Low | Medium | Variant of F01 |
| Abbreviation/expansion semantics | Medium | Low–Medium: no consistently portable DOCX authoring contract | Low–Medium | Low | High | Unknown | Defer |
| Metadata alone | Medium | High | Medium | High | Medium | Medium | Covered by F09 |
| Logical grouping/sections | Medium–High | Medium: section breaks are not the same as semantic grouping | Low–Medium | Low | High | High | Defer |
| Form field labels | High in interactive documents | Medium: content controls/forms vary by authoring path | Low–Medium in static tagged PDF | Low–Medium | High | High | Defer |

## Selected benchmark set

The first expanded benchmark will contain thirteen feature families:

- F01 heading hierarchy
- F02 image alternative text
- F03 list semantics
- F04 table/header structure
- F05 document language
- F06 inline language changes
- F07 decorative image state
- F08 hyperlink semantics
- F09 document title and metadata
- F10 complex/multi-level table headers, with a deliberately small two-row contract
- F11 footnote/endnote association, scoped to one note type per fixture
- F12 equation/math semantics, included only where native OMML can be verified
- F14 figure/caption association

F13 reading order, merged-cell stress cases, abbreviations, logical grouping, and form labels are deferred from the frozen benchmark. Multiple images and nested headings are planned instances of existing or selected families rather than separate families.

## Selection principles

The benchmark prioritizes features that are important to assistive-technology users, have a direct OOXML source representation, and expose a destination representation that can be inspected without relying on a validator score. A feature is not included merely because it is important: it must also support a defensible source-to-destination equivalence rule.

F10–F12 and F14 are intentionally scoped. If independent extraction cannot establish the required relationship, the fixture will be excluded or marked `MEASUREMENT_ERROR`; it will not be forced into a preservation classification.
