# Semantic Contracts

This document freezes the source-grounded semantic contracts before new DOCX fixtures are generated. The contracts define what is being compared, what counts as equivalent, and what evidence is required. They do not define whether a PDF passes a general accessibility checker.

## Frozen two-dimensional taxonomy

### Preservation fidelity

Allowed values:

`EXACT_PRESERVATION`, `SEMANTICALLY_EQUIVALENT`, `PARTIAL_PRESERVATION`, `MUTATED`, `REGENERATED`, `LOST`, `NOT_REPRESENTABLE`, `NOT_APPLICABLE`, `MEASUREMENT_ERROR`, `INVALID_CONVERSION`.

### Destination accessibility

Allowed values:

`ACCESSIBLE_EQUIVALENT`, `ACCESSIBLE_BUT_ALTERED`, `DEGRADED_ACCESSIBILITY`, `INACCESSIBLE_FEATURE`, `UNKNOWN`.

The dimensions are independent. A meaningful but changed alternative text is `MUTATED` plus `ACCESSIBLE_BUT_ALTERED`; it is not `LOST`.

## Common decision rules

- `EXACT_PRESERVATION` requires the source value and destination value to match after only explicitly documented serialization normalization.
- `SEMANTICALLY_EQUIVALENT` permits a different syntax or structure only when the destination has an independently established equivalent meaning.
- `PARTIAL_PRESERVATION` means part of the source contract survives but a required component does not.
- `MUTATED` means a destination value exists but differs without being an intentional, contractually permitted regeneration.
- `REGENERATED` is reserved for converter-created equivalent content whose provenance is established and whose value is not a faithful copy.
- `LOST` requires a capable destination extractor to establish absence. Missing parser support is `MEASUREMENT_ERROR`.
- `NOT_REPRESENTABLE` is used only when the destination format genuinely has no equivalent mechanism.
- `INVALID_CONVERSION` applies to an unreadable or corrupt output, never to a valid but inaccessible output.
- Destination accessibility describes the usability of the destination representation, not fidelity to author intent.

Every result must retain raw source value, raw destination value, representation evidence, source hash, output hash, converter/version, and extraction paths.

## F01 Heading hierarchy

### Source representation

Native Word paragraph styles `Heading 1` through `Heading 6`, extracted from `w:pStyle` in `word/document.xml`. Ground truth includes ordered heading text and level.

### Intended accessibility meaning

The document exposes a navigable hierarchical outline whose level and order match the authored headings.

### PDF equivalent representation

Structure elements `/H1` through `/H6`, their ordered placement in `StructTreeRoot`, and independently extracted heading text.

### Preservation and degradation rules

- Matching levels, order, and heading text: `SEMANTICALLY_EQUIVALENT`.
- Same source headings with an added unrelated heading or altered hierarchy: `PARTIAL_PRESERVATION`.
- Heading text survives but is no longer a heading: `LOST` for heading semantics.
- A changed heading label without an intentional source contract: `MUTATED`.

### Extraction and independent verification

Extract OOXML styles and text. Extract PDF roles and marked-content/page text with pypdf; independently verify the text sequence with a second text extractor where available.

### Known ambiguity

Title styles or converter-generated document titles may appear as headings. They must be reported as additional destination structure, not silently discarded.

## F02 Image alternative text

### Source representation

`wp:docPr/@descr` for each non-decorative image, matched by deterministic image order and relationship evidence.

### Intended accessibility meaning

An assistive-technology user receives the author-written text alternative for meaningful non-text content.

### PDF equivalent representation

`/Figure` structure elements with `/Alt` values.

### Preservation and degradation rules

- Exact author string and non-decorative figure: `EXACT_PRESERVATION`.
- Meaningful changed string: `MUTATED` plus `ACCESSIBLE_BUT_ALTERED`.
- Converter-created equivalent description with provenance: `REGENERATED` plus `ACCESSIBLE_BUT_ALTERED`.
- Missing `/Alt` for a meaningful image: `LOST` plus `INACCESSIBLE_FEATURE`.

### Extraction and independent verification

