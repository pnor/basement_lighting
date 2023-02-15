#!/usr/bin/env python3

from backend.ceiling import Ceiling
from typing import Callable, Optional, List, Tuple
from multiprocessing import Process, Pipe
from multiprocessing.connection import _ConnectionBase

from backend.settings import Settings


class State:
    def __init__(self) -> None:
        self.settings = Settings("settings.toml")

        self.current_process: Optional[Process] = None
        self.current_pattern: Optional[str] = None

    def create_ceiling(self) -> Ceiling:
        if self.settings.test_mode:
            assert self.settings.camera_position is not None
            return Ceiling(
                type="test",
                rows=self.settings.rows,
                number_lights=self.settings.number_lights,
                dimensions=self.settings.dimensions,
                arrangement_file=self.settings.arrangement_file,
                sphere_size=self.settings.sphere_size,
                camera_position=tuple(self.settings.camera_position),
                dimension_mask=self.settings.dimension_mask,
            )
        else:
            return Ceiling(
                type="ws281x",
                rows=self.settings.rows,
                number_lights=self.settings.number_lights,
                dimensions=self.settings.dimensions,
                arrangement_file=self.settings.arrangement_file,
                io_pin=self.settings.io_pin,
            )


global_state = State()
