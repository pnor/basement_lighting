#!/usr/bin/env python3

# NAME: Beta Noise
#
# Animated gray noise, using the float cartesian's effect radius
# (based off gray_noise in light_scripts)


import sys
import time
from typing import Optional, Union
import numpy as np
import colour
from backend.backend_types import RGB

from backend.ceiling import Ceiling
from backend.util import clamp, colour_rgb_to_neopixel_rgb, hex_to_rgb
from scripts.library.render import RenderState


def rand_func(size: int):
    return np.random.beta(a=2, b=5, size=(size, size))


class Render(RenderState):
    def __init__(self, color: RGB, interval: Optional[float]):
        # Number of points used to generate colors (size by size)
        self.RANDOM_SIZE = 20
        self.color = color

        self.points = rand_func(self.RANDOM_SIZE)
        self.next_points = rand_func(self.RANDOM_SIZE)

        super().__init__(interval)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        prog = self.progress()

        ceil.clear()
        for i in range(self.RANDOM_SIZE):
            for j in range(self.RANDOM_SIZE):
                before_col = (self.color * self.points[i, j]).astype(int)
                next_col = (self.color * self.next_points[i, j]).astype(int)
                interpolated_col = (
                    ((1 - prog) * before_col) + (prog * next_col)
                ).astype(int)

                # to better center the effect
                bump = (1 / self.RANDOM_SIZE) / 2
                ceil[
                    bump + (i / self.RANDOM_SIZE), bump + (j / self.RANDOM_SIZE)
                ] = tuple(interpolated_col)

        ceil.show()
        return super().render(delta, ceil)

    def interval_reached(self, ceil: Ceiling) -> None:
        self.points = self.next_points
        self.next_points = rand_func(self.RANDOM_SIZE)
        return super().interval_reached(ceil)


def run(**kwargs):
    color_input = kwargs["color"]
    interval = float(kwargs["interval"])

    # Brightest color this will yield
    color = np.array(hex_to_rgb(color_input))

    ceil = kwargs["ceiling"]
    ceil.use_float_cartesian(effect_radius=0.1)
    ceil.clear()

    render_loop = Render(color, interval)
    render_loop.run(20, ceil)


if __name__ == "__main__":
    run(
        ceiling=Ceiling(),
        color=sys.argv[1],
        interval=sys.argv[2],
    )
