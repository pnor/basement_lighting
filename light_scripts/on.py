#!/usr/bin/env python3

# NAME: On
# Turn all lights white

from backend.ceiling import Ceiling


def run(**kwargs):
    ceil = Ceiling()
    ceil.fill([255, 255, 255])
    ceil.show()


if __name__ == "__main__":
    run()
