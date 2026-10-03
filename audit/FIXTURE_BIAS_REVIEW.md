# Fixture-Bias Review

The source-verification chain reported MANIFEST = OOXML = source extractor for all 13 fixtures. Rendering QA and frozen hashes were available before conversion. Classifications below assess benchmark suitability, not whether a fixture is complex enough to represent every real document.

| Fixture | Rating | Review |
|---|---|---|
| F01_HEADINGS | STRONG | Native Heading styles; ordered hierarchy is directly machine-verifiable. |
| F02_ALT_TEXT | STRONG | Native image description/alt text; exact author string is isolated. |
| F03_LISTS | STRONG | Native numbering with ordered, unordered, and nested items; PDF role/type contract is explicit. |
| F04_TABLE | STRONG | Small native table with explicit header row and deterministic cell matrix. |
| F05_DOCUMENT_LANGUAGE | STRONG | Document default language is explicit in OOXML and PDF `/Lang` is directly inspectable. |
| F06_INLINE_LANGUAGE | STRONG | Run-level language override is explicit and isolated. |
| F07_DECORATIVE_IMAGE | ACCEPTABLE_WITH_LIMITATION | Meaningful and explicitly decorative images are isolated; PDF artifact equivalence is format-sensitive. |
| F08_LINKS | STRONG | Visible link text and URI are explicit; destination name association is parser-sensitive. |
| F09_DOCUMENT_TITLE | STRONG | Visible title and core metadata are separately defined. |
| F10_COMPLEX_TABLE | ACCEPTABLE_WITH_LIMITATION | Small but nontrivial two-level header/span stress case; associations require PDF-specific evidence. |
| F11_FOOTNOTES | ACCEPTABLE_WITH_LIMITATION | Native note part and reference are valid; one engine exposed unresolved `/Note` extraction. |
| F12_EQUATION | ACCEPTABLE_WITH_LIMITATION | Native OMML is valid; PDF math representations are heterogeneous. |
| F14_CAPTIONS | ACCEPTABLE_WITH_LIMITATION | Caption association is atomic but PDF may expose it as role or adjacency. |

No fixture is excluded by this audit. The limitation is scope: atomic fixtures establish causal observability, not population representativeness.