Extract OOXML `docPr` values and image order. Extract `/Figure` and `/Alt` directly from PDF objects; independently verify figure count and page content.

### Known ambiguity

Nearby visible text is not alternative text. Empty `/Alt` is not equivalent to an explicit decorative state unless the decorative contract is separately satisfied.

## F03 List semantics

### Source representation

Word numbering properties `w:numId`, `w:ilvl`, and numbering format. Ground truth includes ordered/unordered type, nesting depth, item text, and parent relationship.

### Intended accessibility meaning

Assistive technology can identify list containers, item boundaries, type, and nesting.

### PDF equivalent representation

`/L`, `/LI`, and `/LBody` structure, plus explicit `/ListNumbering` or an equally strong representation of ordered/unordered type.

### Preservation and degradation rules

- Roles, item order, nesting, and explicit type all match: `SEMANTICALLY_EQUIVALENT`.
- List roles and nesting survive but type is only visually inferable: `PARTIAL_PRESERVATION` plus `DEGRADED_ACCESSIBILITY`.
- Only indentation or bullet glyphs remain: `LOST` for encoded list semantics.

### Extraction and independent verification

Extract OOXML numbering and compare with raw PDF structure traversal. Treat page text and glyphs as corroboration, never as the sole proof of list semantics.

### Known ambiguity

PDF producers differ in whether ordered/unordered type is encoded in `/A /ListNumbering`. Missing attributes are an evidence limitation only if no equivalent representation is found.

## F04 Table/header structure

### Source representation

OOXML table rows/cells, dimensions, cell text, and `w:tblHeader` on the header row.

### Intended accessibility meaning

Users can navigate the table by rows and columns and identify header cells and their relationship to data cells.

### PDF equivalent representation

`/Table`, `/TR`, `/TH`, `/TD`, plus scope/headers/span information where needed.

### Preservation and degradation rules

- Table shape, cell sequence, header row, and associations are established: `SEMANTICALLY_EQUIVALENT`.
- Table and cells survive but header or association evidence is missing: `PARTIAL_PRESERVATION`.
- Visual grid only, with no usable table structure: `LOST`.

### Extraction and independent verification

Extract OOXML cell matrix and header flag. Traverse PDF structure roles and independently verify cell text/page order.

### Known ambiguity

A `TH` role proves header role but not necessarily complete row/column association. Multi-level header contracts therefore require stricter evidence than F04.

## F05 Document language

### Source representation

Default document language from `w:lang/@w:val` in the document defaults/styles settings, with normalized BCP 47 language value.

### Intended accessibility meaning

Speech synthesis, hyphenation, pronunciation, and language-aware assistive technology use the correct primary language.

### PDF equivalent representation

Catalog or structure `/Lang` value, with precedence and inheritance recorded.

### Preservation and degradation rules

- Same normalized primary language: `EXACT_PRESERVATION` or `SEMANTICALLY_EQUIVALENT`.
- Language exists but is changed to another language: `MUTATED` plus `ACCESSIBLE_BUT_ALTERED`.
- Source language exists and destination supports `/Lang` but it is absent: `LOST` plus `INACCESSIBLE_FEATURE`.
- Destination lacks a language mechanism: `NOT_REPRESENTABLE` only after capability verification.

### Extraction and independent verification

Read OOXML settings/styles directly. Read PDF catalog `/Lang` and relevant structure inheritance; verify with a second object-level inspection.

### Known ambiguity

Locale variants such as `en-US` and `en-GB` are not interchangeable for exact preservation, though semantic equivalence may be allowed only when the contract explicitly says so.

## F06 Inline language changes

### Source representation

Run-level `w:lang` on the target run, including the exact text span and language tag.

### Intended accessibility meaning

Assistive technology switches pronunciation language for the marked span without losing the surrounding document language.

### PDF equivalent representation

Language on a marked-content/structure span or another inspectable equivalent attached to the same text span.

### Preservation and degradation rules

