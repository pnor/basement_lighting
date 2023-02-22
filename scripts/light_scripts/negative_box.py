#!/usr/bin/env python3

# NAME: Negative Box

import sys

from backend.ceiling import Ceiling
from backend.state import State
from backend.util import hex_to_rgb


def run(**kwargs):
    color = kwargs["color"]

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_cartesian()
    ceil.fill(hex_to_rgb(color))
    ceil[(0.25, 0.25):(0.75, 0.75)] = (0, 0, 0)
    ceil.show()


if __name__ == "__main__":
    run(ceiling=State().create_ceiling(), color=sys.argv[1])
