#!/usr/bin/env python3

from typing import Optional, Union
from backend.backend_types import RGB
from backend.indexing import Indexing
from backend.neopixel_wrapper import PixelWrapper


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
