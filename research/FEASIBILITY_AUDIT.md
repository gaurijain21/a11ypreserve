# Feasibility Audit

## Scorecard

| Dimension | Assessment | Evidence |
|---|---:|---|
| Research question | 8/10 narrow; 3/10 broad | Standards make the preservation question real, but broad benchmarking is crowded. |
| Novelty | 7/10 narrow; 2/10 broad | Differential provenance/taxonomy survives; generic conversion benchmark does not. |
| Fixture generation | 8/10 | Valid DOCX and HTML fixtures generated; manifest features headings, language, lists, alt text and table headers. |
| Semantic extraction | 5/10 | DOCX/HTML extraction works; PDF text/metadata works; PDF structure adapter is incomplete. |
| Conversion access | 4/10 | Chrome headless produced a real PDF; Word GUI opened the repaired source; Word/Acrobat export was not confirmed; COM was blocked by the local logon session. |
| Reproducibility | 6/10 | Scripts and hashes/evidence layout exist, but an independent second engine and route are still required. |
| Reviewer risk | High | Direct prior art and active 2026 benchmarks make overclaiming easy to detect. |

## Technical finding

The minimal harness is feasible. A real HTML→PDF artifact was created at `outputs/G01_chrome.pdf`; the comparator preserved the document language and marked all unparsed tagged-PDF structure as `MEASUREMENT_ERROR`. This is the correct conservative behavior. The Word route uncovered a real package-quality issue: the initial handcrafted OOXML could not be opened by Word, while the repaired python-docx package opened in Word Compatibility Mode.

## Verdict

**GO WITH SCOPE CHANGES.** Continue only as a source-grounded differential methodology study. Stop the broad “all conversion accessibility” or “PDF→HTML benchmark” framing. The next evidence gate is two independent engines, route-specific output adapters, and manual/AT confirmation of a stratified subset.

