# Literature Review: Dynamical Systems Model of Habit Formation
## For the H-M-E Model (Habit Strength, Motivational Activation, Expectation-Reality Gap)

Generated: 2026-03-27

---

## 1. HABIT FORMATION DYNAMICS

### 1.1 The Asymptotic Automaticity Curve

**Key paper:**
- Lally, P., van Jaarsveld, C. H. M., Potts, H. W. W., & Wardle, J. (2010). How are habits formed: Modelling habit formation in the real world. *European Journal of Social Psychology*, 40(6), 998-1009. DOI: 10.1002/ejsp.674

**Findings:** 96 volunteers chose an eating, drinking, or activity behaviour to perform daily in the same context for 12 weeks. Automaticity (measured via SRHI) followed an **asymptotic curve**: early repetitions produced large gains in automaticity, with diminishing returns over time. Time to reach 95% of asymptote ranged from **18 to 254 days** (median = 66 days). Complex behaviors (exercise) took ~1.5x longer than simple behaviors (drinking water). Missing a single day did not materially affect habit formation.

**Model fit:** The proposed H variable with asymptotic growth toward ceiling A directly captures this. The complexity parameter C modulating growth rate is well-supported.

**Recent meta-analysis:**
- Singh, B., Murphy, A., Maher, C., & Smith, A. E. (2024). Time to Form a Habit: A Systematic Review and Meta-Analysis of Health Behaviour Habit Formation and Its Determinants. *Healthcare*, 12(23), 2488. DOI: 10.3390/healthcare12232488

**Findings:** 20 studies, 2601 participants. Median time: 59-66 days; mean: 106-154 days; individual range: 4-335 days. Simpler behaviors (flossing, water) showed larger effect sizes. Morning practice > evening. Self-selected habits stronger than assigned. Meta-analytic SMD = 0.69 for habit interventions.

**Model relevance:** Supports substantial individual variability - the model should account for person-level parameter heterogeneity, not just fixed parameters.

---

### 1.2 Habit Decay Rates

**Key paper:**
- Edgren, R., Baretta, D., & Inauen, J. (2025). The temporal trajectories of habit decay in daily life: An intensive longitudinal study on four health-risk behaviors. *Applied Psychology: Health and Well-Being*, 17(1), e12612. DOI: 10.1111/aphw.12612

**Findings:** N=194, 11,805 daily observations across sedentary behavior, snacking, alcohol, smoking. Six models tested: constant, linear, quadratic, cubic, **asymptotic, and logistic** (the latter two were best-fitting in 54% of cases). Habit decay follows a "decelerating negative trend" - rapid initial drop, then stabilization. Stabilization time: 1-65 days (median ~9-10 days). Massive between-person heterogeneity.

**Critical insight for model:** Simple exponential decay is NOT the best description. Asymptotic and logistic decay models fit better. The model's decay term may need to be nonlinear (e.g., decay rate that itself diminishes as H approaches some residual floor, or a logistic decay function).

**Additional evidence:**
- Walker, I., Thomas, G. O., & Verplanken, B. (2015). Old Habits Die Hard. *Environment and Behavior*, 47(10), 1089-1106. DOI: 10.1177/0013916514549619

**Findings:** After office relocation, travel habit strength (automaticity) weakened immediately but did not disappear abruptly. Old habit decayed gradually while new habit grew concurrently. This suggests habit decay and formation can occur simultaneously for competing behaviors.

