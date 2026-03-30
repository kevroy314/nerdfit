"""
Run all person x event_stream simulations and analyze outcomes against
literature-based priors.

Literature anchors (from PHENOMENA.md citations):
- 80% of resolutions fail by February (~60 days) [Oscarsson 2020]
- 54.7% still succeeding at 12 months for approach goals [Oscarsson 2020]
- 46% continuous success at 6 months [Norcross 2002]
- 25-45% maintain exercise at 1 year [Kwasnicka 2016]
- Median 66 days to habit formation [Lally 2010]
- ~8-10% achieve long-term goals across all resolution types

For a 2-year window with our diverse population:
- Expected habit_formed: 15-30% (some people have very favorable conditions)
- Expected sedentary/dropout: 40-60%
- Expected partial_habit: 10-20%
- Expected cycling (yo-yo): 5-15%
"""

import json
import sys
import os
import numpy as np
from pathlib import Path
from collections import defaultdict
from dataclasses import asdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'simulation'))
from dynamics import Params, SimState, HabitDynamics, Event


# Literature-based target outcome distributions
LITERATURE_TARGETS = {
    "overall": {
        "habit_formed": (0.15, 0.30),   # 15-30%
        "partial_habit": (0.10, 0.25),   # 10-25%
        "sedentary": (0.25, 0.45),       # 25-45%
        "dropout": (0.10, 0.25),         # 10-25%
        "false_hope_cycle": (0.03, 0.15),  # 3-15%
    },
    # Time-specific dropout rates
    "dropout_by_60_days": (0.50, 0.80),  # 50-80% have stopped by day 60
    "maintaining_at_180": (0.25, 0.50),  # 25-50% still going at 6 months
    "maintaining_at_365": (0.15, 0.35),  # 15-35% at 1 year
}


