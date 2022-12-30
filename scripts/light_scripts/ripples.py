#!/usr/bin/env python3

# NAME: Ripples

import sys
import copy
import colour
from typing import List, Optional, Tuple, Union
from backend.backend_types import RGB
import numpy as np

from backend.ceiling import Ceiling
from backend.util import (
    color_format_to_obj,
    color_format_to_rgb,
    color_obj_to_rgb,
    color_range,
    dim_color,
)
from scripts.library.render import RenderState
from backend.ceiling_animation import circle_clear, fade_out, circle_out


class Render(RenderState):
    def __init__(self, color: colour.Color, interval: Optional[float]):
        self.color = color
        interval = interval if interval else 1
        super().__init__(interval)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        return super().render(delta, ceil)

    def interval_reached(self, ceil: Ceiling) -> None:
        assert self.interval is not None

        x = np.random.random()
        y = np.random.random()

        col = color_obj_to_rgb(self.color)
        circle_out(ceil, 10 * self.interval, col, (x, y), 1.3)

        return super().interval_reached(ceil)


def run(**kwargs):
    color_input = color_format_to_obj(kwargs["color"])
    interval = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_float_cartesian(effect_radius=0.2)
    ceil.clear()

    render_loop = Render(color_input, interval / 8)
    render_loop.run(1, ceil)


if __name__ == "__main__":
    run(
        ceiling=Ceiling(),
        color=sys.argv[1],
        interval=sys.argv[2],
    )
