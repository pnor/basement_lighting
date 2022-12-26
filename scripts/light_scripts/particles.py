#!/usr/bin/env python3

# NAME: Particles

from typing import List, Optional, Union
import sys
import numpy as np
from backend.backend_types import RGB
from backend.ceiling import Ceiling
from backend.util import (
    color_format_to_rgb,
    dim_color_by_amount_fast,
)
from scripts.library.point import Point
from scripts.library.render import RenderState


class LifetimePoint:
    def __init__(self, lifetime: float, point: Point) -> None:
        self.point = point
        self.lifetime = lifetime


def create_random_particle(speed: float) -> LifetimePoint:
    angle = np.random.random() * (2 * np.pi)
    radius = 0.6
    x = (radius * np.cos(angle)) + 0.5
    y = (radius * np.sin(angle)) + 0.5
    position = np.array([x, y])

    MAX_MAGNITUDE = 3 * speed
    v_angle = angle - np.pi - (np.random.random() * (np.pi / 3))
    v_magnitude = np.random.random() * MAX_MAGNITUDE
    v_x = v_magnitude * np.cos(v_angle)
    v_y = v_magnitude * np.sin(v_angle)
    velocity = np.array([v_x, v_y])

    accel = np.array(
        [np.random.random() * MAX_MAGNITUDE, np.random.random() * MAX_MAGNITUDE]
    )

    return LifetimePoint(0, Point(position, velocity, accel))


def interarrival_function(x: float) -> float:
    return np.random.exponential(1 / (5 * x))


class Render(RenderState):
    def __init__(self, color: RGB, interval: Optional[float]):
        # color
        self.color = color

        # speed
        interval = interval if interval else 1
        self.speed = interval / 2

        # starting particles
        self.particles: List[LifetimePoint] = []
        for _ in range(6):
            self.particles += [create_random_particle(self.speed)]

        # spawning of particles
        self.cur = 0
        self.interval = interarrival_function(self.speed)
        self.LIFETIME = 1 * (1 / interval)
        super().__init__(self.interval)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        ceil.clear(False)
        for i in range(len(self.particles)):
            self.particles[i].lifetime += delta
            self.particles[i].point.step(delta)
            col = dim_color_by_amount_fast(
                self.color, 1 - (self.particles[i].lifetime / self.LIFETIME)
            )
            self.particles[i].point.draw(col, ceil)

        self.particles = list(
            filter(lambda t: t.lifetime < self.LIFETIME, self.particles)
        )
        ceil.show()

        if np.random.random() < 0.04:
            self.particles += [create_random_particle(self.speed)]

        return super().render(delta, ceil)

    def interval_reached(self, ceil: Ceiling) -> None:
        self.interval = interarrival_function(self.speed)
        self.particles += [create_random_particle(self.speed)]
        return super().interval_reached(ceil)


def run(**kwargs):
    color_input = color_format_to_rgb(kwargs["color"])
    speed = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_cartesian(search_range=0.1)
    ceil.clear()

    render_loop = Render(color_input, speed)
    render_loop.run(30, ceil)


if __name__ == "__main__":
    run(
        ceiling=Ceiling(),
        color=sys.argv[1],
        interval=sys.argv[2],
    )
