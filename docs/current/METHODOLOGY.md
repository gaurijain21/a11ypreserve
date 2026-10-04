# Methodology

Each source DOCX is verified against a feature-specific contract using the frozen manifest, raw OOXML, and a separately implemented raw-OOXML oracle. The exact source is sent through a named conversion workflow. PDF evidence is extracted through the primary structural path and, for difficult cases, independent parser/object paths. A preservation label is issued only when the contract is supported; otherwise the procedure abstains as `UNRESOLVED_EQUIVALENCE` or records `MEASUREMENT_ERROR` when measurement itself fails.

The method measures preservation of selected source semantics. It is not a PDF/UA validator, a complete accessibility assessment, a screen-reader usability study, or a causal attribution of user harm.
