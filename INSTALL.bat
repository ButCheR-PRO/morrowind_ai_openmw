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

REM Создаём виртуальное окружение в корне проекта
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
    echo + Виртуальное окружение создано в корне
)

REM Активируем виртуальное окружение
echo Активирую виртуальное окружение...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo X Ошибка активации виртуального окружения!
    pause
    exit /b 1
)

REM Проверяем что в venv используется Python 3.12
python --version | findstr "3.12" >nul
if errorlevel 1 (
    echo X В виртуальном окружении не Python 3.12!
    echo Текущая версия:
    python --version
    pause
    exit /b 1
)

echo + Виртуальное окружение активировано (Python 3.12)
echo.

REM Обновляем базовые инструменты в venv
echo Обновляю pip, setuptools, wheel...
python -m pip install --upgrade pip setuptools wheel

REM ПЕРЕХОДИМ В src/server где лежит requirements.txt
cd /d "%~dp0src\server"
echo Перешли в папку: %CD%

REM Проверяем что requirements.txt на месте
if not exist "requirements.txt" (
    echo X requirements.txt не найден в %CD%!
    echo Проверь структуру проекта!
    pause
    exit /b 1
)

echo + requirements.txt найден в %CD%
echo.

REM ================================
REM УСТАНАВЛИВАЕМ КРИТИЧНЫЕ ПАКЕТЫ ПО ОТДЕЛЬНОСТИ
REM (чтобы избежать падений из-за отсутствующих модулей)
REM ================================

echo Устанавливаю критичные Windows API пакеты...
python -m pip install pywin32==306 --prefer-binary
python -m pip install pynput>=1.7.0 --prefer-binary

echo Устанавливаю STT пакеты для распознавания речи...
python -m pip install vosk>=0.3.45 --prefer-binary
python -m pip install sounddevice>=0.4.6 --prefer-binary

echo Устанавливаю OpenAI Whisper (может занять время)...
python -m pip install openai-whisper>=20231117 --prefer-binary
if errorlevel 1 (
    echo ! OpenAI Whisper не установился, пробуем без привязки к версии...
    python -m pip install openai-whisper --prefer-binary
)

echo Устанавливаю все LLM провайдеры...
python -m pip install mistralai>=0.1.0
python -m pip install anthropic>=0.8.0  
python -m pip install google-generativeai>=0.3.0
python -m pip install openai>=1.0.0

echo Устанавливаю системные утилиты...
python -m pip install colorlog>=6.7.0
python -m pip install pathvalidate>=3.0.0

echo Устанавливаю numpy отдельно...
python -m pip install numpy>=1.25.0 --prefer-binary

echo.
echo ================================
echo Устанавливаю остальные зависимости из requirements.txt...
echo ================================

REM Теперь устанавливаем остальное из requirements.txt
python -m pip install -r requirements.txt --prefer-binary

if errorlevel 1 (
    echo.
    echo ! Некоторые пакеты из requirements.txt не установились
    echo Но основные критичные модули установлены
)

echo.
echo ================================
echo Проверяю установку критичных модулей...
echo ================================

REM Проверяем что ВСЕ критичные модули установились
python -c "import win32api; print('+ pywin32 (win32api) работает')" 2>nul || echo "X pywin32 НЕ РАБОТАЕТ!"
python -c "import pynput; print('+ pynput работает')" 2>nul || echo "X pynput НЕ РАБОТАЕТ!"
python -c "import vosk; print('+ vosk работает')" 2>nul || echo "X vosk НЕ РАБОТАЕТ!"
python -c "import whisper; print('+ openai-whisper работает')" 2>nul || echo "X whisper НЕ РАБОТАЕТ!"
python -c "import mistralai; print('+ mistralai работает')" 2>nul || echo "X mistralai НЕ РАБОТАЕТ!"
python -c "import anthropic; print('+ anthropic работает')" 2>nul || echo "X anthropic НЕ РАБОТАЕТ!"
python -c "import google.generativeai; print('+ google-generativeai работает')" 2>nul || echo "X gemini НЕ РАБОТАЕТ!"
python -c "import openai; print('+ openai работает')" 2>nul || echo "X openai НЕ РАБОТАЕТ!"
python -c "import colorlog; print('+ colorlog работает')" 2>nul || echo "X colorlog НЕ РАБОТАЕТ!"
python -c "import pathvalidate; print('+ pathvalidate работает')" 2>nul || echo "X pathvalidate НЕ РАБОТАЕТ!"

echo.
echo ================================
echo УСТАНОВКА ЗАВЕРШЕНА!
echo ================================
echo.
echo Теперь можно запускать:
echo - START.bat (только AI-сервер)
echo - START_HTTP_BRIDGE.bat (только HTTP-мост)  
echo - START_ALL.bat (оба сервиса сразу)
echo.
echo ВАЖНО: Всё установлено в виртуальное окружение venv
echo requirements.txt обработан из src\server\requirements.txt
echo.
pause
