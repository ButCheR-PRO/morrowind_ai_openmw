@echo off
chcp 1251 > nul
echo ============================================================================
echo ЗАПУСК OPENMW AI СЕРВЕРА (порт 8080)
echo ============================================================================
echo.

REM Активируем виртуальное окружение
echo Активируем виртуальное окружение...
if not exist "venv\Scripts\activate.bat" (
    echo ОШИБКА: Виртуальное окружение не найдено!
    echo Запустите сначала INSTALL.bat
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

REM Проверяем наличие config.yml
echo Проверяем конфигурацию...
if not exist "config.yml" (
    echo ОШИБКА: Файл config.yml не найден!
    pause
    exit /b 1
)

REM Переходим в папку сервера
cd src\server

REM Запускаем OpenMW AI сервер
echo Запускаю OpenMW AI сервер на порту 8080...
echo Команда: python openmw_ai_server.py
echo.

python openmw_ai_server.py

REM Проверяем результат запуска
if %errorlevel% neq 0 (
    echo.
    echo ОШИБКА запуска OpenMW AI сервера
    echo Проверьте логи и конфигурацию
) else (
    echo OpenMW AI сервер остановлен нормально
)

echo.
pause
