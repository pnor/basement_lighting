#!/usr/bin/env python3

import board
import neopixel

from microcontroller import Pin
from typing import Callable, Any, Optional

from backend.test_display import TestDisplay

from .backend_types import RGB

from .indexing import *

"""
A layer between the neopixel API and our light scripts to abstract away all that coordinate math
"""

# Basement related constants
NUMBER_LIGHTS = 200
CEILING_ROW_ARRANGEMENT = [
    20,  # ---
    40,  # \
    20,  # ---
    40,  # \
    20,  # ---
    40,  # \
    20,  # ---
]


class Ceiling:
    def __init__(
        self,
        io_pin: Pin = board.D21,
        number_lights: int = NUMBER_LIGHTS,
        auto_write: bool = False,
    ):
        self._pixels = neopixel.NeoPixel(
            io_pin, number_lights, auto_write=auto_write, pixel_order=neopixel.RGB
        )
        self._indexing = LinearIndexing(self._pixels)
        self.NUMBER_LIGHTS = NUMBER_LIGHTS
        self._test_display = None

    def clear(self, show=True) -> None:
        """Set every pixel to black (and updates the LEDs)"""
        self.fill([0, 0, 0])
        if show:
            self._pixels.show()

    def fill(self, clear_color: RGB) -> None:
        """Set every pixel to the given color"""
        self._pixels.fill(clear_color)

    def show(self) -> None:
        """Update all pixels with updated colors at once"""
        self._pixels.show()
        if self._test_display:
            self._test_display.show()

    def set_auto_write(self, auto_write: bool) -> None:
        self._pixels.auto_write = auto_write

    def rows(self) -> Optional[List[int]]:
        """Returns rows information if the indexing is row indexing"""
        if isinstance(self._indexing, RowIndexing):
            return self._indexing.rows
        else:
            return None

    def test_display(self, lights_per_row: Optional[List[int]] = None):
        self._test_display = TestDisplay(
            lights_per_row if lights_per_row else CEILING_ROW_ARRANGEMENT, self._pixels
        )

    def indexing(self) -> Indexing:
        """Return the current Indexing object"""
        return self._indexing

    def use_linear(self):
        "Use linear indexing"
        self._indexing = LinearIndexing(self._pixels)

    def use_row(self, lights_per_row: List[int] = CEILING_ROW_ARRANGEMENT):
        """Use row based indexing"""
        self._indexing = RowIndexing(self._pixels, lights_per_row)

    def use_cartesian(
        self,
        lights_per_row: List[int] = CEILING_ROW_ARRANGEMENT,
        search_range: float = 0.2,
    ):
        """Use cartesian indexing"""
        self._indexing = CartesianIndexing(self._pixels, lights_per_row, search_range)

    def use_polar(self, rows: int, cols: int):
        """Use polar indexing"""
        self._indexing = PolarIndexing(self._pixels, rows, cols)

    def use_float_cartesian(self, rows: int, cols: int):
        """Use floating point cartesian indexing"""
        self._indexing = FloatCartesianIndexing(self._pixels, rows, cols)

    def use_float_polar(self, rows: int, cols: int):
        """Use floating point polar indexing"""
        self._indexing = FloatPolarIndexing(self._pixels, rows, cols)

    def __getitem__(self, key: Any) -> Optional[RGB]:
        return self._indexing.get(key)

    def __setitem__(self, key: Any, value: RGB) -> None:
        self._indexing.set(key, value)
