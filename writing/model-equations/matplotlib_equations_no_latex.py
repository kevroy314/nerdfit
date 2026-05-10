"""
Matplotlib-based visualization of Nerdfit equations WITHOUT LaTeX dependency.
Uses matplotlib's mathtext for equation rendering (no LaTeX required).

Usage:
  python matplotlib_equations_no_latex.py
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend (headless)

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

# Configure matplotlib (no LaTeX)
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['mathtext.fontset'] = 'dejavuserif'

# Phenomenon color palette (matching LaTeX)
COLORS = {
    'st': '#1B2631',      # state variables
    'hb': '#1B7F6A',      # habit & automaticity
    'mv': '#C45C26',      # motivation & reward
    'ef': '#5C4D8A',      # effort / opportunity cost
    'ex': '#6B4C9A',      # expectation excess
    'id': '#2874A6',      # identity & self-concept
    'cx': '#7D6608',      # behavioral complexity
    'fn': '#AF601A',      # fantasy / indulgence
    'cl': '#B03A2E',      # collapse & disinhibition
    'ct': '#1F618D',      # context
    'mt': '#566573',      # meta-control
}

def hex_to_mathtext_color(hex_color):
    """Convert hex color to RGB tuple for mathtext."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4))

def create_tag(ax, x, y, text, color, width=0.08, height=0.03):
    """Create a colored tag/chip."""
    rect = FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.003",
        facecolor=color,
        edgecolor='none',
        transform=ax.transAxes
    )
    ax.add_patch(rect)

    ax.text(
        x + width/2, y + height/2,
        text,
        ha='center', va='center',
        fontsize=7,
        weight='bold',
        color='white',
        transform=ax.transAxes
    )

