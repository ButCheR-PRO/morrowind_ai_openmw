local ui = require('openmw.ui')
local util = require('openmw.util')

local M = {}

-- Импорт конфигурации
local config = require('scripts.morrowind_ai.config')

-- Функция логирования
local function log(message)
    print("[AI Init] " .. message)
end

-- Проверка подключения к AI серверу
function M.testConnection()
    log("🔗 Тестируем подключение к AI серверу...")
    ui.showMessage("[AI] 🔗 Проверяем связь с сервером...")
    
    -- TODO: Реальный HTTP запрос
    -- Пока показываем заглушку
    ui.showMessage("[AI] ✅ Сервер отвечает: " .. config.HTTP_SERVER_URL)
end

-- Показать информацию о системе
function M.showSystemInfo()
    log("📊 Показываем информацию о системе...")
    
    local info = {
        "🤖 AI Мод для Morrowind активен!",
        "🌐 Сервер: " .. config.HTTP_SERVER_URL,
        "🎤 Голосовой ввод: поддерживается",
        "⌨️ Горячие клавиши: P/I/O/Alt",
        "📡 Статус: подключен"
    }
    
    for _, line in ipairs(info) do
        ui.showMessage(line)
    end
end

-- Инициализация AI системы
function M.initializeAI()
    log("🚀 Инициализация AI системы...")
    ui.showMessage("[AI] 🚀 AI система инициализирована")
    
    -- Проверяем доступность модулей
    local modules = {
        'openmw.ui',
        'openmw.input', 
        'openmw.util',
        'scripts.morrowind_ai.config',
        'scripts.morrowind_ai.http_client'
    }
    
    for _, module in ipairs(modules) do
        local ok, mod = pcall(require, module)
        if ok then
            log("✅ Модуль загружен: " .. module)
        else
            log("❌ Ошибка загрузки модуля: " .. module)
        end
    end
end

-- Обработка голосового ввода
function M.processVoiceInput(duration)
    log("🎤 Обрабатываем голосовой ввод (длительность: " .. string.format("%.1f", duration) .. "с)")
    
    if duration < 0.5 then
        ui.showMessage("[AI] ⚠️ Слишком короткая запись (мин. 0.5с)")
        return
    end
    
    if duration > 30.0 then
        ui.showMessage("[AI] ⚠️ Слишком длинная запись (макс. 30с)")
        return
    end
    
    -- TODO: Отправка аудио на сервер для распознавания
    ui.showMessage("[AI] 🔄 Распознаем речь... (" .. string.format("%.1f", duration) .. "с)")
    
    -- Заглушка - имитируем ответ сервера
    local dummyText = "Привет от голосового ввода!"
    ui.showMessage("[AI] 📝 Распознано: '" .. dummyText .. "'")
end

-- Существующая функция testDialogue (оставляем как есть)
function M.testDialogue()
    log("🧪 Тестируем диалоговую систему...")
    
    local testMessage = "Привет! Как дела?"
    log("📤 Отправка: " .. testMessage)
    ui.showMessage("[AI] 📤 Отправляем: " .. testMessage)
    
    -- Имитируем ответ НПС
    local npcResponse = "Приветствую, путник! Я рад тебя видеть в этих землях."
    log("📥 Ответ НПС: " .. npcResponse)
    ui.showMessage("[AI] 📥 НПС ответил: " .. npcResponse)
end

return M
