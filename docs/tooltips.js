/**
 * Tooltip/explanation content for all model variables, parameters, and concepts.
 */

const TOOLTIPS = {
  // State variables
  H: {
    name: "Habit Strength (H)",
    short: "How automatic the behavior has become",
    long: "Ranges from 0 (no habit) to 1 (fully automatic). Grows asymptotically when behavior occurs, following Lally et al.'s (2010) finding that habit formation takes a median of 66 days. Decays when behavior stops, but never fully reaches zero (residual floor H_min). Higher H means the behavior requires less conscious motivation to perform.",
    color: "#44cc88",
  },
  M: {
    name: "Motivation (M)",
    short: "Current drive to perform the behavior",
    long: "The 'fuel' for goal-directed behavior. Decays hyperbolically over time (Steel & Konig, 2006), boosted by external events (health scares, social encouragement), and drained by effort, stress, and indulgent fantasy. At high H, behavior no longer depends heavily on M -- this is why habits survive motivation loss.",
    color: "#ff8844",
  },
  E: {
    name: "Expectation Excess (E)",
    short: "Gap between expectations and reality",
    long: "Positive E means expectations exceed reality ('I should be seeing results by now'). Negative E means reality has exceeded or recalibrated expectations. Large positive E can trigger the 'what the hell' collapse (Cochran & Tesser, 1996). Large negative E triggers false hope collapse (Polivy & Herman, 2000). E naturally recalibrates toward zero over time.",
    color: "#cc4488",
  },
  I: {
    name: "Identity (I)",
    short: "How much 'I am someone who exercises' is part of self-concept",
    long: "The slowest variable in the system (months-years). Grows only when behavior is both occurring AND habitual -- you don't form an exerciser identity from a single gym visit. Once established, identity provides a restoring force on motivation and raises the habit ceiling. This is why long-term exercisers recover from disruptions faster (Rhodes et al., 2016).",
    color: "#8844cc",
  },
  C: {
    name: "Complexity (C)",
    short: "How demanding the target behavior is",
    long: "Dynamic variable representing the aspired behavioral complexity. A daily 15-minute walk is C~0.2; a 6-day gym split is C~0.9. C adapts: failure at high C pushes it down ('maybe I should just walk'), while success at low C gradually pushes it up ('I can handle more'). The equilibrium C depends on habit strength H -- you can sustain complexity proportional to your automaticity.",
    color: "#aacc44",
  },
  B: {
    name: "Behavior (B)",
    short: "Whether the behavior is currently being performed",
    long: "Computed from two components: goal-directed (M vs threshold) and habitual (H-driven). At low H, behavior requires motivation above the complexity threshold. At high H, behavior is mostly automatic but still requires minimum M (de Wit et al., 2018 -- human habits are fragile). B=0 when M is negligible, ensuring the sedentary state is a true fixed point.",
    color: "#44aacc",
  },

  // Parameters
  alpha_H: {
    name: "Habit Growth Rate",
    short: "How fast habits form when behavior occurs",
    long: "Controls the rate of asymptotic growth toward the habit ceiling. Default 0.045 gives ~66 days to 95% of ceiling at constant behavior, matching Lally et al. (2010).",
  },
  beta_M: {
    name: "Motivation Decay Rate",
    short: "How fast motivation fades without reinforcement",
    long: "Controls hyperbolic decay: steep initial drop, long tail. Higher values mean motivation evaporates faster after a motivational event. Relates to temporal discounting (Steel & Konig, 2006).",
  },
  gamma: {
    name: "Reward Coefficient",
    short: "How much performing the behavior boosts motivation",
    long: "Reward follows prediction error: novel behavior is rewarding, routine behavior less so (Schultz, 2016). The effective reward diminishes as H increases (the 'gym excitement' fades) and as M is already high (saturation).",
  },
  lambda: {
    name: "Effort Cost",
    short: "How much effort the behavior requires",
    long: "Scales with complexity C and inversely with habit strength H. Reframed as opportunity cost (Kurzban et al., 2013) rather than resource depletion. High-complexity, non-habitual behavior is effortful; low-complexity or habitual behavior is nearly free.",
  },
  f_0: {
    name: "Indulgence Propensity",
    short: "Tendency to fantasize about goals without acting",
    long: "Controls the endogenous indulgence mechanism (Kappes & Oettingen, 2011). When motivated but not acting, people tend to fantasize about outcomes, which provides phantom reward that drains M without building H. Most damaging at low H.",
  },
  E_wth: {
    name: "What-the-Hell Threshold",
    short: "How much goal violation triggers complete abandonment",
    long: "When E exceeds this threshold, motivation collapses catastrophically rather than gradually (Cochran & Tesser, 1996). Lower values mean the person is more sensitive to perceived violations. All-or-nothing thinkers have lower thresholds.",
  },
  sigma_noise: {
    name: "Stochastic Noise",
    short: "Random daily variation in all variables",
    long: "Represents the inherent unpredictability of daily life. Some days you feel more motivated for no reason; some days less. Noise can push trajectories across the separatrix, creating probabilistic outcomes from identical starting conditions.",
  },

  // Events
  shock: {
    name: "Motivational Shock",
    short: "External event that boosts motivation",
    long: "Health scares, social comparison, New Year's -- events that spike M. Also inflates E (higher expectations). The key insight: shocks alone don't create lasting change unless H has time to grow during the motivational window.",
  },
  lapse: {
    name: "Lapse / Slip",
    short: "Perceived violation of the behavioral goal",
    long: "Spikes E (perceived gap between goal and reality) and drops M (guilt, frustration). The psychological impact far exceeds the actual effect on H -- missing one day barely affects automaticity (Lally et al.), but the abstinence violation effect can be devastating (Marlatt).",
  },
  stress: {
    name: "Stress Event",
    short: "Acute stress that impairs goal-directed control",
    long: "Stress shifts control from prefrontal (M-driven) to habitual (H-driven) (Schwabe & Wolf, 2009). Bad if H is low (can't sustain behavior without M). Also directly drains M, buffered by social support.",
  },
  simplify: {
    name: "Simplify Event",
    short: "Decision to reduce behavioral complexity",
    long: "A coach saying 'just walk', reading Tiny Habits, or a personal realization that the current approach is too complex. Drops C directly and provides an M boost (the 'I can actually do this' feeling). Often the critical event that rescues a trajectory from the complexity trap.",
  },
  escalate: {
    name: "Escalate Event",
    short: "Decision to increase behavioral complexity",
    long: "Signing up for a race, buying a training program, or a trainer pushing for more. Increases C and inflates E. Productive when H supports the new complexity; premature when H is still low.",
  },

  // Concepts
  separatrix: {
    name: "Separatrix",
    short: "The boundary between success and failure basins",
    long: "In the H-C phase portrait, a sharp boundary separates initial conditions that lead to habit formation from those that lead to sedentary. Starting above the separatrix (too complex) leads to failure; below leads to success. The separatrix position depends on initial M -- more motivation allows higher starting C.",
  },
  c_equilibrium: {
    name: "C Equilibrium Curve",
    short: "The sustainable complexity for a given habit strength",
    long: "C_equil(H, I) = C_min + (C_max - C_min) * H * (0.7 + 0.3*I). This curve defines where C stabilizes: you can sustain complexity proportional to your automaticity. The daily walker (H~0.7, C~0.2) and the gym-goer (H~0.6, C~0.5) are distinct equilibria along this curve.",
  },
  bootstrapping: {
    name: "Bootstrapping Strategy",
    short: "Start simple, add complexity as automaticity grows",
    long: "The central thesis: begin with the lowest complexity that constitutes 'doing the behavior' (walking, not CrossFit). This keeps the threshold low, allowing H to grow even as M decays. Once H is established, complexity can be gradually increased. This is the optimal path through the H-C phase space.",
  },
};

window.TOOLTIPS = TOOLTIPS;
