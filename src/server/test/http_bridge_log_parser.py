#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
Morrowind AI Log Parser v1.3
Парсер логов OpenMW для извлечения AI запросов
============================================================================
"""

import os
import sys
import re
import time
import json
import asyncio
import aiohttp
from threading import Thread
from pathlib import Path
import logging
from datetime import datetime

# Настройка логирования
def ensure_log_directory():
    current_dir = Path(__file__).parent
    root_dir = current_dir.parent.parent.parent
    log_dir = root_dir / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir

log_directory = ensure_log_directory()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_directory / 'log_parser.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class OpenMWLogParser:
    def __init__(self):
        self.config = {
            'ai_server_host': 'localhost',
            'ai_server_port': 9090,
            'http_server_port': 8080,
            'log_file': 'f:/Games/MorrowindFullrest/game/openmw.log',  # Путь к логу OpenMW
            'request_pattern': r'\[AI_REQUEST\]\s+ID:([^|]+)\|NPC:([^|]+)\|MSG:([^|]+)\|CTX:([^|]+)\|TIME:(\d+)',
            'check_interval': 1.0,
        }
        
        self.is_running = False
        self.processed_requests = set()
        self.last_position = 0
        
    def start(self):
        """Запуск парсера логов"""
        logger.info("=" * 60)
        logger.info("📝 MORROWIND AI LOG PARSER ЗАПУСКАЕТСЯ...")
        logger.info(f"📁 Отслеживаем лог: {self.config['log_file']}")
        logger.info("=" * 60)
        
        self.is_running = True
        
        # Запускаем мониторинг логов в отдельном потоке
        monitor_thread = Thread(target=self.log_monitor_loop, daemon=True)
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
        """Остановка парсера"""
        self.is_running = False
        logger.info("🛑 Log Parser остановлен")
        
    def log_monitor_loop(self):
        """Основной цикл мониторинга логов OpenMW"""
        logger.info("👁️ Запущен мониторинг логов OpenMW...")
        
        while self.is_running:
            try:
                self.check_log_for_requests()
                time.sleep(self.config['check_interval'])
            except Exception as e:
                logger.error(f"Ошибка в мониторинге логов: {e}")
                time.sleep(1)
                
    def check_log_for_requests(self):
        """Проверяет новые AI запросы в логах OpenMW"""
        log_file = self.config['log_file']
        
        if not os.path.exists(log_file):
            return
            
        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                # Читаем с последней позиции
                f.seek(self.last_position)
                new_lines = f.readlines()
                self.last_position = f.tell()
                
                for line in new_lines:
                    self.parse_ai_request(line.strip())
                    
        except Exception as e:
            logger.error(f"Ошибка чтения лога: {e}")
            
    def parse_ai_request(self, line):
        """Парсит строку лога на предмет AI запросов"""
        pattern = self.config['request_pattern']
        match = re.search(pattern, line)
        
        if match:
            request_id = match.group(1)
            npc_name = match.group(2)
            message = match.group(3)
            context = match.group(4)
            timestamp = int(match.group(5))
            
            # Проверяем что это новый запрос
            if request_id in self.processed_requests:
                return
                
            logger.info("=" * 50)
            logger.info("📨 НОВЫЙ AI ЗАПРОС ИЗ ЛОГА OPENMW")
            logger.info(f"ID: {request_id}")
            logger.info(f"НПС: {npc_name}")
            logger.info(f"Сообщение: {message}")
            logger.info(f"Контекст: {context}")
            logger.info("=" * 50)
            
            # Формируем запрос для AI сервера
            request_data = {
                'request_id': request_id,
                'npc_name': npc_name,
                'message': message,
                'context': context,
                'timestamp': timestamp,
                'source': 'openmw_log_parser'
            }
            
            # Отправляем на AI-сервер
            asyncio.run(self.send_to_ai_server(request_data))
            
            # Помечаем как обработанный
            self.processed_requests.add(request_id)
            
    async def send_to_ai_server(self, request_data):
        """Отправляет запрос на AI-сервер"""
        ai_url = f"http://{self.config['ai_server_host']}:{self.config['ai_server_port']}/api/dialogue"
        
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    'npc_name': request_data.get('npc_name', ''),
                    'message': request_data.get('message', ''),
                    'context': request_data.get('context', ''),
                    'language': 'ru',
                    'game': 'morrowind',
                    'timestamp': request_data.get('timestamp', int(time.time()))
                }
                
                logger.info(f"🚀 Отправляем запрос на AI-сервер: {ai_url}")
                
                async with session.post(
                    ai_url, 
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        ai_response = await response.json()
                        logger.info("✅ Получен ответ от AI-сервера")
                        
                        # Логируем ответ для OpenMW (если нужно)
                        self.log_ai_response(ai_response, request_data)
                    else:
                        logger.error(f"❌ AI-сервер вернул ошибку: {response.status}")
                        
        except Exception as e:
            logger.error(f"❌ Ошибка при обращении к AI-серверу: {e}")
            
    def log_ai_response(self, ai_response, original_request):
        """Логирует ответ AI (для возможного парсинга OpenMW)"""
        response_message = f"[AI_RESPONSE] ID:{original_request['request_id']}|RESPONSE:{ai_response.get('response', 'Нет ответа')}|STATUS:success"
        logger.info(f"🤖 {response_message}")
        
    async def start_http_server(self):
        """Запускает HTTP сервер для статуса"""
        from aiohttp import web
        
        app = web.Application()
        app.router.add_get('/', self.handle_status)
        app.router.add_get('/api/status', self.handle_status)
        
        runner = web.AppRunner(app)
        await runner.setup()
        
        site = web.TCPSite(runner, 'localhost', self.config['http_server_port'])
        await site.start()
        
        logger.info(f"🌐 HTTP статус сервер запущен на порту {self.config['http_server_port']}")
        
        try:
            while self.is_running:
                await asyncio.sleep(1)
        finally:
            await runner.cleanup()
            
    async def handle_status(self, request):
        """Обработчик статуса"""
        status = {
            'service': 'Morrowind AI Log Parser',
            'version': '1.3',
            'status': 'running' if self.is_running else 'stopped',
            'processed_requests': len(self.processed_requests),
            'log_file': self.config['log_file'],
            'log_position': self.last_position
        }
        
        return web.json_response(status)

def main():
    """Главная функция"""
    print("📝 Morrowind AI Log Parser v1.3")
    print("=" * 40)
    
    parser = OpenMWLogParser()
    parser.start()

if __name__ == "__main__":
    main()
