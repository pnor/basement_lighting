#!/usr/bin/env python3

# NAME: Spinnning
# Do a circular running motion

import sys
import time
from typing import Optional, Union
from backend.backend_types import RGB

from backend.ceiling import Ceiling
from backend.util import color_range, dim_color
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, color: RGB, interval: Optional[float]):
        # Getting range of colors for all LEDs to cycle through
        self.TAIL_LENGTH = 8
        self.colors = color_range(color, dim_color(color), self.TAIL_LENGTH)

        super().__init__(interval)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        ceil.clear(False)
        theta = self.progress() * 360

        for i in range(0, self.TAIL_LENGTH):
            ceil[0.6, theta - (i * 20)] = self.colors[i]

        ceil.show()
        return super().render(delta, ceil)


def run(**kwargs):
    color_input = kwargs["color"]
    interval = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_polar((0.5, 0.5))
    ceil.clear()

    render_loop = Render(color_input, interval)
    render_loop.run(30, ceil)


if __name__ == "__main__":
    run(ceiling=Ceiling(), color=sys.argv[1], interval=sys.argv[2])
