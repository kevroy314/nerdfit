"""
Predefined scenarios based on PHENOMENA.md for validating the dynamical systems model.
Each scenario defines initial conditions, parameters, and extrinsic events.
"""

from dynamics import Params, Event, SimState


def scenario_successful_bootstrap():
    """P30: Low complexity, moderate initial motivation, gradual H growth."""
    return {
        "name": "Successful Bootstrapping",
        "description": "Low complexity (walking 15min/day). M decays but B continues firing due to low threshold. H reaches self-sustaining level.",
        "phenomena": ["P1", "P3", "P5", "P19", "P29", "P30"],
        "params": Params(C=0.2, alpha_H=0.045, beta_M=0.12, gamma=0.3, sigma_noise=0.015),
        "initial": SimState(H=0.02, M=1.2, E=0.3, I=0.0),
        "events": [
            Event(time=0, event_type="shock", amplitude=0.5, label="Decided to start walking"),
        ],
        "t_end": 180,
    }


def scenario_false_hope_cycle():
    """P11: High complexity, large shocks, repeated failure cycling."""
    return {
        "name": "False Hope Limit Cycle",
        "description": "New Year's resolution to do intense 6-day/week gym program. High C, periodic shocks re-inject M without H accumulation.",
        "phenomena": ["P11", "P33", "P7"],
        "params": Params(C=0.8, alpha_H=0.045, phi_S=1.5, kappa=0.35, E_crit=-1.0,
                         beta_M=0.2, lambda_=0.35, gamma=0.15),
        "initial": SimState(H=0.02, M=0.3, E=0.0, I=0.0),
        "events": [
            Event(time=0, event_type="new_year", amplitude=2.0, label="New Year's Resolution"),
            Event(time=90, event_type="new_year", amplitude=1.5, label="Spring recommitment"),
            Event(time=180, event_type="shock", amplitude=1.0, label="Summer body motivation"),
            Event(time=270, event_type="new_year", amplitude=1.8, label="Next New Year's"),
        ],
        "t_end": 365,
    }


def scenario_indulgence_trap():
    """P31: Moderate conditions but endogenous fantasy drains M quietly."""
    return {
        "name": "Indulgence Trap",
        "description": "Person watches fitness content, plans routines, fantasizes about results, but rarely acts. M leaks through phantom reward.",
        "phenomena": ["P17", "P31"],
        "params": Params(C=0.7, alpha_H=0.045, f_0=0.6, gamma_ind=0.2, phi_ind=0.1,
                         gamma=0.12, beta_M=0.1, sigma_noise=0.01),
        "initial": SimState(H=0.02, M=0.8, E=0.5, I=0.0),
        "events": [
            Event(time=0, event_type="shock", amplitude=0.5, label="Inspired by fitness influencer"),
        ],
        "t_end": 120,
    }


def scenario_complexity_overshoot():
    """P32: Too much too soon. High C blocks B, effort depletes M."""
    return {
        "name": "Complexity Overshoot",
        "description": "Hired a trainer, bought meal prep containers, signed up for 5am CrossFit. C too high for initial M.",
        "phenomena": ["P32", "P9"],
        "params": Params(C=0.95, alpha_H=0.045, lambda_=0.5, beta_M=0.2,
                         gamma=0.1, sigma_noise=0.015),
        "initial": SimState(H=0.02, M=1.5, E=1.5, I=0.0),
        "events": [
            Event(time=0, event_type="shock", amplitude=1.0, label="All-in commitment"),
        ],
        "t_end": 90,
    }


def scenario_post_shock_dropout():
    """P33: Health scare -> rapid initial engagement -> exponential dropout curve."""
    return {
        "name": "Post-Shock Dropout",
        "description": "Doctor says cholesterol is dangerous. Immediate behavior change attempt with moderate complexity.",
        "phenomena": ["P10", "P33", "P14"],
        "params": Params(C=0.7, alpha_H=0.045, phi_S=1.5, beta_M=0.18,
                         lambda_=0.3, gamma=0.15),
        "initial": SimState(H=0.02, M=0.3, E=0.0, I=0.0),
        "events": [
            Event(time=0, event_type="shock", amplitude=2.5, label="Doctor's warning"),
        ],
        "t_end": 365,
    }


def scenario_context_disruption():
    """P34: Established habit disrupted by moving, then recovery."""
    return {
        "name": "Context Disruption & Recovery",
        "description": "Person with established gym habit moves to new city. H drops but recovers faster than initial formation due to I.",
        "phenomena": ["P4", "P21", "P34"],
        "params": Params(C=0.4, alpha_H=0.045, sigma_noise=0.015),
        "initial": SimState(H=0.7, M=0.8, E=0.0, I=0.5),
        "events": [
            Event(time=30, event_type="context_disruption", amplitude=0.6, label="Moved to new city"),
            Event(time=45, event_type="shock", amplitude=0.5, label="Found new gym"),
        ],
        "t_end": 180,
    }


