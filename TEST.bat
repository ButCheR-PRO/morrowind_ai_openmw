@echo off
chcp 1251 > nul
echo ============================================================================
echo MORROWIND AI MOD - ПОЛНАЯ ДИАГНОСТИКА СИСТЕМЫ v1.0
echo ============================================================================
echo.

cd /d "%~dp0"

set ERROR_COUNT=0

echo [1/10] Проверяем Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Python не найден! Установите Python 3.12
    set /a ERROR_COUNT+=1
) else (
    python --version
    echo [OK] Python найден и работает
)
echo.

echo [2/10] Проверяем структуру проекта...
if not exist "config.yml" (
    echo [ОШИБКА] config.yml не найден
    set /a ERROR_COUNT+=1
) else (
    echo [OK] Конфигурационный файл найден
)

if not exist "venv" (
    echo [ОШИБКА] Виртуальное окружение не найдено - запустите INSTALL.bat
    set /a ERROR_COUNT+=1
) else (
    echo [OK] Виртуальное окружение существует
)

if not exist "src\server\main.py" (
    echo [ОШИБКА] AI сервер не найден
    set /a ERROR_COUNT+=1
) else (
    echo [OK] AI сервер найден
)

if not exist "src\server\test\http_bridge.py" (
    echo [ОШИБКА] HTTP мост не найден  
    set /a ERROR_COUNT+=1
) else (
    echo [OK] HTTP мост найден
)

if not exist "src\Data Files\scripts\morrowind_ai.lua" (
    echo [ОШИБКА] Lua скрипт не найден
    set /a ERROR_COUNT+=1
) else (
    echo [OK] Lua скрипт найден
)

if not exist "morrowind_ai.omwscripts" (
    echo [ОШИБКА] Файл регистрации мода не найден
    set /a ERROR_COUNT+=1
) else (
    echo [OK] Файл регистрации мода найден
)
echo.

echo [3/10] Проверяем директории...
if not exist "logs" mkdir logs
echo [OK] Директория logs готова

if not exist "data" mkdir data  
echo [OK] Директория data готова

if not exist "Data Files\ai_temp" mkdir "Data Files\ai_temp"
echo [OK] Директория ai_temp готова
echo.

echo [4/10] Тестируем виртуальное окружение...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ОШИБКА] Не удается активировать venv
    set /a ERROR_COUNT+=1
) else (
    echo [OK] Виртуальное окружение активировано
    
    echo [5/10] Проверяем Python пакеты...
    pip show aiohttp >nul 2>&1
    if errorlevel 1 (
        echo [ОШИБКА] aiohttp не установлен
        set /a ERROR_COUNT+=1
    ) else (
        echo [OK] aiohttp установлен
    )
    
    pip show google-generativeai >nul 2>&1
    if errorlevel 1 (
        echo [ОШИБКА] google-generativeai не установлен
        set /a ERROR_COUNT+=1
    ) else (
        echo [OK] google-generativeai установлен
    )
    
    pip show vosk >nul 2>&1
    if errorlevel 1 (
        echo [ОШИБКА] vosk не установлен
        set /a ERROR_COUNT+=1
    ) else (
        echo [OK] vosk установлен
    )
)
echo.

echo [6/10] Проверяем конфигурацию...
if exist "config.yml" (
    findstr /i "gemini" config.yml >nul
    if errorlevel 1 (
        echo [ПРЕДУПРЕЖДЕНИЕ] API ключ Gemini не найден в config.yml
    ) else (
        echo [OK] Конфигурация Gemini найдена
    )
) else (
    echo [ОШИБКА] Файл config.yml отсутствует
    set /a ERROR_COUNT+=1
)
echo.

echo [7/10] Тестируем синтаксис Python скриптов...
python -m py_compile src\server\main.py >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Синтаксическая ошибка в main.py
    set /a ERROR_COUNT+=1
) else (
    echo [OK] main.py синтаксически корректен
)

if exist "src\server\test\http_bridge.py" (
    python -m py_compile src\server\test\http_bridge.py >nul 2>&1
    if errorlevel 1 (
        echo [ОШИБКА] Синтаксическая ошибка в http_bridge.py
        set /a ERROR_COUNT+=1
    ) else (
        echo [OK] http_bridge.py синтаксически корректен
    )
)
echo.

echo [8/10] Проверяем порты...
netstat -an | findstr ":9090" >nul
if not errorlevel 1 (
    echo [ПРЕДУПРЕЖДЕНИЕ] Порт 9090 уже занят
) else (
    echo [OK] Порт 9090 свободен
)

netstat -an | findstr ":8080" >nul  
if not errorlevel 1 (
    echo [ПРЕДУПРЕЖДЕНИЕ] Порт 8080 уже занят
) else (
    echo [OK] Порт 8080 свободен
)
echo.

echo [9/10] Тестируем временные файлы...
echo test > "Data Files\ai_temp\test.tmp"
if exist "Data Files\ai_temp\test.tmp" (
    del "Data Files\ai_temp\test.tmp"
    echo [OK] Запись в ai_temp работает
) else (
    echo [ОШИБКА] Не удается записать в ai_temp
    set /a ERROR_COUNT+=1
)
echo.

echo [10/10] Проверяем OpenMW совместимость...
if exist "C:\Program Files\OpenMW\openmw.exe" (
    echo [OK] OpenMW найден в стандартной папке
) else if exist "openmw.exe" (
    echo [OK] OpenMW найден в текущей папке  
) else (
    echo [ПРЕДУПРЕЖДЕНИЕ] OpenMW не найден в стандартных местах
)
echo.

echo ============================================================================
echo ИТОГОВЫЙ ОТЧЕТ
echo ============================================================================

if %ERROR_COUNT%==0 (
    echo СТАТУС: ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!
    echo Система полностью готова к работе
    echo.
    echo Для запуска используйте START_ALL.bat
) else (
    echo СТАТУС: ОБНАРУЖЕНО ОШИБОК: %ERROR_COUNT%
    echo.
    echo РЕКОМЕНДАЦИИ:
    if not exist "venv" echo - Запустите INSTALL.bat для установки зависимостей
    if not exist "config.yml" echo - Создайте config.yml с API ключами
    if %ERROR_COUNT% gtr 5 echo - Переустановите проект с нуля
)

echo ============================================================================
echo.
pause