**Model relevance:** The H variable should potentially allow for residual habit strength (habits don't fully decay to zero), and the decay function should be asymptotic/logistic rather than pure exponential.

- Bouton, M. E. (2024). Habit and persistence. *Journal of Experimental Analysis of Behavior*, 121(1), 88-96. DOI: 10.1002/jeab.894

**Key claim:** Contrary to "sticky habit" notion, habits are NOT inherently more persistent than goal-directed actions. The function of habit learning is to make behavior automatic, not to make it strong or persistent. Habits are tightly context-bound. Partial reinforcement and multiple-context training enhance persistence through generalization, not habit.

**Model relevance:** This challenges the assumption that high H means high persistence. The model may need to distinguish between H (automaticity) and persistence (which may depend more on M and context factors).

---

### 1.3 The Instigation vs. Execution Distinction

**Key papers:**
- Gardner, B., Phillips, L. A., & Judah, G. (2016). Habitual instigation and habitual execution: Definition, measurement, and effects on behaviour frequency. *British Journal of Health Psychology*, 21(3), 613-630. DOI: 10.1111/bjhp.12189

- Phillips, L. A., & Gardner, B. (2016). Habitual exercise instigation (vs. execution) predicts healthy adults' exercise frequency. *Health Psychology*, 35(1), 69-77. DOI: 10.1037/hea0000249

**Findings:** Instigation habit = automatic activation of the decision to perform the behavior (e.g., leaving work triggers "go to gym"). Execution habit = automaticity of the behavioral sequence itself (e.g., once in the gym, exercises flow automatically). N=229 across three health domains: instigation-SRHI was uniformly more predictive of behavior frequency than execution-SRHI. For exercise specifically, instigation habit was the only unique predictor of frequency.

**Framework from Gardner (2024):**
- Gardner, B. (2024). What is habit and how can it be used to change real-world behaviour? Narrowing the theory-reality gap. *Social and Personality Psychology Compass*, 18, e12975. DOI: 10.1111/spc3.12975

**Key claims:** Habit is just one potential influence on behavior at any moment. Habit formation may be neither necessary nor sufficient to sustain behavior change. Instigation habits bridge pre-action to action; execution habits automate performance within action.

**Model relevance:** The H variable in the proposed model likely captures instigation habit (which is what matters for whether behavior occurs). The model may MISS the instigation/execution distinction - could be important for complex exercise behaviors where getting started is the hard part. Consider splitting H into H_i (instigation) and H_e (execution), or treating H as primarily instigation habit.

---

### 1.4 Context-Dependent Habit Triggering and Discontinuity

**Key papers:**
- Verplanken, B., & Roy, D. (2016). Empowering interventions to promote sustainable lifestyles: Testing the habit discontinuity hypothesis in a field experiment. *Journal of Environmental Psychology*, 45, 127-134. DOI: 10.1016/j.jenvp.2015.11.003

- Thomas, G. O., Poortinga, W., & Sautkina, E. (2016). Habit Discontinuity, Self-Activation, and the Diminishing Influence of Context Change: Evidence from the UK Understanding Society Survey. *PLoS ONE*, 11(4), e0153490. DOI: 10.1371/journal.pone.0153490

**Findings (Verplanken):** The habit discontinuity hypothesis states that life course changes (moving house, job change) disrupt contextual cues, opening a "window of opportunity" for behavior change lasting up to 3 months. People who recently moved and had high environmental concern used the car less for commuting.

**Findings (Thomas et al.):** N=18,053 UK respondents. Car use lowest immediately after moving, then sharply increases 0-24 months. Environmental attitudes predicted reduced car use only within 12 months of relocation. The window of opportunity closes as new habits form.

- Orbell, S., & Verplanken, B. (2010). The automatic component of habit in health behavior: Habit as cue-contingent automaticity. *Health Psychology*, 29(4), 374-383. DOI: 10.1037/a0019596

**Findings:** Habitual behaviors are cue-dependent. Environmental changes that disrupt cue exposure discontinue habitual action. Dual process theory: automatic processes depend on internal (mood) or external (places, people, times) cues.

**Model relevance:** The model needs a context variable or context-disruption mechanism. When context changes, H should effectively be "reset" or rapidly decay. This is a MISSING feature if the model treats H as purely internal without context coupling. The E (expectation-reality gap) variable could partially capture this if context disruption creates a large E, but a more explicit mechanism may be needed.

---

### 1.5 Nonlinear/Threshold Effects in Habit Formation

**Evidence from Lally et al. (2010):** The asymptotic curve IS nonlinear - early repetitions matter most. But there is no evidence for a sharp "critical mass" threshold. The curve is smooth.

**From Singh et al. (2024):** The "21-day myth" is refuted. Individuals should anticipate 2-5 months for automaticity. No discrete threshold identified.

**From Bouton (2024):** Habits can revert to goal-directed status when reinforcers become surprising again. This implies the habit-goal transition is not a one-way threshold but a reversible gradient.

**Model relevance:** The model's asymptotic growth toward ceiling A captures the nonlinear saturation well. There is NO strong evidence for a discrete bifurcation or phase transition in habit formation - the transition is smooth/gradual. However, the interaction between H and M could create emergent threshold-like behavior (e.g., when H crosses some value, M requirements drop sharply), which would be an interesting model prediction to test.

---

## 2. HABIT RELAPSE AND FAILURE MODES

### 2.1 Polivy & Herman's False Hope Syndrome

**Key papers:**
- Polivy, J., & Herman, C. P. (2000). The False-Hope Syndrome. *Current Directions in Psychological Science*, 9(4), 128-131. DOI: 10.1111/1467-8721.00076

- Polivy, J., & Herman, C. P. (2002). If at first you don't succeed: False hopes of self-change. *American Psychologist*, 57(9), 677-689. DOI: 10.1037/0003-066X.57.9.677

**The cycling mechanism:**
1. Unrealistic expectations about speed, amount, ease, and consequences of self-change
2. Initial commitment brings immediate rewards (improved self-image, sense of control, optimism) regardless of eventual outcome
3. These anticipated benefits override lessons from prior failure
4. Actual change attempt fails to meet unrealistic expectations
5. Failure is interpreted in a way that preserves optimism about future attempts
6. Cycle repeats: new resolution -> initial euphoria -> failure -> reinterpretation -> new resolution

**Model relevance:** This is DIRECTLY captured by the E variable (expectation-reality gap). The cycle maps to: high initial M (from unrealistic expectations) -> E increases as reality disappoints -> M crashes -> H never gets established -> after recovery, unrealistic expectations regenerate M -> repeat. The model should produce limit cycles or oscillatory trajectories when expectations are systematically miscalibrated. This is a key validation target.

---

### 2.2 Relapse Rates for Exercise and Diet

**Key papers:**
- Oscarsson, M., Carlbring, P., Andersson, G., & Rozental, A. (2020). A large-scale experiment on New Year's resolutions: Approach-oriented goals are more successful than avoidance-oriented goals. *PLoS ONE*, 15(12), e0234097. DOI: 10.1371/journal.pone.0234097

**Findings:** N=1,066. 88.8% successful in January, dropping to 54.7% by December. Approach goals (58.9% success) outperformed avoidance goals (47.1%). Physical health (33%), weight loss (20%), and eating habits (13%) were most common resolutions. Moderate support was more effective than either no support or extended support.

- Norcross, J. C., Mrykalo, M. S., & Blagys, M. D. (2002). Auld lang syne: Success predictors, change processes, and self-reported outcomes of New Year's resolvers and nonresolvers. *Journal of Clinical Psychology*, 58(4), 397-405. DOI: 10.1002/jclp.1151

**Findings:** N=159 resolvers followed 6 months. 46% of resolvers were continuously successful at 6 months vs. 4% of nonresolvers. Predictors of success: self-efficacy, skills to change, readiness to change (all assessed pre-January 1). Successful resolvers used more cognitive-behavioral strategies; unsuccessful ones used more awareness/emotion-focused strategies.

**General statistics:** ~80% of New Year's resolutions fail by February. Only 8-10% achieve long-term goals. "Quitter's Day" around January 12-19.

**Model relevance:** The model should reproduce the characteristic exponential-like dropout curve (rapid initial loss, then slower attrition). The approach vs. avoidance framing may map onto M dynamics - approach goals sustain M better. The 46% at 6 months vs. 4% for non-resolvers suggests that explicit commitment (high initial M) matters even if it's not sufficient.

---

### 2.3 Predictors of Successful Habit Formation

**Summary of predictors from literature:**
1. **Self-efficacy** (Norcross et al. 2002; Bandura 1977) - strongest predictor
2. **Approach-oriented goals** vs. avoidance (Oscarsson et al. 2020)
3. **Context stability** (Lally et al. 2010; Verplanken)
4. **Behavior simplicity** (Singh et al. 2024)
5. **Intrinsic reward/enjoyment** (Wiedemann et al. 2014)
6. **Consistency of repetition** (Lally et al. 2010)
7. **Self-selected vs. assigned behaviors** (Singh et al. 2024)
8. **Readiness to change** (Norcross et al. 2002)

**Model relevance:** The model captures simplicity (via C parameter), and motivation (M). Self-efficacy is partially captured by M but may deserve its own representation or coupling term. Intrinsic reward is a potentially MISSING variable - it could be folded into M dynamics (intrinsic reward sustains M independent of E).

---

### 2.4 Self-Efficacy and Habit Maintenance

**Foundational work:**
- Bandura, A. (1977). Self-efficacy: Toward a unifying theory of behavioral change. *Psychological Review*, 84(2), 191-215. DOI: 10.1037/0033-295X.84.2.191
- Bandura, A. (1997). *Self-efficacy: The exercise of control*. New York: W.H. Freeman.

**Key claims:** Self-efficacy determines (a) whether behavior is initiated, (b) how much effort is expended, (c) how long behavior is sustained against obstacles. Four sources: mastery experiences (strongest), vicarious experience, verbal persuasion, physiological/emotional states.

**Habit-specific self-efficacy:**
- Stojanovic, M., Fries, S., & Grund, A. (2021). Self-Efficacy in Habit Building: How General and Habit-Specific Self-Efficacy Influence Behavioral Automatization and Motivational Interference. *Frontiers in Psychology*, 12, 643753. DOI: 10.3389/fpsyg.2021.643753

**Findings:** N=91 (Study 1), N=265 habits (Study 2). General self-efficacy predicted automaticity (b=0.609, p<0.001) but not motivational interference. Habit-specific self-efficacy predicted both. **Critical finding: A positive feedback loop** - lagged HSE predicted automaticity, and lagged automaticity predicted HSE. This is a self-amplifying virtuous cycle.

**Relapse prevention:**
- Larimer, M. E., Palmer, R. S., & Marlatt, G. A. (1999). Relapse prevention: An overview of Marlatt's cognitive-behavioral model. *Alcohol Research & Health*, 23(2), 151-160. PMID: 10890810

**The relapse chain:** High-risk situation -> ineffective coping -> decreased self-efficacy + positive outcome expectancies -> initial lapse -> abstinence violation effect (guilt, personal failure attribution) -> continued lapse -> full relapse.

**Model relevance:** The self-efficacy feedback loop (SE -> automaticity -> SE) maps onto H dynamics where successful repetitions strengthen both H and the motivation to continue. The "abstinence violation effect" maps to a discontinuous drop in M after a lapse, potentially mediated by E. The model may need to capture: (1) the self-efficacy component either within M or as a separate variable, and (2) the asymmetric effect of lapses (missing one day may not hurt H much, but the PSYCHOLOGICAL response to missing can devastate M).

---

## 3. COMPUTATIONAL AND DYNAMICAL MODELS

### 3.1 Lenne (2019) Dynamical Systems Model of Exercise

- Lenne, R. L. (2019). *What sustains behavioral changes? A dynamical systems approach to improving theories of change in physical exercise.* Ph.D. dissertation, University of Minnesota. Retrieved from https://hdl.handle.net/11299/209098

**Model structure:** Two key psychological processes modeled dynamically:
- **Automaticity/Habit** - how automatically exercise is performed
- **Motivation/Satisfaction** - drive to maintain exercise
- **Behavior** - actual exercise tracked via Fitbit

**Key findings:**
- Within-person increases in automaticity in a given week associated with increases in time spent exercising
- Differences in trajectory of automaticity and satisfaction over time differentiate successful vs. unsuccessful maintainers
- The model was constructed, simulated (Study 1), and tested against observational intensive longitudinal data from Fitbit users (Study 2)

**Model relevance:** This is the most directly comparable prior work to the proposed H-M-E model. Lenne's model uses habit and motivation as the two core state variables - very similar to H and M. The proposed model ADDS the E (expectation-reality gap) variable, which is a novel contribution that could capture the False Hope Syndrome cycling and relapse dynamics that Lenne's model likely struggles to produce.

---

### 3.2 Control Theory / Dynamical Systems Approaches

**Foundational:**
- Rivera, D. E., Pew, M. D., & Collins, L. M. (2007). Using engineering control principles to inform the design of adaptive interventions: A conceptual introduction. *Drug and Alcohol Dependence*, 88(Suppl 2), S31-S40. DOI: 10.1016/j.drugalcdep.2006.10.020

**Contribution:** Established that adaptive behavioral interventions are a form of feedback control system. Used process control analogy (liquid level in tank) for behavioral dynamics.

**Most detailed model:**
- Martin, C. A., Rivera, D. E., Hekler, E. B., Riley, W. T., Buman, M. P., Adams, M. A., & Magann, A. B. (2020). Development of a Control-Oriented Model of Social Cognitive Theory for Optimized mHealth Behavioral Interventions. *IEEE Transactions on Control Systems Technology*, 28(2), 331-346. DOI: 10.1109/tcst.2018.2873538

**Model structure:** 6 state variables based on Social Cognitive Theory:
- eta_1: Self-management skills
- eta_2: Outcome expectancies
- eta_3: Self-efficacy
- eta_4: Behavior
- eta_5: Behavioral outcomes
- eta_6: Cue to action

8 exogenous inputs (skills training, vicarious learning, social support, barriers, etc.)

First-order linear ODEs with time constants (tau_i), coupling coefficients (beta_ij, gamma_ij), and disturbance terms. Fluid analogy: inventories that accumulate/deplete over time.

**Key results:**
- Habituation modeled as nonlinear gain scheduling (diminishing response to persistent stimuli)
- Self-efficacy fit: 49.54%; Behavior fit: 34.95% against real data (MILES study, N=68)
- Demonstrated "ambitious but doable" goal-setting produces inverted-U response curve
- Stability requires all feedback gain products < 1
- When goals exceed capability, goal-attainment deficit depletes self-efficacy -> creates nonlinear response despite linear model structure

**Model relevance:** The Martin et al. model is more complex (6 state variables) but the proposed H-M-E model is more parsimonious (3 variables). The Martin model captures self-efficacy explicitly but does NOT have an expectation-reality gap variable. The proposed E variable may be a more elegant way to capture what Martin's model achieves through goal-attainment deficit signals. The habituation/gain-scheduling mechanism in Martin maps to the asymptotic ceiling A in the proposed model.

**Dynamical systems in psychiatry:**
- Salvi, J. D., Rauch, S. L., & Baker, J. T. (2021). Behavior as Physiology: How Dynamical-Systems Theory Could Advance Psychiatry. *American Journal of Psychiatry*, 178(9), 791-792. DOI: 10.1176/appi.ajp.2020.20081151

**Key concepts:** Bifurcations (small parameter changes trigger dramatic state transitions), attractors (mental states as stable regimes), and the idea that dynamic properties - how things change over time - are more diagnostic than static snapshots.

**Model relevance:** Supports the general approach. The H-M-E model could exhibit bifurcations (e.g., a critical point where H is sufficient to sustain behavior without M) and attractors (stable habit state vs. relapse state).

---

### 3.3 Computational Models of Habit in Neuroscience

**Key review:**
- Dolan, R. J., & Dayan, P. (2013). Goals and Habits in the Brain. *Neuron*, 80(2), 312-325. DOI: 10.1016/j.neuron.2013.09.007

**Framework:**
- **Model-based** (goal-directed): Uses internal model of environment to plan actions prospectively. Dorsomedial striatum + prelimbic cortex. Flexible but computationally expensive.
- **Model-free** (habitual): Caches action values from past experience (temporal difference learning). Dorsolateral striatum + infralimbic cortex. Efficient but inflexible to outcome devaluation.

**Key findings:**
- Systems operate simultaneously and competitively
- Arbitration depends on relative uncertainty/computational cost tradeoff
- As experience accumulates, model-free noise decreases -> dominance shifts toward habitual
- Lesions to dorsolateral striatum maintain goal-directed behavior; lesions to dorsomedial striatum produce early habitual behavior

**Empirical:**
- Daw, N. D., Gershman, S. J., Seymour, B., Dayan, P., & Dolan, R. J. (2011). Model-based influences on humans' choices and striatal prediction errors. *Neuron*, 69(6), 1204-1215. DOI: 10.1016/j.neuron.2011.02.027

**Findings:** ~61% model-free, ~39% model-based weighting at population level. Ventral striatal BOLD signals reflected BOTH model-free and model-based predictions, challenging strict dual-system separation.

**Psychopathology implications (Dolan & Dayan 2013):**
- **Addiction:** Dopamine-dependent spirals shift control from goal-directed to habitual, enabling compulsive behavior
- **OCD:** Habitual system overdominance (insensitivity to outcome devaluation)

**Model relevance:** H maps to model-free habit strength; M maps to model-based goal-directed motivation. The competition/arbitration between systems in neuroscience maps to the H-M interaction in the proposed model. The shift from M-dominant to H-dominant with training is a key dynamic the model should capture. The ~60/40 population split suggests most behavior is a blend, not purely one or the other.

---

### 3.4 Dual-Process Models and Their Relation to H and M

**Key papers:**
- Wood, W., & Neal, D. T. (2007). A new look at habits and the habit-goal interface. *Psychological Review*, 114(4), 843-863. DOI: 10.1037/0033-295X.114.4.843

- Neal, D. T., Wood, W., & Quinn, J. M. (2006). Habits - A Repeat Performance. *Current Directions in Psychological Science*, 15(4), 198-202. DOI: 10.1111/j.1467-8721.2006.00435.x

**Key claims:** Habits are response dispositions activated automatically by context cues from past performance. Once formed, habits can be triggered without mediating goals. Goals interface with habits by: (1) motivating the repetition that forms habits, (2) promoting exposure to habit-triggering cues, (3) being inferred from habitual actions.

**Verplanken & Orbell framework:**
- Verplanken, B., & Orbell, S. (2022). Attitudes, habits, and behavior change. *Annual Review of Psychology*, 73, 327-352.

**Key claim:** Attitudes provide initial motivation for not-yet-automatic behavior. With repetition in stable contexts, control shifts from deliberate (attitude/motivation-driven) to automatic (habit-driven). This shift is accompanied by increasing resistance to outcome devaluation.

**Model relevance:** The H-M model directly maps this dual process: early behavior is M-driven (goal-directed), and over time H grows and takes over. The "shift of control" from M to H is a core prediction of the model. The key insight from Wood & Neal is that once H is strong, behavior can persist even when M is low (as long as context cues are present). This means the model should allow behavior to continue when H > threshold even if M is near zero, but only if context is stable.

---

## SUMMARY: MODEL STRENGTHS AND GAPS

### What the H-M-E Model Captures Well:
1. Asymptotic habit growth (H -> A) matches Lally et al. empirically
2. Complexity parameter C affecting formation rate is well-supported
3. M-to-H handoff mirrors dual-process shift from goal-directed to habitual
4. E variable captures False Hope Syndrome cycling (novel contribution vs. Lenne 2019)
5. The relapse dynamics (E -> M crash -> H decay) maps to Marlatt's relapse chain
6. Self-efficacy feedback loops can be embedded in M dynamics

### What the Model May Miss or Need to Address:
1. **Context dependence** - H should be context-coupled; context disruption should reset or weaken H (habit discontinuity hypothesis)
2. **Instigation vs. execution** - H likely captures instigation; execution habit may need separate treatment for complex behaviors
3. **Decay function** - Pure exponential decay is NOT supported; asymptotic/logistic decay is more accurate (Edgren et al. 2025)
4. **Habit persistence paradox** - High H does not guarantee persistence (Bouton 2024); persistence depends on H + context stability + M backup
5. **Self-efficacy feedback loop** - The virtuous cycle (SE <-> H) is well-documented (Stojanovic et al. 2021) and should be explicitly modeled, possibly as a coupling between H and M
6. **Intrinsic reward** - Enjoyment of behavior sustains M independently of E (Wiedemann et al. 2014); may need a term in M dynamics for intrinsic vs. extrinsic motivation
7. **Residual habit** - Old habits may never fully decay to zero (Walker et al. 2015); consider a non-zero floor for H
8. **Approach vs. avoidance framing** - Not currently parameterized but affects M dynamics significantly (Oscarsson et al. 2020)

---

## FULL CITATION LIST

1. Bandura, A. (1977). Self-efficacy: Toward a unifying theory of behavioral change. *Psychological Review*, 84(2), 191-215. DOI: 10.1037/0033-295X.84.2.191

2. Bandura, A. (1997). *Self-efficacy: The exercise of control*. New York: W.H. Freeman.

3. Bouton, M. E. (2024). Habit and persistence. *Journal of Experimental Analysis of Behavior*, 121(1), 88-96. DOI: 10.1002/jeab.894

4. Daw, N. D., Gershman, S. J., Seymour, B., Dayan, P., & Dolan, R. J. (2011). Model-based influences on humans' choices and striatal prediction errors. *Neuron*, 69(6), 1204-1215. DOI: 10.1016/j.neuron.2011.02.027

5. Dolan, R. J., & Dayan, P. (2013). Goals and Habits in the Brain. *Neuron*, 80(2), 312-325. DOI: 10.1016/j.neuron.2013.09.007

6. Edgren, R., Baretta, D., & Inauen, J. (2025). The temporal trajectories of habit decay in daily life: An intensive longitudinal study on four health-risk behaviors. *Applied Psychology: Health and Well-Being*, 17(1), e12612. DOI: 10.1111/aphw.12612

7. Gardner, B. (2024). What is habit and how can it be used to change real-world behaviour? Narrowing the theory-reality gap. *Social and Personality Psychology Compass*, 18, e12975. DOI: 10.1111/spc3.12975

8. Gardner, B., Phillips, L. A., & Judah, G. (2016). Habitual instigation and habitual execution: Definition, measurement, and effects on behaviour frequency. *British Journal of Health Psychology*, 21(3), 613-630. DOI: 10.1111/bjhp.12189

9. Lally, P., van Jaarsveld, C. H. M., Potts, H. W. W., & Wardle, J. (2010). How are habits formed: Modelling habit formation in the real world. *European Journal of Social Psychology*, 40(6), 998-1009. DOI: 10.1002/ejsp.674

10. Larimer, M. E., Palmer, R. S., & Marlatt, G. A. (1999). Relapse prevention: An overview of Marlatt's cognitive-behavioral model. *Alcohol Research & Health*, 23(2), 151-160. PMID: 10890810

11. Lenne, R. L. (2019). *What sustains behavioral changes? A dynamical systems approach to improving theories of change in physical exercise.* Ph.D. dissertation, University of Minnesota. https://hdl.handle.net/11299/209098

12. Martin, C. A., Rivera, D. E., Hekler, E. B., Riley, W. T., Buman, M. P., Adams, M. A., & Magann, A. B. (2020). Development of a Control-Oriented Model of Social Cognitive Theory for Optimized mHealth Behavioral Interventions. *IEEE Transactions on Control Systems Technology*, 28(2), 331-346. DOI: 10.1109/tcst.2018.2873538

13. Neal, D. T., Wood, W., & Quinn, J. M. (2006). Habits - A Repeat Performance. *Current Directions in Psychological Science*, 15(4), 198-202. DOI: 10.1111/j.1467-8721.2006.00435.x

14. Norcross, J. C., Mrykalo, M. S., & Blagys, M. D. (2002). Auld lang syne: Success predictors, change processes, and self-reported outcomes of New Year's resolvers and nonresolvers. *Journal of Clinical Psychology*, 58(4), 397-405. DOI: 10.1002/jclp.1151

15. Orbell, S., & Verplanken, B. (2010). The automatic component of habit in health behavior: Habit as cue-contingent automaticity. *Health Psychology*, 29(4), 374-383. DOI: 10.1037/a0019596

16. Oscarsson, M., Carlbring, P., Andersson, G., & Rozental, A. (2020). A large-scale experiment on New Year's resolutions: Approach-oriented goals are more successful than avoidance-oriented goals. *PLoS ONE*, 15(12), e0234097. DOI: 10.1371/journal.pone.0234097

17. Phillips, L. A., & Gardner, B. (2016). Habitual exercise instigation (vs. execution) predicts healthy adults' exercise frequency. *Health Psychology*, 35(1), 69-77. DOI: 10.1037/hea0000249

18. Polivy, J., & Herman, C. P. (2000). The False-Hope Syndrome. *Current Directions in Psychological Science*, 9(4), 128-131. DOI: 10.1111/1467-8721.00076

19. Polivy, J., & Herman, C. P. (2002). If at first you don't succeed: False hopes of self-change. *American Psychologist*, 57(9), 677-689. DOI: 10.1037/0003-066X.57.9.677

20. Rivera, D. E., Pew, M. D., & Collins, L. M. (2007). Using engineering control principles to inform the design of adaptive interventions: A conceptual introduction. *Drug and Alcohol Dependence*, 88(Suppl 2), S31-S40. DOI: 10.1016/j.drugalcdep.2006.10.020

21. Salvi, J. D., Rauch, S. L., & Baker, J. T. (2021). Behavior as Physiology: How Dynamical-Systems Theory Could Advance Psychiatry. *American Journal of Psychiatry*, 178(9), 791-792. DOI: 10.1176/appi.ajp.2020.20081151

22. Singh, B., Murphy, A., Maher, C., & Smith, A. E. (2024). Time to Form a Habit: A Systematic Review and Meta-Analysis of Health Behaviour Habit Formation and Its Determinants. *Healthcare*, 12(23), 2488. DOI: 10.3390/healthcare12232488

23. Stojanovic, M., Fries, S., & Grund, A. (2021). Self-Efficacy in Habit Building: How General and Habit-Specific Self-Efficacy Influence Behavioral Automatization and Motivational Interference. *Frontiers in Psychology*, 12, 643753. DOI: 10.3389/fpsyg.2021.643753

24. Thomas, G. O., Poortinga, W., & Sautkina, E. (2016). Habit Discontinuity, Self-Activation, and the Diminishing Influence of Context Change: Evidence from the UK Understanding Society Survey. *PLoS ONE*, 11(4), e0153490. DOI: 10.1371/journal.pone.0153490

25. Verplanken, B., & Orbell, S. (2022). Attitudes, habits, and behavior change. *Annual Review of Psychology*, 73, 327-352.

26. Verplanken, B., & Roy, D. (2016). Empowering interventions to promote sustainable lifestyles: Testing the habit discontinuity hypothesis in a field experiment. *Journal of Environmental Psychology*, 45, 127-134. DOI: 10.1016/j.jenvp.2015.11.003

27. Walker, I., Thomas, G. O., & Verplanken, B. (2015). Old Habits Die Hard. *Environment and Behavior*, 47(10), 1089-1106. DOI: 10.1177/0013916514549619

28. Wiedemann, A. U., Gardner, B., Knoll, N., & Burkert, S. (2014). Intrinsic rewards, fruit and vegetable consumption, and habit strength: A three-wave study testing the associative-cybernetic model. *Applied Psychology: Health and Well-Being*, 6(1), 119-134. DOI: 10.1111/aphw.12020

29. Wood, W., & Neal, D. T. (2007). A new look at habits and the habit-goal interface. *Psychological Review*, 114(4), 843-863. DOI: 10.1037/0033-295X.114.4.843

---

## 4. MOTIVATION AND SELF-REGULATION DYNAMICS

### 4.1 Ego Depletion Debate: Is the "Limited Resource" Model Valid?

**The Original Model:**
- Baumeister, R. F., Bratslavsky, E., Muraven, M., & Tice, D. M. (1998). Ego depletion: Is the active self a limited resource? *Journal of Personality and Social Psychology*, 74(5), 1252-1265. PMID: 9599441
- **Claim:** Self-control draws on a limited inner resource; exerting self-control depletes this resource, leaving subsequent self-control efforts prone to failure. The original meta-analysis of ~200 studies found d = 0.62.

**The Critique (Inzlicht & Berkman):**
- Inzlicht, M. & Berkman, E. (2015). Six questions for the resource model of control (and some answers). *Social and Personality Psychology Compass*, 9(10), 511-524. DOI: 10.1111/spc3.12200. PMID: 28966660
- **Key claims:**
  - Bias-corrected effect size estimates range from d = 0.48 down to d ~ 0.00 depending on method.
  - The specific "resource" that is depleted has never been identified. The glucose hypothesis failed replication and is biologically implausible.
  - Incentives, changed perceptions, and altered construals readily reverse depletion effects -- incompatible with literal resource exhaustion.
  - The revised "central governor" model (which posits only partial depletion) is unfalsifiable and indistinguishable from a motivational account.
  - Ego depletion and mental fatigue are essentially identical: both reflect shifts in motivation and priorities, not resource depletion.

**The Replication Crisis:**
- Hagger, M. S., et al. (2016). A multilab preregistered replication of the ego-depletion effect. *Perspectives on Psychological Science*, 11(4), 546-573.
  - 23 labs, N > 2,000: Found NO significant ego depletion effect.
- Dang, J., Barker, P., Baumert, A., et al. (2020). A multilab replication of the ego depletion effect. *Social Psychological and Personality Science*, 12(1), 14-24. DOI: 10.1177/1948550619887702
  - 12 labs, N = 1,775: Small but significant effect, d = 0.10 (d = 0.16 after excluding random responders).
  - Conclusion: The effect may exist but is far smaller than originally claimed.

**Model fit assessment:** The proposed model treats M as depleted by effort. This aligns with the MOTIVATIONAL reinterpretation of ego depletion (willingness, not ability, declines). The model should NOT assume a literal finite resource that is consumed, but rather a shifting cost-benefit calculation. The opportunity cost framework (see 4.2) provides the more appropriate mechanism.

---

### 4.2 The Opportunity Cost Model of Effort

- Kurzban, R., Duckworth, A., Kable, J. W., & Myers, J. (2013). An opportunity cost model of subjective effort and task performance. *Behavioral and Brain Sciences*, 36(6), 661-679. DOI: 10.1017/S0140525X12003196. PMID: 24304775
- **Key claims:**
  - Executive function mechanisms can only be deployed for a limited number of tasks simultaneously.
  - The phenomenology of effort reflects the OPPORTUNITY COST of allocating these mechanisms to the current task vs. alternatives.
  - The sensation of mental effort is the output of mechanisms designed to measure opportunity costs.
  - Performance improves when appealing alternatives are removed or rewards increase, even after "depleting" tasks.
  - Subjective effort = felt output of cost/benefit computations, NOT the draining of a resource.
  - Fatigue represents a signal that reallocation would be beneficial, not that a tank is empty.
- **Key predictions:**
  1. Performance declines when appealing alternatives are available.
  2. Incentive increases improve performance even after "depleting" tasks.
  3. Performance decrements are larger between similar tasks recruiting overlapping neural systems.
  4. Manipulations changing experienced effort correspondingly alter task performance.

**Model fit assessment:** The "effort depletion" term in the model should be reframed as increasing opportunity cost rather than resource consumption. M doesn't decay because fuel is spent, but because the perceived cost of continued effort rises relative to alternatives. The model CAPTURES this if the depletion term is interpreted as shifting cost-benefit, but MISSES it if interpreted as literal resource consumption.

---

### 4.3 Temporal Dynamics of Motivation: Functional Form

**Temporal Motivation Theory (TMT):**
- Steel, P. & Konig, C. J. (2006). Integrating theories of motivation. *Academy of Management Review*, 31(4), 889-913.
- **The Motivation Equation:** Motivation = (Expectancy x Value) / (1 + Impulsiveness x Delay)
- **Key claim:** Motivation follows a HYPERBOLIC function of temporal delay, NOT a simple exponential decay. The perceived utility of an activity increases hyperbolically as a deadline nears, consistent with behavioral economics literature on delay discounting. Procrastination is explained by hyperbolic sensitivity to delay.

**Temporal Self-Regulation Theory (TST):**
- Hall, P. A. & Fong, G. T. (2015). Temporal self-regulation theory: A neurobiologically informed model for physical activity behavior. *Frontiers in Human Neuroscience*, 9, 117. DOI: 10.3389/fnhum.2015.00117. PMID: 25859196
- **Key claims:**
  - "Outcomes that are temporally nearer are of more value, with immediacy associated with a very sharp spike in value" (hyperbolic discount curve).
  - Physical activity brings immediately felt costs and gradually accumulated benefits -- a temporal mismatch creating self-regulatory demands.
  - Recursive feedback loops: consistent activity strengthens executive function (EF), which reinforces adherence.
  - Without sustained EF and intention strength, individuals revert to preferring immediately available sedentary alternatives.

**Fresh Start Effect:**
- Dai, H., Milkman, K. L., & Riis, J. (2014). The fresh start effect: Temporal landmarks motivate aspirational behavior. *Management Science*, 60(10), 2563-2582.
- **Key claims:**
  - Gym visits increase 33% at the start of a new week, 47% at start of a new semester.
  - Temporal landmarks (New Year, birthdays, Mondays) create "fresh starts" that boost motivation.
  - These landmarks relegate past failures to a "previous period," boosting self-efficacy.
  - Google searches for "diet" spike at temporal landmarks across all years studied.

**Model fit assessment:** The proposed model assumes EXPONENTIAL decay of M, but TMT supports HYPERBOLIC decay. Hyperbolic discounting produces steeper initial decline and a longer tail than exponential decay. The "fresh start" phenomenon suggests M can be DISCONTINUOUSLY reset by temporal landmarks -- not just boosted by external shocks, but by cognitive reframing events. The model should consider whether M decays exponentially, hyperbolically, or via some other form.

---

### 4.4 Self-Determination Theory (SDT): Intrinsic vs. Extrinsic Motivation

- Ryan, R. M. & Deci, E. L. (2000). Self-determination theory and the facilitation of intrinsic motivation, social development, and well-being. *American Psychologist*, 55(1), 68-78. DOI: 10.1037//0003-066x.55.1.68. PMID: 11392867
- Ryan, R. M. & Deci, E. L. (2020). Intrinsic and extrinsic motivation from a self-determination theory perspective: Definitions, theory, practices, and future directions. *Contemporary Educational Psychology*, 61, 101860.

**Key claims:**
- Three basic psychological needs: autonomy, competence, and relatedness. When satisfied, they yield enhanced self-motivation; when thwarted, diminished motivation.
- Intrinsic motivation (doing things for their own sake) is qualitatively different from extrinsic motivation (for external rewards).
- External rewards can UNDERMINE intrinsic motivation (the "overjustification effect").
- Motivation exists on a continuum: amotivation -> external regulation -> introjected regulation -> identified regulation -> integrated regulation -> intrinsic motivation.
- More autonomous (internalized) forms of motivation predict greater persistence, performance, and well-being.
- Autonomy support from coaches/trainers facilitates internalization; controlling environments undermine it.

**Model fit assessment:** The proposed model treats M as a single scalar. SDT shows motivation is MULTIDIMENSIONAL -- intrinsic and extrinsic motivation have different dynamics, persistence, and relationships to effort. Intrinsic motivation may not decay the same way as extrinsic motivation. A high M driven by external pressure (health scare) will decay differently than a high M driven by genuine enjoyment. This is a significant limitation of a unidimensional M.

---

### 4.5 Motivational "Shocks" and Their Temporal Trajectory

**Teachable Moments:**
- McBride, C. M., Emmons, K. M., & Lipkus, I. M. (2003). Understanding the potential of teachable moments: The case of smoking cessation. *Health Education Research*, 18(2), 156-170.
- Brust, M., Gebhardt, W. A., van der Voorde, N. A. E., Numans, M. E., & Kiefte-de Jong, J. C. (2022). The development and validation of scales to measure the presence of a teachable moment following a cardiovascular disease event. *Preventive Medicine Reports*, 28, 101876. DOI: 10.1016/j.pmedr.2022.101876
- **Key claims:**
  - Health scares create "teachable moments" with three components: (1) increased risk perception, (2) affective impact, (3) changed self-concept.
  - These windows are TIME-DEPENDENT and fade without appropriate reinforcement.
  - TMs may create a temporary elevation of M that decays unless structurally supported.

**Cardiac Event Trajectories:**
- Middleton, K. R., Anton, S. D., & Perri, M. G. (2013). Long-term adherence to health behavior change. *American Journal of Lifestyle Medicine*, 7(6), 395-404. DOI: 10.1177/1559827613488867
- **Key claims:**
  - Despite cardiac rehabilitation, exercise follows a downward trajectory during the year after a cardiac event.
  - Non-adherence rates for chronic illness treatment: 50-80%.
  - Weight management: 8-10% initial loss, half regained within a year, back to baseline within 3-5 years.
  - Physiological counter-regulation (decreased metabolic rate, increased hunger signals) actively fights maintained change.
  - Without behavioral intervention, participants were 76% more likely to stop exercising in the year after cardiac rehab.

**Lapse and Relapse Patterns:**
- Kwasnicka, D., Dombrowski, S. U., White, M., & Sniehotta, F. (2016). Theoretical explanations for maintenance of behaviour change. *Health Psychology Review*, 10(3), 277-296.
- **Key claims:**
  - Majority of relapses occur in the first several months.
  - Dropout rates level off at 55-75% (only 25-45% continue exercising after one year).
  - Self-determined motivation at end of cardiac rehab predicts exercise at 3- and 6-week follow-up.

**Model fit assessment:** The model's motivational shock mechanism (impulse function boosting M followed by decay) is PARTIALLY SUPPORTED. The literature confirms the decay pattern but suggests phase transitions (the 3-6 month critical period, then leveling). The model should also account for PHYSIOLOGICAL COUNTER-REGULATION (the body fights behavior change at metabolic level). The teachable moment concept supports the shock mechanism but emphasizes that the shock alone is insufficient without structural support.

---

## 5. REWARD SIGNALING AND LEARNING

### 5.1 Dopamine Prediction Error Signals and Habit Formation

- Schultz, W. (2016). Dopamine reward prediction error coding. *Dialogues in Clinical Neuroscience*, 18(1), 23-32. DOI: 10.31887/DCNS.2016.18.1/wschultz. PMID: 27069377
- Schultz, W., Dayan, P., & Montague, P. R. (1997). A neural substrate of prediction and reward. *Science*, 275(5306), 1593-1599. PMID: 9054347
- Hollerman, J. R. & Schultz, W. (1998). Dopamine neurons report an error in the temporal prediction of reward during learning. *Nature Neuroscience*, 1(4), 304-309.

**Key claims:**
- Dopamine neurons fire for POSITIVE prediction errors (better than expected), remain at baseline for fully predicted rewards, and are depressed for NEGATIVE prediction errors (worse than expected).
- During learning, the dopamine response TRANSFERS from the reward itself to the earliest predictive cue (reward-predicting stimulus). This stepwise transfer allows organisms to anticipate rewards.
- Once a reward is fully predicted, it no longer generates a dopamine response -- the system requires NOVELTY or SURPRISE to maintain signaling.
- Temporal discounting: dopamine response magnitude decreases with longer delays between cue and reward.
- The responses align with formal temporal difference (TD) learning mathematics, providing neurobiological evidence for error-correction learning.

**Model fit assessment:** The model's reward term for M is supported, but prediction error theory implies rewards should have DIMINISHING RETURNS on M as they become expected. The model should incorporate a prediction error term (reward minus expected reward) rather than a fixed reward boost. The cue-transfer phenomenon suggests M should become increasingly cue-triggered rather than reward-triggered as habit formation progresses. This is not currently captured.

---

### 5.2 Goal-Directed to Habitual Control Transition

- Daw, N. D., Niv, Y., & Dayan, P. (2005). Uncertainty-based competition between prefrontal and dorsolateral striatal systems for behavioral control. *Nature Neuroscience*, 8, 1704-1711. PMID: 16286932
- Daw, N. D., Gershman, S. J., Seymour, B., Dayan, P., & Dolan, R. J. (2011). Model-based influences on humans' choices and striatal prediction errors. *Neuron*, 69(6), 1204-1215. DOI: 10.1016/j.neuron.2011.02.027. PMID: 21435563
- Tricomi, E., Balleine, B. W., & O'Doherty, J. P. (2009). A specific role for posterior dorsolateral striatum in human habit learning. *European Journal of Neuroscience*, 29(11), 2225-2232.

**Key claims:**
- Two parallel learning systems: model-based (prefrontal, goal-directed) and model-free (dorsolateral striatum, habitual).
- Arbitration between systems is based on relative UNCERTAINTY: each controller is deployed when it should be most accurate (Bayesian arbitration principle).
- Model-free system is computationally cheap but inflexible; model-based is flexible but costly.
- The transition is GRADUAL: DLS recruitment increases progressively with training, not a discrete switch.
- Model-based signatures appear even in ventral striatum, challenging strict dual-system separation.
- At population level: ~61% model-free, ~39% model-based weighting.
- The two systems develop IN PARALLEL and can compete or cooperate.

**Model fit assessment:** The model may need to distinguish between two components of M: a deliberative/goal-directed component (requiring effort, amenable to rational persuasion) and an automatic/habitual component (cue-triggered, effort-free). As behavior becomes habitual, the nature of M changes qualitatively. The current model treats M as a single undifferentiated quantity, which MISSES this dual-system architecture.

---

### 5.3 Reward Devaluation and Habit Persistence

- de Wit, S., Kindt, M., Knot, S. L., et al. (2018). Shifting the balance between goals and habits: Five failures in experimental habit induction. *Journal of Experimental Psychology: General*, 147(7), 1043-1065. DOI: 10.1037/xge0000402

**Key claims:**
- In rodents, overtraining reliably produces outcome-insensitive (habitual) responding -- animals continue lever-pressing even after reward devaluation.
- In HUMANS, five experimental attempts to induce habits through overtraining FAILED across multiple paradigms (avoidance tasks, appetitive rewards, replications of prior work).
- Extensive training did NOT lead to greater outcome devaluation insensitivity in any of the five experiments.
- Human "habits" may operate differently from rodent habits -- possibly always retaining some goal-directed character.
- Inflexible behavior in psychiatric populations may reflect dysfunction in GOAL-DIRECTED control, not overactive habit learning.

**Model fit assessment:** CRITICAL finding. If human habits do not show robust outcome insensitivity, then a behavioral variable B that becomes fully autonomous from M may be less justified than assumed. Human exercise habits may always remain partially goal-directed, meaning M continues to matter even for "habitual" exercisers. The model should not assume that high H makes behavior immune to motivational disruption.

---

### 5.4 "Phantom Rewards" of Fantasy (Oettingen's Neuroscience Perspective)

- Kappes, H. B. & Oettingen, G. (2011). Positive fantasies about idealized futures sap energy. *Journal of Experimental Social Psychology*, 47(4), 719-729.
- Sevincer, A. T., Busatta, P. D., & Oettingen, G. (2014). Mental contrasting and transfer of energization. *Personality and Social Psychology Bulletin*, 40(2), 139-152. DOI: 10.1177/0146167213507088. PMID: 24145296

**Key claims:**
- Pure positive fantasy about a desired future DECREASES energization, measured by drops in systolic blood pressure.
- Four experiments showed that induced positive fantasies produced less energy than questioning, negative, or neutral fantasies.
- The brain's reward circuitry treats vivid positive fantasy as if the goal has already been partially achieved, providing a "phantom reward" that reduces the dopamine-driven motivation to act.
- Mental contrasting (fantasy + obstacle awareness) INCREASES energization when expectations of success are high, and leads to adaptive disengagement when expectations are low.
- Energization from mental contrasting is TRANSFERABLE to unrelated tasks -- it creates a general arousal state, not task-specific motivation.
- Energization driven by dopamine and norepinephrine supports approach behavior; fatigue from serotonin and inflammatory cytokines underwrites avoidance.

**Model fit assessment:** If M can be boosted by fantasy/visualization but this boost REDUCES actual behavioral activation (by providing a phantom reward), then the model needs to distinguish between motivational states that drive action and those that substitute for action. Pure positive fantasy increases felt M but decreases behavioral output -- a paradox the model may not capture with a single M variable.

---

## 6. AFFECTIVE DYNAMICS

### 6.1 Affect as Information Theory

- Schwarz, N. & Clore, G. L. (1983). Mood, misattribution, and judgments of well-being: Informative and directive functions of affective states. *Journal of Personality and Social Psychology*, 45(3), 513-523.
- Schwarz, N. (2012). Feelings-as-information theory. In P. Van Lange, A. Kruglanski, & E. T. Higgins (Eds.), *Handbook of theories of social psychology* (pp. 289-308). Sage.

**Key claims:**
- People use their current affective state as INFORMATION when making judgments and decisions.
- Mood signals the valence of the current environment: positive mood = safe, proceed; negative mood = problematic, be careful.
- When affect is attributed to an irrelevant source, its influence on judgment DISAPPEARS (the "attribution effect").
- Positive mood -> heuristic processing, less elaboration; negative mood -> systematic processing, more elaboration.
- Different feelings provide different types of information: moods about general environment, emotions about specific objects, metacognitive feelings about one's own processing.

**Model fit assessment:** Affect modulates M not just as a direct input but as an INFORMATIONAL signal. If someone feels bad during exercise, they may interpret this as evidence that exercise is bad for them (even if the bad mood is from an unrelated source). The model should account for how affect is interpreted and attributed, not just its raw valence. Misattribution of incidental affect to the exercise experience could systematically bias M updates.

---

### 6.2 Exercise-Affect Relationship and the Affective Valence Hypothesis

**Dual-Mode Theory:**
- Ekkekakis, P. (2009). The dual-mode theory of affective responses to exercise in metatheoretical context: I & II. *International Review of Sport and Exercise Psychology*, 2(1), 73-94 and 2(2), 119-150.

**Key claims:**
- Below ventilatory threshold (VT): affect is consistently POSITIVE, cognitive factors (self-efficacy, goals) dominate the affective response.
- At VT: affect is HIGHLY VARIABLE across individuals.
- Above VT: affect becomes consistently NEGATIVE, interoceptive (physiological) factors dominate, overriding cognitive appraisals.
- The shift from cognitive to interoceptive dominance is systematic and predictable by exercise intensity.

**Affect-Adherence Link:**
- Williams, D. M. (2008). Exercise, affect, and adherence: An integrated model and a case for self-paced exercise. *Journal of Sport and Exercise Psychology*, 30(5), 471-496. DOI: 10.1123/jsep.30.5.471

**Key claims:**
- Affective response during moderate-intensity exercise at baseline predicted physical activity participation at 6 and 12 months.
- A 1-unit increase on the Feeling Scale during exercise predicts 38 additional minutes/week of exercise at 6 months.
- In-task affect is a stronger predictor of future exercise than post-exercise affect.
- Hedonic theory: people seek to prolong pleasure and minimize displeasure. Expected affect determines whether behavior is repeated.

**Affective-Reflective Theory (ART):**
- Brand, R. & Ekkekakis, P. (2018). Affective-reflective theory of physical inactivity and exercise. *German Journal of Exercise and Sport Research*, 48, 48-58.

**Key claims:**
- Exercise-related stimuli trigger AUTOMATIC affective associations (type-1 process), which form the basis for reflective evaluation (type-2 process).
- The automatic affective valuation connects directly with action impulses -- positive associations promote approach, negative associations promote avoidance.
- Implicit attitudes toward exercise (measured via reaction-time tasks) predict behavior beyond explicit intentions (Conroy et al., 2010; Kiviniemi et al., 2007).
- Changing the affective valuation requires consistently coupling exercise with pleasant experiences.

**Affective Determinants Framework:**
- Stevens, C. J., Baldwin, A. S., Bryan, A. D., Conner, M., Rhodes, R. E., & Williams, D. M. (2020). Affective determinants of physical activity: A conceptual framework and narrative review. *Frontiers in Psychology*, 11, 568331. DOI: 10.3389/fpsyg.2020.568331

**Key claims:**
- Four categories of affective influence on physical activity: (1) affective response during/after PA, (2) incidental affect, (3) affect processing (cognitive processing of prior experiences), (4) affectively charged motivational states.
- Automatic affective associations predict PA engagement even after controlling for deliberative variables.

**Model fit assessment:** The in-task affective experience should feed back into M, and the model should distinguish between in-task and post-task affect. The dual-mode theory suggests exercise prescribed above VT will consistently generate negative affect, depleting M faster. Self-paced exercise preserves M better. The model PARTIALLY captures this through effort depletion but may not represent the intensity-dependent sign change of the affective feedback. Below VT, exercise BOOSTS M; above VT, exercise DEPLETES M -- a nonlinearity the model should incorporate.

---

### 6.3 Dynamic Models of Affect (Affective Chronometry)

- Kuppens, P., Allen, N. B., & Sheeber, L. B. (2010). Emotional inertia and psychological maladjustment. *Psychological Science*, 21(7), 984-991.
- Kuppens, P., Oravecz, Z., & Tuerlinckx, F. (2010). Feelings change: Accounting for individual differences in the temporal dynamics of affect. *Journal of Personality and Social Psychology*, 99(6), 1042-1060.
- Bringmann, L. F., Pe, M. L., Vissers, N., et al. (2016). Assessing temporal emotion dynamics using networks. *Assessment*, 23(4), 425-435.
- Russell, J. A. (1980). A circumplex model of affect. *Journal of Personality and Social Psychology*, 39(6), 1161-1178.

**Key claims:**
- Core affect has two dimensions: valence (pleasant-unpleasant) and arousal (low-high activation).
- Emotional INERTIA (autocorrelation of affect over time) is associated with maladjustment, depression, rumination, low self-esteem. Operationalized as the first-order autoregressive coefficient in time-series models.
- Higher inertia = affect carries over more from one moment to the next (more "sticky" emotional states).
- The "inertia-instability paradox" in depression: depressed individuals show BOTH high inertia AND high variability -- resolved by statistical overlap between these measures.
- Affect dynamics can be modeled using autoregressive time-series, network approaches, and ecological momentary assessment.
- Less pleasant average affect correlates with more variable core affect, particularly in experiencing qualitatively different feelings.

**Model fit assessment:** The model should incorporate affect dynamics as an autoregressive process feeding into M. The inertia concept is directly relevant: some individuals' M will be more "sticky" while others' will be more volatile. The model could represent individual differences in the decay rate of M as differences in affective inertia. The exponential decay parameter in the model corresponds to (1 - inertia) in the affective dynamics literature.

---

## 7. MENTAL CONTRASTING AND IMPLEMENTATION INTENTIONS

### 7.1 Oettingen's WOOP / Mental Contrasting

- Oettingen, G. (2012). Future thought and behaviour change. *European Review of Social Psychology*, 23(1), 1-63.
- Oettingen, G. & Reininger, K. M. (2016). The power of prospection: Mental contrasting and behavior change. *Social and Personality Psychology Compass*, 10(11), 591-604.

**Key claims:**
- Three modes of future thought: INDULGING (pure fantasy), DWELLING (pure obstacle focus), and MENTAL CONTRASTING (fantasy + obstacles).
- Pure positive fantasy REDUCES energization (systolic blood pressure drops -- Kappes & Oettingen, 2011).
- Mental contrasting produces energization proportional to EXPECTATIONS OF SUCCESS:
  - High expectations -> strong commitment and energization.
  - Low expectations -> disengagement (adaptively abandoning unattainable goals).
- Effects are mediated by three non-conscious processes: cognition (strengthened obstacle-behavior associations), energization (physiological mobilization), and response to feedback.
- Mental contrasting changes the MEANING of reality: obstacles become challenges to overcome rather than immovable barriers.

**Model fit assessment:** Mental contrasting could be modeled as a mechanism that CALIBRATES M according to realistic expectations, rather than simply boosting it. The model's shock mechanism doesn't distinguish between adaptive (expectation-calibrated) boosts and maladaptive (pure fantasy) boosts. This is an important missing mechanism: not all M-boosts are created equal.

---

### 7.2 Gollwitzer's Implementation Intentions

- Gollwitzer, P. M. (1999). Implementation intentions: Strong effects of simple plans. *American Psychologist*, 54(7), 493-503.
- Gollwitzer, P. M. & Sheeran, P. (2006). Implementation intentions and goal achievement: A meta-analysis of effects and processes. *Advances in Experimental Social Psychology*, 38, 69-119.

**Key claims:**
- Implementation intentions are if-then plans: "If situation X arises, then I will perform behavior Y."
- Meta-analysis of 94 studies: medium-to-large effect (d = 0.65) on goal attainment.
- Two mechanisms:
  1. ENHANCED CUE ACCESSIBILITY: the if-part becomes highly accessible in memory when the goal is active.
  2. STRATEGIC AUTOMATICITY: a strong associative link between situation and action enables behavior to be initiated immediately, efficiently, and without conscious deliberation.
- Implementation intentions essentially "delegate" behavioral control to environmental cues, creating instant quasi-habits.
- Effective for initiating goal striving, shielding from distractions, disengaging from failing strategies, and conserving self-regulatory resources.

**Model fit assessment:** Implementation intentions change the M-to-B TRANSFER FUNCTION, not M itself. They reduce the threshold of M needed to produce behavior by creating automaticity. The model might represent this as a reduction in the activation threshold, an increase in cue sensitivity, or a boost to H (since IIs create automaticity similar to habit). Implementation intentions don't boost M; they change how efficiently M converts to behavior.

---

### 7.3 Combined MCII Effects

- Duckworth, A. L., Grant, H., Loew, B., Oettingen, G., & Gollwitzer, P. M. (2011). Self-regulation strategies improve self-discipline in adolescents: Benefits of mental contrasting and implementation intentions. *Educational Psychology*, 31(1), 17-26.
- Stadler, G., Oettingen, G., & Gollwitzer, P. M. (2009). Physical activity in women: Effects of a self-regulation intervention. *American Journal of Preventive Medicine*, 36(1), 29-34.
- Wang, G., Wang, Y., & Gai, X. (2021). A meta-analysis of the effects of mental contrasting with implementation intentions on goal attainment. *Frontiers in Psychology*, 12, 565202. DOI: 10.3389/fpsyg.2021.565202

**Key findings from meta-analysis (24 studies, N = 15,907):**
- Overall MCII effect: g = 0.336, 95% CI [0.229, 0.443] (small-to-medium).
- By domain: academic (g = 0.255), health (g = 0.379), personal (g = 0.457), relationships (g = 0.609).
- Experimenter-led interventions (g = 0.465) outperform document-based (g = 0.277).
- MC provides motivational commitment; II provides volitional mechanism.
- Combined, they address both the "motivation gap" and the "intention-behavior gap."

**Model fit assessment:** MCII represents a compound intervention that both CALIBRATES M (via MC) and changes the M-to-B TRANSFER FUNCTION (via II). The model would need at least two parameters to capture this: one for motivational calibration and one for automaticity/cue-binding. This is a concrete, empirically validated intervention that the model should be able to simulate.

---

## 8. EXPANDED SUMMARY: KEY IMPLICATIONS FOR THE PROPOSED MODEL

### What the Model CAPTURES Well:
1. The general decay of motivation over time after an initial boost (health scare, resolution).
2. The concept that effort depletes motivational resources (when reframed as opportunity cost).
3. The role of reward in sustaining motivation.
4. The basic shock-and-decay pattern of motivational activation.
5. The relapse dynamics captured by the E variable (expectation-reality gap).

### What the Model MISSES or Should Modify:

1. **Functional form of decay**: Literature supports HYPERBOLIC rather than exponential decay of M (Steel & Konig, 2006). Hyperbolic produces steeper initial decline and longer tail.

2. **Multidimensionality of motivation**: SDT shows intrinsic and extrinsic motivation have qualitatively different dynamics and persistence (Ryan & Deci, 2000). A health-scare-driven M decays differently from an enjoyment-driven M.

3. **Prediction error vs. fixed reward**: Dopamine signals reward PREDICTION ERROR, not absolute reward (Schultz, 2016). The model's reward term should diminish as the reward becomes expected.

4. **Dual-system architecture**: The goal-directed/habitual distinction (Daw et al., 2005) suggests M should have two components with different dynamics. As behavior becomes habitual, M changes qualitatively.

5. **Affective feedback is intensity-dependent**: Below VT, exercise boosts affect (and thus M). Above VT, exercise depletes affect (Ekkekakis, 2009). The sign of the affect feedback changes with intensity -- a critical nonlinearity.

6. **Phantom reward problem**: Pure positive fantasy can boost subjective M while REDUCING actual energization (Kappes & Oettingen, 2011). The model needs to distinguish felt motivation from action-driving motivation.

7. **Human habits are fragile**: Unlike rodent habits, human exercise habits may never become fully outcome-insensitive (de Wit et al., 2018). M always matters.

8. **Implementation intentions change the transfer function**: IIs don't boost M; they reduce the M needed for behavior (Gollwitzer, 1999). This is a different mechanism than the model currently represents.

9. **Fresh start discontinuities**: Temporal landmarks create discontinuous jumps in M (Dai et al., 2014) through cognitive reframing, not just external shocks.

10. **Affect-as-information**: How people INTERPRET their affective states (not just raw valence) determines impact on M (Schwarz & Clore, 1983). Misattribution effects could systematically bias M updates.

11. **Opportunity cost framing**: Effort depletion is better modeled as rising opportunity cost, not resource consumption (Kurzban et al., 2013). This means M depletion should be context-sensitive (it depends on what alternatives are available).

12. **Affective inertia as individual difference**: The decay rate of M should vary between individuals, corresponding to differences in emotional inertia (Kuppens et al., 2010). High-inertia individuals may have more persistent M (both when high and when low).

---

## ADDITIONAL CITATIONS (Sections 4-7)

30. Baumeister, R. F., Bratslavsky, E., Muraven, M., & Tice, D. M. (1998). Ego depletion: Is the active self a limited resource? *Journal of Personality and Social Psychology*, 74(5), 1252-1265. PMID: 9599441

31. Inzlicht, M. & Berkman, E. (2015). Six questions for the resource model of control (and some answers). *Social and Personality Psychology Compass*, 9(10), 511-524. DOI: 10.1111/spc3.12200. PMID: 28966660

32. Hagger, M. S., et al. (2016). A multilab preregistered replication of the ego-depletion effect. *Perspectives on Psychological Science*, 11(4), 546-573.

33. Dang, J., et al. (2020). A multilab replication of the ego depletion effect. *Social Psychological and Personality Science*, 12(1), 14-24. DOI: 10.1177/1948550619887702

34. Kurzban, R., Duckworth, A., Kable, J. W., & Myers, J. (2013). An opportunity cost model of subjective effort and task performance. *Behavioral and Brain Sciences*, 36(6), 661-679. DOI: 10.1017/S0140525X12003196. PMID: 24304775

35. Steel, P. & Konig, C. J. (2006). Integrating theories of motivation. *Academy of Management Review*, 31(4), 889-913.

36. Hall, P. A. & Fong, G. T. (2015). Temporal self-regulation theory: A neurobiologically informed model for physical activity behavior. *Frontiers in Human Neuroscience*, 9, 117. DOI: 10.3389/fnhum.2015.00117. PMID: 25859196

37. Dai, H., Milkman, K. L., & Riis, J. (2014). The fresh start effect: Temporal landmarks motivate aspirational behavior. *Management Science*, 60(10), 2563-2582.

38. Ryan, R. M. & Deci, E. L. (2000). Self-determination theory and the facilitation of intrinsic motivation, social development, and well-being. *American Psychologist*, 55(1), 68-78. DOI: 10.1037//0003-066x.55.1.68. PMID: 11392867

39. Ryan, R. M. & Deci, E. L. (2020). Intrinsic and extrinsic motivation from a self-determination theory perspective. *Contemporary Educational Psychology*, 61, 101860.

40. McBride, C. M., Emmons, K. M., & Lipkus, I. M. (2003). Understanding the potential of teachable moments. *Health Education Research*, 18(2), 156-170.

41. Brust, M., et al. (2022). The development and validation of scales to measure the presence of a teachable moment following a CVD event. *Preventive Medicine Reports*, 28, 101876. DOI: 10.1016/j.pmedr.2022.101876

42. Middleton, K. R., Anton, S. D., & Perri, M. G. (2013). Long-term adherence to health behavior change. *American Journal of Lifestyle Medicine*, 7(6), 395-404. DOI: 10.1177/1559827613488867

43. Schultz, W. (2016). Dopamine reward prediction error coding. *Dialogues in Clinical Neuroscience*, 18(1), 23-32. DOI: 10.31887/DCNS.2016.18.1/wschultz. PMID: 27069377

44. Schultz, W., Dayan, P., & Montague, P. R. (1997). A neural substrate of prediction and reward. *Science*, 275(5306), 1593-1599. PMID: 9054347

45. Hollerman, J. R. & Schultz, W. (1998). Dopamine neurons report an error in the temporal prediction of reward during learning. *Nature Neuroscience*, 1(4), 304-309.

46. Daw, N. D., Niv, Y., & Dayan, P. (2005). Uncertainty-based competition between prefrontal and dorsolateral striatal systems for behavioral control. *Nature Neuroscience*, 8, 1704-1711. PMID: 16286932

47. Daw, N. D., Gershman, S. J., Seymour, B., Dayan, P., & Dolan, R. J. (2011). Model-based influences on humans' choices and striatal prediction errors. *Neuron*, 69(6), 1204-1215. DOI: 10.1016/j.neuron.2011.02.027. PMID: 21435563

48. Tricomi, E., Balleine, B. W., & O'Doherty, J. P. (2009). A specific role for posterior dorsolateral striatum in human habit learning. *European Journal of Neuroscience*, 29(11), 2225-2232.

49. de Wit, S., et al. (2018). Shifting the balance between goals and habits: Five failures in experimental habit induction. *Journal of Experimental Psychology: General*, 147(7), 1043-1065. DOI: 10.1037/xge0000402

50. Kappes, H. B. & Oettingen, G. (2011). Positive fantasies about idealized futures sap energy. *Journal of Experimental Social Psychology*, 47(4), 719-729.

51. Sevincer, A. T., Busatta, P. D., & Oettingen, G. (2014). Mental contrasting and transfer of energization. *Personality and Social Psychology Bulletin*, 40(2), 139-152. DOI: 10.1177/0146167213507088. PMID: 24145296

52. Schwarz, N. & Clore, G. L. (1983). Mood, misattribution, and judgments of well-being. *Journal of Personality and Social Psychology*, 45(3), 513-523.

53. Schwarz, N. (2012). Feelings-as-information theory. In *Handbook of theories of social psychology* (pp. 289-308). Sage.

54. Ekkekakis, P. (2009). The dual-mode theory of affective responses to exercise in metatheoretical context. *International Review of Sport and Exercise Psychology*, 2(1-2), 73-94 and 119-150.

55. Williams, D. M. (2008). Exercise, affect, and adherence: An integrated model and a case for self-paced exercise. *Journal of Sport and Exercise Psychology*, 30(5), 471-496. DOI: 10.1123/jsep.30.5.471

56. Brand, R. & Ekkekakis, P. (2018). Affective-reflective theory of physical inactivity and exercise. *German Journal of Exercise and Sport Research*, 48, 48-58.

57. Stevens, C. J., et al. (2020). Affective determinants of physical activity: A conceptual framework and narrative review. *Frontiers in Psychology*, 11, 568331. DOI: 10.3389/fpsyg.2020.568331

58. Kuppens, P., Allen, N. B., & Sheeber, L. B. (2010). Emotional inertia and psychological maladjustment. *Psychological Science*, 21(7), 984-991.

59. Kuppens, P., Oravecz, Z., & Tuerlinckx, F. (2010). Feelings change: Accounting for individual differences in the temporal dynamics of affect. *Journal of Personality and Social Psychology*, 99(6), 1042-1060.

60. Bringmann, L. F., et al. (2016). Assessing temporal emotion dynamics using networks. *Assessment*, 23(4), 425-435.

61. Russell, J. A. (1980). A circumplex model of affect. *Journal of Personality and Social Psychology*, 39(6), 1161-1178.

62. Oettingen, G. (2012). Future thought and behaviour change. *European Review of Social Psychology*, 23(1), 1-63.

63. Oettingen, G. & Reininger, K. M. (2016). The power of prospection: Mental contrasting and behavior change. *Social and Personality Psychology Compass*, 10(11), 591-604.

64. Gollwitzer, P. M. (1999). Implementation intentions: Strong effects of simple plans. *American Psychologist*, 54(7), 493-503.

65. Gollwitzer, P. M. & Sheeran, P. (2006). Implementation intentions and goal achievement: A meta-analysis. *Advances in Experimental Social Psychology*, 38, 69-119.

66. Wang, G., Wang, Y., & Gai, X. (2021). A meta-analysis of the effects of mental contrasting with implementation intentions on goal attainment. *Frontiers in Psychology*, 12, 565202. DOI: 10.3389/fpsyg.2021.565202

67. Duckworth, A. L., et al. (2011). Self-regulation strategies improve self-discipline in adolescents. *Educational Psychology*, 31(1), 17-26.

68. Stadler, G., Oettingen, G., & Gollwitzer, P. M. (2009). Physical activity in women: Effects of a self-regulation intervention. *American Journal of Preventive Medicine*, 36(1), 29-34.

69. Kwasnicka, D., Dombrowski, S. U., White, M., & Sniehotta, F. (2016). Theoretical explanations for maintenance of behaviour change. *Health Psychology Review*, 10(3), 277-296.
