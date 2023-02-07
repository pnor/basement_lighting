#!/usr/bin/env python3

# NAME: D N A

import sys
import copy
import colour
from typing import Optional, Union
import numpy as np
from backend.backend_types import RGB

from backend.ceiling import Ceiling
from backend.util import (
    color_format_to_obj,
    color_format_to_rgb,
    color_range,
    dim_color,
)
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, color: colour.Color, interval: Optional[float]):
        assert interval is not None

        color1 = copy.deepcopy(color)
        self.color1 = color_format_to_rgb(color1)

        color2 = copy.deepcopy(color)
        color2.hue = (color2.hue + 0.2) % 1
        self.color2 = color_format_to_rgb(color2)

        self.NUM_POINTS = 50
        super().__init__(interval * 3)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        ceil.clear(False)

        for x in range(0, self.NUM_POINTS):
            x_index = x / self.NUM_POINTS

            y_index1 = np.sin((2 * np.pi) * (self.progress() + (x / self.NUM_POINTS)))
            y_index1 = (y_index1 / 2) + 0.5

            y_index2 = np.sin(
                (2 * np.pi) * (self.progress() + (x / self.NUM_POINTS)) + (np.pi)
            )
            y_index2 = (y_index2 / 2) + 0.5

            ceil[x_index, y_index1] = self.color1
            ceil[x_index, y_index2] = self.color2

        ceil.show()

        return super().render(delta, ceil)


def run(**kwargs):
    color_input = color_format_to_obj(kwargs["color"])
    interval = float(kwargs["interval"])
    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_float_cartesian(effect_radius=0.07)

    render_loop = Render(color_input, interval)
    render_loop.run(60, ceil)


if __name__ == "__main__":
    run(ceiling=Ceiling(test_mode=True), color=sys.argv[1], interval=sys.argv[2])
