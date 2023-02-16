#!/usr/bin/env python3

# NAME: Binary Sparkle

import sys
import time
from typing import Optional, Union
import numpy as np
from backend.backend_types import RGB

from backend.ceiling import Ceiling
from backend.util import dim_color, color_format_to_rgb
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, color: RGB, number_lights: int, interval: Optional[float]):
        interval = interval if interval else 1
        self.progresses_base = np.random.random(number_lights)
        self.THRESHOLD = 0.9
        self.on_color = color
        self.off_color = dim_color(color)
        super().__init__(interval * 7)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        for i in range(len(self.progresses_base)):
            prog = (self.progresses_base[i] + self.progress()) % 1
            if prog > self.THRESHOLD:
                ceil[i] = self.on_color
            else:
                ceil[i] = self.off_color
        ceil.show()


def run(**kwargs):
    color_input = color_format_to_rgb(kwargs["color"])
    interval = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_linear()
    ceil.clear()

    render_loop = Render(color_input, ceil.number_lights(), interval)
    render_loop.run(15, ceil)


if __name__ == "__main__":
    run(
        ceiling=Ceiling(test_mode=True),
        color=sys.argv[1],
        interval=sys.argv[2],
    )
