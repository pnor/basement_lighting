#!/usr/bin/env python3

from neopixel import NeoPixel
from typing import Any, Tuple, List, Union, Optional
import numpy as np

from backend.backend_types import RGB
from backend.led_locations import LEDSpace
from backend.util import (
    dim_color,
    distance_formula,
    polar_to_cartesian,
    set_color_luminance,
    transform_unit_circle_to_origin,
)

"""
Abstraction of how indexing gets and sets indeces
"""


class Indexing:
    """
    Abstract class representing how getting indeces and setting indeces operate
    """

    def __init__(self):
        pass

    def get(self, key: Any) -> Optional[RGB]:
        raise NotImplementedError("'Indexing' class is abstract and should not be used")
        return (0, 0, 0)

    def set(self, key: Any, newvalue: RGB) -> None:
        raise NotImplementedError("'Indexing' class is abstract and should not be used")
        pass


class LinearIndexing(Indexing):
    """Index into the light strip based on their order in sequence.
    This is the default way NeoPixels indexes the lights."""

    def __init__(self, pixels: NeoPixel):
        self._pixels = pixels

    def get(self, key: int) -> Optional[RGB]:
        return self._pixels[key]

    def set(self, key: int, newvalue: RGB) -> None:
        self._pixels[key] = newvalue


class RowIndexing(Indexing):
    """
    Index into the light strip based on how they are arranged into rows.
    """

    def __init__(self, pixels: NeoPixel, lights_per_row: List[int]):
        self._pixels = pixels
        self.rows = lights_per_row

    def get(self, key: Tuple[int, int]) -> Optional[RGB]:
        """key: (row, col)"""
        row, col = key
        return self._pixels[self.row_col_to_indx(row, col)]

    def set(self, key: Union[Tuple[int, int], int], newvalue: RGB) -> None:
        """
        key: (row, col) or row
        if key is a tuple, will set one LED. If key is an int corresponding to the row, will set
        every LED in the row
        """
        if type(key) == tuple:
            row, col = key
            self._pixels[self.row_col_to_indx(row, col)] = newvalue
        elif type(key) == int:
            row = key
            for i in range(self.rows[row]):
                self._pixels[self.row_col_to_indx(row, i)] = newvalue
        else:
            raise NotImplementedError("key for row indexing was neither tuple or int")

    def row_col_to_indx(self, row: int, col: int) -> int:
        """Convert row and col position to index in light strip"""
        row = row % len(self.rows)
        indx = sum(self.rows[:row])
        if row % 2 == 0:
            indx += col
        else:
            indx += self.rows[row] - col
        return indx


class CartesianIndexing(Indexing):
    """Index into the light strip as a grid on 2D space.
    This is done by mapping lights in sequence to integer 2 dimensional coordinates.

    Assumes rows of LEDs are layed out like this:
    --->
     \
      \
    ----
    Indexing will yield the single closest LED to where user specified
    """

    def __init__(
        self, pixels: NeoPixel, lights_per_row: List[int], search_range: float = 0.2
    ):
        self._pixels = pixels
        self._lights_per_row = lights_per_row
        self._search_range = search_range

        self._led_spacing = LEDSpace()
        self._led_spacing.map_LEDs_in_zigzag(lights_per_row)

    def get(self, key: Tuple[float, float]) -> Optional[RGB]:
        """key: (x, y), x and y in (0..1)"""
        x, y = key
        indx = self._led_spacing.get_closest_LED_index(x, y, self._search_range)
        return None if indx is None else self._pixels[indx]

    def set(self, key: Union[Tuple[float, float], slice], newvalue: RGB) -> None:
        """key: either a tuple or slice.
        If tuple, (x, y) are in (0..1)
        If slice, is 2 tuples, (x1, y1):(x2, y2), and will set box spanning x1..x2 and y1..y2 to
        same color"""
        if type(key) is slice:
            x1, y1 = key.start
            x2, y2 = key.stop
            epsilon = 0.01  # little extra to get points on the borders
            horiz_dist = abs(x2 - x1)
            vert_dist = abs(y2 - y1)
            x1 -= epsilon
            y1 -= epsilon

            x = min(x1, x2) + (horiz_dist / 2)
            y = min(y1, y2) + (vert_dist / 2)

            leds = self._led_spacing.get_LEDs_in_area(x, y, horiz_dist, vert_dist)
            for l in leds:
                self._pixels[l._index] = newvalue

        else:
            x, y = key
            indx = self._led_spacing.get_closest_LED_index(x, y, self._search_range)
            if indx is not None:
                self._pixels[indx] = newvalue


