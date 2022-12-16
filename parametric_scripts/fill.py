#!/usr/bin/env python3

# Sets every LED to the same color
#
# Usage:
# python fill.py [color hex string]

import colour
import sys

from backend.ceiling import Ceiling
from backend.util import hex_to_rgb


def run(**kwargs):
    color = kwargs["color"]

    ceil = Ceiling()
    ceil.fill(hex_to_rgb(color))
    ceil.show()


if __name__ == "__main__":
    run(color=sys.argv[1])
