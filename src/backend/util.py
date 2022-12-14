#!/usr/bin/env python3

""" Convenience functions"""

import colour
from typing import Union

from backend.backend_types import RGB


def hex_to_rgb(hex_str: str) -> RGB:
    color_obj = colour.Color(hex_str)
    rgb = color_obj.rgb
    rgb = [int(x * 255) for x in rgb]
    return rgb


def hex_to_color_obj(hex_str: str) -> colour.Color:
    return colour.Color(hex_str)


def color_obj_to_rgb(color_obj: colour.Color) -> RGB:
    rgb = color_obj.rgb
    rgb = [int(x * 255) for x in rgb]
    return rgb


def dim_color(color: Union[RGB, str]) -> RGB:
    pass


def clamp(num, min_value, max_value):
    num = max(min(num, max_value), min_value)
    return num


def sigmoid(x: float) -> float:
    return 1 / (1 + np.exp(-x))
