@echo off
chcp 1251 > nul
echo ============================================================================
echo MORROWIND AI MOD - ПОЛНАЯ ДИАГНОСТИКА СИСТЕМЫ v1.4
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
    echo [ОШИБКА] config.yml не найден в корне
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

REM ПРАВИЛЬНАЯ ПРОВЕРКА - файлы из твоего репо
echo [ДОПОЛНИТЕЛЬНО] Проверяем Lua скрипты в репо:

if not exist "src\Data Files\morrowind_ai.omwscripts" (
    echo [ОШИБКА] morrowind_ai.omwscripts не найден в репо
    set /a ERROR_COUNT+=1
) else (
    echo [OK] morrowind_ai.omwscripts найден в репо
)

if not exist "src\Data Files\scripts\morrowind_ai.lua" (
    echo [ОШИБКА] scripts/morrowind_ai.lua не найден в репо
    set /a ERROR_COUNT+=1
) else (
    echo [OK] scripts/morrowind_ai.lua найден в репо
)

if not exist "src\Data Files\scripts\morrowind_ai\init.lua" (
    echo [ОШИБКА] scripts/morrowind_ai/init.lua не найден в репо
    set /a ERROR_COUNT+=1
) else (
    echo [OK] scripts/morrowind_ai/init.lua найден в репо
)

if not exist "src\Data Files\scripts\morrowind_ai\player.lua" (
    echo [ОШИБКА] scripts/morrowind_ai/player.lua не найден в репо
    set /a ERROR_COUNT+=1
) else (
    echo [OK] scripts/morrowind_ai/player.lua найден в репо
)

if not exist "src\Data Files\scripts\morrowind_ai\console_commands.lua" (
    echo [ОШИБКА] scripts/morrowind_ai/console_commands.lua не найден в репо
    set /a ERROR_COUNT+=1
) else (
    echo [OK] scripts/morrowind_ai/console_commands.lua найден в репо
)

if not exist "src\Data Files\scripts\morrowind_ai\config.lua" (
    echo [ОШИБКА] scripts/morrowind_ai/config.lua не найден в репо
    set /a ERROR_COUNT+=1
) else (
    echo [OK] scripts/morrowind_ai/config.lua найден в репо
)

echo.
echo [ДОПОЛНИТЕЛЬНО] Проверяем установку в игру:

if exist "f:\Games\MorrowindFullrest\game\Data Files\morrowind_ai.omwscripts" (
    echo [OK] morrowind_ai.omwscripts установлен в игру
) else (
    echo [ПРЕДУПРЕЖДЕНИЕ] morrowind_ai.omwscripts НЕ УСТАНОВЛЕН в игру
    echo                   Запустите COPY_TO_GAME.bat
)

if exist "f:\Games\MorrowindFullrest\game\Data Files\scripts\morrowind_ai" (
    echo [OK] Папка скриптов AI создана в игре
    
    if exist "f:\Games\MorrowindFullrest\game\Data Files\scripts\morrowind_ai\init.lua" (
        echo [OK] init.lua установлен в игру
    ) else (
        echo [ПРЕДУПРЕЖДЕНИЕ] init.lua НЕ УСТАНОВЛЕН в игру
    )
    
    if exist "f:\Games\MorrowindFullrest\game\Data Files\scripts\morrowind_ai\player.lua" (
        echo [OK] player.lua установлен в игру
    ) else (
        echo [ПРЕДУПРЕЖДЕНИЕ] player.lua НЕ УСТАНОВЛЕН в игру
    )
    
    if exist "f:\Games\MorrowindFullrest\game\Data Files\scripts\morrowind_ai\console_commands.lua" (
        echo [OK] console_commands.lua установлен в игру
    ) else (
        echo [ПРЕДУПРЕЖДЕНИЕ] console_commands.lua НЕ УСТАНОВЛЕН в игру
    )
    
) else (
    echo [ПРЕДУПРЕЖДЕНИЕ] Папка скриптов AI НЕ НАЙДЕНА в игре
    echo                   Запустите COPY_TO_GAME.bat
)
echo.

echo [3/10] Проверяем директории...
if not exist "logs" (
    mkdir logs
    echo [ИСПРАВЛЕНО] Создана директория logs
) else (
    echo [OK] Директория logs готова
)

if not exist "data" (
    mkdir data
    echo [ИСПРАВЛЕНО] Создана директория data
) else (
    echo [OK] Директория data готова
)

if not exist "f:\Games\MorrowindFullrest\game\Data Files\ai_temp" (
    mkdir "f:\Games\MorrowindFullrest\game\Data Files\ai_temp"
    echo [ИСПРАВЛЕНО] Создана директория ai_temp в игре
) else (
    echo [OK] Директория ai_temp готова
)
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
    
    pip show pathvalidate >nul 2>&1
    if errorlevel 1 (
        echo [ОШИБКА] pathvalidate не установлен - КРИТИЧЕСКИЙ ПАКЕТ!
        set /a ERROR_COUNT+=1
    ) else (
        echo [OK] pathvalidate установлен
    )
    
    pip show vosk >nul 2>&1
    if errorlevel 1 (
        echo [ПРЕДУПРЕЖДЕНИЕ] vosk не установлен
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
python -c "import py_compile; py_compile.compile('src/server/main.py', doraise=True)" >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Синтаксическая ошибка в main.py
    set /a ERROR_COUNT+=1
) else (
    echo [OK] main.py синтаксически корректен
)

if exist "src\server\test\http_bridge.py" (
    python -c "import py_compile; py_compile.compile('src/server/test/http_bridge.py', doraise=True)" >nul 2>&1
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
echo test > "f:\Games\MorrowindFullrest\game\Data Files\ai_temp\test.tmp"
if exist "f:\Games\MorrowindFullrest\game\Data Files\ai_temp\test.tmp" (
    del "f:\Games\MorrowindFullrest\game\Data Files\ai_temp\test.tmp"
    echo [OK] Запись в ai_temp работает
) else (
    echo [ОШИБКА] Не удается записать в ai_temp
    set /a ERROR_COUNT+=1
)
echo.

echo [10/10] Проверяем OpenMW совместимость...
if exist "f:\Games\MorrowindFullrest\game\OpenMW 0.49.0\openmw.exe" (
    echo [OK] OpenMW найден по указанному пути
) else (
    echo [ПРЕДУПРЕЖДЕНИЕ] OpenMW не найден по пути f:\Games\MorrowindFullrest\game\OpenMW 0.49.0\openmw.exe
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
    if not exist "f:\Games\MorrowindFullrest\game\Data Files\morrowind_ai.omwscripts" echo - Запустите COPY_TO_GAME.bat для установки файлов в игру
    if %ERROR_COUNT% gtr 5 echo - Переустановите проект с нуля
)

echo ============================================================================
echo.
pause
