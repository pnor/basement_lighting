#!/usr/bin/env python3

import pdb
import colour
import sys
import time

from backend.ceiling import Ceiling
from backend.util import hex_to_rgb

if len(sys.argv) != 2:
    print("Usage: python fill.py [color hex string]")

color = sys.argv[1]

CEILING_ROW_ARRANGEMENT = [
    30,  # ---
    30,  # \
    30,  # ---
    30,  # \
    30,  # ---
    30,  # \
    20,  # ---
]
ceil = Ceiling(auto_write=False)
ceil.use_float_polar((0.5, 0.5), CEILING_ROW_ARRANGEMENT, 0.2)
ceil.testing_mode(CEILING_ROW_ARRANGEMENT, print_to_stdout=True)
ceil.clear()


# point test
i = 0
while True:
    time.sleep(0.2)

    ceil.clear()
    if i == 0:
        ceil[0.4, 0] = (255, 0, 0)

    elif i == 1:
        ceil[0.4, 90] = (0, 0, 255)

    elif i == 2:
        ceil[0.4, 180] = (0, 255, 0)

    elif i == 3:
        ceil[0.4, 270] = (255, 0, 255)
        ceil[0, 0, 0.5] = (255, 255, 255)

    i = (i + 1) % 4
    ceil.show()

# ceil[0.4, 90] = (0, 0, 255)
# ceil[0.4, 180] = (0, 255, 0)
# ceil[0.4, 270] = (255, 0, 255)

# unit circle
ceil.show()
