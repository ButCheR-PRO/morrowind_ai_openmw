@echo off
chcp 1251 > nul
echo ============================================================================
echo MORROWIND AI MOD - ��������� ������������ v1.0
echo ============================================================================
echo.

cd /d "%~dp0"

echo ������� ����������: %CD%
echo.

echo ��������� Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ������: Python �� ������! ���������� Python 3.12 �� https://python.org
    echo.
    pause
    exit /b 1
)

python --version
echo Python ������ �������
echo.

echo ������� ����������� ���������...
if exist "venv" (
    echo ����������� ��������� ��� ����������
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ������ �������� ������������ ���������
        pause
        exit /b 1
    )
    echo ����������� ��������� �������
)
echo.

echo ���������� ����������� ���������...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ������ ��������� ������������ ���������
    pause
    exit /b 1
)
echo ����������� ��������� ������������
echo.

echo ��������� pip...
python -m pip install --upgrade pip
echo.

echo ������������� �����������...
cd src\server
pip install -r requirements.txt
if errorlevel 1 (
    echo ������ ��������� ������������
    echo ���������� ���������� ����������� �������:
    echo    cd src\server
    echo    pip install aiohttp google-generativeai vosk elevenlabs
    pause
    exit /b 1
)
echo ��� ����������� �����������
echo.

cd ..\..

echo ������� ����������� ����������...
if not exist "logs" mkdir logs
if not exist "data" mkdir data
if not exist "Data Files\ai_temp" mkdir "Data Files\ai_temp"
echo ���������� �������
echo.

echo ��������� ������������...
if not exist "config.yml" (
    echo ��������: ���� config.yml �� ������
    echo �������� config.yml � ����������� API ������
)
echo.

echo ============================================================================
echo ��������� ��������� �������!
echo ============================================================================
echo.
echo ��� �������:
echo    1. ��������� START_AI_SERVER.bat
echo    2. ��������� START_HTTP_BRIDGE.bat  
echo    3. ��������� OpenMW � �����
echo.
echo ������������: https://github.com/ButCheR-PRO/morrowind_ai_openmw/
echo.
pause
