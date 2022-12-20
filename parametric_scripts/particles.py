#!/usr/bin/env python3

# NAME: Particles

from typing import List
import sys
import time
import numpy as np
from numpy._typing import NDArray
from backend.backend_types import RGB
from backend.ceiling import Ceiling
from backend.util import (
    clamp,
    color_format_to_rgb,
    dim_color_by_amount_fast,
    sigmoid_0_to_1,
)


class Particle:
    def __init__(
        self,
        position: NDArray[np.float64],
        velocity: NDArray[np.float64],
        acceleration: NDArray[np.float64],
        lifetime: float,
    ) -> None:
        self._position = position
        self._velocity = velocity
        self._acceleration = acceleration
        self._lifetime = lifetime
        self._cur = 0

    def step(self, delta: float):
        self._cur += delta
        self._position += self._velocity * delta
        self._velocity += self._acceleration * delta

    def life_left(self) -> float:
        return clamp(self._cur / self._lifetime, 0, 1)

    def draw(self, ceiling: Ceiling, base_color: RGB) -> None:
        prog = sigmoid_0_to_1(1 - self.life_left())
        col = dim_color_by_amount_fast(base_color, prog)
        ceiling[self._position[0], self._position[1]] = col

    def is_dead(self) -> bool:
        return self._cur > self._lifetime


def create_random_particle(speed: float) -> Particle:
    angle = np.random.random() * (2 * np.pi)
    radius = 0.6
    x = (radius * np.cos(angle)) + 0.5
    y = (radius * np.sin(angle)) + 0.5

    MAX_MAGNITUDE = 3 * speed
    v_angle = angle - np.pi - (np.random.random() * (np.pi / 3))
    v_magnitude = np.random.random() * MAX_MAGNITUDE
    v_x = v_magnitude * np.cos(v_angle)
    v_y = v_magnitude * np.sin(v_angle)

    accel = np.array(
        [np.random.random() * MAX_MAGNITUDE, np.random.random() * MAX_MAGNITUDE]
    )

    LIFETIME = 1

    return Particle(np.array([x, y]), np.array([v_x, v_y]), accel, LIFETIME)


def run(**kwargs):
    color_input = color_format_to_rgb(kwargs["color"])
    speed = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_cartesian(search_range=0.1)
    ceil.clear()

    particles: List[Particle] = []
    for i in range(6):
        particles += [create_random_particle(speed)]

    FPS = 60
    DELTA = 1 / 60
    while True:
        ceil.clear(False)

        for p in particles:
            p.step(DELTA)
            p.draw(ceil, color_input)
            if p.is_dead():
                particles = list(filter(lambda x: x != p, particles))

        ceil.show()

        if len(particles) < 3:
            for i in range(np.random.randint(6)):
                particles += [create_random_particle(speed)]

        if np.random.random() < 0.04:
            particles += [create_random_particle(speed)]

        time.sleep(DELTA)


if __name__ == "__main__":
    run(ceiling=Ceiling(), color=sys.argv[1], interval=sys.argv[2])
