"""
Bayesian-optimized 5D sweep of (H0, M0, E0, I0, C0) to compute heatmap data.

Metrics computed per simulation:
1. success: H_final > 0.5
2. cognitive_load: integral of C * (1-H) * B over time
3. net_activity: integral of C * B over time
4. path_length: sum of sqrt(dH^2 + dM^2 + dE^2 + dI^2 + dC^2)
5. settling: mean |derivative| in last quarter (lower = more stable)
6. time_to_habit: days until H > 0.5 (or 730 if never)

Strategy:
- Phase 1: Latin Hypercube sample (500 points) for initial coverage
- Phase 2: Bayesian optimization with joint + per-metric acquisition (1500 more points)
- Output: JSON with all sample points and metrics, plus 2D projections

For 2D heatmaps, we marginalize over the non-displayed dimensions by taking
the mean metric value across all samples near each (x,y) bin.
"""

import json
import sys
import os
import numpy as np
from pathlib import Path
from scipy.stats import qmc

sys.path.insert(0, os.path.dirname(__file__))
from dynamics import Params, SimState, HabitDynamics


# Ranges for each initial condition
RANGES = {
    "H": (0.02, 0.8),
    "M": (0.0, 3.0),
    "E": (-1.0, 2.0),
    "I": (0.0, 0.8),
    "C": (0.1, 0.95),
}

VARS = ["H", "M", "E", "I", "C"]
T_END = 365  # 1 year per sample (speed vs coverage tradeoff)
DT = 0.5     # Coarser dt for speed


def run_single(h0, m0, e0, i0, c0, seed=None):
    """Run one simulation and compute all metrics."""
    p = Params(C=c0, alpha_H=0.045, sigma_noise=0.015)
    sim = HabitDynamics(p)
    state = SimState(H=h0, M=m0, E=e0, I=i0, C=c0)
    r = sim.simulate(state, T_END, dt=DT, seed=seed)

    H, M, E, I, C, B = r["H"], r["M"], r["E"], r["I"], r["C"], r["B"]
    n = len(H)

    # 1. Success
    success = 1.0 if H[-1] > 0.5 else 0.0

    # 2. Cognitive load: integral of C * (1-H) * B
    cog_load = np.sum(C * (1 - H) * B) * DT

    # 3. Net activity: integral of C * B
    net_activity = np.sum(C * B) * DT

    # 4. Path length in 5D state space
    diffs = np.sqrt(
        np.diff(H)**2 + np.diff(M)**2 + np.diff(E)**2 +
        np.diff(I)**2 + np.diff(C)**2
    )
    path_length = np.sum(diffs)

    # 5. Settling stability: mean |derivative| in last quarter
    q3 = 3 * n // 4
    settling = np.mean(
        np.abs(np.diff(H[q3:])) + np.abs(np.diff(M[q3:])) +
        np.abs(np.diff(E[q3:])) + np.abs(np.diff(I[q3:])) +
        np.abs(np.diff(C[q3:]))
    ) / DT

    # 6. Time to habit (days until H > 0.5)
    above = np.where(H > 0.5)[0]
    time_to_habit = float(above[0] * DT) if len(above) > 0 else T_END

    return {
        "success": success,
        "cognitive_load": float(cog_load),
        "net_activity": float(net_activity),
        "path_length": float(path_length),
        "settling": float(settling),
        "time_to_habit": time_to_habit,
    }


def latin_hypercube_sample(n_samples, seed=42):
    """Generate LHS samples in 5D."""
    sampler = qmc.LatinHypercube(d=5, seed=seed)
    samples = sampler.random(n_samples)
    # Scale to ranges
    points = []
    for s in samples:
        pt = {}
        for i, var in enumerate(VARS):
            lo, hi = RANGES[var]
            pt[var] = lo + s[i] * (hi - lo)
        points.append(pt)
    return points


