@echo off
chcp 1251 > nul
echo ================================
echo       AI-������
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

REM ��������� � ����� src\server ��� ����� main.py
cd /d "%~dp0\src\server"
echo ������� � �����: %CD%

REM ��������� ��� main.py �� �����
if not exist "main.py" (
    echo X main.py �� ������ � %CD%!
    pause
    exit /b 1
)

REM ��������� AI-������
echo �������� AI-������ main.py �� ����� 18080...
echo ��� ��������� ������� Ctrl+C
echo.
python main.py

pause
