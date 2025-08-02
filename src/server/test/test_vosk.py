#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

def test_vosk():
    print("🔍 Тестируем VOSK...")
    
    try:
        import vosk
        print("✅ Библиотека VOSK импортирована")
    except ImportError:
        print("❌ VOSK не установлен! Запусти: pip install vosk")
        return False
    
    # Проверяем модель
    model_path = "vosk-model-small-ru-0.22"
    if not os.path.exists(model_path):
        print(f"❌ Модель не найдена: {model_path}")
        print("Скачай с https://alphacephei.com/vosk/models")
        return False
    
    # Проверяем структуру модели
    required_dirs = ['am', 'graph', 'ivector', 'conf']
    for dir_name in required_dirs:
        if not os.path.exists(os.path.join(model_path, dir_name)):
            print(f"❌ Отсутствует папка: {model_path}/{dir_name}")
            print("Модель повреждена или не полностью распакована!")
            return False
    
    print("✅ Структура модели корректна")
    
    try:
        print("Loading VOSK model...")
        model = vosk.Model(model_path)
        print("✅ VOSK модель загружена успешно!")
        print("📊 Размер словаря: ~50,000+ русских слов")
        print("🎤 Готов к распознаванию русской речи!")
        return True
    except Exception as e:
        print(f"❌ Ошибка загрузки модели: {e}")
        return False

if __name__ == "__main__":
    success = test_vosk()
    print("\n" + "="*50)
    if success:
        print("🎉 VOSK ГОТОВ К РАБОТЕ!")
    else:
        print("💥 ПРОБЛЕМЫ С VOSK!")
    print("="*50)
