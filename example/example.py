#!/usr/bin/env python3

# NAME: example

from backend.ceiling import Ceiling
from backend.state import State


def run(**kwargs):
    ceil: Ceiling = kwargs["ceiling"]
    ceil.clear()

    # (Do some stuff)
    # ceil[0] = (255, 0, 0) # set the first pixel to red


if __name__ == "__main__":
    run(ceiling=State().create_ceiling())
