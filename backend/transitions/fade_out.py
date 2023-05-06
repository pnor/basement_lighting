#!/usr/bin/env python3

from typing import Union
import numpy as np
import colour

from backend.ceiling import Ceiling
from backend.util import color_obj_to_rgb
from scripts.library.render import RenderState


class FadeOut(RenderState):
    def __init__(self, duration: float):
        self.running_state = True
        target_val = 0.001
        self.mult_step = target_val ** ((1 / 60) / duration)
        super().__init__(duration)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        for i in range(ceil.number_lights()):
            color = ceil.get_by_index(i).astype(np.float64)
            color *= self.mult_step
            color = color.astype(np.int32)
            ceil.set_by_index(i, color)

        ceil.show()

        return self.running_state

    def interval_reached(self, ceil: Ceiling) -> None:
        self.running_state = False
        return super().interval_reached(ceil)
