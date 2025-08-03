@echo off
chcp 1251 > nul
echo ============================================================================
echo ������ AI ������� MORROWIND (���� 9090)
echo ============================================================================
echo.

cd /d "%~dp0"

echo ���������� ����������� ���������...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ������: �� ������� ������������ ����������� ���������
    echo ��������� ������� INSTALL.bat
    pause
    exit /b 1
)

echo ��������� ������������...
if not exist "config.yml" (
    echo ������: config.yml �� ������
    echo �������� ���� config.yml � API �������
    pause
    exit /b 1
)

echo ��������� AI ������ �� ����� 9090...
cd src\server
python main.py

if errorlevel 1 (
    echo ������ ������� AI �������
    echo ��������� ���� � ����� logs/
)

echo.
echo AI ������ ����������
pause
