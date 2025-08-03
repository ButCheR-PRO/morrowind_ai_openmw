@echo off
chcp 1251 > nul
echo ================================
echo   ТЕСТ AI СИСТЕМЫ ЧЕРЕЗ HTTP
echo ================================
echo.

echo 1. Тест главной страницы HTTP моста:
curl http://127.0.0.1:8080/

echo.
echo.
echo 2. Тест статуса системы:
curl http://127.0.0.1:8080/api/status

echo.
echo.
echo 3. Тест диалога с Gemini AI:
curl -X POST http://127.0.0.1:8080/api/dialogue -H "Content-Type: application/json" -d "{\"session_id\":\"test_openmw\",\"text\":\"Привет от исправленного OpenMW!\",\"npc_name\":\"Тестовый НПС\"}"

echo.
echo.
echo 4. Проверка доступности AI-сервера:
curl http://127.0.0.1:9090/ --connect-timeout 3

echo.
echo ================================
echo ТЕСТ ЗАВЕРШЕН
echo ================================
pause
