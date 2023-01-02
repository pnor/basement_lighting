#!/usr/bin/env python3

from backend.ceiling import Ceiling
from typing import Callable, Optional, List, Tuple
from multiprocessing import Process, Pipe
from multiprocessing.connection import _ConnectionBase
import colour


class State:
    def __init__(self) -> None:
        self.current_process: Optional[Process] = None
        self.current_pattern: Optional[str] = None
        self.ceiling: Optional[Ceiling] = Ceiling(test_mode=True)
        self.recv_pipe: Optional[_ConnectionBase] = None
        self.colors: List[colour.Color] = [
            colour.Color("#beebee"),
            colour.Color("red"),
            colour.Color("orange"),
            colour.Color("yellow"),
            colour.Color("green"),
            colour.Color("blue"),
            colour.Color("indigo"),
            colour.Color("violet"),
            colour.Color("purple"),
            colour.Color("cyan"),
            colour.Color("chartreuse"),
            colour.Color("pink"),
            colour.Color("white"),
            colour.Color("darkgrey"),
        ]
        self.color_index = 0

    def get_color_and_cycle(self) -> str:
        color = self.colors[self.color_index]
        self.color_index = (self.color_index + 1) % len(self.colors)
        return color.hex


global_state = State()
