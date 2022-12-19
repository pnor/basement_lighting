#!/usr/bin/env python3

# NAME: Circle Out
# Create ripples outward

import sys
import time

from backend.ceiling import Ceiling
from backend.util import hex_to_rgb

from backend.led_locations import LEDSpace


def run(**kwargs):
    color_input = kwargs["color"]
    interval = float(kwargs["interval"])

    ceil = Ceiling()
    ceil.use_polar((0.5, 0.5))

    color = hex_to_rgb(color_input)

    max_radius = 0.7

    FPS = 60
    DELTA = 1 / FPS
    cur_time = 0
    while True:
        cur_time = (cur_time + DELTA) % interval
        rad = (cur_time / interval) * max_radius

        ceil.clear(False)
        ceil[0.5, 0.5, rad] = color
        ceil[0.5, 0.5, rad - 0.05] = (0, 0, 0)
        ceil.show()

        time.sleep(DELTA)


if __name__ == "__main__":
    run(color=sys.argv[1], interval=sys.argv[2])
