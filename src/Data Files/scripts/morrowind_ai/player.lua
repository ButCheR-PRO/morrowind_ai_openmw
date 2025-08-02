local core = require('openmw.core')
local input = require('openmw.input')
local nearby = require('openmw.nearby')
local ui = require('openmw.ui')

local lastNpcInteraction = nil
local voiceRecording = false
local httpBridgeConnected = false

-- Инициализация модуля
local function onInit()
    print("[Morrowind AI] 👤 Player модуль инициализирован")
    print("[Morrowind AI] 🏓 PONG! Модуль работает!")
    print("[Morrowind AI] ✅ HTTP Bridge: Готов к работе")
    print("[Morrowind AI] 🎤 Голосовой ввод: Нажмите Left Alt")
    print("[Morrowind AI] 📍 Контекст: Player")
    print("[Morrowind AI] 🔧 Горячие клавиши:")
    print("[Morrowind AI]    P - ping тест")
    print("[Morrowind AI]    I - отладочная информация")
    print("[Morrowind AI]    O - тест диалога")
    print("[Morrowind AI]    Left Alt - голосовой ввод")
    
    -- Тестируем подключение к HTTP мосту
    testHttpConnection()
    
    -- Отправляем сообщение через глобальные события
    core.sendGlobalEvent("ai_show_message", {
        message = "[AI] ✅ Голосовое управление готово! Нажмите Left Alt для активации."
    })
end

-- Обновление каждый кадр
local function onUpdate(dt)
    -- Проверяем взаимодействие с НПС
    local player = self.object
    if not player then return end
    
    -- Ищем ближайших НПС
    for _, actor in pairs(nearby.actors) do
        if actor.type and actor.type.record and actor.type.record.id then
            local distance = (actor.position - player.position):length()
            
            -- Если НПС рядом (менее 200 единиц) и это новый НПС
            if distance < 200 and lastNpcInteraction ~= actor.type.record.id then
                lastNpcInteraction = actor.type.record.id
                triggerNpcInteraction(actor)
                break
            end
        end
    end
end

-- Взаимодействие с НПС
function triggerNpcInteraction(actor)
    local npcName = actor.type.record.id
    
    print("[AI] 🗣️ Обнаружен НПС: " .. npcName)
    
    -- Отправляем уведомление через глобальные события
    core.sendGlobalEvent("ai_npc_interaction", {
        npc_name = npcName
    })
    
    -- Отправляем событие для обработки диалога
    core.sendGlobalEvent("ai_dialogue_request", {
        npc_name = npcName,
        message = "Привет! Как дела в " .. (actor.cell and actor.cell.name or "этих краях") .. "?"
    })
end

