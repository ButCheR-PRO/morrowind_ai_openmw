local core = require('openmw.core')

print("[Morrowind AI] Скрипт player.lua загружается...")

local function onInit()
    print("[Morrowind AI] Player onInit вызван!")
    print("[Morrowind AI] Нажмите P для теста")
end

local function onKeyPress(key)
    print("[Morrowind AI] Клавиша: " .. tostring(key.code))
    
    if key.code == 80 then -- P key
        print("=======================================")
        print("[Morrowind AI] PING! Нажата P!")
        print("[Morrowind AI] Модуль работает!")
        print("=======================================")
    end
end

return {
    eventHandlers = {
        onInit = onInit,
        onKeyPress = onKeyPress
    }
}
