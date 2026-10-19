# V5 gap-closure report

This report records what was fixed and what remains open. No unresolved item
is represented as a completed experiment.

## Fixed

| Issue | Closure |
|---|---|
| Aggregate holdout arithmetic | Machine-derived 130 = 52 holdout + 78 non-holdout audit; manuscript labels the holdout as within-family/within-variant. |
| Manifest ambiguity | Paper and README state that each 75-record primary manifest contains 65 atomic plus 10 realistic integrated records. |
| Diagnostic overclaim | “Independent technical validation” is replaced with “independent diagnostic cross-check”; the paper reports 8/26 agreements and 18/26 disagreements. |
| Destination mutation narrowness | Operators now run across all 65 atomic variants with explicit no-op controls; survivors, unsupported attempts, and measurement errors remain visible. |
| Measurement-boundary ambiguity | Semantic preservation, serialization identity, PDF/A/PDF/UA conformance, and human usability are separated in the paper. |
| Historical path leakage | Tracked text artifacts were sanitized; a repository safety audit and secret scan now fail on recurrence. |
| Reproducibility navigation | Root requirements, one-command checks, bundle verification, CI, and V5 release documentation were added. |
| PyMuPDF deprecation | Active Python evidence paths use the supported `pymupdf` import. |

## Experimentally unresolved

| Issue | Current status and exact protocol needed |
|---|---|
| Standards conformance | veraPDF and PAC were unavailable. Pin one validator/version and profile, run every PDF, retain raw reports and exit codes, and report conformance separately from semantic preservation. See `reports/V5_PDF_CONFORMANCE_VALIDATION.md`. |
| Natural-document validation | No rights-cleared natural corpus was available. Assemble 20--30 public or author-permitted DOCX files, record provenance and redistribution rights, have two independent reviewers verify the source contracts before conversion, stratify by document type, and keep the corpus out of the frozen primary denominator. |
| Time-separated Google testing | Run the same pre-registered 26 holdout cases in two sessions separated by at least seven days, with fresh browser sessions, recording date, browser build, producer, source/output hashes, normalized evidence, and classifications. Compare session-level classification stability without pooling cloud versions. |
| Human usability | Recruit participants who use assistive technology or accessibility features, obtain ethics/consent approval, blind the converter labels, define document-navigation and information-retrieval tasks before viewing results, measure completion, errors, time, and reported difficulty, and analyze outcomes separately from machine preservation labels. |
| External expert adjudication | Have at least two qualified accessibility/PDF-structure reviewers independently adjudicate a blinded sample of source contracts and destination evidence using a versioned rubric; report agreement and disagreements, then freeze any comparator revision before rerunning affected rows. |

## Requires human decision

| Issue | Decision required |
|---|---|
| Public license | Select compatible code, data, document, and fixture redistribution terms after checking author rights, third-party assets, Google/Word terms, and venue artifact policy. Root `LICENSE` is an explicit placeholder. |
| Citation metadata | Replace the anonymous author placeholder and confirm title, version, date, repository URL, and license in `CITATION.cff` when public attribution is permitted. |
| Portal submission | Complete HotCRP authors/COI, originality and simultaneous-submission declarations, artifact access/license settings, and final portal-render inspection. |

## Future work

- Expand destination mutation operators to additional object locations and
  multi-mutation interactions after a new frozen comparator version.
- Add standards-validator reports and temporal cloud evidence when the required
  environments and authorized sessions are available.
- Extend the source-contract vocabulary to reading order only after a
  defensible source/destination oracle is established.
- Reassess all manuscript and bundle numbers after any new evidence arm; do not
  append new observations to the frozen primary denominator retroactively.
