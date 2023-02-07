#!/usr/bin/env python3

# NAME: Run through
# Runs a single LED throughout the light strip

import sys
import time
from typing import Optional, Union
from backend.backend_types import RGB

from backend.ceiling import Ceiling
from backend.util import color_format_to_rgb, color_range, dim_color
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, color: RGB, interval: Optional[float]):
        self.TAIL_LENGTH = 7
        self.colors = color_range(color, dim_color(color), self.TAIL_LENGTH)
        super().__init__(interval * 5)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        index = int(self.progress() * ceil.NUMBER_LIGHTS)

        ceil.clear(False)
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

    render_loop = Render(color_input, interval)
    render_loop.run(30, ceil)


if __name__ == "__main__":
    run(ceiling=Ceiling(), color=sys.argv[1], interval=sys.argv[2])
