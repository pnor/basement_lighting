#!/usr/bin/env python3

# NAME: Frugal 2

import sys
import numpy as np
import time

from backend.ceiling import Ceiling
from backend.util import hex_to_rgb


def run(**kwargs):
    color = hex_to_rgb(kwargs["color"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_linear()

    time.sleep(1)
    ceil[int(np.random.random() * ceil.number_lights())] = color
    ceil.show()

    time.sleep(10)
    ceil[int(np.random.random() * ceil.number_lights())] = color
    ceil.show()


if __name__ == "__main__":
    run(ceiling=Ceiling(test_mode=True), color=sys.argv[1])
