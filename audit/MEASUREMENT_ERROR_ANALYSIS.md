# Measurement-Error Analysis

The single measurement error is **F11_FOOTNOTES / LibreOffice**. The PDF is valid, tagged, and contains a `/Note` structure with child objects, but the current marked-content extractor and independent `pdftotext` run do not recover the note-body text sufficiently to verify the source reference-to-body association. The raw object scan confirms `/Note` exists; therefore this is not `LOST`, not `INVALID_CONVERSION`, and not a malformed-output case.

One independent resolution method was attempted: raw PDF object-marker inspection plus Poppler `pdftotext` output. It confirms structure presence but does not resolve the missing body association. The result remains `MEASUREMENT_ERROR`.
