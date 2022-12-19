#!/usr/bin/env python3

# NAME: On Warm
# Light all colors to a warm light color

from backend.ceiling import Ceiling
from backend.util import hex_to_rgb


def run(**kwargs):
    ceil = Ceiling()
    color = hex_to_rgb("#FCEEA7")
    ceil.fill(color)
    ceil.show()


if __name__ == "__main__":
    run()