def bayesian_next_points(existing_points, existing_metrics, n_new, metric_weights=None):
    """
    Simple Bayesian-style adaptive sampling.
    Uses a grid-based uncertainty estimate: regions with fewer samples get priority.
    For each metric, also add points near high-gradient regions.
    """
    rng = np.random.default_rng(123)

    # Convert existing to arrays
    X = np.array([[p[v] for v in VARS] for p in existing_points])
    n_existing = len(X)

    # Bin counts in a coarse 5D grid (5 bins per dim = 3125 cells)
    n_bins = 5
    bins_per_dim = []
    for var in VARS:
        lo, hi = RANGES[var]
        bins_per_dim.append(np.linspace(lo, hi, n_bins + 1))

    # Count samples per bin
    bin_counts = np.zeros([n_bins] * 5)
    for x in X:
        idx = []
        for i, var in enumerate(VARS):
            bi = np.searchsorted(bins_per_dim[i][1:], x[i])
            bi = min(bi, n_bins - 1)
            idx.append(bi)
        bin_counts[tuple(idx)] += 1

    new_points = []

    # Joint: sample from under-represented bins (60% of budget)
    n_joint = int(n_new * 0.6)
    # Weight inversely by count
    weights = 1.0 / (bin_counts + 1)
    weights_flat = weights.flatten()
    weights_flat /= weights_flat.sum()

    for _ in range(n_joint):
        bin_idx = rng.choice(len(weights_flat), p=weights_flat)
        multi_idx = np.unravel_index(bin_idx, [n_bins] * 5)
        pt = {}
        for i, var in enumerate(VARS):
            lo = bins_per_dim[i][multi_idx[i]]
            hi = bins_per_dim[i][multi_idx[i] + 1]
            pt[var] = rng.uniform(lo, hi)
        new_points.append(pt)

    # Per-metric: sample near high-gradient regions (40% of budget)
    n_per_metric = (n_new - n_joint) // 6  # 6 metrics
    metric_names = ["success", "cognitive_load", "net_activity",
                    "path_length", "settling", "time_to_habit"]

    for mname in metric_names:
        vals = np.array([m[mname] for m in existing_metrics])
        if np.std(vals) < 1e-10:
            # Uniform -- just random sample
            for _ in range(n_per_metric):
                pt = {}
                for var in VARS:
                    lo, hi = RANGES[var]
                    pt[var] = rng.uniform(lo, hi)
                new_points.append(pt)
            continue

        # Find nearest-neighbor gradient magnitude for each point
        from scipy.spatial import KDTree
        tree = KDTree(X)
        gradients = np.zeros(n_existing)
        for j in range(n_existing):
            _, nn_idx = tree.query(X[j], k=min(6, n_existing))
            if len(nn_idx) > 1:
                nn_vals = vals[nn_idx[1:]]
                gradients[j] = np.std(nn_vals)

        # Sample near high-gradient points
        grad_weights = gradients / (gradients.sum() + 1e-10)
        for _ in range(n_per_metric):
            base_idx = rng.choice(n_existing, p=grad_weights)
            pt = {}
            for i, var in enumerate(VARS):
                lo, hi = RANGES[var]
                noise = rng.normal(0, (hi - lo) * 0.05)
                pt[var] = np.clip(X[base_idx, i] + noise, lo, hi)
            new_points.append(pt)

    return new_points


