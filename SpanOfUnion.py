from manim import *
import numpy as np

class SpanOfUnion(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-50 * DEGREES)
        axes = ThreeDAxes(x_range=[-6, 6], y_range=[-6, 6], z_range=[-4, 4])
        self.add(axes)

        def show(text):
            t = Text(text, font_size=26).to_corner(UL)
            self.add_fixed_in_frame_mobjects(t)
            return t

        # W1 = entire x-axis, W2 = entire y-axis (drawn long to look infinite)
        w1 = Line3D(np.array([-6, 0, 0]), np.array([6, 0, 0]), color=BLUE, thickness=0.04)
        w2 = Line3D(np.array([0, -6, 0]), np.array([0, 6, 0]), color=GREEN, thickness=0.04)

        t1 = show("W1 = x-axis (a subspace)")
        self.play(Create(w1), Write(t1))
        self.wait(0.5)

        t2 = show("W2 = y-axis (a subspace)")
        self.play(FadeOut(t1), Create(w2), Write(t2))
        self.wait(1)

        # Union = just the two lines
        t3 = show("W1 ∪ W2 = the two lines only")
        self.play(FadeOut(t2), Write(t3))
        self.wait(1)

        # Union is not closed under addition
        p1, p2 = np.array([3, 0, 0]), np.array([0, 2, 0])
        a1 = Arrow3D(ORIGIN, p1, color=BLUE)
        a2 = Arrow3D(ORIGIN, p2, color=GREEN)
        asum = Arrow3D(ORIGIN, p1 + p2, color=YELLOW)
        t4 = show("a1 + a2 leaves the union: not a subspace")
        self.play(FadeOut(t3), Create(a1), Create(a2), Write(t4))
        self.play(Create(asum))
        self.wait(1.5)

        # Smallest subspace containing both = xy-plane = W1 + W2
        plane = Surface(
            lambda u, v: np.array([u, v, 0]),
            u_range=[-6, 6], v_range=[-6, 6],
            resolution=(12, 12),
            fill_opacity=0.3, stroke_opacity=0.2,
            checkerboard_colors=[YELLOW, YELLOW],
        )
        t5 = show("span(W1 ∪ W2) = smallest subspace containing both")
        self.play(FadeOut(t4), FadeIn(plane), Write(t5))
        self.wait(1.5)

        t6 = show("= xy-plane = W1 + W2")
        self.play(FadeOut(t5), Write(t6))

        self.begin_ambient_camera_rotation(rate=0.25)
        self.wait(4)
