# Google Docs repeatability final report

## Design

The historical frozen Google output is Run 1. Runs 2 and 3 were independently uploaded through the recorded authenticated workflow. Repeatability is secondary and does not alter the frozen V2 denominator.

## Results

| Fixture | Run 1 class | Run 1/2/3 byte result | Classification stable |
|---|---|---|---|
| F01_HEADINGS | OBSERVED_PARTIAL | STABLE_BY_BYTE_IDENTITY | YES |
| F02_ALT_TEXT | VERIFIED_PRESERVED | STABLE_BY_BYTE_IDENTITY | YES |
| F03_LISTS | UNRESOLVED_EQUIVALENCE | STABLE_BY_BYTE_IDENTITY | YES |
| F04_TABLE | VERIFIED_PRESERVED | STABLE_BY_BYTE_IDENTITY | YES |
| F05_DOCUMENT_LANGUAGE | ALTERED | STABLE_BY_BYTE_IDENTITY | YES |
| F06_INLINE_LANGUAGE | CONFIRMED_LOST | STABLE_BY_BYTE_IDENTITY | YES |
| F07_DECORATIVE_IMAGE | OBSERVED_PARTIAL | STABLE_BY_BYTE_IDENTITY | YES |
| F08_LINKS | UNRESOLVED_EQUIVALENCE | STABLE_BY_BYTE_IDENTITY | YES |
| F09_DOCUMENT_TITLE | ALTERED | STABLE_BY_BYTE_IDENTITY | YES |
| F10_COMPLEX_TABLE | UNRESOLVED_EQUIVALENCE | STABLE_BY_BYTE_IDENTITY | YES |
| F11_FOOTNOTES | CONFIRMED_LOST | STABLE_BY_BYTE_IDENTITY | YES |
| F12_EQUATION | UNRESOLVED_EQUIVALENCE | STABLE_BY_BYTE_IDENTITY | YES |
| F14_CAPTIONS | UNRESOLVED_EQUIVALENCE | STABLE_BY_BYTE_IDENTITY | YES |

All 13/13 fixtures were byte-identical across all three runs, and classification stability was observed for 13/13 fixtures.

## Interpretation boundary

This result is conditional on the recorded workflow, experiment date, browser/session environment, and an unpinnable Google backend. It is not a guarantee about future Google Docs versions or all accounts. Byte identity is stronger than structural stability for these files, but does not establish general cloud-service determinism.
