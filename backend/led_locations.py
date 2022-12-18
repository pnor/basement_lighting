#!/usr/bin/env python3

"""
Estimate the location of LEDs in 2D space based on how they are arranged
"""

from typing import List, Optional
from smartquadtree import Quadtree

from backend.util import distance_formula

# ====
import cProfile, pstats, io
from pstats import SortKey

# ====


class LED:
    def __init__(self, x: float, y: float, index: int):
        self._x = x
        self._y = y
        self._index = index

    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

    def __str__(self) -> str:
        return "LED(x: %s, y: %s, index: %s)" % (self._x, self._y, self._index)

    def __repr__(self) -> str:
        return "LED(x: %s, y: %s, index: %s)" % (self._x, self._y, self._index)


class LEDSpace:
    """
    Maintains estimated locations of LEDs in 2D space. Can query locations in the space to get the
    nearest LED for that location.

    The 2D space is a 1x1 square, with x going from (0..1) and y going from (0..1)
    """

    def __init__(self) -> None:
        self._quadtree = Quadtree(0.5, 0.5, 1, 1)

    def map_LEDs_in_zigzag(self, lights_per_row: List[int]) -> None:
        """
        Map LEDs based on the row information in `lights_per_row` to positions in 2D space.
        Asssumes LEDs are layed out like so:
          ---> n
           \
            \
        0  ----

        `lights_per_row`: first index represents the bottomost row, closest to the data connection
        of the pi

        For horizontal lines, the first LED in the row corresponds to the leftmost point and the
        last LED corresponds to the *2nd to last* rightmost point.

        For right to left diagonals, the first LED (rightmost one) corresponds to the rightmost
        LED that is in the same vertical line as the LEDs of the previous row. The last LED
        (leftmost one) corresponds to the leftmost LED right below the start of the next horizontal row.

        This is done to compensate for the fact that the first and last LED technically are in 2 rows
        """
        indx = 0

        if len(lights_per_row) == 1:
            row_height = 1
        else:
            row_height = 1 / (len(lights_per_row) // 2)

        for i in range(len(lights_per_row)):
            lights = range(lights_per_row[i])

            number_lights = lights_per_row[i]

            for j in lights:
                x: float
                y: float
                if i % 2 == 0:  # horizontal -
                    x = j / number_lights
                    y = (i / 2) * row_height
                else:  # diagonal \
                    x = 1 - (j / number_lights)
                    # x = j / number_lights
                    y = ((i // 2) * row_height) + ((j / number_lights) * (row_height))

                led = LED(x, y, indx)
                self._quadtree.insert(led)

                indx += 1

    def get_LEDs_in_area(
        self, x: float, y: float, width: float, height: float
    ) -> List[LED]:
        """
        `width`: width of box centered on `(x, y)`
        `height`: height of box centered on `(x, y)`
        """

        # pr = cProfile.Profile()
        # pr.enable()
        # # ... do something ...

        left = x - (width / 2)
        right = x + (width / 2)
        bot = y - (height / 2)
        top = y + (height / 2)

        self._quadtree.set_mask([(left, bot), (left, top), (right, top), (right, bot)])

        res: List[LED] = []
        for led in self._quadtree.elements():
            res += [led]

        self._quadtree.set_mask(None)

        # pr.disable()
        # s = io.StringIO()
        # sortby = SortKey.CUMULATIVE
        # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        # ps.print_stats()
        # print(s.getvalue())

        return res

    def get_LEDs_in_radius(self, x: float, y: float, radius: float) -> List[LED]:
        """
        `radius` around (x, y) of points should be returned
        """
        res = self.get_LEDs_in_area(x, y, radius * 2, radius * 2)
        return list(
            filter(
                lambda l: distance_formula(x, y, l.get_x(), l.get_y()) <= radius, res
            )
        )

    def get_closest_LED_index(
        self, x: float, y: float, max_distance: float = 0.30
    ) -> Optional[int]:
        """
        `max_distance` is the largest distance a point will be returned from the queried point querying for specific
        location in 2D space
        """
        results = self.get_LEDs_in_area(x, y, max_distance * 2, max_distance * 2)

        closest: Optional[LED] = None
        closest_distance = 9999999
        for led in results:
            distance = distance_formula(x, y, led.get_x(), led.get_y())
            if distance > max_distance:
                continue
            if closest is None or distance < closest_distance:
                closest = led
                closest_distance = distance
        self._quadtree.set_mask(None)

        return None if closest is None else closest._index
