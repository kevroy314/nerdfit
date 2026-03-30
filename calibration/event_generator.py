"""
Generate plausible 2-year event streams for each person backstory.

Design:
- Events are drawn from inhomogeneous Poisson processes with rates biased by backstory
- Temporal clustering: stressors can come in bursts (autoregressive intensity)
- Seasonal effects: New Year's motivation, summer body, holiday stress
- Life phase events: some people get contextual disruptions at predictable times
- Lapse events: triggered probabilistically when B is low (estimated from H and M)

Taxonomy of trajectory archetypes (used to ensure diverse coverage):
1. STEADY_BUILDER: Low stress, consistent, gradual success
2. SLOW_GRINDER: High stress but persistent, eventual success
3. FALSE_STARTER: High initial M, crashes within 1-3 months
4. YO_YO: Repeated cycles of start/stop, possibly eventual success
5. CRISIS_INTERRUPTED: Making progress, derailed by major event
6. SOCIAL_CATALYZED: Social events are the key driver
7. INJURY_DERAILED: Physical setback is the main obstacle
8. COMPLEXITY_TRAPPED: Overcomplicated from the start
9. INDULGENCE_FADE: Fantasy substitutes for action
10. LATE_BLOOMER: Fails initially, succeeds on a later attempt
"""

import json
import numpy as np
from pathlib import Path
from persons import PERSONS


# Seasonal modifiers (day of year -> modifier)
def seasonal_motivation(day_of_year):
    """New Year's spike, summer body, fall restart. Returns [0,1] modifier."""
    # Jan spike
    jan = np.exp(-((day_of_year % 365) / 15) ** 2) * 0.8
    # Summer body (April-May)
    summer = np.exp(-(((day_of_year % 365) - 120) / 20) ** 2) * 0.4
    # Fall restart (September)
    fall = np.exp(-(((day_of_year % 365) - 250) / 15) ** 2) * 0.3
    return jan + summer + fall


def seasonal_stress(day_of_year):
    """Holiday stress (Nov-Dec), tax season, end-of-semester."""
    holidays = np.exp(-(((day_of_year % 365) - 340) / 25) ** 2) * 0.5
    return holidays


# Event strength distributions per type
STRENGTH_DISTRIBUTIONS = {
    "shock": {
        "weights": [0.3, 0.3, 0.25, 0.1, 0.05],  # Most shocks are mild
    },
    "stress": {
        "weights": [0.25, 0.35, 0.25, 0.1, 0.05],
    },
    "lapse": {
        "weights": [0.3, 0.3, 0.2, 0.15, 0.05],
    },
    "context": {
        "weights": [0.35, 0.3, 0.2, 0.1, 0.05],
    },
    "social": {
        "weights": [0.3, 0.3, 0.25, 0.1, 0.05],
    },
    "injury": {
        "weights": [0.4, 0.3, 0.15, 0.1, 0.05],
    },
    "simplify": {
        "weights": [0.3, 0.35, 0.2, 0.1, 0.05],
    },
    "escalate": {
        "weights": [0.25, 0.35, 0.25, 0.1, 0.05],
    },
}

# Amplitude tables (strength level -> amplitude) matching events.js catalog
AMPLITUDE_TABLE = {
    "shock":     [0.3, 0.8, 1.5, 2.5, 4.0],
    "lapse":     [0.3, 0.7, 1.2, 1.8, 2.5],
    "stress":    [0.2, 0.4, 0.7, 0.9, 1.0],
    "context":   [0.15, 0.3, 0.5, 0.7, 0.85],
    "social":    [0.2, 0.5, 0.8, 1.2, 1.8],
    "injury":    [1, 1, 1, 1, 1],
    "heal":      [1, 1, 1, 1, 1],
    "simplify":  [0.5, 1.0, 1.5, 2.0, 3.0],  # How much C drops
    "escalate":  [0.3, 0.6, 1.0, 1.5, 2.0],  # How much C rises
}

# Injury durations (days) by strength
INJURY_DURATIONS = [10, 25, 50, 90, 180]

