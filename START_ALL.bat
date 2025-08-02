@echo off
chcp 1251 > nul

REM Запуск AI-сервера
start "AI Server" cmd /k "cd /d %~dp0\src\server && python main.py"
timeout /t 5

REM Запуск HTTP-моста
cd /d "%~dp0\src\server\test"
python http_bridge.py

pause
