# Synthetic Narrative Calibration Method

## Overview

This calibration system validates the H-M-E-I dynamical systems model against
literature-derived population-level outcome statistics by generating diverse,
plausible 2-year life event streams for synthetic individuals and comparing
simulated outcomes against empirical targets.

## Pipeline

```
persons.py          -> 21 backstory descriptors (demographics, goals, event rates)
event_generator.py  -> 100 event streams per person (Poisson + archetype-weighted)
run_calibration.py  -> 2100 simulations -> outcome classification -> comparison to targets
```

## Key Design Decisions

### Person Backstories (persons.py)
- 21 individuals spanning ages 19-67, multiple genders, occupations, fitness goals
- Each person has derived `event_rates` (stress, shock, social, injury, etc.) that
  reflect their life context
- Initial conditions (H, M, E, I) derived from backstory, not arbitrary
- `complexity_target` (C parameter) reflects the fitness goal's inherent difficulty

### Archetype-Weighted Generation (event_generator.py)
Rather than purely random event streams, each person has a probability distribution
over 10 trajectory archetypes:

1. STEADY_BUILDER: Low stress, consistent, gradual success
2. SLOW_GRINDER: High stress but persistent, eventual success
3. FALSE_STARTER: High initial M, crashes within 1-3 months
4. YO_YO: Repeated cycles of start/stop
5. CRISIS_INTERRUPTED: Making progress, derailed by major event
6. SOCIAL_CATALYZED: Social events are the key driver
7. INJURY_DERAILED: Physical setback is the main obstacle
8. COMPLEXITY_TRAPPED: Overcomplicated from the start
9. INDULGENCE_FADE: Fantasy substitutes for action
10. LATE_BLOOMER: Fails initially, succeeds on a later attempt

Each person gets at least 10% STEADY_BUILDER + 5% SOCIAL_CATALYZED + 5% LATE_BLOOMER
streams to ensure some positive-outcome scenarios regardless of backstory.

Archetype weights are derived from person attributes (e.g., high C + low prior fitness
biases toward COMPLEXITY_TRAPPED and FALSE_STARTER).

### Event Generation
- **Inhomogeneous Poisson processes** with rates modulated by:
  - Person backstory (base rates)
  - Archetype (rate multipliers)
  - Seasonal effects (New Year motivation, holiday stress)
  - Autoregressive stress clustering (stress breeds stress, decays over time)
- **Conditional lapse generation**: lapses are more likely when estimated behavioral
  streak is short
- **Injury/heal pairing**: injuries have duration, healing happens automatically
- **Strength levels 1-5**: each event type has a strength distribution; higher
  archetypes bias toward more severe events

### Validation
Each stream is checked for:
- Total event count (5-500 range)
- Temporal spread (not all front-loaded or back-loaded)
- Injury/heal balance

### Literature Calibration Targets
From Oscarsson 2020, Norcross 2002, Kwasnicka 2016, Lally 2010:

| Metric | Target Range | Source |
|--------|-------------|--------|
| habit_formed | 15-30% | Kwasnicka 2016, Norcross 2002 |
| partial_habit | 10-25% | Estimated from partial maintainers |
| sedentary | 25-45% | Never-starters + early dropouts |
| dropout | 10-25% | Oscarsson 2020 (attrition curve) |
| false_hope_cycle | 3-15% | Polivy & Herman 2002 (subset) |
| Dropped by d60 | 50-80% | ~80% fail by February |
| Active at d180 | 25-50% | 46% at 6mo (Norcross) |
| Active at d365 | 15-35% | 25-45% at 1yr (Kwasnicka) |

## Calibration History

### Round 1 (initial)
- false_hope_cycle: 72.7% (target 3-15%) -- **WAY HIGH**
- Root cause: (a) classifier too sensitive, (b) events applied as rates not impulses,
  (c) stress events too frequent due to autoregressive compounding

### Round 2
- Fixes: tighter classifier, capped stress rates, added social_support state variable
- Results: 4/8 metrics in range (habit_formed=15.6%, false_hope=13.6%, d60=65.2%, d180=29.6%)
- Remaining issues: Active@d365 too high (59.6%), sedentary too low (19.1%)

### Round 3 (current -- dynamic C)
- Fixes: C made a dynamic state variable with equilibrium-based adaptation, simplify/escalate
  events added to event generator, C-M coupling (simplifying boosts M)
- Results: 5/8 metrics in range
  - habit_formed: 33.0% (target 15-30%, slightly high)
  - partial_habit: 32.4% (target 10-25%, high)
  - sedentary: 15.8% (target 25-45%, low)
  - dropout: 10.0% (target 10-25%, OK)
  - false_hope_cycle: 8.7% (target 3-15%, OK)
  - Dropped by d60: 63.4% (target 50-80%, OK)
  - Active at d180: 39.9% (target 25-50%, OK)
  - Active at d365: 69.9% (target 15-35%, high)
- Key insight: Dynamic C creates meaningful H-C co-equilibria. The phase portrait
  shows distinct attractor regions (stable habit, complexity trap, sedentary)
  with a sharp separatrix. See simulation/results/hc_phase_portrait.png.

## Reproduction

```bash
cd calibration/
rm -f results/event_streams.json  # Force regeneration
python3 run_calibration.py
# Results in results/calibration_report.md
```

## File Structure

```
calibration/
  README.md                          # This file
  persons.py                         # 21 person backstory descriptors
  event_generator.py                 # Poisson event stream generator
  run_calibration.py                 # Simulation runner + outcome analysis
  results/
    event_streams.json               # Generated event streams (~80MB)
    calibration_results.json         # Outcome statistics per person
    calibration_report.md            # Human-readable report
```
