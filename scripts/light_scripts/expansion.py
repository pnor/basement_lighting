#!/usr/bin/env python3
# NAME: Expansion

import sys
import copy
from typing import Optional, Union
import numpy as np
import colour

from backend.ceiling import Ceiling
from backend.util import color_format_to_obj, color_range
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, color: colour.Color, interval: Optional[float]):
        self.color = color
        self.secondary_color = copy.deepcopy(color)
        self.secondary_color.hue = (self.secondary_color.hue + 0.2) % 1
        self.color_range = color_range(self.color, self.secondary_color, 20)

        assert interval is not None
        self.ROWS = 4
        self.COLS = 4
        self.SIZE_RANGE = [0.04, 0.3]
        self.progresses = np.arange(0, 1, 1 / (self.ROWS * self.COLS))
        np.random.shuffle(self.progresses)

        NUM_POINTS = 50
        NUM_PAD_POINTS = 150
        self.progress_curve = np.arange(0, 1, 1 / (NUM_POINTS / 2))
        self.progress_curve = self.progress_curve**2
        self.progress_curve = list(np.zeros(NUM_PAD_POINTS // 2)) + list(self.progress_curve) + list(reversed(self.progress_curve)) + list(np.zeros(NUM_PAD_POINTS // 2))

        super().__init__(interval * 6)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        ceil.clear(False)

        def _draw(ceil, x, y, color):
            ceil[x, y] = color

        x_spacing = (1 / self.ROWS) / 2
        y_spacing = (1 / self.COLS) / 2
        for i in range(self.ROWS):
            x = i / self.ROWS
            for j in range(self.COLS):
                y = j / self.COLS
                prog = (self.progresses[(i * self.ROWS) + j] + self.progress()) % 1
                prog = self.progress_curve[int(len(self.progress_curve) * prog)]
                rad = (self.SIZE_RANGE[0] * (1 - prog)) + (self.SIZE_RANGE[1] * prog)
                color = self.color_range[int(prog * len(self.color_range))]
                ceil.with_float_cartesian(lambda c: _draw(c, x_spacing + x, y_spacing + y,
                                                          color), effect_radius=rad)
        ceil.show()
        return super().render(delta, ceil)


def run(**kwargs):
    color_input = color_format_to_obj(kwargs["color"])
    interval = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_float_cartesian(effect_radius=0.2)
    ceil.clear()

    render_loop = Render(color_input, interval)
    render_loop.run(60, ceil)


if __name__ == "__main__":
    run(ceiling=Ceiling(test_mode=True, print_to_stdout=True), color=sys.argv[1], interval=sys.argv[2])
