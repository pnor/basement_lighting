#!/usr/bin/env python3


import colour
import sys

from backend.ceiling import Ceiling
from backend.util import hex_to_rgb

if len(sys.argv) != 2:
    print("Usage: python fill.py [color hex string]")

color = sys.argv[1]

ceil = Ceiling(number_lights=100, auto_write=True)
# ceil.use_cartesian([14, 18, 16, 22, 15, 14], 0.1)
ceil.use_cartesian()
ceil.testing_mode()
ceil.clear()

print(ceil._indexing._led_spacing._quadtree)
# for i in ceil._indexing._led_spacing._quadtree.elements():
#     print(i)
# print(list(ceil._indexing._led_spacing._quadtree.elements()))


ceil[0, 0] = (255, 0, 0)
ceil[0, 0.2] = (255, 0, 0)
ceil[0, 0.4] = (255, 0, 0)
ceil[0, 0.6] = (255, 0, 0)
ceil[0, 0.8] = (255, 0, 0)
ceil[0, 1] = (255, 0, 0)

ceil[0.3, 0] = (0, 255, 0)
ceil[0.3, 0.2] = (0, 255, 0)
ceil[0.3, 0.4] = (0, 255, 0)
ceil[0.3, 0.6] = (0, 255, 0)
ceil[0.3, 0.8] = (0, 255, 0)
ceil[0.3, 1] = (0, 255, 0)

ceil[0.6, 0] = (0, 0, 255)
ceil[0.6, 0.2] = (0, 0, 255)
ceil[0.6, 0.4] = (0, 0, 255)
ceil[0.6, 0.6] = (0, 0, 255)
ceil[0.6, 0.8] = (0, 0, 255)
ceil[0.6, 1] = (0, 0, 255)
