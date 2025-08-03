@echo off
chcp 1251 > nul
echo ================================
echo    УСТАНОВКА ЗАВИСИМОСТЕЙ
echo ================================
echo.

REM Проверяем Python 3.12
python3.12 --version >nul 2>&1
if errorlevel 1 (
    python --version 2>nul | findstr "3.12" >nul
    if errorlevel 1 (
        echo X Python 3.12 не найден! Установите Python 3.12+ и добавьте в PATH
        pause
        exit /b 1
    )
    set PYTHON_CMD=python
) else (
    set PYTHON_CMD=python3.12
)

echo + Python 3.12 найден: %PYTHON_CMD%
echo.

REM Создаем виртуальное окружение в корне
echo Создаю виртуальное окружение...
if exist "venv" (
    echo ! Виртуальное окружение уже существует
) else (
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        echo X Ошибка создания виртуального окружения!
        pause
        exit /b 1
    )
    echo + Виртуальное окружение создано
)

REM Активируем виртуальное окружение
echo Активирую виртуальное окружение...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo X Ошибка активации виртуального окружения!
    pause
    exit /b 1
)

echo + Виртуальное окружение активировано (Python 3.12)
echo.

REM Обновляем инструменты в venv
echo Обновляю pip, setuptools, wheel...
python -m pip install --upgrade pip setuptools wheel

REM ПЕРЕХОДИМ В ПАПКУ src/server ГДЕ ЛЕЖИТ requirements.txt
cd /d "%~dp0\src\server"
echo Перешли в папку: %CD%

REM Проверяем что requirements.txt на месте
if not exist "requirements.txt" (
    echo X requirements.txt не найден в %CD%!
    pause
    exit /b 1
)

echo + requirements.txt найден в %CD%

REM Устанавливаем критичные Windows пакеты
echo Устанавливаю Windows API пакеты...
python -m pip install pywin32 --prefer-binary
python -m pip install pynput --prefer-binary

REM Устанавливаем STT пакеты
echo Устанавливаю STT пакеты...
python -m pip install vosk --prefer-binary
python -m pip install sounddevice --prefer-binary

REM Устанавливаем LLM пакеты
echo Устанавливаю LLM провайдеры...
python -m pip install google-generativeai
python -m pip install anthropic
python -m pip install openai

REM Устанавливаю системные утилиты
echo Устанавливаю системные утилиты...
python -m pip install colorlog pathvalidate

REM ТЕПЕРЬ ПРАВИЛЬНЫЙ ПУТЬ К requirements.txt
echo Устанавливаю зависимости из requirements.txt...
python -m pip install -r requirements.txt --prefer-binary

if errorlevel 1 (
    echo.
    echo ! Некоторые пакеты не установились, но основные есть
)

echo.
echo + Установка завершена!
echo Проверяем критичные модули...

REM Проверяем что основные модули установились
python -c "import win32api; print('+ pywin32 работает')" 2>nul || echo "X pywin32 не работает"
python -c "import vosk; print('+ vosk работает')" 2>nul || echo "X vosk не работает"
python -c "import google.generativeai; print('+ gemini работает')" 2>nul || echo "X gemini не работает"

echo.
echo Теперь можно запускать:
echo - START.bat (AI-сервер)
echo - START_HTTP_BRIDGE.bat (HTTP-мост)
echo - START_ALL.bat (оба сервиса)
echo.
echo ВАЖНО: requirements.txt обработан из src\server\
echo.
pause
