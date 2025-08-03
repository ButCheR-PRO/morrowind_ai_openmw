-- ============================================================================
-- Morrowind AI Mod v1.0 - Главный модуль
-- Интеграция с Google Gemini через HTTP сервер
-- Совместимость: OpenMW 0.49.0
-- ============================================================================

local util = require('openmw.util')
local core = require('openmw.core')

-- Конфигурация
local CONFIG = {
    version = "1.0",
    debug = true,
    server_host = "localhost",
    server_port = 8080,
    temp_dir = "Data Files/ai_temp/",
    request_file = "Data Files/ai_temp/ai_request.json",
    response_file = "Data Files/ai_temp/ai_response.json", 
    signal_file = "Data Files/ai_temp/ai_signal.txt",
    check_interval = 1.0  -- секунды между проверками ответов
}

-- Глобальные переменные
local aiRequestQueue = {}
local isProcessing = false
local lastResponseCheck = 0

-- ============================================================================
-- УТИЛИТЫ И ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
-- ============================================================================

local function debugPrint(message)
    if CONFIG.debug then
        print("[Morrowind AI] " .. tostring(message))
    end
end

local function ensureTempDirectory()
    -- Создаем временную директорию если её нет
    local temp_dir = CONFIG.temp_dir
    debugPrint("Проверяем временную директорию: " .. temp_dir)
    
    -- Пытаемся создать тестовый файл для проверки директории
    local test_file = temp_dir .. "test.tmp"
    local file = io.open(test_file, "w")
    if file then
        file:write("test")
        file:close()
        os.remove(test_file)
        debugPrint("Временная директория готова")
        return true
    else
        debugPrint("ОШИБКА: Не удается создать временную директорию")
        return false
    end
end

local function generateRequestId()
    return "req_" .. tostring(os.time()) .. "_" .. tostring(math.random(1000, 9999))
end

-- ============================================================================
-- РАБОТА С ФАЙЛОВОЙ СИСТЕМОЙ (ОСНОВНАЯ ИНТЕГРАЦИЯ)
-- ============================================================================

local function writeJsonFile(filename, data)
    local file = io.open(filename, "w")
    if not file then
        debugPrint("ОШИБКА: Не удается создать файл " .. filename)
        return false
    end
    
    -- Простая JSON сериализация
    local json_string = string.format([[{
    "request_id": "%s",
    "npc_name": "%s",
    "message": "%s",
    "context": "%s",
    "language": "ru",
    "timestamp": %d,
    "game": "morrowind",
    "mod_version": "%s"
}]], 
        data.request_id or "",
        data.npc_name or "",
        data.message or "",
        data.context or "",
        data.timestamp or os.time(),
        CONFIG.version
    )
    
    file:write(json_string)
    file:close()
    debugPrint("JSON записан в файл: " .. filename)
    return true
end

local function readJsonFile(filename)
    local file = io.open(filename, "r")
    if not file then
        return nil
    end
    
    local content = file:read("*all")
    file:close()
    
    if content and content ~= "" then
        debugPrint("JSON прочитан из файла: " .. filename)
        return content
    end
    
    return nil
end

local function createSignalFile()
    local file = io.open(CONFIG.signal_file, "w")
    if file then
        file:write("new_request_" .. tostring(os.time()))
        file:close()
        debugPrint("Сигнальный файл создан")
        return true
    end
    return false
end

local function removeFile(filename)
    local success = os.remove(filename)
    if success then
        debugPrint("Файл удален: " .. filename)
    end
    return success
end

-- ============================================================================
-- AI ИНТЕГРАЦИЯ (ОСНОВНЫЕ ФУНКЦИИ)
-- ============================================================================

local function sendToAI(npcName, message, context)
    debugPrint("=== ОТПРАВКА ЗАПРОСА К AI СЕРВЕРУ ===")
    debugPrint("НПС: " .. tostring(npcName))
    debugPrint("Сообщение: " .. tostring(message))
    debugPrint("Контекст: " .. tostring(context))
    
    if isProcessing then
        debugPrint("ВНИМАНИЕ: Предыдущий запрос еще обрабатывается")
        return false
    end
    
    -- Подготавливаем данные запроса
    local requestData = {
        request_id = generateRequestId(),
        npc_name = npcName,
        message = message,
        context = context,
        timestamp = os.time()
    }
    
    -- Записываем запрос в файл
    if writeJsonFile(CONFIG.request_file, requestData) then
        -- Создаем сигнальный файл для сервера
        if createSignalFile() then
            isProcessing = true
            debugPrint("Запрос успешно отправлен на сервер")
            
            -- Добавляем в очередь для отслеживания
            table.insert(aiRequestQueue, {
                id = requestData.request_id,
                npc = npcName,
                sent_time = os.time()
            })
            
            return true
        else
            debugPrint("ОШИБКА: Не удается создать сигнальный файл")
        end
    else
        debugPrint("ОШИБКА: Не удается записать файл запроса")
    end
    
    return false
