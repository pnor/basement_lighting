#!/usr/bin/env python3


"""
Common Animations for the ceiling object
"""

from typing import Tuple
import numpy as np
import colour
import time
from backend.backend_types import RGB
from backend.ceiling import Ceiling
from backend.transitions.circle_out import CircleOut
from backend.transitions.fade_out import FadeOut
from backend.util import clamp


def circle_clear(ceiling: Ceiling, duration: float, color: colour.Color) -> None:
    """Clears the currently display with a circle animation (centered at the middle)"""
    animation = CircleOut(duration, color)
    animation.run(60, ceiling)


def fade_out(ceiling: Ceiling, duration: float) -> None:
    """Clears the currently display by fading it out over time"""
    animation = FadeOut(duration)
    animation.run(60, ceiling)


def black_out(ceiling: Ceiling) -> None:
    """Clears current display immediately"""
    ceiling.clear()
