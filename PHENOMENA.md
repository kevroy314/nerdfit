# Phenomena a Dynamical Systems Model of Habit Formation Should Capture

This document enumerates phenomena from the academic literature on habit formation, performance psychology, affective dynamics, and neuroscience of reward signaling. Each phenomenon is grounded in citations, classified by whether the proposed H-M-E model captures it, and tagged with the state variables and dynamics implications.

---

## I. Core Habit Formation Dynamics

### P1. Asymptotic Automaticity Growth
**Description:** Habit strength grows as a decelerating function of repetitions, following an asymptotic curve. Median time to 95% asymptote: 66 days (range 18-254). Exercise behaviors take ~1.5x longer than eating/drinking behaviors.
**Citations:** Lally et al. (2010), Singh et al. (2024)
**Model status:** CAPTURED by dH/dt = alpha_H * B * (A - H)
**Variables:** H, C (complexity moderates rate)

### P2. Nonlinear Habit Decay (NOT Exponential)
**Description:** When behavior stops, habits decay following asymptotic or logistic curves (not exponential). Rapid initial drop, then stabilization at a residual floor. Median stabilization: ~9-10 days. Old habits may never fully reach zero.
**Citations:** Edgren et al. (2025), Walker et al. (2015), Bouton (2024)
**Model status:** NEEDS MODIFICATION -- current exponential decay term should be replaced with logistic/asymptotic form with a residual floor H_min.
**Variables:** H
**Dynamics:** dH_decay/dt = -delta_H * (H - H_min) * (1 - B) with possibly nonlinear delta_H

### P3. Instigation vs. Execution Habit Distinction
**Description:** Instigation habit (deciding to start) predicts behavior frequency; execution habit (performing sub-actions) does not. Getting started is the critical bottleneck.
**Citations:** Gardner, Phillips & Judah (2016), Phillips & Gardner (2016), Kaushal et al. (2017)
**Model status:** CAPTURED -- H primarily represents instigation automaticity, which is the correct target variable.
**Variables:** H (as instigation habit)

### P4. Context-Dependent Habit Triggering
**Description:** Habits are cue-contingent. Context disruptions (moving, job change) break cue-behavior associations, creating a ~3-month "window of opportunity." Travel habits weakest immediately after relocation, then increase as new habits form.
**Citations:** Verplanken & Roy (2016), Thomas et al. (2016), Orbell & Verplanken (2010)
**Model status:** PARTIALLY CAPTURED -- needs context stability parameter Ctx that modulates H expression. H should have context-dependent and context-independent (latent skill) components.
**Variables:** H, Ctx (new)
**Dynamics:** Effective H = H * Ctx, where Ctx in [0,1] drops during life transitions

### P5. No Sharp Phase Transition in Habit Formation
**Description:** The automaticity curve is smooth -- no evidence for a critical mass or discrete threshold. The "21-day myth" is refuted.
**Citations:** Lally et al. (2010), Singh et al. (2024), Bouton (2024)
**Model status:** CAPTURED -- the asymptotic growth naturally produces a smooth transition. However, the H-M interaction can create *emergent* threshold-like behavior (a model prediction worth testing).
**Variables:** H, M

---

## II. Motivational Dynamics

### P6. Hyperbolic (Not Exponential) Motivation Decay
**Description:** Motivation follows hyperbolic temporal discounting: steep initial decline with a long tail. Temporal Motivation Theory formalizes this as M = (Expectancy x Value) / (1 + Impulsiveness x Delay).
**Citations:** Steel & Konig (2006), Hall & Fong (2015)
**Model status:** NEEDS MODIFICATION -- replace -beta_M * M with hyperbolic form or mixed hyperbolic-exponential.
**Variables:** M
**Dynamics:** dM/dt includes -beta_M * M^2 / (1 + M) or similar hyperbolic form

### P7. Fresh Start Discontinuities
**Description:** Temporal landmarks (New Year, Mondays, birthdays) create discontinuous jumps in M through cognitive reframing -- relegating past failures to a "previous period." Gym visits increase 33% at week start, 47% at semester start.
**Citations:** Dai, Milkman & Riis (2014)
**Model status:** PARTIALLY CAPTURED by S(t) shock term, but these are cognitive/endogenous resets, not external events. Need a periodic "fresh start" component in S(t).
**Variables:** M, E (both partially reset)

