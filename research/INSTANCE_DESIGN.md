# Phase 4 instance design

## Purpose

The first full benchmark freeze is an atomic, causal-isolation corpus. Each
fixture has one primary feature family and a machine-readable source contract.
The frozen corpus contains 13 atomic fixtures: the four Pilot 1 fixtures plus
nine newly verified Phase 4 fixtures. It is intentionally not yet a large
statistical sample.

## Initial atomic set

| Family | Frozen fixture | Initial instances | Planned robustness variants |
|---|---|---:|---|
| F01 heading hierarchy | F01_HEADINGS | 1 | simple hierarchy; sibling H2s; valid skipped visual sizing with native heading styles |
| F02 image alt text | F02_ALT_TEXT | 1 | short literal; long description; Unicode/punctuation; multiple distinct images |
| F03 list semantics | F03_LISTS | 1 | unordered; ordered; nested; mixed nesting |
| F04 table/header structure | F04_TABLE | 1 | simple header row; multiple data rows |
| F05 document language | F05_DOCUMENT_LANGUAGE | 1 | en-US; another valid primary language |
| F06 inline language | F06_INLINE_LANGUAGE | 1 | one override; multiple overrides; Unicode phrase |
| F07 decorative image state | F07_DECORATIVE_IMAGE | 1 | meaningful/decorative pair; multiple decorative states |
| F08 hyperlink semantics | F08_LINKS | 1 | visible text different from URI; internal target; multiple links |
| F09 document title/metadata | F09_DOCUMENT_TITLE | 1 | title-only; title plus subject/keywords |
| F10 complex table | F10_COMPLEX_TABLE | 1 | two header rows; later controlled span/association variant |
| F11 footnote/endnote association | F11_FOOTNOTES | 1 | footnote; separately verified endnote variant if destination support is adequate |
| F12 equation/math | F12_EQUATION | 1 | simple native OMML; fraction/superscript native OMML variant |
| F14 figure/caption association | F14_CAPTIONS | 1 | one figure/caption pair; multiple figures with distinct captions |

The planned variants are not part of the frozen Phase 4 execution set until
they pass the same raw-OOXML, manifest, extractor, and rendering checks. They
are candidates for replication, not artificial rows for inflating rates.

## Replication policy

After the atomic execution, add variants only when they probe a meaningful
robustness boundary. Keep the source contract and feature family fixed, assign
stable instance identifiers, and create a new corpus version rather than
modifying a frozen fixture. Report feature-level results before any aggregate.

## Integrated documents

After atomic behavior is understood, add a small report, policy memo, or
educational handout containing several already-tested features. Integrated
documents test ecological validity; they do not replace atomic fixtures for
causal attribution. Their ground truth must reference the same component
contracts and must be frozen separately.

## Avoided inflation

Do not count cosmetic changes, repeated copies of the same sentence, or
converter-specific duplicates as independent instances. A new instance must
change the semantic boundary being tested or improve coverage of a realistic
authoring pattern.
