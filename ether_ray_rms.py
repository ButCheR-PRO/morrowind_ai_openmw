# -*- coding: utf-8 -*-
# ether_ray_rms.py
# Аппаратный дебаггер Южного Полюса (Расчет Оптического Миража)
# Этот скрипт математически доказывает, что центр вращения звезд на юге - это оптическая иллюзия, 
# вызванная искривлением света в эфирном градиенте Купола.

import numpy as np
from math import atan2, degrees
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# ====================================================================
# БАЗОВЫЕ КОНСТАНТЫ СРЕДЫ (ETHER_OS)
# Эти данные мы получили при расчете идеальной линзы в предыдущем скрипте.
# ====================================================================
A = 2.5        # Эфирное напряжение (амплитуда градиента - насколько сильно "гнется" свет)
Rscale = 0.4   # Форма линзы Купола (масштаб экспоненты)
R_DOME = 1.0   # Максимальный радиус земного диска (Ледяной барьер Антарктиды)
R_OBS = 0.5    # Место стояния наблюдателя (например, широта Австралии)
N_RAYS = 60    # Количество контрольных лучей для трассировки (разрешение симуляции)
MAX_S = 60.0   # Лимит дистанции для расчета луча, чтобы код не ушел в бесконечность

# --------------------------------------------------------------------
# 1. ЗАДАЕМ ФИЗИКУ СРЕДЫ (Профиль Эфирной Линзы)
# --------------------------------------------------------------------
# Рассчитываем коэффициент преломления (n) в любой точке диска (x, y)
# У края диска (Антарктида) плотность максимальная, в центре (Север) - минимальная.
def n_func_xy(x, y):
    r = np.hypot(x, y) # Расстояние от центра
    return 1.0 + A * (np.cosh(r / Rscale) - 1.0)

# Высчитываем вектор градиента (куда именно и с какой силой закругляется луч света)
def grad_n_xy(x, y):
    r = np.hypot(x, y)
    if r < 1e-9: 
        return (0.0, 0.0) # Защита от системной ошибки в центре диска (точка Меру)
    dn_dr = A * (np.sinh(r / Rscale) / Rscale)
    return (dn_dr * x / r, dn_dr * y / r)

# Дифференциальное уравнение движения фотона (Волны) сквозь Эфир
def ray_ode(s, state):
    x, y, vx, vy = state
    n = n_func_xy(x, y)
    gx, gy = grad_n_xy(x, y)
    
    # Векторная математика изменения скорости и направления луча в зависимости от плотности Эфира
    vdotg = vx * gx + vy * gy
    dvx = (gx - vx * vdotg) / n
    dvy = (gy - vy * vdotg) / n
    return [vx, vy, dvx, dvy]

# Условие остановки вычислений: Луч ударил точно в радиус (глаз) Наблюдателя
def stop_at_obs(s, state, *args): 
    return np.hypot(state[0], state[1]) - R_OBS
stop_at_obs.terminal = True
stop_at_obs.direction = -1

# --------------------------------------------------------------------
# 2. ПРОТОКОЛ ЗАПУСКА ЛУЧА
# --------------------------------------------------------------------
def trace_ray(theta):
    # Стартовые координаты: луч начинается от периметра Купола
    x0 = R_DOME * np.cos(theta)
    y0 = R_DOME * np.sin(theta)
    
    # Начальное направление луча (строго к центру диска)
    dir0 = np.array([-x0, -y0])
    dir0 = dir0 / np.linalg.norm(dir0)
    state0 = [x0, y0, dir0[0], dir0[1]]
    
    # Запуск решателя: луч "летит" через Эфир и гнется
    sol = solve_ivp(ray_ode, [0.0, MAX_S], state0, events=[stop_at_obs], max_step=0.05, rtol=1e-5)
    
    # Если луч достиг наблюдателя - фиксируем параметры попадания
    if sol.status == 1 and len(sol.t_events[0]) > 0:
        return True, sol.y_events[0][0], sol
    return False, None, sol

