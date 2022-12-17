#!/usr/bin/env python3


# Fades every LED on and off
#
# Usage:
# python fade.py [color hex string] [entire fade interval in seconds]
#
# Fade interval is time for it to go from on to off/vice versa

import sys
import time

from backend.ceiling import Ceiling
from backend.util import (
    clamp,
    dim_color,
    sigmoid,
    color_range,
)


def run(**kwargs):
    color_input = kwargs["color"]
    interval = float(kwargs["interval"])

    ceil = Ceiling()
    ceil.clear()

    cycle_colors = color_range(color_input, dim_color(color_input), 100)

    FPS = 30
    DELTA = 1 / FPS
    cur_time = 0
    forward = True
    while True:
        if forward:
            cur_time = clamp(cur_time + DELTA, 0, interval)
            if cur_time >= interval:
                forward = False
        else:
            cur_time = clamp(cur_time - DELTA, 0, interval)
            if cur_time <= 0:
                forward = True

        prog = cur_time / interval
        # use sigmoid to get better pulsing
        LARGE_NUM = 8
        sigmoid_input = (prog - 0.5) * LARGE_NUM
        prog = sigmoid(sigmoid_input)

        i = int(prog * 99)

        ceil.fill(cycle_colors[i])
        ceil.show()

        time.sleep(DELTA)


if __name__ == "__main__":
    run(color=sys.argv[1], interval=sys.argv[2])
