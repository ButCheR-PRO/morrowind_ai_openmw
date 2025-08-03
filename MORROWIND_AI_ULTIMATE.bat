@echo off
chcp 1251 > nul
echo ============================================================================
echo                    MORROWIND AI ULTIMATE v2.0
echo ============================================================================
echo.
echo Универсальный инструмент для AI диалогов в Morrowind
echo.

REM Проверяем виртуальное окружение
echo Проверяем виртуальное окружение...
if not exist "venv\Scripts\activate.bat" (
    echo ОШИБКА: Виртуальное окружение не найдено!
    echo Запустите сначала INSTALL.bat
    pause
    exit /b 1
)

REM Активируем виртуальное окружение
echo Активируем виртуальное окружение...
call venv\Scripts\activate.bat

REM Проверяем AI сервер через Python вместо curl
echo Проверяем AI сервер...
python -c "import requests; r=requests.get('http://127.0.0.1:8080/api/status', timeout=3); print('OK' if r.status_code==200 else 'ERROR')" 2>nul | findstr "OK" >nul
if %errorlevel% neq 0 (
    echo.
    echo ВНИМАНИЕ: AI сервер недоступен на порту 8080
    echo Запустите START_OPENMW_AI_SERVER.bat в отдельном окне
    echo.
    echo 1 - Продолжить без AI сервера
    echo 2 - Отменить запуск
    echo.
    set /p choice="Выберите вариант (1 или 2): "
    
    if "%choice%"=="1" (
        echo Продолжаю без AI сервера...
    ) else (
        echo Запуск отменен
        pause
        exit /b 1
    )
) else (
    echo AI сервер найден и готов к работе!
)

REM Устанавливаем дополнительные модули если нужно
echo Проверяем зависимости...
python -c "import keyboard" 2>nul
if %errorlevel% neq 0 (
    echo Устанавливаю модуль keyboard для горячих клавиш...
    pip install keyboard
)

REM Запускаем приложение
echo.
echo ============================================================================
echo ЗАПУСКАЮ MORROWIND AI ULTIMATE
echo ============================================================================
echo.
echo Доступные функции:
echo - Быстрые диалоги с НПС
echo - Продвинутый чат с ИИ
echo - История диалогов и НПС
echo - Горячие клавиши (Ctrl+Alt+A, Ctrl+Alt+C, Ctrl+Alt+Q)
echo - Мониторинг и настройки
echo.

python MORROWIND_AI_ULTIMATE.py

REM Проверяем результат
if %errorlevel% neq 0 (
    echo.
    echo ОШИБКА при запуске приложения
    echo Проверьте логи и зависимости
) else (
    echo.
    echo Morrowind AI Ultimate завершен нормально
)

echo.
pause
