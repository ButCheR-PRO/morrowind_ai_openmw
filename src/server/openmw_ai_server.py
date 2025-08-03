#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import aiohttp
from aiohttp import web
import json
import logging
from datetime import datetime
import google.generativeai as genai
import yaml

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

class OpenMWAIServer:
    def __init__(self, config_path="../../config.yml"):
        self.config = self.load_config(config_path)
        self.setup_gemini()
        
    def load_config(self, config_path):
        """Загрузка конфигурации"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            logger.info(f"✅ Конфигурация загружена: {config_path}")
            return config
        except Exception as e:
            logger.error(f"❌ Ошибка загрузки конфига: {e}")
            return {}
    
    def setup_gemini(self):
        """Настройка Google Gemini"""
        try:
            api_key = self.config.get('llm', {}).get('system', {}).get('google', {}).get('api_key')
            if not api_key:
                raise ValueError("Google API ключ не найден в конфиге")
                
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("✅ Google Gemini настроен и готов")
        except Exception as e:
            logger.error(f"❌ Ошибка настройки Gemini: {e}")
            self.model = None

    async def generate_ai_response(self, user_text, npc_name="НПС"):
        """Генерация ответа через Gemini AI"""
        if not self.model:
            return "Извини, ИИ временно недоступен"
        
        try:
            prompt = f"""
Ты - {npc_name} из игры Morrowind. 
Игрок сказал: "{user_text}"
Ответь как этот персонаж, кратко и по теме.
Используй русский язык и стиль фэнтези.
"""
            
            response = await asyncio.get_event_loop().run_in_executor(
                None, self.model.generate_content, prompt
            )
            
            ai_response = response.text.strip()
            logger.info(f"🤖 Gemini ответил: {ai_response[:100]}...")
            return ai_response
            
        except Exception as e:
            logger.error(f"❌ Ошибка Gemini: {e}")
            return f"*{npc_name} задумчиво молчит*"

    async def handle_root(self, request):
        """Главная страница"""
        return web.Response(text="""
🤖 OpenMW AI Server v1.0
========================
Статус: Работает
Gemini AI: Готов
Время: %s

Доступные эндпоинты:
- GET  /api/status
- POST /api/dialogue
""" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    async def handle_status(self, request):
        """Статус системы"""
        status = {
            "status": "ready",
            "server": "OpenMW AI Server v1.0",
            "gemini_available": self.model is not None,
            "timestamp": datetime.now().isoformat(),
            "endpoints": ["/api/status", "/api/dialogue"]
        }
        return web.json_response(status)

    async def handle_dialogue(self, request):
        """Обработка диалогов"""
        try:
            data = await request.json()
            user_text = data.get('text', '').strip()
            npc_name = data.get('npc_name', 'Неизвестный НПС')
            session_id = data.get('session_id', 'default')
            
            if not user_text:
                return web.json_response(
                    {"error": "Пустое сообщение"}, 
                    status=400
                )
            
            logger.info(f"📤 Запрос от {session_id}: {user_text}")
            
            # Генерируем ответ через Gemini
            ai_response = await self.generate_ai_response(user_text, npc_name)
            
            result = {
                "status": "success",
                "ai_response": ai_response,
                "npc_name": npc_name,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"📥 Ответ для {session_id}: {ai_response[:50]}...")
            return web.json_response(result)
            
        except Exception as e:
            logger.error(f"❌ Ошибка обработки диалога: {e}")
            return web.json_response(
                {"error": f"Ошибка сервера: {str(e)}"}, 
                status=500
            )

    async def start_server(self, host='127.0.0.1', port=8080):
        """Запуск HTTP сервера"""
        app = web.Application()
        
        # Регистрируем маршруты
        app.router.add_get('/', self.handle_root)
        app.router.add_get('/api/status', self.handle_status)
        app.router.add_post('/api/dialogue', self.handle_dialogue)
        
        logger.info("🚀 Запускаю OpenMW AI Server...")
        logger.info(f"🌐 HTTP сервер: http://{host}:{port}")
        logger.info(f"🔗 Статус: http://{host}:{port}/api/status")
        
        # Запускаем сервер
        runner = web.AppRunner(app)
        await runner.setup()
        
        site = web.TCPSite(runner, host, port)
        await site.start()
        
        logger.info("✅ OpenMW AI Server готов к работе!")
        
        # Держим сервер запущенным
        try:
            while True:
                await asyncio.sleep(3600)  # Спим час
        except KeyboardInterrupt:
            logger.info("👋 Останавливаю сервер...")
        finally:
            await runner.cleanup()

def main():
    try:
        server = OpenMWAIServer()
        asyncio.run(server.start_server())
    except Exception as e:
        logger.error(f"💀 Критическая ошибка: {e}")

if __name__ == "__main__":
    main()
