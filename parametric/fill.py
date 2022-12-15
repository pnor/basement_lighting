#!/usr/bin/env python3

# Sets every LED to the same color
#
# Usage:
# python fill.py [color hex string]

import colour
import sys

from backend.ceiling import Ceiling
from backend.util import hex_to_rgb

if len(sys.argv) != 2:
    print("Usage: python fill.py [color hex string]")

color = sys.argv[1]

ceil = Ceiling(auto_write=True)
ceil.fill(hex_to_rgb(color))
