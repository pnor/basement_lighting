#!/usr/bin/env python3

# NAME: Sparkle X

import sys
import time
from typing import Optional, Union
import numpy as np
import colour
import copy

from backend.state import State
from backend.backend_types import RGB
from backend.ceiling import Ceiling
from backend.util import color_format_to_obj, color_range, dim_color
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(
        self, color: colour.Color, number_lights: int, interval: Optional[float]
    ):
        interval = interval if interval else 1
        self.progresses_base = np.random.random(number_lights)

        COLOR_SIZE = 20
        PADDING_SIZE = 80
        color_indeces = np.linspace(0, 0.999, COLOR_SIZE) ** 4
        padding = [0] * PADDING_SIZE
        self.color_indeces = (
            padding + list(color_indeces) + list(reversed(color_indeces))
        )

        # All colors in a range, indexed into using progress indeces
        color1 = copy.deepcopy(color)
        color1.luminance = 0.01
        color2 = copy.deepcopy(color)
        color2.luminance = 0.95
        self.colors = color_range(color1, color2, 20)

        super().__init__(interval * 7)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        for i in range(len(self.progresses_base)):
            prog = (self.progresses_base[i] + self.progress()) % 1
            color_prog = self.color_indeces[int(len(self.color_indeces) * prog)]
            color_index = int(color_prog * len(self.colors))
            color = self.colors[color_index]
            ceil[i] = color
        ceil.show()


def run(**kwargs):
    color_input = color_format_to_obj(kwargs["color"])
    interval = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_linear()
    ceil.clear()

    render_loop = Render(color_input, ceil.number_lights(), interval)
    render_loop.run(30, ceil)


if __name__ == "__main__":
    run(
        ceiling=State().create_ceiling(),
        color=sys.argv[1],
        interval=sys.argv[2],
    )
