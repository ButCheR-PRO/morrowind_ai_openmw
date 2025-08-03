#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import requests
import time
import threading
import json
import re
from pathlib import Path
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox, simpledialog
import tkinter as tk

# Попытка импорта keyboard для hotkeys (опционально)
try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False
    print("⚠️ Модуль keyboard не установлен. Горячие клавиши недоступны.")

class MorrowindAIUltimate:
    def __init__(self):
        self.ai_server_url = "http://127.0.0.1:8080/api/dialogue"
        self.status_url = "http://127.0.0.1:8080/api/status"
        self.current_npc = "Житель Морровинда"
        
        # История диалогов и НПС
        self.npc_history = []
        self.dialogue_history = []
        self.max_history = 20
        
        # Мониторинг OpenMW логов
        self.log_monitoring = False
        self.log_thread = None
        self.openmw_log_path = None
        
        # Горячие клавиши
        self.hotkeys_enabled = False
        
        # База данных НПС по локациям
        self.npc_database = {
            "🏰 Balmora": [
                "Галаса Отрелет", "Стражник Хлаалу", "Нилено Дорваин", "Рален Хлаалу",
                "Менна", "Дралса Нетхри", "Ра'Виршан", "Южный Стен-Дар", "Бэлл", 
                "Сын'Дар", "Мика Хлаалу", "Торговец оружием", "Торговец заклинаний"
            ],
            "🌊 Vivec": [
                "Арвил Белет", "Ллароса Отран", "Мераса Отран", "Дж'Зарго",
                "Танда", "Висер", "Нордская Торговка", "Стражник Ординатор"
            ],
            "⛰️ Ald'ruhn": [
                "Некреша Отрел", "Брара Мороди", "Фален Арел", "Ллерос Саран",
                "Вирана Отран", "Стражник Редоран"
            ],
            "🔥 Sadrith Mora": [
                "Мастер Арион", "Фастрен Отрел", "Телванни Маг", "Невен Овель"
            ],
            "⭐ Частые": [
                "Стражник", "Торговец", "Житель Морровинда", "НПС", "Пилигрим"
            ]
        }
        
        self.setup_gui()
        self.check_ai_connection()
        
        # Запускаем горячие клавиши если доступны
        if KEYBOARD_AVAILABLE:
            self.setup_hotkeys()

    def setup_gui(self):
        """Создание главного GUI с табами"""
        self.root = tk.Tk()
        self.root.title("🎮 Morrowind AI Ultimate v2.0")
        self.root.geometry("800x700")
        self.root.configure(bg='#2a1810')
        
        # Иконка и заголовок
        main_title = Label(self.root,
                          text="🎮 MORROWIND AI ULTIMATE",
                          font=("Arial", 16, "bold"),
                          bg='#2a1810', fg='#d4af37')
        main_title.pack(pady=10)
        
        # Статус подключения
        self.status_frame = Frame(self.root, bg='#2a1810')
        self.status_frame.pack(fill=X, padx=10, pady=5)
        
        self.status_label = Label(self.status_frame,
                                 text="🔄 Проверяю AI сервер...",
                                 font=("Arial", 10),
                                 bg='#2a1810', fg='#ffffff')
        self.status_label.pack(side=LEFT)
        
        # Кнопка переподключения
        reconnect_btn = Button(self.status_frame,
                              text="🔄 Переподключиться",
                              command=self.check_ai_connection,
                              font=("Arial", 8),
                              bg='#654321', fg='#ffffff')
        reconnect_btn.pack(side=RIGHT)
        
        # Создаём табы
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Настройка стилей для табов
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#2a1810')
        style.configure('TNotebook.Tab', background='#654321', foreground='#ffffff')
        style.map('TNotebook.Tab', background=[('selected', '#d4af37')])
        
        # Таб 1: Быстрые диалоги
        self.create_quick_dialog_tab()
        
        # Таб 2: Продвинутый чат
        self.create_advanced_chat_tab()
        
        # Таб 3: История и настройки
        self.create_history_tab()
        
        # Таб 4: Мониторинг и горячие клавиши
        self.create_monitoring_tab()

    def create_quick_dialog_tab(self):
        """Таб быстрых диалогов с НПС"""
        quick_frame = Frame(self.notebook, bg='#2a1810')
        self.notebook.add(quick_frame, text="⚡ Быстрые диалоги")
        
        # Текущий НПС
        current_frame = Frame(quick_frame, bg='#2a1810')
        current_frame.pack(fill=X, padx=10, pady=10)
        
        Label(current_frame, text="Текущий НПС:",
              bg='#2a1810', fg='#d4af37', font=("Arial", 12, "bold")).pack(anchor=W)
        
        self.current_npc_label = Label(current_frame, text=self.current_npc,
                                      font=("Arial", 14, "bold"),
                                      bg='#2a1810', fg='#00ff00')
        self.current_npc_label.pack(anchor=W)
        
        # Быстрый выбор НПС
        npc_selection_frame = Frame(quick_frame, bg='#2a1810')
        npc_selection_frame.pack(fill=X, padx=10, pady=10)
        
        Label(npc_selection_frame, text="Быстрый выбор НПС:",
              bg='#2a1810', fg='#d4af37', font=("Arial", 12)).pack(anchor=W)
        
        # Создаём кнопки НПС по группам
        for group_name, npcs in self.npc_database.items():
            group_frame = LabelFrame(npc_selection_frame, text=group_name,
                                   bg='#2a1810', fg='#d4af37', font=("Arial", 10))
            group_frame.pack(fill=X, pady=5)
            
            buttons_frame = Frame(group_frame, bg='#2a1810')
            buttons_frame.pack(fill=X, padx=5, pady=5)
            
            for i, npc in enumerate(npcs):
                if i >= 6:  # Показываем только первых 6 в группе
                    break
                btn = Button(buttons_frame, text=npc,
                           command=lambda n=npc: self.select_npc(n),
                           font=("Arial", 8),
                           bg='#654321', fg='#ffffff',
                           activebackground='#d4af37')
                btn.pack(side=LEFT, padx=2, pady=2, fill=X, expand=True)
        
        # Ручной ввод НПС
        manual_frame = Frame(quick_frame, bg='#2a1810')
        manual_frame.pack(fill=X, padx=10, pady=10)
        
        Label(manual_frame, text="Или введи имя НПС:",
              bg='#2a1810', fg='#d4af37', font=("Arial", 11)).pack(anchor=W)
        
        entry_frame = Frame(manual_frame, bg='#2a1810')
        entry_frame.pack(fill=X, pady=5)
        
        self.npc_entry = Entry(entry_frame, font=("Arial", 12),
                              bg='#3a2820', fg='#ffffff',
                              insertbackground='#d4af37')
        self.npc_entry.pack(side=LEFT, fill=X, expand=True)
        
        set_npc_btn = Button(entry_frame, text="✅ Выбрать",
                           command=self.set_manual_npc,
                           font=("Arial", 10),
                           bg='#8b4513', fg='#ffffff')
        set_npc_btn.pack(side=RIGHT, padx=(5, 0))
        
        # Поле диалога
        dialog_frame = Frame(quick_frame, bg='#2a1810')
        dialog_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        Label(dialog_frame, text="Твоя реплика:",
              bg='#2a1810', fg='#d4af37', font=("Arial", 12)).pack(anchor=W)
        
        self.quick_dialog_text = Text(dialog_frame, height=4, font=("Arial", 11),
                                     bg='#3a2820', fg='#ffffff',
                                     insertbackground='#d4af37')
        self.quick_dialog_text.pack(fill=X, pady=5)
        
        # Кнопки действий
        action_frame = Frame(dialog_frame, bg='#2a1810')
        action_frame.pack(fill=X, pady=5)
        
        send_btn = Button(action_frame, text="🤖 Отправить в ИИ",
                         command=self.send_quick_dialog,
                         font=("Arial", 12, "bold"),
                         bg='#8b4513', fg='#ffffff',
                         activebackground='#d4af37')
        send_btn.pack(side=LEFT, padx=(0, 5))
        
        clear_btn = Button(action_frame, text="🗑️ Очистить",
                          command=lambda: self.quick_dialog_text.delete("1.0", "end"),
                          font=("Arial", 10),
                          bg='#654321', fg='#ffffff')
        clear_btn.pack(side=LEFT)
        
        # Область ответа
        Label(dialog_frame, text="Ответ ИИ:",
              bg='#2a1810', fg='#d4af37', font=("Arial", 12)).pack(anchor=W, pady=(10, 0))
        
        self.quick_response_text = Text(dialog_frame, height=8, font=("Arial", 11),
                                       bg='#1a1010', fg='#d4af37',
                                       state=DISABLED, wrap=WORD)
        self.quick_response_text.pack(fill=BOTH, expand=True, pady=5)
        
        # Привязки клавиш
        self.quick_dialog_text.bind('<Control-Return>', lambda e: self.send_quick_dialog())
        self.npc_entry.bind('<Return>', lambda e: self.set_manual_npc())

    def create_advanced_chat_tab(self):
        """Таб продвинутого чата"""
        chat_frame = Frame(self.notebook, bg='#2a1810')
        self.notebook.add(chat_frame, text="💬 Продвинутый чат")
        
        # Область чата с прокруткой
        chat_container = Frame(chat_frame, bg='#2a1810')
        chat_container.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        Label(chat_container, text="Чат с Morrowind AI:",
              bg='#2a1810', fg='#d4af37', font=("Arial", 14, "bold")).pack(anchor=W)
        
        # Создаём область чата с прокруткой
        chat_scroll_frame = Frame(chat_container, bg='#2a1810')
        chat_scroll_frame.pack(fill=BOTH, expand=True, pady=10)
        
        chat_scrollbar = Scrollbar(chat_scroll_frame)
        chat_scrollbar.pack(side=RIGHT, fill=Y)
        
        self.chat_text = Text(chat_scroll_frame, font=("Arial", 11),
                             bg='#1a1010', fg='#ffffff', wrap=WORD,
                             yscrollcommand=chat_scrollbar.set,
                             state=DISABLED)
        self.chat_text.pack(side=LEFT, fill=BOTH, expand=True)
        chat_scrollbar.config(command=self.chat_text.yview)
        
        # Поле ввода чата
        chat_input_frame = Frame(chat_container, bg='#2a1810')
        chat_input_frame.pack(fill=X, pady=10)
        
        Label(chat_input_frame, text="Введи сообщение:",
              bg='#2a1810', fg='#d4af37', font=("Arial", 11)).pack(anchor=W)
        
        input_container = Frame(chat_input_frame, bg='#2a1810')
        input_container.pack(fill=X, pady=5)
        
        self.chat_input = Entry(input_container, font=("Arial", 12),
                               bg='#3a2820', fg='#ffffff',
                               insertbackground='#d4af37')
        self.chat_input.pack(side=LEFT, fill=X, expand=True)
        
        send_chat_btn = Button(input_container, text="📤 Отправить",
                              command=self.send_chat_message,
                              font=("Arial", 11),
                              bg='#8b4513', fg='#ffffff')
        send_chat_btn.pack(side=RIGHT, padx=(5, 0))
        
        # Кнопки управления чатом
        chat_controls = Frame(chat_container, bg='#2a1810')
        chat_controls.pack(fill=X, pady=5)
        
        clear_chat_btn = Button(chat_controls, text="🗑️ Очистить чат",
                               command=self.clear_chat,
                               font=("Arial", 10),
                               bg='#654321', fg='#ffffff')
        clear_chat_btn.pack(side=LEFT)
        
        save_chat_btn = Button(chat_controls, text="💾 Сохранить чат",
                              command=self.save_chat,
                              font=("Arial", 10),
                              bg='#654321', fg='#ffffff')
        save_chat_btn.pack(side=LEFT, padx=(5, 0))
        
        # Привязка Enter для отправки
        self.chat_input.bind('<Return>', lambda e: self.send_chat_message())

    def create_history_tab(self):
        """Таб истории и настроек"""
        history_frame = Frame(self.notebook, bg='#2a1810')
        self.notebook.add(history_frame, text="📚 История")
        
        # История НПС
        npc_hist_frame = LabelFrame(history_frame, text="История НПС",
                                   bg='#2a1810', fg='#d4af37', font=("Arial", 12))
        npc_hist_frame.pack(fill=X, padx=10, pady=10)
        
        self.npc_history_listbox = Listbox(npc_hist_frame, height=6,
                                          bg='#3a2820', fg='#ffffff',
                                          selectbackground='#d4af37',
                                          font=("Arial", 10))
        self.npc_history_listbox.pack(fill=X, padx=5, pady=5)
        
        # Кнопки для истории НПС
        npc_hist_controls = Frame(npc_hist_frame, bg='#2a1810')
        npc_hist_controls.pack(fill=X, padx=5, pady=5)
        
        select_from_hist_btn = Button(npc_hist_controls, text="✅ Выбрать из истории",
                                     command=self.select_npc_from_history,
                                     font=("Arial", 9),
                                     bg='#654321', fg='#ffffff')
        select_from_hist_btn.pack(side=LEFT)
        
        clear_npc_hist_btn = Button(npc_hist_controls, text="🗑️ Очистить историю НПС",
                                   command=self.clear_npc_history,
                                   font=("Arial", 9),
                                   bg='#654321', fg='#ffffff')
        clear_npc_hist_btn.pack(side=RIGHT)
        
        # История диалогов
        dialog_hist_frame = LabelFrame(history_frame, text="История диалогов",
                                      bg='#2a1810', fg='#d4af37', font=("Arial", 12))
        dialog_hist_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Список диалогов с прокруткой
        dialog_container = Frame(dialog_hist_frame, bg='#2a1810')
        dialog_container.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        dialog_scroll = Scrollbar(dialog_container)
        dialog_scroll.pack(side=RIGHT, fill=Y)
        
        self.dialog_history_text = Text(dialog_container, font=("Arial", 9),
                                       bg='#1a1010', fg='#ffffff', wrap=WORD,
                                       yscrollcommand=dialog_scroll.set,
                                       state=DISABLED)
        self.dialog_history_text.pack(side=LEFT, fill=BOTH, expand=True)
        dialog_scroll.config(command=self.dialog_history_text.yview)
        
        # Кнопки управления историей диалогов
        dialog_hist_controls = Frame(dialog_hist_frame, bg='#2a1810')
        dialog_hist_controls.pack(fill=X, padx=5, pady=5)
        
        save_history_btn = Button(dialog_hist_controls, text="💾 Сохранить историю",
                                 command=self.save_dialog_history,
                                 font=("Arial", 9),
                                 bg='#654321', fg='#ffffff')
        save_history_btn.pack(side=LEFT)
        
        clear_dialog_hist_btn = Button(dialog_hist_controls, text="🗑️ Очистить историю",
                                      command=self.clear_dialog_history,
                                      font=("Arial", 9),
                                      bg='#654321', fg='#ffffff')
        clear_dialog_hist_btn.pack(side=RIGHT)

    def create_monitoring_tab(self):
        """Таб мониторинга и настроек"""
        monitoring_frame = Frame(self.notebook, bg='#2a1810')
        self.notebook.add(monitoring_frame, text="⚙️ Настройки")
        
        # Горячие клавиши
        hotkey_frame = LabelFrame(monitoring_frame, text="Горячие клавиши",
                                 bg='#2a1810', fg='#d4af37', font=("Arial", 12))
        hotkey_frame.pack(fill=X, padx=10, pady=10)
        
        if KEYBOARD_AVAILABLE:
            hotkey_status = Label(hotkey_frame, text="✅ Модуль keyboard доступен",
                                 bg='#2a1810', fg='#00ff00', font=("Arial", 10))
            hotkey_status.pack(anchor=W, padx=5, pady=5)
            
            hotkey_info = Label(hotkey_frame,
                               text="🔥 Ctrl+Alt+A - Быстрый диалог с ИИ\n"
                                    "🔥 Ctrl+Alt+C - Открыть чат\n"
                                    "🔥 Ctrl+Alt+Q - Выход из программы",
                               bg='#2a1810', fg='#ffffff', font=("Arial", 9),
                               justify=LEFT)
            hotkey_info.pack(anchor=W, padx=5, pady=5)
            
            self.hotkey_toggle_btn = Button(hotkey_frame, text="🎯 Включить hotkeys",
                                           command=self.toggle_hotkeys,
                                           font=("Arial", 10),
                                           bg='#8b4513', fg='#ffffff')
            self.hotkey_toggle_btn.pack(padx=5, pady=5)
        else:
            hotkey_error = Label(hotkey_frame, text="❌ Модуль keyboard недоступен",
                                bg='#2a1810', fg='#ff0000', font=("Arial", 10))
            hotkey_error.pack(anchor=W, padx=5, pady=5)
            
            install_info = Label(hotkey_frame,
                                text="Для установки горячих клавиш:\npip install keyboard",
                                bg='#2a1810', fg='#ffffff', font=("Arial", 9))
            install_info.pack(anchor=W, padx=5, pady=5)
        
        # Настройки AI сервера
        ai_settings_frame = LabelFrame(monitoring_frame, text="Настройки AI сервера",
                                      bg='#2a1810', fg='#d4af37', font=("Arial", 12))
        ai_settings_frame.pack(fill=X, padx=10, pady=10)
        
        Label(ai_settings_frame, text="URL AI сервера:",
              bg='#2a1810', fg='#ffffff', font=("Arial", 10)).pack(anchor=W, padx=5)
        
        self.ai_url_entry = Entry(ai_settings_frame, font=("Arial", 10),
                                 bg='#3a2820', fg='#ffffff')
        self.ai_url_entry.insert(0, self.ai_server_url)
        self.ai_url_entry.pack(fill=X, padx=5, pady=5)
        
        update_url_btn = Button(ai_settings_frame, text="🔄 Обновить URL",
                               command=self.update_ai_url,
                               font=("Arial", 9),
                               bg='#654321', fg='#ffffff')
        update_url_btn.pack(padx=5, pady=5)
        
        # Статистика
        stats_frame = LabelFrame(monitoring_frame, text="Статистика",
                                bg='#2a1810', fg='#d4af37', font=("Arial", 12))
        stats_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        self.stats_text = Text(stats_frame, height=8, font=("Arial", 9),
                              bg='#1a1010', fg='#ffffff',
                              state=DISABLED)
        self.stats_text.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        refresh_stats_btn = Button(stats_frame, text="🔄 Обновить статистику",
                                  command=self.update_stats,
                                  font=("Arial", 9),
                                  bg='#654321', fg='#ffffff')
        refresh_stats_btn.pack(pady=5)

    def select_npc(self, npc_name):
        """Выбор НПС и обновление истории"""
        self.current_npc = npc_name
        self.current_npc_label.config(text=npc_name)
        
        # Добавляем в историю
        if npc_name in self.npc_history:
            self.npc_history.remove(npc_name)
        self.npc_history.insert(0, npc_name)
        self.npc_history = self.npc_history[:self.max_history]
        
        self.update_npc_history_display()
        print(f"✅ Выбран НПС: {npc_name}")

    def set_manual_npc(self):
        """Установка НПС вручную"""
        npc_name = self.npc_entry.get().strip()
        if npc_name:
            self.select_npc(npc_name)
            self.npc_entry.delete(0, END)

    def send_quick_dialog(self):
        """Отправка быстрого диалога"""
        user_text = self.quick_dialog_text.get("1.0", "end-1c").strip()
        
        if not user_text:
            messagebox.showwarning("Предупреждение", "Введи текст для диалога!")
            return
        
        self.send_to_ai(user_text, self.current_npc, self.quick_response_text)
        self.quick_dialog_text.delete("1.0", "end")

    def send_chat_message(self):
        """Отправка сообщения в чат"""
        user_text = self.chat_input.get().strip()
        
        if not user_text:
            return
        
        # Добавляем сообщение пользователя в чат
        self.add_to_chat(f"🗨️ Ты: {user_text}")
        
        # Отправляем в AI
        try:
            response = requests.post(
                self.ai_server_url,
                json={
                    "session_id": f"chat_{int(time.time())}",
                    "text": user_text,
                    "npc_name": self.current_npc
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get('ai_response', 'Молчание...')
                
                # Добавляем ответ ИИ в чат
                self.add_to_chat(f"🤖 {self.current_npc}: {ai_response}")
                
                # Добавляем в историю диалогов
                self.add_to_dialogue_history(user_text, ai_response, self.current_npc)
                
            else:
                self.add_to_chat(f"❌ Ошибка AI сервера: {response.status_code}")
                
        except Exception as e:
            self.add_to_chat(f"❌ Ошибка подключения: {e}")
        
        self.chat_input.delete(0, END)

    def send_to_ai(self, user_text, npc_name, response_widget):
        """Универсальная отправка в AI"""
        try:
            print(f"📤 Отправляю: '{user_text}' для {npc_name}")
            
            response = requests.post(
                self.ai_server_url,
                json={
                    "session_id": f"ultimate_{int(time.time())}",
                    "text": user_text,
                    "npc_name": npc_name
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get('ai_response', 'Молчание...')
                
                # Показываем ответ
                response_widget.config(state=NORMAL)
                response_widget.delete("1.0", "end")
                response_widget.insert("1.0", f"🤖 {npc_name}:\n\n{ai_response}")
                response_widget.config(state=DISABLED)
                
                # Добавляем в историю
                self.add_to_dialogue_history(user_text, ai_response, npc_name)
                
                print(f"✅ Получен ответ от {npc_name}")
                
            else:
                error_msg = f"❌ Ошибка AI сервера: {response.status_code}"
                response_widget.config(state=NORMAL)
                response_widget.delete("1.0", "end")
                response_widget.insert("1.0", error_msg)
                response_widget.config(state=DISABLED)
                
        except Exception as e:
            error_msg = f"❌ Ошибка подключения: {e}"
            response_widget.config(state=NORMAL)
            response_widget.delete("1.0", "end")
            response_widget.insert("1.0", error_msg)
            response_widget.config(state=DISABLED)

    def add_to_chat(self, message):
        """Добавление сообщения в чат"""
        self.chat_text.config(state=NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_text.insert(END, f"[{timestamp}] {message}\n\n")
        self.chat_text.see(END)
        self.chat_text.config(state=DISABLED)

    def add_to_dialogue_history(self, user_text, ai_response, npc_name):
        """Добавление в историю диалогов"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dialogue_entry = {
            "timestamp": timestamp,
            "user": user_text,
            "ai": ai_response,
            "npc": npc_name
        }
        
        self.dialogue_history.insert(0, dialogue_entry)
        self.dialogue_history = self.dialogue_history[:self.max_history]
        
        self.update_dialogue_history_display()

    def update_npc_history_display(self):
        """Обновление отображения истории НПС"""
        self.npc_history_listbox.delete(0, END)
        for npc in self.npc_history:
            self.npc_history_listbox.insert(END, npc)

    def update_dialogue_history_display(self):
        """Обновление отображения истории диалогов"""
        self.dialog_history_text.config(state=NORMAL)
        self.dialog_history_text.delete("1.0", "end")
        
        for entry in self.dialogue_history:
            self.dialog_history_text.insert(END, 
                f"[{entry['timestamp']}] с {entry['npc']}\n"
                f"🗨️ Ты: {entry['user']}\n"
                f"🤖 ИИ: {entry['ai']}\n"
                f"{'-'*50}\n\n")
        
        self.dialog_history_text.config(state=DISABLED)

    def select_npc_from_history(self):
        """Выбор НПС из истории"""
        selection = self.npc_history_listbox.curselection()
        if selection:
            npc_name = self.npc_history_listbox.get(selection[0])
            self.select_npc(npc_name)

    def clear_npc_history(self):
        """Очистка истории НПС"""
        self.npc_history.clear()
        self.update_npc_history_display()

    def clear_chat(self):
        """Очистка чата"""
        self.chat_text.config(state=NORMAL)
        self.chat_text.delete("1.0", "end")
        self.chat_text.config(state=DISABLED)

    def clear_dialog_history(self):
        """Очистка истории диалогов"""
        self.dialogue_history.clear()
        self.update_dialogue_history_display()

    def save_chat(self):
        """Сохранение чата в файл"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"morrowind_ai_chat_{timestamp}.txt"
            
            chat_content = self.chat_text.get("1.0", "end-1c")
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"=== Morrowind AI Chat - {timestamp} ===\n\n")
                f.write(chat_content)
            
            messagebox.showinfo("Успех", f"Чат сохранен в файл: {filename}")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить чат: {e}")

    def save_dialog_history(self):
        """Сохранение истории диалогов"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"morrowind_ai_history_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.dialogue_history, f, ensure_ascii=False, indent=2)
            
            messagebox.showinfo("Успех", f"История сохранена в файл: {filename}")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")

    def check_ai_connection(self):
        """Проверка подключения к AI серверу"""
        try:
            response = requests.get(self.status_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                gemini_available = data.get('gemini_available', False)
                
                if gemini_available:
                    self.status_label.config(text="🟢 AI сервер готов (Gemini работает)", fg='#00ff00')
                else:
                    self.status_label.config(text="🟡 AI сервер доступен (Gemini недоступен)", fg='#ffff00')
            else:
                self.status_label.config(text="🟡 AI сервер отвечает с ошибками", fg='#ffff00')
        except:
            self.status_label.config(text="🔴 AI сервер недоступен", fg='#ff0000')

    def update_ai_url(self):
        """Обновление URL AI сервера"""
        new_url = self.ai_url_entry.get().strip()
        if new_url:
            self.ai_server_url = new_url
            self.status_url = new_url.replace('/dialogue', '/status')
            self.check_ai_connection()
            print(f"✅ URL обновлен: {new_url}")

    def update_stats(self):
        """Обновление статистики"""
        self.stats_text.config(state=NORMAL)
        self.stats_text.delete("1.0", "end")
        
        stats = f"""📊 Статистика Morrowind AI Ultimate:

🎭 НПС в истории: {len(self.npc_history)}
💬 Диалогов в истории: {len(self.dialogue_history)}
🤖 Текущий НПС: {self.current_npc}
⌨️ Горячие клавиши: {'Включены' if self.hotkeys_enabled else 'Выключены'}
🔗 AI сервер: {self.ai_server_url}

📈 Последние НПС:
"""
        
        for i, npc in enumerate(self.npc_history[:5]):
            stats += f"  {i+1}. {npc}\n"
        
        if self.dialogue_history:
            last_dialog = self.dialogue_history[0]
            stats += f"\n🕒 Последний диалог: {last_dialog['timestamp']}\n"
            stats += f"   с {last_dialog['npc']}"
        
        self.stats_text.insert("1.0", stats)
        self.stats_text.config(state=DISABLED)

    def setup_hotkeys(self):
        """Настройка горячих клавиш"""
        if not KEYBOARD_AVAILABLE:
            return
        
        try:
            keyboard.add_hotkey('ctrl+alt+a', self.hotkey_quick_dialog)
            keyboard.add_hotkey('ctrl+alt+c', self.hotkey_open_chat)
            keyboard.add_hotkey('ctrl+alt+q', self.hotkey_quit)
            print("✅ Горячие клавиши настроены")
        except Exception as e:
            print(f"❌ Ошибка настройки горячих клавиш: {e}")

    def toggle_hotkeys(self):
        """Переключение горячих клавиш"""
        if not KEYBOARD_AVAILABLE:
            return
        
        if self.hotkeys_enabled:
            keyboard.unhook_all()
            self.hotkeys_enabled = False
            self.hotkey_toggle_btn.config(text="🎯 Включить hotkeys")
            print("❌ Горячие клавиши отключены")
        else:
            self.setup_hotkeys()
            self.hotkeys_enabled = True
            self.hotkey_toggle_btn.config(text="🚫 Отключить hotkeys")
            print("✅ Горячие клавиши включены")

    def hotkey_quick_dialog(self):
        """Горячая клавиша быстрого диалога"""
        try:
            # Переключаемся на таб быстрых диалогов
            self.notebook.select(0)
            
            # Поднимаем окно на передний план
            self.root.lift()
            self.root.focus_force()
            
            # Фокус на поле ввода
            self.quick_dialog_text.focus_set()
            
        except Exception as e:
            print(f"❌ Ошибка hotkey: {e}")

    def hotkey_open_chat(self):
        """Горячая клавиша открытия чата"""
        try:
            # Переключаемся на таб чата
            self.notebook.select(1)
            
            # Поднимаем окно на передний план
            self.root.lift()
            self.root.focus_force()
            
            # Фокус на поле ввода чата
            self.chat_input.focus_set()
            
        except Exception as e:
            print(f"❌ Ошибка hotkey: {e}")

    def hotkey_quit(self):
        """Горячая клавиша выхода"""
        self.quit_app()

    def quit_app(self):
        """Выход из приложения"""
        if KEYBOARD_AVAILABLE and self.hotkeys_enabled:
            keyboard.unhook_all()
        
        self.root.quit()
        self.root.destroy()

    def run(self):
        """Запуск приложения"""
        # Обновляем начальные данные
        self.update_npc_history_display()
        self.update_stats()
        
        # Запускаем GUI
        try:
            self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
            self.root.mainloop()
        except KeyboardInterrupt:
            self.quit_app()

def main():
    print("🎮 Запуск Morrowind AI Ultimate v2.0...")
    print("🚀 Универсальный инструмент для AI диалогов в Morrowind")
    print("=" * 60)
    
    try:
        app = MorrowindAIUltimate()
        app.run()
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        input("Нажми Enter для выхода...")

if __name__ == "__main__":
    main()
