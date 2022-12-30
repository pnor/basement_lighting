#!/usr/bin/env python3

# NAME: Trick Step

import sys
from typing import Optional, Union
from backend.backend_types import RGB

from backend.ceiling import Ceiling
from backend.util import color_format_to_rgb, hex_to_rgb
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, color: RGB, interval: Optional[float]):
        self.color = color
        interval = interval if interval else 1
        self.step = 2
        super().__init__(interval)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        return super().render(delta, ceil)

    def interval_reached(self, ceil: Ceiling) -> None:
        ceil.clear(False)

        step = self.step + 2
        if self.step % 2 == 0:
            ceil[::step] = self.color
            ceil[1::step] = (0, 0, 0)
        else:
            ceil[::step] = (0, 0, 0)
            ceil[1::step] = self.color

        ceil.show()
        self.step = (self.step + 1) % 8


def run(**kwargs):
    color = color_format_to_rgb(kwargs["color"])
    interval = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_linear()
    ceil.clear()

    render_loop = Render(color, interval / 3)
    render_loop.run(1, ceil)


if __name__ == "__main__":
    run(ceiling=Ceiling(), color=sys.argv[1], interval=sys.argv[2])
