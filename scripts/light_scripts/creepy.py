#!/usr/bin/env python3

# NAME: Creepy


import sys
import time
from typing import Optional, Union
import numpy as np
from backend.backend_types import RGB

from backend.ceiling import Ceiling
from backend.util import color_range, dim_color_by_amount
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, color: RGB, number_lights: int, interval: Optional[float]):
        interval = interval if interval else 1
        self.SPEED_FACTOR = 0.01 * interval

        # progress for each LED in color cycle
        self.progresses = np.random.random(number_lights)

        # Indeces used to index into colors
        PROGRESS_INDECES_SIZE = 50
        NUMBER_SPIKES = 1
        self.light_amount = np.zeros(50)
        for i in range(len(self.light_amount)):
            self.light_amount[i] = np.random.random() * 0.3
        # place some random spikes
        for i in range(NUMBER_SPIKES):
            self.light_amount[np.random.randint(0, high=len(self.light_amount))] = 1

        # self.colors = color_range(dim_color(color), color, 10)
        self.colors = [dim_color_by_amount(color, x) for x in self.light_amount]

        super().__init__(interval * 7)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        self.progresses = ((delta * self.SPEED_FACTOR) + self.progresses) % 1
        for i in range(len(self.progresses)):
            index = int(self.progresses[i] * (len(self.colors) - 1))
            ceil[i] = self.colors[index]

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
        ceiling=Ceiling(test_mode=True),
        color=sys.argv[1],
        interval=sys.argv[2],
    )
