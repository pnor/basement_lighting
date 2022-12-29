#!/usr/bin/env python3

import numpy as np
from numpy._typing import NDArray
from backend.backend_types import RGB

from backend.ceiling import Ceiling


class Point:
    def __init__(
        self,
        position: NDArray[np.float64],
        velocity: NDArray[np.float64],
        acceleration: NDArray[np.float64],
    ) -> None:
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration

    def step(self, delta: float):
        self.position += self.velocity * delta
        self.velocity += self.acceleration * delta

    def draw(self, color: RGB, ceiling: Ceiling) -> None:
        ceiling[self.position[0], self.position[1]] = color
