#!/usr/bin/env python3


"""
Common Animations for the ceiling object
"""

from typing import Tuple
import numpy as np
import colour
from microcontroller import time
from backend.backend_types import RGB
from backend.ceiling import Ceiling
from backend.util import clamp


FPS = 60
DELTA = 1 / FPS


def circle_clear(ceiling: Ceiling, duration: float, color: RGB) -> None:
    """Clears the currently display with a circle animation (centered at the middle)"""

    circle_out(ceiling, duration, color, (0.5, 0.5), 0.8)


def circle_out(
    ceiling: Ceiling,
    duration: float,
    color: RGB,
    origin: Tuple[float, float],
    max_radius: float,
) -> None:
    """Clears the currently display with a circle animation at the origin"""

    origin_x, origin_y = origin

    def _circle_outwards(ceil: Ceiling):
        FPS = 60
        DELTA = 1 / FPS
        cur_time = 0
        while cur_time < duration:
            cur_time += DELTA
            prog = cur_time / duration
            ceil[origin_x, origin_y, (max_radius * prog)] = color
            ceil[origin_x, origin_y, (max_radius * prog) - 0.05] = (0, 0, 0)
            ceil.show()
            time.sleep(DELTA)

    ceiling.with_polar(lambda c: _circle_outwards(c), (0, 0), search_range=0.1)


def fade_out(ceiling: Ceiling, duration: float, color: RGB) -> None:
    FPS = 60
    DELTA = 1 / FPS
    cur_time = 0

    color = np.array(color)

    while cur_time < duration:
        cur_time += DELTA
        prog = 1 - (cur_time / duration)
        ceiling.fill((color * (clamp(prog, 0, 1))).astype(int))
        ceiling.show()
        time.sleep(DELTA)
