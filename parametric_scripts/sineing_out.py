#!/usr/bin/env python3

# NAME: Sine-ing out
# Circular Bands emanting from the center


import sys
import time
import numpy as np

from backend.ceiling import Ceiling
from backend.util import color_format_to_rgb, sigmoid_0_to_1


def run(**kwargs):
    color_input = color_format_to_rgb(kwargs["color"])
    interval = float(kwargs["interval"])

    # Number of bands
    SAMPLE_SIZE = 5
    # Brightest color this will yield
    color = np.array(color_input)

    ceil = kwargs["ceiling"]
    ceil.use_float_polar(origin=(0.5, 0.5), effect_radius=0.1)
    ceil.clear()

    FPS = 60
    DELTA = 1 / FPS
    cur_time = 0

    radiuses = (np.arange(SAMPLE_SIZE) + 1) / SAMPLE_SIZE
    while True:
        cur_time = (cur_time + DELTA) % interval
        prog = cur_time / interval

        ceil.clear(False)

        for theta in range(0, 360, 10):
            for i in range(len(radiuses)):
                amt = np.sin((i / len(radiuses) + (prog)) * (2 * np.pi))
                amt = (amt / 2) + 0.5
                # print(amt)
                ceil[radiuses[i], theta] = (color * amt).astype(int)
        ceil.show()
        time.sleep(DELTA)


if __name__ == "__main__":
    run(ceiling=Ceiling(), color=sys.argv[1], interval=sys.argv[2])
