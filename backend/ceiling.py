#!/usr/bin/env python3

from typing import Callable, Any, Optional
from backend.neopixel_wrapper import PixelWrapper

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
    def __init__(self, **kwargs):
        """
        If using actual light strip:
        `io_pin`: which GPIO pin neopixels should be initialized for
        `number_lights`: number lights controlled
        `auto_write`: whether every write to the neopixels LED array should update the lights. *False*
        by default(!!!)

        If using testing: (only provide 1 arg)
        `number_lights`: number lights in the light strip
        """
        if len(kwargs) == 1 and kwargs["number_lights"] is not None:
            self._pixels = PixelWrapper.init_for_testing(kwargs["number_lights"])
        else:
            io_pin: Pin = kwargs["io_pin"] if kwargs["io_pin"] else board.D21
            number_lights: int = (
                kwargs["number_lights"] if kwargs["number_lights"] else NUMBER_LIGHTS
            )
            auto_write: bool = kwargs["auto_write"] if kwargs["auto_write"] else False
            self._pixels = PixelWrapper(io_pin, number_lights, auto_write=auto_write)

        self._indexing = LinearIndexing(self._pixels)
        self.NUMBER_LIGHTS = NUMBER_LIGHTS

    def clear(self, show=True) -> None:
        """Set every pixel to black (and updates the LEDs)"""
        self.fill([0, 0, 0])
        if show:
            self.show()

    def fill(self, clear_color: RGB) -> None:
        """Set every pixel to the given color"""
        self._pixels.fill(clear_color)

    def show(self) -> None:
        """Update all pixels with updated colors at once"""
        self._pixels.show()

    def rows(self) -> Optional[List[int]]:
        """Returns rows information if the indexing is row indexing"""
        if isinstance(self._indexing, RowIndexing):
            return self._indexing.rows
        else:
            return None

    def testing_mode(
        self, lights_per_row: Optional[List[int]] = None, print_to_stdout=True
    ):
        """Note: to get std output, must explicitly call ceiling.show()"""
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

    def use_polar(
        self,
        origin: Tuple[float, float],
        lights_per_row: List[int] = CEILING_ROW_ARRANGEMENT,
    ):
        assert len(origin) == 2
        """Use polar indexing"""
        self._indexing = PolarIndexing(
            self._pixels,
            lights_per_row=lights_per_row,
            origin=origin,
        )

    def use_float_cartesian(
        self,
        lights_per_row: List[int] = CEILING_ROW_ARRANGEMENT,
        effect_radius: float = 0.2,
    ):
        """Use floating point cartesian indexing"""
        self._indexing = FloatCartesianIndexing(
            self._pixels, lights_per_row, effect_radius=effect_radius
        )

    def use_float_polar(
        self,
        origin: Tuple[float, float],
        lights_per_row: List[int] = CEILING_ROW_ARRANGEMENT,
        effect_radius: float = 0.2,
    ):
        """Use floating point polar indexing"""
        self._indexing = FloatPolarIndexing(
            self._pixels, lights_per_row, origin, effect_radius=effect_radius
        )

    def __getitem__(self, key: Any) -> Optional[RGB]:
        return self._indexing.get(key)

    def __setitem__(self, key: Any, value: RGB) -> None:
        self._indexing.set(key, value)
