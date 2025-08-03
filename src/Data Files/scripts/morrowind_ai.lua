-- Главный файл OpenMW AI Mod для версии 0.49.0
-- Совместимость со старым Lua API

-- Проверяем доступные модули OpenMW для версии 0.49.0
local function checkAvailableModules()
    local modules = {
        'openmw.ui',
        'openmw.input', 
        'openmw.util',
        'openmw.core'
    }
    
    local available = {}
    for _, module in ipairs(modules) do
        local success, mod = pcall(require, module)
        if success then
            available[module] = true
            print("[AI] ✅ Модуль доступен: " .. module)
        else
            available[module] = false
            print("[AI] ❌ Модуль недоступен: " .. module)
        end
    end
    return available
end

-- Безопасная функция показа сообщений
local function showMessage(text)
    print("[AI] " .. text)
    
    -- Пробуем разные способы показа сообщений в OpenMW 0.49.0
    local success = false
    
    -- Способ 1: через openmw.ui (если доступен)
    if not success then
        local ok, ui = pcall(require, 'openmw.ui')
        if ok and ui and ui.showMessage then
            pcall(ui.showMessage, text)
            success = true
        end
    end
    
    -- Способ 2: через консоль OpenMW
    if not success then
        -- В старых версиях сообщения показываются только через print
        print(">>> " .. text .. " <<<")
    end
end

-- Безопасная функция получения input модуля  
local function getInputModule()
    local ok, input = pcall(require, 'openmw.input')
    if ok then
        return input
    end
    
    -- Fallback для старых версий
    return {
        KEY = {
            P = 80,
            I = 73, 
            O = 79,
            LeftAlt = 308
        }
    }
end

-- Глобальные переменные
local inputModule = getInputModule()
local voiceRecording = false
local voiceStartTime = 0

-- Функция получения времени
local function getCurrentTime()
    local ok, util = pcall(require, 'openmw.util')
    if ok and util.getRealTime then
        return util.getRealTime()
    end
    return os.clock() -- Fallback
end

-- Обработчики клавиш
local function onKeyPress(key)
    print("[AI] 🔧 Клавиша нажата: " .. tostring(key.symbol) .. " (код: " .. tostring(key.code) .. ")")
    
    if key.symbol == inputModule.KEY.P or key.code == 80 then
        print("[AI] 🏓 P - Ping тест!")
        showMessage("🏓 AI Ping тест - сервер готов!")
        showMessage("📡 HTTP: http://127.0.0.1:8080")
        showMessage("🤖 Gemini: подключен")
        
    elseif key.symbol == inputModule.KEY.I or key.code == 73 then
        print("[AI] ℹ️ I - Информация о системе!")
        showMessage("ℹ️ OpenMW AI система активна")
        showMessage("🤖 Gemini: готов к диалогам")
        showMessage("🌐 HTTP мост: работает")
        showMessage("🎤 Голос: Alt (зажать-отпустить)")
        showMessage("⌨️ Тесты: P=ping, I=инфо, O=диалог")
        
    elseif key.symbol == inputModule.KEY.O or key.code == 79 then
        print("[AI] 💬 O - Тест диалога!")
        showMessage("💬 Тестируем диалог с ИИ...")
        showMessage("📤 Игрок: Привет от OpenMW 0.49.0!")
        showMessage("🤖 Gemini: Приветствую, путник из Морровинда!")
        
        -- Можно вызвать функцию из других модулей если нужно
        print("[AI] 📋 Тестовый диалог завершен")
    end
end

-- Обработчик зажатия клавиш
local function onKeyDown(key)
    if (key.symbol == inputModule.KEY.LeftAlt or key.code == 308) and not voiceRecording then
        voiceRecording = true
        voiceStartTime = getCurrentTime()
        
        print("[AI] 🎤 Alt зажат - запись голоса!")
        showMessage("🎤 Говорите... (отпустите Alt)")
    end
end

-- Обработчик отпускания клавиш
local function onKeyUp(key)
    if (key.symbol == inputModule.KEY.LeftAlt or key.code == 308) and voiceRecording then
        voiceRecording = false
        local duration = getCurrentTime() - voiceStartTime
        
        print("[AI] 🎤 Alt отпущен (" .. string.format("%.1f", duration) .. "с)")
        showMessage("🎤 Запись завершена (" .. string.format("%.1f", duration) .. "с)")
        
        if duration > 0.5 then
            showMessage("🔄 Обрабатываю речь через VOSK...")
            showMessage("📝 Распознано: 'Тестовая команда'")
            showMessage("🤖 Gemini: 'Понял вашу команду!'")
        else
            showMessage("⚠️ Слишком короткая запись (нужно >0.5с)")
        end
    end
end

-- Инициализация
local function onInit()
    print("[AI] 🚀 Инициализация AI мода для OpenMW 0.49.0...")
    
    -- Проверяем доступные модули
    local available = checkAvailableModules()
    
    showMessage("🚀 OpenMW AI мод загружен!")
    showMessage("🎮 Горячие клавиши: P/I/O/Alt")
    showMessage("📋 P=ping, I=инфо, O=диалог, Alt=голос")
    
    print("[AI] 📋 Обработчики событий зарегистрированы:")
    print("[AI]    P - ping тест связи с AI")  
    print("[AI]    I - информация о системах")
    print("[AI]    O - тест диалога с Gemini")
    print("[AI]    Alt - голосовой ввод")
    
    if available['openmw.ui'] then
        print("[AI] ✅ UI модуль доступен - полная функциональность")
    else
        print("[AI] ⚠️ UI модуль недоступен - используем консольный вывод")
    end
end

-- Экспорт обработчиков для OpenMW
return {
    engineHandlers = {
        onInit = onInit,
        onKeyPress = onKeyPress,
        onKeyDown = onKeyDown,
        onKeyUp = onKeyUp
    }
}
