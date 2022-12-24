#!/usr/bin/env python3

import colorama
import truecolor

from blessings import Terminal

from typing import List, Optional

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

        # For moving the cursor down to make space for the display
        self._first_draw = True

        # Terminal does not pickle well (inf recursion bug), so we set this to none right before we send it between threads
        # However, when we need it, we initialize it
        self._terminal: Optional[Terminal] = None

    def show_as_linear(self) -> None:
        """
        Prints to terminal a represnetation of the light strip.
        Shows the rows as straight aligned rows.
        """
        index = 0

        full_output = ""
        for i in range(len(self._lights_per_row)):
            line = ""

            for j in range(self._lights_per_row[i]):
                color = self._pixels[index]

                if i % 2 == 0:  # horizontal -
                    line += truecolor.color_text("x", color, (0, 0, 0))
                else:  # diagonal \
                    line = truecolor.color_text("-", color, (0, 0, 0)) + line

                index += 1

            full_output = line + "\n" + full_output

        print((self._terminal.move_up * (len(self._lights_per_row) + 1)), end="")
        print(full_output)

    def show_as_diagonals(self) -> None:
        """
        Prints to terminal a represnetation of the light strip.
        Shows the rows as diagonals arrange like so:
                ----->
        3 ------
         <-----
               ----- 2
                ---->
        1 ------
         <-----
               ----- 0
        """
        index = 0

        output_lines = []
        for i in range(len(self._lights_per_row)):
            line_bot = ""
            line_top = ""

            for j in range(self._lights_per_row[i]):
                color = self._pixels[index]
                if i % 2 == 0:  # backward diagonal
                    if j > self._lights_per_row[i] // 2:
                        line_bot = (
                            truecolor.color_text(" ", (0, 0, 0), (0, 0, 0)) + line_bot
                        )
                        line_top = (
                            truecolor.color_text("x", color, (0, 0, 0)) + line_top
                        )
                    else:
                        line_bot = (
                            truecolor.color_text("x", color, (0, 0, 0)) + line_bot
                        )
                        line_top = (
                            truecolor.color_text(" ", (0, 0, 0), (0, 0, 0)) + line_top
                        )
                else:  # forward diagonal
                    if j > self._lights_per_row[i] // 2:
                        line_bot += truecolor.color_text(" ", (0, 0, 0), (0, 0, 0))
                        line_top += truecolor.color_text("x", color, (0, 0, 0))
                    else:
                        line_bot += truecolor.color_text("x", color, (0, 0, 0))
                        line_top += truecolor.color_text(" ", (0, 0, 0), (0, 0, 0))
                index += 1

            output_lines += [line_bot, line_top]

        output_lines.reverse()
        full_output = "\n".join(output_lines)
        print((self._terminal.move_up * (len(self._lights_per_row) * 2 + 1)), end="")
        print(full_output)

    def show(self) -> None:
        if self._terminal is None:
            self._terminal = Terminal()
            self._first_draw = True  # make space in flask stdout
        if self._first_draw:
            self._first_draw = False
            print(self._terminal.move_down * (len(self._lights_per_row)))

        # self.show_as_linear()
        self.show_as_diagonals()
