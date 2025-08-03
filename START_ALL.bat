@echo off
chcp 1251 > nul

:menu
cls
echo ============================================================================
echo MORROWIND AI MOD - УПРАВЛЕНИЕ СИСТЕМОЙ v1.0
echo ============================================================================
echo.
echo Выберите действие:
echo.
echo [1] Запустить все сервисы
echo [2] Остановить все сервисы  
echo [3] Перезапустить систему
echo [4] Проверить статус
echo [5] Очистить логи и временные файлы
echo [6] Показать активные процессы
echo [0] Выход
echo.
set /p choice=Введите номер (0-6): 

if "%choice%"=="1" goto start_services
if "%choice%"=="2" goto stop_services
if "%choice%"=="3" goto restart_services  
if "%choice%"=="4" goto check_status
if "%choice%"=="5" goto cleanup
if "%choice%"=="6" goto show_processes
if "%choice%"=="0" goto exit
goto menu

:start_services
cls
echo ============================================================================
echo ЗАПУСК ВСЕХ СЕРВИСОВ
echo ============================================================================
echo.

cd /d "%~dp0"

echo [1/4] Проверяем готовность системы...
if not exist "venv" (
    echo ОШИБКА: Виртуальное окружение не найдено
    echo Запустите сначала INSTALL.bat
    pause
    goto menu
)

if not exist "config.yml" (
    echo ОШИБКА: config.yml не найден  
    echo Создайте конфигурационный файл
    pause
    goto menu
)

echo [2/4] Останавливаем старые процессы...
taskkill /f /im python.exe 2>nul >nul
timeout /t 2 /nobreak >nul

echo [3/4] Запускаем AI сервер (порт 9090)...
start "AI Server" cmd /k "cd /d "%~dp0" && call venv\Scripts\activate.bat && cd src\server && python main.py"
timeout /t 3 /nobreak >nul

echo [4/4] Запускаем HTTP мост (порт 8080)...  
start "HTTP Bridge" cmd /k "cd /d "%~dp0" && call venv\Scripts\activate.bat && cd src\server\test && python http_bridge.py"

echo.
echo ВСЕ СЕРВИСЫ ЗАПУЩЕНЫ!
echo.
echo Откроется 2 окна:
echo - AI Server (порт 9090) 
echo - HTTP Bridge (порт 8080)
echo.
echo Теперь можете запускать OpenMW с модом
echo.
pause
goto menu

:stop_services
cls  
echo ============================================================================
echo ОСТАНОВКА ВСЕХ СЕРВИСОВ
echo ============================================================================
echo.

echo Останавливаем Python процессы...
taskkill /f /im python.exe 2>nul
if errorlevel 1 (
    echo Нет активных Python процессов
) else (
    echo Python процессы остановлены
)

echo.
echo Закрываем окна сервисов...
taskkill /f /fi "WINDOWTITLE:AI Server*" 2>nul >nul
taskkill /f /fi "WINDOWTITLE:HTTP Bridge*" 2>nul >nul

echo.
echo Очищаем временные файлы...
if exist "Data Files\ai_temp\*.tmp" del /q "Data Files\ai_temp\*.tmp" 2>nul
if exist "Data Files\ai_temp\*.json" del /q "Data Files\ai_temp\*.json" 2>nul  
if exist "Data Files\ai_temp\*.txt" del /q "Data Files\ai_temp\*.txt" 2>nul

echo.
echo ВСЕ СЕРВИСЫ ОСТАНОВЛЕНЫ!
echo.
pause
goto menu

:restart_services
cls
echo ============================================================================  
echo ПЕРЕЗАПУСК СИСТЕМЫ
echo ============================================================================
echo.

echo Останавливаем сервисы...
call :stop_services_silent

echo Ждем завершения процессов...
timeout /t 3 /nobreak >nul

echo Запускаем сервисы...  
call :start_services_silent

