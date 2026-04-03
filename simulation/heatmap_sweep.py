"""
Bayesian-optimized 5D sweep with parallel execution.
Deterministic (no noise, no events) to map the landscape cleanly.
Stochastic noise and events are the trajectory's job, not the heatmap's.

Target: ~30K+ points in ~1 hour on 10 cores.
"""

import json
import sys
import os
import time
import numpy as np
from pathlib import Path
from multiprocessing import Pool, cpu_count
from functools import partial
from scipy.stats import qmc
from scipy.ndimage import distance_transform_edt, gaussian_filter

sys.path.insert(0, os.path.dirname(__file__))
from dynamics import Params, SimState, HabitDynamics

RANGES = {
    "H": (0.02, 0.8),
    "M": (0.0, 3.0),
    "E": (-1.0, 2.0),
    "I": (0.0, 0.8),
    "C": (0.1, 0.95),
}
VARS = ["H", "M", "E", "I", "C"]
T_END = 365
DT = 0.5  # Coarser for speed


def run_single(args):
    """Run one deterministic simulation. Takes (h0, m0, e0, i0, c0).

    Metrics accumulated sequentially in a loop (not via np.sum on arrays)
    to produce bit-identical results to the CUDA kernel.
    """
    h0, m0, e0, i0, c0 = args
    p = Params(C=c0, alpha_H=0.045, sigma_noise=0)
    sim = HabitDynamics(p)
    state = SimState(H=h0, M=m0, E=e0, I=i0, C=c0)
    r = sim.simulate(state, T_END, dt=DT, seed=None)

    H, M, E, I, C, B = r["H"], r["M"], r["E"], r["I"], r["C"], r["B"]
    n = len(H)  # N_STEPS + 1
    q3 = 3 * n // 4

    success = 1.0 if H[-1] > 0.5 else 0.0

    # Metric accumulation: sequential += over Python floats for reproducibility.
    # The state arrays (H, M, E, I, C, B) come from dynamics.py's vectorized numpy,
    # which is our ground truth. We just accumulate metrics sequentially.
    cum_cog = 0.0
    cum_act = 0.0
    cum_path = 0.0
    settle_acc = 0.0
    settle_n = 0
    time_to_habit = float(T_END)
    reached = bool(H[0] > 0.5)
    if reached:
        time_to_habit = 0.0

    # Pre-extract as Python floats for sequential accumulation
    Hf = H.astype(np.float64)
    Mf = M.astype(np.float64)
    Ef = E.astype(np.float64)
    If = I.astype(np.float64)
    Cf = C.astype(np.float64)
    Bf = B.astype(np.float64)

    for i in range(1, n):
        ci, hi, bi = float(Cf[i]), float(Hf[i]), float(Bf[i])
        cum_cog += ci * (1.0 - hi) * bi * DT
        cum_act += ci * bi * DT

        dh = float(Hf[i] - Hf[i-1])
        dm = float(Mf[i] - Mf[i-1])
        de = float(Ef[i] - Ef[i-1])
        di = float(If[i] - If[i-1])
        dc = float(Cf[i] - Cf[i-1])
        cum_path += float(np.sqrt(dh*dh + dm*dm + de*de + di*di + dc*dc))

        if not reached and Hf[i] > 0.5:
            time_to_habit = float(i * DT)
            reached = True

        if i >= q3 + 1:
            settle_acc += (abs(dh) + abs(dm) + abs(de) + abs(di) + abs(dc)) / DT
            settle_n += 1

    settling = settle_acc / settle_n if settle_n > 0 else 0.0

    return (h0, m0, e0, i0, c0,
            success, cum_cog, cum_act, cum_path, settling, time_to_habit)


def lhs_sample(n, seed=42):
    sampler = qmc.LatinHypercube(d=5, seed=seed)
    raw = sampler.random(n)
    pts = []
    for s in raw:
        pt = []
        for i, var in enumerate(VARS):
            lo, hi = RANGES[var]
            pt.append(lo + s[i] * (hi - lo))
        pts.append(tuple(pt))
    return pts


