local core = require('openmw.core')
local world = require('openmw.world')
local nearby = require('openmw.nearby')

local network = require('scripts.morrowind_ai.network')
local dialogue = require('scripts.morrowind_ai.dialogue')

local M = {}

-- Инициализация мода
function M.onInit()
    print("[Morrowind AI] Инициализация...")
    network.init()
    dialogue.init()
end

-- Обработка событий
function M.onUpdate(dt)
    network.update(dt)
end

-- Обработка диалогов
function M.onDialogueStarted(actor)
    dialogue.onDialogueStarted(actor)
end

return M
