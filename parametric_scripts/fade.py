#!/usr/bin/env python3


# NAME: Fade
# Fades every LED on and off

import sys
import time

from backend.ceiling import Ceiling
from backend.util import (
    clamp,
    dim_color,
    sigmoid,
    color_range,
    sigmoid_0_to_1,
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
        prog = sigmoid_0_to_1(prog)

        i = int(prog * 99)

        ceil.fill(cycle_colors[i])
        ceil.show()

        time.sleep(DELTA)


if __name__ == "__main__":
    run(color=sys.argv[1], interval=sys.argv[2])
