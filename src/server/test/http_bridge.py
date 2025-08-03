#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import aiohttp
from aiohttp import web
import yaml
import logging
from pathlib import Path
import json
from datetime import datetime
import os
import socket
import struct
import uuid

def load_config():
    """Загрузка конфигурации из config.yml"""
    config_path = Path(__file__).parent.parent.parent.parent / 'config.yml'
    
    if not config_path.exists():
        config_path = Path.cwd() / 'config.yml'
        if not config_path.exists():
            config_path = Path(__file__).parent.parent.parent / 'config.yml'
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            logging.info(f"✅ Конфигурация загружена из {config_path}")
            return config
    except Exception as e:
        logging.error(f"❌ Ошибка загрузки конфигурации: {e}")
        return None

# Загружаем конфигурацию
config = load_config()

if config:
    HTTP_HOST = config.get("http_bridge", {}).get("host", "127.0.0.1")
    HTTP_PORT = config.get("http_bridge", {}).get("port", 8080)
    
    # AI-сервер работает через event bus на порту 9090!
    AI_HOST = config.get("event_bus", {}).get("host", "127.0.0.1") 
    AI_PORT = config.get("event_bus", {}).get("port", 9090)
    AI_BASE_URL = f"tcp://{AI_HOST}:{AI_PORT}"
else:
    HTTP_HOST = "127.0.0.1"
    HTTP_PORT = 8080
    AI_HOST = "127.0.0.1"
    AI_PORT = 9090  # Event bus порт!
    AI_BASE_URL = f"tcp://{AI_HOST}:{AI_PORT}"

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AIEventBusClient:
    """Клиент для подключения к AI-серверу через event bus"""
    
    def __init__(self, host="127.0.0.1", port=9090):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None
        self.connected = False
    
    async def connect(self):
        """Подключение к event bus"""
        try:
            logger.info(f"🔌 Подключаюсь к AI event bus {self.host}:{self.port}...")
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
            self.connected = True
            logger.info("✅ Подключение к AI event bus установлено")
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка подключения к event bus: {e}")
            self.connected = False
            return False
    
    async def disconnect(self):
        """Отключение от event bus"""
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
        self.connected = False
        logger.info("🔌 Отключен от AI event bus")
    
    async def send_message(self, message_type, data):
        """Отправка сообщения в event bus"""
        if not self.connected:
            if not await self.connect():
                return None
        
        try:
            # Формируем сообщение в формате event bus
            message = {
                "id": str(uuid.uuid4()),
                "type": message_type,
                "timestamp": datetime.now().isoformat(),
                "data": data
            }
            
            # Сериализуем в JSON
            json_data = json.dumps(message, ensure_ascii=False).encode('utf-8')
            
            # Отправляем длину сообщения + само сообщение
            length = struct.pack('!I', len(json_data))
            self.writer.write(length + json_data)
            await self.writer.drain()
            
            logger.info(f"📤 Отправлено сообщение типа '{message_type}' в event bus")
            
            # Читаем ответ
            response_length_data = await self.reader.read(4)
            if len(response_length_data) < 4:
                logger.error("❌ Неполный ответ от event bus")
                return None
            
            response_length = struct.unpack('!I', response_length_data)[0]
            response_data = await self.reader.read(response_length)
            
            if len(response_data) < response_length:
                logger.error("❌ Неполные данные ответа от event bus")
                return None
            
            response = json.loads(response_data.decode('utf-8'))
            logger.info(f"📥 Получен ответ от event bus: {response.get('type', 'unknown')}")
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Ошибка отправки сообщения в event bus: {e}")
            self.connected = False
            return None

# Создаем глобальный клиент event bus
ai_client = AIEventBusClient(AI_HOST, AI_PORT)

routes = web.RouteTableDef()

@routes.get("/health")
async def health(request):
    """Проверка здоровья HTTP моста"""
    # Проверяем подключение к event bus
    bus_status = "connected" if ai_client.connected else "disconnected"
    
    return web.json_response({
        "status": "healthy",
        "message": "HTTP мост работает!",
        "timestamp": datetime.now().isoformat(),
        "uptime": True,
        "config": {
            "host": HTTP_HOST,
            "port": HTTP_PORT,
            "ai_server": AI_BASE_URL,
            "event_bus_status": bus_status
        }
    })

@routes.get("/test")
async def test(request):
    """Тестовый эндпоинт"""
    logger.info("🧪 Тестовый запрос получен")
    
    # Тестируем подключение к event bus
    test_result = await ai_client.send_message("ping", {"test": True})
    bus_working = test_result is not None
    
    return web.json_response({
        "status": "success", 
        "message": "HTTP мост работает!",
        "timestamp": datetime.now().isoformat(),
        "client_info": {
            "remote": request.remote,
            "user_agent": request.headers.get("User-Agent"),
            "query_params": dict(request.query)
        },
        "server_info": {
            "host": HTTP_HOST,
            "port": HTTP_PORT,
            "pid": os.getpid(),
            "event_bus_working": bus_working
        }
    })

