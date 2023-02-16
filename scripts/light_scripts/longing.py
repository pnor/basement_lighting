#!/usr/bin/env python3

# NAME: Longing

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
    def __init__(
        self, color: NDArray[np.int32], lifetime: float, point: Point, radius: float
    ) -> None:
        self.color = color
        self.point = point
        self.radius = radius
        self.lifetime = lifetime
        self.max_lifetime = lifetime

    def draw(self, x: float, y: float, color: NDArray[np.int32], ceiling: Ceiling):
        def _draw(ceil: Ceiling):
            ceil[x, y] = color

        ceiling.with_float_cartesian(_draw, effect_radius=self.radius)


def create_random_point() -> ColorLifetimePoint:
    pos = np.random.random(2)
    col = np.array(color_format_to_rgb("#2e05fc"))

    return ColorLifetimePoint(col, 5, Point(pos, np.zeros(2), np.zeros(2)), 0.2)


def create_random_shine() -> ColorLifetimePoint:
    pos = np.random.random(2)
    col = np.array(color_format_to_rgb("#eadfaf"))

    return ColorLifetimePoint(col, 1, Point(pos, np.zeros(2), np.zeros(2)), 0.02)


def interarrival_function(x: float) -> float:
    return np.random.exponential(1 / (3 * x))


class Render(RenderState):
    def __init__(self, interval: Optional[float]):
        interval = interval if interval else 1
        # starting particles
        self.particles: List[ColorLifetimePoint] = []

        # spawning of particles
        self.cur = 0
        self.LIFETIME = interval
        super().__init__(0.25)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        ceil.clear()

        for p in self.particles:
            p.lifetime -= delta

            x = p.point.position[0]
            y = p.point.position[1]

            prog = clamp(p.lifetime / p.max_lifetime, 0, 1)
            if prog > 0.5:
                prog = (1 - prog) * 2
            else:
                prog *= 2
            prog = sigmoid_0_to_1(prog)

            col = (p.color * prog).astype(np.int32)
            p.draw(x, y, col, ceil)

        self.particles = list(filter(lambda p: p.lifetime > 0, self.particles))

        ceil.show()

        return super().render(delta, ceil)

    def interval_reached(self, ceil: Ceiling) -> None:
        if np.random.random() < 0.5:
            self.particles += [create_random_point(), create_random_point()]
        if np.random.random() < 0.8:
            self.particles += [
                create_random_shine(),
                create_random_shine(),
                create_random_shine(),
            ]
        return super().interval_reached(ceil)


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