class PolarIndexing(Indexing):
    """
    Index into the light strip using polar coordinates.
    Will select the single nearest LED, assuming origin is at the center of the grid formed by the LEDs
    """

    # NOTE: thinking, wherever the polar coords end up, select the closest of the 4 points around
    # it. Have a check if its v out of bounds ofc

    def __init__(
        self,
        pixels: NeoPixel,
        lights_per_row: List[int],
        origin: Tuple[float, float] = (0.5, 0.5),
        search_range: float = 0.2,
    ):
        self._pixels = pixels
        self._origin = origin
        self._lights_per_row = lights_per_row
        self._search_range = search_range

        self._led_spacing = LEDSpace()
        self._led_spacing.map_LEDs_in_zigzag(lights_per_row)

    def get(self, key: Tuple[float, float]) -> Optional[RGB]:
        """
        key: (radius, theta)
        """
        r, theta = key
        theta %= 360
        x, y = polar_to_cartesian(r, theta)
        x, y = transform_unit_circle_to_origin(x, y, self._origin[0], self._origin[1])
        # get location in light strip
        indx = self._led_spacing.get_closest_LED_index(x, y, self._search_range)
        return None if indx is None else self._pixels[indx]

    def set(
        self, key: Union[Tuple[float, float, float], Tuple[float, float]], newvalue: RGB
    ) -> None:
        """
        key: either a tuple of 2 or 3 elements.
        If tuple of 2, represents (r, theta)
        If tuple of 3, represetns (x, y, r) and will fill a circle of radius `r` centered at `(x,
        y)` with `newvalue`. When doing this, `(x, y)` ignore origin, and are based in (0..1, 0..1)
        """
        if len(key) == 3:
            x, y, r = key
            leds = self._led_spacing.get_LEDs_in_radius(x, y, r)
            for l in leds:
                self._pixels[l._index] = newvalue
        else:
            r, theta = key
            theta %= 360
            x, y = polar_to_cartesian(r, theta)
            x, y = transform_unit_circle_to_origin(
                x, y, self._origin[0], self._origin[1]
            )
            indx = self._led_spacing.get_closest_LED_index(x, y, self._search_range)
            if indx is not None:
                self._pixels[indx] = newvalue


class FloatCartesianIndexing(Indexing):
    """Index into the light strip with floats as a grid on 2D space.
    Setting a decimal index will spread the light effect on nearby lights"""

    def __init__(
        self, pixels: NeoPixel, lights_per_row: List[int], effect_radius: float = 0.2
    ):
        """
        `effect_range`: radius around point that will be affected
        """
        self._pixels = pixels
        self._lights_per_row = lights_per_row
        self._effect_radius = effect_radius

        self._led_spacing = LEDSpace()
        self._led_spacing.map_LEDs_in_zigzag(lights_per_row)

    def get(self, key: Tuple[float, float]) -> Optional[RGB]:
        """key: (x, y), x and y in (0..1)
        Returns nearest LED within `self._effect_radius` or None
        """
        x, y = key
        indx = self._led_spacing.get_closest_LED_index(x, y, self._effect_radius)
        return None if indx is None else self._pixels[indx]

    def set(self, key: Union[Tuple[float, float], slice], newvalue: RGB) -> None:
        """key: either a tuple or slice.
        If tuple, (x, y) are in (0..1). Will set values with varying intensities of `newvalue` based
        on the point's distance from (x, y).
        If slice, is 2 tuples, (x1, y1):(x2, y2), and will set box spanning x1..x2 and y1..y2 to
        same color"""
        if type(key) is slice:
            x1, y1 = key.start
            x2, y2 = key.stop
            epsilon = 0.01  # little extra to get points on the borders
            horiz_dist = abs(x2 - x1)
            vert_dist = abs(y2 - y1)
            x1 -= epsilon
            y1 -= epsilon

            x = min(x1, x2) + (horiz_dist / 2)
            y = min(y1, y2) + (vert_dist / 2)

            leds = self._led_spacing.get_LEDs_in_area(x, y, horiz_dist, vert_dist)
            for l in leds:
                self._pixels[l._index] = newvalue

        else:
            x, y = key
            leds = self._led_spacing.get_LEDs_in_radius(x, y, self._effect_radius)
            for l in leds:
                dist = distance_formula(l.get_x(), l.get_y(), x, y)
                amp = max(0, 1 - (dist / self._effect_radius))

                res = set_color_luminance(amp)
                cur = self._pixels[l._index]
                final_color = (
                    max(res[0], cur[0]),
                    max(res[1], cur[1]),
                    max(res[2], cur[2]),
                )
                self._pixels[l._index] = final_color


class FloatPolarIndexing(Indexing):
    """
    Index into the light strip using float polar coordinates.
    If the index lies between multiple LEDs (not an integer) will spread the light effect on nearby lights
    """

    # NOTE: thinking, wherever the polar coords end up, select the closest of the 4 points around
    # it. Have a check if its v out of bounds ofc

    def __init__(self, pixels: NeoPixel, rows: int, cols: int):
        self._pixels = pixels
        self.ROWS = rows
        self.COLS = cols

    def get(self, key: Tuple[float, float]) -> Optional[RGB]:
        """
        key: (radius, theta)
        """
        # TODO
        rad, theta = key
        return [0, 0, 0]

    def set(self, key: Tuple[float, float], newvalue: RGB) -> None:
        """
        key: (radius, theta)
        """
        # TODO
        rad, theta = key
