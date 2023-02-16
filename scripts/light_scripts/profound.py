#!/usr/bin/env python3

# NAME: Profound

import sys
import numpy as np
from typing import Optional, Union
from backend.backend_types import RGB

from backend.ceiling import Ceiling
from backend.state import State
from backend.util import color_range, dim_color, hex_to_rgb
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, interval: Optional[float]):
        # Getting range of colors for all LEDs to cycle through
        self.TAIL_LENGTH = 8
        color = hex_to_rgb("#7c41fc")
        self.colors_primary = color_range(color, dim_color(color), self.TAIL_LENGTH)

        color = hex_to_rgb("#f70459")
        self.colors_secondary = color_range(color, dim_color(color), self.TAIL_LENGTH)

        super().__init__(interval * 5)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        ceil.clear()
        theta = self.progress() * 2 * np.pi

        for i in range(0, self.TAIL_LENGTH):
            ceil[0.6, (theta + (np.pi / 2)) - (i * np.pi / 4)] = self.colors_secondary[
                i
            ]
            ceil[0.3, theta - (i * np.pi / 4)] = self.colors_primary[i]

        ceil.show()
        return super().render(delta, ceil)


def run(**kwargs):
    interval = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_float_polar([0.5, 0.5], effect_radius=0.3)
    ceil.clear()

    render_loop = Render(interval)
    render_loop.run(30, ceil)


if __name__ == "__main__":
    run(ceiling=State().create_ceiling(), color=sys.argv[1], interval=sys.argv[2])
