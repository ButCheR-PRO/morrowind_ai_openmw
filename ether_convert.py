# -*- coding: utf-8 -*-
# ether_convert.py
# Аппаратный аудио-конвертер Эфирных частот через локальный FFmpeg

import subprocess
import os

def convert_audio(input_file):
    if not os.path.exists(input_file):
        print(f"❌ ОШИБКА: Исходный файл {input_file} не найден!")
        return

    # Целевой формат (mp3 с высоким битрейтом 320k, чтобы не порезать наши гармоники)
    output_mp3 = os.path.splitext(input_file)[0] + ".mp3"
    
    # Ищем ffmpeg (локальный в приоритете)
    ffmpeg_cmd = "ffmpeg"
    if os.path.exists("ffmpeg.exe"):
        ffmpeg_cmd = ".\\ffmpeg.exe"
    
    # Команда сборки: конвертация WAV -> MP3 (320kbps, Stereo/Mono сохраняется)
    command_mp3 = [
        ffmpeg_cmd,
        "-i", input_file,
        "-c:a", "libmp3lame",
        "-b:a", "320k",
        "-y",  # Перезаписываем, если файл уже есть
        output_mp3
    ]
    
    print("--- ЗАПУСК КОМПИЛЯЦИИ ---")
    print(f"Исходник: {input_file}")
    
    try:
        # Генерируем MP3
        print("Конвертирую в MP3 (высшее качество)...")
        subprocess.run(command_mp3, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if os.path.exists(output_mp3):
            size_mb = os.path.getsize(output_mp3) / (1024 * 1024)
            print(f"✅ УСПЕШНО: {output_mp3} создан (Размер: {size_mb:.2f} Мб)")
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ ФАТАЛЬНАЯ ОШИБКА FFmpeg: {e}")
    except FileNotFoundError:
        print("\n❌ ОШИБКА: ffmpeg.exe не найден. Кинь его в папку со скриптом.")

if __name__ == "__main__":
    # Имя нашего базового эфирного трека
    target_file = "ether_resonance_0_3.wav"
    convert_audio(target_file)