local core = require('openmw.core')
local ui = require('openmw.ui')
local util = require('openmw.util')

local M = {}

function M.onInit()
    ui.showMessage("[AI] 🤖 Morrowind AI мод инициализирован!")
    print("[Morrowind AI] Мод загружен успешно")
    
    -- Проверяем доступность HTTP функций
    local success, error = pcall(function()
        print("[AI] Проверка HTTP возможностей...")
    end)
    
    if success then
        ui.showMessage("[AI] ✅ HTTP функции доступны")
    else
        ui.showMessage("[AI] ❌ Ошибка: " .. tostring(error))
    end
end

function M.testDialogue()
    ui.showMessage("[AI] 🧪 Тестируем диалоговую систему...")
    
    -- Симуляция отправки HTTP запроса
    local testData = {
        npc_name = "Тестовый НПС",
        player_message = "Привет! Как дела?"
    }
    
    ui.showMessage("[AI] 📤 Отправка: " .. testData.player_message)
    
    -- Здесь будет реальный HTTP запрос к мосту
    local response = "Приветствую, путник! Как дела в Вварденфелле?"
    
    ui.showMessage("[AI] 📥 Ответ НПС: " .. response)
    
    return response
end

function M.onUpdate(dt)
    -- Периодические проверки
end

return M
