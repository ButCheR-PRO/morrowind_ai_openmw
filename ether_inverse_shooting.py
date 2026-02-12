# ether_inverse_shooting.py
# Proof-of-concept GRIN ray tracer + inverse shooting optimizer
# Required: python -m pip install numpy scipy matplotlib
# Usage: python ether_inverse_shooting.py
import numpy as np
from math import atan2
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# Model geometry (normalized units)
R_dome = 1.0           # rim radius (normalized)
r_obs = 0.5            # observer radial coordinate
observer_angle = 0.0   # we place observer on +x axis for symmetry

# GRIN profile family: n(r) = 1 + A*(cosh(r/R) - 1)
def make_n_profile(A, Rscale):
    def n_func(x, y):
        r = np.hypot(x, y)
        return 1.0 + A*(np.cosh(r / Rscale) - 1.0)
    def grad_n(x, y):
        r = np.hypot(x, y)
        if r == 0: return (0.0, 0.0)
        dn_dr = A*(np.sinh(r / Rscale) / Rscale)
        return (dn_dr * x / r, dn_dr * y / r)
    return n_func, grad_n

def ray_ode(s, state, n_func, grad_n):
    x, y, vx, vy = state
    n = n_func(x, y)
    gx, gy = grad_n(x, y)
    v = np.array([vx, vy])
    g = np.array([gx, gy])
    vdotg = vx*gx + vy*gy
    dvds = (g - v * vdotg) / n
    return [vx, vy, dvds[0], dvds[1]]

def trace_ray_from_source(theta_source, A, Rscale, initial_tilt=0.0, max_s=50.0):
    x0 = R_dome * np.cos(theta_source)
    y0 = R_dome * np.sin(theta_source)
    # initial direction: toward center with optional small tilt
    dir0 = np.array([-x0, -y0])
    dir0 = dir0 / np.linalg.norm(dir0)
    c, s = np.cos(initial_tilt), np.sin(initial_tilt)
    vx0 = c*dir0[0] - s*dir0[1]
    vy0 = s*dir0[0] + c*dir0[1]
    state0 = [x0, y0, vx0, vy0]
    n_func, grad_n = make_n_profile(A, Rscale)
    
    # ВОТ ЗДЕСЬ ПРАВКА: добавили *args
    def stop_event(t, state, *args):
        x, y = state[0], state[1]
        return np.hypot(x, y) - r_obs
        
    stop_event.terminal = True
    stop_event.direction = -1
    # Передаем args в solve_ivp
    sol = solve_ivp(ray_ode, [0, max_s], state0, args=(n_func, grad_n), events=[stop_event], max_step=0.02, rtol=1e-6)
    if sol.status == 1 and len(sol.t_events[0])>0:
        x_e, y_e, vx_e, vy_e = sol.y_events[0][0]
        inc_angle = atan2(vy_e, vx_e)  # global incoming direction
        return True, (x_e, y_e, vx_e, vy_e, inc_angle), sol
    return False, None, sol

# Forward test: visualize rays for given A,R
def plot_forward(A, Rscale, n_rays=36):
    thetas = np.linspace(-np.pi, np.pi, n_rays, endpoint=False)
    plt.figure(figsize=(6,6))
    thplot = np.linspace(0,2*np.pi,400)
    plt.plot(R_dome*np.cos(thplot), R_dome*np.sin(thplot), 'k--', label='dome rim')
    plt.plot(r_obs*np.cos(thplot), r_obs*np.sin(thplot), 'b--', label='observer radius')
    for th in thetas:
        ok, res, sol = trace_ray_from_source(th, A, Rscale)
        if sol.y.shape[1] > 0:
            plt.plot(sol.y[0,:], sol.y[1,:], '-', alpha=0.6)
    plt.gca().set_aspect('equal')
    plt.title(f"Ray traces A={A}, R={Rscale}")
    plt.show()

# Inverse problem: pick several source points on rim and want incoming angles to match target
def objective_params(p, source_angles, target_angle):
    A, Rscale = p
    # penalty if params out of sensible bounds
    if A <= 0 or Rscale <= 0:
        return 1e6 + abs(A) * 1e5 + abs(Rscale) * 1e5
    angles = []
    for th in source_angles:
        ok, res, sol = trace_ray_from_source(th, A, Rscale)
        if not ok:
            # heavy penalty if ray misses observer radius
            return 1e4
        angles.append(res[4])  # incoming global angle
    # map incoming angles to relative angles wrt observer tangent
    # target_angle expected in radians
    diffs = [(ang - target_angle) for ang in angles]
    # reduce periodicity
    diffs = [(d + np.pi) % (2*np.pi) - np.pi for d in diffs]
    J = np.sum(np.array(diffs)**2)
    return float(J)

def run_inverse_demo():
    # pick source sample (a sector towards the "south" relative to observer at +x)
    source_angles = np.linspace(-0.6*np.pi, -0.4*np.pi, 7)  # example
    # target: incoming direction for those rays (approx towards -x i.e. pi)
    target_angle = np.pi  # illustrative
    # initial guess
    p0 = np.array([1.0, 0.3])
    res = minimize(objective_params, p0, args=(source_angles, target_angle), method='Nelder-Mead',
                   options={'maxiter': 50, 'xatol':1e-3, 'fatol':1e-3})
    print("Optimization result:", res)
    return res

if __name__ == "__main__":
    print("Forward demo plot (example parameters):")
    plot_forward(A=1.0, Rscale=0.3)
    print("Running inverse demo (may take time):")
    res = run_inverse_demo()
    print("Inverse demo finished:", res)
