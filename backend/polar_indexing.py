#!/usr/bin/env python3

from typing import Any, Tuple, List, Union, Optional
import numpy as np
from backend.indexing import Indexing

from backend.neopixel_wrapper import PixelWrapper
from backend.backend_types import RGB
from backend.led_locations import LEDSpace
from backend.util import (
    fast_round,
    polar_to_cartesian,
    transform_unit_circle_to_origin,
)


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
        x = fast_round(x, 3)
        y = fast_round(y, 3)

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
            x = fast_round(x, 2)
            y = fast_round(y, 2)
            r = fast_round(r, 2)

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
            x = fast_round(x, 3)
            y = fast_round(y, 3)

            indx = self._led_spacing.get_closest_LED_index(x, y, self._search_range)
            if indx is not None:
                self._pixels[indx] = newvalue

    def prepare_to_send(self):
        self._led_spacing.save_quadtree_values_in_list()
