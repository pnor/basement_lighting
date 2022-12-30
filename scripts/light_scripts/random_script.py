#!/usr/bin/env python3

# NAME: RANDOM

from random import random
import sys
from typing import Callable, List, Optional
import numpy as np
import importlib.util as importlib_util
import os
import colour
from backend.backend_types import RGB

from backend.ceiling import Ceiling
from backend.ceiling_animation import circle_clear
from backend.constants import SCRIPTS_PATH
from backend.util import color_obj_to_rgb, hex_to_rgb


def random_color() -> colour.Color:
    rand_hue = np.random.random()
    rand_sat = 0.7 + (0.3 * np.random.random())
    rand_lum = 0.35 + (0.3 * np.random.random())
    return colour.Color(hsl=(rand_hue, rand_sat, rand_lum))


def random_interval() -> float:
    return 0.8 + (3 * np.random.random())


def get_run_fn_from_other_scripts() -> Optional[Callable]:
    path = SCRIPTS_PATH

    # Choose a random file
    files_to_exclude = ["__init__.py", "__pycache__"]
    files = os.listdir("./" + path)
    files = list(filter(lambda f: f not in files_to_exclude, files))
    assert len(files) > 0

    random_file: str = files[int(len(files) * np.random.random())]

    # Get run function from script
    spec = importlib_util.spec_from_file_location(
        "random_func", path + "/" + random_file
    )
    if spec is None:
        return None

    mod = importlib_util.module_from_spec(spec)

    spec_loader = spec.loader
    if spec_loader is None:
        return None

    try:
        spec_loader.exec_module(mod)
    except Exception as e:  # Script fails to execute
        print(e)
        return None

    return mod.run


def run(**kwargs):
    ceil: Ceiling = kwargs["ceiling"]
    ceil.use_linear()
    ceil.clear()

    run_func = get_run_fn_from_other_scripts()
    if run_func is None:
        print("Got no runnable function")
    else:
        col = random_color()
        interval = random_interval()

        circle_clear(ceil, 0.2, color_obj_to_rgb(col))
        run_func(ceiling=ceil, color=col, interval=interval)


if __name__ == "__main__":
    run(ceiling=Ceiling())
