@echo off
chcp 1251 > nul

REM ������ AI-�������
start "AI Server" cmd /k "cd /d %~dp0\src\server && python main.py"
timeout /t 5

REM ������ HTTP-�����
cd /d "%~dp0\src\server\test"
python http_bridge.py

pause
