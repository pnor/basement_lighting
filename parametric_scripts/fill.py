#!/usr/bin/env python3

# NAME: Fill
# Sets every LED to the same color

import sys

from backend.ceiling import Ceiling
from backend.util import hex_to_rgb


def run(**kwargs):
    color = kwargs["color"]

    ceil = kwargs["ceiling"]
    ceil.fill(hex_to_rgb(color))
    ceil.show()


if __name__ == "__main__":
    run(ceiling=Ceiling(), color=sys.argv[1])
