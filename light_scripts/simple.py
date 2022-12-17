#!/usr/bin/env python3


import time
import numpy as np
import colour
import pdb

from backend.ceiling import Ceiling
from backend.util import colour_rgb_to_neopixel_rgb, rotate_vector


def run(**kwargs):
    ceil = Ceiling()
    ceil.clear()
    # pdb.set_trace()
    ceil[0] = (255, 0, 0)
    ceil[1] = (0, 255, 0)
    ceil[2] = (0, 0, 255)
    ceil.show()


if __name__ == "__main__":
    run()
