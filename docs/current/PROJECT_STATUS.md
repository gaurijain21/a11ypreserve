# Current project status

The current submission state is the 52-case atomic V3 benchmark documented in `CANONICAL_SUBMISSION_STATE.md`. The repository has a verified manuscript PDF and a self-checking review artifact. The scientific claim is intentionally narrow: selected machine-verifiable accessibility semantics are tested for preservation across two named DOCX-to-PDF conditions, with abstention when semantic equivalence is not established.

The evidence is internally consistent under `tools/audit_submission_consistency.py`. The main remaining risks are limited corpus breadth, incomplete destination oracles for 18 atomic rows, opaque/version-variable Google infrastructure, no Word arm, no reading-order arm, no naturally sampled real-world corpus, and no disabled-user study.
