# Pilot Environment

- Date: 2026-09-27 local time; evidence timestamps use UTC.
- OS: Windows 11 build 26200.
- Bundled Python: 3.12.14.
- python-docx: 1.2.0.
- pypdf: 6.10.0.
- Pillow: 10.3.0.
- Microsoft Word: installed at `C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE`, version 16.0.20326.20158; COM/process launch blocked by Windows error `0x80070520`.
- Google Chrome: installed, version 153.0.8010.53; authenticated Google Docs home page was reachable.
- Adobe Acrobat: installed at `C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe`, version 26.2.21931.0; not exercised because the native session limitation prevented a reliable export/validator run.
- LibreOffice: not found.
- PAC: not found.
- veraPDF: not found.
- Poppler: not found on PATH; MiKTeX `pdftotext.exe` was present but was not used as a structural validator.
- Source extraction: deterministic OOXML inspection.
- PDF extraction: pypdf object-model and marked-content inspection.