# Label tables matching events.js
LABEL_TABLE = {
    "shock": [
        "Saw motivating post online",
        "Inspiring conversation",
        "New Year's resolution",
        "Doctor's warning",
        "Life-threatening health scare",
    ],
    "lapse": [
        "Skipped one session",
        "Missed a few days",
        "Broke the streak",
        "Full diet break at party",
        "Complete abandonment event",
    ],
    "stress": [
        "Bad day at work",
        "Week-long work crunch",
        "Relationship conflict",
        "Job loss",
        "Major life crisis",
    ],
    "context": [
        "Schedule change",
        "Gym closed",
        "Moved to new neighborhood",
        "Moved to new city",
        "Complete life restructuring",
    ],
    "social": [
        "Compliment from friend",
        "Workout buddy invitation",
        "Joined a group/class",
        "Coach/trainer engagement",
        "Deep community integration",
    ],
    "injury": [
        "Minor strain (1-2 weeks)",
        "Moderate injury (3-4 weeks)",
        "Significant injury (6-8 weeks)",
        "Major injury (3 months)",
        "Severe injury (6+ months)",
    ],
    "simplify": [
        "Thought 'maybe I should start smaller'",
        "Friend suggested just walking",
        "Read article about habit stacking",
        "Coach said 'drop the program, just show up'",
        "Therapist prescribed Tiny Habits approach",
    ],
    "escalate": [
        "Saw advanced workout on Instagram",
        "Friend invited to intense class",
        "Signed up for a race/challenge",
        "Bought comprehensive training program",
        "Hired trainer with ambitious periodization",
    ],
}


TRAJECTORY_ARCHETYPES = [
    "STEADY_BUILDER",
    "SLOW_GRINDER",
    "FALSE_STARTER",
    "YO_YO",
    "CRISIS_INTERRUPTED",
    "SOCIAL_CATALYZED",
    "INJURY_DERAILED",
    "COMPLEXITY_TRAPPED",
    "INDULGENCE_FADE",
    "LATE_BLOOMER",
]


def assign_archetype_weights(person):
    """Given a person's backstory, assign probability weights to archetypes."""
    w = np.ones(len(TRAJECTORY_ARCHETYPES))

    C = person["complexity_target"]
    stab = person["life_stability"]
    social = person["social_support"]
    prior = person["prior_fitness"]
    lapse_v = person["event_rates"]["lapse_vulnerability"]
    stress_r = person["event_rates"]["stress_base"]
    injury_r = person["event_rates"]["injury_base"]
    M0 = person["initial"]["M"]
    E0 = person["initial"]["E"]

    # STEADY_BUILDER: stable life, low complexity, moderate M
    w[0] = stab * (1 - C) * (1 - lapse_v)

    # SLOW_GRINDER: high stress but persistent
    w[1] = stress_r * (1 - lapse_v) * prior

    # FALSE_STARTER: high M, high E, high C
    w[2] = M0 * max(0, E0) * C * lapse_v

    # YO_YO: repeated attempts (high shock rate, high lapse rate)
    shock_r = person["event_rates"]["shock_positive_base"]
    w[3] = shock_r * lapse_v

    # CRISIS_INTERRUPTED: moderate setup + high stress
    w[4] = stress_r * (1 - C) * 0.5

    # SOCIAL_CATALYZED: high social support
    w[5] = social * person["event_rates"]["social_base"] * 5

    # INJURY_DERAILED: high injury rate
    w[6] = injury_r * 50

    # COMPLEXITY_TRAPPED: high C, low prior
    w[7] = C * (1 - prior)

    # INDULGENCE_FADE: moderate M, high f0 tendency
    w[8] = (1 - prior) * (1 - stab) * 0.3

    # LATE_BLOOMER: multiple attempts lead to eventual success
    w[9] = lapse_v * prior * 0.5

    # Normalize
    w = w / w.sum()
    return w


