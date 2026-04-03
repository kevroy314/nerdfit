"""
GPU-batched heatmap sweep using CuPy.
Runs thousands of simulations in parallel on the GPU.
Each simulation is a row in a batch array -- vectorized Euler integration.
"""

import json
import time
import sys
import os
import numpy as np
import cupy as cp
from pathlib import Path
from scipy.stats import qmc
from scipy.ndimage import distance_transform_edt, gaussian_filter
from scipy.spatial import KDTree

RANGES = {
    "H": (0.02, 0.8),
    "M": (0.0, 3.0),
    "E": (-1.0, 2.0),
    "I": (0.0, 0.8),
    "C": (0.1, 0.95),
}
VARS = ["H", "M", "E", "I", "C"]
T_END = 365
DT = 0.5
N_STEPS = int(T_END / DT)

# Default parameters (fixed across all sims)
P = {
    "A_base": 0.8, "alpha_H": 0.045, "delta_H": 0.01, "H_min": 0.02,
    "beta_M": 0.15, "lambda_": 0.2, "gamma": 0.25, "gamma_ind": 0.1,
    "f_0": 0.3, "phi_M": 0.08, "psi": 0.15, "epsilon": 0.03,
    "phi_ind": 0.05, "kappa": 0.3, "E_crit": -1.5,
    "kappa_wth": 0.8, "E_wth": 1.5, "tau": 0.15, "mu": 0.1,
    "alpha_I": 0.005, "delta_I": 0.001,
    "C_min": 0.1, "C_max": 0.95,
    "alpha_C_down": 0.003, "alpha_C_up": 0.001,
}


