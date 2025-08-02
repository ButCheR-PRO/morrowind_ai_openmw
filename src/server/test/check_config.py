#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import os
import sys

def check_config():
    print("🔍 Проверяем config.yml...")
    
    # Проверяем наличие файла
    if not os.path.exists('config.yml'):
        print("❌ Файл config.yml НЕ найден!")
        return False
    
    try:
        # Читаем конфиг
        with open('config.yml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        print("✅ Config.yml читается корректно!")
        
        # Проверяем основные секции
        required_sections = [
            'morrowind_data_files_dir',
            'language', 
            'llm',
            'event_bus',
            'rpc'
        ]
        
        for section in required_sections:
            if section in config:
                print(f"✅ Секция '{section}' найдена")
            else:
                print(f"❌ Секция '{section}' отсутствует!")
                return False
        
        # Проверяем Gemini API ключ
        if 'llm' in config and 'system' in config['llm']:
            if 'google' in config['llm']['system']:
                api_key = config['llm']['system']['google'].get('api_key', '')
                if api_key and api_key != "ВАШ_GEMINI_API_КЛЮЧ":
                    print(f"✅ Gemini API ключ: {len(api_key)} символов")
                else:
                    print("⚠️  Gemini API ключ не настроен!")
        
        print("\n🎉 Конфигурация готова к использованию!")
        return True
        
    except yaml.YAMLError as e:
        print(f"❌ Ошибка в YAML синтаксисе: {e}")
        return False
    except Exception as e:
        print(f"❌ Общая ошибка: {e}")
        return False

if __name__ == "__main__":
    check_config()

