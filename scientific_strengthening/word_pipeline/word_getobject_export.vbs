Option Explicit

Dim doc, outPath, fso
outPath = "<LOCAL_WORD_WORKSPACE>\getobject_trivial.pdf"
Set fso = CreateObject("Scripting.FileSystemObject")
If fso.FileExists(outPath) Then fso.DeleteFile outPath, True

On Error Resume Next
Set doc = GetObject("<LOCAL_WORD_WORKSPACE>\trivial_diagnostic.docx")
If Err.Number <> 0 Then
  WScript.Echo "GETOBJECT=FAIL"
  WScript.Echo "HResult=0x" & Hex(Err.Number)
  WScript.Echo "Message=" & Err.Description
  WScript.Quit 1
End If
WScript.Echo "GETOBJECT=PASS"
WScript.Echo "WordVersion=" & doc.Application.Version
Err.Clear
doc.ExportAsFixedFormat outPath, 17, False, 0, 0, 0, 0, 0, True, False, 0, True, False, False, 0
If Err.Number <> 0 Then
  WScript.Echo "EXPORT=FAIL"
  WScript.Echo "HResult=0x" & Hex(Err.Number)
  WScript.Echo "Message=" & Err.Description
  WScript.Quit 1
End If
WScript.Echo "EXPORT=RETURNED"
If fso.FileExists(outPath) Then
  WScript.Echo "OUTPUT_EXISTS=True"
  WScript.Echo "OUTPUT_SIZE=" & fso.GetFile(outPath).Size
Else
  WScript.Echo "OUTPUT_EXISTS=False"
End If