def gpu_simulate_batch(H0, M0, E0, I0, C0):
    """
    Run N simulations in parallel on GPU.
    H0, M0, E0, I0, C0: 1D numpy arrays of length N.
    Returns dict of 1D numpy arrays with final metrics.
    """
    N = len(H0)
    dt = cp.float32(DT)
    p = {k: cp.float32(v) for k, v in P.items()}

    # State arrays on GPU
    H = cp.array(H0, dtype=cp.float32)
    M = cp.array(M0, dtype=cp.float32)
    E = cp.array(E0, dtype=cp.float32)
    I = cp.array(I0, dtype=cp.float32)
    C = cp.array(C0, dtype=cp.float32)
    dE_prev = cp.zeros(N, dtype=cp.float32)

    # Metric accumulators
    cum_cog_load = cp.zeros(N, dtype=cp.float32)
    cum_activity = cp.zeros(N, dtype=cp.float32)
    cum_path = cp.zeros(N, dtype=cp.float32)
    H_prev = H.copy()
    M_prev = M.copy()
    E_prev = E.copy()
    I_prev = I.copy()
    C_prev = C.copy()
    time_to_habit = cp.full(N, T_END, dtype=cp.float32)
    habit_reached = cp.zeros(N, dtype=cp.bool_)

    # Settling: accumulate last-quarter derivatives
    q3_start = 3 * N_STEPS // 4
    settle_accum = cp.zeros(N, dtype=cp.float32)
    settle_count = cp.float32(0)

    for step in range(N_STEPS):
        # Behavioral trigger
        theta = C * (1 - H)
        B_goal = 1.0 / (1.0 + cp.exp(-cp.clip((M - theta) / p["tau"], -20, 20)))
        M_habit_floor = 0.15 * (1 - H * 0.5)
        B_habit = H * (1.0 / (1.0 + cp.exp(-cp.clip((M - M_habit_floor) / 0.08, -20, 20))))
        blend = H ** 1.5
        B_raw = (1 - blend) * B_goal + blend * B_habit
        activation = 1.0 / (1.0 + cp.exp(-cp.clip((M - 0.08) / 0.03, -20, 20)))
        B = cp.clip(B_raw * activation, 0, 1)

        # Fantasy
        F = p["f_0"] * M * (1 - B)

        # Habit ceiling
        A_eff = p["A_base"] + (1 - p["A_base"]) * I

        # dH/dt
        decay_rate = p["delta_H"] * (1 + 2 * (1 - B) * H)
        dH = p["alpha_H"] * B * (A_eff - H) - decay_rate * (1 - B) * (H - p["H_min"])

        # dM/dt
        decay = -p["beta_M"] * M / (1 + M)
        novelty = cp.maximum(0, 1 - H * H)
        m_headroom = cp.maximum(0, 1 - M / 2)
        reward = p["gamma"] * B * novelty * m_headroom
        effort = -p["lambda_"] * C * (1 - H) * B
        indulgence = -p["gamma_ind"] * F * (1 - H)
        fh = -p["kappa"] * cp.log1p(cp.exp(cp.clip(-E - abs(p["E_crit"]), -20, 20))) * M
        wth = -p["kappa_wth"] * (1.0 / (1.0 + cp.exp(-cp.clip((E - p["E_wth"]) / 0.2, -20, 20)))) * M
        velocity = p["mu"] * (-dE_prev)
        id_target = 0.2 * I
        id_restore = 0.08 * cp.maximum(0, id_target - M)
        habit_maint = 0.02 * B * H
        dM = decay + reward + effort + indulgence + fh + wth + velocity + id_restore + habit_maint

        # dE/dt
        dE = (p["phi_M"] * M * (1 - H) - p["psi"] * B * H - p["epsilon"] * E
              + p["phi_ind"] * F - 0.3 * B * (1 - H) * (E > 0).astype(cp.float32))

        # dI/dt
        dI = p["alpha_I"] * B * H * (1 - I) - p["delta_I"] * (1 - B) * I

        # dC/dt (equilibrium-based)
        C_equil = p["C_min"] + (p["C_max"] - p["C_min"]) * H * (0.7 + 0.3 * I)
        overreach = cp.maximum(0, C - C_equil) * cp.maximum(0, 0.3 - B)
        failure_p = -p["alpha_C_down"] * overreach
        e_reassess = -p["alpha_C_down"] * 0.3 * cp.log1p(cp.exp(cp.clip(-E - abs(p["E_crit"]) * 0.5, -20, 20))) * cp.maximum(0, 0.3 - B)
        underreach = cp.maximum(0, C_equil - C) * B
        success_p = p["alpha_C_up"] * underreach
        id_c = p["alpha_C_up"] * 0.3 * I * cp.maximum(0, H - 0.3) * cp.maximum(0, C_equil - C)
        dC = failure_p + e_reassess + success_p + id_c

        # C-M coupling
        dM += cp.maximum(0, -dC) * 0.3

        # Euler integration
        H_new = cp.clip(H + dH * dt, p["H_min"], 1.0)
        M_new = cp.maximum(0, M + dM * dt)
        E_new = E + dE * dt
        I_new = cp.clip(I + dI * dt, 0, 1)
        C_new = cp.clip(C + dC * dt, p["C_min"], p["C_max"])

        # Accumulate metrics
        cum_cog_load += C * (1 - H) * B * dt
        cum_activity += C * B * dt
        path_inc = cp.sqrt((H_new - H_prev)**2 + (M_new - M_prev)**2 +
                           (E_new - E_prev)**2 + (I_new - I_prev)**2 + (C_new - C_prev)**2)
        cum_path += path_inc

        # Time to habit
        newly_reached = (H_new > 0.5) & (~habit_reached)
        time_to_habit = cp.where(newly_reached, step * DT, time_to_habit)
        habit_reached |= (H_new > 0.5)

        # Settling (last quarter)
        if step >= q3_start:
            settle_accum += (cp.abs(H_new - H) + cp.abs(M_new - M) +
                             cp.abs(E_new - E) + cp.abs(I_new - I) + cp.abs(C_new - C)) / dt
            settle_count += 1

        # Update state
        H_prev, M_prev, E_prev, I_prev, C_prev = H.copy(), M.copy(), E.copy(), I.copy(), C.copy()
        H, M, E, I, C = H_new, M_new, E_new, I_new, C_new
        dE_prev = dE

    # Compute final metrics
    success = (H > 0.5).astype(cp.float32)
    settling = settle_accum / cp.maximum(settle_count, 1)

    return {
        "success": cp.asnumpy(success),
        "cognitive_load": cp.asnumpy(cum_cog_load),
        "net_activity": cp.asnumpy(cum_activity),
        "path_length": cp.asnumpy(cum_path),
        "settling": cp.asnumpy(settling),
        "time_to_habit": cp.asnumpy(time_to_habit),
    }