end

local function checkForAIResponse()
    -- Проверяем есть ли файл ответа
    local response_content = readJsonFile(CONFIG.response_file)
    
    if response_content then
        debugPrint("=== ПОЛУЧЕН ОТВЕТ ОТ AI СЕРВЕРА ===")
        debugPrint("Содержимое ответа:")
        debugPrint(response_content)
        
        -- Удаляем файл ответа после прочтения
        removeFile(CONFIG.response_file)
        
        -- Сбрасываем флаг обработки
        isProcessing = false
        
        -- Обрабатываем ответ
        processAIResponse(response_content)
        
        return true
    end
    
    return false
end

local function processAIResponse(responseData)
    debugPrint("=== ОБРАБОТКА AI ОТВЕТА ===")
    
    -- Здесь можно добавить парсинг JSON ответа
    -- Пока просто выводим в лог
    debugPrint("AI ответ получен и готов к обработке")
    debugPrint("Данные: " .. tostring(responseData))
    
    -- TODO: Интеграция с диалоговой системой OpenMW
    -- TODO: Отображение ответа игроку
    
    -- Очищаем очередь запросов
    aiRequestQueue = {}
end

-- ============================================================================
-- АВТОМАТИЧЕСКИЕ СИСТЕМЫ И СОБЫТИЯ
-- ============================================================================

local function startAutoDialogue()
    debugPrint("=== ЗАПУСК АВТОМАТИЧЕСКОГО ДИАЛОГА ===")
    
    -- Тестовый запрос к AI для проверки
    local testNPC = "Caius Cosades"
    local testMessage = "Привет, как дела? Есть ли у тебя задания?"
    local testContext = "Игрок впервые встречает НПС в Балморе"
    
    sendToAI(testNPC, testMessage, testContext)
end

local function periodicCheck()
    local currentTime = os.time()
    
    -- Проверяем ответы каждую секунду
    if currentTime - lastResponseCheck >= CONFIG.check_interval then
        checkForAIResponse()
        lastResponseCheck = currentTime
    end
    
    -- Проверяем таймауты запросов (если запрос висит больше 30 сек)
    for i = #aiRequestQueue, 1, -1 do
        local request = aiRequestQueue[i]
        if currentTime - request.sent_time > 30 then
            debugPrint("ТАЙМАУТ запроса: " .. request.id)
            table.remove(aiRequestQueue, i)
            isProcessing = false
        end
    end
end

-- ============================================================================
-- ОСНОВНЫЕ ФУНКЦИИ МОДА
-- ============================================================================

local function onInit()
    debugPrint("=================================================")
    debugPrint("🤖 MORROWIND AI MOD v" .. CONFIG.version .. " ЗАГРУЖАЕТСЯ...")
    debugPrint("=================================================")
    
    -- Проверяем совместимость OpenMW
    debugPrint("Версия OpenMW: " .. tostring(core.API_REVISION or "неизвестно"))
    debugPrint("Доступные модули:")
    debugPrint("- openmw.util: " .. (util and "✅" or "❌"))
    debugPrint("- openmw.core: " .. (core and "✅" or "❌"))
    
    -- Инициализируем файловую систему
    if ensureTempDirectory() then
        debugPrint("✅ Файловая система готова")
    else
        debugPrint("❌ КРИТИЧЕСКАЯ ОШИБКА: Проблемы с файловой системой")
        return
    end
    
    -- Устанавливаем начальное время проверки
    lastResponseCheck = os.time()
    
    debugPrint("=================================================")
    debugPrint("🎮 MORROWIND AI MOD УСПЕШНО ИНИЦИАЛИЗИРОВАН!")
    debugPrint("🔗 Готов к подключению с AI сервером на порту " .. CONFIG.server_port)
    debugPrint("📁 Временные файлы: " .. CONFIG.temp_dir)
    debugPrint("=================================================")
    
    -- Запускаем тестовый диалог через 5 секунд
    debugPrint("⏰ Запуск тестового AI диалога через 5 секунд...")
    
    -- TODO: Здесь должен быть таймер, но в OpenMW 0.49.0 его нет
    -- Пока запускаем сразу для тестирования
    startAutoDialogue()
end

-- В OpenMW нет onUpdate, поэтому используем другой подход
-- Эта функция должна вызываться периодически через другие события
local function update()
    periodicCheck()
end

-- ============================================================================
-- ЭКСПОРТ МОДУЛЯ (для OpenMW)
-- ============================================================================

-- В OpenMW 0.49.0 экспорт функций ограничен, поэтому регистрируем события напрямую
-- Инициализация происходит автоматически при загрузке скрипта

-- Вызываем инициализацию
onInit()

-- Для тестирования можно вызвать update периодически
-- update()

debugPrint("🚀 Модуль Morrowind AI полностью загружен!")

-- ============================================================================
-- КОНЕЦ ФАЙЛА
-- ============================================================================
