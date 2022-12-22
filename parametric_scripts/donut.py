#!/usr/bin/env python3

# NAME: The Bagel Film

# Based off of
# https://www.a1k0n.net/2011/07/20/donut-math.html
# (computationally expensive to run, numba required)

import sys
import time
import numpy as np
from numpy._typing import NDArray
from numba import jit

from backend.ceiling import Ceiling
from backend.util import color_format_to_rgb


# Number of sample points we want to use when drawing on the ceiling
screen_width = 30
screen_height = 30
# largely copied from the example code at the bottom of the article:
theta_spacing = 0.07
phi_spacing = 0.02
R1 = 1
R2 = 2
K2 = 5
K1: float = screen_width * K2 * 3 / (8 * (R1 + R2))


@jit
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


def run(**kwargs):
    color = np.array(color_format_to_rgb(kwargs["color"]))
    interval = float(kwargs["interval"])
    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_cartesian(search_range=0.04)
    ceil.clear()

    FPS = 60
    DELTA = 1 / FPS

    cur_a = 0
    interval_a = interval * 7 * 5
    cur_b = 0
    interval_b = interval * 9

    # while True:
    while True:

        cur_a = (cur_a + DELTA) % interval_a
        cur_b = (cur_b + DELTA) % interval_b
        prog_a = cur_a / interval
        prog_b = cur_b / interval

        a = prog_a * (2 * np.pi)
        b = prog_b * (2 * np.pi)
        mat = render_frame(a, b)

        for i in range(screen_width):
            for j in range(screen_height):
                col = (color * mat[i, j]).astype(int)
                x_indx = i / screen_width
                y_indx = j / screen_height
                ceil[x_indx, y_indx] = col

        ceil.show()
        time.sleep(DELTA)


if __name__ == "__main__":
    run(
        ceiling=Ceiling(),
        color=sys.argv[1],
        interval=sys.argv[2],
    )
