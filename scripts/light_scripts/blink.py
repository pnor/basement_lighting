#!/usr/bin/env python3

# NAME: Blink
# Blinks every LED to the same color


import sys
import time

from backend.ceiling import Ceiling
from backend.state import State
from backend.util import hex_to_rgb


def run(**kwargs):
    color_input = kwargs["color"]
    interval = float(kwargs["interval"])

    on_rgb = hex_to_rgb(color_input)
    off_rgb = [0] * len(on_rgb)

    ceil = kwargs["ceiling"]
    ceil.clear()

    on = True

    while True:
        ceil.fill(on_rgb if on else off_rgb)
        ceil.show()
        on = not on
        time.sleep(interval)


if __name__ == "__main__":
    run(ceiling=State().create_ceiling(), color=sys.argv[1], interval=sys.argv[2])
