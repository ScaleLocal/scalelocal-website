' Launches autodeploy.bat with NO visible console window.
' WScript.Shell.Run window style 0 = hidden.
Dim fso, sh, here
Set fso = CreateObject("Scripting.FileSystemObject")
here = fso.GetParentFolderName(WScript.ScriptFullName)
Set sh = CreateObject("WScript.Shell")
sh.CurrentDirectory = here
sh.Run "cmd /c """ & here & "\autodeploy.bat""", 0, False
