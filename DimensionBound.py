from manim import *
import numpy as np

def P(x, y):
    return np.array([x, y, 0.0])

class DimensionBound(Scene):
    def construct(self):
        self.add(NumberPlane(x_range=[-8, 8, 1], y_range=[-5, 5, 1],
                             background_line_style={"stroke_opacity": 0.2}))

        self.cap = None
        def caption(text):
            new = Tex(text, font_size=34).to_edge(UP)
            if new.width > 12:
                new.scale_to_fit_width(12)
            if self.cap is None:
                self.play(Write(new))
            else:
                self.play(FadeOut(self.cap), Write(new))
            self.cap = new

        def arrow(a, b, color, w=6):
            return Arrow(a, b, buff=0, color=color, stroke_width=w,
                         max_stroke_width_to_length_ratio=100)

        # ---------- V is spanned by (1,0) and (0,1) ----------
        caption(r"$V$ is spanned by $(1,0)$ and $(0,1)$, so $m = 2$")
        e1 = arrow(ORIGIN, P(1, 0), RED, 8)
        e2 = arrow(ORIGIN, P(0, 1), GREEN, 8)
        self.play(Create(e1), Create(e2))
        self.wait(1.5)

        # ---------- Claim ----------
        caption(r"Claim: an independent subset of $V$ has at most $2$ elements")
        self.wait(2)
        caption(r"So we show: any $3$ vectors in $V$ are dependent")
        self.wait(2)
        self.play(FadeOut(e1), FadeOut(e2))

        # ---------- Three vectors alpha, beta, gamma in V ----------
        al, be = P(2, 1), P(-1, 2)
        c1, c2 = 1.5, 1.0
        ga = c1 * al + c2 * be

        caption(r"Take $\alpha,\beta,\gamma$ in $V$")
        a_arr = arrow(ORIGIN, al, YELLOW)
        b_arr = arrow(ORIGIN, be, PURPLE)
        g_arr = arrow(ORIGIN, ga, ORANGE)
        a_l = MathTex(r"\alpha", color=YELLOW).next_to(al, DOWN + RIGHT, buff=0.1)
        b_l = MathTex(r"\beta", color=PURPLE).next_to(be, LEFT, buff=0.1)
        g_l = MathTex(r"\gamma", color=ORANGE).next_to(ga, RIGHT, buff=0.1)
        self.play(Create(a_arr), Write(a_l), Create(b_arr), Write(b_l))
        self.play(Create(g_arr), Write(g_l))
        self.wait(1.5)

        # ---------- gamma = c1 alpha + c2 beta ----------
        caption(r"$\alpha,\beta$ span $V$, so $\gamma = c_1\alpha + c_2\beta$")
        self.play(FadeOut(g_arr), FadeOut(g_l))
        ca = arrow(ORIGIN, c1 * al, YELLOW, 8)
        cb = arrow(c1 * al, ga, PURPLE, 8)
        ca_l = MathTex(r"c_1\alpha", color=YELLOW).next_to(c1 * al, DOWN + RIGHT, buff=0.1)
        cb_l = MathTex(r"c_2\beta", color=PURPLE).next_to(c1 * al + 0.5 * be, RIGHT, buff=0.2)
        self.play(Create(ca), Write(ca_l))
        self.play(Create(cb), Write(cb_l))
        g2 = arrow(ORIGIN, ga, ORANGE, 8)
        g2_l = MathTex(r"\gamma", color=ORANGE).next_to(ga, UP, buff=0.15)
        self.play(Create(g2), Write(g2_l))
        self.wait(1.5)

        # ---------- c1 alpha + c2 beta - gamma = 0 ----------
        caption(r"$c_1\alpha + c_2\beta - 1\cdot\gamma = 0$")
        neg_g = arrow(ga, ORIGIN, RED, 8)
        ng_l = MathTex(r"-\gamma", color=RED).next_to(0.5 * ga, LEFT, buff=0.2)
        self.play(Create(neg_g), Write(ng_l))
        self.play(FadeIn(Dot(ORIGIN, color=GREEN, radius=0.12)))
        self.wait(1.5)
        caption(r"Coefficient of $\gamma$ is $-1\neq 0$, so $\alpha,\beta,\gamma$ are dependent")
        self.wait(3)

        caption(r"Any $n>2$ vectors in $V$ are dependent, so an independent set has $\le 2$ elements")
        self.wait(3)


if __name__ == "__main__":
    config.quality = "low_quality"
    config.preview = True
    DimensionBound().render()
