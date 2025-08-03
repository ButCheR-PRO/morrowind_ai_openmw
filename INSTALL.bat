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

REM ������ ����������� ��������� � ����� �������
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
    echo + ����������� ��������� ������� � �����
)

REM ���������� ����������� ���������
echo ��������� ����������� ���������...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo X ������ ��������� ������������ ���������!
    pause
    exit /b 1
)

REM ��������� ��� � venv ������������ Python 3.12
python --version | findstr "3.12" >nul
if errorlevel 1 (
    echo X � ����������� ��������� �� Python 3.12!
    echo ������� ������:
    python --version
    pause
    exit /b 1
)

echo + ����������� ��������� ������������ (Python 3.12)
echo.

REM ��������� ������� ����������� � venv
echo �������� pip, setuptools, wheel...
python -m pip install --upgrade pip setuptools wheel

REM ��������� � src/server ��� ����� requirements.txt
cd /d "%~dp0src\server"
echo ������� � �����: %CD%

REM ��������� ��� requirements.txt �� �����
if not exist "requirements.txt" (
    echo X requirements.txt �� ������ � %CD%!
    echo ������� ��������� �������!
    pause
    exit /b 1
)

echo + requirements.txt ������ � %CD%
echo.

REM ================================
REM ������������� ��������� ������ �� �����������
REM (����� �������� ������� ��-�� ������������� �������)
REM ================================

echo ������������ ��������� Windows API ������...
python -m pip install pywin32==306 --prefer-binary
python -m pip install pynput>=1.7.0 --prefer-binary

echo ������������ STT ������ ��� ������������� ����...
python -m pip install vosk>=0.3.45 --prefer-binary
python -m pip install sounddevice>=0.4.6 --prefer-binary

echo ������������ OpenAI Whisper (����� ������ �����)...
python -m pip install openai-whisper>=20231117 --prefer-binary
if errorlevel 1 (
    echo ! OpenAI Whisper �� �����������, ������� ��� �������� � ������...
    python -m pip install openai-whisper --prefer-binary
)

echo ������������ ��� LLM ����������...
python -m pip install mistralai>=0.1.0
python -m pip install anthropic>=0.8.0  
python -m pip install google-generativeai>=0.3.0
python -m pip install openai>=1.0.0

echo ������������ ��������� �������...
python -m pip install colorlog>=6.7.0
python -m pip install pathvalidate>=3.0.0

echo ������������ numpy ��������...
python -m pip install numpy>=1.25.0 --prefer-binary

echo.
echo ================================
echo ������������ ��������� ����������� �� requirements.txt...
echo ================================

REM ������ ������������� ��������� �� requirements.txt
python -m pip install -r requirements.txt --prefer-binary

if errorlevel 1 (
    echo.
    echo ! ��������� ������ �� requirements.txt �� ������������
    echo �� �������� ��������� ������ �����������
)

echo.
echo ================================
echo �������� ��������� ��������� �������...
echo ================================

REM ��������� ��� ��� ��������� ������ ������������
python -c "import win32api; print('+ pywin32 (win32api) ��������')" 2>nul || echo "X pywin32 �� ��������!"
python -c "import pynput; print('+ pynput ��������')" 2>nul || echo "X pynput �� ��������!"
python -c "import vosk; print('+ vosk ��������')" 2>nul || echo "X vosk �� ��������!"
python -c "import whisper; print('+ openai-whisper ��������')" 2>nul || echo "X whisper �� ��������!"
python -c "import mistralai; print('+ mistralai ��������')" 2>nul || echo "X mistralai �� ��������!"
python -c "import anthropic; print('+ anthropic ��������')" 2>nul || echo "X anthropic �� ��������!"
python -c "import google.generativeai; print('+ google-generativeai ��������')" 2>nul || echo "X gemini �� ��������!"
python -c "import openai; print('+ openai ��������')" 2>nul || echo "X openai �� ��������!"
python -c "import colorlog; print('+ colorlog ��������')" 2>nul || echo "X colorlog �� ��������!"
python -c "import pathvalidate; print('+ pathvalidate ��������')" 2>nul || echo "X pathvalidate �� ��������!"

echo.
echo ================================
echo ��������� ���������!
echo ================================
echo.
echo ������ ����� ���������:
echo - START.bat (������ AI-������)
echo - START_HTTP_BRIDGE.bat (������ HTTP-����)  
echo - START_ALL.bat (��� ������� �����)
echo.
echo �����: �� ����������� � ����������� ��������� venv
echo requirements.txt ��������� �� src\server\requirements.txt
echo.
pause
