# READY WITH NARROW CLAIMS

## Source oracle independence

PASS: 13/13 included fixtures independently checked by fresh raw DOCX ZIP/XML
assertions. The verifier does not import ASIR, fixture-generation,
manifest-generation, or comparator code. It agrees with the frozen manifests
and the implementation-grounded ASIR. This is an independent measurement path,
not independent human expert validation.

## Partial-case breakdown

The nine frozen `PARTIALLY_PRESERVED` outcomes remain unchanged. Three are
`OBSERVED_PARTIAL` (F01/Google Docs and both F07 outputs); six are
`UNRESOLVED_EQUIVALENCE` (F03/Google Docs, both F08 outputs, F10/Google Docs,
F12/Google Docs, and F14/Google Docs). None is reclassified as measurement
error. The full case table is in `PARTIAL_CASE_REAUDIT.md`.

## Confirmed losses

F06/Google Docs inline language and F11/Google Docs footnote association remain
`LOST` and are independently corroborated through pypdf structure traversal and
PyMuPDF/serialized-object evidence. F11/Google Docs visibly retains the note
text; the loss claim is the machine-verifiable association. F11/LibreOffice
remains `MEASUREMENT_ERROR` because `/Note` exists but its association cannot be
resolved.

## Calibration

27 synthetic positive, negative, and alternate-equivalent controls were run
through the comparator. The diagnostic counts are 12 correct determinate, 6
correctly unresolved, 0 false positives, 2 false negatives, and 7 other
unresolved/indeterminate cases. These are not inferential performance metrics.
They justify exposing uncertainty and identify future comparator work for
alternate link/table representations.

## Parser triangulation

PASS for F06/Google, F11/Google, and F11/LibreOffice. The two paths traverse
catalog/structure-tree objects and independently inspect serialized PDF objects,
page text, and links. This reduces parser-only loss claims without asserting
complete PDF semantics.

## Taxonomy and decision boundary

The frozen primary taxonomy remains exactly `PRESERVED`,
`PARTIALLY_PRESERVED`, `ALTERED`, `LOST`, and `MEASUREMENT_ERROR`. The V2
evidence axis adds `VERIFIED_EQUIVALENCE`, `OBSERVED_DIFFERENCE`,
`OBSERVED_PARTIAL`, `INDEPENDENTLY_CONFIRMED_ABSENCE`,
`UNRESOLVED_EQUIVALENCE`, `INSUFFICIENT_EVIDENCE`, and `MEASUREMENT_FAILURE`.
No primary outcome changed.

## Integrated-document sanity check

Not performed. The study remains intentionally controlled and atomic; external
validity risk is HIGH. No new fixtures or conversions were added because the
current paper can make a defensible protocol-level claim without changing the
frozen experiment. Integrated documents are a required next validation step
before any broader generalization.

## Novelty and prior art

The prior-art review includes DocAccessible, DAISY, Roig/Ribera, SciA11y,
iTagPDF, and Kumar et al. The paper does not claim first, unique, or absence of
prior work. Its narrow boundary is the controlled source-to-destination DOCX-
to-PDF preservation protocol, explicit source contracts, uncertainty-aware
decisions, and reusable provenance artifacts.

## Contributions

The revised manuscript emphasizes: (1) versioned source contracts, (2) an
independent source oracle plus destination evidence triangulation, (3) explicit
uncertainty and calibration, and (4) the bounded empirical application to two
named pipelines.

## Removed or prohibited claims

The manuscript prohibits global converter rankings; claims about all DOCX
documents or software versions; claims that conversion generally destroys
accessibility; claims that altered information necessarily causes harm; claims
that PDF export alone caused every change; claims that a11ydiff measures complete
accessibility; and validator-defect claims.

## Limitations

The corpus is small, controlled, and not representative; features have unequal
complexity; the primary unit is one fixture/converter pair; percentages are
descriptive only; Google Docs backend version cannot be fully pinned; source and
destination equivalence is feature-specific; no direct screen-reader or
disabled-user study was performed; and no population-level or user-impact claim
is supported.

## Artifact readiness

Contracts, schema, source certificates, calibration outputs, parser
triangulation, V2 evidence freeze, changelog, conformance-suite protocol, and
prior-art comparison are present. New artifacts use relative paths and no
browser credentials or session material. Existing frozen evidence remains
unchanged and should be sanitized separately before public release if a package
still exposes local paths.

## Venue fit

DocEng is the strongest fit because the contribution is document transformation,
source contracts, conformance, and reproducible evidence. ASSETS is plausible if
the manuscript foregrounds accessibility-preservation boundaries and avoids
user-impact overclaiming. A software-testing venue is plausible only if the
suite interface, calibration, and independent oracle are expanded in a future
release.

## Additional experiment required

No additional experiment is required for the bounded manuscript claim. The
remaining integrated-document and additional-converter work is a future
external-validity study, not a blocker for reporting this controlled benchmark.

## Recommendation

The project survives hostile review only under the narrow claims above. Submit
as a controlled, uncertainty-aware source-to-destination preservation protocol
and empirical benchmark—not as a general accessibility validator, converter
ranking, or user-impact study.
