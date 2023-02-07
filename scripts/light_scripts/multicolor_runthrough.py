#!/usr/bin/env python3

# NAME: Run thru 2.8 χ BackCover

import numpy as np
import sys
import copy
import colour
from typing import Optional, Union
from backend.backend_types import RGB

from backend.ceiling import Ceiling
from backend.util import color_format_to_obj, color_range, dim_color, mix_colors_fast
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, color: colour.Color, num_lights: int, interval: Optional[float]):
        assert interval is not None
        self.NUMBER_POINTS = 5
        self.TAIL_LENGTH = 10

        color1 = copy.deepcopy(color)
        color1.luminance = 0.95
        color2 = copy.deepcopy(color)
        # color2.hue = (color2.hue + 0.2) % 1
        color2.luminance = 0.01

        color3 = copy.deepcopy(color)
        color3.luminance = 0.95
        color3.hue = (color3.hue - 0.1) % 1
        color4 = copy.deepcopy(color)
        color4.hue = (color4.hue - 0.3) % 1
        color4.luminance = 0.01

        self.colors1 = color_range(color1, color2, 10)
        self.colors2 = color_range(color3, color4, 10)

        self.points1 = (np.random.random(self.NUMBER_POINTS) * num_lights).astype(
            np.int32
        )
        self.points2 = (np.random.random(self.NUMBER_POINTS) * num_lights).astype(
            np.int32
        )
        super().__init__(interval * 8)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        ceil.clear(False)

        for p in self.points1:
            index = (int(self.progress() * ceil.NUMBER_LIGHTS) + p) % ceil.NUMBER_LIGHTS
            for i in range(0, self.TAIL_LENGTH):
                ceil[(index - i) % ceil.NUMBER_LIGHTS] = self.colors1[i]

        for p in self.points2:
            index = (int((1 - self.progress()) * ceil.NUMBER_LIGHTS) + p) % ceil.NUMBER_LIGHTS
            for i in range(0, self.TAIL_LENGTH):
                ceil_index = (index + i) % ceil.NUMBER_LIGHTS
                cur_color = ceil[ceil_index]
                ceil[ceil_index] = mix_colors_fast(self.colors2[i], np.array(cur_color))

        ceil.show()

        return super().render(delta, ceil)


def run(**kwargs):
    color_input = color_format_to_obj(kwargs["color"])
    interval = float(kwargs["interval"])

    ceil = kwargs["ceiling"]
    ceil.use_linear()
    ceil.clear()

    render_loop = Render(color_input, ceil.NUMBER_LIGHTS, interval)
    render_loop.run(30, ceil)


if __name__ == "__main__":
    run(ceiling=Ceiling(test_mode=True), color=sys.argv[1], interval=sys.argv[2])
