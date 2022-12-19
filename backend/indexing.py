#!/usr/bin/env python3

from typing import Any, Tuple, List, Union, Optional
import numpy as np

from backend.neopixel_wrapper import PixelWrapper
from backend.backend_types import RGB
from backend.led_locations import LEDSpace
from backend.util import (
    color_leds_in_area,
    polar_to_cartesian,
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

    def set(self, key: Any, newvalue: RGB) -> None:
        raise NotImplementedError("'Indexing' class is abstract and should not be used")

    def prepare_to_send(self):
        """Function called to prepare indexing objects to be pickled if they are using objects that
        do not handle pickling well.

        One primary example is the quadtree object
        """
        raise NotImplementedError("'Indexing' class is abstract and should not be used")


class LinearIndexing(Indexing):
    """Index into the light strip based on their order in sequence.
    This is the default way NeoPixels indexes the lights."""

    def __init__(self, pixels: PixelWrapper):
        self._pixels = pixels

    def get(self, key: int) -> Optional[RGB]:
        return self._pixels[key]

    def set(self, key: Union[int, slice], newvalue: RGB) -> None:
        if type(key) is slice:
            start = key.start if key.start else 0
            stop = key.stop if key.stop else len(self._pixels)
            step = key.step if key.step else 1
            for i in range(start, stop, step):
                self._pixels[i] = newvalue
        else:
            self._pixels[key] = newvalue

    def prepare_to_send(self):
        pass


class RowIndexing(Indexing):
    """
    Index into the light strip based on how they are arranged into rows.
    """

    def __init__(self, pixels: PixelWrapper, lights_per_row: List[int]):
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

    def prepare_to_send(self):
        pass


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
        self,
        pixels: PixelWrapper,
        lights_per_row: List[int],
        search_range: float = 0.2,
        cached_led_spacing: Optional[LEDSpace] = None,
    ):
        self._pixels = pixels
        self._lights_per_row = lights_per_row
        self._search_range = search_range

        if cached_led_spacing:
            self._led_spacing = cached_led_spacing
            self._led_spacing.clear_caches()
        else:
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

            # Round to improve caching ability of led spacing
            x = np.around(x, 3)
            y = np.around(y, 3)
            horiz_dist = np.around(horiz_dist, 3)
            vert_dist = np.around(vert_dist, 3)

            leds = self._led_spacing.get_LEDs_in_area(x, y, horiz_dist, vert_dist)
            for l in leds:
                self._pixels[l._index] = newvalue

        else:
            x, y = key

            # Round to improve caching ability of led spacing
            x = np.around(x, 3)
            y = np.around(y, 3)

            indx = self._led_spacing.get_closest_LED_index(x, y, self._search_range)
            if indx is not None:
                self._pixels[indx] = newvalue

    def prepare_to_send(self):
        self._led_spacing.save_quadtree_values_in_list()


class PolarIndexing(Indexing):
    """
    Index into the light strip using polar coordinates.
    Will select the single nearest LED, assuming origin is at the center of the grid formed by the LEDs
    """

    def __init__(
        self,
        pixels: PixelWrapper,
        lights_per_row: List[int],
        origin: Tuple[float, float] = (0.5, 0.5),
        search_range: float = 0.2,
        cached_led_spacing: Optional[LEDSpace] = None,
    ):
        self._pixels = pixels
        self._origin = origin
        self._lights_per_row = lights_per_row
        self._search_range = search_range

        if cached_led_spacing:
            self._led_spacing = cached_led_spacing
            self._led_spacing.clear_caches()
        else:
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

        # Round to improve caching ability of led spacing
        x = np.around(x, 3)
        y = np.around(y, 3)

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

            # Round to improve caching ability of led spacing
            x = np.around(x, 2)
            y = np.around(y, 2)
            r = np.around(r, 2)

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

            # Round to improve caching ability of led spacing
            x = np.around(x, 3)
            y = np.around(y, 3)

            indx = self._led_spacing.get_closest_LED_index(x, y, self._search_range)
            if indx is not None:
                self._pixels[indx] = newvalue

    def prepare_to_send(self):
        self._led_spacing.save_quadtree_values_in_list()


