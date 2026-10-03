# A11yPreserve

A11yPreserve is a source-grounded, uncertainty-aware testing protocol for
measuring whether machine-verifiable accessibility information survives
DOCX-to-PDF conversion.

The canonical ICST 2027 research-paper candidate is the anonymous V3 source in
[`submission/ICST2027_V3`](submission/ICST2027_V3). The canonical replication
candidate is [`artifact_v3`](artifact_v3). The older V2 manuscript under
[`paper`](paper) is retained for provenance and is not the submission source.

## Current research snapshot

- 26 controlled DOCX fixtures: two controlled instances for each of 13 selected
  feature families.
- 52 fixture--pipeline cases across LibreOffice and the Google Docs DOCX-to-PDF
  conversion pipeline.
- Evidence-aware result counts: 18 verified preserved, 4 observed partial,
  7 altered, 4 confirmed lost, 18 unresolved equivalence, and 1 measurement
  error.
- A separate 39-run Google Core repeatability arm: all 13 fixture outputs were
  byte-identical across three recorded runs.
- A separate integrated sanity check: three project-generated multi-feature
  documents and 42 property--pipeline observations.

These are controlled-case observations, not prevalence estimates, a global
converter ranking, a complete PDF accessibility score, or a disabled-user
impact study.

## Verify the replication candidate

From `artifact_v3/`:

```powershell
python src/verify_public_package.py
python src/independent_source_oracle.py
python src/v3_difficult_variant_audit.py
python src/v3_finalize_repeatability.py
```

The standard-library self-check validates the result counts, frozen source and
PDF hashes, provenance links, repeatability outputs, and release-path
sanitization. The other commands rerun the source-oracle and stored evidence
audits. Google Docs reproduction requires an authenticated browser workflow;
credentials, cookies, and browser state are intentionally excluded.

## What makes the testing contribution distinct

The suite treats feature contracts as test oracles, controlled DOCX files as
test inputs, conversion pipelines as systems under test, PDF extraction as
observations, and evidence-aware rules as oracle decisions. When multiple PDF
representations are plausible but the evidence is insufficient, the oracle
abstains as `UNRESOLVED_EQUIVALENCE` instead of silently converting uncertainty
into a pass or failure.

## Release and anonymity status

The public candidate is prepared for review, but it is not a release-ready
public repository yet. Before public release, the authors must choose a license
for original code and documentation, verify the provenance and redistribution
rights of every fixture asset, and rebuild the final artifact archive.

For double-blind ICST review, do not link an identity-bearing GitHub repository
from the submission. Use an anonymized replication package and re-run the
anonymity scan after the final archive and PDF are created.

The V3 manuscript PDF is now compiled and verified at
`submission/ICST2027_V3/main.pdf`. The build record reports the hash, page
count, embedded-font check, metadata/anonymity scan, and visual inspection.
Human venue, authorship, license, and portal checks remain before upload.

## Repository map

| Path | Role |
|---|---|
| `submission/ICST2027_V3/` | Anonymous ICST V3 manuscript source and submission checks |
| `artifact_v3/` | Sanitized V3 replication candidate |
| `contracts/v3/` | Cross-format oracle and classification specifications |
| `corpus/`, `results/`, `v3/` | Frozen evidence and derived result records |
| `paper/` | Earlier V2 manuscript and rendered history |
| `research/`, `audit/`, `final_*` | Working research and hostile-review records |
