# Microsoft Word pipeline feasibility

Recorded: 2026-10-03

## Decision

**NO-GO for a third primary pipeline.** Microsoft Word is installed, but deterministic automation is blocked before a document can be opened or exported. No Word PDF is included in the primary or additive result denominators.

## Environment and attempts

- Installed executable: `<INSTALLED_APPLICATION>
- Previously observed Word version/build: `16.0.20326.20158`.
- Current operating system: Windows `10.0.26200.0`.
- Representative pilot set: four existing pilot fixtures covering headings, alternative text, lists, and tables.
- Current attempt: PowerShell `Word.Application` COM activation followed by the normal `Documents.Open` and `ExportAsFixedFormat` PDF route. The pilot was additive and targeted a separate pilot output directory.
- Earlier attempt: native COM export with the same normal Word PDF route; a Python/pywin32 attempt was also recorded, but the bundled Python runtime did not provide pywin32.

Both COM paths fail at activation with:

`0x80070520: A specified logon session does not exist. It may already have been terminated.`

The current attempt produced zero converted fixtures, no Word version object, and no PDF output. The failure is a session/COM activation blocker, not a parseability or tagging result. No GUI automation was used to bypass the authentication/session boundary, and no partially comparable Word result was created.

## Consequence for the study

The frozen evidence remains a two-condition study: the recorded LibreOffice and Google Docs DOCX-to-PDF pipelines. Word is explicitly excluded rather than silently treated as absent evidence. The manuscript's scope is therefore limited to the named tested conditions; the absence of Word is a remaining external-validity limitation, not a scientific finding about Word's PDF export.

