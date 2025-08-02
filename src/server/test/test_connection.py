#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import json
import time
import sys
import yaml
import asyncio
import aiohttp
from pathlib import Path
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config():
    """Загрузка конфигурации"""
    config_path = Path('config.yml')
    
    # Ищем config.yml в текущей и родительских директориях
    if not config_path.exists():
        for parent in Path.cwd().parents:
            potential_config = parent / 'config.yml'
            if potential_config.exists():
                config_path = potential_config
                break
        else:
            logger.warning("⚠️ config.yml не найден, используем настройки по умолчанию")
            return {}
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            logger.info(f"✅ Конфигурация загружена из {config_path}")
            return config or {}
    except Exception as e:
        logger.error(f"❌ Ошибка загрузки конфигурации: {e}")
        return {}

def test_tcp_connection(host, port, timeout=5):
    """Тест TCP подключения"""
    print(f"🔍 Тестируем TCP подключение к {host}:{port}...")
    
    try:
        # Подключаемся к серверу
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(timeout)
        
        start_time = time.time()
        result = client.connect_ex((host, port))
        connect_time = time.time() - start_time
        
        if result == 0:
            print(f"✅ TCP подключение успешно! Время: {connect_time:.3f}с")
            client.close()
            return True
        else:
            print(f"❌ TCP подключение неудачно (код: {result})")
            return False
            
    except socket.timeout:
        print(f"❌ Таймаут TCP подключения ({timeout}с)")
        return False
    except Exception as e:
        print(f"❌ Ошибка TCP подключения: {e}")
        return False

def test_socket_message(host, port, timeout=5):
    """Тест отправки сообщения через сокет"""
    print(f"📤 Тестируем отправку сообщения через сокет...")
    
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(timeout)
        client.connect((host, port))
        
        # Отправляем тестовое сообщение
        test_message = {
            "type": "test_connection",
            "data": "Привет от тестового клиента!",
            "timestamp": time.time()
        }
        
        message_json = json.dumps(test_message, ensure_ascii=False) + "\n"
        client.send(message_json.encode('utf-8'))
        print("📤 Сообщение отправлено")
        
        # Ждём ответ
        client.settimeout(10)  # Увеличиваем таймаут для ответа
        response = client.recv(4096).decode('utf-8')
        
        if response:
            print(f"📥 Ответ сервера ({len(response)} байт): {response.strip()}")
            
            # Пытаемся распарсить JSON ответ
            try:
                response_json = json.loads(response.strip())
                print("✅ Ответ является корректным JSON")
                if isinstance(response_json, dict):
                    for key, value in response_json.items():
                        print(f"   {key}: {value}")
            except json.JSONDecodeError:
                print("⚠️ Ответ не является JSON")
                
            client.close()
            return True
        else:
            print("❌ Сервер не ответил")
            client.close()
            return False
            
    except socket.timeout:
        print("❌ Таймаут при получении ответа")
        return False
    except Exception as e:
        print(f"❌ Ошибка отправки сообщения: {e}")
        return False

async def test_http_endpoint(url, timeout=10):
    """Тест HTTP эндпоинта"""
    print(f"🌐 Тестируем HTTP эндпоинт: {url}")
    
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            start_time = time.time()
            
            async with session.get(url) as response:
                response_time = time.time() - start_time
                content = await response.text()
                
                print(f"📊 HTTP {response.status} - {len(content)} байт - {response_time:.3f}с")
                
                if response.status == 200:
                    print("✅ HTTP эндпоинт доступен")
                    
                    # Пытаемся распарсить JSON
                    try:
                        data = await response.json()
                        print("✅ Ответ содержит корректный JSON:")
                        if isinstance(data, dict):
                            for key, value in data.items():
                                if isinstance(value, (str, int, float, bool)):
                                    print(f"   {key}: {value}")
                                else:
                                    print(f"   {key}: {type(value).__name__}")
                    except:
                        print("⚠️ Ответ не является JSON")
                        print(f"📄 Первые 200 символов: {content[:200]}")
                    
                    return True
                else:
                    print(f"❌ HTTP статус {response.status}")
                    return False
                    
    except asyncio.TimeoutError:
        print(f"❌ HTTP таймаут ({timeout}с)")
        return False
    except aiohttp.ClientError as e:
        print(f"❌ HTTP ошибка: {e}")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return False

