#!/usr/bin/env python3

# NAME: The Bagel Film

# Based off of
# https://www.a1k0n.net/2011/07/20/donut-math.html
# (computationally expensive to run, numba required)

import sys
from typing import Optional, Union
import numpy as np
from numpy._typing import NDArray
from numba import jit
from backend.backend_types import RGB

from backend.ceiling import Ceiling
from backend.state import State
from backend.util import color_format_to_rgb
from scripts.library.render import RenderState


# Number of sample points we want to use when drawing on the ceiling
screen_width = 35
screen_height = 35
# largely copied from the example code at the bottom of the article:
theta_spacing = 0.07
phi_spacing = 0.02
R1 = 1
R2 = 2
K2 = 5
K1: float = screen_width * K2 * 3 / (8 * (R1 + R2))


@jit(fastmath=True)
def render_frame(A: float, B: float) -> NDArray[np.float64]:
    cosA = np.cos(A)
    sinA = np.sin(A)
    cosB = np.cos(B)
    sinB = np.sin(B)

    output = np.zeros((screen_width, screen_height))
    zbuffer = np.zeros((screen_width, screen_height))

    for theta in np.arange(0, 2 * np.pi, theta_spacing):
        costheta = np.cos(theta)
        sintheta = np.sin(theta)

        for phi in np.arange(0, 2 * np.pi, phi_spacing):
            cosphi = np.cos(phi)
            sinphi = np.sin(phi)

            circlex = R2 + R1 * costheta
            circley = R1 * sintheta

            x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
            y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
            z = K2 + cosA * circlex * sinphi + circley * sinA
            ooz = 1 / z

            xp = int(screen_width / 2 + K1 * ooz * x)
            yp = int(screen_height / 2 - K1 * ooz * y)

            L = (
                cosphi * costheta * sinB
                - cosA * costheta * sinphi
                - sinA * sintheta
                + cosB * (cosA * sintheta - costheta * sinA * sinphi)
            )
            if L > 0:
                if ooz > zbuffer[xp, yp]:
                    zbuffer[xp, yp] = ooz
                    # luminance_index is between 0..sqrt(2)
                    # We scale this to 0..1 for output
                    luminance_index = L / np.sqrt(2)
                    output[xp, yp] = luminance_index

    return output


class Render(RenderState):
    def __init__(self, color: RGB, interval: Optional[float]) -> None:
        interval = interval if interval else 1
        self.cur_a = 0
        self.interval_a = interval * 7
        self.cur_b = 0
        self.interval_b = interval * 9
        self.color = np.array(color)
        super().__init__(interval)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        self.cur_a = (self.cur_a + delta) % self.interval_a
        self.cur_b = (self.cur_b + delta) % self.interval_b

        prog_a = self.cur_a / self.interval_a
        prog_b = self.cur_b / self.interval_b

        a = prog_a * (2 * np.pi)
        b = prog_b * (2 * np.pi)
        mat = render_frame(a, b)

        ceil.clear()
        for i in range(screen_width):
            for j in range(screen_height):
                col = (self.color * mat[i, j]).astype(int)
                x_indx = i / screen_width
                y_indx = j / screen_height
                x_indx = x_indx * 1.3 - 0.15
                y_indx = y_indx * 1.3 - 0.15
                ceil[x_indx, y_indx] = col

        ceil.show()
        return super().render(delta, ceil)


def run(**kwargs):
    color = color_format_to_rgb(kwargs["color"])
    interval = float(kwargs["interval"])
    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_cartesian(search_range=0.04)
    ceil.clear()

    render_loop = Render(color, interval)
    render_loop.run(15, ceil)


if __name__ == "__main__":
    run(
        ceiling=State().create_ceiling(),
        color=sys.argv[1],
        interval=sys.argv[2],
    )
