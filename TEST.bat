@echo off
chcp 1251 > nul
echo ================================
echo    �����
================================

if not exist "venv\Scripts\activate.bat" (
    echo ������: ����������� ��������� �� �������!
    pause
    exit /b 1
)

echo ���������� ���������...
call venv\Scripts\activate.bat


echo ================================
echo      �������� ������������
echo ================================
echo.

if not exist "venv" echo ����������� ��������� �� �������
if exist "venv" echo ����������� ��������� �������

if not exist "config.yml" echo ���� config.yml �� ������
if exist "config.yml" echo ���� config.yml ������

if not exist "src\server\main.py" echo ��������� ����� �� �������
if exist "src\server\main.py" echo ��������� ����� �������

if exist "venv" (
    call venv\Scripts\activate.bat
    python -c "import yaml; print('YAML ���������� ��������')" 2>nul || echo YAML ���������� �� ��������
    python -c "import requests; print('Requests ���������� ��������')" 2>nul || echo Requests ���������� �� ��������
)

echo.


echo ��������� �������� ��������...
python src/server/test/check_config.py

echo ��������� �������� ����������...
python src/server/test/test_connection.py

echo ��������� �������� VOSK...
python src/server/test/test_vosk.py

pause
