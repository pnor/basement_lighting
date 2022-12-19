#!/usr/bin/env python3

from backend.ceiling import Ceiling
from typing import Callable, Optional, List, Tuple
from multiprocessing import Process, Pipe
from multiprocessing.connection import _ConnectionBase


class State:
    def __init__(self) -> None:
        self.current_process: Optional[Process] = None
        self.ceiling: Optional[Ceiling] = Ceiling(test_mode=True)
        self.recv_pipe: Optional[_ConnectionBase] = None


global_state = State()
