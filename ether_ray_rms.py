#!/usr/bin/env python3
"""
ether_ray_rms.py

Proof-of-concept ray tracer for GRIN toroidal lens profile n(r) = 1 + A*(cosh(r/R)-1)
Computes RMS angular spread of incoming rays at observer radius and fits a best-fit
virtual focus point from back-projected incoming rays.

Requirements:
    numpy, scipy, matplotlib

Run:
    python ether_ray_rms.py

Adjust parameters in the CONFIGURATION section as needed.
"""

import numpy as np
from math import atan2, degrees
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# -------------------- CONFIGURATION --------------------
A = 1.0        # amplitude in n(r)
Rscale = 0.3   # length scale in n(r)
R_dome = 1.0   # dome radius (normalized units)
r_obs = 0.5    # observer radius (normalized units)
n_rays = 61    # number of rays sampled on dome rim
max_s = 60.0   # max ray integration path length
plot_result = True  # set False to skip plotting
# --------------------------------------------------------

# --- refractive index and gradient (axisymmetric) ---
def n_func_xy(x, y):
    r = np.hypot(x, y)
    return 1.0 + A * (np.cosh(r / Rscale) - 1.0)

def grad_n_xy(x, y):
    r = np.hypot(x, y)
    if r == 0.0:
        return (0.0, 0.0)
    dn_dr = A * (np.sinh(r / Rscale) / Rscale)
    return (dn_dr * x / r, dn_dr * y / r)

# --- ray ODE: state = [x, y, vx, vy] where v is direction (not necessarily unit) ---
def ray_ode(s, state):
    x, y, vx, vy = state
    n = n_func_xy(x, y)
    gx, gy = grad_n_xy(x, y)
    vdotg = vx * gx + vy * gy
    dvx = (gx - vx * vdotg) / n
    dvy = (gy - vy * vdotg) / n
    return [vx, vy, dvx, dvy]

# event when crossing observer radius from outside to inside
def stop_event_factory(r_target):
    def stop_event(s, state):
        x, y = state[0], state[1]
        return np.hypot(x, y) - r_target
    stop_event.terminal = True
    stop_event.direction = -1
    return stop_event

stop_at_obs = stop_event_factory(r_obs)

# trace a single ray starting at angle theta on rim with initial direction approx to center
def trace_ray(theta, initial_tilt=0.0):
    x0 = R_dome * np.cos(theta)
    y0 = R_dome * np.sin(theta)
    # initial direction toward center (unit)
    dir0 = np.array([-x0, -y0])
    dir0 = dir0 / np.linalg.norm(dir0)
    # optional tilt rotation (radians)
    c, s = np.cos(initial_tilt), np.sin(initial_tilt)
    vx0 = c*dir0[0] - s*dir0[1]
    vy0 = s*dir0[0] + c*dir0[1]
    state0 = [x0, y0, vx0, vy0]
    sol = solve_ivp(ray_ode, [0.0, max_s], state0, events=[stop_at_obs],
                    max_step=0.05, rtol=1e-6, atol=1e-9)
    if sol.status == 1 and len(sol.t_events[0]) > 0:
        # event state is in sol.y_events[0][0]
        xe, ye, vxe, vye = sol.y_events[0][0]
        return True, (xe, ye, vxe, vye), sol
    else:
        return False, None, sol

# compute best-fit intersection point of lines: minimize sum of squared distances to lines
# each line: point p_i and unit direction d_i
def best_fit_point_to_lines(points, dirs):
    # Solve: sum (I - d d^T) x = sum (I - d d^T) p
    # A x = b
    n = len(points)
    if n == 0:
        return None
    dim = 2
    A_mat = np.zeros((dim, dim))
    b_vec = np.zeros(dim)
    for p, d in zip(points, dirs):
        d = d.reshape((dim,1))
        I_minus_dd = np.eye(dim) - d @ d.T
        A_mat += I_minus_dd
        b_vec += I_minus_dd @ p
    # regularize if near-singular
    try:
        x = np.linalg.solve(A_mat, b_vec)
        return x
    except np.linalg.LinAlgError:
        # fallback: pseudo-inverse
        x = np.linalg.pinv(A_mat) @ b_vec
        return x

