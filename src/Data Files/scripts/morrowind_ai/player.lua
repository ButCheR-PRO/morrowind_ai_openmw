local ui = require('openmw.ui')
local core = require('openmw.core')

local M = {}

function M.onInit()
    ui.showMessage("[AI] 👤 Player AI модуль активирован!")
end

function M.onUpdate(dt)
    -- Здесь будет логика обработки диалогов
end

-- Событие при активации НПС
function M.onActorActive(actor)
    if actor.type and actor.type.name then
        ui.showMessage("[AI] 🗣️ НПС активирован: " .. actor.type.name)
    end
end

return M
