# -*- coding: utf-8 -*-
# ether_music.py
# Акустическая визуализация Архитектуры Пространства 0³
# Рендеринг траектории тороида через 306 состояний на базу 243 Гц

import numpy as np
from scipy.io import wavfile

# === ПАРАМЕТРЫ ЭФИРНОГО СЕКВЕНСОРА ===
SAMPLE_RATE = 44100
MODULE_STEPS = 306        # Полный динамический цикл (от -153 до +153)
BASE_FREQ = 243.0         # Опорная частота статики куба (81 * 3)
STEP_DUR = 0.12           # Длительность одного шага (сек). Темп шага.
TOTAL_DUR = MODULE_STEPS * STEP_DUR

# 14-интервальный строй Мишина (чистые эфирные дроби, без эвклидовой температуры)
MISHIN_RATIOS = [
    1.0,        # До (База)
    9/8,        # Ре
    6/5,        # Ми бемоль
    5/4,        # Ми
    4/3,        # Фа
    3/2,        # Соль (Квинта - чистая точка баланса)
    5/3,        # Ля
    15/8,       # Си
    2.0         # Октава
]

def generate_xylophone_hit(freq, duration, sample_rate=44100):
    """Генерация единичного эфирного 'удара' с имплозийным (экспоненциальным) затуханием"""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # Синтез волны: основа + чистая квинта + октава (для эффекта хрустального звона)
    signal = np.sin(2 * np.pi * freq * t) + \
             0.5 * np.sin(2 * np.pi * (freq * 3/2) * t) + \
             0.25 * np.sin(2 * np.pi * (freq * 2.0) * t)
    
    # Экспоненциальный спад: имитация акустического резонатора (удар в колокол/ксилофон)
    envelope = np.exp(-5.0 * t)
    return signal * envelope

def compile_ether_track():
    print("[ROOT] Инициализация Эфирного Секвенсора 0³...")
    print(f"Базовая частота: {BASE_FREQ} Гц | Модуль: {MODULE_STEPS} шагов")
    
    track = np.zeros(int(SAMPLE_RATE * TOTAL_DUR))
    
    # Проход по 306 шагам: от схлопывания (-153) к балансу (0) и распространению (+153)
    for step_raw in range(-153, 153):
        # Нормализуем текущий шаг для массивов
        step = step_raw + 153
        
        # Вычисляем фазу текущего шага в полном цикле тороида
        phase = step / float(MODULE_STEPS)
        
        # Архитектура: Траектория проходит 8 октантов за цикл.
        angle = phase * 2 * np.pi * 8 
        
        # Логика детекта: Синус (проникновение) и Косинус (расширение)
        # проецируются на нашу гребенку частот, задавая "ноту" для этой координаты
        idx_x = int(abs(np.sin(angle)) * len(MISHIN_RATIOS)) % len(MISHIN_RATIOS)
        idx_y = int(abs(np.cos(angle + np.pi/4)) * len(MISHIN_RATIOS)) % len(MISHIN_RATIOS)
        
        freq_x = BASE_FREQ * MISHIN_RATIOS[idx_x]
        freq_y = BASE_FREQ * MISHIN_RATIOS[idx_y] * 2.0 # Ось Y играет на октаву выше
        
        # Рендерим звук
        hit_x = generate_xylophone_hit(freq_x, STEP_DUR * 5) # Хвост звучит дольше шага (переливание)
        hit_y = generate_xylophone_hit(freq_y, STEP_DUR * 3)
        
        # Высчитываем точку вставки в глобальный трек
        start_idx = int(step * STEP_DUR * SAMPLE_RATE)
        
        # Микшируем оси (эффект полифонии)
        end_idx_x = min(start_idx + len(hit_x), len(track))
        track[start_idx:end_idx_x] += hit_x[:end_idx_x - start_idx]
        
        end_idx_y = min(start_idx + len(hit_y), len(track))
        track[start_idx:end_idx_y] += hit_y[:end_idx_y - start_idx] * 0.45

    # Нормализация против клиппинга
    print("[ROOT] Применяю лимитер громкости...")
    track = track / np.max(np.abs(track))
    track_int16 = np.int16(track * 32767)
    
    out_file = 'ether_resonance_0_3.wav'
    wavfile.write(out_file, SAMPLE_RATE, track_int16)
    print(f"[SUCCESS] Музыка Сфер скомпилирована. Слушай файл: {out_file}")

if __name__ == '__main__':
    compile_ether_track()