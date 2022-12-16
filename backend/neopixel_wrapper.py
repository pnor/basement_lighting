#!/usr/bin/env python3

import board
import neopixel

from microcontroller import Pin
from typing import Optional, List

from backend.test_display import TestDisplay

"""
Wrapper around the neopixel api to allow for testing without the rasberry pi
"""


class PixelWrapper:
    def __init__(self, *args) -> None:
        """
        If using real neopixel strip:
        `io_pin`: which GPIO pin neopixels should be initialized for
        `number_lights`: number lights controlled
        `auto_write`: whether every write to the neopixels LED array should update the lights. *False*

        If using testing mode:
        `number_lights`:
        """
        self.print_to_stdout = True
        if len(args) == 3:
            self.init_with_real_board(*args)
        else:
            self.init_for_testing(*args)

    def init_with_real_board(
        self, io_pin: Pin, number_lights: int, auto_write: bool
    ) -> None:
        self._auto_write = auto_write
        self._pixels = neopixel.NeoPixel(
            io_pin, number_lights, auto_write=auto_write, pixel_order=neopixel.RGB
        )

    def init_for_testing(self, number_leds: int) -> None:
        self._pretend_pixels = [(0, 0, 0)] * number_leds

    def set_lights_per_row(self, lights_per_row: List[int]) -> None:
        self._lights_per_row = lights_per_row
        self._test_display = TestDisplay(lights_per_row, self)

    def __getitem__(self, key: Any) -> Optional[RGB]:
        if self._pixels:
            return self._pixels.__getitem__(key)
        else:
            return self._pretend_pixels[key]

    def __setitem__(self, key: Any, value: RGB) -> None:
        if self._pixels:
            self._pixels.__setitem__(key, value)
        else:
            self._pretend_pixels[key] = value

        if self._test_display and self._auto_write:
            self._test_display.show()

    def show(self):
        if self._test_display and self.print_to_stdout:
            self._test_display.show()
