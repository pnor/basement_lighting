#!/usr/bin/env python3

# NAME: Mergers
# 2 points of different colors, bouncing around

import time
from typing import Optional, Union
import numpy as np
import colour

from backend.ceiling import Ceiling
from backend.state import State
from backend.util import colour_rgb_to_neopixel_rgb, rotate_vector
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, interval: Optional[float]):
        self.offset_1 = np.random.random()
        self.offset_2 = np.random.random()

        self.col_1 = colour.Color(hsl=(self.offset_1, 1, 0.5))
        self.col_2 = colour.Color(hsl=(self.offset_2, 1, 0.5))

        self.point_1 = np.array([0.5, 0.5])
        self.velocity_1 = np.array([1.0, 0]) * (1 / interval)
        self.velocity_1 = rotate_vector(
            self.velocity_1, np.random.random() * (np.pi * 2)
        )

        self.point_2 = np.array([0.5, 0.5])
        self.velocity_2 = np.array([1.0, 0]) * (1 / interval)
        self.velocity_2 = rotate_vector(self.velocity_2, np.random.random() * np.pi * 2)

        super().__init__(interval * 2)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        self.point_1 += self.velocity_1 * delta
        self.point_2 += self.velocity_2 * delta

        if self.point_1[0] < 0 or self.point_1[0] > 1:
            self.velocity_1[0] = -self.velocity_1[0]
        if self.point_1[1] < 0 or self.point_1[1] > 1:
            self.velocity_1[1] = -self.velocity_1[1]

        if self.point_2[0] < 0 or self.point_2[0] > 1:
            self.velocity_2[0] = -self.velocity_2[0]
        if self.point_2[1] < 0 or self.point_2[1] > 1:
            self.velocity_2[1] = -self.velocity_2[1]

        self.col_1.set_hue(self.progress() + self.offset_1)
        self.col_2.set_hue(self.progress() + self.offset_2)

        ceil.clear()
        ceil[self.point_1[0], self.point_1[1]] = colour_rgb_to_neopixel_rgb(
            self.col_1.rgb
        )
        ceil[self.point_2[0], self.point_2[1]] = colour_rgb_to_neopixel_rgb(
            self.col_2.rgb
        )
        ceil.show()

        return super().render(delta, ceil)

    def interval_reached(self, ceil: Ceiling) -> None:
        return super().interval_reached(ceil)


def run(**kwargs):
    interval = kwargs.get("interval") if kwargs.get("interval") else 1.0
    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_float_cartesian(effect_radius=0.3)
    ceil.clear()

    render_loop = Render(interval * 2)
    render_loop.run(30, ceil)


if __name__ == "__main__":
    run(ceiling=State().create_ceiling())
