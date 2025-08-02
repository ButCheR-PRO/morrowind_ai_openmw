#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import yaml
import json
import wave
import tempfile
from pathlib import Path
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config():
    """Загрузка конфигурации"""
    config_path = Path('config.yml')
    
    # Ищем config.yml в текущей и родительских директориях
    if not config_path.exists():
        for parent in Path.cwd().parents:
            potential_config = parent / 'config.yml'
            if potential_config.exists():
                config_path = potential_config
                break
        else:
            logger.warning("⚠️ config.yml не найден")
            return {}
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            logger.info(f"✅ Конфигурация загружена из {config_path}")
            return config or {}
    except Exception as e:
        logger.error(f"❌ Ошибка загрузки конфигурации: {e}")
        return {}

def check_vosk_installation():
    """Проверка установки VOSK"""
    print("🔍 Проверяем установку VOSK...")
    
    try:
        import vosk
        print("✅ Библиотека VOSK импортирована")
        
        # Проверяем версию, если доступна
        if hasattr(vosk, '__version__'):
            print(f"📦 Версия VOSK: {vosk.__version__}")
        
        return vosk
    except ImportError as e:
        print("❌ VOSK не установлен!")
        print("💡 Установите VOSK: pip install vosk")
        print(f"📄 Ошибка: {e}")
        return None

def find_vosk_model(config):
    """Поиск модели VOSK"""
    print("🔍 Ищем модель VOSK...")
    
    # Проверяем в конфигурации
    vosk_config = config.get('vosk', {})
    model_path_from_config = vosk_config.get('model_path')
    
    # Возможные пути для поиска модели
    search_paths = []
    
    if model_path_from_config:
        search_paths.append(Path(model_path_from_config))
    
    # Стандартные места поиска
    search_paths.extend([
        Path("vosk-model-small-ru-0.22"),
        Path("vosk-model-ru-0.22"),
        Path("models/vosk-model-small-ru-0.22"),
        Path("models/vosk-model-ru-0.22"),
        Path("../models/vosk-model-small-ru-0.22"),
        Path("../models/vosk-model-ru-0.22"),
        Path("vosk-model"),
        Path("models/vosk-model")
    ])
    
    for model_path in search_paths:
        print(f"   Проверяем: {model_path}")
        if model_path.exists() and model_path.is_dir():
            print(f"✅ Найдена модель: {model_path}")
            return model_path
    
    print("❌ Модель VOSK не найдена!")
    print("💡 Скачайте модель с: https://alphacephei.com/vosk/models")
    print("📁 Рекомендуемая модель: vosk-model-small-ru-0.22")
    return None

def check_model_structure(model_path):
    """Проверка структуры модели"""
    print(f"🔍 Проверяем структуру модели: {model_path}")
    
    # Обязательные файлы/папки в модели VOSK
    required_items = [
        'am',           # Acoustic model
        'graph',        # Graph
        'ivector',      # Ivector extractor
        'conf',         # Configuration
    ]
    
    # Опциональные файлы
    optional_items = [
        'phones.txt',   # Phones (может отсутствовать в новых моделях)
        'words.txt'     # Words (может отсутствовать в некоторых моделях)
    ]
    
    missing_items = []
    found_items = []
    
    # Проверяем обязательные элементы
    for item_name in required_items:
        item_path = model_path / item_name
        if item_path.exists():
            if item_path.is_dir():
                files_count = len(list(item_path.iterdir()))
                print(f"   ✅ Папка '{item_name}' найдена ({files_count} файлов)")
            else:
                file_size = item_path.stat().st_size
                print(f"   ✅ Файл '{item_name}' найден ({file_size} байт)")
            found_items.append(item_name)
        else:
            print(f"   ❌ Отсутствует: {item_name}")
            missing_items.append(item_name)
    
    # Проверяем опциональные элементы
    for item_name in optional_items:
        item_path = model_path / item_name
        if item_path.exists():
            if item_path.is_dir():
                files_count = len(list(item_path.iterdir()))
                print(f"   ✅ Опциональная папка '{item_name}' найдена ({files_count} файлов)")
            else:
                file_size = item_path.stat().st_size
                print(f"   ✅ Опциональный файл '{item_name}' найден ({file_size} байт)")
        else:
            print(f"   ⚠️ Опциональный файл отсутствует: {item_name}")
    
    # Проверяем общий размер модели
    try:
        total_size = sum(f.stat().st_size for f in model_path.rglob('*') if f.is_file())
        size_mb = total_size / (1024 * 1024)
        print(f"📊 Общий размер модели: {size_mb:.1f} МБ")
        
        if size_mb < 10:
            print("⚠️ Модель кажется слишком маленькой")
        elif size_mb > 2000:
            print("💾 Это большая модель, загрузка может занять время")
        else:
            print("✅ Размер модели в норме")
            
    except Exception as e:
        print(f"⚠️ Не удалось определить размер модели: {e}")
    
    if missing_items:
        print(f"❌ Структура модели неполная!")
        print(f"💥 Отсутствующие критические элементы: {', '.join(missing_items)}")
        print("💡 Переустановите или перескачайте модель")
        return False
    else:
        print("✅ Структура модели корректна")
        # Если отсутствует phones.txt, это не критично для новых моделей
        if not (model_path / 'phones.txt').exists():
            print("💡 Файл phones.txt отсутствует, но это нормально для новых моделей VOSK")
        return True

