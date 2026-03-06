Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
scriptPath = fso.GetParentFolderName(WScript.ScriptFullName)

' Change to that directory and run the Python script
WshShell.CurrentDirectory = scriptPath
WshShell.Run "pythonw blog_manager.py", 0, False
