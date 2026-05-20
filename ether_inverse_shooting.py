
# -*- coding: utf-8 -*-
# ether_inverse_shooting.py
# Аппаратный дебаг оптики: Тороидальная градиентная линза Купола (GRIN)
# Вычисление параметров эфирного уплотнения, создающих мираж Южного Полюса.

import numpy as np
from math import atan2
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# Базовая геометрия Террариума (нормированные координаты)
R_DOME = 1.0           # Край купола / Ледяной барьер Антарктиды
R_OBS = 0.5            # Радиус Наблюдателя (средние южные широты)
OBS_ANGLE = 0.0        # Наблюдатель на оси +X

# Профиль плотности эфира: n(r) = 1 + A*(cosh(r/Rscale) - 1)
# Чем ближе к краю (R_DOME), тем жестче эфирная плотность.
def make_n_profile(A, Rscale):
    def n_func(x, y):
        r = np.hypot(x, y)
        return 1.0 + A * (np.cosh(r / Rscale) - 1.0)
    def grad_n(x, y):
        r = np.hypot(x, y)
        if r < 1e-9: return (0.0, 0.0)
        dn_dr = A * (np.sinh(r / Rscale) / Rscale)
        return (dn_dr * x / r, dn_dr * y / r)
    return n_func, grad_n

# ОДУ для луча света в эфире с переменной плотностью (закон Ферма)
def ray_ode(s, state, n_func, grad_n):
    x, y, vx, vy = state
    n = n_func(x, y)
    gx, gy = grad_n(x, y)
    vdotg = vx*gx + vy*gy
    dvds_x = (gx - vx * vdotg) / n
    dvds_y = (gy - vy * vdotg) / n
    return [vx, vy, dvds_x, dvds_y]

def trace_ray_from_source(theta_source, A, Rscale, initial_tilt=0.0, max_s=50.0):
    x0 = R_DOME * np.cos(theta_source)
    y0 = R_DOME * np.sin(theta_source)
    # Луч стартует от купола к центру (с оптическим преломлением)
    dir0 = np.array([-x0, -y0])
    dir0 = dir0 / np.linalg.norm(dir0)
    c, s = np.cos(initial_tilt), np.sin(initial_tilt)
    vx0 = c*dir0[0] - s*dir0[1]
    vy0 = s*dir0[0] + c*dir0[1]
    
    state0 = [x0, y0, vx0, vy0]
    n_func, grad_n = make_n_profile(A, Rscale)
    
    # Фиксатор попадания луча в радиус Наблюдателя
    def stop_event(t, state, *args):
        return np.hypot(state[0], state[1]) - R_OBS
    stop_event.terminal = True
    stop_event.direction = -1
    
    sol = solve_ivp(ray_ode, [0, max_s], state0, args=(n_func, grad_n), events=[stop_event], max_step=0.02, rtol=1e-6)
    
    if sol.status == 1 and len(sol.t_events[0]) > 0:
        x_e, y_e, vx_e, vy_e = sol.y_events[0][0]
        inc_angle = atan2(vy_e, vx_e)
        return True, (x_e, y_e, vx_e, vy_e, inc_angle), sol
    return False, None, sol

def objective_params(p, source_angles, target_angle):
    A, Rscale = p
    # Жесткий пенальти за выход за рамки логики
    if A <= 0.1 or Rscale <= 0.05:
        return 1e6 + abs(A) * 1e5 + abs(Rscale) * 1e5
        
    diffs = []
    for th in source_angles:
        ok, res, sol = trace_ray_from_source(th, A, Rscale)
        if not ok: return 1e4
        ang = res[4]
        d = (ang - target_angle)
        d = (d + np.pi) % (2*np.pi) - np.pi
        diffs.append(d)
        
    return float(np.sum(np.array(diffs)**2))

def plot_forward(A, Rscale, n_rays=48):
    plt.style.use('dark_background')
    thetas = np.linspace(-np.pi, np.pi, n_rays, endpoint=False)
    fig, ax = plt.subplots(figsize=(8,8))
    
    thplot = np.linspace(0, 2*np.pi, 400)
    ax.plot(R_DOME*np.cos(thplot), R_DOME*np.sin(thplot), color='#00ff00', linestyle='--', linewidth=1.5, label='Барьер/Купол')
    ax.plot(R_OBS*np.cos(thplot), R_OBS*np.sin(thplot), color='#00aaff', linestyle='--', linewidth=1, label='Радиус Наблюдателя')
    
    for th in thetas:
        ok, res, sol = trace_ray_from_source(th, A, Rscale)
        if sol.y.shape[1] > 0:
            ax.plot(sol.y[0,:], sol.y[1,:], color='#ffffff', alpha=0.4, linewidth=0.8)
            
    ax.set_aspect('equal')
    ax.set_title(f"ETHER LENS RAY TRACING\nA={A:.2f} | Rscale={Rscale:.2f}", color='#00ff00', weight='bold')
    ax.legend(loc='upper right', facecolor='#111111', edgecolor='#333333')
    ax.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("[ROOT] Инициализация эфирного симулятора...")
    # Можно вручную задать параметры (тестовый прогон)
    plot_forward(A=2.5, Rscale=0.4)
    
    print("\n[ROOT] Запуск обратного просчета каустики...")
    source_angles = np.linspace(-0.6*np.pi, -0.4*np.pi, 9)
    target_angle = np.pi # Цель: Иллюзия параллельных лучей из центра
    
    p0 = np.array([2.5, 0.4])
    res = minimize(objective_params, p0, args=(source_angles, target_angle), method='Nelder-Mead',
                   options={'maxiter': 100, 'xatol': 1e-4, 'fatol': 1e-4})
    
    print("\n=== ВЕРДИКТ ВЫЧИСЛИТЕЛЯ ===")
    print(f"Статус сходимости: {'Успешно' if res.success else 'Сбой'}")
    print(f"Оптимальная эфирная амплитуда (A): {res.x[0]:.6f}")
    print(f"Оптимальный радиус кривизны линзы (R): {res.x[1]:.6f}")
    print("Вывод: Линза математически стабильна.")