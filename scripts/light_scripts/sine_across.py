#!/usr/bin/env python3

# NAME: Sine Across
# Bands moving across using sine waves


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
        self.SAMPLE_SIZE = 7
        # Brightest color this will yield
        self.color = np.array(color)

        self.horizs = (np.arange(self.SAMPLE_SIZE) + 1) / self.SAMPLE_SIZE

        super().__init__(interval)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        ceil.clear(False)

        for y in range(10):
            for i in range(len(self.horizs)):
                amt: float = np.sin(
                    (i / len(self.horizs) + (self.progress())) * (2 * np.pi)
                )
                amt = np.sin((i / len(self.horizs) + (self.progress())) * (2 * np.pi))
                amt = (amt / 2) + 0.5
                ceil[self.horizs[i], (y / 10)] = (self.color * amt).astype(int)

        ceil.show()
        return super().render(delta, ceil)


def run(**kwargs):
    color_input = color_format_to_rgb(kwargs["color"])
    interval = float(kwargs["interval"])

    SAMPLE_SIZE = 7
    color = np.array(color_input)

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_float_cartesian(effect_radius=0.2)
    ceil.clear()

    render_loop = Render(color_input, interval)
    render_loop.run(20, ceil)


if __name__ == "__main__":
    run(ceiling=Ceiling(test_mode=True), color=sys.argv[1], interval=sys.argv[2])
