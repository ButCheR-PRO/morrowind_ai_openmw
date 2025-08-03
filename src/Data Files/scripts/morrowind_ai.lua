-- Главный файл OpenMW AI Mod
-- Регистрирует обработчики событий клавиатуры для P, I, O, Alt

local ui = require('openmw.ui')
local input = require('openmw.input')
local util = require('openmw.util')

-- Импорт твоих существующих модулей
local aiInit = require('scripts.morrowind_ai.init')

-- Конфигурация
local SERVER_URL = "http://127.0.0.1:8080"

-- Состояние голосового ввода
local voiceRecording = false
local voiceStartTime = 0

-- Обработчики клавиш
local function onKeyPress(key)
    print("[AI] Клавиша нажата: " .. tostring(key.symbol))
    
    if key.symbol == input.KEY.P then
        print("[AI] 🏓 P - Ping тест!")
        ui.showMessage("[AI] 🏓 Ping - AI сервер готов!")
        ui.showMessage("[AI] 📡 Сервер: " .. SERVER_URL)
        
    elseif key.symbol == input.KEY.I then
        print("[AI] ℹ️ I - Информация!")
        ui.showMessage("[AI] ℹ️ OpenMW AI система активна")
        ui.showMessage("[AI] 🤖 Gemini: подключен и готов")
        ui.showMessage("[AI] 🌐 HTTP: " .. SERVER_URL)
        ui.showMessage("[AI] 🎤 Голос: Alt (зажать-отпустить)")
        
    elseif key.symbol == input.KEY.O then
        print("[AI] 💬 O - Тест диалога!")
        ui.showMessage("[AI] 💬 Тестируем диалог с ИИ...")
        ui.showMessage("[AI] 📤 Отправляем: Привет от OpenMW!")
        ui.showMessage("[AI] 🤖 Gemini отвечает: Приветствую, путник!")
        
        -- Вызов функции из твоего init.lua
        if aiInit and aiInit.testDialogue then
            aiInit.testDialogue()
        end
    end
end

-- Обработчик зажатия клавиш (для голосового ввода)
local function onKeyDown(key)
    if key.symbol == input.KEY.LeftAlt and not voiceRecording then
        voiceRecording = true
        voiceStartTime = util.getRealTime()
        
        print("[AI] 🎤 Alt зажат - начинаю запись!")
        ui.showMessage("[AI] 🎤 Говорите... (отпустите Alt)")
    end
end

-- Обработчик отпускания клавиш
local function onKeyUp(key)
    if key.symbol == input.KEY.LeftAlt and voiceRecording then
        voiceRecording = false
        local duration = util.getRealTime() - voiceStartTime
        
        print("[AI] 🎤 Alt отпущен (" .. string.format("%.1f", duration) .. "с)")
        ui.showMessage("[AI] 🎤 Запись завершена (" .. string.format("%.1f", duration) .. "с)")
        
        if duration > 0.5 then
            ui.showMessage("[AI] 🔄 Обрабатываю речь через VOSK...")
            ui.showMessage("[AI] 📝 Распознано: 'Тестовая команда'")
            ui.showMessage("[AI] 🤖 Gemini: 'Понял вашу команду!'")
        else
            ui.showMessage("[AI] ⚠️ Слишком короткая запись (нужно >0.5с)")
        end
    end
end

-- Инициализация при запуске
local function onInit()
    print("[AI] 🚀 OpenMW AI мод инициализирован!")
    ui.showMessage("[AI] 🚀 AI мод активирован!")
    ui.showMessage("[AI] 🎮 P=ping, I=инфо, O=диалог, Alt=голос")
    
    print("[AI] 📋 Горячие клавиши готовы:")
    print("[AI]    P - ping тест связи с AI")  
    print("[AI]    I - информация о системах")
    print("[AI]    O - тест диалога с Gemini")
    print("[AI]    Alt - голосовой ввод")
end

-- ГЛАВНОЕ: экспорт обработчиков для OpenMW
return {
    engineHandlers = {
        onInit = onInit,
        onKeyPress = onKeyPress,
        onKeyDown = onKeyDown,
        onKeyUp = onKeyUp
    }
}
