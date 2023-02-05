#!/usr/bin/env python3

# NAME: Sine Colorful

import sys
import copy
import colour
from typing import Optional, Union
import numpy as np
from backend.backend_types import RGB

from backend.ceiling import Ceiling
from backend.util import (
    color_format_to_obj,
    color_range,
    dim_color,
)
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, color: colour.Color, interval: Optional[float]):
        assert interval is not None

        color1 = copy.deepcopy(color)

        color2 = copy.deepcopy(color)
        color2.hue = (color2.hue + 0.1) % 1

        color3 = copy.deepcopy(color)
        color3.hue = (color3.hue + 0.3) % 1

        color4 = dim_color(color)

        self.colors = color_range(color1, color2, 10)
        self.colors += color_range(color2, color3, 10)
        self.colors += color_range(color3, color4, 10)
        self.colors += color_range(color4, color1, 10)

        self.color_progress = 0.0

        self.COLOR_RANGE = 0.2  # percentage of self.colors to use at once
        self.NUM_POINTS = 30
        super().__init__(interval * 4)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        ceil.clear(False)

        self.color_progress = (self.color_progress + (delta / 15)) % 1

        base_color_index = int(len(self.colors) * self.color_progress)

        for x in range(0, self.NUM_POINTS):
            x_index = x / self.NUM_POINTS
            y_index = np.sin((2 * np.pi) * (self.progress() + (x / self.NUM_POINTS)))
            y_index = (y_index / 2) + 0.5

            color_index = (
                base_color_index
                + int((x / self.NUM_POINTS) * (self.COLOR_RANGE * len(self.colors)))
            ) % len(self.colors)
            ceil[x_index, y_index] = self.colors[color_index]

        ceil.show()

        return super().render(delta, ceil)


def run(**kwargs):
    color_input = color_format_to_obj(kwargs["color"])
    interval = float(kwargs["interval"])
    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_float_cartesian()

    render_loop = Render(color_input, interval)
    render_loop.run(60, ceil)


if __name__ == "__main__":
    run(ceiling=Ceiling(test_mode=True), color=sys.argv[1], interval=sys.argv[2])
