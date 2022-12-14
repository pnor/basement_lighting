#!/usr/bin/env python3

# Blinks rows

import sys
import time

from typing import List

from backend.ceiling import Ceiling

if len(sys.argv) != 3:
    print("Usage: python blink.py [color hex string] [blink interval in seconds]")

color_input = sys.argv[1]
interval = float(sys.argv[2])

on_rgb = hex_to_rgb(color_input)
off_rgb = [0] * len(on_rgb)

ceil = Ceiling()
ceil.use_row()
ceil.clear()

opt_rows = ceil.rows()
rows: List[int] = []
if opt_rows is None:
    raise NotImplementedError(
        "Indexing should be row indexing and rows should be defined"
    )
else:
    rows = opt_rows

cur = 0

while True:
    ceil[cur] = on_rgb
    ceil[cur - 1] = off_rgb
    cur = (cur + 1) % len(rows)
    ceil.show()
    time.sleep(interval)
