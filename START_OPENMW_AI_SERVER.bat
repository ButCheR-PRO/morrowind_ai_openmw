@echo off
chcp 1251 > nul
echo ============================================================================
echo ������ OPENMW AI ������� (���� 8080)
echo ============================================================================
echo.

REM ���������� ����������� ���������
echo ���������� ����������� ���������...
if not exist "venv\Scripts\activate.bat" (
    echo ������: ����������� ��������� �� �������!
    echo ��������� ������� INSTALL.bat
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

REM ��������� ������� config.yml
echo ��������� ������������...
if not exist "config.yml" (
    echo ������: ���� config.yml �� ������!
    pause
    exit /b 1
)

REM ��������� � ����� �������
cd src\server

REM ��������� OpenMW AI ������
echo �������� OpenMW AI ������ �� ����� 8080...
echo �������: python openmw_ai_server.py
echo.

python openmw_ai_server.py

REM ��������� ��������� �������
if %errorlevel% neq 0 (
    echo.
    echo ������ ������� OpenMW AI �������
    echo ��������� ���� � ������������
) else (
    echo OpenMW AI ������ ���������� ���������
)

echo.
pause
