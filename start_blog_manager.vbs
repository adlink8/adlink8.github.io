Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\li\adlink8.github.io"
WshShell.Run "pythonw blog_manager.py", 0, False
