@echo off
echo ================================
echo    ТЕСТ VOSK
================================

if not exist "venv\Scripts\activate.bat" (
    echo ОШИБКА: Виртуальное окружение не найдено!
    pause
    exit /b 1
)

echo Активируем окружение...
call venv\Scripts\activate.bat

echo Запускаем проверку конфигов...
python src/server/test/check_config.py

echo Запускаем проверку соединения...
python src/server/test/test_connection.py

echo Запускаем проверку VOSK...
python src/server/test/test_vosk.py

pause
