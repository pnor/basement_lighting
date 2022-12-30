#!/usr/bin/env python3

# NAME: jared

import sys

from backend.ceiling import Ceiling
from backend.util import hex_to_rgb


def run(**kwargs):
    color = kwargs["color"]

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_linear()

    ceil.clear()

    ceil[0:3] = hex_to_rgb("#042eba")
    ceil[3:8] = hex_to_rgb("#310169")
    ceil.show()

    raise NotImplemented("jared type script")


if __name__ == "__main__":
    run(ceiling=Ceiling())