async def test_http_post(url, data, timeout=10):
    """Тест HTTP POST запроса"""
    print(f"📤 Тестируем HTTP POST: {url}")
    
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            start_time = time.time()
            
            async with session.post(url, json=data) as response:
                response_time = time.time() - start_time
                content = await response.text()
                
                print(f"📊 HTTP POST {response.status} - {len(content)} байт - {response_time:.3f}с")
                
                if response.status == 200:
                    print("✅ HTTP POST успешен")
                    
                    try:
                        response_data = await response.json()
                        print("✅ Ответ JSON:")
                        if isinstance(response_data, dict):
                            for key, value in response_data.items():
                                if isinstance(value, (str, int, float, bool)):
                                    print(f"   {key}: {value}")
                                else:
                                    print(f"   {key}: {type(value).__name__}")
                    except:
                        print("⚠️ Ответ не JSON")
                        print(f"📄 Ответ: {content[:200]}")
                    
                    return True
                else:
                    print(f"❌ HTTP POST статус {response.status}")
                    print(f"📄 Ответ: {content}")
                    return False
                    
    except Exception as e:
        print(f"❌ Ошибка HTTP POST: {e}")
        return False

async def test_server():
    """Основная функция тестирования"""
    print("🔍 ТЕСТИРОВАНИЕ ПОДКЛЮЧЕНИЯ К СЕРВЕРУ")
    print("=" * 50)
    
    # Загружаем конфигурацию
    config = load_config()
    
    # Получаем настройки подключения
    rpc_config = config.get('rpc', {})
    host = rpc_config.get('host', '127.0.0.1')
    port = rpc_config.get('port', 8080)
    
    print(f"🎯 Целевой сервер: {host}:{port}")
    print(f"📁 Конфигурация: {'найдена' if config else 'по умолчанию'}")
    
    results = []
    
    # 1. Тест TCP подключения
    print(f"\n1️⃣ TCP ПОДКЛЮЧЕНИЕ")
    tcp_result = test_tcp_connection(host, port)
    results.append(("TCP подключение", tcp_result))
    
    if not tcp_result:
        print("❌ TCP подключение неудачно, пропускаем остальные тесты")
        print_summary(results)
        return False
    
    # 2. Тест HTTP эндпоинтов
    print(f"\n2️⃣ HTTP ЭНДПОИНТЫ")
    base_url = f"http://{host}:{port}"
    
    # Тест /test эндпоинта
    test_url = f"{base_url}/test"
    http_test_result = await test_http_endpoint(test_url)
    results.append(("HTTP /test", http_test_result))
    
    # Тест /health эндпоинта
    health_url = f"{base_url}/health"
    http_health_result = await test_http_endpoint(health_url)
    results.append(("HTTP /health", http_health_result))
    
    # 3. Тест POST запроса (диалог)
    print(f"\n3️⃣ HTTP POST ТЕСТЫ")
    dialogue_url = f"{base_url}/dialogue"
    test_dialogue = {
        "npc_name": "Тестовый НПС",
        "player_message": "Привет, это тест!",
        "context": {"location": "test"}
    }
    
    dialogue_result = await test_http_post(dialogue_url, test_dialogue)
    results.append(("HTTP POST /dialogue", dialogue_result))
    
    # 4. Тест голосового эндпоинта
    voice_url = f"{base_url}/voice"
    test_voice = {
        "voice_text": "Тестовое голосовое сообщение"
    }
    
    voice_result = await test_http_post(voice_url, test_voice)
    results.append(("HTTP POST /voice", voice_result))
    
    # Сводка
    print_summary(results)
    
    # Возвращаем True если все основные тесты прошли
    critical_tests = [tcp_result, http_test_result]
    return all(critical_tests)

def print_summary(results):
    """Печать сводки результатов"""
    print(f"\n📊 СВОДКА РЕЗУЛЬТАТОВ")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print("=" * 50)
    print(f"🎯 ИТОГО: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Сервер работает корректно.")
    elif passed > 0:
        print("⚠️ ЧАСТИЧНО РАБОТАЕТ. Проверьте проваленные тесты.")
    else:
        print("💥 ПОЛНЫЙ ПРОВАЛ! Сервер не отвечает.")

async def main():
    """Главная функция"""
    try:
        success = await test_server()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n👋 Тестирование прервано пользователем")
        return 130
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        return 2

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n👋 Тестирование остановлено")
        sys.exit(130)
