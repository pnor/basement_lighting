#!/usr/bin/env python3

# NAME: Uptime
# Shows number of days the system has been up, 1 day per LED
# If system has been up for less than a day, will show 1 led per hour
# Only shows up to 1 year

import os
import sys
import colour
import subprocess
from typing import List, Optional, Tuple, Union
from backend.backend_types import RGB
import numpy as np

from backend.ceiling import Ceiling
from backend.state import State
from backend.util import clamp, color_range, dim_color, dim_color_by_amount, hex_to_rgb
from scripts.library.render import RenderState


def run(**kwargs):
    interval = float(kwargs["interval"])

    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_linear()
    ceil.clear()

    SECONDS_IN_DAY = 86400
    SECONDS_IN_HOUR = 3600

    HOURS_COLOR = hex_to_rgb("#00ffcc")
    DAYS_COLOR_SECONDARY = hex_to_rgb("#0011aa")
    DAYS_COLOR = hex_to_rgb("#00ccff")

    cmd = "cat /proc/uptime | awk '{ print $1 }'"
    uptime_seconds_str = subprocess.check_output(cmd, shell=True)
    uptime_seconds = float(uptime_seconds_str)

    # If system has been up for less than a day, show output in hours
    if uptime_seconds < SECONDS_IN_DAY:
        num_hours = int(uptime_seconds / SECONDS_IN_HOUR)
        if num_hours > ceil.number_lights():
            ceil.fill(HOURS_COLOR)
        elif num_hours == 0:
            ceil.fill(np.array((60, 60, 60)))
        else:
            ceil[:num_hours] = HOURS_COLOR
    else:
        num_days = int(uptime_seconds / SECONDS_IN_DAY)
        if num_days > ceil.number_lights() * 2:
            ceil.fill(DAYS_COLOR)
        elif num_days > ceil.number_lights():
            ceil.fill(DAYS_COLOR_SECONDARY)
            ceil[: (num_days - ceil.number_lights())] = DAYS_COLOR
        else:
            ceil[:num_days] = DAYS_COLOR

    ceil.show()


if __name__ == "__main__":
    run(
        ceiling=State().create_ceiling(),
        interval=sys.argv[1],
    )