def test_vosk_loading(vosk_module, model_path, sample_rate=16000):
    """Тест загрузки модели VOSK"""
    print(f"🚀 Тестируем загрузку модели...")
    print(f"📁 Путь: {model_path}")
    print(f"🎵 Частота: {sample_rate} Hz")
    
    try:
        print("⏳ Загружаем модель VOSK...")
        model = vosk_module.Model(str(model_path))
        print("✅ Модель VOSK загружена успешно!")
        
        print("⏳ Создаем распознаватель...")
        recognizer = vosk_module.KaldiRecognizer(model, sample_rate)
        recognizer.SetWords(True)  # Включаем детальную информацию о словах
        print("✅ Распознаватель создан!")
        
        # Информация о модели
        print("📊 Информация о модели:")
        print(f"   🎵 Частота дискретизации: {sample_rate} Hz")
        print(f"   🧠 Модель готова к распознаванию")
        
        return model, recognizer
        
    except Exception as e:
        print(f"❌ Ошибка загрузки модели: {e}")
        print("💡 Возможные причины:")
        print("   - Повреждена модель")
        print("   - Неподходящая версия VOSK")
        print("   - Недостаточно памяти")
        return None, None

def test_recognition(vosk_module, recognizer, sample_rate=16000):
    """Тест распознавания с синтетическим аудио"""
    print("🎤 Тестируем распознавание речи...")
    
    try:
        # Создаем простое тестовое аудио (тишина)
        print("🔧 Создаем тестовое аудио...")
        
        duration = 1.0  # 1 секунда
        samples = int(sample_rate * duration)
        
        # Создаем массив тишины (нули)
        import array
        audio_data = array.array('h', [0] * samples)  # 16-bit integers
        
        # Конвертируем в байты
        audio_bytes = audio_data.tobytes()
        
        print(f"🎵 Тестовое аудио: {len(audio_bytes)} байт, {duration}с")
        
        # Тестируем распознавание
        print("🤖 Тестируем распознаватель...")
        
        # Подаем данные частями
        chunk_size = 4096
        results = []
        
        for i in range(0, len(audio_bytes), chunk_size):
            chunk = audio_bytes[i:i + chunk_size]
            
            if recognizer.AcceptWaveform(chunk):
                result = json.loads(recognizer.Result())
                results.append(result)
        
        # Получаем финальный результат
        final_result = json.loads(recognizer.FinalResult())
        results.append(final_result)
        
        print("✅ Распознавание завершено успешно!")
        print(f"📊 Получено результатов: {len(results)}")
        
        # Показываем результаты
        for i, result in enumerate(results):
            if result.get('text'):
                print(f"   Результат {i+1}: '{result['text']}'")
            else:
                print(f"   Результат {i+1}: (пустой)")
        
        print("✅ Тест распознавания пройден!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования распознавания: {e}")
        return False

def test_vosk():
    """Главная функция тестирования VOSK"""
    print("🔍 ТЕСТИРОВАНИЕ VOSK")
    print("=" * 50)
    
    # Загружаем конфигурацию
    config = load_config()
    
    # 1. Проверяем установку VOSK
    print(f"\n1️⃣ ПРОВЕРКА УСТАНОВКИ")
    vosk_module = check_vosk_installation()
    if not vosk_module:
        return False
    
    # 2. Ищем модель
    print(f"\n2️⃣ ПОИСК МОДЕЛИ")
    model_path = find_vosk_model(config)
    if not model_path:
        return False
    
    # 3. Проверяем структуру модели
    print(f"\n3️⃣ ПРОВЕРКА СТРУКТУРЫ МОДЕЛИ")
    if not check_model_structure(model_path):
        return False
    
    # 4. Тестируем загрузку
    print(f"\n4️⃣ ТЕСТ ЗАГРУЗКИ")
    vosk_config = config.get('vosk', {})
    sample_rate = vosk_config.get('sample_rate', 16000)
    
    model, recognizer = test_vosk_loading(vosk_module, model_path, sample_rate)
    if not model or not recognizer:
        return False
    
    # 5. Тестируем распознавание
    print(f"\n5️⃣ ТЕСТ РАСПОЗНАВАНИЯ")
    if not test_recognition(vosk_module, recognizer, sample_rate):
        return False
    
    return True

def main():
    """Главная функция"""
    try:
        success = test_vosk()
        
        print("\n" + "=" * 50)
        if success:
            print("🎉 VOSK ГОТОВ К РАБОТЕ!")
            print("✅ Все тесты пройдены успешно")
            print("🎤 Система готова к распознаванию речи")
        else:
            print("💥 ПРОБЛЕМЫ С VOSK!")
            print("❌ Некоторые тесты провалены")
            print("🔧 Исправьте ошибки перед использованием")
        print("=" * 50)
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n👋 Тестирование прервано пользователем")
        return 130
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        return 2

if __name__ == "__main__":
    sys.exit(main())
