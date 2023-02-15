#!/usr/bin/env python3

import numpy as np

from backend.settings import Settings
from backend.ceiling import Ceiling
from backend.state import State

import time

state = State()

ceil = state.ceiling

assert ceil is not None

ceil.set_by_index(0, np.array((100, 200, 200)))
print(ceil.get_by_index(0))

ceil.set_closest([0.5, 0.5], 0.2, np.array((100, 200, 200)))
print(ceil.get_closest([0.5, 0.5], 0.2))

ceil.set_decreasing_intensity([0, 1], 0.4, np.array((255, 0, 0)))

ceil.set_decreasing_intensity_merge([0.9, 1], 0.4, np.array((0, 0, 255)))
ceil.set_decreasing_intensity_merge([0.9, 1], 0.4, np.array((0, 255, 0)))

ceil.set_all_in_box([0.6, 0], [1, 0.4], np.array((0, 0, 0)))
ceil.set_all_in_radius([0.5, 0.5], 0.3, np.array((0, 120, 120)))

ceil.show()

time.sleep(2)
