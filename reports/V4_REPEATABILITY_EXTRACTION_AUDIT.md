# V4 Repeatability Extraction Audit

This is a derived diagnostic audit. The frozen repeatability classifications and primary results are unchanged.

## Summary

| Pipeline | Byte-identical | Raw extraction-identical | Normalized semantic-identical | Classification-stable |
|---|---:|---:|---:|---:|
| LibreOffice | 0/6 | 0/6 | 6/6 | 6/6 |
| Google Docs | 6/6 | 0/6 | 6/6 | 6/6 |

## Cause of the Google anomaly

The Google repeated PDFs have identical SHA-256 hashes and file lengths within each fixture. Raw `pdf_extract` identity was 0/6 because the extracted records include execution/provenance data: output source paths, extraction source paths, PDF hashes, and pypdf object string representations containing a process-memory address. The PDFs themselves are byte-identical, so these differences are not semantic differences in the PDF.

The normalization removes path/extraction provenance and PDF hash fields and replaces only the process-memory address portion of `IndirectObject(...)` strings. After normalization, semantic extraction identity is reported separately from raw extraction identity.

## LibreOffice

LibreOffice byte differences are retained as genuine output-level variation. The audit compares fresh extraction, PDF metadata, structure records, and normalized semantics. Any remaining normalized differences are reported in the machine-readable artifact rather than silently treated as semantic instability.

Machine-readable evidence: `experiments/v4/conversions/V4_REPEATABILITY_NORMALIZED.json`.
