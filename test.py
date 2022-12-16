#!/usr/bin/env python3

import importlib.util
from typing import Callable


def run_script(file):
    file_to_run = file
    color = "#f00"
    interval = 1

    f = function_from_file(file_to_run)
    f(color=color, interval=interval)


def function_from_file(file: str) -> Callable:
    spec = importlib.util.spec_from_file_location("script_func", file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.run


run_script("./parametric_scripts/fill.py")
run_script("./parametric_scripts/bouncing_dvd.py")
