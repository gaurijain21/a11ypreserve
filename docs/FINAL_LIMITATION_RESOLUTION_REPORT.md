# 1. Starting baseline

- Pre-limitation-resolution freeze record: `docs/PRE_LIMITATION_RESOLUTION_FREEZE.md`.
- Clean Stage 1 freeze commit: `4b9e3cd3a08fe6a961b75f3cccb26964b074f247`.
- Audited submission-state commit immediately before the freeze record:
  `d361f99740a86cad15e4009282f7ee9a086405a3`.
- Manuscript SHA-256: `4F4CC53B5783ADEECF418B645EDDC16D39A7CD17144B8CD2A76D6A32D8B46285`.
- Artifact SHA-256: `B315C204C2E112909498B12D17F69B582ACA8813E8A9E42CC1E0E37D1EF08F49`.
- Frozen primary counts: 52 rows; 18 preserved, 4 partial, 7 altered, 4 lost, 18 unresolved, 1 measurement error.
- Additive starting count: 14 unresolved after four hyperlink rows were resolved by the prior deterministic geometry audit.
- Known limitations at start: two completed pipelines, purposive controlled corpus, unresolved representability/equivalence cases, no Word outputs, no converted interaction fixtures, no trustworthy real-world sanity corpus, and no user/screen-reader study.

# 2. Converter scope

Microsoft Word was investigated additively. Office is installed and registered
as x64 Microsoft 365 (`16.0.20430.20092`), but standard PowerShell COM,
64-bit Python/pywin32 COM, 32-bit and 64-bit WSH, and direct `WINWORD.EXE`
launch all failed before conversion. COM/direct launch returned `0x80070520`;
WSH failed with an access-denied settings error. No Word pilot PDF was
produced, so the gate is **NO-GO**.

No legitimate alternative third converter is installed: LibreOffice,
Pandoc, and OnlyOffice were not discoverable. The final completed pipeline
count remains **two**: LibreOffice and the recorded Google Docs route.

# 3. Interaction corpus

The six interaction fixtures still pass 25/25 source-contract checks. They were
not converted. LibreOffice, Word, Pandoc, and OnlyOffice are unavailable or
blocked; the authenticated Google Docs picker was reachable, but the browser
bridge could not complete the native local-file chooser after Browse. No file
was uploaded, and no output/hash/extraction/classification was created.

The interaction corpus therefore improves controlled source/test-input design
only. It adds no converter observations, no denominator changes, and no new
failure claims.

# 4. Real-world sanity corpus

No document was included. Official candidates were investigated, including
Section508.gov authoring resources, the Illinois Word Accessibility Exercise,
and a University of Oregon accessible Word template. They provide public
provenance and accessibility labels or guidance, but not sufficiently specific,
independently inspectable feature-level source contracts. The downloaded binary
files were also not reproducibly retrievable in this environment. Adding them
would create apparent ecological validity without reliable ground truth, so the
candidate set was rejected and documented in `docs/REAL_WORLD_SANITY_CORPUS.md`.

# 5. Unresolved cases

- Starting additive count: **14/52**.
- Final additive count: **14/52**.
- Cases resolved by this attempt: **0**.
- New rules: **none**. No one-off or post-hoc feature-specific rule was added.
- Evidence: all 14 rows were inspected with independent pypdf and PyMuPDF
  evidence; pdfplumber was unavailable. Structure/text was observed, but no
  general standards-grounded relation established the full source contract.
- Verified taxonomy: **11** target-format representability ambiguities, **2**
  semantic-equivalence ambiguities, and **1** extraction limitation.

The secondary audit is in
`scientific_strengthening/unresolved_resolution/SECONDARY_PARSER_AUDIT.md` and
its JSON output. All 14 remain principled abstentions; the frozen result record
and classifications are unchanged.

# 6. Screen-reader/user-study limitation

No automated accessibility/AT proxy was added. Windows Narrator and Acrobat do
not expose a stable, reproducible accessibility-tree extraction interface in
this environment. A viewer-side checker would answer destination conformance,
not source-to-destination preservation, and would introduce an environment-
dependent proprietary measurement path. The absence of a disabled-user or
screen-reader study remains explicit and is not presented as resolved.

