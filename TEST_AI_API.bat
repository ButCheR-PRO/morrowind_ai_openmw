@echo off
chcp 1251 > nul
echo ================================
echo   ���� AI ������� ����� HTTP
echo ================================
echo.

echo 1. ���� ������� �������� HTTP �����:
curl http://127.0.0.1:8080/

echo.
echo.
echo 2. ���� ������� �������:
curl http://127.0.0.1:8080/api/status

echo.
echo.
echo 3. ���� ������� � Gemini AI:
curl -X POST http://127.0.0.1:8080/api/dialogue -H "Content-Type: application/json" -d "{\"session_id\":\"test_openmw\",\"text\":\"������ �� ������������� OpenMW!\",\"npc_name\":\"�������� ���\"}"

echo.
echo.
echo 4. �������� ����������� AI-�������:
curl http://127.0.0.1:9090/ --connect-timeout 3

echo.
echo ================================
echo ���� ��������
echo ================================
pause
