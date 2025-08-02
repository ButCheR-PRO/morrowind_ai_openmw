#!/usr/bin/env python3
import socket
import json
import time

def test_server():
    print("🔍 Тестируем подключение к серверу...")
    
    try:
        # Подключаемся к серверу
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(5)
        client.connect(("127.0.0.1", 8080))
        
        print("✅ Подключение к серверу успешно!")
        
        # Отправляем тестовое сообщение
        test_message = {
            "type": "test_connection",
            "data": "Привет от тестового клиента!"
        }
        
        message_json = json.dumps(test_message) + "\n"
        client.send(message_json.encode('utf-8'))
        print("📤 Сообщение отправлено")
        
        # Ждём ответ
        response = client.recv(1024).decode('utf-8')
        if response:
            print(f"📥 Ответ сервера: {response}")
        else:
            print("❌ Сервер не ответил")
            
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

if __name__ == "__main__":
    test_server()

