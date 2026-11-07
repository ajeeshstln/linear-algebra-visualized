from manim import *
import numpy as np

class OneSidedInverses(Scene):
    def construct(self):
        self.cap = None
        def caption(text):
            new = Tex(text, font_size=30).to_edge(UP)
            if new.width > 12.5:
                new.scale_to_fit_width(12.5)
            if self.cap is None:
                self.play(Write(new))
            else:
                self.play(FadeOut(self.cap), Write(new))
            self.cap = new

        def wipe():
            for m in self.mobjects:
                m.clear_updaters()
            if self.mobjects:
                self.play(*[FadeOut(m) for m in self.mobjects])
            self.cap = None

        def node(tex, x, y, color=WHITE):
            return MathTex(tex, color=color, font_size=40).move_to([x, y, 0])

        def link(a, b, color=YELLOW):
            return Arrow(a.get_right(), b.get_left(), buff=0.15,
                         color=color, stroke_width=5)

        # =====================================================
        # (a) D: onto, not one-to-one
        # =====================================================
        caption(r"(a) $D$ = differentiation on polynomials: $D(x^n)=n\,x^{n-1}$")
        ys = [1.5, 0.5, -0.5, -1.5]
        L = [node(t, -3, y) for t, y in zip([r"x^3", r"x^2", r"x", r"1"], ys)]
        R = [node(t, 3, y) for t, y in zip([r"3x^2", r"2x", r"1", r"0"], ys)]
        R[3].set_color(RED)
        arrows = [link(a, b) for a, b in zip(L, R)]
        self.play(*[Write(m) for m in L + R])
        self.play(*[Create(a) for a in arrows])
        self.wait(1.5)

        caption(r"Onto: any $q$ has an antiderivative, e.g. $3x^2=D(x^3)$")
        self.play(Indicate(L[0]), Indicate(R[0]))
        self.wait(2)
        caption(r"Not one-to-one: $D(1)=0$, the constants are the directions $D$ cannot see")
        self.play(Indicate(L[3], color=RED), Indicate(R[3]))
        self.wait(2)
        wipe()

        caption(r"Information loss: $x^2+1$ and $x^2+5$ both go to $2x$")
        a = node(r"x^2+1", -3, 1)
        b = node(r"x^2+5", -3, -1)
        c = node(r"2x", 3, 0, ORANGE)
        self.play(Write(a), Write(b), Write(c))
        self.play(Create(link(a, c, PURPLE)), Create(link(b, c, PURPLE)))
        self.wait(2.5)
        wipe()

        # T: one-to-one, not onto
        caption(r"$T$ = multiplication by $x$: $T(x^n)=x^{n+1}$")
        ys = [1.5, 0.5, -0.5, -1.5]
        Lt = [node(t, -3, y) for t, y in zip([r"x^2", r"x", r"1"], ys[:3])]
        Rt = [node(t, 3, y) for t, y in zip([r"x^3", r"x^2", r"x", r"1"], ys)]
        Rt[3].set_color(RED)
        at = [link(a, b, GREEN) for a, b in zip(Lt, Rt[:3])]
        self.play(*[Write(m) for m in Lt + Rt])
        self.play(*[Create(a) for a in at])
        self.wait(1.5)
        caption(r"One-to-one: $xp=xq\Rightarrow p=q$, so different inputs stay different")
        self.wait(2.5)
        caption(r"Not onto: every $xp(x)$ has $0$ constant term, so $1$ is never hit")
        self.play(Indicate(Rt[3], color=RED))
        self.wait(3)
        wipe()

        # =====================================================
        # (b) no two-sided inverse, DT - TD = I
        # =====================================================
        caption(r"(b) $D$ is not injective and $T$ is not onto, so neither is invertible")
        self.wait(3)
        caption(r"One-sided inverses exist: $D\circ\!\int=I$, but $\int\!\circ D(1)=0\neq1$")
        self.wait(3.5)
        caption(r"Order matters: compare $DT$ and $TD$ on $p=x^2$")
        l1 = MathTex(r"DT(x^2)=D(x^3)=3x^2", font_size=40).move_to([0, 1.2, 0])
        l2 = MathTex(r"TD(x^2)=T(2x)=2x^2", font_size=40).move_to([0, 0, 0])
        l3 = MathTex(r"(DT-TD)(x^2)=x^2", font_size=40, color=ORANGE).move_to([0, -1.2, 0])
        self.play(Write(l1))
        self.play(Write(l2))
        self.play(Write(l3))
        self.wait(2.5)
        caption(r"In general $DT(p)=p+xp'$ and $TD(p)=xp'$, so $DT-TD=I$")
        ident = MathTex(r"DT-TD=I", font_size=56, color=YELLOW).move_to([0, -2.6, 0])
        self.play(Write(ident))
        self.wait(2)
        caption(r"$DT\neq TD$: composing in a different order gives a different map")
        self.wait(3.5)
        wipe()

        # =====================================================
        # (c) T(x1,x2) = (x1+x2, x1): equal dimensions
        # =====================================================
        M = [[1, 1], [1, 0]]
        caption(r"(c) $T(x_1,x_2)=(x_1+x_2,\,x_1)$ on $\mathbb{R}^2\to\mathbb{R}^2$")
        ref = NumberPlane(x_range=[-8, 8, 1], y_range=[-5, 5, 1],
                          background_line_style={"stroke_opacity": 0.12})
        grid = NumberPlane(x_range=[-8, 8, 1], y_range=[-5, 5, 1],
                           background_line_style={"stroke_opacity": 0.6,
                                                  "stroke_color": BLUE_D})
        square = Polygon(ORIGIN, RIGHT, RIGHT + UP, UP, color=YELLOW,
                         fill_color=YELLOW, fill_opacity=0.35)
        self.add(ref)
        self.play(Create(grid), FadeIn(square))
        self.wait(1)

        caption(r"Null space: $x_1+x_2=0$ and $x_1=0$ force $x=0$, so nullity $=0$")
        self.play(FadeIn(Dot(ORIGIN, color=RED, radius=0.12)))
        self.wait(2.5)
        caption(r"Apply $T$: the grid is sheared but never collapsed")
        self.play(ApplyMatrix(M, grid), ApplyMatrix(M, square), run_time=5)
        self.wait(1.5)
        caption(r"Rank $=2-0=2$, so the range is all of $\mathbb{R}^2$: $T$ is onto")
        self.wait(3)
        eq = MathTex(r"\mathrm{rank}+\mathrm{nullity}=2\ \Rightarrow\ "
                     r"\text{injective}\iff\text{onto}\iff\text{invertible}",
                     font_size=34, color=ORANGE).to_edge(DOWN)
        self.play(Write(eq))
        self.wait(3)
        wipe()

        # contrast: singular map
        caption(r"Contrast: $S(x_1,x_2)=(x_1+x_2,\,x_1+x_2)$ has nullity $1$")
        grid2 = NumberPlane(x_range=[-8, 8, 1], y_range=[-5, 5, 1],
                            background_line_style={"stroke_opacity": 0.6,
                                                   "stroke_color": RED_D})
        self.add(NumberPlane(x_range=[-8, 8, 1], y_range=[-5, 5, 1],
                             background_line_style={"stroke_opacity": 0.12}))
        self.play(Create(grid2))
        self.play(ApplyMatrix([[1, 1], [1, 1]], grid2), run_time=5)
        caption(r"Not injective, and not onto (rank $1<2$): the two failures go together")
        self.wait(3)
        caption(r"For equal dimensions: non-singular $\iff$ onto $\iff$ invertible")
        self.wait(3.5)
        caption(r"In infinite dimensions $D$ and $T$ show this equivalence can fail")
        self.wait(3.5)


if __name__ == "__main__":
    config.quality = "low_quality"
    config.preview = True
    OneSidedInverses().render()
