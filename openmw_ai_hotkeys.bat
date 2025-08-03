@echo off
chcp 1251 > nul
echo ================================
echo    HOTKEYS
================================
cd F:\morrowind_ai_openmw
call venv\Scripts\activate.bat
python "openmw_ai_hotkeys.py"
pause
timeout /t 1 > nul

