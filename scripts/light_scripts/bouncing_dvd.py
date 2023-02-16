#!/usr/bin/env python3

# NAME: Bouncing DVD
# A point bounces around the edges of the display


import sys
import time
from typing import Optional, Union
import numpy as np
from backend.backend_types import RGB

from backend.ceiling import Ceiling
from backend.util import (
    color_format_to_rgb,
    rotate_vector,
)
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, color: RGB, interval: Optional[float]):
        self._color = color
        self._point = np.array([0.5, 0.5])
        self._velocity = np.array([1.0, 0]) * interval
        self._velocity = rotate_vector(self._velocity, np.random.random() * (2 * np.pi))
        super().__init__(None)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        self._point += self._velocity * delta

        if self._point[0] < 0 or self._point[0] > 1:
            self._velocity[0] = -self._velocity[0]

        if self._point[1] < 0 or self._point[1] > 1:
            self._velocity[1] = -self._velocity[1]

        ceil.clear()
        ceil[self._point[0], self._point[1]] = self._color
        ceil.show()

        return super().render(delta, ceil)


def run(**kwargs):
    color_input = kwargs["color"]
    speed = float(kwargs["interval"])

    color = color_format_to_rgb(color_input)

    ceil = kwargs["ceiling"]
    ceil.use_float_cartesian(effect_radius=0.3)
    ceil.clear()

    render_loop = Render(color, speed)
    render_loop.run(30, ceil)


if __name__ == "__main__":
    run(
        ceiling=Ceiling(),
        color=sys.argv[1],
        interval=sys.argv[2],
    )
