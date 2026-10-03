# Confirmed Lost Cases

## F06 / Google Docs / inline language

The source document has primary language `en-US` and an explicit `es-MX` override on the run “Buenos días.” The expected PDF representation is an inline marked span with `/Lang es-MX` or an equivalent. The valid tagged Google Docs PDF contains no inline language span and raw inspection finds no `es-MX` marker. pypdf structure extraction, raw-marker inspection, and Poppler text extraction independently support the absence. The case is **LOST** under the frozen contract, not invalid conversion or non-representability.

## F11 / Google Docs / footnote association

The source contains a native footnote reference and body verified in `word/footnotes.xml`. The expected PDF representation is a `/Note`/footnote structure or equivalent reference-to-body association. The valid tagged Google Docs PDF contains no `/Note`, `/Footnote`, or recovered source note body. pypdf extraction, raw inspection, and Poppler text extraction agree. LibreOffice produced comparable `/Note` evidence, so the Google Docs result is **LOST**, not merely unrepresentable.

These are losses under the tested source contracts and dated pipeline condition; they are not universal claims about Google Docs.
