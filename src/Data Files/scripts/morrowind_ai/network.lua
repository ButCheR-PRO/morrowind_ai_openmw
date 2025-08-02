local json = require('openmw.util').loadJson

local M = {}
local isConnected = false

function M.init()
    print("[Morrowind AI] HTTP мост готов")
    isConnected = true
end

function M.sendDialogue(npcName, playerMessage)
    if not isConnected then return nil end
    
    print("[AI] Отправка диалога: " .. npcName .. " <- " .. playerMessage)
    
    -- Здесь будет HTTP запрос к мосту
    -- Пока возвращаем заглушку
    return {
        status = "success",
        ai_response = "Приветствую! Ты сказал: '" .. playerMessage .. "'"
    }
end

function M.sendVoice(voiceText)
    if not isConnected then return nil end
    
    print("[AI] Голос: " .. voiceText)
    return { status = "success", recognized_text = voiceText }
end

function M.update(dt)
    -- Проверка соединения
end

return M
