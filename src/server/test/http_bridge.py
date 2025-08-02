#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import json
import signal
from aiohttp import web, ClientSession
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class OpenMWBridge:
    def __init__(self):
        self.ai_server_url = "http://127.0.0.1:18080"
        
    async def handle_dialogue(self, request):
        """Обработка диалогов от OpenMW"""
        try:
            data = await request.json()
            
            # Получаем данные от OpenMW
            npc_name = data.get('npc_name', 'Unknown NPC')
            player_message = data.get('player_message', '')
            
            logger.info(f"🗣️ Диалог: {npc_name} <- {player_message}")
            
            # Генерируем ИИ ответ (пока заглушка)
            ai_response = self.generate_ai_response(npc_name, player_message)
            
            # Возвращаем ответ в OpenMW
            return web.json_response({
                'status': 'success',
                'ai_response': ai_response,
                'npc_name': npc_name
            })
            
        except Exception as e:
            logger.error(f"❌ Ошибка обработки диалога: {e}")
            return web.json_response({
                'status': 'error',
                'message': str(e)
            })

    def generate_ai_response(self, npc_name, player_message):
        """Генерация ответа НПС"""
        responses = [
            f"Приветствую, путник! Ты сказал: '{player_message}'. Что тебя интересует?",
            f"Здравствуй! Я {npc_name}. Твои слова '{player_message}' звучат интересно.",
            f"Добро пожаловать! Ты упомянул '{player_message}' - расскажи подробнее.",
            f"Хм, '{player_message}'... Интересная тема для разговора, друг.",
        ]
        
        # Простая логика выбора ответа
        import random
        return random.choice(responses)

    async def handle_voice(self, request):
        """Обработка голосового ввода"""
        try:
            data = await request.json()
            voice_text = data.get('voice_text', '')
            
            logger.info(f"🎤 Голос распознан: {voice_text}")
            
            return web.json_response({
                'status': 'success',
                'recognized_text': voice_text
            })
            
        except Exception as e:
            return web.json_response({
                'status': 'error', 
                'message': str(e)
            })

    async def handle_test(self, request):
        """Тестовый эндпоинт"""
        logger.info("🧪 Тестовый запрос получен")
        return web.json_response({
            'status': 'success',
            'message': 'HTTP мост работает!',
            'timestamp': asyncio.get_event_loop().time()
        })

async def create_app():
    bridge = OpenMWBridge()
    
    app = web.Application()
    app.router.add_post('/dialogue', bridge.handle_dialogue)
    app.router.add_post('/voice', bridge.handle_voice)
    app.router.add_get('/test', bridge.handle_test)
    
    return app

def signal_handler(signum, frame):
    logger.info("🛑 Получен сигнал остановки")
    exit(0)

async def main():
    # Обработка сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("🌉 Запуск OpenMW-AI HTTP моста...")
    logger.info("🔗 HTTP сервер на порту 8080")
    
    app = await create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, '127.0.0.1', 8080)
    await site.start()
    
    logger.info("✅ HTTP мост готов к работе!")
    logger.info("🎮 Тестируй: http://127.0.0.1:8080/test")
    logger.info("📞 Диалоги: POST http://127.0.0.1:8080/dialogue")
    
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.info("👋 Корректная остановка HTTP моста...")
    finally:
        await runner.cleanup()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 HTTP мост остановлен")