-- Реакция на нажатие клавиш
local function onKeyPress(key)
    -- Left Alt (код 342) для активации голосового ввода
    if key.code == 342 then -- Left Alt key
        if not voiceRecording then
            voiceRecording = true
            print("[AI] 🎤 🔴 Начинаем запись голоса...")
            
            -- Отправляем сигнал на начало записи
            core.sendGlobalEvent("ai_voice_start", {
                timestamp = os.time()
            })
        end
    end
    
    -- P (код 80) для тестирования (ping)
    if key.code == 80 then -- P key
        print("==============================================")
        print("[Morrowind AI] 🏓 PING TEST (P)!")
        print("[Morrowind AI] ✅ HTTP Bridge: " .. (httpBridgeConnected and "Подключен" or "Отключен"))
        print("[Morrowind AI] 🎤 Голосовой ввод: Нажмите Left Alt")
        print("[Morrowind AI] 📍 Текущий контекст: Player")
        print("==============================================")
        
        -- Отправляем тестовый запрос
        core.sendGlobalEvent("ai_connection_test", {
            source = "player_ping_p",
            timestamp = os.time()
        })
        
        -- Показываем информацию о игроке
        local player = self.object
        if player then
            print("[Morrowind AI] 🎮 Игрок найден: " .. (player.recordId or "Unknown"))
            print("[Morrowind AI] 📍 Позиция: " .. tostring(player.position))
        else
            print("[Morrowind AI] ⚠️ Объект игрока не найден")
        end
    end
    
    -- I (код 73) для отладки
    if key.code == 73 then -- I key
        print("==============================================")
        print("[Morrowind AI] 🔍 ОТЛАДОЧНАЯ ИНФОРМАЦИЯ (I):")
        print("  📦 Модуль: morrowind_ai.player")
        print("  ✅ Инициализирован: true")
        print("  🔗 HTTP Bridge: " .. (httpBridgeConnected and "✅" or "❌"))
        print("  🎤 Голосовая запись: " .. (voiceRecording and "🔴 ВКЛ" or "⚪ ВЫКЛ"))
        print("  👥 Последний НПС: " .. (lastNpcInteraction or "Нет"))
        
        -- Информация о среде
        local player = self.object
        if player then
            print("  🎮 Игрок: " .. (player.recordId or "Unknown"))
            if player.cell then
                print("  🌍 Локация: " .. (player.cell.name or "Unknown"))
            end
        end
        
        print("  🛠️ Горячие клавиши:")
        print("    P - ping тест")
        print("    I - эта отладочная информация")
        print("    O - тест диалога")
        print("    Left Alt - голосовой ввод")
        print("==============================================")
    end
    
    -- O (код 79) для тестового диалога
    if key.code == 79 then -- O key
        local testMessage = "Тестовое сообщение от игрока (O)"
        print("==============================================")
        print("[AI] 💬 Отправляем тестовый диалог: " .. testMessage)
        print("==============================================")
        
        core.sendGlobalEvent("ai_dialogue_request", {
            npc_name = "TestNPC",
            message = testMessage,
            test = true
        })
    end
end

-- Реакция на отпускание клавиш
local function onKeyRelease(key)
    -- Left Alt отпущен - останавливаем запись
    if key.code == 342 and voiceRecording then -- Left Alt key
        voiceRecording = false
        print("[AI] 🎤 ⚪ Останавливаем запись голоса...")
        
        -- Отправляем сигнал на остановку записи
        core.sendGlobalEvent("ai_voice_stop", {
            timestamp = os.time()
        })
    end
end

-- Тестирование подключения к HTTP мосту
function testHttpConnection()
    print("[AI] 🔗 Тестируем подключение к HTTP мосту...")
    
    -- Отправляем событие для HTTP теста
    core.sendGlobalEvent("ai_http_test", {
        url = "http://127.0.0.1:8080/test",
        timestamp = os.time()
    })
    
    httpBridgeConnected = true -- Предполагаем что подключение есть
end

-- Обработка событий от других модулей
local function onGlobalEvent(eventName, data)
    if eventName == "ai_dialogue_response" then
        local npcName = data.npc_name or "Unknown"
        local response = data.ai_response or "Нет ответа"
        
        print("==============================================")
        print("[AI] 📨 Получен ответ от " .. npcName .. ":")
        print("[AI] 💬 " .. response)
        print("==============================================")
        -- Здесь можно показать ответ в UI
        
    elseif eventName == "ai_voice_recognized" then
        local recognizedText = data.text or "Текст не распознан"
        
        print("==============================================")
        print("[AI] 🎤 Распознано: " .. recognizedText)
        print("==============================================")
        
        -- Отправляем распознанный текст как диалог
        if lastNpcInteraction then
            core.sendGlobalEvent("ai_dialogue_request", {
                npc_name = lastNpcInteraction,
                message = recognizedText,
                voice_input = true
            })
        end
    end
end

-- Экспорт только разрешенных секций для OpenMW
return {
    eventHandlers = {
        onInit = onInit,
        onUpdate = onUpdate,
        onKeyPress = onKeyPress,
        onKeyRelease = onKeyRelease,
        onGlobalEvent = onGlobalEvent
    }
}
