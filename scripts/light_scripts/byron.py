#!/usr/bin/env python3

# NAME: byron

import sys

from backend.ceiling import Ceiling
from backend.util import hex_to_rgb


def run(**kwargs):
    color = kwargs["color"]

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_cartesian()

    color_primary = hex_to_rgb("#0000ff")
    color_secondary = hex_to_rgb("#aaaaff")

    ceil.fill(color_primary)
    ceil[(0, 0):(0.25, 0.25)] = color_secondary
    ceil[(0.75, 0):(1, 0.25)] = color_secondary
    ceil[(0.25, 0.25):(0.75, 0.75)] = color_secondary
    ceil[(0, 0.75):(0.25, 1)] = color_secondary
    ceil[(0.75, 0.75):(1, 1)] = color_secondary
    ceil.show()


if __name__ == "__main__":
    run(ceiling=Ceiling())
