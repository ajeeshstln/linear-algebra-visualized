from manim import *
import numpy as np

def P3(x, y):
    return np.array([x, y, 0.0])

class Coordinates(Scene):
    def construct(self):
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
            return Arrow(a, b, buff=0, color=color, stroke_width=w,
                         max_stroke_width_to_length_ratio=100)

        def vanish(*mobs):
            self.play(*[FadeOut(m) for m in mobs])

        Pm = [[1, -1], [1, 1]]            # columns = f1, f2 in standard coordinates
        f1, f2 = P3(1, 1), P3(-1, 1)
        v = P3(2, 1)                      # v = 1.5 f1 - 0.5 f2

        ref = NumberPlane(x_range=[-8, 8, 1], y_range=[-5, 5, 1],
                          background_line_style={"stroke_opacity": 0.15})
        self.add(ref)

        # ---------- basis B = standard: measuring sticks e1, e2 ----------
        caption(r"A basis is a set of measuring sticks. Basis $B$: $e_1=(1,0),\ e_2=(0,1)$")
        e1a = arrow(ORIGIN, P3(1, 0), RED)
        e2a = arrow(ORIGIN, P3(0, 1), GREEN)
        e1_l = MathTex(r"e_1", color=RED, font_size=30).next_to(P3(1, 0), DOWN, buff=0.1)
        e2_l = MathTex(r"e_2", color=GREEN, font_size=30).next_to(P3(0, 1), LEFT, buff=0.1)
        self.play(Create(e1a), Create(e2a), Write(e1_l), Write(e2_l))
        v_arr = arrow(ORIGIN, v, YELLOW, 8)
        v_l = MathTex(r"v", color=YELLOW, font_size=34).next_to(v, UP + RIGHT, buff=0.1)
        self.play(Create(v_arr), Write(v_l))
        self.wait(1)

        caption(r"Measure $v$ with $B$: $2$ steps of $e_1$, then $1$ step of $e_2$")
        s1 = arrow(ORIGIN, P3(2, 0), RED, 9)
        s2 = arrow(P3(2, 0), v, GREEN, 9)
        self.play(Create(s1))
        self.play(Create(s2))
        coordB = MathTex(r"[v]_B=(2,\,1)", color=YELLOW, font_size=38).to_corner(DR)
        self.play(Write(coordB))
        self.wait(2)
        vanish(s1, s2, e1a, e2a, e1_l, e2_l)

        # ---------- basis B' = f1, f2 ----------
        caption(r"Basis $B'$: $f_1=(1,1),\ f_2=(-1,1)$. Different sticks, same $v$")
        grid2 = NumberPlane(x_range=[-8, 8, 1], y_range=[-5, 5, 1],
                            background_line_style={"stroke_opacity": 0.5,
                                                   "stroke_color": BLUE_D})
        self.play(Create(grid2))
        self.play(ApplyMatrix(Pm, grid2), run_time=3)
        f1a = arrow(ORIGIN, f1, ORANGE)
        f2a = arrow(ORIGIN, f2, PURPLE)
        f1_l = MathTex(r"f_1", color=ORANGE, font_size=30).next_to(f1, RIGHT, buff=0.1)
        f2_l = MathTex(r"f_2", color=PURPLE, font_size=30).next_to(f2, LEFT, buff=0.1)
        self.play(Create(f1a), Create(f2a), Write(f1_l), Write(f2_l))
        self.wait(1)

        caption(r"Measure $v$ with $B'$: $1.5$ steps of $f_1$, then $-0.5$ steps of $f_2$")
        t1 = arrow(ORIGIN, 1.5 * f1, ORANGE, 9)
        t2 = arrow(1.5 * f1, v, PURPLE, 9)
        self.play(Create(t1))
        self.play(Create(t2))
        coordB2 = MathTex(r"[v]_{B'}=(1.5,\,-0.5)", color=YELLOW, font_size=38).next_to(coordB, UP)
        self.play(Write(coordB2))
        caption(r"Same vector $v$, different coordinates: the numbers depend on the basis")
        self.wait(3)
        vanish(t1, t2)

        # ---------- (a) ordered basis ----------
        caption(r"(a) Coordinates are a list, so the order of the sticks matters")
        self.wait(2)
        swap = MathTex(r"B''=(f_2,f_1):\ [v]_{B''}=(-0.5,\,1.5)", color=YELLOW,
                       font_size=36).to_edge(DOWN)
        self.play(Write(swap))
        caption(r"Same set $\{f_1,f_2\}$, new order, new list: $(1.5,-0.5)\neq(-0.5,1.5)$")
        self.wait(3)
        caption(r"An ordered basis tells us which number goes with which stick")
        self.wait(2.5)
        vanish(swap)

        # ---------- (b) change-of-basis matrix ----------
        caption(r"(b) Columns of $P$: the coordinates of the new sticks $f_j$ in the old basis $B$")
        pmat = MathTex(r"P=\begin{pmatrix}1&-1\\1&1\end{pmatrix}", font_size=40
                       ).to_corner(DL)
        self.play(Write(pmat))
        self.play(Indicate(f1a), Indicate(f2a))
        self.wait(2)
        rel = MathTex(r"[v]_B=P\,[v]_{B'}:\ \begin{pmatrix}2\\1\end{pmatrix}="
                      r"\begin{pmatrix}1&-1\\1&1\end{pmatrix}\begin{pmatrix}1.5\\-0.5\end{pmatrix}",
                      font_size=34).to_edge(DOWN)
        self.play(Write(rel))
        caption(r"$P$ turns $B'$-coordinates into $B$-coordinates")
        self.wait(3.5)

        caption(r"$P$ must be invertible: $[v]_{B'}=P^{-1}[v]_B$ lets us go back")
        self.wait(3)

        # what goes wrong if P is not invertible
        vanish(f1a, f2a, f1_l, f2_l, grid2, rel, coordB2)
        bad = NumberPlane(x_range=[-8, 8, 1], y_range=[-5, 5, 1],
                          background_line_style={"stroke_opacity": 0.5,
                                                 "stroke_color": RED_D})
        caption(r"If the $f_j$ were dependent, $P$ would be singular")
        self.play(Create(bad))
        self.play(ApplyMatrix([[1, 2], [1, 2]], bad), run_time=4)
        caption(r"The plane collapses to a line: some vectors get no coordinates, others many")
        self.wait(3)
        caption(r"A basis is independent and spanning, so every $v$ has exactly one list, and $P$ is invertible")
        self.wait(4)


if __name__ == "__main__":
    config.quality = "low_quality"
    config.preview = True
    Coordinates().render()
