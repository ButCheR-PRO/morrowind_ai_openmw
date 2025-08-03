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

echo Запускаем проверку AI-сервера...
echo ================================
echo     ТЕСТ AI-СЕРВЕРА
echo ================================

REM Запускаем AI-сервер в фоне для теста
start /b "" cmd /c "cd src\server && python main.py --config ..\..\config.yml > ..\..\logs\test_server.log 2>&1"

REM Ждём 15 секунд чтобы сервер запустился
echo Жду запуска AI-сервера (15 сек)...
timeout /t 15 /nobreak > nul

REM Проверяем что AI-сервер запустился
curl -s http://127.0.0.1:18080/health > nul 2>&1
if errorlevel 1 (
    echo X AI-сервер не запустился на порту 18080
    echo Проверяем лог...
    if exist "logs\test_server.log" (
        echo === ЛОГ AI-СЕРВЕРА ===
        type logs\test_server.log
    )
) else (
    echo + AI-сервер запустился на порту 18080!
)

REM Останавливаем тестовый сервер
taskkill /f /im python.exe 2>nul

echo Запускаем проверку соединения...
cd src\server\test
python test_connection.py
cd ..\..\..

echo Запускаем проверку VOSK...
cd src\server\test
python test_vosk.py
cd ..\..\..

echo ================================
echo + ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ!
echo ================================
pause
goto :end

:error
echo ================================
echo X КРИТИЧЕСКАЯ ОШИБКА В ТЕСТАХ!
echo ================================
pause

:end
