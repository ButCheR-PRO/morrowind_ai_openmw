-- Сетевая интеграция с HTTP мостом
local core = require('openmw.core')

local M = {}
local HTTP_BASE = "http://127.0.0.1:8080"

function M.sendDialogueRequest(npcName, playerMessage)
    print("[AI Network] 📤 Отправка диалога: " .. npcName .. " <- " .. playerMessage)
    
    -- В OpenMW 0.49 прямые HTTP запросы ограничены, используем события
    core.sendGlobalEvent("http_request", {
        url = HTTP_BASE .. "/dialogue",
        method = "POST",
        data = {
            npc_name = npcName,
            player_message = playerMessage
        }
    })
    
    return "Запрос отправлен к ИИ серверу..."
end

function M.sendVoiceRequest(voiceText)
    print("[AI Network] 🎤 Отправка голоса: " .. voiceText)
    
    core.sendGlobalEvent("http_request", {
        url = HTTP_BASE .. "/voice",
        method = "POST", 
        data = {
            voice_text = voiceText
        }
    })
    
    return "Голос обработан"
end

function M.testConnection()
    print("[AI Network] 🔍 Тест соединения с HTTP мостом")
    
    core.sendGlobalEvent("http_request", {
        url = HTTP_BASE .. "/test",
        method = "GET",
        data = {}
    })
    
    return "Тест запрос отправлен"
end

return M
