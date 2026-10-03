# Partial-case re-audit

The frozen primary category remains `PARTIALLY_PRESERVED` for all nine cases
listed below. This table adds an evidence-status overlay; it does not replace
the frozen outcome. `OBSERVED_PARTIAL` means the destination structure itself
shows a bounded partial representation. `UNRESOLVED_EQUIVALENCE` means that the
available destination evidence does not establish whether a feature-specific
equivalent representation exists. It is not evidence of converter-induced
semantic loss.

| Fixture | Converter | Original classification | Surviving evidence | Missing evidence | Independent evidence | Evidence status | Final classification |
|---|---|---|---|---|---|---|---|
| F01_HEADINGS | Google Docs | PARTIALLY_PRESERVED | Tagged PDF contains H1/H2/H3 structure | Source sequence is not reproduced; title/heading boundary is not isolated | pypdf structure traversal and PyMuPDF text/objects | OBSERVED_PARTIAL | PARTIALLY_PRESERVED |
| F03_LISTS | Google Docs | PARTIALLY_PRESERVED | L/LI nesting and item count survive | Ordered/unordered distinction is not exposed in the extracted destination structure | pypdf roles plus serialized-object scan; page text confirms list content | UNRESOLVED_EQUIVALENCE | PARTIALLY_PRESERVED |
| F07_DECORATIVE_IMAGE | LibreOffice | PARTIALLY_PRESERVED | Informative and decorative images are emitted as Figure elements | Decorative status is not represented as Artifact; alternative text is regenerated | pypdf and PyMuPDF object scans show Figure nodes and `/Alt` values | OBSERVED_PARTIAL | PARTIALLY_PRESERVED |
| F07_DECORATIVE_IMAGE | Google Docs | PARTIALLY_PRESERVED | Informative Figure `/Alt` survives; second Figure has empty `/Alt` | No Artifact/decorative representation is established | pypdf and PyMuPDF both show Figure, empty `/Alt`, no `/Artifact` | OBSERVED_PARTIAL | PARTIALLY_PRESERVED |
| F08_LINKS | LibreOffice | PARTIALLY_PRESERVED | URI link annotation survives | Visible name-to-link structural association is not recoverable | pypdf annotation traversal, PyMuPDF link API, serialized-object scan | UNRESOLVED_EQUIVALENCE | PARTIALLY_PRESERVED |
| F08_LINKS | Google Docs | PARTIALLY_PRESERVED | URI link annotation survives | Visible name-to-link structural association is not recoverable | pypdf annotation traversal, PyMuPDF link API, serialized-object scan | UNRESOLVED_EQUIVALENCE | PARTIALLY_PRESERVED |
| F10_COMPLEX_TABLE | Google Docs | PARTIALLY_PRESERVED | Table/TH structure and column-span evidence survive | Full multi-level header associations or scope are not established | pypdf attribute traversal and PyMuPDF serialized-object scan | UNRESOLVED_EQUIVALENCE | PARTIALLY_PRESERVED |
| F12_EQUATION | Google Docs | PARTIALLY_PRESERVED | Equation is visible in extracted page content | No machine-readable formula/token representation is established | pypdf structure traversal and PyMuPDF object/text scan | UNRESOLVED_EQUIVALENCE | PARTIALLY_PRESERVED |
| F14_CAPTIONS | Google Docs | PARTIALLY_PRESERVED | Caption text and a caption-like node/page-text evidence survive | Structural figure-caption association is not established by the available extraction | pypdf structure traversal and PyMuPDF text/object scan | UNRESOLVED_EQUIVALENCE | PARTIALLY_PRESERVED |

No partial case was reclassified as `MEASUREMENT_ERROR`. The only frozen
measurement-error case remains F11/LibreOffice. The evidence overlay is a
limitation disclosure and a reusable protocol field, not a post-hoc change to
the primary denominator.
