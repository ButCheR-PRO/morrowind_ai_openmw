@echo off
chcp 1251 > nul
echo ================================
echo    ЗАПУСК ВСЕХ СЕРВИСОВ
echo ================================
echo.

REM Проверяем наличие виртуального окружения в корне
if not exist "venv\Scripts\activate.bat" (
    echo X Виртуальное окружение не найдено!
    echo Сначала запустите INSTALL.bat
    pause
    exit /b 1
)

REM Проверяем что все файлы на месте
if not exist "src\server\main.py" (
    echo X main.py не найден в src\server\!
    pause
    exit /b 1
)

if not exist "src\server\test\http_bridge.py" (
    echo X http_bridge.py не найден в src\server\test\!
    pause
    exit /b 1
)

if not exist "config.yml" (
    echo X config.yml не найден в корне!
    pause
    exit /b 1
)

echo + Все файлы найдены
echo + Виртуальное окружение готово
echo.

REM Запуск AI-сервера в отдельном окне с правильными путями И config.yml
echo Запускаю AI-сервер с config.yml...
start "AI Server" cmd /k "chcp 1251 > nul && cd /d %~dp0 && call venv\Scripts\activate.bat && cd src\server && python main.py --config ..\..\config.yml"

REM Ждем 10 секунд чтобы AI-сервер успел запуститься
echo Жду запуска AI-сервера (10 сек)...
timeout /t 10 /nobreak > nul

REM Активируем venv и запускаем HTTP-мост с правильным путем
call venv\Scripts\activate.bat
echo Запускаю HTTP-мост...
cd /d "%~dp0\src\server\test"
python http_bridge.py

pause
