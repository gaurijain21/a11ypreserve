# V5 reading-order feasibility

## Decision: NO-GO for the primary benchmark

Reading order remains an explicit deferred attribute. The source can expose
paragraph order in `word/document.xml`, but floating objects, text boxes,
anchoring, headers/footers, tables, multi-column layout, and drawing order do
not yield one unambiguous intended logical reading order without layout and
author-intent assumptions. PDF extraction also has multiple orderings
(structure tree, marked content, page geometry, and viewer/AT order).

Simple paragraphs could be bounded, but a family-level oracle that covers the
important DOCX layout constructs would require arbitrary human judgments or a
new independently validated layout model. The evidence package has no such
model. Adding reading order now would weaken, rather than strengthen, the
source-grounded preservation claim. It is therefore deferred with a concrete
future GO gate: objective source intent, reliable destination extraction,
accepted equivalent orderings, and mutation/calibration evidence.
