#!/usr/bin/env python3

# NAME: Bouncing DVD
# A point bounces around the edges of the display


import sys
import time
import numpy as np

from backend.ceiling import Ceiling
from backend.util import (
    color_format_to_obj,
    color_format_to_rgb,
    hex_to_rgb,
    rotate_vector,
)


def run(**kwargs):
    color_input = kwargs["color"]
    speed = float(kwargs["interval"])

    color = color_format_to_rgb(color_input)

    ceil = kwargs["ceiling"]
    ceil.use_float_cartesian(effect_radius=0.3)
    ceil.clear()

    point = np.array([0.5, 0.5])
    velocity = np.array([1.0, 0]) * speed
    velocity = rotate_vector(velocity, np.random.random() * 360)

    FPS = 60
    DELTA = 1 / 60
    while True:
        point += velocity * DELTA

        if point[0] < 0 or point[0] > 1:
            velocity[0] = -velocity[0]

        if point[1] < 0 or point[1] > 1:
            velocity[1] = -velocity[1]

        ceil.clear(False)
        ceil[point[0], point[1]] = color
        ceil.show()

        time.sleep(DELTA)


if __name__ == "__main__":
    run(ceiling=Ceiling(), color=sys.argv[1], interval=sys.argv[2])
