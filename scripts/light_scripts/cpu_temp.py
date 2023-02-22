#!/usr/bin/env python3

# NAME: CPU Temperature

import os
import sys
import colour
import subprocess
from typing import List, Optional, Tuple, Union
from backend.backend_types import RGB
import numpy as np

from backend.ceiling import Ceiling
from backend.state import State
from backend.util import clamp, color_range
from scripts.library.render import RenderState


class Render(RenderState):
    def __init__(self, interval: Optional[float]):
        interval = interval if interval else 1

        self.COLD_RANGE = range(-9999, 10)
        self.COOL_RANGE = range(10, 30)
        self.MEDIUM_RANGE = range(30, 70)
        self.WARM_RANGE = range(70, 80)
        self.HOT_RANGE = range(80, 90)
        self.VERY_HOT_RANGE = range(90, 999999)

        colors = color_range(colour.Color("#00f"), colour.Color("#f00"), 6)
        self.COLD_COLOR = colors[0]
        self.COOL_COLOR = colors[1]
        self.MEDIUM_COLOR = colors[2]
        self.WARM_COLOR = colors[3]
        self.HOT_COLOR = colors[4]
        self.VERY_HOT_COLOR = colors[5]
        self.UNKNOWN_COLOR = np.array((255, 255, 255))

        super().__init__(interval)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        return super().render(delta, ceil)

    def interval_reached(self, ceil: Ceiling) -> None:
        assert self.interval is not None

        cmd = "cat /sys/class/thermal/thermal_zone0/temp"
        thermal_zone0_str = subprocess.check_output(cmd, shell=True)
        thermal_zone0_int = int(int(thermal_zone0_str) / 1000)

        last_light_index = int(
            clamp(thermal_zone0_int / 100, 0.01, 1) * ceil.number_lights()
        )

        if thermal_zone0_int in self.COLD_RANGE:
            col = self.COLD_COLOR
        elif thermal_zone0_int in self.COOL_RANGE:
            col = self.COOL_COLOR
        elif thermal_zone0_int in self.MEDIUM_RANGE:
            col = self.MEDIUM_COLOR
        elif thermal_zone0_int in self.WARM_RANGE:
            col = self.WARM_COLOR
        elif thermal_zone0_int in self.HOT_RANGE:
            col = self.HOT_COLOR
        elif thermal_zone0_int in self.VERY_HOT_RANGE:
            col = self.VERY_HOT_COLOR
        else:
            col = self.UNKNOWN_COLOR

        ceil.clear()
        ceil[0:last_light_index] = col
        ceil.show()

        return super().interval_reached(ceil)


def run(**kwargs):
    interval = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_linear()
    ceil.clear()

    render_loop = Render(interval)
    render_loop.run(1, ceil)


if __name__ == "__main__":
    run(
        ceiling=State().create_ceiling(),
        interval=sys.argv[1],
    )
