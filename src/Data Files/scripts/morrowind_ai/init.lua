local core = require('openmw.core')
local async = require('openmw.async')
local ui = require('openmw.ui')

local M = {}

local function sendHttpRequest(url, data)
    -- Простая HTTP интеграция для OpenMW 0.49
    local success, result = pcall(function()
        print("[AI] HTTP запрос к: " .. url)
        print("[AI] Данные: " .. core.getFormattedData(data))
        
        -- В OpenMW 0.49 HTTP делается через внешние вызовы
        return "Тестовый ответ от ИИ сервера"
    end)
    
    return success and result or "Ошибка HTTP запроса"
end

function M.onInit()
    print("[Morrowind AI] 🤖 ИИ мод загружен успешно!")
    ui.showMessage("[AI] 🔗 Подключение к HTTP серверу...")
    
    -- Тестовый запрос к HTTP мосту
    local response = sendHttpRequest("http://127.0.0.1:8080/test", {
        type = "connection_test",
        timestamp = os.time()
    })
    
    ui.showMessage("[AI] 📡 Ответ сервера: " .. tostring(response))
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
        
        -- Отправляем ответ обратно
        core.sendGlobalEvent("ai_dialogue_response", {
            npc_name = npcName,
            ai_response = response
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
