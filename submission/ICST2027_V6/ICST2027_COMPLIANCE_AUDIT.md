# ICST 2027 Research Papers compliance audit

Checked 2026-10-19 against the official ICST 2027 Research Papers page:
<https://conf.researchr.org/track/icst-2027/icst-2027-research-papers>.
The page is the authoritative source used for this audit; HotCRP metadata and
author declarations still require a human check.

| Requirement | Official rule or source | Current status | Required action |
|---|---|---|---|
| Track | ICST 2027 Research Papers | PASS: manuscript is prepared for this track | Author selects the track in HotCRP |
| Scope | Research track accepts novel research, empirical, case-study and replication work; accessibility testing is listed among topics | PASS: topic fit is plausible and bounded | Author confirms final positioning |
| Format | Two-column IEEE conference publication format, letter template, conference option | PASS: current PDF is IEEE two-column, US letter | Recheck HotCRP-generated metadata |
| Page limit | No more than 10 pages including text, figures, tables and appendices; up to 2 additional reference-only pages | PASS: current PDF is 9 pages and needs no extra reference pages | No action unless manuscript changes |
| Review anonymity | Double-blind; omit names; prior work in third person; artifacts and replication packages must also be anonymized | PASS by automated checks, pending author inspection | Inspect exact ZIP and HotCRP fields before upload |
| Replication material | Submission is expected to include or point to an anonymized package with software, data and instructions | PASS with stated environment limits | Author confirms package choice and upload fields |
| Submission platform | HotCRP at <https://icst2027.hotcrp.com/> | NOT PERFORMED by design | Author must upload only after approval and explicit authorization |
| Full-paper deadline | 2 November 2026, AoE (UTC-12) | VERIFIED from official page | Author must meet the deadline |
| Abstract deadline | No separate abstract-registration date is listed on the checked page | UNKNOWN | Author must check HotCRP if a separate field/date appears |
| AI assistance | Generative AI is permitted; authors remain responsible; AI-generated text, figures, images and code must be disclosed in anonymized acknowledgments with tools, affected sections and extent; references must be verified | PASS in manuscript draft, pending author approval | Author confirms disclosure and reference verification |
| Originality and concurrent submission | IEEE plagiarism/authorship policies are linked; paper must not be published or under review elsewhere | REQUIRES AUTHOR CONFIRMATION | Author completes originality and concurrent-submission declarations |
| Licensing and artifact terms | No specific paper/artifact license rule was stated on the checked research-track page | UNKNOWN | Author resolves license and rights decisions; do not add identity-bearing metadata pre-review |
| Supplementary-material size/link rules | No separate size or external-link rule was stated on the checked research-track page | UNKNOWN | Author checks current HotCRP fields and any artifact-track instructions |
| Major revision | Official page describes a possible five-week revision, marked-changes paper and author response | INFORMATIONAL | Not applicable to initial submission |

## Current manuscript checks

- `submission/ICST2027_V6/main.pdf`: 9 pages, 612 x 792 points, IEEE two-column
  layout.
- The current source uses `Anonymous for review` and contains no author list,
  affiliation, acknowledgments, or private repository URL.
- The PDF metadata and archive scan were checked separately; see
  `FINAL_ANONYMITY_AUDIT.md`.
- The archive contains a sanitized replication package and explicit notes that
  Google Docs requires an authenticated interactive environment.
- The manuscript does not claim PDF/UA conformance, natural-document
  generalization, human usability, or temporal Google repeatability.

## Compliance verdict

The technical candidate is **READY FOR AUTHOR SIGN-OFF**, not ready for
submission. Author-controlled identity, originality, conflict, licensing,
rights, AI-disclosure approval, and HotCRP metadata remain gates. No submission
or upload was performed by this audit.
