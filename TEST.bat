@echo off
chcp 1251 > nul
echo ============================================================================
echo MORROWIND AI MOD - ������ ����������� ������� v1.4
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
    echo [������] config.yml �� ������ � �����
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

REM ���������� �������� - ����� �� ������ ����
echo [�������������] ��������� Lua ������� � ����:

if not exist "src\Data Files\morrowind_ai.omwscripts" (
    echo [������] morrowind_ai.omwscripts �� ������ � ����
    set /a ERROR_COUNT+=1
) else (
    echo [OK] morrowind_ai.omwscripts ������ � ����
)

if not exist "src\Data Files\scripts\morrowind_ai.lua" (
    echo [������] scripts/morrowind_ai.lua �� ������ � ����
    set /a ERROR_COUNT+=1
) else (
    echo [OK] scripts/morrowind_ai.lua ������ � ����
)

if not exist "src\Data Files\scripts\morrowind_ai\init.lua" (
    echo [������] scripts/morrowind_ai/init.lua �� ������ � ����
    set /a ERROR_COUNT+=1
) else (
    echo [OK] scripts/morrowind_ai/init.lua ������ � ����
)

if not exist "src\Data Files\scripts\morrowind_ai\player.lua" (
    echo [������] scripts/morrowind_ai/player.lua �� ������ � ����
    set /a ERROR_COUNT+=1
) else (
    echo [OK] scripts/morrowind_ai/player.lua ������ � ����
)

if not exist "src\Data Files\scripts\morrowind_ai\console_commands.lua" (
    echo [������] scripts/morrowind_ai/console_commands.lua �� ������ � ����
    set /a ERROR_COUNT+=1
) else (
    echo [OK] scripts/morrowind_ai/console_commands.lua ������ � ����
)

if not exist "src\Data Files\scripts\morrowind_ai\config.lua" (
    echo [������] scripts/morrowind_ai/config.lua �� ������ � ����
    set /a ERROR_COUNT+=1
) else (
    echo [OK] scripts/morrowind_ai/config.lua ������ � ����
)

echo.
echo [�������������] ��������� ��������� � ����:

if exist "f:\Games\MorrowindFullrest\game\Data Files\morrowind_ai.omwscripts" (
    echo [OK] morrowind_ai.omwscripts ���������� � ����
) else (
    echo [��������������] morrowind_ai.omwscripts �� ���������� � ����
    echo                   ��������� COPY_TO_GAME.bat
)

if exist "f:\Games\MorrowindFullrest\game\Data Files\scripts\morrowind_ai" (
    echo [OK] ����� �������� AI ������� � ����
    
    if exist "f:\Games\MorrowindFullrest\game\Data Files\scripts\morrowind_ai\init.lua" (
        echo [OK] init.lua ���������� � ����
    ) else (
        echo [��������������] init.lua �� ���������� � ����
    )
    
    if exist "f:\Games\MorrowindFullrest\game\Data Files\scripts\morrowind_ai\player.lua" (
        echo [OK] player.lua ���������� � ����
    ) else (
        echo [��������������] player.lua �� ���������� � ����
    )
    
    if exist "f:\Games\MorrowindFullrest\game\Data Files\scripts\morrowind_ai\console_commands.lua" (
        echo [OK] console_commands.lua ���������� � ����
    ) else (
        echo [��������������] console_commands.lua �� ���������� � ����
    )
    
) else (
    echo [��������������] ����� �������� AI �� ������� � ����
    echo                   ��������� COPY_TO_GAME.bat
)
echo.

echo [3/10] ��������� ����������...
if not exist "logs" (
    mkdir logs
    echo [����������] ������� ���������� logs
) else (
    echo [OK] ���������� logs ������
)

if not exist "data" (
    mkdir data
    echo [����������] ������� ���������� data
) else (
    echo [OK] ���������� data ������
)

if not exist "f:\Games\MorrowindFullrest\game\Data Files\ai_temp" (
    mkdir "f:\Games\MorrowindFullrest\game\Data Files\ai_temp"
    echo [����������] ������� ���������� ai_temp � ����
) else (
    echo [OK] ���������� ai_temp ������
)
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
    
    pip show pathvalidate >nul 2>&1
    if errorlevel 1 (
        echo [������] pathvalidate �� ���������� - ����������� �����!
        set /a ERROR_COUNT+=1
    ) else (
        echo [OK] pathvalidate ����������
    )
    
    pip show vosk >nul 2>&1
    if errorlevel 1 (
        echo [��������������] vosk �� ����������
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
python -c "import py_compile; py_compile.compile('src/server/main.py', doraise=True)" >nul 2>&1
if errorlevel 1 (
    echo [������] �������������� ������ � main.py
    set /a ERROR_COUNT+=1
) else (
    echo [OK] main.py ������������� ���������
)

if exist "src\server\test\http_bridge.py" (
    python -c "import py_compile; py_compile.compile('src/server/test/http_bridge.py', doraise=True)" >nul 2>&1
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
echo test > "f:\Games\MorrowindFullrest\game\Data Files\ai_temp\test.tmp"
if exist "f:\Games\MorrowindFullrest\game\Data Files\ai_temp\test.tmp" (
    del "f:\Games\MorrowindFullrest\game\Data Files\ai_temp\test.tmp"
    echo [OK] ������ � ai_temp ��������
) else (
    echo [������] �� ������� �������� � ai_temp
    set /a ERROR_COUNT+=1
)
echo.

echo [10/10] ��������� OpenMW �������������...
if exist "f:\Games\MorrowindFullrest\game\OpenMW 0.49.0\openmw.exe" (
    echo [OK] OpenMW ������ �� ���������� ����
) else (
    echo [��������������] OpenMW �� ������ �� ���� f:\Games\MorrowindFullrest\game\OpenMW 0.49.0\openmw.exe
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
    if not exist "f:\Games\MorrowindFullrest\game\Data Files\morrowind_ai.omwscripts" echo - ��������� COPY_TO_GAME.bat ��� ��������� ������ � ����
    if %ERROR_COUNT% gtr 5 echo - �������������� ������ � ����
)

echo ============================================================================
echo.
pause
