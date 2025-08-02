local core = require('openmw.core')
local ui = require('openmw.ui')
local world = require('openmw.world')

local network = require('scripts.morrowind_ai.network')

local M = {}

function M.onInit()
    ui.showMessage("[AI] 🤖 Morrowind AI мод загружен!")
    ui.showMessage("[AI] 🔗 Подключение к HTTP мосту...")
    
    network.init()
    
    ui.showMessage("[AI] ✅ Готов к диалогам!")
end

function M.onUpdate(dt)
    network.update(dt)
end

-- Тестовая функция для диалогов
function M.testDialogue()
    local response = network.sendDialogue("Тестовый НПС", "Привет!")
    if response and response.ai_response then
        ui.showMessage("[AI] " .. response.ai_response)
    end
end

return M
