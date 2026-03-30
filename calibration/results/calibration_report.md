# Synthetic Narrative Calibration Report
Total simulations: 2100
Persons: 21, Streams per person: 100
Simulation period: 730 days (2 years)

## Methodology

1. **Person backstories**: 20 diverse individuals with varying demographics,
   fitness goals, life stressors, and prior fitness levels.
2. **Archetype-weighted generation**: Each person has a probability distribution
   over 10 trajectory archetypes (STEADY_BUILDER, FALSE_STARTER, etc.).
3. **Event streams**: Generated via inhomogeneous Poisson processes with rates
   biased by person backstory and archetype. Includes seasonal effects,
   autoregressive stress clustering, and conditional lapse generation.
4. **Validation**: Each stream checked for plausibility (event counts, temporal
   spread, injury/heal balance).
5. **Calibration targets**: Derived from Oscarsson 2020, Norcross 2002,
   Kwasnicka 2016, Lally 2010.

## Overall Results vs Literature Targets

| Metric | Observed | Target | Status |
|--------|----------|--------|--------|
| habit_formed | 33.0% | 15-30% | HIGH |
| partial_habit | 32.4% | 10-25% | HIGH |
| sedentary | 15.8% | 25-45% | LOW |
| dropout | 10.0% | 10-25% | OK |
| false_hope_cycle | 8.7% | 3-15% | OK |
| Dropped by d60 | 63.4% | 50-80% | OK |
| Active at d180 | 39.9% | 25-50% | OK |
| Active at d365 | 69.9% | 15-35% | MISS |

## Per-Person Results

### Gloria (gloria_48_teacher)
- C=0.4, Habit formed: 72%
- Active@180d: 76%, Active@365d: 84%
- Avg H_final: 0.62, Avg I_final: 0.62
- Outcomes: {'partial_habit': 18, 'habit_formed': 72, 'false_hope_cycle': 2, 'sedentary': 8}
- Best archetype: INDULGENCE_FADE (100% success)
- Worst archetype: INJURY_DERAILED (36% success)

### Frank (frank_67_cardiac)
- C=0.3, Habit formed: 68%
- Active@180d: 71%, Active@365d: 80%
- Avg H_final: 0.63, Avg I_final: 0.61
- Outcomes: {'habit_formed': 68, 'partial_habit': 23, 'sedentary': 5, 'false_hope_cycle': 4}
- Best archetype: LATE_BLOOMER (100% success)
- Worst archetype: INJURY_DERAILED (22% success)

### Tom (tom_40_remote)
- C=0.2, Habit formed: 66%
- Active@180d: 66%, Active@365d: 88%
- Avg H_final: 0.59, Avg I_final: 0.58
- Outcomes: {'partial_habit': 28, 'habit_formed': 66, 'false_hope_cycle': 5, 'sedentary': 1}
- Best archetype: SOCIAL_CATALYZED (100% success)
- Worst archetype: YO_YO (0% success)

### Helen (helen_62_retired)
- C=0.3, Habit formed: 59%
- Active@180d: 67%, Active@365d: 74%
- Avg H_final: 0.57, Avg I_final: 0.54
- Outcomes: {'habit_formed': 59, 'partial_habit': 33, 'false_hope_cycle': 5, 'sedentary': 2, 'dropout': 1}
- Best archetype: FALSE_STARTER (100% success)
- Worst archetype: INJURY_DERAILED (15% success)

### Jordan (jordan_28_trades)
- C=0.4, Habit formed: 56%
- Active@180d: 59%, Active@365d: 73%
- Avg H_final: 0.55, Avg I_final: 0.53
- Outcomes: {'partial_habit': 31, 'false_hope_cycle': 7, 'habit_formed': 56, 'sedentary': 6}
- Best archetype: INDULGENCE_FADE (83% success)
- Worst archetype: CRISIS_INTERRUPTED (0% success)

### Keiko (keiko_29_postpartum)
- C=0.3, Habit formed: 47%
- Active@180d: 67%, Active@365d: 86%
- Avg H_final: 0.51, Avg I_final: 0.51
- Outcomes: {'habit_formed': 47, 'partial_habit': 39, 'false_hope_cycle': 11, 'sedentary': 3}
- Best archetype: SLOW_GRINDER (100% success)
- Worst archetype: YO_YO (0% success)

### Sarah (sarah_23_grad)
- C=0.3, Habit formed: 46%
- Active@180d: 68%, Active@365d: 87%
- Avg H_final: 0.51, Avg I_final: 0.51
- Outcomes: {'habit_formed': 46, 'partial_habit': 46, 'sedentary': 4, 'false_hope_cycle': 3, 'dropout': 1}
- Best archetype: STEADY_BUILDER (77% success)
- Worst archetype: INJURY_DERAILED (0% success)

### Priya (priya_21_college)
- C=0.6, Habit formed: 46%
- Active@180d: 24%, Active@365d: 77%
- Avg H_final: 0.45, Avg I_final: 0.31
- Outcomes: {'habit_formed': 46, 'partial_habit': 23, 'dropout': 7, 'false_hope_cycle': 2, 'sedentary': 22}
- Best archetype: SOCIAL_CATALYZED (79% success)
- Worst archetype: FALSE_STARTER (0% success)

### David (david_35_newdad)
- C=0.5, Habit formed: 35%
- Active@180d: 28%, Active@365d: 71%
- Avg H_final: 0.43, Avg I_final: 0.33
- Outcomes: {'sedentary': 8, 'partial_habit': 46, 'habit_formed': 35, 'false_hope_cycle': 6, 'dropout': 5}
- Best archetype: SOCIAL_CATALYZED (85% success)
- Worst archetype: FALSE_STARTER (0% success)

