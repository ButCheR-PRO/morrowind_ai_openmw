local ui = require('openmw.ui')
local core = require('openmw.core')

local M = {}

-- Инициализация UI менеджера
function M.onInit()
    print("[Morrowind AI] 🎨 UI Manager инициализирован")
    ui.showMessage("[AI] ✅ Интерфейс готов к работе!")
end

-- Обработка глобальных событий для UI
function M.onGlobalEvent(eventName, data)
    if eventName == "ai_show_message" then
        local message = data.message or "Пустое сообщение"
        ui.showMessage(message)
        print("[AI UI] Показано сообщение: " .. message)
        
    elseif eventName == "ai_dialogue_response" then
        local npcName = data.npc_name or "НПС"
        local aiResponse = data.ai_response or "..."
        
        -- Показываем ответ НПС
        ui.showMessage("[" .. npcName .. "] " .. aiResponse)
        print("[AI UI] ИИ ответ от " .. npcName .. ": " .. aiResponse)
        
    elseif eventName == "ai_voice_start" then
        ui.showMessage("[AI] 🎤 Начало записи голоса... Говорите!")
        print("[AI UI] Активирована запись голоса")
        
    elseif eventName == "ai_voice_stop" then
        ui.showMessage("[AI] 🎤 Запись завершена. Обработка...")
        print("[AI UI] Запись голоса остановлена")
        
    elseif eventName == "ai_connection_test" then
        local response = data.response or "Нет ответа"
        ui.showMessage("[AI] 📡 Тест соединения: " .. response)
        print("[AI UI] Результат теста соединения: " .. response)
        
    elseif eventName == "ai_error" then
        local error = data.error or "Неизвестная ошибка"
        ui.showMessage("[AI] ❌ Ошибка: " .. error)
        print("[AI UI] Ошибка: " .. error)
        
    elseif eventName == "ai_npc_interaction" then
        local npcName = data.npc_name or "НПС"
        ui.showMessage("[AI] 🗣️ НПС рядом: " .. npcName)
        print("[AI UI] Взаимодействие с НПС: " .. npcName)
    end
end

return {
    eventHandlers = {
        onInit = M.onInit,
        onGlobalEvent = M.onGlobalEvent
    }
}
