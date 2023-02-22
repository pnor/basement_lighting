#!/usr/bin/env python3

# NAME: Convergence


import sys
import time
from typing import Optional, Union
import numpy as np
from backend.backend_types import RGB

from backend.ceiling import Ceiling
from backend.state import State
from backend.util import color_format_to_rgb, sigmoid_0_to_1
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, color: RGB, interval: Optional[float]):
        self.color = color
        assert interval is not None
        xs = np.arange(0, 1, 0.05)
        xs = xs**1.5
        xs /= 2
        self.xs = list(xs) + list(reversed(xs))
        super().__init__(interval * 1.5)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        ceil.clear()

        xs_val = self.xs[int(len(self.xs) * self.progress())]
        x = xs_val
        x_reverse = 1 - xs_val

        for i in np.arange(0, 1, 0.1):
            ceil[x, i] = self.color
            ceil[x_reverse, i] = self.color

        ceil.show()
        return super().render(delta, ceil)


def run(**kwargs):
    color_input = color_format_to_rgb(kwargs["color"])
    interval = float(kwargs["interval"])

    color = np.array(color_input)

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_float_cartesian(effect_radius=0.2)
    ceil.clear()

    render_loop = Render(color_input, interval)
    render_loop.run(60, ceil)


if __name__ == "__main__":
    run(ceiling=State().create_ceiling(), color=sys.argv[1], interval=sys.argv[2])
