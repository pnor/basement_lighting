#!/usr/bin/env python3

# NAME: Pulsing

import sys
import copy
import colour
from typing import Optional, Union
from backend.backend_types import RGB
import numpy as np

from backend.ceiling import Ceiling
from backend.util import (
    color_format_to_rgb,
    color_obj_to_rgb,
    color_range,
    dim_color,
    sigmoid,
    sigmoid_0_to_1,
)
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, color: RGB, interval: Optional[float]):
        self.color = color
        interval = interval if interval else 1
        self.MAX_RADIUS = 0.7
        super().__init__(interval)

    def place_radius(self, ceil: Ceiling) -> None:
        ceil[0.5, 0.5] = self.color

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        prog = self.progress()
        if prog > 0.5:
            prog = (1 - prog) * 2
        else:
            prog *= 2
        prog = sigmoid_0_to_1(prog)

        ceil.clear(False)
        ceil.with_float_cartesian(
            lambda c: self.place_radius(c), effect_radius=(prog * self.MAX_RADIUS)
        )
        ceil.show()

        return super().render(delta, ceil)


def run(**kwargs):
    color_input = color_format_to_rgb(kwargs["color"])
    interval = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_float_cartesian(effect_radius=0.2)
    ceil.clear()

    render_loop = Render(color_input, interval)
    render_loop.run(15, ceil)


if __name__ == "__main__":
    run(
        ceiling=Ceiling(test_mode=True),
        color=sys.argv[1],
        interval=sys.argv[2],
    )
