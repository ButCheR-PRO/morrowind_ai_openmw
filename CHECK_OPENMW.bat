@echo off
chcp 1251 >nul

echo ================================
echo    ДИАГНОСТИКА OpenMW
================================

echo Проверяем версию OpenMW...
cd /d "F:\Games\MorrowindFullrest\game\OpenMW 0.49.0"
openmw.exe --version

echo.
echo Проверяем настройки Lua...
if exist "C:\Users\Admin\Documents\My Games\OpenMW\settings.cfg" (
    echo Файл settings.cfg найден
    findstr /i "lua" "C:\Users\Admin\Documents\My Games\OpenMW\settings.cfg"
) else (
    echo settings.cfg НЕ НАЙДЕН!
)

echo.
echo Проверяем openmw.cfg...
if exist "C:\Users\Admin\Documents\My Games\OpenMW\openmw.cfg" (
    echo openmw.cfg найден
    findstr /i "morrowind_ai" "C:\Users\Admin\Documents\My Games\OpenMW\openmw.cfg"
) else (
    echo openmw.cfg НЕ НАЙДЕН!
)
echo ================================
echo   РАСШИРЕННАЯ ДИАГНОСТИКА OpenMW
================================

cd /d "F:\Games\MorrowindFullrest\game\OpenMW 0.49.0"

echo Версия и ревизия:
openmw.exe --version

echo.
echo Поддерживаемые опции:
openmw.exe --help | findstr /i lua

echo.
echo Проверяем settings-default.cfg...
if exist "settings-default.cfg" (
    findstr /i "lua" "settings-default.cfg"
) else (
    echo settings-default.cfg НЕ НАЙДЕН!
)


dir settings-default.cfg
type settings-default.cfg | findstr /i lua


echo.
echo Проверяем все настройки пользователя:
type "C:\Users\Admin\Documents\My Games\OpenMW\settings.cfg" | findstr /i lua

echo.
echo Список всех cfg файлов в системе:
dir /s "C:\Users\Admin\Documents\My Games\OpenMW\*.cfg"

echo ================================
echo   ФИНАЛЬНЫЙ ТЕСТ LUA API
================================

cd /d "F:\Games\MorrowindFullrest\game\OpenMW 0.49.0"

echo Проверяем settings-default.cfg...
if exist "settings-default.cfg" (
    echo ? settings-default.cfg найден!
    findstr /i "lua" "settings-default.cfg"
) else (
    echo ? settings-default.cfg ОТСУТСТВУЕТ!
)

echo.
echo Запускаем OpenMW для теста...
start openmw.exe --debug-lua > openmw_debug.log 2>&1

echo.
echo В игре проверь Lua консоль:
echo luag
echo local ui = require('openmw.ui')
echo ui.showMessage("Lua работает!")


pause
