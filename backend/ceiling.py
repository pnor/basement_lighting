#!/usr/bin/env python3

from typing import Callable, Any, Optional
from backend.neopixel_wrapper import (
    PixelWrapper,
    init_for_testing,
    init_with_real_board,
)

from backend.test_display import TestDisplay

from .backend_types import RGB

from .indexing import *

"""
A layer between the neopixel API and our light scripts to abstract away all that coordinate math
"""

# Basement related constants
NUMBER_LIGHTS = 200
CEILING_ROW_ARRANGEMENT = [29, 29, 32, 29, 32, 28, 20]


class Ceiling:
    def __init__(self, **kwargs):
        """
        If using actual light strip:
        `io_pin`: which GPIO pin neopixels should be initialized for
        `number_lights`: number lights controlled
        `auto_write`: whether every write to the neopixels LED array should update the lights. *False*
        by default(!!!)

        If using testing: (only provide 2 args)
        `test_mode`: to true
        `number_lights`: number lights in the light strip
        `print_to_stdout`: whether to print to stdout. Default true
        """
        if kwargs.get("test_mode"):
            num_lights = (
                kwargs.get("number_lights")
                if kwargs.get("number_lights")
                else NUMBER_LIGHTS
            )
            print_to_stdout = (
                kwargs.get("print_to_stdout")
                if kwargs.get("print_to_stdout") is not None
                else True
            )
            self._pixels = init_for_testing(
                number_leds=num_lights, print_to_stdout=print_to_stdout
            )
            self.testing_mode_rows()
        else:
            io_pin = kwargs.get("io_pin")
            number_lights: int = (
                kwargs.get("number_lights")
                if kwargs.get("number_lights")
                else NUMBER_LIGHTS
            )
            auto_write: bool = (
                kwargs.get("auto_write") if kwargs.get("auto_write") else False
            )
            self._pixels = init_with_real_board(
                io_pin, number_lights, auto_write=auto_write
            )

        self._indexing = LinearIndexing(self._pixels)
        self.NUMBER_LIGHTS = NUMBER_LIGHTS
        self._cached_led_spacing: Optional[LEDSpace] = None

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

    def testing_mode_rows(
        self, lights_per_row: List[int] = CEILING_ROW_ARRANGEMENT, print_to_stdout=True
    ):
        self._pixels.set_lights_per_row(lights_per_row)

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
        self._indexing = CartesianIndexing(
            self._pixels,
            lights_per_row,
            search_range,
            cached_led_spacing=self._cached_led_spacing,
        )
        self._cached_led_spacing = self._indexing._led_spacing

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
            cached_led_spacing=self._cached_led_spacing,
        )
        self._cached_led_spacing = self._indexing._led_spacing

    def use_float_cartesian(
        self,
        lights_per_row: List[int] = CEILING_ROW_ARRANGEMENT,
        effect_radius: float = 0.2,
    ):
        """Use floating point cartesian indexing"""
        self._indexing = FloatCartesianIndexing(
            self._pixels,
            lights_per_row,
            effect_radius=effect_radius,
            cached_led_spacing=self._cached_led_spacing,
        )
        self._cached_led_spacing = self._indexing._led_spacing

    def use_float_polar(
        self,
        origin: Tuple[float, float],
        lights_per_row: List[int] = CEILING_ROW_ARRANGEMENT,
        effect_radius: float = 0.2,
    ):
        """Use floating point polar indexing"""
        self._indexing = FloatPolarIndexing(
            self._pixels,
            lights_per_row,
            origin,
            effect_radius=effect_radius,
            cached_led_spacing=self._cached_led_spacing,
        )
        self._cached_led_spacing = self._indexing._led_spacing

    def __getitem__(self, key: Any) -> Optional[RGB]:
        return self._indexing.get(key)

    def __setitem__(self, key: Any, value: RGB) -> None:
        self._indexing.set(key, value)
