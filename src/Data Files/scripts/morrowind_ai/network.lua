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
    
    -- Уведомляем UI Manager
    core.sendGlobalEvent("ai_show_message", {
        message = "[AI] 📡 Запрос отправлен к ИИ серверу..."
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
    
    core.sendGlobalEvent("ai_show_message", {
        message = "[AI] 🎤 Голос обработан и отправлен"
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
    
    core.sendGlobalEvent("ai_show_message", {
        message = "[AI] 🔍 Тест запрос отправлен"
    })
    
    return "Тест запрос отправлен"
end

function M.sendToServer(data)
    print("[AI Network] 📤 Отправка данных на сервер")
    
    core.sendGlobalEvent("http_request", {
        url = HTTP_BASE .. "/api",
        method = "POST",
        data = data
    })
    
    return "Данные отправлены"
end

function M.receiveFromServer()
    -- В реальной реализации здесь должна быть логика получения ответа
    -- Пока возвращаем тестовые данные
    return {
        ai_response = "Тестовый ответ от ИИ сервера",
        npc_name = "Тестовый НПС"
    }
end

return M
