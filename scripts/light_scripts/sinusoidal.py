#!/usr/bin/env python3

# NAME: Sinusoidal

import sys
import time
from typing import Optional, Union
import numpy as np
from backend.backend_types import RGB

from backend.ceiling import Ceiling
from backend.util import color_format_to_rgb
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, color: RGB, interval: Optional[float]):
        assert interval is not None
        self.color = color
        self.NUM_POINTS = 15
        super().__init__(interval * 3)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        ceil.clear()

        for x in range(0, self.NUM_POINTS):
            x_index = x / self.NUM_POINTS
            y_index = np.sin((2 * np.pi) * (self.progress() + (x / self.NUM_POINTS)))
            y_index = (y_index / 2) + 0.5
            ceil[x_index, y_index] = self.color

        ceil.show()

        return super().render(delta, ceil)


def run(**kwargs):
    color_input = color_format_to_rgb(kwargs["color"])
    interval = float(kwargs["interval"])
    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_cartesian()

    render_loop = Render(color_input, interval)
    render_loop.run(60, ceil)


if __name__ == "__main__":
    run(ceiling=Ceiling(test_mode=True), color=sys.argv[1], interval=sys.argv[2])
