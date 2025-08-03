@echo off
chcp 1251 > nul
echo ================================
echo    ��������� ������������
echo ================================
echo.

REM ��������� Python 3.12
python3.12 --version >nul 2>&1
if errorlevel 1 (
    python --version 2>nul | findstr "3.12" >nul
    if errorlevel 1 (
        echo X Python 3.12 �� ������! ���������� Python 3.12+ � �������� � PATH
        pause
        exit /b 1
    )
    set PYTHON_CMD=python
) else (
    set PYTHON_CMD=python3.12
)

echo + Python 3.12 ������: %PYTHON_CMD%
echo.

REM ������� ����������� ��������� � �����
echo ������ ����������� ���������...
if exist "venv" (
    echo ! ����������� ��������� ��� ����������
) else (
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        echo X ������ �������� ������������ ���������!
        pause
        exit /b 1
    )
    echo + ����������� ��������� �������
)

REM ���������� ����������� ���������
echo ��������� ����������� ���������...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo X ������ ��������� ������������ ���������!
    pause
    exit /b 1
)

echo + ����������� ��������� ������������ (Python 3.12)
echo.

REM ��������� ����������� � venv
echo �������� pip, setuptools, wheel...
python -m pip install --upgrade pip setuptools wheel

REM ��������� � ����� src/server ��� ����� requirements.txt
cd /d "%~dp0\src\server"
echo ������� � �����: %CD%

REM ��������� ��� requirements.txt �� �����
if not exist "requirements.txt" (
    echo X requirements.txt �� ������ � %CD%!
    pause
    exit /b 1
)

echo + requirements.txt ������ � %CD%

REM ������������� ��������� Windows ������
echo ������������ Windows API ������...
python -m pip install pywin32 --prefer-binary
python -m pip install pynput --prefer-binary

REM ������������� STT ������
echo ������������ STT ������...
python -m pip install vosk --prefer-binary
python -m pip install sounddevice --prefer-binary

REM ������������� LLM ������
echo ������������ LLM ����������...
python -m pip install google-generativeai
python -m pip install anthropic
python -m pip install openai

REM ������������ ��������� �������
echo ������������ ��������� �������...
python -m pip install colorlog pathvalidate

REM ������ ���������� ���� � requirements.txt
echo ������������ ����������� �� requirements.txt...
python -m pip install -r requirements.txt --prefer-binary

if errorlevel 1 (
    echo.
    echo ! ��������� ������ �� ������������, �� �������� ����
)

echo.
echo + ��������� ���������!
echo ��������� ��������� ������...

REM ��������� ��� �������� ������ ������������
python -c "import win32api; print('+ pywin32 ��������')" 2>nul || echo "X pywin32 �� ��������"
python -c "import vosk; print('+ vosk ��������')" 2>nul || echo "X vosk �� ��������"
python -c "import google.generativeai; print('+ gemini ��������')" 2>nul || echo "X gemini �� ��������"

echo.
echo ������ ����� ���������:
echo - START.bat (AI-������)
echo - START_HTTP_BRIDGE.bat (HTTP-����)
echo - START_ALL.bat (��� �������)
echo.
echo �����: requirements.txt ��������� �� src\server\
echo.
pause
