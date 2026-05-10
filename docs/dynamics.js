/**
 * Habit Formation Dynamics Engine (browser-side)
 * Full sync with Python simulation/dynamics.py
 * State: H, M, E, I, C (all dynamic), plus transients (stress, ii, social_support)
 */

function sigmoid(x) {
  x = Math.max(-500, Math.min(500, x));
  return 1.0 / (1.0 + Math.exp(-x));
}

function softplus(x) {
  x = Math.max(-500, Math.min(500, x));
  return Math.log(1 + Math.exp(x));
}

function gaussianRandom(rng) {
  let u1 = rng();
  let u2 = rng();
  if (u1 === 0) u1 = 1e-10;
  return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
}

function makeRng(seed) {
  let s = [seed ^ 0xdeadbeef, seed ^ 0xcafebabe, seed ^ 0x12345678, seed ^ 0xfeedface];
  function next() {
    const result = (((s[1] * 5) << 7 | (s[1] * 5) >>> 25) * 9) >>> 0;
    const t = s[1] << 9;
    s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2]; s[0] ^= s[3];
    s[2] ^= t; s[3] = (s[3] << 11 | s[3] >>> 21);
    return (result >>> 0) / 4294967296;
  }
  for (let i = 0; i < 20; i++) next();
  return next;
}

const DEFAULT_PARAMS = {
  C: 0.5,
  C_min: 0.1,
  C_max: 0.95,
  alpha_C_down: 0.003,
  alpha_C_up: 0.001,
  A_base: 0.8,
  alpha_H: 0.045,
  delta_H: 0.01,
  H_min: 0.02,
  beta_M: 0.15,
  lambda: 0.2,
  gamma: 0.25,
  gamma_ind: 0.1,
  f_0: 0.3,
  phi_S: 1.0,
  phi_M: 0.08,
  psi: 0.15,
  epsilon: 0.03,
  phi_ind: 0.05,
  kappa: 0.3,
  E_crit: -1.5,
  kappa_wth: 0.8,
  E_wth: 1.5,
  tau: 0.15,
  mu: 0.1,
  alpha_I: 0.005,
  delta_I: 0.001,
  sigma_noise: 0.02,
};

class HabitDynamics {
  constructor(params = {}) {
    this.p = { ...DEFAULT_PARAMS, ...params };
    this.rng = makeRng(Date.now());
  }

  updateParams(params) {
    Object.assign(this.p, params);
  }

  A(I) {
    return this.p.A_base + (1 - this.p.A_base) * I;
  }

  theta(H, C, stress = 0, ii = 0) {
    const base = C * (1 - H);
    const stressInc = stress * 0.3 * (1 - H);
    return Math.max(0, base + stressInc - ii);
  }

  computeB(M, H, C, stress = 0, ii = 0) {
    const th = this.theta(H, C, stress, ii);
    const B_goal = sigmoid((M - th) / this.p.tau);
    const M_habit_floor = 0.15 * (1 - H * 0.5);
    const B_habit = H * sigmoid((M - M_habit_floor) / 0.08);
    const blend = Math.pow(H, 1.5);
    const B_raw = (1 - blend) * B_goal + blend * B_habit;
    const activation = sigmoid((M - 0.08) / 0.03);
    return Math.max(0, Math.min(1, B_raw * activation));
  }

  computeF(M, B) {
    return this.p.f_0 * M * (1 - B);
  }

