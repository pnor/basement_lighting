#!/usr/bin/env python3

# NAME: Rainbow Fill
# Fill all LEDs with changing colors based off the rainbow

import time
import numpy as np
import colour

from backend.ceiling import Ceiling
from backend.util import colour_rgb_to_neopixel_rgb

from numba import jit


def run(**kwargs):
    ceil = kwargs["ceiling"]
    ceil.clear()

    prog = np.random.random()
    col = colour.Color(hsl=(prog, 1, 0.5))

    cur = 0
    interval = 3

    FPS = 30
    DELTA = 1 / FPS
    while True:
        cur = (cur + DELTA) % interval

        col.set_hue(cur / interval)

        ceil.fill(colour_rgb_to_neopixel_rgb(col.rgb))
        ceil.show()

        time.sleep(DELTA)


if __name__ == "__main__":
    run(ceiling=Ceiling())
