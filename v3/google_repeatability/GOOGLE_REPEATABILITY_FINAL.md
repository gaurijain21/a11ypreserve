# Google Docs repeatability final report

## Design

The historical frozen Google output is Run 1. Runs 2 and 3 were independently uploaded through the recorded authenticated workflow. Repeatability is secondary and does not alter the frozen V2 denominator.

## Results

| Fixture | Run 1 class | Run 1/2/3 byte result | Classification stable |
|---|---|---|---|
| F01_HEADINGS | OBSERVED_PARTIAL | BYTE_IDENTICAL | YES |
| F02_ALT_TEXT | VERIFIED_PRESERVED | BYTE_IDENTICAL | YES |
| F03_LISTS | UNRESOLVED_EQUIVALENCE | BYTE_IDENTICAL | YES |
| F04_TABLE | VERIFIED_PRESERVED | BYTE_IDENTICAL | YES |
| F05_DOCUMENT_LANGUAGE | ALTERED | BYTE_IDENTICAL | YES |
| F06_INLINE_LANGUAGE | CONFIRMED_LOST | BYTE_IDENTICAL | YES |
| F07_DECORATIVE_IMAGE | OBSERVED_PARTIAL | BYTE_IDENTICAL | YES |
| F08_LINKS | UNRESOLVED_EQUIVALENCE | BYTE_IDENTICAL | YES |
| F09_DOCUMENT_TITLE | ALTERED | BYTE_IDENTICAL | YES |
| F10_COMPLEX_TABLE | UNRESOLVED_EQUIVALENCE | BYTE_IDENTICAL | YES |
| F11_FOOTNOTES | CONFIRMED_LOST | BYTE_IDENTICAL | YES |
| F12_EQUATION | UNRESOLVED_EQUIVALENCE | BYTE_IDENTICAL | YES |
| F14_CAPTIONS | UNRESOLVED_EQUIVALENCE | BYTE_IDENTICAL | YES |

All 13/13 fixtures were byte-identical across all three runs, and classification stability was observed for 13/13 fixtures.

## Interpretation boundary

This result is conditional on the recorded workflow, experiment date, browser/session environment, and an unpinnable Google backend. It is not a guarantee about future Google Docs versions or all accounts. Byte identity is stronger than structural stability for these files, but does not establish general cloud-service determinism.
