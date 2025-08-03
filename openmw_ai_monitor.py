#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import re
import requests
import threading
from pathlib import Path
from datetime import datetime

class OpenMWAIMonitor:
    def __init__(self):
        self.ai_server_url = "http://127.0.0.1:8080/api/dialogue"
        self.openmw_log_path = None  # Путь к логу OpenMW
        self.last_position = 0
        
    def find_openmw_log(self):
        """Поиск лога OpenMW"""
        possible_paths = [
            Path.home() / "Documents" / "My Games" / "OpenMW" / "openmw.log",
            Path("openmw.log"),
            Path("logs") / "openmw.log"
        ]
        
        for path in possible_paths:
            if path.exists():
                print(f"✅ Найден лог OpenMW: {path}")
                return path
                
        print("❌ Лог OpenMW не найден")
        return None
    
    def parse_dialogue_from_log(self, line):
        """Извлекает диалоги из строки лога"""
        # Ищем паттерны диалогов (это примерные паттерны)
        patterns = [
            r'Dialog with (.+): (.+)',  # Диалог с НПС
            r'Player says: (.+)',        # Реплика игрока
            r'NPC (.+) says: (.+)'       # Реплика НПС
        ]
        
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                return match.groups()
        return None
    
    def send_to_ai(self, player_text, npc_name="НПС"):
        """Отправка запроса к AI серверу"""
        try:
            response = requests.post(
                self.ai_server_url,
                json={
                    "session_id": f"openmw_monitor_{int(time.time())}",
                    "text": player_text,
                    "npc_name": npc_name
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('ai_response', 'Молчание...')
            else:
                return f"Ошибка AI сервера: {response.status_code}"
                
        except Exception as e:
            return f"Ошибка подключения к AI: {e}"
    
    def monitor_log_file(self):
        """Мониторинг лога OpenMW в реальном времени"""
        if not self.openmw_log_path:
            self.openmw_log_path = self.find_openmw_log()
            if not self.openmw_log_path:
                return
        
        print(f"👁️ Мониторинг OpenMW: {self.openmw_log_path}")
        
        try:
            with open(self.openmw_log_path, 'r', encoding='utf-8') as f:
                # Переходим в конец файла
                f.seek(0, 2)
                self.last_position = f.tell()
                
                while True:
                    line = f.readline()
                    if line:
                        # Обрабатываем новую строку
                        dialogue_data = self.parse_dialogue_from_log(line.strip())
                        if dialogue_data:
                            print(f"📝 Найден диалог: {dialogue_data}")
                            
                            # Отправляем в AI если это реплика игрока
                            if "Player says" in line or len(dialogue_data) >= 2:
                                player_text = dialogue_data[-1]  # Последний элемент - текст
                                npc_name = dialogue_data[0] if len(dialogue_data) > 1 else "НПС"
                                
                                print(f"🤖 Отправляю в AI: '{player_text}'")
                                ai_response = self.send_to_ai(player_text, npc_name)
                                print(f"💬 AI ответ: {ai_response}")
                                
                                # TODO: Отправить ответ обратно в игру
                                self.send_response_to_game(ai_response, npc_name)
                    else:
                        time.sleep(0.1)  # Ждем новых строк
                        
        except Exception as e:
            print(f"❌ Ошибка мониторинга: {e}")
    
    def send_response_to_game(self, ai_response, npc_name):
        """Отправка ответа AI обратно в игру (пока заглушка)"""
        # В OpenMW 0.49.0 нет простого способа это сделать
        # Можно записать в файл который мониторит другой скрипт
        response_file = Path("ai_responses") / f"response_{int(time.time())}.txt"
        response_file.parent.mkdir(exist_ok=True)
        
        with open(response_file, 'w', encoding='utf-8') as f:
            f.write(f"NPC: {npc_name}\n")
            f.write(f"RESPONSE: {ai_response}\n")
            f.write(f"TIMESTAMP: {datetime.now().isoformat()}\n")
        
        print(f"💾 Ответ сохранен в файл: {response_file}")

def main():
    print("🎮 OpenMW AI Monitor v1.0")
    print("👁️ Мониторинг диалогов OpenMW для AI интеграции")
    print("=" * 50)
    
    monitor = OpenMWAIMonitor()
    
    try:
        monitor.monitor_log_file()
    except KeyboardInterrupt:
        print("\n👋 Остановка мониторинга...")

if __name__ == "__main__":
    main()
