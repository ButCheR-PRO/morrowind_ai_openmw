-- Простейший AI мод для OpenMW 0.49.0 (ТОЛЬКО автомат)
local util = require('openmw.util')
local core = require('openmw.core')

-- Переменные
local requestCounter = 0
local startTime = os.time()

-- Функция инициализации (работает в 0.49.0)
local function onInit()
    print("[AI Mod] =================================")
    print("[AI Mod] MORROWIND AI v1.0 ЗАПУСКАЕТСЯ")
    print("[AI Mod] OpenMW версия: " .. tostring(core.API_REVISION))
    print("[AI Mod] Время старта: " .. tostring(startTime))
    print("[AI Mod] =================================")
    
    -- Автоматический тестовый запрос
    requestCounter = requestCounter + 1
    local testRequest = "[AI_REQUEST] ID:auto_" .. tostring(startTime) .. "_" .. requestCounter .. 
                       "|NPC:Caius Cosades|MSG:Тестовое сообщение системы|CTX:Автоматический запуск в Балморе|TIME:" .. tostring(os.time())
    
    print(testRequest)
    print("[AI Mod] Автоматический запрос отправлен!")
    print("[AI Mod] Система готова к работе!")
end

-- ТОЛЬКО автоматическая инициализация (работает в 0.49.0)
onInit()
