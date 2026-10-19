# V4 Microsoft Word Desktop Export Root-Cause Audit

Date: 2026-10-04  
Repository HEAD at audit start: `3913a9e8553fe52d89db7667c8e3046149f51c94`  
V4 protocol freeze: `41a7d3f8b84e98acbdafe14070f2ebe7ea6a59e1`

## Disposition

**NO-GO for a recovered Microsoft Word desktop conversion arm on this machine/session.** No Word PDF is counted, no Word classifications were generated, and the frozen 130-case LibreOffice + Google experiment was not changed.

This is a bounded technical no-go, not a claim that Microsoft Word cannot export PDFs in general.

## Environment

- Windows: `Microsoft Windows NT 10.0.26200.0`.
- Word executable: `<INSTALLED_APPLICATION>
- Office product: `O365ProPlusRetail`.
- Office architecture: x64; the installed Word file and Click-to-Run registry reported build `16.0.20430.20092`.
- Word processes used for diagnosis ran in the ordinary interactive user session (session 1), not as an elevated or scheduled process.
- No unrelated Word process was left running at the end of the diagnostic session.
- Activation state was not conclusively established. No account email, token, license key, Credential Manager entry, or credential setting was read or changed.

## Inputs and local-path controls

The selected non-holdout pilot was `experiments/v4/fixtures/F01_A.docx`.

- Frozen source SHA-256: `62643E92F2A7E40FF87C94795C6AD4CDA019AF8870F0B2F16EEBC625A3A40FC2`.
- A byte-for-byte copy was made at `<LOCAL_WORD_WORKSPACE>\F01_A.docx`; its SHA-256 matched.
- A diagnostic-only heading/paragraph DOCX was created at `<LOCAL_WORD_WORKSPACE>\trivial_diagnostic.docx`; it was not a V4 fixture and was not analyzed.
- The local directory passed a harmless write/delete test.
- The C: volume had approximately 10.8 GB free during testing.
- TEMP/TMP locations existed and were checked for basic accessibility.
- No successful native Word output was produced from the local path, so the local-path test did not demonstrate that OneDrive was the cause or the cure.

## Recovery attempts and observations

| Attempt | Result | Evidence |
|---|---|---|
| Normal Word launch | PASS | Word launched from the installed executable; both the local trivial document and the copied F01_A fixture opened and became responsive. |
| Safe-mode Word launch | PASS | `WINWORD.EXE /safe` opened the diagnostic document in the interactive session. |
| 64-bit PowerShell `Word.Application` activation | FAIL | HRESULT `0x80070520`; the COM class factory reported that the specified logon session did not exist or had terminated. |
| 32-bit PowerShell COM activation | FAIL | Same `0x80070520`, ruling out a simple PowerShell bitness mismatch. |
| Python/pywin32 active-object access | FAIL | `GetActiveObject` was unavailable; document-bound `GetObject` also failed with the same missing-logon-session HRESULT. |
| WSH/VBScript document-bound export probe | BLOCKED | `cscript.exe` failed before the script ran: `Loading your settings failed. (Access is denied.)` Both 64-bit and 32-bit WSH were affected. |
| COM while safe-mode Word was visible | FAIL | Same `0x80070520`; safe mode did not repair the class-factory/session failure. |
| Registry registration | PRESENT | Word’s COM class registration and `/Automation` server path were present. Registration presence did not make activation work. |
| Prior native fixed-format pilot | FAIL | Existing repository evidence records an in-process/safe-mode `ExportAsFixedFormat` call returning without a COM exception but leaving a zero-byte PDF. |
| Application event log | NO RELEVANT EVENT | A bounded recent scan found no relevant Application Error, DistributedCOM, Office, Word, or WER event for this attempt. |

The repository’s existing `reports/V4_WORD_FINAL_NO_GO.md` records the earlier safe-mode native `ExportAsFixedFormat` pilot, including the requested document-structure-tags option and the resulting zero-byte output. That artifact was removed and is not counted as a conversion output.

## GUI route status

Word GUI launch/open was directly verified. The native computer-use bridge available in this task exposed browser surfaces but no native Word application surface. Under the computer-use skill’s safety boundary, direct PowerShell UI automation was not substituted for that missing native surface.

Consequently, this bounded attempt did **not** claim a fresh click-level result for Word’s File → Save As → PDF or File → Export → Create PDF/XPS dialogs. Those routes remain unverified in this host. The historical native fixed-format attempt still provides evidence of the zero-byte symptom, but it does not justify relabeling the GUI routes as tested.

The in-process VBA route was likewise not completed: the document-bound automation path could not obtain the open document because COM activation/GetObject failed, and WSH itself was blocked by the access-denied settings error. No macro was used to alter a document or PDF.

## Best-supported diagnosis

The strongest reproducible blocker is an Office automation/session failure at COM class-factory activation: the same `0x80070520` occurred from 64-bit PowerShell, 32-bit PowerShell, Python/pywin32, document-bound object access, and while a visible Word process was running in the normal interactive session and in safe mode. The Word COM registration is present, so this is not simply a missing registration.

Separately, the prior in-process native fixed-format pilot reached Word’s export call but produced a zero-byte PDF. That indicates an additional failure in the native fixed-format output path, profile, or Office environment. The available evidence does not isolate which internal component created the zero-byte artifact. There were no useful Windows Application log events, and the local-path preparation could not be paired with a click-level GUI export in this host.

Therefore the precise root cause remains **partially unresolved**. It is not scientifically justified to state that OneDrive, the fixture, PDF tagging, or a particular feature caused the failure. The supported conclusion is: **Word opens documents, but its automation/export path is not recoverable through the available same-session interfaces, and the only prior native export reached zero-byte output.**

## Scientific disposition

- Word atomic PDFs: `0`.
- Word realistic-document PDFs: `0`.
- Word repeatability runs: `0`.
- Word classifications: none.
- Word is not part of the frozen primary denominator and was not added as a supplementary arm.
- No fixture, contract, classification, comparator, source oracle, holdout, calibration expectation, LibreOffice output, or Google output was changed.
- No manuscript modification is recommended for this attempt; the existing wording that Word GUI launch/open succeeded but native PDF export produced zero-byte output remains accurate, with this audit adding the COM/session detail and the GUI-route limitation.

## Remaining human action, if a definitive GUI result is required

A human with an interactive native Word-control surface would need to perform one local diagnostic export for the trivial document and one for the copied non-holdout F01_A fixture using Save As → PDF and Export → Create PDF/XPS, while observing File → Account activation status. This is a diagnostic follow-up only; bulk manual conversion is not requested. No Office repair, credential reset, sign-out, or security-setting change was performed.