def compute_2d_heatmaps(points, metrics, resolution=50):
    """
    For each pair of variables, compute 2D heatmaps by binning and averaging.
    """
    pairs = []
    for i in range(len(VARS)):
        for j in range(i+1, len(VARS)):
            pairs.append((VARS[i], VARS[j]))

    metric_names = ["success", "cognitive_load", "net_activity",
                    "path_length", "settling", "time_to_habit"]

    heatmaps = {}
    for v1, v2 in pairs:
        lo1, hi1 = RANGES[v1]
        lo2, hi2 = RANGES[v2]
        edges1 = np.linspace(lo1, hi1, resolution + 1)
        edges2 = np.linspace(lo2, hi2, resolution + 1)
        centers1 = (edges1[:-1] + edges1[1:]) / 2
        centers2 = (edges2[:-1] + edges2[1:]) / 2

        vals1 = np.array([p[v1] for p in points])
        vals2 = np.array([p[v2] for p in points])

        key = f"{v1}_{v2}"
        heatmaps[key] = {
            "v1": v1, "v2": v2,
            "centers1": centers1.tolist(),
            "centers2": centers2.tolist(),
            "metrics": {},
        }

        for mname in metric_names:
            mvals = np.array([m[mname] for m in metrics])
            grid = np.full((resolution, resolution), np.nan)
            counts = np.zeros((resolution, resolution))

            for k in range(len(points)):
                i1 = np.searchsorted(edges1[1:], vals1[k])
                i2 = np.searchsorted(edges2[1:], vals2[k])
                i1 = min(i1, resolution - 1)
                i2 = min(i2, resolution - 1)
                if np.isnan(grid[i1, i2]):
                    grid[i1, i2] = 0
                grid[i1, i2] += mvals[k]
                counts[i1, i2] += 1

            # Average
            mask = counts > 0
            grid[mask] /= counts[mask]

            # Interpolate NaN gaps using nearest neighbor
            from scipy.ndimage import distance_transform_edt
            if np.any(np.isnan(grid)):
                nan_mask = np.isnan(grid)
                _, indices = distance_transform_edt(nan_mask, return_distances=True, return_indices=True)
                grid = grid[tuple(indices)]

            heatmaps[key]["metrics"][mname] = {
                "data": grid.tolist(),
                "min": float(np.nanmin(grid)),
                "max": float(np.nanmax(grid)),
            }

    return heatmaps


def main():
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)

    print("Phase 1: Latin Hypercube Sampling (500 points)...")
    points = latin_hypercube_sample(500)
    metrics = []

    for i, pt in enumerate(points):
        if i % 100 == 0:
            print(f"  Running {i}/500...")
        m = run_single(pt["H"], pt["M"], pt["E"], pt["I"], pt["C"], seed=i)
        metrics.append(m)

    success_rate = np.mean([m["success"] for m in metrics])
    print(f"  Phase 1 done. Success rate: {success_rate:.1%}")

    print("Phase 2: Bayesian adaptive sampling (1500 points)...")
    for batch in range(3):
        new_pts = bayesian_next_points(points, metrics, 500)
        for i, pt in enumerate(new_pts):
            if i % 100 == 0:
                print(f"  Batch {batch+1}/3, running {i}/500...")
            m = run_single(pt["H"], pt["M"], pt["E"], pt["I"], pt["C"],
                           seed=len(points) + i)
            metrics.append(m)
        points.extend(new_pts)

    total = len(points)
    success_rate = np.mean([m["success"] for m in metrics])
    print(f"  Phase 2 done. Total: {total} points. Success: {success_rate:.1%}")

    print("Computing 2D heatmaps (50x50 resolution)...")
    heatmaps = compute_2d_heatmaps(points, metrics, resolution=50)

    # Summary statistics
    metric_names = ["success", "cognitive_load", "net_activity",
                    "path_length", "settling", "time_to_habit"]
    summary = {}
    for mname in metric_names:
        vals = [m[mname] for m in metrics]
        summary[mname] = {
            "mean": float(np.mean(vals)),
            "std": float(np.std(vals)),
            "min": float(np.min(vals)),
            "max": float(np.max(vals)),
            "median": float(np.median(vals)),
        }
        print(f"  {mname}: mean={summary[mname]['mean']:.3f}, "
              f"std={summary[mname]['std']:.3f}, "
              f"range=[{summary[mname]['min']:.3f}, {summary[mname]['max']:.3f}]")

    # Save
    output = {
        "n_points": total,
        "summary": summary,
        "heatmaps": heatmaps,
        # Don't save raw points (too large) -- just heatmaps
    }

    outpath = output_dir / "heatmap_data.json"
    with open(outpath, "w") as f:
        json.dump(output, f, separators=(",", ":"))
    size_mb = outpath.stat().st_size / 1024 / 1024
    print(f"\nSaved to {outpath} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
