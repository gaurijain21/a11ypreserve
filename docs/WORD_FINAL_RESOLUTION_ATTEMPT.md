# Microsoft Word final resolution attempt

This is an additive feasibility record. It does not add Word outputs or alter
the frozen two-pipeline experiment.

## Environment

- Word executable: `<INSTALLED_APPLICATION>
- Office product: `O365ProPlusRetail`
- Office version reported by registry: `16.0.20430.20092`
- Office platform: `x64`
- COM registration: `Word.Application.16` is present under
  `HKEY_CLASSES_ROOT\Word.Application\CurVer`.
- Python: 64-bit Python 3.11 with pywin32 available.

## Attempts

1. Standard x64 PowerShell `New-Object -ComObject Word.Application`.
2. Python 64-bit `win32com.client.DispatchEx("Word.Application")`.
3. Windows Script Host through both `System32\cscript.exe` and
   `SysWOW64\cscript.exe`, using `scientific_strengthening/word_pipeline/word_com_probe.vbs`.
4. Direct launch of the installed `WINWORD.EXE` for an interactive export path.

## Results

- PowerShell COM activation failed before an application object was returned:
  `0x80070520 A specified logon session does not exist. It may already have
  been terminated.`
- Python COM activation failed with the same HRESULT and message.
- Both WSH bitness paths failed before the script executed with
  `CScript Error: Loading your settings failed. (Access is denied.)`.
- Direct `WINWORD.EXE` launch failed with the same `0x80070520` logon-session
  error.
- No Word window was available to the computer-use bridge, no pilot DOCX was
  exported, and zero Word-generated PDFs or result rows exist.

## Gate decision

**NO-GO.** The installation and COM registration are present, but the current
Windows session cannot create or launch Word through any tested deterministic
or interactive path. The failure occurs before conversion, so it provides no
evidence about Word's accessibility behavior. Word remains excluded from the
completed pipeline count.

No Office settings, activation state, registry entries, permissions, or global
system configuration were changed.
