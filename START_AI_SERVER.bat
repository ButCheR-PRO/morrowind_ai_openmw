@echo off
chcp 1251 > nul
echo ============================================================================
echo ЗАПУСК AI СЕРВЕРА MORROWIND (порт 9090)
echo ============================================================================
echo.

cd /d "%~dp0"

echo Активируем виртуальное окружение...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ОШИБКА: Не удалось активировать виртуальное окружение
    echo Запустите сначала INSTALL.bat
    pause
    exit /b 1
)

echo Проверяем конфигурацию...
if not exist "config.yml" (
    echo ОШИБКА: config.yml не найден
    echo Создайте файл config.yml с API ключами
    pause
    exit /b 1
)

echo Запускаем AI сервер на порту 9090...
cd src\server
python main.py

if errorlevel 1 (
    echo ОШИБКА запуска AI сервера
    echo Проверьте логи в папке logs/
)

echo.
echo AI сервер остановлен
pause
