# A11yPreserve V5 baseline and change policy

Status: V5 hardening layer created 2026-10-06 (America/Los_Angeles).

## Frozen V4

The V4 evidence is preserved as historical provenance. The authoritative V4
controlled layer is `experiments/v4/`: 65 frozen DOCX fixtures, 13 families,
five variants per family, D/E holdout membership, source contracts, raw-OOXML
certificates, the frozen comparator, LibreOffice and Google Docs conversion
manifests/outputs, analysis records, realistic-arm records, calibration, and
repeatability evidence. The completed V4 primary denominator is 130 cases
(65 fixtures × 2 primary pipelines). The post-freeze Word arm is 65
supplementary atomic observations and is never pooled into that denominator.

V4's final paper and package remain under `submission/ICST2027_V4/`. The V4
final submission commit named by the project instructions is
`e881a7a3d2cd491bea1ecc7c422e6e4e3fdd8ec3`; the working tree also contained a
user-created untracked Word helper before V5 work began, and it is preserved.

## V5 changes

V5 is additive. New scripts, manifests, reports, machine-readable contracts,
mutants, and manuscript edits belong under `experiments/v5/`, `contracts/v5/`,
`scripts/`, `reports/V5_*.md`, and the V5 manuscript copy. V5 does not edit or
replace V4 fixture bytes, V4 expected labels, V4 output PDFs, V4 manifests, or
V4 analysis JSON.

The first V5 experimental condition addresses the documented LibreOffice
export-profile ambiguity. V4 used `SelectPdfVersion=1`, which authoritative
LibreOffice documentation/source identifies as PDF/A-1b. V5 condition B uses
`SelectPdfVersion=0` (documented default PDF 1.7) with
`UseTaggedPDF=true;PDFUACompliance=true`. Its outputs are separate and are
compared using the same source fixtures, contracts, extractor, and comparator.

## Supersession rule

V5 may supersede a V4 claim only when a new experiment is complete, its
provenance is recorded, its machine-readable results are validated, and the
manuscript labels the chronology explicitly. Until then, V4 numbers remain
the primary frozen evidence and V5 results are diagnostic or supplementary.

## Reproducibility rule

Every new result must record source hashes, condition settings, converter/build,
route, timestamps, output hashes, parser versions, and whether the result is
complete, partial, unsupported, or not run. Failed experiments and negative
results are retained. No V5 report may convert an unresolved or measurement
error into a confident label merely to improve a rate.
