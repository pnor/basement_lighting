#!/usr/bin/env python3

import pdb
import colour
import sys

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
ceil.testing_mode(CEILING_ROW_ARRANGEMENT)
ceil.clear()


# point test
ceil[0, 0] = (255, 0, 0)

# unit circle
ceil.show()
