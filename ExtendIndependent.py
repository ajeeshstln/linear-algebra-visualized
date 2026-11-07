from manim import *
import numpy as np

class ExtendIndependent(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-50 * DEGREES)
        self.add(ThreeDAxes(x_range=[-4, 4], y_range=[-4, 4], z_range=[-3, 3]))

        # W = plane through the origin spanned by p, q
        p = np.array([1.0, 0.0, 0.3])
        q = np.array([0.0, 1.0, 0.2])
        n_hat = np.cross(p, q)
        n_hat = n_hat / np.linalg.norm(n_hat)

        W = Surface(lambda a, b: a * p + b * q,
                    u_range=[-3, 3], v_range=[-3, 3], resolution=(6, 6),
                    fill_opacity=0.25, stroke_opacity=0.25,
                    checkerboard_colors=[BLUE, BLUE])

        al = 1.5 * p                      # alpha in W
        be = 1.5 * q + 0.5 * p            # beta in W (independent of alpha)
        ga = p + q + 2.5 * n_hat          # gamma: above the plane, not in span(S)

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

        def label(tex, pos, color):
            t = MathTex(tex, color=color).move_to(pos)
            self.add_fixed_orientation_mobjects(t)
            return t

        # =============== PART 1: S ∪ {γ} is independent ===============
        caption(r"$W$ is a plane in $\mathbb{R}^3$")
        self.play(FadeIn(W))
        a_arr = Arrow3D(ORIGIN, al, color=YELLOW)
        b_arr = Arrow3D(ORIGIN, be, color=PURPLE)
        a_l = label(r"\alpha", al + 0.3 * OUT, YELLOW)
        b_l = label(r"\beta", be + 0.3 * OUT, PURPLE)
        caption(r"$S=\{\alpha,\beta\}$ is independent, and spans $W$")
        self.play(Create(a_arr), Create(b_arr), FadeIn(a_l), FadeIn(b_l))
        self.wait(1.5)

        g_arr = Arrow3D(ORIGIN, ga, color=ORANGE)
        g_l = label(r"\gamma", ga + 0.3 * OUT, ORANGE)
        drop = DashedLine(ga, ga - 2.5 * n_hat, color=ORANGE)
        caption(r"$\gamma\notin\mathrm{span}(S)$: it sticks out above $W$")
        self.play(Create(g_arr), FadeIn(g_l), Create(drop))
        self.wait(2)

        caption(r"Suppose $c_1\alpha + c_2\beta + b\gamma = 0$. Show $b=c_1=c_2=0$")
        self.wait(3)

        caption(r"If $b\neq 0$: $\gamma = -\frac{c_1}{b}\alpha - \frac{c_2}{b}\beta$")
        w = 0.5 * al + 1.0 * be            # an example combination of alpha, beta
        w_arr = Arrow3D(ORIGIN, w, color=RED)
        w_l = label(r"-\tfrac{c_1}{b}\alpha-\tfrac{c_2}{b}\beta", w + 0.4 * OUT, RED)
        self.play(Create(w_arr), FadeIn(w_l))
        self.wait(2)
        caption(r"That vector lies in $W$, but $\gamma$ does not. Contradiction")
        gap = DashedLine(w, ga, color=WHITE)
        self.play(Create(gap))
        self.wait(3)
        self.play(FadeOut(w_arr), FadeOut(w_l), FadeOut(gap))

        # gamma STAYS on screen from here on
        caption(r"So $b=0$. Then $c_1\alpha + c_2\beta = 0$")
        self.wait(2)
        caption(r"$S$ is independent, so $c_1=c_2=0$")
        self.wait(2.5)
        caption(r"Hence $b=c_1=c_2=0$: $S\cup\{\gamma\}$ is independent")
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()

        # =============== Clear the three vectors, keep W ===============
        self.play(FadeOut(a_arr), FadeOut(b_arr), FadeOut(g_arr),
                  FadeOut(a_l), FadeOut(b_l), FadeOut(g_l), FadeOut(drop))
        self.move_camera(phi=65 * DEGREES, theta=-50 * DEGREES, run_time=2)

        # =============== PART 2: extend to a basis of W ===============
        caption(r"Claim: every independent subset of $W$ extends to a basis of $W$")
        self.wait(3)

        # Step 1: pick one nonzero vector v1 in W (independent)
        v1 = 2 * p + 0.3 * q
        v1_arr = Arrow3D(ORIGIN, v1, color=YELLOW)
        v1_l = label(r"v_1", v1 + 0.3 * OUT, YELLOW)
        caption(r"Pick $v_1\neq 0$ in $W$: $\{v_1\}$ is independent")
        self.play(Create(v1_arr), FadeIn(v1_l))
        self.wait(2)

        # span{v1} = all c*v1 : a line
        L = Line3D(-1.4 * v1, 1.4 * v1, color=ORANGE, thickness=0.03)
        caption(r"$\mathrm{span}\{v_1\}=\{c\,v_1\}$ is only a line, not all of $W$")
        self.play(Create(L), run_time=2)
        self.wait(2)

        # Step 2: choose v2 in W, not in span{v1}
        v2 = -0.5 * p + 1.8 * q
        v2_arr = Arrow3D(ORIGIN, v2, color=PURPLE)
        v2_l = label(r"v_2", v2 + 0.3 * OUT, PURPLE)
        caption(r"Choose $v_2\in W$ with $v_2\notin\mathrm{span}\{v_1\}$")
        self.play(Create(v2_arr), FadeIn(v2_l))
        self.wait(2)
        caption(r"By the result above, $\{v_1,v_2\}$ is independent")
        self.wait(3)

        # Step 3: span{v1, v2} = W
        fam = VGroup(*[
            Line3D(-1.4 * v1 + t * v2, 1.4 * v1 + t * v2,
                   color=ORANGE, thickness=0.02)
            for t in [-1.5, -0.75, 0.75, 1.5]
        ])
        caption(r"Lines $c_1v_1 + t\,v_2$ sweep out the whole plane $W$")
        self.play(Create(fam), run_time=3)
        self.wait(2)
        caption(r"So $\mathrm{span}\{v_1,v_2\}=W$ and $\{v_1,v_2\}$ is independent")
        self.wait(2.5)
        caption(r"Hence $\{v_1,v_2\}$ is a basis of $W$")
        self.wait(3)

        # General statement
        caption(r"In general: if $\mathrm{span}(S)\neq W$, add $\beta\in W\setminus\mathrm{span}(S)$")
        self.wait(3)
        caption(r"$S\cup\{\beta\}$ stays independent, and independent sets in $W$ have at most $\dim V$ elements")
        self.wait(3.5)
        caption(r"So the process stops, and $S$ is part of a basis of $W$")
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)


if __name__ == "__main__":
    config.quality = "low_quality"
    config.preview = True
    ExtendIndependent().render()
