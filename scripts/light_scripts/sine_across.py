#!/usr/bin/env python3

# NAME: Sine Across
# Bands moving across using sine waves


import sys
import time
import numpy as np

from backend.ceiling import Ceiling
from backend.util import color_format_to_rgb, sigmoid_0_to_1


def run(**kwargs):
    color_input = color_format_to_rgb(kwargs["color"])
    interval = float(kwargs["interval"])

    # Number of bands
    SAMPLE_SIZE = 7
    # Brightest color this will yield
    color = np.array(color_input)

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_float_cartesian(effect_radius=0.2)
    ceil.clear()

    FPS = 20
    DELTA = 1 / FPS
    cur_time = 0

    horizs = (np.arange(SAMPLE_SIZE) + 1) / SAMPLE_SIZE
    while True:
        cur_time = (cur_time + DELTA) % interval
        prog = cur_time / interval

        ceil.clear(False)

        for y in range(10):
            for i in range(len(horizs)):
                amt = np.sin((i / len(horizs) + (prog)) * (2 * np.pi))
                amt = (amt / 2) + 0.5
                ceil[horizs[i], (y / 10)] = (color * amt).astype(int)
        ceil.show()
        time.sleep(DELTA)


if __name__ == "__main__":
    run(ceiling=Ceiling(), color=sys.argv[1], interval=sys.argv[2])
