#!/usr/bin/env python3

# NAME: Meters

import numpy as np
import sys
import copy
import colour
from typing import List, Optional, Union

from backend.ceiling import Ceiling
from backend.util import (
    clamp,
    color_format_to_obj,
    color_range,
    dim_color,
)
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(
        self, color_obj: colour.Color, row_info: List[int], interval: Optional[float]
    ):
        assert interval is not None

        self.ROW_INFO = row_info

        # color spectrum
        self.color_obj = color_obj

        self.color_1 = copy.deepcopy(color_obj)
        self.color_2 = copy.deepcopy(color_obj)
        self.color_2.hue = clamp(self.color_2.hue + 0.2, 0, 1)
        self.color_3 = copy.deepcopy(color_obj)
        self.color_3.hue = clamp(self.color_3.hue + 0.3, 0, 1)

        self.color_range = color_range(self.color_1, self.color_2, 20)
        self.color_range = self.color_range + color_range(
            self.color_2, self.color_3, 10
        )

        # Percentage progresses in (0..1). Multiplied with len of color range and number of LEDs in
        # a row to determine how much of the row to illuminate
        low_mound = np.arange(0, np.pi, np.pi / 10)
        low_mound = np.sin(low_mound)
        low_mound /= 4
        mid_mound = np.arange(0, np.pi, np.pi / 10)
        mid_mound = np.sin(mid_mound)
        mid_mound /= 1.5
        high_mound = np.arange(0, np.pi, np.pi / 10)
        high_mound = np.sin(high_mound)
        self.progress_indeces = np.concatenate(
            (
                low_mound,
                low_mound,
                low_mound,
                low_mound,
                mid_mound,
                low_mound,
                low_mound,
                high_mound,
            )
        )

        # offset to make each row not be on the same period
        self.row_progress_percentage_offset = np.random.random(len(row_info))
        # self.row_progress_percentage_offset = np.zeros(len(row_info))

        super().__init__(interval * 6)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        ceil.clear(False)

        prog = self.progress()

        for i in range(len(self.row_progress_percentage_offset)):
            # row_prog = (prog + self.row_progress_percentage_offset[i]) % 1
            # row_prog = clamp(prog + self.row_progress_percentage_offset[i], 0, 0.999)
            row_prog_index = (
                (prog * len(self.progress_indeces))
                + (self.row_progress_percentage_offset[i] * len(self.progress_indeces))
            ) % len(self.progress_indeces)
            row_prog = self.progress_indeces[int(row_prog_index)]

            row_highest_index = int(row_prog * self.ROW_INFO[i])

            for index in range(row_highest_index):
                color = self.color_range[
                    int((index / self.ROW_INFO[i]) * len(self.color_range))
                ]

                if i % 2 == 0:
                    ceil[i, index] = color
                else:
                    ceil[i, (self.ROW_INFO[i] - index)] = color

        ceil.show()

        return super().render(delta, ceil)

    def interval_reached(self, ceil: Ceiling) -> None:
        return super().interval_reached(ceil)


def run(**kwargs):
    color_input = color_format_to_obj(kwargs["color"])
    interval = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_row()
    ceil.clear()

    row_info = ceil.rows()
    assert row_info is not None
    render_loop = Render(color_input, row_info, interval)
    render_loop.run(30, ceil)


if __name__ == "__main__":
    run(
        ceiling=Ceiling(),
        color=sys.argv[1],
        interval=sys.argv[2],
    )