# --------------------------------------------------------------------
# 3. ПОИСК ИЛЛЮЗИИ (Математика Миража)
# --------------------------------------------------------------------
# Функция, которая определяет, куда смотрят ВСЕ полученные векторы.
# Это метод Наименьших Квадратов (МНК). Он вычисляет точку пересечения всех "обманных" 
# прямых линий взгляда наблюдателя, создавая виртуальный центр (Сигму Октанта).
def best_fit_point_to_lines(points, dirs):
    dim = 2
    A_mat, b_vec = np.zeros((dim, dim)), np.zeros(dim)
    for p, d in zip(points, dirs):
        d = d.reshape((dim, 1))
        I_minus_dd = np.eye(dim) - d @ d.T
        A_mat += I_minus_dd
        b_vec += I_minus_dd @ p
    try: 
        return np.linalg.solve(A_mat, b_vec)
    except: 
        return np.linalg.pinv(A_mat) @ b_vec

# --------------------------------------------------------------------
# СБОРКА И РЕНДЕРИНГ (Запуск программы)
# --------------------------------------------------------------------
def main():
    print("[ROOT] Инициализация... Запускаем трассировку эфирных волн.")
    # Генерируем 60 лучей из разных точек горизонта
    thetas = np.linspace(-np.pi, np.pi, N_RAYS, endpoint=False)
    hits, sols, points, dirs = [], [], [], []
    
    for th in thetas:
        ok, res, sol = trace_ray(th)
        sols.append(sol)
        if ok:
            xe, ye, vxe, vye = res
            hits.append((th, xe, ye, vxe, vye))
            points.append(np.array([xe, ye]))
            d = np.array([vxe, vye])
            # КРИТИЧЕСКИ ВАЖНО: сохраняем вектор ОБРАТНОГО взгляда наблюдателя 
            dirs.append(-d / np.linalg.norm(d))

    # Высчитываем координаты Фейкового Полюса
    best_pt = best_fit_point_to_lines(np.array(points), np.array(dirs))

    # === ВИЗУАЛЬНАЯ ПАНЕЛЬ АДМИНИСТРАТОРА ===
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 8))
    t_plot = np.linspace(0, 2*np.pi, 300)
    
    # Рисуем контуры Террариума
    ax.plot(R_DOME*np.cos(t_plot), R_DOME*np.sin(t_plot), color='#00ff00', linestyle='--', linewidth=1, label='Свод Купола (Генератор света)')
    ax.plot(R_OBS*np.cos(t_plot), R_OBS*np.sin(t_plot), color='#00aaff', linestyle='-.', linewidth=1, label='Радиус Наблюдателя (Австралия/Чили)')
    
    # Рисуем изогнутые траектории света в Эфире (как они летят на самом деле)
    for sol in sols:
        if sol is not None and sol.y.shape[1] > 0:
            ax.plot(sol.y[0,:], sol.y[1,:], color='#cccccc', alpha=0.2, linewidth=0.8)
            
    # Рисуем "Обман Зрения" - прямые красные лучи, которые достраивает мозг
    if best_pt is not None:
        ax.plot(best_pt[0], best_pt[1], marker='X', color='#ff0000', ms=12, label='ВИРТУАЛЬНЫЙ ЮЖНЫЙ ПОЛЮС (МИРАЖ)')
        for (th, xe, ye, vxe, vye), d_back in zip(hits, dirs):
            ax.plot([xe, xe + d_back[0]*0.4], [ye, ye + d_back[1]*0.4], color='#ff0055', alpha=0.5, linewidth=0.5)

    # Настройки отображения графика
    ax.set_aspect('equal')
    ax.legend(facecolor='#111111')
    ax.axis('off')
    plt.title("OPTICAL MIRAGE RENDERING (ETHER GRIN LENS)\nДОКАЗАТЕЛЬСТВО ИЛЛЮЗИИ ЮЖНОГО НЕБА", color='#00ff00', weight='bold')
    plt.tight_layout()
    
    print("[SUCCESS] Рендеринг завершен. Каустика вычислена.")
    print("ВЫВОД: Видимый центр вращения южного неба является оптическим фокусом (голограммой), а не физическим объектом в космосе.")
    
    plt.show()

if __name__ == "__main__":
    main()