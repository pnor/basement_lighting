#!/usr/bin/env python3

from backend.ceiling import Ceiling
from typing import Callable, Optional, List, Tuple
from multiprocessing import Process, Pipe
from multiprocessing.connection import _ConnectionBase

from backend.settings import Settings


def create_ceiling(s: Settings) -> Ceiling:
    if s.test_mode:
        assert s.camera_position is not None
        return Ceiling(
            type="test",
            rows=s.rows,
            number_lights=s.number_lights,
            dimensions=s.dimensions,
            arrangement_file=s.arrangement_file,
            sphere_size=s.sphere_size,
            camera_position=tuple(s.camera_position),
            dimension_mask=s.dimension_mask,
        )
    else:
        return Ceiling(
            type="ws281x",
            rows=s.rows,
            number_lights=s.number_lights,
            dimensions=s.dimensions,
            arrangement_file=s.arrangement_file,
            io_pin=s.io_pin,
        )


class State:
    def __init__(self) -> None:
        self.settings = Settings("settings.toml")

        self.current_process: Optional[Process] = None
        self.current_pattern: Optional[str] = None
        self.recv_pipe: Optional[_ConnectionBase] = None

        self.ceiling: Optional[Ceiling] = create_ceiling(self.settings)


global_state = State()
