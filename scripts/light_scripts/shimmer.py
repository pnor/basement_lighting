#!/usr/bin/env python3

# NAME: Shimmer

from typing import List, Optional, Union
import sys
import numpy as np
from backend.backend_types import RGB
from backend.ceiling import Ceiling
from backend.state import State
from backend.util import (
    clamp,
    color_format_to_rgb,
    dim_color_by_amount_fast,
)
from scripts.library.point import Point
from scripts.library.render import RenderState


class LifetimePoint:
    def __init__(self, lifetime: float, point: Point) -> None:
        self.point = point
        self.lifetime = lifetime


def create_random_particle() -> LifetimePoint:
    x = np.random.random() * 1
    y = np.random.random() * 1
    position = np.array([x, y])
    return LifetimePoint(0, Point(position, np.zeros(2), np.zeros(2)))


def interarrival_function(x: float) -> float:
    return np.random.exponential(1 / (5 * x))


class Render(RenderState):
    def __init__(self, color: RGB, interval: Optional[float]):
        # color
        self.color = color

        # speed
        interval = interval if interval else 1
        self.rate = interval * 0.25

        # starting particles
        self.particles: List[LifetimePoint] = []
        for _ in range(6):
            self.particles += [create_random_particle()]

        # spawning of particles
        self.cur = 0
        self.interval = interarrival_function(self.rate)
        self.LIFETIME = 1 * (1 / interval)
        super().__init__(self.interval)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        ceil.clear()
        for i in range(len(self.particles)):
            self.particles[i].lifetime += delta
            col = dim_color_by_amount_fast(
                self.color, 1 - clamp(self.particles[i].lifetime / self.LIFETIME, 0, 1)
            )
            self.particles[i].point.draw(col, ceil)

        self.particles = list(
            filter(lambda t: t.lifetime < self.LIFETIME, self.particles)
        )
        ceil.show()

        return super().render(delta, ceil)

    def interval_reached(self, ceil: Ceiling) -> None:
        self.interval = interarrival_function(self.rate)

        for _ in range(np.random.randint(5, 10)):
            self.particles += [create_random_particle()]

        return super().interval_reached(ceil)


def run(**kwargs):
    color_input = color_format_to_rgb(kwargs["color"])
    speed = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_cartesian(search_range=0.2)
    ceil.clear()

    render_loop = Render(color_input, speed)
    render_loop.run(30, ceil)


if __name__ == "__main__":
    run(
        ceiling=State().create_ceiling(),
        color=sys.argv[1],
        interval=sys.argv[2],
    )
