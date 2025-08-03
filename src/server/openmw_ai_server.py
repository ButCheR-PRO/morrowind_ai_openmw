#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import aiohttp
from aiohttp import web
import json
import logging
from datetime import datetime
import yaml
import os
import google.generativeai as genai
import traceback

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

class OpenMWAIServer:
    def __init__(self, config_path=None):
        # Автоматически определяем путь к config.yml
        if config_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            config_path = os.path.join(project_root, "config.yml")

        self.config = self.load_config(config_path)
        self.setup_gemini()

    def load_config(self, config_path):
        """Загрузка конфигурации с детальной диагностикой"""
        try:
            abs_path = os.path.abspath(config_path)
            logger.info(f"[CONFIG] Абсолютный путь к config: {abs_path}")

            if not os.path.exists(abs_path):
                logger.error(f"[CONFIG] Файл config.yml НЕ НАЙДЕН: {abs_path}")
                return {}

            logger.info(f"[CONFIG] Файл config.yml найден")

            # Читаем содержимое файла
            with open(abs_path, 'r', encoding='utf-8') as f:
                content = f.read()

            logger.info(f"[CONFIG] Размер файла: {len(content)} символов")
            logger.info(f"[CONFIG] Первые 100 символов: {content[:100]}")

            # Парсим YAML
            config = yaml.safe_load(content)
            logger.info(f"[CONFIG] Успешно распарсен YAML")

            # ДЕТАЛЬНАЯ ДИАГНОСТИКА СТРУКТУРЫ
            logger.info(f"[CONFIG] Корневые ключи config: {list(config.keys()) if config else 'Пустой config'}")

            if 'llm' in config:
                logger.info(f"[CONFIG] Секция llm найдена: {list(config['llm'].keys())}")

                if 'system' in config['llm']:
                    logger.info(f"[CONFIG] Секция system найдена: {list(config['llm']['system'].keys())}")

                    if 'google' in config['llm']['system']:
                        google_config = config['llm']['system']['google']
                        logger.info(f"[CONFIG] Секция google найдена: {list(google_config.keys())}")

                        api_key = google_config.get('api_key')
                        if api_key:
                            logger.info(f"[CONFIG] API ключ НАЙДЕН!")
                            logger.info(f"[CONFIG] Длина ключа: {len(api_key)} символов")
                            logger.info(f"[CONFIG] Начинается с: {api_key[:10]}...")
                            logger.info(f"[CONFIG] Заканчивается на: ...{api_key[-10:]}")
                        else:
                            logger.error(f"[CONFIG] API ключ ОТСУТСТВУЕТ в секции google!")
                    else:
                        logger.error(f"[CONFIG] Секция google ОТСУТСТВУЕТ!")
                else:
                    logger.error(f"[CONFIG] Секция system ОТСУТСТВУЕТ!")
            else:
                logger.error(f"[CONFIG] Секция llm ОТСУТСТВУЕТ!")

            return config

        except Exception as e:
            logger.error(f"[CONFIG] Ошибка загрузки конфига: {e}")
            logger.error(f"[CONFIG] Полная ошибка: {traceback.format_exc()}")
            return {}

    def setup_gemini(self):
        """Настройка Google Gemini с детальной диагностикой"""
        try:
            api_key = self.config.get('llm', {}).get('system', {}).get('google', {}).get('api_key')

            if not api_key:
                logger.error("[GEMINI] API ключ пустой или отсутствует")
                self.model = None
                return

            logger.info(f"[GEMINI] Настраиваю Gemini с ключом длиной {len(api_key)} символов")

            # Проверяем формат ключа
            if not api_key.startswith('AIza'):
                logger.warning(f"[GEMINI] API ключ не начинается с 'AIza' - возможно неверный формат")

            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')

            # ТЕСТИРУЕМ ПОДКЛЮЧЕНИЕ К GEMINI
            logger.info("[GEMINI] Тестирую подключение к Gemini...")
            test_response = self.model.generate_content("Скажи просто 'тест'")

            if test_response and test_response.text:
                logger.info(f"[GEMINI] Gemini работает! Тестовый ответ: {test_response.text.strip()}")
                logger.info("[GEMINI] Google Gemini настроен и ПРОТЕСТИРОВАН!")
            else:
                logger.error("[GEMINI] Gemini не ответил на тестовый запрос")

        except Exception as e:
            logger.error(f"[GEMINI] Ошибка настройки Gemini: {e}")
            logger.error(f"[GEMINI] Полная ошибка: {traceback.format_exc()}")
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
            logger.info(f"[AI] Gemini ответил: {ai_response[:100]}...")
            return ai_response

        except Exception as e:
            logger.error(f"[AI] Ошибка Gemini: {e}")
            return f"*{npc_name} задумчиво молчит*"

    async def handle_root(self, request):
        """Главная страница"""
        return web.Response(text=f"""
OpenMW AI Server v1.0
========================
Статус: Работает
Gemini AI: {'Готов' if self.model else 'Недоступен'}
Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Доступные эндпоинты:
- GET  /api/status
- POST /api/dialogue
""")

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

            logger.info(f"[REQUEST] Запрос от {session_id}: {user_text}")

            # Генерируем ответ через Gemini
            ai_response = await self.generate_ai_response(user_text, npc_name)

            result = {
                "status": "success",
                "ai_response": ai_response,
                "npc_name": npc_name,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            }

            logger.info(f"[RESPONSE] Ответ для {session_id}: {ai_response[:50]}...")
            return web.json_response(result)

        except Exception as e:
            logger.error(f"[ERROR] Ошибка обработки диалога: {e}")
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

        logger.info("[SERVER] Запускаю OpenMW AI Server...")
        logger.info(f"[SERVER] HTTP сервер: http://{host}:{port}")
        logger.info(f"[SERVER] Статус: http://{host}:{port}/api/status")

        # Запускаем сервер
        runner = web.AppRunner(app)
        await runner.setup()

        site = web.TCPSite(runner, host, port)
        await site.start()

        logger.info("[SERVER] OpenMW AI Server готов к работе!")

        # Держим сервер запущенным
        try:
            while True:
                await asyncio.sleep(3600)  # Спим час
        except KeyboardInterrupt:
            logger.info("[SERVER] Останавливаю сервер...")
        finally:
            await runner.cleanup()

def main():
    try:
        server = OpenMWAIServer()
        asyncio.run(server.start_server())
    except Exception as e:
        logger.error(f"[FATAL] Критическая ошибка: {e}")

if __name__ == "__main__":
    main()
