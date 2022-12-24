#!/usr/bin/env python3

# NAME: Edges


import sys

from backend.ceiling import Ceiling
from backend.util import hex_to_rgb


def run(**kwargs):
    color = kwargs["color"]

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_cartesian()
    ceil.fill(hex_to_rgb(color))

    EDGE_PADDING = 0.08

    lower = EDGE_PADDING
    upper = 1 - EDGE_PADDING
    ceil[(lower, lower):(upper, upper)] = (0, 0, 0)
    ceil.show()


if __name__ == "__main__":
    run(ceiling=Ceiling(test_mode=True), color=sys.argv[1])
