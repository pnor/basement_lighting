#!/usr/bin/env python3

import colorama
from neopixel import NeoPixel
import truecolor

from typing import List

"""
Print the LED pattern to terminal to test how a display will look
"""


class TestDisplay:
    """
    Class that prints the arrangment of LEDs in stdout to debug
    """

    def __init__(self, lights_per_row: List[int], pixels: NeoPixel) -> None:
        self._lights_per_row = lights_per_row
        self._pixels = pixels

    def show(self):
        MAX_COLS = max(self._lights_per_row)
        indx = 0

        full_output = ""
        for i in range(len(self._lights_per_row)):
            line = ""

            for j in range(self._lights_per_row[i]):
                color = self._pixels[indx]

                if i % 2 == 0:  # horizontal -
                    line += truecolor.fore_text("x", color)
                else:  # diagonal \
                    line += truecolor.fore_text("\\", color)

                indx += 1

            full_output = line + "\n" + full_output

        print(full_output)
