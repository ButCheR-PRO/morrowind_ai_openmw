import numpy as np
import matplotlib.pyplot as plt

def slerp(p0, p1, t, normal=None):
    dot_product = np.clip(np.dot(p0, p1), -1.0, 1.0)
    omega = np.arccos(dot_product)
    
    if omega == 0:
        return np.array([p0] * len(t))
        
    # Идеальная геодезическая обмотка для полюсов (через центр)
    if np.abs(omega - np.pi) < 1e-5:
        if normal is None:
            # Если не задана нормаль, находим любую ортогональную ось
            if p0[0] == 0: normal = np.array([1, 0, 0])
            elif p0[1] == 0: normal = np.array([0, 1, 0])
            else: normal = np.array([0, 0, 1])
        u = p0
        v = np.cross(normal, p0)
        v = v / np.linalg.norm(v)
        arc = u * np.cos(t * np.pi)[:, None] + v * np.sin(t * np.pi)[:, None]
        return arc
    
    so = np.sin(omega)
    arc = np.outer(np.sin((1.0 - t) * omega) / so, p0) + np.outer(np.sin(t * omega) / so, p1)
    return arc

fig = plt.figure(figsize=(12, 12), facecolor='#050505')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#050505')
ax.grid(False) # Убираем матричную сетку, оставляем только Эфир
ax.set_axis_off()

# Эфирная мембрана (Сфера)
u_grid, v_grid = np.mgrid[0:2*np.pi:40j, 0:np.pi:20j]
x_grid = np.cos(u_grid)*np.sin(v_grid)
y_grid = np.sin(u_grid)*np.sin(v_grid)
z_grid = np.cos(v_grid)
ax.plot_wireframe(x_grid, y_grid, z_grid, color='#222233', alpha=0.15, linewidth=0.5)

# Базовые полуоси (Грани бесконечности)
points = {
    '+X': np.array([1, 0, 0]), '-X': np.array([-1, 0, 0]),
    '+Y': np.array([0, 1, 0]), '-Y': np.array([0, -1, 0]),
    '+Z': np.array([0, 0, 1]), '-Z': np.array([0, 0, -1])
}

# 15 Связей 
arcs =[
    ('+X', '+Y', '#ff3333'), ('+X', '-Y', '#ff8833'), 
    ('-X', '+Y', '#cc0000'), ('-X', '-Y', '#ff5500'),
    
    ('+Y', '+Z', '#33ff33'), ('+Y', '-Z', '#88ff33'), 
    ('-Y', '+Z', '#00cc00'), ('-Y', '-Z', '#55ff00'),
    
    ('+Z', '+X', '#3333ff'), ('+Z', '-X', '#3388ff'), 
    ('-Z', '+X', '#0000cc'), ('-Z', '-X', '#0055ff'),
    
    # Сквозные оси (Нуль-транзит)
    ('+X', '-X', '#ff00ff'), # X-Ось (Пурпур)
    ('+Y', '-Y', '#ffff00'), # Y-Ось (Желтый)
    ('+Z', '-Z', '#00ffff')  # Z-Ось (Циан)
]

t = np.linspace(0, 1, 100)

for p1_name, p2_name, color in arcs:
    p1 = points[p1_name]
    p2 = points[p2_name]
    
    normal = None
    if p1_name[1] == p2_name[1]: 
        # Жесткая ортогональная фиксация дуги
        if p1_name[1] == 'X': normal = np.array([0, 0, 1]) # Дуга над экватором
        elif p1_name[1] == 'Y': normal = np.array([1, 0, 0])
        elif p1_name[1] == 'Z': normal = np.array([1, 0, 0])
        
    arc_pts = slerp(p1, p2, t, normal)
    ax.plot(arc_pts[:,0], arc_pts[:,1], arc_pts[:,2], color=color, linewidth=2.5, alpha=0.9)

for name, p in points.items():
    ax.scatter(*p, color='white', s=120, zorder=5)
    # Смещение текста от полюсов для читаемости
    ax.text(p[0]*1.15, p[1]*1.15, p[2]*1.15, name, color='white', fontsize=14, weight='bold', ha='center', va='center')

ax.view_init(elev=20., azim=55) # Угол, чтобы прочитать всю топологию разом
plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
print("Запуск графики: Структура из 6 граней и 15 связей (15x24=360)")
plt.show()