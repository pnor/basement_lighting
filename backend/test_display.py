#!/usr/bin/env python3

import colorama
import truecolor

from blessings import Terminal

from typing import List

"""
Print the LED pattern to terminal to test how a display will look
"""


class TestDisplay:
    """
    Class that prints the arrangment of LEDs in stdout to debug
    """

    def __init__(self, lights_per_row: List[int], pixels) -> None:
        self._lights_per_row = lights_per_row
        self._pixels = pixels
        self._terminal = Terminal()
        # Make space for the terminal display
        print(self._terminal.move_down * (len(lights_per_row)))

    def show(self):
        MAX_COLS = max(self._lights_per_row)
        indx = 0

        full_output = ""
        for i in range(len(self._lights_per_row)):
            line = ""

            for j in range(self._lights_per_row[i]):
                color = self._pixels[indx]

                if i % 2 == 0:  # horizontal -
                    line += truecolor.color_text("x", color, (0, 0, 0))
                else:  # diagonal \
                    line = truecolor.color_text("-", color, (0, 0, 0)) + line

                indx += 1

            full_output = line + "\n" + full_output

        print((self._terminal.move_up * (len(self._lights_per_row) + 1)), end="")
        print(full_output)
