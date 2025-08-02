local socket = require('socket')
local json = require('json')

local M = {}
local client = nil
local isConnected = false

function M.init()
    M.connect()
end

function M.connect()
    client = socket.tcp()
    client:settimeout(0) -- Неблокирующий режим
    
    local result = client:connect("127.0.0.1", 18080)
    if result == 1 then
        isConnected = true
        print("[Morrowind AI] Подключено к серверу")
    else
        print("[Morrowind AI] Не удалось подключиться к серверу")
    end
end

function M.sendToServer(data)
    if not isConnected then return nil end
    
    local jsonData = json.encode(data)
    client:send(jsonData .. "\n")
end

function M.receiveFromServer()
    if not isConnected then return nil end
    
    local response = client:receive()
    if response then
        return json.decode(response)
    end
    return nil
end

function M.update(dt)
    -- Проверка соединения и переподключение
    if not isConnected then
        M.connect()
    end
end

return M