def classify_outcome(H_traj, M_traj, E_traj, B_traj):
    """Classify trajectory outcome with more nuanced categories."""
    n = len(H_traj)
    H_final = H_traj[-1]
    M_final = M_traj[-1]

    # Check last quarter behavior
    q3 = 3 * n // 4
    B_last_quarter = np.mean(B_traj[q3:])
    H_last_quarter = np.mean(H_traj[q3:])

    # Check for oscillations (false hope cycling)
    # Requires multiple LARGE M spikes with returns to low M between them
    # AND that these spikes led to some behavioral attempts (B > 0.3 briefly)
    M_peaks = 0
    for i in range(n // 8, n - n // 8):
        window = n // 15
        local_max = M_traj[i] > 0.5  # Peak must be substantial
        left_low = np.mean(M_traj[max(0, i-window):i]) < M_traj[i] * 0.5
        right_low = np.mean(M_traj[i:min(n, i+window)]) < M_traj[i] * 0.5
        if local_max and left_low and right_low:
            M_peaks += 1

    # Check if there were periods of behavioral activity that didn't stick
    active_windows = 0
    window_size = n // 20
    for w in range(0, n - window_size, window_size):
        if np.mean(B_traj[w:w+window_size]) > 0.3:
            active_windows += 1
    inactive_windows = (n // window_size) - active_windows

    # Classification
    if H_final > 0.5 and B_last_quarter > 0.4:
        return "habit_formed"
    elif H_final > 0.2 and B_last_quarter > 0.1:
        return "partial_habit"
    elif M_peaks >= 3 and active_windows >= 2 and inactive_windows >= 2 and H_final < 0.15:
        # True false hope: multiple start/stop cycles with genuine behavioral attempts
        return "false_hope_cycle"
    elif np.max(H_traj) > 0.15 and H_final < 0.1:
        return "dropout"
    else:
        return "sedentary"


def classify_at_timepoint(B_traj, day, dt=0.1):
    """Is the person still 'active' at a given day?"""
    idx = int(day / dt)
    if idx >= len(B_traj):
        idx = len(B_traj) - 1
    # Average B over a 7-day window around the timepoint
    window = int(7 / dt)
    start = max(0, idx - window)
    end = min(len(B_traj), idx + window)
    avg_B = np.mean(B_traj[start:end])
    return avg_B > 0.15  # "Active" if B > 0.15 on average


def person_to_params(person):
    """Convert a person descriptor to simulation Params."""
    return Params(
        C=person["complexity_target"],  # Initial C (also set on state)
        alpha_H=0.045,
        sigma_noise=0.02,
    )


def person_to_initial(person):
    """Create initial SimState from person descriptor, including dynamic C."""
    ic = person["initial"]
    return SimState(
        H=ic["H"], M=ic["M"], E=ic["E"], I=ic["I"],
        C=person["complexity_target"],  # C starts at the person's target complexity
    )


def stream_to_events(stream_events):
    """Convert event stream to simulation Event objects."""
    sim_events = []
    for e in stream_events:
        etype = e["type"]
        if etype == "new_year":
            sim_events.append(Event(e["time"], "new_year", e["amplitude"], label=e["label"]))
        elif etype == "injury":
            sim_events.append(Event(e["time"], "injury_start", 1, label=e["label"]))
        elif etype == "heal":
            sim_events.append(Event(e["time"], "injury_end", 1, label=e["label"]))
        elif etype in ("shock", "stress", "lapse", "social", "context_disruption",
                        "simplify", "escalate"):
            sim_events.append(Event(e["time"], etype, e["amplitude"], label=e["label"]))
    return sim_events


def run_single(person, stream, params):
    """Run a single person x stream simulation."""
    initial = person_to_initial(person)
    events = stream_to_events(stream["events"])

    sim = HabitDynamics(params, events)
    result = sim.simulate(initial, t_end=730, dt=0.1, seed=stream["stream_idx"])

    outcome = classify_outcome(result["H"], result["M"], result["E"], result["B"])

    # Check timepoint metrics
    active_60 = classify_at_timepoint(result["B"], 60)
    active_180 = classify_at_timepoint(result["B"], 180)
    active_365 = classify_at_timepoint(result["B"], 365)

    return {
        "outcome": outcome,
        "active_60": active_60,
        "active_180": active_180,
        "active_365": active_365,
        "H_final": float(result["H"][-1]),
        "M_final": float(result["M"][-1]),
        "I_final": float(result["I"][-1]),
        "C_final": float(result["C"][-1]),
        "C_min_reached": float(np.min(result["C"])),
        "H_max": float(np.max(result["H"])),
        "B_mean": float(np.mean(result["B"])),
        "archetype": stream["archetype"],
        "n_events": stream["n_events"],
    }


def main():
    # Load event streams
    streams_path = Path(__file__).parent / "results" / "event_streams.json"
    if not streams_path.exists():
        print("Generating event streams first...")
        from event_generator import generate_all_streams
        stream_data = generate_all_streams(n_per_person=100)
        with open(streams_path, "w") as f:
            json.dump(stream_data, f, separators=(",", ":"))
    else:
        print(f"Loading event streams from {streams_path}...")
        with open(streams_path) as f:
            stream_data = json.load(f)

    results = {}
    overall_outcomes = defaultdict(int)
    overall_active_60 = 0
    overall_active_180 = 0
    overall_active_365 = 0
    total_sims = 0

    from persons import PERSONS
    person_lookup = {p["id"]: p for p in PERSONS}

    for pid, pdata in stream_data.items():
        print(f"\nRunning {pid} ({len(pdata['streams'])} streams)...")
        person = person_lookup[pid]
        params = person_to_params(person)

        person_outcomes = defaultdict(int)
        person_results = []

        for stream in pdata["streams"]:
            r = run_single(person, stream, params)
            person_results.append(r)
            person_outcomes[r["outcome"]] += 1
            overall_outcomes[r["outcome"]] += 1
            if r["active_60"]: overall_active_60 += 1
            if r["active_180"]: overall_active_180 += 1
            if r["active_365"]: overall_active_365 += 1
            total_sims += 1

        n = len(person_results)
        results[pid] = {
            "person_name": person["name"],
            "backstory": person["backstory"][:100] + "...",
            "complexity": person["complexity_target"],
            "outcomes": dict(person_outcomes),
            "pct_habit_formed": person_outcomes["habit_formed"] / n * 100,
            "pct_active_180": sum(1 for r in person_results if r["active_180"]) / n * 100,
            "pct_active_365": sum(1 for r in person_results if r["active_365"]) / n * 100,
            "avg_H_final": np.mean([r["H_final"] for r in person_results]),
            "avg_I_final": np.mean([r["I_final"] for r in person_results]),
            "by_archetype": _group_by_archetype(person_results),
        }

        # Print summary
        print(f"  Outcomes: {dict(person_outcomes)}")
        print(f"  Habit formed: {results[pid]['pct_habit_formed']:.0f}%, "
              f"Active@180d: {results[pid]['pct_active_180']:.0f}%, "
              f"Active@365d: {results[pid]['pct_active_365']:.0f}%")

    # Overall statistics
    print("\n" + "=" * 70)
    print("OVERALL CALIBRATION RESULTS")
    print("=" * 70)

    overall_pcts = {k: v / total_sims * 100 for k, v in overall_outcomes.items()}
    pct_60 = overall_active_60 / total_sims * 100
    pct_180 = overall_active_180 / total_sims * 100
    pct_365 = overall_active_365 / total_sims * 100

    print(f"\nTotal simulations: {total_sims}")
    print(f"\nOutcome distribution:")
    for outcome, pct in sorted(overall_pcts.items(), key=lambda x: -x[1]):
        target = LITERATURE_TARGETS["overall"].get(outcome, (None, None))
        in_range = ""
        if target[0] is not None:
            lo, hi = target[0] * 100, target[1] * 100
            in_range = f"  [target: {lo:.0f}-{hi:.0f}%]"
            if lo <= pct <= hi:
                in_range += " OK"
            elif pct < lo:
                in_range += " LOW"
            else:
                in_range += " HIGH"
        print(f"  {outcome:20s}: {pct:5.1f}%{in_range}")

    print(f"\nTimepoint activity rates:")
    t60 = LITERATURE_TARGETS["dropout_by_60_days"]
    t180 = LITERATURE_TARGETS["maintaining_at_180"]
    t365 = LITERATURE_TARGETS["maintaining_at_365"]
    dropout_60 = 100 - pct_60

    def check(val, lo, hi):
        if lo * 100 <= val <= hi * 100: return "OK"
        elif val < lo * 100: return "LOW"
        else: return "HIGH"

    print(f"  Dropped by day 60:  {dropout_60:5.1f}%  [target: {t60[0]*100:.0f}-{t60[1]*100:.0f}%] {check(dropout_60, t60[0], t60[1])}")
    print(f"  Active at day 180:  {pct_180:5.1f}%  [target: {t180[0]*100:.0f}-{t180[1]*100:.0f}%] {check(pct_180, t180[0], t180[1])}")
    print(f"  Active at day 365:  {pct_365:5.1f}%  [target: {t365[0]*100:.0f}-{t365[1]*100:.0f}%] {check(pct_365, t365[0], t365[1])}")

    # Save results
    output = {
        "summary": {
            "total_sims": total_sims,
            "outcome_pcts": overall_pcts,
            "active_60_pct": pct_60,
            "active_180_pct": pct_180,
            "active_365_pct": pct_365,
            "literature_targets": {k: list(v) if isinstance(v, tuple) else
                                   {k2: list(v2) for k2, v2 in v.items()}
                                   for k, v in LITERATURE_TARGETS.items()},
        },
        "by_person": results,
    }

    outpath = Path(__file__).parent / "results" / "calibration_results.json"
    with open(outpath, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nResults saved to {outpath}")

    # Generate report
    _generate_report(output, results)


def _group_by_archetype(person_results):
    groups = defaultdict(lambda: {"count": 0, "habit_formed": 0})
    for r in person_results:
        a = r["archetype"]
        groups[a]["count"] += 1
        if r["outcome"] == "habit_formed":
            groups[a]["habit_formed"] += 1
    return {k: {**v, "success_rate": v["habit_formed"] / v["count"] * 100 if v["count"] > 0 else 0}
            for k, v in groups.items()}


def _generate_report(output, results):
    """Generate a human-readable calibration report."""
    report = []
    report.append("# Synthetic Narrative Calibration Report\n")
    report.append(f"Total simulations: {output['summary']['total_sims']}\n")
    report.append(f"Persons: {len(results)}, Streams per person: 100\n")
    report.append(f"Simulation period: 730 days (2 years)\n\n")

    report.append("## Methodology\n\n")
    report.append("1. **Person backstories**: 20 diverse individuals with varying demographics,\n")
    report.append("   fitness goals, life stressors, and prior fitness levels.\n")
    report.append("2. **Archetype-weighted generation**: Each person has a probability distribution\n")
    report.append("   over 10 trajectory archetypes (STEADY_BUILDER, FALSE_STARTER, etc.).\n")
    report.append("3. **Event streams**: Generated via inhomogeneous Poisson processes with rates\n")
    report.append("   biased by person backstory and archetype. Includes seasonal effects,\n")
    report.append("   autoregressive stress clustering, and conditional lapse generation.\n")
    report.append("4. **Validation**: Each stream checked for plausibility (event counts, temporal\n")
    report.append("   spread, injury/heal balance).\n")
    report.append("5. **Calibration targets**: Derived from Oscarsson 2020, Norcross 2002,\n")
    report.append("   Kwasnicka 2016, Lally 2010.\n\n")

    report.append("## Overall Results vs Literature Targets\n\n")
    report.append("| Metric | Observed | Target | Status |\n")
    report.append("|--------|----------|--------|--------|\n")

    s = output["summary"]
    for outcome in ["habit_formed", "partial_habit", "sedentary", "dropout", "false_hope_cycle"]:
        obs = s["outcome_pcts"].get(outcome, 0)
        tgt = s["literature_targets"]["overall"].get(outcome, [None, None])
        if tgt[0] is not None:
            status = "OK" if tgt[0]*100 <= obs <= tgt[1]*100 else ("LOW" if obs < tgt[0]*100 else "HIGH")
            report.append(f"| {outcome} | {obs:.1f}% | {tgt[0]*100:.0f}-{tgt[1]*100:.0f}% | {status} |\n")

    dropout_60 = 100 - s["active_60_pct"]
    report.append(f"| Dropped by d60 | {dropout_60:.1f}% | 50-80% | {'OK' if 50<=dropout_60<=80 else 'MISS'} |\n")
    report.append(f"| Active at d180 | {s['active_180_pct']:.1f}% | 25-50% | {'OK' if 25<=s['active_180_pct']<=50 else 'MISS'} |\n")
    report.append(f"| Active at d365 | {s['active_365_pct']:.1f}% | 15-35% | {'OK' if 15<=s['active_365_pct']<=35 else 'MISS'} |\n\n")

    report.append("## Per-Person Results\n\n")
    for pid, r in sorted(results.items(), key=lambda x: -x[1]["pct_habit_formed"]):
        report.append(f"### {r['person_name']} ({pid})\n")
        report.append(f"- C={r['complexity']}, Habit formed: {r['pct_habit_formed']:.0f}%\n")
        report.append(f"- Active@180d: {r['pct_active_180']:.0f}%, Active@365d: {r['pct_active_365']:.0f}%\n")
        report.append(f"- Avg H_final: {r['avg_H_final']:.2f}, Avg I_final: {r['avg_I_final']:.2f}\n")
        report.append(f"- Outcomes: {r['outcomes']}\n")
        if r.get("by_archetype"):
            best = max(r["by_archetype"].items(), key=lambda x: x[1]["success_rate"])
            worst = min(r["by_archetype"].items(), key=lambda x: x[1]["success_rate"])
            report.append(f"- Best archetype: {best[0]} ({best[1]['success_rate']:.0f}% success)\n")
            report.append(f"- Worst archetype: {worst[0]} ({worst[1]['success_rate']:.0f}% success)\n")
        report.append("\n")

    report_path = Path(__file__).parent / "results" / "calibration_report.md"
    with open(report_path, "w") as f:
        f.writelines(report)
    print(f"Report saved to {report_path}")


if __name__ == "__main__":
    main()
