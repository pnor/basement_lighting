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
ceil.use_float_cartesian(CEILING_ROW_ARRANGEMENT, 0.4)
ceil.testing_mode(CEILING_ROW_ARRANGEMENT)
ceil.clear()

# print(ceil._indexing._led_spacing._quadtree)
# for i in ceil._indexing._led_spacing._quadtree.elements():
#     print(i)
# print(list(ceil._indexing._led_spacing._quadtree.elements()))


# point test
pdb.set_trace()
ceil[0.5, 0.5] = (255, 0, 0)

# unit circle
ceil.show()