- Same span and language: `SEMANTICALLY_EQUIVALENT`.
- Document language survives but inline override disappears: `PARTIAL_PRESERVATION` plus `DEGRADED_ACCESSIBILITY`.
- Span survives with wrong language: `MUTATED`.
- No span or language evidence where PDF supports it: `LOST`.

### Extraction and independent verification

Extract OOXML runs with `w:lang`. Extract PDF language properties and marked text; independently verify span text through page text and content-stream/structure association.

### Known ambiguity

PDF producers may attach language at a parent structure element rather than the exact run. Parent inheritance must be modeled explicitly; it must not be assumed from document `/Lang` alone.

## F07 Decorative image state

### Source representation

An explicit fixture-level decorative intent, plus the image property state used by the authoring path. A meaningful image with alt text and an explicitly decorative image must be separate manifest records.

### Intended accessibility meaning

Decorative artwork is skipped by assistive technology, while meaningful artwork receives an alternative.

### PDF equivalent representation

Artifact/decorative representation or a documented equivalent; `/Figure` with meaningful `/Alt` for informative images.

### Preservation and degradation rules

- Explicit decorative state maps to an equivalent artifact/decorative representation: `SEMANTICALLY_EQUIVALENT`.
- Image is omitted from the accessibility tree but no explicit equivalent is provable: `PARTIAL_PRESERVATION` or `MEASUREMENT_ERROR` depending evidence.
- Decorative image becomes a meaningful figure or meaningful image loses its non-decorative alternative: `MUTATED` or `LOST`.

### Extraction and independent verification

Inspect OOXML image properties and manifest intent. Inspect PDF structure role, `/Alt`, artifact markers, and page content independently.

### Known ambiguity

Missing `/Alt` alone does not prove decorativeness. This feature must not be inferred from absence alone.

## F08 Hyperlink semantics

### Source representation

Hyperlink relationship target URI, visible link text, and hyperlink run/relationship identity in OOXML.

### Intended accessibility meaning

Users can identify a link and activate the intended destination from meaningful link text.

### PDF equivalent representation

`/Link` structure or link annotation, exact destination URI, and associated visible text/structure.

### Preservation and degradation rules

- Link exists, URI and visible text match: `SEMANTICALLY_EQUIVALENT`.
- URI survives but link structure or name evidence is incomplete: `PARTIAL_PRESERVATION`.
- URI changes: `MUTATED`.
- Visible text remains but activation/destination is absent: `LOST`.

### Extraction and independent verification

Extract OOXML relationships and run text. Extract PDF annotations, actions, destinations, and Link structure; independently compare URI normalization and page association.

### Known ambiguity

URI normalization, external redirects, and link text split across marked-content spans must be normalized only under a documented rule.

## F09 Document title and metadata

### Source representation

Separate source fields: visible document title text/style, core property title, author, subject, and creation metadata where relevant.

### Intended accessibility meaning

Users can identify the document and assistive technology/user agents receive useful document metadata.

### PDF equivalent representation

PDF `/Title`, `/Author`, `/Subject`, language, and title structure where present.

### Preservation and degradation rules

- Exact field match: `EXACT_PRESERVATION`.
- Same document identity in an equivalent field: `SEMANTICALLY_EQUIVALENT`.
- Metadata remains meaningful but is changed: `MUTATED` plus `ACCESSIBLE_BUT_ALTERED`.
- Visible content remains but metadata is absent: classify the specific missing field `LOST`; do not treat all metadata as one failure.

### Extraction and independent verification

Read OOXML core properties and visible title style. Read PDF Info/XMP/catalog values and structure; independently verify visible title text.

### Known ambiguity

Converter-generated titles, producer metadata, and timestamps are not source-preservation targets unless explicitly included in the manifest.

## F10 Complex/multi-level table headers

### Source representation

Small two-row header table with explicit header cells, column spans/row spans where used, and a manifest-level expected header-to-data relationship.

### Intended accessibility meaning

Users can identify all applicable column/row headers for each data cell, not merely the first row.

### PDF equivalent representation

Nested table structure with `/TH`, `/TD`, row/column spans, `/Scope`, `/Headers`, or another inspectable association mechanism.

