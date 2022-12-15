#!/usr/bin/env python3

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
ceil.use_polar((0.5, 0.5), lights_per_row=CEILING_ROW_ARRANGEMENT)
ceil.testing_mode(CEILING_ROW_ARRANGEMENT, print_to_stdout=True)
ceil.clear()

# print(ceil._indexing._led_spacing._quadtree)
# for i in ceil._indexing._led_spacing._quadtree.elements():
#     print(i)
# print(list(ceil._indexing._led_spacing._quadtree.elements()))

# circle of radius
ceil[0.5, 0.5, 0.5] = (0, 0, 255)

# polar points
for theta in range(0, 360, 10):
    ceil[0.4, theta] = (255, 0, 0)


# corners test
# TODO

# unit circle
ceil.show()
