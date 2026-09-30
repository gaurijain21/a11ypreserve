# Novelty Defense

## Closest prior art

The closest current overlap is the DAISY AI SIG's 2026 benchmark of seven services converting PDFs into accessible documents, and DocAccessible's current PDF-to-HTML fidelity benchmark with source/conversion hashes and review evidence. Earlier adjacent work includes Roig/Ribera's office-to-EPUB accessibility work, SciA11y's PDF-to-accessible-HTML conversion, iTagPDF's source-aware PDF remediation, and PDF accessibility-evaluation benchmarks such as Kumar, Padath, and Wang.

## Exact overlap

These efforts overlap in caring about accessibility during transformation, source comparison, conversion fidelity, or destination structure. DAISY and DocAccessible also use controlled evidence and source-oriented review. The paper must therefore avoid a broad claim that source-grounded accessibility conversion evaluation is new.

## Exact difference

A11yPreserve starts with native DOCX documents whose target accessibility properties are machine-verified in manifests, OOXML, and ASIR; sends identical frozen sources through two real DOCX-to-PDF pipelines; extracts PDF structure; and compares destination representations against source contracts. The primary question is preservation of known author-provided accessibility information, not creation/remediation of an accessible destination, PDF-to-HTML fidelity, or accuracy of a destination-only evaluator.

## Claims we can make

- A11yPreserve presents a scoped source-grounded DOCX-to-PDF preservation measurement design.
- The benchmark demonstrates feature-specific and pipeline-specific outcomes under frozen inputs and named conditions.
- The method separates preservation fidelity from the broader question of destination accessibility.

## Claims we cannot make

We cannot claim to be the first preservation benchmark, to cover document conversion generally, to subsume DAISY or DocAccessible, or to establish ecosystem-wide converter behavior. The manuscript's current modest-gap wording is retained.

Focused search date: 2026-09-27. Search was targeted rather than a replacement for a systematic literature review.
