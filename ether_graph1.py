import math
from PIL import Image, ImageDraw

# Параметры холста и базы
IMG_SIZE = 2048
SEG_LEN = 16
# Фазовые сдвиги эфирной структуры
ANGLE_A = math.radians(22.5)
ANGLE_B = math.radians(-67.5)

COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 50)
BG_COLOR = (5, 5, 5)

MAX_STICKS = 306  # Заданный предел (Количество эфирных тактов)

def generate_fractal():
    cx, cy = IMG_SIZE // 2, IMG_SIZE - 200
    start_angle = math.radians(-90)
    
    segments = []
    # Нулевой такт (Корень)
    x1 = cx + SEG_LEN * math.cos(start_angle)
    y1 = cy + SEG_LEN * math.sin(start_angle)
    segments.append((cx, cy, x1, y1, 0))
    active = [(x1, y1, start_angle, 0)]
    
    while len(segments) < MAX_STICKS and active:
        next_active = []
        for xp, yp, ang, lvl in active:
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
        # Цвет переключается как маркер смены фаз (проникновение / расширение)
        color = COLOR_WHITE if lvl % 2 == 0 else COLOR_GREEN
        draw.line([(x0, y0), (x1, y1)], fill=color, width=2)
    
    out_file = 'ether_dynamics_306.png'
    img.save(out_file)
    print(f'Матрица скомпилирована: {out_file} | Шагов (Сегментов): {len(segments)}')

if __name__ == '__main__':
    segs = generate_fractal()
    draw_fractal(segs)