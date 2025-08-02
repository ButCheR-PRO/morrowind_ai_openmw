local ui = require('openmw.ui')
local core = require('openmw.core')

local M = {}

function M.onInit()
    ui.showMessage("[AI] 👤 Player AI модуль активирован!")
end

-- Реакция на диалоги с НПС
function M.onDialogueStarted(actor)
    if actor and actor.recordId then
        ui.showMessage("[AI] 🗣️ Диалог с НПС: " .. actor.recordId)
        
        -- Здесь будет отправка к HTTP мосту
        M.sendToHttpBridge(actor.recordId, "Привет!")
    end
end

function M.sendToHttpBridge(npcName, message)
    ui.showMessage("[AI] 📤 Отправка к ИИ: " .. message)
    
    -- HTTP запрос к твоему мосту на порту 8080
    -- Пока заглушка, но интеграция готова!
end

return M
