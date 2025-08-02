#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import json
import signal
import sys
import yaml
import logging
import os
from pathlib import Path
from aiohttp import web, ClientSession
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('http_bridge.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class OpenMWBridge:
    def __init__(self, config=None):
        self.config = config or {}
        self.ai_server_url = self.config.get('ai_server_url', "http://127.0.0.1:18080")
        self.running = False
        
        # Настройки из конфига
        self.rpc_config = self.config.get('rpc', {})
        self.host = self.rpc_config.get('host', '127.0.0.1')
        self.port = self.rpc_config.get('port', 8080)
        
        logger.info(f"🌉 Инициализация HTTP моста")
        logger.info(f"📡 Сервер ИИ: {self.ai_server_url}")
        logger.info(f"🔌 HTTP сервер: {self.host}:{self.port}")
    
    async def handle_dialogue(self, request):
        """Обработка диалогов от OpenMW"""
        try:
            data = await request.json()
            
            # Получаем данные от OpenMW
            npc_name = data.get('npc_name', 'Unknown NPC')
            player_message = data.get('player_message', '')
            context = data.get('context', {})
            
            logger.info(f"🗣️ Диалог: {npc_name} <- {player_message}")
            
            # Генерируем ИИ ответ
            ai_response = await self.generate_ai_response(npc_name, player_message, context)
            
            # Возвращаем ответ в OpenMW
            response_data = {
                'status': 'success',
                'ai_response': ai_response,
                'npc_name': npc_name,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"📤 Ответ: {ai_response[:100]}...")
            return web.json_response(response_data)
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Ошибка декодирования JSON: {e}")
            return web.json_response({
                'status': 'error',
                'message': 'Некорректный JSON'
            }, status=400)
        except Exception as e:
            logger.error(f"❌ Ошибка обработки диалога: {e}")
            return web.json_response({
                'status': 'error',
                'message': str(e)
            }, status=500)

    async def generate_ai_response(self, npc_name, player_message, context=None):
        """Генерация ответа НПС через ИИ сервер"""
        try:
            # Пытаемся подключиться к серверу ИИ
            async with ClientSession() as session:
                payload = {
                    'npc_name': npc_name,
                    'player_message': player_message,
                    'context': context or {},
                    'language': self.config.get('language', 'ru')
                }
                
                async with session.post(
                    f"{self.ai_server_url}/generate",
                    json=payload,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('response', 'Извините, не могу ответить.')
                    else:
                        logger.warning(f"⚠️ Сервер ИИ вернул статус {response.status}")
                        return self.get_fallback_response(npc_name, player_message)
                        
        except asyncio.TimeoutError:
            logger.warning("⏰ Таймаут запроса к серверу ИИ")
            return self.get_fallback_response(npc_name, player_message)
        except Exception as e:
            logger.warning(f"⚠️ Ошибка подключения к ИИ серверу: {e}")
            return self.get_fallback_response(npc_name, player_message)

    def get_fallback_response(self, npc_name, player_message):
        """Резервные ответы когда ИИ недоступен"""
        responses = [
            f"Приветствую, путник! Ты сказал: '{player_message}'. Что тебя интересует?",
            f"Здравствуй! Я {npc_name}. Твои слова '{player_message}' звучат интересно.",
            f"Добро пожаловать! Ты упомянул '{player_message}' - расскажи подробнее.",
            f"Хм, '{player_message}'... Интересная тема для разговора, друг.",
            f"Извини, {npc_name} сейчас думает о твоих словах '{player_message}'.",
        ]
        
        # Простая логика выбора ответа
        import random
        return random.choice(responses)

    async def handle_voice(self, request):
        """Обработка голосового ввода"""
        try:
            # Проверяем Content-Type
            content_type = request.headers.get('Content-Type', '')
            
            if content_type.startswith('application/json'):
                data = await request.json()
                voice_text = data.get('voice_text', '')
                logger.info(f"🎤 Голос (JSON): {voice_text}")
                
                return web.json_response({
                    'status': 'success',
                    'recognized_text': voice_text,
                    'method': 'json'
                })
                
            elif content_type.startswith('audio/'):
                # Обработка аудио данных
                audio_data = await request.read()
                logger.info(f"🎤 Получены аудио данные: {len(audio_data)} байт")
                
                # Здесь должна быть интеграция с VOSK
                recognized_text = await self.process_audio_with_vosk(audio_data)
                
                return web.json_response({
                    'status': 'success',
                    'recognized_text': recognized_text,
                    'method': 'audio',
                    'audio_size': len(audio_data)
                })
            else:
                return web.json_response({
                    'status': 'error',
                    'message': f'Неподдерживаемый Content-Type: {content_type}'
                }, status=400)
                
        except Exception as e:
            logger.error(f"❌ Ошибка обработки голоса: {e}")
            return web.json_response({
                'status': 'error', 
                'message': str(e)
            }, status=500)

    async def process_audio_with_vosk(self, audio_data):
        """Обработка аудио с помощью VOSK"""
        try:
            # Заглушка для VOSK интеграции
            # Здесь должен быть реальный код распознавания
            logger.info("🤖 Обработка аудио через VOSK...")
            
            # Имитация распознавания
            await asyncio.sleep(0.1)
            return "Распознанный текст из аудио"
            
        except Exception as e:
            logger.error(f"❌ Ошибка VOSK: {e}")
            return "Ошибка распознавания речи"

    async def handle_health(self, request):
        """Проверка здоровья сервера"""
        return web.json_response({
            'status': 'healthy',
            'message': 'HTTP мост работает!',
            'timestamp': datetime.now().isoformat(),
            'uptime': self.running,
            'config': {
                'host': self.host,
                'port': self.port,
                'ai_server': self.ai_server_url
            }
        })

    async def handle_test(self, request):
        """Тестовый эндпоинт"""
        logger.info("🧪 Тестовый запрос получен")
        
        # Получаем параметры запроса
        query_params = dict(request.query)
        headers = dict(request.headers)
        
        return web.json_response({
            'status': 'success',
            'message': 'HTTP мост работает!',
            'timestamp': datetime.now().isoformat(),
            'client_info': {
                'remote': request.remote,
                'user_agent': headers.get('User-Agent', 'Unknown'),
                'query_params': query_params
            },
            'server_info': {
                'host': self.host,
                'port': self.port,
                'pid': os.getpid()
            }
        })

def load_config():
    """Загрузка конфигурации из config.yml"""
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

async def create_app():
    """Создание веб-приложения"""
    config = load_config()
    bridge = OpenMWBridge(config)
    
    app = web.Application()
    
    # Маршруты
    app.router.add_post('/dialogue', bridge.handle_dialogue)
    app.router.add_post('/voice', bridge.handle_voice)
    app.router.add_get('/test', bridge.handle_test)
    app.router.add_get('/health', bridge.handle_health)
    
    # CORS middleware
    @web.middleware
    async def cors_handler(request, handler):
        response = await handler(request)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    
    app.middlewares.append(cors_handler)
    
    return app, bridge

def setup_signal_handlers(bridge):
    """Настройка обработчиков сигналов"""
    def signal_handler(signum, frame):
        logger.info(f"🛑 Получен сигнал {signum}")
        bridge.running = False
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

async def main():
    """Главная функция"""
    logger.info("🌉 Запуск OpenMW-AI HTTP моста...")
    
    try:
        app, bridge = await create_app()
        setup_signal_handlers(bridge)
        
        runner = web.AppRunner(app)
        await runner.setup()
        
        site = web.TCPSite(runner, bridge.host, bridge.port)
        await site.start()
        
        bridge.running = True
        
        logger.info("✅ HTTP мост готов к работе!")
        logger.info(f"🎮 Тест: http://{bridge.host}:{bridge.port}/test")
        logger.info(f"❤️ Здоровье: http://{bridge.host}:{bridge.port}/health")
        logger.info(f"📞 Диалоги: POST http://{bridge.host}:{bridge.port}/dialogue")
        logger.info(f"🎤 Голос: POST http://{bridge.host}:{bridge.port}/voice")
        
        try:
            while bridge.running:
                await asyncio.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            logger.info("👋 Получен сигнал остановки...")
        finally:
            logger.info("🛑 Остановка HTTP моста...")
            await runner.cleanup()
            
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n👋 HTTP мост остановлен")
        sys.exit(0)
