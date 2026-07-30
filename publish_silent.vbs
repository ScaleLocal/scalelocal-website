' Launches daily_publish.bat with NO visible console window.
Dim fso, sh, here
Set fso = CreateObject("Scripting.FileSystemObject")
here = fso.GetParentFolderName(WScript.ScriptFullName)
Set sh = CreateObject("WScript.Shell")
sh.CurrentDirectory = here
sh.Run "cmd /c """ & here & "\daily_publish.bat""", 0, False
