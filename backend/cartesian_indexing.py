#!/usr/bin/env python3

from typing import Optional, Tuple, List, Union
from backend.backend_types import RGB
from backend.indexing import Indexing
from backend.led_locations import LEDSpace
from backend.neopixel_wrapper import PixelWrapper
from backend.util import fast_round


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
            x = fast_round(x, 3)
            y = fast_round(y, 3)
            horiz_dist = fast_round(horiz_dist, 3)
            vert_dist = fast_round(vert_dist, 3)

            leds = self._led_spacing.get_LEDs_in_area(x, y, horiz_dist, vert_dist)
            for l in leds:
                self._pixels[l._index] = newvalue

        else:
            x, y = key

            # Round to improve caching ability of led spacing
            x = fast_round(x, 3)
            y = fast_round(y, 3)

            indx = self._led_spacing.get_closest_LED_index(x, y, self._search_range)
            if indx is not None:
                self._pixels[indx] = newvalue

    def prepare_to_send(self):
        self._led_spacing.save_quadtree_values_in_list()
