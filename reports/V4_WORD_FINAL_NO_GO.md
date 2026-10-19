# V4 Word Final No-Go

One bounded final recovery attempt was performed after the earlier `0x80070520` failure.

- `WINWORD.EXE` was present at `C:\Program Files\Microsoft Office\Root\Office16\WINWORD.EXE`.
- Direct `/safe` launch succeeded.
- The exact frozen `F01_A.docx` opened in Word Safe Mode without editing.
- The active Word GUI was inspectable through the local Word automation interface.
- One native Word `ExportAsFixedFormat` pilot was attempted with document-structure tags requested.
- Word returned without a COM exception but produced a zero-byte PDF; waiting did not produce a usable file.
- The zero-byte pilot artifact was removed and is not counted as a conversion output.

Disposition: **NO-GO for the Word primary pipeline**. No Word PDF is counted, and no bulk Word conversion was attempted. This is an environment/application-output limitation, not evidence that Word cannot export PDFs generally.
