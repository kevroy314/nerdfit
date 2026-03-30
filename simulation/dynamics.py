"""
Dynamical systems model of habit formation.
Core dynamics engine with H (habit), M (motivation), E (expectation), I (identity).
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional, Callable


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))


def softplus(x):
    return np.log1p(np.exp(np.clip(x, -500, 500)))


@dataclass
class Params:
    """Model parameters with literature-grounded defaults."""
    C: float = 0.5           # Initial behavioral complexity [0, 1] (now also in SimState)
    C_min: float = 0.1       # Minimum complexity (can't simplify below "take a walk")
    C_max: float = 0.95      # Maximum complexity
    alpha_C_down: float = 0.003  # Rate at which failure pushes C down
    alpha_C_up: float = 0.001   # Rate at which success pushes C up (slower than down)
    A_base: float = 0.8      # Base habit ceiling
    alpha_H: float = 0.08    # Habit growth rate
    delta_H: float = 0.01    # Habit decay rate
    H_min: float = 0.02      # Residual habit floor
    beta_M: float = 0.15     # Motivation decay rate
    lambda_: float = 0.2     # Effort cost coefficient
    gamma: float = 0.25      # Behavioral reward coefficient
    gamma_ind: float = 0.1   # Indulgence drain coefficient
    f_0: float = 0.3         # Indulgence propensity
    phi_S: float = 1.0       # Expectation inflation per shock
    phi_M: float = 0.08      # Passive expectation drift
    psi: float = 0.15        # Expectation reduction per progress
    epsilon: float = 0.03    # Expectation recalibration rate
    phi_ind: float = 0.05    # Fantasy expectation inflation
    kappa: float = 0.3       # False hope collapse severity
    E_crit: float = -1.5     # False hope collapse threshold
    kappa_wth: float = 0.8   # "What the hell" collapse severity
    E_wth: float = 1.5       # "What the hell" threshold
    tau: float = 0.15        # Behavioral threshold softness
    mu: float = 0.1          # Velocity meta-loop gain
    alpha_I: float = 0.005   # Identity growth rate
    delta_I: float = 0.001   # Identity decay rate
    sigma_noise: float = 0.02  # Stochastic noise amplitude


@dataclass
class Event:
    """An extrinsic event that modifies the dynamics at a specific time."""
    time: float
    event_type: str          # 'shock', 'new_year', 'context_disruption', 'injury_start',
                             # 'injury_end', 'social', 'stress', 'impl_intention'
    amplitude: float = 1.0
    duration: float = 0.0    # For injury/stress events
    label: str = ""


@dataclass
class SimState:
    """Full state of the system at a point in time."""
    H: float = 0.0
    M: float = 0.0
    E: float = 0.0
    I: float = 0.0
    C: float = 0.5           # Dynamic complexity (aspired behavioral complexity)
    B: float = 0.0
    F: float = 0.0
    dE_dt_prev: float = 0.0
    injured: bool = False
    stress: float = 0.0
    ii_active: float = 0.0   # Implementation intention threshold reduction
    social_support: float = 0.0  # Accumulated social support (decays slowly)


class HabitDynamics:
    """Simulate the H-M-E-I dynamical system."""

    def __init__(self, params: Params, events: list[Event] = None):
        self.p = params
        self.events = sorted(events or [], key=lambda e: e.time)
        self._fired_events = set()  # Track which events have been applied

    def A(self, I: float) -> float:
        """Habit ceiling modulated by identity."""
        return self.p.A_base + (1.0 - self.p.A_base) * I

    def theta(self, H: float, C: float, stress: float = 0.0, ii: float = 0.0) -> float:
        """Behavioral threshold. Uses dynamic C from state, not fixed parameter."""
        base = C * (1.0 - H)
        # Stress INCREASES threshold for non-habitual behavior (impairs PFC)
        stress_increase = stress * 0.3 * (1.0 - H)
        return max(0.0, base + stress_increase - ii)

    def compute_B(self, M: float, H: float, C: float, stress: float = 0.0, ii: float = 0.0) -> float:
        """Behavioral trigger (soft threshold).

        Two components: M-driven (goal-directed) and H-driven (habitual).
        Even at high H, behavior requires a minimum M (human habits are fragile,
        de Wit et al. 2018). A global activation gate ensures B is truly zero
        when M is negligible -- you don't accidentally exercise.
        """
        th = self.theta(H, C, stress, ii)
        # Goal-directed component: sharp sigmoid of M vs threshold
        B_goal = sigmoid((M - th) / self.p.tau)
        # Habitual component: H drives behavior but still needs some M
        # At H=0.8, you'll exercise with modest M but not with M≈0
        M_habit_floor = 0.15 * (1.0 - H * 0.5)  # Floor shrinks with H but never vanishes
        B_habit = H * sigmoid((M - M_habit_floor) / 0.08)
        # Blend: at low H, behavior is M-gated; at high H, habit drives
        blend = H ** 1.5
        B_raw = (1.0 - blend) * B_goal + blend * B_habit
        # Global activation gate: kills B when M is truly negligible
        # This ensures the sedentary state is a real fixed point
        activation = sigmoid((M - 0.08) / 0.03)
        return np.clip(B_raw * activation, 0.0, 1.0)

    def compute_F(self, M: float, B: float) -> float:
        """Endogenous indulgence/fantasy."""
        return self.p.f_0 * M * (1.0 - B)

    def step(self, state: SimState, t: float, dt: float,
             shock: float = 0.0, rng: np.random.Generator = None) -> SimState:
        """Advance one timestep."""
        p = self.p
        s = state

        # Handle events at this timestep (fire each event exactly once)
        # Shocks are impulses applied directly to M, not rate terms
        impulse_M = shock  # Direct M addition (not multiplied by dt)
        impulse_E = 0.0    # Direct E addition
        for i, ev in enumerate(self.events):
            if i not in self._fired_events and t <= ev.time < t + dt + 1e-9:
                self._fired_events.add(i)
                m_imp, e_imp, s = self._apply_event(ev, s)
                impulse_M += m_imp
                impulse_E += e_imp

        # Apply impulses directly to state (not through dM/dt)
        s = SimState(**{k: getattr(s, k) for k in s.__dataclass_fields__})
        s.M = max(0.0, s.M + impulse_M)
        s.E = s.E + impulse_E

        # Behavioral trigger (uses dynamic C from state)
        B = 0.0 if s.injured else self.compute_B(s.M, s.H, s.C, s.stress, s.ii_active)
        F = self.compute_F(s.M, B)

        # Habit ceiling
        A_eff = self.A(s.I)

        # --- dH/dt ---
        # Growth: asymptotic toward ceiling when behavior fires
        # Decay: accelerates when B is consistently low (use-it-or-lose-it)
        # The decay rate scales with H itself -- stronger habits decay faster in absolute
        # terms but the system has a residual floor
        decay_rate = p.delta_H * (1.0 + 2.0 * (1.0 - B) * s.H)  # Accelerating decay at high H when not practicing
        dH = (p.alpha_H * B * (A_eff - s.H)
              - decay_rate * (1.0 - B) * (s.H - p.H_min))

        # --- dM/dt ---
        # Hyperbolic decay: steep initial drop, long tail
        decay = -p.beta_M * s.M / (1.0 + s.M)
        # Reward prediction error (diminishes as habit strengthens AND as M saturates)
        # Novel behavior is rewarding; routine behavior and already-high M aren't
        novelty = max(0.0, 1.0 - s.H ** 2)
        m_headroom = max(0.0, 1.0 - s.M / 2.0)  # Reward saturates as M rises
        reward_pe = p.gamma * B * novelty * m_headroom
        # Effort cost (uses dynamic C)
        effort = -p.lambda_ * s.C * (1.0 - s.H) * B
        # Indulgence drain (state-dependent)
        indulgence = -p.gamma_ind * F * (1.0 - s.H)
        # False hope collapse (E very negative = expectations crushed by reality)
        fh_collapse = -p.kappa * softplus(-s.E - abs(p.E_crit)) * s.M
        # "What the hell" collapse (E very positive = goal perceived as violated)
        wth_collapse = -p.kappa_wth * sigmoid((s.E - p.E_wth) / 0.2) * s.M
        # Velocity meta-loop
        velocity = p.mu * (-s.dE_dt_prev)
        # Identity restoring force: pulls M toward a floor proportional to I
        # Strong enough to keep M above activation threshold when I is high
        # This is the "I am a runner, I should go run" self-concept pressure
        identity_target = 0.2 * s.I  # Target M level from identity
        identity_restore = 0.08 * max(0.0, identity_target - s.M)
        # Habitual maintenance reward: even routine behavior generates small M
        # (satisfaction of completing a habit, not novelty)
        habit_maintenance = 0.02 * B * s.H

        # Stress drain on M (stress depletes motivational resources)
        stress_drain = -0.3 * s.stress * s.M * (1.0 - s.H)

        # Social support: provides a sustained M floor (accountability, community)
        # and partially buffers against stress
        social_floor = 0.15 * s.social_support  # Target M from social support
        social_sustain = 0.05 * max(0.0, social_floor - s.M)  # Pulls M up gently
        social_stress_buffer = 0.3 * s.social_support  # Reduces effective stress impact
        stress_drain *= (1.0 - social_stress_buffer)

        dM = (decay + reward_pe + effort + indulgence
              + fh_collapse + wth_collapse + velocity + identity_restore
              + habit_maintenance + stress_drain + social_sustain)

        # --- dE/dt ---
        dE = (p.phi_M * s.M * (1.0 - s.H)
              - p.psi * B * s.H
              - p.epsilon * s.E
              + p.phi_ind * F
              - 0.3 * B * (1.0 - s.H) * (1.0 if s.E > 0 else 0.0))

        # --- dI/dt ---
        dI = (p.alpha_I * B * s.H * (1.0 - s.I)
              - p.delta_I * (1.0 - B) * s.I)

        # --- dC/dt --- Complexity adaptation
        # C is plastic: it responds to success and failure feedback.
        #
        # WHEN C DECREASES (learning to simplify):
        # - Sustained low B (not performing behavior) with high M (wanting to)
        #   signals the regime is too hard. "I keep wanting to go but I never do."
        # - False hope collapse (E very negative) triggers reassessment
        # - Social input can explicitly reduce C (coach says "just walk")
        #
        # WHEN C INCREASES (progressive overload):
        # - Sustained high B AND high H: behavior is automatic, room to add complexity
        # - Identity growth supports higher C ("I'm a runner now, let me train for a 10K")
        #
        # C PLASTICITY CONDITIONS:
        # - C is most plastic after failure (ego depletion -> reassessment)
        # - C is less plastic when things are working (don't fix what isn't broken)
        # - Social support makes C more responsive (coach/mentor guidance)

        # C DYNAMICS: Complexity adapts based on success/failure feedback.
        #
        # Key insight from calibration: C must NOT collapse to C_min unconditionally.
        # C has an equilibrium that depends on H: as H grows, the person can sustain
        # higher C. The "natural" C is proportional to H -- you do what you can handle.
        #
        # C_equil(H, I) = C_min + (C_max - C_min) * H * (0.7 + 0.3 * I)
        # When H=0, C_equil = C_min (can only handle the simplest thing)
        # When H=0.7 and I=0.5, C_equil ≈ 0.1 + 0.85 * 0.7 * 0.85 ≈ 0.61

        C_equil = p.C_min + (p.C_max - p.C_min) * s.H * (0.7 + 0.3 * s.I)

        # Failure signal: C is above what H can support -> pressure to simplify
        # Only fires when behavior is NOT happening (B < 0.3) -- if you're doing it, it's fine
        overreach = max(0.0, s.C - C_equil) * max(0.0, 0.3 - B)
        failure_pressure = -p.alpha_C_down * overreach

        # E-driven reassessment: crushed expectations trigger simplification
        e_reassess = -p.alpha_C_down * 0.3 * softplus(-s.E - abs(p.E_crit) * 0.5) * max(0.0, 0.3 - B)

        # Success signal: C is below what H can support AND behavior is happening -> grow
        # This creates progressive overload: once walking is easy, you naturally add more
        underreach = max(0.0, C_equil - s.C) * B
        success_pressure = p.alpha_C_up * underreach

        # Identity supports higher C
        identity_C_pull = p.alpha_C_up * 0.3 * s.I * max(0.0, s.H - 0.3) * max(0.0, C_equil - s.C)

        # Social support makes C adaptation faster
        social_C_factor = 1.0 + (s.social_support or 0)

        dC = (failure_pressure + e_reassess + success_pressure + identity_C_pull) * social_C_factor

        # C-M coupling: when C is actively dropping (simplifying), a small M boost
        c_simplification_boost = max(0.0, -dC) * 0.3
        dM += c_simplification_boost

        # Add noise
        if rng is not None and p.sigma_noise > 0:
            noise_scale = p.sigma_noise * np.sqrt(dt)
            dH += rng.normal(0, noise_scale * 0.5)
            dM += rng.normal(0, noise_scale)
            dE += rng.normal(0, noise_scale * 0.3)

        # Euler integration
        H_new = np.clip(s.H + dH * dt, p.H_min, 1.0)
        M_new = max(0.0, s.M + dM * dt)
        E_new = s.E + dE * dt
        I_new = np.clip(s.I + dI * dt, 0.0, 1.0)
        C_new = np.clip(s.C + dC * dt, p.C_min, p.C_max)

        # Decay transient effects
        stress_new = s.stress * (1.0 - 0.1 * dt)  # Stress decays
        ii_new = s.ii_active * (1.0 - 0.05 * dt)   # II effect slowly fades
        social_new = s.social_support * (1.0 - 0.003 * dt)  # Social support decays very slowly

        return SimState(
            H=H_new, M=M_new, E=E_new, I=I_new, C=C_new,
            B=B, F=F, dE_dt_prev=dE,
            injured=s.injured, stress=stress_new, ii_active=ii_new,
            social_support=social_new
        )

    def _apply_event(self, ev: Event, state: SimState) -> tuple[float, float, SimState]:
        """Apply an event to the state. Returns (M_impulse, E_impulse, new_state)."""
        s = SimState(**{k: getattr(state, k) for k in state.__dataclass_fields__})
        m_impulse = 0.0
        e_impulse = 0.0

        if ev.event_type == 'shock':
            m_impulse = ev.amplitude
            e_impulse = self.p.phi_S * ev.amplitude  # Shocks also inflate expectations
        elif ev.event_type == 'new_year':
            m_impulse = ev.amplitude
            e_impulse = self.p.phi_S * ev.amplitude
            s.E *= 0.5  # Partial E reset (fresh start)
        elif ev.event_type == 'context_disruption':
            s.H *= (1.0 - ev.amplitude)
        elif ev.event_type == 'injury_start':
            s.injured = True
        elif ev.event_type == 'injury_end':
            s.injured = False
        elif ev.event_type == 'social':
            m_impulse = ev.amplitude * 0.3
            # Social support accumulates and persists (gym buddy, class membership)
            s.social_support = min(1.0, s.social_support + ev.amplitude * 0.2)
        elif ev.event_type == 'stress':
            s.stress = min(1.0, s.stress + ev.amplitude)
            m_impulse = -ev.amplitude * 0.3  # Stress also immediately drains some M
        elif ev.event_type == 'impl_intention':
            s.ii_active = ev.amplitude * s.C * 0.5
        elif ev.event_type == 'lapse':
            e_impulse = ev.amplitude * 1.5
            s.M *= max(0.0, 1.0 - ev.amplitude * 0.4)
        elif ev.event_type == 'simplify':
            # External event that reduces C: coach advice, "Tiny Habits" book,
            # therapist suggestion, friend's example, post-failure realization
            # Simplifying is RE-MOTIVATING: lower bar = "I can do this" = M boost
            old_C = s.C
            s.C = max(self.p.C_min, s.C - ev.amplitude * 0.15)
            c_drop = old_C - s.C
            m_impulse = c_drop * 1.5  # Proportional M boost from renewed achievability
            s.E *= 0.6  # Simplifying recalibrates expectations downward
        elif ev.event_type == 'escalate':
            # Ambitious goal-setting event: signed up for race, bought program,
            # social pressure to do more. Increases C and inflates E.
            s.C = min(self.p.C_max, s.C + ev.amplitude * 0.1)
            e_impulse = ev.amplitude * 0.5  # Escalation inflates expectations

        return m_impulse, e_impulse, s

    def simulate(self, initial: SimState, t_end: float, dt: float = 0.1,
                 seed: Optional[int] = None) -> dict:
        """Run a full simulation."""
        self._fired_events = set()  # Reset event tracking
        rng = np.random.default_rng(seed) if seed is not None else None
        n_steps = int(t_end / dt)

        times = np.zeros(n_steps + 1)
        H = np.zeros(n_steps + 1)
        M = np.zeros(n_steps + 1)
        E = np.zeros(n_steps + 1)
        I = np.zeros(n_steps + 1)
        C = np.zeros(n_steps + 1)
        B = np.zeros(n_steps + 1)
        F = np.zeros(n_steps + 1)

        state = initial
        # Initialize C from state if set, otherwise from params
        if state.C == 0.5 and self.p.C != 0.5:
            state = SimState(**{k: getattr(state, k) for k in state.__dataclass_fields__})
            state.C = self.p.C
        times[0] = 0.0
        H[0], M[0], E[0], I[0], C[0] = state.H, state.M, state.E, state.I, state.C
        B[0], F[0] = state.B, state.F

        for i in range(n_steps):
            t = i * dt
            state = self.step(state, t, dt, rng=rng)
            times[i + 1] = t + dt
            H[i + 1] = state.H
            M[i + 1] = state.M
            E[i + 1] = state.E
            I[i + 1] = state.I
            C[i + 1] = state.C
            B[i + 1] = state.B
            F[i + 1] = state.F

        # Collect event annotations
        event_annotations = [
            {"time": ev.time, "type": ev.event_type, "label": ev.label or ev.event_type,
             "amplitude": ev.amplitude}
            for ev in self.events
        ]

        return {
            "times": times, "H": H, "M": M, "E": E, "I": I, "C": C, "B": B, "F": F,
            "events": event_annotations, "params": self.p
        }
