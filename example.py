#!/usr/bin/env python3


from backend.ceiling import Ceiling


def run(**kwargs):
    ceil = Ceiling()
    ceil.clear()

    # (Do some stuff)
    # ceil[0] = (255, 0, 0) # set the first pixel to red


if __name__ == "__main__":
    run()
