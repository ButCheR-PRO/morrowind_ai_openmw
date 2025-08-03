@echo off
chcp 1251 > nul
echo ================================
echo    ������ ���� ��������
echo ================================
echo.

REM ������� ��� ������ �������� Python
echo ������ ������ �������� Python...
taskkill /f /im python.exe 2>nul
timeout /t 3 /nobreak > nul

REM ������� ���-����� ������� ����� ���� �������������
echo ������ ������ ���-�����...
if exist "src\server\rpgaiserver.log" del /f "src\server\rpgaiserver.log" 2>nul
if exist "src\server\rpgaiserver.log.1" del /f "src\server\rpgaiserver.log.1" 2>nul

REM ��������� ������� ������������ ��������� � �����
if not exist "venv\Scripts\activate.bat" (
    echo X ����������� ��������� �� �������!
    echo ������� ��������� INSTALL.bat
    pause
    exit /b 1
)

REM ��������� ��� ��� ����� �� �����
if not exist "src\server\main.py" (
    echo X main.py �� ������ � src\server\!
    pause
    exit /b 1
)

if not exist "src\server\test\http_bridge.py" (
    echo X http_bridge.py �� ������ � src\server\test\!
    pause
    exit /b 1
)

if not exist "config.yml" (
    echo X config.yml �� ������ � �����!
    pause
    exit /b 1
)

echo + ��� ����� �������
echo + ����������� ��������� ������
echo.

REM ������ AI-������� � ��������� ���� � ����������� ������ � config.yml
echo �������� AI-������ � config.yml...
start "AI Server" cmd /k "chcp 1251 > nul && cd /d %~dp0 && call venv\Scripts\activate.bat && cd src\server && python main.py --config ..\..\config.yml"

REM ���� 15 ������ ����� AI-������ ����� �����������
echo ��� ������� AI-������� (15 ���)...
timeout /t 15 /nobreak > nul

REM ���������� venv � ��������� HTTP-���� � ���������� �����
call venv\Scripts\activate.bat
echo �������� HTTP-����...
cd /d "%~dp0\src\server\test"
python http_bridge.py

pause
