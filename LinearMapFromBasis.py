from manim import *
import numpy as np

class LinearMapFromBasis(Scene):
    def construct(self):
        # ---------- helpers ----------
        self.cap = None
        def caption(text):
            new = Tex(text, font_size=32).to_edge(UP)
            if new.width > 12.5:
                new.scale_to_fit_width(12.5)
            if self.cap is None:
                self.play(Write(new))
            else:
                self.play(FadeOut(self.cap), Write(new))
            self.cap = new

        def arrow(a, b, color, w=7):
            a, b = np.array(a, float), np.array(b, float)
            if np.linalg.norm(b - a) < 0.05:          # never zero-length
                b = a + 0.05 * RIGHT
            return Arrow(a, b, buff=0, color=color, stroke_width=w,
                         max_stroke_width_to_length_ratio=100)

        # =====================================================
        # PART 1: side by side, V = R^2 (left), W = line (right)
        # =====================================================
        lp = NumberPlane(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                         x_length=5, y_length=5,
                         background_line_style={"stroke_opacity": 0.25}
                         ).shift(LEFT * 3.5 + DOWN * 0.4)
        rp = NumberPlane(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                         x_length=5, y_length=5,
                         background_line_style={"stroke_opacity": 0.25}
                         ).shift(RIGHT * 3.5 + DOWN * 0.4)
        L = lambda x, y: lp.c2p(x, y)
        R = lambda x, y: rp.c2p(x, y)

        lt = MathTex(r"V=\mathbb{R}^2", font_size=34).next_to(lp, UP, buff=0.1)
        rt = MathTex(r"W=\mathrm{span}\{(1,1)\}", font_size=34).next_to(rp, UP, buff=0.1)
        W_line = Line(R(-3, -3), R(3, 3), color=BLUE, stroke_width=6)

        # ---- statement of the theorem ----
        caption(r"Theorem: a linear map is determined by its values on a basis")
        self.wait(2)
        caption(r"$V=\mathbb{R}^2$ with ordered basis $\alpha_1=(1,0),\ \alpha_2=(0,1)$")
        self.play(Create(lp), Write(lt))
        a1 = arrow(L(0, 0), L(1, 0), RED)
        a2 = arrow(L(0, 0), L(0, 1), GREEN)
        a1_l = MathTex(r"\alpha_1", color=RED, font_size=30).next_to(L(1, 0), DOWN, buff=0.1)
        a2_l = MathTex(r"\alpha_2", color=GREEN, font_size=30).next_to(L(0, 1), LEFT, buff=0.1)
        self.play(Create(a1), Create(a2), Write(a1_l), Write(a2_l))
        self.wait(1.5)

        caption(r"$W$ is a line through the origin, $W=\mathrm{span}\{(1,1)\}$")
        self.play(Create(rp), Write(rt))
        self.play(Create(W_line))
        self.wait(1.5)

        caption(r"Take any $\beta_1,\beta_2\in W$: here $\beta_1=(1,1),\ \beta_2=(-1,-1)$")
        b1 = arrow(R(0, 0), R(1, 1), RED)
        b2 = arrow(R(0, 0), R(-1, -1), GREEN)
        b1_l = MathTex(r"\beta_1", color=RED, font_size=30).next_to(R(1, 1), UP + LEFT, buff=0.1)
        b2_l = MathTex(r"\beta_2", color=GREEN, font_size=30).next_to(R(-1, -1), DOWN + RIGHT, buff=0.1)
        self.play(Create(b1), Create(b2), Write(b1_l), Write(b2_l))
        self.wait(2)

        caption(r"Claim: exactly one linear $T:V\to W$ with $T\alpha_1=\beta_1,\ T\alpha_2=\beta_2$")
        self.wait(3)

        # ---- existence ----
        caption(r"Existence: every $(x,y)\in V$ is $x\alpha_1+y\alpha_2$, with unique $x,y$")
        x = ValueTracker(1)
        y = ValueTracker(1)
        v_dot = always_redraw(lambda: Dot(L(x.get_value(), y.get_value()), color=YELLOW, radius=0.1))
        v_arr = always_redraw(lambda: arrow(L(0, 0), L(x.get_value(), y.get_value()), YELLOW, 6))
        v_lab = MathTex(r"(x,y)", color=YELLOW, font_size=30)
        v_lab.add_updater(lambda m: m.next_to(v_dot, UP + RIGHT, buff=0.1))
        self.play(Create(v_arr), Create(v_dot), Write(v_lab))
        self.wait(1.5)

        def tv():
            s = x.get_value() - y.get_value()          # x*beta1 + y*beta2
            return R(s, s)
        Tv_dot = always_redraw(lambda: Dot(tv(), color=ORANGE, radius=0.1))
        Tv_arr = always_redraw(lambda: arrow(R(0, 0), tv(), ORANGE, 6))
        Tv_lab = MathTex(r"T(x,y)", color=ORANGE, font_size=30)
        Tv_lab.add_updater(lambda m: m.next_to(Tv_dot, DOWN + RIGHT, buff=0.1))

        caption(r"Define $T(x\alpha_1+y\alpha_2)=x\beta_1+y\beta_2=(x-y)(1,1)$")
        self.play(Create(Tv_arr), Create(Tv_dot), Write(Tv_lab))
        for (xx, yy) in [(2, 1), (-1, 1.5), (1.5, -1), (1, 1)]:
            self.play(x.animate.set_value(xx), y.animate.set_value(yy),
                      run_time=2.5, rate_func=smooth)
            self.wait(0.3)

        caption(r"$T\alpha_1=\beta_1$ and $T\alpha_2=\beta_2$: check $(x,y)=(1,0)$ and $(0,1)$")
        self.play(x.animate.set_value(1), y.animate.set_value(0), run_time=2)
        self.wait(1.5)
        self.play(x.animate.set_value(0), y.animate.set_value(1), run_time=2)
        self.wait(1.5)

        caption(r"$T$ is linear: $T(cu+w)=cT(u)+T(w)$, since $x,y$ depend linearly on $v$")
        self.wait(3.5)

        # ---- uniqueness ----
        caption(r"Uniqueness: let $U$ be linear with $U\alpha_1=\beta_1,\ U\alpha_2=\beta_2$")
        self.play(x.animate.set_value(1.5), y.animate.set_value(0.5), run_time=2)
        self.wait(2.5)
        caption(r"$U(x,y)=xU\alpha_1+yU\alpha_2=x\beta_1+y\beta_2=T(x,y)$")
        self.wait(3.5)
        caption(r"True for every $(x,y)$, so $U=T$: exactly one such map")
        self.wait(3.5)

        # ---- different values on the basis ----
        self.play(FadeOut(Tv_arr), FadeOut(Tv_dot), FadeOut(Tv_lab),
                  FadeOut(b1), FadeOut(b2), FadeOut(b1_l), FadeOut(b2_l))
        Tv_arr.clear_updaters(); Tv_dot.clear_updaters(); Tv_lab.clear_updaters()

        caption(r"Choose other values: $T'\alpha_1=(-1,-1),\ T'\alpha_2=(1,1)$")
        c1 = arrow(R(0, 0), R(-1, -1), RED)
        c2 = arrow(R(0, 0), R(1, 1), GREEN)
        c1_l = MathTex(r"T'\alpha_1", color=RED, font_size=28).next_to(R(-1, -1), DOWN + RIGHT, buff=0.1)
        c2_l = MathTex(r"T'\alpha_2", color=GREEN, font_size=28).next_to(R(1, 1), UP + LEFT, buff=0.1)
        self.play(Create(c1), Create(c2), Write(c1_l), Write(c2_l))
        self.wait(2)

        def tpv():
            s = -x.get_value() + y.get_value()
            return R(s, s)
        Tp_dot = always_redraw(lambda: Dot(tpv(), color=PURPLE, radius=0.1))
        Tp_arr = always_redraw(lambda: arrow(R(0, 0), tpv(), PURPLE, 6))
        Tp_lab = MathTex(r"T'(x,y)", color=PURPLE, font_size=30)
        Tp_lab.add_updater(lambda m: m.next_to(Tp_dot, UP + RIGHT, buff=0.1))
        caption(r"Same recipe: $T'(x,y)=x(-1,-1)+y(1,1)=(y-x)(1,1)$")
        self.play(Create(Tp_arr), Create(Tp_dot), Write(Tp_lab))
        for (xx, yy) in [(2, 1), (-1, 1.5), (1.5, -1), (1, 1)]:
            self.play(x.animate.set_value(xx), y.animate.set_value(yy),
                      run_time=2.5, rate_func=smooth)
            self.wait(0.3)
        caption(r"Different values on the basis give a different map: $T'=-T$")
        self.wait(3)
        caption(r"Each choice of $\beta_1,\beta_2$ gives exactly one linear map")
        self.wait(3)

        # ---- clear Part 1 ----
        for m in list(self.mobjects):
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.cap = None

        # =====================================================
        # PART 2: the whole transformation on the grid
        # =====================================================
        T = [[1, -1], [1, -1]]       # columns = T(alpha1), T(alpha2)
        Tp = [[-1, 1], [-1, 1]]      # swapped images

        def make_grid():
            return NumberPlane(x_range=[-8, 8, 1], y_range=[-5, 5, 1],
                               background_line_style={"stroke_opacity": 0.6,
                                                      "stroke_color": BLUE_D})
        ref = NumberPlane(x_range=[-8, 8, 1], y_range=[-5, 5, 1],
                          background_line_style={"stroke_opacity": 0.12})
        grid = make_grid()
        Wl = Line(np.array([-8, -8, 0]), np.array([8, 8, 0]),
                  color=YELLOW, stroke_width=5)
        Wlab = MathTex(r"W=\mathrm{span}\{(1,1)\}", color=YELLOW,
                       font_size=30).move_to([3.5, 2.3, 0])

        caption(r"Now see $T$ on all of $V$: draw $V=\mathbb{R}^2$ as a grid")
        self.add(ref)
        self.play(Create(grid))
        self.wait(1.5)

        caption(r"$W$ is the line $y=x$")
        self.play(Create(Wl), Write(Wlab))
        self.wait(1.5)

        caption(r"Matrix of $T$: columns $T\alpha_1=(1,1)$ and $T\alpha_2=(-1,-1)$")
        self.wait(3)
        caption(r"Apply $T(x,y)=(x-y)(1,1)$ to every point of the grid")
        self.play(ApplyMatrix(T, grid), run_time=6)
        self.wait(1)
        caption(r"The whole plane collapses onto $W$; the line $y=x$ (the kernel) goes to $0$")
        self.wait(4)

        # swapped map on a fresh grid
        self.play(FadeOut(grid))
        grid2 = make_grid()
        self.play(Create(grid2))
        caption(r"$T'$ (swapped images) collapses onto the same line, but flipped")
        self.play(ApplyMatrix(Tp, grid2), run_time=6)
        self.wait(2)
        caption(r"A linear map is fixed completely by its values on a basis")
        self.wait(3.5)


if __name__ == "__main__":
    config.quality = "low_quality"
    config.preview = True
    LinearMapFromBasis().render()
