#!/usr/bin/env python3

# Create a glittering effect with the LEDs
#
# Usage:
# python sparkle.py [color hex string] [entire fade interval in seconds]


import sys
import time
import numpy as np

from backend.ceiling import Ceiling
from backend.util import color_range, dim_color


if len(sys.argv) != 3:
    print(
        "Usage: python sparkle.py [color hex string] [entire fade interval in seconds]"
    )

color_input = sys.argv[1]
interval = int(sys.argv[2])

ceil = Ceiling(auto_write=False)
ceil.use_linear()
ceil.clear()

colors = color_range(color_input, dim_color(color_input), 100)

FPS = 30
DELTA = 1 / FPS

progress_indeces = (((np.arange(100) / 99) ** 10) * 99).astype(int)
progresses = np.random.random_integers(0, 99, ceil.NUMBER_LIGHTS)

cur_time = 0

while True:
    cur_time += DELTA
    if cur_time > interval:
        cur_time = 0
        progresses = (progresses + 1) % 100
        for i in range(len(progresses)):
            ceil[i] = colors[progress_indeces[progresses[i]]]
        ceil.show()
    time.sleep(DELTA)
