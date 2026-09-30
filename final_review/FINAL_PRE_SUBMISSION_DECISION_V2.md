# READY FOR SUBMISSION TARGETING

## Final title

**A11yPreserve: An Uncertainty-Aware Conformance Suite for DOCX-to-PDF Accessibility Preservation**

## Contribution

A controlled source-to-destination preservation protocol with versioned source
contracts, an independent raw-OOXML source oracle, calibrated differential
comparison, two-path destination evidence, and reproducible provenance.

## Empirical scope

13 controlled atomic DOCX fixtures, F01–F12 and F14, converted to 26 genuine
outputs through LibreOffice and the Google Docs DOCX-to-PDF conversion pipeline.
The unit is one fixture/converter pair; counts and feature matrices are
descriptive, not inferential.

## Oracle

13/13 source contracts pass independent ZIP/XML verification and agree with the
frozen manifests and ASIR. ASIR is disclosed as implementation-grounded, not
independent human validation.

## Calibration

27 synthetic controls expose conservative unresolved/false-negative behavior in
some alternate representations and no false positives in this diagnostic set.
The paper does not present these counts as comparator accuracy estimates.

## Partial and unresolved cases

All nine frozen partial outcomes remain unchanged. Three are observed partials;
six are unresolved equivalence. This distinction is now explicit in the results
table and evidence-status freeze.

## Losses

F06/Google Docs inline language and F11/Google Docs footnote association remain
confirmed contract-level losses with independent parser/object corroboration.
F11/LibreOffice remains measurement error.

## Integrated sanity status

Not performed. External-validity risk remains HIGH and is explicitly stated.
This does not prevent the bounded protocol claim; integrated documents are future
work before generalization.

## Closest prior art

Roig/Ribera's office-to-EPUB accessibility conversion work is the closest
conceptual precedent. DAISY and DocAccessible are important current benchmark
threats; SciA11y and iTagPDF address destination generation/remediation; Kumar et
al. address destination-only evaluation. The paper acknowledges all of these.

## Novelty boundary

No first/unique/no-prior-work claim is made. The contribution is the controlled
source-contract, identical-input, uncertainty-aware DOCX-to-PDF preservation
protocol and empirical benchmark.

## Limitation

The study does not measure complete PDF accessibility, screen-reader usability,
task completion, perceived accessibility, user harm, all DOCX documents, all
software versions, or isolated Google import/export stages.

## Artifact readiness

The contracts, independent certificates, calibration report, triangulation
report, evidence-status freeze, changelog, conformance-suite interface, and
prior-art comparison are present. No frozen fixture, PDF, manifest, hash, or
primary classification was changed.

## Venue

Target DocEng first; consider ASSETS with the same narrow framing.

## Remaining fixes

Before public artifact release, sanitize any pre-existing frozen JSON/report
paths and verify licensing/provenance of every bundled source and output. This is
packaging work, not a scientific blocker.

## Recommendation

Proceed toward submission targeting with narrow claims. Do not submit it as a
general accessibility validator, universal conversion law, converter ranking, or
disabled-user impact study.
