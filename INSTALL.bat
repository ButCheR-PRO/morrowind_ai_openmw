@echo off
chcp 1251 > nul
echo ================================
echo   УСТАНОВКА MORROWIND AI SERVER
echo ================================
echo.

REM Проверяем наличие Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ОШИБКА: Python не найден! Установи Python 3.11+
    pause
    exit /b 1
)

REM Удаляем старое виртуальное окружение если есть
if exist "venv" (
    echo Удаляем старое виртуальное окружение...
    rmdir /s /q venv
)

echo Создаём новое виртуальное окружение...
python -m venv venv
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось создать виртуальное окружение!
    pause
    exit /b 1
)

echo Активируем виртуальное окружение...
call venv\Scripts\activate.bat

echo Обновляем pip до последней версии...
python -m pip install --upgrade pip

echo Устанавливаем зависимости...
pip install -r src/server/requirements.txt
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось установить зависимости!
    echo Проверь файл src/server/requirements.txt
    pause
    exit /b 1
)

echo.
echo ================================
echo   УСТАНОВКА ЗАВЕРШЕНА УСПЕШНО!
echo ================================
echo Теперь можешь запускать START.bat
echo.
pause
