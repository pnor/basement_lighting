#!/usr/bin/env python3

# Runs a single LED throughout the light strip
#
# Usage:
# python runthrough.py [color hex string] [speed to traverse seconds]

import sys
import time
import copy

from backend.ceiling import Ceiling
from backend.util import color_obj_to_rgb, hex_to_color_obj

if len(sys.argv) != 3:
    print("Usage: python runthrough.py [color hex string] [speed to traverse seconds]")

color_input = sys.argv[1]
interval = float(sys.argv[2])

ceil = Ceiling()
ceil.use_linear()
ceil.clear()


# Getting range of colors for all LEDs to cycle through
TAIL_LENGTH = 4
on_color_obj = hex_to_color_obj(color_input)
off_color_obj = copy.deepcopy(on_color_obj)
off_color_obj.luminance = 0.01
color_range = list(on_color_obj.range_to(off_color_obj, TAIL_LENGTH))
colors = [color_obj_to_rgb(c) for c in color_range]

FPS = 60
DELTA = 1 / FPS
cur_time = 0
while True:
    cur_time = (cur_time + DELTA) % interval
    indx = int((cur_time / interval) * ceil.NUMBER_LIGHTS)

    ceil.fill((0, 0, 0))
    for i in range(0, TAIL_LENGTH):
        ceil[indx - i] = colors[i]
    ceil.show()

    time.sleep(DELTA)
