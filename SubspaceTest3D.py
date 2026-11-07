from manim import *
import numpy as np

class SubspaceTest3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)
        axes = ThreeDAxes(x_range=[-6, 6], y_range=[-6, 6], z_range=[-4, 4])
        self.add(axes)

        # W = plane through the origin spanned by p and q
        p = np.array([1, 0, 0.4])
        q = np.array([0, 1, 0.2])
        W = Surface(
            lambda s, t: s * p + t * q,
            u_range=[-5, 5], v_range=[-5, 5], resolution=(8, 8),
            fill_opacity=0.25, stroke_opacity=0.25,
            checkerboard_colors=[BLUE, BLUE],
        )

        alpha_v = 2 * p
        beta_v = 1 * p + 1.5 * q

        self.cap = None
        def caption(text):
            new = Text(text, font_size=24).to_corner(UL)
            self.add_fixed_in_frame_mobjects(new)
            if self.cap is None:
                self.play(Write(new))
            else:
                self.play(FadeOut(self.cap), Write(new))
            self.cap = new

        def label(text, pos, color):
            t = Text(text, font_size=28, color=color).move_to(pos)
            self.add_fixed_orientation_mobjects(t)
            return t

        # Cheap flat arrow (not Arrow3D) with a zero-length guard
        def arrow(start, end, color, width=6):
            start = np.array(start, dtype=float)
            end = np.array(end, dtype=float)
            if np.linalg.norm(end - start) < 0.05:
                end = start + 0.05 * RIGHT        # never zero-length
            return Arrow(start, end, buff=0, color=color, stroke_width=width)

        # Full-width orange line in W through p + s*q, parallel to alpha
        def full_line(s_val):
            return Line(-5.5 * p + s_val * q, 5.5 * p + s_val * q,
                        color=ORANGE, stroke_width=4)

        def stop(*mobs):
            for m in mobs:
                m.clear_updaters()

        # ---------- Step 1: the plane ----------
        caption("W = a plane through the origin")
        self.play(FadeIn(W))
        self.wait(1)

        # ---------- Step 2: alpha and beta ----------
        c = ValueTracker(1)
        ca = lambda: c.get_value() * alpha_v            # c * alpha
        tip = lambda: c.get_value() * alpha_v + beta_v  # c * alpha + beta

        alpha = always_redraw(lambda: arrow(ORIGIN, ca(), YELLOW))
        beta = arrow(ORIGIN, beta_v, PURPLE)
        a_l = label("α", alpha_v + 0.3 * OUT, YELLOW)
        b_l = label("β", beta_v + 0.3 * OUT, PURPLE)
        caption("Pick α and β in W (not parallel, α ≠ 0)")
        self.play(Create(alpha), Create(beta), FadeIn(a_l), FadeIn(b_l))
        self.wait(1)

        # ---------- Step 3: c = 1, parallelogram and diagonal ----------
        para = always_redraw(lambda: Polygon(
            ORIGIN, ca(), tip(), beta_v,
            color=WHITE, fill_color=WHITE, fill_opacity=0.2, stroke_width=1))
        d1 = always_redraw(lambda: DashedLine(ca(), tip(), color=PURPLE))
        d2 = always_redraw(lambda: DashedLine(beta_v, tip(), color=YELLOW))
        diag = always_redraw(lambda: arrow(ORIGIN, tip(), ORANGE))
        s_l = label("α+β", alpha_v + beta_v + 0.3 * OUT, ORANGE)
        caption("c = 1: α + β is the diagonal of the parallelogram")
        self.play(FadeIn(para), Create(d1), Create(d2))
        self.play(Create(diag), FadeIn(s_l))
        self.wait(1.5)

        # ---------- Step 4: scale alpha by c ----------
        caption("Scale α by c: the parallelogram and cα + β grow")
        self.play(FadeOut(a_l), FadeOut(s_l))

        moving = always_redraw(lambda: Dot(tip(), color=ORANGE, radius=0.09))
        trace = TracedPath(lambda: tip(), stroke_color=ORANGE, stroke_width=6)
        self.add(trace, moving)

        self.play(c.animate.set_value(3), run_time=3, rate_func=linear)
        caption("Now c goes negative: the orange line extends the other way")
        self.play(c.animate.set_value(-3.5), run_time=6, rate_func=linear)
        self.play(c.animate.set_value(1), run_time=2)
        self.wait(0.5)

        # Replace the trace with a clean full-width orange line
        stop(moving)
        self.remove(trace, moving)
        base_line = full_line(1.5)
        self.add(base_line)
        caption("All c: cα + β covers a whole line in W, parallel to α")
        self.wait(1)

        # ---------- Step 5: vary beta, the orange line sweeps the plane ----------
        caption("Now move β (violet) across W: the orange line moves with it")
        stop(para, d1, d2, diag, alpha)
        self.play(FadeOut(para), FadeOut(d1), FadeOut(d2),
                  FadeOut(diag), FadeOut(alpha), FadeOut(b_l))
        self.remove(beta)

        s = ValueTracker(1.5)                       # beta = p + s*q
        beta_now = lambda: 1 * p + s.get_value() * q

        alpha_static = arrow(ORIGIN, alpha_v, YELLOW)
        beta_live = always_redraw(lambda: arrow(ORIGIN, beta_now(), PURPLE))
        live_line = always_redraw(lambda: full_line(s.get_value()))
        self.add(alpha_static, beta_live, live_line)
        self.remove(base_line)

        # go to one edge of W
        self.play(s.animate.set_value(-5.5), run_time=2)

        # ONE continuous sweep; copies are dropped as s passes each grid value
        grid = list(np.linspace(-5.5, 5.5, 15))
        state = {"i": 0}
        trail = VGroup()

        def dropper(m):
            while state["i"] < len(grid) and s.get_value() >= grid[state["i"]] - 1e-6:
                m.add(full_line(grid[state["i"]]))
                state["i"] += 1

        trail.add_updater(dropper)
        self.add(trail)
        self.play(s.animate.set_value(5.5), run_time=8, rate_func=linear)
        trail.remove_updater(dropper)
        self.wait(1)

        caption("cα + β never leaves W, so W is closed: a subspace")
        self.begin_ambient_camera_rotation(rate=0.25)
        self.wait(5)


if __name__ == "__main__":
    config.quality = "low_quality"
    config.preview = True
    SubspaceTest3D().render()
