#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
Morrowind AI HTTP Bridge v1.2
Мост между OpenMW (файлы) и AI-сервером (HTTP/WebSocket)
============================================================================
"""

import os
import sys
import json
import time
import asyncio
import aiohttp
from threading import Thread
from pathlib import Path
import logging
from datetime import datetime

# ИСПРАВЛЯЕМ ПРОБЛЕМУ С ЛОГАМИ - правильные пути
def ensure_log_directory():
    # Идём в корень проекта и создаём logs
    current_dir = Path(__file__).parent  # test/
    server_dir = current_dir.parent      # server/
    src_dir = server_dir.parent          # src/
    root_dir = src_dir.parent            # morrowind_ai_openmw/
    log_dir = root_dir / 'logs'
    
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir

# Создаём папку логов перед настройкой логирования
log_directory = ensure_log_directory()

# Настройка логирования с правильными путями
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_directory / 'http_bridge.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class MorrowindAIBridge:
    def __init__(self):
        self.config = {
            'ai_server_host': 'localhost',
            'ai_server_port': 9090,
            'http_server_port': 8080,
            # Пути к твоей игре
            'temp_dir': 'f:/Games/MorrowindFullrest/game/Data Files/ai_temp/',
            'request_file': 'f:/Games/MorrowindFullrest/game/Data Files/ai_temp/ai_request.json',
            'response_file': 'f:/Games/MorrowindFullrest/game/Data Files/ai_temp/ai_response.json',
            'signal_file': 'f:/Games/MorrowindFullrest/game/Data Files/ai_temp/ai_signal.txt',
            'check_interval': 0.5,
            'request_timeout': 30,
        }
        
        self.is_running = False
        self.processed_requests = set()
        
        # Создаем временную директорию
        self.ensure_temp_directory()
        
    def ensure_temp_directory(self):
        """Создает временную директорию если её нет"""
        temp_path = Path(self.config['temp_dir'])
        temp_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Временная директория готова: {temp_path.absolute()}")
        
    def start(self):
        """Запуск моста"""
        logger.info("=" * 60)
        logger.info("🌉 MORROWIND AI BRIDGE ЗАПУСКАЕТСЯ...")
        logger.info(f"📁 Логи сохраняются в: {log_directory}")
        logger.info("=" * 60)
        
        self.is_running = True
        
        # Запускаем файловый мониторинг в отдельном потоке
        monitor_thread = Thread(target=self.file_monitor_loop, daemon=True)
        monitor_thread.start()
        
        # Запускаем HTTP сервер
        try:
            asyncio.run(self.start_http_server())
        except KeyboardInterrupt:
            logger.info("Получен сигнал остановки...")
            self.stop()
        except Exception as e:
            logger.error(f"Критическая ошибка: {e}")
            self.stop()
            
    def stop(self):
        """Остановка моста"""
        self.is_running = False
        logger.info("🛑 Morrowind AI Bridge остановлен")
        
    def file_monitor_loop(self):
        """Основной цикл мониторинга файлов от OpenMW"""
        logger.info("👁️ Запущен мониторинг файлов от OpenMW...")
        logger.info(f"📂 Отслеживаем: {self.config['temp_dir']}")
        
        while self.is_running:
            try:
                self.check_for_new_requests()
                time.sleep(self.config['check_interval'])
            except Exception as e:
                logger.error(f"Ошибка в мониторинге файлов: {e}")
                time.sleep(1)
                
    def check_for_new_requests(self):
        """Проверяет новые запросы от OpenMW"""
        signal_file = self.config['signal_file']
        request_file = self.config['request_file']
        
        # Проверяем наличие сигнального файла
        if not os.path.exists(signal_file):
            return
            
        try:
            # Читаем сигнальный файл
            with open(signal_file, 'r', encoding='utf-8') as f:
                signal_content = f.read().strip()
                
            # Проверяем что это новый запрос
            if signal_content in self.processed_requests:
                return
                
            # Читаем файл запроса
            if not os.path.exists(request_file):
                logger.warning("Сигнальный файл есть, но файл запроса отсутствует")
                os.remove(signal_file)
                return
                
            with open(request_file, 'r', encoding='utf-8') as f:
                request_data = json.load(f)
                
            logger.info("=" * 50)
            logger.info("📨 НОВЫЙ ЗАПРОС ОТ OPENMW")
            logger.info(f"ID запроса: {request_data.get('request_id', 'unknown')}")
            logger.info(f"НПС: {request_data.get('npc_name', 'Unknown')}")
            logger.info(f"Сообщение: {request_data.get('message', '')}")
            logger.info("=" * 50)
            
            # Отправляем на AI-сервер
            asyncio.run(self.send_to_ai_server(request_data))
            
            # Помечаем как обработанный
            self.processed_requests.add(signal_content)
            
            # Удаляем сигнальный файл
            os.remove(signal_file)
            
        except Exception as e:
            logger.error(f"Ошибка обработки запроса: {e}")
            if os.path.exists(signal_file):
                os.remove(signal_file)
                
    async def send_to_ai_server(self, request_data):
        """Отправляет запрос на AI-сервер"""
        ai_url = f"http://{self.config['ai_server_host']}:{self.config['ai_server_port']}/api/dialogue"
        
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    'npc_name': request_data.get('npc_name', ''),
                    'message': request_data.get('message', ''),
                    'context': request_data.get('context', ''),
                    'language': request_data.get('language', 'ru'),
                    'game': 'morrowind',
                    'timestamp': request_data.get('timestamp', int(time.time()))
                }
                
                logger.info(f"🚀 Отправляем запрос на AI-сервер: {ai_url}")
                
                async with session.post(
                    ai_url, 
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=self.config['request_timeout'])
                ) as response:
                    
                    if response.status == 200:
                        ai_response = await response.json()
                        logger.info("✅ Получен ответ от AI-сервера")
                        await self.save_ai_response(ai_response, request_data)
                    else:
                        logger.error(f"❌ AI-сервер вернул ошибку: {response.status}")
                        await self.save_error_response(f"AI server error: {response.status}", request_data)
                        
        except aiohttp.ClientError as e:
            logger.error(f"❌ Ошибка подключения к AI-серверу: {e}")
            await self.save_error_response(f"Connection error: {e}", request_data)
        except Exception as e:
            logger.error(f"❌ Неожиданная ошибка при обращении к AI: {e}")
            await self.save_error_response(f"Unexpected error: {e}", request_data)
            
    async def save_ai_response(self, ai_response, original_request):
        """Сохраняет ответ AI для OpenMW"""
        response_data = {
            'request_id': original_request.get('request_id', ''),
            'npc_name': original_request.get('npc_name', ''),
            'ai_response': ai_response.get('response', 'Извините, не могу ответить'),
            'status': 'success',
            'timestamp': int(time.time()),
            'processing_time': ai_response.get('processing_time', 0)
        }
        
        response_file = self.config['response_file']
        
        try:
            with open(response_file, 'w', encoding='utf-8') as f:
                json.dump(response_data, f, ensure_ascii=False, indent=2)
                
            logger.info(f"💾 Ответ сохранен для OpenMW: {response_file}")
            logger.info(f"🤖 AI ответ: {ai_response.get('response', '')[:100]}...")
            
        except Exception as e:
            logger.error(f"Ошибка сохранения ответа: {e}")
            
    async def save_error_response(self, error_message, original_request):
        """Сохраняет ошибку для OpenMW"""
        response_data = {
            'request_id': original_request.get('request_id', ''),
            'npc_name': original_request.get('npc_name', ''),
            'ai_response': f"Извините, возникла техническая проблема: {error_message}",
            'status': 'error',
            'error': error_message,
            'timestamp': int(time.time())
        }
        
        response_file = self.config['response_file']
        
        try:
            with open(response_file, 'w', encoding='utf-8') as f:
                json.dump(response_data, f, ensure_ascii=False, indent=2)
                
            logger.info(f"💾 Ошибка сохранена для OpenMW: {response_file}")
            
        except Exception as e:
            logger.error(f"Ошибка сохранения ошибки: {e}")
            
    async def start_http_server(self):
        """Запускает HTTP сервер для внешних запросов"""
        from aiohttp import web
        
        app = web.Application()
        
        app.router.add_get('/', self.handle_status)
        app.router.add_post('/api/dialogue', self.handle_dialogue_request)
        app.router.add_get('/api/status', self.handle_status)
        
        runner = web.AppRunner(app)
        await runner.setup()
        
        site = web.TCPSite(runner, 'localhost', self.config['http_server_port'])
        await site.start()
        
        logger.info(f"🌐 HTTP сервер запущен на порту {self.config['http_server_port']}")
        logger.info("🔗 Доступные эндпоинты:")
        logger.info(f"   - GET  http://localhost:{self.config['http_server_port']}/")
        logger.info(f"   - POST http://localhost:{self.config['http_server_port']}/api/dialogue")
        logger.info(f"   - GET  http://localhost:{self.config['http_server_port']}/api/status")
        
        try:
            while self.is_running:
                await asyncio.sleep(1)
        finally:
            await runner.cleanup()
            
    async def handle_status(self, request):
        """Обработчик статуса"""
        status = {
            'service': 'Morrowind AI Bridge',
            'version': '1.2',
            'status': 'running' if self.is_running else 'stopped',
            'uptime': int(time.time()),
            'processed_requests': len(self.processed_requests),
            'ai_server': f"{self.config['ai_server_host']}:{self.config['ai_server_port']}"
        }
        
        return web.json_response(status)
        
    async def handle_dialogue_request(self, request):
        """Обработчик внешних запросов диалогов"""
        try:
            data = await request.json()
            ai_response = await self.forward_to_ai_server(data)
            return web.json_response(ai_response)
            
        except Exception as e:
            logger.error(f"Ошибка обработки внешнего запроса: {e}")
            return web.json_response({'error': str(e)}, status=500)
            
    async def forward_to_ai_server(self, data):
        """Перенаправляет запрос на AI-сервер"""
        ai_url = f"http://{self.config['ai_server_host']}:{self.config['ai_server_port']}/api/dialogue"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(ai_url, json=data) as response:
                return await response.json()

def main():
    """Главная функция"""
    print("🌉 Morrowind AI Bridge v1.2")
    print("=" * 40)
    
    bridge = MorrowindAIBridge()
    bridge.start()

if __name__ == "__main__":
    main()
