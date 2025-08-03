@echo off
chcp 1251 > nul
echo ============================================================================
echo                    MORROWIND AI ULTIMATE v2.0
echo ============================================================================
echo.
echo ������������� ���������� ��� AI �������� � Morrowind
echo.

REM ��������� ����������� ���������
echo ��������� ����������� ���������...
if not exist "venv\Scripts\activate.bat" (
    echo ������: ����������� ��������� �� �������!
    echo ��������� ������� INSTALL.bat
    pause
    exit /b 1
)

REM ���������� ����������� ���������
echo ���������� ����������� ���������...
call venv\Scripts\activate.bat

REM ��������� AI ������ ����� Python ������ curl
echo ��������� AI ������...
python -c "import requests; r=requests.get('http://127.0.0.1:8080/api/status', timeout=3); print('OK' if r.status_code==200 else 'ERROR')" 2>nul | findstr "OK" >nul
if %errorlevel% neq 0 (
    echo.
    echo ��������: AI ������ ���������� �� ����� 8080
    echo ��������� START_OPENMW_AI_SERVER.bat � ��������� ����
    echo.
    echo 1 - ���������� ��� AI �������
    echo 2 - �������� ������
    echo.
    set /p choice="�������� ������� (1 ��� 2): "
    
    if "%choice%"=="1" (
        echo ��������� ��� AI �������...
    ) else (
        echo ������ �������
        pause
        exit /b 1
    )
) else (
    echo AI ������ ������ � ����� � ������!
)

REM ������������� �������������� ������ ���� �����
echo ��������� �����������...
python -c "import keyboard" 2>nul
if %errorlevel% neq 0 (
    echo ������������ ������ keyboard ��� ������� ������...
    pip install keyboard
)

REM ��������� ����������
echo.
echo ============================================================================
echo �������� MORROWIND AI ULTIMATE
echo ============================================================================
echo.
echo ��������� �������:
echo - ������� ������� � ���
echo - ����������� ��� � ��
echo - ������� �������� � ���
echo - ������� ������� (Ctrl+Alt+A, Ctrl+Alt+C, Ctrl+Alt+Q)
echo - ���������� � ���������
echo.

python MORROWIND_AI_ULTIMATE.py

REM ��������� ���������
if %errorlevel% neq 0 (
    echo.
    echo ������ ��� ������� ����������
    echo ��������� ���� � �����������
) else (
    echo.
    echo Morrowind AI Ultimate �������� ���������
)

echo.
pause