def scenario_what_the_hell():
    """P12: Strict diet, single violation triggers catastrophic M collapse."""
    return {
        "name": "What-the-Hell Effect",
        "description": "Strict diet plan. One perceived violation (birthday cake) triggers E spike and catastrophic M drop.",
        "phenomena": ["P12", "P14"],
        "params": Params(C=0.7, alpha_H=0.045, kappa_wth=1.5, E_wth=1.0,
                         beta_M=0.15, lambda_=0.3, sigma_noise=0.01),
        "initial": SimState(H=0.05, M=0.8, E=0.6, I=0.0),
        "events": [
            Event(time=0, event_type="shock", amplitude=1.0, label="Started strict diet"),
            Event(time=21, event_type="lapse", amplitude=1.5, label="Birthday party (lapse)"),
        ],
        "t_end": 90,
    }


def scenario_identity_stabilized():
    """P21: Long-term exerciser weathers disruptions due to strong identity."""
    return {
        "name": "Identity-Stabilized Maintenance",
        "description": "10-year runner with strong exercise identity. Survives injury and stress because I keeps M above zero and A high.",
        "phenomena": ["P21", "P23", "P20"],
        "params": Params(C=0.4, alpha_H=0.045, sigma_noise=0.02),
        "initial": SimState(H=0.85, M=0.6, E=0.0, I=0.8),
        "events": [
            Event(time=30, event_type="injury_start", amplitude=1.0, label="Knee injury"),
            Event(time=60, event_type="injury_end", amplitude=1.0, label="Cleared to exercise"),
            Event(time=90, event_type="stress", amplitude=0.7, label="Work crisis"),
        ],
        "t_end": 180,
    }


def scenario_implementation_intention():
    """P27: Implementation intentions reduce threshold, bootstrapping H faster."""
    return {
        "name": "Implementation Intention Boost",
        "description": "Person forms specific if-then plan: 'When I get home from work, I put on running shoes.' Reduces effective threshold.",
        "phenomena": ["P27", "P28", "P30"],
        "params": Params(C=0.6, alpha_H=0.045, sigma_noise=0.015),
        "initial": SimState(H=0.02, M=0.8, E=0.3, I=0.0),
        "events": [
            Event(time=0, event_type="impl_intention", amplitude=0.8, label="Formed if-then plan"),
            Event(time=0, event_type="shock", amplitude=0.5, label="Motivated to start"),
        ],
        "t_end": 120,
    }


def scenario_stress_relapse():
    """P35: Stress shifts control to habitual. Bad if H_good is low."""
    return {
        "name": "Stress-Induced Relapse",
        "description": "Early habit former (low H) hit by major stressor. Stress depletes M and H is too low to sustain behavior alone.",
        "phenomena": ["P23", "P35"],
        "params": Params(C=0.6, alpha_H=0.045, beta_M=0.2, lambda_=0.3, sigma_noise=0.02),
        "initial": SimState(H=0.05, M=0.7, E=0.3, I=0.0),
        "events": [
            Event(time=0, event_type="shock", amplitude=0.6, label="Started exercising"),
            Event(time=21, event_type="stress", amplitude=0.9, label="Job loss"),
            Event(time=21, event_type="shock", amplitude=-0.5, label="Stress depletes M"),
        ],
        "t_end": 120,
    }


def scenario_reward_habituation():
    """P15: Reward prediction error diminishes as behavior becomes routine."""
    return {
        "name": "Reward Habituation",
        "description": "Initial excitement of new gym fades as reward becomes fully predicted. M sustained only if H grows fast enough.",
        "phenomena": ["P15", "P16"],
        "params": Params(C=0.5, alpha_H=0.045, gamma=0.35, beta_M=0.15, sigma_noise=0.015),
        "initial": SimState(H=0.02, M=1.0, E=0.3, I=0.0),
        "events": [
            Event(time=0, event_type="shock", amplitude=0.5, label="Joined exciting new gym"),
        ],
        "t_end": 180,
    }


# Registry of all scenarios
ALL_SCENARIOS = {
    "bootstrap": scenario_successful_bootstrap,
    "false_hope": scenario_false_hope_cycle,
    "indulgence": scenario_indulgence_trap,
    "complexity_overshoot": scenario_complexity_overshoot,
    "post_shock": scenario_post_shock_dropout,
    "context_disruption": scenario_context_disruption,
    "what_the_hell": scenario_what_the_hell,
    "identity_stable": scenario_identity_stabilized,
    "impl_intention": scenario_implementation_intention,
    "stress_relapse": scenario_stress_relapse,
    "reward_habituation": scenario_reward_habituation,
}