echo.
echo СИСТЕМА ПЕРЕЗАПУЩЕНА!
echo.
pause
goto menu

:check_status
cls
echo ============================================================================
echo СТАТУС СИСТЕМЫ  
echo ============================================================================
echo.

echo Проверяем Python процессы...
tasklist /fi "imagename eq python.exe" 2>nul | findstr python.exe >nul
if errorlevel 1 (
    echo [СТАТУС] Python процессы: НЕ ЗАПУЩЕНЫ
) else (
    echo [СТАТУС] Python процессы: АКТИВНЫ
    tasklist /fi "imagename eq python.exe"
)

echo.
echo Проверяем порты...
netstat -an | findstr ":9090" >nul
if errorlevel 1 (
    echo [ПОРТ 9090] AI Server: НЕ СЛУШАЕТ
) else (
    echo [ПОРТ 9090] AI Server: АКТИВЕН
)

netstat -an | findstr ":8080" >nul
if errorlevel 1 (
    echo [ПОРТ 8080] HTTP Bridge: НЕ СЛУШАЕТ  
) else (
    echo [ПОРТ 8080] HTTP Bridge: АКТИВЕН
)

echo.
echo Проверяем временные файлы...
if exist "Data Files\ai_temp\ai_signal.txt" (
    echo [ФАЙЛЫ] Есть активные запросы от OpenMW
) else (
    echo [ФАЙЛЫ] Нет активных запросов
)

echo.
pause
goto menu

:cleanup
cls
echo ============================================================================
echo ОЧИСТКА СИСТЕМЫ
echo ============================================================================  
echo.

echo Очищаем логи...
if exist "logs\*.log" (
    del /q logs\*.log
    echo Логи очищены
) else (
    echo Логи уже пусты
)

echo.  
echo Очищаем временные файлы...
if exist "Data Files\ai_temp\*.*" (
    del /q "Data Files\ai_temp\*.*"  
    echo Временные файлы очищены
) else (
    echo Временные файлы уже очищены
)

echo.
echo Очищаем кэш Python...
if exist "src\server\__pycache__" (
    rmdir /s /q "src\server\__pycache__"
    echo Кэш Python очищен
)

echo.
echo ОЧИСТКА ЗАВЕРШЕНА!
echo.
pause  
goto menu

:show_processes
cls
echo ============================================================================
echo АКТИВНЫЕ ПРОЦЕССЫ
echo ============================================================================
echo.

echo Python процессы:
tasklist /fi "imagename eq python.exe" 2>nul | findstr /v "Не найдено"

echo.
echo Сетевые подключения:  
netstat -an | findstr ":8080\|:9090"

echo.
echo Окна CMD с сервисами:
tasklist /fi "imagename eq cmd.exe" /fo table

echo.
pause
goto menu

:start_services_silent
taskkill /f /im python.exe 2>nul >nul
timeout /t 2 /nobreak >nul
start "AI Server" cmd /k "cd /d "%~dp0" && call venv\Scripts\activate.bat && cd src\server && python main.py"
timeout /t 3 /nobreak >nul
start "HTTP Bridge" cmd /k "cd /d "%~dp0" && call venv\Scripts\activate.bat && cd src\server\test && python http_bridge.py"
goto :eof

:stop_services_silent
taskkill /f /im python.exe 2>nul >nul
taskkill /f /fi "WINDOWTITLE:AI Server*" 2>nul >nul  
taskkill /f /fi "WINDOWTITLE:HTTP Bridge*" 2>nul >nul
if exist "Data Files\ai_temp\*.tmp" del /q "Data Files\ai_temp\*.tmp" 2>nul
if exist "Data Files\ai_temp\*.json" del /q "Data Files\ai_temp\*.json" 2>nul
if exist "Data Files\ai_temp\*.txt" del /q "Data Files\ai_temp\*.txt" 2>nul
goto :eof

:exit
echo.
echo Завершение работы...
exit
