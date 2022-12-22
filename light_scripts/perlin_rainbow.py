#!/usr/bin/env python3

# NAME: Perlin Noise Rainbow
# Animated Perlin Noise affecting color hue
# (takes in 1 argument for speed)


import sys
import time
import numpy as np
from colour import Color
from perlin_noise import PerlinNoise

from backend.ceiling import Ceiling
from backend.util import color_obj_to_rgb, sigmoid_0_to_1


def run(**kwargs):
    interval = kwargs.get("interval")
    interval = float(interval) if interval else 1

    # Number of points used to sample the perlin noise obj
    SAMPLE_SIZE = 20

    ceil = kwargs["ceiling"]
    ceil.use_float_cartesian(effect_radius=0.1)
    ceil.clear()

    cur_perlin_noise = PerlinNoise()
    next_perlin_noise = PerlinNoise()

    period = interval
    cur = 0

    FPS = 60
    DELTA = 1 / FPS

    # while True:
    iter = 0
    while iter < 1000:
        iter += 1
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

                before_hue = cur_perlin_noise([i_indx, j_indx])
                after_hue = next_perlin_noise([i_indx, j_indx])

                interpolated_hue = ((1 - prog) * before_hue) + (prog * after_hue)

                # to better center the effect
                bump = (1 / SAMPLE_SIZE) / 2

                color_obj = Color(hsl=(interpolated_hue, 1, 0.5))
                ceil[
                    bump + (i / SAMPLE_SIZE), bump + (j / SAMPLE_SIZE)
                ] = color_obj_to_rgb(color_obj)
        ceil.show()
        time.sleep(DELTA)


if __name__ == "__main__":
    run(ceiling=Ceiling(), interval=sys.argv[1])
