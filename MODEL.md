# Dynamical Systems Model of Habit Formation (v3)

A 5-variable dynamical system modeling habit formation, failure, and adaptation.
Grounded in literature from performance psychology, affective dynamics, and
neuroscience of reward signaling. See PHENOMENA.md for the 35 target phenomena
and citations/ for source material.

Reference implementation: `simulation/dynamics.py`
Browser implementation: `visualizer/dynamics.js`

---

## State Variables

| Variable | Range | Interpretation | Timescale |
|----------|-------|---------------|-----------|
| **H** | [H_min, 1] | Habit strength (instigation automaticity) | Weeks-months |
| **M** | [0, inf) | Motivational activation | Hours-days |
| **E** | (-inf, inf) | Expectation excess (positive = inflated) | Days-weeks |
| **I** | [0, 1] | Identity coherence ("I am someone who does this") | Months-years |
| **C** | [C_min, C_max] | Behavioral complexity (dynamic, adapts to H) | Weeks-months |

Plus transient state: `stress` (decays ~10d), `ii_active` (implementation intention, decays ~20d), `social_support` (decays very slowly ~330d), `injured` (boolean).

---

## Parameters

| Symbol | Default | Interpretation |
|--------|---------|---------------|
| C_min | 0.1 | Minimum complexity ("take a walk") |
| C_max | 0.95 | Maximum complexity |
| alpha_C_down | 0.003 | Rate C decreases under failure |
| alpha_C_up | 0.001 | Rate C increases under success (slower) |
| A_base | 0.8 | Base habit ceiling (I raises it) |
| alpha_H | 0.045 | Habit growth rate (~66d to 95% at B=1, per Lally 2010) |
| delta_H | 0.01 | Habit decay base rate |
| H_min | 0.02 | Residual habit floor (habits never fully vanish, Edgren 2025) |
| beta_M | 0.15 | Motivation decay rate (hyperbolic) |
| lambda_ | 0.2 | Effort cost coefficient |
| gamma | 0.25 | Behavioral reward coefficient |
| gamma_ind | 0.1 | Indulgence drain coefficient |
| f_0 | 0.3 | Indulgence propensity |
| phi_S | 1.0 | Expectation inflation per shock event |
| phi_M | 0.08 | Passive E drift rate when M high, H low |
| psi | 0.15 | Expectation reduction per progress event |
| epsilon | 0.03 | Natural E recalibration rate |
| phi_ind | 0.05 | Fantasy-driven E inflation |
| kappa | 0.3 | False hope collapse severity |
| E_crit | -1.5 | False hope collapse threshold |
| kappa_wth | 0.8 | "What the hell" collapse severity |
| E_wth | 1.5 | "What the hell" threshold |
| tau | 0.15 | Behavioral threshold softness |
| mu | 0.1 | Velocity meta-loop gain (Carver & Scheier) |
| alpha_I | 0.005 | Identity growth rate |
| delta_I | 0.001 | Identity decay rate |
| sigma_noise | 0.02 | Stochastic noise amplitude |

---

## Behavioral Trigger

B is computed from two competing systems (Daw et al. 2005; de Wit et al. 2018):

```
theta(H, C, stress, ii) = C * (1 - H) + stress * 0.3 * (1 - H) - ii

B_goal = sigmoid((M - theta) / tau)                    # Goal-directed: M vs threshold
B_habit = H * sigmoid((M - M_habit_floor) / 0.08)      # Habitual: H-driven, still needs some M
blend = H^1.5                                           # Nonlinear shift toward habitual
B_raw = (1 - blend) * B_goal + blend * B_habit
B = B_raw * sigmoid((M - 0.08) / 0.03)                 # Global activation gate
```

Key properties:
- At H=0: behavior is purely M-gated (need M > C to act)
- At H=0.8: behavior is mostly habitual but still requires M > ~0.08
- The activation gate ensures B=0 when M is negligible (sedentary is a true fixed point)
- Stress raises the threshold for non-habitual behavior (Schwabe & Wolf 2009)
- Implementation intentions lower the threshold directly

---

## Endogenous Fantasy/Indulgence

```
F = f_0 * M * (1 - B)    # Fires when motivated but not acting (Kappes & Oettingen 2011)
```

---

## Dynamics

### dH/dt: Habit Strength

```
decay_rate = delta_H * (1 + 2 * (1 - B) * H)           # Accelerating decay when not practicing

dH/dt = alpha_H * B * (A(I) - H)                        # Asymptotic growth (Lally 2010)
      - decay_rate * (1 - B) * (H - H_min)              # Decay toward residual floor
```

where `A(I) = A_base + (1 - A_base) * I` (identity raises the habit ceiling).

### dM/dt: Motivational Activation

Events are **impulses** applied directly to M (not rate terms).

