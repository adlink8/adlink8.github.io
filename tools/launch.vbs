Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get the project root directory (parent of tools folder)
scriptPath = fso.GetParentFolderName(WScript.ScriptFullName)
projectRoot = fso.GetParentFolderName(scriptPath)

' Change to project root and run the Python script
WshShell.CurrentDirectory = projectRoot
WshShell.Run "pythonw tools\blog_manager.py", 0, False
