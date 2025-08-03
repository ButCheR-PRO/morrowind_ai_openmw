@echo off
chcp 1251 > nul
echo ================================
echo   ������ ������� MORROWIND AI
echo ================================
echo.

REM ������� ������ ��������
echo ������ ������ ��������...
taskkill /f /im python.exe 2>nul
taskkill /f /im openmw.exe 2>nul
timeout /t 3 /nobreak > nul

REM ������� ���-�����
echo ������ ������ ���-�����...
if exist "src\server\rpgaiserver.log" del /f "src\server\rpgaiserver.log" 2>nul
if exist "logs\ai_server.log" del /f "logs\ai_server.log" 2>nul

echo + ����������� ��������� ������
echo + ��� ����� �������
echo.

REM 1. ������ AI-�������
echo 1/3 �������� AI-������...
start "AI Server" cmd /k "chcp 1251 > nul && cd /d %~dp0 && call venv\Scripts\activate.bat && cd src\server && python main.py --config ..\..\config.yml"

REM 2. ��� ������� AI-�������  
echo 2/3 ��� ������� AI-������� (15 ���)...
timeout /t 15 /nobreak > nul

REM 3. ������ OpenMW
echo 3/3 �������� OpenMW � �� �����...
echo.
echo �����: � ���� ��������� ������� �������:
echo   P - ping ���� ����� � AI
echo   I - ���������� � �������  
echo   O - ���� ������� � ��
echo   Left Alt - ��������� ���� (������-���������)
echo.

REM ��������� OpenMW (���� ����� ������� ����)
start "OpenMW AI" "F:\Games\MorrowindFullrest\openmw.exe"

echo OpenMW �������! �������� ������ ���� � ����.
echo ��� ������� HTTP ����� �������� ��������� START_HTTP_BRIDGE.bat
echo.
pause
