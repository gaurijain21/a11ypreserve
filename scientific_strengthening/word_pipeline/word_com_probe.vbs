Option Explicit

Dim app
On Error Resume Next
Set app = CreateObject("Word.Application")
If Err.Number <> 0 Then
  WScript.Echo "COM_ACTIVATION=FAIL"
  WScript.Echo "HResult=0x" & Hex(Err.Number)
  WScript.Echo "Message=" & Err.Description
  WScript.Quit 1
End If
WScript.Echo "COM_ACTIVATION=PASS"
WScript.Echo "Version=" & app.Version
app.Quit
Set app = Nothing