class FloatCartesianIndexing(Indexing):
    """Index into the light strip with floats as a grid on 2D space.
    Setting a decimal index will spread the light effect on nearby lights"""

    def __init__(
        self,
        pixels: PixelWrapper,
        lights_per_row: List[int],
        effect_radius: float = 0.2,
        cached_led_spacing: Optional[LEDSpace] = None,
    ):
        """
        `effect_range`: radius around point that will be affected
        """
        self._pixels = pixels
        self._lights_per_row = lights_per_row
        self._effect_radius = effect_radius

        if cached_led_spacing:
            self._led_spacing = cached_led_spacing
            self._led_spacing.clear_caches()
        else:
            self._led_spacing = LEDSpace()
            self._led_spacing.map_LEDs_in_zigzag(lights_per_row)

    def get(self, key: Tuple[float, float]) -> Optional[RGB]:
        """key: (x, y), x and y in (0..1)
        Returns nearest LED within `self._effect_radius` or None
        """
        x, y = key

        # Round to improve caching ability of led spacing
        x = np.around(x, 3)
        y = np.around(y, 3)

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

            # Round to improve caching ability of led spacing
            x = np.around(x, 3)
            y = np.around(y, 3)
            horiz_dist = np.around(horiz_dist, 3)
            vert_dist = np.around(vert_dist, 3)

            leds = self._led_spacing.get_LEDs_in_area(x, y, horiz_dist, vert_dist)
            for l in leds:
                self._pixels[l._index] = newvalue

        else:
            x, y = key

            # Round to improve caching ability of led spacing
            x = np.around(x, 3)
            y = np.around(y, 3)

            color_leds_in_area(
                x, y, self._effect_radius, newvalue, self._led_spacing, self._pixels
            )

    def prepare_to_send(self):
        self._led_spacing.save_quadtree_values_in_list()


class FloatPolarIndexing(Indexing):
    """
    Index into the light strip using float polar coordinates.
    If the index lies between multiple LEDs (not an integer) will spread the light effect on nearby lights
    """

    # NOTE: thinking, wherever the polar coords end up, select the closest of the 4 points around
    # it. Have a check if its v out of bounds ofc

    def __init__(
        self,
        pixels: PixelWrapper,
        lights_per_row: List[int],
        origin: Tuple[float, float] = (0.5, 0.5),
        effect_radius: float = 0.2,
        cached_led_spacing: Optional[LEDSpace] = None,
    ):
        self._pixels = pixels
        self._origin = origin
        self._lights_per_row = lights_per_row
        self._effect_radius = effect_radius

        if cached_led_spacing:
            self._led_spacing = cached_led_spacing
            self._led_spacing.clear_caches()
        else:
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
        # Round to improve caching ability of led spacing
        x = np.around(x, 3)
        y = np.around(y, 3)
        # get location in light strip
        indx = self._led_spacing.get_closest_LED_index(x, y, self._search_range)
        return None if indx is None else self._pixels[indx]

    def set(self, key: Tuple[float, float], newvalue: RGB) -> None:
        """
        key: either a tuple of 2 or 3 elements.
        If tuple of 2, represents (r, theta). Will set values with varying intensities of `newvalue` based
        on the point's distance from (r, theta).
        If tuple of 3, represetns (x, y, r) and will fill a circle of radius `r` centered at `(x,
        y)` with `newvalue`. When doing this, `(x, y)` ignore origin, and are based in (0..1, 0..1)
        """
        if len(key) == 3:
            x, y, r = key

            # Round to improve caching ability of led spacing
            x = np.around(x, 3)
            y = np.around(y, 3)
            r = np.around(r, 3)

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

            # Round to improve caching ability of led spacing
            x = np.around(x, 3)
            y = np.around(y, 3)

            color_leds_in_area(
                x, y, self._effect_radius, newvalue, self._led_spacing, self._pixels
            )

    def prepare_to_send(self):
        self._led_spacing.save_quadtree_values_in_list()
