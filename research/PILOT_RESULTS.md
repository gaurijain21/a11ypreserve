# Pilot Results

## Completed

- Python-generated DOCX and HTML semantic fixtures were created with the expected manifest features.
- The repaired DOCX opened in real Microsoft Word GUI in Compatibility Mode.
- The first handcrafted OOXML package failed Word’s open validation. This was treated as `INVALID_CONVERSION` for that artifact, then repaired rather than misread as an accessibility failure.
- Chrome headless produced `outputs/G01_chrome.pdf` (79,969 bytes).
- The PDF extractor found title, text, `/Lang = en-US`, and a `StructTreeRoot`.
- `scripts/a11ydiff.py` reported language `PRESERVED` and headings, image alternatives, list nesting and table headers as `MEASUREMENT_ERROR` because the output is tagged but the PDF structure adapter is not implemented.

## Unconfirmed or unavailable

- The Word backstage Adobe Acrobat export control did not yield a confirmed output artifact in this environment.
- Word COM automation failed with a local “specified logon session” error, so automated Word conversion evidence is not claimed.
- No screen-reader/user study was run. Word’s accessibility tree exposed only a numeric UI node for the body in this state; that is a tool-observation limitation, not evidence of semantic loss.

## Interpretation

The pilot demonstrates feasibility of the harness and the necessity of a measurement-error state. It does not yet demonstrate cross-engine conversion differences or support a quantitative preservation claim. The correct research conclusion is a scoped go, with further conversion routes as a hard evidence gate.

