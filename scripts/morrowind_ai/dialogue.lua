local ui = require('openmw.ui')
local core = require('openmw.core')
local network = require('scripts.morrowind_ai.network')

local M = {}

function M.init()
    print("[Morrowind AI] ���������� ������� ������")
end

function M.onDialogueStarted(actor)
    if not actor then return end
    
    local npcData = {
        name = actor.recordId,
        race = actor.type and actor.type.race or "unknown",
        class = actor.type and actor.type.class or "unknown",
        faction = actor.type and actor.type.faction or "none"
    }
    
    -- ���������� ������ ��� �� ������
    network.sendToServer({
        type = "dialogue_started",
        npc = npcData,
        player_name = "�������" -- ��� �������� �� ����
    })
end

function M.processPlayerMessage(message)
    -- ���������� ��������� ������ �� ������ ��� ��������� ��
    network.sendToServer({
        type = "player_message", 
        message = message
    })
    
    -- ��� ����� �� ��
    local response = network.receiveFromServer()
    if response and response.ai_response then
        -- ���������� ����� ��� � �������
        ui.showMessage(response.ai_response)
        
        -- ���� ���� ����� ���� - ����������� ���
        if response.audio_file then
            -- ����� ����� �������� ��������������� �����
            M.playNPCAudio(response.audio_file)
        end
    end
end

function M.playNPCAudio(audioFile)
    -- OpenMW ���� �� ������������ ������������ �����
    -- ��� ����� ����� ����������� ����� ������� ��������
    print("[Morrowind AI] ���������������: " .. audioFile)
end

return M
