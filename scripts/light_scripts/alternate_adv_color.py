#!/usr/bin/env python3

# NAME: Rainbow Step

import sys
from typing import Optional, Union
from backend.backend_types import RGB
import colour

from backend.ceiling import Ceiling
from backend.util import color_obj_to_rgb
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, interval: Optional[float]):
        interval = interval if interval else 1
        self.step = 2
        self.hue = 0
        self.color = colour.Color(hsl=(self.hue, 1, 0.5))
        super().__init__(interval)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        return super().render(delta, ceil)

    def interval_reached(self, ceil: Ceiling) -> None:
        ceil.clear(False)

        step = self.step + 2
        col = color_obj_to_rgb(self.color)

        if self.step % 2 == 0:
            ceil[::step] = col
            ceil[1::step] = (0, 0, 0)
        else:
            ceil[::step] = (0, 0, 0)
            ceil[1::step] = col

        ceil.show()
        self.step = (self.step + 1) % 8
        self.hue = (self.hue + 0.05) % 1
        self.color.hue = self.hue


def run(**kwargs):
    interval = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_linear()
    ceil.clear()

    render_loop = Render(interval / 3)
    render_loop.run(1, ceil)


if __name__ == "__main__":
    run(ceiling=Ceiling(), interval=sys.argv[1])
