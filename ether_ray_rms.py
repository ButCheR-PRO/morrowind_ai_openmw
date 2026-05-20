
# -*- coding: utf-8 -*-
# ether_ray_rms.py
# Оценка погрешности каустики (RMS)
# Доказываем физику виртуального центра светил над плоским диском

import numpy as np
from math import atan2, degrees
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# ----------------- БАЗОВЫЕ НАСТРОЙКИ СИСТЕМЫ -----------------
A = 2.5        # Эфирное напряжение (амплитуда градиента n)
Rscale = 0.4   # Форма линзы
R_DOME = 1.0   # Максимальный радиус диска
R_OBS = 0.5    # Место стояния наблюдателя
N_RAYS = 90    # Количество трассировок
MAX_S = 60.0   # Глубина вычислений
# -------------------------------------------------------------

def n_func_xy(x, y):
    r = np.hypot(x, y)
    return 1.0 + A * (np.cosh(r / Rscale) - 1.0)

def grad_n_xy(x, y):
    r = np.hypot(x, y)
    if r < 1e-9: return (0.0, 0.0)
    dn_dr = A * (np.sinh(r / Rscale) / Rscale)
    return (dn_dr * x / r, dn_dr * y / r)

def ray_ode(s, state):
    x, y, vx, vy = state
    n = n_func_xy(x, y)
    gx, gy = grad_n_xy(x, y)
    vdotg = vx * gx + vy * gy
    dvx = (gx - vx * vdotg) / n
    dvy = (gy - vy * vdotg) / n
    return [vx, vy, dvx, dvy]

def stop_event_factory(r_target):
    def stop_event(s, state):
        return np.hypot(state[0], state[1]) - r_target
    stop_event.terminal = True
    stop_event.direction = -1
    return stop_event

stop_at_obs = stop_event_factory(R_OBS)

def trace_ray(theta, initial_tilt=0.0):
    x0 = R_DOME * np.cos(theta)
    y0 = R_DOME * np.sin(theta)
    dir0 = np.array([-x0, -y0])
    dir0 = dir0 / np.linalg.norm(dir0)
    c, s = np.cos(initial_tilt), np.sin(initial_tilt)
    vx0 = c*dir0[0] - s*dir0[1]
    vy0 = s*dir0[0] + c*dir0[1]
    
    state0 = [x0, y0, vx0, vy0]
    sol = solve_ivp(ray_ode, [0.0, MAX_S], state0, events=[stop_at_obs], max_step=0.05, rtol=1e-6, atol=1e-9)
    if sol.status == 1 and len(sol.t_events[0]) > 0:
        xe, ye, vxe, vye = sol.y_events[0][0]
        return True, (xe, ye, vxe, vye), sol
    return False, None, sol

# МНК для поиска Виртуальной Точки Фокуса (Мираж Сигмы Октанта)
def best_fit_point_to_lines(points, dirs):
    n = len(points)
    if n == 0: return None
    dim = 2
    A_mat = np.zeros((dim, dim))
    b_vec = np.zeros(dim)
    for p, d in zip(points, dirs):
        d = d.reshape((dim, 1))
        I_minus_dd = np.eye(dim) - d @ d.T
        A_mat += I_minus_dd
        b_vec += I_minus_dd @ p
    try:
        return np.linalg.solve(A_mat, b_vec)
    except np.linalg.LinAlgError:
        return np.linalg.pinv(A_mat) @ b_vec

def main():
    print("[ROOT] Сканирование оптического преломления эфира...")
    thetas = np.linspace(-np.pi, np.pi, N_RAYS, endpoint=False)
    hits, sols, points, dirs, rel_angles = [], [], [], [], []
    
    for th in thetas:
        ok, res, sol = trace_ray(th)
        sols.append(sol)
        if ok:
            xe, ye, vxe, vye = res
            hits.append((th, xe, ye, vxe, vye))
            rad = np.array([xe, ye]) / np.hypot(xe, ye)
            tangent = np.array([-rad[1], rad[0]])
            inc = atan2(vye, vxe)
            rel = inc - atan2(tangent[1], tangent[0])
            rel = (rel + np.pi) % (2*np.pi) - np.pi
            rel_angles.append(degrees(rel))
            points.append(np.array([xe, ye]))
            d = np.array([vxe, vye])
            dirs.append(-d / np.linalg.norm(d))  # Обратная проекция

    points_arr = np.array(points)
    dirs_arr = np.array(dirs)
    best_pt = best_fit_point_to_lines(points_arr, dirs_arr)

    # Статистика Иллюзии
    nmax = n_func_xy(R_DOME, 0.0)
    print("\n=== ОТЧЕТ ЭФИРНОГО АУДИТОРА ===")
    print(f"Индекс уплотнения эфира на краю диска (R_DOME): {nmax:.4f}")
    print(f"Сходимость лучей: {len(hits)} из {N_RAYS} достигли оператора")
    print(f"RMS угловое отклонение: {np.sqrt(np.mean(np.array(rel_angles)**2)):.4f} градусов")
    
    if best_pt is not None:
        print(f"КОРДИНАТЫ ВИРТУАЛЬНОГО ФОКУСА (Фейковый полюс): X={best_pt[0]:.4f}, Y={best_pt[1]:.4f}")
        print("Вердикт: Иллюзия наличия южного центра вращения звёзд математически валидна.\n")

    # Графика (Matrix Radar UI)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 8))
    theta_plot = np.linspace(0, 2*np.pi, 400)
    
    ax.plot(R_DOME*np.cos(theta_plot), R_DOME*np.sin(theta_plot), color='#00ff00', linestyle='--', linewidth=1, label='Свод Купола')
    ax.plot(R_OBS*np.cos(theta_plot), R_OBS*np.sin(theta_plot), color='#0088ff', linestyle='-.', linewidth=1, label='Радиус Наблюдателя')
    
    # Отрисовка эфирных волн
    for sol in sols:
        if sol is not None and sol.y.shape[1] > 0:
            ax.plot(sol.y[0,:], sol.y[1,:], color='#cccccc', alpha=0.3, linewidth=0.8)
            
    # Виртуальная каустика (где сходится фокус)
    if best_pt is not None:
        ax.plot(best_pt[0], best_pt[1], marker='X', color='#ff0000', ms=12, label='ВИРТУАЛЬНЫЙ ПОЛЮС')
        for (th, xe, ye, vxe, vye), d_back in zip(hits, dirs):
            ax.plot(xe, ye, 'o', color='#ffff00', ms=2)
            # Вектор обмана зрения
            ax.plot([xe, xe + d_back[0]*0.4], [ye, ye + d_back[1]*0.4], color='#ff0055', alpha=0.6, linewidth=0.5)

    ax.set_aspect('equal')
    ax.legend(facecolor='#111111')
    ax.axis('off')
    ax.set_title("OPTICAL MIRAGE RENDERING (ETHER GRIN LENS)", color='#00ff00', weight='bold')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()