Continuous dynamics:
```
dM/dt = -beta_M * M / (1 + M)                           # Hyperbolic decay (Steel & Konig 2006)
      + gamma * B * (1 - H^2) * (1 - M/2)               # Reward prediction error (Schultz 2016)
      - lambda * C * (1 - H) * B                         # Effort cost (Kurzban 2013)
      - gamma_ind * F * (1 - H)                          # Indulgence drain (Oettingen)
      - kappa * softplus(-E - |E_crit|) * M              # False hope collapse (Polivy & Herman)
      - kappa_wth * sigmoid((E - E_wth) / 0.2) * M      # "What the hell" collapse (Cochran & Tesser)
      + mu * (-dE/dt_prev)                               # Velocity meta-loop (Carver & Scheier)
      + 0.08 * max(0, 0.2*I - M)                         # Identity restoring force
      + 0.02 * B * H                                     # Habitual maintenance reward
      - 0.3 * stress * M * (1-H) * (1 - 0.3*social)     # Stress drain (buffered by social support)
      + 0.05 * max(0, 0.15*social - M)                   # Social support sustain
      + max(0, -dC/dt) * 0.3                             # Simplification boost (C-M coupling)
```

### dE/dt: Expectation Excess

Event impulses add directly to E (shocks inflate expectations).

```
dE/dt = phi_M * M * (1 - H)                             # High M + low H = growing expectations
      - psi * B * H                                      # Actual progress reduces E
      - epsilon * E                                      # Slow natural recalibration
      + phi_ind * F                                      # Fantasy inflates expectations
      - 0.3 * B * (1-H) * (E > 0 ? 1 : 0)              # Early effort corrects upward E
```

### dI/dt: Identity Coherence

```
dI/dt = alpha_I * B * H * (1 - I)                       # Grows from established habitual behavior
      - delta_I * (1 - B) * I                            # Very slow decay
```

### dC/dt: Behavioral Complexity (Equilibrium-Based)

C adapts toward `C_equil(H, I)` -- the sustainable complexity for the current habit strength:

```
C_equil = C_min + (C_max - C_min) * H * (0.7 + 0.3 * I)

overreach = max(0, C - C_equil) * max(0, 0.3 - B)       # C too high, not performing
failure = -alpha_C_down * overreach                       # Simplify pressure
e_reassess = -alpha_C_down * 0.3 * softplus(-E - |E_crit|*0.5) * max(0, 0.3 - B)

underreach = max(0, C_equil - C) * B                     # C too low, performing well
success = alpha_C_up * underreach                         # Progressive overload

identity_pull = alpha_C_up * 0.3 * I * max(0, H-0.3) * max(0, C_equil - C)

dC/dt = (failure + e_reassess + success + identity_pull) * (1 + social_support)
```

Key property: C_equil creates a **manifold of attractors** in H-C space. The daily walker
(H~0.7, C~0.2) and the 3x/week gym-goer (H~0.6, C~0.5) are distinct equilibria, not the
same attractor viewed from different initial conditions.

---

## Transient State Decay

```
stress *= (1 - 0.1 * dt)           # ~10-day half-life
ii_active *= (1 - 0.05 * dt)       # ~20-day half-life
social_support *= (1 - 0.003 * dt) # ~330-day half-life
```

---

## Event System (Impulse-Based)

Events modify state **instantaneously** (not through rate terms):

| Event | M impulse | E impulse | Other effects |
|-------|-----------|-----------|---------------|
| shock | +amplitude | +phi_S * amplitude | |
| new_year | +amplitude | +phi_S * amplitude | E *= 0.5 (fresh start) |
| stress | -amplitude * 0.3 | | stress += amplitude |
| lapse | | +amplitude * 1.5 | M *= (1 - amplitude * 0.4) |
| social | +amplitude * 0.3 | | social_support += amplitude * 0.2 |
| context_disruption | | | H *= (1 - amplitude) |
| injury_start | | | injured = true |
| injury_end | | | injured = false |
| impl_intention | | | ii = amplitude * C * 0.5 |
| simplify | +C_drop * 1.5 | | C -= amplitude * 0.15; E *= 0.6 |
| escalate | | +amplitude * 0.5 | C += amplitude * 0.1 |

---

## Phase Portrait Structure

The H-C phase portrait (see `simulation/results/hc_phase_portrait.png`) reveals:

1. **Stable Habit Basin** (lower-right): H > 0.5, C matched to H via C_equil curve.
   Trajectories converge along the equilibrium manifold.

2. **Complexity Trap** (upper-left): High C, low H. Threshold too high for M to
   sustain behavior. Trajectories slide left toward sedentary.

3. **Sedentary Attractor** (lower-left): H ~ H_min, M ~ 0. True fixed point
   due to activation gate.

4. **Separatrix**: Sharp boundary between basins at approximately C ~ 0.55 (for M0=1).
   Starting above this in C leads to failure; below leads to success.

5. **Progressive Overload Zone**: Band along C_equil curve where established habits
   naturally grow in complexity.

The separatrix's position depends on initial M -- higher M0 allows higher initial C
to succeed. This is the geometric formalization of the bootstrapping thesis:
**start simple, build complexity as automaticity grows**.

---

## Calibration Status

Calibrated against 2100 synthetic 2-year simulations (21 persons x 100 event streams).
See `calibration/README.md` for methodology.

Round 3 results vs literature targets:

| Metric | Observed | Target | Status |
|--------|----------|--------|--------|
| habit_formed | 33.0% | 15-30% | Slightly high |
| partial_habit | 32.4% | 10-25% | High |
| sedentary | 15.8% | 25-45% | Low |
| dropout | 10.0% | 10-25% | OK |
| false_hope_cycle | 8.7% | 3-15% | OK |
| Dropped by d60 | 63.4% | 50-80% | OK |
| Active at d180 | 39.9% | 25-50% | OK |
| Active at d365 | 69.9% | 15-35% | High |
