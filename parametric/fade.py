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

from backend.ceiling import Ceiling
from backend.util import clamp, color_obj_to_rgb, hex_to_color_obj, hex_to_rgb

if len(sys.argv) != 2:
    print("Usage: python fade.py [color hex string] [entire fade interval in seconds]")

color_input = sys.argv[1]
interval = int(sys.argv[2])

ceil = Ceiling(auto_write=True)
ceil.clear()


# Getting range of colors for all LEDs to cycle through
on_color_obj = hex_to_color_obj(color_input)
off_color_obj = hex_to_color_obj("#000000")
color_range = list(on_color_obj.range_to(off_color_obj, 100))
cycle_colors = [color_obj_to_rgb(c) for c in color_range]

FPS = 60
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

    i = int((cur_time / interval) * 100)

    ceil.fill(cycle_colors[i])

    time.sleep(DELTA)
