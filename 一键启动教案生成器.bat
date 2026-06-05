@echo off
chcp 65001 >nul
cd /d %USERPROFILE%\lesson_app
start "" http://localhost:5000
python server.py
pause
