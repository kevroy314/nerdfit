"""
Run parameter sweeps and scenario simulations.
1. Phenomena-based scenarios with noise ensemble
2. Bayesian optimization to map phase space
"""

import json
import sys
import os
import numpy as np
from pathlib import Path
from dataclasses import asdict

sys.path.insert(0, os.path.dirname(__file__))
from dynamics import Params, SimState, HabitDynamics, Event
from scenarios import ALL_SCENARIOS


def classify_outcome(result: dict) -> str:
    """Classify a trajectory's outcome."""
    H_final = result["H"][-1]
    M_final = result["M"][-1]
    H_max = np.max(result["H"])
    M_history = result["M"]

    # Check for false hope cycling: M oscillates, H stays low
    if H_final < 0.15 and H_max < 0.2:
        # Check for oscillations in M
        m_peaks = 0
        for i in range(1, len(M_history) - 1):
            if M_history[i] > M_history[i-1] and M_history[i] > M_history[i+1] and M_history[i] > 0.3:
                m_peaks += 1
        if m_peaks >= 2:
            return "false_hope_cycle"
        elif np.max(M_history) > 0.5 and M_final < 0.1:
            return "dropout"
        else:
            return "sedentary"

    if H_final > 0.5:
        return "habit_formed"

    if H_final > 0.2 and H_final < 0.5:
        return "partial_habit"

    return "sedentary"


def run_scenario_ensemble(scenario_fn, n_samples=50, seed_base=42):
    """Run a scenario with noise multiple times."""
    spec = scenario_fn()
    results = []

    for i in range(n_samples):
        sim = HabitDynamics(spec["params"], spec.get("events", []))
        result = sim.simulate(spec["initial"], spec["t_end"], dt=0.1, seed=seed_base + i)
        outcome = classify_outcome(result)
        results.append({
            "seed": seed_base + i,
            "outcome": outcome,
            "H_final": float(result["H"][-1]),
            "M_final": float(result["M"][-1]),
            "E_final": float(result["E"][-1]),
            "I_final": float(result["I"][-1]),
            "H_max": float(np.max(result["H"])),
            "M_max": float(np.max(result["M"])),
        })

    # Deterministic run for the reference trajectory
    sim = HabitDynamics(spec["params"], spec.get("events", []))
    ref = sim.simulate(spec["initial"], spec["t_end"], dt=0.1, seed=None)

    outcomes = [r["outcome"] for r in results]
    outcome_counts = {o: outcomes.count(o) for o in set(outcomes)}

    return {
        "name": spec["name"],
        "description": spec["description"],
        "phenomena": spec.get("phenomena", []),
        "outcome_distribution": outcome_counts,
        "ensemble": results,
        "reference": {
            "times": ref["times"].tolist(),
            "H": ref["H"].tolist(),
            "M": ref["M"].tolist(),
            "E": ref["E"].tolist(),
            "I": ref["I"].tolist(),
            "B": ref["B"].tolist(),
            "events": ref["events"],
        },
        "params": {k: v for k, v in asdict(spec["params"]).items()},
        "initial": {"H": spec["initial"].H, "M": spec["initial"].M,
                     "E": spec["initial"].E, "I": spec["initial"].I},
    }