### P8. Multidimensional Motivation (Intrinsic vs. Extrinsic)
**Description:** Intrinsic motivation (enjoyment) and extrinsic motivation (health scares, social pressure) have qualitatively different dynamics and persistence. External rewards can undermine intrinsic motivation (overjustification effect). More autonomous motivation predicts greater persistence.
**Citations:** Ryan & Deci (2000, 2020), SDT literature
**Model status:** PARTIALLY CAPTURED -- single M conflates two qualitatively different processes. Could split into M_i (intrinsic, slow decay) and M_e (extrinsic, fast decay), or model as weighted sum.
**Variables:** M (should be decomposed or have quality parameter)

### P9. Ego Depletion as Opportunity Cost (Not Resource Depletion)
**Description:** The "limited resource" model of self-regulation is largely discredited. Effort depletion reflects shifting motivation and rising opportunity cost, not literal resource consumption. Incentives and reframing reverse "depletion."
**Citations:** Inzlicht & Berkman (2015), Hagger et al. (2016), Kurzban et al. (2013)
**Model status:** CAPTURED if effort term is interpreted as opportunity cost. The lambda * C * (1-H) * B term works if lambda represents increasing subjective cost, not decreasing capacity.
**Variables:** M, H, C

### P10. Teachable Moments Fade Without Reinforcement
**Description:** Health scares create temporary motivational windows with three components: increased risk perception, affective impact, and changed self-concept. Only 25-45% maintain exercise one year post-cardiac event. Non-adherence for chronic illness: 50-80%.
**Citations:** McBride et al. (2003), Middleton et al. (2013), Kwasnicka et al. (2016)
**Model status:** CAPTURED by shock S(t) followed by decay. The model correctly predicts that shocks alone are insufficient without H accumulation during the window.
**Variables:** M, H

---

## III. Expectation and Failure Dynamics

### P11. False Hope Syndrome (Cycling)
**Description:** Unrealistic expectations -> initial euphoria -> failure to meet expectations -> reinterpretation -> recommitment -> repeat. The initial commitment itself generates reward (improved self-image), making the failure cycle self-sustaining. 88.8% success in January -> 54.7% by December.
**Citations:** Polivy & Herman (2000, 2002), Oscarsson et al. (2020)
**Model status:** CAPTURED by E dynamics. This is a key validation target -- the model should produce limit cycles in M-E space with H stuck near zero.
**Variables:** H, M, E

### P12. The "What the Hell" Effect (Catastrophic Collapse)
**Description:** When goal-setters perceive a goal violation, motivation collapses nonlinearly/catastrophically rather than gradually. All-or-nothing framing amplifies this. One lapse triggers complete abandonment.
**Citations:** Cochran & Tesser (1996), Polivy & Herman (1985)
**Model status:** NEEDS ADDITION -- requires a bifurcation/threshold in M dynamics. When E exceeds a critical value (perceived violation), M should drop discontinuously.
**Variables:** M, E
**Dynamics:** Add catastrophic term: -kappa_wth * Heaviside(E - E_wth) * M (or softer sigmoid version)

### P13. Velocity Meta-Loop (Rate of Progress Drives Affect)
**Description:** It's not just the discrepancy (E) but the *rate of discrepancy reduction* (dE/dt) that generates affect and drives engagement/disengagement. Progress faster than expected -> positive affect -> sustained M. Slower than expected -> negative affect -> M decay.
**Citations:** Carver & Scheier (1982, 1998, 2018)
**Model status:** NEEDS ADDITION -- add dE/dt as a signal modifying M.
**Variables:** M, E
**Dynamics:** Add term to dM/dt: +mu * (-dE/dt) [negative dE/dt means E is decreasing = progress being made]

### P14. Lapse Psychology (Asymmetric Impact)
**Description:** Missing a single day barely affects H (Lally), but the *psychological response* to lapsing can devastate M through the abstinence violation effect (guilt, personal failure attribution). The subjective impact of lapsing far exceeds its objective impact on automaticity.
**Citations:** Marlatt (Larimer et al., 1999), Stojanovic et al. (2021)
**Model status:** PARTIALLY CAPTURED by E dynamics, but needs asymmetric lapse sensitivity. A single B=0 event when the person "should have" performed should create a spike in E disproportionate to its effect on H.
**Variables:** M, E, H

---

## IV. Reward and Affect Dynamics

