local core = require('openmw.core')
local world = require('openmw.world')
local nearby = require('openmw.nearby')

local network = require('scripts.morrowind_ai.network')
local dialogue = require('scripts.morrowind_ai.dialogue')

local M = {}

-- ������������� ����
function M.onInit()
    print("[Morrowind AI] �������������...")
    network.init()
    dialogue.init()
end

-- ��������� �������
function M.onUpdate(dt)
    network.update(dt)
end

-- ��������� ��������
function M.onDialogueStarted(actor)
    dialogue.onDialogueStarted(actor)
end

return M