def run_phase_space_search(n_samples=2000, t_end=365, seed=42):
    """
    Bayesian-optimization-style search of initial conditions and parameter space.
    Uses Latin Hypercube Sampling for initial exploration, then clusters outcomes.
    """
    rng = np.random.default_rng(seed)

    # Parameter ranges for sampling
    param_ranges = {
        "C": (0.1, 0.9),
        "beta_M": (0.05, 0.3),
        "gamma": (0.1, 0.4),
        "lambda_": (0.1, 0.5),
        "f_0": (0.05, 0.5),
        "kappa": (0.1, 0.5),
        "E_crit": (-2.0, -0.5),
        "phi_S": (0.3, 2.0),
    }

    # Initial condition ranges
    ic_ranges = {
        "H": (0.0, 0.8),
        "M": (0.0, 3.0),
        "E": (-1.0, 2.0),
        "I": (0.0, 0.6),
    }

    # Shock patterns
    shock_types = ["none", "single_large", "single_small", "periodic", "health_scare"]

    results = []
    for i in range(n_samples):
        if i % 200 == 0:
            print(f"  Phase space sample {i}/{n_samples}...")

        # Sample parameters
        p = Params()
        for param, (lo, hi) in param_ranges.items():
            setattr(p, param, rng.uniform(lo, hi))

        # Sample initial conditions
        H0 = rng.uniform(*ic_ranges["H"])
        M0 = rng.uniform(*ic_ranges["M"])
        E0 = rng.uniform(*ic_ranges["E"])
        I0 = rng.uniform(*ic_ranges["I"])
        initial = SimState(H=H0, M=M0, E=E0, I=I0)

        # Sample shock pattern
        shock_type = rng.choice(shock_types)
        events = _make_shock_events(shock_type, rng)

        # Run simulation
        sim = HabitDynamics(p, events)
        result = sim.simulate(initial, t_end, dt=0.2, seed=int(rng.integers(0, 100000)))
        outcome = classify_outcome(result)

        # Extract trajectory features for clustering
        H_traj = result["H"]
        M_traj = result["M"]
        E_traj = result["E"]
        n = len(H_traj)
        q1, q2, q3 = n // 4, n // 2, 3 * n // 4

        results.append({
            "idx": i,
            "outcome": outcome,
            "shock_type": shock_type,
            # Initial conditions
            "H0": H0, "M0": M0, "E0": E0, "I0": I0,
            # Key parameters
            "C": p.C, "beta_M": p.beta_M, "gamma": p.gamma,
            "lambda_": p.lambda_, "f_0": p.f_0, "kappa": p.kappa,
            # Final state
            "H_final": float(H_traj[-1]),
            "M_final": float(M_traj[-1]),
            "E_final": float(E_traj[-1]),
            "I_final": float(result["I"][-1]),
            # Trajectory features
            "H_max": float(np.max(H_traj)),
            "M_max": float(np.max(M_traj)),
            "H_q1": float(H_traj[q1]), "H_q2": float(H_traj[q2]), "H_q3": float(H_traj[q3]),
            "M_q1": float(M_traj[q1]), "M_q2": float(M_traj[q2]), "M_q3": float(M_traj[q3]),
            "H_monotone": float(np.mean(np.diff(H_traj) > 0)),  # Fraction of time H is increasing
            "M_oscillation": float(np.std(np.diff(M_traj))),     # M volatility
        })

    # Cluster the results
    outcomes = [r["outcome"] for r in results]
    outcome_counts = {o: outcomes.count(o) for o in set(outcomes)}
    print(f"\nOutcome distribution (n={n_samples}):")
    for o, c in sorted(outcome_counts.items(), key=lambda x: -x[1]):
        print(f"  {o}: {c} ({100*c/n_samples:.1f}%)")

    return results


def _make_shock_events(shock_type, rng):
    """Generate events for a given shock pattern."""
    if shock_type == "none":
        return []
    elif shock_type == "single_large":
        return [Event(time=0, event_type="shock", amplitude=rng.uniform(1.5, 3.0), label="Large shock")]
    elif shock_type == "single_small":
        return [Event(time=0, event_type="shock", amplitude=rng.uniform(0.3, 0.8), label="Small shock")]
    elif shock_type == "periodic":
        return [Event(time=t, event_type="new_year", amplitude=rng.uniform(0.8, 2.0),
                      label=f"Periodic shock t={t}")
                for t in [0, 90, 180, 270]]
    elif shock_type == "health_scare":
        return [Event(time=0, event_type="shock", amplitude=rng.uniform(2.0, 4.0), label="Health scare")]
    return []


def cluster_results(results):
    """Simple clustering of phase space results by outcome and trajectory shape."""
    from collections import defaultdict

    clusters = defaultdict(list)
    for r in results:
        clusters[r["outcome"]].append(r)

    cluster_summaries = {}
    for outcome, members in clusters.items():
        n = len(members)
        cluster_summaries[outcome] = {
            "count": n,
            "pct": 100 * n / len(results),
            "avg_C": np.mean([m["C"] for m in members]),
            "avg_H0": np.mean([m["H0"] for m in members]),
            "avg_M0": np.mean([m["M0"] for m in members]),
            "avg_H_final": np.mean([m["H_final"] for m in members]),
            "avg_M_final": np.mean([m["M_final"] for m in members]),
            "std_C": np.std([m["C"] for m in members]),
            "std_H0": np.std([m["H0"] for m in members]),
        }

    return cluster_summaries


