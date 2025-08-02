local core = require('openmw.core')
local ui = require('openmw.ui')
local nearby = require('openmw.nearby')

local M = {}

local lastNpcInteraction = nil

function M.onInit()
    print("[Morrowind AI] 👤 Player модуль инициализирован")
    ui.showMessage("[AI] ✅ Голосовое управление готово!")
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
    ui.showMessage("[AI] 🗣️ НПС рядом: " .. npcName)
    
    -- Отправляем событие для обработки диалога
    core.sendGlobalEvent("ai_dialogue_request", {
        npc_name = npcName,
        message = "Привет! Как дела в " .. (actor.cell and actor.cell.name or "этих краях") .. "?"
    })
end

-- Обработка ответов от ИИ
function M.onGlobalEvent(eventName, data)
    if eventName == "ai_dialogue_response" then
        local npcName = data.npc_name or "НПС"
        local aiResponse = data.ai_response or "..."
        
        ui.showMessage("[" .. npcName .. "] " .. aiResponse)
        print("[AI] ИИ ответ: " .. aiResponse)
    end
end

-- Реакция на нажатие клавиш (для активации голосового ввода)
function M.onKeyPress(key)
    if key.code == 59 then -- F1 key для активации голоса
        ui.showMessage("[AI] 🎤 Начало записи голоса...")
        
        -- Отправляем сигнал на HTTP мост для начала записи
        core.sendGlobalEvent("ai_voice_start", {
            timestamp = os.time()
        })
    end
end

return {
    eventHandlers = {
        onInit = M.onInit,
        onUpdate = M.onUpdate,
        onGlobalEvent = M.onGlobalEvent,
        onKeyPress = M.onKeyPress
    }
}
