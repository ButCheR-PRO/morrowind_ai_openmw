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
    
    # AI-сервер работает через event bus
    AI_HOST = config.get("event_bus", {}).get("host", "127.0.0.1") 
    AI_PORT = config.get("event_bus", {}).get("port", 9090)
    AI_BASE_URL = f"tcp://{AI_HOST}:{AI_PORT}"
else:
    HTTP_HOST = "127.0.0.1"
    HTTP_PORT = 8080
    AI_HOST = "127.0.0.1"
    AI_PORT = 9090
    AI_BASE_URL = f"tcp://{AI_HOST}:{AI_PORT}"

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AIEventBusClient:
    """Клиент для подключения к AI-серверу через event bus (правильный формат)"""
    
    def __init__(self, host="127.0.0.1", port=9090):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None
        self.connected = False
        self.event_id = 1  # Счётчик событий
    
    async def connect(self):
        """Подключение к event bus"""
        try:
            logger.info(f"🔌 Подключаюсь к AI event bus {self.host}:{self.port}...")
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
            self.connected = True
            logger.info("✅ Подключение к AI event bus установлено")
            
            # Отправляем первоначальное событие как OpenMW клиент
            await self.send_init_event()
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка подключения к event bus: {e}")
            self.connected = False
            return False
    
    async def send_init_event(self):
        """Отправка инициализационного события как OpenMW клиент"""
        try:
            init_event = {
                "event_id": self.event_id,
                "response_to_event_id": None,
                "data": {
                    "type": "client_init",  # Правильный тип для инициализации
                    "client_info": {
                        "name": "HTTP_Bridge_Client",
                        "version": "1.0.0",
                        "platform": "HTTP"
                    }
                }
            }
            
            await self._send_raw_message(init_event)
            self.event_id += 1
            logger.info("📤 Отправлено инициализационное событие")
            
        except Exception as e:
            logger.error(f"❌ Ошибка отправки инициализации: {e}")
    
    async def disconnect(self):
        """Отключение от event bus"""
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
        self.connected = False
        logger.info("🔌 Отключен от AI event bus")
    
    async def _send_raw_message(self, message):
        """Отправка сырого сообщения в правильном формате"""
        if not self.connected:
            raise Exception("Не подключен к event bus")
        
        # Сериализуем в JSON с правильной кодировкой
        json_data = json.dumps(message, ensure_ascii=False).encode('utf-8')
        
        # Добавляем разделитель строк как ожидает сервер
        data_with_newline = json_data + b'\n'
        
        # Отправляем
        self.writer.write(data_with_newline)
        await self.writer.drain()
    
    async def send_dialogue_request(self, session_id, text, npc_name="НПС"):
        """Отправка запроса диалога в правильном формате для AI-сервера"""
        if not self.connected:
            if not await self.connect():
                return None
        
        try:
            # Формируем событие в формате который ожидает AI-сервер
            dialogue_event = {
                "event_id": self.event_id,
                "response_to_event_id": None,
                "data": {
                    "type": "npc_dialogue_request",  # Правильный тип события
                    "session_id": session_id,
                    "player_message": text,
                    "npc_name": npc_name,
                    "context": {
                        "location": "unknown",
                        "mood": "neutral",
                        "language": "ru"
                    }
                }
            }
            
            await self._send_raw_message(dialogue_event)
            self.event_id += 1
            
            logger.info(f"📤 Отправлен запрос диалога (event_id: {dialogue_event['event_id']})")
            
            # Ждём ответ с таймаутом
            try:
                response = await asyncio.wait_for(self._read_response(), timeout=10.0)
                logger.info(f"📥 Получен ответ от AI: {response.get('data', {}).get('type', 'unknown')}")
                return response
            except asyncio.TimeoutError:
                logger.warning("⏰ Таймаут ожидания ответа от AI")
                return None
                
        except Exception as e:
            logger.error(f"❌ Ошибка отправки диалога: {e}")
            self.connected = False
            return None
    
    async def _read_response(self):
        """Чтение ответа от AI-сервера"""
        try:
            # Читаем строку до переноса
            response_line = await self.reader.readline()
            
            if not response_line:
                logger.error("❌ Пустой ответ от event bus")
                return None
            
            # Декодируем JSON
            response_text = response_line.decode('utf-8').strip()
            response = json.loads(response_text)
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Ошибка чтения ответа: {e}")
            return None

# Создаем глобальный клиент event bus
ai_client = AIEventBusClient(AI_HOST, AI_PORT)

routes = web.RouteTableDef()

@routes.get("/health")
async def health(request):
    """Проверка здоровья HTTP моста"""
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
    """Тестовый эндпоинт с проверкой event bus"""
    logger.info("🧪 Тестовый запрос получен")
    
    # Проверяем подключение к event bus
    if not ai_client.connected:
        bus_working = await ai_client.connect()
    else:
        bus_working = True
    
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
    """Обработка диалогов с НПС через event bus (исправленный формат)"""
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

    # Отправляем запрос через event bus в правильном формате
    try:
        response = await ai_client.send_dialogue_request(session_id, text, npc_name)
        
        if response and response.get("data"):
            response_data = response["data"]
            
            # Извлекаем ответ в зависимости от типа события
            if response_data.get("type") == "npc_dialogue_response":
                ai_response = response_data.get("npc_message", "НПС задумался...")
                logger.info("✅ Получен ответ от AI через event bus")
            else:
                ai_response = f"Извини, {npc_name} сейчас думает о твоих словах '{text}'."
                logger.warning(f"⚠️ Неожиданный тип ответа: {response_data.get('type')}")
        else:
            logger.warning("⚠️ Event bus вернул пустой или неправильный ответ")
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
    """Обработка голосового ввода"""
    try:
        if request.content_type == 'application/json':
            payload = await request.json()
            text = payload.get("text", "")
            logger.info(f"🎤 Голос (JSON): {text}")
            
            return web.json_response({
                "status": "success",
                "recognized_text": text,
                "method": "json"
            })
            
        elif request.content_type.startswith('audio/'):
            audio_data = await request.read()
            logger.info(f"🎤 Голос (аудио): {len(audio_data)} байт")
            
            return web.json_response({
                "status": "success", 
                "recognized_text": "Распознавание аудио через VOSK не настроено",
                "method": "audio",
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
    
    # Запускаем сервер
    web.run_app(app, host=HTTP_HOST, port=HTTP_PORT)

if __name__ == "__main__":
    main()
