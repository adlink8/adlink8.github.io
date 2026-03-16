Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get tools directory and project root
toolsPath = fso.GetParentFolderName(WScript.ScriptFullName)
projectRoot = fso.GetParentFolderName(toolsPath)

' Create shortcut in project root
Set shortcut = WshShell.CreateShortcut(fso.BuildPath(projectRoot, "Blog Manager.lnk"))
shortcut.TargetPath = fso.BuildPath(toolsPath, "launch.vbs")
shortcut.WorkingDirectory = projectRoot
shortcut.IconLocation = "C:\Windows\System32\shell32.dll,15"
shortcut.Description = "Hugo Blog Manager"
shortcut.Save

WScript.Echo "Shortcut created: " & fso.BuildPath(projectRoot, "Blog Manager.lnk")
