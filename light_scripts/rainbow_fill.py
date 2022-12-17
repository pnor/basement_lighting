#!/usr/bin/env python3

# Fill all LEDs with changing colors based off the rainbow

import time
import numpy as np
import colour

from backend.ceiling import Ceiling
from backend.util import colour_rgb_to_neopixel_rgb

from numba import jit


def run(**kwargs):
    ceil = Ceiling()
    ceil.clear()

    prog = np.random.random()
    col = colour.Color(hsl=(prog, 1, 0.5))

    FPS = 60
    DELTA = 1 / 60
    while True:

        prog = (prog + (DELTA / 4)) % 1
        col.set_hue(prog)

        ceil.fill(colour_rgb_to_neopixel_rgb(col.rgb))
        ceil.show()

        time.sleep(DELTA)


if __name__ == "__main__":
    run()
