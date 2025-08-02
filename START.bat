@echo off
chcp 1251 > nul
echo ================================
echo    ������ MORROWIND AI SERVER
echo ================================
echo.

REM ��������� ������� ������������ ���������
if not exist "venv\Scripts\activate.bat" (
    echo ������: ����������� ��������� �� �������!
    echo ������� ������� INSTALL.bat
    pause
    exit /b 1
)

REM ��������� ������� �������
if not exist "config.yml" (
    echo ������: ���� config.yml �� ������!
    echo ������ ������ �� ������ config.yml.example
    pause
    exit /b 1
)

echo ���������� ����������� ���������...
call venv\Scripts\activate.bat

echo ��������� �����������...
python -c "import socket, yaml, requests" >nul 2>&1
if %errorlevel% neq 0 (
    echo ������: �� ��� ����������� �����������!
    echo ������� INSTALL.bat ��� ���
    pause
    exit /b 1
)

echo ��������� ������...
echo ������ ����� �������� �� ����� 18080
echo ��� ��������� ����� Ctrl+C
echo.
python src/server/main.py --config config.yml

echo.
echo ������ ����������.
pause
