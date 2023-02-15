#!/usr/bin/env python3

# NAME: Sparkle
# Create a glittering effect with the LEDs


import sys
import time
from typing import Optional, Union
import numpy as np

from backend.state import State
from backend.backend_types import RGB
from backend.ceiling import Ceiling
from backend.util import color_range, dim_color
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, color: RGB, number_lights: int, interval: Optional[float]):
        interval = interval if interval else 1
        # progress for each LED in color cycle
        # 0..199
        self.progresses = np.random.randint(0, number_lights, number_lights)

        # Indeces used to index into colors
        # doesn't cover every index to make the fade effect
        all_steps = number_lights // 2
        self.progress_indeces = (
            ((np.arange(all_steps) / (all_steps - 1)) ** 10) * (all_steps - 1)
        ).astype(int)
        self.progress_indeces = list(self.progress_indeces) + list(
            reversed(self.progress_indeces)
        )

        # All colors in a range, indexed into using progress indeces
        self.colors = color_range(dim_color(color), color, all_steps)
        self.colors = self.colors + list(reversed(self.colors))

        super().__init__(interval * 7)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        index = int(self.progress() * len(self.progress_indeces))
        for i in range(len(self.progresses)):
            prog_index = (index + self.progresses[i]) % len(self.progress_indeces)
            color_index = self.progress_indeces[prog_index]
            ceil[i] = self.colors[color_index]

        ceil.show()


def run(**kwargs):
    color_input = kwargs["color"]
    interval = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_linear()
    ceil.clear()

    render_loop = Render(color_input, ceil.number_lights(), interval)
    render_loop.run(30, ceil)


if __name__ == "__main__":
    run(
        ceiling=State().create_ceiling(),
        color=sys.argv[1],
        interval=sys.argv[2],
    )
