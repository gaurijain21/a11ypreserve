# V5 Google Docs import/export boundary

## Status: secondary diagnostic, not localized for the V4 PDFs

The end-to-end route is DOCX upload/import into Google’s internal document
representation followed by `File → Download → PDF Document (.pdf)`. The
available V4 artifacts contain the source DOCX and final PDF, but no exported
intermediate Google-native document structure or API snapshot. Therefore a
feature-level change cannot responsibly be attributed to import versus PDF
export from the current evidence.

| Feature | Boundary result | Evidence status |
|---|---|---|
| Inline language | Cannot localize | Final PDF lacks required inline marker; intermediate state unavailable. |
| Metadata | Cannot localize | Final PDF metadata differs; no round-trip intermediate. |
| Hyperlinks | End-to-end association uncertainty | URI/annotation evidence exists, but import/export stage is not isolated. |
| Complex tables | Cannot localize | Final structure is incomplete for the contract; no intermediate. |
| Captions/footnotes | Cannot localize | Final association evidence is insufficient; no intermediate. |

V5 preserves this boundary as a secondary limitation. A future localization
arm must export a Google-native document or use a documented API snapshot,
hash it, and apply the same source-contract checks before making causal claims.