def generate_event_stream(person, archetype, rng, stream_idx=0):
    """Generate a single 2-year (730 day) event stream for a person+archetype."""
    T = 730  # days
    events = []
    rates = person["event_rates"]

    # Base rates (events per day)
    stress_rate = rates["stress_base"]
    shock_rate = rates["shock_positive_base"]
    social_rate = rates["social_base"]
    ctx_rate = rates["context_disruption_base"]
    injury_rate = rates["injury_base"]
    lapse_vuln = rates["lapse_vulnerability"]

    # Archetype-specific rate modifiers
    mods = _archetype_modifiers(archetype)

    # Track state for conditional events
    injured = False
    injury_heal_day = 0
    stress_accumulator = 0.0  # Autoregressive stress intensity
    streak_days = 0  # Approximate behavioral streak for lapse triggering
    had_initial_shock = False

    for day in range(T):
        day_events = []
        doy = day % 365

        # Seasonal modifiers
        seas_m = seasonal_motivation(doy)
        seas_s = seasonal_stress(doy)

        # Stress events (Poisson with autoregressive intensity)
        # Cap total intensity to prevent runaway stress cascades
        stress_intensity = min(0.15, stress_rate * mods["stress"] * (1 + seas_s * 0.5 + stress_accumulator * 0.5))
        if rng.random() < stress_intensity:
            strength = _sample_strength(rng, "stress", mods.get("stress_severity", None))
            day_events.append({
                "time": day,
                "type": "stress",
                "strength": strength,
                "amplitude": AMPLITUDE_TABLE["stress"][strength - 1],
                "label": LABEL_TABLE["stress"][strength - 1],
            })
            stress_accumulator += 0.08 * strength  # Stress breeds stress (reduced)
            streak_days = max(0, streak_days - strength * 3)

        stress_accumulator *= 0.93  # Faster decay of stress cascade

        # Motivational shocks (Poisson + seasonal)
        shock_intensity = shock_rate * mods["shock"] * (1 + seas_m * 3)
        # New Year's and fresh starts
        if doy == 0 or doy == 1:
            shock_intensity += 0.5 * mods["shock"]
        if rng.random() < shock_intensity:
            strength = _sample_strength(rng, "shock", mods.get("shock_severity", None))
            day_events.append({
                "time": day,
                "type": "shock" if doy > 5 else "new_year",
                "strength": strength,
                "amplitude": AMPLITUDE_TABLE["shock"][strength - 1],
                "label": LABEL_TABLE["shock"][strength - 1],
            })
            had_initial_shock = True

        # Social events
        social_intensity = social_rate * mods["social"]
        if rng.random() < social_intensity:
            strength = _sample_strength(rng, "social")
            day_events.append({
                "time": day,
                "type": "social",
                "strength": strength,
                "amplitude": AMPLITUDE_TABLE["social"][strength - 1],
                "label": LABEL_TABLE["social"][strength - 1],
            })
            streak_days += 2

        # Context disruptions
        ctx_intensity = ctx_rate * mods["context"]
        if rng.random() < ctx_intensity:
            strength = _sample_strength(rng, "context")
            day_events.append({
                "time": day,
                "type": "context_disruption",
                "strength": strength,
                "amplitude": AMPLITUDE_TABLE["context"][strength - 1],
                "label": LABEL_TABLE["context"][strength - 1],
            })
            streak_days = 0

        # Injury events
        if not injured:
            inj_intensity = injury_rate * mods["injury"]
            if rng.random() < inj_intensity:
                strength = _sample_strength(rng, "injury", mods.get("injury_severity", None))
                duration = INJURY_DURATIONS[strength - 1]
                duration = int(duration * rng.uniform(0.7, 1.3))  # Some variance
                day_events.append({
                    "time": day,
                    "type": "injury",
                    "strength": strength,
                    "amplitude": 1,
                    "label": LABEL_TABLE["injury"][strength - 1],
                })
                injured = True
                injury_heal_day = day + duration
                streak_days = 0
        elif injured and day >= injury_heal_day:
            day_events.append({
                "time": day,
                "type": "heal",
                "strength": 3,
                "amplitude": 1,
                "label": "Cleared to resume",
            })
            injured = False

        # Lapse events: conditional on estimated behavioral state
        # Higher probability when streak is short and vulnerability is high
        # Cap at ~2 per month max to avoid event floods
        if not injured and streak_days < 10:
            lapse_prob = min(0.06, lapse_vuln * mods["lapse"] * 0.01 * max(1, 3 - streak_days * 0.5))
            if rng.random() < lapse_prob:
                strength = _sample_strength(rng, "lapse")
                day_events.append({
                    "time": day,
                    "type": "lapse",
                    "strength": strength,
                    "amplitude": AMPLITUDE_TABLE["lapse"][strength - 1],
                    "label": LABEL_TABLE["lapse"][strength - 1],
                })
                streak_days = 0

        # Simplify events: triggered by sustained failure (low streak, many recent stressors)
        # People don't simplify immediately -- it takes weeks of not succeeding before
        # the "maybe I should just start walking" realization occurs
        if day > 30 and streak_days < 3 and stress_accumulator > 0.1:
            # Probability increases with how long things have been going badly
            simplify_prob = 0.003 * mods.get("simplify", 1.0) * (1 + social_rate * 10)
            if rng.random() < simplify_prob:
                strength = _sample_strength(rng, "simplify")
                day_events.append({
                    "time": day,
                    "type": "simplify",
                    "strength": strength,
                    "amplitude": AMPLITUDE_TABLE["simplify"][strength - 1],
                    "label": LABEL_TABLE["simplify"][strength - 1],
                })

        # Escalate events: triggered by success (long streaks)
        # "I've been walking for a month, maybe I should try the gym"
        if streak_days > 20:
            escalate_prob = 0.002 * mods.get("escalate", 1.0)
            if rng.random() < escalate_prob:
                strength = _sample_strength(rng, "escalate")
                day_events.append({
                    "time": day,
                    "type": "escalate",
                    "strength": strength,
                    "amplitude": AMPLITUDE_TABLE["escalate"][strength - 1],
                    "label": LABEL_TABLE["escalate"][strength - 1],
                })

        # Update streak estimate (crude: assume behavior occurs if no stress/lapse today)
        if not day_events or all(e["type"] in ("shock", "social", "new_year", "simplify") for e in day_events):
            streak_days += 1

        events.extend(day_events)

    # Ensure initial shock for archetypes that need a trigger
    if archetype in ("FALSE_STARTER", "COMPLEXITY_TRAPPED") and not had_initial_shock:
        strength = min(5, max(3, int(person["initial"]["M"] * 2.5)))
        events.insert(0, {
            "time": 0,
            "type": "new_year",
            "strength": strength,
            "amplitude": AMPLITUDE_TABLE["shock"][strength - 1],
            "label": "Initial commitment",
        })

    # Sort by time
    events.sort(key=lambda e: e["time"])

    return events