# main routine
def main():
    thetas = np.linspace(-np.pi, np.pi, n_rays, endpoint=False)
    hits = []  # store tuples (theta_source, xe, ye, vxe, vye)
    sols = []
    for th in thetas:
        ok, res, sol = trace_ray(th)
        sols.append(sol)
        if ok:
            xe, ye, vxe, vye = res
            hits.append((th, xe, ye, vxe, vye))
    if len(hits) == 0:
        print("No rays hit observer radius. Try increasing max_s or changing initial tilts.")
        return

    # incoming direction angles (global) and relative to local tangent
    inc_angles = []
    rel_angles = []
    points = []
    dirs = []
    for (th, xe, ye, vxe, vye) in hits:
        inc = atan2(vye, vxe)  # radians
        inc_angles.append(inc)
        # local tangent at hit point
        rad = np.array([xe, ye]) / np.hypot(xe, ye)
        tangent = np.array([-rad[1], rad[0]])
        tang_ang = atan2(tangent[1], tangent[0])
        rel = inc - tang_ang
        # normalize
        rel = (rel + np.pi) % (2*np.pi) - np.pi
        rel_angles.append(rel)
        points.append(np.array([xe, ye]))
        # back-projection direction for intersection: we want line going backwards from hit point along incoming vector
        d = np.array([vxe, vye])
        d = d / np.linalg.norm(d)
        # back-project (we use direction pointing backwards into scene)
        d_back = -d
        dirs.append(d_back.reshape(2,))
    # convert to degrees
    inc_deg = np.array([degrees(a) for a in inc_angles])
    rel_deg = np.array([degrees(a) for a in rel_angles])
    mean_inc = np.mean(inc_deg)
    std_inc = np.std(inc_deg)
    mean_rel = np.mean(rel_deg)
    std_rel = np.std(rel_deg)

    # compute best-fit virtual focus
    points_arr = np.array(points)
    dirs_arr = np.array(dirs)
    # ensure dirs are column vectors
    dirs_col = np.array([d.reshape(2,1) for d in dirs_arr]).reshape(-1,2)
    # use best-fit function
    best_pt = best_fit_point_to_lines(points_arr, dirs_arr)
    # compute distances from best_pt to each line
    dists = []
    for p, d in zip(points_arr, dirs_arr):
        # distance from point x0 to line (p + t d) = || (I - d d^T)(x0 - p) ||
        diff = best_pt - p
        proj = diff - (d @ diff) * d
        dists.append(np.linalg.norm(proj))
    dists = np.array(dists)
    mean_dist = np.mean(dists)
    std_dist = np.std(dists)

    # print summary
    nmax = n_func_xy(R_dome, 0.0)
    print("=== Ray tracing summary ===")
    print(f"Rays sampled: {n_rays}, rays that hit r_obs: {len(hits)}")
    print(f"n_max at dome edge (r={R_dome}): {nmax:.6f}")
    print(f"Incoming angles (deg): mean = {mean_inc:.4f}, std = {std_inc:.4f}")
    print(f"Relative to local tangent (deg): mean = {mean_rel:.4f}, std = {std_rel:.4f}")
    print(f"RMS relative angle (deg) = {np.sqrt(np.mean(rel_deg**2)):.4f}")
    print()
    print("=== Virtual-focus fit ===")
    print(f"Best-fit focus coordinates (x,y) = ({best_pt[0]:.6f}, {best_pt[1]:.6f})")
    print(f"Distances from focus to back-projected rays: mean = {mean_dist:.6e}, std = {std_dist:.6e}")
    print()
    # optional plotting
    if plot_result:
        plt.figure(figsize=(6,6))
        theta_plot = np.linspace(0, 2*np.pi, 400)
        plt.plot(R_dome*np.cos(theta_plot), R_dome*np.sin(theta_plot), 'k--', label='dome rim')
        plt.plot(r_obs*np.cos(theta_plot), r_obs*np.sin(theta_plot), 'b--', label='observer radius')
        # plot rays
        for sol in sols:
            if sol is None:
                continue
            if sol.y.shape[1] > 0:
                plt.plot(sol.y[0,:], sol.y[1,:], '-', alpha=0.6)
        # plot hit points
        for (th, xe, ye, vxe, vye) in hits:
            plt.plot(xe, ye, 'ro', ms=4)
            # plot back-projected line segment from hit point toward best_pt
            if best_pt is not None:
                # draw small segment along direction
                plt.plot([xe, xe + (best_pt[0]-xe)*0.2], [ye, ye + (best_pt[1]-ye)*0.2], 'r-')
        if best_pt is not None:
            plt.plot(best_pt[0], best_pt[1], 'kx', ms=10, label='best-fit focus')
        plt.gca().set_aspect('equal')
        plt.legend()
        plt.title('GRIN ray traces and best-fit virtual focus')
        plt.xlabel('x'); plt.ylabel('y')
        plt.show()

if __name__ == "__main__":
    main()
