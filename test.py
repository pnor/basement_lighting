#!/usr/bin/env python3

import numpy as np

from backend.settings import Settings
from backend.ceiling import Ceiling
from backend.state import State

import time

state = State()

ceil = state.ceiling

ceil.set_by_index(0, np.array((100, 200, 200)))
print(ceil.get_by_index(0))
ceil.show()

time.sleep(2)
