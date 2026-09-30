# Related-Work Positioning

## Accessibility-aware document conversion

Roig and Ribera study office-to-EPUB accessibility conversion. This supports the importance of accessibility-aware transformation, but differs in destination format, workflow, and source-grounded DOCX-to-PDF comparison.

## Accessible representation generation and remediation

SciA11y converts scientific papers to accessible HTML; iTagPDF uses document cues and visual PDF analysis to automate PDF tagging and related metadata. These primarily create or improve an accessible destination. A11yPreserve measures whether known author-provided source information survives an existing pipeline.

## PDF conversion and fidelity benchmarks

DAISY's benchmark and the DocAccessible research program address conversion quality or fidelity in adjacent settings. A11yPreserve narrows the unit to controlled DOCX source properties and paired destination PDF representations.

## PDF accessibility evaluation

Kumar, Padath, and Wang benchmark automated and LLM-based PDF accessibility evaluation. That work asks how well evaluators assess destination PDFs. A11yPreserve asks whether source accessibility information was preserved. The paper should not present validators as ground truth for preservation.

## Standards context

ATAG 2.0, Section 508, and EN 301 549 explicitly motivate preservation of accessibility information during transformation when destination mechanisms support it. A11yPreserve operationalizes that concern as a reproducible source/destination comparison.

The paper should avoid claiming that no prior work has studied accessibility preservation.
