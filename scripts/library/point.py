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
        self._position = position
        self._velocity = velocity
        self._acceleration = acceleration

    def step(self, delta: float):
        self._position += self._velocity * delta
        self._velocity += self._acceleration * delta

    def draw(self, color: RGB, ceiling: Ceiling) -> None:
        ceiling[self._position[0], self._position[1]] = color
