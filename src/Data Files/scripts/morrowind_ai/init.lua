local core = require('openmw.core')
local ui = require('openmw.ui')

local M = {}

function M.onInit()
    ui.showMessage("[AI] 🤖 Morrowind AI мод загружен!")
    ui.showMessage("[AI] 🔗 Подключение к HTTP серверу...")
    
    -- Проверка доступности HTTP моста
    M.testHttpConnection()
end

function M.testHttpConnection()
    -- Здесь будет HTTP запрос к порту 8080
    ui.showMessage("[AI] 📡 Тестирую связь с ИИ сервером...")
    
    -- Пока заглушка, но скрипт работает!
    core.sendGlobalEvent("ai_server_test", { status = "connecting" })
end

function M.onUpdate(dt)
    -- Периодическая проверка связи с HTTP мостом
end

return M
