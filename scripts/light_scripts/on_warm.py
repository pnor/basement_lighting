#!/usr/bin/env python3

# NAME: On Warm
# Light all colors to a warm light color

from backend.ceiling import Ceiling
from backend.state import State
from backend.util import color_format_to_obj, color_obj_to_rgb, hex_to_rgb


def run(**kwargs):
    ceil = kwargs["ceiling"]
    color_obj = color_format_to_obj("#FCEEA7")
    color_obj.set_luminance(0.7)
    color = color_obj_to_rgb(color_obj)
    ceil.fill(color)
    ceil.show()


if __name__ == "__main__":
    run(ceiling=State().create_ceiling())
