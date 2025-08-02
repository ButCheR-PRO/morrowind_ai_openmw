@echo off
chcp 1251 >nul

echo ================================
echo     HTTP BRIDGE СЕРВЕР
================================

if not exist "venv\Scripts\activate.bat" (
    echo ОШИБКА: Виртуальное окружение не найдено!
    pause
    exit /b 1
)

echo Активируем окружение...
call venv\Scripts\activate.bat

echo Запускаем HTTP мост на порту 8080...
echo Для остановки закрой это окно
echo.

:restart
python src/server/test/http_bridge.py
echo HTTP мост остановлен. Перезапуск через 3 сек...
timeout /t 3 /nobreak >nul
goto restart
