#!/usr/bin/env python3

# NAME: Box


import sys

from backend.ceiling import Ceiling
from backend.util import hex_to_rgb


def run(**kwargs):
    color = kwargs["color"]

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_cartesian()
    ceil[(0.25, 0.25):(0.75, 0.75)] = hex_to_rgb(color)
    ceil.show()


if __name__ == "__main__":
    run(ceiling=Ceiling(test_mode=True), color=sys.argv[1])
