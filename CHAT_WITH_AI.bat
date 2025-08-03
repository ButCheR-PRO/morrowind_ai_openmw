@echo off
chcp 1251 > nul
echo ================================
echo    CHAT
================================
cd F:\morrowind_ai_openmw
call venv\Scripts\activate.bat
python "CHAT_WITH_AI.py"
pause
timeout /t 1 > nul

