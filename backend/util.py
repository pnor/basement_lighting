#!/usr/bin/env python3

""" Convenience functions"""

from functools import lru_cache
import colour
from typing import Union, List, Tuple
import numpy as np

from numba import jit
from numpy._typing import NDArray

from backend.backend_types import RGB

# We import and type LEDSpace due to circular import dependency error /:
# import backend.led_locations as backend_led_space


# ===== Color Math =========================


def hex_to_rgb(hex_str: str) -> RGB:
    color_obj = colour.Color(hex_str)
    rgb = color_obj.rgb
    rgb = [int(x * 255) for x in rgb]
    return np.array(rgb)


def hex_to_color_obj(hex_str: str) -> colour.Color:
    return colour.Color(hex_str)


def color_obj_to_rgb(color_obj: colour.Color) -> RGB:
    rgb = color_obj.rgb
    rgb = [int(x * 255) for x in rgb]
    return np.array(rgb, dtype=np.uint8)


def color_format_to_obj(color: Union[RGB, str, colour.Color]) -> colour.Color:
    if isinstance(color, np.ndarray):
        col = color / 255
        return colour.Color(rgb=tuple(col))
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
    return np.array(rgb)


def dim_color(color: Union[RGB, str, colour.Color]) -> RGB:
    """Returns an extremely dimmed version of `color`
    `color` can be a hex string or rgb tuple"""
    return set_color_luminance(color, 0.01)


@lru_cache(maxsize=100)
def dim_color_by_amount(color: Union[RGB, str, colour.Color], dim_amount: float) -> RGB:
    """Dims a color by a percentage of its current luminance"""
    if isinstance(color, np.ndarray):
        return dim_color_by_amount_fast(color, dim_amount)

    c = color_format_to_obj(color)
    l = c.get_luminance()
    c.set_luminance(l * dim_amount)
    rgb = c.rgb
    rgb = (np.array(rgb) * 255).astype(int)
    return np.array(rgb)


@jit(fastmath=True, cache=True)
def dim_color_by_amount_fast(color: RGB, dim_amount: float) -> RGB:
    """Dims a color by a percentage of its current luminance
    Only works if color is a RGB tuple
    """
    return (color * dim_amount).astype(int)


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


@jit(fastmath=True, cache=True)
def mix_colors_fast(
    col_a: RGB,
    col_b: RGB,
) -> RGB:
    """Mixes `col_a` and `col_b` using maximums on each component"""
    return np.maximum(col_a, col_b)


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
    return np.array((np.array(rgb) * 255).astype(int))


# ===== Math =========================


@jit(fastmath=True, cache=True)
def clamp(num, min_value, max_value):
    return np.clip(num, min_value, max_value)


@jit(fastmath=True, cache=True)
def sigmoid(x: float) -> float:
    return 1 / (1 + np.exp(-x))


@jit(fastmath=True, cache=True)
def gaussian(x: float) -> float:
    return (1 / (np.sqrt(2 * np.pi))) * np.exp(-(1 / 2) * (x**2))


@jit(fastmath=True, cache=True)
def sigmoid_0_to_1(x: float, scale: float = 8) -> float:
    """Returns result between 0..1
    `x` should be in 0..1"""
    LARGE_NUM = scale
    sigmoid_input = (x - 0.5) * LARGE_NUM
    return sigmoid(sigmoid_input)


@jit(fastmath=True, cache=True)
def gaussian_0_to_1(x: float, scale: float = 7.75) -> float:
    """Returns result between 0..1
    `x` should be in 0..1"""
    LARGE_NUM = scale
    gaussian_input = (x - 0.5) * LARGE_NUM
    assert gaussian(gaussian_input) / 0.399 < 1
    return gaussian(gaussian_input) / 0.399


@jit(fastmath=True, cache=True)
def distance_formula(x1: float, y1: float, x2: float, y2: float):
    return np.sqrt(np.power(x2 - x1, 2) + np.power(y2 - y1, 2))


@jit(fastmath=True, cache=True)
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


@jit(fastmath=True, cache=True)
def rotate_vector(vector: NDArray[np.float64], theta: float) -> NDArray[np.float64]:
    """
    theta in radians
    """
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


@jit(fastmath=True, cache=True)
def fast_round(number: float, decimals: int) -> float:
    """Rounds `number` to `decimals` decimal points"""
    return np.around(number, decimals)
