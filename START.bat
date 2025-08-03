@echo off
chcp 1251 > nul
echo ================================
echo       AI-СЕРВЕР
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

REM ПЕРЕХОДИМ В ПАПКУ src\server ГДЕ ЛЕЖИТ main.py
cd /d "%~dp0\src\server"
echo Перешли в папку: %CD%

REM Проверяем что main.py на месте
if not exist "main.py" (
    echo X main.py не найден в %CD%!
    pause
    exit /b 1
)

REM Проверяем что config.yml есть в корне (на 2 уровня выше)
if not exist "..\..\config.yml" (
    echo X config.yml не найден в корне репозитория!
    pause
    exit /b 1
)

REM Запускаем AI-сервер с указанием пути к config.yml
echo Запускаю AI-сервер main.py с config.yml...
echo Для остановки нажмите Ctrl+C
echo.
python main.py --config ..\..\config.yml

pause
