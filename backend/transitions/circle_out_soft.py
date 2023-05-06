#!/usr/bin/env python3

from typing import Union
import numpy as np
import colour

from backend.ceiling import Ceiling
from backend.coordinate_conversions import polar
from backend.util import color_obj_to_rgb
from scripts.library.render import RenderState


class CircleOutSoft(RenderState):
    def __init__(self, duration: float, color: colour.Color):
        self.color = color_obj_to_rgb(color)
        self.clear_color = np.array([0, 0, 0])

        self.running_state = True
        self.MAX_RADIUS = 0.9
        self.last_progress = -1.0

        super().__init__(duration)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        # strictly increasing progress
        prog = max(self.last_progress, self.progress())
        self.last_progress = prog

        fill_radius = self.MAX_RADIUS * prog
        clear_radius = np.clip(fill_radius - 0.1, 0, 1)

        ceil.set_all_in_radius([0.5, 0.5], fill_radius, self.color)
        for i in np.linspace(0, 2 * np.pi, 15):
            ceil.set_decreasing_intensity_merge(
                polar(fill_radius, [i], [0.5, 0.5]), 0.08, self.color
            )
        ceil.set_all_in_radius([0.5, 0.5], clear_radius, self.clear_color)

        ceil.show()

        return self.running_state

    def interval_reached(self, ceil: Ceiling) -> None:
        self.running_state = False
        return super().interval_reached(ceil)
