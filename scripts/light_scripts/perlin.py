#!/usr/bin/env python3

# NAME: Perlin Noise
# Animated Perlin Noise (of any 1 color)


import sys
import numpy as np
from perlin_noise import PerlinNoise
from typing import Union
from backend.backend_types import RGB
from backend.state import State

from backend.ceiling import Ceiling
from backend.util import color_format_to_rgb, sigmoid_0_to_1
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, color: RGB, interval: float) -> None:
        super().__init__(interval=interval)
        self.cur_perlin_noise = PerlinNoise()
        self.next_perlin_noise = PerlinNoise()

        # Number of points used to sample the perlin noise obj
        self.SAMPLE_SIZE = 20
        # Brightest color this will yield
        self.color = color
        # Minimal brightness of any LED
        self.MIN_BRIGHTNESS = 0.20

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        prog = sigmoid_0_to_1(self.progress())
        ceil.clear()

        for i in range(self.SAMPLE_SIZE):
            for j in range(self.SAMPLE_SIZE):
                i_indx = i / self.SAMPLE_SIZE
                j_indx = j / self.SAMPLE_SIZE

                # Bump up the minimal brightness this can yield
                cur_perlin_sample = self.cur_perlin_noise([i_indx, j_indx])
                cur_perlin_sample = self.MIN_BRIGHTNESS + (
                    cur_perlin_sample * (1 - self.MIN_BRIGHTNESS)
                )
                next_perlin_sample = self.next_perlin_noise([i_indx, j_indx])
                next_perlin_sample = self.MIN_BRIGHTNESS + (
                    next_perlin_sample * (1 - self.MIN_BRIGHTNESS)
                )

                before_col = (self.color * cur_perlin_sample).astype(int)
                next_col = (self.color * next_perlin_sample).astype(int)
                interpolated_col = (
                    ((1 - prog) * before_col) + (prog * next_col)
                ).astype(int)
                interpolated_col = np.clip(interpolated_col, 0, 255)

                # to better center the effect
                bump = (1 / self.SAMPLE_SIZE) / 2

                ceil[
                    bump + (i / self.SAMPLE_SIZE), bump + (j / self.SAMPLE_SIZE)
                ] = np.array(interpolated_col)

        ceil.show()
        return super().render(delta, ceil)

    def interval_reached(self, ceiling: Ceiling) -> None:
        self.cur_perlin_noise = self.next_perlin_noise
        self.next_perlin_noise = PerlinNoise(octaves=np.random.randint(1, 6))
        return super().interval_reached(ceiling)


def run(**kwargs):
    color_input = color_format_to_rgb(kwargs["color"])
    interval = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_float_cartesian(effect_radius=0.1)

    render_loop = Render(color_input, interval)
    render_loop.run(30, ceil)


if __name__ == "__main__":
    run(ceiling=State().create_ceiling(), color=sys.argv[1], interval=sys.argv[2])
