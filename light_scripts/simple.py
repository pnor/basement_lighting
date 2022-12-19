#!/usr/bin/env python3


import time
import numpy as np
import colour
import pdb

from backend.ceiling import Ceiling
from backend.util import colour_rgb_to_neopixel_rgb, rotate_vector


def run(**kwargs):
    ceil = kwargs["ceiling"]
    ceil.clear()
    # pdb.set_trace()
    ceil[:29] = (255, 0, 0)
    ceil[29:58] = (0, 0, 255)
    ceil[58:90] = (0, 255, 0)
    ceil[90:119] = (255, 0, 0)
    ceil[119:151] = (255, 255, 30)
    ceil[151:180] = (255, 0, 100)
    ceil[180:200] = (255, 255, 255)
    ceil.show()


if __name__ == "__main__":
    run(ceiling=Ceiling())