### Carlos (carlos_42_teacher)
- C=0.5, Habit formed: 35%
- Active@180d: 49%, Active@365d: 51%
- Avg H_final: 0.44, Avg I_final: 0.61
- Outcomes: {'false_hope_cycle': 15, 'habit_formed': 35, 'partial_habit': 30, 'sedentary': 14, 'dropout': 6}
- Best archetype: STEADY_BUILDER (62% success)
- Worst archetype: INDULGENCE_FADE (0% success)

### Nina (nina_44_immigrant)
- C=0.2, Habit formed: 33%
- Active@180d: 63%, Active@365d: 87%
- Avg H_final: 0.45, Avg I_final: 0.44
- Outcomes: {'partial_habit': 51, 'habit_formed': 33, 'sedentary': 8, 'false_hope_cycle': 8}
- Best archetype: STEADY_BUILDER (81% success)
- Worst archetype: INJURY_DERAILED (0% success)

### Marcus (marcus_26_tech)
- C=0.7, Habit formed: 24%
- Active@180d: 12%, Active@365d: 54%
- Avg H_final: 0.32, Avg I_final: 0.20
- Outcomes: {'habit_formed': 24, 'partial_habit': 20, 'false_hope_cycle': 4, 'sedentary': 32, 'dropout': 20}
- Best archetype: STEADY_BUILDER (62% success)
- Worst archetype: CRISIS_INTERRUPTED (0% success)

### James (james_55_bluecollar)
- C=0.3, Habit formed: 22%
- Active@180d: 32%, Active@365d: 52%
- Avg H_final: 0.40, Avg I_final: 0.31
- Outcomes: {'habit_formed': 22, 'partial_habit': 50, 'sedentary': 6, 'false_hope_cycle': 19, 'dropout': 3}
- Best archetype: SOCIAL_CATALYZED (57% success)
- Worst archetype: CRISIS_INTERRUPTED (0% success)

### Aisha (aisha_33_nurse)
- C=0.3, Habit formed: 21%
- Active@180d: 42%, Active@365d: 84%
- Avg H_final: 0.37, Avg I_final: 0.29
- Outcomes: {'habit_formed': 21, 'partial_habit': 53, 'sedentary': 11, 'false_hope_cycle': 12, 'dropout': 3}
- Best archetype: STEADY_BUILDER (58% success)
- Worst archetype: CRISIS_INTERRUPTED (0% success)

### Robert (robert_52_exec)
- C=0.4, Habit formed: 19%
- Active@180d: 28%, Active@365d: 77%
- Avg H_final: 0.31, Avg I_final: 0.25
- Outcomes: {'sedentary': 17, 'partial_habit': 39, 'habit_formed': 19, 'false_hope_cycle': 16, 'dropout': 9}
- Best archetype: SOCIAL_CATALYZED (57% success)
- Worst archetype: LATE_BLOOMER (0% success)

### Derek (derek_45_yoyo)
- C=0.6, Habit formed: 13%
- Active@180d: 8%, Active@365d: 55%
- Avg H_final: 0.24, Avg I_final: 0.13
- Outcomes: {'partial_habit': 22, 'sedentary': 29, 'habit_formed': 13, 'dropout': 26, 'false_hope_cycle': 10}
- Best archetype: SOCIAL_CATALYZED (50% success)
- Worst archetype: LATE_BLOOMER (0% success)

### Alex (alex_30_adhd)
- C=0.5, Habit formed: 12%
- Active@180d: 32%, Active@365d: 83%
- Avg H_final: 0.31, Avg I_final: 0.18
- Outcomes: {'habit_formed': 12, 'partial_habit': 43, 'sedentary': 34, 'false_hope_cycle': 7, 'dropout': 4}
- Best archetype: STEADY_BUILDER (58% success)
- Worst archetype: LATE_BLOOMER (0% success)

### Maria (maria_50_caregiver)
- C=0.25, Habit formed: 11%
- Active@180d: 28%, Active@365d: 64%
- Avg H_final: 0.28, Avg I_final: 0.24
- Outcomes: {'habit_formed': 11, 'sedentary': 9, 'partial_habit': 44, 'false_hope_cycle': 34, 'dropout': 2}
- Best archetype: SOCIAL_CATALYZED (50% success)
- Worst archetype: LATE_BLOOMER (0% success)

### Lisa (lisa_37_divorce)
- C=0.7, Habit formed: 6%
- Active@180d: 10%, Active@365d: 47%
- Avg H_final: 0.20, Avg I_final: 0.09
- Outcomes: {'sedentary': 38, 'dropout': 28, 'partial_habit': 22, 'habit_formed': 6, 'false_hope_cycle': 6}
- Best archetype: SOCIAL_CATALYZED (27% success)
- Worst archetype: LATE_BLOOMER (0% success)

### Sam (sam_19_freshman)
- C=0.9, Habit formed: 2%
- Active@180d: 6%, Active@365d: 50%
- Avg H_final: 0.13, Avg I_final: 0.03
- Outcomes: {'sedentary': 55, 'dropout': 34, 'habit_formed': 2, 'partial_habit': 7, 'false_hope_cycle': 2}
- Best archetype: SOCIAL_CATALYZED (12% success)
- Worst archetype: LATE_BLOOMER (0% success)

### Mei (mei_38_executive)
- C=0.8, Habit formed: 1%
- Active@180d: 1%, Active@365d: 43%
- Avg H_final: 0.11, Avg I_final: 0.08
- Outcomes: {'dropout': 62, 'partial_habit': 13, 'sedentary': 20, 'false_hope_cycle': 4, 'habit_formed': 1}
- Best archetype: STEADY_BUILDER (8% success)
- Worst archetype: SOCIAL_CATALYZED (0% success)

