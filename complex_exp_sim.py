from manim import *
import numpy as np


# --- Parameters ---
r = 1j             
M_o = 1
T = 2 * np.pi     # how much to rotate
n = 1000          # num steps
dt = T / n

# --- Compute euler approximation vectors  ---
M = [M_o]
delta_M = []
for i in range(1, n):
    delta = M[i - 1] * 1j * dt
    M.append(M[i - 1] + delta)
    delta_M.append(delta)

M = np.array(M)
delta_M = np.array(delta_M)


# --- Animation  ---
class EulerRotation(Scene):
    def construct(self):
        # Complex plane & title
        self.plane = ComplexPlane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            background_line_style={"stroke_opacity": 0.3}
        )
        self.add(self.plane, self.plane.get_coordinate_labels(font_size=24))

        # Add a legend
        legend = VGroup(
            Arrow(ORIGIN, RIGHT, color=BLUE, buff=0).scale(0.5),
            MathTex("M", color=BLUE).scale(0.8),
            Arrow(ORIGIN, RIGHT, color=RED, buff=0).scale(0.5),
            MathTex(r"\Delta M", color=RED).scale(0.8)
        ).arrange(RIGHT, buff=0.3)

        # Position legend in the upper-right corner
        legend.to_corner(UR)
        self.add(legend)
        
        # Moving M arrow
        self.M_vec = Arrow(
            start=self._c2p(0),
            end=self._c2p(M[0]),
            buff=0,
            stroke_width=4,
            color=BLUE
        )
        self.add(self.M_vec)

        # Trail of the M tip
        self.add(TracedPath(self.M_vec.get_end, stroke_color=BLUE, stroke_opacity=0.5, stroke_width=2))

        # Global time tracker
        self.t = ValueTracker(0.0)     # drives continuous progress through segments
        self._t_tracker = self.t       # used by _delta_arrow()

        # ΔM arrow shown ahead of M for the current segment
        dM_vec = always_redraw(lambda: self._delta_arrow(M, color=RED))
        self.add(dM_vec)

        # Continuous update of M_vec
        self.M_vec.add_updater(self._update_M)

        # Simulation duration
        TOTAL_TIME = 7
        self.play(self.t.animate.set_value(len(M) - 1), run_time=TOTAL_TIME, rate_func=linear)

        self.M_vec.remove_updater(self._update_M)
        self.wait(1)


    # Helpers
    def _c2p(self, z):
        return self.plane.c2p(np.real(z), np.imag(z))


    def _update_M(self, mobj):
        tval = self.t.get_value()
        k = int(np.floor(tval))
        alpha = tval - k
        if k >= len(M) - 1:
            z = M[-1]
        else:
            z = (1 - alpha) * M[k] + alpha * M[k + 1]
        mobj.put_start_and_end_on(self._c2p(0), self._c2p(z))


    def _delta_arrow(self, M, color=RED):
        tval = self._t_tracker.get_value()
        k = int(np.floor(tval))
        if k >= len(M) - 1:
            return VGroup()
        return Arrow(
            start=self._c2p(M[k]),
            end=self._c2p(M[k + 1]),
            buff=0,
            stroke_width=3,
            color=color
        )
