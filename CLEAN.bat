@echo off
chcp 1251 > nul
echo Удаляем виртуальное окружение...
if exist "venv" rmdir /s /q venv
echo Очистка завершена.
pause
