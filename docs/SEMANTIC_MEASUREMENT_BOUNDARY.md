# Semantic measurement boundary

Recorded: 2026-10-03

This document defines what A11yPreserve measures and what it does not claim.
The framework tests preservation of selected accessibility semantics through
machine-observable evidence. It does not require source and destination files
to have identical syntax, and it does not treat an unobservable destination as
automatically inaccessible.

## Core distinction

- **Accessibility semantics** are meaningful document properties or
  relationships: roles and hierarchy, language scope, list membership and
  order, table/header relationships, link associations, alternative
  descriptions, footnote associations, equations, and captions.
- **Machine-observable evidence** is the structured or textual evidence from
  which those semantics can be tested: OOXML elements and relationships in the
  source, and PDF structure elements, attributes, annotations, metadata,
  marked content, text, and geometry in the destination.
- **Cross-format equivalence** is a feature-specific rule that accepts a PDF
  realization when it expresses the contracted source meaning, even when its
  syntax differs from OOXML.
- **Measurement boundary** is reached when the available destination evidence
  is insufficient to apply that rule without an unjustified assumption. The
  result is abstention (`UNRESOLVED_EQUIVALENCE`) rather than `LOST`.

## Feature-level classification

The categories describe the semantic property and the current measurement
route, not a claim that every instance of a feature is always decidable.

| Feature family | Semantic property | Source evidence | Destination evidence | Equivalence mechanism | Category |
|---|---|---|---|---|---|
| Headings | heading role and hierarchy | paragraph styles and heading levels | `/H1`--`/H6`, order, and text | style-to-role and hierarchy comparison | A for clear role presence; B for hierarchy |
| Alternative text | image description presence/content | drawing description/alternative-text XML | figure `/Alt` and figure structure | normalized description comparison | A for explicit value; B for figure mapping |
| Lists | list type, item membership, depth, and parent relation | numbering definitions and paragraph numbering | `/L`, `/LI`, labels, nesting, and text | numbering-to-list structure mapping | B |
| Tables | table/cell structure and header relationships | table XML, cell values, header markers | `/Table`, `/TR`, `/TH`, `/TD`, spans and scope evidence | table and header relationship mapping | B |
| Document language | document-wide language | document settings/properties and language contract | PDF `/Lang` and document metadata | normalized language-value comparison | A |
| Inline language | run-scoped language override | run language properties and text span | scoped `/Lang` or equivalent structure | text-span and language-scope mapping | B |
| Decorative image | intentional decorative/non-content state | drawing properties and description state | figure/alt/structure evidence | decorative-state mapping with absence checks | B |
| Hyperlinks | visible-name to target association | relationship target, visible run text | link annotation URI, `/Link`, page text, and geometry | target plus visible-span association | B |
| Document title | document identity/title metadata | core/app properties and visible title contract | PDF metadata and visible title evidence | normalized metadata/visible-title mapping | B |
| Complex tables | multi-level grouping and header scope | merged cells, header rows, cell values | table roles, `/TH`, spans, and structure order | multi-level association mapping | B; some cases C |
| Footnotes | reference-to-note relationship and note text | footnotes part, references, and note IDs | `/Note`, references, links, and note text | reference/target identity mapping | B; some cases C |
| Equations | machine-readable mathematical expression | OMML structure and token sequence | `/Formula` or equivalent tagged expression | expression/token equivalence rule | B; some cases C |
| Captions | figure-to-caption association and text | caption paragraph and figure relationship | `/Figure`, `/Caption`, order, text, and geometry | figure-caption association mapping | B; some cases C |

Category A means the semantic value is directly exposed with minimal
normalization. Category B means the meaning is machine-verifiable only after a
documented cross-format mapping. Category C is reserved for case-level
situations where current evidence cannot establish the relationship; it is not
a synonym for “semantic” or “manual.” In the current additive analysis,
Category-C situations are retained as abstentions for list item/type
correspondence, multi-level table associations, footnote mapping, equation
token identity, and figure-caption association where the required evidence is
missing or ambiguous.

## Measurement coverage and preservation outcomes

A11yPreserve first asks whether a case is measurable: can the source contract,
destination evidence, and equivalence rule support a defensible decision? Only
then does it assign `VERIFIED_PRESERVED`, `OBSERVED_PARTIAL`, `ALTERED`, or
`CONFIRMED_LOST`. `UNRESOLVED_EQUIVALENCE` and `MEASUREMENT_ERROR` are coverage
or measurement outcomes, not hidden preservation outcomes. The frozen primary
analysis has 18 unresolved rows of 52. The additive hyperlink audit resolved
four using independent URI/geometry/text evidence, leaving 14 unresolved in
the derived analysis; it did not modify the frozen result file or primary
denominators.

## Current unresolved taxonomy

The 14 additive unresolved cases remain coded as:

- **11 target-format representability ambiguities:** lists, multi-level
  tables, equations, and captions where the destination exposes related
  structure or text but not a sufficiently accepted realization of the full
  source contract.
- **2 semantic-equivalence ambiguities:** the B04 table rows, where table and
  header structures are visible but complete source-cell correspondence is
  not established.
- **1 extraction limitation:** B11 footnotes, where `/Note` structures exist
  but the body-reference identity mapping is not recoverable from current
  evidence.

These labels distinguish three questions that should not be collapsed:
whether the target format can expose the concept, whether available evidence
can be extracted, and whether the observed representation is semantically
equivalent to the source contract. A secondary pypdf/PyMuPDF audit resolved no
additional rows, so the remaining abstentions are preserved.

## Boundary of the claim

The framework measures preservation of selected accessibility-relevant
semantics in tested DOCX-to-tagged-PDF pipelines. It does not establish
equivalent screen-reader behavior, task completion, perceived accessibility,
or end-user usability. Machine-verifiable semantic preservation is a relevant
structural property, but it is not sufficient evidence for every user's
experience.
