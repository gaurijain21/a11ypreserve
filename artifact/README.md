# A11yPreserve artifact candidate

A11yPreserve is a controlled, contract-based, uncertainty-aware method for testing whether machine-verifiable accessibility information present in a DOCX survives DOCX-to-PDF conversion. The artifact supports the frozen paper's source-grounded comparison protocol; it is not a general PDF accessibility validator and does not measure disabled-user usability.

## What is included

- `corpus/fixtures/`: the 13 frozen atomic DOCX source fixtures, using F01--F12 and F14. F13 was reserved for reading order and deferred because reliable automated source-to-PDF equivalence could not be established.
- `corpus/outputs/`: the 26 frozen genuine outputs from LibreOffice and the Google Docs DOCX-to-PDF conversion pipeline.
- `corpus/evidence/`: source certificates, output evidence, and parser/partial-case evidence used by the paper.
- `contracts/`: machine-readable feature contracts.
- `src/`: the extractor, comparator, independent OOXML source oracle, output checks, and parser support used for verification.
- `tests/`: focused comparator and frozen-experiment checks.
- `results/`: the final evidence-aware primary result and interpretation changelog.
- `corpus/evidence/loss/`: the two confirmed-loss certificates and supporting evidence.
- `results/COMPARATOR_CALIBRATION.json`: the synthetic comparator-calibration record, kept separate from the primary benchmark.
- `integrated_study/`: the separate three-document sanity check. Its 42 property--pipeline observations are not part of the primary 26-case denominator.

## Frozen primary benchmark

The primary unit is one fixture/converter pair: 13 fixtures x 2 pipelines = 26 cases. The final evidence-aware results are 11 VERIFIED PRESERVED, 3 OBSERVED PARTIAL, 3 ALTERED, 2 CONFIRMED LOST, 6 UNRESOLVED EQUIVALENCE, and 1 MEASUREMENT ERROR. The two confirmed losses are F06 inline language and F11 footnote association in the Google Docs pipeline. Historical V1 counts remain archived in the paper and changelog and are not the current headline result.

## Requirements

- Python 3.11 or newer.
- Python packages used by the verification scripts: `python-docx`, `beautifulsoup4`, `pypdf`, and `PyMuPDF`.
- LibreOffice 26.2.6.3 with the recorded PDF export settings is needed for a Level 2 reconversion; the frozen PDFs are already included.
- Poppler `pdftotext` is an optional secondary extraction check.

Install the Python dependencies with `python -m pip install -r requirements.txt`. Package versions were not used to redefine the frozen evidence; pin them in an environment lock file before a long-term public release.

## Reproducibility levels

### Level 1 -- verify existing evidence

The included files allow hash checking, contract inspection, extractor reruns, and result-report inspection. Start with the frozen manifests and `results/FINAL_EVIDENCE_AWARE_RESULTS.md`.

Example comparator invocation from the artifact root:

```powershell
python src/a11ydiff.py corpus/fixtures/F06_INLINE_LANGUAGE.docx corpus/outputs/google_docs/F06_INLINE_LANGUAGE__GOOGLE_DOCS.pdf inline_language
```

The exact output filename can be confirmed with `Get-ChildItem corpus/outputs/google_docs`.

### Level 2 -- reproduce LibreOffice conversion

Repeat the recorded headless LibreOffice conversion using the exact fixture, version, and settings documented in the paper and evidence records. Compare the resulting PDF hash and structure with the frozen output. A changed hash is not by itself a classification change; rerun the evidence checks and treat the result as a new observation.

### Level 3 -- repeat the Google Docs workflow

The workflow can be repeated by uploading the exact fixture to Google Docs and using File -> Download -> PDF Document. The backend version cannot be fully pinned, so cloud behavior may change. The package contains the frozen outputs and recorded workflow metadata but does not contain authentication state, cookies, browser profiles, or private credentials.

## Verifying fixture hashes

Compare the SHA-256 values in `corpus/FROZEN_CORPUS_MANIFEST.json` and the evidence records with a local hash tool. For example:

```powershell
Get-FileHash corpus/fixtures/F06_INLINE_LANGUAGE.docx -Algorithm SHA256
```

The publication copy replaces private machine paths with `<ARTIFACT_ROOT>`; this does not change binary fixture or PDF contents.

## Inspecting contracts and rerunning analysis

Open the JSON files under `contracts/` to see the property-specific source and destination expectations. The source-grounding chain is the source manifest, raw OOXML inspection, and source-extractor agreement, supplemented by separately implemented raw-OOXML source-oracle certificates. From the artifact root, run `python src/independent_source_oracle.py`; it checks all 13 source fixtures and writes its report to `results/INDEPENDENT_SOURCE_ORACLE.json` and certificates to `corpus/evidence/source/`. Run `python src/verify_corpus_ooxml.py` for the focused OOXML checks. Run focused tests from the artifact root after installing dependencies; some historical tests refer to the frozen result layout and are intended as verification aids rather than a turnkey experiment driver.

## Supplying an output from another pipeline

Place a new PDF outside the frozen `corpus/outputs/` tree, keep the original DOCX fixture unchanged, and invoke `src/a11ydiff.py` with the source and new PDF paths. Preserve the pipeline name, software version, settings, date, output hash, and evidence report. Do not merge new observations into the paper's frozen denominator without a separately documented study revision.

## What cannot be perfectly reproduced

The Google Docs backend is cloud-versioned and cannot be fully pinned. Browser and workflow details were recorded, but a rerun may differ after a service update. PDF cross-format equivalence is feature-specific; absence from one extracted encoding is not automatically proof of semantic absence. The study also does not provide a screen-reader or disabled-user task evaluation.

## Known limitations

The corpus is a controlled set of 13 atomic fixtures, not a representative sample. Features have unequal complexity, percentages are descriptive only, and no inferential or population-level claims are justified. The results concern machine-verifiable source information and tested destination structure under two named pipelines; they do not establish overall PDF accessibility, converter superiority, general DOCX behavior, or user harm.

## Review-package status

This is a sanitized candidate package for venue submission. It contains no browser authentication state or credentials. The license and author metadata require a human decision before public release; see `LICENSE`, `CITATION.cff`, and the accompanying submission license report.
