#!/usr/bin/env python3

# NAME: Eclipse

import sys
from typing import Optional, Union
import colour
import copy

import numpy as np


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

        color3 = dim_color(color)

        self.colors = color_range(color1, color2, 10)
        self.colors += color_range(color2, color3, 10)
        self.colors += color_range(color3, color1, 10)

        super().__init__(interval * 4)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        color = self.colors[int(self.progress() * len(self.colors))]

        ceil.set_decreasing_intensity([0.5, 0.5], 0.5, color)
        ceil.set_all_in_radius([0.5, 0.5], 0.25, np.array([0, 0, 0]))

        ceil.show()
        return super().render(delta, ceil)


def run(**kwargs):
    ceil = kwargs["ceiling"]
    ceil.clear()

    color_input = color_format_to_obj(kwargs["color"])
    interval = kwargs.get("interval")
    interval = float(interval) if interval else None

    render_loop = Render(color_input, interval)
    render_loop.run(60, ceil)


if __name__ == "__main__":
    run(
        ceiling=Ceiling(test_mode=True),
        interval=sys.argv[1] if len(sys.argv) > 1 else None,
    )
