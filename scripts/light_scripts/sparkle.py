#!/usr/bin/env python3

# NAME: Sparkle
# Create a glittering effect with the LEDs


import sys
import time
import numpy as np

from backend.ceiling import Ceiling
from backend.util import color_range, dim_color


def run(**kwargs):
    color_input = kwargs["color"]
    interval = float(kwargs["interval"])

    ceil = kwargs["ceiling"]
    ceil.use_linear()
    ceil.clear()

    colors = color_range(dim_color(color_input), color_input, 100)
    colors = colors + list(reversed(colors))

    FPS = 60
    DELTA = 1 / FPS

    progress_indeces = (((np.arange(100) / 99) ** 10) * 99).astype(int)
    progress_indeces = list(progress_indeces) + list(reversed(progress_indeces))
    progresses = np.random.randint(0, 199 + 1, ceil.NUMBER_LIGHTS)

    cur_time = 0

    while True:
        cur_time += DELTA
        if cur_time > (interval / 200):
            cur_time = 0
            progresses = (progresses + 1) % 200
            for i in range(len(progresses)):
                ceil[i] = colors[progress_indeces[progresses[i]]]

            ceil.show()
        time.sleep(DELTA)


if __name__ == "__main__":
    run(ceiling=Ceiling(), color=sys.argv[1], interval=sys.argv[2])
