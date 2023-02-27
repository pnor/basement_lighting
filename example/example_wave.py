#!/usr/bin/env python3

# NAME: Waveform I


import sys
import time
from typing import Optional, Union
import numpy as np
import copy
import colour
from backend.backend_types import RGB
from numba import jit

from backend.ceiling import Ceiling
from backend.state import State
from backend.util import (
    color_format_to_obj,
    color_format_to_rgb,
    color_range,
    dim_color,
    sigmoid_0_to_1,
)
from scripts.library.render import RenderState


@jit
def wave_function(x: float, y: float) -> float:
    return np.sin(x) * np.sin(y)


@jit
def convert_range(
    value: float, orig_min: float, orig_max: float, new_min: float, new_max: float
) -> float:
    return (
        ((value - orig_min) * (new_max - new_min)) / (orig_max - orig_min)
    ) + new_min


class Render(RenderState):
    def __init__(self, color: colour.Color, interval: Optional[float]):
        assert interval is not None

        color1 = dim_color(copy.deepcopy(color))

        color2 = copy.deepcopy(color)

        color3 = copy.deepcopy(color)
        color3.hue = (color2.hue + 0.15) % 1
        color3.luminance = 0.9

        self.colors = color_range(color1, color2, 30)
        self.colors += color_range(color2, color3, 10)

        self.NUM_POINTS = 81
        self.side = int(np.sqrt(self.NUM_POINTS))

        # Lowest Highest x and y moved
        self.MIN_XY = np.array([-500, -500])
        self.MAX_XY = np.array([50, 100])

        # Range of function (min and max of points returned)
        self.RANGE = np.array([-1, 1], dtype=np.float64)

        super().__init__(interval * 500)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        ceil.clear()

        x_base = self.progress() * (self.MAX_XY[0] - self.MIN_XY[0]) + self.MIN_XY[0]
        y_base = self.progress() * (self.MAX_XY[1] - self.MIN_XY[1]) + self.MIN_XY[1]

        for i in range(self.side):
            for j in range(self.side):
                x = x_base + (i / 2)
                y = y_base + (j / 2)

                res = convert_range(
                    wave_function(x, y), self.RANGE[0], self.RANGE[1], 0, 1
                )

                ceil[i / self.side, j / self.side] = self.colors[
                    int(res * (len(self.colors)))
                ]

        ceil.show()
        return super().render(delta, ceil)


def run(**kwargs):
    color_input = color_format_to_obj(kwargs["color"])
    interval = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_float_cartesian(effect_radius=0.12)

    render_loop = Render(color_input, interval)
    render_loop.run(60, ceil)


if __name__ == "__main__":
    run(ceiling=State().create_ceiling(), color=sys.argv[1], interval=sys.argv[2])
