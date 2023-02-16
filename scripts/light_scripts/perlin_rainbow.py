#!/usr/bin/env python3

# NAME: Perlin Noise Rainbow
# Animated Perlin Noise affecting color hue
# (takes in 1 argument for speed)


import sys
from typing import Union
import numpy as np
from colour import Color
from perlin_noise import PerlinNoise

from backend.ceiling import Ceiling
from backend.util import color_obj_to_rgb, sigmoid_0_to_1

from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, interval: float) -> None:
        super().__init__(interval=interval)
        self.cur_perlin_noise = PerlinNoise()
        self.next_perlin_noise = PerlinNoise()
        # Number of points used to sample the perlin noise obj
        self.SAMPLE_SIZE = 20

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        prog = sigmoid_0_to_1(self.progress())
        ceil.clear()

        for i in range(self.SAMPLE_SIZE):
            for j in range(self.SAMPLE_SIZE):
                i_indx = i / self.SAMPLE_SIZE
                j_indx = j / self.SAMPLE_SIZE

                # Bump up the minimal brightness this can yield
                before_hue = self.cur_perlin_noise([i_indx, j_indx])
                after_hue = self.next_perlin_noise([i_indx, j_indx])

                interpolated_hue = ((1 - prog) * before_hue) + (prog * after_hue)

                # to better center the effect
                bump = (1 / self.SAMPLE_SIZE) / 2
                color_obj = Color(hsl=(interpolated_hue, 1, 0.5))
                ceil[
                    bump + (i / self.SAMPLE_SIZE), bump + (j / self.SAMPLE_SIZE)
                ] = color_obj_to_rgb(color_obj)

        ceil.show()
        return super().render(delta, ceil)

    def interval_reached(self, ceiling: Ceiling) -> None:
        self.cur_perlin_noise = self.next_perlin_noise
        self.next_perlin_noise = PerlinNoise(octaves=np.random.randint(1, 4))
        return super().interval_reached(ceiling)


def run(**kwargs):
    interval = kwargs.get("interval")
    interval = float(interval) if interval else 1

    ceil = kwargs["ceiling"]
    ceil.use_float_cartesian(effect_radius=0.1)
    ceil.clear()

    render_loop = Render(interval * 3)
    render_loop.run(20, ceil)


if __name__ == "__main__":
    run(ceiling=Ceiling(test_mode=True), interval=sys.argv[1])
