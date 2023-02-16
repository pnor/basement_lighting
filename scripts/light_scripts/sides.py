#!/usr/bin/env python3

# NAME: Sides


import sys
import time
from typing import Optional, Union
import numpy as np
from backend.backend_types import RGB

from backend.ceiling import Ceiling
from backend.util import color_format_to_rgb, sigmoid_0_to_1
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, color: RGB, interval: Optional[float]):
        self.color = color
        assert interval is not None
        super().__init__(interval * 1.5)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        ceil.clear()

        y = (self.progress() * 1.3) - 0.15

        ceil[0.1, y] = self.color
        ceil[0.9, y] = self.color

        ceil.show()
        return super().render(delta, ceil)


def run(**kwargs):
    color_input = color_format_to_rgb(kwargs["color"])
    interval = float(kwargs["interval"])

    color = np.array(color_input)

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_float_cartesian(effect_radius=0.3)
    ceil.clear()

    render_loop = Render(color_input, interval)
    render_loop.run(60, ceil)


if __name__ == "__main__":
    run(ceiling=Ceiling(test_mode=True), color=sys.argv[1], interval=sys.argv[2])