  step(state, dt, impulseM = 0, impulseE = 0) {
    const p = this.p;
    const s = { ...state };

    // Apply impulses directly
    s.M = Math.max(0, s.M + impulseM);
    s.E = s.E + impulseE;

    // Behavioral trigger (uses dynamic C from state)
    const C = s.C !== undefined ? s.C : p.C;
    const B = s.injured ? 0 : this.computeB(s.M, s.H, C, s.stress || 0, s.ii || 0);
    const F = this.computeF(s.M, B);
    const A_eff = this.A(s.I);

    // --- dH/dt ---
    const decayRate = p.delta_H * (1 + 2 * (1 - B) * s.H);
    let dH = p.alpha_H * B * (A_eff - s.H)
           - decayRate * (1 - B) * (s.H - p.H_min);

    // --- dM/dt ---
    const decay = -p.beta_M * s.M / (1 + s.M);
    const novelty = Math.max(0, 1 - s.H * s.H);
    const mHeadroom = Math.max(0, 1 - s.M / 2);
    const rewardPE = p.gamma * B * novelty * mHeadroom;
    const effort = -p.lambda * C * (1 - s.H) * B;
    const indulgence = -p.gamma_ind * F * (1 - s.H);
    const fhCollapse = -p.kappa * softplus(-s.E - Math.abs(p.E_crit)) * s.M;
    const wthCollapse = -p.kappa_wth * sigmoid((s.E - p.E_wth) / 0.2) * s.M;
    const velocity = p.mu * (-(s.dE_prev || 0));

    // Identity restoring force
    const idTarget = 0.2 * s.I;
    const idRestore = 0.08 * Math.max(0, idTarget - s.M);
    const habitMaintenance = 0.02 * B * s.H;

    // Stress drain (buffered by social support)
    const ss = s.social_support || 0;
    const socialStressBuf = 0.3 * ss;
    const stressDrain = -0.3 * (s.stress || 0) * s.M * (1 - s.H) * (1 - socialStressBuf);

    // Social support sustain
    const socialFloor = 0.15 * ss;
    const socialSustain = 0.05 * Math.max(0, socialFloor - s.M);

    let dM = decay + rewardPE + effort + indulgence
           + fhCollapse + wthCollapse + velocity + idRestore
           + habitMaintenance + stressDrain + socialSustain;

    // --- dE/dt ---
    let dE = p.phi_M * s.M * (1 - s.H)
           - p.psi * B * s.H
           - p.epsilon * s.E
           + p.phi_ind * F
           - 0.3 * B * (1 - s.H) * (s.E > 0 ? 1 : 0);

    // --- dI/dt ---
    let dI = p.alpha_I * B * s.H * (1 - s.I)
           - p.delta_I * (1 - B) * s.I;

    // --- dC/dt --- Equilibrium-based complexity adaptation
    // C_equil depends on H and I: you can sustain complexity proportional to your habit strength
    const C_equil = p.C_min + (p.C_max - p.C_min) * s.H * (0.7 + 0.3 * s.I);

    // Failure: C above what H supports AND behavior not happening -> simplify
    const overreach = Math.max(0, C - C_equil) * Math.max(0, 0.3 - B);
    const failurePressure = -p.alpha_C_down * overreach;

    // E-driven reassessment: crushed expectations + not behaving -> simplify
    const eReassess = -p.alpha_C_down * 0.3 * softplus(-s.E - Math.abs(p.E_crit) * 0.5) * Math.max(0, 0.3 - B);

    // Success: C below what H supports AND behavior happening -> progressive overload
    const underreach = Math.max(0, C_equil - C) * B;
    const successPressure = p.alpha_C_up * underreach;

    // Identity supports higher C
    const identityCPull = p.alpha_C_up * 0.3 * s.I * Math.max(0, s.H - 0.3) * Math.max(0, C_equil - C);

    const socialCFactor = 1 + ss;
    let dC = (failurePressure + eReassess + successPressure + identityCPull) * socialCFactor;

    // C-M coupling: simplifying feels achievable -> small M boost
    const cSimplifyBoost = Math.max(0, -dC) * 0.3;
    dM += cSimplifyBoost;

    // Noise
    if (p.sigma_noise > 0) {
      const ns = p.sigma_noise * Math.sqrt(dt);
      dH += gaussianRandom(this.rng) * ns * 0.5;
      dM += gaussianRandom(this.rng) * ns;
      dE += gaussianRandom(this.rng) * ns * 0.3;
    }

    // Euler integration
    const stress = (s.stress || 0) * (1 - 0.1 * dt);
    const ii = (s.ii || 0) * (1 - 0.05 * dt);
    const social = (s.social_support || 0) * (1 - 0.003 * dt);

    return {
      H: Math.max(p.H_min, Math.min(1, s.H + dH * dt)),
      M: Math.max(0, s.M + dM * dt),
      E: s.E + dE * dt,
      I: Math.max(0, Math.min(1, s.I + dI * dt)),
      C: Math.max(p.C_min, Math.min(p.C_max, C + dC * dt)),
      B: B,
      F: F,
      dE_prev: dE,
      injured: s.injured || false,
      stress: stress,
      ii: ii,
      social_support: social,
    };
  }

  applyEvent(state, event) {
    const s = { ...state };
    const p = this.p;
    let mImpulse = 0, eImpulse = 0;
    switch (event.type) {
      case 'shock':
        mImpulse = event.amplitude || 1.5;
        eImpulse = p.phi_S * (event.amplitude || 1.5);
        break;
      case 'new_year':
        mImpulse = event.amplitude || 1.5;
        eImpulse = p.phi_S * (event.amplitude || 1.5);
        s.E *= 0.5;
        break;
      case 'context_disruption':
        s.H *= (1 - (event.amplitude || 0.6));
        break;
      case 'injury_start':
        s.injured = true;
        break;
      case 'injury_end':
        s.injured = false;
        break;
      case 'social':
        mImpulse = (event.amplitude || 0.5) * 0.3;
        s.social_support = Math.min(1, (s.social_support || 0) + (event.amplitude || 0.5) * 0.2);
        break;
      case 'stress':
        s.stress = Math.min(1, (s.stress || 0) + (event.amplitude || 0.7));
        mImpulse = -(event.amplitude || 0.7) * 0.3;
        break;
      case 'impl_intention':
        s.ii = (event.amplitude || 0.8) * (s.C || p.C) * 0.5;
        break;
      case 'lapse':
        eImpulse = (event.amplitude || 1.5) * 1.5;
        s.M *= Math.max(0, 1 - (event.amplitude || 1.5) * 0.4);
        break;
      case 'simplify': {
        const oldC = s.C || p.C;
        s.C = Math.max(p.C_min, oldC - (event.amplitude || 1) * 0.15);
        const cDrop = oldC - s.C;
        mImpulse = cDrop * 1.5; // Simplifying is re-motivating
        s.E *= 0.6;
        break;
      }
      case 'escalate':
        s.C = Math.min(p.C_max, (s.C || p.C) + (event.amplitude || 1) * 0.1);
        eImpulse = (event.amplitude || 1) * 0.5;
        break;
    }
    return { state: s, mImpulse, eImpulse };
  }
}

window.HabitDynamics = HabitDynamics;
window.DEFAULT_PARAMS = DEFAULT_PARAMS;