def _archetype_modifiers(archetype):
    """Return rate multipliers for each event type given an archetype."""
    base = {
        "stress": 1.0, "shock": 1.0, "social": 1.0, "context": 1.0,
        "injury": 1.0, "lapse": 1.0,
    }
    if archetype == "STEADY_BUILDER":
        base["stress"] = 0.5
        base["lapse"] = 0.4
        base["social"] = 1.5
    elif archetype == "SLOW_GRINDER":
        base["stress"] = 1.3
        base["lapse"] = 0.6
        base["shock"] = 0.8
    elif archetype == "FALSE_STARTER":
        base["shock"] = 1.5
        base["lapse"] = 1.5
        base["shock_severity"] = [0.05, 0.1, 0.3, 0.35, 0.2]  # Biased high
    elif archetype == "YO_YO":
        base["shock"] = 2.0
        base["lapse"] = 1.3
        base["stress"] = 1.2
    elif archetype == "CRISIS_INTERRUPTED":
        base["stress"] = 1.5
        base["stress_severity"] = [0.1, 0.15, 0.25, 0.3, 0.2]  # At least one big one
        base["lapse"] = 0.8
    elif archetype == "SOCIAL_CATALYZED":
        base["social"] = 3.0
        base["lapse"] = 0.6
        base["stress"] = 0.7
    elif archetype == "INJURY_DERAILED":
        base["injury"] = 3.0
        base["injury_severity"] = [0.1, 0.2, 0.3, 0.25, 0.15]  # Biased toward severe
    elif archetype == "COMPLEXITY_TRAPPED":
        base["lapse"] = 1.4
        base["stress"] = 1.1
    elif archetype == "INDULGENCE_FADE":
        base["shock"] = 0.7
        base["social"] = 0.5
        base["lapse"] = 1.2
    elif archetype == "LATE_BLOOMER":
        base["shock"] = 1.5
        base["lapse"] = 1.0
        base["social"] = 1.3
    return base


