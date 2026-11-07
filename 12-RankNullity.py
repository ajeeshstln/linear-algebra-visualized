from manim import *
import numpy as np

class RankNullity(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)
        self.add(ThreeDAxes(x_range=[-4, 4], y_range=[-4, 4], z_range=[-3, 3]))

        ex, ey, ez = np.eye(3)

        # ---------- helpers ----------
        self.cap = None
        def caption(text):
            new = Tex(text, font_size=30).to_corner(UL)
            if new.width > 9:
                new.scale_to_fit_width(9)
            self.add_fixed_in_frame_mobjects(new)
            if self.cap is None:
                self.play(Write(new))
            else:
                self.play(FadeOut(self.cap), Write(new))
            self.cap = new

        self.eq = None
        def equation(tex):
            new = MathTex(tex, font_size=38, color=ORANGE).to_edge(DOWN)
            self.add_fixed_in_frame_mobjects(new)
            if self.eq is None:
                self.play(Write(new))
            else:
                self.play(FadeOut(self.eq), Write(new))
            self.eq = new

        def plane(u, v, color, r=3):
            return Surface(lambda a, b: a * u + b * v,
                           u_range=[-r, r], v_range=[-r, r], resolution=(6, 6),
                           fill_opacity=0.25, stroke_opacity=0.25,
                           checkerboard_colors=[color, color])

        def clear(*mobs):
            self.play(*[FadeOut(m) for m in mobs])

        # =====================================================
        # (a) Projection T(x,y,z) = (x,y,0)
        # =====================================================
        caption(r"(a) $T(x,y,z)=(x,y,0)$ on $\mathbb{R}^3$")
        v = np.array([1.5, 1.0, 2.0])
        Tv = np.array([1.5, 1.0, 0.0])
        v_arr = Arrow3D(ORIGIN, v, color=YELLOW)
        self.play(Create(v_arr))
        self.wait(1)

        caption(r"$T$ drops the $z$-part: $v$ goes to its shadow in the $xy$-plane")
        xy = plane(ex, ey, BLUE)
        Tv_arr = Arrow3D(ORIGIN, Tv, color=ORANGE)
        drop = DashedLine(v, Tv, color=WHITE)
        self.play(FadeIn(xy))
        self.play(Create(drop), Create(Tv_arr))
        self.wait(1.5)

        caption(r"Range $R(T)$ = the $xy$-plane, so rank $=2$")
        self.wait(2.5)

        caption(r"$T(0,0,z)=0$: the $z$-axis is the direction $T$ cannot see, nullity $=1$")
        zaxis = Line3D(-3 * ez, 3 * ez, color=RED, thickness=0.05)
        self.play(Create(zaxis))
        self.wait(2)

        caption(r"Slide $v$ along the vertical line: $T(v)$ never changes")
        fiber = Line3D(Tv - 3 * ez, Tv + 3 * ez, color=YELLOW, thickness=0.02)
        dot = Dot3D(v, color=YELLOW, radius=0.1)
        self.play(Create(fiber), FadeIn(dot))
        self.play(dot.animate.move_to(Tv - 2.5 * ez), run_time=2)
        self.play(dot.animate.move_to(Tv + 2.5 * ez), run_time=2)
        self.wait(0.5)

        caption(r"Each point of the range has a whole copy of the null space above it")
        equation(r"\mathrm{rank}\,T+\mathrm{nullity}\,T=\dim V:\quad 2+1=3")
        self.wait(3.5)
        clear(v_arr, Tv_arr, drop, zaxis, fiber, dot)

        # =====================================================
        # (b) Inclusion R^2 -> R^3, T(x,y) = (x,y,0)
        # =====================================================
        caption(r"(b) $T(x,y)=(x,y,0)$ from $\mathbb{R}^2$ into $\mathbb{R}^3$")
        p1, p2 = np.array([1.0, 0.5, 0]), np.array([-1.5, 1.5, 0])
        d1 = Dot3D(p1, color=YELLOW, radius=0.1)
        d2 = Dot3D(p2, color=PURPLE, radius=0.1)
        self.play(FadeIn(d1), FadeIn(d2))
        self.wait(1)

        caption(r"Different inputs land on different points, and $N(T)=\{0\}$, so $T$ is injective")
        origin = Dot3D(ORIGIN, color=RED, radius=0.12)
        self.play(FadeIn(origin))
        self.wait(3)

        caption(r"The range is only the $xy$-plane, so rank $=2<3=\dim\mathbb{R}^3$")
        self.wait(2.5)
        miss = np.array([0.0, 0.0, 2.0])
        miss_dot = Dot3D(miss, color=RED, radius=0.12)
        miss_line = DashedLine(miss, ORIGIN, color=RED)
        self.play(FadeIn(miss_dot), Create(miss_line))
        caption(r"$(0,0,1)$ is never hit: no $\mathbb{R}^2$ can fill $\mathbb{R}^3$, so $T$ is not onto")
        equation(r"\mathrm{rank}+\mathrm{nullity}=\dim\mathbb{R}^2:\quad 2+0=2")
        self.wait(4)
        clear(d1, d2, origin, miss_dot, miss_line, xy)

        # =====================================================
        # (c) Solutions of Ax = 0 have dimension n - r
        # =====================================================
        caption(r"(c) $A=\begin{pmatrix}1&0&1\\0&1&1\end{pmatrix}$, $n=3$ unknowns, $r=2$ pivots")
        self.wait(2.5)

        P1 = plane(ey, ex - ez, GREEN)        # x + z = 0
        P2 = plane(ex, ey - ez, PURPLE)       # y + z = 0
        caption(r"Each row is one equation $\mathbf r\cdot x=0$: a plane through $0$")
        self.play(FadeIn(P1))
        self.wait(1.5)
        caption(r"Row 1 alone leaves a plane: dimension $3-1=2$")
        self.wait(2)
        self.play(FadeIn(P2))
        caption(r"Row 2 is independent of row 1, so it cuts one more dimension")
        self.wait(2.5)

        d = np.array([-1.0, -1.0, 1.0])
        sol = Line3D(-2.5 * d, 2.5 * d, color=ORANGE, thickness=0.05)
        self.play(Create(sol))
        self.move_camera(phi=75 * DEGREES, theta=-20 * DEGREES, run_time=3)
        caption(r"Solutions of $Ax=0$: the line through $(-1,-1,1)$, dimension $3-2=1$")
        equation(r"\dim\{x:Ax=0\}=n-r=3-2=1")
        self.wait(3)

        caption(r"Each pivot is an independent equation and removes one direction")
        self.wait(2.5)
        caption(r"The $n-r$ free variables are the directions $A$ cannot see")
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)


if __name__ == "__main__":
    config.quality = "low_quality"
    config.preview = True
    RankNullity().render()
