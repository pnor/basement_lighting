#!/usr/bin/env python3

# NAME: Frugal

import sys
import numpy as np

from backend.ceiling import Ceiling
from backend.util import hex_to_rgb


def run(**kwargs):
    color = hex_to_rgb(kwargs["color"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_linear()
    ceil[int(np.random.random() * ceil.NUMBER_LIGHTS)] = color
    ceil.show()


if __name__ == "__main__":
    run(ceiling=Ceiling(test_mode=True), color=sys.argv[1])
