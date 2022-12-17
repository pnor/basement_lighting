#!/usr/bin/env python3

# Blinks every LED to the same color
#
# Usage:
# python blink.py [color hex string] [blink interval in seconds]

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
    ceil.clear()

    on = True

    while True:
        ceil.fill(on_rgb if on else off_rgb)
        ceil.show()
        on = not on
        time.sleep(interval)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python alternate.py [color hex string] [blink interval in seconds]"
        )

    run(color=sys.argv[1], interval=sys.argv[2])
