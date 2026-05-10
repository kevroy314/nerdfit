"""
Manim animation for Nerdfit behavioral dynamics equations.
Renders color-coded equations with flow and dependencies.

Usage:
  manim -pql manim_equations.py ColorKeyScene
  manim -pql manim_equations.py BehavioralTriggerScene
  manim -pql manim_equations.py MotivationScene
  manim -pqh manim_equations.py FullDynamicsScene  # High quality full animation
"""

from manim import *

# Phenomenon color palette (matching LaTeX)
COLORS = {
    'st': '#1B2631',      # state variables
    'hb': '#1B7F6A',      # habit & automaticity
    'mv': '#C45C26',      # motivation & reward
    'ef': '#5C4D8A',      # effort / opportunity cost
    'ex': '#6B4C9A',      # expectation excess & calibration
    'id': '#2874A6',      # identity & self-concept
    'cx': '#7D6608',      # behavioral complexity
    'fn': '#AF601A',      # fantasy / indulgence
    'cl': '#B03A2E',      # collapse & disinhibition
    'ct': '#1F618D',      # context
    'mt': '#566573',      # meta-control
}

class ColorKeyScene(Scene):
    """Display the color key for all phenomena."""

    def construct(self):
        # Title
        title = Text("Nerdfit Behavioral Dynamics", font_size=48, weight=BOLD)
        subtitle = Text("Color-Coded Mechanistic Model", font_size=28, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.3)

        self.play(Write(title), Write(subtitle))
        self.wait()
        self.play(
            title.animate.scale(0.7).to_edge(UP),
            subtitle.animate.scale(0.7).next_to(title.scale(0.7), DOWN, buff=0.2).to_edge(UP)
        )

        # Color key
        phenomena = [
            ('st', 'STATE', 'State variables H, M, E, I, C'),
            ('hb', 'HABIT', 'Habit & automaticity'),
            ('mv', 'REWARD', 'Motivation & reward'),
            ('ef', 'EFFORT', 'Effort / opportunity cost'),
            ('ex', 'EXPECT', 'Expectation dynamics'),
            ('id', 'IDENTITY', 'Identity & self-concept'),
            ('cx', 'COMPLEX', 'Behavioral complexity'),
            ('fn', 'FANTASY', 'Fantasy / indulgence'),
            ('cl', 'COLLAPSE', 'Collapse & disinhibition'),
            ('ct', 'CONTEXT', 'Context (stress, social, plans)'),
            ('mt', 'META', 'Meta-control & gating'),
        ]

        legend_items = VGroup()
        for color_key, label, description in phenomena:
            # Color box
            box = Rectangle(
                width=0.3, height=0.3,
                fill_color=COLORS[color_key],
                fill_opacity=1,
                stroke_width=0
            )

            # Label
            tag = Text(label, font_size=16, weight=BOLD, color=WHITE)
            tag.move_to(box)

            # Description
            desc = Text(description, font_size=20, color=WHITE)
            desc.next_to(box, RIGHT, buff=0.3)

            item = VGroup(box, tag, desc)
            legend_items.add(item)

        # Arrange in two columns
        left_col = VGroup(*legend_items[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        right_col = VGroup(*legend_items[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        legend = VGroup(left_col, right_col).arrange(RIGHT, buff=2, aligned_edge=UP)
        legend.next_to(subtitle, DOWN, buff=1)

        # Animate legend
        for item in legend_items:
            self.play(FadeIn(item, shift=UP), run_time=0.3)

        self.wait(2)


class BehavioralTriggerScene(Scene):
    """Animate the behavioral trigger equation."""

    def construct(self):
        title = Text("Behavioral Trigger", font_size=40, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))

        # Step 1: Threshold
        theta_label = Text("Threshold θ", font_size=28, color=COLORS['cx']).shift(UP*2)
        self.play(FadeIn(theta_label))

        theta_eq = MathTex(
            r"\theta", "=",
            r"C", r"(1-", r"H", r")",
            "+", r"\text{stress}", r"\cdot 0.3\,(1-", r"H", r")",
            "-", r"ii"
        ).scale(0.9)

        # Color coding
        theta_eq[0].set_color(COLORS['cx'])
        theta_eq[2].set_color(COLORS['cx'])  # C
        theta_eq[4].set_color(COLORS['st'])  # H
        theta_eq[7].set_color(COLORS['ct'])  # stress
        theta_eq[9].set_color(COLORS['st'])  # H
        theta_eq[12].set_color(COLORS['ct'])  # ii

        theta_eq.next_to(theta_label, DOWN, buff=0.5)
        self.play(Write(theta_eq))

        # Annotations
        complexity_note = Text(
            "Complexity raises threshold",
            font_size=18,
            color=COLORS['cx']
        ).next_to(theta_eq, DOWN, buff=0.3, aligned_edge=LEFT)

        stress_note = Text(
            "Stress adds extra threshold",
            font_size=18,
            color=COLORS['ct']
        ).next_to(complexity_note, DOWN, buff=0.2, aligned_edge=LEFT)

        ii_note = Text(
            "Implementation intentions lower it",
            font_size=18,
            color=COLORS['ct']
        ).next_to(stress_note, DOWN, buff=0.2, aligned_edge=LEFT)

        self.play(
            FadeIn(complexity_note),
            FadeIn(stress_note),
            FadeIn(ii_note),
            run_time=2
        )
        self.wait()

        # Step 2: Goal-directed behavior
        self.play(
            FadeOut(complexity_note),
            FadeOut(stress_note),
            FadeOut(ii_note)
        )

        b_goal_eq = MathTex(
            r"B_{\text{goal}}", "=", r"\sigma\left(\frac{",
            r"M", "-", r"\theta", "}{", r"\tau", r"}\right)"
        ).scale(0.9)

        b_goal_eq[0].set_color(COLORS['st'])
        b_goal_eq[3].set_color(COLORS['st'])  # M
        b_goal_eq[5].set_color(COLORS['cx'])  # theta
        b_goal_eq[7].set_color(COLORS['mt'])  # tau

        b_goal_eq.next_to(theta_eq, DOWN, buff=0.8)
        self.play(Write(b_goal_eq))

        goal_note = Text(
            "Motivated behavior requires M > θ",
            font_size=20,
            color=COLORS['mv']
        ).next_to(b_goal_eq, DOWN, buff=0.3)

        self.play(FadeIn(goal_note))
        self.wait()

        # Step 3: Habitual behavior
        self.play(FadeOut(goal_note))

        b_habit_eq = MathTex(
            r"B_{\text{habit}}", "=",
            r"H", r"\,\sigma\left(\frac{",
            r"M", r"- M_{\text{floor}}}{0.08}\right)"
        ).scale(0.9)

        b_habit_eq[0].set_color(COLORS['hb'])
        b_habit_eq[2].set_color(COLORS['st'])  # H
        b_habit_eq[4].set_color(COLORS['st'])  # M

        b_habit_eq.next_to(b_goal_eq, DOWN, buff=0.6)
        self.play(Write(b_habit_eq))

        habit_note = Text(
            "Automatic drive scales with habit strength",
            font_size=20,
            color=COLORS['hb']
        ).next_to(b_habit_eq, DOWN, buff=0.3)

        self.play(FadeIn(habit_note))
        self.wait()

        # Step 4: Blend
        self.play(FadeOut(habit_note))

        blend_eq = MathTex(
            r"\text{blend}", "=", r"H^{1.5}"
        ).scale(0.9)
        blend_eq[2].set_color(COLORS['st'])

        b_raw_eq = MathTex(
            r"B_{\text{raw}}", "=",
            r"(1-\text{blend})\,", r"B_{\text{goal}}",
            "+", r"\text{blend}\,", r"B_{\text{habit}}"
        ).scale(0.9)

        b_raw_eq[3].set_color(COLORS['mv'])
        b_raw_eq[6].set_color(COLORS['hb'])

        blend_group = VGroup(blend_eq, b_raw_eq).arrange(DOWN, buff=0.4)
        blend_group.next_to(b_habit_eq, DOWN, buff=0.8)

        self.play(Write(blend_eq))
        self.wait(0.5)
        self.play(Write(b_raw_eq))

        transition_note = Text(
            "Smooth transition from goal-directed to automatic",
            font_size=20,
            color=YELLOW
        ).next_to(blend_group, DOWN, buff=0.3)

        self.play(FadeIn(transition_note))
        self.wait(2)


class MotivationScene(Scene):
    """Animate the motivation equation showing different components."""

    def construct(self):
        title = Text("Motivational Activation", font_size=40, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))

        # Main equation
        eq_label = MathTex(r"\frac{dM}{dt} =").scale(1.2)
        eq_label[0][1].set_color(COLORS['st'])  # M
        eq_label.shift(UP*2.5 + LEFT*5)

        self.play(Write(eq_label))

        # Components to add sequentially
        components = [
            {
                'tex': r"-\beta_M \frac{M}{1+M}",
                'label': "Natural decay",
                'color': COLORS['mv'],
                'highlight': [0, 2, 4]  # beta_M, M, M
            },
            {
                'tex': r"+\gamma\,B\,(1-H^2)(1-M/2)",
                'label': "Reward from action",
                'color': COLORS['mv'],
                'highlight': [0, 2, 6]  # gamma, B, M
            },
            {
                'tex': r"-\lambda\,C\,(1-H)\,B",
                'label': "Effort cost",
                'color': COLORS['ef'],
                'highlight': [0, 2, 4]  # lambda, C, H
            },
            {
                'tex': r"-\gamma_{\text{ind}}\,F\,(1-H)",
                'label': "Fantasy drain",
                'color': COLORS['fn'],
                'highlight': [0, 2]  # gamma_ind, F
            },
            {
                'tex': r"-\kappa\,\text{sp}(-E-|E_c|)\,M",
                'label': "False-hope collapse",
                'color': COLORS['cl'],
                'highlight': [0, 3, 6]  # kappa, E, M
            },
        ]

        current_y = 2
        equation_parts = []

        for i, comp in enumerate(components):
            # Create equation part
            eq_part = MathTex(comp['tex']).scale(0.8)

            # Color highlights
            for idx in comp['highlight']:
                if idx < len(eq_part[0]):
                    eq_part[0][idx].set_color(comp['color'])

            eq_part.next_to(eq_label, RIGHT, buff=0.3)
            if equation_parts:
                eq_part.next_to(equation_parts[-1], DOWN, aligned_edge=LEFT, buff=0.3)

            # Label
            label = Text(comp['label'], font_size=18, color=comp['color'])
            label.next_to(eq_part, RIGHT, buff=0.5)

            # Animate
            self.play(
                Write(eq_part),
                FadeIn(label, shift=LEFT),
                run_time=1
            )

            equation_parts.append(eq_part)
            current_y -= 0.5

            self.wait(0.5)

        # Summary
        summary = Text(
            "Motivation balances reward, cost, and collapse dynamics",
            font_size=24,
            color=YELLOW
        ).to_edge(DOWN, buff=0.5)

        self.play(FadeIn(summary))
        self.wait(2)


class FullDynamicsScene(Scene):
    """Complete animation showing all state variables and their interactions."""

    def construct(self):
        # Title sequence
        title = Text("Nerdfit Behavioral Dynamics", font_size=52, weight=BOLD)
        subtitle = Text("A Mechanistic Model of Behavior Change", font_size=28, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.3)

        self.play(
            Write(title),
            FadeIn(subtitle, shift=UP),
            run_time=2
        )
        self.wait()

        self.play(
            FadeOut(title),
            FadeOut(subtitle)
        )

        # State variables
        state_title = Text("State Variables", font_size=40, weight=BOLD).to_edge(UP)
        self.play(Write(state_title))

        states = [
            (r"H", "Habit Strength", COLORS['hb']),
            (r"M", "Motivation", COLORS['mv']),
            (r"E", "Expectation Excess", COLORS['ex']),
            (r"I", "Identity Coherence", COLORS['id']),
            (r"C", "Behavioral Complexity", COLORS['cx']),
        ]

        state_boxes = VGroup()
        for var, name, color in states:
            box = Rectangle(
                width=2, height=0.8,
                fill_color=color,
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=2
            )

            var_label = MathTex(r"\mathbf{" + var + r"}", color=WHITE, font_size=48)
            name_label = Text(name, font_size=16, color=WHITE)
            name_label.next_to(var_label, DOWN, buff=0.1)

            var_label.move_to(box)
            name_label.move_to(box).shift(DOWN*0.25)

            state_box = VGroup(box, var_label, name_label)
            state_boxes.add(state_box)

        state_boxes.arrange(RIGHT, buff=0.5).shift(DOWN*0.5)

        # Animate state variables appearing
        for box in state_boxes:
            self.play(FadeIn(box, scale=0.8), run_time=0.5)

        self.wait()

        # Show dependencies with arrows
        dependency_label = Text(
            "Dependencies & Feedback Loops",
            font_size=32,
            color=YELLOW
        ).next_to(state_boxes, DOWN, buff=1)

        self.play(FadeIn(dependency_label))

        # Draw some key arrows
        arrows = []

        # H -> M (habit maintenance)
        arrow_h_m = Arrow(
            state_boxes[0].get_bottom(),
            state_boxes[1].get_bottom(),
            color=COLORS['hb'],
            buff=0.1,
            stroke_width=3
        ).shift(DOWN*0.5)
        arrows.append(('hb', arrow_h_m, "Habit → Motivation"))

        # M -> H (practice builds habit)
        arrow_m_h = Arrow(
            state_boxes[1].get_top(),
            state_boxes[0].get_top(),
            color=COLORS['mv'],
            buff=0.1,
            stroke_width=3
        ).shift(UP*0.3)
        arrows.append(('mv', arrow_m_h, "Action → Habit"))

        # E -> M (expectation collapse)
        arrow_e_m = CurvedArrow(
            state_boxes[2].get_left(),
            state_boxes[1].get_right(),
            color=COLORS['cl'],
            stroke_width=3
        )
        arrows.append(('cl', arrow_e_m, "Expectation collapse"))

        # I -> H (identity raises ceiling)
        arrow_i_h = CurvedArrow(
            state_boxes[3].get_left() + DOWN*0.2,
            state_boxes[0].get_right() + DOWN*0.2,
            color=COLORS['id'],
            stroke_width=3,
            angle=-TAU/6
        )
        arrows.append(('id', arrow_i_h, "Identity ceiling"))

        # C -> M (complexity as effort cost)
        arrow_c_m = Arrow(
            state_boxes[4].get_left() + UP*0.1,
            state_boxes[1].get_right() + UP*0.1,
            color=COLORS['ef'],
            buff=0.1,
            stroke_width=3
        )
        arrows.append(('ef', arrow_c_m, "Complexity cost"))

        for color_key, arrow, label_text in arrows:
            label = Text(label_text, font_size=14, color=COLORS[color_key])
            label.next_to(arrow, UP, buff=0.1)

            self.play(
                GrowArrow(arrow),
                FadeIn(label),
                run_time=0.8
            )
            self.wait(0.3)

        self.wait(2)

        # Final message
        final_text = Text(
            "A complex system with rich emergent dynamics",
            font_size=28,
            color=YELLOW,
            weight=BOLD
        ).to_edge(DOWN)

        self.play(FadeIn(final_text, shift=UP))
        self.wait(3)


# Render all scenes
if __name__ == "__main__":
    # This allows running: python manim_equations.py
    import os
    os.system("manim -pql manim_equations.py ColorKeyScene")
