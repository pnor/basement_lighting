#!/usr/bin/env python3

# Blinks every other LED to the same color
#
# Usage:
# python alternate.py [color hex string] [blink interval in seconds]

import sys
import time

from backend.ceiling import Ceiling
from backend.util import hex_to_rgb


def run(**kwargs):
    color_input = kwargs["color"]
    interval = float(kwargs["interval"])

    on_rgb = hex_to_rgb(color_input)
    off_rgb = [0] * len(on_rgb)

    ceil = Ceiling()
    ceil.testing_mode()
    ceil.clear()

    on = True

    while True:
        ceil[::2] = on_rgb if on else off_rgb
        ceil[1::2] = off_rgb if on else on_rgb
        ceil.show()
        on = not on
        time.sleep(interval)


if __name__ == "__main__":
    run(color=sys.argv[1], interval=sys.argv[2])
