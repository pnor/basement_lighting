#!/usr/bin/env python3

""" Convenience functions"""

from functools import lru_cache
import colour
import copy
from typing import Iterable, Union, List, Tuple
import numpy as np

from numba import jit
from numpy._typing import NDArray

from backend.backend_types import RGB, is_RGB
from backend.neopixel_wrapper import PixelWrapper

# We import and type LEDSpace due to circular import dependency error /:
# import backend.led_locations as backend_led_space


# ===== Code working with LEDs =========================
def color_leds_in_area(
    x: float,
    y: float,
    effect_radius: float,
    color: RGB,
    led_spacing,
    pixels: PixelWrapper,
):
    """Colors LEDs within `effect_radius` with `color`. Has an airbrush effect where it will merge
    `color` with the color already there"""
    leds = led_spacing.get_LEDs_in_radius(x, y, effect_radius)

    for l in leds:
        # NOTE: we ignore the type warning/error on pixels as checking types here is pretty slow
        # since this is a very hot section of code
        pixels[l._index] = _area_lerp_color(
            l._x, l._y, x, y, effect_radius, pixels[l._index], color
        )


@jit(nopython=True, fastmath=True)
def _area_lerp_color(
    led_x: float,
    led_y: float,
    x: float,
    y: float,
    effect_radius: float,
    cur_color: RGB,
    set_color: RGB,
) -> RGB:
    dist = distance_formula(led_x, led_y, x, y)
    amp = max(0, 1 - (dist / effect_radius))

    res = dim_color_by_amount_fast(set_color, amp)
    final_color = (
        max(res[0], cur_color[0]),
        max(res[1], cur_color[1]),
        max(res[2], cur_color[2]),
    )
    return final_color


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
    return tuple(rgb)


def color_format_to_obj(color: Union[RGB, str, colour.Color]) -> colour.Color:
    if is_RGB(color):
        return colour.Color(rgb=tuple(np.array(color) / 255))
    else:
        return colour.Color(color)


def color_format_to_rgb(color: Union[RGB, str, colour.Color]) -> RGB:
    return color_obj_to_rgb(color_format_to_obj(color))


def hsl_to_rgb(hue: float, sat: float, lum: float):
    """`hue`, `sat` and `lum` should all be 0..1"""
    colors_obj = colour.Color(hsl=(hue, sat, lum))
    return colors_obj.rgb


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
    return set_color_luminance(color, 0.01)


@lru_cache(maxsize=100)
def dim_color_by_amount(color: Union[RGB, str, colour.Color], dim_amount: float) -> RGB:
    """Dims a color by a percentage of its current luminance"""
    if is_RGB(color):
        return dim_color_by_amount_fast(color, dim_amount)

    c = color_format_to_obj(color)
    l = c.get_luminance()
    c.set_luminance(l * dim_amount)
    rgb = c.rgb
    rgb = (np.array(rgb) * 255).astype(int)
    return tuple(rgb)


@jit(fastmath=True)
def dim_color_by_amount_fast(color: RGB, dim_amount: float) -> RGB:
    """Dims a color by a percentage of its current luminance
    Only works if color is a RGB tuple
    """
    color = list(color)
    for i in range(len(color)):
        color[i] *= dim_amount
    return color


def interpolate_colors(
    col_a: Union[RGB, str, colour.Color],
    col_b: Union[RGB, str, colour.Color],
    progress: float,
) -> RGB:
    """Linearlly Interpolates `col_a` and `col_b` using `progress`"""
    color_a = color_format_to_obj(col_a)
    color_b = color_format_to_obj(col_b)
    prog_indx = int(clamp(progress, 0, 1) * 99)
    res_color = list(color_a.range_to(color_b, 100))[prog_indx]
    return colour_rgb_to_neopixel_rgb(res_color.rgb)


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


def colour_rgb_to_neopixel_rgb(rgb: Tuple[float, float, float]) -> RGB:
    """Convert the colour library's `rgb` which has componenets from 0..1 to neopixel's rgb which
    is 0..255"""
    return tuple((np.array(rgb) * 255).astype(int))


# ===== Math =========================


@jit(fastmath=True)
def clamp(num, min_value, max_value):
    num = max(min(num, max_value), min_value)
    return num


@jit(fastmath=True)
def sigmoid(x: float) -> float:
    return 1 / (1 + np.exp(-x))


@jit(fastmath=True)
def sigmoid_0_to_1(x: float) -> float:
    """Returns result between 0..1
    `x` should be in 0..1"""
    LARGE_NUM = 8
    sigmoid_input = (x - 0.5) * LARGE_NUM
    return sigmoid(sigmoid_input)


@jit(fastmath=True)
def distance_formula(x1: float, y1: float, x2: float, y2: float):
    return np.sqrt(np.power(x2 - x1, 2) + np.power(y2 - y1, 2))


@jit(fastmath=True)
def polar_to_cartesian(r: float, theta: float) -> Tuple[float, float]:
    theta = np.radians(theta)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y


@jit(fastmath=True)
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


@jit(fastmath=True)
def rotate_vector(vector: NDArray[np.float64], theta: float) -> NDArray[np.float64]:
    """
    theta in degrees
    """
    theta = np.radians(theta)
    rot_mat = np.array(
        [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]
    )
    # compute dot product
    vector_0 = float(vector[0])
    vector_1 = float(vector[1])
    x_comp = (vector_0 * rot_mat[0, 0]) + (vector_1 * rot_mat[1, 0])
    y_comp = (vector_0 * rot_mat[1, 0]) + (vector_1 * rot_mat[1, 1])
    return np.array([x_comp, y_comp])
    # return np.dot(vector, rot_mat)


@jit(fastmath=True)
def fast_round(number: float, decimals: int) -> float:
    """Rounds `number` to `decimals` decimal points"""
    return np.around(number, decimals)
