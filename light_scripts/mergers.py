#!/usr/bin/env python3

# NAME: Mergers
# 2 points of different colors, bouncing around

import time
import numpy as np
import colour

from backend.ceiling import Ceiling
from backend.util import colour_rgb_to_neopixel_rgb, rotate_vector


def run(**kwargs):
    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_float_cartesian(effect_radius=0.3)
    ceil.clear()

    prog_1 = np.random.random()
    col_1 = colour.Color(hsl=(prog_1, 1, 0.5))
    prog_2 = np.random.random()
    col_2 = colour.Color(hsl=(prog_2, 1, 0.5))

    point_1 = np.array([0.5, 0.5])
    velocity_1 = np.array([1.0, 0])
    velocity_1 = rotate_vector(velocity_1, np.random.random() * 360)

    point_2 = np.array([0.5, 0.5])
    velocity_2 = np.array([1.0, 0])
    velocity_2 = rotate_vector(velocity_2, np.random.random() * 360)

    FPS = 60
    DELTA = 1 / FPS

    while True:
        point_1 += velocity_1 * DELTA
        point_2 += velocity_2 * DELTA

        if point_1[0] < 0 or point_1[0] > 1:
            velocity_1[0] = -velocity_1[0]
        if point_1[1] < 0 or point_1[1] > 1:
            velocity_1[1] = -velocity_1[1]

        if point_2[0] < 0 or point_2[0] > 1:
            velocity_2[0] = -velocity_2[0]
        if point_2[1] < 0 or point_2[1] > 1:
            velocity_2[1] = -velocity_2[1]

        prog_1 = (prog_1 + DELTA) % 1
        prog_2 = (prog_2 + DELTA) % 1
        col_1.set_hue(prog_1)
        col_2.set_hue(prog_2)

        ceil.clear(False)
        ceil[point_1[0], point_1[1]] = colour_rgb_to_neopixel_rgb(col_1.rgb)
        ceil[point_2[0], point_2[1]] = colour_rgb_to_neopixel_rgb(col_2.rgb)
        ceil.show()

        time.sleep(DELTA)


if __name__ == "__main__":
    run(ceiling=Ceiling())
