#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from datetime import datetime

def chat_with_morrowind_ai():
    print("🎮 Добро пожаловать в мир Morrowind с ИИ!")
    print("💬 Общайся с НПС через Gemini AI")
    print("📝 Введи 'quit' для выхода")
    print("=" * 50)
    
    session_id = f"morrowind_{int(datetime.now().timestamp())}"
    
    while True:
        try:
            user_input = input("\n🗨️ Ты говоришь: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'выход']:
                print("👋 Прощай, путешественник!")
                break
                
            if not user_input:
                continue
                
            # Отправляем запрос к AI серверу
            response = requests.post(
                "http://127.0.0.1:8080/api/dialogue",
                json={
                    "session_id": session_id,
                    "text": user_input,
                    "npc_name": "Житель Морровинда"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get('ai_response', 'Молчание...')
                print(f"🤖 {data.get('npc_name', 'НПС')}: {ai_response}")
            else:
                print(f"❌ Ошибка сервера: {response.status_code}")
                
        except KeyboardInterrupt:
            print("\n👋 До свидания!")
            break
        except Exception as e:
            print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    chat_with_morrowind_ai()
