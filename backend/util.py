#!/usr/bin/env python3

""" Convenience functions"""

import colour
import copy
from typing import Union, List, Tuple
from neopixel import NeoPixel
import numpy as np
from numba import jit

from backend.backend_types import RGB

# We import and type LEDSpace due to circular import dependency error /:
# import backend.led_locations as backend_led_space


# ===== Code working with LEDs =========================
def color_leds_in_area(
    x: float,
    y: float,
    effect_radius: float,
    color: RGB,
    led_spacing,
    pixels: NeoPixel,
):
    leds = led_spacing.get_LEDs_in_radius(x, y, effect_radius)
    for l in leds:
        dist = distance_formula(l.get_x(), l.get_y(), x, y)
        amp = max(0, 1 - (dist / effect_radius))

        res = dim_color_by_amount(color, amp)
        cur = pixels[l._index]
        final_color = (
            max(res[0], cur[0]),
            max(res[1], cur[1]),
            max(res[2], cur[2]),
        )
        pixels[l._index] = final_color


# ===== Color Math =========================


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
    if type(color) is list or type(color) is tuple:
        assert len(color) >= 3
        return colour.Color(rgb=tuple(np.array(color) / 255))
    else:
        return colour.Color(color)


def set_color_luminance(color: Union[RGB, str, colour.Color], luminance: float) -> RGB:
    """Returns `color` with its luminance set to `luminance` as a rgb tuple"""
    c = color_format_to_obj(color)
    c.set_luminance(luminance)
    rgb = c.rgb
    rgb = (np.array(rgb) * 255).astype(int)
    return tuple(rgb)


def dim_color(color: Union[RGB, str, colour.Color]) -> RGB:
    """Returns an extremely dimmed version of `color`
    `color` can be a hex string or rgb tuple"""
    return set_color_luminance(0.01)


def dim_color_by_amount(color: Union[RGB, str, colour.Color], dim_amount) -> RGB:
    """Dims a color by a percentage of its current luminance"""
    c = color_format_to_obj(color)
    l = c.get_luminance()
    c.set_luminance(l * dim_amount)
    rgb = c.rgb
    rgb = (np.array(rgb) * 255).astype(int)
    return tuple(rgb)


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


# ===== Math =========================


@jit
def clamp(num, min_value, max_value):
    num = max(min(num, max_value), min_value)
    return num


@jit
def sigmoid(x: float) -> float:
    return 1 / (1 + np.exp(-x))


@jit
def distance_formula(x1: float, y1: float, x2: float, y2: float):
    return np.sqrt(np.power(x2 - x1, 2) + np.power(y2 - y1, 2))


@jit
def polar_to_cartesian(r: float, theta: float) -> Tuple[float, float]:
    theta = np.radians(theta)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y


@jit
def transform_unit_circle_to_origin(
    x: float, y: float, orig_x: float, orig_y: float
) -> Tuple[float, float]:
    """
    Transforms coordinates in x: (-1..1), y: (-1..1) to box with width and height 1 centered on
    `(orig_x, orig_y)`.
    Mostly for converting the unit circle results in `polar_to_cartesian` to the space used to
    locate LEDs in 2D space.
    """
    x = (x / 2) + orig_x
    y = (y / 2) + orig_y
    return x, y
