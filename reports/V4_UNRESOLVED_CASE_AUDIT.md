# V4 Unresolved-Case Audit

This is a post-freeze diagnostic audit. No unresolved classification was changed.

## LibreOffice

- F13_C captions: the PDF contains `/Caption` markers and `/Figure` structures, and visible caption text is present, but the current extractor cannot establish the required figure-to-caption association. This is a structure-association ambiguity, not confirmed loss.

## Google Docs

- F11_A through F11_E footnotes: visible note text is present in page extraction, but no `/Note` structure or independently recoverable reference/body association is present. Text presence alone cannot establish semantic footnote association. These remain conservative `UNRESOLVED_EQUIVALENCE` results.

## Conclusion

All six unresolved cases have an explicit cause: association evidence is incomplete or format-sensitive. None is an unexplained parser crash, missing output, or silent conversion failure. The frozen abstentions are retained.
