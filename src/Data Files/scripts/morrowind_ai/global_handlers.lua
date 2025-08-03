local ui = require('openmw.ui')
local input = require('openmw.input')
local util = require('openmw.util')

-- Импортируем наши модули
local aiInit = require('scripts.morrowind_ai.init')
local config = require('scripts.morrowind_ai.config')

local M = {}

-- Состояние голосового ввода
local voiceRecording = false
local voiceStartTime = 0

-- Функция логирования
local function log(message)
    print("[AI Global] " .. message)
end

-- Обработчик нажатий клавиш
local function onKeyPress(key)
    log("Клавиша нажата: " .. tostring(key.symbol))
    
    if key.symbol == input.KEY.P then
        log("🏓 Ping тест активирован!")
        ui.showMessage("[AI] 🏓 Ping тест - сервер доступен!")
        
        -- Можно добавить реальный ping к серверу
        aiInit.testConnection()
        
    elseif key.symbol == input.KEY.I then
        log("ℹ️ Информация о системе")
        ui.showMessage("[AI] ℹ️ Система активна. Сервер: " .. config.HTTP_SERVER_URL)
        
        -- Показываем детальную информацию
        aiInit.showSystemInfo()
        
    elseif key.symbol == input.KEY.O then
        log("💬 Тест диалога активирован!")
        ui.showMessage("[AI] 💬 Тестируем диалог с ИИ...")
        
        -- Запускаем тестовый диалог
        aiInit.testDialogue()
    end
end

-- Обработчик нажатия клавиш (для зажимания)
local function onKeyDown(key)
    if key.symbol == input.KEY.LeftAlt and not voiceRecording then
        voiceRecording = true
        voiceStartTime = util.getRealTime()
        
        log("🎤 Голосовой ввод начат...")
        ui.showMessage("[AI] 🎤 Говорите... (отпустите Alt)")
    end
end

-- Обработчик отпускания клавиш  
local function onKeyUp(key)
    if key.symbol == input.KEY.LeftAlt and voiceRecording then
        voiceRecording = false
        local duration = util.getRealTime() - voiceStartTime
        
        log("🎤 Голосовой ввод завершен (длительность: " .. string.format("%.1f", duration) .. "с)")
        ui.showMessage("[AI] 🎤 Голос обработан (" .. string.format("%.1f", duration) .. "с)")
        
        -- Отправляем голосовой запрос
        aiInit.processVoiceInput(duration)
    end
end

-- Инициализация глобальных обработчиков
local function onInit()
    log("🚀 Инициализация глобальных обработчиков AI...")
    ui.showMessage("[AI] 🚀 Мод загружен! P/I/O - тесты, Alt - голос")
    
    -- Проверяем подключение к AI серверу
    aiInit.initializeAI()
end

-- Экспортируем обработчики для OpenMW
M.engineHandlers = {
    onInit = onInit,
    onKeyPress = onKeyPress, 
    onKeyDown = onKeyDown,
    onKeyUp = onKeyUp
}

return M
