local util = require('openmw.util')
local core = require('openmw.core')
local async = require('openmw.async')

-- Пытаемся подключить "запрещенные" в 0.49 модули
local input_status, input = pcall(require, 'openmw.input')
local ui_status, ui = pcall(require, 'openmw.ui')
local camera_status, camera = pcall(require, 'openmw.camera')

local function onInit()
    print("========================================")
    print("🔥 OpenMW 0.50.0 API CHECKER by ButCheR")
    print("========================================")
    
    print("CORE version: " .. core.getAppVersion())
    
    if input_status then
        print("✅ OPENMW.INPUT: ДОСТУПЕН! (Можно делать хоткеи!)")
        -- Попробуем проверить функции
        if input.registerAction then
            print("   -> input.registerAction: ЕСТЬ")
        else
            print("   -> input.registerAction: НЕТ (странно)")
        end
    else
        print("❌ OPENMW.INPUT: НЕ ДОСТУПЕН (Печаль...)")
    end

    if ui_status then
        print("✅ OPENMW.UI: ДОСТУПЕН! (Можно пилить менюхи!)")
    else
        print("❌ OPENMW.UI: НЕ ДОСТУПЕН")
    end
    
    print("========================================")
end

return {
    engineHandlers = {
        onInit = onInit
    }
}
