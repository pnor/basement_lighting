#!/usr/bin/env python3

# NAME: Run through 2

import numpy as np
import sys
import time
from typing import Optional, Union
from backend.backend_types import RGB

from backend.ceiling import Ceiling
from backend.state import State
from backend.util import color_format_to_rgb, color_range, dim_color
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, color: RGB, num_lights: int, interval: Optional[float]):
        assert interval is not None
        self.NUMBER_POINTS = 10
        self.TAIL_LENGTH = 10

        self.colors = color_range(color, dim_color(color), self.TAIL_LENGTH)
        self.points = (np.random.random(self.NUMBER_POINTS) * num_lights).astype(
            np.int32
        )
        super().__init__(interval * 7)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        ceil.clear()

        for p in self.points:
            index = (
                int(self.progress() * ceil.number_lights()) + p
            ) % ceil.number_lights()

            for i in range(0, self.TAIL_LENGTH):
                ceil[index - i] = self.colors[i]

        ceil.show()

        return super().render(delta, ceil)


def run(**kwargs):
    color_input = color_format_to_rgb(kwargs["color"])
    interval = float(kwargs["interval"])

    ceil = kwargs["ceiling"]
    ceil.use_linear()
    ceil.clear()

    render_loop = Render(color_input, ceil.number_lights(), interval)
    render_loop.run(30, ceil)


if __name__ == "__main__":
    run(ceiling=State().create_ceiling(), color=sys.argv[1], interval=sys.argv[2])
