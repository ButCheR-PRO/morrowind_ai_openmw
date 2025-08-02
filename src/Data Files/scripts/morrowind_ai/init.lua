local core = require('openmw.core')

-- Заглушка HTTP запросов для OpenMW
local function sendHttpRequest(url, data)
    print("[AI] 📡 HTTP запрос к: " .. url)
    print("[AI] 📤 Данные отправлены")
    
    -- В OpenMW прямых HTTP запросов нет, но можно использовать внешние процессы
    -- Пока используем заглушку
    return "✅ Тестовый ответ от ИИ сервера"
end

-- Инициализация глобального модуля
local function onInit()
    print("[Morrowind AI] 🤖 ИИ мод загружен успешно!")
    print("[Morrowind AI] 🌐 Глобальный модуль инициализирован")
    
    -- Тестовый запрос к HTTP мосту
    local response = sendHttpRequest("http://127.0.0.1:8080/test", {
        type = "connection_test",
        timestamp = os.time()
    })
    
    print("[AI] 📨 Ответ сервера: " .. response)
end

-- Обработка глобальных событий
local function onGlobalEvent(eventName, data)
    print("[AI] 📢 Получено событие: " .. eventName)
    
    if eventName == "ai_dialogue_request" then
        local npcName = data.npc_name or "Unknown"
        local message = data.message or ""
        
        print("[AI] 🗣️ Диалог: " .. npcName .. " <- " .. message)
        
        -- Отправляем запрос к HTTP мосту
        local response = sendHttpRequest("http://127.0.0.1:8080/dialogue", {
            npc_name = npcName,
            player_message = message,
            context = data.context or {}
        })
        
        -- Отправляем ответ обратно
        core.sendGlobalEvent("ai_dialogue_response", {
            npc_name = npcName,
            ai_response = response,
            original_message = message
        })
        
    elseif eventName == "ai_voice_start" then
        print("[AI] 🎤 🔴 Начало записи голоса")
        
        -- HTTP запрос для начала записи голоса
        local voiceResponse = sendHttpRequest("http://127.0.0.1:8080/voice", {
            action = "start_recording",
            timestamp = data.timestamp or os.time()
        })
        
        print("[AI] 🎤 Сервер ответ: " .. voiceResponse)
        
    elseif eventName == "ai_voice_stop" then
        print("[AI] 🎤 ⚪ Остановка записи голоса")
        
        -- HTTP запрос для остановки записи
        local voiceResponse = sendHttpRequest("http://127.0.0.1:8080/voice", {
            action = "stop_recording",
            voice_text = "Тестовый распознанный текст",
            timestamp = data.timestamp or os.time()
        })
        
        print("[AI] 🎤 Распознанный текст: " .. voiceResponse)
        
        -- Отправляем распознанный текст обратно
        core.sendGlobalEvent("ai_voice_recognized", {
            text = "Тестовый распознанный текст",
            timestamp = os.time()
        })
        
    elseif eventName == "ai_connection_test" then
        print("[AI] 🔗 Тест подключения от: " .. (data.source or "unknown"))
        
        -- Отправляем ping к HTTP мосту
        local pingResponse = sendHttpRequest("http://127.0.0.1:8080/health", {
            ping = true,
            source = data.source,
            timestamp = os.time()
        })
        
        print("[AI] 🏓 Ping ответ: " .. pingResponse)
        
    elseif eventName == "ai_http_test" then
        print("[AI] 🌐 HTTP тест к: " .. (data.url or "unknown"))
        
        local testResponse = sendHttpRequest(data.url or "http://127.0.0.1:8080/test", {
            test = true,
            timestamp = data.timestamp or os.time()
        })
        
        print("[AI] 📡 HTTP тест результат: " .. testResponse)
    end
end

-- Экспорт только разрешенных секций
return {
    eventHandlers = {
        onInit = onInit,
        onGlobalEvent = onGlobalEvent
    }
}
