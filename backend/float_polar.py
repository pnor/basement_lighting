#!/usr/bin/env python3

from typing import Tuple, List, Union, Optional
from backend.indexing import Indexing

from backend.neopixel_wrapper import PixelWrapper
from backend.backend_types import RGB
from backend.led_locations import LEDSpace
from backend.util import (
    color_leds_in_area,
    fast_round,
    polar_to_cartesian,
    transform_unit_circle_to_origin,
)


class FloatPolarIndexing(Indexing):
    """
    Index into the light strip using float polar coordinates.
    If the index lies between multiple LEDs (not an integer) will spread the light effect on nearby lights
    """

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
        x = fast_round(x, 3)
        y = fast_round(y, 3)
        # get location in light strip
        indx = self._led_spacing.get_closest_LED_index(x, y, self._effect_radius)
        return None if indx is None else self._pixels[indx]

    def set(
        self, key: Union[Tuple[float, float, float], Tuple[float, float]], newvalue: RGB
    ) -> None:
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
            x = fast_round(x, 3)
            y = fast_round(y, 3)
            r = fast_round(r, 3)

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

            color_leds_in_area(
                x, y, self._effect_radius, newvalue, self._led_spacing, self._pixels
            )

    def prepare_to_send(self):
        self._led_spacing.save_quadtree_values_in_list()
