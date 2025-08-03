-- Упрощенный init.lua для OpenMW 0.49.0
-- Без использования недоступных модулей

local function log(message)
    print("[AI Init] " .. message)
end

-- Инициализация модуля (без UI зависимостей)
local function initialize()
    log("✅ AI Init модуль загружен (OpenMW 0.49.0)")
    log("🔧 Работает в режиме совместимости")
    log("⚠️ UI модуль недоступен в релизной версии")
end

-- Запускаем инициализацию
initialize()

-- Возвращаем пустую таблицу (не экспортируем функции)
return {}
