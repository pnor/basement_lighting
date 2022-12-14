#!/usr/bin/env python3

""" Convenience functions"""

import colour
import copy
from typing import Union, List

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


def color_format_to_obj(color: Union[RGB, str, colour.Color]) -> colour.Color:
    if color is RGB:
        return colour.Color(rgb=color)
    else:
        return colour.Color(color)


def dim_color(color: Union[RGB, str, colour.Color]) -> RGB:
    """Returns an extremely dimmed version of `color`
    `color` can be a hex string or rgb tuple"""
    c = color_format_to_obj(color)
    c.set_luminance(0.001)
    return c.rgb


def color_range(
    color_start: Union[RGB, str, colour.Color],
    color_end: Union[RGB, str, colour.Color],
    number: int,
) -> List[RGB]:
    """Returns `number` colors spanning the range from `color_start` to `color_end`"""
    c1 = color_format_to_obj(color_start)
    c2 = color_format_to_obj(color_end)
    colors_spanning = list(c1.range_to(c2, number))
    return [color_obj_to_rgb(c) for c in colors_spanning]


def clamp(num, min_value, max_value):
    num = max(min(num, max_value), min_value)
    return num


def sigmoid(x: float) -> float:
    return 1 / (1 + np.exp(-x))
