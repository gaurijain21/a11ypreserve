# Cross-converter mutation results

Status: COMPLETED AND VERIFIED as a bounded archived-output diagnostic.

The audit selected one existing variant per family from each of LibreOffice,
Google Docs, and Microsoft Word outputs: 39 archived PDFs. It applied raw
destination mutations without rerunning a converter. There were 31 applied and
valid mutations, 30 direct Tier-A contract faults, and 25 coarse-comparator
detections. Eight operators were not applicable on the selected archived
outputs; one applied Google document-metadata rewrite did not meet the source
title equality rule and is retained as non-scorable.

This result is descriptive, not a converter ranking and not stage-level fault
localization. Google remains an end-to-end import/export condition. No claim is
made that a mutation response isolates import, internal representation, PDF
generation, or extraction.

Raw per-case evidence and hashes are in
`experiments/v8/V8_CROSS_CONVERTER_MUTATIONS.json` and
`experiments/v8/cross_converter_mutation_cases/`; the executable protocol is
`scripts/v8_cross_converter_mutation.py`.