def adaptive_refine(results, n_new, rng):
    """Generate points near high-gradient regions of the success metric."""
    X = np.array([(r[0], r[1], r[2], r[3], r[4]) for r in results])
    success = np.array([r[5] for r in results])

    from scipy.spatial import KDTree
    tree = KDTree(X)
    gradients = np.zeros(len(X))
    for j in range(len(X)):
        _, nn_idx = tree.query(X[j], k=min(8, len(X)))
        if len(nn_idx) > 1:
            nn_vals = success[nn_idx[1:]]
            gradients[j] = np.std(nn_vals)

    # Mix: 50% near separatrix (high gradient), 50% under-sampled regions
    new_pts = []

    # Near-separatrix sampling
    n_sep = n_new // 2
    grad_weights = gradients / (gradients.sum() + 1e-10)
    for _ in range(n_sep):
        base_idx = rng.choice(len(X), p=grad_weights)
        pt = []
        for i, var in enumerate(VARS):
            lo, hi = RANGES[var]
            noise = rng.normal(0, (hi - lo) * 0.03)
            pt.append(float(np.clip(X[base_idx, i] + noise, lo, hi)))
        new_pts.append(tuple(pt))

    # Under-sampled regions
    n_under = n_new - n_sep
    n_bins = 6
    bins_per_dim = [np.linspace(*RANGES[v], n_bins + 1) for v in VARS]
    bin_counts = np.zeros([n_bins] * 5)
    for x in X:
        idx = tuple(min(np.searchsorted(bins_per_dim[i][1:], x[i]), n_bins - 1) for i in range(5))
        bin_counts[idx] += 1
    weights = 1.0 / (bin_counts + 1)
    wf = weights.flatten()
    wf /= wf.sum()
    for _ in range(n_under):
        bi = rng.choice(len(wf), p=wf)
        mi = np.unravel_index(bi, [n_bins] * 5)
        pt = []
        for i, var in enumerate(VARS):
            lo = bins_per_dim[i][mi[i]]
            hi = bins_per_dim[i][mi[i] + 1]
            pt.append(float(rng.uniform(lo, hi)))
        new_pts.append(tuple(pt))

    return new_pts


