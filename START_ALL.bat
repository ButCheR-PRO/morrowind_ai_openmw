@echo off
chcp 1251 > nul

:menu
cls
echo ============================================================================
echo MORROWIND AI MOD - ���������� �������� v1.0
echo ============================================================================
echo.
echo �������� ��������:
echo.
echo [1] ��������� ��� �������
echo [2] ���������� ��� �������  
echo [3] ������������� �������
echo [4] ��������� ������
echo [5] �������� ���� � ��������� �����
echo [6] �������� �������� ��������
echo [0] �����
echo.
set /p choice=������� ����� (0-6): 

if "%choice%"=="1" goto start_services
if "%choice%"=="2" goto stop_services
if "%choice%"=="3" goto restart_services  
if "%choice%"=="4" goto check_status
if "%choice%"=="5" goto cleanup
if "%choice%"=="6" goto show_processes
if "%choice%"=="0" goto exit
goto menu

:start_services
cls
echo ============================================================================
echo ������ ���� ��������
echo ============================================================================
echo.

cd /d "%~dp0"

echo [1/4] ��������� ���������� �������...
if not exist "venv" (
    echo ������: ����������� ��������� �� �������
    echo ��������� ������� INSTALL.bat
    pause
    goto menu
)

if not exist "config.yml" (
    echo ������: config.yml �� ������  
    echo �������� ���������������� ����
    pause
    goto menu
)

echo [2/4] ������������� ������ ��������...
taskkill /f /im python.exe 2>nul >nul
timeout /t 2 /nobreak >nul

echo [3/4] ��������� AI ������ (���� 9090)...
start "AI Server" cmd /k "cd /d "%~dp0" && call venv\Scripts\activate.bat && cd src\server && python main.py"
timeout /t 3 /nobreak >nul

echo [4/4] ��������� HTTP ���� (���� 8080)...  
start "HTTP Bridge" cmd /k "cd /d "%~dp0" && call venv\Scripts\activate.bat && cd src\server\test && python http_bridge.py"

echo.
echo ��� ������� ��������!
echo.
echo ��������� 2 ����:
echo - AI Server (���� 9090) 
echo - HTTP Bridge (���� 8080)
echo.
echo ������ ������ ��������� OpenMW � �����
echo.
pause
goto menu

:stop_services
cls  
echo ============================================================================
echo ��������� ���� ��������
echo ============================================================================
echo.

echo ������������� Python ��������...
taskkill /f /im python.exe 2>nul
if errorlevel 1 (
    echo ��� �������� Python ���������
) else (
    echo Python �������� �����������
)

echo.
echo ��������� ���� ��������...
taskkill /f /fi "WINDOWTITLE:AI Server*" 2>nul >nul
taskkill /f /fi "WINDOWTITLE:HTTP Bridge*" 2>nul >nul

echo.
echo ������� ��������� �����...
if exist "Data Files\ai_temp\*.tmp" del /q "Data Files\ai_temp\*.tmp" 2>nul
if exist "Data Files\ai_temp\*.json" del /q "Data Files\ai_temp\*.json" 2>nul  
if exist "Data Files\ai_temp\*.txt" del /q "Data Files\ai_temp\*.txt" 2>nul

echo.
echo ��� ������� �����������!
echo.
pause
goto menu

:restart_services
cls
echo ============================================================================  
echo ���������� �������
echo ============================================================================
echo.

echo ������������� �������...
call :stop_services_silent

echo ���� ���������� ���������...
timeout /t 3 /nobreak >nul

echo ��������� �������...  
call :start_services_silent

echo.
echo ������� ������������!
echo.
pause
goto menu

:check_status
cls
echo ============================================================================
echo ������ �������  
echo ============================================================================
echo.

echo ��������� Python ��������...
tasklist /fi "imagename eq python.exe" 2>nul | findstr python.exe >nul
if errorlevel 1 (
    echo [������] Python ��������: �� ��������
) else (
    echo [������] Python ��������: �������
    tasklist /fi "imagename eq python.exe"
)

echo.
echo ��������� �����...
netstat -an | findstr ":9090" >nul
if errorlevel 1 (
    echo [���� 9090] AI Server: �� �������
) else (
    echo [���� 9090] AI Server: �������
)

netstat -an | findstr ":8080" >nul
if errorlevel 1 (
    echo [���� 8080] HTTP Bridge: �� �������  
) else (
    echo [���� 8080] HTTP Bridge: �������
)

echo.
echo ��������� ��������� �����...
if exist "Data Files\ai_temp\ai_signal.txt" (
    echo [�����] ���� �������� ������� �� OpenMW
) else (
    echo [�����] ��� �������� ��������
)

echo.
pause
goto menu

:cleanup
cls
echo ============================================================================
echo ������� �������
echo ============================================================================  
echo.

echo ������� ����...
if exist "logs\*.log" (
    del /q logs\*.log
    echo ���� �������
) else (
    echo ���� ��� �����
)

echo.  
echo ������� ��������� �����...
if exist "Data Files\ai_temp\*.*" (
    del /q "Data Files\ai_temp\*.*"  
    echo ��������� ����� �������
) else (
    echo ��������� ����� ��� �������
)

echo.
echo ������� ��� Python...
if exist "src\server\__pycache__" (
    rmdir /s /q "src\server\__pycache__"
    echo ��� Python ������
)

echo.
echo ������� ���������!
echo.
pause  
goto menu

:show_processes
cls
echo ============================================================================
echo �������� ��������
echo ============================================================================
echo.

echo Python ��������:
tasklist /fi "imagename eq python.exe" 2>nul | findstr /v "�� �������"

echo.
echo ������� �����������:  
netstat -an | findstr ":8080\|:9090"

echo.
echo ���� CMD � ���������:
tasklist /fi "imagename eq cmd.exe" /fo table

echo.
pause
goto menu

:start_services_silent
taskkill /f /im python.exe 2>nul >nul
timeout /t 2 /nobreak >nul
start "AI Server" cmd /k "cd /d "%~dp0" && call venv\Scripts\activate.bat && cd src\server && python main.py"
timeout /t 3 /nobreak >nul
start "HTTP Bridge" cmd /k "cd /d "%~dp0" && call venv\Scripts\activate.bat && cd src\server\test && python http_bridge.py"
goto :eof

:stop_services_silent
taskkill /f /im python.exe 2>nul >nul
taskkill /f /fi "WINDOWTITLE:AI Server*" 2>nul >nul  
taskkill /f /fi "WINDOWTITLE:HTTP Bridge*" 2>nul >nul
if exist "Data Files\ai_temp\*.tmp" del /q "Data Files\ai_temp\*.tmp" 2>nul
if exist "Data Files\ai_temp\*.json" del /q "Data Files\ai_temp\*.json" 2>nul
if exist "Data Files\ai_temp\*.txt" del /q "Data Files\ai_temp\*.txt" 2>nul
goto :eof

:exit
echo.
echo ���������� ������...
exit
