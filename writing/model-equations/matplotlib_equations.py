"""
Matplotlib-based visualization of Nerdfit equations with rich typography.
Better control over layout, colors, and styling than pure LaTeX.

Usage:
  python matplotlib_equations.py
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

# Configure matplotlib for LaTeX rendering
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Computer Modern Roman']
plt.rcParams['font.size'] = 11

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

def create_equation_card(fig, ax, title, tags, equation, description, y_pos, height=0.15, highlight_color=None):
    """Create a styled equation card."""

    # Background box
    if highlight_color:
        box = FancyBboxPatch(
            (0.05, y_pos), 0.9, height,
            boxstyle="round,pad=0.01",
            facecolor=highlight_color,
            edgecolor='gray',
            linewidth=1.5,
            alpha=0.1,
            transform=ax.transAxes
        )
    else:
        box = FancyBboxPatch(
            (0.05, y_pos), 0.9, height,
            boxstyle="round,pad=0.01",
            facecolor='white',
            edgecolor='gray',
            linewidth=1.5,
            transform=ax.transAxes
        )
    ax.add_patch(box)

    # Title
    ax.text(
        0.08, y_pos + height - 0.025,
        title,
        fontsize=13,
        weight='bold',
        transform=ax.transAxes
    )

    # Tags
    tag_x = 0.55
    for tag_text, tag_color in tags:
        create_tag(ax, tag_x, y_pos + height - 0.025, tag_text, COLORS[tag_color])
        tag_x += 0.09

    # Equation
    ax.text(
        0.5, y_pos + height/2,
        equation,
        fontsize=12,
        ha='center',
        va='center',
        transform=ax.transAxes
    )

    # Description
    ax.text(
        0.08, y_pos + 0.015,
        description,
        fontsize=8,
        style='italic',
        color='#444',
        transform=ax.transAxes,
        wrap=True
    )

def create_full_visualization():
    """Create the complete visualization with all equations."""

    fig = plt.figure(figsize=(16, 22))
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Title
    ax.text(
        0.5, 0.98,
        r'\textbf{\Large Nerdfit Behavioral Dynamics}',
        ha='center',
        fontsize=24,
        weight='bold'
    )

    ax.text(
        0.5, 0.955,
        r'\textit{Color-Coded Mechanistic Model}',
        ha='center',
        fontsize=14,
        color='#666'
    )

    # Color legend
    legend_y = 0.91
    legend_items = [
        ('STATE', 'st', r'State variables $\mathbf{H}, \mathbf{M}, \mathbf{E}, \mathbf{I}, \mathbf{C}$'),
        ('HABIT', 'hb', 'Habit \\& automaticity'),
        ('REWARD', 'mv', 'Motivation \\& reward'),
        ('EFFORT', 'ef', 'Effort / opportunity cost'),
        ('EXPECT', 'ex', 'Expectation dynamics'),
        ('IDENTITY', 'id', 'Identity \\& self-concept'),
    ]

    legend_items_2 = [
        ('COMPLEX', 'cx', 'Behavioral complexity'),
        ('FANTASY', 'fn', 'Fantasy / indulgence'),
        ('COLLAPSE', 'cl', 'Collapse \\& disinhibition'),
        ('CONTEXT', 'ct', 'Context (stress, social, plans)'),
        ('META', 'mt', 'Meta-control \\& gating'),
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

    # 1. Behavioral Trigger
    trigger_eq = r'''$\begin{aligned}
        \theta &= \textcolor[HTML]{7D6608}{C}(1-\mathbf{H}) + \textcolor[HTML]{1F618D}{\text{stress}} \cdot 0.3\,(1-\mathbf{H}) - \textcolor[HTML]{1F618D}{ii} \\
        B_{\text{goal}} &= \sigma\!\left(\frac{\mathbf{M}-\theta}{\textcolor[HTML]{566573}{\tau}}\right) \quad
        B_{\text{habit}} = \mathbf{H}\,\sigma\!\left(\frac{\mathbf{M}-M_{\text{floor}}}{0.08}\right) \\
        \text{blend} &= \mathbf{H}^{1.5} \quad
        B = B_{\text{raw}}\,\sigma\!\left(\frac{\mathbf{M}-0.08}{0.03}\right)
    \end{aligned}$'''

    create_equation_card(
        fig, ax,
        'Behavioral Trigger',
        [('COMPLEX', 'cx'), ('STATE', 'st'), ('CONTEXT', 'ct'), ('META', 'mt')],
        trigger_eq,
        r'Complexity and stress raise threshold; implementation intentions lower it. As $\mathbf{H}$ grows, shifts to automatic.',
        current_y,
        height=0.11
    )

    current_y -= 0.13

    # 2. Habit Strength (left) and Fantasy (right)
    habit_y = current_y
    habit_eq = r'''$\begin{aligned}
        \text{decay} &= \textcolor[HTML]{1B7F6A}{\delta_H}\bigl(1 + 2(1-B)\mathbf{H}\bigr) \\
        \frac{d\mathbf{H}}{dt} &= \textcolor[HTML]{1B7F6A}{\alpha_H}\,B\,(A(\mathbf{I})-\mathbf{H}) \\
        &\quad - \text{decay}\,(1-B)\,(\mathbf{H}-\textcolor[HTML]{1B7F6A}{H_{\min}})
    \end{aligned}$'''

    # Manual placement for side-by-side
    habit_box = FancyBboxPatch(
        (0.05, habit_y), 0.43, 0.11,
        boxstyle="round,pad=0.01",
        facecolor='white',
        edgecolor='gray',
        linewidth=1.5,
        transform=ax.transAxes
    )
    ax.add_patch(habit_box)

    ax.text(0.07, habit_y + 0.095, 'Habit Strength', fontsize=13, weight='bold', transform=ax.transAxes)
    create_tag(ax, 0.22, habit_y + 0.09, 'HABIT', COLORS['hb'])
    create_tag(ax, 0.31, habit_y + 0.09, 'IDENTITY', COLORS['id'])

    ax.text(0.26, habit_y + 0.055, habit_eq, ha='center', va='center', fontsize=11, transform=ax.transAxes)

    ax.text(
        0.07, habit_y + 0.012,
        r'Ceiling $A(\mathbf{I})$ raised by identity. Decay when not practicing.',
        fontsize=7, style='italic', color='#444', transform=ax.transAxes
    )

    # Fantasy (right side)
    fantasy_box = FancyBboxPatch(
        (0.51, habit_y), 0.44, 0.11,
        boxstyle="round,pad=0.01",
        facecolor='white',
        edgecolor='gray',
        linewidth=1.5,
        transform=ax.transAxes
    )
    ax.add_patch(fantasy_box)

    ax.text(0.53, habit_y + 0.095, 'Fantasy / Indulgence', fontsize=13, weight='bold', transform=ax.transAxes)
    create_tag(ax, 0.76, habit_y + 0.09, 'FANTASY', COLORS['fn'])

    fantasy_eq = r'$F = \textcolor[HTML]{AF601A}{f_0}\,\mathbf{M}\,(1-B)$'
    ax.text(0.73, habit_y + 0.055, fantasy_eq, ha='center', va='center', fontsize=13, transform=ax.transAxes)

    ax.text(
        0.53, habit_y + 0.012,
        'Mental indulgence when motivation exists but behavior doesn\'t.',
        fontsize=7, style='italic', color='#444', transform=ax.transAxes
    )

    current_y -= 0.14

    # 3. Motivation (large, highlighted)
    motivation_eq = r'''$\begin{aligned}
        \frac{d\mathbf{M}}{dt} &=
        \underbrace{-\textcolor[HTML]{C45C26}{\beta_M}\,\frac{\mathbf{M}}{1+\mathbf{M}}}_{\text{decay}}
        + \underbrace{\textcolor[HTML]{C45C26}{\gamma}\,B\,(1-\mathbf{H}^2)(1-\mathbf{M}/2)}_{\text{reward}}
        - \underbrace{\textcolor[HTML]{5C4D8A}{\lambda}\,\mathbf{C}\,(1-\mathbf{H})\,B}_{\text{effort}} \\
        &\quad - \underbrace{\textcolor[HTML]{AF601A}{\gamma_{\text{ind}}}\,F\,(1-\mathbf{H})}_{\text{fantasy drain}}
        - \underbrace{\textcolor[HTML]{B03A2E}{\kappa}\,\text{sp}(-\mathbf{E}-|E_c|)\,\mathbf{M}}_{\text{false-hope}}
        - \underbrace{\textcolor[HTML]{B03A2E}{\kappa_{\text{wth}}}\,\sigma\!\left(\frac{\mathbf{E}-E_{\text{wth}}}{0.2}\right)\,\mathbf{M}}_{\text{what-the-hell}} \\
        &\quad + \underbrace{\textcolor[HTML]{566573}{\mu}\,\left(-\frac{d\mathbf{E}}{dt}\right)}_{\text{velocity}}
        + \underbrace{0.08\max(0, 0.2\mathbf{I}-\mathbf{M})}_{\text{identity}}
        + \underbrace{0.02\,B\,\mathbf{H}}_{\text{maintenance}}
        + \text{context terms}
    \end{aligned}$'''

    create_equation_card(
        fig, ax,
        'Motivational Activation',
        [('REWARD', 'mv'), ('EFFORT', 'ef'), ('FANTASY', 'fn'), ('COLLAPSE', 'cl'), ('META', 'mt')],
        motivation_eq,
        r'Central hub: reward vs effort, fantasy drain, expectation collapse, velocity feedback, identity sustenance.',
        current_y,
        height=0.13,
        highlight_color=COLORS['mv']
    )

    current_y -= 0.15

    # 4. Expectation (left) and Identity (right)
    exp_y = current_y

    # Expectation
    exp_box = FancyBboxPatch(
        (0.05, exp_y), 0.43, 0.11,
        boxstyle="round,pad=0.01",
        facecolor='white',
        edgecolor='gray',
        linewidth=1.5,
        transform=ax.transAxes
    )
    ax.add_patch(exp_box)

    ax.text(0.07, exp_y + 0.095, 'Expectation Excess', fontsize=13, weight='bold', transform=ax.transAxes)
    create_tag(ax, 0.22, exp_y + 0.09, 'EXPECT', COLORS['ex'])
    create_tag(ax, 0.31, exp_y + 0.09, 'FANTASY', COLORS['fn'])

    exp_eq = r'''$\begin{aligned}
        \frac{d\mathbf{E}}{dt} &= \textcolor[HTML]{6B4C9A}{\phi_M}\,\mathbf{M}(1-\mathbf{H})
        - \textcolor[HTML]{6B4C9A}{\psi}\,B\,\mathbf{H} \\
        &\quad - \textcolor[HTML]{6B4C9A}{\epsilon}\,\mathbf{E}
        + \textcolor[HTML]{AF601A}{\phi_{\text{ind}}}\,F \\
        &\quad - 0.3\,B\,(1-\mathbf{H})\,\mathbf{1}_{\{\mathbf{E}>0\}}
    \end{aligned}$'''

    ax.text(0.26, exp_y + 0.055, exp_eq, ha='center', va='center', fontsize=10, transform=ax.transAxes)

    ax.text(
        0.07, exp_y + 0.012,
        r'High $\mathbf{M}$ with weak habit inflates. Progress corrects.',
        fontsize=7, style='italic', color='#444', transform=ax.transAxes
    )

    # Identity
    id_box = FancyBboxPatch(
        (0.51, exp_y), 0.44, 0.11,
        boxstyle="round,pad=0.01",
        facecolor='white',
        edgecolor='gray',
        linewidth=1.5,
        transform=ax.transAxes
    )
    ax.add_patch(id_box)

    ax.text(0.53, exp_y + 0.095, 'Identity Coherence', fontsize=13, weight='bold', transform=ax.transAxes)
    create_tag(ax, 0.76, exp_y + 0.09, 'IDENTITY', COLORS['id'])

    id_eq = r'$\frac{d\mathbf{I}}{dt} = \textcolor[HTML]{2874A6}{\alpha_I}\,B\,\mathbf{H}\,(1-\mathbf{I}) - \textcolor[HTML]{2874A6}{\delta_I}\,(1-B)\,\mathbf{I}$'
    ax.text(0.73, exp_y + 0.055, id_eq, ha='center', va='center', fontsize=11, transform=ax.transAxes)

    ax.text(
        0.53, exp_y + 0.012,
        'Grows when behavior is habitual. Decays when inactive.',
        fontsize=7, style='italic', color='#444', transform=ax.transAxes
    )

    current_y -= 0.14

    # 5. Complexity (large, highlighted)
    complexity_eq = r'''$\begin{aligned}
        \mathbf{C}_{\text{eq}} &= \textcolor[HTML]{7D6608}{C_{\min}} + (\textcolor[HTML]{7D6608}{C_{\max}}-\textcolor[HTML]{7D6608}{C_{\min}})\,\mathbf{H}\,(0.7+0.3\mathbf{I}) \\
        \frac{d\mathbf{C}}{dt} &= \Bigg[
        \underbrace{-\textcolor[HTML]{7D6608}{\alpha_{C\downarrow}}\max(0,\mathbf{C}-\mathbf{C}_{\text{eq}})\max(0,0.3-B)}_{\text{simplify when above equilibrium}}
        + \underbrace{\textcolor[HTML]{7D6608}{\alpha_{C\uparrow}}\max(0,\mathbf{C}_{\text{eq}}-\mathbf{C})\,B}_{\text{progressive overload}} \\
        &\quad + \text{false-hope pressure} + \text{identity growth}
        \Bigg] \cdot (1+\textcolor[HTML]{1F618D}{\text{social}})
    \end{aligned}$'''

    create_equation_card(
        fig, ax,
        'Behavioral Complexity',
        [('COMPLEX', 'cx'), ('IDENTITY', 'id'), ('EXPECT', 'ex'), ('CONTEXT', 'ct')],
        complexity_eq,
        r'Equilibrium rises with habit and identity. Progressive overload when performing; simplification when overwhelmed.',
        current_y,
        height=0.12,
        highlight_color=COLORS['cx']
    )

    current_y -= 0.14

    # 6. Context decay
    context_eq = r'''$\textcolor[HTML]{1F618D}{\text{stress}} \gets \text{stress}\,(1-0.1\,\Delta t) \qquad
    \textcolor[HTML]{1F618D}{ii} \gets ii\,(1-0.05\,\Delta t) \qquad
    \textcolor[HTML]{1F618D}{\text{social}} \gets \text{social}\,(1-0.003\,\Delta t)$'''

    create_equation_card(
        fig, ax,
        'Transient Context Variables',
        [('CONTEXT', 'ct')],
        context_eq,
        'Multiplicative decay on different time scales (days to months).',
        current_y,
        height=0.09
    )

    # Footer
    ax.text(
        0.5, 0.02,
        r'\textit{A mechanistic model synthesizing habit formation, motivation dynamics, expectation calibration,}',
        ha='center',
        fontsize=9,
        color='#666',
        transform=ax.transAxes
    )

    ax.text(
        0.5, 0.005,
        r'\textit{identity development, and behavioral complexity for understanding behavior change.}',
        ha='center',
        fontsize=9,
        color='#666',
        transform=ax.transAxes
    )

    plt.tight_layout()
    return fig

def create_individual_cards():
    """Create individual high-quality cards for each equation."""

    equations = [
        {
            'name': 'behavioral_trigger',
            'title': 'Behavioral Trigger',
            'tags': [('COMPLEX', 'cx'), ('STATE', 'st'), ('CONTEXT', 'ct')],
            'equation': r'''$\begin{aligned}
                \theta &= \textcolor[HTML]{7D6608}{C}(1-\mathbf{H}) + \textcolor[HTML]{1F618D}{\text{stress}} \cdot 0.3 - \textcolor[HTML]{1F618D}{ii} \\
                B_{\text{goal}} &= \sigma\!\left(\frac{\mathbf{M}-\theta}{\textcolor[HTML]{566573}{\tau}}\right) \quad
                B_{\text{habit}} = \mathbf{H}\,\sigma\!\left(\frac{\mathbf{M}-M_{\text{floor}}}{0.08}\right) \\
                B &= \bigl[(1-\mathbf{H}^{1.5})\,B_{\text{goal}} + \mathbf{H}^{1.5}\,B_{\text{habit}}\bigr]
                \,\sigma\!\left(\frac{\mathbf{M}-0.08}{0.03}\right)
            \end{aligned}$''',
            'description': 'Complexity and stress raise threshold; implementation intentions lower it. Smooth transition from goal-directed to automatic behavior.',
            'highlight': None
        },
        {
            'name': 'motivation',
            'title': 'Motivational Activation',
            'tags': [('REWARD', 'mv'), ('EFFORT', 'ef'), ('COLLAPSE', 'cl'), ('META', 'mt')],
            'equation': r'''$\begin{aligned}
                \frac{d\mathbf{M}}{dt} &=
                -\textcolor[HTML]{C45C26}{\beta_M}\,\frac{\mathbf{M}}{1+\mathbf{M}}
                + \textcolor[HTML]{C45C26}{\gamma}\,B\,(1-\mathbf{H}^2)(1-\mathbf{M}/2)
                - \textcolor[HTML]{5C4D8A}{\lambda}\,\mathbf{C}\,(1-\mathbf{H})\,B \\
                &\quad - \textcolor[HTML]{AF601A}{\gamma_{\text{ind}}}\,F\,(1-\mathbf{H})
                - \textcolor[HTML]{B03A2E}{\kappa}\,\text{sp}(-\mathbf{E}-|E_c|)\,\mathbf{M}
                - \textcolor[HTML]{B03A2E}{\kappa_{\text{wth}}}\,\sigma((\mathbf{E}-E_{\text{wth}})/0.2)\,\mathbf{M} \\
                &\quad + \textcolor[HTML]{566573}{\mu}\,(-d\mathbf{E}/dt)
                + 0.08\max(0, 0.2\mathbf{I}-\mathbf{M})
                + 0.02\,B\,\mathbf{H} + \text{context}
            \end{aligned}$''',
            'description': 'Central dynamics: reward from action, effort cost, fantasy drain, collapse mechanisms, velocity feedback, identity sustenance.',
            'highlight': COLORS['mv']
        },
    ]

    for eq_data in equations:
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

        create_equation_card(
            fig, ax,
            eq_data['title'],
            eq_data['tags'],
            eq_data['equation'],
            eq_data['description'],
            0.15,
            height=0.7,
            highlight_color=eq_data['highlight']
        )

        plt.tight_layout()
        plt.savefig(f'equation_card_{eq_data["name"]}.png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

if __name__ == '__main__':
    print("Creating full visualization...")
    fig = create_full_visualization()
    plt.savefig('nerdfit_equations_matplotlib.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig('nerdfit_equations_matplotlib.pdf', bbox_inches='tight', facecolor='white')
    print("Saved: nerdfit_equations_matplotlib.png and .pdf")

    print("\nCreating individual equation cards...")
    create_individual_cards()
    print("Done!")

    plt.show()
