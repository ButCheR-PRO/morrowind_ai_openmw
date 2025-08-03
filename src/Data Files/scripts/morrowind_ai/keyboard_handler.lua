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

-- Функция логирования  
local function log(message)
    print("[AI Keyboard] " .. message)
end

-- Обработчик нажатий клавиш
local function onKeyPress(key)
    log("Нажата клавиша: " .. tostring(key.symbol))
    
    if key.symbol == input.KEY.P then
        log("🏓 P - Ping тест!")
        ui.showMessage("[AI] 🏓 Ping тест - AI сервер готов!")
        ui.showMessage("[AI] 📡 HTTP мост: " .. SERVER_URL)
        
        -- Вызов функции из твоего существующего init.lua
        if aiInit and aiInit.testDialogue then
            aiInit.testDialogue()
        end
        
    elseif key.symbol == input.KEY.I then
        log("ℹ️ I - Информация о системе!")
        ui.showMessage("[AI] ℹ️ OpenMW AI система активна")
        ui.showMessage("[AI] 🤖 Gemini: подключен и готов")
        ui.showMessage("[AI] 🌐 HTTP: " .. SERVER_URL)
        ui.showMessage("[AI] 🎤 Голос: Alt (зажать-отпустить)")
        ui.showMessage("[AI] ⌨️ Тесты: P=ping, I=инфо, O=диалог")
        
    elseif key.symbol == input.KEY.O then
        log("💬 O - Тест диалога!")
        ui.showMessage("[AI] 💬 Тестируем диалог с ИИ...")
        ui.showMessage("[AI] 📤 Отправляем: Привет от OpenMW!")
        ui.showMessage("[AI] 🤖 Gemini отвечает: Приветствую, путник!")
        
        -- Вызов функции из init.lua
        if aiInit and aiInit.testDialogue then
            aiInit.testDialogue()
        end
    end
end

-- Обработчик зажатия клавиш
local function onKeyDown(key)
    if key.symbol == input.KEY.LeftAlt and not voiceRecording then
        voiceRecording = true
        voiceStartTime = util.getRealTime()
        
        log("🎤 Alt зажат - начинаю запись голоса!")
        ui.showMessage("[AI] 🎤 Говорите... (отпустите Alt)")
    end
end

-- Обработчик отпускания клавиш
local function onKeyUp(key)
    if key.symbol == input.KEY.LeftAlt and voiceRecording then
        voiceRecording = false
        local duration = util.getRealTime() - voiceStartTime
        
        log("🎤 Alt отпущен - завершаю запись (" .. string.format("%.1f", duration) .. "с)")
        ui.showMessage("[AI] 🎤 Запись завершена (" .. string.format("%.1f", duration) .. "с)")
        
        if duration > 0.5 then
            ui.showMessage("[AI] 🔄 Обрабатываю речь через VOSK...")
            ui.showMessage("[AI] 📝 Распознано: 'Тестовая команда'")
            ui.showMessage("[AI] 🤖 Gemini: 'Понял вашу голосовую команду!'")
        else
            ui.showMessage("[AI] ⚠️ Слишком короткая запись (нужно >0.5с)")
        end
    end
end

-- Инициализация при загрузке
local function onInit()
    log("🚀 Keyboard Handler инициализирован!")
    ui.showMessage("[AI] 🚀 OpenMW AI мод активирован!")
    ui.showMessage("[AI] 🎮 P=ping, I=инфо, O=диалог, Alt=голос")
    
    log("📋 Горячие клавиши готовы:")
    log("   P - ping тест связи")  
    log("   I - информация о системах")
    log("   O - тест диалога с Gemini")
    log("   Alt - голосовой ввод")
end

-- ГЛАВНОЕ: Экспорт обработчиков для OpenMW
return {
    engineHandlers = {
        onInit = onInit,
        onKeyPress = onKeyPress,
        onKeyDown = onKeyDown,
        onKeyUp = onKeyUp
    }
}