# 7. Limitations status table

| Limitation | Starting severity | Action attempted | Result | Final status |
|---|---|---|---|---|
| Two completed pipelines | HIGH | Word COM/WSH/Python/direct-launch diagnostics; alternative-converter inventory | Word no-go; no legitimate third converter available | UNCHANGED |
| Purposive controlled corpus | HIGH | Sought public government/university DOCX candidates with known semantics | Candidates lacked sufficiently inspectable contracts | UNCHANGED |
| 14 additive unresolved cases | HIGH | Independent pypdf/PyMuPDF structure/text triangulation | No general safe equivalence rule; all abstentions retained | REDUCED |
| No Word outputs | MEDIUM | Full deterministic and interactive feasibility attempt | Zero outputs; pre-conversion session blocker documented | UNCHANGED |
| Interaction fixtures without outputs | MEDIUM | Local converter inventory and Google Docs upload pilot | Source contracts pass; upload bridge blocked before transmission | UNCHANGED |
| No real-world sanity corpus | MEDIUM | Public-provenance candidate search and contract assessment | Inclusion would weaken oracle validity | UNCHANGED |
| No screen-reader/user study | MEDIUM | Automated proxy feasibility assessment | No trustworthy proxy; not required by the central claim | NOT NECESSARY TO RESOLVE |
| Structural vs end-user accessibility | HIGH | No claim-expanding experiment; boundary review | Correct limitation retained | NOT NECESSARY TO RESOLVE |

# 8. New scientific findings

1. Independent parser triangulation supports, rather than undermines, the 14
   additive abstentions: structure presence is observable in several hard cases,
   but the required source relation is not thereby established.
2. The Word limitation is environmental and pre-conversion, not an observed
   Word accessibility result.
3. The interaction corpus is a validated source/test-input extension, not an
   empirical converter extension in this environment.
4. Public accessibility examples are not automatically usable as research
   oracles; explicit feature-level source semantics remain necessary.

# 9. Did any frozen baseline result change?

**NO.** No fixture, source contract, frozen PDF, hash, provenance link, primary
classification, result row, denominator, or artifact evidence file changed.

# 10. Did the central conclusion change?

**NO.** The central conclusion remains that selected machine-verifiable
accessibility semantics show feature- and pipeline-specific preservation,
alteration, loss, and principled uncertainty under the two tested DOCX-to-PDF
pipelines. The evidence does not support universal converter, prevalence, or
end-user-usability claims.

# 11. New risks introduced

No scientific or packaging risk was introduced. Stage 2 added only isolated
scripts and reports. No Google interaction file was uploaded, no external DOCX
was committed, no new converter output was created, and no manuscript/artifact
hash changed. The additive parser audit uses independent libraries but does not
claim parser independence from every component of the original extractor.

# 12. Final paper changes justified

None from this limitation-resolution stage. The current manuscript already
contains the necessary bounded scope, frozen-versus-additive distinction,
testing-oracle framing, baseline contrast, Word exclusion, and interaction
boundary. Adding failed feasibility attempts or unconverted fixtures to the
main empirical results would add complexity without evidence.

# 13. Remaining limitations

Ranked by reviewer importance:

1. Only two completed conversion pipelines support the primary comparison.
2. The corpus is purposive and controlled rather than population-representative.
3. Fourteen additive cases remain unresolved because cross-format equivalence is
   not sufficiently observable.
4. The six new interaction fixtures have validated contracts but no converted
   outputs.
5. The Google backend is cloud-versioned and Word could not enter the study.
6. Structural preservation does not establish screen-reader usability or
   end-user accessibility.

# 14. Final recommendation

**SUBMIT STRENGTHENED VERSION**

The current audited manuscript is the appropriate submission version. The
limitation-resolution attempt produced useful negative evidence and stronger
provenance, but no new empirical result that justifies changing the paper or
the frozen reviewer artifact.
