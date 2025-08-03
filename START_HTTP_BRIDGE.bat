@echo off
chcp 1251 > nul
echo ================================
echo    HTTP BRIDGE СЕРВЕР
echo ================================
echo.

REM Проверяем наличие виртуального окружения в корне
if not exist "venv\Scripts\activate.bat" (
    echo X Виртуальное окружение не найдено!
    echo Сначала запустите INSTALL.bat
    pause
    exit /b 1
)

REM Активируем виртуальное окружение
echo Активирую виртуальное окружение...
call venv\Scripts\activate.bat

REM ПЕРЕХОДИМ В ПАПКУ src\server\test ГДЕ ЛЕЖИТ http_bridge.py
cd /d "%~dp0\src\server\test"
echo Перешли в папку: %CD%

REM Проверяем что http_bridge.py на месте
if not exist "http_bridge.py" (
    echo X http_bridge.py не найден в %CD%!
    pause
    exit /b 1
)

REM Запускаем HTTP мост
echo Запускаю HTTP мост http_bridge.py на порту 8080...
echo Для остановки закрой это окно
echo.
python http_bridge.py

pause
