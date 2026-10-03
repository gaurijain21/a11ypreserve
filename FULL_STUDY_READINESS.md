# READY FOR FULL EXPERIMENT

## Readiness basis

Phase 4 benchmark construction is complete. The corpus is frozen only after
raw OOXML verification, manifest comparison, source-extractor comparison,
render QA, and regression tests. The large conversion matrix has not been
launched.

## Final feature set

The 13 atomic feature families are:

1. F01 heading hierarchy
2. F02 image alternative text
3. F03 list semantics
4. F04 table/header structure
5. F05 document language
6. F06 inline language changes
7. F07 decorative image state
8. F08 hyperlink semantics
9. F09 document title and metadata
10. F10 scoped complex/multi-level table headers
11. F11 scoped footnote association
12. F12 native OMML equation/math semantics
13. F14 figure/caption association

F13 reading order, merged-cell stress variants, abbreviations, logical
grouping/sections, and forms remain deferred because their first-pass
equivalence rules or representations are too ambiguous for the frozen atomic
set.

## Corpus status

- Atomic fixture count: 13.
- Initial instance count: 13, one per feature family.
- New Phase 4 fixtures: 9.
- Historical frozen fixtures retained unchanged: 4.
- Frozen manifest: `corpus/FROZEN_CORPUS_MANIFEST.json`.
- Raw OOXML verification: PASS for all 9 new fixtures.
- Source manifest = OOXML = source extractor: PASS for all 9 new fixtures.
- Render QA: PASS for all 9 new fixtures; each rendered to a one-page PDF/PNG inspection artifact.
- Original F01–F04 SHA-256 integrity: PASS.

## Converter matrix

Primary execution:

| Converter | Route | Planned outputs |
|---|---|---:|
| LibreOffice 26.2.6.3 or recorded execution version | DOCX → tagged PDF | 13 |
| Google Docs, recorded cloud/export date | DOCX → PDF | 13 |

Expected primary total: 26 outputs. Microsoft Word is an optional third
engine, expected at 13 additional outputs if native `ExportAsFixedFormat`
becomes usable. Word is not a blocker and is not a result until a legitimate
native export succeeds.

## Required validators and extraction

Primary evidence is direct PDF object/structure inspection through the
deterministic extractor: `/StructTreeRoot`, role map, structure roles, marked
content, `/Alt`, `/Lang`, link annotations, table roles, metadata, and page
content. The comparator is `scripts/phase4_compare.py`, exposed through
`scripts/a11ydiff.py`.

Secondary evidence should include PAC, Acrobat Accessibility Checker, or
veraPDF when available. These validators must be recorded as observations and
must not override source-grounded preservation classifications.

## Expected verification burden

Automated work includes conversion orchestration, SHA-256 recording, PDF
parseability/page checks, structure extraction, feature comparison, JSON
provenance, and regression tests. Manual or semi-manual review is expected for
converter settings, Google Docs export state, ambiguous structure-tree cases,
validator observations, and falsification of every reported loss/degradation.

## Current test status

- Source verification: PASS.
- Phase 4 taxonomy/extractor/freeze tests: PASS.
- Pilot 1 regression: PASS.
- Pilot 2 regression: PASS.
- Pilot 3 regression: PASS.
- Test report: `results/test_results.json`.

## Unresolved limitations

- The new F11 and F12 contracts are ready for measurement but may produce
  `MEASUREMENT_ERROR` or `NOT_REPRESENTABLE` when a converter has no
  independently inspectable PDF equivalent.
- One instance per family is suitable for a controlled first execution, not
  for population estimates. Variants are specified in
  `research/INSTANCE_DESIGN.md` and should follow after atomic results.
- Google Docs is a cloud service and may drift between runs.
- Word remains environment-deferred.
- Human assistive-technology evaluation is outside this readiness phase.

## Execution constraint

Use `research/EXPERIMENT_EXECUTION_PLAN.md` for the full run. Do not start the
26-output primary matrix until explicitly instructed.
