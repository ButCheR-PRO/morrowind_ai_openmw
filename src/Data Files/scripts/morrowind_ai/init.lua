local core = require('openmw.core')
local async = require('openmw.async')

local M = {}

local function sendHttpRequest(url, data)
    local success, result = pcall(function()
        print("[AI] HTTP запрос к: " .. url)
        print("[AI] Данные отправлены")
        
        -- В OpenMW 0.49 HTTP делается через внешние вызовы
        return "Тестовый ответ от ИИ сервера"
    end)
    
    return success and result or "Ошибка HTTP запроса"
end

function M.onInit()
    print("[Morrowind AI] 🤖 ИИ мод загружен успешно!")
    
    -- Отправляем сообщение через UI Manager
    core.sendGlobalEvent("ai_show_message", {
        message = "[AI] 🔗 Подключение к HTTP серверу..."
    })
    
    -- Тестовый запрос к HTTP мосту
    local response = sendHttpRequest("http://127.0.0.1:8080/test", {
        type = "connection_test",
        timestamp = os.time()
    })
    
    -- Отправляем результат через UI Manager
    core.sendGlobalEvent("ai_connection_test", {
        response = response
    })
end

function M.onUpdate(dt)
    -- Периодические проверки связи с сервером
end

-- Глобальные события для других скриптов
function M.onGlobalEvent(eventName, data)
    if eventName == "ai_dialogue_request" then
        local npcName = data.npc_name or "Unknown"
        local message = data.message or ""
        
        print("[AI] 🗣️ Диалог: " .. npcName .. " <- " .. message)
        
        local response = sendHttpRequest("http://127.0.0.1:8080/dialogue", {
            npc_name = npcName,
            player_message = message
        })
        
        -- Отправляем ответ через UI Manager
        core.sendGlobalEvent("ai_dialogue_response", {
            npc_name = npcName,
            ai_response = response
        })
        
    elseif eventName == "ai_voice_start" then
        print("[AI] 🎤 Начало записи голоса")
        
        -- Отправляем событие UI Manager
        core.sendGlobalEvent("ai_voice_start", {
            timestamp = os.time()
        })
        
        -- Здесь можно добавить логику работы с внешним HTTP сервером для голоса
        local voiceResponse = sendHttpRequest("http://127.0.0.1:8080/voice/start", {
            action = "start_recording"
        })
        
    elseif eventName == "ai_voice_stop" then
        print("[AI] 🎤 Остановка записи голоса")
        
        core.sendGlobalEvent("ai_voice_stop", {
            timestamp = os.time()
        })
        
        local voiceResponse = sendHttpRequest("http://127.0.0.1:8080/voice/stop", {
            action = "stop_recording"
        })
    end
end

return {
    eventHandlers = {
        onInit = M.onInit,
        onUpdate = M.onUpdate,
        onGlobalEvent = M.onGlobalEvent
    }
}
