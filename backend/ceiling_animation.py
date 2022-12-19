#!/usr/bin/env python3


"""
Common Animations for the ceiling object
"""

import colour
from microcontroller import time
from backend.backend_types import RGB
from backend.ceiling import Ceiling


def circle_clear(ceiling: Ceiling, duration: float, color: RGB) -> None:
    """Clears the currently display with a circle animation"""

    def _circle_outwards(ceil: Ceiling):
        FPS = 60
        DELTA = 1 / FPS
        cur_time = 0
        max_radius = 0.8
        while cur_time < duration:
            cur_time += DELTA
            prog = cur_time / duration
            ceil[0.5, 0.5, (max_radius * prog)] = color
            ceil[0.5, 0.5, (max_radius * prog) - 0.05] = (0, 0, 0)
            ceil.show()
            time.sleep(DELTA)

    ceiling.with_polar(lambda c: _circle_outwards(c), (0.5, 0.5), search_range=0.1)