### Preservation and degradation rules

- Every data cell has the expected header set: `SEMANTICALLY_EQUIVALENT`.
- Header roles survive but some associations cannot be established: `PARTIAL_PRESERVATION`.
- Table exists only visually or first-row header survives while grouped headers disappear: `DEGRADED_ACCESSIBILITY` and `PARTIAL_PRESERVATION`.
- No semantic table remains: `LOST`.

### Extraction and independent verification

Extract OOXML grid spans and manifest associations. Traverse PDF rows/cells and association attributes; independently check a small manually enumerated association sample.

### Known ambiguity

The first multi-level table fixture is a scoped stress case. If the PDF representation cannot establish associations deterministically, exclude the fixture rather than inventing a score.

## F11 Footnote/endnote association

### Source representation

One note type per atomic fixture: reference marker identity, note body identity, and source-to-note relationship from footnotes/endnotes parts.

### Intended accessibility meaning

Users can move from the reference to the note and understand the note’s association with the source text.

### PDF equivalent representation

Note/reference structure or stable link/backlink association with note text and reading order evidence.

### Preservation and degradation rules

- Reference, body, and association all survive: `SEMANTICALLY_EQUIVALENT`.
- Note text survives but reference/backlink or association is missing: `PARTIAL_PRESERVATION`.
- Note text or reference disappears: `LOST`.
- Destination has no equivalent association mechanism: `NOT_REPRESENTABLE` only after capability check.

### Extraction and independent verification

Parse OOXML note parts and reference markers. Inspect PDF structure, annotations, links, and text order; independently verify the reference/body pair.

### Known ambiguity

Superscript appearance is not proof of a footnote relationship. A visually placed note without association evidence is degraded.

## F12 Equation/math semantics

### Source representation

Native OMML subtree with normalized operator/text structure, not merely a raster image or plain-text fallback.

### Intended accessibility meaning

Users can perceive or navigate the mathematical expression as mathematics rather than as an unexplained image or ambiguous glyph sequence.

### PDF equivalent representation

Native math structure/MathML or an explicitly documented equivalent. A rasterized image is not equivalent to native math semantics.

### Preservation and degradation rules

- Native expression structure and meaning survive: `SEMANTICALLY_EQUIVALENT`.
- Visual equation survives with no machine-readable math structure: `PARTIAL_PRESERVATION` or `DEGRADED_ACCESSIBILITY`.
- Equation becomes unrelated text/image or disappears: `MUTATED` or `LOST`.
- If a converter genuinely cannot represent native math, `NOT_REPRESENTABLE` requires capability evidence.

### Extraction and independent verification

Extract OMML and normalize tokens/operators. Inspect PDF structure and content; independently inspect whether the destination exposes math semantics rather than only pixels.

### Known ambiguity

Equation rendering quality and equation accessibility are separate. The fixture must not be included if only visual similarity can be measured.

## F14 Figure/caption association

### Source representation

One meaningful image, one explicit caption paragraph, and a manifest association based on document order and a stable caption marker.

### Intended accessibility meaning

Users can identify which caption describes which figure and encounter the pair in a coherent order.

### PDF equivalent representation

Figure and caption structure/association, or a deterministic equivalent based on structure and ordered adjacency.

### Preservation and degradation rules

- Figure, caption text, and association survive: `SEMANTICALLY_EQUIVALENT`.
- Both survive but association is only adjacency-based: `PARTIAL_PRESERVATION` unless the contract permits adjacency.
- Caption or figure disappears: `LOST`.

### Extraction and independent verification

Extract OOXML figure order and caption marker. Inspect PDF Figure/Caption/paragraph structure, order, and text; independently verify the pairing from raw structure.

### Known ambiguity

A caption-looking paragraph is not necessarily semantically associated. If no inspectable association exists, report the limitation rather than assuming it.

## Deferred feature contracts

Reading order, merged-cell stress cases, abbreviations, logical grouping/sections, and form labels are deferred. They require additional destination-specific equivalence rules before they can be frozen into the benchmark. They may be revisited after the selected corpus has passed readiness checks.
