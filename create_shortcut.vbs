Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get script directory
scriptPath = fso.GetParentFolderName(WScript.ScriptFullName)

' Create shortcut
Set shortcut = WshShell.CreateShortcut(fso.BuildPath(scriptPath, "Blog Manager.lnk"))
shortcut.TargetPath = fso.BuildPath(scriptPath, "launch.vbs")
shortcut.WorkingDirectory = scriptPath
shortcut.IconLocation = "C:\Windows\System32\shell32.dll,15"
shortcut.Description = "Hugo Blog Manager"
shortcut.Save

WScript.Echo "Shortcut created: " & fso.BuildPath(scriptPath, "Blog Manager.lnk")
