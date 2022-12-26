#!/usr/bin/env python3

# NAME: Sine-ing out
# Circular Bands emanting from the center


import sys
import time
from typing import Optional, Union
import numpy as np
from backend.backend_types import RGB

from backend.ceiling import Ceiling
from backend.util import color_format_to_rgb, sigmoid_0_to_1
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, color: RGB, interval: Optional[float]):
        # Number of bands
        self.SAMPLE_SIZE = 8
        # Brightest color this will yield
        self.color = np.array(color)
        self.radiuses = (np.arange(self.SAMPLE_SIZE) + 1) / self.SAMPLE_SIZE
        super().__init__(interval)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        ceil.clear(False)
        for theta in range(0, 360, 10):
            for i in range(len(self.radiuses)):
                amt = np.sin((i / len(self.radiuses) + (self.progress())) * (2 * np.pi))
                amt = (amt / 2) + 0.5
                ceil[self.radiuses[i], theta] = (self.color * amt).astype(int)

        ceil.show()
        return super().render(delta, ceil)


def run(**kwargs):
    color_input = color_format_to_rgb(kwargs["color"])
    interval = float(kwargs["interval"])

    ceil = kwargs["ceiling"]
    ceil.use_float_polar(origin=(0.5, 0.5), effect_radius=0.1)

    render_loop = Render(color_input, interval)
    render_loop.run(20, ceil)


if __name__ == "__main__":
    run(ceiling=Ceiling(), color=sys.argv[1], interval=sys.argv[2])