### P15. Reward Prediction Error (Not Absolute Reward)
**Description:** Dopamine neurons encode prediction error (actual minus expected reward), not absolute reward magnitude. Fully predicted rewards generate no dopamine response. Novel/surprising rewards are maximally motivating. Cue-transfer: over time, the dopamine signal shifts from reward to earliest predictive cue.
**Citations:** Schultz (2016), Schultz, Dayan & Montague (1997)
**Model status:** NEEDS MODIFICATION -- the gamma * B reward term should become gamma * (B - E_reward) where E_reward is the expected reward, creating diminishing returns as behavior becomes routine.
**Variables:** M
**Dynamics:** Replace fixed reward with prediction error: gamma * B * max(0, novelty_factor - familiarity(H))

### P16. Intensity-Dependent Affective Feedback
**Description:** Below ventilatory threshold: exercise boosts affect (positive feedback to M). Above VT: exercise consistently depletes affect (negative feedback). The sign of the affective feedback reverses at high intensity. In-task affect is the strongest predictor of future exercise (1 unit = +38 min/week at 6 months).
**Citations:** Ekkekakis (2009), Williams (2008), Brand & Ekkekakis (2018)
**Model status:** NEEDS MODIFICATION -- the effort cost term should have an intensity-dependent sign change. Low-complexity (self-paced) exercise generates positive affect; high-intensity prescribed exercise generates negative affect.
**Variables:** M, C (or intensity parameter)
**Dynamics:** Affect feedback = gamma_aff * B * (V_threshold - C) where V_threshold marks the sign change

### P17. Phantom Reward / Indulgence Decoupling
**Description:** Positive fantasy about goals drops systolic blood pressure and reduces energization. The brain partially treats vivid fantasy as goal achievement, providing phantom reward that substitutes for behavioral reward without incrementing H. Maximally damaging at low H.
**Citations:** Kappes & Oettingen (2011), Oettingen (2012)
**Model status:** CAPTURED by the F(t) indulgence mechanism and gamma_ind term. The state-dependent toxicity (worse at low H) is correctly modeled by the (1-H) factor.
**Variables:** M, H, F(t)

### P18. Affective Inertia as Individual Difference
**Description:** Emotional carry-over (autocorrelation) varies between individuals. High inertia = "sticky" mood states, associated with maladjustment. This maps to individual differences in M decay rate -- some people's motivation is more persistent but also harder to boost.
**Citations:** Kuppens et al. (2010), Bringmann et al. (2016)
**Model status:** CAPTURED as individual differences in beta_M parameter. High-inertia individuals have lower beta_M.
**Variables:** M (beta_M as individual difference parameter)

---

## V. Dual-Process and Neural Architecture

### P19. Model-Free / Model-Based Competition
**Description:** Two parallel learning systems: model-based (goal-directed, flexible, costly) and model-free (habitual, efficient, inflexible). ~60/40 population-level weighting. Bayesian arbitration based on relative uncertainty. The transition is gradual and the systems compete continuously.
**Citations:** Daw et al. (2005, 2011), Dolan & Dayan (2013), Tricomi et al. (2009)
**Model status:** CAPTURED by the H-M architecture. As H grows, behavior becomes less M-dependent (model-free takes over from model-based). The soft threshold B = sigma((M - theta)/tau) with theta = C*(1-H) naturally implements this shift.
**Variables:** H, M

### P20. Human Habits Are Fragile (Outcome-Sensitive)
**Description:** Unlike rodent habits, human habits may never become fully outcome-insensitive. Five experimental attempts to induce outcome-insensitive habits in humans all failed. M always matters to some degree.
**Citations:** de Wit et al. (2018)
**Model status:** NEEDS MODIFICATION -- B should never become completely independent of M. Even at H=1, M should have some residual influence: theta_min > 0 or B = sigma((M + H - theta)/tau) with minimum M contribution.
**Variables:** H, M, B

---

## VI. Identity, Social, and Contextual Factors

### P21. Identity as Slow Variable
**Description:** Exercise identity (d=0.73 for intention-behavior gap) is the strongest predictor of long-term maintenance. Identity modulates how difficulty is interpreted (motivating vs. demoralizing). Changes on months-to-years timescale. The Identity-Value Model shows I increases subjective value of congruent behaviors via vmPFC.
**Citations:** Rhodes et al. (2016, 2021), Oyserman (2010), Berkman et al. (2017), Kendzierski (1988, 1990), Caldwell et al. (2018)
**Model status:** NEEDS ADDITION as a 4th state variable I(t).
**Variables:** I (new)
**Dynamics:** dI/dt = alpha_I * B * H - delta_I * (1-B) * I, very slow (alpha_I << alpha_H). Feeds back: I raises A (ceiling), amplifies M, modulates E interpretation.

