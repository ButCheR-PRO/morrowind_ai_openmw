# -*- coding: utf-8 -*-
# ether_graph1.py
# Аппаратная визуализация Динамики Эфира (Фрактал 0³)
# Доказательство точки абсолютного равновесия 22.5 градусов

import math
from PIL import Image, ImageDraw

# === БАЗОВЫЕ НАСТРОЙКИ СИСТЕМЫ ===
IMG_SIZE = 2048

# Эталонный квант шага. В геометрии эфира шаг фиксирован.
# Динамика рождается из изменения угла, а не из удлинения самой связи.
SEG_LEN = 16            

# Фазовые сдвиги эфирной структуры (выведены из правила заточки сверла 135 градусов).
# 22.5 градуса - это точка идеального баланса, половина системного шага в 45 градусов.
# В этой точке продольное проникновение (sin) уравновешено радиальным расширением (cos).
# sin(22.5) = cos(67.5). Тор скользит без сопротивления среды.
ANGLE_A = math.radians(22.5)   # Фаза вхождения (Синус)
ANGLE_B = math.radians(-67.5)  # Фаза расширения (Косинус)

COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 50)
BG_COLOR = (5, 5, 5)

# Системный лимит развертки цикла
# 306 - это не градусы. Это жесткий аппаратный предел количества ветвлений (тактов)
# детекта изнутри системы, при котором замыкается фрактальная петля без ухода в хаос.
MAX_STICKS = 306 

def generate_fractal():
    # Нулевая точка (0³). Место Наблюдателя, старт развертки системы.
    cx, cy = IMG_SIZE // 2, IMG_SIZE - 200
    start_angle = math.radians(-90) # Вектор устремлен прямо
    
    segments = []
    
    # Нулевой такт (Корень фрактала)
    x1 = cx + SEG_LEN * math.cos(start_angle)
    y1 = cy + SEG_LEN * math.sin(start_angle)
    
    # Структура: (x_начало, y_начало, x_конец, y_конец, уровень_вложенности)
    segments.append((cx, cy, x1, y1, 0))
    
    # Буфер активных узлов для следующего такта ветвления
    active = [(x1, y1, start_angle, 0)]
    
    # Разворачиваем геометрию строго по уровням (октавам 2^n), 
    # пока не упремся в лимит 306 тактов
    while len(segments) < MAX_STICKS and active:
        next_active = []
        for xp, yp, ang, lvl in active:
            
            # В каждой точке происходит разделение на 2 фазы (+22.5 и -67.5)
            # Это и есть перетекание синуса в косинус
            for off in (ANGLE_A, ANGLE_B):
                if len(segments) >= MAX_STICKS:
                    break
                
                na = ang + off
                xn = xp + SEG_LEN * math.cos(na)
                yn = yp + SEG_LEN * math.sin(na)
                
                new_lvl = lvl + 1
                segments.append((xp, yp, xn, yn, new_lvl))
                next_active.append((xn, yn, na, new_lvl))
                
        active = next_active
        
    return segments

def draw_fractal(segments):
    img = Image.new('RGB', (IMG_SIZE, IMG_SIZE), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    for x0, y0, x1, y1, lvl in segments:
        # Цвет переключается как маркер смены фаз (проникновение / расширение).
        # Поуровневое чередование цветов доказывает прохождение Стенки Блоха
        # и смену знаковых состояний внутри октантов.
        color = COLOR_WHITE if lvl % 2 == 0 else COLOR_GREEN
        draw.line([(x0, y0), (x1, y1)], fill=color, width=2)
    
    out_name = 'ether_dynamics_306.png'
    img.save(out_name)
    print(f'[SUCCESS] Динамика Эфира скомпилирована: {out_name} | Отрендерено шагов: {len(segments)}')

if __name__ == '__main__':
    segs = generate_fractal()
    draw_fractal(segs)