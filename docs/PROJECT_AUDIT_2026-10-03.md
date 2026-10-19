# A11yPreserve project and paper audit — 2026-10-03 (pre-final-PDF snapshot)

> This document records the state before the final V3 PDF build. The superseding readiness record is `docs/FINAL_V3_SUBMISSION_READINESS.md`.

## Executive verdict

The V3 scientific story is defensible and substantially stronger than the V2
candidate, but the project is not submission-ready yet. The remaining blockers
are release integrity and submission verification, not a need to invent a new
headline result:

1. Compile and visually inspect the unchanged V3 manuscript in a trusted
   IEEEtran environment. No verified V3 PDF currently exists.
2. Keep V3 as the only canonical manuscript. Do not accidentally submit the
   older 26-case `paper/` copy.
3. Use the repaired and self-checking `artifact_v3` package for replication.
4. Choose code/data/document licenses and verify fixture-asset provenance.
5. Re-run the double-anonymity and archive scans after final packaging.

## What passed in this audit

- Python compilation passed for the artifact scripts.
- The frozen Core raw-OOXML source oracle passed 13/13 fixtures.
- The Variant B raw-OOXML source oracle passed 13/13 fixtures.
- Comparator tests passed 17 cases.
- Core Google repeatability passed 13/13 byte-identical checks across 39 PDFs.
- The repaired public-artifact self-check passed all 52 result rows, source and
  destination hashes, provenance links, repeatability outputs, and path
  sanitization.
- The machine-readable V3 counts sum correctly to 52:
  18 preserved, 4 partial, 7 altered, 4 lost, 18 unresolved, 1 measurement
  error.
- The official ICST research-track page confirms the 2 November 2026 deadline,
  10 content-page limit plus up to two reference-only pages, IEEE two-column
  format, double-blind review, anonymized replication material, and AI-use
  disclosure requirements.

## Findings that could kill the submission

### Critical: no final V3 PDF

`submission/ICST2027_V3/FINAL_PACKAGE_DECISION.md` is correct: no valid V3
PDF, page count, font-embedding check, PDF metadata record, or final visual QA
record exists. The V2 rendered pages are not a substitute for the V3 source.

### Critical: manuscript ambiguity without a canonical path

The repository contains both a V2 26-case manuscript and a V3 52-case
submission. This is now documented in the root README, but the release process
must still copy only the V3 source into the upload package.

### High: ICST testing contribution remains domain-specific

The paper now makes the testing mapping explicit: contracts are oracles,
fixtures are inputs, pipelines are systems under test, extraction supplies
observations, and abstention is an oracle decision. A hostile reviewer can still
argue that the contribution is a DOCX-specific harness rather than a broader
testing advance. The best defense is precise wording plus the existing
feature/representation/evidence coverage matrix; do not claim a universal
testing theory.

### High: small purposive suite and unresolved outcomes

There are two controlled instances per selected family, not a representative
sample. Eighteen of 52 rows are unresolved equivalence, and calibration records
two false negatives plus seven unresolved/indeterminate controls. This is a
real utility limitation. Keep the abstention category and report the counts;
do not convert unresolved rows into losses to make the result look stronger.

### High: cloud workflow and route deviation

Google Docs is cloud-versioned. Variant B outputs were obtained through the
authenticated in-session export backend after visible downloads did not
register. The manuscript discloses this, but it prevents a stronger claim that
every arm used one identical UI path or that the result identifies a particular
internal Google stage.

### High: footnote representability attack

The Google F11/B11 loss certificates are strong for serialized absence, but a
reviewer can ask how “representable” was established when the LibreOffice
footnote association is itself unresolved in one Core case and one Variant B
case. Keep the claim narrowly phrased as absence of the required
machine-verifiable association in the tested Google outputs, not as a universal
statement about PDF capability.

### High: no external reproduction

The package is internally cross-checked, but no independent third-party run is
recorded. The new self-check makes this easy to attempt; it does not create
external validation. Treat third-party reproduction as the highest-value
post-submission extension.

### Administrative: GitHub is not connected

The local repository has no configured Git remote, and only the original
22-file skeleton is tracked; the substantive paper, artifact, and audit work is
currently uncommitted. Do not push blindly. First decide whether to submit
anonymously, select the public release boundary, add authorship/license
metadata, commit a clean snapshot, and then configure the intended remote.

### Administrative: public release rights are incomplete

The candidate artifact explicitly lacks a final redistribution license. Image
provenance, third-party runtime material, and any included generated documents
must be checked before a public GitHub release.

## Highest-value improvements

1. Produce and inspect the V3 PDF; freeze its hash, page count, fonts,
   metadata, and visual-QA result.
2. Add a clean anonymous archive manifest containing exactly the V3 source,
   artifact candidate, and required license/provenance records.
3. Obtain one independent clean-machine artifact run or a reviewer-friendly
   container/lockfile path.
4. Add a concise fault-model/adequacy table to the paper or artifact README:
   deletion, mutation, structural substitution, and association/scope errors,
   each linked to the selected feature contracts and evidence paths. This
   strengthens the ICST test-design framing without changing the frozen data.
5. After the submission, add a third converter and a user/assistive-technology
   study as separate extensions. Neither should be smuggled into the current
   claims.

## Do not do

- Do not submit the V2 PDF or V2 manuscript under the V3 claims.
- Do not publish an identity-bearing GitHub URL in a double-blind submission.
- Do not report unresolved equivalence as confirmed loss.
- Do not call the tool a complete PDF accessibility validator.
- Do not claim Google Docs or LibreOffice is globally better or worse.
- Do not change frozen classifications merely to improve headline counts.
