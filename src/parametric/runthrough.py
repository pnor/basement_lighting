#!/usr/bin/env python3

# Runs a single LED throughout the light strip
#
# Usage:
# python runthrough.py [color hex string] [speed to traverse seconds]

import sys
import time
import copy

from backend.ceiling import Ceiling
from backend.util import color_range, dim_color

if len(sys.argv) != 3:
    print("Usage: python runthrough.py [color hex string] [speed to traverse seconds]")

color_input = sys.argv[1]
interval = float(sys.argv[2])

ceil = Ceiling()
ceil.use_linear()
ceil.clear()


# Getting range of colors for all LEDs to cycle through
TAIL_LENGTH = 4
colors = color_range(color_input, dim_color(color_input), TAIL_LENGTH)

FPS = 60
DELTA = 1 / FPS
cur_time = 0
while True:
    cur_time = (cur_time + DELTA) % interval
    indx = int((cur_time / interval) * ceil.NUMBER_LIGHTS)

    ceil.clear(False)
    for i in range(0, TAIL_LENGTH):
        ceil[indx - i] = colors[i]
    ceil.show()

    time.sleep(DELTA)
