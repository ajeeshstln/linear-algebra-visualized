from manim import *
import numpy as np

class SubspaceTest(MovingCameraScene):
    def construct(self):
        plane = NumberPlane(x_range=[-30, 30, 2], y_range=[-20, 20, 2],
                            background_line_style={"stroke_opacity": 0.15})
        self.add(plane)

        d = np.array([2, 1, 0]) / np.sqrt(5)   # direction of the line W
        W = Line(-30 * d, 30 * d, color=BLUE)
        W_label = Text("W", font_size=30, color=BLUE).move_to(5.5 * d + 0.5 * UP)
        self.play(Create(W), Write(W_label))

        # Caption helper: stays at the top of the camera frame, even after zooming
        self.cap = None
        def caption(text):
            frame = self.camera.frame
            k = frame.width / config.frame_width
            new = Text(text, font_size=24).scale(k)
            new.move_to(frame.get_top() + DOWN * 0.5 * k)
            if self.cap is None:
                self.play(Write(new))
            else:
                self.play(FadeOut(self.cap), Write(new))
            self.cap = new

        # Vanish helper: stop updaters, then fade everything out
        def vanish(*mobs):
            for m in mobs:
                m.clear_updaters()
            self.play(*[FadeOut(m) for m in mobs])

        caption("W is a line through the origin in R²")
        self.wait(1)
        caption("In 2D, α and β on W are always parallel")
        self.wait(1.5)

        # ---------- Statement 1: W is non-empty, pick α ----------
        alpha = Arrow(ORIGIN, 2.5 * d, buff=0, color=YELLOW)
        alpha_l = Text("α", font_size=30, color=YELLOW)
        alpha_l.add_updater(lambda m: m.next_to(alpha.get_end(), UP, buff=0.15))
        caption("W non-empty: pick a vector α in W")
        self.play(Create(alpha), Write(alpha_l))
        self.wait(1.5)
        vanish(alpha, alpha_l)

        # ---------- Statement 2: (-1)α + α = 0, so 0 is in W ----------
        alpha_b = Arrow(ORIGIN, 2.5 * d, buff=0, color=YELLOW)
        alpha_b_l = Text("α", font_size=30, color=YELLOW)
        alpha_b_l.add_updater(lambda m: m.next_to(alpha_b.get_end(), UP, buff=0.15))
        neg = Arrow(ORIGIN, -2.5 * d, buff=0, color=RED)
        neg_l = Text("-α", font_size=30, color=RED)
        neg_l.add_updater(lambda m: m.next_to(neg.get_end(), DOWN, buff=0.15))
        origin = Dot(ORIGIN, color=GREEN, radius=0.12)
        origin_l = Text("0", font_size=28, color=GREEN).next_to(origin, DOWN + RIGHT, buff=0.1)
        caption("c = -1, β = α:  (-1)α + α = 0, so 0 is in W")
        self.play(Create(alpha_b), Write(alpha_b_l))
        self.play(Create(neg), Write(neg_l))
        self.play(FadeIn(origin), Write(origin_l))
        self.wait(1.5)
        vanish(alpha_b, alpha_b_l, neg, neg_l, origin, origin_l)

        # ---------- Statement 3: β = 0 is in W, so cα is in W ----------
        c = ValueTracker(1)
        def cval():
            v = c.get_value()
            if abs(v) < 0.05:                 # avoid a zero-length arrow
                v = 0.05 if v >= 0 else -0.05
            return v

        c_alpha = always_redraw(
            lambda: Arrow(ORIGIN, cval() * 2.5 * d, buff=0, color=ORANGE))
        c_lbl = always_redraw(
            lambda: Text(f"cα,  c = {c.get_value():.1f}", font_size=24, color=ORANGE)
            .next_to(c_alpha.get_end(), DOWN + RIGHT, buff=0.15))

        caption("β = 0 is in W, so cα = cα + 0 is in W")
        self.add(c_alpha, c_lbl)
        self.play(c.animate.set_value(2.2), run_time=2, rate_func=linear)
        self.play(c.animate.set_value(-1), run_time=4, rate_func=linear)
        caption("c = -1:  -α = (-1)α + 0 is in W")
        self.wait(1)
        self.play(c.animate.set_value(1), run_time=2, rate_func=linear)
        self.wait(0.5)
        vanish(c_alpha, c_lbl)

        # ---------- Statement 4: tip-to-tail addition, all on W ----------
        alpha2 = Arrow(ORIGIN, 2.5 * d, buff=0, color=YELLOW, stroke_width=10,
                       max_stroke_width_to_length_ratio=100).set_z_index(2)
        alpha2_l = Text("α", font_size=30, color=YELLOW)
        alpha2_l.add_updater(lambda m: m.next_to(alpha2.get_end(), DOWN, buff=0.2))
        beta2 = Arrow(ORIGIN, 1.5 * d, buff=0, color=PURPLE, stroke_width=6,
                      max_stroke_width_to_length_ratio=100).set_z_index(3)
        beta2_l = Text("β", font_size=30, color=PURPLE)
        beta2_l.add_updater(lambda m: m.next_to(beta2.get_center(), UP, buff=0.2))

        caption("Take α and β, both starting at the origin")
        self.play(Create(alpha2), Write(alpha2_l))
        self.play(Create(beta2), Write(beta2_l))
        self.wait(1)

        caption("Slide β so its tail sits at the head of α")
        self.play(beta2.animate.shift(2.5 * d), run_time=2)
        self.wait(1)

        sum_arrow = Arrow(ORIGIN, 4 * d, buff=0, color=ORANGE, stroke_width=14,
                          max_stroke_width_to_length_ratio=100).set_z_index(1)
        total = Dot(4 * d, color=WHITE, radius=0.1).set_z_index(4)
        total_l = Text("α + β", font_size=24, color=ORANGE)
        total_l.add_updater(lambda m: m.next_to(total, DOWN + RIGHT, buff=0.2))
        caption("α + β: from the origin to the head of β. It stays in W")
        self.play(Create(sum_arrow))
        self.play(FadeIn(total), Write(total_l))
        self.wait(2)
        vanish(alpha2, alpha2_l, beta2, beta2_l, sum_arrow, total, total_l)

        # ---------- Statement 5: vary c, the head of cα + β slides along W ----------
        caption("Vary c: the head of cα + β slides along W")
        k = ValueTracker(1)

        def coef():                       # position of the head along W (cα + β, β fixed)
            v = k.get_value() * 2.5 + 1.5
            if abs(v) < 0.05:             # avoid a zero-length arrow
                v = 0.05
            return v

        sweep_vec = always_redraw(lambda: Arrow(
            ORIGIN, coef() * d, buff=0, color=ORANGE, stroke_width=8,
            max_stroke_width_to_length_ratio=100))
        moving_dot = always_redraw(lambda: Dot(coef() * d, color=ORANGE, radius=0.12))
        c_live = always_redraw(
            lambda: Text(f"c = {k.get_value():.1f}", font_size=24, color=ORANGE)
            .next_to(moving_dot, UP, buff=0.25))
        trace = TracedPath(moving_dot.get_center, stroke_color=ORANGE, stroke_width=8)
        self.add(trace, sweep_vec, moving_dot, c_live)

        self.play(k.animate.set_value(-13), run_time=3)      # c decreases: head moves down
        self.play(
            k.animate.set_value(13),                          # c increases: head moves up
            self.camera.frame.animate.scale(3),
            run_time=7,
            rate_func=linear,
        )
        caption("Every point of W is cα + β: W is closed")
        self.wait(1)

        # Remove the vector, dot and label; keep the orange sweep
        vanish(sweep_vec, moving_dot, c_live)
        trace.clear_updaters()

        sweep_line = Line(-30 * d, 30 * d, color=ORANGE, stroke_width=8)
        self.play(FadeIn(sweep_line), run_time=1)
        self.wait(3)


if __name__ == "__main__":
    config.quality = "low_quality"
    config.preview = True
    SubspaceTest().render()
