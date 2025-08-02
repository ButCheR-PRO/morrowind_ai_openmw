@echo off
chcp 1251 > nul
echo ================================
echo   ��������� MORROWIND AI SERVER
echo ================================
echo.

REM ��������� ������� Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ������: Python �� ������! �������� Python 3.11+
    pause
    exit /b 1
)

REM ������� ������ ����������� ��������� ���� ����
if exist "venv" (
    echo ������� ������ ����������� ���������...
    rmdir /s /q venv
)

echo ������ ����� ����������� ���������...
python -m venv venv
if %errorlevel% neq 0 (
    echo ������: �� ������� ������� ����������� ���������!
    pause
    exit /b 1
)

echo ���������� ����������� ���������...
call venv\Scripts\activate.bat

echo ��������� pip �� ��������� ������...
python -m pip install --upgrade pip

echo ������������� �����������...
pip install -r src/server/requirements.txt
if %errorlevel% neq 0 (
    echo ������: �� ������� ���������� �����������!
    echo ������� ���� src/server/requirements.txt
    pause
    exit /b 1
)

echo.
echo ================================
echo   ��������� ��������� �������!
echo ================================
echo ������ ������ ��������� START.bat
echo.
pause
