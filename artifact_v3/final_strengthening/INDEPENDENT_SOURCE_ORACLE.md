# Independent source-oracle audit

Status: **PASS — 13/13 included frozen fixtures independently checked.**

The audit uses `scripts/independent_source_oracle.py`, a separate implementation
that reads the DOCX ZIP package directly with `zipfile` and
`xml.etree.ElementTree`. It does not import the ASIR source extractor, the
fixture generator, the manifest-generation code, or the comparator. The audit
checks feature-specific OOXML parts and elements, compares them with the frozen
source manifests, and writes one certificate per fixture under
`evidence/source/`.

The source ground truth is therefore established by three linked artifacts:

1. the frozen source manifest;
2. direct raw-OOXML inspection by the independent oracle; and
3. agreement with the implementation-grounded ASIR source extractor.

This is not independent human expert validation, and the independent oracle is
not a second accessibility interpretation of every contract. It is an
independent package/XML measurement path that reduces the risk of a shared
extractor bug. A future release should add a second human or standards-based
review if the contracts are extended to less atomic source cases.

F13 is absent by design: it was reserved for reading order but deferred because
reliable automated source-to-PDF equivalence could not be established.
