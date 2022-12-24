#!/usr/bin/env python3

# NAME: Radial

import sys

from backend.ceiling import Ceiling
from backend.util import hex_to_rgb


def run(**kwargs):
    color = kwargs["color"]

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_float_cartesian(effect_radius=0.6)
    ceil[0.5, 0.5] = hex_to_rgb(color)
    ceil.show()


if __name__ == "__main__":
    run(ceiling=Ceiling(test_mode=True), color=sys.argv[1])
