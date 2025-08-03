-- Консольные команды для AI мода (PLAYER контекст)

print("[AI Console] 🎮 Загружаю консольные команды...")

-- Функции для PLAYER контекста
local function pingTest()
    print("[AI] 🏓 PING из PLAYER контекста!")
    print("[AI] ✅ AI сервер отвечает!")
    return "Ping OK"
end

local function infoShow()
    print("[AI] ℹ️ INFO из PLAYER контекста!")
    print("[AI] 🎮 Система работает!")
    return "Info OK"
end

-- Экспорт для доступа из консоли
return {
    ping = pingTest,
    info = infoShow,
    
    engineHandlers = {
        onInit = function()
            print("[AI Console] ✅ PLAYER команды готовы!")
        end
    }
}