def create_full_visualization():
    """Create the complete visualization with all equations."""

    fig = plt.figure(figsize=(18, 24))
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Title
    ax.text(
        0.5, 0.98,
        'Nerdfit Behavioral Dynamics',
        ha='center',
        fontsize=28,
        weight='bold',
        family='sans-serif'
    )

    ax.text(
        0.5, 0.955,
        'Color-Coded Mechanistic Model',
        ha='center',
        fontsize=16,
        color='#666',
        style='italic',
        family='sans-serif'
    )

    # Color legend
    legend_y = 0.91
    legend_items = [
        ('STATE', 'st', 'State variables H, M, E, I, C'),
        ('HABIT', 'hb', 'Habit & automaticity'),
        ('REWARD', 'mv', 'Motivation & reward'),
        ('EFFORT', 'ef', 'Effort / opportunity cost'),
        ('EXPECT', 'ex', 'Expectation dynamics'),
        ('IDENTITY', 'id', 'Identity & self-concept'),
    ]

    legend_items_2 = [
        ('COMPLEX', 'cx', 'Behavioral complexity'),
        ('FANTASY', 'fn', 'Fantasy / indulgence'),
        ('COLLAPSE', 'cl', 'Collapse & disinhibition'),
        ('CONTEXT', 'ct', 'Context (stress, social, plans)'),
        ('META', 'mt', 'Meta-control & gating'),
    ]

    # Draw legend background
    legend_box = FancyBboxPatch(
        (0.05, legend_y - 0.055), 0.9, 0.045,
        boxstyle="round,pad=0.005",
        facecolor='#f5f5f5',
        edgecolor='#ccc',
        linewidth=1,
        transform=ax.transAxes
    )
    ax.add_patch(legend_box)

    # First row of legend
    legend_x = 0.07
    for label, color_key, desc in legend_items:
        create_tag(ax, legend_x, legend_y - 0.02, label, COLORS[color_key], width=0.065)
        ax.text(
            legend_x + 0.068, legend_y - 0.02 + 0.015,
            desc,
            fontsize=7,
            va='center',
            transform=ax.transAxes
        )
        legend_x += 0.15

    # Second row of legend
    legend_x = 0.07
    for label, color_key, desc in legend_items_2:
        create_tag(ax, legend_x, legend_y - 0.045, label, COLORS[color_key], width=0.065)
        ax.text(
            legend_x + 0.068, legend_y - 0.045 + 0.015,
            desc,
            fontsize=7,
            va='center',
            transform=ax.transAxes
        )
        legend_x += 0.18

    current_y = 0.83

    # Helper function to create equation boxes
    def eq_box(y, h, title, tags, eq_text, desc, highlight=None):
        if highlight:
            box = FancyBboxPatch(
                (0.05, y), 0.9, h,
                boxstyle="round,pad=0.01",
                facecolor=highlight,
                edgecolor='gray',
                linewidth=1.5,
                alpha=0.1,
                transform=ax.transAxes
            )
        else:
            box = FancyBboxPatch(
                (0.05, y), 0.9, h,
                boxstyle="round,pad=0.01",
                facecolor='white',
                edgecolor='gray',
                linewidth=1.5,
                transform=ax.transAxes
            )
        ax.add_patch(box)

        # Title
        ax.text(
            0.08, y + h - 0.025,
            title,
            fontsize=14,
            weight='bold',
            family='sans-serif',
            transform=ax.transAxes
        )

        # Tags
        tag_x = 0.55
        for tag_text, tag_color in tags:
            create_tag(ax, tag_x, y + h - 0.025, tag_text, COLORS[tag_color])
            tag_x += 0.09

        # Equation
        ax.text(
            0.5, y + h/2,
            eq_text,
            fontsize=11,
            ha='center',
            va='center',
            transform=ax.transAxes
        )

        # Description
        ax.text(
            0.08, y + 0.015,
            desc,
            fontsize=8,
            style='italic',
            color='#444',
            family='sans-serif',
            transform=ax.transAxes
        )

    # 1. Behavioral Trigger
    # Using matplotlib's mathtext (simplified from LaTeX)
    trigger_eq = r'''$\theta = C(1-H) + \mathrm{stress} \cdot 0.3 - ii$
    $B_{\mathrm{goal}} = \sigma((M-\theta)/\tau) \quad B_{\mathrm{habit}} = H\,\sigma((M-M_{\mathrm{floor}})/0.08)$
    $\mathrm{blend} = H^{1.5} \quad B = B_{\mathrm{raw}}\,\sigma((M-0.08)/0.03)$'''

    eq_box(
        current_y, 0.11,
        'Behavioral Trigger',
        [('COMPLEX', 'cx'), ('STATE', 'st'), ('CONTEXT', 'ct'), ('META', 'mt')],
        trigger_eq,
        'Complexity and stress raise threshold; implementation intentions lower it. Smooth shift to automatic.',
        None
    )

    current_y -= 0.13

    # 2. Habit & Fantasy (side by side - simplified)
    habit_box = FancyBboxPatch(
        (0.05, current_y), 0.43, 0.11,
        boxstyle="round,pad=0.01",
        facecolor='white',
        edgecolor='gray',
        linewidth=1.5,
        transform=ax.transAxes
    )
    ax.add_patch(habit_box)

    ax.text(0.07, current_y + 0.095, 'Habit Strength', fontsize=13, weight='bold', family='sans-serif', transform=ax.transAxes)
    create_tag(ax, 0.22, current_y + 0.09, 'HABIT', COLORS['hb'])
    create_tag(ax, 0.31, current_y + 0.09, 'IDENTITY', COLORS['id'])

    habit_eq = r'$dH/dt = \alpha_H B(A(I)-H) - \mathrm{decay}(1-B)(H-H_{\min})$'
    ax.text(0.26, current_y + 0.055, habit_eq, ha='center', va='center', fontsize=11, transform=ax.transAxes)
    ax.text(0.07, current_y + 0.012, 'Ceiling A(I) raised by identity. Decay when not practicing.',
            fontsize=7, style='italic', color='#444', family='sans-serif', transform=ax.transAxes)

    # Fantasy
    fantasy_box = FancyBboxPatch(
        (0.51, current_y), 0.44, 0.11,
        boxstyle="round,pad=0.01",
        facecolor='white',
        edgecolor='gray',
        linewidth=1.5,
        transform=ax.transAxes
    )
    ax.add_patch(fantasy_box)

    ax.text(0.53, current_y + 0.095, 'Fantasy / Indulgence', fontsize=13, weight='bold', family='sans-serif', transform=ax.transAxes)
    create_tag(ax, 0.76, current_y + 0.09, 'FANTASY', COLORS['fn'])

    fantasy_eq = r'$F = f_0 M(1-B)$'
    ax.text(0.73, current_y + 0.055, fantasy_eq, ha='center', va='center', fontsize=13, transform=ax.transAxes)
    ax.text(0.53, current_y + 0.012, 'Mental indulgence when motivation exists but behavior doesn\'t.',
            fontsize=7, style='italic', color='#444', family='sans-serif', transform=ax.transAxes)

    current_y -= 0.14

    # 3. Motivation (large, highlighted)
    motivation_eq = r'''$dM/dt = -\beta_M M/(1+M) + \gamma B(1-H^2)(1-M/2) - \lambda C(1-H)B$
    $- \gamma_{\mathrm{ind}} F(1-H) - \kappa\,\mathrm{sp}(-E-|E_c|)M - \kappa_{\mathrm{wth}}\sigma((E-E_{\mathrm{wth}})/0.2)M$
    $+ \mu(-dE/dt) + 0.08\max(0, 0.2I-M) + 0.02BH + \mathrm{context}$'''

    eq_box(
        current_y, 0.13,
        'Motivational Activation',
        [('REWARD', 'mv'), ('EFFORT', 'ef'), ('FANTASY', 'fn'), ('COLLAPSE', 'cl'), ('META', 'mt')],
        motivation_eq,
        'Central hub: reward from action, effort cost, fantasy drain, collapse mechanisms, velocity feedback.',
        COLORS['mv']
    )

    current_y -= 0.15

    # 4. Expectation & Identity (side by side)
    exp_box = FancyBboxPatch(
        (0.05, current_y), 0.43, 0.11,
        boxstyle="round,pad=0.01",
        facecolor='white',
        edgecolor='gray',
        linewidth=1.5,
        transform=ax.transAxes
    )
    ax.add_patch(exp_box)

    ax.text(0.07, current_y + 0.095, 'Expectation Excess', fontsize=13, weight='bold', family='sans-serif', transform=ax.transAxes)
    create_tag(ax, 0.22, current_y + 0.09, 'EXPECT', COLORS['ex'])
    create_tag(ax, 0.31, current_y + 0.09, 'FANTASY', COLORS['fn'])

    exp_eq = r'$dE/dt = \phi_M M(1-H) - \psi BH - \epsilon E + \phi_{\mathrm{ind}} F$'
    ax.text(0.26, current_y + 0.055, exp_eq, ha='center', va='center', fontsize=11, transform=ax.transAxes)
    ax.text(0.07, current_y + 0.012, 'High M with weak habit inflates expectations. Progress corrects.',
            fontsize=7, style='italic', color='#444', family='sans-serif', transform=ax.transAxes)

    # Identity
    id_box = FancyBboxPatch(
        (0.51, current_y), 0.44, 0.11,
        boxstyle="round,pad=0.01",
        facecolor='white',
        edgecolor='gray',
        linewidth=1.5,
        transform=ax.transAxes
    )
    ax.add_patch(id_box)

    ax.text(0.53, current_y + 0.095, 'Identity Coherence', fontsize=13, weight='bold', family='sans-serif', transform=ax.transAxes)
    create_tag(ax, 0.76, current_y + 0.09, 'IDENTITY', COLORS['id'])

    id_eq = r'$dI/dt = \alpha_I BH(1-I) - \delta_I(1-B)I$'
    ax.text(0.73, current_y + 0.055, id_eq, ha='center', va='center', fontsize=11, transform=ax.transAxes)
    ax.text(0.53, current_y + 0.012, 'Grows when behavior is habitual. Decays when inactive.',
            fontsize=7, style='italic', color='#444', family='sans-serif', transform=ax.transAxes)

    current_y -= 0.14

    # 5. Complexity
    complexity_eq = r'''$C_{\mathrm{eq}} = C_{\min} + (C_{\max}-C_{\min})H(0.7+0.3I)$
    $dC/dt = [-\alpha_{C\downarrow}\max(0,C-C_{\mathrm{eq}})\max(0,0.3-B) + \alpha_{C\uparrow}\max(0,C_{\mathrm{eq}}-C)B$
    $+ \mathrm{false\!-\!hope} + \mathrm{identity}] \cdot (1+\mathrm{social})$'''

    eq_box(
        current_y, 0.12,
        'Behavioral Complexity',
        [('COMPLEX', 'cx'), ('IDENTITY', 'id'), ('EXPECT', 'ex'), ('CONTEXT', 'ct')],
        complexity_eq,
        'Equilibrium rises with habit and identity. Progressive overload when performing; simplify when overwhelmed.',
        COLORS['cx']
    )

    current_y -= 0.14

    # 6. Context
    context_eq = r'$\mathrm{stress} \leftarrow \mathrm{stress}(1-0.1\Delta t) \quad ii \leftarrow ii(1-0.05\Delta t) \quad \mathrm{social} \leftarrow \mathrm{social}(1-0.003\Delta t)$'

    eq_box(
        current_y, 0.09,
        'Transient Context Variables',
        [('CONTEXT', 'ct')],
        context_eq,
        'Multiplicative decay on different time scales (days to months).',
        None
    )

    # Footer
    ax.text(
        0.5, 0.02,
        'A mechanistic model synthesizing habit formation, motivation dynamics, expectation calibration,',
        ha='center',
        fontsize=9,
        color='#666',
        style='italic',
        family='sans-serif',
        transform=ax.transAxes
    )

    ax.text(
        0.5, 0.005,
        'identity development, and behavioral complexity for understanding behavior change.',
        ha='center',
        fontsize=9,
        color='#666',
        style='italic',
        family='sans-serif',
        transform=ax.transAxes
    )

    plt.tight_layout()
    return fig

if __name__ == '__main__':
    print("Creating visualization (without LaTeX dependency)...")
    fig = create_full_visualization()
    plt.savefig('nerdfit_equations_nolatex.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Saved: nerdfit_equations_nolatex.png")

    try:
        plt.savefig('nerdfit_equations_nolatex.pdf', bbox_inches='tight', facecolor='white')
        print("✓ Saved: nerdfit_equations_nolatex.pdf")
    except Exception as e:
        print(f"  (PDF save failed: {e})")

    print("\nDone!")
