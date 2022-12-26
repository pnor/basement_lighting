#!/usr/bin/env python3

# NAME: Sparkle
# Create a glittering effect with the LEDs


import sys
import time
from typing import Optional, Union
import numpy as np
from backend.backend_types import RGB

from backend.ceiling import Ceiling
from backend.util import color_range, dim_color
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, color: RGB, number_lights: int, interval: Optional[float]):
        self.progresses = np.random.randint(0, 199 + 1, number_lights)
        self.progress_indeces = (((np.arange(100) / 99) ** 10) * 99).astype(int)
        self.progress_indeces = list(self.progress_indeces) + list(
            reversed(self.progress_indeces)
        )

        self.colors = color_range(dim_color(color), color, 100)
        self.colors = self.colors + list(reversed(self.colors))

        super().__init__(interval)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        # TODO redo how we find the colors
        index = int(self.progress() * len(self.colors))
        for i in range(len(self.progresses)):
            progress_index = self.progress_indeces[self.progresses[i]]
            progress_index = (progress_index + index) % len(self.colors)
            ceil[i] = self.colors[progress_index]
        ceil.show()


def run(**kwargs):
    color_input = kwargs["color"]
    interval = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_linear()
    ceil.clear()

    render_loop = Render(color_input, ceil.NUMBER_LIGHTS, interval)
    render_loop.run(60, ceil)
    # colors = color_range(dim_color(color_input), color_input, 100)
    # colors = colors + list(reversed(colors))

    # FPS = 60
    # DELTA = 1 / FPS

    # progress_indeces = (((np.arange(100) / 99) ** 10) * 99).astype(int)
    # progress_indeces = list(progress_indeces) + list(reversed(progress_indeces))
    # progresses = np.random.randint(0, 199 + 1, ceil.NUMBER_LIGHTS)

    # cur_time = 0

    # while True:
    #     cur_time += DELTA
    #     if cur_time > (interval / 200):
    #         cur_time = 0
    #         progresses = (progresses + 1) % 200
    #         for i in range(len(progresses)):
    #             ceil[i] = colors[progress_indeces[progresses[i]]]

    #         ceil.show()
    #     time.sleep(DELTA)


if __name__ == "__main__":
    run(ceiling=Ceiling(test_mode=True), color=sys.argv[1], interval=sys.argv[2])
