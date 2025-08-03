@echo off
chcp 1251 >nul

echo ================================
echo    ����������� OpenMW
================================

echo ��������� ������ OpenMW...
cd /d "F:\Games\MorrowindFullrest\game\OpenMW 0.49.0"
openmw.exe --version

echo.
echo ��������� ��������� Lua...
if exist "C:\Users\Admin\Documents\My Games\OpenMW\settings.cfg" (
    echo ���� settings.cfg ������
    findstr /i "lua" "C:\Users\Admin\Documents\My Games\OpenMW\settings.cfg"
) else (
    echo settings.cfg �� ������!
)

echo.
echo ��������� openmw.cfg...
if exist "C:\Users\Admin\Documents\My Games\OpenMW\openmw.cfg" (
    echo openmw.cfg ������
    findstr /i "morrowind_ai" "C:\Users\Admin\Documents\My Games\OpenMW\openmw.cfg"
) else (
    echo openmw.cfg �� ������!
)
echo ================================
echo   ����������� ����������� OpenMW
================================

cd /d "F:\Games\MorrowindFullrest\game\OpenMW 0.49.0"

echo ������ � �������:
openmw.exe --version

echo.
echo �������������� �����:
openmw.exe --help | findstr /i lua

echo.
echo ��������� settings-default.cfg...
if exist "settings-default.cfg" (
    findstr /i "lua" "settings-default.cfg"
) else (
    echo settings-default.cfg �� ������!
)


dir settings-default.cfg
type settings-default.cfg | findstr /i lua


echo.
echo ��������� ��� ��������� ������������:
type "C:\Users\Admin\Documents\My Games\OpenMW\settings.cfg" | findstr /i lua

echo.
echo ������ ���� cfg ������ � �������:
dir /s "C:\Users\Admin\Documents\My Games\OpenMW\*.cfg"

echo ================================
echo   ��������� ���� LUA API
================================

cd /d "F:\Games\MorrowindFullrest\game\OpenMW 0.49.0"

echo ��������� settings-default.cfg...
if exist "settings-default.cfg" (
    echo ? settings-default.cfg ������!
    findstr /i "lua" "settings-default.cfg"
) else (
    echo ? settings-default.cfg �����������!
)

echo.
echo ��������� OpenMW ��� �����...
start openmw.exe --debug-lua > openmw_debug.log 2>&1

echo.
echo � ���� ������� Lua �������:
echo luag
echo local ui = require('openmw.ui')
echo ui.showMessage("Lua ��������!")


pause
