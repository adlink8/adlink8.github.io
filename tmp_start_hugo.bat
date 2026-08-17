@echo off
cd /d "D:\ADLINK\Myproject\adlink8.github.io"
start "" "D:\ADLINK\Myproject\hugo-bin\hugo.exe" server -D --port 1313 --bind 127.0.0.1
