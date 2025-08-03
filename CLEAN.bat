@echo off
chcp 1251 > nul
echo Удаляем виртуальное окружение...
if exist "venv" rmdir /s /q venv
cd src\server
for /d %%i in (0.* 1.* 3.* 6.* 20*) do rmdir /s /q "%%i"

echo Очистка завершена.
pause