def _sample_strength(rng, event_type, custom_weights=None):
    """Sample a strength level 1-5."""
    if custom_weights is not None:
        weights = np.array(custom_weights)
    else:
        weights = np.array(STRENGTH_DISTRIBUTIONS[event_type]["weights"])
    weights = weights / weights.sum()
    return int(rng.choice([1, 2, 3, 4, 5], p=weights))


def validate_stream(events, person):
    """Check a stream for basic plausibility."""
    issues = []
    T = 730

    # Count by type
    counts = {}
    for e in events:
        t = e["type"]
        counts[t] = counts.get(t, 0) + 1

    total = len(events)
    if total < 5:
        issues.append(f"Too few events ({total})")
    if total > 500:
        issues.append(f"Suspiciously many events ({total})")

    # Check injury/heal balance
    injuries = sum(1 for e in events if e["type"] == "injury")
    heals = sum(1 for e in events if e["type"] == "heal")
    if injuries > heals + 1:
        issues.append(f"Unhealed injuries: {injuries} injuries vs {heals} heals")

    # Check temporal spread
    if events:
        times = [e["time"] for e in events]
        first_half = sum(1 for t in times if t < T / 2)
        second_half = total - first_half
        if first_half > 0 and second_half > 0:
            ratio = first_half / second_half
            if ratio > 5 or ratio < 0.2:
                issues.append(f"Temporal imbalance: {first_half} vs {second_half}")

    return issues


def generate_all_streams(n_per_person=100, seed=42):
    """Generate event streams for all persons."""
    rng = np.random.default_rng(seed)
    all_data = {}

    for person in PERSONS:
        pid = person["id"]
        archetype_weights = assign_archetype_weights(person)

        streams = []
        archetype_counts = {}

        # Guarantee minimum representation of positive-outcome archetypes
        # At least 10% STEADY_BUILDER, 5% SOCIAL_CATALYZED, 5% LATE_BLOOMER
        # This ensures every person has some plausible success scenarios
        forced_archetypes = (
            ["STEADY_BUILDER"] * max(1, n_per_person // 10)
            + ["SOCIAL_CATALYZED"] * max(1, n_per_person // 20)
            + ["LATE_BLOOMER"] * max(1, n_per_person // 20)
        )
        forced_indices = list(range(len(forced_archetypes)))
        rng.shuffle(forced_indices)
        forced_map = {forced_indices[j]: forced_archetypes[j]
                      for j in range(len(forced_archetypes))}

        for i in range(n_per_person):
            # Use forced archetype if assigned, otherwise sample
            if i in forced_map:
                archetype = forced_map[i]
            else:
                archetype = rng.choice(TRAJECTORY_ARCHETYPES, p=archetype_weights)
            archetype_counts[archetype] = archetype_counts.get(archetype, 0) + 1

            events = generate_event_stream(person, archetype, rng, stream_idx=i)
            issues = validate_stream(events, person)

            # Regenerate if problematic (up to 3 tries)
            attempts = 0
            while issues and attempts < 3:
                events = generate_event_stream(person, archetype, rng, stream_idx=i)
                issues = validate_stream(events, person)
                attempts += 1

            streams.append({
                "stream_idx": i,
                "archetype": archetype,
                "events": events,
                "n_events": len(events),
                "validation_issues": issues,
            })

        all_data[pid] = {
            "person": {k: v for k, v in person.items() if k != "event_rates"},
            "event_rates": person["event_rates"],
            "archetype_distribution": archetype_counts,
            "streams": streams,
        }

        print(f"  {pid}: {n_per_person} streams, archetypes: {archetype_counts}")

    return all_data


if __name__ == "__main__":
    print("Generating event streams...")
    data = generate_all_streams(n_per_person=100)

    outpath = Path(__file__).parent / "results" / "event_streams.json"
    outpath.parent.mkdir(exist_ok=True)

    # Save compact (events are the bulk)
    with open(outpath, "w") as f:
        json.dump(data, f, separators=(",", ":"))
    size_mb = outpath.stat().st_size / 1024 / 1024
    print(f"Saved to {outpath} ({size_mb:.1f} MB)")
