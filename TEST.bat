@echo off
chcp 1251 > nul
echo ================================
echo    ТЕСТЫ
================================

if not exist "venv\Scripts\activate.bat" (
    echo ОШИБКА: Виртуальное окружение не найдено!
    pause
    exit /b 1
)

echo Активируем окружение...
call venv\Scripts\activate.bat


echo ================================
echo      ПРОВЕРКА КОНФИГУРАЦИИ
echo ================================
echo.

if not exist "venv" echo Виртуальное окружение НЕ создано
if exist "venv" echo Виртуальное окружение создано

if not exist "config.yml" echo Файл config.yml НЕ найден
if exist "config.yml" echo Файл config.yml найден

if not exist "src\server\main.py" echo Серверные файлы НЕ найдены
if exist "src\server\main.py" echo Серверные файлы найдены

if exist "venv" (
    call venv\Scripts\activate.bat
    python -c "import yaml; print('YAML библиотека работает')" 2>nul || echo YAML библиотека НЕ работает
    python -c "import requests; print('Requests библиотека работает')" 2>nul || echo Requests библиотека НЕ работает
)

echo.


echo Запускаем проверку конфигов...
python src/server/test/check_config.py

echo Запускаем проверку соединения...
python src/server/test/test_connection.py

echo Запускаем проверку VOSK...
python src/server/test/test_vosk.py

pause
