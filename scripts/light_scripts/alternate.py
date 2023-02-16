#!/usr/bin/env python3

# NAME: Alternate
# Blinks every other LED to the same color

import sys
from typing import Optional, Union
from backend.backend_types import RGB

from backend.ceiling import Ceiling
from backend.util import color_format_to_rgb
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, color: RGB, interval: Optional[float]):
        self.color = color
        interval = interval if interval else 1
        self.first_lit = True
        super().__init__(interval)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        return super().render(delta, ceil)

    def interval_reached(self, ceil: Ceiling) -> None:
        ceil.clear()

        ceil[::2] = self.color if self.first_lit else (0, 0, 0)
        ceil[1::2] = (0, 0, 0) if self.first_lit else self.color

        ceil.show()
        self.first_lit = not self.first_lit


def run(**kwargs):
    color_input = color_format_to_rgb(kwargs["color"])
    interval = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_linear()
    ceil.clear()

    render_loop = Render(color_input, interval / 3)
    render_loop.run(1, ceil)


if __name__ == "__main__":
    run(ceiling=Ceiling(test_mode=True), color=sys.argv[1], interval=sys.argv[2])
