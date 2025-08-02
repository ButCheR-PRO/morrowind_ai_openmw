@echo off
chcp 1251 > nul
echo ================================
echo    ЗАПУСК MORROWIND AI SERVER
echo ================================
echo.

REM Проверяем наличие виртуального окружения
if not exist "venv\Scripts\activate.bat" (
    echo ОШИБКА: Виртуальное окружение не найдено!
    echo Сначала запусти INSTALL.bat
    pause
    exit /b 1
)

REM Проверяем наличие конфига
if not exist "config.yml" (
    echo ОШИБКА: Файл config.yml не найден!
    echo Создай конфиг на основе config.yml.example
    pause
    exit /b 1
)

echo Активируем виртуальное окружение...
call venv\Scripts\activate.bat

echo Проверяем зависимости...
python -c "import socket, yaml, requests" >nul 2>&1
if %errorlevel% neq 0 (
    echo ОШИБКА: Не все зависимости установлены!
    echo Запусти INSTALL.bat ещё раз
    pause
    exit /b 1
)

echo Запускаем сервер...
echo Сервер будет доступен на порту 18080
echo Для остановки нажми Ctrl+C
echo.
python src/server/main.py --config config.yml

echo.
echo Сервер остановлен.
pause
