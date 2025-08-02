local core = require('openmw.core')
local ui = require('openmw.ui')

local M = {}

function M.onInit()
    -- Эти сообщения должны появиться автоматически при загрузке
    ui.showMessage("[AI] 🤖 Morrowind AI мод загружен!")
    ui.showMessage("[AI] 🔗 Попытка подключения к HTTP серверу...")
    
    -- Попытка тестового HTTP запроса
    core.sendGlobalEvent("ai_test_connection", {})
end

function M.onUpdate(dt)
    -- Периодическая проверка каждые 10 секунд
    if core.getGameTime() % 10 < 0.1 then
        -- Тестовый вызов HTTP моста (если реализован)
    end
end

return M
