#!/usr/bin/env python3

#!/usr/bin/env python3

# NAME: Perlin Noise
# Animated Perlin Noise (of any 1 color)


import sys
import time
import numpy as np
from perlin_noise import PerlinNoise

from backend.ceiling import Ceiling
from backend.util import color_format_to_rgb, sigmoid_0_to_1


def run(**kwargs):
    color_input = color_format_to_rgb(kwargs["color"])
    interval = float(kwargs["interval"])

    # Number of points used to sample the perlin noise obj
    SAMPLE_SIZE = 20
    # Brightest color this will yield
    color = np.array(color_input)

    ceil = Ceiling()
    ceil.use_float_cartesian(effect_radius=0.1)
    ceil.clear()

    cur_perlin_noise = PerlinNoise()
    next_perlin_noise = PerlinNoise()

    period = interval
    cur = 0

    FPS = 60
    DELTA = 1 / FPS

    while True:
        cur += DELTA
        if cur > period:
            cur = 0
            cur_perlin_noise = next_perlin_noise
            next_perlin_noise = PerlinNoise(octaves=np.random.randint(1, 4))

        prog = sigmoid_0_to_1(cur / period)

        ceil.clear(False)
        for i in range(SAMPLE_SIZE):
            for j in range(SAMPLE_SIZE):
                i_indx = i / SAMPLE_SIZE
                j_indx = j / SAMPLE_SIZE
                before_col = (color * cur_perlin_noise([i_indx, j_indx])).astype(int)
                next_col = (color * next_perlin_noise([i_indx, j_indx])).astype(int)
                interpolated_col = (
                    ((1 - prog) * before_col) + (prog * next_col)
                ).astype(int)

                # to better center the effect
                bump = (1 / SAMPLE_SIZE) / 2
                ceil[bump + (i / SAMPLE_SIZE), bump + (j / SAMPLE_SIZE)] = tuple(
                    interpolated_col
                )

        ceil.show()
        time.sleep(DELTA)


if __name__ == "__main__":
    run(color=sys.argv[1], interval=sys.argv[2])
