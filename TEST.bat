@echo off
chcp 1251 > nul
echo ================================
echo          �����
echo ================================

REM ������� ������ �� pip
echo ������ ����� �� pip...
cd /d "%~dp0src\server"
for /d %%i in (0.* 1.* 3.* 6.* 20*) do (
    if exist "%%i" (
        echo ������ �������� �����: %%i
        rmdir /s /q "%%i"
    )
)
cd /d "%~dp0"

REM ��������� ����������� ���������
if not exist "venv\Scripts\activate.bat" (
    echo X ����������� ��������� �� �������!
    echo ������� ��������� INSTALL.bat
    pause
    exit /b 1
)

echo ���������� ���������...
call venv\Scripts\activate.bat

echo ================================
echo     �������� ������������
echo ================================

REM ��������� ��� ��� ������ ����� � ����� ����
if not exist "venv" echo X ����������� ��������� �� ������� && goto :error
echo + ����������� ��������� �������

if not exist "config.yml" echo X config.yml �� ������ && goto :error
echo + ���� config.yml ������

if not exist "src\server\main.py" echo X main.py �� ������ && goto :error
echo + ��������� ����� �������

if not exist "logs" (
    mkdir logs
    echo + ����� logs �������
) else (
    echo + ����� logs �������
)

if not exist "data" (
    mkdir data
    echo + ����� data �������
) else (
    echo + ����� data �������
)

if not exist "data\scene_instructions.txt" (
    echo. > data\scene_instructions.txt
    echo + ���� scene_instructions.txt ������
)

REM ��������� �������� ������ Python
python -c "import yaml" 2>nul && echo + YAML ���������� �������� || (echo X YAML �� �������� && goto :error)
python -c "import requests" 2>nul && echo + Requests ���������� �������� || (echo X Requests �� �������� && goto :error)

echo.
echo ��������� �������� ��������...
cd src\server\test
python check_config.py
if errorlevel 1 goto :error
cd ..\..\..

echo ��������� �������� AI-�������...
echo ================================
echo     ���� AI-�������
echo ================================

REM ��������� AI-������ � ���� ��� �����
start /b "" cmd /c "cd src\server && python main.py --config ..\..\config.yml > ..\..\logs\test_server.log 2>&1"

REM ��� 15 ������ ����� ������ ����������
echo ��� ������� AI-������� (15 ���)...
timeout /t 15 /nobreak > nul

REM ��������� ��� AI-������ ����������
curl -s http://127.0.0.1:18080/health > nul 2>&1
if errorlevel 1 (
    echo X AI-������ �� ���������� �� ����� 18080
    echo ��������� ���...
    if exist "logs\test_server.log" (
        echo === ��� AI-������� ===
        type logs\test_server.log
    )
) else (
    echo + AI-������ ���������� �� ����� 18080!
)

REM ������������� �������� ������
taskkill /f /im python.exe 2>nul

echo ��������� �������� ����������...
cd src\server\test
python test_connection.py
cd ..\..\..

echo ��������� �������� VOSK...
cd src\server\test
python test_vosk.py
cd ..\..\..

echo ================================
echo + ��� ����� ���������!
echo ================================
pause
goto :end

:error
echo ================================
echo X ����������� ������ � ������!
echo ================================
pause

:end
