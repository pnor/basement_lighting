#!/usr/bin/env python3

# Animated gray noise, using the float cartesian's effect radius


import time
import numpy as np
import colour

from backend.ceiling import Ceiling
from backend.util import clamp, colour_rgb_to_neopixel_rgb


def rand_func(size: int):
    return np.random.beta(a=2, b=15, size=(size, size))
    # return np.random.beta(a=2, b=10, size=(size, size))


def run(**kwargs):
    # Number of points used to generate colors (size by size)
    RANDOM_SIZE = 10
    # Brightest color this will yield
    color = np.array([100, 100, 100])

    ceil = Ceiling()
    ceil.use_float_cartesian(effect_radius=0.15)
    ceil.clear()

    points = rand_func(RANDOM_SIZE)
    next_points = rand_func(RANDOM_SIZE)

    period = 1
    cur = 0

    FPS = 60
    DELTA = 1 / FPS

    while True:
        cur += DELTA
        if cur > period:
            cur = 0
            points = next_points
            next_points = rand_func(RANDOM_SIZE)

        prog = clamp(cur / period, 0, 1)
        # print(f"cur: {cur} period: {period} prog: {prog}")

        ceil.clear(False)
        for i in range(RANDOM_SIZE):
            for j in range(RANDOM_SIZE):
                before_col = (color * points[i, j]).astype(int)
                next_col = (color * next_points[i, j]).astype(int)
                interpolated_col = (
                    ((1 - prog) * before_col) + (prog * next_col)
                ).astype(int)

                # to better center the effect
                bump = (1 / RANDOM_SIZE) / 2
                ceil[bump + (i / RANDOM_SIZE), bump + (j / RANDOM_SIZE)] = tuple(
                    interpolated_col
                )

        ceil.show()
        time.sleep(DELTA)


if __name__ == "__main__":
    run()
