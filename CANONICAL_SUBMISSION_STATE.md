# Canonical submission state

This is the single current account of the A11yPreserve submission state. It supersedes contradictory pre-V3 readiness notes. Historical records remain recoverable and are not rewritten.

## Canonical experiment

- Feature families: 13 selected families (`F01`–`F12` and `F14`); F13 reading order is explicitly deferred.
- Controlled fixtures: 13 Core fixtures plus 13 pre-specified Variant B fixtures = 26 DOCX fixtures.
- Converters: LibreOffice `26.2.6.3` with recorded tagged/PDF-UA settings; the recorded authenticated Google Docs DOCX-to-PDF workflow. Microsoft Word is excluded.
- Primary cases: 52 fixture–pipeline rows, 26 per pipeline, with Core and Variant B kept identifiable.
- Outcomes: 18 `VERIFIED_PRESERVED`, 4 `OBSERVED_PARTIAL`, 7 `ALTERED`, 4 `CONFIRMED_LOST`, 18 `UNRESOLVED_EQUIVALENCE`, and 1 `MEASUREMENT_ERROR`.
- Confirmed-loss identities: Core/Variant B inline-language and footnote-association rows under Google Docs; claims are limited to the contracted machine-verifiable destination representation.

## Supplementary evidence

- Historical Core: 26 rows, unchanged; 11 preserved, 3 partial, 3 altered, 2 confirmed lost, 6 unresolved, 1 measurement error.
- Calibration: 27 diagnostic controls: 12 correct determinate, 6 correctly unresolved, 0 false positives, 2 false negatives, 7 other unresolved/indeterminate. This is diagnostic calibration, not a sensitivity or specificity estimate.
- Repeatability: 13 Core fixtures × 3 Google runs = 39; classifications stable 13/13 and byte-identical PDFs 13/13 under the recorded workflow.
- Integrated sanity arm: 3 project-generated multi-feature documents, 21/21 source assertions, and 42 property–pipeline observations; excluded from the atomic denominator.
- Variant C: not completed. No Variant C output is claimed; the untouched-holdout protocol remains future work.
- Word: not added. Word was installed, but COM activation failed with `0x80070520`; no Word PDF was produced.
- Reading order: not added. No defensible automated contract was established.
- Realistic/external-validity arm: not added as a real-world corpus. The integrated arm is explicitly synthetic and secondary.

## Current authoritative files

- Machine-readable primary record: `results/V3_PRIMARY_RESULTS.json`.
- Generated consistency report: `reports/FINAL_CONSISTENCY_AUDIT.md`.
- Current manuscript: `submission/ICST2027_V3/main.tex` and verified PDF `submission/ICST2027_V3/main.pdf`.
- Review artifact: `artifact_v3/`.
- Source contracts: `contracts/`.
- Historical evidence: `results/full_experiment/`, `paper/`, `pilot/`, `pilot2/`, `pilot3/`, and older root-level freeze/readiness records.

The V3 record, manuscript, and artifact use the same 52-row denominator. Root-level documents that describe only the 26-row Core experiment are historical snapshots and must not be cited as the current submission state.