@routes.post("/dialogue")
async def dialogue(request):
    """Обработка диалогов с НПС через event bus"""
    try:
        payload = await request.json()
    except Exception as e:
        logger.error(f"❌ Ошибка декодирования JSON: {e}")
        return web.json_response(
            {"status": "error", "message": "Некорректный JSON"}, status=400
        )

    session_id = payload.get("session_id")
    text = payload.get("text")
    npc_name = payload.get("npc_name", "НПС")
    
    if not session_id or not text:
        return web.json_response(
            {"status": "error", "message": "Отсутствуют session_id или text"}, status=400
        )

    logger.info(f"🗣️ Диалог: {npc_name} <- {text}")

    # Отправляем запрос через event bus
    try:
        response = await ai_client.send_message("dialogue", {
            "session_id": session_id,
            "text": text,
            "npc_name": npc_name,
            "context": "morrowind_dialogue",
            "language": "ru"
        })
        
        if response and response.get("status") == "success":
            ai_response = response.get("data", {}).get("response", "НПС задумался...")
            logger.info("✅ Получен ответ от AI через event bus")
        else:
            logger.warning("⚠️ Event bus вернул ошибку или пустой ответ")
            ai_response = f"Извини, {npc_name} сейчас думает о твоих словах '{text}'."
            
    except Exception as e:
        logger.error(f"❌ Ошибка общения с AI через event bus: {e}")
        ai_response = f"Извини, {npc_name} сейчас не может ответить. Попробуй позже."

    response_data = {
        "status": "success",
        "ai_response": ai_response,
        "npc_name": npc_name,
        "timestamp": datetime.now().isoformat(),
        "method": "event_bus"
    }
    
    logger.info(f"📤 Ответ: {ai_response[:50]}...")
    return web.json_response(response_data)

@routes.post("/voice")
async def voice(request):
    """Обработка голосового ввода через event bus"""
    try:
        if request.content_type == 'application/json':
            payload = await request.json()
            text = payload.get("text", "")
            logger.info(f"🎤 Голос (JSON): {text}")
            
            # Отправляем через event bus для обработки
            response = await ai_client.send_message("voice", {
                "text": text,
                "format": "json",
                "language": "ru"
            })
            
            return web.json_response({
                "status": "success",
                "recognized_text": text,
                "method": "event_bus_json",
                "ai_processed": response is not None
            })
            
        elif request.content_type.startswith('audio/'):
            audio_data = await request.read()
            logger.info(f"🎤 Голос (аудио): {len(audio_data)} байт")
            
            # Отправляем аудио через event bus
            response = await ai_client.send_message("voice_audio", {
                "audio_data": audio_data.hex(),  # Кодируем в hex
                "format": "binary",
                "language": "ru"
            })
            
            recognized_text = "Распознавание через event bus..."
            if response and response.get("data"):
                recognized_text = response["data"].get("text", recognized_text)
            
            return web.json_response({
                "status": "success", 
                "recognized_text": recognized_text,
                "method": "event_bus_audio",
                "size": len(audio_data)
            })
        else:
            return web.json_response(
                {"status": "error", "message": "Неподдерживаемый тип контента"}, 
                status=400
            )
            
    except Exception as e:
        logger.error(f"❌ Ошибка обработки голоса: {e}")
        return web.json_response(
            {"status": "error", "message": str(e)}, status=500
        )

@routes.post("/generate")
async def generate(request):
    """Прямая генерация через AI для совместимости"""
    try:
        payload = await request.json()
        prompt = payload.get("prompt", payload.get("text", ""))
        
        if not prompt:
            return web.json_response(
                {"status": "error", "message": "Отсутствует prompt или text"}, status=400
            )
        
        logger.info(f"🤖 Генерация: {prompt[:50]}...")
        
        response = await ai_client.send_message("generate", {
            "prompt": prompt,
            "max_tokens": payload.get("max_tokens", 150),
            "temperature": payload.get("temperature", 0.7),
            "language": "ru"
        })
        
        if response and response.get("status") == "success":
            generated_text = response.get("data", {}).get("text", "Генерация не удалась...")
        else:
            generated_text = f"Ответ на '{prompt[:30]}...' обрабатывается..."
        
        return web.json_response({
            "status": "success",
            "generated_text": generated_text,
            "method": "event_bus",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Ошибка генерации: {e}")
        return web.json_response(
            {"status": "error", "message": str(e)}, status=500
        )

async def cleanup_on_shutdown(app):
    """Очистка при завершении работы"""
    logger.info("🧹 Очистка ресурсов...")
    await ai_client.disconnect()

def main():
    """Главная функция запуска HTTP моста"""
    logger.info("🌉 Запуск OpenMW-AI HTTP моста...")
    
    if config:
        logger.info(f"✅ Конфигурация загружена из config.yml")
    else:
        logger.warning("⚠️ Используются значения по умолчанию")
    
    logger.info("🌉 Инициализация HTTP моста")
    logger.info(f"📡 AI event bus: {AI_BASE_URL}")
    logger.info(f"🔌 HTTP сервер: {HTTP_HOST}:{HTTP_PORT}")
    
    # Создаем приложение
    app = web.Application()
    app.add_routes(routes)
    
    # Добавляем обработчик очистки
    app.on_cleanup.append(cleanup_on_shutdown)
    
    logger.info("✅ HTTP мост готов к работе!")
    logger.info(f"🎮 Тест: http://{HTTP_HOST}:{HTTP_PORT}/test")
    logger.info(f"❤️ Здоровье: http://{HTTP_HOST}:{HTTP_PORT}/health")
    logger.info(f"📞 Диалоги: POST http://{HTTP_HOST}:{HTTP_PORT}/dialogue")
    logger.info(f"🎤 Голос: POST http://{HTTP_HOST}:{HTTP_PORT}/voice")
    logger.info(f"🤖 Генерация: POST http://{HTTP_HOST}:{HTTP_PORT}/generate")
    
    # Запускаем сервер на правильном порту 8080!
    web.run_app(app, host=HTTP_HOST, port=HTTP_PORT)

if __name__ == "__main__":
    main()
