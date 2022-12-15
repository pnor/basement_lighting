#!/usr/bin/env python3

# Blinks every other LED to the same color
#
# Usage:
# python blink.py [color hex string] [blink interval in seconds]

import sys
import time

from backend.ceiling import Ceiling
from backend.util import hex_to_rgb

if len(sys.argv) != 2:
    print("Usage: python alternate.py [color hex string] [blink interval in seconds]")

color_input = sys.argv[1]
interval = float(sys.argv[2])

on_rgb = hex_to_rgb(color_input)
off_rgb = [0] * len(on_rgb)

ceil = Ceiling()
ceil.clear()

on = True

while True:
    # ceil doesn't support slicing (yet??)
    for i in range(ceil.NUMBER_LIGHTS):
        if i % 2 == 0:
            ceil[i] = on_rgb if on else off_rgb
        else:
            ceil[i] = off_rgb if on else on_rgb

    # ceil._pixels[::2] = on_rgb if on else off_rgb
    # ceil._pixels[1::2] = off_rgb if on else on_rgb
    ceil.show()
    on = not on
    time.sleep(interval)
