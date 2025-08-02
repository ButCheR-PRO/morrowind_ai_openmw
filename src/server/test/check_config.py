#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import os
import sys
from pathlib import Path

def check_config():
    print("🔍 Проверяем config.yml...")
    
    # Проверяем наличие файла
    config_path = Path('config.yml')
    if not config_path.exists():
        print("❌ Файл config.yml НЕ найден!")
        print("📁 Ищем в текущей директории:", Path.cwd())
        
        # Попробуем найти config.yml в родительских директориях
        for parent in Path.cwd().parents:
            potential_config = parent / 'config.yml'
            if potential_config.exists():
                print(f"✅ Найден config.yml в: {potential_config}")
                config_path = potential_config
                break
        else:
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
        
        # Проверяем основные секции
        required_sections = [
            'morrowind_data_files_dir',
            'language', 
            'llm',
            'event_bus',
            'rpc'
        ]
        
        missing_sections = []
        for section in required_sections:
            if section in config:
                print(f"✅ Секция '{section}' найдена")
                
                # Дополнительные проверки для каждой секции
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
                    else:
                        print(f"   ⚠️ В секции event_bus отсутствуют host или port")
                
                elif section == 'rpc':
                    if 'host' in config[section] and 'port' in config[section]:
                        host = config[section]['host']
                        port = config[section]['port']
                        print(f"   🔌 RPC сервер: {host}:{port}")
                    else:
                        print(f"   ⚠️ В секции rpc отсутствуют host или port")
                        
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
                if api_key and api_key != "ВАШ_GEMINI_API_КЛЮЧ":
                    print(f"✅ Gemini API ключ: {len(api_key)} символов")
                else:
                    print("⚠️ Gemini API ключ не настроен!")
                    print("   🔑 Установите ваш API ключ Google Gemini")
            else:
                print("⚠️ Конфигурация Google Gemini не найдена в секции llm.system")
        else:
            print("⚠️ Секция llm.system не найдена")
        
        # Проверяем языковые настройки
        if 'language' in config:
            lang = config['language']
            print(f"🌍 Язык системы: {lang}")
            if lang not in ['ru', 'en']:
                print(f"⚠️ Неизвестный язык: {lang}. Поддерживаются: ru, en")
        
        # Дополнительные проверки
        print("\n📋 Дополнительные проверки:")
        
        # Проверяем наличие секции vosk (если есть)
        if 'vosk' in config:
            vosk_config = config['vosk']
            print("✅ Найдена конфигурация VOSK")
            
            if 'model_path' in vosk_config:
                model_path = Path(vosk_config['model_path'])
                if model_path.exists():
                    print(f"   ✅ Модель VOSK найдена: {model_path}")
                else:
                    print(f"   ⚠️ Модель VOSK не найдена: {model_path}")
        
        # Проверяем наличие секции audio (если есть)
        if 'audio' in config:
            print("✅ Найдена конфигурация аудио")
            audio_config = config['audio']
            if 'sample_rate' in audio_config:
                print(f"   🎵 Частота дискретизации: {audio_config['sample_rate']} Hz")
        
        print("\n🎉 Конфигурация готова к использованию!")
        return True
        
    except yaml.YAMLError as e:
        print(f"❌ Ошибка в YAML синтаксисе: {e}")
        print("💡 Проверьте отступы и синтаксис YAML")
        return False
    except UnicodeDecodeError as e:
        print(f"❌ Ошибка кодировки файла: {e}")
        print("💡 Убедитесь, что файл сохранен в UTF-8")
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
