#!/usr/bin/env python3

# NAME: Ping Pong

import sys
import time
from typing import List, Optional, Union
import numpy as np
import colour
from numpy._typing import NDArray

from backend.ceiling import Ceiling
from backend.util import color_obj_to_rgb, colour_rgb_to_neopixel_rgb, rotate_vector
from scripts.library.point import Point
from scripts.library.render import RenderState


class ColorPoint:
    def __init__(
        self,
        pos,
        velocity,
        color: colour.Color,
        offset: float,
    ) -> None:
        self.point = Point(pos, velocity, np.zeros(2))
        self.offset = offset
        self.color = color


def random_point(speed: float) -> ColorPoint:
    pos = np.random.random(2)

    offset = np.random.random()
    color = colour.Color(hsl=(offset, 1, 0.5))

    velocity = np.array([speed, 0])
    velocity = rotate_vector(velocity, np.random.random() * 360)

    p = ColorPoint(pos, velocity, color, offset)
    return p


class Render(RenderState):
    def __init__(self, interval: Optional[float]):
        assert interval is not None

        self.points: List[ColorPoint] = []
        for i in range(4):
            self.points += [random_point(0.5 + (np.random.random() * 1.5 * interval))]

        super().__init__(interval)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        ceil.clear()

        for p in self.points:
            p.point.step(delta)
            p.color.set_hue(self.progress() + p.offset)

            if p.point.position[0] < 0 or p.point.position[0] > 1:
                p.point.velocity[0] = -p.point.velocity[0]
            if p.point.position[1] < 0 or p.point.position[1] > 1:
                p.point.velocity[1] = -p.point.velocity[1]

            ceil[p.point.position[0], p.point.position[1]] = color_obj_to_rgb(p.color)

        ceil.show()

        return super().render(delta, ceil)

    def interval_reached(self, ceil: Ceiling) -> None:
        return super().interval_reached(ceil)


def run(**kwargs):
    interval = kwargs.get("interval") if kwargs.get("interval") else 1.0
    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_cartesian()
    ceil.clear()

    render_loop = Render(interval)
    render_loop.run(30, ceil)


if __name__ == "__main__":
    run(ceiling=Ceiling(test_mode=True, interval=sys.argv[1]))
