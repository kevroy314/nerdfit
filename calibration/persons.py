"""
Person backstory descriptors for synthetic calibration.

Each person is defined by demographics, life context, and derived event rate
modifiers that bias the Poisson processes for event generation.

Design principles:
- Cover a range of ages (18-70), genders, fitness goals, career types
- Life stressor profiles vary from stable to chaotic
- Motivation sources vary (intrinsic, health-driven, social, appearance)
- Starting conditions (H, M, E, I) derived from backstory, not arbitrary
"""

PERSONS = [
    # === YOUNG ADULTS (18-30) ===
    {
        "id": "sarah_23_grad",
        "name": "Sarah",
        "age": 23,
        "gender": "F",
        "occupation": "Graduate student (biology)",
        "fitness_goal": "Start running to manage anxiety",
        "motivation_source": "intrinsic_wellbeing",
        "backstory": "PhD student with irregular schedule. Anxiety has been building. Therapist suggested exercise. Has never been athletic but is intellectually convinced it will help. Lives alone in a studio apartment near campus.",
        "life_stability": 0.5,  # Moderate: academic stress, flexible but chaotic schedule
        "social_support": 0.3,  # Low: new city, few close friends
        "prior_fitness": 0.1,   # Very low: never exercised regularly
        "complexity_target": 0.3,  # Low: just wants to run 3x/week
        "initial": {"H": 0.02, "M": 0.6, "E": 0.3, "I": 0.0},
        "event_rates": {
            "stress_base": 0.08,      # ~3/month
            "shock_positive_base": 0.02,
            "social_base": 0.01,
            "context_disruption_base": 0.005,  # Academic transitions
            "lapse_vulnerability": 0.6,  # Moderate-high: no habit buffer
            "injury_base": 0.002,
        },
    },
    {
        "id": "marcus_26_tech",
        "name": "Marcus",
        "age": 26,
        "gender": "M",
        "occupation": "Software engineer at startup",
        "fitness_goal": "Get back to lifting after college",
        "motivation_source": "appearance_social",
        "backstory": "Lifted in college but stopped after starting his job. 60-hour weeks, Uber Eats for dinner. A college friend's wedding photos shocked him. Has gym knowledge but zero current habit.",
        "life_stability": 0.4,  # Startup chaos, long hours
        "social_support": 0.5,  # Some gym-going friends from college
        "prior_fitness": 0.4,   # Used to be fit, muscle memory exists
        "complexity_target": 0.7,  # High: wants a real lifting program
        "initial": {"H": 0.05, "M": 1.2, "E": 0.8, "I": 0.1},
        "event_rates": {
            "stress_base": 0.1,       # High: startup culture
            "shock_positive_base": 0.03,
            "social_base": 0.03,
            "context_disruption_base": 0.003,
            "lapse_vulnerability": 0.5,
            "injury_base": 0.004,     # Higher: lifting injuries
        },
    },
    {
        "id": "priya_21_college",
        "name": "Priya",
        "age": 21,
        "gender": "F",
        "occupation": "College senior (pre-med)",
        "fitness_goal": "Lose weight for health and confidence",
        "motivation_source": "health_appearance",
        "backstory": "Family history of diabetes. Pre-med courses are brutal. Eats in the dining hall -- limited control over food quality. Has tried and failed to diet three times in the past two years. Each attempt lasted 2-4 weeks.",
        "life_stability": 0.6,  # Structured semester but exam stress
        "social_support": 0.5,  # Roommates, campus community
        "prior_fitness": 0.15,  # Some attempts, nothing stuck
        "complexity_target": 0.6,  # Moderate-high: diet + exercise
        "initial": {"H": 0.03, "M": 0.9, "E": 0.6, "I": 0.0},
        "event_rates": {
            "stress_base": 0.09,      # Exam cycles
            "shock_positive_base": 0.025,
            "social_base": 0.04,
            "context_disruption_base": 0.008,  # Semester breaks disrupt
            "lapse_vulnerability": 0.7,  # High: diet lapses are common
            "injury_base": 0.001,
        },
    },
    {
        "id": "jordan_28_trades",
        "name": "Jordan",
        "age": 28,
        "gender": "NB",
        "occupation": "Electrician",
        "fitness_goal": "Build strength for physically demanding job",
        "motivation_source": "functional_performance",
        "backstory": "Physically active at work but it's not 'exercise' -- repetitive, asymmetric loading. Back pain starting. Union has a gym benefit but hasn't used it. Partner is supportive. Shift work (early mornings).",
        "life_stability": 0.7,  # Stable job, stable relationship
        "social_support": 0.6,  # Partner, coworkers
        "prior_fitness": 0.3,   # Physically active but not structured
        "complexity_target": 0.4,  # Moderate: strength training basics
        "initial": {"H": 0.08, "M": 0.7, "E": 0.2, "I": 0.05},
        "event_rates": {
            "stress_base": 0.04,
            "shock_positive_base": 0.02,
            "social_base": 0.03,
            "context_disruption_base": 0.002,
            "lapse_vulnerability": 0.4,
            "injury_base": 0.008,     # High: physical job + lifting
        },
    },

    # === MIDDLE ADULTS (30-45) ===
    {
        "id": "david_35_newdad",
        "name": "David",
        "age": 35,
        "gender": "M",
        "occupation": "Marketing manager",
        "fitness_goal": "Lose 30lbs, 'get healthy for the kids'",
        "motivation_source": "health_family",
        "backstory": "Two kids under 5. Used to play rec soccer. Sleep-deprived, stress-eating. Wife exercises regularly which creates both inspiration and guilt. Doctor mentioned borderline cholesterol at last checkup.",
        "life_stability": 0.5,  # Stable job but chaotic home life
        "social_support": 0.6,  # Wife, some dad friends
        "prior_fitness": 0.35,  # Athletic past, gone now
        "complexity_target": 0.5,  # Moderate
        "initial": {"H": 0.03, "M": 0.8, "E": 0.5, "I": 0.05},
        "event_rates": {
            "stress_base": 0.1,       # Young kids = constant stress
            "shock_positive_base": 0.02,
            "social_base": 0.02,
            "context_disruption_base": 0.006,  # Kid illnesses, daycare changes
            "lapse_vulnerability": 0.6,
            "injury_base": 0.003,
        },
    },
    {
        "id": "mei_38_executive",
        "name": "Mei",
        "age": 38,
        "gender": "F",
        "occupation": "VP of Operations at mid-size company",
        "fitness_goal": "Run a half marathon, manage cortisol",
        "motivation_source": "performance_stress_management",
        "backstory": "High-powered career, travel 30% of the time. Has a personal trainer she sees when she's in town. The inconsistency drives her crazy. Recently read about cortisol and exercise. Very goal-oriented, tends to overcomplicate.",
        "life_stability": 0.4,  # Travel disrupts everything
        "social_support": 0.4,  # Trainer, but no consistent social circle for fitness
        "prior_fitness": 0.4,   # Sporadic but informed
        "complexity_target": 0.8,  # High: half marathon training plan
        "initial": {"H": 0.15, "M": 1.5, "E": 1.0, "I": 0.1},
        "event_rates": {
            "stress_base": 0.12,      # Very high: executive role
            "shock_positive_base": 0.03,
            "social_base": 0.02,
            "context_disruption_base": 0.04,   # Travel = constant context disruption
            "lapse_vulnerability": 0.5,
            "injury_base": 0.005,     # Running injury risk
        },
    },
    {
        "id": "carlos_42_teacher",
        "name": "Carlos",
        "age": 42,
        "gender": "M",
        "occupation": "High school teacher and coach",
        "fitness_goal": "Stay fit enough to keep coaching track",
        "motivation_source": "identity_role",
        "backstory": "Was a competitive runner in his 20s. Still identifies as a runner. Coaches the high school track team. Knee has been bothering him. Wife wants him to 'slow down.' Running identity is core to who he is.",
        "life_stability": 0.7,  # Stable career, stable family
        "social_support": 0.7,  # Students, running community
        "prior_fitness": 0.7,   # Long history, current maintenance
        "complexity_target": 0.5,  # Moderate: adapted training
        "initial": {"H": 0.65, "M": 0.4, "E": -0.2, "I": 0.7},
        "event_rates": {
            "stress_base": 0.05,
            "shock_positive_base": 0.02,
            "social_base": 0.05,
            "context_disruption_base": 0.003,
            "lapse_vulnerability": 0.25,  # Low: strong identity buffer
            "injury_base": 0.012,     # High: aging runner with knee issues
        },
    },
    {
        "id": "aisha_33_nurse",
        "name": "Aisha",
        "age": 33,
        "gender": "F",
        "occupation": "ICU nurse, night shift",
        "fitness_goal": "Any consistent exercise to fight shift work fatigue",
        "motivation_source": "health_energy",
        "backstory": "12-hour night shifts, 3 days on, 4 off. Circadian rhythm is destroyed. Knows exercise would help her energy but the schedule makes it nearly impossible. Single, lives with a cat. Ironic: she counsels patients on lifestyle change daily.",
        "life_stability": 0.3,  # Shift work is inherently destabilizing
        "social_support": 0.3,  # Isolated by schedule
        "prior_fitness": 0.2,   # Walks sometimes on days off
        "complexity_target": 0.3,  # Low: anything consistent
        "initial": {"H": 0.02, "M": 0.5, "E": 0.2, "I": 0.0},
        "event_rates": {
            "stress_base": 0.15,      # Very high: ICU nursing
            "shock_positive_base": 0.015,
            "social_base": 0.01,
            "context_disruption_base": 0.02,   # Schedule rotations
            "lapse_vulnerability": 0.7,
            "injury_base": 0.002,
        },
    },
    {
        "id": "tom_40_remote",
        "name": "Tom",
        "age": 40,
        "gender": "M",
        "occupation": "Remote freelance writer",
        "fitness_goal": "Break sedentary cycle, reduce back pain",
        "motivation_source": "pain_avoidance",
        "backstory": "Works from home, alone, for 5 years. Hasn't exercised in a decade. Back pain from sitting all day. Gained 40lbs since going remote. No commute means no incidental movement. Highly introverted -- group fitness is a non-starter.",
        "life_stability": 0.6,  # Stable but monotonous
        "social_support": 0.1,  # Very isolated
        "prior_fitness": 0.05,  # Essentially zero
        "complexity_target": 0.2,  # Very low: just move
        "initial": {"H": 0.02, "M": 0.4, "E": 0.1, "I": 0.0},
        "event_rates": {
            "stress_base": 0.04,      # Low external stress
            "shock_positive_base": 0.01,
            "social_base": 0.005,     # Very rare social fitness events
            "context_disruption_base": 0.001,
            "lapse_vulnerability": 0.5,
            "injury_base": 0.002,
        },
    },
    {
        "id": "lisa_37_divorce",
        "name": "Lisa",
        "age": 37,
        "gender": "F",
        "occupation": "Accountant",
        "fitness_goal": "Reinvent herself post-divorce",
        "motivation_source": "identity_transformation",
        "backstory": "Recently divorced after 12 years. Two kids (8, 11) with shared custody. Using fitness as a way to reclaim her identity. Signed up for a CrossFit intro. The community aspect is as important as the exercise. High initial motivation but fragile.",
        "life_stability": 0.3,  # Divorce upheaval
        "social_support": 0.5,  # CrossFit community, a few close friends
        "prior_fitness": 0.15,  # Minimal
        "complexity_target": 0.7,  # High: CrossFit is complex
        "initial": {"H": 0.02, "M": 1.8, "E": 1.2, "I": 0.0},
        "event_rates": {
            "stress_base": 0.14,      # Very high: divorce + single parenting
            "shock_positive_base": 0.04,  # Transformation energy
            "social_base": 0.06,      # CrossFit community
            "context_disruption_base": 0.01,  # Custody schedule changes
            "lapse_vulnerability": 0.65,
            "injury_base": 0.006,     # CrossFit injury risk
        },
    },

    # === MIDDLE-OLDER ADULTS (45-60) ===
    {
        "id": "robert_52_exec",
        "name": "Robert",
        "age": 52,
        "gender": "M",
        "occupation": "CFO, publicly traded company",
        "fitness_goal": "Cardiac health after father's heart attack",
        "motivation_source": "health_fear",
        "backstory": "Father had a heart attack at 55. Robert is now 52 with borderline hypertension. Has resources (home gym, can hire trainer) but zero time and massive work stress. Travels internationally. Wife nags him about health.",
        "life_stability": 0.4,  # High stress, high resources
        "social_support": 0.4,  # Wife cares but he resists
        "prior_fitness": 0.2,   # Played golf, occasional walks
        "complexity_target": 0.4,  # Moderate: cardio + basic strength
        "initial": {"H": 0.02, "M": 1.4, "E": 0.8, "I": 0.0},
        "event_rates": {
            "stress_base": 0.13,
            "shock_positive_base": 0.02,
            "social_base": 0.02,
            "context_disruption_base": 0.03,  # Travel
            "lapse_vulnerability": 0.6,
            "injury_base": 0.004,
        },
    },
    {
        "id": "gloria_48_teacher",
        "name": "Gloria",
        "age": 48,
        "gender": "F",
        "occupation": "Elementary school teacher",
        "fitness_goal": "Manage menopause symptoms through exercise",
        "motivation_source": "symptom_management",
        "backstory": "Perimenopause hit hard -- weight gain, sleep disruption, mood swings. Doctor recommended exercise before HRT. Has a structured daily schedule (school hours). Husband exercises regularly. Empty nester (kids in college).",
        "life_stability": 0.7,  # Very stable external life
        "social_support": 0.7,  # Husband, teacher friends
        "prior_fitness": 0.25,  # Some yoga classes over the years
        "complexity_target": 0.4,  # Moderate: mixed cardio/strength
        "initial": {"H": 0.05, "M": 0.9, "E": 0.3, "I": 0.05},
        "event_rates": {
            "stress_base": 0.04,
            "shock_positive_base": 0.025,
            "social_base": 0.04,
            "context_disruption_base": 0.004,  # Summer break changes routine
            "lapse_vulnerability": 0.4,
            "injury_base": 0.003,
        },
    },
    {
        "id": "james_55_bluecollar",
        "name": "James",
        "age": 55,
        "gender": "M",
        "occupation": "Warehouse supervisor",
        "fitness_goal": "Lose weight, doc says knees won't last",
        "motivation_source": "health_ultimatum",
        "backstory": "BMI 35. Knees are shot from decades of warehouse work. Doctor said 'lose weight or prepare for knee replacement by 60.' Smokes a pack a day. Wife cooks southern food. Skeptical of 'gym culture.' Limited health literacy.",
        "life_stability": 0.6,
        "social_support": 0.3,  # Wife enables, coworkers don't exercise
        "prior_fitness": 0.05,
        "complexity_target": 0.3,  # Low: walking and basic diet change
        "initial": {"H": 0.02, "M": 0.6, "E": 0.4, "I": 0.0},
        "event_rates": {
            "stress_base": 0.06,
            "shock_positive_base": 0.015,
            "social_base": 0.005,
            "context_disruption_base": 0.002,
            "lapse_vulnerability": 0.8,  # Very high: diet change in enabling environment
            "injury_base": 0.01,      # High: bad knees, heavy
        },
    },
    {
        "id": "nina_44_immigrant",
        "name": "Nina",
        "age": 44,
        "gender": "F",
        "occupation": "Restaurant owner",
        "fitness_goal": "Energy and stress relief",
        "motivation_source": "energy_stress",
        "backstory": "Immigrated 15 years ago, built a restaurant from scratch. Works 14-hour days. Type 2 diabetes diagnosed last year. Daughter (16) is worried about her. No time, no energy, but the diagnosis scared her. Culturally, 'exercise for exercise's sake' feels foreign.",
        "life_stability": 0.3,  # Restaurant = constant crisis
        "social_support": 0.4,  # Daughter, a few close friends
        "prior_fitness": 0.05,
        "complexity_target": 0.2,  # Very low: walking after dinner
        "initial": {"H": 0.02, "M": 0.7, "E": 0.5, "I": 0.0},
        "event_rates": {
            "stress_base": 0.12,
            "shock_positive_base": 0.02,
            "social_base": 0.02,
            "context_disruption_base": 0.008,  # Restaurant crises
            "lapse_vulnerability": 0.7,
            "injury_base": 0.002,
        },
    },

    # === OLDER ADULTS (60+) ===
    {
        "id": "helen_62_retired",
        "name": "Helen",
        "age": 62,
        "gender": "F",
        "occupation": "Retired teacher, part-time tutor",
        "fitness_goal": "Maintain independence, prevent falls",
        "motivation_source": "independence_longevity",
        "backstory": "Recently retired. Watched her mother decline physically in her 70s and is determined to avoid the same fate. Plenty of time. Joined a Silver Sneakers class at the community center. Widowed 3 years ago.",
        "life_stability": 0.8,
        "social_support": 0.6,  # Silver Sneakers group, church friends
        "prior_fitness": 0.2,
        "complexity_target": 0.3,
        "initial": {"H": 0.02, "M": 0.8, "E": 0.2, "I": 0.0},
        "event_rates": {
            "stress_base": 0.02,
            "shock_positive_base": 0.02,
            "social_base": 0.05,      # High: community classes
            "context_disruption_base": 0.003,
            "lapse_vulnerability": 0.3,
            "injury_base": 0.008,     # Higher: age-related
        },
    },
    {
        "id": "frank_67_cardiac",
        "name": "Frank",
        "age": 67,
        "gender": "M",
        "occupation": "Retired engineer",
        "fitness_goal": "Cardiac rehab after mild heart attack",
        "motivation_source": "health_survival",
        "backstory": "Mild MI six months ago. Completed cardiac rehab. Now on his own. Wife is terrified and monitors everything he eats. Has the knowledge and the motivation but the fear of another event creates anxiety around exertion.",
        "life_stability": 0.7,
        "social_support": 0.7,  # Wife (overprotective), cardiac rehab alumni group
        "prior_fitness": 0.3,   # Cardiac rehab gave him a base
        "complexity_target": 0.3,
        "initial": {"H": 0.2, "M": 1.0, "E": 0.3, "I": 0.1},
        "event_rates": {
            "stress_base": 0.03,
            "shock_positive_base": 0.03,  # Regular checkups provide feedback
            "social_base": 0.04,
            "context_disruption_base": 0.002,
            "lapse_vulnerability": 0.35,
            "injury_base": 0.006,
        },
    },

    # === SPECIAL POPULATIONS ===
    {
        "id": "alex_30_adhd",
        "name": "Alex",
        "age": 30,
        "gender": "M",
        "occupation": "Graphic designer (freelance)",
        "fitness_goal": "Use exercise to manage ADHD without meds",
        "motivation_source": "cognitive_function",
        "backstory": "Diagnosed ADHD at 25. Medication helped but side effects were bad. Read that exercise can substitute for some of the dopamine regulation. Hyperfocuses on new things then drops them. Has started and stopped at least 8 different exercise programs. Knows the pattern but can't break it.",
        "life_stability": 0.4,  # Freelance income variability
        "social_support": 0.3,  # Mostly online friends
        "prior_fitness": 0.2,   # Bursts of intense activity, never sustained
        "complexity_target": 0.5,
        "initial": {"H": 0.05, "M": 1.6, "E": 0.9, "I": 0.0},
        "event_rates": {
            "stress_base": 0.08,
            "shock_positive_base": 0.06,  # High: novelty-seeking creates many 'fresh starts'
            "social_base": 0.02,
            "context_disruption_base": 0.005,
            "lapse_vulnerability": 0.8,   # Very high: ADHD executive function
            "injury_base": 0.003,
        },
    },
    {
        "id": "keiko_29_postpartum",
        "name": "Keiko",
        "age": 29,
        "gender": "F",
        "occupation": "UX researcher (on parental leave)",
        "fitness_goal": "Postpartum recovery and mental health",
        "motivation_source": "recovery_wellbeing",
        "backstory": "Baby is 4 months old. Dealing with postpartum mood issues. Was a regular yoga practitioner before pregnancy. Body feels alien. Sleep deprivation is profound. Partner is supportive but also exhausted. Cleared for exercise by OB.",
        "life_stability": 0.3,  # New baby chaos
        "social_support": 0.6,  # Partner, mom group, former yoga friends
        "prior_fitness": 0.4,   # Was consistent before pregnancy
        "complexity_target": 0.3,  # Low: rebuild slowly
        "initial": {"H": 0.1, "M": 0.6, "E": 0.3, "I": 0.15},
        "event_rates": {
            "stress_base": 0.12,      # Baby = constant
            "shock_positive_base": 0.025,
            "social_base": 0.04,      # Mom groups
            "context_disruption_base": 0.015,  # Baby milestones change everything
            "lapse_vulnerability": 0.6,
            "injury_base": 0.003,
        },
    },
    {
        "id": "derek_45_yoyo",
        "name": "Derek",
        "age": 45,
        "gender": "M",
        "occupation": "Sales director",
        "fitness_goal": "Lose weight (again) -- 5th serious attempt",
        "motivation_source": "repeated_shame",
        "backstory": "Classic yo-yo dieter. Has lost 30+ lbs four times, gained it back each time. Knows every diet. Currently at his heaviest (265lbs at 5'10\"). Each cycle is harder. Cynical but desperate. Wife has stopped commenting, which feels worse than nagging.",
        "life_stability": 0.5,
        "social_support": 0.3,  # Wife has given up, colleagues don't know
        "prior_fitness": 0.15,  # Temporary fitness, never maintained
        "complexity_target": 0.6,  # Moderate-high: still overcomplicates
        "initial": {"H": 0.03, "M": 0.5, "E": -0.5, "I": 0.0},  # Negative E: learned helplessness
        "event_rates": {
            "stress_base": 0.09,
            "shock_positive_base": 0.03,  # Something always sparks another attempt
            "social_base": 0.01,
            "context_disruption_base": 0.005,
            "lapse_vulnerability": 0.85,  # Very high: established failure pattern
            "injury_base": 0.003,
        },
    },
    {
        "id": "sam_19_freshman",
        "name": "Sam",
        "age": 19,
        "gender": "M",
        "occupation": "College freshman (undeclared)",
        "fitness_goal": "Get big, impress people",
        "motivation_source": "appearance_social_status",
        "backstory": "Skinny kid who watched too many fitness YouTubers. First month of college, signed up for the campus gym. Has a 6-day PPL split from Reddit. No actual training experience. Expects visible results in 4 weeks. Very high motivation, very high expectations, zero patience.",
        "life_stability": 0.5,  # New environment but structured
        "social_support": 0.5,  # Dorm friends, some gym bros
        "prior_fitness": 0.05,
        "complexity_target": 0.9,  # Way too high for a beginner
        "initial": {"H": 0.02, "M": 2.0, "E": 2.0, "I": 0.0},  # Very high M and E
        "event_rates": {
            "stress_base": 0.07,
            "shock_positive_base": 0.04,
            "social_base": 0.05,
            "context_disruption_base": 0.01,  # Semester breaks
            "lapse_vulnerability": 0.7,
            "injury_base": 0.006,     # Ego lifting
        },
    },
    {
        "id": "maria_50_caregiver",
        "name": "Maria",
        "age": 50,
        "gender": "F",
        "occupation": "Office manager + caregiver for elderly mother",
        "fitness_goal": "Strength to physically assist mother, personal stress relief",
        "motivation_source": "functional_caregiving",
        "backstory": "Mother moved in after a stroke 2 years ago. Maria does all the transfers, bathing assistance, appointments. Her own health is declining from the physical and emotional toll. A home health aide comes 3x/week, giving her small windows of free time.",
        "life_stability": 0.3,  # Caregiving is unpredictable
        "social_support": 0.3,  # Isolated by caregiving duties
        "prior_fitness": 0.1,
        "complexity_target": 0.25,  # Very low: anything she can fit in
        "initial": {"H": 0.02, "M": 0.5, "E": 0.2, "I": 0.0},
        "event_rates": {
            "stress_base": 0.15,      # Extreme: caregiving
            "shock_positive_base": 0.01,
            "social_base": 0.01,
            "context_disruption_base": 0.02,   # Mother's health crises
            "lapse_vulnerability": 0.7,
            "injury_base": 0.005,     # Back strain from caregiving
        },
    },
]
