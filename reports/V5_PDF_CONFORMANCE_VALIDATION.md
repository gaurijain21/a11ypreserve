# V5 PDF conformance validation

Status: **experimentally unresolved; no conformance claim is made**.

The environment was checked for veraPDF and PAC before finalization. Neither
validator was available for deterministic execution in this run. The existing
LibreOffice flags (`UseTaggedPDF` and `PDFUACompliance`) and the observed
`/StructTreeRoot` markers are export settings and structural observations;
they are not a standards-conformance verdict. The V5 profile comparison also
reports zero raw PDF/A markers for condition B without treating that as proof
of PDF/A or PDF/UA status.

Required future protocol: pin the validator name and version, run the same
validator configuration over every primary and supplementary PDF, retain raw
reports and exit codes, record profile/standard selection, and report
validator failures separately from A11yPreserve semantic classifications. A
validator result must never be used to relabel a source-preservation outcome.
