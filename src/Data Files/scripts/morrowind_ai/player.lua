local core = require('openmw.core')
local input = require('openmw.input')
local nearby = require('openmw.nearby')

local M = {}

local lastNpcInteraction = nil
local voiceRecording = false

function M.onInit()
    print("[Morrowind AI] 👤 Player модуль инициализирован")
    
    -- Отправляем сообщение через UI Manager
    core.sendGlobalEvent("ai_show_message", {
        message = "[AI] ✅ Голосовое управление готово! Нажмите Left Alt для активации."
    })
end

function M.onUpdate(dt)
    -- Проверяем взаимодействие с НПС
    local player = self.object
    if not player then return end
    
    -- Ищем ближайших НПС
    for _, actor in pairs(nearby.actors) do
        if actor.type and actor.type.record and actor.type.record.id then
            local distance = (actor.position - player.position):length()
            
            -- Если НПС рядом (менее 200 единиц) и это новый НПС
            if distance < 200 and lastNpcInteraction ~= actor.type.record.id then
                lastNpcInteraction = actor.type.record.id
                M.triggerNpcInteraction(actor)
                break
            end
        end
    end
end

function M.triggerNpcInteraction(actor)
    local npcName = actor.type.record.id
    
    -- Отправляем уведомление через UI Manager
    core.sendGlobalEvent("ai_npc_interaction", {
        npc_name = npcName
    })
    
    -- Отправляем событие для обработки диалога
    core.sendGlobalEvent("ai_dialogue_request", {
        npc_name = npcName,
        message = "Привет! Как дела в " .. (actor.cell and actor.cell.name or "этих краях") .. "?"
    })
end

-- Реакция на нажатие клавиш
function M.onKeyPress(key)
    -- Left Alt (код 342) для активации голосового ввода
    if key.code == 342 then -- Left Alt key
        if not voiceRecording then
            voiceRecording = true
            -- Отправляем сигнал на начало записи
            core.sendGlobalEvent("ai_voice_start", {
                timestamp = os.time()
            })
        end
    end
end

-- Реакция на отпускание клавиш
function M.onKeyRelease(key)
    -- Left Alt отпущен - останавливаем запись
    if key.code == 342 and voiceRecording then -- Left Alt key
        voiceRecording = false
        -- Отправляем сигнал на остановку записи
        core.sendGlobalEvent("ai_voice_stop", {
            timestamp = os.time()
        })
    end
end

return {
    eventHandlers = {
        onInit = M.onInit,
        onUpdate = M.onUpdate,
        onKeyPress = M.onKeyPress,
        onKeyRelease = M.onKeyRelease
    }
}
