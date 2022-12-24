#!/usr/bin/env python3

# NAME: Sinusoidal
# Since curves

import sys
import time
import numpy as np

from backend.ceiling import Ceiling
from backend.util import color_format_to_rgb


def run(**kwargs):
    color_input = color_format_to_rgb(kwargs["color"])
    interval = float(kwargs["interval"])
    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_cartesian()

    FPS = 60
    DELTA = 1 / FPS
    cur_time = 0

    while True:
        cur_time = (cur_time + DELTA) % interval
        prog = cur_time / interval

        ceil.clear(False)

        for x in range(0, 10):
            x_indx = x / 10
            y_indx = np.sin((2 * np.pi) * (prog + (x / 9)))
            y_indx = (y_indx / 2) + 0.5
            ceil[x_indx, y_indx] = color_input

        ceil.show()

        time.sleep(DELTA)


if __name__ == "__main__":
    run(ceiling=Ceiling(test_mode=True), color=sys.argv[1], interval=sys.argv[2])
