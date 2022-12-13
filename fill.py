#!/usr/bin/env python3

# Sets every LED to the same color
#
# Usage:
# python fill.py [color hex string]

import colour
import sys

from backend.ceiling import Ceiling


print(sys.stdin)

col = input()

color_obj = colour.Color(col)
color_rgb = list(color.rgb)

ceil = Ceiling()
ceil.fill(color_rgb)
