@echo off
echo ================================
echo    ���� VOSK
================================

if not exist "venv\Scripts\activate.bat" (
    echo ������: ����������� ��������� �� �������!
    pause
    exit /b 1
)

echo ���������� ���������...
call venv\Scripts\activate.bat

echo ��������� �������� ��������...
python src/server/test/check_config.py

echo ��������� �������� ����������...
python src/server/test/test_connection.py

echo ��������� �������� VOSK...
python src/server/test/test_vosk.py

pause