def compute_heatmaps(results, resolution=80):
    """Compute smoothed 2D heatmaps for all variable pairs and metrics."""
    X = np.array([(r[0], r[1], r[2], r[3], r[4]) for r in results])
    metric_names = ["success", "cognitive_load", "net_activity",
                    "path_length", "settling", "time_to_habit"]
    metric_idx = {m: i + 5 for i, m in enumerate(metric_names)}

    pairs = []
    for i in range(5):
        for j in range(i + 1, 5):
            pairs.append((VARS[i], VARS[j]))

    heatmaps = {}
    for v1, v2 in pairs:
        i1, i2 = VARS.index(v1), VARS.index(v2)
        lo1, hi1 = RANGES[v1]
        lo2, hi2 = RANGES[v2]
        edges1 = np.linspace(lo1, hi1, resolution + 1)
        edges2 = np.linspace(lo2, hi2, resolution + 1)
        centers1 = (edges1[:-1] + edges1[1:]) / 2
        centers2 = (edges2[:-1] + edges2[1:]) / 2

        key = f"{v1}_{v2}"
        heatmaps[key] = {
            "v1": v1, "v2": v2,
            "centers1": centers1.tolist(),
            "centers2": centers2.tolist(),
            "metrics": {},
        }

        for mname in metric_names:
            mi = metric_idx[mname]
            mvals = np.array([r[mi] for r in results])

            grid = np.full((resolution, resolution), np.nan)
            counts = np.zeros((resolution, resolution))

            for k in range(len(results)):
                b1 = min(np.searchsorted(edges1[1:], X[k, i1]), resolution - 1)
                b2 = min(np.searchsorted(edges2[1:], X[k, i2]), resolution - 1)
                if np.isnan(grid[b1, b2]):
                    grid[b1, b2] = 0
                grid[b1, b2] += mvals[k]
                counts[b1, b2] += 1

            mask = counts > 0
            grid[mask] /= counts[mask]

            # Fill NaN via nearest neighbor then smooth
            if np.any(np.isnan(grid)):
                nan_mask = np.isnan(grid)
                _, indices = distance_transform_edt(nan_mask, return_distances=True, return_indices=True)
                grid = grid[tuple(indices)]

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
    n_workers = min(10, cpu_count())
    print(f"Using {n_workers} workers")

    rng = np.random.default_rng(42)

    # Phase 1: Dense LHS
    n_phase1 = 8000
    print(f"Phase 1: LHS ({n_phase1} points)...")
    pts = lhs_sample(n_phase1, seed=42)

    with Pool(n_workers) as pool:
        results = list(pool.imap_unordered(run_single, pts, chunksize=100))

    elapsed = time.time() - t_start
    rate = len(results) / elapsed
    print(f"  {len(results)} done in {elapsed:.0f}s ({rate:.0f} pts/s)")
    success_rate = np.mean([r[5] for r in results])
    print(f"  Success rate: {success_rate:.1%}")

    # Phase 2: Adaptive refinement (repeat until budget)
    budget_s = 3000  # ~50 min of compute, leave margin
    phase = 2
    while (time.time() - t_start) < budget_s:
        remaining = budget_s - (time.time() - t_start)
        # Estimate how many more points we can do
        n_new = min(4000, max(500, int(remaining * rate * 0.8)))
        print(f"Phase {phase}: Adaptive refinement ({n_new} points, {remaining:.0f}s remaining)...")

        new_pts = adaptive_refine(results, n_new, rng)
        with Pool(n_workers) as pool:
            new_results = list(pool.imap_unordered(run_single, new_pts, chunksize=100))
        results.extend(new_results)

        elapsed = time.time() - t_start
        rate = len(results) / elapsed
        success_rate = np.mean([r[5] for r in results])
        print(f"  Total: {len(results)} pts, {elapsed:.0f}s, {rate:.0f} pts/s, success={success_rate:.1%}")
        phase += 1

    total = len(results)
    print(f"\nFinal: {total} points in {time.time() - t_start:.0f}s")

    # Compute heatmaps
    print("Computing 2D heatmaps (80x80 with smoothing)...")
    heatmaps = compute_heatmaps(results, resolution=80)

    metric_names = ["success", "cognitive_load", "net_activity",
                    "path_length", "settling", "time_to_habit"]
    summary = {}
    for mname in metric_names:
        mi = {"success": 5, "cognitive_load": 6, "net_activity": 7,
              "path_length": 8, "settling": 9, "time_to_habit": 10}[mname]
        vals = [r[mi] for r in results]
        summary[mname] = {
            "mean": round(float(np.mean(vals)), 4),
            "std": round(float(np.std(vals)), 4),
            "min": round(float(np.min(vals)), 4),
            "max": round(float(np.max(vals)), 4),
        }
        print(f"  {mname}: mean={summary[mname]['mean']}, range=[{summary[mname]['min']}, {summary[mname]['max']}]")

    output = {
        "n_points": total,
        "summary": summary,
        "heatmaps": heatmaps,
    }

    outpath = output_dir / "heatmap_data.json"
    with open(outpath, "w") as f:
        json.dump(output, f, separators=(",", ":"))
    size_mb = outpath.stat().st_size / 1024 / 1024
    print(f"\nSaved to {outpath} ({size_mb:.1f} MB)")

    # Also copy to visualizer
    viz_path = Path(__file__).parent.parent / "visualizer" / "heatmap_data.json"
    import shutil
    shutil.copy2(outpath, viz_path)
    print(f"Copied to {viz_path}")


if __name__ == "__main__":
    main()
