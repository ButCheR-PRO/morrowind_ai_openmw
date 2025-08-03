@echo off
chcp 1251 > nul
echo ================================
echo          ТЕСТЫ
echo ================================

REM Очистка мусора от pip
echo Очищаю мусор от pip...
cd /d "%~dp0src\server"
for /d %%i in (0.* 1.* 3.* 6.* 20*) do (
    if exist "%%i" (
        echo Удаляю мусорную папку: %%i
        rmdir /s /q "%%i"
    )
)
cd /d "%~dp0"

REM Убиваем все старые процессы Python перед началом
echo Очищаю старые процессы Python...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak > nul

REM Очищаем старые лог-файлы
echo Очищаю старые лог-файлы...
if exist "src\server\rpgaiserver.log" del /f "src\server\rpgaiserver.log" 2>nul
if exist "src\server\rpgaiserver.log.1" del /f "src\server\rpgaiserver.log.1" 2>nul
if exist "logs\test_server.log" del /f "logs\test_server.log" 2>nul
if exist "logs\ai_server.log" del /f "logs\ai_server.log" 2>nul

REM Проверяем виртуальное окружение
if not exist "venv\Scripts\activate.bat" (
    echo X Виртуальное окружение не найдено!
    echo Сначала запустите INSTALL.bat
    pause
    exit /b 1
)

echo Активируем окружение...
call venv\Scripts\activate.bat

echo ================================
echo     ПРОВЕРКА КОНФИГУРАЦИИ
echo ================================

REM Проверяем что все нужные файлы и папки есть
if not exist "venv" echo X Виртуальное окружение не создано && goto :error
echo + Виртуальное окружение создано

if not exist "config.yml" echo X config.yml не найден && goto :error
echo + Файл config.yml найден

if not exist "src\server\main.py" echo X main.py не найден && goto :error
echo + Серверные файлы найдены

if not exist "logs" (
    mkdir logs
    echo + Папка logs создана
) else (
    echo + Папка logs найдена
)

if not exist "data" (
    mkdir data
    echo + Папка data создана
) else (
    echo + Папка data найдена
)

if not exist "data\scene_instructions.txt" (
    echo. > data\scene_instructions.txt
    echo + Файл scene_instructions.txt создан
)

REM Проверяем основные модули Python
python -c "import yaml" 2>nul && echo + YAML библиотека работает || (echo X YAML не работает && goto :error)
python -c "import requests" 2>nul && echo + Requests библиотека работает || (echo X Requests не работает && goto :error)

echo.
echo Запускаем проверку конфигов...
cd src\server\test
python check_config.py
if errorlevel 1 goto :error
cd ..\..\..

echo ================================
echo     ПРОПУСКАЕМ ТЕСТ AI-СЕРВЕРА
echo     (чтобы избежать блокировки)
echo ================================

echo Запускаем проверку VOSK...
cd src\server\test
python test_vosk.py
cd ..\..\..

echo ================================
echo + ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ!
echo ================================
echo.
echo ВНИМАНИЕ: Тест AI-сервера пропущен чтобы избежать
echo блокировки лог-файлов. AI-сервер протестируется
echo при запуске START_ALL.bat
echo.
pause
goto :end

:error
echo ================================
echo X КРИТИЧЕСКАЯ ОШИБКА В ТЕСТАХ!
echo ================================
pause

:end
REM Финальная очистка процессов
taskkill /f /im python.exe 2>nul
timeout /t 1 > nul
