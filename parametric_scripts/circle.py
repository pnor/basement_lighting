#!/usr/bin/env python3

# NAME: Circle
# Sets a circle to a solid color


import sys

from backend.ceiling import Ceiling
from backend.util import hex_to_rgb


def run(**kwargs):
    color = kwargs["color"]

    ceil = Ceiling()
    ceil.use_polar((0.5, 0.5))
    ceil[0.5, 0.5, 0.35] = hex_to_rgb(color)
    ceil.show()


if __name__ == "__main__":
    run(color=sys.argv[1])
