#!/usr/bin/env python3

# NAME: On
# Turn all lights white

from backend.ceiling import Ceiling
from backend.state import State


def run(**kwargs):
    ceil = kwargs["ceiling"]
    ceil.fill([255, 255, 255])
    ceil.show()


if __name__ == "__main__":
    run(ceiling=State().create_ceiling())
