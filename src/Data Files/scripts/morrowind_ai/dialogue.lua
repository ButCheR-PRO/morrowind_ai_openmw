local ui = require('openmw.ui')
local core = require('openmw.core')
local network = require('scripts.morrowind_ai.network')

local M = {}

function M.init()
    print("[Morrowind AI] Диалоговая система готова")
end

function M.onDialogueStarted(actor)
    if not actor then return end
    
    local npcData = {
        name = actor.recordId,
        race = actor.type and actor.type.race or "unknown",
        class = actor.type and actor.type.class or "unknown",
        faction = actor.type and actor.type.faction or "none"
    }
    
    -- Отправляем данные НПС на сервер
    network.sendToServer({
        type = "dialogue_started",
        npc = npcData,
        player_name = "Неревар" -- Или получить из игры
    })
end

function M.processPlayerMessage(message)
    -- Отправляем сообщение игрока на сервер для обработки ИИ
    network.sendToServer({
        type = "player_message", 
        message = message
    })
    
    -- Ждём ответ от ИИ
    local response = network.receiveFromServer()
    if response and response.ai_response then
        -- Показываем ответ НПС в диалоге
        ui.showMessage(response.ai_response)
        
        -- Если есть аудио файл - проигрываем его
        if response.audio_file then
            -- Здесь нужно добавить воспроизведение аудио
            M.playNPCAudio(response.audio_file)
        end
    end
end

function M.playNPCAudio(audioFile)
    -- OpenMW пока не поддерживает динамическое аудио
    -- Это нужно будет реализовать через внешние средства
    print("[Morrowind AI] Воспроизведение: " .. audioFile)
end

return M
