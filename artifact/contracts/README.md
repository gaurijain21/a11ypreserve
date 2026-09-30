# A11yPreserve preservation contracts

Each JSON contract defines the machine-verifiable accessibility information
present in one frozen DOCX source, the destination representation accepted as
equivalent, and the feature-specific decision and uncertainty rules. The
contracts are source-grounded; they are not claims of complete document
accessibility or PDF/UA conformance.

The included frozen corpus is `F01`–`F12` and `F14`. `F13` was reserved for
reading order but deferred because reliable automated source-to-PDF equivalence
could not be established. It is intentionally not represented as an included
fixture contract.

The source `sha256` and `manifest_sha256` fields bind each contract to the
frozen evidence. `source.oracle` identifies the independent raw-OOXML audit;
the source extractor agreement is a cross-check, not an independent human
validation claim.