### P22. Social Contagion and Accountability
**Description:** Friends becoming obese increases risk by 57% (171% for mutual friends). Accountability to a coach increases adherence >100%. "Autonomous accountability" outperforms shame-based.
**Citations:** Christakis & Fowler (2007), Oussedik et al. (2017), Mohr et al. (2011)
**Model status:** NOT CAPTURED -- purely individual model. Can be modeled as exogenous social coupling in dM/dt.
**Variables:** M (social influence as parameter or slow exogenous variable)

### P23. Stress Shifts Control from Goal-Directed to Habitual
**Description:** Acute stress shifts behavioral control from prefrontal (M-driven) to dorsal striatum (H-driven). Stressed subjects continue devalued actions. Only 28% of stressed participants could name action-outcome associations vs. 58% controls.
**Citations:** Schwabe & Wolf (2009, 2011), Heatherton & Wagner (2011)
**Model status:** NEEDS ADDITION -- stress parameter sigma(t) should modulate the M vs. H balance in the behavioral equation. Under stress, theta decreases (H dominates regardless of M). Double-edged: good if H is positive habit, bad if H is maladaptive.
**Variables:** H, M, sigma (new parameter)
**Dynamics:** theta(H, C, sigma) = C * (1 - H) * (1 - sigma) -- stress reduces the M threshold

### P24. Sleep/Circadian Modulation of Self-Regulation
**Description:** Sleep deprivation impairs PFC, reducing M effectiveness. Self-control shows circadian variation. When cognitive capacity is low, habitual behavior dominates.
**Citations:** Pilcher et al. (2015), Lim & Dinges (2010)
**Model status:** PARTIALLY CAPTURED as time-varying modulation of M effectiveness. Can be modeled as a capacity parameter R(t) multiplying M in the behavioral equation.
**Variables:** M, R(t) (new parameter)

### P25. Competing Habits
**Description:** Breaking bad habits is most effective when a competing good habit is installed using the same cue. The brain maintains parallel S-R associations that compete for expression.
**Citations:** Wood & Runger (2016), Gardner (2024)
**Model status:** NOT CAPTURED by single H variable. Requires at minimum H_good and H_bad, or H as a vector.
**Variables:** H (should be extended)

### P26. Habit Stacking / Cue Chaining
**Description:** Existing habits serve as cues for new habits ("After I [anchor], I will [new behavior]"). Creates chains where completion of one triggers the next. Weakest link determines chain robustness.
**Citations:** Fogg (2020), Clear (2018)
**Model status:** NOT CAPTURED -- requires coupled H variables with sequential triggering.
**Variables:** H_1, H_2, ... (coupled)

---

## VII. Intervention Mechanisms

### P27. Implementation Intentions as Transfer Function Change
**Description:** If-then plans (d=0.65 across 94 studies) don't boost M -- they reduce the M needed for behavior by creating "strategic automaticity." They change the behavioral transfer function, not the motivational input.
**Citations:** Gollwitzer (1999), Gollwitzer & Sheeran (2006)
**Model status:** PARTIALLY CAPTURED -- maps to an immediate reduction in theta (behavioral threshold) or a boost to dH/dt. Important distinction: IIs change the transfer function, not the state.
**Variables:** theta (parameter shift)

### P28. Mental Contrasting Calibrates (Not Just Boosts) Motivation
**Description:** Mental contrasting produces M proportional to realistic expectations of success. High expectations -> strong commitment. Low expectations -> adaptive disengagement. Indulging and dwelling both produce indiscriminate (uncalibrated) M.
**Citations:** Oettingen (2012), Oettingen & Reininger (2016)
**Model status:** PARTIALLY CAPTURED -- the model can represent this as a coupling between M and E where mental contrasting reduces phi_S (expectation inflation per shock) while maintaining the M boost.
**Variables:** M, E

### P29. Self-Efficacy Feedback Loop
**Description:** Habit-specific self-efficacy and automaticity form a positive feedback loop -- each predicts increases in the other. Mastery experiences are the strongest source of self-efficacy.
**Citations:** Stojanovic et al. (2021), Bandura (1977, 1997)
**Model status:** CAPTURED implicitly -- successful B -> H growth -> lower theta -> easier B -> more success. Could be made explicit with a self-efficacy coupling term.
**Variables:** H, M (positive feedback)

