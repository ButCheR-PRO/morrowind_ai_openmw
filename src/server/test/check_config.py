#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import os
import sys
from pathlib import Path

def check_config():
    print("🔍 Проверяем config.yml...")
    
    # ПРАВИЛЬНЫЙ путь - ищем в корне проекта (на 3 уровня выше от src/server/test/)
    config_path = Path(__file__).parent.parent.parent.parent / 'config.yml'
    
    # Альтернативный способ поиска - через абсолютный путь
    if not config_path.exists():
        # Попробуем найти через рабочую директорию
        config_path = Path.cwd() / 'config.yml'
    
    # Ещё один способ - через переменные окружения или стандартные места
    if not config_path.exists():
        # Ищем в родительских директориях от текущей
        current = Path.cwd()
        for _ in range(5):  # максимум 5 уровней вверх
            potential_config = current / 'config.yml'
            if potential_config.exists():
                config_path = potential_config
                break
            current = current.parent
    
    if not config_path.exists():
        print("❌ Файл config.yml НЕ найден!")
        print(f"📁 Искали в: {config_path}")
        print("📂 Текущая директория:", Path.cwd())
        print("📂 Директория скрипта:", Path(__file__).parent)
        # Покажем что есть в корне проекта
        root_dir = Path(__file__).parent.parent.parent.parent
        if root_dir.exists():
            print(f"📂 Содержимое корня проекта {root_dir}:")
            for item in root_dir.iterdir():
                print(f"   - {item.name}")
        return False
    
    try:
        # Читаем конфиг
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        if config is None:
            print("❌ Config.yml пустой или содержит только комментарии!")
            return False
            
        print("✅ Config.yml читается корректно!")
        print(f"📄 Путь к файлу: {config_path}")
        
        # Проверяем ВСЕ обязательные секции
        required_sections = {
            'morrowind_data_files_dir': 'Путь к данным Morrowind',
            'language': 'Язык системы', 
            'log': 'Настройки логирования',
            'speech_to_text': 'Распознавание речи (STT)',
            'text_to_speech': 'Синтез речи (TTS)',
            'llm': 'LLM провайдеры',
            'event_bus': 'Шина событий',
            'rpc': 'RPC сервер',
            'database': 'База данных',
            'player_database': 'База данных игрока',
            'npc_database': 'База данных НПС',
            'npc_director': 'Режиссёр НПС',
            'npc_speaker': 'Голос НПС',
            'scene_instructions': 'Инструкции сцены'
        }
        
        missing_sections = []
        for section, description in required_sections.items():
            if section in config:
                print(f"✅ Секция '{section}' найдена - {description}")
                
                # Дополнительные проверки для важных секций
                if section == 'morrowind_data_files_dir':
                    data_dir = Path(config[section])
                    if data_dir.exists():
                        print(f"   📁 Путь к данным Morrowind корректен: {data_dir}")
                    else:
                        print(f"   ⚠️ Путь к данным Morrowind не найден: {data_dir}")
                
                elif section == 'event_bus':
                    if 'host' in config[section] and 'port' in config[section]:
                        host = config[section]['host']
                        port = config[section]['port']
                        print(f"   📡 Event Bus: {host}:{port}")
                
                elif section == 'rpc':
                    if 'host' in config[section] and 'port' in config[section]:
                        host = config[section]['host']
                        port = config[section]['port']
                        print(f"   🔌 RPC сервер: {host}:{port}")
                
                elif section == 'log':
                    if all(field in config[section] for field in ['log_to_console', 'log_to_file', 'file_path']):
                        print(f"   📋 Логирование настроено корректно")
                    else:
                        print(f"   ⚠️ В секции log отсутствуют обязательные поля")
                        
            else:
                print(f"❌ Секция '{section}' отсутствует!")
                missing_sections.append(section)
        
        if missing_sections:
            print(f"❌ Критические секции отсутствуют: {', '.join(missing_sections)}")
            return False
        
        # Проверяем Gemini API ключ
        if 'llm' in config and 'system' in config['llm']:
            if 'google' in config['llm']['system']:
                api_key = config['llm']['system']['google'].get('api_key', '')
                if api_key and api_key != "ТВОЙ_GEMINI_API_КЛЮЧ_ЗДЕСЬ":
                    print(f"✅ Gemini API ключ: {len(api_key)} символов")
                else:
                    print("⚠️ Gemini API ключ не настроен!")
            else:
                print("⚠️ Конфигурация Google Gemini не найдена")
        
        # Проверяем язык
        if 'language' in config:
            lang = config['language']
            print(f"🌍 Язык системы: {lang}")
        
        # Дополнительные проверки папок
        print("\n📋 Дополнительные проверки:")
        
        # Проверяем папки logs и data относительно config.yml
        root_dir = config_path.parent
        logs_dir = root_dir / 'logs'
        data_dir = root_dir / 'data'
        
        if not logs_dir.exists():
            logs_dir.mkdir()
            print("✅ Папка logs создана")
        else:
            print("✅ Папка logs найдена")
            
        if not data_dir.exists():
            data_dir.mkdir()
            print("✅ Папка data создана")
        else:
            print("✅ Папка data найдена")
        
        # Проверяем scene_instructions.txt
        scene_file = data_dir / 'scene_instructions.txt'
        if not scene_file.exists():
            scene_file.touch()
            print("✅ Файл scene_instructions.txt создан")
        else:
            print("✅ Файл scene_instructions.txt найден")
        
        print("\n🎉 Конфигурация готова к использованию!")
        return True
        
    except yaml.YAMLError as e:
        print(f"❌ Ошибка в YAML синтаксисе: {e}")
        return False
    except Exception as e:
        print(f"❌ Общая ошибка: {e}")
        return False

def main():
    """Главная функция"""
    print("=" * 50)
    print("🔧 ПРОВЕРКА КОНФИГУРАЦИИ MORROWIND AI")
    print("=" * 50)
    
    success = check_config()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 КОНФИГУРАЦИЯ КОРРЕКТНА!")
        print("✅ Система готова к запуску")
    else:
        print("💥 ПРОБЛЕМЫ С КОНФИГУРАЦИЕЙ!")
        print("❌ Исправьте ошибки перед запуском")
    print("=" * 50)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
