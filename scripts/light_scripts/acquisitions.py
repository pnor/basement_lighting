#!/usr/bin/env python3

# NAME: Acquisitions

import sys
import colour
from typing import List, Optional, Tuple, Union

from numpy._typing import NDArray
from backend.backend_types import RGB
import numpy as np

from backend.ceiling import Ceiling
from backend.util import (
    clamp,
    color_format_to_rgb,
    color_obj_to_rgb,
    color_range,
    dim_color,
    sigmoid_0_to_1,
)
from backend.ceiling_animation import circle_clear

from scripts.library.point import Point
from scripts.library.render import RenderState


class ColorLifetimePoint:
    def __init__(self, color: NDArray[np.int32], lifetime: float, point: Point) -> None:
        self.color = color
        self.point = point
        self.lifetime = lifetime


def create_random_point() -> ColorLifetimePoint:
    pos = np.random.random(2)
    point = Point(pos, np.zeros(2), np.zeros(2))

    random_hue = np.random.random()
    col = colour.Color(hsl=(random_hue, 1, 0.5))
    col = np.array(color_obj_to_rgb(col))

    return ColorLifetimePoint(col, 0, Point(pos, np.zeros(2), np.zeros(2)))


def interarrival_function(x: float) -> float:
    return np.random.exponential(1 / (5 * x))


class Render(RenderState):
    def __init__(self, interval: Optional[float]):
        interval = interval if interval else 1
        # starting particles
        self.particles: List[ColorLifetimePoint] = []

        # spawning of particles
        self.cur = 0
        self.LIFETIME = 2 * interval
        super().__init__(interval)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        ceil.clear(False)

        for p in self.particles:
            p.lifetime += delta

            x = p.point.position[0]
            y = p.point.position[1]

            prog = clamp(p.lifetime / self.LIFETIME, 0, 1)
            if prog > 0.5:
                prog = (1 - prog) * 2
            else:
                prog *= 2
            prog = sigmoid_0_to_1(prog)

            col = (p.color * prog).astype(np.int32)
            ceil[x, y] = col

        self.particles = list(
            filter(lambda p: p.lifetime < self.LIFETIME, self.particles)
        )
        ceil.show()

        if np.random.random() < 0.2:
            self.particles += [create_random_point()]
        return super().render(delta, ceil)


def run(**kwargs):
    interval = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_float_cartesian(effect_radius=0.2)
    ceil.clear()

    render_loop = Render(interval)
    render_loop.run(30, ceil)


if __name__ == "__main__":
    run(
        ceiling=Ceiling(),
        interval=sys.argv[1],
    )
