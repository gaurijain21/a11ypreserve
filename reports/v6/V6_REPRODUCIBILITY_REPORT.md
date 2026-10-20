# V6 reproducibility report

## Executed checks

| Check | Status |
|---|---|
| V6 control rerun computes all 65 controls | PASS: 65/65 |
| V6 mutation sensitivity rerun | PASS: 65 attempts; 59 valid applied |
| V6 executable baseline/ablation run | PASS: 130 primary cases; 59 known faults |
| V6 regression tests | PASS: standalone scientific regression assertions; `pytest` is not installed in this environment |
| Historical V4/V5 denominators preserved | PASS by machine accounting in V6 records |
| External validator run (PAC/verapDF) | NOT RUN: tools unavailable |
| Google temporal rerun | NOT RUN: authenticated sessions and seven-day schedule unavailable |
| Natural external corpus | NOT RUN: rights-cleared corpus unavailable |
| Current V6 manuscript compile | PASS: 9-page IEEE letter PDF generated; references resolved; all nine pages rendered and visually inspected |

V6 records Python, OS, pypdf, and PyMuPDF versions for each executed run. Exact package versions are pinned in `requirements-v6.txt`; a future release can add wheel hashes for fully offline installation. The static V6 package manifest verifies listed file sizes and SHA-256 hashes, and `.github/workflows/v6.yml` runs the scientific computations rather than only checking pre-existing JSON. Existing V4 manifests retain converter/browser/producer/timestamp/output-hash provenance. The package contains no credentials, cookies, tokens, or private browser data. The V6 source-to-PDF record is `experiments/v6/V6_PDF_BUILD_PROVENANCE.json`; it records source-input hashes, compiler commands and versions, PDF hash/size/page count, and final log diagnostics. The static manifest includes the compiled PDF, bibliography, and IEEE class/style files.

## Remaining infrastructure work

Remaining reproducibility work is wheel-hash locking for fully offline installation. External GUI/cloud reproduction is documented as an authenticated offline path and cannot be honestly run in ordinary CI. The local build required an elevated MiKTeX invocation because the ordinary process could not access the existing MiKTeX registry/configuration; this environment-specific requirement is recorded rather than hidden.