---

## VIII. Emergent / Composite Phenomena

### P30. The Bootstrapping Trajectory
**Description:** Starting with minimal complexity C, allowing H to grow through repeated easy behavioral events, then gradually increasing C as automaticity absorbs cognitive load. The "time as first-order variable" insight from the original brainstorming.
**Citations:** Ericsson et al. (1993), Gardner & Lally (2018), Lally et al. (2010) -- synthesis from chat.txt
**Model status:** CAPTURED as the key design principle. Low C -> low theta -> B fires at low M -> H grows -> theta drops further -> self-sustaining. Validated by instigation > execution literature.

### P31. The Indulgence Trap (Quiet Failure)
**Description:** High M decoupled from B by phantom reward. M leaks away through fantasy, H never increments, system drifts to sedentary attractor without dramatic failure. Distinct from false hope cycling -- no recommitment events, just quiet erosion.
**Citations:** Kappes & Oettingen (2011), Oettingen (2012)
**Model status:** CAPTURED by endogenous F(t) = f_0 * M * (1-B) mechanism.

### P32. The Complexity Overshoot
**Description:** Attempting high execution quality (high C) from the start. Theta too high for available M, B barely fires, H doesn't grow, effort depletion drains M. Fails at M->B conversion without needing expectation dynamics.
**Citations:** Synthesis from deliberate practice (Ericsson) + instigation habit literature
**Model status:** CAPTURED by C parameter raising theta beyond M reach.

### P33. The Post-Shock Dropout Curve
**Description:** After a motivational event (health scare, New Year), rapid initial dropout (80% fail by February), then slower attrition (46% continuous success at 6 months). The curve shape should emerge from the dynamics.
**Citations:** Oscarsson et al. (2020), Norcross et al. (2002), Middleton et al. (2013)
**Model status:** SHOULD EMERGE from M decay + E dynamics. Key validation target.

### P34. Context Disruption and Recovery
**Description:** Life transitions reset context-dependent H, but latent capacity remains. Recovery is faster than initial formation if the person has prior H and I. The "window of opportunity" can be leveraged for positive change.
**Citations:** Verplanken & Roy (2016), Thomas et al. (2016)
**Model status:** PARTIALLY CAPTURED -- needs context parameter to model the reset-and-recovery dynamic.

### P35. Stress-Induced Relapse to Bad Habits
**Description:** Under stress, control shifts from M (goal-directed) to H (habitual). If the dominant H is sedentary/unhealthy, stress causes relapse. If H is healthy, stress actually helps maintenance. Double-edged sword.
**Citations:** Schwabe & Wolf (2009)
**Model status:** NEEDS stress parameter sigma(t). Predicts that early habit formation is maximally vulnerable to stress (low H_good, possibly high H_bad).

---

## Summary Statistics (Updated for Model v3)

- **Total phenomena enumerated:** 35
- **Well captured by current H-M-E-I-C model:** 22 (P1, P2, P3, P5, P6, P9, P10, P11, P12, P13, P15, P17, P18, P19, P20, P21, P23, P29, P30, P31, P32, P33)
- **Partially captured:** 9 (P4, P7, P8, P14, P22, P24, P27, P28, P34)
- **Not captured (require new architecture):** 4 (P16, P25, P26, P35)

## Implementation Status of Recommended Revisions

1. **Hyperbolic M decay** (P6) -- DONE: `-beta_M * M / (1 + M)`
2. **"What the hell" catastrophic collapse** (P12) -- DONE: sigmoid threshold on E
3. **Reward prediction error** (P15) -- DONE: `gamma * B * (1-H^2) * (1-M/2)`
4. **Velocity meta-loop** (P13) -- DONE: `mu * (-dE/dt_prev)`
5. **Identity variable I(t)** (P21) -- DONE: full state variable with dI/dt
6. **Nonlinear habit decay with floor** (P2) -- DONE: accelerating decay, H_min floor
7. **Intensity-dependent affect sign change** (P16) -- NOT YET: would need exercise intensity parameter
8. **Fragile human habits** (P20) -- DONE: B requires minimum M even at high H
9. **Stress parameter** (P23, P35) -- DONE: transient stress state, drains M, raises threshold
10. **Context disruption** (P4, P34) -- DONE: event that resets H
11. **Dynamic C** (new) -- DONE: C adapts via equilibrium-based dynamics, simplify/escalate events
12. **Social support** (P22) -- DONE: persistent state, buffers stress, sustains M
