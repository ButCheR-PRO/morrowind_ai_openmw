@echo off
chcp 1251 > nul
echo ================================
echo   ПОЛНАЯ СИСТЕМА MORROWIND AI
echo ================================
echo.

REM Убиваем старые процессы
echo Очищаю старые процессы...
taskkill /f /im python.exe 2>nul
taskkill /f /im openmw.exe 2>nul
timeout /t 3 /nobreak > nul

REM Очищаем лог-файлы
echo Очищаю старые лог-файлы...
if exist "src\server\rpgaiserver.log" del /f "src\server\rpgaiserver.log" 2>nul
if exist "logs\ai_server.log" del /f "logs\ai_server.log" 2>nul

echo + Виртуальное окружение готово
echo + Все файлы найдены
echo.

REM 1. Запуск AI-сервера
echo 1/3 Запускаю AI-сервер...
start "AI Server" cmd /k "chcp 1251 > nul && cd /d %~dp0 && call venv\Scripts\activate.bat && cd src\server && python main.py --config ..\..\config.yml"

REM 2. Ждём запуска AI-сервера  
echo 2/3 Жду запуска AI-сервера (15 сек)...
timeout /t 15 /nobreak > nul

REM 3. Запуск OpenMW
echo 3/3 Запускаю OpenMW с ИИ модом...
echo.
echo ВАЖНО: В игре используй горячие клавиши:
echo   P - ping тест связи с AI
echo   I - информация о системе  
echo   O - тест диалога с ИИ
echo   Left Alt - голосовой ввод (зажать-отпустить)
echo.

REM Запускаем OpenMW (путь нужно указать свой)
start "OpenMW AI" "F:\Games\MorrowindFullrest\openmw.exe"

echo OpenMW запущен! Проверяй работу мода в игре.
echo Для запуска HTTP моста отдельно используй START_HTTP_BRIDGE.bat
echo.
pause
