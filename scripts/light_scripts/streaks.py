#!/usr/bin/env python3

# NAME: Streaks

import sys
import time
from typing import Optional, Union
import numpy as np
import colour

from backend.backend_types import RGB
from backend.ceiling import Ceiling
from backend.util import (
    color_format_to_rgb,
    color_obj_to_rgb,
    rotate_vector,
)
from backend.ceiling_animation import circle_clear
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, speed: float, interval: Optional[float]):
        interval = interval if interval else 1
        self.color_obj = colour.Color(hsl=(0, 1, 0.5))
        self._point = np.array([0.5, 0.5])
        self._velocity = np.array([1.0, 0]) * speed
        self._velocity = rotate_vector(self._velocity, np.random.random() * np.pi * 2)
        self.speed = speed
        super().__init__(interval)

    def reset(self):
        self.color_obj = colour.Color(hsl=(0, 1, 0.5))
        self._point = np.array([0.5, 0.5])
        self._velocity = np.array([1.0, 0]) * self.speed
        self._velocity = rotate_vector(self._velocity, np.random.random() * np.pi * 2)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        self._point += self._velocity * delta

        if self._point[0] < 0 or self._point[0] > 1:
            self._velocity[0] = -self._velocity[0]

        if self._point[1] < 0 or self._point[1] > 1:
            self._velocity[1] = -self._velocity[1]

        ceil[self._point[0], self._point[1]] = color_obj_to_rgb(self.color_obj)
        ceil.show()

        self.color_obj.hue = (self.color_obj.hue + 0.02) % 1
        return super().render(delta, ceil)

    def interval_reached(self, ceil: Ceiling) -> None:
        circle_clear(ceil, 0.2, (255, 255, 255))
        self.reset()
        return super().interval_reached(ceil)


def run(**kwargs):
    color_input = kwargs["color"]
    speed = float(kwargs["interval"])

    color = color_format_to_rgb(color_input)

    ceil = kwargs["ceiling"]
    ceil.use_cartesian()
    ceil.clear()

    render_loop = Render(speed, 10)
    render_loop.run(30, ceil)


if __name__ == "__main__":
    run(
        ceiling=Ceiling(),
        interval=sys.argv[1],
    )
