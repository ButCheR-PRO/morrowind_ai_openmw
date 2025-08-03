@echo off
chcp 1251 > nul
echo ================================
echo    HTTP BRIDGE ������
echo ================================
echo.

REM ��������� ������� ������������ ��������� � �����
if not exist "venv\Scripts\activate.bat" (
    echo X ����������� ��������� �� �������!
    echo ������� ��������� INSTALL.bat
    pause
    exit /b 1
)

REM ���������� ����������� ���������
echo ��������� ����������� ���������...
call venv\Scripts\activate.bat

REM ��������� � ����� src\server\test ��� ����� http_bridge.py
cd /d "%~dp0\src\server\test"
echo ������� � �����: %CD%

REM ��������� ��� http_bridge.py �� �����
if not exist "http_bridge.py" (
    echo X http_bridge.py �� ������ � %CD%!
    pause
    exit /b 1
)

REM ��������� HTTP ����
echo �������� HTTP ���� http_bridge.py �� ����� 8080...
echo ��� ��������� ������ ��� ����
echo.
python http_bridge.py

pause
