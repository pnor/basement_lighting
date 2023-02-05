#!/usr/bin/env python3

# NAME: Box Wipe

import sys
import colour
import copy
import numpy as np
from typing import Optional, Union
from backend.backend_types import RGB

from backend.ceiling import Ceiling
from backend.util import color_range, dim_color, color_format_to_obj
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, color: colour.Color, interval: Optional[float]):
        assert interval is not None

        color1 = copy.deepcopy(color)

        color2 = copy.deepcopy(color)
        color2.hue = (color2.hue + 0.2) % 1

        color3 = copy.deepcopy(color)
        color3.hue = (color3.hue + 0.3) % 1

        color4 = copy.deepcopy(color)
        color4.hue = (color4.hue + 0.5) % 1

        self.colors = color_range(color1, color2, 10)
        self.colors += color_range(color2, color3, 10)
        self.colors += color_range(color3, color4, 10)
        self.colors += color_range(color4, color1, 10)

        self.RADIUS = 0.35
        self.BOX_SIDE = 0.2
        self.color_progress = 0

        super().__init__(interval * 5)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        self.color_progress = ((delta / 6) + self.color_progress) % 1

        theta = self.progress() * (2 * np.pi)

        center_x = np.cos(theta) * self.RADIUS + 0.5
        center_y = np.sin(theta) * self.RADIUS + 0.5

        lower_x = center_x - (self.BOX_SIDE / 2)
        lower_y = center_y - (self.BOX_SIDE / 2)
        upper_x = center_x + (self.BOX_SIDE / 2)
        upper_y = center_y + (self.BOX_SIDE / 2)

        ceil[(lower_x, lower_y):(upper_x, upper_y)] = self.colors[
            int(len(self.colors) * self.color_progress)
        ]

        ceil.show()
        return super().render(delta, ceil)


def run(**kwargs):
    color_input = color_format_to_obj(kwargs["color"])
    interval = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_cartesian()
    ceil.clear()

    render_loop = Render(color_input, interval)
    render_loop.run(30, ceil)


if __name__ == "__main__":
    run(ceiling=Ceiling(test_mode=True), color=sys.argv[1], interval=sys.argv[2])
