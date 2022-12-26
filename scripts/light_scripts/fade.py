#!/usr/bin/env python3


# NAME: Fade
# Fades every LED on and off

import sys
import time
from typing import Optional, Union
from backend.backend_types import RGB

from backend.ceiling import Ceiling
from backend.util import (
    clamp,
    dim_color,
    hex_to_rgb,
    color_range,
    sigmoid_0_to_1,
)
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, color: RGB, interval: Optional[float]):
        self.cycle_colors = color_range(color, dim_color(color), 100)
        self.forward = True
        super().__init__(interval)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        prog = sigmoid_0_to_1(self.progress())
        if not self.forward:
            prog = 1 - prog
        i = int(prog * 99)

        ceil.fill(self.cycle_colors[i])
        ceil.show()

        return super().render(delta, ceil)

    def interval_reached(self, ceil: Ceiling) -> None:
        self.forward = not self.forward
        return super().interval_reached(ceil)


def run(**kwargs):
    color_input = hex_to_rgb(kwargs["color"])
    interval = float(kwargs["interval"])

    ceil = kwargs["ceiling"]
    ceil.clear()

    render_loop = Render(color_input, interval)
    render_loop.run(30, ceil)


if __name__ == "__main__":
    run(
        ceiling=Ceiling(),
        color=sys.argv[1],
        interval=sys.argv[2],
    )
