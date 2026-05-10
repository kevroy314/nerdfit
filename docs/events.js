/**
 * Event catalog: narrative descriptions and amplitude mappings
 * for each event type at each strength level (1-5).
 *
 * Each event type maps strength (1-5) to:
 *   - amplitude: the dynamical parameter passed to the engine
 *   - label: short label for the trajectory annotation
 *   - narrative: a plausible real-world scenario at that intensity
 */

const EVENT_CATALOG = {
  shock: {
    name: "Motivational Shock",
    description: "An external event that suddenly boosts motivation.",
    levels: {
      1: {
        amplitude: 0.3,
        label: "Saw a motivating post online",
        narrative: "A friend posted their 5K finish on social media. Brief pang of 'I should do that too.' Gone by tomorrow, but plants a seed.",
      },
      2: {
        amplitude: 0.8,
        label: "Inspiring conversation",
        narrative: "Had lunch with a friend who's been training consistently. Their energy and clarity were palpable. You leave thinking about what you could change.",
      },
      3: {
        amplitude: 1.5,
        label: "New Year's resolution",
        narrative: "January 1st. This is the year. You've bought new shoes, downloaded an app, and told three people about your plan. Motivation is high but so are expectations.",
      },
      4: {
        amplitude: 2.5,
        label: "Doctor's warning",
        narrative: "Bloodwork came back bad. Doctor said 'If you don't change something, we're looking at medication or worse in five years.' The fear is real and immediate.",
      },
      5: {
        amplitude: 4.0,
        label: "Life-threatening health scare",
        narrative: "Chest pain in the ER. Turned out to be a panic attack, not a heart attack -- this time. The discharge nurse handed you a brochure about cardiac risk factors. Your hands were shaking.",
      },
    },
  },

  lapse: {
    name: "Lapse / Slip",
    description: "A perceived violation of the behavioral goal.",
    levels: {
      1: {
        amplitude: 0.3,
        label: "Skipped one session",
        narrative: "Missed the gym because you stayed late at work. You know it's fine -- one day doesn't matter. Mild guilt but you'll go tomorrow.",
      },
      2: {
        amplitude: 0.7,
        label: "Missed a few days",
        narrative: "A cold kept you home for three days. You feel the gap. The shoes by the door look accusatory. Starting again feels harder than it should.",
      },
      3: {
        amplitude: 1.2,
        label: "Broke the streak",
        narrative: "Three-week streak broken by a weekend trip. On Monday you opened the tracking app and the empty days felt like a verdict. 'What's the point of starting over?'",
      },
      4: {
        amplitude: 1.8,
        label: "Full diet break at party",
        narrative: "Birthday party. You had the cake, the pizza, the drinks. Woke up feeling like the last month of discipline evaporated in one night. The voice says: 'See? You always do this.'",
      },
      5: {
        amplitude: 2.5,
        label: "Complete abandonment event",
        narrative: "Weighed yourself after two weeks of 'being good' and the number went UP. Something broke. You drove to McDonald's and ordered everything. If it doesn't work, why suffer?",
      },
    },
  },

  stress: {
    name: "Stress Event",
    description: "Acute stress that impairs goal-directed control and drains M.",
    levels: {
      1: {
        amplitude: 0.2,
        label: "Bad day at work",
        narrative: "Difficult meeting, passive-aggressive emails. You're depleted by 5pm. The couch pulls harder than the gym tonight.",
      },
      2: {
        amplitude: 0.4,
        label: "Week-long work crunch",
        narrative: "Deadline week. Sleeping poorly, eating fast food at your desk. Exercise isn't even on the radar -- survival mode.",
      },
      3: {
        amplitude: 0.7,
        label: "Relationship conflict",
        narrative: "Big fight with your partner. Can't concentrate, appetite gone. The emotional bandwidth for self-improvement is exactly zero.",
      },
      4: {
        amplitude: 0.9,
        label: "Job loss",
        narrative: "Laid off. The financial anxiety is constant. Your identity just shifted. All the mental energy that went toward habits is now consumed by survival planning.",
      },
      5: {
        amplitude: 1.0,
        label: "Major life crisis",
        narrative: "Family emergency, financial ruin, or loss of a loved one. The self you were building habits for feels like a stranger. Everything that wasn't essential got dropped.",
      },
    },
  },

  context: {
    name: "Context Disruption",
    description: "Environmental change that breaks cue-behavior associations.",
    levels: {
      1: {
        amplitude: 0.15,
        label: "Schedule change",
        narrative: "New work hours. Your usual 6am gym slot doesn't exist anymore. The routine still works, just... shifted. Takes a week to find the new rhythm.",
      },
      2: {
        amplitude: 0.3,
        label: "Gym closed / equipment broke",
        narrative: "Your gym is renovating for a month. The backup gym is 20 minutes farther. The cue-response chain that got you through the door is broken.",
      },
      3: {
        amplitude: 0.5,
        label: "Moved to new neighborhood",
        narrative: "New apartment, new commute, new grocery store. Every spatial cue that triggered your habit is gone. You know HOW to exercise but nothing in your environment says WHEN.",
      },
      4: {
        amplitude: 0.7,
        label: "Moved to new city",
        narrative: "Different city entirely. No gym membership, no running route, no workout buddy. The habit knowledge is there but the environmental scaffold is demolished.",
      },
      5: {
        amplitude: 0.85,
        label: "Complete life restructuring",
        narrative: "Divorce, cross-country move, career change -- all at once. You're rebuilding everything from scratch. The person who had those habits lived in a different world.",
      },
    },
  },

  injury: {
    name: "Injury (Start)",
    description: "Physical injury that prevents the target behavior entirely.",
    levels: {
      1: {
        amplitude: 1,
        label: "Minor strain (1-2 weeks)",
        narrative: "Tweaked your back doing deadlifts. Doctor says rest for a week or two. Annoying but manageable. You'll substitute with walking.",
      },
      2: {
        amplitude: 1,
        label: "Moderate injury (3-4 weeks)",
        narrative: "Sprained ankle on a trail run. Boot for three weeks. No weight-bearing exercise. You're watching your habit window close day by day.",
      },
      3: {
        amplitude: 1,
        label: "Significant injury (6-8 weeks)",
        narrative: "Torn rotator cuff. Surgery scheduled. Two months minimum before you can lift anything. The gym bag sits in the closet gathering dust.",
      },
      4: {
        amplitude: 1,
        label: "Major injury (3 months)",
        narrative: "ACL tear playing basketball. Surgery, PT, months of recovery. You'll be starting from scratch physically. The mental game is keeping hope alive.",
      },
      5: {
        amplitude: 1,
        label: "Severe injury (6+ months)",
        narrative: "Serious accident. Long hospitalization, extensive rehab. Exercise was the furthest thing from possible. When you're cleared, it'll be like starting from zero.",
      },
    },
  },

  heal: {
    name: "Heal (End Injury)",
    description: "Cleared to resume activity after injury.",
    levels: {
      1: {
        amplitude: 1,
        label: "Cleared for light activity",
        narrative: "Doctor gave the green light for walking and light stretching. Not back to full capacity, but the door is open again.",
      },
      2: {
        amplitude: 1,
        label: "Cleared for modified exercise",
        narrative: "PT says you can start exercising again with modifications. 50% of your old capacity. It feels like starting over, but the knowledge is still there.",
      },
      3: {
        amplitude: 1,
        label: "Full clearance",
        narrative: "Fully cleared. No restrictions. Your body is ready. The question is whether your habit infrastructure survived the gap.",
      },
      4: {
        amplitude: 1,
        label: "Full clearance + motivation",
        narrative: "Doctor cleared you and said 'you healed faster than expected.' That felt like a win. You're eager to get back.",
      },
      5: {
        amplitude: 1,
        label: "Full clearance + renewed purpose",
        narrative: "Six months of not being able to exercise taught you exactly how much it meant to you. You're not just cleared -- you're hungry. This time it's different.",
      },
    },
  },

  social: {
    name: "Social Encouragement",
    description: "Positive social influence without expectation inflation.",
    levels: {
      1: {
        amplitude: 0.2,
        label: "Compliment from friend",
        narrative: "'Hey, you look like you've been working out.' A small comment, but it registered. Someone noticed.",
      },
      2: {
        amplitude: 0.5,
        label: "Workout buddy invitation",
        narrative: "A coworker asked if you want to start running together on lunch breaks. Having someone to show up for changes the equation.",
      },
      3: {
        amplitude: 0.8,
        label: "Joined a group/class",
        narrative: "Signed up for a beginner's running group. Now there are people who expect you on Saturday mornings. Social accountability kicks in.",
      },
      4: {
        amplitude: 1.2,
        label: "Coach/trainer engagement",
        narrative: "Started working with a trainer who checks in weekly. You're paying them and they're tracking your progress. The external structure changes everything.",
      },
      5: {
        amplitude: 1.8,
        label: "Deep community integration",
        narrative: "You've become a regular at the 6am class. People know your name. Missing a day means someone texts to ask if you're OK. The habit has a social scaffold.",
      },
    },
  },

  impl_intention: {
    name: "Implementation Intention",
    description: "An if-then plan that reduces the M threshold needed for behavior.",
    levels: {
      1: {
        amplitude: 0.3,
        label: "Vague plan formed",
        narrative: "'I'll try to exercise more this week.' Not specific enough to create automaticity, but the intention is there.",
      },
      2: {
        amplitude: 0.5,
        label: "Specific plan, no cue",
        narrative: "'I'll go to the gym on Monday, Wednesday, Friday.' Days are set but no environmental trigger. Still requires remembering.",
      },
      3: {
        amplitude: 0.8,
        label: "If-then plan with cue",
        narrative: "'When I get home from work, I immediately put on running shoes and go out the door.' The cue-action link is explicit. Strategic automaticity.",
      },
      4: {
        amplitude: 1.2,
        label: "If-then plan + environment design",
        narrative: "Shoes by the door, gym bag in the car, alarm set for 5:45am, phone charging in the kitchen so you can't scroll in bed. Every friction point addressed.",
      },
      5: {
        amplitude: 1.5,
        label: "Full MCII protocol",
        narrative: "Mentally contrasted your desired future with current obstacles, formed specific if-then plans for each obstacle, and shared the plans with your accountability partner. The research-backed full protocol.",
      },
    },
  },

  simplify: {
    name: "Simplify (Reduce C)",
    description: "An event that causes the person to lower their behavioral complexity target.",
    levels: {
      1: {
        amplitude: 0.5,
        label: "Thought 'maybe start smaller'",
        narrative: "Lying in bed, scrolling past another missed gym session on your calendar. A quiet thought: 'What if I just walked around the block?' Not a plan yet, just a crack in the armor of ambition.",
      },
      2: {
        amplitude: 1.0,
        label: "Friend suggested just walking",
        narrative: "Over coffee, a friend who actually exercises regularly said: 'I started by just walking my dog every morning. That was it for the first three months.' It landed differently than the usual advice.",
      },
      3: {
        amplitude: 1.5,
        label: "Read about habit stacking / Tiny Habits",
        narrative: "Found BJ Fogg's Tiny Habits. The idea that you can start with two pushups after you pee -- that you can make the behavior laughably small -- felt like permission to stop failing at the hard version.",
      },
      4: {
        amplitude: 2.0,
        label: "Coach said 'drop the program, just show up'",
        narrative: "Your trainer looked at your attendance log and said: 'Forget the periodization plan. For the next month, your only job is to walk through the door. I don't care if you just stretch and leave.' A professional giving you permission to do less.",
      },
      5: {
        amplitude: 3.0,
        label: "Therapist prescribed radical simplification",
        narrative: "After describing your fifth failed diet-and-exercise overhaul, your therapist said: 'What if the goal isn't fitness? What if the goal is putting on shoes and stepping outside, every day, for 5 minutes?' Something about hearing it as a prescription -- not fitness advice but mental health treatment -- made it real.",
      },
    },
  },

  escalate: {
    name: "Escalate (Increase C)",
    description: "An event that increases behavioral complexity target -- sometimes productive, sometimes premature.",
    levels: {
      1: {
        amplitude: 0.3,
        label: "Saw advanced workout on Instagram",
        narrative: "Your explore page served you a fitness influencer's '10 exercises for shredded abs.' You saved it. Probably won't do it, but the seed of 'I should be doing more' is planted.",
      },
      2: {
        amplitude: 0.6,
        label: "Friend invited to intense class",
        narrative: "Your gym buddy said 'I signed us up for the Saturday HIIT class.' You said yes before thinking. It's twice the intensity of anything you've been doing.",
      },
      3: {
        amplitude: 1.0,
        label: "Signed up for a race/challenge",
        narrative: "Registered for a 5K three months out. Now you need a training plan, not just 'go for walks.' The goal is concrete and public -- you told people. The complexity of what you need to do just jumped.",
      },
      4: {
        amplitude: 1.5,
        label: "Bought comprehensive training program",
        narrative: "Dropped $200 on a 16-week periodized program with macros, supplements, and progressive overload spreadsheets. It's what serious people do. The gap between this and your current 3x/week walks is... significant.",
      },
      5: {
        amplitude: 2.0,
        label: "Hired trainer with ambitious periodization",
        narrative: "New trainer assessed you and built a 6-day program with two-a-days on weekends, meal prep Sundays, and daily weigh-ins. 'If you want results, you have to commit.' Your current habit was working. Now it needs to be ten times more.",
      },
    },
  },
};

/**
 * Get the event spec for a given type and strength level.
 */
function getEventSpec(type, strength) {
  const catalog = EVENT_CATALOG[type];
  if (!catalog) return null;
  const level = catalog.levels[strength];
  if (!level) return null;
  return {
    type: type === 'injury' ? 'injury_start' : type === 'heal' ? 'injury_end' : type,
    amplitude: level.amplitude,
    label: level.label,
    narrative: level.narrative,
  };
}

/**
 * Get the narrative text for a given type and strength.
 */
function getEventNarrative(type, strength) {
  const spec = getEventSpec(type, strength);
  return spec ? spec.narrative : '';
}

window.EVENT_CATALOG = EVENT_CATALOG;
window.getEventSpec = getEventSpec;
window.getEventNarrative = getEventNarrative;
