from manim import *
import numpy as np

class SpanAsIntersection(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)
        axes = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3])
        self.add(axes)

        # Caption helper (fixed on screen)
        self.cap = None
        def caption(text):
            new = Text(text, font_size=24).to_corner(UL)
            self.add_fixed_in_frame_mobjects(new)
            if self.cap is None:
                self.play(Write(new))
            else:
                self.play(FadeOut(self.cap), Write(new))
            self.cap = new

        # ---------- S = {s}, s = (1, 1, 1) ----------
        s = np.array([1.0, 1.0, 1.0])
        s_hat = s / np.linalg.norm(s)
        e1 = np.array([1.0, -1.0, 0.0]) / np.sqrt(2)   # perpendicular to s
        e2 = np.cross(s_hat, e1)                        # perpendicular to s and e1

        s_arrow = Arrow3D(ORIGIN, s, color=YELLOW)
        s_label = Text("s = (1,1,1)", font_size=26, color=YELLOW).move_to(s + 0.5 * OUT)
        self.add_fixed_orientation_mobjects(s_label)
        caption("S = {s}, with s = (1, 1, 1)")
        self.play(Create(s_arrow), FadeIn(s_label))
        self.wait(1)

        # ---------- Planes (subspaces) containing s ----------
        # Each plane = span{s, u}, where u rotates around the line through s
        colors = [BLUE, GREEN, RED, PURPLE, TEAL, GOLD]
        planes = []
        for i, col in enumerate(colors):
            th = i * 30 * DEGREES                      # 0, 30, ..., 150 degrees
            u = np.cos(th) * e1 + np.sin(th) * e2
            plane = Surface(
                lambda a, b, u=u: a * s_hat + b * u,
                u_range=[-3, 3], v_range=[-3, 3], resolution=(6, 6),
                fill_opacity=0.22, stroke_opacity=0.2,
                checkerboard_colors=[col, col],
            )
            planes.append(plane)

        caption("Subspaces containing s: planes through the origin and s")
        for p in planes:
            self.play(FadeIn(p), run_time=0.8)
        self.begin_ambient_camera_rotation(rate=0.25)
        self.wait(3)
        caption("(Using every such plane would fill a solid cylinder, so we show a few)")
        self.wait(2)
        self.stop_ambient_camera_rotation()

        # ---------- Intersection of all of them ----------
        caption("Intersection of subspaces is a subspace: it contains 0, closed under cα+β")
        self.wait(2)
        self.play(*[p.animate.set_opacity(0.08) for p in planes], run_time=1.5)

        inter = Line3D(-3 * s_hat * 1.2, 3 * s_hat * 1.2, color=YELLOW, thickness=0.04)
        caption("All the planes meet only along one line: the intersection = span(S)")
        self.play(Create(inter), run_time=2)

        # Turn the camera to look at the line from the side, so its full length shows
        self.move_camera(phi=85 * DEGREES, theta=-45 * DEGREES, run_time=3)
        self.wait(2)

        # ---------- It equals L(S) = { c s } ----------
        self.play(FadeOut(*planes), run_time=1.5)
        caption("L(S) = all linear combinations of S = all scalings c·s")
        c = ValueTracker(1)

        def cs():
            v = c.get_value()
            if abs(v) < 0.03:                  # avoid a zero-length line
                v = 0.03
            return v * s

        cs_line = always_redraw(lambda: Line3D(ORIGIN, cs(), color=ORANGE, thickness=0.05))
        cs_head = always_redraw(lambda: Dot3D(cs(), color=ORANGE, radius=0.12))
        trace = TracedPath(cs_head.get_center, stroke_color=ORANGE, stroke_width=6)
        self.add(trace, cs_line, cs_head)

        self.play(c.animate.set_value(1.7), run_time=2, rate_func=linear)
        self.play(c.animate.set_value(-1.7), run_time=5, rate_func=linear)
        self.play(c.animate.set_value(0), run_time=2, rate_func=linear)
        self.wait(0.5)

        # Orange line sits exactly on the intersection line
        for m in (cs_line, cs_head):
            m.clear_updaters()
        self.play(FadeOut(cs_line), FadeOut(cs_head))
        trace.clear_updaters()
        orange = Line3D(-3.6 * s_hat, 3.6 * s_hat, color=ORANGE, thickness=0.05)
        self.play(FadeIn(orange), FadeOut(inter), run_time=1.5)

        caption("span(S) = ∩ of subspaces ⊇ S = L(S) = { c·s }")
        self.begin_ambient_camera_rotation(rate=0.25)
        self.wait(5)


if __name__ == "__main__":
    config.quality = "low_quality"
    config.preview = True
    SpanAsIntersection().render()