def lhs_sample(n, seed=42):
    sampler = qmc.LatinHypercube(d=5, seed=seed)
    raw = sampler.random(n)
    pts = np.zeros((n, 5))
    for i, var in enumerate(VARS):
        lo, hi = RANGES[var]
        pts[:, i] = lo + raw[:, i] * (hi - lo)
    return pts


def adaptive_refine(pts, metrics, n_new, rng):
    """Sample near the separatrix and in under-sampled regions."""
    X = pts
    success = metrics["success"]

    tree = KDTree(X)
    gradients = np.zeros(len(X))
    for j in range(0, len(X), max(1, len(X) // 2000)):  # Subsample for speed
        _, nn_idx = tree.query(X[j], k=min(8, len(X)))
        if len(nn_idx) > 1:
            gradients[j] = np.std(success[nn_idx[1:]])

    new_pts = np.zeros((n_new, 5))

    # 60% near separatrix
    n_sep = int(n_new * 0.6)
    gw = gradients / (gradients.sum() + 1e-10)
    for k in range(n_sep):
        bi = rng.choice(len(X), p=gw)
        for i, var in enumerate(VARS):
            lo, hi = RANGES[var]
            new_pts[k, i] = np.clip(X[bi, i] + rng.normal(0, (hi - lo) * 0.02), lo, hi)

    # 40% under-sampled
    n_bins = 6
    bins = [np.linspace(*RANGES[v], n_bins + 1) for v in VARS]
    bc = np.zeros([n_bins] * 5)
    for x in X[::max(1, len(X) // 5000)]:
        idx = tuple(min(np.searchsorted(bins[i][1:], x[i]), n_bins - 1) for i in range(5))
        bc[idx] += 1
    wf = (1.0 / (bc + 1)).flatten()
    wf /= wf.sum()
    for k in range(n_sep, n_new):
        bi = rng.choice(len(wf), p=wf)
        mi = np.unravel_index(bi, [n_bins] * 5)
        for i, var in enumerate(VARS):
            lo, hi = bins[i][mi[i]], bins[i][mi[i] + 1]
            new_pts[k, i] = rng.uniform(lo, hi)

    return new_pts


def compute_heatmaps(pts, metrics, resolution=80):
    pairs = [(VARS[i], VARS[j]) for i in range(5) for j in range(i + 1, 5)]
    metric_names = list(metrics.keys())
    heatmaps = {}

    for v1, v2 in pairs:
        i1, i2 = VARS.index(v1), VARS.index(v2)
        lo1, hi1 = RANGES[v1]
        lo2, hi2 = RANGES[v2]
        edges1 = np.linspace(lo1, hi1, resolution + 1)
        edges2 = np.linspace(lo2, hi2, resolution + 1)
        c1 = ((edges1[:-1] + edges1[1:]) / 2).tolist()
        c2 = ((edges2[:-1] + edges2[1:]) / 2).tolist()

        key = f"{v1}_{v2}"
        heatmaps[key] = {"v1": v1, "v2": v2, "centers1": c1, "centers2": c2, "metrics": {}}

        for mname in metric_names:
            mvals = metrics[mname]
            grid = np.full((resolution, resolution), np.nan)
            counts = np.zeros((resolution, resolution))

            b1 = np.clip(np.searchsorted(edges1[1:], pts[:, i1]), 0, resolution - 1)
            b2 = np.clip(np.searchsorted(edges2[1:], pts[:, i2]), 0, resolution - 1)

            for k in range(len(pts)):
                r, c = b1[k], b2[k]
                if np.isnan(grid[r, c]):
                    grid[r, c] = 0
                    counts[r, c] = 0
                grid[r, c] += mvals[k]
                counts[r, c] += 1

            mask = counts > 0
            grid[mask] /= counts[mask]

            if np.any(np.isnan(grid)):
                nm = np.isnan(grid)
                _, idx = distance_transform_edt(nm, return_distances=True, return_indices=True)
                grid = grid[tuple(idx)]

            grid = gaussian_filter(grid, sigma=2.0)

            heatmaps[key]["metrics"][mname] = {
                "data": [[round(v, 4) for v in row] for row in grid.tolist()],
                "min": round(float(np.min(grid)), 4),
                "max": round(float(np.max(grid)), 4),
            }

    return heatmaps


def main():
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)
    t_start = time.time()
    rng = np.random.default_rng(42)

    # GPU batch size: 1080 Ti can handle ~50K sims per batch
    BATCH = 20000

    # Phase 1: Dense LHS
    n1 = 20000
    print(f"Phase 1: LHS ({n1} points on GPU)...")
    pts = lhs_sample(n1, seed=42)
    metrics = gpu_simulate_batch(pts[:, 0], pts[:, 1], pts[:, 2], pts[:, 3], pts[:, 4])

    elapsed = time.time() - t_start
    rate = n1 / elapsed
    sr = np.mean(metrics["success"])
    print(f"  Done: {elapsed:.1f}s, {rate:.0f} pts/s, success={sr:.1%}")

    # Phase 2: Adaptive refinement loops
    budget_s = 2700  # 45 min budget
    phase = 2
    all_pts = pts
    all_metrics = {k: v.copy() for k, v in metrics.items()}

    while (time.time() - t_start) < budget_s:
        remaining = budget_s - (time.time() - t_start)
        n_new = min(BATCH, max(2000, int(remaining * rate * 0.7)))
        print(f"Phase {phase}: Adaptive ({n_new} pts, {remaining:.0f}s left)...")

        new_pts = adaptive_refine(all_pts, all_metrics, n_new, rng)
        new_m = gpu_simulate_batch(new_pts[:, 0], new_pts[:, 1], new_pts[:, 2],
                                   new_pts[:, 3], new_pts[:, 4])

        all_pts = np.vstack([all_pts, new_pts])
        for k in all_metrics:
            all_metrics[k] = np.concatenate([all_metrics[k], new_m[k]])

        elapsed = time.time() - t_start
        rate = len(all_pts) / elapsed
        sr = np.mean(all_metrics["success"])
        print(f"  Total: {len(all_pts)} pts, {elapsed:.0f}s, {rate:.0f} pts/s, success={sr:.1%}")
        phase += 1

    total = len(all_pts)
    print(f"\nFinal: {total} points in {time.time() - t_start:.0f}s")

    print("Computing heatmaps (80x80)...")
    heatmaps = compute_heatmaps(all_pts, all_metrics, resolution=80)

    summary = {}
    for mname, vals in all_metrics.items():
        summary[mname] = {
            "mean": round(float(np.mean(vals)), 4),
            "std": round(float(np.std(vals)), 4),
            "min": round(float(np.min(vals)), 4),
            "max": round(float(np.max(vals)), 4),
        }
        print(f"  {mname}: mean={summary[mname]['mean']}, range=[{summary[mname]['min']}, {summary[mname]['max']}]")

    output = {"n_points": total, "summary": summary, "heatmaps": heatmaps}

    outpath = output_dir / "heatmap_data.json"
    with open(outpath, "w") as f:
        json.dump(output, f, separators=(",", ":"))
    print(f"Saved to {outpath} ({outpath.stat().st_size / 1024 / 1024:.1f} MB)")

    viz_path = Path(__file__).parent.parent / "visualizer" / "heatmap_data.json"
    import shutil
    shutil.copy2(outpath, viz_path)
    print(f"Copied to {viz_path}")


if __name__ == "__main__":
    main()
