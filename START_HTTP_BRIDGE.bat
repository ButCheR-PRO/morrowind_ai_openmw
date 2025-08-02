@echo off
chcp 1251 >nul

echo ================================
echo     HTTP BRIDGE ������
================================

if not exist "venv\Scripts\activate.bat" (
    echo ������: ����������� ��������� �� �������!
    pause
    exit /b 1
)

echo ���������� ���������...
call venv\Scripts\activate.bat

echo ��������� HTTP ���� �� ����� 8080...
echo ��� ��������� ������ ��� ����
echo.

:restart
python src/server/test/http_bridge.py
echo HTTP ���� ����������. ���������� ����� 3 ���...
timeout /t 3 /nobreak >nul
goto restart
