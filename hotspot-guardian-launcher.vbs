' Set objShell = CreateObject("Shell.Application")
' Set objFSO = CreateObject("Scripting.FileSystemObject")
' strPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
' objShell.ShellExecute "pythonw", """" & strPath & "\hotspot_guardian.pyw""", "", "runas", 0


Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Ensure the script is run as administrator
If Not WScript.Arguments.Named.Exists("elevated") Then
  CreateObject("Shell.Application").ShellExecute "wscript.exe", Chr(34) & WScript.ScriptFullName & Chr(34) & " /elevated", "", "runas", 1
  WScript.Quit
End If

' Run the Python script without showing the console window
objShell.Run "pythonw.exe hotspot_guardian_v2.pyw", 0, False