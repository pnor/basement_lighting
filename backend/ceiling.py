#!/usr/bin/env python3

from microcontroller import Pin
import neopixel
import board
from typing import Callable, Any
from backend.backend_types import RGB

from indexing import Indexing, LinearIndexing

"""
A layer between the neopixel API and our light scripts to abstract away all that coordinate math
"""

# Basement related constants
NUMBER_LIGHTS = 200


class Ceiling:
    def __init__(
        self,
        io_pin: Pin = board.D21,
        number_lights: int = NUMBER_LIGHTS,
        auto_write: bool = True,
    ):
        self._pixels = neopixel.NeoPixel(io_pin, number_lights, auto_write=auto_write)
        self._indexing = LinearIndexing(self._pixels)

    def __getitem__(self, key: Any) -> RGB:
        return self._indexing.get(key)

    def __setitem__(self, key: Any, value: RGB) -> None:
        self._indexing.set(key, value)
