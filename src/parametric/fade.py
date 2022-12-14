#!/usr/bin/env python3


# Fades every LED on and off
#
# Usage:
# python fade.py [color hex string] [entire fade interval in seconds]
#
# Fade interval is time for it to go from on to off/vice versa

import colour
import sys
import time
import copy

from backend.ceiling import Ceiling
from backend.util import (
    clamp,
    color_obj_to_rgb,
    dim_color,
    hex_to_color_obj,
    hex_to_rgb,
    sigmoid,
    color_range,
)


if len(sys.argv) != 3:
    print("Usage: python fade.py [color hex string] [entire fade interval in seconds]")

color_input = sys.argv[1]
interval = int(sys.argv[2])

ceil = Ceiling(auto_write=True)
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

    time.sleep(DELTA)
