#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
from tkinter import simpledialog, messagebox
import tkinter as tk

class MorrowindAIHotkeys:
    def __init__(self):
        self.ai_server_url = "http://127.0.0.1:8080/api/dialogue"
        self.current_npc = "Житель Морровинда"  # По умолчанию
        
    def get_npc_name(self):
        """Запрос имени текущего НПС"""
        root = tk.Tk()
        root.withdraw()
        
        npc_name = simpledialog.askstring(
            "НПС", 
            f"С кем говоришь?\n(текущий: {self.current_npc})",
            initialvalue=self.current_npc
        )
        
        if npc_name:
            self.current_npc = npc_name
            
        root.destroy()
        return self.current_npc
    
    def trigger_dialogue_with_npc(self):
        """Диалог с указанием конкретного НПС"""
        try:
            # Сначала спрашиваем имя НПС
            npc_name = self.get_npc_name()
            
            # Затем текст диалога
            root = tk.Tk()
            root.withdraw()
            
            user_input = simpledialog.askstring(
                f"Диалог с {npc_name}",
                "Что сказать?"
            )
            
            if user_input:
                response = requests.post(
                    self.ai_server_url,
                    json={
                        "session_id": f"morrowind_{int(time.time())}",
                        "text": user_input,
                        "npc_name": npc_name  # Указываем конкретного НПС
                    },
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    ai_response = data.get('ai_response', 'Молчание...')
                    
                    messagebox.showinfo(
                        f"Ответ {npc_name}",
                        f"{npc_name}:\n\n{ai_response}"
                    )
                else:
                    messagebox.showerror("Ошибка", f"AI недоступен: {response.status_code}")
            
            root.destroy()
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")

# Использование с keyboard (если установлен)
try:
    import keyboard
    
    app = MorrowindAIHotkeys()
    print("🎮 Morrowind AI Hotkeys активированы!")
    print("⌨️ Ctrl+Alt+A - Диалог с НПС")
    print("⌨️ Ctrl+Alt+Q - Выход")
    
    keyboard.add_hotkey('ctrl+alt+a', app.trigger_dialogue_with_npc)
    keyboard.add_hotkey('ctrl+alt+q', lambda: exit())
    
    print("✅ Играй в OpenMW и используй горячие клавиши!")
    keyboard.wait()
    
except ImportError:
    print("❌ Модуль keyboard не установлен")
    print("Установи: pip install keyboard")
