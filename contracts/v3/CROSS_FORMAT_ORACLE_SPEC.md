# Cross-format oracle specification

## Purpose

The oracle compares a verified source contract with destination PDF structure. It does not compare serialized XML and PDF bytes, and it does not infer complete accessibility from a tag count or validator score.

## Evidence model

Each feature contract declares (a) the source assertion, (b) the concept being preserved, (c) one or more accepted destination representations, (d) disallowed shortcuts, and (e) the evidence required to make a definitive decision. Destination evidence must identify structure elements, attributes, annotations, marked-content or object references, text, and parser path where applicable.

## Standards grounding

The mapping is grounded in the feature concepts rather than a claim that DOCX and PDF have identical semantics. WCAG 2.2 defines programmatically determinable headings, text alternatives, link purpose, page language, and language of parts as accessibility concepts: <https://www.w3.org/TR/WCAG22/>. PDF/UA reference material identifies the PDF structure types and attributes relevant to this study, including `Figure`, `Caption`, `Formula`, `Note`, `Link`, `Table`, `TH`, `Lang`, `Alt`, `ActualText`, `RoleMap`, and parent relationships: <https://pdfa.org/download-area/accessibility/MatterhornProtocol_1-02.pdf>, <https://pdfa.org/download-area/cheat-sheets/LogicalStructureObjects.pdf>. Microsoft’s current Word PDF accessibility documentation provides a concrete exporter mapping for headings, figures/alt text, artifacts, captions, links, notes, and formulas: <https://learn.microsoft.com/en-us/office/pdf/word/wordpdfaccessibility>.

These sources justify inspecting a destination representation; they do not prove that every source concept has one canonical PDF encoding. Equivalence is therefore feature-specific and may be unresolved.

## Feature mapping table

| Source concept | Accepted destination evidence | Definitive absence rule | Main uncertainty |
|---|---|---|---|
| heading hierarchy | ordered `H`/`H1`--`H6` structure with contract-matching levels and content/order evidence | no accepted heading representation after full structure traversal | extraction may not bind all heading text |
| image alternative text | `Figure` with matching `Alt`, or a contract-approved equivalent | no figure/alt or equivalent after object and structure search | regenerated/prefixed alt text and object association |
| list semantics | `L`/`LI`/`LBody`, nesting, and explicit numbering/type evidence where required | required list structure absent and representable | ordered/unordered type may be omitted or encoded differently |
| table/header structure | `Table`/`TR`/`TH`/`TD` plus span/scope evidence required by contract | required table/header representation absent | multi-level header relationships may be encoded indirectly |
| document language | document/structure `Lang` matching source contract | no applicable language declaration after inheritance search | document-level versus element-level scope |
| inline language | span/structure `Lang` or accepted equivalent bound to the target text | no target-bound language representation after full search | text binding and inheritance |
| decorative image | `Artifact` or contract-approved decorative representation | no accepted representation and informative/decorative distinction is measured | some producers emit empty `Figure` instead of `Artifact` |
| hyperlink | `Link` structure/annotation association and matching URI/name evidence | no link annotation/structure or required association | visible-name association may be encoded indirectly |
| title/metadata | matching PDF metadata/title structure under the contract | required title metadata absent | multiple metadata/title fields and producer defaults |
| complex table | table/header roles plus required span/scope/association evidence | required associations absent and measurable | `Scope`, headers, spans, and role mappings vary |
| footnote | `Note`/`Reference`/association or contract-approved equivalent | no association after structure, parent, annotation, object, and text-order search | note body text may not be recoverable |
| equation | `Formula`/MathML/approved machine-readable math representation with visible expression | no accepted machine-readable math representation | token-level math is heterogeneous |
| figure/caption | `Caption` and figure association, or explicitly accepted feature-specific equivalent | no association after structure and text/object search | adjacency is not equivalent unless contract allows it |

## Prohibited inferences

Visible text is not proof of semantic association. A tagged PDF is not proof that a source property survived. Absence in one parser's extracted encoding is not proof of semantic absence. A validator pass/fail is not a source-preservation oracle. `ALTERED` is not a claim of user harm.

