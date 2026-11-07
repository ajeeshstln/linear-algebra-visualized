from manim import *
import numpy as np

class DimensionFormula(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)
        axes = ThreeDAxes(x_range=[-4, 4], y_range=[-4, 4], z_range=[-4, 4])
        self.add(axes)

        ex = np.array([1.0, 0, 0])
        ey = np.array([0, 1.0, 0])
        ez = np.array([0, 0, 1.0])

        self.cap = None
        def caption(text):
            new = Tex(text, font_size=32).to_corner(UL)
            if new.width > 9:
                new.scale_to_fit_width(9)
            self.add_fixed_in_frame_mobjects(new)
            if self.cap is None:
                self.play(Write(new))
            else:
                self.play(FadeOut(self.cap), Write(new))
            self.cap = new

        def fixed(mob):
            self.add_fixed_in_frame_mobjects(mob)
            return mob

        def plane(u, v, color, r=3.5):
            return Surface(lambda a, b: a * u + b * v,
                           u_range=[-r, r], v_range=[-r, r], resolution=(6, 6),
                           fill_opacity=0.25, stroke_opacity=0.25,
                           checkerboard_colors=[color, color])

        # Formula (always at the bottom)
        formula = fixed(MathTex(
            r"\dim W_1+\dim W_2=\dim(W_1\cap W_2)+\dim(W_1+W_2)",
            font_size=34).to_edge(DOWN))

        # ================= EXAMPLE 1: x-axis and y-axis =================
        caption(r"Example 1: $W_1$ = $x$-axis, $W_2$ = $y$-axis in $\mathbb{R}^3$")
        w1 = Line3D(-4 * ex, 4 * ex, color=BLUE, thickness=0.04)
        w2 = Line3D(-4 * ey, 4 * ey, color=GREEN, thickness=0.04)
        self.play(Create(w1), Create(w2))
        self.play(Write(formula))
        self.wait(1)

        caption(r"$W_1\cap W_2=\{0\}$, so $\dim(W_1\cap W_2)=0$")
        zero = Dot3D(ORIGIN, color=RED, radius=0.12)
        self.play(FadeIn(zero))
        self.wait(2)

        caption(r"$W_1+W_2$ = all $a\,e_1 + b\,e_2$ = the $xy$-plane, dimension $2$")
        xy = plane(ex, ey, YELLOW)
        self.play(FadeIn(xy), run_time=2)
        self.wait(2)

        nums1 = fixed(MathTex(r"1\;+\;1\;=\;0\;+\;2", font_size=44, color=ORANGE)
                      .next_to(formula, UP))
        caption(r"$\dim W_1=1,\ \dim W_2=1$: the formula holds")
        self.play(Write(nums1))
        self.wait(3)

        self.play(FadeOut(w1), FadeOut(w2), FadeOut(zero), FadeOut(xy), FadeOut(nums1))

        # ================= EXAMPLE 2: two planes =================
        caption(r"Example 2: $W_1$, $W_2$ two non-parallel planes in $\mathbb{R}^3$")
        u2, v2 = ex, ey + ez                       # W2 = span{(1,0,0), (0,1,1)}
        W1 = plane(ex, ey, BLUE)                   # xy-plane
        W2 = plane(u2, v2, GREEN)                  # tilted plane through the x-axis
        self.play(FadeIn(W1), FadeIn(W2), run_time=2)
        self.wait(1)

        caption(r"$\dim W_1 = 2,\ \dim W_2 = 2$")
        self.wait(2)

        caption(r"$W_1\cap W_2$ is a line, so $\dim(W_1\cap W_2)=1$")
        inter = Line3D(-4 * ex, 4 * ex, color=RED, thickness=0.05)
        self.play(Create(inter), run_time=2)
        self.move_camera(phi=80 * DEGREES, theta=-20 * DEGREES, run_time=3)
        self.wait(1.5)

        caption(r"Basis of the intersection: $\{e_1\}$. Extend it in each plane")
        e1_arr = Arrow3D(ORIGIN, 2.5 * ex, color=RED)
        f1 = Arrow3D(ORIGIN, 2.5 * ey, color=BLUE)
        f2 = Arrow3D(ORIGIN, 2.5 * (ey + ez) / np.sqrt(2), color=GREEN)
        self.play(Create(e1_arr))
        self.play(Create(f1), Create(f2))
        self.wait(2)

        caption(r"$\{e_1,f_1,f_2\}$ is independent and spans $W_1+W_2$")
        self.wait(3)

        caption(r"So $W_1+W_2=\mathbb{R}^3$, dimension $3$")
        cube = Cube(side_length=6, fill_opacity=0.08, stroke_opacity=0.3,
                    fill_color=YELLOW)
        self.play(FadeIn(cube), run_time=2)
        self.wait(2)

        nums2 = fixed(MathTex(r"2\;+\;2\;=\;1\;+\;3", font_size=44, color=ORANGE)
                      .next_to(formula, UP))
        caption(r"$2+2=1+3$: the formula holds")
        self.play(Write(nums2))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()

        # ================= WHY IT WORKS =================
        self.play(FadeOut(e1_arr), FadeOut(f1), FadeOut(f2), FadeOut(cube),
                  FadeOut(W1), FadeOut(W2), FadeOut(inter), FadeOut(nums2))
        caption(r"Proof idea: take a basis $\{e_i\}$ of $W_1\cap W_2$")
        self.wait(2.5)
        caption(r"Extend to a basis $\{e_i,f_j\}$ of $W_1$ and $\{e_i,g_k\}$ of $W_2$")
        self.wait(2.5)
        caption(r"Then $\{e_i,f_j,g_k\}$ is a basis of $W_1+W_2$")
        self.wait(2.5)
        caption(r"Count: $(r+s)+(r+t)=r+(r+s+t)$")
        self.wait(3)


if __name__ == "__main__":
    config.quality = "low_quality"
    config.preview = True
    DimensionFormula().render()
