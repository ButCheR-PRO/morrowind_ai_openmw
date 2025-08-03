@echo off
chcp 1251 > nul
echo ============================================================================
echo MORROWIND AI MOD - ������ ����������� ������� v1.0
echo ============================================================================
echo.

cd /d "%~dp0"

set ERROR_COUNT=0

echo [1/10] ��������� Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [������] Python �� ������! ���������� Python 3.12
    set /a ERROR_COUNT+=1
) else (
    python --version
    echo [OK] Python ������ � ��������
)
echo.

echo [2/10] ��������� ��������� �������...
if not exist "config.yml" (
    echo [������] config.yml �� ������
    set /a ERROR_COUNT+=1
) else (
    echo [OK] ���������������� ���� ������
)

if not exist "venv" (
    echo [������] ����������� ��������� �� ������� - ��������� INSTALL.bat
    set /a ERROR_COUNT+=1
) else (
    echo [OK] ����������� ��������� ����������
)

if not exist "src\server\main.py" (
    echo [������] AI ������ �� ������
    set /a ERROR_COUNT+=1
) else (
    echo [OK] AI ������ ������
)

if not exist "src\server\test\http_bridge.py" (
    echo [������] HTTP ���� �� ������  
    set /a ERROR_COUNT+=1
) else (
    echo [OK] HTTP ���� ������
)

if not exist "src\Data Files\scripts\morrowind_ai.lua" (
    echo [������] Lua ������ �� ������
    set /a ERROR_COUNT+=1
) else (
    echo [OK] Lua ������ ������
)

if not exist "morrowind_ai.omwscripts" (
    echo [������] ���� ����������� ���� �� ������
    set /a ERROR_COUNT+=1
) else (
    echo [OK] ���� ����������� ���� ������
)
echo.

echo [3/10] ��������� ����������...
if not exist "logs" mkdir logs
echo [OK] ���������� logs ������

if not exist "data" mkdir data  
echo [OK] ���������� data ������

if not exist "Data Files\ai_temp" mkdir "Data Files\ai_temp"
echo [OK] ���������� ai_temp ������
echo.

echo [4/10] ��������� ����������� ���������...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [������] �� ������� ������������ venv
    set /a ERROR_COUNT+=1
) else (
    echo [OK] ����������� ��������� ������������
    
    echo [5/10] ��������� Python ������...
    pip show aiohttp >nul 2>&1
    if errorlevel 1 (
        echo [������] aiohttp �� ����������
        set /a ERROR_COUNT+=1
    ) else (
        echo [OK] aiohttp ����������
    )
    
    pip show google-generativeai >nul 2>&1
    if errorlevel 1 (
        echo [������] google-generativeai �� ����������
        set /a ERROR_COUNT+=1
    ) else (
        echo [OK] google-generativeai ����������
    )
    
    pip show vosk >nul 2>&1
    if errorlevel 1 (
        echo [������] vosk �� ����������
        set /a ERROR_COUNT+=1
    ) else (
        echo [OK] vosk ����������
    )
)
echo.

echo [6/10] ��������� ������������...
if exist "config.yml" (
    findstr /i "gemini" config.yml >nul
    if errorlevel 1 (
        echo [��������������] API ���� Gemini �� ������ � config.yml
    ) else (
        echo [OK] ������������ Gemini �������
    )
) else (
    echo [������] ���� config.yml �����������
    set /a ERROR_COUNT+=1
)
echo.

echo [7/10] ��������� ��������� Python ��������...
python -m py_compile src\server\main.py >nul 2>&1
if errorlevel 1 (
    echo [������] �������������� ������ � main.py
    set /a ERROR_COUNT+=1
) else (
    echo [OK] main.py ������������� ���������
)

if exist "src\server\test\http_bridge.py" (
    python -m py_compile src\server\test\http_bridge.py >nul 2>&1
    if errorlevel 1 (
        echo [������] �������������� ������ � http_bridge.py
        set /a ERROR_COUNT+=1
    ) else (
        echo [OK] http_bridge.py ������������� ���������
    )
)
echo.

echo [8/10] ��������� �����...
netstat -an | findstr ":9090" >nul
if not errorlevel 1 (
    echo [��������������] ���� 9090 ��� �����
) else (
    echo [OK] ���� 9090 ��������
)

netstat -an | findstr ":8080" >nul  
if not errorlevel 1 (
    echo [��������������] ���� 8080 ��� �����
) else (
    echo [OK] ���� 8080 ��������
)
echo.

echo [9/10] ��������� ��������� �����...
echo test > "Data Files\ai_temp\test.tmp"
if exist "Data Files\ai_temp\test.tmp" (
    del "Data Files\ai_temp\test.tmp"
    echo [OK] ������ � ai_temp ��������
) else (
    echo [������] �� ������� �������� � ai_temp
    set /a ERROR_COUNT+=1
)
echo.

echo [10/10] ��������� OpenMW �������������...
if exist "C:\Program Files\OpenMW\openmw.exe" (
    echo [OK] OpenMW ������ � ����������� �����
) else if exist "openmw.exe" (
    echo [OK] OpenMW ������ � ������� �����  
) else (
    echo [��������������] OpenMW �� ������ � ����������� ������
)
echo.

echo ============================================================================
echo �������� �����
echo ============================================================================

if %ERROR_COUNT%==0 (
    echo ������: ��� �������� �������� �������!
    echo ������� ��������� ������ � ������
    echo.
    echo ��� ������� ����������� START_ALL.bat
) else (
    echo ������: ���������� ������: %ERROR_COUNT%
    echo.
    echo ������������:
    if not exist "venv" echo - ��������� INSTALL.bat ��� ��������� ������������
    if not exist "config.yml" echo - �������� config.yml � API �������
    if %ERROR_COUNT% gtr 5 echo - �������������� ������ � ����
)

echo ============================================================================
echo.
pause