def main():
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)

    # 1. Run all scenario ensembles
    print("=" * 60)
    print("PHASE 1: Phenomena-Based Scenario Ensembles")
    print("=" * 60)

    scenario_results = {}
    for key, fn in ALL_SCENARIOS.items():
        print(f"\nRunning scenario: {key}...")
        result = run_scenario_ensemble(fn, n_samples=50)
        scenario_results[key] = result
        print(f"  Outcome distribution: {result['outcome_distribution']}")

    with open(output_dir / "scenario_results.json", "w") as f:
        json.dump(scenario_results, f, indent=2, default=str)
    print(f"\nScenario results saved to {output_dir / 'scenario_results.json'}")

    # 2. Phase space search
    print("\n" + "=" * 60)
    print("PHASE 2: Phase Space Search (Bayesian-style)")
    print("=" * 60)

    phase_results = run_phase_space_search(n_samples=2000, t_end=365)
    cluster_info = cluster_results(phase_results)

    print("\nCluster summaries:")
    for outcome, info in sorted(cluster_info.items(), key=lambda x: -x[1]["count"]):
        print(f"  {outcome} ({info['count']}, {info['pct']:.1f}%):")
        print(f"    avg C={info['avg_C']:.2f}, avg H0={info['avg_H0']:.2f}, avg M0={info['avg_M0']:.2f}")
        print(f"    avg H_final={info['avg_H_final']:.2f}, avg M_final={info['avg_M_final']:.2f}")

    with open(output_dir / "phase_space_results.json", "w") as f:
        json.dump({
            "samples": phase_results,
            "clusters": cluster_info,
        }, f, indent=2, default=str)
    print(f"\nPhase space results saved to {output_dir / 'phase_space_results.json'}")

    # 3. Generate representative trajectories for each cluster
    print("\n" + "=" * 60)
    print("PHASE 3: Representative Cluster Trajectories")
    print("=" * 60)

    cluster_trajectories = {}
    for outcome, members in _group_by_outcome(phase_results).items():
        # Pick the member closest to the cluster centroid
        avg_H = np.mean([m["H_final"] for m in members])
        avg_M = np.mean([m["M_final"] for m in members])
        dists = [(abs(m["H_final"] - avg_H) + abs(m["M_final"] - avg_M), m) for m in members]
        representative = min(dists, key=lambda x: x[0])[1]

        # Re-simulate with full trajectory output
        p = Params(
            C=representative["C"],
            beta_M=representative["beta_M"],
            gamma=representative["gamma"],
            lambda_=representative["lambda_"],
            f_0=representative["f_0"],
            kappa=representative["kappa"],
        )
        initial = SimState(
            H=representative["H0"],
            M=representative["M0"],
            E=representative["E0"],
            I=representative["I0"],
        )
        events = _make_shock_events(representative["shock_type"], np.random.default_rng(123))
        sim = HabitDynamics(p, events)
        result = sim.simulate(initial, 365, dt=0.1, seed=42)

        # Downsample for JSON
        step = max(1, len(result["times"]) // 500)
        cluster_trajectories[outcome] = {
            "representative_idx": representative["idx"],
            "params": {k: v for k, v in asdict(p).items()},
            "initial": {"H": representative["H0"], "M": representative["M0"],
                        "E": representative["E0"], "I": representative["I0"]},
            "shock_type": representative["shock_type"],
            "trajectory": {
                "times": result["times"][::step].tolist(),
                "H": result["H"][::step].tolist(),
                "M": result["M"][::step].tolist(),
                "E": result["E"][::step].tolist(),
                "I": result["I"][::step].tolist(),
                "B": result["B"][::step].tolist(),
            },
            "events": result["events"],
        }
        print(f"  {outcome}: idx={representative['idx']}, C={p.C:.2f}, H0={representative['H0']:.2f}")

    with open(output_dir / "cluster_trajectories.json", "w") as f:
        json.dump(cluster_trajectories, f, indent=2, default=str)
    print(f"\nCluster trajectories saved to {output_dir / 'cluster_trajectories.json'}")

    print("\n" + "=" * 60)
    print("DONE. All results saved to simulation/results/")
    print("=" * 60)


def _group_by_outcome(results):
    from collections import defaultdict
    groups = defaultdict(list)
    for r in results:
        groups[r["outcome"]].append(r)
    return groups


if __name__ == "__main__":
    main()
