#!/usr/bin/env python3

# NAME: Sine-ing out Rainbow
# Circular Bands emanting from the center, rainbow

import sys
import time
from typing import Optional, Union
import numpy as np
from backend.backend_types import RGB
import colour

from backend.ceiling import Ceiling
from backend.util import color_format_to_rgb, color_obj_to_rgb, sigmoid_0_to_1
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, interval: Optional[float]):
        # Number of bands
        self.SAMPLE_SIZE = 16
        interval = self.interval if self.interval else 1

        self.color_obj = colour.Color(hsl=(0, 1, 0.5))
        self.radiuses = (np.arange(self.SAMPLE_SIZE) + 1) / self.SAMPLE_SIZE
        super().__init__(interval * 3)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        ceil.clear(False)
        for theta in range(0, 360, 10):
            for i in range(len(self.radiuses)):
                amt = np.sin((i / len(self.radiuses) + (self.progress())) * (2 * np.pi))
                amt = (amt / 2) + 0.5
                self.color_obj.set_hue(amt)
                ceil[self.radiuses[i], theta] = color_obj_to_rgb(self.color_obj)

        ceil.show()
        return super().render(delta, ceil)


def run(**kwargs):
    interval = float(kwargs["interval"])

    ceil = kwargs["ceiling"]
    ceil.use_float_polar(origin=(0.5, 0.5), effect_radius=0.2)

    render_loop = Render(interval)
    render_loop.run(20, ceil)


if __name__ == "__main__":
    run(ceiling=Ceiling(test_mode=True), interval=sys.argv[1])
