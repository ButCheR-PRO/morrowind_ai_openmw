@echo off
chcp 1251 > nul
echo ============================================================================
echo MORROWIND AI MOD - УСТАНОВКА ЗАВИСИМОСТЕЙ v1.0
echo ============================================================================
echo.

cd /d "%~dp0"

echo Текущая директория: %CD%
echo.

echo Проверяем Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ОШИБКА: Python не найден! Установите Python 3.12 из https://python.org
    echo.
    pause
    exit /b 1
)

python --version
echo Python найден успешно
echo.

echo Создаем виртуальное окружение...
if exist "venv" (
    echo Виртуальное окружение уже существует
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ОШИБКА создания виртуального окружения
        pause
        exit /b 1
    )
    echo Виртуальное окружение создано
)
echo.

echo Активируем виртуальное окружение...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ОШИБКА активации виртуального окружения
    pause
    exit /b 1
)
echo Виртуальное окружение активировано
echo.

echo Обновляем pip...
python -m pip install --upgrade pip
echo.

echo Устанавливаем зависимости...
cd src\server
pip install -r requirements.txt
if errorlevel 1 (
    echo ОШИБКА установки зависимостей
    echo Попробуйте установить зависимости вручную:
    echo    cd src\server
    echo    pip install aiohttp google-generativeai vosk elevenlabs
    pause
    exit /b 1
)
echo Все зависимости установлены
echo.

cd ..\..

echo Создаем необходимые директории...
if not exist "logs" mkdir logs
if not exist "data" mkdir data
if not exist "Data Files\ai_temp" mkdir "Data Files\ai_temp"
echo Директории созданы
echo.

echo Проверяем конфигурацию...
if not exist "config.yml" (
    echo ВНИМАНИЕ: Файл config.yml не найден
    echo Создайте config.yml с настройками API ключей
)
echo.

echo ============================================================================
echo УСТАНОВКА ЗАВЕРШЕНА УСПЕШНО!
echo ============================================================================
echo.
echo Для запуска:
echo    1. Запустите START_AI_SERVER.bat
echo    2. Запустите START_HTTP_BRIDGE.bat  
echo    3. Запустите OpenMW с модом
echo.
echo Документация: https://github.com/ButCheR-PRO/morrowind_ai_openmw/
echo.
pause
